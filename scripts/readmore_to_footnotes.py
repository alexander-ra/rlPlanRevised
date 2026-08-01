#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/readmore_to_footnotes.py
#
# PURPOSE: Retire the "Read more" / "Прочетете повече" callouts now that the
#   chapters carry source footnotes, without losing any reference.
#
#   A callout is a blockquote holding one or more bibliographic references,
#   optionally each followed by a gloss explaining why the source is worth
#   reading. For every reference the script asks: is this work already a
#   footnote in this chapter?
#     - yes -> the callout is redundant; drop it
#     - no  -> mint a footnote for it, anchored to the last sentence of the
#              section the callout was closing, then drop the callout
#
#   Nothing is deleted before its content has a home. A callout whose
#   references cannot all be placed is left alone and reported.
#
#   EN and BG are processed as a pair: callouts are positionally aligned (the
#   files are translations of each other and the counts are verified equal), so
#   both languages get the same footnote keys in the same order, and the
#   Bulgarian gloss survives onto the Bulgarian footnote.
#
# USAGE (run from repo root):
#   python scripts/readmore_to_footnotes.py --dry-run
#   python scripts/readmore_to_footnotes.py
#   python scripts/readmore_to_footnotes.py --step step07
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS = REPO_ROOT / "deliverables" / "reports"

LABEL = {"en": "**Read more:**", "bg": "**Прочетете повече:**"}
FILES = {"en": "summary/summaryEn.md", "bg": "summary/summaryBg.md"}

FOOTNOTE_HEADER = {
    "en": ("<!-- Source footnotes. Definitions may sit anywhere at top level; keeping them\n"
           "     together here keeps the prose readable and the EN/BG pair easy to compare. -->"),
    "bg": ("<!-- Бележки към източниците. Заглавията на чуждоезични източници не се\n"
           "     превеждат (правило 7 от terminology_EN_BG.md). -->"),
}

SEP = " · "
GLOSS = re.compile(r"\s+[—–]\s+|\s+-\s+")
YEAR = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
# A surname: a capitalised Latin word, not an all-caps acronym (NeurIPS, ICML).
SURNAME = re.compile(r"\b([A-Z][a-z]{2,})\b")


def norm_ref(s: str) -> tuple[str, str] | None:
    """A reference reduced to (first surname lowercased, year) - enough to tell
    whether two spellings of the same work are the same work."""
    s = unicodedata.normalize("NFKC", s)
    y = YEAR.search(s)
    n = SURNAME.search(s)
    if not y or not n:
        return None
    return n.group(1).lower(), y.group(1)


def key_for(ref: str) -> str | None:
    k = norm_ref(ref)
    return f"{k[0]}{k[1]}" if k else None


def split_gloss(seg: str) -> tuple[str, str]:
    """-> (reference, gloss). A gloss is prose: several words, not starting with
    a capital or a digit (those are chapter titles and page ranges)."""
    parts = GLOSS.split(seg)
    if len(parts) < 2:
        return seg, ""
    tail = parts[-1]
    if len(tail.split()) < 3 or tail[:1].isupper() or tail[:1].isdigit():
        return seg, ""
    head = seg[: seg.rfind(tail)]
    head = re.sub(r"\s+[—–-]\s*$", "", head).strip()
    return head, tail.strip()


def find_callouts(lines: list[str], label: str) -> list[tuple[int, int, str, str]]:
    """-> [(start, end_exclusive, body, keep)] for each callout blockquote.

    `keep` is text that shared the opening line with the callout and is not part
    of it. Eight callouts in the corpus are glued straight onto the end of the
    preceding sentence ("...through Chapter 8.> **Read more:** ..."), with no
    newline; dropping the whole line there would delete a paragraph.
    """
    out = []
    i = 0
    while i < len(lines):
        if label in lines[i]:
            j = i
            while j + 1 < len(lines) and lines[j + 1].lstrip().startswith(">"):
                j += 1
            head = lines[i].split(label, 1)[0]
            # anything before the blockquote marker on that line is real prose
            keep = head[: head.rfind(">")] if ">" in head else ""
            body_parts = [lines[i].split(label, 1)[1].strip()]
            for k in range(i + 1, j + 1):
                s = lines[k].lstrip()
                body_parts.append(s[1:].strip() if s.startswith(">") else s)
            out.append((i, j + 1, " ".join(x for x in body_parts if x).strip(),
                        keep.rstrip()))
            i = j + 1
        else:
            i += 1
    return out


def existing_keys(text: str) -> dict[tuple[str, str], str]:
    """(surname, year) -> footnote key, for footnotes the file already has."""
    found = {}
    for m in re.finditer(r"^\[\^([\w-]+)\]:\s*(.+)$", text, re.M):
        k = norm_ref(m.group(2))
        if k:
            found[k] = m.group(1)
    return found


def anchor_index(lines: list[str], before: int) -> int | None:
    """Index of the last line of the nearest prose block above `before` that can
    carry a footnote marker. Skips blank lines, blockquotes, images, rules and
    headings - a marker on those either renders badly or reads as unattached."""
    i = before - 1
    while i >= 0:
        s = lines[i].strip()
        if not s or s.startswith((">", "#", "---", "===", "![", "|", ":::", "$$")):
            i -= 1
            continue
        if s.startswith("```") or s.startswith("~~~"):
            return None
        return i
    return None


def process_step(step: str, dry: bool) -> tuple[int, int, list[str]]:
    """-> (callouts removed, footnotes added, problems)"""
    paths = {lg: REPORTS / step / FILES[lg] for lg in ("en", "bg")}
    if not all(p.exists() for p in paths.values()):
        return 0, 0, []

    text = {lg: paths[lg].read_text(encoding="utf-8") for lg in paths}
    lines = {lg: text[lg].splitlines() for lg in paths}
    cal = {lg: find_callouts(lines[lg], LABEL[lg]) for lg in paths}

    problems: list[str] = []
    if len(cal["en"]) != len(cal["bg"]):
        return 0, 0, [f"{step}: {len(cal['en'])} EN vs {len(cal['bg'])} BG callouts; skipped"]
    if not cal["en"]:
        return 0, 0, []

    known = {lg: existing_keys(text[lg]) for lg in paths}
    # new footnote definitions, keyed the same in both languages
    new_defs: dict[str, dict[str, str]] = {lg: {} for lg in paths}
    # per language: line index -> markers to append
    inserts: dict[str, dict[int, str]] = {lg: {} for lg in paths}
    # (start, end, text that shared the opening line and must survive)
    drop: dict[str, list[tuple[int, int, str]]] = {lg: [] for lg in paths}
    added = 0

    for (s_en, e_en, body_en, keep_en), (s_bg, e_bg, body_bg, keep_bg) in zip(
            cal["en"], cal["bg"]):
        segs = {"en": body_en.split(SEP), "bg": body_bg.split(SEP)}
        if len(segs["en"]) != len(segs["bg"]):
            problems.append(f"{step}: callout at EN line {s_en+1} has "
                            f"{len(segs['en'])} vs {len(segs['bg'])} references; left alone")
            continue

        markers: dict[str, list[str]] = {"en": [], "bg": []}
        ok = True
        for seg_en, seg_bg in zip(segs["en"], segs["bg"]):
            ref_en, gloss_en = split_gloss(seg_en.strip())
            ref_bg, gloss_bg = split_gloss(seg_bg.strip())
            k = norm_ref(ref_en)
            if not k:
                problems.append(f"{step}: cannot identify a work in "
                                f"{ref_en[:60]!r}; callout left alone")
                ok = False
                break
            if k in known["en"]:
                key = known["en"][k]          # already footnoted; reuse it
            else:
                key = key_for(ref_en)
                base, n = key, 2
                while any(key in known[lg].values() or key in new_defs[lg]
                          for lg in paths):
                    key = f"{base}{chr(ord('a') + n - 2)}"
                    n += 1
                new_defs["en"][key] = f"{ref_en}{' — ' + gloss_en if gloss_en else ''}"
                new_defs["bg"][key] = f"{ref_bg}{' - ' + gloss_bg if gloss_bg else ''}"
                known["en"][k] = key
                added += 1
            for lg in paths:
                if f"[^{key}]" not in markers[lg]:
                    markers[lg].append(f"[^{key}]")
        if not ok:
            continue

        starts = {"en": s_en, "bg": s_bg}
        ends = {"en": e_en, "bg": e_bg}
        keeps = {"en": keep_en, "bg": keep_bg}
        anchors = {lg: (starts[lg] if keeps[lg] else anchor_index(lines[lg], starts[lg]))
                   for lg in paths}
        if any(a is None for a in anchors.values()):
            problems.append(f"{step}: no anchor paragraph above callout at EN "
                            f"line {s_en+1}; left alone")
            continue
        for lg in paths:
            inserts[lg][anchors[lg]] = inserts[lg].get(anchors[lg], "") + "".join(markers[lg])
            drop[lg].append((starts[lg], ends[lg], keeps[lg]))

    if not any(drop.values()):
        return 0, 0, problems

    removed = len(drop["en"])
    for lg in paths:
        out = list(lines[lg])
        # Salvage first: a line that carried a glued-on callout is replaced by its
        # prose, and that replacement must happen BEFORE markers are appended -
        # doing it after silently discarded the marker and orphaned the footnote.
        salvaged = {a: keep for a, _b, keep in drop[lg] if keep}
        for idx, keep in salvaged.items():
            out[idx] = keep
        for idx, marks in inserts[lg].items():
            s = out[idx].rstrip()
            trail = out[idx][len(s):]
            # keep the marker inside the sentence's final punctuation
            out[idx] = (s + marks + trail) if not s.endswith(("  ",)) else s + marks
        cut = set()
        for a, b, keep in drop[lg]:
            if keep:
                cut.update(range(a + 1, b))
                continue
            cut.update(range(a, b))
            # a callout is usually preceded by a blank line that would be left doubled
            if a - 1 >= 0 and not out[a - 1].strip():
                cut.add(a - 1)
        body = [l for i, l in enumerate(out) if i not in cut]
        newtext = "\n".join(body).rstrip("\n") + "\n"
        if new_defs[lg]:
            if "[^" not in newtext.split("\n")[-3:][0] and FOOTNOTE_HEADER[lg] not in newtext:
                newtext += "\n" + FOOTNOTE_HEADER[lg] + "\n"
            for key, ref in new_defs[lg].items():
                newtext += f"\n[^{key}]: {ref}\n"
        newtext = re.sub(r"\n{3,}", "\n\n", newtext)
        print(f"    {paths[lg].relative_to(REPO_ROOT)}: "
              f"-{len(drop[lg])} callouts, +{len(new_defs[lg])} footnotes")
        if not dry:
            paths[lg].write_text(newtext, encoding="utf-8")

    return removed, added, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--step", default="")
    a = ap.parse_args()

    tot_r = tot_a = 0
    problems: list[str] = []
    for i in range(1, 13):
        step = f"step{i:02d}"
        if a.step and step != a.step:
            continue
        r, n, probs = process_step(step, a.dry_run)
        tot_r += r
        tot_a += n
        problems += probs

    print(f"\n{tot_r} callout(s) retired, {tot_a} footnote(s) added"
          f"{' (dry run)' if a.dry_run else ''}")
    for p in problems:
        print(f"  ! {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
