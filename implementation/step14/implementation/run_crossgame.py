"""
run_crossgame.py -- assemble the cross-game comparison and the failure-mode summary from the
saved results (no simulation; deterministic).

    python run_crossgame.py   -> results/crossgame.json

Reads validation.json, population_{kuhn,leduc}.json, adaptation_{kuhn,leduc}.json,
approx_br_{kuhn,leduc}.json, nplayer_kuhn3.json, sls.json and (if present)
bridge13_pluribus.json.
"""

from __future__ import annotations

import json
import os

import numpy as np

import deps
from logutil import Logger


def load(name):
    p = os.path.join(deps.RESULTS_DIR, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    log = Logger("crossgame")
    V = load("validation.json")
    P = {g: load(f"population_{g}.json") for g in ("kuhn", "leduc")}
    A = {g: load(f"adaptation_{g}.json") for g in ("kuhn", "leduc")}
    B = {g: load(f"approx_br_{g}.json") for g in ("kuhn", "leduc")}
    N = load("nplayer_kuhn3.json")
    S = load("sls.json")
    Br = load("bridge13_pluribus.json")
    out = {}

    # ---------------- agent profiles (the joint protocol), two-player games
    prof = {}
    for g in ("kuhn", "leduc"):
        rows = {}
        pa = P[g]["analysis"]["2000"]
        names = P[g]["agents"]
        for a, blk in A[g]["agents"].items():
            st = blk["stationary"]
            teach = [v["loss_after_switch"]["mean"] for v in blk["teach"].values()]
            sw = list(blk["switch"].values())
            i = names.index(a)
            rows[a] = {
                "gain": st["population_gain"]["mean"], "gain_ci95": st["population_gain"]["ci95"],
                "capture": st["final_capture"]["mean"],
                "h50_median": st["h50"].get("median"), "h50_reached": st["h50_reached_share"],
                "r50_median": float(np.nanmedian([x["r50"].get("median") if x["r50"].get("median") is not None else np.nan for x in sw])) if sw else None,
                "switch_cost": float(np.mean([x["switch_cost"]["mean"] for x in sw])),
                "exposure_mean": st["exposure_mean"]["mean"], "exposure_max": st["exposure_max"]["mean"],
                "teach_loss_mean": float(np.mean(teach)), "teach_loss_max": float(np.max(teach)),
                "exploitability_ranking_value": pa["exploitability"][i],
                "elo": pa["elo"][i], "nash_avg_skill": pa["nash_avg_skill"][i],
                "nash_avg_p": pa["nash_avg_p"][i], "vase_iml_rank": pa["iml_rank"][i],
                "alpharank_a0.1": pa["alpharank"]["0.1"][i], "alpharank_a100": pa["alpharank"]["100.0"][i],
                "population_return": pa["population_return"][i],
                "rrps_within_pop_expl": pa["within_pop_exploitability"][i],
                "rrps_aggregate": pa["rrps_aggregate"][i],
            }
        prof[g] = rows
    out["profiles_2p"] = prof

    # ---------------- failure mode 1: exploitability can only punish adaptation
    fm1 = {}
    for g in ("kuhn", "leduc"):
        r = prof[g]
        fm1[g] = {a: {"gain": r[a]["gain"], "exposure": r[a]["exposure_mean"],
                      "teach_loss": r[a]["teach_loss_mean"]} for a in r}
        order_expl = sorted(r, key=lambda a: r[a]["exposure_mean"])
        order_gain = sorted(r, key=lambda a: -r[a]["gain"])
        fm1[g]["order_by_exposure"] = order_expl
        fm1[g]["order_by_gain"] = order_gain
    out["fm1"] = fm1

    # ---------------- failure mode 3: approximate best responses are lower bounds
    fm3 = {}
    for g in ("kuhn", "leduc"):
        t = B[g]["targets"]
        fm3[g] = {k: {"exact": v["exact_exploitability"],
                      **{f"ratio_{b}": v["by_budget"][str(b)]["ratio"] for b in (1000, 10000, 100000)}}
                  for k, v in t.items() if v["exact_exploitability"] > 1e-3}
        fm3[g]["online_learner"] = B[g]["online_learner"]
        fm3[g]["white_box_teach_loss"] = {a: prof[g][a]["teach_loss_mean"] for a in prof[g]}
    out["fm3"] = fm3

    # ---------------- failure mode 4: rankings
    fm4 = {}
    for g in ("kuhn", "leduc"):
        d = P[g]
        names = d["agents"]
        a = d["analysis"]["2000"]
        def top(key, scores):
            return names[int(np.argmax(scores))]
        ar = {al: top("ar", a["alpharank"][al]) for al in a["alpharank"]}
        clone = d["clone_test"]
        rows = clone["rows"]
        ref = names.index("Nash")
        gaps = {x: [r["elo"][names.index(x)] - r["elo"][ref] for r in rows] for x in ("DirBR", "RNR(0.5)", "BestEq")}
        na_inv = max(abs(r["nash_avg_skill"][i] - rows[0]["nash_avg_skill"][i]) for r in rows for i in range(len(names)))
        horizon = {}
        for h in d["horizons"]:
            ah = d["analysis"][str(h)]
            horizon[str(h)] = {"elo_top": names[int(np.argmax(ah["elo"]))],
                               "popret_top": names[int(np.argmax(ah["population_return"]))],
                               "alpharank_a10_top": names[int(np.argmax(ah["alpharank"]["10.0"]))],
                               "elo_rank_of": {x: int(ah["ranks"]["elo"][names.index(x)]) for x in d["adaptive"] + ["Nash"]}}
        boot = d["bootstrap_ranks"]
        stab = {k: {"top_agent_share": float(np.mean([np.argmin(r) == np.argmin(boot[k][0]) for r in boot[k]])),
                    "mean_rank_sd": float(np.mean(np.std(np.asarray(boot[k]), axis=0)))} for k in boot}
        fm4[g] = {"elo_top": names[int(np.argmax(a["elo"]))], "popret_top": names[int(np.argmax(a["population_return"]))],
                  "nash_avg_support": {names[i]: p for i, p in enumerate(a["nash_avg_p"]) if p > 1e-3},
                  "vase_top": [names[i] for i in range(len(names)) if a["iml_rank"][i] == 0],
                  "alpharank_top_by_alpha": ar,
                  "rrps_top": names[int(np.argmax(a["rrps_aggregate"]))],
                  "clone": clone["clone"], "elo_gap_to_nash_by_k": gaps,
                  "nash_avg_skill_max_change_with_clones": na_inv,
                  "kendall_tau": a["kendall_tau"], "horizon": horizon, "bootstrap_stability": stab,
                  "transitive_ratio": a["transitive_ratio"]}
    out["fm4"] = fm4

    # ---------------- failure mode 5
    out["fm5"] = {g: A[g]["fm5"] for g in ("kuhn", "leduc")}
    out["fm5"]["aivat_validation"] = {g: V["V8_aivat"][f"{g}_summary"] for g in ("kuhn", "leduc")}
    if Br:
        out["fm5"]["pluribus_raw"] = Br["players"].get("Pluribus")

    # ---------------- failure mode 9: LLM-derived strategies (Kuhn)
    d = P["kuhn"]; names = d["agents"]; a = d["analysis"]["2000"]
    fm9 = {}
    for x in ("LLM-Qwen7B", "LLM-GPT20B", "LLM-OT7B", "Nash", "Threshold"):
        i = names.index(x)
        fm9[x] = {"elo": a["elo"][i], "elo_rank": int(a["ranks"]["elo"][i]),
                  "exploitability": a["exploitability"][i], "expl_rank": int(a["ranks"]["exploitability"][i]),
                  "population_return": a["population_return"][i]}
    out["fm9"] = fm9

    # ---------------- N-player
    np_ = N["part3"]["protocol"]
    out["nplayer"] = {
        "equilibria": {k: {"nash_conv": v["nash_conv"], "values": v["values"], "coalition_value": v["coalition_value"]}
                       for k, v in N["part1"]["equilibria"].items()},
        "crossplay_nash_conv_max": N["part1"]["crossplay_nash_conv_max"],
        "crossplay_value_range": N["part1"]["crossplay_value_range"],
        "protocol": {a: {"gain": v["gain"]["mean"], "gain_ci95": v["gain"]["ci95"],
                         "capture": v["final_capture"]["mean"], "h50_median": v["h50"]["median"],
                         "r50_median": v["switch_r50"]["median"], "switch_cost": v["switch_cost"]["mean"],
                         "vs_fixed_colluders": v["colluders_mean_ev"]["mean"],
                         "teach_before": v["teach_ev_before"]["mean"], "teach_after": v["teach_ev_after"]["mean"],
                         "coalition_value_final": v["coalition_value_final_policy"]["mean"]} for a, v in np_.items()},
        "population": {"agents": N["part2"]["agents"], "population_return": N["part2"]["population_return"],
                       "vase_iml_rank": N["part2"]["vase_iml_rank"], "transitive_ratio": N["part2"]["transitive_ratio"],
                       "alpharank_top": {k: v["top_profile"] for k, v in N["part2"]["alpharank_multipop"].items()},
                       "elo_from_rankings": N["part2"]["elo_from_rankings"],
                       "nash_avg_p": N["part2"]["nash_avg_p"]},
        "does_not_extend": N["does_not_extend"]}

    # ---------------- SLS
    out["sls"] = {"transitive_ratio": S["layer2"]["transitive_ratio"], "elo": S["layer2"]["elo"],
                  "agents": S["layer2"]["agents"], "nash_avg_p": S["layer2"]["nash_avg_p"],
                  "alpharank": S["layer2"]["alpharank"],
                  "coalition_probe": {k: {"independent": v["independent"]["mean"], "independent_ci95": v["independent"]["ci95"],
                                          "alliance": v["alliance"]["mean"], "alliance_ci95": v["alliance"]["ci95"],
                                          "drop": v["exposure"]} for k, v in S["coalition_probe"].items()}}

    # ---------------- the cross-game table (what the unchanged protocol reports)
    def g2(g, a):
        r = prof[g][a]
        return {"gain": r["gain"], "gain_ci95": r["gain_ci95"], "capture": r["capture"], "h50": r["h50_median"],
                "r50": r["r50_median"], "exposure": r["exposure_mean"], "teach_loss": r["teach_loss_mean"]}
    table = {"kuhn": {k: g2("kuhn", k) for k in ("Nash", "DirBR", "RNR(0.5)", "BestEq")},
             "leduc": {k: g2("leduc", k) for k in ("Nash", "DirBR", "RNR(0.5)", "BestEq")},
             "kuhn3": {k: {"gain": v["gain"], "gain_ci95": v["gain_ci95"], "capture": v["capture"],
                           "h50": v["h50_median"], "r50": v["r50_median"],
                           "coalition_value": v["coalition_value_final"],
                           "teach_after": v["teach_after"]} for k, v in out["nplayer"]["protocol"].items()}}
    out["crossgame_table"] = table
    with open(os.path.join(deps.RESULTS_DIR, "crossgame.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=float)
    log("-> results/crossgame.json")
    for g in ("kuhn", "leduc"):
        log(f"[{g}] FM4 top by method: Elo {fm4[g]['elo_top']}, population return {fm4[g]['popret_top']}, "
            f"RRPS {fm4[g]['rrps_top']}, VasE {fm4[g]['vase_top']}, Nash-avg support {fm4[g]['nash_avg_support']}, "
            f"alpha-Rank {fm4[g]['alpharank_top_by_alpha']}")
        log(f"[{g}] FM4 bootstrap stability: {fm4[g]['bootstrap_stability']}")
        log(f"[{g}] FM4 Elo gap to Nash with k clones of {fm4[g]['clone']}: " +
            ", ".join(f"{k}: {v[0]:+.0f}->{v[-1]:+.0f}" for k, v in fm4[g]['elo_gap_to_nash_by_k'].items()) +
            f"; Nash-avg skill max change {fm4[g]['nash_avg_skill_max_change_with_clones']:.1e}")
        log(f"[{g}] FM4 horizon: " + "; ".join(f"H={h}: Elo top {v['elo_top']}" for h, v in fm4[g]['horizon'].items()))


if __name__ == "__main__":
    main()
