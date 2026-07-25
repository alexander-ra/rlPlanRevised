"""summary figure: the coalition detector (reading alliances off the SLS move stream).

In So Long Sucker, placing a chip into another player's pile is HELP (a handshake) and capturing a
pile is HARM (the knife). The detector accumulates help/harm matrices from the move log, differences
them into NET SUPPORT, and names the pair with the highest mutual support as the coalition. This is
Step 07's opponent modeling lifted from "what hand?" to "who is allied with whom?" (Contribution #1).
Measured: a planted {0,1} alliance is recovered exactly (score 10.0). Output: sls_coalition.png. Run
with the project .venv active; the PNG lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_NET, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.4, xlim=(0, 14), ylim=(0, 7.4), shrink=1.7)

moves = box(ax, 0.4, 4.3, 3.1, 1.5, "SLS move stream\n(place / capture\nchips each turn)", fc=C_ANNOT, fs=8.4)
helpb = box(ax, 4.2, 5.5, 3.2, 1.1, "HELP matrix\nplace chip into $j$'s pile", fc=C_MODEL, fs=8.2, fontweight="bold")
harmb = box(ax, 4.2, 3.6, 3.2, 1.1, "HARM matrix\ncapture $j$'s pile", fc=C_EXPLOIT, fs=8.2, fontweight="bold")
net = box(ax, 8.1, 4.3, 2.9, 1.5, "NET SUPPORT\n$= $ help $-$ harm", fc=C_SAFE, fs=8.6, fontweight="bold")
coal = box(ax, 11.4, 4.3, 2.3, 1.5, "Strongest pair\n$=$ coalition", fc=C_NET, fs=8.6, fontweight="bold")

arrow(ax, (moves[0] + moves[2], moves[1] + moves[3] / 2 + 0.4), (helpb[0], helpb[1] + helpb[3] / 2), rad=0.15)
arrow(ax, (moves[0] + moves[2], moves[1] + moves[3] / 2 - 0.4), (harmb[0], harmb[1] + harmb[3] / 2), rad=-0.15)
arrow(ax, (helpb[0] + helpb[2], helpb[1] + helpb[3] / 2), (net[0], net[1] + net[3] / 2 + 0.4), rad=-0.15)
arrow(ax, (harmb[0] + harmb[2], harmb[1] + harmb[3] / 2), (net[0], net[1] + net[3] / 2 - 0.4), rad=0.15)
arrow(ax, (net[0] + net[2], net[1] + net[3] / 2), (coal[0], coal[1] + coal[3] / 2))

note(ax, 7.0, 7.05,
     "The alliance is encoded in the moves themselves - no separate negotiation phase to model.",
     fs=8.4, color="#2c3e50", style="normal")

res = box(ax, 0.4, 1.1, 13.3, 1.6,
          "MEASURED: a planted {0,1} alliance is recovered EXACTLY - strongest pair {0,1}, score 10.0,\n"
          "with 0 / -1 net support on every cross-pair edge. Opponent modeling (Step 07) generalized to\n"
          "the game's SOCIAL STRUCTURE (Contribution #1).",
          fc=C_ANNOT, fs=8.0)

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sls_coalition.png"))
