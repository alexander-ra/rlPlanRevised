"""
Cross-verify CFR implementation against OpenSpiel for Leduc Poker.

Usage:
    cd implementation/step03
    python compare_openspiel.py
"""

import sys
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from config import CFR_CONFIG
from cfr.cfr_trainer import LeducTrainer


def get_openspiel_exploitability(iterations: int):
    """Run OpenSpiel CFR on Leduc and return exploitability."""
    try:
        import pyspiel
        from open_spiel.python.algorithms import cfr as os_cfr
        from open_spiel.python.algorithms import exploitability as os_exploit
    except ImportError:
        print("  ✗ OpenSpiel not installed. Install with: pip install open_spiel")
        return None, None

    game = pyspiel.load_game("leduc_poker")
    cfr_solver = os_cfr.CFRSolver(game)

    for _ in range(iterations):
        cfr_solver.evaluate_and_update_policy()

    avg_policy = cfr_solver.average_policy()
    exploit = os_exploit.exploitability(game, avg_policy)
    return exploit, avg_policy


def main():
    iterations = CFR_CONFIG["training_iterations"]

    print(f"\n  Leduc Poker — CFR Cross-Verification ({iterations:,} iterations)")
    print("  " + "=" * 55)

    # Train our CFR
    print(f"\n  Training our vanilla CFR...")
    trainer = LeducTrainer()
    avg_val = trainer.train(iterations)
    print(f"  Game value: {avg_val:+.6f}")
    print(f"  Info sets:  {len(trainer.node_map)}")

    # Our exploitability
    from evaluate.exploitability import compute_exploitability
    our_exploit = compute_exploitability(trainer.node_map)
    print(f"  Our exploitability: {our_exploit:.6f}")

    # OpenSpiel comparison
    print(f"\n  Running OpenSpiel CFR...")
    os_exploit, _ = get_openspiel_exploitability(iterations)
    if os_exploit is not None:
        print(f"  OpenSpiel exploitability: {os_exploit:.6f}")
        ratio = our_exploit / os_exploit if os_exploit > 0 else float('inf')
        print(f"  Ratio (ours/theirs): {ratio:.2f}")
        if 0.1 < ratio < 10:
            print(f"  ✓ Same order of magnitude — implementations consistent")
        else:
            print(f"  ✗ Large discrepancy — investigate")
    else:
        print("  Skipped (OpenSpiel not available)")

    # Save results
    results = {
        "iterations": iterations,
        "our_game_value": avg_val,
        "our_exploitability": our_exploit,
        "our_num_info_sets": len(trainer.node_map),
    }
    if os_exploit is not None:
        results["openspiel_exploitability"] = os_exploit

    results_path = os.path.join(script_dir, "models", "comparison_results.json")
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to: {results_path}")
    print()


if __name__ == "__main__":
    main()
