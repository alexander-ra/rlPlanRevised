"""Stage D - write the morning artifacts.

Called after every stage (and on exit), so killing the run at any moment still
leaves a usable queue on disk rather than only a database.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from stages.b_normalize import CATEGORIES, UNCLEAR


def _j(s, default):
    try:
        return json.loads(s) if s else default
    except Exception:  # noqa: BLE001
        return default


def emit(store, out: Path, meta: dict, log=print) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    rows = store.proposals()

    auto, queue, deferred = [], [], []
    by_cat: dict[str, list] = defaultdict(list)
    unclear: list[dict] = []

    for (key, term, cat, freq, ctx_json, ex_bg,
         samples_json, cands_json, decision, chosen, reason) in rows:
        rec = {
            "key": key, "term": term, "category": cat or UNCLEAR, "freq": freq,
            "contexts": _j(ctx_json, []), "existing_bg": ex_bg,
            "candidates": _j(cands_json, []), "reason": reason,
        }
        by_cat[rec["category"]].append(rec)
        if decision == "auto":
            rec["bg"] = chosen
            auto.append(rec)
        elif decision == "deferred":
            deferred.append(rec)
        else:
            # existing translation first so tomorrow it is a single keypress
            cands = list(rec["candidates"])
            if ex_bg:
                cands = ([{"bg": ex_bg, "votes": 0, "source": "current glossary"}]
                         + [c for c in cands if c.get("bg") != ex_bg])
            rec["candidates"] = cands
            queue.append(rec)
        if (cat or UNCLEAR) == UNCLEAR:
            unclear.append(rec)

    (out / "glossary_auto.json").write_text(
        json.dumps(auto, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "glossary_queue.json").write_text(
        json.dumps(queue, ensure_ascii=False, indent=1), encoding="utf-8")
    if deferred:
        (out / "glossary_deferred.json").write_text(
            json.dumps(deferred, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── taxonomy proposal ──
    lines = ["# Taxonomy proposal", "",
             "Counts per category from this run. Approve, rename or merge as you like.", "",
             "| # | Category | Terms |", "|---|---|---:|"]
    for i, c in enumerate(CATEGORIES, 1):
        lines.append(f"| {i} | {c} | {len(by_cat.get(c, []))} |")
    lines += ["", f"**Unclassified ({len(unclear)})** — fitted none of the 14. "
                  "These are the candidates for new groups; clusters below are by shared "
                  "head-word, offered as a starting point rather than a decision.", ""]
    if unclear:
        heads = Counter((r["term"].split()[-1].lower() if r["term"].split() else "?")
                        for r in unclear)
        for head, n in heads.most_common(18):
            if n < 2:
                continue
            ex = [r["term"] for r in unclear if r["term"].lower().endswith(head)][:6]
            lines.append(f"- **…{head}** ({n}): " + ", ".join(ex))
        lines += ["", "<details><summary>All unclassified terms</summary>", "",
                  ", ".join(sorted(r["term"] for r in unclear)), "", "</details>"]
    (out / "taxonomy_proposal.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ── run report ──
    pend, done, failed = store.chunk_counts()
    rep = ["# Overnight glossary run", "",
           f"- started: {meta.get('started')}", f"- finished: {meta.get('finished', 'in progress')}",
           f"- granularity chosen: **{meta.get('granularity', '?')}**",
           f"- chunks: {done} done, {failed} failed, {pend} pending",
           f"- unique terms: {store.term_count()}",
           f"- proposals: auto **{len(auto)}**, queued **{len(queue)}**, deferred {len(deferred)}",
           ""]
    if meta.get("smoke"):
        rep += ["## Granularity smoke test", "",
                "| mode | chunks | secs | raw | unique | unique/min | dup rate |",
                "|---|---:|---:|---:|---:|---:|---:|"]
        for r in meta["smoke"]:
            rep.append(f"| {r['mode']} | {r['chunks']} | {r['secs']} | {r['raw']} | "
                       f"{r['unique']} | {r['uniq_per_min']} | {r['dup_rate']:.0%} |")
        rep.append("")
    if meta.get("stage_times"):
        rep += ["## Stage timings", "", "| stage | minutes |", "|---|---:|"]
        for k, v in meta["stage_times"].items():
            rep.append(f"| {k} | {v/60:.1f} |")
        rep.append("")
    rep += ["## Auto-accept reasons", ""]
    for reason, n in Counter(r["reason"] for r in auto).most_common():
        rep.append(f"- {n} — {reason}")
    rep += ["", "## Queue reasons", ""]
    for reason, n in Counter(r["reason"] for r in queue).most_common():
        rep.append(f"- {n} — {reason}")
    rep += ["", "## Checks", "",
            "- `vanilla CFR` must be QUEUED, not auto-accepted (known-hard calque case)",
            "- spot-check 10 auto-accepted terms against `planning/rawStepsBg/`",
            "- all existing glossary rows should appear in the queue (full audit)", ""]
    (out / "run_report.md").write_text("\n".join(rep) + "\n", encoding="utf-8")

    log(f"   emitted: auto={len(auto)} queue={len(queue)} deferred={len(deferred)} "
        f"unclear={len(unclear)}")
    return {"auto": len(auto), "queue": len(queue), "deferred": len(deferred),
            "unclear": len(unclear)}
