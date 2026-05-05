"""Card-bucketing abstraction for Leduc.

Composes day-2's `hand_strength`, `emd`, and `kmeans_emd` modules into a
runnable lossy abstraction:

  1. compute the HSD per (private rank, community rank) info set,
  2. cluster pre-flop and post-flop info sets *separately* into `k`
     buckets each (so per-round bucket budgets stack),
  3. expose a key-translator from full-game info-set keys to
     bucketed keys for the day-1 exploitability evaluator.

Two recall flavours are provided:

- `perfect_recall=True` — the bucket trail is preserved across rounds.
  A round-1 info set's key includes the round-0 bucket id this hand
  belonged to. The agent never forgets which bucket it was in.

- `perfect_recall=False` — the round-0 bucket is discarded once the
  round-1 community card is revealed. Different hands that travel
  through different round-0 buckets can collide in round 1 if they
  share the same round-1 bucket. This is the §6.1 Level 2 / §6.2
  imperfect-recall mode that frees buckets for later rounds.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import card_rank
from day02_hand_strength import (
    NUM_RANKS,
    hsd_pre_flop,
    hsd_post_flop,
)
from day02_kmeans_emd import kmeans_emd


def build_card_buckets(k_preflop: int, k_postflop: int, seed: int = 42):
    """Cluster Leduc info sets into bucket ids per round.

    Returns:
        dict with two sub-mappings:
            'preflop': {p_rank: bucket_id} for p_rank in 0..NUM_RANKS-1
            'postflop': {(p_rank, c_rank): bucket_id}
    """
    # Pre-flop bucketing
    preflop_keys = [(p,) for p in range(NUM_RANKS)]
    preflop_hists = [hsd_pre_flop(p) for p in range(NUM_RANKS)]
    if k_preflop >= len(preflop_keys):
        # Trivial — every info set its own bucket.
        preflop_assign = {p: idx for idx, (p,) in enumerate(preflop_keys)}
    else:
        preflop_result = kmeans_emd(preflop_hists, k=k_preflop,
                                    n_restarts=5, seed=seed)
        preflop_assign = {p[0]: preflop_result["labels"][i]
                          for i, p in enumerate(preflop_keys)}

    # Post-flop bucketing
    postflop_keys = []
    postflop_hists = []
    for p in range(NUM_RANKS):
        for c in range(NUM_RANKS):
            postflop_keys.append((p, c))
            postflop_hists.append(hsd_post_flop(p, c))
    if k_postflop >= len(postflop_keys):
        postflop_assign = {key: idx
                           for idx, key in enumerate(postflop_keys)}
    else:
        postflop_result = kmeans_emd(postflop_hists, k=k_postflop,
                                     n_restarts=5, seed=seed + 1)
        postflop_assign = {key: postflop_result["labels"][i]
                           for i, key in enumerate(postflop_keys)}

    return {"preflop": preflop_assign, "postflop": postflop_assign}


def make_key_translator(buckets: dict, perfect_recall: bool = False):
    """Return a callable `(full_game_info_set_key) -> bucketed_key`.

    Full-game keys have the form
        round 0: "<card_id>|<history>"
        round 1: "<card_id>:<community_card_id>|<history>"
    """

    preflop_assign = buckets["preflop"]
    postflop_assign = buckets["postflop"]

    def translate(full_key: str) -> str:
        head, sep, tail = full_key.partition("|")
        if ":" in head:
            # Round 1 — postflop
            priv_str, _, comm_str = head.partition(":")
            p_rank = int(priv_str) // 2
            c_rank = int(comm_str) // 2
            postflop_id = postflop_assign[(p_rank, c_rank)]
            if perfect_recall:
                preflop_id = preflop_assign[p_rank]
                head_out = f"{preflop_id}>{postflop_id}"
            else:
                head_out = f"b{postflop_id}"
            return head_out + sep + tail
        # Round 0 — preflop
        p_rank = int(head) // 2
        preflop_id = preflop_assign[p_rank]
        return f"b{preflop_id}" + sep + tail

    return translate


def bucketed_info_set_count(buckets: dict, perfect_recall: bool) -> int:
    """Count the number of distinct *bucketed* info sets the translator
    can produce for Leduc, ignoring history. This is the lower bound on
    info-set count after bucketing.
    """
    n_preflop = len(set(buckets["preflop"].values()))
    if perfect_recall:
        n_postflop = len(set((buckets["preflop"][p],
                              buckets["postflop"][(p, c)])
                             for (p, c) in buckets["postflop"]))
    else:
        n_postflop = len(set(buckets["postflop"].values()))
    return n_preflop + n_postflop


if __name__ == "__main__":
    print("=== Card-bucket sweep on Leduc ===\n")
    for k in (2, 3, "full"):
        if k == "full":
            kp = NUM_RANKS
            kf = NUM_RANKS * NUM_RANKS
            label = "full"
        else:
            kp = k
            kf = k
            label = f"k={k}"
        buckets = build_card_buckets(kp, kf)
        for recall in (True, False):
            tag = "perfect" if recall else "imperfect"
            n = bucketed_info_set_count(buckets, perfect_recall=recall)
            print(f"  {label:>5}, recall={tag:>9}: {n} bucketed info sets "
                  f"(before history)")
        print()
