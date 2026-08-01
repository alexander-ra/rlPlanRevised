#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/check_captions.py
#
# PURPOSE: Catch figures whose caption never made it onto the page.
#
#   The sibling failure to the one check_headings.py guards. LaTeX can drop a
#   caption without a word of complaint: the image is typeset, the \caption{} is
#   present and well-formed in the generated .tex, and nothing reaches the PDF.
#   Chapter 10's Mini-PBT figure lost its caption this way and nobody noticed
#   for months - the per-chapter build gave no reason to count figures, so a
#   hole in the numbering was invisible.
#
#   Two things are asserted:
#     1. every image in the markdown produces a numbered caption in the PDF
#     2. the numbering is contiguous from 1 - a gap means a counter was spent
#        on a float whose caption vanished
#
# REQUIREMENTS: PyMuPDF
#
# USAGE (run from repo root):
#   python scripts/check_captions.py                # per-chapter deliverables
#   python scripts/check_captions.py --bundles      # the bundles instead
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS_DIR = REPO_ROOT / "deliverables" / "reports"
BUNDLES_DIR = REPO_ROOT / "deliverables" / "bundles"
SUMMARIES_DIR = REPO_ROOT / "deliverables" / "summaries"

# Matched lazily: one caption in the corpus contains a literal [8,8,1,1], which
# a "[^]]*" alt pattern truncates.
IMAGE_RE = re.compile(r"!\[.*?\]\(([^)]+)\)")
# babel renders the label in the document language
CAPTION_RE = re.compile(r"(?:Figure|Фигура)\s+(\d+)\s*:")


def image_count(md_file: Path) -> int:
    if not md_file.exists():
        return 0
    return len(IMAGE_RE.findall(md_file.read_text(encoding="utf-8")))


def caption_numbers(pdf_file: Path) -> list[int]:
    import fitz
    with fitz.open(str(pdf_file)) as doc:
        text = "".join(p.get_text() for p in doc)
    return sorted({int(m.group(1)) for m in CAPTION_RE.finditer(text)})


def check(md_files: list[Path], pdf_file: Path) -> list[str]:
    """-> list of problems, empty when the PDF accounts for every figure."""
    if not pdf_file.exists():
        return [f"no PDF at {pdf_file.name}"]
    expected = sum(image_count(m) for m in md_files)
    if expected == 0:
        return []
    got = caption_numbers(pdf_file)
    problems = []
    if len(got) != expected:
        problems.append(f"{expected} image(s) in source, {len(got)} numbered "
                        f"caption(s) in the PDF")
    gaps = [n for n in range(1, (max(got) if got else 0) + 1) if n not in got]
    if gaps:
        problems.append(f"gap in figure numbering at {gaps} — a counter was "
                        f"spent on a caption that was not typeset")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bundles", action="store_true")
    a = ap.parse_args()

    try:
        import fitz  # noqa: F401
    except ImportError:
        print("ERROR: PyMuPDF is required.\n  pip install pymupdf", file=sys.stderr)
        return 1

    steps = sorted(p.name for p in REPORTS_DIR.iterdir()
                   if p.is_dir() and re.fullmatch(r"step\d{2}", p.name))

    jobs: list[tuple[str, list[Path], Path]] = []
    if a.bundles:
        for lang in ("en", "bg"):
            fn = "summaryEn.md" if lang == "en" else "summaryBg.md"
            jobs.append((f"allSummaries_{lang}.pdf",
                         [REPORTS_DIR / s / "summary" / fn for s in steps],
                         BUNDLES_DIR / f"allSummaries_{lang}.pdf"))
            rep = "report_en.md" if lang == "en" else "report_bg.md"
            jobs.append((f"allReports_{lang}.pdf",
                         [REPORTS_DIR / s / rep for s in steps],
                         BUNDLES_DIR / f"allReports_{lang}.pdf"))
    else:
        for s in steps:
            for lang, fn in (("en", "summaryEn.md"), ("bg", "summaryBg.md")):
                jobs.append((f"{s}_{lang}.pdf",
                             [REPORTS_DIR / s / "summary" / fn],
                             SUMMARIES_DIR / f"{s}_{lang}.pdf"))

    checked = bad = 0
    for name, mds, pdf in jobs:
        if not any(m.exists() for m in mds) or not pdf.exists():
            continue
        checked += 1
        problems = check(mds, pdf)
        if problems:
            bad += 1
            print(f"{pdf.relative_to(REPO_ROOT)}")
            for p in problems:
                print(f"   ✗ {p}")

    print(f"\n{checked} PDF(s) checked, {bad} with unaccounted figures.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
