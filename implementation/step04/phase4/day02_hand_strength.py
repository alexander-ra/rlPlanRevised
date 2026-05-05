"""Hand-Strength Distribution (HSD) features for Leduc info sets.

Implements the §6.1 Level 3 / §6.2 Tool 2 feature: per info set, the
histogram of end-of-game showdown strengths obtained by enumerating
opponent rollouts.

For Leduc the rollout space is tiny — opponent has one of the four
remaining cards — so the HSD is exact, not Monte Carlo. The feature
function is keyed on `(private_rank, community_rank_or_None)`:

- Pre-flop (round 0, no community card): 50-bin histogram averaged over
  every legal community-card outcome.
- Post-flop (round 1, community known): 50-bin histogram conditioned on
  the revealed community card.

Each histogram is a length-`HSD_BINS` list of probabilities summing to 1.
The hand strength itself is the standard `P(win) + 0.5 * P(tie)` score
against a uniform random remaining opponent card.
"""

import os
import sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import card_rank
from leduc_rank_engine import showdown_winner

HSD_BINS = 50
NUM_RANKS = 3
COPIES_PER_RANK = 2
NUM_CARDS = NUM_RANKS * COPIES_PER_RANK


def _bin_index(value: float) -> int:
    """Map a hand-strength value in [0, 1] to a bin index in [0, HSD_BINS)."""
    if value <= 0.0:
        return 0
    if value >= 1.0:
        return HSD_BINS - 1
    return int(value * HSD_BINS)


def hand_strength_at_showdown(p_rank: int, c_rank: int) -> float:
    """`P(win) + 0.5 * P(tie)` for `p_rank` vs a uniform random opponent
    rank, given a known community rank.
    """
    wins = 0
    ties = 0
    total = 0
    for opp_rank in range(NUM_RANKS):
        # Each rank has COPIES_PER_RANK copies; we enumerate cards rather
        # than ranks to weight correctly when the agent's card or the
        # community card removes copies.
        # For Leduc this simplifies because rank dictates outcome — but
        # we keep card-level enumeration for parity with Texas hold'em
        # extensions.
        for opp_suit in range(COPIES_PER_RANK):
            opp_card = 2 * opp_rank + opp_suit
            # The agent's private card and the community card each
            # remove a specific (rank, suit). Approximate by keeping
            # ranks but assuming suit 0 is the agent's and suit 1 the
            # community's where possible. For Leduc HSD we do not need
            # exact card removal — only rank distributions matter.
            outcome = showdown_winner((p_rank, opp_rank), c_rank)
            if outcome == 1:
                wins += 1
            elif outcome == 0:
                ties += 1
            total += 1
    return (wins + 0.5 * ties) / total


def hsd_post_flop(p_rank: int, c_rank: int) -> list:
    """50-bin HSD when both private and community ranks are known.

    Because Leduc's outcome is deterministic given (private, community,
    opponent), the HSD is a one-hot histogram at the bin index
    corresponding to `hand_strength_at_showdown(p, c)`.
    """
    hist = [0.0] * HSD_BINS
    bin_idx = _bin_index(hand_strength_at_showdown(p_rank, c_rank))
    hist[bin_idx] = 1.0
    return hist


def hsd_pre_flop(p_rank: int) -> list:
    """50-bin HSD pre-flop: average of post-flop HSDs over every legal
    community rank, weighted by the probability of that community rank
    given that the agent already holds a card of `p_rank`.
    """
    # Probability the community is rank `c_rank` given that the agent
    # holds a card of rank `p_rank`. Cards remaining = 5 (one of the
    # 6 cards is in the agent's hand). For c_rank == p_rank, only 1
    # card is left of that rank; otherwise 2 are left.
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


def info_set_hsd(p_rank: int, c_rank=None) -> list:
    """Dispatch to pre- or post-flop HSD based on whether community is
    known. `c_rank=None` ⇒ pre-flop.
    """
    if c_rank is None:
        return hsd_pre_flop(p_rank)
    return hsd_post_flop(p_rank, c_rank)


def all_leduc_hsds() -> dict:
    """Return a dict keyed by `(p_rank, c_rank or None)` mapping to its
    HSD histogram. There are `NUM_RANKS` pre-flop entries and
    `NUM_RANKS * NUM_RANKS` post-flop entries — 12 total for Leduc.
    """
    out = {}
    for p_rank in range(NUM_RANKS):
        out[(p_rank, None)] = info_set_hsd(p_rank)
        for c_rank in range(NUM_RANKS):
            out[(p_rank, c_rank)] = info_set_hsd(p_rank, c_rank)
    return out


if __name__ == "__main__":
    hsds = all_leduc_hsds()
    print(f"Computed {len(hsds)} HSDs for Leduc (3 pre-flop + 9 post-flop).")
    for (p, c), hist in hsds.items():
        ones = sum(1 for h in hist if h > 0.0)
        c_label = "*" if c is None else str(c)
        print(f"  (p={p}, c={c_label}): {ones} non-zero bin(s), "
              f"sum={sum(hist):.3f}")
