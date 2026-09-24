# Step 04 — final review

**Summary:** The chapter's literature summary is broadly right, but four things matter most. (1) **Bulgarian.** Several settled glossary terms produce meaning errors: "загубен" (lost) for *lossy* (8×), "режим на извикване" for *recall*, "експлоатируема разлика" for *exploitability gap* (8×), and in the one-pager "таван" (ceiling) for *floor* and "ранно начално число" (an early random seed) for *early seed*. The text also still contains English ("nP-complete", "live CFR solve", "live re-solving", "Wasserstein GANs", "(state-of-the-art)", "suit+action", "Extended Leduc"), first-person "преизчислявам", and "наш равновесието". Four of the candidate's August comments were not applied, or only in part. (2) **Figures.** All five figures fail. The three CFR+ result panels are the English PNGs, print at 4.4–5.8 pt and leave pages 56–58 half empty. The Pareto figure uses "ден2/ден3" diary labels and plots a 200-iteration smoke-test run, not the 180-s benchmark the text reports. Figure 12 (k-means) is illegible (3–4.5 pt) and does not show the HSD + EMD pipeline its section describes. (3) **Content.** The headline "action abstraction is ruinous / translation error dominates" rests on an evaluation harness in which all three translators return bit-identical results and every abstract small bet is played as the large bet (`day03_train.py`, `day07_cfrplus_panels.py`). Five literature claims are misstated: the 10¹⁷ card count, "10–100× … every prior translator", "every HUNL AI since 2017 incl. Pluribus", the CFR-BR explanation, and imperfect recall as a law that the chapter's own data do not reproduce. (4) **Sources.** All three SOURCE_GAPS items now have verified sources or a proposed softening. Five new references are proposed and all were verified.
**Counts:** S1 15 · S2 40 · S3 6   (by category: G 5 · B 27 · T 9 · C 11 · S 6 · X 3)

Conventions in this file (as in the step-07 pilot):
- Quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md` / `summaryEn.md`. "l. N" is the line in that file.
- Pages are PDF pages of `allSummaries_bg.pdf`, as in `renders/manifest.json`. The printed folio is one lower.
- Proposals keep the chapter's decimal points and its em dashes. Both are fixed centrally.
- Printed type size = matplotlib size × (printed width ÷ saved width). Body text is 10.9 pt; the floor is ≈ 8.2 pt.
- **Central, not itemised:**
  - The chapter uses " — " (76×), " – " (4×) and " - " (3×) as dashes in `summaryBg.md`, and " - " (8×) in `onePagerBg.md`.
  - `summaryBg.md` has 5 decimal points; `onePagerBg.md` has 9, plus 6 thousands commas ("14,185", "10,304", "4,704").
  - `summaryBg.md` has 110 bold spans against 78 in the EN. The pipeline added about 32, including bold on the pronouns "**ѝ**" and "**него**" (l. 123).
  - Footnote labels are shared across chapters (F07-X01; confirmed in X01).

## G — Figures

### F04-G01 · S1 · Bulgarian captions for all five figures
- **Where:** summaryBg.md, image alt text of figs. 12–16 (pp. 52, 56, 57, 58, 59). All five print in English (known corpus-wide defect).
- **Now → Proposed:**
  - "![Infoset grouping via K-means]" → "![Групиране на 936-те информационни множества в Ледюк с k-средни (k = 12) по седем стандартизирани признака; по осите са силата на ръката и размерът на пота. Клъстерите следват предимно размера на пота, т.е. историята на залозите, а не картите.]"
  - "![Fixed-limit Leduc CFR+ abstraction results]" → "![Ледюк с лимит: крайна експлоатируемост след 180 s CFR+ за всяка конфигурация на абстракцията (три изпълнения, логаритмична скала).]"
  - "![Mini-NL Leduc CFR+ abstraction results]" → "![Mini-NL Ледюк: крайна експлоатируемост след 180 s CFR+ – пълната игра срещу абстракцията на действията.]"
  - "![Extended Leduc CFR+ abstraction results]" → "![Разширен Ледюк: крайна експлоатируемост след 180 s CFR+ за пълната игра, изоморфизма на боите и комбинираните абстракции.]"
  - "![Abstraction Pareto frontier]" → "![Граница на Парето: брой информационни множества срещу експлоатируемост в пълната игра за всяка конфигурация на абстракцията.]"
- **Fix:** replace the alt text in `summaryBg.md`; the `](file.png)` part stays, except as noted in G03. Adjust the fig. 12 and fig. 16 captions if G02 or G04 changes the figure.

### F04-G02 · S1 · Fig. 12 (k-means): English title and legend, 3–4.5 pt, and it does not show what its section describes
- **Where:** `renders/ch04/p052_f1.png`, caption "Infoset grouping via K-means". It is printed under "### Конвейер 2 — HSD + разстояние на Васерщайн + k-средни + непълна памет (загубен)". Script: `implementation/step04/exploration/day01_infoset_clustering.py` (`_plot_scatter`, `main`).
- **Problem:**
  1. **English in the BG figure.** The title is an f-string and not in the mapping: "Leduc info sets — k-means (k=12) on standardised 7-feature space, n=936 / Same axes as the manual plot — only the colour mapping differs". It also refers to a "manual plot" that is not in the bundle. The legend reads "cluster_00 (n=96)" … "cluster_11 (n=72)".
  2. **One word, two translations.** The x-label renders *jittered* as "— разбъркана" (shuffled), the y-label as "— с разсейване".
  3. **Illegible.** The figure is saved from figsize (12, 8) at dpi 150 (1789 px) and printed at `width=65%` = 11.4 cm, a scale of 0.376. Legend fs 8 → 3.0 pt; axis labels and ticks 10 → 3.8 pt; title 12 → 4.5 pt.
  4. **It shows the wrong mechanism.** The section describes clustering hand-strength distributions with EMD. The figure clusters seven standardised features (`hand_strength, own_bet, opp_bet, pot, num_raises, facing_raise, round`), and the clusters are horizontal bands of pot size, i.e. betting history. Card abstraction merges only on cards, not on betting. Johanson et al. (2013): the abstractions "only merge information sets on the basis of having similar chance events". A reader takes the figure as the HSD + EMD bucketing, which it is not.
- **Fix:**
  - **Preferred:** drop the figure from § 4.9.2 (EN and BG), or replace it with a plot of the Leduc HSD histograms that `phase4/day02_hand_strength.py` computes.
  - **Minimal fix, if it stays:**
    - `_plot_scatter`: figsize (12, 8) → (8, 5.4); delete `ax.set_title(...)` (the caption carries it); `ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.13), ncol=4, fontsize=10, frameon=False)`; `ax.set_xlabel(..., fontsize=11)` and `ax.set_ylabel(..., fontsize=11)`; `ax.tick_params(labelsize=10)`; dpi 150 → 300.
    - `main`: `f"cluster_{c:02d}"` → `f"C{c+1}"` (language-neutral).
    - `summaryBg.md` / `summaryEn.md`: `{width=65% fig-pos="H"}` → `{width=100% fig-pos="H"}`. At 8 in saved and 17.6 cm printed, fs 10 prints at 8.7 pt.
    - Mapping: 'Hand strength (P(win) + 0.5·P(tie))  — jittered' → 'Сила на ръката (P(win) + 0.5·P(tie)) — с разсейване'. Re-render with `render_bg_figures.py --only step04`.

### F04-G03 · S1 · Figs. 13–15 (CFR+ panels): entirely English, 4.4–5.8 pt, each forces a half-empty page
- **Where:** `renders/ch04/p056_f1.png`, `p057_f1.png`, `p058_f1.png`. `summaryBg.md` links `day07_cfrplus_fixed_leduc.png`, `day07_cfrplus_mini_nl_leduc.png` and `day07_cfrplus_extended_leduc.png`, the English files; no `_bg` variant exists in `phase4/figures/` or `summary/`. Script: `implementation/step04/phase4/day07_cfrplus_panels.py`, `_plot_single_panel`.
- **Problem:**
  1. **All English.** Titles "Fixed-limit Leduc - CFR+ after 180s" etc.; y-label "Final exploitability (log scale)"; legend title "Mean +/- SD exploitability"; every tick and legend label ("Full CFR+ (936 infos)", "Suit iso", "k2 perfect", "full bucket p", "Action abs", "Suit + action + buckets"); decimal points and thousands commas ("4,704", "10,304").
  2. **Illegible.**
     - Fixed panel: figsize (16, 7) at dpi 150 → 2383 px (15.9 in), printed at 17.6 cm, scale 0.436. Legend, ticks and y-label 10 → 4.4 pt; title 12 → 5.2 pt.
     - Mini-NL and Extended panels: (12, 7) → 1783 px, scale 0.58 → 5.8 pt.
  3. **Clutter.** The legend repeats the tick labels. "infos" is slang.
  4. **Layout.** Each figure is about 14 cm tall, so pp. 56, 57 and 58 are each half empty (X02).
- **Fix** (`_plot_single_panel`):
  - `figsize=(width, 7)` → `figsize=(8, 5.0 if len(labels) > 4 else 4.2)`.
  - Delete `ax.set_title(...)` and the `ax.legend(...)` call; the text and report table give the means.
  - `ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=10)`, labels without the "(N infos)" suffix, so that they are mappable.
  - Annotate the information-set count as a bare number above each group: `ax.annotate(f"{info}", (x, max(values)), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=10)`.
  - `ax.set_ylabel(..., fontsize=11)`; `ax.tick_params(axis="y", labelsize=10)`; dpi 150 → 300.
  - New mapping keys:

    | EN | BG |
    |---|---|
    | 'Full CFR+', 'Full mini-NL', 'Full extended' | 'Пълна игра' |
    | 'Suit iso' | 'Изоморфизъм на боите' |
    | 'k2 perfect' / 'k2 imperfect' | 'k2, пълна памет' / 'k2, непълна памет' (same pattern for k3, k5) |
    | 'full bucket p' / 'full bucket i' | 'по ранг, пълна памет' / 'по ранг, непълна памет' |
    | 'Action abs' | 'Абстракция на действията' |
    | 'Suit + action' | 'Бои + действия' |
    | 'Suit + action + buckets' | 'Бои + действия + клъстери' |

    Existing key 'Final exploitability (log scale)' → 'Крайна експлоатируемост (логаритмична скала)'.
  - Then run `python scripts/figures/render_bg_figures.py --only step04`. The script reloads `.day07_cfrplus_results.json` and skips the completed runs. Copy the three `_bg` PNGs next to `summaryBg.md` and relink: "(day07_cfrplus_fixed_leduc.png)" → "(day07_cfrplus_fixed_leduc_bg.png)", and the same for the mini_nl and extended files.
  - Add to the captions (G01): "числото над всяка група е броят информационни множества".

### F04-G04 · S1 · Fig. 16 (Pareto): diary labels, 4.4 pt, and it plots a smoke-test run, not the benchmark in the text
- **Where:** `renders/ch04/p059_f1.png`, caption "Abstraction Pareto frontier". Script: `implementation/step04/phase4/day05_plots.py`, data `phase4/.day05_pareto.json` / `.day05_pareto_table.csv`.
- **Problem:**
  1. **Meaningless labels.** Point labels are development-diary names: "ден2 k2 непълна", "ден2 k3/k5 пълна", "ден3 транслатори", "ден1 пълна Ледюк", "ден3 мини nl пълна", "беззагубен/пълни клъстери". The title is "Фаза 4 — …". Nothing in the text says what "ден2" is.
  2. **Illegible.** figsize (11, 7) at dpi 150 = 1650 px, printed at 17.6 cm, scale 0.63. Point labels fs 7 → 4.4 pt; axis labels 10 → 6.3 pt; title 12 → 7.6 pt. The large markers cover "ден2 k2 пълна" / "ден2 k3/k5 непълна".
  3. **Wrong data.**
     - The points are the smoke-test runs: vanilla CFR, 200 iterations for day 1–2 and 100 for day 3; the README calls this budget a smoke test. They are not the 180-s CFR+ benchmark that the text and figs. 13–15 report.
     - The unabstracted reference is itself 0.19 exploitable, so the plotted "Δ_abs" is exploitability minus that of an unconverged full-game run, not the § 4.4 definition (minus exact Nash, i.e. 0).
     - The values contradict the text: k2 perfect 0.958 (text and fig. 13: 0.571); k3/k5 perfect 0.459 (0.382); k3/k5 imperfect 0.697 (0.574).
     - Three zero gaps are drawn at the clip value 10⁻⁶ without saying so. The Extended Leduc rows have no exploitability and are missing.
  4. **Not a frontier.** It is a scatter, with no non-dominated line.
- **Fix:**
  - Rewrite `day05_plots.py` to read `.day07_cfrplus_results.json`: mean exploitability of the three runs per config against `info_sets`, one colour per game (Ледюк с лимит / Mini-NL Ледюк / разширен Ледюк), non-dominated points joined by a step line.
  - Drop the marker-size encoding and the title; annotate with the G03 config labels at fontsize 10; axis labels fs 11; figsize (8, 5); dpi 300.
  - Mapping: 'info-set count' → 'брой информационни множества'; 'exploitability gap Δ_abs (full game)' → 'експлоатируемост в пълната игра'.
  - If the old figure stays, the caption must say "пробен прогон: 200 итерации CFR; нулевите стойности са нанесени при 10⁻⁶", and the "denN" labels must be replaced.

### F04-G05 · S3 · Mapping entries of this step's plotting scripts
- **Where:** `scripts/figures/out/figure_labels.json`, step-04 entries.
- **Now → Proposed:**
  - 'CFR+ abstraction comparison: 3 seeds x 3 minutes each' → 'Сравнение на абстракциите в CFR+: 3 начални числа × 3 минути' ("семена", F07-B19).
  - 'Mean +/- SD exploitability' → 'Средна експлоатируемост ± стандартно отклонение'.
  - 'Final exploitability after 180s (log scale)' → 'Крайна експлоатируемост след 180 s (логаритмична скала)'.
  - 'Exploitability (full game)' / '(own game)' → 'експлоатируемост (пълна игра)' / 'експлоатируемост (собствена игра)'. These still contain English and belong to exploration plots that are not in the bundle.

## B — Bulgarian language

### F04-B01 · S1 · meaning — "загубен" (*lost*) for *lossy* (T01)
- **Where:** summaryBg.md §§ 4.7, 4.8, 4.9.1, 4.9.2, 4.11, 4.12; onePagerBg.md "**Подход.**" and "**Ключови резултати (измерени).**"
- **EN:** "lossy" / "Bounded lossy" / "lossy card bucketing" / "Lossy card buckets install a floor"
- **Now → Proposed:**
  - "аналитичната граница оценява загубено сливане от Ниво 2 с ограничени отклонения" → "аналитичната граница оценява сливане със загуби от Ниво 2 (с ограничено отклонение)"
  - "след това се приемат ограничени загубни обединявания само когато бюджетът на грешки е приемлив" → "след това се приемат сливания с ограничени загуби само когато бюджетът на грешките е приемлив"
  - "преди прилагането на каквато и да е загубена стъпка" → "преди да се приложи каквато и да е стъпка със загуби"
  - "+ k-средни + непълна памет (загубен)" → "+ k-средни + непълна памет (със загуби)"
  - "прилагат се беззагубна и загубена абстракция за свиване на играта" → "прилагат се беззагубна абстракция и абстракция със загуби, за да се свие играта"
  - "- **Загубено групиране на карти**, използващо" → "- **Групиране на карти със загуби**, използващо"
  - "докато **загубената** информационна и **абстракцията на действията** въвеждат постоянни нива на експлоатируемост." → "докато информационната абстракция със загуби и абстракцията на действията въвеждат трайна долна граница на експлоатируемостта."
  - "Загубените експерименти с клъстери показват другата страна на компромиса." → "Експериментите с клъстери със загуби показват другата страна на компромиса."
  - onePagerBg: "**загубено групиране на карти**" → "**групиране на карти със загуби**" (for the "Загубените клъстери" bullet see B26)
- **Why:** "загубен" means *lost*, so "загубено групиране" reads "a lost bucketing". The curated glossary says "Абстракция със загуби … not „загубна"". The settled glossary is the source (T01). The EN "floor" also became "нива" (levels); see B26 for the same slip.

### F04-B02 · S1 · meaning/terminology — "експлоатируема разлика" for *exploitability gap* (T03)
- **Where:** summaryBg.md §§ 4.1, 4.4, 4.7.1, 4.12, 4.14 (8 places); fig. 16 y-label (G04)
- **EN:** "the **exploitability gap** — how much worse the abstract strategy is than the real game's exact Nash"
- **Now → Proposed:**
  - "а по другата — **експлоатируема разлика** — с колко е по-лоша абстрактната стратегия спрямо точното **Нашево равновесие** в реалната игра" → "а по другата – **разликата в експлоатируемостта**, т.е. с колко абстрактната стратегия е по-лоша от точното равновесие на Наш в реалната игра"
  - "## Експлоатируемата разлика" → "## Разлика в експлоатируемостта"
  - "Глава 4 въвежда производна метрика – **експлоатируема разлика**: с колко една абстрактна стратегия се различава от точното Нашево равновесие на реалната игра" → "Глава 4 въвежда производна метрика – **разлика в експлоатируемостта**: с колко една абстрактна стратегия е по-лоша от точното равновесие на Наш на реалната игра"
  - "> **Запомнете:** експлоатируемата разлика е цената" → "> **Запомнете:** разликата в експлоатируемостта е цената"
  - "и така се получава горна граница на експлоатируемата разлика." → in B19.
  - "Това е практическото значение на експлоатируемата разлика" → "Това е практическото значение на разликата в експлоатируемостта"
  - "план, транслация на действия, експлоатируема разлика, Парето граница" → "план, транслация на действия, разлика в експлоатируемостта, Парето граница"
  - Table 7, "Ограничена експлоатируема разлика в **същата** игра" → see C04.
- **Why:** "експлоатируема разлика" means *a difference that can be exploited*. Δ_abs is a difference *between* two exploitabilities. The chapter already writes "разлики в експлоатируемостта" (§ 4.12, list). "различава" in the § 4.4 sentence also loses *worse*.

### F04-B03 · S1 · meaning — *recall* rendered as "извикване" (T02)
- **Where:** summaryBg.md § 4.9.2; onePagerBg.md "**Подход.**"
- **EN:** "Two recall regimes:" / "in perfect- and imperfect-recall regimes"
- **Now → Proposed:**
  - "Съществуват два режима на извикване:" → "Възможни са два режима на паметта:"
  - "в режими на перфектно и неперфектно извикване" → "с пълна и с непълна памет"
- **Why:** "извикване" means *calling up* (a function or a person). *Perfect/imperfect recall* is "пълна/непълна памет" in the curated glossary and elsewhere in this chapter.

### F04-B04 · S1 · grammar — first person "преизчислявам" (candidate's comment p. 53 applied only in part)
- **Where:** summaryBg.md § 4.3.2 (last paragraph) and § 4.10 (first paragraph)
- **Candidate's comment:** "трябва генерално да видим в документа къде има 1ви и 2ри род и да го сменим с преизчислява се". Only the second half of the sentence was changed.
- **Now → Proposed:**
  - "преизчислявам реалната под-игра с реалния залог, вместо да се разчита на преводача." → "реалната под-игра се преизчислява с реалния залог, вместо да се разчита на транслатора."
  - "Когато играта премине в под-игра и абстрактният план е твърде груб, преизчислявам под-играта с по-висока точност *в реално време*." → "Когато играта премине в под-игра, която абстрактният план покрива твърде грубо, под-играта се преизчислява с по-висока точност *в реално време*."
- **Why:** "преизчислявам" is 1st person singular ("I re-solve"), the pattern of F07-T03.

### F04-B05 · S1 · meaning/terminology — Nash rendered four ways (candidate's comment p. 54 not applied)
- **Where:** summaryBg.md §§ 4.1, 4.2 (table), 4.4
- **Candidate's comment** on "наш р…": "наш в този контекст трябва да е с главна буква (генерален коментар)"
- **Now → Proposed:**
  - "преди абстрактната Нашева стратегия да престане да бъде добра стратегия в реалната игра?" → "преди равновесната стратегия на абстрактната игра да престане да бъде добра стратегия в реалната игра?"
  - "Нека $\hat\sigma^*$ е наш равновесието на $\hat G$" → "Нека $\hat\sigma^*$ е равновесие на Наш на $\hat G$"
  - "с $\sigma^*_G$ точното **Нашево равновесие** на $G$." → "където $\sigma^*_G$ е точното равновесие на Наш на $G$."
  - "**няма** теорема за запазване на Неш равновесие" → "**няма** теорема за запазване на равновесието на Наш"
  - § 4.1 "…точното **Нашево равновесие** в реалната игра" is in B02. § 4.7.3 "Нашево равновесие" is in C03.
- **Why:** "наш равновесието" reads "our the-equilibrium". "Неш" is a second transliteration. The glossary term is "равновесие на Наш" (F07-B02).

### F04-B06 · S1 · English left in the text
- **Where:** summaryBg.md §§ 4.2, 4.3.2, 4.5, 4.8, 4.10.1, 4.10.3, 4.11; onePagerBg.md
- **Now → Proposed:**
  - **Formula (l. 49):** "$$\mathcal{L} = \underbrace{\text{Complexity}(Z)}_{\text{memory cost}} - \beta \cdot \underbrace{\text{Value}(\pi_Z)}_{\text{strategic worth}}$$" → "$$\mathcal{L} = \underbrace{\text{Сложност}(Z)}_{\text{цена в памет}} - \beta \cdot \underbrace{\text{Стойност}(\pi_Z)}_{\text{стратегическа стойност}}$$". In l. 53–54 replace "\text{Value}" (4×) with "\text{Стойност}". Cyrillic inside `\text{}` is new to the corpus (F07-B08), so check the first rebuild.
  - "(типична покерна мрежа: `{fold, call, 0.5×pot, 1×pot, 2×pot, all-in}`)" → "(типичен набор от действия в покера: {пас, плащане, 0,5×пот, 1×пот, 2×пот, ол-ин})"
  - "е **nP-complete**, дори за малка еднопотребителска игра с дълбочина две нива" → "е **NP-пълна** задача дори за игра с един играч и дърво с височина две"
  - "В по-ново време то стои в основата на Wasserstein GANs" → "В по-ново време то стои в основата на генеративно-състезателните мрежи на Васерщайн (WGAN)"
  - "Играчът $P_1$ избира между *Sell* (с печалба, зависеща от резултата на монетата) и *Play*" → "Играчът $P_1$ избира между „Продай“ (Sell; с печалба, зависеща от резултата на монетата) и „Играй“ (Play)". The five later *Sell* / *Play* in § 4.10.1 become „Продай“ / „Играй“.
  - "остават подходящият избор само когато латентността не позволява live CFR solve (онлайн игра, вградени приложения)" → "остават подходящият избор само когато закъснението не позволява решаване с CFR в реално време (онлайн игра, вградени приложения)"
  - "производствената архитектура е една част предварително изчислен план и една част live re-solving" → "архитектурата на реалните системи е наполовина предварително изчислен план и наполовина повторно решаване в реално време"
  - onePagerBg: "Extended Ледюк е още по-драстичен: suit+action **4.696** и suit+action+buckets **4.734**" → "Разширеният Ледюк е още по-показателен: бои + действия **4.696** и бои + действия + клъстери **4.734**"
  - "(state-of-the-art)" in § 4.3.2 → S02.
- **Why:** English prose in the Bulgarian text, all printed (pp. 43, 45, 51, 52, 54, 55). "nP" is also a case error. "производствен" means *manufacturing*.

### F04-B07 · S2 · English and lower-case game names; fixed-limit
- **Where:** summaryBg.md §§ 4.1, 4.9.1, 4.12; footnote `gilpin2007`; onePagerBg.md
- **Now → Proposed:**
  - "върху игра с достатъчно малък размер, за да може дървото на играта ѝ да бъде изброено точно: кун (12 информационни множества) и ледюк (936)." → "върху игра с достатъчно малък размер, за да може дървото на играта ѝ да бъде изброено точно: Кун (12 информационни множества) и Ледюк (936)."
  - "- **Беззагубен изоморфизъм на боите** върху ледюк с фиксиран лимит и Extended Leduc." → "- **Беззагубен изоморфизъм на боите** върху Ледюк с лимит и разширения Ледюк (Extended Leduc)."
  - "- **Абстракция на действията** върху Mini-NL Leduc с кодове за транслация „най-близък“, „вероятностно разпределение“ и „псевдохармоничен“." → "- **Абстракция на действията** върху Mini-NL Ледюк с реализирани транслатори „най-близко действие“, „вероятностно разделяне“ и „псевдохармонично преобразуване“."
  - "- **Extended Leduc** с четири ранга и две бои" → "- **Разширен Ледюк** с четири ранга и две бои"
  - "намали броя на информационните множества в **ледюка с фиксиран лимит** от 936 до 288" → "намали броя на информационните множества в Ледюк с лимит от 936 до 288"
  - "В **Extended Leduc**, същата идея намали броя на" → "В разширения Ледюк същата идея намали броя на"
  - "В **ледюка с фиксиран лимит** грубите абстракции с клъстери останаха около експлоатируемост" → "В Ледюк с лимит грубите абстракции с клъстери останаха на експлоатируемост около"
  - "В Mini-NL ледюк ограничаването на множеството действия" → "В Mini-NL Ледюк ограничаването на множеството действия"
  - "В Extended Leduc добавянето на абстракция на действията" → "В разширения Ледюк добавянето на абстракция на действията"
  - "В Rhode Island Холдем сигналното дърво" → "В Род Айлънд холдем (Rhode Island Hold'em) сигналното дърво"; "решава Rhode Island Холдем през 2007 г." → "решава Род Айлънд холдем през 2007 г."; footnote "резултатът за Rhode Island холдем" → "резултатът за Род Айлънд холдем"
  - onePagerBg: "и 4-рангов Extended Ледюк" → "и разширен Ледюк с 4 ранга"; "Потвърдено в по-голям мащаб върху Extended Ледюк" → "Потвърдено в по-голям мащаб върху разширения Ледюк"
- **Why:**
  - Rule: Leduc → Ледюк, Kuhn → Кун, capitalised. The curated glossary adds "Ледюк с лимит".
  - "кодове" means ciphers or codes, not code.
  - The translator names should match § 4.3.2 and the curated "Вероятностно разделяне".

### F04-B08 · S1 · meaning — "края на дисертацията" for the end of the chapter
- **Where:** summaryBg.md § 4.2 — "те са обобщени в отделен раздел към края на дисертацията"
- **EN:** "since no implicit work is performed in this chapter they are collected in a single section near the end rather than interleaved."
- **Now → Proposed:** "те са обобщени в отделен раздел към края на дисертацията, вместо да бъдат разпределени помежду останалите." → "те са събрани в отделен раздел към края на главата („Аналози на дълбокото обучение с подкрепление“), вместо да бъдат разпределени между останалите."
- **Why:** The section is § 4.13 of this chapter. The BG promises a section of the dissertation that does not exist.

### F04-B09 · S2 · meaning — table 7 cells ("ръчно изведени признаци", "заложна комбинация"); candidate's comment "фактор за настройка" not applied
- **Where:** summaryBg.md § 4.2, table 7 (p. 44)
- **EN:** "A human-designed rule or a clustering pass on hand features" / "The 'knob' | $k$ in k-means buckets, the bet-set, the suit-isomorphism rule" / "A partition over info sets / a finite chosen set of actions | A continuous latent vector"
- **Candidate's comment** (p. 51, on „Врътката“): "фактор за настройка". The header became „Регулаторът“ instead.
- **Now → Proposed:**
  - "Човешки проектирано правило или клъстеризация върху ръчно изведени признаци" → "Правило, зададено от човек, или клъстеризация по признаци на ръката"
  - "| „Регулаторът“ | $k$ в k-средни клъстери, заложна комбинация, правилото за изоморфизъм на боя |" → "| Фактор за настройка | $k$ в k-средни, наборът от размери на залога, правилото за изоморфизъм на боите |"
  - "Разделяне върху информационни множества / крайно избран набор от действия | Непрекъснат скрит вектор" → "Разбиване на информационните множества / краен избран набор от действия | Непрекъснат латентен вектор"
- **Why:**
  - *Hand features* are features of the poker hand, not "manually derived" ones.
  - "заложна" belongs to "заложна къща" (pawnshop).
  - "скрит" collides with "скрити карти/състояния" in the same chapter.
  - *Partition* is "разбиване".

### F04-B10 · S2 · meaning — *joint torques*
- **Where:** summaryBg.md § 4.3.2 — "съвместни въртящи моменти при непрекъснато управление"
- **EN:** "joint torques in continuous control"
- **Now → Proposed:** "съвместни въртящи моменти при непрекъснато управление" → "въртящи моменти в ставите при непрекъснато управление"
- **Why:** In robotics *joint* is the articulation. "съвместни" means *shared* or *combined*.

### F04-B11 · S2 · meaning — "разрешаването" for re-solving; "легалното"
- **Where:** summaryBg.md § 4.3.2
- **EN:** "before translation or resolving" / "a subset of the legal one"
- **Now → Proposed:**
  - "абстракцията на действията определя кои ходове може да обмисля агентът преди превода или разрешаването." → "абстракцията на действията определя кои ходове агентът може да обмисля преди транслацията или повторното решаване."
  - "ако абстрактното множество действия е подмножество на легалното" → "ако абстрактното множество действия е подмножество на допустимите действия"
- **Why:** "разрешаване" means *permitting* (or *resolving a conflict*). *Re-solving* is "повторно решаване". "легален" means lawful.

### F04-B12 · S2 · terminology — "превод" vs "транслация" (candidate's comment p. 53 not applied throughout) (T04)
- **Where:** summaryBg.md §§ 4.3.2, 4.10.3; onePagerBg.md
- **Candidate's comment:** "като цяло превод в контекста на абстракцията трябва да стане англицизъмът транслация - изключение". The chapter now mixes both, sometimes in one paragraph (l. 92–103).
- **Now → Proposed:**
  - "Преводът обикновено е тривиален" → "Транслацията обикновено е тривиална"
  - "агентът трябва да преведе този залог към възел, върху който е обучен. Три преводача се използват най-често:" → "агентът трябва да транслира този залог към възел, върху който е обучен. Най-често се използват три транслатора:"
  - "Грешките при превода се натрупват" → "Грешките при транслацията се натрупват"
  - "2. **Вероятностно разпределение (линейно)**" → "2. **Вероятностно разделяне (линейно)**" (curated: "Вероятностно разделяне"; "разпределение" is *distribution*)
  - onePagerBg: "**абстракция на действията плюс преобразуване** (най-близко действие, вероятностно разпределение, псевдохармонично)" → "**абстракция на действията с транслация** (към най-близкото действие, вероятностно разделяне, псевдохармонично преобразуване)"
  - onePagerBg: "зависят от текущия преводач" → "зависят от текущия транслатор"
  - l. 101, l. 103, the § 4.10.3 heading, "Грешката в превода" and "Статичният превод" are in B04, B11, B16, C01 and B27.
- **Why:** Curated: "Action translation → Транслация на действия (deliberate anglicism …)". This is the candidate's own decision.

### F04-B13 · S2 · candidate's August comments not applied
- **Where:** summaryBg.md §§ 4.1, 4.3.2, 4.5
- **Now → Proposed:**
  - Comment p. 52 "незначителни" (on "незаинтересовани"). Now a non-word: "(премахване на доминирани или незаинтересоващи действия преди решаването)" → "(премахване на доминирани или незначителни действия преди решаването)"
  - Comment p. 55 "това да се премахне" (on the EMD-primer "Запомнете"). Still printed on p. 48. Delete the line "> **Запомнете:** разстоянието на Васерщайн сравнява формата на разпределението, а не само средната стойност — затова две раздавания с еднакви проценти на печалба все още могат да бъдат стратегически различни." The EN has no such line.
  - Comment p. 49 "игри" (on „игри-играчки"). Applied as "игрови задачи" instead: "мостът между „игрови задачи, които можем да изброим“ и „игрови задачи, които не можем“" → "мостът между „игри, които можем да изброим изцяло“ и „игри, които не можем“"
  - Comment p. 55 "биново генерално трябва да е булево". Not applied, and it should not be: "булево" means Boolean (true/false), and the bins are intervals of win probability. Fix what the comment was pointing at:
    - "Когато поддръжката е едномерна и подредена (бинирана вероятност за победа ∈ [0, 1])" → "Когато носителят е едномерен и подреден (вероятността за победа ∈ [0, 1], разделена на интервали)"
    - "еднократно линейно **обхождане** на биновете" → "едно линейно преминаване през интервалите"

    "поддръжка" means maintenance or support service; *support* of a distribution is "носител".
  - The fifth unapplied comment („Врътката“ → "фактор за настройка") is in B09. The remaining 21 chapter-4 comments are applied; the "покер - без ударение" check found no stress marks left.

### F04-B14 · S2 · stale cross-references to renamed headings
- **Where:** summaryBg.md §§ 4.3.1, 4.4, 4.10.3
- **Candidate's TOC comments** (p. 3): "Видове оси на абстракцията" and "решения по време на компилация". They were applied to the headings but not to the references.
- **Now → Proposed:**
  - "виж „Двете оси на абстракцията“ по-горе" → "вж. „Видове оси на абстракцията“ по-горе"
  - "изложен по-горе в раздела „Оси на абстракцията“" → "изложен по-горе в раздела „Видове оси на абстракцията“"
  - "(Критерият за сливане, Бюджетът на грешки, Конвейерът по време на компилиране)" → "(„Критерият за сливане“, „Бюджетът на грешките“, „Решения по време на компилация“)"
  - "всяка фаза от критерия за сливане до конвейера по време на компилиране е посветена" → "всяка фаза – от критерия за сливане до решенията по време на компилация – е посветена"
- **Why:** A reader looks for a section that does not exist under that name. "компилиране/компилация" and "грешки/грешките" also differ from the headings.

### F04-B15 · S2 · terminology — "явен/неявен" vs "изричен", "имплицитен маршрут" (candidate's TOC comment p. 4)
- **Where:** summaryBg.md §§ 4.1, 4.3.1, 4.3.2, 4.14
- **Candidate's comment:** "няма нужда от „имплицитен маршрут“". The heading was fixed; the body still uses the phrase.
- **Now → Proposed:**
  - "Мостът към глава 5 е имплицитният маршрут, току-що описан:" → "Мостът към глава 5 е току-що описаният неявен път:"
  - "Тази рецепта има два маршрута." → "Тази рецепта може да се следва по два пътя."
  - "При изрична информационна абстракция в обикновен вариант на CFR" → "При явна информационна абстракция в обикновения вариант на CFR"
  - "Проблемът с транслацията е **значителен** при изричната дискретизация" → "Проблемът с транслацията е **значителен** при явната дискретизация"
- **Why:** § 4.2 and table 7 define the pair "явен / неявен път". The body uses three other words for the same thing.

### F04-B16 · S2 · terminology — the two runtime patches named four ways
- **Where:** summaryBg.md §§ 4.10, 4.10.2, 4.10.3, 4.11
- **Now → Proposed:**
  - "Два пача са от значение" → "Две корекции са от значение"
  - "### Коригиране 1 — Безопасно решаване на под-игри" → "### Корекция 1 — Безопасно решаване на под-игри"
  - "### Пач 2 — Вложено решаване на под-игри (убиецът на превода на действия)" → "### Корекция 2 — Вложено решаване на под-игри (заместител на транслацията на действия)"
  - "чрез безопасно решаване на под-игри (Кръпка 1)" → "чрез безопасно решаване на под-игри (корекция 1)"
  - "включваща това действие (Кръпка 2)." → "включваща това действие (корекция 2)."
  - "## Архитектура: План и актуализации по време на работа" → "## Архитектура: план и корекции в реално време"
  - "актуализациите по време на работа възстановяват прецизността" → "корекциите в реално време възстановяват точността"
- **Why:** The section heading defines *patching* as "Корекция по време на изпълнение". "пач" is slang; "убиецът" is a calque of *killer*. "актуализации по време на работа" means *updates during work*.

### F04-B17 · S2 · blueprint compounds, "Reach", first mention (T06)
- **Where:** summaryBg.md §§ 4.9.2, 4.10.2, 4.10.3, 4.14
- **Now → Proposed:**
  - "в останалата част от това резюме се обозначава като **план**." → "в останалата част от главата се обозначава като **план** (blueprint)."
  - "Разширената под-игра се основава на план-стойности:" → "Разширената под-игра се закотвя към стойностите от плана:"
  - "Практическо усъвършенстване (*обхват*) пренася напред" → "Практическо усъвършенстване (Reach) пренася напред"
  - "На практика консервативните план-печалби могат да бъдат заменени с *оценки* на равновесната стойност. Това отпада строгата гаранция" → "На практика консервативните печалби по плана могат да бъдат заменени с *оценки* на равновесната стойност. Така строгата гаранция отпада"
  - "тъй като самите консервативни план-печалби са неточни." → "тъй като самите консервативни печалби по плана са неточни."
  - "тя е закотвена чрез план-стойности." → "тя е закотвена към стойностите от плана."
  - "преизчислява я с помощта на **безопасна под-игра-скеле** и добавя новата **подстратегия** към **плана**" → "преизчислява я по схемата на безопасното решаване на под-игри и добавя новата подстратегия към плана"
  - "Мостът към глава 6 е архитектурният план." → "Мостът към глава 6 е архитектурата „план + корекции“."
- **Why:**
  - Hyphen compounds such as "план-стойности" are not Bulgarian word formation.
  - *Reach* is the name of Brown & Sandholm's technique; "обхват" means *range*.
  - "Това отпада строгата гаранция" is ungrammatical (intransitive verb).
  - "архитектурният план" means *the architectural plan*.
  - First-mention rule 1 needs the English term. "резюме" is the old name of the chapter.

### F04-B18 · S2 · grammar
- **Where:** summaryBg.md §§ 4.1, 4.2, 4.3, 4.4, 4.5, 4.10.1
- **Now → Proposed:**
  - "повече от броя на атомите в наблюдаемата вселена с $10^{80}$ пъти повече." → "около $10^{80}$ пъти повече от броя на атомите в наблюдаемата вселена." The candidate's comment p. 50 was applied literally, so "повече" now appears twice.
  - "- **Беззагубен** — граничен случай $\beta \to \infty$ клони към безкрайност:" → "- **Беззагубно сливане** — граничният случай $\beta \to \infty$:" ("β → ∞ клони към безкрайност" says the same thing twice.)
  - "(идентичност, ако $\hat G$ представлява единствено информационна абстракция; нетривиален, ако включва и абстракция на действията" → "(тъждественото преобразуване, ако $\hat G$ е само информационна абстракция, и нетривиално преобразуване, ако включва и абстракция на действията" ("идентичност" is feminine; "нетривиален" is masculine and has no noun.)
  - "Трета ос, *усъвършенстване във време на изпълнение*, е независима" → "Трета ос, *усъвършенстване по време на изпълнение*, е независима"
  - "Разстоянието на Васерщайн, дадени две вероятностни разпределения върху една и съща носеща област, представлява минималното количество „работа“" → "За две вероятностни разпределения върху един и същ носител разстоянието на Васерщайн е минималното количество „работа“" ("дадени …" is a calque of *Given …*.)
  - "Две HSD с една и съща средна стойност могат да имат напълно различни форми: остро „стабилна средна ръка“ срещу бимодална „успех или провал“ ръка." → "Две HSD с една и съща средна стойност могат да имат напълно различна форма: тясно разпределение с един връх („стабилна средна ръка“) или бимодално („успех или провал“)." ("остро" is an adverb with no noun; the quotes break the phrase.)
  - "тя зависи от стойността $P_1$, която би получил, ако вместо това беше избрал *Sell*." → "тя зависи от стойността, която $P_1$ би получил, ако вместо това беше избрал „Продай“."

### F04-B19 · S2 · calques and wrong words (§§ 4.6–4.14)
- **Now → Proposed:**
  - "Три инструмента за количествено определяне, които се подреждат по строгост и формална прецизност в обратна зависимост." → "Три инструмента за количествена оценка, подредени така, че точността на оценката расте, а формалната строгост намалява." (The BG orders *rigour* against *precision*; the EN says "increasing in tightness and decreasing in formal rigour".)
  - "Дадена е абстракция със загуби с константи на отпуснатата връзка за всяко сливане, които се сумират — претеглени според честотата, с която всяка информационна съвкупност действително се достига по време на игра — и така се получава горна граница на експлоатируемата разлика." → "За абстракция със загуби допустимите отклонения на отделните сливания се сумират, претеглени с вероятността всяко информационно множество действително да бъде достигнато в игра, и така се получава горна граница на разликата в експлоатируемостта." ("отпусната връзка" means a loose connection.)
  - "всяко сливане допринася към бюджет на отпускането" → "всяко сливане добавя своето допустимо отклонение към общия бюджет на грешката"
  - "Теглото на достижимостта е ключовата идея." → "Ключовата идея е претеглянето по вероятността за достигане."; "най-важната ѝ идея е теглото на достижимостта." → "най-важната ѝ идея е претеглянето по вероятността за достигане." (curated: "Граница, претеглена по достигането")
  - "> **Запомнете:** Емпиричната абстракция е бюджетно предположение, което трябва да бъде измерено след решаването." → "> **Запомнете:** емпиричната абстракция е приближение в рамките на бюджета, чието качество трябва да се измери след решаването." ("бюджетно" means *budgetary* or *cheap*.)
  - "**Глобалната оптимизация е невъзможна.**" → "**Глобалната оптимизация е практически неприложима.**" (NP-completeness is not impossibility; the EN says "off the table".)
  - "**Разпределение-съзнателен срещу очакваностойностен.**" → "**Отчитащи разпределението срещу основани на очакването.**"
  - "> **Запомнете:** gameShrink търси в *сигналното дърво* всяко свободно сливане" → "> **Запомнете:** GameShrink търси в *сигналното дърво* всяко сливане без загуба" ("свободно" means *unconstrained*; the EN says *free* as in free of cost. The capital G is lost.)
  - "Нескъпата версия изгражда под-игра непосредствено след" → "По-евтиният вариант изгражда под-игра непосредствено след"
  - "Повечето реални действия извън дървото не се верижат" → "Повечето реални действия извън дървото не образуват вериги"
  - "проблемът по време на компилация става решим" → "задачата по време на компилация става изчислително поносима" (*tractable* is not *solvable*; F07-T06 pattern)
  - "Парето изгледът представлява окончателната и най-правилна диагноза." → "Изгледът на Парето е правилната крайна проверка."; "Грубите интервали и абстракцията на действията" → "Грубите клъстери и абстракцията на действията" (*buckets* are not *intervals*; "диагноза" is medical)
  - "Това са насочващи указатели — реалните реализации попадат в глави 5–6." → "Това са само препратки напред – реализациите са в глави 5 и 6."; "## Връзки и насочващи указатели" → "## Връзки и препратки напред"

### F04-B20 · S2 · terminology — information set rendered four ways
- **Where:** summaryBg.md § 4.8; onePagerBg.md (6×); fig. 16 axis (G04)
- **Now → Proposed:**
  - "**Две надеждни сравнения при равни бюджети за информационни набори.**" → "**Две надеждни сравнения при еднакъв брой информационни множества.**"
  - "при еднакъв бюджет на множеството от информационни състояния" → rewritten in C02
  - "информационна съвкупност" → rewritten in B19
  - onePagerBg: "информационни набора" (6×) → "информационни множества". For example, "от **936 до 288** информационни набора" → "от **936 до 288** информационни множества"; "**10,304 -> 2,968** информационни набора" → "**10,304 -> 2,968** информационни множества".
- **Why:** Curated: "Information set → Информационно множество", used everywhere else in the chapter.

### F04-B21 · S2 · poker terms and variant names (F07-T02; T08)
- **Where:** summaryBg.md §§ 4.1, 4.6.2, 4.10
- **Now → Proposed:**
  - "увеличава разклоняването на възел от 3 (пас/залог/повишаване във фиксиран лимит) до 5–10" → "увеличава разклоняването на възел от 3 (пас/плащане/повишаване в лимитния вариант) до 5–10" (EN "fold/call/raise"; "залог" for *call* is F07-T02)
  - "- **Скрити състояния** — Тексас холдем раздава 2 скрити карти от 52" → "- **Скрити състояния** — В тексаски холдем се раздават по 2 скрити карти от 52"
  - "- **Коефициент на разклоняване** — Покер без лимит позволява" → "- **Коефициент на разклоняване** — Безлимитният покер позволява" (curated "Безлимитен")
  - "Комбинираният брой информационни множества в хедс-ъп безлимит Холдем е" → "Броят на информационните множества в безлимитния тексаски холдем за двама играчи е"
  - "победи най-добрите играчи в хедс-ъп безлимит тексаски холдем." → "победи най-добрите професионалисти в безлимитния тексаски холдем за двама играчи."
  - "*Пример:* Обединяването на J и Q в един „клъстер с ниски карти“" → "*Пример:* Обединяването на вале и дама в един „клъстер с ниски карти“" (curated J/Q/K → Вале/Дама/Поп; the level-1 example already says "вале")
- **Why:** One name per game variant. "хедс-ъп" is jargon, and "Холдем" is capitalised in one place and not in others.

### F04-B22 · S2 · Latin letters inside Cyrillic words
- **Where:** summaryBg.md § 4.1 "отчетенa" (Latin a, U+0061); § 4.14 "неврoнното" (Latin o, U+006F)
- **Now → Proposed:** "Deep CFR и неврoнното приближение на равновесие" → "Deep CFR и невронното приближение на равновесие". The sentence with "отчетенa" is rewritten in C05.
- **Why:** Search, hyphenation and spell-check fail on mixed-script words.

### F04-B23 · S2 · EMD primer: "премествач на пръст", Cyrillic author names, "извличане на изображения"
- **Where:** summaryBg.md § 4.5 "**Произход и други наименования.**"
- **EN:** "Rubner, Tomasi & Guibas (2000) popularised the "Earth Mover's Distance" name in computer vision for image retrieval."
- **Now → Proposed:** "Името „Разстояние на премествача на пръст“ е популяризирано от Рубнер, Томази и Гуибас (2000) в областта на компютърното зрение за извличане на изображения." → "Името Earth Mover's Distance (EMD) е популяризирано от Rubner, Tomasi и Guibas (2000)[^rubner2000] в компютърното зрение при търсенето на изображения по съдържание." New footnote, verified in Crossref: `[^rubner2000]: Rubner, Y., Tomasi, C. & Guibas, L. J. (2000). "The Earth Mover's Distance as a Metric for Image Retrieval." *International Journal of Computer Vision*, 40(2), 99–121.`
- **Why:**
  - "премествач" is not a Bulgarian word. The name the reader will meet in the literature is the English one, and the curated glossary keeps "EMD".
  - Rule 6 keeps author surnames of cited works in Latin script.
  - "извличане на изображения" means extracting images; *retrieval* is search.

### F04-B24 · S2 · meaning — Deep-RL counterparts: *equivariant* rendered as "инвариантни" (T07)
- **Where:** summaryBg.md § 4.13
- **EN:** "lossless ↔ permutation-equivariant networks (Deep Sets), bounded lossy ↔ information bottlenecks in recurrent/transformer policies" / "exact equilibrium re-solvers"
- **Now → Proposed:**
  - "беззагубен ↔ инвариантни спрямо разместване мрежи (Deep Sets), ограничена загуба ↔ стеснения на информацията в рекурентни/трансформър политики" → "беззагубен ↔ мрежи, еквивариантни спрямо пермутации (Deep Sets), ограничена загуба ↔ информационно стеснение в политики с рекурентни мрежи или трансформъри"
  - "точните решаващи средства за равновесие" → "точните методи за изчисляване на равновесие"
- **Why:** Equivariance and invariance are different properties. The settled glossary entry is wrong (T07).

### F04-B25 · S3 · consistency polish
- **Now → Proposed:**
  - "> **Не забравяйте:** информационната абстракция" → "> **Запомнете:** информационната абстракция" (every other callout says "Запомнете")
  - "(a) броят на различните скрити състояния" / "(b) коефициентът" / "(c) дълбочината" → "(а)", "(б)", "(в)". The same applies to "(a) на **картата на възлите**" / "(b) на **обхождането**" in § 4.3.1.
  - "### Инструмент 2 — прокси на разстоянието на Васерщайн" → "### Инструмент 2 — Заместваща оценка чрез разстоянието на Васерщайн"; "### Инструмент 3 — директен оценител CFR-BR" → "### Инструмент 3 — Пряка оценка чрез CFR-BR"
  - "(Информационно стеснение)" → "(информационно стеснение)"

### F04-B26 · S1 · meaning — one-pager: *floor* as "таван", *early seed* as "ранно начално число"
- **Where:** onePagerBg.md "**Ключови резултати (измерени).**" and "**Връзка с дисертацията.**"
- **EN:** "*Lossy card buckets install a floor that compute cannot lift.*" / "the Pareto frontier of the two is an early seed of Contribution #3's evaluation methodology"
- **Now → Proposed:**
  - "*Загубените клъстери за карти поставят таван, който изчислителната мощност не може да преодолее.*" → "*Клъстерите на карти със загуби поставят долна граница на експлоатируемостта, която допълнителните изчисления не могат да понижат.*"
  - "представлява ранно начално число за методологията за оценяване в принос №3" → "е зародишът на методологията за оценяване от принос 3"
- **Why:**
  - A *floor* is the lowest exploitability the abstraction can reach. "таван" (ceiling) says the opposite.
  - "начално число" is the glossary term for a *random* seed (F07-B19), so the BG says "an early random seed for the methodology".
  - "изчислителна мощност" is F07-T12.

### F04-B27 · S2 · one-pager — calques, terms, agreement
- **Where:** onePagerBg.md
- **Now → Proposed:**
  - "(изплащанията в Ледюк зависят единствено от ранга и дали тайната карта съвпада с борда" → "(печалбите в Ледюк зависят единствено от ранга и от това дали частната карта образува чифт с общата" (payoff → печалба; *pairs the board* means forms a pair, not "coincides")
  - "(характеристика за силата на ръката, разстояния от ЕМД тип, k-средни, в режими на перфектно и неперфектно извикване)" → "(признаци за силата на ръката, разстояния от типа EMD, k-средни, с пълна и с непълна памет)" (EMD stays in Latin; B03)
  - "Тестван с CFR+ при общ бюджет от **180 секунди**, 3 семена," → "Всичко е тествано с CFR+ при общ бюджет от **180 секунди**, с 3 начални числа,"; "така че трите семена не са независими стохастични изпълнения" → "така че трите изпълнения не са независими" (F07-B19)
  - "за същото време на часовника" → "за същото реално време" (curated "Бюджет в реално време")
  - "дали изчислителната мощност, спестена от намалението" → "дали изчислителното време, спестено от намалението" (F07-T12)
  - "*Абстракция на действията е опасната ос.*" → "*Абстракцията на действията е опасната ос.*"
  - "пост-флоп разпределенията на силата на ръката в Ледюк" → "разпределенията на силата на ръката в Ледюк след откриването на общата карта" (Leduc has no flop)
  - "базираното на типове моделиране на противника от глава 7" → "типово базираното моделиране на противника от глава 7" (glossary)
  - "а неговият уверен, но погрешен неуспех представлява неправилна спецификация на преобразуването на действие в друга форма." → "а неговият провал – уверено, но погрешно убеждение – е същата грешна спецификация като при транслацията на действия, само в друга форма." (The BG reads "misspecification of converting an action into another form".)
  - "Статичният превод е крехък по конструкция, поради което под-играта и вложеното решаване (Глава 6) се явяват производствено решение за действия извън дървото." → "Статичната транслация е крехка по самото си устройство, затова решаването на под-игри и вложеното решаване (глава 6) са отговорът на действията извън дървото, използван в реалните системи." (*subgame solving* was parsed as "the subgame")
  - "Дали наблюдаваната тук йерархия - абстракция на карти оцеляваща, абстракция на действията разрушителна - ще се запази" → "Дали измереният тук ред - абстракцията на картите е поносима, а абстракцията на действията е разрушителна - ще се запази" (see also C01)

## T — Glossary-level terminology

### F04-T01 · S1 · "lossy → загубен", "lossy card bucketing → загубено групиране на карти"
- **Where:** `llmPipeline/glossary_settled.md`; printed 8× in chapter 4 and 3× in its one-pager (B01).
- **Now → Proposed:** "загубен" → "със загуби" (adjectival phrase); "загубено групиране на карти" → "групиране на карти със загуби".
- **Why:** "загубен" means *lost*. The curated `terminology_EN_BG.md` already forbids "загубна". The settled file contradicts it and the pipeline follows the settled file.

### F04-T02 · S1 · "recall → извличане", "recall regimes → режим на извикване"
- **Where:** glossary_settled.md; printed in § 4.9.2 and the one-pager (B03).
- **Now → Proposed:** "recall" (in games) → "памет"; "recall regimes" → "режими на паметта"; "perfect/imperfect-recall buckets → кошчета с …" → "клъстери с пълна/непълна памет" ("кош" is retired by the curated file).
- **Why:** "извличане/извикване" is information-retrieval or function-call vocabulary.

### F04-T03 · S2 · exploitability gap: two glossaries, neither right
- **Where:** settled "exploitability gap → експлоатируема разлика" (freq 6); curated "Exploitability gap → Пропуск в експлоатируемостта".
- **Now → Proposed:** both → "разлика в експлоатируемостта".
- **Why:** "експлоатируема разлика" means *an exploitable difference*. "пропуск" means an omission or lapse. Δ_abs is literally the difference of two exploitabilities (B02). This also affects chapters 5, 6 and 8, which reuse the term.

### F04-T04 · S2 · "translation → превод", "translation errors → грешки при превода", "pseudo-harmonic mapping → псевдохармонично отображение"
- **Where:** glossary_settled.md, against curated "Action translation → Транслация на действия" and "Pseudo-harmonic mapping → Псевдохармонично преобразуване".
- **Now → Proposed:** settled entries → "транслация", "грешки при транслацията", "псевдохармонично преобразуване" (in the abstraction sense only; *translation* of text stays "превод").
- **Why:** The candidate asked for this in August (B12). The settled file keeps reintroducing "превод".

### F04-T05 · S2 · suit isomorphism: "бои" (settled, corpus) vs "цветове" (curated)
- **Where:** curated "Suit isomorphism → Изоморфизъм на цветовете (Suit = цвят (на карта))"; settled "suit isomorphism → изоморфизъм на боите"; chapter 4 uses "бои" consistently (≈ 15×).
- **Now → Proposed:** change the curated entry to "Изоморфизъм на боите", with suit → "боя".
- **Why:** "боя" is the standard Bulgarian word for a card suit, and the corpus already uses it. Changing the curated line is one edit, against ≈ 15 in the text.

### F04-T06 · S2 · blueprint: curated "Схема", corpus "план", settled "план-стратегия"
- **Where:** curated "Blueprint (strategy) → Схема (на стратегията)". Corpus counts of "план*": chapter 4 ≈ 15, chapter 6 ≈ 85, chapter 8 ≈ 19. Settled: "blueprint strategy → план-стратегия", "blueprint floor → план за долна граница".
- **Now → Proposed:** decide once. Recommended: keep "план" (the corpus usage), with "(blueprint)" at first mention in chapter 4 (B17). Drop hyphen compounds ("план-стойности", "план-стратегия" → "стойностите от плана", "стратегията-план" → "планът"). Update the curated entry.
- **Why:** The two glossaries disagree and the text follows neither cleanly. "план" also collides with "план за обучение" (the bundle's own name), so the first-mention gloss matters.

### F04-T07 · S2 · "permutation-equivariant → инвариантен спрямо разместване"
- **Where:** glossary_settled.md; printed in § 4.13 (B24).
- **Now → Proposed:** → "еквивариантен спрямо пермутации"; keep "permutation-invariant → инвариантен спрямо пермутации".
- **Why:** The entry maps *equivariant* to *invariant*, which are different properties.

### F04-T08 · S2 · poker variant names, five forms
- **Where:** glossary_settled.md:
  - "heads-up no-limit Texas hold'em → Тексаски но-лимит покер за двама"
  - "heads-up no-limit → хедс-ъп безлимит покер"
  - "no-limit texas hold'em → No-Limit Texas Холдем" (mixed script)
  - "no-limit hold'em → No-Limit Холдем"
  - "heads-up limit texas hold'em → хедс-ъп лимит тексаски холдем"
- **Now → Proposed:** HUNL → "безлимитен тексаски холдем за двама играчи"; HULHE → "лимитен тексаски холдем за двама играчи"; no-limit → "безлимитен" (curated).
- **Why:** Chapter 4 alone prints four variants (B21).

### F04-T09 · S3 · "river → река"
- **Where:** glossary_settled.md; printed as "канонични река бордове" (§ 4.6.3, rewritten in C05).
- **Now → Proposed:** "river" → "ривър (петата обща карта)", the same way "flop → флоп".
- **Why:** "река" is a literal calque, meaningless to a reader who does not play poker.

## C — Content

### F04-C01 · S1 · The action-abstraction results measure the evaluation harness, not translation
- **Where:**
  - summaryEn.md l. 330, "In Extended Leduc, adding action abstraction on top of suit isomorphism produced a compact tree, but the translated strategy was highly exploitable. This is why the literature moves from static action translation toward nested subgame solving: the full action actually played by the opponent often matters too much to round away.[^brown2017]"
  - summaryBg.md § 4.12, the same passage
  - onePager(Bg).md: "Translation error dominates the total." / "Грешката в превода доминира общата стойност."; the headline "roughly **100x worse**"; the open question "card abstraction survivable, action abstraction ruinous"
- **Problem** (from the code and results):
  1. **The translators never engage.** In `implementation/step04/phase4/day03_train.py::_strategy_with_translation`, `translate(name, ABSTRACT_HIGH_OFF_TREE, ABSTRACT_LOW, ABSTRACT_HIGH_OFF_TREE)` is always called with b = b_high = 2.0. All three translators therefore return `{2.0: 1.0}`. `.day03_results.json` confirms it: nearest, probability_split and pseudo_harmonic all give 1.4015325672357215.
  2. **The rule doubles the agent's own bets.** Wherever the large bet is legal, the agent's *own* abstract small-bet mass is moved entirely onto the 2×pot bet, and the small bet gets 0. `day07_cfrplus_panels.py::_extended_strategy` does the same (`EXT_BET_LARGE` ← small-bet mass, `EXT_BET_SMALL` ← 0), and the Mini-NL benchmark calls the day-03 function with "nearest".
  3. **Opponent large bets are read as small ones**, via the key collapse `info_full.replace("l", "s")`.
  - The numbers 0.673 (Mini-NL) and 4.696 / 4.734 (Extended) therefore measure an agent that plays every bet it learned at twice the size. They do not measure the cost of rounding the opponent's off-tree bet. The chapter's reading of them, and the one-pager's "translation error dominates", are not supported. The one-pager's "Stated limitations" hedge ("depend on the current translator and deployment semantics") exists, but the summary has none.
- **Now → Proposed:**
  - summaryBg.md: "но получената стратегия беше силно експлоатируема. Поради това литературата се насочва от статична транслация на действия към вложено решаване на под-игри: действието, което опонентът реално изиграва, често е твърде важно, за да бъде закръглено.[^brown2017]" → "но внедрената стратегия беше силно експлоатируема. Тези стойности обаче измерват текущото правило за внедряване – всеки абстрактен малък залог се изиграва като голям, а големите залози на противника се четат като малки – а не качеството на трите транслатора, които в тази реализация не се задействат и дават еднакви резултати. Те показват колко може да струва наивното съпоставяне на абстрактното и реалното множество действия; отговорът на литературата за действията извън дървото е вложеното решаване на под-игри[^brown2017]."
  - EN: "but the translated strategy was highly exploitable. This is why … round away.[^brown2017]" → "but the deployed strategy was highly exploitable. These numbers measure the current deployment rule — every abstract small bet is played as the large bet, and opponent large bets are read as small — rather than the three translators, which never engage in this harness and return identical values. They show how much a naive mapping between the abstract and the real action set can cost; the literature's answer to off-tree actions is nested subgame solving.[^brown2017]"
  - One-pager EN: "Translation error dominates the total." → "Under the current deployment rule the mapping error dominates the total (see limitations)." BG: "Грешката в превода доминира общата стойност." → "При текущото правило за внедряване грешката от съпоставянето на действията доминира общата стойност (вж. ограниченията)."
  - Report §3.2 (report_en/bg) needs the same caveat.
- **Code fix, to rerun day 03 and the mini/extended panels:**
  - Map the agent's own abstract actions identically (small → small).
  - Apply `translate(name, b_actual, b_low, b_high)` only to the *opponent's* off-tree bet in the history, with its real pot fraction.
  - Until then, do not cite the action-abstraction numbers (extract, "To verify").

### F04-C02 · S2 · "Imperfect recall consistently wins" is stated as a law; the chapter's own runs do not reproduce it
- **Where:**
  - summaryEn.md l. 221, "Imperfect-recall abstractions outperform perfect-recall ones at matched info-set budget", and l. 254, "Imperfect recall consistently wins at a fixed bucket budget"
  - summaryBg.md § 4.8 and § 4.9.2
- **Problem:** In Texas hold'em this is a published finding. Johanson et al. (2013): imperfect-recall abstractions showed "a clear improvement in one-on-one performance and exploitability" and "can contain less exploitable strategies than equal sized perfect recall" ones. But the chapter gives no source, and its Leduc runs point the other way (`.day07_cfrplus_results.csv`; the bars are in fig. 13, the text never mentions them):
  - k3/k5 imperfect (108 information sets) reach 0.574 against 0.382 for perfect recall (228).
  - At a similar size, k3 imperfect (108) gets 0.574 against k2 perfect (132) 0.571.
  - Only k2 imperfect (72) gets 0.528 against k2 perfect (132) 0.571.

  "последователно" in the BG also means *sequentially*, not *consistently*.
- **Now → Proposed:**
  - "Абстракциите с непълна памет превъзхождат тези с пълна памет при еднакъв бюджет на множеството от информационни състояния — свободата за преразпределение на клъстерите е емпирично по-ценна от изгубената непрекъснатост." → "В тексаски холдем абстракциите с непълна памет превъзхождат тези с пълна памет при еднакъв брой информационни множества – свободата да се преразпределят клъстерите се оказва по-ценна от изгубената непрекъснатост[^johanson2013abs]."
  - "Непълната памет последователно надделява при фиксиран бюджет на клъстерите — капацитетът се използва за кръгове, които имат значение, вместо за запаметяване на историята." → "В тексаски холдем непълната памет надделява при фиксиран бюджет на клъстерите – капацитетът се изразходва за рундовете, които имат значение, вместо за запомняне на историята[^johanson2013abs]. В малкия Ледюк от тази глава предимството не се потвърждава: при сходен размер (108 срещу 132 информационни множества) абстракцията с непълна памет не е по-добра (0.574 срещу 0.571; фиг. 13)."
  - EN equivalents: "In Texas hold'em, imperfect recall wins at a fixed bucket budget …[^johanson2013abs] The Leduc runs of this chapter do not reproduce it: at a similar size (108 vs 132 information sets) imperfect recall is no better (0.574 vs 0.571; Figure 13)."

### F04-C03 · S2 · CFR-BR: the 1/3 figure is right, the explanation is wrong, and there is no citation
- **Where:** summaryEn.md l. 202–204; summaryBg.md § 4.7.3
- **EN:** "it returns the closest representable Nash approximation … a large fraction of measured "abstraction error" in the literature is actually *solving error in disguise* — the abstraction itself was capable of better, but the solver hadn't converged."
- **Problem:**
  - The 1/3 is verified. Johanson et al. (2013): "In practice, the exploitability of these CFR-BR strategies is as little as 1/3 of those found via CFR".
  - The explanation is not. CFR does converge, to an equilibrium of the *abstract* game, and that equilibrium is not the least exploitable strategy the abstraction can represent (Johanson et al. 2012, 2013: CFR-BR strategies "are not abstract game equilibria, as are found by CFR, but instead are the closest approximations to a real game equilibrium that can be represented within an abstraction"). The loss comes from the target, not from non-convergence.
  - The result is stated for perfect-recall abstractions. BG "не се е сходил" is also not a verb form.
- **Now → Proposed:**
  - "Най-силната мярка: тя връща най-близкото представимо Нашево равновесие, което може да бъде изразено чрез абстракцията" → "Най-силната мярка: за абстракции с пълна памет тя намира стратегията в абстракцията с най-ниска експлоатируемост в пълната игра"
  - "Изводът е, че значителна част от измерената „грешка на абстракцията“ в литературата всъщност представлява *скрита грешка при решаване* — самата абстракция е била способна на по-добро представяне, но решавачът не се е сходил." → "Изводът е, че част от измерената „грешка на абстракцията“ не се дължи на самата абстракция, а на избора на *равновесието на абстрактната игра* за цел: CFR се сходи към него, но то не е най-малко експлоатируемата стратегия, която абстракцията може да изрази[^johanson2013abs]."
  - EN: "The takeaway: part of the measured "abstraction error" is not the abstraction's fault but the choice of the abstract game's equilibrium as the target — CFR converges to it, yet it is not the least exploitable strategy the abstraction can express.[^johanson2013abs]"

### F04-C04 · S2 · Table 7 claims a formal bound for the whole explicit route; refinement can even hurt
- **Where:** summaryEn.md l. 64 "| Guarantee | Bounded exploitability gap in the **same** game (formal exploitability bound) |"; summaryBg.md table 7; § 4.6.3
- **Problem:**
  - Only lossless abstraction (Gilpin & Sandholm 2007) and bounded abstractions of the Kroer–Sandholm type carry a formal bound.
  - The k-means/EMD, imperfect-recall abstractions that practice uses, and that this chapter implements, carry none. § 4.6.3 says so itself: "There is no formal exploitability guarantee here".
  - Waugh et al. (2009): "Refining an abstraction can actually lead to a weaker strategy", with examples in Leduc for both card and betting abstraction.
- **Now → Proposed:**
  - "| Гаранция | Ограничена експлоатируема разлика в **същата** игра (формална граница на експлоатируемостта) |" → "| Гаранция | Формална граница на разликата в експлоатируемостта само за беззагубни и ограничени абстракции; за емпиричните (k-средни + EMD) – никаква |". EN: "| Guarantee | A formal bound on the exploitability gap only for lossless and bounded abstractions; none for empirical (k-means + EMD) ones |".
  - Append to § 4.6.3 after "като експлоатируемостта на получената стратегия се измерва.": " Нещо повече, дори по-финото разделяне не гарантира по-ниска експлоатируемост[^waugh2009]." EN: " Worse, even refining an abstraction does not guarantee lower exploitability.[^waugh2009]"
  - New footnote (verified: PDF abstract and Crossref pages): `[^waugh2009]: Waugh, K., Schnizlein, D., Bowling, M. & Szafron, D. (2009). "Abstraction Pathologies in Extensive Games." *AAMAS*, 781–788.`

### F04-C05 · S2 · Game-size numbers: the 10¹⁷ and 10⁹ claims are wrong
- **Where:** summaryEn.md l. 26 and l. 170; summaryBg.md §§ 4.1, 4.6.3
- **EN:** "The number of hand-vs-board distinguishable situations is on the order of $10^{17}$ before counting betting history." / "(Texas hold'em has $\sim 10^9$ canonical river boards)"
- **Problem:**
  - Hole-card + board combinations are C(52,2)·C(50,5) ≈ 2.8 × 10⁹. After suit isomorphism on the last round there are 2,428,287,420 (Johanson et al. 2013, verified in the PDF).
  - 3.16 × 10¹⁷ is the number of *game states* of heads-up limit hold'em *including* betting (Bowling et al. 2015, verified in the PDF).
  - The 2.4 × 10⁹ counts hand + board combinations, not boards; boards alone are ≈ 2.6 × 10⁶.
- **Now → Proposed:**
  - "Броят на различимите ситуации „ръка срещу борд“ е от порядъка на $10^{17}$ преди да бъде отчетенa историята на залозите." → "Само комбинациите от скрити и общи карти са около $2.8 \times 10^{9}$, още преди да се отчете историята на залозите; с нея лимитният вариант за двама играчи достига $3.16 \times 10^{17}$ състояния[^bowling2015]."
  - "(тексас холдем има $\sim 10^9$ канонични река бордове)" → "(в тексаски холдем на последния рунд има около $2.4 \times 10^9$ канонични комбинации от скрити и общи карти[^johanson2013abs])"
  - EN: "Hole-card and board combinations alone number about $2.8 \times 10^{9}$ before betting history; with it, heads-up limit hold'em reaches $3.16 \times 10^{17}$ states.[^bowling2015]" / "(Texas hold'em has about $2.4 \times 10^9$ canonical private/public card combinations on the last round)"
  - New footnote (verified in Crossref): `[^bowling2015]: Bowling, M., Burch, N., Johanson, M. & Tammelin, O. (2015). "Heads-up Limit Hold'em Poker Is Solved." *Science*, 347(6218), 145–149.`
  - The ~10¹⁶¹ information sets of HUNL is **correct**: 6.37 × 10¹⁶¹ in Johanson (2013), arXiv:1302.7008, Table 6.

### F04-C06 · S2 · "Every competitive heads-up no-limit AI since 2017 (Libratus, Modicum, Pluribus)" used the blueprint pattern
- **Where:** summaryEn.md l. 300; summaryBg.md § 4.11 — "който всеки състезателен изкуствен интелект за покер без лимит един на един от 2017 г. насам (Libratus, Modicum, Pluribus) използва"
- **Problem:**
  - Pluribus plays *six-player* no-limit (Brown & Sandholm 2019, Science 365:885).
  - DeepStack, which also beat professionals at heads-up no-limit in 2017, "does not compute and store a complete strategy prior to play" (Moravčík et al. 2017, verified in the PDF). It is a counter-example to "every".
  - The Libratus footnote supports only Libratus.
- **Now → Proposed:** "Целият конвейер вече се свежда до един архитектурен модел, който всеки състезателен изкуствен интелект за покер без лимит един на един от 2017 г. насам (Libratus, Modicum, Pluribus) използва:" → "Целият конвейер се свежда до един архитектурен модел, използван от водещите системи за безлимитен покер след 2017 г. – Libratus и Modicum при двама играчи и Pluribus при шестима (DeepStack е изключение: той не изчислява предварително стратегия за цялата игра):". EN: "…the architectural pattern used by the leading no-limit poker AIs since 2017 — Libratus and Modicum heads-up, Pluribus six-handed (DeepStack is the exception: it computes no whole-game strategy in advance):". Add footnotes `moravcik2017` and `brown2019` (S06).

### F04-C07 · S2 · Nested solving "10–100× lower than every prior action-translation method … on HUNL" overstates the source
- **Where:** summaryEn.md l. 290; summaryBg.md § 4.10.3 — "*Емпирично въздействие.* При **хедс-ъп безлимит покер**"
- **Problem:** Brown & Sandholm (2017, arXiv v3, Table 4) compare nested subgame solving against one translator, the randomized pseudo-harmonic mapping, in one game: no-limit *flop* hold'em with 0.5/0.75/1.0-pot bets and no information abstraction. The result is 1,465 mbb/h against 119–150 mbb/h, i.e. about 10×. There is no 100× figure, no dependence on abstraction size, and no HUNL measurement. The paper's claim is that nested solving "significantly outperforms the prior state-of-the-art approach, action translation".
- **Now → Proposed:** "*Емпирично въздействие.* При **хедс-ъп безлимит покер** експлоатируемостта на **вложеното решаване на под-игри** срещу действия на противника извън дървото е **10–100 пъти по-ниска** от тази на всеки предходен метод за транслация на действия, в зависимост от степента на абстракция.[^brown2017]" → "*Емпирично въздействие.* В опростен безлимитен вариант (холдем, игран само до флопа) вложеното решаване на под-игри срещу залози на противника извън дървото има около 10 пъти по-ниска експлоатируемост от псевдохармоничната транслация (119–150 срещу 1465 mbb на раздаване)[^brown2017]." EN: "*Empirical impact.* In a no-limit flop hold'em test game, nested subgame solving against off-tree opponent bets was about 10× less exploitable than pseudo-harmonic translation (119–150 vs 1,465 mbb/hand).[^brown2017]"

### F04-C08 · S2 · The strictness levels are ordered backwards
- **Where:** summaryEn.md l. 148 "Three nested levels of strictness, weakest at the top."; summaryBg.md § 4.6 — "Три вложени нива на строгост, подредени от най-слабо към най-силно."
- **Problem:** Level 1 (lossless) is the *strictest* merging criterion; level 3 (empirical) is the loosest.
- **Now → Proposed:** "Три вложени нива на строгост, подредени от най-слабо към най-силно." → "Три вложени нива на строгост, подредени от най-строгото към най-хлабавото."; EN "weakest at the top" → "strictest at the top".

### F04-C09 · S2 · Stale references
- **Where:**
  - summaryEn.md l. 67 "chapters 11–12 (sequence models)"; summaryBg.md table 7 "глави 11–12 (последователни модели)". Chapter 11 is coalition formation; sequence models are chapter 12 only.
  - summaryEn.md l. 108 "the standard step-3 metric"; summaryBg.md § 4.4 "експлоатируемостта е стандартният показател на трета стъпка:"
  - summaryBg.md § 4.12 "Абстракцията на действията беше най-рисковата част от стъпката." The EN already says "chapter".
- **Now → Proposed:**
  - "глави 11–12 (последователни модели)" → "глава 12 (последователни модели)"; EN "chapters 11–12 (sequence models)" → "chapter 12 (sequence models)"
  - "експлоатируемостта е стандартният показател на трета стъпка:" → "експлоатируемостта е стандартният показател от глава 3:"; EN "the standard step-3 metric" → "the standard metric from Chapter 3"
  - "Абстракцията на действията беше най-рисковата част от стъпката." → "Абстракцията на действията беше най-рисковата част от главата."

### F04-C10 · S2 · Tool 2: "EMD correlates well with post-solve exploitability" is not in the cited source, and the chapter's own data contradict it
- **Where:** summaryEn.md l. 198; summaryBg.md § 4.7.2 — "корелира добре с експлоатируемостта след решаването"
- **Problem:**
  - Johanson et al. (2013) use EMD as the *clustering* distance. The metric they show to be "well-correlated with the in-game performance" is CFR-BR exploitability, not EMD.
  - In this chapter's Pareto data (`phase4/.day05_pareto_table.csv`) the EMD proxy is 0.0 for the k3/k5 abstractions, whose gap is 0.46–0.70, and 45–55 for k2 (gap 0.96–1.01). It does not track the gap.
- **Now → Proposed:** "То представлява *прокси*, а не граница — корелира добре с експлоатируемостта след решаването, но не носи формална гаранция.[^johanson2013abs]" → "То е *заместваща оценка*, а не граница, и не носи формална гаранция[^johanson2013abs]; в експериментите на тази глава то не проследява експлоатируемостта (нула при k = 3 и k = 5 въпреки разлика от 0.46–0.70)." EN: "It is a *proxy*, not a bound, and carries no formal guarantee;[^johanson2013abs] in this chapter's runs it does not track exploitability (zero for k = 3 and k = 5 despite gaps of 0.46–0.70)."

### F04-C11 · S3 · Precision
- **Now → Proposed:**
  - "като равенство се достига тогава и само тогава, когато абстракцията е **беззагубна**" → "като равенство има, когато абстракцията е беззагубна"; EN "with equality iff the abstraction is lossless" → "with equality if the abstraction is lossless". A lossy abstraction can still contain an exact equilibrium, as Leduc's full-rank buckets do here.
  - "пропорционално на тяхното разстояние от реалния залог" → "обратно пропорционално на разстоянието им от реалния залог"; EN "in proportion to their distance from the actual bet" → "in inverse proportion to their distance from the actual bet". The code (`day03_translators.py`) does it correctly.
  - "и строго по-ниска, когато локалните условия го позволяват" → delete; EN "and strictly lower whenever local conditions allow" → delete. Brown & Sandholm guarantee "no higher than … the blueprint", not strictly lower.
  - "Това е *причината* всяка практическа абстракция в покера след 2010 г. да бъде клъстеризационен конвейер ниво по ниво, а не глобален оптимизатор." → "Това съответства на практиката: абстракциите в покера се строят ниво по ниво чрез клъстеризация, а не чрез глобална оптимизация." The NP-completeness result (Kroer & Sandholm 2016, Thm. 3) postdates that practice, so it cannot be its cause.

## S — Sources

### F04-S01 · S2 · SOURCE_GAPS row 1, "two meanings of abstraction": soften, and cite the IB analogy
- **Where:** summaryBg.md § 4.2 — "Думата „абстракция“ в тази литература всъщност обозначава две операционно различни понятия."; EN l. 44
- **Proposal (soften + cite):**
  - "Думата „абстракция“ в тази литература всъщност обозначава две операционно различни понятия." → "В тази глава думата „абстракция“ се използва в два оперативно различни смисъла; в литературата невронното приближение обикновено се представя като алтернатива на абстракцията, а не като неин вид[^brown2019deep]."
  - EN: "In this chapter the word "abstraction" covers two operationally different things; the literature usually presents neural approximation as an alternative to abstraction rather than a kind of it.[^brown2019deep]"
  - Verified on the arXiv abstract of 1811.00164: Deep CFR "obviates the need for abstraction by instead using deep neural networks to approximate the behavior of CFR in the full game".
  - Footnote: `[^brown2019deep]: Brown, N., Lerer, A., Gross, S. & Sandholm, T. (2019). "Deep Counterfactual Regret Minimization." *ICML*; arXiv:1811.00164.`
- **Also:**
  - The "Information Bottleneck Lagrangian" (l. 46–48) and the "IB-style" column of table 7 are the candidate's analogy. No deep-RL method of chapters 5–6 has a β·I(S;Z) term. After "целевата функция на информационното стеснение" add "(по аналогия с метода на информационното стеснение[^tishby1999])".
  - Footnote: `[^tishby1999]: Tishby, N., Pereira, F. C. & Bialek, W. (1999). "The Information Bottleneck Method." arXiv:physics/0004057.` Verified on the arXiv abstract page; the Allerton venue is unverified.

### F04-S02 · S2 · SOURCE_GAPS row 2, pseudo-harmonic "state-of-the-art": cite, correct the description, soften
- **Where:** summaryBg.md § 4.3.2, item 3; EN l. 98
- **Problem:**
  - The chapter says the mapping "interpolate[s] in pot-fraction space rather than in the linear space of absolute bet amounts". Every mapping in the paper works in pot units. The pseudo-harmonic mapping differs because it is *derived* from the equilibrium of a simplified game, the clairvoyance game, in which a bet x is called with probability 1/(1+x).
  - "(state-of-the-art)" is English in the BG text.
  - Chapter 4 itself shows that nested solving superseded the mapping (C07).
- **Proposal (cite + correct):**
  - "3. **Псевдохармонично преобразуване** – интерполация в пространството на фракциите от пота, вместо в линейното пространство на абсолютните суми. Този подход отразява много по-точно стратегическата еквивалентност между два различни залога и представлява водещия стандарт (state-of-the-art) за транслация на залозите в покера." → "3. **Псевдохармонично преобразуване** – вероятностно преобразуване, изведено от равновесието на опростена покерна игра: залог $x$ (в части от пота) между абстрактните размери $A$ и $B$ се свързва с $A$ с вероятност $\frac{(B-x)(1+A)}{(B-A)(1+x)}$. В сравненията на авторите то е значително по-малко експлоатируемо от по-ранните евристични преобразувания в три малки покерни игри, сред които Кун и Ледюк, и е водещият статичен транслатор преди появата на вложеното решаване на под-игри (по-долу)[^ganzfried2013]."
  - EN: "3. **Pseudo-harmonic mapping** — a randomized mapping derived from the equilibrium of a simplified poker game: a bet $x$ (in pot units) between abstract sizes $A$ and $B$ is mapped to $A$ with probability $\frac{(B-x)(1+A)}{(B-A)(1+x)}$. In its authors' comparisons it is markedly less exploitable than earlier heuristic mappings in three small poker games, including Kuhn and Leduc, and it was the leading static translator before nested subgame solving (below).[^ganzfried2013]"
  - Verified in the IJCAI-13 PDF: formula; "achieves significantly lower exploitability than any of the prior approaches in the clairvoyance game, Kuhn poker, and Leduc Hold'em"; pages 120–127. Brown & Sandholm (2017) call action translation "the state-of-the-art prior approach".
  - Footnote: `[^ganzfried2013]: Ganzfried, S. & Sandholm, T. (2013). "Action Translation in Extensive-Form Games with Large Action Spaces: Axioms, Paradoxes, and the Pseudo-Harmonic Mapping." *IJCAI*, 120–127.`

### F04-S03 · S2 · SOURCE_GAPS row 3, EMD as the Level-3 similarity metric: cite
- **Where:** summaryBg.md § 4.6.3 — "- Използва се **разстояние на Васерщайн (EMD)** между векторите на характеристики като метрика за сходство."
- **Proposal (cite):** append "[^johanson2013abs][^ganzfried2014]" after "като метрика за сходство.".
  - Johanson et al. (2013), verified in the PDF: EMD over hand-strength histograms "provides a candidate distance function", computed "with a single pass over the histogram bars". This also sources the § 4.5 1-D claim.
  - Ganzfried & Sandholm (2014), verified in the PDF abstract and Crossref: "The leading abstraction algorithm … generates abstractions that have imperfect recall and are distribution aware, using k-means with the earth mover's distance". The same paper introduces *potential-aware* EMD abstraction (over the trajectory of future strength). The chapter does not mention it; one sentence would bring the pipeline up to date.
  - Footnote: `[^ganzfried2014]: Ganzfried, S. & Sandholm, T. (2014). "Potential-Aware Imperfect-Recall Abstraction with Earth Mover's Distance in Imperfect-Information Games." *AAAI*, 28(1).`

### F04-S04 · S2 · "HSD + EMD strictly dominates" overclaims, and the paragraph has no source
- **Where:** summaryBg.md § 4.8 — "HSD + разстояние на Васерщайн строго доминира клъстеризацията, базирана на очаквана стойност"; EN l. 220
- **Problem:** Johanson et al. (2013, conclusion, verified): "distribution-aware distance metrics provide a clear advantage once the abstract game is large enough". The same paper reports that Gilpin & Sandholm found "expectation-based abstractions yielded stronger strategies in small abstractions, but are surpassed as more buckets are made available". So the advantage is not strict dominance, and it is not universal.
- **Proposal (soften + cite):** "HSD + разстояние на Васерщайн строго доминира клъстеризацията, базирана на очаквана стойност, както по експлоатируемост, така и по процент победи в директен сблъсък срещу фиксирани опоненти." → "При достатъчно голяма абстракция HSD + разстояние на Васерщайн превъзхожда клъстеризацията по очаквана сила на ръката както по експлоатируемост, така и в директни срещи; при много малки абстракции очакването може да е по-добро[^johanson2013abs]." EN: "Once the abstraction is large enough, HSD + EMD beats expected-strength clustering on both exploitability and head-to-head play; in very small abstractions the expectation-based one can be stronger.[^johanson2013abs]" ("процент победи" is also wrong: poker performance is chips per hand, not a win percentage.)

### F04-S05 · S2 · Other unsourced or overreaching claims
- **Where / Proposal:**
  - § 4.3.2: "Емпирично именно там практическите изкуствени интелекти за покер губят най-много стойност" (EN l. 100, "This is empirically where practical poker AIs lose the most equity"). No source was found that ranks translation as the largest loss.
    - **Soften:** → "Такава уязвимост е наблюдавана на практика (агентът Tartanian1, 2007 г.)[^ganzfried2013], и това е оперативната причина…"
    - Verified in the IJCAI-13 PDF: a deterministic mapping is exploited by "betting slightly less than (A+B)/2"; "this phenomenon was observed in the 2007 Annual Poker Competition when the agent Tartanian1 used this mapping".
  - § 4.10.1, the Coin Toss example. Coin Toss is introduced by Brown & Sandholm (2017, § 2, verified); the paragraph cites nothing and the next one cites Burch et al. (2014). **Cite:** append "[^brown2017]" after "остава непроменена.".
  - § 4.7.3, CFR-BR: no citation (fixed in C03). § 4.2, IB: fixed in S01. § 4.1, card counts: fixed in C05.

### F04-S06 · S3 · Spot-check of the chapter's seven footnotes, and new footnotes
- **Findings:**
  - All seven are real papers with correct authors and years. Checked in Crossref, and in the PDFs where marked.
    - `gilpin2007`: J. ACM 54(5), art. 25. PDF: 3.1 billion nodes, signal tree 6,632,705, "over four orders of magnitude"; the ≈500× in § 4.9.1 is correct.
    - `kroer2014`: EC'14 621–638; EC'16 459–476. The arXiv PDF of the 2016 paper checks out: Theorem 3 NP-complete "even if there is only a single player, and the game tree has height two"; single-level reduction to clustering, 2-approximation in the metric case; leaf error "weighted by the probability of a given leaf being reached".
    - `johanson2013abs`: AAMAS 271–278.
    - `johanson2013size`: arXiv:1302.7008 (6.37 × 10¹⁶¹).
    - `burch2014`: AAAI 28(1).
    - `brown2017`: NIPS 2017; PDF checked.
    - `libratus`: Science 359(6374), 418–424.
- **Proposal (optional metadata):**
  - `brown2017`: "*NeurIPS*" → "*NIPS 2017* (Advances in Neural Information Processing Systems 30)"
  - `gilpin2007`: add "art. 25"
  - `johanson2013abs`: add "271–278"
  - `kroer2014`: add "621–638" and "459–476"
  - `johanson2013size`: add "arXiv:1302.7008"
- **New footnotes proposed in this review:** `waugh2009` (C04), `bowling2015` (C05), `rubner2000` (B23), `brown2019deep` and `tishby1999` (S01), `ganzfried2013` (S02, S05), `ganzfried2014` (S03), plus `moravcik2017` and `brown2019` for C06:
  - `[^moravcik2017]: Moravčík, M. et al. (2017). "DeepStack: Expert-Level Artificial Intelligence in Heads-Up No-Limit Poker." *Science*, 356(6337), 508–513.`
  - `[^brown2019]: Brown, N. & Sandholm, T. (2019). "Superhuman AI for Multiplayer Poker." *Science*, 365(6456), 885–890.`

  All were verified in Crossref or on arXiv, as stated in each finding.

## X — Structure

### F04-X01 · S2 · `brown2017` footnote markers point into chapter 3
- **Where:** marker 25 on p. 54 (§ 4.10.2) and p. 57 (§ 4.12)
- **Problem:** The note text "Safe and Nested Subgame Solving…" prints only on p. 41, the last page of chapter 3 (PyMuPDF text search of `allSummaries_bg.pdf`). The other six chapter-4 footnotes print within the chapter. This is F07-X01 confirmed for this chapter.
- **Fix:** the central fix of F07-X01 (per-chapter footnote label prefixes in `scripts/build_reports.py`).

### F04-X02 · S2 · Three half-empty pages
- **Where:** pp. 56, 57, 58: each holds one CFR+ panel and half a page of white space.
- **Fix:** G03. At figsize 8 × 4.2–5.0 in, printed full-width, two panels fit on one page.

### F04-X03 · S3 · Loose lists from trailing double spaces
- **Where:** summaryBg.md l. 53–55 and l. 97–98 end with two spaces (markdown hard break); the EN does not. They print with large gaps between items (pp. 43, 46).
- **Fix:** strip the trailing spaces on those five lines.
