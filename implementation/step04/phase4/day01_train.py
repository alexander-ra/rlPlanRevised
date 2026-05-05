"""Day 1 — train CFR on the full Leduc engine and on the rank-canonical
engine, and report info-set counts + wall-clock per iteration.

Usage:

    python implementation/step04/phase4/day01_train.py [--iterations N]

Outputs:
    phase4/.day01_results.json — info-set counts, wall clocks,
    exploitabilities (when budget permits).
"""

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import ALL_DEALS, LeducState
from leduc_rank_engine import CANONICAL_DEALS, LeducRankState
from cfr_trainer import train_cfr
from exploitability import exploitability_full_game, exploitability_via_proxy
from day01_suit_isomorphism import verify_suit_isomorphism

RESULTS_PATH = os.path.join(_HERE, ".day01_results.json")


def _full_to_rank_translator(full_key: str) -> str:
    """Translate a full-game info-set key into the rank-canonical key.

    Full-game keys have the form
        round 0:  "<card_id>|<history>"
        round 1:  "<card_id>:<community_card_id>|<history>"
    Rank-canonical keys replace card ids by `card_id // 2`.
    """
    sep = "|"
    head, _, tail = full_key.partition(sep)
    if ":" in head:
        priv, _, comm = head.partition(":")
        head = f"{int(priv) // 2}:{int(comm) // 2}"
    else:
        head = str(int(head) // 2)
    return head + sep + tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=200,
                    help="CFR iterations (default 200; smoke-test budget)")
    ap.add_argument("--skip-exploit", action="store_true",
                    help="skip the BR-based exploitability scoring")
    args = ap.parse_args()

    print("=== Day 1 — lossless suit-isomorphic abstraction on Leduc ===\n")

    print("[1/3] Sanity probe — Definition 3.2 condition (3) on Leduc")
    pairs, viol = verify_suit_isomorphism()
    print(f"      pairs checked: {pairs}, violations: {viol}\n")

    print(f"[2/3] CFR on full 6-card engine ({len(ALL_DEALS)} deals)")
    full_result = train_cfr(
        state_factory=LeducState,
        deals_iterable=ALL_DEALS,
        num_iterations=args.iterations,
        progress_every=max(args.iterations // 5, 1),
    )
    print(f"      info sets: {len(full_result['node_map'])}")
    print(f"      wall clock: {full_result['wall_clock_seconds']:.2f}s\n")

    print(f"[3/3] CFR on rank-canonical engine ({len(CANONICAL_DEALS)} canonical deals)")
    rank_result = train_cfr(
        state_factory=LeducRankState,
        deals_iterable=CANONICAL_DEALS,
        num_iterations=args.iterations,
        progress_every=max(args.iterations // 5, 1),
    )
    print(f"      info sets: {len(rank_result['node_map'])}")
    print(f"      wall clock: {rank_result['wall_clock_seconds']:.2f}s\n")

    speedup = full_result["wall_clock_seconds"] / max(
        rank_result["wall_clock_seconds"], 1e-9)
    print(f"Wall-clock speedup (rank/full): {speedup:.2f}x")

    out = {
        "iterations": args.iterations,
        "full_engine": {
            "info_sets": len(full_result["node_map"]),
            "wall_clock_s": full_result["wall_clock_seconds"],
        },
        "rank_engine": {
            "info_sets": len(rank_result["node_map"]),
            "wall_clock_s": rank_result["wall_clock_seconds"],
        },
        "wall_clock_speedup": speedup,
        "suit_isomorphism_check": {
            "pairs_checked": pairs,
            "violations": viol,
        },
    }

    if not args.skip_exploit:
        print("\nScoring exploitability in the full 6-card game...")
        exp_full = exploitability_full_game(full_result["node_map"])
        exp_rank = exploitability_via_proxy(
            rank_result["node_map"], _full_to_rank_translator)
        print(f"  full-engine strategy:  exploitability = {exp_full:.5f}")
        print(f"  rank-engine strategy:  exploitability = {exp_rank:.5f}")
        out["exploitability_full"] = exp_full
        out["exploitability_rank"] = exp_rank

    with open(RESULTS_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
