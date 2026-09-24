"""summary figure: evolutionary game theory <-> population-based training.

The replicator equation (share grows in proportion to how much a strategy beats the population
average) is the continuous-time idealization of what a PBT league does discretely: copy the
fitter agents (selection) and perturb their hyper-parameters (mutation). Stable rest points of the
replicator flow include every ESS (asymptotically stable); the league's counterpart is the
meta-Nash mixture it is trying to reach. Output: replicator_selection.png. Run with the project
.venv active; the PNG lands next to this file.

Drawn at print size: the canvas is 7.0 in wide (the 17.6 cm text width), all text is fs 10.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save, panel_bg
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_PANEL_BG_A, C_PANEL_BG_B

fig, ax = new_fig(w=14, h=11.2, xlim=(0, 14), ylim=(0.45, 11.5), shrink=2.0)

panel_bg(ax, 0.2, 2.0, 6.7, 9.4, C_PANEL_BG_B, label="Evolutionary game theory")
panel_bg(ax, 7.1, 2.0, 6.7, 9.4, C_PANEL_BG_A, label="PBT league (this chapter)")

W, H = 6.3, 1.7
LX, RX = 0.4, 7.3
ROWS = (8.9, 6.75, 4.6, 2.45)

# left column: EGT
eq = box(ax, LX, ROWS[0], W, H,
         "Replicator: $\\dot{x}_i = x_i\\,[\\,f_i(x) - \\bar f(x)\\,]$\n"
         "a share grows if it beats\nthe population average",
         fc=C_MODEL, fs=10)
sel = box(ax, LX, ROWS[1], W, H, "Selection\n(fitter shares expand)", fc=C_SAFE, fs=10)
mut = box(ax, LX, ROWS[2], W, H, "Mutation / drift\n(explore nearby strategies)", fc=C_SAFE, fs=10)
rest = box(ax, LX, ROWS[3], W, H, "Stable rest points = ESS\n(no small mutant share\ncan invade)",
           fc=C_NET, fs=10)

# right column: PBT
pop = box(ax, RX, ROWS[0], W, H,
          "Population of neural PPO agents\n(main agents, main exploiters,\nleague exploiters)",
          fc=C_MODEL, fs=10)
copy = box(ax, RX, ROWS[1], W, H,
           "Exploit step: copy the top agents\n(fitness = share of wins\nagainst the population)",
           fc=C_SAFE, fs=10)
pert = box(ax, RX, ROWS[2], W, H, "Explore step: perturb lr / entropy\n(mutate hyper-parameters)",
           fc=C_SAFE, fs=10)
conv = box(ax, RX, ROWS[3], W, H, "Meta-Nash of the league\n(measured by exact exploitability)",
           fc=C_NET, fs=10)

# vertical flow within each column
for b_top, b_bot in [(eq, sel), (sel, mut), (mut, rest), (pop, copy), (copy, pert), (pert, conv)]:
    arrow(ax, (b_top[0] + b_top[2] / 2, b_top[1]), (b_bot[0] + b_bot[2] / 2, b_bot[1] + b_bot[3]))

# cross-column mapping arrows (dashed = "is the discrete analog of")
for b_l, b_r in [(sel, copy), (mut, pert), (rest, conv)]:
    arrow(ax, (b_l[0] + b_l[2], b_l[1] + b_l[3] / 2), (b_r[0], b_r[1] + b_r[3] / 2),
          color="#8a97a6", lw=1.2, dashed=True, rad=0.0)

note(ax, 7.0, 1.05,
     'dashed = "discrete analog of": the league is replicator dynamics\n'
     "with learned agents instead of fixed strategy shares",
     fs=10, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "replicator_selection.png"))
