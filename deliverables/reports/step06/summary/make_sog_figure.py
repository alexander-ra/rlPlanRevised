"""Generate Figure 6.5 for the Step 6 summary: Student of Games architecture.

Two side-by-side panels (GT-CFR search / sound self-play training) sharing
one highlighted CVPN block, echoing the DeepStack (6.1) and ReBeL (6.4)
figures since SoG generalizes both. A footer strip spans both panels naming
the unification across game classes.

Print legibility: same geometry as the ReBeL figure (~8 in canvas, printed at
96 % of the text width), all text fs 10, panel titles fs 11. The CVPN feeds the
search through a dashed arrow in the white gutter between the panels; the new
network is pushed back to the actors through the outer right lane, so no
arrow crosses a box. Output: sog_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_ANNOT, C_NET, EC,
)

FS = 10
NET_C = "#8a6d1a"
PUSH_C = "#1f4a1f"

fig, ax = new_fig(w=20.0, h=18.7, xlim=(0, 20.0), ylim=(0, 18.7), shrink=2.47)

PB, PT = 3.1, 15.9
panel_bg(ax, 0.1, PB, 9.65, PT - PB, C_OFFLINE,
         label="GT-CFR SEARCH (one decision):\ngrow the tree, solve the tree",
         label_fs=11, label_ha="left", label_dy=0.62)
panel_bg(ax, 10.25, PB, 9.65, PT - PB, C_ONLINE,
         label="SOUND SELF-PLAY\n(training)", label_fs=11, label_ha="left", label_dy=0.62)

# ---- shared network (top) ----
net = box(ax, 7.4, 16.3, 9.2, 2.2,
          "CVPN: f(β) → (counterfactual\nvalues v, prior policy p)\nβ = (public state, beliefs r over\neach player's information states)",
          fc=C_NET, fs=FS, lw=1.8)
note(ax, 7.1, 17.4, "one network, both outputs,\nall game stages", fs=FS, ha="right")

# ================= LEFT: GT-CFR search cycle =================
LX, BW = 0.8, 8.5
G1 = box(ax, LX, 12.2, BW, 2.2,
         "Regret-update phase: run\npublic-tree CFR⁺ on the current\ntree; at each leaf, query the\nCVPN for leaf values",
         fc="white", fs=FS)
G2 = box(ax, LX, 7.1, BW, 3.7,
         "Expansion phase: simulate a\nPUCT-guided trajectory mixing\nthe learned prior with the\ncurrent CFR policy\n(½π_PUCT + ½π_CFR); add the first\nunvisited public state to the tree",
         fc="white", fs=FS)
arrow(ax, (LX + BW - 0.6, G1[1]), (LX + BW - 0.6, G2[1] + G2[3]), lw=1.6)
arrow(ax, (LX + 0.6, G2[1] + G2[3]), (LX + 0.6, G1[1]), lw=1.6)
note(ax, LX + BW / 2, 11.5, "expand the tree,\nimprove the policy, …", fs=FS)

note(ax, LX + BW / 2, 5.95,
     "k = 1 for perfect information\n(one best action, MCTS-like);\nk = ∞ for imperfect information\n(all children, so the policy can mix)",
     fs=FS)

# tiny growing-tree callout
tx, ty = 1.7, 4.6
ax.plot([tx, tx - 0.35, tx, tx + 0.35], [ty, ty - 0.55, ty, ty - 0.55], "o-", color=EC, ms=3, lw=1.0, zorder=3)
ax.plot([tx, tx], [ty, ty - 0.55], "-", color=EC, lw=1.0, zorder=3)
ax.plot([tx - 0.35, tx - 0.6], [ty - 0.55, ty - 1.05], "o-", color="#8a8a8a", ms=3, lw=0.9, zorder=3)
note(ax, 2.7, 4.05, "tree grows\nacross iterations", fs=FS, ha="left")

# ================= RIGHT: sound self-play training =================
RX = 10.75
S1 = box(ax, RX, 13.15, BW, 1.3, "Play a self-play game, running a\nGT-CFR search at every decision", fc="white", fs=FS)
S2 = box(ax, RX, 10.45, BW, 2.2,
         "Collect data: full-game trajectories\n(policy + outcome targets) AND every\nbelief state the CVPN was queried at\n(the \"queries\")",
         fc="white", fs=FS)
S3 = box(ax, RX, 7.35, BW, 2.6,
         "Solve the queries with another\n(recursive) GT-CFR search →\ncounterfactual-value targets\n(queries may spawn sub-searches\nthat add still more queries)",
         fc="white", fs=FS)
S4 = box(ax, RX, 4.25, BW, 2.6,
         "Train the CVPN (Huber loss on\nvalues, cross-entropy on policy)\non a replay buffer; periodically\npush the new net to the actors",
         fc="white", fs=FS)
for a, b in ((S1, S2), (S2, S3), (S3, S4)):
    arrow(ax, bc(a), tc(b))
note(ax, RX + BW / 2, 3.65, "no human data; no blueprint;\nno card abstraction", fs=FS)

# push the new net back: outer right lane, then into the CVPN's right side
MXR = 19.6
ny = cc(net)[1]
arrow(ax, rc(S4), (MXR, rc(S4)[1]), style="-", color=PUSH_C, lw=1.7)
arrow(ax, (MXR, rc(S4)[1]), (MXR, ny), style="-", color=PUSH_C, lw=1.7)
arrow(ax, (MXR, ny), rc(net), color=PUSH_C, lw=1.7)
note(ax, 18.1, 18.05, "push new\nnet", fs=FS, color=PUSH_C)

# CVPN -> search, down the white gutter
yG1 = cc(G1)[1]
arrow(ax, (9.95, net[1]), (9.95, yG1), style="-", dashed=True, color=NET_C, lw=1.5)
arrow(ax, (9.95, yG1), rc(G1), dashed=True, color=NET_C, lw=1.5)

# ================= footer strip =================
box(ax, 0.3, 1.4, 19.4, 1.4,
    "one algorithm · one network · one search\n→ chess · Go · heads-up poker · Scotland Yard",
    fc="#eceff3", fs=FS, fontweight="bold")
note(ax, 5.0, 0.7, "perfect-information games\n(k = 1, AlphaZero-like regime)", fs=FS)
note(ax, 15.0, 0.7, "imperfect-information games\n(k = ∞, CFR-like regime)", fs=FS)

save(fig, str(Path(__file__).parent / "sog_arch.png"))
