"""
MCCFR (Monte Carlo Counterfactual Regret Minimization) on Kuhn Poker
Explores two sampling types: External Sampling vs Outcome Sampling

Algorithm Overview:
- Standard CFR traverses the full game tree → expensive O(|T|) per update
- MCCFR samples histories stochastically → exploits tree sparsity
- Both types converge to Nash equilibrium at O(1/√T) rate

External Sampling:
  • Sample external (chance) nodes only when not in reach of agents being trained
  • Lower variance on counterfactual regrets
  • Explores less frequently visited paths
  • Good baseline for convergence study

Outcome Sampling:
  • Sample outcomes from current policy distribution
  • Higher variance but often faster convergence in practice
  • Explores current policy more intensively
  • Useful for online learning scenarios
"""

import pyspiel
from open_spiel.python.algorithms import external_sampling_mccfr
from open_spiel.python.algorithms import outcome_sampling_mccfr
from open_spiel.python.algorithms import exploitability as expl
from open_spiel.python import policy as policy_module
import time
import json


def run_mccfr_variants(num_iterations=10000, seed=42):
    game = pyspiel.load_game("kuhn_poker")
    results = {}
    
    print("="*70)
    print("MCCFR SAMPLING COMPARISON ON KUHN POKER")
    print("="*70)
    
    # ─────────────────────────────────────────────────────────────
    # 1. EXTERNAL SAMPLING MCCFR
    # ─────────────────────────────────────────────────────────────
    print("\n[1/2] EXTERNAL SAMPLING MCCFR")
    print("-" * 70)
    print("Sampling Strategy:")
    print("  • Sample outcomes from chance nodes (card deals)")
    print("  • Use deterministic best response for agent decisions")
    print("  • Lower variance on regret estimates")
    print("  • Typically slower to converge in practice")
    
    start_time = time.time()
    es_solver = external_sampling_mccfr.ExternalSamplingSolver(game)
    
    es_record = []
    for i in range(num_iterations):
        es_solver.iteration()
        
        # Periodic logging for convergence analysis
        if (i + 1) % 1000 == 0:
            es_policy = es_solver.average_policy()
            es_exploit = expl.nash_conv(game, es_policy)
            es_record.append({
                'iteration': i + 1,
                'exploitability': es_exploit
            })
            print(f"  Iter {i+1:5d} | Exploitability: {es_exploit:.6f}")
    
    es_time = time.time() - start_time
    es_final = es_solver.average_policy()
    es_final_exploit = expl.nash_conv(game, es_final)
    
    results['external_sampling'] = {
        'final_exploitability': es_final_exploit,
        'time_seconds': es_time,
        'convergence': es_record
    }
    
    print(f"\n  Final Exploitability: {es_final_exploit:.6f}")
    print(f"  Time: {es_time:.2f}s")
    
    # ─────────────────────────────────────────────────────────────
    # 2. OUTCOME SAMPLING MCCFR
    # ─────────────────────────────────────────────────────────────
    print("\n[2/2] OUTCOME SAMPLING MCCFR")
    print("-" * 70)
    print("Sampling Strategy:")
    print("  • Sample outcomes from BOTH chance AND agent actions")
    print("  • Use current policy to sample agent plays")
    print("  • Higher variance but faster exploration")
    print("  • Often converges quicker in practice")
    
    start_time = time.time()
    os_solver = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
    
    os_record = []
    for i in range(num_iterations):
        os_solver.iteration()
        
        # Periodic logging for convergence analysis
        if (i + 1) % 1000 == 0:
            os_policy = os_solver.average_policy()
            os_exploit = expl.nash_conv(game, os_policy)
            os_record.append({
                'iteration': i + 1,
                'exploitability': os_exploit
            })
            print(f"  Iter {i+1:5d} | Exploitability: {os_exploit:.6f}")
    
    os_time = time.time() - start_time
    os_final = os_solver.average_policy()
    os_final_exploit = expl.nash_conv(game, os_final)
    
    results['outcome_sampling'] = {
        'final_exploitability': os_final_exploit,
        'time_seconds': os_time,
        'convergence': os_record
    }
    
    print(f"\n  Final Exploitability: {os_final_exploit:.6f}")
    print(f"  Time: {os_time:.2f}s")
    
    # ─────────────────────────────────────────────────────────────
    # 3. COMPARISON & ANALYSIS
    # ─────────────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70)
    
    print(f"\nExternal Sampling:")
    print(f"  Exploitability: {es_final_exploit:.6f}")
    print(f"  Time: {es_time:.2f}s")
    print(f"  [Reference: Nash equilibrium exploitability ≈ 0.0]")
    
    print(f"\nOutcome Sampling:")
    print(f"  Exploitability: {os_final_exploit:.6f}")
    print(f"  Time: {os_time:.2f}s")
    
    difference = abs(es_final_exploit - os_final_exploit)
    print(f"\nDifference: {difference:.6f}")
    
    speedup = es_time / os_time if os_time > 0 else 1.0
    print(f"Outcome Sampling speedup: {speedup:.2f}x")
    
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)
    print("• Both converge to Nash equilibrium (exploitability → 0)")
    print("• Outcome Sampling typically converges faster (lower bias)")
    print("• External Sampling has lower variance but explores less")
    print("• Choice depends on problem structure & computational budget")
    
    return results


if __name__ == "__main__":
    # Run comparison with 10k iterations each
    results = run_mccfr_variants(num_iterations=10000, seed=42)
    
    # Optional: Save results for further analysis
    output_file = "mccfr_comparison_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Results saved to {output_file}")

