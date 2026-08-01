#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/add_table_captions.py
#
# PURPOSE: Give every table a caption, so every table gets a number.
#
#   Pandoc only numbers a table that has a caption - an uncaptioned pipe table
#   renders as an unnumbered longtable. The corpus had 42 tables and no
#   captions, so nothing could be referred to as "Таблица N".
#
#   Captions are written from what each table actually shows, EN first and BG
#   mirrored through terminology_EN_BG.md. They are keyed by position: the Nth
#   table in a file, which is stable as long as no table is inserted above one.
#   A count mismatch aborts that file rather than captioning the wrong table.
#
# USAGE (run from repo root):
#   python scripts/add_table_captions.py --dry-run
#   python scripts/add_table_captions.py
#   python scripts/add_table_captions.py --review   # write the review table only
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS = REPO_ROOT / "deliverables" / "reports"
REVIEW = REPORTS / "TABLE_CAPTIONS_REVIEW.md"

# step -> [(en, bg)] in file order
CAPTIONS: dict[str, list[tuple[str, str]]] = {
 "step03": [
  ("Minimax with alpha-beta pruning against MCTS, across five properties.",
   "Минимакс с алфа-бета отсичане срещу MCTS по пет характеристики."),
  ("Kuhn and Leduc Poker compared: cards, betting rounds, information sets and tree size.",
   "Сравнение между Кун и Ледюк покер: карти, кръгове на залагане, информационни множества и размер на дървото."),
  ("External and outcome sampling: what each variant samples at every node type, and the resulting cost per iteration.",
   "Извадка по външни възли и извадка по резултати: какво взема всеки вариант при всеки тип възел и произтичащата цена на итерация."),
  ("Measured convergence constants for the four solvers, per iteration and in wall-clock terms.",
   "Измерени константи на сходимост за четирите решавача - на итерация и в реално време."),
  ("Game size at which MCCFR overtakes vanilla CFR, per sampling variant.",
   "Размер на играта, при който MCCFR изпреварва обикновения вариант на CFR, по вариант на извадката."),
  ("The crossover threshold applied to three real games.",
   "Прагът на пресичане, приложен към три реални игри."),
 ],
 "step04": [
  ("The explicit and implicit routes to abstraction, compared on every practical axis.",
   "Явният и неявният път към абстракцията, сравнени по всеки практически показател."),
 ],
 "step05": [
  ("Families of neural methods for imperfect-information games: core idea, where each fits, and its cost.",
   "Семейства невронни методи за игри с непълна информация: основна идея, приложимост и цена."),
 ],
 "step06": [
  ("DeepStack (2017) at a glance.", "DeepStack (2017) накратко."),
  ("Libratus (2017/2018) at a glance.", "Libratus (2017/2018) накратко."),
  ("Pluribus (2019) at a glance.", "Pluribus (2019) накратко."),
  ("ReBeL (2020) at a glance.", "ReBeL (2020) накратко."),
  ("Student of Games (2023) at a glance.", "Student of Games (2023) накратко."),
  ("The five systems in sequence: what each added, and what it gave up for it.",
   "Петте системи по ред: какво добавя всяка и от какво се отказва за него."),
 ],
 "step07": [
  ("Exploitation headroom in Kuhn: Nash EV, best-response EV, and the gap between them, per opponent type.",
   "Потенциал за експлоатация в Кун: очаквана стойност при равновесие на Наш, при най-добър отговор и разликата между тях, по тип опонент."),
  ("The opponent type zoo: the behaviour of each fixed style.",
   "Зоологическата градина от типове опоненти: поведението на всеки постоянен стил."),
  ("The three opponent models compared on representation, convergence, robustness, interpretability and cost.",
   "Трите модела на противника, сравнени по представяне, сходимост, устойчивост, интерпретируемост и цена."),
  ("Detector reliability over 300 seeds of 500 hands each.",
   "Надеждност на детектора при 300 семена по 500 раздавания."),
  ("Kuhn: the exploitation ceiling against what each model actually realised.",
   "Кун: таванът на експлоатация спрямо реално постигнатото от всеки модел."),
  ("Leduc: the exploitation ceiling against what each model actually realised.",
   "Ледюк: таванът на експлоатация спрямо реално постигнатото от всеки модел."),
  ("Static against change-point forgetting, after a mid-match style switch.",
   "Статичен модел срещу забравяне при точка на промяна, след смяна на стила по средата на мача."),
 ],
 "step08": [
  ("Three safety notions: the floor each guarantees, what it requires, and where it is weak.",
   "Три понятия за безопасност: прагът, който всяко гарантира, какво изисква и къде е слабо."),
  ("Restricted Nash Response across the mixing parameter: the canonical form against a naive blend.",
   "Ограничен отговор по Наш по стойността на параметъра на смесване: каноничната форма срещу наивно смесване."),
  ("Kuhn: expected value and worst-case value for every method against every opponent.",
   "Кун: очаквана стойност и стойност в най-лошия случай за всеки метод срещу всеки опонент."),
  ("Leduc: the subgame method against the global solvers.",
   "Ледюк: методът с под-игри срещу глобалните решавачи."),
  ("The teaching attack: realised profit and safety violations per method.",
   "Обучаващата атака: реализирана печалба и нарушения на безопасността по метод."),
 ],
 "step09": [
  ("The MARL method families: what each does, when to reach for it, and its main weakness.",
   "Семействата методи в MARL: какво прави всеки, кога да се използва и основната му слабост."),
  ("Independent learners on four matrix games, against the analytic Nash equilibrium.",
   "Самостоятелно обучаващи се агенти върху четири матрични игри, спрямо аналитичното равновесие на Наш."),
  ("Centralised against independent critics: the final value-loss residual.",
   "Централизиран срещу самостоятелен оценител: краен остатък от загубата на стойност."),
  ("PSRO exploitability trajectory, per game family.",
   "Траектория на експлоатируемостта при PSRO, по семейство игри."),
  ("Learned communication: team reward with the channel on and off.",
   "Научена комуникация: отборна награда при включен и изключен канал."),
  ("LOLA against naive learners on the iterated Prisoner's Dilemma.",
   "LOLA срещу наивно обучаващи се агенти в повторената дилема на затворника."),
 ],
 "step10": [
  ("The population-based method families: what each does, when to reach for it, and its main weakness.",
   "Семействата методи, базирани на популации: какво прави всеки, кога да се използва и основната му слабост."),
  ("Replicator dynamics on four symmetric games, against the analytic reference.",
   "Репликаторна динамика върху четири симетрични игри, спрямо аналитичната референция."),
  ("Transitive and cyclic components of four populations, by combinatorial-Hodge decomposition.",
   "Транзитивни и циклични компоненти на четири популации чрез комбинаторна декомпозиция на Ходж."),
  ("League training metrics at both scales.",
   "Показатели от обучението на лигата при двата мащаба."),
  ("Mini-PBT diversity over generations, on a transitive and on a cyclic game.",
   "Разнообразие при мини-PBT през поколенията - върху транзитивна и върху циклична игра."),
  ("Meta-Nash exploitability against the best individual agent, per configuration.",
   "Експлоатируемост на мета-Наш сместа спрямо най-добрия отделен агент, по конфигурация."),
  ("Final Leduc exploitability, by method.",
   "Крайна експлоатируемост в Ледюк, по метод."),
 ],
 "step11": [
  ("Shapley value and core stability on two cooperative-game toys.",
   "Стойност на Шапли и стабилност на ядрото при два опростени кооперативни модела."),
  ("Paired coalition-score gap of Shapley credit over the sparse baseline, per regime.",
   "Сдвоена разлика в коалиционния резултат на разпределението по Шапли спрямо разредената базова линия, по режим."),
  ("Cyclic ratio and structure of two SLS populations.",
   "Циклично съотношение и структура на две популации в SLS."),
 ],
}

FILES = {"en": ("summary/summaryEn.md", 0), "bg": ("summary/summaryBg.md", 1)}
SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$")


def table_ends(lines: list[str]) -> list[int]:
    """Index just past the last row of each pipe table, in file order."""
    ends = []
    i = 0
    while i < len(lines):
        if SEP_RE.match(lines[i]) and i > 0 and lines[i - 1].lstrip().startswith("|"):
            j = i + 1
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            ends.append(j)
            i = j
        else:
            i += 1
    return ends


def process(step: str, lang: str, dry: bool) -> str | None:
    rel, idx = FILES[lang]
    p = REPORTS / step / rel
    if not p.exists() or step not in CAPTIONS:
        return None
    lines = p.read_text(encoding="utf-8").splitlines()
    ends = table_ends(lines)
    want = CAPTIONS[step]
    if len(ends) != len(want):
        return (f"{step} {lang}: {len(ends)} table(s) in the file but "
                f"{len(want)} caption(s) defined — skipped")

    # walk backwards so earlier indices stay valid
    for end, (en, bg) in zip(reversed(ends), reversed(want)):
        caption = (en, bg)[idx]
        if end < len(lines) and lines[end].lstrip().startswith(": "):
            lines[end] = f": {caption}"          # replace an existing caption
            continue
        lines.insert(end, f": {caption}")
        lines.insert(end, "")
    if not dry:
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return None


def write_review() -> None:
    L = ["# Надписи на таблиците - за преглед\n",
         f"{sum(len(v) for v in CAPTIONS.values())} таблици. Надписът е това, което "
         "прави таблицата *номерирана* - pandoc не номерира таблица без надпис.\n",
         "Английският е написан от съдържанието на таблицата; българският го следва "
         "през `terminology_EN_BG.md`.\n"]
    for step in sorted(CAPTIONS):
        L.append(f"\n## {step}  ({len(CAPTIONS[step])})\n")
        L.append("| # | Английски | Български |")
        L.append("|---|---|---|")
        for n, (en, bg) in enumerate(CAPTIONS[step], 1):
            L.append(f"| {n} | {en} | {bg} |")
    REVIEW.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"  wrote {REVIEW.relative_to(REPO_ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--review", action="store_true", help="only write the review file")
    a = ap.parse_args()

    if a.review:
        write_review()
        return 0

    problems = []
    for step in sorted(CAPTIONS):
        for lang in ("en", "bg"):
            err = process(step, lang, a.dry_run)
            if err:
                problems.append(err)
    total = sum(len(v) for v in CAPTIONS.values()) * 2
    print(f"{total} caption(s) applied{' (dry run)' if a.dry_run else ''}")
    for p in problems:
        print(f"  ! {p}", file=sys.stderr)
    if not a.dry_run and not problems:
        write_review()
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
