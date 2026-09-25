"""
run_protocol2p.py -- P1: RWYWE, the two-player C2 baseline, under Chapter 14's joint protocol.

    python run_protocol2p.py --game kuhn [--seeds 10] [--hands 2000] [--workers 14]
    python run_protocol2p.py --game leduc --tol 0.01

Agents (all share Chapter 7's continuous opponent model, refitted every 50 hands, as in Ch. 14):
  Nash       the CFR+ blueprint (Chapter 14)
  BestEq     best equilibrium against the model: G&S's per-hand baseline (Chapter 14)
  RNR(0.5)   restricted Nash response, p = 0.5 (Chapter 14)
  DirBR      full best response to the model (Chapter 14)
  RWYWE      Ganzfried & Sandholm's Risk What You've Won in Expectation; the opponent's card is
             used by the gift accounting only when the hand is shown down (Sec. 8.2.2 otherwise)
  RWYWE-rev  the same, with G&S's experimental assumption that the card is revealed every hand
  RWYWE-tb   RWYWE with LP ties broken toward the blueprint (safe_agents.floor_tiebreak)
  BEFEWP     G&S's best equilibrium, full exploitation when possible (showdown accounting)

Opponents: Chapter 14's sub-optimal Kuhn / Leduc population, its three switching opponents
(switch at hand 1,000 of 2,000) and its three teaching baits -- here with the attacker
re-computing its best response to the agent's CURRENT policy every hand ("TEACH1"), because
RWYWE's policy changes every hand (Chapter 14's attacker refreshed every 50 hands, in step with
its agents' refits; for the refit-every-50 agents the two attackers coincide).

Readouts: Chapter 14's gain / capture / h50 / exposure / switch r50 / teaching loss, with the
same definitions (imported from Chapter 14's run_adaptation), plus the match-level safety of
G&S's Def. 4.1: S = mean over the match of (EV_t - v*_seat), which must be >= 0 in expectation.
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
import tasks as tasks14
from agents import TeachingAdversary
from run_adaptation import (refs, first_hold, summarize, SUBOPT, SWITCH, TEACH, MIN_ATTAIN)
from safe_agents import GiftSafe
from log15 import Logger

ZOO_AGENTS = ["Nash", "BestEq", "RNR(0.5)", "DirBR"]
GIFT_AGENTS = ["RWYWE", "RWYWE-rev", "RWYWE-tb", "BEFEWP"]
N_CARDS = {"kuhn": 3, "leduc": 6}
_TOL = {"v": 0.0}


def build_agent(ctx, name, tol):
    if name == "RWYWE":
        return GiftSafe(name, ctx, rule="rwywe", model="cont", reveal="showdown", tol=tol)
    if name == "RWYWE-rev":
        return GiftSafe(name, ctx, rule="rwywe", model="cont", reveal="always", tol=tol)
    if name == "RWYWE-tb":
        return GiftSafe(name, ctx, rule="rwywe", model="cont", reveal="showdown", tol=tol,
                        tiebreak=True)
    if name == "BEFEWP":
        return GiftSafe(name, ctx, rule="befewp", model="cont", reveal="showdown", tol=tol)
    return ctx.agent(name)


def build_opp(ctx, spec):
    if spec.startswith("TEACH1:"):
        a, T = spec[7:].split("@")
        return TeachingAdversary(spec, ctx.agent(a), int(T), refit_every=1)
    return tasks14.build(ctx, spec)


def job(args):
    game, a, o, seed, seat, n, tol = args
    ctx = zoo.context(game)
    decks = simulate.seat_decks(simulate.draw_decks(n, N_CARDS[game], 10_000 + seed), seat)
    act_seed = zlib.crc32(f"{game}|{a}|{o}|{seed}|{seat}".encode()) % (2 ** 31)
    agent, opp = build_agent(ctx, a, tol), build_opp(ctx, o)
    t0 = time.time()
    r = simulate.play_match(ctx.tg, ctx.bridge, agent, opp, seat, n, decks, act_seed, None, None,
                            ctx.v_star)
    out = {"meta": (game, a, o, seed, seat, n), "ev": r["ev"].astype(np.float32),
           "chips": r["chips"].astype(np.float32), "expo": r["expo"].astype(np.float32),
           "seconds": time.time() - t0}
    if isinstance(agent, GiftSafe):
        out["k"] = np.asarray(agent.k_trace, dtype=np.float32)
        out["solves"] = agent.n_solves
        out["br_share"] = float(np.mean(agent.mode_trace)) if agent.mode_trace else None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="kuhn", choices=["kuhn", "leduc"])
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--hands", type=int, default=2000)
    ap.add_argument("--switch", type=int, default=1000)
    ap.add_argument("--tol", type=float, default=0.0, help="RWYWE re-solve tolerance on k (chips)")
    ap.add_argument("--workers", type=int, default=14)
    ap.add_argument("--agents", nargs="+", default=ZOO_AGENTS + GIFT_AGENTS)
    args = ap.parse_args()
    game, K, T = args.game, args.hands, args.switch
    log = Logger(f"protocol2p_{game}")
    t0 = time.time()
    ctx = zoo.context(game)
    tested = args.agents
    opps = list(SUBOPT[game]) + [f"SW:{a}>{b}@{T}" for a, b in SWITCH[game]] + \
        [f"TEACH1:{a}@{T}" for a in TEACH[game]]
    jobs = [(game, a, o, s, seat, K, args.tol) for a in tested for o in opps
            for s in range(args.seeds) for seat in (0, 1)]
    # longest jobs first (gift agents), so the pool is not left waiting on stragglers
    jobs.sort(key=lambda j: (j[1] not in GIFT_AGENTS, j[2]))
    log(f"[{game}] {len(tested)} agents x {len(opps)} conditions x {args.seeds} seeds x 2 seats = "
        f"{len(jobs)} matches of {K} hands (tol {args.tol})")
    with Pool(args.workers) as pool:
        res = pool.map(job, jobs, chunksize=1)
    by = {(r["meta"][1], r["meta"][2], r["meta"][3], r["meta"][4]): r for r in res}
    R = {s: {} for s in (0, 1)}
    for o in SUBOPT[game] + list({x for p in SWITCH[game] for x in p}) + TEACH[game]:
        for seat in (0, 1):
            R[seat][o] = refs(ctx, o, seat)
    vs = ctx.v_star
    out = {"game": game, "seeds": args.seeds, "hands": K, "switch_at": T, "tol": args.tol,
           "tested": tested, "subopt": SUBOPT[game], "switch_pairs": SWITCH[game],
           "teach_baits": TEACH[game], "teach_refresh": 1, "v_star": list(vs), "agents": {},
           "curves": {}}
    for a in tested:
        A = {"stationary": {}, "switch": {}, "teach": {}, "safety": {}}
        # ------------- stationary sub-optimal population (Chapter 14's definitions)
        caps, h50s, reach, expo_m, S_all = [], [], [], [], []
        per_opp = {}
        for o in SUBOPT[game]:
            og, oc = [], []
            for s in range(args.seeds):
                gp, cp = [], []
                for seat in (0, 1):
                    r = by[(a, o, s, seat)]
                    nash, br = R[seat][o]
                    ev = r["ev"].astype(float)
                    gp.append(float(np.mean(ev - nash)))
                    expo_m.append(float(np.mean(r["expo"])))
                    S_all.append(float(np.mean(ev - vs[seat])))
                    if br - nash >= MIN_ATTAIN:
                        cap = (ev - nash) / (br - nash)
                        cp.append(float(np.mean(cap[-500:])))
                        h = first_hold(cap, 0.5)
                        h50s.append(h if h is not None else np.nan)
                        reach.append(h is not None)
                og.append(np.mean(gp))
                if cp:
                    oc.append(np.mean(cp))
            caps.extend(oc)
            per_opp[o] = {"gain": summarize(og), "final_capture": summarize(oc)}
        seed_gain = [np.mean([np.mean([float(np.mean(by[(a, o, s, seat)]["ev"] - R[seat][o][0]))
                                       for seat in (0, 1)]) for o in SUBOPT[game]])
                     for s in range(args.seeds)]
        A["stationary"] = {"population_gain": summarize(seed_gain), "final_capture": summarize(caps),
                           "h50": summarize(h50s),
                           "h50_reached_share": float(np.mean(reach)) if reach else None,
                           "exposure_mean": summarize(expo_m), "per_opponent": per_opp,
                           "match_safety_S": summarize(S_all),
                           "matches_with_S_below_0": int(sum(x < 0 for x in S_all))}
        # ------------- switching opponents
        for (oa, ob) in SWITCH[game]:
            spec = f"SW:{oa}>{ob}@{T}"
            r50s, costs, S = [], [], []
            for s in range(args.seeds):
                for seat in (0, 1):
                    r = by[(a, spec, s, seat)]
                    ev = r["ev"].astype(float)
                    nb, bb = R[seat][ob]
                    if bb - nb >= MIN_ATTAIN:
                        h = first_hold((ev - nb) / (bb - nb), 0.5, start=T)
                        r50s.append(h if h is not None else np.nan)
                    costs.append(float(np.mean(nb - ev[T:T + 300])))
                    S.append(float(np.mean(ev - vs[seat])))
            A["switch"][spec] = {"r50": summarize(r50s),
                                 "r50_reached_share": float(np.mean(np.isfinite(r50s))) if r50s else None,
                                 "switch_cost": summarize(costs), "match_safety_S": summarize(S)}
        # ------------- teaching attacks (attacker refreshes every hand)
        S_teach = []
        for bait in TEACH[game]:
            spec = f"TEACH1:{bait}@{T}"
            loss, baitgain, expo_after, S, kT = [], [], [], [], []
            for s in range(args.seeds):
                lp = []
                for seat in (0, 1):
                    r = by[(a, spec, s, seat)]
                    ev = r["ev"].astype(float)
                    lp.append(float(np.mean(vs[seat] - ev[T:])))
                    baitgain.append(float(np.mean(ev[:T] - R[seat][bait][0])))
                    expo_after.append(float(np.mean(r["expo"][T:])))
                    S.append(float(np.mean(ev - vs[seat])))
                    if "k" in r:
                        kT.append(float(r["k"][T - 1]))
                loss.append(np.mean(lp))
            S_teach.extend(S)
            A["teach"][spec] = {"loss_after_switch": summarize(loss), "bait_phase_gain": summarize(baitgain),
                                "exposure_after_switch": summarize(expo_after),
                                "match_safety_S": summarize(S),
                                "matches_with_S_below_0": int(sum(x < 0 for x in S)),
                                "k_at_switch": summarize(kT) if kT else None}
        A["safety"] = {"teach_S": summarize(S_teach),
                       "teach_matches_S_below_0": int(sum(x < 0 for x in S_teach)),
                       "teach_S_min": float(min(S_teach))}
        # ------------- gift-agent diagnostics
        G = [r for (aa, _, _, _), r in by.items() if aa == a and "k" in r]
        if G:
            kmins, viol, solves, secs, brsh = [], 0, [], [], []
            for r in G:
                k = r["k"].astype(float)
                kb = np.concatenate([[0.0], k[:-1]])
                viol += int(np.sum(r["expo"] > np.maximum(kb, 0.0) + 1e-6))
                kmins.append(float(k.min()))
                solves.append(r["solves"])
                secs.append(r["seconds"])
                if r["br_share"] is not None:
                    brsh.append(r["br_share"])
            A["gift_diagnostics"] = {"k_min": float(min(kmins)), "exposure_above_k": viol,
                                     "lp_solves_mean": float(np.mean(solves)),
                                     "seconds_per_match": float(np.mean(secs)),
                                     "full_br_share": float(np.mean(brsh)) if brsh else None}
        out["agents"][a] = A
        g = A["stationary"]["population_gain"]
        log(f"[{game}] {a:10s} gain {g['mean']:+.3f}±{g['ci95']:.3f} capture "
            f"{A['stationary']['final_capture']['mean']:.2f} expo {A['stationary']['exposure_mean']['mean']:.3f} "
            f"| teach loss " + " ".join(f"{k.split(':')[1].split('@')[0]} {v['loss_after_switch']['mean']:+.3f}"
                                        for k, v in A["teach"].items())
            + f" | teach match S {A['safety']['teach_S']['mean']:+.4f} (min {A['safety']['teach_S_min']:+.4f},"
              f" {A['safety']['teach_matches_S_below_0']} below 0)"
            + (f" | k_min {A['gift_diagnostics']['k_min']:.1e} viol {A['gift_diagnostics']['exposure_above_k']} "
               f"solves {A['gift_diagnostics']['lp_solves_mean']:.0f} {A['gift_diagnostics']['seconds_per_match']:.1f}s"
               if "gift_diagnostics" in A else ""))

    # ------------- curves (mean over seeds and seats, every 10 hands)
    def curve(a, o, fn):
        return np.mean([fn(by[(a, o, s, seat)], seat) for s in range(args.seeds) for seat in (0, 1)],
                       axis=0)[::10].tolist()
    rep = {"kuhn": "LooseAggr", "leduc": "Maniac"}[game]
    out["curves"]["capture_vs"] = rep
    out["curves"]["capture"] = {a: curve(a, rep, lambda r, seat: (r["ev"] - R[seat][rep][0]) /
                                         (R[seat][rep][1] - R[seat][rep][0])) for a in tested}
    out["curves"]["teach"] = {}
    for bait in TEACH[game]:
        te = f"TEACH1:{bait}@{T}"
        out["curves"]["teach"][te] = {
            "ev_minus_vstar": {a: curve(a, te, lambda r, seat: r["ev"] - vs[seat]) for a in tested},
            "cum_ev_minus_vstar": {a: curve(a, te, lambda r, seat: np.cumsum(r["ev"] - vs[seat])) for a in tested},
            "exposure": {a: curve(a, te, lambda r, seat: r["expo"]) for a in tested},
            "k": {a: curve(a, te, lambda r, seat: r["k"]) for a in tested if a in GIFT_AGENTS}}
    out["curves"]["k_vs_rep"] = {a: curve(a, rep, lambda r, seat: r["k"]) for a in tested if a in GIFT_AGENTS}
    out["runtime_seconds"] = time.time() - t0
    path = os.path.join(boot.RESULTS_DIR, f"protocol2p_{game}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=float)
    log(f"[{game}] done in {out['runtime_seconds']:.0f} s -> {path}")


if __name__ == "__main__":
    main()
