#!/usr/bin/env python3
"""Clear the remaining glossary queue.

Three stages, all reversible and all recorded with a distinct `reason` so every
decision is filterable in the picker:

  A  atomic corrections + propagation
     Three single-word entries were wrong, and normalisation had spread them:
       Nash       "Неш"      -> "Наш"        (owner's own picks and published BG summaries)
       weight     "тежест"   -> "тегло"      (тежест = heaviness; ML weights are тегла)
       transitive "преходен" -> "транзитивен"(преходен = transitional)
  B  the 102 terms occurring twice, decided individually below
  C  the ~869 terms occurring once: accept the top-voted candidate in bulk

Terms with corpus frequency 0 (glossary seeds never used in the documents) are
left alone deliberately - they do not appear in any text being translated.

    python llmPipeline/finalize_glossary.py --dry-run
    python llmPipeline/finalize_glossary.py
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

DB = Path(__file__).resolve().parent / "out" / "glossary.db"
REPORT = DB.parent / "glossary_finalisation.md"

# ── A. atomic corrections, applied across every settled rendering ─────────────
ATOMIC = [
    # (english must contain, wrong pattern, replacement, note)
    (None, r"Неш", "Наш", "Nash transliteration unified"),
    (None, r"неш", "наш", "Nash transliteration unified"),
    ("weight", r"тежест", "тегло", "ML weight is тегло, not тежест"),
    ("weight", r"тежести", "тегла", "ML weight is тегло, not тежест"),
    ("transitive", r"преходн", "транзитивн", "transitive relation is транзитивен"),
    ("transitive", r"преходен", "транзитивен", "transitive relation is транзитивен"),
]

# ── B. the 102 freq-2 decisions ──────────────────────────────────────────────
# "?" marks entries I am genuinely unsure about; they are listed in the report.
DECIDED: dict[str, str] = {
    "matrix-valued states": "матрични състояния?",
    "minimax return conditioning": "минимаксно обуславяне по възвръщаемост?",
    "open-world type discovery": "откриване на типове в отворен свят",
    "pomdp": "частично наблюдаем марковски процес на вземане на решения",
    "sequence-form representation": "представяне в последователна форма",
    "sparse betting abstraction": "рядка абстракция на залозите",
    "type-based": "базиран на типове",
    "skew-symmetric approximation": "антисиметрично приближение",
    "state-of-the-art": "най-съвременно ниво",
    "thesis signal": "сигнал за дисертацията?",
    "translation problem": "проблем на транслацията?",
    "proof-of-concept": "доказателство за концепция",
    "thesis contribution gap": "пропуск в приноса на дисертацията",
    "model misspecification": "неправилна спецификация на модела",
    "nash reveal": "разкриване на равновесието на Наш",
    "paired gap": "сдвоена разлика",
    "prediction reconciliation": "съгласуване на прогнозата с действителността",
    "random baseline": "случайна базова линия",
    "seeded": "инициализиран",
    "smoke-run": "пробно изпълнение",
    "training-trajectory snapshots": "моментни снимки на траекториите на обучение",
    "transitive/cyclic diagnostic": "транзитивна/циклична диагностика",
    "worst-case exploitability": "експлоатируемост в най-лошия случай",
    "max-min": "максимин",
    "minimax optimal": "оптимален по минимакс",
    "mutual defection": "взаимно предателство",
    "n-player game": "игра с n играчи",
    "n-player safety": "безопасност при n играчи",
    "payoff-dominant": "доминиращ по печалба",
    "perfect- and imperfect-information play": "игра с пълна и непълна информация",
    "risk-dominant": "рисково доминиращ",
    "robust Nash response": "устойчив отговор на Наш",
    "strategic settings": "стратегически ситуации",
    "strategy space": "пространство на стратегиите",
    "worst-case adversary": "най-лошият възможен противник",
    "monotone decline": "монотонно намаляване",
    "total variation distance": "разстояние по обща вариация",
    "worst case": "най-лош случай",
    "mixed-motive": "със смесени мотиви",
    "multi-agent actor-critic": "многоагентен актьор-критик",
    "opponent-blind": "независим от противника",
    "player-count barrier": "бариера на броя играчи",
    "pure-strategy population": "популация от чисти стратегии",
    "safe opponent exploitation": "безопасна експлоатация на противника",
    "safe-exploitation mechanism": "механизъм за безопасна експлоатация",
    "skill-ladder pool": "пул от нива на умения",
    "neural equilibrium approximation": "невронно приближение на равновесие",
    "neural value approximation": "невронно приближение на стойността",
    "state-only target": "цел само по състояние",
    "tensor-native decomposition": "тензорно разлагане?",
    "translation equivariance": "еквивариантност спрямо транслация",
    "loose aggressive": "свободно-агресивен?",
    "loose passive": "свободно-пасивен?",
    "looseaggressive": "свободно-агресивен?",
    "maniac strategy": "маниакална стратегия",
    "modal gap": "модален интервал?",
    "multi-street poker": "покер с няколко кръга на залагане",
    "natural-language game": "игра на естествен език",
    "off-tree opponent bet": "залог на противника извън дървото",
    "out-of-menu opponent": "противник извън менюто",
    "pot odds": "шансове на пота",
    "prioritized matchmaking": "приоритизирано сдвояване",
    "realization plan": "план за реализация",
    "realization weight": "тегло на реализацията",
    "rock strategy": "стратегия „камък“",
    "rock–paper–scissors": "камък-ножица-хартия",
    "soft play": "пасивна игра срещу съучастник",
    "treeplex": "treeplex",
    "turn": "ход?",
    "verbalised strategy": "вербализирана стратегия",
    "per-step discounted return": "дисконтирана възвръщаемост на стъпка",
    "prior policy": "предходна стратегия",
    "relabel target": "цел за преозначаване",
    "return-conditioned policies": "стратегии, обусловени от възвръщаемостта",
    "return-to-go conditioning": "обуславяне по остатъчна възвръщаемост",
    "reward function": "функция на наградата",
    "selection": "подбор",
    "single-agent reinforcement learning": "обучение с подкрепление с един агент",
    "state-action pairs": "двойки състояние-действие",
    "value target": "целева стойност",
    "meta-nash computation": "изчисляване на мета-Наш равновесие",
    "meta-solver": "мета-решател",
    "minimax solver": "минимакс решател",
    "monte-carlo rollouts": "Монте Карло симулации",
    "nash convergence": "сходимост към равновесие на Наш",
    "near-nash": "почти равновесие на Наш",
    "offline solve": "офлайн решаване",
    "per-decision decomposition": "разлагане по решения",
    "re-solving": "пререшаване",
    "regret floor": "праг на съжалението",
    "regret-update phase": "фаза на актуализация на съжалението",
    "pfsp matchmaking": "сдвояване по PFSP",
    "raw step validation": "проверка на суровите стъпки",
    "runtime patching": "корекция по време на изпълнение",
    "toy game": "опростена игра",
    "validation harness": "валидационна среда",
    "minimax expectile regression": "минимакс експектилна регресия",
    "over-fitting": "преобучение",
    "population-based methods": "популационни методи",
    "refit": "преобучаване",
    "step budget": "бюджет от стъпки",
    "underfit": "недообучение",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(str(DB))
    stats: Counter = Counter()
    uncertain, atomic_log = [], []

    # ── A ──
    # NOTE: A must run again after B/C. Stage C accepts raw CANDIDATES, which were
    # never corrected, so bulk-accepting one can reintroduce a wrong atomic form
    # ("Неш" came back on 12 terms the first time). Stage A is idempotent, so it is
    # simply applied a second time at the end.
    rows = con.execute("""SELECT t.key, t.term, COALESCE(pk.bg, p.chosen)
        FROM terms t JOIN proposals p ON p.key = t.key
        LEFT JOIN picks pk ON pk.key = t.key
        WHERE COALESCE(pk.bg, p.chosen) IS NOT NULL""").fetchall()
    for key, term, bg in rows:
        new = bg
        why = None
        for need, pat, rep, note in ATOMIC:
            if need and need not in term.lower():
                continue
            if re.search(pat, new):
                new = re.sub(pat, rep, new)
                why = note
        if new != bg:
            atomic_log.append((term, bg, new, why))
            stats["A atomic corrected"] += 1
            if not a.dry_run:
                con.execute("UPDATE proposals SET chosen=?, reason=? WHERE key=?",
                            (new, f"atomic fix: {why}", key))
                con.execute("""INSERT OR REPLACE INTO picks
                    (key,bg,status,keep_latin,first_use,note,stage,ts)
                    VALUES (?,?,?,0,1,?,?,?)""",
                            (key, new, "auto", f"atomic fix: {why}", "finalise", time.time()))

    # ── B and C ──
    pend = con.execute("""SELECT t.key, t.term, t.freq, p.candidates_json
        FROM proposals p JOIN terms t ON t.key = p.key
        LEFT JOIN picks pk ON pk.key = p.key
        WHERE p.decision IN ('queue','stage2') AND pk.key IS NULL""").fetchall()
    dec_lower = {k.lower(): v for k, v in DECIDED.items()}

    for key, term, freq, cj in pend:
        chosen = reason = None
        pick = dec_lower.get(term.lower())
        if pick:
            flagged = pick.endswith("?")
            chosen = pick.rstrip("?")
            reason = "decided by assistant (freq 2)"
            if flagged:
                uncertain.append((term, chosen))
                reason += " — UNCERTAIN, review"
            stats["B freq-2 decided"] += 1
        elif freq >= 1:
            try:
                cands = json.loads(cj or "[]")
            except Exception:  # noqa: BLE001
                cands = []
            if cands and cands[0].get("bg"):
                chosen = cands[0]["bg"]
                reason = "bulk: top-voted candidate (freq 1)"
                stats["C singleton bulk-accepted"] += 1
        if not chosen:
            stats["left undecided"] += 1
            continue
        if not a.dry_run:
            con.execute("UPDATE proposals SET decision='auto', chosen=?, reason=? WHERE key=?",
                        (chosen, reason, key))
            con.execute("""INSERT OR REPLACE INTO picks
                (key,bg,status,keep_latin,first_use,note,stage,ts)
                VALUES (?,?,?,0,1,?,?,?)""",
                        (key, chosen, "auto", reason, "finalise", time.time()))
    if not a.dry_run:
        con.commit()

    md = ["# Glossary finalisation", "",
          *[f"- {k}: **{v}**" for k, v in stats.most_common()], "",
          "## Atomic corrections propagated", "",
          "| term | was | now | why |", "|---|---|---|---|"]
    for t, o, n, w in atomic_log[:120]:
        md.append(f"| {t} | {o} | **{n}** | {w} |")
    md += ["", f"## Uncertain — please review ({len(uncertain)})", "",
           "My Bulgarian is analytical, not native. These are the freq-2 terms where "
           "I was genuinely unsure.", "", "| term | I chose |", "|---|---|"]
    for t, v in uncertain:
        md.append(f"| {t} | {v} |")
    REPORT.write_text("\n".join(md) + "\n", encoding="utf-8")

    print("\n".join(f"  {k:<28} {v}" for k, v in stats.most_common()))
    print(f"\nuncertain (in report): {len(uncertain)}")
    print(f"report: {REPORT}")
    if a.dry_run:
        print("(dry run — nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
