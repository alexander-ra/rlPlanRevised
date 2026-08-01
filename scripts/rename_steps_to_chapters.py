#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/rename_steps_to_chapters.py
#
# PURPOSE: "Step" in this corpus is used in two unrelated senses:
#   (1) a curriculum unit — "Step 7", "Стъпка 7", "the following steps"
#   (2) an algorithmic/training step — "at each step", "264K steps",
#       "training step", "На всяка стъпка"
#   The review asked for (1) to read "Chapter"/"Глава"; (2) must not change,
#   or every timestep count and training-loop description in the corpus goes
#   wrong. So this only rewrites occurrences that are unambiguously (1):
#   number-anchored ("Step 7", "steps 9 and 11") or demonstrative/ordinal
#   ("this step", "the following steps", "тази стъпка", "следващите стъпки").
#   A bare "step"/"steps"/"стъпка"/"стъпки" with no such marker is left alone.
#
#   Directory and file names (step01/, report_bg.md) are untouched - this is a
#   prose rename, not a repo reorganisation.
#
# USAGE (run from repo root):
#   python scripts/rename_steps_to_chapters.py --dry-run
#   python scripts/rename_steps_to_chapters.py
#   python scripts/rename_steps_to_chapters.py --skip deliverables/reports/step04/summary/summaryBg.md
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS = REPO_ROOT / "deliverables" / "reports"
STUDYPLAN = REPO_ROOT / "deliverables" / "studyPlan"

REL = ["report_en.md", "report_bg.md", "summary/summaryEn.md", "summary/summaryBg.md",
       "summary/onePager.md", "summary/onePagerBg.md"]


def files() -> list[Path]:
    out = []
    for i in range(1, 13):
        for rel in REL:
            p = REPORTS / f"step{i:02d}" / rel
            if p.exists():
                out.append(p)
    out += sorted(STUDYPLAN.rglob("*.md"))
    return out


# ── English ──────────────────────────────────────────────────────────────
# "Step 7", "Steps 7-8", "steps 9 and 11", "Steps 1, 4 and 9"
EN_NUM = re.compile(
    r"\b(Step|step)s?\s+(\d{1,2}(?:\s*[-–]\s*\d{1,2}|(?:,\s*\d{1,2})*\s+and\s+\d{1,2})?)\b")
EN_DEM = re.compile(
    r"\b(This|That|These|Those|Later|Following|Earlier|Previous|Next|Current|"
    r"this|that|these|those|later|following|earlier|previous|next|current)"
    r"(\s+)(step|steps)\b")


def fix_en(t: str) -> tuple[str, int]:
    n = 0

    def repl_num(m: re.Match) -> str:
        nonlocal n
        n += 1
        word, nums = m.group(1), m.group(2)
        plural = bool(re.search(r"[-–,]|\band\b", nums))
        head = "Chapter" if word[0].isupper() else "chapter"
        return f"{head}{'s' if plural else ''} {nums}"

    t = EN_NUM.sub(repl_num, t)

    def repl_dem(m: re.Match) -> str:
        nonlocal n
        n += 1
        plural = m.group(3) == "steps"
        return f"{m.group(1)}{m.group(2)}{'chapters' if plural else 'chapter'}"

    t = EN_DEM.sub(repl_dem, t)
    return t, n


# ── Bulgarian ────────────────────────────────────────────────────────────
# "Стъпка 7", "Стъпки 7-8", "стъпки 9 и 11" — С/с and singular/plural both vary
BG_NUM = re.compile(
    r"\b(Стъпк[аи]|стъпк[аи])\s+(\d{1,2}(?:\s*[-–]\s*\d{1,2}|(?:,\s*\d{1,2})*\s+и\s+\d{1,2})?)\b")
BG_DEM = re.compile(
    r"\b(тази|тези|тезите|следващите|предишните|текущата|настоящата|"
    r"Тази|Тези|Тезите|Следващите|Предишните|Текущата|Настоящата)"
    r"(\s+)(стъпка|стъпки)\b")


def fix_bg(t: str) -> tuple[str, int]:
    n = 0

    def repl_num(m: re.Match) -> str:
        nonlocal n
        n += 1
        word, nums = m.group(1), m.group(2)
        plural = word.endswith("и") or bool(re.search(r"[-–,]|\sи\s", nums))
        cap = word[0].isupper()
        head = ("Глави" if plural else "Глава") if cap else ("глави" if plural else "глава")
        return f"{head} {nums}"

    t = BG_NUM.sub(repl_num, t)

    def repl_dem(m: re.Match) -> str:
        nonlocal n
        n += 1
        plural = m.group(3) == "стъпки"
        return f"{m.group(1)}{m.group(2)}{'глави' if plural else 'глава'}"

    t = BG_DEM.sub(repl_dem, t)
    return t, n


def is_bg(p: Path) -> bool:
    name = p.name.lower()
    return "bg" in name or str(p).lower().count("\\bg\\") or "/bg/" in str(p).replace("\\", "/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip", action="append", default=[],
                    help="relative or absolute path to exclude (repeatable)")
    a = ap.parse_args()
    skip = {str((REPO_ROOT / s).resolve()) for s in a.skip}

    total = 0
    for f in files():
        if str(f.resolve()) in skip:
            print(f"  (skip) {f.relative_to(REPO_ROOT)}")
            continue
        t = f.read_text(encoding="utf-8")
        new, n = (fix_bg(t) if is_bg(f) else fix_en(t))
        if n:
            print(f"  {f.relative_to(REPO_ROOT)}: {n} replacement(s)")
            total += n
            if not a.dry_run:
                f.write_text(new, encoding="utf-8")

    print(f"\n{total} total{' (dry run)' if a.dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
