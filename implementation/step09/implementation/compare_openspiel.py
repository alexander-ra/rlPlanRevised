"""
Cross-validation against OpenSpiel (raw step L136-138, L482-485: OpenSpiel is the reference
PSRO / exploitability implementation).

WHAT WE CROSS-CHECK
-------------------
Step 09's PSRO convergence claim rests entirely on Step 07's EXACT best-response / NashConv
engine (the oracle AND the exploitability metric). So the load-bearing, mapping-free check is
the same one Steps 07/08 use: does our `nash_gap(...)['nash_conv']` agree with OpenSpiel's
`nash_conv` for a trivially representable policy (uniform random) on Kuhn and Leduc? If yes,
the exploitability curves PSRO reports are trustworthy.

A DIRECT check of a SOLVED PSRO meta-Nash strategy's exploitability inside OpenSpiel needs
OpenSpiel's exact information_state_string format -> a verified info-set mapping, left as a
clearly-marked TODO (identical situation to Steps 07/08). A Goofspiel cross-check is also
sketched but needs matching OpenSpiel's `goofspiel` parameters (points_order, num_cards,
returns_type) to our variant first.

GUARDED: prints SKIP and exits cleanly if OpenSpiel is absent.
NOTE (per implementation/WORKFLOW.md): written but NOT executed by the agent.
"""

from __future__ import annotations

import deps  # noqa: F401
from engines import make_game
from policies import uniform_policy
from best_response import nash_gap

_OPENSPIEL_GAME = {"kuhn": "kuhn_poker", "leduc": "leduc_poker"}
_TOL = {"kuhn": 0.001, "leduc": 0.01}


def cross_check_nashconv_uniform():
    try:
        import pyspiel  # noqa: F401
        from open_spiel.python.policy import UniformRandomPolicy
        from open_spiel.python.algorithms.exploitability import nash_conv
    except ImportError:
        print("[SKIP] OpenSpiel not installed. `pip install open_spiel` to enable this "
              "cross-validation. (validate.py's internal exact checks do not need it.)")
        return None

    print("OpenSpiel cross-validation: NashConv(uniform) ours vs OpenSpiel")
    print("-" * 64)
    all_ok = True
    for name in ("kuhn", "leduc"):
        game = make_game(name)
        ours = nash_gap(game, uniform_policy(), uniform_policy())["nash_conv"]
        os_game = pyspiel.load_game(_OPENSPIEL_GAME[name])
        os_value = nash_conv(os_game, UniformRandomPolicy(os_game))
        delta = abs(ours - os_value)
        ok = delta < _TOL[name]
        all_ok = all_ok and ok
        print(f"[{'OK ' if ok else 'FAIL'}] {name:6s} ours={ours:.6f} "
              f"openspiel={os_value:.6f} |delta|={delta:.6f} (tol {_TOL[name]})")
    return all_ok


def sketch_compare_psro_meta_nash():
    """TODO (verify the info-state mapping before trusting this).

    To cross-check our PSRO meta-Nash strategy's exploitability directly against OpenSpiel:
      1. Run our PSRO on Kuhn/Leduc -> a behavioral meta-Nash policy (psro.meta_nash_policies()).
      2. Build an OpenSpiel TabularPolicy and copy, per OpenSpiel info state, the action
         probabilities from our behavioral policy -- needs a verified map from OpenSpiel's
         information_state_string to our info_set key (the formats differ).
      3. Compare nash_conv(os_game, mapped_policy) to our reported exploitability.
    Left as a scaffold: the mapping cannot be confirmed without running OpenSpiel.
    """
    try:
        import pyspiel  # noqa: F401
    except ImportError:
        print("[SKIP] OpenSpiel not installed.")
        return
    os_game = pyspiel.load_game("kuhn_poker")
    state = os_game.new_initial_state()
    while state.is_chance_node():
        state.apply_action(state.legal_actions()[0])
    print("Sample OpenSpiel Kuhn information_state_string:")
    print(f"  {state.information_state_string()!r}")
    print("  -> confirm this format, then implement the mapping before trusting a direct "
          "PSRO meta-Nash exploitability comparison.")


def sketch_compare_goofspiel():
    """TODO: OpenSpiel has `goofspiel`, but its default (num_cards, points_order, returns_type,
    imp_info) must be matched to OUR variant (fixed descending point-order, win-splits-tie,
    total-points win/lose returns) before values are comparable. Left as a scaffold."""
    try:
        import pyspiel  # noqa: F401
    except ImportError:
        print("[SKIP] OpenSpiel not installed.")
        return
    print("Goofspiel cross-check is a TODO: align pyspiel.load_game('goofspiel', {...}) "
          "parameters with goofspiel.Goofspiel before comparing exact values.")


if __name__ == "__main__":
    cross_check_nashconv_uniform()
