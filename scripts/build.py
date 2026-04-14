#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# scripts/build.py
#
# PURPOSE: Build the standalone Interactive Study Viewer HTML file.
#   Reads interactiveStudy/src/{shell.html, styles.css, JS modules} and all 15
#   rawSteps markdown files (EN + BG), inlines everything into a single
#   self-contained docs/index.html (GitHub Pages).
#
# USAGE (run from repo root):
#   python3 scripts/build.py
# ---------------------------------------------------------------------------

import base64
import json
import re
import sys
from pathlib import Path

# Paths — all resolved relative to repo root regardless of cwd
REPO_ROOT         = Path(__file__).parent.parent.resolve()
SRC_DIR           = REPO_ROOT / "interactiveStudy" / "src"
DIST_DIR          = REPO_ROOT / "docs"    # served by GitHub Pages
RAW_STEPS_DIR_EN  = REPO_ROOT / "planning" / "rawSteps"
RAW_STEPS_DIR_BG  = REPO_ROOT / "planning" / "rawStepsBg"
INTRO_MD_EN       = REPO_ROOT / "deliverables" / "studyPlan" / "en" / "01_introduction.md"
INTRO_MD_BG       = REPO_ROOT / "deliverables" / "studyPlan" / "bg" / "01_introduction.md"
STUDY_PLAN_DIR    = REPO_ROOT / "deliverables" / "studyPlan"

# Study plan phase files → phase letter mapping
STUDY_PLAN_PHASE_FILES = [
    ("02_phase_a.md", "A"),
    ("03_phase_b.md", "B"),
    ("04_phase_c.md", "C"),
    ("05_phase_d.md", "D"),
    ("06_phase_e.md", "E"),
    ("07_phase_f.md", "F"),
    ("08_phase_g.md", "G"),
]

# Step file list (order matters)
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

# JS modules in dependency order (concatenated into one bundle)
JS_MODULES = [
    "config.js",
    "i18n.js",
    "lock.js",
    "cloud.js",
    "theme.js",
    "schedule.js",
    "youtube.js",
    "reading-guide.js",
    "content.js",
    "markdown.js",
    "calendar.js",
    "nav.js",
    "glossary.js",
    "main.js",
]


def read_steps(steps_dir: Path) -> dict[str, str]:
    """Read all rawSteps markdown files into a dict keyed by short ID."""
    if not steps_dir.is_dir():
        print(f"WARNING: Steps directory not found: {steps_dir}", file=sys.stderr)
        return {}

    steps: dict[str, str] = {}
    for filename in STEP_FILES:
        filepath = steps_dir / filename
        if not filepath.exists():
            print(f"WARNING: Missing step file: {filepath}", file=sys.stderr)
            continue
        # Short ID: "step_01" from "step_01_rl_basics.md"
        parts = filename.replace(".md", "").split("_")
        short_id = parts[0] + "_" + parts[1]  # "step_01"
        steps[short_id] = filepath.read_text(encoding="utf-8")
    return steps


def parse_study_plans(lang: str) -> tuple[dict[str, str], dict[str, str]]:
    """Parse study plan phase files for a given language.

    Returns:
        phase_overviews: {"A": "paragraph text...", ...}  (one per phase)
        contrib_alignments: {"step_01": "paragraph text...", ...}  (one per step)
    """
    study_dir = STUDY_PLAN_DIR / lang

    if lang == "en":
        overview_re   = re.compile(r"###\s+\d+\.\d+\s+Phase Overview\s*\n\n(.*?)(?=\n###|\Z)", re.DOTALL)
        step_sec_re   = re.compile(r"(###\s+\d+\.\d+\s+Step\s+\d+.*?)(?=\n###|\Z)", re.DOTALL)
        step_num_re   = re.compile(r"###\s+\d+\.\d+\s+Step\s+(\d+)")
        contrib_re    = re.compile(r"\*\*Contribution Alignment\.\*\*\s+(.*?)(?=\n\n\*\*Literature)", re.DOTALL)
    else:
        overview_re   = re.compile(r"###\s+\d+\.\d+\s+Преглед на етапа\s*\n\n(.*?)(?=\n###|\Z)", re.DOTALL)
        step_sec_re   = re.compile(r"(###\s+\d+\.\d+\s+Стъпка\s+\d+.*?)(?=\n###|\Z)", re.DOTALL)
        step_num_re   = re.compile(r"###\s+\d+\.\d+\s+Стъпка\s+(\d+)")
        contrib_re    = re.compile(r"\*\*Връзка с приносите\.\*\*\s+(.*?)(?=\n\n\*\*Литература)", re.DOTALL)

    phase_overviews: dict[str, str] = {}
    contrib_alignments: dict[str, str] = {}

    for filename, phase_letter in STUDY_PLAN_PHASE_FILES:
        filepath = study_dir / filename
        if not filepath.exists():
            print(f"WARNING: Study plan file not found: {filepath}", file=sys.stderr)
            continue
        text = filepath.read_text(encoding="utf-8")

        # --- Phase overview ---
        m = overview_re.search(text)
        if m:
            phase_overviews[phase_letter] = m.group(1).strip()
        else:
            print(f"WARNING: No phase overview found in {filepath}", file=sys.stderr)

        # --- Contribution alignments (one per step section) ---
        for sec_m in step_sec_re.finditer(text):
            section = sec_m.group(1)
            heading_line = section.split("\n", 1)[0]
            num_m = step_num_re.search(heading_line)
            if not num_m:
                continue
            step_id = f"step_{int(num_m.group(1)):02d}"
            ca_m = contrib_re.search(section)
            if ca_m:
                # Normalise to a single line of plain text (collapse internal whitespace)
                align_text = " ".join(ca_m.group(1).split())
                contrib_alignments[step_id] = align_text
            else:
                print(f"WARNING: No contribution alignment found for {step_id} in {filepath}", file=sys.stderr)

    return phase_overviews, contrib_alignments


def bundle_js() -> str:
    """Concatenate all JS modules in order into one bundle string."""
    parts = []
    for module in JS_MODULES:
        path = SRC_DIR / module
        if not path.exists():
            print(f"WARNING: JS module not found: {path}", file=sys.stderr)
            continue
        parts.append(f"/* === {module} === */\n" + path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def read_translations() -> dict:
    """Read both translations JSON files and return combined dict."""
    translations = {}
    for lang in ("en", "bg"):
        path = SRC_DIR / f"translations_{lang}.json"
        if not path.exists():
            print(f"WARNING: Translation file not found: {path}", file=sys.stderr)
            translations[lang] = {}
        else:
            translations[lang] = json.loads(path.read_text(encoding="utf-8"))
    return translations


def read_intro_md() -> tuple[str, str]:
    """Read bilingual intro markdown files."""
    en = INTRO_MD_EN.read_text(encoding="utf-8") if INTRO_MD_EN.exists() else ""
    bg = INTRO_MD_BG.read_text(encoding="utf-8") if INTRO_MD_BG.exists() else ""
    if not en:
        print(f"WARNING: Intro EN not found: {INTRO_MD_EN}", file=sys.stderr)
    if not bg:
        print(f"WARNING: Intro BG not found: {INTRO_MD_BG}", file=sys.stderr)
    return en, bg


def get_glossary_data() -> dict:
    """Return the bilingual glossary data dict for embedding in the viewer."""
    return {
        # ── Reinforcement Learning ──────────────────────────────────────────
        "reinforcement_learning": {
            "domain": "rl",
            "en": {"term": "Reinforcement learning", "abbr": "RL",
                   "def": "A learning paradigm where an agent learns a policy by interacting with an environment to maximise cumulative reward."},
            "bg": {"term": "Обучение с подкрепление",
                   "def": "Парадигма, при която агент научава стратегия чрез взаимодействие с среда с цел максимизиране на кумулативна награда."},
        },
        "value_function": {
            "domain": "rl",
            "en": {"term": "Value function",
                   "def": "A function estimating expected cumulative reward from a state (V) or state-action pair (Q) under a given policy."},
            "bg": {"term": "Функция на стойността",
                   "def": "Функция, оценяваща очакваната кумулативна награда от дадено състояние или двойка (състояние, действие) при зададена стратегия."},
        },
        "experience_replay": {
            "domain": "rl",
            "en": {"term": "Experience replay",
                   "def": "Stores past transitions in a replay buffer and samples them randomly during training, breaking temporal correlations."},
            "bg": {"term": "Повторение на натрупан опит",
                   "def": "Съхранява минали преходи в буфер и взема произволни мостри при обучение, нарушавайки темпоралните корелации."},
        },
        "mdp": {
            "domain": "rl",
            "en": {"term": "Markov decision process", "abbr": "MDP",
                   "def": "Mathematical framework for sequential decision-making where transitions depend only on the current state and action (Markov property)."},
            "bg": {"term": "Марковски процес на вземане на решения",
                   "def": "Математическа рамка за последователно вземане на решения, при която преходите зависят само от текущото състояние."},
        },
        "policy_gradient": {
            "domain": "rl",
            "en": {"term": "Policy gradient",
                   "def": "A family of RL algorithms that directly optimise policy parameters via gradient ascent on expected return."},
            "bg": {"term": "Градиент на стратегията",
                   "def": "Клас алгоритми за обучение с подкрепление, оптимизиращи директно параметрите на стратегията чрез градиентно изкачване."},
        },
        "advantage_function": {
            "domain": "rl",
            "en": {"term": "Advantage function",
                   "def": "A(s,a) = Q(s,a) − V(s). Measures how much better action a is compared to the average action in state s."},
            "bg": {"term": "Функция на предимството",
                   "def": "A(s,a) = Q(s,a) − V(s). Измерва колко по-добро е действие a спрямо средното действие в състояние s."},
        },
        "gae": {
            "domain": "rl",
            "en": {"term": "Generalized Advantage Estimation", "abbr": "GAE",
                   "def": "Combines n-step returns with exponential averaging (λ parameter) for low-variance advantage estimation."},
            "bg": {"term": "Обобщена оценка на предимството",
                   "def": "Комбинира n-стъпкови изчисления с експоненциално усредняване (параметър λ) за оценка на предимството с ниска дисперсия."},
        },
        "marl": {
            "domain": "rl",
            "en": {"term": "Multi-agent RL", "abbr": "MARL",
                   "def": "Multiple learning agents simultaneously interacting in a shared environment with cooperative, competitive, or mixed objectives."},
            "bg": {"term": "Многоагентно обучение с подкрепление",
                   "def": "Множество агенти, едновременно обучаващи се в обща среда с кооперативни, конкурентни или смесени цели."},
        },
        "population_based_training": {
            "domain": "rl",
            "en": {"term": "Population-based training", "abbr": "PBT",
                   "def": "Trains multiple agents simultaneously as a diverse population, using meta-game pressure to drive strategy improvement."},
            "bg": {"term": "Обучение на базата на популации",
                   "def": "Едновременно обучение на множество агенти като популация, използвайки мета-игровия натиск за подобряване на стратегиите."},
        },
        # ── Game Theory ─────────────────────────────────────────────────────
        "game_theory": {
            "domain": "game_theory",
            "en": {"term": "Game theory",
                   "def": "Mathematical study of strategic interactions between rational decision-makers, analysing optimal strategies and equilibria."},
            "bg": {"term": "Теория на игрите",
                   "def": "Математично изучаване на стратегически взаимодействия между рационални участници, анализиращо оптимални стратегии и равновесия."},
        },
        "extensive_form_game": {
            "domain": "game_theory",
            "en": {"term": "Extensive-form game",
                   "def": "A game representation with an explicit tree structure capturing sequential play, chance moves, and information sets."},
            "bg": {"term": "Игра в разгърната форма",
                   "def": "Представяне на игра с дърво, улавящо последователна игра, случайни ходове и информационни множества."},
        },
        "normal_form_game": {
            "domain": "game_theory",
            "en": {"term": "Normal-form game",
                   "def": "A game represented as a matrix of payoffs for every combination of pure strategies across all players."},
            "bg": {"term": "Игра в нормална форма",
                   "def": "Игра, представена като матрица на изплащанията за всяка комбинация от чисти стратегии на играчите."},
        },
        "imperfect_information": {
            "domain": "game_theory",
            "en": {"term": "Imperfect information",
                   "def": "Game condition where players cannot observe the full game state (e.g. hidden cards in poker). Distinct from incomplete information."},
            "bg": {"term": "Несъвършена информация",
                   "def": "Ситуация, при която играчите не могат да наблюдават пълното игрово състояние (напр. скрити карти в покер)."},
        },
        "incomplete_information": {
            "domain": "game_theory",
            "en": {"term": "Incomplete information",
                   "def": "Players have uncertainty about other players' types or payoffs (Bayesian games). Distinct from imperfect information."},
            "bg": {"term": "Непълна информация",
                   "def": "Играчите имат несигурност относно типовете или изплащанията на другите (Байесови игри). Различава се от несъвършена информация."},
        },
        "information_set": {
            "domain": "game_theory",
            "en": {"term": "Information set",
                   "def": "A set of game-tree nodes a player cannot distinguish between when making a decision, due to hidden information."},
            "bg": {"term": "Информационно множество",
                   "def": "Множество от върхове на игровото дърво, които играчът не може да различи при вземане на решение поради скрита информация."},
        },
        "nash_equilibrium": {
            "domain": "game_theory",
            "en": {"term": "Nash equilibrium",
                   "def": "A strategy profile where no player can improve their expected payoff by unilaterally changing strategy, given others' strategies are fixed."},
            "bg": {"term": "Равновесие на Наш",
                   "def": "Стратегически профил, при който нито един играч не може да подобри очакваната си печалба чрез едностранна промяна на стратегията."},
        },
        "exploitability": {
            "domain": "game_theory",
            "en": {"term": "Exploitability",
                   "def": "How far a strategy is from Nash equilibrium — the maximum additional payoff an optimal adversary can extract against it."},
            "bg": {"term": "Експлоатируемост",
                   "def": "Мярка за отдалеченост на стратегия от равновесие на Наш — максималното допълнително изплащане, което оптимален опонент може да извлече."},
        },
        "safe_exploitation": {
            "domain": "game_theory",
            "en": {"term": "Safe exploitation",
                   "def": "Exploiting an opponent's weaknesses while maintaining a formal guarantee of near-Nash performance against any opponent."},
            "bg": {"term": "Безопасна експлоатация",
                   "def": "Използване на слабостите на опонента при запазване на гаранция за почти равновесно представяне срещу произволен опонент."},
        },
        "zero_sum_game": {
            "domain": "game_theory",
            "en": {"term": "Zero-sum game",
                   "def": "One player's gain exactly equals another's loss — total payoff is constant. Poker and chess are zero-sum."},
            "bg": {"term": "Игра с нулева сума",
                   "def": "Печалбата на един играч е равна на загубата на другите — сборът на всички изплащания е константен."},
        },
        "mixed_strategy": {
            "domain": "game_theory",
            "en": {"term": "Mixed strategy",
                   "def": "A probability distribution over pure strategies, allowing randomised play. Nash equilibrium often requires mixed strategies."},
            "bg": {"term": "Смесена стратегия",
                   "def": "Вероятностно разпределение върху чисти стратегии, позволяващо рандомизирана игра. Равновесието на Наш обикновено изисква смесени стратегии."},
        },
        "counterfactual_value": {
            "domain": "game_theory",
            "en": {"term": "Counterfactual value",
                   "def": "Expected value of reaching and playing from a node, assuming the player acts to reach it but otherwise plays their current strategy."},
            "bg": {"term": "Контрафактуална стойност",
                   "def": "Очакваната стойност от достигане и игра от дадения връх, при условие че играчът действа за достигане на върха, но иначе играе текущата стратегия."},
        },
        "regret": {
            "domain": "game_theory",
            "en": {"term": "Regret",
                   "def": "Difference between the payoff of the best hindsight action and the actual payoff. Minimising cumulative regret leads to Nash equilibrium."},
            "bg": {"term": "Съжаление",
                   "def": "Разлика между изплащането на най-доброто действие на преглед и действително полученото. Минимизирането на кумулативното съжаление води към равновесие."},
        },
        "coalition": {
            "domain": "game_theory",
            "en": {"term": "Coalition",
                   "def": "A group of players coordinating strategies toward a shared goal, common in cooperative game theory and free-for-all games."},
            "bg": {"term": "Коалиция",
                   "def": "Група от играчи, координиращи стратегиите си за постигане на обща цел — характерна за кооперативната теория на игрите и FFA игри."},
        },
        "opponent_modeling": {
            "domain": "game_theory",
            "en": {"term": "Opponent modeling",
                   "def": "Inferring and predicting an opponent's strategy or behavioural type to adapt one's own play or exploit weaknesses."},
            "bg": {"term": "Моделиране на противника",
                   "def": "Извличане и прогнозиране на стратегията или поведенческия тип на опонента за адаптиране на собствената игра или използване на слабости."},
        },
        "game_tree": {
            "domain": "game_theory",
            "en": {"term": "Game tree",
                   "def": "The complete tree of all possible states, actions, and transitions in an extensive-form game. Exponentially large in practice."},
            "bg": {"term": "Дърво на играта",
                   "def": "Пълното дърво от всички възможни игрови състояния, действия и преходи. Експоненциално голямо на практика."},
        },
        "subgame_solving": {
            "domain": "game_theory",
            "en": {"term": "Subgame solving",
                   "def": "Resolving a portion of the game tree independently at runtime, enabling strong play in large games through focused computation."},
            "bg": {"term": "Решаване на подигри",
                   "def": "Самостоятелно решаване на подграф от игровото дърво по време на игра, осигуряващо силна игра в мащабни игри."},
        },
        "behavioral_cloning": {
            "domain": "game_theory",
            "en": {"term": "Behavioral cloning",
                   "def": "Learning a policy by imitating recorded expert behaviour via supervised learning on (state, action) pairs."},
            "bg": {"term": "Поведенческо клониране",
                   "def": "Научаване на стратегия чрез имитация на записано поведение на експерт с наблюдавано обучение върху двойки (състояние, действие)."},
        },
        "non_stationarity": {
            "domain": "game_theory",
            "en": {"term": "Non-stationarity",
                   "def": "Property of an environment or opponent whose underlying behaviour changes over time, making convergence harder for a learning agent."},
            "bg": {"term": "Нестационарност",
                   "def": "Свойство на среда или опонент, при което основното поведение се променя с времето, затруднявайки сходимостта на обучаващия се агент."},
        },
        "spinning_top": {
            "domain": "game_theory",
            "en": {"term": "Spinning top decomposition",
                   "def": "Decomposes multi-agent interactions into transitive (rankable) and cyclic (rock-paper-scissors) components (Balduzzi et al., 2019)."},
            "bg": {"term": 'Декомпозиция \u201e\u043f\u0443\u043c\u043f\u0430\u043b\u201c',
                   "def": "Декомпозиция на многоагентни взаимодействия на транзитивни (класируеми) и цикличерни компоненти (Balduzzi et al., 2019)."},
        },
        "shapley_value": {
            "domain": "game_theory",
            "en": {"term": "Shapley value",
                   "def": "Cooperative game theory concept allocating credit to each player proportional to their marginal contribution across all possible coalitions."},
            "bg": {"term": "Стойност на Шапли",
                   "def": "Концепция от кооперативната теория на игрите, разпределяща заслугата на всеки играч пропорционално на маргиналния му принос."},
        },
        "action_abstraction": {
            "domain": "game_theory",
            "en": {"term": "Action abstraction",
                   "def": "Reducing the action space by grouping similar actions together, making large games computationally tractable."},
            "bg": {"term": "Абстракция на действията",
                   "def": "Намаляване на пространството от действия чрез групиране на сходни действия, правейки мащабни игри изчислително обработваеми."},
        },
        "behavioral_trace": {
            "domain": "game_theory",
            "en": {"term": "Behavioral trace",
                   "def": "A recorded sequence of observable actions made by a player during gameplay, used for opponent modelling and analysis."},
            "bg": {"term": "Поведенчески проследявания",
                   "def": "Записана последователност от наблюдаеми действия на играч по време на игра, използвана за моделиране и анализ."},
        },
        "kuhn_poker": {
            "domain": "game_theory",
            "en": {"term": "Kuhn Poker",
                   "def": "Minimal two-player imperfect-information poker variant with a 3-card deck (J, Q, K). Has a known analytical Nash equilibrium, making it ideal for verifying CFR implementations."},
            "bg": {"term": "Kuhn Poker",
                   "def": "Минимален вариант на покер за двама играчи с несъвършена информация с тесте от 3 карти (J, Q, K). Притежава известно аналитично равновесие на Наш, което го прави идеален за верификация на CFR имплементации."},
        },
        "leduc_holdem": {
            "domain": "game_theory",
            "en": {"term": "Leduc Hold'em",
                   "def": "Small two-player poker benchmark with a 6-card deck (two suits of J, Q, K) and two betting rounds. Has ~936 information sets and serves as a standard scalability testbed."},
            "bg": {"term": "Leduc Hold'em",
                   "def": "Малък бенчмарк за покер за двама играчи с тесте от 6 карти (два цвята J, Q, K) и два кръга на залагане. Има ~936 информационни множества и е стандартна тестова среда за мащабируемост."},
        },
        "so_long_sucker": {
            "domain": "game_theory",
            "en": {"term": "So Long Sucker",
                   "def": "Classic 4-player negotiation and coalition game designed by von Neumann. Involves chip trading with binding deals that can be betrayed, making it a testbed for multi-agent dynamics and coalition stability."},
            "bg": {"term": "So Long Sucker",
                   "def": "Класическа игра за четирима играчи с преговори и коалиции, разработена от фон Нойман. Включва търговия с чипове и обвързващи споразумения, чието нарушаване е разрешено — тестова среда за многоагентна динамика и стабилност на коалициите."},
        },
        # ── Algorithms ──────────────────────────────────────────────────────
        "cfr": {
            "domain": "algorithms",
            "en": {"term": "Counterfactual Regret Minimization", "abbr": "CFR",
                   "def": "Iterative self-play algorithm minimising per-information-set regret. Provably converges to Nash equilibrium in two-player zero-sum games."},
            "bg": {"term": "Минимизиране на контрафактуалното съжаление",
                   "def": "Итеративен алгоритъм за самоигра, минимизиращ съжалението на всяко информационно множество. Сходи към равновесие на Наш при двама играчи."},
        },
        "mccfr": {
            "domain": "algorithms",
            "en": {"term": "Monte Carlo CFR", "abbr": "MCCFR",
                   "def": "Samples game trajectories instead of traversing the full tree, making CFR scalable to games too large for full traversal."},
            "bg": {"term": "Монте Карло вариант на CFR",
                   "def": "Използва Монте Карло семплиране на игрови траектории вместо пълно обхождане на дървото, правейки CFR мащабируем."},
        },
        "cfr_plus": {
            "domain": "algorithms",
            "en": {"term": "CFR+",
                   "def": "CFR variant using regret matching+ and alternating updates, achieving faster practical convergence than standard CFR."},
            "bg": {"term": "CFR+",
                   "def": "Вариант на CFR с регрет мачинг+ и редуващи се обновявания, постигащ по-бърза практическа сходимост от стандартния CFR."},
        },
        "dqn": {
            "domain": "algorithms",
            "en": {"term": "Deep Q-Network", "abbr": "DQN",
                   "def": "Combines Q-learning with a neural network, experience replay, and a target network to stabilise training on high-dimensional inputs."},
            "bg": {"term": "Дълбока Q-мрежа",
                   "def": "Комбинира Q-обучение с невронна мрежа, повторение на опит и целева мрежа за стабилизиране на обучението върху многомерни входове."},
        },
        "ppo": {
            "domain": "algorithms",
            "en": {"term": "Proximal Policy Optimization", "abbr": "PPO",
                   "def": "Policy gradient algorithm using a clipped surrogate objective to prevent large policy updates, achieving TRPO-like stability with first-order methods."},
            "bg": {"term": "Оптимизация на стратегията с ограничение на близостта",
                   "def": "Алгоритъм с изрязана сурогатна цел, предотвратяваща прекалено големи обновявания — постига стабилност като TRPO с методи от първи ред."},
        },
        "deep_cfr": {
            "domain": "algorithms",
            "en": {"term": "Deep CFR",
                   "def": "Uses neural networks to approximate regret and strategy functions in CFR, enabling application to games too large for tabular methods."},
            "bg": {"term": "Deep CFR",
                   "def": "Използва невронни мрежи за апроксимация на функциите за съжаление и стратегия в CFR, позволявайки приложение в мащабни игри."},
        },
        "rebel": {
            "domain": "algorithms",
            "en": {"term": "ReBeL", "abbr": "ReBeL",
                   "def": "Recursive Belief-based Learning — combines CFR subgame solving with deep RL value estimation for strong play in large imperfect-information games."},
            "bg": {"term": "ReBeL",
                   "def": "Recursive Belief-based Learning — комбинира CFR решаване на подигри с дълбоко RL за оценка на стойността в мащабни игри."},
        },
        "psro": {
            "domain": "algorithms",
            "en": {"term": "Policy Space Response Oracles", "abbr": "PSRO",
                   "def": "Iteratively computes best responses in a population meta-game, approximating Nash equilibrium through an empirical game-theoretic framework."},
            "bg": {"term": "Оракули за отговор в пространството на стратегиите",
                   "def": "Итеративно изчислява най-добри отговори в мета-игра на популация, апроксимирайки равновесие чрез емпиричен теоретико-игрови анализ."},
        },
        "maddpg": {
            "domain": "algorithms",
            "en": {"term": "MADDPG",
                   "def": "Multi-Agent DDPG — extends DDPG with centralised training and decentralised execution for cooperative/competitive MARL."},
            "bg": {"term": "MADDPG",
                   "def": "Многоагентен DDPG — разширява DDPG с централизирано обучение и децентрализирано изпълнение за кооперативни/конкурентни задачи."},
        },
        "qmix": {
            "domain": "algorithms",
            "en": {"term": "QMIX",
                   "def": "Factors the joint Q-value as a monotone combination of individual Q-values, enabling efficient cooperative multi-agent training."},
            "bg": {"term": "QMIX",
                   "def": "Факторизира съвместната Q-стойност като монотонна комбинация от Q-стойностите на отделните агенти за ефективно кооперативно обучение."},
        },
        "mappo": {
            "domain": "algorithms",
            "en": {"term": "MAPPO",
                   "def": "Multi-Agent PPO — extends PPO with a centralised critic and decentralised actors, a strong cooperative MARL baseline."},
            "bg": {"term": "MAPPO",
                   "def": "Многоагентна PPO — разширява PPO с централизиран критик и децентрализирани актьори, силна базова линия за кооперативни задачи."},
        },
        "lola": {
            "domain": "algorithms",
            "en": {"term": "LOLA",
                   "def": "Learning with Opponent-Learning Awareness — meta-learning algorithm accounting for how one agent's updates affect co-learners' future policies."},
            "bg": {"term": "LOLA",
                   "def": "Обучение с осъзнаване на обучението на противника — мета-алгоритъм, отчитащ как обновяванията на агента влияят на бъдещите стратегии на съ-учещите."},
        },
        "alpha_rank": {
            "domain": "algorithms",
            "en": {"term": "α-Rank",
                   "def": "Evolutionary ranking algorithm based on long-run dominance in multi-player tournaments, providing a solution concept beyond Nash equilibrium."},
            "bg": {"term": "α-Rank",
                   "def": "Еволюционен алгоритъм за класиране по дългосрочна доминация в многоплейърен турнир — решение отвъд равновесието на Наш."},
        },
        "egta": {
            "domain": "algorithms",
            "en": {"term": "Empirical Game-Theoretic Analysis", "abbr": "EGTA",
                   "def": "Combines agent simulation with game theory — uses a small simulated meta-game to analyse strategies without solving the full game."},
            "bg": {"term": "Емпиричен теоретико-игрови анализ",
                   "def": "Комбинира симулация на агенти с теория на игрите — анализира стратегии чрез симулирана мета-игра без да решава пълната игра."},
        },
        "pikl": {
            "domain": "algorithms",
            "en": {"term": "piKL",
                   "def": "KL-divergence regularisation term added to the policy objective, preventing excessive deviation from a reference strategy during adaptation."},
            "bg": {"term": "piKL",
                   "def": "KL-дивергентна регуларизация в целевата функция, предотвратяваща прекомерно отклонение от базова стратегия при адаптация."},
        },
        # ── Evaluation ──────────────────────────────────────────────────────
        "evaluation_framework": {
            "domain": "evaluation",
            "en": {"term": "Evaluation framework",
                   "def": "A systematic methodology for comparing and assessing agent performance across diverse opponents, environments, and metrics."},
            "bg": {"term": "Рамка за оценяване",
                   "def": "Систематична методология за сравняване и оценяване на представянето на агенти при разнообразни опоненти, среди и метрики."},
        },
        "convergence": {
            "domain": "evaluation",
            "en": {"term": "Convergence",
                   "def": "An algorithm approaching a stable fixed point (e.g. Nash equilibrium) as iterations increase. Key metric for CFR-family algorithms."},
            "bg": {"term": "Сходимост",
                   "def": "Свойство на алгоритъм да се доближава към стабилна точка (напр. равновесие на Наш) с увеличаване на итерациите."},
        },
        "benchmark": {
            "domain": "evaluation",
            "en": {"term": "Benchmark",
                   "def": "A standardised task, game, or environment used to compare algorithm performance in a reproducible, fair manner."},
            "bg": {"term": "Еталонен тест",
                   "def": "Стандартизирана задача, игра или среда, използвана за сравнение на алгоритми по възпроизводим и справедлив начин."},
        },
        "hyperparameter": {
            "domain": "evaluation",
            "en": {"term": "Hyperparameter",
                   "def": "A parameter controlling the learning process (e.g. learning rate, network size, discount factor) rather than being learned from data."},
            "bg": {"term": "Хиперпараметър",
                   "def": "Параметър, управляващ процеса на обучение (напр. скорост на учене, размер на мрежа), а не научаван от данните."},
        },
        "robustness": {
            "domain": "evaluation",
            "en": {"term": "Robustness",
                   "def": "Ability of a strategy to maintain acceptable performance across a wide range of opponents, environments, and perturbations."},
            "bg": {"term": "Устойчивост",
                   "def": "Способността на стратегия да поддържа приемливо представяне при широк диапазон от опоненти, среди и смущения."},
        },
        "adaptability": {
            "domain": "evaluation",
            "en": {"term": "Adaptability",
                   "def": "Ability of an agent to modify its strategy in response to changing opponent behaviour or environmental conditions."},
            "bg": {"term": "Адаптивност",
                   "def": "Способността на агент да модифицира стратегията си в отговор на промени в поведението на опонента или условията на средата."},
        },
    }


def get_favicon_link() -> str:
    """Return a text-based favicon link with 'RL' text."""
    return '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text x=%2250%22 y=%2275%22 font-size=%2280%22 font-weight=%22bold%22 text-anchor=%22middle%22 fill=%22%231e293b%22>RL</text></svg>">'


def generate_content_script(steps_en: dict, steps_bg: dict, translations: dict,
                             intro_en: str, intro_bg: str,
                             phase_overviews_en: dict, phase_overviews_bg: dict,
                             contrib_align_en: dict, contrib_align_bg: dict) -> str:
    """Generate a <script> block embedding EN/BG content, translations, and glossary."""
    def dict_to_js(d: dict, var_name: str) -> str:
        pairs = [f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in d.items()]
        return f"const {var_name} = {{\n" + ",\n".join(pairs) + "\n};"

    en_js              = dict_to_js(steps_en, "STEPS_CONTENT_EN")
    bg_js              = dict_to_js(steps_bg, "STEPS_CONTENT_BG")
    trans_js           = f"const TRANSLATIONS = {json.dumps(translations, ensure_ascii=False, indent=2)};"
    intro_en_js        = f"const INTRO_MD_EN = {json.dumps(intro_en)};"
    intro_bg_js        = f"const INTRO_MD_BG = {json.dumps(intro_bg)};"
    glossary_js        = f"const GLOSSARY_DATA = {json.dumps(get_glossary_data(), ensure_ascii=False, indent=2)};"
    phase_ov_en_js     = dict_to_js(phase_overviews_en, "PHASE_OVERVIEWS_EN")
    phase_ov_bg_js     = dict_to_js(phase_overviews_bg, "PHASE_OVERVIEWS_BG")
    contrib_en_js      = dict_to_js(contrib_align_en, "CONTRIB_ALIGN_EN")
    contrib_bg_js      = dict_to_js(contrib_align_bg, "CONTRIB_ALIGN_BG")

    return (
        f"<script>\n{en_js}\n\n{bg_js}\n\n{trans_js}\n\n"
        f"{intro_en_js}\n{intro_bg_js}\n\n{glossary_js}\n\n"
        f"{phase_ov_en_js}\n\n{phase_ov_bg_js}\n\n"
        f"{contrib_en_js}\n\n{contrib_bg_js}\n</script>"
    )


def write_service_worker(dist_dir: Path) -> None:
    """Write docs/sw.js — network-first with cache fallback for offline use."""
    sw_content = """\
const CACHE_NAME = 'rl-study-v2';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.add('./'))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      }).catch(() => caches.match('./'))
    );
  }
});
"""
    (dist_dir / "sw.js").write_text(sw_content, encoding="utf-8")


def build():
    """Main build: inline CSS, JS modules, translations, and content into shell.html."""
    # Read source files
    shell_html = (SRC_DIR / "shell.html").read_text(encoding="utf-8")
    styles_css = (SRC_DIR / "styles.css").read_text(encoding="utf-8")

    # Bundle all JS modules
    app_js = bundle_js()

    # Read step content (EN + BG)
    steps_en = read_steps(RAW_STEPS_DIR_EN)
    steps_bg = read_steps(RAW_STEPS_DIR_BG)
    if not steps_en:
        print("ERROR: No EN step files found.", file=sys.stderr)
        sys.exit(1)

    # Read translations
    translations = read_translations()

    # Read bilingual intro markdown
    intro_en, intro_bg = read_intro_md()

    # Parse study plan data: phase overviews + contribution alignments
    phase_overviews_en, contrib_align_en = parse_study_plans("en")
    phase_overviews_bg, contrib_align_bg = parse_study_plans("bg")
    print(f"  Phase overviews EN: {len(phase_overviews_en)}, BG: {len(phase_overviews_bg)}")
    print(f"  Contribution alignments EN: {len(contrib_align_en)}, BG: {len(contrib_align_bg)}")

    # Generate combined content + translations script
    content_script = generate_content_script(
        steps_en, steps_bg, translations, intro_en, intro_bg,
        phase_overviews_en, phase_overviews_bg,
        contrib_align_en, contrib_align_bg,
    )

    # Build favicon link
    favicon_link = get_favicon_link()

    # Replace placeholders
    output = shell_html
    output = output.replace("<!-- INLINE_CSS -->", f"<style>\n{styles_css}\n</style>")
    output = output.replace("<!-- INLINE_JS -->", f"<script>\n{app_js}\n</script>")
    output = output.replace("<!-- INLINE_CONTENT -->", content_script)
    output = output.replace("<!-- INLINE_FAVICON -->", favicon_link)

    # Write output
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIST_DIR / "index.html"
    out_path.write_text(output, encoding="utf-8")

    # .nojekyll prevents GitHub Pages from running Jekyll on our built HTML
    (DIST_DIR / ".nojekyll").touch()

    # Service worker
    write_service_worker(DIST_DIR)

    size_kb = out_path.stat().st_size / 1024
    print(f"Built {out_path} ({size_kb:.0f} KB)")
    print(f"  EN steps: {len(steps_en)}, BG steps: {len(steps_bg)}")
    print(f"  Translations: {list(translations.keys())}")
    print(f"  JS modules: {len(JS_MODULES)}")
    print(f"  Phase overviews EN: {sorted(phase_overviews_en)}, BG: {sorted(phase_overviews_bg)}")
    print(f"  Contrib alignments EN: {len(contrib_align_en)} steps, BG: {len(contrib_align_bg)} steps")


if __name__ == "__main__":
    build()
