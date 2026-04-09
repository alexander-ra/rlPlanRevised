"""
Advanced MCCFR Analysis: Strategy Comparison and Convergence Visualization
Extracts learned strategies from both MCCFR variants and compares them.
"""

import pyspiel
from open_spiel.python.algorithms import external_sampling_mccfr
from open_spiel.python.algorithms import outcome_sampling_mccfr
from open_spiel.python.algorithms import exploitability as expl
import json
import numpy as np
import time


def extract_strategy_from_policy(policy, game):
    """
    Extract human-readable strategy from OpenSpiel policy.
    For Kuhn Poker: Shows action probabilities for each information set.
    """
    game_type = game.get_type().short_name
    
    if game_type != "kuhn_poker":
        return None
    
    strategy_dict = {}
    
    # Iterate through all states and extract policy info
    for state_id, policy_data in policy.state_dict.items():
        if state_data is None:
            continue
        
        # Parse state string to understand game situation
        # Kuhn poker state: cardP0 cardP1 (history)
        strategy_dict[state_id] = policy_data
    
    return strategy_dict


def analyze_convergence(records, name=""):
    """Compute convergence statistics from iteration records."""
    if not records:
        return {}
    
    exps = [r['exploitability'] for r in records]
    iters = [r['iteration'] for r in records]
    
    # Rate of convergence: approximate O(1/√T)
    # Log-log slope should be ~-0.5
    log_exps = np.log(np.array(exps) + 1e-8)
    log_iters = np.log(np.array(iters) + 1e-8)
    
    if len(log_iters) > 1:
        slope = np.polyfit(log_iters, log_exps, 1)[0]
    else:
        slope = 0
    
    stats = {
        'name': name,
        'final_exploitability': exps[-1],
        'initial_exploitability': exps[0],
        'improvement': exps[0] - exps[-1],
        'num_records': len(records),
        'convergence_slope_loglog': slope,
        'expected_slope': -0.5,
        'slope_error': abs(slope - (-0.5))
    }
    
    return stats


def compare_sampling_variance(num_runs=5, num_iters=5000):
    """
    Run multiple independent MCCFR solvers to estimate sampling variance.
    Higher variance = more noise in individual runs.
    """
    game = pyspiel.load_game("kuhn_poker")
    
    print("\n" + "="*70)
    print("VARIANCE ANALYSIS: Multiple Independent Runs")
    print("="*70)
    print(f"Running {num_runs} independent solvers for {num_iters} iterations each...")
    print()
    
    es_exploits = []
    os_exploits = []
    
    for run in range(num_runs):
        seed = 42 + run
        
        # External Sampling
        es_solver = external_sampling_mccfr.ExternalSamplingSolver(game)
        for _ in range(num_iters):
            es_solver.iteration()
        es_policy = es_solver.average_policy()
        es_exploit = expl.nash_conv(game, es_policy)
        es_exploits.append(es_exploit)
        
        # Outcome Sampling
        os_solver = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
        for _ in range(num_iters):
            os_solver.iteration()
        os_policy = os_solver.average_policy()
        os_exploit = expl.nash_conv(game, os_policy)
        os_exploits.append(os_exploit)
        
        print(f"Run {run+1}: ES={es_exploit:.6f}, OS={os_exploit:.6f}")
    
    es_array = np.array(es_exploits)
    os_array = np.array(os_exploits)
    
    print("\n" + "-"*70)
    print("VARIANCE STATISTICS")
    print("-"*70)
    
    print(f"\nExternal Sampling:")
    print(f"  Mean exploitability: {es_array.mean():.6f}")
    print(f"  Std deviation:      {es_array.std():.6f}")
    print(f"  Min: {es_array.min():.6f}, Max: {es_array.max():.6f}")
    print(f"  Range: {es_array.max() - es_array.min():.6f}")
    
    print(f"\nOutcome Sampling:")
    print(f"  Mean exploitability: {os_array.mean():.6f}")
    print(f"  Std deviation:      {os_array.std():.6f}")
    print(f"  Min: {os_array.min():.6f}, Max: {os_array.max():.6f}")
    print(f"  Range: {os_array.max() - os_array.min():.6f}")
    
    # Analysis
    es_cv = es_array.std() / (es_array.mean() + 1e-8)  # Coefficient of variation
    os_cv = os_array.std() / (os_array.mean() + 1e-8)
    
    print(f"\nCoefficient of Variation (lower = more stable):")
    print(f"  External Sampling: {es_cv:.4f}")
    print(f"  Outcome Sampling:  {os_cv:.4f}")
    
    if es_cv < os_cv:
        print(f"  → External Sampling is {os_cv/es_cv:.2f}x more stable")
    else:
        print(f"  → Outcome Sampling is {es_cv/os_cv:.2f}x more stable")
    
    return {
        'external_sampling_runs': es_exploits,
        'outcome_sampling_runs': os_exploits,
        'external_stats': {
            'mean': float(es_array.mean()),
            'std': float(es_array.std()),
            'min': float(es_array.min()),
            'max': float(es_array.max()),
            'cv': float(es_cv)
        },
        'outcome_stats': {
            'mean': float(os_array.mean()),
            'std': float(os_array.std()),
            'min': float(os_array.min()),
            'max': float(os_array.max()),
            'cv': float(os_cv)
        }
    }


def iteration_cost_analysis():
    """
    Analyze computational cost per iteration.
    Compare wall-clock time per sampled history.
    """
    game = pyspiel.load_game("kuhn_poker")
    
    print("\n" + "="*70)
    print("ITERATION COST ANALYSIS")
    print("="*70)
    
    # Time 1000 iterations for each
    import time
    
    iterations = 1000
    
    print(f"\nMeasuring time for {iterations} iterations...\n")
    
    # External Sampling
    start = time.time()
    es_solver = external_sampling_mccfr.ExternalSamplingSolver(game)
    for _ in range(iterations):
        es_solver.iteration()
    es_time = time.time() - start
    
    # Outcome Sampling
    start = time.time()
    os_solver = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
    for _ in range(iterations):
        os_solver.iteration()
    os_time = time.time() - start
    
    print(f"External Sampling: {es_time:.4f}s ({es_time/iterations*1000:.4f}ms per iter)")
    print(f"Outcome Sampling:  {os_time:.4f}s ({os_time/iterations*1000:.4f}ms per iter)")
    
    if es_time > 0:
        ratio = os_time / es_time
        print(f"\nOutcome Sampling is {ratio:.2f}x the time of External Sampling")
        if ratio > 1:
            print(f"  (Outcome Sampling has {(ratio-1)*100:.1f}% overhead)")
        else:
            print(f"  (Outcome Sampling is {(1-ratio)*100:.1f}% faster)")
    
    return {
        'external_time_s': es_time,
        'outcome_time_s': os_time,
        'external_ms_per_iter': es_time / iterations * 1000,
        'outcome_ms_per_iter': os_time / iterations * 1000
    }


if __name__ == "__main__":
    # Run variance analysis
    variance_results = compare_sampling_variance(num_runs=5, num_iters=5000)
    
    # Run iteration cost analysis
    cost_results = iteration_cost_analysis()
    
    # Save results
    all_results = {
        'variance_analysis': variance_results,
        'cost_analysis': cost_results
    }
    
    with open('mccfr_detailed_analysis.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "="*70)
    print("✓ Analysis complete. Results saved to mccfr_detailed_analysis.json")
    print("="*70)
