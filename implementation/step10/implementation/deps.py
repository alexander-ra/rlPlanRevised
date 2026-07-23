"""
Dependency bootstrap for the Step 10 implementation.

WHAT THIS DOES
--------------
Step 10 is built ON TOP OF Step 09 (PSRO + meta-Nash + the matrix-game testbed) and Step 07
(the exact Kuhn/Leduc engines, exact best response / exploitability, CFR Nash baseline, and
the policy currency). It re-implements NONE of those. This module appends BOTH folders to
`sys.path` so plain imports resolve:

    import deps  # noqa: F401  (side effect: extends sys.path)

    # from Step 07 (the exact engine + ground truth):
    from engines import make_game
    from best_response import exact_value, best_response_policy, nash_gap
    from nash import solve_nash_cached
    from policies import tabular_policy, uniform_policy, materialize, blend_policies

    # from Step 09 (the population machinery we lift to a league):
    from meta_nash import solve_meta_nash, nashconv_matrix
    from psro import PSRO, mixture_behavioral_policy
    import matrix_games as mg09

WHY WE *APPEND* (not insert) THE PRIOR STEPS TO sys.path
--------------------------------------------------------
When you run a Step 10 script, Python puts that script's own directory
(step10/implementation) at `sys.path[0]`, so Step 10's own copies of same-named modules
(`config.py`, `tournament.py`, `plotting.py`, `evaluation.py`, `validate.py`) ALWAYS win. We
APPEND Step 09's then Step 07's directories, so they are only consulted for names Step 10
does NOT define (`psro`, `meta_nash`, `matrix_games`, `engines`, `best_response`, `nash`,
`policies`).

THE `import deps` INSIDE STEP 09's psro.py (read this before debugging import errors)
------------------------------------------------------------------------------------
Step 09's `psro.py` starts with `import deps`. Because Step 10's folder is `sys.path[0]`,
that line resolves to THIS module, not Step 09's `deps.py`. That is fine and intentional:
this module appends Step 07 (which psro.py needs for `best_response`/`policies`) AND Step 09
(which psro.py needs for `meta_nash`). So Step 09's PSRO gets everything it expects. If you
ever see `ModuleNotFoundError: meta_nash` or `best_response` while importing `psro`, the
cause is almost always that this bootstrap did not run first.

Run Step 10 scripts from `implementation/step10/implementation/`.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# step10/implementation -> step10 -> implementation/
_IMPL_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
STEP09_IMPL = os.path.join(_IMPL_ROOT, "step09", "implementation")
STEP07_IMPL = os.path.join(_IMPL_ROOT, "step07", "implementation")

for _label, _path in (("Step 09", STEP09_IMPL), ("Step 07", STEP07_IMPL)):
    if not os.path.isdir(_path):
        raise RuntimeError(
            f"Could not find {_label}'s implementation at {_path!r}. Step 10 reuses "
            f"{_label}'s modules (PSRO/meta-Nash from Step 09; the exact engine, best "
            "response, CFR Nash and policy currency from Step 07). Run from a checkout that "
            "still contains both step07/implementation/ and step09/implementation/."
        )

# APPEND (see module docstring): Step 10's own same-named modules must shadow the prior steps'.
# Order: Step 09 first, then Step 07 (Step 09 imports Step 07 names, but the resolution order
# only matters for names that collide -- and none of the reused names collide between 07/09).
for _path in (STEP09_IMPL, STEP07_IMPL):
    if _path not in sys.path:
        sys.path.append(_path)
