"""
Information Set Node for Counterfactual Regret Minimization.

Game-agnostic: works with any number of actions (not hardcoded to 2).
Supports vanilla CFR, CFR+, and MCCFR variants.
"""


class InfoSetNode:
    """
    Tracks cumulative regrets and strategy sums at one information set.

    Attributes:
        num_actions: number of legal actions at this info set
        regret_sum: cumulative counterfactual regret for each action
        strategy_sum: cumulative strategy weighted by reach probability
    """

    def __init__(self, num_actions: int):
        self.num_actions = num_actions
        self.regret_sum = [0.0] * num_actions
        self.strategy_sum = [0.0] * num_actions

    def get_strategy(self, realization_weight: float) -> list:
        """
        Compute current strategy via regret matching.

        Args:
            realization_weight: reach probability of the current player
        Returns:
            list of action probabilities
        """
        strategy = [0.0] * self.num_actions
        normalizing_sum = 0.0

        for a in range(self.num_actions):
            strategy[a] = max(self.regret_sum[a], 0.0)
            normalizing_sum += strategy[a]

        for a in range(self.num_actions):
            if normalizing_sum > 0:
                strategy[a] /= normalizing_sum
            else:
                strategy[a] = 1.0 / self.num_actions
            self.strategy_sum[a] += realization_weight * strategy[a]

        return strategy

    def get_current_strategy(self) -> list:
        """
        Compute current strategy via regret matching WITHOUT updating
        strategy_sum. Used by MCCFR where strategy accumulation is
        handled separately.
        """
        strategy = [0.0] * self.num_actions
        normalizing_sum = 0.0

        for a in range(self.num_actions):
            strategy[a] = max(self.regret_sum[a], 0.0)
            normalizing_sum += strategy[a]

        for a in range(self.num_actions):
            if normalizing_sum > 0:
                strategy[a] /= normalizing_sum
            else:
                strategy[a] = 1.0 / self.num_actions

        return strategy

    def get_average_strategy(self) -> list:
        """
        Compute the average strategy across all training iterations.
        This converges to the Nash equilibrium.
        """
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum > 0:
            return [s / normalizing_sum for s in self.strategy_sum]
        return [1.0 / self.num_actions] * self.num_actions
