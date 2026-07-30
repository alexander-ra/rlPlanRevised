#!/usr/bin/env python3
"""Repair individual blocks that fell back to English, without re-running files.

After the corpus run, 21 of 2,094 blocks were left in English because two
verification rules were too strict (exact blockquote line equality, and demanding
Cyrillic in headings that are pure system names). The rules are fixed; this
re-translates only the affected blocks and splices them back, which costs minutes
rather than the hours a full re-run of ten files would take.

Each block is translated independently anyway, with its neighbours as context, so
a spliced repair is equivalent to having produced it in the original run.

    python llmPipeline/repair_blocks.py --dry-run
    python llmPipeline/repair_blocks.py
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import translate_doc as T                       # noqa: E402

REPO = HERE.parent
R = REPO / "deliverables" / "reports"
CYR = re.compile(r"[Ѐ-ӿ]")
PAIR = [("summary/onePager.md", "summary/onePagerBg.md"),
        ("summary/summaryEn.md", "summary/summaryBg.md"),
        ("report_en.md", "report_bg.md")]


def math_n(s: str) -> int:
    return len(re.findall(r"(?<!\$)\$[^$\n]+\$(?!\$)", s)) + s.count("$$") // 2


def needs_repair(en, bg) -> str | None:
    """Why this block needs redoing, or None."""
    if en.kind in T.SKIP_KINDS:
        return None
    trans = [w for w in re.findall(r"[A-Za-z]{3,}", en.raw) if not w.isupper()]
    if not CYR.search(bg.raw) and len(trans) >= 3:
        return "left in English"
    if math_n(en.raw) != math_n(bg.raw):
        return f"math spans {math_n(en.raw)} -> {math_n(bg.raw)}"
    if en.kind == "heading" and not bg.raw.lstrip().startswith("#"):
        return "heading marker lost"
    return None


def repair_file(en_path: Path, bg_path: Path, dry: bool, log=print) -> int:
    pre_en, en_blocks = T.parse(en_path.read_text(encoding="utf-8"))
    pre_bg, bg_blocks = T.parse(bg_path.read_text(encoding="utf-8"))
    if len(en_blocks) != len(bg_blocks):
        log(f"   SKIP {bg_path.name}: block counts differ "
            f"({len(en_blocks)}/{len(bg_blocks)}) - needs a full re-run")
        return 0

    targets = [(i, why) for i, (a, b) in enumerate(zip(en_blocks, bg_blocks))
               if (why := needs_repair(a, b))]
    if not targets:
        return 0

    log(f"   {bg_path.parent.name}/{bg_path.name}: {len(targets)} block(s)")
    for i, why in targets:
        log(f"      block {i} [{en_blocks[i].kind}] {why}: "
            f"{' '.join(en_blocks[i].raw.split())[:64]}")
    if dry:
        return len(targets)

    T.set_source(en_path)
    gloss = T.load_glossary()
    # existing Bulgarian becomes context for neighbours (out[0] is what
    # build_prompt reads as "already handled" when running pass 1)
    for b, q in zip(en_blocks, bg_blocks):
        b.out[0] = q.raw
        b.out[5] = q.raw

    fixed = 0
    for i, _why in targets:
        blk = en_blocks[i]
        blk.out.pop(5, None)
        ok = True
        for pn in (1, 2, 3, 4):
            prompt, store = T.build_prompt(en_blocks, i, pn, gloss)
            best, good = None, None
            bad = ["not attempted"]
            for attempt in (1, 2):
                p = prompt if attempt == 1 else prompt + (
                    "\n\nYour previous answer was rejected (" + "; ".join(bad)
                    + "). Return ONLY the target block with its markdown intact.")
                try:
                    raw = T.ollama.generate(
                        T.MODEL, p, T.PASS_PROMPT[pn],
                        temperature=T.PASSES[pn][1], top_p=0.9, num_predict=1600,
                        num_ctx=8192, think=False, log=log)
                except Exception as e:      # noqa: BLE001
                    bad = [f"request failed: {e}"]
                    continue
                cand, miss = T.thaw(T.clean_reply(raw), store)
                bad = T.check(blk, cand, miss)
                if best is None:
                    best = cand
                if not bad:
                    good = cand
                    break
            blk.out[pn] = good or blk.out.get(pn - 1) or best or blk.raw
            if not good:
                ok = False
                log(f"      block {i} pass {pn} still failing: {bad}")
        blk.out[5] = blk.out.get(4, blk.raw)
        fixed += 1 if ok else 0

    body = "\n\n".join(b.out.get(5, b.raw) for b in en_blocks)
    bg_path.write_text((pre_bg + "\n\n" if pre_bg else "") + body + "\n",
                       encoding="utf-8")
    log(f"      rewrote {bg_path.name} ({fixed}/{len(targets)} clean)")
    return len(targets)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.dry_run and not T.ollama.wait_until_up():
        print("ollama unreachable")
        return 1

    total = 0
    t0 = time.perf_counter()
    for i in range(1, 13):
        step = f"step{i:02d}"
        for en_rel, bg_rel in PAIR:
            pe, pb = R / step / en_rel, R / step / bg_rel
            if pe.exists() and pb.exists():
                total += repair_file(pe, pb, a.dry_run)
    print(f"\n{total} block(s) {'would be' if a.dry_run else ''} repaired "
          f"in {(time.perf_counter()-t0)/60:.1f}m")
    return 0


if __name__ == "__main__":
    sys.exit(main())
