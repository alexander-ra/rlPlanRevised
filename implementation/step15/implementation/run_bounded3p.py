"""
run_bounded3p.py -- P2: a first three-player Kuhn pilot for Experiment 2.1 (feasibility only).

    python run_bounded3p.py [--seeds 5] [--hands 2000] [--workers 14]

Question: can a deviation from the equilibrium blueprint, scaled by model confidence and capped
by an exactly computed baseline-relative loss bound, keep a useful share of the exploitation gain
against heterogeneous opponents while bounding what a colluding pair can take -- and where does
it land relative to the equal-share line (0 chips/hand, the game being zero-sum)?

Agents (seat-rotated over the three seats, 5 seeds, 2,000 hands):
  Nash               the CFR+ blueprint (Chapter 14; NashConv 1.5e-7)
  DirBR3P, Blend3P   Chapter 14's unbounded exploiter and its fixed 50/50 behaviour blend
  BD(eps)            BoundedMix3P: L(sigma_t) <= eps by construction (eps = inf: confidence only)
  KL(beta)           KLAnchor3P: KL-anchored soft response, loss measured only
Opponent conditions (Chapter 14's, plus two pairs with one equilibrium player):
  independent pairs  (TightPassive, LooseAggr), (AlwaysPass, AlwaysBet), (Random, Random),
                     (LooseAggr, LooseAggr), (TightPassive, TightPassive),
                     (Nash, LooseAggr), (Nash, TightPassive)
  collude            a fixed pair playing the exact coalition best response to the BLUEPRINT
  teach              bait (TightPassive x 2) until hand 1,000, then the exact coalition best
                     response to the agent's CURRENT policy, refreshed every 50 hands
Per hand the runner records the agent's exact EV, the blueprint's exact EV against the same
opponent strategies (so the per-hand baseline-relative loss l_t = u(bp, y_t) - u(sigma_t, y_t)
is exact), and -- whenever the agent's policy changes -- its exact worst-case baseline-relative
loss L(sigma_t) over all coordinated pairs.
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
import run_nplayer as rn14
from agents import HandRecord
from bounded3p import Probe3, BoundedMix3P, KLAnchor3P
from mmsafe3p import CoalitionOracle, MMSafe3P, OracleProbe
from nplayer import Stationary3
from log15 import Logger

INDEP = [("TightPassive", "LooseAggr"), ("AlwaysPass", "AlwaysBet"), ("Random", "Random"),
         ("LooseAggr", "LooseAggr"), ("TightPassive", "TightPassive"),
         ("Nash", "LooseAggr"), ("Nash", "TightPassive")]
EPS = [0.01, 0.03, 0.1, 0.3, None]
BETAS = [1.0, 3.0, 10.0, 30.0]
MM_AGENTS = ["Maximin", "MM-BestEq", "MM-RWYWE", "MM-RWYWE-sd"]
_P = {}


def probe(c):
    """Exact coalition value / baseline-relative loss (CoalitionOracle; equals Probe3 to 1e-9)."""
    if "p" not in _P:
        _P["p"] = OracleProbe(c.tg, oracles(c))
    return _P["p"]


def maximin_data(c):
    """v_mm and the maximin strategy of each seat (results/maximin3p.json, maximin3p.py)."""
    if "mm" not in _P:
        with open(os.path.join(boot.RESULTS_DIR, "maximin3p.json"), encoding="utf-8") as fh:
            d = json.load(fh)
        v = [d["seats"][str(i)]["value"] for i in range(3)]
        prof = [np.asarray(d["seats"][str(i)]["strategy"]) for i in range(3)]
        _P["mm"] = (v, prof)
    return _P["mm"]


def oracles(c):
    if "orc" not in _P:
        _P["orc"] = {i: CoalitionOracle(c.tg, i) for i in range(3)}
    return _P["orc"]


def agent_names():
    return (["Nash", "DirBR3P", "Blend3P"] + [f"BD({'inf' if e is None else e})" for e in EPS]
            + [f"KL({b:g})" for b in BETAS] + MM_AGENTS)


def make_agent(c, name):
    if name.startswith("BD("):
        v = name[3:-1]
        return BoundedMix3P(name, c.blueprint, probe(c), None if v == "inf" else float(v))
    if name.startswith("KL("):
        return KLAnchor3P(name, c.blueprint, probe(c), float(name[3:-1]))
    if name in MM_AGENTS:
        v, prof = maximin_data(c)
        if name == "Maximin":
            return Stationary3(name, prof)
        rule = "besteq" if name == "MM-BestEq" else "rwywe"
        reveal = "showdown" if name.endswith("-sd") else "always"
        return MMSafe3P(name, c.blueprint, probe(c), oracles(c), v, prof, rule=rule, reveal=reveal)
    return c.agent(name)


def job(args):
    kind, name, seat, opps, seed, n, T = args
    c = rn14.ctx3()
    tg = c.tg
    pr = probe(c)
    agent = make_agent(c, name)
    others = [q for q in range(3) if q != seat]
    agents = [None] * 3
    agents[seat] = agent
    coalition = None
    if kind == "indep":
        for q, o in zip(others, opps):
            agents[q] = c.agent(o)
    elif kind == "collude":
        coalition = rn14.FixedCoalition(c, rn14._BlueprintStandIn(seat, c.blueprint[seat]), None, 0, 0)
    elif kind == "teach":
        bait = [None] * 3
        for q, o in zip(others, opps):
            bait[q] = c.profiles[o][q]
        coalition = rn14.FixedCoalition(c, agent, bait, T, 50)
    rng = np.random.default_rng(zlib.crc32(f"{seed}|{name}|{kind}|{opps}|{seat}".encode()))
    drng = np.random.default_rng(20_000 + seed)
    decks = np.stack([drng.permutation(4) for _ in range(n)])
    for s, a in enumerate(agents):
        if a is not None:
            a.start(tg, s, np.random.default_rng(seed * 31 + s))
    bp = c.blueprint[seat]
    ev = np.zeros(n); ev_bp = np.zeros(n); chips = np.zeros(n)
    Lt = np.zeros(n)
    cache, prof = {}, [None] * 3
    L_cache, CV_cache = {}, {}
    is_mm = hasattr(agent, "k_trace")
    cvt = np.zeros(n)
    last_ver = None
    t0 = time.time()
    for t in range(n):
        for a in agents:
            if a is not None:
                a.begin_hand(t)
        if coalition is not None:
            coalition.step(t)
        for s in range(3):
            prof[s] = agents[s].policy() if agents[s] is not None else coalition.policy(s)
        key = tuple((a.version if a is not None else coalition.version) for a in agents)
        if key not in cache:
            v = tg.values(prof)[seat]
            pb = list(prof); pb[seat] = bp
            cache = {key: (float(v), float(tg.values(pb)[seat]))}
        if agent.version != last_ver:
            last_ver = agent.version
            if last_ver not in L_cache:
                L_cache[last_ver] = 0.0 if name == "Nash" else pr.rel_loss(seat, agent.policy(), bp)
                if is_mm:
                    CV_cache[last_ver] = pr.coalition_value(seat, agent.policy())
        ev[t], ev_bp[t] = cache[key]
        Lt[t] = L_cache[last_ver]
        if is_mm:
            cvt[t] = CV_cache[last_ver]
        term, decisions, chances = tg.sample_hand(prof, rng, chance_seq=decks[t])
        chips[t] = tg.term_util[term, seat]
        rec = HandRecord(t, term, chances, [a for _, a in decisions], None, decisions)
        for a in agents:
            if a is not None:
                a.observe(rec)
    final = agent.policy()
    return {"kind": kind, "agent": name, "seat": seat, "opps": opps, "seed": seed,
            "ev": ev.astype(np.float32), "ev_bp": ev_bp.astype(np.float32),
            "L": Lt.astype(np.float32), "chips": chips.astype(np.float32),
            "final_coalition_value": pr.coalition_value(seat, final),
            "final_L": 0.0 if name == "Nash" else pr.rel_loss(seat, final, bp),
            "trace": getattr(agent, "trace", None), "seconds": time.time() - t0,
            "k": np.asarray(agent.k_trace, dtype=np.float32) if is_mm else None,
            "cv_in_force": cvt.astype(np.float32) if is_mm else None,
            "mm_solves": getattr(agent, "n_solves", None), "mm_unconverged": getattr(agent, "unconverged", None),
            "mm_cuts_added": getattr(agent, "n_cuts_added", None)}


def sm(v):
    v = np.asarray([x for x in v if x is not None and np.isfinite(x)], float)
    if len(v) == 0:
        return {"mean": None, "ci95": None, "n": 0}
    return {"mean": float(v.mean()), "ci95": float(1.96 * v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0,
            "min": float(v.min()), "max": float(v.max()), "n": int(len(v))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--hands", type=int, default=2000)
    ap.add_argument("--workers", type=int, default=14)
    ap.add_argument("--agents", nargs="+", default=None)
    args = ap.parse_args()
    log = Logger("bounded3p")
    t0 = time.time()
    n, T = args.hands, args.hands // 2
    names = args.agents or agent_names()
    conds = [("indep", op) for op in INDEP] + [("collude", None), ("teach", ("TightPassive", "TightPassive"))]
    jobs = [(k, a, seat, op, s, n, T) for a in names for (k, op) in conds
            for seat in range(3) for s in range(args.seeds)]
    jobs.sort(key=lambda j: (j[1] in ("Nash",), j[0] != "teach"))
    log(f"P2 bounded 3P pilot: {len(names)} agents x {len(conds)} conditions x 3 seats x "
        f"{args.seeds} seeds = {len(jobs)} matches of {n} hands")
    with Pool(args.workers) as pool:
        res = pool.map(job, jobs, chunksize=1)
    c = rn14.ctx3()
    tg = c.tg

    def ref(seat, opps):
        prof = [None] * 3
        prof[seat] = c.blueprint[seat]
        for q, o in zip([q for q in range(3) if q != seat], opps):
            prof[q] = c.profiles[o][q]
        return float(tg.values(prof)[seat]), float(tg.best_response(seat, prof))

    out = {"game": "kuhn_poker(players=3)", "seeds": args.seeds, "hands": n, "switch_at": T,
           "agents": names, "conditions": [[k, op] for k, op in conds], "equal_share": 0.0,
           "blueprint_seat_values": [float(x) for x in tg.values(c.blueprint)], "summary": {},
           "curves": {}}
    for a in names:
        R = [r for r in res if r["agent"] == a]
        S = {}
        # heterogeneous / independent opponents: gain over the blueprint, seat-averaged per seed
        gains, caps, Lmax, Lmean, lt_max, seat_avg_ev = [], [], [], [], [], []
        per_pair = {}
        for op in INDEP:
            g_seed = []
            for s in range(args.seeds):
                gs = []
                for seat in range(3):
                    r = next(x for x in R if x["kind"] == "indep" and tuple(x["opps"]) == op
                             and x["seat"] == seat and x["seed"] == s)
                    nash, br = ref(seat, op)
                    ev = r["ev"].astype(float)
                    gs.append(float(np.mean(ev - nash)))
                    if br - nash >= 0.02:
                        caps.append(float(np.mean((ev[-500:] - nash) / (br - nash))))
                    Lmax.append(float(r["L"].max())); Lmean.append(float(r["L"].mean()))
                    lt_max.append(float(np.max(r["ev_bp"] - r["ev"])))
                g_seed.append(np.mean(gs))
            gains.append(g_seed)
            per_pair["+".join(op)] = sm(g_seed)
        gains = np.asarray(gains)                       # (pairs, seeds)
        indep_ev = [np.mean([float(np.mean(x["ev"])) for x in R if x["kind"] == "indep" and x["seed"] == s])
                    for s in range(args.seeds)]
        S["indep"] = {"gain": sm(gains.mean(axis=0)), "final_capture": sm(caps), "seat_avg_ev": sm(indep_ev),
                      "L_max": sm(Lmax), "L_mean": sm(Lmean), "per_pair_gain": per_pair,
                      "realised_rel_loss_max": sm(lt_max)}
        for kind in ("collude", "teach"):
            Rk = [x for x in R if x["kind"] == kind]
            ev_seed, rel_seed, relmax, seat_ev, Lm, cv = [], [], [], [], [], []
            for s in range(args.seeds):
                rs = [x for x in Rk if x["seed"] == s]
                sl = slice(T, None) if kind == "teach" else slice(None)
                ev_seed.append(np.mean([float(np.mean(x["ev"][sl])) for x in rs]))      # seat-averaged
                rel_seed.append(np.mean([float(np.mean(x["ev_bp"][sl] - x["ev"][sl])) for x in rs]))
                relmax.extend([float(np.max(x["ev_bp"] - x["ev"])) for x in rs])
                Lm.extend([float(x["L"].max()) for x in rs])
                cv.extend([x["final_coalition_value"] for x in rs])
            bpv = np.mean([np.mean(x["ev_bp"][slice(T, None) if kind == "teach" else slice(None)]) for x in Rk])
            S[kind] = {"seat_avg_ev": sm(ev_seed), "rel_loss_mean": sm(rel_seed), "rel_loss_hand_max": sm(relmax),
                       "L_max": sm(Lm), "final_coalition_value": sm(cv),
                       "blueprint_ev_same_opponents": float(bpv),
                       "window": "hands 1000-1999" if kind == "teach" else "all hands"}
        S["final_L"] = sm([x["final_L"] for x in R])
        if R[0]["k"] is not None:
            v_mm, _ = maximin_data(c)
            Sm, viol, kmin, unconv, solves = {}, 0, [], 0, []
            for kind in ("indep", "collude", "teach"):
                vals = [float(np.mean(x["ev"] - v_mm[x["seat"]])) for x in R if x["kind"] == kind]
                Sm[kind] = sm(vals)
                Sm[kind]["matches_below_0"] = int(sum(v < 0 for v in vals))
            for x in R:
                k = x["k"].astype(float)
                kb = np.concatenate([[0.0], k[:-1]])
                viol += int(np.sum(x["cv_in_force"] < np.array([v_mm[x["seat"]]]) - np.maximum(kb, 0.0) - 1e-6))
                kmin.append(float(k.min())); unconv += int(x["mm_unconverged"] or 0); solves.append(x["mm_solves"])
            S["maximin_safety"] = {"S_vs_vmm": Sm, "cv_below_floor_hands": viol, "k_min": float(min(kmin)),
                                   "unconverged_solves": unconv, "solves_mean": float(np.mean(solves)),
                                   "k_end_mean": {kind: float(np.mean([x["k"][-1] for x in R if x["kind"] == kind]))
                                                  for kind in ("indep", "collude", "teach")}}
        S["seconds_per_match"] = float(np.mean([x["seconds"] for x in R]))
        tr = [x["trace"] for x in R if x["trace"]]
        if tr and "lam" in tr[0][-1]:
            S["lambda_final"] = sm([t[-1]["lam"] for t in tr])
            S["bound_final"] = sm([t[-1]["bound"] for t in tr])
            S["delta_br_final"] = sm([t[-1]["delta_br"] for t in tr])
        out["summary"][a] = S
        log(f"{a:9s} gain {S['indep']['gain']['mean']:+.4f}±{S['indep']['gain']['ci95']:.4f} "
            f"L_max(indep) {S['indep']['L_max']['max']:.3f} | collude ev {S['collude']['seat_avg_ev']['mean']:+.4f} "
            f"rel {S['collude']['rel_loss_mean']['mean']:+.4f} | teach ev {S['teach']['seat_avg_ev']['mean']:+.4f} "
            f"rel {S['teach']['rel_loss_mean']['mean']:+.4f} L_max {S['teach']['L_max']['max']:.3f} "
            f"| final CV {S['teach']['final_coalition_value']['mean']:+.3f} | {S['seconds_per_match']:.1f}s/match")
    # curves: teach condition, seat-averaged over seeds (every 10 hands)
    for kind in ("teach", "collude"):
        out["curves"][kind] = {a: np.mean([x["ev"] for x in res if x["agent"] == a and x["kind"] == kind],
                                          axis=0)[::10].tolist() for a in names}
        out["curves"][kind + "_k"] = {a: np.mean([x["k"] for x in res if x["agent"] == a and x["kind"] == kind],
                                                 axis=0)[::10].tolist() for a in names
                                      if any(x["k"] is not None for x in res if x["agent"] == a)}
        out["curves"][kind + "_bp"] = {a: np.mean([x["ev_bp"] for x in res if x["agent"] == a and x["kind"] == kind],
                                                  axis=0)[::10].tolist() for a in names}
    out["runtime_seconds"] = time.time() - t0
    with open(os.path.join(boot.RESULTS_DIR, "bounded3p.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=float)
    log(f"done in {out['runtime_seconds']:.0f} s")


if __name__ == "__main__":
    main()
