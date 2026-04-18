"""
Monte Carlo CFR with External Sampling for Leduc Poker.

External Sampling (Lanctot et al., 2009):
  - The "traverser" (player being updated) explores ALL their actions.
  - The opponent's actions are SAMPLED according to their current strategy.
  - Chance nodes are sampled (one deal per iteration, not all 120).

This is much faster per iteration than full CFR (no full tree traversal)
but noisier. Converges to Nash with enough iterations.

Each iteration updates only ONE player. Alternating updates between
player 0 and player 1 is standard.

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


class LeducExternalSamplingTrainer:
    """
    MCCFR with External Sampling for Leduc Poker.

    Per iteration:
      1. Sample a random deal (chance sampling)
      2. Traverse for the update player, exploring all their actions
      3. Sample opponent actions according to current strategy
      4. Alternate update player each iteration
    """

    def __init__(self):
        self.node_map: dict[str, tuple[InfoSetNode, list]] = {}
        self.game_value_history = []
        self.iteration_history = []

    def train(self, iterations: int) -> float:
        """
        Run External Sampling MCCFR.

        Alternates the update player each iteration.
        Returns average game value estimate for player 0.
        """
        cumulative_util = 0.0
        checkpoint_interval = max(1, iterations // 100)

        for i in range(iterations):
            # Sample a random deal
            cards = random.sample(range(NUM_CARDS), 3)
            p0_card, p1_card, community = cards[0], cards[1], cards[2]
            state = LeducState((p0_card, p1_card), community)

            # Alternate update player
            update_player = i % 2
            util = self.external_cfr(state, update_player)

            # Accumulate utility estimate (only meaningful for update_player=0)
            if update_player == 0:
                cumulative_util += util

            if (i + 1) % checkpoint_interval == 0 or i == iterations - 1:
                p0_iters = (i + 2) // 2  # number of P0-update iterations so far
                avg = cumulative_util / p0_iters if p0_iters > 0 else 0
                self.game_value_history.append(avg)
                self.iteration_history.append(i + 1)

        p0_iters = (iterations + 1) // 2
        return cumulative_util / p0_iters if p0_iters > 0 else 0

    def external_cfr(self, state: LeducState, update_player: int) -> float:
        """
        External Sampling CFR traversal.

        At update_player's nodes: explore ALL actions, compute regrets.
        At opponent's nodes: SAMPLE one action from current strategy.

        Args:
            state: current game state
            update_player: the player whose regrets we're updating

        Returns:
            utility for the update_player
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

        if player == update_player:
            # Traverser: explore ALL actions
            util = [0.0] * num_legal
            node_util = 0.0

            for idx, action in enumerate(legal_actions):
                next_state = state.apply_action(action)
                util[idx] = self.external_cfr(next_state, update_player)
                node_util += strategy[idx] * util[idx]

            # Update regrets (no reach probability weighting in external sampling)
            for idx in range(num_legal):
                node.regret_sum[idx] += util[idx] - node_util

            # Accumulate strategy (uniform weight — reach not tracked)
            for idx in range(num_legal):
                node.strategy_sum[idx] += strategy[idx]

            return node_util
        else:
            # Opponent: SAMPLE one action
            r = random.random()
            cumulative = 0.0
            sampled_idx = num_legal - 1
            for idx in range(num_legal):
                cumulative += strategy[idx]
                if r < cumulative:
                    sampled_idx = idx
                    break

            next_state = state.apply_action(legal_actions[sampled_idx])
            return self.external_cfr(next_state, update_player)

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
