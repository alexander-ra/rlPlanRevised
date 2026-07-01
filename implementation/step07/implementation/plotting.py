"""
Plotting for the Step 07 tournament results.

Renders three figures per game from the results dict (or the saved JSON):
  - exploitation_<game>.png   : realized mean/hand per model per opponent, with the exact
                                Nash-EV and best-response ceiling drawn in for reference.
  - cumulative_<game>.png     : cumulative profit curves vs a few exploitable types.
  - nonstationarity_<game>.png: static vs change-point exploiter through a mid-match switch.

matplotlib is imported at module load, so a missing install surfaces as an ImportError when
tournament.py tries `import plotting` -- which it catches and skips gracefully.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")  # file output only; no interactive backend needed
import matplotlib.pyplot as plt  # noqa: E402


def plot_exploitation(result: dict, out_path: str):
    exploitation = result.get("exploitation", {})
    if not exploitation:
        return
    types = list(exploitation)
    model_names = list(next(iter(exploitation.values()))["models"].keys())
    x = range(len(types))
    width = 0.8 / max(1, len(model_names))

    fig, ax = plt.subplots(figsize=(max(8, 1.1 * len(types)), 5))
    for j, m in enumerate(model_names):
        vals = [exploitation[t]["models"][m]["mean_per_hand"] for t in types]
        ax.bar([i + j * width for i in x], vals, width=width, label=m)
    ceiling = [exploitation[t]["references"]["ceiling"] for t in types]
    nash_ev = [exploitation[t]["references"]["nash_ev"] for t in types]
    center = [i + (len(model_names) - 1) * width / 2 for i in x]
    ax.plot(center, ceiling, "k_", markersize=18, markeredgewidth=2, label="BR ceiling (exact)")
    ax.plot(center, nash_ev, "r_", markersize=18, markeredgewidth=2, label="Nash EV (exact)")
    ax.axhline(0.0, color="grey", lw=0.8)
    ax.set_xticks(center)
    ax.set_xticklabels(types, rotation=30, ha="right")
    ax.set_ylabel("hero mean profit / hand")
    ax.set_title(f"Exploitation vs opponent type ({result.get('game')}, {result.get('config')})")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_cumulative(result: dict, out_path: str, max_types: int = 4):
    exploitation = result.get("exploitation", {})
    if not exploitation:
        return
    types = list(exploitation)[:max_types]
    model_names = list(next(iter(exploitation.values()))["models"].keys())
    fig, axes = plt.subplots(1, len(types), figsize=(4 * len(types), 4), squeeze=False)
    for col, t in enumerate(types):
        ax = axes[0][col]
        for m in model_names:
            curve = result["exploitation"][t]["models"][m].get("cumulative_seed0") or []
            ax.plot(range(len(curve)), curve, label=m, lw=1.2)
        ax.axhline(0.0, color="grey", lw=0.8)
        ax.set_title(t, fontsize=10)
        ax.set_xlabel("hand (downsampled)")
        if col == 0:
            ax.set_ylabel("cumulative profit")
            ax.legend(fontsize=8)
    fig.suptitle(f"Cumulative exploitation profit ({result.get('game')})")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_nonstationarity(result: dict, out_path: str):
    ns = result.get("nonstationarity", {})
    variants = ns.get("variants", {})
    if not variants:
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    for variant, blk in variants.items():
        curve = blk.get("cumulative") or []
        ax.plot(range(len(curve)), curve, label=variant, lw=1.4)
        for cp in blk.get("changepoints", []):
            # cp is a hand index; the curve is downsampled, so mark proportionally.
            frac = cp / max(1, ns.get("total", 1))
            ax.axvline(frac * len(curve), color="green", ls=":", lw=0.8)
    # mark the true switch point proportionally too
    frac = ns.get("switch_at", 0) / max(1, ns.get("total", 1))
    any_curve = next(iter(variants.values())).get("cumulative") or [0]
    ax.axvline(frac * len(any_curve), color="black", ls="--", lw=1.0, label="true switch")
    ax.set_xlabel("hand (downsampled)")
    ax.set_ylabel("cumulative profit")
    ax.set_title(f"Non-stationarity: {ns.get('first')} -> {ns.get('second')} "
                 f"({result.get('game')})")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_posterior_evolution(history: list, type_names: list, out_path: str):
    """Standalone helper: plot a type-based posterior trajectory (model.history)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for name in type_names:
        series = [post.get(name, 0.0) for post in history]
        ax.plot(range(len(series)), series, label=name, lw=1.2)
    ax.set_xlabel("hands observed")
    ax.set_ylabel("posterior probability")
    ax.set_ylim(-0.02, 1.02)
    ax.set_title("Type posterior evolution")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_all(all_results: dict, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    for game_name, result in all_results.items():
        plot_exploitation(result, os.path.join(out_dir, f"exploitation_{game_name}.png"))
        plot_cumulative(result, os.path.join(out_dir, f"cumulative_{game_name}.png"))
        plot_nonstationarity(result, os.path.join(out_dir, f"nonstationarity_{game_name}.png"))
