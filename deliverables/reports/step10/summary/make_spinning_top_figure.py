"""summary figure: the spinning-top (transitive strength vs cyclic dimension).

Balduzzi et al.'s picture: real games have a TRANSITIVE axis (skill: there is a better player)
and a CYCLIC dimension (rock-paper-scissors: only counters, no best). The width of the top is the
cyclic component; the height is skill. We place the four measured populations on it: pure RPS
(all cyclic, transitive ratio 0.0), a pure skill ladder (all transitive, 1.0), the PSRO-Leduc
best-response meta-game (mostly cyclic, ~0.45 transitive / ~0.90 cyclic, 27 three-cycles), and the
league's snapshot meta-game (mostly transitive, ~0.94-0.98). Output: spinning_top.png.
Run with the project .venv active; the PNG lands next to this file.
"""
import os

import matplotlib
matplotlib.use("Agg")
from matplotlib.patches import Ellipse, FancyArrowPatch

from _diagram_utils import new_fig, note, save, EC, C_EXPLOIT, C_SAFE, C_NET, C_MODEL

fig, ax = new_fig(w=12, h=9.0, xlim=(0, 12), ylim=(0, 9.0), shrink=1.7)

cx = 6.0  # central skill axis

# vertical transitive (skill) axis
ax.add_patch(FancyArrowPatch((cx, 0.6), (cx, 8.4), arrowstyle="-|>", mutation_scale=14,
             color=EC, lw=1.8, zorder=2))
note(ax, cx + 0.15, 8.15, "transitive strength (skill)", fs=8.6, color="#2c3e50",
     ha="left", style="normal")
note(ax, cx + 0.15, 0.75, "weakest", fs=7.4, color="#5b6b7b", ha="left")

# nested ellipses: widest (most cyclic) in the middle skill band, narrow at the extremes
bands = [
    (7.7, 1.4, "#e9eef4"),
    (6.2, 3.2, "#dfe7f1"),
    (4.6, 4.4, "#d4dded"),
    (3.0, 3.2, "#dfe7f1"),
    (1.5, 1.4, "#e9eef4"),
]
for y, w, c in bands:
    ax.add_patch(Ellipse((cx, y), width=w, height=1.15, facecolor=c, edgecolor=EC, lw=1.0, zorder=1))
note(ax, cx, 4.6, "cyclic dimension\n(width = #counters)", fs=7.8, color="#2c3e50", style="normal")

# place the four measured populations
def marker(x, y, label, sub, fc):
    ax.add_patch(Ellipse((x, y), width=1.7, height=0.85, facecolor=fc, edgecolor=EC, lw=1.3, zorder=5))
    ax.text(x, y + 0.08, label, ha="center", va="center", fontsize=8.2, fontweight="bold", zorder=6)
    ax.text(x, y - 0.22, sub, ha="center", va="center", fontsize=6.8, color="#2c3e50", zorder=6)

marker(cx, 4.6, "RPS", "T=0.0  C=1.0", C_EXPLOIT)                  # widest band, pure cyclic
marker(cx, 8.0, "skill ladder", "T=1.0  C=0.0", C_SAFE)           # top, pure transitive
marker(2.6, 4.6, "PSRO-Leduc", "T~0.45  C~0.90", C_NET)           # wide band, mostly cyclic
marker(cx + 0.05, 6.9, "league", "T~0.94-0.98", C_MODEL)          # near-top, mostly transitive

note(ax, 6.0, 0.15,
     "same game, different populations: a best-response population (PSRO) sits in the wide cyclic belly; "
     "a training-snapshot population (league) climbs the transitive spine.",
     fs=7.5, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "spinning_top.png"))
