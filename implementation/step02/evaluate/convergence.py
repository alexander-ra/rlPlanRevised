"""
Convergence analysis: exploitability vs CFR iterations.

Trains CFR once per seed (5 seeds), measures the exploitability of the
average strategy at log-spaced checkpoints, saves the curves to
models/convergence.json and plots them on a log-log scale against the
O(1/√T) reference (slope -0.5).

Usage:
    cd implementation/step02
    python evaluate/convergence.py
"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
step02_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step02_dir)

import json
import random

import numpy as np

from config import CFR_CONFIG
from cfr.cfr_trainer import KuhnTrainer
from evaluate.exploitability import compute_exploitability
from utils.plotting import create_exploitability_chart

RESULTS_PATH = os.path.join(step02_dir, "models", "convergence.json")


def run_convergence_analysis(checkpoints: list[int] = None,
                             seeds: list[int] = None) -> dict:
    """
    For each seed, train ONE trainer incrementally and measure the
    exploitability of its average strategy at every checkpoint.

    trainer.train(n) continues from the regret and strategy sums already in
    node_map, so each seed gives one continuing run measured at every
    checkpoint, not one independent run per point. (train() restarts its card
    list at each call, so the deal sequence differs from a single
    trainer.train(100_000) with the same seed - statistically the same
    process, not the same numbers as cfr/train.py.)

    Returns:
        dict with checkpoints, per-seed exploitabilities, their mean/min/max,
        and the log-log slope per seed and of the mean curve
    """
    if checkpoints is None:
        checkpoints = CFR_CONFIG["convergence_checkpoints"]
    if seeds is None:
        seeds = CFR_CONFIG["convergence_seeds"]

    per_seed = []
    for seed in seeds:
        random.seed(seed)
        trainer = KuhnTrainer()
        done = 0
        curve = []
        for cp in checkpoints:
            trainer.train(cp - done)
            done = cp
            exploit = compute_exploitability(trainer.node_map)
            curve.append(exploit)
            print(f"  seed {seed}  iterations {cp:>7,}  |  "
                  f"exploitability {exploit:.6f}", flush=True)
        per_seed.append(curve)

    arr = np.array(per_seed)
    log_x = np.log10(checkpoints)
    slopes = [float(np.polyfit(log_x, np.log10(c), 1)[0]) for c in per_seed]
    mean = arr.mean(axis=0)
    return {
        "checkpoints": list(checkpoints),
        "seeds": list(seeds),
        "per_seed": arr.tolist(),
        "exploitabilities": mean.tolist(),        # mean over seeds
        "min": arr.min(axis=0).tolist(),
        "max": arr.max(axis=0).tolist(),
        "slopes_per_seed": slopes,
        "slope_mean": float(np.mean(slopes)),
        "slope_sd": float(np.std(slopes, ddof=1)) if len(slopes) > 1 else 0.0,
        "slope_of_mean_curve": float(np.polyfit(log_x, np.log10(mean), 1)[0]),
    }


def main():
    print("\n  CFR Convergence Analysis")
    print("  " + "=" * 50)
    print(f"  Checkpoints: {CFR_CONFIG['convergence_checkpoints']}")
    print(f"  Seeds:       {CFR_CONFIG['convergence_seeds']}")
    print()

    res = run_convergence_analysis()

    print("\n  Log-log slope per seed: "
          + ", ".join(f"{s:.3f}" for s in res["slopes_per_seed"]))
    print(f"  Mean +- SD:             {res['slope_mean']:.3f} +- {res['slope_sd']:.3f}")
    print(f"  Slope of the mean curve: {res['slope_of_mean_curve']:.3f}")
    print(f"  Reference (O(1/sqrt T)): -0.500")

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(res, f, indent=2)
    print(f"  Results saved to: {RESULTS_PATH}")

    # Save figure (redraw later without retraining: python utils/plotting.py)
    figures_dir = os.path.join(step02_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    create_exploitability_chart(res["checkpoints"], res["exploitabilities"],
                                figures_dir, lo=res["min"], hi=res["max"])

    print()


if __name__ == "__main__":
    main()
