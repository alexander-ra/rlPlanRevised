"""Section 3 figure: partial observability - fold vs showdown.

Two panels. Left (showdown): the opponent's action pins to a single revealed private
card -> one situation credited. Right (fold): the card stays hidden -> evidence spread
over all consistent deals. Output: partial_observability.png.
Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, rc, lc, tc, bc, cc
from _diagram_utils import C_MODEL, C_NET, C_ANNOT, C_EXPLOIT, C_PANEL_BG_A, C_PANEL_BG_B
from _diagram_utils import panel_bg

fig, ax = new_fig(w=14, h=7.4, xlim=(0, 14), ylim=(0, 7.4), shrink=1.7)

panel_bg(ax, 0.2, 0.2, 6.6, 7.0, C_PANEL_BG_B, label="Showdown: cause and effect")
panel_bg(ax, 7.2, 0.2, 6.6, 7.0, C_PANEL_BG_A, label="Fold: effect only")

# ---- showdown panel ----
act1 = box(ax, 2.2, 5.0, 2.6, 1.0, "Observed: BET", fc=C_NET, fs=9.0)
card = box(ax, 2.2, 3.2, 2.6, 1.0, "Card revealed: K", fc=C_MODEL, fs=9.0, fontweight="bold")
sit = box(ax, 2.0, 1.2, 3.0, 1.0, "credit ONE situation\n(bet with K)", fc=C_ANNOT, fs=8.4)
arrow(ax, bc(act1), tc(card))
arrow(ax, bc(card), tc(sit))
note(ax, 3.5, 0.65, "unambiguous update", fs=7.6)

# ---- fold panel ----
act2 = box(ax, 9.2, 5.0, 2.6, 1.0, "Observed: BET, then fold", fc=C_NET, fs=8.2)
hidden = box(ax, 9.2, 3.2, 2.6, 1.0, "Card hidden: J? Q? K?", fc=C_EXPLOIT, fs=8.6,
             fontweight="bold")
h1 = box(ax, 7.5, 1.2, 1.7, 1.0, "bet w/ J", fc=C_ANNOT, fs=7.8)
h2 = box(ax, 9.45, 1.2, 1.7, 1.0, "bet w/ Q", fc=C_ANNOT, fs=7.8)
h3 = box(ax, 11.4, 1.2, 1.7, 1.0, "bet w/ K", fc=C_ANNOT, fs=7.8)
arrow(ax, bc(act2), tc(hidden))
for h in (h1, h2, h3):
    arrow(ax, bc(hidden), tc(h), rad=0.0)
note(ax, 10.5, 0.65, "spread evidence over every consistent deal", fs=7.6)

save(fig, "deliverables/reports/step07/summary/partial_observability.png")
