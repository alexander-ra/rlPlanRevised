"""§1 figure: non-stationarity as two partners learning to dance at once.

Two agents, each best-responding to the OTHER's current policy (solid arrows), while that
policy is itself moving because the other agent is optimizing back (dashed arrows). The target
each one chases never holds still -> naive learners cycle/over-correct rather than converge.
Output: nonstationarity_dance.png. Run from the repo root (or anywhere) with the project .venv
active; the PNG lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_EXPLOIT, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.2, xlim=(0, 14), ylim=(0, 7.2), shrink=1.7)

# the two learning agents
box(ax, 1.0, 3.0, 3.4, 1.4, "Agent 1\npolicy $\\pi_1$ (learning)", fc=C_MODEL, fs=9.5,
    fontweight="bold")
box(ax, 9.6, 3.0, 3.4, 1.4, "Agent 2\npolicy $\\pi_2$ (learning)", fc=C_EXPLOIT, fs=9.5,
    fontweight="bold")

# solid: each best-responds to the other's CURRENT policy
arrow(ax, (4.4, 4.1), (9.6, 4.1), color=EC, lw=1.8, rad=-0.28)
note(ax, 7.0, 5.55, "best-responds to $\\pi_2$ (as it is now)", fs=8.4, color="#2c3e50")
arrow(ax, (9.6, 3.3), (4.4, 3.3), color=EC, lw=1.8, rad=-0.28)
note(ax, 7.0, 1.95, "best-responds to $\\pi_1$ (as it is now)", fs=8.4, color="#2c3e50")

# dashed: but the target is moving because the other updates too
arrow(ax, (2.7, 4.4), (2.7, 5.6), color="#a5453a", lw=1.6, dashed=True)
note(ax, 2.7, 5.95, "...but $\\pi_1$ keeps moving", fs=7.8, color="#a5453a")
arrow(ax, (11.3, 2.8), (11.3, 1.6), color="#a5453a", lw=1.6, dashed=True)
note(ax, 11.3, 1.2, "...but $\\pi_2$ keeps moving", fs=7.8, color="#a5453a")

# the moral
box(ax, 3.6, 0.15, 6.8, 0.72,
    "non-stationarity: each agent's target is another learner, so it never holds still",
    fc=C_ANNOT, fs=8.6, fontweight="bold")

note(ax, 7.0, 6.75,
     "Single-agent RL assumes a fixed world; here the 'world' is a partner who is also learning.",
     fs=8.6, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "nonstationarity_dance.png"))
