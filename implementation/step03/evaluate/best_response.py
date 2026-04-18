"""
Best Response computation for Leduc Poker.

Info-set-constrained best response: the BR player must play the
same action at all game states in the same information set.

Uses iterative refinement:
  1. Traverse all deals, accumulating counterfactual values per info set per action.
  2. Pick the best action at each info set.
  3. Repeat with the updated BR strategy until stable.
  4. Evaluate the final BR value exactly.

This matches the exploitability metric used by OpenSpiel (NashConv).
"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
step03_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step03_dir)

from cfr.leduc_poker import ALL_DEALS, LeducState, NUM_ACTIONS
from cfr.info_set_node import InfoSetNode


def best_response_value(node_map: dict, br_player: int) -> float:
    """
    Compute the info-set-constrained best response value for br_player
    against the average strategy of the opponent stored in node_map.

    Iteratively refines the BR strategy until stable, then evaluates
    the exact expected value.
    """
    br_strategy = {}  # info_set -> chosen action index

    for _ in range(10):  # Converges in ≤ tree_depth iterations
        br_cv = {}  # info_set -> {action_idx: counterfactual_value}

        for deal in ALL_DEALS:
            p0_card, p1_card, community = deal
            state = LeducState((p0_card, p1_card), community)
            _br_accumulate(state, br_player, node_map,
                           br_strategy, 1.0, br_cv)

        # Update BR strategy: pick best action at each info set
        changed = False
        for info_set, action_vals in br_cv.items():
            best_a = max(action_vals, key=action_vals.get)
            if info_set not in br_strategy or br_strategy[info_set] != best_a:
                changed = True
            br_strategy[info_set] = best_a

        if not changed:
            break

    # Evaluate exact BR value under the final strategy
    total = 0.0
    for deal in ALL_DEALS:
        p0_card, p1_card, community = deal
        state = LeducState((p0_card, p1_card), community)
        total += _br_eval(state, br_player, node_map, br_strategy)
    return total / len(ALL_DEALS)


def _br_accumulate(state: LeducState, br_player: int,
                   node_map: dict, br_strategy: dict,
                   opp_reach: float, br_cv: dict) -> float:
    """
    Traverse game tree accumulating counterfactual values at BR info sets.

    At BR player nodes: explores ALL actions (for cv computation),
    returns value under the current BR strategy for upstream use.
    At opponent nodes: follows their average strategy.

    Returns: value for br_player at this state (under current BR strategy).
    """
    if state.is_terminal():
        return state.get_utility(br_player)

    player = state.current_player()
    legal_actions = state.legal_actions()

    if player == br_player:
        info_set = state.get_info_set(player)
        if info_set not in br_cv:
            br_cv[info_set] = {i: 0.0 for i in range(len(legal_actions))}

        # Explore ALL actions to compute counterfactual values
        action_values = {}
        for idx, action in enumerate(legal_actions):
            child_val = _br_accumulate(
                state.apply_action(action), br_player, node_map,
                br_strategy, opp_reach, br_cv)
            br_cv[info_set][idx] += opp_reach * child_val
            action_values[idx] = child_val

        # Return value under current BR strategy (for upstream nodes)
        if info_set in br_strategy:
            return action_values[br_strategy[info_set]]
        else:
            # First iteration: use per-state best as initial estimate
            return max(action_values.values())
    else:
        # Opponent: follow average strategy
        info_set = state.get_info_set(player)
        if info_set in node_map:
            node, _ = node_map[info_set]
            strategy = node.get_average_strategy()
        else:
            strategy = [1.0 / len(legal_actions)] * len(legal_actions)

        val = 0.0
        for idx, action in enumerate(legal_actions):
            child_val = _br_accumulate(
                state.apply_action(action), br_player, node_map,
                br_strategy, opp_reach * strategy[idx], br_cv)
            val += strategy[idx] * child_val
        return val


def _br_eval(state: LeducState, br_player: int,
             node_map: dict, br_strategy: dict) -> float:
    """
    Evaluate the expected value for br_player when following
    the determined BR strategy against the opponent's average strategy.
    """
    if state.is_terminal():
        return state.get_utility(br_player)

    player = state.current_player()
    legal_actions = state.legal_actions()

    if player == br_player:
        info_set = state.get_info_set(player)
        chosen = br_strategy.get(info_set, 0)
        return _br_eval(
            state.apply_action(legal_actions[chosen]),
            br_player, node_map, br_strategy)
    else:
        info_set = state.get_info_set(player)
        if info_set in node_map:
            node, _ = node_map[info_set]
            strategy = node.get_average_strategy()
        else:
            strategy = [1.0 / len(legal_actions)] * len(legal_actions)

        val = 0.0
        for idx, action in enumerate(legal_actions):
            child_val = _br_eval(
                state.apply_action(action),
                br_player, node_map, br_strategy)
            val += strategy[idx] * child_val
        return val
