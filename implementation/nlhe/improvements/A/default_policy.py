"""PROPOSAL A1 + A2 — sensible policy for untrained / thin infosets.

NOT wired in. To use: copy this file into ../../src/ (so `import engine_nb`
etc. resolve the same way as the other src modules), then apply the wiring
snippets in ./README.md to evalmatch.py and distill.py.

Why: at 5B iters ~87% of postflop infosets are never visited, so the current
uniform fallback makes the blueprint play RANDOM postflop — exactly the cold
start a self-play seed must avoid. These two functions replace "uniform" with:

  A1 heuristic_default : pot-odds / bucket-equity rule (always available).
  A2 nearest_bucket    : borrow the strategy of the closest *visited* bucket
                         (same public state) by mean-equity distance.

Both are OUTPUT-side only (eval + distill targets). They never touch regrets or
the CFR math, so there is no convergence/correctness risk to training.
"""
from __future__ import annotations

import numpy as np
from numba import njit

import engine_nb as EN
from actions import base_infoset_hash, mix_bucket
from mccfr import table_find

# action kind codes (match engine_nb.legal_actions_nb output)
_FOLD, _CALL, _RAISE = 0, 1, 2


@njit(cache=True)
def _action_slots(ok, n):
    """Locate abstract-action indices by kind. Returns
    (fold_idx, call_idx, first_raise_idx, last_raise_idx); -1 if absent.
    first_raise = smallest raise (pot), last_raise = all-in (largest)."""
    fold_i = -1
    call_i = -1
    raise_lo = -1
    raise_hi = -1
    for a in range(n):
        k = ok[a]
        if k == _FOLD:
            fold_i = a
        elif k == _CALL:
            call_i = a
        else:  # raise-kind (pot / all-in share kind 2)
            if raise_lo == -1:
                raise_lo = a
            raise_hi = a
    return fold_i, call_i, raise_lo, raise_hi


@njit(cache=True)
def heuristic_default(st, p, n, ok, eq, out):
    """A1: fill out[0:n] with a pot-odds / equity heuristic policy.

    `eq` = acting seat's per-bucket mean equity in [0,1] (same array eval/distill
    already build). Deterministic-ish mixes, not a solve — just "not dumb"."""
    for a in range(n):
        out[a] = 0.0
    pot = 0.0
    for i in range(EN.N):
        pot += st[EN.O_COMMIT + i]
    call_amt = st[EN.S_CBET] - st[EN.O_SBET + p]
    if call_amt < 0.0:
        call_amt = 0.0
    fold_i, call_i, r_lo, r_hi = _action_slots(ok, n)
    facing = call_amt > 0.0
    req = call_amt / (pot + call_amt) if (pot + call_amt) > 0.0 else 0.0

    if not facing:
        # can check (call_i is a free check here)
        if eq > 0.66 and r_lo >= 0:
            out[r_lo] = 0.7
            if call_i >= 0:
                out[call_i] = 0.3
        elif eq > 0.5 and r_lo >= 0:
            out[r_lo] = 0.25
            if call_i >= 0:
                out[call_i] = 0.75
        else:
            if call_i >= 0:
                out[call_i] = 1.0
            elif r_lo >= 0:
                out[r_lo] = 1.0
    else:
        strong = req + 0.20
        if eq >= strong and r_lo >= 0:      # clear value raise
            out[r_lo] = 0.6
            if call_i >= 0:
                out[call_i] = 0.4
        elif eq >= req:                     # profitable call
            if call_i >= 0:
                out[call_i] = 0.85
            if r_lo >= 0:
                out[r_lo] = 0.15
        elif eq >= req - 0.08 and call_i >= 0:  # marginal: mostly fold
            out[call_i] = 0.35
            if fold_i >= 0:
                out[fold_i] = 0.65
        else:                               # weak facing a bet -> fold
            if fold_i >= 0:
                out[fold_i] = 1.0
            elif call_i >= 0:
                out[call_i] = 1.0

    tot = 0.0
    for a in range(n):
        tot += out[a]
    if tot <= 0.0:
        u = 1.0 / n
        for a in range(n):
            out[a] = u
    else:
        for a in range(n):
            out[a] /= tot


@njit(cache=True)
def nearest_bucket_strategy(st, n_buckets, my_eq, eq_street,
                            slot_key, stratsum, n, out):
    """A2: copy the average strategy of the closest *visited* bucket at THIS
    public state (bucket-independent base hash), ranked by |eq - my_eq|.

    Returns True if a visited neighbour was found (out filled), else False so the
    caller can fall back to heuristic_default. O(n_buckets) table probes — fine
    for eval/distill, do NOT call in the training hot loop."""
    base = base_infoset_hash(st)
    best_d = 1.0e18
    best_slot = -1
    for b in range(n_buckets):
        h = mix_bucket(base, b)
        slot = table_find(slot_key, h)
        if slot < 0:
            continue
        s = 0.0
        for a in range(n):
            v = stratsum[slot, a]
            if v > 0.0:
                s += v
        if s <= 0.0:
            continue
        d = eq_street[b] - my_eq
        if d < 0.0:
            d = -d
        if d < best_d:
            best_d = d
            best_slot = slot
    if best_slot < 0:
        return False
    tot = 0.0
    for a in range(n):
        v = stratsum[best_slot, a]
        out[a] = v if v > 0.0 else 0.0
        tot += out[a]
    if tot <= 0.0:
        return False
    for a in range(n):
        out[a] /= tot
    return True
