"""
run_adaptation.py -- E2: the joint adaptation protocol on Kuhn and Leduc
(+ failure modes 1, 5 and 7).

    python run_adaptation.py [--games kuhn leduc] [--seeds 10] [--hands 2000] [--workers 14]

For every agent under test and every opponent condition, `seeds` duplicate match pairs
(both seats, same cards) of K hands. The protocol reports, per agent:

  GAIN      mean payoff above the Nash blueprint against the sub-optimal population
            (policy-exact EV), and the share of the attainable gain captured
            capture_t = (EV_t - EV_Nash) / (EV_BR - EV_Nash)   (EV_BR = exact best response)
  SPEED     h50 / h80: first hand t at which the mean capture over [t, t+100) reaches 0.5 / 0.8
  RECOVERY  opponent switches A -> B at hand T: r50 = hands after T until capture vs B
            reaches 0.5 (same rule); switch cost = mean (EV_Nash(B) - EV_t) over [T, T+300)
  EXPOSURE  seat exposure of the policy in force (v*_seat - worst case), mean and max over
            the match; and the realised loss under a white-box teaching attack (bait until T,
            then the exact best response to the agent's current policy, refreshed every 50
            hands): mean (v*_seat - EV_t) over [T, K)
  CONFIDENCE  95% intervals over seeds (seat-pairs); the per-window estimator comparison
            (raw chips / AIVAT / policy-exact) for failure mode 5
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
from logutil import Logger

TESTED = {"kuhn": ["Nash", "BR-Tight", "TypeBR", "DirBR", "DirBR-CP", "RNR(0.5)", "BestEq"],
          "leduc": ["Nash", "BR-Rock", "TypeBR", "DirBR", "DirBR-CP", "RNR(0.5)", "BestEq"]}
SUBOPT = {"kuhn": ["Random", "AlwaysPass", "AlwaysBet", "TightPassive", "LooseAggr", "Threshold",
                   "LLM-Qwen7B", "LLM-GPT20B", "LLM-OT7B", "BR-Tight"],
          "leduc": ["Random", "CallingStation", "Maniac", "Rock", "LoosePassive", "BR-Rock"]}
SWITCH = {"kuhn": [("TightPassive", "LooseAggr"), ("LooseAggr", "TightPassive"), ("AlwaysPass", "AlwaysBet")],
          "leduc": [("Rock", "Maniac"), ("Maniac", "Rock"), ("CallingStation", "Rock")]}
TEACH = {"kuhn": ["TightPassive", "LooseAggr", "AlwaysBet"],
         "leduc": ["Rock", "Maniac", "CallingStation"]}
WIN = 100          # window for the capture rule
MIN_ATTAIN = 0.02  # chips/hand; below this the capture ratio is not defined


def refs(ctx, opp, seat):
    """(EV of the Nash blueprint, exact best-response value) for `seat` against a stationary opp."""
    tg = ctx.tg
    prof = [None, None]
    prof[seat] = ctx.blueprint[seat]
    prof[1 - seat] = ctx.profiles[opp][1 - seat]
    nash = float(tg.values(prof)[seat])
    br = float(tg.best_response(seat, prof))
    return nash, br


def first_hold(g, thr, start=0, win=WIN):
    """Hands after `start` until the policy in force captures >= thr AND keeps it on average
    over the next `win` hands: first t >= start with g[t] >= thr and mean(g[t:t+win]) >= thr
    (None if never). Measured on the policy-exact capture, so it has no sampling noise."""
    if len(g) - start < win:
        return None
    seg = g[start:]
    c = np.concatenate([[0.0], np.cumsum(seg)])
    m = (c[win:] - c[:-win]) / win
    ok = (seg[:len(m)] >= thr) & (m >= thr)
    idx = np.where(ok)[0]
    return int(idx[0]) if len(idx) else None


GRID_STEP = 50


def grid_windows(g, win=WIN, step=GRID_STEP):
    """Means of g over windows [t, t+win) for t = 0, step, 2*step, ..."""
    starts = np.arange(0, len(g) - win + 1, step)
    c = np.concatenate([[0.0], np.cumsum(g)])
    return starts, (c[starts + win] - c[starts]) / win


def grid_h50(g, thr=0.5):
    starts, m = grid_windows(g)
    idx = np.where(m >= thr)[0]
    return int(starts[idx[0]]) if len(idx) else None


def summarize(vals):
    v = np.asarray([x for x in vals if x is not None and np.isfinite(x)], dtype=float)
    if len(v) == 0:
        return {"mean": None, "ci95": None, "n": 0}
    se = v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else 0.0
    return {"mean": float(v.mean()), "ci95": float(1.96 * se), "n": int(len(v)),
            "median": float(np.median(v))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="+", default=["kuhn", "leduc"])
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--hands", type=int, default=2000)
    ap.add_argument("--switch", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=14)
    args = ap.parse_args()
    log = Logger("adaptation")
    K, T = args.hands, args.switch
    for game in args.games:
        t0 = time.time()
        ctx = zoo.context(game)
        tested = TESTED[game]
        opps = list(SUBOPT[game]) + [f"SW:{a}>{b}@{T}" for a, b in SWITCH[game]] + \
            [f"TEACH:{a}@{T}" for a in TEACH[game]]
        jobs = [(game, a, o, s, seat, K) for a in tested for o in opps
                for s in range(args.seeds) for seat in (0, 1)]
        log(f"[{game}] {len(tested)} agents x {len(opps)} opponent conditions x {args.seeds} seeds "
            f"x 2 seats = {len(jobs)} matches of {K} hands")
        with Pool(args.workers) as pool:
            res = pool.map(tasks.run, jobs, chunksize=4)
        by = {(r["meta"][1], r["meta"][2], r["meta"][3], r["meta"][4]): r for r in res}
        R = {s: {} for s in (0, 1)}
        for o in SUBOPT[game] + list({x for p in SWITCH[game] for x in p}) + TEACH[game]:
            for seat in (0, 1):
                R[seat][o] = refs(ctx, o, seat)
        out = {"game": game, "seeds": args.seeds, "hands": K, "switch_at": T, "window": WIN,
               "tested": tested, "subopt": SUBOPT[game], "switch_pairs": SWITCH[game],
               "teach_baits": TEACH[game], "v_star": list(ctx.v_star), "refs": {
                   o: {"nash_ev": [R[0][o][0], R[1][o][0]], "br_ev": [R[0][o][1], R[1][o][1]]}
                   for o in R[0]}, "agents": {}, "curves": {}, "fm5": {}}
        fm5_rows = []
        for a in tested:
            A = {"stationary": {}, "switch": {}, "teach": {}}
            # ---------------- stationary sub-optimal population
            gains, caps, h50s, h80s, expo_m, expo_x, reach50 = [], [], [], [], [], [], []
            per_opp = {}
            for o in SUBOPT[game]:
                og, oc, oh50, oh80 = [], [], [], []
                for s in range(args.seeds):
                    g_pair, cap_pair = [], []
                    for seat in (0, 1):
                        r = by[(a, o, s, seat)]
                        nash, br = R[seat][o]
                        att = br - nash
                        ev = r["ev"].astype(float)
                        g_pair.append(float(np.mean(ev - nash)))
                        expo_m.append(float(np.mean(r["expo"]))); expo_x.append(float(np.max(r["expo"])))
                        if att >= MIN_ATTAIN:
                            cap = (ev - nash) / att
                            cap_pair.append(float(np.mean(cap[-500:])))
                            h50 = first_hold(cap, 0.5); h80 = first_hold(cap, 0.8)
                            oh50.append(h50 if h50 is not None else np.nan)
                            oh80.append(h80 if h80 is not None else np.nan)
                            reach50.append(h50 is not None)
                            # failure mode 5: what an evaluator who sees only realised
                            # results can estimate per 100-hand window (grid every 50 hands)
                            _, wx = grid_windows(cap)
                            hx = grid_h50(cap)
                            for est_name in ("chips", "aivat"):
                                est = (r[est_name].astype(float) - nash) / att
                                _, we = grid_windows(est)
                                fm5_rows.append({"agent": a, "opp": o, "seed": s, "seat": seat,
                                                 "estimator": est_name, "h50_exact": hx,
                                                 "h50_est": grid_h50(est),
                                                 "window_abs_err": float(np.mean(np.abs(we - wx))),
                                                 "sd_hand": float(r[est_name].std()),
                                                 "att": att})
                    og.append(np.mean(g_pair))
                    if cap_pair:
                        oc.append(np.mean(cap_pair))
                gains.extend(og); caps.extend(oc); h50s.extend(oh50); h80s.extend(oh80)
                per_opp[o] = {"gain": summarize(og), "final_capture": summarize(oc),
                              "h50_median": float(np.nanmedian(oh50)) if oh50 and np.any(np.isfinite(oh50)) else None,
                              "h50_reached": float(np.mean(np.isfinite(oh50))) if oh50 else None}
            # per-seed population gain (mean over opponents) for the CI
            seed_gain = []
            for s in range(args.seeds):
                seed_gain.append(np.mean([np.mean([float(np.mean(by[(a, o, s, seat)]["ev"] - R[seat][o][0]))
                                                   for seat in (0, 1)]) for o in SUBOPT[game]]))
            A["stationary"] = {"population_gain": summarize(seed_gain),
                               "final_capture": summarize(caps),
                               "h50": summarize(h50s), "h80": summarize(h80s),
                               "h50_reached_share": float(np.mean(reach50)) if reach50 else None,
                               "exposure_mean": summarize(expo_m), "exposure_max": summarize(expo_x),
                               "per_opponent": per_opp}
            # ---------------- switching opponents
            for (oa, ob) in SWITCH[game]:
                spec = f"SW:{oa}>{ob}@{T}"
                r50s, costs, pre = [], [], []
                for s in range(args.seeds):
                    for seat in (0, 1):
                        r = by[(a, spec, s, seat)]
                        ev = r["ev"].astype(float)
                        na, ba = R[seat][oa]; nb, bb = R[seat][ob]
                        attb = bb - nb
                        if attb >= MIN_ATTAIN:
                            capb = (ev - nb) / attb
                            h = first_hold(capb, 0.5, start=T)
                            r50s.append(h if h is not None else np.nan)
                        costs.append(float(np.mean(nb - ev[T:T + 300])))
                        if ba - na >= MIN_ATTAIN:
                            pre.append(float(np.mean((ev[T - 300:T] - na) / (ba - na))))
                A["switch"][spec] = {"r50": summarize(r50s),
                                     "r50_reached_share": float(np.mean(np.isfinite(r50s))) if r50s else None,
                                     "switch_cost": summarize(costs), "pre_switch_capture": summarize(pre)}
            # ---------------- teaching attacks
            for bait in TEACH[game]:
                spec = f"TEACH:{bait}@{T}"
                loss, baitgain, expo_after = [], [], []
                for s in range(args.seeds):
                    lp = []
                    for seat in (0, 1):
                        r = by[(a, spec, s, seat)]
                        ev = r["ev"].astype(float)
                        vs = ctx.v_star[seat]
                        lp.append(float(np.mean(vs - ev[T:])))
                        baitgain.append(float(np.mean(ev[:T] - R[seat][bait][0])))
                        expo_after.append(float(np.mean(r["expo"][T:])))
                    loss.append(np.mean(lp))
                A["teach"][spec] = {"loss_after_switch": summarize(loss),
                                    "bait_phase_gain": summarize(baitgain),
                                    "exposure_after_switch": summarize(expo_after)}
            out["agents"][a] = A
            log(f"[{game}] {a:9s} gain {A['stationary']['population_gain']['mean']:+.3f}"
                f"±{A['stationary']['population_gain']['ci95']:.3f}  capture "
                f"{A['stationary']['final_capture']['mean'] if A['stationary']['final_capture']['mean'] is not None else float('nan'):.2f} "
                f"h50 med {A['stationary']['h50'].get('median', float('nan'))} "
                f"expo {A['stationary']['exposure_mean']['mean']:.3f} | teach loss "
                + " ".join(f"{k.split(':')[1]} {v['loss_after_switch']['mean']:+.3f}" for k, v in A['teach'].items()))
        # ---------------- curves for figures (mean over seeds and seats, every 10 hands)
        def curve(a, o, fn):
            arr = np.mean([fn(by[(a, o, s, seat)], seat) for s in range(args.seeds) for seat in (0, 1)], axis=0)
            return arr[::10].tolist()
        rep = {"kuhn": "LooseAggr", "leduc": "Maniac"}[game]
        out["curves"]["capture_vs"] = rep
        out["curves"]["capture"] = {a: curve(a, rep, lambda r, seat: (r["ev"] - R[seat][rep][0]) /
                                             (R[seat][rep][1] - R[seat][rep][0])) for a in tested}
        out["curves"]["switch"] = {}
        for (oa, ob) in SWITCH[game]:
            sw = f"SW:{oa}>{ob}@{T}"
            out["curves"]["switch"][sw] = {
                "gain_over_nash": {a: curve(a, sw, lambda r, seat, oa=oa, ob=ob: r["ev"] - np.where(
                    np.arange(K) < T, R[seat][oa][0], R[seat][ob][0])) for a in tested},
                "capture": {a: curve(a, sw, lambda r, seat, oa=oa, ob=ob: np.where(
                    np.arange(K) < T, (r["ev"] - R[seat][oa][0]) / max(R[seat][oa][1] - R[seat][oa][0], 1e-9),
                    (r["ev"] - R[seat][ob][0]) / max(R[seat][ob][1] - R[seat][ob][0], 1e-9))) for a in tested}}
        out["curves"]["teach"] = {}
        for bait in TEACH[game]:
            te = f"TEACH:{bait}@{T}"
            out["curves"]["teach"][te] = {
                "ev_minus_vstar": {a: curve(a, te, lambda r, seat: r["ev"] - ctx.v_star[seat]) for a in tested},
                "exposure": {a: curve(a, te, lambda r, seat: r["expo"]) for a in tested}}
        # cross-capture: how much of the attainable gain vs B the exact best response to A keeps
        cross = {}
        for (oa, ob) in SWITCH[game]:
            vals = []
            for seat in (0, 1):
                prof = [None, None]
                prof[seat] = ctx.tg.uniform(seat)
                prof[1 - seat] = ctx.profiles[oa][1 - seat]
                _, brA = ctx.tg.best_response(seat, prof, return_policy=True)
                prof[seat] = brA
                prof[1 - seat] = ctx.profiles[ob][1 - seat]
                ev = float(ctx.tg.values(prof)[seat])
                nb, bb = R[seat][ob]
                vals.append((ev - nb) / (bb - nb))
            cross[f"SW:{oa}>{ob}@{T}"] = float(np.mean(vals))
        out["switch_cross_capture"] = cross
        fm5_agent = "DirBR"
        out["curves"]["fm5_pair"] = [fm5_agent, rep]
        for est in ("chips", "aivat", "ev"):
            per = []
            for s in range(args.seeds):
                for seat in (0, 1):
                    r = by[(fm5_agent, rep, s, seat)]
                    nash, br = R[seat][rep]
                    per.append(grid_windows((r[est].astype(float) - nash) / (br - nash))[1])
            per = np.asarray(per)
            out["curves"][f"fm5_{est}_mean"] = per.mean(axis=0).tolist()
            out["curves"][f"fm5_{est}_sd"] = per.std(axis=0, ddof=1).tolist()
        out["curves"]["fm5_window_starts"] = grid_windows(np.zeros(K))[0].tolist()
        # ---------------- failure mode 5 summary
        for est in ("chips", "aivat"):
            rows = [r for r in fm5_rows if r["estimator"] == est and r["h50_exact"] is not None]
            err = [abs((r["h50_est"] if r["h50_est"] is not None else K) - r["h50_exact"]) for r in rows]
            sd = [r["sd_hand"] / r["att"] for r in rows]
            # hands for a +/- 0.25-capture 95% interval on one window mean
            need = [(1.96 * r["sd_hand"] / (0.25 * r["att"])) ** 2 for r in rows]
            out["fm5"][est] = {"n": len(rows), "h50_abs_error_median": float(np.median(err)),
                               "h50_abs_error_mean": float(np.mean(err)),
                               "window_capture_abs_error_median": float(np.median([r["window_abs_err"] for r in rows])),
                               "sd_over_attainable_median": float(np.median(sd)),
                               "hands_for_pm025_capture_median": float(np.median(need))}
        out["fm5"]["exact"] = {"h50_abs_error_median": 0.0, "note": "policy-exact EV has no card or action noise"}
        out["runtime_seconds"] = time.time() - t0
        path = os.path.join(deps.RESULTS_DIR, f"adaptation_{game}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, default=float)
        log(f"[{game}] FM5: " + "; ".join(f"{k}: |h50 err| median {v['h50_abs_error_median']:.0f}, "
                                          f"hands for ±0.25 capture {v.get('hands_for_pm025_capture_median', 0):.0f}"
                                          for k, v in out["fm5"].items() if k != "exact"))
        log(f"[{game}] done in {out['runtime_seconds']:.0f} s -> {path}")


if __name__ == "__main__":
    main()
