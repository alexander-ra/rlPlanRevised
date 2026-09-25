#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/bg_typography.py
#
# PURPOSE: Bulgarian typography for the BG sources, in one reviewable pass.
#   The translation pipeline carried over English conventions:
#     - a spaced hyphen " - " as the dash        -> " – " (en dash, no break before)
#     - decimal point 0.571                      -> decimal comma 0,571 ($0{,}571$ in math)
#     - thousands separator 20,000               -> 20 000 (no-break space)
#     - "300 x 500", "4.4x"                      -> "300 × 500", "4,4×"
#
#   Code, URLs, image targets, footnote labels and bibliographic footnote
#   definitions are left alone: DOIs, arXiv ids and page ranges must survive
#   verbatim. Section, figure and version numbers ("раздел 7.5", "v1.6.13",
#   "Melting Pot 2.0") are not decimals and are skipped by context.
#
# Run it ONCE, on text that has not been converted: after the first pass a
#   decimal like 1,234 cannot be told apart from a thousands group.
#
# USAGE (run from repo root):
#   python scripts/bg_typography.py            # dry run: counts + samples
#   python scripts/bg_typography.py --apply
#   python scripts/bg_typography.py --apply --only step07
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
NBSP = " "

FILES = ["summary/summaryBg.md", "summary/onePagerBg.md", "report_bg.md"]

# Protected spans: replaced by placeholders, transformed text, then restored.
PROTECT = [
    re.compile(r"```.*?```", re.S),                  # fenced code
    re.compile(r"<!--.*?-->", re.S),                 # comments
    re.compile(r"`[^`\n]+`"),                        # inline code
    re.compile(r"\]\([^)\s]*\)"),                    # link / image targets
    re.compile(r"\[\^[^\]]+\]"),                     # footnote labels
    re.compile(r"https?://\S+"),                     # URLs
    re.compile(r"\{[#.][^}]*\}"),                    # pandoc attributes {#id .class}
    re.compile(r"\b(?:doi:|DOI:?\s*)?10\.\d{4,}/\S+"),  # DOIs
    re.compile(r"arXiv:\s*\d{4}\.\d{4,5}(?:v\d+)?", re.I),
]
MATH = re.compile(r"\$\$.*?\$\$|\$[^$\n]+\$", re.S)

# A number preceded by one of these words is a label, not a decimal.
LABEL_BEFORE = re.compile(
    r"(?:§|(?<![\wА-Яа-я])(?:[Рр]аздел[аи]?|[Гг]лав[аи]|[Гг]л\.|[Фф]игур[аи]|[Фф]иг\.|"
    r"[Тт]аблиц[аи]|[Тт]абл\.|[Тт]еорем[аи]|[Тт]върдение|[Лл]ема|[Уу]пражнение|"
    r"[Сс]тъпк[аи]|Thm\.?|Prop\.?|Theorem|Proposition|Lemma|Figure|Fig\.|Table|"
    r"Section|Eq\.?|[Уу]равнение|[Вв]ерсия|Python|Pot|OpenSpiel|v|V|[Вв]ер\.))\s*$")
DECIMAL = re.compile(r"(?<![\d.,\w])(-|−)?(\d+)\.(\d+)(?!\d|\.\d)")
THOUSANDS = re.compile(r"(?<![\d.,])(\d{1,3})((?:,\d{3})+)(?!\d|,\d|\.\d)")
TIMES_BETWEEN = re.compile(r"(?<=\d)\s*[xх]\s*(?=\d)")
TIMES_AFTER = re.compile(r"(?<=\d)[xх](?=[\s.,;:)]|$)")
DASH = re.compile(r"(?<=\S) - (?=\S)")


def protect(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def keep(m: re.Match) -> str:
        saved.append(m.group(0))
        return f"\x00{len(saved) - 1}\x00"

    for rx in PROTECT:
        text = rx.sub(keep, text)
    return text, saved


def restore(text: str, saved: list[str]) -> str:
    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m.group(1))], text)
    return text


def decimal_comma(text: str, in_math: bool, stats: dict) -> str:
    def sub(m: re.Match) -> str:
        before = text[max(0, m.start() - 14):m.start()]
        if LABEL_BEFORE.search(before):
            return m.group(0)
        sign = m.group(1) or ""
        stats["decimal"] += 1
        sep = "{,}" if in_math else ","
        return f"{sign}{m.group(2)}{sep}{m.group(3)}"
    return DECIMAL.sub(sub, text)


def thousands(text: str, in_math: bool, stats: dict) -> str:
    def sub(m: re.Match) -> str:
        # Layer sizes like [128,128] or (128,128,128) are tuples, not thousands.
        before = text[m.start() - 1] if m.start() else ""
        after = text[m.end()] if m.end() < len(text) else ""
        groups = [m.group(1)] + m.group(2).lstrip(",").split(",")
        if before in "[=" and before or (before == "(" and after == ")") \
                or (len(groups[0]) == 3 and len(set(groups)) == 1):
            return m.group(0)
        stats["thousands"] += 1
        sep = r"\," if in_math else NBSP
        return m.group(1) + m.group(2).replace(",", sep)
    return THOUSANDS.sub(sub, text)


def prose(text: str, stats: dict) -> str:
    text = thousands(text, False, stats)
    text = decimal_comma(text, False, stats)
    n = len(TIMES_BETWEEN.findall(text)) + len(TIMES_AFTER.findall(text))
    stats["times"] += n
    text = TIMES_BETWEEN.sub(" × ", text)
    text = TIMES_AFTER.sub("×", text)
    stats["dash"] += len(DASH.findall(text))
    text = DASH.sub(f"{NBSP}– ", text)
    return text


def math(segment: str, stats: dict) -> str:
    segment = thousands(segment, True, stats)
    return decimal_comma(segment, True, stats)


def transform_line(line: str, stats: dict) -> str:
    # Bibliographic footnote definitions keep their English-style numbers.
    if re.match(r"\s*\[\^[^\]]+\]:", line):
        return line
    # Table separator rows and horizontal rules are structure, not prose.
    if re.fullmatch(r"\s*\|?[\s:|-]+\|?\s*", line) or re.fullmatch(r"\s*-{3,}\s*", line):
        return line
    out, pos = [], 0
    for m in MATH.finditer(line):
        out.append(prose(line[pos:m.start()], stats))
        out.append(math(m.group(0), stats))
        pos = m.end()
    out.append(prose(line[pos:], stats))
    return "".join(out)


def transform(text: str, stats: dict) -> str:
    text, saved = protect(text)
    lines = [transform_line(l, stats) for l in text.split("\n")]
    return restore("\n".join(lines), saved)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="stepNN")
    args = ap.parse_args()

    total = {"dash": 0, "decimal": 0, "thousands": 0, "times": 0}
    for step_dir in sorted((REPO_ROOT / "deliverables" / "reports").glob("step*")):
        if args.only and step_dir.name != args.only:
            continue
        for rel in FILES:
            f = step_dir / rel
            if not f.exists():
                continue
            old = f.read_text(encoding="utf-8")
            stats = {k: 0 for k in total}
            new = transform(old, stats)
            for k in total:
                total[k] += stats[k]
            if new != old:
                print(f"{f.relative_to(REPO_ROOT)}: " +
                      ", ".join(f"{k} {v}" for k, v in stats.items() if v))
                if not args.apply:
                    shown = 0
                    for a, b in zip(old.split("\n"), new.split("\n")):
                        if a != b and shown < 3:
                            print(f"    - {a.strip()[:110]}")
                            print(f"    + {b.strip()[:110]}")
                            shown += 1
                if args.apply:
                    f.write_text(new, encoding="utf-8")
    print("\ntotal: " + ", ".join(f"{k} {v}" for k, v in total.items())
          + ("" if args.apply else "   (dry run)"))


if __name__ == "__main__":
    main()
