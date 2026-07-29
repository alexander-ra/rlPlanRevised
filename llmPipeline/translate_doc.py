#!/usr/bin/env python3
"""Four-pass EN→BG document translation, one markdown block per request.

Divergence is prevented structurally rather than detected afterwards: each
request carries wide context but asks for exactly ONE block, so the model cannot
drop, merge or reorder anything. Verification reduces to "one unit in, one unit
out", and a failed unit costs a single cheap retry.

  pass 1  translate   faithful; no reordering, merging or additions
  pass 2  fluency     natural Bulgarian academic flow; meaning locked
  pass 3  deanglicise pseudo-Bulgarian anglicism -> real Bulgarian, or keep the
                      original English word in Latin script
  pass 4  grammar     agreement, definite articles, case

The existing human summaryBg.md is never read and never written.

    python llmPipeline/translate_doc.py --dry-run
    python llmPipeline/translate_doc.py --pass 1 --limit 5
    python llmPipeline/translate_doc.py            # all four passes
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import ollama                                    # noqa: E402

REPO = HERE.parent
SRC = REPO / "deliverables" / "reports" / "step01" / "summary" / "summaryEn.md"
OUTDIR = SRC.parent
DB = HERE / "out" / "glossary.db"
REPORT = HERE / "out" / "translate_step01_report.md"
MODEL = "bggpt3-27b"
CYR = re.compile(r"[Ѐ-ӿ]")

PASSES = {
    1: ("p1_translate", 0.25),
    2: ("p2_fluency", 0.40),
    3: ("p3_deanglicised", 0.40),
    4: ("p4_grammar", 0.25),
    5: ("p5_register", 0.20),
}

# pass 5 works on whole sections, because tense consistency is invisible from
# inside a single block. Internal newlines ride through as this sentinel so the
# numbered-block protocol stays line-oriented.
NL = "⏎"

# ── frozen spans ─────────────────────────────────────────────────────────────
# Order matters: block math before inline math, links before bare URLs.
FREEZE = [
    ("MATHB", re.compile(r"\$\$.*?\$\$", re.S)),
    ("MATHI", re.compile(r"(?<!\$)\$[^$\n]+\$(?!\$)")),
    ("IMGP",  re.compile(r"(?<=\]\()[^)\s]+(?=\))")),   # image/link TARGET only
    ("URL",   re.compile(r"<https?://[^>]+>")),
    ("SUP",   re.compile(r"<sup[^>]*>.*?</sup>", re.S)),
]


def freeze(text: str) -> tuple[str, dict[str, str]]:
    store: dict[str, str] = {}
    n = 0
    for tag, rx in FREEZE:
        def sub(m, tag=tag):
            nonlocal n
            k = f"⟦{tag}{n}⟧"
            store[k] = m.group(0)
            n += 1
            return k
        text = rx.sub(sub, text)
    return text, store


def thaw(text: str, store: dict[str, str]) -> tuple[str, list[str]]:
    missing = []
    for k, v in store.items():
        if k in text:
            text = text.replace(k, v)
        else:
            missing.append(k)
    return text, missing


# ── blocks ───────────────────────────────────────────────────────────────────

@dataclass
class Block:
    idx: int
    raw: str
    kind: str                      # frontmatter|heading|hr|quote|list|image|math|para
    level: int = 0
    out: dict[int, str] = field(default_factory=dict)   # pass -> bulgarian
    notes: list[str] = field(default_factory=list)


def classify(b: str) -> tuple[str, int]:
    s = b.strip()
    if re.fullmatch(r"-{3,}", s):
        return "hr", 0
    if s.startswith("#"):
        return "heading", len(s) - len(s.lstrip("#"))
    if s.startswith(">"):
        return "quote", 0
    if re.match(r"^\s*([-*+]|\d+\.)\s", s):
        return "list", 0
    if s.startswith("$$") and s.endswith("$$"):
        return "math", 0
    if re.fullmatch(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", s):
        return "image", 0
    return "para", 0


def parse(md: str) -> tuple[str, list[Block]]:
    fm = ""
    m = re.match(r"\A(---\r?\n.*?\r?\n---)\r?\n", md, re.S)
    if m:
        fm = m.group(1)
        md = md[m.end():]
    blocks = []
    for i, raw in enumerate(re.split(r"\n\s*\n", md)):
        if not raw.strip():
            continue
        k, lv = classify(raw)
        blocks.append(Block(len(blocks), raw.strip("\n"), k, lv))
    return fm, blocks


# ── glossary ─────────────────────────────────────────────────────────────────

def load_glossary() -> list[tuple[str, str]]:
    if not DB.exists():
        return []
    con = sqlite3.connect(str(DB))
    rows = con.execute("""
        SELECT t.term, COALESCE(pk.bg, p.chosen)
        FROM terms t JOIN proposals p ON p.key = t.key
        LEFT JOIN picks pk ON pk.key = t.key
        WHERE COALESCE(pk.bg, p.chosen) IS NOT NULL""").fetchall()
    con.close()
    out = [(t, b) for t, b in rows if t and b and len(t) > 2]
    out.sort(key=lambda r: -len(r[0]))      # longest first when matching
    return out


def gl_lemma(s: str) -> str:
    """Glossary rows are stored title-cased ("Информационно множество"); injected
    verbatim they plant capitals mid-sentence. Lowercase the first character
    unless the entry is an abbreviation or a multi-word proper noun."""
    s = (s or "").strip()
    if not s or s.isupper():
        return s
    parts = s.split()
    if len(parts) > 1 and parts[1][:1].isupper():
        return s
    return s[0].lower() + s[1:]


def glossary_for(text: str, gloss: list[tuple[str, str]], cap: int = 20):
    low = text.lower()
    hits, used = [], set()
    for en, bg in gloss:
        e = en.lower()
        if e in used:
            continue
        if re.search(r"(?<![a-z])" + re.escape(e) + r"(?![a-z])", low):
            hits.append((en, gl_lemma(bg)))
            used.add(e)
        if len(hits) >= cap:
            break
    return hits


# ── prompts ──────────────────────────────────────────────────────────────────

COMMON = """You are translating an academic dissertation summary from English into Bulgarian. The subject is artificial intelligence in computer games: reinforcement learning, game theory and neural networks.

ABSOLUTE RULES:
- You are given surrounding context ONLY so you understand the text. Translate or edit ONLY the block marked <<<TARGET>>>.
- Output the target block and NOTHING else. No preamble, no explanation, no quotes around it, no commentary.
- Preserve markdown EXACTLY: heading level (#, ##, ###), list markers (-), blockquote markers (>), bold (**), italics (*), and line breaks inside the block.
- Placeholders like ⟦MATHI3⟧ are frozen formulas, links and paths. Copy each one through unchanged, in place. Never translate, renumber, delete or reorder them.
- Keep algorithm names and abbreviations in Latin script: RL, CFR, DQN, PPO, MDP, TD, SB3.
- Never add a translator's note, never explain your choices, never summarise."""

P1 = COMMON + """

TASK: translate the target block into Bulgarian.
Translate it COMPLETELY and FAITHFULLY, sentence for sentence. Do not merge sentences, do not split them, do not reorder them, do not omit any detail, do not add anything that is not in the English. Every fact, number, name and citation must survive. The result must contain the same number of sentences as the English."""

P2 = COMMON + """

TASK: improve the Bulgarian so it reads as natural, fluent academic Bulgarian.
If the target block is a single heading line, return a single heading line - never append the paragraph that follows it.
You may restructure sentences, change word order and choose better wording. You may make LARGE edits to phrasing. But the MEANING must stay identical: no fact, number, name or nuance may be added, removed or altered. Do not translate afresh from the English - edit the Bulgarian you are given. The English is shown only so you can check nothing drifts."""

P3 = COMMON + """

TASK: remove pseudo-Bulgarian anglicisms from the Bulgarian text.
Find words that are merely English words given Bulgarian endings or Cyrillic spelling where a real Bulgarian word exists or where the English should have been left alone. For each one choose ONE of:
  (a) the established Bulgarian term, if one exists;
  (b) the original English word written in LATIN script, if Bulgarian has no accepted term and the English is what a Bulgarian specialist would actually write.
Do not touch words that are already correct, established Bulgarian scientific vocabulary, even if they are of foreign origin. Change nothing else: no restructuring, no rewording beyond these substitutions."""

P4 = COMMON + """

TASK: correct the grammar of the Bulgarian text.
Fix gender, number and case agreement between nouns, adjectives, participles and verbs; fix definite article usage including the full/short article on masculine nouns; fix prepositions and word order where they are ungrammatical. Preserve the wording and style otherwise - this is proofreading, not rewriting. If a sentence is already correct, return it unchanged."""

TENSE_RULES = """
BULGARIAN TENSE AND REGISTER (apply strictly):

1. NARRATING HOW A FIELD, IDEA OR METHOD DEVELOPED HISTORICALLY — use the historical present (сегашно историческо време) throughout: "Белман разработва динамичното програмиране", "Уоткинс формализира Q-learning", "Сътън преодолява пропастта". Do NOT drift into aorist mid-narrative ("разработи", "формализира" as past, "останаха", "преодоля", "оказа влияние"). A general unanchored statement may use the perfect: "не е възникнало в завършен вид".

2. STATING TIMELESS FACTS — definitions, how a method works, what something is — use the plain present: "Агентът наблюдава състоянието", "МДП представлява...".

3. REPORTING THIS WORK'S OWN EXPERIMENTS — use the aorist for what was done ("реализирахме", "сравнихме", "PPO постигна"), the imperfect for conditions that held ("най-влиятелните хиперпараметри бяха"), and the present for what results show ("резултатите показват", "фигурата илюстрира").

4. NEVER use the renarrative mood (преизказно наклонение) for results from the literature. Established findings are stated in the indicative — "Уоткинс формализира", never "Уоткинс бил формализирал".
"""

P5 = """You are a Bulgarian academic editor harmonising ONE SECTION of a dissertation summary on artificial intelligence in computer games.

You are given the section as numbered blocks. Return EVERY block, with the SAME number, in the SAME order, and NOTHING else.
""" + TENSE_RULES + """
5. TERMINOLOGY CONSISTENCY — the same English concept must be rendered by the same Bulgarian term everywhere in the section. If two variants appear, keep the one listed in the glossary below; if none is listed, pick one and use it consistently.

WHAT YOU MAY CHANGE: verb tense and aspect, and inconsistent terminology.
WHAT YOU MUST NOT CHANGE: anything else. Do not rephrase, do not reorder, do not shorten or expand, do not "improve" style, do not touch headings, do not add or remove sentences, facts, numbers or citations.
Preserve markdown exactly (#, -, >, **). Copy every ⟦…⟧ placeholder through unchanged. Keep the """ + NL + """ symbol where it appears - it marks a line break inside a block.
If a block already follows the rules, return it byte-for-byte unchanged."""

ALT1 = COMMON + """

TASK: translate the target block into natural, publication-quality academic Bulgarian in ONE step.

Translate completely and faithfully - every fact, number, name and citation must survive, and you must not add anything. But do NOT translate word-for-word: produce the sentence a Bulgarian academic would actually write.

At the same time, apply all of the following:
- Avoid pseudo-Bulgarian anglicisms. Where a real Bulgarian term exists, use it. Where Bulgarian has no accepted term, keep the English word in LATIN script rather than inventing a Cyrillic imitation.
- Get gender, number and case agreement right, and use definite articles correctly.
""" + TENSE_RULES

ALT2 = """You are a Bulgarian academic editor performing a final pass on ONE SECTION of a dissertation summary on artificial intelligence in computer games.

You are given the section as numbered blocks. Return EVERY block, with the SAME number, in the SAME order, and NOTHING else.
""" + TENSE_RULES + """
5. TERMINOLOGY CONSISTENCY — the same English concept must be rendered by the same Bulgarian term throughout the section, preferring the glossary form below.

6. GRAMMAR — fix gender/number/case agreement, definite articles (full and short forms), and prepositions.

Do not rephrase for style, do not reorder, do not add or remove content, do not touch headings.
Preserve markdown exactly (#, -, >, **). Copy every ⟦…⟧ placeholder through unchanged. Keep the """ + NL + """ symbol where it appears.
If a block is already correct, return it byte-for-byte unchanged."""

PASS_PROMPT = {1: P1, 2: P2, 3: P3, 4: P4, 5: P5, 11: ALT1, 12: ALT2}
PASSES[11] = ("alt1_rich", 0.30)
PASSES[12] = ("alt2_polish", 0.20)
SECTION_PASSES = {5, 12}


def build_prompt(blocks: list[Block], i: int, pnum: int,
                 gloss: list[tuple[str, str]]) -> tuple[str, dict[str, str]]:
    tgt = blocks[i]
    src_frozen, store = freeze(tgt.raw)

    parts = []
    prev = [b for b in blocks[max(0, i - 3):i] if b.kind != "hr"]
    if prev:
        lines = []
        for b in prev:
            done = b.out.get(pnum) or b.out.get(pnum - 1) or ""
            lines.append(f"EN: {b.raw}\nBG: {done}" if done else f"EN: {b.raw}")
        parts.append("PRECEDING CONTEXT (already handled - do not repeat):\n"
                     + "\n\n".join(lines))
    nxt = [b for b in blocks[i + 1:i + 3] if b.kind != "hr"]
    if nxt:
        parts.append("FOLLOWING CONTEXT (not yet handled - do not translate):\n"
                     + "\n\n".join(b.raw for b in nxt))

    hits = glossary_for(tgt.raw, gloss)
    if hits:
        # Framed as overridable, the model substituted its own wording 16 times for
        # "policy" alone. Terminology consistency has to be enforced where the text
        # is generated - inflection is expected, a different word is not.
        parts.append(
            "GLOSSARY — BINDING TERMINOLOGY. For each English term below you MUST use "
            "the given Bulgarian term. You MUST inflect it as Bulgarian grammar requires "
            "(case, number, definite article, gender agreement) — that is expected. You "
            "MUST NOT replace it with a synonym or a different wording, even if another "
            "word seems more natural. Consistency across the document depends on this.\n"
            + "\n".join(f'  "{e}" → "{b}"' for e, b in hits))

    if pnum == 1:
        parts.append(f"<<<TARGET>>>\n{src_frozen}\n<<<END TARGET>>>\n\n"
                     "Bulgarian translation of the target block:")
    else:
        cur = tgt.out.get(pnum - 1, "")
        cur_frozen, _ = freeze(cur)
        parts.append(f"ENGLISH SOURCE of the target block (reference only):\n{src_frozen}\n\n"
                     f"<<<TARGET>>>\n{cur_frozen}\n<<<END TARGET>>>\n\n"
                     "Corrected Bulgarian for the target block:")
    return "\n\n".join(parts), store


# ── verification ─────────────────────────────────────────────────────────────

def check(tgt: Block, out: str, missing: list[str]) -> list[str]:
    bad = []
    if missing:
        bad.append(f"lost placeholders: {','.join(missing)}")
    if not out.strip():
        bad.append("empty")
        return bad
    s = out.strip()
    if tgt.kind == "heading":
        lv = len(s) - len(s.lstrip("#"))
        if not s.startswith("#") or lv != tgt.level:
            bad.append(f"heading level {lv} != {tgt.level}")
        # a heading is one line; extra lines mean the model pulled the FOLLOWING
        # context into the target, which is how divergence actually showed up
        if len([l for l in s.splitlines() if l.strip()]) > 1:
            bad.append("heading gained extra lines (absorbed following context)")
    if tgt.kind == "quote":
        lines = [l for l in s.splitlines() if l.strip()]
        if not lines or not all(l.lstrip().startswith(">") for l in lines):
            bad.append("blockquote marker lost")
        if len(lines) != len([l for l in tgt.raw.splitlines() if l.strip()]):
            bad.append("blockquote line count changed")
    if tgt.kind == "list" and not re.match(r"^\s*([-*+]|\d+\.)\s", s):
        bad.append("list marker lost")
    if tgt.kind in ("para", "heading", "quote", "list") and not CYR.search(s):
        bad.append("no Cyrillic")
    r = len(s.split()) / max(1, len(tgt.raw.split()))
    if not 0.6 <= r <= 1.8:
        bad.append(f"length ratio {r:.2f}")
    return bad


def clean_reply(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"^<<<TARGET>>>\s*", "", s)
    s = re.sub(r"\s*<<<END TARGET>>>\s*$", "", s)
    s = re.sub(r"^```[a-z]*\s*|\s*```$", "", s)
    # models sometimes prefix a label
    s = re.sub(r"^(Bulgarian|Превод|Български)\s*[:\-]\s*", "", s, flags=re.I)
    return s.strip()


# ── run ──────────────────────────────────────────────────────────────────────

def run_pass(blocks: list[Block], pnum: int, gloss, limit: int, log) -> list[str]:
    name, temp = PASSES[pnum]
    todo = [b for b in blocks if b.kind not in ("hr", "math", "image")]
    if limit:
        todo = todo[:limit]
    log(f"\n=== pass {pnum} ({name}) — {len(todo)} blocks ===")
    problems = []
    t0 = time.perf_counter()

    for n, b in enumerate(blocks):
        if b.kind in ("hr", "math", "image"):
            b.out[pnum] = b.raw                       # nothing to translate
            continue
        if limit and b not in todo:
            continue

        prompt, store = build_prompt(blocks, n, pnum, gloss)
        # a failed edit must never replace known-good text: for passes 2-4 the
        # previous pass already passed verification, so that is the fallback.
        # Only pass 1 has nothing better to fall back to than the English.
        fallback = b.out.get(pnum - 1) if pnum > 1 else b.raw
        best, good, bad = None, None, ["not attempted"]
        for attempt in (1, 2):
            p = prompt if attempt == 1 else (
                prompt + "\n\nYour previous answer was rejected ("
                + "; ".join(bad) + "). Return ONLY the target block, "
                "preserving every ⟦…⟧ placeholder and its markdown formatting.")
            try:
                raw = ollama.generate(MODEL, p, PASS_PROMPT[pnum], temperature=temp,
                                      top_p=0.9, num_predict=1600, num_ctx=8192,
                                      think=False, log=log)
            except Exception as e:                    # noqa: BLE001
                bad = [f"request failed: {e}"]
                continue
            cand, miss = thaw(clean_reply(raw), store)
            bad = check(b, cand, miss)
            if best is None:
                best = cand
            if not bad:
                good = cand
                break

        b.out[pnum] = good or (fallback if fallback else (best or b.raw))
        if bad:
            b.notes.append(f"pass{pnum}: " + "; ".join(bad))
            problems.append(f"block {b.idx} ({b.kind}): " + "; ".join(bad))
            log(f"   ! block {b.idx} {b.kind}: {'; '.join(bad)}")

        done = sum(1 for x in blocks if pnum in x.out)
        if done % 20 == 0:
            el = time.perf_counter() - t0
            log(f"   {done}/{len(blocks)}  {el/60:4.1f}m")
    return problems


FM_SYSTEM = ("Translate the given English document title into Bulgarian for an academic "
             "dissertation on artificial intelligence in computer games. Keep algorithm "
             "abbreviations in Latin script. Output only the translated title, with no "
             "quotes and no commentary.")

_fm_cache: dict[str, str] = {}


# ── section pass (5 and 12): wide context, per-block acceptance ──────────────

BLOCK_RE = re.compile(r"^\s*\[(\d+)\]\s*(.*)$")


def sections(blocks: list[Block]) -> list[list[Block]]:
    out, cur = [], []
    for b in blocks:
        if b.kind == "heading" and b.level <= 2 and cur:
            out.append(cur)
            cur = [b]
        else:
            cur.append(b)
    if cur:
        out.append(cur)
    return out


def stems(text: str) -> set[str]:
    """Content-word stems. A tense/terminology fix keeps stems ("възникна" ->
    "възниква" both stem to "възник"); a rewrite does not. That is what lets us
    tell an intended edit from a regression."""
    return {w[:5] for w in re.findall(r"\w+", text.lower()) if len(w) > 3}


def accept_block(prev: str, cand: str, b: Block, missing: list[str]) -> list[str]:
    """Guards specific to a harmonisation pass: it may change verb forms and
    terminology, and nothing else."""
    bad = check(b, cand, missing)
    if bad:
        return bad
    if b.kind == "heading" and cand.strip() != prev.strip():
        return ["heading altered (register pass must not touch headings)"]
    a, c = stems(prev), stems(cand)
    if a:
        keep = len(a & c) / len(a)
        if keep < 0.70:
            bad.append(f"content drift: only {keep:.0%} of stems retained")
    r = len(cand.split()) / max(1, len(prev.split()))
    if not 0.85 <= r <= 1.20:
        bad.append(f"length changed {r:.2f}x")
    return bad


def run_section_pass(blocks: list[Block], pnum: int, src_pass: int, gloss, log):
    name, temp = PASSES[pnum]
    log(f"\n=== pass {pnum} ({name}) — section-level, from pass {src_pass} ===")
    problems, reverted = [], 0

    for si, sec in enumerate(sections(blocks)):
        work = [b for b in sec if b.kind not in ("hr", "math", "image")]
        for b in sec:
            if b.kind in ("hr", "math", "image"):
                b.out[pnum] = b.out.get(src_pass, b.raw)
        if not work:
            continue

        frozen, stores = [], []
        for b in work:
            f, st = freeze(b.out.get(src_pass, b.raw))
            frozen.append(f.replace("\n", f" {NL} "))
            stores.append(st)

        hits = glossary_for(" ".join(b.raw for b in work), gloss, cap=30)
        gl = ("\nGLOSSARY — BINDING. Where any of these English concepts appears, the "
              "Bulgarian term below must be the one used (inflected as grammar "
              "requires). Replace any competing wording with it:\n"
              + "\n".join(f'  "{e}" → "{bg}"' for e, bg in hits)) if hits else ""
        body = "\n".join(f"[{i}] {t}" for i, t in enumerate(frozen, 1))
        prompt = (f"{gl}\n\nSECTION ({len(work)} blocks). Return exactly "
                  f"{len(work)} lines, [1] to [{len(work)}]:\n\n{body}")

        got = None
        for attempt in (1, 2):
            p = prompt if attempt == 1 else prompt + (
                f"\n\nYour previous answer was malformed. Return EXACTLY "
                f"{len(work)} lines, each starting [n], nothing else.")
            try:
                raw = ollama.generate(MODEL, p, PASS_PROMPT[pnum], temperature=temp,
                                      top_p=0.9, num_predict=3000, num_ctx=8192,
                                      think=False, log=log)
            except Exception as e:  # noqa: BLE001
                log(f"   section {si}: request failed: {e}")
                continue
            d = {}
            for line in clean_reply(raw).splitlines():
                m = BLOCK_RE.match(line)
                if m and 1 <= int(m.group(1)) <= len(work):
                    d.setdefault(int(m.group(1)), m.group(2).strip())
            if len(d) == len(work):
                got = [d[i] for i in range(1, len(work) + 1)]
                break

        if got is None:
            log(f"   section {si}: malformed reply; whole section kept from pass {src_pass}")
            problems.append(f"section {si}: malformed reply, kept pass {src_pass}")
            for b in work:
                b.out[pnum] = b.out.get(src_pass, b.raw)
            reverted += len(work)
            continue

        for b, cand, store in zip(work, got, stores):
            prev = b.out.get(src_pass, b.raw)
            text, miss = thaw(cand.replace(f" {NL} ", "\n").replace(NL, "\n"), store)
            bad = accept_block(prev, text, b, miss)
            if bad:
                b.out[pnum] = prev            # revert THIS block only
                reverted += 1
                problems.append(f"block {b.idx} ({b.kind}): " + "; ".join(bad))
            else:
                b.out[pnum] = text
        log(f"   section {si}: {len(work)} blocks")

    log(f"   reverted {reverted} block(s) to pass {src_pass}")
    return problems


def frontmatter_bg(fm: str, translate: bool = True, log=print) -> str:
    """Only `title` and `subtitle` are translated; author/date/vars stay as-is
    and `lang` is forced to bg so the PDF build picks Bulgarian typesetting."""
    out = []
    for line in fm.splitlines():
        m = re.match(r'^(title|subtitle):\s*"(.*)"\s*$', line)
        if m and translate:
            field, val = m.group(1), m.group(2)
            if val not in _fm_cache:
                try:
                    r = ollama.generate(MODEL, f"English title: {val}\n\nBulgarian:",
                                        FM_SYSTEM, temperature=0.2, num_predict=160,
                                        num_ctx=2048, think=False, log=log)
                    _fm_cache[val] = (r or "").strip().strip('"').splitlines()[0].strip()
                except Exception:  # noqa: BLE001
                    _fm_cache[val] = val
            out.append(f'{field}: "{_fm_cache[val] or val}"')
        elif line.startswith("lang:"):
            out.append("lang: bg")
        else:
            out.append(line)
    return "\n".join(out)


def write_out(fm: str, blocks: list[Block], pnum: int) -> Path:
    name, _ = PASSES[pnum]
    body = "\n\n".join(b.out.get(pnum, b.raw) for b in blocks)
    p = OUTDIR / f"summaryBg_{name}.md"
    p.write_text(frontmatter_bg(fm) + "\n\n" + body + "\n", encoding="utf-8")
    assert p.name != "summaryBg.md", "must never overwrite the human translation"
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pass", dest="only", type=int, default=0,
                    choices=[0, 1, 2, 3, 4, 5, 11, 12])
    ap.add_argument("--chain", default="", choices=["", "main", "alt"],
                    help="main = p1..p5 (iterative)  alt = rich single pass + polish")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    def log(*x):
        print(" ".join(str(i) for i in x), flush=True)

    fm, blocks = parse(SRC.read_text(encoding="utf-8"))
    kinds = {}
    for b in blocks:
        kinds[b.kind] = kinds.get(b.kind, 0) + 1
    log(f"source: {SRC.name}  blocks={len(blocks)}  {kinds}")

    gloss = load_glossary()
    log(f"glossary: {len(gloss)} settled terms")

    if a.dry_run:
        i = next(i for i, b in enumerate(blocks) if b.kind == "para" and i > 3)
        p, store = build_prompt(blocks, i, 1, gloss)
        log(f"\n--- sample prompt for block {i} ({len(store)} frozen spans) ---\n")
        log(p[:2200])
        return 0

    if not ollama.wait_until_up(log=log):
        log("FATAL: ollama unreachable")
        return 1

    CHAINS = {"main": [1, 2, 3, 4, 5], "alt": [11, 12]}
    if a.only:
        passes = [a.only]
    elif a.chain:
        passes = CHAINS[a.chain]
    else:
        passes = [1, 2, 3, 4, 5]

    # which pass each one edits (pass 1 and alt1 translate from English).
    # NB: not named SRC - that is the module-level path to summaryEn.md.
    SRC_PASS = {2: 1, 3: 2, 4: 3, 5: 4, 12: 11}

    allprob: dict[int, list[str]] = {}
    for pn in passes:
        src = SRC_PASS.get(pn)
        if src and not any(src in b.out for b in blocks):
            prev = OUTDIR / f"summaryBg_{PASSES[src][0]}.md"
            if prev.exists():                        # resume from a written pass
                _f, pb = parse(prev.read_text(encoding="utf-8"))
                if len(pb) != len(blocks):
                    log(f"FATAL: {prev.name} has {len(pb)} blocks, source has {len(blocks)}")
                    return 1
                for b, q in zip(blocks, pb):
                    b.out[src] = q.raw
            else:
                log(f"pass {pn} needs pass {src} first")
                break
        if pn in SECTION_PASSES:
            allprob[pn] = run_section_pass(blocks, pn, src, gloss, log)
        else:
            allprob[pn] = run_pass(blocks, pn, gloss, a.limit, log)
        out = write_out(fm, blocks, pn)
        log(f"   wrote {out.name}  ({len(allprob[pn])} problem blocks)")

    lines = ["# Step 01 translation report", "",
             f"- source blocks: {len(blocks)} {kinds}",
             f"- glossary terms available: {len(gloss)}", ""]
    for pn, probs in allprob.items():
        lines += [f"## pass {pn} ({PASSES[pn][0]}) — {len(probs)} problem blocks", ""]
        lines += [f"- {p}" for p in probs] or ["_none_"]
        lines.append("")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"\nreport: {REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
