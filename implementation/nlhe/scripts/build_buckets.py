"""GPU card-abstraction build. Resumable per street (skips existing outputs).

Usage (repo root, venv active):
  python implementation/nlhe/scripts/build_buckets.py --street river
  python implementation/nlhe/scripts/build_buckets.py --all
  python implementation/nlhe/scripts/build_buckets.py --check   # sanity only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
sys.path.insert(0, str(SRC))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--street", choices=["preflop", "flop", "turn", "river"])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    import buckets
    cfg = json.loads((HERE.parent / "config" / "default.json").read_text())
    bk = cfg["buckets"]

    if a.check:
        import torch
        print("cuda:", torch.cuda.is_available())
        eq = buckets.Equity()
        import numpy as np
        keys = np.load(buckets.ART / "keys_river.npy")[:100000]
        h, b = buckets.decode_keys_to_cards(keys, 5)
        e = eq.river_equity(torch.from_numpy(h).to(eq.dev),
                            torch.from_numpy(b).to(eq.dev))
        print("sample river equity mean/min/max:",
              float(e.mean()), float(e.min()), float(e.max()))
        return

    order = ["river", "turn", "flop", "preflop"]  # river first (feature reuse)
    streets = order if a.all else [a.street]
    for s in streets:
        if s is None:
            continue
        n = bk[s]
        print(f"=== building {s} ({n} buckets) ===", flush=True)
        buckets.build_street(s, n, bins=30, flop_samples=bk["flop_runout_samples"],
                             kmeans_iters=bk["kmeans_iters"], force=a.force)


if __name__ == "__main__":
    main()
