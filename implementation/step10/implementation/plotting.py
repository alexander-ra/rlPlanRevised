"""
plotting.py -- OPTIONAL, GUARDED plots of a Step 10 results JSON.

matplotlib is optional: if it is not installed, every function prints a SKIP line and returns
without error (per WORKFLOW.md: plots are a bonus, never a dependency of the core result).

Phase portraits are re-simulated from the config (the replicator dynamics are cheap and
deterministic, so we don't bloat the results JSON with full trajectories); the league /
baseline / spinning-top plots read the results JSON.

USAGE
    python plotting.py --config smoke     # reads results/smoke_results.json, writes plots/*.png

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import argparse
import json
import os

import deps  # noqa: F401
from config import RESULTS_DIR, PLOTS_DIR, get_config


def _get_plt():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        return None


def plot_replicator_portraits(config: dict, out_dir: str):
    plt = _get_plt()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no replicator portraits.")
        return
    import numpy as np
    import evo_games
    import replicator as rep
    rc = config["replicator"]
    games = rc["games"]
    fig, axes = plt.subplots(1, len(games), figsize=(4.2 * len(games), 4))
    if len(games) == 1:
        axes = [axes]
    rng = np.random.default_rng(config["seed"])
    for ax, name in zip(axes, games):
        g = evo_games.make_evo_game(name)
        starts = rc.get("starts", {}).get(name) or [rep._normalize(rng.random(g.n) + 0.1).tolist()]
        for x0 in starts:
            xs = np.array(rep.simulate_single(g.A, x0, T=rc["T"], dt=rc["dt"]))
            ax.plot(xs[:, 0], lw=1.3, label=f"x0[0]={round(x0[0], 2)}")
        ax.set_title(f"{name}\n(P[{g.action_names[0]}] over time)")
        ax.set_xlabel("replicator step")
        ax.set_ylabel(f"share of {g.action_names[0]}")
        ax.set_ylim(-0.02, 1.02)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7)
    path = os.path.join(out_dir, "replicator_portraits.png")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"wrote {path}")


def plot_transitive_ratios(results: dict, out_dir: str):
    plt = _get_plt()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no spinning-top plot.")
        return
    st = results.get("spinning_top")
    if not st:
        return
    names, ratios = [], []
    for key, block in st.items():
        names.append(key)
        ratios.append(block.get("transitive_ratio_hodge", 0.0))
    league = results.get("league", {})
    if league and not league.get("skipped") and "league_metagame_transitive_ratio" in league:
        names.append("league_metagame")
        ratios.append(league["league_metagame_transitive_ratio"])
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.bar(names, ratios, color="#369")
    ax.axhline(1.0, ls="--", color="green", lw=1, label="pure skill (transitive)")
    ax.axhline(0.0, ls=":", color="grey", lw=1, label="pure cycling (RPS)")
    ax.set_ylabel("transitive ratio  ||T|| / ||A_anti||")
    ax.set_title("Spinning-top: how much of each game is real skill vs cycling")
    ax.set_ylim(0, 1.05)
    ax.tick_params(axis="x", rotation=20)
    ax.legend()
    path = os.path.join(out_dir, "transitive_ratios.png")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"wrote {path}")


def plot_league(results: dict, out_dir: str):
    plt = _get_plt()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no league plot.")
        return
    league = results.get("league")
    if not league or league.get("skipped"):
        print("[SKIP] no league results (torch absent or suite not run).")
        return
    tr = league["trajectory"]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(tr["epoch"], tr["min_main_exploitability"], marker="o", label="min main-agent exploitability")
    ax.plot(tr["epoch"], tr["meta_nash_exploitability"], marker="s", label="meta-Nash exploitability")
    ax.set_xlabel("league epoch")
    ax.set_ylabel("exploitability (NashConv, exact)")
    ax.set_title("PBT league: exploitability over training (PREDICT: decreasing)")
    ax.grid(alpha=0.3)
    ax.legend()
    path = os.path.join(out_dir, "league_exploitability.png")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"wrote {path}")


def plot_comparison(results: dict, out_dir: str):
    plt = _get_plt()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no comparison plot.")
        return
    base = results.get("baselines")
    if not base:
        return
    labels, vals = [], []
    league = results.get("league", {})
    if league and not league.get("skipped"):
        labels.append("league\n(meta-Nash)")
        vals.append(league["egta"]["meta_nash_exploitability"])
    labels.append(f"PSRO\n({base['psro']['rounds']} rnd)")
    vals.append(base["psro"]["final_exploitability"])
    if not base["selfplay"].get("skipped"):
        labels.append("self-play\n(1 agent)")
        vals.append(base["selfplay"]["final_exploitability"])
    labels.append("CFR Nash")
    vals.append(base["cfr_nash"]["exploitability"])
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.bar(labels, vals, color="#a44")
    ax.set_ylabel("Leduc exploitability (lower = closer to Nash)")
    ax.set_title("Comparison on Leduc (PREDICT: CFR Nash ~ 0 is the floor)")
    ax.grid(alpha=0.3, axis="y")
    path = os.path.join(out_dir, "comparison_exploitability.png")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"wrote {path}")


def main():
    ap = argparse.ArgumentParser(description="Plot a Step 10 tournament results JSON.")
    ap.add_argument("--config", default="smoke", choices=["smoke", "scale"])
    args = ap.parse_args()

    cfg = get_config(args.config)
    in_path = os.path.join(RESULTS_DIR, f"{args.config}_results.json")
    results = {}
    if os.path.isfile(in_path):
        with open(in_path, encoding="utf-8") as f:
            results = json.load(f)
    else:
        print(f"[note] {in_path} not found -- phase portraits still render from config; run "
              f"tournament.py --config {args.config} for the rest.")

    os.makedirs(PLOTS_DIR, exist_ok=True)
    plot_replicator_portraits(cfg, PLOTS_DIR)
    plot_transitive_ratios(results, PLOTS_DIR)
    plot_league(results, PLOTS_DIR)
    plot_comparison(results, PLOTS_DIR)


if __name__ == "__main__":
    main()
