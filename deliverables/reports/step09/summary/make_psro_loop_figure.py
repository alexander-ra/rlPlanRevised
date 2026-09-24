"""§6 figure: the PSRO double-oracle loop.

Population -> empirical meta-game payoff matrix -> meta-Nash mixture -> best-response oracle ->
add the new policy back into the population. Exploitability of the meta-Nash mixture is expected
to fall as the population grows. In this project the oracle is Chapter 7's EXACT best response,
so PSRO's progress is the same exploitability yardstick used in the game-theory chapters.
Output: psro_loop.png. Run with the project .venv active; the PNG lands next to this file.

Sizes: the figure prints at ~0.82 of its matplotlib size, so every label is fs 10.5 (~8.6 pt).
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT, EC

FS = 10.5

fig, ax = new_fig(w=14, h=8.9, xlim=(0, 14), ylim=(0, 8.9), shrink=1.65)

pop = box(ax, 0.1, 5.9, 4.6, 1.4, "Population of policies\n$\\{\\pi^1,\\dots,\\pi^k\\}$ per player",
          fc=C_MODEL, fs=FS, fontweight="bold")
meta = box(ax, 5.5, 5.9, 3.4, 1.4, "Empirical meta-game\npayoff matrix $M$", fc=C_SAFE, fs=FS)
nash = box(ax, 9.9, 5.9, 3.9, 1.4, "Meta-Nash mixture\n$\\sigma$ over the population", fc=C_NET,
           fs=FS, fontweight="bold")
oracle = box(ax, 4.5, 2.4, 5.4, 1.4,
             "Best-response oracle\n$\\pi^{k+1}=\\mathrm{BR}(\\sigma_{-i})$\n(exact BR, Chapter 7)",
             fc=C_EXPLOIT, fs=FS, fontweight="bold")

# clockwise loop; the labels of the two short arrows sit above the row, where there is room
arrow(ax, (4.7, 6.6), (5.5, 6.6))
note(ax, 5.1, 7.75, "simulate\nmatch-ups", fs=FS, color="#2c3e50")
arrow(ax, (8.9, 6.6), (9.9, 6.6))
note(ax, 9.4, 7.75, "solve", fs=FS, color="#2c3e50")
arrow(ax, (11.6, 5.9), (8.6, 3.8), color=EC, lw=1.6, rad=0.2)
note(ax, 11.4, 4.6, "best-respond\nto $\\sigma$", fs=FS, color="#2c3e50", ha="left")
arrow(ax, (5.8, 3.8), (2.35, 5.9), color=EC, lw=1.6, rad=0.2)
note(ax, 2.7, 4.6, "add $\\pi^{k+1}$\nto population", fs=FS, color="#2c3e50", ha="right")

box(ax, 2.5, 0.4, 9.0, 1.2,
    "exploitability of $\\sigma$ (NashConv) falls\nas the population grows",
    fc=C_ANNOT, fs=FS, fontweight="bold")

note(ax, 7.0, 8.5,
     "PSRO = Chapter 2's iterated best response, lifted from actions to whole policies.",
     fs=FS, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "psro_loop.png"))
