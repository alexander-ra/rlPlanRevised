"""
plotting.py -- OPTIONAL, GUARDED plots of a tournament results JSON.

matplotlib is optional: if it is not installed, every function prints a SKIP line and returns
without error (per WORKFLOW.md: plots are a bonus, never a dependency of the core result).

USAGE
    python plotting.py                    # reads results/scale_results.json, writes plots/*.png
    python plotting.py --config smoke     # reads results/smoke_results.json instead

The chapter's figures are the scale-config ones (the neural effects only appear at scale), so
scale is the default. Figures are drawn at print size: <= 7.2 in wide, >= 10 pt text, 300 dpi.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import argparse
import json
import os

from config import RESULTS_DIR, PLOTS_DIR


def _get_plt():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        return None


FS = 10
DPI = 300

# Display names for the legend (the results keys are code identifiers).
PSRO_NAMES = {"kuhn": "Kuhn", "leduc": "Leduc"}
MATRIX_GAME_NAMES = {"matching_pennies": "matrix game (Matching Pennies)"}


def _style(plt):
    plt.rcParams.update({"font.size": FS, "axes.titlesize": FS + 0.5, "axes.labelsize": FS,
                         "xtick.labelsize": FS, "ytick.labelsize": FS, "legend.fontsize": FS})


def plot_psro(results: dict, out_dir: str):
    plt = _get_plt()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no PSRO plot.")
        return
    psro = results.get("psro")
    if not psro:
        return
    from matplotlib.ticker import MaxNLocator
    _style(plt)
    fig, ax = plt.subplots(figsize=(6.9, 4.3))
    for key in ("kuhn", "leduc", "matrix", "goofspiel"):
        if key not in psro:
            continue
        h = psro[key]
        if key == "matrix":
            game = h.get("game", "")
            label = MATRIX_GAME_NAMES.get(game, f"matrix game ({game})")
        elif key == "goofspiel":
            label = f"Goofspiel, K={h.get('num_cards', '')}"
        else:
            label = PSRO_NAMES[key]
        ax.plot(h["round"], h["exploitability"], marker="o", ms=4, label=label)
    ax.set_xlabel("PSRO round (population size - 1)")
    ax.set_ylabel("meta-Nash exploitability (NashConv)")
    ax.set_title("PSRO: exploitability shrinks as the population grows")
    ax.axhline(0.5, ls="--", color="grey", lw=1, label="Leduc target < 0.5")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    path = os.path.join(out_dir, "psro_exploitability.png")
    fig.tight_layout()
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(f"wrote {path}")


def plot_coop(results: dict, out_dir: str):
    plt = _get_plt()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no coop plot.")
        return
    coop = results.get("coop")
    if not coop or coop.get("skipped"):
        print("[SKIP] no coop results (torch absent or suite not run).")
        return
    _style(plt)
    # 2 x 2 grid, the climbing game spanning the bottom row: at print width a single row of
    # three panels has no room for 10 pt tick labels and titles (the Bulgarian ones collide).
    fig = plt.figure(figsize=(7.0, 5.6))
    grid = fig.add_gridspec(2, 2)
    axes = [fig.add_subplot(grid[0, 0]), fig.add_subplot(grid[1, :]),
            fig.add_subplot(grid[0, 1])]

    def bars(ax, names, values, color):
        # tick labels go through set_xticklabels so the BG renderer can translate them
        ax.bar(range(len(names)), values, color=color, width=0.6)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names)

    cv = coop["critic_variance"]
    bars(axes[0], ["central", "independent"],
         [cv["central_final_loss"], cv["indep_final_loss"]], ["#2a7", "#a44"])
    axes[0].set_yscale("log")        # 3e-11 vs 0.077: invisible on a linear axis
    axes[0].set_title("Critic residual\n(lower = better fit)")
    axes[0].set_ylabel("final critic loss")

    cr = coop["climbing_reward"]
    bars(axes[1], ["IL", "MADDPG", "MAPPO"],
         [cr["independent"], cr["maddpg"], cr["mappo"]], "#369")
    axes[1].axhline(cr["optimum"], ls="--", color="green", label="optimum")
    axes[1].axhline(cr["safe"], ls=":", color="grey", label="safe")
    axes[1].set_ylim(0, cr["optimum"] * 1.15)
    axes[1].set_title("Climbing game:\nno method reaches the optimum")
    axes[1].set_xlim(-0.6, 4.2)      # room for the legend on the right
    axes[1].set_ylabel("greedy reward")
    axes[1].legend(loc="lower right")

    cm = coop["communication"]
    bars(axes[2], ["comm ON", "comm OFF"],
         [cm["comm_on_reward"], cm["comm_off_reward"]], ["#2a7", "#a44"])
    axes[2].axhline(cm["no_comm_ceiling"], ls="--", color="grey", label="1/K ceiling")
    axes[2].set_ylim(0, 1.0)
    axes[2].set_title("Communication lifts\nthe listener above 1/K")
    axes[2].set_ylabel("greedy reward")
    axes[2].legend(loc="upper right")

    path = os.path.join(out_dir, "coop_ctde_comm.png")
    fig.tight_layout()
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(f"wrote {path}")


def main():
    ap = argparse.ArgumentParser(description="Plot a Step 09 tournament results JSON.")
    ap.add_argument("--config", default="scale", choices=["smoke", "scale"])
    args = ap.parse_args()

    in_path = os.path.join(RESULTS_DIR, f"{args.config}_results.json")
    if not os.path.isfile(in_path):
        print(f"[SKIP] {in_path} not found -- run tournament.py --config {args.config} first.")
        return
    with open(in_path, encoding="utf-8") as f:
        results = json.load(f)
    os.makedirs(PLOTS_DIR, exist_ok=True)
    plot_psro(results, PLOTS_DIR)
    plot_coop(results, PLOTS_DIR)


if __name__ == "__main__":
    main()
