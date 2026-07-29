"""Stage A - extract glossary-candidate terms with Qwen3.6-27B.

Tuned for RECALL: the manual picker is the filter, so a false positive costs one
keypress tomorrow while a miss costs a term missing from the thesis glossary.
"""
from __future__ import annotations

import json
import re
import time

from core import ollama

MODEL = "qwen3.6-27b"

SYSTEM = """You extract terminology for a bilingual (English→Bulgarian) glossary for a PhD thesis on AI in computer games: reinforcement learning, game theory, imperfect-information games, neural networks and multi-agent systems.

From the passage, extract every expression that a translator would need to render CONSISTENTLY every time it appears.

INCLUDE:
- technical terms and multi-word concepts (information set, counterfactual regret, replay buffer, suit isomorphism)
- neural architecture and training vocabulary (self-attention, weight decay, target network, learning rate)
- algorithm and method names (CFR+, Deep CFR, PSRO, MAPPO, Adam)
- game-domain vocabulary (Leduc, community card, pot, fixed-limit, showdown)
- evaluation, mathematics and statistics terms (exploitability, Pareto frontier, Earth Mover's Distance, k-means)
- software/experiment vocabulary (smoke test, wall-clock, checkpoint, ablation, seed)
- recurring academic or argumentative phrases (the present study, related work, key takeaway, limitations)

EXCLUDE:
- ordinary English needing no fixed rendering (however, therefore, very large)
- file names, code identifiers, paths, URLs, numbers
- names of people, universities and institutions

OUTPUT: a JSON array only. Each element: {"term": "...", "kind": "...", "ctx": "..."}
- "term": the base form, lowercase unless it is a proper name or abbreviation (Nash equilibrium, CFR, replay buffer)
- "kind": one of concept, algorithm, metric, architecture, training, domain, math, software, phrase
- "ctx": the short clause from the passage where it occurred (max 15 words)
No prose, no markdown fence, no commentary. If nothing qualifies, output []."""

ARRAY_RE = re.compile(r"\[.*\]", re.S)


def _parse(reply: str) -> list[dict]:
    if not reply:
        return []
    m = ARRAY_RE.search(reply)
    if not m:
        return []
    raw = m.group(0)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # models occasionally trail a comma or truncate mid-array; salvage objects
        data = []
        for om in re.finditer(r"\{[^{}]*\}", raw):
            try:
                data.append(json.loads(om.group(0)))
            except json.JSONDecodeError:
                continue
    out = []
    for d in data if isinstance(data, list) else []:
        if not isinstance(d, dict):
            continue
        t = str(d.get("term", "")).strip()
        if not t or len(t) > 90:
            continue
        out.append({"term": t,
                    "kind": str(d.get("kind", "concept")).strip()[:20],
                    "ctx": str(d.get("ctx", "")).strip()[:220]})
    return out


def extract_one(text: str, log=print) -> list[dict]:
    reply = ollama.generate(
        MODEL, f"PASSAGE:\n{text}\n\nJSON array:", SYSTEM,
        temperature=0.2, num_predict=1400, num_ctx=16384, think=False, log=log)
    return _parse(reply)


def smoke(files, log=print, corpus_words: int = 120_500) -> tuple[str, list[dict]]:
    """Compare sentence / paragraph / window on a sample; return the winner.

    Scoring must be normalised by WORDS COVERED, not by chunk count. Every mode
    has to process the same corpus, so a fixed number of chunks compares wildly
    different amounts of text -- 14 sentences is ~350 words against 13 windows at
    ~5,200. An earlier per-minute score made sentence mode look best purely
    because its chunks are tiny; corrected, it is the slowest way to cover the
    corpus. Reported here: yield per 1k words and projected full-corpus hours.
    """
    from core import corpus as C

    results = []
    for mode in ("paragraph", "window", "sentence"):
        rows = C.build_chunks(mode, files)[:14]
        if not rows:
            continue
        t0 = time.perf_counter()
        terms: set[str] = set()
        got = words = 0
        for _cid, _p, _m, text in rows:
            words += len(text.split())
            try:
                ts = extract_one(text, log=log)
            except Exception as e:  # noqa: BLE001
                log(f"   smoke {mode}: chunk failed ({e})")
                continue
            got += len(ts)
            terms.update(t["term"].lower() for t in ts)
        el = max(0.001, time.perf_counter() - t0)
        words = max(1, words)
        density = len(terms) / words * 1000
        proj_h = (el / words) * corpus_words / 3600
        dup = 1 - (len(terms) / got) if got else 0
        results.append({"mode": mode, "chunks": len(rows), "secs": round(el, 1),
                        "words": words, "raw": got, "unique": len(terms),
                        "per_1k_words": round(density, 1),
                        "proj_hours": round(proj_h, 2), "dup_rate": round(dup, 3)})
        log(f"   smoke {mode:<9} {len(rows):3d} chunks {words:5d}w  {el:5.1f}s  "
            f"{len(terms):4d} uniq  {density:5.1f}/1kw  proj {proj_h:4.1f}h  dup {dup:.0%}")

    if not results:
        return "window", []

    # Prefer the richest context that still fits the budget. Density alone cannot
    # detect precision loss: without context the model labels ordinary noun
    # phrases as terms, inflating both density and tomorrow's review queue.
    budget_h = 3.5
    order = {"window": 0, "paragraph": 1, "sentence": 2}   # most context first
    affordable = [r for r in results if r["proj_hours"] <= budget_h]
    pool = affordable or results
    best = min(pool, key=lambda r: (order[r["mode"]], r["proj_hours"]))
    log(f"   chose {best['mode']} (most context within {budget_h}h budget)")
    return best["mode"], results


def run(store, log=print, deadline: float | None = None) -> None:
    pending = store.pending_chunks()
    total_done = store.chunk_counts()[1]
    total = len(pending) + total_done
    log(f"   {len(pending)} chunks pending of {total}")

    t0 = time.perf_counter()
    for i, (cid, path, text) in enumerate(pending, 1):
        if deadline and time.time() > deadline:
            log("   DEADLINE reached in stage A; stopping cleanly")
            return
        try:
            terms = extract_one(text, log=log)
            store.finish_chunk(cid, terms)
        except Exception as e:  # noqa: BLE001 - one bad chunk must not end the run
            log(f"   chunk {cid} failed: {e}")
            store.finish_chunk(cid, [], err=str(e)[:400])

        if i % 10 == 0 or i == len(pending):
            el = time.perf_counter() - t0
            eta = el / i * (len(pending) - i)
            log(f"   extract {i}/{len(pending)}  {el/60:5.1f}m elapsed  ~{eta/60:5.1f}m left")
