"""summary figure: the AlphaStar-style PBT league (three agent types + freezing + PFSP).

Main agents are the product; main exploiters hunt weaknesses in the current mains; league
exploiters hunt weaknesses anywhere in the frozen history. Periodically a copy of each agent is
FROZEN into a snapshot museum, and matchmaking (PFSP, prioritized fictitious self-play) samples
opponents in proportion to how hard they are to beat. Output: league_architecture.png. Run with
the project .venv active; the PNG lands next to this file.

Drawn at print size: the canvas is 7.0 in wide (the 17.6 cm text width), all text is fs 10.
The measured numbers live in the caption and the text, not in the diagram.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save, panel_bg
from _diagram_utils import C_SAFE, C_EXPLOIT, C_NET, C_ANNOT, C_PANEL_BG_A, EC

fig, ax = new_fig(w=14, h=9.65, xlim=(0, 14), ylim=(0.55, 10.2), shrink=2.0)

panel_bg(ax, 0.2, 3.1, 13.6, 5.6, C_PANEL_BG_A, label="Live population (trains + PBT exploit/explore)")

main = box(ax, 0.5, 5.6, 4.2, 2.2, "MAIN agents\n(the product)\nSP + PFSP vs everyone",
           fc=C_SAFE, fs=10, fontweight="bold")
mexp = box(ax, 4.9, 5.6, 4.2, 2.2, "MAIN exploiters\nhunt weaknesses in\nthe CURRENT mains",
           fc=C_EXPLOIT, fs=10, fontweight="bold")
lexp = box(ax, 9.3, 5.6, 4.2, 2.2, "LEAGUE exploiters\nhunt weaknesses in\nthe FROZEN history",
           fc=C_EXPLOIT, fs=10, fontweight="bold")

pbt = box(ax, 2.8, 3.25, 8.4, 1.4,
          "PBT step: copy the top agents (exploit)\n+ perturb learning rate / entropy (explore)",
          fc=C_NET, fs=10)

# frozen museum
museum = box(ax, 0.5, 0.75, 13.0, 1.75,
             "FROZEN snapshot museum\n"
             "[ main#e4 | main#e9 | … | mexp#… | lexp#… ]\n"
             "periodic frozen copies → opponents that never forget an old style",
             fc=C_ANNOT, fs=10)

# exploiters attack mains / museum
arrow(ax, (mexp[0] + mexp[2] / 2, mexp[1]), (main[0] + main[2] / 2 + 0.4, main[1]),
      color=EC, lw=1.4, rad=-0.3, style="-|>")
note(ax, 5.0, 5.33, "beat me!", fs=10, color="#b3403a", ha="center")
arrow(ax, (lexp[0] + lexp[2] / 2, lexp[1]), (museum[0] + museum[2] - 1.5, museum[1] + museum[3]),
      color=EC, lw=1.4, rad=-0.15, style="-|>")

# freeze arrows (down into museum)
for b in (main, mexp, lexp):
    arrow(ax, (b[0] + b[2] / 2, b[1]), (b[0] + b[2] / 2, museum[1] + museum[3]),
          color="#8a97a6", lw=1.1, dashed=True, style="-|>")
note(ax, 2.4, 4.1, "freeze", fs=10, color="#5b6b7b", ha="right")

# PFSP note (above the panel, clear of its title)
note(ax, 7.0, 9.55,
     "PFSP matchmaking: each opponent is sampled with a probability that rises\n"
     "with how hard it is to beat (training focuses where the agent is losing).",
     fs=10, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "league_architecture.png"))
