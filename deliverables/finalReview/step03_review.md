# Step 03 — final review

**Summary:** The Bulgarian text is mostly fluent. The chapter's quantitative core, however, has errors a supervisor can check with a calculator. (1) The crossover analysis is off by a factor of two: 10,200 × (107/0.34)² × 20.6/19,470 = 1.07 M nodes, not 2.1 M, so Leduc is 105×/233× below the threshold, not 210×/466×. "10.2× / 15.3× slower" is the ratio of exploitabilities at equal time; to reach a given accuracy, sampling takes about 105×/233× longer. The CFR+ row of the constants table is internally inconsistent. "All four algorithms follow O(1/√T)" is contradicted by the chapter's own data: vanilla CFR's slope is ≈ −0.84 and CFR+'s ≈ −1.7. The alternating-update description is wrong for both the algorithm and the code. (2) The HULHE claims contradict the cited source. The chapter credits full-traversal CFR+ with solving heads-up limit hold'em, then says one full traversal of hold'em "would take longer than the age of the universe" and that MCCFR is "the only tractable approach". Bowling et al. (2015) ran 1,579 full CFR+ iterations of 61 min each and report that CFR+ needed less computation than sampling CFR. (3) All six figures print in English and at 4.9–6.4 pt, and no BG render exists. Figs. 6–9 plot NashConv under the label "Exploitability", and the Kuhn "Custom CFR" curve is not an exploitability at all.
**Counts:** S1 18 · S2 33 · S3 8   (by category: G 6 · B 20 · T 7 · C 17 · S 6 · X 3)

Conventions in this file (as in the pilot): quotes are raw markdown from `summaryBg.md` / `onePagerBg.md` (and `summaryEn.md` / `onePager.md` for EN). Proposals keep the chapter's current " - " dashes and decimal points; those are fixed centrally. Decided centrally and not itemised: 53 " - " dashes in summaryBg (8 in the one-pager); 21 decimal points and 6 "10,200"-style separators in summaryBg (19 and 7 in the one-pager); 79 bold spans against 53 in the EN; and shared footnote labels (F07-X01). Markers 20 (`bowling2015`) and 6 (`suttonbarto2018`) point back into chapters 2 and 1. Footnote 25 (`brown2017`) prints without this chapter's gloss. For external and importance sampling the proposals keep the settled glossary terms ("външно вземане на проби", "извадка по важност"). Page numbers are printed page numbers in the current `allSummaries_bg.pdf`; chapter 3 = PDF pp. 29–41 = printed pp. 28–40.

## G — Figures

### F03-G01 · S1 · Bulgarian captions for all six figures
- **Where:** summaryBg.md, image alt text of figs. 6–11 (printed pp. 33–38). All six captions print in English (known corpus-wide defect). Four of them are half-translated ("Ледюк Poker - …").
- **Now → Proposed** (the file name changes to `_bg` only once F03-G02 has produced the files):
  - "![Ледюк Poker - Exploitability vs Iterations](leduc_exploitability_iterations.png)" → "![Ледюк покер: експлоатируемост (NashConv) спрямо броя на итерациите при четирите решавача на OpenSpiel](leduc_exploitability_iterations_bg.png)"
  - "![Ледюк Poker - Exploitability vs Wall-Clock Time](leduc_exploitability_time.png)" → "![Ледюк покер: експлоатируемост (NashConv) спрямо времето за изпълнение при четирите решавача на OpenSpiel](leduc_exploitability_time_bg.png)"
  - "![Kuhn Poker - Exploitability vs Iterations](kuhn_exploitability_iterations.png)" → "![Кун покер: експлоатируемост (NashConv) спрямо броя на итерациите](kuhn_exploitability_iterations_bg.png)"
  - "![Kuhn Poker - Exploitability vs Wall-Clock Time](kuhn_exploitability_time.png)" → "![Кун покер: експлоатируемост (NashConv) спрямо времето за изпълнение](kuhn_exploitability_time_bg.png)"
  - "![Exploitability vs Iterations](exploitability_vs_iterations.png)" → "![Ледюк покер, собствени реализации с бюджет от 180 s за всеки алгоритъм: експлоатируемост спрямо броя на итерациите](exploitability_vs_iterations_bg.png)"
  - "![Exploitability vs Wall-Clock Time](exploitability_vs_wallclock.png)" → "![Ледюк покер, собствени реализации с бюджет от 180 s за всеки алгоритъм: експлоатируемост спрямо времето за изпълнение](exploitability_vs_wallclock_bg.png)"
- **Fix:** Replace the alt text in `summaryBg.md`. In the EN captions of figs. 6–9, write "NashConv" instead of "Exploitability" (see F03-C07).

### F03-G02 · S1 · All six figures are English in the BG bundle; no BG render exists or can be made as the scripts stand
- **Where:** `deliverables/reports/step03/summary/*.png`. These are copies dated 1 Jul, and there is no `_bg` twin. `summaryBg.md` links the EN files.
- **Problem:** Every label, legend and title is English, and ticks use decimal points. None of the three generating scripts can be re-rendered cheaply:
  - `implementation/step03/exploration/implDayOne1_test.py` (figs. 8–9) and `exploration/leduc_comparison.py` (figs. 6–7) retrain OpenSpiel from scratch on every run, and a Leduc run takes about 30 min.
  - Both write their caches through the cwd-relative `relativePath = "exploration/figures/"`. Under `render_bg_figures.py`, which chdirs into the script folder, the 1 Aug run therefore wrote `exploration/exploration/figures/*_cache.json` and no `_bg` PNG.
  - MCCFR is unseeded, so a re-run plots different data. The nested 1 Aug Kuhn cache has outcome sampling at 0.065, while the printed fig. 8 shows 0.162.
  - `cfr/train_all_timed.py` (figs. 10–11) retrains all four algorithms for 180 s each.
- **Fix:**
  1. In `implDayOne1_test.py` and `leduc_comparison.py`, set `relativePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures") + os.sep`. Add a plot-only path: when `os.environ.get("PLOT_ONLY") == "1"`, load `{kuhn,leduc}_results_cache.json` from `exploration/figures/` (the 1 Jul caches that match the printed figures) and skip training. An environment variable is used because the renderer runs scripts via `runpy`, without arguments.
  2. In `train_all_timed.py`, add the same switch: load `models/timed_all_snapshots.json`, then call `plot_iterations_chart`/`plot_wallclock_chart` only.
  3. Run `PLOT_ONLY=1 python scripts/figures/render_bg_figures.py --only step03`.
  4. Copy the six `*_bg.png` into `deliverables/reports/step03/summary/` and relink `summaryBg.md` (F03-G01).
  5. Delete the stray `implementation/step03/exploration/exploration/`.

### F03-G03 · S1 · Figs. 6–9 (OpenSpiel runs) print at 4.9–5.9 pt and mislabel NashConv as exploitability
- **Where:** `renders/ch03/p034_f1.png`, `p035_f1.png`, `p036_f1.png`, `p037_f1.png`
- **Problem:**
  1. Legibility: all four are saved at `figsize=(14, 7)`, dpi 150 (2100 px) and printed at 17.6 cm, a scale of 0.495. Ticks, axis labels and the `legend(fontsize=10)` print at 4.9 pt; the title (12) at 5.9 pt. The legend in figs. 6 and 8 and the tick labels cannot be read at print size.
  2. The y-axis says "Exploitability (log scale)", but the scripts compute `expl.nash_conv`, which is twice the "exploitability" of figs. 10–11 and of the custom evaluator (`evaluate/exploitability.py`: `(BR₀+BR₁)/2`). The same word therefore means two quantities, a factor 2 apart, on pp. 33–38 (see F03-C07).
  3. The x-axis ends at 3,829 iterations, the last point of `printSteps` (100·1.5ᵏ ≤ 5000), while the text and report say 5,000.
- **Fix:** `leduc_comparison.py`, `implDayOne1_test.py`, both plots:
  - `figsize=(14, 7)` → `(8, 4.5)`, `dpi=150` → `300`
  - `plt.xlabel/ylabel(..., fontsize=11)`, `plt.tick_params(labelsize=10)`, `plt.legend(fontsize=10)`
  - drop `plt.title` (the caption carries it)
  - `ylabel('Exploitability (log scale)')` → `ylabel('NashConv (log scale)')`

  Printed scale becomes 0.866, so fs 10 prints at 8.7 pt. Mapping: new key 'NashConv (log scale)' → 'NashConv (логаритмичен мащаб)'.

### F03-G04 · S2 · Figs. 8–9: the "Custom CFR (Hand-coded)" curve is not an exploitability
- **Where:** `renders/ch03/p036_f1.png`, `p037_f1.png` (the red zig-zag curve)
- **Problem:** `implDayOne1_test.py` computes the curve as `cfr_exploit = abs(avg_game_value - theoretical_value)`: the distance of the running average game value from −1/18. The trainer is step 02's `KuhnTrainer`, which samples one random deal per iteration (chance-sampled, not vanilla). The curve is plotted on the NashConv axis next to four real NashConv curves. That explains the zig-zag, and it cannot be compared with them. Report §4.1 lists it as an exploitability ("Custom CFR (Chapter 02) ~3.5×10⁻⁴").
- **Fix:** In `implDayOne1_test.py`, either delete the custom-CFR block and its two `plt.plot` calls, or compute `expl.nash_conv` on the custom trainer's average strategy (wrap it in a `policy.TabularPolicy`) and label it 'Custom CFR (chance-sampled, step 02)'. Mapping: 'Custom CFR (Hand-coded)' → 'Собствен CFR (извадка от раздаването, глава 2)'. The current 'Персонализиран CFR' means "personalised".

### F03-G05 · S1 · Figs. 10–11 (timed benchmark) print at 6.4 pt; "final exploit 0.0000" for CFR+
- **Where:** `renders/ch03/p039_f1.png`, `p039_f2.png`
- **Problem:**
  1. Legibility: `figsize=(11, 6)`, dpi 150, `bbox_inches="tight"` → 1633 px, printed at 17.6 cm, a scale of 0.636. Ticks, axis labels and legend print at 6.4 pt; the title at 7.6 pt. Effective ppi is 236, which is fine.
  2. Fig. 11 legend: "CFR+ — final exploit 0.0000" (format `:.4f`). It reads as exactly zero, while the text says 2.6×10⁻⁵.
  3. The legend strings are f-strings ("Vanilla CFR — final 3,713 iters"), and the title interpolates the budget. The exact-string BG mapping can never translate them.
- **Fix:** `train_all_timed.py`:
  - `plot_iterations_chart` / `plot_wallclock_chart`: `figsize=(11, 6)` → `(8, 4.4)`; `dpi=150` → `300`; `ax.tick_params(labelsize=10)`; xlabel/ylabel `fontsize=11`; `ax.legend(..., fontsize=10)`; drop `ax.set_title` (the caption carries it).
  - Legend: `label=DISPLAY_NAMES[algo]` (the final values are in the text and in Table 4). If a value is kept, use `f"{ys[-1]:.2g}"`.
  - Mapping, new keys: 'Vanilla CFR' → 'Обикновен CFR', 'MCCFR External' → 'MCCFR, външно вземане на проби', 'MCCFR Outcome' → 'MCCFR, извадка по резултати'.

### F03-G06 · S2 · Mapping entries for step 03 that leave English or mistranslate
- **Where:** `scripts/figures/out/figure_labels.json` (and `FIGURE_LABELS_BG.md`, step03 section)
- **Now → Proposed:**
  - 'Exploitability (log scale)' → 'експлоатируемост (log scale)' ⇒ 'Експлоатируемост (логаритмичен мащаб)'
  - 'Iterations (log scale)' → 'итерации (log scale)' ⇒ 'Итерации (логаритмичен мащаб)'
  - 'Outcome Sampling MCCFR' → 'Извадка по резултати MCCFR' ⇒ 'MCCFR с извадка по резултати'
  - 'Wall Clock Time (seconds, log scale)' → 'Реално време (секунди, логаритмичен мащаб)' ⇒ 'Време за изпълнение (секунди, логаритмичен мащаб)' (T07)
  - 'Wall-Clock Training Time (seconds)' → 'Време за обучение в реално време (секунди)' ⇒ 'Време за обучение (секунди)'
  - 'Wall-clock time (seconds)' → 'реално време (seconds)' ⇒ 'Време за изпълнение (секунди)'
  - 'Exploitability vs Iterations: MCCFR Variants vs Custom CFR' → '…срещу Custom CFR' ⇒ 'Експлоатируемост спрямо итерациите: варианти на MCCFR срещу собствения CFR'
  - 'Exploitability (Nash Conv)' → 'експлоатируемост (Nash Conv)' ⇒ 'NashConv'
- **Why:** "log scale", "seconds" and "Custom CFR" are English. "Извадка по резултати MCCFR" has English word order. The titles become moot if the titles are dropped (G03, G05).

## B — Bulgarian language

### F03-B01 · S1 · English left in the text, tables and formulas
- **Where:** summaryBg.md §§ 3.3, 3.6, 3.7, 3.8, 3.9; onePagerBg.md "**Подход.**"
- **Now → Proposed:**
  - "което гарантира сходимост към същото равновесие на Наш като при Full-Traversal CFR." → see F03-C11 (the new text says "CFR с пълно обхождане")
  - "Глава 2 установи Full-Traversal CFR върху Кун и доказа" → "В Глава 2 беше реализиран CFR с пълно обхождане за Кун и беше показано" (see also F03-C16)
  - "| Вариант | Възли на шанса | Възли на traverser-а | Възли на опонента | Разход на итерация |" → "| Вариант | Възли на случайността | Възли на обхождащия играч | Възли на опонента | Цена на итерация |"
  - "Съжаленията за traverser-а се актуализират въз основа на извадковото поддърво." → "Съжаленията на обхождащия играч се обновяват въз основа на поддървото от извадката."
  - "Извадка от едно действие (ε-on-policy)" → "Извадка от едно действие (ε-микс с текущата стратегия)"
  - "Един ε-on-policy микс (с вероятност ε се избира равномерно; в противен случай се следва текущата стратегия) осигурява разглеждане на всички действия дори когато текущата **политика на работа** им присвоява нулева вероятност." → "Един ε-микс (с вероятност ε действието се избира равномерно, а в противен случай - според текущата стратегия) гарантира, че всички действия се разглеждат, дори когато текущата стратегия им присвоява нулева вероятност."
  - "| MCCFR External | 107 | 19,470 | **0.767** |" → "| MCCFR, външно вземане на проби | 107 | 19,470 | **0.767** |"; "| MCCFR Outcome | 245 | 45,901 | **1.143** |" → "| MCCFR, извадка по резултати | 245 | 45,901 | **1.143** |" (last column: F03-C02)
  - "| No-Limit Texas Холдем |" → "| Тексас холдем без лимит |" (numbers: F03-C06)
  - "$$\frac{99{,}000 \times \text{more iterations needed}}{945 \times \text{faster per iteration}} \approx 105 \times \text{more wall-clock time}$$" → "$$\frac{99{,}000 \times \text{повече итерации}}{945 \times \text{по-бърза итерация}} \approx 105 \times \text{повече време за изпълнение}$$"
  - "$C_w = C / \sqrt{\text{speed}}$" → "$C_w = C / \sqrt{\text{скорост}}$"; "$C_{\text{iter}}$" → "$C_{\text{итер}}$"; "\mathbb{E}_{\text{deal}}" → "\mathbb{E}_{\text{раздаване}}"
  - "$$|N|_{\text{crossover}} = |N|_{\text{Leduc}} \cdot \left(\frac{C_{mc}}{C_v}\right)^2 \cdot \frac{\text{speed}_v}{\text{speed}_{mc}}$$" → "$$|N|_{\text{пресичане}} = |N|_{\text{Ледюк}} \cdot \left(\frac{C_{mc}}{C_v}\right)^2 \cdot \frac{\text{скорост}_v}{\text{скорост}_{mc}}$$"; "| Вариант | $|N|_{\text{crossover}}$ |" → "| Вариант | $|N|_{\text{пресичане}}$ |"
  - onePagerBg: "(всички действия на traverser-а, едно случайно избрано действие на противника)" → "(всички действия на обхождащия играч и едно случайно избрано действие на противника)"
- **Why:** English prose and English words in formulas print on pp. 30, 34, 36–40. "ε-микс" keeps the candidate's own choice of "микс" (Aug comment 78). "политика на работа" is also a meaning error (T02). Cyrillic inside `\text{}`: check the first rebuild, as in the pilot.

### F03-B02 · S1 · meaning — crossover table header: "External victories? / Victories by results?"
- **Where:** summaryBg.md § "Кога MCCFR надделява - точката на пресичане", Table 6
- **EN:** "| Game | $|N|$ | External wins? | Outcome wins? |"
- **Now → Proposed:** "| Игра | $|N|$ | Външни победи? | Победи по резултати? |" → "| Игра | $|N|$ | Печели ли външното вземане на проби? | Печели ли извадката по резултати? |"; in the Leduc row, "твърде малко" → "под прага" (numbers: F03-C01).
- **Why:** "Външни победи" / "Победи по резултати" read as nouns ("external victories", "victories by results"). The column asks whether each sampling variant beats full traversal.

### F03-B03 · S1 · meaning — "политика на работа" for *on-policy*; Aug comment 77 not carried into the one-pager
- **Where:** onePagerBg.md "**Подход.**" (the summary instance is in F03-B01)
- **EN:** "(one root-to-terminal trajectory, `eps = 0.6` on-policy mixture with importance-sampling" [line break] "correction)"
- **Now → Proposed:** "(една корен–краен траектория, `eps = 0.6` политика на работа смес с корекция чрез важностно вземане на проби)" → "(една траектория до край, ε-микс с текущата стратегия при `eps = 0.6` и корекция чрез извадка по важност)"
- **Why:** "политика на работа" means "work policy" (T02). "корен–краен траектория" has no agreement. The candidate's Aug comment 77 ("една траектория до край") was applied in the summary but not here. "важностно вземане на проби" differs from the chapter's "извадка по важност".

### F03-B04 · S1 · meaning — the Nash reference rendered as "our" reference algorithm (cf. F07-B02)
- **Where:** onePagerBg.md "**Връзка с дисертацията.**"
- **EN:** "Nash reference against which every later opponent-modelling, safe-exploitation and LLM number is" (preceded by "and CFR+ becomes the")
- **Now → Proposed:** "а **CFR+** става **наш** референтният алгоритъм, спрямо който всяко по-късно моделиране на противника, **безопасна експлоатация** и число, свързано с **голям езиков модел**, ще бъдат съпоставяни" → "а CFR+ става еталонът за равновесие на Наш, спрямо който ще се съпоставят всички по-късни резултати за моделиране на противника, безопасна експлоатация и големи езикови модели"
- **Why:** "наш референтният алгоритъм" reads as "our the reference algorithm", which is ungrammatical and wrong. It is the same glossary slip as the pilot's "наш противник". "моделиране … ще бъдат съпоставяни" also lacks agreement.

### F03-B05 · S1 · meaning — *breaks even* rendered "reaches equilibrium"
- **Where:** onePagerBg.md "Ключови резултати (измерени)"
- **EN:** "Sampling breaks even at roughly" / "**2.1M nodes** (external) and **4.8M** (outcome)"
- **Now → Proposed:** "Извадката достига равновесие при приблизително **2.1 милиона възела** (външна) и **4.8 милиона** (по резултати)" → "Извадката се изравнява с пълното обхождане при приблизително **1.1 милиона възела** (външна) и **2.4 милиона** (по резултати)"
- **Why:** In a game-theory text, "достига равновесие" means reaching (Nash) equilibrium. The numbers are corrected per F03-C01.

### F03-B06 · S2 · meaning — "averaging of linear strategies" and "moving average"
- **Where:** summaryBg.md § 3.1 list, § 3.5
- **EN:** "linear strategy averaging" / "**Linear strategy averaging.** Vanilla CFR weights every iteration's strategy equally in the running average. CFR+ weights iteration $t$ by $t$ itself:"
- **Now → Proposed:**
  - "усредняване на линейни стратегии и редуващи се актуализации" → "линейно претеглено усредняване на стратегиите и редуващи се актуализации"
  - "**Усредняване на линейни стратегии.** Обикновен вариант на CFR включва стратегията от всяка итерация с еднаква тежест в плъзгащата средна. При CFR+ всяка итерация $t$ се претегля със самата нея, тоест $t$." → "**Линейно претеглено усредняване на стратегиите.** Обикновеният вариант на CFR включва стратегията от всяка итерация с еднакво тегло в текущата средна. При CFR+ стратегията от итерация $t$ получава тегло $t$:"
- **Why:** The strategies are not "linear"; the averaging is linearly weighted (T03). "плъзгаща средна" is a moving (windowed) average, while the running average keeps every iteration. "се претегля със самата нея, тоест $t$" is a calque.

### F03-B07 · S2 · meaning — MCTS backpropagation rendered as neural "error backpropagation"
- **Where:** summaryBg.md § 3.2 list
- **Now → Proposed:** "**Обратно разпространение на грешката** - пропагиране на крайния резултат" → "**Обратно разпространение** - разпространяване на крайния резултат"
- **Why:** In MCTS no error is propagated, only the playout result. The glossary entry is correct for neural networks only; it needs a sense note. "пропагиране" is an anglicism.

### F03-B08 · S2 · grammar — non-word "сходяват" and "се сближава до"
- **Where:** summaryBg.md §§ 3.2, 3.3
- **Now → Proposed:**
  - "Случайните разгръщания, агрегирани в хиляди **итерации**, **сходяват** към точни **стойностни оценки**" → "Случайните разгръщания, обобщени в хиляди итерации, дават все по-точни оценки на стойността" (content: F03-C14)
  - "средната **стойност** на извадените стойности се сближава до истинската очаквана **стойност**" → "средната стойност на извадката клони към истинската очаквана стойност"
- **Why:** "сходяват" is not a Bulgarian verb (cf. "сходява", F07-B03). "се сближава до" mixes "се сближава с" and "клони към".

### F03-B09 · S2 · terminology — variance as "вариация"; two names for *unbiased estimator*
- **Where:** summaryBg.md §§ 3.3, 3.6, 3.7
- **Now → Proposed:**
  - "Този компромис между вариация и скорост е основната тема на тази глава." → "Този компромис между дисперсия и скорост е основната тема на главата."
  - "## Компромисът скорост–вариация" → "## Компромисът между дисперсия и скорост"
  - "**компромисът скорост–вариация** е невидим" → rewritten in F03-C08
  - "**непристрастни оценители**" → "**неизместени оценки**"
- **Why:** The chapter also writes "дисперсия" (6×) and "крива дисперсия–скорост" for the same statistical variance. "Вариация" means variation. The same section later says "неизместени оценки", which is the standard term (glossary: unbiased estimator → неизместена оценка). See T05.

### F03-B10 · S2 · terminology — three names for external sampling in one section
- **Where:** summaryBg.md § 3.6 (Table 3 caption), Tables 4–6 (English names: F03-B01)
- **Now → Proposed:** ": Извадка по външни възли и извадка по резултати: какво взема всеки вариант при всеки тип възел и произтичащата цена на итерация." → ": Външно вземане на проби и извадка по резултати: от какво взема извадка всеки вариант при всеки тип възел и каква е цената на една итерация."
- **Why:** The caption renames the method used in the text and table ("Външно вземане на проби"). "какво взема всеки вариант" is incomplete ("what each variant takes").

### F03-B11 · S2 · occurrences of pilot glossary errors (F07-T13, T12, T06)
- **Where:** summaryBg.md §§ 3.1, 3.7, 3.9
- **Now → Proposed:**
  - "базовата **Нашева стратегия**" → "базовата стратегия на равновесие на Наш" (F07-T13; the whole sentence: F03-X01)
  - "практически точно Нашево равновесие" → "практически точно равновесие на Наш" (F07-T13)
  - "(при еднаква изчислителна мощност кой алгоритъм генерира най-добрата стратегия?)" → "(при еднакви изчислителни разходи кой алгоритъм дава най-добрата стратегия?)" (F07-T12)
  - "Комбинира се с MCCFR, за да направи реалния покер управляем." → "В комбинация с MCCFR прави решаването на реалния покер изчислително постижимо." (F07-T06: "управляем" means controllable)

### F03-B12 · S2 · terminology — *benchmark game* as "еталонен тест"
- **Where:** summaryBg.md §§ 3.1, 3.4
- **Now → Proposed:**
  - "върху междинните **еталонни тестове**, използвани в глави 5–8" → "върху междинните еталонни игри, използвани в глави 5–8"
  - "## Ледюк покер - Разширяване на еталонния тест" → "## Ледюк покер - по-голяма еталонна игра"
  - "Това го прави идеален **еталонен тест**" → "Това го прави идеална еталонна игра"
- **Why:** Leduc is a game, not a test. The curated glossary has "Benchmark game → Еталонна игра". The settled entry "benchmark game → референтна игра" contradicts it and should be aligned. "еталонен тест" stays right for the 180-second benchmark run.

### F03-B13 · S2 · terminology — "марковска свойственост"; heading/text mismatch
- **Where:** summaryBg.md § 3.3
- **Now → Proposed:** "(марковска свойственост)" → "(марковско свойство)"; "## Маркови вериги и законът за големите числа" → "## Марковски вериги и законът за големите числа" (heading content: F03-C11)
- **Why:** The term is "марковско свойство" (T06). The text says "марковски вериги" under a heading that says "Маркови".

### F03-B14 · S2 · typography/calque/content — the ReLU sentence
- **Where:** summaryBg.md § 3.5
- **EN:** "The analogy to ReLU activations in neural networks is direct: both clip negative values to zero, preventing dead units (or dead actions) from requiring a long recovery period."
- **Now → Proposed:** "Аналогията с reLU активациите в невронните мрежи е пряка: и двете ограничават отрицателните стойности до нула, като по този начин предотвратяват мъртви единици (или мъртви действия) да изискват дълъг период на възстановяване." → "Аналогията с активационната функция ReLU в невронните мрежи е пряка: и двете занулават отрицателните стойности." EN: → "The analogy to ReLU activations in neural networks is direct: both clip negative values to zero."
- **Why:** "reLU" is the wrong case. "предотвратяват X да изискват" is an English construction. The second half is also wrong as an analogy: ReLU *causes* dead units (zero gradient for negative input) rather than preventing them. The regret-matching+ point is already made in the sentence before.

### F03-B15 · S2 · grammar — agreement, word order, "със"
- **Where:** summaryBg.md §§ 3.2, 3.4, 3.9
- **Now → Proposed:**
  - "все още решимо точно, но достатъчно голямо, за да станат значими разликите между алгоритмите" → "все още решим точно, но достатъчно голям, за да станат значими разликите между алгоритмите"
  - "се пренася към игра с непълна информация дървета чрез MCCFR." → "се пренася чрез MCCFR към дърветата на игрите с непълна информация."
  - "Три нови качествени характеристики се появяват:" → "Появяват се три качествено нови характеристики:"
  - "## Връзки със глава 2 и бъдещи насоки" → "## Връзки с Глава 2 и бъдещи насоки"
- **Why:** The subject is "Ледюк покер" (masculine). "игра с непълна информация дървета" does not parse. The EN says "qualitatively new". "със" is used only before с/з.

### F03-B16 · S2 · calques and unnatural constructions
- **Where:** summaryBg.md §§ 3.1, 3.2, 3.6, 3.7, 3.8, 3.9
- **Now → Proposed:**
  - "Глава 2 установи работещ обикновен вариант на CFR решавач за Кун покер" → "В Глава 2 беше създаден работещ решавач с обикновения вариант на CFR за Кун покер"
  - "Грациозна: съсредоточава се върху обещаващи разклонения" → "Умерена: съсредоточава се върху обещаващи разклонения"
  - "Подбрани разклонения до терминал" → "Подбрани разклонения до крайно състояние"
  - "детето на корена с най-голям брой посещения" → "дъщерният възел на корена с най-голям брой посещения"
  - "**Извадка по резултати** избутва извадката още по-напред: тегли се една траектория до край." → "**Извадката по резултати** отива още по-далеч: тегли се една-единствена траектория до край."
  - "но извършва извадка от възлите на шанса и възловите състояния на противника" → "но взема извадка във възлите на случайността и във възлите на противника"
  - "Формален 180-секунден еталонен тест с ограничение във времето за изпълнение на всичките четири варианта върху Ледюк прави сравнението в реално време конкретно. Гледна точка, базирана на итерациите (вариантите с извадка завършват милиони обновления, докато вариантите с пълно обхождане - само няколко хиляди):" → "Сравнителен тест с бюджет от 180 секунди за всеки от четирите варианта върху Ледюк прави сравнението по време на изпълнение конкретно. Изглед по итерации (вариантите с извадка извършват милиони обновявания, а вариантите с пълно обхождане - само няколко хиляди):"
  - "Гледна точка в реално време - справедливото сравнение" → "Изглед по време на изпълнение - справедливото сравнение"
  - "Горният модел поставя очевиден въпрос" → "Тази закономерност поставя очевиден въпрос"
  - "(среднопретеглена извадка вместо точна очаквана стойност)" → "(извадкова оценка вместо точна очаквана стойност)"
- **Why:**
  - "установи" means "ascertained". "обикновен вариант на CFR решавач" is a noun pile.
  - *graceful* → "грациозна" is literal.
  - "терминал" is a device, not a terminal state. "дете" is a calque of *child*.
  - "избутва" (shoves) and "възлови състояния" (nodal states) are calques.
  - "модел" misreads *pattern*.
  - "среднопретеглена" (weighted-average) changes the meaning: the EN says a sampled estimator.
  - "в реално време" for wall-clock: see T07.

### F03-B17 · S2 · terminology — *chips* as "чип/чипа" (glossary: жетони; cf. F07-B36)
- **Where:** summaryBg.md § 3.4
- **Now → Proposed:** "Фиксирани (1 чип)" → "Фиксирани (1 жетон)"; "повишаването с 4 чипа във втори кръг" → "повишаването с 4 жетона във втория кръг"

### F03-B18 · S2 · Aug comment 70 not fully applied
- **Where:** summaryBg.md § 3.1. Comment (p. 35 of the Aug build, on "Стъпка 3 п…"): "Глава 3 показва механизмите за преодоляване на проблема"
- **Now → Proposed:** "Глава 3 преодолява проблема с мащаба чрез два взаимнодопълващи се механизма, разработени независимо" → "Глава 3 показва двата взаимно допълващи се механизма за преодоляване на проблема с мащаба, разработени независимо"
- **Why:** "Стъпка" → "Глава" was applied, but the requested wording was not. A chapter presents mechanisms; it does not itself overcome the problem. The other ten chapter-3 comments are applied: 69, 71, 72, 73, 74 (section 3.4 removed), 75, 76, 78, 79 (open questions removed), and 77 in the summary only (F03-B03).

### F03-B19 · S2 · one-pager — calques, stale "стъпки", "loose bound"
- **Where:** onePagerBg.md "**Проблем.**", "Ключови резултати (измерени)"
- **EN:** "being affordable one game up from Kuhn" / "the solver every later chapter depends on" / "*CFR+ is the workhorse, and it is not close.*" / "so the `O(1/sqrt(T))` bound is loose here in a way the bound itself does not predict"
- **Now → Proposed:**
  - "което става недостъпно дори само една игра над Кун" → "което престава да е изчислително поносимо още при следващата по големина игра след Кун"
  - "върху който ще се надграждат всички следващи стъпки" → "върху който се надграждат всички следващи глави"
  - "**CFR+ е работният кон и не е близо до останалите.**" → "**CFR+ е основният инструмент, с категорично предимство.**"
  - "така че границата `O(1/sqrt(T))` тук е по-слаба, отколкото самата граница предвижда" → "така че горната граница `O(1/sqrt(T))` тук далеч не се достига" (content: F03-C04)
- **Why:**
  - "недостъпно … една игра над Кун" is a word-for-word calque.
  - "стъпки" is stale naming (Aug comment 0).
  - "не е близо до останалите" says CFR+ is *far from* the others, which could mean behind. The EN means "the contest is not close".
  - "по-слаба, отколкото самата граница предвижда" is circular.

### F03-B20 · S3 · Aug comment 73 applied, but "в пъти" understates the EN
- **Where:** summaryBg.md § 3.1 — "Всяка итерация е в пъти по-евтина, за сметка на по-шумни актуализации."
- **EN:** "Each iteration is orders of magnitude cheaper"
- **Now → Proposed (optional):** "Всяка итерация е в пъти по-евтина" → "Всяка итерация е стотици до хиляди пъти по-евтина"
- **Why:** The measured ratios are 945× and 2,228×. "в пъти" means "several times". The proposal keeps the candidate's wish to avoid "с порядъци" while keeping the magnitude.

## T — Glossary-level terminology

### F03-T01 · S1 · settled entries whose "translation" is English
- **Where:** `llmPipeline/glossary_settled.md`
- **Now → Proposed:**
  - "traverser → Traverser" ⇒ "обхождащ играч"
  - "full-traversal cfr → Full-Traversal CFR" ⇒ "CFR с пълно обхождане"
  - "ε-on-policy → ε-on-policy" and "ε-on-policy mixture → ε-on-policy mixture" ⇒ "ε-микс с текущата стратегия"
  - "mccfr external sampling → MCCFR External Sampling" ⇒ "MCCFR с външно вземане на проби"
  - "mccfr outcome sampling → MCCFR Outcome Sampling" ⇒ "MCCFR с извадка по резултати"
  - "no-limit texas hold'em → No-Limit Texas Холдем" ⇒ "тексас холдем без лимит"
  - "heads-up no-limit hold'em → Heads-Up No-Limit Холдем" ⇒ "тексас холдем без лимит за двама"
  - "vanilla counterfactual regret minimization → Vanilla Counterfactual Regret Minimization" ⇒ "обикновен вариант на CFR"
- **Why:** These entries are the source of every English fragment in F03-B01. Rule: only algorithm and system names stay in Latin script.

### F03-T02 · S1 · "on-policy → политика на работа"
- **Where:** glossary_settled.md (freq 3); chapter 3 §3.6 and the one-pager (F03-B01, B03)
- **Now → Proposed:** "политика на работа" ⇒ "по текущата политика (on-policy)" in RL. For sampling mixtures, use "по текущата стратегия". Step 01 already writes "работи по текущата политика" for SARSA.
- **Why:** "политика на работа" means "work policy / policy of operation". The meaning is lost everywhere it is inserted.

### F03-T03 · S2 · "linear strategy averaging → усредняване на линейни стратегии"; "running average → плъзгаща средна"
- **Now → Proposed:** ⇒ "линейно претеглено усредняване на стратегиите"; ⇒ "текуща средна" (keep "плъзгаща средна" for *moving average* only)
- **Why:** The first makes the strategies linear. The second names a windowed average. Both recur wherever CFR+ is described (steps 3–5).

### F03-T04 · S2 · "regret flooring → подово ограничаване на съжалението"
- **Now → Proposed:** ⇒ "нулиране на отрицателните съжаления"
- **Why:** "подово" is the floor of a room, a calque of *floor*. The operation is max(R, 0), i.e. resetting negative regrets to zero. Avoid "подрязване/отрязване", which the glossary already uses for *pruning*. Chapter 3 occurrences: § 3.1 "чрез подово ограничаване на съжалението", the § 3.5 heading and bold lead-in, § 3.9 "(подово ограничаване на съжалението + линейно претегляне)", and the one-pager "(подово ограничаване на съжалението, линейно осредняване, редуващи се актуализации)".

### F03-T05 · S2 · compounds that contradict "variance → дисперсия" and "unbiased → неизместен"
- **Now → Proposed:**
  - "variance-for-speed tradeoff → компромис между вариация и скорост" ⇒ "компромис между дисперсия и скорост"
  - "variance-speed tradeoff → компромис скорост–вариация" ⇒ same
  - "low-variance estimator → оценител с ниска вариация" ⇒ "оценка с ниска дисперсия"
  - "unbiased estimation theorem → теорема за непредубедена оценка" ⇒ "теорема за неизместената оценка"
- **Why:** In Bulgarian statistics the terms are "дисперсия" and "неизместена оценка". "вариация" and "непредубедена" are word-for-word. The chapter mixes them (F03-B09).

### F03-T06 · S2 · "markov property → марковска свойственост"
- **Now → Proposed:** ⇒ "марковско свойство"
- **Why:** "свойственост" is not a term. The standard name is "марковско свойство".

### F03-T07 · S2 · "wall-clock time / budget / convergence → реално време"
- **Now → Proposed:** ⇒ "време за изпълнение" (e.g. "бюджет от 180 s време за изпълнение", "изглед по време на изпълнение", $C_w$ "(по време на изпълнение)")
- **Why:** "в реално време" means *real-time*, and the dissertation uses exactly that sense for C1 ("real-time opponent inference"). "Бюджет в реално време от 180 секунди" reads as "a real-time budget", and "сходимост в реално време" as "real-time convergence". Chapter 3 occurrences: § 3.7 (5×), Table 4 header, one-pager "бюджет в реално време", "константа за реално време", and three figure labels (F03-G06).

## C — Content

### F03-C01 · S1 · Crossover arithmetic is off by a factor of two
- **Where:** summaryEn/summaryBg § 3.8 (Tables 5–6 and the paragraph below); onePager/onePagerBg "Key results"; `implementation/step03/convergence_analysis.md` § 7
- **Problem:** With the chapter's own formula and values, 10,200 × (107/0.34)² × 20.6/19,470 = **1.07 M** nodes (external) and 10,200 × (245/0.34)² × 20.6/45,901 = **2.38 M** (outcome). The printed 2.1 M / 4.8 M are what the formula gives with 20,400 (= 2|N|, the nodes one iteration visits for both players). The "210× / 466× too small" then divides by 10,200. The ratio crossover / |N|_Leduc = (C_mc/C_v)²·speed_v/speed_mc = **105 / 233**, whatever unit |N| is counted in. These are exactly the wall-clock penalties the chapter derives in § 3.7 ("≈ 105× more wall-clock time").
- **Now → Proposed (BG):**
  - "| Външно вземане на проби | ~2.1 милиона възела |" → "| Външно вземане на проби | ~1.1 милиона възела |"
  - "| Извадка по резултати | ~4.8 милиона възела |" → "| Извадка по резултати | ~2.4 милиона възела |"
  - "| Ледюк покер | 10,200 | Не (210 пъти твърде малко) | Не (466 пъти твърде малко) |" → "| Ледюк покер | 10,200 | Не (105 пъти под прага) | Не (233 пъти под прага) |"
  - "Ледюк е 210 пъти под прага за външно вземане на проби и 466 пъти под прага за извадка по резултати." → "Ледюк е 105 пъти под прага за външното вземане на проби и 233 пъти под прага за извадката по резултати."
  - onePagerBg: F03-B05, plus "10,200-те възела на Ледюк са **210x / 466x** твърде малко" → "10,200-те възела на Ледюк са **105x / 233x** под прага"
- **Now → Proposed (EN):** "| External Sampling | ~2.1 million nodes |" → "| External Sampling | ~1.1 million nodes |"; "| Outcome Sampling | ~4.8 million nodes |" → "| Outcome Sampling | ~2.4 million nodes |"; "| Leduc Poker | 10,200 | No (210× too small) | No (466× too small) |" → "| Leduc Poker | 10,200 | No (105× too small) | No (233× too small) |"; "Leduc sits 210× below the External Sampling crossover and 466× below the Outcome Sampling crossover." → "Leduc sits 105× below the External Sampling crossover and 233× below the Outcome Sampling crossover."; one-pager (the EN one-pager is hard-wrapped; quote is one line) "**2.1M nodes** (external) and **4.8M** (outcome); Leduc's 10,200 nodes are **210x / 466x** too" → "**1.1M nodes** (external) and **2.4M** (outcome); Leduc's 10,200 nodes are **105x / 233x** too". Correct `convergence_analysis.md` § 7 the same way.

### F03-C02 · S1 · "10.2× / 15.3× slower" is an accuracy ratio, not a time ratio
- **Where:** summaryEn/Bg Table 4, last column; onePager/onePagerBg "*The reason is variance…*"
- **Problem:** With ε(t) = C_w/√t, C_w,mc/C_w,v = 10.2 means that *at equal time* external sampling's exploitability is 10.2× higher. That matches the measured 5.5×10⁻² / 4.4×10⁻³ = 12.5 at 180 s. Reaching a *given* accuracy takes (C_w,mc/C_w,v)² = **105×** (external) and **233×** (outcome) longer, which is the chapter's own formula line under the table. The one-pager states the wrong reading outright: "slower to any given accuracy".
- **Now → Proposed:**
  - BG header: "| Относително към обикновен вариант на CFR |" → "| $C_w$ спрямо обикновения CFR |"; cells "10.2× по-бавен |" → "10.2× (≈105× повече време) |", "15.3× по-бавен |" → "15.3× (≈233× повече време) |"
  - EN: "| Relative to Vanilla |" → "| $C_w$ relative to vanilla |"; "10.2× slower |" → "10.2× (≈105× more time) |"; "15.3× slower |" → "15.3× (≈233× more time) |"
  - onePagerBg: "- извадката е **10.2x / 15.3x** по-бавна за постигане на дадена точност." → "- при еднакво време извадката завършва с **10.2x / 15.3x** по-висока експлоатируемост, т.е. за дадена точност ѝ е нужно **~105x / ~233x** повече време."
  - onePager: "— sampling is **10.2x / 15.3x** slower to any given accuracy." → "— at equal time sampling ends **10.2x / 15.3x** less accurate, so reaching a given accuracy takes **~105x / ~233x** longer."

### F03-C03 · S1 · CFR+ row of the constants table is internally inconsistent
- **Where:** summaryEn/Bg Table 4 — "| CFR+ | 0.34 | 20.6 | **~0.002** | ~38 пъти по-бърз |" / "| CFR+ | 0.34 | 20.6 | **~0.002** | ~38× faster |"
- **Problem:** C_iter = 0.34 is copied from vanilla. With it, C_w = 0.34/√20.6 = 0.075, not 0.002. The "~0.002" is CFR+'s ε√T at T = 3,706 (0.0016), put in the C_w column. CFR+ does not follow C/√T at all: ε√T falls from 0.142 (T = 97) to 0.0016 (T = 3,706) (`implementation/step03/models/timed_cfrplus_snapshots.json`). "~38×" is therefore meaningless.
- **Now → Proposed:** "| CFR+ | 0.34 | 20.6 | **~0.002** | ~38 пъти по-бърз |" → "| CFR+ | – | 20.6 | – | не следва $C/\sqrt{T}$ (вж. текста) |"; EN "| CFR+ | 0.34 | 20.6 | **~0.002** | ~38× faster |" → "| CFR+ | – | 20.6 | – | not $C/\sqrt{T}$ (see text) |"

### F03-C04 · S1 · "The rate is a property of the algorithm family" — contradicted by the chapter's own data
- **Where:** summaryEn/Bg § 3.9 "Convergence rates" (the § 3.7 opening sentence is SOURCE_GAPS row 1: F03-S01)
- **Problem:** Log-log slopes from `models/timed_*_snapshots.json`: external −0.50 and outcome −0.53 (T ≈ 10⁵–3.5×10⁶); vanilla CFR −0.84 (T = 97–3,713, ε√T 0.94 → 0.27); CFR+ −1.74. Only MCCFR follows O(1/√T). O(1/√T) is a worst-case *bound* for all four, not the observed rate. The one-pager's "anomaly" (vanilla beating its bound) is simply a bound that is not tight, which is common. Chapter 2's −0.5 on Kuhn is not a counter-example.
- **Now → Proposed:**
  - BG: "Глава 3 показва, че тази скорост е свойство на цялото семейство алгоритми, а не само на конкретна реализация - единствено емпиричният $O(1/T)$ при CFR+ е по-бърз, но без формално доказателство. MCCFR остава със скорост $O(1/\sqrt{T})$, но с драстично по-голяма константа." → "В Глава 3 се вижда, че $O(1/\sqrt{T})$ е горна граница за цялото семейство, а не наблюдаваната скорост: върху Ледюк двата варианта на MCCFR следват наклон около $-0.5$, обикновеният CFR се сближава по-бързо (около $-0.8$), а CFR+ - значително по-бързо (около $-1.7$), което не е формално доказано. MCCFR остава при скорост $O(1/\sqrt{T})$, но с драстично по-голяма константа."
  - EN: "Chapter 3 shows that this rate is a property of the algorithm family, not of any one implementation — only CFR+'s empirical $O(1/T)$ is faster, and it lacks a formal proof." → "Chapter 3 shows that $O(1/\sqrt{T})$ is the family's upper bound, not its observed rate: on Leduc both MCCFR variants follow a slope of about $-0.5$, vanilla CFR converges faster (about $-0.8$) and CFR+ much faster (about $-1.7$), without a formal proof."

### F03-C05 · S1 · Alternating updates described wrongly; "three changes" are two in the measured comparison
- **Where:** summaryEn/Bg § 3.5 "**Alternating updates.**" and the "~140×" sentence; onePager/Bg "roughly **170x** better, from three localised code changes"; report_en/bg § 3.2
- **Problem:**
  1. In Tammelin's CFR+ (and in `cfrplus_trainer.py`, which follows "Algorithm 1 from Tammelin (2014)"), every iteration updates *both* players in turn: `for traversing_player in (0, 1)`. The second player's update sees the first player's new regrets. Nothing is skipped on odd or even iterations, and the work per iteration is not halved. The measurements confirm it: CFR+ ran 3,706 iterations in 180 s against vanilla's 3,713.
  2. Both baselines already alternate. `cfr_trainer.py` says "Full-traversal vanilla CFR with alternating updates", and OpenSpiel's `CFRSolver` sets `alternating_updates=True` (checked in the installed package). The ~140× and ~170× gaps therefore come from regret-matching+ and linear averaging only.
- **Now → Proposed:**
  - BG: "**Редуващи се актуализации.** Вместо при всяка итерация да се актуализират съжаленията и на двамата играчи, CFR+ актуализира съжаленията на играч 0 при нечетни итерации, а на играч 1 - при четни. Това намалява наполовина изчислителната работа за една итерация и носи малка полза по отношение на сходимостта, като предотвратява едновременните промени в стратегията." → "**Редуващи се актуализации.** Вместо двамата играчи да се обновяват едновременно спрямо един и същ профил от стратегии, CFR+ ги обновява последователно в рамките на всяка итерация, така че обновяването на втория играч вече отчита новата стратегия на първия. Работата за една итерация не се променя; ползата е по-бързата сходимост."
  - EN: "**Alternating updates.** Instead of updating both players' regrets every iteration, CFR+ updates player 0 on odd iterations and player 1 on even iterations. This halves per-iteration work and provides a small convergence benefit by avoiding simultaneous strategy shifts." → "**Alternating updates.** Instead of updating both players simultaneously from the same strategy profile, CFR+ updates them in turn within each iteration, so the second player's update already sees the first player's new strategy. The work per iteration is unchanged; the benefit is faster convergence."
  - onePagerBg: "благодарение на три локализирани промени в кода." → "благодарение на две локализирани промени в кода (нулиране на отрицателните съжаления и линейно усредняване; базовият вариант вече редува актуализациите)."; onePager: "from three localised code changes." → "from two localised code changes (regret flooring and linear averaging; the vanilla baseline already alternates updates)."
  - "~140×" sentence: F03-C07.

### F03-C06 · S2 · Game sizes in the crossover table are wrong for both hold'em rows
- **Where:** summaryEn/Bg Table 6 — "| Тексас холдем с лимит | ~$10^{14}$ | Да ($10^7$ пъти над прага) | Да |", "| No-Limit Texas Холдем | ~$10^{17}$ | Да ($10^{10}$ пъти над прага) | Да |"
- **Problem:** The column is tree nodes |N|. For HULHE, 3.19×10¹⁴ is the number of *information sets*; the game has 3.16×10¹⁷ states (Bowling et al. 2015; Johanson 2013). No-limit hold'em in the ACPC formats has 1.4×10⁵¹ to 6.3×10¹⁶⁴ states (Johanson 2013, arXiv:1302.7008, precise counts in § 4), not 10¹⁷. The verdicts do not change, but the multipliers do. The LHE row's "Yes" is also contradicted by how LHE was actually solved (F03-S02).
- **Now → Proposed:** BG → "| Тексас холдем с лимит (за двама) | ~$3 \times 10^{17}$ | Да по модела (~$10^{11}$ пъти над прага), но е решен с CFR+ с пълно обхождане | Да по модела |" and "| Тексас холдем без лимит | до ~$6 \times 10^{164}$ | Да | Да |"; EN "| Limit Texas Hold'em | ~$10^{14}$ | Yes ($10^7$× above threshold) | Yes |" → "| Heads-up limit Texas Hold'em | ~$3 \times 10^{17}$ | Yes by the model (~$10^{11}$× above), yet solved by full-traversal CFR+ | Yes by the model |"; "| No-Limit Texas Hold'em | ~$10^{17}$ | Yes ($10^{10}$× above threshold) | Yes |" → "| No-Limit Texas Hold'em | up to ~$6 \times 10^{164}$ | Yes | Yes |". Add `[^johanson2013]` (F03-S02).

### F03-C07 · S2 · "5,000 iterations" is 3,829, and two metrics a factor 2 apart are both called "exploitability"
- **Where:** summaryEn/Bg § 3.5 last paragraph; figs. 6–9 (F03-G03); report_en/bg § 4 ("5,000 iterations", "Exploitability @5k")
- **Problem:** The exploration scripts log at `printSteps` = 100·1.5ᵏ ≤ 5000, so the last measurement is at 3,829 (`exploration/figures/leduc_results_cache.json`). They also log OpenSpiel `nash_conv`. The timed benchmark and `compare_openspiel.py` use exploitability = NashConv/2. So "5.4×10⁻⁵" (NashConv at 3,829) and "2.6×10⁻⁵" (exploitability at 3,706) are the same quality of strategy. Both baselines alternate updates (F03-C05).
- **Now → Proposed:**
  - BG: "Емпирично, при Ледюк с 5000 итерации CFR+ достига експлоатируемост ≈ 5.4×10⁻⁵, докато обикновеният вариант на CFR все още е около ~7.6×10⁻³ - подобрение приблизително 140 пъти, постигнато чрез три малки модификации." → "Емпирично, при Ледюк след 3829 итерации реализацията на CFR+ в OpenSpiel достига NashConv ≈ 5.4×10⁻⁵ (експлоатируемост ≈ 2.7×10⁻⁵), докато обикновеният вариант на CFR все още е около 7.6×10⁻³ - подобрение приблизително 140 пъти, постигнато с две от трите модификации (и двата решавача на OpenSpiel редуват актуализациите)."
  - EN: "Empirically, on Leduc at 5,000 iterations CFR+ reaches exploitability ≈ 5.4×10⁻⁵ while vanilla CFR is still at ~7.6×10⁻³ — a ~140× improvement from three small modifications." → "Empirically, on Leduc after 3,829 iterations OpenSpiel's CFR+ reaches NashConv ≈ 5.4×10⁻⁵ (exploitability ≈ 2.7×10⁻⁵) while vanilla CFR is still at 7.6×10⁻³ — a ~140× improvement from two of the three modifications (both OpenSpiel solvers already alternate updates)."
  - Add one defining sentence where exploitability is first used (§ 3.4 or 3.5). BG: "Тук експлоатируемост означава средната печалба на най-добрия отговор срещу двамата играчи, $(BR_0 + BR_1)/2$; NashConv е сумата им, т.е. двойно по-голяма." EN: "Exploitability here is the average best-response gain against the two players, $(BR_0 + BR_1)/2$; NashConv is their sum, i.e. twice as large."
  - Report § 4: "5,000 iterations" → "3,829 iterations (last snapshot of a 5,000-iteration run)"; "Exploitability @5k" → "NashConv @3,829".

### F03-C08 · S2 · Kuhn: "all four reach near-Nash … the trade-off is invisible" — the figures show otherwise
- **Where:** summaryEn/Bg § 3.6, sentence before fig. 8; report_en/bg § 4.1 table
- **Problem:** At the last snapshot (3,829 iterations; `exploration/figures/kuhn_results_cache.json`), the NashConv values are: CFR+ 6.1×10⁻⁵, OpenSpiel CFR 4.2×10⁻⁴, external sampling 1.7×10⁻², outcome sampling 1.6×10⁻¹. Kuhn's uniform strategy is at 0.92, so outcome sampling is not "near-Nash". The ordering is Leduc's, i.e. the trade-off is visible. Report § 4.1's values (CFR 1.5×10⁻³, CFR+ 3.0×10⁻⁴, ES 4×10⁻³, OS 2.5×10⁻²) match neither this cache nor the printed figure. Its "Custom CFR ~3.5×10⁻⁴" is not an exploitability (F03-G04).
- **Now → Proposed:**
  - BG: "Върху 12-те информационни множества на **Кун покер** и четирите алгоритъма (**обикновен вариант на CFR**, **CFR+**, двата варианта на **MCCFR**) достигат **почти равновесие на Наш** за секунди - **компромисът скорост–вариация** е невидим при този **мащаб** и изборът на алгоритъм е по-скоро теоретичен." → "Върху 12-те информационни множества на Кун покер всички алгоритми се изпълняват за секунди, а подредбата им вече е същата като при Ледюк: след 3829 итерации CFR+ достига NashConv ≈ 6×10⁻⁵, обикновеният CFR - ≈ 4×10⁻⁴, а външното вземане на проби и извадката по резултати са едва при ≈ 0.02 и ≈ 0.16."
  - EN: "On Kuhn Poker's 12 information sets, all four algorithms (vanilla CFR, CFR+, both MCCFR variants) reach near-Nash within seconds — the variance-speed tradeoff is invisible at this scale, and the choice of algorithm is academic:" → "On Kuhn Poker's 12 information sets every algorithm runs in seconds, and the ordering is already Leduc's: after 3,829 iterations CFR+ is at NashConv ≈ 6×10⁻⁵ and vanilla CFR at ≈ 4×10⁻⁴, while external and outcome sampling are still at ≈ 0.02 and ≈ 0.16:"
  - Report § 4.1: replace the table with the cache values at 3,829 iterations and drop or relabel the custom-CFR row.

### F03-C09 · S2 · The crossover model rests on three unstated simplifications, each worth an order of magnitude
- **Where:** summaryEn/Bg § 3.8 — "Отговорът се крие във факта, че разходът на итерация при обикновения вариант на CFR нараства линейно с размера на дървото $|N|$, докато този на MCCFR е приблизително постоянен."
- **Problem:**
  1. External sampling's cost per iteration is not constant. Lanctot et al. (2009, § 4, after Thm. 4) give O(√|H|) for balanced games. With that growth, the same measured numbers put the threshold near 10,200 × 105² ≈ 1.1×10⁸ nodes, not 10⁶.
  2. The constants are measured on Leduc only. The CFR and MCCFR regret bounds grow with the number of information sets, so C_v and C_mc need not keep their ratio as the game grows.
  3. Vanilla CFR is modelled as C/√T although its slope is ≈ −0.84 (F03-C04).

  The one-pager's "Open questions" names only the implementation-constant caveat. The summary presents the threshold as a property of the algorithms ("the critical tree size").
- **Now → Proposed:**
  - BG: "докато този на MCCFR е приблизително постоянен." → "докато този на MCCFR расте много по-бавно (при външното вземане на проби - приблизително като $\sqrt{|N|}$[^mccfr])."
  - After the Leduc paragraph, add: "Оценката е от порядъка на величината и важи за тази реализация: константите са измерени само върху Ледюк, обикновеният CFR е моделиран като $C/\sqrt{T}$, въпреки че се сближава по-бързо, а ако цената на итерация на MCCFR расте като $\sqrt{|N|}$, същите данни дават праг около $10^8$ възела."
  - EN: "while MCCFR's is roughly constant." → "while MCCFR's grows far more slowly (roughly as $\sqrt{|N|}$ for external sampling [^mccfr])."; add: "The estimate is an order-of-magnitude figure for this implementation: the constants are measured on Leduc only, vanilla CFR is modelled as $C/\sqrt{T}$ although it converges faster, and if MCCFR's cost per iteration grows as $\sqrt{|N|}$ the same data put the threshold near $10^8$ nodes."

### F03-C10 · S2 · Unsourced variance formula and a wrong attribution of the variance
- **Where:** summaryEn/Bg § 3.7 "Why does the variance exist?"
- **Problem:** "$\propto |N|/|I|$" has no derivation and no source. It is dimensionally inconsistent (a variance in utility² set proportional to a pure number). The chapter's model contradicts it: if variance grew with |N|/|I|, C_mc would not be scale-free. The variance comes from *sampling the chance event*. It arises in any game with chance nodes, hidden information or not. It is a property of the sampling scheme (VR-MCCFR removes most of it with baselines; F03-S06).
- **Now → Proposed:**
  - BG: "$$\mathrm{Var}[\hat{v}_I] = \mathbb{E}_{\text{deal}}\left[(\hat{v}_I - v_I)^2\right] \propto \frac{|N|}{|I|}$$" → "$$\mathrm{Var}[\hat{v}_I] = \mathbb{E}_{\text{раздаване}}\left[(\hat{v}_I - v_I)^2\right]$$"; "- следствие от самата скрита информация, а не недостатък на схемата на извадка:" → "- следствие от извадката на случайното събитие (раздаването), а не от начина на обхождане в рамките на едно раздаване:"
  - EN: drop "\propto \frac{|N|}{|I|}"; "a consequence of the hidden information itself, not a deficiency of the sampling scheme:" → "a consequence of sampling the chance event (the deal) itself, not of how the tree is explored within a deal:"

### F03-C11 · S2 · Unbiasedness does not by itself give "convergence to the same Nash equilibrium"; the LLN/Markov framing misdescribes MCCFR
- **Where:** summaryEn/Bg § 3.3 (heading, the formula paragraph); § 3.6 "Критичното теоретично свойство…"
- **Problem:**
  1. Lanctot et al. (2009) prove unbiasedness in **Lemma 1** (Theorem 1 there is the regret-to-equilibrium link). Convergence then needs their regret bounds, which hold with probability 1 − p and scale with 1/δ, the minimum sampling probability (Thms. 4–5). The limit is *an* approximate equilibrium, not "the same" one as CFR's.
  2. The displayed LLN averages sampled values of a *changing* strategy σᵗ, so there is no fixed $v_I$ to converge to.
  3. MCCFR's samples are independent draws per iteration. The Markov property plays no role in its guarantee.
- **Now → Proposed:**
  - BG § 3.3: "Тези извадени стойности са **непристрастни оценители** - тяхната очаквана стойност съвпада с истинската стойност - което гарантира сходимост към същото равновесие на Наш като при Full-Traversal CFR." → "Тези извадкови стойности са **неизместени оценки** - очакваната им стойност съвпада с истинската. Заедно с ограничение отдолу на вероятностите за извадка това осигурява, с вероятност поне $1-p$, същото намаляване на средното съжаление като $O(1/\sqrt{T})$, както при CFR с пълно обхождане, и следователно сходимост на средната стратегия към приблизително равновесие на Наш[^mccfr]."
  - BG § 3.6: "(Lanctot и др., Теорема 1). Това гарантира сходимост към същото равновесие на Наш като при обикновения вариант на CFR, въпреки шума от извадката." → "(Lanctot и др., лема 1). Заедно с техните граници за съжалението (теореми 4 и 5) това гарантира сходимост към приблизително равновесие на Наш въпреки шума от извадката."
  - EN § 3.3: "The sampled values are **unbiased estimators** — their expected value equals the true value — which guarantees convergence to the same Nash equilibrium as full-traversal CFR." → "The sampled values are **unbiased estimators** — their expected value equals the true value — and, with sampling probabilities bounded away from zero, this gives with probability at least $1-p$ the same $O(1/\sqrt{T})$ decrease of average regret as full-traversal CFR, hence convergence of the average strategy to an approximate Nash equilibrium [^mccfr]."
  - EN § 3.6: "(Lanctot et al., Theorem 1). This guarantees convergence to the same Nash equilibrium as vanilla CFR, despite the sampling noise." → "(Lanctot et al., Lemma 1). Together with their regret bounds (Theorems 4–5), this guarantees convergence to an approximate Nash equilibrium despite the sampling noise."
  - Optional: retitle § 3.3 "Метод Монте Карло и законът за големите числа" and drop the Markov-chain paragraph, or keep it as background with "траектории, изтеглени независимо" instead of "траектории през марковската верига".

### F03-C12 · S2 · Stale forward pointers
- **Where:** summaryEn/Bg § 3.9 "Forward"; onePager "Chapters 7-12"
- **Problem:**
  - The titles do not match the chapters. Chapter 5 is "Neural Networks for Imperfect-Information Games" / "Невронни мрежи за игри с непълна информация". Chapter 6 is "End-to-End Game AI Architectures" / "Архитектури на игрови изкуствен интелект от край до край".
  - Chapter 5 does not say Deep CFR "requires specific variance-reduction techniques (advantage networks, importance-weighted targets)". It says Deep CFR uses *external sampling* with advantage networks and iteration-weighted samples, and that DREAM adds a learned baseline to control the variance of *outcome* sampling (step05 summaryEn l. 152–160).
  - BG "важни целеви стойности с тегла" means "important target values with weights".
  - "Машината Ледюк … през Глава 8" means "the Leduc machine during Chapter 8". The one-pager says the testbed runs through Chapters 7–12.
- **Now → Proposed:**
  - BG: "- **Глава 5 (Невронно равновесие / Deep CFR)**" → "- **Глава 5 (Невронни мрежи за игри с непълна информация)**"
  - BG: "Свойствата на дисперсията, установени тук, обясняват защо Deep CFR изисква специфични техники за намаляване на дисперсията (мрежи за предимство, важни целеви стойности с тегла)." → "Свойствата на дисперсията, установени тук, обясняват защо Deep CFR използва външно вземане на проби и защо неговият наследник DREAM, който преминава към извадка по резултати, добавя обучена базова стойност за намаляване на дисперсията."
  - BG: "- **Глава 6 (Игрови изкуствен интелект от край до край)**" → "- **Глава 6 (Архитектури на игрови изкуствен интелект от край до край)**"
  - BG: "Машината Ледюк, разработена за тази глава, се превръща в еталонна среда през Глава 8." → "Реализацията на Ледюк, разработена за тази глава, остава еталонната среда в следващите глави."
  - EN: "- **Chapter 5 (Neural Equilibrium / Deep CFR)**" → "- **Chapter 5 (Neural Networks for Imperfect-Information Games)**"
  - EN: "The variance properties established here explain why Deep CFR requires specific variance-reduction techniques (advantage networks, importance-weighted targets)." → "The variance properties established here explain why Deep CFR samples externally and why its outcome-sampling successor DREAM adds a learned baseline to control variance."
  - EN: "- **Chapter 6 (End-to-End Game AI)**" → "- **Chapter 6 (End-to-End Game AI Architectures)**"
  - EN: "The Leduc engine built for this chapter becomes the benchmark environment through Chapter 8." → "The Leduc engine built for this chapter remains the benchmark environment in later chapters."

### F03-C13 · S2 · "Multiple orders of magnitude" holds against CFR+ only
- **Where:** summaryEn/Bg § 3.7 last paragraph; onePager/Bg "*MCCFR loses badly…*"; report § 5
- **Problem:** At 180 s, MCCFR is 5.5×10⁻² and 1.0×10⁻¹ against vanilla's 4.4×10⁻³. That is 12× and 23× worse, about one order of magnitude. Against CFR+ (2.6×10⁻⁵) it is 2,100× and 4,000×.
- **Now → Proposed:**
  - BG: "И двата варианта на MCCFR изостават с няколко порядъка при този размер на играта." → "Двата варианта на MCCFR изостават 12–23 пъти от обикновения CFR и три до четири порядъка от CFR+ при този размер на играта."
  - EN: "Both MCCFR variants lag by multiple orders of magnitude on this game size." → "Both MCCFR variants trail vanilla CFR by 12–23× and CFR+ by three to four orders of magnitude on this game size."
  - onePagerBg: "три до четири порядъка по-лошо от пълното обхождане въпреки ~1,000 пъти повече итерации" → "12–23 пъти по-лошо от обикновения CFR и три до четири порядъка по-лошо от CFR+ въпреки ~1,000 пъти повече итерации"
  - onePager (hard-wrapped; the line before ends "three to four orders of magnitude"): "worse than full traversal despite ~1,000x more iterations." → "worse than CFR+ (and 12–23x worse than vanilla CFR) despite ~1,000x more iterations."

### F03-C14 · S3 · MCTS: random rollouts alone do not converge to accurate values
- **Where:** summaryEn § 3.2 "Random rollouts, aggregated over thousands of iterations, converge to accurate value estimates — even without any domain knowledge beyond the game rules." (BG: F03-B08)
- **Problem:** Flat random playouts estimate the value of random play. MCTS converges to the minimax value because the UCB-guided selection concentrates the playouts (UCT; Browne et al. 2012 § 3.3, already cited).
- **Now → Proposed:** EN → "Guided by the selection policy, the playouts, aggregated over thousands of iterations, converge to accurate value estimates — even without any domain knowledge beyond the game rules." The BG proposal in F03-B08 already drops "converge".

### F03-C15 · S3 · Node counts: "58 terminal nodes"; what "10,200" counts
- **Where:** summaryEn/Bg § 3.1 "12 information sets, 58 terminal nodes" / "12 информационни множества, 58 крайни възли"; Table 2 "10,200"
- **Problem:** Checked with OpenSpiel. Kuhn has 58 nodes in total, of which 30 are terminal. Leduc's OpenSpiel tree has 9,457 nodes. The 10,200 is the chapter engine's count per full traversal: 120 deals × 85 nodes, with the first-round nodes repeated for each board card and chance nodes excluded. The Kuhn 58 counts chance nodes, so the two cells of Table 2 are counted differently.
- **Now → Proposed:** "58 крайни възли" → "58 възела (30 от тях крайни)"; EN "58 terminal nodes" → "58 nodes (30 terminal)". Optional footnote to Table 2: "10,200 = 120 раздавания × 85 възела при едно пълно обхождане; в OpenSpiel дървото на Ледюк има 9457 възела."

### F03-C16 · S3 · "Chapter 2 … proved"
- **Where:** summaryEn § 3.9 "Chapter 2 established full-traversal CFR on Kuhn and proved that minimizing regret locally"; BG in F03-B01
- **Problem:** Chapter 2 demonstrated the theorem empirically. The proof is Zinkevich et al. (2007).
- **Now → Proposed:** EN "and proved that" → "and showed that"

### F03-C17 · S2 · CFR+ claim of "1,000 vs ~1,000,000 iterations" is an own extrapolation, stated as a fact
- **Where:** summaryEn/Bg § 3.5 "Combined effect"
- **Problem:** No source, and not measured. From this chapter's run, CFR+ reaches 2.0×10⁻⁴ after 1,113 iterations, and vanilla's measured C (0.27–0.34) gives (C/2.0×10⁻⁴)² ≈ 1.8–2.9 M iterations. The order of magnitude is right, but it is an extrapolation. Tammelin (2014) claims "an order of magnitude or more", not 1000×.
- **Now → Proposed:**
  - BG: "С 1000 итерации CFR+ постига резултат, за който на обикновения вариант на CFR са необходими около 1,000,000 итерации." → "При Ледюк CFR+ достига 2.0×10⁻⁴ след около 1100 итерации; при измерената скорост на обикновения вариант на CFR за същата стойност биха били нужни от порядъка на два милиона итерации (екстраполация)."
  - EN: "CFR+ with 1,000 iterations achieves what vanilla CFR needs ~1,000,000 iterations for." → "On Leduc, CFR+ reaches 2.0×10⁻⁴ after about 1,100 iterations; at vanilla CFR's measured rate the same value would take on the order of two million iterations (extrapolated)."

## S — Sources

### F03-S01 · S1 · SOURCE_GAPS row 1: "Всички четири алгоритъма демонстрират $O(1/\sqrt{T})$ сходимост…" → correct and cite
- **Where:** summaryBg.md § 3.7 opening — "Всички четири алгоритъма демонстрират $O(1/\sqrt{T})$ сходимост, но стойностите на константите им се различават съществено. При изразяване на експлоатируемостта като $\epsilon(T) = C / \sqrt{T}$ и преобразуването ѝ в реално време чрез $C_w = C / \sqrt{\text{speed}}$:"
- **Proposal (correct + cite):** The claim is true as a statement about worst-case *bounds* and false as a statement about the measured rates (F03-C04).
  - BG → "И четирите алгоритъма имат гарантирана горна граница на експлоатируемостта от порядъка $O(1/\sqrt{T})$ - за CFR[^zinkevich2007], за MCCFR с вероятност поне $1-p$[^mccfr] и за CFR+[^tammelin2015][^burch2019]. Измерената скорост обаче се различава: двата варианта на MCCFR следват наклон около $-0.5$, обикновеният CFR - около $-0.8$, а CFR+ - около $-1.7$. Затова моделът $\epsilon(T) = C / \sqrt{T}$ по-долу е приближение (при обикновения CFR произведението $\epsilon\sqrt{T}$ намалява от 0.94 до 0.27), а за CFR+ не е приложим. Преобразуването към време за изпълнение става чрез $C_w = C / \sqrt{\text{скорост}}$:"
  - EN "All four algorithms follow $O(1/\sqrt{T})$ convergence, but the constants differ enormously. Writing exploitability as $\epsilon(T) = C / \sqrt{T}$, and converting to wall-clock via $C_w = C / \sqrt{\text{speed}}$:" → "All four algorithms have a guaranteed $O(1/\sqrt{T})$ upper bound on exploitability — CFR [^zinkevich2007], MCCFR with probability at least $1-p$ [^mccfr], and CFR+ [^tammelin2015][^burch2019]. Their measured rates differ: both MCCFR variants follow a slope of about $-0.5$, vanilla CFR about $-0.8$ and CFR+ about $-1.7$. The model $\epsilon(T) = C/\sqrt{T}$ below is therefore an approximation (for vanilla CFR, $\epsilon\sqrt{T}$ falls from 0.94 to 0.27) and does not apply to CFR+. Converting to wall-clock via $C_w = C/\sqrt{\text{speed}}$:"
  - New footnotes:
    - `[^zinkevich2007]: Zinkevich, M., Johanson, M., Bowling, M. & Piccione, C. (2007). "Regret Minimization in Games with Incomplete Information." *Advances in Neural Information Processing Systems 20*.`
    - `[^tammelin2015]: Tammelin, O., Burch, N., Johanson, M. & Bowling, M. (2015). "Solving Heads-Up Limit Texas Hold'em." *Proc. IJCAI*, 645–652.`
    - `[^burch2019]: Burch, N., Moravčík, M. & Schmid, M. (2019). "Revisiting CFR+ and Alternating Updates." *Journal of Artificial Intelligence Research*, 64, 429–443. DOI 10.1613/jair.1.11370.`
- **Verified:**
  - Zinkevich: NeurIPS proceedings listing and PDF. The bound Δ|I|√|A|/√T is quoted as "[1, Theorem 4]" in Lanctot et al. (2009).
  - Lanctot: Theorems 4–5 read in the NeurIPS PDF.
  - IJCAI 2015: abstract page, which says the paper proves "the theoretical soundness of CFR+ and its component algorithm, regret-matching+". Start page 645 checked there; the end page 652 was not checked.
  - Burch et al.: Crossref and JAIR abstract ("an error in one step of the proof … updated proofs to recover the original bound").
  - Slopes: `implementation/step03/models/timed_*_snapshots.json`.

### F03-S02 · S1 · SOURCE_GAPS row 2: "дори една итерация на пълно обхождане на холдем би отнела повече време от възрастта на Вселената" → false for limit hold'em; correct and cite
- **Where:** summaryBg.md § 3.8 — "При реални мащаби на покера заключението се обръща напълно - дори една итерация на пълно обхождане на холдем би отнела повече време от възрастта на Вселената. В такъв мащаб MCCFR (с разширения за намаляване на дисперсията) е **единственият** приложим подход."; also § 3.1 "Това е единственият осъществим подход за игри, при които пълното обхождане е физически невъзможно."
- **Problem:** The chapter's own § 3.1 and its footnote [^bowling2015] say CFR+ solved HULHE. Bowling et al. (2015, full text): "CFR+ does exhaustive iterations over the entire game tree". The computation ran "1579 iterations, taking 68.5 days … 900 core-years", with "61 minutes on average to complete one iteration". The authors "have empirically observed CFR+ to require considerably less computation … than state-of-the-art sampling CFR". So for limit hold'em a full traversal took an hour, and it was the method that won. The "age of the universe" claim holds only for no-limit (up to 6.31×10¹⁶⁴ states, Johanson 2013). Abstraction (Chapter 4) is the other route there, so "the only" is an overclaim too.
- **Proposal (correct + cite):**
  - BG → "При реалните мащаби на покера заключението се обръща, но не навсякъде. Тексас холдем с лимит за двама ($3.16 \times 10^{17}$ състояния) все пак е решен с CFR+ с пълно обхождане - 1579 итерации по около 61 минути на 4800 процесорни ядра[^bowling2015] - като авторите отчитат, че CFR+ изисква значително по-малко изчисления от вариантите на CFR с извадка. Тексас холдем без лимит (до $6.31 \times 10^{164}$ състояния във форматите на ACPC[^johanson2013]) е недостижим за пълно обхождане; там практическият път е извадката - MCCFR в комбинация с абстракция и с разширения за намаляване на дисперсията[^schmid2019]."
  - BG § 3.1: "Това е единственият осъществим подход за игри, при които пълното обхождане е физически невъзможно." → "Това е основният подход за игри, при които пълното обхождане е физически невъзможно; другият - абстракцията на играта - е предмет на Глава 4."
  - EN "At real poker scales the conclusion reverses completely — even one full-traversal iteration of Hold'em would take longer than the age of the universe. At that scale, MCCFR (with variance-reduction extensions) becomes the **only** tractable approach." → "At real poker scales the conclusion reverses, though not uniformly. Heads-up limit hold'em ($3.16 \times 10^{17}$ states) was still solved by full-traversal CFR+ — 1,579 iterations of about 61 minutes each on 4,800 cores [^bowling2015] — and its authors report CFR+ needing considerably less computation than sampling CFR. No-limit hold'em (up to $6.31 \times 10^{164}$ states in the ACPC formats [^johanson2013]) is beyond any full traversal; there sampling — MCCFR combined with abstraction and variance-reduction extensions [^schmid2019] — is the practical route."
  - New footnote: `[^johanson2013]: Johanson, M. (2013). "Measuring the Size of Large No-Limit Poker Games." arXiv:1302.7008.`
  - `[^schmid2019]` is in F03-S06.
- **Verified:** Bowling et al. full-text PDF (webdocs.cs.ualberta.ca/~bowling/papers/15science.pdf), all quotes above; Crossref DOI 10.1126/science.1259433. Johanson: arXiv PDF text. The HULHE counts are 3.162×10¹⁷ states / 3.194×10¹⁴ infosets; ACPC 2009–13 no-limit has 6.31×10¹⁶⁴ states / 6.37×10¹⁶¹ infosets; the smallest ACPC no-limit game has 1.38×10⁵¹ states.

### F03-S03 · S2 · The origin of the name "Monte Carlo" is misattributed (not in SOURCE_GAPS)
- **Where:** summaryBg.md § 3.3 — "Наименованието произхожда от проекта „Манхатън“, където Станислав Улам и Джон фон Нойман прилагат **случайна извадка** за симулиране на дифузията на неутрони - проблем, твърде сложен за аналитично решаване."
- **Problem:** The method was conceived by Ulam at Los Alamos in 1946 and developed with von Neumann and Metropolis for neutron-diffusion calculations. The *name* comes from the Monte Carlo casino and was suggested by Metropolis.
- **Proposal (correct + cite):**
  - BG → "Методът е създаден в Лос Аламос през 1946 г., където Станислав Улам и Джон фон Нойман го прилагат за симулиране на дифузията на неутрони - задача, твърде сложна за аналитично решаване; наименованието, предложено от Никълъс Метрополис, идва от казиното в Монте Карло[^metropolis1987]."
  - EN "The name originates from the Manhattan Project, where Stanislaw Ulam and John von Neumann used random sampling to simulate neutron diffusion — a problem too complex for analytical solution." → "The method was devised at Los Alamos in 1946, where Stanislaw Ulam and John von Neumann used random sampling to simulate neutron diffusion — a problem too complex for analytical solution; the name, suggested by Nicholas Metropolis, refers to the Monte Carlo casino [^metropolis1987]."
  - Footnote: `[^metropolis1987]: Metropolis, N. (1987). "The Beginning of the Monte Carlo Method." *Los Alamos Science*, 15, 125ff. The first publication is Metropolis, N. & Ulam, S. (1949). "The Monte Carlo Method." *JASA*, 44(247), 335–341.`
- **Verified:** Metropolis & Ulam via Crossref (DOI 10.1080/01621459.1949.10483310). Metropolis 1987 by web search: the LANL history pages give the title, issue and start page, the 1946 conception and the naming anecdote. The 1987 article itself was not read.

### F03-S04 · S2 · "Tammelin et al. give the algorithm but not a convergence theorem" — a theorem exists
- **Where:** summaryBg.md § 3.5 — "Забележка: макар че скоростта $O(1/T)$ се наблюдава последователно, тя няма формално доказателство - Tammelin и др. представят алгоритъма, но не и теорема за сходимост, съответстваща на наблюдавана скорост."
- **Problem:** The cited Tammelin (2014) has a single author, so "Tammelin et al." misnames it. Tammelin et al. (2015) do prove convergence (O(1/√T)), and Burch et al. (2019) corrected that proof. What is unproven is the observed ~1/T rate.
- **Proposal (correct + cite):**
  - BG → "Забележка: скоростта $O(1/T)$ се наблюдава последователно, но не е доказана; доказана е само общата за семейството горна граница $O(1/\sqrt{T})$[^tammelin2015], чието първоначално доказателство е коригирано от Burch и др.[^burch2019]"
  - EN "Note: while the $O(1/T)$ rate is consistently observed, it lacks a formal proof — Tammelin et al. give the algorithm but not a convergence theorem matching the observed rate." → "Note: the $O(1/T)$ rate is consistently observed but unproven; what is proven is the family-wide $O(1/\sqrt{T})$ bound [^tammelin2015], whose original proof was corrected by Burch et al. [^burch2019]."
- **Verified:** as in F03-S01. The Tammelin (2014) arXiv abstract has no theorem.

### F03-S05 · S3 · Footnote spot-check
- `mccfr`: correct paper and authors (NeurIPS 2009 page and PDF). The in-text "Теорема 1" should be "лема 1" (F03-C11). The ε = 0.6 in the one-pager is the paper's own setting ("ϵ = 0.6 worked well across all games") and could be credited to it. Pages 1078–1086 not checked.
- `bowling2015` (EN and BG, shared with ch. 2): "the first non-trivial imperfect-information game to be essentially solved" drops the qualifier in the paper ("no nontrivial imperfect-information game played competitively by humans has previously been solved"). Change EN "— the first non-trivial imperfect-information game to be essentially solved." → "— the first non-trivial imperfect-information game played competitively by humans to be essentially solved.". Change BG "- първата нетривиална игра с непълна информация, която по същество е решена." → "- първата нетривиална игра с непълна информация, играна състезателно от хора, която по същество е решена.". Add DOI 10.1126/science.1259433 (Crossref). Note that Bowling et al. used the *current* CFR+ strategy, not the average ("instead using the players' current strategies as the CFR+ solution"). § 3.9's "Both still output the **average** strategy" is therefore not true of that landmark run.
- `browne2012`: correct (Crossref, 10 authors, IEEE TCIAIG 4(1):1–43, DOI 10.1109/TCIAIG.2012.2186810).
- `cfrplus`: correct (arXiv:1407.5042, single author, 18 Jul 2014).
- `southey2005`: correct for Leduc's origin. Add "arXiv:1207.1411" (verified in the pilot).
- `brown2017`: correct paper. It prints without this chapter's gloss (F07-X01, central).

### F03-S06 · S3 · Unsourced "variance-reduction extensions"; CFR+ presented as the end of the line
- **Where:** summaryBg.md § 3.8 "MCCFR (с разширения за намаляване на дисперсията)"
- **Proposal (cite):**
  - `[^schmid2019]: Schmid, M., Burch, N., Lanctot, M., Moravčík, M., Kadlec, R. & Bowling, M. (2019). "Variance Reduction in Monte Carlo Counterfactual Regret Minimization (VR-MCCFR) for Extensive Form Games Using Baselines." *Proc. AAAI*, 33(01), 2157–2164.` Verified: Crossref and arXiv abstract: "an order of magnitude speedup … allows for the first time CFR+ to be used with sampling".
  - Optional, in § 3.5: "A later variant, discounted CFR, outperforms CFR+ in every game tested[^brown2019dcfr]." (BG: "По-късен вариант - CFR с отстъпка (discounted CFR) - превъзхожда CFR+ във всички изпробвани игри[^brown2019dcfr].") `[^brown2019dcfr]: Brown, N. & Sandholm, T. (2019). "Solving Imperfect-Information Games via Discounted Regret Minimization." *Proc. AAAI*, 33(01), 1829–1836.` Verified: Crossref and arXiv:1809.04040 abstract.

## X — Structure

### F03-X01 · S2 · § 3.1 names MCCFR as the thesis's Nash solver; the chapter's own result and the one-pager name CFR+
- **Where:** summaryBg.md § 3.1 — "За дисертацията MCCFR е алгоритъмът, който изчислява базовата **Нашева стратегия** - опорната точка „играй на сигурно“, от която адаптивният агент се отклонява въз основа на наблюденията върху опонента (Принос №1)."; EN "For the thesis, MCCFR is the algorithm that computes the baseline Nash strategy"
- **Problem:** § 3.7 shows CFR+ winning on Leduc by 3–4 orders of magnitude. The one-pager says "CFR+ becomes the Nash reference". The opening paragraph therefore contradicts the chapter's conclusion.
- **Now → Proposed:**
  - BG: "За дисертацията MCCFR е алгоритъмът, който изчислява базовата **Нашева стратегия**" → "За дисертацията тези решавачи изчисляват базовата стратегия на равновесие на Наш"; append after "(Принос №1)": "В игрите с размера на Кун и Ледюк това е CFR+ (вж. раздел 3.7), а MCCFR става необходим при по-големите игри."
  - EN: "For the thesis, MCCFR is the algorithm that computes the baseline Nash strategy" → "For the thesis, these solvers compute the baseline Nash strategy"; append after "(Contribution #1)": "On games of Kuhn and Leduc size that is CFR+ (see the timed benchmark below); MCCFR becomes necessary on larger games."

### F03-X02 · S3 · Figs. 6–7 and 10–11 show the same comparison twice, on different scales
- **Where:** pp. 33–34 (OpenSpiel, NashConv, 3,829 iterations) and p. 38 (custom, NashConv/2, 180 s)
- **Fix:** Keep figs. 10–11, which carry the chapter's numbers, and drop figs. 6–7. Or keep figs. 6–7 only as the OpenSpiel cross-check, captioned as such (F03-G01) and with the NashConv axis (F03-G03). Figs. 8–9 (Kuhn) earn their place only with the rewritten Kuhn sentence (F03-C08).

### F03-X03 · S3 · Tables 1, 3, 4 and 6: the first column wraps to 3–4 lines
- **Where:** pp. 29–30, 34, 36–37, 39. Examples: "Външно / вземане / на / проби" and "No-Limit / Texas / Холдем". Table 1 runs over 1.5 pages.
- **Fix:** Widen the first column's dash count:
  - Table 1: "|----------|--------------|------|" → "|-----------|-------------|-----------|"
  - Table 3: "|---------|-----------------|-----------------------|--------------------|------------------:|" → "|-----------------|-------------|-------------|-------------|------------:|"
  - Table 4: "|-----------|------------------:|---------------:|-------------------:|--------------------:|" → "|------------------|-------:|---------:|---------:|-------------:|"
  - Table 6: "|------|------:|:--------------:|:-------------:|" → "|--------------|------:|:------------:|:------------:|"
