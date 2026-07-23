"""
psro_population_peek.py -- PSRO as population-based training; look inside the population
(raw step 10 Day 1, L89-115).

WHAT IT DOES
------------
Reuses Step 09's exact PSRO on Leduc (double-oracle: grow a population of policies, each a best
response to the opponent's meta-Nash mixture). After running, it inspects the population:

  - how exploitability falls as the population grows;
  - how many policies are ACTIVE in the meta-Nash (weight > 1%) vs dead weight (the diversity
    problem the AlphaStar league is designed to fix);
  - how TRANSITIVE the meta-game is (Hodge transitive ratio): is Leduc's population structure a
    skill ladder or does it have rock-paper-scissors cycling?

The raw step suggests 50+ iterations; exact PSRO on Leduc is the slow one (Step 09 noted each
round is a full-tree best response per player), so the default is modest -- raise `rounds` if
you want the fuller picture and have the minutes.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Numbers are PREDICTIONS.
"""

from __future__ import annotations

import numpy as np

import _bootstrap  # noqa: F401  (step09 + step07 on sys.path)
from engines import make_game
from psro import PSRO
from meta_nash import solve_meta_nash

from _evo_tools import transitive_ratio_hodge, effective_size, save_json

CONFIG = {
    "game": "leduc",     # "kuhn" is much faster if you want many rounds
    "rounds": 10,        # raise toward 50 for the fuller population (slow on Leduc)
    "seed": 0,
    "active_threshold": 0.01,
}


def main():
    game = make_game(CONFIG["game"])
    psro = PSRO(game, oracle="exact", seed=CONFIG["seed"])
    hist = psro.iterate(rounds=CONFIG["rounds"])

    print(f"[{CONFIG['game']}] PSRO exploitability over {CONFIG['rounds']} rounds:")
    for r, e, ps in zip(hist["round"], hist["exploitability"], hist["pop_sizes"]):
        print(f"   round {r:2d}: pop={ps} exploitability={e:.4f}")

    # meta-Nash over the final population + active-policy count
    row_mix, col_mix = solve_meta_nash(psro.U)
    active0 = [i for i, w in enumerate(row_mix) if w > CONFIG["active_threshold"]]
    eff = effective_size(row_mix, CONFIG["active_threshold"])
    tr = transitive_ratio_hodge(psro.U)

    print(f"\n   final population size (seat 0) = {len(psro.pop[0])}")
    print(f"   ACTIVE policies in meta-Nash (w>1%) = {len(active0)} / {len(psro.pop[0])}  "
          f"(PREDICT: only a few carry weight -- the diversity problem)")
    print(f"   effective size (participation ratio) = {eff['participation_ratio']}")
    print(f"   meta-game transitive ratio (Hodge) = {tr:.4f}  "
          f"(PREDICT: Leduc is mostly transitive -> self-play works reasonably)")

    save_json("psro_population_peek", {
        "game": CONFIG["game"], "rounds": CONFIG["rounds"],
        "exploitability": [round(v, 5) for v in hist["exploitability"]],
        "final_pop_size": len(psro.pop[0]),
        "active_policies": len(active0),
        "effective_size": eff,
        "meta_game_transitive_ratio": round(tr, 5),
    })


if __name__ == "__main__":
    main()
