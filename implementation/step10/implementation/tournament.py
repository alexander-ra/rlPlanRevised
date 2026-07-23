"""
tournament.py -- the Step 10 experiment runner: runs the suites, prints comparison tables, and
writes results JSON (raw step 10 L467-484: "comparison table: league vs PSRO vs self-play vs
MCCFR Nash").

USAGE
    python tournament.py --config smoke      # fast, correctness-oriented (default)
    python tournament.py --config scale      # 100+ league epochs + larger everything
    python tournament.py --config smoke --only replicator spinning_top   # a subset

Writes results/<config>_results.json. The neural suites (league, self-play) SKIP cleanly if
torch is absent; the exact suites always run.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import argparse
import json
import os

import deps  # noqa: F401

from config import get_config, RESULTS_DIR
import evaluation as ev


def _print_replicator(res: dict):
    print("\n=== Replicator dynamics: evolutionary outcomes vs analytic ESS ===")
    for name, block in res.items():
        print(f"\n[{name}]  ESS: {block['ess_reference']}")
        print(f"   PREDICT: {block['prediction']}")
        for run in block["runs"]:
            tag = "converged" if run["converged"] else "ORBIT (no convergence)"
            print(f"   x0={run['x0']} -> final={run['final']}  [{tag}] "
                  f"orbit_radius={run['orbit_radius_vs_uniform']}")
        for ess in block["ess_checks"]:
            print(f"   ESS? x={ess['x']} -> is_ess={ess['is_ess']}")


def _print_spinning_top(res: dict):
    print("\n=== Spinning-top decomposition: transitive (skill) vs cyclic (RPS) ===")
    for name, block in res.items():
        line = f"[{name}] transitive_ratio(Hodge)={block['transitive_ratio_hodge']}"
        if "cyclic_ratio_hodge" in block:
            line += f" cyclic_ratio={block['cyclic_ratio_hodge']}"
        if "transitive_ratio_svd_rawstep" in block:
            line += f"  | raw-step SVD transitive_ratio={block['transitive_ratio_svd_rawstep']}"
        print("   " + line)


def _print_league(res: dict):
    print("\n=== PBT League for Leduc ===")
    if res.get("skipped"):
        print(f"   [SKIP] {res['reason']}")
        return
    tr = res["trajectory"]
    print(f"   epochs={len(tr['epoch'])}  live={res['num_live']} frozen={res['num_frozen']}")
    print(f"   min-main-exploitability: {tr['min_main_exploitability']}")
    print(f"   meta-Nash exploitability: {tr['meta_nash_exploitability']}")
    egta_rep = res["egta"]
    print(f"   FINAL meta-Nash exploitability={egta_rep['meta_nash_exploitability']} vs "
          f"best individual={egta_rep['best_individual_exploitability']} "
          f"-> meta<=best? {egta_rep['meta_nash_no_worse_than_best_individual']}")
    div = res["diversity"]
    print(f"   diversity: effective_pop={div['effective_population']} "
          f"clusters={div['clustering']['num_clusters']} "
          f"exploit_coverage={div['exploit_coverage']['fraction_covered']}")
    print(f"   league meta-game transitive_ratio={res['league_metagame_transitive_ratio']}")


def _print_baselines(res: dict, league_res: dict):
    print("\n=== Comparison on Leduc: league vs PSRO vs self-play vs CFR Nash ===")
    print(f"   PSRO ({res['psro']['rounds']} rounds):   exploitability="
          f"{res['psro']['final_exploitability']}")
    sp = res["selfplay"]
    if sp.get("skipped"):
        print(f"   self-play:               [SKIP] {sp['reason']}")
    else:
        print(f"   self-play (1 agent):     exploitability={sp['final_exploitability']}")
    print(f"   CFR Nash ({res['cfr_nash']['iters']} it): exploitability="
          f"{res['cfr_nash']['exploitability']}  (the ~0 reference)")
    if league_res and not league_res.get("skipped"):
        egta_rep = league_res["egta"]
        print(f"   LEAGUE meta-Nash:        exploitability={egta_rep['meta_nash_exploitability']} "
              f"(best individual main/exploiter={egta_rep['best_individual_exploitability']})")
    print("   PREDICT (raw L490-492): league meta-Nash <= best individual; league meta-Nash "
          "exploitability comparable to PSRO; CFR Nash ~ 0 (the floor).")


def main():
    ap = argparse.ArgumentParser(description="Step 10 population-training / evo-GT tournament.")
    ap.add_argument("--config", default="smoke", choices=["smoke", "scale"])
    ap.add_argument("--only", nargs="*", default=None,
                    choices=["replicator", "spinning_top", "league", "baselines"],
                    help="Run only these suites (default: all).")
    args = ap.parse_args()

    cfg = get_config(args.config)
    suites = args.only or ["replicator", "spinning_top", "league", "baselines"]
    results = {"config": cfg["name"], "suites": suites}

    if "replicator" in suites:
        results["replicator"] = ev.run_replicator_suite(cfg)
        _print_replicator(results["replicator"])
    if "spinning_top" in suites:
        results["spinning_top"] = ev.run_spinning_top_suite(cfg)
        _print_spinning_top(results["spinning_top"])
    if "league" in suites:
        results["league"] = ev.run_league_suite(cfg)
        _print_league(results["league"])
    if "baselines" in suites:
        results["baselines"] = ev.run_baselines_suite(cfg)
        _print_baselines(results["baselines"], results.get("league", {}))

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, f"{cfg['name']}_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
