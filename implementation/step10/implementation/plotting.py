"""
plotting.py -- OPTIONAL, GUARDED plots of a Step 10 results JSON.

matplotlib is optional: if it is not installed, every function prints a SKIP line and returns
without error (per WORKFLOW.md: plots are a bonus, never a dependency of the core result).

Phase portraits are re-simulated from the config (the replicator dynamics are cheap and
deterministic, so we don't bloat the results JSON with full trajectories); the league /
baseline / spinning-top plots read the results JSON.

USAGE
    python plotting.py                    # scale (default): reads results/scale_results.json,
                                          # writes plots/*.png
    python plotting.py --config smoke     # reads results/smoke_results.json

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


# Print-size typography. Every figure is drawn at (or just under) the 17.6 cm text width, so a
# font size here is the size it prints at; 10 pt matches the body text, 9.5 pt is the floor used
# for legends. The BG renderer translates every string passed to a labelling call, so labels are
# plain display text (no code identifiers).
_RC = {"font.size": 10, "axes.titlesize": 10, "axes.labelsize": 10,
       "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 9.5}
_DPI = 300

_GAME_TITLES = {
    "prisoners_dilemma": "Prisoner's Dilemma\nshare of Cooperate",
    "hawk_dove": "Hawk-Dove\nshare of Hawk",
    "rock_paper_scissors": "Rock-Paper-Scissors\nshare of Rock",
    "stag_hunt": "Stag Hunt\nshare of Stag",
}

_POPULATION_NAMES = {
    "rock_paper_scissors": "Rock-Paper-\nScissors",
    "pure_skill": "pure skill\nladder",
    "psro_leduc_metagame": "PSRO best responses\n(Leduc)",
    "league_metagame": "league snapshots\n(Leduc)",
}


def _start_label(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return f"$x_0 = {s}$"


def _num(v: float, fmt: str = "%.2f") -> str:
    """Locale-aware number (the BG renderer switches LC_NUMERIC to a decimal comma)."""
    import locale
    return locale.format_string(fmt, v)


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
    rng = np.random.default_rng(config["seed"])
    with plt.rc_context(_RC):
        fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.6), sharex=True)
        axes = axes.flatten()
        for i, (ax, name) in enumerate(zip(axes, games)):
            g = evo_games.make_evo_game(name)
            starts = rc.get("starts", {}).get(name) or [rep._normalize(rng.random(g.n) + 0.1).tolist()]
            for x0 in starts:
                xs = np.array(rep.simulate_single(g.A, x0, T=rc["T"], dt=rc["dt"]))
                ax.plot(xs[:, 0], lw=1.4, label=_start_label(x0[0]))
            ax.set_title(_GAME_TITLES.get(name, name))
            if i >= 2:
                ax.set_xlabel("replicator step")
            ax.set_ylim(-0.02, 1.02)
            ax.grid(alpha=0.3)
            ax.legend(loc="center right" if name == "stag_hunt" else "best")
        path = os.path.join(out_dir, "replicator_portraits.png")
        fig.tight_layout()
        fig.savefig(path, dpi=_DPI)
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
    with plt.rc_context(_RC):
        fig, ax = plt.subplots(figsize=(7.0, 3.9))
        bars = ax.bar(range(len(names)), ratios, color="#369", width=0.6)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels([_POPULATION_NAMES.get(n, n) for n in names])
        ax.bar_label(bars, labels=[_num(r) for r in ratios], padding=3,
                     bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
        ax.axhline(1.0, ls="--", color="green", lw=1, label="pure skill (transitive)")
        ax.axhline(0.0, ls=":", color="grey", lw=1, label="pure cycling (RPS)")
        ax.set_ylabel("transitive ratio")
        ax.set_ylim(0, 1.5)
        ax.legend(loc="upper center", ncol=1, frameon=False)
        path = os.path.join(out_dir, "transitive_ratios.png")
        fig.tight_layout()
        fig.savefig(path, dpi=_DPI)
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
    with plt.rc_context(_RC):
        fig, ax = plt.subplots(figsize=(7.0, 4.0))
        ax.plot(tr["epoch"], tr["min_main_exploitability"], lw=1.5,
                label="min exploitability of the main agents")
        ax.plot(tr["epoch"], tr["meta_nash_exploitability"], lw=1.5,
                label="meta-Nash exploitability")
        sp = (results.get("baselines") or {}).get("selfplay") or {}
        if sp.get("exploitability_trajectory"):
            traj = sp["exploitability_trajectory"]
            ax.plot(range(len(traj)), traj, ls="--", lw=1.2, color="grey",
                    label="self-play (baseline)")
        ax.set_xlabel("league epoch")
        ax.set_ylabel("exploitability (NashConv, exact)")
        ax.grid(alpha=0.3)
        ax.legend(loc="upper right")
        path = os.path.join(out_dir, "league_exploitability.png")
        fig.tight_layout()
        fig.savefig(path, dpi=_DPI)
        plt.close(fig)
    print(f"wrote {path}")


def plot_comparison(results: dict, out_dir: str):
    """Horizontal bars, lowest (best) at the top. Best-of-run values are shown next to
    best-of-run values: the league's best individual next to self-play's best iterate."""
    plt = _get_plt()
    if plt is None:
        print("[SKIP] matplotlib not installed -> no comparison plot.")
        return
    base = results.get("baselines")
    if not base:
        return
    league_c, selfplay_c, psro_c, cfr_c = "#3a6ea5", "#c0504d", "#8064a2", "#7f7f7f"
    rows = [("CFR (Nash)", base["cfr_nash"]["exploitability"], cfr_c)]
    league = results.get("league", {})
    if league and not league.get("skipped"):
        rows.append(("league – best individual",
                     league["egta"]["best_individual_exploitability"], league_c))
    sp = base["selfplay"]
    if not sp.get("skipped") and sp.get("exploitability_trajectory"):
        rows.append(("self-play – best iterate", min(sp["exploitability_trajectory"]), selfplay_c))
    rows.append(("PSRO (exact oracle)", base["psro"]["final_exploitability"], psro_c))
    if league and not league.get("skipped"):
        rows.append(("league – meta-Nash mixture",
                     league["egta"]["meta_nash_exploitability"], league_c))
    if not sp.get("skipped"):
        rows.append(("self-play – final agent", sp["final_exploitability"], selfplay_c))
    labels = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    with plt.rc_context(_RC):
        fig, ax = plt.subplots(figsize=(7.0, 3.4))
        bars = ax.barh(range(len(vals)), vals, color=[r[2] for r in rows], height=0.6)
        ax.set_yticks(range(len(vals)))
        ax.set_yticklabels(labels)
        ax.invert_yaxis()
        ax.bar_label(bars, labels=[_num(v) for v in vals], padding=3)
        ax.set_xlim(0, max(vals) * 1.15)
        ax.set_xlabel("exploitability (NashConv); lower = closer to Nash")
        ax.grid(alpha=0.3, axis="x")
        path = os.path.join(out_dir, "comparison_exploitability.png")
        fig.tight_layout()
        fig.savefig(path, dpi=_DPI)
        plt.close(fig)
    print(f"wrote {path}")


def main():
    ap = argparse.ArgumentParser(description="Plot a Step 10 tournament results JSON.")
    # scale is the configuration the deliverables cite. parse_known_args, because the BG figure
    # renderer runs this file with its own command line.
    ap.add_argument("--config", default="scale", choices=["smoke", "scale"])
    args, _ = ap.parse_known_args()

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
