"""Generate the network-shape schematic for the Step 5 summary.

Shows width profiles: uniform, funnel, hourglass (bottleneck), collar.
Bar height = layer width. Output: arch_shapes.png in this directory.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

FC = "#9bc1ff"
EC = "#1f3a5f"
BOT = "#F3A35F"


def draw_net(ax, widths, title, bidx=None):
    xs = np.linspace(0, 1, len(widths))
    bw = 0.13
    for i, (x, c) in enumerate(zip(xs, widths)):
        h = c / 8.0
        fc = BOT if (bidx is not None and i == bidx) else FC
        ax.add_patch(Rectangle((x - bw / 2, -h / 2), bw, h,
                     facecolor=fc, edgecolor=EC, lw=1.1))
    ax.set_xlim(-0.18, 1.18)
    ax.set_ylim(-0.62, 0.62)
    ax.axis("off")
    ax.set_title(title, fontsize=10.5)


fig, axes = plt.subplots(1, 4, figsize=(12.5, 3.0))
draw_net(axes[0], [6, 6, 6, 6], "Uniform")
draw_net(axes[1], [8, 6, 4, 2], "Funnel (tapering)")
draw_net(axes[2], [8, 4, 1, 4, 8], "Hourglass (bottleneck)", bidx=2)
draw_net(axes[3], [6, 6, 2, 6, 6], "Collar", bidx=2)

plt.tight_layout()
out = "deliverables/reports/step05/summary/arch_shapes.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print("saved", out)
