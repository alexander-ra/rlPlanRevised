#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/read_pdf_comments.py
#
# PURPOSE: Extract review comments (Acrobat / any PDF annotations) from the
#   built deliverables, so a proofreading pass done in a PDF reader can be
#   acted on against the markdown sources.
#
#   Reads sticky notes, highlights, underlines, strikeouts and free text.
#   For markup annotations it also reports the text that was marked, which is
#   what makes a comment locatable in the .md source.
#
# REQUIREMENTS: PyMuPDF  (pip install pymupdf)
#
# USAGE (run from repo root):
#   python scripts/read_pdf_comments.py                       # all bundles
#   python scripts/read_pdf_comments.py path/to/file.pdf ...  # specific files
#   python scripts/read_pdf_comments.py --json comments.json  # machine-readable
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()


def extract(pdf_path: Path) -> list[dict]:
    import fitz  # PyMuPDF

    out: list[dict] = []
    with fitz.open(str(pdf_path)) as doc:
        for pno, page in enumerate(doc, start=1):
            for annot in page.annots() or []:
                info = annot.info
                # For highlights/strikeouts the useful anchor is the text under
                # the annotation, not the comment - that is what identifies the
                # spot in the markdown.
                marked = ""
                if annot.type[1] in ("Highlight", "StrikeOut", "Underline", "Squiggly"):
                    marked = " ".join(page.get_textbox(annot.rect).split())
                out.append({
                    "file": pdf_path.name,
                    "page": pno,
                    "type": annot.type[1],
                    "author": info.get("title", ""),
                    "comment": (info.get("content") or "").strip(),
                    "marked_text": marked,
                })
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Extract review comments from built PDFs.")
    ap.add_argument("pdfs", nargs="*", help="PDFs to read (default: all bundles)")
    ap.add_argument("--json", metavar="FILE", help="also write results as JSON")
    args = ap.parse_args()

    try:
        import fitz  # noqa: F401
    except ImportError:
        print("ERROR: PyMuPDF is required.\n  pip install pymupdf", file=sys.stderr)
        sys.exit(1)

    paths = [Path(p) for p in args.pdfs] or [
        Path(p) for p in sorted(glob.glob(str(REPO_ROOT / "deliverables/bundles/*.pdf")))
    ]
    paths = [p for p in paths if p.exists()]
    if not paths:
        print("No PDFs found.", file=sys.stderr)
        sys.exit(1)

    all_comments: list[dict] = []
    for p in paths:
        comments = extract(p)
        all_comments += comments
        if not comments:
            continue
        print(f"\n{p.relative_to(REPO_ROOT) if REPO_ROOT in p.parents else p} "
              f"— {len(comments)} comment(s)")
        for c in comments:
            who = f" [{c['author']}]" if c["author"] else ""
            print(f"  p{c['page']:<4} {c['type']:<10}{who}")
            if c["marked_text"]:
                print(f"        marked : {c['marked_text'][:100]}")
            if c["comment"]:
                print(f"        comment: {c['comment']}")

    print(f"\n{len(all_comments)} comment(s) across {len(paths)} file(s).")
    if args.json:
        Path(args.json).write_text(
            json.dumps(all_comments, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"JSON written to {args.json}")


if __name__ == "__main__":
    main()
