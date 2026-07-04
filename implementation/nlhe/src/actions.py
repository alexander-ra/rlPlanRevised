"""Action abstraction helpers: infoset hashing, off-tree bet translation, and
the G6 sizing report.

Abstraction (see config/default.json, DEVIATIONS.md):
  actions = fold / check-call / pot-raise / all-in, max 2 raises per street.

Infoset identity
----------------
Dense (street, seq_id, bucket) indexing is infeasible at this scale (millions
of public betting states; see the G6 sizing report). Instead every infoset is a
64-bit FNV-1a hash of the public betting state plus the acting player's card
bucket, stored in an open-addressed table (see mccfr.py). With ~4.6e8 live keys
in a 2^64 space the expected number of 64-bit collisions is ~0.01, so the hash
serves as the infoset identity.
"""
from __future__ import annotations

import numpy as np
from numba import njit, uint64

import engine_nb as EN

# action kind codes (match engine_nb.legal_actions_nb output)
FOLD = 0
CALL = 1
RAISE = 2

_FNV_OFFSET = uint64(1469598103934665603)
_FNV_PRIME = uint64(1099511628211)


@njit(cache=True, inline="always")
def _mix(h, x):
    return (h ^ uint64(x & 0xFFFFFFFFFFFFFFFF)) * _FNV_PRIME


@njit(cache=True)
def base_infoset_hash(st):
    """FNV hash of the public betting state only (no bucket, no 0-guard).

    Public fields that define the betting state: street, to_act, current_bet,
    min_raise, raises_this_street, and per-seat committed / folded / allin /
    street_bet. Split out so pre-population can derive every bucket variant of a
    state cheaply (see mccfr.prepopulate_table)."""
    h = _FNV_OFFSET
    h = _mix(h, st[EN.S_STREET])
    h = _mix(h, st[EN.S_TOACT])
    h = _mix(h, st[EN.S_CBET])
    h = _mix(h, st[EN.S_MINR])
    h = _mix(h, st[EN.S_RAISES])
    for p in range(EN.N):
        h = _mix(h, st[EN.O_COMMIT + p])
        h = _mix(h, st[EN.O_FOLD + p] * 4 + st[EN.O_ALLIN + p] * 2)
        h = _mix(h, st[EN.O_SBET + p])
    return h


@njit(cache=True)
def mix_bucket(base_h, bucket):
    """Fold the acting player's card bucket into a base betting-state hash."""
    h = _mix(base_h, bucket + 1)
    if h == uint64(0):  # avoid the sentinel 0 (empty-slot marker)
        h = uint64(1)
    return h


@njit(cache=True)
def infoset_hash(st, bucket):
    """64-bit infoset id = base betting-state hash folded with the card bucket."""
    return mix_bucket(base_infoset_hash(st), bucket)


def pseudo_harmonic(x, A, B):
    """Ganzfried & Sandholm (2013) pseudo-harmonic mapping.

    An off-tree bet of (pot-normalized) size x, lying between abstraction sizes
    A < B, is mapped to the SMALLER size A with this probability (else B). All
    three sizes are fractions of the pot.
    """
    if x <= A:
        return 1.0
    if x >= B:
        return 0.0
    return ((B - x) * (1.0 + A)) / ((B - A) * (1.0 + x))


# ---------------------------------------------------------------------------
# G6 sizing report (diagnostic; reuses the readable reference engine)
# ---------------------------------------------------------------------------

def enumerate_state_counts(rules, board=None, verbose=False):
    """Distinct public betting states per street under `rules`.

    Betting states are card-independent, so a single fixed board suffices.
    Returns {street: count}. O(20-30s) in pure Python — a one-time diagnostic.
    """
    import sys
    import engine_ref as ER
    sys.setrecursionlimit(1_000_000)
    if board is None:
        board = [24, 25, 26, 27, 28]
    holes = [[4 * i, 4 * i + 1] for i in range(rules.num_players)]

    def key(s):
        return (s.street, s.to_act, s.current_bet, s.min_raise,
                s.raises_this_street, tuple(s.committed), tuple(s.folded),
                tuple(s.allin), tuple(s.street_bet))

    per = {0: set(), 1: set(), 2: set(), 3: set()}
    seen = set()

    def dfs(s):
        if ER.is_terminal(s):
            return
        k = key(s)
        if k in seen:
            return
        seen.add(k)
        per[s.street].add(k)
        for kind, a in zip(*ER.legal_actions(s)):
            s2 = s.clone()
            ER.apply_action(s2, kind, a)
            dfs(s2)

    dfs(ER.new_hand(rules, holes, board, 0))
    return {st: len(per[st]) for st in per}


def sizing_report(rules, buckets, table_cfg):
    """G6: infoset total and hash-table memory. Returns a dict; prints a table."""
    counts = enumerate_state_counts(rules)
    infosets = (counts[0] * buckets["preflop"]
                + counts[1] * buckets["flop"]
                + counts[2] * buckets["turn"]
                + counts[3] * buckets["river"])
    max_a = table_cfg["max_actions"]
    bytes_per_slot = 8 + max_a * 4 + max_a * 4  # key + regret + strat (float32)
    load = table_cfg["load_factor_target"]
    needed_slots = infosets / load
    cap = table_cfg["capacity"]
    table_gb = cap * bytes_per_slot / 1e9
    live_gb = infosets * bytes_per_slot / 1e9
    report = {
        "states_per_street": counts,
        "infosets": int(infosets),
        "bytes_per_slot": bytes_per_slot,
        "capacity": cap,
        "needed_slots_at_load": int(needed_slots),
        "table_gb_at_capacity": table_gb,
        "live_gb": live_gb,
        "fits_capacity": needed_slots <= cap,
        "load_at_capacity": infosets / cap,
    }
    print("G6 sizing report")
    print(f"  betting states/street : {counts}")
    print(f"  infosets              : {infosets:,}")
    print(f"  bytes/slot            : {bytes_per_slot} (max_actions={max_a})")
    print(f"  hash-table capacity   : {cap:,} slots -> {table_gb:.1f} GB")
    print(f"  load factor at cap    : {infosets / cap:.2f}")
    print(f"  fits (<= {load} load)   : {report['fits_capacity']}")
    return report


if __name__ == "__main__":
    import json
    from pathlib import Path
    import engine_ref as ER
    cfg = json.loads((Path(__file__).resolve().parents[1]
                      / "config" / "default.json").read_text())
    a = cfg["abstraction"]
    rules = ER.Rules(
        num_players=cfg["game"]["num_players"],
        starting_stack=cfg["game"]["starting_stack"],
        small_blind=cfg["game"]["small_blind"],
        big_blind=cfg["game"]["big_blind"],
        ante=cfg["game"]["ante"],
        raise_fractions=tuple(a["raise_fractions"]),
        include_allin=a["include_allin"],
        use_preflop_open=a["use_preflop_open"],
        preflop_open_bb=a["preflop_open_bb"],
        max_raises_per_street=a["max_raises_per_street"],
    )
    sizing_report(rules, cfg["buckets"], cfg["infoset_table"])
