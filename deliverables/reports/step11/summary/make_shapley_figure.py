"""summary figure: Shapley credit adapted to a purely competitive game.

Classical Shapley splits a coalition's WORTH fairly among members (averaging marginal contributions
over join orders). SLS has no shared pot, so the coalition value is redefined as the PROBABILITY a
coalition member wins (estimated by rollouts); each player's credit is the Shapley value of that
win-probability function. The structural warning is the empty core of the 3-player majority game: no
stable allocation exists, so coalitions WILL break - the SLS situation and the reason N-player "safe"
play needs a behavioral prior (Contribution #2). Output: shapley_credit.png. Run with the project
.venv active; the PNG lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_NET, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.6, xlim=(0, 14), ylim=(0, 7.6), shrink=1.7)

coal = box(ax, 0.4, 5.0, 3.2, 1.5, "Coalition $S$\nof players", fc=C_MODEL, fs=8.6, fontweight="bold")
val = box(ax, 4.3, 5.0, 3.6, 1.5, "Coalition VALUE $v(S)$\n$= P(\\text{a member of } S \\text{ wins})$\n(rollout estimate)", fc=C_SAFE, fs=8.0)
shap = box(ax, 8.6, 5.0, 3.2, 1.5, "Shapley value\n$\\phi_i$ = fair marginal\ncontribution", fc=C_NET, fs=8.4, fontweight="bold")
credit = box(ax, 8.6, 2.6, 3.2, 1.2, "Per-player CREDIT\n(the training signal)", fc=C_SAFE, fs=8.4, fontweight="bold")

arrow(ax, (coal[0] + coal[2], coal[1] + coal[3] / 2), (val[0], val[1] + val[3] / 2))
arrow(ax, (val[0] + val[2], val[1] + val[3] / 2), (shap[0], shap[1] + shap[3] / 2))
arrow(ax, (shap[0] + shap[2] / 2, shap[1]), (credit[0] + credit[2] / 2, credit[1] + credit[3]))

note(ax, 7.0, 7.25,
     "Shapley = the UNIQUE fair split; adapted to a competitive game via win-probability as the value.",
     fs=8.4, color="#2c3e50", style="normal")

# structural core warning
core = box(ax, 0.4, 2.4, 7.4, 2.1,
           "EMPTY CORE = structural betrayal (measured, exact):\n"
           "  glove game -> Shapley (2/3, 1/6, 1/6), core NON-empty (a stable split exists)\n"
           "  3-player majority -> Shapley (1/3, 1/3, 1/3), core EMPTY (no stable split)\n"
           "The empty core is the SLS situation: coalitions are inherently unstable and WILL break -\n"
           "so N-player 'safe' play cannot anchor to a Nash/core equilibrium (Contribution #2).",
           fc=C_ANNOT, fs=7.8)

note(ax, 10.2, 1.9,
     "MEASURED on SLS: symmetric credit spread 0.013 (post-fix);\n"
     "asymmetric [8,8,1,1] -> strong pair credit 1.0, weak 0.0.",
     fs=7.4, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shapley_credit.png"))
