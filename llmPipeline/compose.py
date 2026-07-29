#!/usr/bin/env python3
"""Compositional glossary resolution.

Re-evaluates multi-word terms with their already-settled constituents injected as
constraints, so "counterfactual value decomposition" is forced to render
"counterfactual value" the way that term was actually settled. Runs in rounds:
each newly settled term unlocks the compounds built on it.

    python llmPipeline/compose.py --report-only    # consistency + quarantine, writes report
    python llmPipeline/compose.py --dry-run        # sizes round 1, shows prompts
    python llmPipeline/compose.py                  # full run
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import ollama, store as store_mod                       # noqa: E402
from core.compose_graph import (Term, build_pool, constituents,    # noqa: E402
                                fold, has_cyrillic, load_terms,
                                ready_terms, stem)
from stages.c_propose import norm_answer                           # noqa: E402

MODEL = "bggpt3-27b"
SAMPLES = 5
TEMP = 0.8
OUT = HERE / "out"

BASE_SYSTEM = """You are a terminologist building an English→Bulgarian glossary for a PhD dissertation on artificial intelligence in computer games (reinforcement learning, game theory, imperfect-information games, neural networks, multi-agent systems).

Given ONE English term, give the single best Bulgarian rendering for academic writing.

RULES:
- Prefer established Bulgarian scientific usage over a literal calque.
- Algorithm abbreviations (CFR, DQN, PPO, MARL) stay in Latin script.
- Give the base dictionary form, not an inflected one.
- No explanation, no alternatives, no quotes, no parentheses.

Answer with the Bulgarian term and nothing else."""

CONSTRAINT_BLOCK = """

These parts of the term ALREADY have fixed Bulgarian renderings agreed for this glossary:
{pairs}

Use those renderings for those parts so the glossary stays internally consistent.
Bulgarian grammar comes first: inflect them, add prepositions, and reorder as the
language requires - "равновесие на Наш", never "Наш равновесие". Do NOT concatenate
the parts mechanically, and do not leave a part untranslated."""


def log(*a):
    line = f"[{dt.datetime.now():%H:%M:%S}] " + " ".join(str(x) for x in a)
    print(line, flush=True)
    try:
        with open(OUT / "compose.log", "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:  # noqa: BLE001
        pass


def sample_constrained(term: str, cons: dict[str, str], contexts: list[str]) -> list[str]:
    pairs = "\n".join(f'  "{k}" = "{v}"' for k, v in cons.items())
    system = BASE_SYSTEM + CONSTRAINT_BLOCK.format(pairs=pairs)
    hint = ("\n\nIt appears in contexts such as: " + " | ".join(contexts[:2])) if contexts else ""
    out = []
    for i in range(SAMPLES):
        try:
            r = ollama.generate(MODEL, f"English term: {term}{hint}\n\nBulgarian term:",
                                system, temperature=TEMP, top_p=0.95, num_predict=80,
                                num_ctx=4096, seed=2000 + i, think=False, log=log)
            a = norm_answer(r)
            if a:
                out.append(a)
        except Exception as e:  # noqa: BLE001
            log(f"      sample {i} failed for {term!r}: {e}")
    return out


def uses_constraints(answer: str, cons: dict[str, str]) -> bool:
    """Did the answer actually use every constrained rendering?

    Matched on a trimmed stem because Bulgarian inflects: the constraint
    "равновесие" legitimately surfaces as "равновесието" or "равновесия".
    """
    a = fold(answer)
    for bg in cons.values():
        if not has_cyrillic(bg):                    # Latin constraint: exact
            if fold(bg) not in a:
                return False
            continue
        if not all(stem(w) in a for w in fold(bg).split() if len(w) > 3):
            return False
    return True


def is_idiom(answer: str, prior: list[dict]) -> bool:
    """Non-compositional compounds ("deadly triad") produce an answer sharing no
    stem with any earlier unconstrained candidate. Never auto-accept those."""
    if not prior:
        return False
    a = fold(answer)
    for c in prior:
        bg = fold(c.get("bg", ""))
        if not bg:
            continue
        if any(stem(w) in a for w in bg.split() if len(w) > 3):
            return False
    return True


# ── reports ──────────────────────────────────────────────────────────────────

def consistency_report(terms: list[Term], pool: dict[str, str],
                       quarantined: list[Term], benign: list[Term],
                       leaky: dict[str, str] | None = None) -> int:
    known = set(pool) | {fold(t.term) for t in terms}
    rows = []
    for t in terms:
        if not t.settled_bg:
            continue
        cons = constituents(t, known)
        for c in cons:
            sub = pool.get(c)
            if not sub or not has_cyrillic(sub):
                continue
            if not all(stem(w) in fold(t.settled_bg)
                       for w in fold(sub).split() if len(w) > 3):
                rows.append((t.freq, t.term, t.settled_bg, c, sub))
    rows.sort(reverse=True)

    md = ["# Consistency report", "",
          "Settled compounds whose constituent is rendered differently than that",
          "constituent's own settled value. **Nothing here has been changed.**", "",
          f"- settled terms scanned: {sum(1 for t in terms if t.settled_bg)}",
          f"- inconsistencies found: **{len(rows)}**", ""]
    if rows:
        md += ["| freq | term | settled as | constituent | constituent settled as |",
               "|---:|---|---|---|---|"]
        for f, term, bg, c, sub in rows[:200]:
            md.append(f"| {f} | {term} | {bg} | {c} | {sub} |")
    md += ["", "## Quarantined constraints (real conflicts)", "",
           "Glossary holds a Bulgarian translation but the term was settled as Latin -",
           "a keep-Latin misclassification. Excluded from constraints and reverted to pending.", ""]
    if quarantined:
        md += ["| term | glossary | wrongly settled as |", "|---|---|---|"]
        for t in quarantined:
            md.append(f"| {t.term} | {t.existing_bg} | {t.settled_bg} |")
    else:
        md.append("_none_")
    md += ["", f"## Leaky single-word constraints ({len(leaky or {})})", "",
           "One-word terms whose settled Bulgarian absorbed a larger compound's meaning",
           "(`nash` settled as *Наш равновесие*, i.e. the rendering of *Nash equilibrium*).",
           "Dropped from the constraint pool - composing on them produces nonsense.", ""]
    for k, v in (leaky or {}).items():
        md.append(f"- `{k}` → “{v}”")

    md += ["", f"## Benign abbreviation-convention pairs ({len(benign)})", "",
           "Glossary stores the English expansion for abbreviation rows, so these are",
           "two roles rather than a disagreement. Kept as constraints.", ""]
    for t in benign[:40]:
        md.append(f"- `{t.term}` — glossary “{t.existing_bg}” · settled “{t.settled_bg}”")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "consistency_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    log(f"   consistency: {len(rows)} inconsistencies, {len(quarantined)} quarantined, "
        f"{len(benign)} benign -> out/consistency_report.md")
    return len(rows)


def revert_quarantined(st, quarantined: list[Term]) -> None:
    for t in quarantined:
        st.db.execute("DELETE FROM picks WHERE key=?", (t.key,))
        st.db.execute(
            "UPDATE proposals SET decision='queue', chosen=NULL, reason=? WHERE key=?",
            ("reverted: keep-Latin overrode a Bulgarian glossary entry", t.key))
    st.db.commit()
    if quarantined:
        log(f"   reverted {len(quarantined)} wrongly keep-Latin terms to the queue")


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--rounds", type=int, default=6)
    ap.add_argument("--hours", type=float, default=6.0)
    a = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    st = store_mod.Store(OUT / "glossary.db")
    deadline = time.time() + a.hours * 3600

    terms = load_terms(st)
    pool, quarantined, benign, leaky = build_pool(terms)
    log(f"terms={len(terms)}  constraints={len(pool)}  quarantined={len(quarantined)}  "
        f"benign={len(benign)}  leaky={len(leaky)}")
    for k, v in list(leaky.items())[:10]:
        log(f"   leaky constraint dropped: {k!r} -> {v!r}")

    consistency_report(terms, pool, quarantined, benign, leaky)
    if a.report_only:
        return 0

    if not a.dry_run:
        revert_quarantined(st, quarantined)
        terms = load_terms(st)
        pool, quarantined, benign, leaky = build_pool(terms)

    if not ollama.wait_until_up(log=log):
        log("FATAL: ollama unreachable")
        return 1

    totals: Counter = Counter()
    for rnd in range(1, a.rounds + 1):
        known = {fold(t.term) for t in terms}
        pending = [t for t in terms
                   if not t.settled_bg and t.decision in ("queue", "stage2")
                   and t.status not in ("picked",)]
        ready = ready_terms(pending, pool, known)
        log(f"\n=== round {rnd}: {len(ready)} ready of {len(pending)} pending ===")
        if not ready:
            break

        if a.dry_run:
            for t, cons in ready[:8]:
                log(f"   {t.term}  <-  {cons}")
            log(f"   [dry-run] would sample {len(ready)} terms")
            return 0

        newly = 0
        t0 = time.perf_counter()
        for i, (t, cons) in enumerate(ready, 1):
            if time.time() > deadline:
                log("   deadline reached; stopping cleanly")
                break
            try:
                contexts = json.loads(
                    st.db.execute("SELECT contexts_json FROM terms WHERE key=?",
                                  (t.key,)).fetchone()[0] or "[]")
            except Exception:  # noqa: BLE001
                contexts = []

            samples = sample_constrained(t.term, cons, contexts)
            counts = Counter(fold(s) for s in samples)
            pretty = {}
            for s in samples:
                pretty.setdefault(fold(s), s)
            cands = [{"bg": pretty[k], "votes": v} for k, v in counts.most_common()]

            decision, chosen, reason = "queue", None, ""
            if len(counts) == 1 and len(samples) == SAMPLES:
                top = pretty[next(iter(counts))]
                if is_idiom(top, t.candidates):
                    reason = "composed: 5/5 but diverges from all prior candidates - possible idiom"
                elif uses_constraints(top, cons):
                    decision, chosen = "auto", top
                    reason = "composed: 5/5 and uses the settled constituents"
                    newly += 1
                else:
                    reason = "composed: 5/5 but ignored the settled constituents"
            else:
                reason = f"composed: samples split ({counts.most_common(1)[0][1]}/{len(samples)})"

            # merge new candidates ahead of the old unconstrained ones
            merged = cands + [c for c in t.candidates
                              if fold(c.get("bg", "")) not in counts]
            st.db.execute(
                """UPDATE proposals SET decision=?, chosen=?, reason=?,
                       candidates_json=?, samples_json=? WHERE key=?""",
                (decision, chosen, reason,
                 json.dumps(merged, ensure_ascii=False),
                 json.dumps(samples, ensure_ascii=False), t.key))
            if decision == "auto":
                st.db.execute(
                    """INSERT OR REPLACE INTO picks(key,bg,status,keep_latin,first_use,note,stage,ts)
                       VALUES (?,?,?,0,1,?,?,?)""",
                    (t.key, chosen, "auto", reason, "composed", time.time()))
                pool[fold(t.term)] = chosen
            st.db.commit()
            totals[decision] += 1

            if i % 25 == 0 or i == len(ready):
                el = time.perf_counter() - t0
                log(f"   {i}/{len(ready)}  {el/60:5.1f}m  "
                    f"~{el/i*(len(ready)-i)/60:5.1f}m left  accepted={newly}")

        log(f"   round {rnd}: {newly} newly settled")
        if newly == 0:
            break
        terms = load_terms(st)
        pool, _q, _b, _l = build_pool(terms)

    log(f"\nDONE  auto={totals.get('auto',0)}  queued={totals.get('queue',0)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted - progress is committed, rerun to resume")
        sys.exit(130)
