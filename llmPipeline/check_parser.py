#!/usr/bin/env python3
"""Parser self-check across the whole corpus.

Three parser bugs reached production before this existed - a leading HTML comment
swallowed as a block, code fences and raw HTML sent to the translator, and a
heading rule that rejected headings glued to their following list. Each was found
only by inspecting output after the fact.

This asserts the property that actually matters: preamble + blocks must reconstruct
the source exactly, and every block must be classified in a way that survives
verification. Run it before any batch translation.

    python llmPipeline/check_parser.py
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import translate_doc as T                                   # noqa: E402

GLOBS = ("deliverables/reports/step*/summary/onePager.md",
         "deliverables/reports/step*/summary/summaryEn.md",
         "deliverables/reports/step*/report_en.md")


def norm(s: str) -> str:
    """Collapse whitespace: block joining changes blank-line runs, nothing else."""
    return re.sub(r"\s+", " ", s).strip()


def main() -> int:
    repo = HERE.parent
    files = [f for g in GLOBS for f in sorted(glob.glob(str(repo / g)))]
    bad = 0
    print(f"checking {len(files)} files\n")

    for f in files:
        src = Path(f).read_text(encoding="utf-8")
        fm, blocks = T.parse(src)
        rebuilt = (fm + "\n\n" if fm else "") + "\n\n".join(b.raw for b in blocks)
        rel = Path(f).relative_to(repo)
        problems = []

        if norm(rebuilt) != norm(src):
            # locate the divergence rather than just flagging the file
            a, b = norm(src), norm(rebuilt)
            i = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]),
                     min(len(a), len(b)))
            problems.append(f"round-trip lost/changed content near: ...{a[max(0,i-60):i+60]!r}")

        # a fence must be atomic and never classified as prose
        opens = len(re.findall(r"^(?:```|~~~)[A-Za-z0-9_+\-]*[ \t]*$", src, re.M))
        if opens % 2:
            problems.append(f"odd number of code-fence delimiters ({opens}) - pairing unreliable")
        for b in blocks:
            if b.kind != "code" and re.search(r"^(?:```|~~~)", b.raw, re.M):
                problems.append(f"block {b.idx} holds a fence but is kind={b.kind}")
                break

        # every heading block's level must be recoverable
        for b in blocks:
            if b.kind == "heading" and not 1 <= b.level <= 6:
                problems.append(f"block {b.idx} heading level {b.level}")
                break

        if problems:
            bad += 1
            print(f"FAIL {rel}")
            for p in problems:
                print(f"       {p}")
        else:
            kinds = {}
            for b in blocks:
                kinds[b.kind] = kinds.get(b.kind, 0) + 1
            skipped = sum(v for k, v in kinds.items() if k in T.SKIP_KINDS)
            print(f"ok   {str(rel):<52} {len(blocks):3d} blocks "
                  f"({skipped} not translated)")

    print(f"\n{len(files) - bad}/{len(files)} files pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
