"""
Experiment configuration + sizing policy for Step 08.

COMPUTE REALITY CHECK (read before reaching for the 5090).
----------------------------------------------------------
Like Step 07, everything here is *tabular / exact*: CFR for the Nash baseline, full-tree best
response as the worst-case oracle, and small sequence-form LINEAR PROGRAMS (SciPy HiGHS) for
the solvers. This is CPU-bound, single-threaded work; the RTX 5090 does NOT accelerate any of
it (no neural nets, no GPU kernels). "Scale" here means a bigger game (Leduc), tighter Nash
solves, more opponent types, and more online hands -- all CPU time. The GPU matters in later
function-approximation steps, not this one.

Per implementation/WORKFLOW.md the default is small and fast. `smoke` (Kuhn only) runs in
well under a minute for the exact tables (the online pipeline adds a bit). `scale` adds Leduc
and the online matches; rough CPU estimates are in RUNTIME_NOTES (verify on your machine).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os

_HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(_HERE, "results")
PLOTS_DIR = os.path.join(_HERE, "plots")


SMOKE = {
    "name": "smoke",
    "games": ["kuhn"],
    "hero": 0,
    "nash_iters": {"kuhn": 30000, "leduc": 8000},
    # early-stopped CFR gives the eps-equilibrium baseline for prime-safe (eps > 0 on purpose).
    "epsilon_baseline_iters": {"kuhn": 200, "leduc": 400},
    # methods compared in the exact head-to-head table.
    "methods": ["nash", "full_br", "rnr_0.5", "ganzfried", "prime_safe", "adaptation"],
    # opponents to exploit (per game). Nash is included as the "can't be exploited" control.
    "opponents": {"kuhn": ["TightPassive", "LooseAggressive", "Thresholdish", "Nash"],
                  "leduc": ["Rock", "Maniac", "LoosePassive", "Nash"]},
    "rnr_ps": [0.0, 0.25, 0.5, 0.75, 1.0],
    "ses_predicate": {"kuhn": "whole_game", "leduc": "leduc_postflop"},
    # online pipeline / teaching attack sizing.
    "pipeline": {"model": "continuous", "refit_every": 200, "min_hands_before_exploit": 100,
                 "hands": 2000, "seeds": [0, 1, 2]},
    "teaching_attack": {"bait": {"kuhn": "TightPassive", "leduc": "Rock"},
                        "reveal": {"kuhn": "Nash", "leduc": "Nash"},
                        "switch_at": 1000, "total": 2000,
                        "methods": ["full_br", "ganzfried", "adaptation", "nash"],
                        "seeds": [0, 1, 2]},
    "plot": True,
}

SCALE = {
    "name": "scale",
    "games": ["kuhn", "leduc"],
    "hero": 0,
    "nash_iters": {"kuhn": 200000, "leduc": 40000},
    "epsilon_baseline_iters": {"kuhn": 400, "leduc": 800},
    "methods": ["nash", "full_br", "rnr_0.5", "ganzfried", "prime_safe", "adaptation",
                "ses_subgame"],
    "opponents": {"kuhn": ["TightPassive", "LooseAggressive", "Thresholdish", "AlwaysBet",
                           "AlwaysPass", "Nash"],
                  "leduc": ["Rock", "Maniac", "LoosePassive", "CallingStation", "Nash"]},
    "rnr_ps": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "ses_predicate": {"kuhn": "whole_game", "leduc": "leduc_postflop"},
    "pipeline": {"model": "continuous", "refit_every": 500, "min_hands_before_exploit": 200,
                 "hands": 20000, "seeds": [0, 1, 2, 3, 4]},
    "teaching_attack": {"bait": {"kuhn": "TightPassive", "leduc": "Rock"},
                        "reveal": {"kuhn": "Nash", "leduc": "Nash"},
                        "switch_at": 10000, "total": 20000,
                        "methods": ["full_br", "ganzfried", "adaptation", "nash"],
                        "seeds": [0, 1, 2, 3, 4]},
    "plot": True,
}

CONFIGS = {"smoke": SMOKE, "scale": SCALE}

# Rough, UNVERIFIED CPU estimates (single core). Measure on your own machine.
RUNTIME_NOTES = {
    "kuhn smoke (exact tables)": "seconds (small LPs + a few CFR solves).",
    "kuhn smoke (+ online pipeline)": "~1-3 min (solver refit every 200 hands x seeds).",
    "leduc scale (exact tables)": "minutes (bigger LPs; Ganzfried/adaptation do a few "
                                  "constraint-generation iters, each a full-tree BR).",
    "leduc scale (+ online pipeline)": "tens of minutes: the online loop re-solves an LP every "
                                       "refit; raise refit_every or shorten hands if it drags.",
    "note": "The most expensive single piece is the constraint-generation loop's inner "
            "full-tree best response on Leduc; it is exact and usually converges in a handful "
            "of iterations.",
}


def get_config(name: str = "smoke") -> dict:
    if name not in CONFIGS:
        raise ValueError(f"Unknown config {name!r}; choose from {sorted(CONFIGS)}")
    return dict(CONFIGS[name])
