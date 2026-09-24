#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/merge_label_overlays.py
#
# PURPOSE: Fold the per-chapter figure-label overlays written during the
#   September 2026 final review (deliverables/finalReview/fixes/labels_stepNN.json)
#   into the shared mapping scripts/figures/out/figure_labels.json.
#
#   Chapters were fixed in parallel, so each wrote its label corrections to its
#   own overlay instead of the shared file. A key proposed by two chapters with
#   different Bulgarian is a conflict: it is reported and the shared file is
#   left untouched until it is resolved.
#
# USAGE (run from repo root):
#   python scripts/figures/merge_label_overlays.py          # report only
#   python scripts/figures/merge_label_overlays.py --apply
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
LABELS = REPO_ROOT / "scripts" / "figures" / "out" / "figure_labels.json"
OVERLAYS = REPO_ROOT / "deliverables" / "finalReview" / "fixes"
SOURCE = "final-review-2026-09"


def load_overlay(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        data = {e["en"]: e["bg"] for e in data if e.get("bg")}
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    entries = json.loads(LABELS.read_text(encoding="utf-8"))
    by_en = {e["en"]: e for e in entries}

    proposals: dict[str, dict[str, str]] = defaultdict(dict)
    for path in sorted(OVERLAYS.glob("labels_step*.json")):
        step = path.stem.replace("labels_", "")
        for en, bg in load_overlay(path).items():
            proposals[en][step] = bg

    conflicts = {en: p for en, p in proposals.items() if len(set(p.values())) > 1}
    changed = added = 0
    for en, p in proposals.items():
        if en in conflicts:
            continue
        bg = next(iter(p.values()))
        if en in by_en:
            if by_en[en].get("bg") != bg:
                by_en[en]["bg"] = bg
                by_en[en]["source"] = SOURCE
                changed += 1
        else:
            # same shape as the extracted entries; the overlay is the only
            # known location until extract_labels.py is re-run
            entry = {"en": en, "bg": bg, "source": SOURCE, "glossary_bg": None,
                     "occurrences": [{"file": f"deliverables/finalReview/fixes/labels_{s}.json",
                                      "line": None, "call": "overlay"} for s in sorted(p)]}
            entries.append(entry)
            by_en[en] = entry
            added += 1

    print(f"{len(proposals)} keys from {len(list(OVERLAYS.glob('labels_step*.json')))} "
          f"overlays: {changed} changed, {added} added, {len(conflicts)} conflicts")
    for en, p in conflicts.items():
        print(f"  CONFLICT {en!r}: " + " | ".join(f"{s}={b!r}" for s, b in p.items()))
    if conflicts:
        print("resolve the conflicts first; nothing written")
        return
    if args.apply:
        LABELS.write_text(json.dumps(entries, ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8")
        print(f"written {LABELS.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
