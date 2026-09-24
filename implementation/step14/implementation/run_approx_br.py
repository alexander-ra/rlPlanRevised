"""
run_approx_br.py -- failure mode 3: an approximate (learned) best response is a LOWER bound.

    python run_approx_br.py [--seeds 3] [--max-hands 100000] [--workers 14]

Part A -- stationary targets. A black-box learner (tabular every-visit Monte-Carlo control,
epsilon = 0.1, sees only its own cards, the public actions and its payoff) plays the target in
each seat for up to `max_hands` hands. At budgets 1e2..1e5 hands its greedy strategy is
evaluated EXACTLY against the target; the approximate exploitability is the mean over seats of
that value (the same convention as exact exploitability = NashConv/2 = mean best-response
value over seats). Ratio approx / exact < 1 always; the plan's target: within 10 % on Leduc.

Part B -- adaptive targets online. The same learner plays each adaptive agent for one
2000-hand match (both seats, duplicate cards). Its realised damage (v*_seat minus the agent's
policy-exact EV) is compared with the white-box teaching attack of run_adaptation.py.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from multiprocessing import Pool

import numpy as np

import deps
import zoo
import tasks
from agents import MCLearner, HandRecord
from logutil import Logger

TARGETS = {"kuhn": ["Random", "TightPassive", "LooseAggr", "AlwaysBet", "LLM-Qwen7B", "LLM-GPT20B",
                    "BR-Tight", "Nash"],
           "leduc": ["Random", "Rock", "Maniac", "CallingStation", "LoosePassive", "BR-Rock", "Nash"]}
BUDGETS = [100, 300, 1000, 3000, 10000, 30000, 100000]


def learn(args):
    game, target, seat, seed, max_hands = args
    ctx = zoo.context(game)
    tg = ctx.tg
    rng = np.random.default_rng(seed * 1009 + seat)
    L = MCLearner(eps=0.1)
    L.start(tg, seat, rng)
    tprof = ctx.profiles[target]
    prof = [None, None]
    prof[1 - seat] = tprof[1 - seat]
    out = {}
    for t in range(max_hands):
        prof[seat] = L.policy()
        term, decisions, chances = tg.sample_hand(prof, rng)
        L.observe(HandRecord(t, term, chances, None, None, decisions))
        if t + 1 in BUDGETS:
            ev = [None, None]
            ev[seat] = L.greedy(); ev[1 - seat] = tprof[1 - seat]
            out[t + 1] = float(tg.values(ev)[seat])
    return (game, target, seat, seed, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="+", default=["kuhn", "leduc"])
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--max-hands", type=int, default=100000)
    ap.add_argument("--workers", type=int, default=14)
    args = ap.parse_args()
    log = Logger("approx_br")
    for game in args.games:
        t0 = time.time()
        ctx = zoo.context(game)
        jobs = [(game, tg_, seat, s, args.max_hands) for tg_ in TARGETS[game]
                for seat in (0, 1) for s in range(args.seeds)]
        with Pool(args.workers) as pool:
            res = pool.map(learn, jobs)
        out = {"game": game, "budgets": BUDGETS, "seeds": args.seeds, "targets": {}}
        for target in TARGETS[game]:
            exact = ctx.tg.nash_conv(ctx.profiles[target])["exploitability"]
            per_b = {}
            for b in BUDGETS:
                vals = []
                for s in range(args.seeds):
                    vv = [r[4][b] for r in res if r[1] == target and r[3] == s]
                    vals.append(float(np.mean(vv)))        # mean over the two seats
                per_b[b] = {"approx": float(np.mean(vals)), "min": float(np.min(vals)),
                            "max": float(np.max(vals)),
                            "ratio": float(np.mean(vals) / exact) if exact > 1e-6 else None}
            out["targets"][target] = {"exact_exploitability": exact, "by_budget": per_b}
            log(f"[{game}] {target:13s} exact {exact:.4f} | " + " ".join(
                f"{b}:{per_b[b]['approx']:+.3f}" for b in BUDGETS))
        # Part B: online learner vs adaptive agents (2000 hands, 5 seeds)
        jobs = [(game, a, "MC-learner", s, seat, 2000) for a in ctx.adaptive_names + ["Nash"]
                for s in range(5) for seat in (0, 1)]
        with Pool(args.workers) as pool:
            res = pool.map(tasks.run, jobs)
        online = {}
        for a in ctx.adaptive_names + ["Nash"]:
            dmg = [float(np.mean(ctx.v_star[r["meta"][4]] - r["ev"])) for r in res if r["meta"][1] == a]
            expo = [float(np.mean(r["expo"])) for r in res if r["meta"][1] == a]
            online[a] = {"damage_mean": float(np.mean(dmg)), "damage_ci95": float(1.96 * np.std(dmg, ddof=1) / np.sqrt(len(dmg))),
                         "exposure_mean": float(np.mean(expo)), "n": len(dmg)}
            log(f"[{game}] online MC learner vs {a:9s}: damage {online[a]['damage_mean']:+.3f} "
                f"± {online[a]['damage_ci95']:.3f} (agent's mean exposure {online[a]['exposure_mean']:.3f})")
        out["online_learner"] = online
        out["runtime_seconds"] = time.time() - t0
        with open(os.path.join(deps.RESULTS_DIR, f"approx_br_{game}.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, default=float)
        log(f"[{game}] done in {out['runtime_seconds']:.0f} s")


if __name__ == "__main__":
    main()
