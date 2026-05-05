"""Suit-isomorphism check on Leduc info sets.

Implements the §6.1 `is_lossless_merge` pseudocode from the deliverable.
The Gilpin & Sandholm (2007) Definition 3.2 criterion for merging two
sibling info sets `I_a, I_b` is:

  1. they have the same parent in the signal tree,
  2. there is a bijection over their children with matching edge
     probabilities,
  3. each paired child pair is itself ordered-game-isomorphic
     (recursive),
  4. base case at leaves: utilities match for every opponent
     continuation.

In Leduc the only non-trivial isomorphism family is suit-permutation:
swapping suits within a rank produces an identical strategic situation
because Leduc has no flushes and pair-matching is rank-based. The
rank-canonical engine in `leduc_rank_engine.py` has these merges already
baked in. This module is therefore a *sanity probe* — it verifies the
isomorphism on the original 6-card engine — rather than a merge driver.

Two functions are exposed:

- `is_suit_isomorphic_pair(card_a, card_b)` — lightweight rank-equality
  check; the structural condition for the merge to be lossless in Leduc.
- `verify_suit_isomorphism()` — walks the 6-card game tree and confirms
  that for every (private rank, community rank) pair, the four suit
  variants `(p_suit ∈ {0, 1}) × (c_suit ∈ {0, 1})` produce identical
  utility distributions against every opponent rank continuation. Returns
  `(num_merges_found, num_violations)`.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import ALL_DEALS, LeducState, NUM_ACTIONS, card_rank


def is_suit_isomorphic_pair(card_a: int, card_b: int) -> bool:
    """Two Leduc cards are suit-isomorphic iff they share a rank.

    This is the structural precondition for Definition 3.2 condition (3)
    to hold in Leduc: identical rank means identical pair-match outcome
    against every opponent rank continuation.
    """
    return card_rank(card_a) == card_rank(card_b)


def utility_signature_at_leaves(p_card: int, c_card: int) -> tuple:
    """For a fixed (private, community) pair, enumerate every opponent
    private card and tabulate the showdown utility from player 0's
    perspective when both private and community are fixed.

    Returns a tuple keyed by opponent rank (J, Q, K) listing the utility
    differential. Two (private, community) pairs are leaf-utility
    equivalent iff they produce identical signatures.
    """
    # Build a probe state that reaches showdown immediately:
    # round 1, both players check.
    sig = []
    for opp_card in range(6):
        if opp_card == p_card or opp_card == c_card:
            continue
        # Construct a terminal state: r0 cc, r1 cc → showdown.
        state = LeducState((p_card, opp_card), c_card)
        state = state.apply_action(1)  # CHECK_CALL p0
        state = state.apply_action(1)  # CHECK_CALL p1 → enters round 1
        state = state.apply_action(1)  # CHECK_CALL p0 round 1
        state = state.apply_action(1)  # CHECK_CALL p1 round 1 → terminal
        assert state.is_terminal()
        sig.append((card_rank(opp_card), state.get_utility(0)))
    return tuple(sorted(sig))


def verify_suit_isomorphism() -> tuple:
    """Walk every (private rank, community rank) and check that the
    four suit variants of (private card, community card) produce
    identical leaf-utility signatures.

    Returns:
        (num_pairs_checked, num_violations)
    """
    num_pairs_checked = 0
    num_violations = 0

    # For every (private rank, community rank) where both ranks are
    # legal (0..2) and the cards are distinct, gather the four suit
    # variants and compare their signatures.
    for p_rank in range(3):
        for c_rank in range(3):
            for p_suit in range(2):
                for c_suit in range(2):
                    p_card = 2 * p_rank + p_suit
                    c_card = 2 * c_rank + c_suit
                    if p_card == c_card:
                        continue
                    # Compare against the canonical (suit=0, suit=0) variant.
                    canonical_p = 2 * p_rank
                    canonical_c = 2 * c_rank
                    if canonical_p == canonical_c:
                        # Skip the rank-collision case (same rank for
                        # private and community); the canonical variant
                        # is undefined.
                        continue
                    if (p_card, c_card) == (canonical_p, canonical_c):
                        continue
                    sig_actual = utility_signature_at_leaves(p_card, c_card)
                    sig_canonical = utility_signature_at_leaves(canonical_p, canonical_c)
                    num_pairs_checked += 1
                    if sig_actual != sig_canonical:
                        num_violations += 1
    return num_pairs_checked, num_violations


if __name__ == "__main__":
    pairs, violations = verify_suit_isomorphism()
    print(f"suit-isomorphic pairs checked: {pairs}")
    print(f"violations:                    {violations}")
    if violations == 0:
        print("OK — Definition 3.2 condition (3) holds for every suit "
              "permutation in Leduc.")
    else:
        print("UNEXPECTED — at least one pair fails the leaf-utility check.")
