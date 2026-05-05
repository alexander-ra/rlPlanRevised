"""Day 3 — train CFR on full and action-abstracted mini-NL Leduc, then
evaluate the abstracted strategy in the full game with each translator.

Procedure:
  1. Train CFR on the full mini-NL game (4 actions: fold, call, small,
     large).
  2. Train CFR on the action-abstracted mini-NL game (3 actions: fold,
     call, small).
  3. Evaluate exploitability of the full strategy in the full game.
  4. Evaluate exploitability of the abstracted strategy when deployed
     in the full game, with each of the three translators of
     `day03_translators.py` deciding what to do when the opponent plays
     `BET_LARGE`.

The day-3 best-response evaluator is a thin reimplementation rather than
a re-use of step03's `best_response_value`: the mini-NL Leduc game has 4
actions per node (vs 3 for fixed-limit Leduc), and the deal enumeration
runs over all 120 suit-deals, not the canonical 24.

Outputs:
    phase4/.day03_results.json
"""

import argparse
import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import InfoSetNode
from mini_nl_leduc import (
    ALL_DEALS,
    MiniNLLeducState,
    BET_SMALL,
    BET_LARGE,
    NUM_ACTIONS,
)
from cfr_trainer import _cfr, _accumulate_strategy
from day03_translators import translate

RESULTS_PATH = os.path.join(_HERE, ".day03_results.json")

# Bet-fraction map used by the translators: round 0 small=2 (~1× pot),
# large=4 (~2× pot). Round 1 small=4 (~1× pot), large=8 (~2× pot). For
# translation purposes both rounds share the same {1.0, 2.0} fraction
# pair. The abstraction keeps small = 1.0; the off-tree action is large
# = 2.0.
BET_FRACTIONS = {BET_SMALL: 1.0, BET_LARGE: 2.0}
ABSTRACT_LOW = BET_FRACTIONS[BET_SMALL]
ABSTRACT_HIGH_OFF_TREE = BET_FRACTIONS[BET_LARGE]


def train_cfr_mini_nl(abstracted: bool, num_iterations: int):
    """Vanilla CFR on mini-NL Leduc using `cfr_trainer._cfr` directly."""
    node_map = {}
    t0 = time.time()
    for it in range(num_iterations):
        regret_buffer = {}
        for deal in ALL_DEALS:
            cards = (deal[0], deal[1])
            community = deal[2]
            for player in (0, 1):
                state = MiniNLLeducState(cards, community,
                                         abstracted=abstracted)
                _cfr(state, player, 1.0, 1.0, regret_buffer, node_map,
                     state_factory=lambda c, com: MiniNLLeducState(
                         c, com, abstracted=abstracted))
        for info_set, deltas in regret_buffer.items():
            node, _ = node_map[info_set]
            for a in range(node.num_actions):
                node.regret_sum[a] += deltas[a]
        for deal in ALL_DEALS:
            cards = (deal[0], deal[1])
            community = deal[2]
            for player in (0, 1):
                state = MiniNLLeducState(cards, community,
                                         abstracted=abstracted)
                _accumulate_strategy(state, player, 1.0, node_map,
                                     weight=1.0)
    return node_map, time.time() - t0


def _strategy_at(state, node_map):
    info = state.get_info_set(state.current_player())
    if info not in node_map:
        legal = state.legal_actions()
        return [1.0 / len(legal)] * len(legal), legal
    node, legal = node_map[info]
    return node.get_average_strategy(), legal


def _strategy_with_translation(state, node_map_abstract, translator_name):
    """Look up the abstracted strategy for a state in the *full* game.

    If the state's legal action set is identical to the abstract game's
    (no `BET_LARGE` available right now), the abstract strategy maps
    cleanly. If `BET_LARGE` is among the legal actions (which it never
    is in the abstract game), the abstract strategy has no opinion on
    it: we instead split the abstract `{fold, call, small}` mass over
    `{fold, call, small, large}` by taking the abstract small-bet mass
    and translating *that* into a {small, large} mixture per the chosen
    translator. The fold and call masses pass through unchanged.

    This is the §6.4-vs-§3.2 contrast: a translator only fires for the
    off-tree action; everything else is a direct lookup.
    """
    # Build the abstract-key for this state by stripping `l` characters
    # from the history (since they cannot occur in the abstract tree).
    info_full = state.get_info_set(state.current_player())
    info_abstract = info_full.replace("l", "s")  # rough collapse
    if info_abstract in node_map_abstract:
        node, legal_abstract = node_map_abstract[info_abstract]
        avg = node.get_average_strategy()
        abstract_mix = dict(zip(legal_abstract, avg))
    else:
        legal = state.legal_actions()
        return [1.0 / len(legal)] * len(legal), legal

    legal_full = state.legal_actions()
    out = [0.0] * len(legal_full)
    for full_idx, action in enumerate(legal_full):
        if action == BET_LARGE:
            small_mass = abstract_mix.get(BET_SMALL, 0.0)
            split = translate(translator_name, ABSTRACT_HIGH_OFF_TREE,
                              ABSTRACT_LOW, ABSTRACT_HIGH_OFF_TREE)
            # The translator says how a real `BET_LARGE` would have been
            # mapped *into* the abstraction. We invert: the abstract
            # small-bet mass should be redistributed in the same ratio
            # over {small, large} in the full game.
            for fraction, p in split.items():
                if fraction == ABSTRACT_HIGH_OFF_TREE:
                    out[full_idx] += small_mass * p
        elif action == BET_SMALL:
            small_mass = abstract_mix.get(BET_SMALL, 0.0)
            split = translate(translator_name, ABSTRACT_HIGH_OFF_TREE,
                              ABSTRACT_LOW, ABSTRACT_HIGH_OFF_TREE)
            for fraction, p in split.items():
                if fraction == ABSTRACT_LOW:
                    out[full_idx] += small_mass * p
            # If `BET_LARGE` is not legal at this node (e.g. stack
            # constraint), the small-bet mass remains intact.
            if BET_LARGE not in legal_full:
                out[full_idx] = small_mass
        else:
            out[full_idx] = abstract_mix.get(action, 0.0)
    s = sum(out)
    if s > 0:
        out = [x / s for x in out]
    else:
        out = [1.0 / len(legal_full)] * len(legal_full)
    return out, legal_full


def best_response_full_game(node_map, br_player: int,
                            translator_name: str = None,
                            node_map_abstract=None) -> float:
    """Iterative info-set-constrained best response over the full mini-NL
    Leduc game. If `translator_name` is given, the *opponent* (non-BR
    player) plays the abstract strategy through the translator.
    """
    br_strategy = {}
    for _ in range(12):
        br_cv = {}
        for deal in ALL_DEALS:
            cards = (deal[0], deal[1])
            community = deal[2]
            state = MiniNLLeducState(cards, community, abstracted=False)
            _br_walk(state, br_player, node_map, br_strategy, 1.0, br_cv,
                     translator_name, node_map_abstract)
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
        cards = (deal[0], deal[1])
        community = deal[2]
        state = MiniNLLeducState(cards, community, abstracted=False)
        total += _br_eval(state, br_player, node_map, br_strategy,
                          translator_name, node_map_abstract)
    return total / len(ALL_DEALS)


def _br_walk(state, br_player, node_map, br_strategy, opp_reach, br_cv,
             translator_name, node_map_abstract):
    if state.is_terminal():
        return state.get_utility(br_player)
    player = state.current_player()
    legal = state.legal_actions()
    if player == br_player:
        info = state.get_info_set(player)
        if info not in br_cv:
            br_cv[info] = {i: 0.0 for i in range(len(legal))}
        action_values = {}
        for idx, a in enumerate(legal):
            child = state.apply_action(a)
            v = _br_walk(child, br_player, node_map, br_strategy,
                         opp_reach, br_cv, translator_name,
                         node_map_abstract)
            br_cv[info][idx] += opp_reach * v
            action_values[idx] = v
        if info in br_strategy:
            return action_values[br_strategy[info]]
        return max(action_values.values())

    # Opponent: follow either the full-game `node_map` or the
    # translator-wrapped abstract `node_map_abstract`.
    if translator_name and node_map_abstract is not None:
        strat, legal_eff = _strategy_with_translation(
            state, node_map_abstract, translator_name)
    else:
        strat, legal_eff = _strategy_at(state, node_map)
    val = 0.0
    for idx, a in enumerate(legal_eff):
        child = state.apply_action(a)
        val += strat[idx] * _br_walk(
            child, br_player, node_map, br_strategy,
            opp_reach * strat[idx], br_cv, translator_name,
            node_map_abstract)
    return val


def _br_eval(state, br_player, node_map, br_strategy, translator_name,
             node_map_abstract):
    if state.is_terminal():
        return state.get_utility(br_player)
    player = state.current_player()
    legal = state.legal_actions()
    if player == br_player:
        info = state.get_info_set(player)
        chosen = br_strategy.get(info, 0)
        return _br_eval(state.apply_action(legal[chosen]), br_player,
                        node_map, br_strategy, translator_name,
                        node_map_abstract)
    if translator_name and node_map_abstract is not None:
        strat, legal_eff = _strategy_with_translation(
            state, node_map_abstract, translator_name)
    else:
        strat, legal_eff = _strategy_at(state, node_map)
    val = 0.0
    for idx, a in enumerate(legal_eff):
        val += strat[idx] * _br_eval(
            state.apply_action(a), br_player, node_map, br_strategy,
            translator_name, node_map_abstract)
    return val


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=100,
                    help="CFR iterations per game (default 100; "
                         "smoke-test budget).")
    args = ap.parse_args()

    print("=== Day 3 — action abstraction + translation on mini-NL Leduc ===\n")

    print(f"[1/4] Train CFR on the full mini-NL game ({args.iterations} iters)")
    full_nm, full_t = train_cfr_mini_nl(abstracted=False,
                                        num_iterations=args.iterations)
    print(f"      info_sets={len(full_nm):>4}  wall={full_t:.2f}s")

    print(f"\n[2/4] Train CFR on the action-abstracted game ({args.iterations} iters)")
    abs_nm, abs_t = train_cfr_mini_nl(abstracted=True,
                                      num_iterations=args.iterations)
    print(f"      info_sets={len(abs_nm):>4}  wall={abs_t:.2f}s")

    print("\n[3/4] Score full strategy in the full game (no translator)")
    exp_full = (best_response_full_game(full_nm, 0)
                + best_response_full_game(full_nm, 1))
    print(f"      exploitability_full = {exp_full:.5f}")

    print("\n[4/4] Score abstracted strategy in the full game per translator")
    translator_results = {}
    for name in ("nearest", "probability_split", "pseudo_harmonic"):
        e = (best_response_full_game(full_nm, 0,
                                     translator_name=name,
                                     node_map_abstract=abs_nm)
             + best_response_full_game(full_nm, 1,
                                       translator_name=name,
                                       node_map_abstract=abs_nm))
        translator_results[name] = e
        gap = e - exp_full
        print(f"      {name:>20}: exploit={e:.5f}  gap={gap:+.5f}")

    out = {
        "iterations": args.iterations,
        "full_info_sets": len(full_nm),
        "abstract_info_sets": len(abs_nm),
        "exploit_full": exp_full,
        "exploit_per_translator": translator_results,
        "wall_clock_full_s": full_t,
        "wall_clock_abstract_s": abs_t,
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
