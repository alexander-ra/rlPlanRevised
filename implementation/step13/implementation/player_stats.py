"""
player_stats.py -- PokerTracker-style player statistics with minimum-sample thresholds, their
sampling reliability, the VPIP x PFR map, and the frequency gap to a strong reference (raw step
13, Day 2 "PlayerStatistics"; Day 5-6 "gap between real behaviour and GTO play").

    python player_stats.py          # -> results/player_stats.json

WHAT IS MEASURED
----------------
* stats(): every statistic as count / opportunities (a player's 3-bet % is 3-bets over the times
  they faced exactly one raise, not over all hands).
* reliability(): split-half test-retest correlation of each statistic at m hands per half, over
  players with >= 2m hands, for m = 25 ... 1000 (3 seeds). The hands needed for r >= 0.8 is the
  data-driven minimum sample (the plan asserts 500+ hands; this checks it per statistic).
* quadrants(): the classic VPIP x PFR map with the plan's thresholds (see QUADRANT RULE).
* gap(): the frequency gap to Pluribus in 6-handed play, position by position. Pluribus is not an
  equilibrium; it is the strongest six-player reference with public hands, and a gap in
  frequencies says where an exploiter would look, not how much it would earn.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CACHE_ROOT, MIN_HANDS_PLAYER, MIN_OPP, RESULTS, SEEDS  # noqa: E402

# name -> (numerator column, denominator column or "hands")
STATS = {
    "vpip": ("vpip", "hands"), "pfr": ("pfr", "hands"), "limp": ("limp", "hands"),
    "rfi": ("rfi", "rfi_opp"), "steal": ("steal", "steal_opp"),
    "three_bet": ("tb", "tb_opp"), "fold_to_3bet": ("f3b", "f3b_opp"),
    "cbet": ("cbet", "cbet_opp"), "fold_to_cbet": ("fcb", "fcb_opp"),
    "donk": ("donk", "donk_opp"), "check_raise": ("cr", "cr_opp"),
    "wtsd": ("wtsd", "saw_flop"), "afq": ("post_br", "post_act"),
    "af": ("post_br", "post_call"), "saw_flop": ("saw_flop", "hands"),
}
# the style vector used for clustering / comparison with the embedding
STYLE = ["vpip", "pfr", "three_bet", "steal", "limp", "cbet", "fold_to_cbet", "wtsd", "afq",
         "check_raise", "fold_to_3bet", "post_size"]
# QUADRANT RULE (plan: tight < 20 %, loose > 35 %, passive PFR < VPIP/2). The loose/tight line is
# drawn at the midpoint 27.5 % so every player lands in one of four quadrants.
LOOSE_AT = 0.275
AGGR_RATIO = 0.5


def load(source: str):
    d = np.load(CACHE_ROOT / source / "seats.npz")
    I, F = d["I"], d["F"]
    ci = {k: i for i, k in enumerate(d["icols"])}
    cf = {k: i for i, k in enumerate(d["fcols"])}
    names = json.load(open(CACHE_ROOT / source / "players.json"))
    return I, F, ci, cf, names


def sums(I, F, ci, cf, rows=None, n_players=None):
    """Per-player sums of every count column (+ 'hands', 'post_act', 'post_size')."""
    if rows is not None:
        I, F = I[rows], F[rows]
    pid = I[:, ci["pid"]]
    m = n_players or int(pid.max()) + 1
    out = {"hands": np.bincount(pid, minlength=m).astype(float)}
    for k, j in ci.items():
        if k in ("hand", "pid", "seat", "pos", "n"):
            continue
        out[k] = np.bincount(pid, weights=I[:, j], minlength=m)
    for k, j in cf.items():
        out[k] = np.bincount(pid, weights=F[:, j], minlength=m)
    out["post_act"] = out["post_br"] + out["post_call"] + out["post_fold"]
    return out


def stats(S: dict, min_opp: bool = True) -> dict:
    """name -> (value array with NaN where below threshold, opportunities array)."""
    out = {}
    for name, (num, den) in STATS.items():
        d = S[den]
        with np.errstate(invalid="ignore", divide="ignore"):
            v = S[num] / d
        if min_opp and name in MIN_OPP:
            v = np.where(d >= MIN_OPP[name], v, np.nan)
        out[name] = (v, d)
    with np.errstate(invalid="ignore", divide="ignore"):
        ps = S["post_size_sum"] / S["post_size_n"]
    out["post_size"] = (np.where(S["post_size_n"] >= 30, ps, np.nan), S["post_size_n"])
    with np.errstate(invalid="ignore", divide="ignore"):
        out["bb100_nosd"] = (100 * S["won_nosd"] / S["hands"], S["hands"])
    return out


def style_matrix(st: dict, players: np.ndarray) -> np.ndarray:
    return np.stack([st[k][0][players] for k in STYLE], axis=1)


def reliability(I, F, ci, cf, seeds=SEEDS, ms=(25, 50, 100, 200, 500, 1000)) -> dict:
    """Split-half test-retest correlation of each statistic at m hands per half."""
    pid = I[:, ci["pid"]]
    order = np.argsort(pid, kind="stable")
    counts = np.bincount(pid)
    starts = np.concatenate([[0], np.cumsum(counts)])
    res = {}
    for m in ms:
        elig = np.where(counts >= 2 * m)[0]
        per_seed = []
        for s in seeds:
            rng = np.random.default_rng(1000 + s)
            ra, rb = [], []
            for p in elig:
                rows = order[starts[p]:starts[p + 1]]
                pick = rng.choice(rows, 2 * m, replace=False)
                ra.append(pick[:m]); rb.append(pick[m:])
            ra, rb = np.concatenate(ra), np.concatenate(rb)
            Sa = stats(sums(I, F, ci, cf, ra, int(pid.max()) + 1), min_opp=False)
            Sb = stats(sums(I, F, ci, cf, rb, int(pid.max()) + 1), min_opp=False)
            rr = {}
            for k in STYLE + ["af"]:
                a, b = Sa[k][0][elig], Sb[k][0][elig]
                if k == "af":
                    a, b = np.log1p(a), np.log1p(b)
                ok = np.isfinite(a) & np.isfinite(b)
                rr[k] = float(np.corrcoef(a[ok], b[ok])[0, 1]) if ok.sum() > 20 else None
            per_seed.append(rr)
        res[m] = {"players": int(len(elig)),
                  "r": {k: _mean_se([d[k] for d in per_seed]) for k in per_seed[0]}}
        print(f"  reliability m={m}: players={len(elig)} vpip={res[m]['r']['vpip']} "
              f"3bet={res[m]['r']['three_bet']}", flush=True)
    return res


def _mean_se(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None
    a = np.array(xs)
    return [float(a.mean()), float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else 0.0]


def quadrant(vpip, pfr):
    loose = vpip >= LOOSE_AT
    aggr = pfr >= AGGR_RATIO * vpip
    return np.where(loose & aggr, "LAG", np.where(loose, "loose-passive",
                    np.where(aggr, "TAG", "tight-passive")))


def position_profile(I, ci, rows) -> dict:
    """6-handed pre-flop profile: raise-first-in % by position, 3-bet %, c-bet %, and counts."""
    X = I[rows]
    prof = {}
    for code, name in [(3, "LJ"), (4, "HJ"), (5, "CO"), (6, "BTN"), (0, "SB")]:
        m = X[:, ci["pos"]] == code
        opp = X[m, ci["rfi_opp"]].sum()
        prof[f"rfi_{name}"] = (float(X[m, ci["rfi"]].sum() / max(opp, 1)), int(opp))
    m = X[:, ci["pos"]] == 1
    prof["vpip_BB"] = (float(X[m, ci["vpip"]].mean()) if m.any() else np.nan, int(m.sum()))
    for k, (num, den) in {"three_bet": ("tb", "tb_opp"), "cbet": ("cbet", "cbet_opp"),
                          "fold_to_cbet": ("fcb", "fcb_opp")}.items():
        o = X[:, ci[den]].sum()
        prof[k] = (float(X[:, ci[num]].sum() / max(o, 1)), int(o))
    prof["vpip"] = (float(X[:, ci["vpip"]].mean()), int(len(X)))
    prof["pfr"] = (float(X[:, ci["pfr"]].mean()), int(len(X)))
    return prof


def gap(I_ipn, ci_i, I_plu, ci_p, names_plu, min_hands=500) -> dict:
    """Per-player gap to Pluribus's 6-handed profile, for IPN regulars and for the pros."""
    plu_id = names_plu.index("Pluribus")
    ref_rows = np.where(I_plu[:, ci_p["pid"]] == plu_id)[0]
    ref = position_profile(I_plu, ci_p, ref_rows)
    keys = list(ref)

    def groups(I, ci):
        r6 = np.where(I[:, ci["n"]] == 6)[0]
        pid = I[r6, ci["pid"]]
        o = np.argsort(pid, kind="stable")
        r6, pid = r6[o], pid[o]
        u, st = np.unique(pid, return_index=True)
        en = np.append(st[1:], len(pid))
        return {int(p): r6[a:b] for p, a, b in zip(u, st, en) if b - a >= min_hands}

    G = {"ipn": groups(I_ipn, ci_i), "plu": groups(I_plu, ci_p)}

    def one(I, ci, pid):
        rows = G["ipn" if I is I_ipn else "plu"].get(int(pid))
        if rows is None:
            return None
        p = position_profile(I, ci, rows)
        # binomial SE of the reference makes the gap a z-like distance; keep the plain one too
        d = {k: p[k][0] - ref[k][0] for k in keys if p[k][1] >= 30}
        return {"n6": int(len(rows)), "diff": d, "profile": {k: p[k][0] for k in keys},
                "mean_abs_gap": float(np.mean(np.abs(list(d.values()))))}

    ipn_pids = list(G["ipn"])
    ipn = {}
    for pid in ipn_pids:
        r = one(I_ipn, ci_i, pid)
        if r:
            ipn[int(pid)] = r
    pros = {}
    for pid, name in enumerate(names_plu):
        if name == "Pluribus":
            continue
        r = one(I_plu, ci_p, pid)
        if r:
            pros[name] = r
    return {"reference": {k: list(v) for k, v in ref.items()}, "ipn": ipn, "pros": pros}


def main():
    I, F, ci, cf, names = load("IPN100")
    S = sums(I, F, ci, cf)
    st = stats(S)
    hands = S["hands"]
    regs = np.where(hands >= MIN_HANDS_PLAYER)[0]
    print(f"IPN100: {len(names)} players, {len(regs)} with >= {MIN_HANDS_PLAYER} hands", flush=True)
    out = {"min_hands": MIN_HANDS_PLAYER, "min_opp": MIN_OPP, "n_regulars": int(len(regs))}
    # distributions over regulars
    dist = {}
    for k in list(STATS) + ["post_size", "bb100_nosd"]:
        v = st[k][0][regs]
        v = v[np.isfinite(v)]
        dist[k] = {"n": int(len(v)), "q10": float(np.quantile(v, .1)), "median": float(np.median(v)),
                   "q90": float(np.quantile(v, .9)), "mean": float(v.mean())}
    out["distribution_regulars"] = dist
    # W$SD coverage (showdown cards are mostly unknown in HandHQ)
    with np.errstate(invalid="ignore", divide="ignore"):
        cover = S["wsd_known"][regs] / S["wtsd"][regs]
    out["wsd_coverage_median"] = float(np.nanmedian(cover))
    # quadrants
    q = quadrant(st["vpip"][0][regs], st["pfr"][0][regs])
    u, c = np.unique(q, return_counts=True)
    out["quadrants"] = {str(a): int(b) for a, b in zip(u, c)}
    out["quadrant_rule"] = {"loose_at_vpip": LOOSE_AT, "aggressive_if_pfr_ge_vpip_times": AGGR_RATIO}
    # per-player table for downstream scripts (regulars only, style vector)
    X = style_matrix(st, regs)
    np.savez(CACHE_ROOT / "IPN100" / "style_regulars.npz", pids=regs, X=X, cols=np.array(STYLE),
             hands=hands[regs], vpip=st["vpip"][0][regs], pfr=st["pfr"][0][regs],
             af=st["af"][0][regs])
    out["style_complete_rows"] = int(np.isfinite(X).all(1).sum())
    # scatter data for the figure (regulars)
    out["scatter"] = {"vpip": st["vpip"][0][regs].round(4).tolist(),
                      "pfr": st["pfr"][0][regs].round(4).tolist(),
                      "hands": hands[regs].astype(int).tolist()}
    # reliability
    out["reliability"] = reliability(I, F, ci, cf)
    # Pluribus table: per-player stats
    Ip, Fp, cip, cfp, names_p = load("PLURIBUS")
    Sp = sums(Ip, Fp, cip, cfp)
    stp = stats(Sp, min_opp=False)
    out["pluribus_table"] = {names_p[p]: {k: (float(stp[k][0][p]) if np.isfinite(stp[k][0][p]) else None)
                                          for k in STYLE + ["af", "donk"]} | {"hands": int(Sp["hands"][p])}
                             for p in range(len(names_p))}
    # gap to Pluribus (6-handed only)
    g = gap(I, ci, Ip, cip, names_p)
    ipn_gaps = np.array([v["mean_abs_gap"] for v in g["ipn"].values()])
    pro_gaps = np.array([v["mean_abs_gap"] for v in g["pros"].values()])
    out["gap"] = {
        "reference_pluribus_6h": g["reference"],
        "ipn_players": int(len(ipn_gaps)),
        "ipn_mean_abs_gap": {"median": float(np.median(ipn_gaps)), "q10": float(np.quantile(ipn_gaps, .1)),
                             "q90": float(np.quantile(ipn_gaps, .9))},
        "pros_mean_abs_gap": {k: v["mean_abs_gap"] for k, v in g["pros"].items()},
        "pros_median": float(np.median(pro_gaps)),
        "ipn_per_stat_median_diff": {k: float(np.median([v["diff"][k] for v in g["ipn"].values()
                                                         if k in v["diff"]]))
                                     for k in g["reference"]},
        "pros_per_stat_median_diff": {k: float(np.median([v["diff"][k] for v in g["pros"].values()
                                                          if k in v["diff"]]))
                                      for k in g["reference"]},
        "ipn_share_closer_than_median_pro": float((ipn_gaps < np.median(pro_gaps)).mean()),
    }
    json.dump(out, open(RESULTS / "player_stats.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("n_regulars", "quadrants", "wsd_coverage_median")}))
    print(json.dumps(out["gap"], indent=1)[:3000])


if __name__ == "__main__":
    main()
