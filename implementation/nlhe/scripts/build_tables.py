"""One-time build of the static lookup tables into artifacts/.

Builds:
  - rank7.npy       : C(52,7) int16 normalized 7-card strengths (larger=stronger)
  - indexer_*.npy   : suit-isomorphism canonical index tables (see indexer.py)

Usage (from repo root, venv active):
  python implementation/nlhe/scripts/build_tables.py --rank
  python implementation/nlhe/scripts/build_tables.py --indexer
  python implementation/nlhe/scripts/build_tables.py --all
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
ART = HERE.parent / "artifacts"
sys.path.insert(0, str(SRC))


def build_rank(force=False):
    import cards
    ART.mkdir(exist_ok=True)
    out = ART / "rank7.npy"
    if out.exists() and not force:
        print(f"rank7 exists ({out}); use --force to rebuild")
        return
    print(f"building rank7 table -> {out} (C(52,7)={cards.C52_7:,})")
    t0 = time.time()
    cards.build_rank_table(out)
    print(f"done in {time.time()-t0:.0f}s")


def build_indexer(force=False):
    import indexer
    ART.mkdir(exist_ok=True)
    indexer.build_and_save(ART, force=force)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rank", action="store_true")
    ap.add_argument("--indexer", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.all or a.rank:
        build_rank(force=a.force)
    if a.all or a.indexer:
        build_indexer(force=a.force)
    if not (a.all or a.rank or a.indexer):
        ap.print_help()
