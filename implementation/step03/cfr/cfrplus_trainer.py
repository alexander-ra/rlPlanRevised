"""
CFR+ (Regret Matching Plus) trainer for Leduc Poker.

Implements Algorithm 1 from:
  Tammelin, O. (2014). "Solving Large Imperfect Information Games
  Using CFR+"

Full-traversal with alternating updates. Each iteration t:
  1. For each player i in {0, 1}:
     - Traverse all 120 deals, buffering regret increments
     - Apply buffered regrets atomically: r[a] = max(r[a] + Δ, 0)
  2. Strategy sums accumulated at opponent's info sets with
     linear weight w = max(t − d, 0)   (d = 0 by default)

Regret increments are buffered across deals so that every deal within
one (player, iteration) pass sees the same strategy.  The buffer is
applied with CFR+ flooring after the full pass.
"""

from cfr.info_set_node import InfoSetNode
from cfr.leduc_poker import (
    FOLD, CHECK_CALL, RAISE, NUM_ACTIONS,
    ALL_DEALS, NUM_CARDS, LeducState,
)


class LeducCFRPlusTrainer:
    """
    Trains an approximate Nash equilibrium for Leduc Poker using CFR+.

    Matches Algorithm 1 from Tammelin (2014):
    - Full tree traversal with alternating player updates
    - Regret flooring: r[a] = max(r[a] + Δ, 0)
    - Linear-weighted strategy accumulation (weight = iteration number)
    - Regret increments buffered across deals for strategy consistency
    """

    def __init__(self):
        self.node_map: dict[str, tuple[InfoSetNode, list]] = {}
        self.iteration_history = []

    def train(self, iterations: int, delay: int = 0) -> None:
        """
        Run CFR+ training.

        Args:
            iterations: number of full iterations
            delay: d parameter for weight = max(t - d, 0); 0 = standard
        """
        checkpoint_interval = max(1, iterations // 100)

        for t in range(1, iterations + 1):
            w = max(t - delay, 0)
            for traversing_player in (0, 1):
                regret_buffer: dict[str, list[float]] = {}
                for deal in ALL_DEALS:
                    state = LeducState((deal[0], deal[1]), deal[2])
                    self.cfr(state, traversing_player, w, 1.0,
                             regret_buffer)
                # Apply buffered regret deltas with CFR+ flooring
                for info_set, deltas in regret_buffer.items():
                    node, _ = self.node_map[info_set]
                    for a in range(node.num_actions):
                        node.regret_sum[a] = max(
                            node.regret_sum[a] + deltas[a], 0.0)

            if t % checkpoint_interval == 0 or t == iterations:
                self.iteration_history.append(t)

    def cfr(self, state: LeducState, traversing: int,
            weight: int, pi_opponent: float,
            regret_buffer: dict[str, list[float]]) -> float:
        """
        CFR+ recursive traversal for one traversing player.

        Args:
            state: current game state
            traversing: the player whose regrets are updated this pass
            weight: w for linear strategy-sum weighting
            pi_opponent: product of opponent reach probabilities
            regret_buffer: accumulates regret increments (applied after
                           all deals in the current pass)

        Returns:
            expected utility for *traversing* player at this node
        """
        if state.is_terminal():
            return state.get_utility(traversing)

        player = state.current_player()
        info_set = state.get_info_set(player)
        legal_actions = state.legal_actions()
        num_legal = len(legal_actions)

        if info_set not in self.node_map:
            node = InfoSetNode(num_legal)
            self.node_map[info_set] = (node, legal_actions)
        else:
            node, _ = self.node_map[info_set]

        strategy = node.get_current_strategy()

        if player == traversing:
            # --- Traversing player's node: compute regrets, buffer them ---
            util = [0.0] * num_legal
            node_util = 0.0
            for idx, action in enumerate(legal_actions):
                next_state = state.apply_action(action)
                util[idx] = self.cfr(next_state, traversing, weight,
                                     pi_opponent, regret_buffer)
                node_util += strategy[idx] * util[idx]

            # Buffer regret deltas (applied atomically after all deals)
            if info_set not in regret_buffer:
                regret_buffer[info_set] = [0.0] * num_legal
            for idx in range(num_legal):
                regret_buffer[info_set][idx] += (
                    pi_opponent * (util[idx] - node_util))

            return node_util
        else:
            # --- Opponent's node: pass through, accumulate strategy sum ---
            node_util = 0.0
            for idx, action in enumerate(legal_actions):
                next_state = state.apply_action(action)
                child_val = self.cfr(next_state, traversing, weight,
                                     pi_opponent * strategy[idx],
                                     regret_buffer)
                node_util += strategy[idx] * child_val

            # Linear-weighted strategy sum (paper line 37)
            for idx in range(num_legal):
                node.strategy_sum[idx] += pi_opponent * strategy[idx] * weight

            return node_util

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
