"""
Best-response / exploitability for mini-NL Leduc.

Adapted from step03/evaluate/best_response.py. Parametrised on the game
class so the same code works for the full and action-abstracted variants.

The BR player is info-set-constrained: at each of their info sets they must
commit to a single action. Iterative refinement converges in <= tree depth.
"""

from mini_nl_leduc import ALL_DEALS, MiniNLLeducState


def best_response_value(node_map: dict, br_player: int, abstracted: bool) -> float:
    """Info-set-constrained BR value for `br_player` against the opponent's
    average strategy in `node_map`, evaluated in the game of the given
    abstraction flag.

    `node_map[info_set] = (InfoSetNode, legal_actions)` — legal_actions
    matches the order the trainer used, so node.strategy_sum is indexable
    in the same order.
    """
    br_strategy = {}

    for _ in range(12):
        br_cv: dict = {}

        for deal in ALL_DEALS:
            state = MiniNLLeducState((deal[0], deal[1]), deal[2], abstracted=abstracted)
            _br_accumulate(state, br_player, node_map, br_strategy, 1.0, br_cv)

        changed = False
        for info_set, action_vals in br_cv.items():
            best_a = max(action_vals, key=action_vals.get)
            if br_strategy.get(info_set) != best_a:
                changed = True
            br_strategy[info_set] = best_a
        if not changed:
            break

    total = 0.0
    for deal in ALL_DEALS:
        state = MiniNLLeducState((deal[0], deal[1]), deal[2], abstracted=abstracted)
        total += _br_eval(state, br_player, node_map, br_strategy)
    return total / len(ALL_DEALS)


def _br_accumulate(state, br_player, node_map, br_strategy, opp_reach, br_cv):
    if state.is_terminal():
        return state.get_utility(br_player)

    player = state.current_player()
    legal = state.legal_actions()

    if player == br_player:
        info_set = state.get_info_set(player)
        if info_set not in br_cv:
            br_cv[info_set] = {i: 0.0 for i in range(len(legal))}

        action_values = {}
        for idx, action in enumerate(legal):
            child_val = _br_accumulate(state.apply_action(action), br_player,
                                       node_map, br_strategy, opp_reach, br_cv)
            br_cv[info_set][idx] += opp_reach * child_val
            action_values[idx] = child_val

        if info_set in br_strategy:
            return action_values[br_strategy[info_set]]
        return max(action_values.values())

    # opponent node — follow average strategy
    info_set = state.get_info_set(player)
    if info_set in node_map:
        node, _ = node_map[info_set]
        strategy = node.get_average_strategy()
    else:
        strategy = [1.0 / len(legal)] * len(legal)

    val = 0.0
    for idx, action in enumerate(legal):
        child_val = _br_accumulate(state.apply_action(action), br_player,
                                   node_map, br_strategy,
                                   opp_reach * strategy[idx], br_cv)
        val += strategy[idx] * child_val
    return val


def _br_eval(state, br_player, node_map, br_strategy):
    if state.is_terminal():
        return state.get_utility(br_player)

    player = state.current_player()
    legal = state.legal_actions()

    if player == br_player:
        info_set = state.get_info_set(player)
        chosen = br_strategy.get(info_set, 0)
        return _br_eval(state.apply_action(legal[chosen]),
                        br_player, node_map, br_strategy)

    info_set = state.get_info_set(player)
    if info_set in node_map:
        node, _ = node_map[info_set]
        strategy = node.get_average_strategy()
    else:
        strategy = [1.0 / len(legal)] * len(legal)

    val = 0.0
    for idx, action in enumerate(legal):
        child_val = _br_eval(state.apply_action(action), br_player,
                             node_map, br_strategy)
        val += strategy[idx] * child_val
    return val


def exploitability(node_map: dict, abstracted: bool) -> float:
    br0 = best_response_value(node_map, br_player=0, abstracted=abstracted)
    br1 = best_response_value(node_map, br_player=1, abstracted=abstracted)
    return (br0 + br1) / 2
