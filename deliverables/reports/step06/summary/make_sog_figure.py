"""Generate Figure 6.5 for the Step 6 summary: Student of Games architecture.

Two side-by-side panels (GT-CFR search / sound self-play training) sharing
one highlighted CVPN block, echoing the DeepStack (6.1) and ReBeL (6.4)
figures since SoG generalizes both. A footer strip spans both panels naming
the unification across game classes. Output: sog_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_ANNOT, C_NET, EC,
)
import matplotlib.pyplot as plt

fig, ax = new_fig(w=17.4, h=11.6, xlim=(-1.0, 18.0), ylim=(0.4, 12.7))

panel_bg(ax, 0.15, 2.9, 7.5, 7.6, C_OFFLINE, label="GT-CFR SEARCH (one decision): grow the tree, solve the tree", label_fs=9.0)
panel_bg(ax, 8.35, 2.9, 7.7, 7.6, C_ONLINE, label="SOUND SELF-PLAY (training)", label_fs=9.6)

net = box(ax, 6.4, 11.0, 3.6, 1.35,
           "CVPN: f(β) → (counterfactual\nvalues v, prior policy p)\nβ = (public state, beliefs r over\neach player's information states)",
           fc=C_NET, fs=7.6, lw=1.8)
note(ax, 8.2, 10.75, "one network, both outputs, all game stages", fs=6.9, ha="center")

# ================= LEFT: GT-CFR search cycle =================
G1 = box(ax, 0.45, 7.9, 6.9, 1.75,
          "Regret-update phase: run public-tree\nCFR⁺ on the current tree; at each leaf,\nquery the CVPN for leaf values", fc="white", fs=8.0)
G2 = box(ax, 0.45, 5.4, 6.9, 1.9,
          "Expansion phase: simulate a PUCT-guided\ntrajectory mixing the learned prior with the\ncurrent CFR policy (½π_PUCT + ½π_CFR); add\nthe first unvisited public state to the tree", fc="white", fs=7.8)

arrow(ax, (G1[0] + 6.3, G1[1]), (G2[0] + 6.3, G2[1] + G2[3]), lw=1.6)
arrow(ax, (G2[0] + 0.6, G2[1] + G2[3]), (G1[0] + 0.6, G1[1]), lw=1.6)
note(ax, 3.9, 7.5, "expand the tree,\nimprove the policy, …", fs=6.6, style="italic")

arrow(ax, (net[0] + 0.7, net[1]), (G1[0] + G1[2] * 0.75, G1[1] + G1[3]), dashed=True, color="#8a6d1a", rad=-0.1)

note(ax, 3.9, 4.55,
     "k = 1 for perfect-info (one best action, MCTS-like);\nk = ∞ for imperfect-info (all children, so the policy can mix)",
     fs=7.3, ha="center")

# tiny growing-tree callout
tx, ty = 1.1, 3.6
ax.plot([tx, tx - 0.35, tx, tx + 0.35], [ty, ty - 0.55, ty, ty], "o-", color=EC, ms=3, lw=1.0, zorder=3)
ax.plot([tx, tx], [ty, ty - 0.55], "-", color=EC, lw=1.0, zorder=3)
ax.plot([tx - 0.35, tx - 0.55], [ty - 0.55, ty - 1.0], "o-", color="#8a8a8a", ms=3, lw=0.9, zorder=3)
note(ax, 2.3, 3.35, "tree grows\nacross iterations", fs=6.8, ha="left")

# ================= RIGHT: sound self-play training =================
S1 = box(ax, 8.65, 8.35, 6.9, 1.15, "Play a self-play game, running a\nGT-CFR search at every decision", fc="white", fs=8.2)
S2 = box(ax, 8.65, 6.35, 6.9, 1.55,
          "Collect data: full-game trajectories (policy +\noutcome targets) AND every belief state the\nCVPN was queried at (the \"queries\")", fc="white", fs=7.7)
S3 = box(ax, 8.65, 4.55, 6.9, 1.55,
          "Solve the queries with another (recursive) GT-CFR\nsearch → counterfactual-value targets (queries may\nspawn sub-searches that add still more queries)", fc="white", fs=7.5)
S4 = box(ax, 8.65, 2.95, 6.9, 1.35,
          "Train the CVPN (Huber loss on values, cross-\nentropy on policy) on a replay buffer; periodically\npush the new net to the actors", fc="white", fs=7.6)

arrow(ax, bc(S1), tc(S2))
arrow(ax, bc(S2), tc(S3))
arrow(ax, bc(S3), tc(S4))

import numpy as np
rng = np.random.default_rng(7)
px = rng.uniform(S2[0] + 0.5, S2[0] + S2[2] - 0.5, 9)
py = rng.uniform(S2[1] + 0.25, S2[1] + 0.5, 9)
ax.scatter(px, py, s=14, color="#d1418a", zorder=4)

arrow(ax, (S4[0] + S4[2] - 0.6, S4[1] + S4[3]), (net[0] + net[2] - 0.7, net[1]),
      dashed=False, color="#1f4a1f", lw=1.7, rad=0.15)
note(ax, 15.3, 10.55, "push new\nnet", fs=6.8, color="#1f4a1f")
note(ax, 12.1, 9.85, "no human data; no blueprint; no card abstraction", fs=6.6, ha="center")

# ================= footer strip =================
footer = box(ax, 0.15, 1.15, 15.9, 1.35,
              "one algorithm · one network · one search  →  chess · Go · heads-up poker · Scotland Yard",
              fc="#eceff3", fs=9.2, fontweight="bold")
note(ax, 3.5, 1.5, "perfect-information games (k = 1, AlphaZero-like regime)", fs=7.2)
note(ax, 12.5, 1.5, "imperfect-information games (k = ∞, CFR-like regime)", fs=7.2)

save(fig, str(Path(__file__).parent / "sog_arch.png"))
