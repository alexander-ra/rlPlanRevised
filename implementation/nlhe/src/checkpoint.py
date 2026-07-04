"""Atomic checkpoint / resume / milestone I/O for the MCCFR table.

Full checkpoints (slot_key + regret + stratsum + counters) alternate between A/B
directories so a crash mid-write never destroys the last good state. Each write
goes to ``*.tmp`` then os.replace(); a ``DONE`` marker written last is the
integrity flag. Milestones store only the average-strategy inputs (slot_key +
stratsum), zstd-compressed — the permanent record consumed by eval/distill.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import numpy as np


def _atomic_save(path: Path, arr):
    tmp = path.with_suffix(path.suffix + ".tmp")
    np.save(tmp, arr)
    os.replace(tmp, path)  # np.save appends .npy to tmp; handle below


def _save_npy(path: Path, arr):
    """Atomic np.save to an explicit .npy path."""
    tmp = str(path) + ".tmp.npy"
    np.save(tmp, arr)
    os.replace(tmp, path)


def save_full(run_dir, which, slot_key, regret, stratsum, iteration, meta=None):
    """Write a full checkpoint into checkpoints/<which> (which in {'A','B'})."""
    d = Path(run_dir) / "checkpoints" / which
    d.mkdir(parents=True, exist_ok=True)
    done = d / "DONE"
    if done.exists():
        done.unlink()
    t0 = time.time()
    _save_npy(d / "slot_key.npy", slot_key)
    _save_npy(d / "regret.npy", regret)
    _save_npy(d / "stratsum.npy", stratsum)
    info = {"iteration": int(iteration), "ts": time.time()}
    if meta:
        info.update(meta)
    (d / "meta.json").write_text(json.dumps(info))
    done.write_text(str(iteration))  # integrity flag, written last
    return time.time() - t0


def _valid(d: Path):
    return (d / "DONE").exists() and (d / "meta.json").exists()


def latest_checkpoint(run_dir):
    """Return (dir, iteration) of the newest valid checkpoint, or (None, 0)."""
    best = None
    best_it = -1
    for which in ("A", "B"):
        d = Path(run_dir) / "checkpoints" / which
        if _valid(d):
            it = json.loads((d / "meta.json").read_text())["iteration"]
            if it > best_it:
                best_it = it
                best = d
    return best, max(best_it, 0)


def load_full(ckpt_dir):
    d = Path(ckpt_dir)
    slot_key = np.load(d / "slot_key.npy")
    regret = np.load(d / "regret.npy")
    stratsum = np.load(d / "stratsum.npy")
    meta = json.loads((d / "meta.json").read_text())
    return slot_key, regret, stratsum, meta


def load_strategy(ckpt_dir):
    """Load only slot_key + stratsum (for evaluation; skips the regret array)."""
    d = Path(ckpt_dir)
    slot_key = np.load(d / "slot_key.npy")
    stratsum = np.load(d / "stratsum.npy")
    meta = json.loads((d / "meta.json").read_text())
    return slot_key, stratsum, meta


def next_slot(run_dir):
    """Which of A/B to write next (the older / invalid one)."""
    _, it_a = _which_it(run_dir, "A")
    _, it_b = _which_it(run_dir, "B")
    return "A" if it_a <= it_b else "B"


def _which_it(run_dir, which):
    d = Path(run_dir) / "checkpoints" / which
    if _valid(d):
        return d, json.loads((d / "meta.json").read_text())["iteration"]
    return d, -1


def save_milestone(run_dir, slot_key, stratsum, iteration, day):
    """Compressed average-strategy snapshot (slot_key + nonzero stratsum rows)."""
    import zstandard as zstd
    d = Path(run_dir) / "milestones"
    d.mkdir(parents=True, exist_ok=True)
    used = slot_key != 0
    keys = slot_key[used]
    strat = stratsum[used]
    buf = _pack(keys, strat, iteration)
    out = d / f"m_{day:03d}_{iteration}.npz.zst"
    tmp = str(out) + ".tmp"
    cctx = zstd.ZstdCompressor(level=3)
    with open(tmp, "wb") as f:
        f.write(cctx.compress(buf))
    os.replace(tmp, out)
    return out


def _pack(keys, strat, iteration):
    import io
    bio = io.BytesIO()
    np.savez(bio, keys=keys, strat=strat, iteration=np.int64(iteration))
    return bio.getvalue()


def load_milestone(path):
    import io
    import zstandard as zstd
    dctx = zstd.ZstdDecompressor()
    with open(path, "rb") as f:
        raw = dctx.decompress(f.read())
    z = np.load(io.BytesIO(raw))
    return z["keys"], z["strat"], int(z["iteration"])
