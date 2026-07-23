"""
_bootstrap.py -- put Step 09's and Step 07's implementation folders on sys.path for the
exploration scripts that reuse them (the PSRO peek reuses Step 09's `PSRO`; the Leduc engine
comes from Step 07). Import this FIRST in any exploration script that touches them.

The replicator / matrix-game / spinning-top tinkering is kept SELF-CONTAINED in `_evo_tools.py`
(numpy only) so the exploration phase does not depend on the Phase-4 implementation modules --
mirroring how Step 09's exploration used its own `_marl_tools.py`.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# step10/exploration -> step10 -> implementation/
_IMPL_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
STEP09_IMPL = os.path.join(_IMPL_ROOT, "step09", "implementation")
STEP07_IMPL = os.path.join(_IMPL_ROOT, "step07", "implementation")

for _path in (STEP09_IMPL, STEP07_IMPL):
    if os.path.isdir(_path) and _path not in sys.path:
        sys.path.append(_path)
