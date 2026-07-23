"""§6 figure: the PSRO double-oracle loop.

Population -> empirical meta-game payoff matrix -> meta-Nash mixture -> best-response oracle ->
add the new policy back into the population. Exploitability of the meta-Nash mixture is expected
to fall as the population grows. In this project the oracle is Step 07's EXACT best response, so
PSRO's progress is the same exploitability yardstick used in the game-theory steps.
Output: psro_loop.png. Run with the project .venv active; the PNG lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT, EC

fig, ax = new_fig(w=14, h=8.4, xlim=(0, 14), ylim=(0, 8.4), shrink=1.65)

pop = box(ax, 0.7, 5.9, 3.6, 1.4, "Population of policies\n$\\{\\pi^1,\\dots,\\pi^k\\}$ per player",
          fc=C_MODEL, fs=8.8, fontweight="bold")
meta = box(ax, 5.4, 5.9, 3.6, 1.4, "Empirical meta-game\npayoff matrix $M$", fc=C_SAFE, fs=8.8)
nash = box(ax, 10.0, 5.9, 3.3, 1.4, "Meta-Nash mixture\n$\\sigma$ over the population", fc=C_NET,
           fs=8.8, fontweight="bold")
oracle = box(ax, 5.1, 2.4, 4.2, 1.4, "Best-response oracle\n$\\pi^{k+1}=\\mathrm{BR}(\\sigma_{-i})$\n(exact BR, Step 07)",
             fc=C_EXPLOIT, fs=8.4, fontweight="bold")

# clockwise loop
arrow(ax, (4.3, 6.6), (5.4, 6.6))
note(ax, 4.85, 6.95, "simulate\nmatch-ups", fs=7.2, color="#2c3e50")
arrow(ax, (9.0, 6.6), (10.0, 6.6))
note(ax, 9.5, 6.95, "solve", fs=7.2, color="#2c3e50")
arrow(ax, (11.0, 5.9), (8.2, 3.8), color=EC, lw=1.6, rad=0.2)
note(ax, 11.0, 4.6, "best-respond\nto $\\sigma$", fs=7.2, color="#2c3e50", ha="left")
arrow(ax, (5.6, 3.8), (2.4, 5.9), color=EC, lw=1.6, rad=0.2)
note(ax, 2.7, 4.6, "add $\\pi^{k+1}$\nto population", fs=7.2, color="#2c3e50", ha="right")

box(ax, 3.9, 0.5, 6.4, 0.9,
    "exploitability of $\\sigma$ (NashConv) falls as the population grows",
    fc=C_ANNOT, fs=8.4, fontweight="bold")

note(ax, 7.0, 7.95,
     "PSRO = Step 2's iterated best response, lifted from actions to whole policies.",
     fs=8.6, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "psro_loop.png"))
