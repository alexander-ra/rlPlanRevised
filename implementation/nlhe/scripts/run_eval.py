"""Standalone evaluation of the latest checkpoint, run as an isolated subprocess
by the daemon so a crash here can never take down training.

  python run_eval.py <run_dir>

Loads the newest valid checkpoint (slot_key + stratsum only), plays the blueprint
vs each baseline in duplicate-seat matches, and appends the bb/100 results to
<run_dir>/eval/index.json (+ a per-iteration file). Also dumps the 169-class
preflop raise frequency for the dashboard heatmap.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
sys.path.insert(0, str(SRC))


def main(run_dir):
    run_dir = Path(run_dir)
    import checkpoint as CK
    import evalmatch
    cfg = json.loads((HERE.parent / "config" / "default.json").read_text())
    n_decks = cfg["eval"].get("pilot_decks", 2000)

    ckpt, it = CK.latest_checkpoint(run_dir)
    if ckpt is None:
        print("no checkpoint yet; skipping eval")
        return
    slot_key, stratsum, meta = CK.load_strategy(ckpt)
    res = {"iteration": int(meta["iteration"])}
    for name, code in [("random", evalmatch.RANDOM),
                       ("calling_station", evalmatch.CALLING_STATION),
                       ("tag", evalmatch.TAG)]:
        t = time.time()
        bb, ci, _ = evalmatch.duplicate_match(slot_key, stratsum, code,
                                              n_decks=n_decks)
        res[name] = round(bb, 2)
        res[name + "_ci"] = round(ci, 2)
        print(f"  vs {name}: {bb:+.1f} bb/100 (+/-{ci:.0f}) [{time.time()-t:.0f}s]",
              flush=True)

    edir = run_dir / "eval"
    edir.mkdir(exist_ok=True)
    idx = edir / "index.json"
    hist = json.loads(idx.read_text()) if idx.exists() else []
    hist.append(res)
    tmp = str(idx) + ".tmp"
    Path(tmp).write_text(json.dumps(hist))
    import os
    os.replace(tmp, idx)
    (edir / f"eval_{res['iteration']}.json").write_text(json.dumps(res))
    print(f"eval @ {res['iteration']:,} written", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
