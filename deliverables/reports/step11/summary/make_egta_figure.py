"""summary figure: the EGTA + spinning-top pipeline for SLS (a wheel or a ladder?).

Treat whole SLS strategies as the atoms of a meta-game, play every group to fill an empirical payoff
TENSOR, project the 4-player tensor to a 2-player pairwise matchup matrix (so Chapter 9's meta-Nash
and Chapter 10's Hodge spinning-top still apply), and split it into a transitive (skill-ladder) and
a cyclic (coalition-counters) component. Measured: which POOL you decompose decides the answer - a
skill-ladder pool is transitive (cyclic ~0.25-0.31), a coalition pool has a strong cyclic part
(~0.57-0.69) while the transitive part stays slightly larger. The 2-type projection likely discards
3-/4-player coalition effects, so the cyclic ratio may be underestimated.
Output: egta_spinning_top.png. Run with the project .venv active; the PNG lands next to this file.

Text sizes: the figure prints at 17.6 cm (scale ~0.87), so fs 10 prints at ~8.7 pt.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.2, xlim=(0, 14), ylim=(0, 7.2), shrink=1.7)

pop = box(ax, 0.3, 4.3, 3.0, 1.6, "Strategy\npool\n$\\{\\pi_1,\\dots,\\pi_n\\}$", fc=C_MODEL, fs=10, fontweight="bold")
tensor = box(ax, 3.7, 4.3, 3.1, 1.6, "4-player payoff\nTENSOR\n(play every group)", fc=C_SAFE, fs=10)
proj = box(ax, 7.2, 4.3, 3.1, 1.6, "Project to pairwise\nmatchup matrix", fc=C_SAFE, fs=10)
split = box(ax, 10.7, 4.3, 3.1, 1.6, "Hodge spinning-top\nsplit (Chapter 10)", fc=C_NET, fs=10, fontweight="bold")

trans = box(ax, 8.9, 1.9, 2.3, 1.3, "TRANSITIVE\n(skill ladder)", fc=C_SAFE, fs=10)
cyc = box(ax, 11.4, 1.9, 2.4, 1.3, "CYCLIC\n(coalition\nwheel)", fc=C_EXPLOIT, fs=10, fontweight="bold")

arrow(ax, (pop[0] + pop[2], pop[1] + pop[3] / 2), (tensor[0], tensor[1] + tensor[3] / 2))
arrow(ax, (tensor[0] + tensor[2], tensor[1] + tensor[3] / 2), (proj[0], proj[1] + proj[3] / 2))
arrow(ax, (proj[0] + proj[2], proj[1] + proj[3] / 2), (split[0], split[1] + split[3] / 2))
arrow(ax, (split[0] + split[2] / 2 - 0.6, split[1]), (trans[0] + trans[2] / 2, trans[1] + trans[3]), rad=0.1)
arrow(ax, (split[0] + split[2] / 2 + 0.6, split[1]), (cyc[0] + cyc[2] / 2, cyc[1] + cyc[3]), rad=-0.1)

note(ax, 7.0, 6.75,
     "EGTA = an empirical meta-game whose \"strategies\" are whole policies;\n"
     "exploitability gives no guarantee against a coalition.",
     fs=10, color="#2c3e50", style="normal")

res = box(ax, 0.3, 0.5, 8.2, 3.3,
          "MEASURED - the POPULATION decides the shape:\n"
          "  skill-ladder pool -> cyclic ~0.25-0.31 (a LADDER)\n"
          "  coalition pool -> cyclic ~0.57-0.69\n"
          "  (strong cyclic part)\n"
          "Transitive part still slightly larger - the\n"
          "2-type projection likely discards 3-/4-player\n"
          "coalition effects (Contribution #3, open).",
          fc=C_ANNOT, fs=10)

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "egta_spinning_top.png"))
