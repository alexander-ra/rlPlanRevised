"""
plot_results.py -- redraw the Part I figures from the SAVED JSON (no experiment is rerun).

WHAT IT DOES
------------
Reads the artifacts the exploration scripts wrote under `figures/*.json` and draws their PNGs
at print size (7 in wide or less, 10 pt text, 300 dpi):

  matrix_games_playground.png  <- figures/matrix_games_playground.json (config)
  nonstationarity_demo.png     <- figures/nonstationarity_demo.json    (config)
  selfplay_vs_nash.png         <- figures/selfplay_vs_nash.json        (curve)
  lola_ipd_playground.png      <- figures/lola_ipd_playground.json     (histories)
  psro_peek.png                <- figures/psro_peek.json               (curve)

The two matrix-game figures need the (p, q) TRAJECTORY, which the JSON does not store. The
exact-gradient IGA dynamics are deterministic, so the trajectory is recomputed from the saved
config with `run_independent_learners` (pure numpy, < 1 s). Nothing is written but the PNGs --
no JSON is touched. The experiment scripts call these functions for their own plots, so a
rerun and a redraw give the same figure.

    python plot_results.py
"""

from __future__ import annotations

import json
import os

from _marl_tools import GAMES, figures_dir, get_plt, run_independent_learners

FS = 10          # every text element prints at >= 10 pt at 7 in wide
DPI = 300

GAME_TITLES = {
    "prisoners_dilemma": "Prisoner's Dilemma",
    "matching_pennies": "Matching Pennies",
    "stag_hunt": "Stag Hunt",
    "battle_of_the_sexes": "Battle of the Sexes",
}
# Matching Pennies started at the mixed Nash itself does not move visibly, so its panel starts
# off-centre -- the same start nonstationarity_demo.py uses.
MP_PANEL_INIT = (0.7, 0.3)


def _load(name: str) -> dict:
    with open(os.path.join(figures_dir(), name), encoding="utf-8") as fh:
        return json.load(fh)


def _style(plt):
    plt.rcParams.update({"font.size": FS, "axes.titlesize": FS + 0.5,
                         "axes.labelsize": FS, "xtick.labelsize": FS,
                         "ytick.labelsize": FS, "legend.fontsize": FS})


def _save(fig, stem: str) -> None:
    out = os.path.join(figures_dir(), f"{stem}.png")
    fig.savefig(out, dpi=DPI, bbox_inches="tight", pad_inches=0.05)
    print(f"[plot] wrote {out}")


def plot_matrix_games(cfg: dict) -> None:
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    _style(plt)
    fig, axes = plt.subplots(2, 2, figsize=(7, 6.2))
    handles = None
    for ax, (name, meta) in zip(axes.flat, GAMES.items()):
        init = MP_PANEL_INIT if name == "matching_pennies" else tuple(cfg["init"])
        ps, qs = run_independent_learners(name, cfg["steps"], cfg["lr"], init, cfg["seed"])
        ax.plot(ps, qs, lw=0.9)
        h_start, = ax.plot(ps[0], qs[0], "go", ms=6, label="start")
        h_end, = ax.plot(ps[-1], qs[-1], "rs", ms=6, label="end")
        handles = [h_start, h_end]
        title = GAME_TITLES[name]
        if name == "matching_pennies":
            title = "Matching Pennies (start off-centre)"
        ax.set_title(title)
        a0 = meta["actions"][0]
        ax.set_xlabel(f"P(row={a0})")
        ax.set_ylabel(f"P(col={a0})")
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        ax.set_aspect("equal")
    fig.suptitle("Independent learners in 2x2 games (strategy-space trajectories)",
                 fontsize=FS + 1)
    fig.legend(handles, [h.get_label() for h in handles], loc="lower center", ncol=2,
               frameon=False)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    _save(fig, "matrix_games_playground")
    plt.close(fig)


def plot_nonstationarity(cfg: dict) -> None:
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    _style(plt)
    ps, qs = run_independent_learners("matching_pennies", cfg["steps"], cfg["lr"],
                                      tuple(cfg["init"]), cfg["seed"])
    fig, ax = plt.subplots(figsize=(5.6, 6.0))
    ax.plot(ps, qs, lw=0.6, alpha=0.8)
    ax.plot(0.5, 0.5, "k*", ms=14, label="mixed Nash (0.5,0.5)")
    ax.plot(ps[0], qs[0], "go", ms=7, label="start")
    ax.plot(ps[-1], qs[-1], "rs", ms=7, label="end")
    ax.set_title("Matching Pennies: independent learners\nspiral outward, never converge")
    ax.set_xlabel("P(row = Heads)")
    ax.set_ylabel("P(col = Heads)")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, frameon=False,
              handletextpad=0.3, columnspacing=1.0)
    _save(fig, "nonstationarity_demo")
    plt.close(fig)


def plot_selfplay(curve: dict) -> None:
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    _style(plt)
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.plot(curve["iter"], curve["avg_nashconv"], "-o", ms=3, label="average iterate")
    ax.plot(curve["iter"], curve["last_nashconv"], "-s", ms=3, label="last iterate (pure BR)")
    ax.set_yscale("log")
    ax.set_xlabel("fictitious-play iteration")
    ax.set_ylabel("NashConv (exploitability)")
    ax.set_title("Kuhn self-play: the AVERAGE converges to Nash,\nthe last iterate does not")
    ax.legend(loc="center right")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    _save(fig, "selfplay_vs_nash")
    plt.close(fig)


def plot_lola(data: dict) -> None:
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    _style(plt)

    def mean(h):
        return [(a + b) / 2 for a, b in zip(h["v1"], h["v2"])]

    naive, lola = data["naive"]["history"], data["lola"]["history"]
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.plot(naive["step"], mean(naive), "-o", ms=3, label="naive (mean of both agents)")
    ax.plot(lola["step"], mean(lola), "-s", ms=3, label="LOLA (mean of both agents)")
    ax.axhline(3.0, ls="--", c="g", alpha=0.5, label="mutual cooperation (3)")
    ax.axhline(1.0, ls="--", c="r", alpha=0.5, label="mutual defection (1)")
    ax.set_xlabel("training step")
    ax.set_ylabel("per-step discounted return")
    ax.set_title("IPD: LOLA reaches cooperation where naive learners defect")
    ax.set_ylim(0.8, 3.2)
    ax.legend(loc="center right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _save(fig, "lola_ipd_playground")
    plt.close(fig)


def plot_psro_peek(curve: dict) -> None:
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    _style(plt)
    from matplotlib.ticker import MaxNLocator
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.plot(curve["round"], curve["exploitability"], "-o")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("PSRO round (best responses added)")
    ax.set_ylabel("meta-Nash exploitability (NashConv)")
    ax.set_title("PSRO on RPS: exploitability falls as the population completes the cycle")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _save(fig, "psro_peek")
    plt.close(fig)


def main() -> None:
    plot_matrix_games(_load("matrix_games_playground.json")["config"])
    plot_nonstationarity(_load("nonstationarity_demo.json")["config"])
    plot_selfplay(_load("selfplay_vs_nash.json")["curve"])
    plot_lola(_load("lola_ipd_playground.json"))
    plot_psro_peek(_load("psro_peek.json")["curve"])


if __name__ == "__main__":
    main()
