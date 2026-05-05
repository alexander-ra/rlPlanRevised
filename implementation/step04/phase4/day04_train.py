"""Day 4 — train MCCFR on the triple-abstracted Extended Leduc and
report info-set counts after each successive abstraction.

External-sampling MCCFR is used (rather than vanilla CFR) because
Extended Leduc has 336 deals × deeper trees, making full-traversal CFR
too slow at the smoke-test budget. The trainer is a plain external-
sampling implementation modelled on step03's `mccfr_external_trainer`.

Outputs:
    phase4/.day04_results.json
"""

import argparse
import json
import os
import random
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import InfoSetNode
from extended_leduc import (
    ExtendedLeducState,
    ALL_DEALS,
    CANONICAL_DEALS,
    enumerate_info_sets,
)
from day04_combined import build_buckets, make_translator

RESULTS_PATH = os.path.join(_HERE, ".day04_results.json")


class _BucketedExtendedState(ExtendedLeducState):
    """Extended-Leduc state with the bucket translator wired into
    `get_info_set`.
    """

    def __init__(self, cards, community, abstracted, rank_canonical,
                 translator):
        super().__init__(cards, community, abstracted=abstracted,
                         rank_canonical=rank_canonical)
        self._translator = translator

    def get_info_set(self, player: int) -> str:
        base = super().get_info_set(player)
        return self._translator(base)

    def apply_action(self, action: int) -> "_BucketedExtendedState":
        s = _BucketedExtendedState(self.cards, self.community,
                                   self.abstracted, self.rank_canonical,
                                   self._translator)
        s.history = self.history
        s.round = self.round
        s.bets = list(self.bets)
        s.stacks = list(self.stacks)
        s.num_raises = list(self.num_raises)
        s.round_actions = list(self.round_actions)
        s.folded = self.folded
        s._is_terminal = self._is_terminal
        s._do_action(action)
        return s


def _external_mccfr(state, update_player, node_map, rng):
    """External-sampling MCCFR step. Returns the counterfactual value
    for `update_player`.

    On `update_player` nodes, all actions are explored and per-action
    counterfactual regrets are accumulated.

    On the opponent's nodes, a single action is sampled from the current
    strategy and the recursion only follows that branch.
    """
    if state.is_terminal():
        return state.get_utility(update_player)

    player = state.current_player()
    info = state.get_info_set(player)
    legal = state.legal_actions()
    n = len(legal)

    if info not in node_map:
        node_map[info] = (InfoSetNode(n), legal)
    node, _ = node_map[info]
    strat = node.get_current_strategy()

    if player == update_player:
        utils = [0.0] * n
        v = 0.0
        for i, a in enumerate(legal):
            utils[i] = _external_mccfr(state.apply_action(a),
                                       update_player, node_map, rng)
            v += strat[i] * utils[i]
        for i in range(n):
            node.regret_sum[i] += utils[i] - v
            node.strategy_sum[i] += strat[i]
        return v

    # Opponent — sample one action.
    r = rng.random()
    cumulative = 0.0
    sampled = n - 1
    for i in range(n):
        cumulative += strat[i]
        if r <= cumulative:
            sampled = i
            break
    return _external_mccfr(state.apply_action(legal[sampled]),
                           update_player, node_map, rng)


def train_mccfr(state_factory, deals_iterable, num_iterations: int,
                seed: int = 42):
    """Run external-sampling MCCFR for `num_iterations` iterations.

    Each iteration samples ONE deal (with multiplicity weighting if the
    deals list is weighted) and updates regrets for both players.
    """
    rng = random.Random(seed)
    deals_list = list(deals_iterable)
    is_weighted = (
        isinstance(deals_list[0], tuple)
        and len(deals_list[0]) == 2
        and isinstance(deals_list[0][1], (int, float))
    )

    if is_weighted:
        deal_choices = [d for d, _ in deals_list]
        weights = [w for _, w in deals_list]
    else:
        deal_choices = deals_list
        weights = [1.0] * len(deals_list)

    node_map = {}
    t0 = time.time()
    for it in range(num_iterations):
        deal = rng.choices(deal_choices, weights=weights, k=1)[0]
        cards = (deal[0], deal[1])
        community = deal[2]
        for player in (0, 1):
            state = state_factory(cards, community)
            _external_mccfr(state, player, node_map, rng)
    return node_map, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=20_000,
                    help="MCCFR iterations on the triple-abstracted "
                         "engine (default 20 000; smoke-test budget).")
    ap.add_argument("--k-preflop", type=int, default=3)
    ap.add_argument("--k-postflop", type=int, default=3)
    args = ap.parse_args()

    print("=== Day 4 — combined abstraction on Extended Leduc ===\n")

    # Step 1: report unabstracted info-set count.
    full_count = len(enumerate_info_sets(abstracted=False,
                                         rank_canonical=False))
    print(f"[1/4] Unabstracted Extended Leduc info sets:        {full_count}")

    # Step 2: rank-canonical (suit-iso) only.
    suit_count = len(enumerate_info_sets(abstracted=False,
                                         rank_canonical=True))
    print(f"[2/4] After suit isomorphism:                       {suit_count}")

    # Step 3: action-abstracted on top of suit-iso.
    suit_act_count = len(enumerate_info_sets(abstracted=True,
                                             rank_canonical=True))
    print(f"[3/4] After + action abstraction:                   {suit_act_count}")

    # Step 4: card bucketing + suit-iso + action.
    buckets = build_buckets(args.k_preflop, args.k_postflop)
    translator = make_translator(buckets, perfect_recall=False)

    def state_factory(cards, community):
        return _BucketedExtendedState(cards, community,
                                      abstracted=True,
                                      rank_canonical=True,
                                      translator=translator)

    print(f"[4/4] Triple-abstracted MCCFR ({args.iterations} iters)")
    nm, wall = train_mccfr(state_factory, CANONICAL_DEALS,
                           args.iterations)
    print(f"      info_sets={len(nm):>4}  wall={wall:.2f}s")

    out = {
        "iterations": args.iterations,
        "k_preflop": args.k_preflop,
        "k_postflop": args.k_postflop,
        "info_sets_unabstracted": full_count,
        "info_sets_suit_iso": suit_count,
        "info_sets_suit_iso_action_abstract": suit_act_count,
        "info_sets_triple_abstract": len(nm),
        "wall_clock_s": wall,
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
