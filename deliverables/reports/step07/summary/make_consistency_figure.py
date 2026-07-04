"""Section 5 figure: why responding to the posterior mean can miss the truth.

Two panels on the rock-paper-scissors probability simplex:
  (left)  the true strategy lies OUTSIDE the hull of the modeler's samples -> unreachable.
  (right) the truth lies INSIDE the hull, but the posterior collapses onto a single
          vertex (sample) instead of settling on the true mixture.
Motivates the sequence-form consistent (FMAP) estimator. Output: consistency_convex_hull.png.
Run from repo root with the project .venv active.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import numpy as np

# 2-simplex corners (rock, paper, scissors) drawn as a triangle
R = np.array([0.0, 0.0])
P = np.array([2.0, 0.0])
S = np.array([1.0, 1.732])


def bary(a, b, c):
    """barycentric (rock, paper, scissors) -> 2D point."""
    return a * R + b * P + c * S


fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.1))

for ax in axes:
    tri = Polygon([R, P, S], closed=True, facecolor="#f3f6fa",
                  edgecolor="#3b4a5a", lw=1.4, zorder=1)
    ax.add_patch(tri)
    ax.text(*(R + [-0.12, -0.16]), "rock", fontsize=9, ha="center")
    ax.text(*(P + [0.12, -0.16]), "paper", fontsize=9, ha="center")
    ax.text(*(S + [0.0, 0.14]), "scissors", fontsize=9, ha="center")
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.4, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")

# ---- LEFT: truth outside the sample hull ----
ax = axes[0]
ax.set_title("Truth outside the sample hull:\nunreachable by any average", fontsize=10.5)
samples = [bary(0.5, 0.3, 0.2), bary(0.3, 0.5, 0.2), bary(0.45, 0.2, 0.35)]
hull = Polygon(samples, closed=True, facecolor="#cfe0fb", edgecolor="#2c5a8f",
               lw=1.3, alpha=0.75, zorder=2)
ax.add_patch(hull)
for s in samples:
    ax.add_patch(Circle(s, 0.05, facecolor="#2c5a8f", edgecolor="none", zorder=4))
truth = bary(0.8, 0.1, 0.1)
ax.add_patch(Circle(truth, 0.07, facecolor="#d1495b", edgecolor="k", lw=0.8, zorder=5))
ax.text(truth[0] + 0.02, truth[1] + 0.18, "true \u03c3*\n(0.8, 0.1, 0.1)", fontsize=8.2,
        ha="center", color="#8c2f3d")
ax.text(np.mean([s[0] for s in samples]), np.mean([s[1] for s in samples]) - 0.02,
        "samples'\nhull", fontsize=8.0, ha="center", color="#22405f")

# ---- RIGHT: truth inside, posterior collapses to a vertex ----
ax = axes[1]
ax.set_title("Truth inside the hull:\nposterior still collapses to one sample", fontsize=10.5)
samples = [bary(0.6, 0.25, 0.15), bary(0.2, 0.6, 0.2), bary(0.25, 0.2, 0.55)]
hull = Polygon(samples, closed=True, facecolor="#cfe0fb", edgecolor="#2c5a8f",
               lw=1.3, alpha=0.75, zorder=2)
ax.add_patch(hull)
for s in samples:
    ax.add_patch(Circle(s, 0.05, facecolor="#2c5a8f", edgecolor="none", zorder=4))
truth = bary(1 / 3, 1 / 3, 1 / 3)
ax.add_patch(Circle(truth, 0.07, facecolor="#d1495b", edgecolor="k", lw=0.8, zorder=5))
ax.text(truth[0], truth[1] - 0.22, "true \u03c3*\n(1/3, 1/3, 1/3)", fontsize=8.2,
        ha="center", color="#8c2f3d")
# arrow: belief drifts from centre toward one vertex
win = samples[0]
ax.annotate("", xy=win + (truth - win) * 0.18, xytext=truth,
            arrowprops=dict(arrowstyle="-|>", color="#e07a1f", lw=2.0), zorder=6)
ax.text(win[0] + 0.02, win[1] + 0.16, "belief collapses\nto one vertex", fontsize=8.0,
        ha="center", color="#b5641a")

fig.tight_layout()
out = "deliverables/reports/step07/summary/consistency_convex_hull.png"
fig.savefig(out, dpi=200, bbox_inches="tight")
print("saved", out)
