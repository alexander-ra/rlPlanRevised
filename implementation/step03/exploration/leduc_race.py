"""
LEDUC POKER — FINAL RACE: CFR+ vs External Sampling vs Outcome Sampling MCCFR
==============================================================================
5-minute race per algorithm with 10-second progress tracking.
Linear axes. CFR+ and OS-MCCFR loaded from cache if available.

Usage:
    cd implementation/step03/exploration
    python leduc_race.py

Requirements:
    - OpenSpiel (pyspiel)
    - matplotlib
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pyspiel
except ImportError as e:
    print(f"ERROR: Could not import pyspiel. {e}")
    sys.exit(1)

try:
    from open_spiel.python.algorithms import cfr as cfr_module
    from open_spiel.python.algorithms import outcome_sampling_mccfr
    from open_spiel.python.algorithms import external_sampling_mccfr
    from open_spiel.python.algorithms import exploitability
    CFRPlusSolver = cfr_module.CFRPlusSolver
except ImportError as e:
    print(f"ERROR: Could not import from open_spiel.python.algorithms. {e}")
    sys.exit(1)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')


# ============================================================================
# RUNNER (shared by all algorithms)
# ============================================================================

def run_algorithm(label, solver, game_string, num_seconds=300, checkpoint_interval=10):
    """
    Run any OpenSpiel solver for num_seconds, checkpointing every checkpoint_interval.
    solver must have .iteration() and .average_policy() methods.
    Returns: list of (time_elapsed, exploitability)
    """
    game = pyspiel.load_game(game_string)
    history = []
    start_time = time.time()
    last_checkpoint = 0
    iteration_count = 0

    while True:
        elapsed = time.time() - start_time
        if elapsed >= num_seconds:
            break
        solver.iteration()
        iteration_count += 1
        if elapsed - last_checkpoint >= checkpoint_interval:
            conv = exploitability.nash_conv(game, solver.average_policy())
            history.append((elapsed, conv))
            last_checkpoint = elapsed
            print(f"  {label:20s} {elapsed:6.1f}s  iter {iteration_count:7d}  exploit = {conv:.6f}")

    elapsed = time.time() - start_time
    conv = exploitability.nash_conv(game, solver.average_policy())
    history.append((elapsed, conv))
    print(f"  {label:20s} {elapsed:6.1f}s  iter {iteration_count:7d}  exploit = {conv:.6f}  [FINAL]")
    return history


def run_cfr_plus(game_string, num_seconds, checkpoint_interval):
    game = pyspiel.load_game(game_string)
    solver = CFRPlusSolver(game)
    # CFRPlusSolver uses evaluate_and_update_policy, not iteration
    history = []
    start_time = time.time()
    last_checkpoint = 0
    iteration_count = 0
    label = "CFR+"
    while True:
        elapsed = time.time() - start_time
        if elapsed >= num_seconds:
            break
        solver.evaluate_and_update_policy()
        iteration_count += 1
        if elapsed - last_checkpoint >= checkpoint_interval:
            conv = exploitability.nash_conv(game, solver.average_policy())
            history.append((elapsed, conv))
            last_checkpoint = elapsed
            print(f"  {label:20s} {elapsed:6.1f}s  iter {iteration_count:7d}  exploit = {conv:.6f}")
    elapsed = time.time() - start_time
    conv = exploitability.nash_conv(game, solver.average_policy())
    history.append((elapsed, conv))
    print(f"  {label:20s} {elapsed:6.1f}s  iter {iteration_count:7d}  exploit = {conv:.6f}  [FINAL]")
    return history


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*70)
    print("LEDUC POKER — RACE: CFR+ vs External Sampling vs Outcome Sampling")
    print("="*70)
    print("Config: 5 minutes each, checkpoint every 10 seconds, linear axes\n")

    game_string = "leduc_poker"
    num_seconds = 300
    checkpoint_interval = 10

    os.makedirs(FIGURES_DIR, exist_ok=True)
    cache_path = os.path.join(FIGURES_DIR, 'leduc_race_cache.json')

    # Load existing cache for CFR+ and OS if available
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            cache = json.load(f)
        print(f"Loaded existing cache from {cache_path}")

    # ---- CFR+ (cached) ----
    if 'cfr_plus' in cache:
        print("CFR+: using cached results.")
        cfr_plus_times   = cache['cfr_plus']['times']
        cfr_plus_exploits = cache['cfr_plus']['exploits']
    else:
        print("Training CFR+...")
        cfr_plus_history  = run_cfr_plus(game_string, num_seconds, checkpoint_interval)
        cfr_plus_times    = [t for t, _ in cfr_plus_history]
        cfr_plus_exploits = [e for _, e in cfr_plus_history]

    # ---- Outcome Sampling MCCFR (cached) ----
    if 'outcome_sampling' in cache:
        print("Outcome Sampling MCCFR: using cached results.")
        os_times    = cache['outcome_sampling']['times']
        os_exploits = cache['outcome_sampling']['exploits']
    else:
        print("\nTraining Outcome Sampling MCCFR...")
        game = pyspiel.load_game(game_string)
        os_solver   = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
        os_history  = run_algorithm("OS-MCCFR", os_solver, game_string, num_seconds, checkpoint_interval)
        os_times    = [t for t, _ in os_history]
        os_exploits = [e for _, e in os_history]

    # ---- External Sampling MCCFR (always run) ----
    print("\nTraining External Sampling MCCFR...")
    game = pyspiel.load_game(game_string)
    es_solver  = external_sampling_mccfr.ExternalSamplingSolver(game)
    es_history = run_algorithm("ES-MCCFR", es_solver, game_string, num_seconds, checkpoint_interval)
    es_times    = [t for t, _ in es_history]
    es_exploits = [e for _, e in es_history]

    # ========================================================================
    # PLOT: Exploitability vs Time (Linear)
    # ========================================================================
    print("\nCreating plot (linear axes)...")
    plt.figure(figsize=(14, 7))
    plt.plot(cfr_plus_times, cfr_plus_exploits,
             label='CFR+', marker='o', linewidth=2, color='blue', markersize=5)
    plt.plot(es_times, es_exploits,
             label='External Sampling MCCFR', marker='^', linewidth=2, color='green', markersize=5)
    plt.plot(os_times, os_exploits,
             label='Outcome Sampling MCCFR', marker='s', linewidth=2, color='orange', markersize=5)

    plt.xlabel('Wall-clock time (seconds)', fontsize=12)
    plt.ylabel('Exploitability (Nash Conv)', fontsize=12)
    plt.title('Leduc Poker — 5-Minute Race: CFR+ vs ES-MCCFR vs OS-MCCFR', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, ls="--", alpha=0.6)
    plt.tight_layout()

    plot_path = os.path.join(FIGURES_DIR, 'leduc_race_time.png')
    plt.savefig(plot_path, dpi=150)
    print(f"✓ Plot saved: {plot_path}")
    plt.close()

    # ========================================================================
    # SAVE CACHE (full)
    # ========================================================================
    cache = {
        'cfr_plus':         {'times': cfr_plus_times,  'exploits': cfr_plus_exploits},
        'external_sampling': {'times': es_times,         'exploits': es_exploits},
        'outcome_sampling':  {'times': os_times,         'exploits': os_exploits},
    }
    with open(cache_path, 'w') as f:
        json.dump(cache, f, indent=2)
    print(f"✓ Cache saved: {cache_path}")

    print("\n" + "="*70)
    print("RACE COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
