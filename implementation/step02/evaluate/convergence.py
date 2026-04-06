"""
Convergence analysis: exploitability vs CFR iterations.

Trains CFR at multiple checkpoints and plots exploitability on a
log-log scale, verifying O(1/√T) convergence (slope ≈ -0.5).

Usage:
    cd implementation/step02
    python evaluate/convergence.py
"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
step02_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step02_dir)

from config import CFR_CONFIG
from cfr.cfr_trainer import KuhnTrainer
from evaluate.exploitability import compute_exploitability
from utils.plotting import create_exploitability_chart


def run_convergence_analysis(checkpoints: list[int] = None) -> tuple:
    """
    Train CFR at each checkpoint and measure exploitability.

    Returns:
        (checkpoints, exploitabilities) — lists of matching length
    """
    if checkpoints is None:
        checkpoints = CFR_CONFIG["convergence_checkpoints"]

    exploitabilities = []

    for iters in checkpoints:
        trainer = KuhnTrainer()
        trainer.train(iters)
        exploit = compute_exploitability(trainer.node_map)
        exploitabilities.append(exploit)
        print(f"  Iterations: {iters:>7,}  |  Exploitability: {exploit:.6f}")

    return checkpoints, exploitabilities


def main():
    print("\n  CFR Convergence Analysis")
    print("  " + "=" * 50)
    print(f"  Checkpoints: {CFR_CONFIG['convergence_checkpoints']}")
    print()

    checkpoints, exploitabilities = run_convergence_analysis()

    # Compute log-log slope
    import numpy as np
    if len(checkpoints) >= 2:
        log_x = np.log10(checkpoints)
        log_y = np.log10(exploitabilities)
        slope = np.polyfit(log_x, log_y, 1)[0]
        print(f"\n  Log-log slope: {slope:.3f}")
        print(f"  Expected (O(1/√T)): -0.500")
        print(f"  Match: {'✓ Good' if -0.7 < slope < -0.3 else '✗ Investigate'}")

    # Save figure
    figures_dir = os.path.join(step02_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    create_exploitability_chart(checkpoints, exploitabilities, figures_dir)

    print()


if __name__ == "__main__":
    main()
