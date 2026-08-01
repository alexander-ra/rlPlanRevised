#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/translate_labels.py
#
# PURPOSE: Fill in the Bulgarian rendering for every figure label extracted by
#   extract_labels.py.
#
#   Two tiers, cheapest first:
#     1. the settled glossary, for terms already arbitrated
#     2. BgGPT, for the rest, with the relevant glossary rows in the prompt
#
#   Every model output passes a gate before it is accepted. A label that loses
#   a number, gains or loses a line break, or renames an algorithm is worse
#   than one left in English: the figure would then contradict the text it sits
#   beside, and nothing downstream would notice.
#
# REQUIREMENTS: a running ollama with bggpt3-27b
#
# USAGE (run from repo root):
#   python scripts/figures/translate_labels.py --dry-run
#   python scripts/figures/translate_labels.py            # resumable
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT / "llmPipeline"))
from core import ollama  # noqa: E402

MODEL = "bggpt3-27b:latest"
LABELS = REPO_ROOT / "scripts" / "figures" / "out" / "figure_labels.json"
GLOSSARY = REPO_ROOT / "llmPipeline" / "glossary_settled.json"
BATCH = 12

# Names that must survive untouched. Latin per the project convention in
# CLAUDE.md and terminology_EN_BG.md.
KEEP_LATIN = re.compile(
    r"\b(CFR\+?|MCCFR|DQN|PPO|SB3|PSRO|MAPPO|MADDPG|QMIX|CTDE|EGTA|NFSP|ARDT|"
    r"LLM|RNR|SES|SLS|AIVAT|piKL|Shapley|OpenSpiel|Goofspiel|"
    r"AlphaStar|AlphaZero|DeepStack|Libratus|Pluribus|ReBeL|CartPole|"
    r"LunarLander|Adam|alpha|beta|tau|epsilon)\b")

# Names this corpus transliterates rather than keeping in Latin - Кун appears
# 142 times against 43 for Kuhn, Ледюк 253 against 86. Requiring the Latin form
# here rejected correct Bulgarian; requiring the Cyrillic one is the real check.
TRANSLITERATED = {"Kuhn": "Кун", "Leduc": "Ледюк", "Nash": "Наш"}

# A label made only of identifiers, numbers and punctuation has nothing to
# translate. "SB3 DQN" and "CFR+" must come through untouched, so absence of
# Cyrillic is the correct outcome, not a failure.
def is_identity(text: str) -> bool:
    stripped = KEEP_LATIN.sub(" ", text)
    stripped = re.sub(r"[\d\W_]+", " ", stripped, flags=re.UNICODE)
    return not stripped.strip()
NUM = re.compile(r"\d+(?:[.,]\d+)?")
MATH = re.compile(r"\$[^$]*\$")

SYSTEM = ("Ти си преводач на надписи в научни графики от английски на български. "
          "Превеждаш кратки етикети за оси, легенди и пояснения в диаграми.")

RULES = """Преведи всеки номериран надпис на български.

ЗАДЪЛЖИТЕЛНО:
- Запази ТОЧНО всички числа и стойности.
- Запази ТОЧНО всички нови редове (\\n). Надписите са разположени в кутии с
  фиксиран размер - смяна на броя редове разваля оформлението.
- Запази имената на алгоритми и системи на латиница: CFR, CFR+, MCCFR, DQN,
  PPO, SB3, PSRO, MAPPO, EGTA, NFSP, ARDT, LLM, Shapley, Kuhn, Leduc,
  Goofspiel, DeepStack, Libratus, Pluribus, ReBeL, OpenSpiel, alpha, tau.
- Запази символите ->, <-, ~, %, ±, стрелки и математиката между $...$.
- Бъди КРАТЪК: това са надписи в графика, не изречения от текст. Ако българският
  става много по-дълъг от английския, съкрати.

ЗАБРАНЕНО:
- да добавяш обяснения, кавички или коментари
- да променяш числа
- да превеждаш имена на алгоритми

Върни РЕДОВЕ във формата:
<номер>|<превод>
Нищо друго.
"""


def load_glossary() -> dict[str, str]:
    by_en: dict[str, str] = {}
    for e in json.loads(GLOSSARY.read_text(encoding="utf-8")):
        by_en.setdefault(e["en"].strip().lower(), e["bg"])
    return by_en


def glossary_hit(text: str, by_en: dict[str, str]) -> str | None:
    """Exact match, then again with a trailing parenthetical removed.

    The whitespace before the parenthetical is carried over verbatim. Collapsing
    it to a space silently rewrapped "Action heads\\n(autoregr.)" onto one line,
    which changes how the box lays out - the same failure the gate rejects
    model output for.
    """
    key = text.strip().lower()
    if key in by_en:
        return by_en[key]
    m = re.search(r"(\s*)\(([^)]*)\)\s*$", text)
    if not m:
        return None
    stripped = text[: m.start()].strip().lower()
    if stripped and stripped in by_en and stripped != key:
        return f"{by_en[stripped]}{m.group(1)}({m.group(2)})"
    return None


def check(src: str, out: str) -> list[str]:
    """Reasons to reject a translation, empty if acceptable."""
    problems = []
    if not re.search(r"[а-яА-Я]", out) and not is_identity(src):
        problems.append("no Cyrillic")
    for latin, cyr in TRANSLITERATED.items():
        if re.search(rf"\b{latin}\b", src) and cyr not in out and latin in out:
            problems.append(f"{latin} not transliterated to {cyr}")
    if Counter(NUM.findall(src)) != Counter(NUM.findall(out)):
        problems.append("numbers changed")
    if src.count("\n") != out.count("\n"):
        problems.append(f"line count {src.count(chr(10))}->{out.count(chr(10))}")
    if Counter(MATH.findall(src)) != Counter(MATH.findall(out)):
        problems.append("math changed")
    lost = Counter(KEEP_LATIN.findall(src)) - Counter(KEEP_LATIN.findall(out))
    if lost:
        problems.append(f"names lost: {sorted(lost)[:3]}")
    if len(out) > max(40, len(src) * 2.2):
        problems.append("far longer than the source")
    return problems


def translate_single(text: str, by_en: dict[str, str]) -> str:
    """One long label at a time, with its shape spelled out.

    The batch prompt loses line structure on the long multi-line annotation
    blocks - the model rewraps them. Stating the exact line count and echoing
    the lines back to it recovers most of those.
    """
    lines = text.split("\n")
    numbered = "\n".join(f"[{i+1}] {ln}" for i, ln in enumerate(lines))
    terms = sorted({f"  {en} -> {bg}" for en, bg in by_en.items()
                    if len(en) > 3 and en in text.lower()})[:25]
    term_block = "\nТерминология:\n" + "\n".join(terms) if terms else ""
    prompt = (
        f"Преведи следния надпис от графика на български.\n\n"
        f"Той има ТОЧНО {len(lines)} реда. Върни ТОЧНО {len(lines)} реда, "
        f"в същия формат [номер] съдържание.\n"
        f"Запази всички числа, стойности, имена на алгоритми (alpha, Shapley, "
        f"CFR, PBS) и математиката между $...$ непроменени.\n"
        f"Не добавяй и не махай редове. Не обяснявай.\n"
        f"{term_block}\n\nНадпис:\n{numbered}\n")
    raw = ollama.generate(MODEL, prompt, system=SYSTEM, temperature=0.1,
                          num_predict=1536, num_ctx=8192, timeout=600).strip()
    out = []
    for ln in raw.splitlines():
        m = re.match(r"\s*\[(\d+)\]\s?(.*)$", ln)
        if m:
            out.append(m.group(2))
    return "\n".join(out) if out else ""


def translate_batch(items: list[str], by_en: dict[str, str]) -> dict[int, str]:
    """Ask the model for one batch; returns index -> translation."""
    terms = []
    for en, bg in by_en.items():
        if len(en) > 3 and any(en in s.lower() for s in items):
            terms.append(f"  {en} -> {bg}")
    term_block = ("\nТерминология (използвай тези съответствия):\n"
                  + "\n".join(sorted(set(terms))[:40])) if terms else ""

    numbered = "\n".join(
        f"{i}|{s}".replace("\n", "\\n") for i, s in enumerate(items))
    prompt = f"{RULES}{term_block}\n\nНадписи:\n{numbered}\n"

    raw = ollama.generate(MODEL, prompt, system=SYSTEM, temperature=0.1,
                          num_predict=2048, num_ctx=8192, timeout=900).strip()
    out: dict[int, str] = {}
    for line in raw.splitlines():
        m = re.match(r"\s*(\d+)\s*\|(.*)$", line)
        if m:
            out[int(m.group(1))] = m.group(2).strip().replace("\\n", "\n")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--single", action="store_true",
                    help="retry whatever is still English, one label per request")
    args = ap.parse_args()

    entries = json.loads(LABELS.read_text(encoding="utf-8"))
    by_en = load_glossary()

    # tier 1 - held to the same gate as the model, since a glossary entry can
    # still be the wrong shape for a figure label (line breaks, lost names)
    from_gloss = gloss_failed = 0
    for e in entries:
        if e.get("bg"):
            continue
        hit = glossary_hit(e["en"], by_en)
        if not hit:
            continue
        if check(e["en"], hit):
            gloss_failed += 1          # fall through to the model
            continue
        e["bg"], e["source"] = hit, "glossary"
        from_gloss += 1
    if gloss_failed:
        print(f"  ({gloss_failed} glossary hits failed the gate, left to the model)")

    # tier 0 - nothing to translate: pure identifiers pass through verbatim
    identity = 0
    for e in entries:
        if not e.get("bg") and is_identity(e["en"]):
            e["bg"], e["source"] = e["en"], "identity"
            e.pop("reject", None)
            identity += 1
    if identity:
        print(f"  ({identity} labels are identifiers only, kept as-is)")

    todo = [e for e in entries if not e.get("bg")]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(entries)} strings | from glossary: {from_gloss} | "
          f"needing the model: {len(todo)}")
    if args.dry_run:
        return

    t0 = time.time()
    accepted = rejected = 0

    if args.single:
        for n, e in enumerate(todo, 1):
            try:
                cand = translate_single(e["en"], by_en)
            except Exception as exc:                  # noqa: BLE001
                print(f"  {n}/{len(todo)} error: {exc}", file=sys.stderr)
                continue
            problems = check(e["en"], cand) if cand else ["no output"]
            if problems:
                rejected += 1
                e["reject"] = "; ".join(problems)
            else:
                e["bg"], e["source"] = cand, "model-single"
                e.pop("reject", None)
                accepted += 1
            print(f"  {n}/{len(todo)} {'ok' if not problems else 'reject'}",
                  flush=True)
            LABELS.write_text(
                json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
        print(f"\nsingle-pass accepted {accepted}, still English "
              f"{sum(1 for e in entries if not e.get('bg'))} "
              f"({(time.time()-t0)/60:.1f} min)")
        return

    for start in range(0, len(todo), BATCH):
        chunk = todo[start:start + BATCH]
        try:
            got = translate_batch([e["en"] for e in chunk], by_en)
        except Exception as exc:                      # noqa: BLE001
            print(f"  batch at {start} failed: {exc}", file=sys.stderr)
            continue
        for i, e in enumerate(chunk):
            cand = got.get(i)
            if not cand:
                rejected += 1
                e["reject"] = "no output"
                continue
            problems = check(e["en"], cand)
            if problems:
                rejected += 1
                e["reject"] = "; ".join(problems)
            else:
                e["bg"], e["source"] = cand, "model"
                e.pop("reject", None)
                accepted += 1
        done = start + len(chunk)
        print(f"  {done}/{len(todo)}  accepted={accepted} rejected={rejected}",
              flush=True)
        LABELS.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")

    dt = time.time() - t0
    print(f"\nglossary {from_gloss} | model {accepted} | rejected {rejected} "
          f"| {dt/60:.1f} min")
    print(f"still English: {sum(1 for e in entries if not e.get('bg'))}")


if __name__ == "__main__":
    main()
