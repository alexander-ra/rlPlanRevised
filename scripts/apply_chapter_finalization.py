"""Apply the candidate's September 2026 Bulgarian terminology picks.

Only source Markdown, glossary values and figure-label overlays are edited. The
English side of a glossary entry is never translated, and the distinction
between bootstrapping an estimate and bootstrap resampling is preserved.
"""

from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "deliverables" / "reports"
LABELS = ROOT / "deliverables" / "finalReview" / "fixes"

# Longest forms first. These are technical uses of self-play and an algorithmic
# oracle in Bulgarian chapter prose, not self-directed study or mythology.
TERMS = [
    ("САМООБУЧЕНИЕ", "ИГРА СРЕЩУ СЕБЕ СИ"),
    ("Самообучението", "Играта срещу себе си"),
    ("самообучението", "играта срещу себе си"),
    ("Самообучение", "Игра срещу себе си"),
    ("самообучение", "игра срещу себе си"),
    ("Самоиграта", "Играта срещу себе си"),
    ("самоиграта", "играта срещу себе си"),
    ("Самоигра", "Игра срещу себе си"),
    ("самоигра", "игра срещу себе си"),
    ("Оракулът", "Предсказвачът"),
    ("оракулът", "предсказвачът"),
    ("Оракула", "Предсказвача"),
    ("оракула", "предсказвача"),
    ("Оракули", "Предсказвачи"),
    ("оракули", "предсказвачи"),
    ("Оракул", "Предсказвач"),
    ("оракул", "предсказвач"),
    ("Оракъл", "Предсказвач"),
    ("оракъл", "предсказвач"),
    ("Стегнат-", "Стегнато-"),
    ("стегнат-", "стегнато-"),
    ("Разпуснат-", "Разпуснато-"),
    ("разпуснат-", "разпуснато-"),
]

GRAMMAR = [
    ("Наивното игра срещу себе си", "Наивната игра срещу себе си"),
    ("наивното игра срещу себе си", "наивната игра срещу себе си"),
    ("наивно игра срещу себе си", "наивна игра срещу себе си"),
    ("Базовото игра срещу себе си", "Базовата игра срещу себе си"),
    ("базовото игра срещу себе си", "базовата игра срещу себе си"),
    ("Обикновеното игра срещу себе си", "Обикновената игра срещу себе си"),
    ("обикновеното игра срещу себе си", "обикновената игра срещу себе си"),
    ("Коректното игра срещу себе си", "Коректната игра срещу себе си"),
    ("коректното игра срещу себе си", "коректната игра срещу себе си"),
    ("коректно игра срещу себе си", "коректна игра срещу себе си"),
    ("Предварителното игра срещу себе си", "Предварителната игра срещу себе си"),
    ("предварителното игра срещу себе си", "предварителната игра срещу себе си"),
    ("самото игра срещу себе си", "самата игра срещу себе си"),
    ("със игра срещу себе си", "с игра срещу себе си"),
    ("играта срещу себе си не е възможно", "играта срещу себе си не е възможна"),
    ("играта срещу себе си е дадено", "играта срещу себе си е представена"),
    ("играта срещу себе си (базова линия), което", "играта срещу себе си (базова линия), която"),
    ("играта срещу себе си, което", "играта срещу себе си, която"),
    ("играта срещу себе си с бутстрапинг", "играта срещу себе си със самоподкрепяне"),
    ("за буутстрапинг на", "за самоподкрепяне на"),
    ("коректната игра срещу себе си**, което", "коректната игра срещу себе си**, която"),
    ("фиктивна игра с игра срещу себе си", "игра срещу себе си по метода на фиктивната игра"),
    ("**AlwaysPass** (`AlwaysPass`; ", "**AlwaysPass** ("),
    ("хетерогенно антагонистично игра срещу себе си", "хетерогенна антагонистична игра срещу себе си"),
    ("правилно игра срещу себе си", "коректна игра срещу себе си"),
    ("играта срещу себе си на GPU, с което се обучава", "играта срещу себе си на GPU, чрез която се обучава"),
    ("Партия с игра срещу себе си:", "Партия срещу себе си:"),
    ("самообучаваща се популация", "популация, обучавана чрез игра срещу себе си"),
]

AUTHORS = [
    ("Блекуел", "Blackwell"), ("Харт и Мас-Колел", "Hart и Mas-Colell"),
    ("Чен и Анкенман", "Chen и Ankenman"),
    ("Сътон", "Sutton"), ("Сътън", "Sutton"), ("Барто", "Barto"),
    ("Торндайк", "Thorndike"), ("Самюел", "Samuel"),
    ("Уоткинс", "Watkins"), ("Шмид", "Schmid"),
    ("Ганцфрид", "Ganzfried"), ("Сандхолм", "Sandholm"),
    ("Йохансон", "Johanson"), ("Хауснер", "Hausner"),
    ("Шубик", "Shubik"),
]


def substitute_names(value: str, chapter: str) -> str:
    for old, new in AUTHORS:
        value = value.replace(old, new)
    # These two personal names also name concepts throughout the corpus. Only
    # the explicit list of the So Long Sucker authors is changed.
    value = value.replace("Hausner, Наш, Шапли и Shubik", "Hausner, Nash, Shapley и Shubik")
    value = value.replace("Hausner, Наш, Шапли, Shubik", "Hausner, Nash, Shapley, Shubik")
    value = value.replace("Наш (1950)[^nash1950]", "Nash (1950)[^nash1950]")
    if chapter in {"step07", "step08"}:
        lines = value.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if "камък-ножица-хартия" in line.lower():
                continue
            for old, new in (("Камък", "Rock"), ("камъкът", "Rock"),
                             ("камъка", "Rock"), ("камък", "Rock"),
                             ("Маниак", "Maniac"), ("маниакът", "Maniac"),
                             ("маниака", "Maniac"), ("маниак", "Maniac")):
                line = line.replace(old, new)
            line = line.replace("„Rock“", "Rock").replace("„Maniac“", "Maniac")
            if chapter == "step08":
                line = line.replace("Винаги пасува", "AlwaysPass")
            lines[i] = line
        value = "".join(lines)
        if chapter == "step07":
            value = value.replace("| Кун | Rock → Maniac |", "| Кун | TightPassive → LooseAggressive |")
            value = value.replace("| Кун | Стегнато-пасивен → Свободно-агресивен |",
                                  "| Кун | TightPassive → LooseAggressive |")
        if chapter == "step08":
            value = value.replace("| **Стегнато-пасивен** |", "| **TightPassive** |")
            value = value.replace("| **Разпуснато-агресивен** |", "| **LooseAggressive** |")
            value = value.replace("**Винаги залага** (`AlwaysBet`)", "**AlwaysBet**")
    if chapter == "step12":
        for old, new in (("„Винаги пас“", "AlwaysPass"),
                         ("„Винаги залог“", "AlwaysBet"),
                         ("„Случаен“", "Random"),
                         ("„Стегнато-пасивен“", "TightPassive")):
            value = value.replace(old, new)
    return value


def read(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as f:
        return f.read()


def write_if_changed(path: Path, before: str, after: str) -> None:
    if after != before:
        with path.open("w", encoding="utf-8", newline="") as f:
            f.write(after)
        print(path.relative_to(ROOT))


def substitute_terms(value: str) -> str:
    for old, new in TERMS:
        value = value.replace(old, new)
    for old, new in GRAMMAR:
        value = value.replace(old, new)
    return value


def substitute_figure_label(value: str) -> str:
    value = substitute_names(substitute_terms(value), "")
    value = value.replace("План-стратегия — ясна", "План — ясен")
    value = value.replace("План-стратегия — подробна", "План — подробен")
    value = value.replace("все по-неясна на", "все по-неясен на")
    value = value.replace("все по-груба", "все по-груб")
    value = value.replace("груба за кръгове", "груб за кръгове")
    value = value.replace("играе се директно", "използва се директно")
    return value


def update_bg_markdown() -> None:
    for path in sorted(REPORTS.glob("step??/**/*")):
        if not path.is_file() or path.suffix != ".md":
            continue
        if path.name not in {"report_bg.md", "summaryBg.md", "onePagerBg.md"}:
            continue
        before = read(path)
        after = substitute_terms(before)
        after = substitute_names(after, path.parent.parent.name if path.name != "report_bg.md" else path.parent.name)
        after = after.replace("холдем", "Холдем")
        after = re.sub(r"(?m)^(.*Johanson.*?)[ \t]+(\r?)$", r"\1\2", after)
        chapter = path.parent.parent.name if path.name != "report_bg.md" else path.parent.name
        if chapter == "step01" and path.name == "summaryBg.md":
            after = after.replace("използвайки самоподкрепяне:",
                                  "използвайки самоподкрепяне (bootstrapping):", 1)
        if chapter == "step01" and path.name == "report_bg.md":
            after = after.replace("стойностите от буутстрапинга",
                                  "стойностите от самоподкрепянето (bootstrapping)", 1)
        if chapter == "step06" and path.name == "summaryBg.md":
            after = after.replace("играта срещу себе си със самоподкрепяне на AlphaZero",
                                  "играта срещу себе си със самоподкрепяне (bootstrapping) на AlphaZero", 1)
        # The choice for blueprint is “план”. This is the only compound variant
        # introduced by the translation pipeline; ordinary “схема” may mean a
        # diagram or a procedure and is left for contextual review.
        after = after.replace("план-стратегия", "план")
        # Only the RL bootstrapping sense: the chapter also discusses a
        # distinct statistical bootstrap with replacement.
        after = after.replace("целта с бутстрапиране", "целта със самоподкрепяне")
        after = after.replace("**целеви стойности по метода „bootstrap“**", "**целеви стойности чрез самоподкрепяне**")
        after = after.replace("*самоподкрепяне*. Актуализация", "*самоподкрепяне (bootstrapping)*. Актуализация")
        # Use the visible chapter heading for both forms in the six flagged
        # summaries. Keep the existing metadata prefix and punctuation.
        if path.name == "summaryBg.md" and path.parent.parent.name in {
            "step02", "step04", "step09", "step10", "step11", "step12"
        }:
            title = re.search(r'(?m)^title: "([^"\r]+)"\r?$', after)
            heading = re.search(r"(?m)^# (Глава \d+\s*[–—-]\s*[^\r\n]+)\r?$", after)
            if title and heading:
                visible = re.sub(r"^Глава (\d+)\s*[–—-]\s*", r"Глава \1 Обобщение – ", heading.group(1))
                after = after[:title.start(1)] + visible + after[title.end(1):]
        write_if_changed(path, before, after)


def update_labels() -> None:
    for path in sorted(LABELS.glob("labels_step??.json")):
        before = read(path)
        data = json.loads(before)
        after_data = {
            key: substitute_figure_label(value) if isinstance(value, str) else value
            for key, value in data.items()
        }
        chapter = path.stem.removeprefix("labels_")
        if chapter == "step07":
            for name in ("Rock", "Maniac", "Calling station", "Loose-passive",
                         "Random", "Level-1", "Level-2"):
                if name in after_data:
                    after_data[name] = name
        if chapter == "step08":
            for key, value in list(after_data.items()):
                if key in {"exploitation profit (EV vs TightPassive)", "EV vs TightPassive"}:
                    after_data[key] = value.replace("„камък“", "TightPassive")
        if chapter == "step12":
            for name in ("AlwaysPass", "AlwaysBet", "TightPassive",
                         "LooseAggressive", "Thresholdish", "Random"):
                if name in after_data:
                    after_data[name] = name
        # Preserve the file's indentation and ordering rather than reformatting
        # the whole overlay merely to change a few values.
        after = before
        for key, value in data.items():
            if after_data[key] != value:
                after = after.replace(json.dumps(value, ensure_ascii=False), json.dumps(after_data[key], ensure_ascii=False))
        write_if_changed(path, before, after)


def update_base_figure_labels() -> None:
    path = ROOT / "scripts" / "figures" / "out" / "figure_labels.json"
    before = read(path)
    entries = json.loads(before)
    after = before
    agent_names = {
        "Rock", "Maniac", "AlwaysPass", "AlwaysBet", "TightPassive",
        "LooseAggressive", "Thresholdish", "Random", "Calling station",
        "Loose-passive", "Level-1", "Level-2",
    }
    for entry in entries:
        old = entry.get("bg")
        if not isinstance(old, str):
            continue
        new = entry["en"] if entry.get("en") in agent_names else substitute_figure_label(old)
        if new != old:
            old_json = '"bg": ' + json.dumps(old, ensure_ascii=False)
            new_json = '"bg": ' + json.dumps(new, ensure_ascii=False)
            after = after.replace(old_json, new_json)
    write_if_changed(path, before, after)


def update_settled_glossary() -> None:
    db = ROOT / "llmPipeline" / "out" / "glossary.db"
    con = sqlite3.connect(db)
    rows = con.execute("""SELECT t.key, t.term, COALESCE(pk.bg, p.chosen)
        FROM terms t JOIN proposals p ON p.key = t.key
        LEFT JOIN picks pk ON pk.key = t.key
        WHERE COALESCE(pk.bg, p.chosen) IS NOT NULL""").fetchall()
    changed = 0
    for key, term, bg in rows:
        en = term.lower()
        new = bg
        if "self-play" in en or "self play" in en:
            new = substitute_terms(new)
        if "blueprint" in en:
            new = new.replace("план-стратегия", "план").replace("таблична схема", "табличен план")
        if en == "bootstrapped target":
            new = "цел със самоподкрепяне"
        elif en == "bootstrapping":
            new = "самоподкрепяне"
        if "hold'em" in en:
            new = new.replace("холдем", "Холдем")
            new = {
                "heads-up no-limit hold'em": "безлимитен Холдем за двама",
                "heads-up no-limit texas hold'em": "безлимитен тексаски Холдем за двама",
                "no-limit hold'em": "безлимитен Холдем",
                "no-limit texas hold'em": "безлимитен тексаски Холдем",
            }.get(en, new)
        if new == bg:
            continue
        con.execute("""INSERT INTO picks
            (key,bg,status,keep_latin,first_use,note,stage,ts)
            VALUES (?,?,?,0,1,?,?,?)
            ON CONFLICT(key) DO UPDATE SET
                bg=excluded.bg,status=excluded.status,
                note=excluded.note,stage=excluded.stage,ts=excluded.ts""",
            (key, new, "picked", "Candidate finalization choice, 2026-09-25", "finalization", time.time()))
        changed += 1
    con.commit()
    con.close()
    print(f"Updated {changed} working-glossary picks")
    subprocess.run([sys.executable, str(ROOT / "llmPipeline" / "export_glossary.py")],
                   cwd=ROOT, check=True)


if __name__ == "__main__":
    update_bg_markdown()
    update_labels()
    update_base_figure_labels()
    update_settled_glossary()
