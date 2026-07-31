#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/check_headings.py
#
# PURPOSE: Catch headings that exist in the markdown but never made it onto the
#   page. LaTeX can silently drop a section heading that falls between floats -
#   it appears in the generated .tex, is absent from the PDF, and no error is
#   raised. Step 11's "Coalition-aware MAPPO" heading was lost this way.
#
#   Compares every ATX heading in a source file against the heading-sized text
#   actually present in the built PDF.
#
# REQUIREMENTS: PyMuPDF
#
# USAGE (run from repo root):
#   python scripts/check_headings.py                # all step deliverables
#   python scripts/check_headings.py --bundles      # the bundles instead
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS_DIR = REPO_ROOT / "deliverables" / "reports"


# LaTeX sets ff/fi/fl as single ligature glyphs, so "efficient" extracts from
# the PDF as "e<ﬀ>icient". Without expanding these, a correctly typeset heading
# looks missing.
LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
             "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st"}


def norm(s: str) -> str:
    for lig, plain in LIGATURES.items():
        s = s.replace(lig, plain)
    return re.sub(r"[^0-9a-zA-Zа-яА-Я]+", "", s).lower()


def source_headings(md: Path) -> list[str]:
    """Level 1-2 ATX headings, skipping fenced code and comments.

    Only levels 1-2. LaTeX sets \\subsubsection at the body size, so a level-3
    heading cannot be told apart from body text by size, and including them
    produced hundreds of false positives.
    """
    out, in_fence, in_comment = [], False, False
    for line in md.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if s.startswith("<!--"):
            in_comment = True
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if in_fence:
            continue
        if m := re.match(r"^(#{1,2})\s+(.+?)\s*$", s):
            # Inline HTML anchors and code spans are markup, not printed text.
            text = re.sub(r"<[^>]*>", "", m.group(2))
            text = re.sub(r"`([^`]*)`", r"\1", text)
            # A hand-written Contents section is deliberately dropped from
            # bundle parts, so its absence is not a defect.
            if text.strip() and norm(text) not in ("tableofcontents", "contents",
                                                   "съдържание"):
                out.append(text.strip())
    return out


def pdf_headings(pdf: Path) -> str:
    """Normalised text of everything set larger than the body font."""
    import fitz

    with fitz.open(str(pdf)) as doc:
        sizes: dict[float, int] = {}
        spans: list[tuple[float, str]] = []
        for page in doc:
            for block in page.get_text("dict")["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = round(span["size"], 1)
                        sizes[size] = sizes.get(size, 0) + len(span["text"])
                        spans.append((size, span["text"]))
        if not sizes:
            return ""
        body = max(sizes, key=lambda s: sizes[s])
        return norm("".join(t for sz, t in spans if sz > body * 1.02))


PAIRS = [
    ("report_en.md", "{step}_report_en.pdf", ""),
    ("report_bg.md", "{step}_report_bg.pdf", ""),
    ("summary/summaryEn.md", "{step}_en.pdf", "summaries"),
    ("summary/summaryBg.md", "{step}_bg.pdf", "summaries"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundles", action="store_true")
    args = ap.parse_args()

    try:
        import fitz  # noqa: F401
    except ImportError:
        print("ERROR: PyMuPDF required (pip install pymupdf)", file=sys.stderr)
        sys.exit(1)

    missing_total = 0
    checked = 0

    if args.bundles:
        targets = []
        for pdf in sorted(glob.glob(str(REPO_ROOT / "deliverables/bundles/*.pdf"))):
            lang = "bg" if pdf.endswith("_bg.pdf") else "en"
            if "Reports" in pdf:
                srcs = sorted(glob.glob(str(REPORTS_DIR / f"step*/report_{lang}.md")))
            elif "Summaries" in pdf:
                name = "summaryEn.md" if lang == "en" else "summaryBg.md"
                srcs = sorted(glob.glob(str(REPORTS_DIR / f"step*/summary/{name}")))
            else:
                name = "onePager.md" if lang == "en" else "onePagerBg.md"
                srcs = sorted(glob.glob(str(REPORTS_DIR / f"step*/summary/{name}")))
            targets.append((Path(pdf), [Path(s) for s in srcs]))
    else:
        targets = []
        for step_dir in sorted(REPORTS_DIR.glob("step[0-9][0-9]")):
            step = step_dir.name
            for md_rel, pdf_pat, sub in PAIRS:
                md = step_dir / md_rel
                pdf = (REPO_ROOT / "deliverables" / sub / pdf_pat.format(step=step)
                       if sub else step_dir / pdf_pat.format(step=step))
                if md.exists() and pdf.exists():
                    targets.append((pdf, [md]))

    for pdf, srcs in targets:
        rendered = pdf_headings(pdf)
        missing = []
        for md in srcs:
            for h in source_headings(md):
                key = norm(h)[:24]
                if key and key not in rendered:
                    missing.append((md.name, h))
        checked += 1
        if missing:
            missing_total += len(missing)
            print(f"\n{pdf.relative_to(REPO_ROOT)}  — {len(missing)} heading(s) NOT typeset")
            for name, h in missing[:8]:
                print(f"   ✗ {name}: {h[:66]}")

    print(f"\n{checked} PDF(s) checked, {missing_total} missing heading(s).")
    sys.exit(1 if missing_total else 0)


if __name__ == "__main__":
    main()
