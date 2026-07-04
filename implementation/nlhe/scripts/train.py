"""MCCFR training entry point (start / resume / benchmark).

  python implementation/nlhe/scripts/train.py --benchmark   # Gate G5 throughput
  python implementation/nlhe/scripts/train.py --pilot-iters 2000000
  python implementation/nlhe/scripts/train.py --resume <run_id>

The full daemon (checkpointing, dashboard, eval) wraps this; this module owns
the core train loop and the throughput gate.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
sys.path.insert(0, str(SRC))


def _load(cfg):
    import numba
    import engine_ref as ER
    import engine_nb as EN
    import mccfr
    a = cfg["abstraction"]
    rules = ER.Rules(
        num_players=cfg["game"]["num_players"],
        starting_stack=cfg["game"]["starting_stack"],
        small_blind=cfg["game"]["small_blind"],
        big_blind=cfg["game"]["big_blind"],
        ante=cfg["game"]["ante"],
        raise_fractions=tuple(a["raise_fractions"]),
        include_allin=a["include_allin"],
        use_preflop_open=a["use_preflop_open"],
        preflop_open_bb=a["preflop_open_bb"],
        max_raises_per_street=a["max_raises_per_street"],
    )
    rules_arr = EN.pack_rules(rules)
    art = mccfr.load_artifacts()
    return EN, mccfr, rules_arr, art, numba


def benchmark(cfg, n_workers, seconds=30):
    """Throughput benchmark on a PRE-POPULATED table (the real steady state).

    Reports iters/sec plus the 400h visits-per-infoset budget so abstraction
    sizes can be compared directly."""
    EN, mccfr, rules_arr, art, numba = _load(cfg)
    numba.set_num_threads(n_workers)
    slot_key, regret, stratsum, tinfo = mccfr.build_table(rules_arr, cfg["buckets"])
    pb = float(cfg["mccfr"]["prune_threshold"])
    args = (rules_arr, slot_key, regret, stratsum,
            art["kpre"], art["bpre"], art["kflop"], art["bflop"],
            art["kturn"], art["bturn"], art["kriver"], art["briver"],
            art["rank"], art["binom"], art["perms"], pb)
    print(f"warming up JIT ({n_workers} threads)...", flush=True)
    mccfr.run_batch(2000, 0, *args, False)  # compile + warm
    print("benchmarking...", flush=True)
    total = 0
    start = time.time()
    gi = 2000
    batch = 20000
    while time.time() - start < seconds:
        mccfr.run_batch(batch, gi, *args, False)
        gi += batch
        total += batch
    dt = time.time() - start
    rate = total / dt
    used = int((slot_key != 0).sum())
    dupes = used - tinfo["used_slots"]
    iters_400h = rate * 400 * 3600
    ipi = iters_400h / tinfo["infosets"]  # iterations per infoset over 400h
    print(f"\nBENCHMARK buckets={cfg['buckets']['flop']}: "
          f"{rate:,.0f} iters/sec ({n_workers} threads, {total:,} iters in {dt:.0f}s)")
    print(f"  infosets: {tinfo['infosets']:,}  table: {tinfo['table_gb']} GB")
    print(f"  NEW slots created during run (must be 0): {dupes}")
    print(f"  400h budget: {iters_400h/1e9:.1f}B iters -> "
          f"{ipi:,.0f} iterations/infoset")
    print(f"  target >= 1000 iters/sec: {'PASS' if rate >= 1000 else 'FAIL'}")
    return {"buckets": cfg["buckets"]["flop"], "iters_per_sec": rate,
            "infosets": tinfo["infosets"], "new_slots": dupes,
            "iters_per_infoset_400h": ipi}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", action="store_true")
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--seconds", type=int, default=30)
    ap.add_argument("--buckets", type=int, default=None,
                    help="override postflop bucket count (100/200/400)")
    ap.add_argument("--run", type=str, default=None, help="run id to start/resume")
    ap.add_argument("--pilot-hours", type=float, default=None)
    ap.add_argument("--pilot-iters", type=int, default=None)
    a = ap.parse_args()
    cfg = json.loads((HERE.parent / "config" / "default.json").read_text())
    if a.buckets:
        for s in ("flop", "turn", "river"):
            cfg["buckets"][s] = a.buckets
    workers = a.workers or cfg["mccfr"]["n_workers"]
    if a.benchmark:
        benchmark(cfg, workers, a.seconds)
    elif a.run:
        import daemon
        daemon.main(a.run, a.pilot_hours, a.pilot_iters, cfg=cfg)
    else:
        ap.print_help()
