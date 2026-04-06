"""
Training entrypoint for Kuhn Poker CFR.

Usage:
    cd implementation/step02
    python cfr/train.py                   # default 100k iterations
    python cfr/train.py --iterations 50000
"""

import os
import sys
import argparse
import json

# Path setup — same pattern as step01
script_dir = os.path.dirname(os.path.abspath(__file__))
step02_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step02_dir)

from config import CFR_CONFIG
from cfr.cfr_trainer import KuhnTrainer
from cfr.kuhn_poker import PASS, BET, CARD_NAMES
from utils.plotting import create_strategy_charts, create_convergence_chart


def display_results(trainer: KuhnTrainer, avg_game_value: float, iterations: int):
    """Print a clean summary of the computed Nash equilibrium strategy."""
    theoretical = CFR_CONFIG["theoretical_game_value"]

    print("=" * 65)
    print("   KUHN POKER — CFR Nash Equilibrium Results")
    print(f"   Iterations: {iterations:,}")
    print("=" * 65)
    print()
    print(f"  Average game value (player 1): {avg_game_value:+.6f}")
    print(f"  Theoretical optimal value:     {theoretical:+.6f}")
    print(f"  Difference:                    {abs(avg_game_value - theoretical):.6f}")
    print()

    print("-" * 65)
    print(f"  {'Info Set':<12} {'Card':<6} {'History':<10} "
          f"{'P(pass)':<10} {'P(bet)':<10}")
    print("-" * 65)

    table = trainer.get_strategy_table()
    for info_set, row in table.items():
        print(f"  {info_set:<12} {row['card']:<6} {row['history']:<10} "
              f"{row['p_pass']:.4f}     {row['p_bet']:.4f}")

    print("-" * 65)
    print()
    print("  KNOWN NASH EQUILIBRIUM STRUCTURE:")
    print("  ─────────────────────────────────")
    print("  Player 1 (J): pass, then fold to bet  (never bluff)")
    print("  Player 1 (Q): pass, call bet ~1/3 of the time")
    print("  Player 1 (K): bet ~3α of the time (α ∈ [0,1/3])")
    print("  Player 2 (J): bluff ~1/3 after pass, fold to bet")
    print("  Player 2 (Q): pass after pass, call bet ~1/3")
    print("  Player 2 (K): always bet / always call")
    print()


def save_results(trainer: KuhnTrainer, avg_game_value: float, iterations: int):
    """Save strategy table and game value to JSON for later comparison."""
    results = {
        "iterations": iterations,
        "avg_game_value": avg_game_value,
        "theoretical_game_value": CFR_CONFIG["theoretical_game_value"],
        "strategies": trainer.get_strategy_table(),
    }
    results_path = os.path.join(step02_dir, "models", "cfr_results.json")
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to: {results_path}")


def main():
    parser = argparse.ArgumentParser(description="Train CFR on Kuhn Poker")
    parser.add_argument("--iterations", type=int,
                        default=CFR_CONFIG["training_iterations"],
                        help="Number of CFR iterations")
    args = parser.parse_args()

    iterations = args.iterations
    figures_dir = os.path.join(step02_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    print()
    print("  Training Kuhn Poker with CFR...")
    print(f"  Running {iterations:,} iterations...")
    print()

    trainer = KuhnTrainer()
    avg_game_value = trainer.train(iterations)

    display_results(trainer, avg_game_value, iterations)
    save_results(trainer, avg_game_value, iterations)

    # Generate visualizations
    create_convergence_chart(trainer, figures_dir)
    create_strategy_charts(trainer, figures_dir)

    print("  Done! Review figures/ for visual breakdown of the strategy.")
    print()


if __name__ == "__main__":
    main()
