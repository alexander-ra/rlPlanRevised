"""
plotting.py -- OPTIONAL, GUARDED plots of a tournament results JSON.

matplotlib is optional: if it is not installed, every function prints a SKIP line and returns
without error (per WORKFLOW.md: plots are a bonus, never a dependency of the core result).

USAGE
    python plotting.py --config smoke     # reads results/smoke_results.json, writes plots/*.png

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


def plot_psro(results: dict, out_dir: str):
    plt = _get_plt()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no PSRO plot.")
        return
    psro = results.get("psro")
    if not psro:
        return
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for key in ("kuhn", "leduc", "matrix", "goofspiel"):
        if key not in psro:
            continue
        h = psro[key]
        label = key if key in ("kuhn", "leduc") else \
            (f"matrix:{h.get('game','')}" if key == "matrix" else f"goofspiel K={h.get('num_cards','')}")
        ax.plot(h["round"], h["exploitability"], marker="o", label=label)
    ax.set_xlabel("PSRO round (population size - 1)")
    ax.set_ylabel("meta-Nash exploitability (NashConv)")
    ax.set_title("PSRO: exploitability shrinks as the population grows")
    ax.axhline(0.5, ls="--", color="grey", lw=1, label="Leduc target < 0.5")
    ax.legend()
    ax.grid(alpha=0.3)
    path = os.path.join(out_dir, "psro_exploitability.png")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
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
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))

    cv = coop["critic_variance"]
    axes[0].bar(["central", "independent"],
                [cv["central_final_loss"], cv["indep_final_loss"]],
                color=["#2a7", "#a44"])
    axes[0].set_title("Critic residual (lower = less variance)")
    axes[0].set_ylabel("final critic loss")

    cr = coop["climbing_reward"]
    axes[1].bar(["IL", "MADDPG", "MAPPO"], [cr["independent"], cr["maddpg"], cr["mappo"]],
                color="#369")
    axes[1].axhline(cr["optimum"], ls="--", color="green", label=f"optimum={cr['optimum']}")
    axes[1].axhline(cr["safe"], ls=":", color="grey", label=f"safe={cr['safe']}")
    axes[1].set_title("Climbing game: CTDE escapes the safe trap")
    axes[1].set_ylabel("greedy reward")
    axes[1].legend()

    cm = coop["communication"]
    axes[2].bar(["comm ON", "comm OFF"], [cm["comm_on_reward"], cm["comm_off_reward"]],
                color=["#2a7", "#a44"])
    axes[2].axhline(cm["no_comm_ceiling"], ls="--", color="grey",
                    label=f"1/K ceiling={cm['no_comm_ceiling']}")
    axes[2].set_title("Communication lifts the listener above 1/K")
    axes[2].set_ylabel("greedy reward")
    axes[2].legend()

    path = os.path.join(out_dir, "coop_ctde_comm.png")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"wrote {path}")


def main():
    ap = argparse.ArgumentParser(description="Plot a Step 09 tournament results JSON.")
    ap.add_argument("--config", default="smoke", choices=["smoke", "scale"])
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
