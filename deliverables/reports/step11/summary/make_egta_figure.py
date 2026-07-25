"""summary figure: the EGTA + spinning-top pipeline for SLS (a wheel or a ladder?).

Treat whole SLS strategies as the atoms of a meta-game, play every pair to fill an empirical payoff
TENSOR, project the 4-player tensor to a 2-player pairwise matchup matrix (so Step 09's meta-Nash and
Step 10's Hodge spinning-top still apply), and split it into a transitive (skill-ladder) and a cyclic
(coalition-counters) component. Measured: which POOL you decompose decides the answer - a skill-ladder
pool is transitive (cyclic ~0.25-0.31), a coalition pool is strongly cyclic (~0.57-0.69). The 2-type
projection likely discards 3-/4-player coalition effects, so the cyclic ratio is a lower bound.
Output: egta_spinning_top.png. Run with the project .venv active; the PNG lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.2, xlim=(0, 14), ylim=(0, 7.2), shrink=1.7)

pop = box(ax, 0.4, 4.4, 2.9, 1.4, "Strategy pool\n$\\{\\pi_1,\\dots,\\pi_n\\}$", fc=C_MODEL, fs=8.6, fontweight="bold")
tensor = box(ax, 3.7, 4.4, 3.0, 1.4, "4-player payoff\nTENSOR\n(play every group)", fc=C_SAFE, fs=8.2)
proj = box(ax, 7.1, 4.4, 3.0, 1.4, "Project to pairwise\nmatchup matrix", fc=C_SAFE, fs=8.4)
split = box(ax, 10.5, 4.4, 3.1, 1.4, "Hodge spinning-top\nsplit (Step 10)", fc=C_NET, fs=8.4, fontweight="bold")

trans = box(ax, 8.0, 2.0, 2.6, 1.2, "TRANSITIVE\n(skill ladder)", fc=C_SAFE, fs=8.2)
cyc = box(ax, 11.0, 2.0, 2.6, 1.2, "CYCLIC\n(coalition wheel)", fc=C_EXPLOIT, fs=8.2, fontweight="bold")

arrow(ax, (pop[0] + pop[2], pop[1] + pop[3] / 2), (tensor[0], tensor[1] + tensor[3] / 2))
arrow(ax, (tensor[0] + tensor[2], tensor[1] + tensor[3] / 2), (proj[0], proj[1] + proj[3] / 2))
arrow(ax, (proj[0] + proj[2], proj[1] + proj[3] / 2), (split[0], split[1] + split[3] / 2))
arrow(ax, (split[0] + split[2] / 2 - 0.6, split[1]), (trans[0] + trans[2] / 2, trans[1] + trans[3]), rad=0.1)
arrow(ax, (split[0] + split[2] / 2 + 0.6, split[1]), (cyc[0] + cyc[2] / 2, cyc[1] + cyc[3]), rad=-0.1)

note(ax, 7.0, 6.85,
     "EGTA = Nash of a game whose 'strategies' are whole policies (exploitability has no meaning vs a coalition).",
     fs=8.4, color="#2c3e50", style="normal")

res = box(ax, 0.4, 1.6, 7.2, 2.2,
          "MEASURED - which POOL you decompose decides the shape:\n"
          "  skill-ladder pool  -> cyclic ~0.25-0.31 (a LADDER)\n"
          "  coalition pool     -> cyclic ~0.57-0.69 (a WHEEL)\n"
          "Strongly cyclic, confirming the Step-10 direction, but just\n"
          "under strict dominance - the 2-type projection likely discards\n"
          "3-/4-player coalition effects (Contribution #3, open).",
          fc=C_ANNOT, fs=7.7)

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "egta_spinning_top.png"))
