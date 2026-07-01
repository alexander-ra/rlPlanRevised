"""
Cross-validation against OpenSpiel (raw step Validation, step_07 line 465: BR/exploitability
must match OpenSpiel to within 0.001 on Kuhn, 0.01 on Leduc).

The clean, mapping-free check
-----------------------------
In a two-player zero-sum game, v_0 + v_1 = 0 for any profile, so NashConv -- the sum of how
much each player could gain by best-responding -- equals (br0 + br1), which is exactly what
our `nash_gap(...)['nash_conv']` returns. That means we can compare our number to
OpenSpiel's `nash_conv` for the SAME policy with no info-state-string mapping at all. We use
the uniform-random policy (trivially representable in both libraries) as the cross-check
strategy. If our best-response engine is correct, the two NashConv values match to within
the raw step's tolerance.

A second, optional check (mapping our trained Nash into an OpenSpiel TabularPolicy) is
sketched at the bottom but left as a clearly-marked TODO -- it depends on OpenSpiel's exact
information_state_string format, which must be confirmed on your machine.

GUARDED: if OpenSpiel is not installed, this prints a SKIP message and exits cleanly.
NOTE (per implementation/WORKFLOW.md): written but NOT executed by the agent.
"""

from __future__ import annotations

from engines import make_game
from policies import uniform_policy
from best_response import nash_gap

# OpenSpiel action order for these games matches our engines by construction
# (see step03/cfr/leduc_poker.py header: "matches OpenSpiel leduc_poker exactly").
_OPENSPIEL_GAME = {"kuhn": "kuhn_poker", "leduc": "leduc_poker"}
_TOL = {"kuhn": 0.001, "leduc": 0.01}


def cross_check_nashconv_uniform():
    try:
        import pyspiel
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


# --- optional, UNVERIFIED: compare exploitability of our trained Nash ----------------
def sketch_compare_trained_nash():
    """TODO (verify the info-state mapping before trusting this).

    Plan:
      1. Train our Nash table (nash.solve_nash_cached) for the game.
      2. Build an OpenSpiel TabularPolicy and, for each OpenSpiel info state, set the action
         probabilities from our table -- this requires mapping OpenSpiel's
         information_state_string to our info_set key. The two formats are NOT identical, so
         confirm the mapping by printing a handful of OpenSpiel info states first.
      3. Compare nash_conv(os_game, mapped_policy) against our nash_gap(...).
    Left as a scaffold because the mapping cannot be verified without running OpenSpiel.
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
    print("Sample OpenSpiel Kuhn information_state_string for the first decision node:")
    print(f"  {state.information_state_string()!r}")
    print("  -> confirm this format, then implement the mapping in step 2 above.")


if __name__ == "__main__":
    cross_check_nashconv_uniform()
