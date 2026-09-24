# Step 06a — final review (Introduction, DeepStack, Libratus, Pluribus; one-pager)

**Summary:** The survey is accurate on its headline numbers (every figure below was checked against the primary papers or their supplements), but the Bulgarian text of this half is the weakest reviewed so far, and three things matter most. (1) Meaning errors a reader will notice on almost every page: "*звуково*" (acoustic) for *sound*, "мрежата от ходове" for the *turn* network, "ръчни клъстера" (manual) for *hand clusters*, "възмущава" (outrages) for *perturbs*, "подучастъци" (plots of land) for *subgames*, "процент победи" for a chip win rate, "в шест ръце" for *six-handed*, "двуигров" (two-game) for *two-player*, a reversed trade-off ("за сметка на сила"), an English heading ("The gap it closed"), English table cells and 31 × "deepStack". Many come from settled glossary entries (new T01–T18), so other chapters inherit them. (2) All three architecture figures are unreadable in print: text overlaps text in every figure, labels print at 5.2–6.9 pt, the printed BG renders are stale (the mapping already fixes "Адаптация" for *gadget*), and the mapping still has a Latin "a", "финален" for *fine*, "множество" for *set* (verb). (3) Content: the one-pager inverts the Go result ("1,100 Elo **below**" — it is 1,100 Elo **above** Pachi), the Pluribus section contradicts the Libratus section on Libratus's compute (15 M vs 6 M/25 M core-hours), overstates the Loeliger result and the pro count, and the chapter's reason for why these systems do not adapt drops the reason the Pluribus paper itself gives (sample inefficiency) — which is the one Chapter I needs.
**Counts:** S1 30 · S2 81 · S3 9   (by category: G 5 · B 63 · T 18 · C 12 · S 18 · X 4) — in addition, decided centrally and not itemised: 209 × " - " as a dash, 9 decimal points and 8 "20,000"-style thousands separators, 215 bold spans in BG lines 1–298 vs 142 in the corresponding EN (lines 1–809), and 3 of the 4 footnote markers on pp. 79–103 that print without a note on the page (F07-X01: `burch2014` → p. 26, `libratus` → p. 53, `brown2017` → p. 41; only `deepstack` prints on p. 79).

Conventions in this file: quotes are **raw markdown** from `summaryBg.md` (lines 1–298) / `onePagerBg.md`; "EN" quotes come from `summaryEn.md` (lines 1–809) / `onePager.md`. Proposals keep the chapter's " - " dashes and decimal points (fixed centrally). Page numbers are PDF pages of `allSummaries_bg.pdf` (printed number = PDF page − 1). Printed type sizes = matplotlib fs × (printed width ÷ saved width): fig. 24 16.2 cm ÷ 21.94 cm = 0.738; fig. 25 16.7 ÷ 21.51 = 0.776; fig. 26 16.7 ÷ 21.69 = 0.770 (saved at 330 dpi; effective ppi 425–447, so none is soft). Primary sources were read in full text: DeepStack arXiv:1701.01724v3 (incl. supplement); Libratus *Science* first-release PDF (NSF PAR 10077416) and the 8-page final version; Pluribus *Science* author PDF and supplementary materials (noambrown.github.io); NeurIPS-17 arXiv:1705.02955; NeurIPS-18 arXiv:1805.08195; IJCAI-17 demo paper; Lisý & Bowling arXiv:1612.07547; Ganzfried arXiv:1510.08578; Sandholm CMU 15-888 F21 Lecture 13 slides.

Terminology used in the proposals (see T): sound → коректен; unsafe → небезопасен; continual re-solving → непрекъснато пререшаване; re-solve → пререшаване; continuation strategy → стратегия за продължение; leaf → листо; action translation → транслация на действия (curated); augmented subgame → разширена под-игра (curated); win rate → темп на печалба; two-player → за двама играчи; six-player/multiplayer → с шестима / с много играчи; offline/online → офлайн/онлайн (as the chapter's tables already do); counterfactual → контрафактичен (corpus majority, see T12); blueprint → план (see T13); compute → изчислителни разходи (F07-T12).

## G — Figures

### F06a-G01 · S1 · Bulgarian captions for the three figures
- **Where:** summaryBg.md image alt text of figs. 24–26 (pp. 83, 90, 99). All three print in English (known corpus-wide defect).
- **Now → Proposed:**
  - "![DeepStack architecture: offline intuition-building (left) feeding a shared deep counterfactual-value network, reused as the leaf evaluator inside the online continual-re-solving loop (right).]" → "![Архитектура на DeepStack: предварителното (офлайн) изграждане на „интуиция“ (вляво) обучава обща дълбока мрежа за контрафактични стойности, която след това служи за оценяване на листата в онлайн цикъла на непрекъснато пререшаване (вдясно).]" (if F06a-G02's two-row layout is adopted: "(вляво)" → "(горе)", "(вдясно)" → "(долу)")
  - "![Libratus's three-module pipeline: an offline blueprint (top), the online nested safe-subgame solver that plays it (middle), and the overnight self-improver that grafts solved holes back into the blueprint (bottom, feedback arrow).]" → "![Тримодулният конвейер на Libratus: предварително изчисленият план (горе), онлайн модулът за вложено безопасно решаване на под-игри, чрез който планът се изиграва (в средата), и нощният модул за самоусъвършенстване, който вгражда решените „дупки“ обратно в плана (долу, стрелката за обратна връзка).]"
  - "![Pluribus's two-phase architecture: an offline Linear-MCCFR blueprint (top) reused as the source of k=4 continuation strategies inside the online depth-limited search (bottom).]" → "![Двуфазната архитектура на Pluribus: предварително изчисленият с Linear MCCFR план (горе) служи като източник на k=4 стратегии за продължение в онлайн търсенето с ограничена дълбочина (долу).]"
- **Fix:** replace the alt text in `summaryBg.md`; the `](…_bg.png)` part stays.

### F06a-G02 · S1 · Fig. 24 DeepStack: text overlaps text everywhere; "ход" for turn; English "zero-sum"; prints at 5.3–6.6 pt
- **Where:** `renders/ch06/p083_f1.png` — caption "DeepStack architecture: offline intuition-building…"; script `deliverables/reports/step06/summary/make_deepstack_figure.py`.
- **Problem:**
  1. Illegible overlaps: the two panel titles run into each other ("…(преди игра)ОНЛАЙН: …"); "Текущо публично състояние" is printed on top of the first line of the neighbouring box ("Изграждане на разредено дърво за предвиждане с ограничена дълбочина", one 70-character line that spans both boxes); the CFV-network text runs over "Избира се действие, след това стратегията се изхвърля", which in turn runs over "Преизчисляване на CFR дървото за предвиждане"; "стойности на възли (граница на дълбочината)" and "връща се за следващото решение" are printed on top of each other and of the side box. The dashed net → re-solve arrow is hidden behind boxes D and "side" (EN too).
  2. Meaning: "флоп / ход / префлоп-спомагателни" — *turn* (the 4th card) as "ход" (a move; T01); "ОНЛАЙН: търсене с него" — "it" is the intuition (feminine): "с нея"; leaf → "възли" (T07); "Преизчисляване на CFR дървото" reads "recomputing the CFR tree".
  3. English/typography: "zero-sum глава", "1,000 клъстера", "(× пот)".
  4. Stale render: the PNG (1 Aug 13:08) predates the mapping (1 Aug 19:50) — it prints "ОФЛАЙН:", the mapping says "ИЗВЪН ЛИНИЯ:" (which T09 proposes to revert to "ОФЛАЙН").
  5. Legibility (scale 0.738): net box fs 7.6 → 5.6 pt; B box 7.3 → 5.4; side box 7.9 → 5.8; notes 7.2 → 5.3; other boxes 8.3–9 → 6.1–6.6; panel titles 10.5 → 7.7.
  6. Overflow (central fix): b1, b2, net, A/B, D, C, side — every box.
- **Fix:** `make_deepstack_figure.py` — switch to the two stacked panels that figs. 25–26 already use, so the net → re-solve link becomes a short vertical arrow and nothing crosses a box: `new_fig(w=15.8, h=10.4, xlim=(0, 16.2), ylim=(0.2, 11.0), shrink=2.0)`; offline panel `panel_bg(ax, 0.15, 7.3, 15.9, 3.5, …)` with `b1 = box(ax, 0.4, 7.7, 4.6, 2.3, …)`, `b2 = box(ax, 5.6, 7.7, 4.6, 2.3, …)`, `net = box(ax, 10.8, 7.6, 5.0, 2.6, …)` in a row; online panel `panel_bg(ax, 0.15, 0.4, 15.9, 6.6, …)` with `A = box(ax, 0.4, 3.9, 3.5, 1.9)`, `B = box(ax, 4.3, 3.9, 3.9, 1.9)`, `C = box(ax, 8.6, 3.9, 3.3, 1.9)`, `D = box(ax, 12.3, 3.9, 3.5, 1.9)`, `side = box(ax, 3.0, 0.8, 10.2, 2.2)`; arrows A→B→C→D (rc→lc), D → side top, side left → bc(A) (`rad=-0.3`), dashed `bc(net)` → `tc(C)`; delete the "loops back" note (the arrow says it) and put the leaf-values note at `note(ax, 15.9, 6.35, …, ha="right")` as two lines; all `box`/`note` fs → 10, `panel_bg(label_fs=11)`. At shrink 2.0 the canvas is 7.9 in and fs 10 prints at ≈ 8.2 pt. Verify in the re-render. Mapping (`figure_labels.json`): 'Deep counterfactual value…' → 'Дълбоки мрежи за\nконтрафактични стойности (CFV)\nфлоп / търн / префлоп (спомагателна)\n7×500 PReLU, изход с нулева сума\nвход: пот + диапазони (1000 клъстера)\nизход: CFV за всяка ръка (× пот)'; 'Build a sparse, depth-limited…' → 'Изграждане на разредено\nдърво за предвиждане\n(пас/плащане/2–3 размера/\nол-ин; до края на рунда)' (also drops the stray trailing `\n`); 'CFR re-solve\nthe look-ahead' → 'Пререшаване на\nдървото с CFR'; 'ONLINE: search with it (every decision)' → 'ОНЛАЙН: търсене с нея (при всяко решение)'; 'OFFLINE: learn intuition (before play)' → 'ОФЛАЙН: изграждане на интуицията (преди играта)'; 'leaf values (depth limit)' → 'стойности на листата\n(граница на дълбочината)'; 'Carries between decisions ONLY:…' → 'Между решенията се пренасят САМО:\nсобственият диапазон r₁ (обновен по Бейс след собствено действие)\n+ контрафактичните стойности на опонента v₂ (от пререшаването)'; 'Solve each with CFR+…' → 'Решаване на всяка с CFR+\n(без абстракция на картите) →\nцели = контрафактични стойности'.

### F06a-G03 · S1 · Fig. 25 Libratus: "Адаптация" for gadget (stale), "Обхват кръг 3", first person, notes on top of boxes, prints at 5.4–6.4 pt
- **Where:** `renders/ch06/p090_f1.png` — caption "Libratus's three-module pipeline…"; script `make_libratus_figure.py`.
- **Problem:**
  1. Meaning: the gadget box prints "Адаптация (в разширения корен)" — *gadget* as "adaptation", in the chapter about systems that refuse to adapt. The current mapping already says "Приспособление", so the render is stale. "Обхват кръг 3" — *Reach round 3* as "scope/range" (noun): "Достигане на кръг 3". "ясна/неясна" for *crisp/blurry* (the text says "подробна/груба").
  2. First person / imperative mix: "преизчислявам нова РАЗШИРЕНА под-игра" (T03-type), "Играй плана", "Избери k≈3 дупки" next to nouns "Решаване…", "Събиране…".
  3. Terminology inside one figure: "ДОПЪЛНЕНА под-игра" and "РАЗШИРЕНА под-игра" for the same augmented subgame (curated: разширена); "подигра" (no hyphen) vs "под-игра"; "кръг" vs the text's "рунд".
  4. English/typography: "55M→2.5M търн; 2.4B→1.25M ривър" (M/B, decimal points).
  5. Layout: the red note "обратна връзка: вграждане в план" is printed inside the "Действие" box; the dashed blueprint → gadget arrow crosses the "Решаване на ДОПЪЛНЕНА под-игра" box; "планът осигурява оценката на стойността" sits on the curved Act → m2 arrow.
  6. Legibility (scale 0.776): t1/m2/gadget fs 7.6 → 5.9 pt; notes 7.0–7.2 → 5.4–5.6; t2/t3 8.0 → 6.2; m1/m3/o1 8.3 → 6.4; panel titles 10.5 → 8.1.
  7. Overflow: t2, t3 (touches), m2, gadget, o1 (runs into o2), o2, o3.
- **Fix:** `make_libratus_figure.py`: `new_fig(..., shrink=2.0)`; all fs → 10, panel titles 11; `gadget = box(ax, 6.6, 4.4, 5.4, 1.9, …)` and the dashed arrow `arrow(ax, (12.02, t3[1]), (11.9, gadget[1] + gadget[3]), dashed=True, color="#8a6d1a")` (it then runs down the gap between m3 and m4); the value-estimate note → `note(ax, 14.2, 8.5, …)` (after shortening the online title, see mapping); the feedback note → one line at `note(ax, 15.9, 3.3, "обратна връзка: вграждане в плана", ha="right")` (the white gap between the online and overnight panels). Verify in the re-render. Mapping: 'Reach round 3 (or a small-\nenough subtree): …' → 'Достигане на кръг 3 (или на\nдостатъчно малко поддърво):\nпо-фина под-игра БЕЗ\nабстракция на картите'; 'Solve an AUGMENTED\nsubgame with CFR+' → 'Решаване на РАЗШИРЕНАТА\nпод-игра с CFR+'; 'opponent bets off-tree → re-solve…' → 'залог извън дървото → пререшава се нова РАЗШИРЕНА под-игра, която го съдържа (вложено);\nLibratus също променя собствените си размери на залозите с 0–8% при първото решаване'; 'Play the blueprint\non rounds 1–2' → 'Игра по плана\nв кръгове 1–2'; 'Pick k≈3 holes…' → 'Избор на k≈3 „дупки“\n(честота × разстояние до\nнай-близкото действие)'; 'Blueprint strategy — crisp on\nrounds 1–2, blurry on rounds 3–4…' → 'План — подробен за кръгове 1–2,\nгруб за кръгове 3–4 (късните числа\nсамо оценяват стойността\nна достигането до под-игра)'; 'Abstract the game: …' → '…(55 млн.→2,5 млн. за търна;\n2,4 млрд.→1,25 млн. за ривъра)…'; 'Collect opponents' most-used…' → 'Събиране на най-честите\nразмери на залози извън менюто'; 'ONLINE: nested safe subgame solving (every late decision)' → 'ОНЛАЙН: вложено безопасно решаване на под-игри'; 'OVERNIGHT: self-improver (between days)' → 'ПРЕЗ НОЩТА: самоусъвършенстване (между игралните дни)' (the current mapping value 'самоусъвършенстващ се' is an adjective without a noun, T15).

### F06a-G04 · S1 · Fig. 26 Pluribus: "финален" for fine, Latin "a", "множество" for set, "ВЪЗЕЛ" for LEAF, garbled chance-node note, prints at 5.4–6.9 pt
- **Where:** `renders/ch06/p099_f1.png` — caption "Pluribus's two-phase architecture…"; script `make_pluribus_figure.py`.
- **Problem:**
  1. Meaning: "финален кръг 1" — *fine round 1* read as "final"; "Текущо публично състояние → множество корен на под-игра" — *set* (verb) read as the noun "set"; "(възел на случайността върху убеждението за ръка разпределение)" does not parse; "При всеки ВЪЗЕЛ" — *LEAF* as "node" (T07), and "до стойността на възела"; "планът смесена към пас / залог / повишаване" — *biased* as "mixed", agreement error, and call → "залог" (F07-T02); printed "дългосрочни стратегии" (long-term) for continuation strategies (stale; mapping now 'продължителните', itself wrong, T06).
  2. English: "граница на дълбочината a кръг или два напред" — a Latin "a" (U+0061) left from "a round or two ahead" (mapping entry, not only the render); "Абстракция на играта 6-max".
  3. Grammar/typos (printed, stale): "поддиграда", "външно изваждкови MCCFR"; mapping still has "външно извадкови MCCFR" (plural adjective, calque), "линейно итерационно тегло", "модифицирано отрицателно-съжаление подрязване" (noun pile).
  4. Mood: "Действай при последната итерация" (imperative), "добави точно този залог и преизчислявам" (imperative + 1st person).
  5. Layout: the dashed blueprint → leaf arrow crosses the "Решаване в реално време…" box; the bottom third of the online panel is empty while the off-tree note is printed below the panel (EN too).
  6. Legibility (scale 0.770): p2 fs 7.0 → 5.4 pt; q1 7.3 → 5.6; q2 7.4 → 5.7; p1/p3/q3/q4 7.6–7.7 → 5.9; notes 7.0–7.4 → 5.4–5.7; q5 9.0 → 6.9; titles 10.5 → 8.1.
  7. Overflow: p1, p2, q1 (both edges), q2, q3.
- **Fix:** `make_pluribus_figure.py`: `new_fig(..., shrink=2.0)`, all fs → 10, titles 11; dashed arrow → `arrow(ax, (11.9, p3[1]), (11.9, q4[1] + q4[3]), dashed=True, color="#8a6d1a")` (down the gap between q3 and q5); its note → `note(ax, 12.1, 7.35, "планът е източникът\nна k=4 стратегии\nза продължение", ha="left")`; off-tree note → `note(ax, 8.1, 1.2, …)` inside the panel. Mapping: 'Abstract the 6-max game:…' → 'Абстракция на играта с шестима:\nдействия (1–14 размера на залога\nкато част от пота; подробна в кръг 1,\nгруба в кръгове 3–4) + информация\n(без загуби в кръг 1;\n~200 клъстера/кръг след това)'; 'Solve by Linear MCCFR:…' → 'Решаване с Linear MCCFR:\nMCCFR с външна извадка,\nлинейно претегляне на итерациите\n+ модифицирано подрязване\n(съжаление ≲ −3×10⁸ се пропуска в 95%\nот итерациите, освен в последния кръг)'; 'Current public state → set…' → 'Текущо публично състояние →\nкорен на под-играта в НАЧАЛОТО\nна текущия рунд (възел на\nслучайността над убежденията\nза картите)'; 'Solve in real time with\nLinear CFR (depth limit a\nround or two ahead)' → 'Решаване в реално време\nс Linear CFR (граница на\nдълбочината: кръг или два напред)'; 'At each LEAF: …' → 'Във всяко ЛИСТО всеки останал играч избира една от k=4\nстратегии за продължение - плана или плана, изместен към\nпас / плащане / повишаване - и остатъкът от раздаването се\nразиграва с избраните стратегии, за да се оцени листото'; 'Act on the\nfinal iterate' → 'Действие по\nпоследната итерация'; "any off-tree opponent bet → …" → 'залог на противника извън дървото → залогът се добавя\nи се пререшава от корена на текущия кръг'; 'blueprint is the source of\nthe k=4 continuation strategies' → as in the note above; 'Build a finer-grained subgame…' → 'По-фина под-игра (без загуби\nв текущия кръг; ~500 клъстера/\nкръг след това; 1–6 размера)'; 'OFFLINE: blueprint by self-play (one 64-core server, ~$150)' → 'ОФЛАЙН: план чрез самообучение (един 64-ядрен сървър, ~$150)'.

### F06a-G05 · S2 · Stale BG renders; the legibility floor for the central overflow fix
- **Where:** `deliverables/reports/step06/summary/{deepstack,libratus,pluribus}_arch_bg.png` (written 1 Aug 13:08) vs `scripts/figures/out/figure_labels.json` (1 Aug 19:50).
- **Problem:** The printed figures predate the mapping, which is why "Адаптация", "дългосрочни", "поддиграда", "изваждкови", "ОФЛАЙН" still print. All three figures are drawn with `_diagram_utils.new_fig(shrink=1.8)` at w = 15.5–15.8, i.e. an 8.6–8.8 in canvas squeezed to 16.2–16.7 cm, so one matplotlib point prints as 0.74–0.78 pt: 8.2 pt on paper needs fs ≥ 10.6–11.1 at the current size. Every label is 7.0–9.5. An auto-fit that shrinks text would make these figures worse.
- **Fix:** after the mapping fixes, re-run `python scripts/figures/render_bg_figures.py --only step06` and rebuild. In the central overflow fix, wrap or enlarge boxes, never shrink below the floor. For the step-06 figures the simplest lever is `shrink` 1.8 → 2.0 (canvas 7.9 in, fs 10 → ≈ 8.2 pt) plus fs 10; `note()`'s default fs 7.6 → 10 in `_diagram_utils.py` (as F07-G09).

## B — Bulgarian language

### F06a-B01 · S1 · English heading
- **Where:** summaryBg.md § Libratus — "### The gap it closed" (printed as "6.3.1 The gap it closed", p. 89; the SoG section has the same, F06b).
- **Now → Proposed:** "### The gap it closed" → "### Пропускът, който запълни" (same heading for all five systems, see F06a-X02)
- **Why:** English heading in the BG bundle, also in the PDF bookmarks.

### F06a-B02 · S1 · English left in text and tables
- **Where:** summaryBg.md §§ Въведение, DeepStack, Libratus, Pluribus; onePagerBg.md "Подход."
- **Now → Proposed:**
  - "със самообучение в стил **AlphaZero-style Self-Play**" → "със самообучение в стила на **AlphaZero**"
  - "линията минимакс / Monte-Carlo-tree-search / AlphaZero" → "линията минимакс / търсене в дърво по метода Монте Карло / AlphaZero"
  - "във вътрешния цикъл на **Recursive Belief-based Learning** и **Student of Games**" → "във вътрешния цикъл на **ReBeL** и **Student of Games**"
  - "което **Recursive Belief-based Learning** и **Student of Games** разрушават след това" → "което **ReBeL** и **Student of Games** разрушават след това"
  - onePagerBg: "**Recursive Belief-based Learning** (2020)" → "**ReBeL** (2020)"
  - "| Невронна компонента | Deep Counterfactual Value Networks (флоп, търн, спомагателни); само стойност |" → "| Невронен компонент | Дълбоки мрежи за контрафактични стойности (за флопа, търна и спомагателна); само стойности |"
  - "обучават **дълбоките контрафактични мрежи за стойности (CFV Network)**" → "обучават **дълбоките мрежи за контрафактични стойности (CFV мрежи)**"; "като използва CFV Network за изчисляване" → "като използва CFV мрежата за изчисляване"
  - "почти изцяло в CFR solving, използвано за етикетиране на мрежите за стойности" → "почти изцяло в решаването с CFR, чрез което се получават целевите стойности за мрежите"
  - "със **AlphaZero-style самообучение**" → "със **самообучение в стила на AlphaZero**"
  - "избира един играч като „traverser“" → "избира един играч за „обхождащ“ (traverser)"
  - "Libratus реши двуигровия No-Limit Холдем" → see F06a-B37
  - "| Тип игра | 6-max NLHE - шестпотребителски No-Limit Texas Холдем (непълна информация; многопотребителски, *не* двуигрови с нулева сума) |" → "| Тип игра | 6-max NLHE - безлимитен тексаски холдем с шестима играчи (непълна информация; с много играчи, *не* е игра за двама с нулева сума) |"
  - "широко смятан за най-добрия Six-Max Cash Player в момента" → see F06a-C03
  - "- същата теза за „**тест-тайм изчислителна мощност**“" → "- същата теза за „**изчисления по време на изпълнение**“ (test-time compute)"
- **Why:** English prose (and English in Cyrillic, "тест-тайм") in the BG bundle; all print (pp. 79–103). ReBeL is written "ReBeL" everywhere else in the chapter; the expanded English name appears only in these three places.

### F06a-B03 · S1 · English in formulas
- **Where:** summaryBg.md §§ DeepStack "Ключова иновация", Libratus "Ключова иновация", Pluribus "Ключова иновация" (pp. 85, 93, 101)
- **Now → Proposed:**
  - "$$ \text{exploitability} \;<\; k_1\,\epsilon \;+\; k_2/\sqrt{T}, $$" → "$$ \text{експлоатируемост} \;<\; k_1\,\epsilon \;+\; k_2/\sqrt{T}, $$"
  - "$$ \text{exploitability}(\sigma_{\text{refined}}) \;\le\; \text{exploitability}(\sigma^{*}) \;+\; 2\Delta. $$" → "$$ \text{експлоатируемост}(\sigma_{\text{усъв}}) \;\le\; \text{експлоатируемост}(\sigma^{*}) \;+\; 2\Delta. $$"
  - "(\text{no-regret})" → "(\text{без съжаление})"
- **Why:** English words print inside the displayed formulas. Cyrillic in `\text{}` needs a check in the first rebuild (as noted in F07-B08).

### F06a-B04 · S1 · System names mis-cased (pipeline artefact)
- **Where:** summaryBg.md lines 1–298: "deepStack" 31× (e.g. "Отвореният въпрос, който deepStack се опита да реши"), "alphaGo" 1×, "modicum" 2× ("двуигровия предшественик modicum", "В modicum само *противникът*"), "estimated-Maxmargin" 1× ("Компромисът на estimated-Maxmargin"), "gPUs" 1×; onePagerBg "**deepStack** (2017)".
- **Now → Proposed:** "deepStack" → "DeepStack"; "alphaGo" → "AlphaGo"; "modicum" → "Modicum"; "estimated-Maxmargin" → "Estimated-Maxmargin"; "gPUs" → see F06a-B28.
- **Why:** Proper names; the lower-case first letter appears only in BG, apparently where a name started a translated segment. A global replace of `deepStack` → `DeepStack` is safe (no other use).

### F06a-B05 · S1 · meaning — "звуково" for *sound*
- **Where:** summaryBg.md DeepStack table and § "Затворената празнина"
- **EN:** "the first *sound* heuristic search for imperfect-information games" / "whether heuristic search can be made *sound* under hidden information"
- **Now → Proposed:**
  - "първото *звуково* евристично търсене за игри с непълна информация" → "първото *коректно* евристично търсене за игри с непълна информация"
  - "може да бъде направено *звуково* при наличие на скрита информация" → "може да бъде направено *коректно* при наличие на скрита информация"
- **Why:** "звуков" means acoustic. The chapter elsewhere renders the same word as "коректен", "надежден", "разумно" (T08).

### F06a-B06 · S1 · meaning — the turn network as "мрежата от ходове"
- **Where:** summaryBg.md DeepStack table and § "Изчислителна мощност и достъпност"
- **EN:** "~175 CPU-core-years to label the turn network" / "the turn network alone consumed"
- **Now → Proposed:**
  - "~175 процесорно-ядрени години за етикетиране на мрежата от ходове" → "~175 процесорни ядро-години за генериране на целите на мрежата за търна"
  - "самата **мрежа от ходове** изразходва" → "само **мрежата за търна** изразходва"
- **Why:** *Turn* is the fourth community card ("търн", as the same table row above says); "мрежа от ходове" is "a network of moves" (T01).

### F06a-B07 · S1 · meaning — "ръчни клъстера" for *hand clusters*
- **Where:** summaryBg.md DeepStack § "Ключова иновация"
- **EN:** "the two ranges (compressed into 1,000 hand clusters)"
- **Now → Proposed:** "(компресирани в 1000 ръчни клъстера)" → "(компресирани в 1000 клъстера от ръце)"
- **Why:** "ръчни" means manual/hand-made (T02).

### F06a-B08 · S1 · meaning — who wins against LBR
- **Where:** summaryBg.md DeepStack § "Силни страни и ограничения"
- **EN:** "LBR … cannot find any way to beat it, itself losing by over 350 mbb/g"
- **Now → Proposed:** "не успява да намери начин да го победи, а самият той печели над 350 mbb/g" → "не успява да намери начин да го победи, а самото то губи от DeepStack над 350 mbb/g"
- **Why:** Read with LBR as the subject, the BG says the probe *wins* 350 mbb/g — the opposite of the paper ("LBR fails to exploit DeepStack at all — itself losing by over 350 mbb/g", arXiv:1701.01724v3).

### F06a-B09 · S1 · meaning — the Libratus opening contradicts the DeepStack section
- **Where:** summaryBg.md § Libratus, first paragraph
- **EN:** "it was never tested head-to-head against the strongest prior bots or against HUNL specialists in a long, rigorous match"
- **Now → Proposed:** "и никога не беше тестван в директен сблъсък срещу най-силните предварителни ботове или срещу човешки играчи в дълъг, строг мач" → "и никога не беше изпитан в директен двубой срещу най-силните по-ранни ботове или срещу специалисти по HUNL в дълъг и строго проведен мач"
- **Why:** "срещу човешки играчи" says DeepStack never played humans, which the preceding section refutes (33 professionals); the point is *specialists*. "предварителни ботове" means "preliminary bots".

### F06a-B10 · S1 · grammar — imperative and tense in the Libratus/DeepStack contrast
- **Where:** summaryBg.md § Libratus first paragraph; § Въведение
- **Now → Proposed:**
  - "запази парадигмата „абстракция и план“ и излекувай нейната единствена фатална болест" → "запази парадигмата „абстракция и план“ и излекува единствения ѝ фатален недостатък"
  - "докато **Libratus** я запазва и излекува единствения ѝ фатален недостатък" → "докато **Libratus** я запазва и лекува единствения ѝ фатален недостатък"
- **Why:** "излекувай" is an imperative; a bare perfective present ("запазва и излекува") cannot stand in a main clause.

### F06a-B11 · S1 · meaning — *prior* rendered as "предварително убеждение" (F07-T04)
- **Where:** summaryBg.md Libratus § "Ключова иновация"; DeepStack § "Затворената празнина"
- **EN:** "Both adjectives matter, and each fixes a specific prior failure." / "which in turn depends recursively on what they believe about your cards"
- **Now → Proposed:**
  - "и всяко от тях коригира конкретно **предварително убеждение** за неуспех" → "и всяко от тях отстранява конкретен недостатък на по-ранните методи"
  - "зависят рекурсивно от предварителните му убеждения относно вашите карти" → "зависят рекурсивно от това какво той предполага за вашите карти"
- **Why:** The first says "each corrects a specific prior belief about failure" — the glossary entry for the Bayesian *prior* pasted onto the adjective *prior* (earlier). The second adds a Bayesian "prior" the EN does not have.

### F06a-B12 · S1 · meaning — "възмущава" for *perturbs*
- **Where:** summaryBg.md Libratus § "Ключова иновация"
- **EN:** "it perturbs them by a random 0–8% at the first solve"
- **Now → Proposed:** "той ги възмущава със случайна стойност от 0–8% при първото решаване" → "той ги увеличава или намалява със случаен процент между 0 и 8% при първото решаване"
- **Why:** "възмущава" means "outrages/angers"; the physics sense ("смущение") is not what a reader hears. The proposal matches the paper's note 49 ("increased or decreased all its bet sizes by a percentage chosen uniformly at random between 0 and 8%").

### F06a-B13 · S1 · meaning — the Estimated-Maxmargin trade-off reversed
- **Where:** summaryBg.md Libratus § "Ограничения, задънени улици…"
- **EN:** "The **Estimated-Maxmargin** choice itself trades a little theoretical purity for strength"
- **Now → Proposed:** "сам по себе си жертва малко теоретична чистота за сметка на сила" → "сам по себе си жертва малко теоретична чистота в полза на силата"
- **Why:** "за сметка на" means "at the expense of" — the BG says strength is what is lost.

### F06a-B14 · S1 · meaning — endgame and subgame as "крайна игра", "подучастъци"; the gadget as "подпомагащият"
- **Where:** summaryBg.md Libratus §§ "Ключова иновация", "Наследство и съвременна значимост"
- **EN:** "once you reach an endgame" / "**safe subgame / endgame solving**" / "the **augmented-subgame gadget**" / "its safe-subgame-solving exploitability bound"
- **Now → Proposed:**
  - "В шаха, когато се достигне крайна игра" → "В шаха, когато се достигне ендшпил"
  - "**безопасно решаване на подучастъци / ендшпил**" → "**безопасно решаване на под-игри / на ендшпила**"
  - "**подпомагащият под-игра**" → "**помощната конструкция на разширената под-игра**"
  - "неговата граница на експлоатируемостта при безопасно решаване на подучастъци" → "неговата граница на експлоатируемостта при безопасно решаване на под-игри"
- **Why:** "подучастъци" are plots of land; "подпомагащият под-игра" is ungrammatical (masculine participle, feminine noun); "крайна игра" is a calque, the chess term is "ендшпил" (T11).

### F06a-B15 · S1 · meaning — "any" rendered as "every"
- **Where:** summaryBg.md Pluribus § "Силни страни и ограничения"
- **EN:** "the first AI to reach superhuman performance in any widely recognized benchmark game with more than two players or two teams"
- **Now → Proposed:** "който постига свръхчовешко представяне във всяка широко призната референтна игра" → "който постига свръхчовешко представяне в която и да е широко призната еталонна игра"
- **Why:** "във всяка" = "in every" such game — a claim no one makes. The table row already has the correct "в която и да е". Benchmark game → "еталонна игра" (curated).

### F06a-B16 · S1 · meaning — *six-handed* as "в шест ръце"; heads-up
- **Where:** summaryBg.md Pluribus § "Силни страни и ограничения"
- **EN:** "its 48-mbb/g six-handed win rate, though decisive, is not the same currency as Libratus's 147 heads-up"
- **Now → Proposed:** "И неговият процент победи от 48 mbb/g в шест ръце, макар и решителен, не е същата „валута“ като 147 на Libratus в един на един" → "И неговият темп на печалба от 48 mbb/g на маса с шестима, макар и решителен, не е в същата „валута“ като 147-те mbb/g на Libratus в игра един срещу един"
- **Why:** "в шест ръце" means "in six hands (deals)". Win rate: F06a-B20.

### F06a-B17 · S1 · meaning — *time-average* as "усреднено време"
- **Where:** summaryBg.md Pluribus § "Ограничения, неизследвани пътища…"
- **EN:** "Pluribus plays its **final** search iterate rather than the usual time-average"
- **Now → Proposed:** "Pluribus играе своята **последна** търсене итерация, вместо обичайното усреднено време" → "Pluribus играе стратегията от **последната** итерация на търсенето, а не обичайната усреднена по итерациите стратегия"
- **Why:** The BG says Pluribus plays "the averaged time". "последна търсене итерация" is an ungrammatical noun pile.

### F06a-B18 · S1 · grammar/meaning — "двуигров" for *two-player* (T03)
- **Where:** summaryBg.md §§ DeepStack, Pluribus (11 occurrences of "двуигров-")
- **Now → Proposed:**
  - "DeepStack е **само двуигрови игра с нулева сума**" → "DeepStack е приложим **само в игри за двама с нулева сума**"
  - "подход, който е обоснован в **двуигрови игра с нулева сума**" → "подход, който е обоснован в **игри за двама с нулева сума**"
  - "когато премахнете двуигровия патерица" → "когато махнете патерицата на игрите за двама"
  - "двуигровия предшественик modicum" → "предшественика за двама играчи Modicum" (same for "в двуигровия предшественик")
  - "**двуигровия покер с нулева сума**" → "**покера за двама с нулева сума**"; "за двуигрови мрежи за стойности" → "за мрежи за стойности в игри за двама"; "вече беше скъпа в двуигровия покер" → "вече беше скъпа в покера за двама"
- **Why:** "двуигров" reads "of two games". "DeepStack е … игра" makes DeepStack a game; "двуигрови игра" and "двуигровия патерица" break agreement.

### F06a-B19 · S1 · grammar — agreement and government errors
- **Where:** summaryBg.md throughout
- **Now → Proposed:**
  - "като всяка от тях прави другата осъществим" → "като всяка от тях прави другата осъществима"
  - "при държане на всяка възможна **раздаване**" → "за всяка възможна ръка"
  - "вместо консервативни **горна граница**" → "вместо консервативни **горни граници**"; "а не консервативни *горна граница*" → "а не консервативни *горни граници*"
  - "дисциплина, която, с **без човешки данни и без експертни познания**, поддържа резултата чист" → "дисциплина, която заедно с **липсата на човешки данни и експертни познания** запазва резултата чист"
  - "за един до осем седмици наведнъж" → "за периоди от една до осем седмици"
  - "Прочетено по този начин, главата е изследване" → "Прочетена по този начин, главата е изследване"
  - "всичко все още е табличен и ръчно абстрахиран" → "всичко все още е таблично и ръчно абстрахирано"
  - "като същевременно предлагат **абсолютно никаква гаранция за безопасност**" → "без да предлагат **абсолютно никаква гаранция за безопасност**"
  - "всеки играч, който възприеме такова, е *гарантирано, че няма да загуби* в очакване" → "на всеки играч, който възприеме такова равновесие, е *гарантирано, че няма да загуби* средно (по математическо очакване)"
  - "за тринадесет силни човека" → "за тринадесет силни играчи"
  - "но *прави* групиране на ръцете в 1000 клъстери" → "но *групира* ръцете в 1000 клъстера"; "клъстеризацията k-средни със 1000 клъстери" → "клъстеризацията по метода на k-средните с 1000 клъстера"
  - "с загуби в по-късните" → "със загуби в по-късните"
- **Why:** gender/number agreement ("осъществим", "възможна раздаване", "горна граница", "табличен"), "с без", missing negation ("предлагат никаква"), "в очакване" (= "awaiting"), count forms after numerals ("1000 клъстера", "седмици" feminine), "със" only before с/з.

### F06a-B20 · S1 · meaning — win rate as "процент победи" (T05)
- **Where:** summaryBg.md §§ DeepStack, Libratus, Pluribus (5 places)
- **Now → Proposed:**
  - "стандартната покер единица за процент победи" → "стандартната единица за темп на печалба в покера"
  - "(мили-големи блайнда на игра, единицата за процент победи от предишния раздел;" → see F06a-B40
  - "(mbb/g, мерната единица за процент победи от предишните раздели" → "(mbb/g, мерната единица за темп на печалба от предишните раздели"
  - "процентът победи едва се колебаеше" → "темпът на печалба почти не се колебаеше"
  - "И неговият процент победи от 48 mbb/g" → see F06a-B16
- **Why:** mbb/g is chips won per 1000 hands, not a percentage of wins; the one-pager already writes "темпа на печалба".

### F06a-B21 · S2 · terminology — *unsafe/safe* as "несигурно/сигурно"
- **Where:** summaryBg.md §§ Libratus, Pluribus: "**несигурно** решаване на под-игра", "*несигурни* решавания", "Това „несигурно“ търсене", "разчита на **несигурно** търсене", "*несигурното* търсене", "доказано *сигурно* спрямо него"; onePagerBg "в полза на несигурно търсене"
- **Now → Proposed:** "несигурн-" → "небезопасн-" (keeping the inflection); "може да бъде доказано *сигурно* спрямо него" → "може да бъде доказуемо *безопасно* спрямо него"
- **Why:** Safe/unsafe subgame solving is a defined pair; the chapter already uses "безопасно/небезопасно" in five other places ("*небезопасен* вариант", "едно небезопасно решаване"). "несигурно" reads "uncertain".

### F06a-B22 · S2 · terminology — continual re-solving / re-solve
- **Where:** summaryBg.md: "продължително пре-решаване" (heading, table, text), "Продължително пре-решаване + научени контрафактични стойности", "непрекъснатото пререшаване" (2×), "преизчисляването с ограничена дълбочина", "**преизчислява от нулата**", "**преизчисляване в реално време**", "преизчисляване при всяко решение"
- **Now → Proposed:** "продължително пре-решаване" → "непрекъснато пререшаване" (also in the heading "### Ключова иновация: продължително пре-решаване с научени контрафактични стойности" → "### Ключова иновация: непрекъснато пререшаване с научени контрафактични стойности"); "преизчисляването с ограничена дълбочина свива играта" → "пререшаването с ограничена дълбочина свива играта"; "**преизчислява от нулата**" → "**пререшава от нулата**"
- **Why:** "продължително" means long-lasting (*continual* = непрекъснато); one concept, one word, one spelling ("пре-решаване" vs "пререшаване"). "преизчисляване" (recomputation) blurs the defined operation.

### F06a-B23 · S2 · terminology — continuation strategies (T06)
- **Where:** summaryBg.md: "продължителните стратегии на **Pluribus**", heading "### Ключова иновация: търсене с ограничена дълбочина с продължителни стратегии", "продължителна стратегия" / "продължителни стратегии" (15 places), vs "стратегии за продължение" (table, 2 places)
- **Now → Proposed:** "продължителн- стратеги-" → "стратеги- за продължение" throughout; "конструкцията **продължителна стратегия (многозначна листова)**" → "конструкцията със **стратегии за продължение (листо с няколко стойности)**"; "приемането на *единствена* план-продължителна стратегия в листата" → "приемането на *една-единствена* стратегия за продължение (плана) в листата"
- **Why:** "продължителна стратегия" means a long-term strategy; the chapter's own table already uses "стратегии за продължение".

### F06a-B24 · S2 · terminology — *leaf* as "възел" (T07)
- **Where:** summaryBg.md: "оценител на възел съпоставя", "„стойност на възел“", "Възел в игра с непълна информация следователно няма", "стойност за възлите", "чрез даване на всеки възел малко меню"; onePagerBg "вместо да се изхвърля във възел"
- **Now → Proposed:** "възел/възлите" → "листо/листата" in these places (e.g. "Листо в игра с непълна информация следователно няма *една-единствена стойност*"; "вместо да се изхвърля в листото")
- **Why:** Every tree position is a node; the argument is specifically about *leaves* at the depth limit. The chapter uses "листа" correctly elsewhere ("стойностите на листата").

### F06a-B25 · S2 · terminology — action translation
- **Where:** summaryBg.md: "**абстракция плюс офлайн равновесие плюс превод**", "*преведете*", "стъпката на превода", "граници на превод", "стъпката на преобразуване на действие", "вместо преобразуване на действие" (table), "преобразуването на действие", "чрез превод на действие"; onePagerBg "превод на действие", "провалът на превода от Глава 4"
- **Now → Proposed:** "превод/преобразуване на действие" → "транслация на действия" (e.g. "**абстракция плюс офлайн равновесие плюс транслация**"; "чрез транслация на действия"; "провалът на транслацията от Глава 4")
- **Why:** The curated file makes "транслация на действия" the deliberate exception ("превод" collides with translation of text), and chapter 4 uses it; this chapter never does.

### F06a-B26 · S2 · terminology — augmented subgame and off-menu
- **Where:** summaryBg.md Libratus §§ "Ключова иновация", "Архитектура"
- **Now → Proposed:** "*допълнената под-игра*" → "*разширената под-игра*"; "Решаването на тази допълнена игра" → "Решаването на тази разширена игра"; "той изгражда допълнена под-игра" → "той изгражда разширена под-игра"; "за всяко последващо извънсписъчно действие" → "за всяко следващо действие извън менюто"; "нестандартни размери на залозите" / "всеки нестандартен залог" / "всеки следващ нестандартен залог" → "размери на залозите извън менюто" / "всеки залог извън менюто"
- **Why:** Curated: augmented subgame → разширена под-игра (the figure says "разширена" too). One term for *off-menu* ("извън менюто" is already used twice).

### F06a-B27 · S2 · terminology — *imperfect recall*
- **Where:** summaryBg.md Libratus § "Архитектура"
- **Now → Proposed:** "патология на абстракциите с непълно извличане" → "патология на абстракциите с непълна памет"
- **Why:** Curated: imperfect recall → непълна памет; the chapter uses that form in the next section. "непълно извличане" means incomplete extraction.

### F06a-B28 · S2 · terminology — core-hours and GPUs
- **Where:** summaryBg.md Libratus table, § "Изчислителна мощност и достъпност"; DeepStack §§ table, compute
- **Now → Proposed:**
  - "~25 милиона часа ядро на процесор" → "~25 милиона процесорни ядро-часа"; "**25 милиона часове ядро на процесор**" → "**25 милиона процесорни ядро-часа**"; "всеки час ядро е CFR или абстракция" → "всеки ядро-час е изразходван за CFR или абстракция"
  - "**Не е имало gPUs и обучение на невронна мрежа никъде**" → "**Не са използвани нито графични процесори (GPU), нито обучение на невронни мрежи**"
  - "процесорно-ядрени години" (3×) → "процесорни ядро-години"; "на едно GPU" / "едно стандартно GPU" / "на една GPU" → "на един GPU" (throughout)
- **Why:** Four forms for one unit; the Pluribus section already writes "ядро-часа". "gPUs" is English and mis-cased; GPU gender varies within the chapter.

### F06a-B29 · S2 · terminology — "извън линия" for *offline* (T09)
- **Where:** summaryBg.md 14× "извън линия" + "извънлинейното" 2×, alongside 8× "офлайн"; tables "План (офлайн)?" (DeepStack, Pluribus) vs "План (извън линия)?" (Libratus); onePagerBg "**извън линия**"
- **Now → Proposed:** "извън линия" → "офлайн" (adverb) / "предварително" where it reads better; "deepStack се разделя ясно на **извън линия** фаза за изграждане на интуиция и **онлайн** фаза за търсене с нея" → "DeepStack се разделя ясно на **офлайн** фаза, в която се изгражда интуицията, и **онлайн** фаза, в която с нея се търси"; "(което би довело до експлозия на извънлинейното решаване)" → "(което би раздуло предварителното офлайн решаване)"; "| План (извън линия)? |" → "| План (офлайн)? |"
- **Why:** "извън линия" is a word-for-word calque of *off-line* and cannot modify a noun ("извън линия фаза"); the chapter's own tables use "офлайн".

### F06a-B30 · S2 · terminology — *multiplayer / six-player* as "-потребителски" (T03)
- **Where:** summaryBg.md Pluribus section (10 places): "многопотребителския въпрос", "решаващ шестпотребителски марж", "шестпотребителски No-Limit", "Шестпотребителският покер", "в многопотребителския покер", "в шестпотребителската обстановка", "**многопотребителският успех дойде без никаква гаранция за безопасност**", "Свръхчовешка шестпотребителска игра", "в N-потребителски игри"
- **Now → Proposed:** "многопотребителск-" → "с много играчи" (e.g. "въпроса за игрите с много играчи", "в покера с много играчи", "**успехът в игра с много играчи дойде без никаква гаранция за безопасност**"); "шестпотребителск-" → "с шестима играчи" (e.g. "решаващ марж на маса с шестима", "Покерът с шестима играчи"); "в N-потребителски игри" → "в игри с N играчи"
- **Why:** "потребител" is a (software) user; multi-user is a computing term.

### F06a-B31 · S2 · terminology — *hand* (F07-B20)
- **Where:** summaryBg.md §§ DeepStack, Libratus, Pluribus
- **Now → Proposed:**
  - "(разпределението върху възможните раздавания, които може да държи)" → "(разпределението върху възможните ръце, които може да държи)"
  - "за всяко раздаване, което той може да държи" → "за всяка ръка, която той може да държи"; "скритите раздавания, които противникът може да държи тук" → "скритите ръце, които противникът може да държи тук"
  - "в 44,852 ръце" → "в 44,852 раздавания"; "в 120,000 ръце" (Libratus opening) / "147 mbb/g за 120,000 ръце" (2×) → "раздавания"; "в десетки хиляди ръце" (2×) → see F06a-C02; "симулира ръка" → "симулира раздаване"
- **Why:** One holds cards (ръка); one plays deals (раздавания). The chapter mixes both senses both ways.

### F06a-B32 · S2 · calque — *dissolve* as "разтварям"
- **Where:** summaryBg.md: "разтваряйки както абстракцията, така и плана", "разтворена до *без абстракция на карти*" (Libratus table), "Шестпотребителският покер разтваря всичко това.", "всички от които се разтварят чрез научените представяния", "които научените представяния на ReBeL и SoG разтварят"
- **Now → Proposed:** "разтваряйки както абстракцията, така и плана" → "премахвайки както абстракцията, така и плана"; "разтворена до *без абстракция на карти*" → "отпада изцяло (*без абстракция на картите*)"; "Шестпотребителският покер разтваря всичко това." → "Покерът с шестима играчи обезсмисля всичко това."; "всички от които се разтварят" → "всички те отпадат"; "разтварят" → "премахват"
- **Why:** "разтварям" is to dissolve in a liquid (or to open).

### F06a-B33 · S2 · calque — *signal strength*
- **Where:** summaryBg.md Libratus and Pluribus "Силни страни и ограничения"
- **Now → Proposed:** "Сигналната сила на Libratus е" → "Главното предимство на Libratus е"; "Силата на сигнала на Pluribus е просто в това" → "Главното предимство на Pluribus е просто в това"
- **Why:** "сила на сигнала" is radio signal strength (the EN idiom means "signature strength").

### F06a-B34 · S2 · calque — *field* and *frontier*
- **Where:** summaryBg.md Libratus and Pluribus "Наследство…", Pluribus "Изчислителна мощност…"
- **Now → Proposed:** "**високата граница на парадигма, която след това полето изостави**" → "**върхът на една парадигма, която областта след това изостави**"; "централна тема на границата на изкуствения интелект" → "централна тема за най-напредналите системи с изкуствен интелект"; "граничният игрови изкуствен интелект" → "най-напредналият игрови изкуствен интелект"
- **Why:** "полето" is a meadow/field of land; *high-water mark* is not a border; "граничен" means "border(line)".

### F06a-B35 · S2 · meaning — "представителна" for *representational*
- **Where:** summaryBg.md § Въведение — "Първата е **представителна**:"
- **Now → Proposed:** "Първата е **представителна**:" → "Първата ос е **на представянето**:"
- **Why:** "представителна" means representative (as in a delegation).

### F06a-B36 · S2 · calque — *decision points* as "решаващи точки" (T11)
- **Where:** summaryBg.md: "игра с приблизително $10^{160}$ решаващи точки", "свива играта от $10^{160}$ решаващи точки", "приблизително $10^{161}$ решаващи точки на HUNL"
- **Now → Proposed:** "решаващи точки" → "точки на решение"
- **Why:** "решаващи точки" = decisive points.

### F06a-B37 · S2 · meaning — "Libratus реши…" (*settled* as *solved*)
- **Where:** summaryBg.md § Pluribus, first sentence
- **EN:** "Libratus settled two-player no-limit hold'em"
- **Now → Proposed:** "Libratus реши двуигровия No-Limit Холдем" → "Libratus сложи точка на въпроса за безлимитния холдем за двама"
- **Why:** In this chapter "решавам игра" is the technical *solve* (compute an equilibrium), which Libratus did not do; also English "No-Limit" and "двуигров".

### F06a-B38 · S2 · calque — the intro's scorecard and axis sentences
- **Where:** summaryBg.md § Въведение
- **EN:** "A short per-system scorecard opens each section so the same nine dimensions line up at a glance" / "the offline-to-search axis" / "opponent-awareness" / "Chapters 1–5 assembled the parts in isolation … converge into complete … systems"
- **Now → Proposed:**
  - "Кратък отчет за всяка система открива всяка секция, така че същите девет измерения да се подреждат с един поглед" → "Всеки раздел започва с кратка обобщаваща таблица по едни и същи девет измерения, така че системите да се сравняват с един поглед"
  - "механизмът *чрез който* оста извън линия към търсене всъщност функционира" → "механизмът, *чрез който* всъщност действа оста „от офлайн изчисление към търсене в реално време“"
  - "именно съзнанието за противник, което тези системи пропускат" → "именно отчитането на конкретния противник, което тези системи пропускат"
  - "Глави 1–5 сглобяват отделните елементи" → "Глави 1–5 изграждат поотделно съставните елементи"
- **Why:** "отчет" is a (financial) report; "да се подреждат с един поглед" is a word-for-word *line up at a glance*; "оста извън линия към търсене" does not parse; "съзнание" is consciousness. The last item restores *in isolation* and removes the "сглобяват … сглобяват" repetition.

### F06a-B39 · S2 · terminology — "Изчислителна мощ(ност)" for *compute* (F07-T12)
- **Where:** summaryBg.md: 3 headings "### Изчислителна мощност и достъпност", 3 table rows "| Изчислителна мощ |", "*изчислителна мощност по време на игра*", "**изчислителната мощ почти отсъства от основната статия**", "Историята за изчислителната мощност на Pluribus", "изчислителната мощност за обучение на Libratus", "изразходвайте изчислителна мощност"
- **Now → Proposed:** headings → "### Изчислителни разходи и достъпност"; rows → "| Изчислителни разходи |"; "**изчислителната мощ почти отсъства от основната статия**" → "**данните за изчислителните разходи почти липсват в основната статия**"; others "изчислителна мощност" → "изчисления/изчислителни разходи"
- **Why:** The meaning is cost, not hardware power (F07-T12). Also "| Изчислителна мощ | Прочуто евтин:" breaks agreement → "| Изчислителни разходи | Забележително ниски:".

### F06a-B40 · S2 · mbb/g spelled out three times, defined by itself
- **Where:** summaryBg.md § Libratus first paragraph and "The gap it closed"
- **EN:** "147 mbb/g (milli-big-blinds per game, the win-rate unit from the previous section; ~50 mbb/g is a sizable professional edge)"
- **Now → Proposed:**
  - "с 147 мили-големи блайнда на игра (мили-големи блайнда на игра, единицата за процент победи от предишния раздел; ~50 мили-големи блайнда на игра е значително професионално предимство)" → "със 147 mbb/g (мили-големи блайнда на игра, единицата за темп на печалба от предишния раздел; ~50 mbb/g е значително професионално предимство)"
  - "губят хиляди мили-големи блайнда на игра" → "губят хиляди mbb/g"; "с 91 мили-големи блайнда на игра" → "с 91 mbb/g"
- **Why:** The abbreviation was expanded everywhere, so the gloss defines the term by itself.

### F06a-B41 · S2 · meaning — "настойчив", "демонтира"
- **Where:** summaryBg.md § Libratus first paragraph
- **EN:** "and *forceful*, for its play" / "it first dismantled the prior best poker AI head-to-head"
- **Now → Proposed:** "и *настойчив*, за своята игра" → "и *силен*, заради мощната си игра"; "първо демонтира предишния най-добър изкуствен интелект за покер в директен сблъсък" → "първо победи убедително в директен двубой най-добрия дотогава изкуствен интелект за покер"
- **Why:** The paper glosses the name as "forceful (for its powerful play style and strength)"; "настойчив" is persistent. "демонтира" is dismantling machinery.

### F06a-B42 · S2 · calque — *bookkeeping*
- **Where:** summaryBg.md DeepStack § "Ключова иновация"
- **Now → Proposed:** "Това, което прави това възможно, е воденето на отчетност." → "Всичко това е възможно благодарение на начина, по който се поддържат двата вектора."
- **Why:** "водене на отчетност" is accounting/reporting to someone.

### F06a-B43 · S2 · terminology — *feed-forward*, *units*, *layer*
- **Where:** summaryBg.md DeepStack § "Ключова иновация"
- **Now → Proposed:** "с директна мрежа от седем скрити слоя с по 500 единици" → "с мрежа с право разпространение от седем скрити слоя с по 500 неврона"; "Специално външно ниво налага ограничението с нулева сума" → "Специален външен слой налага ограничението за нулева сума"; "и цялото нещо да остане диференцируемо" → "а цялата мрежа да остане диференцируема"
- **Why:** "директна мрежа" is not a term; *layer* is "слой" in the same sentence; "цялото нещо" is colloquial.

### F06a-B44 · S2 · calques — warm start, solvers, well-resourced
- **Where:** summaryBg.md DeepStack §§ "Ограничения…", "Изчислителна мощност…"
- **Now → Proposed:** "тя също така прави **топли стартове** на диапазона на опонента" → "той също така започва от **предварителна оценка** на диапазона на опонента (warm start)"; "с по-бързи модерни решаващи устройства" → "с по-бързи съвременни програми за решаване"; "добре ресурсирана лаборатория" → "добре осигурена лаборатория"
- **Why:** "решаващи устройства" are hardware devices (the meaning is software solvers); "топли стартове", "ресурсирана" are anglicisms (cf. F07-B16).

### F06a-B45 · S2 · noun piles
- **Where:** summaryBg.md Pluribus § "Ключова иновация"
- **Now → Proposed:** "*безсъжаление играта се сближава до равновесие на Наш" → "*играта без съжаление (no-regret) се сближава към равновесие на Наш"; "от безсъжаление до безопасност" → "от липсата на съжаление до безопасност"; "**модифицирано отрицателно-съжаление подрязване**" → "**модифицирано подрязване на действията с отрицателно съжаление**"
- **Why:** English-style attributive nouns do not work in Bulgarian.

### F06a-B46 · S2 · meaning — *ablated* as "премахвани"
- **Where:** summaryBg.md Pluribus § "Ограничения, неизследвани пътища…"
- **EN:** "Pluribus's headline innovations are **never individually ablated**"
- **Now → Proposed:** "**никога не са индивидуално премахвани**" → "**никога не са оценени поотделно (чрез аблация)**"
- **Why:** The BG says the innovations were never removed; the point is that their individual effect was never measured.

### F06a-B47 · S2 · meaning — whose blueprint
- **Where:** summaryBg.md Pluribus § "Ограничения, неизследвани пътища…"
- **EN:** "on the *first* betting round, opponent bets too far off the blueprint's menu are still **rounded** by action translation"
- **Now → Proposed:** "твърде отдалечени от плана на опонента действия все още се **закръглят** чрез превод на действие" → "залозите на опонента, които се отклоняват твърде много от менюто на плана, все още се **закръглят** чрез транслация на действия"
- **Why:** The BG says "actions too far from the opponent's plan"; the blueprint is Pluribus's own.

### F06a-B48 · S2 · poker terms — call, raise, donk, limp (F07-T02)
- **Where:** summaryBg.md DeepStack § "Ограничения…"; Pluribus §§ "Ключова иновация", "Ограничения…"
- **Now → Proposed:** "(пас, залог, два или три размера на залога, ол-ин)" → "(пас, плащане, два или три размера на залога, ол-ин)"; "за *пас*, за *колл* и за *рейз*" → "за *пас*, за *плащане* и за *повишаване*"; "той се научи да **изоставя „лимпинга“** по време на самообучението, но **„донкове“ много повече от хората**" → "по време на самообучението той се научи да **избягва влизането само с плащане на блайнда („лимпинг“)**, но **залага „донк“ (с изпреварващ залог) много по-често от хората**"
- **Why:** *call* as "залог" (F07-T02) makes it identical to *bet*; "колл/рейз" are slang the chapter does not use elsewhere; "донкове" is not a Bulgarian verb.

### F06a-B49 · S2 · meaning — "Запознатите", "разумно"
- **Where:** summaryBg.md Pluribus § "Архитектура"
- **Now → Proposed:** "Запознатите градивни елементи са всички налице" → "Познатите градивни елементи са налице"; "Две съставки правят ранното спиране разумно" → "Две съставки правят ранното спиране коректно"
- **Why:** "запознат" means acquainted (with someone); *sound* is "коректно" (T08), "разумно" = reasonable.

### F06a-B50 · S2 · meaning — "гаранция за експлоатируемост"
- **Where:** summaryBg.md Pluribus § "Ключова иновация"
- **EN:** "because, unlike Libratus's, it carries no exploitability guarantee"
- **Now → Proposed:** "не носи гаранция за **експлоатируемост**" → "не дава гаранция, която да ограничава **експлоатируемостта**"
- **Why:** The BG literally says it gives no guarantee *of being exploitable*.

### F06a-B51 · S2 · meaning — *thesis*, *safe exploitation*, opponent terms
- **Where:** summaryBg.md DeepStack and Libratus "Наследство и съвременна значимост"
- **Now → Proposed:** "анализ на безопасното използване (**принос 2**)" → "анализ на безопасната експлоатация (**принос 2**)"; "За тази теза конкретно Libratus допринася с две основи" → "За настоящата дисертация Libratus дава две основи"; "вместо да експлоатира съперника" / "не моделирайте съперника" / "**адаптация към съперника**" → "противника"
- **Why:** "използване" is not the defined term (curated: exploitation → експлоатация); *thesis* = the dissertation, not "теза" (F07-B23); the chapter otherwise uses "противник/опонент", "съперник" appears only here.

### F06a-B52 · S2 · meaning — the thousandfold comparison
- **Where:** summaryBg.md Pluribus opening and § "Изчислителна мощност…"
- **Now → Proposed:** "с порядък хиляда по-малко от това, което свръхкомпютърът зад Libratus консумираше" → "с около хиляда пъти по-малко изчисления, отколкото изразходва свръхкомпютърът на Libratus"; "за порядък от хилядна част от изчислителната мощност за обучение на Libratus" → "за около една хилядна от изчисленията за обучение на Libratus"; "Сривът не е магия, а алгоритмичен" → "Рязкото поевтиняване не е магия, а резултат от алгоритмите"
- **Why:** "порядък хиляда" / "порядък от хилядна част" do not parse; "срив" (crash) suggests failure.

### F06a-B53 · S2 · calque — "персонализирани", "таблица за търсене"
- **Where:** summaryBg.md Pluribus §§ "Изчислителна мощност…", "Силни страни…"
- **Now → Proposed:** "Deep Blue 480 персонализирани чипа" → "Deep Blue - 480 специално проектирани чипа"; "планът е гигантска таблица за търсене, а не модел" → "планът е гигантска справочна таблица, а не модел"
- **Why:** *custom-designed* ≠ personalised; *lookup table* as "таблица за търсене" collides with "търсене" (*search*), the chapter's key term (T11).

### F06a-B54 · S2 · grammar — the self-improver as a bare adjective (T15)
- **Where:** summaryBg.md Libratus §§ "Архитектура", "Наследство…"; Pluribus § "Архитектура"
- **Now → Proposed:** "**Модул 3 - самоусъвършенстващият се (през нощта).**" → "**Модул 3 - модулът за самоусъвършенстване (през нощта).**"; "Самоусъвършенстващият се стеснява този остатък между дните" → "Модулът за самоусъвършенстване стеснява тази остатъчна слабост между игралните дни"; "моделът на **самоусъвършенстващ се**" → "моделът на **самоусъвършенстването**"; "няма **самоусъвършенстващ се**" → "няма **модул за самоусъвършенстване**"
- **Why:** An adjective with no noun; "Самоусъвършенстващият се стеснява" reads "the self-improving one gets shy (се стеснява = is embarrassed)".

### F06a-B55 · S2 · grammar — the systems change gender
- **Where:** summaryBg.md: DeepStack is "тя" ("тя победи група от 33", "тя също така прави"), "то" ("то *никога* не съхранява", "то заменя"), "той" ("Той **не изисква", "Той запазва"); Pluribus is "тя" ("а както тя, така и Libratus", "тя цели единствено", "нейните алгоритми") and "той" elsewhere; "**заменена като внедрена архитектура, но оправдана и изострена като теза**" (Pluribus)
- **Now → Proposed:** one gender per system — masculine, agreeing with "бот/алгоритъм", as most of the text already does (e.g. "то *никога* не съхранява" → "той *никога* не съхранява"; "тя цели единствено" → "той цели единствено"; "**заменен като внедрена архитектура, но оправдан и изострен като теза**")
- **Why:** The same subject switches between три рода within a paragraph.

### F06a-B56 · S2 · names in Cyrillic; the match name
- **Where:** summaryBg.md Pluribus §§ "Ключова иновация", "Наследство…"; Libratus "The gap it closed"
- **Now → Proposed:** "а Браун и Сандхолм илюстрират провала" → "а Brown и Sandholm илюстрират провала"; "Ноам Браун оттогава посочи" → "Noam Brown оттогава посочи"; "загуби първия мач *Мозъци срещу ИИ*" → "загуби първия мач *Brains vs. AI*"
- **Why:** Rule 6: author surnames stay in Latin script (the chapter writes "Brown & Sandholm", "Noam Brown" elsewhere); an event's proper name is not translated (rule 7 by analogy).

### F06a-B57 · S2 · calques in the DeepStack section
- **Where:** summaryBg.md DeepStack §§ "Затворената празнина", "Наследство…", table
- **Now → Proposed:**
  - "Компресията е загубна и загубата се проявява като експлоатируемост - колко може да спечели опонент в най-лошия случай, качественият показател на областта" → "Компресията е със загуби и загубата се проявява като експлоатируемост - колко може да спечели опонент в най-лошия случай, основният показател за качество в областта"
  - "*осъзнато убеждение* търсене" → "търсене, *отчитащо убежденията*"
  - "**диференцируемата глава за изходна нулева сума** за двуигрови мрежи за стойности" → "**диференцируемият изходен слой, който налага условието за нулева сума** в мрежите за стойности за двама играчи"
  - "| Абстракция? | Няма ограничения в играта; 1000-клъстерна клъстеризация само на входа на мрежата," → "| Абстракция? | Никаква абстракция не ограничава играта; групиране в 1000 клъстера само на входа на мрежата,"
  - "| Тип игра | HUNL - хедс-ъп безлимит тексаски но-лимит покер за двама (двуиграчева игра с нулева сума) |" → "| Тип игра | HUNL - безлимитен тексаски холдем за двама (игра за двама с нулева сума) |"
- **Why:** Curated: lossy → "със загуби", not "загубна"; "качествен" = qualitative; "Няма ограничения в играта" says the game has no restrictions; "безлимит … но-лимит" says *no-limit* twice (T16).

### F06a-B58 · S2 · "абстрактно-базиран" for *abstraction-based*
- **Where:** summaryBg.md: "абстрактно-базираната програма Claudico", "в абстрактно-базирания покер", "Той остава **абстрактно-базиран**", "**изцяло табличен и абстрактно-базиран**", "най-силните абстрактни ботове", "абстракционните ботове"
- **Now → Proposed:** → "основаната на абстракция програма Claudico", "в покера, основан на абстракция", "**основан на абстракция**", "ботовете, основани на абстракция"
- **Why:** "абстрактен" means abstract (not concrete); the meaning is "built on game abstraction".

### F06a-B59 · S2 · terminology — *extensive form*, *heads-up*
- **Where:** summaryBg.md § Въведение; DeepStack opening
- **Now → Proposed:** "игровотеоретичния речник на игрите в разширена форма" → "игровотеоретичния речник на игрите в разгърната форма"; "в хедс-ъп безлимит покер (HUNL)" → "в безлимитния тексаски холдем за двама (HUNL)"
- **Why:** Curated: extensive-form game → игра в разгърната форма; heads-up no-limit → T16.

### F06a-B60 · S3 · typography — straight quotes
- **Where:** summaryBg.md Libratus § "Ключова иновация" — '"Вложено" е втората половина.'
- **Now → Proposed:** '"Вложено" е втората половина.' → "„Вложено“ е втората половина."

### F06a-B61 · S1 · one-pager — meaning errors
- **Where:** onePagerBg.md "Ключови резултати", "Отворени въпроси"
- **EN:** "opponent-blindness itself" / "real-time compute budgets, whose six-order-of-magnitude spread" / "Corollary: build on the cheap, open lineage — the flagship code is unreleased or supercomputer-scale." / "its authors' "price of generality""
- **Now → Proposed:**
  - "самата **невидимост за противника** (Глава 7)" → "самата **независимост от противника** (Глава 7)"
  - "чието шест-редово разпределение най-силно ограничава агент" → "чийто разброс от шест порядъка най-силно ограничава агент"
  - "Следствие: изграждане на евтино, с отворен произход - водещият код е непубликуван или със **свръхкомпютърен мащаб**." → "Следствие: надграждането трябва да е върху евтините системи с отворен код - кодът на водещите системи не е публикуван или изисква **свръхкомпютър**."
  - "„цената на общността“, според авторите му" → "„цената на универсалността“, по думите на авторите"
- **Why:** "невидимост за противника" = being invisible to the opponent (inverted; T04); "шест-редово" = six-row; the corollary does not parse; "общност" out of the fixed phrase "без загуба на общност" reads "community".

### F06a-B62 · S2 · one-pager — calques and terminology
- **Where:** onePagerBg.md
- **Now → Proposed:**
  - "неврално приближение на стойност" → "невронно приближение на стойностите"
  - "от игра с непълна информация само до унифицирана игра" → "от игри само с непълна информация към единен алгоритъм за двата вида игри"
  - "тя изчислява най-лошосценарийна устойчива стратегия" → "тя изчислява стратегия, устойчива в най-лошия случай,"
  - "**безопасна експлоатация** извън **двуигрова игра с нулева сума**, която Pluribus спечели без и Student of Games не можа да разшири" → "**безопасна експлоатация** извън **игрите за двама с нулева сума** - Pluribus спечели без нея, а Student of Games не успя да я разшири"
  - "**Общодостъпното състояние на вярванията** на ReBeL" → "**Публичното състояние на убежденията** (public belief state) на ReBeL" (T18; coordinate with F06b)
  - "*Търсенето при извод, а не предварителната стратегия, носи предимството.*" → "*Предимството идва от търсенето по време на игра, а не от предварителната стратегия.*"
  - "в полза на несигурно търсене" → "в полза на небезопасно търсене"; "ReBeL възстанови двуигровата гаранция" → "ReBeL възстанови гаранцията за игри за двама"; "**извън линия**" → "**офлайн**"; "**147 mbb/g за 120,000 ръце**" → "**147 mbb/g за 120,000 раздавания**"
- **Why:** "неврален" is anatomical; "която Pluribus спечели без" is a dangling preposition; the other items are the chapter-wide fixes above.

### F06a-B63 · S3 · chapter title "от край до край"
- **Where:** summaryBg.md "# Глава 6 - Архитектури на игрови изкуствен интелект от край до край"; onePagerBg "# Глава 6 Резюме - Архитектури на игрови ИИ от край до край"
- **Now → Proposed:** "# Глава 6 - Архитектури на игрови изкуствен интелект от край до край" → "# Глава 6 - Цялостни архитектури на игрови изкуствен интелект"; one-pager "# Глава 6 Резюме - Архитектури на игрови ИИ от край до край" → "# Глава 6 Резюме - Цялостни архитектури на игрови изкуствен интелект"
- **Why:** "от край до край" is the fixed calque of *end-to-end encryption*; for a system that is complete from offline training to play, "цялостни" is the natural word (optional). The one-pager also abbreviates "ИИ" where the chapter writes it out.

(The candidate's two TOC comments for this chapter were checked: "нека да запазим оригиналното име на Libratus" (marked "Либратус (") is **applied** — no "Либратус" remains in the chapter or one-pager; "решаване на под игри" (marked "- под-игра джаджи (") was on TOC p. 7, i.e. a chapter-8 heading, and is **applied** there ("## Безопасност в реално време - решаване на под-игри (SES)"); chapter 6 renders *gadget* as "приспособление", except the stale figure label "Адаптация", F06a-G03.)

## T — Glossary-level terminology

### F06a-T01 · S1 · "turn → ход", "river → река"
- **Where:** `llmPipeline/glossary_settled.md` ("| turn | ход | 2 |", "| river | река | 4 |", "| river abstraction | речна абстракция | 1 |"); printed in ch. 6 as "мрежата от ходове" (F06a-B06), "флоп / ход / префлоп" (fig. 24), "флоп, търн, река" (Pluribus § Архитектура)
- **Now → Proposed:** turn (poker street) → "търн"; river → "ривър"; river abstraction → "абстракция на ривъра"
- **Why:** The fourth and fifth community cards; the chapter uses "търн/ривър" everywhere else. As entries they will misfire in any poker chapter.

### F06a-T02 · S1 · "hand clusters → ръчни клъстера", "hand features → ръчно изведени признаци"
- **Now → Proposed:** hand clusters → "клъстери от ръце"; hand features → check the source sentence: if poker-hand features, "признаци на ръката"; if hand-crafted, keep but re-key as "hand-crafted features"
- **Why:** "ръчен" = manual (F06a-B07).

### F06a-T03 · S1 · player-count adjectives
- **Where:** glossary_settled.md: "two-player → двуигрови", "n-player → n-играчeн" (contains a **Latin "e"**, U+0065), "N-player settings → N-игрова среда", "N-player bound → N-играторска граница", "multiplayer → многопотребителски", "multiplayer symmetric games → многоигрални симетрични игри", "multiplayer safety → безопасност в мултиплейър среда", "multiplayer adaptation → адаптация за многоиграчова среда"
- **Now → Proposed:** two-player → "за двама играчи" (adj. "с двама играчи"); N-player → "с N играчи"; multiplayer → "с много играчи"; six-player → "с шестима играчи"
- **Why:** Seven different stems for one idea; "двуигров"/"N-игров" mean "of two/N games", "-потребителски" means multi-user, "мултиплейър" is slang. Fix the mixed-script entry in the picker.

### F06a-T04 · S1 · "opponent-blindness → невидимост за противника"
- **Now → Proposed:** → "независимост от противника" (matching the settled adjective "opponent-blind → независим от противника")
- **Why:** The entry says the reverse (being invisible to the opponent); printed in onePagerBg (F06a-B61).

### F06a-T05 · S2 · "win rate / win-rate → процент победи" (also "hero win-rate → процент победи на героя")
- **Now → Proposed:** → "темп на печалба" (for mbb/g, bb/100); keep "процент победи" only for a genuine share of games won
- **Why:** In poker the win rate is chips per hand, not a percentage (F06a-B20). 12 settled occurrences.

### F06a-T06 · S2 · "continuation strategy → продължителна стратегия" (freq 9 + 1)
- **Now → Proposed:** → "стратегия за продължение"
- **Why:** "продължителен" = long-lasting (F06a-B23); the same stem gives "продължително пре-решаване" (continual re-solving → "непрекъснато пререшаване", settled freq 10).

### F06a-T07 · S2 · "leaf value → стойност на възел"
- **Now → Proposed:** → "стойност на листо"
- **Why:** leaf ≠ node (F06a-B24).

### F06a-T08 · S2 · sound / soundness split three ways
- **Where:** "sound algorithm → надежден алгоритъм", "sound self-play → правилно самообучение", "soundness → коректност" (+ 5 compounds with "коректност"), "generality with soundness → обобщеност с коректност"
- **Now → Proposed:** sound → "коректен" throughout ("коректен алгоритъм", "коректно самообучение")
- **Why:** In ch. 6 the one word appears as "звуково", "надежден", "коректен", "разумно".

### F06a-T09 · S2 · offline/online entries
- **Where:** "offline → извън линия", "offline phase → офлайн фаза", "offline cost → предварителна цена", "offline strategy → предварителна стратегия"
- **Now → Proposed:** offline → "офлайн" (or "предварително" as an adverb); offline cost → "предварителни изчислителни разходи"
- **Why:** "извън линия" is a calque that cannot modify a noun (F06a-B29); the settled entries already disagree with each other.

### F06a-T10 · S2 · "inference → извод", "test-time → време на тестване", "reasoning models → Модели с възможност за мислене"
- **Now → Proposed:** inference (running a trained model / acting) → "по време на изпълнение" (in games: "по време на игра"); test-time compute → "изчисления по време на изпълнение (test-time compute)"; reasoning models → "модели за разсъждение"
- **Why:** "извод" is a logical conclusion or statistical inference; "търсене при извод" and "тест-тайм" do not read (F06a-B02, B62).

### F06a-T11 · S2 · "decision points → решаващи точки", "endgame → крайна игра", "lookup table → таблица за търсене"
- **Now → Proposed:** → "точки на решение"; → "ендшпил" (chess) / "крайна фаза на играта"; → "справочна таблица"
- **Why:** F06a-B36, B14, B53.

### F06a-T12 · S2 · counterfactual: curated vs settled disagree
- **Where:** `deliverables/terminology_EN_BG.md` "Counterfactual value → Контрафактуална стойност" and the CFR gloss "…контрафактуалното съжаление"; settled "counterfactual value → контрафактична стойност" (freq 20). The summaries use "контрафактичн-" 42× and "контрафактуал-" 2× (both in ch. 6: "вектора на контрафактуални стойности на опонента", "векторът на контрафактуалните стойности на опонента").
- **Now → Proposed:** make "контрафактичен" the curated form (the corpus has already chosen it) and change the two ch. 6 occurrences.
- **Why:** The curated file is the authority but is out of line with the whole corpus.

### F06a-T13 · S2 · blueprint: curated "Схема" vs settled "план"
- **Where:** curated "Blueprint (strategy) → Схема (на стратегията)"; settled "blueprint → план" (freq 15), "tabular blueprint → таблична схема", "blueprint strategy → план-стратегия", "blueprint architecture → архитектурен план" (a meaning error: that is an architectural plan). Chapters 4, 6 and 8 use "план" (15/93/19 occurrences); ch. 6 also has "таблична схема" 2× ("грешката на оценката на таблична схема", "много-петабайтовата **таблична схема**").
- **Now → Proposed:** curated → "План (blueprint) – предварително изчислената стратегия за цялата игра", with the gloss on first use in each chapter; "tabular blueprint" → "табличен план"; drop "blueprint architecture → архитектурен план".
- **Why:** One object, two names in one chapter.

### F06a-T14 · S2 · value-network entries
- **Where:** "deep counterfactual value networks → Deep Counterfactual Value Networks", "learned counterfactual value network → научена контрафактична стойност мрежа", "feed-forward network → мрежа с директно разпространение"
- **Now → Proposed:** → "дълбоки мрежи за контрафактични стойности"; → "научена мрежа за контрафактични стойности"; → "мрежа с право разпространение"
- **Why:** An English entry and an ungrammatical one, both printed (F06a-B02, and "Втората идея е **научена контрафактична стойност мрежа**" in DeepStack § Ключова иновация → "Втората идея е **научената мрежа за контрафактични стойности**").

### F06a-T15 · S2 · "self-improver → самоусъвършенстващ се"
- **Now → Proposed:** → "модул за самоусъвършенстване" (already the entry for "self-improver module")
- **Why:** An adjective without a noun (F06a-B54).

### F06a-T16 · S2 · heads-up no-limit entries (five variants)
- **Where:** "heads-up no-limit Texas hold'em → Тексаски но-лимит покер за двама", "heads-up no-limit → хедс-ъп безлимит покер", "heads-up no-limit hold'em → Heads-Up No-Limit Холдем", "heads-up no-limit poker AI → изкуствен интелект за по̀кер без лимит един на един", "six-max → Six-Max"
- **Now → Proposed:** HUNL → "безлимитен тексаски холдем за двама (HUNL)"; six-max → "маса с шестима (6-max)"; curated "No-limit → Безлимитен" already says so
- **Why:** English, a transliteration ("но-лимит") and a stress mark (по̀кер) in one family; produced "хедс-ъп безлимит тексаски но-лимит покер" (F06a-B57).

### F06a-T17 · S3 · "local-best-response probe → сондаж за най-добър локален отговор"; "no-regret → безсъжаление"; "frontier game-AI → граничен изкуствен интелект в игрите"
- **Now → Proposed:** → "проверка с локален най-добър отговор (LBR)"; → "без съжаление (no-regret)"; → "най-напредналият игрови изкуствен интелект"
- **Why:** "сондаж" is an opinion poll or a borehole; "безсъжаление" is not a word; "граничен" = borderline.

### F06a-T18 · S2 · "public belief state → общодостъпно състояние на вярванията" vs "belief state → състояние на убеждението"
- **Now → Proposed:** → "публично състояние на убежденията"
- **Why:** "общодостъпно" means publicly accessible; the chapter says "публично състояние" for *public state*, and "вярвания" vs "убеждение" split one concept. Mostly ReBeL (coordinate with F06b); printed in the one-pager (F06a-B62).

## C — Content

### F06a-C01 · S1 · One-pager inverts the Go result
- **Where:** onePager.md "while sitting **over 1,100 Elo** below Go specialists"; onePagerBg.md "докато остана **над 1100 Elo** под специалистите по Го"
- **Problem:** The chapter (summaryEn l. 1268–1270) says Student of Games won 2 of 400 games against AlphaZero while "crushing the classical program Pachi by over 1,100 Elo". 1,100 Elo is SoG's margin **above** Pachi, not below the specialists.
- **Now → Proposed:** EN "while sitting **over 1,100 Elo** below Go specialists" → "while winning only **2 of 400** Go games against AlphaZero"; BG "докато остана **над 1100 Elo** под специалистите по Го" → "докато в Го спечели само **2 от 400** партии срещу AlphaZero"

### F06a-C02 · S2 · Pluribus's opponents: thirteen vs fifteen; hands
- **Where:** summaryEn l. 584 "it beat a rotating cast of thirteen elite pros, several of them World Series or World Poker Tour champions,"; l. 762–763 "over tens of thousands of hands, against thirteen professionals"; l. 771 "about thirteen strong humans over tens of thousands of hands"; BG equivalents ("той победи въртящ се състав от тринадесет елитни професионалисти", "в десетки хиляди ръце, срещу тринадесет професионалисти", "за тринадесет силни човека в десетки хиляди ръце").
- **Problem:** Verified in the paper: 13 professionals rotated through 5H+1AI (10,000 hands, 12 days); the two in 1H+5AI (Chris Ferguson, Darren Elias — the WSOP/WPT champions the sentence names) were not among them (5,000 hands each). Across both formats: 15 professionals, 20,000 hands.
- **Now → Proposed:** EN l. 584 → "it beat fifteen elite professionals — thirteen rotating through the five-human format and two, the WSOP and WPT champions Chris Ferguson and Darren Elias, in the one-human format"; "tens of thousands of hands" → "20,000 hands"; BG "той победи въртящ се състав от тринадесет елитни професионалисти, няколко от които шампиони от Световните серии или Световния покер тур" → "той победи петнадесет елитни професионалисти - тринадесет, които се редуваха във формата с петима души, и двама (шампионите от WSOP и WPT Chris Ferguson и Darren Elias) във формата с един човек"; "в десетки хиляди ръце" → "в 20 000 раздавания".

### F06a-C03 · S2 · Loeliger "rematch" is overstated and unsourced
- **Where:** summaryEn l. 763–764 "A later rematch even beat **Linus Loeliger**, widely regarded as the best six-max cash player alive."; BG "По-късен реванш дори победи **Linus Loeliger**, широко смятан за най-добрия Six-Max Cash Player в момента."
- **Problem:** Loeliger is one of the thirteen 5H+1AI participants in the paper. The "later" 1H+5AI session comes from the Meta AI blog (per `research/pluribus.md`), which returned HTTP 500 when checked; secondary reports (PokerStrategy, Wikipedia) give −0.5 bb/100 for Loeliger, and the research notes give SE 1.0 — not significant. "even beat" overclaims; "Six-Max Cash Player" is English.
- **Now → Proposed (remove):** delete the sentence in EN and BG. If kept: "In an additional one-human session reported by Facebook AI, Linus Loeliger, regarded by many as the strongest six-max cash-game player, also finished behind Pluribus, by a margin (0.5 bb/100) that is not significant on its own." / "В допълнителна сесия с един човек, съобщена от Facebook AI, Linus Loeliger, смятан от мнозина за най-силния играч на кеш игри на маса с шестима, също завърши след Pluribus, но с разлика (0.5 bb/100), която сама по себе си не е статистически значима." — only after the blog is read.

### F06a-C04 · S2 · Libratus's compute: two incompatible figures in one chapter
- **Where:** summaryEn l. 742–743 "and Libratus around fifteen million core-hours to build its"; BG "а Libratus около петнадесет милиона ядро-часа за изграждане на своя план и приблизително сто-CPU клъстер за игра"
- **Problem:** The Libratus section (IJCAI-17, verified) says ~25 M core-hours in total, ~6 M of them for abstraction and blueprint. The 15 M comes from a CMU press release ("around 15 million core hours to develop its strategies"), which the Pluribus section turned into "to build its blueprint". Play: 100 CPUs (Pluribus paper), i.e. the 1,400 cores in the press release, is correct.
- **Now → Proposed:** EN (l. 742–743, across a line break) "Libratus around fifteen million core-hours to build its blueprint and a roughly hundred-CPU cluster to play" → "Libratus about 25 million core-hours in total (some 6 million of them for its blueprint) and 100 CPUs to play"; BG → "а Libratus - около 25 милиона ядро-часа общо (от тях около 6 милиона за плана) и 100 процесора по време на игра". The "thousandth" comparison stays true (12,400 vs 6–25 M).

### F06a-C05 · S2 · Why the landmark systems do not adapt — the papers' reasons, not a "principle"
- **Where:** summaryEn l. 82–83 (intro) "both it and Libratus refuse on principle to model"; l. 765–766 "it plays a fixed strategy, never models or adapts to opponents, and does not even know"; BG "а както тя, така и Libratus отказват по принцип да ги моделират или да се адаптират към тях, за да не бъдат контраексплоатирани в отговор"
- **Problem:** Pluribus's paper gives two reasons: shifting to an exploitative strategy "opens oneself up to exploitation because the opponent could also change strategies at any moment", and "existing techniques for opponent exploitation require too many samples to be competitive with human ability outside of small games". The identity remark is about collusion ("does not know the identity of its opponents, so the copies of Pluribus could not intentionally collude"). Libratus: "to a first approximation, Libratus did not do opponent exploitation" — with the same counter-exploitation reason. Both papers name "certain restricted ways" / "a certain conservative family of exploitation techniques" (Ganzfried & Sandholm's safe exploitation) as the exception. The sample-efficiency reason and the named exception are exactly the openings C1/C2 use; the chapter reduces them to "on principle".
- **Now → Proposed:** EN intro → "Pluribus does not even know its opponents' identities, and both it and Libratus deliberately avoid modelling or adapting to them — because an exploitative deviation can itself be counter-exploited and, in Pluribus's authors' words, because existing opponent-exploitation techniques 'require too many samples to be competitive with human ability outside of small games'; both papers name conservative (safe) exploitation as the only exception."; BG → "Pluribus дори не знае самоличността на своите опоненти, а и той, и Libratus съзнателно избягват да ги моделират или да се адаптират към тях - защото отклонението с цел експлоатация може да бъде контраексплоатирано и, по думите на авторите на Pluribus, защото съществуващите техники за експлоатация на противника „изискват твърде много наблюдения, за да се конкурират с човешките способности извън малките игри“; и двете статии посочват консервативната (безопасна) експлоатация като единствено изключение." Cite [^pluribus], [^libratus].

### F06a-C06 · S2 · Baby Tartanian8: the −8 is not a loss beyond noise
- **Where:** summaryEn l. 462 "Libratus's raw blueprint *lost* by 8 mbb/g"; BG "суровият план на Libratus *губи* с 8 mbb/g"; onePager.md "**lost** to Baby Tartanian8 by **8 mbb/g**"; onePagerBg "**загуби** от Baby Tartanian8 с **8 mbb/g**"
- **Problem:** Libratus *Science* Table 3: blueprint −8 ± 15 mbb/hand (95 % CI), post-processed blueprint +18 ± 21, on-tree nested solving +59 ± 28, full nested solving +63 ± 28. The heading claim "does not even beat the prior bot" stands; "lost by 8" without the interval does not.
- **Now → Proposed:** EN → "Libratus's raw blueprint did not beat it (−8 ± 15 mbb/g, 95 % CI)"; BG → "суровият план на Libratus не го побеждава (−8 ± 15 mbb/g при 95% доверителен интервал)"; one-pager EN "**lost** to Baby Tartanian8 by **8 mbb/g**" → "**did not beat** Baby Tartanian8 (**−8 ± 15 mbb/g**)"; BG "**загуби** от Baby Tartanian8 с **8 mbb/g**" → "**не победи** Baby Tartanian8 (**−8 ± 15 mbb/g**)".

### F06a-C07 · S2 · Modicum ablation: one of the two "losses" is noise, and the source is not the supplement
- **Where:** summaryEn l. 726–729 "The supplement does, however, dispatch one tempting misconception"… "was shown in the two-player precursor to *lose* to both champion bots (by 10 and 1 mbb/g)"; BG "Допълнението обаче разсейва едно изкушаващо погрешно схващане" … "е показано в двуигровия предшественик да *губи* от двамата шампионски бота (с 10 и 1 mbb/g)"
- **Problem:** Brown, Sandholm & Amos (NeurIPS-18) Table 1: naïve (single-value) depth-limited solving −10 ± 8 vs Baby Tartanian8, −1 ± 15 vs Slumbot; continuation strategies +6 ± 5 and +11 ± 9. Only the first is a loss; the source is the NeurIPS-18 paper.
- **Now → Proposed:** EN → "The two-player precursor paper dispatches one tempting misconception: … lost to Baby Tartanian8 (−10 ± 8 mbb/g) and did not beat Slumbot (−1 ± 15), whereas the four-continuation version beat both (+6 ± 5 and +11 ± 9)[^brown2018dls]"; BG → "Статията за двуигровия предшественик разсейва едно изкушаващо погрешно схващане: … губи от Baby Tartanian8 (−10 ± 8 mbb/g) и не побеждава Slumbot (−1 ± 15), докато версията с четири стратегии за продължение побеждава и двата бота (+6 ± 5 и +11 ± 9)". Also delete "and the way the underlying study notes sometimes gloss the method" / "и начинът, по който основните бележки понякога описват метода" — it points at the candidate's own notes, which a bundle reader does not have.

### F06a-C08 · S2 · Stale "Chapters 7–15" and "steps"
- **Where:** summaryEn l. 79 "and exploitation work of Chapters 7–15", l. 85 "opponent-awareness these systems omit that Chapters 7–15 set out to add"; BG "в глави 7–15, си струва" and "глави 7–15 се стремят да добавят"; BG "Класическите градивни елементи от по-ранните стъпки" (EN "of earlier chapters").
- **Now → Proposed:** "7–15" → "7–12" (EN and BG, both places); "от по-ранните стъпки" → "от по-ранните глави".
- **Why:** Chapters 13–15 were never written.

### F06a-C09 · S2 · One-pager: "several times the win rate"; "the human-tested systems say so"
- **Where:** onePager.md "several times the win rate that made them look strong" / "The human-tested systems say so explicitly"; onePagerBg "няколко пъти повече от темпа на печалба, който ги правеше да изглеждат силни" / "Системите, тествани срещу хора, го казват изрично"
- **Problem:** ACPC margins are tens of mbb/g (Baby Tartanian8 beat the next AIs by 12 ± 10 and 24 ± 20), so 3,000 mbb/g is about a hundred times the competition margins; the papers' own comparison is "four times as large as simply folding each game". DeepStack and ReBeL were tested against humans, but DeepStack's paper says nothing about adaptation; only Libratus and Pluribus say it.
- **Now → Proposed:** EN → "four times what folding every hand would lose"; "Libratus and Pluribus say so explicitly"; BG → "четири пъти повече, отколкото би се загубило при пас на всяко раздаване"; "Libratus и Pluribus го казват изрично".

### F06a-C10 · S3 · DeepStack's 10⁷ needs the sparse action set as well
- **Where:** summaryEn l. 196–198 "the depth-limited re-solve shrinks the game from $10^{160}$ decision points to about $10^{7}$"; BG "преизчисляването с ограничена дълбочина свива играта от $10^{160}$ решаващи точки до около $10^{7}$"
- **Problem:** Paper: the depth limit alone gives "no more than 10¹⁷"; "with sparse and depth-limited lookahead trees, the re-solved games have approximately 10⁷ decision points".
- **Now → Proposed:** EN → "the depth limit shrinks the re-solved game from $10^{160}$ decision points to at most $10^{17}$, and the sparse action set described below to about $10^{7}$"; BG → "ограничението по дълбочина свива пререшаваната игра от $10^{160}$ до най-много $10^{17}$ точки на решение, а описаният по-долу разреден набор от действия - до около $10^{7}$".

### F06a-C11 · S3 · DeepStack's opponents were not HUNL specialists; "unifies"
- **Where:** summaryEn l. 98–101 "was the first program to defeat professional poker players at heads-up no-limit Texas hold'em (HUNL)"; l. 72 "It is the theory that retroactively unifies DeepStack's continual"
- **Problem:** Both Libratus (*Science*) and Brown, Sandholm & Amos (2018) note that DeepStack's 33 professionals were "not specialists in HUNL" — the chapter says so only in the Libratus bridge. The depth-limited-solving paper presents DeepStack's joint-belief-state approach as an *alternative* with "benefits and drawbacks", not as a special case it unifies.
- **Now → Proposed:** add after "(HUNL)": "(professionals, though not HUNL specialists)" / BG "(професионалисти, макар и не специалисти по HUNL)"; "retroactively unifies" → "places in a common framework" / BG "ретроспективно обединява" → "поставя в обща рамка".

### F06a-C12 · S3 · Stale status line in the one-pager
- **Where:** onePager.md "and the chapter itself is drafted but not yet signed off"; onePagerBg "и самата глава е изготвена, но все още не е окончателно одобрена"
- **Fix:** delete in both (internal workflow status in a published bundle).

## S — Sources

Rows of `SOURCE_GAPS.md` § step06 that fall in this half: 14 (rows 1–12, 14 and the Pluribus-legacy row; the ReBeL/SoG/Synthesis rows are F06b's). Each proposal below was checked in the full text named.

### F06a-S01 · S2 · SOURCE_GAPS "Затворената празнина" (Claudico 91 mbb/g; LBR > 3,000) → cite
- **Where:** summaryBg DeepStack § "Затворената празнина" — "През 2015 г. абстрактно-базираната програма Claudico загуби от професионалисти с 91 mbb/g"
- **Proposal (cite):** append `[^deepstack]` after "с 91 mbb/g" and `[^lbr]` after "отколкото ако се откажеш от всяка ръка". Verified in arXiv:1701.01724v3: "In 2015, the computer program Claudico lost to a team of professional poker players by a margin of 91 mbb/g"; "All four abstraction-based programs are beatable by over 3,000 mbb/g, which is four times as large as simply folding each game." Lisý & Bowling (arXiv:1612.07547): "For every program tested, it would be far less exploitable to immediately fold every hand". The "2 TB / 14 CPU years" strategy is also DeepStack's (supplement: "almost 2TB of memory and … approximately 14 CPU years", computed for 100-BB stacks) — same footnote.

### F06a-S02 · S2 · SOURCE_GAPS "Архитектура" (DeepStack) → cite
- **Proposal (cite):** `[^deepstack]` after "(Фигура 6.1)" (see X01 for the figure reference). Verified: offline random situations solved to CFV targets, online two vectors (range, opponent CFVs), updates (i)–(iii) ("Opponent action: no change to our range or the opponent values are required"), seven 500-unit PReLU layers, 1,000 buckets, zero-sum outer network.

### F06a-S03 · S2 · SOURCE_GAPS "Изчислителна мощност и достъпност" (DeepStack) → cite
- **Proposal (cite):** `[^deepstack]` after "с под пет секунди на решение". Verified (supplement): turn net "10 million … solved with 6,144 CPU cores … over 175 core years"; flop net "a cluster of 20 GPUS and one-half of a GPU year"; "trained … over two days on a single GPU"; play "under five seconds using a single NVIDIA GeForce GTX 1080".

### F06a-S04 · S2 · SOURCE_GAPS "Силни страни и ограничения" (DeepStack) → cite
- **Proposal (cite):** `[^deepstack]` after the 350 mbb/g sentence (with F06a-B08). Verified: "Until DeepStack, no theoretically sound application of heuristic search was known in imperfect information games"; "LBR fails to exploit DeepStack at all — itself losing by over 350 mbb/g"; AIVAT "an impressive 85% reduction in standard deviation … significance … with as few as 3,000 games".

### F06a-S05 · S2 · SOURCE_GAPS "Наследство и съвременна значимост" (DeepStack) → cite, and correct the authors
- **Where:** summaryBg — "Brown & Sandholm формализираха **теорията на решаването с ограничена дълбочина** през следващата година" (also EN l. 69–70 "Formalized by Brown & Sandholm (2018)", l. 208–209, l. 275)
- **Proposal (cite + correct):** "Brown & Sandholm" → "Brown, Sandholm & Amos" in the four places, with a new footnote `[^brown2018dls]: Brown, N., Sandholm, T. & Amos, B. (2018). "Depth-Limited Solving for Imperfect-Information Games." *NeurIPS* 31; arXiv:1805.08195.` (verified: arXiv API metadata + full text). ReBeL: `[^rebel2020]: Brown, N., Bakhtin, A., Lerer, A. & Gong, Q. (2020). "Combining Deep Reinforcement Learning and Search for Imperfect-Information Games." *NeurIPS* 33; arXiv:2007.13544.` (verified: arXiv API; coordinate with F06b, which may add the same). SoG: existing `[^sog]`. CICERO (optional): Meta FAIR Diplomacy Team et al. (2022), *Science* 378(6624), 1067–1074, doi:10.1126/science.ade9097 (verified in `lit_gaps.md` via Crossref).

### F06a-S06 · S2 · SOURCE_GAPS "Архитектура" (Libratus) → cite
- **Proposal (cite):** `[^libratus]` after "(Фигура 6.2)". Verified (*Science*): "Libratus features three main modules"; card abstraction only on rounds 3–4 in the blueprint (55 M → 2.5 M, 2.4 B → 1.25 M buckets); regret-based pruning "a factor of three speedup"; CFR+ for subgames (note 46). The 10¹⁶¹ → 10¹² figure is from the IJCAI paper (`[^libratusijcai]`, S08).

### F06a-S07 · S2 · SOURCE_GAPS Baby Tartanian8 −8/+63 → cite with the intervals
- **Proposal (cite):** `[^libratus]` after "спечели с 63 mbb/g", and add the intervals (F06a-C06). Verified: Table 3 and text ("Using only the raw blueprint strategy, Libratus lost to Baby Tartanian8 by 8 ± 15 mbb/hand … defeating Baby Tartanian8 by 63 ± 28 mbb/hand").

### F06a-S08 · S2 · SOURCE_GAPS 25 M core-hours on Bridges → cite (new footnote)
- **Proposal (cite):** new `[^libratusijcai]: Brown, N. & Sandholm, T. (2017). "Libratus: The Superhuman AI for No-Limit Poker (Demonstration)." *IJCAI-17*. https://www.ijcai.org/proceedings/2017/0772` after "експериментални опити и оценка". Verified (full text): "In total, Libratus used about 25 million core hours. Of those, about 13 million … exploratory experiments and evaluation. About 6 million … initial abstraction and equilibrium finding …, another 3 million … nested subgame solving, and about 3 million … self-improvement"; "196 nodes on the Bridges supercomputer"; "The subgame solver used 50 nodes per game". The operational numbers (1 + 195 nodes for 1–8 weeks, 30–60 s per endgame solve, 196–600 nodes for 8–30 h, 2.6 PB, Jan 2016–Jan 2017) are verified in Sandholm, CMU 15-888 F21, Lecture 13 slides (which say "officially used ~24 million core hours") — cite those as `[^sandholm2021]` if the operational sentence stays.

### F06a-S09 · S2 · SOURCE_GAPS 147 mbb/g, 120,000 hands, 99.98 % → cite
- **Proposal (cite):** `[^libratus]` after "не оставя никакво реално съмнение" / after "99.98% значимост". Verified: "Libratus decisively defeated the humans by a margin of 147 mbb/hand, with 99.98% statistical significance and a p-value of 0.0002 (if the hands are treated as independent and identically distributed)… It also beat each of the humans individually"; note 57 on adaptation.

### F06a-S10 · S2 · SOURCE_GAPS the two bounds (k₁ε + k₂/√T; 2Δ) → cite
- **Proposal (cite):** in the Pluribus sentence "deepStack ограничи своята експлоатируемост до $k_1\epsilon + k_2/\sqrt{T}$, а Libratus - до $2\Delta$" add `[^deepstack]` and `[^brown2017]`; the same footnotes after the two displayed formulas. Verified: DeepStack main text, Theorem 1 ("exploitability is less than k₁ϵ + k₂/√T"); Libratus *Science* Theorem 1 ("overall exploitability at most 2Δ higher than that of σ*ᵢ") and NeurIPS-17 arXiv:1705.02955v3 Theorem 2 ("exploitability no higher than exp(σ*₂) + 2Δ").

### F06a-S11 · S2 · SOURCE_GAPS Modicum 10/1 vs 6/11 → cite (new footnote) and correct
- **Proposal (cite + correct):** `[^brown2018dls]` (S05) with the corrected sentence of F06a-C07. Verified: NeurIPS-18 Table 1 (numbers in C07); "defeats two prior top agents using only a 4-core CPU and 16 GB of memory".

### F06a-S12 · S2 · SOURCE_GAPS 8 days, 12,400 core-hours, 512 GB, $144 → cite
- **Proposal (cite):** `[^pluribus]` after "при спот цени в облака". Verified (*Science* 2019): "computed in 8 days on a 64-core server for a total of 12,400 CPU core hours. It required less than 512 GB of memory. … this would cost about $144"; play "two Intel Haswell E5-2695 v3 CPUs and uses less than 128 GB of memory"; "between 1 and 33 s"; "20 s per hand … roughly twice as fast as professional humans"; AlphaGo 1920 CPUs + 280 GPUs, Deep Blue 480 chips, "Libratus used 100 CPUs".

### F06a-S13 · S2 · SOURCE_GAPS "first … with more than two players" → cite
- **Proposal (cite):** `[^pluribus]` after "в най-популярната форма на покера". Verified: "Past successes in such benchmarks, including poker, have been limited to two-player games"; "all prior breakthroughs have been limited to settings involving only two players"; note 10 explains why two-team Dota 2 counts as two-player.

### F06a-S14 · S2 · SOURCE_GAPS Noam Brown and "test-time compute" → cite a report of the talk, and match its wording
- **Where:** summaryBg Pluribus § "Наследство…" — "Ноам Браун оттогава посочи точно това"; the same claim in the Libratus legacy paragraph ("наблюдението, че добавянето на търсене във време на тестване струваше далеч повече"), and the DeepStack legacy parenthesis "(изказано от Noam Brown)".
- **Proposal (cite + soften):** new `[^nunez2024]: Nuñez, M. (2024, 23 Oct.). "OpenAI's Noam Brown stuns TED AI Conference: '20 seconds of thinking worth 100,000x more data'." *VentureBeat*.` — verified via WebFetch of the article (the quote as returned: "having a bot think for just 20 seconds in a hand of poker got the same boosting performance as scaling up the model by 100,000x and training it for 100,000 times longer"; re-check the exact wording before quoting verbatim). Rephrase to match: "…that 20 seconds of search per hand improved his poker bot as much as scaling the model up 100,000-fold" / "…че 20 секунди търсене на раздаване подобряват покер бота толкова, колкото увеличаването на модела 100 000 пъти". The DeepStack parenthesis "(voiced by Noam Brown)" about belief-aware search has no source found — delete the attribution.

### F06a-S15 · S2 · The `libratus` footnote does not support the Claudico sentence it is attached to
- **Where:** summaryBg Libratus "The gap it closed" — "…отчасти защото опонентите можеха да усетят и накажат неговите граници на превод.[^libratus]"
- **Problem:** The Libratus *Science* paper does not mention Claudico (full-text search). The claim is supported by Ganzfried's account of the 2015 match: 9.16 BB/100 (≈ 91 mbb/g) over 80,000 hands, and the off-tree/translation "misperception of the pot size" that Doug Polk "views … as Claudico's biggest weakness".
- **Proposal (cite):** replace `[^libratus]` here by new `[^ganzfried2016]: Ganzfried, S. (2016). "Reflections on the First Man vs. Machine No-Limit Texas Hold 'em Competition." *ACM SIGecom Exchanges* 14(2), 2–15; arXiv:1510.08578.` (verified: arXiv full text; venue and pages from the reference list of Lisý & Bowling 2017), and move `[^libratus]` to the section's first sentence (S16).

### F06a-S16 · S2 · Citation placement: the Pluribus section cites nothing
- **Where:** summaryEn/Bg Pluribus section (no footnote at all; `[^pluribus]` is first used in the Synthesis); `[^deepstack]` hangs on the intro's last sentence about the chapter ("…а не класация на победители.[^deepstack]").
- **Proposal:** put each system's primary reference on its first mention: "DeepStack (Moravčík et al., 2017)[^deepstack]", "Libratus (Brown & Sandholm, 2017; Carnegie Mellon)[^libratus]", "Pluribus (Brown & Sandholm, 2019; Carnegie Mellon и Facebook AI)[^pluribus]", and a supplement footnote for the Pluribus caveats paragraph: `[^pluribussm]: Brown, N. & Sandholm, T. (2019). Supplementary Materials for "Superhuman AI for multiplayer poker." *Science* 365(6456).` (verified PDF: the "lacks theoretical guarantees" quote, "too expensive", "more effective, easier, and more elegant", the factor-3/2/>2 estimates, "probably at least five orders of magnitude", AIVAT "by about a factor of 9"). Remove the intro's `[^deepstack]`.

### F06a-S17 · S2 · Pluribus claims with no source found
- **Where:** summaryEn l. 749–750 "the authors explicitly present it as a rebuttal to the worry that frontier game-AI would belong only to teams with millions of dollars"; l. 775–776 "The authors add that the whole approach may not survive where players can **communicate and collude**"; BG "авторите я представят изрично като опровержение на опасението", "Авторите добавят, че целият подход може да не оцелее там, където играчите могат да **комуникират и се сговарят**, което покерът до голяма степен забранява."
- **Problem:** Neither appears in the paper or the supplement (full-text search); the notes attribute them to the Meta AI blog, which could not be read (HTTP 500).
- **Proposal (soften):** EN "the authors explicitly present it as…" → "the paper contrasts it with 'all the other recent superhuman AI milestones for games, which used large numbers of servers and/or farms of graphics processing units'"; the collusion sentence → "The paper claims only that 'there are large-scale, complex multiplayer imperfect-information settings in which a carefully constructed self-play-with-search algorithm can produce superhuman strategies'; it makes no claim for games in which players can communicate or collude." BG accordingly ("…статията го противопоставя на „всички други скорошни постижения на свръхчовешкия изкуствен интелект в игрите, които са използвали голям брой сървъри и/или ферми от графични процесори“" and "Статията твърди само, че „съществуват мащабни и сложни среди с много играчи и непълна информация, в които внимателно конструиран алгоритъм за самообучение с търсене може да създаде свръхчовешки стратегии“; за игри, в които играчите могат да комуникират или да се сговарят, тя не твърди нищо.").

### F06a-S18 · S3 · Footnote metadata (spot-check)
- **Findings:** `deepstack` correct (*Science* 356(6337), 508–513; doi:10.1126/science.aam6960 from arXiv metadata). `libratus` correct (*Science* 359(6374), 418–424; first release 17 Dec 2017, doi:10.1126/science.aao1733). `pluribus` correct (*Science* 365(6456), 885–890). `brown2017`: add "30, 689–699" and arXiv:1705.02955 (pages from Libratus ref. 43). `burch2014`: add "pp. 602–608" (from DeepStack ref. 17). `lbr`: add arXiv:1612.07547 (workshop verified in the arXiv PDF's reference style). The DeepStack quote "lack a theoretical justification" is inexact — the supplement says "Despite lacking a theoretical justification for its soundness"; drop the quotation marks or quote exactly. All other quoted phrases in this half were found verbatim.

## X — Structure

### F06a-X01 · S2 · Figure references "Figure 6.1–6.3" print against "Фигура 24–26"
- **Where:** summaryBg "(Фигура 6.1)", "(Фигура 6.2)", "(Фигура 6.3)"; EN "(Figure 6.1)", "(Figure 6.2)", "(Figure 6.3)" (6.4–6.5 in F06b's half). The single-document bundle numbers them 24, 25, 26 (pp. 83, 90, 99); no other chapter uses "N.M" references.
- **Fix:** "(Фигура 6.1)" → "(вж. фигурата по-долу)" (same for 6.2, 6.3; EN "(see the figure below)"), which survives renumbering.

### F06a-X02 · S2 · One template, three translations of its headings
- **Where:** EN "The gap it closed" → "Затворената празнина" / "The gap it closed" / "Пропуските, които запълни"; EN "Caveats, dead-ends, and what the paper under-describes" → "Ограничения, задънени улици и недостатъчно описаното в статията" / "Ограничения, задънени улици и какво е подценено в статията" / "Ограничения, неизследвани пътища и пропуснати детайли в статията"; table rows "Също и с пълна информация?" vs "Също и пълна информация?", "План (офлайн)?" vs "План (извън линия)?".
- **Fix:** one set for all five sections: "### Пропускът, който запълни"; "### Уговорки, задънени улици и какво статията не описва"; "### Изчислителни разходи и достъпност"; rows "| Също и с пълна информация? |", "| План (офлайн)? |". "Caveats" → "Уговорки" also frees "Ограничения" for "Силни страни и ограничения". Apply the same in ReBeL/SoG (F06b).

### F06a-X03 · S3 · Equal-width columns make the three scorecards run to a page each
- **Where:** pp. 81, 88, 97 — the left column (row labels) takes half the width, the values wrap into 3–5 lines; each table sits alone on a page with half-page gaps before it.
- **Fix:** separator "|---|---|" → "|--|------|" in the three tables (and in F06b's two).

### F06a-X04 · S3 · 10¹⁶⁰ vs 10¹⁶¹ for the same game
- **Where:** DeepStack sections "$10^{160}$", Libratus "$10^{161}$".
- **Fix:** both are the respective papers' counts; add once, at the Libratus figure: "(DeepStack's paper rounds the same count to 10¹⁶⁰)" / "(статията на DeepStack закръгля същия брой до $10^{160}$)".
