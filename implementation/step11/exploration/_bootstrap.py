"""
_bootstrap.py -- put Step 11's own `implementation/` folder on `sys.path` so the exploration
scripts can import the SHARED SLS engine (`sls_game`) and endgame oracle (`sls_endgame`) instead
of re-implementing the rules (WORKFLOW S6: reuse, don't reinvent).

Import it FIRST in any exploration script that touches SLS:

    import _bootstrap  # noqa: F401
    from sls_game import SLSGame, play_game

The two toy-game scripts (`shapley_playground.py`) are pure numpy and need no bootstrap.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# step11/exploration -> step11 -> step11/implementation
STEP11_IMPL = os.path.abspath(os.path.join(_HERE, "..", "implementation"))

if not os.path.isdir(STEP11_IMPL):
    raise RuntimeError(f"Could not find Step 11's implementation at {STEP11_IMPL!r}.")

if STEP11_IMPL not in sys.path:
    sys.path.insert(0, STEP11_IMPL)
