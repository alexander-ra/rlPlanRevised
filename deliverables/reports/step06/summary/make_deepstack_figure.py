"""Generate Figure 6.1 for the Step 6 summary: DeepStack architecture.

Two side-by-side panels (offline intuition-building / online continual
re-solving) sharing one highlighted CFV-network block, making explicit that
the network trained offline is the exact leaf evaluator used online.
Output: deepstack_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_NET, C_ANNOT, EC,
)

fig, ax = new_fig(w=15.5, h=6.7, xlim=(0, 16), ylim=(3.3, 10.0))

# ---- panel backgrounds ----
panel_bg(ax, 0.15, 3.5, 5.0, 6.3, C_OFFLINE, label="OFFLINE: learn intuition (before play)")
panel_bg(ax, 9.2, 3.5, 6.65, 6.3, C_ONLINE, label="ONLINE: search with it (every decision)")

# ================= LEFT: offline pipeline =================
b1 = box(ax, 0.55, 7.3, 4.2, 1.5,
         "Generate random poker\nsituations (pot, board,\nboth players' ranges)", fc="white", fs=9)
b2 = box(ax, 0.55, 5.0, 4.2, 1.5,
         "Solve each with CFR+\n(no card abstraction) →\ntargets = counterfactual values", fc="white", fs=9)
arrow(ax, bc(b1), tc(b2))

# ================= SHARED: CFV network (highlighted) =================
net = box(ax, 5.6, 5.15, 3.6, 2.6,
          "Deep counterfactual value\n(CFV) networks\nflop / turn / pre-flop-aux\n7×500 PReLU, zero-sum head\nin: pot + ranges (1,000 clusters)\nout: per-hand CFV (× pot)",
          fc=C_NET, fs=7.6, lw=1.8)
arrow(ax, rc(b2), lc(net))

# ================= RIGHT: online loop =================
A = box(ax, 9.55, 8.15, 2.85, 1.1, "Current public state", fc="white", fs=9)
B = box(ax, 12.6, 7.75, 3.25, 1.55,
        "Build a sparse, depth-limited\nlook-ahead tree (fold/call/\n2–3 sizes/all-in; depth = end\nof current betting round)", fc="white", fs=7.3)
C = box(ax, 12.85, 5.85, 2.85, 1.3, "CFR re-solve\nthe look-ahead", fc="white", fs=9)
D = box(ax, 9.3, 5.65, 3.35, 1.55, "Sample an action,\nthen discard the strategy", fc="white", fs=8.3)
side = box(ax, 9.7, 3.75, 6.1, 1.55,
           "Carries between decisions ONLY:\nown range r₁ (Bayes-updated on own action)\n+ opponent counterfactual values v₂ (from re-solve)",
           fc=C_ANNOT, fs=7.9)

arrow(ax, rc(A), lc(B))
arrow(ax, bc(B), tc(C))
arrow(ax, lc(C), rc(D))
arrow(ax, bc(D), (side[0] + 1.4, side[1] + side[3]))
arrow(ax, bc(net), (C[0] + 0.4, C[1]), dashed=True, color="#8a6d1a", rad=-0.35)
arrow(ax, (side[0] + 0.3, side[1] + side[3] * 0.5), lc(A), rad=-0.5)

note(ax, 10.9, 5.15, "leaf values (depth limit)", fs=7.2, color="#8a6d1a")
note(ax, 8.9, 4.9, "loops back for\nthe next decision", fs=7.2)

save(fig, str(Path(__file__).parent / "deepstack_arch.png"))
