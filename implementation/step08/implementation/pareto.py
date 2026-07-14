"""
pareto.py -- the exploitation-safety Pareto frontier per method (raw step L397, L552).

For a representative exploitee, this assembles the frontier data that shows WHY the LP solvers
beat the naive blend:
  - the canonical RNR curve (a real frontier: points swept over p),
  - the naive Nash/BR blend curve (dominated),
  - single points for Ganzfried, prime-safe, and adaptation (each a constrained-optimum).

Axes: X = exploitation profit (EV vs the exploitee), Y = exploitability (game value minus
worst-case; >= 0). "Good" is high profit / low exploitability. The Ganzfried / prime-safe /
adaptation points should sit ON or ABOVE the canonical RNR curve, and the whole thing should
dominate the naive blend.

Writes results/pareto_<game>.json and (if matplotlib present) a plot via plotting.py.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import json

import deps  # noqa: F401
from engines import make_game
from nash import solve_nash_cached
from opponent_types import make_type_zoo

from seq_form import HeroTreeplex
from safety_checker import game_value, worst_case_value
from exploitation_metrics import exploitation_value
from rnr_solver import rnr_sweep
from ganzfried_solver import ganzfried_safe_exploit
from prime_safe import prime_safe_exploit, make_epsilon_equilibrium
from adaptation_safety import adaptation_safe_exploit
import config as cfgmod

# The most-exploitable representative type per game (clearest frontier).
_EXPLOITEE = {"kuhn": "TightPassive", "leduc": "Rock"}


def _point(game, hero, res, v):
    return {"exploitation_value": res["exploitation_value"],
            "worst_case_value": res["worst_case_value"],
            "exploitability": v - res["worst_case_value"]}


def build_pareto(game, hero, opp_model, nash_policy, blueprint_policy, nash_value,
                 rnr_ps, treeplex=None) -> dict:
    tp = treeplex if treeplex is not None else HeroTreeplex(game, hero)
    sweep = rnr_sweep(game, hero, opp_model, nash_policy, ps=rnr_ps, include_naive=True)

    ganz = ganzfried_safe_exploit(game, hero, opp_model, nash_value, treeplex=tp)
    prime = prime_safe_exploit(game, hero, opp_model, blueprint_policy, nash_value, treeplex=tp)
    adapt = adaptation_safe_exploit(game, hero, opp_model, blueprint_policy, treeplex=tp)

    return {
        "game": game.name, "hero": hero, "game_value": nash_value,
        "rnr_canonical": sweep["canonical"],
        "rnr_naive": sweep["naive"],
        "points": {
            "ganzfried": _point(game, hero, ganz, nash_value),
            "prime_safe": _point(game, hero, prime, nash_value),
            "adaptation": _point(game, hero, adapt, nash_value),
        },
        "epsilon_baseline": nash_value - worst_case_value(game, blueprint_policy, hero),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Step 08 exploitation-safety Pareto frontier")
    parser.add_argument("--config", default="smoke", choices=list(cfgmod.CONFIGS))
    parser.add_argument("--game", default=None)
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()

    cfg = cfgmod.get_config(args.config)
    games = [args.game] if args.game else cfg["games"]
    os.makedirs(cfgmod.RESULTS_DIR, exist_ok=True)

    all_results = {}
    for game_name in games:
        game = make_game(game_name)
        hero = cfg["hero"]
        nash, _ = solve_nash_cached(game, cfg["nash_iters"][game_name])
        zoo = make_type_zoo(game, nash_iters=cfg["nash_iters"][game_name])
        opp = zoo[_EXPLOITEE[game_name]]
        v = game_value(game, nash, hero)
        blueprint = make_epsilon_equilibrium(game, cfg["epsilon_baseline_iters"][game_name])

        print(f"=== {game_name.upper()} Pareto vs {_EXPLOITEE[game_name]} "
              f"(game value {v:+.4f}) ===", flush=True)
        data = build_pareto(game, hero, opp, nash, blueprint, v, cfg["rnr_ps"])
        data["exploitee"] = _EXPLOITEE[game_name]
        all_results[game_name] = data

        print(f"{'p':>5s} {'canon EV':>10s} {'canon expl':>11s} "
              f"{'naive EV':>10s} {'naive expl':>11s}")
        for cr, nr in zip(data["rnr_canonical"], data["rnr_naive"]):
            print(f"{cr['p']:>5.1f} {cr['exploitation_value']:>10.4f} "
                  f"{cr['exploitability']:>11.4f} {nr['exploitation_value']:>10.4f} "
                  f"{nr['exploitability']:>11.4f}")
        for name, pt in data["points"].items():
            print(f"  {name:12s} EV={pt['exploitation_value']:+.4f} "
                  f"expl={pt['exploitability']:+.4f}")

        path = os.path.join(cfgmod.RESULTS_DIR, f"pareto_{game_name}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        print(f"wrote {path}")

    if cfg["plot"] and not args.no_plot:
        try:
            import plotting
            plotting.plot_pareto(all_results, cfgmod.PLOTS_DIR)
            print(f"wrote Pareto plots to {cfgmod.PLOTS_DIR}")
        except ImportError:
            print("(matplotlib not installed -> skipping plots; JSON is complete)")


if __name__ == "__main__":
    main()
