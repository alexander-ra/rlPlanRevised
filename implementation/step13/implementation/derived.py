"""
derived.py -- small numbers the chapter quotes that are computed FROM saved results (no data
loading, no training). Output: results/derived.json.

    python derived.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parent / "results"


def main():
    out = {}
    # collusion: detection at the null 99th-percentile threshold, by heads-up sample size
    for name in ("collusion.json", "collusion_mw.json"):
        d = json.load(open(R / name))
        thr = d["null"]["union"]["q99"]
        res = {"threshold_union_null_q99": thr}
        for cfg in d["runs"][next(iter(d["runs"]))]:
            rows = [p for s in d["runs"] for p in d["runs"][s][cfg]["pos_detail"]]
            hu = np.array([p["hu"] for p in rows])
            det = np.array([p["detected_at_null_q99"] for p in rows])
            clean = np.array([p["clean_union"] for p in rows])
            med = float(np.median(hu))
            res[cfg] = {"pairs": int(len(rows)), "median_hu": med,
                        "detected_share_hu_le_median": float(det[hu <= med].mean()),
                        "detected_share_hu_gt_median": float(det[hu > med].mean()),
                        "detected_share_all": float(det.mean()),
                        "clean_version_above_threshold": float((clean > thr).mean())}
        out[name.replace(".json", "")] = res
    # bot detection: Pluribus's rank on the player-level randomisation index (>= 400 decisions)
    b = json.load(open(R / "botdetect.json"))
    rnd = {k: v for k, v in b["randomisation"].items() if v[1] >= 400}
    order = sorted(rnd, key=lambda k: -rnd[k][0])
    out["randomisation"] = {"players_ge_400_grouped_decisions": len(rnd),
                            "pluribus_rank": order.index("Pluribus") + 1,
                            "pluribus": rnd["Pluribus"][0],
                            "max_human": max(v[0] for k, v in rnd.items() if k != "Pluribus"),
                            "median_human": float(np.median([v[0] for k, v in rnd.items() if k != "Pluribus"]))}
    g = b["size_granularity"]["pluribus_table"]
    hum = [v for k, v in g.items() if k != "Pluribus" and v == v]
    out["size_granularity"] = {"pluribus": g["Pluribus"], "humans_min": min(hum), "humans_max": max(hum),
                               "humans_n": len(hum)}
    loss = b["by_B"]["250"]["decision_loss_by_player_seed0"]
    hl = [v for k, v in loss.items() if k != "Pluribus"]
    out["decision_loss_B250_seed0"] = {"pluribus": loss["Pluribus"], "humans_min": min(hl),
                                       "humans_max": max(hl),
                                       "pluribus_rank_lowest_first": sorted(loss.values()).index(loss["Pluribus"]) + 1,
                                       "players": len(loss)}
    # behavioural cloning: seed-mean accuracy by group, and gain over the majority baseline
    bc = json.load(open(R / "bc.json"))
    seeds = list(bc["runs"])
    grp = {}
    for g in ("by_street", "by_position", "by_quadrant"):
        grp[g] = {}
        for k in bc["majority"][g]:
            maj = bc["majority"][g][k]["acc"]
            m = float(np.mean([bc["runs"][s]["mlp"][g][k]["acc"] for s in seeds]))
            ms = float(np.mean([bc["runs"][s]["mlp+stats"][g][k]["acc"] for s in seeds]))
            grp[g][k] = {"majority": maj, "mlp": m, "mlp_stats": ms,
                         "mlp_gain_pts": 100 * (m - maj), "mlp_stats_gain_pts": 100 * (ms - maj),
                         "style_gain_pts": 100 * (ms - m), "n": bc["majority"][g][k]["n"]}
    out["bc_groups_seed_mean"] = grp
    rnd_all = [v[0] for k, v in b["randomisation"].items() if v[1] >= 400 and k != "Pluribus"]
    out["randomisation"]["min_human"] = min(rnd_all)
    json.dump(out, open(R / "derived.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
