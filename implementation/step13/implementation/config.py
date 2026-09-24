"""
config.py -- paths, seeds and thresholds for Chapter 13 (behavioural analysis on real hand histories).

DATA (outside the repo, never committed)
----------------------------------------
The Playtech hand histories the plan assumes are not available yet. The substitute is the public,
MIT-licensed PHH dataset (github.com/uoftcprg/phh-dataset), sparse-cloned to DATA_ROOT:

  data/handhq/IPN-2009-07-01_2009-07-23_<stake>NLH_OBFU/   real online no-limit hold'em, July 2009,
                                                          iPoker Network, player IDs obfuscated
  data/pluribus/                                          the 10,000 released hands of Pluribus vs
                                                          five professionals per hand (a known bot)

Parsed arrays are cached under CACHE_ROOT (also outside the repo). Results JSON and logs live in
this folder (results/, logs/); figures are made from the JSON only.
"""
from __future__ import annotations

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
LOGS = HERE / "logs"

DATA_ROOT = Path(os.environ.get("STEP13_DATA", "D:/datasets/phh-dataset"))
CACHE_ROOT = Path(os.environ.get("STEP13_CACHE", "D:/datasets/step13_cache"))

# The iPoker Network (IPN) no-limit folders. 100NL = blinds $0.50/$1.
IPN_DIRS = {
    "IPN100": DATA_ROOT / "data/handhq/IPN-2009-07-01_2009-07-23_100NLH_OBFU",
}
PLURIBUS_DIR = DATA_ROOT / "data/pluribus"

# Seeds: every experiment that trains or samples runs these three (brief: >= 3 seeds).
SEEDS = (0, 1, 2)

# Minimum-sample thresholds (justified in player_stats.reliability(); see EXECUTION_NOTES).
MIN_HANDS_PLAYER = 500          # player included in style analysis
MIN_OPP = {                     # per-statistic minimum opportunities before a stat is reported
    "vpip": 100, "pfr": 100, "limp": 100, "three_bet": 30, "fold_to_3bet": 15,
    "cbet": 20, "fold_to_cbet": 20, "wtsd": 30, "af": 30, "afq": 50, "steal": 30,
    "donk": 20, "check_raise": 30,
}

# Action classes for behavioural cloning.
ACTION_NAMES = ["fold", "check", "call", "raise_s", "raise_m", "raise_l"]
FOLD, CHECK, CALL, RAISE_S, RAISE_M, RAISE_L = range(6)
# Raise-size buckets: (raise_to - current_bet) / (pot + to_call), i.e. the raise as a fraction
# of the pot after calling. A preflop open to 3 BB = (3-1)/(1.5+1) = 0.8 -> medium.
SIZE_EDGES = (0.55, 1.05)

STREETS = ["preflop", "flop", "turn", "river"]
