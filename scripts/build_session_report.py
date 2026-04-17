#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/build_session_report.py
#
# PURPOSE: Build PDF for the Ruse University academic session report
#   from deliverables/reports/ruseMay/
#
# Outputs:
#   deliverables/reports/ruseMay/report.pdf
#
# USAGE (run from repo root):
#   python3 scripts/build_session_report.py
# ---------------------------------------------------------------------------

import subprocess
import sys
import shutil
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent.resolve()
REPORT_DIR  = REPO_ROOT / "deliverables" / "reports" / "ruseMay"
METADATA    = REPORT_DIR / "metadata.yaml"
CONTENT     = REPORT_DIR / "report.md"
OUTPUT      = REPORT_DIR / "report.pdf"


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


def main():
    try:
        pandoc_bin = find_pandoc()
        engine = find_engine()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"pandoc : {pandoc_bin}")
    print(f"engine : {engine}")

    cmd = [
        pandoc_bin,
        str(METADATA),
        str(CONTENT),
        "--pdf-engine", engine,
        "--number-sections",
        "-V", "geometry:margin=2.5cm",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.25",
        "-o", str(OUTPUT),
    ]

    print(f"\n[Building report.pdf] ...")
    print(f"  Output: {OUTPUT}")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPORT_DIR)
    if result.returncode == 0:
        size_kb = OUTPUT.stat().st_size / 1024
        print(f"  Done ({size_kb:.0f} KB)")
    else:
        errors = [
            line for line in result.stderr.splitlines()
            if not line.startswith("warning:")
        ]
        print(f"  pandoc error:\n" + "\n".join(errors), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
