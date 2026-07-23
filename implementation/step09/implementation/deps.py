"""
Dependency bootstrap for the Step 09 implementation.

WHAT THIS DOES
--------------
Step 09 is built ON TOP OF Step 07's validated modules -- it does not re-implement the game
engines, exact best response, CFR Nash, or the policy currency. This module puts Step 07's
`implementation/` folder on `sys.path` so plain imports resolve:

    import deps  # noqa: F401  (side effect: extends sys.path)
    from engines import make_game
    from best_response import best_response_value, best_response_policy, nash_gap, exact_value
    from nash import solve_nash_cached
    from policies import tabular_policy, uniform_policy, play_hand, blend_policies

WHY WE *APPEND* (not insert) STEP 07 TO sys.path
------------------------------------------------
Step 09 ships some modules with the SAME NAME as Step 07 (`config.py`, `tournament.py`,
`plotting.py`, `compare_openspiel.py`, `validate.py`). When you run a Step 09 script, Python
puts that script's own directory (step09/implementation) at `sys.path[0]`, so Step 09's own
copies always win for those names. We APPEND Step 07's directory so it is only consulted for
names Step 09 does NOT define (engines, best_response, nash, policies). None of the Step 07
modules we import pull in Step 07's config/tournament/plotting, so there is no cross-wiring.
(Step 07's engines.py itself loads the step02/step03 engines via importlib under unique
names, which avoids the deeper `cfr` namespace-package clash -- we inherit that for free.)

Run Step 09 scripts from `implementation/step09/implementation/`.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# step09/implementation -> step09 -> implementation/
_IMPL_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
STEP07_IMPL = os.path.join(_IMPL_ROOT, "step07", "implementation")

if not os.path.isdir(STEP07_IMPL):
    raise RuntimeError(
        f"Could not find Step 07's implementation at {STEP07_IMPL!r}. Step 09 reuses Step 07's "
        "engines / best_response / nash / policies as the PSRO oracle and the validation "
        "ground truth. Run from a checkout that still contains step07/implementation/."
    )

# APPEND (see module docstring): Step 09's own same-named modules must shadow Step 07's.
if STEP07_IMPL not in sys.path:
    sys.path.append(STEP07_IMPL)
