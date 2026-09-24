"""Section 4 figure: three models, one interface.

A shared observation stream feeds three interchangeable estimators (type-based,
continuous, consistent), each emitting a predicted opponent strategy consumed by the
same best-response step. Output: three_models.png.
Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, rc, lc, tc, bc, cc
from _diagram_utils import C_SAFE, C_MODEL, C_NET, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=7.6, xlim=(0, 14), ylim=(0, 7.6), shrink=1.7)

# boxes sized for the longer Bulgarian labels at fs 10 (prints at ~8.5 pt)
stream = box(ax, 0.2, 3.1, 2.4, 1.4, "Observed\nhands", fc=C_ANNOT, fs=10)

t = box(ax, 3.3, 5.3, 5.3, 1.5,
        "Type-based\nbelief over a few known types", fc=C_SAFE, fs=10)
c = box(ax, 3.3, 3.05, 5.3, 1.5,
        "Continuous\nper-situation counts, smoothed", fc=C_MODEL, fs=10)
s = box(ax, 3.3, 0.8, 5.3, 1.5,
        "Consistent\none valid global strategy (convex)", fc=C_NET, fs=10)

iface = box(ax, 9.2, 3.0, 2.5, 1.6, "Predicted\nopponent\nstrategy", fc=C_ANNOT, fs=10,
            fontweight="bold")
br = box(ax, 12.0, 3.1, 1.9, 1.4, "Best\nresponse", fc=C_EXPLOIT, fs=10)

for m in (t, c, s):
    arrow(ax, rc(stream), lc(m), rad=0.02)
    arrow(ax, rc(m), lc(iface), rad=0.02)
arrow(ax, rc(iface), lc(br))

note(ax, 5.95, 7.2, "same interface: consume observations → emit a strategy", fs=10,
     color="#2c3e50")
note(ax, 5.95, 0.35, "fast/fragile  →  robust/data-hungry  →  principled/costly", fs=10)

save(fig, "deliverables/reports/step07/summary/three_models.png")
