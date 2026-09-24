"""Generate Figure 6.7 for the Step 6 summary: component-reuse map.

A grid of building blocks (rows) x the five systems (columns, chronological).
Filled circles mark use; gold stars mark the system that *introduced* a
chapter-native primitive, with a light staircase connecting those origins.

Cells follow the primary papers: continual re-solving is DeepStack's and
Student of Games' (Libratus uses nested safe subgame solving, Pluribus
depth-limited search, ReBeL its own safe search); Libratus's subgames run to
the end of the game, so it has no depth-limited solving; AIVAT is used by
DeepStack, Pluribus, ReBeL and SoG, not by Libratus; Pluribus's search is
unsafe, so it has no safe subgame solving.

Print legibility: coordinates are in inches on an ~8 in canvas printed at
98 % of the text width; all text fs 10. Row labels have their own column;
long Bulgarian labels wrap onto two lines within the 0.46 in row pitch.
Output: component_reuse.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import note, new_fig, save, EC
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

FS = 10
COLS = ["DeepStack", "Libratus", "Pluribus", "ReBeL", "Student of\nGames"]
COL_X = [3.35, 4.25, 5.15, 6.05, 6.95]

# (label, group, fills, origin_col)  fills: True / False / "vestigial"; group: "A" inherited, "B" native
ROWS = [
    ("CFR / CFR⁺", "A", [True, True, True, True, True], None),
    ("MCCFR", "A", [False, True, True, False, False], None),
    ("Card / information abstraction", "A", [True, True, True, False, False], None),
    ("Action abstraction", "A", [True, True, True, "vestigial", "vestigial"], None),
    ("Neural value net", "A", [True, False, False, False, False], None),
    ("Neural value-and-policy net", "A", [False, False, False, True, True], None),
    ("Depth-limited solving", "B", [True, False, True, True, True], 0),
    ("Continual re-solving", "B", [True, False, False, False, True], 0),
    ("AIVAT variance reduction", "B", [True, False, True, True, True], 0),
    ("Safe (nested) subgame solving", "B", [False, True, False, True, True], 1),
    ("Public belief state", "B", [False, False, False, True, True], 3),
    ("GT-CFR", "B", [False, False, False, False, True], 4),
]

PITCH = 0.46
ROW_Y = [6.0 - i * PITCH for i in range(len(ROWS))]
R_OUT, R_IN = 0.17, 0.13
SH_X0, SH_X1 = 2.9, 7.45

fig, ax = new_fig(w=8.0, h=6.75, xlim=(0, 8.0), ylim=(0, 6.75), shrink=1.0)
ax.set_aspect("equal", adjustable="box")

# group shading
ax.add_patch(Rectangle((SH_X0, ROW_Y[5] - PITCH / 2), SH_X1 - SH_X0, ROW_Y[0] - ROW_Y[5] + PITCH,
                       facecolor="#e4ecfa", edgecolor="none", zorder=0))
ax.add_patch(Rectangle((SH_X0, ROW_Y[-1] - PITCH / 2), SH_X1 - SH_X0, ROW_Y[6] - ROW_Y[-1] + PITCH,
                       facecolor="#e3f3ea", edgecolor="none", zorder=0))
ax.text(7.62, (ROW_Y[0] + ROW_Y[5]) / 2, "inherited from Chapters 3–5", fontsize=FS,
        color="#2a4d8f", ha="center", va="center", rotation=270, fontweight="bold")
ax.text(7.62, (ROW_Y[6] + ROW_Y[-1]) / 2, "introduced in this chapter", fontsize=FS,
        color="#1f6b3d", ha="center", va="center", rotation=270, fontweight="bold")

# column headers
for x, name in zip(COL_X, COLS):
    ax.text(x, ROW_Y[0] + 0.32, name, ha="center", va="bottom", fontsize=FS, fontweight="bold", color="#2c3345")

# row labels
for y, (label, group, fills, origin) in zip(ROW_Y, ROWS):
    ax.text(SH_X0 - 0.1, y, label, ha="right", va="center", fontsize=FS)

# grid dots + fills
for y, (label, group, fills, origin) in zip(ROW_Y, ROWS):
    for xi, (x, fill) in enumerate(zip(COL_X, fills)):
        ax.add_patch(plt.Circle((x, y), R_OUT, facecolor="white", edgecolor="#c7ccd3", lw=1.0, zorder=1))
        if origin is not None and xi == origin:
            ax.scatter([x], [y], marker="*", s=260, color="#e8b93e", edgecolor="#7a5b0e", lw=1.0, zorder=3)
        elif fill == "vestigial":
            ax.add_patch(plt.Circle((x, y), R_IN, facecolor="#9fb3c8", edgecolor="#5b6b7b", lw=0.8, alpha=0.55, zorder=2))
        elif fill:
            ax.add_patch(plt.Circle((x, y), R_IN, facecolor="#4C72B0" if group == "A" else "#55A868",
                                    edgecolor="#2c3345", lw=0.8, zorder=2))

# staircase through origin cells (native rows, in order)
pts = [(COL_X[origin], y) for y, (label, group, fills, origin) in zip(ROW_Y, ROWS) if origin is not None]
ax.plot([p[0] for p in pts], [p[1] for p in pts], "--", color="#b8973e", lw=1.4, zorder=2)

note(ax, 3.9, 0.32,
     "★ = the system that introduced the block (chapter-native primitives only) ·\n"
     "abstraction rows empty out after Pluribus; neural rows return\n"
     "(as value + policy) from ReBeL onward",
     fs=FS, ha="center")

save(fig, str(Path(__file__).parent / "component_reuse.png"))
