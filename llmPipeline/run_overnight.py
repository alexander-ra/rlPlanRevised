#!/usr/bin/env python3
"""Overnight glossary build - Stage 0 of the EN→BG pipeline.

Designed to be started and left alone. Resumable, deadline-bounded, and it
always leaves usable artifacts on disk even if killed mid-stage.

    python llmPipeline/run_overnight.py                 # full run
    python llmPipeline/run_overnight.py --hours 8
    python llmPipeline/run_overnight.py --smoke-only
    python llmPipeline/run_overnight.py --limit-files 3 --skip-smoke   # quick e2e
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import corpus, ollama, store as store_mod          # noqa: E402
from stages import a_extract, b_normalize, c_propose, d_emit  # noqa: E402

OUT = HERE.parent / "llmPipeline" / "out"
LOG_PATH = OUT / "run.log"


def make_logger():
    OUT.mkdir(parents=True, exist_ok=True)
    fh = open(LOG_PATH, "a", encoding="utf-8", buffering=1)

    def log(*a):
        msg = " ".join(str(x) for x in a)
        line = f"[{dt.datetime.now():%H:%M:%S}] {msg}"
        print(line, flush=True)
        try:
            fh.write(line + "\n")
        except Exception:  # noqa: BLE001
            pass
    return log


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=8.0, help="hard deadline")
    ap.add_argument("--granularity", default="", help="skip smoke test, force a mode")
    ap.add_argument("--skip-smoke", action="store_true")
    ap.add_argument("--smoke-only", action="store_true")
    ap.add_argument("--limit-files", type=int, default=0, help="debug: first N files")
    ap.add_argument("--max-queue", type=int, default=1400)
    ap.add_argument("--limit-terms", type=int, default=0, help="debug: propose only N terms")
    ap.add_argument("--fresh", action="store_true", help="ignore existing checkpoint")
    a = ap.parse_args()

    log = make_logger()
    t_start = time.time()
    deadline = t_start + a.hours * 3600
    stage_times: dict[str, float] = {}

    log("=" * 68)
    log(f"OVERNIGHT GLOSSARY RUN  deadline {a.hours}h "
        f"({dt.datetime.fromtimestamp(deadline):%H:%M})")
    log("=" * 68)

    db_path = OUT / "glossary.db"
    if a.fresh and db_path.exists():
        db_path.unlink()
        log("fresh start: checkpoint removed")
    st = store_mod.Store(db_path)
    meta = {"started": st.get("started") or f"{dt.datetime.now():%Y-%m-%d %H:%M}"}
    st.set("started", meta["started"])

    if not ollama.wait_until_up(log=log):
        log("FATAL: ollama never came up")
        return 1

    files = corpus.discover()
    if a.limit_files:
        files = files[:a.limit_files]
    log(f"corpus: {len(files)} files")

    # ── smoke test / granularity choice ────────────────────────────────
    gran = a.granularity or st.get("granularity")
    if a.smoke_only or (not gran and not a.skip_smoke):
        log("\n[SMOKE] comparing sentence / paragraph / window")
        t = time.perf_counter()
        sample = [f for f in files if "step03" in str(f[1]) or "step_07" in str(f[1])][:2] \
            or files[:2]
        try:
            gran, results = a_extract.smoke(sample, log=log)
            meta["smoke"] = results
            st.set("smoke", json.dumps(results))
        except Exception as e:  # noqa: BLE001
            log(f"[SMOKE] failed ({e}); defaulting to paragraph")
            gran, meta["smoke"] = "paragraph", []
        stage_times["smoke"] = time.perf_counter() - t
        log(f"[SMOKE] winner: {gran}")
        if a.smoke_only:
            d_emit.emit(st, OUT, {**meta, "granularity": gran,
                                  "stage_times": stage_times}, log=log)
            return 0
    gran = gran or "paragraph"
    st.set("granularity", gran)
    meta["granularity"] = gran
    if st.get("smoke") and "smoke" not in meta:
        meta["smoke"] = json.loads(st.get("smoke"))

    # ── A: extract ──────────────────────────────────────────────────────
    log(f"\n[A] extract  (granularity={gran})")
    t = time.perf_counter()
    st.add_chunks(corpus.build_chunks(gran, files))
    log(f"   {st.chunk_counts()[0]} pending / {sum(st.chunk_counts())} total chunks")
    a_extract.run(st, log=log, deadline=deadline)
    stage_times["A extract"] = time.perf_counter() - t
    d_emit.emit(st, OUT, {**meta, "stage_times": stage_times}, log=log)

    # ── B: normalise + categorise ───────────────────────────────────────
    log("\n[B] normalise + categorise")
    t = time.perf_counter()
    b_normalize.build_terms(st, log=log)
    b_normalize.categorise(st, log=log, deadline=deadline)
    stage_times["B normalise"] = time.perf_counter() - t
    d_emit.emit(st, OUT, {**meta, "stage_times": stage_times}, log=log)

    # Qwen and BgGPT are ~22GB each; 32GB cannot hold both
    ollama.unload(a_extract.MODEL, log=log)

    # ── C: propose + rule ───────────────────────────────────────────────
    log("\n[C] propose Bulgarian + auto-accept ruling")
    t = time.perf_counter()
    c_propose.run(st, log=log, deadline=deadline, max_queue=a.max_queue,
                  limit=a.limit_terms)
    stage_times["C propose"] = time.perf_counter() - t

    # ── D: emit ─────────────────────────────────────────────────────────
    log("\n[D] emit")
    meta["finished"] = f"{dt.datetime.now():%Y-%m-%d %H:%M}"
    counts = d_emit.emit(st, OUT, {**meta, "stage_times": stage_times}, log=log)

    log("=" * 68)
    log(f"DONE in {(time.time()-t_start)/60:.1f} min   "
        f"auto={counts['auto']} queue={counts['queue']} "
        f"deferred={counts['deferred']} unclear={counts['unclear']}")
    log(f"artifacts in {OUT}")
    log("=" * 68)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("interrupted - checkpoint is intact, rerun to resume")
        sys.exit(130)
    except Exception:
        traceback.print_exc()
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as fh:
                fh.write("FATAL\n" + traceback.format_exc() + "\n")
        except Exception:
            pass
        sys.exit(1)
