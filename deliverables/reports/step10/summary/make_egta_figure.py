"""summary figure: the EGTA pipeline (empirical game-theoretic analysis of a population).

Play every pair of agents to fill an empirical payoff matrix, solve its meta-Nash mixture, collapse
that mixture to a single behavioral policy, and score its EXACT full-game exploitability. The
measured caveat (this step, scale): the meta-Nash minimizes META-GAME regret, which is NOT the same
as minimizing full-game exploitability -- the collapsed mixture (3.42) can be MORE exploitable than
the best single member (1.31). Output: egta_pipeline.png. Run with the project .venv active; the PNG
lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.2, xlim=(0, 14), ylim=(0, 7.2), shrink=1.7)

pop = box(ax, 0.4, 4.2, 3.0, 1.4, "Population\n$\\{\\pi_1,\\dots,\\pi_n\\}$", fc=C_MODEL, fs=8.8, fontweight="bold")
mat = box(ax, 4.0, 4.2, 3.2, 1.4, "Empirical payoff\nmatrix $M_{ij}$\n(play every pair)", fc=C_SAFE, fs=8.4)
nash = box(ax, 7.8, 4.2, 3.0, 1.4, "Meta-Nash mixture\n$\\sigma$ over agents", fc=C_NET, fs=8.6, fontweight="bold")
coll = box(ax, 11.0, 4.2, 2.8, 1.4, "Collapse $\\sigma$ to one\nbehavioral policy", fc=C_SAFE, fs=8.2)
exp = box(ax, 7.8, 1.4, 3.0, 1.4, "EXACT exploitability\n(NashConv, Step 07)", fc=C_EXPLOIT, fs=8.4, fontweight="bold")

arrow(ax, (pop[0] + pop[2], pop[1] + pop[3] / 2), (mat[0], mat[1] + mat[3] / 2))
arrow(ax, (mat[0] + mat[2], mat[1] + mat[3] / 2), (nash[0], nash[1] + nash[3] / 2))
note(ax, 7.5, 5.95, "solve", fs=7.2, color="#2c3e50")
arrow(ax, (nash[0] + nash[2], nash[1] + nash[3] / 2), (coll[0], coll[1] + coll[3] / 2))
arrow(ax, (coll[0] + coll[2] / 2, coll[1]), (exp[0] + exp[2], exp[1] + exp[3] / 2),
      color=EC, lw=1.5, rad=-0.25)

caveat = box(ax, 0.4, 1.2, 6.8, 1.7,
             "CAVEAT (measured, scale): meta-Nash minimizes META-GAME regret,\n"
             "not full-game exploitability. The collapsed mixture scored 3.42 --\n"
             "WORSE than the best single member (1.31). Mixing can add tells.",
             fc=C_ANNOT, fs=7.8)

note(ax, 7.0, 6.85,
     "EGTA = Nash of a game whose 'strategies' are whole policies -- the population lift of exploitability.",
     fs=8.4, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "egta_pipeline.png"))
