# Step 06 (second half: ReBeL, Student of Games, Synthesis) — final review

**Summary:** The ReBeL / SoG / Synthesis half of Chapter 6 is technically well researched: nearly every number checks out against the primary papers (ReBeL Table 1 and Appendix E, SoG Table 1–2, Theorems 1–2, Pluribus and Libratus data statements). Four things matter most. (1) **The BG text prints broken and English passages**: two sentences are corrupted by the math masking of the translation pipeline ("$ pairs the public state … with a **range** $", "($) and search deepens ($) … (⟦MATHI10⟧)", printed on pp. 118 and 120), the SoG heading "The gap it closed" is English, "Recursive Belief-based Learning" replaces "ReBeL" 19 times, and English fragments ("CFR solving", "pBS value мрежа", "alphaZero loop", "CFR policy", "Huber loss", "CFR family") sit in the prose. (2) **Glossary entries produce meaning errors** that recur: "звуково търсене" (sound = acoustic), "многопотребителски" (multiplayer = multi-user), "многопроцесорно поле" (multi-pro field), "невидимост за противника" (opponent-blindness, inverted), "в очакване" (in expectation = while waiting), "предходна стратегия" (prior policy), "начално число" for a metaphorical seed, "двуигрови", "полицийно насочено". (3) **All four figures fail at print size** (labels 3.2–6.6 pt against 10.9 pt body text), carry English, "Студент по Игри", overlapping labels and first-person verbs; fig. 30 marks AIVAT, continual re-solving, depth-limited solving and safe search in the wrong columns. (4) **Sourcing:** the chapter never cites the ReBeL paper at all; apart from one [^sog] marker, the only footnote markers in these sections are misplaced ([^lbr] on an unverified "holy grail" quote, [^brown2017] and [^pluribus] on SoG sentences, a repeated [^deepstack]), so 12 of the 13 SOURCE_GAPS rows in these sections get a verified citation (S02–S14; one needs none). The SoG exploitability bound has *A* where the paper has √*A*, "mid-training AlphaZero" is wrong, "first provably sound across both classes" overclaims, and the hand-off still points to Chapters 7–15 and Phases D–G.
Corpus-wide items, not reported per occurrence: 195 hyphens used as dashes, 12 decimal points and 4 "20,000"-style thousands separators, 193 bold spans against 120 in the EN (the pipeline added about 73), and two footnote markers whose notes print in other chapters (F07-X01: marker 38 on p. 118 → note on p. 79; marker 25 on p. 123 → note on p. 41).
**Counts:** S1 35 · S2 66 · S3 9   (by category: G 6 · B 54 · T 14 · C 14 · S 20 · X 2)

Conventions in this file: quotes are **raw markdown** (EN quotes join the source's hard line breaks with a single space) from `summaryBg.md` (lines 299–564) / `summaryEn.md` (lines 810–1575), including `**`, `*`, `$`, so read this file as source, not rendered. Proposals keep the chapter's " - " dashes and decimal points; those are fixed centrally (F07-B41, F07-B42). Page numbers are PDF page numbers of `deliverables/bundles/allSummaries_bg.pdf` (the printed folio is one lower). Printed type sizes = matplotlib size × (printed width ÷ saved width), from `renders/manifest.json`; the floor is ≈ 8.2 pt. B05 is a replace-all: apply it **after** the other fixes, because several quotes below still contain "Recursive Belief-based Learning". New footnote labels proposed here (`brown2020rebel`, `bakhtin2020`, `brown2018dls`, `kilcher2022`, `cicero2022`) are not used anywhere else in the corpus (checked with grep).

## G — Figures

### F06b-G01 · S1 · Bulgarian captions for figs. 27–30
- **Where:** summaryBg.md image alt text, lines 339, 436, 518, 524 (bundle pp. 108, 117, 126, 127). All four print in English (known corpus-wide defect). The fig. 30 alt text also says "Step 3–5", while the EN alt text says "Chapters 3–5".
- **Now → Proposed:**
  - "![ReBeL's AlphaZero-style loop: self-play training (left) and test-time play (right) share one PBS value/policy network, both solving depth-limited subgames rooted at the public belief state (shared definition box, bottom).]" → "![Цикълът на ReBeL в стил AlphaZero: обучението чрез самоигра (вляво) и играта при тестване (вдясно) използват една и съща мрежа за стойности и стратегия върху PBS; и в двата случая се решават под-игри с ограничена дълбочина и корен в публичното състояние на убежденията (общото определение е в полето долу).]"
  - "![Student of Games: the GT-CFR search loop (left) and the sound self-play training loop that feeds it (right) share one CVPN; the footer strip names the unification across perfect- and imperfect-information games.]" → "![Student of Games: цикълът на търсене GT-CFR (вляво) и цикълът на обучение чрез коректна самоигра, който го захранва (вдясно), използват една и съща CVPN; долната лента обобщава обединяването на игрите с пълна и с непълна информация.]"
  - "![The seven-year arc as trade-offs: the five systems placed along three axes (abstraction → neural; offline → real-time search; imperfect-only → unified), with lineage arrows and a per-system capability-gained/given-up tag.]" → "![Седемгодишното развитие като поредица от компромиси: петте системи по три оси (абстракция → невронни мрежи; предварително изчисление → търсене в реално време; само непълна информация → обединение), със стрелки на наследяване и бележка за спечеленото и изгубеното от всяка система.]"
  - "![Component-reuse map: Step 3–5 building blocks and chapter-native primitives (rows) against the five systems in chronological order (columns); stars mark the system that introduced each native primitive, connected by a staircase of first appearances.]" → "![Карта на повторно използваните компоненти: градивните елементи от глави 3–5 и примитивите, въведени в тази глава (редове), срещу петте системи в хронологичен ред (колони); звездите отбелязват системата, въвела съответния примитив, а пунктирната „стълба“ свързва първите им появи.]"
- **Fix:** replace the alt text in `summaryBg.md`; the `](file.png)` part stays.

### F06b-G02 · S1 · Fig. 27 ReBeL loop: English definition box, overlapping text, imperatives and first person, prints at 4.4–6.6 pt
- **Where:** `renders/ch06/p108_f1.png` — caption "ReBeL's AlphaZero-style loop: …"; script `deliverables/reports/step06/summary/make_rebel_figure.py`.
- **Problem:**
  1. English in the BG figure: the whole bottom box "Public belief state (PBS) β = a probability distribution over each player's possible hidden states (in HUNL, both players' 1,326 possible two-card hands) …" (the mapping entry is `null`), and "Мрежа за PBS value (+ стратегия)".
  2. Overlaps: the two panel titles run into each other ("…(в стил AlphaZ**ТЕС**Т / ИГРА…"); the text of left box ④ "Генерирай данни…" runs across the gap into right box ③ and the two texts print on top of each other; boxes ②, ④, ⑤ (left) and ②, ③ (right) overflow their borders.
  3. Mood and person: imperatives "Конструирай", "Реши я", "Генерирай", "Избери", "Започни", "Изпълни", "Действай"; first person "преобучавам мрежите, след това повтарям целия цикъл", "добавям точно този залог … и преизчислявам" (F07-T03).
  4. "Изпълни CFR с мрежата за стойности във възлите" — *leaf* is "листо", not "възел" (T09); "Текущ PBS" but "кореново PBS" in the text (PBS = състояние, neuter).
  5. Legibility: saved 3175 px at 330 dpi (9.62 in), printed 16.9 cm → scale 0.69. Panel titles 9.6 → 6.6 pt; boxes 7.8–9.5 → 5.4–6.6 pt; notes 6.3–7.4 → 4.4–5.1 pt; definition box 8.2 → 5.7 pt.
- **Fix:** `make_rebel_figure.py`: `new_fig(w=17.4, h=11.6, …, shrink=2.2)` (scale ≈ 0.85 at 16.9 cm); all `box` fs → 10, `note` fs → 9.6, `panel_bg` label_fs → 10 with each title on two lines; heights of L2, L4, R3 +0.4. Mapping (`figure_labels.json`), new key for the definition box: → "Публично състояние на убежденията (PBS) β – вероятностно разпределение върху възможните\nскрити състояния на всеки играч (в HUNL – 1326-те двойки карти на всеки от двамата)\nпри дадена публична история; обновява се по Бейс след всяко публично действие."; 'PBS value (+ policy) network\nf(β) → infostate values, policy' → 'Мрежа за стойности (+ стратегия) върху PBS\nf(β) → стойности на инф. състояния, стратегия'; 'TRAINING: self-play RL + search (AlphaZero-style)' → 'ОБУЧЕНИЕ: самоигра с RL + търсене\n(в стил AlphaZero)'; 'TEST / PLAY: the same search' → 'ТЕСТ / ИГРА:\nсъщото търсене'; '① Current PBS β' → '① Текущо PBS β'; '② Construct a depth-limited subgame rooted at β\n(fixed depth: end of the current betting round)' → '② Под-игра с ограничена дълбочина и корен β\n(до края на текущия рунд залагания)'; '③ Solve it with CFR' → '③ Решаване с CFR'; '④ Emit training data: …' → '④ Данни за обучение: (β, средни стойности\nна инф. състояния) → за мрежата за стойности;\n(β, средна стратегия) → за мрежата за стратегия'; '⑤ Sample a leaf PBS on a random CFR iteration' → '⑤ Избор на листо PBS от случайна\nитерация на CFR'; '① Root a subgame at the current PBS' → '① Под-игра с корен в текущото PBS'; '② Run CFR with the value net at the leaves' → '② CFR с мрежата за стойности в листата'; '③ Pick the policy of a random CFR iteration —…' → '③ Стратегия от случайна итерация на CFR –\nтова прави търсенето при тестване доказуемо\nбезопасно, без допълнителни ограничения'; '④ Act' → '④ Действие'; 'retrain nets,\nthen repeat\nthe whole loop' → 'мрежите се преобучават\nи целият цикъл\nсе повтаря'; 'opponent bets off-tree →\nadd that exact bet to the\nsubgame and re-solve' → 'залог на противника извън дървото →\nзалогът се добавя към под-играта\nи тя се решава отново'; 'leaf value = v̂(infostate | beliefs\nat the leaf this iteration)' → 'стойност в листото = v̂(инф. състояние |\nубеждения в листото при тази итерация)'; 'values are well-defined on a PBS — unlike on a public state alone' → 'върху PBS стойностите са добре дефинирани – за разлика от само публичното състояние'.

### F06b-G03 · S1 · Fig. 28 SoG loop: overlapping titles, stray dots and arrow over text, English, first person, 4.7–6.9 pt
- **Where:** `renders/ch06/p117_f1.png` — caption "Student of Games: the GT-CFR search loop …"; script `make_sog_figure.py`.
- **Problem:**
  1. The two panel titles overlap ("…решаване на д**Самоо**бучение (training)"); both are single long lines.
  2. Nine random pink dots (`ax.scatter(px, py …)`, seed 7) print on top of the text of the "Събиране на данни…" box, in EN too; the dark-green "push new net" arrow runs diagonally through all four right-hand boxes; the mini-tree callout's grey branch touches the footer box.
  3. English: "(training)", "Huber loss", "кръстосана-\nentropy".
  4. First person: "изпълнявам CFR⁺", "правя заявка", "Обучавам CVPN", "изпращам новата мрежа", "изпращам нова мрежа"; imperative "Играй игра със самообучение".
  5. Meaning: "предходна стратегия" for *prior policy* (T08); "актьорите" for *actors* (B20); the regret-update box says "CFR⁺ върху публичното дърво\nна текущото дърво" (tree twice).
  6. Legibility: 3054 px at 330 dpi (9.25 in), printed 16.9 cm → scale 0.72. Titles 9.0–9.6 → 6.5–6.9 pt; boxes 7.5–8.2 → 5.4–5.9 pt; notes 6.6–7.3 → 4.7–5.2 pt; footer 9.2 → 6.6 pt.
- **Fix:** `make_sog_figure.py`: delete the three lines that build and draw `px`, `py` (`ax.scatter(...)`); route the push arrow outside the panel: `arrow(ax, rc(S4), (16.4, S4[1] + S4[3]/2), style="-", color="#1f4a1f", lw=1.7)`, `arrow(ax, (16.4, S4[1] + S4[3]/2), (16.4, 11.7), style="-", color="#1f4a1f", lw=1.7)`, `arrow(ax, (16.4, 11.7), rc(net), color="#1f4a1f", lw=1.7)` instead of the `rad=0.15` arrow; mini-tree `ty` 3.6 → 4.2; `new_fig(…, shrink=2.2)`; all box fs → 10, notes → 9.6; titles on two lines. Mapping: 'GT-CFR SEARCH (one decision): grow the tree, solve the tree' → 'ТЪРСЕНЕ GT-CFR (едно решение):\nрастеж и решаване на дървото'; 'SOUND SELF-PLAY (training)' → 'КОРЕКТНА САМОИГРА\n(обучение)'; "CVPN: f(β) → …" → 'CVPN: f(β) → (контрафактични\nстойности v, априорна стратегия p)\nβ = (публично състояние, убеждения r\nза инф. състояния на всеки играч)'; 'Regret-update phase: …' → 'Фаза на обновяване на съжалението:\nCFR⁺ върху текущото публично дърво;\nстойностите в листата идват от CVPN'; 'Expansion phase: …' → 'Фаза на разширяване: траектория по PUCT,\nкоято смесва научената априорна стратегия\nс текущата стратегия на CFR (½π_PUCT + ½π_CFR);\nпървото ново публично състояние се добавя'; 'Play a self-play game, …' → 'Игра срещу себе си с търсене\nGT-CFR при всяко решение'; 'Collect data: …' → 'Събиране на данни: пълни траектории\n(цели за стратегията и изхода) и всички\nсъстояния, при които е запитана CVPN („заявки“)'; 'Solve the queries …' → 'Заявките се решават с друго (рекурсивно)\nтърсене GT-CFR → цели за контрафактичните\nстойности (възможни са нови подзаявки)'; 'Train the CVPN (Huber loss …' → 'Обучение на CVPN (загуба на Хюбер за стойностите,\nкръстосана ентропия за стратегията) от буфер;\nновата мрежа периодично се изпраща на изпълнителите'; 'push new\nnet' → 'нова\nмрежа'; 'perfect-information games (k = 1, AlphaZero-like regime)' → 'игри с пълна информация (k = 1, режим като при AlphaZero)'.

### F06b-G04 · S1 · Fig. 29 evolution arc: "Студент по Игри", English lane label, colliding tags, overflowing footer shrinks the whole figure to 3.2–4.1 pt
- **Where:** `renders/ch06/p126_f1.png` — caption "The seven-year arc as trade-offs…"; script `make_evolution_figure.py`.
- **Problem:**
  1. System name translated: "Студент по Игри" (mapping 'Student of\nGames' → 'Студент по\nИгри'). Names stay in Latin script (brief rule 2; cf. the candidate's comment on p. 5 of the Aug build: "нека да запазим оригиналното име на Libratus").
  2. English: lane label "imperfect-only ↔ unified" (mapping `null`).
  3. Overlaps: the five +/– tags sit on two rows and collide ("…експлоа**тира**уемост", "…решава**не**–без гаранция…", "+ точен отговор в реално вре**ме**…възстановява"); in the BG render the footer is a single line far wider than its box.
  4. Because the footer text extends beyond the axes, the tight bounding box grows from 3544 px (EN) to 4604 px (13.95 in) and the figure prints at scale 0.485: names 8.4 → 4.1 pt, lane labels 8.2 → 4.0 pt, tags 7.1 → 3.4 pt, notes 6.6–7.0 → 3.2–3.4 pt, footer 7.6 → 3.7 pt.
  5. Stale render: the print shows "перфектна/неперфектна информация" and "само несъвършени → обединени", while the mapping already says "пълна/непълна" and "само с непълна информация" (F06b-G06).
  6. Content: the dashed DeepStack–Libratus link "unified by depth-limited solving" suggests Libratus used depth-limited solving. It did not: its real-time subgames "always extended to the end of the game" (Brown, Sandholm & Amos, NeurIPS 2018, §1, read in arXiv:1805.08195). The unifying paper came a year later.
  7. "извън линия ↔ …" for *offline* (T12).
- **Fix:** `make_evolution_figure.py`: footer string split in two lines with "\n" (and the mapping likewise), box height 0.85 → 1.3; tags on three y-levels (`tag_y = [-0.3, -1.15, -2.0][i % 3]`) with ylim bottom −2.9 → −3.9, or shorten the BG tags; `new_fig(…, shrink=2.2)` once the bbox no longer widens; all fs ≥ 10. Note text: 'unified by depth-limited solving' → 'later unified by depth-limited solving (2018)' and the mapping → 'по-късно обобщени от решаването с ограничена дълбочина (2018)'. Mapping: 'Student of\nGames' → 'Student of\nGames' and 'Student of\nGames\n(2023)' → 'Student of\nGames\n(2023)' (identity); 'imperfect-only ↔ unified' → 'само непълна ↔ обединена\nинформация'; 'offline ↔ real-time search' → 'предварително изчисление ↔\nтърсене в реално време'; 'abstraction ↔ neural' → 'абстракция ↔ невронни мрежи'; 'learned-values lineage' → 'линия на научените стойности'; 'blueprint + search lineage' → 'линия „план + търсене“'; footer → 'Три оси на развитие – абстракция → невронни мрежи · предварително изчисление → търсене в реално време · само непълна информация → обединение –\nи нито една система не е най-напред и по трите едновременно: развитието е поредица от компромиси, а не класация.'

### F06b-G05 · S1 · Fig. 30 component-reuse map: wrong cells, "Студент по Игри", "стъпки 3–5", prints at 3.9–4.5 pt
- **Where:** `renders/ch06/p127_f1.png` — caption "Component-reuse map: …"; script `make_reuse_figure.py`.
- **Problem:**
  1. The figure contradicts the sources and the chapter text in four rows:
     - *AIVAT variance reduction* is filled for Libratus and empty for ReBeL and SoG. Libratus's *Science* paper never mentions AIVAT (full-text search); ReBeL §8: "Variance was reduced by using AIVAT"; SoG Results: "we use the Action-Informed Value Assessment Tool (AIVAT)".
     - *Continual re-solving* is filled for Libratus, Pluribus and ReBeL. SoG's Related Work names it as the difference from ReBeL ("The main difference is that SOG is based on (safe) continual re-solving"); Libratus uses nested safe subgame solving and Pluribus depth-limited search.
     - *Depth-limited solving* is filled for Libratus (see G04 item 6).
     - *Safe (nested) subgame solving* is filled for Pluribus, while the chapter says Pluribus "relies on *unsafe* search" and ReBeL §6 lists Pluribus [14] among the agents that "used unsafe search either partially or entirely".
  2. "Студент по Игри" (G04), "наследено от стъпки 3–5" (stale naming; EN source string "inherited from Steps 3–5").
  3. Mixed capitalization of row labels ("абстракция на действията", "ограничено по дълбочина решаване" vs "Невронна мрежа…"); "Карта / Информационна абстракция" (reads "Map / …"); "общодостъпно състояние на вярванията" vs the text's "публично състояние на убежденията" (T07).
  4. The long bottom note in BG widens the bounding box to 3924 px (11.9 in; EN 3300 px) → scale 0.52 at 15.8 cm: headers 8.6 → 4.5 pt, row labels 8.4 → 4.4 pt, side labels 8.2 → 4.3 pt, note 7.4 → 3.9 pt.
- **Fix:** `make_reuse_figure.py` ROWS: `("Continual re-solving", "B", [True, False, False, False, True], 0)`, `("Depth-limited solving", "B", [True, False, True, True, True], 0)`, `("AIVAT variance reduction", "B", [True, False, True, True, True], 0)`, `("Safe (nested) subgame solving", "B", [False, True, False, True, True], 1)`; "inherited from Steps 3–5" → "inherited from Chapters 3–5"; note split in two lines; `xlim=(-11.0, 14.4)` so that longer BG labels stay inside the axes, `shrink=2.6`, all fs → 10. Mapping: 'inherited from Chapters 3–5' → 'наследено от глави 3–5'; 'Card / information abstraction' → 'Абстракция на картите / информацията'; 'Action abstraction' → 'Абстракция на действията'; 'Depth-limited solving' → 'Решаване с ограничена дълбочина'; 'Continual re-solving' → 'Продължително пререшаване'; 'AIVAT variance reduction' → 'Намаляване на дисперсията (AIVAT)'; 'Safe (nested) subgame solving' → 'Безопасно (вложено) решаване на под-игри'; 'Public belief state' → 'Публично състояние на убежденията'; 'Neural value-and-policy net' → 'Невронна мрежа за стойности и стратегия'; 'Student of\nGames' identity (G04).

### F06b-G06 · S2 · Stale BG renders, and a print scale far below the pilot's assumption
- **Where:** `deliverables/reports/step06/summary/*_bg.png` (all written 1 Aug 13:08) vs `scripts/figures/out/figure_labels.json` (1 Aug 19:50).
- **Problem:** The printed fig. 29 predates the mapping (G04 item 5). Separately, the step-06 diagrams use `new_fig(shrink=1.8)` and print at 16.9 cm, so one matplotlib point prints as 0.69–0.72 pt (0.49–0.52 for figs. 29–30 because of the widened BG bounding box), not the 0.85 the brief assumes. At the current canvas the 8.2 pt floor needs fs ≥ 11.5; a central auto-fit that *shrinks* text to fit boxes would make these figures worse.
- **Fix:** after the mapping fixes, `python scripts/figures/render_bg_figures.py --only step06` and rebuild. Prefer `shrink` ≈ 2.2 (figs. 27–29) / 2.6 (fig. 30) with fs 10, and check that the BG render is not wider than the EN one (any text outside the axes widens the bbox). The same `new_fig` is used by figs. 24–26 (other reviewer).

## B — Bulgarian language

### F06b-B01 · S1 · corrupted sentence with English (SoG § "Архитектура")
- **Where:** summaryBg.md line 438; printed p. 118.
- **EN:** "The representation is inherited from the ReBeL lineage: a **public belief state** $\beta = (s_{\text{pub}},\nr)$ pairs the public state (in poker, the betting history and board) with a **range** $r$ — a pair of distributions over the information states each player could privately occupy."
- **Now → Proposed:** "Представянето е наследено от линията ReBeL: **общодостъпно състояние на вярванията** $ pairs the public state (in poker, the betting history and board) with a **range** $ - двойка разпределения върху информационните състояния, които всеки играч може тайно да заема." → "Представянето е наследено от линията на ReBeL: **публичното състояние на убежденията** $\beta = (s_{\text{pub}}, r)$ съчетава публичното състояние (в покера – историята на залаганията и общите карти) с **диапазон** $r$ – двойка разпределения върху информационните състояния, в които всеки играч може да се намира, без другите да знаят."
- **Why:** The inline math in the EN spans a line break (EN l. 1176–1177); the pipeline's math masking kept the two `$` and left the English between them untranslated. The printed page shows "$ pairs the public state … with a range $".

### F06b-B02 · S1 · corrupted sentence with a leftover placeholder (SoG § "Ключова иновация")
- **Where:** summaryBg.md line 454; printed p. 120 as "()𝑎𝑛𝑑𝑠𝑒𝑎𝑟𝑐ℎ𝑑𝑒𝑒𝑝𝑒𝑛𝑠() … (⟦MATHI10⟧)".
- **EN:** "as the network improves ($\epsilon \to\n0$) and search deepens ($T \to \infty$), play converges to a Nash equilibrium — now for poker and chess alike."
- **Now → Proposed:** "Заедно теоремите казват това, което AlphaZero можеше само да предполага: с подобряването на мрежата ($) and search deepens ($) и задълбочаването на търсенето (⟦MATHI10⟧), играта сходи към равновесие на Наш - сега както за покер, така и за шах." → "Заедно теоремите казват това, което AlphaZero можеше само да предполага: с подобряването на мрежата ($\epsilon \to 0$) и задълбочаването на търсенето ($T \to \infty$) играта клони към равновесие на Наш - вече както в покера, така и в шаха."
- **Why:** Same cause as B01 (math across a line break, EN l. 1256–1257). "сходи" is not a verb form. Central note: `⟦MATHI…⟧` placeholders also survive in step08 (2×) and step09 (1×); a grep for `⟦MATH` and for `\$ [a-z]` in all summaryBg files should be part of the build check.

### F06b-B03 · S1 · English heading
- **Where:** summaryBg.md line 426 — "### The gap it closed" (printed as 6.6.1 on p. 116, and in the TOC).
- **Now → Proposed:** "### The gap it closed" → "### Празнината, която запълва"
- **Why:** English in the Bulgarian text. Optional (S3): the ReBeL heading "### Затворената празнина" (l. 329, also l. 63) reads as "the closed gap"; the same "### Празнината, която запълва" would align all five sections (Pluribus has "### Пропуските, които запълни").

### F06b-B04 · S1 · English in the SoG formula and English possessives
- **Where:** summaryBg.md lines 452, 454 (the l. 538 bullet is handled in F06b-C11).
- **Now → Proposed:**
  - "$$ \text{exploitability}\big(\bar{\pi}^{T}\big) \;\lesssim\; \underbrace{|\mathcal{F}|\,\epsilon}_{\text{value-net error (frontier)}} \;+\; \underbrace{\frac{|\mathcal{N}|\,U\!A}{\sqrt{T}}}_{\text{CFR convergence (interior)}}, $$" → "$$ \text{експлоатируемост}\big(\bar{\pi}^{T}\big) \;\lesssim\; \underbrace{|\mathcal{F}|\,\epsilon}_{\text{грешка на мрежата (граница)}} \;+\; \underbrace{\frac{|\mathcal{N}|\,U\sqrt{A}}{\sqrt{T}}}_{\text{сходимост на CFR (вътрешност)}}, $$" (also fixes F06b-C01)
  - "пряк структурен наследник на този при deepStack's $k_1\epsilon + k_2/\sqrt{T}$ и ReBeL's $\delta C_1 + \delta C_2/\sqrt{T}$" → "пряк структурен наследник на границите на DeepStack ($k_1\epsilon + k_2/\sqrt{T}$) и на ReBeL ($\delta C_1 + \delta C_2/\sqrt{T}$)"
- **Why:** English prints on p. 120 ("value-net error (frontier)", "deepStack’s", "ReBeL’s"). Cyrillic inside `\text{}` is untested in this corpus (F07-B08); check the first rebuild.

### F06b-B05 · S1 · "Recursive Belief-based Learning" used as a name 19 times
- **Where:** summaryBg.md lines 347, 349 (2×), 355 (3×), 363, 371 (3×), 373 (3×), 377, 379, 428 (2×), 430, 476. Lines 34 and 292 (other reviewer's sections) have the same defect.
- **EN:** "ReBeL" everywhere in these sentences.
- **Now → Proposed:** replace-all "Recursive Belief-based Learning" → "ReBeL" (apply last). Two agreement fixes follow from it: "но срещу реален противник то не знае неговата стратегия" → "но срещу реален противник той не знае стратегията му"; "Дори Recursive Belief-based Learning, най-общата от тях, беше представена и гарантирана само за непълна информация" → "Дори ReBeL, най-общата от тези системи, беше представен и имаше гаранции само за непълна информация".
- **Why:** The expansion is English, the EN says "ReBeL", and the two names alternate within one paragraph (l. 355), so a reader may think they are two systems. The Bulgarian expansion is given once, at l. 313.

### F06b-B06 · S1 · English fragments in the prose
- **Where:** summaryBg.md §§ ReBeL, SoG, Synthesis.
- **Now → Proposed:**
  - "представлява CFR solving на ограничена по дълбочина под-игра" → "представлява решаване с CFR на под-игра с ограничена дълбочина"
  - "Второто следствие е, че **alphaZero loop** може да работи с **CFR като алгоритъм за търсене**." → "Второто следствие е, че **цикълът на AlphaZero** може да работи с **CFR като алгоритъм за търсене**."
  - "Самата **pBS representation** е най-важната" → "Най-важно е самото **представяне чрез PBS**"
  - "уникалната pBS стойност, изпъкналостта, която позволява CFR-as-Search" → "единствената стойност на PBS, изпъкналостта, която позволява CFR да се използва като търсене"
  - "моделът на **CFR-as-Search с научен оценител на възел**" → "схемата **CFR като търсене с научен оценител на листата**"
  - "публични състояния на убеждението плюс AlphaZero-style RL и търсене" → "публични състояния на убежденията плюс обучение с подкрепление и търсене в стил AlphaZero"
  - "с pUCT expansion phase в стил AlphaZero, който *разширява* публичното дърво" → "с фаза на разширяване по PUCT в стил AlphaZero, която *разраства* публичното дърво"
  - "с текущата CFR policy" → "с текущата стратегия на CFR"
  - "стойности чрез Huber loss, стратегия чрез кръстосана ентропия" → "стойностите – чрез функцията на загуба на Хюбер (Huber loss), стратегията – чрез кръстосана ентропия"
  - "който предоставя CFR family и самите еталонни тестове" → "който предоставя семейството алгоритми CFR и самите еталонни игри"
  - "(в контраст с CPU-only ~$150 на Pluribus)" → "(за разлика от ~$150 само за CPU при Pluribus)"
  - "прави парадигмата RL+Search на AlphaZero *доказуемо коректна*" → "прави парадигмата на AlphaZero „обучение с подкрепление + търсене“ *доказуемо коректна*"
  - "„до 128 машини с по 8 gPUs всяка“" → "„до 128 машини с по 8 GPU всяка“"
  - "осем 32 GB Nvidia V100 gPUs** (от порядъка на 700 gPUs)" → "осем GPU Nvidia V100 с 32 GB** (общо около 700 GPU)"
  - l. 318 and l. 540: see F06b-B15 and F06b-C07.
- **Why:** English in the Bulgarian text; all of these print (pp. 106–124). The tokens "pBS", "gPU", "alphaZero" also show the lower-casing defect of B07.

### F06b-B07 · S2 · Names printed with a lower-case first letter
- **Where:** summaryBg.md: "deepStack" (10× in lines 331–522; 41× in the file), "gPU" (l. 343, 371), "pBS" (l. 341, 379, 385 2×), "hUNL" (l. 318, 324), "pUCT" (l. 418, 444), "babyTartanian8" (l. 377), "muZero" (l. 462), "reBeL" (l. 540), "alphaZero" (l. 353).
- **Now → Proposed:** case-sensitive replace-all: "deepStack" → "DeepStack", "gPU" → "GPU", "pBS" → "PBS", "hUNL" → "HUNL", "pUCT" → "PUCT", "babyTartanian8" → "BabyTartanian8", "muZero" → "MuZero", "reBeL" → "ReBeL", "alphaZero" → "AlphaZero".
- **Why:** The pipeline lower-cased the first letter of names it treated as sentence-internal words; all print (e.g. p. 106 "Само deepStack имаше…"). None of these strings is correct anywhere in the corpus, so a file-wide replace is safe.

### F06b-B08 · S2 · Latin letter inside a Bulgarian word
- **Where:** summaryBg.md line 313 — "Триĸът е да се преформулира играта"
- **Now → Proposed:** "Триĸът е да се преформулира играта" → "Трикът е да се преформулира играта"
- **Why:** "ĸ" is U+0138 LATIN SMALL LETTER KRA, not Cyrillic "к": the word cannot be found by search and breaks hyphenation. It is the only mixed-script word in lines 299–564.

### F06b-B09 · S1 · meaning — "concave" for *convex* optimization problems
- **Where:** summaryBg.md § "Ключова иновация" (ReBeL) — "тези представяния на убежденията са *вдлъбнати* задачи за оптимизация"
- **EN:** "in two-player zero-sum games these belief representations are *convex* optimization problems"
- **Now → Proposed:** "тези представяния на убежденията са *вдлъбнати* задачи за оптимизация" → "тези представяния на убежденията са *изпъкнали* оптимизационни задачи"
- **Why:** The BG changes the mathematical claim. The ReBeL paper (§4) and the Meta blog both say "convex optimization problems"; the value function is concave, the problem is convex. The chapter itself says "изпъкналостта" at l. 379.

### F06b-B10 · S1 · meaning — "в очакване" for *in expectation* (T05)
- **Where:** summaryBg.md § "Ключова иновация" (ReBeL) — "това води до безопасно търсене - равновесие на Наш *в очакване* - без допълнителни ограничения"
- **EN:** "this yields safe search — a Nash equilibrium *in expectation* — with no extra constraints"
- **Now → Proposed:** "това води до безопасно търсене - равновесие на Наш *в очакване* - без допълнителни ограничения" → "това води до безопасно търсене (изиграната стратегия е равновесие на Наш *по математическо очакване*) без допълнителни ограничения"
- **Why:** "равновесие в очакване" reads as "an equilibrium that is pending". The meaning is that the randomly chosen iteration's policy equals a Nash policy on average (ReBeL §6).

### F06b-B11 · S1 · meaning — "многопроцесорно поле" for *multi-pro field*
- **Where:** summaryBg.md § "Силни страни и ограничения" (ReBeL) — "в 7500 ръце, вместо на многопроцесорно поле."
- **EN:** "over 7,500 hands rather than a multi-pro field"
- **Now → Proposed:** "в 7500 ръце, вместо на многопроцесорно поле." → "в 7500 раздавания, а не на мач срещу няколко професионалисти."
- **Why:** "многопроцесорно" means multi-processor. The settled glossary entry "multi-pro field → многопроцесорно поле" is the source; fix it in the picker.

### F06b-B12 · S1 · meaning — "възпрепятствани" for *perturbed*
- **Where:** summaryBg.md § "Ограничения, задънени улици…" (ReBeL) — "запазва ръчно избран списък с най-много осем или девет размера на залози (възпрепятствани по време на обучението)"
- **EN:** "a hand-chosen menu of at most eight or nine bet sizes (perturbed during training)"
- **Now → Proposed:** "(възпрепятствани по време на обучението)" → "(леко варирани по време на обучението)"
- **Why:** "възпрепятствани" means "hindered". ReBeL App. D: each bet size "is perturbed by ±0.1× pot during training".

### F06b-B13 · S1 · meaning — "предварителните" for *preflop*
- **Where:** summaryBg.md § "Изчислителна мощност и достъпност" (ReBeL) — "като предварителните под‑игри са кеширани"
- **EN:** "with preflop subgames cached to go faster still"
- **Now → Proposed:** "като предварителните под‑игри са кеширани" → "като под‑игрите на префлопа се кешират"
- **Why:** *Preflop* is the first betting round, not "preliminary". The quote contains U+2011 non-breaking hyphens, as in the file.

### F06b-B14 · S1 · meaning — "речна абстракция" for *river abstraction*
- **Where:** summaryBg.md § "Ограничения, задънени улици…" (ReBeL) — "(използвайки **речна абстракция**, за да направят това постижимо)"
- **Now → Proposed:** "(използвайки **речна абстракция**, за да направят това постижимо)" → "(използвайки **абстракция на ривъра**, за да го направят изчислимо)"
- **Why:** "речна" means "of a river (water)". The chapter already says "абстракция на ривъра" at l. 331. Settled entry "river abstraction → речна абстракция" (freq 1) should be fixed in the picker.

### F06b-B15 · S1 · translated or half-translated names (T13)
- **Where:** summaryBg.md lines 318, 373, 377, 379, 410, 470.
- **Now → Proposed:**
  - "| Тип на играта | Общи двуигрови игри с непълна информация; оценяван върху hUNL poker + лъжливи зарове (и ендгейм холд'ем на ход)." → "| Тип на играта | Произволни игри за двама с нулева сума и непълна информация; оценен върху HUNL покер и Liar's Dice (и опростения вариант turn endgame hold'em)."
  - "(за „лъжливи зарове“)" → "(за Liar's Dice)"
  - "се сближава към **приблизително равновесие на Наш** в „лъжливи зарове“" → "се сближава към **приблизително равновесие на Наш** в Liar's Dice"
  - "(Ледюк, лъжливи зарове, Scotland Yard)" → "(Ледюк, Liar's Dice, Scotland Yard)"
  - "статията посочва „слепец шах с разузнаване“" → "статията посочва Reconnaissance Blind Chess (шах „на сляпо“ с разузнаване)"
  - "под името *играч на игри*" → "под името *Player of Games*"
- **Why:** Game and system names stay in Latin script (brief rule; the chapter itself writes "Liar's Dice" at l. 313 and 513 and "Scotland Yard" throughout). "*играч на игри*" hides that it is the paper's former title. "hUNL poker" and "ендгейм холд'ем на ход" are English/calques; "двуигрови" see B27.

### F06b-B16 · S1 · meaning — "надвишава … нивото" for *defeats the agent*
- **Where:** summaryBg.md § "Student of Games / SoG (2023)" — "**надвишава най-съвременното ниво на агент за Scotland Yard**"
- **EN:** "**defeats the state-of-the-art Scotland Yard agent**"
- **Now → Proposed:** "**надвишава най-съвременното ниво на агент за Scotland Yard**" → "**побеждава най-силния съществуващ агент за Scotland Yard**"
- **Why:** The BG says SoG "exceeds the state-of-the-art level of an agent"; the result is a head-to-head win against PimBot (SoG Fig. 5).

### F06b-B17 · S2 · meaning — "детективът … се брои като един отбор"
- **Where:** summaryBg.md SoG table — "(детективът в Scotland Yard се брои като един отбор)"
- **EN:** "(Scotland Yard's detectives count as one team)"
- **Now → Proposed:** "(детективът в Scotland Yard се брои като един отбор)" → "(в Scotland Yard детективите действат като един отбор, т.е. като един играч)"
- **Why:** A single detective cannot be a team; the point is that the several detectives are pooled into one player.

### F06b-B18 · S1 · meaning — SoG's +434 against LBR attributed to "weaker bots"
- **Where:** summaryBg.md § "Силни страни и ограничения" (SoG) — "и решаващо е, че *не* бива експлоатиран от сондаж за най-добър локален отговор, който хваща по-слабите ботове, които той побеждава с +434 mbb/g)"
- **EN:** "and crucially it is *not* exploited by the local-best-response probe that catches weaker bots, which it beats by +434 mbb/g)"
- **Now → Proposed:** "и решаващо е, че *не* бива експлоатиран от сондаж за най-добър локален отговор, който хваща по-слабите ботове, които той побеждава с +434 mbb/g)" → "и, което е решаващо, локалният най-добър отговор (LBR), който открива слабости в по-слабите ботове, *не* успява да го експлоатира – SoG печели срещу него +434 mbb/g)". EN (the relative clause is ambiguous there too): → "and crucially the local-best-response probe that catches weaker bots fails to exploit it — SoG beats LBR by +434 mbb/g)".
- **Why:** In the BG, SoG beats the weaker bots by 434; SoG Table 2 reports +434 ± 9 mbb/hand against LBR.

### F06b-B19 · S1 · meaning — "предходна стратегия" for *prior policy* (T08); "излъчва"
- **Where:** summaryBg.md lines 438, 444, 446; table l. 417 has "предварителна *стратегия*".
- **Now → Proposed:**
  - "излъчва както вектор от контрафактични стойности (по една за всяко информационно състояние, за всеки играч), така и предходна стратегия" → "извежда както вектор от контрафактични стойности (по една за всяко информационно състояние и всеки играч), така и априорна стратегия"
  - "което *смесва* предварителната стратегия на мрежата с текущата CFR policy" → "което *смесва* априорната стратегия на мрежата с текущата стратегия на CFR" (includes the B06 item)
  - "GT-CFR следователно разширява първите $k$ действия по предварително убеждение" → "Затова GT-CFR разширява $k$-те действия с най-голяма априорна вероятност"
  - "предварителна *стратегия*" → "априорна *стратегия*"
- **Why:** "предходна" means "previous"; the CVPN outputs a *prior* policy that guides search. "излъчва" means "broadcasts" (F07-G05). "по предварително убеждение" misreads *by prior* (the policy head), not a belief.

### F06b-B20 · S1 · calque — *actors* / *trainers* as "актьори" / "треньори" / "изпълнители"
- **Where:** summaryBg.md lines 438, 468.
- **Now → Proposed:**
  - "Офлайн актьорите играят игри чрез самообучение" → "Офлайн процесите за генериране на данни (actors) играят срещу себе си"
  - "докато треньорите настройват нова CVPN и периодично я връщат обратно" → "докато обучаващите процеси (trainers) обучават нова CVPN и периодично я изпращат обратно"
  - "Базовата линия на AlphaZero използва 3500 едновременни изпълнители, всеки на един Google TPUv4" → "Базовата версия на AlphaZero използва 3500 паралелни процеса за генериране на данни (actors), всеки на един Google TPUv4"
- **Why:** "актьори" are stage actors and "треньори" sports coaches. These are distributed-training roles.

### F06b-B21 · S1 · meaning — "полицийно насочено" for *policy-guided*
- **Where:** summaryBg.md § "Наследство и съвременна значимост" (SoG) — "**GT-CFR** като търсене с нарастващо дърво, полицийно насочено и валидно за всеки клас игри"
- **Now → Proposed:** "**GT-CFR** като търсене с нарастващо дърво, полицийно насочено и валидно за всеки клас игри" → "**GT-CFR** като търсене с нарастващо дърво, насочвано от мрежата за стратегия и приложимо за всеки клас игри"
- **Why:** "полицийно" means "by the police".

### F06b-B22 · S1 · meaning — "звуково" for *sound* (T03)
- **Where:** summaryBg.md lines 484, 548 (2×).
- **Now → Proposed:**
  - "Като най-общата **рамка за звуково търсене**, базирана на PBS, тя е естественият контекст за **принос 1**" → "Като най-общата **рамка за коректно търсене**, базирана на PBS, тя е естественият контекст за **Принос 1**"
  - "че дори най-общата **рамка за звуково търсене** все още ограничава" → "че дори най-общата **рамка за коректно търсене** все още ограничава"
  - "носенето на **модел на противника** по звуков начин отвъд този хоризонт - вместо да се изхвърля на листа -" → "коректното пренасяне на **модела на противника** отвъд този хоризонт - вместо той да се изоставя в листата -"
- **Why:** "звуково търсене" is "acoustic search". *Sound* means correct/soundness-preserving; the chapter uses "коректен" elsewhere. "изхвърля на листа" reads as "throws onto a sheet of paper".

### F06b-B23 · S1 · meaning — "многопотребителски", "мултиплейър", "N-играч", "седем-игрови" for *multiplayer* (T01)
- **Where:** summaryBg.md lines 383, 476, 532, 548.
- **Now → Proposed:**
  - "така че *многопотребителската* празнина в сигурността, разкрита от Pluribus, остава недокосната дори тук" → "така че празнината в *безопасността при много играчи*, разкрита от Pluribus, остава незасегната дори тук"
  - "Ако равновесието не осигурява безопасност в многопотребителската среда от самото начало" → "Ако при много играчи равновесието изначално не осигурява безопасност"
  - "Вторият е **безопасност в мултиплейър среда**" → "Вторият е **безопасността при много играчи**"
  - "в седем-игрови, със смесени мотиви, игра на естествен език далеч извън двуигровите гаранции на ReBeL" → "в игра за седем играчи със смесени мотиви и комуникация на естествен език, далеч извън гаранциите на ReBeL за двама играчи"
  - l. 528 "двете многопотребителски и тествани с хора системи": see F06b-C05; l. 512 table: see F06b-B46; l. 548 "N-играч игри": see F06b-S14.
- **Why:** "многопотребителски" is "multi-user" (software); "сигурност" is security, while the chapter's term is "безопасност" (safety). Glossary entries cause it (T01).

### F06b-B24 · S1 · meaning — "невидимост за противника" / "независима от противника" for *opponent-blind(ness)* (T04)
- **Where:** summaryBg.md lines 528, 548.
- **Now → Proposed:**
  - "Всяка система, разгледана тук, е **независима от противника по дизайн**:" → "Всяка система, разгледана тук, е **„сляпа“ за противника по замисъл**:"
  - "Първият е самата **невидимост за противника**:" → "Първият е самата **„слепота“ за противника**:"
- **Why:** "невидимост за противника" says the system is invisible *to* the opponent, the inverse of the point. "независима от противника" is closer but loses "blind"; "по дизайн" is a calque (B38).

### F06b-B25 · S1 · meaning — "начално число" for a metaphorical *seed*
- **Where:** summaryBg.md lines 536, 548.
- **EN:** "each is a one-line seed for later chapters" / "each is the seed of a later chapter"
- **Now → Proposed:**
  - "всяко представлява едноредово **начално число** за по-късни глави." → "всяка е идея в един ред, която следващите глави могат да развият."
  - "и всеки е начално число за по-късна стъпка." → "и всеки от тях е отправна точка за някоя от следващите глави."
- **Why:** "начално число" is the glossary term for a random-number *seed* (F07-B19); here *seed* means "germ of an idea". "стъпка" is stale naming (C07).

### F06b-B26 · S1 · meaning — "цялата граница" for *the entire frontier* (state of the art)
- **Where:** summaryBg.md § "Нерешени проблеми…" — "цялата граница изчислява фиксирана, **стратегия, оптимална в най-лошия случай** и я играе безусловно"
- **EN:** "the entire frontier computes a fixed, worst-case-optimal strategy and plays it unconditionally"
- **Now → Proposed:** "цялата граница изчислява фиксирана, **стратегия, оптимална в най-лошия случай** и я играе безусловно" → "всички най-съвременни системи изчисляват фиксирана **стратегия, оптимална в най-лошия случай**, и я играят безусловно"
- **Why:** "граница" (boundary) does not mean "state of the art" (settled entry "frontier → граница"). The comma after "фиксирана" splits the adjective from its noun.

### F06b-B27 · S2 · terminology — "двуигрови" for *two-player* (T02)
- **Where:** summaryBg.md lines 318 (in B15), 351, 353, 359, 377, 379, 383 (in B23), 484, 504.
- **Now → Proposed:**
  - "в двуигрови игри с нулева сума всяко общодостъпно състояние на убеждението $\beta$ носи уникална стойност" → "в игрите за двама с нулева сума всяко публично състояние на убежденията $\beta$ има единствена стойност"
  - "Спасителният фактор е, че в двуигрови игри с нулева сума" → "За щастие, в игрите за двама с нулева сума"
  - "*се връща към двуигрови игри с нулева сума и възстановява" → "*се връща към игрите за двама с нулева сума и възстановява"
  - "във всяка **двуигрови игра с нулева сума**" → "във всяка **игра за двама с нулева сума**"
  - "важат **само за двуигрови игри с нулева сума**" → "важат **само за игри за двама с нулева сума**"
  - "до **двуигрови игра с нулева сума**" → "до **игри за двама с нулева сума**"
  - "И двете системи останаха двуигрови" → "И двете системи останаха за двама играчи"
- **Why:** "двуигрови" suggests "two-game"; the curated and settled term is "игра за двама с нулева сума", which the chapter also uses. "уникална стойност" → "единствена" (*unique* in the mathematical sense).

### F06b-B28 · S2 · terminology — "самообучение" for *self-play*, including tautologies (T06)
- **Where:** summaryBg.md, 33 occurrences in lines 299–564 (7 already say "самоигра").
- **Now → Proposed:**
  - "за първи път я комбинира с обучение чрез самообучение в *състезателна* среда" → "за първи път я съчетава с обучение с подкрепление чрез самоигра в *състезателна* среда"
  - "пуснем AlphaZero - обучение чрез самоигра с подкрепление плюс търсене" → "пуснем AlphaZero - обучение с подкрепление чрез самоигра плюс търсене"
  - "съюзът на AlphaZero между обучение чрез самоигра с подкрепление и търсене" → "съчетанието в AlphaZero на обучение с подкрепление чрез самоигра и търсене"
  - "пълната сила на обучение чрез самоигра с подкрепление плюс търсене се прехвърля" → "цялата мощ на обучението с подкрепление чрез самоигра плюс търсене може да се пренесе"
  - "който се учи чрез самообучение без човешки данни" → "който се учи чрез самоигра, без човешки данни"
  - All other *self-play* occurrences: "самообучение" → "самоигра" (e.g. "цикъл на самообучение" → "цикъл на самоигра"; "правилно самообучение" → "коректна самоигра", T03).
- **Why:** "обучение чрез самообучение" is "training by self-training"; *self-play* is play against copies of oneself. "обучение чрез самоигра с подкрепление" misplaces "с подкрепление" (*self-play reinforcement learning* = RL by self-play).

### F06b-B29 · S2 · terminology — five names for the public belief state (T07)
- **Where:** summaryBg.md lines 313, 333, 337, 343, 345, 349, 351.
- **Now → Proposed:**
  - "върху **публични състояния на убеждения**" → "върху **публични състояния на убежденията (PBS)**"
  - "*общодостъпно състояние на убеждението*" → "*публично състояние на убежденията*"
  - "### Ключова иновация: общодостъпни състояния на убеждението и научени стойности в пространството на убежденията" → "### Ключова иновация: публични състояния на убежденията и научени стойности в пространството на убежденията"
  - "*общодостъпни състояния на убеждението*" → "*публични състояния на убежденията*"
  - "**общодостъпното състояние на убеждението** (разделът по-долу)" → "**публичното състояние на убежденията** (разделът по-долу)"
  - "**Общодостъпното състояние на убеждението (PBS)** е сърцевината" → "**Публичното състояние на убежденията (PBS)** е сърцевината"
  - "нарича това състояние общодостъпно състояние на убеждението" → "нарича това състояние публично състояние на убежденията"
  - "Но под-игра, вкоренена в *общодостъпно състояние на убеждението*, има такава" → "Но под-игра с корен в *публично състояние на убежденията* има такава"
  - l. 438 "общодостъпно състояние на вярванията": in B01.
- **Why:** The chapter pairs PBS with "публично състояние" (*public state*) in the same sentences; "общодостъпно" (publicly accessible) and "вярвания" (religious beliefs) break the pairing. "вкоренена" means "deeply rooted".

### F06b-B30 · S2 · terminology — *leaf* rendered "възел" (node) (T09)
- **Where:** summaryBg.md lines 337, 341, 343, 430.
- **Now → Proposed:**
  - "като оценителят на възел е научена мрежа за стойности, вместо разгръщане" → "като оценителят на листата е научена мрежа за стойности, а не симулация до края на играта (rollout)"
  - "избира възел, който да стане следващото кореново PBS" → "избира листо, което става следващото коренно PBS"
  - "задава стойността на всеки възел чрез заявка към **научената pBS value мрежа** - така че стойностите на възлите се променят от итерация до итерация" → "задава стойността на всяко листо чрез заявка към **научената мрежа за стойности върху PBS** - така стойностите в листата се променят от итерация до итерация"
  - "(Глава 5) е оценителят на възел" → "(Глава 5) е оценителят на листата"
  - "да прочете една единствена стойност от всеки **възел**" → "да прочете една-единствена стойност от всяко **листо**"
  - "за *убеждение* относно скритите състояния във всеки **възел**" → "за *убеждение* относно скритите състояния във всяко **листо**"
- **Why:** The point of depth-limited search is what happens at the *leaves*; "възел" (any node) loses it. The chapter uses "листа" correctly elsewhere (l. 321, 450). "разгръщане" for *rollout* is opaque.

### F06b-B31 · S2 · terminology — "търсене по всяко време" for *anytime search* (T10)
- **Where:** summaryBg.md lines 410, 430, 444, 468.
- **Now → Proposed:**
  - "търсене по всяко време, което изгражда дървото на играта постепенно, водено от мрежа за политики" → "търсене, което може да бъде прекъснато във всеки момент (anytime) и изгражда дървото на играта постепенно, насочвано от мрежа за стратегия"
  - "насочено, асиметрично, по всяко време" → "насочено, асиметрично и с възможност за прекъсване във всеки момент"
  - "дава търсене *по всяко време*" → "дава търсене, което *може да бъде прекъснато във всеки момент*"
  - "По време на игра търсенето е по всяко време и може да се настройва" → "По време на игра търсенето може да бъде прекъснато във всеки момент и бюджетът му се настройва"
- **Why:** "по всяко време" reads as "at any time of day". An anytime algorithm returns a usable answer whenever it is stopped.

### F06b-B32 · S2 · terminology — *compute* as "изчислителна мощност" (F07-T12) and *test-time compute* (T11)
- **Where:** summaryBg.md lines 324, 343, 367, 369, 383, 421, 466, 468, 474, 506, 511, 540 (in C07), 542 (in S17).
- **Now → Proposed:**
  - "### Изчислителна мощност и достъпност" (2× in this half; 5× in the file) → "### Изчислителни разходи и достъпност"
  - "| Изчислителна мощ |" (2×) → "| Изчислителни разходи |"
  - "основната изчислителна мощност се използва за **gPU самообучение**, което обучава мрежата за стойности (балансът е разгледан под *Изчислителна мощност*)" → "основните изчислителни разходи са за самоиграта на GPU, с която се обучава мрежата за стойности (вж. *Изчислителни разходи*)"
  - "най-важните данни за изчислителната мощност" → "най-важните данни за изчислителните разходи"
  - "**изчислителна мощност във време на тестване**" → "**изчисления по време на изпълнение (test-time compute)**"
  - "„е обучен с подобно количество изчислителна мощност TPU“" → "„е обучен с подобно количество TPU ресурси“"
  - "намаляването на тази изчислителна мощност" → "намаляването на тези изчислителни разходи"
  - "той **се мащабира** с изчислителна мощност" → "качеството му **расте** с изчислителния ресурс"
  - "пълна информация, изчислителна мощност, ключова иновация)" → "пълна информация, изчислителни разходи, ключова иновация)"
  - "изчислителна мощност в мащаба на суперкомпютър" → "изчислителни разходи в мащаба на суперкомпютър"
- **Why:** "мощност" is hardware power; every use here means cost or resources. The SoG quote translates "TPU resources".

### F06b-B33 · S2 · terminology — *policy* as "политика" next to "стратегия"
- **Where:** summaryBg.md, 17 occurrences in lines 313–514 ("мрежа за стойност и политика (CVPN)", "мрежа за политики", "стойност/политика", "своята политика"); "стратегия" is used 45 times for the same concept.
- **Now → Proposed:** "политика/политики" → "стратегия/стратегии" in all 17, e.g. "**Контрафактичната мрежа за стойност и политика (CVPN)**" → "**Контрафактичната мрежа за стойности и стратегия (CVPN)**", "водено от мрежа за политики" → "насочвано от мрежа за стратегия" (in B31), "усъвършенства своята политика" → "усъвършенства своята стратегия".
- **Why:** The curated dictionary (`terminology_EN_BG.md`: Policy → Стратегия, "standard in BG") and the rest of the chapter use "стратегия". "политика" also reads as "politics/policy (government)".

### F06b-B34 · S2 · terminology — "Неш" next to "Наш"
- **Where:** summaryBg.md § "Наследство и съвременна значимост" (SoG), l. 484 (2×).
- **Now → Proposed:**
  - "превръщайки убеждение, търсещо Неш равновесие, в адаптивно такова" → "превръщайки убеждение, насочено към равновесие на Наш, в адаптивно"
  - "статията изрично посочва, че Неш е „по-малко значим“ извън нея" → "статията изрично посочва, че извън тях гаранцията на равновесието на Наш е „по-малко смислена“"
- **Why:** The chapter and glossary use "Наш" (15×). The second quote also misattributes: SoG says "the theoretical guarantee of Nash equilibria … is less meaningful", not that Nash himself is (F06b-C06).

### F06b-B35 · S2 · terminology — "термин" for a *term* of a formula
- **Where:** summaryBg.md lines 359, 454.
- **Now → Proposed:**
  - "термин за грешка в стойността плюс обикновен термин за сходимост на CFR" → "член за грешката в стойността плюс обичайния член за сходимостта на CFR"
  - "и двата термина вече се мащабират" → "и двата члена вече се мащабират"
  - "член за грешка в стойността плюс $1/\sqrt{T}$ термин за сходимост на CFR" → "член за грешката в стойността плюс член за сходимостта на CFR от вида $1/\sqrt{T}$"
- **Why:** "термин" is a terminology word; a summand is "член" (F07-B16). The chapter uses "член" correctly at l. 450.

### F06b-B36 · S2 · grammar — agreement errors
- **Where:** summaryBg.md lines 331, 359, 377, 410, 444, 528, 534, 544.
- **Now → Proposed:**
  - "Междувременно най-успешният парадигма във всички игрови изкуствени интелекти" → "Междувременно най-успешната парадигма в изкуствения интелект за игри"
  - "с подобряването на мрежата за стойности, $\delta \to 0$ и играта на ReBeL се доближават до точно равновесие на Наш" → "с подобряването на мрежата за стойности $\delta \to 0$ и играта на ReBeL се доближава до точно равновесие на Наш"
  - "търсене, което е **доказуемо безопасен** по време на тестване" → "търсене, което е **доказуемо безопасно** по време на тестване"
  - "ReBeL възстанови коректността за игра за двама с нулева сума покер" → "ReBeL възстанови коректността в покера като игра за двама с нулева сума"
  - "за да го поддържа самосъгласуван" → "за да го поддържа самосъгласувано"
  - "които споделят точно една пропуск" → "които споделят точно един пропуск"
  - "Тази обща пропуск представлява отвора, който заема цялата тази дисертация" → "Именно този общ пропуск е нишата, в която работи цялата дисертация"
  - "Глава стандартизира **експлоатируемостта**" → "Главата стандартизира **експлоатируемостта**"
  - "твърде грубият типови модел" → "твърде грубият типов модел"
- **Why:** "парадигма", "играта" are feminine singular; "търсене", "дърво" neuter; "пропуск" masculine; "типови" is plural. "отвор" is a physical hole.

### F06b-B37 · S2 · non-words and typos
- **Where:** summaryBg.md lines 331, 333, 448 (l. 454 in B02).
- **Now → Proposed:**
  - "шахматна позиция струва толкова, колкотото струва" → "шахматна позиция струва толкова, колкото струва"
  - "да сходяват към игровотеоретичните" → "да клонят към игровотеоретичните"
  - "Предишните три системи се сходиха към една и съща рецепта" → "Предишните три системи стигнаха до една и съща рецепта"
- **Why:** "колкотото" is a typo; "сходяват" is not a Bulgarian verb (cf. F07-B03 "сходява"); "се сходиха" means "became friends / came together".

### F06b-B38 · S2 · calques — ReBeL and SoG sections
- **Where:** summaryBg.md lines 331, 351, 353, 355, 365, 367, 377, 383, 385, 460, 462, 480, 482.
- **Now → Proposed:**
  - "може ли рецептата на AlphaZero да бъде накарана да работи коректно" → "може ли рецептата на AlphaZero да работи коректно" (inside the S02 rewrite)
  - "но бяха обучени по много по-ад хок начин." → "но бяха обучени по много по-импровизиран начин."
  - "Третото следствие - и водещото заглавие - е" → "Третото и най-важно следствие е"
  - "**пререшаването** ѝ, à la Libratus и Pluribus." → "**пререшаването** ѝ, както в Libratus и Pluribus."
  - "(резултатът от §6 премахва *време-на-тестване* версията на това предположение" → "(резултатът от §6 на статията премахва това предположение за *етапа на тестване*"
  - "статията е, по дизайн, теоретична." → "статията е по замисъл теоретична."
  - "Силата на сигнала на Recursive Belief-based Learning е **общност с гаранция**." → "Главното предимство на ReBeL е **общност, подкрепена с гаранция**."
  - "а ReBeL е най-чистото изявление на" → "а ReBeL е най-ясната формулировка на"
  - "вместо всичко да се пече в една предварително изчислена стратегия, същата теза, която сега е централна за моделите с възможност за мислене." → "вместо всичко да се влага предварително в една изчислена стратегия – същата идея, която днес е централна за моделите за разсъждение (reasoning models)."
  - "**ReBeL е жив стъпаловиден камък, а не крайна точка**" → "**ReBeL е междинна, но все още актуална стъпка, а не крайна точка**"
  - "Шмид откровено заявява, че това е по дизайн" → "Шмид откровено заявява, че това е умишлено"
  - "с над 1100 ело точки" → "с над 1100 точки Ело"
  - "а не най-добрият шахматен двигател" → "а не най-силната шахматна програма"
  - "„забранително скъпо в някои игри“" → "„непосилно скъпо в някои игри“"
  - "*избира проби* от състояния на света" → "*генерира извадка* от състояния на света"
  - "полето премина от" → "областта премина от"
  - "Отношенията му към околния фронтир са изясняващи." → "Показателно е как SoG се съотнася със съседните направления."
  - "би разтворило и двете му посочени ограничения наведнъж" → "би премахнало наведнъж и двете му посочени ограничения"
- **Why:** Word-for-word renderings of *be made to work*, *ad hoc*, *the headline*, *à la*, *test-time version*, *by design*, *signal strength* (radio), *cleanest statement*, *bake*, *reasoning models*, *stepping stone*, *prohibitively*, *field* (a meadow), *frontier*, *dissolve*; "двигател" is a motor; Elo is a surname.

### F06b-B39 · S2 · calques — Synthesis
- **Where:** summaryBg.md lines 502, 534, 541, 542, 544.
- **Now → Proposed:**
  - "### Дъгата в едно четене" → "### Развитието накратко"
  - "прави ли преследването на слаб противник вас **контраексплоатируем**?" → "не става ли агентът **контраексплоатируем**, когато преследва слаб противник?"
  - "което е точно антагонистичната, стил „учебна атака“ оценка, от която се нуждае глава 8" → "което е точно състезателната оценка от типа на „обучаващата атака“, за която настоява глава 8"
  - "**намалителят на дисперсията на научената стойност**" → "**методът за намаляване на дисперсията чрез научени стойности**"
  - "срещу бруталната дисперсия на картите игри" → "въпреки огромната дисперсия в игрите с карти"
  - "дисертацията изпълнява същия цикъл наблюдение–последвано от корекция" → "дисертацията прилага същия цикъл „наблюдение → корекция“"
  - "- **Кука за разказ за границата (рамкиране).**" → "- **Връзка със съвременния дебат (рамкиране).**"
  - "предсказвайки режим на отказ за Принос 3 да улови." → "което предсказва вид провал, който Принос 3 трябва да може да улови."
- **Why:** *the arc in one read*, *hook*, *failure mode for C3 to catch*, *learned-value variance reducer* are word-for-word; "картите игри" is ungrammatical; "учебна атака" contradicts Chapter 8, which says "обучаващата атака".

### F06b-B40 · S2 · meaning — "представителна" for *representational*
- **Where:** summaryBg.md lines 383, 504 (2×).
- **Now → Proposed:**
  - "Отстранете покера и трайната идея на ReBeL е представителна:" → "Ако оставим покера настрана, трайната идея на ReBeL е свързана с представянето:"
  - "странично движение по представителната ос и назад по гаранциите" → "странично движение по оста на представянето и крачка назад по гаранциите"
  - "придвижи представителната ос най-далеч досега" → "стигна най-далеч по оста на представянето"
- **Why:** "представителна" means "representative" (as in a sample, or impressive), not "concerning representation".

### F06b-B41 · S2 · meaning — finite-time guarantee
- **Where:** summaryBg.md § "Ключова иновация" (SoG) — "С $k=\infty$ търсенето дори получава *крайно-времева* гаранция за качеството на стратегията, а не само такава в крайна сметка."
- **EN:** "With $k=\infty$ the search even gains a *finite-time* guarantee on policy quality, not merely an in-the-limit one."
- **Now → Proposed:** "С $k=\infty$ търсенето дори получава *крайно-времева* гаранция за качеството на стратегията, а не само такава в крайна сметка." → "При $k=\infty$ търсенето има дори гаранция за качеството на стратегията *при краен брой итерации*, а не само асимптотична."
- **Why:** "в крайна сметка" means "after all"; *in-the-limit* is "асимптотична / в границата".

### F06b-B42 · S2 · meaning — "наивно прекъсва търсенето"
- **Where:** summaryBg.md § "Ключова иновация" (ReBeL) — "и следователно не знае в кое PBS се намира, което наивно прекъсва търсенето."
- **EN:** "and therefore does not know which PBS it is in, which naively breaks search"
- **Now → Proposed:** "и следователно не знае в кое PBS се намира, което наивно прекъсва търсенето." → "и следователно не знае в кое PBS се намира, а при наивен подход това прави търсенето некоректно."
- **Why:** "прекъсва" means "interrupts"; the problem is that search rooted at a wrong PBS is unsound (ReBeL §6).

### F06b-B43 · S2 · meaning — network size and input
- **Where:** summaryBg.md ReBeL table — "MLP (GeLU/LayerNorm), 6×1536 скрити слоя за покер, вход = убеждение върху всеки от 1,326 ръце на играча + борда + пота + флаг за залог"
- **EN:** "6×1536 hidden for poker, input = belief over each player's 1,326 hands + board + pot + bet flag"
- **Now → Proposed:** "MLP (GeLU/LayerNorm), 6×1536 скрити слоя за покер, вход = убеждение върху всеки от 1,326 ръце на играча + борда + пота + флаг за залог" → "MLP (GeLU/LayerNorm), за покера 6 скрити слоя по 1536 неврона; вход = убеждения върху 1326-те възможни ръце на всеки играч + борда + пота + флаг за залог"
- **Why:** "6×1536 скрити слоя" reads as 9216 layers (ReBeL App. E: "6 hidden layers with 1536 [units] each"); "всеки от … ръце" breaks agreement.

### F06b-B44 · S2 · meaning — "сметка за обучение чрез дълбоко обучение"; CPU thread vs core; broken clause
- **Where:** summaryBg.md lines 324, 343, 371.
- **Now → Proposed:**
  - "Тясното място е генерирането на данни от самообучение - секвенциален CFR решава, чиято всяка итерация оценява всички възли листа чрез мрежата" → "Тясното място е генерирането на данни чрез самоигра – последователни решавания с CFR, при които на всяка итерация мрежата оценява всички листа"
  - "Това е категорично сметка за обучение чрез дълбоко обучение, а не CFR сметка: самото CFR търсене се изпълнява на едно процесорно ядро." → "Това са разходи за обучение на невронна мрежа, а не за CFR: самото търсене с CFR се изпълнява в една процесорна нишка."
  - "А **CFR търсене** работи на **един CPU поток** без никаква абстракция" → "А **търсенето с CFR** работи в **една нишка на CPU** без никаква абстракция"
  - "CFR на един CPU поток" → "CFR в една нишка на CPU"
- **Why:** "секвенциален CFR решава, чиято…" has no subject–verb structure; "обучение чрез дълбоко обучение" is a tautology; *thread* is "нишка" (ReBeL App. D: "single-thread CPU"), not "ядро" (core) or "поток" (stream).

### F06b-B45 · S2 · calque — "CFR търсене изпълнява търсенето"
- **Where:** summaryBg.md § "Архитектура" (ReBeL) — "Класическите градивни елементи от по-ранните стъпки все още са видими - **CFR търсене** (Глава 3) изпълнява търсенето"
- **EN:** "The classic building blocks of the earlier chapters are still visible — CFR (Chapter 3) is the search engine"
- **Now → Proposed:** "Класическите градивни елементи от по-ранните стъпки все още са видими - **CFR търсене** (Глава 3) изпълнява търсенето" → "Класическите градивни елементи от по-ранните глави все още са видими - **CFR** (Глава 3) изпълнява търсенето"
- **Why:** Tautology; "стъпки" is stale naming (the EN says "chapters").

### F06b-B46 · S2 · meaning — Synthesis table, Libratus and Pluribus rows
- **Where:** summaryBg.md lines 511–512, 516 (Table 14, p. 125).
- **Now → Proposed:**
  - "Първа директна *и* човешка победа чрез **вложено безопасно решаване на под-игри** в реално време с доказуема граница; самоусъвършенстващ се за една нощ, който поправя собствените си пропуски" → "Първа победа както срещу ботове, така и срещу хора, чрез **вложено безопасно решаване на под-игри** в реално време с доказуема граница; нощен модул за самоусъвършенстване, който запълва собствените пропуски на плана"
  - "без неврално обобщаване" → "без невронно обобщаване"
  - "Първа свръхчовешка **многоиграчена** (шест играчи) игра; прочуто евтина (~150 долара на един сървър)" → "Първа свръхчовешка игра **с много играчи** (шестима); известна с ниската си цена (~150 долара на един сървър)"
  - "(без N-игрови граници)" → "(без граници за N играчи)"
  - ": Петте системи по ред: какво добавя всяка и от какво се отказва за него." → ": Петте системи по ред: какво добавя всяка и от какво се отказва в замяна."
- **Why:** "директна победа" does not say *head-to-head against bots*; "самоусъвършенстващ се за една нощ" says it improved itself in one night; "многоиграчена" and "N-игрови" are not words; "за него" has no antecedent.

### F06b-B47 · S2 · meaning — card abstraction dropped
- **Where:** summaryBg.md § "Какво се пренася напред" — "**абстракция на действията** (глава 4) е в основата на Libratus и Pluribus"
- **EN:** "**card and action abstraction** (Chapter 4) underpin Libratus and Pluribus"
- **Now → Proposed:** "**абстракция на действията** (глава 4) е в основата на Libratus и Pluribus" → "**абстракцията на картите и на действията** (глава 4) е в основата на Libratus и Pluribus"
- **Why:** The BG says less than the EN: the card abstraction is exactly what ReBeL and SoG remove.

### F06b-B48 · S2 · meaning — "затвори *многоагентната безопасност*"
- **Where:** summaryBg.md l. 484 — "не направи нищо, за да затвори *многоагентната безопасност*, която Pluribus първо разкри"
- **EN:** "did nothing to close the *multi-agent safety* gap that Pluribus first exposed"
- **Now → Proposed:** "не направи нищо, за да затвори *многоагентната безопасност*, която Pluribus първо разкри" → "не затвори *празнината в безопасността при много агенти*, която Pluribus разкри първи"
- **Why:** The BG drops "gap" and says the safety itself was "closed".

### F06b-B49 · S2 · terminology — LBR as "сондаж"/"сонда"/"реакция"
- **Where:** summaryBg.md lines 377, 534 (l. 474 in B18).
- **Now → Proposed:**
  - "довежда **сондажа за най-добър локален отговор** до голяма загуба" → "побеждава с голяма разлика и **локалния най-добър отговор (LBR)**" (the footnote marker: see F06b-S02)
  - "**Локалната най-добра реакция (LBR) сонда**, използвана в цялата глава" → "**Локалният най-добър отговор (LBR)**, използван в цялата глава"
- **Why:** "сондаж" is drilling; "реакция" deviates from "най-добър отговор" (best response) used everywhere, including the [^lbr] footnote.

### F06b-B50 · S2 · terminology — mbb/g and *hands* (T14)
- **Where:** summaryBg.md lines 313, 324, 371, 377, 379.
- **Now → Proposed:**
  - "побеждавайки топ човешкия специалист в хедс-ъп Донг Ким със 165 mbb/g (мили-големи блайнда на игра, мерната единица за резултат от предишните раздели) в рамките на 7,500 ръце" → "побеждавайки Донг Ким – професионалист в хедс-ъп, загубил най-малко от Libratus – със 165 mbb/g (хилядни от големия блайнд на раздаване – мерната единица от предишните раздели) в рамките на 7,500 раздавания"
  - "игра < 2 s/ръка, ≤ 5 s/решение" → "игра < 2 s на раздаване, ≤ 5 s на решение"
  - "под две секунди на ръка средно" → "средно под две секунди на раздаване"
  - "с 165 mbb/g в 7500 ръце" → "с 165 mbb/g в 7500 раздавания"
  - l. 379 "в 7500 ръце": in B11.
- **Why:** "мили-големи блайнда" is a calque (settled entry "milli-big-blinds per game"); a played *hand* is "раздаване" (F07-B20). "топ … специалист" is colloquial and overstates the paper (F06b-C13).

### F06b-B51 · S2 · terminology — CFR-AVG "обоснована" vs "коректна"
- **Where:** summaryBg.md § "Ограничения, задънени улици…" (ReBeL) — "според самите автори *няма доказана теоретична обоснованост* („дали тази модифицирана форма на CFR-AVG е теоретично обоснована остава отворен въпрос“)"
- **Now → Proposed:** "*няма доказана теоретична обоснованост* („дали тази модифицирана форма на CFR-AVG е теоретично обоснована остава отворен въпрос“)" → "*не е доказано коректна* („дали тази модифицирана форма на CFR-AVG е теоретично коректна, остава отворен въпрос“)"
- **Why:** *Theoretically sound* = "коректна" everywhere else in the chapter (settled: soundness → коректност); "обоснована" means "justified", a weaker and different notion.

### F06b-B52 · S2 · grammar — broken constructions
- **Where:** summaryBg.md lines 321, 349, 419, 438, 444, 474, 476.
- **Now → Proposed:**
  - "решаващ ограничена по дълбочина под-игра, кореняща се в PBS" → "решаващ под-игра с ограничена дълбочина и корен в PBS"
  - "дадено общите публични наблюдения." → "при дадени общи публични наблюдения."
  - "запазва само малко *рандомизирано залагане* (действие) меню в покера (≈20,000 → 4–5 действия), както ReBeL" → "запазва само малко *рандомизирано* меню от залози (действия) в покера (≈20,000 → 4–5 действия), както ReBeL"
  - "докато DeepStack използва отделни мрежи само за стойност на рунд" → "докато DeepStack използваше отделни мрежи само за стойности, по една за всеки рунд"
  - "решава за игрално-теоретично съгласувана стратегия на всяка стъпка." → "на всяка стъпка търси игровотеоретично коректна стратегия."
  - "Той използва **без човешки данни, без предварително изчислен план и без абстракция на картите**" → "Той **не използва човешки данни, предварително изчислен план или абстракция на картите**"
  - "до игри с огромни частни състояния" → "до игри с огромни пространства от частни състояния"
- **Why:** "кореняща се" (taking root), "дадено общите", "използва без", the displaced "меню", and "само за стойност на рунд" do not parse; "игрално" is not the adjective of "игра"; *sound* is "коректна", not "съгласувана".

### F06b-B53 · S2 · terminology — *offline* as "извън линия" (T12)
- **Where:** summaryBg.md lines 430, 468.
- **Now → Proposed:**
  - "Резултатът е кулминацията на главата: точката, в която дъгите абстракция-към-невронна и извън линия-към-търсене са съединени от трета - пълна и непълна информация, обединени." → "Резултатът е кулминацията на главата: към линиите „от абстракция към невронни мрежи“ и „от предварително изчисление към търсене“ се добавя трета – обединяването на игрите с пълна и непълна информация."
  - "Разходите на Student of Games са концентрирани **извън линия, в обучение чрез самообучение с мащаб TPU**" → "Разходите на Student of Games са съсредоточени **в предварителното обучение чрез самоигра на TPU клъстери**"
- **Why:** "извън линия" is a calque of *off-line*; the chapter otherwise says "офлайн" or "предварително". "с мащаб TPU" and the hyphenated noun chains do not parse.

### F06b-B54 · S3 · small consistency and typography items
- **Where:** summaryBg.md lines 349, 367, 410, 418, 442.
- **Now → Proposed:**
  - "(тя датира от работата върху кооперативни POMDPs)" → "(тя датира от работите върху кооперативни POMDP)"
  - "Линеен CFR" → "Linear CFR"
  - "работи вътре в продължително пре-решаване" → "работи вътре в продължителното пререшаване"
  - "търсенето с дърво Монте-Карло" → "търсенето в дърво на Монте Карло"
  - "**побеждава Slumbot - най-силният публично достъпен бот за хедс-ъп безлимит покер**" → "**побеждава Slumbot - най-силния публично достъпен бот за хедс-ъп безлимит покер**"
- **Why:** English plural "-s"; algorithm names stay Latin; one spelling per term; apposition to a direct object takes the short article.

## T — Glossary-level terminology

### F06b-T01 · S1 · "multiplayer → многопотребителски" (and derived entries)
- **Where:** `llmPipeline/glossary_settled.md`: "multiplayer → многопотребителски", "multiplayer setting → многопотребителска среда", "multiplayer imperfect-information games → многопотребителски игри с непълна информация", "multiplayer opponent modeling → … многопотребителска игра", "multiplayer safety gap → многопотребителска безопасна разлика", "multiplayer safety → безопасност в мултиплейър среда", "multiplayer symmetric games → многоигрални симетрични игри". Printed in step 06 (B23).
- **Now → Proposed:** → "с много играчи" (adjectival: "игри с много играчи", "безопасност при много играчи"); "multiplayer safety gap" → "празнина в безопасността при много играчи".
- **Why:** "многопотребителски" means multi-user (software); "мултиплейър" is gaming slang; "безопасна разлика" means "a safe difference". C2 is about exactly this concept, so the entries will recur in chapters 8–11 and in Chapter I.

### F06b-T02 · S1 · "two-player → двуигрови"
- **Where:** glossary_settled.md "two-player → двуигрови" (freq 1, but "двуигров…" occurs in the summaries of steps 02 (2), 05 (1), 06 (19), 08 (2), 09 (3), 11 (1)).
- **Now → Proposed:** → "за двама играчи" ("игра за двама с нулева сума", which is already the entry for *two-player zero-sum*).
- **Why:** "двуигров" suggests "of two games" and is not a Bulgarian word; the entry contradicts its own *two-player zero-sum* entry.

### F06b-T03 · S1 · *sound* family: "звуково", "правилно", "надежден", "коректен"
- **Where:** glossary_settled.md: "sound-search framework → рамка за звуково търсене", "sound self-play → правилно самообучение" (freq 3), "sound algorithm → надежден алгоритъм", "soundness → коректност" (and 6 derived "коректност" entries).
- **Now → Proposed:** sound → "коректен"; sound search → "коректно търсене"; sound self-play → "коректна самоигра"; sound algorithm → "коректен алгоритъм".
- **Why:** Four renderings of one technical property, one of them acoustic (B22). SoG defines *sound* via consistency between searches (Materials and Methods, "Data Generation via Sound Self-play").

### F06b-T04 · S1 · "opponent-blindness → невидимост за противника"; "opponent-blind → независим от противника"
- **Now → Proposed:** → "„слепота“ за противника"; → "„сляп“ за противника"
- **Why:** The first says the system is invisible to the opponent, the opposite of the intended meaning; this is the central framing of §1.3 ("none of the landmark systems adapts to its opponents"), so the term will recur (B24).

### F06b-T05 · S1 · "in expectation → в очакване"
- **Now → Proposed:** → "по математическо очакване" / "средно"
- **Why:** "в очакване" means "while waiting" (B10). The phrase recurs in any chapter that states expected-value guarantees (safe exploitation, chapter 8).

### F06b-T06 · S2 · "self-play → самообучение" (freq 43)
- **Where:** glossary_settled.md; summaries of steps 05 (7), 06 (33), 08, 09, 10 (8), 11, 12.
- **Now → Proposed:** → "самоигра" (игра срещу копия на самия себе си); "self-play reinforcement learning" → "обучение с подкрепление чрез самоигра".
- **Why:** "самообучение" is "self-learning / self-study" and produces "обучение чрез самообучение" (B28). Chapter 6 already uses "самоигра" 7 times.

### F06b-T07 · S2 · "public belief state → общодостъпно състояние на вярванията"
- **Where:** glossary_settled.md (freq 15) next to "belief state → състояние на убеждението", "public belief states and decomposition → публични убеждения и разлагане".
- **Now → Proposed:** → "публично състояние на убежденията (PBS)"
- **Why:** It must pair with "публично състояние" (*public state*) and with "убеждение" (*belief*) used everywhere else; five variants print in chapter 6 (B29) and in fig. 30.

### F06b-T08 · S2 · "prior policy → предходна стратегия"
- **Now → Proposed:** → "априорна стратегия"
- **Why:** "предходна" means "previous" (B19). Consistent with F07-T04 (prior → априорно разпределение).

### F06b-T09 · S2 · "leaf → възел", "leaf evaluator → оценител на възел", "leaf nodes → възли листа"
- **Now → Proposed:** → "листо"; → "оценител на листата"; → "листа"
- **Why:** A leaf is a specific node; depth-limited search is defined by what happens at leaves (B30).

### F06b-T10 · S2 · "anytime search → търсене по всяко време", "anytime → по всяко време"
- **Now → Proposed:** → "търсене с възможност за прекъсване във всеки момент (anytime)"; short form "прекъсваемо търсене"
- **Why:** B31.

### F06b-T11 · S2 · "test-time compute → тест-тайм изчислителна мощност" (freq 5)
- **Now → Proposed:** → "изчисления по време на изпълнение (test-time compute)"
- **Why:** English transliteration plus the "мощност" error of F07-T12.

### F06b-T12 · S2 · "offline → извън линия" vs "offline phase → офлайн фаза"
- **Now → Proposed:** → "офлайн" / "предварително" (offline precomputation → "предварително изчисление", which is already an entry)
- **Why:** Two renderings; "извън линия" is a calque (B53, fig. 29 lane label).

### F06b-T13 · S2 · names translated in the glossary and the figure mapping
- **Where:** glossary_settled.md: "Player of Games → играч на игри", "liar's dice → Лъжливи зарове", "recon blind chess → слепец шах с разузнаване"; `figure_labels.json`: 'Student of\nGames' → 'Студент по\nИгри'.
- **Now → Proposed:** identity for all four (Player of Games, Liar's Dice, Reconnaissance Blind Chess, Student of Games), marked as names.
- **Why:** Brief rule: system names stay in Latin script; the candidate asked the same for Libratus (Aug comments, TOC p. 5). Scotland Yard is already kept (B15, G04, G05).

### F06b-T14 · S2 · "milli-big-blinds per game → мили-големи блайнда на игра" (freq 3); "hands → раздаване" vs text "ръце"
- **Now → Proposed:** → "хилядни от големия блайнд на раздаване (mbb/g)"; played hands → "раздавания" (cards held stay "ръка")
- **Why:** B50. The unit is defined once per chapter and reused, so the entry fixes several chapters (05, 06, 08).

## C — Content

### F06b-C01 · S1 · SoG exploitability bound: *A* should be √*A*
- **Where:** summaryEn.md l. 1243 and summaryBg.md l. 452 (the displayed formula); Synthesis bullet EN l. 1512, BG l. 538 ("SoG's $|\mathcal{F}|\epsilon + |\mathcal{N}|UA/\sqrt{T}$").
- **Problem:** SoG Theorem 1 (Materials and Methods, "Performance Guarantees for Continual Re-solving", read in arXiv:2112.03178v2) bounds the regret by $\sum_{t=1}^{T}|F(L^t)|\epsilon + \sum_{s_{pub}\in N(L^T)}|S_i(s_{pub})|\,U\sqrt{AT}$; Theorem 2 has $(5D+2)(F\epsilon + NU\sqrt{A/T})$. Dividing by $T$ gives $|\mathcal{N}|U\sqrt{A}/\sqrt{T}$, not $|\mathcal{N}|UA/\sqrt{T}$. The error comes from `research/student_of_games.md` ("U·A·√T").
- **Now → Proposed:** EN formula "\underbrace{\frac{|\mathcal{N}|\,U\!A}{\sqrt{T}}}" → "\underbrace{\frac{|\mathcal{N}|\,U\sqrt{A}}{\sqrt{T}}}" (BG: in F06b-B04); EN l. 1245 "with $|\mathcal{F}|$ and $|\mathcal{N}|$ the frontier and interior sizes" → "with $|\mathcal{F}|$ the frontier size and $|\mathcal{N}|$ the number of information states in the interior"; Synthesis EN: "$|\mathcal{F}|\epsilon + |\mathcal{N}|UA/\sqrt{T}$" → "$|\mathcal{F}|\epsilon + |\mathcal{N}|U\sqrt{A}/\sqrt{T}$" (BG in C11).

### F06b-C02 · S2 · "mid-training AlphaZero" is wrong
- **Where:** summaryEn.md l. 1268 "against a mid-training AlphaZero"; summaryBg.md "срещу AlphaZero в средна фаза на обучение".
- **Problem:** The 2/400 result is against AlphaZero(s=8000, t=800k), i.e. AlphaZero after its full 800k training steps, searching 8,000 simulations (SoG Results and Table 1).
- **Now → Proposed:** "срещу AlphaZero в средна фаза на обучение" → "срещу напълно обучен AlphaZero с 8000 симулации на ход"; EN "against a mid-training AlphaZero" → "against a fully trained AlphaZero searching 8,000 simulations per move".

### F06b-C03 · S2 · Overclaim: "first provably sound across both classes", "the one guarantee that spans both"
- **Where:** summaryBg.md — "Това е първият алгоритъм, който е *доказуемо коректен както за игри с пълна, така и за игри с непълна информация* (Теореми 1–2)" and "това е единствената гаранция за коректност, която обхваща и двата класа"; EN l. 1326–1327 and l. 1251–1252.
- **Problem:** ReBeL "provably converges to a Nash equilibrium in any two-player zero-sum game" (abstract), perfect-information ones included, and "reduces to an algorithm similar to AlphaZero" there. The published SoG abstract makes no "first" claim; the "first" in the 2021 *Player of Games* abstract ("the first algorithm to achieve strong empirical performance in large perfect and imperfect information games", arXiv v1) was dropped from the *Science Advances* version. What SoG can claim is soundness for both classes *plus* evaluation on both.
- **Now → Proposed:**
  - "Това е първият алгоритъм, който е *доказуемо коректен както за игри с пълна, така и за игри с непълна информация* (Теореми 1–2)" → "Той е *доказуемо коректен както за игри с пълна, така и за игри с непълна информация* (Теореми 1–2) и е проверен експериментално и в двата класа"; EN "It is the first algorithm to be *provably sound across both perfect- and imperfect-information games* (Theorems 1–2)" → "It is *provably sound for both perfect- and imperfect-information games* (Theorems 1–2) and is evaluated on both classes"
  - "това е единствената гаранция за коректност, която обхваща и двата класа" → "така една и съща гаранция обхваща и двата класа"; EN "it is the one soundness guarantee that spans both classes" → "one guarantee covers both classes".

### F06b-C04 · S2 · "the algorithm has been run with more players" is unsupported
- **Where:** summaryBg.md — "Макар алгоритъмът да е изпълняван и с повече играчи, теорията не го обхваща в тези случаи - „2 играча“ в оценката се отнася до *гаранцията*, а не до кода." and the table row "алгоритъмът се обобщава за повече играчи, но **без** гаранциите"; EN l. 1043–1044 and l. 844.
- **Problem:** ReBeL was never run with more than two players: its notation is written for N agents (§3), every experiment is two-player ("Liar's Dice is a two-player zero-sum game in our experiments", App. C), and "ReBeL's theoretical guarantees are also limited only to two-player zero-sum games" (§9). The multiplayer evidence in the research notes is Pluribus's, not ReBeL's.
- **Now → Proposed:** "Макар алгоритъмът да е изпълняван и с повече играчи, теорията не го обхваща в тези случаи - „2 играча“ в оценката се отнася до *гаранцията*, а не до кода." → "Формализмът на статията е записан за N играчи, но всички експерименти и гаранции са за двама – „2 играча“ в таблицата „С един поглед“ се отнася до *гаранцията*, а не до формализма."; "алгоритъмът се обобщава за повече играчи, но **без** гаранциите" → "формализмът е за N играчи, но гаранциите и експериментите са само за двама"; EN: "although the algorithm has been run with more players, the theory does not follow it there — the scorecard's "2 players" is a statement about the *guarantee*, not the code" → "the paper's notation is written for N agents, but every experiment and guarantee is two-player — the scorecard's "2 players" is a statement about the *guarantee*, not the formalism"; l. 844 "the algorithm generalizes to more players but **without** the guarantees" → "the formalism is N-player, but guarantees and experiments are two-player only".

### F06b-C05 · S2 · "Opponent-blind" framing overstates what the sources say
- **Where:** summaryBg.md § "Защо това е важно…" — "всяка изчислява най-лошосценарийна устойчива стратегия и я играе безусловно, а двете многопотребителски и тествани с хора системи правят тази позиция явна - те отказват да моделират или да се адаптират към противниците си, за да не бъдат контраексплоатирани, а Pluribus дори не знае срещу кого играе."; EN l. 1464–1466.
- **Problem:** Only Pluribus makes the stance explicit. Its paper: "Pluribus plays a fixed strategy that does not adapt to the observed tendencies of the opponents", "does not know the identity of its opponents", and shifting to an exploitative strategy "opens oneself up to exploitation" (Brown & Sandholm 2019, pp. 1 and 5, full text). "The two multiplayer- and human-tested systems" is wrong (only one is multiplayer), and Libratus does not play its strategy "unconditionally": its self-improver "uses the opponents' actual moves to suggest where in the game tree such filling is worthwhile" (Libratus paper). `lit_gaps.md` recommends "none of the landmark superhuman systems adapts to its opponents".
- **Now → Proposed:** "всяка изчислява най-лошосценарийна устойчива стратегия и я играе безусловно, а двете многопотребителски и тествани с хора системи правят тази позиция явна - те отказват да моделират или да се адаптират към противниците си, за да не бъдат контраексплоатирани, а Pluribus дори не знае срещу кого играе." → "всяка изчислява стратегия, устойчива в най-лошия случай (приближение на равновесие), и не я адаптира към конкретния противник. Статията за Pluribus го казва изрично: системата „играе фиксирана стратегия, която не се адаптира към наблюдаваните тенденции на противниците“, не знае кои са противниците ѝ, а отклонението към експлоатираща стратегия се отхвърля, защото прави самата система уязвима за експлоатация.[^pluribus]"; EN: "each computes a worst-case-robust strategy and plays it unconditionally, and the two multiplayer- and human-tested systems make the stance explicit — they refuse to model or adapt to opponents so as never to be counter-exploited, and Pluribus does not even know who it is playing" → "each computes a worst-case-robust (approximately equilibrium) strategy and does not adapt it to the particular opponent. The Pluribus paper says so explicitly: Pluribus "plays a fixed strategy that does not adapt to the observed tendencies of the opponents", does not know who its opponents are, and exploitative deviation is rejected because it "opens oneself up to exploitation".[^pluribus]"

### F06b-C06 · S2 · Concessions attributed to both Pluribus and SoG that only Pluribus makes
- **Where:** summaryBg.md — "Pluribus и Student of Games и двете ограничават своите гаранции до игра за двама с нулева сума и признават, че извън нея равновесието на Наш нито е уникално, нито може да бъде изчислено ефективно, нито дори представлява гаранция срещу загуба."; EN l. 1489–1491; SoG table (l. 414) "но равновесието на Наш е „по-малко смислено“ извън 2p0s".
- **Problem:** The three points (non-uniqueness via the Lemonade Stand game, PPAD-hardness, independently chosen equilibria may not form an equilibrium) are in the Pluribus paper, which has no guarantees to "restrict". SoG says only that "the theoretical guarantee of Nash equilibria outside of this setting is less meaningful and it is unclear how effective they would be" (Background).
- **Now → Proposed:** "Pluribus и Student of Games и двете ограничават своите гаранции до игра за двама с нулева сума и признават, че извън нея равновесието на Наш нито е уникално, нито може да бъде изчислено ефективно, нито дори представлява гаранция срещу загуба." → "Статията за Pluribus посочва, че при повече от двама играчи равновесията на Наш не са единствени, намирането им е изчислително трудно, а независимо избрани равновесни стратегии може да не образуват равновесие – т.е. равновесната игра не гарантира, че играчът няма да загуби;[^pluribus] Student of Games ограничава гаранциите си до игри за двама с нулева сума, защото извън тях гаранцията на равновесието е „по-малко смислена“.[^sog]"; "но равновесието на Наш е „по-малко смислено“ извън 2p0s" → "но извън 2p0s гаранцията на равновесието на Наш е „по-малко смислена“". EN analogous: "Pluribus's paper argues that beyond two-player zero-sum a Nash equilibrium is neither unique nor efficiently computable, and that independently chosen equilibrium strategies need not form an equilibrium, so equilibrium play guarantees nothing;[^pluribus] Student of Games restricts its guarantees to two-player zero-sum play because there the guarantee is "less meaningful".[^sog]"

### F06b-C07 · S2 · Stale hand-off: Chapters 7–15, Phases D–G, the ReBeL-Lite task, "Chapter 8 takes up directly"
- **Where:** summaryBg.md lines 343, 539, 540, 546, 548, 550; EN l. 912 is correct ("chapters"), l. 1517–1518, 1522, 1538, 1550, 1554–1557; fig. 30 and its alt text (G01, G05).
- **Problem:** Chapters 13–15 were never written; "Phase D/E/F/G" are planning labels never defined in the bundle; the "ReBeL-Lite-on-Leduc task" was planned (`planning/rawSteps/step_06…`, `deliverables/studyPlan/en/04_phase_c.md`) but never implemented (`implementation/` has no step06); Chapter 8 only cites Milec et al. (2025) in a footnote and works with local subgame safety, so it does not "take up directly" adaptation beyond the depth limit.
- **Now → Proposed:**
  - "### Нерешени проблеми и предаването към глави 7–15" → "### Нерешени проблеми и връзка с глави 7–12"; EN "### Open problems and the hand-off to Chapters 7–15" → "### Open problems and the hand-off to Chapters 7–12"
  - "Тези проблеми определят фаза D (глави 7–8), критичното ядро на дисертацията, и се разклоняват през следващите фази - динамика на многоагентни системи и формиране на коалиции (фаза E), поведенчески конвейери, задвижвани от данни, които основават моделите върху реални следи (фаза F), и рамката за междудоменна оценяване, която затваря плана (фаза G)." → "Тези проблеми са в основата на глави 7 и 8 – ядрото на дисертацията – и се развиват в следващите глави: многоагентно обучение, популации и образуване на коалиции (глави 9–11) и последователностни модели и агенти с големи езикови модели (глава 12); междудомейнната рамка за оценяване остава за бъдеща работа."; EN l. 1554–1557 analogous.
  - "- точният проблем, който глава 8 „адаптиране отвъд границата на дълбочината“ разглежда." → "- точно проблемът, с който се занимават Milec и др. (2025), цитирани в глава 8."; EN "— the exact problem Chapter 8's "adapting beyond the depth limit" takes up" → "— the problem Milec et al. (2025), cited in Chapter 8, take up"
  - "е нерешен проблем, който глава 8 разглежда пряко" → "е нерешен проблем; глава 8 само го очертава чрез работата на Milec и др. (2025)"; EN "an unsolved problem Chapter 8 takes up directly" → "an unsolved problem; Chapter 8 only points to it (Milec et al., 2025)"
  - "Подразделите „Изчислителна мощ и достъпност“ сортират областта на това, което е възпроизводимо в мащаба на докторска дисертация (Single-Server CFR на Pluribus, CPU решавач с един поток на ReBeL, отворената OpenSpiel среда, малки игри) спрямо това, което е само за цитиране (свръхкомпютърът на Libratus, TPU басейнът на SoG) - неявната обосновка за изграждане върху евтината, отворена линия (задачата reBeL-Lite-on-Ледюк), вместо възпроизвеждане на водещ продукт." → "Подразделите „Изчислителни разходи и достъпност“ разделят областта на възпроизводимото в мащаба на една докторантура (CFR на Pluribus върху един сървър, еднонишковият CPU решавач на ReBeL, отворената среда OpenSpiel, малките игри) и на онова, което може само да се цитира (суперкомпютърът на Libratus, TPU клъстерът на SoG) – неявна обосновка да се надгражда евтината и отворена линия, вместо да се възпроизвежда някоя от водещите системи."; EN: drop "(the ReBeL-Lite-on-Leduc task)".
  - l. 343 "по-ранните стъпки": in B45; l. 548 "по-късна стъпка": in B25.

### F06b-C08 · S2 · "six orders of magnitude" is unsupported
- **Where:** summaryBg.md — "разходите на системите варират в шест порядъка"; EN l. 1551.
- **Problem:** The chapter's own figures give ≈12,400 core-hours for Pluribus's blueprint and ≈25 million core-hours for Libratus (≈3.3 orders of magnitude); ReBeL and SoG are reported in GPU/TPU units that cannot be put on the same scale.
- **Now → Proposed:** "разходите на системите варират в шест порядъка" → "разходите на системите се различават с няколко порядъка"; EN "range over six orders of magnitude" → "differ by several orders of magnitude".

### F06b-C09 · S2 · piKL analogy: wrong anchor and a misdescribed SoG constraint
- **Where:** summaryBg.md l. 543 — "„Правилното самообучение“ на Student of Games изисква всяко локално търсене да остане *в съответствие* с безопасна референция, концептуално същото ограничение като регулираната с КЛ-дивергенция (PiKL) експлоатация, която Принос 2 ще използва - аналогия, която си струва да бъде заета."; EN l. 1531–1533.
- **Problem:** (1) SoG's sound self-play requires searches to be consistent "with both the CVPN … and with searches made at previous public states along the same trajectory" (Materials and Methods), not with a "safe reference". (2) `lit_gaps.md` Correction 2: in piKL the anchor is a human imitation policy and gives no worst-case guarantee [Jacob 2022; Bakhtin 2023]; KL-anchoring an exploiting policy to a blueprint is the thesis's own proposal. (3) "КЛ" breaks the Latin-abbreviation rule (F07-T11); the method is "piKL", not "PiKL".
- **Now → Proposed:** "„Правилното самообучение“ на Student of Games изисква всяко локално търсене да остане *в съответствие* с безопасна референция, концептуално същото ограничение като регулираната с КЛ-дивергенция (PiKL) експлоатация, която Принос 2 ще използва - аналогия, която си струва да бъде заета." → "„Коректната самоигра“ на Student of Games изисква всяко локално търсене да е съгласувано с мрежата за стойности и с предишните търсения по същата траектория.[^sog] Това напомня предлаганото в Принос 2 закотвяне на експлоатиращата стратегия към безопасна базова стратегия чрез KL-регуларизация. Такова закотвяне е собствено предложение на дисертацията: в piKL котвата е стратегия, имитираща човешка игра, и регуларизацията не дава гаранция за най-лошия случай."; EN analogous.

### F06b-C10 · S2 · Draft editorial note printed in the bundle
- **Where:** summaryBg.md — "*По-нататъшни опорни точки (кандидат - за запазване или премахване според крайната дължина).* Следните са компактни екстраполации, а не твърдения, вече направени от системите; всяко представлява едноредово **начално число** за по-късни глави." (p. 129); EN l. 1507–1508.
- **Problem:** A note to the author ("candidate — to keep or trim against final length") prints in the published chapter.
- **Now → Proposed:** decide now; if kept: → "*По-нататъшни опорни точки.* Следващите бележки са кратки екстраполации, а не твърдения на самите системи; всяка е идея в един ред, която следващите глави могат да развият." EN: "*Further leverage points.* The following are compact extrapolations rather than claims made by the systems; each is a one-line idea for later chapters."

### F06b-C11 · S3 · "Every guarantee has the same form" contradicted by its own list
- **Where:** summaryBg.md l. 538 — "Всяка гаранция в главата има една и съща форма - термин за приближение на стойността плюс $1/\sqrt{T}$ термин за сходимост (DeepStack's $k_1\epsilon + k_2/\sqrt{T}$, Libratus's $2\Delta$, ReBeL's $\delta C_1 + \delta C_2/\sqrt{T}$, SoG's $|\mathcal{F}|\epsilon + |\mathcal{N}|UA/\sqrt{T}$)"; EN l. 1510–1512.
- **Problem:** Libratus's $2\Delta$ has no $1/\sqrt{T}$ term; SoG's term needs √A (C01); English possessives (B04).
- **Now → Proposed:** → "Гаранциите в главата имат сходна форма – член за грешката на приближението на стойността и (без Libratus) член за сходимост от вида $1/\sqrt{T}$ (DeepStack: $k_1\epsilon + k_2/\sqrt{T}$; Libratus: $2\Delta$; ReBeL: $\delta C_1 + \delta C_2/\sqrt{T}$; SoG: $|\mathcal{F}|\epsilon + |\mathcal{N}|U\sqrt{A}/\sqrt{T}$)"; EN analogous.

### F06b-C12 · S3 · "For seventy years" the two traditions ran separately
- **Where:** summaryBg.md — "В продължение на седемдесет години двете големи традиции в игровия изкуствен интелект вървяха по отделни пътища."; EN l. 1142.
- **Problem:** The CFR tradition dates from 2007; seventy years fits only the search tradition (Samuel, 1950s). SoG's introduction supports a different, defensible claim: every milestone focused on a single game.
- **Now → Proposed:** → "От програмата за игра на дама на Самюъл през 50-те години насам пробивите в изкуствения интелект за игри идваха по една игра наведнъж, а двете големи традиции се развиваха поотделно.[^sog]"; EN "Since Samuel's checkers program of the 1950s, game-AI milestones have come one game at a time, and the two great traditions ran on separate tracks.[^sog]"

### F06b-C13 · S3 · Inexact quotation; "the top" human
- **Where:** summaryBg.md l. 464 "(„$c=1$ не винаги е най-добрият в практиката … надяваме се да го проучим по-задълбочено“)"; EN l. 1291; ReBeL "топ човешкия специалист" (l. 313 in B50; l. 377).
- **Problem:** SoG's words are "c = 1 is not always the best choice in practice and hope to explore this more thoroughly in the future"; the EN quotation marks enclose altered text. ReBeL describes Dong Kim as "a top human HUNL expert that did best among the four top humans that played against Libratus" (§8), not *the* top specialist.
- **Now → Proposed:** "(„$c=1$ не винаги е най-добрият в практиката … надяваме се да го проучим по-задълбочено“)" → "(„$c = 1$ не винаги е най-добрият избор на практика“, и авторите се надяват „да проучат това по-задълбочено в бъдеще“)"; EN → "("$c = 1$ is not always the best choice in practice", which the authors "hope to explore this more thoroughly in the future")"; "побеждава топ човешкия специалист Донг Ким" → "побеждава професионалиста в хедс-ъп Донг Ким"; EN "the top human specialist Dong Kim" → "the heads-up professional Dong Kim".

### F06b-C14 · S3 · "opened the decade"
- **Where:** summaryBg.md — "DeepStack и Libratus откриха десетилетието"; EN l. 1413.
- **Problem:** 2017 does not open a decade; the chapter's span is 2017–2023.
- **Now → Proposed:** "DeepStack и Libratus откриха десетилетието" → "DeepStack и Libratus откриха този период"; EN "opened the decade" → "opened the period".

## S — Sources

### F06b-S01 · S1 · The ReBeL paper is not cited anywhere in the chapter
- **Where:** summaryEn.md / summaryBg.md footnote list (7 notes: brown2017, burch2014, deepstack, lbr, libratus, pluribus, sog). ReBeL has no note; no summary in the corpus defines one (grep).
- **Proposal (cite):** add to both files: `[^brown2020rebel]: Brown, N., Bakhtin, A., Lerer, A. & Gong, Q. (2020). "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games." *NeurIPS 33*, 17057–17069. arXiv:2007.13544.` [verified: NeurIPS proceedings BibTeX (authors, pages) + arXiv full text] and `[^bakhtin2020]: Bakhtin, A. (2020). "ReBeL: A general game-playing AI bot that excels at poker and more." Meta AI blog, 3 December 2020.` [verified: page fetched; byline and date]. First marker: "ReBeL (Brown, Bakhtin, Lerer & Gong, 2020; Facebook AI Research) прави крачка назад" → "ReBeL (Brown, Bakhtin, Lerer & Gong, 2020; Facebook AI Research)[^brown2020rebel] прави крачка назад" (EN l. 827 likewise).

### F06b-S02 · S2 · SOURCE_GAPS row "Затворената празнина" (AlphaZero paradigm unavailable); unverified "holy grail"; misplaced [^lbr]
- **Where:** summaryBg.md — "Отвореният въпрос, на който ReBeL отговаря, е този, който Ноам Браун нарича „свещеният граал“ на областта: **може ли рецептата на AlphaZero да бъде накарана да работи коректно в игри със скрита информация?**[^lbr]"; EN l. 865–866.
- **Problem:** The [^lbr] note (Lisý & Bowling, local best response) has nothing to do with the sentence. The "holy grail" attribution could not be found (web search, ReBeL paper, Meta blog, NeurIPS page).
- **Proposal (cite and soften):** → "Отвореният въпрос, на който отговаря ReBeL, е: **може ли рецептата на AlphaZero да работи коректно в игри със скрита информация?** Дотогава алгоритмите, съчетаващи обучение с подкрепление и търсене, не са били теоретично коректни при непълна информация и не са били прилагани успешно в такива игри.[^brown2020rebel]" EN → "The open question ReBeL answers is: **can the AlphaZero recipe be made to work, soundly, in games of hidden information?** Prior RL+Search algorithms were "not theoretically sound in imperfect-information games and have not been shown to be successful in such settings".[^brown2020rebel]" Verified: ReBeL §2 (quoted) and abstract ("prior algorithms of this form cannot cope with imperfect-information games"). Move `[^lbr]` to the LBR mention in § "Силни страни и ограничения" (after "**локалния най-добър отговор (LBR)**", F06b-B49; EN "drove the local-best-response probe to a large loss").

### F06b-S03 · S2 · SOURCE_GAPS row "Архитектура" (ReBeL) — the architecture description
- **Where:** summaryBg.md § "Архитектура" (ReBeL), first paragraph ending "(Фигура 6.4)."
- **Proposal (cite):** append `[^brown2020rebel][^bakhtin2020]` after "(Фигура 6.4)." (EN l. 890 likewise). Verified: ReBeL §5 and Algorithm 1 (construct depth-limited subgame at PBS, solve with CFR using the value net at leaves, add training data, sample a leaf on a random iteration); Meta blog "AlphaZero-like" framing.

### F06b-S04 · S2 · SOURCE_GAPS row "Ключова иновация…" — PBS definition
- **Where:** summaryBg.md — "Recursive Belief-based Learning нарича това състояние общодостъпно състояние на убеждението: формално, **съвместно разпределение на вероятностите** върху възможните информационни състояния на играчите, дадено общите публични наблюдения."
- **Proposal (cite):** append `[^brown2020rebel]` after the sentence. Verified in ReBeL §4: "In general terms, a PBS is described by a joint probability distribution over the agents' possible infostates"; the referee example and "these two games are strategically identical" are also in §4 (and the Meta blog). EN l. 928–929 likewise. Also add to "(тя датира от работата върху кооперативни POMDPs)" the paper's wording: the concept "originated in work on decentralized multi-agent POMDPs" (§2).

### F06b-S05 · S2 · SOURCE_GAPS row "Ограничения…" — the modified CFR-AVG caveat
- **Where:** summaryBg.md — "(„дали тази модифицирана форма на CFR-AVG е теоретично обоснована остава отворен въпрос“)"
- **Proposal (cite):** append `[^brown2020rebel]` after the closing parenthesis. Verified in ReBeL Appendix A ("List of contributions"): "in order to implement CFR-AVG efficiently, in our experiments we modify the algorithm in a way that is not theoretically sound but empirically performs well in poker. Whether or not this modified form of CFR-AVG is theoretically sound remains an open question"; Appendix I repeats it for depth-limited subgames. The EN quotation is exact.

### F06b-S06 · S2 · SOURCE_GAPS row "Изчислителна мощност и достъпност" — open vs closed source
- **Where:** summaryBg.md — "реализация беше с отворен код** (за „лъжливи зарове“), докато кодът както за Libratus, така и за Pluribus остана затворен."
- **Proposal (cite):** after "остана затворен." add `[^brown2020rebel][^libratus][^pluribus]`. Verified: ReBeL Broader Impact ("we have decided not to release the code for poker. We instead open source our implementation for Liar's Dice"; repository github.com/facebookresearch/rebel); Libratus *Science* 2018 and Pluribus *Science* 2019 data-availability statements, both: "the risk associated with releasing the code outweighs the benefits … we have included the pseudocode … in the supplementary materials". Optionally add "(и двете статии публикуват само псевдокод)".

### F06b-S07 · S2 · SOURCE_GAPS row "Силни страни…" — "first provably sound RL+search for imperfect information"
- **Where:** summaryBg.md — "Това е първият алгоритъм, който прави парадигмата RL+Search на AlphaZero *доказуемо коректна* в игри с непълна информация"; also the intro (l. 313) and table (l. 325).
- **Proposal (attribute + cite):** → "По думите на авторите това е първият алгоритъм, който прави парадигмата на AlphaZero „обучение с подкрепление + търсене“ *доказуемо коректна* в игри с непълна информация[^bakhtin2020]"; EN "It is, by its authors' account, the first algorithm to make …[^bakhtin2020]". Verified: Meta blog "ReBeL is the first AI to enable sound RL+Search in imperfect-information games"; paper App. A: "we are not aware of any prior RL+Search algorithms for two-player zero-sum games in general. We view this as the central contribution of this paper." Note that the paper cites earlier value-function learning in "limited subsets of zero-sum imperfect-information games" [29], so "first" should stay attributed.

### F06b-S08 · S2 · SOURCE_GAPS row "Наследство…" (ReBeL) — SoG as "direct descendant"; "PBS now the standard substrate"
- **Where:** summaryBg.md — "Неговият пряк наследник е **Student of Games** (2023)" and "Публичните състояния на убеждението вече са стандартният субстрат за коректно търсене в игри с непълна информация".
- **Problem:** SoG comes from the DeepStack/Alberta line (the chapter says so at l. 410); its Related Work calls ReBeL "the most closely related algorithm", not its parent. "Standard substrate" has no source.
- **Proposal (soften + cite):** → "Най-близкият му наследник е **Student of Games** (2023), чиито автори го определят като „най-близкия“ до своя алгоритъм[^sog]"; → "Публичните състояния на убежденията оттогава са в основата и на по-късните методи за коректно търсене, например Student of Games[^sog]". EN analogous. Verified: SoG Related Work ("The most closely related algorithm is … ReBeL"; "The use of public belief states and decomposition … has been a critical component of success in no-limit Texas Hold'em poker").

### F06b-S09 · S2 · SOURCE_GAPS row "Архитектура" (SoG) — representation inherited from ReBeL
- **Where:** summaryBg.md l. 438 (the sentence rewritten in B01).
- **Proposal (cite):** append `[^sog]` after the B01 sentence. Verified: SoG Background (public belief state β = (s_pub, r), range = pair of distributions over information states) and Related Work (above). Replace the `[^deepstack]` marker at the end of the paragraph ("всяко търсене съгласувано с всяко друго.[^deepstack]") by `[^sog]`: the sentence describes SoG's sound self-play, and the repeated DeepStack note prints 40 pages earlier (p. 79).

### F06b-S10 · S2 · SOURCE_GAPS row "Изчислителна мощност…" (SoG) — 3500 TPUv4 / 800,000 steps; misplaced [^pluribus]
- **Where:** summaryBg.md — "Базовата линия на AlphaZero използва 3500 едновременни изпълнители, всеки на един Google TPUv4, в продължение на 800,000 стъпки на обучение, а Student of Games „е обучен с подобно количество изчислителна мощност TPU“"; paragraph ends "силните конфигурации също не са евтини.[^pluribus]".
- **Proposal (cite):** append `[^sog]` after the quoted "…TPU ресурси“" (B32). Verified in SoG "Results in Challenge Domains": "We trained a version of AlphaZero using its original settings … with 3500 concurrent actors each on a single TPUv4, for a total of 800k training steps. SOG was trained using a similar amount of TPU resources"; steps: chess 3M, Go 1M, poker ≤1.1M, Scotland Yard 17M. The numbers describe the AlphaZero re-run, and the text says so correctly; Chapter I must not write "SoG used 3500 TPUs". Move `[^pluribus]` to "от рода на тази, с която Pluribus стана известен" (the only Pluribus fact in the paragraph). Schmid's "on a few GPUs" / "by far the hardest": see S16.

### F06b-S11 · S2 · SOURCE_GAPS row "Силни страни…" (SoG) — weaker than the specialists in Go
- **Where:** summaryBg.md — "Той е **по-слаб от специалистите** в техните собствени области - особено забележимо в Го - признатата цена за един алгоритъм за всичко."
- **Proposal (cite):** append `[^sog]` after "за всичко.". Verified: SoG Results ("In both cases, SOG is weaker than AlphaZero, with the gap being smaller in chess … the price of SOG's generality"; Table 1: SoG(16k) +1970 vs AlphaZero(8k) +2875 Elo in Go; 2/400 wins) and Discussion ("can be substantially weaker in head-to-head play than specialized algorithms … like AlphaZero, when given the same resources").

### F06b-S12 · S3 · SOURCE_GAPS row "Наследство…" (SoG) — "the capstone of this chapter's argument"
- **Where:** summaryBg.md — "Student of Games е завършекът на аргумента в тази глава и обединява трите ѝ сюжетни линии едновременно."
- **Proposal (keep):** no citation needed: it is the chapter's own synthesis, not a factual claim. The facts it rests on are cited in S09–S11.

### F06b-S13 · S2 · SOURCE_GAPS row "Дъгата в едно четене" — DeepStack and Libratus from opposite directions
- **Where:** summaryBg.md — "DeepStack изостави парадигмата и я замени с научени стойности и продължително пререшаване, докато Libratus я запази и добави доказуемо безопасна корекция в реално време. И двете системи останаха двуигрови и нито една от тях не съобщи за резултата на другата"
- **Proposal (cite):** after "в реално време." add `[^deepstack][^libratus]`; after "резултата на другата" add `[^brown2020rebel]` and clarify: "…и нито една не съобщи резултат по основната метрика на другата (DeepStack – само срещу LBR, Libratus – само срещу ботове и хора)". Verified: Libratus paper ("This technique comes with a provable safety guarantee"; blueprint + subgame solving + self-improver); ReBeL Table 1 lists DeepStack only against LBR (383 ± 112) and Libratus only against BabyTartanian8 (63 ± 14) and humans (147 ± 39). The DeepStack side relies on the other reviewer's verification of the DeepStack paper.

### F06b-S14 · S2 · SOURCE_GAPS row "Нерешени проблеми…" — "Pluribus proved … no safety guarantee at all"
- **Where:** summaryBg.md — "Pluribus доказа, че методите „**търсене по Наш и търсене**“ *печелят* в N-играч игри с **непълна информация**, без да предлагат никаква **гаранция за безопасност**"
- **Proposal (soften + cite):** → "Pluribus показа, че методите, съчетаващи самоигра и търсене, *печелят* в игри с N играчи и **непълна информация**, макар да нямат известни теоретични гаранции извън игрите за двама с нулева сума[^pluribus]"; EN "Pluribus proved that Nash-and-search methods *win* in N-player imperfect-information games while offering no safety guarantee at all" → "Pluribus showed that self-play-plus-search methods *win* in N-player imperfect-information games although they have no known theoretical guarantees outside two-player zero-sum games[^pluribus]". Verified in the Pluribus paper: the algorithms "are not guaranteed to converge to a Nash equilibrium outside of two-player zero-sum games"; "despite the lack of known strong theoretical guarantees on performance in multiplayer games". "Nash-and-search" is inaccurate (Pluribus does not compute a Nash equilibrium); "доказа" overstates an empirical result; "търсене по Наш и търсене" is a mistranslation (settled entry "nash-and-search").

### F06b-S15 · S2 · Misplaced [^brown2017] on the SoG capstone sentence
- **Where:** summaryBg.md — "четири много различни игри.[^brown2017]"; EN l. 1361.
- **Problem:** Safe and nested subgame solving has nothing to do with the sentence; in the bundle the marker (25, p. 123) points to a note printed on p. 41 (chapter 3).
- **Proposal (correct):** "четири много различни игри.[^brown2017]" → "четири много различни игри.[^sog]"

### F06b-S16 · S2 · Quotations from the Schmid interview are uncited
- **Where:** summaryBg.md lines 410 („AlphaZero и DeepStack в един голям унифициран алгоритъм“), 444, 460 („по-добър от хората“), 462 („се разпада“, „зад линията на AlphaZero“), 468 („на няколко GPU“, „безспорно най-трудното“); EN l. 1113–1114, 1204, 1273, 1279, 1283, 1304–1305.
- **Problem:** Six quotations come from Y. Kilcher's video interview with M. Schmid (per `research/student_of_games.md`); the chapter gives no source. Existence verified (YouTube oEmbed: "Player of Games: All the games, one algorithm! (w/ author Martin Schmid)", channel Yannic Kilcher); the quotations themselves were **not** checked against the audio.
- **Proposal (cite, or drop the quotation marks):** add `[^kilcher2022]: Kilcher, Y. (2022). "Player of Games: All the games, one algorithm! (w/ author Martin Schmid)." Video interview, YouTube, https://www.youtube.com/watch?v=U0mxx7AoNz0.` and attach it to the first quotation (l. 410). Where the paper says the same thing, cite the paper instead: "prohibitively expensive in some games" is SoG's Discussion, not the interview.

### F06b-S17 · S2 · "Test-time compute" attributed to Noam Brown for all five systems
- **Where:** summaryBg.md l. 383 ("която Ноам Браун посочва като ранен, конкретен пример за **изчислителна мощност във време на тестване**") and l. 542 ("И петте системи вече са цитирани като ранни инстанции на „изчислителна мощ по време на тест“"); EN l. 1063–1066, 1527–1530.
- **Problem:** The only source named in the research notes (Sequoia "Training Data" podcast, 22 Sep 2024) was fetched: its transcript mentions poker only as the reason MCTS "doesn't work in a game like poker" and does not present DeepStack/Libratus/Pluribus/ReBeL as test-time-compute instances; Brown's X post on the topic could not be read (HTTP 402). "All five systems are now cited as early instances" (SoG and DeepStack included) has no source at all.
- **Proposal (soften):** l. 383: "- която Ноам Браун посочва като ранен, конкретен пример за" → "- която днес често се представя като ранен пример за"; l. 542: "И петте системи вече са цитирани като ранни инстанции на „изчислителна мощ по време на тест“" → "И петте системи могат да се разглеждат като ранни примери за „изчисления по време на изпълнение“ (test-time compute)"; EN: "that Noam Brown points to as an early, concrete instance of" → "that is now often presented as an early instance of"; "All five systems are now cited as early instances of" → "All five systems can be read as early instances of". The same attribution in the Pluribus section is SOURCE_GAPS row 66 (other reviewer).

### F06b-S18 · S2 · Depth-limited solving (Brown, Sandholm & Amos 2018) is never cited
- **Where:** summaryBg.md — "Pluribus беше закърпил симптома със стратегии за продължение по избор на листата" (ReBeL gap); "**ограничено по дълбочина решаване**" in § "Какво се пренася напред"; the "Многозначните листа на Pluribus" bullet; fig. 29 note.
- **Proposal (cite):** add `[^brown2018dls]: Brown, N., Sandholm, T. & Amos, B. (2018). "Depth-Limited Solving for Imperfect-Information Games." *NeurIPS 31*. arXiv:1805.08195.` [verified: arXiv metadata and full text; NeurIPS 2018 proceedings BibTeX] after "по избор на листата". It is the source of the multi-valued-leaf idea and of the statement that "states do not have well-defined values" in imperfect-information games (abstract), which is the crux of the ReBeL gap paragraph. Note for the other reviewer: the DeepStack legacy section attributes it to "Brown & Sandholm" only; the paper has three authors.

### F06b-S19 · S3 · CICERO named without a source
- **Where:** summaryBg.md lines 383, 482 (**CICERO** (2022), "играча на Diplomacy на Meta").
- **Proposal (cite):** add `[^cicero2022]: Meta Fundamental AI Research Diplomacy Team (FAIR), Bakhtin, A., Brown, N., Dinan, E. et al. (2022). "Human-level play in the game of Diplomacy by combining language models with strategic reasoning." *Science*, 378(6624), 1067–1074. DOI 10.1126/science.ade9097.` [verified: Crossref] at the first mention (l. 383).

### F06b-S20 · S3 · Footnote metadata (spot-check)
- **Where:** footnotes `sog`, `brown2017`, `pluribus`, `lbr`.
- **Findings:** `sog` checked correct but incomplete: add ", eadg3256. DOI 10.1126/sciadv.adg3256 (arXiv:2112.03178, first posted in 2021 as "Player of Games")" [verified: Crossref, arXiv journal-ref]. `brown2017` correct (Brown & Sandholm, arXiv:1705.02955, NeurIPS 2017; add "*NeurIPS 30*"). `pluribus` correct (365(6456), 885–890, Crossref). `lbr` correct (arXiv:1612.07547, AAAI-17 workshop; `lit_evaluation.md`). All key numbers of these sections were checked against the primary texts: ReBeL 45 ± 5 / 9 ± 4 / 881 ± 94 / 165 ± 69, 7,500 hands, 90 DGX-1 × 8 V100, 1,750 epochs, 6 × 1536, < 2 s per hand / ≤ 5 s per decision, Theorem 3 bound $\delta C_1 + \delta C_2/\sqrt{T}$, 156-dimensional action example; SoG +7 ± 3 vs Slumbot, +434 ± 9 vs LBR, 2/400 vs AlphaZero, > 1100 Elo over Pachi, 55 % vs PimBot at 10M simulations, 24 rounds, $(5D+2)$, $O(kT^2)$ / $O(T)$, "only informally", "exponential memory", 20,000 → 4–5 actions. The ± in ReBeL Table 1 is one standard deviation ("The ± shows one standard deviation"), while App. E.1 calls the 165 ± 69 "one standard error"; the chapter gives no ± and is unaffected.

## X — Structure

### F06b-X01 · S2 · Figure cross-references do not match the printed numbers
- **Where:** summaryBg.md "(Фигура 6.4)" (l. 337), "(Фигура 6.5)" (l. 434), "(Фигура 2)" (l. 365); EN l. 890, 1172, 984.
- **Problem:** The bundle numbers figures consecutively: ReBeL is "Фигура 27" and SoG "Фигура 28" (pp. 108, 117). "(Фигура 2)" refers to the ReBeL paper's figure but reads as the bundle's figure 2 (chapter 1).
- **Fix:** "(Фигура 6.4)" → "(фиг. 27)", "(Фигура 6.5)" → "(фиг. 28)" — better via pandoc-crossref labels so the numbers follow the build; "(Фигура 2)" → "(фиг. 2 в статията)". EN likewise.

### F06b-X02 · S3 · Table 14 wastes a third of its width on the first column
- **Where:** p. 125–126, "Петте системи по ред…"; summaryBg.md l. 509 "|---|---|---|".
- **Fix:** "|---|---|---|" (the separator of this table) → "|--|-----|-----|", so the short system names get 1/6 of the width and the two text columns 5/12 each; the table then fits on fewer lines and page 125 no longer ends with a half-empty page.
