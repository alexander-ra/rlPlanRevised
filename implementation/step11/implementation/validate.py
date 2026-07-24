"""
validate.py -- the PASS/FAIL harness encoding the raw step's Validation targets (L556-561). 🔴/🟢

Each check maps 1:1 to a raw-step validation item and prints PASS / FAIL / SKIP. This is the
load-bearing correctness gate the human runs after the code is written. Every threshold is a
TARGET to verify (WORKFLOW S0) -- nothing here was executed.

    1. SLS env         : 2-player endgame matches exact minimax + games terminate + zero-sum  (L557)
    2. coalition detect: planted cooperative pair is identified                                 (L558)
    3. Shapley         : glove/majority exact; symmetric->equal, asymmetric->strong pair higher (L559)
    4. coalition-aware : Shapley agents' coalition score > sparse agents' (torch; else SKIP)     (L560)
    5. spinning top    : SLS meta-game cyclic component > 50% (cyclic_ratio > transitive_ratio)  (L561)

Usage (from implementation/step11/implementation/):
    python validate.py --config smoke
    python validate.py --config smoke --no-training     # skip the (slow, torch) training check

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import argparse

from config import get_config
from evaluation import (run_env_check, run_detector_check, run_shapley_check,
                        run_training_comparison, run_egta)


def _status(ok):
    return "PASS" if ok else "FAIL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="smoke", choices=["smoke", "scale"])
    ap.add_argument("--no-training", action="store_true",
                    help="skip the slow torch training-comparison check")
    args = ap.parse_args()
    cfg = get_config(args.config)

    print(f"Step 11 validation harness  (config={args.config}; targets from raw L556-561)")
    print("=" * 78)
    results = []

    # 1. environment correctness -------------------------------------------------------
    env = run_env_check(cfg)
    ok1 = env["endgame_passed"] and env["all_terminated"] and env["all_zero_sum"]
    print(f"[1] SLS env: endgame_mismatches={env['endgame_mismatches']} "
          f"terminated={env['all_terminated']} zero_sum={env['all_zero_sum']}  -> {_status(ok1)}")
    print("    NOTE: exact vs the *engine's* minimax; the paper-theorem cross-check is on the "
          "verify-list (targetedReading/summary.md).")
    results.append(("env", ok1))

    # 2. coalition detection -----------------------------------------------------------
    det = run_detector_check(cfg)
    ok2 = det["identified_correct_pair"]
    print(f"[2] coalition detection: strongest_pair={det['strongest_pair']} "
          f"(planted {det['planted_allies']})  -> {_status(ok2)}")
    results.append(("detector", ok2))

    # 3. Shapley -----------------------------------------------------------------------
    sh = run_shapley_check(cfg)
    ok3 = (sh["glove_ok"] and sh["majority_ok"] and sh["symmetric_spread"] < 0.15
           and sh["asym_strong_dominates"])
    print(f"[3] Shapley: glove_ok={sh['glove_ok']} majority_ok={sh['majority_ok']} "
          f"sym_spread={sh['symmetric_spread']} (<0.15?) asym_strong_dominates="
          f"{sh['asym_strong_dominates']}  -> {_status(ok3)}")
    print("    NOTE: symmetric_spread is Monte-Carlo noise-sensitive; raise shapley_rollouts if "
          "borderline.")
    results.append(("shapley", ok3))

    # 4. coalition-aware training comparison -------------------------------------------
    if args.no_training:
        print("[4] coalition-aware training: SKIP (--no-training)")
    else:
        tr = run_training_comparison(cfg)
        if tr.get("skipped"):
            print(f"[4] coalition-aware training: SKIP ({tr['reason']})")
        else:
            ok4 = tr["shapley_higher_coalition"]
            print(f"[4] coalition-aware: shapley_score={tr['shapley']['mean_coalition_score']:.3f} "
                  f"> sparse_score={tr['sparse']['mean_coalition_score']:.3f} ? "
                  f"-> {_status(ok4)}")
            print(f"    (win rates -- secondary, raw L560: shapley={tr['shapley']['win_rate_vs_random']} "
                  f"sparse={tr['sparse']['win_rate_vs_random']})")
            results.append(("training", ok4))

    # 5. spinning top ------------------------------------------------------------------
    # Use the COALITION pool (ally-different-partner strategies) -- the cyclicity question of
    # raw L561. The baseline pool is a skill ladder by construction, so it cannot answer it.
    egta = run_egta(cfg, pool_name="coalition")
    ok5 = egta["cyclic_dominates"]
    print(f"[5] spinning top (coalition pool): transitive={egta['transitive_ratio']} "
          f"cyclic={egta['cyclic_ratio']} cyclic>50%? {ok5}  -> {_status(ok5)}")
    print(f"    meta-Nash mixture={egta['meta_nash_mixture']} num_active={egta['num_active']}")
    results.append(("spinning_top", ok5))

    # summary --------------------------------------------------------------------------
    n_pass = sum(1 for _, ok in results if ok)
    print("=" * 78)
    print(f"SUMMARY: {n_pass}/{len(results)} PASS  ->  "
          + "  ".join(f"{name}:{_status(ok)}" for name, ok in results))
    print("(All thresholds are targets to verify -- WORKFLOW S0. A FAIL may be a real finding; "
          "follow WORKFLOW S0.1 before concluding the prediction was simply wrong.)")


if __name__ == "__main__":
    main()
