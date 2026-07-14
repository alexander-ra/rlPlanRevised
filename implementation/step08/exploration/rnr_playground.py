"""
A Restricted-Nash-Response *playground* (raw step L128-142) -- the NAIVE version.

Sweeps p in {0.0, 0.1, ..., 1.0} and, at each p, plays the behavioral blend
    hero = (1 - p) * Nash  +  p * BestResponse(exploitee)
then reports, for each p:
  - exploitation profit = EV vs the exploitee
  - exploitability      = game value minus worst-case EV (>= 0)

The lesson to build here (raw step L142): deviating from Nash buys profit but also buys
exploitability, and there is a *budget* -- you can deviate a lot before exploitability grows
unacceptably, especially early in the sweep.

>>> BIG FLAG -- naive vs canonical RNR <<<
This p-blend is the raw step's Day-2 description (L128-142), and it is a fine INTUITION tool.
It is NOT Johanson's actual Restricted Nash Response. Canonical RNR computes the EQUILIBRIUM
against a "p-restricted" opponent (who is forced to play your model with prob p and plays
adversarially with prob 1-p); that is a constrained optimization, not a blend of two fixed
strategies, and it dominates this curve (more profit at the same exploitability). The
canonical solver lives in the implementation phase (`rnr_solver.py`). Both are provided there
so you can see the gap. Do not mistake this playground for the real algorithm.

Run:  python rnr_playground.py
Outputs: table to stdout + figures/rnr_playground_<game>.{png,json}.
Runtime: seconds on Kuhn.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import json

import _bootstrap  # noqa: F401
from engines import make_game
from nash import solve_nash_cached
from opponent_types import make_type_zoo
from best_response import best_response_policy
from policies import blend_policies

import _soe_tools as tools

CONFIG = {
    "game": "kuhn",
    "hero": 0,
    "exploitee": "TightPassive",   # "Rock" for leduc
    "nash_iters": {"kuhn": 30000, "leduc": 4000},
    "ps": [i / 10.0 for i in range(11)],  # 0 = pure Nash, 1 = pure BR
}

_FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")


def main():
    cfg = CONFIG
    game = make_game(cfg["game"])
    hero = cfg["hero"]
    exploitee_name = cfg["exploitee"] if cfg["game"] == "kuhn" else "Rock"
    nash, _ = solve_nash_cached(game, cfg["nash_iters"][game.name])
    zoo = make_type_zoo(game, nash_iters=cfg["nash_iters"][game.name])
    opp = zoo[exploitee_name]
    v_star = tools.game_value(game, nash, hero)
    br = best_response_policy(game, hero, opp)

    rows = []
    print(f"naive RNR p-sweep  game={game.name} hero=P{hero} exploitee={exploitee_name}")
    print(f"(p = weight on best response; 0 = Nash, 1 = full BR)")
    print(f"{'p':>5s} {'profit(EV vs opp)':>18s} {'exploitability':>15s}")
    for p in cfg["ps"]:
        if p == 0.0:
            h = nash
        elif p == 1.0:
            h = br
        else:
            h = blend_policies([br, nash], [p, 1.0 - p])
        profit = tools.exploitation_ev(game, h, opp, hero)
        expl = tools.exploitability(game, h, v_star, hero)
        rows.append({"p": p, "profit": profit, "exploitability": expl})
        print(f"{p:>5.1f} {profit:>18.4f} {expl:>15.4f}")

    os.makedirs(_FIG_DIR, exist_ok=True)
    json_path = os.path.join(_FIG_DIR, f"rnr_playground_{game.name}.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"game": game.name, "exploitee": exploitee_name,
                   "game_value": v_star, "rows": rows,
                   "note": "naive p-blend, NOT canonical RNR (see implementation/rnr_solver.py)"},
                  fh, indent=2)
    print(f"wrote {json_path}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(matplotlib not installed -> skipping PNG; JSON written)")
        return

    ps = [r["p"] for r in rows]
    fig, ax1 = plt.subplots(figsize=(6, 4.5))
    ax1.plot(ps, [r["profit"] for r in rows], "-o", color="tab:green", label="profit vs opp")
    ax1.set_xlabel("p (weight on best response)")
    ax1.set_ylabel("exploitation profit", color="tab:green")
    ax2 = ax1.twinx()
    ax2.plot(ps, [r["exploitability"] for r in rows], "-s", color="tab:red",
             label="exploitability")
    ax2.set_ylabel("exploitability (>= 0)", color="tab:red")
    ax1.set_title(f"Naive RNR sweep -- {game.name} (NOT canonical RNR)")
    ax1.grid(True, alpha=0.3)
    fig.tight_layout()
    png_path = os.path.join(_FIG_DIR, f"rnr_playground_{game.name}.png")
    fig.savefig(png_path, dpi=130)
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
