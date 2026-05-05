"""Day 2 — sweep card-bucket counts × recall flavour, train CFR on each
bucketed engine, score exploitability in the full game.

Usage:
    python implementation/step04/phase4/day02_train.py [--iterations N]

Outputs:
    phase4/.day02_results.json — one entry per (k, recall) configuration
    with info-set count, exploitability, and wall-clock seconds.

Implementation note: rather than build a separate "bucketed engine", we
train CFR on the rank-canonical engine with a custom `get_info_set`
override applied via subclassing. The override delegates to the
key translator from `day02_card_bucketing`. This keeps the trainer
identical between days and isolates the abstraction effect to a single
function call.
"""

import argparse
import json
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_rank_engine import LeducRankState, CANONICAL_DEALS
from cfr_trainer import train_cfr
from exploitability import exploitability_via_proxy
from day02_card_bucketing import (
    build_card_buckets,
    make_key_translator,
)
from day02_hand_strength import NUM_RANKS

RESULTS_PATH = os.path.join(_HERE, ".day02_results.json")


def _make_bucketed_state_factory(buckets: dict, perfect_recall: bool):
    """Build a `state_factory` that returns LeducRankState instances
    whose `get_info_set` is overridden to apply the bucket translator.

    The override translates the rank-canonical key (which uses ranks
    directly) into a fully bucketed key. It re-uses the same translator
    as the post-hoc proxy used at evaluation time, so training and
    evaluation see identical info-set structures.
    """
    rank_translator = make_key_translator(buckets, perfect_recall)

    def state_factory(cards, community):
        # The rank engine exposes ranks directly; the translator expects
        # full-game card-id keys. We adapt by inflating each rank to
        # `2*rank` (suit 0) before calling the translator.
        s = _BucketedRankState(cards, community, rank_translator)
        return s

    return state_factory


class _BucketedRankState(LeducRankState):
    """`LeducRankState` whose info-set keys go through a card translator.

    The translator was designed for full-game keys (card-id form). To
    reuse it from the rank engine we inflate each rank to a card id of
    the form `2 * rank` (suit 0), call the translator, and the output is
    a bucketed key indexed by rank — which is what we want.
    """

    def __init__(self, cards, community, rank_translator):
        super().__init__(cards, community)
        self._rank_translator = rank_translator

    def get_info_set(self, player: int) -> str:
        # Rebuild a full-game-shaped key, then translate.
        rank = self.cards[player]
        if self.round >= 1:
            full_key = f"{2 * rank}:{2 * self.community}|{self.history}"
        else:
            full_key = f"{2 * rank}|{self.history}"
        return self._rank_translator(full_key)

    def apply_action(self, action: int) -> "_BucketedRankState":
        s = _BucketedRankState(self.cards, self.community,
                               self._rank_translator)
        s.history = self.history
        s.round = self.round
        s.bets = list(self.bets)
        s.num_raises = list(self.num_raises)
        s.round_actions = list(self.round_actions)
        s.folded = self.folded
        s._is_terminal = self._is_terminal
        s._do_action(action)
        return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=200,
                    help="CFR iterations per configuration "
                         "(default 200; smoke-test budget).")
    ap.add_argument("--skip-exploit", action="store_true")
    args = ap.parse_args()

    print("=== Day 2 — lossy card bucketing on Leduc ===\n")

    configurations = []
    for k_label, kp, kf in [("k2", 2, 2), ("k3", 3, 3),
                            ("k5", min(3, NUM_RANKS),
                             min(5, NUM_RANKS * NUM_RANKS)),
                            ("full", NUM_RANKS,
                             NUM_RANKS * NUM_RANKS)]:
        for recall in (True, False):
            recall_label = "perfect" if recall else "imperfect"
            configurations.append((k_label, recall_label, kp, kf, recall))

    results = []
    for k_label, recall_label, kp, kf, recall in configurations:
        tag = f"{k_label}_{recall_label}"
        print(f"--- config: {tag}  (kp={kp}, kf={kf}) ---")
        buckets = build_card_buckets(kp, kf)
        state_factory = _make_bucketed_state_factory(buckets, recall)
        t0 = time.time()
        result = train_cfr(
            state_factory=state_factory,
            deals_iterable=CANONICAL_DEALS,
            num_iterations=args.iterations,
            progress_every=0,
        )
        t1 = time.time()
        n_info_sets = len(result["node_map"])
        wall = t1 - t0
        print(f"  info_sets={n_info_sets:>4}  wall_clock={wall:6.2f}s")

        entry = {
            "config": tag,
            "k_preflop": kp,
            "k_postflop": kf,
            "recall": recall_label,
            "info_sets": n_info_sets,
            "wall_clock_s": wall,
        }

        if not args.skip_exploit:
            translator = make_key_translator(buckets, recall)
            # Compose translators: full -> rank -> bucket. Since our
            # `_BucketedRankState` already produces bucketed keys at
            # train time, the rank translator alone (driven from full
            # cards via the same inflation path) is the right proxy.
            def full_to_bucket(full_key, _t=translator):
                return _t(full_key)
            exp = exploitability_via_proxy(
                result["node_map"], full_to_bucket)
            print(f"  exploitability_full_game = {exp:.5f}")
            entry["exploitability"] = exp

        results.append(entry)
        print()

    with open(RESULTS_PATH, "w") as f:
        json.dump({"iterations": args.iterations, "results": results},
                  f, indent=2)
    print(f"Results saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
