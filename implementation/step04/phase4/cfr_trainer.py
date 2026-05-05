"""Generic vanilla-CFR trainer for any Leduc-flavoured engine.

A single function, `train_cfr`, drives any state class implementing the
shared interface (`is_terminal`, `current_player`, `get_info_set`,
`legal_actions`, `apply_action`, `get_utility`). It accepts a
`deals_iterable` so the same trainer drives:

- the original 6-card engine with `ALL_DEALS` of length 120 (unit
  weights), and
- the rank-canonical engine with `CANONICAL_DEALS` of length 24
  (multiplicities summing to 120).

The buffered regret update mirrors the step03 reference implementation:
all per-iteration regret deltas are collected per info set and applied
atomically at the end of the deal traversal. This avoids mid-iteration
strategy drift across the deals enumerated within one CFR step.
"""

import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import InfoSetNode


def train_cfr(state_factory, deals_iterable, num_iterations: int,
              progress_every: int = 0):
    """Run vanilla CFR on a generic Leduc-shaped engine.

    Args:
        state_factory: callable `(cards_tuple, community)` -> game state.
        deals_iterable: iterable of either `(cards_tuple, community)` or
            `((cards_tuple, community), weight)` items. The trainer
            inspects the first item to pick the right unpacking.
        num_iterations: number of CFR iterations.
        progress_every: print iteration / time / info-set count every N
            iterations; 0 disables progress output.

    Returns:
        dict with keys:
            'node_map': dict[info_set_str, (InfoSetNode, legal_actions)]
            'iterations': num_iterations
            'wall_clock_seconds': total training time
    """
    deals_list = list(deals_iterable)
    if not deals_list:
        raise ValueError("deals_iterable must not be empty")

    # Treat `(deal_triple, weight)` as weighted; otherwise unit weights.
    sample = deals_list[0]
    is_weighted = (
        isinstance(sample, tuple) and len(sample) == 2
        and isinstance(sample[1], (int, float))
        and isinstance(sample[0], tuple) and len(sample[0]) == 3
    )

    node_map = {}
    start = time.time()

    for it in range(num_iterations):
        regret_buffer = {}
        for entry in deals_list:
            if is_weighted:
                deal, weight = entry
            else:
                deal = entry
                weight = 1.0
            cards = (deal[0], deal[1])
            community = deal[2]
            state = state_factory(cards, community)
            for player in (0, 1):
                deal_regret_buffer = {}
                _cfr(state, player, 1.0, 1.0, deal_regret_buffer, node_map,
                     state_factory)
                _merge_regret_buffer(regret_buffer, deal_regret_buffer,
                                     weight)

        # Atomic regret update + strategy accumulation.
        for info_set, deltas in regret_buffer.items():
            node, _legal = node_map[info_set]
            for a in range(node.num_actions):
                node.regret_sum[a] += deltas[a]

        # Strategy accumulation: walk the deals once more, recording the
        # current strategy weighted by the player's own reach probability.
        for entry in deals_list:
            if is_weighted:
                deal, weight = entry
            else:
                deal = entry
                weight = 1.0
            cards = (deal[0], deal[1])
            community = deal[2]
            state = state_factory(cards, community)
            for player in (0, 1):
                _accumulate_strategy(state, player, 1.0,
                                     node_map, weight)

        if progress_every and (it + 1) % progress_every == 0:
            elapsed = time.time() - start
            print(f"  iter {it + 1:>6}/{num_iterations}  "
                  f"info_sets={len(node_map):>4}  "
                  f"elapsed={elapsed:6.1f}s")

    elapsed_total = time.time() - start
    return {
        "node_map": node_map,
        "iterations": num_iterations,
        "wall_clock_seconds": elapsed_total,
    }


def _merge_regret_buffer(target: dict, source: dict, weight: float):
    """Merge a single chance branch's regret deltas into an iteration
    buffer, scaled by that branch's multiplicity.
    """
    for info_set, deltas in source.items():
        if info_set not in target:
            target[info_set] = [0.0] * len(deltas)
        out = target[info_set]
        for a, delta in enumerate(deltas):
            out[a] += weight * delta


def _cfr(state, traversing_player: int, p0_reach: float, p1_reach: float,
         regret_buffer: dict, node_map: dict, state_factory) -> float:
    """Recursive CFR traversal accumulating buffered regret deltas.

    Returns: counterfactual value from `traversing_player`'s perspective.
    """
    if state.is_terminal():
        return state.get_utility(traversing_player)

    player = state.current_player()
    info_set = state.get_info_set(player)
    legal = state.legal_actions()
    n = len(legal)

    if info_set not in node_map:
        node_map[info_set] = (InfoSetNode(n), legal)
    node, _ = node_map[info_set]
    strategy = node.get_current_strategy()

    if player == traversing_player:
        utils = [0.0] * n
        node_value = 0.0
        for i, a in enumerate(legal):
            child = state.apply_action(a)
            if player == 0:
                utils[i] = _cfr(child, traversing_player,
                                p0_reach * strategy[i], p1_reach,
                                regret_buffer, node_map, state_factory)
            else:
                utils[i] = _cfr(child, traversing_player,
                                p0_reach, p1_reach * strategy[i],
                                regret_buffer, node_map, state_factory)
            node_value += strategy[i] * utils[i]
        opp_reach = p1_reach if player == 0 else p0_reach
        if info_set not in regret_buffer:
            regret_buffer[info_set] = [0.0] * n
        for i in range(n):
            regret_buffer[info_set][i] += opp_reach * (utils[i] - node_value)
        return node_value

    # Opponent: weighted recursion only, no regret update from this
    # player's perspective.
    node_value = 0.0
    for i, a in enumerate(legal):
        child = state.apply_action(a)
        if player == 0:
            child_val = _cfr(child, traversing_player,
                             p0_reach * strategy[i], p1_reach,
                             regret_buffer, node_map, state_factory)
        else:
            child_val = _cfr(child, traversing_player,
                             p0_reach, p1_reach * strategy[i],
                             regret_buffer, node_map, state_factory)
        node_value += strategy[i] * child_val
    return node_value


def _accumulate_strategy(state, player_id: int, reach: float,
                         node_map: dict, weight: float):
    """Walk the tree once and accumulate the current strategy weighted
    by `player_id`'s reach probability times the deal multiplicity.
    """
    if state.is_terminal():
        return
    player = state.current_player()
    legal = state.legal_actions()
    info_set = state.get_info_set(player)
    if info_set not in node_map:
        return
    node, _ = node_map[info_set]
    strat = node.get_current_strategy()
    if player == player_id:
        for a in range(node.num_actions):
            node.strategy_sum[a] += weight * reach * strat[a]
    for i, a in enumerate(legal):
        next_reach = reach * strat[i] if player == player_id else reach
        _accumulate_strategy(state.apply_action(a), player_id, next_reach,
                             node_map, weight)
