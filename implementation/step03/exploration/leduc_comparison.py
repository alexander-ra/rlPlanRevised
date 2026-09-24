"""
Leduc Poker comparison: MCCFR variants and OpenSpiel's CFR/CFR+ implementations.
Similar to Kuhn poker test but for the larger Leduc poker game.
No custom CFR implementation (would be too complex for Leduc).

Usage (any working directory):
    python exploration/leduc_comparison.py              # seeded run: train, save cache, plot
    python exploration/leduc_comparison.py --plot-only  # plot from the saved cache, no training
    PLOT_ONLY=1 python exploration/leduc_comparison.py  # same; the BG figure renderer uses this,
                                                        # because it runs the script without args

Measurement conventions (September 2026 rerun):
  - Metric: exploitability = NashConv / 2 (OpenSpiel's `exploitability` for a
    two-player zero-sum game) - the same quantity as the custom evaluator
    (evaluate/exploitability.py) and the timed benchmark (cfr/train_all_timed.py).
    NashConv itself is stored in the cache next to it.
  - Snapshots at 100 * 1.5^k iterations plus the final iteration, so the curve
    ends at MAX_STEPS.
  - `time_elapsed` is training time only: the clock is paused while a snapshot's
    exploitability is computed (as in cfr/train_all_timed.py).
  - Every solver starts from the same seed (numpy + random), so a rerun
    reproduces the sampled MCCFR curves.
"""
import datetime
import json
import os
import random
import sys
import time

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
relativePath = os.path.join(SCRIPT_DIR, "figures") + os.sep
CACHE_PATH = relativePath + 'leduc_results_cache.json'

SEED = 42
MAX_STEPS = 5000

# (cache key, legend label, marker, colour) - colours as in the original figures
SERIES = [
    ('es_results', 'External Sampling MCCFR', 'o', '#1f77b4'),
    ('os_results', 'Outcome Sampling MCCFR', 's', '#ff7f0e'),
    ('osCFR_results', 'OpenSpiel CFR', 'D', 'green'),
    ('osCFRPlus_results', 'OpenSpiel CFR+', 'v', 'purple'),
]


def snapshot_steps(max_steps: int) -> list[int]:
    """100, 150, 225, ... (x1.5) up to max_steps, always ending at max_steps."""
    steps = [100]
    while steps[-1] < max_steps:
        steps.append(int(steps[-1] * 1.5))
    steps = [s for s in steps if s <= max_steps]
    if steps[-1] != max_steps:
        steps.append(max_steps)
    return steps


def run_solver(name, game, solver, step_fn, steps, expl):
    """Train one solver with a fixed seed; snapshot exploitability at `steps`."""
    random.seed(SEED)
    np.random.seed(SEED)
    wanted = set(steps)
    results = []
    train_time = 0.0
    for i in range(1, steps[-1] + 1):
        t0 = time.perf_counter()
        step_fn()
        train_time += time.perf_counter() - t0
        if i in wanted:
            nash_conv = expl.nash_conv(game, solver.average_policy())
            exploit = nash_conv / game.num_players()
            results.append({'iteration': i, 'exploitability': exploit,
                            'nash_conv': nash_conv, 'time_elapsed': train_time})
            print(f"  {name:<8} - Iteration {i:>5}: exploitability = {exploit:.6f} "
                  f"(NashConv {nash_conv:.6f}, train {train_time:7.2f}s)", flush=True)
    return results


def train():
    import pyspiel
    import open_spiel
    from open_spiel.python.algorithms import cfr as cfr_module
    from open_spiel.python.algorithms import exploitability as expl
    from open_spiel.python.algorithms import external_sampling_mccfr
    from open_spiel.python.algorithms import outcome_sampling_mccfr

    game = pyspiel.load_game("leduc_poker")
    steps = snapshot_steps(MAX_STEPS)
    print("=" * 60)
    print(f"LEDUC POKER COMPARISON - {MAX_STEPS} iterations, seed {SEED}")
    print("=" * 60)
    print(f"Snapshot steps: {steps}\n")

    cache = {
        'meta': {
            'game': 'leduc_poker',
            'seed': SEED,
            'max_steps': MAX_STEPS,
            'metric': 'exploitability = NashConv / 2 (OpenSpiel exploitability); '
                      'nash_conv stored alongside',
            'time_elapsed': 'training time only; exploitability evaluation excluded',
            'openspiel_version': getattr(open_spiel, '__version__', 'unknown'),
            'generated': datetime.datetime.now().isoformat(timespec='seconds'),
        },
        'iterations': steps,
    }

    print("Running External Sampling MCCFR...")
    es = external_sampling_mccfr.ExternalSamplingSolver(game)
    cache['es_results'] = run_solver('ES', game, es, es.iteration, steps, expl)

    print("\nRunning Outcome Sampling MCCFR...")
    osmc = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
    cache['os_results'] = run_solver('OS', game, osmc, osmc.iteration, steps, expl)

    print("\nTraining OpenSpiel CFR...")
    cfr_solver = cfr_module.CFRSolver(game)
    cache['osCFR_results'] = run_solver(
        'OS-CFR', game, cfr_solver, cfr_solver.evaluate_and_update_policy, steps, expl)

    print("\nTraining OpenSpiel CFR+...")
    cfrplus_solver = cfr_module.CFRPlusSolver(game)
    cache['osCFRPlus_results'] = run_solver(
        'OS-CFR+', game, cfrplus_solver, cfrplus_solver.evaluate_and_update_policy,
        steps, expl)

    with open(CACHE_PATH, 'w') as f:
        json.dump(cache, f, indent=2)
    print(f"\nResults cached to '{CACHE_PATH}'")
    return cache


def _limits(values, lo_pad=0.8, hi_pad=1.5, floor=1e-6):
    positive = [v for v in values if v > 0] or [floor]
    return min(positive) * lo_pad, max(values) * hi_pad


def _legend_below():
    # Below the axes: inside, it hid a curve whatever corner it was put in.
    plt.legend(fontsize=10, loc='upper center', bbox_to_anchor=(0.5, -0.17),
               ncol=2, frameon=False)


def plot(cache):
    iterations = cache['iterations']
    curves = [(label, marker, color,
               [r['exploitability'] for r in cache.get(key, [])],
               [r['time_elapsed'] for r in cache.get(key, [])])
              for key, label, marker, color in SERIES]
    curves = [c for c in curves if c[3]]
    all_exploits = [e for c in curves for e in c[3]]

    # Plot 1: exploitability vs iterations
    plt.figure(figsize=(8, 5))
    for label, marker, color, ys, _ in curves:
        plt.plot(iterations, ys, label=label, marker=marker, linewidth=2, color=color)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim([min(iterations) * 0.8, max(iterations) * 1.2])
    plt.ylim(_limits(all_exploits))
    plt.xlabel('Iterations (log scale)', fontsize=11)
    plt.ylabel('Exploitability (log scale)', fontsize=11)
    plt.tick_params(labelsize=10)
    _legend_below()
    plt.grid(True, which="both", ls="--")
    plot1_path = relativePath + 'leduc_exploitability_iterations.png'
    plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved: {plot1_path}")
    plt.close()

    # Plot 2: exploitability vs training time
    plt.figure(figsize=(8, 5))
    for label, marker, color, ys, xs in curves:
        plt.plot(xs, ys, label=label, marker=marker, linewidth=2, color=color)
    plt.xscale('log')
    plt.yscale('log')
    all_times = [t for c in curves for t in c[4]]
    plt.xlim(_limits(all_times, floor=1e-3))
    plt.ylim(_limits(all_exploits))
    plt.xlabel('Training time (seconds, log scale)', fontsize=11)
    plt.ylabel('Exploitability (log scale)', fontsize=11)
    plt.tick_params(labelsize=10)
    _legend_below()
    plt.grid(True, which="both", ls="--")
    plot2_path = relativePath + 'leduc_exploitability_time.png'
    plt.savefig(plot2_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved: {plot2_path}")
    plt.close()


def main():
    plot_only = os.environ.get("PLOT_ONLY") == "1" or "--plot-only" in sys.argv
    if plot_only:
        with open(CACHE_PATH) as f:
            cache = json.load(f)
        print(f"Plot-only: loaded '{CACHE_PATH}'")
    else:
        cache = train()
    plot(cache)


if __name__ == "__main__":
    main()
