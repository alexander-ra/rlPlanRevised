"""§5 figure: CTDE = centralized training, decentralized execution.

Left panel (TRAINING): a centralized critic/value sees the global state + the joint action and
produces low-variance value targets that update both actors. Right panel (EXECUTION): each actor
acts on its own local observation only -- no critic, no message passing. The training/execution
asymmetry is the whole idea.
Output: ctde_architecture.png. Run with the project .venv active; the PNG lands next to this file.

Sizes: the figure prints at ~0.77 of its matplotlib size, so every label is fs 11 (~8.5 pt).
"""
import os

from _diagram_utils import new_fig, box, arrow, note, panel_bg, save
from _diagram_utils import C_SAFE, C_MODEL, C_NET, C_ANNOT, EC, C_PANEL_BG_A, C_PANEL_BG_B

FS = 11

fig, ax = new_fig(w=15, h=8.2, xlim=(0, 15), ylim=(0, 8.2), shrink=1.6)

# ---- panel backgrounds ----
panel_bg(ax, 0.2, 0.3, 7.1, 7.6, C_PANEL_BG_A, label="TRAINING (centralized)", label_fs=FS)
panel_bg(ax, 7.7, 0.3, 7.1, 7.6, C_PANEL_BG_B, label="EXECUTION (decentralized)", label_fs=FS)

# ---- TRAINING ----
critic = box(ax, 1.2, 5.4, 5.1, 1.6,
             "Centralized critic\n$Q(s,\\,a_1,a_2)$\n(low-variance target)",
             fc=C_NET, fs=FS, fontweight="bold")
gs = box(ax, 0.5, 3.4, 2.9, 1.2, "global state $s$", fc=C_SAFE, fs=FS)
ja = box(ax, 4.1, 3.4, 2.9, 1.2, "joint action $a_1,a_2$", fc=C_SAFE, fs=FS)
act1 = box(ax, 0.7, 1.6, 2.5, 1.0, "Actor 1\n$\\pi_1(a_1\\mid o_1)$", fc=C_MODEL, fs=FS)
act2 = box(ax, 4.3, 1.6, 2.5, 1.0, "Actor 2\n$\\pi_2(a_2\\mid o_2)$", fc=C_MODEL, fs=FS)

arrow(ax, (1.95, 4.6), (2.6, 5.4))
arrow(ax, (5.55, 4.6), (4.9, 5.4))
arrow(ax, (1.95, 2.6), (1.95, 3.4))
arrow(ax, (5.55, 2.6), (5.55, 3.4))
# critic teaches both actors (dashed = gradient signal at training only)
arrow(ax, (2.6, 5.4), (1.95, 2.6), color="#a5453a", lw=1.4, dashed=True, rad=0.32)
arrow(ax, (4.9, 5.4), (5.55, 2.6), color="#a5453a", lw=1.4, dashed=True, rad=-0.32)
note(ax, 3.75, 0.85, "the critic sees everything:\neach actor's world looks stationary",
     fs=FS, color="#2c3e50")

# ---- EXECUTION ----
e1 = box(ax, 8.3, 3.7, 2.5, 1.0, "Actor 1\n$\\pi_1(a_1\\mid o_1)$", fc=C_MODEL, fs=FS)
e2 = box(ax, 11.7, 3.7, 2.5, 1.0, "Actor 2\n$\\pi_2(a_2\\mid o_2)$", fc=C_MODEL, fs=FS)
o1 = box(ax, 8.2, 5.4, 2.7, 1.2, "local\nobservation $o_1$", fc=C_SAFE, fs=FS)
o2 = box(ax, 11.6, 5.4, 2.7, 1.2, "local\nobservation $o_2$", fc=C_SAFE, fs=FS)
u1 = box(ax, 8.3, 2.0, 2.5, 0.9, "action $a_1$", fc=C_ANNOT, fs=FS)
u2 = box(ax, 11.7, 2.0, 2.5, 0.9, "action $a_2$", fc=C_ANNOT, fs=FS)

arrow(ax, (9.55, 5.4), (9.55, 4.7))
arrow(ax, (12.95, 5.4), (12.95, 4.7))
arrow(ax, (9.55, 3.7), (9.55, 2.9))
arrow(ax, (12.95, 3.7), (12.95, 2.9))

note(ax, 11.25, 0.85, "no critic, no messages:\neach actor relies on its own observation",
     fs=FS, color="#2c3e50")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ctde_architecture.png"))
