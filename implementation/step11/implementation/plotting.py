"""
plotting.py -- coalition-dynamics visualizations (raw step 11 L540-544). 🟢 GENERATED infra.

Guarded matplotlib: if it is not installed, every function SKIPs with a message (the tournament /
validation still run and write JSON). Produces four PNGs into `plots/`:

  1. coalition_timeline.png   -- pairwise coalition score over the turns of a sample game
                                 (formation / dissolution, raw L543).
  2. shapley_attribution.png  -- per-player Shapley credit on a sample position (raw L542).
  3. spinning_top.png         -- transitive vs cyclic ratio of the SLS meta-game (raw L544).
  4. coalition_graph.png      -- the end-of-game coalition-score matrix as a heatmap.

Usage (from implementation/step11/implementation/):
    python plotting.py --config smoke      # reads results/<config>_results.json for the ratios

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np


def _mpl():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        return None


def _out_dir():
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
    os.makedirs(d, exist_ok=True)
    return d


def plot_coalition_timeline(plt, n_players: int, move_log, path: str):
    from coalition_detector import coalition_timeline
    turns, series, pairs = coalition_timeline(n_players, move_log)
    if series.shape[0] == 0:
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    for k, (i, j) in enumerate(pairs):
        ax.plot(turns, series[:, k], label=f"{{{i},{j}}}")
    ax.axhline(0.0, color="gray", lw=0.7)
    ax.set_xlabel("turn")
    ax.set_ylabel("coalition score C[i][j]")
    ax.set_title("Coalition formation / dissolution over one game (PREDICTION)")
    ax.legend(fontsize=7, ncol=3)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def plot_shapley_attribution(plt, credit, path: str):
    credit = np.asarray(credit, float)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar([f"P{i}" for i in range(len(credit))], credit)
    ax.set_ylabel("Shapley credit (win-prob share)")
    ax.set_title("Per-player Shapley credit on a sample position (PREDICTION)")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def plot_spinning_top(plt, transitive_ratio: float, cyclic_ratio: float, path: str):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(["transitive", "cyclic"], [transitive_ratio, cyclic_ratio],
           color=["tab:blue", "tab:red"])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Frobenius ratio")
    ax.set_title("SLS meta-game: transitive vs cyclic (Hodge; PREDICT cyclic-heavy)")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def plot_coalition_graph(plt, matrix, path: str):
    M = np.asarray(matrix, float)
    fig, ax = plt.subplots(figsize=(5, 4.5))
    im = ax.imshow(M, cmap="coolwarm", vmin=-abs(M).max() - 1e-9, vmax=abs(M).max() + 1e-9)
    ax.set_xticks(range(M.shape[0]))
    ax.set_yticks(range(M.shape[0]))
    ax.set_title("End-of-game coalition-score matrix (PREDICTION)")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{M[i, j]:.1f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def plot_sweep(plt, reports: dict, path: str):
    """Coalition-emergence sweep: paired gap (shapley - sparse coalition score) vs alpha, one line
    per credit series, error bars = 1 SE, faceted by tier. `reports` = {tier: sweep_report}."""
    tiers = list(reports.keys())
    fig, axes = plt.subplots(1, len(tiers), figsize=(6.2 * len(tiers), 4.4), squeeze=False)
    for ax, tier in zip(axes[0], tiers):
        rep = reports[tier]
        cells = rep["cells"]
        # series key: "counterfactual" or "proxy syn=X"
        series = {}
        for c in cells:
            key = "counterfactual" if c["credit_mode"] == "counterfactual" else f"proxy syn={c['synergy']:.1f}"
            series.setdefault(key, []).append(c)
        for key, cs in sorted(series.items()):
            cs = sorted(cs, key=lambda c: c["alpha"])
            xs = [c["alpha"] for c in cs]
            ys = [c["gap_mean"] for c in cs]
            es = [c["gap_se"] or 0.0 for c in cs]
            ax.errorbar(xs, ys, yerr=es, marker="o", capsize=3, label=key)
        ax.axhline(0.0, color="gray", lw=0.8, ls="--")
        ax.set_xlabel("alpha  (sparse<->credit blend; 0 = pure coalition credit)")
        ax.set_ylabel("coalition-score gap  (shapley - sparse)")
        ax.set_title(f"[{tier}] chips={rep['chips_per_player']} train={rep['train_games']} "
                     f"seeds={rep['n_seeds']}\nsparse baseline score={rep['sparse_coalition_score_mean']:.4f}")
        ax.legend(fontsize=8)
    fig.suptitle("When do coalitions emerge? paired gap > 0 = Shapley beats sparse", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="smoke", choices=["smoke", "scale"])
    ap.add_argument("--sweep", default=None, choices=["smoke", "scale", "both"],
                    help="plot the coalition-emergence sweep from results/sweep_<tier>.json instead")
    args = ap.parse_args()

    plt = _mpl()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no plots. (tournament/validate still run.)")
        return

    if args.sweep:
        res_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
        tiers = ["smoke", "scale"] if args.sweep == "both" else [args.sweep]
        reports = {}
        for t in tiers:
            p = os.path.join(res_dir, f"sweep_{t}.json")
            if os.path.exists(p):
                with open(p, encoding="utf-8") as f:
                    reports[t] = json.load(f)
        if not reports:
            print("[SKIP] no results/sweep_*.json found -- run sweep.py first.")
            return
        out = _out_dir()
        plot_sweep(plt, reports, os.path.join(out, "sweep_coalition_gap.png"))
        print(f"wrote sweep plot ({', '.join(reports)}) to {out}/sweep_coalition_gap.png")
        return

    from config import get_config
    from sls_game import SLSGame, play_game
    from agents import default_baseline_pool
    from coalition_detector import coalition_score_from_log
    from shapley import win_prob_coalition_values, shapley_credit
    from sls_game import SLSState

    cfg = get_config(args.config)
    out = _out_dir()
    n = cfg["n_players"]
    game = SLSGame(n_players=n, chips_per_player=cfg["chips_per_player"])

    # a sample game with heuristic allies so structure is visible
    _names, pool = default_baseline_pool()
    final, _ = play_game(game, pool, seed=cfg["seed"])
    plot_coalition_timeline(plt, n, final.move_log, os.path.join(out, "coalition_timeline.png"))
    plot_coalition_graph(plt, coalition_score_from_log(n, final.move_log),
                         os.path.join(out, "coalition_graph.png"))

    # shapley attribution on an asymmetric position
    asym = SLSState(n_players=n, hands=tuple(tuple((8 if p < 2 else 1) if c == p else 0
                                                   for c in range(n)) for p in range(n)),
                    piles=(), eliminated=frozenset(), current_player=0)
    vals, _wp = win_prob_coalition_values(game, asym, n_rollouts=cfg["shapley_rollouts"], seed=0)
    plot_shapley_attribution(plt, shapley_credit(n, vals),
                             os.path.join(out, "shapley_attribution.png"))

    # spinning top ratios from the results JSON if present, else recompute a small EGTA
    res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results",
                            f"{args.config}_results.json")
    if os.path.exists(res_path):
        with open(res_path, encoding="utf-8") as f:
            egta = json.load(f).get("egta", {})
        tr = egta.get("transitive_ratio")
        cr = egta.get("cyclic_ratio")
    else:
        tr = cr = None
    if tr is None or cr is None:
        from evaluation import run_egta
        egta = run_egta(cfg)
        tr, cr = egta["transitive_ratio"], egta["cyclic_ratio"]
    plot_spinning_top(plt, tr, cr, os.path.join(out, "spinning_top.png"))

    print(f"wrote 4 plots to {out}")


if __name__ == "__main__":
    main()
