"""
Counterfactual Regret Minimization (CFR) trainer for Kuhn Poker.

Based on Algorithm 1 from:
  "An Introduction to Counterfactual Regret Minimization"
   by Todd W. Neller and Marc Lanctot (2013)

Uses chance sampling: at each iteration, shuffle/deal cards randomly
rather than summing over all possible deals. This is simpler and
converges to the same result.
"""

import random

from cfr.info_set_node import InfoSetNode
from cfr.kuhn_poker import (
    PASS, BET, NUM_ACTIONS, CARD_NAMES,
    get_player, get_info_set, action_to_str,
)


class KuhnTrainer:
    """
    Trains an approximate Nash equilibrium for Kuhn Poker using CFR.

    Attributes:
        node_map: maps info set string → InfoSetNode
        game_value_history: average game values at checkpoints
        iteration_history: iteration numbers at checkpoints
    """

    def __init__(self):
        self.node_map: dict[str, InfoSetNode] = {}
        self.game_value_history = []
        self.iteration_history = []

    def train(self, iterations: int) -> float:
        """
        Run CFR training for the specified number of iterations.

        Each iteration:
          1. Shuffle cards (chance sampling)
          2. Call cfr() recursively from the root
          3. Accumulate the returned utility

        Returns:
            average game value for player 1
        """
        cards = [1, 2, 3]
        cumulative_util = 0.0
        checkpoint_interval = max(1, iterations // 200)

        for i in range(iterations):
            random.shuffle(cards)
            cumulative_util += self.cfr(cards, "", 1.0, 1.0)

            if (i + 1) % checkpoint_interval == 0 or i == iterations - 1:
                self.game_value_history.append(cumulative_util / (i + 1))
                self.iteration_history.append(i + 1)

        return cumulative_util / iterations

    def cfr(self, cards: list, history: str, p0: float, p1: float) -> float:
        """
        Core recursive CFR function.

        Walks the game tree, computes counterfactual values, updates regrets.

        Args:
            cards: [player1_card, player2_card, unused_card]
            history: string of actions taken so far
            p0: player 0's reach probability
            p1: player 1's reach probability

        Returns:
            expected utility for the current player at this node
        """
        num_plays = len(history)
        player = num_plays % 2
        opponent = 1 - player

        # Terminal state check
        if num_plays > 1:
            terminal_pass = (history[-1] == 'p')
            double_bet = (history[-2:] == "bb")
            is_player_card_higher = cards[player] > cards[opponent]

            if terminal_pass:
                if history == "pp":
                    return 1 if is_player_card_higher else -1
                else:
                    return 1
            elif double_bet:
                return 2 if is_player_card_higher else -2

        # Build information set and get/create node
        info_set = get_info_set(cards[player], history)
        if info_set not in self.node_map:
            self.node_map[info_set] = InfoSetNode()
        node = self.node_map[info_set]

        # Strategy computation via regret matching
        strategy = node.get_strategy(p0 if player == 0 else p1)

        # Recursive CFR calls for each action
        util = [0.0] * NUM_ACTIONS
        node_util = 0.0

        for a in range(NUM_ACTIONS):
            next_history = history + action_to_str(a)
            if player == 0:
                util[a] = -self.cfr(cards, next_history,
                                    p0 * strategy[a], p1)
            else:
                util[a] = -self.cfr(cards, next_history,
                                    p0, p1 * strategy[a])
            node_util += strategy[a] * util[a]

        # Regret update — weighted by opponent's reach probability
        for a in range(NUM_ACTIONS):
            regret = util[a] - node_util
            node.regret_sum[a] += (p1 if player == 0 else p0) * regret

        return node_util

    def get_strategy_table(self) -> dict:
        """
        Return a dict: info_set → {card, history, p_pass, p_bet}.
        """
        table = {}
        for info_set in sorted(self.node_map.keys()):
            node = self.node_map[info_set]
            avg = node.get_average_strategy()
            card = CARD_NAMES.get(int(info_set[0]), info_set[0])
            hist = info_set[1:] if len(info_set) > 1 else "(root)"
            table[info_set] = {
                "card": card,
                "history": hist,
                "p_pass": avg[PASS],
                "p_bet": avg[BET],
            }
        return table
