#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/check_coverage.py
#
# PURPOSE: Which figures used by the Bulgarian documents now have a _bg
#   variant, and which are still English.
#
# USAGE (run from repo root):
#   python scripts/figures/check_coverage.py
# ---------------------------------------------------------------------------

from __future__ import annotations

import glob
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
REPORTS = REPO_ROOT / "deliverables" / "reports"
IMG = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

# Left English by decision: their scripts run training or the image came from a
# textbook. See the plan and FIGURE_LABELS_BG.md.
BY_DECISION = {
    "day02_nfsp_leduc.png", "selfplay_vs_nash.png", "deepcfr.png",
    "mixture_recovery_mixture_tightpassive_50_looseaggressive_50.png",
    "mixture_recovery_mixture_tightpassive_70_looseaggressive_30.png",
}


def bg_docs() -> list[Path]:
    return [Path(p) for p in
            glob.glob(str(REPORTS / "step*/report_bg.md"))
            + glob.glob(str(REPORTS / "step*/summary/summaryBg.md"))
            + glob.glob(str(REPORTS / "step*/summary/onePagerBg.md"))]


def main() -> None:
    refs: dict[Path, set[str]] = defaultdict(set)
    for md in bg_docs():
        for m in IMG.finditer(md.read_text(encoding="utf-8")):
            src = m.group(1).split()[0].strip('"\'')
            if src.startswith("http"):
                continue
            refs[(md.parent / src).resolve()].add(
                md.relative_to(REPORTS).as_posix())

    have, missing, by_decision, broken = [], [], [], []
    for path in sorted(refs):
        if path.name in BY_DECISION:
            by_decision.append(path)
            continue
        if path.stem.endswith("_bg"):
            # already repointed - the only question is whether the file is there
            (have if path.exists() else broken).append(path)
        else:
            # still English: is there a variant it could have pointed at?
            bg = path.with_name(f"{path.stem}_bg{path.suffix}")
            (broken if bg.exists() else missing).append(path)

    total = len(refs)
    print(f"figure references in the BG documents : {total}")
    print(f"  localised (points at a _bg file)    : {len(have)}")
    print(f"  English by decision                 : {len(by_decision)}")
    print(f"  no BG variant exists                : {len(missing)}")
    if broken:
        print(f"  ** BROKEN (variant exists but not used, or file absent): "
              f"{len(broken)}")
        for p in broken[:8]:
            print(f"       {p.name}")

    if missing:
        per_step: dict[str, list[str]] = defaultdict(list)
        for p in missing:
            step = next((x for x in p.parts if x.startswith("step")), "?")
            per_step[step].append(p.name)
        print("\nmissing, by step:")
        for step in sorted(per_step):
            names = sorted(set(per_step[step]))
            print(f"   {step}: {len(names)}")
            for n in names[:6]:
                print(f"      {n}")


if __name__ == "__main__":
    main()
