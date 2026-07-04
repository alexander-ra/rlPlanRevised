"""Suit-isomorphism canonical hand keys for card abstraction.

Two (hole, board) situations are *isomorphic* if one becomes the other by
permuting the four suits. Equity, and therefore the correct bucket, is
identical across an isomorphism class, so we collapse each class to one
canonical key.

Design
------
`canonical_key(cards, nhole, k)` returns an ``int64`` that is IDENTICAL for all
isomorphic hands and DISTINCT for non-isomorphic ones. It is the minimum, over
all 24 suit permutations, of a positional encoding of the (suit-relabelled,
re-sorted) hole and board. Being pure integer arithmetic over fixed-size local
arrays, it runs inside ``njit(nogil=True)`` MCCFR traversal threads.

The set of DISTINCT canonical keys for a street equals the number of canonical
classes. Gate G3 asserts these equal the known values:

    preflop (2)         169
    flop    (2+3)       1,286,792
    turn    (2+4)       13,960,050
    river   (2+5)       123,156,254

Artifacts (built by :func:`build_and_save`): ``keys_<street>.npy`` — the sorted
unique canonical keys for that street. Bucketing (`buckets.py`) later attaches a
parallel ``bucket_<street>.npy``. At runtime,
``bucket = buckets[searchsorted(keys, canonical_key(...))]``.
"""
from __future__ import annotations

import numpy as np
from numba import njit, prange

from cards import BINOM, NUM_CARDS

# Known canonical class counts (Gate G3).
CLASS_COUNTS = {"preflop": 169, "flop": 1_286_792,
                "turn": 13_960_050, "river": 123_156_254}
STREET_BOARD_K = {"preflop": 0, "flop": 3, "turn": 4, "river": 5}

# All 24 permutations of the 4 suits, as an int8 (24,4) array.
def _all_suit_perms():
    from itertools import permutations
    return np.array(list(permutations(range(4))), dtype=np.int8)
SUIT_PERMS = _all_suit_perms()

# Hole-pair table: index 0..1325 -> (h0,h1) with h0<h1.
def _hole_pairs():
    pairs = [(a, b) for a in range(NUM_CARDS) for b in range(a + 1, NUM_CARDS)]
    return np.array(pairs, dtype=np.int64)
HOLE_PAIRS = _hole_pairs()  # (1326, 2)

BINOM64 = BINOM.astype(np.int64)


@njit(cache=True, inline="always")
def _sort_small(a, n):
    """In-place insertion sort of the first n entries of a."""
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


@njit(cache=True)
def canonical_key(cards, nhole, k, binom, perms):
    """Canonical int64 key for hole(nhole) + board(k). cards len = nhole+k.

    nhole is 2 in this project; kept as a parameter for clarity/reuse.
    """
    best = np.int64(1) << 62
    hole = np.empty(2, dtype=np.int64)
    board = np.empty(5, dtype=np.int64)
    for p in range(perms.shape[0]):
        # relabel suits
        for i in range(nhole):
            c = cards[i]
            hole[i] = (c // 4) * 4 + perms[p, c % 4]
        for i in range(k):
            c = cards[nhole + i]
            board[i] = (c // 4) * 4 + perms[p, c % 4]
        _sort_small(hole, nhole)
        _sort_small(board, k)
        # positional encode: colex(board) * 2704 + hole0*52 + hole1
        colex = np.int64(0)
        for j in range(k):
            colex += binom[board[j], j + 1]
        key = colex * 2704 + hole[0] * 52 + hole[1]
        if key < best:
            best = key
    return best


@njit(cache=True)
def decode_key(key, k, binom, out):
    """Inverse of the encoding in canonical_key: fill out[0:2]=hole (sorted),
    out[2:2+k]=board (sorted). Returns nothing; out must be length >= 2+k.

    Encoding was: colex(board)*2704 + hole0*52 + hole1  (hole0<hole1).
    Board colex decoded via the combinatorial number system (greedy from the
    top position down).
    """
    hole_part = key % 2704
    out[0] = hole_part // 52
    out[1] = hole_part % 52
    colex = key // 2704
    # greedy decode k board cards: for position j=k..1, find largest c with
    # binom[c, j] <= remaining.
    rem = colex
    for j in range(k, 0, -1):
        c = j - 1
        while binom[c + 1, j] <= rem:
            c += 1
        out[2 + (j - 1)] = c
        rem -= binom[c, j]


@njit(cache=True)
def key_to_class(key, sorted_keys):
    """Dense class id via binary search; -1 if absent (should not happen)."""
    lo = 0
    hi = sorted_keys.shape[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if sorted_keys[mid] < key:
            lo = mid + 1
        else:
            hi = mid
    if lo < sorted_keys.shape[0] and sorted_keys[lo] == key:
        return lo
    return -1


@njit(parallel=True, cache=True)
def _enumerate_street(k, C50k, hole_pairs, binom, perms):
    """All canonical keys for a street, one contiguous block per hole pair.

    Returns an int64 array of length 1326*C50k (with duplicates; caller uniques).
    """
    n_hp = hole_pairs.shape[0]
    out = np.empty(n_hp * C50k, dtype=np.int64)
    for hp in prange(n_hp):
        h0 = hole_pairs[hp, 0]
        h1 = hole_pairs[hp, 1]
        avail = np.empty(50, dtype=np.int64)
        t = 0
        for c in range(52):
            if c != h0 and c != h1:
                avail[t] = c
                t += 1
        cards = np.empty(2 + 5, dtype=np.int64)
        cards[0] = h0
        cards[1] = h1
        idx = np.empty(5, dtype=np.int64)
        for j in range(k):
            idx[j] = j
        base = hp * C50k
        cnt = 0
        while True:
            for j in range(k):
                cards[2 + j] = avail[idx[j]]
            out[base + cnt] = canonical_key(cards, 2, k, binom, perms)
            cnt += 1
            i = k - 1
            while i >= 0 and idx[i] == 50 - k + i:
                i -= 1
            if i < 0:
                break
            idx[i] += 1
            for j in range(i + 1, k):
                idx[j] = idx[j - 1] + 1
    return out


def enumerate_unique_keys(street, verbose=True):
    """Return sorted unique canonical keys for a street (validates count)."""
    k = STREET_BOARD_K[street]
    if k == 0:
        # preflop: just the 1326 hole pairs canonicalized
        keys = np.empty(HOLE_PAIRS.shape[0], dtype=np.int64)
        cards = np.empty(2, dtype=np.int64)
        for hp in range(HOLE_PAIRS.shape[0]):
            cards[0] = HOLE_PAIRS[hp, 0]
            cards[1] = HOLE_PAIRS[hp, 1]
            keys[hp] = canonical_key(cards, 2, 0, BINOM64, SUIT_PERMS)
        uniq = np.unique(keys)
    else:
        C50k = int(BINOM[50, k])
        if verbose:
            total = HOLE_PAIRS.shape[0] * C50k
            print(f"  enumerating {street}: {total:,} raw keys "
                  f"({total*8/1e9:.1f} GB) ...", flush=True)
        raw = _enumerate_street(k, C50k, HOLE_PAIRS, BINOM64, SUIT_PERMS)
        uniq = np.unique(raw)
        del raw
    if verbose:
        exp = CLASS_COUNTS[street]
        ok = "OK" if len(uniq) == exp else f"MISMATCH (expected {exp:,})"
        print(f"  {street}: {len(uniq):,} classes  {ok}", flush=True)
    return uniq


@njit(parallel=True, cache=True)
def _enumerate_hole_group(k, hp_lo, hp_hi, C50k, hole_pairs, binom, perms):
    """Canonical keys for hole pairs [hp_lo, hp_hi); block of (hp_hi-hp_lo)*C50k."""
    n = hp_hi - hp_lo
    out = np.empty(n * C50k, dtype=np.int64)
    for g in prange(n):
        hp = hp_lo + g
        h0 = hole_pairs[hp, 0]
        h1 = hole_pairs[hp, 1]
        avail = np.empty(50, dtype=np.int64)
        t = 0
        for c in range(52):
            if c != h0 and c != h1:
                avail[t] = c
                t += 1
        cards = np.empty(2 + 5, dtype=np.int64)
        cards[0] = h0
        cards[1] = h1
        idx = np.empty(5, dtype=np.int64)
        for j in range(k):
            idx[j] = j
        base = g * C50k
        cnt = 0
        while True:
            for j in range(k):
                cards[2 + j] = avail[idx[j]]
            out[base + cnt] = canonical_key(cards, 2, k, binom, perms)
            cnt += 1
            i = k - 1
            while i >= 0 and idx[i] == 50 - k + i:
                i -= 1
            if i < 0:
                break
            idx[i] += 1
            for j in range(i + 1, k):
                idx[j] = idx[j - 1] + 1
    return out


def build_river_keys(out_path, hole_pairs_per_chunk=64, verbose=True):
    """Memory-safe river build: unique within chunks of hole pairs, merge.

    Peak memory ~= (chunk * C(50,5) * 8) for the raw block plus the running
    merged unique set. With chunk=64 the raw block is ~1.1 GB; the merged
    unique set grows toward 123M keys (~1 GB). Fits comfortably in 62 GB.
    """
    import time
    k = 5
    C50k = int(BINOM[50, k])
    n_hp = HOLE_PAIRS.shape[0]
    merged = None
    t0 = time.time()
    for lo in range(0, n_hp, hole_pairs_per_chunk):
        hi = min(lo + hole_pairs_per_chunk, n_hp)
        raw = _enumerate_hole_group(k, lo, hi, C50k, HOLE_PAIRS, BINOM64, SUIT_PERMS)
        u = np.unique(raw)
        del raw
        if merged is None:
            merged = u
        else:
            merged = np.unique(np.concatenate([merged, u]))
        del u
        if verbose:
            el = time.time() - t0
            frac = hi / n_hp
            print(f"  river {hi}/{n_hp} hole pairs  uniq={len(merged):,}  "
                  f"{el:.0f}s  eta {el/frac - el:.0f}s", flush=True)
    assert len(merged) == CLASS_COUNTS["river"], (len(merged), CLASS_COUNTS["river"])
    np.save(out_path, merged)
    if verbose:
        print(f"saved river keys ({len(merged):,})")
    return merged


def build_and_save(art_dir, streets=("preflop", "flop", "turn"), force=False):
    """Build and save keys_<street>.npy for the given streets.

    River is excluded by default (2.8B raw keys, multi-hour, ~22 GB peak).
    Add it explicitly: build_and_save(art, streets=("river",)).
    """
    from pathlib import Path
    art_dir = Path(art_dir)
    art_dir.mkdir(exist_ok=True)
    for street in streets:
        out = art_dir / f"keys_{street}.npy"
        if out.exists() and not force:
            print(f"{out.name} exists; skip (use force=True)")
            continue
        uniq = enumerate_unique_keys(street)
        assert len(uniq) == CLASS_COUNTS[street], (
            street, len(uniq), CLASS_COUNTS[street])
        np.save(out, uniq)
        print(f"saved {out.name} ({len(uniq):,} keys)")
