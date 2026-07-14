"""
The exploitation-safety Pareto curve (raw step L117-121).

Sweeps the naive blend parameter lambda from 0 (pure best response) to 1 (pure Nash) in
0.1 steps. For each blend it computes:
  - X = exploitation profit = EV vs the (weak) exploitee
  - Y = worst-case loss     = how far worst-case EV sits below the game value (exploitability)

and plots profit (X) against worst-case loss (Y). This curve IS the picture of safe
exploitation: the "good" region is high profit / low worst-case loss (up and to the left).
The optimal operating point is the highest profit subject to a worst-case-loss budget.

IMPORTANT (read `README.md` §"what to watch out for"): the *naive blend* traces A curve, but
it is generally NOT the efficient frontier. The implementation-phase solvers (RNR, Ganzfried)
find points ABOVE this curve -- same worst-case loss, strictly more profit -- because they
choose WHERE to deviate instead of scaling every info set uniformly.

Run:  python pareto_curve.py
Outputs: a table to stdout + figures/pareto_curve_<game>.png (if matplotlib present) and
         figures/pareto_curve_<game>.json (always).
Runtime: seconds on Kuhn (11 exact evaluations).

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
    "lambdas": [i / 10.0 for i in range(11)],  # 0.0 .. 1.0 (weight on Nash)
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
    print(f"Pareto sweep  game={game.name} hero=P{hero} exploitee={exploitee_name} "
          f"(lambda = weight on Nash)")
    print(f"{'lambda':>7s} {'profit(EV vs opp)':>18s} {'worst-case loss':>16s}")
    for lam in cfg["lambdas"]:
        h = blend_policies([br, nash], [1.0 - lam, lam]) if lam not in (0.0, 1.0) else (
            br if lam == 0.0 else nash)
        profit = tools.exploitation_ev(game, h, opp, hero)
        worst_case_loss = tools.exploitability(game, h, v_star, hero)  # >= 0
        rows.append({"lambda": lam, "profit": profit, "worst_case_loss": worst_case_loss})
        print(f"{lam:>7.1f} {profit:>18.4f} {worst_case_loss:>16.4f}")

    os.makedirs(_FIG_DIR, exist_ok=True)
    json_path = os.path.join(_FIG_DIR, f"pareto_curve_{game.name}.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"game": game.name, "exploitee": exploitee_name,
                   "game_value": v_star, "rows": rows}, fh, indent=2)
    print(f"wrote {json_path}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(matplotlib not installed -> skipping PNG; JSON written)")
        return

    xs = [r["profit"] for r in rows]
    ys = [r["worst_case_loss"] for r in rows]
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.plot(xs, ys, "-o", color="tab:blue")
    for r in rows:
        ax.annotate(f"{r['lambda']:.1f}", (r["profit"], r["worst_case_loss"]),
                    fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel(f"exploitation profit (EV vs {exploitee_name})")
    ax.set_ylabel("worst-case loss (exploitability, >= 0)")
    ax.set_title(f"Naive Nash/BR blend frontier -- {game.name}\n"
                 "(labels = lambda; efficient solvers push ABOVE this)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    png_path = os.path.join(_FIG_DIR, f"pareto_curve_{game.name}.png")
    fig.savefig(png_path, dpi=130)
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main()
