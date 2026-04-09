#!/usr/bin/env python3
"""
Step 03 Educational Guide: Running MCCFR Variants on Kuhn Poker

This script demonstrates the complete workflow:
  1. Load Kuhn Poker game
  2. Train External Sampling MCCFR
  3. Train Outcome Sampling MCCFR  
  4. Compare strategies learned
  5. Analyze convergence patterns

Run this to understand the MCCFR algorithm in action!
"""

import pyspiel
from open_spiel.python.algorithms import external_sampling_mccfr
from open_spiel.python.algorithms import outcome_sampling_mccfr
from open_spiel.python.algorithms import exploitability as expl
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*75)
    print(f" {title}")
    print("="*75)


def get_strategy_summary(game, policy, method_name):
    """Extract and summarize learned strategy from policy."""
    print(f"\n{method_name} Strategy Summary:")
    print("-" * 75)
    
    # Create initial state and examine a few info sets
    state = game.new_initial_state()
    
    # We can't easily iterate info sets directly, so show exploitability as proxy
    nash_conv = expl.nash_conv(game, policy)
    
    print(f"  Nash Exploitability: {nash_conv:.6f}")
    print(f"  → Measures how exploitable the strategy is")
    print(f"  → Lower = closer to Nash equilibrium")
    
    # In Kuhn poker:
    # - Perfect Nash has exploitability = 0
    # - Random strategy has exploitability ≈ 0.2
    if nash_conv < 0.02:
        rating = "EXCELLENT (near-equilibrium)"
    elif nash_conv < 0.05:
        rating = "GOOD (reasonable approximation)"
    elif nash_conv < 0.1:
        rating = "FAIR (room for improvement)"
    else:
        rating = "POOR (needs more training)"
    
    print(f"  → Rating: {rating}")


def run_educational_demo():
    """Main demonstration of MCCFR variants."""
    
    print_section("STEP 03: MCCFR SAMPLING VARIANTS - EDUCATIONAL DEMO")
    
    print("\nThis demo shows why MCCFR matters:")
    print("  • Standard CFR: Must traverse entire game tree each iteration")
    print("  • MCCFR: Sample one history per iteration")
    print("  • Benefit: Scales to real-world games (poker, video games)")
    print("  • Tradeoff: Variance in regret estimates")
    print("\nWe explore 2 ways to balance this tradeoff...")
    
    # Load game
    print_section("STEP 1: Loading Kuhn Poker")
    game = pyspiel.load_game("kuhn_poker")
    print(f"✓ Game loaded: {game.get_type().short_name}")
    print(f"  Players: {game.num_players()}")
    print(f"  This is a simplified poker for learning (tractable)")
    
    # External Sampling MCCFR
    print_section("STEP 2: External Sampling MCCFR (5k iterations)")
    print("\nAlgorithm:")
    print("  1. Sample how cards are dealt (random chance)")
    print("  2. Walk game tree using BEST RESPONSE for each player")
    print("  3. Update counterfactual regrets")
    print("  4. Compute avg strategy via regret matching")
    print("\nProperties:")
    print("  ✓ Low variance (regrets don't change randomly)")
    print("  ✗ Slower exploration (uses fixed best response)")
    
    es_solver = external_sampling_mccfr.ExternalSamplingSolver(game)
    
    print("\nTraining...")
    for i in range(5000):
        es_solver.iteration()
        if (i + 1) % 1000 == 0:
            print(f"  Completed {i+1} iterations...", end="")
            policy = es_solver.average_policy()
            nc = expl.nash_conv(game, policy)
            print(f" (exploitability: {nc:.6f})")
    
    es_policy = es_solver.average_policy()
    es_exploit = expl.nash_conv(game, es_policy)
    get_strategy_summary(game, es_policy, "EXTERNAL SAMPLING")
    
    # Outcome Sampling MCCFR
    print_section("STEP 3: Outcome Sampling MCCFR (5k iterations)")
    print("\nAlgorithm:")
    print("  1. Sample how cards are dealt (random chance)")
    print("  2. Sample player actions from CURRENT POLICY")
    print("  3. Walk stochastic tree (importance-weighted)")
    print("  4. Update counterfactual regrets")
    print("  5. Compute avg strategy via regret matching")
    print("\nProperties:")
    print("  ✓ Fast exploration (samples policy diversity)")
    print("  ✗ Higher variance (policy stochasticity adds noise)")
    
    os_solver = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
    
    print("\nTraining...")
    for i in range(5000):
        os_solver.iteration()
        if (i + 1) % 1000 == 0:
            print(f"  Completed {i+1} iterations...", end="")
            policy = os_solver.average_policy()
            nc = expl.nash_conv(game, policy)
            print(f" (exploitability: {nc:.6f})")
    
    os_policy = os_solver.average_policy()
    os_exploit = expl.nash_conv(game, os_policy)
    get_strategy_summary(game, os_policy, "OUTCOME SAMPLING")
    
    # Comparison
    print_section("STEP 4: Comparison & Analysis")
    
    print(f"\nExternal Sampling:")
    print(f"  Exploitability: {es_exploit:.6f}")
    
    print(f"\nOutcome Sampling:")
    print(f"  Exploitability: {os_exploit:.6f}")
    
    print(f"\nDifference: {abs(es_exploit - os_exploit):.6f}")
    
    if es_exploit < os_exploit:
        winner = f"EXTERNAL SAMPLING ({es_exploit:.6f} < {os_exploit:.6f})"
    else:
        winner = f"OUTCOME SAMPLING ({os_exploit:.6f} < {es_exploit:.6f})"
    
    print(f"\nWinner for Kuhn Poker: {winner}")
    
    print("\nKey Insights:")
    print("  1. Both converge to Nash equilibrium (exploitability → 0)")
    print("  2. External sampling converges faster on Kuhn Poker")
    print(f"     (simpler game, deterministic agent walk = stable)")
    print("  3. Outcome sampling better for large strategy spaces")
    print("  4. Choice is problem-dependent")
    
    print_section("STEP 5: When to Use Each Method")
    
    print("\nUSE EXTERNAL SAMPLING WHEN:")
    print("  • Game has few chance nodes (cards already dealt)")
    print("  • Agent strategy space is large (bluffing, mixed strategies)")
    print("  • You want stable, predictable convergence")
    print("  • Memory is critical (lower variance = fewer histories)")
    
    print("\nUSE OUTCOME SAMPLING WHEN:")
    print("  • Game has many chance nodes (randomness dominates)")
    print("  • You want to explore policy space quickly")
    print("  • Fast initial convergence is more important than stability")
    print("  • Game is very large (sampling wins over determinism)")
    
    print_section("Learning Achieved!")
    
    print("\nYou now understand:")
    print("✓ Why MCCFR scales better than standard CFR")
    print("✓ How External Sampling trades variance for stability")
    print("✓ How Outcome Sampling trades stability for exploration")
    print("✓ Why algorithm choice matters for game-solving")
    print("✓ How to measure algorithm quality (exploitability)")


if __name__ == "__main__":
    run_educational_demo()
