"""
Best Response computation for Kuhn Poker.

Given a fixed opponent strategy, compute the optimal counter-strategy.

In imperfect-information games, the BR player must choose the same
action at all game states within the same information set (they cannot
distinguish those states). We enumerate all 2^6 = 64 possible pure
strategies and evaluate each against the opponent's average strategy,
returning the maximum value.

This brute-force approach is correct and tractable for Kuhn Poker
(6 info sets per player, 6 possible deals). For larger games,
a bottom-up info-set-aggregated traversal would be needed instead.
"""

import sys
import os
from itertools import product

script_dir = os.path.dirname(os.path.abspath(__file__))
step02_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step02_dir)

from cfr.kuhn_poker import (
    PASS, BET, NUM_ACTIONS, ALL_DEALS,
    get_player, get_info_set, action_to_str,
)
from cfr.info_set_node import InfoSetNode

# All information sets per player in Kuhn Poker
_P0_INFO_SETS = ["1", "2", "3", "1pb", "2pb", "3pb"]
_P1_INFO_SETS = ["1p", "2p", "3p", "1b", "2b", "3b"]


def best_response_value(node_map: dict[str, InfoSetNode],
                        br_player: int) -> float:
    """
    Compute the best response value for br_player against the
    average strategy of the opponent stored in node_map.

    Enumerates all pure strategies for br_player (2^6 = 64 in Kuhn)
    and evaluates each against the opponent's average strategy across
    all 6 possible card deals.

    Returns:
        expected payoff for br_player under best response play
    """
    br_info_sets = _P0_INFO_SETS if br_player == 0 else _P1_INFO_SETS

    best_value = float('-inf')
    for actions in product(range(NUM_ACTIONS), repeat=len(br_info_sets)):
        br_strategy = dict(zip(br_info_sets, actions))
        value = _evaluate_br_strategy(node_map, br_player, br_strategy)
        best_value = max(best_value, value)

    return best_value


def _evaluate_br_strategy(node_map: dict[str, InfoSetNode],
                          br_player: int,
                          br_strategy: dict[str, int]) -> float:
    """Evaluate a fixed pure strategy for br_player against opponent."""
    total = 0.0
    for c0, c1 in ALL_DEALS:
        cards = [c0, c1]
        total += _eval_traverse(cards, "", br_player, br_strategy, node_map)
    return total / len(ALL_DEALS)


def _eval_traverse(cards: list, history: str, br_player: int,
                   br_strategy: dict[str, int],
                   node_map: dict[str, InfoSetNode]) -> float:
    """
    Recursively traverse the game tree evaluating a fixed BR strategy.

    At br_player nodes: follow the fixed br_strategy dict.
    At opponent nodes: follow opponent's average strategy from node_map.
    At terminal nodes: return payoff from br_player's perspective.
    """
    num_plays = len(history)
    player = num_plays % 2

    # Terminal check
    if num_plays > 1:
        terminal_pass = (history[-1] == 'p')
        double_bet = (history[-2:] == "bb")
        is_br_higher = cards[br_player] > cards[1 - br_player]

        if terminal_pass:
            if history == "pp":
                return 1.0 if is_br_higher else -1.0
            else:
                folder = (num_plays - 1) % 2
                return -1.0 if folder == br_player else 1.0
        elif double_bet:
            return 2.0 if is_br_higher else -2.0

    info_set = get_info_set(cards[player], history)

    if player == br_player:
        # Follow pre-determined BR strategy at this info set
        action = br_strategy[info_set]
        next_history = history + action_to_str(action)
        return _eval_traverse(cards, next_history, br_player,
                              br_strategy, node_map)
    else:
        # Opponent follows their average strategy
        if info_set in node_map:
            strategy = node_map[info_set].get_average_strategy()
        else:
            strategy = [1.0 / NUM_ACTIONS] * NUM_ACTIONS

        val = 0.0
        for a in range(NUM_ACTIONS):
            next_history = history + action_to_str(a)
            val += strategy[a] * _eval_traverse(cards, next_history,
                                                br_player, br_strategy,
                                                node_map)
        return val
