"""
Cross-validation against OpenSpiel (raw step Validation, L536, L564: exploitability must match
OpenSpiel within 0.001 on Kuhn, 0.01 on Leduc).

WHY THIS MATTERS FOR STEP 08
----------------------------
EVERY safety number in this step -- worst-case value, exploitability, the constraint-generation
cuts -- is computed from Step 07's exact best response. If that engine is right, the safety
guarantees are trustworthy; if it is wrong, they are worthless. So the load-bearing
cross-check is: does our best-response / exploitability engine agree with OpenSpiel?

THE CLEAN, MAPPING-FREE CHECK (reused from Step 07)
---------------------------------------------------
In a 2p zero-sum game, NashConv = br0 + br1 (each player's gain from best-responding). We
compare OUR `nash_gap(...)['nash_conv']` to OpenSpiel's `nash_conv` for the SAME, trivially
representable policy (uniform random) -- no info-state-string mapping needed. If our BR engine
is correct, the two match within tolerance, and by extension so do all the worst-case / safety
computations built on it.

MAPPING A SOLVED STRATEGY INTO OPENSPIEL (to cross-check a *safe-exploitation* strategy's
exploitability directly) requires OpenSpiel's exact information_state_string format and is left
as a clearly-marked TODO, exactly as in Step 07 -- it cannot be verified without running
OpenSpiel on your machine.

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


def sketch_compare_solved_strategy():
    """TODO (verify the info-state mapping before trusting this).

    To cross-check a SOLVED safe-exploitation strategy's exploitability directly:
      1. Solve it here (e.g. ganzfried_safe_exploit) -> a behavioral table over OUR info-set keys.
      2. Build an OpenSpiel TabularPolicy and set, per OpenSpiel info state, the action
         probabilities from our table -- this needs a verified map from OpenSpiel's
         information_state_string to our info_set key (the formats are NOT identical).
      3. Compare nash_conv(os_game, mapped_policy) to our exploitability.
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
          "solved-strategy exploitability comparison.")


if __name__ == "__main__":
    cross_check_nashconv_uniform()
