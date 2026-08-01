#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/extract_labels.py
#
# PURPOSE: Collect every human-readable text string that the matplotlib
#   plotting scripts put into a figure, so the set can be translated once and
#   applied to Bulgarian renders of the same figures.
#
#   Uses the ast module rather than a regex or a language model: the labels are
#   string literals in source, so parsing gives an exact answer with file and
#   line numbers, survives multi-line and implicitly concatenated strings, and
#   is deterministic.
#
#   Only arguments that carry human text are collected. `ha="center"`,
#   `va="bottom"` and `weight="bold"` are the same kind of literal in the same
#   calls and must NOT be translated - doing so silently breaks layout.
#
# USAGE (run from repo root):
#   python scripts/figures/extract_labels.py
#   python scripts/figures/extract_labels.py --json out/figure_labels.json
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import ast
import glob
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
DEFAULT_OUT = REPO_ROOT / "scripts" / "figures" / "out" / "figure_labels.json"

# call name -> index of the positional argument holding display text
TEXT_POSITIONAL = {
    "set_xlabel": 0, "set_ylabel": 0, "set_zlabel": 0,
    "set_title": 0, "suptitle": 0,
    "xlabel": 0, "ylabel": 0, "title": 0,
    "set_label": 0,
    "annotate": 0,          # annotate(s, xy=...)
    "text": 2,              # ax.text(x, y, s)
    "figtext": 2,
    # Project helpers from deliverables/reports/step*/summary/_diagram_utils.py.
    # The architecture diagrams route every string through these rather than
    # calling matplotlib directly, so without them the whole diagram set - 32 of
    # the scripts - looks label-free.
    "box": 5,               # box(ax, x, y, w, h, label, ...)
    "panel_bg": 6,          # panel_bg(ax, x, y, w, h, fc, label=None, ...)
    "note": 3,              # note(ax, x, y, text, ...)
}
# keyword arguments holding display text
TEXT_KEYWORDS = {"label", "title", "xlabel", "ylabel"}
# calls whose first argument is a list of tick label strings
TICK_CALLS = {"set_xticklabels", "set_yticklabels", "xticks", "yticks"}

# Scripts that run training or simulation. Re-running them could produce
# numbers that no longer match the text - one has no pinned seed - so their
# figures stay English by decision.
SKIP = {
    "implementation/step05/exploration/day02_nfsp.py",
    "implementation/step07/exploration/mixture_recovery.py",
    "implementation/step09/exploration/selfplay_vs_nash.py",
}


def call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    if isinstance(node.func, ast.Name):
        return node.func.id
    return ""


def literal_strings(node: ast.AST) -> list[str]:
    """Strings from a constant, or from a list/tuple of constants."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, (ast.List, ast.Tuple)):
        out = []
        for el in node.elts:
            if isinstance(el, ast.Constant) and isinstance(el.value, str):
                out.append(el.value)
        return out
    return []


def plotting_scripts() -> list[Path]:
    """Every script that draws a figure used by the step deliverables.

    Two homes, found the hard way: the result plots live under implementation/,
    but the architecture diagrams live beside the summaries they illustrate, in
    deliverables/reports/stepNN/summary/make_*.py. Scanning only implementation/
    silently misses step 06 entirely.
    """
    roots = [
        REPO_ROOT / "implementation",
        REPO_ROOT / "deliverables" / "reports",
    ]
    found = []
    for root in roots:
        for f in glob.glob(str(root / "**" / "*.py"), recursive=True):
            p = Path(f)
            rel = p.relative_to(REPO_ROOT).as_posix()
            if rel in SKIP or "/ruseMay/" in f"/{rel}":
                continue
            try:
                src = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            # a diagram module may only define helpers; its callers do the saving
            if "savefig" in src or "_diagram_utils" in src:
                found.append(p)
    return sorted(found)


def extract(path: Path) -> list[dict]:
    """Every display string in one script, with its location."""
    src = path.read_text(encoding="utf-8", errors="ignore")
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        print(f"  ! cannot parse {path.name}: {e}", file=sys.stderr)
        return []

    rel = path.relative_to(REPO_ROOT).as_posix()
    found: list[dict] = []

    def add(text: str, line: int, call: str) -> None:
        if text and text.strip():
            found.append({"text": text, "file": rel, "line": line, "call": call})

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = call_name(node)

        idx = TEXT_POSITIONAL.get(name)
        if idx is not None and len(node.args) > idx:
            for s in literal_strings(node.args[idx]):
                add(s, node.lineno, name)

        if name in TICK_CALLS:
            # xticks(positions, labels) or set_xticklabels(labels)
            target = node.args[1] if (name in ("xticks", "yticks") and len(node.args) > 1) \
                else (node.args[0] if node.args else None)
            if target is not None:
                for s in literal_strings(target):
                    add(s, node.lineno, name)

        for kw in node.keywords:
            if kw.arg in TEXT_KEYWORDS:
                for s in literal_strings(kw.value):
                    add(s, node.lineno, f"{name}({kw.arg}=)")

    return found


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract matplotlib label strings.")
    ap.add_argument("--json", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    scripts = plotting_scripts()
    occurrences: list[dict] = []
    for p in scripts:
        occurrences += extract(p)

    by_text: dict[str, list[dict]] = defaultdict(list)
    for occ in occurrences:
        by_text[occ["text"]].append(
            {"file": occ["file"], "line": occ["line"], "call": occ["call"]})

    # glossary hit, for the translation step
    gloss_path = REPO_ROOT / "llmPipeline" / "glossary_settled.json"
    by_en: dict[str, str] = {}
    if gloss_path.exists():
        for e in json.loads(gloss_path.read_text(encoding="utf-8")):
            by_en.setdefault(e["en"].strip().lower(), e["bg"])

    entries = []
    for text, occs in sorted(by_text.items()):
        entries.append({
            "en": text,
            "bg": None,
            "source": None,
            "glossary_bg": by_en.get(text.strip().lower()),
            "occurrences": occs,
        })

    out = Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")

    steps = sorted({o["file"].split("/")[1] for o in occurrences})
    print(f"plotting scripts scanned : {len(scripts)} "
          f"({len(SKIP)} skipped by decision)")
    print(f"label occurrences        : {len(occurrences)}")
    print(f"distinct strings         : {len(entries)}")
    print(f"  already in the glossary: {sum(1 for e in entries if e['glossary_bg'])}")
    print(f"steps covered            : {', '.join(steps)}")
    print(f"\nwritten to {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
