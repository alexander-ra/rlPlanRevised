#!/usr/bin/env python3
"""Auto-resolve the queue entries that need no human judgement.

Three patterns, all of which were being shown as manual decisions:

  A  abbreviations      - Qwen classifies whether a term stays in Latin script in
                          Bulgarian text (CFR, DQN, CFR+, Q-learning). If so the
                          answer is the term itself; there is nothing to choose.
  B  case-only differs  - existing glossary "Експлоатируемост" vs 5/5 proposal
                          "експлоатируемост" is the same term. Keeps the lowercase
                          lemma but preserves embedded proper nouns
                          ("Равновесие на Наш" -> "равновесие на Наш").
  C  single 5/5         - one distinct candidate, unanimous across 5 samples, so
                          the picker offers a single radio button and no choice.

C relaxes the overnight run's corroboration requirement, which demanded a verbatim
hit in the human Bulgarian corpus. That corpus only covers steps 1-4, so most
vocabulary could never corroborate however obviously right it was.

Nothing already picked by hand is touched, and everything resolved here is written
as decision='auto' with a distinct reason, so it stays reviewable in the Auto tab.

    python llmPipeline/auto_resolve.py --dry-run
    python llmPipeline/auto_resolve.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import ollama, protocol, store as store_mod   # noqa: E402

QWEN = "qwen3.6-27b"
DB = HERE / "out" / "glossary.db"

# terms worth asking Qwen about: anything carrying capitals or a hyphenated
# Latin stem. Pure lowercase multi-word phrases are never keep-Latin.
LOOKS_LATIN = re.compile(r"[A-Z]{2,}|^[A-Z][a-z]*(\+|\d)|[A-Za-z]+-[A-Za-z]+|α|Q-")

ABBR_SYSTEM = """You decide how English technical terms should appear inside Bulgarian academic text about AI and game theory.

Answer KEEP if the term stays written in Latin script unchanged in Bulgarian text. This covers:
- abbreviations and acronyms: CFR, DQN, PPO, MARL, CFR+, MCCFR, PSRO, EGTA, NFSP, PBT
- algorithm and method names: Deep CFR, Q-learning, ReBeL, Adam
- system, agent, program and product names: AlphaStar, AlphaZero, AlphaGo, DeepStack, Libratus, Pluribus, OpenSpiel, PyTorch
- named games and benchmarks used as titles: Scotland Yard, Pommerman, StarCraft, Atari, Hanabi, Diplomacy

These are proper names. NEVER transliterate them into Cyrillic - "AlphaStar" must not become "алфаСтар".
The input may be lowercased; judge by what the term refers to, not its capitalisation.

Answer TRANSLATE if it is ordinary terminology that gets a Bulgarian rendering (examples: information set, replay buffer, learning rate, coalition, hand strength, battle of the sexes, normal-form game).

The input is a numbered list, and terms may arrive lowercased. For each input line output one line:
  [same number as the input line] KEEP <the term written with its correct capitalisation>
or
  [same number as the input line] TRANSLATE

Restore proper capitalisation on KEEP: "alphastar" -> KEEP AlphaStar, "commnet" -> KEEP CommNet,
"monte carlo cfr" -> KEEP Monte Carlo CFR, "cfr+" -> KEEP CFR+, "scotland yard" -> KEEP Scotland Yard.

The bracketed number must be the INPUT LINE NUMBER. Output only those lines."""


def fold(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s or "").lower()).strip()


def lower_lemma(s: str) -> str:
    """Lowercase the first character so the entry is a mid-sentence lemma.

    Embedded proper nouns must survive ("Равновесие на Наш" -> "равновесие на
    Наш"), and a leading multi-word proper noun must not be broken: if the second
    word is also capitalised the first word belongs to a name ("Монте Карло CFR"),
    so leave it alone.
    """
    s = (s or "").strip()
    if not s or s.isupper():
        return s
    parts = s.split()
    if len(parts) > 1 and parts[1][:1].isupper():
        return s
    return s[0].lower() + s[1:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    st = store_mod.Store(DB)
    rows = st.db.execute("""
        SELECT t.key, t.term, t.existing_bg, p.candidates_json, p.samples_json
        FROM terms t JOIN proposals p ON p.key = t.key
        LEFT JOIN picks pk ON pk.key = t.key
        WHERE p.decision IN ('queue','stage2') AND pk.key IS NULL
        ORDER BY t.freq DESC""").fetchall()
    print(f"{len(rows)} undecided terms")

    # ── A: ask Qwen which terms stay Latin ────────────────────────────────
    # Every term is classified, not just capital-looking ones: normalisation
    # lowercases keys, so proper nouns arrive as "alphastar" / "scotland yard"
    # and a capitalisation-based filter silently skipped exactly the names that
    # must not be transliterated.
    cand = rows
    print(f"asking Qwen about all {len(cand)} undecided terms")
    keep: dict[str, str] = {}      # key -> properly-cased Latin form
    if cand and not a.dry_run or cand:
        if not ollama.wait_until_up():
            print("ollama unreachable")
            return 1
        t0 = time.perf_counter()
        for i in range(0, len(cand), 25):
            grp = cand[i:i + 25]

            def call(items):
                return ollama.generate(
                    QWEN, "Classify each term:\n" + protocol.render(items),
                    ABBR_SYSTEM, temperature=0.1, num_predict=900,
                    num_ctx=8192, think=False)

            out = protocol.run_batched(grp, call, lambda r: r[1], lambda r: "TRANSLATE")
            for r, verdict in zip(grp, out):
                v = (verdict or "").strip()
                if v.upper().startswith("KEEP"):
                    cased = v[4:].strip(" :-") or (r[1] or "").strip()
                    keep[r[0]] = cased
            print(f"   classified {min(i+25,len(cand))}/{len(cand)}  "
                  f"{time.perf_counter()-t0:5.1f}s", flush=True)

    # ── apply ─────────────────────────────────────────────────────────────
    stats: Counter = Counter()
    changes: list[tuple] = []

    for key, term, ex_bg, cj, sj in rows:
        cands = json.loads(cj or "[]")
        samples = json.loads(sj or "[]")
        distinct = {fold(c["bg"]) for c in cands if c.get("bg")}
        pretty = {}
        for c in cands:
            if c.get("bg"):
                pretty.setdefault(fold(c["bg"]), c["bg"])

        # A - stays in Latin; Qwen also restores the proper capitalisation, since
        # key normalisation lowercased names like CommNet and AlphaStar
        if key in keep:
            changes.append((key, keep[key], "auto: proper name / abbreviation kept in Latin", 1))
            stats["A keep-Latin"] += 1
            continue

        # B - the audit AGREES with your existing entry, so there is nothing to
        # review: either every sample matched it, or it was the top-voted answer.
        # Only genuine disagreements need your judgement.
        if ex_bg and distinct:
            top = fold(cands[0]["bg"]) if cands and cands[0].get("bg") else ""
            if distinct == {fold(ex_bg)}:
                changes.append((key, lower_lemma(ex_bg),
                                "auto: audit agrees with glossary (unanimous)", 0))
                stats["B agrees (unanimous)"] += 1
                continue
            if top == fold(ex_bg):
                changes.append((key, lower_lemma(ex_bg),
                                "auto: audit agrees with glossary (top-voted)", 0))
                stats["B agrees (top-voted)"] += 1
                continue

        # C - a single distinct candidate, unanimous: the picker offered no choice.
        # But never overwrite a curated human entry that DISAGREES - a conflict
        # between your glossary and the model is exactly what the full audit is for.
        if len(distinct) == 1 and len(samples) >= 5:
            if ex_bg and fold(ex_bg) not in distinct:
                stats["conflict -> you"] += 1
                continue
            bg = pretty[next(iter(distinct))]
            changes.append((key, lower_lemma(bg), "auto: 5/5 unanimous, single candidate", 0))
            stats["C single 5/5"] += 1
            continue

        stats["left for you"] += 1

    print("\n" + "\n".join(f"  {k:<16} {v}" for k, v in stats.items()))

    if a.dry_run:
        print("\n-- sample of what would change --")
        for key, bg, reason, latin in changes[:12]:
            print(f"   {key[:34]:<36} -> {bg:<34} {reason}")
        return 0

    for key, bg, reason, latin in changes:
        st.db.execute(
            "UPDATE proposals SET decision='auto', chosen=?, reason=? WHERE key=?",
            (bg, reason, key))
        # keep_latin travels with the pick so the emitter knows not to inflect it
        st.db.execute(
            """INSERT OR REPLACE INTO picks(key,bg,status,keep_latin,first_use,note,stage,ts)
               VALUES (?,?,?,?,?,?,?,?)""",
            (key, bg, "auto", latin, 1, reason, "auto", time.time()))
    st.db.commit()
    print(f"\napplied {len(changes)} auto-resolutions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
