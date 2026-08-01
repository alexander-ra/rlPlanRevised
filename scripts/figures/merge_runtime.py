#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/merge_runtime.py
#
# PURPOSE: Fold the strings observed while actually running the plotting
#   scripts into the label set produced by static parsing.
#
#   Static parsing sees only literals at the call site. Several diagrams keep
#   their text in a module-level table and pass it through a variable, so a
#   third of the vocabulary is invisible to ast and only shows up at runtime.
#
# USAGE (run from repo root):
#   python scripts/figures/merge_runtime.py <runtime_labels.json>
# ---------------------------------------------------------------------------

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
LABELS = REPO_ROOT / "scripts" / "figures" / "out" / "figure_labels.json"


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: merge_runtime.py <runtime_labels.json>", file=sys.stderr)
        sys.exit(1)

    entries = json.loads(LABELS.read_text(encoding="utf-8"))
    observed = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    known = {e["en"] for e in entries}
    added = 0
    for s in observed:
        if s in known or not s.strip():
            continue
        entries.append({
            "en": s,
            "bg": None,
            "source": None,
            "glossary_bg": None,
            "occurrences": [{"file": "(observed at runtime)", "line": 0,
                             "call": "runtime"}],
        })
        known.add(s)
        added += 1

    entries.sort(key=lambda e: e["en"].lower())
    LABELS.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(f"observed at runtime : {len(observed)}")
    print(f"newly added         : {added}")
    print(f"total label strings : {len(entries)}")
    print(f"  still untranslated: {sum(1 for e in entries if not e.get('bg'))}")


if __name__ == "__main__":
    main()
