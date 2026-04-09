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

import json
import sys
from pathlib import Path

# Paths — all resolved relative to repo root regardless of cwd
REPO_ROOT         = Path(__file__).parent.parent.resolve()
SRC_DIR           = REPO_ROOT / "interactiveStudy" / "src"
DIST_DIR          = REPO_ROOT / "docs"    # served by GitHub Pages
RAW_STEPS_DIR_EN  = REPO_ROOT / "planning" / "rawSteps"
RAW_STEPS_DIR_BG  = REPO_ROOT / "planning" / "rawStepsBg"

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


def generate_content_script(steps_en: dict, steps_bg: dict, translations: dict) -> str:
    """Generate a <script> block embedding EN/BG content and translations."""
    def dict_to_js(d: dict, var_name: str) -> str:
        pairs = [f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in d.items()]
        return f"const {var_name} = {{\n" + ",\n".join(pairs) + "\n};"

    en_js    = dict_to_js(steps_en, "STEPS_CONTENT_EN")
    bg_js    = dict_to_js(steps_bg, "STEPS_CONTENT_BG")
    trans_js = f"const TRANSLATIONS = {json.dumps(translations, ensure_ascii=False, indent=2)};"

    return f"<script>\n{en_js}\n\n{bg_js}\n\n{trans_js}\n</script>"


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

    # Generate combined content + translations script
    content_script = generate_content_script(steps_en, steps_bg, translations)

    # Replace placeholders
    output = shell_html
    output = output.replace("<!-- INLINE_CSS -->", f"<style>\n{styles_css}\n</style>")
    output = output.replace("<!-- INLINE_JS -->", f"<script>\n{app_js}\n</script>")
    output = output.replace("<!-- INLINE_CONTENT -->", content_script)

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
