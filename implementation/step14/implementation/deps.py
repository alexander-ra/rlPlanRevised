"""
Dependency bootstrap for the Chapter 14 evaluation framework.

Chapter 14 builds ON TOP of earlier chapters and imports their code read-only:

  * Step 07 (opponent modelling): the Kuhn/Leduc engines, the type zoo, the Bayesian
    type model, the continuous (Dirichlet) model, the change-point detector, the exact
    best response used as a cross-check.
  * Step 08 (safe exploitation): the constraint-generation solvers, used only as a
    cross-check of this chapter's one-shot dual LP on Kuhn.
  * Step 10 (EGTA): the Hodge "spinning-top" decomposition.

Step 07 and Step 08 both ship modules named config.py / tournament.py / plotting.py /
validate.py. We APPEND their folders to sys.path (never insert), so this chapter's own
modules always win on a name clash, and we never import those clashing names from them.
Step 10's spinning_top.py is numpy-only and is loaded by file path under a unique name.
"""

from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMPL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO_ROOT = os.path.abspath(os.path.join(IMPL_ROOT, ".."))
STEP07_IMPL = os.path.join(IMPL_ROOT, "step07", "implementation")
STEP08_IMPL = os.path.join(IMPL_ROOT, "step08", "implementation")
STEP10_IMPL = os.path.join(IMPL_ROOT, "step10", "implementation")
STEP11_IMPL = os.path.join(IMPL_ROOT, "step11", "implementation")
STEP12_RESULTS = os.path.join(IMPL_ROOT, "step12", "implementation", "results")
RESULTS_DIR = os.path.join(HERE, "results")
LOGS_DIR = os.path.join(HERE, "logs")

for _p in (STEP07_IMPL,):
    if _p not in sys.path:
        sys.path.append(_p)


def load_by_path(path: str, name: str):
    """Load a standalone .py file under a unique module name (avoids name clashes)."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def spinning_top():
    """Step 10's Hodge decomposition module (numpy only)."""
    return load_by_path(os.path.join(STEP10_IMPL, "spinning_top.py"), "step10_spinning_top")


os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
