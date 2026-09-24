"""Generate Figure 6.6 for the Step 6 summary: the seven-year evolution arc.

A left-to-right timeline (2017-2023) with the five systems as nodes across
three faint horizontal lanes (one per axis of travel), plus lineage arrows
and a per-system +/- capability tag.

Print legibility: coordinates are in inches on an ~8.2 in canvas printed at
98 % of the text width, so fs 10 prints at ~8.3 pt or more. Lane labels sit
in their own column left of the lanes; the tags alternate between two rows
(the last one right-aligned) so neighbours never collide and nothing reaches
past the canvas, which would widen the saved image and shrink the print.
Output: evolution_arc.png.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import box, arrow, note, new_fig, save, EC
import matplotlib.pyplot as plt

FS = 10
fig, ax = new_fig(w=8.2, h=6.85, xlim=(0, 8.2), ylim=(0, 6.85), shrink=1.0)

LANE_X0, LANE_X1 = 1.7, 8.15
LANES = {
    "info_unified": (2.65, 0.85, "imperfect-only ↔\nunified"),
    "offline_online": (3.6, 0.9, "offline ↔\nreal-time search"),
    "abstraction_neural": (4.6, 1.35, "abstraction ↔\nneural"),
}
for bottom, h, label in LANES.values():
    ax.add_patch(plt.Rectangle((LANE_X0, bottom), LANE_X1 - LANE_X0, h,
                               facecolor="#eef1f5", edgecolor="none", zorder=0))
    ax.text(LANE_X0 - 0.08, bottom + h / 2, label, ha="right", va="center", fontsize=FS,
            fontweight="bold", color="#445")

# (name, x, year, colour, lane positions 0..1, tag, tag row, tag alignment)
systems = [
    ("DeepStack", 2.2, "2017", "#4C72B0",
     {"abstraction_neural": 0.82, "offline_online": 0.55, "info_unified": 0.05},
     "+ sound search with\n  low exploitability\n– 2p0s only; heavy\n  offline solve", 0, "center"),
    ("Libratus", 3.3, "2017", "#DD8452",
     {"abstraction_neural": 0.08, "offline_online": 0.55, "info_unified": 0.05},
     "+ exact real-time\n  response\n– no neural net;\n  2-player only", 1, "center"),
    ("Pluribus", 4.7, "2019", "#55A868",
     {"abstraction_neural": 0.14, "offline_online": 0.48, "info_unified": 0.05},
     "+ scales to N players,\n  ~$150\n– no safety guarantee", 0, "center"),
    ("ReBeL", 6.1, "2020", "#C44E52",
     {"abstraction_neural": 0.90, "offline_online": 0.78, "info_unified": 0.10},
     "+ recovers 2p0s safety;\n  neural\n– back to two players\n  only", 1, "center"),
    ("Student of\nGames", 7.5, "2023", "#8172B2",
     {"abstraction_neural": 0.95, "offline_online": 0.82, "info_unified": 0.95},
     "+ unifies perfect/\n  imperfect info\n– weaker peak strength\n  (e.g. Go)", 0, "right"),
]
TAG_TOP = [2.55, 1.8]      # two rows under the lanes


def ly(i, key):
    bottom, h, _ = LANES[key]
    return bottom + systems[i][4][key] * h


# chronological guide lines within each lane
for key in LANES:
    ax.plot([s[1] for s in systems], [ly(i, key) for i in range(len(systems))],
            "-", color="#c3cad3", lw=1.2, zorder=1)

for i, (name, x, year, color, vals, tag, row, align) in enumerate(systems):
    for key in LANES:
        ax.scatter([x], [ly(i, key)], s=110, color=color, edgecolor="#2c3345", lw=1.1, zorder=3)
    ax.text(x, 6.15, f"{name}\n({year})", ha="center", va="bottom", fontsize=FS,
            fontweight="bold", color=color)
    tx = x if align == "center" else LANE_X1
    ax.text(tx, TAG_TOP[row], tag, ha=align, va="top", ma="left", fontsize=FS, color="#333")

# lineage arrows in the abstraction <-> neural lane
K = "abstraction_neural"
arrow(ax, (systems[0][1], ly(0, K) + 0.06), (systems[3][1], ly(3, K) + 0.06), rad=-0.04, lw=1.8, color="#2a4d8f")
arrow(ax, (systems[3][1], ly(3, K) + 0.06), (systems[4][1], ly(4, K) + 0.06), rad=-0.1, lw=1.8, color="#2a4d8f")
note(ax, 4.0, 5.62, "learned-values lineage", fs=FS, color="#2a4d8f")

arrow(ax, (systems[1][1], ly(1, K) - 0.1), (systems[2][1], ly(2, K) - 0.1), rad=0.06, lw=1.8, color="#b2560d")
note(ax, 4.0, 5.2, "blueprint + search lineage", fs=FS, color="#b2560d")

# ReBeL -> SoG carrying the public belief state (info lane)
K2 = "info_unified"
arrow(ax, (systems[3][1], ly(3, K2)), (systems[4][1], ly(4, K2)), dashed=True, color="#6a6a6a", lw=1.4)
note(ax, 7.3, 2.8, "PBS carried\nforward", fs=FS, color="#6a6a6a")

box(ax, 0.1, 0.08, 8.05, 0.95,
    "Three axes of travel — abstraction → neural · offline → real-time search ·\n"
    "imperfect-only → unified — and no system sits furthest along all three at once:\n"
    "the arc is a set of trades, not a ranking.",
    fc="#eceff3", fs=FS)

save(fig, str(Path(__file__).parent / "evolution_arc.png"))
