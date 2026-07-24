"""
Dependency bootstrap for the Step 11 implementation.

WHAT THIS DOES
--------------
Step 11 (dynamic coalition formation in So Long Sucker, a 4-player FFA game) reuses two prior
steps and re-implements NONE of them:

  - Step 10 -- the spinning-top transitive/cyclic decomposition (applied to the *projected*
    pairwise SLS meta-matrix) and the EGTA meta-Nash-mixture pattern.
  - Step 09 -- `solve_meta_nash` (for that projected 2-player meta-game) and the lazy torch
    guard (`torch_available` / `require_torch`).

This module appends BOTH folders to `sys.path` so plain imports resolve:

    import deps  # noqa: F401  (side effect: extends sys.path)

    # from Step 10:
    from spinning_top import transitive_ratio, cyclic_ratio, spinning_top_decomposition
    # from Step 09:
    from meta_nash import solve_meta_nash, nashconv_matrix
    from learners import torch_available, require_torch

WHY WE *APPEND* (not insert) THE PRIOR STEPS
--------------------------------------------
When you run a Step 11 script, Python puts that script's own directory
(step11/implementation) at `sys.path[0]`, so Step 11's own copies of same-named modules
(`config.py`, `tournament.py`, `plotting.py`, `evaluation.py`, `validate.py`) ALWAYS win. We
APPEND Step 10's then Step 09's directories, so they are only consulted for names Step 11 does
NOT define (`spinning_top`, `meta_nash`, `learners`, ...).

WHAT WE DELIBERATELY DO NOT REUSE
---------------------------------
- No Step 07 import: SLS is 4-player, so there is NO exact best-response / exploitability engine
  to reuse. The coalition detector is the conceptual descendant of Step 07's opponent model but
  is hand-coded fresh (help/harm matrices).
- No Step 09/10 PPO import: those learners are one-step / 2-player. SLS's PPO
  (`sls_ppo.py`) is sequential, variable-length and 4-player, so it is new code.

Run Step 11 scripts from `implementation/step11/implementation/`.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# step11/implementation -> step11 -> implementation/
_IMPL_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
STEP10_IMPL = os.path.join(_IMPL_ROOT, "step10", "implementation")
STEP09_IMPL = os.path.join(_IMPL_ROOT, "step09", "implementation")

for _label, _path in (("Step 10", STEP10_IMPL), ("Step 09", STEP09_IMPL)):
    if not os.path.isdir(_path):
        raise RuntimeError(
            f"Could not find {_label}'s implementation at {_path!r}. Step 11 reuses "
            f"{_label}'s modules (spinning-top + EGTA pattern from Step 10; meta-Nash + the "
            "torch guard from Step 09). Run from a checkout that still contains both "
            "step09/implementation/ and step10/implementation/."
        )

# APPEND (see module docstring): Step 11's own same-named modules must shadow the prior steps'.
for _path in (STEP10_IMPL, STEP09_IMPL):
    if _path not in sys.path:
        sys.path.append(_path)
