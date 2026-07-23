"""§5 figure: CTDE = centralized training, decentralized execution.

Left panel (TRAINING): a centralized critic/value sees the global state + the joint action and
produces low-variance value targets that update both actors. Right panel (EXECUTION): each actor
acts on its own local observation only -- no critic, no message passing. The training/execution
asymmetry is the whole idea.
Output: ctde_architecture.png. Run with the project .venv active; the PNG lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, panel_bg, save
from _diagram_utils import C_SAFE, C_MODEL, C_NET, C_ANNOT, EC, C_PANEL_BG_A, C_PANEL_BG_B

fig, ax = new_fig(w=15, h=8.2, xlim=(0, 15), ylim=(0, 8.2), shrink=1.6)

# ---- panel backgrounds ----
panel_bg(ax, 0.2, 0.3, 7.1, 7.6, C_PANEL_BG_A, label="TRAINING (centralized)")
panel_bg(ax, 7.7, 0.3, 7.1, 7.6, C_PANEL_BG_B, label="EXECUTION (decentralized)")

# ---- TRAINING ----
critic = box(ax, 1.5, 5.4, 4.4, 1.2, "Centralized critic  $Q(s,\\,a_1,a_2)$\n(low-variance target)",
             fc=C_NET, fs=8.8, fontweight="bold")
gs = box(ax, 0.7, 3.7, 2.5, 0.9, "global state $s$", fc=C_SAFE, fs=8.2)
ja = box(ax, 4.2, 3.7, 2.5, 0.9, "joint action $a_1,a_2$", fc=C_SAFE, fs=8.2)
act1 = box(ax, 0.7, 1.6, 2.5, 1.0, "Actor 1\n$\\pi_1(a_1\\mid o_1)$", fc=C_MODEL, fs=8.4)
act2 = box(ax, 4.2, 1.6, 2.5, 1.0, "Actor 2\n$\\pi_2(a_2\\mid o_2)$", fc=C_MODEL, fs=8.4)

arrow(ax, (1.95, 4.6), (2.6, 5.4))
arrow(ax, (5.45, 4.6), (4.8, 5.4))
arrow(ax, (1.95, 2.6), (1.95, 3.7))
arrow(ax, (5.45, 2.6), (5.45, 3.7))
# critic teaches both actors (dashed = gradient signal at training only)
arrow(ax, (2.6, 5.4), (1.95, 2.6), color="#a5453a", lw=1.4, dashed=True, rad=0.32)
arrow(ax, (4.8, 5.4), (5.45, 2.6), color="#a5453a", lw=1.4, dashed=True, rad=-0.32)
note(ax, 3.7, 0.95, "the critic sees everything; it makes each actor's world look stationary",
     fs=7.8, color="#2c3e50")

# ---- EXECUTION ----
e1 = box(ax, 8.4, 3.9, 2.5, 1.0, "Actor 1\n$\\pi_1(a_1\\mid o_1)$", fc=C_MODEL, fs=8.4)
e2 = box(ax, 11.5, 3.9, 2.5, 1.0, "Actor 2\n$\\pi_2(a_2\\mid o_2)$", fc=C_MODEL, fs=8.4)
o1 = box(ax, 8.4, 5.6, 2.5, 0.9, "local obs $o_1$", fc=C_SAFE, fs=8.2)
o2 = box(ax, 11.5, 5.6, 2.5, 0.9, "local obs $o_2$", fc=C_SAFE, fs=8.2)
u1 = box(ax, 8.4, 2.1, 2.5, 0.9, "action $a_1$", fc=C_ANNOT, fs=8.2)
u2 = box(ax, 11.5, 2.1, 2.5, 0.9, "action $a_2$", fc=C_ANNOT, fs=8.2)

arrow(ax, (9.65, 5.6), (9.65, 4.9))
arrow(ax, (12.75, 5.6), (12.75, 4.9))
arrow(ax, (9.65, 3.9), (9.65, 3.0))
arrow(ax, (12.75, 3.9), (12.75, 3.0))

note(ax, 11.2, 0.95, "no critic, no messages: each actor is on its own, on local obs",
     fs=7.8, color="#2c3e50")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ctde_architecture.png"))
