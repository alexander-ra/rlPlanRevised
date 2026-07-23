"""§3 figure: the MARL method family on two axes.

Horizontal axis: cooperative <-> competitive target setting. Vertical axis: how much is
centralized and when (nothing -> critic at training -> a full meta-game solve; communication
centralizes information at execution). LOLA is the outlier that models the opponent as a LEARNER
rather than as a fixed strategy.
Output: methods_spectrum.png. Run with the project .venv active; the PNG lands next to this file.
"""
import os

from matplotlib.patches import FancyArrowPatch

from _diagram_utils import new_fig, box, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT, EC

fig, ax = new_fig(w=14, h=9.0, xlim=(0, 14), ylim=(0, 10), shrink=1.6)

# ---- axes ----
ax.add_patch(FancyArrowPatch((1.2, 1.2), (13.2, 1.2), arrowstyle="-|>", mutation_scale=14,
                             color=EC, lw=1.6))
ax.add_patch(FancyArrowPatch((1.2, 1.2), (1.2, 9.4), arrowstyle="-|>", mutation_scale=14,
                             color=EC, lw=1.6))
note(ax, 7.2, 0.55, "cooperative  $\\longleftrightarrow$  competitive", fs=9.5, color="#2c3e50",
     style="normal")
note(ax, 0.55, 5.3, "centralization  $\\longrightarrow$", fs=9.5, color="#2c3e50",
     style="normal")
note(ax, 2.2, 1.7, "none", fs=7.6, color="#5b6b7b", ha="left")
note(ax, 2.2, 4.6, "critic @ training", fs=7.6, color="#5b6b7b", ha="left")
note(ax, 2.2, 8.6, "full meta-game solve", fs=7.6, color="#5b6b7b", ha="left")

# ---- method placements (x: coop..competitive ; y: centralization) ----
box(ax, 2.2, 1.9, 2.6, 0.95, "Independent\nLearning", fc=C_ANNOT, fs=8.0)          # coop-ish, none
box(ax, 3.0, 4.2, 2.4, 0.95, "MADDPG", fc=C_MODEL, fs=8.4, fontweight="bold")       # coop/mixed, critic
box(ax, 1.9, 5.4, 2.4, 0.95, "QMIX", fc=C_MODEL, fs=8.4)                            # coop, value factor
box(ax, 3.2, 3.1, 2.4, 0.95, "MAPPO", fc=C_MODEL, fs=8.4)                           # coop, critic (simple)
box(ax, 1.9, 3.1, 2.4, 0.95, "CommNet\n(info @ exec)", fc=C_SAFE, fs=7.8)           # coop, comm
box(ax, 9.6, 7.7, 3.0, 1.1, "PSRO\n(population + meta-Nash)", fc=C_NET, fs=8.4,
    fontweight="bold")                                                              # competitive, meta-solve
box(ax, 8.4, 3.6, 3.2, 1.1, "LOLA\nmodels opponent as a LEARNER", fc=C_EXPLOIT, fs=7.8,
    fontweight="bold")                                                              # mixed-motive

# highlight LOLA as the "dynamic opponent" outlier
note(ax, 10.0, 2.9, "the odd one out: dynamic, not static, opponent", fs=7.4, color="#a5453a")

note(ax, 7.0, 9.6,
     "Two axes organize the field: what/when is centralized, and whether the opponent is static or learning.",
     fs=8.4, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "methods_spectrum.png"))
