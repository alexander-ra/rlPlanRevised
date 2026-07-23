"""
matrix_games_playground.py -- the four canonical 2x2 games under INDEPENDENT learners.

WHAT IT DOES
------------
Runs two independent gradient learners (naive policy gradient / IGA) on Prisoner's Dilemma,
Matching Pennies, Stag Hunt, and Battle of the Sexes, and prints, for each: the final action
probabilities, the final expected payoffs, and whether the run converged or is still moving.
This is the raw step's Day-1 baseline (L362-378): establish WHAT converges, what cycles, and
what fails BEFORE adding any coordination machinery.

HOW TO PLAY WITH IT (edit CONFIG below)
---------------------------------------
  steps  : more steps -> clearer convergence / clearer cycling.
  lr     : bigger learning rate -> faster, but Matching Pennies orbits grow.
  init   : (p, q) initial action-0 probabilities. Stag Hunt & BoS are init-SENSITIVE --
           try (0.9, 0.9) vs (0.1, 0.1) and watch the equilibrium you land in change.

WHAT TO WATCH OUT FOR
---------------------
- These are EXACT-gradient learners, not sampled PPO. That is deliberate: it removes noise so
  the dynamics (converge vs orbit) are unambiguous. Sampled learners show the same qualitative
  behavior with more jitter.
- "Converged" here means the last 100 steps barely moved. Matching Pennies will report NOT
  converged no matter how long you run -- that IS the result, not a bug.

HOW TO READ THE RESULTS (PREDICTIONS -- verify by running)
----------------------------------------------------------
- Prisoner's Dilemma -> both Cooperate-probabilities collapse to ~0 (mutual defection).
- Matching Pennies   -> (p, q) orbits (0.5, 0.5); never settles.
- Stag Hunt          -> converges to (Stag,Stag) OR (Hare,Hare) depending on init.
- Battle of the Sexes-> locks onto one of the two pure equilibria (init-dependent).

RUNTIME: < 1 second (pure numpy, no plotting unless SAVE_PLOT).
"""

from __future__ import annotations

import numpy as np

from _marl_tools import GAMES, expected_payoffs, game_matrices, run_independent_learners, \
    save_json, get_plt

CONFIG = {
    "steps": 4000,
    "lr": 0.1,
    "init": (0.5, 0.5),
    "seed": 0,
    "save_plot": True,
}


def _converged(ps, qs, window: int = 100, tol: float = 1e-3) -> bool:
    return bool(ps[-window:].std() < tol and qs[-window:].std() < tol)


def main():
    cfg = CONFIG
    print("Matrix games under INDEPENDENT gradient learners")
    print("=" * 78)
    results = {}
    for name, meta in GAMES.items():
        A, B = game_matrices(name)
        ps, qs = run_independent_learners(name, cfg["steps"], cfg["lr"], cfg["init"], cfg["seed"])
        p, q = float(ps[-1]), float(qs[-1])
        rr, rc = expected_payoffs(A, B, p, q)
        conv = _converged(ps, qs)
        a0, a1 = meta["actions"]
        print(f"\n[{name}]  actions = ({a0}, {a1})")
        print(f"  Nash (analytic): {meta['nash']}")
        print(f"  PREDICT        : {meta['predict']}")
        print(f"  final P(row={a0}) = {p:.3f}   P(col={a0}) = {q:.3f}")
        print(f"  final payoffs  : row = {rr:+.3f}   col = {rc:+.3f}")
        print(f"  converged?     : {conv}   (Matching Pennies should say False)")
        results[name] = {"p_final": p, "q_final": q, "row_payoff": rr, "col_payoff": rc,
                         "converged": conv}

    path = save_json("matrix_games_playground.json", {"config": _cfg_json(cfg), "results": results})
    print(f"\nsaved {path}")

    if cfg["save_plot"]:
        _plot(cfg)


def _cfg_json(cfg):
    out = dict(cfg)
    out["init"] = list(cfg["init"])
    return out


def _plot(cfg):
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG (JSON still written).")
        return
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, (name, meta) in zip(axes.flat, GAMES.items()):
        ps, qs = run_independent_learners(name, cfg["steps"], cfg["lr"], cfg["init"], cfg["seed"])
        ax.plot(ps, qs, lw=0.8)
        ax.plot(ps[0], qs[0], "go", label="start")
        ax.plot(ps[-1], qs[-1], "rs", label="end")
        ax.set_title(name)
        ax.set_xlabel(f"P(row={meta['actions'][0]})")
        ax.set_ylabel(f"P(col={meta['actions'][0]})")
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        ax.legend(fontsize=7)
    fig.suptitle("Independent learners in 2x2 games (strategy-space trajectories)")
    fig.tight_layout()
    from _marl_tools import figures_dir
    import os
    out = os.path.join(figures_dir(), "matrix_games_playground.png")
    fig.savefig(out, dpi=120)
    print(f"[plot] wrote {out}")


if __name__ == "__main__":
    np.random.seed(CONFIG["seed"])
    main()
