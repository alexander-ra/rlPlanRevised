"""
Dependency bootstrap for the Step 12 implementation.

WHAT THIS DOES
--------------
Step 12 (sequence models + LLM agents in strategic settings) reuses prior steps and
re-implements NONE of their engines (WORKFLOW.md section 6 -- import, never copy):

  - Step 02 -- the Kuhn Poker engine, the vanilla-CFR `KuhnTrainer` (our near-Nash data
    generator), and the exact `compute_exploitability` / `best_response_value` (the exact,
    tabular Kuhn metric all agents are measured against).
  - Step 07 -- the uniform `Game` interface (`make_game`), the policy currency + `play_hand`
    simulator (`policies`), and the exploitable opponent zoo (`opponent_types.make_type_zoo`)
    that supplies the "mixed opponent" data ARDT is trained on.
  - Step 09 -- the lazy torch guard (`torch_available` / `require_torch`); we fall back to a
    local definition if step09 is unavailable, so this module never hard-fails on import.

WHY WE *APPEND* (not insert) THE PRIOR STEPS
--------------------------------------------
Running a Step 12 script puts that script's own directory (step12/implementation) at
`sys.path[0]`, so Step 12's own same-named modules (`config.py`, `evaluation.py`,
`plotting.py`, `validate.py`) ALWAYS win. We APPEND the prior-step directories, so they are
only consulted for names Step 12 does not define.

THE `cfr` PACKAGE-COLLISION TRAP (why only step02 is on the path)
-----------------------------------------------------------------
BOTH step02 and step03 ship a package literally named `cfr`. Putting both on `sys.path`
merges them into one namespace package and silently cross-wires Kuhn's 2-action nodes with
Leduc's 3-action nodes. So we add ONLY step02's directory here. Leduc (SCALE-only, optional)
is reached through step07's `make_game("leduc")`, which loads the Leduc engine file directly
with importlib under a unique name -- no `cfr` package is ever imported for Leduc.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# step12/implementation -> step12 -> implementation/
_IMPL_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

STEP02 = os.path.join(_IMPL_ROOT, "step02")
STEP07_IMPL = os.path.join(_IMPL_ROOT, "step07", "implementation")
STEP09_IMPL = os.path.join(_IMPL_ROOT, "step09", "implementation")

# step02 is REQUIRED (Kuhn engine + exact exploitability + KuhnTrainer). step07 is REQUIRED
# (Game interface + opponent zoo). step09 is OPTIONAL (torch guard has a local fallback).
for _label, _path, _required in (
    ("Step 02", STEP02, True),
    ("Step 07", STEP07_IMPL, True),
    ("Step 09", STEP09_IMPL, False),
):
    if not os.path.isdir(_path):
        if _required:
            raise RuntimeError(
                f"Could not find {_label}'s code at {_path!r}. Step 12 reuses it "
                "(WORKFLOW.md section 6). Run from a checkout that still contains "
                "step02/ and step07/implementation/."
            )
        continue
    if _path not in sys.path:
        sys.path.append(_path)


# --- torch guard: prefer step09's, fall back to a local copy -------------------------
try:  # step09/implementation/learners.py
    from learners import torch_available, require_torch  # type: ignore  # noqa: F401
except Exception:  # pragma: no cover - only if step09 is missing/renamed
    _TORCH = None

    def torch_available() -> bool:  # type: ignore[misc]
        """True iff PyTorch can be imported (cached)."""
        global _TORCH
        if _TORCH is None:
            try:
                import torch  # noqa: F401

                _TORCH = True
            except ImportError:
                _TORCH = False
        return _TORCH

    def require_torch():  # type: ignore[misc]
        """Import and return torch, or raise a helpful error."""
        if not torch_available():
            raise ImportError(
                "PyTorch is required for the Decision Transformer / ARDT modules. "
                "Install it (`pip install torch`) or run only the torch-free suites "
                "(data generation, CFR/Nash, LLM-with-offline-stub, exploitability)."
            )
        import torch

        return torch


if __name__ == "__main__":
    print("Step 12 deps bootstrap")
    print("-" * 50)
    print(f"IMPL_ROOT   : {_IMPL_ROOT}")
    print(f"step02 path : {STEP02}  (exists={os.path.isdir(STEP02)})")
    print(f"step07 path : {STEP07_IMPL}  (exists={os.path.isdir(STEP07_IMPL)})")
    print(f"step09 path : {STEP09_IMPL}  (exists={os.path.isdir(STEP09_IMPL)})")
    print(f"torch_available() = {torch_available()}")
    # Smoke: the reused engines import cleanly.
    from engines import make_game  # noqa: E402
    from cfr.cfr_trainer import KuhnTrainer  # noqa: E402
    from evaluate.exploitability import compute_exploitability  # noqa: E402

    g = make_game("kuhn")
    print(f"make_game('kuhn') -> {g.name}, #deals={len(g.deals())} (expect 6)")
    print("KuhnTrainer + compute_exploitability imported OK:",
          KuhnTrainer is not None and compute_exploitability is not None)
