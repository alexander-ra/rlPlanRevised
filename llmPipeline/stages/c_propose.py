"""Stage C - propose Bulgarian renderings with BgGPT and rule on auto-accept.

Confidence is measured by SELF-CONSISTENCY, not by asking the model how sure it
is (LLM self-reported confidence is badly calibrated). Five independent samples
at temperature 0.8 -- the temperature is load-bearing: at 0.25 the samples would
agree trivially and unanimity would carry no information. The spread is the signal.

Auto-accept requires ALL of:
  1. 5/5 samples agree on the same normalised form
  2. corroboration - the form appears verbatim in the human Bulgarian corpus,
     or the term is a keep-Latin abbreviation
  3. the term is NOT one of the existing glossary rows (those get a full audit)
"""
from __future__ import annotations

import json
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path

from core import ollama

REPO = Path(__file__).resolve().parent.parent.parent
MODEL = "bggpt3-27b"
SAMPLES = 5
TEMP = 0.8

KEEP_LATIN = re.compile(r"^[A-Z][A-Za-z0-9]*(\+|\-[A-Za-z0-9]+)?$")

SYSTEM = """You are a terminologist building an English→Bulgarian glossary for a PhD dissertation on artificial intelligence in computer games (reinforcement learning, game theory, imperfect-information games, neural networks, multi-agent systems).

Given ONE English term, give the single best Bulgarian rendering for academic writing.

RULES:
- Prefer established Bulgarian scientific usage over a literal calque.
- Avoid unnecessary foreign borrowings when a natural Bulgarian form exists.
- Algorithm abbreviations (CFR, DQN, PPO, MARL, MAPPO, PSRO) stay in Latin script - answer with the abbreviation unchanged.
- Give the base dictionary form (singular, indefinite), not an inflected one.
- No explanation, no alternatives, no quotes, no parentheses.

Answer with the Bulgarian term and nothing else."""


def bg_corpus(log=print) -> str:
    """Human-written Bulgarian, used as the corroboration source."""
    parts = []
    d = REPO / "planning" / "rawStepsBg"
    if d.exists():
        for p in sorted(d.glob("*.md")):
            parts.append(p.read_text(encoding="utf-8", errors="replace"))
    for p in sorted((REPO / "deliverables" / "reports").glob("step*/summary/summaryBg.md")):
        parts.append(p.read_text(encoding="utf-8", errors="replace"))
    txt = fold(" \n ".join(parts))
    log(f"   corroboration corpus: {len(txt):,} chars of human Bulgarian")
    return txt


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"\s+", " ", s)


def norm_answer(s: str) -> str:
    s = (s or "").strip()
    s = s.split("\n")[0].strip()
    s = s.strip('"\'“”„«»')
    s = re.sub(r"^\s*(превод|термин)\s*[:\-]\s*", "", s, flags=re.I)
    s = re.sub(r"\s*\([^)]*\)\s*$", "", s)          # trailing gloss
    s = re.sub(r"[.;,]+$", "", s)
    return re.sub(r"\s+", " ", s).strip()


def sample_term(term: str, contexts: list[str], log=print) -> list[str]:
    hint = ""
    if contexts:
        hint = "\n\nIt appears in contexts such as: " + " | ".join(contexts[:2])
    out = []
    for i in range(SAMPLES):
        try:
            r = ollama.generate(
                MODEL, f"English term: {term}{hint}\n\nBulgarian term:", SYSTEM,
                temperature=TEMP, top_p=0.95, num_predict=60, num_ctx=4096,
                seed=1000 + i, think=False, log=log)
            a = norm_answer(r)
            if a:
                out.append(a)
        except Exception as e:  # noqa: BLE001
            log(f"      sample {i} failed for {term!r}: {e}")
    return out


def rule(term: str, samples: list[str], sources: list[str], corpus: str):
    """-> (decision, chosen, reason, candidates)"""
    cands = Counter(fold(s) for s in samples)
    pretty: dict[str, str] = {}
    for s in samples:
        pretty.setdefault(fold(s), s)
    candidates = [{"bg": pretty[k], "votes": v} for k, v in cands.most_common()]

    if not samples:
        return "queue", None, "no samples returned", candidates

    is_existing = any(s in ("glossary", "term_map") for s in sources)
    unanimous = len(cands) == 1 and len(samples) == SAMPLES
    top_fold, top_votes = cands.most_common(1)[0]
    top = pretty[top_fold]

    if not unanimous:
        return "queue", None, f"samples split {top_votes}/{len(samples)}", candidates

    # existing rows get a full audit regardless of agreement (user decision)
    if is_existing:
        return "queue", None, "existing glossary row - full audit requested", candidates

    if KEEP_LATIN.match(term.strip()) and fold(term) == top_fold:
        return "auto", top, "keep-Latin abbreviation, unchanged", candidates

    if top_fold and top_fold in corpus:
        return "auto", top, "5/5 unanimous + appears verbatim in human BG corpus", candidates

    return "queue", None, "5/5 unanimous but no corroboration in human BG corpus", candidates


def run(store, log=print, deadline: float | None = None, max_queue: int = 1400,
        limit: int = 0) -> None:
    corpus = bg_corpus(log=log)
    done = store.done_proposals()

    # store.terms() -> (key, term, kind, freq, contexts_json, sources_json,
    #                   category, existing_bg). Index by name: an earlier version
    #                   unpacked positionally, skipped `kind`, and so read `sources`
    #                   out of the `category` column -- json.loads("Game Theory")
    #                   fails, is_existing was always False, and existing glossary
    #                   rows could auto-accept instead of being audited.
    K, T, FREQ, CTX, SRC, EXBG = 0, 1, 3, 4, 5, 7

    def parse_sources(r) -> list[str]:
        try:
            v = json.loads(r[SRC] or "[]")
            return v if isinstance(v, list) else []
        except Exception:  # noqa: BLE001
            return []

    rows = [r for r in store.terms() if r[K] not in done]

    # Existing glossary/TERM_MAP rows FIRST: they are a mandated full audit, and
    # seed-only terms have freq=0 so a plain frequency sort would push all 208 into
    # the deferred tail. After them, frequency order so a deadline or budget cut
    # always keeps the terms that actually matter.
    rows.sort(key=lambda r: (0 if set(parse_sources(r)) & {"glossary", "term_map"} else 1,
                             -(r[FREQ] or 0), r[T]))
    if limit:
        rows = rows[:limit]
    if not rows:
        log("   all terms already proposed")
        return

    queued_so_far = store.decision_counts().get("queue", 0)
    n_existing = sum(1 for r in rows if set(parse_sources(r)) & {"glossary", "term_map"})
    log(f"   {len(rows)} terms to propose ({SAMPLES} samples each @ temp {TEMP})")
    log(f"   {n_existing} are existing glossary rows - queued first, exempt from budget")
    t0 = time.perf_counter()

    for i, r in enumerate(rows, 1):
        key, term, ctx_json = r[K], r[T], r[CTX]
        if deadline and time.time() > deadline:
            log("   DEADLINE reached in stage C; stopping cleanly")
            return
        try:
            contexts = json.loads(ctx_json or "[]")
        except Exception:  # noqa: BLE001
            contexts = []

        sources = parse_sources(r)
        is_existing = bool(set(sources) & {"glossary", "term_map"})

        # the audit is not optional, so existing rows never hit the budget cap
        if queued_so_far >= max_queue and not is_existing:
            store.save_proposal(key, [], [], "deferred", None,
                                f"queue budget {max_queue} reached; lower frequency")
            continue

        samples = sample_term(term, contexts, log=log)
        decision, chosen, reason, cands = rule(term, samples, sources, corpus)
        if decision == "queue":
            queued_so_far += 1
        store.save_proposal(key, samples, cands, decision, chosen, reason)

        if i % 25 == 0 or i == len(rows):
            el = time.perf_counter() - t0
            eta = el / i * (len(rows) - i)
            c = store.decision_counts()
            log(f"   propose {i}/{len(rows)}  {el/60:5.1f}m  ~{eta/60:5.1f}m left  "
                f"auto={c.get('auto',0)} queue={c.get('queue',0)} defer={c.get('deferred',0)}")
