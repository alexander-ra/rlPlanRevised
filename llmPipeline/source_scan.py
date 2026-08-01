#!/usr/bin/env python3
"""Find claims in the summaries that a reader would expect a citation for.

Chapters 4, 5 and 6 carry no references at all, and the rest were sourced ad hoc.
Rather than reread 200 pages by hand, this walks the corpus section by section
and asks a local model one narrow question per section: does this assert
something attributable, and is a source already attached?

The model is only ever asked to JUDGE and QUOTE. It never writes a citation and
never edits the corpus - a model-invented reference in a doctoral deliverable is
worse than a missing one. The output is a review list to work from.

    python llmPipeline/source_scan.py --dry-run     # show the first prompt
    python llmPipeline/source_scan.py --lang bg
    python llmPipeline/source_scan.py --only step04
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import ollama                                    # noqa: E402

REPO = HERE.parent
REPORTS = REPO / "deliverables" / "reports"
OUT_MD = REPO / "deliverables" / "reports" / "SOURCE_GAPS.md"
OUT_JSON = HERE / "out" / "source_gaps.json"

MODEL = "qwen3.6-27b"
FILES = {"en": "summary/summaryEn.md", "bg": "summary/summaryBg.md"}

SYSTEM = """You audit an academic dissertation chapter for missing citations. \
The subject is artificial intelligence in computer games: reinforcement learning, \
game theory, counterfactual regret minimisation and poker AI.

You are given ONE section. Decide whether it makes a claim that an academic reader \
would expect a source for, and whether a source is already attached.

Attributable claims are: named algorithms, theorems and results; empirical findings \
credited to someone; historical statements; performance numbers from published \
systems; assertions about what "the literature" shows.

NOT attributable: the author's own experiments and measurements (usually first \
person or "measured"/"our run"/"нашето изпълнение"), definitions of standard \
notation, descriptions of this project's own code, and forward or backward \
pointers to other chapters.

A source is already attached if the text carries a footnote marker, a parenthetical \
citation like (Author, Year), or names the paper inline.

Answer with STRICT JSON and nothing else:
{"verdict": "needs-source" | "has-source" | "n/a", "claim": "<the exact sentence \
needing a source, copied verbatim, or empty>", "why": "<max 12 words>"}"""

VERDICTS = {"needs-source", "has-source", "n/a"}
# a section is its heading plus the prose under it, up to the next heading
HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.M)
FOOTNOTE_DEF = re.compile(r"^\[\^[\w-]+\]:", re.M)


def sections(md: str) -> list[tuple[str, str]]:
    """-> [(heading, body)]. Footnote definitions and frontmatter are not prose."""
    md = re.sub(r"\A\s*<!--.*?-->\s*?\r?\n", "", md, flags=re.S)
    md = re.sub(r"\A\s*---\r?\n.*?\r?\n---\r?\n", "", md, flags=re.S)
    md = "\n".join(l for l in md.splitlines() if not FOOTNOTE_DEF.match(l))

    out: list[tuple[str, str]] = []
    marks = list(HEADING.finditer(md))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(md)
        body = md[m.end():end].strip()
        if len(body.split()) >= 40:          # too short to carry a claim
            out.append((m.group(2).strip(), body))
    return out


def ask(heading: str, body: str, log) -> dict | None:
    prompt = (f"SECTION HEADING: {heading}\n\nSECTION TEXT:\n{body[:6000]}\n\nJSON:")
    for attempt in (1, 2):
        raw = ollama.generate(MODEL, prompt, SYSTEM, temperature=0.1,
                              num_predict=300, num_ctx=16384, think=False, log=log)
        m = re.search(r"\{.*\}", raw, re.S)
        if not m:
            continue
        try:
            d = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if d.get("verdict") in VERDICTS:
            return d
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="bg", choices=["en", "bg"])
    ap.add_argument("--only", default="", help="restrict to one step, e.g. step04")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    def log(*x):
        print(" ".join(str(i) for i in x), flush=True)

    jobs = []
    for i in range(1, 13):
        step = f"step{i:02d}"
        if a.only and step != a.only:
            continue
        p = REPORTS / step / FILES[a.lang]
        if p.exists():
            for heading, body in sections(p.read_text(encoding="utf-8")):
                jobs.append((step, heading, body))

    log(f"{len(jobs)} section(s) to audit ({a.lang})")
    if a.dry_run:
        step, heading, body = jobs[0]
        log(f"\n--- sample prompt ({step}) ---\nSECTION HEADING: {heading}\n\n"
            f"SECTION TEXT:\n{body[:900]}\n...")
        return 0

    if not ollama.wait_until_up(log=log):
        log("FATAL: ollama unreachable")
        return 1

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    results, t0 = [], time.perf_counter()
    for n, (step, heading, body) in enumerate(jobs, 1):
        try:
            d = ask(heading, body, log) or {"verdict": "n/a", "claim": "",
                                            "why": "model gave no usable answer"}
        except Exception as e:                                  # noqa: BLE001
            d = {"verdict": "n/a", "claim": "", "why": f"request failed: {e}"}
        d.update(step=step, heading=heading)
        results.append(d)
        if n % 10 == 0 or n == len(jobs):
            el = (time.perf_counter() - t0) / 60
            gaps = sum(1 for r in results if r["verdict"] == "needs-source")
            log(f"   {n}/{len(jobs)}  {el:4.1f}m  needs-source so far: {gaps}")
            OUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                                encoding="utf-8")

    OUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    gaps = [r for r in results if r["verdict"] == "needs-source"]
    have = sum(1 for r in results if r["verdict"] == "has-source")
    L = ["# Липсващи източници - за преглед\n",
         f"{len(results)} проверени раздела: **{len(gaps)}** се нуждаят от източник, "
         f"{have} вече имат, {len(results)-len(gaps)-have} не изискват.\n",
         "Списъкът е съставен от локален езиков модел, който само *преценява и цитира* - "
         "не е писал нито една референция. Всяка добавена референция минава през "
         "проверка на човек.\n"]
    by_step: dict[str, list[dict]] = {}
    for r in gaps:
        by_step.setdefault(r["step"], []).append(r)
    for step in sorted(by_step):
        L.append(f"\n## {step}  ({len(by_step[step])})\n")
        L.append("| Раздел | Твърдение, което се нуждае от източник | Защо |")
        L.append("|---|---|---|")
        for r in by_step[step]:
            claim = (r.get("claim") or "").replace("|", "\\|").replace("\n", " ")[:220]
            why = (r.get("why") or "").replace("|", "\\|")[:60]
            L.append(f"| {r['heading'][:48]} | {claim} | {why} |")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")

    log(f"\n{len(gaps)} section(s) need a source → {OUT_MD.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
