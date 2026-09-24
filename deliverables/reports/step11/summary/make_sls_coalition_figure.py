"""summary figure: the coalition detector (reading alliances off the SLS move stream).

In So Long Sucker, placing a chip into another player's pile is HELP (a handshake) and capturing a
pile is HARM (the knife). The detector accumulates help/harm matrices from the move log, differences
them into NET SUPPORT, and names the pair with the highest mutual support as the coalition. This is
Chapter 7's opponent modeling lifted from "what hand?" to "who is allied with whom?" (Contribution
#1). In this chapter's engine negotiation is not modelled, so the alliance shows only in the moves.
Measured: a planted {0,1} alliance is recovered exactly (score 10.0). Output: sls_coalition.png.
Run with the project .venv active; the PNG lands next to this file.

Text sizes: the figure prints at 17.6 cm (scale ~0.85), so fs 10 prints at ~8.5 pt.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_NET, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.4, xlim=(0, 14), ylim=(0, 7.4), shrink=1.7)

moves = box(ax, 0.2, 4.2, 3.4, 1.7, "SLS move stream\n(place / capture\nchips each turn)", fc=C_ANNOT, fs=10)
helpb = box(ax, 4.0, 5.4, 3.95, 1.2, "HELP matrix\nplace chip into $j$'s pile", fc=C_MODEL, fs=10, fontweight="bold")
harmb = box(ax, 4.0, 3.5, 3.95, 1.2, "HARM matrix\ncapture $j$'s pile", fc=C_EXPLOIT, fs=10, fontweight="bold")
net = box(ax, 8.4, 4.2, 3.05, 1.7, "NET SUPPORT\n$= $ help $-$ harm", fc=C_SAFE, fs=10, fontweight="bold")
coal = box(ax, 11.8, 4.2, 2.05, 1.7, "Strongest pair\n$=$ coalition", fc=C_NET, fs=10, fontweight="bold")

arrow(ax, (moves[0] + moves[2], moves[1] + moves[3] / 2 + 0.4), (helpb[0], helpb[1] + helpb[3] / 2), rad=0.15)
arrow(ax, (moves[0] + moves[2], moves[1] + moves[3] / 2 - 0.4), (harmb[0], harmb[1] + harmb[3] / 2), rad=-0.15)
arrow(ax, (helpb[0] + helpb[2], helpb[1] + helpb[3] / 2), (net[0], net[1] + net[3] / 2 + 0.4), rad=-0.15)
arrow(ax, (harmb[0] + harmb[2], harmb[1] + harmb[3] / 2), (net[0], net[1] + net[3] / 2 - 0.4), rad=0.15)
arrow(ax, (net[0] + net[2], net[1] + net[3] / 2), (coal[0], coal[1] + coal[3] / 2))

note(ax, 7.0, 7.1,
     "In this engine the alliance is visible only in the moves - negotiation is not modelled.",
     fs=10, color="#2c3e50", style="normal")

res = box(ax, 0.3, 0.6, 13.5, 2.2,
          "MEASURED: the planted alliance {0, 1} is recovered EXACTLY -\n"
          "strongest pair {0, 1}, score 10.0; net support is 0 or -1 for every other pair.\n"
          "Opponent modeling (Chapter 7) carried over to the game's\n"
          "SOCIAL STRUCTURE (Contribution #1).",
          fc=C_ANNOT, fs=10)

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sls_coalition.png"))
