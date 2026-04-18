"""
Training entrypoint for Leduc Poker CFR variants.

Usage:
    cd implementation/step03
    python cfr/train.py                              # vanilla CFR (default)
    python cfr/train.py --algo cfrplus               # CFR+
    python cfr/train.py --algo external               # MCCFR External Sampling
    python cfr/train.py --algo outcome                # MCCFR Outcome Sampling
    python cfr/train.py --algo external --iterations 10000
"""

import os
import sys
import argparse
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
step03_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step03_dir)

from config import CFR_CONFIG
from cfr.cfr_trainer import LeducTrainer
from cfr.cfrplus_trainer import LeducCFRPlusTrainer
from cfr.mccfr_external_trainer import LeducExternalSamplingTrainer
from cfr.mccfr_outcome_trainer import LeducOutcomeSamplingTrainer
from utils.plotting import create_strategy_charts, create_convergence_chart

ALGO_MAP = {
    "vanilla": ("Vanilla CFR", LeducTrainer),
    "cfrplus": ("CFR+", LeducCFRPlusTrainer),
    "external": ("MCCFR External Sampling", LeducExternalSamplingTrainer),
    "outcome": ("MCCFR Outcome Sampling", LeducOutcomeSamplingTrainer),
}


def display_results(trainer, algo_name: str, avg_game_value: float, iterations: int):
    """Print summary of computed strategy."""
    print("=" * 65)
    print(f"   LEDUC POKER — {algo_name} Results")
    print(f"   Iterations: {iterations:,}")
    print("=" * 65)
    print()
    print(f"  Average game value (player 0): {avg_game_value:+.6f}")
    print(f"  Total info sets discovered:    {len(trainer.node_map)}")
    print()

    table = trainer.get_strategy_table()
    # Show a sample of info sets (Leduc has ~936, too many to print all)
    print("-" * 65)
    print(f"  {'Info Set':<20} {'Strategy'}")
    print("-" * 65)
    shown = 0
    for info_set, strat in sorted(table.items()):
        if shown >= 30:
            print(f"  ... and {len(table) - 30} more info sets")
            break
        strat_str = "  ".join(f"{k}={v:.3f}" for k, v in strat.items())
        print(f"  {info_set:<20} {strat_str}")
        shown += 1
    print("-" * 65)
    print()


def save_results(trainer, algo_key: str, avg_game_value: float, iterations: int):
    """Save results to JSON."""
    results = {
        "algorithm": algo_key,
        "iterations": iterations,
        "avg_game_value": avg_game_value,
        "num_info_sets": len(trainer.node_map),
        "strategies": trainer.get_strategy_table(),
    }
    results_path = os.path.join(step03_dir, "models", f"cfr_{algo_key}_results.json")
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to: {results_path}")


def main():
    parser = argparse.ArgumentParser(description="Train CFR variants on Leduc Poker")
    parser.add_argument("--algo", type=str, default="vanilla",
                        choices=list(ALGO_MAP.keys()),
                        help="CFR algorithm variant")
    parser.add_argument("--iterations", type=int,
                        default=CFR_CONFIG["training_iterations"],
                        help="Number of iterations")
    args = parser.parse_args()

    algo_name, TrainerClass = ALGO_MAP[args.algo]
    iterations = args.iterations
    figures_dir = os.path.join(step03_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    is_sampling = args.algo in ("external", "outcome")

    print()
    print(f"  Training Leduc Poker with {algo_name}...")
    print(f"  Running {iterations:,} iterations...")
    if not is_sampling:
        print(f"  (120 deals per iteration — full traversal)")
    else:
        print(f"  (1 sampled deal per iteration)")
    print()

    trainer = TrainerClass()
    avg_game_value = trainer.train(iterations)

    display_results(trainer, algo_name, avg_game_value, iterations)
    save_results(trainer, args.algo, avg_game_value, iterations)

    create_convergence_chart(trainer, figures_dir)
    create_strategy_charts(trainer, figures_dir)

    print("  Done! Review figures/ for visual breakdown.")
    print()


if __name__ == "__main__":
    main()
