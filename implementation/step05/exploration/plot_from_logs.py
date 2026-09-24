"""
Plot the Chapter 5 result figures from the saved exploration logs.

Nothing is trained here. The three result figures the chapter prints are drawn
from logs/day01_results.json and logs/day02_results.json and written beside the
summaries, in deliverables/reports/step05/summary/:

  day01_network_sizes.png       Deep CFR exploitability per network size
  day01_deep_cfr_vs_mccfr.png   Deep CFR vs tabular MCCFR against wall-clock time
  day02_nfsp_leduc.png          NFSP exploitability on Leduc over episodes

day01_deep_cfr.py imports the plot functions from this module, so a fresh
training run draws the same figures. Keeping them here also means the Bulgarian
renderer (scripts/figures/render_bg_figures.py) runs this file rather than the
training script, which would retrain every model and overwrite the logs.

Sizes: each figure is drawn at the width it prints at (62 % of a 17.6 cm text
block, about 4.3 in), so a 10 pt font prints at about 10 pt.

The (64, 64) run is left out of the chapter figures: patched, it sits at
1.700-1.706 at every checkpoint, the value the unpatched solver gave, so it is
held back until it is rerun (final review, R5).
"""

from __future__ import annotations

import json
import locale
import os
from types import SimpleNamespace

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(HERE, "logs")
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CHAPTER_FIG_DIR = os.path.join(REPO_ROOT, "deliverables", "reports", "step05", "summary")

# OpenSpiel's exploitability of UniformRandomPolicy on leduc_poker; equals the
# MCCFR checkpoint at iteration 1 in logs/day01_results.json.
LEDUC_UNIFORM_RANDOM = 2.3736

# Held back from the chapter figures until rerun (see module docstring).
RERUN_PENDING = {(64, 64)}

FIGSIZE = (4.3, 2.9)
FONT_SIZE = 10
DPI = 300
COLORS = {(32, 32): "C2", (64, 64): "C3", (128, 128, 128): "C4"}


def _style():
    plt.rcParams["font.size"] = FONT_SIZE


def _layers_label(layers) -> str:
    return "×".join(str(n) for n in layers)


def _plain_ticks(ax):
    """Tick labels that honour the locale's decimal sign (the Bulgarian render
    turns on axes.formatter.use_locale)."""
    def fmt(v, _pos):
        s = f"{v:g}"
        if matplotlib.rcParams.get("axes.formatter.use_locale"):
            s = locale.format_string("%g", v)
        return s
    ax.yaxis.set_major_formatter(FuncFormatter(fmt))


def _save(fig, out_path: str):
    fig.tight_layout()
    fig.savefig(out_path, dpi=DPI)
    plt.close(fig)
    print(f"  saved {out_path}")


def plot_network_size_sweep(runs: list, out_path: str):
    """Exploitability vs outer iterations, one line per network size."""
    _style()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    for i, r in enumerate(runs):
        layers = tuple(r.layers)
        ax.plot(r.checkpoints, r.exploitabilities, marker="o", ms=4,
                label=_layers_label(layers), color=COLORS.get(layers, f"C{i}"))
    ax.set_xlabel("Deep CFR outer iterations")
    ax.set_ylabel("Exploitability")
    _plain_ticks(ax)
    ax.grid(True, alpha=0.3)
    ax.legend()
    _save(fig, out_path)


def plot_deep_cfr_vs_mccfr(deep_runs: list, mccfr_run, out_path: str):
    """Exploitability against wall-clock time - the only axis on which the
    two methods' 'iterations' are comparable."""
    _style()
    fig, ax = plt.subplots(figsize=(FIGSIZE[0], 3.3))
    ax.plot(mccfr_run.wall_times, mccfr_run.exploitabilities,
            marker="o", ms=3, label="Tabular MCCFR", color="C0")
    for i, r in enumerate(deep_runs):
        layers = tuple(r.layers)
        ax.plot(r.wall_times, r.exploitabilities, marker="s", ms=4,
                label=f"Deep CFR ({_layers_label(layers)})",
                color=COLORS.get(layers, f"C{i + 1}"))
    # The reference line is labelled in place: a fourth legend entry leaves no
    # free corner inside the axes at this size.
    ax.axhline(LEDUC_UNIFORM_RANDOM, ls="--", lw=1, color="grey")
    x_right = max(max(r.wall_times) for r in deep_runs + [mccfr_run])
    ax.text(x_right, LEDUC_UNIFORM_RANDOM + 0.05, "Uniform random policy",
            ha="right", va="bottom", color="dimgrey")
    ax.set_xlabel("Wall-clock time (s)")
    ax.set_ylabel("Exploitability")
    ax.set_ylim(0, 2.8)
    _plain_ticks(ax)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.22), ncol=2,
              frameon=False, columnspacing=1.2, handlelength=1.6)
    _save(fig, out_path)


def plot_nfsp(run, out_path: str, uniform_random: float | None = None):
    """NFSP average-policy exploitability vs episodes, with the uniform-random
    level for reference so a curve that never leaves it reads as no learning."""
    _style()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    episodes_k = [c / 1000 for c in run.checkpoints]
    ax.plot(episodes_k, run.exploitabilities, marker="o", ms=4, color="C2",
            label="NFSP (average policy)")
    if uniform_random is not None:
        ax.axhline(uniform_random, ls="--", lw=1, color="grey",
                   label="Uniform random policy")
    ax.set_xlabel("Episodes (thousands)")
    ax.set_ylabel("Exploitability")
    ax.set_ylim(0, 3.4)
    _plain_ticks(ax)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right")
    _save(fig, out_path)


def _load(name: str) -> dict:
    with open(os.path.join(LOG_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    day01 = _load("day01_results.json")
    day02 = _load("day02_results.json")

    deep_runs = [SimpleNamespace(**r) for r in day01["deep_cfr_runs"]]
    shown = [r for r in deep_runs if tuple(r.layers) not in RERUN_PENDING]
    shown.sort(key=lambda r: sum(r.layers))
    mccfr_run = SimpleNamespace(**day01["tabular_mccfr"])
    nfsp_leduc = SimpleNamespace(**day02["nfsp_leduc"])

    plot_network_size_sweep(
        shown, os.path.join(CHAPTER_FIG_DIR, "day01_network_sizes.png"))
    plot_deep_cfr_vs_mccfr(
        shown, mccfr_run, os.path.join(CHAPTER_FIG_DIR, "day01_deep_cfr_vs_mccfr.png"))
    plot_nfsp(
        nfsp_leduc, os.path.join(CHAPTER_FIG_DIR, "day02_nfsp_leduc.png"),
        uniform_random=LEDUC_UNIFORM_RANDOM)


if __name__ == "__main__":
    main()
