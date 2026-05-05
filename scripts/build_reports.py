#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/build_reports.py
#
# OFFICIAL PhD TITLE (keep consistent across all documents):
#   EN: Research on the possibilities for applying Artificial Intelligence in computer games
#   BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
#
# PURPOSE: Generate PDFs for step implementation reports and summaries.
#   Mirrors the logic of scripts/build_pdf.py (used for the study plan).
#
# Outputs (for each step):
#   deliverables/reports/stepNN/report_en.pdf   (from report_en.md)
#   deliverables/reports/stepNN/report_bg.pdf   (from report_bg.md)
#   deliverables/summaries/stepNN_en.pdf        (from reports/stepNN/summary/summaryEn.md)
#   deliverables/summaries/stepNN_bg.pdf        (from reports/stepNN/summary/summaryBg.md)
#
# REQUIREMENTS:
#   pandoc >= 2.x   (https://pandoc.org/installing.html)
#   tectonic        (conda: conda install -c conda-forge tectonic)
#   DejaVu fonts    (provides Cyrillic support for BG PDFs)
#
#   On this system tectonic is at: ~/miniconda3/bin/tectonic
#   Pandoc is at: ~/miniconda3/bin/pandoc
#
# USAGE (run from repo root):
#   python3 scripts/build_reports.py [--step 01] [--lang en|bg|both]
#                                    [--type report|summary|both]
# ---------------------------------------------------------------------------

import subprocess
import sys
import shutil
import argparse
from pathlib import Path

REPO_ROOT    = Path(__file__).parent.parent.resolve()
REPORTS_DIR  = REPO_ROOT / "deliverables" / "reports"
SUMMARIES_DIR = REPO_ROOT / "deliverables" / "summaries"

# Discover available steps automatically
AVAILABLE_STEPS = sorted(p.name for p in REPORTS_DIR.iterdir() if p.is_dir())


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


def find_engine() -> str:
    """Locate a suitable PDF engine (tectonic preferred, then xelatex)."""
    # Try tectonic first (available via miniconda on this system)
    conda_tectonic = Path.home() / "miniconda3" / "bin" / "tectonic"
    if conda_tectonic.exists():
        return str(conda_tectonic)  # use absolute path so it works outside conda env
    if shutil.which("tectonic"):
        return "tectonic"
    if shutil.which("xelatex"):
        return "xelatex"
    raise FileNotFoundError(
        "No suitable PDF engine found. Install tectonic with:\n"
        "  conda install -c conda-forge tectonic\n"
        "or install xelatex via texlive-xetex."
    )


def run_pandoc(
    input_file: Path,
    output_file: Path,
    lang: str,
    engine: str,
    pandoc_bin: str,
    extra_args: list[str] | None = None,
    geometry: str | None = None,
    number_offset: int = 0,
) -> bool:
    """Run pandoc to convert a markdown file to PDF.
    
    number_offset: shifts section numbering so step N starts at N.1, N.2, etc.
                   e.g. number_offset=1 makes sections start at 2.x
    """
    # Use custom geometry if provided, otherwise use default
    margin = geometry if geometry else "2.5cm"
    
    cmd = [
        pandoc_bin,
        str(input_file),
        "--pdf-engine", engine,
        "--toc",
        "--toc-depth=3",
        "--number-sections",
        "-V", "secnumdepth=3",
        "-V", f"geometry:margin={margin}",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.25",
        "-o", str(output_file),
    ]

    # For Bulgarian: Liberation fonts + lang flag for proper hyphenation/layout
    if lang == "bg":
        cmd += [
            "-V", "lang=bg",
            "-V", "mainfont=Liberation Serif",
            "-V", "sansfont=Liberation Sans",
        ]

    # Inject LaTeX section counter offset (--number-offset is ignored for PDF engines)
    if number_offset > 0:
        cmd += ["-V", f"header-includes=\\setcounter{{section}}{{{number_offset}}}"]

    if extra_args:
        cmd += extra_args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=input_file.parent,   # resolve relative image paths from md location
        )
        if result.returncode == 0:
            size_kb = output_file.stat().st_size / 1024
            print(f"  ✓ Done ({size_kb:.0f} KB) → {output_file.relative_to(REPO_ROOT)}")
            return True
        else:
            # tectonic outputs warnings to stderr even on success; filter those
            errors = [
                line for line in result.stderr.splitlines()
                if not line.startswith("warning:")
            ]
            print(f"  ✗ pandoc error:\n" + "\n".join(errors), file=sys.stderr)
            return False
    except FileNotFoundError:
        print(f"ERROR: Cannot run '{pandoc_bin}'.", file=sys.stderr)
        return False


def build_report(step: str, lang: str, engine: str, pandoc_bin: str) -> bool:
    """Build report_en.pdf or report_bg.pdf for a given step."""
    step_dir = REPORTS_DIR / step
    suffix = "en" if lang == "en" else "bg"
    md_file = step_dir / f"report_{suffix}.md"
    pdf_file = step_dir / f"{step}_report_{suffix}.pdf"

    if not md_file.exists():
        print(f"  SKIP: {md_file.relative_to(REPO_ROOT)} not found")
        return True  # not an error — step may not have BG report yet

    print(f"  Building {step}_report_{suffix}.pdf for step {step} ({lang.upper()}) ...")
    return run_pandoc(md_file, pdf_file, lang, engine, pandoc_bin)


def build_summary(step: str, lang: str, engine: str, pandoc_bin: str) -> bool:
    """Build stepNN_en.pdf or stepNN_bg.pdf in deliverables/summaries/."""
    step_dir = REPORTS_DIR / step
    summary_dir = step_dir / "summary"
    suffix = "En" if lang == "en" else "Bg"
    md_file = summary_dir / f"summary{suffix}.md"
    pdf_file = SUMMARIES_DIR / f"{step}_{lang}.pdf"

    if not md_file.exists():
        print(f"  SKIP: {md_file.relative_to(REPO_ROOT)} not found")
        return True

    print(f"  Building {step}_{lang}.pdf ({lang.upper()}) ...")
    # Extract step number for section numbering offset (step01 → 0, step02 → 1, etc.)
    # so pandoc generates 1.x for step01, 2.x for step02, 3.x for step03...
    step_num = int(step.replace("step", ""))
    offset = step_num - 1
    return run_pandoc(md_file, pdf_file, lang, engine, pandoc_bin,
                      geometry="2.0cm", number_offset=offset)


def main():
    parser = argparse.ArgumentParser(
        description="Build PDFs for step implementation reports and summaries."
    )
    parser.add_argument(
        "--step",
        nargs="+",
        default=AVAILABLE_STEPS,
        help=f"Step(s) to build (default: all discovered — {AVAILABLE_STEPS})",
    )
    parser.add_argument(
        "--lang",
        choices=["en", "bg", "both"],
        default="both",
        help="Language(s) to build (default: both)",
    )
    parser.add_argument(
        "--type",
        choices=["report", "summary", "both"],
        default="both",
        help="Whether to build reports, summaries, or both (default: both)",
    )
    args = parser.parse_args()

    try:
        pandoc_bin = find_pandoc()
        engine     = find_engine()
        print(f"pandoc : {pandoc_bin}")
        print(f"engine : {engine}")
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    langs   = ["en", "bg"] if args.lang == "both" else [args.lang]
    types   = ["report", "summary"] if args.type == "both" else [args.type]
    results = []

    for step in args.step:
        print(f"\n[Step {step}]")
        for build_type in types:
            for lang in langs:
                if build_type == "report":
                    ok = build_report(step, lang, engine, pandoc_bin)
                else:
                    ok = build_summary(step, lang, engine, pandoc_bin)
                results.append(ok)

    if all(results):
        print("\nAll PDFs built successfully.")
    else:
        failed = results.count(False)
        print(f"\n{failed} build(s) failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
