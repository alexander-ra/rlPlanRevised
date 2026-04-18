"""
Monte Carlo CFR with Outcome Sampling for Leduc Poker.

Outcome Sampling (Lanctot et al., 2009):
  - Samples a SINGLE trajectory through the game tree per iteration.
  - The update player's actions are sampled with epsilon-on-policy.
  - The opponent's actions are sampled according to their current strategy.
  - Uses importance sampling weights to correct for the sampling bias.

This is the cheapest per-iteration MCCFR variant (O(game length) per
iteration) but has the highest variance. Needs many more iterations
to converge compared to external sampling.

Epsilon-on-policy exploration (ε ∈ [0,1]):
  - With probability ε, sample uniformly; otherwise follow strategy.
  - Applied ONLY at the update player's nodes.
  - Ensures all info sets are explored even if strategy assigns zero
    probability to some actions.

Implementation follows OpenSpiel's outcome_sampling_mccfr.py:
  - Terminal returns raw utility (not importance-sampled).
  - Value estimate at each node incorporates tail importance weights
    (ratio of strategy to sampling probabilities on the tail).
  - Regret update uses cf_action_value - cf_value formulation.

Reference:
  Lanctot, M. et al. (2009). "Monte Carlo Sampling for Regret
  Minimization in Extensive Games"
"""

import random

from cfr.info_set_node import InfoSetNode
from cfr.leduc_poker import (
    FOLD, CHECK_CALL, RAISE, NUM_ACTIONS,
    NUM_CARDS, LeducState,
)

# Default exploration parameter — same as OpenSpiel default
DEFAULT_EPSILON = 0.6


class LeducOutcomeSamplingTrainer:
    """
    MCCFR with Outcome Sampling for Leduc Poker.

    Per iteration:
      1. Sample a random deal
      2. Walk a single sampled trajectory through the game tree
      3. Use importance sampling to correct regret and strategy updates
      4. Alternate update player each iteration
    """

    def __init__(self, epsilon: float = DEFAULT_EPSILON):
        self.node_map: dict[str, tuple[InfoSetNode, list]] = {}
        self.game_value_history = []
        self.iteration_history = []
        self.epsilon = epsilon  # exploration parameter

    def train(self, iterations: int) -> float:
        """
        Run Outcome Sampling MCCFR.

        Alternates the update player each iteration.
        Returns average game value estimate for player 0.
        """
        cumulative_util = 0.0
        checkpoint_interval = max(1, iterations // 100)

        for i in range(iterations):
            cards = random.sample(range(NUM_CARDS), 3)
            p0_card, p1_card, community = cards[0], cards[1], cards[2]
            state = LeducState((p0_card, p1_card), community)

            update_player = i % 2
            util = self.outcome_cfr(state, update_player,
                                    1.0, 1.0, 1.0)

            if update_player == 0:
                cumulative_util += util

            if (i + 1) % checkpoint_interval == 0 or i == iterations - 1:
                p0_iters = (i + 2) // 2
                avg = cumulative_util / p0_iters if p0_iters > 0 else 0
                self.game_value_history.append(avg)
                self.iteration_history.append(i + 1)

        p0_iters = (iterations + 1) // 2
        return cumulative_util / p0_iters if p0_iters > 0 else 0

    def outcome_cfr(self, state: LeducState, update_player: int,
                    my_reach: float, opp_reach: float,
                    sample_reach: float) -> float:
        """
        Outcome Sampling CFR traversal (OpenSpiel-style).

        Returns a value_estimate for update_player. The estimate
        already incorporates tail importance weights (ratio of
        strategy probabilities to sampling probabilities on the
        sub-trajectory below this node).

        Args:
            state: current game state
            update_player: the player whose regrets we're updating
            my_reach: reach probability of the update player
            opp_reach: reach probability of the opponent
            sample_reach: reach probability of the sampling policy
        """
        player = state.current_player()

        if state.is_terminal():
            return state.get_utility(update_player)

        info_set = state.get_info_set(player)
        legal_actions = state.legal_actions()
        num_legal = len(legal_actions)

        if info_set not in self.node_map:
            node = InfoSetNode(num_legal)
            self.node_map[info_set] = (node, legal_actions)
        else:
            node, _ = self.node_map[info_set]

        strategy = node.get_current_strategy()

        # Sampling policy: epsilon-on-policy for update player,
        # current strategy for opponent (matches OpenSpiel)
        if player == update_player:
            eps = self.epsilon
            sample_policy = [(eps / num_legal) + (1.0 - eps) * strategy[a]
                             for a in range(num_legal)]
        else:
            sample_policy = list(strategy)

        # Sample one action
        r = random.random()
        cumulative = 0.0
        sampled_idx = num_legal - 1
        for idx in range(num_legal):
            cumulative += sample_policy[idx]
            if r < cumulative:
                sampled_idx = idx
                break

        action = legal_actions[sampled_idx]
        next_state = state.apply_action(action)

        # Update reach probabilities
        if player == update_player:
            new_my_reach = my_reach * strategy[sampled_idx]
            new_opp_reach = opp_reach
        else:
            new_my_reach = my_reach
            new_opp_reach = opp_reach * strategy[sampled_idx]

        new_sample_reach = sample_reach * sample_policy[sampled_idx]

        # Recurse on sampled trajectory
        child_value = self.outcome_cfr(
            next_state, update_player,
            new_my_reach, new_opp_reach, new_sample_reach
        )

        # Baseline-corrected child values (vanilla: baseline = 0)
        # Sampled action: child_value / sample_prob
        # Unsampled actions: 0
        child_values = [0.0] * num_legal
        child_values[sampled_idx] = child_value / sample_policy[sampled_idx]

        # Value estimate = weighted sum over child values
        value_estimate = 0.0
        for a in range(num_legal):
            value_estimate += strategy[a] * child_values[a]

        if player == update_player:
            # Counterfactual value of the current strategy
            cf_value = value_estimate * opp_reach / sample_reach

            # Update regrets
            for idx in range(num_legal):
                cf_action_value = child_values[idx] * opp_reach / sample_reach
                node.regret_sum[idx] += cf_action_value - cf_value

            # Update average strategy
            for idx in range(num_legal):
                node.strategy_sum[idx] += my_reach / sample_reach * strategy[idx]

        return value_estimate

    def get_strategy_table(self) -> dict:
        """Return dict: info_set → {actions, strategy (action_name: prob)}."""
        table = {}
        for info_set in sorted(self.node_map.keys()):
            node, legal_actions = self.node_map[info_set]
            avg = node.get_average_strategy()
            action_names = {FOLD: 'fold', CHECK_CALL: 'check/call', RAISE: 'raise'}
            strat = {}
            for idx, action in enumerate(legal_actions):
                strat[action_names[action]] = avg[idx]
            table[info_set] = strat
        return table
