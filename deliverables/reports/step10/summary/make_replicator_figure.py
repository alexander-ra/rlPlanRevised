"""summary figure: evolutionary game theory <-> population-based training.

The replicator equation (share grows in proportion to how much a strategy beats the population
average) is the continuous-time idealization of what a PBT league does discretely: copy the
fitter agents (selection) and perturb their hyper-parameters (mutation). Rest points of the
replicator flow correspond to Nash / ESS. Output: replicator_selection.png. Run with the project
.venv active; the PNG lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save, panel_bg
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_ANNOT, C_PANEL_BG_A, C_PANEL_BG_B, EC

fig, ax = new_fig(w=14, h=8.6, xlim=(0, 14), ylim=(0, 8.6), shrink=1.65)

panel_bg(ax, 0.2, 0.4, 6.6, 7.8, C_PANEL_BG_B, label="Evolutionary game theory")
panel_bg(ax, 7.2, 0.4, 6.6, 7.8, C_PANEL_BG_A, label="PBT league (this step)")

# left column: EGT
eq = box(ax, 0.6, 6.2, 5.8, 1.3,
         "Replicator: $\\dot{x}_i = x_i\\,[\\,f_i(x) - \\bar f(x)\\,]$\nshare grows if it beats the population avg",
         fc=C_MODEL, fs=8.6, fontweight="bold")
sel = box(ax, 0.6, 4.4, 5.8, 1.1, "Selection\n(fitter shares expand)", fc=C_SAFE, fs=8.8)
mut = box(ax, 0.6, 2.7, 5.8, 1.1, "Mutation / drift\n(explore nearby strategies)", fc=C_SAFE, fs=8.8)
rest = box(ax, 0.6, 1.0, 5.8, 1.1, "Rest points $\\leftrightarrow$ Nash / ESS\n(fixed shares, no profitable deviation)",
           fc=C_NET, fs=8.4, fontweight="bold")

# right column: PBT
pop = box(ax, 7.6, 6.2, 5.8, 1.3, "Population of neural PPO agents\n(main / main-exploiter / league-exploiter)",
          fc=C_MODEL, fs=8.4, fontweight="bold")
copy = box(ax, 7.6, 4.4, 5.8, 1.1, "Exploit step: copy the top agents\n(fitness = win-rate vs population)", fc=C_SAFE, fs=8.6)
pert = box(ax, 7.6, 2.7, 5.8, 1.1, "Explore step: perturb lr / entropy\n(mutate hyper-parameters)", fc=C_SAFE, fs=8.6)
conv = box(ax, 7.6, 1.0, 5.8, 1.1, "Meta-Nash of the league\n(measured by exact exploitability)", fc=C_NET, fs=8.4, fontweight="bold")

# vertical flow within each column
for b_top, b_bot in [(eq, sel), (sel, mut), (mut, rest), (pop, copy), (copy, pert), (pert, conv)]:
    arrow(ax, (b_top[0] + b_top[2] / 2, b_top[1]), (b_bot[0] + b_bot[2] / 2, b_bot[1] + b_bot[3]))

# cross-column mapping arrows (dashed = "is the discrete analog of")
for b_l, b_r in [(sel, copy), (mut, pert), (rest, conv)]:
    arrow(ax, (b_l[0] + b_l[2], b_l[1] + b_l[3] / 2), (b_r[0], b_r[1] + b_r[3] / 2),
          color="#8a97a6", lw=1.2, dashed=True, rad=0.0)

note(ax, 7.0, 0.15,
     "dashed = 'discrete analog of': the league is replicator dynamics with learned agents instead of fixed strategy shares",
     fs=7.6, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "replicator_selection.png"))
