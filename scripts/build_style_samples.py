#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/build_style_samples.py
#
# PURPOSE: Render one sample document five times, under five different
#   preambles, so the look of the bundle can be chosen by seeing it rather than
#   described.
#
#   The sample exercises every element the summaries bundle contains - three
#   heading levels, prose, inline and display maths, a captioned figure, a
#   captioned table, a callout, a glossary term at first mention, a source
#   footnote, a code span and a list - using real chapter content, so the
#   Bulgarian and the formulae behave as they will in the actual document.
#
#   The styles are meant to be mixed: "headings from 2, tables from 3" is the
#   expected kind of answer, which is why each preamble keeps its concerns in
#   clearly separated blocks.
#
# USAGE (run from repo root):
#   python scripts/build_style_samples.py
#   python scripts/build_style_samples.py --only 3
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_reports as B                                    # noqa: E402

SAMPLES = REPO_ROOT / "deliverables" / "styleSamples"
STYLES = REPO_ROOT / "scripts" / "styles"

NAMES = {
    1: ("Класически", "PT Serif навсякъде; малки главни в заглавията; booktabs "
                      "линии; надписи в курсив. Консервативният дисертационен вид."),
    2: ("Технически доклад", "Заглавия без серифи върху серифен текст; тънка линия "
                             "под всеки раздел; таблици с редуващи се редове; "
                             "изнесените бележки в рамка."),
    3: ("Списание", "Компактен: стегнат интерлиниаж, заглавие от трето ниво в реда "
                    "на абзаца, надпис над таблиците и под фигурите."),
    4: ("Модерен академичен", "Просторен: повече бяло, по-леки номера на заглавията, "
                              "таблици без линии, надписи без серифи."),
    5: ("Формален монографичен", "Центрирани начала на раздели с линия отдолу; "
                                 "плътно очертани таблици; изнесените бележки с "
                                 "вертикална черта."),
}


def build(n: int, engine: str, pandoc: str) -> bool:
    style = STYLES / f"style{n}.tex"
    if not style.exists():
        print(f"  ! no {style.name}")
        return False
    out = SAMPLES / f"style{n}_bg.pdf"
    print(f"  Style {n} — {NAMES[n][0]} ...")
    return B.run_pandoc(
        SAMPLES / "sample_bg.md", out, "bg", engine, pandoc,
        geometry="2.2cm", toc=False, number_sections=True,
        extra_args=["--include-in-header", str(style)],
        work_dir=SAMPLES,   # the sample keeps its own copy of the figure
    )


def write_contact_sheet() -> None:
    L = ["# Мостри на оформлението\n",
         "Един и същ документ, пет оформления. Всяко е самостоятелен PDF в тази "
         "папка. Стиловете са замислени да се комбинират - „заглавията от 2, "
         "таблиците от 3“ е очакваният вид отговор.\n",
         "| # | Име | Какво го отличава | Файл |", "|---|---|---|---|"]
    for n, (name, desc) in NAMES.items():
        L.append(f"| {n} | **{name}** | {desc} | `style{n}_bg.pdf` |")
    L += ["\n## Кои елементи се различават\n",
          "| Елемент | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|",
          "| Заглавия | малки главни | без серифи + линия | компактни, трето ниво в реда | леки, просторни | центрирани с линия |",
          "| Надписи | курсив, отдолу | без серифи, отдолу | над таблици, под фигури | без серифи, ляво подравнени | тире, отдолу |",
          "| Таблици | booktabs | редуващи се редове | booktabs, компактни | без линии | плътно очертани |",
          "| Изнесени бележки | вдаден курсив | сива рамка | вдадени, дребен шрифт | вдадени, просторни | вертикална черта |",
          "\nВсичко останало - шрифт за текста, кирилица, формули, код - е еднакво, "
          "за да се сравнява само оформлението.\n"]
    (SAMPLES / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"  wrote {(SAMPLES / 'README.md').relative_to(REPO_ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", type=int, choices=[1, 2, 3, 4, 5])
    a = ap.parse_args()

    engine, pandoc = B.find_engine(), B.find_pandoc()
    ok = True
    for n in ([a.only] if a.only else sorted(NAMES)):
        ok &= build(n, engine, pandoc)
    write_contact_sheet()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
