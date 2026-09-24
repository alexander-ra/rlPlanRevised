"""
zoo_sanity.py -- Phase 2, Day 2: the plan's sanity checks on the stationary bot zoo, exactly
(no sampling): "Nash should be approximately unexploitable, random should lose to everyone,
always-fold should lose even more" (raw step 14, Day 2).

    python zoo_sanity.py        ~5 s

Prints each stationary agent's exploitability (NashConv/2) and population return, and which
agents Random beats. Saves figures/zoo_sanity.json.
"""

from __future__ import annotations

import json
import os

import numpy as np

import _bootstrap  # noqa: F401
import zoo

out = {}
for game in ("kuhn", "leduc"):
    ctx = zoo.context(game)
    tg, names = ctx.tg, ctx.stationary_names
    n = len(names)
    M = np.zeros((n, n))
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            M[i, j] = 0.5 * (tg.values([ctx.profiles[a][0], ctx.profiles[b][1]])[0]
                             + tg.values([ctx.profiles[b][0], ctx.profiles[a][1]])[1])
    expl = {a: tg.nash_conv(ctx.profiles[a])["exploitability"] for a in names}
    popret = {a: float(np.mean(np.delete(M[i], i))) for i, a in enumerate(names)}
    r = names.index("Random")
    beaten_by_random = [names[j] for j in range(n) if j != r and M[r, j] > 0]
    print(f"\n[{game}]  agent            exploitability  population return")
    for a in sorted(names, key=lambda x: expl[x]):
        print(f"          {a:15s}  {expl[a]:13.4f}  {popret[a]:+.4f}")
    print(f"  Nash exploitability {expl['Nash']:.2e} (want ~0)")
    print(f"  Random beats: {beaten_by_random or 'nobody'}  (the plan predicted: nobody)")
    worst = min(popret, key=popret.get)
    print(f"  lowest population return: {worst}")
    out[game] = {"exploitability": expl, "population_return": popret,
                 "random_beats": beaten_by_random, "lowest_population_return": worst}
with open(os.path.join(_bootstrap.FIG, "zoo_sanity.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
