"""
nonstationarity_demo.py -- SEE the moving-target problem that motivates CTDE.

WHAT IT DOES
------------
Zooms in on Matching Pennies -- the cleanest illustration of non-stationarity (raw step
L118-121). Two independent learners each best-respond to the OTHER's current policy; because
the other is ALSO moving, they chase each other in a closed orbit around the 50/50 mixed Nash
and never converge. We print the orbit radius over time (it does not shrink) and, for
contrast, run the SAME learners on Prisoner's Dilemma (which DOES converge, to defection) so
you can see that "independent learning" is not always doomed -- it is doomed when the unique
equilibrium is a mixed saddle.

HOW TO PLAY WITH IT (edit CONFIG)
---------------------------------
  steps  : longer horizon -> the orbit persists (it will not close in).
  lr     : larger -> larger orbit radius (energy is injected each step).
  init   : start off-center, e.g. (0.7, 0.3), to make the first orbit obvious.

WHAT TO WATCH OUT FOR
---------------------
- The orbit does not spiral IN or OUT much under exact simultaneous gradient updates -- it is
  (approximately) energy-preserving. With alternating updates or averaging it would behave
  differently; that is the whole point of the fictitious-play / averaging trick you will see
  in `selfplay_vs_nash.py`.
- Do not read "it didn't converge" as a failure of the code. Non-convergence is the finding.

HOW TO READ THE RESULTS (PREDICTIONS -- verify by running)
----------------------------------------------------------
- Matching Pennies: mean distance from (0.5, 0.5) stays roughly CONSTANT across windows
  (an orbit), and the last iterate is far from Nash.
- Prisoner's Dilemma: distance-to-(defect,defect) shrinks to ~0 (convergence).

RUNTIME: < 1 second.
"""

from __future__ import annotations

import numpy as np

from _marl_tools import run_independent_learners, save_json, get_plt, figures_dir

CONFIG = {
    "steps": 6000,
    "lr": 0.1,
    "init": (0.7, 0.3),
    "seed": 0,
    "save_plot": True,
}


def _windowed_radius(ps, qs, center, n_windows: int = 6):
    """Mean Euclidean distance from `center` in each of n_windows time slices."""
    d = np.sqrt((ps - center[0]) ** 2 + (qs - center[1]) ** 2)
    chunks = np.array_split(d, n_windows)
    return [float(c.mean()) for c in chunks]


def main():
    cfg = CONFIG
    print("Non-stationarity: independent learners chase a moving target")
    print("=" * 78)

    ps_mp, qs_mp = run_independent_learners("matching_pennies", cfg["steps"], cfg["lr"],
                                            cfg["init"], cfg["seed"])
    rad_mp = _windowed_radius(ps_mp, qs_mp, (0.5, 0.5))
    print("\n[matching_pennies] distance from Nash (0.5,0.5) per time-window:")
    print("  " + "  ".join(f"{r:.3f}" for r in rad_mp))
    print(f"  PREDICT: roughly CONSTANT (an orbit) -> non-stationarity, no convergence.")
    print(f"  last iterate: P(row=H)={ps_mp[-1]:.3f}, P(col=H)={qs_mp[-1]:.3f}")

    ps_pd, qs_pd = run_independent_learners("prisoners_dilemma", cfg["steps"], cfg["lr"],
                                            cfg["init"], cfg["seed"])
    rad_pd = _windowed_radius(ps_pd, qs_pd, (0.0, 0.0))  # (Defect,Defect) is action-0-prob 0
    print("\n[prisoners_dilemma] distance from (Defect,Defect) per time-window:")
    print("  " + "  ".join(f"{r:.3f}" for r in rad_pd))
    print(f"  PREDICT: SHRINKS to ~0 -> independent learning DOES converge here.")

    path = save_json("nonstationarity_demo.json", {
        "config": {**cfg, "init": list(cfg["init"])},
        "matching_pennies_radius_windows": rad_mp,
        "prisoners_dilemma_radius_windows": rad_pd,
    })
    print(f"\nsaved {path}")

    if cfg["save_plot"]:
        _plot(ps_mp, qs_mp)


def _plot(ps_mp, qs_mp):
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    import os
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(ps_mp, qs_mp, lw=0.6, alpha=0.8)
    ax.plot(0.5, 0.5, "k*", ms=14, label="mixed Nash (0.5,0.5)")
    ax.plot(ps_mp[0], qs_mp[0], "go", label="start")
    ax.plot(ps_mp[-1], qs_mp[-1], "rs", label="end")
    ax.set_title("Matching Pennies: independent learners orbit, never converge")
    ax.set_xlabel("P(row = Heads)")
    ax.set_ylabel("P(col = Heads)")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.legend()
    out = os.path.join(figures_dir(), "nonstationarity_demo.png")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    print(f"[plot] wrote {out}")


if __name__ == "__main__":
    np.random.seed(CONFIG["seed"])
    main()
