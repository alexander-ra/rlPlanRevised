"""summary figure: the AlphaStar-style PBT league (three agent types + freezing + PFSP).

Main agents are the product; main exploiters hunt weaknesses in the current mains; league
exploiters hunt weaknesses anywhere in the frozen history. Periodically a copy of each agent is
FROZEN into a snapshot museum, and matchmaking (PFSP) samples opponents in proportion to how hard
they are to beat. Output: league_architecture.png. Run with the project .venv active; the PNG
lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save, panel_bg
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_NET, C_ANNOT, C_PANEL_BG_A, EC

fig, ax = new_fig(w=14, h=8.8, xlim=(0, 14), ylim=(0, 8.8), shrink=1.6)

panel_bg(ax, 0.2, 3.2, 13.6, 5.2, C_PANEL_BG_A, label="Live population (trains + PBT exploit/explore)")

main = box(ax, 0.8, 5.4, 3.6, 1.7, "MAIN agents\n(the product)\nSP + PFSP vs everyone",
           fc=C_SAFE, fs=8.6, fontweight="bold")
mexp = box(ax, 5.2, 5.4, 3.6, 1.7, "MAIN exploiters\nhunt weaknesses in\nthe CURRENT mains",
           fc=C_EXPLOIT, fs=8.6, fontweight="bold")
lexp = box(ax, 9.6, 5.4, 3.6, 1.7, "LEAGUE exploiters\nhunt weaknesses in\nthe FROZEN history",
           fc=C_EXPLOIT, fs=8.6, fontweight="bold")

pbt = box(ax, 3.4, 3.5, 7.2, 1.0, "PBT step: copy top agents (exploit) + perturb lr / entropy (explore)",
          fc=C_NET, fs=8.4, fontweight="bold")

# frozen museum
museum = box(ax, 0.8, 1.0, 12.4, 1.4,
             "FROZEN snapshot museum   [ main#e4 | main#e9 | ... | mexp#... | lexp#... ]\n"
             "periodic frozen copies -> opponents that never forget an old style",
             fc=C_ANNOT, fs=8.2)

# exploiters attack mains / museum
arrow(ax, (mexp[0] + mexp[2] / 2, mexp[1]), (main[0] + main[2] / 2 + 0.4, main[1]),
      color=EC, lw=1.4, rad=0.25, style="-|>")
note(ax, 4.7, 5.0, "beat me!", fs=7.2, color="#b3403a", ha="center")
arrow(ax, (lexp[0] + lexp[2] / 2, lexp[1]), (museum[0] + museum[2] - 1.5, museum[1] + museum[3]),
      color=EC, lw=1.4, rad=-0.15, style="-|>")

# freeze arrows (down into museum)
for b in (main, mexp, lexp):
    arrow(ax, (b[0] + b[2] / 2, b[1]), (b[0] + b[2] / 2, museum[1] + museum[3]),
          color="#8a97a6", lw=1.1, dashed=True, style="-|>")
note(ax, 12.9, 3.0, "freeze", fs=7.0, color="#5b6b7b", ha="right")

# PFSP note
note(ax, 7.0, 8.15,
     "PFSP matchmaking: sample each opponent with probability rising in how hard it is to beat "
     "(focus training where you are losing).",
     fs=8.2, color="#2c3e50", style="normal")

note(ax, 7.0, 0.35,
     "measured: main exploitability falls 4.73 -> ~1.21 then regresses to ~2.05 (scale, 120 epochs); "
     "best frozen snapshot 1.31 beats PSRO 2.16 and self-play 3.68.",
     fs=7.4, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "league_architecture.png"))
