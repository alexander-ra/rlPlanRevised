#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/render_printed.py
#
# PURPOSE: Show each figure the way a reader sees it - cropped out of the built
#   PDF together with its caption, at a fixed print scale. Judging legibility
#   from the source PNG is misleading: the same file can be crisp at half a
#   page and unreadable at a third. The caption is included on purpose, as a
#   body-size reference - a label much smaller than the caption text is too
#   small.
#
#   Writes <out>/<chapter>/p<page>_f<n>.png plus manifest.json recording, per
#   figure: page, printed width in cm, source pixel size, effective ppi, and the
#   caption text.
#
# USAGE (run from repo root):
#   python scripts/figures/render_printed.py                       # BG summaries, all chapters
#   python scripts/figures/render_printed.py --chapter 7
#   python scripts/figures/render_printed.py --pdf deliverables/bundles/allSummaries_en.pdf
#   python scripts/figures/render_printed.py --pages               # also full pages
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import fitz

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
DEFAULT_PDF = REPO_ROOT / "deliverables" / "bundles" / "allSummaries_bg.pdf"
DEFAULT_OUT = REPO_ROOT / "deliverables" / "finalReview" / "renders"

DPI = 150            # print scale: 1 pt of type = DPI/72 px
PAGE_DPI = 110       # full pages, for layout checks only
CAPTION_RE = re.compile(r"^\s*(Фигура|Figure)\s+\d+", re.IGNORECASE)
CHAPTER_RE = re.compile(r"(Глава|Chapter)\s+(\d+)")


def chapter_ranges(doc: fitz.Document) -> dict[int, tuple[int, int]]:
    """Map chapter number -> (first, last) 0-based page, from level-1 bookmarks."""
    starts = []
    for level, title, page in doc.get_toc():
        m = CHAPTER_RE.search(title)
        if level == 1 and m:
            starts.append((int(m.group(2)), page - 1))
    ranges = {}
    for i, (num, first) in enumerate(starts):
        last = starts[i + 1][1] - 1 if i + 1 < len(starts) else doc.page_count - 1
        ranges[num] = (first, last)
    return ranges


def caption_below(page: fitz.Page, rect: fitz.Rect) -> tuple[fitz.Rect | None, str]:
    """The caption block directly under a figure, if there is one."""
    blocks = sorted(page.get_text("blocks"), key=lambda b: b[1])
    start = None
    for i, (x0, y0, x1, y1, text, *_) in enumerate(blocks):
        if y0 >= rect.y1 - 2 and y0 - rect.y1 < 40 and CAPTION_RE.match(text):
            start = i
            break
    if start is None:
        return None, ""
    # a caption can span several blocks; take those that follow without a gap
    cap = fitz.Rect(blocks[start][:4])
    texts = [blocks[start][4]]
    for x0, y0, x1, y1, text, *_ in blocks[start + 1:]:
        if y0 - cap.y1 > 9:
            break
        cap |= fitz.Rect(x0, y0, x1, y1)
        texts.append(text)
    return cap, " ".join(" ".join(texts).split())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--chapter", type=int, action="append",
                    help="chapter number (repeatable); default all")
    ap.add_argument("--pages", action="store_true", help="also render full pages")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    ranges = chapter_ranges(doc)
    chapters = args.chapter or sorted(ranges)
    manifest = {}
    for ch in chapters:
        first, last = ranges[ch]
        outdir = args.out / f"ch{ch:02d}"
        outdir.mkdir(parents=True, exist_ok=True)
        figs = []
        for pno in range(first, last + 1):
            page = doc[pno]
            if args.pages:
                page.get_pixmap(dpi=PAGE_DPI).save(outdir / f"page_p{pno + 1:03d}.png")
            for n, info in enumerate(page.get_image_info(xrefs=True), 1):
                rect = fitz.Rect(info["bbox"])
                if rect.width < 60 or rect.height < 40:      # icons, rules
                    continue
                cap_rect, cap_text = caption_below(page, rect)
                clip = rect | cap_rect if cap_rect else fitz.Rect(rect)
                clip = (clip + (-6, -6, 6, 6)) & page.rect
                name = f"p{pno + 1:03d}_f{n}.png"
                page.get_pixmap(dpi=DPI, clip=clip).save(outdir / name)
                src_w = info.get("width") or 0
                width_in = rect.width / 72
                figs.append({
                    "file": f"ch{ch:02d}/{name}",
                    "page": pno + 1,
                    "printed_width_cm": round(width_in * 2.54, 1),
                    "source_px": [info.get("width"), info.get("height")],
                    "effective_ppi": round(src_w / width_in) if src_w else None,
                    "caption": cap_text,
                })
        manifest[f"ch{ch:02d}"] = {"pages": [first + 1, last + 1], "figures": figs}
        print(f"chapter {ch:2d}: pages {first + 1}-{last + 1}, {len(figs)} figures")

    args.out.mkdir(parents=True, exist_ok=True)
    mpath = args.out / "manifest.json"
    old = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {}
    old.update(manifest)
    mpath.write_text(json.dumps(old, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
