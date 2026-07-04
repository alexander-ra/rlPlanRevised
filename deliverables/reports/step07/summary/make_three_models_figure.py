"""Section 4 figure: three models, one interface.

A shared observation stream feeds three interchangeable estimators (type-based,
continuous, consistent), each emitting a predicted opponent strategy consumed by the
same best-response step. Output: three_models.png.
Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, rc, lc, tc, bc, cc
from _diagram_utils import C_SAFE, C_MODEL, C_NET, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=7.2, xlim=(0, 14), ylim=(0, 7.2), shrink=1.7)

stream = box(ax, 0.4, 3.0, 2.6, 1.2, "Observed\nhands", fc=C_ANNOT, fs=9.0)

t = box(ax, 4.0, 5.2, 4.6, 1.3,
        "Type-based\nbelief over a few known types", fc=C_SAFE, fs=8.6)
c = box(ax, 4.0, 3.0, 4.6, 1.3,
        "Continuous\nper-situation counts, smoothed", fc=C_MODEL, fs=8.6)
s = box(ax, 4.0, 0.8, 4.6, 1.3,
        "Consistent\none valid global strategy (convex)", fc=C_NET, fs=8.6)

iface = box(ax, 9.4, 3.0, 2.3, 1.3, "Predicted\nopponent\nstrategy", fc=C_ANNOT, fs=8.6,
            fontweight="bold")
br = box(ax, 12.0, 3.0, 1.7, 1.3, "Best\nresponse", fc=C_EXPLOIT, fs=8.8)

for m in (t, c, s):
    arrow(ax, rc(stream), lc(m), rad=0.02)
    arrow(ax, rc(m), lc(iface), rad=0.02)
arrow(ax, rc(iface), lc(br))

note(ax, 6.3, 6.75, "same interface: consume observations -> emit a strategy", fs=8.0,
     color="#2c3e50")
note(ax, 6.3, 0.35, "fast/fragile  \u2192  robust/data-hungry  \u2192  principled/costly", fs=7.8)

save(fig, "deliverables/reports/step07/summary/three_models.png")
