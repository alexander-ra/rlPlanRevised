#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/drop_open_questions.py
#
# PURPOSE: Delete the "Open Questions" / "Отворени въпроси" block from every
#   chapter summary, per the review. Formatting is not uniform across chapters
#   (some are a bold lead-in + bullet list, some are a single bold-led
#   paragraph), so each block is found by its start marker and closed at the
#   next blockquote, heading, or "---" rule rather than by a single regex.
#
# USAGE (run from repo root):
#   python scripts/drop_open_questions.py --dry-run
#   python scripts/drop_open_questions.py
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()

MARKERS = [
    "**Open Questions:**", "**Open questions:**", "**Open questions.**",
    "**Open questions carried forward.**",
    "**Отворени въпроси:**", "**Отворени въпроси.**",
    "**Отворени въпроси за бъдеща работа.**",
    "**Отворени въпроси за бъдещи изследвания.**",
]

# a block ends at the next blockquote, heading, horizontal rule, or another
# bold lead-in paragraph — whichever comes first
STOP = re.compile(r"^(>|#{1,6}\s|---\s*$|\*\*[A-ZА-Я])", re.M)


def find_block(t: str, marker: str) -> tuple[int, int] | None:
    i = t.find(marker)
    if i < 0:
        return None
    # walk back over the blank line(s) before the marker
    start = i
    while start > 0 and t[start - 1] in "\n":
        start -= 1
    m = STOP.search(t, i + len(marker))
    end = m.start() if m else len(t)
    return start, end


def process(path: Path, dry: bool) -> int:
    t = path.read_text(encoding="utf-8")
    removed = 0
    while True:
        hit = None
        for marker in MARKERS:
            span = find_block(t, marker)
            if span:
                hit = span
                break
        if not hit:
            break
        start, end = hit
        snippet = t[hit[0]:hit[0] + 60].replace("\n", " ")
        print(f"    - [{path.name}] {snippet}...")
        t = t[:start] + t[end:]
        removed += 1
    if removed and not dry:
        path.write_text(t, encoding="utf-8")
    return removed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    total = 0
    for i in range(1, 13):
        step = f"step{i:02d}"
        for rel in ["summary/summaryEn.md", "summary/summaryBg.md"]:
            p = REPO_ROOT / "deliverables" / "reports" / step / rel
            if not p.exists():
                continue
            n = process(p, a.dry_run)
            if n:
                print(f"  {p.relative_to(REPO_ROOT)}: {n} block(s)")
            total += n

    print(f"\n{total} block(s) removed{' (dry run)' if a.dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
