"""summary figure: the Chapter 13 pipeline, from raw hand histories to the six analyses.

Raw PHH files (2.03 M iPoker hands from July 2009 and the 10,000 Pluribus hands) are replayed by
the chapter's own parser and checked by two validators; the parsed hands become four data products
(seat rows, decision rows, token streams, pair table), and each analysis reads one of them.
Numbers in the boxes come from implementation/step13/implementation/results/build_IPN100.json and
validator.json. Output: pipeline.png next to this file.

Text sizes: the figure is about 7.9 in wide and prints at 17.6 cm (scale ~0.87), so fs 10.5
prints at ~9.2 pt.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save, rc, lc
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_NET, C_ANNOT

FS = 10.5
fig, ax = new_fig(w=14, h=8.2, xlim=(0, 14), ylim=(0, 8.2), shrink=1.7)

raw = box(ax, 0.1, 3.3, 2.7, 1.9, "Hand histories\n(PHH)\n2.03 M iPoker\n+ 10,000 Pluribus",
          fc=C_ANNOT, fs=FS)
par = box(ax, 3.2, 3.3, 2.5, 1.9, "Parser +\n2 validators\n99.77 % parsed", fc=C_SAFE, fs=FS,
          fontweight="bold")
arrow(ax, rc(raw), lc(par))

prods = [("Seat rows\n(stat opportunities)", 6.7), ("Decision rows\n(state, action)", 5.0),
         ("Token streams\n(one per player)", 3.3), ("Pair table\n(heads-up, chip flow)", 1.55)]
pb = {}
for lab, yc in prods:
    b = box(ax, 6.2, yc - 0.6, 2.9, 1.2, lab, fc=C_MODEL, fs=FS)
    pb[lab.split("\n")[0]] = b
    arrow(ax, rc(par), lc(b))

an = [("Profiles, reliability,\ngap to Pluribus", 7.3, "Seat rows", C_NET),
      ("Style clusters,\nBayesian typing", 6.1, "Seat rows", C_NET),
      ("Behavioral cloning", 5.0, "Decision rows", C_NET),
      ("Embedding,\nre-identification", 3.9, "Token streams", C_NET),
      ("Bot detection\n(Pluribus)", 2.7, "Token streams", C_EXPLOIT),
      ("Collusion detector\n(injected colluders)", 1.55, "Pair table", C_EXPLOIT)]
for lab, yc, src, col in an:
    b = box(ax, 9.9, yc - 0.48, 3.95, 0.96, lab, fc=col, fs=FS)
    arrow(ax, rc(pb[src]), lc(b))

note(ax, 11.9, 8.15, "C1: represent, predict, classify, track", fs=FS, color="#2c3e50",
     style="normal")
note(ax, 11.9, 0.55, "red boxes: fair play (bots, collusion)", fs=FS, color="#2c3e50",
     style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline.png"))
