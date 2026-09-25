"""
boot.py -- read-only access to Chapter 14's exact engine (and, through it, Chapter 7).

Chapter 15's pilots reuse Chapter 14's array trees, sequence-form LPs, zoos, match runner and
three-player machinery without copying them. Chapter 14's folder is APPENDED to sys.path, so a
module of this folder always wins on a name clash; every module here has a name that Chapter 14
and Chapter 7 do not use (boot, gifts, safe_agents, bounded3p, log15, run_*, plot_pilots).

Chapter 14's modules read their cached blueprints from Chapter 14's results/cache (read only:
every cache file this chapter needs already exists). Nothing here writes into another chapter's
folder: results, logs and figures go to this chapter's folders.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMPL_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO_ROOT = os.path.abspath(os.path.join(IMPL_ROOT, ".."))
STEP14_IMPL = os.path.join(IMPL_ROOT, "step14", "implementation")
RESULTS_DIR = os.path.join(HERE, "results")
LOGS_DIR = os.path.join(HERE, "logs")
FIG_DIR = os.path.join(REPO_ROOT, "deliverables", "reports", "step15", "figures")

if STEP14_IMPL not in sys.path:
    sys.path.append(STEP14_IMPL)

import deps as _deps14  # noqa: E402,F401  (Chapter 14's bootstrap: appends Chapter 7)

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
