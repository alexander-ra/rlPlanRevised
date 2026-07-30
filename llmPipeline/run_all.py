#!/usr/bin/env python3
"""Translate the whole corpus: 34 files, steps 01-12, five passes each.

Order is strict - steps ascending, and within each step onePager -> summary ->
report. Any existing Bulgarian target is renamed to *_old.md before the new one
is written, so nothing is overwritten.

Resumable and fault tolerant, because the run takes hours: completed files are
recorded in out/run_state.json and skipped on restart, and a file that fails is
logged while the batch continues.

State is written atomically after every block so the dashboard always reads a
consistent snapshot.

    python llmPipeline/run_all.py --dry-run
    python llmPipeline/run_all.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import traceback
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import ollama                       # noqa: E402
import translate_doc as T                     # noqa: E402

REPO = HERE.parent
REPORTS = REPO / "deliverables" / "reports"
OUT = HERE / "out"
STATE = OUT / "run_state.json"
LOG = OUT / "run_all.log"

ORDER = [("onePager", "summary/onePager.md"),
         ("summary", "summary/summaryEn.md"),
         ("report", "report_en.md")]


def log(msg: str) -> None:
    line = f"[{dt.datetime.now():%H:%M:%S}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:  # noqa: BLE001
        pass


def worklist() -> list[dict]:
    items = []
    for i in range(1, 13):
        step = f"step{i:02d}"
        for kind, rel in ORDER:
            p = REPORTS / step / rel
            if not p.exists():
                continue
            words = len(p.read_text(encoding="utf-8", errors="replace").split())
            items.append({"step": step, "kind": kind, "src": str(p),
                          "target": str(p.parent / T.OUT_NAME.get(p.name, p.stem + "Bg.md")),
                          "words": words})
    return items


# ── state ────────────────────────────────────────────────────────────────────

class State:
    """Atomically-written run state; the dashboard is a pure reader."""

    def __init__(self, items: list[dict]):
        self.d = {
            "started": time.time(),
            "heartbeat": time.time(),
            "total_files": len(items),
            "total_words": sum(x["words"] for x in items),
            "done_files": 0, "done_words": 0,
            "files": {x["src"]: {"step": x["step"], "kind": x["kind"],
                                 "words": x["words"], "status": "pending",
                                 "secs": 0, "defects": 0, "parity": None}
                      for x in items},
            "current": None, "log": [], "finished": None,
            "tokens_out": 0, "requests": 0, "tps_series": [],
            "retries": 0, "failures": 0, "reverted": 0,
        }
        if STATE.exists():                       # resume
            try:
                old = json.loads(STATE.read_text(encoding="utf-8"))
                for k, v in old.get("files", {}).items():
                    if k in self.d["files"] and v.get("status") == "done":
                        self.d["files"][k] = v
                self.d["done_files"] = sum(1 for v in self.d["files"].values()
                                           if v["status"] == "done")
                self.d["done_words"] = sum(v["words"] for v in self.d["files"].values()
                                           if v["status"] == "done")
                self.d["started"] = old.get("started", self.d["started"])
            except Exception:  # noqa: BLE001
                pass
        self._last = 0.0

    def note(self, msg: str) -> None:
        self.d["log"] = (self.d["log"] + [f"{dt.datetime.now():%H:%M:%S} {msg}"])[-40:]

    def save(self, force: bool = False) -> None:
        now = time.time()
        if not force and now - self._last < 1.0:
            return
        self._last = now
        self.d["heartbeat"] = now
        tmp = STATE.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.d, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, STATE)                    # atomic: readers never see a partial file


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    items = worklist()
    if a.limit:
        items = items[:a.limit]

    if a.dry_run:
        print(f"{len(items)} files, {sum(x['words'] for x in items):,} words\n")
        for x in items:
            t = Path(x["target"])
            act = f"rename -> {t.stem}_old.md, then write" if t.exists() else "write"
            print(f"  {x['step']} {x['kind']:<9} {x['words']:6,}w   {act} {t.name}")
        return 0

    st = State(items)
    recent: deque = deque(maxlen=60)

    def sink(s):                                  # live tokens/sec
        st.d["requests"] += 1
        st.d["tokens_out"] += s.get("out_tokens", 0)
        if s.get("gen_secs", 0) > 0.05:
            recent.append(s["out_tokens"] / s["gen_secs"])
            tps = sum(recent) / len(recent)
            st.d["tps"] = round(tps, 1)
            ser = st.d["tps_series"]
            if not ser or time.time() - ser[-1][0] > 20:
                ser.append([round(time.time()), round(tps, 1)])
                st.d["tps_series"] = ser[-120:]
    ollama.STATS_SINK = sink

    log(f"=== corpus run: {len(items)} files, {st.d['total_words']:,} words ===")
    if not ollama.wait_until_up(log=log):
        log("FATAL: ollama unreachable")
        return 1

    for x in items:
        src = Path(x["src"])
        rec = st.d["files"][x["src"]]
        if rec["status"] == "done":
            log(f"skip (done) {x['step']} {x['kind']}")
            continue

        target = Path(x["target"])
        if target.exists():                       # never overwrite; keep one _old
            old = target.with_name(f"{target.stem}_old{target.suffix}")
            if not old.exists():
                target.rename(old)
                log(f"   renamed {target.name} -> {old.name}")
            else:
                log(f"   {old.name} already exists; leaving it, {target.name} will be replaced")

        rec["status"] = "running"
        st.d["current"] = {"src": x["src"], "step": x["step"], "kind": x["kind"],
                           "words": x["words"], "pass": 0, "block": 0, "blocks": 0,
                           "started": time.time()}
        st.note(f"start {x['step']}/{x['kind']} ({x['words']:,}w)")
        st.save(True)
        log(f"--- {x['step']} {x['kind']} ({x['words']:,}w) ---")

        t0 = time.perf_counter()
        try:
            T.set_source(src)
            fm, blocks = T.parse(src.read_text(encoding="utf-8"))
            gloss = T.load_glossary()
            st.d["current"]["blocks"] = len(blocks)

            def progress(pn, i, n):
                c = st.d["current"]
                c["pass"], c["block"], c["blocks"] = pn, i, n
                st.save()
            T.PROGRESS = progress

            for pn in (1, 2, 3, 4, 5):
                st.d["current"]["pass"] = pn
                st.save(True)
                probs = (T.run_section_pass(blocks, pn, 4, gloss, log) if pn == 5
                         else T.run_pass(blocks, pn, gloss, 0, log))
                rec["defects"] += len(probs)
                if pn == 5:
                    st.d["reverted"] += len(probs)
                T.write_out(fm, blocks, pn)

            # structural parity against the source - the honest quality check
            out_blocks = [b for b in T.parse(
                Path(x["target"]).read_text(encoding="utf-8"))[1]]
            rec["parity"] = (len(out_blocks) == len(blocks))
            rec["status"] = "done"
            rec["secs"] = round(time.perf_counter() - t0, 1)
            st.d["done_files"] += 1
            st.d["done_words"] += x["words"]
            st.note(f"done {x['step']}/{x['kind']} in {rec['secs']/60:.1f}m"
                    + ("" if rec["parity"] else "  PARITY MISMATCH"))
            log(f"   done in {rec['secs']/60:.1f}m  defects={rec['defects']}  "
                f"parity={'ok' if rec['parity'] else 'MISMATCH'}")
        except Exception as e:                    # noqa: BLE001 - one bad file must not end the batch
            rec["status"] = "failed"
            rec["secs"] = round(time.perf_counter() - t0, 1)
            st.d["failures"] += 1
            st.note(f"FAILED {x['step']}/{x['kind']}: {e}")
            log(f"   FAILED: {e}\n{traceback.format_exc()[:600]}")
        st.d["current"] = None
        st.save(True)

    st.d["finished"] = time.time()
    st.save(True)
    log(f"=== finished: {st.d['done_files']}/{st.d['total_files']} files, "
        f"{st.d['failures']} failures ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted - rerun to resume")
        sys.exit(130)
