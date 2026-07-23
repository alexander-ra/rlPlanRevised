"""
Path bootstrap for the Step 08 exploration scripts.

WHAT / WHY
----------
Everything the exploration needs -- the uniform game interface, exact best response and
exploitability, the CFR Nash baseline, the opponent type zoo, and the policy currency --
already exists and is validated in Step 07. We do NOT re-implement any of it. This module
puts Step 07's `implementation/` folder on `sys.path` so a plain `from engines import
make_game` resolves to Step 07's modules.

Step 07's `engines.py` in turn loads the Kuhn (step02) and Leduc (step03) engines via
importlib under unique names, which is what avoids the `cfr`-package namespace clash. By
importing Step 07's engines.py we inherit that safe loader for free.

Import this module FIRST in every exploration script:

    import _bootstrap  # noqa: F401  (side effect: extends sys.path)
    from engines import make_game
    from best_response import best_response_value, exact_value, nash_gap
    ...

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# step08/exploration -> step08 -> implementation/  (the rlPlan implementation root)
_IMPL_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
_STEP07_IMPL = os.path.join(_IMPL_ROOT, "step07", "implementation")

if not os.path.isdir(_STEP07_IMPL):
    raise RuntimeError(
        f"Could not find Step 07's implementation folder at {_STEP07_IMPL!r}. "
        "The Step 08 exploration reuses Step 07's engines/best_response/nash/opponent_types "
        "-- run these scripts from a checkout that still contains step07/implementation/."
    )

if _STEP07_IMPL not in sys.path:
    sys.path.insert(0, _STEP07_IMPL)
