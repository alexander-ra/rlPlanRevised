#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/build.py
#
# PURPOSE: Build the standalone Interactive Study Viewer HTML file.
#   Reads interactiveStudy/src/{shell.html, styles.css, app.js} and all 15
#   rawSteps markdown files, inlines everything into a single self-contained
#   interactiveStudy/dist/interactiveStudy.html.
#
# USAGE (run from repo root):
#   python3 scripts/build.py
# ---------------------------------------------------------------------------

import json
import sys
from pathlib import Path

# Paths — all resolved relative to repo root regardless of cwd
REPO_ROOT     = Path(__file__).parent.parent.resolve()
SRC_DIR       = REPO_ROOT / "interactiveStudy" / "src"
DIST_DIR      = REPO_ROOT / "interactiveStudy" / "dist"
RAW_STEPS_DIR = REPO_ROOT / "planning" / "rawSteps"

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


def read_steps() -> dict[str, str]:
    """Read all rawSteps markdown files into a dict keyed by short ID."""
    if not RAW_STEPS_DIR.is_dir():
        print(f"ERROR: rawSteps directory not found: {RAW_STEPS_DIR}", file=sys.stderr)
        sys.exit(1)

    steps: dict[str, str] = {}
    for filename in STEP_FILES:
        filepath = RAW_STEPS_DIR / filename
        if not filepath.exists():
            print(f"WARNING: Missing step file: {filepath}", file=sys.stderr)
            continue
        # Short ID: "step_01" from "step_01_rl_basics.md"
        parts = filename.replace(".md", "").split("_")
        short_id = parts[0] + "_" + parts[1]  # "step_01"
        steps[short_id] = filepath.read_text(encoding="utf-8")
    return steps


def generate_content_script(steps: dict[str, str]) -> str:
    """Generate a <script> block embedding all step content as JSON."""
    pairs = []
    for step_id, content in steps.items():
        pairs.append(f"  {json.dumps(step_id)}: {json.dumps(content)}")
    js_obj = "const STEPS_CONTENT = {\n" + ",\n".join(pairs) + "\n};"
    return f"<script>\n{js_obj}\n</script>"


def build():
    """Main build: inline CSS, JS, and content into shell.html → dist/interactiveStudy.html."""
    # Read source files
    shell_html = (SRC_DIR / "shell.html").read_text(encoding="utf-8")
    styles_css = (SRC_DIR / "styles.css").read_text(encoding="utf-8")
    app_js     = (SRC_DIR / "app.js").read_text(encoding="utf-8")

    # Read step content
    steps = read_steps()
    if not steps:
        print("ERROR: No step files found.", file=sys.stderr)
        sys.exit(1)
    content_script = generate_content_script(steps)

    # Replace placeholders
    output = shell_html
    output = output.replace("<!-- INLINE_CSS -->", f"<style>\n{styles_css}\n</style>")
    output = output.replace("<!-- INLINE_JS -->", f"<script>\n{app_js}\n</script>")
    output = output.replace("<!-- INLINE_CONTENT -->", content_script)

    # Write output
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIST_DIR / "interactiveStudy.html"
    out_path.write_text(output, encoding="utf-8")

    size_kb = out_path.stat().st_size / 1024
    print(f"Built {out_path} ({size_kb:.0f} KB)")
    print(f"Embedded {len(steps)} steps")


if __name__ == "__main__":
    build()
