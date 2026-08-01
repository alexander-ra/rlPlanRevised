#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/merge_shared_references.py
#
# PURPOSE: Give every work exactly one footnote, corpus-wide.
#
#   Seven works are cited from two to four chapters. Because each chapter used
#   to compile on its own, each wrote its own version of the note - the same key
#   with a different body, usually differing only in which chapter or section of
#   the source it points at. Once the bundle is a single LaTeX document those
#   collide: pandoc keeps one body and drops the rest, silently losing the
#   pointers.
#
#   So each of them gets one canonical note that keeps EVERY chapter's pointer,
#   and one key. Where a note also carried a second, related work, that work is
#   kept in the merged note rather than dropped.
#
#   This edits the chapter sources, which means a standalone chapter PDF now
#   shows the full merged note rather than just its own pointer. That is the
#   agreed trade: the bundle is the deliverable, the split is internal.
#
# USAGE (run from repo root):
#   python scripts/merge_shared_references.py --dry-run
#   python scripts/merge_shared_references.py
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS = REPO_ROOT / "deliverables" / "reports"

# key -> {"aliases": [other keys folded into it], "en": body, "bg": body}
CANONICAL: dict[str, dict] = {
    "shoham2008": {
        "aliases": [],
        "en": ('Shoham, Y. & Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, '
               'Game-Theoretic, and Logical Foundations*. Ch. 3–4 (normal- and '
               'extensive-form games); Ch. 5 (extensive-form games); §3.4 (computing '
               'equilibria) and §4.6 (computing best responses), the sequence-form '
               'machinery underneath every LP in Chapter 8; Ch. 7 "Learning and '
               'Teaching", the learning-in-repeated-games framing, including the tension '
               'that your actions both *exploit* and *teach* the opponent. '
               'Free: <http://www.masfoundations.org/download.html>'),
        "bg": ('Shoham, Y. & Leyton-Brown, K. (2008). *Multiagent Systems: Algorithmic, '
               'Game-Theoretic, and Logical Foundations*. Гл. 3–4 (игри в нормална и '
               'разгърната форма); гл. 5 (игри в разгърната форма); §3.4 (изчисляване на '
               'равновесия) и §4.6 (изчисляване на най-добри отговори) - механизмът в '
               'последователна форма под всяка линейна програма в Глава 8; гл. 7 "Learning '
               'and Teaching" - рамката за учене в повтарящи се игри, включително '
               'напрежението, че действията едновременно *експлоатират* и *обучават* '
               'опонента. Свободно достъпна: <http://www.masfoundations.org/download.html>'),
    },
    "suttonbarto2018": {
        "aliases": ["sutton2018"],
        "en": ('Sutton, R.S. & Barto, A.G. (2018). *Reinforcement Learning: An '
               'Introduction*, 2nd edition. MIT Press. Ch. 1 (the field); Ch. 3 (finite '
               'Markov decision processes); Ch. 4 (dynamic programming); Ch. 5 (Monte '
               'Carlo methods); Ch. 6 (temporal-difference learning). '
               '<http://incompleteideas.net/book/the-book-2nd.html>'),
        "bg": ('Sutton, R.S. & Barto, A.G. (2018). *Reinforcement Learning: An '
               'Introduction*, второ издание. MIT Press. Гл. 1 (областта); гл. 3 (крайни '
               'марковски процеси на вземане на решения); гл. 4 (динамично програмиране); '
               'гл. 5 (методи на Монте Карло); гл. 6 (обучение с темпорална разлика). '
               '<http://incompleteideas.net/book/the-book-2nd.html>'),
    },
    "bowling2015": {
        "aliases": [],
        "en": ('Bowling, M., Burch, N., Johanson, M. & Tammelin, O. (2015). "Heads-up '
               'limit hold\'em poker is solved." *Science*, 347(6218), 145–149. Used CFR+ '
               'to solve heads-up limit Texas Hold\'em — the first non-trivial '
               'imperfect-information game to be essentially solved.'),
        "bg": ('Bowling, M., Burch, N., Johanson, M. & Tammelin, O. (2015). "Heads-up '
               'limit hold\'em poker is solved." *Science*, 347(6218), 145–149. Използва '
               'CFR+ за решаването на хедс-ъп лимит тексаски холдем - първата нетривиална '
               'игра с непълна информация, която по същество е решена.'),
    },
    "southey2005": {
        "aliases": [],
        "en": ('Southey, F. et al. (2005). "Bayes\' Bluff: Opponent Modelling in Poker." '
               '*UAI*.'),
        "bg": ('Southey, F. et al. (2005). "Bayes\' Bluff: Opponent Modelling in Poker." '
               '*UAI*.'),
    },
    "ganzfried2015": {
        "aliases": [],
        # Two venue strings for one paper; the journal version is the citable one.
        "en": ('Ganzfried, S. & Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM '
               'Transactions on Economics and Computation* — the paper that first made '
               '"exploit but never lose to the baseline" a theorem; the safety half of the '
               'dial and the anchor for Chapter 8.'),
        "bg": ('Ganzfried, S. & Sandholm, T. (2015). "Safe Opponent Exploitation." *ACM '
               'Transactions on Economics and Computation* - статията, която за първи път '
               'формулира като теорема принципа „експлоатирай, но никога не губи спрямо '
               'базовата линия“; безопасната половина от скалата и основата за Глава 8.'),
    },
    "lanctot2017": {
        "aliases": [],
        "en": ('Lanctot, M. et al. (2017). "A Unified Game-Theoretic Approach to '
               'Multiagent Reinforcement Learning." *NeurIPS* (PSRO). Related: McMahan, '
               'H. B., Gordon, G. & Blum, A. (2003). "Planning in the Presence of Cost '
               'Functions Controlled by an Adversary." *ICML* (the double-oracle method '
               'PSRO generalizes); Tuyls, K. et al. (2020). "Bounds and dynamics for '
               'empirical game-theoretic analysis." *AAMAS/JAAMAS* (EGTA).'),
        "bg": ('Lanctot, M. et al. (2017). "A Unified Game-Theoretic Approach to '
               'Multiagent Reinforcement Learning." *NeurIPS* (PSRO). Свързани: McMahan, '
               'H. B., Gordon, G. & Blum, A. (2003). "Planning in the Presence of Cost '
               'Functions Controlled by an Adversary." *ICML* (методът на двойния '
               'предсказвач, който PSRO обобщава); Tuyls, K. et al. (2020). "Bounds and '
               'dynamics for empirical game-theoretic analysis." *AAMAS/JAAMAS* (EGTA).'),
    },
    "balduzzi2019": {
        "aliases": [],
        "en": ('Balduzzi, D. et al. (2019). "Open-ended Learning in Symmetric Zero-sum '
               'Games." *ICML* — the spinning-top geometry of transitive vs cyclic '
               'structure. Related: Jaderberg, M. et al. (2017). "Population Based '
               'Training of Neural Networks." *arXiv:1711.09846*.'),
        "bg": ('Balduzzi, D. et al. (2019). "Open-ended Learning in Symmetric Zero-sum '
               'Games." *ICML* - геометрията на пумпала на транзитивната спрямо цикличната '
               'структура. Свързани: Jaderberg, M. et al. (2017). "Population Based '
               'Training of Neural Networks." *arXiv:1711.09846*.'),
    },
}

FILES = {"en": "summary/summaryEn.md", "bg": "summary/summaryBg.md"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    alias_to_key = {al: k for k, v in CANONICAL.items() for al in v["aliases"]}
    bodies = 0
    renamed = 0

    for i in range(1, 13):
        step = f"step{i:02d}"
        for lang, rel in FILES.items():
            p = REPORTS / step / rel
            if not p.exists():
                continue
            t = orig = p.read_text(encoding="utf-8")

            # fold aliases onto the canonical key, uses and definition alike
            for alias, key in alias_to_key.items():
                if f"[^{alias}]" in t:
                    t = t.replace(f"[^{alias}]", f"[^{key}]")
                    renamed += 1

            # rewrite each canonical definition to the merged body
            for key, spec in CANONICAL.items():
                pat = re.compile(rf"^\[\^{re.escape(key)}\]:\s*.+$", re.M)
                if pat.search(t):
                    t = pat.sub(f"[^{key}]: {spec[lang]}", t)
                    bodies += 1

            # a chapter may now define the same key twice (its own + a folded
            # alias); keep the first definition only
            seen: set[str] = set()
            out = []
            for line in t.splitlines():
                m = re.match(r"^\[\^([\w-]+)\]:", line)
                if m:
                    if m.group(1) in seen:
                        continue
                    seen.add(m.group(1))
                out.append(line)
            t = "\n".join(out) + "\n"
            t = re.sub(r"\n{3,}", "\n\n", t)

            if t != orig:
                print(f"  {p.relative_to(REPO_ROOT)}")
                if not a.dry_run:
                    p.write_text(t, encoding="utf-8")

    print(f"\n{bodies} definition(s) canonicalised, {renamed} alias key(s) folded"
          f"{' (dry run)' if a.dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
