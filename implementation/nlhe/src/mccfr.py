"""Linear external-sampling MCCFR core + the open-addressed infoset table.

Two reusable, separately-tested pieces live here:

1. **Infoset table** — an open-addressed hash table (linear probing) mapping a
   64-bit infoset hash (from actions.infoset_hash) to a slot holding regret and
   strategy-sum rows. This replaces dense (street, seq_id, bucket) indexing,
   which is infeasible at 421M infosets (see DEVIATIONS.md).

2. **CFR primitives** — `regret_matching` and the linear-CFR update, shared by
   the NLHE traversal and by the Kuhn/Leduc validation games (Gate G4). Sharing
   the exact update code is what makes the small-game convergence tests
   meaningful evidence for the big game.

The NLHE traversal itself (engine_nb + buckets + this table) is added once the
bucket artifacts are built; the primitives below are validated first.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from numba import njit, prange

MAXA = 4  # fold / call / pot-raise / all-in
ART = Path(__file__).resolve().parents[1] / "artifacts"


# ---------------------------------------------------------------------------
# CFR primitives (game-agnostic)
# ---------------------------------------------------------------------------

@njit(cache=True)
def regret_matching(regret_row, n_actions, out):
    """Regret-matching: out[0:n] = normalized positive regrets, else uniform."""
    pos_sum = 0.0
    for a in range(n_actions):
        r = regret_row[a]
        if r > 0.0:
            pos_sum += r
    if pos_sum > 0.0:
        for a in range(n_actions):
            r = regret_row[a]
            out[a] = (r / pos_sum) if r > 0.0 else 0.0
    else:
        u = 1.0 / n_actions
        for a in range(n_actions):
            out[a] = u


# ---------------------------------------------------------------------------
# Open-addressed infoset table
# ---------------------------------------------------------------------------

@njit(cache=True)
def table_find(slot_key, h):
    """Return slot index for hash h if present, else -1. Linear probing.

    slot_key is uint64 (0 = empty sentinel); h is uint64; returned slot int64."""
    capu = np.uint64(slot_key.shape[0])
    s = h % capu
    for _ in range(slot_key.shape[0]):
        k = slot_key[s]
        if k == h:
            return np.int64(s)
        if k == np.uint64(0):
            return np.int64(-1)
        s += np.uint64(1)
        if s == capu:
            s = np.uint64(0)
    return np.int64(-1)


@njit(cache=True)
def table_find_or_insert(slot_key, h):
    """Return slot for h, inserting if absent. -1 only if the table is full.

    Single-threaded-correct. NOTE: under concurrent multi-thread FIRST-insertion
    this races and creates duplicate slots (measured 85% dupes in the pilot!) —
    which is why training PRE-POPULATES the full table single-threaded via
    build_table(); after that, threads only ever hit the k == h fast path."""
    capu = np.uint64(slot_key.shape[0])
    s = h % capu
    for _ in range(slot_key.shape[0]):
        k = slot_key[s]
        if k == h:
            return np.int64(s)
        if k == np.uint64(0):
            slot_key[s] = h
            return np.int64(s)
        s += np.uint64(1)
        if s == capu:
            s = np.uint64(0)
    return np.int64(-1)


def make_table(capacity, max_actions=MAXA):
    """Allocate the infoset table arrays (slot_key uint64, 0 = empty)."""
    slot_key = np.zeros(capacity, dtype=np.uint64)
    regret = np.zeros((capacity, max_actions), dtype=np.float32)
    stratsum = np.zeros((capacity, max_actions), dtype=np.float32)
    return slot_key, regret, stratsum


# ---------------------------------------------------------------------------
# NLHE external-sampling traversal
# ---------------------------------------------------------------------------
import engine_nb as EN  # noqa: E402
from actions import infoset_hash, base_infoset_hash, mix_bucket  # noqa: E402
from indexer import canonical_key, key_to_class  # noqa: E402


@njit(cache=True)
def player_bucket(st, p, kpre, bpre, kflop, bflop, kturn, bturn,
                  kriver, briver, binom, perms):
    """Card bucket of seat p at the current street (numba, traversal hot path)."""
    cards = np.empty(7, dtype=np.int64)
    cards[0] = st[EN.O_HOLES + 2 * p]
    cards[1] = st[EN.O_HOLES + 2 * p + 1]
    street = st[EN.S_STREET]
    if street == 0:
        key = canonical_key(cards, 2, 0, binom, perms)
        return bpre[key_to_class(key, kpre)]
    elif street == 1:
        for i in range(3):
            cards[2 + i] = st[EN.O_BOARD + i]
        key = canonical_key(cards, 2, 3, binom, perms)
        return bflop[key_to_class(key, kflop)]
    elif street == 2:
        for i in range(4):
            cards[2 + i] = st[EN.O_BOARD + i]
        key = canonical_key(cards, 2, 4, binom, perms)
        return bturn[key_to_class(key, kturn)]
    else:
        for i in range(5):
            cards[2 + i] = st[EN.O_BOARD + i]
        key = canonical_key(cards, 2, 5, binom, perms)
        return briver[key_to_class(key, kriver)]


@njit(cache=True)
def _sample(strat, n, r):
    """Sample an index from strat[0:n] given uniform r in [0,1)."""
    c = 0.0
    for a in range(n):
        c += strat[a]
        if r < c:
            return a
    return n - 1


@njit(cache=True)
def traverse(st, traverser, rules, slot_key, regret, stratsum,
             kpre, bpre, kflop, bflop, kturn, bturn, kriver, briver,
             rank, binom, perms, rng, prune_below, prune_on, cfr_plus):
    """External-sampling linear-CFR traversal for one traverser. Returns the
    traverser's counterfactual value at this node. cfr_plus=1 floors regrets at
    0 after each update (C3): buried actions revive on first positive update;
    the regret-prune path never fires under flooring (regrets never go negative)."""
    if st[EN.S_FIN] == 1:
        out = np.zeros(EN.N, dtype=np.int64)
        EN.payoffs_nb(st, rank, binom, out)
        return np.float64(out[traverser])

    p = st[EN.S_TOACT]
    bucket = player_bucket(st, p, kpre, bpre, kflop, bflop, kturn, bturn,
                           kriver, briver, binom, perms)
    h = infoset_hash(st, bucket)
    slot = table_find_or_insert(slot_key, h)

    ok = np.empty(8, dtype=np.int64)
    oa = np.empty(8, dtype=np.int64)
    n = EN.legal_actions_nb(st, rules, ok, oa)
    strat = np.empty(8, dtype=np.float64)
    regret_matching(regret[slot], n, strat)

    if p == traverser:
        util = np.empty(n, dtype=np.float64)
        node = 0.0
        street = st[EN.S_STREET]
        for a in range(n):
            # regret-based pruning: skip deeply-negative actions (never on the
            # river / last street, to keep leaf values exact)
            if prune_on and street < 3 and regret[slot, a] < prune_below:
                r = np.random.random()
                if r < 0.95:
                    util[a] = 0.0
                    continue
            st2 = st.copy()
            EN.apply_action_nb(st2, rules, ok[a], oa[a])
            util[a] = traverse(st2, traverser, rules, slot_key, regret, stratsum,
                               kpre, bpre, kflop, bflop, kturn, bturn,
                               kriver, briver, rank, binom, perms, rng,
                               prune_below, prune_on, cfr_plus)
            node += strat[a] * util[a]
        for a in range(n):
            if cfr_plus == 1:
                r = regret[slot, a] + (util[a] - node)
                regret[slot, a] = r if r > 0.0 else 0.0
            else:
                regret[slot, a] += util[a] - node
        return node
    else:
        for a in range(n):
            stratsum[slot, a] += strat[a]
        a = _sample(strat, n, np.random.random())
        st2 = st.copy()
        EN.apply_action_nb(st2, rules, ok[a], oa[a])
        return traverse(st2, traverser, rules, slot_key, regret, stratsum,
                        kpre, bpre, kflop, bflop, kturn, bturn,
                        kriver, briver, rank, binom, perms, rng,
                        prune_below, prune_on, cfr_plus)


# ---------------------------------------------------------------------------
# Parallel runner + linear-CFR discounting
# ---------------------------------------------------------------------------

@njit(nogil=True, parallel=True, cache=True)
def run_batch(n_iters, start_iter, rules, slot_key, regret, stratsum,
              kpre, bpre, kflop, bflop, kturn, bturn, kriver, briver,
              rank, binom, perms, prune_below, prune_on, cfr_plus=0):
    """Run n_iters external-sampling iterations in parallel over cores.

    Each iteration deals one hand (chance sampled once) and traverses for one
    traverser. The BUTTON IS FIXED at seat 0: positions are absolute (seat i =
    a fixed position relative to the button), so a single button geometry covers
    the whole game; rotating the button would 6x the infoset space and, if tied
    to the traverser, would only ever train the button seat. The traverser
    rotates through all 6 seats so every position's regrets are updated. At
    deployment, rotate the real table so the hero's seat maps onto this geometry.
    Table writes race across threads (accepted, Pluribus-style); numba gives each
    prange worker an independent RNG."""
    for it in prange(n_iters):
        gi = start_iter + it
        traverser = gi % EN.N
        button = 0
        # Fisher-Yates deal of 17 cards (12 holes + 5 board)
        deck = np.arange(52)
        for i in range(51, 0, -1):
            j = np.random.randint(0, i + 1)
            tmp = deck[i]
            deck[i] = deck[j]
            deck[j] = tmp
        holes = deck[:12].astype(np.int32)
        board = deck[12:17].astype(np.int32)
        st = EN.new_hand_nb(rules, holes, board, button)
        traverse(st, traverser, rules, slot_key, regret, stratsum,
                 kpre, bpre, kflop, bflop, kturn, bturn, kriver, briver,
                 rank, binom, perms, 0, prune_below, prune_on, cfr_plus)


@njit(nogil=True, parallel=True, cache=True)
def discount(regret, stratsum, factor):
    """LCFR discounting: scale regrets and strategy sums by `factor`."""
    n = regret.shape[0]
    a = regret.shape[1]
    for i in prange(n):
        for j in range(a):
            regret[i, j] *= factor
            stratsum[i, j] *= factor


def enumerate_base_hashes(rules):
    """DFS the fixed (button=0) betting tree; return (base_hashes, streets).

    Card-independent, so dummy cards suffice. These are the 1.077M distinct
    public betting states; each spawns `buckets[street]` infosets."""
    import sys
    sys.setrecursionlimit(1_000_000)
    holes = np.array([0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21], dtype=np.int32)
    board = np.array([24, 25, 26, 27, 28], dtype=np.int32)
    ok = np.empty(8, dtype=np.int64)
    oa = np.empty(8, dtype=np.int64)
    seen = {}  # base_hash -> street
    st0 = EN.new_hand_nb(rules, holes, board, 0)

    def dfs(st):
        if st[EN.S_FIN] == 1:
            return
        bh = int(base_infoset_hash(st))
        if bh in seen:
            return
        seen[bh] = int(st[EN.S_STREET])
        n = EN.legal_actions_nb(st, rules, ok, oa)
        acts = [(int(ok[i]), int(oa[i])) for i in range(n)]
        for k, a in acts:
            st2 = st.copy()
            EN.apply_action_nb(st2, rules, k, a)
            dfs(st2)

    dfs(st0)
    bases = np.fromiter(seen.keys(), dtype=np.uint64, count=len(seen))
    streets = np.fromiter(seen.values(), dtype=np.int64, count=len(seen))
    return bases, streets


@njit(cache=True)
def _prepop(slot_key, bases, streets, buckets_per_street):
    """Insert every (betting state x bucket) infoset. Single-threaded -> no race.
    h is uint64 throughout, matching the traversal's infoset_hash path."""
    count = 0
    for i in range(bases.shape[0]):
        nb = buckets_per_street[streets[i]]
        base = bases[i]
        for b in range(nb):
            h = mix_bucket(base, b)
            s = table_find_or_insert(slot_key, h)
            if s >= 0:
                count += 1
    return count


def _betting_tree(rules):
    """Enumerate (or load cached) base betting-state hashes + streets."""
    cache = ART / "betting_tree_v1.npz"
    if cache.exists():
        z = np.load(cache)
        return z["bases"], z["streets"]
    bases, streets = enumerate_base_hashes(rules)
    np.savez(cache, bases=bases, streets=streets)
    return bases, streets


def build_table(rules, buckets_cfg, load_target=0.55, max_actions=MAXA,
                verbose=True):
    """Allocate an auto-sized table and PRE-POPULATE every reachable infoset
    single-threaded, so multi-threaded training never inserts (no dupe race).

    Returns (slot_key, regret, stratsum, info_dict)."""
    import time
    t0 = time.time()
    bases, streets = _betting_tree(rules)
    bps = np.array([buckets_cfg["preflop"], buckets_cfg["flop"],
                    buckets_cfg["turn"], buckets_cfg["river"]], dtype=np.int64)
    counts = np.bincount(streets, minlength=4)
    n_infosets = int((counts * bps).sum())
    capacity = int(n_infosets / load_target)
    slot_key, regret, stratsum = make_table(capacity, max_actions)
    inserted = _prepop(slot_key, bases, streets, bps)
    used = int((slot_key != 0).sum())
    # used < n_infosets only via 64-bit hash collisions (expect ~0)
    assert n_infosets - used < 100, (n_infosets, used)
    info = {"betting_states": int(len(bases)), "infosets": n_infosets,
            "capacity": capacity, "used_slots": used,
            "table_gb": round(capacity * (8 + 8 * max_actions) / 1e9, 1),
            "prepop_seconds": round(time.time() - t0, 1)}
    if verbose:
        print(f"table prepopulated: {used:,} infosets in {capacity:,} slots "
              f"({info['table_gb']} GB, load {used/capacity:.2f}) "
              f"[{info['prepop_seconds']}s]", flush=True)
    return slot_key, regret, stratsum, info


def load_artifacts(buckets_cfg=None):
    """Load bucket keys/assignments, rank table, binom, suit perms for training.

    Bucket files are suffixed by size (bucket_flop_100.npy etc.) so several
    abstraction sizes can coexist; falls back to the unsuffixed name."""
    import indexer
    from cards import BINOM

    def bfile(street, n):
        p = ART / f"bucket_{street}_{n}.npy"
        return p if p.exists() else ART / f"bucket_{street}.npy"

    if buckets_cfg is None:
        import json
        buckets_cfg = json.loads(
            (ART.parent / "config" / "default.json").read_text())["buckets"]
    A = {}
    A["kpre"] = np.load(ART / "keys_preflop.npy")
    A["bpre"] = np.load(ART / "bucket_preflop.npy")
    A["kflop"] = np.load(ART / "keys_flop.npy")
    A["bflop"] = np.load(bfile("flop", buckets_cfg["flop"]))
    A["kturn"] = np.load(ART / "keys_turn.npy")
    A["bturn"] = np.load(bfile("turn", buckets_cfg["turn"]))
    A["kriver"] = np.load(ART / "keys_river.npy")
    A["briver"] = np.load(bfile("river", buckets_cfg["river"]))
    for s in ("flop", "turn", "river"):
        assert int(A["b" + s].max()) < buckets_cfg[s], \
            f"bucket_{s} file does not match configured size {buckets_cfg[s]}"
    A["rank"] = np.load(ART / "rank7.npy")
    A["binom"] = BINOM.astype(np.int64)
    A["perms"] = indexer.SUIT_PERMS
    return A
