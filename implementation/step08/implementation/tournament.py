"""
tournament.py -- the Step 08 head-to-head (raw step Day 9-10, L517-525, L554).

Two studies per game, written to results/<game>_<config>.json:

  1. EXACT METHOD x OPPONENT TABLE. For every opponent type and every method, we solve the
     hero strategy against a PERFECT model of that type (the exact, offline case) and report
     three EXACT numbers plus timing:
        - exploitation value : EV vs that opponent (profit)
        - worst-case value   : hero's guaranteed EV (safety)
        - safety violation   : game value - worst-case (> 0 means it dips below the Nash floor)
     These are exact (full-tree), so they are the trustworthy yardstick -- no sampling noise.
     (The realized-online version, with a learned model, is `pipeline.py`.)

  2. TEACHING ATTACK. The online deception stress test from teaching_attack.py.

Run:  python tournament.py --config smoke
NOTHING HERE IS RUN BY THE AGENT. See README.md for how to interpret the output and the
expected outcomes (all framed as predictions).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import json
import time
import argparse

import deps  # noqa: F401
from engines import make_game
from nash import solve_nash_cached
from opponent_types import make_type_zoo

from safety_checker import game_value, worst_case_value
from exploitation_metrics import exploitation_value, safety_violation
from prime_safe import make_epsilon_equilibrium
from pipeline import build_hero_policy, make_ctx
from subgame_exploit_solver import whole_game, leduc_postflop
from teaching_attack import run_teaching_attack, print_summary as print_ta
import config as cfgmod


_PREDICATES = {"whole_game": whole_game, "leduc_postflop": leduc_postflop}


def method_x_opponent(game, hero, cfg, nash, zoo, ctx) -> dict:
    v = ctx["nash_value"]
    opponents = cfg["opponents"][game.name]
    methods = cfg["methods"]
    table = {}
    for opp_name in opponents:
        opp = zoo[opp_name]
        row = {}
        for method in methods:
            t0 = time.time()
            try:
                pol = build_hero_policy(method, game, hero, opp, ctx)
                elapsed = time.time() - t0
                ev = exploitation_value(game, pol, opp, hero)
                wc = worst_case_value(game, pol, hero)
                row[method] = {
                    "exploitation_value": ev,
                    "worst_case_value": wc,
                    "safety_violation": safety_violation(game, pol, hero, v),
                    "safe": wc >= v - 1e-3,
                    "solve_seconds": elapsed,
                }
            except Exception as exc:  # noqa: BLE001 - surface as a visible cell, don't abort
                row[method] = {"error": f"{type(exc).__name__}: {exc}"}
            print(f"  [{game.name}] {opp_name:16s} {method:12s} done", flush=True)
        table[opp_name] = row
    return table


def run_game(game_name, cfg) -> dict:
    game = make_game(game_name)
    hero = cfg["hero"]
    print(f"\n=== {game_name.upper()} ({cfg['name']}) | hero=P{hero} ===", flush=True)
    t0 = time.time()

    nash, _ = solve_nash_cached(game, cfg["nash_iters"][game_name])
    zoo = make_type_zoo(game, nash_iters=cfg["nash_iters"][game_name])
    v = game_value(game, nash, hero)
    blueprint = make_epsilon_equilibrium(game, cfg["epsilon_baseline_iters"][game_name])
    predicate = _PREDICATES[cfg["ses_predicate"][game_name]]
    ctx = make_ctx(game, hero, nash, blueprint, v, predicate=predicate)

    print("  [1/2] exact method x opponent table ...", flush=True)
    table = method_x_opponent(game, hero, cfg, nash, zoo, ctx)

    print("  [2/2] teaching attack ...", flush=True)
    teaching = run_teaching_attack(game, hero, cfg, zoo=zoo, ctx=ctx)

    elapsed = time.time() - t0
    _print_table(game_name, v, cfg, table)
    print_ta(teaching)
    print(f"  ({game_name} done in {elapsed:.1f}s)", flush=True)

    return {"game": game_name, "config": cfg["name"], "game_value": v,
            "elapsed_sec": elapsed, "methods": cfg["methods"],
            "table": table, "teaching_attack": teaching}


def _print_table(game_name, v, cfg, table):
    methods = cfg["methods"]
    print(f"\n  -- exact method x opponent: EV vs opp (top) / worst-case (bottom) "
          f"({game_name}, game value {v:+.4f}) --")
    header = f"  {'opponent':16s}"
    for m in methods:
        header += f" {m[:11]:>12s}"
    print(header)
    for opp_name, row in table.items():
        line_ev = f"  {opp_name:16s}"
        line_wc = f"  {'  worst-case':16s}"
        for m in methods:
            cell = row.get(m, {})
            if "error" in cell:
                line_ev += f" {'ERR':>12s}"
                line_wc += f" {'-':>12s}"
            else:
                line_ev += f" {cell['exploitation_value']:>12.4f}"
                mark = "" if cell["safe"] else "!"
                line_wc += f" {cell['worst_case_value']:>11.4f}{mark:1s}"
        print(line_ev)
        print(line_wc)
    print("  ('!' after a worst-case = below the Nash floor -> unsafe; expect only full_br)")


def main():
    parser = argparse.ArgumentParser(description="Step 08 safe-exploitation tournament")
    parser.add_argument("--config", default="smoke", choices=list(cfgmod.CONFIGS))
    parser.add_argument("--game", default=None)
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()

    cfg = cfgmod.get_config(args.config)
    games = [args.game] if args.game else cfg["games"]
    os.makedirs(cfgmod.RESULTS_DIR, exist_ok=True)

    all_results = {}
    for game_name in games:
        result = run_game(game_name, cfg)
        all_results[game_name] = result
        path = os.path.join(cfgmod.RESULTS_DIR, f"{game_name}_{cfg['name']}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print(f"  wrote {path}")

    if cfg["plot"] and not args.no_plot:
        try:
            import plotting
            plotting.plot_tournament(all_results, cfgmod.PLOTS_DIR)
            print(f"  wrote plots to {cfgmod.PLOTS_DIR}")
        except ImportError:
            print("  (matplotlib not installed -> skipping plots; results JSON is complete)")


if __name__ == "__main__":
    main()
