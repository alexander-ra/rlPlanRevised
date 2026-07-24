"""Shared matplotlib primitives for the Step 10 summary figures.

One place for the box/arrow/panel drawing code the conceptual diagrams share; style
mirrors deliverables/reports/step09/summary/_diagram_utils.py (FancyBboxPatch rounded
boxes, FancyArrowPatch arrows, muted flat palette). Run each make_*_figure.py from the
repo root with the project .venv active; outputs land next to this file.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

EC = "#3b4a5a"           # default edge/stroke colour
C_SAFE = "#cfe0fb"       # safety / Nash / blueprint (blue)
C_EXPLOIT = "#f7c6c0"    # exploitation / exploiter block (red-ish)
C_MODEL = "#cdeedd"      # model / population block (green)
C_NET = "#ffe1a8"        # highlighted / key block (orange)
C_ANNOT = "#eceff3"      # neutral annotation / side box (grey)
C_PANEL_BG_A = "#f5f8fd"
C_PANEL_BG_B = "#f3fbf6"


def box(ax, x, y, w, h, label, fc=C_ANNOT, fs=9.0, ec=EC, lw=1.2, z=3, fontweight=None):
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


def tc(b):
    """Top-centre anchor."""
    return (b[0] + b[2] / 2, b[1] + b[3])


def bc(b):
    """Bottom-centre anchor."""
    return (b[0] + b[2] / 2, b[1])


def cc(b):
    """Centre anchor."""
    return (b[0] + b[2] / 2, b[1] + b[3] / 2)


def arrow(ax, p, q, color=EC, lw=1.4, z=1, style="-|>", dashed=False,
          rad=0.0, mutation_scale=12, shrinkA=1, shrinkB=2):
    connectionstyle = f"arc3,rad={rad}" if rad else None
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=mutation_scale,
                 color=color, lw=lw, zorder=z, shrinkA=shrinkA, shrinkB=shrinkB,
                 linestyle=(0, (4, 3)) if dashed else "solid",
                 connectionstyle=connectionstyle))


def panel_bg(ax, x, y, w, h, fc, label=None, label_fs=10.5):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor="none", zorder=0))
    if label:
        ax.text(x + w / 2, y + h - 0.32, label, ha="center", va="center",
                fontsize=label_fs, fontweight="bold", color="#2c3e50", zorder=1, clip_on=False)


def note(ax, x, y, text, fs=7.6, color="#5b6b7b", ha="center", va="center", style="italic"):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color, style=style, zorder=4)


def new_fig(w=13.5, h=9.0, xlim=(0, 14), ylim=(0, 10), shrink=1.8):
    """shrink divides the physical canvas size while data coordinates stay unchanged,
    so fixed-point font sizes end up proportionally larger relative to the boxes once
    the image is embedded at PDF page width."""
    fig, ax = plt.subplots(figsize=(w / shrink, h / shrink))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def save(fig, out, dpi=330):
    plt.tight_layout()
    fig.savefig(out, dpi=dpi, bbox_inches="tight", pad_inches=0.12)
    print("saved", out)
