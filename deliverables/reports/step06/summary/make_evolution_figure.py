"""Generate Figure 6.6 for the Step 6 summary: the seven-year evolution arc.

A left-to-right timeline (2017-2023) with the five systems as nodes across
three faint horizontal lanes (one per axis of travel), plus lineage arrows
and a per-system +/- capability tag. Output: evolution_arc.png.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import box, arrow, note, new_fig, save, EC
import matplotlib.pyplot as plt

fig, ax = new_fig(w=19.5, h=10.9, xlim=(-0.6, 11.4), ylim=(-2.9, 10.6))

LANES = {
    "info_unified": (1.0, 2.0, "imperfect-only ↔ unified"),
    "offline_online": (4.0, 2.0, "offline ↔ real-time search"),
    "abstraction_neural": (7.0, 2.0, "abstraction ↔ neural"),
}
for bottom, h, label in LANES.values():
    ax.add_patch(plt.Rectangle((-0.4, bottom), 11.4, h, facecolor="#eef1f5", edgecolor="none", zorder=0))
    ax.text(-0.55, bottom + h / 2, label, ha="right", va="center", fontsize=8.2,
            fontweight="bold", color="#445", rotation=0)

systems = [
    ("DeepStack", 1.0, "2017", "#4C72B0",
     {"abstraction_neural": 0.82, "offline_online": 0.55, "info_unified": 0.05},
     "+ sound, low-exploitability search\n– 2p0s only; heavy offline solve"),
    ("Libratus", 2.9, "2017", "#DD8452",
     {"abstraction_neural": 0.08, "offline_online": 0.55, "info_unified": 0.05},
     "+ exact real-time response\n– no neural net; 2-player only"),
    ("Pluribus", 5.3, "2019", "#55A868",
     {"abstraction_neural": 0.14, "offline_online": 0.48, "info_unified": 0.05},
     "+ scales to N players, ~$150\n– no safety guarantee"),
    ("ReBeL", 7.7, "2020", "#C44E52",
     {"abstraction_neural": 0.90, "offline_online": 0.78, "info_unified": 0.10},
     "+ recovers 2p0s safety, neural\n– back to two players only"),
    ("Student of\nGames", 10.2, "2023", "#8172B2",
     {"abstraction_neural": 0.95, "offline_online": 0.82, "info_unified": 0.95},
     "+ unifies perfect/imperfect info\n– weaker peak strength (e.g. Go)"),
]

# chronological guide lines within each lane
for key, (bottom, h, _) in LANES.items():
    xs = [s[1] for s in systems]
    ys = [bottom + s[4][key] * h for s in systems]
    ax.plot(xs, ys, "-", color="#c3cad3", lw=1.2, zorder=1)

for i, (name, x, year, color, vals, tag) in enumerate(systems):
    for key, (bottom, h, _) in LANES.items():
        y = bottom + vals[key] * h
        ax.scatter([x], [y], s=130, color=color, edgecolor="#2c3345", lw=1.1, zorder=3)
    ax.text(x, 9.55, f"{name}\n({year})", ha="center", va="bottom", fontsize=8.4, fontweight="bold", color=color)
    tag_y = -0.3 if i % 2 == 0 else -1.15
    ax.text(x, tag_y, tag, ha="center", va="top", fontsize=7.1, color="#333")

# lineage arrows (abstraction<->neural lane): DeepStack -> ReBeL -> SoG (learned values)
lane_b, lane_h, _ = LANES["abstraction_neural"]


def ly(i):
    return lane_b + systems[i][4]["abstraction_neural"] * lane_h


arrow(ax, (systems[0][1], ly(0) + 0.15), (systems[3][1], ly(3) + 0.15), rad=-0.15, lw=1.8, color="#2a4d8f")
arrow(ax, (systems[3][1], ly(3) + 0.15), (systems[4][1], ly(4) + 0.15), rad=-0.1, lw=1.8, color="#2a4d8f")
note(ax, 4.5, 9.0, "learned-values lineage", fs=7.0, color="#2a4d8f")

arrow(ax, (systems[1][1], ly(1) - 0.15), (systems[2][1], ly(2) - 0.15), rad=0.2, lw=1.8, color="#b2560d")
note(ax, 4.1, 6.65, "blueprint + search lineage", fs=7.0, color="#b2560d")

# dashed cross-influence: DeepStack <-> Libratus (depth-limited solving)
arrow(ax, (systems[0][1] + 0.05, ly(0) - 0.3), (systems[1][1] - 0.05, ly(1) - 0.3), dashed=True, color="#6a6a6a", style="-", lw=1.3)
note(ax, 1.95, 6.35, "unified by depth-limited solving", fs=6.6, color="#6a6a6a")

# dashed cross-influence: ReBeL -> SoG carrying PBS (info_unified lane)
lb2, lh2, _ = LANES["info_unified"]
arrow(ax, (systems[3][1], lb2 + systems[3][4]["info_unified"] * lh2),
      (systems[4][1], lb2 + systems[4][4]["info_unified"] * lh2), dashed=True, color="#6a6a6a", lw=1.4)
note(ax, 8.95, 1.35, "PBS carried\nforward", fs=6.6, color="#6a6a6a")

footer = box(ax, -0.45, -2.85, 11.3, 0.85,
              "Three axes of travel — abstraction → neural · offline → real-time search · imperfect-only → unified — "
              "and no system sits furthest along all three at once: the arc is a set of trades, not a ranking.",
              fc="#eceff3", fs=7.6)

save(fig, str(Path(__file__).parent / "evolution_arc.png"))
