# Step 05 — final review

**Summary:** Chapter 5 is a clear survey, but four problems stand out. (1) **Structure.** 13 headings of sections that were never written (the rest of Part 4, all of Part 5, Synthesis) print as a bare list on p. 78 and appear in the table of contents. The candidate's TOC comment asked for the "Част N -" prefixes to go; it was not applied, and all five prefixes remain in both languages. Forward references still point to the unwritten parts and to "Глава 15". (2) **Meaning errors in the Bulgarian** that a technical reader will notice: equivariant is rendered "инвариантна"; also "еквивариантност спрямо превод", "неупотребена колекция", "решаващите игри", "разкаяние" for regret, "усреднено време" for time-average and "двуигрови"; and "мрежа" is used for both the neural network and the grid. Two of these come from settled glossary entries (T01, T02). (3) **Own results.** The chapter misreports its own measurements: the advantage losses *rose* (about 20 → 1 600), they did not fall, and the random-strategy level is 2.37, not 1.69. The Single Deep CFR, DREAM and NFSP descriptions contain factual slips, and Fig. 21 is cited to the wrong paper. (4) **Currency and figures.** The survey stops in 2020: it has no ESCHER, R-NaD/DeepNash or MMD, and not the ICLR 2026 result that generic policy-gradient methods match the specialised ones. All seven figures print at 3–7 pt.
**Counts:** S1 24 · S2 39 · S3 11   (by category: G 9 · B 27 · T 10 · C 13 · S 11 · X 4)

Conventions in this file:
- Quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md` (including `**`, `*`, `$`), so read this file as source.
- "EN" quotes come from `summaryEn.md` / `onePager.md`.
- Page numbers are PDF pages of `allSummaries_bg.pdf`. The printed folio is one lower: PDF p. 66 prints "65".
- Printed type size = matplotlib size × (printed width ÷ saved width). Body text is 10.9 pt and the legibility floor is ≈ 8.2 pt.
- Proposals keep the chapter's current " - " dashes and decimal points; those are fixed centrally.
- Decided centrally, so not itemised:
  - hyphen used as a dash: 119× in the summary, 15× in the one-pager;
  - decimal points: ≈ 10 in the summary text, 20 in the one-pager, plus "50,000" 2× in the one-pager;
  - "x" for ×: 4×;
  - pipeline bold: 87 spans in `summaryBg.md` against 11 in the EN; 32 against 22 in the one-pager;
  - shared footnote labels: none of this chapter's six labels is defined in another chapter, so nothing is affected.

## G — Figures

### F05-G01 · S1 · Bulgarian captions for all seven figures
- **Where:** summaryBg.md, the image alt text of figs. 17–23 (pp. 66–75). All seven captions print in English, a known corpus-wide defect. In three of them the pipeline replaced only "Leduc" with "Ледюк".
- **Now → Proposed:**
  - "![Connectivity of the four layer families: a fully connected MLP, a convolution that reuses one filter across local windows, a recurrent cell reused across time, and self-attention.]" → "![Свързаност на четирите семейства слоеве: напълно свързан слой (MLP), конволюция, която прилага един и същ филтър към локални прозорци, рекурентна клетка, използвана многократно във времето, и самовнимание.]"
  - "![The general encoder / trunk / heads pattern (top); two instances below - DRQN and AlphaStar.]" → "![Общата схема с кодировчици, общ ствол и изходни глави (горе) и два нейни примера (долу): DRQN и AlphaStar.]"
  - "![Deep CFR exploitability on Ледюк across network sizes (32x32, 64x64, 128x128x128).]" → "![Експлоатируемост на Deep CFR в Ледюк при три размера на мрежата (32×32, 64×64 и 128×128×128).]"
  - "![Common network shapes: a uniform stack, a tapering funnel, an hourglass with a central bottleneck (orange), and a uniform stack with a single narrow collar (orange). Bar height represents layer width.]" → "![Типични форми на мрежата: равномерна поредица от слоеве, стесняваща се фуния, пясъчен часовник с централно стеснение (в оранжево) и равномерна поредица с една тясна „яка“ (в оранжево). Височината на всеки правоъгълник показва ширината на слоя.]"
  - "![Single Deep CFR (SD-CFR) matches or slightly beats Deep CFR while training only one network (left); the right panel shows how reservoir-buffer capacity affects convergence. From the Single Deep CFR paper - not an experiment from this work.]" → with the crop proposed in F05-G06: "![Single Deep CFR (SD-CFR) достига същата или малко по-ниска експлоатируемост от Deep CFR в Ледюк, без да обучава мрежа за средната стратегия. Фигурата е от статията на Steinberger (2019) и не представя експеримент от настоящата работа.]". If the right panel is kept, append: "Вдясно: ефектът от ограничаването на броя съхранени мрежи за предимства (буфера $B^M$)."
  - "![Deep CFR vs. tabular MCCFR exploitability on Ледюк.]" → "![Експлоатируемост на Deep CFR и на табличния MCCFR в Ледюк при сравнимо време за изпълнение.]" This wording fits the single-panel figure proposed in F05-G07.
  - "![NFSP exploitability on Ледюк over training episodes.]" → "![Експлоатируемост на NFSP в Ледюк в хода на 50 000 епизода обучение: кривата остава около нивото на равномерно случайната стратегия (≈ 2.37).]"
- **Why the fig. 21 caption changes meaning:** $B^M$ in the source paper is the buffer of *stored value networks*, not the reservoir of training samples (Steinberger 2019, §5.4 and Fig. 1b). "Reservoir-buffer capacity" therefore misdescribes the right panel.
- **Fix:** replace the alt text in `summaryBg.md`. For figs. 19, 22 and 23 also change the file links (F05-G04, G07, G08).

### F05-G02 · S1 · Fig. 17 layer families: prints at 3.7–4.5 pt, "Сгъвка", colour legend contradicted by two panels
- **Where:** `renders/ch05/p066_f1.png`, p. 66. Caption: "Connectivity of the four layer families…"
- **Problem:**
  1. **Size.** The figure is saved at 1377 px @ 130 dpi (10.59 in) and printed at 11.6 cm (4.57 in), a scale of 0.431. Panel titles at fs 10.5 print at 4.5 pt. The notes "един и същи цвят = …" and "t=1…t=4" at fs 8.5 print at 3.7 pt.
  2. **Terminology.** The CNN panel title reads "Сгъвка (CNN)", which comes from the glossary (F05-T04); the text says "конволюция".
  3. **Wording.** The BG titles are long ("всеки елемент обръща внимание на всички останали") and will not fit once the figure is printed larger.
  4. **Text contradicts the figure.** The text says "цветът на ръбовете обозначава отделно тегло, така че повтарящият се цвят маркира споделено тегло" for the whole figure. But all MLP edges are one grey, although each has its own weight. All attention arrows are one colour, although attention weights differ per pair. The note "same colour = same (shared) weight" sits only under the CNN panel.
  5. **Layout.** With `fig-pos="H"` the tall figure leaves about half of p. 65 blank (see F05-X04).
- **Fix:**
  - `make_arch_figure.py`: `figsize=(11, 8.2)` → `(6.9, 5.2)`; both notes and the `t=` labels `fontsize=8.5` → `10`; titles stay 10.5; `dpi=130` → `300`.
  - Both summaries: `(arch_comparison_bg.png){width=66% fig-pos="H"}` → `{width=100% fig-pos="H"}`, and the same for `arch_comparison.png` in the EN. The scale becomes ≈ 1.0, so titles print at 10.5 pt and notes at 10 pt.
  - Mapping:
    - 'Fully connected (MLP)\nevery unit connects to every unit' → 'Напълно свързан слой (MLP)\nвсеки възел с всеки възел'
    - 'Convolution (CNN)\none shared filter slid over local windows' → 'Конволюция (CNN)\nобщ филтър върху локални прозорци'
    - 'Recurrent (RNN)\nsame cell over time, hidden state = memory' → 'Рекурентен слой (RNN)\nобща клетка; скритото състояние е памет'
    - 'Self-attention (Transformer)\nevery element attends to all others' → 'Самовнимание (трансформър)\nвсеки елемент към всички останали'
    - 'same colour = same (shared) weight' → 'еднакъв цвят = споделено тегло'
    - 'one (orange) query token attends to all' → 'оранжевата заявка се свързва с всички елементи'
  - Text (§ "Типове слоеве на практика…"): "На фигурата по-долу цветът на ръбовете обозначава отделно тегло, така че повтарящият се цвят маркира споделено тегло; следващите параграфи описват всеки панел." → "В панела на конволюцията цветът на връзката обозначава теглото: еднаквият цвят означава споделено тегло, а в останалите панели цветът само различава видовете връзки. Следващите параграфи описват всеки панел."
  - EN: "In the figure below, edge colour denotes a distinct weight, so a repeated colour marks a shared weight; the paragraphs that follow read off each panel." → "In the convolution panel, edge colour denotes the weight, so a repeated colour marks a shared weight; in the other panels colour only distinguishes kinds of connection. The paragraphs that follow read off each panel."

### F05-G03 · S1 · Fig. 18 encoder/trunk/heads: prints at 3.2–3.9 pt, English in boxes, one component with two names
- **Where:** `renders/ch05/p068_f1.png`, p. 68. Caption: "The general encoder / trunk / heads pattern…"
- **Problem:**
  1. **Size.** Saved at 1482 px @ 130 dpi (11.4 in), printed at 10.2 cm (4.02 in), a scale of 0.352. Box text at fs 9 prints at 3.2 pt; section titles at fs 11 print at 3.9 pt. This is the least legible figure in the chapter.
  2. **English left in the BG figure:** "RNN / attn.", "Сливане (concat)", "Concat", "Transformer" (in the AlphaStar title), "(autoregr.)", and ASCII "->" arrows.
  3. **Inconsistent terms:**
     - Titles say "MLP" while boxes say "многослоен перцептрон". The settled glossary expands MLP, although rule 2 keeps abbreviations in Latin script.
     - The AlphaStar core is "LSTM ствол" in the title but "LSTM ядро" in the box.
     - Heads are "изходни слоеве" in the titles but "глава на стратегията / стойностна глава" in the boxes.
     - "Карти / сет" uses the anglicism "сет".
  4. **Overflow (central fix).** At the proposed print size (box width 2.3 units ≈ 82 pt) these boxes overflow: "Пространствена дъска", "История на действията", "Скаларни величини" (2×), "многослоен перцептрон" (3×), "Единици (множество)", "Споделен ствол (MLP / LSTM)", "изходни слоеве за действие (autoregr.)".
- **Fix:**
  - `make_hybrid_figure.py`: `figsize=(11.5, 9.2)` → `(6.9, 5.6)`; every `fs=9` (and the default `fs=9.5`) → `9.6`; `title()` fontsize 11 → 10.5; in the three title strings "->" → "→"; `dpi=130` → `300`.
  - Both summaries: `(arch_hybrid_bg.png){width=58% fig-pos="H"}` → `{width=100% fig-pos="H"}`, and the same in the EN. The scale becomes ≈ 1.0: boxes print at 9.6 pt and titles at 10.5 pt.
  - Mapping, shorter where possible:
    - 'Spatial board' → 'Дъска (решетка)'
    - 'Action history' → 'История на ходовете'
    - 'Cards / set' → 'Карти (множество)'
    - 'Scalars' → 'Скалари'
    - 'MLP': delete the glossary-sourced entry so it stays "MLP"
    - 'RNN / attn.' → 'RNN / внимание'
    - 'Fuse\n(concat)' → 'Сливане\n(конкатенация)'
    - 'Concat' → 'Конкатенация'
    - 'Shared trunk\n(MLP / LSTM)' → 'Общ ствол\n(MLP / LSTM)'
    - 'Policy head' → 'Глава на\nстратегията'
    - 'Value head' → 'Глава за\nстойността'
    - 'Units (set)' → 'Единици\n(множество)'
    - 'Minimap' → 'Миникарта'
    - 'Transformer' → 'Трансформър'
    - 'Action heads\n(autoregr.)' → 'Глави за действия\n(авторегресивни)'
  - Titles. The keys change with the "→" edit:
    - 'General pattern: encoders (one per input) → fuse → shared trunk → heads' → 'Обща схема: кодировчици (по един за вход) → сливане → общ ствол → изходни глави'
    - 'Example 1 — DRQN: CNN → LSTM → MLP (memory for partial observability)' → 'Пример 1 — DRQN: CNN → LSTM → MLP (памет при частична наблюдаемост)'
    - 'Example 2 — AlphaStar: Transformer + CNN + MLP → LSTM core → action heads' → 'Пример 2 — AlphaStar: трансформър + CNN + MLP → LSTM ядро → глави за действия'

### F05-G04 · S1 · Fig. 19 network-size sweep: entirely English, 6.1 pt, meaningless log ticks
- **Where:** `renders/ch05/p070_f1.png`, p. 70. `summaryBg.md` links the EN file `day01_network_sizes.png`.
- **Problem:**
  1. **English everywhere:** title, axis labels, a legend that repeats the layer sizes ("(64,64) baseline  layers=(64, 64)"), and decimal points.
  2. **Why the BG render is missing.** `implementation/step05/exploration/day01_deep_cfr.py` is listed in `plotting_scripts()`, but running it retrains every model (5–15 min), so no `_bg` twin exists.
  3. **Size.** 910 px @ 130 dpi (7.0 in) printed at 10.9 cm (4.29 in), a scale of 0.613. Ticks, axis labels and legend at fs 10 print at 6.1 pt; the title prints at 7.4 pt.
  4. **Log axis.** A log y-axis over 1.14–1.70 prints ticks as "1.7 × 10⁰" … "1.2 × 10⁰".
  5. **Data.** The 64×64 curve is flat at 1.70, the value the chapter reports for the *unpatched* solver (F05-C04; extract "To verify").
- **Fix:**
  - Add `implementation/step05/exploration/plot_from_logs.py`. It loads `logs/day01_results.json` and `logs/day02_results.json` and calls the three plot functions, writing to `deliverables/reports/step05/summary/`. List it in `plotting_scripts()` in place of `day01_deep_cfr.py`.
  - In `plot_network_size_sweep`:
    - `figsize=(7, 4.5)` → `(4.3, 2.9)`
    - drop `set_yscale("log")` and `set_title`
    - label → `"×".join(map(str, r.layers))`
    - `plt.rcParams["font.size"] = 10`
    - `dpi=130` → `300`
    
    At 62 % width the scale is ≈ 1.0, so text prints at 10 pt.
  - Mapping: 'Exploitability' → 'Експлоатируемост'; 'Deep CFR outer iterations' → 'Външни итерации на Deep CFR' (existing entry).
  - `summaryBg.md`: "(day01_network_sizes.png)" → "(day01_network_sizes_bg.png)".

### F05-G05 · S1 · Fig. 20 network shapes: prints at 4.8 pt, "(bottleneck)" left in English
- **Where:** `renders/ch05/p071_f1.png`, p. 71. Caption: "Common network shapes…"
- **Problem:**
  1. **Size.** 1612 px @ 130 dpi (12.4 in) printed at 14.4 cm (5.67 in), a scale of 0.457. Titles at fs 10.5 print at 4.8 pt.
  2. **Labels.** "пясъчен часовник (bottleneck)" keeps an English word and is lower case, as is "яка", while "Равномерно" and "Фуния" are capitalised. "Равномерно" is neuter, although the implied noun "форма" is feminine.
- **Fix:**
  - `make_shapes_figure.py`: `figsize=(12.5, 3.0)` → `(6.9, 1.9)`; `dpi=130` → `300`.
  - Both summaries: `{width=82% fig-pos="H"}` → `{width=100% fig-pos="H"}`. Titles then print at 10.5 pt.
  - Mapping:
    - 'Uniform' → 'Равномерна'
    - 'Funnel (tapering)' → 'Фуния'
    - 'Hourglass (bottleneck)' → 'Пясъчен часовник\n(стеснение)'
    - 'Collar' → 'Яка'

### F05-G06 · S1 · Fig. 21 (reproduced from Steinberger 2019): soft, ≈ 5 pt legend, panel (b) misdescribed, not cited
- **Where:** `renders/ch05/p074_f1.png`, p. 74. File: `deliverables/reports/step05/deepcfr.png`.
- **Problem:**
  1. **Resolution and size.** The figure is a raster screenshot: 967 px printed at 15.5 cm, i.e. 159 ppi, which looks soft. The panel (b) legend prints at about 5 pt.
  2. **Panel (b).** It shows reservoir sampling over SD-CFR's *buffer of stored networks* $B^M$. The caption calls it "reservoir-buffer capacity", and the text never discusses it.
  3. **Wrong game in the text.** Panel (a) is **Leduc** ("Figure 1: Empirical analysis of SD-CFR in Leduc Hold'em Poker"). The text presents it as "големи покер игри" (see F05-C05).
  4. **Wrong citation.** The source paper is not cited anywhere; the nearby footnote is DREAM (F05-S07).
- **Fix:**
  - Keep panel (a) only, the one the text uses. Re-extract it at ≥ 300 ppi from the arXiv source of 1901.07621: the plots are vector (pgfplots), so a PDF-to-PNG render at 300 dpi works.
  - `(../deepcfr.png){width=88% fig-pos="H"}` → `{width=55% fig-pos="H"}`.
  - Use the caption in F05-G01 and add `[^sdcfr]`.
  - Before Chapter I reuses the figure, check the arXiv licence of 1901.07621 (see the extract, "To verify").

### F05-G07 · S1 · Fig. 22 Deep CFR vs MCCFR: prints at 3.9 pt, entirely English, mixed-unit left panel
- **Where:** `renders/ch05/p074_f2.png`, p. 74. `summaryBg.md` links the EN file `day01_deep_cfr_vs_mccfr.png`.
- **Problem:**
  1. **Size.** 1430 px @ 130 dpi (11.0 in) printed at 10.9 cm (4.29 in), a scale of 0.390. Legend, ticks and labels at fs 10 print at 3.9 pt; titles at fs 12 print at 4.7 pt. It is illegible.
  2. **English:** suptitle, both titles, legends, axis labels.
  3. **Left panel.** It plots "iterations" of two different kinds on one axis (its own title admits "unit differs per method"). The text uses only the wall-clock comparison.
- **Fix:**
  - In `plot_deep_cfr_vs_mccfr`, called from `plot_from_logs.py` (F05-G04):
    - keep only the wall-clock panel: `fig, ax = plt.subplots(figsize=(4.3, 2.9))`
    - drop the suptitle and title
    - font size 10; `dpi=300`
    - Deep CFR label `f"Deep CFR ({'×'.join(map(str, deep_run.layers))})"`
    - optionally add the 32×32 and 128×128×128 end points
  - Mapping:
    - 'Wall-clock seconds' → 'Време за изпълнение (s)'
    - 'Tabular MCCFR' → 'Табличен MCCFR'
    - new 'Deep CFR (64×64)' → 'Deep CFR (64×64)'
    - 'Exploitability (log)' → 'Експлоатируемост'
  - `summaryBg.md`: "(day01_deep_cfr_vs_mccfr.png)" → "(day01_deep_cfr_vs_mccfr_bg.png)".

### F05-G08 · S1 · Fig. 23 NFSP: entirely English, 6.1 pt, code name in title, no reference line
- **Where:** `renders/ch05/p075_f1.png`, p. 75. `summaryBg.md` links the EN file `day02_nfsp_leduc.png`.
- **Problem:**
  1. **English:** the title "NFSP on leduc_poker" (a code identifier), the legend "NFSP (avg policy)" and the axis labels. `day02_nfsp.py` is not in `plotting_scripts()`, and 'Episodes' and 'NFSP (avg policy)' have no mapping entries.
  2. **Size.** Scale 0.613: text prints at 6.1 pt and the title at 7.4 pt. The log y-axis over 2.3–3.2 again gives "3.2 × 10⁰" ticks.
  3. **Missing reference.** The curve starts at 2.35 and ends at 2.46 (`logs/day02_results.json`), i.e. at the uniform-random level of 2.37 (F05-C02). Without a reference line the reader cannot see that nothing was learned.
- **Fix:**
  - `plot_nfsp` (via `plot_from_logs.py`):
    - `figsize=(7, 4.5)` → `(4.3, 2.9)`
    - drop `set_yscale("log")`, `set_title` and the one-series legend
    - add `ax.axhline(2.374, ls="--", color="grey", label="Uniform random policy")` with `ax.legend(fontsize=10)`
    - font size 10; `dpi=300`
  - Mapping:
    - 'Episodes' → 'Епизоди'
    - 'Exploitability' → 'Експлоатируемост'
    - 'Uniform random policy' → 'Равномерно случайна стратегия'
  - `summaryBg.md`: "(day02_nfsp_leduc.png)" → "(day02_nfsp_leduc_bg.png)".

### F05-G09 · S3 · The BG renders predate the label mapping
- **Where:** `deliverables/reports/step05/summary/arch_*_bg.png` were written on 1 Aug at 13:08; `scripts/figures/out/figure_labels.json` changed on 1 Aug at 19:50.
- **Fix:** after the mapping changes in G02–G05, run `python scripts/figures/render_bg_figures.py --only step05` (and the new `plot_from_logs.py`), then rebuild. In the central overflow fix, wrap the text or widen the box, never shrink below fs 9.6 (same rule as F07-G09).

## B — Bulgarian language

### F05-B01 · S1 · meaning — "permutation-equivariant" rendered as "invariant"
- **Where:** summaryBg.md § "Типове слоеве на практика…" — "тя е **инвариантна спрямо разместване**, а редът трябва да бъде предоставен изрично"
- **EN:** "Because the operation ignores element order, it is permutation-equivariant, and order must be supplied explicitly through positional encodings when it matters."
- **Now → Proposed:** "тя е **инвариантна спрямо разместване**, а редът трябва да бъде предоставен изрично" → "тя е еквивариантна спрямо пермутации (пренареждането на входа пренарежда изхода по същия начин), а редът трябва да бъде подаден изрично"
- **Why:** An invariant output does not change; an equivariant output is permuted in the same way as the input. Two paragraphs later the chapter contrasts exactly these two properties (Deep Sets = invariance), so the error erases the point. The wrong form comes from the settled glossary (F05-T01).

### F05-B02 · S1 · meaning / non-words — the convolution vocabulary
- **Where:** summaryBg.md §§ "Типове слоеве на практика…", "Кодиране на състоянието на играта и историята"
- **EN:** "A **convolutional layer** (CNN) connects each output unit…"; "(translation equivariance)"; "Stacking convolutions enlarges the effective receptive field"; "so that a convolution can read it directly"
- **Now → Proposed:**
  - "Свръзъчен слой (CNN) свързва всяка изходна единица" → "Конволюционният слой (CNN) свързва всяка изходна единица"
  - "(еквивариантност спрямо превод)" → "(еквивариантност спрямо транслация)"
  - "Подреждането на свръзки увеличава ефективното приемно поле" → "Наслагването на няколко конволюционни слоя увеличава ефективното приемно поле"
  - "така че сгъвката да може да го прочете директно" → "така че конволюцията да може да го обработи пряко"
- **Why:**
  - "свръзъчен" and "свръзки" are not Bulgarian words.
  - "превод" means translation of a text. The curated glossary warns about exactly this collision under *Action translation*, and § 5.2.1 itself says "еквивариантност спрямо транслация".
  - One operation now has three names in the chapter (конволюция / свръзка / сгъвка). "сгъвка" comes from the settled glossary (F05-T04).
  - The fourth occurrence, "предположенията на сгъвката", is rewritten in F05-B04.

### F05-B03 · S1 · meaning — "unordered" rendered as "unused" and "unsettled"
- **Where:** summaryBg.md §§ "Индуктивно пристрастие…", "Типове слоеве на практика…"
- **EN:** "When part of the state is an unordered collection — a hand of cards, or the set of other players —"; "A genuinely unordered input"
- **Now → Proposed:**
  - "е неупотребена колекция - ръка карти или множеството от други играчи" → "е неподредена съвкупност - картите в ръката или множеството от останалите играчи"
  - "Вход, който е наистина неуреден" → "Вход, който е наистина неподреден"
- **Why:** "неупотребена" means *unused*; "неуреден" means *unsettled/unregulated*. The whole paragraph is about order not mattering.

### F05-B04 · S1 · meaning — *grid* rendered as "мрежа" (network)
- **Where:** summaryBg.md §§ 5.2.1, 5.2.2, 5.2.3, 5.3.4, 5.4.4 (9 places)
- **EN:** "a board or a grid"; "why convolutions dominate grid domains"; "the standard choice for boards and grids"; "a fog-of-war grid agent"; "a stack of grids"; "a grid-based, Bomberman-style game"; "a grid is presented as a grid precisely so that a convolution's assumptions hold"; "as in a gridworld"; "gridworlds, Pommerman, and the like"
- **Now → Proposed:**
  - "е пространствено - дъска или мрежа -" → "е пространствено - дъска или решетка -"
  - "обяснява защо конволюциите доминират в мрежовите области" → "обяснява защо конволюциите са стандартният избор за дъски и решетки" (the softening is F05-S02)
  - "Това е стандартният избор за дъски и мрежи." → "Това е стандартният избор за дъски и решетки."
  - "естественият шаблон за агент в мрежа с „мъгла на войната“" → "естественият шаблон за агент в решетъчна среда с „мъгла на войната“"
  - "Пространственото състояние се кодира като купчина от мрежи" → "Пространственото състояние се кодира като поредица от наслоени решетки"
  - "игра в стил Bomberman на базата на мрежа" → "игра в стил Bomberman върху решетка"
  - "мрежата се представя като мрежа именно за да важат предположенията на сгъвката" → "решетката се подава като решетка именно за да са в сила предположенията на конволюцията"
  - "както в една мрежова среда" → "както в една решетъчна среда"
  - "мрежи от клетки, Pommerman и подобни" → "решетъчни среди, Pommerman и подобни"
- **Why:** In this chapter "мрежа" is the neural network, in almost every paragraph. "мрежата се представя като мрежа" is unreadable, and "конволюциите доминират в мрежовите области" reads as "in network domains". Table 8 already says "решетки". The glossary has no entry for *grid* (F05-T07).

### F05-B05 · S1 · meaning — *solver* rendered as "решаващи игри" and "решаващи средства/двигатели"
- **Where:** summaryBg.md §§ 5.1.3, 5.2.5; onePagerBg.md "**Подход.**"
- **EN:** "the neural game solvers of Parts 3 and 4"; "Two more recur specifically in the game solvers ahead."; "OpenSpiel's reference solvers"
- **Now → Proposed:**
  - "Още две се появяват конкретно в решаващите игри по-нататък." → "Още две се срещат специално в невронните решавачи на игри по-нататък."
  - "невронните решаващи средства за игри" → "невронните решавачи на игри"
  - onePagerBg: "референтните решаващи двигатели на OpenSpiel" → "референтните решавачи на OpenSpiel"
- **Why:** "решаващите игри" means "the decisive games". The glossary term *solver* → "решавач" is used elsewhere in the same chapter ("невронен решавач", "решавач на игра").

### F05-B06 · S1 · meaning — *regret* rendered as "разкаяние" (repentance)
- **Where:** summaryBg.md § "Deep CFR и неговите варианти с една мрежа" — "стъпката на съвпадение по разкаяние"
- **EN:** "the traversal, the regret-matching step, the averaging"
- **Now → Proposed:** "стъпката на съвпадение по разкаяние" → "стъпката на напасване на съжалението"
- **Why:** "разкаяние" means repentance. The glossary term, used twice a few lines earlier, is "напасване на съжалението".

### F05-B07 · S1 · system names translated or spelled out
- **Where:** summaryBg.md §§ 5.4.1, 5.4.3 (heading, text) and Table 8
- **EN:** "search-plus-RL methods (ReBeL, Player of Games)"; "### Search + RL: ReBeL & Player of Games"; "Player of Games (Schmid et al., 2023) generalizes the recipe"
- **Now → Proposed:**
  - "### Търсене + RL: Recursive Belief-based Learning и играч на игри" → "### Търсене + RL: ReBeL и Student of Games"
  - "*търсене плюс обучение с подкрепление* методи (Recursive Belief-based Learning, играч на игри)" → "методи, съчетаващи *търсене и обучение с подкрепление* (ReBeL, Student of Games)"
  - "| Търсене + RL (Recursive Belief-based Learning, играч на игри) |" → "| Търсене + RL (ReBeL, Student of Games) |"
  - "Играч на игри (Schmid и др., 2023) обобщава този подход" → "Student of Games (Schmid и др., 2023; в предварителната версия - Player of Games) обобщава този подход"
- **Why:**
  - The curated glossary: named systems (it lists ReBeL and Student of Games) are never translated. "играч на игри" reads as "a player of games" in ordinary prose.
  - The published name of Schmid et al. (2023) is *Student of Games* (see F05-C10).
  - The second item also fixes the English-like word order "*…* методи".

### F05-B08 · S1 · names lower-cased by the pipeline; wrong pronoun
- **Where:** summaryBg.md §§ 5.1.1, 5.1.2, 5.2.4, 5.3.4, 5.4.1
- **Now → Proposed:**
  - "> **reLU** (rectified linear unit)" → "> **ReLU** (rectified linear unit)"
  - "Малка **мрежа** картографира този вектор към **стойност** за всяко **действие**; **обратното разпространение на грешката** с **adam** го настройва спрямо **целевите стойности**" → "Малка мрежа съпоставя на този вектор стойност за всяко действие; обратното разпространение на грешката с Adam я настройва спрямо целевите стойности"
  - "принципът, залегнал в основата на resNets" → "принципът, залегнал в основата на ResNet"
  - "neuRD" (2×: "(Deep CFR, DREAM, neuRD) от Част 3" and "- neuRD, например,") → "NeuRD"
  - "**alphaStar** достига" → "AlphaStar достига" (rewritten in F05-C08)
- **Why:**
  - The pipeline lower-cased the first letter of glossary terms.
  - "го настройва" refers back to "мрежа", which is feminine.
  - "картографира … към" is a calque of *maps … to*.
  - The bold spans in the second item come from the pipeline, not the EN.

### F05-B09 · S1 · meaning — NFSP networks: "усредненото време", "политика"
- **Where:** summaryBg.md § "NFSP - Neural Fictitious Self-Play"
- **EN:** "A *best-response network*, a DQN, learns the greedy best response to the opponent's current behaviour; an *average-policy network*, trained by supervised learning on the player's own past actions, learns the time-average of those best responses."
- **Now → Proposed:** "*мрежа за най-добър отговор* (DQN), която се обучава да изчислява алчен най-добър отговор спрямо текущото поведение на опонента, и *мрежа с усреднена политика*, обучена чрез обучение с учител върху собствените минали действия на играча, която се учи на усредненото време на тези най-добри отговори." → "*мрежа за най-добър отговор* (DQN), която научава алчен най-добър отговор на текущото поведение на опонента, и *мрежа на средната стратегия*, която чрез обучение с учител върху собствените минали действия на играча при игра с най-добрия отговор научава средното във времето на тези най-добри отговори."
- **Why:**
  - "усредненото време" means "the averaged time", not the time-average of strategies. It comes from the settled glossary (F05-T02).
  - "политика" contradicts the curated *Policy → Стратегия*; the next sentence says "Средната стратегия".
  - "при игра с най-добрия отговор" adds a precision: NFSP stores behaviour tuples in its supervised memory only when acting with the best response (Heinrich & Silver 2016, Algorithm 1).

### F05-B10 · S1 · meaning — PSRO paragraph: "усредненото време", "двуигровите", "n-игровия"
- **Where:** summaryBg.md § "Популационни методи: PSRO, NFSP, XFP"
- **EN:** "…is the special case where the best response targets the time-average of the pool. Because the population is an explicit set of opponents rather than a single moving target, these methods extend naturally beyond two-player zero-sum into the *n*-player, opponent-modeling setting this thesis is concerned with"
- **Now → Proposed:**
  - "е насочен към **усредненото време** на набора" → "е насочен към средното във времето на набора"
  - "тези методи естествено се разширяват отвъд двуигровите **игри с нулева сума** до *n*-игровия сценарий за **моделиране на противника**, който е предмет на тази дисертация" → "тези методи естествено излизат извън рамките на игрите с нулева сума за двама играчи и обхващат сценариите с *n* играчи и моделиране на противника, които са предмет на тази дисертация"
- **Why:** "двуигров" means "of two games" and "n-игров" means "of n games". The *time-average* error is the same as in F05-B09. The AlphaStar clause of the same sentence is F05-C08.

### F05-B11 · S1 · English left in the text ("attention", "bootstrap")
- **Where:** summaryBg.md §§ 5.1.1, 5.1.3, 5.4.4
- **Now → Proposed:**
  - "те използват рекурентните и attention архитектури от Част 2" → "те използват рекурентните архитектури и архитектурите с внимание от раздел 5.2"
  - "тъй като **целевите стойности по метода „bootstrap“** за всяка актуализация зависят" → "тъй като целевите стойности, получени чрез самоподкрепяне, при всяка актуализация зависят"
  - "само за изчисляване на **целеви стойности по метода „bootstrap“**" → "само за изчисляване на целевите стойности при самоподкрепяне"
  - "разликата между текущата оценка и целта с бутстрапиране" → "разликата между текущата оценка и целта, получена чрез самоподкрепяне"
- **Why:** These are English words in running text, all printed (pp. 64, 78). The chapter defines *bootstrapping* as "самоподкрепяне" and then uses two other forms for it (F05-T08). "раздел 5.2": see F05-X02.

### F05-B12 · S2 · meaning — "Цената е ефективност на извадката"
- **Where:** summaryBg.md § "NFSP - Neural Fictitious Self-Play" — "Цената е ефективност на извадката. В играта Ледюк изследването стартира NFSP за десетки хиляди епизоди"
- **EN:** "The price is sample efficiency."
- **Now → Proposed:** "Цената е ефективност на извадката." → "Цената е ниската ефективност по отношение на извадките."
- **Why:** The BG says "the price is the efficiency of the sample". The EN means that sample efficiency is what is *paid* (F05-T10).

### F05-B13 · S2 · meaning — *wall-clock* rendered as "в реално време"
- **Where:** summaryBg.md §§ "Защо невронни мрежи", "Deep CFR и неговите варианти с една мрежа"
- **EN:** "under a comparable wall-clock budget"; "at comparable wall-clock time"
- **Now → Proposed:**
  - "при сравним бюджет в реално време достигна само 1.70" → "при сравнимо време за изпълнение достигна само 1.70"
  - "за табличен MCCFR при сравними реално време" → "за табличния MCCFR при сравнимо време за изпълнение"
- **Why:** "в реално време" means *real-time*, as in real-time systems. "сравними реално време" is ungrammatical. The source is a curated entry (F05-T10).

### F05-B14 · S2 · meaning — "Глава 5 от изследването" inside Chapter 5
- **Where:** summaryBg.md §§ "Оразмеряване и капацитет", "Стабилност на обучението и диагностиката"
- **EN:** "The Chapter 5 exploration showed this directly."; "what the Chapter 5 networks showed on Leduc"
- **Now → Proposed:**
  - "Глава 5 от изследването показа това директно." → "Експериментите в тази глава показаха това пряко."
  - "което показаха мрежите от Глава 5 при Ледюк" → "което показаха мрежите от експериментите в тази глава при Ледюк"
- **Why:** The BG reads "Chapter 5 of the study showed…", written inside Chapter 5. EN: "The Chapter 5 exploration" → "The experiments in this chapter"; "the Chapter 5 networks" → "the networks in this chapter".

### F05-B15 · S2 · terminology — "смъртоносната тройка" vs "троица"
- **Where:** summaryBg.md § "Стабилност на обучението и диагностиката" — "Две стабилизиращи средства от обсъждането на „смъртоносната тройка“"
- **Now → Proposed:** "„смъртоносната тройка“" → "„смъртоносната троица“"
- **Why:** The heading of § 5.1.3 and the glossary say "смъртоносна троица". "тройка" can also be read as a school mark or a troika.

### F05-B16 · S2 · terminology — "Тясното място", "адресират"
- **Where:** summaryBg.md § "Оразмеряване и капацитет" — "Тясното място ограничава *ширината*; *остатъчните (residual) връзки* адресират *дълбочината*"
- **EN:** "The bottleneck constrains *width*; *skip (residual) connections* address *depth*"
- **Now → Proposed:** "Тясното място ограничава *ширината*; *остатъчните (residual) връзки* адресират *дълбочината*" → "Стеснението ограничава *ширината*, а *остатъчните (residual) връзки* решават проблема с *дълбочината*"
- **Why:** The curated glossary retires "тясно място" (the paragraph above says "стеснение"). "адресират" is a calque of *address*.

### F05-B17 · S2 · terminology — "енкодер", "повтарящ се слой"
- **Where:** summaryBg.md §§ 5.2.2, 5.2.3
- **Now → Proposed:**
  - "Deep Recurrent Q-Network (DRQN) комбинира конволюционен енкодер" → "Deep Recurrent Q-Network (DRQN) комбинира конволюционен кодировчик"
  - "Повтарящ се слой (RNN) прилага" → "Рекурентният слой (RNN) прилага"
  - "до които повтарящ се слой достига само косвено" → "до които рекурентният слой достига само косвено"
  - "за повтарящ се слой или трансформър" → "за рекурентен слой или трансформър"
- **Why:** The chapter and the glossary use "кодировчик" and "рекурентна мрежа". "повтарящ се" means "repeating" and hides the technical term.

### F05-B18 · S2 · terminology — overfitting / underfitting under three names
- **Where:** summaryBg.md §§ "Основи на невронните мрежи", "Оразмеряване и капацитет"
- **EN:** "— *overfitting*."; "Too little capacity and the network *underfits*, unable to express the target strategy; too much and it *overfits*, fitting the noise in a limited sample rather than the underlying structure."
- **Now → Proposed:**
  - "и след това да се представи слабо при невиждани състояния - *пренастройване*." → "и след това да се представи слабо при невиждани състояния - *преобучение* (overfitting)."
  - "При твърде малък капацитет мрежата *подпасва* (underfits), неспособна да изрази целевата стратегия; при твърде голям капацитет тя *свръхпасва* (overfits), пасвайки шума в ограничен набор от данни, вместо основната структура." → "При твърде малък капацитет мрежата остава *недообучена* (underfitting) и не може да изрази целевата стратегия; при твърде голям капацитет тя се *преобучава* (overfitting), като напасва шума в ограничения набор от данни вместо основната структура."
- **Why:** "пренастройване" means re-tuning. "подпасва" and "свръхпасва" are ad-hoc coinages. One concept should have one term (F05-T06).

### F05-B19 · S2 · terminology — "нашово" / "Нашево" for Nash (F07-B02)
- **Where:** summaryBg.md §§ 5.3.1, 5.3.2
- **EN:** "the Nash approximation the algorithm ultimately returns"; "the Nash approximation returned at the end"; "to approach Nash"
- **Now → Proposed:**
  - "нашовото приближение, което алгоритъмът в крайна сметка връща" → "приближението на равновесието на Наш, което алгоритъмът в крайна сметка връща"
  - "нашовото приближение, което се връща в края" → "приближението на равновесието на Наш, което се връща в края"
  - "за да се доближи до Нашево равновесие" → "за да се доближи до равновесие на Наш"
- **Why:** "нашов" is not a word. The glossary term is "равновесие на Наш". The one-pager occurrence is in F05-B26.

### F05-B20 · S2 · calques
- **Where:** summaryBg.md §§ "Защо невронни мрежи", 5.2.3, 5.2.4, 5.2.5, 5.3.4
- **Now → Proposed:**
  - "Двата режима се срещат при пресичане в размер на играта - под него изброяването е по-евтино и точно; над него таблицата не може да бъде конструирана и апроксимация на функция е единствената възможност." → "Двата режима се разделят от праг в размера на играта: под него изброяването е по-евтино и точно, а над него таблицата не може да бъде построена и апроксимацията на функция е единствената възможност."
  - "Игрите, към които тази работа е насочена, са над пресичането" → "Игрите, към които е насочена тази работа, са над този праг"
  - "Две по-малки точки завършват изработката." → "Остават две по-дребни практически бележки."
  - "Това аргументира за умишлено оразмеряване на мрежата" → "Това е аргумент в полза на съзнателното оразмеряване на мрежата"
  - "тиха неоперация е неразличима от труден проблем" → "обучение, което тихо не прави нищо, изглежда точно като труден проблем"
  - "Отстъпвайки назад:" → "В обобщение:"
- **Why:** These are word-for-word renderings of *crossover*, *complete the craft*, *argues for*, *a silent no-op* and *stepping back*. None of them means anything in Bulgarian. The "жива, но не сходима" phrase is rewritten in F05-C01.

### F05-B21 · S2 · grammar — case, gender, noun piles
- **Where:** summaryBg.md §§ 5.1.1, 5.2.2, 5.3.1, 5.3.4
- **Now → Proposed:**
  - "Всичко останало (неврона, нелинейността" → "Всичко останало (невронът, нелинейността"
  - "Методите по-долу се различават основно в *кое* от двете таблици те апроксимират" → "Методите по-долу се различават основно по това *коя* от двете таблици апроксимират"
  - "### Компромиси: Кога невронната CFR е от полза" → "### Компромиси: кога невронният CFR е от полза"
  - "вместо това се използва кръстосана ентропия загуба" → "вместо това се използва загубата на кръстосана ентропия"
- **Why:**
  - A subject takes the full article ("невронът").
  - "таблица" is feminine.
  - CFR is masculine everywhere else ("Табличният CFR").
  - Bulgarian does not capitalise after a colon.
  - "кръстосана ентропия загуба" is an English noun pile.

### F05-B22 · S2 · meaning — *example* and *teaching benchmark* rendered as "еталонен тест"
- **Where:** summaryBg.md § "NFSP - Neural Fictitious Self-Play" — "собственият еталонен тест на OpenSpiel използва още по-голям брой"
- **EN:** "OpenSpiel's own example uses far more still. NFSP scales to large games, where its model-free simplicity is an asset, but on a teaching benchmark it converges far more slowly than either tabular CFR or Deep CFR."
- **Now → Proposed:** "собственият еталонен тест на OpenSpiel използва още по-голям брой. NFSP се мащабира до големи игри, където неговата безмоделна простота е предимство, но при еталонен тест за обучение той се сближава значително по-бавно от табличен CFR или Deep CFR." → "собственият пример на OpenSpiel за Ледюк използва още повече епизоди. NFSP се мащабира до големи игри, където безмоделната му простота е предимство, но в учебна игра като Ледюк той се сближава значително по-бавно от табличния CFR или Deep CFR."
- **Why:** The OpenSpiel item is an example script (`nfsp_leduc_pytorch.py`, 2·10⁷ episodes), not a benchmark. "по-голям брой" has no noun it counts.

### F05-B23 · S2 · "превод" for a neural counterpart; "et al."
- **Where:** summaryBg.md § "Deep CFR и неговите варианти с една мрежа" — "Deep CFR (Brown et al., 2019) е директният невронен превод на MCCFR."
- **EN:** "Deep CFR (Brown et al., 2019) is the direct neural translation of MCCFR."
- **Now → Proposed:** "Deep CFR (Brown et al., 2019) е директният невронен превод на MCCFR." → "Deep CFR (Brown и др., 2019) е прекият невронен аналог на MCCFR."
- **Why:** "превод" is translation of a text (curated note). The curated glossary has *et al.* → "и др.", and § 5.4.3 already writes "Brown и др.".

### F05-B24 · S2 · Table 8 cells — verb form, "мощност", "извод"
- **Where:** summaryBg.md § "Четирите водещи фамилии алгоритми", Table 8
- **EN:** "Best-respond to a growing opponent pool"; "Learned value plus online search at play"; "High-stakes; inference-time compute"
- **Now → Proposed:**
  - "| Популационен (PSRO, NFSP, XFP) | Оптимално отговаряне на нарастваща популация от противници |" → "| Популационен (PSRO, NFSP, XFP) | Най-добър отговор на нарастваща популация от противници |"
  - "| Търсене + RL (Recursive Belief-based Learning, играч на игри) | Научена стойност плюс онлайн търсене по време на извод | Игри с високи залози; изчислителна мощност по време на извод | Висока |" → "| Търсене + RL (ReBeL, Student of Games) | Научена функция на стойността плюс търсене по време на игра | Игри с високи залози; изчисления по време на игра | Висока |"
- **Why:**
  - "оптимално отговаряне" is the verb-entry problem (F07-T03).
  - "изчислителна мощност" means hardware power (F07-T12).
  - "извод" reads as "conclusion". In this table *inference-time* means "during play".

### F05-B25 · S3 · terminology — "вектор на пристрастията"
- **Where:** summaryBg.md § "Основи на невронните мрежи" — "са съответно обучаемата матрица на теглата и векторът на пристрастията"
- **Now → Proposed:** "векторът на пристрастията" → "векторът на отместванията"
- **Why:** The bias term of a layer is an offset. "пристрастие" is bias in the statistical or cognitive sense, which the chapter also uses ("индуктивно пристрастие") (F05-T09).

### F05-B26 · S1 · one-pager — meaning errors, a misspelt game, a corrupted path
- **Where:** onePagerBg.md "**Подход.**", "Ключови резултати (измерени)", "**Връзка с дисертацията.**"
- **EN:** "(`implementation/step05/exploration/logs/day0{1,2}_results.json`)"; "Leduc at comparable wall time"; "8 sampled Leduc info states"; "an under-confident smoothing of equilibrium"; "a model with the right direction and the wrong frequency is what makes best-responding to an imperfect read lose to Nash"
- **Now → Proposed:**
  - "Ледиюк" (3×) → "Ледюк"
  - "day0{1.2}_results.json" → "day0{1,2}_results.json"
  - "8 взети извадкови информационни множества на Ледиюк" → "8 случайно избрани информационни състояния на Ледюк"
  - "води до недоверено изглаждане на равновесието" → "води до изгладено приближение на равновесието с прекалено ниска увереност"
  - "модел с правилна посока, но грешна честота, води до това най-добре реагиращият към несъвършено четене да загуби от Нашево равновесие" → "модел с правилна посока, но грешни честоти, е причината най-добрият отговор на неточна преценка за противника да губи срещу „Наш“"
- **Why:**
  - "Ледиюк" is a misspelling of the game name; the summary has "Ледюк".
  - The decimal-comma pass turned the shell brace "{1,2}" into "{1.2}", which names a non-existent file.
  - "недоверено" means "distrusted", not *under-confident*.
  - The last sentence has a participle as subject, "четене" for *read* (F07-B30) and "Нашево" (F07-B02).

### F05-B27 · S2 · one-pager — calques
- **Where:** onePagerBg.md
- **Now → Proposed:**
  - "**Подход.** Обхватът, заявено честно:" → "**Подход.** Казано откровено, обхватът е ограничен:"
  - "така че директният сблъсък да е честен" → "така че прякото сравнение да е коректно"
  - "Поправено е с една промяна на символ, локално закърпено." → "Поправката е от един символ и е приложена локално." (see also F05-C13)
  - "Прието правило: недоверявайте се на крива на NFSP Ледюк под ~1e6 епизода." → "Прието правило: на крива на NFSP за Ледюк под ~1e6 епизода не може да се разчита."
  - "Срещу 400-итерационен еталонен тест CFR+" → "В сравнение с еталонна стратегия от CFR+ след 400 итерации"
  - "**медианна обща вариация 0.35**" → "**медианно разстояние по обща вариация 0.35**"
  - "с Vitter резервоарен **извадков модул**" → "с резервоарна извадка по Vitter"
  - "дали табличното спрямо **невронното** подреждане се обръща точно при преминаването на броя възли в глава 3" → "дали предимството на табличния метод пред невронния се обръща точно в точката на пресичане по брой възли от глава 3"
- **Why:**
  - *stated honestly*, *head-to-head is honest* and *patched* are rendered literally.
  - "недоверявайте се" is not a form ("не се доверявайте").
  - A CFR+ *reference* is not a benchmark test.
  - "обща вариация" alone names no metric (F07-B17).
  - "tabular-versus-neural ordering flips" lost its meaning in the BG.

## T — Glossary-level terminology

### F05-T01 · S1 · "permutation-equivariant → инвариантен спрямо разместване" (wrong), plus two more names for permutation invariance
- **Where:** `llmPipeline/glossary_settled.md`: "permutation-equivariant → инвариантен спрямо разместване", "permutation-invariant → инвариантен спрямо пренареждане", "permutation invariance → инвариантност спрямо пермутации". It is printed in F05-B01.
- **Now → Proposed:** permutation-equivariant → "еквивариантен спрямо пермутации"; permutation-invariant → "инвариантен спрямо пермутации" (one root for both entries).
- **Why:** The first entry states the opposite property. The three entries give one idea three different nouns.

### F05-T02 · S1 · "time-average → Усреднено време"
- **Where:** glossary_settled.md (freq 3). It is printed in F05-B09 and F05-B10.
- **Now → Proposed:** → "средно във времето" (as a noun: "средното във времето на …"; as an adjective: "осреднен във времето").
- **Why:** "усреднено време" means "averaged time". Fictitious play averages *strategies over time*; the phrase carries that algorithm's central idea.

### F05-T03 · S2 · "self-play → самообучение" (freq 43)
- **Where:** glossary_settled.md. It is used 33× in step 06, 7× in step 05 (including the § 5.4.4 heading and Table 8), 2× in step 09 and 1× in step 08. The same glossary has "fictitious self-play → фиктивна самоигра", which the chapter also uses.
- **Now → Proposed:** self-play → "самоигра" (on first use: "игра срещу собствени копия (self-play)").
- **Why:** "самообучение" means self-study or self-learning and hides the idea that the agent plays copies of itself. It also collides with "обучение" in "обучение с подкрепление", giving "Самообучение без използване на модел" for *model-free self-play*.

### F05-T04 · S2 · "convolution → сгъвка"
- **Where:** glossary_settled.md. It is printed in fig. 17 ("Сгъвка (CNN)") and twice in § 5.2.3 (F05-B02, B04).
- **Now → Proposed:** convolution → "конволюция"; add convolutional → "конволюционен".
- **Why:** "сгъвка" is a fold. The established Bulgarian ML term is "конволюция", and the chapter itself writes "конволюционна мрежа" and "конволюциите".

### F05-T05 · S2 · "anticipatory parameter → предварителен параметър"
- **Where:** glossary_settled.md. It is printed in § 5.3.3 (fixed in F05-C06).
- **Now → Proposed:** → "антиципиращ параметър (anticipatory parameter)".
- **Why:** "предварителен" means preliminary. The parameter sets how often the agent plays its anticipated best response.

### F05-T06 · S2 · "overfitting → пренастройване"; "underfitting → недообучен"
- **Where:** glossary_settled.md. It is printed in F05-B18.
- **Now → Proposed:** overfitting → "преобучение"; underfitting → "недообучение" (verbs: "преобучава се", "остава недообучена").
- **Why:** "пренастройване" means re-tuning. The underfitting entry is an adjective where a noun is needed, so the pipeline coined "подпасва"/"свръхпасва" instead.

### F05-T07 · S2 · no entry for *grid* / *gridworld*
- **Where:** No entry exists. The pipeline chose "мрежа", which collides with the neural network (F05-B04). The same will affect chapters 6 and 9, which discuss gridworlds and Pommerman.
- **Now → Proposed:** add grid → "решетка"; gridworld → "решетъчна среда"; grid-based → "върху решетка".

### F05-T08 · S3 · pairs of entries or glossaries that disagree
- **Where:**
  - "bootstrapping → самоподкрепяне" vs "bootstrap → буутстрапинг" (the chapter prints both, plus "„bootstrap“");
  - curated "Counterfactual value → Контрафактуална стойност" vs settled "counterfactual value → контрафактична стойност" (freq 20; this chapter follows the settled form);
  - curated "Policy → Стратегия" vs settled "off-policy → извънполитикова" and the pipeline's "политика" (F05-B09).
- **Now → Proposed:** decide one form for each and store it in both files: "самоподкрепяне" (with the gloss "(bootstrapping)" on first use); one of "контрафактичен"/"контрафактуален"; off-policy → "обучение извън текущата стратегия".

### F05-T09 · S3 · "bias vector → вектор на пристрастията"
- **Where:** glossary_settled.md (F05-B25).
- **Now → Proposed:** → "вектор на отместванията"; keep "пристрастие" for the statistical and inductive senses.

### F05-T10 · S3 · calque entries "sample efficiency → ефективност на извадката" and "Wall-clock budget → Бюджет в реално време"
- **Where:** glossary_settled.md; curated `terminology_EN_BG.md` § 2 (F05-B12, B13).
- **Now → Proposed:** sample efficiency → "ефективност по отношение на извадките"; wall-clock budget → "бюджет от време за изпълнение"; wall-clock seconds → "време за изпълнение (s)".
- **Why:** "в реално време" is the *real-time* sense. "ефективност на извадката" describes a property of one sample.

## C — Content

### F05-C01 · S1 · "the advantage losses fell as expected": they rose
- **Where:** summaryBg.md § "Deep CFR и неговите варианти с една мрежа" — "Deep CFR се обучи правилно - загубите му на предимство намаляха, както се очакваше - но на 120 итерации"; § "Стабилност на обучението и диагностиката" — "Загуба, която намалява стабилно, докато оценителният показател"; EN l. 140, 164.
- **Problem:** In `implementation/step05/exploration/logs/day01_results.json` every run's advantage loss *rises*, from about 10–25 at iteration 2 to about 1 300–1 600 at iteration 120. This is by design: OpenSpiel weights outputs and targets by √t, i.e. the squared error by t, as in Linear CFR (Deep CFR paper §5.3). `findings.md` says the same ("grow from ~300 to ~1500"). The text reports the opposite and builds its "diagnostic signature" on a falling loss.
- **Now → Proposed:**
  - "Deep CFR се обучи правилно - загубите му на предимство намаляха, както се очакваше - но на 120 итерации" → "Deep CFR се обучаваше - загубите на мрежите за предимства се променяха (и растяха, защото целите се претеглят с номера на итерацията) - но на 120 итерации"
  - "Загуба, която намалява стабилно, докато оценителният показател - експлоатируемост за решавач - застива, е знак за мрежа, която е *жива, но не сходима*" → "Загуба, която се променя, докато оценителният показател - експлоатируемост за решавач - застива, е признак, че обучението *протича, но още не е сходило*"
  - EN: "Deep CFR trained correctly — its advantage losses fell as expected — but at 120 iterations" → "Deep CFR was training — its advantage losses moved (and grew, because the targets are weighted by iteration) — but at 120 iterations"; "A loss that falls steadily while" → "A loss that keeps moving while"

### F05-C02 · S2 · "frozen at the random-strategy level" (~1.69): uniform random is 2.37
- **Where:** summaryBg.md § 5.2.5 — "но програмата завърши изпълнението си и произведе правдоподобен резултат, като експлоатируемостта просто замръзна на нивото на случайната стратегия."; onePagerBg.md — "експлоатируемостта остава на нивото на случайна стратегия (**~1.69**) независимо от броя итерации"; EN summary and one-pager equivalents.
- **Problem:**
  - OpenSpiel's exploitability of `UniformRandomPolicy` on `leduc_poker` is **2.3736**, computed with the repository's `.venv`. It equals the MCCFR checkpoint-1 value in `day01_results.json` (2.3736), and NFSP starts at 2.348 (`day02_results.json`).
  - The bug-frozen value of ~1.69 is therefore *not* the random level. An untrained advantage network still yields a fixed, non-uniform strategy.
- **Now → Proposed:**
  - "като експлоатируемостта просто замръзна на нивото на случайната стратегия." → "като експлоатируемостта просто замръзна около 1.69, независимо от броя итерации."
  - onePagerBg: "експлоатируемостта остава на нивото на случайна стратегия (**~1.69**) независимо от броя итерации" → "експлоатируемостта остава около **~1.69** независимо от броя итерации (равномерно случайната стратегия има 2.37)"
  - EN: "with exploitability simply frozen at the random-strategy level" → "with exploitability simply frozen near 1.69 whatever the iteration count"
  - EN one-pager, l. 36–37, where the phrase wraps across two source lines: "sits at random-strategy" + "level (**~1.69**)" → "stays near **~1.69** (a uniform random policy scores 2.37)"
- **Note:** the *patched* 64×64 run also sits at 1.700–1.706 at every checkpoint, and the 40-iteration probe in `day02_results.json` gives 1.704. See F05-C04 and the extract, "To verify".

### F05-C03 · S2 · The Leduc information-state tensor contains no pot; it was not used in chapters 3–4
- **Where:** summaryBg.md § "Обединяване на основите в Ледюк покера" — "Вземете **Ледюк покер**, тестовата среда от глави 3–4: неговото **информационно състояние** - **тайната карта**, **историята на залозите** и **потът** - се кодира като вектор от около тридесет числа."; § "Кодиране на състоянието на играта и историята" — "а потът - една скаларна величина, което води до приблизително трийсетмерния вектор, използван в глави 3–4."; EN equivalents.
- **Problem:**
  - I inspected `pyspiel.load_game("leduc_poker").information_state_tensor(...)`. The 30 entries are: player to act (2), private card (6), public card (6) and betting sequence (16 = 2 rounds × 4 × 2). The pot appears only in the information-state *string*.
  - Chapters 3–4 were tabular on a custom engine; `implementation/step03`, `step04` never call `information_state_tensor`.
- **Now → Proposed:**
  - "неговото **информационно състояние** - **тайната карта**, **историята на залозите** и **потът** - се кодира като вектор от около тридесет числа." → "неговото информационно състояние - кой играч е на ход, тайната карта, общата карта и историята на залозите - се кодира като вектор от 30 числа."
  - "тайната карта, общата карта и историята на залозите стават one-hot полета, а потът - една скаларна величина, което води до приблизително трийсетмерния вектор, използван в глави 3–4." → "играчът на ход, тайната карта, общата карта и историята на залозите стават one-hot полета, което дава трийсетмерния вектор на OpenSpiel; размерът на пота не се подава отделно, защото следва от историята на залозите."
  - EN: "the private card, the betting history, and the pot" → "the player to act, the private card, the public card and the betting history"; "and the pot a single scalar, producing the roughly thirty-dimensional vector used in Chapters 3–4" → "producing OpenSpiel's thirty-dimensional vector; the pot is not a separate input because it follows from the betting history"

### F05-C04 · S2 · The capacity lesson rests on one seed, flat curves and contradictory explanations
- **Where:**
  - summaryBg.md § 5.1.2: "защото при ограничен бюджет на пробите по-големите мрежи задържаха твърде много параметри за твърде малко данни и пасваха шум, вместо структура"
  - § 5.2.4: "по-големите мрежи съдържаха повече параметри, отколкото няколкото хиляди обхождания можеха да ограничат, и изразходваха излишъка за пасване на шум от извадката"
  - onePagerBg.md: "съгласувано с недообучен резултат при малко различни извадки и се очаква да се обърне с повече итерации"
- **Problem:**
  - The summary explains the ranking by *overfitting* (fitting noise); the one-pager and `findings.md` say *underfitting*.
  - The sweep is one seed (42). Every curve is essentially flat from iteration 30 to 120: 64×64 gives 1.702 / 1.700 / 1.706 / 1.700.
  - The 64×64 value equals the unpatched solver's value (F05-C02).
  - The run used 40 traversals per iteration. The Deep CFR hyper-parameters used for Leduc in the SD-CFR paper use 1 500 (Steinberger 2019, App. A).
  - The Deep CFR paper (Fig. 3, FHP) reports that larger models *lower* final exploitability.
  - The data therefore cannot separate capacity from a budget or training failure.
- **Now → Proposed:**
  - "защото при ограничен бюджет на пробите по-големите мрежи задържаха твърде много параметри за твърде малко данни и пасваха шум, вместо структура" → "вероятно защото при толкова малък бюджет по-големите мрежи не получават достатъчно различни извадки, за да се обучат (резултатът е от едно начално число при почти хоризонтални криви, затова обяснението е хипотеза)"
  - "по-големите мрежи съдържаха повече параметри, отколкото няколкото хиляди обхождания можеха да ограничат, и изразходваха излишъка за пасване на шум от извадката" → "вероятното обяснение е, че няколкото хиляди обхождания не стигат, за да се обучат по-големите мрежи; при едно начално число и почти хоризонтални криви това е хипотеза, а не измерен ефект"
  - onePagerBg: "съгласувано с недообучен резултат при малко различни извадки и се очаква да се обърне с повече итерации" → "което съответства на недообучение при малко на брой различни извадки (едно начално число); при повече итерации подредбата вероятно ще се обърне"
  - EN: "because at a limited sample budget the larger networks held too many parameters for too little data and fit noise rather than structure" → "probably because at so small a budget the larger networks see too few distinct samples to train (one seed, near-flat curves, so this is a hypothesis)"; "the larger networks held more parameters than the few thousand traversals could constrain and spent the surplus fitting sampling noise" → "the likely reason is that a few thousand traversals are too few to train the larger networks; with one seed and near-flat curves this is a hypothesis, not a measured effect"

### F05-C05 · S2 · The Single Deep CFR and DREAM descriptions are inaccurate
- **Where:** summaryBg.md § "Deep CFR и неговите варианти с една мрежа", the paragraph beginning "Две усъвършенствания намаляват разхода на итерация."; EN l. 160.
- **Problem:** Checked against the full texts of arXiv:1901.07621 v4 and arXiv:2006.10410 v2.
  1. **Motives.** Neither refinement is about cost. SD-CFR avoids the *approximation error* of the average-strategy network (abstract). DREAM's contribution is being *model-free*: it needs no perfect simulator (abstract).
  2. **"Halving".** SD-CFR still trains one advantage network per player every iteration; it drops only the average-strategy network and stores every iteration's advantage network ($B^M$).
  3. **"One trajectory per iteration".** DREAM collects *T* trajectories per iteration (§5.1); outcome sampling means one trajectory *per traversal*.
  4. **"Large poker games".** The exploitability comparison in fig. 21 is **Leduc** (Fig. 1). The large-game result is head-to-head play in 5-Flop Hold'em, where "SD-CFR clearly defeats Deep CFR" (Fig. 2).
  5. **Citation.** It is cited to DREAM (see F05-S07).
- **Now → Proposed:**
  - BG, the whole paragraph from «Две усъвършенствания намаляват разхода на итерация.» to «…както показва сравнението в оригиналната статия.[^dream]» → "Последваха две усъвършенствания. *Single Deep CFR* премахва отделната стратегическа мрежа: пази мрежата за предимства от всяка итерация и възстановява средната стратегия пряко от тях, с което отпада грешката от приближаването на средната стратегия. В Ледюк то достига същата или малко по-ниска експлоатируемост от Deep CFR, а в пряк двубой в по-голямата игра 5-Flop Hold'em го побеждава.[^sdcfr] *DREAM* прави метода безмоделен, т.е. той вече не изисква перфектен симулатор на играта: вместо външно вземане на проби използва извадка по резултати (по една траектория на обхождане) и добавя научена базова линия като контролна променлива, която поема допълнителната дисперсия - същата идея за намаляване на дисперсията от раздел 5.2.[^dream]"
  - EN, the whole paragraph from «Two refinements cut the cost.» to «…as the original paper's comparison shows.[^dream]» → "Two refinements followed. *Single Deep CFR* drops the separate strategy network: it keeps the advantage network of every iteration and recovers the average strategy directly from them, which removes the approximation error of the second network. It matched or slightly beat Deep CFR in exploitability on Leduc and beat it head-to-head in the larger 5-Flop Hold'em.[^sdcfr] *DREAM* makes the method model-free, so it no longer needs a perfect simulator of the game: it replaces external sampling with outcome sampling (one sampled trajectory per traversal) and adds a learned baseline as a control variate to absorb the extra variance, the same variance-reduction idea from Section 5.2.[^dream]"
  - Add a footnote to both files (F05-S07).

### F05-C06 · S2 · NFSP picks its policy per episode, not per step
- **Where:** summaryBg.md § "NFSP - Neural Fictitious Self-Play" — "Двете мрежи са свързани чрез *предварителен параметър* $\eta$: на всяка стъпка агентът действа от своята мрежа за най-добър отговор с вероятност $\eta$, а в останалите случаи - от своята мрежа с усреднена политика."; EN "at each step the agent acts from its best-response network with probability $\eta$ and from its average-policy network otherwise."
- **Problem:** Heinrich & Silver (2016), Algorithm 1, sets the policy once per episode: "for each episode do: Set policy σ ← ε-greedy(Q) with probability η, Π with probability 1 − η". OpenSpiel's `nfsp.py` does the same (`_sample_episode_policy` at episode end). The sentence also carries the glossary errors "предварителен" (F05-T05) and "политика".
- **Now → Proposed:**
  - BG → "Двете мрежи са свързани чрез *антиципиращия параметър* $\eta$: в началото на всеки епизод агентът избира с вероятност $\eta$ да играе с мрежата за най-добър отговор, а в останалите случаи - с мрежата на средната стратегия."
  - EN: "at each step the agent acts from its best-response network with probability $\eta$ and from its average-policy network otherwise." → "at the start of each episode the agent chooses, with probability $\eta$, to play it with its best-response network, and otherwise with its average-policy network."

### F05-C07 · S2 · "Model-free self-play carries no pressure toward unexploitability": out of date, and contradicted by the chapter's own NFSP
- **Where:** summaryBg.md § "Самообучение без използване на модел: PPO, DQN, MAPPO, QMIX" — "Тяхната слабост е огледален образ на тяхната сила: без концепция за контрафактично съжаление, те не притежават вграден натиск към неексплоатируемост, така че един безмоделен агент може да бъде силен средностатистически, но все пак да остане експлоатируем от противник в най-лошия случай - което е именно причината експлоатируемостта да трябва да се измерва отделно, тема на по-късна секция."; EN l. 214.
- **Problem:**
  - NFSP, presented two sections earlier as "безмоделна", converges toward Nash.
  - Model-free methods that change the learning dynamics do converge: R-NaD (DeepNash, Science 2022: "converges to an approximate Nash equilibrium, instead of 'cycling' around it"), NeuRD (equivalent to softmax CFR in the tabular case) and magnetic mirror descent (ICLR 2023).
  - Rudolph et al. (ICLR 2026) ran over 7 000 runs on five games with millions of information states. They found that "NFSP, PSRO, ESCHER, and R-NaD fail to outperform the generic PG methods (MMD, PPO, PPG)" in exploitability.
  - The "later section" is an unwritten stub (F05-X01).
- **Now → Proposed:**
  - BG → "Наивната самоигра с алгоритъм за един агент може да се върти в цикъл и да остане силно експлоатируема. Затова по-новите безмоделни методи променят динамиката на обучението (NeuRD, R-NaD в DeepNash, магнитно огледално спускане), така че играта да се доближава до равновесие.[^neurd][^deepnash][^mmd] Мащабно сравнение в пет големи игри показва, че общи методи с градиент на стратегията (PPO, MMD) не отстъпват по експлоатируемост на методите, основани на фиктивна игра, двоен предсказвач и CFR.[^rudolph2026] Затова експлоатируемостта на всеки безмоделен агент трябва да се измерва, а не да се предполага." (This uses "самоигра", F05-T03.)
  - EN → "Naive self-play with a single-agent algorithm can cycle and stay highly exploitable, which is why newer model-free methods change the learning dynamics (NeuRD, R-NaD in DeepNash, magnetic mirror descent) so that play approaches equilibrium. A large exploitability study over five games found that generic policy-gradient methods (PPO, MMD) were not outperformed by methods based on fictitious play, double oracle or CFR. Exploitability therefore has to be measured for every model-free agent, not assumed."
  - Footnotes: F05-S09.

### F05-C08 · S2 · "They are how AlphaStar reached grandmaster level": overclaim
- **Where:** summaryBg.md § "Популационни методи…" — "- и именно чрез тях **alphaStar** достига нивото на гросмайстор в StarCraft II."; EN "— and they are how AlphaStar reached grandmaster level at StarCraft II."
- **Problem:** AlphaStar was first trained by supervised learning on human games and then refined in a continuous league of agents (DeepMind's AlphaStar blog, verified; Vinyals et al., Nature 2019). League training is population-based, but AlphaStar is not a PSRO/NFSP result, and the claim is uncited.
- **Now → Proposed:**
  - BG: "- и именно чрез тях **alphaStar** достига нивото на гросмайстор в StarCraft II." → "; популационно обучение от този вид е в основата и на „лигата“ от агенти, с която AlphaStar, първоначално обучен чрез подражание на човешки игри, достига нивото на гросмайстор в StarCraft II.[^vinyals2019]"
  - EN: "— and they are how AlphaStar reached grandmaster level at StarCraft II." → "; population training of this kind is also at the core of the league with which AlphaStar, first trained by imitating human games, reached grandmaster level in StarCraft II.[^vinyals2019]"

### F05-C09 · S2 · Stale references to Chapter 15 and to parts that were never written
- **Where:** summaryBg.md intro, §§ 5.1.3, 5.2.3, 5.2.4, 5.4.4 (the last one is handled in F05-C07); EN equivalents.
- **Now → Proposed:**
  - "Той изпълнява две функции: служи като бързо опресняване при преминаване през по-късните глави и като основен източник за синтеза на публичния доклад от Глава 15." → "Той служи като кратък справочник при четенето на следващите глави."
    EN: "It serves two purposes: as a quick refresher while progressing through later chapters, and as a primary source for the Chapter 15 public report synthesis." → "It serves as a quick reference while reading the later chapters."
  - "а техниките за моделиране на противника и бърза адаптация от части 4 и 5 се опитват да я проследят директно" → "а техниките за моделиране на противника и бърза адаптация (глави 7 и 12) се опитват да я проследят пряко"
    EN: "and the opponent-modeling and fast-adaptation techniques of Parts 4 and 5 attempt to track it directly." → "and the opponent-modeling and fast-adaptation techniques of Chapters 7 and 12 attempt to track it directly."
  - "идея, която Част 4 развива като научена абстракция, а Част 5 - като научени състояния на убеждение." → "идея, която стои в основата на научените абстракции и на научените състояния на убеждение (глава 6)."
    EN: "an idea Part 4 develops into learned abstraction and Part 5 into learned belief states." → "the idea behind learned abstractions and learned belief states (Chapter 6)."
  - "семето на научена абстракция или състояние на убеждението (Части 4 и 5)" → "зародишът на научена абстракция или на състояние на убеждението"
    EN: "the seed of a learned abstraction or belief state (Parts 4 and 5)" → "the seed of a learned abstraction or belief state"
  - "принципът, залегнал в основата на resNets и дълбоките мрежи за стойности от Част 4." → "принципът, залегнал в основата на ResNet и на дълбоките мрежи за стойности от глава 6."
    EN: "the idea behind ResNets and the deep value networks of Part 4." → "the idea behind ResNets and the deep value networks of Chapter 6."
- **Why:**
  - Chapters 13–15 were never written.
  - Parts 4 (except §§ 5.4.1–5.4.4) and 5 exist only as HTML comments (F05-X01).
  - Deep value networks appear in chapter 6, not in Part 4.
  - The BG stub comment still says "Step 1/3/4/6", but it disappears with F05-X01.

### F05-C10 · S3 · "Player of Games" is published as *Student of Games*; "reach the strongest play"
- **Where:** summaryBg.md § 5.4.3 — "Тези системи достигат най-силно ниво на игра, но са най-сложни за изграждане"; EN "Player of Games (Schmid et al., 2023) generalizes the recipe into one algorithm that handles both perfect and imperfect information. These systems reach the strongest play"
- **Problem:** The 2023 paper is "Student of Games: A unified learning algorithm for both perfect and imperfect information games", *Science Advances* 9(46), eadg3256 (Crossref). Its own claim is "strong empirical performance", not the strongest play in each game. ReBeL's claim is superhuman heads-up no-limit hold'em.
- **Now → Proposed:**
  - "Тези системи достигат най-силно ниво на игра, но са най-сложни за изграждане" → "Тези системи са в основата на най-силните резултати в покера (ReBeL достига свръхчовешко ниво в безлимитния холдем за двама), но са най-сложни за изграждане"
  - EN: "Player of Games (Schmid et al., 2023)" → "Student of Games (Schmid et al., 2023; preprint title Player of Games)"; "These systems reach the strongest play" → "These systems underlie the strongest poker results (ReBeL is superhuman in heads-up no-limit hold'em)"
  - Names in the BG: F05-B07.

### F05-C11 · S2 · MAPPO and QMIX are cooperative, not "cooperative and mixed"
- **Where:** summaryBg.md § 5.4.4 — "Те са основните методи в многоагентното обучение с подкрепление: PPO и DQN за едноагентното ядро и многоагентните разширения MAPPO и QMIX за кооперативни и смесени сценарии."; EN "…MAPPO and QMIX for cooperative and mixed settings."
- **Problem:** QMIX factorises a *team* value function (Rashid et al., ICML 2018). MAPPO is "The Surprising Effectiveness of PPO in *Cooperative* Multi-Agent Games" (Yu et al., NeurIPS 2022). Both titles were verified on arXiv.
- **Now → Proposed:** "за кооперативни и смесени сценарии" → "за кооперативни сценарии"; EN "for cooperative and mixed settings" → "for cooperative settings". Sources: F05-S05.

### F05-C12 · S2 · One-pager numbers: selective range, unverifiable "400+", untraceable CFR+ value
- **Where:** onePagerBg.md — "Ледиюк при сравнимо реално време: CFR+ **0.00123** (400 итерации, 92 s), табличен MCCFR **0.0967** (50,000 итерации, 68 s), Deep CFR **1.49–1.70** (120 итерации, ~95 s)"; "Кривите на Deep CFR са плоски от итерация 30 до 120, където в статията се използват 400+"; EN "Deep CFR **1.49-1.70**", "iteration 30 to 120 where the paper uses 400+"
- **Problem:**
  1. At the same budget the 32×32 network reached **1.144** (`day01_results.json`), so the Deep CFR range is 1.14–1.70.
  2. "the paper uses 400+" could not be verified. `findings.md` attributes 400+ to "the original paper and OpenSpiel's own example script". The installed OpenSpiel example `deep_cfr_pytorch.py` uses 101 iterations × 375 traversals, and the Deep CFR paper reports FHP runs with 10 000 traversals per iteration. The verifiable shortfall is traversals: 40 per iteration here, against 1 500 in the Leduc setup of Steinberger (2019, App. A).
  3. The CFR+ value 0.00123 / 92 s is in `findings.md` only, not in the two JSON files the one-pager names as the source of "all numbers".
- **Now → Proposed:**
  - "Deep CFR **1.49–1.70** (120 итерации, ~95 s)" → "Deep CFR **1.14–1.70** според размера на мрежата (120 итерации, 87–101 s)"
  - "където в статията се използват 400+" → "при само 40 обхождания на итерация (в настройката за Ледюк на Steinberger, 2019, те са 1 500)"
  - EN: "Deep CFR **1.49-1.70**" → "Deep CFR **1.14-1.70** across network sizes"; "where the paper uses 400+" → "with only 40 traversals per iteration (Steinberger 2019 uses 1,500 on Leduc)"
  - Either log the CFR+ run in `day02_results.json` or cite `findings.md` as its source.

### F05-C13 · S2 · The OpenSpiel bug was fixed upstream in March 2026
- **Where:** onePagerBg.md — "Загубите за предимство се връщат мълчаливо като `None`, а експлоатируемостта остава на нивото на случайна стратегия (**~1.69**) независимо от броя итерации. Поправено е с една промяна на символ, локално закърпено."; EN "A one-character fix, patched locally."; `implementation/step05/exploration/findings.md` §4 ("File a fix upstream").
- **Problem:** Upstream commit `d499542d` ("Fix advantage network learning", 25 Mar 2026) changes exactly `if len(samples.info_state == 0):` → `if len(samples.info_state) == 0:`. It was released in v1.6.13 (1 May 2026). Both were verified via the GitHub API. The repository's `.venv` now has open_spiel 1.6.15, where the local patch is a no-op.
- **Now → Proposed:**
  - "Поправено е с една промяна на символ, локално закърпено." → "Поправката е от един символ; тя е приложена локално, а в OpenSpiel е отстранена независимо през март 2026 г. (версия 1.6.13)."
  - EN: "A one-character fix, patched locally." → "A one-character fix, patched locally; fixed upstream independently in March 2026 (OpenSpiel 1.6.13)."
  - The "file a fix upstream" item in `findings.md` is obsolete.

## S — Sources

### F05-S01 · S2 · SOURCE_GAPS row 1 (tabular memory per information set): cite Zinkevich et al. (2007)
- **Where:** summaryBg.md § "Защо невронни мрежи" — "Табличният CFR и неговите варианти на Монте Карло (Глави 2–4) съхраняват стойност на съжалението и стойност на стратегията във всяко информационно множество, така че разходът им за памет е пропорционален на броя на информационните множества, който нараства с размера на играта."
- **Proposal (cite):** append a footnote. Verified in the NeurIPS 2007 PDF: "Repeated play requires storing $R_i^t(I,a)$ for every information set $I$ and action $a$, and updating it after each iteration." The entry already exists in chapter 2 as `[^zinkevich2007]` (Zinkevich, Johanson, Bowling & Piccione, *NeurIPS 20*, 1729–1736). Reuse it only after the central footnote-prefix fix (F07-X01); otherwise define `[^zinkevich2007c05]` with the same text.

### F05-S02 · S2 · SOURCE_GAPS row 2 ("convolutions dominate grid domains"): soften and cite LeCun, Bengio & Hinton (2015)
- **Where:** summaryBg.md § 5.2.1 — "тази *еквивариантност спрямо транслация* обяснява защо конволюциите доминират в мрежовите области."
- **Proposal (soften + cite):**
  - → "тази *еквивариантност спрямо транслация* обяснява защо конволюциите са стандартният избор за дъски и решетки.[^lecun2015]" (this also fixes F05-B04)
  - EN "why convolutions dominate grid domains" → "why convolutions are the standard choice for boards and grids"
  - Footnote: `[^lecun2015]: LeCun, Y., Bengio, Y. & Hinton, G. (2015). "Deep learning." *Nature* 521, 436–444. DOI 10.1038/nature14539.`
- **Verified:** Crossref metadata, and the text of the author PDF: "if a motif can appear in one part of the image, it could appear anywhere, hence the idea of units at different locations sharing the same weights".

### F05-S03 · S2 · SOURCE_GAPS row 3 (AlphaStar architecture): cite Vinyals et al. (2019)
- **Where:** summaryBg.md § 5.2.2 — "AlphaStar отива по-далеч, кодирайки множество единици с трансформър"
- **Proposal (cite):** append `[^vinyals2019]` at the end of the sentence. The same note serves F05-C08: `[^vinyals2019]: Vinyals, O. et al. (2019). "Grandmaster level in StarCraft II using multi-agent reinforcement learning." *Nature* 575, 350–354. DOI 10.1038/s41586-019-1724-z.`
- **Verified:**
  - Crossref.
  - DeepMind's AlphaStar blog: "a transformer torso to the units …, combined with a deep LSTM core, an auto-regressive policy head with a pointer network".
  - The minimap-ResNet and scalar-MLP encoders are confirmed only by secondary sources (Perceiver IO, mini-AlphaStar), because the Nature page required a login. Check them in the Nature Methods before quoting.
- **Optional:** DRQN in the same paragraph: `Hausknecht, M. & Stone, P. (2015). "Deep Recurrent Q-Learning for Partially Observable MDPs." *arXiv:1507.06527*` (verified on arXiv). Its output is a linear layer, so "изходен MLP" is slightly loose.

### F05-S04 · S2 · SOURCE_GAPS row 4 ("four leading families"): soften, and cite a published grouping
- **Where:** summaryBg.md § 5.4.1 — "Това е едно от четирите основни семейства, които определят съвременното равнище, като изборът между тях до голяма степен зависи"
- **Proposal (soften + cite):**
  - "Това е едно от четирите основни семейства, които определят съвременното равнище" → "Това е едно от четирите големи семейства, по които в тази глава се подреждат съвременните методи"
  - EN "It is one of four broad families that define the current state of the art" → "It is one of four broad families this chapter uses to organise current methods"
  - Cite `[^rudolph2026]` for the grouping of deep RL methods for imperfect-information games into fictitious-play-, double-oracle- and CFR-based versus generic policy-gradient methods. Verified in the arXiv v4 full text, ICLR 2026. It maps onto three of the four rows; search + learning is cited separately (F05-S08).
- **Why:** No single source defines exactly these four families as "the state of the art".

### F05-S05 · S2 · SOURCE_GAPS row 5 (PPO, DQN, MAPPO, QMIX as the mainstream): cite the four originals
- **Where:** summaryBg.md § 5.4.4 — "Те са основните методи в многоагентното обучение с подкрепление"
- **Proposal (cite, with the fix in F05-C11):**
  - `Schulman, J. et al. (2017). "Proximal Policy Optimization Algorithms." *arXiv:1707.06347*`
  - `Mnih, V. et al. (2015). "Human-level control through deep reinforcement learning." *Nature* 518, 529–533. DOI 10.1038/nature14236`
  - `Yu, C. et al. (2022). "The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games." *NeurIPS Datasets and Benchmarks*; arXiv:2103.01955`
  - `Rashid, T. et al. (2018). "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning." *ICML*; arXiv:1803.11485`
  
  Verified: arXiv API (venues from the arXiv comments), Crossref for Mnih. If DQN/PPO already have footnotes in chapter 1, reuse those after F07-X01.
- **Soften:** "Те са основните методи" → "Те са сред най-използваните методи".

### F05-S06 · S3 · SOURCE_GAPS row 6 (memory models: S4/Mamba/neural ODE…): the claim sits in a stub that does not print
- **Where:** summaryBg.md § "Памет и време". The text is an HTML comment; only the heading prints (F05-X01).
- **Proposal (remove):** delete the heading with the other stubs. Nothing needs a citation now.
- **If the section is written:** verified candidates (arXiv API / Crossref, metadata only):
  - S4, Gu, Goel & Ré, ICLR 2022, arXiv:2111.00396
  - Mamba, Gu & Dao, arXiv:2312.00752
  - Neural ODE, Chen et al., arXiv:1806.07366
  - Liquid time-constant networks, Hasani et al., AAAI-21, arXiv:2006.04439
  - NTM, Graves et al., arXiv:1410.5401
  - DNC, Graves et al., *Nature* 538, 471–476, 2016, DOI 10.1038/nature20101
  - Modern Hopfield networks, Ramsauer et al., arXiv:2008.02217

### F05-S07 · S2 · The Single Deep CFR claim and fig. 21 are cited to DREAM; the source paper is missing
- **Where:** summaryBg.md § 5.3.2 — "При големи покер игри *Single Deep CFR* съвпада или леко превъзхожда *Deep CFR*, докато обучава една мрежа вместо две, както показва сравнението в оригиналната статия.[^dream]"
- **Proposal (cite):** add `[^sdcfr]: Steinberger, E. (2019). "Single Deep Counterfactual Regret Minimization." *arXiv:1901.07621*.` to both summaries and use it as in F05-C05. Verified: arXiv v4 full text (Fig. 1 Leduc, Fig. 2 5-FHP, App. A). It is an arXiv preprint with no venue found.

### F05-S08 · S2 · ReBeL, Student of Games and NeuRD are named without a source
- **Where:** summaryBg.md §§ 5.3.4, 5.4.3 — "ReBeL (Brown и др., 2020) прави това прецизно"; the Student of Games sentence; "- neuRD, например, преформулира обновяването на съжалението като стъпка на градиента на стратегията, за да комбинира стабилността на CFR с оптимизация на невронна стратегия - но"
- **Proposal (cite + correct):**
  - `[^rebel]: Brown, N., Bakhtin, A., Lerer, A. & Gong, Q. (2020). "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games." *NeurIPS 33*; arXiv:2007.13544.` Verified: arXiv abstract and the NeurIPS 2020 proceedings page. The chapter's description (public belief state, depth-limited subgame, CFR with a learned value network) matches the paper.
  - `[^sog]: Schmid, M. et al. (2023). "Student of Games: A unified learning algorithm for both perfect and imperfect information games." *Science Advances* 9(46), eadg3256. DOI 10.1126/sciadv.adg3256.` Verified: Crossref and arXiv:2112.03178.
  - `[^neurd]: Hennes, D. et al. (2020). "Neural Replicator Dynamics: Multiagent Learning via Hedging Policy Gradients." *AAMAS*, 492–501; arXiv:1906.00190.` Verified: arXiv abstract and the AAMAS proceedings listing.
  - Correct the NeuRD description. The paper is "a one-line change to policy gradient … that bypasses the gradient step through the softmax", following the replicator dynamics; it "has formal equivalence to softmax counterfactual regret minimization". It is not a recast regret update:
    - BG: "преформулира обновяването на съжалението като стъпка на градиента на стратегията, за да комбинира стабилността на CFR с оптимизация на невронна стратегия" → "променя с един ред обновяването по градиента на стратегията така, че то да следва репликаторната динамика; в табличния случай методът е еквивалентен на softmax CFR[^neurd]"
    - EN: "recasts the regret update as a policy-gradient step to combine CFR's stability with neural policy optimization" → "changes the softmax policy-gradient update by one line so that it follows the replicator dynamics; in the tabular case it is equivalent to softmax CFR[^neurd]"

### F05-S09 · S2 · The survey stops in 2020: no ESCHER, R-NaD/DeepNash, MMD, or the 2026 re-evaluation
- **Where:** summaryBg.md §§ 5.3.2–5.4.4 and Table 8
- **Problem:** Chapter I § 1.3 needs the current state of the art. All four works below are verified and bear directly on the chapter's claims (F05-C07).
- **Proposal (cite):**
  - `[^escher]: McAleer, S., Farina, G., Lanctot, M. & Sandholm, T. (2023). "ESCHER: Eschewing Importance Sampling in Games by Computing a History Value Function to Estimate Regret." *ICLR*; arXiv:2206.04122.` Verified: arXiv abstract and the ML Anthology ICLR 2023 listing. Mention it after DREAM in § 5.3.2: it removes the importance-sampling term and beats DREAM and NFSP head-to-head in over 90 % of dark-chess games.
  - `[^deepnash]: Perolat, J. et al. (2022). "Mastering the game of Stratego with model-free multiagent reinforcement learning." *Science* 378, 990–996. DOI 10.1126/science.add4679.` Verified: Crossref and the arXiv:2206.15378 abstract.
  - `[^mmd]: Sokota, S. et al. (2023). "A Unified Approach to Reinforcement Learning, Quantal Response Equilibria, and Two-Player Zero-Sum Games." *ICLR*; arXiv:2206.05825.` Verified: arXiv; ICLR 2023 header on the PDF.
  - `[^rudolph2026]: Rudolph, M. et al. (2026). "Reevaluating Policy Gradient Methods for Imperfect-Information Games." *ICLR*; arXiv:2502.08938.` Verified: arXiv v4 full text, whose header reads "Published as a conference paper at ICLR 2026".

### F05-S10 · S3 · Spot-check of the existing footnotes
- **Findings:**
  - `deepcfr` is correct (arXiv:1811.00164, ICML 2019). Algorithm 1, the from-scratch retraining and the Linear CFR weighting all match the chapter.
  - `dream` is correct (arXiv:2006.10410, three authors; an arXiv preprint, no venue found). The abstract's main point is model-freeness (F05-C05).
  - `nfsp` is correct (arXiv:1603.01121).
  - `openspiel` is correct (arXiv:1908.09453).
  - `psro_ref` is correct (NIPS 2017 per arXiv:1711.00832).
  - `resnet` is correct. Optionally add "770–778. DOI 10.1109/CVPR.2016.90" (Crossref).
  - The in-text "глави 9 и 11 от Sutton & Barto (2-ро издание)" is correct: the deadly triad is § 11.3 (checked in the 2020 PDF).
  - DREAM is cited as "Steinberger, Lerer & Brown (2020)" in the footnote, but the text never names it with authors. That is fine.

### F05-S11 · S3 · `[^deepcfr]` attached to variance reduction, which Deep CFR does not use
- **Where:** summaryBg.md § 5.2.5 — "Нормализиране на входа и разумна инициализация на теглата, споменати по-рано, допълват списъка: и двете поддържат активациите и градиентите в използваем диапазон още от първата стъпка.[^deepcfr]"
- **Problem:** The paragraph's footnote supports the reservoir-sampling sentence, not baselines or control variates.
- **Proposal (move + cite):**
  - Move `[^deepcfr]` to the end of the reservoir sentence ("…през всички итерации (Част 3).").
  - After "използване на контролни променливи" add `[^vrmccfr]: Schmid, M., Burch, N., Lanctot, M., Moravčík, M., Kadlec, R. & Bowling, M. (2019). "Variance Reduction in Monte Carlo Counterfactual Regret Minimization (VR-MCCFR) for Extensive Form Games Using Baselines." *AAAI* 33, 2157–2164.` Verified: Crossref and arXiv:1809.03057.

## X — Structure

### F05-X01 · S1 · 13 empty headings print, and five of them are in the table of contents
- **Where:** p. 78 (printed folio 77). The following have no body text; their content is an HTML comment that pandoc drops.
  - § 5.4.5 "Невронни мрежи за абстракция, моделиране на противника и представяне на убеждението"
  - § 5.4.6 "Оценяване на невронните стратегии: експлоатируемостта в мащаб"
  - § 5.4.7 "Обобщаване отвъд покера: среди и инструменти"
  - § 5.5 "Част 5 - Експериментална / граница" and §§ 5.5.1–5.5.6
  - § 5.6 "Синтез" and §§ 5.6.1–5.6.2
  
  The bundle TOC (p. 3) lists "Част 5 - Експериментална / граница" and "Синтез". The same holds in the EN.
- **Fix:**
  - Delete these 13 headings from both summaries, or move each heading into its STUB comment.
  - Add one sentence at the end of the intro paragraph. BG: "Разделите за научената абстракция, оценяването на невронни стратегии, експерименталните архитектури и обобщаващата карта на решенията са планирани, но не са включени в тази версия." EN: "Sections on learned abstraction, evaluating neural policies, experimental architectures and a closing decision map are planned but not included in this version."
  - This removes SOURCE_GAPS row 6 (F05-S06), "тема на по-късна секция" (F05-C07) and the stale BG stub pointers "Step 1/3/4/6".

### F05-X02 · S2 · The candidate's TOC comment was not applied: all five "Част N -" prefixes remain
- **Where:** `user_comments_2026-08-01.json`, chapter 0, TOC page 4. The comment "тези част 1 част 2 няма нужда от тях" was made on "Част 1 - О…", i.e. this chapter's "Част 1 - Основни положения".
  - summaryBg.md still has "## Част 1 - Основни положения", "## Част 2 - Архитектура и композиция", "## Част 3 - Невронни мрежи в CFR", "## Част 4 - Други невронни приложения" and "## Част 5 - Експериментална / граница".
  - summaryEn.md has "## Part 1 — Fundamentals" … "## Part 5 — Experimental / Frontier".
  - All five print as §§ 5.1–5.5 and in the TOC.
- **Fix:**
  - Headings: "## Част 1 - Основни положения" → "## Основни положения"; "## Част 2 - Архитектура и композиция" → "## Архитектура и композиция"; "## Част 3 - Невронни мрежи в CFR" → "## Невронни мрежи в CFR"; "## Част 4 - Други невронни приложения" → "## Други невронни приложения". Remove Part 5 (F05-X01). The EN is the same without "Part N —".
  - In-text references then need section numbers:
    - "точка, която част 2 развива в изрични насоки за оразмеряване" → "…раздел 5.2…"
    - "от части 3 и 4" → "от раздели 5.3 и 5.4"
    - "Решенията за архитектура в останалата част от Част 2" → "…от раздел 5.2"
    - "Практическият урок за останалата част от Част 2 е" → "…от раздел 5.2 е"
    - "(Част 3)" → "(раздел 5.3)"
    - "същата идея за намаляване на дисперсията от Част 2" → "…от раздел 5.2"
    - "безмоделните методи за самообучение от Част 4 се превръщат в по-естественото решение" → "…от раздел 5.4…"
    - "Част 3 представи един от начините" → "Раздел 5.3 представи един от начините"
    - "(Deep CFR, DREAM, neuRD) от Част 3" → "(Deep CFR, DREAM, NeuRD) от раздел 5.3"
    - "от Част 2" in § 5.4.4 → "от раздел 5.2" (F05-B11)
    - The references to Parts 4–5 in §§ 5.1.3, 5.2.3 and 5.2.4 are handled in F05-C09.
    - "Няколко метода в следващите части са най-добре разбрани като отговори на нея" → "Няколко метода в следващите раздели се разбират най-добре като отговор на нея"
  - EN: "Part N" → "Section 5.N" in the same places.

### F05-X03 · S3 · Leftover temporary markup
- **Where:** both summaries contain "<!-- APPROVED-HIGHLIGHT START (temporary; remove before final build) -->", a `<div style="background-color:#e6f9e6 …">` and the matching end markers.
- **Fix:** delete the four lines. They do not print (pp. 61–76 show no background), but the comment itself says they must go before the final build.

### F05-X04 · S3 · Half-empty page before fig. 17
- **Where:** p. 65. Fig. 17 is forced `fig-pos="H"` and does not fit, so about 45 % of the page is blank.
- **Fix:** resolved by the smaller printed height in F05-G02. If not, let this figure float (`fig-pos="htbp"`).
