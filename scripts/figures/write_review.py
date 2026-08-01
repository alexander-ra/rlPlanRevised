#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/figures/write_review.py
#
# PURPOSE: Turn the translated label set into a table a human can check.
#   Figure labels are short and there are hundreds of them, so reading them as
#   a list is far faster than opening 91 images.
#
# USAGE (run from repo root):
#   python scripts/figures/write_review.py
# ---------------------------------------------------------------------------

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
LABELS = REPO_ROOT / "scripts" / "figures" / "out" / "figure_labels.json"
OUT = REPO_ROOT / "deliverables" / "reports" / "FIGURE_LABELS_BG.md"

SOURCE_NOTE = {
    "glossary": "речник",
    "model": "модел",
    "model-single": "модел",
    "identity": "без превод",
}


def step_of(occ: list[dict]) -> str:
    for o in occ:
        for part in o["file"].split("/"):
            if part.startswith("step"):
                return part
    return "общи"


def cell(s: str) -> str:
    """Make a string safe inside a markdown table cell."""
    return s.replace("|", "\\|").replace("\n", " ⏎ ").strip()


def main() -> None:
    entries = json.loads(LABELS.read_text(encoding="utf-8"))
    by_step: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_step[step_of(e["occurrences"])].append(e)

    done = [e for e in entries if e.get("bg")]
    todo = [e for e in entries if not e.get("bg")]

    L: list[str] = []
    w = L.append
    w("# Надписи на фигурите - за преглед\n")
    n_scripts = len({o["file"] for e in entries for o in e["occurrences"]})
    w(f"{len(entries)} различни надписа от {n_scripts} скрипта за чертане.\n")
    w(f"- преведени: **{len(done)}**")
    w(f"  - от речника: {sum(1 for e in done if e['source'] == 'glossary')}")
    w(f"  - от модела: {sum(1 for e in done if str(e['source']).startswith('model'))}")
    w(f"  - оставени както са (само идентификатори): "
      f"{sum(1 for e in done if e['source'] == 'identity')}")
    w(f"- **остават на английски: {len(todo)}** (виж последния раздел)\n")
    w("Имената на алгоритми и системи (CFR, DQN, PPO, MCCFR, Shapley, "
      "OpenSpiel) остават на латиница по конвенцията в `terminology_EN_BG.md`. "
      "`Kuhn` и `Leduc` се транслитерират като `Кун` и `Ледюк`, както в текста.\n")
    w("Символът ⏎ отбелязва нов ред в надписа - броят редове е запазен, "
      "защото определя оформлението в кутиите на диаграмите.\n")

    for step in sorted(by_step):
        items = sorted(by_step[step], key=lambda e: e["en"].lower())
        w(f"\n## {step}  ({len(items)})\n")
        w("| Английски | Български | Източник |")
        w("|---|---|---|")
        for e in items:
            bg = cell(e["bg"]) if e.get("bg") else "**— непреведен —**"
            src = SOURCE_NOTE.get(e.get("source"), "—")
            w(f"| {cell(e['en'])} | {bg} | {src} |")

    if todo:
        w("\n\n## Останали на английски\n")
        w("Тези надписи не преминаха проверката - моделът променяше числа или "
          "броя редове. Оставени са на английски, защото сгрешен надпис върху "
          "графика е по-лош от английски надпис.\n")
        w("| Надпис | Причина |")
        w("|---|---|")
        for e in sorted(todo, key=lambda e: e["en"].lower()):
            w(f"| {cell(e['en'][:110])} | {cell(e.get('reject', ''))} |")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")
    print(f"  {len(done)} translated, {len(todo)} left in English")


if __name__ == "__main__":
    main()
