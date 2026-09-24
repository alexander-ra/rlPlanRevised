"""summary figure: the EGTA pipeline (empirical game-theoretic analysis of a population).

Play every pair of agents to fill an empirical payoff matrix, solve its meta-Nash mixture, collapse
that mixture to a single behavioral policy, and score its EXACT full-game exploitability. The
measured caveat (this chapter, scale): the meta-Nash minimizes META-GAME regret, which is NOT the
same as minimizing full-game exploitability -- the collapsed mixture (3.42) is less exploitable
than each of its three components but more exploitable than the population's best agent (1.31),
which got zero meta-Nash weight. Output: egta_pipeline.png. Run with the project .venv active; the
PNG lands next to this file.

Drawn at print size: the canvas is 7.0 in wide (the 17.6 cm text width), all text is fs 10.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT, EC

fig, ax = new_fig(w=14.2, h=8.7, xlim=(-0.1, 14.1), ylim=(0.2, 8.9), shrink=14.2 / 7.0)

pop = box(ax, 0.0, 4.9, 2.4, 1.9, "Population\n$\\{\\pi_1,\\dots,\\pi_n\\}$", fc=C_MODEL, fs=10,
          fontweight="bold")
mat = box(ax, 2.8, 4.9, 3.8, 1.9, "Empirical payoff\nmatrix $M_{ij}$\n(play every pair)", fc=C_SAFE, fs=10)
nash = box(ax, 7.0, 4.9, 3.4, 1.9, "Meta-Nash mixture\n$\\sigma$ over agents", fc=C_NET, fs=10)
coll = box(ax, 10.8, 4.9, 3.2, 1.9, "Collapse $\\sigma$ to one\nbehavioral policy", fc=C_SAFE, fs=10)
exp = box(ax, 4.6, 2.6, 4.8, 1.6, "EXACT exploitability\n(NashConv, Chapter 7)", fc=C_EXPLOIT, fs=10,
          fontweight="bold")

arrow(ax, (pop[0] + pop[2], pop[1] + pop[3] / 2), (mat[0], mat[1] + mat[3] / 2))
arrow(ax, (mat[0] + mat[2], mat[1] + mat[3] / 2), (nash[0], nash[1] + nash[3] / 2))
note(ax, 6.8, 7.15, "solve", fs=10, color="#2c3e50")
arrow(ax, (nash[0] + nash[2], nash[1] + nash[3] / 2), (coll[0], coll[1] + coll[3] / 2))
arrow(ax, (coll[0] + coll[2] / 2, coll[1]), (exp[0] + exp[2], exp[1] + exp[3] / 2),
      color=EC, lw=1.5, rad=-0.25)

box(ax, 0.0, 0.35, 14.0, 1.85,
    "CAVEAT (measured, scale): meta-Nash minimizes META-GAME regret,\n"
    "not full-game exploitability. Its mixture scored 3.42, while the\n"
    "least exploitable agent (1.31) got zero weight.",
    fc=C_ANNOT, fs=10)

note(ax, 7.0, 8.2,
     'EGTA = Nash of a game whose "strategies" are whole policies —\n'
     "the population lift of exploitability.",
     fs=10, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "egta_pipeline.png"))
