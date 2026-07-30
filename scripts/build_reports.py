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
#   deliverables/onePagers/stepNN_en.pdf        (from reports/stepNN/summary/onePager.md)
#   deliverables/onePagers/stepNN_bg.pdf        (from reports/stepNN/summary/onePagerBg.md)
#
# Bundles (--bundle) concatenate the per-step PDFs above into one file per
# type and language, with a PDF outline bookmark per step:
#   deliverables/bundles/allReports_{en,bg}.pdf
#   deliverables/bundles/allSummaries_{en,bg}.pdf
#   deliverables/bundles/allOnePagers_{en,bg}.pdf
#
# REQUIREMENTS:
#   pandoc >= 2.x   (https://pandoc.org/installing.html)
#   tectonic        (conda: conda install -c conda-forge tectonic)
#                   — xelatex (TeX Live / MiKTeX) is used as a fallback
#   A Cyrillic-capable serif font for BG PDFs (Liberation / DejaVu preferred;
#   the script falls back to whatever the system has — see resolve_fonts())
#   pypdf or PyMuPDF — only needed for --bundle
#
#   On this system tectonic is at: ~/miniconda3/bin/tectonic
#   Pandoc is at: ~/miniconda3/bin/pandoc
#
# USAGE (run from repo root):
#   python3 scripts/build_reports.py [--step 01] [--lang en|bg|both]
#                                    [--type report|summary|onepager|all]
#                                    [--bundle | --bundle-only]
# ---------------------------------------------------------------------------

import subprocess
import sys
import shutil
import argparse
import re
from pathlib import Path

REPO_ROOT     = Path(__file__).parent.parent.resolve()
REPORTS_DIR   = REPO_ROOT / "deliverables" / "reports"
SUMMARIES_DIR = REPO_ROOT / "deliverables" / "summaries"
ONEPAGERS_DIR = REPO_ROOT / "deliverables" / "onePagers"
BUNDLES_DIR   = REPO_ROOT / "deliverables" / "bundles"

# Discover available steps automatically
AVAILABLE_STEPS = sorted(p.name for p in REPORTS_DIR.iterdir() if p.is_dir())

# Bundles only ever cover the numbered stepNN/ directories, in order —
# other folders under reports/ (e.g. ruseMay/) are one-off deliverables.
STEP_DIR_RE = re.compile(r"^step\d{2}$")
BUNDLE_STEPS = sorted(s for s in AVAILABLE_STEPS if STEP_DIR_RE.match(s))

# Progressively tighter (fontsize, linestretch, margin) tried in order until a
# one-pager fits on a single page. See build_onepager().
ONEPAGER_FILTER = REPO_ROOT / "scripts" / "filters" / "onepager.lua"
ONEPAGER_FIT_LADDER = [
    ("11pt", "1.15", "2.0cm"),
    ("10pt", "1.05", "1.8cm"),
    ("10pt", "0.95", "1.5cm"),
    ("9pt",  "0.95", "1.5cm"),
    ("9pt",  "0.90", "1.3cm"),
]


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


# Cyrillic-capable families, best first. Liberation/DejaVu keep BG PDFs
# byte-identical to the Linux builds; the rest are Windows/macOS fallbacks so
# the BG side still builds on a machine without the metric-compatible fonts.
BG_SERIF_CANDIDATES = [
    "Liberation Serif", "DejaVu Serif", "FreeSerif", "Charis SIL",
    "Times New Roman", "Cambria", "Georgia",
]
BG_SANS_CANDIDATES = [
    "Liberation Sans", "DejaVu Sans", "FreeSans",
    "Arial", "Segoe UI", "Verdana",
]

_font_cache: dict[str, tuple[str, str]] = {}


def installed_font_families() -> set[str]:
    """Best-effort list of font family names installed on this system."""
    families: set[str] = set()

    if sys.platform == "win32":
        import winreg
        key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
        for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                with winreg.OpenKey(root, key_path) as key:
                    for i in range(winreg.QueryInfoKey(key)[1]):
                        name = winreg.EnumValue(key, i)[0]
                        # "Liberation Serif Bold Italic (TrueType)" → family stem
                        name = re.sub(r"\s*\((TrueType|OpenType)\)$", "", name)
                        for variant in name.split(" & "):
                            families.add(variant.strip())
            except OSError:
                continue
    else:
        try:
            out = subprocess.run(
                ["fc-list", "--format", "%{family}\\n"],
                capture_output=True, text=True, check=True,
            ).stdout
            for line in out.splitlines():
                for variant in line.split(","):
                    families.add(variant.strip())
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    return families


def resolve_fonts(lang: str) -> tuple[str, str] | None:
    """Pick an installed (serif, sans) pair that can render `lang`.

    Returns None for languages needing no special font (EN uses the LaTeX
    default) or when nothing suitable is installed, in which case pandoc is
    left to its own defaults rather than being handed a font that fails.
    """
    if lang != "bg":
        return None
    if lang in _font_cache:
        return _font_cache[lang]

    installed = installed_font_families()

    def pick(candidates: list[str]) -> str | None:
        for family in candidates:
            # Registry entries are per-style ("Georgia Bold"), so match the stem
            if any(f == family or f.startswith(family + " ") for f in installed):
                return family
        return None

    serif, sans = pick(BG_SERIF_CANDIDATES), pick(BG_SANS_CANDIDATES)
    if not serif or not sans:
        print(
            f"  ! No Cyrillic serif/sans pair found among "
            f"{BG_SERIF_CANDIDATES[:2]}; falling back to the engine default. "
            f"Install Liberation or DejaVu fonts for the canonical BG layout.",
            file=sys.stderr,
        )
        return None

    if serif not in ("Liberation Serif", "DejaVu Serif"):
        print(f"  ! BG fonts: using '{serif}' / '{sans}' (Liberation/DejaVu not installed)")

    _font_cache[lang] = (serif, sans)
    return serif, sans


def page_count(pdf_file: Path) -> int | None:
    """Page count of a built PDF, or None if no PDF library is installed."""
    try:
        from pypdf import PdfReader
    except ImportError:
        pass
    else:
        return len(PdfReader(str(pdf_file)).pages)

    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None
    with fitz.open(str(pdf_file)) as doc:
        return doc.page_count


def run_pandoc(
    input_file: Path,
    output_file: Path,
    lang: str,
    engine: str,
    pandoc_bin: str,
    extra_args: list[str] | None = None,
    geometry: str | None = None,
    number_offset: int = 0,
    toc: bool = True,
    number_sections: bool = True,
    fontsize: str = "11pt",
    linestretch: str = "1.25",
    quiet: bool = False,
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
        "-V", f"geometry:margin={margin}",
        "-V", f"fontsize={fontsize}",
        "-V", f"linestretch={linestretch}",
        "-o", str(output_file),
    ]

    if toc:
        cmd += ["--toc", "--toc-depth=2"]
    if number_sections:
        cmd += ["--number-sections", "-V", "secnumdepth=3"]

    # For Bulgarian: Cyrillic-capable fonts + lang flag for hyphenation/layout
    if lang == "bg":
        cmd += ["-V", "lang=bg"]
        if fonts := resolve_fonts(lang):
            serif, sans = fonts
            cmd += ["-V", f"mainfont={serif}", "-V", f"sansfont={sans}"]

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
            if not quiet:
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


def build_onepager(step: str, lang: str, engine: str, pandoc_bin: str) -> bool:
    """Build stepNN_en.pdf / stepNN_bg.pdf in deliverables/onePagers/."""
    summary_dir = REPORTS_DIR / step / "summary"
    md_file = summary_dir / ("onePager.md" if lang == "en" else "onePagerBg.md")
    pdf_file = ONEPAGERS_DIR / f"{step}_{lang}.pdf"

    if not md_file.exists():
        print(f"  SKIP: {md_file.relative_to(REPO_ROOT)} not found")
        return True

    print(f"  Building onePagers/{step}_{lang}.pdf ({lang.upper()}) ...")

    # A one-pager must fit on one page. Drop the TOC, the section numbering and
    # the duplicated title heading, then tighten the type one notch at a time
    # until it fits — BG runs ~20% longer than EN, so a single fixed size that
    # works for every step would leave the short ones needlessly cramped.
    for fontsize, linestretch, margin in ONEPAGER_FIT_LADDER:
        ok = run_pandoc(
            md_file, pdf_file, lang, engine, pandoc_bin,
            geometry=margin, toc=False, number_sections=False,
            fontsize=fontsize, linestretch=linestretch,
            extra_args=["--lua-filter", str(ONEPAGER_FILTER)],
            quiet=True,
        )
        if not ok:
            return False
        pages = page_count(pdf_file)
        if pages is None or pages <= 1:
            break
    else:
        print(f"    ! still {page_count(pdf_file)} pages at the tightest setting")

    size_kb = pdf_file.stat().st_size / 1024
    print(f"  ✓ Done ({size_kb:.0f} KB, {fontsize}/{margin}) → {pdf_file.relative_to(REPO_ROOT)}")
    return True


# --- Bundling ---------------------------------------------------------------

# type -> (per-step PDF path builder, bundle filename stem)
BUNDLE_TYPES = {
    "report":   (lambda step, lang: REPORTS_DIR / step / f"{step}_report_{lang}.pdf",
                 "allReports"),
    "summary":  (lambda step, lang: SUMMARIES_DIR / f"{step}_{lang}.pdf",
                 "allSummaries"),
    "onepager": (lambda step, lang: ONEPAGERS_DIR / f"{step}_{lang}.pdf",
                 "allOnePagers"),
}


def merge_pdfs(parts: list[tuple[str, Path]], output_file: Path) -> bool:
    """Concatenate `parts` [(bookmark_label, pdf_path), ...] into output_file.

    Adds one top-level outline bookmark per part so the bundle is navigable.
    Uses pypdf when present, else PyMuPDF; both are common enough that one is
    normally already installed.
    """
    try:
        from pypdf import PdfWriter
    except ImportError:
        pass
    else:
        writer = PdfWriter()
        for label, path in parts:
            page_index = len(writer.pages)
            writer.append(str(path))
            writer.add_outline_item(label, page_index)
        with open(output_file, "wb") as fh:
            writer.write(fh)
        return True

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print(
            "ERROR: bundling needs pypdf or PyMuPDF. Install one with:\n"
            "  pip install pypdf",
            file=sys.stderr,
        )
        return False

    out = fitz.open()
    toc = []
    for label, path in parts:
        page_index = out.page_count
        with fitz.open(str(path)) as src:
            out.insert_pdf(src)
        toc.append([1, label, page_index + 1])  # fitz page numbers are 1-based
    out.set_toc(toc)
    out.save(str(output_file))
    out.close()
    return True


def build_bundle(build_type: str, lang: str) -> bool:
    """Merge the already-built per-step PDFs of one type into a single file."""
    pdf_for_step, stem = BUNDLE_TYPES[build_type]
    output_file = BUNDLES_DIR / f"{stem}_{lang}.pdf"

    parts, missing = [], []
    for step in BUNDLE_STEPS:
        path = pdf_for_step(step, lang)
        if path.exists():
            parts.append((f"Step {int(step.replace('step', ''))}", path))
        else:
            missing.append(step)

    if not parts:
        print(f"  SKIP {output_file.name}: no {build_type} PDFs found for {lang.upper()}")
        return True

    print(f"  Bundling {len(parts)} {build_type} PDFs → {output_file.name} ...")
    if missing:
        print(f"    (no {lang.upper()} PDF for: {', '.join(missing)})")

    if not merge_pdfs(parts, output_file):
        return False

    size_kb = output_file.stat().st_size / 1024
    print(f"  ✓ Done ({size_kb:.0f} KB) → {output_file.relative_to(REPO_ROOT)}")
    return True


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
        choices=["report", "summary", "onepager", "all", "both"],
        default="all",
        help="Which document type(s) to build (default: all; 'both' = report+summary)",
    )
    parser.add_argument(
        "--bundle",
        action="store_true",
        help="Also merge the per-step PDFs into one bundle per type and language",
    )
    parser.add_argument(
        "--bundle-only",
        action="store_true",
        help="Skip the per-step builds and only re-merge existing PDFs",
    )
    args = parser.parse_args()

    langs = ["en", "bg"] if args.lang == "both" else [args.lang]
    types = {
        "all":  ["report", "summary", "onepager"],
        "both": ["report", "summary"],
    }.get(args.type, [args.type])

    for directory in (SUMMARIES_DIR, ONEPAGERS_DIR, BUNDLES_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    results = []

    if not args.bundle_only:
        try:
            pandoc_bin = find_pandoc()
            engine     = find_engine()
            print(f"pandoc : {pandoc_bin}")
            print(f"engine : {engine}")
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)

        builders = {
            "report":   build_report,
            "summary":  build_summary,
            "onepager": build_onepager,
        }
        for step in args.step:
            print(f"\n[Step {step}]")
            for build_type in types:
                for lang in langs:
                    results.append(builders[build_type](step, lang, engine, pandoc_bin))

    if args.bundle or args.bundle_only:
        print("\n[Bundles]")
        for build_type in types:
            for lang in langs:
                results.append(build_bundle(build_type, lang))

    if all(results):
        print("\nAll PDFs built successfully.")
    else:
        failed = results.count(False)
        print(f"\n{failed} build(s) failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
