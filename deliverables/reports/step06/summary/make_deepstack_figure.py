"""Generate Figure 6.1 for the Step 6 summary: DeepStack architecture.

Two stacked panels (offline intuition-building on top / online continual
re-solving below) sharing one highlighted CFV-network block, making explicit
that the network trained offline is the exact leaf evaluator used online.
Stacked rather than side by side so the net -> re-solve link is a short
vertical arrow that crosses no box. All text is fs 10 (titles 11) on a 7.9 in
canvas, i.e. >= 8.2 pt when printed at full text width; the boxes are sized
for the longer Bulgarian labels.
Output: deepstack_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_NET, C_ANNOT, EC,
)

FS = 10

fig, ax = new_fig(w=15.8, h=12.68, xlim=(0, 16.2), ylim=(0.2, 13.2), shrink=2.0)

# ---- panel backgrounds (titles left-aligned: the net -> re-solve arrow and
#      its note use the right-hand side of the online panel's title band) ----
panel_bg(ax, 0.15, 7.7, 15.9, 5.3, C_OFFLINE, label="OFFLINE: learn intuition (before play)",
         label_fs=11, label_ha="left")
panel_bg(ax, 0.15, 0.4, 15.9, 7.1, C_ONLINE, label="ONLINE: search with it (every decision)",
         label_fs=11, label_ha="left")

# ================= TOP: offline pipeline =================
b1 = box(ax, 0.35, 10.5, 7.3, 1.7,
         "Generate random poker situations\n(pot, board, both players' ranges)", fc="white", fs=FS)
b2 = box(ax, 0.35, 8.0, 7.3, 2.1,
         "Solve each with CFR+\n(no card abstraction);\ntargets = the resulting\ncounterfactual values",
         fc="white", fs=FS)
arrow(ax, bc(b1), tc(b2))

# ================= SHARED: CFV network (highlighted) =================
net = box(ax, 8.1, 8.0, 7.8, 4.2,
          "Deep counterfactual value\n(CFV) networks:\nflop / turn / pre-flop-aux\n7×500 PReLU, zero-sum head\nin: pot + ranges\n(1,000 clusters)\nout: per-hand CFV (× pot)",
          fc=C_NET, fs=FS, lw=1.8)
arrow(ax, rc(b2), (net[0], rc(b2)[1]))

# ================= BOTTOM: online loop =================
A = box(ax, 0.35, 3.2, 2.6, 3.0, "Current\npublic state", fc="white", fs=FS)
B = box(ax, 3.35, 3.2, 5.0, 3.0,
        "Build a sparse,\ndepth-limited\nlook-ahead tree (fold /\ncall / 2–3 sizes / all-in;\ndepth = end of the\ncurrent betting round)",
        fc="white", fs=FS)
C = box(ax, 8.75, 3.2, 3.3, 3.0, "CFR re-solve\nof the\nlook-ahead", fc="white", fs=FS)
D = box(ax, 12.45, 3.2, 3.2, 3.0, "Sample an\naction, then\ndiscard the\nstrategy", fc="white", fs=FS)
side = box(ax, 2.4, 0.7, 11.2, 2.1,
           "Carries between decisions ONLY:\nown range r₁ (Bayes-updated on own action)\n+ opponent counterfactual values v₂ (from re-solve)",
           fc=C_ANNOT, fs=FS)

arrow(ax, rc(A), lc(B))
arrow(ax, rc(B), lc(C))
arrow(ax, rc(C), lc(D))
arrow(ax, bc(D), rc(side), rad=-0.3)
arrow(ax, lc(side), bc(A), rad=-0.3)

# the offline net is the online leaf evaluator: straight down into the re-solve
AX = 10.4
arrow(ax, (AX, net[1]), (AX, C[1] + C[3]), dashed=True, color="#8a6d1a")
note(ax, AX + 0.25, 7.0, "leaf values\n(depth limit)", fs=FS, color="#8a6d1a", ha="left")

save(fig, str(Path(__file__).parent / "deepstack_arch.png"))
