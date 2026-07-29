#!/usr/bin/env python3
"""Normalise compound glossary entries against their constituent terms.

The translation smoke test showed the pipeline faithfully propagating a glossary
that contradicts itself: `policy` is settled as "стратегия" while `policy
network`, `behavioral policy` and `proximal policy optimization` all use
"политика". 168 such pairs exist.

Blind propagation would WRECK the glossary, because the atomic entry often carries
a different sense than it has inside the compound:
    failure mode  vs  mode -> "мода"   (fashion / statistical mode)
    key takeaways vs  key  -> "ключ"   (a physical key)
    betting round vs  round -> "кръг"
So the script only FINDS candidates; BgGPT decides FIX vs KEEP per pair, and a
FIX is applied only if the new rendering verifiably contains the constituent.

Hand-picked terms are never rewritten - those are your decisions; conflicts among
them are reported instead.

    python llmPipeline/normalize_glossary.py --dry-run
    python llmPipeline/normalize_glossary.py
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import ollama, protocol, store as store_mod             # noqa: E402
from core.compose_graph import (build_pool, constituents, fold,    # noqa: E402
                                has_cyrillic, load_terms, stem)

MODEL = "bggpt3-27b"
OUT = HERE / "out"
REPORT = OUT / "glossary_normalisation.md"

SYSTEM = """You are a Bulgarian terminologist auditing a glossary for a computer-science dissertation on artificial intelligence in computer games.

You are shown ONE English part with its agreed Bulgarian rendering, and then every compound term in the glossary that contains that part but currently renders it differently. Judge the whole family together and be CONSISTENT across it: near-identical compounds must get the same verdict.

Decide which case this is:

FIX — the compound should use the part's Bulgarian rendering, and currently does not. The glossary is simply inconsistent. Example: "policy network" = "мрежа на политиката" while "policy" = "стратегия" — these should agree.

KEEP — the English part means something DIFFERENT inside this compound, so the part's rendering must not be forced in. Example: "failure mode" must not use "мода" (fashion / statistical mode); "key takeaways" must not use "ключ" (a physical key). Also KEEP when the compound is an established Bulgarian term in its own right.

For each input line output exactly one line:
  [same number] FIX <the corrected full Bulgarian rendering of the compound>
or
  [same number] KEEP

When you write a FIX, use the part's given Bulgarian form, inflected as Bulgarian grammar requires (case, number, definite article, agreement), and keep the rest of the compound's meaning intact. Output only the numbered lines."""


def violations(terms, pool):
    known = set(pool)
    out = []
    for t in terms:
        if not t.settled_bg or not has_cyrillic(t.settled_bg):
            continue
        for c in constituents(t, known):
            sub = pool.get(c)
            if not sub or not has_cyrillic(sub):
                continue
            words = [w for w in fold(sub).split() if len(w) > 3]
            if not words:
                continue
            if not all(stem(w) in fold(t.settled_bg) for w in words):
                out.append((t, c, sub))
                break                      # one violation per term is enough
    out.sort(key=lambda r: -r[0].freq)
    return out


def _judge(grp, outs, changes, kept, stats) -> None:
    """Apply one family's verdicts, rejecting fixes that fail verification."""
    for (t, c, sub), verdict in zip(grp, outs):
        v = (verdict or "").strip()
        if not v.upper().startswith("FIX"):
            stats["KEEP (different sense)"] += 1
            kept.append((t, c, sub))
            continue
        new = v[3:].strip(" :–-").strip().strip('"')
        if not new or not has_cyrillic(new):
            stats["rejected: no Bulgarian"] += 1
            continue
        # the fix must actually use the constituent's rendering
        if not all(stem(w) in fold(new) for w in fold(sub).split() if len(w) > 3):
            stats["rejected: fix ignored the part"] += 1
            continue
        # guards against additive nonsense like "грешка в кода" -> "грешка дефект в кода"
        old_w, new_w = len(t.settled_bg.split()), len(new.split())
        if new_w > old_w + 1 or not 0.6 <= new_w / max(1, old_w) <= 1.5:
            stats["rejected: implausible length"] += 1
            continue
        changes.append((t, c, sub, new))
        stats["FIX applied"] += 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--batch", type=int, default=15)
    a = ap.parse_args()

    st = store_mod.Store(OUT / "glossary.db")
    terms = load_terms(st)
    pool, quarantined, benign, leaky = build_pool(terms)
    vio = violations(terms, pool)

    # Hand picks were originally excluded as the owner's decisions. They were made
    # term-by-term without seeing the family, which is the very thing that produced
    # the inconsistency, so the owner released them for normalisation. Every change
    # to a previously hand-picked term is still listed separately in the report.
    handpicked = [v for v in vio if v[0].status == "picked"]
    auto = list(vio)
    was_picked = {v[0].key for v in handpicked}
    print(f"{len(vio)} inconsistent compounds "
          f"({len(vio) - len(handpicked)} machine-settled, "
          f"{len(handpicked)} previously hand-picked — now also normalised)")

    if not ollama.wait_until_up():
        print("ollama unreachable")
        return 1

    stats: Counter = Counter()
    changes, kept = [], []
    t0 = time.perf_counter()

    # Group by shared constituent so a whole family is judged in one request.
    # Judged separately, the model gave opposite verdicts on identical cases
    # ("global policy" FIX but "tabular policy" KEEP) purely because they landed
    # in different batches.
    families: dict[tuple[str, str], list] = {}
    for t, c, sub in auto:
        families.setdefault((c, sub), []).append(t)
    print(f"grouped into {len(families)} constituent families "
          f"(largest: {max((len(v) for v in families.values()), default=0)})")

    done = 0
    for (c, sub), members in sorted(families.items(), key=lambda kv: -len(kv[1])):
        for i in range(0, len(members), a.batch):
            grp = [(t, c, sub) for t in members[i:i + a.batch]]
            items = [f'"{t.term}" currently = "{t.settled_bg}"' for t, _c, _s in grp]
            head = (f'PART: "{c}" is agreed to be "{sub}".\n\n'
                    f'Compounds containing "{c}" that do not use it:\n')

            def call(xs, head=head):
                return ollama.generate(MODEL, head + protocol.render(xs),
                                       SYSTEM, temperature=0.2, num_predict=1400,
                                       num_ctx=8192, think=False)

            idx = {id(x): n for n, x in enumerate(grp)}
            outs = protocol.run_batched(grp, call, lambda x: items[idx[id(x)]],
                                        lambda x: "KEEP")
            done += len(grp)
            _judge(grp, outs, changes, kept, stats)
        print(f"   {done}/{len(auto)}  {time.perf_counter()-t0:5.0f}s", flush=True)

    if not a.dry_run:
        for t, _c, _sub, new in changes:
            st.db.execute("UPDATE proposals SET chosen=?, reason=? WHERE key=?",
                          (new, "normalised: agrees with its constituent term", t.key))
            st.db.execute(
                """INSERT OR REPLACE INTO picks(key,bg,status,keep_latin,first_use,note,stage,ts)
                   VALUES (?,?,?,0,1,?,?,?)""",
                (t.key, new, "auto", "normalised against constituent", "normalise",
                 time.time()))
        st.db.commit()

    repicked = [x for x in changes if x[0].key in was_picked]
    md = ["# Glossary normalisation", "",
          f"- inconsistent compounds found: {len(vio)}",
          f"- rewritten to agree with their constituent: **{len(changes)}**",
          f"- kept (the part means something else inside the compound): {len(kept)}",
          f"- of the rewrites, previously hand-picked: **{len(repicked)}**", "",
          "## Rewritten", "", "| term | was | now | because of | was your pick |",
          "|---|---|---|---|---|"]
    for t, c, _s, new in changes:
        mark = "yes" if t.key in was_picked else ""
        md.append(f"| {t.term} | {t.settled_bg} | **{new}** | {c} | {mark} |")
    md += ["", "## Kept — polysemy, forcing the part would be wrong", "",
           "| term | rendering | part | part's own form |", "|---|---|---|---|"]
    for t, c, sub in kept[:80]:
        md.append(f"| {t.term} | {t.settled_bg} | {c} | {sub} |")
    still = [(t, c, s) for t, c, s in kept if t.key in was_picked]
    if still:
        md += ["", "## Previously hand-picked, left unchanged (judged polysemy)", "",
               "| term | rendering | part | part's form |", "|---|---|---|---|"]
        for t, c, sub in still:
            md.append(f"| {t.term} | {t.settled_bg} | {c} | {sub} |")
    REPORT.write_text("\n".join(md) + "\n", encoding="utf-8")

    print("\n" + "\n".join(f"  {k:<30} {v}" for k, v in stats.most_common()))
    print(f"\nreport: {REPORT}")
    if a.dry_run:
        print("(dry run — nothing written to the glossary)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
