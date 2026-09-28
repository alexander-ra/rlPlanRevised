"""summary figure: the gift bank of Ganzfried & Sandholm's RWYWE, with two and three players.

One loop per hand: play the best response to the model among strategies whose worst case is at
least (reference - k); observe the hand; credit the worst outcome consistent with what was seen;
update the bank k. The reference is the game value v* with two players (G&S 2015, Alg. 2 and 6)
and the team-maxmin value v_mm against a coordinated pair with three (G&S's Sec. 2.3 remark, made
concrete in this chapter's pilot P2). No data.
Output: gift_bank.png next to this file. Run from the repo root with the project .venv active.

Text sizes: 14 x 7.4 units / shrink 2 = 7 in wide, printed at 17.6 cm: fs 10 prints at ~9.9 pt.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save, rc, lc, tc, bc
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=7.4, xlim=(0, 14), ylim=(0.2, 7.4), shrink=2.0)
FS = 10
X1, W1 = 0.2, 3.6
X2, X3, W = 4.3, 9.3, 4.5
YT, YB, H = 4.6, 1.5, 2.4

model = box(ax, X1, YT, W1, H, "MODEL\nof the opponents,\nfrom past hands", fc=C_MODEL, fs=FS)
solve = box(ax, X2, YT, W, H, "PLAY π(t)\nbest response to the\nmodel, with worst\ncase ≥ ref − k", fc=C_SAFE, fs=FS)
obs = box(ax, X3, YT, W, H, "OBSERVE\nthe actions; the cards\nonly at showdown", fc=C_ANNOT, fs=FS)
credit = box(ax, X3, YB, W, H, "CREDIT\nthe worst opponent play\nthat fits what was\nseen, against π(t)", fc=C_EXPLOIT, fs=FS)
bank = box(ax, X2, YB, W, H, "UPDATE THE BANK\nk ← k + credit − ref\n(k stays ≥ 0)", fc=C_NET, fs=FS)
ref = box(ax, X1, YB, W1, H, "REFERENCE\n2 players: v*\n3 players: v_mm,\nmaximin against a\ncoordinated pair", fc=C_ANNOT, fs=FS)

arrow(ax, rc(model), lc(solve))
arrow(ax, rc(solve), lc(obs))
arrow(ax, bc(obs), tc(credit))
arrow(ax, lc(credit), rc(bank))
arrow(ax, tc(bank), bc(solve))
arrow(ax, rc(ref), lc(bank), dashed=True)
note(ax, 7.0, 0.75, "Over the whole match: total expected payoff ≥ T · ref, against any opponents",
     fs=FS, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "gift_bank.png"))
