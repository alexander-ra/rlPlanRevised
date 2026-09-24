# Step 09 — final review

**Summary:** The chapter is well built and its numbers match the results JSON, but four things matter most. (1) The Bulgarian text contains visible defects: a leftover pipeline placeholder prints on p. 184 ("взаимно предателство ⟦MATHI1⟧"), and English is left in the prose ("single-agent RL", "Stag Hunt/Hare", "Kuhn's Theorem", "Machine Zero", "**lOLA learners**", "jSON artifacts", "smoke config"). Several meaning errors come from settled glossary entries: *Defect* → "дефект" (a flaw), *thesis hooks* → "три теза", *greedy team reward* → "награда за отборна алчност", *communication ON* → "комуникация върху", *time-average* → "усредненото време", *hard-exploration* → "прекомерно изследване", *self-play* rendered as "самостоятелно обучение" (which in this chapter means independent learning). (2) Figures: six of the ten are entirely English in the BG bundle (47, 48, 50, 52–54). Fig. 50's title asserts the refuted prediction ("CTDE escapes the safe trap"). Fig. 46 has overlapping boxes and contradicts its caption. Fig. 49 has colliding notes. The Matching Pennies panel of fig. 47 shows no movement at all. (3) Content: the EN and BG both say LOLA "differentiates through that **chapter**" (a step→chapter replace went too far). The CTDE "variance-reduction claim, confirmed" is contradicted by Lyu et al. (2021): what was measured is the critic's fit residual, not policy-gradient variance. The "MADDPG" that underperforms is a COMA-style variant. The Leduc PSRO curve is not "roughly monotone". (4) Both SOURCE_GAPS items can be closed with verified citations, but the CTDE variance claim must also be softened.
**Counts:** S1 27 · S2 46 · S3 10   (by category: G 12 · B 35 · T 11 · C 12 · S 8 · X 5)

Conventions in this file: quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md` (including `**`, `*`, `$`), so read this file as source, not rendered. Proposals keep the chapter's current " - " dashes and decimal points; those are fixed centrally. "EN" quotes come from `summaryEn.md` / `onePager.md`. Page numbers are PDF page numbers of `allSummaries_bg.pdf`, as in `renders/manifest.json`; the printed folio is one lower. Printed type size = matplotlib size × (printed width ÷ saved width); body text is 10.9 pt and the floor is ≈ 8.2 pt. Centrally decided items in this chapter, not reported per occurrence: 86 hyphens used as dashes (71 summary, 15 one-pager); 71 decimal points (56 + 15); about 17 extra bold spans (BG 113 vs EN 99 in the summary, 23 vs 20 in the one-pager). Footnote-label sharing (F07-X01): **0** in this chapter. All 8 footnotes (54–61) print on the chapter's own pages. The leftover placeholder of F09-B01 also occurs in step06 `summaryBg.md` l. 454 and step08 l. 141 and l. 186; worth a corpus-wide grep for "⟦".

## G — Figures

### F09-G01 · S1 · Bulgarian captions for all ten figures
- **Where:** summaryBg.md, image alt text of figs. 45–54 (pp. 168–186). All ten print in English (known corpus-wide defect). Fig. 51's alt text also says "Step 07's" and "game-theory steps". Fig. 52's contains the only Cyrillic word ("Ледюк") inside an English sentence.
- **Now → Proposed** (the `](file.png)` part stays; for the six data figures also see F09-G12). Where a caption also needs a content fix (figs. 48, 50, 52, 54), the BG below already includes it, and the EN change is in the figure's own finding.
  - "![Non-stationarity as two partners learning to dance at once. …](nonstationarity_dance_bg.png)" → "![Нестационарността като двама партньори, които се учат да танцуват едновременно. Всеки агент оптимизира спрямо текущата стратегия на другия (плътните стрелки), но тази стратегия също се променя, защото другият агент на свой ред оптимизира спрямо него (пунктирните стрелки). Целта, която всеки преследва, никога не стои на място, затова наивните обучаващи се агенти циклират или прекалено се коригират, вместо да се сближат с равновесие. Всеки метод в тази глава е различен начин целта да се задържи неподвижна достатъчно дълго, за да може агентът да се научи спрямо нея.](nonstationarity_dance_bg.png)"
  - "![The method family on two axes. …](methods_spectrum_bg.png)" → "![Семейството методи по две оси. Хоризонтално: доколко целевата среда е кооперативна или конкурентна (IL и PSRO обхващат и конкурентните среди; MADDPG, MAPPO, QMIX и CommNet са насочени към сътрудничество; LOLA е мостът към смесените мотиви). Вертикално: какво и кога се централизира (нищо при IL; оценителят по време на обучение при CTDE; пълното решаване на мета-играта при PSRO; информацията по време на изпълнение при CommNet). LOLA е изключението, което моделира противника като учещ се агент, а не като фиксирана стратегия.](methods_spectrum_bg.png)"
  - "![Independent learners on the four matrix games: …](matrix_games_playground.png)" → "![Независими обучаващи се агенти в четирите матрични игри: в дилемата на затворника те стигат до взаимно предателство, в „лов на елен“ и „битка на половете“ се установяват в чисто равновесие, а в „съвпадение на монети“ не се сближават (траекторията се отдалечава от смесеното равновесие на Наш, вместо да се установи в него). Контрастът показва нагледно защо са нужни механизми за координация.](matrix_games_playground_bg.png)"
  - "![Zoom on non-stationarity: …](nonstationarity_demo.png)" → "![Нестационарността отблизо: при „съвпадение на монети“ разстоянието до смесеното равновесие на Наш не намалява, а расте през последователните времеви прозорци (от 0.30 до 0.48); траекторията се отдалечава по спирала към границата. Последната итерация не се сближава, колкото и дълго да продължи обучението.](nonstationarity_demo_bg.png)"
  - "![CTDE architecture. …](ctde_architecture_bg.png)" → "![Архитектура CTDE. По време на обучението централизиран оценител (или функция на стойността) вижда глобалното състояние и съвместното действие и дава целеви стойности с ниска дисперсия; по време на изпълнението всеки актьор действа само въз основа на собственото си локално наблюдение, без достъп до оценителя и без обмен на съобщения. Асиметрията между обучение и изпълнение прави света стационарен в очите на обучаващия се агент, без да се „мами“ по време на реалната игра.](ctde_architecture_bg.png)"
  - "![Cooperative CTDE and communication results (scale config). …](impl_coop_ctde_comm.png)" → "![Резултати за кооперативното CTDE и за комуникацията (пълна конфигурация). Вляво: остатъкът на централизирания оценител е с порядъци по-малък от този на независимия. В средата: в играта „изкачване“ нито един метод не достига оптимума (11); MADDPG (5) изостава от IL и MAPPO (7) - CTDE намалява дисперсията на оценителя, но само по себе си не решава координацията, когато изследването е трудно. Вдясно: комуникацията издига слушателя далеч над тавана при случайно отгатване 1/K (вж. раздел 9.7).](impl_coop_ctde_comm_bg.png)"
  - "![The PSRO double-oracle loop. …](psro_loop_bg.png)" → "![Цикълът на двойния оракул в PSRO. От текущите популации се построява матрицата на печалбите на мета-играта и се намира нейната мета-Наш смес; оракулът за най-добър отговор изчислява отговор на сместа на противника и новата стратегия се добавя към популацията. Очаква се експлоатируемостта на мета-Наш сместа да намалява с нарастването на популацията. В този проект оракулът е точният най-добър отговор от Глава 7, затова сходимостта на PSRO се измерва със същата мярка за експлоатируемост като в главите по теория на игрите.](psro_loop_bg.png)"
  - "![PSRO exploitability vs population size across games (scale config). …](impl_psro_exploitability.png)" → "![Експлоатируемост при PSRO спрямо размера на популацията в различни игри (пълна конфигурация). При Кун и при матричната игра тя спада до (почти) нула за няколко кръга; при Ледюк силно се колебае през първите осем кръга, след което намалява, но след 20 кръга остава далеч над целта 0.5 (стената на мащабиране за популация от чисти стратегии); при Goofspiel с K = 4 се колебае, без да се установи (отбелязана аномалия). Точният оракул за най-добър отговор гарантира сходимост по принцип; размерът на играта определя скоростта.](impl_psro_exploitability_bg.png)"
  - "![Self-play on Kuhn: …](selfplay_vs_nash.png)" → "![Игра срещу себе си в Кун: експлоатируемостта (NashConv) на средната стратегия постепенно спада към нула, докато тази на последната итерация продължава да се колебае. Затова играта срещу себе си и PSRO разчитат на осредняване по популацията, а не на последната стратегия.](selfplay_vs_nash_bg.png)"
  - "![LOLA vs naive learners on the Iterated Prisoner's Dilemma: …](lola_ipd_playground.png)" → "![LOLA срещу наивни обучаващи се агенти в повтарящата се дилема на затворника: при наивните агенти възвръщаемостта на стъпка спада към взаимно предателство (~1), а при агентите с LOLA нараства към взаимно сътрудничество (~2.8, средно за двамата агенти). Именно предвиждането на следващата стъпка на обучение на противника превръща динамиката от предателство в сътрудничество.](lola_ipd_playground_bg.png)"
- **Fix:** replace the alt text in `summaryBg.md`. The `_bg` file names for the six data figures exist only after F09-G12.

### F09-G02 · S2 · Fig. 45 non-stationarity dance: English line, overflowing bottom box, small notes
- **Where:** `renders/ch09/p168_f1.png`, caption "Non-stationarity as two partners…"
- **Problem:**
  1. English in the BG figure: the top line starts "Single-agent RL предполага фиксиран свят; тук 'светът' е партньор…". It also uses straight single quotes instead of „…“.
  2. The bottom box overflows on both sides: "нестационарност: целта на всеки агент е друг обучаващ се, така че никога не стои на едно място" runs about 2 cm past the box.
  3. "Агент 1 / стратегия π₁ (обучение)" touches both box edges. "(обучение)" reads "(training)", but the meaning is "is learning".
  4. Legibility: 2563 px at 330 dpi, printed at 17.6 cm, so the scale is 0.892. Box text 9.5 → 8.5 pt. Arrow notes 8.4 → 7.5 pt. Red notes 7.8 → 7.0 pt. Bottom box and top line 8.6 → 7.7 pt.
- **Fix:** `make_nonstationarity_figure.py`:
  - All `note` fs → 10; bottom `box` fs 8.6 → 10, height 0.72 → 1.05 (y 0.15 → 0.05), width 6.8 → 9.0 (x 3.6 → 2.5).
  - Agent boxes width 3.4 → 3.8 (x 1.0 → 0.8 and 9.6 → 9.4).
  - Mapping:
    - "Single-agent RL assumes a fixed world; here the 'world' is a partner who is also learning." → "Едноагентното обучение с подкрепление приема, че светът е неизменен; тук „светът“ е партньор, който също се учи."
    - "non-stationarity: each agent's target is another learner, so it never holds still" → "нестационарност: целта на всеки агент е друг учещ се агент,\nзатова тя никога не стои на място"
    - "Agent 1\npolicy $\\pi_1$ (learning)" → "Агент 1\nстратегия $\\pi_1$ (учи се)" (the same for Agent 2)
    - "best-responds to $\\pi_2$ (as it is now)" → "най-добър отговор на текущата $\\pi_2$" (the same for $\\pi_1$)

### F09-G03 · S1 · Fig. 46 method map: overlapping boxes and label, IL placed against the caption, prints at 6–7 pt
- **Where:** `renders/ch09/p172_f1.png`, caption "The method family on two axes…"
- **Problem:**
  1. Illegible overlaps (the EN figure has them too):
     - The CommNet box (x 1.9–4.3) is drawn over the MAPPO box (x 3.2–5.6) and hides the start of "MAPPO".
     - The note "оценител @ обучение" (x 2.2, y 4.6) is printed inside the MADDPG box (y 4.2–5.15).
  2. Figure contradicts caption: the caption says "IL and PSRO span competition", but the IL box sits in the cooperative corner (x 2.2–4.8).
  3. The vertical axis label "централизация ⟶" has a horizontal arrow on a vertical axis.
  4. Overflow (central fix): "моделира опонента като ОБУЧАВАЩ СЕ" runs past the LOLA box.
  5. BG wording:
     - "Две оси организират полето" (*field* as a pitch).
     - "(инфо @ изпълнение)", with "@" and the colloquial "инфо".
     - "нито един" for *none*: here it means "no centralisation", not "not a single one".
     - "опонент" next to "противник" elsewhere.
  6. Legibility: 2840 px at 330 dpi, so the scale is 0.805. Box text 7.8–8.4 → 6.3–6.8 pt. Notes 7.4–7.6 → 6.0–6.1 pt. Axis labels 9.5 → 7.6 pt.
- **Fix:** `make_methods_spectrum_figure.py`:
  - Move the boxes apart:
    - MAPPO `box(ax, 4.6, 3.1, 2.4, 0.95, …)`
    - MADDPG `box(ax, 4.6, 4.3, 2.4, 0.95, …)`
    - QMIX `box(ax, 1.9, 4.3, 2.4, 0.95, …)`
    - The note "critic @ training" to `note(ax, 7.2, 4.8, …, ha="left")`.
  - IL spans the axis: `box(ax, 2.2, 1.9, 10.4, 0.95, "Independent Learning (any setting)", …)`.
  - The vertical label: `ax.text(0.55, 5.3, "centralization  $\\longrightarrow$", rotation=90, …)`.
  - Font sizes: all `box` fs → 10.5 and all `note` fs → 10.5, because this figure needs fs ≥ 10.2.
  - Mapping:
    - "Two axes organize the field: what/when is centralized, and whether the opponent is static or learning." → "Две оси подреждат областта: какво и кога се централизира и дали противникът е статичен, или се учи."
    - "LOLA\nmodels opponent as a LEARNER" → "LOLA\nмоделира противника като УЧЕЩ СЕ"
    - "the odd one out: dynamic, not static, opponent" → "изключението: динамичен, а не статичен противник"
    - "CommNet\n(info @ exec)" → "CommNet\n(информация при изпълнение)"
    - "critic @ training" → "оценител при обучение"
    - "none" → "без централизация"
    - "centralization  $\\longrightarrow$" → "централизация  $\\longrightarrow$"
    - new key "Independent Learning (any setting)" → "Независимо обучение (във всякакви среди)"

### F09-G04 · S1 · Fig. 47 matrix games: entirely English, the Matching Pennies panel shows nothing, legend at 4.9 pt
- **Where:** `renders/ch09/p175_f1.png`, caption "Independent learners on the four matrix games…"; `summaryBg.md` links the EN `matrix_games_playground.png`.
- **Problem:**
  1. Everything is English: panel titles with underscores ("prisoners_dilemma", "matching_pennies", …), axis labels "P(row=Cooperate)", legend "start/end", suptitle.
  2. **Does not show what the caption claims.** The run starts exactly at the mixed equilibrium, `CONFIG["init"] = [0.5, 0.5]` (`exploration/figures/matrix_games_playground.json`). So in the Matching Pennies panel the start and end markers sit on top of each other at (0.51, 0.50), and no trajectory is visible. The caption says it "drifts away from the mixed Nash".
  3. Legibility: figsize (10, 8) at 120 dpi (1200 px) printed at 17.6 cm, so the scale is 0.693. Ticks and axis labels 10 → 6.9 pt; titles 12 → 8.3 pt; legend 7 → 4.9 pt; 173 effective ppi.
- **Fix:** `exploration/matrix_games_playground.py`, in `_plot`:
  - For "matching_pennies", run from `init=(0.7, 0.3)` (as `nonstationarity_demo.py` does) and note "(start off-centre)" in the title. Update report_en/bg §2's MP row from the regenerated JSON, or keep the table's run and plot a separate off-centre one.
  - `figsize=(7, 5.6)`, `dpi=300`, `ax.legend(fontsize=10)`, `ax.set_title(TITLE_BG_OR_EN[name])` with display names instead of dict keys.
  - Mapping: the "Останали на английски" entries get real values:
    - "prisoners_dilemma" → "Дилема на затворника"
    - "matching_pennies" → "Съвпадение на монети"
    - "stag_hunt" → "Лов на елен"
    - "battle_of_the_sexes" → "Битка на половете"
    - "P(col=Stag)" → "P(колона = Елен)", "P(col=Opera)" → "P(колона = Опера)"
    - new "P(row=Cooperate)" → "P(ред = Сътрудничество)", "P(col=Cooperate)" → "P(колона = Сътрудничество)", "P(row=Stag)" → "P(ред = Елен)", "P(row=Opera)" → "P(ред = Опера)"
    - "start" → "начало"
    - "Independent learners in 2x2 games (strategy-space trajectories)" → "Независими обучаващи се агенти в игри 2×2 (траектории в пространството на стратегиите)"

### F09-G05 · S1 · Fig. 48 Matching Pennies spiral: English, title says "orbit", legend covers the equilibrium, caption describes a curve that is not there
- **Where:** `renders/ch09/p176_f1.png`, caption "Zoom on non-stationarity…"
- **Problem:**
  1. Entirely English (title, axes "P(row = Heads)", legend).
  2. The title "independent learners orbit, never converge" contradicts the chapter's own reconciliation ("neither orbited cleanly … spirals outward").
  3. The legend box sits on the centre and hides the equilibrium star at (0.5, 0.5); only a grey half-star shows next to "start".
  4. The caption says "while the Prisoner's Dilemma distance-to-(Defect,Defect) collapses to zero", but the figure plots only Matching Pennies.
  5. 120 effective ppi (720 px at 15.2 cm), so it prints soft.
  6. Existing mapping entries: "Игра „хвърляне на монета“: … никога не Сходяват" (capital С, non-word, wrong game name); "P(row = Ези)" (half English); "смесено равновесие на Наш (0.5,0.5)" (decimal points).
- **Fix:** `exploration/nonstationarity_demo.py`:
  - Title → "Matching Pennies: independent learners spiral outward, never converge".
  - `ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize=10)`, `fig.savefig(out, dpi=300, bbox_inches="tight")`.
  - EN caption: "while the Prisoner's Dilemma distance-to-(Defect,Defect) collapses to zero" → delete, or plot the PD radius as an inset.
  - Mapping:
    - new title key → "„Съвпадение на монети“: независимите агенти се отдалечават по спирала и не се сближават"
    - "P(row = Heads)" → "P(ред = Ези)", "P(col = Heads)" → "P(колона = Ези)"
    - "mixed Nash (0.5,0.5)" → "смесено равновесие на Наш (0,5; 0,5)"
    - "end" stays "край"; "start" → "начало"
  - See also F09-C02 on the "more compute" sentence.

### F09-G06 · S1 · Fig. 49 CTDE architecture: the two bottom notes print on top of each other; every label box overflows
- **Where:** `renders/ch09/p177_f1.png`, caption "CTDE architecture…"
- **Problem:**
  1. Illegible: the two notes at y = 0.95 (x = 3.7 and 11.2) collide in the middle, "…да изг[без оценител, без с]ъобщения…". Both BG strings are longer than half the figure.
  2. Overflow (central fix):
     - "Централизиран оценител Q(s, a₁, a₂)" (the formula overlaps the box edge)
     - "глобално състояние s"
     - "съвместно действие a₁,a₂"
     - both "локално наблюдение o₁/o₂"
  3. BG wording:
     - "нискодисперсностна цел" is not a word.
     - "той прави света на всеки актьор да изглежда стационарен" is a calque of *makes … look*.
     - "всеки агент е сам по себе си, на локални наблюдения".
  4. Legibility: 2972 px at 330 dpi, so the scale is 0.769. Critic 8.8 → 6.8 pt; other boxes 8.2–8.4 → 6.3–6.5 pt; notes 7.8 → 6.0 pt; panel titles 10.5 → 8.1 pt.
- **Fix:** `make_ctde_figure.py`:
  - All `box` and `note` fs → 11, because this figure needs fs ≥ 10.7. Label boxes (gs, ja, o1, o2) height 0.9 → 1.2 and two-line text. Critic box height 1.2 → 1.6.
  - Notes as two lines each, inside their panels: `note(ax, 3.75, 0.85, …)` and `note(ax, 11.25, 0.85, …)`.
  - Mapping:
    - "Centralized critic  $Q(s,\\,a_1,a_2)$\n(low-variance target)" → "Централизиран оценител\n$Q(s,\\,a_1,a_2)$ (цел с ниска дисперсия)"
    - "global state $s$" → "глобално\nсъстояние $s$"
    - "joint action $a_1,a_2$" → "съвместно\nдействие $a_1,a_2$"
    - "local obs $o_1$" → "локално\nнаблюдение $o_1$" (the same for $o_2$)
    - "the critic sees everything; it makes each actor's world look stationary" → "оценителят вижда всичко:\nза всеки актьор светът изглежда стационарен"
    - "no critic, no messages: each actor is on its own, on local obs" → "без оценител и без съобщения:\nвсеки актьор разчита само на своето наблюдение"

### F09-G07 · S1 · Fig. 50 cooperative results: English, a title that states the refuted prediction, 5.3 pt type
- **Where:** `renders/ch09/p179_f1.png`, caption "Cooperative CTDE and communication results (scale config)…"
- **Problem:**
  1. The middle panel's title reads **"Climbing game: CTDE escapes the safe trap"**, while the bars below it show that no method escapes and MADDPG sits exactly on the safe value 5. The figure asserts the prediction the chapter reports as refuted. The existing mapping entry translates this false title ("CTDE избягва безопасния капан").
  2. Entirely English: titles, "final critic loss", "greedy reward", tick labels "central/independent", "comm ON/OFF", legends "optimum=11.0", "safe=5.0", "1/K ceiling=0.2".
  3. The central critic's bar (3.2e-11) is invisible on the linear axis, so the left panel shows one bar only.
  4. Legibility: figsize (13, 4) at 120 dpi printed at 17.6 cm, so the scale is 0.533. Ticks, axis labels and legends 10 → 5.3 pt; titles 12 → 6.4 pt.
  5. `plotting.py`'s `main()` defaults to `--config smoke`, and `render_bg_figures.py` runs `__main__` with no arguments. A BG render would therefore plot the **smoke** numbers (IL 5, MADDPG 5, MAPPO 6; comm 0.24/0.24) under a caption quoting the scale numbers.
- **Fix:** `implementation/step09/implementation/plotting.py`:
  - Title → "Climbing game: no method reaches the optimum".
  - `figsize=(7.5, 3.2)`, `dpi=300`, `axes[0].set_yscale("log")`.
  - Static legend labels ("optimum", "safe", "1/K ceiling"). The values are visible on the axis, and f-strings cannot be mapped.
  - `ap.add_argument("--config", default="scale", …)`.
  - Mapping:
    - new title key → "Игра „изкачване“: нито един метод не достига оптимума"
    - "greedy reward" → "награда при алчна стратегия"
    - "Critic residual (lower = less variance)" → "Остатък на оценителя (по-нисък = по-малка дисперсия)"
    - "final critic loss" → "крайна загуба на оценителя"
    - "Communication lifts the listener above 1/K" → "Комуникацията издига слушателя над 1/K"
    - new "central" → "централизиран", "independent" → "независим", "comm ON" → "с комуникация", "comm OFF" → "без комуникация", "optimum" → "оптимум", "safe" → "безопасна стойност", "1/K ceiling" → "таван 1/K"

### F09-G08 · S1 · Fig. 51 PSRO loop: stale "Стъпка", first person, "предсказвач", overflowing bottom box, small notes
- **Where:** `renders/ch09/p180_f1.png`, caption "The PSRO double-oracle loop…"
- **Problem:**
  1. Stale naming: "итериран най-добър отговор от стъпка 2" (top line) and "(точен BR, Стъпка 07)" (oracle box). The EN source strings say "Step 2's" / "Step 07".
  2. First person: "оптимално отговарям на σ" (F07-T03). Imperatives in the arrow labels: "симулирай сблъсъци", "реши", "добави".
  3. "Предсказвач за най-добър отговор" (*oracle* → "predictor", F09-T07). "Съвкупност от политики" (the text also says "популация", and the glossary has policy → стратегия). "Емпирична мета-игра / матрица на печалбата M" is a noun pile. "σ над популацията" (*over* as "above").
  4. The bottom box overflows on both sides: "експлоатируемостта на σ (NashConv) намалява с растежа на популацията".
  5. Legibility: 2780 px at 330 dpi, so the scale is 0.823. Boxes 8.4–8.8 → 6.9–7.2 pt; arrow labels 7.2 → 5.9 pt; top line 8.6 → 7.1 pt.
- **Fix:** `make_psro_loop_figure.py`:
  - Source strings "Step 2's" → "Chapter 2's", "(exact BR, Step 07)" → "(exact BR, Chapter 7)".
  - All fs → 10.5; bottom box height 0.9 → 1.2 (two-line text).
  - Mapping (new keys where the source changes):
    - "PSRO = Chapter 2's iterated best response, lifted from actions to whole policies." → "PSRO = итерираният най-добър отговор от Глава 2, пренесен от действия към цели стратегии."
    - "Best-response oracle\n$\\pi^{k+1}=\\mathrm{BR}(\\sigma_{-i})$\n(exact BR, Chapter 7)" → "Оракул за най-добър отговор\n$\\pi^{k+1}=\\mathrm{BR}(\\sigma_{-i})$\n(точен BR, Глава 7)"
    - "best-respond\nto $\\sigma$" → "най-добър\nотговор на $\\sigma$"
    - "Population of policies\n$\\{\\pi^1,\\dots,\\pi^k\\}$ per player" → "Популация от стратегии\n$\\{\\pi^1,\\dots,\\pi^k\\}$ за всеки играч"
    - "Empirical meta-game\npayoff matrix $M$" → "Емпирична матрица на\nпечалбите $M$ на мета-играта"
    - "Meta-Nash mixture\n$\\sigma$ over the population" → "Мета-Наш смес\n$\\sigma$ върху популацията"
    - "simulate\nmatch-ups" → "симулиране\nна срещите"
    - "solve" → "решаване"
    - "add $\\pi^{k+1}$\nto population" → "добавяне на $\\pi^{k+1}$\nкъм популацията"
    - "exploitability of $\\sigma$ (NashConv) falls as the population grows" → "експлоатируемостта на $\\sigma$ (NashConv) намалява,\nкогато популацията расте"

### F09-G09 · S1 · Fig. 52 PSRO exploitability: English, soft, caption describes curves that are not plotted or not steady
- **Where:** `renders/ch09/p182_f1.png`, caption "PSRO exploitability vs population size…"
- **Problem:**
  1. Entirely English, including the legend's code names "kuhn", "leduc", "matrix:matching_pennies", "goofspiel K=4".
  2. 840 px at 17.6 cm = 121 ppi (soft); x ticks 2.5 / 7.5 / … for integer rounds.
  3. The caption says Rock–Paper–Scissors collapses to zero, but RPS is not plotted (it is in `psro_peek.png`, which the chapter does not show). It says Leduc "declines steadily", but the plotted curve rises to 6.83 at round 1 and oscillates between 3.7 and 6.8 until round 7 (see F09-C06).
  4. Mapping value "Цел в Ледюк < 0.5" has a decimal point.
- **Fix:** `plotting.py` `plot_psro`:
  - `dpi=300`; `ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))`; display names instead of keys.
  - EN caption: "Kuhn, the matrix game, and Rock-Paper-Scissors collapse" → "Kuhn and the matrix game collapse"; "Leduc declines steadily but stays" → "Leduc oscillates for the first eight rounds, then declines but stays".
  - Mapping:
    - new "kuhn" → "Кун", "leduc" → "Ледюк", "matrix:matching_pennies" → "матрична игра („съвпадение на монети“)", "goofspiel K=4" → "Goofspiel, K=4"
    - "Leduc target < 0.5" → "цел за Ледюк < 0,5"
    - "PSRO round (population size - 1)" → "Кръг на PSRO (размер на популацията − 1)"
    - "meta-Nash exploitability (NashConv)" → "експлоатируемост на мета-Наш сместа (NashConv)"
    - "PSRO: exploitability shrinks as the population grows" → keep the existing BG.

### F09-G10 · S1 · Fig. 53 self-play: entirely English, soft
- **Where:** `renders/ch09/p183_f1.png`, caption "Self-play on Kuhn…"
- **Problem:** Title, legend ("average iterate", "last iterate (pure BR)") and axis labels are English. None of these strings is in the mapping, so the script was apparently not captured by the extractor. 121 ppi. Type size itself is fine (scale 0.99).
- **Fix:** `exploration/selfplay_vs_nash.py`:
  - `dpi=300`, `ax.legend(fontsize=10)`.
  - Mapping (new keys):
    - "Kuhn self-play: the AVERAGE converges to Nash, the last iterate does not" → "Кун, игра срещу себе си: СРЕДНАТА стратегия се сближава с равновесието на Наш, последната итерация - не"
    - "average iterate" → "средна стратегия"
    - "last iterate (pure BR)" → "последна итерация (чист BR)"
    - "fictitious-play iteration" → "итерация на фиктивната игра"
    - "NashConv (exploitability)" → "NashConv (експлоатируемост)"

### F09-G11 · S1 · Fig. 54 LOLA on IPD: entirely English, soft, legend below the floor, plots one agent only
- **Where:** `renders/ch09/p186_f1.png`, caption "LOLA vs naive learners on the Iterated Prisoner's Dilemma…"
- **Problem:**
  1. English throughout.
  2. Legend fontsize 8 → 7.9 pt; 121 ppi.
  3. Only agent 1 is plotted. Its LOLA curve peaks at 2.84 near step 110 and ends at 2.67, so "climbs toward mutual cooperation (~2.8)" does not describe it. Agent 2 ends at 2.93; the mean of the two is 2.80 (`exploration/figures/lola_ipd_playground.json`).
  4. Mapping "IPD: LOLA достига сътрудничество там, където наивните учащи дефектират" uses "дефектират" (F09-T03) and "учащи".
- **Fix:** `exploration/lola_ipd_playground.py`:
  - Plot `(v1+v2)/2` for each learner type, labels "naive (mean of both agents)" / "LOLA (mean of both agents)".
  - `ax.legend(fontsize=10)`, `dpi=300`.
  - Mapping:
    - "IPD: LOLA reaches cooperation where naive learners defect" → "Повтаряща се дилема на затворника: LOLA стига до сътрудничество, наивните агенти - до предателство"
    - new "naive (mean of both agents)" → "наивни (средно за двамата агенти)", "LOLA (mean of both agents)" → "LOLA (средно за двамата агенти)"

### F09-G12 · S2 · The six data figures never got BG versions; how to produce them
- **Where:** `summaryBg.md` links `matrix_games_playground.png`, `nonstationarity_demo.png`, `impl_coop_ctde_comm.png`, `impl_psro_exploitability.png`, `selfplay_vs_nash.png`, `lola_ipd_playground.png` (all EN). No `*_bg.png` exists under `implementation/step09/**`.
- **Problem:** The four diagram figures are translated; the six result plots are not. They live under `implementation/step09/{exploration,implementation}` and are *copied* into `deliverables/reports/step09/summary/`. So even a successful BG render would not reach the bundle. The four BG diagram renders date from 1 Aug; re-render them after the mapping changes above.
- **Fix:**
  1. After F09-G04/05/07/09/10/11, run `python scripts/figures/render_bg_figures.py --only step09`.
  2. Copy `exploration/figures/*_bg.png` and `implementation/plots/{psro_exploitability,coop_ctde_comm}_bg.png` into `deliverables/reports/step09/summary/` (the latter two as `impl_…_bg.png`).
  3. Point the six links in `summaryBg.md` to the `_bg` names (done in F09-G01).
  4. For the diagrams, keep every fs ≥ the per-figure floor given above (9.2 / 10.2 / 10.7 / 10.0 for figs. 45 / 46 / 49 / 51). Wrap text or enlarge boxes rather than shrinking type.
  5. Raise `note()`'s default fs 7.6 → 10.5 in `deliverables/reports/step09/summary/_diagram_utils.py`.

## B — Bulgarian language

### F09-B01 · S1 · leftover pipeline placeholder prints on p. 184
- **Where:** summaryBg.md § "LOLA - моделиране на опонента като учащ се", "Измерена (дисконтирана възвръщаемост на стъпка; пълно сътрудничество $\approx 3$, взаимно предателство ⟦MATHI1⟧):"
- **EN:** "Measured (per-step discounted return; full cooperation $\approx 3$, mutual defection $\approx\n1$):"
- **Now → Proposed:** "Измерена (дисконтирана възвръщаемост на стъпка; пълно сътрудничество $\approx 3$, взаимно предателство ⟦MATHI1⟧):" → "Измерено (дисконтирана възвръщаемост на стъпка; пълно сътрудничество $\approx 3$, взаимно предателство $\approx 1$):"
- **Why:** The placeholder prints literally ("телство ⟦MATHI1⟧):", p. 184). The cause is visible in the EN: the inline math `$\approx` / `1$` is split across a line break (summaryEn.md l. 362–363), and the restore step did not match it. Join that EN math onto one line so a re-translation does not repeat it. "Измерена" agrees with nothing; the chapter elsewhere writes "Измерено".

### F09-B02 · S1 · English left in the running text, tables and one-pager
- **Where:** summaryBg.md §§ 9.1, 9.3, 9.4, 9.5, 9.6, 9.8; onePagerBg.md "Подход." and "Ключови резултати". (For "В single-agent RL (Глави 1 и 6)" see F09-C07; for "jSON artifacts" see F09-B12; for "smoke/scale config" see F09-B08.)
- **Now → Proposed:**
  - "нарушава предположението, което стои в основата на single-agent RL." → "нарушава предположението, на което се крепи едноагентното обучение с подкрепление."
  - "бихте могли да запаметите рутина, която им подхожда - това е single-agent RL." → "бихте могли да научите наизуст последователност от стъпки, която им подхожда - това е едноагентното обучение с подкрепление."
  - "| всеки агент изпълнява свое собствено single-agent RL, третирайки останалите като среда |" → "| всеки агент използва собствен алгоритъм за едноагентно обучение и третира останалите като част от средата |"
  - "**оценителят** на всеки агент вижда obs+действията на всички агенти по време на обучението; всеки **актьор** вижда само своите obs при изпълнение" → "**оценителят** на всеки агент вижда наблюденията и действията на всички агенти по време на обучението; всеки **актьор** вижда само собственото си наблюдение при изпълнение"
  - "обикновен PPO с **централизирана стойност** $V(\text{global state})$ и споделени параметри" → "обикновен PPO с **централизирана функция на стойността** $V(s)$ на глобалното състояние и споделени параметри"
  - "обикновен PPO с една централизирана функция на стойността $V(\text{global state})$ вместо на агент $V(o_i)$" → "обикновен PPO с една централизирана функция на стойността $V(s)$ на глобалното състояние вместо отделна $V(o_i)$ за всеки агент"
  - "| централизиран $Q(s,\text{joint }a)$ |" → "| централизиран $Q(s,a_1,\dots,a_N)$ |"
  - "**Stag Hunt** (две чисти равновесия на Наш - доминиращото по печалба (Stag, Stag) и рисково доминиращото (Hare, Hare) - плюс едно смесено)" → "**лов на елен** (две чисти равновесия на Наш - доминиращото по печалба (Елен, Елен) и рисково доминиращото (Заек, Заек) - плюс едно смесено)"
  - "| всички семена $\to$ (Hare, Hare) |" → "| всички начални числа $\to$ (Заек, Заек) |" ("семена": F07-B19)
  - "**рисково доминиращото** равновесие (Hare), вместо доминиращото по печалба (Stag), въпреки че Stag носи повече печалба - едностранен ход към Stag се наказва" → "**рисково доминиращото** равновесие (Заек), вместо доминиращото по печалба (Елен), въпреки че „Елен“ носи по-голяма печалба - едностранният ход към „Елен“ се наказва"
  - "Прогнозирах, че Matching Pennies ще проследи чиста орбита" → "Прогнозирах, че в „съвпадение на монети“ траекторията ще опише чиста орбита"
  - "съгласно Kuhn's Theorem (тъй като тези игри имат пълна памет)" → "съгласно теоремата на Кун (тъй като тези игри са с пълна памет)"
  - "| сближава се до Machine Zero |" → "| сближава се до машинна нула |"
  - "Класическата демонстрация е **Iterated Prisoner's Dilemma** с памет-1" → "Класическата демонстрация е **повтарящата се дилема на затворника** с памет 1"
  - "Наивни градиентни обучаеми, всеки максимизиращ собствената си възвръщаемост спрямо текущата стратегия на другия, сходява към взаимно предателство; **lOLA learners**, всеки отчитащ предстоящата актуализация на другия, достига взаимно сътрудничество." → "Наивните градиентни агенти, всеки от които максимизира собствената си възвръщаемост спрямо текущата стратегия на другия, стигат до взаимно предателство, докато агентите с **LOLA**, всеки от които отчита предстоящото обновяване на другия, достигат взаимно сътрудничество."
  - "; and Yu, C. et al. (2022)." → "; и Yu, C. et al. (2022)." (footnote `lowe2017`)
  - onePagerBg: "Експлоатируемостта → машинна нула при **Kuhn**" → "Експлоатируемостта → машинна нула при **Кун**"
  - onePagerBg: "при Kuhn **средният** итеративен NashConv пада до $0.24\to0.031$" → "при Кун NashConv на **средната** стратегия спада $0.24\to0.031$"
- **Why:** All of this prints (pp. 167–185). "single-agent", "obs", "global state", "joint", "Stag/Hare", "Matching Pennies", "Kuhn's Theorem", "Machine Zero", "Iterated Prisoner's Dilemma" and "lOLA learners" (with a mangled capital) are English in Bulgarian prose. Several come straight from settled glossary values (F09-T02). "сходява" after a plural subject is also an agreement error (F09-B17). The glossary rule is Kuhn → Кун. Replacing `\text{global state}` by $V(s)$ avoids Cyrillic inside `\text{}`.

### F09-B03 · S1 · meaning — self-play rendered as "независимо/самостоятелно обучение" and as "самообучение"
- **Where:** summaryBg.md § "Честни бележки…", § PSRO, § "Основни изводи"
- **EN:** "self-play converges in the average but not the last iterate" / "It unifies self-play, fictitious play, and the double-oracle method" / "Why a population and not just the last self-play policy? Because self-play converges in the *average*" / "fictitious-play self-play" / "Self-play/PSRO succeed in the average/population"
- **Now → Proposed:**
  - "самостоятелното обучение се сближава в средното, но не и в последната итерация" → "играта срещу себе си се сближава в средното, но не и в последната итерация"
  - "То обединява самообучението, фиктивната игра и метода на **двоен предсказвач**" → "То обединява играта срещу себе си, фиктивната игра и метода на **двойния оракул**"
  - "**Защо популация, а не просто последната стратегия от самообучението?** Защото самообучението се сближава в *средното*" → "**Защо популация, а не просто последната стратегия от играта срещу себе си?** Защото играта срещу себе си се сближава в *средното*"
  - "при фиктивна игра със самообучение" → "при фиктивна игра срещу себе си"
  - "- **Самообучението/PSRO успяват в средното/популацията, а не в последната итерация**" → "- **Играта срещу себе си и PSRO успяват чрез средното и популацията, а не чрез последната итерация**"
- **Why:** In this chapter "самостоятелно обучение" is the name of *independent learning* (§ 9.4). The § 9.9 sentence therefore tells the reader that independent learning converges in the average, which contradicts § 9.4. "самообучение" means self-study or self-supervised learning, not playing against oneself (F09-T08).

### F09-B04 · S1 · meaning — "three thesis hooks" rendered "три теза"
- **Where:** summaryBg.md chapter intro; § "Честни бележки…"
- **EN:** "It carries three thesis hooks." / "Forward: the three thesis hooks are now concrete"
- **Now → Proposed:**
  - "Тя съдържа три теза." → "Тя предлага три връзки с дисертацията."
  - "Напред: трите тези вече са конкретизирани" → "Напред: трите връзки с дисертацията вече са конкретни"
- **Why:** "три теза" is ungrammatical (the plural is "тези"). Even corrected, "three theses" says the chapter states three claims of the dissertation, which it does not. The source is the settled entry "thesis hooks → теза" (F09-T04).

### F09-B05 · S1 · meaning — *Defect* rendered "дефект / дефектиране / дефекция"
- **Where:** summaryBg.md §§ 9.4, 9.8, 9.9, 9.10; onePagerBg.md (the "Ловът на елени" sentence is in F09-B34)
- **EN:** "Defect strictly beats Cooperate, so the unique Nash is mutual Defect" / "(Defect)" / "cooperation emerges where naive learning defects" / "LOLA turns IPD defectors into cooperators" / "turns IPD defection into cooperation"
- **Now → Proposed:**
  - "(доминираща стратегия: дефектът строго превъзхожда сътрудничеството, така че уникалното равновесие е взаимен дефект)" → "(доминираща стратегия: предателството строго превъзхожда сътрудничеството, така че единственото равновесие е взаимно предателство)"
  - "| $x \to [0.001,\,0.999]$ (дефект) |" → "| $x \to [0.001,\,0.999]$ (предателство) |"
  - "там, където наивното обучение води до дефектиране" → "там, където наивното обучение води до предателство"
  - "и LOLA превръща дефектьорите в IPD сътрудници." → "и LOLA превръща предателството в повтарящата се дилема на затворника в сътрудничество."
  - "превръща дефекцията в IPD в кооперация" → "превръща предателството в IPD в сътрудничество"
  - onePagerBg: "*LOLA превръща дефекторите в кооператори.*" → "*LOLA превръща предателството в сътрудничество.*"
  - onePagerBg: "`1.04` (наивна дефекция) до `2.82` (кооперация с LOLA)" → "`1.04` (наивните агенти стигат до предателство) до `2.82` (сътрудничество с LOLA)"
- **Why:**
  - "дефект" means a flaw; "взаимен дефект" reads as "a mutual flaw". "сътрудници" means co-workers or employees.
  - The chapter itself writes "взаимно предателство" in § 9.8, and so does the figure mapping ("mutual defection (1)" → "взаимно предателство (1)").
  - "уникално" is a calque of *unique*: in Bulgarian it means "remarkable".
  - Source: the settled entry "defect → дефект" (F09-T03).

### F09-B06 · S1 · meaning — *hard-exploration* rendered "прекомерно изследване" (three places)
- **Where:** summaryBg.md § CTDE reconciliation, § "Честни бележки…" (4); onePagerBg.md "Честни отрицателни…"
- **EN:** "is **not sufficient** to overcome relative over-generalization plus the hard-exploration risk of the $-30$ penalties" / "does not by itself solve hard-exploration coordination"
- **Now → Proposed:**
  - "но това **не е достатъчно**, за да преодолее относителната свръхобобщеност плюс риска от прекомерно изследване на $-30$ санкциите - агентите няма да опитат" → "но това **не е достатъчно**, за да преодолее относителното свръхобобщаване и трудното изследване, което санкциите от $-30$ налагат - агентите няма да опитат"
  - "но сам по себе си не решава координация при риск от прекомерно изследване." → "но сам по себе си не решава координацията, когато изследването е трудно."
  - onePagerBg: "но сам по себе си не решава координацията при риск от прекомерно изследване." → "но сам по себе си не решава координацията, когато изследването е трудно."
- **Why:** The problem is the opposite of "excessive exploration": the −30 penalties make agents explore *too little* to find the 11. The settled entry is "hard-exploration coordination → координация при сложно проучване", so the text deviates from it as well. "относителна свръхобобщеност" names a state; the RL phenomenon is a process ("свръхобобщаване").

### F09-B07 · S1 · meaning — *greedy* and *ON* in the communication table
- **Where:** summaryBg.md § CommNet, table 31 (p. 184); § CTDE reconciliation
- **EN:** "| Channel | Greedy team reward |", "| communication ON |", "| communication OFF |", "Measured greedy rewards:"
- **Now → Proposed:**
  - "| Канал | Награда за отборна алчност |" → "| Канал | Отборна награда (алчна стратегия) |"
  - "| комуникация върху | $0.795$ |" → "| с комуникация | $0.795$ |"
  - "| изключена комуникация | $0.204$ |" → "| без комуникация | $0.204$ |"
  - "Измерени алчни награди:" → "Измерени награди при алчна стратегия:"
- **Why:**
  - "Награда за отборна алчност" means "a reward for team greed".
  - "комуникация върху" means "communication on top of".
  - Rewards are not greedy; the *policy* evaluated is.
  - Source: the settled entry "greedy team reward → награда за отборна алчност" (F09-T04).

### F09-B08 · S1 · English and calque — "smoke config" / "конфигурация на дима" / "в мащаб"
- **Where:** summaryBg.md § CTDE (methodological note), § CommNet, § "Честни бележки…"
- **EN:** "invisible at the fast "smoke" configuration … appeared only once trained at the larger "scale" configuration. The smoke config proves the code runs" / "Measured (scale config, $K=5$" / "at the smoke configuration both numbers were $0.24$ … only after training at scale" / "invisible at the fast smoke config and only emerged at scale, so the scale numbers are the ones the claims rest on"
- **Now → Proposed:**
  - "**невидими при бързата "smoke config"**" → "**невидими при бързата пробна конфигурация (smoke)**"
  - "Те се проявиха едва след обучение до сходимост при по-голямата "scale" конфигурация. Конфигурацията на дима показва, че кодът функционира;" → "Те се проявиха едва след обучение до сходимост в по-голямата, пълна конфигурация (scale). Пробната конфигурация показва, че кодът работи;"
  - "Измерено (конфигурация на мащаба, $K=5$, при което прагът на отгатваемост е $0.2$):" → "Измерено (пълна конфигурация, $K=5$, при което таванът при случайно отгатване е $0.2$):"
  - "обърнете внимание, че съгласуването от §5 важи и тук: при конфигурацията с дим и двете числа бяха $0.24$ (каналът все още не се беше научил да пренася информация), а ползата се появи едва след обучение в мащаб." → "обърнете внимание, че изводът от съпоставката в §5 важи и тук: при пробната конфигурация и двете числа бяха $0.24$ (каналът все още не се беше научил да пренася информация), а ползата се появи едва след обучението в пълната конфигурация."
  - "ефектите на невронните мрежи бяха невидими при бързата конфигурация на дима и се появиха едва в мащаб, така че именно числата за мащаба са тези, върху които почиват твърденията." → "ефектите при невронните мрежи бяха невидими при бързата пробна конфигурация и се появиха едва в пълната, така че твърденията почиват именно на числата от пълната конфигурация."
- **Why:** "конфигурация на дима / с дим" is a literal rendering of *smoke* (as in a smoke test) and reads as "the configuration of the smoke". The straight quotes around English words print on p. 179. The settled glossary already has "smoke-run → пробно изпълнение", so "пробна конфигурация" follows it.

### F09-B09 · S1 · meaning and stale — "последователността на стъпката"
- **Where:** summaryBg.md § "PSRO - теория на игрите…", first sentence
- **EN:** "The second structural fix is the through-line of the chapter and the direct descendant of Chapter 2's iterated best response."
- **Now → Proposed:** "Втората структурна корекция е последователността на стъпката и прекият наследник" → "Втората структурна корекция е водещата нишка на главата и прекият наследник"
- **Why:** "последователността на стъпката" means "the sequence of the step". *Through-line* is the thread that runs through the chapter, and "стъпка" is stale naming (F09-C09).

### F09-B10 · S1 · meaning — the § 9.9 heading says "this deal"
- **Where:** summaryBg.md heading (also in the bundle TOC, p. 186)
- **EN:** "## Honest notes, limitations, and where this hands off"
- **Now → Proposed:** "## Честни бележки, ограничения и къде това раздаване продължава нататък" → "## Честни бележки, ограничения и връзка със следващите глави"
- **Why:** "раздаване" is a poker deal. *Hands off* (passes on to what follows) was read as a noun "hand".

### F09-B11 · S1 · meaning — *time-average* rendered "усредненото време"
- **Where:** summaryBg.md § 9.4 reconciliation, "е *усредненото време* (§6)"
- **EN:** "the thing that converges is the *time-average* (§6)"
- **Now → Proposed:** "е *усредненото време* (§6)" → "е *средното по времето* (§6)"
- **Why:** "усредненото време" means "the averaged time". What converges is the strategy averaged over time. Source: the settled entry "time-average → Усреднено време" (F09-T09).

### F09-B12 · S1 · English and calque — "ангажираните jSON artifacts"
- **Where:** summaryBg.md § "Честни бележки…", paragraph "**Доверие.**"
- **EN:** "The experiment PNGs cited above are generated from the committed JSON artifacts (see `../figures/README.md`); a few were not saved on the run and are marked "to close.""
- **Now → Proposed:** "PNG изображенията на експериментите, цитирани по-горе, са генерирани от ангажираните jSON artifacts (виж `../figures/README.md`); няколко от тях не бяха запазени при изпълнението и са маркирани като „за затваряне“." → "Графиките на експериментите по-горе са генерирани от JSON файловете с резултати, записани в хранилището (вж. `../figures/README.md`)."
- **Why:** "ангажираните" (engaged, committed to a cause) is a calque of git's *committed*. "jSON artifacts" is English with a mangled capital. "виж" is the imperative; the abbreviation for "see" is "вж.". The second clause is stale (F09-C10).

### F09-B13 · S2 · system name and meaning — "commNet" and "научен канал"
- **Where:** summaryBg.md § 9.3 (two places), § 9.7 heading and text; bundle TOC and p. 183
- **EN:** "CommNet centralizes *information at execution* through a learned channel" / "(CommNet, 2016)" / "## Learned communication (CommNet)" / "In **CommNet** (Sukhbaatar et al., 2016)"
- **Now → Proposed:**
  - "commNet централизира *информация по време на изпълнение* чрез научен канал" → "CommNet централизира *информацията по време на изпълнение* чрез канал, който агентите сами научават"
  - "(commNet, 2016)" → "(CommNet, 2016)"
  - "## Научена комуникация (commNet)" → "## Научена комуникация (CommNet)"
  - "В **commNet** (Sukhbaatar и др., 2016)" → "В **CommNet** (Sukhbaatar и др., 2016)"
- **Why:** The system name is CommNet; the lower-case "c" is a pipeline artefact and prints in the TOC. The masculine participle "научен" is identical to the adjective "научен" (*scientific*), so "научен канал" reads first as "scientific channel".

### F09-B14 · S2 · meaning — *guessing ceiling* rendered "праг на отгатваемост"; "научен протокол"
- **Where:** summaryBg.md §§ 9.7, 9.9; onePagerBg.md "Ключови резултати" (the § 9.7 "Измерено (…)" line is in F09-B08)
- **EN:** "learned communication lifts the listener above the guessing ceiling" / "*Communication clears the guessing ceiling.*" / "(ceiling 1/K = 0.2) — a learned, not designed, protocol"
- **Now → Proposed:**
  - "научената комуникация издига слушателя над прага на отгатваемост;" → "научената комуникация издига слушателя над тавана при случайно отгатване;"
  - onePagerBg: "*Комуникацията премахва прага на отгатваемост.*" → "*Комуникацията надхвърля тавана при случайно отгатване.*"
  - onePagerBg: "(праг 1/K = 0.2) - научен, а не проектиран протокол." → "(таван 1/K = 0.2) - протокол, който агентите научават, а не който някой е проектирал."
- **Why:** "праг" is a threshold (a floor to cross), and the same paragraph already says "над тавана от $1/K$". "отгатваемост" (guessability) is not the meaning. "премахва" says the ceiling disappears, but it is exceeded. "научен протокол" reads as "scientific protocol" (F09-B13).

### F09-B15 · S2 · terminology — "двуигрови" (not a word) and "Нашева стратегия"
- **Where:** summaryBg.md intro, § 9.2, § 9.9; onePagerBg.md "Проблем." and "Връзка с дисертацията." (for "Глави 2–8 съществуват изцяло…" see F09-C07)
- **EN:** "every two-player guarantee" / "in two-player zero-sum a Nash strategy guarantees $v^*$" / "a Nash strategy secures a value"
- **Now → Proposed:**
  - "Мястото, където всяка двуигрова гаранция се нарушава" → "Мястото, където се нарушава всяка гаранция за игри с двама играчи"
  - "в двуигрови игра с нулева сума Нашева стратегия гарантира $v^*$ срещу всеки противник" → "в игра за двама с нулева сума равновесната стратегия на Наш гарантира $v^*$ срещу всеки противник"
  - "единственото място, където всяка двуигрова гаранция от Глави 2–8 престава да бъде валидна." → "единственото място, където престава да важи всяка гаранция за игри с двама играчи от глави 2–8."
  - onePagerBg: "Глави 2–8 се развиваха в рамките на двуигрови игри с нулева сума, където една Нашева стратегия осигурява стойност" → "Глави 2–8 се развиваха в рамките на игри за двама с нулева сума, където равновесната стратегия на Наш осигурява стойност"
  - onePagerBg: "а мястото, където всяка двуигрова гаранция престава да важи" → "а мястото, където престава да важи всяка гаранция за игри с двама играчи"
- **Why:** "двуигров" is not Bulgarian, and "двуигрови игра" also breaks number agreement. The settled glossary itself has "two-player zero-sum → игра за двама с нулева сума"; the stray entry "two-player → двуигрови" (F09-T05) overrides it. "Нашева" is the unusual adjective of F07-T13.

### F09-B16 · S2 · meaning — "наш / нашово / Нашово" for Nash (F07-B02 pattern)
- **Where:** summaryBg.md intro, § 9.4 reconciliation; onePagerBg.md "Ключови резултати" (the "Нашовото равновесие" of the open questions is in F09-B34)
- **Now → Proposed:**
  - "(наш равновесия, точни стойности на най-добър отговор)" → "(равновесия на Наш, точни стойности на най-добрия отговор)"
  - "измереното разстояние до нашово равновесие нарасна" → "измереното разстояние до равновесието на Наш нарасна"
  - onePagerBg: "То се сближава към Нашово равновесие при" → "То се сближава към равновесие на Наш при"
  - onePagerBg: "разстоянието ѝ до Нашово равновесие всъщност *нараства*" → "разстоянието ѝ до равновесието на Наш всъщност *нараства*"
- **Why:** "наш равновесия" reads as "our equilibria", and "нашов" is not a word (F07-B02). The concept is "равновесие на Наш" (glossary).

### F09-B17 · S2 · grammar — "сходява / сходи / сходяват" (not a Bulgarian verb)
- **Where:** summaryBg.md §§ 9.1, 9.4 (table and text), 9.4 reconciliation, footnote `singh2000`. The LOLA sentence is in F09-B02.
- **Now → Proposed:**
  - "към която агентът сходява." → "към която агентът да се сближава."
  - "| **не сходява** (последната итерация се отклонява към границата) |" → "| **не се сближава** (последната итерация се отклонява към границата) |"
  - "Три от четирите игри сходяват към истинско равновесие на Наш" → "В три от четирите игри агентите се сближават с истинско равновесие на Наш"
  - "тя **никога не сходи към равновесие**" → "тя **никога не се сближава с равновесие**"
  - "и двамата не успяха да **сходяват**" → "и двамата не успяха да **се сближат с равновесие**"
  - "не сходи към равновесие в игра само със смесено равновесие - това, което сходи," → "не се сближава с равновесие в игра само със смесено равновесие - това, което се сближава,"
  - "анализът защо изкачването по градиент циклира, вместо да се сходи в игри като игра „хвърляне на монета“." → "анализ на това защо градиентното изкачване циклира, вместо да се сближи с равновесие, в игри като „съвпадение на монети“."
- **Why:** "сходява" does not exist (F07-B03 found it in chapter 7 as well). The chapter itself uses "се сближава" in §§ 9.6 and 9.9, so this also unifies the term. "Три от четирите игри сходяват" makes the *games* converge. Source: settled "converge → Сходява" (F09-T01).

### F09-B18 · S2 · meaning — Matching Pennies rendered "хвърляне на монета" (a coin toss)
- **Where:** summaryBg.md §§ 9.1, 9.4 (text and table), 9.6 table, 9.9 (twice), 9.10; onePagerBg.md "Ключови резултати" (the footnote is in F09-B17, the reconciliation in F09-B02)
- **Now → Proposed:**
  - "(както в игра „хвърляне на монета“, §4)" → "(както в „съвпадение на монети“, §4)"
  - "**игра „хвърляне на монета“** (игра с нулева сума; уникалното равновесие е напълно смесената $(\tfrac12,\tfrac12)$ със стойност 0)" → "**„съвпадение на монети“** (игра с нулева сума; единственото равновесие е напълно смесеното $(\tfrac12,\tfrac12)$ със стойност 0)"
  - "| игра „хвърляне на монета“ | **не сходява**" → "| „съвпадение на монети“ | **не сходява**" (apply before F09-B17's table change, or merge both)
  - "Играта „хвърляне на монета“ е показателна" → "Играта „съвпадение на монети“ е показателна"
  - "| матрица (игра „хвърляне на монета“) |" → "| матрична игра („съвпадение на монети“) |"
  - "*се проваля* при игра „хвърляне на монета“;" → "*се проваля* в „съвпадение на монети“;"
  - "(1) Игра „хвърляне на монета“ се отклонява към границата" → "(1) В „съвпадение на монети“ траекторията се отклонява към границата"
  - "- играта „хвърляне на монета“ се разминава, независимо колко дълго тренирате." → "- в „съвпадение на монети“ последната итерация не се сближава, колкото и дълго да продължи обучението."
  - onePagerBg: "но **игра „хвърляне на монета“ никога не се сближава**" → "но **в „съвпадение на монети“ обучението никога не се сближава**"
- **Why:** "хвърляне на монета" is a coin toss, a chance device, while Matching Pennies is a two-player game in which each player *chooses* a side. The two are not the same. No established Bulgarian name was found (web search), so a descriptive name is proposed; add "(Matching Pennies)" at the first use in § 9.4. "уникалното" is a calque, and "напълно смесената" does not agree with "равновесие". "се разминава" means "miss each other" (F09-T09). "тренирате" is colloquial for training. Source: settled "matching pennies → игра „хвърляне на монета“" (F09-T06).

### F09-B19 · S2 · terminology — *oracle* rendered "предсказвач"
- **Where:** summaryBg.md table 27, § 9.6 (three places), § 9.9, footnote `lanctot2017`; onePagerBg.md "Подход." (the "двоен предсказвач" of § 9.6 is in F09-B03, the one-pager's open question in F09-B34)
- **Now → Proposed:**
  - "пълен най-добър отговор на рунд; приблизителен предсказвач отслабва гаранцията" → "пълен най-добър отговор във всеки кръг; приблизителният оракул отслабва гаранцията"
  - "обучава **най-добър отговор** (предсказвач)" → "обучава **най-добър отговор** (оракул)"
  - "Първо, предсказвачът използва повторно" → "Първо, оракулът използва повторно"
  - "с точен предсказвач;" → "с точен оракул;"
  - "(методът на двойния предсказвач, който PSRO обобщава)" → "(методът на двойния оракул, който PSRO обобщава)"
  - onePagerBg: "(мета-Наш + предсказвач за най-добър отговор)" → "(мета-Наш + оракул за най-добър отговор)"
  - onePagerBg: "както като предсказвач, така и като метрика за експлоатируемост" → "както като оракул, така и като мярка за експлоатируемост"
- **Why:** An *oracle* here is a subroutine that returns a best response on request, not something that predicts. "оракул" is the established Bulgarian term in computer science ("машина с оракул"). Source: both glossaries (F09-T07). "рунд" vs "кръг": the PSRO table uses "кръг".

### F09-B20 · S2 · terminology — *policy* rendered "политика" and *population* "съвкупност", against the curated glossary
- **Where:** summaryBg.md §§ 9.1, 9.2, table 27, § 9.6 heading; onePagerBg.md "Подход." (the table-27 PSRO cell is in F09-B28)
- **Now → Proposed:**
  - "зависят от политиките $\pi_{-i}$ на другите агенти" → "зависят от стратегиите $\pi_{-i}$ на другите агенти"
  - "Какво преминава през моста е *речникът*. Политиката все още съпоставя" → "Това, което преминава през моста, е *речникът*. Стратегията все още съпоставя"
  - "е точно политиката на марковска игра $\pi_i(a_i\mid o_i)$" → "е точно стратегията в марковската игра $\pi_i(a_i\mid o_i)$"
  - "и го подава в своята политика" → "и го подава на входа на своята стратегия"
  - "## PSRO - теория на игрите върху съвкупност от политики" → "## PSRO - теория на игрите върху популация от стратегии"
  - onePagerBg: "*популация* от политики" → "*популация* от стратегии"
- **Why:** `terminology_EN_BG.md` fixes "Policy → Стратегия" ("In RL context, „стратегия" is standard in BG"), and the rest of the chapter follows it. "Какво преминава … е" is an English cleft; a Bulgarian subject clause needs "Това, което…". The heading's "съвкупност" clashes with "популация" used everywhere else, including the figure.

### F09-B21 · S2 · terminology — *independent learning* rendered "самостоятелно" next to "независим"
- **Where:** summaryBg.md table 27, § 9.4 heading and text, table 28 caption, § 9.9; onePagerBg.md (twice)
- **Now → Proposed:**
  - "| **Самостоятелно обучение (IL)** |" → "| **Независимо обучение (IL)** |"
  - "## Самостоятелно обучение и неговите режими на провал" → "## Независимо обучение и начините, по които то се проваля"
  - "При самостоятелното обучение всеки агент се поставя" → "При независимото обучение всеки агент се поставя"
  - ": Самостоятелно обучаващи се агенти върху четири матрични игри, спрямо аналитичното равновесие на Наш." → ": Независими обучаващи се агенти в четири матрични игри, сравнени с аналитичното равновесие на Наш."
  - "самостоятелното обучение се сближава при доминиращи/координационни игри" → "независимото обучение се сближава в игрите с доминираща стратегия и в координационните игри"
  - onePagerBg: "**Самостоятелно обучение** (контролният вариант, който се проваля)" → "**Независимо обучение** (контролният вариант, който се проваля)"
  - onePagerBg: "*Самостоятелното обучение се проваля точно там, където теорията предсказва.*" → "*Независимото обучение се проваля точно там, където го предвижда теорията.*"
- **Why:** The same chapter writes "независими обучаващи агенти", "независим оценител", and fig. 46 prints "Независимо обучение". "Самостоятелно обучение" means self-study, and it led to the self-play mix-up in F09-B03. "режими на провал" is a calque of *failure modes*. "доминиращи игри" says the games dominate.

### F09-B22 · S2 · terminology — *learner* rendered "обучаем" (trainable); "проектиран градиент"
- **Where:** summaryBg.md §§ 9.4, 9.4 reconciliation, 9.10 (the "лов на елен" sentence is in F09-B02, the BoS sentence in F09-C12)
- **Now → Proposed:**
  - "Изпълнението на двама независими градиентни учещи се (с точни градиенти, така че динамиката е чиста и безшумна) дава, измерено:" → "Два независими градиентни агента (с точни градиенти, така че динамиката е чиста и без шум) дават следните измерени резултати:"
  - "Двама обучаеми, пуснати по два начина," → "Два вида обучаващи се агенти,"
  - "Обучаемият с проектиран градиент (IGA), използван в скриптовете за изследване," → "Агентът с градиентен метод с проекция (IGA), използван в изследователските скриптове,"
  - "Обучаемият със softmax-logit, използван в имплементацията," → "Агентът със softmax параметризация, използван в имплементацията,"
  - "- **LOLA преформулира противника като обучаем**" → "- **LOLA разглежда противника като учещ се агент**"
- **Why:** "обучаем" means *trainable/teachable*. For LOLA it says the opponent can be taught, which is not the claim. The chapter uses four words for *learner* ("обучаеми", "учещи се", "обучаващи се агенти", "учащ се"). "проектиран" reads as "designed" (F07-T10). "Двама обучаеми, пуснати по два начина" misreads the EN: it means two kinds of learner, not two runs.

### F09-B23 · S2 · meaning — the reconciliation boxes: "Съгласуване (запази прогнозата …)"
- **Where:** summaryBg.md §§ 9.4, 9.5, 9.6 (two boxes); chapter intro (the § 9.7 cross-reference is in F09-B08)
- **EN:** "**Reconciliation (kept prediction $\to$ what actually happened).**" / "**Reconciliation 1 (Leduc).**" / "I keep the original expectation and reconcile it with what happened"
- **Now → Proposed:**
  - "**Съгласуване (запази прогнозата $\to$ за това какво всъщност се случи).**" → "**Съпоставка (запазена прогноза $\to$ какво всъщност се случи).**"
  - "**Съгласуване (запази прогноза $\to$ какво всъщност се случи).**" → "**Съпоставка (запазена прогноза $\to$ какво всъщност се случи).**"
  - "**Съгласуване 1 (Ледюк).**" → "**Съпоставка 1 (Ледюк).**"
  - "**Съгласуване 2 (Goofspiel $K=4$).**" → "**Съпоставка 2 (Goofspiel $K=4$).**"
  - "запазвам първоначалното предварително убеждение и го съгласувам с получения резултат" → "запазвам първоначалното очакване и го съпоставям с получения резултат"
- **Why:**
  - "запази" is an imperative ("keep!"), whereas *kept* is a participle.
  - "Съгласуване" means coordination or agreement, and it collides with "съгласуван" for *consistent* (F07-T05). What the box does is compare a prediction with a result.
  - "предварително убеждение" (the *prior* of Bayes, F07-T04) is wrong for a plain "expectation".
  - Source: settled "reconciliation → съгласуване" (F09-T10).

### F09-B24 · S2 · calque — "по-нисък дисперсионен учител"
- **Where:** summaryBg.md § CTDE; onePagerBg.md "Ключови резултати"
- **EN:** "so it is a far lower-variance teacher" / "*A centralized critic is a near-zero-variance teacher.*"
- **Now → Proposed:**
  - "така че той е значително по-нисък дисперсионен учител." → "затова дава обучаващ сигнал със значително по-ниска дисперсия."
  - onePagerBg: "*Централизиран оценител е почти нулев дисперсионен учител.*" → "*Централизираният оценител дава обучаващ сигнал с почти нулева дисперсия.*"
- **Why:** "по-нисък … учител" reads as "a shorter teacher". "почти нулев … учител" reads as "an almost-zero teacher". For the content caveat see F09-C04.

### F09-B25 · S2 · grammar and terminology — § 9.2 "Марковски игри"
- **Where:** summaryBg.md § "Марковски игри - мостът между глави 2–8 и MARL" (for "Какво преминава…" see F09-B20; for the CFR sentence see F09-C03)
- **Now → Proposed:**
  - "**множества информация**, групиращи истории" → "**информационни множества**, които групират истории"
  - "подавани към решавач за съжаление (CFR)" → "подавани към алгоритъм за минимизиране на съжалението (CFR)"
  - "Глава 9 разсъждава върху **Марковски (стохастични) игри**" → "Глава 9 разсъждава върху **марковски (стохастични) игри**"
  - "Двете се свързват чисто и изясняването" → "Двете се свързват естествено и изясняването"
  - "Една **Марковска игра** е наредената n-торка" → "**Марковската игра** е наредената n-торка"
  - "награди на агент $R_i(s,a_1,\dots,a_N)$" → "наградите на отделните агенти $R_i(s,a_1,\dots,a_N)$"
  - "- Последователна игра с **непълна информация** и **игра с нулева сума** дава **EFG** (Глави 2–8): Markov игра, при която" → "- Последователна игра с непълна информация и нулева сума дава **EFG** (глави 2–8): марковска игра, при която"
  - "фактът, който направи безопасната експлоатация в Глава 8 последователна" → "фактът, на който се крепи безопасната експлоатация в Глава 8"
  - "Тази липсваща котва е точната празнина, която Принос #2 наследява." → "Именно тази липсваща опора е празнината, която наследява Принос №2."
- **Why:**
  - "множества информация" breaks the glossary term used two sentences later ("информационно множество").
  - "решавач за съжаление" means "a solver for regret (sorrow)".
  - Adjectives from names are lower case in Bulgarian ("марковски"); the chapter mixes cases.
  - "игра с нулева сума" inside the list makes it "a sequential game and a zero-sum game".
  - "Markov игра" is English.
  - "последователна" means *sequential/consistent*, not *coherent*.
  - "Принос #2" breaks the chapter's "№" style.

### F09-B26 · S2 · calque — chapter intro
- **Where:** summaryBg.md, intro paragraphs before § 9.1 (for "Глави 2–8 съществуват изцяло…" see F09-C07; for the PSRO sentence see F09-C08; for "три теза" see F09-B04)
- **EN:** "This is a ground-up chapter on multi-agent reinforcement learning" / "bounded … by *exact* analytical references" / "the moving-target complement to Chapter 7's static read" / "named here and left open for the thesis to attack"
- **Now → Proposed:**
  - "Тази глава е изградена от основи върху многоагентното обучение с подкрепление (MARL):" → "Тази глава въвежда от самото начало многоагентното обучение с подкрепление (MARL):"
  - "са ограничени от *точни* аналитични препратки" → "са поставени в *точни* аналитични граници" (F07-B11)
  - "допълнение към статичното четене от Глава 7 (Принос №1)" → "допълнение към статичната преценка за противника от Глава 7, насочено към противник, който се променя (Принос №1)"
  - "е назовано тук и оставено отворено за атака от дисертацията." → "е назовано тук и оставено като отворен проблем, към който е насочена дисертацията."
- **Why:**
  - "изградена от основи върху" is ungrammatical.
  - "препратки" means cross-references.
  - Poker *read* is not "четене" (F07-B30).
  - The BG drops *moving-target*, the point of the comparison.
  - "атака от дисертацията" is a calque of *attack*.

### F09-B27 · S2 · grammar and calque — § 9.1 dance paragraph and coordination question
- **Where:** summaryBg.md § "Защо многоагентното обучение с подкрепление е различен проблем" (the "рутина" and "single-agent RL" sentence is in F09-B02)
- **Now → Proposed:**
  - "(как си сътрудничещите агенти се учат да действат заедно, без да им бъде казано как?)" → "(как агентите, които си сътрудничат, се научават да действат заедно, без някой да им казва как?)"
  - "Картина, която да запомните:" → "Образ, който си струва да запомните:"
  - "докато или не се заключите в споделен ритъм (координирано равновесие), или циклирате завинаги" → "докато или не намерите общ ритъм (координирано равновесие), или не започнете да се въртите в кръг безкрайно"
- **Why:** "как си сътрудничещите агенти" misplaces the clitic and does not parse. "Картина" is a calque of *picture* (F07-B01). "да се заключите в" is a calque of *lock into*. The "или не …, или …" pair is broken.

### F09-B28 · S2 · calque and grammar — table 27 and § 9.3 text
- **Where:** summaryBg.md table 27 (pp. 170–171) and the paragraph after it (for "single-agent RL" and "obs" see F09-B02; for the CommNet sentence see F09-B13)
- **Now → Proposed:**
  - "| бърза базова линия; почти стационарни настройки | нестационарност $\to$, цикличност, координационен провал |" → "| бърза базова линия; почти стационарни среди | нестационарност $\to$ цикличност, провал на координацията |"
  - "| цена на on-policy извадката; „прост“, но чувствителен към настройка |" → "| висока цена на данните при обучение по текущата стратегия (on-policy); „прост“, но чувствителен към настройката |"
  - "| поддържайте съвкупност от политики; решавайте **мета-Наш** върху нея; обучете **най-добър отговор** към тази смес; добавете го; повторете |" → "| поддържа популация от стратегии; намира **мета-Наш** сместа върху нея; обучава **най-добър отговор** на тази смес; добавя го; цикълът се повтаря |"
  - "| оптимизирайте, приемайки, че противникът прави **една стъпка на обучение**; диференцирайте *през* неговото обновяване | 2-играч диференцируеми игри, където наивното обучение се проваля (IPD) |" → "| оптимизира, като приема, че противникът ще направи **една стъпка на обучение**; диференцира *през* неговото обновяване | диференцируеми игри с двама играчи, в които наивното обучение се проваля (IPD) |"
  - "| средното обединяване изхвърля *кой* какво е казал |" → "| усредняването губи информацията *кой* какво е казал |"
  - "като фиксирана, докато ти отговаряш;" → "като фиксирана, докато агентът ѝ отговаря;"
- **Why:**
  - "настройки" means configuration settings.
  - The stray comma after $\to$ leaves the arrow pointing at nothing (p. 170).
  - The PSRO cell mixes imperfective and perfective imperatives ("поддържайте … обучете"); a "Какво прави" column reads naturally in the 3rd person.
  - "2-играч" is ungrammatical.
  - "ти" breaks the formal "вие" register of the rest of the chapter.

### F09-B29 · S2 · meaning — table 28 header, "уникално", "намаляваща"
- **Where:** summaryBg.md § 9.4 table 28 (p. 173); § 9.6 reconciliation 2
- **EN:** "| Game | Measured outcome | NashConv | Matches analytic Nash? |" / "I predicted non-increasing exploitability."
- **Now → Proposed:**
  - "| Игра | Измерено равновесие | NashConv |" → "| Игра | Измерен резултат | NashConv |"
  - "Прогнозирах намаляваща експлоатируемост." → "Прогнозирах ненарастваща експлоатируемост."
- **Why:** In the Matching Pennies row there is no equilibrium to report, which is the row's point. "намаляваща" (*decreasing*) is a stronger prediction than *non-increasing*, which allows plateaus. (For "уникалното" see F09-B05 and F09-B18.)

### F09-B30 · S2 · calque — § 9.5 CTDE
- **Where:** summaryBg.md § "Централизирано обучение, децентрализирано изпълнение (CTDE)" (for "Измерени алчни награди" see F09-B07; for "прекомерно изследване" see F09-B06)
- **Now → Proposed:**
  - "като същевременно предоставя на *обучаващия* привилегирован изглед по време на обучение" → "като същевременно дава на *обучаващия се агент* привилегирован достъп до информация по време на обучение"
  - "централизираният оценител, обусловен върху всичко, вижда целева стойност" → "централизираният оценител, който отчита цялата информация, вижда целева стойност"
  - "Измерено върху едностъпкова кооперативна „референтна“ задача (говорителят вижда целта, слушателят не, и двамата трябва да я назоват), обучено до сходимост:" → "Измерено в едностъпкова кооперативна „референциална“ задача (говорителят вижда целта, слушателят - не, а двамата трябва да я назоват), след обучение до сходимост:"
  - "| Оценител | Краен остатък (загуба на стойност) |" → "| Оценител | Краен остатък (грешка на функцията на стойността) |"
  - ": Централизиран срещу самостоятелен оценител: краен остатък от загубата на стойност." → ": Централизиран срещу независим оценител: краен остатък на грешката на функцията на стойността."
  - "Прогнозирах, че в **изкачващата се игра** на Claus–Boutilier" → "Прогнозирах, че в играта **„изкачване“** на Claus и Boutilier"
  - "Честният прочит:" → "Честното тълкуване:"
  - "Резултатът на MADDPG под нивото на IL конкретно посочва неговото дискретно контрафактично актьорско обновяване с базова линия като частта, която трябва да бъде разгледана следваща." → "Това, че MADDPG остава под IL, насочва вниманието към дискретното обновяване на актьора с контрафактична базова линия - то трябва да бъде проверено първо."
  - "**CTDE купува по-добър оценител, но не и автоматична координация.**" → "**CTDE осигурява по-добър оценител, но не и автоматична координация.**"
  - "в референтната задача говорещият" → "в референциалната задача говорителят"
- **Why:**
  - "изглед" is a view, as of scenery.
  - "обусловен върху" is a calque of *conditioned on*.
  - "референтна" means *reference/benchmark*, but a *referential* task is one of naming a referent.
  - "загуба на стойност" means depreciation (F09-T11).
  - "изкачващата се игра" is "the game that is climbing". The chapter's own § 9.9 says "играта „изкачване“".
  - "купува" is a calque of *buys*.
  - The MADDPG sentence is a noun pile.
  - "говорителят/говорещият" are two words for one role.

### F09-B31 · S2 · calque — § 9.6 PSRO
- **Where:** summaryBg.md § PSRO (the first sentence is in F09-B09; oracle terms in F09-B19; self-play in F09-B03)
- **Now → Proposed:**
  - "изгражда емпиричната **мета-игра** матрица на печалбата между популациите" → "изгражда емпиричната матрица на печалбите на **мета-играта** между популациите"
  - "и добавя този отговор към популацията - повтори." → "и добавя този отговор към популацията; цикълът се повтаря."
  - "| Игра | Траектория на експлоатируемостта | Присъда |" → "| Игра | Траектория на експлоатируемостта | Извод |"
  - "*скоростта* е мащабиращата пречка" → "*скоростта* е стената на мащабиране"
  - "за да апроксимира плътно неговия смесен Наш." → "за да приближи добре неговото смесено равновесие на Наш."
  - "позволява директното прилагане на двигателя за точен най-добър отговор." → "позволява модулът за точен най-добър отговор да се приложи директно."
- **Why:**
  - "мета-игра матрица" is a noun pile.
  - "повтори" is an imperative inside 3rd-person narration.
  - "Присъда" is a court sentence.
  - "мащабиращата" is an active participle ("the one that scales"), and the chapter elsewhere says "стена на мащабиране".
  - "двигател" is a calque of software *engine*.

### F09-B32 · S2 · meaning — § 9.8 LOLA
- **Where:** summaryBg.md § "LOLA - моделиране на опонента като учащ се" (for "през тази глава" see F09-C01; the "~2.9" sentence is in F09-C11)
- **Now → Proposed:**
  - "сътрудничеството произтича конкретно от втория ред на члена за **предвиждане**." → "сътрудничеството произтича именно от члена за **предвиждане** от втори ред."
  - "LOLA предвижда тяхната *обучителна траектория*. Комбинирането на двете - статично четене, което задейства динамично предвиждане - е кандидат" → "LOLA предвижда неговата *траектория на обучение*. Съчетаването на двете - статична преценка, която задава началото на динамичното предвиждане - е кандидат"
- **Why:** "от втория ред на члена" means "from the second row of the term". *Second-order* describes the term. "тяхната" does not agree with the singular "противника". "четене" is F07-B30. "задейства" (triggers) misreads *seeds*.

### F09-B33 · S2 · calque — §§ 9.9–9.10
- **Where:** summaryBg.md § "Честни бележки…", § "Основни изводи…"
- **Now → Proposed:**
  - "Четири честни уговорки се пренасят напред." → "Четири честни уговорки остават в сила и за следващите глави."
  - "**Обратни и бъдещи връзки.** Обратно:" → "**Връзки с предходните и следващите глави.** Назад:"
  - "- **Нестационарността е *основният проблем*, и тя е структурна, а не въпрос на изчислителна мощност**" → "- **Нестационарността е *основният проблем* и тя е структурна, а не въпрос на изчислителен бюджет**"
  - "- **PSRO е мостът между теорията на игрите ↔ MARL**" → "- **PSRO е мостът между теорията на игрите и MARL**"
  - "а RPS - до равномерност;" → "а RPS - до равномерна смес;"
  - "- **Минимаксната разлика $N>2$ е отворената врата към дисертацията** (Принос №2): речникът на глави 2–8 преминава в MARL, но предпазният ограничител не." → "- **Липсата на минимаксна стойност при $N>2$ е отворената врата към дисертацията** (Принос №2): речникът на глави 2–8 преминава в MARL, но опората на безопасността - не."
- **Why:**
  - "се пренасят напред" is a calque of *travel forward*.
  - "Обратно:" reads as "Conversely:".
  - "изчислителна мощност" is hardware power (F07-T12).
  - "мостът между X ↔ Y" doubles the relation.
  - "разлика" is a numeric difference, not a *gap*.
  - The same anchor is "котва" in §§ 9.1/9.2/9.9 and "предпазен ограничител" here (settled "safety anchor → предпазен ограничител").

### F09-B34 · S2 · one-pager — title, calques, grammar, meaning
- **Where:** onePagerBg.md
- **EN:** "# Chapter 9 One-Pager — Multi-Agent Reinforcement Learning" / "Build and compare the field's four structural answers to non-stationarity" / "and a native Goofspiel" / "Prisoner's Dilemma (defection), Stag Hunt (the risk-dominant corner), and Battle of the Sexes" / "(a contradicted prediction, §9 of the report)" / "*Honest negatives (kept predictions, §9).*" / "**Thesis connection.**" / "LOLA is *dynamic* opponent modeling, the moving-target complement to Chapter 7's static read" / "Can an approximate (RL) oracle push Leduc PSRO close to Nash, and at what cost to the guarantee?"
- **Now → Proposed:**
  - "# Глава 9 Резюме - Обучение с подкрепление за множество агенти" → "# Глава 9 Резюме - Многоагентно обучение с подкрепление" (and the same in `title:`)
  - "Изграждане и сравняване на четирите структурни отговора на полето на нестационарност" → "Изграждане и сравняване на четирите структурни отговора, които областта дава на нестационарността,"
  - "върху Kuhn, Ледюк, матрична игра и родна Goofspiel" → "върху Кун, Ледюк, матрична игра и собствена реализация на Goofspiel"
  - "при Дилемата на затворника (дефекция), Ловът на елени (рисково доминиращият ъгъл) и Битката на половете" → "при дилемата на затворника (предателство), лова на елен (рисково доминиращия ъгъл) и битката на половете"
  - "(противоречиво предсказание, §9 от доклада)" → "(опровергано предсказание, §9 от доклада)"
  - "*Честни отрицателни (запазени предсказания, §9).*" → "*Отрицателни резултати, запазени честно (опровергани предсказания, §9 от доклада).*"
  - "достига скалираща стена" → "достига стената на мащабиране"
  - "Връзка с дисертацията. PSRO представлява" → "**Връзка с дисертацията.** PSRO представлява"
  - "LOLA е *динамично* моделиране на противника - допълнение към статичното четене от Глава 7, насочено към движеща се цел (Принос №1)" → "LOLA е *динамично* моделиране на противника - насочено към движеща се цел допълнение към статичната преценка за противника от Глава 7 (Принос №1)"
  - "Може ли приблизителен (RL) предсказвач да доближи Ледюк PSRO до Нашовото равновесие и каква е цената на тази гаранция?" → "Може ли приблизителен (RL) оракул да доближи PSRO в Ледюк до равновесието на Наш и доколко това отслабва гаранцията?"
- **Why:**
  - The title differs from the chapter's own title ("Многоагентно обучение…").
  - "отговора на полето на нестационарност" means "answers of the field of non-stationarity" (a pitch).
  - "родна" means *home-born*, whereas *native* here means "implemented in-house".
  - "Ловът … Битката" wrongly carry the subject article after "при", and "Елени" is plural against the glossary's "лов на елен".
  - "противоречиво" means *self-contradictory*.
  - "Честни отрицателни" has no noun.
  - The paragraph label lost its bold (the other three are bold).
  - In the LOLA sentence "насочено към движеща се цел" attaches to Chapter 7's *static* read, which inverts the point.
  - "цената на тази гаранция" means "the price of the guarantee", but the EN asks how much the guarantee is weakened.

### F09-B35 · S3 · typography — "Глава 07", "виж", "Принос #"
- **Where:** summaryBg.md "Глава 07" (3×: § 9.6 "от Глава 07 за игрите", § 9.9 "от Глава 07 за Кун", "от Глава 07;"); onePagerBg.md "от Глава 07 както"
- **Now → Proposed:** "Глава 07" → "Глава 7" (all four)
- **Why:** The chapter elsewhere writes "Глава 7"; a zero-padded chapter number is a file-name convention. The same in the EN ("Chapter 07's", 4× + one-pager).

## T — Glossary-level terminology

### F09-T01 · S1 · "converge → Сходява"
- **Where:** `llmPipeline/glossary_settled.md` (freq 4). "сходява/сходи/сходяват" occur in the BG summaries of chapters 1, 3, 5, 6, 7, 8, 9 and the one-pager of chapter 2; 8 times in chapter 9 (F09-B17).
- **Now → Proposed:** converge → "се сближава (с/към)" / "клони към"; convergent → "сходящ" (keep "сходимост" for *convergence*).
- **Why:** "сходява" is not a Bulgarian verb. The capital "С" in the value also leaks into figure labels ("никога не Сходяват", fig. 48 mapping).

### F09-T02 · S1 · settled entries whose "Bulgarian" value is English
- **Where:** glossary_settled.md: "kuhn's theorem → Kuhn's Theorem", "machine zero → Machine Zero", "iterated prisoner's dilemma → Iterated Prisoner's Dilemma", "lola learners → LOLA learners", "JSON artifacts → JSON artifacts", also "egta meta-game → EGTA Meta-Game". All of the first five print in chapter 9 (F09-B02, F09-B12).
- **Now → Proposed:** → "теорема на Кун"; "машинна нула"; "повтаряща се дилема на затворника"; "агенти с LOLA"; "JSON файлове с резултати"; "мета-игра в EGTA".
- **Why:** An English value makes the pipeline insert English into Bulgarian prose, and title-case values ("Machine Zero") print capitalised mid-sentence.

### F09-T03 · S1 · "defect → дефект"
- **Where:** glossary_settled.md (freq 2); chapter 9 (6 places, F09-B05), and "дефект…" also in chapters 5 and 10.
- **Now → Proposed:** defect (PD action) → "предателство" (verb "предава"); cooperate → "сътрудничество"; defector → "предаващ играч".
- **Why:** "дефект" is a flaw. The glossary's own "mutual defection → взаимно предателство" already uses the right word.

### F09-T04 · S1 · "thesis hooks → теза"; "greedy team reward → награда за отборна алчност"
- **Where:** glossary_settled.md; printed in chapter 9 (F09-B04, F09-B07); mapping "greedy reward → алчна награда".
- **Now → Proposed:** thesis hooks → "връзки с дисертацията"; greedy team reward → "отборна награда при алчна стратегия"; greedy reward → "награда при алчна стратегия".
- **Why:** The first value turns "three links to the dissertation" into "three theses". The second means "a reward for team greed". Greedy qualifies the policy being evaluated, not the reward.

### F09-T05 · S2 · "two-player → двуигрови"
- **Where:** glossary_settled.md (freq 1, but "двуигров…" prints in the BG summaries of chapters 2, 5, 6, 8, 9, 11 and the one-pagers of 6, 8, 9, 11).
- **Now → Proposed:** delete the entry, or → "за двама играчи"; "two-player zero-sum → игра за двама с нулева сума" (already settled) should win.
- **Why:** "двуигров" is not a word (F09-B15).

### F09-T06 · S2 · "matching pennies → игра „хвърляне на монета“"
- **Where:** glossary_settled.md (freq 10); chapters 4 and 9.
- **Now → Proposed:** → "„съвпадение на монети“ (Matching Pennies)"
- **Why:** A coin toss is a chance event, whereas Matching Pennies is a strategic game with chosen sides. No established Bulgarian name was found, so a descriptive one with the English name at first use is safest (F09-B18).

### F09-T07 · S2 · oracle family → "предсказвач"
- **Where:** glossary_settled.md: "oracle → предсказвач", "best-response oracle → предсказвач за най-добър отговор", "double oracle → двоен предсказвач"; the same in the curated `terminology_EN_BG.md` (two rows). Chapters 8, 9, 10, 11 and the one-pagers of 2, 8, 9, 10, 11.
- **Now → Proposed:** → "оракул"; "оракул за най-добър отговор"; "метод на двойния оракул".
- **Why:** The oracle is a subroutine queried for an answer; it predicts nothing. "оракул" is the standard Bulgarian computer-science term ("машина с оракул"). This touches the curated file, so it needs the owner's decision.

### F09-T08 · S2 · "self-play → самообучение"; "independent learning → самостоятелно обучение"
- **Where:** glossary_settled.md (freq 43 and 6); "самообучение" in chapters 5, 6, 8, 9, 10, 11, 12.
- **Now → Proposed:** self-play → "игра срещу себе си" (first use: "(self-play)"); independent learning → "независимо обучение"; independent learners → "независими обучаващи се агенти" (already settled).
- **Why:** "самообучение" means self-study or self-supervised learning. "самостоятелно обучение" is also "self-study". With both in one chapter they were confused (F09-B03). This is a high-frequency change, so decide it centrally.

### F09-T09 · S2 · "time-average → Усреднено време"; "divergence → разминаване"
- **Where:** glossary_settled.md; chapters 5 and 9 (F09-B11, F09-B18, F09-C02).
- **Now → Proposed:** time-average → "средно по времето"; divergence (of a trajectory) → "отдалечаване (от равновесието)"; keep "дивергенция" for KL.
- **Why:** "усреднено време" means "averaged time". "разминаване" means "missing each other" or "a mismatch".

### F09-T10 · S2 · "reconciliation → съгласуване"
- **Where:** glossary_settled.md (freq 2); the reconciliation boxes of chapters 5, 6, 9, 10, 11.
- **Now → Proposed:** → "съпоставка (прогноза → резултат)"
- **Why:** In this corpus a *reconciliation* compares a kept prediction with the measured result. "съгласуване" means coordination or agreement, and it collides with "съгласуван" = *consistent* (F07-T05).

### F09-T11 · S3 · smaller MARL entries
- **Where:** glossary_settled.md
- **Now → Proposed:**
  - "climbing game → изкачваща се игра" → "играта „изкачване“"
  - "value loss → загуба на стойност" → "грешка на функцията на стойността"
  - "referential task → референтна задача" → "референциална задача"
  - "naive learners → наивни учащи", "softmax learner → софтмакс обучаващ", "cooperative learners → сътрудничещи се обучаеми" → "наивни обучаващи се агенти", "агент със softmax параметризация", "сътрудничещи си обучаващи се агенти"
  - "hard-exploration coordination → координация при сложно проучване" → "координация при трудно изследване" (exploration is "изследване" elsewhere)
- **Why:** Each is a literal calque or uses a second word for a settled concept (F09-B06, F09-B22, F09-B30).

## C — Content

### F09-C01 · S1 · "differentiates through that chapter" (EN and BG)
- **Where:** summaryEn.md l. 352 "differentiates *through* that chapter."; summaryBg.md § 9.8 "като диференцира *през* тази глава."
- **Problem:** LOLA differentiates through the opponent's learning *step*. A global "step" → "chapter" replacement caught the word "step" here, and the translation followed.
- **Now → Proposed:** EN "differentiates *through* that chapter." → "differentiates *through* that learning step."; BG "като диференцира *през* тази глава." → "като диференцира *през* тази стъпка на обучение."
- **Note:** Before closing the step → chapter work, grep the EN summaries of all chapters for "that chapter", "one chapter", "each chapter" in algorithmic contexts.

### F09-C02 · S2 · The Matching Pennies explanation blames the wrong thing
- **Where:** summaryBg.md § 9.4 reconciliation "Конкретният мисловен модел за „енергозапазваща орбита“ беше грешната част; механизмът е бавно **разминаване** към границата, което, ако нещо, е още по-силен аргумент за среднопретеглящия механизъм, който следва."; EN l. 189–191; fig. 48 caption "More compute traces a bigger divergence, not convergence"; report_en §3 "more compute traces a larger divergence".
- **Problem:** The prediction was right for the model the chapter cites. Singh, Kearns & Mansour (2000) analyse *infinitesimal* gradient ascent. When the dynamics matrix has imaginary eigenvalues (Matching Pennies), the unconstrained trajectories are ellipses around the equilibrium ("limit-cycle behavior", their Fig. 1a; read in arXiv:1301.3892). The outward spiral measured here comes from the fixed step lr = 0.1 (`exploration/figures/nonstationarity_demo.json`): each Euler step lands slightly outside the ellipse. A smaller step would slow the growth. So "more compute traces a bigger divergence" is a property of this step size, not of non-stationarity. What *is* structural is that the last iterate does not converge either way.
- **Now → Proposed:** "Конкретният мисловен модел за „енергозапазваща орбита“ беше грешната част; механизмът е бавно **разминаване** към границата, което, ако нещо, е още по-силен аргумент за среднопретеглящия механизъм, който следва." → "Моделът на „енергозапазващата орбита“ е верен за непрекъснатата динамика (безкрайно малка стъпка): тогава траекторията обикаля около равновесието по затворена крива (Singh и др., 2000). При фиксирана стъпка 0.1 обаче всяка стъпка излиза леко навън от кривата и траекторията бавно се отдалечава по спирала към границата. И в двата случая последната итерация не се сближава, а това е аргумент в полза на механизмите за осредняване, разгледани по-нататък." EN analogous: "The 'energy-preserving orbit' is the right picture for the continuous-time dynamics (infinitesimal step), where the trajectory circles the equilibrium on a closed curve (Singh et al., 2000). With a fixed step of 0.1 each update lands slightly outside that curve, so the trajectory spirals slowly out to the boundary. Either way the last iterate does not converge, which is the case for the averaging machinery that follows." Fig. 48 caption: see F09-G01. Report §3/§9.1: the same correction.

### F09-C03 · S2 · Why "average strategy → Nash" fails is misattributed
- **Where:** summaryBg.md § 9.2 "Контрафактичното разлагане на CFR изисква дърво и пълна памет, които общите марковски игри (цикли, едновременни ходове, $N>2$) не предоставят, така че „средна стратегия $\to$ Наш“ вече не важи;"; EN l. 102–104.
- **Problem:** A game with $N>2$ players can still be a tree with perfect recall, and CFR runs on it. What fails is the guarantee. Abou Risk & Szafron (2010) write: "CFR is only guaranteed to converge to an ε-Nash equilibrium strategy profile for two-player zero-sum perfect recall games … for multiplayer … games, we lose all theoretical guarantees for CFR". They also report that in 3-player Leduc "CFR does not produce an ε-Nash equilibrium" (read in the AAMAS 2010 preprint).
- **Now → Proposed:** "Контрафактичното разлагане на CFR изисква дърво и пълна памет, които общите марковски игри (цикли, едновременни ходове, $N>2$) не предоставят, така че „средна стратегия $\to$ Наш“ вече не важи;" → "Контрафактичното разлагане на CFR изисква дърво на играта с пълна памет, каквото общите марковски игри (с цикли и едновременни ходове) не предоставят, а при $N>2$ играчи CFR губи гаранцията за сходимост към равновесие на Наш дори в дърво с пълна памет (Abou Risk и Szafron, 2010), така че „средна стратегия $\to$ Наш“ вече не важи;". EN: "CFR's counterfactual decomposition needs a game tree with perfect recall, which general Markov games (loops, simultaneous moves) do not provide; and with $N>2$ players CFR loses its guarantee of converging to a Nash equilibrium even on such a tree (Abou Risk & Szafron, 2010), so "average strategy → Nash" no longer holds;". Source: F09-S08.

### F09-C04 · S2 · "The CTDE variance-reduction claim, confirmed" overclaims; "necessary" is not shown
- **Where:** summaryBg.md § 9.5 "Това потвърждава твърдението за намаляване на дисперсията при CTDE по ясен начин."; § 9.10 "- но само намаляването на дисперсията не реши изкачващата се игра, така че то е необходимо, но не и достатъчно."; onePagerBg.md "- потвърждение на твърдението за намаляване на дисперсията в CTDE."; EN l. 228–229, l. 431, onePager l. 46–47.
- **Problem:**
  1. What was measured is the regression residual of each critic on a one-step task. The central critic sees the target, so it can fit exactly; the independent one cannot. That confirms a better-fitted *value target*, not lower variance of the *policy gradient*, which is what "variance reduction" in CTDE usually refers to. Lyu et al. (2021) prove the opposite for converged critics: "the centralized critic results in higher variance updates of the decentralized actors assuming converged on-policy value functions" and "stability of value function learning does not directly translate to a reduced variance in policy learning" (read in arXiv:2102.04402). The journal version (JAIR 2023) concludes that "critic centralization is not strictly beneficial".
  2. "Necessary" is not shown by any result. IL and MAPPO reach the same reward (7), and the chapter has no run without a centralised critic that fails where one with it succeeds.
- **Now → Proposed:**
  - "Това потвърждава твърдението за намаляване на дисперсията при CTDE по ясен начин." → "Това потвърждава, че централизираният оценител напасва целевата си стойност много по-точно. Това само по себе си не означава по-ниска дисперсия на градиента на стратегията: при сходили оценители централизираният оценител може дори да я увеличи (Lyu и др., 2021)."
  - "- но само намаляването на дисперсията не реши изкачващата се игра, така че то е необходимо, но не и достатъчно." → "- но по-точният оценител не реши играта „изкачване“: той не е достатъчен за координация."
  - onePagerBg: "- потвърждение на твърдението за намаляване на дисперсията в CTDE." → "- много по-точно напасване на целевата стойност (което не е същото като по-ниска дисперсия на градиента на стратегията)."
  - EN: "This is the CTDE variance-reduction claim, confirmed cleanly." → "This confirms that the centralized critic fits its value target far more precisely. That alone does not mean lower policy-gradient variance: with converged critics a centralized critic can even increase it (Lyu et al., 2021)."; "so it is necessary, not sufficient." → "so a better critic is not sufficient for coordination."; onePager "— the CTDE variance-reduction claim, confirmed." → "— a far better fit of the value target (not the same as lower policy-gradient variance)."
- **Source:** F09-S02.

### F09-C05 · S2 · The "MADDPG" in the results is a COMA-style variant
- **Where:** summaryBg.md § 9.5 reconciliation and § 9.9 (4); table 27 row "MADDPG (CTDE)"; fig. 50.
- **Problem:** `implementation/step09/implementation/maddpg.py` (docstring): "MADDPG's original actor update is the deterministic policy gradient; for DISCRETE actions we use the equivalent stochastic-policy update with a COMA-style COUNTERFACTUAL baseline". This is not equivalent to MADDPG. It is the actor update of COMA (Foerster et al., AAAI 2018: "a counterfactual baseline that marginalises out a single agent's action"). So "MADDPG trails at 5" is a result for that hybrid, and the chapter's own next step ("the counterfactual baseline to scrutinize") already points there.
- **Now → Proposed:** after "а MADDPG всъщност *изостана* както спрямо IL, така и спрямо MAPPO." insert "(Използваният вариант на MADDPG за дискретни действия заменя детерминистичния градиент на стратегията с контрафактична базова линия в стила на COMA (Foerster и др., 2018), затова резултатът се отнася до този вариант, а не до MADDPG в оригиналния му вид.)" EN after "MADDPG actually *underperformed* both IL and MAPPO.": "(The discrete-action MADDPG variant used here replaces the deterministic policy gradient with a COMA-style counterfactual baseline (Foerster et al., 2018), so the result speaks for that variant, not for MADDPG as published.)"

### F09-C06 · S2 · The Leduc PSRO curve is not "roughly monotone"; the Goofspiel ranges are off
- **Where:** summaryBg.md § 9.6 reconciliation 1 "ясно, приблизително монотонно намаление"; fig. 52 caption "declines steadily"; table 30 Goofspiel rows; reconciliation 2; report_en §5 and §9.
- **Problem:** `results/scale_results.json` → `psro.leduc.exploitability` = 4.75, **6.83**, 4.60, 5.83, 3.73, 5.80, 5.07, 5.48, 3.64, 3.57, 3.12, 3.04, 3.51, 2.92, 2.83, 3.10, 2.23, 2.35, 2.51, 2.16. The first eight rounds oscillate between 3.7 and 6.8, and round 1 is the maximum. The decline starts only at round 8. Goofspiel K = 4 (8 rounds, not 20) is 1.50, 2.0, **1.24**, 2.0, 1.55, 2.0, 1.41, 1.71, so "1.4–2.0" misses the minimum. The K = 3 row (1.33 → 0) comes from `smoke_results.json`; the scale config ran K = 4 only. Report §5 attributes both to `scale_results.json`.
- **Now → Proposed:**
  - "Измерено, тя спадна от $4.75$ до $2.16$ - ясно, приблизително монотонно намаление, но далеч от $0.5$." → "Измерено, тя спадна от $4.75$ до $2.16$ - след силни колебания през първите осем кръга (до $6.83$) следва ясно намаление, но стойността остава далеч от $0.5$."
  - "| Goofspiel ($K=4$) | колебае се $1.4 \leftrightarrow 2.0$ | не се установява |" → "| Goofspiel ($K=4$) | колебае се $1.24 \leftrightarrow 2.0$ (8 кръга) | не се установява |"
  - "| Goofspiel ($K=3$) | $1.33 \to 0$ | сближава се |" → "| Goofspiel ($K=3$, пробна конфигурация) | $1.33 \to 0$ | сближава се |"
  - "осцилира между $\sim\!1.4$ и $\sim\!2.0$ и не се установява" → "осцилира между $\sim\!1.2$ и $2.0$ и не се установява"
  - EN the same (l. 299–300, table, l. 307); report_en/bg §5 table and §9.2–9.3 likewise.
- **Note:** All other chapter numbers match the JSON (PSRO Kuhn/matrix/RPS, critic residuals, climbing and communication rewards, LOLA returns, self-play curve, MP radius and NashConv 1.44–1.84 across 5 seeds, the smoke numbers). EN and BG summary, one-pager and report agree number for number (checked by script).

### F09-C07 · S2 · Wrong cross-chapter claims: "single-agent RL (Chapters 1 and 6)" and "Chapters 2–8 lived entirely inside two-player zero-sum"
- **Where:** summaryBg.md § 9.1 "В single-agent RL (Глави 1 и 6) един агент"; intro "Глави 2–8 съществуват изцяло в рамките на **двуигрови игри с нулева сума**"; onePagerBg.md "Проблем."; EN l. 44, l. 29, onePager l. 16.
- **Problem:** Chapter 6 is "End-to-End Game AI Architectures" (DeepStack, Libratus, Pluribus, ReBeL, SoG), not single-agent RL. It covers Pluribus, which "broke the *player-count* barrier, reaching superhuman six-player play" (step06 summaryEn l. 47–48). So chapters 2–8 were not *entirely* two-player zero-sum.
- **Now → Proposed:**
  - "В single-agent RL (Глави 1 и 6) един агент" → "В едноагентното обучение с подкрепление (Глава 1) един агент"
  - "Глави 2–8 съществуват изцяло в рамките на **двуигрови игри с нулева сума**" → "Глави 2–8 работят почти изцяло в рамките на **игри за двама с нулева сума** (Pluribus в Глава 6 е изключението, което се отказва от гаранциите)"
  - EN: "In single-agent RL (Chapters 1 and 6)" → "In single-agent RL (Chapter 1)"; "Chapters 2–8 lived entirely inside **two-player zero-sum**\ngames" → "Chapters 2–8 worked almost entirely inside **two-player zero-sum** games (Pluribus in Chapter 6 being the exception that gave up the guarantees)". One-pager: "lived inside" → "worked almost entirely inside".

### F09-C08 · S2 · Overclaim: PSRO "is the framework for safe exploitation where there is no minimax theorem"
- **Where:** summaryBg.md intro "едновременно представлява рамката за безопасна експлоатация, когато няма теорема за минимакс (Принос №2)"; EN l. 35.
- **Problem:** Nothing in the chapter (or in Lanctot et al., 2017) shows PSRO providing any safety notion. The chapter's own § 9.9 and one-pager pose it as an open question ("can PSRO's meta-game supply the substitute?"). `lit_gaps.md` (C2) finds no N-player method with a safety criterion.
- **Now → Proposed:** "едновременно представлява рамката за безопасна експлоатация, когато няма теорема за минимакс (Принос №2)" → "е кандидат-рамка за безопасна експлоатация там, където няма теорема за минимакса (Принос №2)"; EN "is both the framework for safe exploitation where there is no minimax theorem" → "is both a candidate framework for safe exploitation where there is no minimax theorem".

### F09-C09 · S2 · Stale "step" naming (the candidate's own comment not fully applied)
- **Where:** candidate's comment (chapter 0, p. 2 of the Aug build): "maybe its time to change all emntion of steps into chapters". Still stale in chapter 9:
  - summaryBg.md "Всеки метод на този етап представлява"
  - "последователността на стъпката" (F09-B09)
  - figures 51 ("стъпка 2", "Стъпка 07", F09-G08)
  - the fig. 51 EN alt text ("Step 07's", "game-theory steps", F09-G01)
  - summaryEn.md l. 26–27 "the most instructive parts of\nthe step."
- **Now → Proposed:** "Всеки метод на този етап представлява" → "Всеки метод в тази глава представлява"; EN "the most instructive parts of\nthe step." → "the most instructive parts of\nthe chapter."; the others as in the cited findings.
- **Why:** The bundle says "Глава". "на този етап" also reads as "at this stage (of time)".

### F09-C10 · S2 · Stale "to close": the figures exist
- **Where:** summaryBg.md § 9.9 "**Доверие.**" (BG fix in F09-B12); summaryEn.md l. 412–414 "a few were not saved on the run and are marked "to close.""; report_en/bg §10 last bullet and §11.6; `deliverables/reports/step09/figures/README.md` ("Status: … the PNGs were not saved … marked **[to close]**", all eleven rows).
- **Problem:** All seven experiment PNGs are in `figures/` and `summary/`, dated 24 Jul, and the four diagrams exist. The chapter tells the reader that figures it prints are missing.
- **Now → Proposed:** EN "The experiment PNGs cited above are generated from the committed JSON artifacts (see `../figures/README.md`); a few were not saved on the run and are marked "to close."" → "The experiment figures above are generated from the committed JSON results (see `../figures/README.md`)."; report §10: drop "and the experiment PNGs"; README: set the status column to "generated (24 Jul 2026)".

### F09-C11 · S3 · "~2.9" for the LOLA exploration run picks one agent
- **Where:** summaryBg.md § 9.8 "а изследователското изпълнение с по-голяма **скорост на обучение при предвиждане** достигна $\sim\!2.9$.)"; EN l. 373–374.
- **Problem:** `exploration/figures/lola_ipd_playground.json` → `lola.final` = [2.665, 2.932]. The mean (2.80) is no higher than the main run's 2.82. The report (§8) states "2.67–2.93" correctly.
- **Now → Proposed:** "а изследователското изпълнение с по-голяма **скорост на обучение при предвиждане** достигна $\sim\!2.9$.)" → "а в изследователското изпълнение с по-голяма **скорост на обучение при предвиждане** двамата агенти достигнаха $2.67$ и $2.93$ (средно $2.80$).)"; EN "reached $\sim\!2.9$.)" → "reached $2.67$ and $2.93$ for the two agents (mean $2.80$).)"

### F09-C12 · S3 · Markov-game special cases stated too narrowly or too broadly
- **Where:** summaryBg.md § 9.2 "- $N=2$, $R_1=-R_2$, едно състояние води до **матрична игра** (тестовата среда на тази глава, §4)."; EN l. 94–95.
- **Problem:** Three of the four § 9.4 testbeds (PD, Stag Hunt, BoS) are general-sum, so "$R_1=-R_2$" excludes the chapter's own examples. The next bullet makes EFGs zero-sum, which they need not be (fixed in F09-B25's rewrite by keeping "нулева сума" only as the chapters' case).
- **Now → Proposed:** "- $N=2$, $R_1=-R_2$, едно състояние води до **матрична игра** (тестовата среда на тази глава, §4)." → "- $N=2$ и едно състояние дава **матрична игра** (с нулева сума при $R_1=-R_2$; тестовата среда на тази глава, §4)."; EN "- $N=2$, $R_1=-R_2$, a single state gives a **matrix game**" → "- $N=2$ and a single state give a **matrix game** (zero-sum when $R_1=-R_2$)".

## S — Sources

### F09-S01 · S2 · SOURCE_GAPS row 1: LOLA in the intro → cite Foerster et al. (2018), and soften "is"
- **Where:** summaryBg.md intro, "**LOLA** - диференциране през *стъпката на обучение* на противника - е *динамично* моделиране на противника"
- **Proposal (cite and soften):** "**LOLA** - диференциране през *стъпката на обучение* на противника - е *динамично* моделиране на противника" → "**LOLA** (Foerster и др., 2018) - диференциране през *стъпката на обучение* на противника - може да се разглежда като *динамично* моделиране на противника". EN the same ("LOLA (Foerster et al., 2018) … can be read as *dynamic* opponent modeling").
  - Verified on the arXiv abstract of 1709.04326: "each agent shapes the anticipated learning of the other agents"; "a term that accounts for the impact of one agent's policy on the anticipated parameter update of the other agents"; "the emergence of tit-for-tat and therefore cooperation in the iterated prisoners' dilemma".
  - The "dynamic opponent modelling" label is the chapter's reading, not the paper's; the paper uses "opponent modelling" only for its grid-world variant.
  - Complete the footnote as "Foerster, J., Chen, R. Y., Al-Shedivat, M., Whiteson, S., Abbeel, P. & Mordatch, I. (2018). "Learning with Opponent-Learning Awareness." *AAMAS*, 122–130. arXiv:1709.04326." (authors and pages from Crossref).
  - An inline author-year is proposed because the footnote `[^foerster2018]` is already referenced once in § 9.8.

### F09-S02 · S2 · SOURCE_GAPS row 2: CTDE definition and the variance claim → cite, and soften (F09-C04)
- **Where:** summaryBg.md § 9.10 "- **CTDE централизира оценителя по време на обучението и децентрализира актьора при изпълнението**; измерено е, че осигурява оценител с почти нулева дисперсия"
- **Proposal (cite and soften):**
  - Definition: the chapter already cites Lowe et al. (2017) at the end of § 9.5 (`[^lowe2017]`). For the paradigm itself add "Kraemer, L. & Banerjee, B. (2016). "Multi-agent reinforcement learning as a rehearsal for decentralized planning." *Neurocomputing* 190, 82–94. DOI 10.1016/j.neucom.2016.01.031" (Crossref metadata; commonly credited with the CTDE framing, but I did not read it: see the extract's *To verify*).
  - Variance: the numbers are the chapter's own measurement and need no citation, but the interpretation does. Cite "Lyu, X., Xiao, Y., Daley, B. & Amato, C. (2021). "Contrasting Centralized and Decentralized Critics in Multi-Agent Reinforcement Learning." *AAMAS*, 844–852. arXiv:2102.04402". Verified in the arXiv PDF: "the centralized critic results in higher variance updates of the decentralized actors assuming converged on-policy value functions"; pages from Crossref. Use it with the wording of F09-C04. Journal version: Lyu, Baisero, Xiao, Daley, Amato, *JAIR* 77, 295–354, 2023, DOI 10.1613/jair.1.14386 (Crossref + JAIR abstract).
  - In the § 9.10 bullet: "измерено е, че осигурява оценител с почти нулева дисперсия" → "измерено е, че централизираният оценител напасва целевата си стойност почти без остатък".

### F09-S03 · S2 · Unsourced: the climbing game and relative over-generalisation
- **Where:** summaryBg.md § 9.5 reconciliation ("играта „изкачване“ на Claus и Boutilier", "относителното свръхобобщаване").
- **Proposal (cite):** after "на Claus и Boutilier" add `[^claus1998]`, with "Claus, C. & Boutilier, C. (1998). "The Dynamics of Reinforcement Learning in Cooperative Multiagent Systems." *AAAI*, 746–752." (verified: AAAI-98 paper listing and dblp via web search). For relative over-generalisation and the coordination failures of independent learners add "Matignon, L., Laurent, G. J. & Le Fort-Piat, N. (2012). "Independent reinforcement learners in cooperative Markov games: a survey regarding coordination problems." *Knowledge Engineering Review* 27(1), 1–31. DOI 10.1017/S0269888912000057" (Crossref metadata only).

### F09-S04 · S2 · Unsourced named methods and results: QMIX, COMA, Kuhn's theorem
- **Where:** summaryBg.md § 9.3 "(QMIX, 2018)" and fig. 46; § 9.5 "контрафактична базова линия" (F09-C05); § 9.6 "съгласно теоремата на Кун".
- **Proposal (cite):**
  - "Rashid, T., Samvelyan, M., Schroeder de Witt, C., Farquhar, G., Foerster, J. & Whiteson, S. (2018). "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning." *ICML*. arXiv:1803.11485" (arXiv).
  - "Foerster, J., Farquhar, G., Afouras, T., Nardelli, N. & Whiteson, S. (2018). "Counterfactual Multi-Agent Policy Gradients." *AAAI* 32(1). DOI 10.1609/aaai.v32i1.11794" (Crossref + arXiv abstract).
  - "Kuhn, H. W. (1953). "Extensive Games and the Problem of Information." *Contributions to the Theory of Games II*, 193–216. DOI 10.1515/9781400881970-012" (Crossref).
  - QMIX appears in the timeline and the figure but nowhere else (see F09-X04).

### F09-S05 · S2 · Footnote `lowe2017`: MAPPO title and venue
- **Where:** summaryBg.md and summaryEn.md footnote `lowe2017`, "Yu, C. et al. (2022). "The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games." *NeurIPS* (MAPPO)."
- **Proposal (correct):** → "Yu, C., Velu, A., Vinitsky, E., Gao, J., Wang, Y., Bayen, A. & Wu, Y. (2022). "The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games." *NeurIPS Datasets and Benchmarks Track*. arXiv:2103.01955." Verified on the arXiv page. The title has a comma, and the paper is in the Datasets and Benchmarks track. The same page supports "often the strongest baseline" only as "competitive or superior results … with minimal hyperparameter tuning". MADDPG (arXiv:1706.02275, Lowe, Wu, Tamar, Harb, Abbeel, Mordatch) checked correct.

### F09-S06 · S2 · Footnote `albrecht2024` cites the wrong chapters
- **Where:** summaryBg.md footnote "… (MIT Press), Ch. 8–9 - актуално учебникарско изложение точно на тази таксономия."
- **Problem:** Checked against the book's site (marl-book.com). Ch. 8 is "Deep Reinforcement Learning" (single-agent). The challenges this chapter opens with are in Ch. 5 ("Multi-Agent Reinforcement Learning in Games: First Steps and Challenges"), and the method families in Ch. 9 ("Multi-Agent Deep Reinforcement Learning").
- **Proposal (correct):** "Ch. 8–9 - актуално учебникарско изложение точно на тази таксономия." → "гл. 5 и 9 - съвременно учебно изложение на тези предизвикателства и методи." EN "Ch. 8–9" → "Ch. 5 and 9". Only chapter titles were verified. "учебникарско" is often pejorative ("school-bookish").

### F09-S07 · S3 · Spot-check of the remaining footnotes
- **Where:** footnotes `zhang2021`, `littman1994`, `singh2000`, `lanctot2017`, `sukhbaatar2016`, `foerster2018`
- **Findings:**
  - **Checked correct:**
    - Zhang, Yang & Başar, *Handbook of RL and Control*, Springer 2021, pp. 321–384 (Springer listing).
    - Littman, ICML 1994, pp. 157–163.
    - Singh, Kearns & Mansour, UAI 2000, pp. 541–548, arXiv:1301.3892. The abstract matches the chapter's use: "either the agents will converge to a Nash equilibrium, or … their average payoffs will nevertheless converge".
    - Lanctot et al., NIPS 2017, arXiv:1711.00832, eight authors. The abstract says it "generalizes previous ones such as InRL, iterated best response, double oracle, and fictitious play", matching "unifies self-play, fictitious play, and the double-oracle method".
    - McMahan, Gordon & Blum, ICML 2003, pp. 536–543.
    - Sukhbaatar, Szlam & Fergus, NIPS 2016 ("communication between them is learned alongside their policy").
  - **Correct:** in `lanctot2017`, "Tuyls, K. et al. (2020). … *AAMAS/JAAMAS* (EGTA)." → "Tuyls, K. et al. (2020). "Bounds and dynamics for empirical game theoretic analysis." *Autonomous Agents and Multi-Agent Systems* 34(1), art. 7. DOI 10.1007/s10458-019-09432-y." (Crossref; the title has no hyphen in "game theoretic").
  - **Optional:** add authors and pages to `foerster2018` (F09-S01).

### F09-S08 · S2 · New source needed for the corrected N > 2 claim (F09-C03)
- **Where:** summaryBg.md § 9.2 (after the F09-C03 rewrite)
- **Proposal (cite):** "Abou Risk, N. & Szafron, D. (2010). "Using Counterfactual Regret Minimization to Create Competitive Multiplayer Poker Agents." *AAMAS*, 159–166." Verified: the AAMAS 2010 preprint PDF (poker.cs.ualberta.ca), quotes as in F09-C03; pages from the search listing. Optional, for "self-play converges in the average" (§ 9.6): "Robinson, J. (1951). "An Iterative Method of Solving a Game." *Annals of Mathematics* 54(2), 296–301. DOI 10.2307/1969530" (Crossref). The chapter's fictitious play converges in the average by Robinson's theorem, not by a property of self-play in general.

## X — Structure

### F09-X01 · S3 · Cross-references "§4 … §7" vs printed "9.4 … 9.7"
- **Where:** summaryBg.md "(…, §4)" twice in §§ 9.1–9.2, "(оттук и цикличността в §4)", "(§6)", "(§7)", "съпоставката в §5"; fig. 50 caption.
- **Fix:** "§N" → "раздел 9.N" (lower case, as the glossary's "както е показано в раздел N"). In a 226-page bundle a bare "§4" can be read as chapter 4. The one-pager's "§9 от доклада" is correct as it stands.

### F09-X02 · S3 · Takeaway bullets end with two spaces: blank lines between bullets (p. 187)
- **Where:** summaryBg.md § "Основни изводи…", all six bullets end with "  " (a Markdown hard break); the EN has none.
- **Fix:** strip the trailing double spaces. The printed list has an empty line inside each item.

### F09-X03 · S3 · "Five families" but six rows, and QMIX is not among them
- **Where:** summaryBg.md § 9.3 "Тук са от значение пет основни **семейства**." and table 27; QMIX in the timeline and fig. 46 only.
- **Fix:** either add a QMIX row ("факторизира съвместната стойност монотонно на стойности по агенти | кооперативни задачи с общи награди | монотонността ограничава класа на представимите функции") with the F09-S04 citation, or drop QMIX from the timeline and the figure. Also add "(MADDPG и MAPPO са два варианта на CTDE)" after "пет основни семейства", so the count matches the six rows.

### F09-X04 · S3 · Figure 52 and table 30 disagree on what is shown
- **Where:** table 30 lists RPS and Goofspiel K = 3; fig. 52 plots neither.
- **Fix:** either add them to `plot_psro` (RPS from `exploration/figures/psro_peek.json`, K = 3 from `smoke_results.json`, marked as such), or adjust the caption (F09-G09). No text change needed otherwise.

### F09-X05 · S3 · The one-pager's "four structural answers" vs five listed
- **Where:** onePagerBg.md "Подход.": "четирите структурни отговора" followed by IL, CTDE, PSRO, communication, LOLA.
- **Fix:** "(контролният вариант, който се проваля)" already sets IL apart. Add "контролен вариант плюс" before the list, or say "четирите структурни отговора и контролния вариант". EN the same.
