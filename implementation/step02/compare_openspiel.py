"""
Cross-verify CFR implementation against OpenSpiel.

Trains both our vanilla CFR and OpenSpiel's CFR on Kuhn Poker
and compares the resulting strategies at every information set.

Usage:
    cd implementation/step02
    python compare_openspiel.py

Requires: pip install open_spiel
(If not installed, the script exits gracefully.)
"""

import sys
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from config import CFR_CONFIG
from cfr.cfr_trainer import KuhnTrainer
from cfr.kuhn_poker import CARD_NAMES

# Known analytical Nash equilibrium for verification
# For P1 with J: bet = 1/3 (bluff), for P1 with Q: bet = 0, for P1 with K: bet = 1
# (one Nash eq. with α=1/3)
ANALYTICAL_NASH = {
    "1":   {"p_pass": 2/3, "p_bet": 1/3},  # J: bluff 1/3
    "2":   {"p_pass": 1.0, "p_bet": 0.0},  # Q: always pass
    "3":   {"p_pass": 0.0, "p_bet": 1.0},  # K: always bet (α=1/3)
    "1p":  {"p_pass": 2/3, "p_bet": 1/3},  # J after pass: bluff 1/3
    "2p":  {"p_pass": 1.0, "p_bet": 0.0},  # Q after pass: pass
    "3p":  {"p_pass": 0.0, "p_bet": 1.0},  # K after pass: always bet
    "1b":  {"p_pass": 1.0, "p_bet": 0.0},  # J facing bet: fold
    "2b":  {"p_pass": 2/3, "p_bet": 1/3},  # Q facing bet: call 1/3
    "3b":  {"p_pass": 0.0, "p_bet": 1.0},  # K facing bet: always call
    "1pb": {"p_pass": 1.0, "p_bet": 0.0},  # J facing bet after pass: fold
    "2pb": {"p_pass": 2/3, "p_bet": 1/3},  # Q facing bet after pass: call 1/3
    "3pb": {"p_pass": 0.0, "p_bet": 1.0},  # K facing bet after pass: always call
}


def get_openspiel_strategies(iterations: int) -> dict:
    """Run OpenSpiel CFR and extract strategies at each info set."""
    try:
        import pyspiel
        from open_spiel.python.algorithms import cfr as os_cfr
    except ImportError:
        print("  ✗ OpenSpiel not installed. Install with: pip install open_spiel")
        return None

    game = pyspiel.load_game("kuhn_poker")
    cfr_solver = os_cfr.CFRSolver(game)

    for _ in range(iterations):
        cfr_solver.evaluate_and_update_policy()

    avg_policy = cfr_solver.average_policy()

    # Map OpenSpiel info state strings to our format
    # OpenSpiel uses "0" for J, "1" for Q, "2" for K and "p"/"b" for actions
    # Our format uses "1" for J, "2" for Q, "3" for K
    os_card_map = {"0": "1", "1": "2", "2": "3"}

    strategies = {}
    for state_str in avg_policy.state_lookup:
        policy = avg_policy.policy_for_key(state_str)
        # Parse OpenSpiel info state: e.g., "0" (card 0, no actions),
        # "0pb" (card 0, pass then bet)
        if len(state_str) >= 1 and state_str[0] in os_card_map:
            our_key = os_card_map[state_str[0]] + state_str[1:]
            # policy is dict {action_id: probability}
            p_pass = policy.get(0, 0.0)
            p_bet = policy.get(1, 0.0)
            strategies[our_key] = {"p_pass": p_pass, "p_bet": p_bet}

    return strategies


def compare_strategies(our: dict, reference: dict, ref_name: str):
    """Print comparison table between our strategies and a reference."""
    print(f"\n  {'Info Set':<10} {'Card':<6} "
          f"{'Ours P(pass)':<14} {'Ours P(bet)':<14} "
          f"{ref_name + ' P(pass)':<16} {ref_name + ' P(bet)':<16} "
          f"{'Δ(pass)':<10}")
    print("  " + "-" * 90)

    max_delta = 0.0
    for info_set in sorted(set(list(our.keys()) + list(reference.keys()))):
        our_row = our.get(info_set, {"p_pass": 0, "p_bet": 0})
        ref_row = reference.get(info_set, {"p_pass": 0, "p_bet": 0})
        card = CARD_NAMES.get(int(info_set[0]), "?")
        delta = abs(our_row["p_pass"] - ref_row["p_pass"])
        max_delta = max(max_delta, delta)
        print(f"  {info_set:<10} {card:<6} "
              f"{our_row['p_pass']:>10.4f}     {our_row['p_bet']:>10.4f}     "
              f"{ref_row['p_pass']:>12.4f}     {ref_row['p_bet']:>12.4f}     "
              f"{delta:>8.4f}")

    print("  " + "-" * 90)
    print(f"  Max delta: {max_delta:.6f}")
    return max_delta


def main():
    iterations = CFR_CONFIG["training_iterations"]
    tolerance = CFR_CONFIG["nash_tolerance"]

    print(f"\n  CFR Cross-Verification ({iterations:,} iterations)")
    print("  " + "=" * 55)

    # Train our CFR
    print(f"\n  Training our CFR...")
    trainer = KuhnTrainer()
    avg_val = trainer.train(iterations)
    our_strategies = {}
    for info_set, row in trainer.get_strategy_table().items():
        our_strategies[info_set] = {"p_pass": row["p_pass"], "p_bet": row["p_bet"]}

    print(f"  Game value: {avg_val:+.6f}")

    # Compare vs analytical Nash
    print("\n  --- Comparison vs Analytical Nash Equilibrium ---")
    delta_nash = compare_strategies(our_strategies, ANALYTICAL_NASH, "Nash")
    # Note: our CFR may find a different point in the Nash set (α varies)
    # so some info sets (like "1", "3") may not exactly match the α=1/3 case
    print(f"\n  Note: Kuhn Poker has a family of Nash equilibria (α ∈ [0,1/3]).")
    print(f"  CFR may converge to a different α than the reference (α=1/3).")
    print(f"  Fixed-strategy info sets (1b, 3b, 1pb, 3pb) should match exactly.")

    # Compare vs OpenSpiel
    print("\n  --- Comparison vs OpenSpiel CFR ---")
    os_strategies = get_openspiel_strategies(iterations)
    if os_strategies:
        delta_os = compare_strategies(our_strategies, os_strategies, "OpenSpiel")
        if delta_os < 0.05:
            print(f"  ✓ Strategies match OpenSpiel within tolerance")
        else:
            print(f"  ✗ Large discrepancy — investigate")
    else:
        print("  Skipped (OpenSpiel not available)")

    # Save comparison results
    results = {
        "iterations": iterations,
        "our_game_value": avg_val,
        "our_strategies": our_strategies,
        "analytical_nash": {k: v for k, v in ANALYTICAL_NASH.items()},
    }
    results_path = os.path.join(script_dir, "models", "comparison_results.json")
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to: {results_path}")
    print()


if __name__ == "__main__":
    main()
