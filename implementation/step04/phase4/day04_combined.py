"""Combined abstraction (suits + buckets + actions) on Extended Leduc.

Composes the day 1, day 2, and day 3 modules into a single abstraction
pipeline:

    Extended Leduc (336 deals, 8 cards)
      ├─→ suit isomorphism      (rank-canonical engine, day 1 idea)
      ├─→ card bucketing        (k=3 buckets per round, day 2 idea)
      └─→ action abstraction    ({fold, call, small}, day 3 idea)

Each successive abstraction reduces the info-set count further. The
day-4 trainer reports the count after each step so the day-5 Pareto
plot has a clean data point per configuration.

The bucketing pipeline is reused from day 2 unchanged — Extended Leduc's
HSDs are computed by the same `hand_strength_at_showdown` formula, just
with `NUM_RANKS=4`. We re-implement the per-rank HSD here so the day-2
module stays Leduc-3-only.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from extended_leduc import (
    NUM_RANKS,
    NUM_CARDS,
    COPIES_PER_RANK,
    showdown_winner,
)
from day02_emd import emd_distance
from day02_kmeans_emd import kmeans_emd

HSD_BINS = 50


def _bin(value: float) -> int:
    if value <= 0.0:
        return 0
    if value >= 1.0:
        return HSD_BINS - 1
    return int(value * HSD_BINS)


def hand_strength(p_rank: int, c_rank: int) -> float:
    """`P(win) + 0.5 * P(tie)` for `p_rank` against a uniform random
    opponent rank, given a known community rank.
    """
    wins = 0
    ties = 0
    total = 0
    for opp_rank in range(NUM_RANKS):
        for _suit in range(COPIES_PER_RANK):
            outcome = showdown_winner((p_rank, opp_rank), c_rank)
            if outcome == 1:
                wins += 1
            elif outcome == 0:
                ties += 1
            total += 1
    return (wins + 0.5 * ties) / total


def hsd_post_flop(p_rank: int, c_rank: int) -> list:
    hist = [0.0] * HSD_BINS
    hist[_bin(hand_strength(p_rank, c_rank))] = 1.0
    return hist


def hsd_pre_flop(p_rank: int) -> list:
    weights = []
    for c_rank in range(NUM_RANKS):
        if c_rank == p_rank:
            weights.append(1.0)
        else:
            weights.append(2.0)
    total = sum(weights)
    weights = [w / total for w in weights]
    hist = [0.0] * HSD_BINS
    for c_rank, w in enumerate(weights):
        post = hsd_post_flop(p_rank, c_rank)
        for i in range(HSD_BINS):
            hist[i] += w * post[i]
    return hist


def build_buckets(k_preflop: int, k_postflop: int, seed: int = 42) -> dict:
    """Cluster Extended Leduc's HSDs into `k_preflop` pre-flop and
    `k_postflop` post-flop buckets.
    """
    pre_hists = [hsd_pre_flop(p) for p in range(NUM_RANKS)]
    if k_preflop >= NUM_RANKS:
        pre_assign = {p: p for p in range(NUM_RANKS)}
    else:
        pre_res = kmeans_emd(pre_hists, k=k_preflop, n_restarts=5, seed=seed)
        pre_assign = {p: pre_res["labels"][p] for p in range(NUM_RANKS)}

    post_keys = [(p, c) for p in range(NUM_RANKS) for c in range(NUM_RANKS)]
    post_hists = [hsd_post_flop(p, c) for p, c in post_keys]
    if k_postflop >= len(post_keys):
        post_assign = {key: idx for idx, key in enumerate(post_keys)}
    else:
        post_res = kmeans_emd(post_hists, k=k_postflop, n_restarts=5,
                              seed=seed + 1)
        post_assign = {key: post_res["labels"][i]
                       for i, key in enumerate(post_keys)}
    return {"preflop": pre_assign, "postflop": post_assign}


def make_translator(buckets: dict, perfect_recall: bool = False):
    """Translate a (rank-canonical, action-abstracted) Extended Leduc
    info-set key of the form `<rank>|<history>` or
    `<rank>:<community_rank>|<history>` into a bucketed key.
    """
    pre = buckets["preflop"]
    post = buckets["postflop"]

    def translate(key: str) -> str:
        head, sep, tail = key.partition("|")
        if ":" in head:
            priv_str, _, comm_str = head.partition(":")
            p, c = int(priv_str), int(comm_str)
            post_id = post[(p, c)]
            head_out = (f"{pre[p]}>{post_id}" if perfect_recall
                        else f"b{post_id}")
        else:
            head_out = f"b{pre[int(head)]}"
        return head_out + sep + tail

    return translate
