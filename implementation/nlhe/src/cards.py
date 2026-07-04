"""Card encoding, combinatorial indexing, and the 7-card rank lookup table.

Card encoding
-------------
A card is an int in ``0..51`` with ``card = rank * 4 + suit`` where
``rank in 0..12`` (2,3,...,T,J,Q,K,A -> 0..12) and ``suit in 0..3``.
This is the SAME convention used by :mod:`indexer` and the engines.

7-card rank table
-----------------
Showdown strength is precomputed for every 7-card combination and stored in a
flat ``int16`` array indexed by the colexicographic combinatorial index of the
7 sorted cards (see :func:`combo_index`). The array holds a *normalized* rank
where **LARGER = STRONGER** (opposite of phevaluator's native convention).

Table size = C(52,7) = 133,784,560 int16 values ~= 255 MiB.

Build once with :func:`build_rank_table` (uses phevaluator, C-speed) and load
with :func:`load_rank_table`. Inside numba the showdown is a single array read.
"""

from __future__ import annotations

import numpy as np
from numba import njit

NUM_CARDS = 52
NUM_RANKS = 13
NUM_SUITS = 4

# phevaluator returns 1 (best) .. 7462 (worst). We normalize to
# 0 (worst) .. 7461 (best) via NORMALIZE - rank so larger = stronger.
PHEVAL_MAX = 7462

# Precomputed binomial table BINOM[n][k] for n<=52, k<=7. Global so numba can
# close over it. C(n, k) with C(n, k) = 0 for k > n.
_BINOM = np.zeros((NUM_CARDS + 1, 8), dtype=np.int64)
for _n in range(NUM_CARDS + 1):
    _BINOM[_n, 0] = 1
    for _k in range(1, 8):
        if _k <= _n:
            _BINOM[_n, _k] = _BINOM[_n - 1, _k - 1] + _BINOM[_n - 1, _k]
BINOM = _BINOM  # exported, read-only

C52_7 = int(_BINOM[52, 7])  # 133_784_560


# ---------------------------------------------------------------------------
# Card helpers
# ---------------------------------------------------------------------------

RANK_CHARS = "23456789TJQKA"
SUIT_CHARS = "cdhs"  # clubs, diamonds, hearts, spades


def card_from_str(s: str) -> int:
    """'As' -> int. Rank char then suit char."""
    r = RANK_CHARS.index(s[0].upper())
    su = SUIT_CHARS.index(s[1].lower())
    return r * NUM_SUITS + su


def card_to_str(c: int) -> str:
    return RANK_CHARS[c // NUM_SUITS] + SUIT_CHARS[c % NUM_SUITS]


def rank_of(c: int) -> int:
    return c // NUM_SUITS


def suit_of(c: int) -> int:
    return c % NUM_SUITS


# ---------------------------------------------------------------------------
# Combinatorial (colex) index of a sorted k-card set
# ---------------------------------------------------------------------------

@njit(cache=True)
def combo_index7(c0, c1, c2, c3, c4, c5, c6, binom):
    """Colex index of 7 cards given ascending sorted values.

    Caller MUST pass c0<c1<...<c6. Uses the convention
    index = sum_i C(card_i, i+1).
    """
    return (binom[c0, 1] + binom[c1, 2] + binom[c2, 3] + binom[c3, 4]
            + binom[c4, 5] + binom[c5, 6] + binom[c6, 7])


def combo_index(cards) -> int:
    """Colex index of an arbitrary-length combination (Python-side helper)."""
    cs = sorted(int(x) for x in cards)
    idx = 0
    for i, c in enumerate(cs):
        idx += int(BINOM[c, i + 1])
    return idx


# ---------------------------------------------------------------------------
# 7-card rank table
# ---------------------------------------------------------------------------

def build_rank_table(out_path, verbose=True):
    """Enumerate all C(52,7) combos, evaluate with phevaluator, store normalized.

    Writes an int16 .npy of length C(52,7) to ``out_path``. Combos are
    enumerated via :func:`itertools.combinations` (C-speed, ascending order)
    so the write index equals the colex :func:`combo_index`.

    phevaluator's integer card convention equals ours (``rank*4+suit``, suits
    ``cdhs``), verified: 2c=0, As=51, Td=33. So we use the int fast path
    ``_evaluate_cards`` with no string construction.
    """
    import time
    from itertools import combinations
    from phevaluator.evaluator import _evaluate_cards  # int-only fast path

    # itertools yields lexicographic order but combo_index is colex; the two
    # differ, so we SCATTER-write to table[combo_index(combo)]. combo_index is
    # the combinatorial number system, a bijection onto [0, C52_7).
    # List-based binom avoids numpy scalar overhead in this 133M-iteration loop.
    b = [[int(BINOM[n, k]) for k in range(8)] for n in range(NUM_CARDS + 1)]
    table = np.full(C52_7, -1, dtype=np.int16)
    t0 = time.time()
    idx = 0
    report = 10_000_000
    for c0, c1, c2, c3, c4, c5, c6 in combinations(range(52), 7):
        ci = (b[c0][1] + b[c1][2] + b[c2][3] + b[c3][4]
              + b[c4][5] + b[c5][6] + b[c6][7])
        table[ci] = PHEVAL_MAX - _evaluate_cards(c0, c1, c2, c3, c4, c5, c6)
        idx += 1
        if verbose and idx % report == 0:
            el = time.time() - t0
            rate = idx / el
            eta = (C52_7 - idx) / rate
            print(f"  {idx:,}/{C52_7:,} ({100*idx/C52_7:4.1f}%) "
                  f"{rate/1e6:.2f}M/s eta {eta/60:.1f}m", flush=True)
    assert idx == C52_7, (idx, C52_7)
    assert table.min() >= 0, "scatter-write left gaps: combo_index not a bijection"
    np.save(out_path, table)
    if verbose:
        print(f"rank table written: {out_path} ({idx:,} entries, "
              f"{time.time()-t0:.0f}s)")
    return table


def load_rank_table(path):
    return np.load(path, mmap_mode="r")


@njit(cache=True)
def rank7(cards7, table, binom):
    """Normalized strength of a 7-card hand (unsorted int array len 7)."""
    # insertion sort of 7 elements
    a = cards7.copy()
    for i in range(1, 7):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return table[combo_index7(a[0], a[1], a[2], a[3], a[4], a[5], a[6], binom)]
