"""§3 figure: the MARL method family on two axes.

Horizontal axis: cooperative <-> competitive target setting. Vertical axis: how much is
centralized and when (nothing -> critic at training -> a full meta-game solve; communication
centralizes information at execution). Independent learning spans the whole horizontal axis;
LOLA is the outlier that models the opponent as a LEARNER rather than as a fixed strategy.
Output: methods_spectrum.png. Run with the project .venv active; the PNG lands next to this file.

Sizes: the figure prints at ~0.8 of its matplotlib size, so every label is fs 10.5 (~8.4 pt).
"""
import os

from matplotlib.patches import FancyArrowPatch

from _diagram_utils import new_fig, box, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT, EC

FS = 10.5

fig, ax = new_fig(w=14, h=9.45, xlim=(0, 14), ylim=(0, 10.5), shrink=1.6)

# ---- axes ----
ax.add_patch(FancyArrowPatch((1.2, 1.2), (13.2, 1.2), arrowstyle="-|>", mutation_scale=14,
                             color=EC, lw=1.6))
ax.add_patch(FancyArrowPatch((1.2, 1.2), (1.2, 9.4), arrowstyle="-|>", mutation_scale=14,
                             color=EC, lw=1.6))
note(ax, 7.2, 0.55, "cooperative  $\\longleftrightarrow$  competitive", fs=FS, color="#2c3e50",
     style="normal")
note(ax, 0.55, 5.3, "centralization  $\\longrightarrow$", fs=FS, color="#2c3e50",
     style="normal", rotation=90)
note(ax, 2.2, 1.55, "none", fs=FS, color="#5b6b7b", ha="left")
note(ax, 2.2, 5.85, "critic @ training", fs=FS, color="#5b6b7b", ha="left")
note(ax, 2.2, 8.6, "full meta-game solve", fs=FS, color="#5b6b7b", ha="left")

# ---- method placements (x: coop..competitive ; y: centralization) ----
box(ax, 2.2, 1.85, 10.4, 0.95, "Independent Learning (any setting)", fc=C_ANNOT, fs=FS)
box(ax, 1.9, 3.2, 2.8, 1.15, "CommNet\n(info @ exec)", fc=C_SAFE, fs=FS)               # coop, comm
box(ax, 5.0, 3.2, 2.4, 0.95, "MAPPO", fc=C_MODEL, fs=FS)                               # coop, critic
box(ax, 1.9, 4.6, 2.8, 0.95, "QMIX", fc=C_MODEL, fs=FS)                                # coop, value factor
box(ax, 5.0, 4.6, 2.4, 0.95, "MADDPG", fc=C_MODEL, fs=FS, fontweight="bold")           # coop/mixed, critic
box(ax, 8.6, 7.7, 4.6, 1.2, "PSRO\n(population + meta-Nash)", fc=C_NET, fs=FS,
    fontweight="bold")                                                                  # competitive, meta-solve
box(ax, 8.4, 3.7, 3.8, 1.4, "LOLA\nmodels the opponent\nas a LEARNER", fc=C_EXPLOIT, fs=FS,
    fontweight="bold")                                                                  # mixed-motive

# highlight LOLA as the "dynamic opponent" outlier
note(ax, 10.3, 3.25, "the odd one out:\ndynamic, not static, opponent", fs=FS, color="#a5453a")

note(ax, 7.0, 10.0,
     "Two axes organize the field: what and when is centralized,\n"
     "and whether the opponent is static or learning.",
     fs=FS, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "methods_spectrum.png"))
