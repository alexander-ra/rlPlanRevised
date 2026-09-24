"""summary figure: the spinning top (transitive strength vs cyclic dimension).

The transitive/cyclic split of a payoff matrix is Balduzzi et al. (2018, 2019); the "spinning
top" picture of real games is Czarnecki et al. (2020): a TRANSITIVE axis (skill: there is a
better player) and a CYCLIC dimension (rock-paper-scissors: only counters, no best). The width of
the top is the cyclic component; the height is skill. The four measured populations are placed
on it schematically: pure RPS (all cyclic, transitive ratio 0.0), a pure skill ladder (all
transitive, 1.0), the PSRO-Leduc best-response meta-game (mostly cyclic, ~0.45 transitive / ~0.90
cyclic, 27 three-cycles), and the league's snapshot meta-game (mostly transitive, ~0.94-0.98).
Output: spinning_top.png. Run with the project .venv active; the PNG lands next to this file.

Drawn at print size: the canvas is 7.0 in wide (the 17.6 cm text width), all text is fs 10.
"""
import os

import matplotlib
matplotlib.use("Agg")
from matplotlib.patches import Ellipse, FancyArrowPatch

from _diagram_utils import new_fig, note, save, EC, C_EXPLOIT, C_SAFE, C_NET, C_MODEL

fig, ax = new_fig(w=13.5, h=11.3, xlim=(0, 13.5), ylim=(-1.3, 10.0), shrink=13.5 / 7.0)

cx = 5.5  # central skill axis

# vertical transitive (skill) axis
ax.add_patch(FancyArrowPatch((cx, 0.3), (cx, 9.9), arrowstyle="-|>", mutation_scale=14,
             color=EC, lw=1.8, zorder=2))
note(ax, cx + 1.85, 9.05, "transitive strength (skill)", fs=10, color="#2c3e50",
     ha="left", style="normal")
note(ax, cx + 0.2, 0.45, "weakest", fs=10, color="#5b6b7b", ha="left")

# nested ellipses: widest (most cyclic) in the middle skill band, narrow at the extremes
bands = [  # (y, width, height)
    (8.4, 1.6, 1.1),
    (6.9, 3.8, 1.2),
    (4.9, 7.2, 1.7),
    (2.9, 3.8, 1.2),
    (1.3, 1.6, 1.1),
]
for y, w, h in bands:
    c = {1.6: "#e9eef4", 3.8: "#dfe7f1", 7.2: "#d4dded"}[w]
    ax.add_patch(Ellipse((cx, y), width=w, height=h, facecolor=c, edgecolor=EC, lw=1.0, zorder=1))
note(ax, 9.4, 4.9, "cyclic dimension\n(width = number\nof counters)", fs=10, color="#2c3e50",
     ha="left", style="normal")


def marker(x, y, label, sub, fc):
    """A measured population: label inside the ellipse, its T/C ratios just below it."""
    ax.add_patch(Ellipse((x, y), width=3.25, height=1.05, facecolor=fc, edgecolor=EC, lw=1.3,
                         zorder=5))
    ax.text(x, y, label, ha="center", va="center", fontsize=10, zorder=6)
    ax.text(x, y - 0.8, sub, ha="center", va="center", fontsize=10, color="#2c3e50", zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.92))


marker(cx, 9.0, "skill\nladder", "T = 1.0   C = 0.0", C_SAFE)             # top, pure transitive
marker(cx, 6.95, "league\nsnapshots", "T ≈ 0.94–0.98", C_MODEL)          # near-top, mostly transitive
marker(cx, 4.9, "Rock-Paper-\nScissors", "T = 0.0   C = 1.0", C_EXPLOIT)  # widest band, pure cyclic
marker(2.1, 4.9, "PSRO best\nresponses", "T ≈ 0.45   C ≈ 0.90", C_NET)  # wide band, mostly cyclic

note(ax, 6.75, -0.55,
     "same game, different populations: a best-response population (PSRO)\n"
     "sits in the wide cyclic belly; a training-snapshot population (league)\n"
     "climbs the transitive spine.",
     fs=10, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "spinning_top.png"))
