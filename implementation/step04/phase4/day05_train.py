"""Day 5 entry point — collect prior days' results and emit the §8
Pareto frontier table + plot.

Two sub-stages:
  1. `day05_pareto.py` — read every `dayXX_results.json` and write the
     `pareto_table.csv` / `pareto.json` aggregate.
  2. `day05_plots.py` — render the matplotlib figure.

This script just dispatches to those drivers. EMD proxy values for the
day-2 / day-4 configurations are computed inline here and merged into
the JSON before plotting.
"""

import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from day02_card_bucketing import build_card_buckets
from day05_emd_evaluator import emd_proxy
from day02_hand_strength import NUM_RANKS as LEDUC_RANKS
from day05_pareto import write_outputs

PARETO_CSV = os.path.join(_HERE, ".day05_pareto_table.csv")
PARETO_JSON = os.path.join(_HERE, ".day05_pareto.json")


def _augment_with_emd():
    """Compute EMD proxy values for day-2 configurations and merge into
    `.day05_pareto.json` in place.
    """
    if not os.path.exists(PARETO_JSON):
        return
    with open(PARETO_JSON) as f:
        rows = json.load(f)

    # Pre-compute the lookup for day-2 configs.
    day2_emd = {}
    for k_label, kp, kf in [("k2", 2, 2), ("k3", 3, 3),
                            ("k5", min(3, LEDUC_RANKS),
                             min(5, LEDUC_RANKS * LEDUC_RANKS)),
                            ("full", LEDUC_RANKS,
                             LEDUC_RANKS * LEDUC_RANKS)]:
        buckets = build_card_buckets(kp, kf)
        for recall in (True, False):
            tag = f"{k_label}_{'perfect' if recall else 'imperfect'}"
            day2_emd[f"day2_{tag}"] = emd_proxy(buckets, recall)

    for r in rows:
        if r["name"] in day2_emd and r["emd_proxy"] is None:
            r["emd_proxy"] = day2_emd[r["name"]]

    write_outputs(rows, PARETO_CSV, PARETO_JSON)


def main():
    print("=== Day 5 — quality evaluation + Pareto frontier ===\n",
          flush=True)
    print("[1/3] Aggregating per-day results...", flush=True)
    rc = subprocess.call([sys.executable,
                          os.path.join(_HERE, "day05_pareto.py")])
    if rc != 0:
        return rc
    print("\n[2/3] Augmenting with EMD proxy values...", flush=True)
    _augment_with_emd()
    print("\n[3/3] Rendering Pareto plot...", flush=True)
    rc = subprocess.call([sys.executable,
                          os.path.join(_HERE, "day05_plots.py")])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
