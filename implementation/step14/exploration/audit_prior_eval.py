"""
audit_prior_eval.py -- Phase 2, Day 1: inventory the evaluation code written in Chapters 3-11
and check that each piece agrees with this chapter's single engine on a common input.

    python audit_prior_eval.py        (from implementation/step14/exploration/)  ~10 s

Prints one row per prior evaluator: what it computes, the value it returns, the value the
Chapter 14 engine returns for the same input, and whether they agree. Saves figures/audit.json.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

import _bootstrap  # noqa: F401
import deps
import trees
import zoo
import population as pop

rows = []


def row(chapter, what, theirs, mine, note=""):
    ok = abs(theirs - mine) < 1e-6
    rows.append({"chapter": chapter, "evaluator": what, "theirs": theirs, "mine": mine,
                 "agree": bool(ok), "note": note})
    print(f"{chapter:5s} {what:52s} {theirs:+.6f} {mine:+.6f} {'OK' if ok else 'DIFF'} {note}")


# Chapter 3 -- exploitability of Leduc CFR (its own trainer + evaluator)
step03 = os.path.join(deps.IMPL_ROOT, "step03")
sys.path.insert(0, step03)
from cfr.cfr_trainer import LeducTrainer                  # noqa: E402
from evaluate.exploitability import compute_exploitability  # noqa: E402
sys.path.remove(step03)
ctx = zoo.context("leduc")
tr = LeducTrainer(); tr.train(20)
theirs = compute_exploitability(tr.node_map)
prof = []
for p in (0, 1):
    P = ctx.tg.players[p]
    B = np.zeros((len(P.infoset_strings), ctx.tg.n_actions))
    for I, node in ctx.bridge.rep_node[p].items():
        n, legal = tr.node_map[ctx.bridge.g07.info_set(ctx.bridge.state07(node), p)]
        avg = n.get_average_strategy()
        for i, a in enumerate(legal):
            B[I, a] = avg[i]
    prof.append(ctx.tg.normalize(p, B))
row("Ch. 3", "Leduc CFR (20 it.) exploitability = NashConv/2", theirs, ctx.tg.nash_conv(prof)["exploitability"])

# Chapter 7 -- NashConv of a profile (exact best response on its own engine)
from best_response import nash_gap          # noqa: E402  (Step 07)
k = zoo.context("kuhn")
tp = k.types07["TightPassive"]
g = nash_gap(k.bridge.g07, tp, tp)["nash_conv"]
row("Ch. 7", "Kuhn NashConv(TightPassive self-play)", g,
    k.tg.nash_conv([k.bridge.materialize(tp, 0), k.bridge.materialize(tp, 1)])["nash_conv"])

# Chapter 8 -- worst-case value of a strategy (safety checker)
sys.path.append(deps.STEP08_IMPL)
from safety_checker import worst_case_value  # noqa: E402  (Step 08)
import solvers  # noqa: E402
row("Ch. 8", "Kuhn worst case of seat-0 LooseAggressive", worst_case_value(k.bridge.g07, k.types07["LooseAggressive"], 0),
    solvers.worst_case(k.tg, 0, k.bridge.materialize(k.types07["LooseAggressive"], 0)))

# Chapter 10 -- spinning top (Hodge) and Elo
st = deps.spinning_top()
rps = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float)
row("Ch. 10", "transitive ratio of RPS (Hodge)", st.transitive_ratio(rps), pop.transitive_ratio(rps))
elo10 = deps.load_by_path(os.path.join(deps.STEP10_IMPL, "elo.py"), "step10_elo")
S = np.array([[0.5, 0.75, 0.9], [0.25, 0.5, 0.75], [0.1, 0.25, 0.5]])
r10 = elo10.ratings_from_score_matrix(["A", "B", "C"], S, k=16, passes=300)
r14 = pop.elo_fit(S)
row("Ch. 10", "Elo gap A-C on a 3-agent ladder (online vs ML fit)", r10["A"] - r10["C"], r14[0] - r14[2],
    "different fitting procedures; same order expected")

print("\nChapter 11 (So Long Sucker): help/harm matrices and win rates are game-specific; "
      "the EGTA projection is reused in run_sls.py.")
with open(os.path.join(_bootstrap.FIG, "audit.json"), "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=1)
