"""Generate the hybrid-architecture schematic for the Step 5 summary.

Shows the encoder -> fuse -> trunk -> heads pattern, plus two concrete
examples (DRQN, AlphaStar). Output: arch_hybrid.png in this directory.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

C_IN = "#eceff3"    # input
C_ENC = "#cfe0fb"   # encoder
C_FUSE = "#e6dbf7"  # fuse / trunk
C_HEAD = "#cdeedd"  # head / output
EC = "#3b4a5a"


def box(ax, x, y, w, h, label, fc, fs=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.10",
                 facecolor=fc, edgecolor=EC, lw=1.2, zorder=2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=3)
    return (x, y, w, h)


def rc(b):
    return (b[0] + b[2], b[1] + b[3] / 2)


def lc(b):
    return (b[0], b[1] + b[3] / 2)


def arr(ax, p, q, color="#5b6b7b", lw=1.4):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12,
                 color=color, lw=lw, zorder=1, shrinkA=1, shrinkB=2))


def title(ax, y, txt):
    ax.text(0.1, y, txt, fontsize=11, fontweight="bold", color="#2c3e50", va="center")


fig, ax = plt.subplots(figsize=(11.5, 9.2))
ax.set_xlim(0, 14)
ax.set_ylim(0, 12)
ax.axis("off")

# ===== Section A: general pattern =====
title(ax, 11.5, "General pattern:  encoders (one per input)  ->  fuse  ->  shared trunk  ->  heads")
H = 0.7
xs_in, xs_enc, x_fuse, x_trunk, x_head = 0.3, 2.9, 5.6, 7.6, 10.4
ys = [10.4, 9.5, 8.6, 7.7]
in_labels = ["Spatial board", "Action history", "Cards / set", "Scalars"]
enc_labels = ["CNN", "RNN / attn.", "Deep Sets", "MLP"]
encs = []
for y, il, el in zip(ys, in_labels, enc_labels):
    b_in = box(ax, xs_in, y, 2.3, H, il, C_IN, fs=9)
    b_en = box(ax, xs_enc, y, 2.3, H, el, C_ENC, fs=9)
    arr(ax, rc(b_in), lc(b_en))
    encs.append(b_en)
fuse = box(ax, x_fuse, ys[-1], 1.5, ys[0] + H - ys[-1], "Fuse\n(concat)", C_FUSE, fs=9)
for b_en in encs:
    arr(ax, rc(b_en), (x_fuse, b_en[1] + b_en[3] / 2))
trunk = box(ax, x_trunk, 8.8, 2.2, 1.4, "Shared trunk\n(MLP / LSTM)", C_FUSE, fs=9)
arr(ax, rc(fuse), lc(trunk))
ph = box(ax, x_head, 9.7, 2.4, 0.7, "Policy head", C_HEAD, fs=9)
vh = box(ax, x_head, 8.6, 2.4, 0.7, "Value head", C_HEAD, fs=9)
arr(ax, rc(trunk), lc(ph))
arr(ax, rc(trunk), lc(vh))

ax.plot([0.1, 13.9], [7.0, 7.0], color="#d0d5db", lw=1, ls="--")

# ===== Section B: DRQN =====
title(ax, 6.5, "Example 1 — DRQN:  CNN -> LSTM -> MLP   (memory for partial observability)")
yB = 5.3
xb = 0.3
prev = None
for lab, fc in [("Frame /\nlocal view", C_IN), ("CNN", C_ENC), ("LSTM", C_ENC),
                ("MLP", C_ENC), ("Q-values\nper action", C_HEAD)]:
    b = box(ax, xb, yB, 2.3, 0.9, lab, fc, fs=9)
    if prev is not None:
        arr(ax, rc(prev), lc(b))
    prev = b
    xb += 2.75

ax.plot([0.1, 13.9], [4.4, 4.4], color="#d0d5db", lw=1, ls="--")

# ===== Section C: AlphaStar =====
title(ax, 3.9, "Example 2 — AlphaStar:  Transformer + CNN + MLP -> LSTM core -> action heads")
xs_in2, xs_enc2, x_cat, x_lstm, x_head2 = 0.3, 2.9, 5.6, 7.6, 10.0
ys2 = [3.0, 2.1, 1.2]
encs2 = []
for y, il, el in zip(ys2, ["Units (set)", "Minimap", "Scalars"],
                     ["Transformer", "CNN", "MLP"]):
    b_in = box(ax, xs_in2, y, 2.3, 0.7, il, C_IN, fs=9)
    b_en = box(ax, xs_enc2, y, 2.3, 0.7, el, C_ENC, fs=9)
    arr(ax, rc(b_in), lc(b_en))
    encs2.append(b_en)
cat = box(ax, x_cat, ys2[-1], 1.5, ys2[0] + 0.7 - ys2[-1], "Concat", C_FUSE, fs=9)
for b_en in encs2:
    arr(ax, rc(b_en), (x_cat, b_en[1] + b_en[3] / 2))
lstm = box(ax, x_lstm, 1.65, 2.0, 1.0, "LSTM\ncore", C_FUSE, fs=9)
arr(ax, rc(cat), lc(lstm))
heads2 = box(ax, x_head2, 1.65, 3.0, 1.0, "Action heads\n(autoregr.)", C_HEAD, fs=9)
arr(ax, rc(lstm), lc(heads2))

plt.tight_layout()
out = "deliverables/reports/step05/summary/arch_hybrid.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print("saved", out)
