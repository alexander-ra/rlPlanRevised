"""Day 6 — cross-validate phase-4's full-Leduc CFR strategy against
OpenSpiel's reference solver.

Mirrors `step03/compare_openspiel.py` in spirit but is graceful when
OpenSpiel is not installed: in that case it prints an explanation and
exits cleanly. When OpenSpiel is available, it:

  1. trains OpenSpiel CFR on Leduc for a matched iteration budget,
  2. loads the day-1 phase-4 strategy (or trains it fresh if missing),
  3. computes the maximum and mean strategy-probability difference at
     matching info sets,
  4. saves a comparison report.

Outputs:
    phase4/.day06_openspiel_compare.json
"""

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import LeducState, ALL_DEALS
from cfr_trainer import train_cfr

RESULTS_PATH = os.path.join(_HERE, ".day06_openspiel_compare.json")

_ACTION_TO_CHAR = {0: "f", 1: "c", 2: "r"}


def _try_import_openspiel():
    try:
        import pyspiel  # noqa: F401
        return True
    except ImportError:
        return False


def _train_openspiel_cfr(num_iterations: int):
    """Run OpenSpiel CFR on Leduc and return the average strategy as a
    `dict[info_set_str, list[float]]`.
    """
    import pyspiel
    from open_spiel.python.algorithms import cfr

    game = pyspiel.load_game("leduc_poker")
    solver = cfr.CFRSolver(game)
    for _ in range(num_iterations):
        solver.evaluate_and_update_policy()
    avg = solver.average_policy()
    # Walk the game tree and record the policy at each info state.
    out = {}
    states = [game.new_initial_state()]
    seen = set()
    while states:
        s = states.pop()
        if s.is_terminal():
            continue
        if s.is_chance_node():
            for action, _ in s.chance_outcomes():
                states.append(s.child(action))
            continue
        info = _openspiel_info_to_phase4_key(s.information_state_string())
        if info not in seen:
            ap = avg.action_probabilities(s)
            legal = s.legal_actions()
            probs = [ap.get(a, 0.0) for a in legal]
            out[info] = (legal, probs)
            seen.add(info)
        for action in s.legal_actions():
            states.append(s.child(action))
    return out


def _field(info_state: str, name: str) -> str:
    m = re.search(rf"\[{re.escape(name)}: ([^\]]*)\]", info_state)
    if not m:
        return ""
    return m.group(1).strip()


def _actions_to_history(actions: str) -> str:
    if not actions:
        return ""
    return "".join(_ACTION_TO_CHAR[int(a)] for a in actions.split())


def _openspiel_info_to_phase4_key(info_state: str) -> str:
    """Translate OpenSpiel's verbose Leduc info-state string into the
    compact phase-4 key: `<private>|<history>` before the public card and
    `<private>:<public>|<round1>/<round2>` after the public card.
    """
    private = _field(info_state, "Private")
    public = _field(info_state, "Public")
    round1 = _actions_to_history(_field(info_state, "Round1"))
    round2 = _actions_to_history(_field(info_state, "Round2"))
    if public:
        return f"{private}:{public}|{round1}/{round2}"
    return f"{private}|{round1}"


def _our_average_strategy(node_map):
    """Convert phase-4 `node_map` into the same `(legal, probs)` form."""
    out = {}
    for info, (node, legal) in node_map.items():
        out[info] = (legal, node.get_average_strategy())
    return out


def _diff_metrics(ours: dict, theirs: dict) -> dict:
    """Maximum and mean L1 distance between the two strategies on the
    intersection of info-set keys. OpenSpiel's verbose keys are
    translated to phase-4's compact Leduc keys during extraction.
    """
    common = set(ours) & set(theirs)
    if not common:
        return {
            "common_info_sets": 0,
            "max_l1": None,
            "mean_l1": None,
        }
    deltas = []
    for k in common:
        legal_ours, probs_ours = ours[k]
        legal_theirs, probs_theirs = theirs[k]
        if legal_ours != legal_theirs:
            continue
        l1 = sum(abs(a - b) for a, b in zip(probs_ours, probs_theirs))
        deltas.append(l1)
    if not deltas:
        return {
            "common_info_sets": len(common),
            "max_l1": None,
            "mean_l1": None,
            "comment": ("info-set keys overlap but action lists differ "
                        "— translator needed."),
        }
    return {
        "common_info_sets": len(common),
        "compared_info_sets": len(deltas),
        "max_l1": max(deltas),
        "mean_l1": sum(deltas) / len(deltas),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=200)
    args = ap.parse_args()

    if not _try_import_openspiel():
        print("OpenSpiel (`pyspiel`) is not installed. Install with")
        print("    pip install open_spiel")
        print("and re-run to get a cross-validation report.")
        with open(RESULTS_PATH, "w") as f:
            json.dump({"status": "openspiel_unavailable"}, f, indent=2)
        return 0

    print(f"=== Day 6 — OpenSpiel cross-validation ({args.iterations} iters) ===\n")

    print("[1/3] Train phase-4 CFR on the full 6-card engine")
    ours_result = train_cfr(LeducState, ALL_DEALS, args.iterations)
    ours = _our_average_strategy(ours_result["node_map"])
    print(f"      info_sets={len(ours)}")

    print("[2/3] Train OpenSpiel CFR on Leduc")
    theirs = _train_openspiel_cfr(args.iterations)
    print(f"      info_sets={len(theirs)}")

    print("[3/3] Diff strategies on matching info sets")
    diff = _diff_metrics(ours, theirs)
    print(f"      common_info_sets = {diff['common_info_sets']}")
    if diff.get("max_l1") is not None:
        print(f"      max L1 distance  = {diff['max_l1']:.5f}")
        print(f"      mean L1 distance = {diff['mean_l1']:.5f}")
    elif "comment" in diff:
        print(f"      {diff['comment']}")

    out = {
        "iterations": args.iterations,
        "ours_info_sets": len(ours),
        "openspiel_info_sets": len(theirs),
        "diff": diff,
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
