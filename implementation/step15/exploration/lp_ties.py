"""
lp_ties.py -- exploration: which equilibrium does the "best equilibrium" LP return when many are
equally good against the model?  (~20 s)

    python lp_ties.py

Against a model that is itself an equilibrium, every equilibrium of player 1 in Kuhn poker is
optimal, so the LP's answer is decided by the solver's tie-breaking. This script prints the
strategy HiGHS returns, the strategy returned when ties are broken toward the CFR+ blueprint
(safe_agents.floor_tiebreak), and what each earns against 300 of Ganzfried & Sandholm's
"sophisticated" opponents (each probability within 0.2 of the equilibrium) and with the true
opponent as the model. It is the check behind surprise 1 in EXECUTION_NOTES.md.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "implementation"))
import boot  # noqa: E402,F401
import zoo  # noqa: E402
from safe_agents import floor_tiebreak  # noqa: E402
from run_gs_table import opponent_profile  # noqa: E402


def main():
    ctx = zoo.context("kuhn")
    tg, lp, v = ctx.tg, ctx.lps[0], ctx.v_star[0]
    names = tg.players[0].infoset_strings
    eq_model = ctx.blueprint[1]
    x_raw = lp.floor(eq_model, v - 1e-7, fill=ctx.blueprint[0])[0]
    x_tb = floor_tiebreak(lp, eq_model, v - 1e-7, ctx.blueprint[0], fill=ctx.blueprint[0])
    print("P(bet) at player 1's information sets:", names)
    print("  blueprint (CFR+)        ", np.round(ctx.blueprint[0][:, 1], 3))
    print("  HiGHS vertex, eq. model ", np.round(x_raw[:, 1], 3))
    print("  tie-broken, eq. model   ", np.round(x_tb[:, 1], 3))
    rows = {"blueprint": [], "HiGHS vertex": [], "tie-broken": [], "best eq, true model": []}
    for i in range(300):
        B1 = opponent_profile(ctx, "sophisticated", i)[1]
        rows["blueprint"].append(tg.values([ctx.blueprint[0], B1])[0])
        rows["HiGHS vertex"].append(tg.values([x_raw, B1])[0])
        rows["tie-broken"].append(tg.values([x_tb, B1])[0])
        xt = lp.floor(B1, v - 1e-7, fill=ctx.blueprint[0])[0]
        rows["best eq, true model"].append(tg.values([xt, B1])[0])
    print("Mean EV against 300 sophisticated opponents (v* = %.4f):" % v)
    for k, vals in rows.items():
        print(f"  {k:22s} {np.mean(vals):+.4f}")


if __name__ == "__main__":
    main()
