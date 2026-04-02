#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/build_pdf.py
#
# PURPOSE: Generate PDF study plans from the markdown source files in
#   deliverables/studyPlan/{en,bg}/ using pandoc.
#
#   Outputs:
#     deliverables/studyPlan/studyPlanEN.pdf
#     deliverables/studyPlan/studyPlanBG.pdf
#
# REQUIREMENTS:
#   pandoc >= 2.x   (available at: https://pandoc.org/installing.html)
#   A PDF engine: xelatex (via texlive-xetex) or weasyprint or wkhtmltopdf
#
#   On this system pandoc is at: /home/alexanderandreev/miniconda3/bin/pandoc
#   Check:  pandoc --version
#
# USAGE (run from repo root):
#   python3 scripts/build_pdf.py [--lang en] [--lang bg] [--engine xelatex]
# ---------------------------------------------------------------------------

import subprocess
import sys
import shutil
import argparse
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent.resolve()
STUDY_DIR   = REPO_ROOT / "deliverables" / "studyPlan"
OUTPUT_DIR  = STUDY_DIR  # PDFs go directly into deliverables/studyPlan/

# Ordered list of content files per language (metadata must come first)
CONTENT_FILES = [
    "00_metadata.yaml",
    "01_introduction.md",
    "02_phase_a.md",
    "03_phase_b.md",
    "04_phase_c.md",
    "05_phase_d.md",
    "06_phase_e.md",
    "07_phase_f.md",
    "08_phase_g.md",
    "09_glossary.md",
]

OUTPUT_NAMES = {
    "en": "studyPlanEN.pdf",
    "bg": "studyPlanBG.pdf",
}


def find_pandoc() -> str:
    """Locate pandoc, preferring the system PATH then miniconda."""
    if path := shutil.which("pandoc"):
        return path
    conda_pandoc = Path.home() / "miniconda3" / "bin" / "pandoc"
    if conda_pandoc.exists():
        return str(conda_pandoc)
    raise FileNotFoundError(
        "pandoc not found. Install it with:\n"
        "  conda install -c conda-forge pandoc\n"
        "or visit https://pandoc.org/installing.html"
    )


def build_pdf(lang: str, pdf_engine: str = "xelatex", pandoc_bin: str = "pandoc"):
    """Build a PDF for the given language."""
    lang_dir = STUDY_DIR / lang
    if not lang_dir.is_dir():
        print(f"ERROR: Language directory not found: {lang_dir}", file=sys.stderr)
        return False

    # Collect input files in order
    inputs: list[str] = []
    for filename in CONTENT_FILES:
        path = lang_dir / filename
        if path.exists():
            inputs.append(str(path))
        else:
            print(f"  WARNING: Missing {path.name} — skipping")

    if not inputs:
        print(f"ERROR: No input files found in {lang_dir}", file=sys.stderr)
        return False

    out_file = OUTPUT_DIR / OUTPUT_NAMES[lang]

    cmd = [
        pandoc_bin,
        "--pdf-engine", pdf_engine,
        "--toc",                    # table of contents
        "--toc-depth=2",
        "--number-sections",
        "-V", "geometry:margin=2.5cm",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.25",
        "-o", str(out_file),
        *inputs,
    ]

    # For BG: use a font that supports Cyrillic (if xelatex)
    if lang == "bg" and pdf_engine == "xelatex":
        cmd += ["-V", "mainfont=DejaVu Serif", "-V", "sansfont=DejaVu Sans"]

    print(f"\n[Building {OUTPUT_NAMES[lang]} ({lang.upper()})] ...")
    print(f"  Engine: {pdf_engine}")
    print(f"  Inputs: {len(inputs)} files")
    print(f"  Output: {out_file}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            size_kb = out_file.stat().st_size / 1024
            print(f"  ✓ Done ({size_kb:.0f} KB)")
            return True
        else:
            print(f"  ✗ pandoc error:\n{result.stderr}", file=sys.stderr)
            return False
    except FileNotFoundError:
        print(f"ERROR: Cannot run '{pandoc_bin}'. Is pandoc installed?", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Build PDF study plans from markdown.")
    parser.add_argument(
        "--lang", choices=["en", "bg", "both"], default="both",
        help="Language to build (default: both)"
    )
    parser.add_argument(
        "--engine", default="xelatex",
        help="PDF engine for pandoc (xelatex | pdflatex | weasyprint | wkhtmltopdf)"
    )
    args = parser.parse_args()

    try:
        pandoc_bin = find_pandoc()
        print(f"Found pandoc: {pandoc_bin}")
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    langs = ["en", "bg"] if args.lang == "both" else [args.lang]
    success = all(build_pdf(lang, pdf_engine=args.engine, pandoc_bin=pandoc_bin)
                  for lang in langs)
    if success:
        print(f"\nAll PDFs written to: {OUTPUT_DIR}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
