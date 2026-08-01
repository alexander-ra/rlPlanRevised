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
# TOC-less renders used only for bundling; cached, not a deliverable.
BUNDLE_PARTS_DIR = BUNDLES_DIR / ".parts"

# Discover available steps automatically
AVAILABLE_STEPS = sorted(p.name for p in REPORTS_DIR.iterdir() if p.is_dir())

# Bundles only ever cover the numbered stepNN/ directories, in order —
# other folders under reports/ (e.g. ruseMay/) are one-off deliverables.
STEP_DIR_RE = re.compile(r"^step\d{2}$")
BUNDLE_STEPS = sorted(s for s in AVAILABLE_STEPS if STEP_DIR_RE.match(s))

# Progressively tighter (fontsize, linestretch, margin) tried in order until a
# one-pager fits on a single page. See build_onepager().
ONEPAGER_FILTER = REPO_ROOT / "scripts" / "filters" / "onepager.lua"
# Routes characters the body fonts lack to a font that has them. Without it
# XeLaTeX drops them silently and the reader sees a gap, not a warning.
GLYPH_FALLBACK = REPO_ROOT / "scripts" / "glyph_fallback.tex"
# Float parameters. Without these a heading between figures can go untypeset.
FLOAT_LAYOUT = REPO_ROOT / "scripts" / "float_layout.tex"
# Makes pagestyle=empty stick even on a page \maketitle marked as `plain`.
NO_PAGE_NUMBERS = REPO_ROOT / "scripts" / "no_page_numbers.tex"
# Bundle parts only: strips a hand-written Contents section from the markdown.
BUNDLE_PART_FILTER = REPO_ROOT / "scripts" / "filters" / "bundle_part.lua"
# Prints a repeated citation once, then points back at that number.
DEDUPE_FOOTNOTES = REPO_ROOT / "scripts" / "filters" / "dedupe_footnotes.lua"
ONEPAGER_FIT_LADDER = [
    ("11pt", "1.15", "2.0cm"),
    ("10pt", "1.05", "1.8cm"),
    ("10pt", "0.95", "1.5cm"),
    ("9pt",  "0.95", "1.5cm"),
    ("9pt",  "0.90", "1.3cm"),
    # The last two rungs exist for the densest BG one-pagers (steps 11-12) under
    # PT Serif, which sets wider than the Times-metric fonts the ladder was
    # first tuned against.
    ("8.5pt", "0.88", "1.2cm"),
    ("8pt",   "0.85", "1.1cm"),
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


# Cyrillic-capable families, best first.
#
# PT Serif / PT Sans lead deliberately: ParaType drew them for Cyrillic rather
# than extending a Latin face, so the Bulgarian sets the colour of the page
# instead of looking like an afterthought. Install with:
#     mpm --install=paratype        (MiKTeX)
#     tlmgr install paratype        (TeX Live)
# Liberation and DejaVu follow as metric-compatible / always-present fallbacks;
# the tail exists so the BG side still builds on a bare machine.
BG_SERIF_CANDIDATES = [
    "PT Serif", "Liberation Serif", "DejaVu Serif", "FreeSerif", "Charis SIL",
    "Times New Roman", "Cambria", "Georgia",
]
BG_SANS_CANDIDATES = [
    "PT Sans", "Liberation Sans", "DejaVu Sans", "FreeSans",
    "Arial", "Segoe UI", "Verdana",
]
# The default LaTeX monospace (lmmono10) has NO Cyrillic, so every Cyrillic
# character inside a `code span` silently vanished from the BG PDFs. Any
# monospace chosen here must cover Cyrillic.
# DejaVu Sans Mono leads rather than PT Mono, which would match PT Serif/PT Sans
# stylistically: PT Mono has no combining tilde, so `R̃_t = Q̃_ν(...)` in the
# step 12 reports lost its diacritics. A monospace face is a different family
# from the body text anyway, so coverage wins over the family match.
BG_MONO_CANDIDATES = [
    "DejaVu Sans Mono", "PT Mono", "Liberation Mono", "FreeMono",
    "Consolas", "Courier New",
]

_font_cache: dict[str, tuple[str, str]] = {}

# Families that live in the TeX tree rather than in the OS font list. XeTeX
# finds them; the Windows registry and fc-list do not, so probing only the OS
# would silently downgrade a machine that has the better font installed.
# Each value is a file kpsewhich can resolve when the family is present.
TEX_TREE_FONTS = {
    "PT Serif": "PTF55F.pfb",       # paratype, Type1
    "PT Sans": "PTN57F.pfb",
    "PT Mono": "PTM55F.pfb",
    "DejaVu Serif": "DejaVuSerif.ttf",
    "DejaVu Sans": "DejaVuSans.ttf",
    "DejaVu Sans Mono": "DejaVuSansMono.ttf",
}


def tex_tree_families() -> set[str]:
    """Families installed as TeX packages, found via kpsewhich."""
    if not shutil.which("kpsewhich"):
        return set()
    found = set()
    for family, probe in TEX_TREE_FONTS.items():
        try:
            r = subprocess.run(["kpsewhich", probe], capture_output=True,
                               text=True, timeout=20)
            if r.returncode == 0 and r.stdout.strip():
                found.add(family)
        except (subprocess.SubprocessError, OSError):
            continue
    return found


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


def resolve_fonts(lang: str) -> tuple[str, str, str | None] | None:
    """Pick an installed (serif, sans, mono) set that can render `lang`.

    Returns None for languages needing no special font (EN uses the LaTeX
    default) or when nothing suitable is installed, in which case pandoc is
    left to its own defaults rather than being handed a font that fails.
    """
    if lang != "bg":
        return None
    if lang in _font_cache:
        return _font_cache[lang]

    installed = installed_font_families()
    from_tex = tex_tree_families()

    def pick(candidates: list[str]) -> str | None:
        for family in candidates:
            if family in from_tex:
                return family
            # Registry entries are per-style ("Georgia Bold"), so match the stem
            if any(f == family or f.startswith(family + " ") for f in installed):
                return family
        return None

    serif, sans = pick(BG_SERIF_CANDIDATES), pick(BG_SANS_CANDIDATES)
    mono = pick(BG_MONO_CANDIDATES)
    if not serif or not sans:
        print(
            f"  ! No Cyrillic serif/sans pair found among "
            f"{BG_SERIF_CANDIDATES[:2]}; falling back to the engine default. "
            f"Install Liberation or DejaVu fonts for the canonical BG layout.",
            file=sys.stderr,
        )
        return None

    if serif != BG_SERIF_CANDIDATES[0]:
        print(f"  ! BG fonts: using '{serif}' / '{sans}' "
              f"('{BG_SERIF_CANDIDATES[0]}' not installed - see BG_SERIF_CANDIDATES)")
    if not mono:
        print("  ! No Cyrillic monospace found; code spans containing Cyrillic "
              "will not render. Install DejaVu: mpm --install=dejavu",
              file=sys.stderr)

    _font_cache[lang] = (serif, sans, mono)
    return serif, sans, mono


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
    footnote_offset: int = 0,
    toc: bool = True,
    number_sections: bool = True,
    fontsize: str = "11pt",
    linestretch: str = "1.25",
    pagestyle: str | None = None,
    quiet: bool = False,
) -> bool:
    """Run pandoc to convert a markdown file to PDF.

    number_offset: shifts section numbering so step N starts at N.1, N.2, etc.
                   e.g. number_offset=1 makes sections start at 2.x
    footnote_offset: starts footnote numbering at N+1. Each bundle part is
                   compiled on its own, so without this every chapter restarts
                   its notes at 1; the bundle wants one continuous run.
    pagestyle:     LaTeX page style. "empty" suppresses the footer entirely,
                   which is what a bundle part wants: its own numbering would
                   restart at 1 inside the merged document. merge_pdfs() stamps
                   continuous numbers instead.
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
    if pagestyle:
        cmd += ["-V", f"pagestyle={pagestyle}"]
        if pagestyle == "empty" and NO_PAGE_NUMBERS.exists():
            cmd += ["--include-in-header", str(NO_PAGE_NUMBERS)]

    # For Bulgarian: Cyrillic-capable fonts + lang flag for hyphenation/layout
    if lang == "bg":
        cmd += ["-V", "lang=bg"]
        if fonts := resolve_fonts(lang):
            serif, sans, mono = fonts
            cmd += ["-V", f"mainfont={serif}", "-V", f"sansfont={sans}"]
            if mono:
                cmd += ["-V", f"monofont={mono}"]

    for preamble in (GLYPH_FALLBACK, FLOAT_LAYOUT):
        if preamble.exists():
            cmd += ["--include-in-header", str(preamble)]

    if DEDUPE_FOOTNOTES.exists():
        cmd += ["--lua-filter", str(DEDUPE_FOOTNOTES)]

    # Inject LaTeX section counter offset (--number-offset is ignored for PDF engines)
    if number_offset > 0:
        cmd += ["-V", f"header-includes=\\setcounter{{section}}{{{number_offset}}}"]
    if footnote_offset > 0:
        cmd += ["-V", f"header-includes=\\setcounter{{footnote}}{{{footnote_offset}}}"]

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


def report_opts(step: str) -> dict:
    """Pandoc options for a step report. Shared by the standalone PDF and the
    bundle part, so the two cannot drift apart."""
    return {}


def summary_opts(step: str) -> dict:
    """Pandoc options for a step summary.

    number_offset shifts section numbering so step N starts at N.1 - which also
    makes the numbers unique once the steps are merged into one bundle.
    """
    return {"geometry": "2.0cm", "number_offset": int(step.replace("step", "")) - 1}


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
    return run_pandoc(md_file, pdf_file, lang, engine, pandoc_bin,
                      **report_opts(step))


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
    return run_pandoc(md_file, pdf_file, lang, engine, pandoc_bin,
                      **summary_opts(step))


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
            fontsize=fontsize, linestretch=linestretch, pagestyle="empty",
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

# type -> (per-step PDF path builder, bundle filename stem, source md builder)
BUNDLE_TYPES = {
    "report": (
        lambda step, lang: REPORTS_DIR / step / f"{step}_report_{lang}.pdf",
        "allReports",
        lambda step, lang: REPORTS_DIR / step / f"report_{lang}.md",
    ),
    "summary": (
        lambda step, lang: SUMMARIES_DIR / f"{step}_{lang}.pdf",
        "allSummaries",
        lambda step, lang: REPORTS_DIR / step / "summary" /
                           ("summaryEn.md" if lang == "en" else "summaryBg.md"),
    ),
    "onepager": (
        lambda step, lang: ONEPAGERS_DIR / f"{step}_{lang}.pdf",
        "allOnePagers",
        lambda step, lang: REPORTS_DIR / step / "summary" /
                           ("onePager.md" if lang == "en" else "onePagerBg.md"),
    ),
}

BUNDLE_TITLES = {
    ("report", "en"):   "All Chapter Reports",
    ("report", "bg"):   "Доклади по глави",
    ("summary", "en"):  "All Chapter Summaries",
    ("summary", "bg"):  "Обобщения по глави",
    ("onepager", "en"): "All Chapter One-Pagers",
    ("onepager", "bg"): "Резюмета по глави",
}
CONTENTS_HEADING = {"en": "Contents", "bg": "Съдържание"}
PREFACE_HEADING = {"en": "Preface", "bg": "Предговор"}

# Official PhD title, kept identical across every document in the repo.
OFFICIAL_TITLE = {
    "en": "Research on the possibilities for applying Artificial Intelligence "
          "in computer games",
    "bg": "Изследване на възможностите за приложение на изкуствения интелект "
          "в компютърни игри",
}
BUNDLE_AUTHOR = {"en": "Alexander Andreev", "bg": "Александър Андреев"}
BUNDLE_DATE = {"en": "July 2026", "bg": "Юли 2026"}

# The preface is the study plan's introduction, reused verbatim.
def preface_source(lang: str) -> Path:
    return REPO_ROOT / "deliverables" / "studyPlan" / lang / "01_introduction.md"


def build_title_pdf(build_type: str, lang: str, out_file: Path,
                    engine: str, pandoc_bin: str) -> bool:
    """A title page for the bundle."""
    body = "\n".join([
        r"\thispagestyle{empty}",
        r"\begin{center}",
        r"\vspace*{5cm}",
        rf"{{\Huge\bfseries {latex_escape(BUNDLE_TITLES[(build_type, lang)])}}}\par",
        r"\vspace{2cm}",
        r"\rule{0.7\textwidth}{0.4pt}\par",
        r"\vspace{1.2cm}",
        rf"{{\large {latex_escape(OFFICIAL_TITLE[lang])}}}\par",
        r"\vspace{4cm}",
        rf"{{\large {latex_escape(BUNDLE_AUTHOR[lang])}}}\par",
        r"\vspace{0.6cm}",
        rf"{{{latex_escape(BUNDLE_DATE[lang])}}}\par",
        r"\vfill",
        r"\end{center}",
    ])
    md_file = out_file.with_suffix(".title.md")
    md_file.write_text(f"```{{=latex}}\n{body}\n```\n", encoding="utf-8")
    ok = run_pandoc(md_file, out_file, lang, engine, pandoc_bin,
                    geometry="2.5cm", toc=False, number_sections=False,
                    pagestyle="empty", quiet=True)
    md_file.unlink(missing_ok=True)
    return ok


def build_preface_pdf(lang: str, out_file: Path,
                      engine: str, pandoc_bin: str) -> bool:
    """Render the study-plan introduction as the bundle's preface.

    The source carries glossary cross-references - superscript indices like
    ^15^ and inline <sup class="gl"> markers - that point at a glossary living
    at the end of the study plan. There is no glossary in a bundle, so the
    references are stripped rather than left dangling.
    """
    src = preface_source(lang)
    if not src.exists():
        print(f"    ! no preface source at {src.relative_to(REPO_ROOT)}")
        return False

    text = src.read_text(encoding="utf-8")
    text = re.sub(r"<sup[^>]*>.*?</sup>", "", text)      # glossary markers
    text = re.sub(r"\^\d+\^", "", text)                  # superscript indices
    # the note explaining those indices is now pointless
    text = re.sub(r"^>\s*\*.*?(Речника|Glossary).*?\*\s*$", "", text, flags=re.M)
    # replace the study-plan title block with a preface heading
    text = re.sub(r"\A(.*?)(?=^##\s)", "", text, flags=re.S | re.M)
    text = f"# {PREFACE_HEADING[lang]}\n\n" + text
    text = re.sub(r"\n{3,}", "\n\n", text)

    md_file = out_file.with_suffix(".preface.md")
    md_file.write_text(text, encoding="utf-8")
    ok = run_pandoc(md_file, out_file, lang, engine, pandoc_bin,
                    geometry="2.5cm", toc=False, number_sections=False,
                    pagestyle="empty", quiet=True)
    md_file.unlink(missing_ok=True)
    return ok


def doc_title(md_file: Path, fallback: str) -> str:
    """Title of a source document: YAML `title:`, else its first H1."""
    if not md_file.exists():
        return fallback
    text = md_file.read_text(encoding="utf-8")
    if m := re.search(r'^title:\s*"(.+?)"', text, re.M):
        return m.group(1)
    if m := re.search(r"^#\s+(.+)$", text, re.M):
        return m.group(1).strip()
    return fallback


def latex_escape(s: str) -> str:
    """Escape a heading for use inside raw LaTeX in the contents page."""
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    return s


def build_toc_pdf(entries: list[tuple[int, str, int]], lang: str, heading: str,
                  out_file: Path, engine: str, pandoc_bin: str) -> bool:
    """Render the bundle's contents pages.

    `entries` is the merged section outline of every document in the bundle,
    as (level, title, page-in-bundle). Emitted as raw LaTeX so the entries get
    real dotted leaders and can flow across as many pages as they need.
    """
    lines = [r"\begin{flushleft}",
             rf"{{\Large\bfseries {latex_escape(CONTENTS_HEADING[lang])}}}\par",
             r"\vspace{1.2em}"]
    # Level 1 at body size and bold, deeper levels progressively smaller, so the
    # structure is legible at a glance in a contents that runs to seven pages.
    SIZE = {2: r"\small", 3: r"\footnotesize", 4: r"\scriptsize"}
    for level, title, page, number in entries:
        t = latex_escape(title)
        num = f"{latex_escape(number)}\\quad " if number else ""
        if level <= 1:
            lines.append(r"\vspace{0.6em}")
            lines.append(rf"\textbf{{{num}{t}}}\dotfill \textbf{{{page}}}\par")
        else:
            indent = 1.5 * (level - 1)
            size = SIZE.get(level, r"\scriptsize")
            lines.append(
                rf"{{{size}\hspace*{{{indent:.1f}em}}{num}{t}\dotfill {page}\par}}")
    lines.append(r"\end{flushleft}")

    md = f"% {heading}\n\n```{{=latex}}\n" + "\n".join(lines) + "\n```\n"
    md_file = out_file.with_suffix(".toc.md")
    md_file.write_text(md, encoding="utf-8")
    ok = run_pandoc(md_file, out_file, lang, engine, pandoc_bin,
                    geometry="2.2cm", toc=False, number_sections=False,
                    linestretch="1.05", pagestyle="empty", quiet=True)
    md_file.unlink(missing_ok=True)
    return ok


def footnote_count(md_file: Path) -> int:
    """How many distinct footnotes a document will print.

    Mirrors filters/dedupe_footnotes.lua: every `[^key]` that has a definition
    contributes once, however often it is cited. Counting from the markdown
    rather than reading it back out of the PDF keeps bundling to a single pass.
    """
    if not md_file.exists():
        return 0
    text = md_file.read_text(encoding="utf-8")
    defined = {m.group(1) for m in re.finditer(r"^\[\^([\w-]+)\]:", text, re.M)}
    used = [m.group(1) for m in re.finditer(r"\[\^([\w-]+)\](?!:)", text)]
    return len([k for k in dict.fromkeys(used) if k in defined])


def bundle_part(build_type: str, step: str, lang: str,
                engine: str, pandoc_bin: str,
                footnote_offset: int = 0) -> Path | None:
    """A step PDF rendered for inclusion in a bundle, i.e. without its own TOC.

    A per-step TOC is right in a standalone PDF and wrong in a bundle: its page
    numbers are relative to that step, so once merged they all point to the
    wrong place. The bundle gets one merged contents instead. One-pagers carry
    no TOC to begin with, so their existing PDF is reused as-is.

    Parts are cached and only re-rendered when the markdown is newer.
    """
    pdf_for_step, _stem, md_for_step = BUNDLE_TYPES[build_type]
    md_file = md_for_step(step, lang)
    if not md_file.exists():
        return None

    if build_type == "onepager":
        p = pdf_for_step(step, lang)
        return p if p.exists() else None

    BUNDLE_PARTS_DIR.mkdir(parents=True, exist_ok=True)
    out = BUNDLE_PARTS_DIR / f"{build_type}_{step}_{lang}.pdf"
    # The cache keys on the offset too: an earlier chapter gaining a footnote
    # shifts every later part's numbering even though its own markdown is
    # untouched, and a stale part would silently renumber mid-bundle.
    stamp = out.with_suffix(".offset")
    cached = stamp.read_text(encoding="utf-8").strip() if stamp.exists() else None
    if (out.exists() and out.stat().st_mtime >= md_file.stat().st_mtime
            and cached == str(footnote_offset)):
        return out

    opts = report_opts(step) if build_type == "report" else summary_opts(step)
    ok = run_pandoc(md_file, out, lang, engine, pandoc_bin,
                    toc=False, quiet=True, pagestyle="empty",
                    footnote_offset=footnote_offset,
                    extra_args=["--lua-filter", str(BUNDLE_PART_FILTER)], **opts)
    if ok:
        stamp.write_text(str(footnote_offset), encoding="utf-8")
    return out if ok else None


# LaTeX sets ff/fi/fl as single glyphs, so "efficient" comes back out of a PDF
# as "e<ﬀ>icient" and a correct heading looks like it does not match.
_LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl",
              "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st"}


def _norm(s: str) -> str:
    """Fold text for comparison: letters and digits only, lowercased."""
    for lig, plain in _LIGATURES.items():
        s = s.replace(lig, plain)
    return re.sub(r"[^0-9a-zA-Zа-яА-Я]+", "", s).lower()


def read_outline(pdf_file: Path) -> list[tuple[int, str, int]]:
    """A PDF's section outline as (level, title, page), page numbers verified.

    hyperref's recorded page can be stale: when a float moves a heading, the
    bookmark keeps the page from an earlier LaTeX pass, and the extra pass that
    would fix it only happens when a \\tableofcontents is present - which the
    bundle parts deliberately lack. One heading was off by four pages this way.
    So each entry is checked against the text of the page it names, and
    relocated to the page its heading actually appears on.
    """
    try:
        import fitz
    except ImportError:
        return []

    with fitz.open(str(pdf_file)) as doc:
        toc = doc.get_toc()
        if not toc:
            return []
        # Collect text set larger than the body, i.e. headings. Matching against
        # all page text instead gives false hits, because a section's title is
        # usually also mentioned in the prose near it.
        sizes: dict[float, int] = {}
        page_spans: list[list[tuple[float, str]]] = []
        for page in doc:
            spans: list[tuple[float, str]] = []
            for block in page.get_text("dict")["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = round(span["size"], 1)
                        sizes[size] = sizes.get(size, 0) + len(span["text"])
                        spans.append((size, span["text"]))
            page_spans.append(spans)

        if not sizes:
            return [(lvl, t, p, "") for lvl, t, p in toc]
        body = max(sizes, key=lambda s: sizes[s])          # most-used size
        headings = [
            _norm("".join(t for sz, t in spans if sz > body * 1.05))
            for spans in page_spans
        ]

    # LaTeX puts a section's number in its own span ("11.2"), so the printed
    # numbering can be recovered and reused in the merged contents - the PDF
    # outline itself carries no numbers.
    numbers: list[tuple[str, str]] = []          # (normalised title, number)
    current_num, current_txt = "", []
    for spans in page_spans:
        for size, text in spans:
            if size <= body * 1.05:
                continue
            if re.fullmatch(r"\d+(\.\d+)*", text.strip()):
                if current_num and current_txt:
                    numbers.append((_norm("".join(current_txt)), current_num))
                current_num, current_txt = text.strip(), []
            elif current_num:
                current_txt.append(text)
    if current_num and current_txt:
        numbers.append((_norm("".join(current_txt)), current_num))

    # Both the outline and the numbered runs are in document order, so they are
    # walked together. Matching purely on title text instead gave every section
    # called "Architecture" - step 06 has several - the number of the first one.
    cursor = 0

    def number_for(title: str) -> str:
        nonlocal cursor
        key = _norm(title)[:24]
        if not key:
            return ""
        for i in range(cursor, len(numbers)):
            norm_title, num = numbers[i]
            if norm_title.startswith(key) or key in norm_title:
                cursor = i + 1
                return num
        return ""

    out: list[tuple[int, str, int, str]] = []
    for lvl, title, page in toc:
        key = _norm(title)[:24]
        if key and 1 <= page <= len(headings) and key not in headings[page - 1]:
            for i, text in enumerate(headings, start=1):
                if key in text:
                    page = i
                    break
        out.append((lvl, title, page, number_for(title)))
    return out


def stamp_page_numbers(doc, skip_first: int = 1) -> None:
    """Draw a continuous page number at the foot of every page.

    Each part is rendered with pagestyle=empty, because a part that numbered
    its own pages restarted at 1 inside the bundle - so the reader saw a dozen
    "page 1"s and the contents pointed at numbers that appeared nowhere. The
    number has to be applied after merging, since only then is it known.

    skip_first leaves the bundle's title page bare, as a title page should be;
    it still counts, so physical page N reads "N" and matches the contents,
    which is computed from physical positions.
    """
    import fitz  # caller already established it is importable

    for i, page in enumerate(doc, start=1):
        if i <= skip_first:
            continue
        label = str(i)
        # Helvetica is metrically known to PyMuPDF without embedding, and the
        # glyphs needed are digits - no Cyrillic coverage problem here.
        width = fitz.get_text_length(label, fontname="helv", fontsize=10)
        page.insert_text(
            fitz.Point((page.rect.width - width) / 2, page.rect.height - 28),
            label, fontname="helv", fontsize=10)


def merge_pdfs(paths: list[Path], outline: list[tuple[int, str, int]],
               output_file: Path) -> bool:
    """Concatenate `paths`, number the pages continuously, and attach `outline`
    as the bundle's bookmarks.

    PyMuPDF is preferred because it can set a nested outline in one call;
    pypdf is the fallback and gets a flattened version.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        fitz = None

    if fitz is not None:
        out = fitz.open()
        for path in paths:
            with fitz.open(str(path)) as src:
                out.insert_pdf(src)
        stamp_page_numbers(out)
        if outline:
            out.set_toc([[lvl, title, page] for lvl, title, page in outline])
        out.save(str(output_file))
        out.close()
        return True

    try:
        from pypdf import PdfWriter
    except ImportError:
        print("ERROR: bundling needs PyMuPDF or pypdf.\n  pip install pymupdf",
              file=sys.stderr)
        return False

    writer = PdfWriter()
    for path in paths:
        writer.append(str(path))
    for lvl, title, page in outline:
        if lvl == 1:                      # pypdf fallback: top level only
            writer.add_outline_item(title, page - 1)
    with open(output_file, "wb") as fh:
        writer.write(fh)
    return True


def build_bundle(build_type: str, lang: str, engine: str, pandoc_bin: str) -> bool:
    """Merge the per-step PDFs of one type, behind a generated contents page."""
    pdf_for_step, stem, md_for_step = BUNDLE_TYPES[build_type]
    output_file = BUNDLES_DIR / f"{stem}_{lang}.pdf"

    parts, missing = [], []
    running_notes = 0
    for step in BUNDLE_STEPS:
        part = bundle_part(build_type, step, lang, engine, pandoc_bin,
                           footnote_offset=running_notes)
        running_notes += footnote_count(md_for_step(step, lang))
        if part is None:
            missing.append(step)
            continue
        n = int(step.replace("step", ""))
        title = doc_title(md_for_step(step, lang), f"Step {n}")
        parts.append((title, part, page_count(part) or 1, read_outline(part)))

    if not parts:
        print(f"  SKIP {output_file.name}: no {build_type} PDFs found for {lang.upper()}")
        return True

    print(f"  Bundling {len(parts)} {build_type} PDFs → {output_file.name} ...")
    if missing:
        print(f"    (no {lang.upper()} source for: {', '.join(missing)})")

    # --- front matter: title page, then (summaries only) a preface ---------
    title_pdf = BUNDLES_DIR / f".{stem}_{lang}_title.pdf"
    if not build_title_pdf(build_type, lang, title_pdf, engine, pandoc_bin):
        print("    ! title page failed; bundling without one")
        title_pdf = None
    title_pages = (page_count(title_pdf) or 1) if title_pdf else 0

    preface_pdf = None
    preface_pages = 0
    if build_type == "summary":
        preface_pdf = BUNDLES_DIR / f".{stem}_{lang}_preface.pdf"
        if build_preface_pdf(lang, preface_pdf, engine, pandoc_bin):
            preface_pages = page_count(preface_pdf) or 1
        else:
            preface_pdf = None

    def merged_outline(offset: int, max_level: int | None = None) -> list[tuple[int, str, int, str]]:
        """Every part's own outline, shifted into bundle page numbers.

        max_level caps how deep the *printed* contents goes - the PDF's
        navigable bookmark outline (set_toc(), below) always keeps every
        level regardless, since a reader's sidebar isn't the space-constrained
        page a chapter's own H3s were cluttering.
        """
        entries: list[tuple[int, str, int, str]] = []
        page = offset + 1
        for title, _path, n, own in parts:
            if own:
                # A part's outline already names the document at level 1.
                for lvl, t, p, num in own:
                    if max_level is None or lvl <= max_level:
                        entries.append((lvl, t, page + p - 1, num))
            else:
                entries.append((1, title, page, ""))
            page += n
        return entries

    def contents_entries(toc_pages: int, max_level: int | None = 2
                         ) -> list[tuple[int, str, int, str]]:
        """What the contents page lists: the preface, then every step.

        Capped at 2 levels (chapter title + its top-level sections) by
        default - a third level of subsections was cluttering a printed
        contents that already runs to several pages, without helping anyone
        find a chapter. The PDF's own sidebar bookmarks are a different,
        space-unconstrained UI and call this with max_level=None to keep
        every level for in-reader navigation.
        """
        first = title_pages + toc_pages
        entries: list[tuple[int, str, int, str]] = []
        if preface_pages:
            entries.append((1, PREFACE_HEADING[lang], first + 1, ""))
        return entries + merged_outline(first + preface_pages, max_level=max_level)

    # The contents pages shift every page number, and how many pages they take
    # depends on how many entries they hold. Render, measure, repeat until the
    # count stops moving.
    toc_pdf = BUNDLES_DIR / f".{stem}_{lang}_toc.pdf"
    toc_pages = 1
    heading = BUNDLE_TITLES[(build_type, lang)]
    for _ in range(5):
        if not build_toc_pdf(contents_entries(toc_pages), lang, heading,
                             toc_pdf, engine, pandoc_bin):
            print("    ! contents pages failed; bundling without them")
            toc_pdf = None
            break
        actual = page_count(toc_pdf) or 1
        if actual == toc_pages:
            break
        toc_pages = actual

    paths: list[Path] = []
    outline: list[tuple[int, str, int]] = []
    if title_pdf:
        paths.append(title_pdf)
    if toc_pdf and toc_pdf.exists():
        paths.append(toc_pdf)
        outline.append((1, CONTENTS_HEADING[lang], title_pages + 1))
        body = contents_entries(toc_pages)
    else:
        toc_pages = 0
        body = contents_entries(0)
    if preface_pdf:
        paths.append(preface_pdf)
    paths += [p for _t, p, _n, _o in parts]
    # The sidebar has room for the depth the printed page doesn't: recomputed
    # at max_level=None rather than reusing `body`, so a chapter's H3s stay
    # navigable even though they're not listed on the contents page.
    full_body = contents_entries(toc_pages, max_level=None)
    # Carry the section number into the bookmark label too, so the PDF sidebar
    # and the printed contents read the same.
    outline += [(lvl, f"{num} {t}".strip() if num else t, page)
                for lvl, t, page, num in full_body]

    bits = [f"title {title_pages}p"]
    if toc_pages:
        bits.append(f"contents {toc_pages}p / {len(body)} entries")
    if preface_pages:
        bits.append(f"preface {preface_pages}p")
    print(f"    front matter: {', '.join(bits)}")

    ok = merge_pdfs(paths, outline, output_file)
    for tmp in (title_pdf, toc_pdf, preface_pdf):
        if tmp:
            tmp.unlink(missing_ok=True)
    if not ok:
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
        if args.bundle_only:
            try:
                pandoc_bin = find_pandoc()
                engine = find_engine()
            except FileNotFoundError as e:
                print(f"ERROR: {e}", file=sys.stderr)
                sys.exit(1)
        for build_type in types:
            for lang in langs:
                results.append(build_bundle(build_type, lang, engine, pandoc_bin))

    if all(results):
        print("\nAll PDFs built successfully.")
    else:
        failed = results.count(False)
        print(f"\n{failed} build(s) failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
