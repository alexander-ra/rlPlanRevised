"""Generate the layer-family connectivity schematic for the Step 5 summary.

Four panels (MLP / CNN / RNN / self-attention) showing how the families differ
in *wiring* and *weight sharing*. Output: arch_comparison.png in this directory.
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import numpy as np

NODE_R = 0.18
NODE_FC = "#5B8FF9"
NODE_EC = "#1f3a5f"
SHARE = ["#E8684A", "#F6BD16", "#3AA76D"]  # three shared-filter weight colours


def node(ax, x, y, r=NODE_R, fc=NODE_FC, ec=NODE_EC, z=3):
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, lw=1.3, zorder=z))
    return (x, y)


def _trim(p, q, shrink):
    dx, dy = q[0] - p[0], q[1] - p[1]
    d = math.hypot(dx, dy) or 1.0
    ux, uy = dx / d, dy / d
    return (p[0] + ux * shrink, p[1] + uy * shrink), (q[0] - ux * shrink, q[1] - uy * shrink)


def edge(ax, p, q, color="#b8c2cc", lw=1.0, z=1, alpha=1.0, shrink=NODE_R):
    p2, q2 = _trim(p, q, shrink)
    ax.plot([p2[0], q2[0]], [p2[1], q2[1]], color=color, lw=lw, zorder=z,
            alpha=alpha, solid_capstyle="round")


def arrow(ax, p, q, color="#34495e", lw=1.4, z=2, shrink=NODE_R):
    p2, q2 = _trim(p, q, shrink)
    ax.add_patch(FancyArrowPatch(p2, q2, arrowstyle="-|>", mutation_scale=11,
                                 color=color, lw=lw, zorder=z))


fig, axes = plt.subplots(2, 2, figsize=(11, 8.2))
for ax in axes.ravel():
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4.3)
    ax.set_aspect("equal")
    ax.axis("off")

# ---- MLP ----
ax = axes[0, 0]
ax.set_title("Fully connected (MLP)\nevery unit connects to every unit", fontsize=10.5)
inp = [node(ax, 1.0, y, fc="#9bc1ff") for y in (0.8, 1.7, 2.6, 3.5)]
hid = [node(ax, 3.0, y) for y in (1.2, 2.2, 3.2)]
out = [node(ax, 5.0, y, fc="#7bd0a8") for y in (1.6, 2.8)]
for p in inp:
    for q in hid:
        edge(ax, p, q)
for p in hid:
    for q in out:
        edge(ax, p, q)

# ---- CNN ----
ax = axes[0, 1]
ax.set_title("Convolution (CNN)\none shared filter slid over local windows", fontsize=10.5)
xin = np.linspace(0.6, 5.4, 6)
inp = [node(ax, x, 1.0, r=0.16, fc="#9bc1ff") for x in xin]
outA = node(ax, 1.8, 3.3, r=0.16, fc="#7bd0a8")
outB = node(ax, 3.6, 3.3, r=0.16, fc="#7bd0a8")
for k, i in enumerate((0, 1, 2)):
    edge(ax, (xin[i], 1.0), outA, color=SHARE[k], lw=1.9, shrink=0.16)
for k, i in enumerate((2, 3, 4)):
    edge(ax, (xin[i], 1.0), outB, color=SHARE[k], lw=1.9, shrink=0.16)
ax.text(3.0, 0.15, "same colour = same (shared) weight", fontsize=8.5,
        ha="center", color="#555")

# ---- RNN ----
ax = axes[1, 0]
ax.set_title("Recurrent (RNN)\nsame cell over time, hidden state = memory", fontsize=10.5)
xs = np.linspace(0.9, 5.1, 4)
xin = [node(ax, x, 0.8, fc="#9bc1ff") for x in xs]
hid = [node(ax, x, 2.6) for x in xs]
for i in range(4):
    arrow(ax, xin[i], hid[i], color=SHARE[2], lw=1.7)
for i in range(3):
    arrow(ax, hid[i], hid[i + 1], color=SHARE[0], lw=1.7)
for i, x in enumerate(xs):
    ax.text(x, 0.12, f"t={i + 1}", fontsize=8.5, ha="center", color="#555")

# ---- Attention ----
ax = axes[1, 1]
ax.set_title("Self-attention (Transformer)\nevery element attends to all others", fontsize=10.5)
keys_x = np.linspace(0.8, 5.2, 5)
keys = [node(ax, x, 2.9, fc="#9bc1ff") for x in keys_x]
query = node(ax, 3.0, 0.9, fc="#F3A35F")
for k in keys:
    arrow(ax, query, k, color="#E8684A", lw=1.3)
ax.text(3.0, 0.18, "one (orange) query token attends to all", fontsize=8.5,
        ha="center", color="#555")

plt.tight_layout()
out_path = "deliverables/reports/step05/summary/arch_comparison.png"
fig.savefig(out_path, dpi=130, bbox_inches="tight")
print("saved", out_path)
