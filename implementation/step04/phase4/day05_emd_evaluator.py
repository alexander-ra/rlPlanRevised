"""Direct EMD-based abstraction-quality proxy.

Implements §6.2 Tool 2 of the deliverable: for an explicit partition
`P` over Leduc's info sets, sum the EMD between each abstract bucket's
mean HSD and the HSDs of the original info sets it covers, weighted by
each info set's reach probability (here approximated by uniform reach
over the chance-deal distribution).

A single scalar `emd_proxy(buckets, perfect_recall)` is returned per
configuration. Empirically this is the strongest predictor of
post-solve exploitability that does not require solving anything.

The function is keyed on the day-2 / day-4 bucket structure
`{'preflop': {...}, 'postflop': {...}}` so it works across both
configurations.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from day02_emd import emd_distance
from day02_hand_strength import (
    NUM_RANKS,
    hsd_pre_flop,
    hsd_post_flop,
)


def _mean_hist(hists):
    if not hists:
        return None
    n = len(hists[0])
    out = [0.0] * n
    for h in hists:
        for i, v in enumerate(h):
            out[i] += v
    inv = 1.0 / len(hists)
    return [v * inv for v in out]


def emd_proxy(buckets: dict, perfect_recall: bool = False) -> float:
    """Sum of within-bucket EMD distances, weighted by bucket population.

    For each bucket `b`, compute the mean HSD `μ_b` of its members and
    sum `EMD(member_HSD, μ_b)` for every member. Then sum across
    buckets. Lower = tighter abstraction.
    """
    pre_assign = buckets["preflop"]
    post_assign = buckets["postflop"]

    # Group HSDs by bucket id.
    pre_groups: dict = {}
    for p, bid in pre_assign.items():
        pre_groups.setdefault(bid, []).append(hsd_pre_flop(p))

    post_groups: dict = {}
    for (p, c), bid in post_assign.items():
        if perfect_recall:
            key = (pre_assign[p], bid)
        else:
            key = bid
        post_groups.setdefault(key, []).append(hsd_post_flop(p, c))

    total = 0.0
    for hists in pre_groups.values():
        center = _mean_hist(hists)
        for h in hists:
            total += emd_distance(h, center)
    for hists in post_groups.values():
        center = _mean_hist(hists)
        for h in hists:
            total += emd_distance(h, center)
    return total


if __name__ == "__main__":
    from day02_card_bucketing import build_card_buckets

    print("EMD proxy across bucket configurations on Leduc:")
    for k in (2, 3, 5, NUM_RANKS):
        kp = min(k, NUM_RANKS)
        kf = min(k, NUM_RANKS * NUM_RANKS)
        b = build_card_buckets(kp, kf)
        for recall in (True, False):
            tag = f"k={k} {'perfect' if recall else 'imperfect'}"
            print(f"  {tag:>22}: {emd_proxy(b, recall):.4f}")
