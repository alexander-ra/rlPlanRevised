"""
game_landscape.py -- see the competitive landscape: skill ladder vs rock-paper-scissors
cycles (raw step 10 Day 1, L109-114).

WHAT IT DOES
------------
Takes three payoff matrices -- pure-cyclic RPS, a pure-skill ladder, and the exact PSRO-Leduc
meta-game (reused from Step 09) -- and for each reports:

  - the Hodge TRANSITIVE RATIO (skill vs cycling);
  - the "who-beats-whom" graph and a count of 3-CYCLES (A>B>C>A), the signature of
    non-transitivity;
  - a 2D embedding from the top-2 singular vectors of the antisymmetric part (cyclic games
    show a rotational "disc"; transitive games collapse onto a line/axis).

This is the intuition behind the spinning-top: transitive games have a clear hierarchy;
cyclic games rotate and self-play chases its own tail.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

import _bootstrap  # noqa: F401  (step09 + step07 on sys.path)
from engines import make_game
from psro import PSRO

from _evo_tools import transitive_ratio_hodge, save_json, get_plt

CONFIG = {"leduc_rounds": 8, "seed": 0, "beat_tol": 1e-6}


def count_three_cycles(P, tol=1e-6):
    """Number of ordered 3-cycles i->j->k->i where each 'beats' the next (P[a,b] > tol)."""
    n = P.shape[0]
    beats = P > tol
    count = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and j != k and i != k and beats[i, j] and beats[j, k] and beats[k, i]:
                    count += 1
    return count // 3   # each cycle counted 3x (rotations)


def embed_2d(P):
    """2D coordinates from the top-2 left singular vectors of the antisymmetric part."""
    A_anti = (P - P.T) / 2.0
    U, S, _ = np.linalg.svd(A_anti)
    k = min(2, U.shape[1])
    coords = U[:, :k] * np.sqrt(S[:k] + 1e-12)
    if coords.shape[1] == 1:
        coords = np.hstack([coords, np.zeros((coords.shape[0], 1))])
    return coords


def _leduc_metagame():
    psro = PSRO(make_game("leduc"), oracle="exact", seed=CONFIG["seed"])
    psro.iterate(rounds=CONFIG["leduc_rounds"])
    return psro.U


def main():
    matrices = {
        "rock_paper_scissors": np.array([[0.0, -1.0, 1.0], [1.0, 0.0, -1.0], [-1.0, 1.0, 0.0]]),
        "skill_ladder": (np.arange(4)[:, None] - np.arange(4)[None, :]).astype(float),
        "psro_leduc_metagame": _leduc_metagame(),
    }
    plt = get_plt()
    fig = None
    if plt is not None:
        fig, axes = plt.subplots(1, len(matrices), figsize=(4.2 * len(matrices), 4))
    results = {}
    for idx, (name, P) in enumerate(matrices.items()):
        tr = transitive_ratio_hodge(P)
        cycles = count_three_cycles(P, CONFIG["beat_tol"])
        coords = embed_2d(P)
        print(f"\n[{name}]  shape={P.shape}")
        print(f"   transitive_ratio(Hodge)={tr:.4f}  3-cycles={cycles}  "
              f"(PREDICT: RPS ~0 & many cycles; skill ~1 & 0 cycles; Leduc in between)")
        results[name] = {"transitive_ratio": round(tr, 5), "three_cycles": int(cycles),
                         "size": int(P.shape[0])}
        if plt is not None:
            axes[idx].scatter(coords[:, 0], coords[:, 1], c=range(len(coords)), cmap="viridis")
            for i in range(len(coords)):
                axes[idx].annotate(str(i), (coords[i, 0], coords[i, 1]), fontsize=8)
            axes[idx].set_title(f"{name}\ntransitive={tr:.2f}, cycles={cycles}")
            axes[idx].grid(alpha=0.3)
            axes[idx].set_aspect("equal", "box")
    save_json("game_landscape", results)
    if plt is not None:
        import os
        from _evo_tools import FIGURES_DIR
        os.makedirs(FIGURES_DIR, exist_ok=True)
        path = os.path.join(FIGURES_DIR, "game_landscape.png")
        fig.tight_layout()
        fig.savefig(path, dpi=120)
        plt.close(fig)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
