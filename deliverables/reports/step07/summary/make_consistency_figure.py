"""Section 5 figure: why responding to the posterior mean can miss the truth.

Two panels on the rock-paper-scissors probability simplex:
  (left)  the true strategy lies OUTSIDE the hull of the modeler's samples -> unreachable.
  (right) the truth lies INSIDE the hull, but the posterior collapses onto a single
          vertex (sample) instead of settling on the true mixture.
Sample values follow Ganzfried (2025, arXiv:2508.17671): left, sigma* = (0.8, 0.1, 0.1)
with samples (0.5, 0.3, 0.2), (0.3, 0.5, 0.2), (0.2, 0.3, 0.5); right (Proposition 2),
sigma* = (1/3, 1/3, 1/3) with s1 = (0.2, 0.4, 0.4), s2 = (0.6, 0.3, 0.1),
s3 = (0.2, 0.3, 0.5), which average to sigma*, and the posterior collapses onto s1.
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

# a label drawn over lines stays readable on a light, borderless backing
LABEL_BG = dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85)


def bary(a, b, c):
    """barycentric (rock, paper, scissors) -> 2D point."""
    return a * R + b * P + c * S


# 8.0 in wide at 300 dpi: printed at 17.6 cm the scale is ~0.87, so fs 10 prints ~8.7 pt
fig, axes = plt.subplots(1, 2, figsize=(8.0, 4.4))

for ax in axes:
    tri = Polygon([R, P, S], closed=True, facecolor="#f3f6fa",
                  edgecolor="#3b4a5a", lw=1.4, zorder=1)
    ax.add_patch(tri)
    ax.text(*(R + [-0.12, -0.18]), "rock", fontsize=10.5, ha="center")
    ax.text(*(P + [0.12, -0.18]), "paper", fontsize=10.5, ha="center")
    ax.text(*(S + [0.0, 0.12]), "scissors", fontsize=10.5, ha="center")
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.55, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")

# ---- LEFT: truth outside the sample hull ----
ax = axes[0]
ax.set_title("Truth outside the sample hull:\nunreachable by any average", fontsize=11)
samples = [bary(0.5, 0.3, 0.2), bary(0.3, 0.5, 0.2), bary(0.2, 0.3, 0.5)]
hull = Polygon(samples, closed=True, facecolor="#cfe0fb", edgecolor="#2c5a8f",
               lw=1.3, alpha=0.75, zorder=2)
ax.add_patch(hull)
for s in samples:
    ax.add_patch(Circle(s, 0.05, facecolor="#2c5a8f", edgecolor="none", zorder=4))
truth = bary(0.8, 0.1, 0.1)
ax.add_patch(Circle(truth, 0.07, facecolor="#d1495b", edgecolor="k", lw=0.8, zorder=5))
ax.text(truth[0] - 0.05, truth[1] + 0.42, "true σ*\n(0.8, 0.1, 0.1)", fontsize=10,
        ha="center", va="center", color="#8c2f3d", bbox=LABEL_BG, zorder=6)
# hull label above the hull, clear of its edges and sample dots
ax.text(np.mean([s[0] for s in samples]), max(s[1] for s in samples) + 0.12,
        "samples'\nhull", fontsize=10, ha="center", va="bottom", color="#22405f",
        bbox=LABEL_BG, zorder=6)

# ---- RIGHT: truth inside, posterior collapses to a vertex ----
ax = axes[1]
ax.set_title("Truth inside the hull:\nposterior still collapses to one sample", fontsize=11)
samples = [bary(0.2, 0.4, 0.4), bary(0.6, 0.3, 0.1), bary(0.2, 0.3, 0.5)]
hull = Polygon(samples, closed=True, facecolor="#cfe0fb", edgecolor="#2c5a8f",
               lw=1.3, alpha=0.75, zorder=2)
ax.add_patch(hull)
for s in samples:
    ax.add_patch(Circle(s, 0.05, facecolor="#2c5a8f", edgecolor="none", zorder=4))
truth = bary(1 / 3, 1 / 3, 1 / 3)
ax.add_patch(Circle(truth, 0.07, facecolor="#d1495b", edgecolor="k", lw=0.8, zorder=5))
ax.text(truth[0] - 0.2, truth[1] + 0.05, "true σ*\n(1/3, 1/3, 1/3)", fontsize=10,
        ha="right", va="center", color="#8c2f3d", bbox=LABEL_BG, zorder=6)
# the posterior collapses onto s1: an orange ring marks it (the samples sit close to
# the centre, so an arrow from sigma* to s1 would be hidden under the dot)
win = samples[0]
ax.add_patch(Circle(win, 0.1, facecolor="none", edgecolor="#e07a1f", lw=2.2, zorder=6))
# below the triangle, on one line, clear of the dots and the hull
ax.text(1.0, -0.40, "belief collapses to one vertex", fontsize=10,
        ha="center", va="center", color="#b5641a")

fig.tight_layout()
out = "deliverables/reports/step07/summary/consistency_convex_hull.png"
fig.savefig(out, dpi=300, bbox_inches="tight")
print("saved", out)
