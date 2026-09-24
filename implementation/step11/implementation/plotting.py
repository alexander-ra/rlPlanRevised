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
    python plotting.py                     # chapter figures from SAVED results only (no games are
                                           # played, nothing is written to results/): the detector
                                           # matrix, the two-position Shapley credit and the sweep,
                                           # into deliverables/reports/step11/summary/impl_*.png
    python plotting.py --config smoke      # (legacy) simulates a sample game/position -> plots/
    python plotting.py --sweep both        # (legacy) sweep plot -> plots/sweep_coalition_gap.png

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


def plot_shapley_two_positions(plt, symmetric, asymmetric, path: str):
    """Grouped bars: per-seat Shapley credit on the symmetric and the asymmetric [8,8,1,1] position,
    as saved in results/smoke_results.json (`shapley` block). Sized to print at ~12.7 cm."""
    sym = np.asarray(symmetric, float)
    asym = np.asarray(asymmetric, float)
    x = np.arange(len(sym))
    w = 0.38
    fig, ax = plt.subplots(figsize=(5.0, 3.2))
    ax.bar(x - w / 2, sym, w, color="tab:blue", label="symmetric position")
    ax.bar(x + w / 2, asym, w, color="tab:orange", label="asymmetric [8,8,1,1]")
    ax.axhline(0.25, ls="--", color="gray", lw=1.0, label="equal share 0.25")
    ax.set_xticks(x)
    ax.set_xticklabels([f"seat {i}" for i in range(len(sym))], fontsize=10)
    ax.set_ylabel("Shapley credit\n(win-probability share)", fontsize=10)
    ax.set_ylim(0, 0.8)
    ax.tick_params(labelsize=10)
    ax.legend(fontsize=9.6, loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
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


def plot_detector_matrix(plt, matrix, path: str):
    """Coalition-score matrix of the planted-alliance test, as saved in
    results/smoke_results.json (`detector.coalition_matrix`). Sized to print at ~11 cm."""
    M = np.asarray(matrix, float)
    n = M.shape[0]
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    im = ax.imshow(M, cmap="RdBu", vmin=-10, vmax=10)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.tick_params(labelsize=10)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{M[i, j]:.0f}", ha="center", va="center", fontsize=11,
                    color="white" if abs(M[i, j]) > 6 else "black")
    ax.set_xlabel("player", fontsize=10)
    ax.set_ylabel("player", fontsize=10)
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("mutual net support", fontsize=10)
    cb.ax.tick_params(labelsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def plot_sweep(plt, reports: dict, path: str):
    """Coalition-score sweep: paired gap (shapley - sparse coalition score) vs alpha, one line
    per credit series, error bars = 1 SE, faceted by tier. `reports` = {tier: sweep_report}.
    Sized to print at full text width (17.6 cm) with every label >= 9.6 pt."""
    tiers = list(reports.keys())
    tier_title = {"smoke": "smoke ({c} chips, {g} games)", "scale": "scale ({c} chips, {g} games)"}
    series_label = {"counterfactual": "rollout credit",
                    "proxy syn=0.1": "proxy, synergy 0.1",
                    "proxy syn=0.3": "proxy, synergy 0.3"}
    colors = {"counterfactual": "tab:blue", "proxy syn=0.1": "tab:orange", "proxy syn=0.3": "tab:green"}
    fig, axes = plt.subplots(1, len(tiers), figsize=(7.0, 3.8), squeeze=False)
    for k, (ax, tier) in enumerate(zip(axes[0], tiers)):
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
            ax.errorbar(xs, ys, yerr=es, marker="o", ms=4, capsize=3, color=colors.get(key),
                        label=series_label.get(key, key))
        ax.axhline(0.0, color="gray", lw=0.8, ls="--")
        ax.set_ylabel("coalition-score gap\n(Shapley − sparse)", fontsize=10)
        ax.set_title(tier_title.get(tier, tier).format(c=rep["chips_per_player"], g=rep["train_games"]),
                     fontsize=10)
        ax.tick_params(labelsize=9.6)
        ax.set_xticks([0.0, 0.1, 0.3, 0.5, 0.7])
    # one legend below both panels: inside a panel it covers the steep alpha 0 -> 0.1 lines
    handles, labels = axes[0][-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=9.6, frameon=False,
               bbox_to_anchor=(0.5, 0.0), columnspacing=1.2, handlelength=1.6)
    fig.text(0.5, 0.085, "$\\alpha$ (0 = coalition credit only, 1 = sparse only)",
             ha="center", va="bottom", fontsize=10)
    fig.tight_layout(rect=(0, 0.15, 1, 1))
    fig.savefig(path, dpi=300)
    plt.close(fig)


def plot_from_saved_results():
    """Draw the chapter's result figures from the SAVED results only - no game is played, nothing
    is trained, and no results file is written. Output goes straight to the chapter summary folder
    (deliverables/reports/step11/summary/impl_*.png), where the summary links it."""
    plt = _mpl()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no plots.")
        return
    here = os.path.dirname(os.path.abspath(__file__))
    res_dir = os.path.join(here, "results")
    repo = os.path.abspath(os.path.join(here, "..", "..", ".."))
    out = os.path.join(repo, "deliverables", "reports", "step11", "summary")
    with open(os.path.join(res_dir, "smoke_results.json"), encoding="utf-8") as f:
        smoke = json.load(f)
    plot_detector_matrix(plt, smoke["detector"]["coalition_matrix"],
                         os.path.join(out, "impl_coalition_graph.png"))
    plot_shapley_two_positions(plt, smoke["shapley"]["symmetric_credit"],
                               smoke["shapley"]["asymmetric_credit"],
                               os.path.join(out, "impl_shapley_attribution.png"))
    reports = {}
    for t in ("smoke", "scale"):
        with open(os.path.join(res_dir, f"sweep_{t}.json"), encoding="utf-8") as f:
            reports[t] = json.load(f)
    plot_sweep(plt, reports, os.path.join(out, "impl_sweep_coalition_gap.png"))
    print(f"wrote 3 plots from saved results to {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None, choices=["smoke", "scale"],
                    help="(legacy) simulate a sample game/position and plot into plots/")
    ap.add_argument("--sweep", default=None, choices=["smoke", "scale", "both"],
                    help="plot the coalition-emergence sweep from results/sweep_<tier>.json instead")
    args = ap.parse_args()

    if args.config is None and args.sweep is None:
        # default: the chapter figures, from saved results only (safe for the BG figure renderer)
        plot_from_saved_results()
        return

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
