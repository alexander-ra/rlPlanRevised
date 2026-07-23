"""Section 7/8 figure: global vs local safety (the headline Leduc finding).

Global safe-exploitation re-solves the whole tree and its constraint-generation loop
did NOT converge within the iteration cap on Leduc (worst-case -0.64..-1.33). The
subgame (SES) method pins play outside a chosen subgame to the blueprint and re-solves
only that subgame with a gadget -- a far smaller LP that DID converge (worst-case ~-0.13).
Output: global_vs_local.png. Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, tc, bc, cc
from _diagram_utils import C_SAFE, C_EXPLOIT, C_MODEL, C_ANNOT, EC
from matplotlib.patches import Polygon

fig, ax = new_fig(w=14, h=6.6, xlim=(0, 14), ylim=(0, 6.6), shrink=1.7)

note(ax, 3.3, 6.2, "GLOBAL safety (Ganzfried / prime-safe / adaptation)", fs=9.0,
     color="#a5453a", style="normal")
note(ax, 10.6, 6.2, "LOCAL safety (SES subgame gadget)", fs=9.0, color="#2c5a8f",
     style="normal")

# --- global: whole tree re-solved ---
gtri = Polygon([(3.3, 5.4), (0.7, 1.4), (5.9, 1.4)], closed=True,
               facecolor=C_EXPLOIT, edgecolor=EC, lw=1.3, zorder=2)
ax.add_patch(gtri)
note(ax, 3.3, 3.2, "re-solve the\nWHOLE tree", fs=8.6, color="#2c3e50", style="normal")
note(ax, 3.3, 0.85, "Leduc: capped at 40 iters, NOT converged\nworst-case -0.64 .. -1.33 "
                    "(grossly unsafe)", fs=7.6, color="#a5453a")

# --- local: blueprint tree with a small re-solved subgame ---
ltri = Polygon([(10.6, 5.4), (8.0, 1.4), (13.2, 1.4)], closed=True,
               facecolor=C_SAFE, edgecolor=EC, lw=1.3, zorder=2)
ax.add_patch(ltri)
sub = Polygon([(10.6, 3.3), (9.7, 1.4), (11.5, 1.4)], closed=True,
              facecolor=C_MODEL, edgecolor=EC, lw=1.3, zorder=3)
ax.add_patch(sub)
note(ax, 10.6, 4.4, "blueprint\n(pinned)", fs=8.0, color="#2c3e50", style="normal")
note(ax, 10.6, 2.05, "subgame\n(re-solved\n+ gadget)", fs=7.4, color="#2c3e50", style="normal")
note(ax, 10.6, 0.85, "Leduc: converged in 194-350 iters\nworst-case ~-0.13 (near-safe), "
                     "+0.25..+0.68 vs weak types", fs=7.6, color="#2c5a8f")

save(fig, "deliverables/reports/step08/summary/global_vs_local.png")
