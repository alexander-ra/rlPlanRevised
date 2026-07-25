"""
_bootstrap.py -- path shim for the Step 12 exploration scripts.

Exploration lives one folder up from the implementation. Importing this module puts the Step 12
`implementation/` directory on sys.path, which in turn imports `deps` there and chains the prior
steps (step02 / step07 / step09) onto the path. So an exploration script only needs:

    import _bootstrap  # noqa: F401

and can then `from decision_transformer import ...`, `from trajectory_dataset import ...`, etc.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_IMPL = os.path.abspath(os.path.join(_HERE, "..", "implementation"))
if _IMPL not in sys.path:
    sys.path.insert(0, _IMPL)

import deps  # noqa: E402,F401  (adds step02/step07/step09 and exposes torch guards)
