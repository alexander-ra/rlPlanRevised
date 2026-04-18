"""
Counterfactual Regret Minimization (CFR) trainer for Leduc Poker.

Full-traversal vanilla CFR with alternating updates.  Each iteration
traverses all 120 deals for player 0 (updating only player 0 regrets),
then repeats for player 1.  Strategy sums are accumulated at the
*opponent's* information sets during traversal (uniform weighting).

Regret increments are buffered across deals so that every deal within
one (player, iteration) pass sees the same strategy.  The buffer is
applied additively (no flooring) after the full pass.
"""

from cfr.info_set_node import InfoSetNode
from cfr.leduc_poker import (
    FOLD, CHECK_CALL, RAISE, NUM_ACTIONS,
    ALL_DEALS, NUM_CARDS, LeducState,
)


class LeducTrainer:
    """
    Trains an approximate Nash equilibrium for Leduc Poker using vanilla CFR.

    Attributes:
        node_map: maps info set string → (InfoSetNode, legal_actions)
        iteration_history: iteration numbers at checkpoints
    """

    def __init__(self):
        self.node_map: dict[str, tuple[InfoSetNode, list]] = {}
        self.iteration_history = []

    def train(self, iterations: int) -> None:
        """Run vanilla CFR for the specified number of iterations."""
        checkpoint_interval = max(1, iterations // 100)

        for t in range(1, iterations + 1):
            for traversing_player in (0, 1):
                regret_buffer: dict[str, list[float]] = {}
                for deal in ALL_DEALS:
                    state = LeducState((deal[0], deal[1]), deal[2])
                    self.cfr(state, traversing_player, 1.0, regret_buffer)
                # Apply buffered regret deltas (no flooring)
                for info_set, deltas in regret_buffer.items():
                    node, _ = self.node_map[info_set]
                    for a in range(node.num_actions):
                        node.regret_sum[a] += deltas[a]

            if t % checkpoint_interval == 0 or t == iterations:
                self.iteration_history.append(t)

    def cfr(self, state: LeducState, traversing: int,
            pi_opponent: float,
            regret_buffer: dict[str, list[float]]) -> float:
        """
        Recursive CFR traversal for one traversing player.

        Args:
            state: current game state
            traversing: the player whose regrets are updated this pass
            pi_opponent: product of opponent (and chance) reach probs
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
            # --- Traversing player's node: compute regrets ---
            util = [0.0] * num_legal
            node_util = 0.0
            for idx, action in enumerate(legal_actions):
                next_state = state.apply_action(action)
                util[idx] = self.cfr(next_state, traversing, pi_opponent,
                                     regret_buffer)
                node_util += strategy[idx] * util[idx]

            # Buffer regret deltas (applied after all deals)
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
                child_val = self.cfr(next_state, traversing,
                                     pi_opponent * strategy[idx],
                                     regret_buffer)
                node_util += strategy[idx] * child_val

            for idx in range(num_legal):
                node.strategy_sum[idx] += pi_opponent * strategy[idx]

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
