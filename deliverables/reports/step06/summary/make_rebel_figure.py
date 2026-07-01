"""Generate Figure 6.4 for the Step 6 summary: ReBeL architecture.

Two side-by-side panels (training self-play RL+search / test-time play)
sharing one highlighted PBS value+policy network, echoing the DeepStack
figure since ReBeL generalizes that design. A shared belief-state definition
box spans the bottom. Output: rebel_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_ANNOT, C_NET, EC,
)

fig, ax = new_fig(w=17.4, h=11.6, xlim=(-1.0, 18.0), ylim=(0.3, 12.7))

panel_bg(ax, 0.15, 2.5, 7.5, 8.4, C_OFFLINE, label="TRAINING: self-play RL + search (AlphaZero-style)", label_fs=9.6)
panel_bg(ax, 8.35, 2.5, 7.7, 8.4, C_ONLINE, label="TEST / PLAY: the same search", label_fs=9.6)

net = box(ax, 6.6, 11.1, 3.2, 1.15,
           "PBS value (+ policy) network\nf(β) → infostate values, policy",
           fc=C_NET, fs=8.0, lw=1.8)

# ================= LEFT: training loop =================
L1 = box(ax, 0.45, 9.1, 6.9, 0.85, "① Current PBS β", fc="white", fs=8.6)
L2 = box(ax, 0.45, 6.9, 6.9, 1.15,
          "② Construct a depth-limited subgame rooted at β\n(fixed depth: end of the current betting round)", fc="white", fs=8.0)
L3 = box(ax, 0.45, 5.55, 6.9, 1.15, "③ Solve it with CFR", fc="white", fs=8.6)
L4 = box(ax, 0.45, 3.95, 6.9, 1.4,
          "④ Emit training data: add (β, average infostate-\nvalues) → value-net dataset; (β, average policy)\n→ policy-net dataset", fc="white", fs=7.8)
L5 = box(ax, 0.45, 2.7, 6.9, 1.05, "⑤ Sample a leaf PBS on a random CFR iteration", fc="white", fs=8.0)

arrow(ax, bc(L1), tc(L2))
arrow(ax, bc(L2), tc(L3))
arrow(ax, bc(L3), tc(L4))
arrow(ax, bc(L4), tc(L5))

MXL = -0.35
arrow(ax, lc(L5), (MXL, L5[1] + L5[3] * 0.5), style="-", lw=1.8, color="#1f4a1f")
arrow(ax, (MXL, L5[1] + L5[3] * 0.5), (MXL, L1[1] + L1[3] * 0.5), style="-", lw=1.8, color="#1f4a1f")
arrow(ax, (MXL, L1[1] + L1[3] * 0.5), lc(L1), lw=1.8, color="#1f4a1f")
note(ax, -0.55, 5.4, "retrain nets,\nthen repeat\nthe whole loop", fs=7.2, color="#1f4a1f", ha="center")
note(ax, 6.9, 10.15, "no blueprint, no abstraction — the only\nstored artefacts are the two nets", fs=6.3, ha="right")

arrow(ax, (net[0] + 0.6, net[1]), (L3[0] + L3[2] * 0.8, L3[1] + L3[3]), dashed=True, color="#8a6d1a", rad=-0.1)

# ================= RIGHT: test / play loop =================
R1 = box(ax, 8.65, 8.85, 6.9, 1.0, "① Root a subgame at the current PBS", fc="white", fs=8.6)
R2 = box(ax, 8.65, 5.95, 6.9, 1.25, "② Run CFR with the value net at the leaves", fc="white", fs=8.6)
R3 = box(ax, 8.65, 4.2, 6.9, 1.4,
          "③ Pick the policy of a random CFR iteration —\nthis is what makes test-time search provably\nsafe, with no extra constraints", fc="white", fs=7.9)
R4 = box(ax, 8.65, 2.85, 6.9, 1.0, "④ Act", fc="white", fs=9.5)

arrow(ax, bc(R1), tc(R2))
arrow(ax, bc(R2), tc(R3))
arrow(ax, bc(R3), tc(R4))

MXR = 16.55
arrow(ax, rc(R4), (MXR, R4[1] + R4[3] * 0.5), style="-", lw=1.6)
arrow(ax, (MXR, R4[1] + R4[3] * 0.5), (MXR, R1[1] + R1[3] * 0.5), style="-", lw=1.6)
arrow(ax, (MXR, R1[1] + R1[3] * 0.5), rc(R1), lw=1.6)
note(ax, 16.65, 5.4, "opponent bets off-tree →\nadd that exact bet to the\nsubgame and re-solve", fs=7.0, ha="left")

arrow(ax, (net[0] + net[2] - 0.6, net[1]), (R2[0] + R2[2] * 0.2, R2[1] + R2[3]), dashed=True, color="#8a6d1a", rad=0.1)
note(ax, 8.9, 10.15, "leaf value = v̂(infostate | beliefs\nat the leaf this iteration)", fs=6.3, ha="left")

# ================= shared belief-state definition =================
belief = box(ax, 0.4, 0.5, 15.4, 1.55,
              "Public belief state (PBS) β = a probability distribution over each player's possible hidden\n"
              "states (in HUNL, both players' 1,326 possible two-card hands), conditioned on the public\n"
              "history; Bayes-updated after every public action.",
              fc=C_ANNOT, fs=8.2)
note(ax, 8.1, 2.35, "values are well-defined on a PBS — unlike on a public state alone", fs=7.4)
arrow(ax, (2.5, belief[1] + belief[3]), lc(L5), rad=0.2, color="#7b8a99")
arrow(ax, (13.5, belief[1] + belief[3]), lc(R4), rad=-0.2, color="#7b8a99")

save(fig, str(Path(__file__).parent / "rebel_arch.png"))
