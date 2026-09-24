"""summary figure: Shapley credit adapted to a purely competitive game.

The Shapley value is the unique split of a coalition's WORTH that satisfies Shapley's axioms
(averaging marginal contributions over join orders). SLS has no shared pot, so the coalition value
is redefined as the PROBABILITY a coalition member wins (estimated by rollouts); each player's
credit is the Shapley value of that win-probability function. The structural warning is the empty
core of the 3-player majority game: no stable allocation exists. SLS, an essential constant-sum
game, has an empty core too - the reason N-player "safe" play cannot anchor to an equilibrium or the
core (Contribution #2). Output: shapley_credit.png. Run with the project .venv active; the PNG
lands next to this file.

Text sizes: the figure prints at 17.6 cm (scale ~0.80), so fs 10.2 prints at ~8.2 pt.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_NET, C_ANNOT, EC

FS = 10.2

fig, ax = new_fig(w=14, h=7.6, xlim=(0, 14), ylim=(0, 7.6), shrink=1.7)

coal = box(ax, 0.3, 4.9, 2.8, 1.7, "Coalition $S$\nof players", fc=C_MODEL, fs=FS, fontweight="bold")
val = box(ax, 3.6, 4.9, 4.9, 1.7, "Coalition VALUE\n$v(S) = P(w \\in S)$, $w$ = winner\n(rollout estimate)", fc=C_SAFE, fs=FS)
shap = box(ax, 9.0, 4.9, 4.0, 1.7, "Shapley value\n$\\phi_i$ = average\nmarginal contribution", fc=C_NET, fs=FS, fontweight="bold")
credit = box(ax, 9.0, 2.7, 4.0, 1.35, "Per-player CREDIT\n(the training signal)", fc=C_SAFE, fs=FS, fontweight="bold")

arrow(ax, (coal[0] + coal[2], coal[1] + coal[3] / 2), (val[0], val[1] + val[3] / 2))
arrow(ax, (val[0] + val[2], val[1] + val[3] / 2), (shap[0], shap[1] + shap[3] / 2))
arrow(ax, (shap[0] + shap[2] / 2, shap[1]), (credit[0] + credit[2] / 2, credit[1] + credit[3]))

note(ax, 7.0, 7.2,
     "Shapley value = the unique split satisfying Shapley's axioms;\n"
     "here a coalition's value is its win probability.",
     fs=FS, color="#2c3e50", style="normal")

note(ax, 4.2, 3.4,
     "MEASURED on SLS: symmetric credit spread\n"
     "0.013 (post-fix); asymmetric [8,8,1,1] ->\n"
     "strong-pair credit 1.0, weak pair 0.0.",
     fs=FS, color="#2c3e50", style="normal")

# structural core warning, full width at the bottom
core = box(ax, 0.3, 0.1, 13.4, 2.3,
           "EMPTY CORE = structural instability (measured, exact):\n"
           "glove game -> Shapley (2/3, 1/6, 1/6), core NON-empty (a stable split exists)\n"
           "3-player majority -> Shapley (1/3, 1/3, 1/3), core EMPTY (no stable split)\n"
           "SLS, an essential constant-sum game, also has an empty core: coalitions are unstable -\n"
           "N-player 'safe' play cannot anchor to an equilibrium or the core (Contribution #2).",
           fc=C_ANNOT, fs=FS)

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shapley_credit.png"))
