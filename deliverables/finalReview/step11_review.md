# Step 11 — final review

**Summary:** The chapter's central learning claim does not hold as written. The reward formula in the text, report and fig. 68 is the inverse of the code. The "Shapley coalition credit" carries no coalition information: the rollout value is additive, so each player's Shapley value is just its own win probability, and the proxy reduces to "own critic value minus the table mean". The coalition score also counts hostile interactions. Engine artefacts are presented as properties of So Long Sucker: ~99.5 % deadlocks, and "no negotiation phase", although SLS is a bargaining game (C01–C03). All eight figures fail in print. Three of them show something other than their caption: an all-zero "PREDICTION" matrix, one position instead of two, one population instead of two. Fig. 68 prints the inverted formula, and fig. 66 has English text overlapping a box (G). The Bulgarian has meaning errors that come from the glossary: critic → "критична стойност", pre-fix → "представка", behavioral prior → "априорен разпредел", PASS → "ПРЕЗ", {0,1} → "{0.1}", and the §11.6 heading says "раздаване". The Chapter 12/14 forward links are stale. On sources: the 1950 origin cannot be verified, since the game was published in 1964. The Nash claims now have verified sources (Brown & Sandholm 2019 full text). The piKL and spinning-top attributions are corrected. Central items (count only): " - " as a dash 43 × summary + 10 × one-pager; decimal point in 56 + 23 numbers; excess bold 74 vs 69 (one-pager 47 vs 30); shared footnote label `balduzzi2019` (F07-X01 — marker 62 on p. 214 prints no footnote text; the note sits in chapter 10).
**Counts:** S1 24 · S2 37 · S3 5   (by category: G 10 · B 20 · T 16 · C 11 · S 7 · X 2)

Conventions in this file (as in the pilot): quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md` (with `**`, `*`, `$`), so read this file as source. Proposals keep the chapter's current " - " dashes and decimal points, because those are fixed centrally. "l. N" means the line in the source file. Where two findings touch the same sentence, one of them owns the full replacement and the other points to it, so every search-and-replace segment appears only once. Printed sizes = matplotlib size × (printed width ÷ saved width). The body text is 10.9 pt, so the 75 % floor is ≈ 8.2 pt. Bundle pages are PDF page numbers 205–217 (the printed folio is one lower).

## G — Figures

### F11-G01 · S1 · Bulgarian captions for all eight figures (figs. 64–71)
- **Where:** summaryBg.md image alt text, l. 42, 46, 65, 69, 86, 102, 112, 125 (bundle pp. 207–215). Seven captions print in English (known defect). The eighth (fig. 67) is Bulgarian but wrong. Several contain content errors: "{0.1}", "Step 7", "Step-10", "lower bound", "negative for every alpha >= 0.3", and the fig. 65/67/71 captions do not describe their figures (G03, G05, G09).
- **Now → Proposed** (the captions for figs. 65, 67 and 71 assume the regenerated figures of G03/G05/G09):
  - "![The coalition detector: from the SLS move stream, placing a chip into another player's pile counts as HELP and capturing a pile counts as HARM. Accumulated into help/harm matrices and differenced into net support, a reciprocal alliance shows up as a strong mutual edge. Opponent modeling (Step 7) lifted from "what hand?" to "who is allied with whom?" (Contribution #1).]" → "![Детекторът на коалиции: в потока от ходове на SLS поставянето на жетон в купчината на друг играч се отчита като ПОМОЩ, а вземането на купчина - като ВРЕДА. От натрупаните матрици на помощта и вредата се получава нетната подкрепа, в която взаимният съюз се вижда като силна двупосочна връзка. Моделирането на противника от Глава 7 се пренася от въпроса „каква ръка има?“ към въпроса „кой с кого е в съюз?“ (Принос №1).]"
  - "![Coalition graph inferred purely from chip placement: the planted {0.1} alliance appears as a strong reciprocal help edge; cross-pair edges are neutral or hostile. The detector cleanly recovers a coalition it was never told about.]" → "![Матрица на коалиционния резултат, изведена само от поставянето на жетоните: предварително зададеният съюз между играчи 0 и 1 се вижда като силна взаимна подкрепа (10), а за останалите двойки стойностите са неутрални (0) или враждебни (-1). Детекторът разпознава коалиция, за която не е получил никаква информация.]"
  - "![Shapley credit adapted to a purely competitive game: the coalition's "value" is redefined as the PROBABILITY a coalition member wins (estimated by rollouts), and each player's Shapley value of that win-probability function is their credit. The empty core of the majority game (no stable allocation) is the structural signature of SLS coalitions - they will break.]" → "![Принос по Шапли в изцяло състезателна игра: „стойността“ на коалицията се предефинира като ВЕРОЯТНОСТТА неин член да спечели (оценена чрез симулации), а приносът на всеки играч е стойността на Шапли на тази функция. Празното ядро на играта на мнозинството (няма стабилно разпределение) илюстрира защо коалициите в SLS рано или късно се разпадат.]"
  - "![Разпределение на заслуги по Шейпли върху SLS позиции: почти равномерно между местата в симетричния случай (разпределение 0.013, след отстраняване на грешка), и изцяло концентрирано върху силната двойка в асиметричния случай [8,8,1,1]. Заслугите проследяват реалния принос, след като развръзката на двигателя бъде безпристрастна.]" → "![Принос по Шапли в две позиции на SLS: почти равен за четирите места в симетричната позиция (размах 0.013 след поправката) и изцяло съсредоточен върху силната двойка в асиметричната позиция [8, 8, 1, 1]. Приносът следва реалното предимство едва след като правилото при равенство в двигателя стане безпристрастно.]"
  - "![Coalition-aware MAPPO reward blend: the sparse winner-takes-all signal is mixed with the Shapley coalition credit by weight alpha. Measured, alpha is the dominant knob: coalitions emerge significantly only at low alpha (heavy credit weight), and every alpha >= 0.3 suppresses the signal. The cheap critic-value proxy beats the expensive counterfactual credit.]" → "![Смесване на наградите в MAPPO с отчитане на коалициите: рядката награда „победителят взема всичко“ се смесва с коалиционния принос по Шапли с тегло α (α = 1 - само рядка награда, α = 0 - само принос). Измерено: α е определящият параметър - коалиционният резултат нараства значимо само при ниско α, а при α ≥ 0.3 сигналът е потиснат. Евтиният заместител, изчислен от оценките на критика, дава по-силен ефект от по-скъпата оценка чрез симулации.]"
  - "![Paired coalition-score gap across the alpha x credit x synergy sweep (5 seeds, error bars): large and significant only in the low-alpha regime (peaking at +0.038 with the proxy at alpha=0), negative for every alpha >= 0.3. The earlier null came from measuring in the alpha=0.3 dead zone.]" → "![Сдвоена разлика в коалиционния резултат по мрежата α × вид на приноса × синергия (5 начални числа, ± една стандартна грешка): голяма и значима само при ниско α (максимум +0.038 при заместителя и α = 0); в разширената конфигурация е отрицателна при всяко α ≥ 0.3. Първоначалният нулев резултат идва от измерване в „мъртвата зона“ α = 0.3.]"
  - "![The EGTA + spinning-top pipeline for SLS: play every pair of strategies to fill a payoff tensor, project the 4-player tensor to a pairwise matchup matrix, and Hodge-decompose it into transitive (skill ladder) and cyclic (coalition counters) parts. Measured caveat: the 2-type projection likely discards 3-/4-player coalition effects, so the cyclic ratio is a lower bound.]" → "![EGTA и разлагането „пумпал“ за SLS: всяка четворка стратегии се изиграва многократно, за да се попълни тензорът на печалбите за четирима играчи; той се проецира в матрица на сблъсъците по двойки, която се разлага на транзитивна (стълба на уменията) и циклична (контрастратегии между коалициите) компонента. Уговорка: проекцията върху двойки вероятно губи коалиционните ефекти между трима и четирима играчи, затова цикличната компонента може да е подценена.]"
  - "![Spinning-top transitive/cyclic ratios: the skill-ladder pool is transitive-dominant (cyclic ~0.25-0.31), while the coalition pool is strongly cyclic (~0.57-0.69). Coalition play injects large non-transitivity, confirming the Step-10 direction while staying just under strict cyclic dominance.]" → "![Транзитивна и циклична компонента на двете популации в SLS: популацията тип „стълба на уменията“ е преобладаващо транзитивна (циклично съотношение ~0.25-0.31), а коалиционната има силна циклична компонента (~0.57-0.69), която остава под прага на строго доминиране (0.707). Посоката съвпада с прогнозата от Глава 10.]" (delete the line instead if fig. 71 is dropped, G09).
- **Fix:** replace the alt text in `summaryBg.md`. For the four `impl_*` figures, also switch the link to the `_bg` file once G03/G05/G07/G09 are rendered. The EN alt texts need the same content fixes: "Step 7" → "Chapter 7", "Step-10" → "Chapter 10", "{0,1}" stays, "lower bound" → "may be underestimated", and "negative for every alpha >= 0.3" → "negative for every alpha >= 0.3 in the scale tier".

### F11-G02 · S1 · Fig. 64 detector diagram: English HELP/HARM, "Стъпка 07", "кръстосан ръб", overflow, 6.8–7.3 pt
- **Where:** `renders/ch11/p207_f1.png`, `summary/make_sls_coalition_figure.py` → `sls_coalition_bg.png`
- **Problem:**
  1. English in the BG figure: "HELP матрица", "HARM матрица".
  2. Stale "(Стъпка 07)" in the result box (source string "Step 07").
  3. Terms: "кръстосан ръб" (a graph edge is "ребро", and *cross-pair* means "between the other pairs"); "засаден съюз" (T09); "чифт" (colloquial; the text says "двойка"); *capture* is "заграбване" in one box and "улавяне" in another.
  4. Top note: "няма отделна фаза за договаряне за моделиране" is a calque. In content it presents an engine simplification as a property of SLS (C03).
  5. Legibility (scale 0.852: 2684 px at 330 dpi → 17.6 cm): box fs 8.2–8.6 → 7.0–7.3 pt; note 8.4 → 7.2 pt; result box 8.0 → 6.8 pt.
  6. Overflow: "поставяне на чип в купчината на j" crosses both edges of the green box; "Най-силната двойка" crosses the orange box; "улавяне на купчината на j" touches both edges.
- **Fix:** `make_sls_coalition_figure.py`: every `box` fs → 10 and `note` fs → 10; `helpb`/`harmb` x 4.2 → 4.0, w 3.2 → 3.4; `coal` w 2.3 → 2.4 with a three-line label. Source strings: "Opponent modeling (Step 07)" → "Opponent modeling (Chapter 7)"; the note → "In this engine the alliance is visible only in the moves - negotiation is not modelled." Mapping (`figure_labels.json`):
  - 'HELP matrix\nplace chip into $j$\'s pile' → 'Матрица ПОМОЩ\nжетон в купчината на $j$'
  - 'HARM matrix\ncapture $j$\'s pile' → 'Матрица ВРЕДА\nвзема купчината на $j$'
  - 'SLS move stream\n(place / capture\nchips each turn)' → 'Поток от ходове в SLS\n(поставяне / вземане\nна жетони)'
  - 'Strongest pair\n$=$ coalition' → 'Най-силна\nдвойка $=$\nкоалиция'
  - new note → 'В този двигател съюзът се вижда само в ходовете - преговорите не се моделират.'
  - the result box (new key after the "Chapter 7" change) → 'ИЗМЕРЕНО: предварително зададеният съюз {0,1} е разпознат ТОЧНО - най-силна двойка {0,1}, резултат 10.0;\nнетната подкрепа за всички останали двойки е 0 или -1. Моделирането на противника (Глава 7) е пренесено\nкъм СОЦИАЛНАТА СТРУКТУРА на играта (Принос №1).'

### F11-G03 · S1 · Fig. 65 shows an all-zero "PREDICTION" matrix, not the planted alliance
- **Where:** `renders/ch11/p208_f1.png`; `summary/impl_coalition_graph.png` (= `implementation/step11/implementation/plots/coalition_graph.png`, byte-identical). Caption: "…the planted {0.1} alliance appears as a strong reciprocal help edge…"
- **Problem:**
  1. **The figure contradicts its caption.** It is a 4×4 heatmap with every cell "0.0", titled "End-of-game coalition-score matrix (PREDICTION", with a ±1e-9 colour bar. `plotting.py` (`plot_coalition_graph`) draws the coalition matrix of *one sample game of the baseline pool* (`default_baseline_pool`, seed 0), not the planted-alliance test. The planted result (`smoke_results.json` → `detector.coalition_matrix`: [0,1] = 10, [0,2] = [0,3] = −1, the rest 0) appears in no figure. It is a heatmap, not a "graph".
  2. English throughout. The title is clipped by the colour bar, and "PREDICTION" is stale.
  3. 110 ppi (550 px at 12.7 cm): soft in print.
  4. The BG caption text says "{0.1}": the translation pipeline changed the set {0,1} into a decimal number.
- **Fix:** `implementation/step11/implementation/plotting.py`: replace `plot_coalition_graph` with a function that loads `results/smoke_results.json`, `M = np.array(res["detector"]["coalition_matrix"])`, and draws `ax.imshow(M, cmap="RdBu", vmin=-10, vmax=10)`. Annotate cells with `f"{M[i,j]:.0f}"` at fontsize 11, set `ax.set_xlabel("player")` / `ax.set_ylabel("player")` at fontsize 10, use `fig.colorbar(im, ax=ax, label="mutual net support")`, drop the title, use figsize (4.4, 3.6) and save at dpi 300 directly to `deliverables/reports/step11/summary/impl_coalition_graph.png`. Mapping: 'player' → 'играч', 'mutual net support' → 'взаимна нетна подкрепа'. In `summaryBg.md` link `impl_coalition_graph_bg.png`. Caption: see G01.

### F11-G04 · S1 · Fig. 66 Shapley diagram: English core box overlaps the credit box; φ overlaps the arrow; 5.9–6.9 pt
- **Where:** `renders/ch11/p209_f1.png`, `summary/make_shapley_figure.py` → `shapley_credit_bg.png`
- **Problem:**
  1. The whole "EMPTY CORE = structural betrayal …" box is English: the mapping was rejected with "numbers changed". Its lines run past both edges of the grey box and print over the "Кредит на играч (сигнал за обучение)" box ("WILL break - / Кредит на играч …Contribution #2).": unreadable.
  2. "Coalition VALUE v(S) = P(a member of S wins) (rollout estimate)" is English (rejected: "math changed").
  3. In the orange box "$\phi_i$" is pushed left onto the arrow ("wins)ϕ_i = справедлив"), and "справедлив маргинален принос" overflows the box.
  4. "Shapley стойност" (English word order; the glossary has "стойност на Шапли"). In the note, "силен кредитен чифт 1.0" misparses *strong-pair credit* as "a strong credit pair".
  5. Content: "Shapley = ЕДИНСТВЕНОТО справедливо разпределение" (C11); "cannot anchor to a Nash/core equilibrium" (C05).
  6. Legibility (scale 0.803: 2849 px at 330 dpi): box fs 7.8–8.6 → 6.3–6.9 pt; notes 7.4–8.4 → 5.9–6.7 pt. The floor here is fs ≥ 10.2.
- **Fix:** `make_shapley_figure.py`: all `box`/`note` fs → 10.2. Move the core box to the full width at the bottom: `box(ax, 0.4, 0.2, 13.2, 2.0, …)`. Move the "MEASURED" note to `note(ax, 4.2, 3.2, …)`. Widen `credit` to x 8.4, w 3.6. Source strings: 'Coalition VALUE $v(S)$\n$= P(\\text{a member of } S \\text{ wins})$\n(rollout estimate)' → 'Coalition VALUE\n$v(S) = P(w \\in S)$, $w$ = winner\n(rollout estimate)', so that the math survives translation unchanged; 'Shapley value\n$\\phi_i$ = fair marginal\ncontribution' → 'Shapley value\n$\\phi_i$ = average\nmarginal contribution'. Mapping:
  - 'Coalition VALUE\n$v(S) = P(w \\in S)$, $w$ = winner\n(rollout estimate)' → 'СТОЙНОСТ на коалицията\n$v(S) = P(w \\in S)$, $w$ - победителят\n(оценка чрез симулации)'
  - 'Shapley value\n$\\phi_i$ = average\nmarginal contribution' → 'Стойност на Шапли\n$\\phi_i$ = среден\nпределен принос'
  - 'Per-player CREDIT\n(the training signal)' → 'ПРИНОС на играча\n(сигнал за обучението)'
  - 'Shapley = the UNIQUE fair split; …' → 'Стойността на Шапли е единственото разпределение, което удовлетворява аксиомите на Шапли; тук стойност на коалицията е вероятността за победа.'
  - the EMPTY CORE box, numbers unchanged → 'ПРАЗНО ЯДРО = структурна нестабилност (измерено, точно):\n  игра с ръкавиците -> Shapley (2/3, 1/6, 1/6), ядрото е НЕПРАЗНО (има стабилно разпределение)\n  мнозинство от трима -> Shapley (1/3, 1/3, 1/3), ядрото е ПРАЗНО (няма стабилно разпределение)\nSLS е игра с постоянна сума и също има празно ядро: коалициите са нестабилни -\nбезопасната игра при N играчи не може да се опре на равновесие или ядро (Принос №2).' ("Shapley" is kept because the validator rejects a lost name; see B08 for the Cyrillic/Latin decision.)
  - 'MEASURED on SLS: …' → 'ИЗМЕРЕНО в SLS: размах на симетричния принос 0.013 (след поправката);\nасиметрична позиция [8,8,1,1] -> принос на силната двойка 1.0, на слабата 0.0.'

### F11-G05 · S1 · Fig. 67 shows only the asymmetric position; the caption describes both
- **Where:** `renders/ch11/p210_f1.png`; `summary/impl_shapley_attribution.png` (= `plots/shapley_attribution.png`). Caption: "…почти равномерно между местата в симетричния случай (разпределение 0.013…), и изцяло концентрирано върху силната двойка…"
- **Problem:**
  1. **The figure does not show the symmetric case.** `plotting.py` plots only the asymmetric [8,8,1,1] position (P0 ≈ 0.47, P1 ≈ 0.53, P2 = P3 = 0). The "near-flat, spread 0.013" half of the caption has nothing to point at.
  2. English title "Per-player Shapley credit on a sample position (PREDICTIO[N]" (clipped; stale "PREDICTION"), English y-label "Shapley credit (win-prob share)", ticks "P0…P3", decimal points.
  3. 110 ppi.
- **Fix:** `plotting.py`: replace `plot_shapley_attribution` with grouped bars from `results/smoke_results.json` → `shapley.symmetric_credit` [0.247, 0.257, 0.253, 0.243] and `shapley.asymmetric_credit` [0.503, 0.497, 0, 0]. Use width 0.38, `ax.axhline(0.25, ls="--", color="gray", label="equal share 0.25")`, xticks "seat 0…3", ylabel "Shapley credit (win-probability share)", fontsize 10, legend 9.6, no title, figsize (5.0, 3.2), dpi 300. Save to `summary/impl_shapley_attribution.png`. Mapping: 'symmetric position' → 'симетрична позиция', 'asymmetric [8,8,1,1]' → 'асиметрична [8,8,1,1]', 'equal share 0.25' → 'равен дял 0.25', 'Shapley credit (win-probability share)' → 'принос по Шапли (дял от вероятността за победа)', 'seat' → 'място'. Link the `_bg` file in `summaryBg.md`.

### F11-G06 · S1 · Fig. 68 MAPPO blend: inverted formula, English boxes, overlapping boxes
- **Where:** `renders/ch11/p211_f1.png`, `summary/make_mappo_figure.py` → `mappo_blend_bg.png`
- **Problem:**
  1. **The formula is inverted.** The box prints $r = (1-\alpha)\,r_{\text{sparse}} + \alpha\,\text{credit}$, but the code is `alpha * sparse + (1 - alpha) * credit_centered` (`coalition_mappo.py` l. 110). The note above the box says the opposite ("alpha=0 -> pure coalition credit") (C01). The note is also an unfinished sentence: "between 'just win' (… 1 -> pure sparse)."
  2. English: the top note, the whole "MEASURED (5-seed paired sweep …)" box and the "TRADE-OFF (measured)" box (three mappings rejected: "names lost: ['alpha']"); "Episodic PPO" inside the BG label.
  3. **The boxes overlap geometrically.** The credit box spans y 3.5–4.8 and the MEASURED box y 0.9–3.8, so "Shapley коалиционен кредит (прокси или контрафактичен)" sits on the grey box edge. "r_sparse (победителят взема всичко)" overflows the blue box on both sides.
  4. Numbers in the MEASURED box: "(~4.4x sparse)" and "alpha >= 0.3 (any cell): -0.001 ... -0.004" (C06).
  5. Legibility (scale 0.874): box fs 7.7–8.6 → 6.7–7.5 pt.
- **Fix:** `make_mappo_figure.py`: all fs → 10; `sweep` and `tradeoff` h 2.9 → 2.4 (top at 3.3); `sparse`/`credit` labels wrapped to three lines. Source strings:
  - 'BLEND\n$r = \\alpha\\,r_{\\text{sparse}} + (1-\\alpha)\\,\\text{credit}$'
  - note → '$\\alpha$ sets the balance: $\\alpha=1$ -> win reward only ("just win"), $\\alpha=0$ -> coalition credit only.'
  - MEASURED box → 'MEASURED (5 seeds, paired; gap = coalition score Shapley - sparse):\n  $\\alpha=0$, proxy, synergy 0.3: +0.0376 +/- 0.0103 (score 4.5x sparse)\n  $\\alpha=0$, rollout credit: +0.0128 +/- 0.0026\n  $\\alpha \\geq 0.3$, scale tier: -0.0003 ... -0.0035 (the DEAD ZONE)'
  - TRADE-OFF box → 'TRADE-OFF (measured):\n$\\alpha=0$ -> win rate ~0.29\n(chance level 0.25)\n$\\alpha \\geq 0.1$ -> win rate ~0.52'. Using `$\alpha$` instead of the word "alpha" passes the names-lost validator.

  Mapping:
  - 'BLEND…' → 'СМЕСВАНЕ\n$r = \\alpha\\,r_{\\text{sparse}} + (1-\\alpha)\\,\\text{credit}$'
  - note → '$\\alpha$ задава баланса: $\\alpha=1$ -> само наградата за победа, $\\alpha=0$ -> само коалиционният принос.'
  - MEASURED → 'ИЗМЕРЕНО (5 начални числа, сдвоени; разлика = коалиционен резултат Шапли - рядка награда):\n  $\\alpha=0$, заместител, синергия 0.3: +0.0376 +/- 0.0103 (резултат 4.5 пъти по-висок)\n  $\\alpha=0$, принос чрез симулации: +0.0128 +/- 0.0026\n  $\\alpha \\geq 0.3$, разширена конфигурация: -0.0003 ... -0.0035 (МЪРТВА ЗОНА)'
  - TRADE-OFF → 'КОМПРОМИС (измерен):\n$\\alpha=0$ -> дял на победите ~0.29\n(ниво на случайността 0.25)\n$\\alpha \\geq 0.1$ -> дял на победите ~0.52'
  - 'Sparse reward\n$r_{\\text{sparse}}$ (winner takes all)' → 'Рядка награда\n$r_{\\text{sparse}}$ (победителят\nвзема всичко)'
  - 'Shapley coalition credit\n(proxy or counterfactual)' → 'Коалиционен принос\nпо Шапли (заместител\nили симулации)'
  - 'Masked episodic PPO\nself-play (4 seats)' → 'PPO с маскиране,\nигра срещу себе си\n(4 места)'

### F11-G07 · S1 · Fig. 69 sweep: entirely English, prints at 4.5–6.7 pt
- **Where:** `renders/ch11/p213_f1.png`; `summary/impl_sweep_coalition_gap.png` (= `plots/sweep_coalition_gap.png`)
- **Problem:**
  1. Everything is English: the suptitle, the panel titles "[smoke] chips=5 train=400 seeds=5 / sparse baseline score=0.0073", the axis labels "alpha (sparse<->credit blend; 0 = pure coalition credit)" and "coalition-score gap (shapley - sparse)", the legend, and decimal points. The BG renderer runs `plotting.py` without `--sweep`, so this plot never gets a `_bg` twin, and `summaryBg.md` links the EN file.
  2. Legibility: 1488 px at 120 dpi = 12.4 in wide, printed at 17.6 cm → scale 0.559. Legend 8 → 4.5 pt; ticks and axis labels 10 → 5.6 pt; panel titles 12 → 6.7 pt; suptitle 11 → 6.1 pt.
  3. The smoke panel shows the counterfactual cell at α = 0.3 at +0.0012, which contradicts the caption's "negative for every alpha >= 0.3" (C06).
- **Fix:** `plotting.py` `plot_sweep`: figsize (6.2·2, 4.4) → (7.0, 3.3); dpi 120 → 300; drop `fig.suptitle`; panel titles → 'smoke (5 chips, 400 games)' / 'scale (7 chips, 1500 games)'; `ax.legend(fontsize=9.6)`; `ax.tick_params(labelsize=9.6)`; labels fontsize 10: xlabel '$\\alpha$ (0 = coalition credit only, 1 = sparse only)', ylabel 'coalition-score gap (Shapley - sparse)'; series labels 'rollout credit' / 'proxy, synergy 0.1' / 'proxy, synergy 0.3'. Make the no-argument `__main__` also render the sweep into `summary/`. Mapping: the two panel titles → 'пробна (5 жетона, 400 игри)' / 'разширена (7 жетона, 1500 игри)'; xlabel → '$\\alpha$ (0 = само принос, 1 = само рядка награда)'; ylabel → 'разлика в коалиционния резултат (Шапли - рядка)'; 'rollout credit' → 'принос чрез симулации'; 'proxy, synergy 0.1' → 'заместител, синергия 0.1'.

### F11-G08 · S1 · Fig. 70 EGTA pipeline: every box overflows; "Басейн", "TENSOR", "wheel", "Стъпка 10"
- **Where:** `renders/ch11/p214_f1.png`, `summary/make_egta_figure.py` → `egta_spinning_top_bg.png`
- **Problem:**
  1. Overflow into neighbours: "Басейн от стратегии", "Печалба при 4 играчи", "Проектиране към по двойки матрица на съперничеството" (runs into both arrows), "Пумпал на Ходж разделяне (Стъпка 10)", "скала на уменията", "(коалиция wheel)". The result-box lines run past both edges ("Силно цикличен, потвърждава посоката от Стъпка 10, но точно").
  2. English: "TENSOR", "wheel". The current mapping is worse still: 'TRANSITIVE\n(skill ladder)' → 'транзитивен\n(skill ladder)' and 'CYCLIC\n(coalition wheel)' → 'цикличен\n(coalition wheel)' (source "glossary").
  3. Meaning: "Басейн от стратегии" (a *swimming* pool); "Проектиране" (designing, for *project*); "Пумпал на Ходж разделяне" (no syntax); stale "(Стъпка 10)" / "от Стъпка 10".
  4. Top note: "EGTA = равновесие на Наш на игра…" misdefines EGTA (it is the empirical meta-game and its analysis; the meta-Nash is one analysis of it). "експлоатируемостта няма смисъл" overclaims (C09). 'стратегии' is in straight quotes.
  5. "(КОЛЕЛО)" is written for a population whose transitive part is still the larger one (C08).
  6. Stale render: the printed "скала на уменията", "(коалиция wheel)" and "от кой ПУЛ зависи формата на разлагането" differ from the current mapping, so the PNG predates it (G10).
  7. Legibility (scale 0.873): fs 7.7–8.6 → 6.7–7.5 pt.
- **Fix:** `make_egta_figure.py`: all fs → 10. `trans` x 8.0 → 7.7, w 2.6 → 2.9; `cyc` x 11.0 → 10.8, w 2.6 → 2.9; `res` y 1.6 → 0.9, h 2.2 → 3.0, lines wrapped to ≤ 50 characters. Source strings: "(Step 10)" → "(Chapter 10)"; the note → 'EGTA = an empirical meta-game whose "strategies" are whole policies; exploitability gives no guarantee against a coalition.'; the result box → '…coalition pool -> cyclic ~0.57-0.69 (strong cyclic part)\nTransitive part still slightly larger - the 2-type projection likely\ndiscards 3-/4-player coalition effects (Contribution #3, open).' Mapping:
  - 'Strategy pool\n$\\{\\pi_1,\\dots,\\pi_n\\}$' → 'Набор от стратегии\n$\\{\\pi_1,\\dots,\\pi_n\\}$'
  - '4-player payoff\nTENSOR\n(play every group)' → 'ТЕНЗОР на печалбите\nза 4 играчи\n(всяка четворка)'
  - 'Project to pairwise\nmatchup matrix' → 'Проекция в\nматрица на\nсблъсъците по двойки'
  - 'Hodge spinning-top\nsplit (Chapter 10)' → 'Разлагане „пумпал“\n(на Ходж, Глава 10)'
  - 'TRANSITIVE\n(skill ladder)' → 'ТРАНЗИТИВНА\n(стълба на уменията)'
  - 'CYCLIC\n(coalition wheel)' → 'ЦИКЛИЧНА\n(колело от коалиции)'
  - the note → 'EGTA = емпирична мета-игра, в която „стратегиите“ са цели политики; експлоатируемостта не дава гаранция срещу коалиция.'
  - the result box → 'ИЗМЕРЕНО - съставът на ПОПУЛАЦИЯТА определя формата:\n  стълба на уменията -> циклично ~0.25-0.31 (СТЪЛБА)\n  коалиционна популация -> циклично ~0.57-0.69 (силна циклична част)\nТранзитивната част остава малко по-голяма - проекцията\nвърху 2 типа вероятно губи ефектите между 3-4 играчи\n(Принос №3, отворен въпрос).'

### F11-G09 · S1 · Fig. 71 shows one population; the caption describes two
- **Where:** `renders/ch11/p215_f1.png`; `summary/impl_spinning_top.png` (= `plots/spinning_top.png`)
- **Problem:**
  1. **The figure shows only the skill-ladder smoke pool** (transitive 0.97, cyclic 0.25 = `smoke_results.json` `egta`). The coalition-pool values the caption quotes (~0.57–0.69) are in no figure and **in no results file**: they exist only in `EXECUTION_NOTES.md` ("check 5"), because `validate.py` prints them and saves nothing.
  2. English title "SLS meta-game: transitive vs cyclic (Hodge; PREDICT cyclic-h[eavy]" (clipped, stale), "Frobenius ratio", "transitive/cyclic", decimal points. 110 ppi.
  3. As printed it adds nothing to Table 42, which gives the same numbers.
- **Fix:** Preferred: delete the figure (l. 125 of `summaryBg.md`, l. 208 of `summaryEn.md`); Table 42 carries the result. If it stays: make `validate.py` write the check-5 block (`transitive_ratio`, `cyclic_ratio`, pool names, games per cell) to `results/validate_smoke.json`. Then `plot_spinning_top` should draw grouped bars for both pools, with `ax.axhline(0.707, ls="--", label="strict-dominance threshold")`, fontsize 10, figsize (5.0, 3.2), dpi 300, no title. Mapping: 'transitive' → 'транзитивна', 'cyclic' → 'циклична', 'Frobenius ratio' → 'дял по нормата на Фробениус', 'strict-dominance threshold' → 'праг на строго доминиране'.

### F11-G10 · S2 · Pipeline: stale renders, seven rejected mappings, `impl_*` figures outside the BG pipeline, 110 ppi
- **Where:** `summary/*_bg.png` (written 1 Aug 13:08) vs `figure_labels.json`; `summaryBg.md` l. 46, 69, 102, 125.
- **Problem:**
  1. Seven step-11 mapping entries have `bg: null` and print in English: 'alpha (sparse<->credit blend…)', 'alpha dials between…', 'Coalition VALUE…', 'EMPTY CORE…', 'MEASURED (5-seed…)', 'Per-player Shapley credit … (PREDICTION)', 'TRADE-OFF…'. Rejection reasons: "names lost: ['alpha']", "math changed", "numbers changed".
  2. Two entries with source "glossary" leave English in the BG ('(skill ladder)', '(coalition wheel)').
  3. The `egta_spinning_top_bg.png` render predates the mapping.
  4. All four `impl_*` figures are copies of `implementation/step11/implementation/plots/*.png` from 24 Jul. `summaryBg.md` links the EN files, so no BG version is ever produced. Three of them are 550 px (110 ppi at 12.7 cm), soft in print. (The manifest gives 110 ppi, not the ~92 mentioned in the brief.)
- **Fix:** After G02–G09, rerun `python scripts/figures/render_bg_figures.py --only step11` and rebuild. For labels containing α, change the EN source to `$\alpha$` rather than weakening the validator. Keep all fs ≥ 10 in these diagrams (the scale is 0.80–0.87), and when BG text overflows, wrap or enlarge the box.

## B — Bulgarian language

### F11-B01 · S1 · English left in the summary text
- **Where:** summaryBg.md, throughout. Most items are fixed inside the sentence rewrites listed below; one is fixed here.
- **Now → Proposed:**
  - "## Coalition-Aware MAPPO - и кога всъщност се проявяват коалиции" → "## MAPPO с отчитане на коалициите - и кога всъщност възникват коалиции"
  - The other English, with the finding that fixes each: Read-more block l. 33–34 "(the game itself); and De" (S03); "маскиран агент на Episodic PPO" (B14); "(Shapley coalition credit)" in the formula (C01); "| smoke, заместител" and "„smoke-положително / мащаб-нула“" (B14); "червен FAIL" (B13); "(cyclic $\sim 0.07$)", "seat-0", "(разделът *Shapley credit*)", "cyclic$^2$", "**2-type projection discards 3-/4-player coalition effects**" (B15); "| Glove Game |" (B09); "**EGTA Meta-Game + стойност на Шейпли**" (C09); "eGTA-tensor evaluation" (C04); "EGTA Cyclic Ratio" (S02); "$\alpha\ge 0.1$ restores" (C06); "`scale_results.JSON`" (B05); footnote `chapter2022` in English (S05); "(core, shapley, nucleolus)" (S07).
- **Why:** English prose on pp. 206, 211–216. Several items come from glossary entries whose BG side is English (T02).

### F11-B02 · S1 · One-pager: meaning errors and English
- **Where:** onePagerBg.md "**Подход.**", "**Ключови резултати (измерени).**", "**Отворени въпроси.**"
- **EN:** "the authoritative figures are `sweep_scale.json`… `scale_results.json` is a **pre-fix** run" / "**planted `{0,1}` alliance**" / "Harness: **4/5 PASS**" / "a **coalition-aware MAPPO** trainer" / "Whether a 3- or 4-player-aware EGTA projection surfaces the cycling the 2-type collapse discards."
- **Now → Proposed:**
  - "`scale_results.json` представлява **предварително коригиран** прогон" → "`scale_results.json` е прогон **отпреди поправката**"
  - "Детекторът възстановява **„засадена“ коалиция `{0.1}`** единствено от потока ходове" → "Детекторът разпознава **предварително зададената коалиция `{0,1}`** единствено от потока от ходове"
  - "Резултат: **4/5 ПРЕЗ**." → "Проверки: **4 от 5 успешни**."
  - "**Coalition-Aware MAPPO** треньор, който комбинира наградата за коалиция и „всичко или нищо“ чрез тегло `alpha`" → "обучение **MAPPO с отчитане на коалициите**, което смесва коалиционния принос и наградата „победителят взема всичко“ с тегло `alpha`"
  - "анализ **eGTA + пумпал**, преизползван от Глава 10" → "анализ **EGTA + разлагане „пумпал“**, преизползван от Глава 10"
  - "Дали **EGTA Projection**, съобразена с 3 или 4 играчи, ще разкрие **цикличността**, която колапсът от 2 типа премахва." → "Дали проекция за **EGTA**, съобразена с 3 или 4 играчи, ще разкрие **цикличността**, която свиването до 2 типа губи."
- **Why:** "предварително коригиран" (*corrected in advance*) inverts *pre-fix*. "{0.1}" turns the set of players 0 and 1 into a decimal number. "ПРЕЗ" is a transliteration of *PASS* and means "through". "треньор" is a sports coach. The rest is English on the printed page.

### F11-B03 · S1 · Pilot glossary errors in this chapter (F07-T06 "неразрешим", F07-T09 "обхождане", F07-T14 "герой")
- **Where / Now → Proposed:**
  - T06, summaryBg l. 19: "където **Нашево равновесие и експлоатируемост спират да бъдат управляеми *и* губят смисъла си**, така че „сработи ли?“ вече не може да бъде едно-единствено число." → "където **равновесието на Наш и експлоатируемостта стават изчислително непосилни *и* губят смисъла си**, така че на въпроса „проработи ли?“ вече не може да се отговори с едно-единствено число."
  - T06, onePagerBg: "докато **наш равновесието** става едновременно неразрешим и стратегически празен, тъй като изцяло пренебрегва коалициите." → "докато **равновесието на Наш** става едновременно изчислително непосилно и лишено от гаранции, тъй като изобщо не отчита коалициите."
  - T06, l. 27 "…е едновременно **неразрешим** от гледна точка на изчислителна мощност…" and l. 143 "Стойността на Наш е неразрешима и стратегически празна" → replacements in F11-S02 (sources are added there).
  - T09, l. 133: "една единствена конфигурация скрива онова, което обхождане с фиксирани начални стойности разкрива." → in F11-B16.
  - T14, l. 75 "процент на победа на героя е бил *същият* артефакт (героят винаги е седял на място 0)" → in F11-B13; l. 133 "завиши процента победи на героя" → in F11-B16; onePagerBg "намали впечатляващия процент победи на героя" → in F11-B18.
- **Why:** "неразрешим" means unsolvable, and "управляеми" means manageable/controllable (*tractable*). "Равновесие … неразрешим … безсъдържателен" also breaks gender agreement (the noun is neuter), and "наш" in lower case reads as "our". Extend T06 to the settled entries "computationally intractable → изчислително неразрешим" and "tractable heuristics → управляеми евристики".

### F11-B04 · S1 · meaning — §11.6 heading says "this deal"
- **Where:** summaryBg.md l. 129
- **EN:** "## Honest notes, limitations, and where this hands off"
- **Now → Proposed:** "## Честни бележки, ограничения и къде това раздаване се поема оттук нататък" → "## Бележки, ограничения и връзка със следващите глави"
- **Why:** "раздаване" is a poker deal, so the printed heading (p. 215, and in the TOC) reads "where this deal is taken over from here on". *Hands off* means "passes on to the next chapters".

### F11-B05 · S1 · meaning — "представка-артефакт", ".JSON", "с грешки"
- **Where:** summaryBg.md l. 135 "**Доверие.**"
- **EN:** "the training claims rest on a 5-seed paired sweep with error bars" / "(The committed `scale_results.json` is a pre-fix artifact, cited only as evidence of the bug; authoritative scale numbers come from the sweep.)"
- **Now → Proposed:**
  - "твърденията за обучението се основават на петкратно кръстосано сравнение по двойки с грешки" → "твърденията за обучението се основават на сдвоени сравнения с 5 начални числа и интервали на грешката"
  - "(Подаденият `scale_results.JSON` е представка-артефакт, цитиран единствено като доказателство за грешката; авторитетните данни за мащаб идват от обхождането.)" → "(Записаният файл `scale_results.json` е резултат отпреди поправката и се цитира само като доказателство за грешката; меродавните данни за разширената конфигурация идват от серията експерименти.)"
- **Why:** "представка" is a grammatical prefix (T04). "с грешки" means "with mistakes". "петкратно кръстосано" means "fivefold cross[-validation]" (T07). The file name was changed to `.JSON`, which does not exist. "авторитетни" (*authoritative* as a calque) → "меродавни".

### F11-B06 · S1 · meaning — "(незначителна)" for a significant result; "мода" for mode
- **Where:** summaryBg.md Table 41 last row; l. 88
- **EN:** "| smoke, proxy, $\alpha=0$, synergy $0.1$ | **$+0.0024 \pm 0.0008$** (tiny) |" / "over $\alpha\times$ credit-mode $\times$ synergy"
- **Now → Proposed:**
  - "**$+0.0024 \pm 0.0008$** (незначителна)" → "**$+0.0024 \pm 0.0008$** (много малка)"
  - "върху $\alpha\times$ мода на кредита $\times$ синергия" → "по мрежата $\alpha\times$ вид на приноса $\times$ синергия"
- **Why:** In a statistics table "незначителна" reads as "not significant", which contradicts the `**` and the text (3.1 SE). "мода" means fashion (T10).

### F11-B07 · S2 · terminology — the Nash naming (pilot rule F07-B02)
- **Where:** summaryBg.md l. 21; onePagerBg.md "**Връзка с дисертацията.**"; the other occurrences are rewritten in B03, B18 and C04.
- **Now → Proposed:**
  - "**Безопасната базова линия губи своята Нашева опорна точка**" → "**Безопасната базова линия губи опората си в равновесието на Наш**"
  - "при **празно ядро** и липса на котва в **Нашево равновесие**" → "при **празно ядро** и без опора в **равновесието на Наш**"
- **Why:** One concept should have one form: "равновесие на Наш" (glossary). The chapter uses "Нашево" (l. 19, 21), "Нашово" (l. 137), "наш равновесието" and "Неш" (one-pager).

### F11-B08 · S2 · terminology — Shapley written three ways; *credit* as "кредит/стойност/заслуги"
- **Where:** summaryBg.md: "Шейпли" 7×, "Шапли" 6×, "Shapley" 12× (Table 40 has "Шейпли" in the header and "Шапли" in its own caption); onePagerBg.md "Шейпли" 4×. *Credit*: "кредит" 11×, "стойност на Шейпли" (l. 21, 52), "заслуги" (fig. 67).
- **Now → Proposed** (the occurrences not rewritten elsewhere):
  - "## Стойност на Шейпли в състезателна игра" → "## Принос по Шапли в състезателна игра"
  - "Класическият инструмент е **стойността на Шейпли**:" → "Класическият инструмент е **стойността на Шапли**:"
  - "| Кооперативна игра-играчка | Стойност на Шейпли | Ядро (стабилност) |" → "| Опростена кооперативна игра | Стойност на Шапли | Ядро (стабилност) |"
  - "| Режим | Сдвоена разлика (Shapley - оскъдна базова линия) |" → "| Режим | Сдвоена разлика (Шапли - рядка награда) |"
- **Why:** The curated `terminology_EN_BG.md` has "Стойност на Шапли". The settled glossary has "Шейпли" (T06n below). The brief's name list keeps "Shapley" in Latin, and the figure validator enforces it. That is one rule too many: decide once. The form "стойност на Шапли" matches "равновесие на Наш" and the curated file. *Credit* in RL credit assignment is the share of the outcome attributed to an agent, "принос". "Кредит" reads as a bank loan, and "стойност на Шапли" for *Shapley credit* merges the tool with its use (the §11.3 heading says "Shapley value in a competitive game", but the section is about credit).

### F11-B09 · S2 · English and calques in Table 40
- **Where:** summaryBg.md Table 40 rows
- **EN:** "| Glove game |" / "| 3-player majority |"
- **Now → Proposed:**
  - "| Glove Game |" → "| Игра с ръкавиците |"
  - "| тричленно мнозинство |" → "| Мнозинство от трима играчи |"
- **Why:** "Glove Game" is English in the printed table (p. 209). "тричленно мнозинство" is a "three-member majority" of a committee, not the three-player majority game. (Header: B08.)

### F11-B10 · S2 · terminology — *capture* four ways, *chip* two ways
- **Where:** summaryBg.md l. 29, 44 (l. 40 in B12, l. 75 in B13); onePagerBg "поставянето на чип"
- **Now → Proposed:**
  - "или завладявате техните купчини (ножът)" → "или вземате техните купчини (ножът)"
  - "Коалицията е напълно разпознаваема единствено от начина на поставяне на чиповете." → "Коалицията се разпознава напълно само по начина, по който се поставят жетоните."
  - onePagerBg "(оценяващ помощта или вредата от поставянето на чип)" → "(помощ и вреда според поставянето на жетоните)"
- **Why:** *Capture* appears as "завладявате" (l. 29), "залови" (l. 40), "заграбване" and "улавяне" (figure). *Chips* appears as "жетони" (l. 29, 133) and "чип/чиповете/чипове" (l. 40, 44, 75). The glossary has chips → жетони.

### F11-B11 · S2 · calques — introduction and §11.1
- **Where:** summaryBg.md l. 19, 21, 27, 29, 31
- **Now → Proposed:**
  - "са ограничени от *точни* референции (учебникови стойности на Шапли/ядро за кооперативни игри; точен двуиграчев минимакс решавач за крайната игра на SLS)" → "са поставени в рамките на *точни* еталонни стойности (учебниковите стойности на Шапли и ядрото за опростени кооперативни игри; точен минимаксен решавач за крайната фаза на SLS с двама играчи)"
  - "включително и реален бъг в двигателя - запазвам първоначалното очакване и го съгласувам с това, което се е случило; тези пропуски са най-поучителните части от главата." → "включително истинска грешка в двигателя на играта - запазвам първоначалното очакване и го съпоставям с действителния резултат; тези разминавания са най-поучителната част от главата."
  - "Глава 11 го премахва и навлиза във фронтира. Тук се съдържат три основни приноса на дисертацията." → "Глава 11 се отказва от него и навлиза в нерешените проблеми на областта. Тук главата се свързва с трите приноса на дисертацията."
  - "издига моделирането на противника от „какъв тип играч е това?“ до „с кого е в съюз?“ (Принос №1)" → "пренася моделирането на противника от въпроса „какъв тип играч е това?“ към въпроса „кой с кого е в съюз?“ (Принос №1)"
  - "е едно-единствено, смислено число, което поддържаше всяка стъпка от Глава 2 насам." → "е едно-единствено смислено число, на което се опираше всяка глава от Глава 2 насам."
  - "Картина, която да задържите в ума си:" → "Полезна аналогия:"
  - "Со Лонг Съкър прави това буквално" → "So Long Sucker прави това буквално"
  - "**на $N\ge 3$ се преминава от точна оценка към емпирична оценка.**" → "**при $N\ge 3$ точната оценка отстъпва място на емпиричната.**"
  - "Вместо експлоатируемост се използват процент победи, резултат на коалиция от детектора и циклично съотношение на една емпирична мета-игра - всичко това е закотвено в единствената под-игра, която *е* точно решима, а именно крайната игра с двама играчи." → "Вместо експлоатируемост се използват делът на победите, коалиционният резултат от детектора и цикличното съотношение на емпиричната мета-игра, закотвени в единствената подигра, която *е* точно решима: крайната фаза с двама играчи."
- **Why:** "Тук се съдържат три основни приноса" says the three contributions are *in* this chapter; the EN says "three thesis hooks". "с кого е в съюз?" asks "who is he allied with?" and loses the *who with whom* of the detector. "фронтир", "бъг", "референции", "двуиграчев" and "на $N\ge 3$" are calques or anglicisms. "стъпка" is stale (the EN has "step" here too, see C04). The curated glossary keeps "So Long Sucker" in Latin script. "съгласувам" means to make consistent (see T15).

### F11-B12 · S2 · calques — §11.2 and §11.3
- **Where:** summaryBg.md l. 40, 44, 48, 63, 67
- **Now → Proposed:**
  - "Той наблюдава хода и натрупва две матрици: **помощ** (играч $i$ поставя чип в купчината на играч $j$) и **вреда** (играч $i$ залови купчината на играч $j$)." → "Той следи дневника на ходовете и натрупва две матрици: **помощ** (играч $i$ поставя жетон в купчината на играч $j$) и **вреда** (играч $i$ взема купчината на играч $j$)."
  - "Скриптираме двама играчи да си помагат систематично и да вредят на останалите, без да предоставяме никаква информация на детектора, и го караме да посочи коалицията. В резултат той възстановява засадената $\{0,1\}$ коалиция **точно**" → "Програмираме двама играчи да си помагат систематично и да вредят на останалите, без да даваме на детектора никаква информация, и го караме да посочи коалицията. Той разпознава **точно** предварително зададената коалиция $\{0,1\}$"
  - "> **Прочетете повече:** двигателят за моделиране на противника от Глава 07 (това хранилище) - принципът „наблюдавай действия -> актуализирай вярвания“, който детекторът преоткрива като матрици на помощ/вреда." → "> **Прочетете повече:** реализацията на моделирането на противника от Глава 7 - принципът „наблюдение на действията → обновяване на убежденията“, който детекторът пресъздава като матрици на помощта и вредата."
  - "е концептуалното сърце на стъпката" → "е ключовата идея на главата"
  - "SLS е състезателна, а не кооперативна игра - няма общ пот за разделяне - така че ние **предефинираме стойността на коалиция** като *вероятността член на коалицията да спечели*, оценена чрез Монте Карло симулации." → "SLS е състезателна, а не кооперативна игра - няма обща печалба, която да се поделя, - затова **предефинираме стойността на коалицията** като *вероятността неин член да спечели*, оценена чрез симулации по метода Монте Карло."
  - "Кредитът на всеки играч след това се изчислява като стойността на Шейпли на тази функция за вероятност от печалба." → "Приносът на всеки играч е стойността на Шапли на тази функция на вероятността за победа."
  - "Измерено върху SLS позиции: една наистина симетрична позиция води до почти равностойно разпределение на кредита (разпределение $0.013$), а една асиметрична $[8,8,1,1]$ позиция присъжда *целия* кредит на силната двойка (стойност на коалиция $1.0$)." → "Резултати върху позиции в SLS: наистина симетрична позиция дава почти равни приноси (размах $0.013$), а асиметричната позиция $[8,8,1,1]$ приписва *целия* принос на силната двойка (стойност на коалицията $1.0$)."
  - "Симетричният резултат е докладван **след** отстраняване на грешка - виж съгласуването по-долу." → "Симетричният резултат е получен **след** отстраняване на грешка - вж. съпоставката по-долу."
- **Why:** "наблюдава хода" means "watches the move/course" (EN: the move log). "Скриптираме", "засадена" (T09n) and "пот" are calques; in Bulgarian "пот" means sweat. "печалба" is payoff, not winning. *Spread* is the max−min range ("размах"), not a distribution (T11). "Глава 07" should be "Глава 7".

### F11-B13 · S2 · the first reconciliation block (l. 71–76)
- **Where:** summaryBg.md l. 71–76. Replace the whole block. It also carries the C03 content fix ("in this engine").
- **Now:** "> **Съгласуване (запазена прогноза -> какво всъщност се случи).** Прогнозирах, че симетрична позиция\n> ще даде симетрично разпределение на кредита ($<0.15$). Първото изпълнение даде $0.54$ - червен FAIL - с\n> Играч 0 печелещ ~2x своя справедлив дял в три независими скрипта. Подозрявайки механиката преди\n> прогнозата, открих механизма: **~99.5% от случайните SLS игри завършват със задънена улица** (всички живи\n> ръце празни), така че победителят се решава чрез най-много чипове **развръзка при равенство** - чието правило с най-нисък индекс тихо даде предимство на място 0. **Безпристрастна случайна развръзка при равенство** го поправи: симетрично разпределение $0.54\to 0.013$, победителите вече са равномерни. Това също разкри, че впечатляващ $\sim 0.87$ процент на победа на героя е бил *същият* артефакт (героят винаги е седял на място 0); справедливият брой е\n> $\sim 0.41$. Урокът: в игра, която почти винаги завършва с почти равенство, правилото за развръзка при равенство е най-натовареният ред в механиката, и симетрична *позиция* не е симетричен *изход*, докато не бъде безпристрастна."
- **Proposed:** "> **Съпоставка (запазена прогноза → действителен резултат).** Прогнозирах, че симетрична позиция\n> ще даде симетрично разпределение на приноса (размах $<0.15$). Първото изпълнение даде $0.54$ (неуспешна проверка), като\n> играч 0 печелеше около два пъти повече от справедливия си дял в три независими скрипта. Тъй като заподозрях първо двигателя, а не\n> прогнозата, открих механизма: **~99.5% от случайните игри в този двигател завършват с пат** (всички играчи, останали в играта,\n> са без жетони в ръка), затова победителят се определя от правилото при равенство по брой жетони, а то тихомълком даваше предимство на място 0, защото избираше играча с най-малък индекс. **Безпристрастното случайно разрешаване на равенството** отстрани проблема: размахът на симетричния принос спадна от $0.54$ на $0.013$, а победите вече се разпределят равномерно. Това разкри също, че впечатляващият дял победи $\sim 0.87$ на обучения агент е бил *същият* артефакт (агентът винаги е заемал място 0); реалната стойност е\n> $\sim 0.41$. Урокът: в игра, която почти винаги завършва с почти равен резултат, правилото при равенство е най-важният ред в кода на двигателя, а симетричната *позиция* дава симетричен *изход* едва когато това правило е безпристрастно."
- **Why:** "червен FAIL" is English. "Играч 0 печелещ ~2x" is a participle calque. "Подозрявайки механиката преди прогнозата" does not parse. "задънена улица" (T08) is a physical dead end. "чрез най-много чипове развръзка при равенство" is word salad. "героя" (T14). "най-натовареният ред" (*load-bearing*, calqued as "most loaded"). "докато не бъде безпристрастна" has no agreeing noun. The "(всички живи ръце празни)" calque becomes a real clause. "SLS" → "този двигател" (C03).

### F11-B14 · S2 · calques — §11.4
- **Where:** summaryBg.md l. 82, 88, 90–97, 99–100, 104
- **Now → Proposed:**
  - "Сега провеждаме обучението. Всяко място в SLS е маскиран агент на Episodic PPO, който се обучава чрез самообучение." → "Следва обучението. Всяко място в SLS се заема от отделен агент PPO с маскиране на недопустимите ходове, който се обучава по цели епизоди чрез игра срещу копия на себе си."
  - "Формират ли коалиция-осъзнатите агенти повече коалиции отколкото оскъдните агенти?" → "Формират ли агентите, обучени с коалиционен принос, повече коалиции от агентите с рядка награда?"
  - "Честният отговор изискваше **петкратно кръстосано сравнение по двойки** върху" → "Честният отговор изискваше **сдвоени сравнения с 5 начални числа**"
  - "една единствена конфигурация ме подведе сериозно (по-долу). Измерено (сдвоена разлика = коалиционен резултат на Shapley агентите минус този на оскъдните агенти; `**` = значимо при $>2\times$ SE):" → "една-единствена конфигурация ме подведе сериозно (вж. по-долу). Резултати (сдвоена разлика = коалиционен резултат на агентите с принос по Шапли минус този на агентите с рядка награда; `**` = разлика, по-голяма от две стандартни грешки):"
  - "| мащаб, заместител," → "| разширена, заместител,"; "| мащаб, контрафактичен," → "| разширена, чрез симулации,"; "| smoke, заместител," → "| пробна, заместител,"
  - ": Сдвоена разлика в коалиционния резултат на разпределението по Шапли спрямо разредената базова линия, по режим." → ": Сдвоена разлика в коалиционния резултат между агентите с принос по Шапли и базовата линия с рядка награда, по режим."
  - "Моите експерименти с един конфигурационен файл използваха стойността по подразбиране" → "Експериментите ми с една-единствена конфигурация използваха стойността по подразбиране"
  - "показаха, че коалиционният сигнал изчезва при мащаб - което първоначално тълкувах като „прокси кредитът е твърде слаб, когато обучението е по-дълго“. Прегледът на параметрите напълно обърна това:" → "показаха, че коалиционният сигнал изчезва в разширената конфигурация - което първоначално тълкувах като „приносът от заместителя е твърде слаб при по-дълго обучение“. Серията експерименти напълно обърна този извод:"
  - "Коалиции възникват значително *само при ниски стойности на $\alpha$*" → "Коалиционният резултат нараства статистически значимо *само при ниски стойности на $\alpha$*"
  - "(при $\alpha\approx 0$ агентът Shapley побеждава оскъдната базова линия с $+0.038$, ~4.4x)" → "(при $\alpha\approx 0$ агентите с принос по Шапли надминават базовата линия с $+0.038$)"
  - "- оскъдният всичко или нищо член заглушава коалиционния сигнал." → "- членът с рядка награда „всичко или нищо“ заглушава коалиционния сигнал."
  - "(обратното на моето „smoke-положително / мащаб-нула“ тълкуване, което беше артефакт от фиксирането на $\alpha=0.3$ и на двете нива)" → "(обратно на първоначалното ми тълкуване „положителен ефект в пробната, нулев в разширената конфигурация“, което се дължеше на това, че и в двете беше използвано $\alpha=0.3$)"
  - "и **евтиният прокси побеждава скъпия контрафактичен**" → "и **евтиният заместител дава по-силен ефект от скъпата оценка чрез симулации**"
  - "Решението е „да се придаде голяма тежест на коалиционния кредит“, а не „да се изчисли по-точен кредит“." → "Решението е „да се даде голяма тежест на коалиционния принос“, а не „да се изчисли по-точен принос“."
  - "при чисто коалиционен кредит ($\alpha=0$) процентът победи спада до $\sim 0.29$ (близо до $0.25$ случайния минимум)" → "при изцяло коалиционен принос ($\alpha=0$) делът на победите спада до $\sim 0.29$ (близо до нивото на случайната игра $0.25$)"
  - "това е рамката на суровата стъпка, вече количествено изразена." → "точно както беше заложено в плана на главата, но вече количествено."
- **Why:** "Episodic", "smoke" and "Shapley агентите" are English. "коалиция-осъзнатите", "оскъдните агенти" (T05), "кръстосано" (T07), "мащаб" as a noun without a head ("at scale"), "прокси", "побеждава" (a gap does not *beat* anything) and "суровата стъпка" (*raw step*, internal jargon) are calques. "Прегледът на параметрите" (a parameter review) misreads *the sweep*. "контрафактичен" names a credit that is not counterfactual (C02). The tier names "пробна/разширена" should be defined once, at Table 41: "пробна (5 жетона, 400 игри за обучение) и разширена (7 жетона, 1500 игри)". The second reconciliation's claim sentence is replaced in C02.

### F11-B15 · S2 · calques and English — §11.5
- **Where:** summaryBg.md l. 110, 114, 123
- **Now → Proposed:**
  - "За да се използват повторно решавачът на мета-Наш от Глава 9 и **пумпалът** (Hodge) разлагане от Глава 10 - и двата двуигрови инструмента - 4-игровият тензор на печалбата се **проектира** към матрица на двустранни сблъсъци, след което се разделя на **транзитивен** (стълба на умения) компонент и **цикличен** (камък-ножица-хартия) компонент." → "За да се използват повторно решавачът за мета-равновесие на Наш от Глава 9 и разлагането „пумпал“ (на Ходж) от Глава 10 - и двата инструмента за игри с двама играчи - тензорът на печалбите за четирима играчи се **проецира** в матрица на сблъсъците по двойки, която след това се разлага на **транзитивна** (стълба на уменията) и **циклична** (камък-ножица-хартия) компонента."
  - "Глава 10 предвижда, че коалиционните игри всеки срещу всеки ще бъдат силно циклични. Измерено, това зависи изцяло от **популацията, която се разлага** - същият урок, който Глава 10 научава:" → "Глава 10 предвиди, че коалиционните игри всеки срещу всеки ще бъдат силно циклични. Измерванията показват, че това зависи изцяло от **популацията, която се разлага** - същият урок, който даде и Глава 10:"
  - "първоначално видях почти перфектна стълба на умения (cyclic $\sim 0.07$). Това беше отчасти грешката в seat-0 (разделът *Shapley credit*)" → "първоначално видях почти съвършена стълба на уменията (циклично съотношение $\sim 0.07$). Причината беше отчасти грешката с място 0 (раздел 11.3)"
  - "но остава **честно под строго доминиране** (cyclic$^2$ малко под $0.5$)" → "но остава **под прага на строго доминиране** (квадратът на цикличното съотношение е малко под $0.5$)"
  - "Основният заподозрян за остатъка е, че **2-type projection discards 3-/4-player coalition effects** - разлагане, естествено за тензори, е отвореният въпрос." → "Основната вероятна причина е, че **проекцията върху двойки типове губи коалиционните ефекти между трима и четирима играчи**; разлагането директно на тензора остава отворен въпрос."
  - "Нито едното тълкуване не е грешка; коя популация изграждаш решава дали SLS изглежда като колело или стълба." → "Нито едно от двете тълкувания не е грешка: съставът на популацията определя дали SLS изглежда като колело, или като стълба."
- **Why:** "двуигрови" means "of two games" and "4-игровият" "of four games". "проектира" means *designs*, not *projects* (the same trap as F07-T10). "Глава 10 … научава" says chapter 10 *learns*. The rest is English or a literal calque ("честно под", "основният заподозрян", the informal "ти" in "изграждаш").

### F11-B16 · S2 · calques — §11.6 and §11.7
- **Where:** summaryBg.md l. 131, 133, 135, 147, 148
- **Now → Proposed:**
  - "Точните опори са стабилни: sLS двигателят съвпада с 2-играчовата минимакс крайна игра без **нито едно** несъответствие; детекторът възстановява засадена коалиция **точно** ($\{0,1\}$, резултат $10.0$); кодът на Shapley възпроизвежда кооперативни игри-играчки - *включително тяхното ядро* - до четири десетични знака." → "Точните опорни точки са надеждни: двигателят на SLS съвпада с минимаксното решение на крайната фаза с двама играчи без **нито едно** несъответствие; детекторът разпознава **точно** предварително зададената коалиция ($\{0,1\}$, резултат $10.0$); кодът за стойността на Шапли възпроизвежда опростените кооперативни игри - *включително тяхното ядро* - с точност до четвъртия знак след десетичната запетая."
  - "Две честни корекции се предават напред." → "Две поправки остават в сила и за следващите глави."
  - "- **грешка при разпределение на равни резултати** с най-много жетони даде на място 0 приблизително два пъти по-голям дял от справедливия и завиши процента победи на героя от истински $\sim 0.41$ до фалшив $\sim 0.87$; поправено е, но това доказва, че *правилата* на двигателя, а не неговият решавач, са мястото, където се крие рискът." → "- **грешка в правилото при равенство** по брой жетони даде на място 0 около два пъти по-голям дял от справедливия и завиши дела на победите на обучения агент от реалните $\sim 0.41$ до фалшивите $\sim 0.87$; грешката е поправена, но показва, че рискът се крие в *правилата* на двигателя, а не в решавача."
  - "(2) „Коалициите не възникват в голям мащаб“ беше **неправилно зададено тегло на смесване**" → "(2) „Коалициите не възникват в разширената конфигурация“ се оказа следствие от **неподходящо тегло на смесване**"
  - "Методологично ехо от Глави 9-10: **една единствена конфигурация скрива онова, което обхождане с фиксирани начални стойности разкрива.**" → "Методологичен паралел с глави 9-10: **една-единствена конфигурация скрива онова, което разкрива серия експерименти с няколко начални числа.**"
  - "Всяка точна цел (минимакс на крайната игра, кооперативни игри-играчки) е детерминистичен и възпроизводим;" → "Всяка точна проверка (минимаксът на крайната фаза, опростените кооперативни игри) е детерминирана и възпроизводима;"
  - "Постоянното предупреждение е **точност на двигателя**:" → "Основната уговорка остава **верността на двигателя спрямо правилата**:"
  - "- **Коя популация се разлага определя стълбата срещу колелото** (урокът от Глава 10, потвърден):" → "- **Съставът на разлаганата популация определя дали се вижда стълба, или колело** (урокът от Глава 10 се потвърждава):"
  - "която премина точно през своите учебникови проверки" → "която издържа точно учебниковите проверки"
- **Why:** "sLS" is a case artefact. "2-играчовата" is not a word. "грешка при разпределение на равни резултати" means an error in *distributing tied results* (T08). "героя" (T14). "обхождане" (T09). "детерминистичен и възпроизводим" disagrees with "цел" (feminine). "точност" is accuracy, not fidelity. "стълбата срещу колелото" calques "ladder-vs-wheel".

### F11-B17 · S2 · terminology — "Съгласуване" for the reconciliation boxes
- **Where:** summaryBg.md l. 71, 99, 123 (the l. 71 heading is inside B13)
- **EN:** "> **Reconciliation (kept prediction -> what actually happened).**"
- **Now → Proposed:** "> **Съгласуване (запазена прогноза -> какво всъщност се случи).**" (l. 99, 123) → "> **Съпоставка (запазена прогноза → действителен резултат).**"
- **Why:** "съгласуване" means bringing two things into agreement, which suggests adjusting the prediction to fit, the opposite of the honest comparison the boxes make (T15).

### F11-B18 · S2 · One-pager calques
- **Where:** onePagerBg.md
- **Now → Proposed:**
  - "Глави 2–10 се опираха на една опора: двуигрови игра с точен най-добър отговор и предсказвач за експлоатируемост" → "Глави 2–10 се опираха на една опора: игра с двама играчи с точен най-добър отговор и предсказвач за експлоатируемост"
  - "Това представлява границата на тезата, а не стъпка за консолидация." → "Тук е отвореният край на дисертацията, а не етап на затвърждаване."
  - "Създаден е нативен 4-игрови **двигател „Со Лонг Съкър“** - играта от 1950 г., разработена от Неш, Шейпли, Шубик и Хауснер за изследване на съюзите - въз основа на формализацията на De Carufel & Jerade, като единствената му точна опора е **минимакс крайна игра**." → "Създаден е собствен **двигател на So Long Sucker** за 4 играчи - играта на Хауснер, Наш, Шапли и Шубик, публикувана през 1964 г. - по публикуваните правила, като единствената точна опорна точка е **минимаксното решение на крайната фаза**; анализът на крайната фаза на De Carufel & Jerade е еталонът, с който двигателят още не е сверен."
  - "всички награди са **игра с нулева сума**" → "сумата на наградите във всяка игра е **нула**"
  - "(оценка на двойката **10.0**, записи между двойките 0 или -1)" → "(резултат на двойката **10.0**, за останалите двойки 0 или -1)"
  - "а стойността на Шейпли точно възпроизвежда играчките „ръкавица“ и „мнозинство“, включително празнотата на ядрото." → "а стойността на Шапли точно възпроизвежда опростените игри „ръкавици“ и „мнозинство“, включително празното ядро."
  - "чиято **развръзка** по най-нисък индекс даваше на място 0 два пъти повече, отколкото му се полага" → "чието **правило при равенство** (най-малък индекс) даваше на място 0 два пъти повече, отколкото му се полага"
  - "С безпристрастна развръзка симетричното разпределение на Шейпли спадна от **0.525 до 0.013**" → "При безпристрастно разрешаване на равенството размахът на симетричния принос по Шапли спадна от **0.54 до 0.013**" (numbers: C06)
  - "същата поправка намали впечатляващия процент победи на героя от **0.87** до честен **~0.41** спрямо минимум от 0.25. В игра, която почти винаги завършва с равен резултат, правилото за развръзка е носещо." → "същата поправка намали впечатляващия дял победи на обучения агент от **0.87** до реалните **~0.41** при ниво на случайната игра 0.25. В игра, която почти винаги завършва с равен резултат, правилото при равенство е решаващо."
  - "*„Коалициите не възникват в голям мащаб“ беше опровергано чрез намирането на правилния регулатор.*" → "*„Коалициите не възникват в разширената конфигурация“ се опроверга, след като беше открит решаващият параметър.*"
  - "а евтиният заместващ показател за критична стойност превъзхожда скъпия контрафактичен кредит" → "а евтиният заместител, изчислен от оценките на критика, дава по-силен ефект от скъпия принос чрез симулации"
  - "по същество случаен минимум" → "практически нивото на случайната игра"
  - "*Силно цикличен, честно казано недостатъчен.*" → "*Силна циклична компонента, но под прага.*"
  - "Съгласуването на модела за **ход** и **развръзка** на **двигателя** с този на De Carufel & Jerade представлява най-ценното последващо действие" → "Най-ценната следваща стъпка е да се сверят правилата на **двигателя** за реда на ходовете и за **равенството** с формализацията на De Carufel & Jerade"
  - "а теоремите остават непроверени за четене" → "а теоремите на статията още не са проверени"
- **Why:** "двуигрови" means "of two games". "нативен" and "4-игрови" are calques. "Неш" is a third spelling. "всички награди са игра с нулева сума" says the rewards *are a game*. "носещо" (*load-bearing*) is a building term. "честно казано недостатъчен" means "frankly inadequate", which is harsher than the EN. "непроверени за четене" does not parse. Also T01, T08, T12, T14. The origin sentence also carries S01 and S03.

### F11-B19 · S2 · The official BG title in `subtitle:` differs from the fixed wording (corpus-wide)
- **Where:** summaryBg.md l. 9 and onePagerBg.md l. 9 (the same in all 24 BG summary/one-pager files).
- **Now → Proposed:** "subtitle: \"Изследване върху възможностите за прилагане на изкуствен интелект в компютърните игри\"" → "subtitle: \"Изследване на възможностите за приложение на изкуствения интелект в компютърни игри\""
- **Why:** The comment block at the top of each file fixes the official title, and its instruction reads "keep consistent across all documents". Fix it once with a replace across all 24 files. It matters wherever the per-step PDFs print the subtitle.

### F11-B20 · S3 · typography (not covered by the central decisions)
- **Where:** summaryBg.md "->" 6× (l. 48, 71, 99, 123 and in figure labels); "~2x", "~4.4x" (l. 72, 99, 131, 144); "Принос #3", "Принос #2" (l. 137, 146) next to "Принос №1–3"; "под-игра" (l. 31, 143); "Глава 07" (l. 48); "n-играчен", "n-играчи" (l. 63, 146) where the EN has $N$.
- **Fix:** "->" → "→"; "~2x" → "~2×"; "#" → "№"; "под-игра" → "подигра"; "Глава 07" → "Глава 7"; "n-играч…" → "N играчи".

## T — Glossary-level terminology

### F11-T01 · S1 · "critic-value proxy → заместващ показател за критична стойност"
- **Where:** `glossary_settled.md` (freq 3). Printed: summaryBg l. 84 "евтин заместител с критична стойност"; onePagerBg "евтиният заместващ показател за критична стойност"; report_bg l. 99.
- **Now → Proposed:** → "заместител, изчислен от оценките на критика" (the settled "critic → оценител" is also fine: "…от оценките на оценителя").
- **Why:** "критична стойност" is a statistical threshold (*critical value*). The proxy is computed from the *critic* network's value estimates. This is a meaning error.

### F11-T02 · S1 · Entries whose Bulgarian side is English
- **Where:** `glossary_settled.md`: "egta meta-game → EGTA Meta-Game", "egta meta-game analysis → EGTA Meta-Game Analysis", "egta cyclic ratio → EGTA Cyclic Ratio", "egta + spinning-top → EGTA + Spinning-Top", "coalition-aware mappo → Coalition-Aware MAPPO", "rollout shapley → Rollout Shapley"; figure mapping "(skill ladder)", "(coalition wheel)".
- **Now → Proposed:** → "мета-игра на EGTA", "анализ на мета-играта с EGTA", "циклично съотношение (EGTA)", "EGTA + разлагане „пумпал“", "MAPPO с отчитане на коалициите", "принос по Шапли чрез симулации"; "(стълба на уменията)", "(колело от коалиции)".
- **Why:** Rule 2 keeps only abbreviations in Latin script. These entries put English phrases into the printed BG (B01, B02, G08).

### F11-T03 · S1 · "behavioral prior → поведенчески априорен разпредел"
- **Where:** `glossary_settled.md` (freq 4). Printed: summaryBg l. 137 (2×) and l. 146 (both rewritten in C04 and C05).
- **Now → Proposed:** → "поведенческа опорна стратегия" (for piKL's anchor policy), or "поведенческо априорно разпределение" where a distribution is meant.
- **Why:** "разпредел" is not a Bulgarian word.

### F11-T04 · S1 · "pre-fix artifact → представка-артефакт"
- **Where:** `glossary_settled.md`; printed at l. 135 (B05).
- **Now → Proposed:** → "резултат отпреди поправката"
- **Why:** "представка" is a grammatical prefix. The entry parsed *pre-fix* as *prefix*.

### F11-T05 · S2 · "sparse reward → оскъдна награда"; "sparse agent → оскъдни агенти"; "sparse baseline → оскъдна базова линия"
- **Where:** `glossary_settled.md` (freq 8 / 1 / 1). The chapter also has "разредената базова линия" (Table 41 caption). There are 8 "оскъд-" forms in the summary and 1 in the one-pager (fixed in B08, B14, C02, C06).
- **Now → Proposed:** → "рядка награда", "агенти с рядка награда", "базова линия с рядка награда"
- **Why:** "оскъдна" means meagre or scarce. In RL a *sparse* reward is one that is rarely non-zero. "Оскъдни агенти" means "impoverished agents".

### F11-T06 · S2 · "shapley value → стойност на Шейпли"; "shapley credit → стойност на Шейпли"; "coalition credit → коалиционен кредит"
- **Where:** `glossary_settled.md` (freq 14, 7, 3) vs curated `terminology_EN_BG.md` "Стойност на Шапли". The brief's Latin-name list and the figure validator ("names lost: ['Shapley']") say "Shapley".
- **Now → Proposed:** → "стойност на Шапли" (the curated form, parallel to "равновесие на Наш"), "принос по Шапли", "коалиционен принос". Decide Cyrillic vs Latin once, and align the validator's name list with the decision.
- **Why:** Three written forms in one chapter (B08). *Credit* is not *value*, and "кредит" is a loan.

### F11-T07 · S2 · "5-seed paired sweep → петкратно кръстосано сравнение по двойки"
- **Where:** `glossary_settled.md` (freq 2); printed at l. 88, 131, 135.
- **Now → Proposed:** → "сдвоени сравнения с 5 начални числа"
- **Why:** "петкратно кръстосано" reads as five-fold *cross*-validation, a different procedure. This is a sibling of the pilot's F07-T09 (sweep → "обхождане").

### F11-T08 · S2 · tie-break and deadlock entries
- **Where:** `glossary_settled.md`: "tie-break → развръзка", "tie-break rule → правило за развръзка", "deadlock tie-break → развръзка при задънена улица", "engine tie-break artifact → артефакт на развръзка при равенство в двигателя"
- **Now → Proposed:** tie-break → "разрешаване на равенството" / "правило при равенство"; deadlock → "пат" (the one-pager already uses "патова ситуация")
- **Why:** "развръзка" is the dénouement of a plot, and "задънена улица" is a physical dead end. The mistranslation spread into "грешка при разпределение на равни резултати" (B16).

### F11-T09 · S2 · "planted alliance/coalition → засаден съюз / засадена коалиция"
- **Where:** `glossary_settled.md`; printed at l. 44, 131, one-pager, fig. 64.
- **Now → Proposed:** → "предварително зададен съюз / предварително зададена коалиция"
- **Why:** "засаден" means planted like a tree, and next to "засада" (ambush) it misleads. The one-pager even puts it in quotation marks.

### F11-T10 · S2 · "mode → мода"; "credit mode → мода на приписване"
- **Now → Proposed:** → "вид", "вид на приноса" (or "режим", as in "режим на отказ")
- **Why:** "мода" means fashion (B06).

### F11-T11 · S2 · "spread → разпределение"; "symmetric spread → симетрично разпределение"
- **Now → Proposed:** → "размах" ("размах на симетричния принос")
- **Why:** The spread here is max − min over seats. "Разпределение" (distribution) says something else and clashes with "разпределение на кредита" in the same sentence (l. 67).

### F11-T12 · S2 · "random floor → случаен минимум"
- **Where:** `glossary_settled.md` (freq 4); l. 104, 145, one-pager.
- **Now → Proposed:** → "нивото на случайната игра" (or "шанс при случайна игра")
- **Why:** "случаен минимум" means "an accidental minimum". The 0.25 is the win rate of random play, not a floor: one trained cell scores 0.216, below it (C06).

### F11-T13 · S2 · "cooperative-GT toys → кооперативни игри-играчки"; "toy scale → игрови мащаб"
- **Now → Proposed:** → "опростени (учебни) кооперативни игри"; → "мащаб на опростен модел"
- **Why:** "игри-играчки" calques *toy games*, and "игрови мащаб" (*game scale*) loses *toy* entirely. The settled "toy-game solutions → решения на опростени игрови модели" already shows the right form.

### F11-T14 · S2 · "wheel of counters → колело от броячи"; "coalition counters → коалиционни жетони"
- **Now → Proposed:** → "колело от контрастратегии"; → "контрастратегии между коалициите"
- **Why:** *Counters* here are counter-strategies (rock-paper-scissors), not counting devices or tokens. This matters for the fig. 70 caption.

### F11-T15 · S2 · "reconciliation → съгласуване"; "prediction reconciliation → съгласуване на прогнозата с действителността"
- **Now → Proposed:** → "съпоставка" / "съпоставка на прогнозата с резултата"
- **Why:** "Съгласуване" means reconciling in the sense of making things agree, which suggests adjusting the prediction. The corpus uses it for an honest prediction-vs-result comparison (B17). It affects every chapter with these boxes.

### F11-T16 · S3 · "self-play → самообучение"
- **Where:** `glossary_settled.md` (e.g. "model-free self-play → самообучение без използване на модел"); l. 82, one-pager, report.
- **Now → Proposed:** → "игра срещу себе си" (or "обучение чрез игра срещу себе си")
- **Why:** "самообучение" means self-study or self-learning and loses *play*. This is low priority, but high frequency across chapters 9–12.

## C — Content

### F11-C01 · S1 · The reward formula is the inverse of the code
- **Where:** summaryEn l. 136 and summaryBg l. 83 (identical string); report_en and report_bg l. 99; fig. 68 (G06). The code: `coalition_mappo.py` l. 9 and l. 110: `R = alpha * sparse + (1 - alpha) * credit_centered`.
- **Problem:** The text says $r=(1-\alpha)r_{\text{sparse}}+\alpha\cdot\text{credit}$, under which $\alpha=0$ is *pure sparse*. The same chapter then calls $\alpha=0$ "pure coalition credit", and so do the code, the sweep plot's x-label and fig. 68's note. A reader who trusts the formula reads every $\alpha$ result backwards.
- **Now → Proposed:**
  - summaryBg l. 83: "$$ r = (1-\alpha)\,r_{\text{sparse}} \;+\; \alpha\,\text{(Shapley coalition credit)}, $$" → "$$ r = \alpha\,r_{\text{sparse}} \;+\; (1-\alpha)\,\text{(коалиционен принос по Шапли)}, $$"
  - summaryEn l. 136: the same string → "$$ r = \alpha\,r_{\text{sparse}} \;+\; (1-\alpha)\,\text{(Shapley coalition credit)}, $$"
  - summaryBg l. 84: "където $r_{\text{sparse}}$ е наградата „всичко или нищо“, а кредитният член представлява стойността на Шейпли за вероятността от победа от раздела *коалиционен кредит* (евтин заместител с критична стойност, или скъпо контрафактично разгръщане). Теглото на смесване $\alpha$ определя баланса между „просто победи“ и „формирай коалиции“." → "където $r_{\text{sparse}}$ е рядката награда „победителят взема всичко“, а вторият член е центрираният принос по Шапли от раздел 11.3 - изчислен или евтино, от оценките на критика, или по-скъпо, чрез симулации (в кода „counterfactual“). Теглото $\alpha$ определя баланса между „просто победи“ ($\alpha=1$) и „формирай коалиции“ ($\alpha=0$)."
  - summaryEn l. 137–139: "the credit term is the win-probability Shapley value from the *Shapley credit* section (a cheap critic-value **proxy**, or an expensive rollout **counterfactual**). The blend weight $\alpha$ dials between "just win" and "form coalitions."" → "the second term is the centered Shapley credit from the *Shapley credit* section, computed either cheaply from critic values (**proxy**) or by rollouts (**counterfactual** in the code). The weight $\alpha$ dials between "just win" ($\alpha=1$) and "form coalitions" ($\alpha=0$)."
  - report_en/report_bg l. 99: "$r = (1-\alpha)\cdot r_\text{sparse} + \alpha \cdot \text{credit}$" → "$r = \alpha\cdot r_\text{sparse} + (1-\alpha) \cdot \text{credit}$"

### F11-C02 · S1 · The "Shapley coalition credit" carries no coalition information; "coalitions can be learned" is not shown
- **Where:** summaryEn l. 109–113, 134–139, 157–167, 217–218, 249–252; summaryBg l. 67, 84, 99–100, 131, 144; one-pager "Key results"; report Exp. 4.
- **Problem** (verified by reading the code and by a numerical check with the chapter's own functions):
  1. **Rollout ("counterfactual") credit.** `shapley.py` l. 113 sets $v(S)=\sum_{i\in S}\hat P(i\text{ wins})$. This is an *additive* (inessential) game, so the Shapley value of player $i$ is simply its own win probability. `exact_shapley` returns [0.4, 0.3, 0.2, 0.1] for win probabilities [0.4, 0.3, 0.2, 0.1]. In training it is computed once per batch, from the initial state (`_counterfactual_credit`), so every game in a batch gives player $p$ the same credit, whatever it did. Nothing is counterfactual: no player is removed and no action is replaced. For inessential games, "there is no tendency for the players to form coalitions" (Ferguson, *Game Theory* notes, Part IV §2.2; verified in the PDF text).
  2. **Proxy credit.** With $v(S)\propto(1+s|S|)\sum_{i\in S}y_i$, the centered Shapley value is $c\,(1+sn/2)\,(y_i-\bar y)$, i.e. each agent's own mean critic value minus the table mean. Synergy only rescales it: the ratio credit/(y − ȳ) is constant across players in every test.
  3. **Metric.** The "coalition score" is `mean_offdiagonal_coalition` = the mean of $|C_{ij}|$ (`coalition_detector.py` l. 96–103). It rises with mutual *hostility* as much as with support. Its magnitudes are tiny: sparse 0.011 and Shapley 0.048 per game, against 10.0 for the planted pair.
  4. So the low-$\alpha$ result shows that *replacing the win reward with a dense, coalition-free signal changes the interaction pattern* (and win rate falls to 0.29; the rollout-credit cell falls to 0.216, below random). It does not show coalition-aware learning. The needed control is a dense reward with no coalition content, which the proxy already is.
- **Now → Proposed** (BG; the EN is parallel):
  - l. 100: "Така че основният сигнал на тезата (коалиционно формиране) е реален и устойчив - просто го измерих в единствения режим, в който оскъдният член го скрива." → "Ефектът е устойчив при ниско $\alpha$ и просто не се вижда в режима, в който преобладава членът с рядка награда; дали той отразява формиране на коалиции, още не е проверено (вж. уговорката по-долу)."
  - After l. 100, add a paragraph (outside the quote): "**Уговорка за механизма.** В `shapley.py` стойността от симулациите е $v(S)=\sum_{i\in S}P(i \text{ печели})$ - адитивна игра, в която стойността на Шапли на всеки играч е просто собствената му вероятност за победа. Центрираният принос на заместителя е пропорционален на собствената оценка на критика за агента минус средната за масата; синергията само го мащабира. Нито един от двата сигнала не показва кой на кого помага, а коалиционният резултат е средната *абсолютна* взаимна нетна подкрепа и расте и при взаимна враждебност. Ефектът при ниско $\alpha$ следователно показва, че замяната на наградата за победа с плътен сигнал променя взаимодействията между агентите; дали така възникват коалиции, изисква контролен експеримент с еднакво плътна награда без коалиционна информация."
  - l. 131: "И основното твърдение за обучението оцелява при петкратно кръстосано сравнение по двойки: обучението с отчитане на коалициите произвежда значително повече поведение на коалиция ($+0.038$, ~4.4x) в ниския $\alpha$ режим." → "Основният резултат от обучението се потвърждава в сдвоени сравнения с 5 начални числа: при ниско $\alpha$ коалиционният резултат е значимо по-висок ($+0.038$), макар че, както е реализиран, приносът по Шапли не носи информация за коалициите (раздел 11.4)."
  - l. 144: "- **Коалициите могат да бъдат *научени* - но само ако се претегли кредитът.** Сигналът за коалиция на Шапли превъзхожда оскъдната награда с $+0.038$ (~4.4x, 5 семена) при ниска $\alpha$ и е *потиснат* при $\alpha\ge 0.3$; ефектът нараства с размера на играта, а евтиният заместващ сигнал превъзхожда скъпия контрафактичен." → "- **Коалиционният резултат расте, когато наградата за победа се замени с плътен сигнал, но това още не доказва научени коалиции.** При $\alpha\approx 0$ коалиционният резултат на агентите с принос по Шапли надвишава този на агентите с рядка награда с $+0.038$ (5 начални числа, разширена конфигурация), а при $\alpha\ge 0.3$ ефектът изчезва. Както е реализиран, приносът не показва кой на кого помага, а коалиционният резултат отчита и враждебните взаимодействия; нужна е контролна награда без коалиционна информация."
  - EN takeaway l. 249–252 → "- **Replacing the win reward with a dense credit raises the coalition score, which is not yet evidence of learned coalitions.** At $\alpha\approx 0$ the Shapley-credit agents' coalition score exceeds the sparse agents' by $+0.038$ (5 seeds, scale tier); at $\alpha\ge 0.3$ the effect vanishes. As implemented, the credit does not encode who helped whom (the proxy reduces to each agent's own critic value minus the table mean, the rollout variant to its own win-probability share), and the coalition score also counts hostile interactions; a coalition-free dense-reward control is needed."
  - Optional, for consistency: rename "coalition-aware MAPPO" → "MAPPO with a Shapley-shaped reward" in the headings, or implement a credit that uses the detector's help/harm matrix.

### F11-C03 · S1 · Engine artefacts presented as properties of So Long Sucker
- **Where:** summaryEn l. 53–55, 121; summaryBg l. 29, 74 (the l. 74 fix is in B13); one-pager EN and BG "~99.5% of random games end in deadlock".
- **Problem:**
  1. *Negotiation.* SLS is a bargaining game. Its 1964 introduction says it "depends almost completely on the bargaining ability and the persuasiveness of the players" (quoted in Burnett, *Cabinet* 45, 2012). De Carufel & Jerade's abstract lists "players taking turns but not in a fixed order, agreements made between some players broken at any time" (arXiv abstract, verified). The engine omits both the negotiation and the choice of the next player (`sls_game.py`, NOTE (a)). "There is no separate negotiation phase to model" therefore describes the engine, not SLS. This matters for the fair-play angle: real collusion happens off the board, and the detector only sees the board.
  2. *Deadlocks.* "~99.5% of random SLS games end in a deadlock" is a property of the simplified ruleset (NOTE (b): an empty-handed player is *skipped*; NOTE (c): a most-chips tie-break for "the (rare) all-stuck deadlock", whose rarity the engine's own notes expected). Almost every game in this engine is decided by a tie-break, a strong caveat on every win rate in the chapter.
- **Now → Proposed:**
  - summaryBg l. 29: "Целият съюз е **кодиран в самите ходове** - няма отделна **фаза** за преговори, която да се моделира, което е именно причината детекторът да може да прочете коалицията директно от потока на **ходовете**." → "В двигателя на тази глава съюзът е **кодиран изцяло в ходовете**: преговорите, които в истинската игра са свободни и необвързващи, не се моделират, затова детекторът може да прочете коалицията директно от потока от ходове."
  - summaryEn l. 54–55: "The whole alliance is **encoded in the moves themselves** — there is no separate negotiation phase to model" → "In this chapter's engine the alliance is **encoded entirely in the moves**: the free, unenforceable negotiation of the real game is not modelled"
  - summaryEn l. 121: "**~99.5% of random SLS games end in a deadlock**" → "**~99.5% of random games in this engine end in a deadlock** (a consequence of its simplified rules, which skip a player with an empty hand)"; one-pager EN "**~99.5% of random games end in deadlock**" → "…**in this engine**"; onePagerBg "**~99.5% от случайните игри завършват с патова ситуация**" → "**~99.5% от случайните игри в този двигател завършват с пат**".

### F11-C04 · S1 · Stale forward links and "Step" naming
- **Where:** summaryEn l. 235–240 and summaryBg l. 137 ("**Chapter 12** (language / negotiation, CICERO / Welfare-Diplomacy)", "**Chapter 14** inherits"); EN "Step-10" (l. 208, 258); EN "exactly the raw step's framing" (l. 173); EN "in the step" (l. 57); BG "стъпка/стъпката" (l. 27, 63, 104); footnote "Step 09"; figs. 64 and 70 (G02, G08).
- **Problem:** Chapter 14 was never written. Chapter 12 ("Sequence Models and LLM Agents in Strategic Settings") mentions neither negotiation, CICERO, Diplomacy, piKL nor coalitions (checked by grep).
- **Now → Proposed:** summaryBg l. 137 "**Обратни и напредни връзки.** Обратно: детекторът е моделът на противника от Глава 7, разширен до социална структура; мета-Наш и пумпалът са Глави 9–10, приложени повторно върху проектираната мета-игра; празното ядро прави невъзможно определянето на „безопасно = ограничено отклонение от Нашово равновесие“ от Глава 8, което налага използването на поведенческия априорен разпредел на piKL. Напред: празнината в безопасността, свързана с поведенческия априорен разпредел, насочва към **Глава 12** (език / преговори, CICERO / Welfare-Diplomacy), а eGTA-tensor evaluation е многоагентното обобщаване на експлоатируемост, което **Глава 14** наследява (Принос #3)." → "**Връзки с другите глави.** Назад: детекторът е моделът на противника от Глава 7, пренесен към социалната структура; мета-равновесието на Наш и разлагането „пумпал“ от глави 9–10 се прилагат повторно върху проецираната мета-игра; без минимаксна стойност и при празно ядро определението от Глава 8 „безопасно = ограничено отклонение от равновесието на Наш“ губи опората си, а регуларизацията към поведенческа опорна стратегия (по подобие на piKL) остава кандидат без гаранция. Напред: Глава 12 разглежда езиковите модели като стратегически агенти, но не и договарянето; безопасността при N играчи (Принос №2) и оценката чрез EGTA върху тензора на печалбите като многоагентно обобщение на експлоатируемостта (Принос №3) остават задачи на дисертацията." EN l. 235–240 in parallel. Also: "Step-10" → "Chapter 10"; "exactly the raw step's framing, now quantified" → "exactly as the chapter's plan framed it, now quantified"; "in the step" → "in the chapter".

### F11-C05 · S2 · "Empty core ⇒ safe play needs piKL" is argued the wrong way round
- **Where:** summaryEn l. 33–35, 103–105, 236–238, 255–257; summaryBg l. 21, 63, 146 (l. 137 is in C04); one-pager "Thesis connection"; fig. 66.
- **Problem:**
  1. Chapter 8's safety fails for $N\ge3$ because there is no minimax value [Brown & Sandholm 2019], not because of the core.
  2. The empty core is asserted for SLS but not shown. The only SLS coalition function in the chapter (§11.3) is additive, and its core is *non-empty*: it is the single point of individual win probabilities. The claim can be supported, though: an essential constant-sum game has an empty core (Ferguson, Part IV §2.3, Thm 1, verified; attributed to Owen). SLS is constant-sum (one winner), and a lone player cannot guarantee a win.
  3. piKL anchors to an imitation-learned human policy and gives no worst-case guarantee (`lit_gaps.md`, C2 Correction 2). KL-anchoring an exploiter to a behavioural baseline is the thesis's own proposal, not an established N-player safety recipe.
- **Now → Proposed:**
  - l. 21: "- при празно ядро няма стабилно разпределение, така че „безопасно“ трябва да стане поведенческа/популационна (piKL), пропускът, който тази глава очертава, но не запълва (Принос №2)." → "- без минимаксна стойност и при празно ядро няма стабилно разпределение, на което да се опре безопасността; регуларизация към поведенческа опорна стратегия по подобие на piKL е кандидат, но не дава гаранция - празнина, която главата очертава, но не запълва (Принос №2)."
  - l. 63: "Това е ситуацията в SLS - и причината n-играчен „безопасен“ стил на игра да не може да бъде основан на стабилно равновесие (Принос №2)." → "SLS е игра с постоянна сума (печели само един), а всяка съществена игра с постоянна сума има празно ядро; следователно и коалиционната игра на SLS, в която стойността на коалицията е гарантираната ѝ вероятност за победа, няма стабилно разпределение. Заедно с липсата на минимаксна стойност при повече от двама играчи това обяснява защо „безопасната“ игра при N играчи не може да се опре на стабилно равновесие (Принос №2)."
  - l. 146: "- **Празното ядро $\Rightarrow$ означава структурна нестабилност.** Празното ядро на играта на мнозинството е ситуацията в SLS: не съществува стабилно разпределение, така че коалициите *ще* се разпадат - поради което „безопасната“ игра при n-играчи изисква поведенчески априорен разпредел (piKL), а не закотвяне в Наш/ядро (Принос #2)." → "- **Празното ядро означава структурна нестабилност.** Като игра с постоянна сума SLS има празно ядро, както играта на мнозинството: няма стабилно разпределение и коалициите *ще* се разпадат. Затова „безопасната“ игра при N играчи не може да се закотви в равновесие на Наш или в ядрото; регуларизацията към поведенческа опорна стратегия (по подобие на piKL) е кандидат, а не гаранция (Принос №2)."
  - EN l. 255–257 in parallel ("As a constant-sum game, SLS has an empty core, like the majority game … a behavioral anchor in the spirit of piKL is a candidate, not a guarantee"). Add the constant-sum theorem with a textbook citation (see To verify in the extract).

### F11-C06 · S2 · Numbers that do not match the results files
- **Where / Problem → Proposed:**
  1. "~4.4x the sparse baseline" (summary Table 41, text l. 161/99, l. 218/131, l. 250/144; one-pager; report; figs. 68–69). From `sweep_scale.json`: gap 0.0376 / sparse 0.0109 = **3.5×**. It is the Shapley agents' *score* (0.0484) that is **4.5×** the sparse one. BG Table 41: "(~4.4 пъти над оскъдната базова линия)" → "(резултатът на агентите с принос е ~4.5 пъти този на базовата линия)". One-pager BG: "(~4.4 пъти по-голяма от оскъдните **0.0109**)" → "(резултатът на агентите с принос е ~4.5 пъти по-висок от **0.0109** при рядката награда)". EN analogously.
  2. "any tier, $\alpha \ge 0.3$ | $-0.001 \ldots -0.004$ (negative)". Scale cells range **−0.0003 … −0.0035** (all negative). Smoke cells range **−0.0031 … +0.0012**: the rollout-credit cell at α = 0.3 is positive, none is significant. BG: "| всяко ниво, $\alpha \ge 0.3$ | $-0.001 \ldots -0.004$ (отрицателна) |" → "| разширена, $\alpha \ge 0.3$ | $-0.0003 \ldots -0.0035$ (навсякъде отрицателна; в пробната: $-0.003 \ldots +0.001$, без значими) |". In the text: "докато *всяка* клетка с $\alpha\ge 0.3$ е отрицателна" → "докато *всяка* клетка с $\alpha\ge 0.3$ в разширената конфигурация е отрицателна". The report tables (l. 116, 118) need the same correction.
  3. The takeaway (EN l. 253) says "$\alpha=0$ drops win-rate to the $\sim 0.25$ floor" but the body says ~0.29 (0.2875 in the headline cell; 0.216 for rollout credit). BG l. 145: "$\alpha=0$ понижава процента на победи до $\sim 0.25$ минимум; $\alpha\ge 0.1$ restores $\sim 0.52$ - формирането е първично, победата вторична, количествено определено." → "$\alpha=0$ понижава дела на победите до $\sim 0.29$, близо до нивото на случайната игра ($0.25$); при $\alpha\ge 0.1$ той се възстановява до $\sim 0.52$. Формирането на коалиции е основната цел, а победата - второстепенна, и това вече е измерено."
  4. The one-pager (EN and BG) gives "0.525 -> 0.013". 0.525 is the pre-fix *scale* run and 0.013 the post-fix *smoke* run; the summary uses 0.54 → 0.013 (smoke both). → "0.54 -> 0.013".
  5. (S3) "Skill-ladder pool 0.25-0.31": 0.31 comes from the pre-fix `scale_results.json`, which the chapter says is "cited only as evidence of the bug". Either quote 0.25 (smoke, post-fix) or rerun the scale tier.

### F11-C07 · S2 · "Grows with game size" is confounded; ">2 SE" with 5 seeds
- **Where:** summaryEn l. 163, 251 and summaryBg l. 100, 144 (C02 rewrites 144); one-pager "(~10x smoke)"; report.
- **Problem:** The smoke tier is 5 chips and 400 training games; the scale tier is 7 chips and 1500 games, so size and training length change together. "~10x" is 12.6× on synergy 0.1 (0.0305/0.0024) and 45× on synergy 0.3. With 5 seeds, "mean > 2 SE" corresponds to two-sided p ≈ 0.12 (t with 4 df). The headline cells clear 3 SE (3.7, 4.9 and 3.1 SE), but the report's "+0.0305 ± 0.0130 **" (2.35 SE) does not survive a t-test.
- **Now → Proposed:** BG l. 100 "ефектът **нараства с размера на играта**" → "ефектът е **по-голям в разширената конфигурация** (7 жетона и 1500 игри за обучение срещу 5 и 400), така че размерът на играта и продължителността на обучението не са разделени"; EN "the effect **grows with game size**" → "the effect is **larger in the scale tier** (7 chips, 1500 training games vs 5 and 400), so game size and training length are confounded". One-pager "(~10x smoke)" → "(12× the smoke tier at the same synergy)". In the definition of `**` add "(with 5 seeds, ≈ p < 0.12)".

### F11-C08 · S2 · "Strongly cyclic (a wheel)" while the transitive part is larger; "lower bound"; missing artefact
- **Where:** Table 42 (EN l. 194, BG l. 119); fig. 70 caption "so the cyclic ratio is a lower bound"; figs. 70–71.
- **Problem:** The ratios are Frobenius-norm shares whose squares sum to 1. Cyclic 0.57–0.69 means the cyclic share of variance is 0.32–0.48, so the transitive part is still larger in both runs. The chapter's own reconciliation says so ("just under 0.5"), yet the table calls it "a wheel". "Lower bound" is unsupported, because a projection can remove cycles as well as add them. The coalition-pool numbers exist only in `EXECUTION_NOTES.md`; no results file holds them (G09).
- **Now → Proposed:** "| Коалиционен пул (стратегии „съюзник/предател“) | $\sim 0.57$-$0.69$ | силно цикличен (колело) |" → "| Коалиционна популация (стратегии „съюзник/предател“) | $\sim 0.57$-$0.69$ | силна циклична компонента; транзитивната е малко по-голяма |"; EN "| strongly cyclic (a wheel) |" → "| strong cyclic component; transitive still slightly larger |". Caption: "is a lower bound" → "may be underestimated" (G01). Save the check-5 output to JSON.

### F11-C09 · S2 · "Exploitability has no meaning against a coalition"; EGTA "replaces" it
- **Where:** summaryEn l. 35–36; summaryBg l. 21; fig. 70 note.
- **Problem:** With N players, exploitability (NashConv) is still defined. It measures distance from equilibrium, not a guarantee. Against a coordinated coalition the worst-case notion is the team-maxmin value [Celli & Gatti 2018; Zhang et al. 2021] (`lit_evaluation.md` failure mode 2). EGTA ranks a population empirically and is not a worst-case substitute.
- **Now → Proposed:** BG "И **EGTA Meta-Game + стойност на Шейпли** заменя експлоатируемостта, която няма смисъл срещу коалиция (Принос №3)." → "Мета-играта на **EGTA** и **приносът по Шапли** заместват експлоатируемостта, която при повече от двама играчи вече не показва какво е гарантирано на агента, още по-малко срещу коалиция (Принос №3)."; EN "replaces\nexploitability, which has no meaning against a coalition" → "stand in for exploitability, which with more than two players no longer measures what an agent is guaranteed, least of all against a coalition".

### F11-C10 · S2 · The detector is validated on one scripted, overt pair
- **Where:** summaryEn l. 76–79 and summaryBg l. 44; "Contribution #1 made concrete" (report); the one-pager.
- **Problem:** The only test is two scripted players who "systematically help each other and harm the rest", in an engine where alliances can *only* be expressed on the board (C03). There is no false-positive test on non-colluding play, no noisy or covert colluder, and no learned play. It is a sanity check, not evidence for collusion detection. Given the thesis's fair-play angle, the limitation should be stated.
- **Now → Proposed:** after "Коалицията се разпознава напълно само по начина, по който се поставят жетоните." (B10) add: "Това е проверка срещу една програмирана, открито действаща двойка; честотата на фалшивите тревоги при игра без съюзи и разпознаването на прикрити съучастници не са проверявани." EN: after "The alliance is fully legible from chip placement alone." add "This is a sanity check against one scripted, overt pair; false positives on non-colluding play and covert colluders were not tested."

### F11-C11 · S3 · Shapley "the unique fair way"
- **Where:** summaryEn l. 91 and summaryBg l. 54; fig. 66.
- **Problem:** The Shapley value is the unique value satisfying Shapley's axioms. "Fair" is an interpretation. In the glove game the Shapley point (2/3, 1/6, 1/6) lies *outside* the core {(1,0,0)} (worked in `targetedReading/summary.md` MF-1), so "fair" and "stable" diverge in the chapter's own table.
- **Now → Proposed:** "единственият справедлив начин за разпределяне на стойността на една коалиция между нейните членове" → "единственото разпределение на стойността на коалицията между членовете ѝ, което удовлетворява аксиомите на Шапли (ефективност, симетрия, нулев играч, адитивност)"; EN "the unique fair way to split a coalition's worth among its members" → "the unique split of a coalition's worth that satisfies Shapley's axioms (efficiency, symmetry, null player, additivity)".

## S — Sources

### F11-S01 · S2 · SOURCE_GAPS row 1: "играта от 1950 г., която … проектираха именно за да изучават това" → cite the 1964 publication and soften
- **Where:** summaryBg l. 19 (with S04); EN l. 19–21; one-pager (B18); report l. 9.
- **Verification:**
  - Wikipedia states "invented in 1950", but its only reference is the 1964 chapter: Hausner, M., Nash, J., Shapley, L., Shubik, M. (1964), "So Long Sucker - A Four-Person Game", in M. Shubik (ed.), *Game Theory and Related Approaches to Social Behavior*, Wiley, pp. 359–361. The book exists (OUP *Social Forces* review listing "Wiley, 1964, 390 pp."; Internet Archive record); I did not see the chapter itself.
  - De Carufel & Jerade (arXiv HTML v2) say "In 1964, the game So Long Sucker was developed by …".
  - Burnett (*Cabinet* 45, 2012) says "late-1950s" and quotes the 1964 introduction: "depends almost completely on the bargaining ability and the persuasiveness of the players".
  - The year 1950 therefore has no citable primary source. "Designed to study exactly this [alliances]" is a paraphrase; the source says bargaining.
- **Proposal (cite and soften):** "Тя изгражда първото обучение с подкрепление, отчитащо **коалиции** в **So Long Sucker (SLS)** - играта от 1950 г., която Наш, Шапли, Шубик и Хауснер проектираха именно за да изучават това - и я използва, за да осмисли прехода от $N=2$ към $N\ge 3$," → "Тя използва **So Long Sucker (SLS)** - играта за четирима на Хауснер, Наш, Шапли и Шубик, публикувана през 1964 г., в която изходът зависи почти изцяло от договарянето между играчите[^hausner1964], - и допълва единствения публикуван подход с обучение с подкрепление за нея[^sharan2024], чиито агенти не отчитат **коалициите**, с детектор на коалиции и награда по Шапли. Играта служи, за да се осмисли прехода от $N=2$ към $N\ge 3$,". New footnote: `[^hausner1964]: Hausner, M., Nash, J., Shapley, L. & Shubik, M. (1964). "So Long Sucker - A Four-Person Game." В M. Shubik (Ed.), *Game Theory and Related Approaches to Social Behavior*, 359–361. New York: Wiley.` EN parallel: "It uses **So Long Sucker (SLS)** — the four-player bargaining game of Hausner, Nash, Shapley & Shubik, published in 1964 [hausner1964] — and extends the only published RL treatment of it [sharan2024], whose agents are coalition-blind, with a coalition detector and a Shapley-based reward. It uses the game to internalize the jump…"

### F11-S02 · S1 · SOURCE_GAPS rows 2 and 4: Nash in 4-player FFA "intractable and strategically empty" → cite Brown & Sandholm (2019) and Daskalakis et al. (2009), soften "empty"
- **Where:** summaryBg l. 27 and l. 143; EN l. 46–48 and l. 246–248; the one-pager (B03).
- **Verification:**
  - Brown & Sandholm, "Superhuman AI for multiplayer poker," *Science* 365(6456):885–890, 2019, DOI 10.1126/science.aay2400. I read the full-text PDF. It says: "Finding a Nash equilibrium in zero-sum games with three or more players is at least as hard (because a dummy player can be added to the two-player game to make it a three-player zero-sum game)." Also: "even if a Nash equilibrium could be computed efficiently in a game with more than two players, it is not clear that playing such an equilibrium strategy would be wise", and "The shortcomings of Nash equilibria outside of two-player zero-sum games … have raised the question of what the right goal should even be in such games."
  - Daskalakis, Goldberg & Papadimitriou, "The Complexity of Computing a Nash Equilibrium," *SIAM J. Comput.* 39(1):195–259, 2009, DOI 10.1137/070699652 (Crossref, with the abstract: "finding a Nash equilibrium in three-player games is indeed PPAD-complete").
  - Bernheim, Peleg & Whinston, "Coalition-Proof Nash Equilibria I. Concepts," *J. Econ. Theory* 42(1):1–12, 1987, DOI 10.1016/0022-0531(87)90099-8 (Crossref metadata only) supports "Nash covers only unilateral deviations".
  - "Strategically empty" is too strong: an equilibrium exists and constrains play. What fails is the guarantee.
- **Proposal:**
  - l. 27: "Равновесие на Наш в игра всеки срещу всеки с четирима играчи е едновременно **неразрешим** от гледна точка на изчислителна мощност и **стратегически безсъдържателен** - то не дава никаква информация за коалициите, които всъщност определят изхода от играта." → "Равновесието на Наш в игра всеки срещу всеки с четирима играчи е едновременно **изчислително непосилно** и **лишено от гаранции**: намирането му е поне толкова трудно, колкото при общите игри с двама играчи, а ако всеки играч избере равновесие независимо от другите, получената комбинация може изобщо да не е равновесие[^brown2019mp]. Освен това равновесието на Наш защитава само от едностранни отклонения, а не от съвместните отклонения на коалициите, които всъщност определят изхода от играта[^bernheim1987]."
  - l. 143: "Стойността на Наш е неразрешима и стратегически празна при 4-играчна игра всеки срещу всеки; оценката става емпирична (процент на победи + коалиционен резултат + EGTA Cyclic Ratio), закотвена в единствената точно решима под-игра (2-играчният минимакс игра в крайна фаза, $0$ несъответствия)." → "В игра всеки срещу всеки с четирима играчи равновесието на Наш е изчислително непосилно и не дава гаранции; оценката става емпирична (дял на победите, коалиционен резултат и циклично съотношение от EGTA), закотвена в единствената точно решима подигра (минимаксното решение на крайната фаза с двама играчи, $0$ несъответствия)."
  - EN l. 46–48: "Nash equilibrium in a 4-player free-for-all is both **intractable** to compute and **strategically empty** — it says nothing about the coalitions that actually decide the game." → "Nash equilibrium in a 4-player free-for-all is both **intractable** to compute and **without guarantees**: finding one is at least as hard as in general two-player games, and equilibria chosen independently need not form an equilibrium [brown2019mp]; it also guards only against unilateral deviations, not against the coalitions that actually decide the game [bernheim1987]." Takeaway l. 246–247: "Nash is intractable and strategically empty in 4-player FFA" → "Nash is intractable and offers no guarantee in 4-player FFA".
  - Footnotes: `[^brown2019mp]: Brown, N. & Sandholm, T. (2019). "Superhuman AI for multiplayer poker." *Science* 365(6456), 885–890. DOI 10.1126/science.aay2400; за сложността: Daskalakis, C., Goldberg, P. W. & Papadimitriou, C. H. (2009). "The Complexity of Computing a Nash Equilibrium." *SIAM J. Comput.* 39(1), 195–259. DOI 10.1137/070699652.` and `[^bernheim1987]: Bernheim, B. D., Peleg, B. & Whinston, M. D. (1987). "Coalition-Proof Nash Equilibria I. Concepts." *Journal of Economic Theory* 42(1), 1–12. DOI 10.1016/0022-0531(87)90099-8.`

### F11-S03 · S2 · SOURCE_GAPS row 3: De Carufel & Jerade → full reference; say what it anchors and what it does not
- **Where:** summaryBg l. 33–34 (Read more, which is also English) and l. 135; EN l. 62–63, 230; one-pager EN "implemented from the De Carufel & Jerade formalization" (BG in B18).
- **Verification:** J.-L. De Carufel, M. R. Jerade, "So Long Sucker: Endgame Analysis," arXiv:2403.17302 (v1 26 Mar 2024, v2 10 Oct 2025, 51 pp.), checked on the arXiv abstract and HTML v2. It characterizes Blue's winning scenarios when two players remain, each holding only their own colour. The chapter's "exact anchor" is the engine's own minimax on its own rules; `targetedReading/summary.md` says the theorems were not checked, and the engine omits rules (C03). So the paper does not supply the anchor, and "implemented from the formalization" overstates the link.
- **Proposal:**
  - "> **Прочетете повече:** Nash, Shapley, Shubik & Hausner (1950s), *So Long Sucker* (the game itself); and De\n> Carufel, J. & Jerade, M. - the 2-player SLS анализ на крайна игра, който дава единствената точна опора." → "> **Прочетете повече:** Hausner, Nash, Shapley & Shubik (1964) - правилата на играта[^hausner1964]; De Carufel & Jerade (2024) - пълна характеристика на крайната фаза с двама играчи[^decarufel2024]. Точната опорна точка в тази глава е собственото минимаксно решение на двигателя; то още не е сверено с тази характеристика."
  - l. 135: "а не спрямо транскрипция на De Carufel & Jerade" → "а не спрямо формализацията на De Carufel & Jerade[^decarufel2024]"
  - Footnote: `[^decarufel2024]: De Carufel, J.-L. & Jerade, M. R. (2024). "So Long Sucker: Endgame Analysis." *arXiv:2403.17302*.`
  - EN Read more analogously. One-pager EN "implemented from the De Carufel & Jerade formalization" → "implemented from the published rules, with the De Carufel & Jerade endgame analysis as the (not yet cross-checked) reference".

### F11-S04 · S2 · The only prior RL work on SLS is not cited; "the first coalition-aware RL treatment"
- **Where:** summaryEn l. 19–20 and summaryBg l. 19 (proposal in S01); `planning/cleanSteps/step_11…` cites the paper, the chapter does not.
- **Verification:** M. Sharan, C. Adak, "Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'," arXiv:2411.11057 (v1 17 Nov 2024, v2 14 Oct 2025), checked on the arXiv abstract. It offers a framework with a GUI; DQN/DDQN/Dueling DQN agents reach "roughly half of the maximum attainable reward"; "coalition-aware strategies" are named as future work. A web search (Sept 2026) found no RL work on SLS with coalition mechanisms. The only other hit is a non-academic LLM deception site. "First" is plausible as a statement about SLS, but the credit does not use coalition information (C02), so the chapter does not earn "coalition-aware".
- **Proposal:** Replace "the first coalition-aware RL treatment" with the S01 wording ("extends the only published RL treatment … whose agents are coalition-blind"). Footnote: `[^sharan2024]: Sharan, M. & Adak, C. (2024). "Reinforcing Competitive Multi-Agents for Playing 'So Long Sucker'." *arXiv:2411.11057*.`

### F11-S05 · S2 · piKL is attributed to Bakhtin et al. (2022) and called "the N-player safe-play recipe"
- **Where:** footnote `chapter2022` (EN l. 270, BG l. 155, English in both); `targetedReading/summary.md` Paper 3.
- **Verification:** `lit_gaps.md` (C2, Correction 2, verified there): piKL originates in Jacob et al., ICML 2022 (arXiv:2112.07544). Bakhtin et al., ICLR 2023 (arXiv:2210.05492) is DiL-piKL for no-press Diplomacy. The anchor is a human-imitation policy, and neither paper gives a safety or loss bound.
- **Proposal:** "[^chapter2022]: the Step 09 MARL stack (this repo) for MAPPO with a centralized critic; and Bakhtin и др. (2022) on **piKL** - regularizing toward a behavioral prior instead of Nash, the n-играчен безопасен начин на игра recipe this step points at." → "[^chapter2022]: Реализацията на MAPPO с централизиран критик е от Глава 9. piKL (регуларизация на търсенето към стратегия, наподобяваща човешката игра) е въведен от Jacob, A. P. и др. (2022). "Modeling Strong and Human-Like Gameplay with KL-Regularized Search." *ICML*, arXiv:2112.07544, и е приложен в Diplomacy от Bakhtin, A. и др. (2023). "Mastering the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning." *ICLR*, arXiv:2210.05492. Опорната стратегия там е имитация на човешка игра и не дава гаранция за безопасност; използването ѝ като опора за безопасна експлоатация при N играчи е предложение на дисертацията." EN parallel. Also correct `targetedReading/summary.md` Paper 3 (title and year).

### F11-S06 · S2 · Spinning-top attributed to Balduzzi et al. (2019) only (lit_evaluation correction)
- **Where:** footnote `balduzzi2019` (EN l. 272, BG l. 157); curated `terminology_EN_BG.md` row "Spinning top decomposition … (Balduzzi et al., 2019)".
- **Verification:** `lit_evaluation.md` (verified there): Balduzzi et al. 2019 (ICML, PMLR 97:434–443) gives the transitive/cyclic decomposition. The spinning-top geometry is Czarnecki et al., "Real World Games Look Like Spinning Tops," NeurIPS 2020, arXiv:2004.09468.
- **Proposal:** "*ICML* - геометрията на пумпала на транзитивната спрямо цикличната структура. Свързани: Jaderberg, M. et al. (2017). "Population Based Training of Neural Networks." *arXiv:1711.09846*." → "*ICML* - разлагане на транзитивна и циклична компонента; Czarnecki, W. M. и др. (2020). "Real World Games Look Like Spinning Tops." *NeurIPS*, arXiv:2004.09468 - геометрията „пумпал“." Drop the PBT reference: this chapter does no population-based training. EN parallel. In the curated glossary note: "(Balduzzi et al., 2019; Czarnecki et al., 2020)".

### F11-S07 · S3 · `shapley1953` footnote metadata
- **Where:** summaryBg l. 153 and EN l. 268
- **Verification:** Crossref:
  - Shapley, "A Value for n-Person Games," *Contributions to the Theory of Games II* (Ann. Math. Stud. 28), Princeton UP, 1953, pp. 307–318, DOI 10.1515/9781400881970-018.
  - Wang, Zhang, Kim & Gu, "Shapley Q-Value: A Local Reward Approach to Solve Global Reward Games," *AAAI* 34(05):7285–7292, 2020, DOI 10.1609/aaai.v34i05.6220.
  - Chalkiadakis, Elkind & Wooldridge, *Computational Aspects of Cooperative Game Theory*, Synthesis Lectures on AI and ML (DOI resolves to the Springer record 10.1007/978-3-031-01558-8, listed as 2012; the Morgan & Claypool original is 2011).
- **Proposal:** "*Contributions to the Theory of Games*; Chalkiadakis, Elkind & Wooldridge (2011), *Computational Aspects of Cooperative Game Theory* (core, shapley, nucleolus); и Wang и др. относно разпределянето на заслугата, базирано на Shapley в MARL." → "В *Contributions to the Theory of Games II* (Annals of Mathematics Studies 28), 307–318. Princeton University Press; Chalkiadakis, G., Elkind, E. & Wooldridge, M. (2011). *Computational Aspects of Cooperative Game Theory*. Morgan & Claypool (ядро, стойност на Шапли, нуклеолус); Wang, J., Zhang, Y., Kim, T.-K. & Gu, Y. (2020). "Shapley Q-Value: A Local Reward Approach to Solve Global Reward Games." *AAAI* 34(5), 7285–7292 (разпределяне на приноса в MARL чрез стойността на Шапли)." EN parallel.

## X — Structure

### F11-X01 · S2 · Candidate's TOC comment only partly applied: "Формиране и засичане на коалиции"
- **Where:** user_comments_2026-08-01.json, chapter 0, p. 8, on the TOC line "11 Стъпка 11 - Динамично формиране на коалиции в състезателни игри всеки срещу всеки": comment "Формиране и засичане на коалиции". Now: summaryBg l. 17 "# Глава 11 - Динамично формиране и засичане на коалиции в състезателни игри всеки срещу всеки" (and the YAML title). The one-pager titles lack "засичане" entirely: onePagerBg "# Глава 11 Резюме - Динамично формиране на коалиции в състезателни игри всеки срещу всеки"; EN one-pager "Dynamic Coalition Formation in Competitive FFA Games".
- **Problem:** "засичане" was inserted, but the heading was not shortened to the requested form. It still breaks over two lines on p. 205.
- **Now → Proposed:**
  - "# Глава 11 - Динамично формиране и засичане на коалиции в състезателни игри всеки срещу всеки" → "# Глава 11 - Формиране и засичане на коалиции"
  - YAML `title:` "Глава 11 Обобщение - Динамично формиране и засичане на коалиции в състезателни игри всеки срещу всеки (So Long Sucker)" → "Глава 11 Обобщение - Формиране и засичане на коалиции (So Long Sucker)"
  - onePagerBg "# Глава 11 Резюме - Динамично формиране на коалиции в състезателни игри всеки срещу всеки" → "# Глава 11 Резюме - Формиране и засичане на коалиции" (and its `title:`)
  - EN headings: "Chapter 11 — Coalition Formation and Detection" (summary and one-pager)
- The candidate's own choice "засичане" is acceptable Bulgarian in technical use, so I kept it. The glossary has "откриване" for *detection*; the body text uses "детектор", which is consistent with either.

### F11-X02 · S3 · Cross-references by section name that do not match the BG headings
- **Where:** summaryBg l. 84 "от раздела *коалиционен кредит*"; l. 123 "(разделът *Shapley credit*)"; EN "the *Shapley credit* section" (l. 138, 200).
- **Problem:** No BG heading is called "коалиционен кредит" or "Shapley credit" (it is "Стойност на Шейпли в състезателна игра", which is B08 in any case).
- **Fix:** Use numbered references: "(раздел 11.3)"; EN "(Section 11.3)". Already applied in the B14, B15 and C01 proposals.
