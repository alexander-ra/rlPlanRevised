# Glossary decisions — for the candidate

Merged from 146 glossary-level findings (F01-T … F12-T) of the September 2026 final review.
Each row is one decision that applies to **every** chapter, the one-pagers, the reports and
the figure labels, and to both glossaries (`deliverables/terminology_EN_BG.md` and the
settled `llmPipeline/glossary_settled.md`, via the picker).

**⟲** marks a recommendation that changes an entry *you* chose in the curated
`terminology_EN_BG.md` — check those first.

**Candidate picks (2026-09-25):** the seven formerly open rows are resolved below.
Apply them to every Bulgarian chapter, report, one-pager, figure label and glossary.
Chapter 15's Bulgarian prose will be translated later using these picks.

Convention kept from the brief: algorithm and system names stay in Latin script (CFR, PPO,
Libratus, Decision Transformer …); cited authors stay in Latin script in prose, while
established game and concept names remain Bulgarian (Наш, Кун, Шапли).
On first use in each chapter, a Bulgarian term is followed by the English in parentheses.

## 0. Pipeline rules (not single terms)

| # | Problem | Decision |
|---|---|---|
| 0.1 | Verbs stored in 1st-person dictionary form ("рандомизирам", "оптимално отговарям") are pasted into prose | ✅ store verbs as nouns/neutral phrases ("най-добър отговор", "избира на случаен принцип"); never insert a 1st-person form |
| 0.2 | ~25 entries whose "Bulgarian" side is English (TD error, Kuhn's Theorem, Machine Zero, Full-Traversal CFR, EGTA Meta-Game, Coalition-Aware MAPPO, No-Limit Texas Холдем …) | ✅ translate all; only acronyms/system names stay Latin |
| 0.3 | Entries with a Latin letter inside Cyrillic ("n-играчeн", "типoв") | ✅ fix; they break search and hyphenation |
| 0.4 | The non-word "сходява/сходяват" (≈15× in 9 chapters) | ✅ "клони към" / "се сближава с" / "достига", by context |
| 0.5 | Pipeline bolded glossary terms the EN does not bold | ✅ remove extra bold (applied mechanically) |
| 0.6 | Title-case values ("Сходява", "Усреднено време") print capitalised mid-sentence | ✅ lower-case all values |

## 1. Core game theory and the thesis's own vocabulary

| # | English | Now | Recommended | Decision |
|---|---|---|---|---|
| 1.1 | two-player | двуигрови (= "two-game"; ≈30× in 6 chapters) | за двама играчи ("игра за двама с нулева сума") | ✅ |
| 1.2 | N-player / n-player | N-игрова среда, N-играторска, n-играчeн | с N играчи | ✅ |
| 1.3 | multiplayer | многопотребителски (= multi-user), мултиплейър | с много играчи | ✅ |
| 1.4 | safety–exploitation spectrum | безопасност–изследване (= exploration) | безопасност–експлоатация | ✅ |
| 1.5 | safe exploitation | also "безопасно използване" | безопасна експлоатация (only) | ✅ |
| 1.6 | exploiter | експлоатьор, експлоатер, експлойтър | експлоататор | ✅ |
| 1.7 | Nash (opponent type) vs Nash (concept) | "наш противник" (= "our opponent"), Нашево, Нашов | type in quotes: „Наш“; concept: равновесие на Наш; Nash EV → очаквана стойност при равновесие на Наш | ✅ |
| 1.8 | Restricted Nash Response | curated "Ограничен Наш отговор" (= "our response") | ограничен отговор по Наш (RNR) | ✅ ⟲ changes your curated entry (curated: Ограничен Наш отговор) |
| 1.9 | SES (curated expansion) | Safe Exploitation *Subgame* | Safe Exploitation *Search* — търсене на безопасна експлоатация (Liu et al. 2022) | ✅ ⟲ changes your curated entry (curated: Safe Exploitation Subgame) |
| 1.10 | blueprint | curated "Схема"; corpus "план" (≈130×); settled "план-стратегия" | **план (blueprint)** | ✅ candidate pick |
| 1.11 | counterfactual | curated "контрафактуален"; corpus "контрафактичен" (≈45× vs 2) | контрафактичен — change the curated file, not the text | ✅ ⟲ changes your curated entry (curated: контрафактуален) |
| 1.12 | consistent / consistency (statistical, Ganzfried 2025) | съгласуван | състоятелен / състоятелност (as in "състоятелна оценка"); keep "съгласуван" only for "consistent with the observations" | ✅ ⟲ changes your curated entry (curated: Консистентно) |
| 1.13 | intractable / tractable | неразрешим (= undecidable) | изчислително непосилен / ефективно изчислим | ✅ |
| 1.14 | worst-case value | най-лошият стойностен случай | стойност в най-лошия случай | ✅ |
| 1.15 | in expectation | в очакване (= "while waiting") | средно (по математическо очакване) | ✅ |
| 1.16 | sound / soundness | звуково, правилно, надежден, коректен | коректен / коректност | ✅ |
| 1.17 | opponent-blind(ness) | невидимост за противника (inverted) | „сляп“ за противника / „слепота“ за противника | ✅ |
| 1.18 | oracle (best-response oracle, double oracle) | предсказвач — your curated choice | **предсказвач** | ✅ candidate pick |
| 1.19 | bang-bang | изненадващ обрат (= "a surprising twist") | скокообразно превключване; threshold → праг на превключване | ✅ |
| 1.20 | gadget (subgame solving) | джаджа | приспособление (gadget) | ✅ |
| 1.21 | cutting-plane / cut | равнина на отсичане; cut → сечение/срез/разрез | отсичаща равнина; метод на отсичащите равнини; cut → отсичащо ограничение | ✅ |
| 1.22 | continuation strategy / continual re-solving | продължителна (= long-lasting) | стратегия за продължение; непрекъснато пререшаване | ✅ |
| 1.23 | leaf (of the tree) | възел | листо; leaf evaluator → оценител на листата | ✅ |
| 1.24 | public belief state | общодостъпно състояние на вярванията | публично състояние на убежденията (PBS) | ✅ |
| 1.25 | rest point (dynamics) | равновесна точка (clashes with Nash) | точка на покой | ✅ |
| 1.26 | wheel of counters / counters | колело от броячи, коалиционни жетони | кръг от контрастратегии; counters → контрастратегии | ✅ |
| 1.27 | reconciliation (prediction vs result boxes) | съгласуване | съпоставка (прогноза → резултат) | ✅ |
| 1.28 | Shapley value / credit | Шейпли, Shapley, "коалиционен кредит" | стойност на Шапли; credit → принос (по Шапли) | ✅ |
| 1.29 | Matching Pennies | „хвърляне на монета“ (a chance event) | „съвпадение на монети“ (Matching Pennies) | ✅ |
| 1.30 | defect / cooperate (PD) | дефект (= a flaw) | предателство (verb предава); сътрудничество | ✅ |
| 1.31 | spinning top (curated note) | attributed to Balduzzi 2019 | decomposition: Balduzzi et al. 2018/2019; "spinning top": Czarnecki et al. 2020 | ✅ |

## 2. Reinforcement learning and statistics

| # | English | Now | Recommended | Decision |
|---|---|---|---|---|
| 2.1 | policy | mixed "политика"/"стратегия" (curated says стратегия) | стратегия everywhere (policy iteration → итерация по стратегии) | ✅ |
| 2.2 | on-policy / off-policy | политика на работа; извънполитикова | по текущата стратегия (on-policy); извън текущата стратегия (off-policy) | ✅ |
| 2.3 | self-play (freq 43, 7 chapters) | самообучение (= self-study; "обучение чрез самообучение") | **игра срещу себе си** | ✅ candidate pick |
| 2.4 | independent learning | самостоятелно обучение (= self-study) | независимо обучение | ✅ |
| 2.5 | bootstrapping | самоподкрепяне, буутстрапинг, „bootstrap“ | **самоподкрепяне (bootstrapping)** on first use in each chapter | ✅ candidate pick; statistical bootstrap resampling is separate |
| 2.6 | converge / convergent | Сходява (non-word) | клони към / се сближава с; сходящ; convergence → сходимост | ✅ |
| 2.7 | prior / posterior / likelihood | предварително убеждение / задно (= "rear") / вероятност | априорно разпределение / апостериорно разпределение / правдоподобие; conjugate prior → спрегнато априорно разпределение | ✅ |
| 2.8 | variance / unbiased | also вариация / непредубеден | дисперсия / неизместен | ✅ |
| 2.9 | bias (statistical) / bias vector | пристрастие (= prejudice) | отместване; вектор на отместванията (keep "индуктивно пристрастие" for inductive bias) | ✅ |
| 2.10 | divergence (of an iteration/trajectory) | разминаване (= a mismatch) | разходимост / отдалечаване (от равновесието); KL stays "дивергенция" | ✅ |
| 2.11 | KL divergence / KL-regularized | разминаване на Кълбек-Лайблер; КЛ | дивергенция на Кулбак–Лайблер (KL); с KL-регуларизация | ✅ |
| 2.12 | mode | мода (fashion) for everything | мода (of a distribution only); режим / вид (operating mode, credit mode) | ✅ |
| 2.13 | time-average | Усреднено време (= "averaged time") | средно по времето | ✅ |
| 2.14 | sample efficiency / sample-efficient | ефективност на извадката; ефективен по отношение на пробите | ефективност по отношение на данните (sample efficiency) | ✅ |
| 2.15 | wall-clock time / budget | реално време (clashes with C1's "real-time") | време за изпълнение; бюджет от време за изпълнение | ✅ ⟲ changes your curated entry (curated: Бюджет в реално време) |
| 2.16 | compute (cost) | изчислителна мощност (= hardware) | изчислителни разходи; test-time compute → изчисления по време на изпълнение | ✅ |
| 2.17 | inference (running a model), test-time | извод; време на тестване; тест-тайм | по време на изпълнение / по време на игра | ✅ |
| 2.18 | offline | извън линия (calque) | офлайн / предварително | ✅ |
| 2.19 | sparse reward | оскъдна награда (= meagre) | рядка награда; sparse agents → агенти с рядка награда | ✅ |
| 2.20 | critic (actor-critic) | "критична стойност" (= statistical critical value) | оценител (your curated term, "актьор-оценител"); critic-value proxy → заместител от оценките на оценителя | ✅ |
| 2.21 | return conditioning | условно връщане (= conditional refund) | обуславяне по възвръщаемостта | ✅ |
| 2.22 | return-to-go | очаквана възвръщаемост до края (wrong: it is realised) | остатъчна възвръщаемост | ✅ |
| 2.23 | sequence models | последователни модели (= consistent/successive) | модели на последователности | ✅ |
| 2.24 | Decision Transformer / ARDT | трансформатор (electrical) / трансформър … | keep Latin names; first-use gloss "трансформър за вземане на решения" | ✅ |
| 2.25 | overfitting / underfitting | пренастройване / недообучен | преобучение / недообучение | ✅ |
| 2.26 | convolution | сгъвка (= a fold) | конволюция; конволюционен | ✅ |
| 2.27 | permutation-equivariant / -invariant | инвариантен (wrong for equivariant) | еквивариантен / инвариантен спрямо пермутации | ✅ |
| 2.28 | grid / gridworld (no entry) | мрежа (clashes with neural network) | решетка; решетъчна среда | ✅ |
| 2.29 | proximal policy optimization (gloss) | оптимизация на проксималната стратегия | оптимизация на стратегията с ограничение на близостта (PPO) | ✅ |
| 2.30 | generalized advantage estimation | обобщено изчисляване на предимството | обобщена оценка на предимството (GAE) | ✅ |
| 2.31 | custom (own implementation) | персонализиран | собствена реализация / собствен | ✅ |
| 2.32 | Markov property | марковска свойственост | марковско свойство | ✅ |
| 2.33 | regret flooring | подово ограничаване на съжалението | нулиране на отрицателните съжаления | ✅ |
| 2.34 | linear averaging / running average | усредняване на линейни стратегии; плъзгаща средна | линейно претеглено усредняване; текуща средна | ✅ |
| 2.35 | smoke / scale runs | smoke/scale, "дим", пробно изпълнение | бърза проверка / пълен мащаб | ✅ |
| 2.36 | sweep / paired sweep | обхождане (= traversal); петкратно кръстосано | серия експерименти; сдвоени сравнения с 5 начални числа | ✅ |
| 2.37 | undersampling | подбиране на ограничена извадка | недостиг на наблюдения | ✅ |
| 2.38 | seed | семена (in places) | начално число | ✅ |
| 2.39 | projected gradient / convex program | проектиран (= designed); програмираща задача | градиентен метод с проекция; задача на изпъкналата оптимизация | ✅ |
| 2.40 | lossy / recall (abstraction) | загубен (= lost); извличане | със загуби; памет (perfect/imperfect recall → пълна/непълна памет) | ✅ |
| 2.41 | exploitability gap | експлоатируема разлика / пропуск в експлоатируемостта | разлика в експлоатируемостта | ✅ |
| 2.42 | action translation / pseudo-harmonic mapping | превод; отображение | транслация на действия; псевдохармонично преобразуване | ✅ |
| 2.43 | churn | загуба на памет | непрекъсната смяна (на стратегиите) | ✅ |
| 2.44 | gap closed (metric) | разликата е намалена | затворена част от разликата | ✅ |
| 2.45 | tie-break / deadlock | развръзка (= plot dénouement); задънена улица | правило при равенство; пат | ✅ |
| 2.46 | planted coalition | засадена (like a tree) | предварително зададена коалиция | ✅ |
| 2.47 | random floor | случаен минимум | нивото на случайната игра | ✅ |
| 2.48 | toy games / toy scale | игри-играчки; игрови мащаб | опростени (учебни) игри; мащаб на опростен модел | ✅ |

## 3. Poker vocabulary

| # | English | Now | Recommended | Decision |
|---|---|---|---|---|
| 3.1 | bet / call / raise / fold / check | залог / **залог** / вдига / **пас** / проверка | залог / плащане (плаща) / вдигане / отказ (се отказва) / чек | ✅ |
| 3.2 | pass (Kuhn's action p) | пас | пас (kept — this is why fold must not be "пас") | ✅ |
| 3.3 | suit / suit isomorphism | curated "цвят", corpus "боя" | боя; изоморфизъм на боите (change the curated file) | ✅ ⟲ changes your curated entry (curated: цвят) |
| 3.4 | turn / river / street | ход / река / улица | търн / ривър / рунд на залагане | ✅ |
| 3.5 | board / board texture / high board | дъска, маса, текстура на дъската | общи карти; състав на общите карти; висока обща карта | ✅ |
| 3.6 | hand (cards held) vs hand (one deal played) | mixed | ръка (cards held); раздаване (a deal played, "на раздаване") | ✅ |
| 3.7 | hero | герой | собственият агент | ✅ |
| 3.8 | leak (in one's play) | изтичане | уязвимост / слабост | ✅ |
| 3.9 | win rate (poker, chips per hand) | процент победи | темп на печалба (keep "процент победи" for a share of games won) | ✅ |
| 3.10 | mbb/g | мили-големи блайнда на игра | хилядни от големия блайнд на раздаване (mbb/g) | ✅ |
| 3.11 | HUNL / HULHE / no-limit | 5+ variants incl. "но-лимит", "по̀кер" | безлимитен тексаски холдем за двама играчи (HUNL); лимитен … (HULHE); no-limit → безлимитен | ✅ |
| 3.12 | chips | фиш / жетони | жетони | ✅ |
| 3.13 | read (on an opponent) | прочитане, прочит, прочетеното | преценка за противника | ✅ |
| 3.14 | Kuhn / Leduc | mixed | Кун покер / Ледюк Холдем (as the brief) | ✅ |

## 4. Names kept in Latin script (identity entries)

Student of Games, Player of Games, Liar's Dice, Reconnaissance Blind Chess, Decision
Transformer, ARDT, Libratus, DeepStack (not "deepStack"), Pluribus, ReBeL, AlphaStar,
OpenSpiel — the glossary and the figure mapping must stop translating them
("Студент по Игри", "Лъжливи зарове", "слепец шах с разузнаване").

## 5. Typography and bundle policy

| # | Item | Decision |
|---|---|---|
| 5.1 | Hyphen used as a dash (" - "), ~1,500× across the BG corpus | ✅ en dash " – " with a non-breaking space before it, applied in the build (outside math, code and negative numbers) |
| 5.2 | Decimal point, "20,000", "x" in BG text | ✅ decimal comma (0,571; `0{,}571` in math), "20 000", "×" — matches the BG figures |
| 5.3 | Works cited in several chapters share one footnote number in the single-document bundle (note prints only in the first chapter) | ✅ repeat the note in each chapter that cites the work |
| 5.4 | Cross-references "Раздел 5" inside chapter 7 | ✅ "раздел 7.5" |

## 6. New terms from chapters 13–15

Applied in the Bulgarian chapters 13–14 as listed; use the same choices when Chapter 15
is translated. ✅ unless you change them.

| # | English | Chosen | Note |
|---|---|---|---|
| 6.1 | behavioural cloning | поведенческо клониране | as chapter 12 and the curated glossary |
| 6.2 | embedding | вграждане | as chapter 5 and the glossary |
| 6.3 | collusion / colluders | тайно съглашение / съучастници | as the curated glossary and rawStepsBg |
| 6.4 | soft play / chip dumping | пасивна игра (срещу съучастника) / прехвърляне на жетони | |
| 6.5 | light / strong collusion | съглашение с ниска / висока интензивност | |
| 6.6 | bot detection | откриване на ботове | |
| 6.7 | unsupervised / self-supervised | без учител / научено без етикети | |
| 6.8 | false-positive rate / recall / AUC | дял на фалшиво положителните резултати (FPR) / пълнота / AUC | |
| 6.9 | VPIP, PFR, 3-bet, c-bet, WTSD, HUD | Latin, Bulgarian description on first use | |
| 6.10 | c-bet / limp / steal / post / donk bet | продължаващ залог / влизане с плащане / кражба на блайндовете / вноска / „донк“ залог | |
| 6.11 | heads-up / hole cards / showdown | сблъсък един срещу друг / скрити карти / разкриване на картите | |
| 6.12 | regulars / hand history | редовни играчи / история на раздаванията | |
| 6.13 | TAG / LAG / nit / fish | стегнато- / разпуснато-агресивен; „нит“ / „риба“ | ✅ **стегнато-пасивен / разпуснато-агресивен** (connecting -о throughout) |
| 6.14 | re-identification / multi-accounting | повторно разпознаване / множество акаунти | |
| 6.15 | majority baseline / split-half / minimum sample | мажоритарна базова линия / корелация между половините / минимална извадка | |
| 6.16 | archetype / parser | архетип / парсер | |
| 6.17 | gain / capture / exposure / confidence | приръст / реализиран дял / експозиция / статистическа увереност | chapter 14 |
| 6.18 | teaching attack / teach loss | обучаваща атака (curated) / загуба от обучаващата атака | |
| 6.19 | coalition value (exposure vs a pair) | стойност срещу коалиция | kept apart from chapter 11's „стойност на коалицията“ = v(S) |
| 6.20 | estimator / policy-exact / control variate | оценка / точна по стратегиите / контролна променлива | "оценител" stays reserved for the critic (2.20) |
| 6.21 | Nash averaging / maximal lotteries / round robin / selection pressure | усредняване по Наш / максимални лотарии / кръгов турнир / селекционен натиск | α-Rank, VasE, AIVAT, h50/r50, RRPS stay Latin with a gloss |
| 6.22 | population return / within-population exploitability | възвръщаемост срещу популацията / експлоатируемост в рамките на популацията | |
| 6.23 | zoo / duplicate / bootstrap resampling | зоопарк от агенти / дублирани карти / повторни извадки с връщане | the last kept apart from row 2.5 |
| 6.24 | cited authors in running text | ✅ Keep Latin spellings in Bulgarian prose (e.g. Ganzfried и Sandholm); established game and concept names remain Bulgarian. | |
| 6.25 | bot/agent names (AlwaysPass, Rock, Maniac, Random) | ✅ Keep code and figure names in Latin script in Bulgarian prose. | |
| 6.26 | bank (RWYWE's k) / gift / credit (accounting) | резерв / подарък / зачита, зачетена стойност | chapter 15 — to confirm; „банка“ avoided |
| 6.27 | floor / maximin floor / team-maxmin value | праг / максиминен праг / отборна максиминна стойност (team-maxmin) | as chapters 8 and 14 |
| 6.28 | capped mixture / cap | смес с таван / таван | chapter 15 — to confirm |
| 6.29 | KL anchor / KL anchoring | KL-котва / закотвяне чрез KL | chapter 15 — to confirm |
| 6.30 | match-level safety S | безопасност на ниво мач | chapter 15 — to confirm |
| 6.31 | frontier map / design documents / publication pipeline | карта на изследователската граница / проектни документи / публикационен план | as the study plan and the curated glossary |
| 6.32 | (feasibility) pilot | пилотен експеримент (за осъществимост) | chapter 15 — to confirm |
| 6.33 | opponent inference / calibrated confidence | извеждане на стратегията на противника / калибрирана увереност | "извеждане" as in chapter 1; chapter 15 — to confirm |
| 6.34 | showdown-only accounting / cards shown (RWYWE variants) | отчитане само при разкриване на картите / открити карти; labels „RWYWE (разкриване)“, „RWYWE (открити карти)“ | chapter 15 — to confirm |
| 6.35 | colluding pair / colluding opponents | двойка съучастници / противници в тайно съглашение | follows 6.3 |
| 6.36 | stretch option (venue) | амбициозен вариант | chapter 15 — to confirm |
| 6.37 | RQ1–RQ3 | kept Latin after „изследователските въпроси“ | chapter 15 — to confirm |
