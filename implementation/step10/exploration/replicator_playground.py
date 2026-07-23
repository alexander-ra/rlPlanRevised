"""
replicator_playground.py -- watch a population of strategies EVOLVE (raw step 10 Day 2,
L117-138).

WHAT IT DOES
------------
Runs single-population replicator dynamics on the four canonical games and prints, for each,
the final population state and whether it converged. Saves phase-portrait PNGs (probability of
the first action over time) + a JSON of the outcomes.

The whole point in one screen:
  - Prisoner's Dilemma -> defection takes over (converges).
  - Hawk-Dove          -> settles at the mixed ESS p(Hawk)=0.5 (converges).
  - Rock-Paper-Scissors -> ORBITS forever, never converges (the non-transitive cycling that the
    spinning-top decomposition explains and that self-play/PBT inherit).
  - Stag Hunt          -> all-Stag or all-Hare depending on where you start (two basins).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Every number is a
PREDICTION to verify.
"""

from __future__ import annotations

import numpy as np

from _evo_tools import GAMES, simulate, converged, orbit_radius, save_json, get_plt

CONFIG = {
    "T": 6000,
    "dt": 0.01,
    "seed": 0,
    # a couple of starts per game so Stag Hunt reveals both basins
    "starts": {
        "prisoners_dilemma": [[0.5, 0.5], [0.9, 0.1]],
        "hawk_dove": [[0.2, 0.8], [0.9, 0.1]],
        "rock_paper_scissors": [[0.4, 0.35, 0.25]],
        "stag_hunt": [[0.8, 0.2], [0.2, 0.8]],
    },
}


def main():
    rng = np.random.default_rng(CONFIG["seed"])
    plt = get_plt()
    results = {}
    fig = None
    if plt is not None:
        fig, axes = plt.subplots(1, len(GAMES), figsize=(4.2 * len(GAMES), 4))
    for idx, (name, spec) in enumerate(GAMES.items()):
        A = spec["A"]
        starts = CONFIG["starts"].get(name) or [rng.random(A.shape[0])]
        runs = []
        print(f"\n[{name}]  actions={spec['actions']}")
        print(f"   PREDICT: {spec['predict']}")
        for x0 in starts:
            xs = simulate(A, x0, T=CONFIG["T"], dt=CONFIG["dt"])
            conv = converged(xs)
            uniform = np.ones(A.shape[0]) / A.shape[0]
            r = orbit_radius(xs, uniform)
            runs.append({"x0": [round(v, 3) for v in x0],
                         "final": [round(float(v), 3) for v in xs[-1]],
                         "converged": bool(conv), "orbit_radius": round(r, 4)})
            tag = "converged" if conv else "ORBIT (never converges)"
            print(f"   x0={np.round(x0,2).tolist()} -> final={np.round(xs[-1],3).tolist()} [{tag}]")
            if plt is not None:
                axes[idx].plot(xs[:, 0], lw=1.2, label=f"x0[0]={round(x0[0],2)}")
        results[name] = {"predict": spec["predict"], "runs": runs}
        if plt is not None:
            axes[idx].set_title(f"{name}\nP[{spec['actions'][0]}]")
            axes[idx].set_ylim(-0.02, 1.02)
            axes[idx].set_xlabel("replicator step")
            axes[idx].grid(alpha=0.3)
            axes[idx].legend(fontsize=7)
    save_json("replicator_playground", results)
    if plt is not None:
        import os
        from _evo_tools import FIGURES_DIR
        os.makedirs(FIGURES_DIR, exist_ok=True)
        path = os.path.join(FIGURES_DIR, "replicator_playground.png")
        fig.tight_layout()
        fig.savefig(path, dpi=120)
        plt.close(fig)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
