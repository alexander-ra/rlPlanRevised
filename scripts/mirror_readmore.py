#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/mirror_readmore.py
#
# PURPOSE: Restore the bibliographic half of every "Прочетете повече" callout
#   from its English counterpart.
#
#   The translation pass rendered source titles and author surnames in Cyrillic
#   — "Наш, Дж. Ф. (1950). „Равновесни точки в игри с n играчи.“", "Шохам, Й. и
#   Лейтън-Браун, К.", "*neurIPS*". A reader who follows the reference needs the
#   words actually printed on the paper, so glossary rules 6 and 7 keep surnames
#   in Latin and do not translate the titles of foreign-language works.
#
#   A callout is `> **Read more:** <reference> [— <gloss>]`. The reference is
#   bibliography and is taken verbatim from English; the gloss is prose about
#   why the source is worth reading, and the Bulgarian one is kept.
#
#   EN and BG callouts are paired by position. That is safe because the pair of
#   files is a translation, block for block — the script refuses to touch a file
#   where the two counts disagree, which is exactly the case where position
#   would be meaningless.
#
# USAGE (run from repo root):
#   python scripts/mirror_readmore.py --dry-run
#   python scripts/mirror_readmore.py
#   python scripts/mirror_readmore.py --step step02
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS = REPO_ROOT / "deliverables" / "reports"

EN_LABEL = "**Read more:**"
BG_LABEL = "**Прочетете повече:**"

PAIRS = [("summary/summaryEn.md", "summary/summaryBg.md"),
         ("report_en.md", "report_bg.md"),
         ("summary/onePager.md", "summary/onePagerBg.md")]

# A gloss is separated from the reference by a spaced dash. The corpus uses an
# em dash in English and has drifted to a hyphen in Bulgarian.
GLOSS = re.compile(r"\s+[—–-]\s+")

# One callout may carry several references, separated by a middle dot. They are
# paired one for one, so a Bulgarian gloss stays with its own reference.
SEP = " · "

# A reference names a work: it carries a year, or an italicised title, or a
# quoted title. A callout that does none of that is a pointer to something in
# this repo ("the Step 07 opponent-modeling engine") and must stay Bulgarian.
LOOKS_LIKE_CITATION = re.compile(r"\(?(19|20)\d{2}\)?|\*[^*]+\*|\"[^\"]+\"|„[^“]+“")


def split_gloss(body: str) -> tuple[str, str]:
    """-> (reference, gloss). The gloss is whatever follows the LAST spaced dash,
    and only when it reads as prose rather than a page range or a chapter title."""
    parts = GLOSS.split(body)
    if len(parts) < 2:
        return body, ""
    head, tail = GLOSS.split(body, maxsplit=len(parts) - 2)[0], parts[-1]
    # "Chapter 5 — Extensive-form games" and "145–149" are part of the reference,
    # not a gloss. A gloss is a sentence: several words, starting lowercase.
    if len(tail.split()) < 3 or tail[:1].isupper() or tail[:1].isdigit():
        return body, ""
    return head, tail


def label_body(line: str, label: str) -> tuple[str, str]:
    """-> (prefix up to and including the label, the rest)."""
    i = line.index(label) + len(label)
    return line[:i], line[i:].strip()


def process(en_file: Path, bg_file: Path, dry: bool) -> tuple[int, str | None]:
    en_lines = en_file.read_text(encoding="utf-8").splitlines(keepends=True)
    bg_lines = bg_file.read_text(encoding="utf-8").splitlines(keepends=True)

    en_idx = [i for i, l in enumerate(en_lines) if EN_LABEL in l]
    bg_idx = [i for i, l in enumerate(bg_lines) if BG_LABEL in l]
    if not bg_idx:
        return 0, None
    if len(en_idx) != len(bg_idx):
        return 0, (f"{len(en_idx)} EN callouts vs {len(bg_idx)} BG — "
                   f"cannot pair by position, skipped")

    changed = 0
    for ei, bi in zip(en_idx, bg_idx):
        en_body = label_body(en_lines[ei], EN_LABEL)[1].rstrip()
        bg_prefix, bg_body = label_body(bg_lines[bi], BG_LABEL)
        # a callout may end in two spaces (a markdown hard break) — keep them
        trail = re.search(r"[ \t]*\r?\n?$", bg_lines[bi]).group(0)

        en_parts = en_body.split(SEP)
        bg_parts = bg_body.rstrip().split(SEP)
        if len(en_parts) != len(bg_parts):
            print(f"    ! {len(en_parts)} vs {len(bg_parts)} references in one "
                  f"callout; left alone")
            continue
        if not all(LOOKS_LIKE_CITATION.search(p) for p in en_parts):
            print(f"    . not a bibliographic callout, left alone: {bg_body[:70]}")
            continue

        out = []
        for en_part, bg_part in zip(en_parts, bg_parts):
            en_ref, _ = split_gloss(en_part)
            _, bg_gloss = split_gloss(bg_part)
            out.append(f"{en_ref} - {bg_gloss}" if bg_gloss else en_ref)
        new_body = SEP.join(out)
        new_line = f"{bg_prefix} {new_body}{trail}"
        if new_line != bg_lines[bi]:
            print(f"    - {bg_body[:96]}")
            print(f"    + {new_body[:96]}")
            bg_lines[bi] = new_line
            changed += 1

    if changed and not dry:
        bg_file.write_text("".join(bg_lines), encoding="utf-8")
    return changed, None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--step", default="", help="restrict to one step, e.g. step02")
    a = ap.parse_args()

    total, problems = 0, []
    for i in range(1, 13):
        step = f"step{i:02d}"
        if a.step and step != a.step:
            continue
        for en_rel, bg_rel in PAIRS:
            en, bg = REPORTS / step / en_rel, REPORTS / step / bg_rel
            if not (en.exists() and bg.exists()):
                continue
            print(f"  {step} {bg_rel}")
            n, err = process(en, bg, a.dry_run)
            if err:
                print(f"    ! {err}", file=sys.stderr)
                problems.append(f"{step} {bg_rel}: {err}")
            total += n

    print(f"\n{total} callout(s) restored{' (dry run)' if a.dry_run else ''}")
    for p in problems:
        print(f"  ! {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
