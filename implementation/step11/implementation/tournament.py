"""
tournament.py -- the runnable entry point: run the evaluation suites for a config, print the
raw-step comparison table (L533-538), and write `results/<config>_results.json`. 🟢

Usage (from implementation/step11/implementation/):
    python tournament.py --config smoke
    python tournament.py --config scale
    python tournament.py --config smoke --only env detector shapley egta   # skip training
    python tournament.py --config smoke --no-torch                         # force baseline-only

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Numbers are predictions.
"""

from __future__ import annotations

import argparse
import json
import os

from config import get_config
from evaluation import (run_env_check, run_detector_check, run_shapley_check,
                        run_training_comparison, run_egta)

ALL_SUITES = ["env", "detector", "shapley", "training", "egta"]


def _print_comparison_table(results: dict):
    """The raw-step comparison table (L533-538): Method | Win Rate vs Random | Coalition Score."""
    print("\n=== Comparison (raw L533-538) -- PREDICTIONS to verify ===")
    print(f"  {'Method':28s} {'WinRate vs Random':>18s} {'Coalition Score':>16s}")
    print("  " + "-" * 64)
    # random baseline is symmetric -> ~1/N win rate, ~0 coalition structure
    rows = [("Random baseline", 0.25, 0.0)]
    tr = results.get("training", {})
    if tr and not tr.get("skipped"):
        rows.append(("MAPPO (sparse reward)", tr["sparse"]["win_rate_vs_random"],
                     tr["sparse"]["mean_coalition_score"]))
        rows.append(("MAPPO + Shapley (this step)", tr["shapley"]["win_rate_vs_random"],
                     tr["shapley"]["mean_coalition_score"]))
    for name, wr, cs in rows:
        print(f"  {name:28s} {wr:18.3f} {cs:16.3f}")
    if tr and not tr.get("skipped"):
        print(f"  -> Shapley coalition score > sparse? {tr['shapley_higher_coalition']} "
              f"(raw L560 target: True)")
    else:
        print("  (training suite skipped -- torch absent; run with torch for the MAPPO rows)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="smoke", choices=["smoke", "scale"])
    ap.add_argument("--only", nargs="*", default=None, choices=ALL_SUITES,
                    help="run only these suites (default: all)")
    ap.add_argument("--no-torch", action="store_true", help="skip the training suite")
    args = ap.parse_args()

    cfg = get_config(args.config)
    suites = args.only or ALL_SUITES
    results = {"config": args.config, "config_values": cfg}

    if "env" in suites:
        print("[env] 2-player endgame + termination + zero-sum ...")
        results["env"] = run_env_check(cfg)
        print("   ", results["env"])
    if "detector" in suites:
        print("[detector] coalition detection on a planted cooperative log ...")
        results["detector"] = run_detector_check(cfg)
        print("   identified correct pair?", results["detector"]["identified_correct_pair"])
    if "shapley" in suites:
        print("[shapley] exact reference games + symmetric/asymmetric SLS credit ...")
        results["shapley"] = run_shapley_check(cfg)
        print("    glove_ok", results["shapley"]["glove_ok"], "majority_ok",
              results["shapley"]["majority_ok"], "asym_strong_dominates",
              results["shapley"]["asym_strong_dominates"])

    if "training" in suites and not args.no_torch:
        print("[training] coalition-aware (Shapley) vs sparse MAPPO ... (needs torch; may be slow)")
        results["training"] = run_training_comparison(cfg)
        if results["training"].get("skipped"):
            print("    SKIPPED:", results["training"]["reason"])
    elif "training" in suites:
        results["training"] = {"skipped": True, "reason": "--no-torch"}

    if "egta" in suites:
        print("[egta] projected pairwise meta-game + spinning top + meta-Nash ...")
        # EGTA runs on the torch-free baseline pool so the spinning-top check needs no training.
        results["egta"] = run_egta(cfg)
        print(f"    transitive_ratio={results['egta']['transitive_ratio']} "
              f"cyclic_ratio={results['egta']['cyclic_ratio']} "
              f"cyclic_dominates={results['egta']['cyclic_dominates']}")

    _print_comparison_table(results)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{args.config}_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
