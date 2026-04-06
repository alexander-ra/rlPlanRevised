"""
Information Set Node for Counterfactual Regret Minimization.

Based on the pseudocode from:
  "An Introduction to Counterfactual Regret Minimization"
   by Todd W. Neller and Marc Lanctot (2013)

Each node represents one information set in the game tree —
a group of game states indistinguishable to the acting player.
In Kuhn Poker, a player knows their own card and the action
history, but NOT the opponent's card.

Example info sets: "1" (hold Jack, no actions yet),
                   "2pb" (hold Queen, history = pass then bet)
"""

from cfr.kuhn_poker import NUM_ACTIONS


class InfoSetNode:
    """
    Tracks cumulative regrets and strategy sums at one information set.

    Attributes:
        regret_sum: cumulative counterfactual regret for each action
                    (used to compute strategy via regret matching)
        strategy_sum: cumulative strategy weighted by reach probability
                      (used to compute the final average strategy)
    """

    def __init__(self):
        self.regret_sum = [0.0] * NUM_ACTIONS
        self.strategy_sum = [0.0] * NUM_ACTIONS

    def get_strategy(self, realization_weight: float) -> list:
        """
        Compute current strategy using REGRET MATCHING.

        Play each action in proportion to its positive cumulative regret.
        If all regrets are non-positive, play uniformly.

        Implements Equation 5 from the paper:
          σ^{T+1}(I, a) = R^{T,+}(I,a) / Σ R^{T,+}(I,a')  if sum > 0
                        = 1/|A(I)|                           otherwise

        Args:
            realization_weight: probability that the current player
                played to reach this info set (π_i). Weights the
                strategy sum for computing the average strategy.

        Returns:
            list of action probabilities [p_pass, p_bet]
        """
        strategy = [0.0] * NUM_ACTIONS
        normalizing_sum = 0.0

        for a in range(NUM_ACTIONS):
            strategy[a] = max(self.regret_sum[a], 0.0)
            normalizing_sum += strategy[a]

        for a in range(NUM_ACTIONS):
            if normalizing_sum > 0:
                strategy[a] /= normalizing_sum
            else:
                strategy[a] = 1.0 / NUM_ACTIONS
            self.strategy_sum[a] += realization_weight * strategy[a]

        return strategy

    def get_average_strategy(self) -> list:
        """
        Compute the AVERAGE strategy across all training iterations.

        THIS is what converges to the Nash equilibrium — not the final
        iteration's strategy.

        The average is computed by normalizing the accumulated strategy sums.
        """
        normalizing_sum = sum(self.strategy_sum)

        if normalizing_sum > 0:
            return [s / normalizing_sum for s in self.strategy_sum]
        return [1.0 / NUM_ACTIONS] * NUM_ACTIONS
