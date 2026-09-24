"""
run_bridge13.py -- optional bridge to Chapter 13: the confidence layer on real hand histories.

    python run_bridge13.py

Reads Chapter 13's parsed Pluribus hands (the 10 000 released six-player no-limit hold'em
hands, parsed by implementation/step13/build_dataset.py into D:/datasets/step13_cache/PLURIBUS;
Chapter 13 log: 10 000 of 10 000 hands parsed). For every player it reports the raw win rate in
milli-big-blinds per hand (mbb/hand) with a 95 % interval from the per-hand results -- the only
estimator available to a third party without the agents' strategies. Reference: Brown &
Sandholm (2019) report Pluribus at 48 +/- 25 mbb/game over these hands using AIVAT, which needs
Pluribus's strategy; no individual human's result reached significance.
"""

from __future__ import annotations

import json
import os

import numpy as np

import deps
from logutil import Logger

CACHE = os.environ.get("STEP13_CACHE", "D:/datasets/step13_cache")


def main():
    log = Logger("bridge13")
    path = os.path.join(CACHE, "PLURIBUS", "seats.npz")
    if not os.path.exists(path):
        log(f"Chapter 13 cache not found at {path}; bridge skipped")
        return
    d = np.load(path)
    icols = list(d["icols"]); fcols = list(d["fcols"])
    I, F = d["I"], d["F"]
    with open(os.path.join(CACHE, "PLURIBUS", "players.json"), encoding="utf-8") as fh:
        players = json.load(fh)
    pid = I[:, icols.index("pid")]
    resolved = I[:, icols.index("resolved")] == 1
    net = F[:, fcols.index("net")]
    out = {"source": "Chapter 13 cache, PLURIBUS seats.npz", "unit": "mbb per hand (net big blinds x 1000)",
           "rows": int(len(net)), "resolved_share": float(resolved.mean()), "players": {}}
    for k, name in enumerate(players):
        m = (pid == k) & resolved
        x = 1000.0 * net[m]
        if len(x) < 2:
            continue
        se = x.std(ddof=1) / np.sqrt(len(x))
        out["players"][name] = {"hands": int(len(x)), "mean": float(x.mean()), "ci95": float(1.96 * se),
                                "sd_per_hand": float(x.std(ddof=1)),
                                "hands_for_pm25": float((1.96 * x.std(ddof=1) / 25.0) ** 2)}
    for name, r in sorted(out["players"].items(), key=lambda kv: -kv[1]["hands"]):
        log(f"{name:9s} hands {r['hands']:6d}  raw {r['mean']:+7.1f} ± {r['ci95']:6.1f} mbb/hand  "
            f"(SD {r['sd_per_hand']:.0f}; hands for ±25: {r['hands_for_pm25']:.0f})")
    out["zero_sum_check_mbb"] = float(1000.0 * net[resolved].sum() / max(1, len(np.unique(I[resolved, icols.index('hand')]))))
    with open(os.path.join(deps.RESULTS_DIR, "bridge13_pluribus.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    log("-> results/bridge13_pluribus.json")


if __name__ == "__main__":
    main()
