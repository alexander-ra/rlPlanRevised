"""
Convergence analysis: exploitability vs CFR iterations for Leduc Poker.

Usage:
    cd implementation/step03
    python evaluate/convergence.py
"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
step03_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step03_dir)

from config import CFR_CONFIG
from cfr.cfr_trainer import LeducTrainer
from evaluate.exploitability import compute_exploitability
from utils.plotting import create_exploitability_chart


def run_convergence_analysis(checkpoints: list[int] = None) -> tuple:
    if checkpoints is None:
        checkpoints = CFR_CONFIG["convergence_checkpoints"]

    exploitabilities = []

    for iters in checkpoints:
        trainer = LeducTrainer()
        trainer.train(iters)
        exploit = compute_exploitability(trainer.node_map)
        exploitabilities.append(exploit)
        print(f"  Iterations: {iters:>7,}  |  Exploitability: {exploit:.6f}"
              f"  |  Info sets: {len(trainer.node_map)}")

    return checkpoints, exploitabilities


def main():
    print("\n  Leduc Poker — CFR Convergence Analysis")
    print("  " + "=" * 50)
    print(f"  Checkpoints: {CFR_CONFIG['convergence_checkpoints']}")
    print()

    checkpoints, exploitabilities = run_convergence_analysis()

    import numpy as np
    if len(checkpoints) >= 2:
        log_x = np.log10(checkpoints)
        log_y = np.log10(exploitabilities)
        slope = np.polyfit(log_x, log_y, 1)[0]
        print(f"\n  Log-log slope: {slope:.3f}")
        print(f"  Expected (O(1/√T)): -0.500")
        print(f"  Match: {'✓ Good' if -0.7 < slope < -0.3 else '✗ Investigate'}")

    figures_dir = os.path.join(step03_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    create_exploitability_chart(checkpoints, exploitabilities, figures_dir)

    print()


if __name__ == "__main__":
    main()
