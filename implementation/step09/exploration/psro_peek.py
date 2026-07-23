"""
psro_peek.py -- watch a POPULATION + meta-Nash grow toward equilibrium (PSRO, numpy-only).

WHAT IT DOES
------------
A minimal PSRO (Policy-Space Response Oracles, raw step L259-285, L395-424) on Rock-Paper-
Scissors -- the smallest game where naive learning cycles but PSRO converges. It shows the
whole double-oracle loop with exact arithmetic and no heavy dependencies:

  1. maintain a POPULATION of pure strategies per player (start: one each),
  2. build the META-GAME payoff matrix between the populations,
  3. solve its META-NASH (fictitious play on the submatrix),
  4. train a BEST RESPONSE (here: the exact best pure action) to the opponent's meta-Nash
     mixture, and add it to the population,
  5. repeat -- and watch the meta-Nash mixture's EXPLOITABILITY (NashConv) fall to ~0.

RPS is chosen because its unique Nash is uniform (1/3, 1/3, 1/3), so you can literally read
the population "discovering" Rock, then Paper, then Scissors, and the mixture converging to
uniform. The EFG version (PSRO on Kuhn with Step 07's exact BR oracle) lives in the
implementation phase; here we keep it pure-numpy for clarity.

HOW TO PLAY WITH IT (edit CONFIG)
---------------------------------
  rounds     : how many best-response additions. RPS needs only ~3 to complete the cycle.
  fp_iters   : fictitious-play iterations for the meta-Nash solve (more -> tighter mixture).

WHAT TO WATCH OUT FOR
---------------------
- The best-response oracle is EXACT here (argmax over the full action set). With an
  approximate (RL) oracle -- as in the implementation phase on Leduc -- convergence is
  empirical, not guaranteed (raw step's OPEN question, L487-489).
- "Exploitability" is the meta-Nash mixture's NashConv in the FULL game, not the meta-game.

HOW TO READ THE RESULTS (PREDICTIONS -- verify by running)
----------------------------------------------------------
- The population grows to include Rock, Paper, Scissors.
- The meta-Nash mixture approaches (1/3, 1/3, 1/3).
- Exploitability (NashConv) falls toward ~0.

RUNTIME: < 1 second.
"""

from __future__ import annotations

import numpy as np

from _marl_tools import fictitious_play_matrix, save_json, get_plt, figures_dir

# Rock-Paper-Scissors, row-player payoff (zero-sum). Actions: 0=Rock, 1=Paper, 2=Scissors.
RPS = np.array([[0.0, -1.0, 1.0],
                [1.0, 0.0, -1.0],
                [-1.0, 1.0, 0.0]])
ACTION_NAMES = ["Rock", "Paper", "Scissors"]

CONFIG = {
    "rounds": 6,
    "fp_iters": 5000,
    "seed": 0,
    "save_plot": True,
}


def _full_mixture(population, meta_mix, n_actions):
    """Map a meta-Nash mixture over a population of pure actions to a full-action mixture."""
    x = np.zeros(n_actions)
    for action, w in zip(population, meta_mix):
        x[action] += w
    return x


def _nashconv(M, x, y):
    """NashConv of a zero-sum matrix profile (x=row mix, y=col mix)."""
    cur = float(x @ M @ y)
    row_gain = float(np.max(M @ y)) - cur       # best row deviation
    col_gain = cur - float(np.min(x @ M))       # best col deviation (col minimizes row payoff)
    return row_gain + col_gain


def main():
    cfg = CONFIG
    rng = np.random.default_rng(cfg["seed"])
    M = RPS
    n = M.shape[0]

    # start each population with one random pure strategy
    pop_row = [int(rng.integers(n))]
    pop_col = [int(rng.integers(n))]

    print("PSRO on Rock-Paper-Scissors")
    print("=" * 78)
    curve = {"round": [], "exploitability": [], "row_mixture": []}

    for rnd in range(cfg["rounds"]):
        # meta-game submatrix between the two populations
        sub = M[np.ix_(pop_row, pop_col)]
        row_mix, col_mix, _ = fictitious_play_matrix(sub, cfg["fp_iters"])

        x = _full_mixture(pop_row, row_mix, n)
        y = _full_mixture(pop_col, col_mix, n)
        expl = _nashconv(M, x, y)
        curve["round"].append(rnd)
        curve["exploitability"].append(expl)
        curve["row_mixture"].append([round(float(v), 3) for v in x])

        pr = ", ".join(f"{ACTION_NAMES[a]}={w:.2f}" for a, w in zip(pop_row, row_mix))
        print(f"\nround {rnd}: |pop_row|={len(pop_row)} |pop_col|={len(pop_col)}")
        print(f"  meta-Nash (row): {pr}")
        print(f"  full-action row mixture: " +
              ", ".join(f"{ACTION_NAMES[i]}={x[i]:.3f}" for i in range(n)))
        print(f"  exploitability (NashConv): {expl:.4f}")

        # best-response oracle: best pure action vs the opponent's meta-Nash mixture
        br_row = int(np.argmax(M @ y))          # row maximizes
        br_col = int(np.argmin(x @ M))          # col minimizes row payoff
        if br_row not in pop_row:
            pop_row.append(br_row)
        if br_col not in pop_col:
            pop_col.append(br_col)

    print("\nPREDICT: mixture -> (0.333, 0.333, 0.333) and exploitability -> ~0.")
    path = save_json("psro_peek.json", {"config": cfg, "curve": curve})
    print(f"saved {path}")

    if cfg["save_plot"]:
        _plot(curve)


def _plot(curve):
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    import os
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(curve["round"], curve["exploitability"], "-o")
    ax.set_xlabel("PSRO round (best responses added)")
    ax.set_ylabel("meta-Nash exploitability (NashConv)")
    ax.set_title("PSRO on RPS: exploitability falls as the population completes the cycle")
    ax.grid(True, alpha=0.3)
    out = os.path.join(figures_dir(), "psro_peek.png")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    print(f"[plot] wrote {out}")


if __name__ == "__main__":
    main()
