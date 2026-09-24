"""Shared matplotlib primitives for the Chapter 7 summary figures.

Default text size is 10 pt: at the 17.6 cm print width (shrink=1.7) one matplotlib
point prints as ~0.85 pt, so 10 prints at ~8.5 pt, above the 8.2 pt legibility floor.

One place for the box/arrow/panel drawing code the conceptual diagrams share; style
mirrors deliverables/reports/step06/summary/_diagram_utils.py (FancyBboxPatch rounded
boxes, FancyArrowPatch arrows, muted flat palette). Run each make_*_figure.py from the
repo root with the project .venv active; outputs land next to this file.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.transforms import Bbox

EC = "#3b4a5a"           # default edge/stroke colour
C_SAFE = "#cfe0fb"       # safety / Nash / blueprint (blue)
C_EXPLOIT = "#f7c6c0"    # exploitation / lean-in (red-ish)
C_MODEL = "#cdeedd"      # model / inference block (green)
C_NET = "#ffe1a8"        # highlighted / key block (orange)
C_ANNOT = "#eceff3"      # neutral annotation / side box (grey)
C_PANEL_BG_A = "#f5f8fd"
C_PANEL_BG_B = "#f3fbf6"


def box(ax, x, y, w, h, label, fc=C_ANNOT, fs=10.0, ec=EC, lw=1.2, z=3, fontweight=None):
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


def note(ax, x, y, text, fs=10.0, color="#5b6b7b", ha="center", va="center", style="italic"):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color, style=style, zorder=4)


def new_fig(w=13.5, h=9.0, xlim=(0, 14), ylim=(0, 10), shrink=1.8):
    """shrink divides the physical canvas size while data coordinates stay unchanged,
    so fixed-point font sizes end up proportionally larger relative to the boxes once
    the image is embedded at PDF page width."""
    fig, ax = plt.subplots(figsize=(w / shrink, h / shrink))
    # The axes fill the figure from the start (there are no axis labels to make room
    # for). A later tight_layout() would enlarge the axes after the boxes were drawn,
    # so anything that measures text against a box while drawing (the Bulgarian
    # renderer re-wraps labels to fit) would see boxes ~25 % smaller than printed.
    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.005, top=0.995)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def save(fig, out, dpi=330, pad=0.12):
    # No tight_layout(): new_fig already sizes the axes to the figure, and changing
    # them now would move every box relative to its (already fitted) text.
    # Crop to the drawn content rather than bbox_inches="tight", which keeps the whole
    # (invisible) axes and so makes the image wider and every label print smaller.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    parts = [a.get_window_extent(renderer)
             for ax in fig.axes for a in (*ax.patches, *ax.texts) if a.get_visible()]
    content = Bbox.union(parts).transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(out, dpi=dpi, bbox_inches=content.padded(pad))
    print("saved", out)
