"""summary figure: the research programme on one time axis (September 2026 - April 2029).

Rows: the individual plan's stages (each ends with a chapter and an article), the experiments of
implementation/step15/design/experiments.md, and the six papers of design/publications.md
(submission months; hollow markers = estimated deadlines, filled = announced ones).
No data: dates are the plan's and the venues' (verified or marked estimated in publications.md).
Output: timeline.png next to this file. Run from the repo root with the project .venv active.

Text sizes: saved 7 in wide, printed at 17.6 cm, so fs 10 prints at ~9.9 pt.
"""
import datetime as dt
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

FS = 10
plt.rcParams.update({"font.size": FS, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "axes.edgecolor": "#52514e",
                     "xtick.color": "#52514e", "ytick.color": "#0b0b0b"})
INK2, GRID = "#52514e", "#e4e3df"
D = lambda y, m, d=1: dt.date(y, m, d)  # noqa: E731

stages = [("Stage I · Ch. I", D(2026, 3), D(2026, 11, 30)),
          ("Stage II · Ch. II", D(2026, 12), D(2027, 4, 30)),
          ("Stage III · Ch. III", D(2027, 5), D(2028, 1, 31)),
          ("Stage IV · Ch. IV", D(2028, 2), D(2028, 8, 31)),
          ("Write-up, defence", D(2028, 9), D(2029, 4, 30))]
exps = [("Exp. 2.1 (3P Kuhn → Leduc)", D(2026, 11), D(2027, 12, 31)),
        ("Exp. 1.1–1.2 (inference)", D(2027, 1), D(2027, 10, 31)),
        ("Exp. 2.2 (colluders)", D(2027, 6), D(2028, 1, 31)),
        ("Exp. 3.1 (cross-game)", D(2027, 9), D(2028, 6, 30))]
papers = [("P1 protocol (CoG)", D(2027, 3, 1), True), ("P3 N-player safety (IJCAI)", D(2027, 1, 15), False),
          ("P4 inference (NeurIPS)", D(2027, 5, 15), False), ("P2 hand histories (ToG)", D(2027, 6, 30), False),
          ("P5 colluders (AAMAS)", D(2027, 10, 8), False), ("P6 cross-game (journal)", D(2028, 7, 31), False)]

fig, ax = plt.subplots(figsize=(7.0, 4.9))
rows = []
y = 0
blue, violet, red = "#2a78d6", "#4a3aa7", "#e34948"
for name, when, announced in reversed(papers):
    ax.plot([when], [y], marker="D", ms=8, color=red, mfc=red if announced else "white", mew=1.6, zorder=3)
    rows.append((y, name)); y += 1
y += 0.4
for name, a, b in reversed(exps):
    ax.barh(y, (b - a).days, left=a, height=0.55, color=violet, alpha=0.85)
    rows.append((y, name)); y += 1
y += 0.4
for name, a, b in reversed(stages):
    ax.barh(y, (b - a).days, left=a, height=0.6, color=blue, alpha=0.85)
    rows.append((y, name)); y += 1
ax.plot([D(2026, 10, 8)], [rows[[n for _, n in rows].index("P1 protocol (CoG)")][0]], marker="D", ms=8,
        color=red, mfc="white", mew=1.0, alpha=0.55, zorder=3)
today = D(2026, 9, 25)
ax.axvline(today, color=INK2, lw=0.9, ls=":")
ax.text(today, -0.9, "today ", ha="right", va="center", color=INK2, fontsize=FS)
ax.set_yticks([r for r, _ in rows])
ax.set_yticklabels([n for _, n in rows])
ax.tick_params(axis="y", length=0)
ax.set_xlim(D(2026, 3), D(2029, 5))
ax.set_ylim(-1.4, y - 0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m.%Y"))
ax.tick_params(axis="x", labelsize=9)
plt.setp(ax.get_xticklabels(), rotation=25, ha="right")
ax.grid(axis="x", color=GRID)
ax.set_axisbelow(True)
ax.set_xlabel("filled ◆: announced deadline   hollow ◇: estimated\n"
              "faint ◇: AAMAS 2027 stretch option for P1")
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timeline.png")
fig.savefig(out, dpi=250, bbox_inches="tight", pad_inches=0.06)
print("saved", out)
