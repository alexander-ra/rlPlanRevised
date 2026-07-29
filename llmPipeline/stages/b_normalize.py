"""Stage B - dedupe extracted terms, ingest seeds, assign the 14 categories.

Seeds are the 208 rows of terminology_EN_BG.md and the 49 TERM_MAP ids. They
carry their existing Bulgarian so the picker can pre-select it tomorrow -- but
per the full-audit decision they are still queued, never auto-accepted.
"""
from __future__ import annotations

import json
import re
import time
from collections import defaultdict
from pathlib import Path

from core import ollama, protocol

REPO = Path(__file__).resolve().parent.parent.parent
MODEL = "qwen3.6-27b"

CATEGORIES = [
    "Document Structure & Administrative",
    "Game Theory",
    "Reinforcement Learning",
    "Algorithm Names",
    "Evaluation & Methodology",
    "Common Academic Phrases",
    "Neural Architecture & Layers",
    "Training & Optimization",
    "Abstraction & State Representation",
    "Search & Equilibrium Solving",
    "Multi-Agent & Coalition Dynamics",
    "Poker & Domain Vocabulary",
    "Mathematics & Statistics",
    "Software & Experimental Infrastructure",
]
UNCLEAR = "UNCLEAR"

# NOTE: the category list is deliberately UNNUMBERED. An earlier version numbered
# them 1..14, and the model conflated those numbers with the [n] item indices of the
# protocol - emitting "[3] Reinforcement Learning" for every item, which failed every
# batch. The only numbers in this prompt must be the item indices.
CAT_SYSTEM = (
    "You assign glossary terms from a PhD thesis on AI in computer games to exactly one category.\n\n"
    "ALLOWED CATEGORIES:\n"
    + "\n".join(f"- {c}" for c in CATEGORIES)
    + f"\n- {UNCLEAR}\n\n"
      "The input is a numbered list. For EACH input line, output one line:\n"
      "  [same number as the input line] <category name copied exactly>\n\n"
      f"The bracketed number must be the INPUT LINE NUMBER, never a category number.\n"
      f"Use {UNCLEAR} when a term fits none of the categories - do not force a bad fit.\n"
      "Output exactly as many lines as there are inputs, in the same order. No other text."
)

# ── seed ingestion ────────────────────────────────────────────────────────────

ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")


def load_glossary_rows() -> dict[str, str]:
    p = REPO / "deliverables" / "terminology_EN_BG.md"
    out: dict[str, str] = {}
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        en, bg = m.group(1).strip(), m.group(2).strip()
        if not en or en.lower() in {"english", "---"} or set(en) <= set("-: "):
            continue
        out[en] = bg
    return out


def load_term_map() -> dict[str, str]:
    """Pull EN phrase -> first BG surface form out of add_glossary_markers.py."""
    p = REPO / "scripts" / "add_glossary_markers.py"
    if not p.exists():
        return {}
    src = p.read_text(encoding="utf-8")
    m = re.search(r"TERM_MAP\s*=\s*\{(.*?)\n\}", src, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    for em in re.finditer(r'"([a-z0-9_]+)":\s*\(\s*(\[.*?\])\s*,\s*(\[.*?\])\s*,\s*\)', m.group(1), re.S):
        try:
            en_list = json.loads(em.group(2).replace("'", '"'))
            bg_list = json.loads(em.group(3).replace("'", '"'))
        except json.JSONDecodeError:
            continue
        if en_list:
            out[str(en_list[0])] = str(bg_list[0]) if bg_list else ""
    return out


# ── normalisation ─────────────────────────────────────────────────────────────

KEEP_CASE = re.compile(r"^[A-Z0-9][A-Z0-9+\-]*$")     # CFR, CFR+, DQN, MAPPO


def norm_key(t: str) -> str:
    s = t.strip().strip('."“”‘’,;:()[]')
    s = re.sub(r"\s+", " ", s)
    low = s.lower()
    # crude singularisation; only for multi-char words to avoid mangling "bias"
    if len(low) > 4 and low.endswith("ies"):
        low = low[:-3] + "y"
    elif len(low) > 4 and low.endswith("ses"):
        low = low[:-2]
    elif len(low) > 3 and low.endswith("s") and not low.endswith(("ss", "us", "is")):
        low = low[:-1]
    return low


def canonical(variants: list[str]) -> str:
    for v in variants:
        if KEEP_CASE.match(v.strip()):
            return v.strip()
    return min(variants, key=lambda v: (v[:1].isupper(), len(v)))


def build_terms(store, log=print) -> int:
    buckets: dict[str, dict] = defaultdict(
        lambda: {"variants": [], "kinds": [], "ctx": [], "freq": 0, "sources": set()})

    for rec in store.all_chunk_terms():
        t = rec.get("term", "")
        if not t or len(t) < 2:
            continue
        k = norm_key(t)
        if not k or k.isdigit():
            continue
        b = buckets[k]
        b["variants"].append(t.strip())
        b["kinds"].append(rec.get("kind", "concept"))
        b["freq"] += 1
        b["sources"].add("extracted")
        c = rec.get("ctx", "")
        if c and len(b["ctx"]) < 3:
            b["ctx"].append(c)

    for src_name, mapping in (("glossary", load_glossary_rows()),
                              ("term_map", load_term_map())):
        for en, bg in mapping.items():
            k = norm_key(en)
            if not k:
                continue
            b = buckets[k]
            b["variants"].append(en.strip())
            b["sources"].add(src_name)
            b["existing_bg"] = b.get("existing_bg") or bg
        log(f"   seeded {len(mapping)} rows from {src_name}")

    rows = []
    for k, b in buckets.items():
        kinds = b["kinds"] or ["concept"]
        rows.append({
            "key": k,
            "term": canonical(b["variants"]),
            "kind": max(set(kinds), key=kinds.count),
            "freq": b["freq"],
            "contexts": json.dumps(b["ctx"], ensure_ascii=False),
            "sources": json.dumps(sorted(b["sources"]), ensure_ascii=False),
            "existing_bg": b.get("existing_bg"),
        })
    store.upsert_terms(rows)
    log(f"   {len(rows)} unique terms after dedupe")
    return len(rows)


def categorise(store, log=print, deadline: float | None = None, batch: int = 20) -> None:
    todo = store.terms(only_uncategorised=True)
    if not todo:
        log("   all terms already categorised")
        return
    log(f"   categorising {len(todo)} terms")
    t0 = time.perf_counter()

    for i in range(0, len(todo), batch):
        if deadline and time.time() > deadline:
            log("   DEADLINE reached in stage B; stopping cleanly")
            return
        grp = todo[i:i + batch]

        def call(items):
            return ollama.generate(
                MODEL, "Assign a category to each term:\n" + protocol.render(items),
                CAT_SYSTEM, temperature=0.1, num_predict=1400, num_ctx=8192,
                think=False, log=log)

        out = protocol.run_batched(grp, call, lambda r: r[1], lambda r: UNCLEAR, log=log)
        for row, cat in zip(grp, out):
            cat = (cat or "").strip()
            if cat not in CATEGORIES:
                hit = next((c for c in CATEGORIES if c.lower() in cat.lower()), None)
                cat = hit or UNCLEAR
            store.set_category(row[0], cat)
        store.commit()

        n = min(i + batch, len(todo))
        if (i // batch) % 5 == 0 or n == len(todo):
            el = time.perf_counter() - t0
            log(f"   categorise {n}/{len(todo)}  {el/60:4.1f}m")
