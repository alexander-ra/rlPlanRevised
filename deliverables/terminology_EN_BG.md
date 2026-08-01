# Terminology Reference: English → Bulgarian

> Auxiliary file for translating `studyPlanEN.md` into Bulgarian.
> Goal: minimize unnecessary foreign borrowings while maintaining scientific register.
> Convention: On first occurrence in the Bulgarian text, give the Bulgarian term followed
> by the English original in parentheses. Subsequent occurrences use only the Bulgarian form.
> Algorithm abbreviations (CFR, DQN, PPO, MARL, etc.) are kept in Latin script throughout.

---

## 1. Document Structure and Administrative Terms

| English | Bulgarian | Notes |
|---------|----------|-------|
| Individual study plan | Индивидуален план за обучение | Standard university term |
| Doctoral student | Докторант | |
| Scientific supervisor | Научен ръководител | |
| Scientific consultant | Научен консултант | |
| Dissertation / Thesis | Дисертация / Дисертационен труд | |
| Official research focus / Dissertation title | Изследване на възможностите за приложение на изкуствения интелект в компютърни игри | |
| Contribution | Принос | научен принос |
| Expected contribution | Очакван принос | |
| Research objective | Цел на изследването | |
| Research context | Изследователски контекст | |
| Literature review | Преглед на литературата | |
| Methodology | Методология | |
| Phase | Фаза / Етап | „Етап" is more native-sounding |
| Step (study step) | Стъпка | |
| Duration | Продължителност | |
| Milestone | Етапен срок | Avoid „майлстоун" |
| Buffer (schedule) | Резерв от време | |
| Study plan structure | Структура на плана за обучение | |
| Enrollment | Зачисляване | |
| Defense (thesis) | Защита (на дисертация) | |
| Approved by | Одобрил / Утвърдил | |
| Preprint | Предварителна публикация | Or keep „препринт" if clarity demands it |
| et al. | и др. | |
| The present study | Настоящото изследване | |

---

## 2. Game Theory

| English | Bulgarian | Notes |
|---------|----------|-------|
| Game theory | Теория на игрите | |
| Extensive-form game | Игра в разгърната форма | |
| Normal-form game | Игра в нормална форма | |
| Imperfect information | Непълна информация | Settled. „Несъвършена" is retired — the corpus uses „непълна" throughout |
| Perfect information | Пълна информация | |
| Incomplete information | Непълна по Харшани информация | Bayesian games. Qualified, because plain „непълна информация" is now imperfect information |
| Information set | Информационно множество | |
| Nash equilibrium | Равновесие на Наш | |
| Equilibrium strategy | Равновесна стратегия | |
| Best response | Най-добър отговор | |
| Bucket (abstraction) | Клъстер | Не „кофа" / „кош"; мъжки род |
| Critic (network) | Оценител | Но устойчивото словосъчетание остава „актьор-оценител" |
| Game AI | Игрови изкуствен интелект | Не „изкуствен интелект в игрите" |
| LLM / LLM agent | Голям езиков модел / агент с голям езиков модел | В проза; етикетите в таблици остават „LLM" |
| Oracle (algorithmic) | Предсказвач | Not „оракул"/„оракъл" — those read as the mythological sense |
| Oracle value (omniscient estimate) | Приблизителна стойност | ⚠ NOT „предсказвач стойност" — the *oracle* sense here is a value, not a component |
| State-of-the-art | Водещ стандарт | Also as an adjective: „водещ стандарт при…". Not „най-съвременно ниво" |
| Jack / Queen / King (cards) | Вале / Дама / Поп | Kuhn poker J/Q/K. „Цар" is retired |
| Best-response oracle | Предсказвач за най-добър отговор | |
| Double oracle | Двоен предсказвач | |
| Exploitability | Експлоатируемост | Neologism; alt: „степен на уязвимост към експлоатация" |
| Exploitation | Експлоатация | In strategic sense, not pejorative |
| Safe exploitation | Безопасна експлоатация | „Безопасна" = safe (security-sense) |
| Zero-sum game | Игра с нулева сума | |
| Strategy | Стратегия | |
| Strategy profile | Стратегически профил | |
| Mixed strategy | Смесена стратегия | |
| Payoff | Печалба | |
| Utility | Полезност | |
| Counterfactual value | Контрафактуална стойност | Foreign root unavoidable; gloss on first use: „хипотетична стойност при отклонение от текущата стратегия" |
| Regret (algorithmic) | Съжаление | Standard term in BG optimization literature |
| Cumulative regret | Сборно съжаление | Also: кумулативно |
| Coalition | Коалиция | |
| Coalition formation | Формиране на коалиции | |
| Free-for-all (FFA) | Игри всеки срещу всеки | Винаги описателно, не „FFA" |
| Opponent modeling | Моделиране на противника | |
| Behavioral trace | Поведенчески проследявания | Or „наблюдавана последователност от действия" |
| Bayesian opponent modeling | Байесово моделиране на противника | |
| Type-based model | Типово базиран модел | |
| Consistent opponent modeling | Консистентно моделиране на противника | |
| Restricted Nash Response (RNR) | Ограничен Наш отговор | Keep „RNR" abbreviation in Latin |
| Teaching attack | Обучаваща атака | Adversarial manipulation of opponent model |
| Adaptation safety | Безопасност на адаптацията | Ge et al. (2024) safety notion |
| Exploitation–safety tradeoff | Компромис между експлоатация и безопасност | |
| Safety theorem | Теорема за безопасността | Ganzfried & Sandholm (2015) |
| Pareto frontier | Парето граница | |
| Spinning top decomposition | Декомпозиция „пумпал" | Transitive-cyclic decomposition (Balduzzi et al., 2019) |
| Empirical Game-Theoretic Analysis (EGTA) | Емпиричен теоретико-игрови анализ | Keep „EGTA" in Latin |
| Shapley value | Стойност на Шапли | |
| Shapley Q-value | Q-стойност на Шапли | Credit assignment in MARL |
| So Long Sucker (SLS) | — | Keep game name in English; „SLS" in Latin |
| Non-stationarity (multi-agent) | Нестационарност | |
| piKL regularization | piKL регуларизация | Keep notation in Latin |
| Decision Transformer | Трансформатор за решения | Or keep „Decision Transformer" with gloss on first use |
| Adversarially Robust Decision Transformer (ARDT) | Устойчив на противник трансформатор за решения | Keep „ARDT" in Latin |
| Behavioral cloning | Поведенческо клониране | |
| Player embedding (player2vec) | Вграждане на играч | Keep „player2vec" in Latin |
| Collusion detection | Разпознаване на тайно съглашение | |
| Chip dumping | Прехвърляне на чипове | Collusion signal |
| Soft play | Пасивна игра срещу съучастник | Collusion signal |
| VPIP | Voluntarily Put In Pot | Keep abbreviation in Latin |
| PFR | Pre-Flop Raise | Keep abbreviation in Latin |
| State tensor encoding | Тензорно кодиране на състоянието | |
| Hand history | История на ръце | Poker record format |
| Approximate exploitability | Приблизителна експлоатируемост | RL-based best response estimation |
| Marginal exploitability | Маргинална експлоатируемост | N-player extension |
| α-Rank | α-Rank | Keep in Latin; „еволюционно класиране" as gloss |
| VasE | VasE | Keep in Latin; „оценяване чрез теория на социалния избор" as gloss |
| AIVAT | AIVAT | Keep in Latin; „редукция на дисперсията чрез контролни варианти" as gloss |
| Maximal lottery | Максимална лотария | Social choice theory concept |
| Intransitive cycle | Нетранзитивен цикъл | |
| Bot zoo | Зоопарк от агенти | Reference agent collection for evaluation |
| Research frontier | Изследователска граница | |
| Publication pipeline | Публикационен план | |
| Dissertation chapter | Глава на дисертацията | |
| Subgame solving | Решаване на под-игри | |
| Nested subgame solving | Вложено решаване на под-игри | Brown & Sandholm (2017) |
| Safe subgame solving | Безопасно решаване на под-игри | |
| Augmented subgame | Разширена под-игра | Subgame plus alternative-payoff nodes |
| Action abstraction | Абстракция на действията | |
| Information abstraction | Информационна абстракция | |
| Card bucketing | Групиране на карти | „Групиране" avoids anglicism |
| Game tree | Дърво на играта | |
| Signal tree | Сигнално дърво | Smaller than game tree (Gilpin & Sandholm 2007) |
| Chance node | Възел на случайността | |
| Terminal state | Крайно състояние | |
| Lossless abstraction | Беззагубна абстракция | Standard CS BG; avoid „безпотерна" |
| Lossy abstraction | Абстракция със загуби | Use „със загуби" as adjectival phrase, not „загубна" |
| Exploitability gap | Пропуск в експлоатируемостта | Prefer prepositional phrase over adj+noun „експлоатируемостен пропуск" |
| Action translation | Транслация на действия | Deliberate anglicism, and the one exception to rule 4: „превод" collides with translation of *text*, which the corpus also discusses |
| Nearest-action translator | Транслатор към най-близкото действие | |
| Probability-split translator | Вероятностно разделяне | |
| Pseudo-harmonic mapping | Псевдохармонично преобразуване | Ganzfried & Sandholm (2013); single word, no hyphen |
| Suit isomorphism | Изоморфизъм на цветовете | Suit = цвят (на карта) |
| Ordered game isomorphism (OGI) | Подреден игрови изоморфизъм | Gilpin & Sandholm Definition 3.2 |
| Hand-strength distribution (HSD) | Разпределение на силата на ръката | Keep „HSD" abbreviation in Latin |
| Earth Mover's Distance (EMD) | Разстояние на Васерщайн | Keep „EMD" abbreviation in Latin. The same quantity as Wasserstein-1; „Земекопача"/„Земьов-Мъри" are retired — a calque that reads as a surname |
| Perfect recall | Пълна памет | Follows the пълна/непълна decision above |
| Imperfect recall | Непълна памет | |
| Reach probability | Вероятност за достигане | |
| Reach-weighted bound | Граница, претеглена по достигането | Kroer & Sandholm (2016) |
| Counterfactual best-response value (CBV) | Стойност на най-добрия отговор по контрафактуалния стандарт | Keep „CBV" symbolic |
| Blueprint (strategy) | Схема (на стратегията) | |
| Off-tree action | Действие извън дървото | |
| Information bottleneck (IB) | Информационно стеснение | Keep „IB" abbreviation in Latin. „Тясно място" is retired |
| Bottleneck (general) | Стеснение | |
| Equivariant encoder | Еквивариантен кодер | |
| Production-grade | Промишлено ниво / промишлен | Use „промишлен", not „продуктивен" (false friend) |
| Fixed-limit (poker) | С лимит / лимитен | „Ледюк с лимит" preferred over „лимит Ледюк" |
| Fixed-limit Leduc | Ледюк с лимит | Винаги „Ледюк" на кирилица, с главна буква |
| No-limit (poker) | Безлимитен | |
| Wall-clock budget | Бюджет в реално време | |
| Smoke test | Бърза проверка със смалени бюджети | Avoid calque „димен тест" |

---

## 3. Reinforcement Learning

| English | Bulgarian | Notes |
|---------|----------|-------|
| Reinforcement learning (RL) | Обучение с подкрепление | Не „обучение с подсилване" |
| Agent | Агент | |
| Environment | Среда | |
| Policy | Стратегия | In RL context, „стратегия" is standard in BG |
| Optimal policy | Оптимална стратегия | |
| Value function | Функция на стойността | |
| State-value function | Функция на стойността на състоянието | Or V-функция |
| Action-value function | Функция на стойността на действието | Or Q-функция |
| Reward | Награда | |
| Cumulative reward / Return | Кумулативна награда / Възвръщаемост | |
| Discount factor | Дисконтиращ множител | |
| Experience replay | Повторение на натрупан опит | On first mention, then abbreviated |
| Markov decision process (MDP) | Марковски процес на вземане на решения | Keep „MDP" abbreviation in Latin |
| Policy gradient | Градиент на стратегията | |
| Advantage function | Функция на предимството | |
| Generalized advantage estimation (GAE) | Обобщена оценка на предимството | |
| Clipped surrogate objective | Изрязана сурогатна цел | Also: ограничена / отрязана заместваща целева функция |
| Target network | Целева мрежа | |
| Multi-agent RL (MARL) | Многоагентно обучение с подкрепление | |
| Population-based training | Обучение на базата на популации | |

---

## 4. Algorithm Names

> Algorithm proper names and abbreviations are kept in English (Latin script).
> On first mention, give the full English name, then the Bulgarian descriptive gloss in parentheses.
> The same holds for **named systems**: Libratus, Pluribus, DeepStack, ReBeL, Student of Games,
> AlphaStar, AlphaGo, OpenSpiel, Stable-Baselines3. Never transliterate them („Либратус" is wrong).
> Only *games* are transliterated, because they are read aloud in the text: Кун, Ледюк, Го.

| Abbreviation | Full English Name | Bulgarian Gloss (first mention only) |
|-------------|-------------------|--------------------------------------|
| CFR | Counterfactual Regret Minimization | Минимизиране на контрафактуалното съжаление |
| MCCFR | Monte Carlo CFR | Монте Карло вариант на CFR |
| CFR+ | CFR+ | Ускорен вариант на CFR |
| DQN | Deep Q-Network | Дълбока Q-мрежа |
| PPO | Proximal Policy Optimization | Оптимизация на стратегията с ограничение на близостта |
| Deep CFR | Deep CFR | Дълбок CFR (невронна апроксимация на CFR) |
| DREAM | Deep Regret minimization with Advantage baselines and Model-free learning | — |
| ReBeL | Recursive Belief-based Learning | Рекурсивно обучение на основата на убеждения |
| piKL | Policy-regularized KL | — (keep as notation) |
| RNR | Restricted Nash Response | Ограничен Наш отговор |
| SES | Safe Exploitation Subgame | Безопасна експлоатация на под-игри |
| OX-Search | Opponent Exploitation Search | — (keep as algorithm name) |
| ABD | Adapting Beyond the Depth limit | — (keep as algorithm name) |
| MADDPG | Multi-Agent Deep Deterministic Policy Gradient | Многоагентен дълбок детерминистичен градиент на стратегията |
| QMIX | QMIX | Монотонна факторизация на стойностната функция |
| MAPPO | Multi-Agent PPO | Многоагентна PPO |
| PSRO | Policy Space Response Oracles | Предсказвачи за отговор в пространството на стратегиите |
| PBT | Population-Based Training | Обучение на базата на популации |
| LOLA | Learning with Opponent-Learning Awareness | Обучение с осъзнаване на обучението на противника |
| CommNet | Communication Neural Network | Комуникационна невронна мрежа |
| EGTA | Empirical Game-Theoretic Analysis | Емпиричен теоретико-игрови анализ |
| DT | Decision Transformer | Трансформатор за решения |
| ARDT | Adversarially Robust Decision Transformer | Устойчив на противник трансформатор за решения |
| CQL | Conservative Q-Learning | Консервативно Q-обучение |
| α-Rank | Alpha-Rank | Еволюционно класиране на агенти |
| VasE | Voting as Stochastic Estimation | Оценяване чрез теория на социалния избор |
| AIVAT | AIVAT | Редукция на дисперсията чрез контролни варианти |

---

## 5. Evaluation and Methodology

| English | Bulgarian | Notes |
|---------|----------|-------|
| Evaluation framework | Рамка за оценяване | |
| Exploitability metric | Метрика за експлоатируемост | |
| Convergence | Сходимост | |
| Convergence rate | Скорост на сходимост | |
| Benchmark | Еталонен тест | Avoid „бенчмарк" if possible |
| Benchmark game | Еталонна игра | |
| Testbed | Тестова среда | |
| Validation | Валидация / Проверка | „Проверка" is more native |
| Cross-validation | Кръстосана проверка | |
| Learning curve | Крива на обучение | |
| Hyperparameter | Хиперпараметър | Foreign root, but established |
| Failure mode | Режим на отказ | |
| Domain-agnostic | Независим от предметната област | |
| Robustness | Устойчивост | |
| Adaptability | Адаптивност | |

---

## 6. Common Academic Phrases

| English | Bulgarian |
|---------|----------|
| The primary objective of this research is | Основната цел на настоящото изследване е |
| It is demonstrated that | Демонстрирано е, че |
| The proposed method | Предложеният метод |
| In the context of | В контекста на |
| As shown in Section N | Както е показано в раздел N |
| The results indicate | Резултатите показват |
| Contribution N addresses | Принос N е насочен към |
| The following phase covers | Следващият етап обхваща |
| The study plan is organized as | Планът за обучение е организиран като |
| Under conditions of imperfect information | При условия на непълна информация |
| A strategy profile in which | Стратегически профил, при който |
| Without loss of generality | Без загуба на общност |
| It follows that | Следва, че |
| Extends existing results from | Разширява съществуващи резултати от |
| Empirical validation | Емпирична проверка |

---

## 7. Translation Guidelines

1. **First-mention rule.** When a term appears for the first time, write the Bulgarian translation followed by the English term in parentheses: „Минимизиране на контрафактуалното съжаление (Counterfactual Regret Minimization, CFR)". All subsequent uses: either the Bulgarian form or the abbreviation alone.

2. **Algorithm abbreviations.** Always in Latin script: CFR, DQN, PPO, MCCFR, MARL, etc. Never transliterate abbreviations into Cyrillic.

3. **Formulas and notation.** Keep all mathematical notation in Latin/Greek as in the English original. Variable names ($T$, $V$, $Q$, $\sigma$) are not translated.

4. **Anglicisms to avoid.** Prefer native or established Slavic-origin alternatives where they exist (see individual entries above). When no good Bulgarian equivalent exists (e.g., „контрафактуален"), use the borrowed term with a brief gloss on first occurrence.

5. **Register.** Maintain formal academic tone throughout: passive constructions, third person, impersonal sentences. Avoid colloquialisms, contractions, or unnecessarily informal phrasing.

6. **Citation format.** Author surnames are kept in Latin script. Titles of works may be given in the original language (English) since no standard Bulgarian translation exists for most.

7. **Titles of parts of a foreign-language source are not translated.** A reference to
   „Sutton & Barto (2018), *Reinforcement Learning: An Introduction*, Chapter 3 — Finite
   Markov Decision Processes" keeps the book title *and* the chapter title in English. Only
   the surrounding prose is Bulgarian. A reader who follows the reference needs the words
   that are actually printed in the book.
