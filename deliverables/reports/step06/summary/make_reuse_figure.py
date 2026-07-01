"""Generate Figure 6.7 for the Step 6 summary: component-reuse map.

A grid of building blocks (rows) x the five systems (columns, chronological).
Filled circles mark use; gold stars mark the system that *introduced* a
chapter-native primitive, with a light staircase connecting those origins.
Output: component_reuse.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import note, new_fig, save, EC
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

COLS = ["DeepStack", "Libratus", "Pluribus", "ReBeL", "Student of\nGames"]
COL_X = [0.0, 3.2, 6.4, 9.6, 12.8]

# (label, group, fills, origin_col)  fills: True / False / "vestigial"; group: "A" inherited, "B" native
ROWS = [
    ("CFR / CFR⁺", "A", [True, True, True, True, True], None),
    ("MCCFR", "A", [False, True, True, False, False], None),
    ("Card / information abstraction", "A", [True, True, True, False, False], None),
    ("Action abstraction", "A", [True, True, True, "vestigial", "vestigial"], None),
    ("Neural value net", "A", [True, False, False, False, False], None),
    ("Neural value-and-policy net", "A", [False, False, False, True, True], None),
    ("Depth-limited solving", "B", [True, True, True, True, True], 0),
    ("Continual re-solving", "B", [True, True, True, True, True], 0),
    ("AIVAT variance reduction", "B", [True, True, True, False, False], 0),
    ("Safe (nested) subgame solving", "B", [False, True, True, True, True], 1),
    ("Public belief state", "B", [False, False, False, True, True], 3),
    ("GT-CFR", "B", [False, False, False, False, True], 4),
]

n = len(ROWS)
ROW_Y = [12.0 - i for i in range(n)]

fig, ax = new_fig(w=18.0, h=10.6, xlim=(-6.3, 14.4), ylim=(0.2, 13.6))
ax.set_aspect("equal", adjustable="box")

# group shading
ax.add_patch(Rectangle((-0.9, ROW_Y[5] - 0.5), 14.9, ROW_Y[0] - ROW_Y[5] + 1.0,
                        facecolor="#e4ecfa", edgecolor="none", zorder=0))
ax.add_patch(Rectangle((-0.9, ROW_Y[-1] - 0.5), 14.9, ROW_Y[6] - ROW_Y[-1] + 1.0,
                        facecolor="#e3f3ea", edgecolor="none", zorder=0))
ax.text(13.95, 9.5, "inherited from Steps 3–5", fontsize=8.2,
        color="#2a4d8f", ha="center", va="center", rotation=270, fontweight="bold")
ax.text(13.95, 3.5, "introduced in this chapter", fontsize=8.2,
        color="#1f6b3d", ha="center", va="center", rotation=270, fontweight="bold")

# column headers
for x, name in zip(COL_X, COLS):
    ax.text(x, 12.85, name, ha="center", va="bottom", fontsize=8.6, fontweight="bold", color="#2c3345")

# row labels
for y, (label, group, fills, origin) in zip(ROW_Y, ROWS):
    ax.text(-0.9, y, label, ha="right", va="center", fontsize=8.4)

# grid dots + fills
for y, (label, group, fills, origin) in zip(ROW_Y, ROWS):
    for xi, (x, fill) in enumerate(zip(COL_X, fills)):
        ax.add_patch(plt.Circle((x, y), 0.42, facecolor="white", edgecolor="#c7ccd3", lw=1.0, zorder=1))
        if origin is not None and xi == origin:
            ax.scatter([x], [y], marker="*", s=340, color="#e8b93e", edgecolor="#7a5b0e", lw=1.0, zorder=3)
        elif fill == "vestigial":
            ax.add_patch(plt.Circle((x, y), 0.32, facecolor="#9fb3c8", edgecolor="#5b6b7b", lw=0.8, alpha=0.55, zorder=2))
        elif fill:
            ax.add_patch(plt.Circle((x, y), 0.32, facecolor="#4C72B0" if group == "A" else "#55A868",
                                     edgecolor="#2c3345", lw=0.8, zorder=2))

# staircase through origin cells (native rows, in order)
native_origin_pts = [(COL_X[origin], y) for y, (label, group, fills, origin) in zip(ROW_Y, ROWS) if origin is not None]
xs = [p[0] for p in native_origin_pts]
ys = [p[1] for p in native_origin_pts]
ax.plot(xs, ys, "--", color="#b8973e", lw=1.4, zorder=2)

note(ax, 6.4, 0.55,
     "★ = the system that introduced the block (chapter-native primitives only)   ·   "
     "abstraction rows empty out after Pluribus; neural rows return (as value+policy) from ReBeL onward",
     fs=7.4, ha="center")

save(fig, str(Path(__file__).parent / "component_reuse.png"))
