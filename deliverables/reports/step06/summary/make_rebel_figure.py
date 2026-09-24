"""Generate Figure 6.4 for the Step 6 summary: ReBeL architecture.

Two side-by-side panels (training self-play RL+search / test-time play)
sharing one highlighted PBS value+policy network, echoing the DeepStack
figure since ReBeL generalizes that design. A shared belief-state definition
box spans the bottom.

Print legibility: the canvas is ~8 in wide and the figure prints at 96 % of
the text width (16.9 cm), so fs 10 prints at ~8.3 pt and the fs 11 titles at
~9.1 pt. Boxes are sized for the longer (Bulgarian) labels. The net feeds both
loops through dashed arrows in the white gutter between the panels, so no
arrow crosses a box; each loop-back arrow runs in its panel's outer lane.
Output: rebel_arch.png in this directory.
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
LOOP_C = "#1f4a1f"

fig, ax = new_fig(w=20.0, h=17.5, xlim=(0, 20.0), ylim=(0, 17.5), shrink=2.47)

# ---- panels (titles left-aligned, two lines) ----
PB, PT = 3.4, 15.5
panel_bg(ax, 0.1, PB, 9.65, PT - PB, C_OFFLINE,
         label="TRAINING: self-play RL + search\n(AlphaZero-style)",
         label_fs=11, label_ha="left", label_dy=0.62)
panel_bg(ax, 10.25, PB, 9.65, PT - PB, C_ONLINE,
         label="TEST / PLAY:\nthe same search", label_fs=11, label_ha="left", label_dy=0.62)

# ---- shared network (top) ----
net = box(ax, 7.0, 15.9, 11.2, 1.35,
          "PBS value (+ policy) network\nf(β) → infostate values, policy",
          fc=C_NET, fs=FS, lw=1.8)
note(ax, 6.7, 16.55, "no blueprint, no abstraction —\nthe only stored artefacts\nare the two nets",
     fs=FS, ha="right")

# ================= LEFT: training loop =================
LX, BW = 0.8, 8.5
L1 = box(ax, LX, 13.25, BW, 0.9, "① Current PBS β", fc="white", fs=FS)
L2 = box(ax, LX, 10.95, BW, 1.75,
         "② Construct a depth-limited subgame\nrooted at β (fixed depth: end of\nthe current betting round)",
         fc="white", fs=FS)
L3 = box(ax, LX, 9.5, BW, 0.9, "③ Solve it with CFR", fc="white", fs=FS)
L4 = box(ax, LX, 6.35, BW, 2.6,
         "④ Emit training data:\n(β, average infostate values)\n→ value-net dataset;\n(β, average policy)\n→ policy-net dataset",
         fc="white", fs=FS)
L5 = box(ax, LX, 3.65, BW, 2.15,
         "⑤ Sample a leaf PBS on a random\nCFR iteration → the next β; after\nthe game, retrain the nets and\nrepeat the whole loop",
         fc="white", fs=FS)
for a, b in ((L1, L2), (L2, L3), (L3, L4), (L4, L5)):
    arrow(ax, bc(a), tc(b))

# loop-back in the left lane: leaf -> next root
MXL = 0.4
arrow(ax, lc(L5), (MXL, lc(L5)[1]), style="-", lw=1.8, color=LOOP_C)
arrow(ax, (MXL, lc(L5)[1]), (MXL, lc(L1)[1]), style="-", lw=1.8, color=LOOP_C)
arrow(ax, (MXL, lc(L1)[1]), lc(L1), lw=1.8, color=LOOP_C)

# ================= RIGHT: test / play loop =================
RX = 10.75
R1 = box(ax, RX, 13.25, BW, 0.9, "① Root a subgame at the current PBS", fc="white", fs=FS)
R2 = box(ax, RX, 10.4, BW, 2.15,
         "② Run CFR with the value net at the\nleaves; leaf value = v̂(infostate |\nbeliefs at the leaf on this iteration)",
         fc="white", fs=FS)
R3 = box(ax, RX, 7.1, BW, 2.6,
         "③ Pick the policy of a random CFR\niteration — this is what makes\ntest-time search provably safe,\nwith no extra constraints",
         fc="white", fs=FS)
R4 = box(ax, RX, 5.5, BW, 0.9, "④ Act", fc="white", fs=FS)
for a, b in ((R1, R2), (R2, R3), (R3, R4)):
    arrow(ax, bc(a), tc(b))

MXR = 19.6
arrow(ax, rc(R4), (MXR, rc(R4)[1]), style="-", lw=1.6)
arrow(ax, (MXR, rc(R4)[1]), (MXR, rc(R1)[1]), style="-", lw=1.6)
arrow(ax, (MXR, rc(R1)[1]), rc(R1), lw=1.6)
note(ax, 15.0, 4.45, "opponent bets off-tree →\nadd that exact bet to the\nsubgame and re-solve", fs=FS)

# ---- net -> both searches, down the white gutter between the panels ----
yL3, yR2 = cc(L3)[1], cc(R2)[1]
arrow(ax, (9.9, net[1]), (9.9, yL3), style="-", dashed=True, color=NET_C, lw=1.5)
arrow(ax, (9.9, yL3), rc(L3), dashed=True, color=NET_C, lw=1.5)
arrow(ax, (10.1, net[1]), (10.1, yR2), style="-", dashed=True, color=NET_C, lw=1.5)
arrow(ax, (10.1, yR2), lc(R2), dashed=True, color=NET_C, lw=1.5)

# ================= shared belief-state definition =================
note(ax, 10.0, 2.9, "values are well-defined on a PBS — unlike on a public state alone", fs=FS)
box(ax, 0.3, 0.3, 19.4, 2.2,
    "Public belief state (PBS) β = a probability distribution over each player's possible hidden\n"
    "states (in HUNL, both players' 1,326 possible two-card hands), conditioned on the public\n"
    "history; Bayes-updated after every public action.",
    fc=C_ANNOT, fs=FS)

save(fig, str(Path(__file__).parent / "rebel_arch.png"))
