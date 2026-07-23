"""
tournament.py -- the Step 09 experiment runner: runs every suite, prints comparison tables,
and writes results JSON (raw step L432-441, "comparison table across all games").

USAGE
    python tournament.py --config smoke      # fast, correctness-oriented (default)
    python tournament.py --config scale      # adds Leduc PSRO + larger coop training
    python tournament.py --config smoke --only matrix psro lola   # subset of suites

Writes results/<config>_results.json. Neural suites SKIP cleanly if torch is absent.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import argparse
import json
import os

import deps  # noqa: F401

from config import get_config, RESULTS_DIR
import evaluation as ev


def _print_matrix(res: dict):
    print("\n=== Matrix games: independent-learner outcomes vs analytic Nash ===")
    for name, block in res.items():
        print(f"\n[{name}]  zero_sum={block['zero_sum']}")
        print(f"   analytic: {block['nash_reference']}")
        for run in block["runs"]:
            print(f"   seed {run['seed']}: x={run['x']} y={run['y']} "
                  f"NashConv={run['nashconv']:.4f} -> {run['classification']}")


def _print_psro(res: dict):
    print("\n=== PSRO: meta-Nash exploitability vs population size ===")
    for key in ("kuhn", "leduc"):
        if key not in res:
            continue
        h = res[key]
        last = h["exploitability"][-1]
        print(f"\n[{key}] rounds={len(h['round'])}  final exploitability={last:.5f}")
        for r, e, ps in zip(h["round"], h["exploitability"], h["pop_sizes"]):
            print(f"   round {r:2d}: pop={ps} exploitability={e:.5f}")
    if "matrix" in res:
        h = res["matrix"]
        print(f"\n[matrix:{h['game']}] final exploitability={h['exploitability'][-1]:.5f}")
        for r, e in zip(h["round"], h["exploitability"]):
            print(f"   round {r:2d}: exploitability={e:.5f}")
    if "goofspiel" in res:
        h = res["goofspiel"]
        print(f"\n[goofspiel K={h['num_cards']}] final exploitability={h['exploitability'][-1]:.5f}")
        for r, e in zip(h["round"], h["exploitability"]):
            print(f"   round {r:2d}: exploitability={e:.5f}")


def _print_coop(res: dict):
    print("\n=== Cooperative CTDE / communication ===")
    if res.get("skipped"):
        print(f"   [SKIP] {res['reason']}")
        return
    cv = res["critic_variance"]
    print(f"   critic variance (CoopSignal): central_final_loss={cv['central_final_loss']:.4f} "
          f"vs indep_final_loss={cv['indep_final_loss']:.4f} -> "
          f"central_lower={cv['central_lower']}")
    cr = res["climbing_reward"]
    print(f"   climbing game reward: IL={cr['independent']} MADDPG={cr['maddpg']} "
          f"MAPPO={cr['mappo']}  (optimum={cr['optimum']}, safe={cr['safe']})")
    cm = res["communication"]
    print(f"   communication: comm_ON={cm['comm_on_reward']} vs comm_OFF={cm['comm_off_reward']} "
          f"(no-comm ceiling={cm['no_comm_ceiling']}) -> comm_helps={cm['comm_helps']}")


def _print_lola(res: dict):
    print("\n=== LOLA on the Iterated Prisoner's Dilemma ===")
    print(f"   naive-vs-naive return={res['naive_return']:.3f} (expect ~1, defection)")
    print(f"   LOLA-vs-LOLA return={res['lola_return']:.3f} (expect ~3, cooperation)")
    print(f"   lola_cooperates_more={res['lola_cooperates_more']}")


def main():
    ap = argparse.ArgumentParser(description="Step 09 multi-agent RL tournament runner.")
    ap.add_argument("--config", default="smoke", choices=["smoke", "scale"])
    ap.add_argument("--only", nargs="*", default=None,
                    choices=["matrix", "psro", "coop", "lola"],
                    help="Run only these suites (default: all).")
    args = ap.parse_args()

    cfg = get_config(args.config)
    suites = args.only or ["matrix", "psro", "coop", "lola"]
    results = {"config": cfg["name"], "suites": suites}

    if "matrix" in suites:
        results["matrix"] = ev.run_matrix_suite(cfg)
        _print_matrix(results["matrix"])
    if "psro" in suites:
        results["psro"] = ev.run_psro_suite(cfg)
        _print_psro(results["psro"])
    if "coop" in suites:
        results["coop"] = ev.run_coop_suite(cfg)
        _print_coop(results["coop"])
    if "lola" in suites:
        results["lola"] = ev.run_lola(cfg)
        _print_lola(results["lola"])

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, f"{cfg['name']}_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
