#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/build_session_report.py
#
# PURPOSE: Build PDFs for the Ruse University academic session report
#   from deliverables/reports/ruseMay/
#
# Outputs:
#   deliverables/reports/ruseMay/report.pdf      (English)
#   deliverables/reports/ruseMay/report_bg.pdf   (Bulgarian)
#
# USAGE (run from repo root):
#   python3 scripts/build_session_report.py [--lang en|bg|both]
# ---------------------------------------------------------------------------

import argparse
import subprocess
import sys
import shutil
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent.resolve()
REPORT_DIR  = REPO_ROOT / "deliverables" / "reports" / "ruseMay"
METADATA    = REPORT_DIR / "metadata.yaml"


def find_pandoc() -> str:
    if path := shutil.which("pandoc"):
        return path
    conda_pandoc = Path.home() / "miniconda3" / "bin" / "pandoc"
    if conda_pandoc.exists():
        return str(conda_pandoc)
    raise FileNotFoundError("pandoc not found.")


def find_engine() -> str:
    conda_tectonic = Path.home() / "miniconda3" / "bin" / "tectonic"
    if conda_tectonic.exists():
        return str(conda_tectonic)
    if shutil.which("tectonic"):
        return "tectonic"
    if shutil.which("xelatex"):
        return "xelatex"
    raise FileNotFoundError("No suitable PDF engine found.")


def build(lang: str, pandoc_bin: str, engine: str) -> bool:
    if lang == "en":
        content = REPORT_DIR / "report.md"
        output  = REPORT_DIR / "report.pdf"
        extra   = []
    else:
        content = REPORT_DIR / "report_bg.md"
        output  = REPORT_DIR / "report_bg.pdf"
        extra   = [
            "-V", "lang=bg",
            "-V", "mainfont=Liberation Serif",
            "-V", "sansfont=Liberation Sans",
        ]

    if not content.exists():
        print(f"  SKIP: {content.name} not found")
        return True

    cmd = [
        pandoc_bin,
        str(METADATA),
        str(content),
        "--pdf-engine", engine,
        "--number-sections",
        "-V", "geometry:margin=2.5cm",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.25",
        "-o", str(output),
    ] + extra

    label = output.name
    print(f"\n[Building {label}] ...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPORT_DIR)
    if result.returncode == 0:
        size_kb = output.stat().st_size / 1024
        print(f"  Done ({size_kb:.0f} KB) → {output.relative_to(REPO_ROOT)}")
        return True
    else:
        errors = [
            line for line in result.stderr.splitlines()
            if not line.startswith("warning:")
        ]
        print(f"  pandoc error:\n" + "\n".join(errors), file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Build PDFs for the Ruse May session report."
    )
    parser.add_argument(
        "--lang",
        choices=["en", "bg", "both"],
        default="both",
        help="Language(s) to build (default: both)",
    )
    args = parser.parse_args()

    try:
        pandoc_bin = find_pandoc()
        engine = find_engine()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"pandoc : {pandoc_bin}")
    print(f"engine : {engine}")

    langs = ["en", "bg"] if args.lang == "both" else [args.lang]
    results = [build(lang, pandoc_bin, engine) for lang in langs]

    if not all(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
