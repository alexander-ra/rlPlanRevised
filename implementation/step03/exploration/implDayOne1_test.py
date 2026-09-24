"""
Test version of implDayOne1.py with reduced iterations (5k max).
Trains the chapter 2 custom CFR alongside MCCFR variants and OpenSpiel's CFR/CFR+
on Kuhn Poker.

Usage (any working directory):
    python exploration/implDayOne1_test.py              # seeded run: train, save cache, plot
    python exploration/implDayOne1_test.py --plot-only  # plot from the saved cache, no training
    PLOT_ONLY=1 python exploration/implDayOne1_test.py  # same; the BG figure renderer uses this,
                                                        # because it runs the script without args

Measurement conventions (September 2026 rerun):
  - Metric: exploitability = NashConv / 2 (OpenSpiel's `exploitability` for a
    two-player zero-sum game) for every curve, including the custom CFR, whose
    average strategy is wrapped in an OpenSpiel TabularPolicy. (The earlier
    custom-CFR curve plotted |average game value - (-1/18)|, which is not an
    exploitability.) NashConv is stored in the cache next to it.
  - Snapshots at 100 * 1.5^k iterations plus the final iteration.
  - `time_elapsed` is training time only; evaluation is excluded.
  - Every solver starts from the same seed (numpy + random).
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
STEP02_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', 'step02'))
relativePath = os.path.join(SCRIPT_DIR, "figures") + os.sep
CACHE_PATH = relativePath + 'kuhn_results_cache.json'

SEED = 42
MAX_STEPS = 5000

# (cache key, legend label, marker, colour) - colours as in the original figures
SERIES = [
    ('es_results', 'External Sampling MCCFR', 'o', '#1f77b4'),
    ('os_results', 'Outcome Sampling MCCFR', 's', '#ff7f0e'),
    ('customCFR_results', 'Custom CFR (chance-sampled, Chapter 2)', '^', 'red'),
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


def run_solver(name, game, policy_fn, step_fn, steps, expl):
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
            nash_conv = expl.nash_conv(game, policy_fn())
            exploit = nash_conv / game.num_players()
            results.append({'iteration': i, 'exploitability': exploit,
                            'nash_conv': nash_conv, 'time_elapsed': train_time})
            print(f"  {name:<8} - Iteration {i:>5}: exploitability = {exploit:.6f} "
                  f"(NashConv {nash_conv:.6f}, train {train_time:7.3f}s)", flush=True)
    return results


def load_kuhn_trainer():
    """Import chapter 2's KuhnTrainer. step03 has its own (regular) `cfr` package,
    which would win over step02's namespace package wherever it sits on sys.path,
    so it is hidden and any already-imported `cfr` modules are set aside while
    step02's are loaded."""
    saved = {k: sys.modules.pop(k) for k in list(sys.modules)
             if k == 'cfr' or k.startswith('cfr.')}
    saved_path = list(sys.path)
    sys.path[:] = [STEP02_DIR] + [
        p for p in sys.path
        if not os.path.isfile(os.path.join(p or '.', 'cfr', '__init__.py'))]
    try:
        from cfr.cfr_trainer import KuhnTrainer
    finally:
        sys.path[:] = saved_path
        for k in [k for k in sys.modules if k == 'cfr' or k.startswith('cfr.')]:
            sys.modules.pop(k)
        sys.modules.update(saved)
    return KuhnTrainer


def custom_policy_fn(game, trainer):
    """The custom trainer's average strategy as an OpenSpiel TabularPolicy.

    Chapter 2 deals cards 1..3 (J, Q, K) and keys an information set as
    str(card) + history ('p'/'b'); OpenSpiel's Kuhn uses cards 0..2 and the
    same history letters, with action 0 = pass, 1 = bet (as in chapter 2).
    """
    from open_spiel.python import policy as policy_lib

    def fn():
        pol = policy_lib.TabularPolicy(game)
        for key, node in trainer.node_map.items():
            os_key = f"{int(key[0]) - 1}{key[1:]}"
            pol.policy_for_key(os_key)[:] = node.get_average_strategy()
        return pol
    return fn


def train():
    import pyspiel
    import open_spiel
    from open_spiel.python.algorithms import cfr as cfr_module
    from open_spiel.python.algorithms import exploitability as expl
    from open_spiel.python.algorithms import external_sampling_mccfr
    from open_spiel.python.algorithms import outcome_sampling_mccfr

    game = pyspiel.load_game("kuhn_poker")
    steps = snapshot_steps(MAX_STEPS)
    print(f"KUHN POKER COMPARISON - {MAX_STEPS} iterations, seed {SEED}")
    print(f"Snapshot steps: {steps}\n")

    cache = {
        'meta': {
            'game': 'kuhn_poker',
            'seed': SEED,
            'max_steps': MAX_STEPS,
            'metric': 'exploitability = NashConv / 2 (OpenSpiel exploitability); '
                      'nash_conv stored alongside',
            'time_elapsed': 'training time only; exploitability evaluation excluded',
            'custom_cfr': 'chapter 2 KuhnTrainer (one random deal per iteration), '
                          'average strategy evaluated as a TabularPolicy',
            'openspiel_version': getattr(open_spiel, '__version__', 'unknown'),
            'generated': datetime.datetime.now().isoformat(timespec='seconds'),
        },
        'iterations': steps,
    }

    print("Running External Sampling MCCFR...")
    es = external_sampling_mccfr.ExternalSamplingSolver(game)
    cache['es_results'] = run_solver('ES', game, es.average_policy, es.iteration,
                                     steps, expl)

    print("\nRunning Outcome Sampling MCCFR...")
    osmc = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
    cache['os_results'] = run_solver('OS', game, osmc.average_policy, osmc.iteration,
                                     steps, expl)

    print("\nTraining custom CFR (chapter 2, chance-sampled)...")
    KuhnTrainer = load_kuhn_trainer()
    trainer = KuhnTrainer()
    cards = [1, 2, 3]

    def custom_step():
        random.shuffle(cards)
        trainer.cfr(cards, "", 1.0, 1.0)
    cache['customCFR_results'] = run_solver(
        'CFR', game, custom_policy_fn(game, trainer), custom_step, steps, expl)

    print("\nTraining OpenSpiel CFR...")
    cfr_solver = cfr_module.CFRSolver(game)
    cache['osCFR_results'] = run_solver(
        'OS-CFR', game, cfr_solver.average_policy,
        cfr_solver.evaluate_and_update_policy, steps, expl)

    print("\nTraining OpenSpiel CFR+...")
    cfrplus_solver = cfr_module.CFRPlusSolver(game)
    cache['osCFRPlus_results'] = run_solver(
        'OS-CFR+', game, cfrplus_solver.average_policy,
        cfrplus_solver.evaluate_and_update_policy, steps, expl)

    with open(CACHE_PATH, 'w') as f:
        json.dump(cache, f, indent=2)
    print(f"\nResults cached to '{CACHE_PATH}'")
    return cache


def _limits(values, lo_pad=0.5, hi_pad=2.0, floor=1e-6):
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
    plot1_path = relativePath + 'kuhn_exploitability_iterations.png'
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
    plt.xlim(_limits(all_times, lo_pad=0.8, hi_pad=1.2, floor=1e-4))
    plt.ylim(_limits(all_exploits))
    plt.xlabel('Training time (seconds, log scale)', fontsize=11)
    plt.ylabel('Exploitability (log scale)', fontsize=11)
    plt.tick_params(labelsize=10)
    _legend_below()
    plt.grid(True, which="both", ls="--")
    plot2_path = relativePath + 'kuhn_exploitability_time.png'
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
