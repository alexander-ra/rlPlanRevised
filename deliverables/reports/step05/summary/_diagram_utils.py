"""Box and arrow primitives for the Step 5 architecture diagrams.

The hybrid-architecture figure draws its labelled boxes through box() here
rather than through a local helper, because the Bulgarian figure renderer wraps
this module's box(): it translates the label, re-wraps it to the box width and
reports any label that still overflows. A local helper would get the
translation but not the fitting.
"""
import matplotlib
matplotlib.use("Agg")
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

EC = "#3b4a5a"


def box(ax, x, y, w, h, label, fc, fs=10.0, ec=EC, lw=1.2, z=2, fontweight=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.10",
                 facecolor=fc, edgecolor=ec, lw=lw, zorder=z))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, zorder=z + 1, fontweight=fontweight)
    return (x, y, w, h)


def rc(b):
    """Right-centre anchor of a box tuple (x, y, w, h)."""
    return (b[0] + b[2], b[1] + b[3] / 2)


def lc(b):
    """Left-centre anchor."""
    return (b[0], b[1] + b[3] / 2)


def arrow(ax, p, q, color="#5b6b7b", lw=1.4):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12,
                 color=color, lw=lw, zorder=1, shrinkA=1, shrinkB=2))
