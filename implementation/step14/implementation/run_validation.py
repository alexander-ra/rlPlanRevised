"""
run_validation.py -- E0: validate every framework component against an independent reference.

    python run_validation.py            -> results/validation.json, logs/validation.log

Checks (plan's Validation section, raw step L776-781, plus the cross-checks this chapter adds):
  V1  NashConv / exploitability == OpenSpiel's exploitability.nash_conv (Kuhn, Leduc, 3P Kuhn)
  V2  exact values / best responses == Chapter 7's engine (bridge mapping)
  V3  Leduc exploitability of a Chapter 3 CFR strategy == Chapter 3's own evaluator (4 d.p.)
  V4  game values: Kuhn -1/18, Leduc -0.0856 (seat 0)
  V5  one-shot dual LP == Chapter 8's constraint-generation solvers on Kuhn
  V6  alpha-Rank (single + multi-population), Nash averaging, maximal lotteries, IML == OpenSpiel
  V7  spinning top: RPS -> transitive ratio 0, skill ladder -> 1
  V8  AIVAT: exact unbiasedness, exact variance-reduction factors (targets: >= 5x Kuhn,
      >= 10x Leduc), and a Monte Carlo confirmation
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

import deps
import trees
import solvers
import population as pop
import aivat
import zoo
from logutil import Logger

log = Logger("validation")
OUT = {}
T0 = time.time()


def v1_openspiel_nashconv():
    from open_spiel.python.algorithms import exploitability as ex
    rows = []
    for name in ("kuhn", "leduc", "kuhn3"):
        tg = trees.load(name)
        profs = {"uniform": tg.uniform_profile()}
        if name == "kuhn3":
            profs["cfr_10k"] = solvers.cfr_profile(tg, 10000, algo="cfr")
        else:
            ctx = zoo.context(name)
            for k in ("Nash", "Random") + tuple(zoo.TYPES[name])[:2]:
                profs[k] = ctx.profiles[k]
        for k, prof in profs.items():
            mine = tg.nash_conv(prof)["nash_conv"]
            ref = ex.nash_conv(tg.game, tg.to_openspiel_tabular(prof))
            rows.append({"game": name, "profile": k, "nash_conv": mine, "openspiel": ref,
                         "abs_diff": abs(mine - ref)})
            log(f"V1 {name:6s} {k:12s} NashConv mine {mine:.10f}  OpenSpiel {ref:.10f}")
    OUT["V1_nashconv_vs_openspiel"] = {"rows": rows,
                                        "max_abs_diff": max(r["abs_diff"] for r in rows)}


def v2_chapter7():
    from best_response import exact_value, best_response_value
    rows = []
    for name in ("kuhn", "leduc"):
        ctx = zoo.context(name)
        tg, br = ctx.tg, ctx.bridge
        names = list(ctx.types07)
        for a in names:
            for b in names[:3]:
                A, B = br.materialize(ctx.types07[a], 0), br.materialize(ctx.types07[b], 1)
                d1 = abs(tg.values([A, B])[0] - exact_value(br.g07, 0, ctx.types07[a], ctx.types07[b]))
                d2 = abs(tg.best_response(1, [A, B]) - best_response_value(br.g07, 1, ctx.types07[a]))
                rows.append({"game": name, "p0": a, "p1": b, "value_diff": d1, "br_diff": d2})
    mx = max(max(r["value_diff"], r["br_diff"]) for r in rows)
    log(f"V2 Chapter 7 bridge: {len(rows)} pairs, max |diff| = {mx:.2e}")
    OUT["V2_chapter7_bridge"] = {"n_pairs": len(rows), "max_abs_diff": mx}


def v3_chapter3():
    step03 = os.path.join(deps.IMPL_ROOT, "step03")
    sys.path.insert(0, step03)
    try:
        from cfr.cfr_trainer import LeducTrainer
        from evaluate.exploitability import compute_exploitability
    finally:
        sys.path.remove(step03)
    ctx = zoo.context("leduc")
    tg, br = ctx.tg, ctx.bridge
    out = []
    for iters in (10, 100):
        tr = LeducTrainer()
        tr.train(iters)
        theirs = compute_exploitability(tr.node_map)
        table = {}
        for key, (node, legal) in tr.node_map.items():
            avg = node.get_average_strategy()
            table[key] = {a: avg[i] for i, a in enumerate(legal)}
        prof = []
        for p in (0, 1):
            P = tg.players[p]
            B = np.zeros((len(P.infoset_strings), tg.n_actions))
            for I, node in br.rep_node[p].items():
                key = br.g07.info_set(br.state07(node), p)
                for a, pr in table[key].items():
                    B[I, a] = pr
            prof.append(tg.normalize(p, B))
        mine = tg.nash_conv(prof)["exploitability"]
        out.append({"iters": iters, "chapter3": theirs, "mine": mine, "abs_diff": abs(theirs - mine)})
        log(f"V3 Chapter 3 Leduc CFR {iters} it.: exploitability ch3 {theirs:.6f}  mine {mine:.6f}")
    OUT["V3_chapter3_exploitability"] = out


def v4_game_values():
    out = {}
    for name, ref in (("kuhn", -1.0 / 18.0), ("leduc", -0.0856)):
        ctx = zoo.context(name)
        v0 = ctx.v_star[0]
        bp = ctx.tg.nash_conv(ctx.blueprint)
        out[name] = {"lp_value_seat0": v0, "reference": ref, "abs_diff": abs(v0 - ref),
                     "blueprint_nash_conv": bp["nash_conv"],
                     "blueprint_exploitability": bp["exploitability"],
                     "blueprint_iters": zoo.BLUEPRINT_ITERS[name]}
        log(f"V4 {name}: LP value {v0:+.6f} (reference {ref:+.4f}); blueprint NashConv "
            f"{bp['nash_conv']:.2e} (exploitability {bp['exploitability']:.2e})")
    OUT["V4_game_values"] = out


def v5_chapter8():
    sys.path.append(deps.STEP08_IMPL)
    import ganzfried_solver as gs          # Step 08
    import rnr_solver as rs                # Step 08
    from safety_checker import game_value  # Step 08
    ctx = zoo.context("kuhn")
    tg, br = ctx.tg, ctx.bridge
    nash07 = ctx.types07["Nash"]
    rows = []
    for hero in (0, 1):
        v8 = game_value(br.g07, nash07, hero)
        for opp in ("TightPassive", "LooseAggressive", "AlwaysBet", "Random"):
            model07 = ctx.types07[opp]
            model = br.materialize(model07, 1 - hero)
            # best equilibrium (floor = v*)
            t = time.time()
            r8 = gs.safe_exploit(br.g07, hero, model07, floor=v8)
            t8 = time.time() - t
            t = time.time()
            B, v0 = ctx.lps[hero].floor(model, ctx.v_star[hero] - 1e-9, fill=ctx.blueprint[hero])
            t14 = time.time() - t
            prof = [None, None]; prof[hero] = B; prof[1 - hero] = model
            ev14 = tg.values(prof)[hero]
            wc14 = solvers.worst_case(tg, hero, B)
            rows.append({"hero": hero, "opp": opp, "method": "best_equilibrium",
                         "ev_ch8": r8["exploitation_value"], "ev_ch14": ev14,
                         "wc_ch8": r8["worst_case_value"], "wc_ch14": wc14,
                         "iters_ch8": r8["iterations"], "time_ch8": t8, "time_ch14": t14})
            for p in (0.3, 0.5, 0.8):
                r8 = rs.canonical_rnr(br.g07, hero, model07, p)
                B, _ = ctx.lps[hero].rnr(model, p, fill=ctx.blueprint[hero])
                prof = [None, None]; prof[hero] = B; prof[1 - hero] = model
                ev14 = tg.values(prof)[hero]
                wc14 = solvers.worst_case(tg, hero, B)
                rows.append({"hero": hero, "opp": opp, "method": f"rnr_{p}",
                             "ev_ch8": r8["exploitation_value"], "ev_ch14": ev14,
                             "wc_ch8": r8["worst_case_value"], "wc_ch14": wc14,
                             "obj_ch8": p * r8["exploitation_value"] + (1 - p) * r8["worst_case_value"],
                             "obj_ch14": p * ev14 + (1 - p) * wc14})
    for r in rows:
        if r["method"] == "best_equilibrium":
            r["diff"] = abs(r["ev_ch8"] - r["ev_ch14"])
        else:
            r["diff"] = abs(r["obj_ch8"] - r["obj_ch14"])
        log(f"V5 hero {r['hero']} vs {r['opp']:15s} {r['method']:17s} EV ch8 {r['ev_ch8']:+.4f} "
            f"ch14 {r['ev_ch14']:+.4f} | wc ch8 {r['wc_ch8']:+.4f} ch14 {r['wc_ch14']:+.4f} | diff {r['diff']:.1e}")
    OUT["V5_dual_lp_vs_chapter8"] = {"rows": rows, "max_objective_diff": max(r["diff"] for r in rows)}
    # timing on full Leduc (Chapter 8's loop did not converge there within its caps)
    ctxl = zoo.context("leduc")
    times = []
    for hero in (0, 1):
        model = ctxl.profiles["Rock"][1 - hero]
        t = time.time(); ctxl.lps[hero].floor(model, ctxl.v_star[hero] - 1e-9); times.append(time.time() - t)
        t = time.time(); ctxl.lps[hero].rnr(model, 0.5); times.append(time.time() - t)
    OUT["V5_dual_lp_vs_chapter8"]["leduc_solve_seconds"] = times
    log(f"V5 Leduc full-game LP solve times (s): {np.round(times, 3).tolist()}")


def v6_population():
    from open_spiel.python.egt import alpharank as osar
    from open_spiel.python.algorithms import nash_averaging as osna
    from open_spiel.python.voting import maximal_lotteries as osml, base as vbase
    import pyspiel
    rng = np.random.default_rng(14)
    mats = {"rps": np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float),
            "transitive": np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]], float)}
    X = rng.normal(size=(8, 8)); mats["random8"] = X - X.T
    rows = []
    for nm, M in mats.items():
        for a in (0.1, 1.0, 10.0, 100.0):
            mine = pop.alpharank(M, a, 50)
            _, _, pi, _, _ = osar.compute([M], m=50, alpha=a)
            rows.append({"matrix": nm, "method": f"alpharank_a{a}", "abs_diff": float(np.abs(mine - pi).max())})
        p, _ = pop.nash_average(M)
        osp, _ = osna.nash_averaging(pyspiel.create_tensor_game([M, -M]))
        rows.append({"matrix": nm, "method": "nash_average", "abs_diff": float(np.abs(p - np.ravel(osp)).max())})
        ml = pop.maximal_lottery(M)
        osm = np.asarray(osml.MaximalLotteriesVoting()._solve_game(M))
        rows.append({"matrix": nm, "method": "maximal_lottery", "abs_diff": float(np.abs(ml - osm).max())})
    # IML ranking vs OpenSpiel's run_election on a weighted-vote profile
    alts = ["a", "b", "c", "d"]
    votes = [vbase.WeightedVote(3, ["a", "b", "c", "d"]), vbase.WeightedVote(2, ["b", "c", "a", "d"]),
             vbase.WeightedVote(2, ["c", "a", "b", "d"]), vbase.WeightedVote(1, ["d", "a", "b", "c"])]
    prof = vbase.PreferenceProfile(votes=votes, alternatives=alts)
    margin = prof.margin_matrix()
    mine_levels = [[alts[i] for i in lvl] for lvl in pop.iterative_ml(margin.astype(float))]
    os_out = osml.MaximalLotteriesVoting(iterative=True).run_election(prof)
    rows.append({"matrix": "vote_profile", "method": "iml", "mine": mine_levels,
                 "openspiel": list(os_out.ranking)})
    T = [rng.normal(size=(3, 3, 3)) for _ in range(3)]
    for a in (0.5, 1.0):
        mine = pop.alpharank_multipop(T, a, 20)
        _, _, pi, _, _ = osar.compute(T, m=20, alpha=a)
        rows.append({"matrix": "random3x3x3", "method": f"multipop_a{a}", "abs_diff": float(np.abs(mine - pi).max())})
    for r in rows:
        log(f"V6 {r['matrix']:12s} {r['method']:18s} " +
            (f"|diff| {r['abs_diff']:.1e}" if "abs_diff" in r else f"mine {r['mine']} os {r['openspiel']}"))
    OUT["V6_population_vs_openspiel"] = {"rows": rows, "max_abs_diff": max(r.get("abs_diff", 0) for r in rows)}


def v7_spinning_top():
    rps = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float)
    idx = np.arange(5.0); ladder = idx[:, None] - idx[None, :]
    out = {"rps_transitive_ratio": pop.transitive_ratio(rps),
           "ladder_transitive_ratio": pop.transitive_ratio(ladder)}
    log(f"V7 spinning top: RPS {out['rps_transitive_ratio']:.4f} (target 0), ladder "
        f"{out['ladder_transitive_ratio']:.4f} (target 1)")
    OUT["V7_spinning_top"] = out


def v8_aivat(n_mc: int = 20000):
    out = {"exact": [], "monte_carlo": []}
    for name in ("kuhn", "leduc"):
        ctx = zoo.context(name)
        tg = ctx.tg
        opps = [k for k in ctx.stationary_names if k != "Nash"]
        for x in (0, 1):
            Vref = ctx.v_ref(x)
            tabs = {k: aivat.AivatTables(tg, x, k) for k in ("chance", "chance+x", "chance+x+y")}
            for o in opps:
                yB = ctx.profiles[o][1 - x]
                prof = [None, None]; prof[x] = ctx.blueprint[x]; prof[1 - x] = yB
                m0, v0 = aivat.exact_moments(tg, prof, tg.term_util[:, x])
                row = {"game": name, "seat": x, "agent": "Nash", "opponent": o, "ev": m0, "var_raw": v0}
                for k, T in tabs.items():
                    m, v = aivat.exact_moments(tg, prof, T.table(ctx.blueprint[x], Vref, B_y=yB))
                    row[f"bias_{k}"] = m - m0
                    row[f"vr_{k}"] = v0 / v
                out["exact"].append(row)
        # Monte Carlo confirmation on one pair per seat
        rng = np.random.default_rng(2026)
        for x in (0, 1):
            o = "Random"
            prof = [None, None]; prof[x] = ctx.blueprint[x]; prof[1 - x] = ctx.profiles[o][1 - x]
            tab = aivat.AivatTables(tg, x, "chance+x").table(ctx.blueprint[x], ctx.v_ref(x))
            terms = np.array([tg.sample_hand(prof, rng)[0] for _ in range(n_mc)])
            raw, av = tg.term_util[terms, x], tab[terms]
            exact = tg.values(prof)[x]
            rec = {"game": name, "seat": x, "opponent": o, "n": n_mc, "exact_ev": exact,
                   "raw_mean": raw.mean(), "raw_se": raw.std(ddof=1) / np.sqrt(n_mc),
                   "aivat_mean": av.mean(), "aivat_se": av.std(ddof=1) / np.sqrt(n_mc),
                   "sample_vr": raw.var(ddof=1) / av.var(ddof=1)}
            rec["aivat_z"] = (rec["aivat_mean"] - exact) / rec["aivat_se"]
            rec["raw_z"] = (rec["raw_mean"] - exact) / rec["raw_se"]
            out["monte_carlo"].append(rec)
            log(f"V8 MC {name} seat {x} Nash vs Random, n={n_mc}: exact {exact:+.4f} | raw "
                f"{rec['raw_mean']:+.4f} ± {1.96 * rec['raw_se']:.4f} | AIVAT {rec['aivat_mean']:+.4f} ± "
                f"{1.96 * rec['aivat_se']:.4f} | sample VR {rec['sample_vr']:.1f}")
    for name, target in (("kuhn", 5.0), ("leduc", 10.0)):
        rows = [r for r in out["exact"] if r["game"] == name]
        vr = np.array([r["vr_chance+x"] for r in rows])
        out[f"{name}_summary"] = {"target_vr": target, "n_pairs": len(rows),
                                  "vr_min": float(vr.min()), "vr_median": float(np.median(vr)),
                                  "vr_max": float(vr.max()), "n_meeting_target": int((vr >= target).sum()),
                                  "max_abs_bias": float(max(abs(r["bias_chance+x"]) for r in rows)),
                                  "vr_chance_only_median": float(np.median([r["vr_chance"] for r in rows])),
                                  "vr_full_median": float(np.median([r["vr_chance+x+y"] for r in rows]))}
        s = out[f"{name}_summary"]
        log(f"V8 {name}: AIVAT (chance+x) variance reduction min {s['vr_min']:.1f} median "
            f"{s['vr_median']:.1f} max {s['vr_max']:.1f}; {s['n_meeting_target']}/{s['n_pairs']} "
            f"pairs >= {target}x; max |bias| {s['max_abs_bias']:.1e}; chance-only median "
            f"{s['vr_chance_only_median']:.1f}; both-known median {s['vr_full_median']:.1f}")
    OUT["V8_aivat"] = out


if __name__ == "__main__":
    v1_openspiel_nashconv()
    v2_chapter7()
    v3_chapter3()
    v4_game_values()
    v5_chapter8()
    v6_population()
    v7_spinning_top()
    v8_aivat()
    OUT["runtime_seconds"] = time.time() - T0
    with open(os.path.join(deps.RESULTS_DIR, "validation.json"), "w", encoding="utf-8") as fh:
        json.dump(OUT, fh, indent=1, default=float)
    log(f"done in {OUT['runtime_seconds']:.1f} s -> results/validation.json")
