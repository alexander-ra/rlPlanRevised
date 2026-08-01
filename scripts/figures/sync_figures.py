#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/sync_figures.py
#
# PURPOSE: Put each generated *_bg.png wherever its English twin already sits,
#   and repoint the Bulgarian markdown at it.
#
#   The plotting scripts write into their own output directories; the reports
#   reference figures/, and the summaries keep a flat byte-identical copy of the
#   same file. There is no existing copy helper - those duplicates were placed
#   by hand - so this walks the English figures and mirrors each BG variant to
#   the same places.
#
#   A figure with no BG variant keeps pointing at the English file. That is the
#   agreed outcome for the textbook image and for the scripts that were not
#   re-run.
#
# USAGE (run from repo root):
#   python scripts/figures/sync_figures.py --dry-run
#   python scripts/figures/sync_figures.py
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import glob
import re
import shutil
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
REPORTS = REPO_ROOT / "deliverables" / "reports"
IMG = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)(\s*(?:\"[^\"]*\")?\))")


def bg_sources() -> dict[str, Path]:
    """filename -> newest generated *_bg.png anywhere in the repo."""
    found: dict[str, Path] = {}
    for f in glob.glob(str(REPO_ROOT / "**" / "*_bg.png"), recursive=True):
        p = Path(f)
        if ".venv" in p.parts:
            continue
        prev = found.get(p.name)
        if prev is None or p.stat().st_mtime > prev.stat().st_mtime:
            found[p.name] = p
    return found


def bg_docs() -> list[Path]:
    return [Path(p) for p in
            glob.glob(str(REPORTS / "step*/report_bg.md"))
            + glob.glob(str(REPORTS / "step*/summary/summaryBg.md"))
            + glob.glob(str(REPORTS / "step*/summary/onePagerBg.md"))]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sources = bg_sources()
    print(f"generated BG figures found: {len(sources)}")

    # 1. place each _bg.png beside every copy of its English twin
    copied = 0
    targets: dict[str, list[Path]] = defaultdict(list)
    for eng in glob.glob(str(REPORTS / "step*/**/*.png"), recursive=True):
        p = Path(eng)
        if p.stem.endswith("_bg"):
            continue
        bg_name = f"{p.stem}_bg{p.suffix}"
        src = sources.get(bg_name)
        if src is None:
            continue
        dest = p.with_name(bg_name)
        targets[bg_name].append(dest)
        if dest.resolve() == src.resolve():
            continue
        if dest.exists() and dest.read_bytes() == src.read_bytes():
            continue
        if not args.dry_run:
            shutil.copy2(src, dest)
        copied += 1

    print(f"copies placed beside their English twin: {copied}")

    # 2. repoint the BG markdown at the _bg variant, where one exists
    rewritten = 0
    reverted = 0
    files_touched = 0
    for md in bg_docs():
        text = md.read_text(encoding="utf-8")

        def repl(m: re.Match) -> str:
            nonlocal rewritten, reverted
            path = m.group(2)
            if path.startswith("http"):
                return m.group(0)
            target = md.parent / path
            if Path(path).stem.endswith("_bg"):
                # Already localised. If the file is gone the reproducibility
                # gate removed it, so point back at the English original rather
                # than leave a reference to a file that does not exist.
                if target.exists():
                    return m.group(0)
                english = Path(path).with_name(
                    Path(path).name.replace("_bg", "", 1))
                if not (md.parent / english).exists():
                    return m.group(0)
                reverted += 1
                return f"{m.group(1)}{str(english).replace(chr(92), '/')}{m.group(3)}"
            candidate = target.parent / f"{Path(path).stem}_bg{Path(path).suffix}"
            if not candidate.exists():
                return m.group(0)          # no BG variant: keep English
            rewritten += 1
            new = str(Path(path).with_name(candidate.name)).replace("\\", "/")
            return f"{m.group(1)}{new}{m.group(3)}"

        out = IMG.sub(repl, text)
        if out != text:
            files_touched += 1
            if not args.dry_run:
                md.write_text(out, encoding="utf-8")

    print(f"markdown image references repointed: {rewritten} "
          f"in {files_touched} file(s)")
    if reverted:
        print(f"reverted to English (BG variant removed by the gate): {reverted}")
    if args.dry_run:
        print("[dry-run] nothing written")


if __name__ == "__main__":
    main()
