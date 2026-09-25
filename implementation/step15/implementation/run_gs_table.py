"""
run_gs_table.py -- P0: replicate Ganzfried & Sandholm (2015), Table I, on Chapter 14's Kuhn engine.

    python run_gs_table.py [--n 400] [--n-eq 200] [--hands 1000] [--workers 14] [--no-tiebreak]

Validation of this chapter's RWYWE implementation against the published numbers before it is
used anywhere else. Setup as in G&S Sec. 9.2: we are player 1 (seat 0, v* = -1/18); frequency
model with a Dirichlet prior of 5 fictitious equilibrium hands at every opponent information
set; the opponent's card is observed after every hand; all algorithms use Alg. 6's pessimistic
update; 1,000-hand matches; the same deals for every algorithm against a given opponent.
Opponent classes (G&S Sec. 9.2):
  random        a mixed strategy drawn uniformly at every information set, fixed for the match
  sophisticated each action probability drawn uniformly within 0.2 of player 2's equilibrium
  dynamic       a random strategy for 100 hands, then a best response to our CURRENT strategy
                (re-computed every hand) for the remaining 900
  equilibrium   player 2's equilibrium (Chapter 14's CFR+ blueprint, exploitability 9.6e-6)
G&S ran 40,000 opponents per class; this replication runs fewer, so its intervals are wider.
Win rate is reported two ways: realised chips (what G&S's table reports) and the exact expected
value of the two policies in force each hand (lower variance, same mean).
"""

from __future__ import annotations

import argparse
import json
import os
import time
import zlib
from multiprocessing import Pool

import numpy as np

import boot
import zoo
import simulate
from agents import Stationary, TeachingAdversary
from safe_agents import GiftSafe
from log15 import Logger

RULES = ["rwywe", "befewp", "beffe", "besteq", "br"]
LABEL = {"rwywe": "RWYWE", "befewp": "BEFEWP", "beffe": "BEFFE", "besteq": "Best Equilibrium",
         "br": "Best response"}
# G&S (2015) Table I, $/hand, 95 % CI +-0.0004 (40,000 opponents per class)
GS_TABLE = {"rwywe": {"random": 0.3636, "sophisticated": -0.0110, "dynamic": -0.02043, "equilibrium": -0.0556},
            "befewp": {"random": 0.3553, "sophisticated": -0.0115, "dynamic": -0.02138, "equilibrium": -0.0556},
            "beffe": {"random": 0.1995, "sophisticated": -0.0131, "dynamic": -0.03972, "equilibrium": -0.0556},
            "besteq": {"random": 0.1450, "sophisticated": -0.0148, "dynamic": -0.03522, "equilibrium": -0.0556},
            "br": {"random": 0.4700, "sophisticated": 0.0548, "dynamic": -0.12094, "equilibrium": -0.0556}}


def opponent_profile(ctx, cls, idx):
    tg = ctx.tg
    rng = np.random.default_rng(zlib.crc32(f"gs|{cls}|{idx}".encode()))
    P = tg.players[1]
    B = np.zeros((len(P.infoset_strings), tg.n_actions))
    eq = ctx.blueprint[1]
    for I in range(len(P.infoset_strings)):
        if cls in ("random", "dynamic"):
            p = rng.uniform(0.0, 1.0)
        elif cls == "sophisticated":
            ps = eq[I, 1]
            p = rng.uniform(max(0.0, ps - 0.2), min(1.0, ps + 0.2))
        else:
            p = eq[I, 1]
        B[I, 1], B[I, 0] = p, 1.0 - p
    prof = [ctx.blueprint[0], tg.normalize(1, B)]
    return prof


def job(args):
    cls, idx, rule, n, tb = args
    ctx = zoo.context("kuhn")
    tg = ctx.tg
    prof = opponent_profile(ctx, cls, idx)
    base = Stationary(f"{cls}-{idx}", prof)
    opp = TeachingAdversary("dyn", base, 100, refit_every=1) if cls == "dynamic" else base
    agent = GiftSafe(LABEL[rule], ctx, rule=rule, model="gs", reveal="always", refit_every=1,
                     horizon=n, tiebreak=tb)
    decks = simulate.draw_decks(n, 3, zlib.crc32(f"deal|{cls}|{idx}".encode()) % (2 ** 31))
    act_seed = zlib.crc32(f"act|{cls}|{idx}|{rule}".encode()) % (2 ** 31)
    r = simulate.play_match(tg, ctx.bridge, agent, opp, 0, n, decks, act_seed, None, None,
                            ctx.v_star)
    kb = np.concatenate([[0.0], np.asarray(agent.k_trace[:-1])])
    viol = int(np.sum(r["expo"] > np.maximum(kb, 0.0) + 1e-6))
    return {"cls": cls, "idx": idx, "rule": rule, "ev": float(r["ev"].mean()),
            "chips": float(r["chips"].mean()), "k_end": float(agent.k),
            "k_min": float(min(agent.k_trace)), "expo_mean": float(np.nanmean(r["expo"])),
            "expo_viol": viol, "solves": agent.n_solves,
            "br_share": float(np.mean(agent.mode_trace)) if agent.mode_trace else None}


def ci(v):
    v = np.asarray(v, float)
    return float(v.mean()), float(1.96 * v.std(ddof=1) / np.sqrt(len(v)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400, help="opponents per class (random/soph./dynamic)")
    ap.add_argument("--n-eq", type=int, default=200, help="opponents in the equilibrium class")
    ap.add_argument("--hands", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=14)
    ap.add_argument("--no-tiebreak", action="store_true",
                    help="use Chapter 14's LP as is (ties among optimal strategies left to HiGHS)")
    args = ap.parse_args()
    tb = not args.no_tiebreak
    log = Logger("gs_table" + ("" if tb else "_notb"))
    t0 = time.time()
    counts = {"random": args.n, "sophisticated": args.n, "dynamic": args.n, "equilibrium": args.n_eq}
    jobs = [(c, i, r, args.hands, tb) for c, m in counts.items() for i in range(m) for r in RULES]
    log(f"P0 G&S Table I replication: {len(jobs)} matches of {args.hands} hands, {args.workers} workers")
    with Pool(args.workers) as pool:
        res = pool.map(job, jobs, chunksize=4)
    out = {"setup": {"hands": args.hands, "opponents": counts, "seat": 0,
                     "v_star": float(zoo.context("kuhn").v_star[0]),
                     "model": "frequency counts + Dirichlet prior of 5 equilibrium hands",
                     "update": "Alg. 6 (card observed every hand)",
                     "lp_tiebreak_toward_blueprint": tb},
           "gs_table": GS_TABLE, "table": {}, "checks": {}}
    for rule in RULES:
        out["table"][rule] = {}
        for c in counts:
            R = [x for x in res if x["rule"] == rule and x["cls"] == c]
            ev_m, ev_ci = ci([x["ev"] for x in R])
            ch_m, ch_ci = ci([x["chips"] for x in R])
            out["table"][rule][c] = {"ev": ev_m, "ev_ci95": ev_ci, "chips": ch_m, "chips_ci95": ch_ci,
                                     "n": len(R), "gs": GS_TABLE[rule][c],
                                     "k_end_mean": float(np.mean([x["k_end"] for x in R])),
                                     "k_min": float(min(x["k_min"] for x in R)),
                                     "expo_mean": float(np.mean([x["expo_mean"] for x in R])),
                                     "expo_violations": int(sum(x["expo_viol"] for x in R)),
                                     "matches_below_vstar": int(sum(x["ev"] < out["setup"]["v_star"] for x in R)),
                                     "br_share": (float(np.mean([x["br_share"] for x in R]))
                                                  if R[0]["br_share"] is not None else None)}
            e = out["table"][rule][c]
            log(f"{LABEL[rule]:17s} {c:13s} EV {ev_m:+.4f}±{ev_ci:.4f}  chips {ch_m:+.4f}±{ch_ci:.4f}  "
                f"(G&S {GS_TABLE[rule][c]:+.4f})  k_end {e['k_end_mean']:.2f} k_min {e['k_min']:.1e} "
                f"expo {e['expo_mean']:.3f} viol {e['expo_violations']} below v* {e['matches_below_vstar']}/{len(R)}")
    out["runtime_seconds"] = time.time() - t0
    fn = "gs_replication.json" if tb else "gs_replication_notb.json"
    with open(os.path.join(boot.RESULTS_DIR, fn), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    log(f"done in {out['runtime_seconds']:.0f} s")


if __name__ == "__main__":
    main()
