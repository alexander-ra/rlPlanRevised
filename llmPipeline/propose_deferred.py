#!/usr/bin/env python3
"""Stage 2 - generate BgGPT candidates for the DEFERRED terms.

The overnight run deferred 1,639 frequency-1 terms *before* sampling them, so
they carry no candidates and cannot be reviewed in the picker. This pass gives
them the same 5-sample treatment the queue got, so they become pickable.

Decisions written back:
  auto    - same conservative gate as the overnight run (unanimous + corroborated)
  stage2  - reviewable in the picker, second-priority behind the main queue

Resumable: rows already carrying samples are skipped.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import ollama, store as store_mod          # noqa: E402
from stages import c_propose                          # noqa: E402

OUT = HERE / "out"
LOG = OUT / "stage2.log"


def log(*a):
    line = f"[{dt.datetime.now():%H:%M:%S}] " + " ".join(str(x) for x in a)
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:  # noqa: BLE001
        pass


def main() -> int:
    st = store_mod.Store(OUT / "glossary.db")
    if not ollama.wait_until_up(log=log):
        log("FATAL: ollama down")
        return 1

    corpus = c_propose.bg_corpus(log=log)

    rows = st.db.execute(
        """SELECT p.key, t.term, t.contexts_json, t.sources_json, t.freq
           FROM proposals p JOIN terms t ON t.key = p.key
           WHERE p.decision = 'deferred'
             AND (p.samples_json IS NULL OR p.samples_json IN ('[]',''))
           ORDER BY t.freq DESC, t.term""").fetchall()

    log(f"stage 2: {len(rows)} deferred terms need candidates")
    t0 = time.perf_counter()

    for i, (key, term, ctx_json, src_json, _freq) in enumerate(rows, 1):
        try:
            contexts = json.loads(ctx_json or "[]")
        except Exception:  # noqa: BLE001
            contexts = []
        try:
            sources = json.loads(src_json or "[]")
        except Exception:  # noqa: BLE001
            sources = []

        samples = c_propose.sample_term(term, contexts, log=log)
        decision, chosen, reason, cands = c_propose.rule(term, samples, sources, corpus)
        # anything not auto-accepted is second-stage review, not "queue"
        if decision != "auto":
            decision, chosen = "stage2", None
        st.save_proposal(key, samples, cands, decision, chosen, reason)

        if i % 25 == 0 or i == len(rows):
            el = time.perf_counter() - t0
            eta = el / i * (len(rows) - i)
            c = st.decision_counts()
            log(f"   {i}/{len(rows)}  {el/60:5.1f}m  ~{eta/60:5.1f}m left  "
                f"auto={c.get('auto',0)} stage2={c.get('stage2',0)}")

    log(f"stage 2 done in {(time.perf_counter()-t0)/60:.1f} min")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted - rerun to resume")
        sys.exit(130)
