"""summary figure: the research frontier map of Chapter 15 (three contributions x four rows).

Columns: C1 within-match opponent inference, C2 N-player safe exploitation, C3 joint evaluation.
Rows: what exists (September 2026 literature check), what is open (lit_gaps.md wording, shortened),
the thesis's approach (implementation/step15/design/C*.md), and the evidence already in hand
(Chapters 13-14 and this chapter's pilots; numbers from the result files named in the chapter).
Output: frontier_map.png next to this file. Run from the repo root with the project .venv active.

Text sizes: 14 x 9.6 units / shrink 2 = 7 in wide, printed at 17.6 cm: fs 10 prints at ~9.9 pt.
"""
import os

from _diagram_utils import new_fig, box, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=9.6, xlim=(0, 14), ylim=(0.7, 9.6), shrink=2.0)
FS = 10
cols = [("C1  opponent inference", 2.0), ("C2  N-player safety", 5.95), ("C3  evaluation", 9.9)]
rows = [("EXISTS", 7.05, C_ANNOT), ("OPEN", 5.0, C_EXPLOIT), ("APPROACH", 2.95, C_SAFE),
        ("EVIDENCE", 0.9, C_MODEL)]
W, H = 3.85, 1.85
text = {
    ("C1", "EXISTS"): "2-player detect → adapt\n(GSCU, PACE); poker\nexploiters (StratFormer,\nAlphaExploitem)",
    ("C1", "OPEN"): "N players; shifts within\na match; coupled to a\nsafety criterion",
    ("C1", "APPROACH"): "Dirichlet model per\nopponent, log prior,\nchange points,\ncalibrated confidence",
    ("C1", "EVIDENCE"): "Ch. 13: re-ID 15.6 %\nof 834 players;\nCh. 14: 3P model +0.37\nchips/hand in 50 hands",
    ("C2", "EXISTS"): "2P safe exploitation:\nRNR, RWYWE, OX-Search;\nN players: equal share,\nteam-maxmin",
    ("C2", "OPEN"): "N-player exploitation\nwith a checked loss\nbound, tested against\ncolluders",
    ("C2", "APPROACH"): "maximin-floor RWYWE;\ncapped mixture;\nKL anchor (measured)",
    ("C2", "EVIDENCE"): "P1: RWYWE safe in all\n60 attacked matches;\nP2: MM-RWYWE +0.08,\n−0.007 vs colluders",
    ("C3", "EXISTS"): "exploitability, AIVAT,\nElo, α-Rank, VasE;\nRRPS (one 2P game)",
    ("C3", "OPEN"): "gain, speed and a\ncoalition-aware worst\ncase, with confidence,\nacross games",
    ("C3", "APPROACH"): "Ch. 14 joint protocol\n+ match-level safety S\n+ failure-mode matrix",
    ("C3", "EVIDENCE"): "Ch. 14: Elo vs exploit.\nτ = 0.36 (Leduc); 3P\nexploiter −0.47 under\nadaptive coalition",
}
for label, y, fc in rows:
    note(ax, 0.02, y + H / 2, label, fs=FS, color="#2c3e50", ha="left", style="normal")
for (cname, x) in cols:
    note(ax, x + W / 2, 9.2, cname, fs=10.5, color="#2c3e50", style="normal")
    key = cname.split()[0]
    for label, y, fc in rows:
        box(ax, x, y, W, H, text[(key, label)], fc=fc, fs=FS)

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontier_map.png"))
