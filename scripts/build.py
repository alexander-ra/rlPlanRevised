#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/build.py
#
# PURPOSE: Build the standalone Interactive Study Viewer HTML file.
#   Reads interactiveStudy/src/{shell.html, styles.css, JS modules} and all 15
#   rawSteps markdown files (EN + BG), inlines everything into a single
#   self-contained docs/index.html (GitHub Pages).
#
# USAGE (run from repo root):
#   python3 scripts/build.py
# ---------------------------------------------------------------------------

import base64
import json
import re
import sys
from pathlib import Path

# Paths — all resolved relative to repo root regardless of cwd
REPO_ROOT         = Path(__file__).parent.parent.resolve()
SRC_DIR           = REPO_ROOT / "interactiveStudy" / "src"
DIST_DIR          = REPO_ROOT / "docs"    # served by GitHub Pages
RAW_STEPS_DIR_EN  = REPO_ROOT / "planning" / "rawSteps"
RAW_STEPS_DIR_BG  = REPO_ROOT / "planning" / "rawStepsBg"
INTRO_MD_EN       = REPO_ROOT / "deliverables" / "studyPlan" / "en" / "01_introduction.md"
INTRO_MD_BG       = REPO_ROOT / "deliverables" / "studyPlan" / "bg" / "01_introduction.md"

# Step file list (order matters)
STEP_FILES = [
    "step_01_rl_basics.md",
    "step_02_game_theory_cfr.md",
    "step_03_cfr_variants_mc.md",
    "step_04_game_abstraction_scaling.md",
    "step_05_neural_equilibrium.md",
    "step_06_end_to_end_game_ai.md",
    "step_07_opponent_modeling.md",
    "step_08_safe_exploitation.md",
    "step_09_multi_agent_rl.md",
    "step_10_population_training_evo_gt.md",
    "step_11_coalition_formation_ffa.md",
    "step_12_sequence_models_llm_agents.md",
    "step_13_behavioral_analysis.md",
    "step_14_evaluation_frameworks.md",
    "step_15_research_frontier_mapping.md",
]

# JS modules in dependency order (concatenated into one bundle)
JS_MODULES = [
    "config.js",
    "lock.js",
    "i18n.js",
    "cloud.js",
    "theme.js",
    "schedule.js",
    "youtube.js",
    "reading-guide.js",
    "content.js",
    "markdown.js",
    "calendar.js",
    "nav.js",
    "main.js",
]


def read_steps(steps_dir: Path) -> dict[str, str]:
    """Read all rawSteps markdown files into a dict keyed by short ID."""
    if not steps_dir.is_dir():
        print(f"WARNING: Steps directory not found: {steps_dir}", file=sys.stderr)
        return {}

    steps: dict[str, str] = {}
    for filename in STEP_FILES:
        filepath = steps_dir / filename
        if not filepath.exists():
            print(f"WARNING: Missing step file: {filepath}", file=sys.stderr)
            continue
        # Short ID: "step_01" from "step_01_rl_basics.md"
        parts = filename.replace(".md", "").split("_")
        short_id = parts[0] + "_" + parts[1]  # "step_01"
        steps[short_id] = filepath.read_text(encoding="utf-8")
    return steps


def bundle_js() -> str:
    """Concatenate all JS modules in order into one bundle string."""
    parts = []
    for module in JS_MODULES:
        path = SRC_DIR / module
        if not path.exists():
            print(f"WARNING: JS module not found: {path}", file=sys.stderr)
            continue
        parts.append(f"/* === {module} === */\n" + path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def read_translations() -> dict:
    """Read both translations JSON files and return combined dict."""
    translations = {}
    for lang in ("en", "bg"):
        path = SRC_DIR / f"translations_{lang}.json"
        if not path.exists():
            print(f"WARNING: Translation file not found: {path}", file=sys.stderr)
            translations[lang] = {}
        else:
            translations[lang] = json.loads(path.read_text(encoding="utf-8"))
    return translations


def read_intro_md() -> tuple[str, str]:
    """Read bilingual intro markdown files."""
    en = INTRO_MD_EN.read_text(encoding="utf-8") if INTRO_MD_EN.exists() else ""
    bg = INTRO_MD_BG.read_text(encoding="utf-8") if INTRO_MD_BG.exists() else ""
    if not en:
        print(f"WARNING: Intro EN not found: {INTRO_MD_EN}", file=sys.stderr)
    if not bg:
        print(f"WARNING: Intro BG not found: {INTRO_MD_BG}", file=sys.stderr)
    return en, bg


# SVG source files and their inline IDs
SVG_FILES = {
    "MAIN_LOGO_SVG":    ("mainLogo.svg",            "main-logo"),
    "CONTRIB_ONE_SVG":  ("contributionOneLogo.svg",  "contrib-one"),
    "CONTRIB_TWO_SVG":  ("contributionTwoLogo.svg",  "contrib-two"),
    "CONTRIB_THREE_SVG":("contributionThreeLogo.svg","contrib-three"),
}


def process_svg_for_inline(svg_content: str, svg_id: str) -> str:
    """Add a unique ID to the SVG root and scope its <style> class selectors
    to that ID, preventing CSS class-name collisions when multiple SVGs are
    inlined in the same document."""
    # Inject id attribute into the root <svg ...> tag
    svg = re.sub(r'^(<svg\s)', lambda m: m.group(1) + f'id="{svg_id}" ', svg_content, count=1)

    def scope_style_block(m: re.Match) -> str:
        style = m.group(1)
        # Prepend each class-selector rule with the SVG id scope
        style = re.sub(
            r'(\.(?:[a-zA-Z_-][a-zA-Z0-9_-]*))\s*\{',
            lambda x: f'#{svg_id} {x.group(1)} {{',
            style
        )
        return f'<style>{style}</style>'

    return re.sub(r'<style>(.*?)</style>', scope_style_block, svg, flags=re.DOTALL)


def read_svgs() -> dict[str, str]:
    """Read and inline-safe process all hero/contribution SVG assets."""
    svgs: dict[str, str] = {}
    for js_const, (filename, svg_id) in SVG_FILES.items():
        path = SRC_DIR / filename
        if not path.exists():
            print(f"WARNING: SVG not found: {path}", file=sys.stderr)
            svgs[js_const] = ""
            continue
        raw = path.read_text(encoding="utf-8").strip()
        svgs[js_const] = process_svg_for_inline(raw, svg_id)
    return svgs


def get_favicon_link() -> str:
    """Return an SVG favicon <link> tag using the mainLogo.svg as a base64 data URI."""
    path = SRC_DIR / "mainLogo.svg"
    if not path.exists():
        return ''
    svg_bytes = path.read_text(encoding="utf-8").strip().encode("utf-8")
    b64 = base64.b64encode(svg_bytes).decode("ascii")
    return f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,{b64}">'


def generate_content_script(steps_en: dict, steps_bg: dict, translations: dict,
                             intro_en: str, intro_bg: str, svgs: dict) -> str:
    """Generate a <script> block embedding EN/BG content, translations, and SVGs."""
    def dict_to_js(d: dict, var_name: str) -> str:
        pairs = [f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in d.items()]
        return f"const {var_name} = {{\n" + ",\n".join(pairs) + "\n};"

    en_js       = dict_to_js(steps_en, "STEPS_CONTENT_EN")
    bg_js       = dict_to_js(steps_bg, "STEPS_CONTENT_BG")
    trans_js    = f"const TRANSLATIONS = {json.dumps(translations, ensure_ascii=False, indent=2)};"
    intro_en_js = f"const INTRO_MD_EN = {json.dumps(intro_en)};"
    intro_bg_js = f"const INTRO_MD_BG = {json.dumps(intro_bg)};"
    svg_js      = "\n".join(
        f"const {key} = {json.dumps(val)};" for key, val in svgs.items()
    )

    return (
        f"<script>\n{en_js}\n\n{bg_js}\n\n{trans_js}\n\n"
        f"{intro_en_js}\n{intro_bg_js}\n\n{svg_js}\n</script>"
    )


def write_service_worker(dist_dir: Path) -> None:
    """Write docs/sw.js — network-first with cache fallback for offline use."""
    sw_content = """\
const CACHE_NAME = 'rl-study-v2';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.add('./'))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      }).catch(() => caches.match('./'))
    );
  }
});
"""
    (dist_dir / "sw.js").write_text(sw_content, encoding="utf-8")


def build():
    """Main build: inline CSS, JS modules, translations, and content into shell.html."""
    # Read source files
    shell_html = (SRC_DIR / "shell.html").read_text(encoding="utf-8")
    styles_css = (SRC_DIR / "styles.css").read_text(encoding="utf-8")

    # Bundle all JS modules
    app_js = bundle_js()

    # Read step content (EN + BG)
    steps_en = read_steps(RAW_STEPS_DIR_EN)
    steps_bg = read_steps(RAW_STEPS_DIR_BG)
    if not steps_en:
        print("ERROR: No EN step files found.", file=sys.stderr)
        sys.exit(1)

    # Read translations
    translations = read_translations()

    # Read bilingual intro markdown
    intro_en, intro_bg = read_intro_md()

    # Read and process SVG assets
    svgs = read_svgs()

    # Generate combined content + translations + SVGs script
    content_script = generate_content_script(steps_en, steps_bg, translations, intro_en, intro_bg, svgs)

    # Build favicon link
    favicon_link = get_favicon_link()

    # Replace placeholders
    output = shell_html
    output = output.replace("<!-- INLINE_CSS -->", f"<style>\n{styles_css}\n</style>")
    output = output.replace("<!-- INLINE_JS -->", f"<script>\n{app_js}\n</script>")
    output = output.replace("<!-- INLINE_CONTENT -->", content_script)
    output = output.replace("<!-- INLINE_FAVICON -->", favicon_link)

    # Write output
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIST_DIR / "index.html"
    out_path.write_text(output, encoding="utf-8")

    # .nojekyll prevents GitHub Pages from running Jekyll on our built HTML
    (DIST_DIR / ".nojekyll").touch()

    # Service worker
    write_service_worker(DIST_DIR)

    size_kb = out_path.stat().st_size / 1024
    print(f"Built {out_path} ({size_kb:.0f} KB)")
    print(f"  EN steps: {len(steps_en)}, BG steps: {len(steps_bg)}")
    print(f"  Translations: {list(translations.keys())}")
    print(f"  JS modules: {len(JS_MODULES)}")


if __name__ == "__main__":
    build()
