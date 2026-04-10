#!/usr/bin/env python3
"""
scripts/add_glossary_markers.py

One-time utility: adds HTML glossary superscript markers to raw step files.
Adds <sup class="gl" data-gl="TERM_ID">gl</sup> after the FIRST occurrence
of each glossary term per file, skipping code blocks and inline code spans.

Usage (run from repo root):
    python3 scripts/add_glossary_markers.py [--dry-run]
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
RAW_STEPS_EN = REPO_ROOT / "planning" / "rawSteps"
RAW_STEPS_BG = REPO_ROOT / "planning" / "rawStepsBg"

STEP_FILES = [
    "step_01_rl_basics.md",
    "step_02_game_theory_cfr.md",
    "step_03_cfr_variants_mc.md",
    "step_04_game_abstraction_scaling.md",
    "step_05_neural_equilibrium.md",
    "step_06_end_to_end_game_ai.md",
    "step_07_opponent_modeling.md",
    "step_08_safe_exploitation.md",
    "step_09_multi_agent_rl.md",
    "step_10_population_training_evo_gt.md",
    "step_11_coalition_formation_ffa.md",
    "step_12_sequence_models_llm_agents.md",
    "step_13_behavioral_analysis.md",
    "step_14_evaluation_frameworks.md",
    "step_15_research_frontier_mapping.md",
]

# ─────────────────────────────────────────────────────────────────────────────
# Glossary term mapping: term_id → (en_phrases, bg_phrases)
# Phrases are matched case-sensitively with word boundary awareness.
# List more specific phrases BEFORE shorter/more common ones.
# ─────────────────────────────────────────────────────────────────────────────
TERM_MAP = {
    # ── Reinforcement Learning ──────────────────────────────────────────────
    "reinforcement_learning": (
        ["reinforcement learning", "Reinforcement Learning", "Reinforcement learning"],
        ["обучение с подкрепление", "Обучение с подкрепление"],
    ),
    "value_function": (
        ["value function", "Value function", "Q-function", "V-function",
         "state-value function", "action-value function"],
        ["функция на стойността", "Функция на стойността",
         "Q-функция", "V-функция"],
    ),
    "experience_replay": (
        ["experience replay", "Experience replay", "replay buffer"],
        ["повторение на натрупан опит", "Повторение на натрупан опит"],
    ),
    "mdp": (
        ["Markov decision process", "Markov Decision Process"],
        ["Марковски процес на вземане на решения",
         "марковски процес на вземане на решения"],
    ),
    "policy_gradient": (
        ["policy gradient method", "policy gradient algorithm",
         "policy gradient", "Policy gradient", "Policy Gradient"],
        ["градиент на стратегията", "Градиент на стратегията"],
    ),
    "advantage_function": (
        ["advantage function", "Advantage function"],
        ["функция на предимството", "Функция на предимството"],
    ),
    "gae": (
        ["Generalized Advantage Estimation"],
        ["обобщена оценка на предимството", "Обобщена оценка на предимството"],
    ),
    "marl": (
        ["multi-agent reinforcement learning",
         "Multi-Agent Reinforcement Learning",
         "Multi-agent Reinforcement Learning"],
        ["многоагентно обучение с подкрепление",
         "Многоагентно обучение с подкрепление"],
    ),
    "population_based_training": (
        ["population-based training", "Population-based training",
         "population based training"],
        ["обучение на базата на популации",
         "Обучение на базата на популации"],
    ),
    # ── Game Theory ─────────────────────────────────────────────────────────
    "game_theory": (
        ["game theory", "Game theory", "Game Theory", "game-theoretic"],
        ["теория на игрите", "Теория на игрите"],
    ),
    "extensive_form_game": (
        ["extensive-form game", "Extensive-form game",
         "extensive-form games", "extensive form game"],
        ["игра в разгърната форма", "Игра в разгърната форма",
         "игри в разгърната форма"],
    ),
    "normal_form_game": (
        ["normal-form game", "Normal-form game",
         "normal form game"],
        ["игра в нормална форма", "Игра в нормална форма"],
    ),
    "imperfect_information": (
        ["imperfect-information game", "imperfect information game",
         "imperfect information", "Imperfect information",
         "imperfect-information"],
        ["несъвършена информация", "Несъвършена информация"],
    ),
    "incomplete_information": (
        ["incomplete information", "Incomplete information"],
        ["непълна информация", "Непълна информация"],
    ),
    "information_set": (
        ["information set", "Information set", "information sets"],
        ["информационно множество", "Информационно множество",
         "информационни множества"],
    ),
    "nash_equilibrium": (
        ["Nash equilibrium", "Nash Equilibrium",
         "Nash equilibria", "Nash eq."],
        ["равновесие на Наш", "Равновесие на Наш",
         "равновесия на Наш"],
    ),
    "exploitability": (
        ["exploitability", "Exploitability"],
        ["експлоатируемост", "Експлоатируемост"],
    ),
    "safe_exploitation": (
        ["safe exploitation", "Safe exploitation"],
        ["безопасна експлоатация", "Безопасна експлоатация"],
    ),
    "zero_sum_game": (
        ["zero-sum game", "Zero-sum game", "zero-sum games",
         "zero sum game", "zero-sum"],
        ["игра с нулева сума", "Игра с нулева сума",
         "игри с нулева сума"],
    ),
    "mixed_strategy": (
        ["mixed strategy", "Mixed strategy", "mixed strategies"],
        ["смесена стратегия", "Смесена стратегия",
         "смесени стратегии"],
    ),
    "counterfactual_value": (
        ["counterfactual value", "Counterfactual value",
         "counterfactual regret", "Counterfactual Regret"],
        ["контрафактуална стойност", "Контрафактуална стойност",
         "контрафактуално съжаление"],
    ),
    "regret": (
        ["cumulative regret", "Cumulative regret",
         "regret minimization", "Regret minimization"],
        ["кумулативно съжаление", "Кумулативно съжаление",
         "минимизиране на съжалението"],
    ),
    "coalition": (
        ["coalition formation", "Coalition formation",
         "coalition", "Coalition"],
        ["формиране на коалиции", "Формиране на коалиции",
         "коалиция", "Коалиция"],
    ),
    "opponent_modeling": (
        ["opponent modeling", "Opponent modeling",
         "opponent model", "opponent models"],
        ["моделиране на противника", "Моделиране на противника"],
    ),
    "game_tree": (
        ["game tree", "Game tree", "game trees"],
        ["дърво на играта", "Дърво на играта"],
    ),
    "subgame_solving": (
        ["subgame solving", "Subgame solving", "subgame resolution"],
        ["решаване на подигри", "Решаване на подигри"],
    ),
    "behavioral_cloning": (
        ["behavioral cloning", "Behavioral cloning",
         "behaviour cloning"],
        ["поведенческо клониране", "Поведенческо клониране"],
    ),
    "non_stationarity": (
        ["non-stationarity", "Non-stationarity",
         "non-stationary environment", "non-stationary"],
        ["нестационарност", "Нестационарност"],
    ),
    "shapley_value": (
        ["Shapley value", "Shapley values", "Shapley Q-value"],
        ["стойност на Шапли", "Стойност на Шапли"],
    ),
    "action_abstraction": (
        ["action abstraction", "Action abstraction"],
        ["абстракция на действията", "Абстракция на действията"],
    ),
    "behavioral_trace": (
        ["behavioral trace", "Behavioral trace", "behavioral traces"],
        ["поведенчески проследявания", "Поведенчески проследявания"],
    ),
    "spinning_top": (
        ["spinning top decomposition", "Spinning top decomposition",
         "spinning-top"],
        ['декомпозиция "пумпал"'],
    ),
    # ── Algorithms ──────────────────────────────────────────────────────────
    "cfr": (
        ["Counterfactual Regret Minimization"],
        ["минимизиране на контрафактуалното съжаление",
         "Минимизиране на контрафактуалното съжаление"],
    ),
    "mccfr": (
        ["Monte Carlo CFR", "Monte Carlo Counterfactual"],
        ["Монте Карло вариант на CFR",
         "монте карло вариант на CFR"],
    ),
    "dqn": (
        ["Deep Q-Network", "deep Q-network"],
        ["Дълбока Q-мрежа", "дълбока Q-мрежа"],
    ),
    "ppo": (
        ["Proximal Policy Optimization"],
        ["оптимизация на стратегията с ограничение на близостта",
         "Оптимизация на стратегията с ограничение на близостта"],
    ),
    "deep_cfr": (
        # "Deep CFR" abbreviation — handled separately below as algorithm name
        [],
        [],
    ),
    "rebel": (
        ["Recursive Belief-based Learning"],
        [],
    ),
    "psro": (
        ["Policy Space Response Oracles"],
        ["оракули за отговор в пространството на стратегиите",
         "Оракули за отговор в пространството на стратегиите"],
    ),
    "maddpg": (
        ["Multi-Agent Deep Deterministic Policy Gradient"],
        ["многоагентен дълбок детерминистичен градиент на стратегията",
         "Многоагентен дълбок детерминистичен градиент на стратегията"],
    ),
    "egta": (
        ["Empirical Game-Theoretic Analysis"],
        ["емпиричен теоретико-игрови анализ",
         "Емпиричен теоретико-игрови анализ"],
    ),
    "lola": (
        ["Learning with Opponent-Learning Awareness"],
        [],
    ),
    "alpha_rank": (
        ["Alpha-Rank", "α-Rank"],
        [],
    ),
    # ── Evaluation ──────────────────────────────────────────────────────────
    "evaluation_framework": (
        ["evaluation framework", "Evaluation framework",
         "evaluation frameworks"],
        ["рамка за оценяване", "Рамка за оценяване",
         "рамки за оценяване"],
    ),
    "convergence": (
        ["convergence rate", "convergence guarantee",
         "convergence", "Convergence"],
        ["скорост на сходимост", "Скорост на сходимост",
         "сходимост", "Сходимост"],
    ),
    "hyperparameter": (
        ["hyperparameter", "Hyperparameter", "hyperparameters"],
        ["хиперпараметър", "Хиперпараметър", "хиперпараметри"],
    ),
    "robustness": (
        ["robustness", "Robustness"],
        ["устойчивост", "Устойчивост"],
    ),
    "adaptability": (
        ["adaptability", "Adaptability"],
        ["адаптивност", "Адаптивност"],
    ),
    "benchmark": (
        ["benchmark game", "benchmark environment",
         "benchmark", "Benchmark"],
        ["еталонен тест", "Еталонен тест",
         "еталонни тестове", "еталонна игра"],
    ),
}

MARKER_TPL = '<sup class="gl" data-gl="{tid}">gl</sup>'
ALREADY_MARKED_RE = re.compile(r'<sup class="gl"[^>]*>gl</sup>')


def make_phrase_pattern(phrase: str) -> re.Pattern:
    """Compile a case-sensitive, word-boundary-aware pattern for the phrase."""
    esc = re.escape(phrase)
    # Use Unicode word boundaries (\b works for ASCII; for Cyrillic we use
    # look-ahead / look-behind to avoid partial matches inside longer words.
    left  = r'(?<![А-Яа-яЁёA-Za-z0-9_\-])'
    right = r'(?![А-Яа-яЁёA-Za-z0-9_\-])'
    return re.compile(left + esc + right)


def split_code_blocks(text: str):
    """
    Yield (is_code, chunk) for alternating code/prose regions.
    Handles fenced code blocks (``` or ~~~) and indented code.
    """
    fence_re = re.compile(r'^(`{3,}|~{3,})', re.MULTILINE)
    pos = 0
    in_fence = False
    fence_char = None

    for m in fence_re.finditer(text):
        start = m.start()
        char = m.group(1)[0]

        if not in_fence:
            # prose before the opening fence
            if start > pos:
                yield (False, text[pos:start])
            in_fence = True
            fence_char = char
            pos = start
        else:
            # closing fence must match opening
            if m.group(1)[0] == fence_char:
                end = m.end()
                # include the newline after the closing fence if present
                if end < len(text) and text[end] == '\n':
                    end += 1
                yield (True, text[pos:end])
                in_fence = False
                fence_char = None
                pos = end

    # remainder
    if pos < len(text):
        yield (in_fence, text[pos:])


def strip_inline_code(line: str):
    """
    Return a version of line where backtick spans are replaced with a
    placeholder, and a list of (start, end) spans that are code.
    """
    code_spans = []
    result = list(line)
    i = 0
    while i < len(line):
        if line[i] == '`':
            j = i + 1
            while j < len(line) and line[j] != '`':
                j += 1
            code_spans.append((i, j + 1))
            for k in range(i, min(j + 1, len(line))):
                result[k] = '\x00'  # placeholder
            i = j + 1
        else:
            i += 1
    return ''.join(result), code_spans


def apply_markers_to_prose(prose: str, lang: str, seen: set) -> str:
    """
    Apply glossary markers to a prose chunk.
    Only modifies each term once (tracks in `seen`).
    Skips inline code spans and markdown URLs.
    """
    lines = prose.split('\n')
    result = []

    # Sort terms: longer phrases first to avoid partial-match shadowing
    ordered_terms = sorted(
        TERM_MAP.items(),
        key=lambda kv: max((len(p) for p in kv[1][0 if lang == 'en' else 1]), default=0),
        reverse=True,
    )

    for line in lines:
        # Skip headings that are anchor-only (TOC links) or YAML-like metadata
        stripped = line.lstrip()
        if stripped.startswith('- [') and '](' in stripped:
            # TOC link — don't mark
            result.append(line)
            continue

        masked, _code_spans = strip_inline_code(line)

        for term_id, (en_phrases, bg_phrases) in ordered_terms:
            if term_id in seen:
                continue
            phrases = en_phrases if lang == 'en' else bg_phrases
            if not phrases:
                continue

            for phrase in phrases:
                pat = make_phrase_pattern(phrase)
                # Search in masked line (code spans are zeroed out)
                m = pat.search(masked)
                if not m:
                    continue
                # Ensure the matched region is not in a code span
                start, end = m.start(), m.end()
                if '\x00' in masked[start:end]:
                    continue
                # Also skip if the match is inside a markdown link URL:
                # [...](URL) — check if preceded by '](' without intervening ')'
                pre = masked[:start]
                if re.search(r'\]\([^)]*$', pre):
                    continue

                marker = MARKER_TPL.format(tid=term_id)
                # Replace in REAL line (not masked)
                line = line[:end] + marker + line[end:]
                # Shift masked too to keep offsets valid if we loop again
                masked = masked[:end] + marker + masked[end:]
                seen.add(term_id)
                break  # next term

        result.append(line)

    return '\n'.join(result)


def process_file(path: Path, lang: str, dry_run: bool) -> int:
    """Process one file. Returns number of markers added."""
    text = path.read_text(encoding='utf-8')

    # Skip if already processed (has existing markers)
    existing = len(ALREADY_MARKED_RE.findall(text))

    seen: set = set()
    output_parts = []
    markers_added = 0

    for is_code, chunk in split_code_blocks(text):
        if is_code:
            output_parts.append(chunk)
        else:
            new_chunk = apply_markers_to_prose(chunk, lang, seen)
            markers_added += new_chunk.count('class="gl"') - chunk.count('class="gl"')
            output_parts.append(new_chunk)

    result = ''.join(output_parts)

    if dry_run:
        print(f"  [DRY-RUN] {path.name}: would add {markers_added} markers "
              f"(already had {existing})")
    else:
        path.write_text(result, encoding='utf-8')
        print(f"  {path.name}: added {markers_added} markers "
              f"(total now: {existing + markers_added})")

    return markers_added


def main():
    dry_run = '--dry-run' in sys.argv

    total = 0
    for lang, steps_dir in [('en', RAW_STEPS_EN), ('bg', RAW_STEPS_BG)]:
        print(f"\n=== {lang.upper()} steps: {steps_dir} ===")
        for fname in STEP_FILES:
            fpath = steps_dir / fname
            if not fpath.exists():
                print(f"  MISSING: {fpath}")
                continue
            n = process_file(fpath, lang, dry_run)
            total += n

    print(f"\nDone. Total markers {'would be added' if dry_run else 'added'}: {total}")


if __name__ == '__main__':
    main()
