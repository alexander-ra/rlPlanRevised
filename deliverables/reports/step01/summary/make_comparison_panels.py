"""Chapter 1 figures 1-2: the rolling-average panel of the saved SB3 comparisons.

STOP-GAP, September 2026 final review (F01-G02/G03). The learning-curve figures
come from implementation/step01/compare_sb3.py, which reads the TensorBoard logs
of our own DQN/PPO runs. Those logs were never committed and are gone, so the
figures cannot be re-drawn without re-training. What is left are the saved
renders:

    figures/dqn_comparison.png  - render of 6 Apr 2026 (commit de7456b): our final
                                  DQN run (1,011 episodes) vs the SB3 DQN run in
                                  implementation/step01/sb3_results_cache.json
    figures/ppo_comparison.png  - render of 3 Apr 2026 (commit 049b4c4): our final
                                  PPO run (547 episodes) vs the SB3 PPO run in the
                                  same cache. (The 6 Apr render had picked up the
                                  earlier [64,64] run instead - review F01-G03.)

Both are two-panel figures, 13 in wide, that print at about half size. This
script keeps only the right-hand panel (rolling average - the only one the text
uses), which then prints near full size, and redraws its axis labels and legend
with matplotlib so that scripts/figures/render_bg_figures.py can produce the
Bulgarian twin from the label mapping like every other figure. The curves, ticks
and tick numbers are the saved pixels, unchanged. The panel title is dropped; the
caption carries it.

Once the runs are repeated and compare_sb3.py draws single-panel figures again,
this script is obsolete: its input check fails and it writes nothing.

Usage (from the repo root):  python deliverables/reports/step01/summary/make_comparison_panels.py
Outputs: figures/{dqn,ppo}_rolling.png and summary/{dqn,ppo}_rolling.png
"""

from pathlib import Path
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).parent.resolve()
FIGURES = HERE.parent / "figures"

C_OUR = "#2196F3"   # as in compare_sb3.py
C_SB3 = "#FF5722"

SRC_SIZE = (1931, 814)            # both saved renders, 150 dpi
SRC_DPI = 150
CROP = (1002, 125, 1924, 717)     # right panel: y tick numbers .. x tick numbers
SCALE = 0.90                      # print scale of the saved pixels
LABEL_FS = 10                     # new text, printed size in pt

PANELS = [
    dict(src="dqn_comparison.png", out="dqn_rolling.png",
         spine_x=1066,                  # left spine column, for the input check
         legend_box=(1078, 351, 1309, 462),
         labels=["Custom DQN", "SB3 DQN", "Target (475)"],
         styles=[dict(color=C_OUR, lw=1.8), dict(color=C_SB3, lw=1.8),
                 dict(color="k", lw=1.2, ls=":")],
         ylabel="Rolling Avg Reward (100 ep)"),
    dict(src="ppo_comparison.png", out="ppo_rolling.png",
         spine_x=1085,
         legend_box=(1097, 144, 1321, 256),
         labels=["Custom PPO", "SB3 PPO", "Target (200)"],
         styles=[dict(color=C_OUR, lw=1.8), dict(color=C_SB3, lw=1.8),
                 dict(color="k", lw=1.2, ls=":")],
         ylabel="Rolling Avg Reward (50 ep)"),
]
BOTTOM_SPINE_Y = 679


def input_ok(img: np.ndarray, spine_x: int) -> bool:
    """The saved two-panel layout, and nothing else, is what the crop assumes."""
    h, w, _ = img.shape
    if (w, h) != SRC_SIZE:
        return False
    dark = img[:, :, :3].astype(int).sum(axis=2) < 200
    return dark[150:670, spine_x].mean() > 0.95 and \
        dark[BOTTOM_SPINE_Y, spine_x + 5:1900].mean() > 0.95


def make_panel(p: dict) -> bool:
    src = FIGURES / p["src"]
    img = np.asarray(Image.open(src).convert("RGB")).copy()
    if not input_ok(img, p["spine_x"]):
        print(f"  {p['src']}: not the saved two-panel render - skipped "
              "(re-draw the figure with compare_sb3.py instead)")
        return False

    x0, y0, x1, y1 = CROP
    crop = img[y0:y1, x0:x1].copy()
    # descenders of the dropped panel title reach the first rows of the crop
    crop[0:4, 1100 - x0:, :] = 255
    ch, cw = crop.shape[:2]

    left, bottom, top, right = 0.34, 0.34, 0.04, 0.04          # inches
    w_in, h_in = cw / SRC_DPI * SCALE, ch / SRC_DPI * SCALE
    fw, fh = left + w_in + right, bottom + h_in + top
    fig = plt.figure(figsize=(fw, fh))
    ax = fig.add_axes([left / fw, bottom / fh, w_in / fw, h_in / fh])
    ax.imshow(crop, extent=(0, cw, ch, 0), interpolation="antialiased")

    # invisible artists, so the legend labels pass through `label=` like any plot
    for lab, st in zip(p["labels"], p["styles"]):
        ax.plot([], [], label=lab, **{**st, "lw": st["lw"] * SCALE})
    ax.set_xlim(0, cw)
    ax.set_ylim(ch, 0)
    ax.axis("off")

    # the new legend sits exactly on the old one and must hide it completely
    bx0, by0, bx1, by1 = p["legend_box"]
    old = [bx0 - x0 - 2, by0 - y0 - 2, bx1 - x0 + 2, by1 - y0 + 2]
    pad = 0.4
    for _ in range(12):
        leg = ax.legend(loc="upper left", bbox_to_anchor=(old[0], old[1]),
                        bbox_transform=ax.transData, borderaxespad=0,
                        fontsize=11 * SCALE, framealpha=1.0, edgecolor="0.8",
                        borderpad=pad)
        fig.canvas.draw()
        bb = leg.get_window_extent()
        (ox0, oy1), (ox1, oy0) = ax.transData.transform([(old[0], old[1]),
                                                         (old[2], old[3])])
        if bb.x0 <= ox0 + 0.5 and bb.x1 >= ox1 and bb.y0 <= oy0 and bb.y1 >= oy1 - 0.5:
            break
        pad += 0.1
        leg.remove()
    else:
        print(f"  {p['src']}: new legend does not cover the old one")
        plt.close(fig)
        return False

    # axis labels, centred on the axes area of the crop
    ax_x0, ax_x1 = p["spine_x"] - x0, 1916 - x0
    ax_y0, ax_y1 = 134 - y0, BOTTOM_SPINE_Y - y0
    ycen = bottom + h_in * (1 - (ax_y0 + ax_y1) / 2 / ch)
    xcen = left + w_in * ((ax_x0 + ax_x1) / 2 / cw)
    fig.text(0.13 / fw, ycen / fh, p["ylabel"], rotation=90,
             ha="center", va="center", fontsize=LABEL_FS)
    fig.text(xcen / fw, 0.12 / fh, "Episode", ha="center", va="center",
             fontsize=LABEL_FS)

    for out in (FIGURES / p["out"], HERE / p["out"]):
        fig.savefig(out, dpi=300)
        print(f"  saved {out.relative_to(HERE.parent.parent.parent.parent)}")
    plt.close(fig)
    return True


def main() -> int:
    ok = [make_panel(p) for p in PANELS]
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
