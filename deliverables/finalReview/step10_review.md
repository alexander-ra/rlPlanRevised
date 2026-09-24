# Step 10 — final review

**Summary:** The chapter is well organised and its numbers match the report exactly (EN/BG, summary, one-pager, report). Four points matter most. (1) Four of its interpretive claims are contradicted by its own results JSON or by the literature. The league's meta-Nash mixture is *better* than self-play (3.418 < 3.683), not "the weakest". The mixture is *less* exploitable than each of its three components, so the "tells" explanation is wrong: the best agent simply got zero weight. "Best individual beats self-play" compares a best-of-run snapshot (1.305) with self-play's final iterate; self-play's own best iterate was 1.396. And "rest points are exactly Nash equilibria; stable rest points are ESS" is false (Hofbauer & Sigmund 2003). (2) The Bulgarian has meaning errors a reader will stumble on: "smoke/scale/дима", "научен резултат", "безопасността за населението", "колело от броячи", "дефект", "намисля се", "RPS 0.0 е транзитивна", "(скала)". Several come from settled glossary entries (see T). (3) Six of the nine figures print entirely in English, because no `_bg` twins exist and `plotting.py` cannot be run by the renderer. Figs. 59 (league) and 62 (EGTA) are illegible in BG, fig. 56 prints at 3–4 pt, and fig. 63 does not show the result its caption claims. (4) The spinning top is attributed to Balduzzi 2019; it belongs to Czarnecki et al. 2020, and the Hodge decomposition to Balduzzi et al. 2018/2019. This is fixed here per `lit_gaps.md`. Decided centrally, not itemised: 66 hyphen-dashes (55 summary, 11 one-pager), 122 decimal points, ≈45 bold spans the EN does not have (109 vs 74 in the summary, 27 vs 17 in the one-pager). Two footnote labels are shared across chapters: `lanctot2017`, so ch. 10's marker prints ch. 9's note (PDF p. 181), and `balduzzi2019`, also defined in ch. 11. The candidate's TOC comment (ch. 0) about extra numbering in chapters 8–10 is applied; there are no ch.-10 comments.
**Counts:** S1 24 · S2 42 · S3 7   (by category: G 11 · B 32 · T 10 · C 10 · S 8 · X 2)

Conventions in this file:
- Quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md`, including `**`, `*` and `$`.
- Proposals keep the chapter's " - " dashes and decimal points; those are fixed centrally.
- Several findings replace a whole paragraph because a language fix and a content fix fall on the same line. Each fragment is quoted by exactly one finding, so all of them can be applied in any order.
- Page numbers are PDF pages of `allSummaries_bg.pdf`; the printed folio is one lower.
- Printed size = matplotlib size × (6.93 in printed width ÷ saved width in inches). The floor is ≈ 8.2 pt.
- The JSON facts come from `implementation/step10/implementation/results/{smoke,scale}_results.json`.

## G — Figures

### F10-G01 · S1 · Bulgarian captions for all nine figures
- **Where:** summaryBg.md, image alt text of figs. 55–63 (PDF pp. 192–202). All nine print in English (known corpus-wide defect). Content corrections from F10-C01/C02/C03/C05 are folded in, and the EN alt text needs the same corrections.
- **Now → Proposed:**
  - "![Evolutionary game theory as the continuous idealization of a PBT league: replicator selection ↔ copying the fitter agents, mutation/drift ↔ perturbing learning rate and entropy, and replicator rest points ↔ the meta-Nash / ESS the league is trying to reach. The league is replicator dynamics with learned agents instead of fixed strategy shares.]" → "![Еволюционната теория на игрите като непрекъсната идеализация на PBT лигата: подборът в репликаторната динамика съответства на копирането на по-успешните агенти, мутацията (дрейфът) - на промяната на скоростта на обучение и на ентропията, а устойчивите точки на покой (ESS) - на мета-Наш сместа, към която се стреми лигата. Лигата е репликаторна динамика, в която вместо фиксирани дялове на стратегиите участват обучаващи се агенти.]"
  - "![Replicator phase portraits: Prisoner's Dilemma → all-Defect, Hawk-Dove → the 0.5 interior ESS, Rock-Paper-Scissors → a closed orbit that never converges, and Stag Hunt → two basins (all-Stag or all-Hare). The non-converging RPS orbit is why populations in cyclic games need explicit machinery to avoid spinning.]" → "![Траектории на репликаторната динамика (дял на първата стратегия във времето): в дилемата на затворника популацията стига до всеобщо предателство, в „ястреб-гълъб“ - до вътрешната ESS с дял 0.5 на ястребите, в „камък-ножица-хартия“ обикаля около центъра, без да се сближава, а в „лов на елен“ стига до „всички ловуват елен“ или „всички ловуват заек“ в зависимост от началната точка. Тази несходяща орбита показва защо популациите в циклични игри се нуждаят от специални механизми, за да не се въртят в кръг.]"
  - "![The spinning top: a vertical transitive axis (skill - there is a better player) and a cyclic dimension (width - the number of counters, rock-paper-scissors structure). Rock-Paper-Scissors sits in the widest cyclic belly (transitive ratio 0.0); a pure skill ladder sits on the transitive spine (1.0); the PSRO-Ледюк best-response meta-game sits in the wide cyclic belly (~0.45 transitive), while the league's snapshot meta-game climbs the transitive spine (~0.94-0.98).]" → "![„Пумпалът“: вертикалната ос е транзитивната сила (умението - съществува по-добър играч), а ширината е цикличното измерение (броят на контрастратегиите, структурата „камък-ножица-хартия“). „Камък-ножица-хартия“ е в най-широката циклична част (транзитивно съотношение 0.0), чистата стълбица на уменията е върху транзитивната ос (1.0), мета-играта на най-добрите отговори в PSRO за Ледюк е в широката циклична част (транзитивно съотношение ~0.45), а мета-играта на моментните снимки на лигата се изкачва по транзитивната ос (~0.94-0.98). T - транзитивно, C - циклично съотношение.]"
  - "![Transitive ratio across four populations: RPS (0.0, purely cyclic), a pure skill ladder (1.0), the PSRO-Ледюк best-response meta-game (~0.41-0.46, mostly cyclic), and the league snapshot meta-game (~0.94-0.98, mostly transitive). Same game, opposite structure, depending on how the population is built.]" → "![Транзитивно съотношение на четири популации: „камък-ножица-хартия“ (0.0, чисто циклична), чиста стълбица на уменията (1.0), мета-играта на най-добрите отговори в PSRO за Ледюк (~0.41-0.46, предимно циклична) и мета-играта на моментните снимки на лигата (~0.94-0.98, предимно транзитивна). Една и съща игра има противоположна структура в зависимост от това как е изградена популацията.]"
  - "![The league: main agents (the product), main exploiters (hunt weaknesses in the current mains), and league exploiters (hunt weaknesses in the frozen history), with periodic freezing into a snapshot museum and PFSP matchmaking that focuses training where the agent is losing. PBT copies the top agents and perturbs their hyper-parameters.]" → "![Лигата: основни агенти (крайният продукт), основни експлоататори (търсят слабости в текущите основни агенти) и експлоататори на лигата (търсят слабости в цялата замразена история), с периодично замразяване на копия в „музей“ от моментни снимки и сдвояване по PFSP, което насочва обучението към противниците, срещу които агентът губи. PBT копира най-добрите агенти и променя хиперпараметрите им.]"
  - "![League exploitability over 120 epochs (scale): both min-main and meta-Nash exploitability fall to a minimum near epoch 60 and then regress upward. The frozen snapshots capture the strong mid-run agents; the live agents degrade late under exploiter pressure.]" → "![Експлоатируемост на лигата за 120 епохи (пълен мащаб): минималната експлоатируемост сред основните агенти и тази на мета-Наш сместа спадат рязко през първите около 15 епохи, най-ниски са около епохи 20-40 и отново нарастват в края на обучението. Замразените моментни снимки запазват силните агенти от първата половина на обучението, а активните агенти се влошават към края.]"
  - "![Mini-PBT diversity: on the transitive Prisoner's Dilemma the population collapses to a single strategy (diversity → 0), while on cyclic Rock-Paper-Scissors it churns indefinitely (0.07-0.29) as it chases the wheel of counters. Game structure, not population size, decides whether diversity survives.]" → "![Разнообразие при мини-PBT: в транзитивната дилема на затворника популацията се свежда до една-единствена стратегия (разнообразие → 0), а в цикличната игра „камък-ножица-хартия“ стратегиите непрекъснато се сменят (0.07-0.29), докато популацията следва кръга от контрастратегии. Дали разнообразието ще се запази, зависи от структурата на играта.]"
  - "![The EGTA pipeline: play every pair of agents to build an empirical payoff matrix, solve its meta-Nash mixture, collapse the mixture to a single behavioral policy, and measure its EXACT full-game exploitability. The measured caveat: the meta-Nash minimizes meta-game regret, not full-game exploitability, so the mixture can be more exploitable than the best single member.]" → "![Процесът на EGTA: всяка двойка агенти се изиграва, за да се построи емпирична матрица на печалбите, намира се мета-Наш сместа, тя се свежда до една поведенческа стратегия и се измерва ТОЧНАТА ѝ експлоатируемост в пълната игра. Измерената уговорка: мета-Наш минимизира съжалението в мета-играта, а не експлоатируемостта в пълната игра, затова сместа може да е по-експлоатируема от най-добрия член на популацията, който дори може да не участва в нея.]"
  - "![Final Ледюк exploitability by method (scale): CFR-Nash floor ~0.01; the league's best individual (1.31) beats PSRO (2.16) and self-play (3.68); the league's meta-Nash mixture (3.42) is the weakest learned result.]" → "![Крайна експлоатируемост в Ледюк по методи (пълен мащаб): долна граница CFR (равновесие на Наш) ~0.01; най-добрият отделен агент на лигата (1.31, най-добрият за цялото обучение) е под PSRO (2.16), под мета-Наш сместа на лигата (3.42) и под крайния агент от самообучението (3.68; най-добрата му итерация е 1.40).]"
- **Fix:** Replace the alt text in `summaryBg.md`. The `](file)` part changes to the `_bg` twins per F10-G11.
  - Figs. 56 and 61, EN: "Replicator phase portraits" → "Replicator trajectories". The plots are time series of one share, not phase portraits.
  - Fig. 61, EN: drop ", not population size,". Only one population size was run, so that part is untested.

### F10-G02 · S1 · Fig. 55 replicator ↔ league: English left, stale "стъпка", stale render, overflow, below the floor
- **Where:** `renders/ch10/p192_f1.png` — caption "Evolutionary game theory as the continuous idealization…"
- **Problem:**
  1. English in the BG figure: "подбор (fitter shares expand)". The mapping entry itself has English as its "bg" value.
  2. "Лига PBT (тази стъпка)" is stale naming.
  3. "Равновесни точки ↔ Наш / ESS" repeats the false claim of F10-C01. It also contradicts the text, which says "точки на покой".
  4. Imperative "копирай топ агентите", colloquial "топ", "фитнес" (a gym) for *fitness*, the English abbreviation "lr", and straight quotes 'дискретен аналог на'.
  5. The render is stale. It prints "(базов / базов-експлоатер / експлоатер на лига)" and "(фитнес = % победи …)", while the mapping now has "основен …" and "процент победи" (egta_/league_/replicator_selection_bg.png date from 1 Aug 13:08).
  6. Legibility at scale 0.924 (2475 px / 330 dpi = 7.5 in): box text 8.4–8.8 → 7.8–8.1 pt, note 7.6 → 7.0 pt.
  7. Overflow in the replicator, population, exploit, explore and rest-point boxes.
- **Fix:**
  - `make_replicator_figure.py` label changes:
    - 'PBT league (this step)' → 'PBT league (this chapter)'.
    - The rest box → 'Stable rest points = ESS\n(no small mutant share can invade)'.
    - The note → 'dashed = "discrete analog of": the league is replicator dynamics\nwith learned agents instead of fixed strategy shares'.
  - Size: all `box` fs → 10, `note` fs → 10, box heights 1.1 → 1.4, and wrap at ≤ 38 characters per line.
  - Mapping:
    - 'Evolutionary game theory' → 'Еволюционна теория на игрите'.
    - 'PBT league (this chapter)' → 'PBT лига (тази глава)'.
    - 'Selection\n(fitter shares expand)' → 'Подбор\n(дяловете на по-успешните растат)'.
    - 'Mutation / drift\n(explore nearby strategies)' → 'Мутация / дрейф\n(изследване на близки стратегии)'.
    - rest box → 'Устойчиви точки на покой = ESS\n(малък дял мутанти не може да навлезе)'.
    - replicator box second line → 'делът расте, ако печалбата е над средната'.
    - 'Population of neural PPO agents\n(main / main-exploiter / league-exploiter)' → 'Популация от невронни PPO агенти\n(основни агенти / основни експлоататори /\nексплоататори на лигата)'.
    - 'Exploit step: copy the top agents\n(fitness = win-rate vs population)' → 'Експлоатация: копиране на най-добрите агенти\n(приспособеност = дял победи\nсрещу популацията)'.
    - 'Explore step: perturb lr / entropy\n(mutate hyper-parameters)' → 'Изследване: промяна на скоростта на обучение\nи ентропията (мутация на хиперпараметрите)'.
    - 'Meta-Nash of the league\n(measured by exact exploitability)' → 'Мета-Наш сместа на лигата\n(оценена с точна експлоатируемост)'.
    - note → 'пунктир = „дискретен аналог на“: лигата е репликаторна динамика\nс обучаващи се агенти вместо фиксирани дялове на стратегиите'.
  - Re-render.

### F10-G03 · S1 · Fig. 56 replicator trajectories: entirely English, prints at 3–4 pt
- **Where:** `renders/ch10/p193_f1.png` — caption "Replicator phase portraits…"; `summaryBg.md` links the EN `replicator_playground.png`.
- **Problem:**
  1. Everything is English: code-name titles "prisoners_dilemma", "hawk_dove", "rock_paper_scissors", "stag_hunt"; "P[Cooperate]"; "replicator step"; legend "x0[0]=0.5".
  2. Illegible: `figsize=(4.2 × 4, 4)` at 120 dpi is 16.8 in wide, so the print scale is 0.41. Ticks and axis labels print at 4.1 pt, titles at 5.0 pt, the legend (fs 7) at 2.9 pt.
  3. These are time series of one share, not the "phase portraits" of the caption.
- **Fix:** `implementation/step10/exploration/replicator_playground.py`:
  - `plt.subplots(1, len(GAMES), figsize=(4.2 * len(GAMES), 4))` → `plt.subplots(2, 2, figsize=(8, 6.4))` with `axes = axes.flatten()`.
  - Titles from a static dict: TITLES = {"prisoners_dilemma": "Prisoner's Dilemma: share of Cooperate", "hawk_dove": "Hawk-Dove: share of Hawk", "rock_paper_scissors": "Rock-Paper-Scissors: share of Rock", "stag_hunt": "Stag Hunt: share of Stag"}.
  - Legend label `f"$x_0 = {x0[0]:.1f}$"`, `legend(fontsize=9)`, `tick_params(labelsize=9)`; `savefig(dpi=120)` → `dpi=300`.
  - Mapping, new keys:
    - "Prisoner's Dilemma: share of Cooperate" → 'Дилема на затворника: дял на сътрудничеството'.
    - 'Hawk-Dove: share of Hawk' → 'Ястреб-гълъб: дял на ястребите'.
    - 'Rock-Paper-Scissors: share of Rock' → 'Камък-ножица-хартия: дял на „камък“'.
    - 'Stag Hunt: share of Stag' → 'Лов на елен: дял на „елен“'.
    - 'replicator step' exists.
  - Render and link `_bg` (F10-G11).

### F10-G04 · S1 · Fig. 57 spinning top: no BG render, colliding labels, 5–7 pt
- **Where:** `renders/ch10/p194_f1.png` — caption "The spinning top…"; `summaryBg.md` links the EN `spinning_top.png`. No `spinning_top_bg.png` exists. I ran the renderer on a scratch copy and it works, so the twin was never generated.
- **Problem:**
  1. The whole figure is English.
  2. Colliding labels, even in EN:
     - "skill ladder" is printed over "transitive strength (skill)".
     - The RPS marker covers "cyclic dimension (width = #counters)".
     - The sub-labels "T=1.0 C=0.0" and "T~0.94-0.98" run over the ellipse edges.
     - "PSRO-Leduc" overflows its marker.
  3. Size: the long bottom note makes `bbox_inches="tight"` widen the canvas to 8.84 in, so the scale is 0.78. Marker labels 8.2 → 6.4 pt, sub-labels 6.8 → 5.3 pt, notes 7.4–8.6 → 5.8–6.7 pt.
  4. The scratch BG render has the same collisions plus mapping errors: 'RPS' → 'КНХ' (an unknown abbreviation), 'cyclic dimension\n(width = #counters)' → '…#броячи' (T02), 'skill ladder' → 'скала на уменията' (F10-B30).
  5. (S3, optional) The picture places whole games (RPS, a ladder) and populations on one top, while Czarnecki et al.'s top describes the strategy space of *one* game. The caption could say it is schematic.
- **Fix:** `make_spinning_top_figure.py`:
  - `marker()`: width 1.7 → 2.8, height 0.85 → 1.3; label fs 8.2 → 10; sub-label fs 6.8 → 9.5, drawn below the ellipse at `y - 0.85`.
  - Marker labels: "skill\nladder", "Rock-Paper-\nScissors", "PSRO best\nresponses", "league\nsnapshots".
  - PSRO marker x 2.6 → 2.0.
  - Notes:
    - Axis note → `note(ax, cx + 1.6, 8.4, …, ha="left", fs=10)`.
    - Cyclic note → `note(ax, cx + 2.4, 4.6, …, ha="left", fs=10)`.
    - "weakest" fs → 9.6.
    - Bottom note split with "\n" after "belly;" and fs → 10. This removes the canvas inflation: width ≈ 7.1 in, scale ≈ 0.98.
  - Mapping:
    - 'skill\nladder' → 'стълбица\nна уменията'.
    - 'Rock-Paper-\nScissors' → 'камък-ножица-\nхартия'.
    - 'PSRO best\nresponses' → 'най-добри\nотговори (PSRO)'.
    - 'league\nsnapshots' → 'моментни снимки\nна лигата'.
    - 'cyclic dimension\n(width = #counters)' → 'циклично измерение\n(ширина = брой контрастратегии)'.
    - 'transitive strength (skill)' → 'транзитивна сила (умение)' (exists).
    - the split bottom note → 'една и съща игра, различни популации: популацията от най-добри отговори (PSRO) е в широката циклична част;\nпопулацията от моментни снимки (лигата) се изкачва по транзитивната ос.'
  - Render and link `spinning_top_bg.png`.

### F10-G05 · S2 · Fig. 58 transitive ratios: English, code tick labels, soft
- **Where:** `renders/ch10/p196_f1.png` — caption "Transitive ratio across four populations…"
- **Problem:**
  1. All English, including the x ticks `rock_paper_scissors`, `pure_skill`, `psro_leduc_metagame`, `league_metagame` and the y-label "transitive ratio ||T|| / ||A_anti||".
  2. The tick labels are passed through `ax.bar(names, …)`, which the renderer does not translate, so they would stay English even after a BG render.
  3. 121 ppi prints soft. Type size is fine (≈ 9.9 pt).
  4. The existing mapping 'pure cycling (RPS)' → 'чисто цикличност (RPS)' is ungrammatical.
- **Fix:** `implementation/step10/implementation/plotting.py`, `plot_transitive_ratios`:
  - After `ax.bar`, add `ax.set_xticks(range(len(names))); ax.set_xticklabels([DISPLAY.get(n, n) for n in names], rotation=15)`, with DISPLAY = {"rock_paper_scissors": "Rock-Paper-Scissors", "pure_skill": "pure skill ladder", "psro_leduc_metagame": "PSRO best responses (Leduc)", "league_metagame": "league snapshots (Leduc)"}.
  - ylabel → "transitive ratio"; drop `set_title`; dpi 120 → 300.
  - Mapping:
    - 'Rock-Paper-Scissors' → 'Камък-ножица-хартия'.
    - 'pure skill ladder' → 'чиста стълбица на уменията'.
    - 'PSRO best responses (Leduc)' → 'най-добри отговори в PSRO (Ледюк)'.
    - 'league snapshots (Leduc)' → 'моментни снимки на лигата (Ледюк)'.
    - 'transitive ratio' → 'транзитивно съотношение'.
    - 'pure cycling (RPS)' → 'чисто циклична („камък-ножица-хартия“)'.
    - 'pure skill (transitive)' → 'чисто умение (транзитивна)'.

### F10-G06 · S1 · Fig. 59 league: BG layout collapses, labels collide, prints at 4–5 pt
- **Where:** `renders/ch10/p197_f1.png` — caption "The league: main agents…"
- **Problem:**
  1. The BG render is 3847 px wide against 2791 px for the EN. The two long BG notes extend beyond the axes, so `tight_layout` shrinks the axes and `bbox_inches="tight"` widens the canvas to 11.66 in (scale 0.59). Box text 8.4–8.6 → 5.0–5.1 pt, museum 8.2 → 4.9 pt, notes 7.0–8.2 → 4.2–4.9 pt.
  2. At that size every box label overflows into its neighbour ("ОСНОВНИ агентиОСНОВНИ експлоатьориЕксплоатьори…").
  3. The PFSP note is printed over the panel title. The same happens in the EN: the note is at y = 8.15 and the panel label at y = 8.08.
  4. Meaning: "наруши lr / ентропия" ("наруши" = violate); imperatives "копирай", "избери", "фокусирай"; "->"; "експлоатьори" (T04).
  5. The bottom note repeats the overclaim "best frozen snapshot 1.31 beats … self-play 3.68" (F10-C04).
- **Fix:** `make_league_figure.py`:
  - PFSP note y 8.15 → 8.75 with `ylim=(0, 9.3)`, split into two lines.
  - Delete the bottom "measured: …" note: the caption and text carry the numbers.
  - All `box` fs → 10, `note` fs → 9.6.
  - Mapping:
    - 'MAIN agents\n(the product)\nSP + PFSP vs everyone' → 'ОСНОВНИ агенти\n(крайният продукт)\nсамообучение + PFSP\nсрещу всички'.
    - 'MAIN exploiters\nhunt weaknesses in\nthe CURRENT mains' → 'ОСНОВНИ\nЕКСПЛОАТАТОРИ\nтърсят слабости в\nТЕКУЩИТЕ основни агенти'.
    - 'LEAGUE exploiters\nhunt weaknesses in\nthe FROZEN history' → 'ЕКСПЛОАТАТОРИ\nНА ЛИГАТА\nтърсят слабости в\nЗАМРАЗЕНАТА история'.
    - 'PBT step: …' → 'Стъпка на PBT: копиране на най-добрите агенти (експлоатация)\n+ промяна на скоростта на обучение и ентропията (изследване)' (EN key split with "\n" too).
    - 'Live population (trains + PBT exploit/explore)' → 'Активна популация (обучение + експлоатация/изследване в PBT)'.
    - museum → 'МУЗЕЙ от ЗАМРАЗЕНИ моментни снимки   [ main#e4 | main#e9 | ... | mexp#... | lexp#... ]\nпериодични замразени копия → противници, които не забравят стар стил'.
    - PFSP → 'Сдвояване по PFSP: всеки противник се избира с вероятност, която расте с трудността да бъде победен\n(обучението се съсредоточава там, където агентът губи)'.

### F10-G07 · S2 · Fig. 60 league exploitability: English, "(PREDICT: decreasing)", wrong legend mapping, soft
- **Where:** `renders/ch10/p198_f1.png` — caption "League exploitability over 120 epochs…"
- **Problem:**
  1. All English, including the title "PBT league: exploitability over training (PREDICT: decreasing)", which leaks the workflow.
  2. 130 ppi.
  3. The mappings are wrong or incomplete: 'min main-agent exploitability' → 'мин. основна експлоатируемост на агента' ("the agent's main exploitability"); 'exploitability (NashConv, exact)' → '…(NashConv, exact)' leaves "exact" in English; 'league epoch' → 'епоха в лига'.
  4. The plot itself contradicts the caption's "minimum near epoch 60" (F10-C05). The steep fall ends by epoch ~12 and the lowest band is epochs 20–40.
- **Fix:** `plotting.py` `plot_league`:
  - Drop `set_title`; dpi 120 → 300; legend label 'min exploitability of the main agents'.
  - Mapping:
    - 'min exploitability of the main agents' → 'минимална експлоатируемост сред основните агенти'.
    - 'meta-Nash exploitability' → 'експлоатируемост на мета-Наш сместа'.
    - 'exploitability (NashConv, exact)' → 'експлоатируемост (NashConv, точна)'.
    - 'league epoch' → 'епоха на лигата'.
  - Optional (F10-C04): add the self-play trajectory as a dashed grey line, `label="self-play (baseline)"` → 'самообучение (базова линия)'. It shows that self-play regresses late too.

### F10-G08 · S2 · Fig. 61 mini-PBT: English; the would-be BG render is also broken
- **Where:** `renders/ch10/p199_f1.png` — caption "Mini-PBT diversity…"
- **Problem:**
  1. English, at 130 ppi.
  2. I rendered a scratch copy through `render_bg_figures.py` to see what a BG version would look like. The title is clipped and mistranslated: "…загуба на памет при цик", because 'churn' is mapped to "memory loss" (T05). The y-label keeps "(mean pairwise L1 distance)" in English and is clipped. The legend shows "prisoners_dilemma" (unmapped) and "камък_ножица_хартия" (underscores inside the mapping value).
- **Fix:** `implementation/step10/exploration/mini_pbt.py`:
  - Legend labels via a dict: "Prisoner's Dilemma (transitive)", "Rock-Paper-Scissors (cyclic)".
  - Drop `set_title`; ylabel "diversity (mean pairwise L1 distance)"; dpi 120 → 300.
  - Mapping:
    - "Prisoner's Dilemma (transitive)" → 'Дилема на затворника (транзитивна)'.
    - 'Rock-Paper-Scissors (cyclic)' → 'Камък-ножица-хартия (циклична)'.
    - 'diversity (mean pairwise L1 distance)' → 'разнообразие (средно L1 разстояние\nмежду двойките)'.
    - Fix 'rock_paper_scissors' → 'камък-ножица-хартия'.
    - If the title stays: 'Naive PBT: …' → 'Наивно PBT: разнообразието изчезва в транзитивните игри и непрекъснато се мени в цикличните'.

### F10-G09 · S1 · Fig. 62 EGTA: caveat overruns into the neighbouring box, wrong caveat, stale render
- **Where:** `renders/ch10/p200_f1.png` — caption "The EGTA pipeline…"
- **Problem:**
  1. Illegible: the three caveat lines are wider than their box and run over the red "точна експлоатируемост (NashConv, Стъпка 07)" box. "Свиване на σ до една поведенческа стратегия" also overflows its box.
  2. Stale "Стъпка 07".
  3. Top note "…цели стратегии -- повишаване на популацията на експлоатация" is nonsense ("raising of the population of exploitation"), with a literal "--" and straight quotes 'стратегии'. The render is stale: the mapping now says "повдигане … експлоатируемост".
  4. Imperatives "играй всяка двойка", "реши"; "над агентите" is a calque.
  5. Decimal points "3.42", "1.31". These are hard-coded strings, so the tick-formatting fix will not catch them.
  6. The caveat is wrong in substance: "Mixing can add tells" (F10-C03).
  7. Size at scale 0.877: boxes 8.2–8.8 → 7.2–7.7 pt, caveat 7.8 → 6.8 pt, "solve" 7.2 → 6.3 pt.
- **Fix:** `make_egta_figure.py`:
  - EN caveat → "CAVEAT (measured, scale): meta-Nash minimizes META-GAME regret,\nnot full-game exploitability. Its mixture scored 3.42, while the\nleast exploitable agent (1.31) got zero weight."
  - Caveat box h 1.7 → 2.2; exp box label 'EXACT exploitability\n(NashConv, Chapter 7)'; all fs → 10.
  - Mapping:
    - caveat → 'УГОВОРКА (измерено, пълен мащаб): мета-Наш минимизира съжалението\nв МЕТА-ИГРАТА, а не експлоатируемостта в пълната игра. Сместа ѝ има 3,42,\nа най-малко експлоатируемият агент (1,31) получава тегло нула.'
    - 'EXACT exploitability\n(NashConv, Chapter 7)' → 'ТОЧНА експлоатируемост\n(NashConv, Глава 7)'.
    - 'Collapse $\sigma$ to one\nbehavioral policy' → 'Свиване на $\sigma$\nдо една поведенческа\nстратегия'.
    - 'Empirical payoff\nmatrix $M_{ij}$\n(play every pair)' → 'Емпирична матрица\nна печалбите $M_{ij}$\n(всяка двойка се изиграва)'.
    - 'Meta-Nash mixture\n$\sigma$ over agents' → 'Мета-Наш смес\n$\sigma$ върху агентите'.
    - 'solve' → 'решаване' (shared with step 09; the imperative is wrong there too).
    - top note → 'EGTA = равновесие на Наш на игра, чиито „стратегии“ са цели агенти - експлоатируемостта, пренесена на ниво популация.'

### F10-G10 · S1 · Fig. 63 comparison: does not show the result the caption claims
- **Where:** `renders/ch10/p202_f1.png` — caption "…the league's best individual (1.31) beats PSRO (2.16) and self-play (3.68)…"
- **Problem:**
  1. There is no "best individual" bar. `plot_comparison` plots only league (meta-Nash), PSRO, self-play and CFR Nash, so the figure cannot support its own caption.
  2. English title "(PREDICT: CFR Nash ~ 0 is the floor)".
  3. The tick labels come from `ax.bar(labels, …)` and would not be translated.
  4. 121 ppi.
- **Fix:** `plotting.py` `plot_comparison`:
  - Before PSRO, add `labels.append("league\n(best individual)"); vals.append(league["egta"]["best_individual_exploitability"])`.
  - After self-play, add `labels.append("self-play\n(best iterate)"); vals.append(min(base["selfplay"]["exploitability_trajectory"]))` (F10-C04). Rename the self-play bar "self-play\n(final)" and the PSRO bar "PSRO" (static text, not the f-string).
  - `bars = ax.bar(range(len(vals)), vals, …); ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels); ax.bar_label(bars, fmt="%.2f", fontsize=9)`; drop the title; dpi → 300.
  - Mapping:
    - 'league\n(best individual)' → 'лига\n(най-добър агент)'.
    - 'league\n(meta-Nash)' → 'лига\n(мета-Наш смес)'.
    - 'self-play\n(final)' → 'самообучение\n(краен агент)'.
    - 'self-play\n(best iterate)' → 'самообучение\n(най-добра итерация)'.
    - 'CFR Nash' → 'CFR (Наш)'.

### F10-G11 · S2 · No BG twins for six figures; `plotting.py` cannot run under the renderer
- **Where:** `summaryBg.md` links `replicator_playground.png`, `spinning_top.png`, `impl_transitive_ratios.png`, `impl_league_exploitability.png`, `mini_pbt.png`, `impl_comparison_exploitability.png` (EN files). No `_bg` twin of any of them exists in `summary/`, `implementation/step10/implementation/plots/` or `exploration/figures/`.
- **Problem:**
  - `plotting.py` parses `sys.argv` with `argparse`, and `runpy` leaves the renderer's argv in place. With `--only step10` it exits on "unrecognized arguments", which the renderer logs as "ok (exited)" with 0 figures. Without arguments it plots the **smoke** config, not scale.
  - The exploration scripts and `make_spinning_top_figure.py` do render correctly through the renderer; I checked scratch copies, and nothing was written in the repo. So those twins were simply never generated or linked.
  - The three `_bg` diagrams that do exist are stale against the mapping (F10-G02, G09).
- **Fix:**
  1. In `plotting.py` `main()`: `default="smoke"` → `default="scale"` and `args = ap.parse_args()` → `args, _ = ap.parse_known_args()`.
  2. `python scripts/figures/render_bg_figures.py --only step10`. Note that it rewrites the deterministic `replicator_playground.json` / `mini_pbt.json`.
  3. Copy `implementation/step10/implementation/plots/{transitive_ratios,league_exploitability,comparison_exploitability}_bg.png` → `deliverables/reports/step10/summary/impl_*_bg.png`, and `exploration/figures/{replicator_playground,mini_pbt}_bg.png` → `summary/`.
  4. In `summaryBg.md`, change the six links to the `_bg` names.
  5. In any central overflow fix, wrap or enlarge boxes. Never shrink below fs ≈ 9.6.

## B — Bulgarian language

### F10-B01 · S1 · English left in the text
- **Where:** summaryBg.md §§ 10.2, 10.5, 10.7, footnote `vinyals2019`
- **Now → Proposed:**
  - "| **AlphaStar League** | PBT с три типа агенти" → "| **Лига в стила на AlphaStar** | PBT с три типа агенти"
  - "## Лигата AlphaStar-style PBT" → "## PBT лига в стила на AlphaStar"
  - "| CFR-Nash (прагът) | $0.0099$ |" → "| CFR, равновесие на Наш (долна граница) | $0.0099$ |"
  - "*Nature* (AlphaStar; the league and PFSP)." → "*Nature* 575, 350–354 (AlphaStar; лигата и PFSP)."
- **Why:** English prose in the BG bundle, printed on pp. 190, 197, 201, 199. "прагът" (threshold) is not *floor*. The other English fragments are fixed inside the findings that rewrite their sentences: "alphaStar" 2× (B26, B21), "sVD rank-1" (B18), "Smoke's/scale's", "churn" (B11), "naive PBT" (B24), "jSON artifacts" (B23), "p(\text{Hawk})" (B16), and one-pager "лига от тип AlphaStar PBT" (B31).

### F10-B02 · S1 · "smoke / scale / дим" — the run configurations left in English or calqued
- **Where:** summaryBg.md §§ 10.5–10.7 (the lines not rewritten in B11, B22, C03)
- **EN:** "Does it improve? Measured, over two configs (smoke: 7 agents, 15 epochs; scale: 8 agents, 120 epochs, 48 frozen snapshots):"
- **Now → Proposed:**
  - "Измерва ли се подобрение? Оценено върху две конфигурации (smoke: 7 агента, 15 епохи; мащаб: 8 агента, 120 епохи, 48 замразени моментни снимки):" → "Подобрява ли се лигата? Резултатите от двете конфигурации (бърза проверка: 7 агента, 15 епохи; пълен мащаб: 8 агента, 120 епохи, 48 замразени моментни снимки) са следните:"
  - "| Метрика | Smoke | Мащаб |" → "| Показател | Бърза проверка | Пълен мащаб |"
  - "коефициентът на участие се увеличава от $1.0$ (smoke) до $1.9$ (scale)" → "коефициентът на участие нараства от $1.0$ (бърза проверка) до $1.9$ (пълен мащаб)"
  - "дори при scale, където максималното" → "дори при пълен мащаб, където максималното"
  - "| Smoke | $2.665$ | $2.665$ |" → "| Бърза проверка | $2.665$ | $2.665$ |"
  - "| Scale | $3.418$ | $1.305$ |" → "| Пълен мащаб | $3.418$ | $1.305$ |"
  - "| Метод (мащаб) | Крайна експлоатируемост |" → "| Метод (пълен мащаб) | Крайна експлоатируемост |"
- **Why:**
  - English in the text; the curated glossary has "Smoke test → Бърза проверка със смалени бюджети" (T08).
  - "Измерва ли се подобрение?" means "Is improvement measured?". The EN asks whether the league improves.
  - "Оценено върху" is a dangling participle.

### F10-B03 · S1 · meaning — "min-main" as "at a main response"; "ЕЛО"
- **Where:** summaryBg.md § 10.5 table
- **EN:** "| min-main exploitability | $4.67 \to 3.04$ (ends at min) |" / "| final Elo (live agents) |"
- **Now → Proposed:**
  - "| минимална експлоатируемост при основен отговор | $4.67 \to 3.04$ (завършва на мин) |" → "| минимална експлоатируемост сред основните агенти | $4.67 \to 3.04$ (най-ниската стойност е в края) |"
  - "| експлоатируемост на мета-Наш равновесие | $4.73 \to 3.04$ |" → "| експлоатируемост на мета-Наш сместа | $4.73 \to 3.04$ |"
  - "| финален ЕЛО (активни агенти) |" → "| краен рейтинг по Ело (активни агенти) |"
- **Why:** "при основен отговор" means "under a main response". The metric is the minimum over the main agents (`league.py` l. 171–182). Elo is a surname: glossary "Ело", and the one-pager already writes "Ело".

### F10-B04 · S1 · meaning — "научен резултат", "научени методи", "Изпратете" (§ 10.7 closing paragraph)
- **Where:** summaryBg.md § "EGTA - оценка на популацията и неочаквано откритие", the three physical lines after the comparison table
- **EN:** "The league's **best individual** is the strongest learned result — beating exact PSRO and self-play — though all learned methods remain far above the CFR-Nash floor. The league's **mixture** is the weakest, worse even than self-play (the §7 reconciliation). Ship the member, not the mixture."
- **Now → Proposed:** the three lines
  - "Най-добрият индивид от **лигата** е най-силният научен резултат - надминавайки точния PSRO и самообучението -"
  - "въпреки че всички научени методи остават далеч над долната граница на Наш. Сместа от **лигата** е"
  - "най-слабата, дори по-лоша от самообучението (съгласуване в §7). Изпратете индивида, а не сместа.[^lanctot2017]"
  
  → one paragraph: "Най-добрият отделен агент на лигата ($1.305$, най-добрата моментна снимка за цялото обучение) е най-добрият резултат сред методите, основани на обучение, но предимството му трябва да се чете внимателно: PSRO достига $2.163$, а при самообучението най-добрата итерация е $1.396$ (епоха 100) и едва накрая се влошава до $3.683$. Всички тези методи остават далеч над долната граница, зададена от CFR. Мета-Наш сместа на лигата ($3.418$) е по-добра от крайния агент на самообучението, но по-лоша от PSRO и от най-добрия отделен агент (вж. съпоставянето по-горе). Затова като резултат от лигата трябва да се използва избран отделен агент, а не сместа.[^lanctot2017]"
- **Why:**
  - "научен резултат" is a *scientific* result and "научени методи" are methods that *were learned*. The EN means "learned" (trained).
  - "Изпратете" is a calque of *ship*.
  - The content fixes are F10-C02 (the mixture is not worse than self-play) and F10-C04 (best-of-run vs final).

### F10-B05 · S1 · meaning — "безопасността за населението", "отворената врата"
- **Where:** summaryBg.md § "Основни изводи за синтеза на дисертацията", last bullet
- **EN:** "**The population-safety gap is the open door (Contribution #2):** the AlphaStar exploiter mechanism is the population analog of Chapter 8's safe exploitation, but it is heuristic — it neither guarantees monotone improvement nor a non-exploitable mixture."
- **Now → Proposed:** "- **Разликата в безопасността за населението е отворената врата (Принос №2):** експлоатационният механизъм на AlphaStar е аналогът на популацията на безопасната експлоатация от Глава 8, но той е евристичен - нито гарантира монотонно подобрение, нито неексплоатируема смес." → "- **Липсата на гаранция за безопасност на ниво популация е отворен проблем (Принос №2):** механизмът с експлоататори в лигата на AlphaStar е аналог на ниво популация на безопасната експлоатация от Глава 8, но е евристичен: устойчивостта му е показана само емпирично[^vinyals2019], а в малката лига от тази глава той не осигури нито монотонно подобрение, нито неексплоатируема смес."
- **Why:**
  - "населението" is a country's human population, and "Разликата" means a difference. The heading as printed reads "The difference in safety for the population is the open door".
  - "аналогът на популацията" means "the population's analogue".
  - Also SOURCE_GAPS row 3 (F10-S03): softened and cited.

### F10-B06 · S1 · meaning — "RPS 0.0 е транзитивна"; "предварително обучение"
- **Where:** summaryBg.md § "Основни изводи…", first bullet
- **EN:** "is a *pre-training diagnostic* … Measured: RPS $0.0$ transitive, skill ladder $1.0$, PSRO-Leduc $\approx0.45$ (cyclic), league snapshots $\approx0.94$-$0.98$ (transitive)."
- **Now → Proposed:**
  - "*диагностика при предварително обучение*" → "*диагностика преди обучението*"
  - "Измерено: RPS $0.0$ е транзитивна, скала на уменията $1.0$, PSRO-Ледюк $\approx0.45$ (циклична), моментни снимки на лигата $\approx0.94$–$0.98$ (транзитивни)." → "Измерено транзитивно съотношение: „камък-ножица-хартия“ $0.0$, стълбица на уменията $1.0$, PSRO в Ледюк $\approx0.45$ (циклична), моментни снимки на лигата $\approx0.94$–$0.98$ (транзитивна)."
- **Why:** The BG says "RPS is transitive", the opposite of the finding. "Предварително обучение" is *pre-training*, as in language models.

### F10-B07 · S1 · meaning — "колело от броячи" (counters as counting devices)
- **Where:** summaryBg.md § 10.1; onePagerBg.md "**Проблем.**"
- **EN:** "a **cyclic** part (a wheel of counters — there is only *what beats what*)"
- **Now → Proposed:**
  - "(**колело от броячи** - има само *какво побеждава какво*)" → "(**кръг от контрастратегии** - има само *какво побеждава какво*)"
  - onePagerBg: "е скала на уменията или колело от броячи" → "е стълбица на уменията или кръг от контрастратегии"
- **Why:** "брояч" is a counting device. *Counter* here is a counter-move. This is a settled glossary entry (T02).

### F10-B08 · S1 · meaning — "дефект" for *defect* in Prisoner's Dilemma
- **Where:** summaryBg.md § 10.3 table, § 10.6 table; onePagerBg.md
- **Now → Proposed:**
  - "| Дилемата на затворника | Дефект доминира; ESS $(0,1)$ |" → "| Дилемата на затворника | предателството доминира; ESS $(0,1)$ |"
  - "колабира до $0$ (всички → дефект)" → "спада до $0$ (всички → предателство)"
  - onePagerBg: "Дилемата на затворника → всички „Дефект“" → "Дилемата на затворника → всички избират „предателство“"
- **Why:** "дефект" is a flaw or fault. The Bulgarian PD pair is "сътрудничество / предателство", and the settled glossary itself has "mutual defection → взаимно предателство" (T01).

### F10-B09 · S1 · meaning — "намисля се" (is thought up) in the EGTA definition
- **Where:** summaryBg.md § "EGTA - оценка на популацията и неочаквано откритие"
- **EN:** "treat whole policies as the "strategies" of a higher game, play every pair to fill an empirical payoff matrix, solve its **meta-Nash** mixture, and score it. It is the population lift of exploitability — Nash of a game whose atoms are policies."
- **Now → Proposed:** "разглеждат се цялостните политики като „стратегии“ в по-висша игра, изиграва се всяка двойка с цел попълване на емпирична матрица на печалбата, намисля се нейната **мета-Наш** смес и тя се оценява. Това представлява измерване на експлоатируемостта на ниво популация - Нашево равновесие в игра, чиито атоми са политики." → "цели агенти (стратегии за цялата игра) се разглеждат като „чисти стратегии“ на игра от по-високо ниво, всяка двойка агенти се изиграва, за да се попълни емпиричната матрица на печалбите, намира се **мета-Наш** сместа на тази матрица и тя се оценява. Така експлоатируемостта се пренася на ниво популация: търси се равновесие на Наш на игра, чиито „атоми“ са цели стратегии."
- **Why:**
  - "намисля се" means "is thought up" (typo for "намира се").
  - "политики" vs curated "Policy → Стратегия" (T10); "по-висша игра" reads as "a superior game".
  - "Нашево равновесие" (F07-B02 rule).

### F10-B10 · S1 · meaning — one-pager: "(скала)", "оценка на популационно равнище", "противоречаща прогноза", "повече експлоатируема"
- **Where:** onePagerBg.md "**Проблем.**", "Ключови резултати (измерени)"
- **EN:** "Chapter 10 is the population-level layer of the thesis" / "(scale)" / "a contradicted prediction, §4/§7 of the report" / "*Honest negatives (kept predictions).*" / "the **meta-Nash mixture is *more* exploitable than its best member** at scale" / "is **non-monotone at scale**" / "meta-Nash minimizes meta-game regret, not full-game exploitability,"
- **Now → Proposed:**
  - "Глава 10 представлява оценка на популационно равнище" → "Глава 10 е популационното ниво на дисертацията"
  - "достига експлоатируемост **$1.305$** (скала)," → "достига експлоатируемост **$1.305$** (пълен мащаб),"
  - "- противоречаща прогноза (§4/§7 от доклада)." → "- прогноза, която измерванията опровергаха (§3 и §8.2 от доклада)."
  - "*Честни отрицателни (запазени прогнози).*" → "*Отрицателни резултати (запазени прогнози).*"
  - "е **немонотонна в мащаб**" → "е **немонотонна при пълен мащаб**"
  - "**мета-Наш сместа е *повече* експлоатируема от най-добрия си член** в мащаб ($3.418 > 1.305$)" → "**мета-Наш сместа е *по-*експлоатируема от най-добрия член на популацията** при пълен мащаб ($3.418 > 1.305$)"
  - "мета-Наш минимизира мета-игровото съжаление, а не пълната експлоатируемост на играта," → "мета-Наш минимизира съжалението в мета-играта, а не експлоатируемостта в пълната игра,"
- **Why:**
  - "скала" is a scale in the sense of a ladder or dial, not the run size.
  - "представлява оценка" says the chapter *is an evaluation*.
  - "противоречаща" (active: "contradicting") inverts *contradicted*. The report sections are §3 and §8.2, not §4/§7 (F10-C08).
  - "повече експлоатируема" is a non-standard comparative. "Its best member" is not in the mixture (F10-C03).
  - "пълната експлоатируемост на играта" reads as "the complete exploitability of the game"; the EN means exploitability in the full game, as opposed to the meta-game.

### F10-B11 · S1 · § 10.5 reconciliation block: English possessives, "churn", calques, content
- **Where:** summaryBg.md § "Лигата AlphaStar-style PBT", the eight `>` lines after table 36
- **Now:**
  - "> **Съгласуване (запазена прогноза -> какво всъщност се случи).** Прогнозирах *монотонно* намаляване на"
  - "> експлоатируемостта. Smoke's 15 епохи се подчиняват - чисто спадане, което завършва в своя минимум. Но scale's 120"
  - "> епохи разказват истинската история: експлоатируемостта пада рязко до минимум около епоха 60 (минимална експлоатируемост при основен отговор"
  - "> $\approx1.21$, мета-Наш равновесие достига дъно $\approx1.32$ и след това поддържа плато $\approx1.60$), и след това"
  - "> **регресира** обратно до $\approx2.05$ / $\approx2.96$ към епоха 119. Най-добрите агенти са *замразените"
  - "> моментни снимки* от средата на изпълнението; *активните* основни агенти се влошават късно, преследвайки своите експлоатьори (churn /"
  - "> частично забравяне). Това е видимо само когато обучението е достатъчно дълго - една непрекъсната лига не е"
  - "> монотонно подобряваща се. Лекарството (нетествано тук) е съхраняване на най-добрия модел / регуляризация на популацията. Методологически това отразява Глава 9: **мащабът разкрива това, което smoke скрива.**"
- **Proposed** (one `>` paragraph): "> **Съпоставяне (запазена прогноза → какво всъщност се случи).** Очаквах *монотонно* намаляване на експлоатируемостта. При бързата проверка (15 епохи) очакването се потвърждава: спадът е плавен и най-ниската стойност е в края. При пълния мащаб (120 епохи) картината е друга: експлоатируемостта спада рязко през първите около 15 епохи и е най-ниска около епохи 20-40 (мета-Наш сместа достига $\approx1.32$ в епоха 21, а най-добрата моментна снимка е от епоха 29; единичният минимум сред основните агенти, $\approx1.21$, е в епоха 66). След плато ($\approx1.60$ за мета-Наш сместа) тя **нараства отново** до $\approx2.05$ / $\approx2.96$ в епоха 119. Най-добрите агенти са *замразените моментни снимки* от първата половина на обучението; *активните* основни агенти се влошават към края - стратегиите им непрекъснато се сменят и част от наученото се забравя. Самообучението, което няма експлоататори, също се влошава след епоха 100, така че натискът на експлоататорите не е единственото обяснение. Това се вижда само при достатъчно дълго обучение: лигата не се подобрява монотонно. Възможното решение (непроверено тук) е запазване на най-добрата моментна снимка или регуляризация на популацията. Методологично това повтаря извода от Глава 9: **пълният мащаб разкрива това, което бързата проверка скрива.**"
- **Why:**
  - English: "Smoke's", "scale's", "churn".
  - Calques: "се подчиняват" (*oblige*), "разказват истинската история", "достига дъно", "Лекарството" (as F07-B16), "непрекъсната лига" (*running* ≠ continuous).
  - "при основен отговор" (B03). "експлоатьори" (T04).
  - The epoch timing is corrected per F10-C05, and the causal claim is hedged per F10-C04.

### F10-B12 · S2 · meaning — "три основни приноса на тезата", "втори обучаем"
- **Where:** summaryBg.md chapter intro, second paragraph
- **EN:** "**Where this sits in the thesis.** … Chapter 9 added a *second* learner. … It carries three thesis hooks."
- **Now → Proposed:**
  - "**Къде се вписва това в тезата.**" → "**Място в дисертацията.**"
  - "Глава 9 добавя *втори* обучаем." → "Глава 9 добавя *втори* обучаващ се агент."
  - "Тя носи три основни приноса на тезата." → "Тя има три връзки с приносите на дисертацията."
- **Why:** The BG claims the chapter *carries the three main contributions*, which is an overclaim; *hooks* are connection points. *Thesis* here is the dissertation (F07-B23). "обучаем" is an adjective.

### F10-B13 · S2 · calque — "автоматизирани моделиращи съперника - повдигането … прочит"
- **Where:** summaryBg.md intro; onePagerBg.md "**Връзка с дисертацията.**"
- **EN:** "**Main exploiters** are automated opponent modelers — the population lift of Chapter 7's static read (Contribution #1)."
- **Now → Proposed:**
  - "**Основни експлоатьори** са автоматизирани моделиращи съперника - повдигането на популационно ниво на статичния прочит от Глава 7 (Принос №1)." → "**Основните експлоататори** на практика са автоматизирани модели на противника - статичната преценка за противника от Глава 7, пренесена на ниво популация (Принос №1)."
  - onePagerBg: "основните експлоатьори са автоматизирани моделиращи съперника (Принос №1)" → "основните експлоататори на практика са автоматизирани модели на противника (Принос №1)"
- **Why:**
  - A participle used as a noun ("моделиращи").
  - "повдигането" is a calque of *lift*, and "прочит" of poker *read* (F07-B30).
  - "експлоатьори" (T04). The glossary pair is "противник", not "съперник".

### F10-B14 · S2 · calques in § 10.2 — "почине", "ги пресичат", "изчислителната мощност"
- **Where:** summaryBg.md § "Семейството от методи", paragraph after table 33
- **EN:** "Two evaluation tools cut across them. … where a population *flows* and where it can *rest* … *before* you spend the compute"
- **Now → Proposed:**
  - "Два инструмента за оценка ги пресичат." → "Два инструмента за оценка са общи за всички тях."
  - "тя показва къде една популация *тече* и къде може да *почине*." → "тя показва накъде се движи една популация и къде може да се *установи*."
  - "*преди* да бъде използвана изчислителната мощност" → "*преди* да бъдат изразходвани изчислителните ресурси"
- **Why:**
  - "почине" means "take a rest", and in the past tense "почина" means "died".
  - "пресичат" is geometric intersection.
  - "изчислителна мощност" is hardware power (F07-T12).

### F10-B15 · S2 · grammar — dangling participle
- **Where:** summaryBg.md § "Репликаторна динамика…", before table 34
- **Now → Proposed:** "Изпълнен върху четири канонични симетрични игри (с детерминистична динамика, поради което резултатът е недвусмислен), измерените резултати съвпадат напълно с теорията:" → "При четири канонични симетрични игри (динамиката е детерминистична, затова резултатът е еднозначен) измерените резултати съвпадат напълно с теорията:"
- **Why:** "Изпълнен" (masculine singular) has no antecedent. It is the English dangling modifier copied over.

### F10-B16 · S2 · grammar — ESS gender, nonce words
- **Where:** summaryBg.md tables 34 and 37 and text of § 10.3; onePagerBg.md
- **Now → Proposed:**
  - "| Ястреб-гълъб | вътрешно ESS $p(\text{Hawk})=V/C=0.5$ |" → "| Ястреб-гълъб | вътрешна ESS $p(\text{ястреб})=V/C=0.5$ |"
  - "орбитира около центъра с радиус $0.095$" → "обикаля около центъра на разстояние $0.095$"
  - "| Лов на елен | две чисти ESS (басейнозависими) |" → "| Лов на елен | две чисти ESS (според басейна на привличане) |"
  - "ловът на елен избира различно чисто ESS в зависимост от басейна" → "ловът на елен избира различна чиста ESS в зависимост от басейна на привличане"
  - "| Дилемата на затворника (транзитивен) |" → "| Дилемата на затворника (транзитивна) |"
  - "| Камък-ножица-хартия (цикличен) | върти се безкрайно" → "| Камък-ножица-хартия (циклична) | непрекъснато се променя"
  - onePagerBg: "Ястреб–Гълъб → вътрешният $0.5$ ESS (орбитален радиус $0.0$)" → "„Ястреб-гълъб“ → вътрешната ESS $0.5$ (орбитален радиус $0.0$)"
  - onePagerBg: "(орбитира центъра, радиус $0.095$)" → "(обикаля около центъра на разстояние $0.095$)"
  - onePagerBg: "Лов на елен → басейнозависим чист ESS." → "„Лов на елен“ → чиста ESS според басейна на привличане."
- **Why:**
  - ESS is a "стратегия" (feminine). The chapter uses neuter, the one-pager masculine, and § 10.3 feminine.
  - The table labels agree with "игра".
  - "орбитира" and "басейнозависим" are nonce words. "Hawk" is English.

### F10-B17 · S2 · grammar/calque — Hodge table (gender, English word order, "трицикли")
- **Where:** summaryBg.md table 35
- **Now → Proposed:**
  - "| Популация | Транзитивен (Ходж) | Цикличен | Структура |" → "| Популация | Транзитивна компонента (Ходж) | Циклична компонента | Структура |"
  - "| камък-ножица-хартия | $0.0$ | $1.0$ | чисто цикличен |" → "| камък-ножица-хартия | $0.0$ | $1.0$ | чисто циклична |"
  - "| стълбица на чистото умение | $1.0$ | $0.0$ | чисто транзитивен |" → "| стълбица на уменията | $1.0$ | $0.0$ | чисто транзитивна |"
  - "| PSRO-Ледюк **най-добър отговор** мета-игра | $0.41$–$0.46$ | $0.89$–$0.91$ | **предимно цикличен** (27 трицикли) |" → "| мета-игра на най-добрите отговори в PSRO (Ледюк) | $0.41$–$0.46$ | $0.89$–$0.91$ | **предимно циклична** (27 цикъла от три стратегии) |"
  - "| Лига **моментна снимка** мета-игра | $0.94$–$0.98$ | - | **предимно транзитивен** |" → "| мета-игра на моментните снимки на лигата | $0.94$–$0.98$ | - | **предимно транзитивна** |"
- **Why:**
  - The adjectives must agree with "популация" / "компонента".
  - "PSRO-Ледюк най-добър отговор мета-игра" is English noun-stacking.
  - "трицикъл" is a tricycle, the vehicle.

### F10-B18 · S2 · calque/English — the SVD vs Hodge sentence
- **Where:** summaryBg.md § "Въртящият се пумпал…", paragraph after fig. 57
- **EN:** "A subtlety worth flagging: the raw step suggested an **SVD rank-1** decomposition, which wrongly reports Rock-Paper-Scissors as $\approx0.707$ transitive — a rank-1 skew-symmetric approximation simply cannot represent a pure cycle. The implementation uses the **combinatorial-Hodge** (ratings-difference) method instead…"
- **Now → Proposed:** "Една тънкост, която си струва да се отбележи: първоначалната стъпка предполагаше **sVD rank-1** декомпозиция, която неправилно съобщава за $\approx0.707$ транзитивно съотношение на **камък-ножица-хартия** - едно **антисиметрично приближение** с ранг 1 просто не може да представи чист цикъл. Внедряването използва вместо това **комбинаторния-Ходж** (разлика в оценките) метод, който правилно определя транзитивното съотношение на RPS като $0.0$. Измерено:" → "Една тънкост заслужава внимание: първоначалният план предлагаше декомпозиция чрез **SVD с ранг 1**, която неправилно дава транзитивно съотношение $\approx0.707$ за „камък-ножица-хартия“ - сингулярните стойности на антисиметрична матрица винаги са по двойки, затова приближението с ранг 1 обхваща най-много половината от квадрата на нормата ѝ при всяка игра. Реализацията използва вместо това комбинаторното разлагане на Ходж (по разлики в рейтингите)[^balduzzi2018], което правилно дава транзитивно съотношение $0.0$ за „камък-ножица-хартия“. Измерено:"
- **Why:**
  - "sVD rank-1" is English and mis-capitalised.
  - "Внедряването" means deployment; *implementation* is "реализация".
  - "комбинаторния-Ходж … метод" splits the adjective from its noun. "съобщава" is a calque of *reports*.
  - "първоначалната стъпка" is stale (F10-C08).
  - The reason clause follows F10-C09. If C09 is declined, keep "- приближение с ранг 1 не може да представи чист цикъл".
  - The footnote comes from F10-S04.

### F10-B19 · S2 · calque — § 10.4 reconciliation
- **Where:** summaryBg.md § "Въртящият се пумпал…", the `>` block
- **EN:** "I framed poker as a skill ladder … Measured, it depends entirely on *which population you decompose*. … ($\approx0.45$ transitive, 27 three-cycles) … Balduzzi's spinning-top in action."
- **Now → Proposed:**
  - "**Съгласуване (запазена прогноза -> това, което действително се случи).** Аз формулирах покера като стълбица на уменията и очаквах" → "**Съпоставяне (запазена прогноза → какво всъщност се случи).** Бях приел, че покерът е стълбица на уменията, и очаквах"
  - "Измерено, тя зависи изцяло от *коя популация разложите*." → "Измерванията показват, че тя зависи изцяло от това *коя популация се разлага*."
  - "($\approx0.45$ транзитивна, 27 трицикъла)" → "(транзитивно съотношение $\approx0.45$, 27 цикъла от три стратегии)"
  - "въртящият се пумпал на Balduzzi в действие" → "„пумпалът“ на Czarnecki и др. в действие"
- **Why:**
  - "формулирах покера като" is a calque of *framed*. "Измерено," is used as a sentence adverb.
  - "->" should be an arrow, as in the § 10.7 block. "Съгласуване" (*agreement*) does not render *reconciliation*; the same header is changed in B11 and C03.
  - The attribution fix is F10-S04.

### F10-B20 · S2 · meaning — "подкрепата" for the support of a distribution; clustering terms
- **Where:** summaryBg.md § "Разнообразие - наистина ли популацията е разнообразна?"
- **Now → Proposed:**
  - "**поведенческо групиране** (политиките наистина ли са различни?)" → "**поведенческа клъстеризация** (наистина ли стратегиите са различни?)"
  - "но поведенческото групиране свежда всичко до **един клъстер**" → "но поведенческата клъстеризация свежда всичко до **един клъстер**"
  - "методът на единична връзка обединява веригата" → "методът на единичното свързване обединява агентите във верига"
  - "Разнообразието тук е *на ниво тегло* (мета-Наш разпределя подкрепата върху няколко агента), а не *на поведенческо ниво* (агентите играят почти идентично)." → "Разнообразието тук е *на ниво тегла* (мета-Наш сместа разпределя теглото си между няколко агента), а не *на ниво поведение* (агентите играят почти еднакво)."
- **Why:**
  - "подкрепата" means help or backing; *support* of a distribution is its set of non-zero weights.
  - The paragraph mixes "групиране" with "клъстер"/"клъстеризация" (glossary: clustering → клъстеризация). *Single-linkage* is "единично свързване".

### F10-B21 · S2 · meaning — "един най-добър отговор" for "one best"; "поддържат" for "force"
- **Where:** summaryBg.md § 10.6, paragraph after fig. 61
- **EN:** "Transitive games *kill* diversity (there is one best, everyone converges to it); cyclic games *force* it (there is no best, so the population keeps churning). The Leduc league sits near the transitive end, which is exactly why its diversity is thin — and why the AlphaStar diversity benefits reported at ~600 agents do not materialize at this scale."
- **Now → Proposed:** "Транзитивните игри *убиват* разнообразието (съществува един най-добър отговор и всички стратегии се сближават към него), докато цикличните игри го *поддържат* (няма един най-добър отговор, поради което популацията продължава да се променя). Лигата Ледюк е близка до транзитивния край, което е и причината за ниското ѝ разнообразие - както и защо ползите от разнообразието на alphaStar, докладвани при приблизително 600 агента, не се проявяват в този мащаб.[^vinyals2019]" → "Транзитивните игри *унищожават* разнообразието (има една най-добра стратегия и всички се сближават към нея), а цикличните игри го *налагат* (най-добра стратегия няма, затова популацията непрекъснато се променя). Лигата в Ледюк е близо до транзитивния край - затова разнообразието ѝ е ниско и затова ползите от разнообразието, описани за AlphaStar, където по време на обучението са създадени близо 900 различни агента, не се проявяват в този мащаб.[^vinyals2019]"
- **Why:**
  - "най-добър отговор" is a technical term (a best response to an opponent). The EN means one best *strategy*.
  - "поддържат" weakens *force*, and the takeaways already say "налагат".
  - "alphaStar", "докладвани" (a calque of *reported*), "Лигата Ледюк".
  - 600 → 900 per F10-S05.

### F10-B22 · S2 · calque — § 10.8 "Какво не се получи"
- **Where:** summaryBg.md § "Честни бележки, ограничения и предаване на щафетата", second paragraph
- **EN:** "Three honest caveats travel forward. … a running league is not a monotonically improving one … ship a member, not the mixture … **transitive as a snapshot population** … invisible at the fast smoke config — scale reveals what smoke hides."
- **Now → Proposed:** "**Какво не се получи и защо това има значение.** Три честни уговорки вървят напред. (1) Експлоатируемостта на лигата **претърпява късна регресия** в мащаб ($4.73\to\approx1.21\to\approx2.05$) - непрекъснатата лига не е монотонно подобряваща се; най-добрите агенти са замразени моментни снимки. (2) **Мета-Наш сместа е по-експлоатируема от своя най-добър член** в мащаб ($3.42$ срещу $1.31$) - смесването на поведенчески политики не гарантира устойчивост, затова изпратете член, а не сместа. (3) Мета-играта на Ледюк е **циклична като популация на най-добри отговори**, но **транзитивна като моментна популация** - структурата е свойство на популацията, която се изгражда. И един методологичен момент: късната регресия и провалът при смесването са невидими в бързата конфигурация на дима - мащабът разкрива това, което димът скрива." → "**Какво не се получи и защо това има значение.** Три уговорки остават валидни и за следващите глави. (1) При пълен мащаб експлоатируемостта на лигата **нараства отново в края на обучението** ($4.73\to\approx1.21\to\approx2.05$) - лигата не се подобрява монотонно, а най-добрите агенти са замразени моментни снимки. (2) При пълен мащаб **мета-Наш сместа е по-експлоатируема от най-добрия член на популацията** ($3.42$ срещу $1.31$), защото не му дава никакво тегло - изборът на мета-Наш не гарантира устойчивост, затова като резултат трябва да се използва избран отделен агент, а не сместа. (3) Мета-играта на Ледюк е **циклична като популация от най-добри отговори**, но **транзитивна като популация от моментни снимки** - структурата е свойство на начина, по който е изградена популацията. И един методологичен извод: късната регресия и слабостта на сместа не се виждат при бързата проверка - пълният мащаб разкрива това, което бързата проверка скрива."
- **Why:**
  - "конфигурация на дима" means "the configuration of the smoke". "вървят напред" is a calque; "изпратете" (*ship*).
  - "моментна популация" means a momentary population.
  - The content fix is F10-C03: the best member is not a member of the mixture.

### F10-B23 · S2 · calque/English — "Доверие" paragraph
- **Where:** summaryBg.md § 10.8, "**Доверие.**"
- **Now → Proposed:** "**Доверие.** Всяка еволюционна цел е *аналитична* (ESS/Наш равновесие на матричните игри), а всяка експлоатируемост на лигата е *точният* NashConv от глава 07 върху таблично извлечена политика - така че игровотеоретичните резултати са ограничени от обективната истина. Невронните резултати са едно PBT изпълнение на конфигурация: *посоките* (ранно подобрение, най-добър индивид < PSRO < самообучение, късна регресия, мета-Наш > най-добър член) представляват надеждните твърдения, а не величините с третия десетичен знак. Експерименталните PNG изображения по-горе са генерирани от ангажираните jSON artifacts (виж `../figures/README.md`); концептуалните диаграми са създадени от скриптовете `make_*_figure.py`." → "**Доверие.** Всяка еволюционна цел е *аналитична* (ESS или равновесие на Наш на матричните игри), а всяка стойност на експлоатируемостта в лигата е *точният* NashConv от Глава 7, изчислен върху таблично извлечените стратегии - така игровотеоретичните резултати са проверени спрямо точни стойности. Невронните резултати идват от едно изпълнение на PBT за всяка конфигурация: надеждни са *посоките* (ранно подобрение; най-добрата моментна снимка < PSRO < крайния агент на самообучението; късна регресия; мета-Наш сместа > най-добрия член на популацията), а не точните стойности до третия десетичен знак. Графиките с експериментални резултати са построени от съхранените в проекта JSON файлове с резултати, а концептуалните диаграми - от скриптовете `make_*_figure.py`."
- **Why:**
  - "ангажираните" is a calque of git *committed*. "jSON artifacts" is English and mis-capitalised.
  - The relative repository path means nothing in a 226-page bundle.
  - "ограничени от обективната истина" is a calque of *bounded by ground truth*.

### F10-B24 · S2 · calque/English — "Обратни и бъдещи връзки"
- **Where:** summaryBg.md § 10.8, last paragraph
- **Now → Proposed:** "**Обратни и бъдещи връзки.** Обратно: лигата е асинхронизиран вариант на PSRO от глава 9, използващ невронни предсказвачи, и тя изцяло възприема точния най-добър отговор от глава 07; „мета-Наш на популация“ представлява Наш от глава 2, повдигнат на едно ниво. Бъдеще: основните експлоатьори са автоматизирани моделиращи съперника (Принос №1); EGTA/мета-Наш е методологията за оценяване (Принос №3); а липсващата гаранция на лигата - тя може да претърпи регресия и нейната смес може да бъде експлоатируема - е популационната форма на **липсващия $N>2$ предпазен ограничител** (Принос №2). Транзитивната/циклична диагностика предсказва, че коалиционните игри от глава 11 ще бъдат силно циклични, така че naive PBT там ще се държи циклично." → "**Връзки с предходните и следващите глави.** С предходните: лигата е асинхронен вариант на PSRO от Глава 9 с невронни предсказвачи и изцяло използва точния най-добър отговор от Глава 7; „мета-Наш на популация“ е равновесието на Наш от Глава 2, пренесено едно ниво по-горе. Със следващите: основните експлоататори на практика са автоматизирани модели на противника (Принос №1); EGTA/мета-Наш е методологията за оценяване (Принос №3); а липсващата гаранция на лигата - тя може да се влоши и сместа ѝ може да е експлоатируема - е популационната форма на **липсващата опора за безопасност при $N>2$ играчи** (Принос №2). Транзитивната/цикличната диагностика предсказва, че коалиционните игри всеки срещу всеки от Глава 11 ще бъдат силно циклични, така че наивното PBT там ще зацикли."
- **Why:**
  - English "naive". "Обратно:" means "conversely"; "Бъдеще:" is a bare noun.
  - "предпазен ограничител" is a mechanical safety limiter; the EN means *anchor*.
  - The EN "FFA" was dropped. Lower-case "глава" and "07" appear against "Глава 7" elsewhere.

### F10-B25 · S2 · calque — takeaways 3 and 4
- **Where:** summaryBg.md § "Основни изводи…", bullets 3–4
- **Now → Proposed:**
  - "- **Мета-Наш оптимизира мета-игровото съжаление, а не пълната експлоатируемост на играта**" → "- **Мета-Наш оптимизира съжалението в мета-играта, а не експлоатируемостта в пълната игра**"
  - "така че оценката на популацията трябва директно да оценява колапсиралата смес и да изпраща избран член." → "затова при оценката на популацията експлоатируемостта на сместа трябва да се измерва пряко, а като резултат да се използва избран отделен агент."
  - "прави всяко твърдение за популацията проверено на място - същият NashConv от Глава 2." → "прави всяко твърдение за популацията проверимо спрямо точни стойности - със същия NashConv като в Глава 2."
- **Why:** *full-game* (B10). "изпраща" (*ship*), "колапсиралата" (*collapsed*) and "проверено на място" (*ground-truthed*) are calques.

### F10-B26 · S2 · meaning/calque — chapter intro
- **Where:** summaryBg.md, first paragraph under the chapter heading
- **EN:** "This is a ground-up chapter … a small AlphaStar-style **league** built on a solvable poker game … bounded by *exact* references (analytic ESS/Nash for the matrix games; Chapter 07's exact best-response exploitability for Leduc)"
- **Now → Proposed:**
  - "Това е цялостна глава за обучение и оценка на **популации** от агенти:" → "Тази глава изгражда от основите темата за обучение и оценка на **популации** от агенти:"
  - "малка **лига** в стил alphaStar, изградена върху решима покер игра" → "малка **лига** в стила на AlphaStar, изградена върху решим вариант на покер"
  - "са ограничени от *точни* референции (аналитично равновесие на Еволюционно стабилни стратегии/Наш за матричните игри; точната експлоатируемост по най-добър отговор от Глава 07 за Ледюк)" → "са съпоставени с *точни* еталонни стойности (аналитичните ESS и равновесия на Наш за матричните игри; точната експлоатируемост спрямо най-добър отговор от Глава 7 за Ледюк)"
- **Why:**
  - *Ground-up* means from first principles; "цялостна" means comprehensive.
  - "равновесие на Еволюционно стабилни стратегии/Наш" does not parse and carries a capital mid-phrase.
  - "референции" is a calque (cf. F07-B11). "alphaStar" is misspelled.

### F10-B27 · S2 · grammar — "с спаринг", nonce verb
- **Where:** summaryBg.md § 10.1, dojo paragraph
- **Now → Proposed:**
  - "Поддържате зала, пълна с **спаринг партньори**" → "Поддържате зала, пълна със **спаринг партньори**"
  - "учениците спарингуват, силните се копират и леко мутират" → "учениците тренират помежду си, по-силните се копират и леко се изменят"
- **Why:** "с" becomes "със" before с/з. "спарингуват" is not a Bulgarian verb.

### F10-B28 · S2 · meaning — method table cells
- **Where:** summaryBg.md table 33
- **Now → Proposed:**
  - "цикли / забравя в циклични игри" → "зацикля и забравя в цикличните игри"
  - "пълен най-добър отговор на рунд; *смесването* не е решението (виж §7)" → "пълен най-добър отговор на всеки кръг; *сместа* не е решението (вж. §10.7)"
  - "може да намали разнообразието или да регресира (виж §5)" → "може да загуби разнообразието си или да регресира (вж. §10.5)"
- **Why:**
  - "цикли" reads as the plural noun "cycles", not the verb.
  - "смесването" is the act of mixing; the EN means the *mixture*.
  - "рунд" is a sports round. "виж" → "вж.". The section numbers follow F10-X01.

### F10-B29 · S2 · terminology — "Наш равновесие" word order (F07-B02 rule)
- **Where:** summaryBg.md table 34
- **Now → Proposed:** "Наш равновесие = равномерно" → "равновесие на Наш = равномерна стратегия"
- **Why:** The concept is "равновесие на Наш" (glossary; F07-B02), and "равномерно" has no noun. The other occurrences are rewritten in B09, B23, B31 and B01 ("CFR-Nash").

### F10-B30 · S2 · terminology — within-chapter inconsistencies (skill ladder, exploiter, spinning top, policy, title, EGTA, RPS)
- **Where:** summaryBg.md throughout (occurrences not rewritten in other findings)
- **Now → Proposed:**
  - "(истинска **скала на уменията** - съществува *по-добър играч*)" → "(истинска **стълбица на уменията** - съществува *по-добър играч*)" (the chapter also has "стълбица на уменията" and "стълбица на чистото умение"; *ladder* = стълбица, and "скала" collides with "мащаб/scale", see B10)
  - "в настоящите ученици (експлоатьори)" → "в настоящите ученици (експлоататори)"
  - "**основни експлоатьори** (търсят слабости в *текущите* основни) и **експлоатьори в лигата**" → "**основни експлоататори** (търсят слабости в *текущите* основни агенти) и **експлоататори на лигата**" (table 33 already says "експлоататор на лигата"; T04)
  - "## Въртящият се пумпал - транзитивна спрямо циклична структура" → "## „Пумпалът“ - транзитивна и циклична структура"
  - "Транзитивното/цикличното (пумпал) съотношение" → "Транзитивното/цикличното съотношение („пумпал“)" (curated: Декомпозиция „пумпал“)
  - "обучава последната политика срещу (копие на) самата себе си" → "обучава последната стратегия срещу (копие на) самата себе си"
  - "Извличането на невронни политики в табличен вид" → "Извличането на невронните стратегии в табличен вид" (curated Policy → Стратегия; T10)
  - "# Глава 10 - Обучение, базирано на популации и еволюционна теория на игрите" → "# Глава 10 - Обучение на базата на популации и еволюционна теория на игрите" (curated; YAML already has "на базата на"). In the YAML title "…и Еволюционна теория на игрите" → "…и еволюционна теория на игрите".
  - "Последният инструмент е **емпиричен игровотеоретичен анализ (EGTA)**:" → "Последният инструмент е **емпиричният теоретико-игрови анализ (EGTA)**:" (curated)
  - footnote: "ESS и центърът на RPS" → "ESS и центъра при „камък-ножица-хартия“"
- **Why:** One concept, one word. "RPS" is an English abbreviation the BG text never defines. The other occurrences are rewritten in B06, B18, S02 and B31.

### F10-B31 · S2 · calques — one-pager
- **Where:** onePagerBg.md "**Проблем.**", "**Подход.**", "Ключови резултати", "**Връзка…**", "**Отворени въпроси.**"
- **Now → Proposed:**
  - "без минимакс котва (#2)" → "без опора в минимаксната стойност (#2)"
  - "и транзитивната/цикличната **пумпал** декомпозиция" → "и декомпозицията „пумпал“ на транзитивна и циклична част"
  - "**Част II - лига от тип AlphaStar PBT** от невронни PPO агенти" → "**Част II - PBT лига в стила на AlphaStar** от невронни PPO агенти"
  - "(три типа агенти: основен / експлоатер на основната стратегия / експлоатер на лигата, плюс замразяване и PFSP)" → "(три типа агенти: основни агенти / основни експлоататори / експлоататори на лигата, плюс замразяване и PFSP)"
  - "Декомпозицията на Ходж дава RPS транзитивни $0.0$ / циклични $1.0$ и скала на уменията $1.0$ / $0.0$ (методът SVD с ранг 1 неправилно дава RPS $0.707$)." → "Декомпозицията на Ходж дава за „камък-ножица-хартия“ транзитивна компонента $0.0$ и циклична $1.0$, а за стълбицата на уменията - $1.0$ и $0.0$ (методът SVD с ранг 1 неправилно дава $0.707$ за „камък-ножица-хартия“)."
  - "Мета-играта **най-добър отговор** на PSRO върху Ледюк е предимно **циклична** ($\approx0.45$ транзитивни, 27 трицикли); мета-играта на **моментната снимка на лигата**" → "Мета-играта на **най-добрите отговори** в PSRO за Ледюк е предимно **циклична** (транзитивно съотношение $\approx0.45$, 27 цикъла от три стратегии); мета-играта на **моментните снимки на лигата**"
  - "CFR-Наш долната граница е $0.0099$." → "долната граница, CFR (равновесие на Наш), е $0.0099$."
  - "**липсващия $N>2$ предпазен ограничител**" → "**липсващата опора за безопасност при $N>2$ играчи**"
  - "Премахва ли **задържането на моментна снимка** / **регуляризацията на популацията** късната регресия (поправка в обучението), или тя е присъща на тритипния дизайн (поправка в дизайна)?" → "Премахва ли **запазването на най-добрата моментна снимка** или **регуляризацията на популацията** късната регресия (поправка в обучението), или тя е присъща на дизайна с три типа агенти (поправка в дизайна)?"
  - "Трябва ли една популация да изпрати избран **най-добър устойчив отговор елемент**, или" → "Трябва ли като резултат от популацията да се използва избран член, **устойчив срещу най-добър отговор**, или"
  - "И подлежащо и на двете:" → "И по-дълбокият въпрос зад двата:"
  - "може ли **експлоатационният механизъм** да получи гаранция" → "може ли **механизмът с експлоататори** да получи гаранция"
- **Why:**
  - "котва" is a calque of *anchor*. "експлоатер на основната стратегия" says the exploiter targets a *strategy*, when it targets the main agents; "експлоатер" is the fourth variant of the word (T04).
  - English noun-stacking; "трицикли" (tricycles).
  - "задържането на моментна снимка" drops *best*. "тритипния" is a nonce word.
  - "най-добър устойчив отговор елемент" does not parse. "подлежащо" is a calque of *underneath*.

### F10-B32 · S3 · first mention — PFSP never expanded
- **Where:** summaryBg.md § 10.5 — "**PFSP** сдвояването избира всеки противник"
- **Now → Proposed:** "**PFSP** сдвояването избира всеки противник" → "сдвояването по **PFSP** (приоритизирана фиктивна игра срещу себе си, Prioritized Fictitious Self-Play) избира всеки противник"; EN "**PFSP** matchmaking" → "**PFSP** (prioritized fictitious self-play) matchmaking"
- **Why:** This is the first-mention rule (terminology rule 1). The name is verified in Vinyals et al. (2019): "a prioritized fictitious self-play (PFSP) mechanism".

## T — Glossary-level terminology

### F10-T01 · S1 · "defect → дефект", "defectors → дефектьори"
- **Where:** `llmPipeline/glossary_settled.md`; printed in ch. 10 (F10-B08)
- **Now → Proposed:** defect → "предателство" (verb "предава"); defectors → "предатели"; cooperate → "сътрудничество"
- **Why:** "дефект" is a flaw. The same glossary already has "mutual defection → взаимно предателство".

### F10-T02 · S1 · "wheel of counters → колело от броячи"
- **Now → Proposed:** → "кръг от контрастратегии" (and *counter* in this sense → "контрастратегия", which is already settled)
- **Why:** "брояч" is a counting device (F10-B07; figure mapping '#броячи', F10-G04).

### F10-T03 · S2 · "self-play → самообучение" (freq 43)
- **Now → Proposed:** → "игра срещу себе си" (noun phrase; "обучение чрез игра срещу себе си" where the process is meant)
- **Why:** "самообучение" means self-learning or self-study. Ch. 10 also uses it for *self-training* ("процесът на самообучение", "самообучаваща се популация"), so self-play and self-training become one word and the distinction the chapter draws disappears. The change affects 14 places in this chapter and figure labels (F10-G06, G10). The proposals in this file keep "самообучение" until this is decided.

### F10-T04 · S2 · exploiter: three coinages
- **Where:** settled "main exploiters → основни експлоататори", "league exploiters → експлоатьори в лигата", "exploiters → експлоатьори", "adaptive exploiter → адаптивен експлоатер"
- **Now → Proposed:** → "експлоататор" throughout; "league exploiters → експлоататори на лигата"
- **Why:** Ch. 10 prints all three forms, and the one-pager adds "експлоатер". Only "експлоататор" is a Bulgarian word; "-ьор" is a French-loan suffix. The league exploiters exploit *the league*; they are not "в лигата". This is consistent with F07-B36.

### F10-T05 · S2 · "churn → загуба на памет"
- **Now → Proposed:** → "непрекъсната смяна (на стратегиите)"
- **Why:** *churn* is continual turnover, not memory loss. The entry feeds the fig. 61 title (F10-G08).

### F10-T06 · S2 · non-words in the settled glossary
- **Now → Proposed:** "best responder → най-добър отговорчик" → "агентът, който играе най-добър отговор"; "info-set tells → информационен комплект подсказки" → "издайнически сигнали в информационните множества"; "running league → непрекъсната лига" → "лигата по време на обучение"
- **Why:** "отговорчик" is not a word, and "информационен комплект подсказки" does not parse. Both entered ch. 10's § 10.7 (F10-C03).

### F10-T07 · S2 · curated attribution "Spinning top decomposition … (Balduzzi et al., 2019)"
- **Where:** `deliverables/terminology_EN_BG.md` l. 92
- **Now → Proposed:** note → "Transitive–cyclic decomposition: Balduzzi et al., 2018, 2019; the "spinning top" geometry: Czarnecki et al., 2020"
- **Why:** This is the same misattribution as `lit_gaps.md` lists for steps 10–11 (F10-S04). The curated file propagates it.

### F10-T08 · S2 · smoke / scale runs
- **Where:** curated "Smoke test → Бърза проверка със смалени бюджети" vs settled "smoke-run → пробно изпълнение"
- **Now → Proposed:** one pair for run configurations: smoke → "бърза проверка", scale → "пълен мащаб"
- **Why:** Ch. 10 uses neither: it has English "smoke/scale" and the calque "дим" (F10-B02). Other chapters with smoke/scale runs (09, 11) need the same pair.

### F10-T09 · S2 · "rest point → равновесна точка"; "uniform centre → равновесна точка"
- **Now → Proposed:** rest point → "точка на покой" (as ch. 10's text uses); uniform centre → "равномерният център (1/3, 1/3, 1/3)"
- **Why:** "равновесна точка" collides with Nash equilibrium, which makes "rest points ↔ Nash" a tautology in Bulgarian (fig. 55). The second entry is wrong outright.

### F10-T10 · S2 · "policy → политика" family vs curated "Policy → Стратегия"
- **Where:** settled "nash policy → политика на Наш", "population of policies → съвкупност от политики", "tabular-extracted policies → таблично извлечена политика", "policy iteration → итерация на политиката", …
- **Now → Proposed:** align the settled entries with the curated rule ("стратегия"; "итерация по стратегии")
- **Why:** Ch. 10 mixes "политика" (8×) and "стратегия" for the same object.

## C — Content

### F10-C01 · S1 · "Rest points are exactly Nash equilibria; stable rest points are ESS" — false
- **Where:** summaryEn l. 90–92; summaryBg § 10.3 (below) and its heading; fig. 55 box (F10-G02); report_en §2 Conclusion ("their rest points are exactly Nash/ESS")
- **Problem:** For the replicator equation, every Nash equilibrium is a rest point, but not conversely: every pure strategy is a rest point, e.g. all-Cooperate in PD. Stable rest points are Nash equilibria. Every ESS is an asymptotically stable rest point, and "the converse does not hold in general". Hofbauer & Sigmund (2003), *Bull. AMS* 40(4), §2.3 ("None of the converse statements holds") and §2.6. ESS can also be pure (PD, Stag Hunt), so "mixes" is too narrow.
- **Now → Proposed:**
  - "## Репликаторна динамика - равновесия на популацията" → "## Репликаторна динамика - къде една популация може да се установи"
  - "Точките на покой съвпадат точно с равновесията на Наш; *стабилните* точки на покой са **еволюционно стабилни стратегии (ESS)** - смесени стратегии, които, след като бъдат възприети от цялата популация, не могат да бъдат изместени от малък дял мутанти. Това представлява непрекъснатото идеализиране на това, което една PBT лига прави дискретно: копиране на по-добрите агенти (подбор) и тяхното смущаване (мутация)." → "Всяко равновесие на Наш е точка на покой, но не и обратното - например всяка чиста стратегия също е точка на покой. Устойчивите точки на покой обаче винаги са равновесия на Наш, а всяка **еволюционно стабилна стратегия (ESS)** - чиста или смесена стратегия, която, възприета от цялата популация, не може да бъде изместена от малък дял мутанти - е асимптотично устойчива точка на покой[^hofbauer2003]. Това е непрекъснатата идеализация на онова, което PBT лигата прави дискретно: копира по-успешните агенти (подбор) и внася малки случайни промени в тях (мутация)."
  - EN l. 90–92: "Its rest points are exactly Nash equilibria; the *stable* rest points are **evolutionarily stable strategies (ESS)** — mixes that, …" → "Every Nash equilibrium is a rest point, but not conversely (every pure strategy is one too); stable rest points are Nash equilibria, and every **evolutionarily stable strategy (ESS)** — a pure or mixed strategy that, once adopted by the whole population, cannot be invaded by a small mutant share — is an asymptotically stable rest point.[^hofbauer2003]"
  - report_en l. 43: "their rest points are exactly Nash/ESS" → "every Nash equilibrium is one of their rest points and every ESS an asymptotically stable one".
- **Note:** "смущаване" (perturbing = embarrassing/disturbing) and "идеализиране" are fixed in the same sentence. The footnote is new (F10-S02).

### F10-C02 · S1 · "The league's mixture is the weakest, worse even than self-play" — false
- **Where:** summaryEn l. 269–270 and table l. 258–264; fig. 63 caption; report_en l. 141–143 ("is the *weakest*, worse even than self-play"), l. 147; BG text in F10-B04
- **Problem:** Lower is better. The mixture scores 3.418 and self-play 3.683, so the mixture beats the final self-play agent. The weakest learned result is self-play's final agent. The table order (mixture last) reinforces the error.
- **Now → Proposed** (BG table): "| Самообучение | $3.683$ |" → "| Лига - мета-Наш смес | $3.418$ |"; "| Лига - мета-Наш смес | $3.418$ |" → "| Самообучение (краен агент) | $3.683$ |" (i.e. swap the rows); EN likewise ("| Self-play (final agent) | $3.683$ |" last). EN l. 269–270 → "The league's **mixture** ($3.418$) is better than the final self-play agent but worse than PSRO and the best individual."
- **Report:** l. 143 "the *weakest*, worse even than self-play" → "worse than PSRO and the best individual, though better than the final self-play agent".

### F10-C03 · S1 · The "tells" explanation is contradicted by the data; "its best member" is not a member
- **Where:** summaryEn l. 244–254; summaryBg § 10.7 reconciliation (below); § 10.8 item (2) (F10-B22); takeaways; one-pager EN l. 45–47 / BG (below); fig. 62 caveat (F10-G09); report_en §8.1 l. 155
- **Problem:** `scale_results.json` → `league.egta` gives the mixture weights main_1#e119 0.645 (NashConv 3.932), main_0 0.322 (3.558), mexp_0 0.032 (4.262).
  - The collapsed mixture scores **3.418, lower than every component** (weighted mean 3.82). Mixing *reduced* exploitability, so "a realization-weighted mixture … can be *more* exploitable than its components, because the blend introduces … tells" is not what happened.
  - The least exploitable agent, main_2#e29 (1.305), has weight 0. So the mixture is worse than *the population's* best member, which is not "its" member.
  - The correct explanation is the one the paragraph already gives first: meta-Nash weights agents by results against the population (meta-game regret), not by full-game exploitability.
- **Now → Proposed** (BG, the whole `>` line): "> **Съгласуване (запазена прогноза → какво всъщност се случи).** Очаквах **мета-Наш смес** да бъде поне толкова **неексплоатируема**, колкото нейният най-добър елемент. Smoke го потвърди тривиално - **мета-Наш** постави *цялото* тегло върху единствения най-добър агент, така че мета = най-добър = $2.665$. При мащаб **мета-Наш** разпределя тегло ($0.645$ върху един агент плюс опашка), а колапсираната **поведенческа смес** отбелязва $3.418$ - **по-лошо** от най-добрата единична моментна снимка ($1.305$). Това не е грешка в смесването (същият кодов път даде мета = най-добър в smoke). **Мета-Наш** минимизира **мета-игрово съжаление** - справяне добре *срещу популацията* - което е *различна цел* от минимизирането на **пълна експлоатируемост на играта**; и реализационно претеглена смес от поведенчески политики може да бъде *по-експлоатируема* от своите компоненти, защото блендът въвежда „разкриващи“ информационни множества, които най-добрият отговорчик наказва. Изводът се обръща: това, което една **лига** трябва да *изпрати*, е избран, **най-добър устойчив на отговор елемент** - а не **мета-Наш смес**." → "> **Съпоставяне (запазена прогноза → какво всъщност се случи).** Очаквах **мета-Наш сместа** да бъде поне толкова **неексплоатируема**, колкото най-добрият член на популацията. Бързата проверка го потвърди тривиално: **мета-Наш** даде *цялото* тегло на единствения най-добър агент, така че сместа = най-добрия = $2.665$. При пълния мащаб **мета-Наш** разпределя теглото ($0.645$ върху един агент и по-малки тегла върху още два), а сместа, сведена до една поведенческа стратегия, има експлоатируемост $3.418$ - **по-висока** от тази на най-добрата отделна моментна снимка ($1.305$). Това не е грешка в смесването: същият код дава смес = най-добрия при бързата проверка, а сместа е по-малко експлоатируема от всеки от трите си компонента ($3.558$, $3.932$ и $4.262$). Причината е в целта: **мета-Наш** минимизира **съжалението в мета-играта** - тоест доколко добре се представя *срещу популацията* - а това е *различна цел* от минимизирането на **експлоатируемостта в пълната игра**. Затова най-малко експлоатируемите агенти получиха тегло нула. Изводът е обратен на очакването: като резултат от лигата трябва да се използва избран член, **устойчив срещу най-добър отговор**, а не **мета-Наш сместа**."
  - onePagerBg: "така че смесването на поведенчески стратегии може да навреди" → "а мета-Наш не даде никакво тегло на най-малко експлоатируемия агент"
  - EN l. 251–254: replace "; and a realization-weighted mixture of behavioral policies can be *more* exploitable than its components, because the blend introduces information-set "tells" that an exact best responder punishes" with ". The mixture is in fact *less* exploitable than each of its three components ($3.558$, $3.932$, $4.262$); the least exploitable agent ($1.305$) simply received zero meta-Nash weight". In l. 245 and elsewhere, "its best member" → "the population's best member". One-pager EN "so mixing behavioral policies can hurt" → "and the meta-Nash gave zero weight to the least exploitable agent".
- **Note:** The BG replacement also removes "блендът", "отговорчик" (T06), "изпрати", "отбелязва", "кодов път" and "Smoke/smoke".

### F10-C04 · S1 · Overclaim — "the best individual beats self-play" compares best-of-run with a final iterate
- **Where:** summaryEn l. 268, 280–281, 297, 317–318; one-pager l. 41–42; BG takeaway 2 (below), § 10.7 (B04), § 10.8 (S02, B23), one-pager (below); fig. 59 note, fig. 63; report_en §7, §9, §11
- **Problem:**
  - The league figure 1.305 is the minimum over 56 agents across 120 epochs, selected with the exact oracle. Self-play's 3.683 is its *final* iterate.
  - Self-play's own trajectory (`baselines.selfplay.exploitability_trajectory`) reaches **1.396 at epoch 100** and then collapses to 3.68.
  - Like for like, best-of-run gives 1.305 (league), 1.396 (self-play) and 2.163 (PSRO, whose final value is also its best). With one run each, 1.305 vs 1.396 is not a meaningful difference.
  - Self-play also regresses late without any exploiters, which weakens "the live agents … chasing their exploiters" as *the* cause (B11).
- **Now → Proposed:**
  - "- **Лигата произвежда силни индивиди, но не носи гаранция.** Най-добрият модел $1.305$ побеждава PSRO $2.163$ и самообучението $3.683$ - въпреки това експлоатируемостта *регресира* късно ($\to2.05$), а мета-Наш *сместа* ($3.42$) е по-лоша от най-добрия си член ($1.31$)." → "- **Лигата произвежда силни отделни агенти, но не носи гаранция.** Най-добрата моментна снимка ($1.305$) е по-добра от PSRO ($2.163$) и сравнима с най-добрата итерация на самообучението ($1.396$) - и двете при едно изпълнение; въпреки това експлоатируемостта *нараства отново* към края ($\to2.05$), а мета-Наш *сместа* ($3.42$) е по-лоша от най-добрия член на популацията ($1.31$)."
  - onePagerBg: "надминавайки точния PSRO ($2.163$) и самообучението ($3.683$);" → "по-добре от PSRO с точен предсказвач ($2.163$) и сравнимо с най-добрата итерация на самообучението ($1.396$; крайният агент е $3.683$);"
  - EN takeaway: "Best snapshot $1.305$ beats PSRO $2.163$ and self-play $3.683$" → "Best snapshot $1.305$ beats PSRO $2.163$ and matches self-play's best iterate ($1.396$; its final agent is $3.683$) — one run each"; the same in the EN one-pager and in report §7 and §11.

### F10-C05 · S2 · Trajectory timing: the minimum is not "near epoch 60"
- **Where:** summaryEn l. 184–186; fig. 60 caption; report_en l. 87 "(ep ~64)", l. 92 "near epoch 60-65", l. 96, l. 159; BG block in F10-B11
- **Problem:** From `league.trajectory` (scale):
  - The steep fall is over by epoch ~14 (min-main 1.40).
  - Decade means of min-main are 3.46, 1.56, **1.36, 1.39**, 1.71, 1.65, 1.71, 1.74, 1.77, 2.05, 1.99, 2.11.
  - The meta-Nash minimum is **1.323 at epoch 21**. The min-main single low 1.212 is at **epoch 66**, not 64, and it is an isolated dip. The best snapshot is from epoch 29.
  - The 1.598 "plateau" is 18 epochs between 41 and 74.
  - So the lowest band is epochs 20–40, and the rise starts around epoch 90.
- **Fix:** EN l. 184–186: "exploitability falls steeply to a minimum near epoch 60 (min-main $\approx1.21$, meta-Nash bottoming $\approx1.32$ then holding a $\approx1.60$ plateau)" → "exploitability falls steeply within ~15 epochs and is lowest around epochs 20–40 (meta-Nash $\approx1.32$ at epoch 21; best snapshot from epoch 29; the single lowest min-main value, $\approx1.21$, at epoch 66), then holds a $\approx1.60$ meta-Nash plateau". "*frozen snapshots* from mid-run" → "from the first half of the run". Report "(ep ~64)" → "(ep 66)". Caption per F10-G01.

### F10-C06 · S2 · Two different "final meta-Nash" values at scale, unexplained
- **Where:** summaryEn table l. 177 (→ $2.96$) vs l. 239 / l. 264 ($3.418$); BG tables 36 and 38/39
- **Problem:** A reader sees two final meta-Nash exploitabilities for the same run.
  - 2.96 is computed each epoch on the population *before* that epoch's training (`league.py` l. 170–176).
  - 3.418 is the EGTA of the final 56-agent population after training (`egta.analyze_population`).
- **Now → Proposed:** after BG caption ": Показатели от обучението на лигата при двата мащаба." add the line "(Стойността $2.96$ е за мета-Наш сместа на популацията в началото на епоха 119, преди последната стъпка на обучение; стойността $3.418$ в §10.7 е за крайната популация от 56 агента.)"; EN: "(The $2.96$ is the meta-Nash of the population at the start of epoch 119, before its last training step; the $3.418$ in §7 is the final 56-agent population.)"

### F10-C07 · S3 · "Exploitability" figures are NashConv (sum over both seats)
- **Where:** summary §§ 10.5–10.8 and report throughout
- **Problem:** Every value is `nash_gap(...)["nash_conv"] = br0 + br1` (`implementation/step07/implementation/best_response.py` l. 157–166). In OpenSpiel's convention exploitability is NashConv/n (`lit_evaluation.md`, Lanctot 2019). The first PSRO value, 4.747, is uniform-random Leduc NashConv. The chapter says "the same NashConv", but labels every value "exploitability".
- **Fix:** At the first use (§ 10.5, after "същият NashConv, използван още от Глава 2") add: "(NashConv е сумата от печалбите на двата най-добри отговора; в конвенцията на OpenSpiel експлоатируемостта е половината от нея)". EN likewise. Chapter I must quote these numbers as NashConv.

### F10-C08 · S2 · Stale "стъпка" and "raw step"
- **Where:** summaryBg §§ 10.3, 10.7; summaryEn l. 128, l. 234; fig. 55 (G02), fig. 62 (G09); one-pager report refs (B10)
- **Now → Proposed:**
  - "мотивация за останалата част от стъпката" → "мотивация за останалата част от главата" (the EN already says "chapter")
  - "Очакването (от контролния списък на суровата стъпка) беше, че **мета-Наш** равновесието в **лигата** ще бъде *по-малко* експлоатируемо от всеки отделен член." → "Очакването (от първоначалния план) беше, че **мета-Наш** сместа на **лигата** ще бъде *по-малко* експлоатируема от всеки отделен член."
  - EN "the raw step suggested" → "the original plan suggested"; "(from the raw step's checklist)" → "(from the original plan)"; one-pager EN "§4/§7 of the report" → "§3 and §8.2 of the report" (spinning top is report §3, the reconciliation is §8.2)
- **Why:** The bundle says "Глава". "суровата стъпка" (raw, as in uncooked) is internal jargon.

### F10-C09 · S3 · Why SVD rank-1 fails: the stated reason is imprecise
- **Where:** summaryEn l. 128–130; report_en l. 63
- **Problem:** The singular values of a real antisymmetric matrix come in equal pairs, so a rank-1 truncation captures at most half of the squared norm for *any* game. The pure skill ladder also scores 0.707 (checked numerically on RPS and on a 4-strategy ladder). The method fails for every game, not only because it "cannot represent a pure cycle".
- **Fix:** EN "— a rank-1 skew-symmetric approximation simply cannot represent a pure cycle" → "— the singular values of an antisymmetric matrix come in equal pairs, so a rank-1 truncation captures at most half of its squared norm for *any* game (a pure skill ladder also scores $0.707$)". BG in F10-B18.

### F10-C10 · S3 · "Orbits forever": the Euler simulation drifts outward
- **Where:** summaryEn l. 111–112, 34–35 of the one-pager; BG § 10.3
- **Problem:** The continuous RPS replicator flow has closed orbits (Zeeman; Hofbauer & Sigmund 2003, Thm 2). The simulation, explicit Euler (`replicator.py` l. 46–62), spirals slowly outward. The distance to the centre goes from 0.084 at the start to 0.098 at the end (report table), and in the exploration run from 0.108 to 0.119. This is visible as growing peaks in fig. 56.
- **Fix:** Add to the § 10.3 sentence: BG "(в непрекъснато време орбитите са затворени; явният метод на Ойлер ги превръща в бавно разширяваща се спирала)"; EN "(closed in continuous time; explicit Euler turns them into a slowly widening spiral)".

## S — Sources

### F10-S01 · S2 · SOURCE_GAPS row 1: "AlphaStar League … гаранция *липсва*" → cite Vinyals et al. (2019), and reframe
- **Where:** summaryBg.md chapter intro — "**AlphaStar League** е механизъм за безопасна експлоатация на популационно ниво, но чиято гаранция *липсва* - точното място, където се съдържа Принос №2."
- **Proposal (cite and soften):** → "**Лигата на AlphaStar** използва експлоататори, за да направи основните агенти устойчиви - механизъм, близък до безопасната експлоатация на ниво популация, но без формална гаранция: авторите обосновават подхода с фиктивната игра срещу себе си, чиято смес се сближава към равновесие на Наш при игри за двама с нулева сума, а устойчивостта на лигата показват само емпирично[^vinyals2019]. Точно тук се намира Принос №2." EN: "The **AlphaStar league** uses exploiters to make its main agents robust — close to a population-level safe-exploitation mechanism, but without a formal guarantee: its authors motivate it by fictitious self-play, whose mixture converges to a Nash equilibrium in two-player zero-sum games, and support the league's robustness only empirically.[^vinyals2019] That is exactly where Contribution #2 lives."
- **Verified** in DeepMind's preprint of the Nature paper (storage.googleapis.com/…/AlphaStar_unformatted.pdf):
  - "Fictitious self-play (FSP) avoids cycles by computing a best response against a uniform mixture of all previous policies; the mixture converges to a Nash equilibrium in two-player zero-sum games. We extend this approach to compute a best response against a non-uniform mixture…"
  - Main exploiters' "purpose is to identify potential exploits in the main agents; the main agents are thereby encouraged to address their weaknesses".
  - Evidence of no cycling is empirical: the league Nash "assigns small probabilities to players from previous iterations, suggesting that the learning algorithm does not cycle or regress".
  - The paper calls the league a robustness mechanism; "safe exploitation" is the candidate's framing, so it is presented as an analogy.

### F10-S02 · S2 · SOURCE_GAPS row 2: "репликаторната динамика възпроизвежда всяко … ESS/Наш, включително … орбита на RPS" → cite Hofbauer & Sigmund, and correct
- **Where:** summaryBg.md § 10.8, "**Какво се потвърди.**" (whole paragraph)
- **Proposal (cite and correct):** "**Какво се потвърди.** Потвърденият гръбнак: репликаторната динамика възпроизвежда всяко аналитично равновесие на Еволюционно стабилни стратегии/Наш, включително неконвергиращата орбита на RPS; декомпозицията тип пумпал на Ходж чисто отделя умението от цикли и правилно обозначава чистите случаи; лигата води до силно *ранно* подобрение и създава най-добър индивид ($1.305$), който превъзхожда PSRO ($2.163$) и самообучение ($3.683$); а EGTA дава работеща експлоатируемост на ниво популация. Заедно те проследяват дъгата от „в кои игри една популация дори може да се установи?“ до „какво се случва, когато една популация сама се обучава?“." → "**Какво се потвърди.** Основните резултати се потвърдиха: репликаторната динамика възпроизвежда всеки аналитичен резултат за матричните игри (ESS или равновесие на Наш), включително затворената орбита при „камък-ножица-хартия“, която не се сближава[^hofbauer2003]; разлагането на Ходж ясно отделя умението от цикличността и правилно определя чистите случаи; лигата постига бързо *ранно* подобрение и дава отделен агент с експлоатируемост $1.305$ - по-добър от PSRO ($2.163$) и сравним с най-добрата итерация на самообучението ($1.396$); а EGTA дава работеща мярка за експлоатируемост на ниво популация. Заедно те проследяват пътя от „в кои игри една популация изобщо може да се установи?“ до „какво се случва, когато една популация сама се обучава?“."
- **New footnote:** "[^hofbauer2003]: Hofbauer, J. & Sigmund, K. (2003). "Evolutionary game dynamics." *Bulletin of the American Mathematical Society* 40(4), 479–519 - т.нар. „фолклорна теорема“ за репликаторната динамика (§2.3), асимптотичната устойчивост на ESS (§2.6) и затворените орбити при „камък-ножица-хартия“ (теорема 2)."
- **Verified** in the full text (Sigmund's homepage PDF):
  - §2.3: "(a) if z is a Nash equilibrium, then it is a rest point; … (d) if the rest point z is stable, then it is a Nash equilibrium. … None of the converse statements holds."
  - §2.6: "an ESS is an asymptotically stable rest point … The converse does not hold in general."
  - Thm 2 (Zeeman): "If det A = 0, then all orbits in int Sn are closed orbits around z."
  - The 1998 book footnote stays; its publisher listing was checked, not its text.

### F10-S03 · S2 · SOURCE_GAPS row 3: takeaway on AlphaStar's mechanism → cite and soften (applied in F10-B05)
- **Where:** summaryBg.md last takeaway — "експлоатационният механизъм на AlphaStar е аналогът на популацията на безопасната експлоатация от Глава 8, но той е евристичен - нито гарантира монотонно подобрение, нито неексплоатируема смес."
- **Proposal (soften and cite):** see F10-B05. The "monotone improvement / exploitable mixture" failures are this chapter's small-league measurements. Vinyals et al. report the opposite at their scale ("does not cycle or regress"), so the claim is attributed to the chapter and the heuristic nature to [^vinyals2019]. Verified as in F10-S01. EN takeaway: "…but it is heuristic — its robustness is shown only empirically,[^vinyals2019] and in this chapter's small league it guaranteed neither monotone improvement nor a non-exploitable mixture."

### F10-S04 · S2 · Spinning top attributed to Balduzzi 2019 (`lit_gaps.md` correction)
- **Where:**
  - summaryBg § 10.4, "**Декомпозицията на пумпала** (Balduzzi и др.)".
  - § 10.4 reconciliation (F10-B19).
  - The history line (F10-S06).
  - Footnote `balduzzi2019` ("геометрията на пумпала"). The same appears in the EN, the report and `terminology_EN_BG.md` (T07).
- **Problem:** The transitive/cyclic (Hodge) decomposition of an antisymmetric payoff matrix is from Balduzzi et al. (2018), and Balduzzi et al. (2019) give Theorem 1 for functional-form games. The "spinning top" geometry, including "widest at intermediate strength" and "why populations are necessary", is Czarnecki et al. (2020).
- **Proposal (correct):**
  - "**Декомпозицията на пумпала** (Balduzzi и др.) разделя матрицата на печалбата на една игра на **транзитивен** компонент (скала на уменията, изразена чрез оценки за всяка стратегия) и **цикличен** компонент (това, което остава - частта камък-ножица-хартия). Името произлиза от формата: реалните игри са най-широки (най-циклични) сред посредствените стратегии и се стесняват до точка (чисто транзитивни) в крайностите на уменията." → "**Декомпозицията „пумпал“** разделя матрицата на печалбите на една игра на **транзитивна** компонента (стълбица на уменията, изразена чрез рейтинг на всяка стратегия) и **циклична** компонента (остатъкът - частта „камък-ножица-хартия“)[^balduzzi2018]. Името идва от формата, която Czarnecki и др. откриват при реални игри: те са най-широки (най-циклични) при стратегиите със средна сила и се стесняват към крайностите на уменията[^czarnecki2020]."
  - New footnotes:
    - "[^balduzzi2018]: Balduzzi, D., Tuyls, K., Pérolat, J. & Graepel, T. (2018). "Re-evaluating Evaluation." *NeurIPS*; arXiv:1806.02643 - разлагане на Ходж на антисиметричната матрица на печалбите на транзитивна и циклична компонента; усредняване по Наш."
    - "[^czarnecki2020]: Czarnecki, W. M., Gidel, G., Tracey, B., Tuyls, K., Omidshafiei, S., Balduzzi, D. & Jaderberg, M. (2020). "Real World Games Look Like Spinning Tops." *NeurIPS*; arXiv:2004.09468 - геометрията „пумпал“ и защо обучението изисква популации."
  - `balduzzi2019` → "…*ICML* - разлагане на функционалните игри на транзитивна и циклична част; PSRO$_{rN}$." (drop "геометрията на пумпала").
  - EN likewise: "(Balduzzi et al.)" → "[^balduzzi2018] … [^czarnecki2020]"; "Balduzzi's spinning-top in action" → "Czarnecki et al.'s spinning top in action".
- **Verified:**
  - Balduzzi 2018, arXiv PDF: "any antisymmetric matrix decomposes as A = transitive component + cyclic component = grad(r)+rot(A) … The Hodge decomposition separates transitive … from cyclic interactions".
  - Czarnecki 2020, arXiv abstract: "the upright axis representing transitive strength, and the radial axis … the non-transitive dimension … it clarifies why populations of strategies are necessary for training of agents".
  - Balduzzi 2019, arXiv abstract (ICML 2019).

### F10-S05 · S2 · "~600 agents" for AlphaStar → "almost 900 distinct players"
- **Where:** summaryEn l. 220–221; report_en §10 item 3; BG in F10-B21
- **Proposal (correct):** EN "the AlphaStar diversity benefits reported at ~600 agents" → "the diversity benefits reported for AlphaStar, whose league created almost 900 distinct players". Verified in the Nature preprint: "During league training almost 900 distinct players were created." No "600" appears in the paper.

### F10-S06 · S2 · History line: dates, what AlphaStar achieved, where EGTA comes from
- **Where:** summaryBg.md § 10.2, last paragraph
- **Now → Proposed:** "Исторически линията е следната: обучение, базирано на популации като онлайн търсене на хиперпараметри (PBT, 2017) → теория на игрите върху популация от стратегии (PSRO, 2017) → геометрията, която обяснява *защо* е необходима популация („пумпал“, 2019) → и пълната тритипна лига, която победи професионални човешки играчи (AlphaStar, 2019), оценена с емпирична теория на игрите (EGTA, Tuyls и др., 2020)." → "Исторически линията е следната: обучение на базата на популации като онлайн търсене на хиперпараметри (PBT, 2017)[^jaderberg2017] → теория на игрите върху популация от стратегии (PSRO, 2017)[^lanctot2017] → лигата с три типа агенти, достигнала ниво „гросмайстор“ в StarCraft II - над 99.8% от класираните човешки играчи (AlphaStar, 2019)[^vinyals2019] → геометрията, която обяснява *защо* е необходима популация (транзитивно-циклична декомпозиция, 2018-2019; „пумпал“, 2020)[^czarnecki2020]. Такива популации се оценяват с емпиричен теоретико-игрови анализ (EGTA)[^wellman2006][^tuyls2020]."
- **Why:**
  - The spinning top is 2020 (F10-S04).
  - EGTA is older than, and independent of, AlphaStar: Wellman (2006) systematised it, and Tuyls et al. (2020) give bounds. "оценена с" wrongly implies AlphaStar was evaluated by Tuyls 2020.
  - The cited Nature paper reports a Grandmaster rating "above 99.8% of officially ranked human players" (verified); the matches against professionals are not in it.
  - "тритипна" is a nonce word.
- **New footnotes:**
  - "[^wellman2006]: Wellman, M. P. (2006). "Methods for Empirical Game-Theoretic Analysis." *AAAI*, 1552–1555."
  - "[^tuyls2020]: Tuyls, K., Pérolat, J., Lanctot, M., Hughes, E., Everett, R., Leibo, J. Z., Szepesvári, C. & Graepel, T. (2020). "Bounds and dynamics for empirical game theoretic analysis." *Autonomous Agents and Multi-Agent Systems* 34(1), 7. DOI 10.1007/s10458-019-09432-y."
  - `jaderberg2017`: see F10-S08.
- **Verified:** Wellman from the AAAI PDF (page folios 1552–1555); Tuyls from Crossref.

### F10-S07 · S3 · Footnote metadata
- **Where:** footnotes `vinyals2019`, `lanctot2017`, `hofbauer1998`
- **Proposal (correct):**
  - `vinyals2019`: add "575(7782), 350–354. DOI 10.1038/s41586-019-1724-z" (Crossref).
  - `lanctot2017`: "Tuyls, K. et al. (2020). "Bounds and dynamics…" *AAMAS/JAAMAS* (EGTA)" → drop it here (own footnote, F10-S06). Add pages to McMahan: "*ICML*, 536–543". Verified via the ICML 2003 PDF (Theorem 1: "The Double Oracle algorithm converges to a minimax equilibrium") and a proceedings listing for the pages. "AAMAS/JAAMAS" conflated the AAMAS 2018 conference version (arXiv:1803.06376) with the journal.
  - `hofbauer1998`: "обзорът на Bloembergen–Tuyls (JAIR, 2015)" → "обзорът на Bloembergen, Tuyls, Hennes & Kaisers (JAIR 53, 659–697, 2015)" (Crossref, DOI 10.1613/jair.4818).
  - "Свързани:" (2×) → "Вж. също:".

### F10-S08 · S2 · The dojo/league sentence cites Balduzzi 2019; PBT has no footnote of its own
- **Where:** summaryBg.md § 10.1 — "Лигата е това доджо, превърнато в математическа форма.[^balduzzi2019]"
- **Problem:** The dojo is the AlphaStar league: main agents, exploiters, frozen snapshots, PFSP, i.e. Vinyals et al. 2019. Copying and mutating the strong agents is PBT (Jaderberg et al. 2017), which is hidden under "Свързани:" in the Balduzzi note.
- **Proposal (correct):** "Лигата е това доджо, превърнато в математическа форма.[^balduzzi2019]" → "Лигата е това доджо, превърнато в математическа форма.[^vinyals2019]" plus the new footnote "[^jaderberg2017]: Jaderberg, M., Dalibard, V., Osindero, S., Czarnecki, W. M. et al. (2017). "Population Based Training of Neural Networks." *arXiv:1711.09846*." (used in F10-S06), and remove "Свързани: Jaderberg…" from `balduzzi2019`. Verified: arXiv abstract page (authors, 27 Nov 2017).

## X — Structure

### F10-X01 · S3 · Cross-references "§3/§4/§5" vs printed "10.N"
- **Where:** summaryBg.md § 10.2, the paragraph after table 33 (the table cells are in F10-B28)
- **Now → Proposed:** "**Репликаторната динамика** (§3)" → "**Репликаторната динамика** (§10.3)"; "**Декомпозицията „пумпал“** (§4)" → "**Декомпозицията „пумпал“** (§10.4)"; "дали лигата в §5 ще се установи" → "дали лигата от §10.5 ще се установи"; EN likewise.
- **Why:** The bundle numbers sections 10.1–10.9. A bare "§5" in a 226-page bundle reads as another chapter (as F07-X03).

### F10-X02 · S3 · BG subtitle differs from the official title (corpus-wide)
- **Where:** summaryBg.md / onePagerBg.md YAML (and all 24 BG summary/one-pager files)
- **Now → Proposed:** "subtitle: "Изследване върху възможностите за прилагане на изкуствен интелект в компютърните игри"" → "subtitle: "Изследване на възможностите за приложение на изкуствения интелект в компютърни игри""
- **Why:** The files' own header comment gives the official BG title, and the subtitle paraphrases it. It prints on the standalone summary PDFs. Fix it once centrally.
