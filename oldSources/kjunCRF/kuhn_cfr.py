"""
=============================================================================
Counterfactual Regret Minimization (CFR) for Kuhn Poker
=============================================================================

Based on the pseudocode from:
  "An Introduction to Counterfactual Regret Minimization"
   by Todd W. Neller and Marc Lanctot (2013)

KUHN POKER RULES:
  - 3 cards: {1, 2, 3} (think of them as Jack, Queen, King)
  - 2 players each ante 1 chip (forced blind bet before the deal)
  - Each player is dealt 1 card (private information)
  - Players alternate, starting with Player 1
  - On a turn, a player may PASS or BET (bet = add 1 chip to pot)
  - Terminal conditions:
      pass-pass  → higher card wins 1 chip
      pass-bet-pass → bettor (player 2) wins 1 chip
      pass-bet-bet  → higher card wins 2 chips
      bet-pass   → bettor (player 1) wins 1 chip
      bet-bet    → higher card wins 2 chips

KEY CONCEPTS:
  - An "information set" is what a player knows: their card + the action history
    e.g. "2pb" = player holds card 2, history is pass-then-bet
  - CFR finds a Nash equilibrium by tracking "counterfactual regret" at each
    information set and using "regret matching" to update strategies
  - The AVERAGE strategy (not the final one!) converges to Nash equilibrium

ALGORITHM OVERVIEW (Algorithm 1 from the paper):
  1. Initialize all cumulative regrets and strategy sums to 0
  2. For many iterations:
     a. Shuffle/deal cards (chance sampling)
     b. Recursively walk the game tree
     c. At each info set, compute strategy via regret matching
     d. Compute counterfactual values for each action
     e. Update cumulative regrets weighted by opponent reach probability
  3. The average strategy profile converges to Nash equilibrium

The known optimal game value for player 1 in Kuhn Poker is: -1/18 ≈ -0.0556
"""

import random
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for saving figures
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# =============================================================================
# CONSTANTS
# =============================================================================

# The two possible actions in Kuhn Poker
PASS = 0
BET = 1
NUM_ACTIONS = 2

# Card names for display purposes
CARD_NAMES = {1: 'J', 2: 'Q', 3: 'K'}


# =============================================================================
# INFORMATION SET NODE
# =============================================================================

class InfoSetNode:
    """
    Represents one information set in the game tree.

    An information set groups together all game states that are
    indistinguishable to the acting player. In Kuhn Poker, a player
    knows their own card and the history of actions, but NOT the
    opponent's card.

    Example info sets: "1" (hold Jack, no actions yet),
                       "2pb" (hold Queen, history = pass then bet)

    Each node tracks:
      - regret_sum: cumulative counterfactual regret for each action
        (used to compute the current strategy via regret matching)
      - strategy_sum: cumulative strategy weighted by reach probability
        (used to compute the final average strategy)
    """

    def __init__(self):
        # Cumulative counterfactual regret for each action [PASS, BET]
        # Positive regret for an action means "I wish I had taken this action more"
        self.regret_sum = [0.0] * NUM_ACTIONS

        # Running sum of strategies weighted by player's reach probability
        # This is used to compute the AVERAGE strategy, which is what converges
        self.strategy_sum = [0.0] * NUM_ACTIONS

    def get_strategy(self, realization_weight: float) -> list:
        """
        Compute the current strategy using REGRET MATCHING.

        Regret matching: play each action in proportion to its positive
        cumulative regret. If all regrets are non-positive, play uniformly.

        This implements Equation 5 from the paper:
          σ^{T+1}(I, a) = R^{T,+}(I,a) / Σ R^{T,+}(I,a')  if sum > 0
                        = 1/|A(I)|                           otherwise

        Args:
            realization_weight: the probability that the CURRENT player
                played to reach this info set (π_i). Used to weight the
                strategy sum for computing the average strategy later.

        Returns:
            list of action probabilities [p_pass, p_bet]
        """
        strategy = [0.0] * NUM_ACTIONS
        normalizing_sum = 0.0

        # Step 1: Take only POSITIVE regrets (negative regret = no desire to play that action)
        for a in range(NUM_ACTIONS):
            strategy[a] = max(self.regret_sum[a], 0.0)
            normalizing_sum += strategy[a]

        # Step 2: Normalize to get probabilities
        for a in range(NUM_ACTIONS):
            if normalizing_sum > 0:
                # Proportional to positive regrets
                strategy[a] /= normalizing_sum
            else:
                # All regrets non-positive → play uniformly (no preference)
                strategy[a] = 1.0 / NUM_ACTIONS

            # Accumulate weighted strategy for computing the average later
            # Weight = reach probability of the current player to this info set
            self.strategy_sum[a] += realization_weight * strategy[a]

        return strategy

    def get_average_strategy(self) -> list:
        """
        Compute the AVERAGE strategy across all training iterations.

        THIS is what converges to the Nash equilibrium — not the final
        iteration's strategy! This is the most commonly misunderstood
        aspect of CFR (as noted in the paper).

        The average is computed by normalizing the accumulated strategy sums.
        """
        avg_strategy = [0.0] * NUM_ACTIONS
        normalizing_sum = sum(self.strategy_sum)

        if normalizing_sum > 0:
            avg_strategy = [s / normalizing_sum for s in self.strategy_sum]
        else:
            # Fallback: uniform strategy
            avg_strategy = [1.0 / NUM_ACTIONS] * NUM_ACTIONS

        return avg_strategy


# =============================================================================
# KUHN POKER CFR TRAINER
# =============================================================================

class KuhnTrainer:
    """
    Trains an approximate Nash equilibrium for Kuhn Poker using
    Counterfactual Regret Minimization (CFR) with chance sampling.

    Chance sampling means we sample the random card deal at the start
    of each iteration rather than summing over all possible deals.
    This is simpler and converges to the same result.
    """

    def __init__(self):
        # Maps info set string → InfoSetNode
        # e.g. "1p" → node for player holding card 1 after a pass
        self.node_map: dict[str, InfoSetNode] = {}

        # Track exploitability and game value over training for visualization
        self.game_value_history = []
        self.iteration_history = []

    def train(self, iterations: int) -> float:
        """
        Run CFR training for the specified number of iterations.

        Each iteration:
          1. Shuffle cards (this IS the chance sampling — replaces explicit
             chance nodes from Algorithm 1, lines 8-10)
          2. Call cfr() recursively from the root of the game tree
          3. Accumulate the returned utility

        Args:
            iterations: number of training iterations

        Returns:
            average game value for player 1
        """
        cards = [1, 2, 3]  # The three Kuhn Poker cards
        cumulative_util = 0.0

        # How often to record metrics for plotting
        checkpoint_interval = max(1, iterations // 200)

        for i in range(iterations):
            # ----------------------------------------------------------
            # CHANCE SAMPLING: shuffle cards randomly
            # Card at index 0 → Player 1, Card at index 1 → Player 2
            # This replaces explicit chance node handling in the recursion
            # (Fisher-Yates / Durstenfeld shuffle, as described in the paper)
            # ----------------------------------------------------------
            random.shuffle(cards)

            # ----------------------------------------------------------
            # Start recursive CFR from root:
            #   - cards: the dealt cards
            #   - history: "" (empty — no actions taken yet)
            #   - p0=1.0: player 0's reach probability (starts at 1)
            #   - p1=1.0: player 1's reach probability (starts at 1)
            # ----------------------------------------------------------
            cumulative_util += self.cfr(cards, "", 1.0, 1.0)

            # Record metrics periodically for plotting
            if (i + 1) % checkpoint_interval == 0 or i == iterations - 1:
                self.game_value_history.append(cumulative_util / (i + 1))
                self.iteration_history.append(i + 1)

        avg_game_value = cumulative_util / iterations
        return avg_game_value

    def cfr(self, cards: list, history: str, p0: float, p1: float) -> float:
        """
        The core recursive CFR function. Walks the game tree, computes
        counterfactual values, and updates regrets.

        This implements the CFR function from Algorithm 1 in the paper.

        Args:
            cards: [player1_card, player2_card, unused_card]
            history: string of actions taken so far ("p"=pass, "b"=bet)
            p0: probability that player 0 played to reach this state
                (product of all player 0's action probabilities on the path)
            p1: probability that player 1 played to reach this state

        Returns:
            expected utility for the CURRENT player at this node
        """
        num_plays = len(history)
        # Player alternates: player 0 acts on even turns, player 1 on odd
        player = num_plays % 2
        opponent = 1 - player

        # =============================================================
        # TERMINAL STATE CHECK (Algorithm 1, line 6-7)
        # If the game is over, return the utility for the current player
        # =============================================================
        if num_plays > 1:
            # Check if the last action was a pass (potential terminal)
            terminal_pass = (history[-1] == 'p')
            # Check if the last two actions were both bets
            double_bet = (history[-2:] == "bb")
            # Compare cards to determine winner
            is_player_card_higher = cards[player] > cards[opponent]

            if terminal_pass:
                if history == "pp":
                    # Both players passed → showdown, higher card wins 1 chip
                    return 1 if is_player_card_higher else -1
                else:
                    # One player bet, the other passed → bettor wins 1 chip
                    # The current player is the one who just passed (folded)
                    return 1  # previous player bet and current player folded
            elif double_bet:
                # Both players bet → showdown, higher card wins 2 chips
                return 2 if is_player_card_higher else -2

        # =============================================================
        # NON-TERMINAL: Build information set and get/create node
        # (Algorithm 1, line 12)
        # =============================================================

        # Information set = player's card + action history
        # e.g. "2pb" means "I hold card 2, and the history is pass-then-bet"
        info_set = str(cards[player]) + history

        # Retrieve existing node or create a new one
        if info_set not in self.node_map:
            self.node_map[info_set] = InfoSetNode()
        node = self.node_map[info_set]

        # =============================================================
        # STRATEGY COMPUTATION via regret matching
        # The realization weight is the current player's reach probability
        # =============================================================
        strategy = node.get_strategy(p0 if player == 0 else p1)

        # =============================================================
        # RECURSIVE CFR CALLS for each action
        # (Algorithm 1, lines 15-22)
        # =============================================================
        util = [0.0] * NUM_ACTIONS  # utility of each action for current player
        node_util = 0.0  # expected utility of this node

        for a in range(NUM_ACTIONS):
            # Append action to history ("p" for pass, "b" for bet)
            next_history = history + ("p" if a == PASS else "b")

            # Recurse with updated reach probabilities
            # KEY INSIGHT: We only multiply the CURRENT player's reach probability
            # by the action probability (strategy[a]). The opponent's reach
            # probability stays the same because the opponent didn't act here.
            #
            # Also note the NEGATION: cfr returns utility for the player who
            # acts at the child node, which is our opponent. Since Kuhn Poker
            # is zero-sum, our utility = negative of opponent's utility.
            if player == 0:
                util[a] = -self.cfr(cards, next_history,
                                    p0 * strategy[a], p1)
            else:
                util[a] = -self.cfr(cards, next_history,
                                    p0, p1 * strategy[a])

            # Weighted utility contribution of this action
            node_util += strategy[a] * util[a]

        # =============================================================
        # REGRET UPDATE (Algorithm 1, lines 23-28)
        # Only update regrets for the CURRENT player's information sets
        # =============================================================
        for a in range(NUM_ACTIONS):
            # Regret = "how much better would action a have been vs what I did?"
            regret = util[a] - node_util

            # COUNTERFACTUAL regret: weight by the OPPONENT's reach probability
            # This is the key "counterfactual" part — we ask:
            # "If I had intentionally played to reach this info set,
            #  and the opponent played according to their strategy,
            #  how much do I regret not taking action a?"
            #
            # π_{-i} (opponent reach probability) weights this because:
            # the regret matters more when the opponent is more likely to
            # have played to this state
            node.regret_sum[a] += (p1 if player == 0 else p0) * regret

        return node_util


# =============================================================================
# DISPLAY AND VISUALIZATION
# =============================================================================

def display_results(trainer: KuhnTrainer, avg_game_value: float, iterations: int):
    """Print a clean summary of the computed Nash equilibrium strategy."""

    print("=" * 65)
    print("   KUHN POKER — CFR Nash Equilibrium Results")
    print(f"   Iterations: {iterations:,}")
    print("=" * 65)
    print()

    # Known theoretical value
    theoretical_value = -1/18
    print(f"  Average game value (player 1): {avg_game_value:+.6f}")
    print(f"  Theoretical optimal value:     {theoretical_value:+.6f}")
    print(f"  Difference:                    {abs(avg_game_value - theoretical_value):.6f}")
    print()

    # Collect and sort information sets
    print("-" * 65)
    print(f"  {'Info Set':<12} {'Card':<6} {'History':<10} "
          f"{'P(pass)':<10} {'P(bet)':<10}")
    print("-" * 65)

    for info_set in sorted(trainer.node_map.keys()):
        node = trainer.node_map[info_set]
        avg = node.get_average_strategy()
        card = CARD_NAMES.get(int(info_set[0]), info_set[0])
        hist = info_set[1:] if len(info_set) > 1 else "(root)"
        print(f"  {info_set:<12} {card:<6} {hist:<10} "
              f"{avg[PASS]:.4f}     {avg[BET]:.4f}")

    print("-" * 65)
    print()

    # =========================================================================
    # Known Nash equilibrium structure for Kuhn Poker:
    #   Player 1 (Jack):  always pass first; if facing bet, always fold
    #   Player 1 (Queen): pass first; if facing bet, call with prob 1/3
    #   Player 1 (King):  bet with prob 3α; if check, bet 3*alpha
    #                     (α is a free parameter in [0, 1/3])
    #   Player 2 (Jack):  if p1 passes, bet with prob 1/3; if p1 bets, fold
    #   Player 2 (Queen): if p1 passes, pass; if p1 bets, call with prob 1/3
    #   Player 2 (King):  always bet/call
    # =========================================================================
    print("  KNOWN NASH EQUILIBRIUM STRUCTURE:")
    print("  ─────────────────────────────────")
    print("  Player 1 (J): pass, then fold to bet  (never bluff)")
    print("  Player 1 (Q): pass, call bet ~1/3 of the time")
    print("  Player 1 (K): bet ~3α of the time (α ∈ [0,1/3])")
    print("  Player 2 (J): bluff ~1/3 after pass, fold to bet")
    print("  Player 2 (Q): pass after pass, call bet ~1/3")
    print("  Player 2 (K): always bet / always call")
    print()


def create_visualizations(trainer: KuhnTrainer, avg_game_value: float,
                          iterations: int):
    """Create charts showing training convergence and final strategy."""

    fig = plt.figure(figsize=(16, 14))
    fig.suptitle("Kuhn Poker — CFR Analysis", fontsize=16, fontweight='bold',
                 y=0.98)

    gs = gridspec.GridSpec(3, 2, hspace=0.4, wspace=0.35,
                           top=0.92, bottom=0.06, left=0.08, right=0.95)

    # =====================================================================
    # CHART 1: Game Value Convergence
    # Shows how the average game value converges to the theoretical -1/18
    # =====================================================================
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(trainer.iteration_history, trainer.game_value_history,
             color='#2196F3', linewidth=1.5, label='Computed game value')
    ax1.axhline(y=-1/18, color='#F44336', linestyle='--', linewidth=1.5,
                label=f'Theoretical value (-1/18 ≈ {-1/18:.4f})')
    ax1.set_xlabel('Training Iterations')
    ax1.set_ylabel('Average Game Value (Player 1)')
    ax1.set_title('Convergence of Game Value to Nash Equilibrium')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # =====================================================================
    # CHART 2: Player 1's Strategy (opening action)
    # Player 1 acts first — what does P1 do with each card?
    # =====================================================================
    ax2 = fig.add_subplot(gs[1, 0])

    p1_cards = ['1', '2', '3']  # Player 1's opening nodes
    p1_labels = ['J (card 1)', 'Q (card 2)', 'K (card 3)']
    p1_pass_probs = []
    p1_bet_probs = []

    for card in p1_cards:
        if card in trainer.node_map:
            avg = trainer.node_map[card].get_average_strategy()
            p1_pass_probs.append(avg[PASS])
            p1_bet_probs.append(avg[BET])
        else:
            p1_pass_probs.append(0)
            p1_bet_probs.append(0)

    x = range(len(p1_labels))
    bars1 = ax2.bar([i - 0.18 for i in x], p1_pass_probs, 0.35,
                    label='Pass', color='#66BB6A', edgecolor='white')
    bars2 = ax2.bar([i + 0.18 for i in x], p1_bet_probs, 0.35,
                    label='Bet', color='#EF5350', edgecolor='white')

    # Add value labels on bars
    for bar in bars1:
        h = bar.get_height()
        if h > 0.02:
            ax2.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        h = bar.get_height()
        if h > 0.02:
            ax2.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=9)

    ax2.set_xlabel('Player 1 Card')
    ax2.set_ylabel('Probability')
    ax2.set_title('Player 1: Opening Action')
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(p1_labels)
    ax2.set_ylim(0, 1.15)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    # =====================================================================
    # CHART 3: Player 2's Strategy after Player 1 passes
    # These are info sets like "1p", "2p", "3p"
    # =====================================================================
    ax3 = fig.add_subplot(gs[1, 1])

    p2_after_pass_cards = ['1p', '2p', '3p']
    p2_ap_labels = ['J (card 1)', 'Q (card 2)', 'K (card 3)']
    p2_ap_pass = []
    p2_ap_bet = []

    for info in p2_after_pass_cards:
        if info in trainer.node_map:
            avg = trainer.node_map[info].get_average_strategy()
            p2_ap_pass.append(avg[PASS])
            p2_ap_bet.append(avg[BET])
        else:
            p2_ap_pass.append(0)
            p2_ap_bet.append(0)

    x = range(len(p2_ap_labels))
    bars1 = ax3.bar([i - 0.18 for i in x], p2_ap_pass, 0.35,
                    label='Pass', color='#66BB6A', edgecolor='white')
    bars2 = ax3.bar([i + 0.18 for i in x], p2_ap_bet, 0.35,
                    label='Bet', color='#EF5350', edgecolor='white')

    for bar in bars1:
        h = bar.get_height()
        if h > 0.02:
            ax3.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        h = bar.get_height()
        if h > 0.02:
            ax3.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=9)

    ax3.set_xlabel('Player 2 Card')
    ax3.set_ylabel('Probability')
    ax3.set_title('Player 2: Response to Pass')
    ax3.set_xticks(list(x))
    ax3.set_xticklabels(p2_ap_labels)
    ax3.set_ylim(0, 1.15)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')

    # =====================================================================
    # CHART 4: Player 2's Strategy after Player 1 bets
    # These are info sets like "1b", "2b", "3b"
    # =====================================================================
    ax4 = fig.add_subplot(gs[2, 0])

    p2_after_bet_cards = ['1b', '2b', '3b']
    p2_ab_labels = ['J (card 1)', 'Q (card 2)', 'K (card 3)']
    p2_ab_pass = []
    p2_ab_bet = []

    for info in p2_after_bet_cards:
        if info in trainer.node_map:
            avg = trainer.node_map[info].get_average_strategy()
            p2_ab_pass.append(avg[PASS])  # pass = fold to bet
            p2_ab_bet.append(avg[BET])    # bet = call the bet
        else:
            p2_ab_pass.append(0)
            p2_ab_bet.append(0)

    x = range(len(p2_ab_labels))
    bars1 = ax4.bar([i - 0.18 for i in x], p2_ab_pass, 0.35,
                    label='Fold (pass)', color='#66BB6A', edgecolor='white')
    bars2 = ax4.bar([i + 0.18 for i in x], p2_ab_bet, 0.35,
                    label='Call (bet)', color='#EF5350', edgecolor='white')

    for bar in bars1:
        h = bar.get_height()
        if h > 0.02:
            ax4.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        h = bar.get_height()
        if h > 0.02:
            ax4.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=9)

    ax4.set_xlabel('Player 2 Card')
    ax4.set_ylabel('Probability')
    ax4.set_title('Player 2: Response to Bet (fold vs call)')
    ax4.set_xticks(list(x))
    ax4.set_xticklabels(p2_ab_labels)
    ax4.set_ylim(0, 1.15)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')

    # =====================================================================
    # CHART 5: Player 1's Strategy after pass-bet (facing a bet after passing)
    # These are info sets like "1pb", "2pb", "3pb"
    # =====================================================================
    ax5 = fig.add_subplot(gs[2, 1])

    p1_pb_cards = ['1pb', '2pb', '3pb']
    p1_pb_labels = ['J (card 1)', 'Q (card 2)', 'K (card 3)']
    p1_pb_pass = []
    p1_pb_bet = []

    for info in p1_pb_cards:
        if info in trainer.node_map:
            avg = trainer.node_map[info].get_average_strategy()
            p1_pb_pass.append(avg[PASS])  # pass = fold
            p1_pb_bet.append(avg[BET])    # bet = call
        else:
            p1_pb_pass.append(0)
            p1_pb_bet.append(0)

    x = range(len(p1_pb_labels))
    bars1 = ax5.bar([i - 0.18 for i in x], p1_pb_pass, 0.35,
                    label='Fold (pass)', color='#66BB6A', edgecolor='white')
    bars2 = ax5.bar([i + 0.18 for i in x], p1_pb_bet, 0.35,
                    label='Call (bet)', color='#EF5350', edgecolor='white')

    for bar in bars1:
        h = bar.get_height()
        if h > 0.02:
            ax5.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        h = bar.get_height()
        if h > 0.02:
            ax5.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                     f'{h:.2f}', ha='center', va='bottom', fontsize=9)

    ax5.set_xlabel('Player 1 Card')
    ax5.set_ylabel('Probability')
    ax5.set_title('Player 1: Facing Bet After Passing (fold vs call)')
    ax5.set_xticks(list(x))
    ax5.set_xticklabels(p1_pb_labels)
    ax5.set_ylim(0, 1.15)
    ax5.legend()
    ax5.grid(True, alpha=0.3, axis='y')

    # Save figure
    output_path = 'kuhn_cfr_results.png'
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {output_path}")
    print()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    ITERATIONS = 100_000  # More iterations → closer to true Nash equilibrium
                          # The paper uses 1,000,000; 100k is fast & close enough

    print()
    print("  Training Kuhn Poker with CFR...")
    print(f"  Running {ITERATIONS:,} iterations...")
    print()

    # ------------------------------------------------------------------
    # Train
    # ------------------------------------------------------------------
    trainer = KuhnTrainer()
    avg_game_value = trainer.train(ITERATIONS)

    # ------------------------------------------------------------------
    # Display results in terminal
    # ------------------------------------------------------------------
    display_results(trainer, avg_game_value, ITERATIONS)

    # ------------------------------------------------------------------
    # Create and save visualizations
    # ------------------------------------------------------------------
    create_visualizations(trainer, avg_game_value, ITERATIONS)

    print("  Done! Review the chart for a visual breakdown of the strategy.")
    print()
