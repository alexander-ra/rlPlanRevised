"""Generate the hybrid-architecture schematic for the Step 5 summary.

Shows the encoder -> fuse -> trunk -> heads pattern, plus two concrete
examples (DRQN, AlphaStar). Output: arch_hybrid.png in this directory.

Drawn at the size it prints (full text width, 17.6 cm = 6.9 in), so the 10 pt
box text prints at 10 pt. Boxes are sized so that the Bulgarian labels fit
after the renderer re-wraps them.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _diagram_utils import box, rc, lc, arrow  # noqa: E402

C_IN = "#eceff3"    # input
C_ENC = "#cfe0fb"   # encoder
C_FUSE = "#e6dbf7"  # fuse / trunk
C_HEAD = "#cdeedd"  # head / output
FS = 10


def title(ax, y, txt):
    ax.text(0.1, y, txt, fontsize=10, fontweight="bold", color="#2c3e50", va="center")


fig, ax = plt.subplots(figsize=(6.9, 5.4))
# Fix the axes to the whole canvas before drawing: the Bulgarian renderer fits
# each label to its box at the moment box() is called, so the box geometry must
# already be the printed one (tight_layout would enlarge the axes afterwards).
fig.subplots_adjust(left=0.005, right=0.995, bottom=0.005, top=0.995)
ax.set_xlim(0, 13.4)
ax.set_ylim(1.55, 12)
ax.axis("off")

# ===== Section A: general pattern =====
title(ax, 11.55, "General pattern: encoders → fuse → shared trunk → heads")
H = 0.8
xs_in, xs_enc, x_fuse, x_trunk, x_head = 0.1, 3.0, 5.8, 7.85, 10.6
ys = [10.3, 9.35, 8.4, 7.45]
in_labels = ["Spatial board", "Action history", "Cards / set", "Scalars"]
enc_labels = ["CNN", "RNN / attn.", "Deep Sets", "MLP"]
encs = []
for y, il, el in zip(ys, in_labels, enc_labels):
    b_in = box(ax, xs_in, y, 2.5, H, il, C_IN, fs=FS)
    b_en = box(ax, xs_enc, y, 2.4, H, el, C_ENC, fs=FS)
    arrow(ax, rc(b_in), lc(b_en))
    encs.append(b_en)
fuse = box(ax, x_fuse, ys[-1], 1.7, ys[0] + H - ys[-1], "Fuse\n(concat)", C_FUSE, fs=FS)
for b_en in encs:
    arrow(ax, rc(b_en), (x_fuse, b_en[1] + b_en[3] / 2))
trunk = box(ax, x_trunk, 8.7, 2.4, 1.6, "Shared trunk\n(MLP / LSTM)", C_FUSE, fs=FS)
arrow(ax, rc(fuse), lc(trunk))
ph = box(ax, x_head, 9.85, 2.6, 0.9, "Policy head", C_HEAD, fs=FS)
vh = box(ax, x_head, 8.25, 2.6, 0.9, "Value head", C_HEAD, fs=FS)
arrow(ax, rc(trunk), lc(ph))
arrow(ax, rc(trunk), lc(vh))

ax.plot([0.1, 13.3], [7.0, 7.0], color="#d0d5db", lw=1, ls="--")

# ===== Section B: DRQN =====
title(ax, 6.6, "Example 1 — DRQN (memory for partial observability)")
yB = 5.35
xb = 0.1
prev = None
for lab, fc in [("Frame /\nlocal view", C_IN), ("CNN", C_ENC), ("LSTM", C_ENC),
                ("MLP", C_ENC), ("Q-values\nper action", C_HEAD)]:
    b = box(ax, xb, yB, 2.4, 0.95, lab, fc, fs=FS)
    if prev is not None:
        arrow(ax, rc(prev), lc(b))
    prev = b
    xb += 2.7

ax.plot([0.1, 13.3], [4.95, 4.95], color="#d0d5db", lw=1, ls="--")

# ===== Section C: AlphaStar =====
title(ax, 4.55, "Example 2 — AlphaStar")
xs_in2, xs_enc2, x_cat, x_lstm, x_head2 = 0.1, 3.0, 5.8, 7.85, 10.4
ys2 = [3.5, 2.6, 1.7]
encs2 = []
for y, il, el in zip(ys2, ["Units (set)", "Minimap", "Scalars"],
                     ["Transformer", "CNN", "MLP"]):
    b_in = box(ax, xs_in2, y, 2.5, 0.75, il, C_IN, fs=FS)
    b_en = box(ax, xs_enc2, y, 2.4, 0.75, el, C_ENC, fs=FS)
    arrow(ax, rc(b_in), lc(b_en))
    encs2.append(b_en)
cat = box(ax, x_cat, ys2[-1], 1.7, ys2[0] + 0.75 - ys2[-1], "Concat", C_FUSE, fs=FS)
for b_en in encs2:
    arrow(ax, rc(b_en), (x_cat, b_en[1] + b_en[3] / 2))
lstm = box(ax, x_lstm, 2.45, 2.0, 1.0, "LSTM\ncore", C_FUSE, fs=FS)
arrow(ax, rc(cat), lc(lstm))
heads2 = box(ax, x_head2, 2.45, 2.9, 1.0, "Action heads\n(autoregr.)", C_HEAD, fs=FS)
arrow(ax, rc(lstm), lc(heads2))

out = "deliverables/reports/step05/summary/arch_hybrid.png"
fig.savefig(out, dpi=300, bbox_inches="tight")
print("saved", out)
