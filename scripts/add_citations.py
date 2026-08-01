#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/add_citations.py
#
# PURPOSE: Attach source footnotes to the claims llmPipeline/source_scan.py
#   flagged as needing one.
#
#   Chapters 4, 5 and 6 carried no references at all; the audit found 61 of its
#   86 gaps there. Each entry below pairs a flagged section with a work I can
#   state confidently - this is the CFR / poker-AI / deep-RL literature the
#   thesis is built on. Anything I would have been guessing at is NOT here; it
#   stays in SOURCE_GAPS.md for the author, because a wrong citation in a
#   doctoral deliverable is worse than a missing one.
#
#   Anchoring: a citation is attached to the end of a chosen paragraph of a
#   chosen section, by index. EN and BG have identical heading counts (verified)
#   and are translations paragraph for paragraph, so the same (section,
#   paragraph) lands on the same claim in both languages.
#
# USAGE (run from repo root):
#   python scripts/add_citations.py --dry-run
#   python scripts/add_citations.py
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS = REPO_ROOT / "deliverables" / "reports"

# key -> (en body, bg body). Bulgarian keeps the title in the original language
# per terminology_EN_BG.md rule 7; only the surrounding words are translated.
REFS: dict[str, tuple[str, str]] = {
 "johanson2013size": (
   'Johanson, M. (2013). "Measuring the Size of Large No-Limit Poker Games." '
   'Technical report, University of Alberta.',
   'Johanson, M. (2013). "Measuring the Size of Large No-Limit Poker Games." '
   'Технически доклад, University of Alberta.'),
 "gilpin2007": (
   'Gilpin, A. & Sandholm, T. (2007). "Lossless Abstraction of Imperfect Information '
   'Games." *Journal of the ACM*, 54(5) — GameShrink, and the Rhode Island Hold\'em result.',
   'Gilpin, A. & Sandholm, T. (2007). "Lossless Abstraction of Imperfect Information '
   'Games." *Journal of the ACM*, 54(5) - GameShrink и резултатът за Rhode Island холдем.'),
 "ganzfried2013": (
   'Ganzfried, S. & Sandholm, T. (2013). "Action Translation in Extensive-Form Games '
   'with Large Action Spaces: Axioms, Paradoxes, and the Pseudo-Harmonic Mapping." *IJCAI*.',
   'Ganzfried, S. & Sandholm, T. (2013). "Action Translation in Extensive-Form Games '
   'with Large Action Spaces: Axioms, Paradoxes, and the Pseudo-Harmonic Mapping." *IJCAI*.'),
 "johanson2013abs": (
   'Johanson, M., Burch, N., Valenzano, R. & Bowling, M. (2013). "Evaluating State-Space '
   'Abstractions in Extensive-Form Games." *AAMAS*.',
   'Johanson, M., Burch, N., Valenzano, R. & Bowling, M. (2013). "Evaluating State-Space '
   'Abstractions in Extensive-Form Games." *AAMAS*.'),
 "kroer2014": (
   'Kroer, C. & Sandholm, T. (2014). "Extensive-Form Game Abstraction with Bounds." '
   '*ACM EC*; and Kroer, C. & Sandholm, T. (2016). "Imperfect-Recall Abstractions with '
   'Bounds in Games." *ACM EC*.',
   'Kroer, C. & Sandholm, T. (2014). "Extensive-Form Game Abstraction with Bounds." '
   '*ACM EC*; и Kroer, C. & Sandholm, T. (2016). "Imperfect-Recall Abstractions with '
   'Bounds in Games." *ACM EC*.'),
 "burch2014": (
   'Burch, N., Johanson, M. & Bowling, M. (2014). "Solving Imperfect Information Games '
   'Using Decomposition." *AAAI* — re-solving and the augmented subgame.',
   'Burch, N., Johanson, M. & Bowling, M. (2014). "Solving Imperfect Information Games '
   'Using Decomposition." *AAAI* - пререшаване и разширената под-игра.'),
 "libratus": (
   'Brown, N. & Sandholm, T. (2018). "Superhuman AI for heads-up no-limit poker: '
   'Libratus beats top professionals." *Science*, 359(6374), 418–424.',
   'Brown, N. & Sandholm, T. (2018). "Superhuman AI for heads-up no-limit poker: '
   'Libratus beats top professionals." *Science*, 359(6374), 418-424.'),
 "deepstack": (
   'Moravčík, M. et al. (2017). "DeepStack: Expert-level artificial intelligence in '
   'heads-up no-limit poker." *Science*, 356(6337), 508–513.',
   'Moravčík, M. et al. (2017). "DeepStack: Expert-level artificial intelligence in '
   'heads-up no-limit poker." *Science*, 356(6337), 508-513.'),
 "pluribus": (
   'Brown, N. & Sandholm, T. (2019). "Superhuman AI for multiplayer poker." *Science*, '
   '365(6456), 885–890.',
   'Brown, N. & Sandholm, T. (2019). "Superhuman AI for multiplayer poker." *Science*, '
   '365(6456), 885-890.'),
 "rebel": (
   'Brown, N., Bakhtin, A., Lerer, A. & Gong, Q. (2020). "Combining Deep Reinforcement '
   'Learning and Search for Imperfect-Information Games." *NeurIPS*.',
   'Brown, N., Bakhtin, A., Lerer, A. & Gong, Q. (2020). "Combining Deep Reinforcement '
   'Learning and Search for Imperfect-Information Games." *NeurIPS*.'),
 "sog": (
   'Schmid, M. et al. (2023). "Student of Games: A unified learning algorithm for both '
   'perfect and imperfect information games." *Science Advances*, 9(46).',
   'Schmid, M. et al. (2023). "Student of Games: A unified learning algorithm for both '
   'perfect and imperfect information games." *Science Advances*, 9(46).'),
 "deepcfr": (
   'Brown, N., Lerer, A., Gross, S. & Sandholm, T. (2019). "Deep Counterfactual Regret '
   'Minimization." *ICML*.',
   'Brown, N., Lerer, A., Gross, S. & Sandholm, T. (2019). "Deep Counterfactual Regret '
   'Minimization." *ICML*.'),
 "nfsp": (
   'Heinrich, J. & Silver, D. (2016). "Deep Reinforcement Learning from Self-Play in '
   'Imperfect-Information Games." *arXiv:1603.01121*.',
   'Heinrich, J. & Silver, D. (2016). "Deep Reinforcement Learning from Self-Play in '
   'Imperfect-Information Games." *arXiv:1603.01121*.'),
 "dream": (
   'Steinberger, E., Lerer, A. & Brown, N. (2020). "DREAM: Deep Regret Minimization with '
   'Advantage Baselines and Model-free Learning." *arXiv:2006.10410*.',
   'Steinberger, E., Lerer, A. & Brown, N. (2020). "DREAM: Deep Regret Minimization with '
   'Advantage Baselines and Model-free Learning." *arXiv:2006.10410*.'),
 "openspiel": (
   'Lanctot, M. et al. (2019). "OpenSpiel: A Framework for Reinforcement Learning in '
   'Games." *arXiv:1908.09453*.',
   'Lanctot, M. et al. (2019). "OpenSpiel: A Framework for Reinforcement Learning in '
   'Games." *arXiv:1908.09453*.'),
 "resnet": (
   'He, K., Zhang, X., Ren, S. & Sun, J. (2016). "Deep Residual Learning for Image '
   'Recognition." *CVPR*.',
   'He, K., Zhang, X., Ren, S. & Sun, J. (2016). "Deep Residual Learning for Image '
   'Recognition." *CVPR*.'),
 "alphastar": (
   'Vinyals, O. et al. (2019). "Grandmaster level in StarCraft II using multi-agent '
   'reinforcement learning." *Nature*, 575, 350–354.',
   'Vinyals, O. et al. (2019). "Grandmaster level in StarCraft II using multi-agent '
   'reinforcement learning." *Nature*, 575, 350-354.'),
 "lbr": (
   'Lisý, V. & Bowling, M. (2017). "Equilibrium Approximation Quality of Current '
   'No-Limit Poker Bots." *AAAI Workshop on Computer Poker* — local best response (LBR).',
   'Lisý, V. & Bowling, M. (2017). "Equilibrium Approximation Quality of Current '
   'No-Limit Poker Bots." *AAAI Workshop on Computer Poker* - локален най-добър отговор (LBR).'),
 "brown2017": (
   'Brown, N. & Sandholm, T. (2017). "Safe and Nested Subgame Solving for '
   'Imperfect-Information Games." *NeurIPS*.',
   'Brown, N. & Sandholm, T. (2017). "Safe and Nested Subgame Solving for '
   'Imperfect-Information Games." *NeurIPS*.'),
 "psro_ref": (
   'Lanctot, M. et al. (2017). "A Unified Game-Theoretic Approach to Multiagent '
   'Reinforcement Learning." *NeurIPS* (PSRO).',
   'Lanctot, M. et al. (2017). "A Unified Game-Theoretic Approach to Multiagent '
   'Reinforcement Learning." *NeurIPS* (PSRO).'),
}

# (step, section heading as reported by the audit, citation key)
# The audit recorded the exact sentence it flagged; the script finds THAT
# sentence's paragraph in the Bulgarian and puts the marker at the same
# (section, paragraph) in the English. Anchoring on the claim rather than on a
# hand-counted index is what keeps a citation attached to the thing it cites.
PLACEMENTS: list[tuple[str, str, str]] = [
 # -- chapter 4: abstraction -------------------------------------------------
 ("step04", "Защо е необходима абстракцията", "johanson2013size"),
 ("step04", "Абстракция на действията и проблемът с транслацията {.unlisted}", "ganzfried2013"),
 ("step04", "Ниво 1 — Беззагубен", "gilpin2007"),
 ("step04", "Ниво 3 — Емпирична сходност", "johanson2013abs"),
 ("step04", "Инструмент 1 — Аналитична граница", "kroer2014"),
 ("step04", "Инструмент 2 — прокси на разстоянието на Васерщайн", "johanson2013abs"),
 ("step04", "Избор на абстракция на практика", "kroer2014"),
 ("step04", "Конвейер 1 — GameShrink (беззагубен)", "gilpin2007"),
 ("step04", "Корекция по време на изпълнение", "libratus"),
 ("step04", "Защо решаването на под-игра не може да се извършва изолирано (хвърляне на монета)", "burch2014"),
 ("step04", "Коригиране 1 — Безопасно решаване на под-игри", "brown2017"),
 ("step04", "Пач 2 — Вложено решаване на под-игри (убиецът на превода на действия)", "brown2017"),
 ("step04", "Архитектура: План и актуализации по време на работа", "libratus"),
 ("step04", "Практическо валидиране", "brown2017"),
 # -- chapter 5: neural methods ----------------------------------------------
 ("step05", "Кодиране на състоянието на играта и историята", "openspiel"),
 ("step05", "Оразмеряване и капацитет", "resnet"),
 ("step05", "Стабилност на обучението и диагностиката", "deepcfr"),
 ("step05", "От табличен CFR към апроксимация на функция", "deepcfr"),
 ("step05", "Deep CFR и неговите варианти с една мрежа", "dream"),
 ("step05", "NFSP - Neural Fictitious Self-Play", "nfsp"),
 ("step05", "Компромиси: Кога невронната CFR е от полза", "deepcfr"),
 ("step05", "Популационни методи: PSRO, NFSP, XFP", "psro_ref"),
 ("step05", "Типове слоеве на практика: многослоен перцептрон, CNN, RNN, внимание/трансформъри", "alphastar"),
 # -- chapter 6: the five systems --------------------------------------------
 ("step06", "Въведение", "deepstack"),
 ("step06", "Затворената празнина", "lbr"),
 ("step06", "Архитектура", "deepstack"),
 ("step06", "Ключова иновация: продължително пре-решаване с научени контрафактични стойности", "burch2014"),
 ("step06", "Наследство и съвременна значимост", "brown2017"),
 ("step06", "The gap it closed", "libratus"),
 ("step06", "Ключова иновация: вложено безопасно решаване на под-игри", "brown2017"),
 ("step06", "Силни страни и ограничения", "libratus"),
 ("step06", "Изчислителна мощност и достъпност", "pluribus"),
 ("step06", "Ключова иновация: общодостъпни състояния на убеждението и научени стойности", "rebel"),
 ("step06", "Ключова иновация: Growing-Tree CFR и правилно самообучение", "sog"),
]

FILES = {"en": ("summary/summaryEn.md", 0), "bg": ("summary/summaryBg.md", 1)}
HEADING = re.compile(r"^#{1,6}\s+\S")
GAPS = REPO_ROOT / "llmPipeline" / "out" / "source_gaps.json"


def paragraph_ends(lines: list[str]) -> list[tuple[int, int, int]]:
    """-> [(section index, paragraph index in section, last line of paragraph)]."""
    out: list[tuple[int, int, int]] = []
    sec = -1
    para = 0
    cur = None
    for i, l in enumerate(lines):
        if HEADING.match(l):
            if cur is not None:
                out.append((sec, para, cur)); cur = None
            sec += 1
            para = 0
            continue
        s = l.strip()
        skip = (not s or s.startswith((">", "|", "!", "---", ": ", "$$", "```", "<"))
                or re.match(r"^[-*+]\s|^\d+\.\s", s))
        if skip:
            if cur is not None:
                out.append((sec, para, cur)); para += 1; cur = None
        else:
            cur = i
    if cur is not None:
        out.append((sec, para, cur))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    import json
    gaps = {(g["step"], g["heading"]): g.get("claim") or ""
            for g in json.loads(GAPS.read_text(encoding="utf-8"))
            if g["verdict"] == "needs-source"}

    added, problems = 0, []
    for step in sorted({p[0] for p in PLACEMENTS}):
        wanted = [x for x in PLACEMENTS if x[0] == step]

        # 1. locate each claim in the BULGARIAN, which is what the audit read
        bg_path = REPORTS / step / FILES["bg"][0]
        bg_lines = bg_path.read_text(encoding="utf-8").splitlines()
        bg_index = paragraph_ends(bg_lines)
        targets: list[tuple[int, int, str]] = []      # (sec, para, key)
        for _s, heading, key in wanted:
            claim = gaps.get((step, heading), "")
            probe = " ".join(claim.split()[:8])
            if not probe:
                problems.append(f"{step}: no recorded claim for {heading!r}")
                continue
            hit = next(((sec, para) for sec, para, ln in bg_index
                        if probe in " ".join(bg_lines[ln].split())), None)
            if hit is None:
                problems.append(f"{step}: could not locate the claim for [^{key}] "
                                f"({heading[:40]!r})")
                continue
            targets.append((hit[0], hit[1], key))

        # 2. apply the same (section, paragraph) in both languages
        for lang, (rel, idx) in FILES.items():
            p = REPORTS / step / rel
            lines = p.read_text(encoding="utf-8").splitlines()
            index = {(sec, para): ln for sec, para, ln in paragraph_ends(lines)}
            used: set[str] = set()
            for sec, para, key in sorted(targets, key=lambda x: (-x[0], -x[1])):
                ln = index.get((sec, para))
                if ln is None:
                    problems.append(f"{step} {lang}: no paragraph {para} in section {sec}")
                    continue
                if f"[^{key}]" in lines[ln]:
                    continue
                lines[ln] = lines[ln].rstrip() + f"[^{key}]"
                used.add(key)
                if lang == "bg":
                    added += 1
            text = chr(10).join(lines)
            defined = set(re.findall(r"^\[\^([\w-]+)\]:", text, re.M))
            for key in sorted(used - defined):
                if key not in REFS:
                    problems.append(f"{step} {lang}: [^{key}] has no body")
                    continue
                text = (text.rstrip(chr(10)) + chr(10)*2 +
                        f"[^{key}]: {REFS[key][idx]}" + chr(10))
            if not a.dry_run:
                p.write_text(text, encoding="utf-8")

    print(f"{added} citation(s) placed in each language"
          f"{' (dry run)' if a.dry_run else ''}")
    for x in problems:
        print(f"  ! {x}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
