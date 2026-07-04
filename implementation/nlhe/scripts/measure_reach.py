"""Measurement for the sampling redesign (read-only; safe alongside training).

1) Flop-reach study: play N hands where EVERY seat samples from the current
   regret-matched strategy (exactly how opponents behave inside training
   iterations). Reports: % of hands ending per street, and where the sampled-
   path decision points fall (how much sampled work is preflop).

2) Coverage scan: for every one of the 214M infosets (base betting state x
   bucket), check whether its regret row / stratsum row has been touched, and
   how big the stratsum mass is. Per-street totals.

Usage: python measure_reach.py <run_dir>
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
ART = HERE.parent / "artifacts"
sys.path.insert(0, str(SRC))

import numba  # noqa: E402
from numba import njit, prange  # noqa: E402

numba.set_num_threads(6)  # modest: don't starve the live training run

import engine_ref as ER  # noqa: E402
import engine_nb as EN  # noqa: E402
import mccfr  # noqa: E402
from actions import infoset_hash, mix_bucket  # noqa: E402


@njit(cache=True)
def _playout(rules, sk, regret, kpre, bpre, kflop, bflop, kturn, bturn,
             kriver, briver, binom, perms, end_street, dec_street, seen_flop):
    """One full hand, all seats sampling regret-matched current strategy."""
    deck = np.arange(52)
    for i in range(51, 0, -1):
        j = np.random.randint(0, i + 1)
        t = deck[i]
        deck[i] = deck[j]
        deck[j] = t
    holes = deck[:12].astype(np.int32)
    board = deck[12:17].astype(np.int32)
    st = EN.new_hand_nb(rules, holes, board, 0)
    ok = np.empty(8, dtype=np.int64)
    oa = np.empty(8, dtype=np.int64)
    strat = np.empty(8, dtype=np.float64)
    got_flop = 0
    while st[EN.S_FIN] == 0:
        p = st[EN.S_TOACT]
        s = st[EN.S_STREET]
        if s >= 1:
            got_flop = 1
        dec_street[s] += 1
        bucket = mccfr.player_bucket(st, p, kpre, bpre, kflop, bflop,
                                     kturn, bturn, kriver, briver, binom, perms)
        h = infoset_hash(st, bucket)
        slot = mccfr.table_find(sk, h)
        n = EN.legal_actions_nb(st, rules, ok, oa)
        if slot >= 0:
            mccfr.regret_matching(regret[slot], n, strat)
        else:
            for a in range(n):
                strat[a] = 1.0 / n
        r = np.random.random()
        c = 0.0
        a_pick = n - 1
        for a in range(n):
            c += strat[a]
            if r < c:
                a_pick = a
                break
        EN.apply_action_nb(st, rules, ok[a_pick], oa[a_pick])
    end_street[st[EN.S_STREET]] += 1
    seen_flop[0] += got_flop


@njit(cache=True)
def playout_study(n_hands, rules, sk, regret, kpre, bpre, kflop, bflop,
                  kturn, bturn, kriver, briver, binom, perms):
    end_street = np.zeros(4, dtype=np.int64)
    dec_street = np.zeros(4, dtype=np.int64)
    seen_flop = np.zeros(1, dtype=np.int64)
    for _ in range(n_hands):
        _playout(rules, sk, regret, kpre, bpre, kflop, bflop, kturn, bturn,
                 kriver, briver, binom, perms, end_street, dec_street, seen_flop)
    return end_street, dec_street, seen_flop[0]


@njit(parallel=True, cache=True)
def coverage_scan(bases, streets, bps, sk, regret, stratsum, n_chunks):
    """Per-chunk per-street counters:
    [total, regret_nz, strat_nz, strat>1, strat>10, strat>100, strat_sum]"""
    out = np.zeros((n_chunks, 4, 7), dtype=np.float64)
    nb_ = bases.shape[0]
    chunk = (nb_ + n_chunks - 1) // n_chunks
    for c in prange(n_chunks):
        lo = c * chunk
        hi = min(lo + chunk, nb_)
        for i in range(lo, hi):
            s = streets[i]
            base = bases[i]
            nbk = bps[s]
            for b in range(nbk):
                h = mix_bucket(base, b)
                slot = mccfr.table_find(sk, h)
                out[c, s, 0] += 1
                if slot < 0:
                    continue
                rnz = False
                for a in range(4):
                    if regret[slot, a] != 0.0:
                        rnz = True
                        break
                if rnz:
                    out[c, s, 1] += 1
                ssum = 0.0
                for a in range(4):
                    ssum += stratsum[slot, a]
                if ssum > 0.0:
                    out[c, s, 2] += 1
                if ssum > 1.0:
                    out[c, s, 3] += 1
                if ssum > 10.0:
                    out[c, s, 4] += 1
                if ssum > 100.0:
                    out[c, s, 5] += 1
                out[c, s, 6] += ssum
    return out


def main(run_dir):
    import checkpoint as CK
    t0 = time.time()
    ck, it = CK.latest_checkpoint(run_dir)
    print(f"checkpoint: iter {it:,}")
    sk = np.load(Path(ck) / "slot_key.npy")
    regret = np.load(Path(ck) / "regret.npy")
    stratsum = np.load(Path(ck) / "stratsum.npy")
    print(f"loaded table ({time.time()-t0:.0f}s)")

    cfg = json.loads((HERE.parent / "config" / "default.json").read_text())
    a = cfg["abstraction"]
    rules = ER.Rules(
        num_players=cfg["game"]["num_players"],
        starting_stack=cfg["game"]["starting_stack"],
        small_blind=cfg["game"]["small_blind"], big_blind=cfg["game"]["big_blind"],
        ante=cfg["game"]["ante"], raise_fractions=tuple(a["raise_fractions"]),
        include_allin=a["include_allin"], use_preflop_open=a["use_preflop_open"],
        preflop_open_bb=a["preflop_open_bb"],
        max_raises_per_street=a["max_raises_per_street"])
    rules_arr = EN.pack_rules(rules)
    A = mccfr.load_artifacts(cfg["buckets"])

    print("\n=== 1) PLAYOUT STUDY (200k hands, all seats = current strategy) ===")
    t = time.time()
    end_street, dec_street, saw_flop = playout_study(
        200_000, rules_arr, sk, regret,
        A["kpre"], A["bpre"], A["kflop"], A["bflop"], A["kturn"], A["bturn"],
        A["kriver"], A["briver"], A["binom"], A["perms"])
    n = end_street.sum()
    names = ["preflop", "flop", "turn", "river"]
    print(f"hands ending on street: " + "  ".join(
        f"{names[s]} {100*end_street[s]/n:.1f}%" for s in range(4)))
    print(f"hands REACHING the flop: {100*saw_flop/n:.1f}%")
    dtot = dec_street.sum()
    print("sampled decision points by street: " + "  ".join(
        f"{names[s]} {100*dec_street[s]/dtot:.1f}%" for s in range(4)))
    print(f"({time.time()-t:.0f}s)")

    print("\n=== 2) COVERAGE SCAN (all 214M infosets) ===")
    t = time.time()
    z = np.load(ART / "betting_tree_v1.npz")
    bases, streets = z["bases"], z["streets"]
    bps = np.array([cfg["buckets"]["preflop"], cfg["buckets"]["flop"],
                    cfg["buckets"]["turn"], cfg["buckets"]["river"]],
                   dtype=np.int64)
    out = coverage_scan(bases, streets, bps, sk, regret, stratsum, 512)
    agg = out.sum(axis=0)  # (4 streets, 7 counters)
    print(f"{'street':>8} {'infosets':>12} {'regret_nz':>10} {'strat_nz':>9} "
          f"{'strat>1':>8} {'strat>10':>9} {'strat>100':>10} {'avg_mass':>9}")
    for s in range(4):
        tot = agg[s, 0]
        if tot == 0:
            continue
        print(f"{names[s]:>8} {int(tot):>12,} "
              f"{100*agg[s,1]/tot:>9.1f}% {100*agg[s,2]/tot:>8.1f}% "
              f"{100*agg[s,3]/tot:>7.1f}% {100*agg[s,4]/tot:>8.1f}% "
              f"{100*agg[s,5]/tot:>9.1f}% {agg[s,6]/max(agg[s,2],1):>9.1f}")
    print(f"({time.time()-t:.0f}s)")


if __name__ == "__main__":
    main(sys.argv[1])
