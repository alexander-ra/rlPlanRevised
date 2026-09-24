# Step 07 — final review

**Summary:** The chapter's substance is sound and well sourced, but three things matter most. (1) The Bulgarian text is uneven: §7.1, §7.2 and §7.5, and the BG one-pager, still contain meaning errors a reader will notice — "наш противник" (our opponent) for the Nash opponent, "задното тегло" for posterior weight, "безопасност–изследване" (exploration) for safety–exploitation, first-person verbs ("да рандомизирам", "оптимално отговарям"), English left in formulas and in the one-pager ("Kuhn противници", "губи от Nash"). Several of these come from settled glossary entries, so they will recur in other chapters (see T). (2) All seven figures fail at print size: labels print at 5–7.6 pt against 10.9 pt body text; fig. 35 labels "paper" as "статия" (a journal article) and has overlapping labels; fig. 36 is entirely English; figs. 31 and 37 have colliding notes. (3) Numbers: the non-stationarity table and its "single seed" caveat are stale (the report and the results JSON use 5 seeds with different means), and "statistically indistinguishable from the ceiling on every type" is false for 3 of 19 types.
**Counts:** S1 22 · S2 55 · S3 7   (by category: G 9 · B 43 · T 14 · C 6 · S 8 · X 4)

Conventions in this file: quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md` (including `**`, `*`, `$`), so read this file as source, not rendered. Proposals keep the chapter's current " - " dashes and decimal points; those are fixed centrally (F07-B41, F07-B42). "EN" quotes come from `summaryEn.md` / `onePager.md`. Printed sizes below are computed as matplotlib size × (17.6 cm print width ÷ saved image width); body text in the bundle is 10.9 pt, so the 75 % threshold is ≈ 8.2 pt.

## G — Figures

### F07-G01 · S1 · Bulgarian captions for all seven figures
- **Where:** summaryBg.md, image alt text of figs. 31–37 (bundle pp. 132–147). All seven captions print in English (known corpus-wide defect); the fig. 31 alt text also says "Step 7 / Step 8".
- **Now → Proposed:**
  - "![The safety-exploitation dial: pure equilibrium play is unexploitable but blind; a hard best response extracts the most value but is maximally risky. Opponent modeling operates in between. Step 7 builds the sensor (the model); Step 8 builds the actuator (safe exploitation).]" → "![Скалата безопасност–експлоатация: чистата равновесна игра е неексплоатируема, но „сляпа“; чистият най-добър отговор извлича най-голяма стойност, но носи най-голям риск. Моделирането на противника действа между двете крайности. Глава 7 изгражда сензора (модела), а Глава 8 изгражда изпълнителния механизъм (безопасната експлоатация).]"
  - "![The opponent-modeling loop: a prior belief is multiplied by the likelihood of each observed action to give a posterior, which drives a best response; the outcome feeds the next observation.]" → "![Цикълът на моделиране на противника: априорното убеждение се умножава по правдоподобието на всяко наблюдавано действие и дава апостериорното разпределение, спрямо което се изчислява най-добрият отговор; резултатът от раздаването захранва следващото наблюдение.]"
  - "![Partial observability: a showdown reveals the opponent's private card, pinning the action to one situation; a fold hides it, forcing the model to spread the evidence across every hand the opponent might have held.]" → "![Частична наблюдаемост: при разкриване картата на противника става видима и действието се свързва с една-единствена ситуация; при пас картата остава скрита и моделът трябва да разпредели наблюдението между всички карти, които противникът би могъл да държи.]"
  - "![Three models on one interface: a discrete belief over types, a free-form per-situation count, and a globally-consistent sequence-form estimate - all emit a predicted opponent strategy consumed by the same best-response step.]" → "![Три модела с общ интерфейс: дискретно убеждение върху типове, свободно преброяване по ситуации и глобално съгласувана оценка в последователна форма; и трите връщат прогноза за стратегията на противника, която постъпва в една и съща стъпка за най-добър отговор.]"
  - "![Why fitting the mean can miss the truth: the modeler can only ever produce points in the shaded hull of its samples. A true strategy outside the hull is unreachable; even one inside is abandoned as the posterior collapses onto a single vertex.]" → "![Защо напасването към средната стойност може да пропусне истината: моделът може да породи само точки в оцветената обвивка на своите извадки. Истинска стратегия извън обвивката е недостижима, а дори такава вътре в нея бива изоставена, защото апостериорното разпределение се свива към един-единствен връх.]"
  - "![Exploitation against each Ледюк opponent: the type-based model (which fits these opponents) hugs the exact best-response ceiling, while the continuous model tracks close but sits below for the hardest-to-fit types - and dips below the safe baseline against Nash.]" → "![Експлоатация срещу всеки противник в Ледюк: типово базираният модел (който описва точно тези противници) следва плътно точния таван на най-добрия отговор, а непрекъснатият модел остава близо, но под тавана при най-трудните за напасване типове и пада под безопасната базова стойност срещу „Наш“.]"
  - "![The adaptive exploitation loop: observe, update the model, best-respond (blended toward Nash for safety), and act; a change-point detector can reset the model when the opponent's style shifts.]" → "![Цикълът на адаптивна експлоатация: наблюдение, обновяване на модела, най-добър отговор (смесен с равновесието на Наш за безопасност) и действие; детекторът на точки на промяна може да нулира модела, когато противникът смени стила си.]"
- **Fix:** replace the alt text in `summaryBg.md` (the `](file.png)` part stays; for fig. 36 also see F07-G07).

### F07-G02 · S1 · Fig. 31 spectrum: colliding notes, wrong "Труден", first person, stale "Стъпка", too small
- **Where:** `renders/ch07/p132_f1.png` — caption "The safety-exploitation dial…"
- **Problem:**
  1. The two bottom notes run into each other: "…(модела)Стъпка 8 изгражда…" — both are centred at y = 0.6 (x = 3.6 and 10.4) and the BG strings are longer than the gap. Both also say "Стъпка" (stale naming).
  2. "Труден най-добър отговор" — *hard* translated as *difficult*; meaning is "pure/strict".
  3. First person in the note: "извличам стойност … ограничавам колко експлоатируем позволявам да стана".
  4. "БЕЗОПАСНОСТ" is upper case, "експлоатация" lower case (the EN has both in capitals; the dictionary entry lower-cased it).
  5. "Наш / GTO" — GTO is an undefined English abbreviation, used nowhere in the text.
  6. Legibility: box text 8.6–8.8 → prints 7.4–7.6 pt; notes 8.0–8.2 → 6.9–7.1 pt (scale 0.863).
  7. Overflow (central fix): right box "Труден най-добър отговор / (макс. стойност, макс. риск)"; left box "Наш / GTO (неексплоатируем, сляп)" touches both edges.
- **Fix:** `make_spectrum_figure.py`: labels "Step 7 builds…"/"Step 8 builds…" → "Chapter 7 builds the SENSOR (the model)" / "Chapter 8 builds the ACTUATOR (safe exploitation)", and stack them: `note(ax, 7.0, 0.85, …)` and `note(ax, 7.0, 0.35, …)` instead of x = 3.6 / 10.4 at y = 0.6; all `box` fs → 10, all `note` fs → 10. Mapping (`figure_labels.json`): 'Hard best response\n(max value, max risk)' → 'Чист най-добър отговор\n(макс. стойност, макс. риск)'; 'opponent modeling lives here: …' → 'тук действа моделирането на противника: стойност се извлича от обосновани преценки,\nа собствената експлоатируемост се ограничава'; 'EXPLOITATION' → 'ЕКСПЛОАТАЦИЯ' (shared with step08 `make_dial_figure.py`); 'Nash / GTO\n(unexploitable, blind)' → 'Равновесие на Наш\n(неексплоатируемо, сляпо)'; new keys 'Глава 7 изгражда СЕНЗОРА (модела)', 'Глава 8 изгражда ИЗПЪЛНИТЕЛНИЯ МЕХАНИЗЪМ (безопасната експлоатация)'.

### F07-G03 · S1 · Fig. 32 Bayes loop: literal "\н", overflow into neighbouring box, first person, too small
- **Where:** `renders/ch07/p134_f1.png` — caption "The opponent-modeling loop…"
- **Problem:**
  1. "Предварително\нубеждение" (known literal escape).
  2. "Апостериорно разпределение" (bold) overflows its box, runs over the arrow and hides the first letters of "Най-добър отговор" in the next box.
  3. First person: "отговарям на средната стойност апостериори".
  4. "Вероятност на наблюдаваното действие" — likelihood is "правдоподобие" (the one-pager already uses it); the formula note says "предварително" where the rest of the figure pairs with "апостериорно".
  5. Mood mix: "Наблюдава …" (3rd person) next to "Действай в ръката" (imperative).
  6. Legibility: notes 7.4–7.6 → 6.4–6.5 pt; boxes 8.6–9.0 → 7.4–7.8 pt; formula 9.0 → 7.8 pt (scale 0.861).
  7. Overflow: prior, likelihood, posterior, best-response and observe boxes.
- **Fix:** `make_bayes_loop_figure.py`: all `box` fs → 10, `note` fs 7.4/7.6/9.0 → 10. Mapping: 'Prior belief\nover strategy' → 'Априорно убеждение\nза стратегията'; 'Posterior belief' → 'Апостериорно\nубеждение'; 'Best response' → 'Най-добър\nотговор' (key used only here); 'Likelihood of\nobserved action' → 'Правдоподобие на\nнаблюдаваното действие'; 'respond to the\nposterior mean' → 'най-добър отговор на\nапостериорното средно'; 'Observe opponent\naction (or showdown)' → 'Наблюдение на действието\nна противника (или разкриване)'; 'Act in the hand' → 'Действие в раздаването'; 'posterior  ∝  prior  ×  P(action | strategy)' → 'апостериорно ∝ априорно × P(действие | стратегия)'.

### F07-G04 · S1 · Fig. 33 partial observability: English "BET", "сделка", "кредит", stale "Q-бетинг", too small
- **Where:** `renders/ch07/p137_f1.png` — caption "Partial observability…"
- **Problem:**
  1. English in the BG figure: "Наблюдавано: BET, след това пас".
  2. Printed box reads "Q-бетинг"; the mapping already says 'залог с Q', so the BG render is stale (see F07-G09).
  3. Meaning: "Кредит ЕДНА ситуация" (*credit* read as a noun, "a loan") and "разпредели доказателствата върху всяка съгласувана сделка" (*deal* = a business transaction; imperative mood).
  4. Panel title "Пас: само ефект" but the text says "Пас - само следствие".
  5. Legibility: notes 7.6 → 6.7 pt; small boxes 7.8 → 6.8 pt; other boxes 8.2–9.0 → 7.2–7.9 pt (scale 0.877).
  6. Overflow: "Наблюдавано: BET, след това пас", "Карта скрита: J? Q? K?".
  7. (S3, optional) Cards appear as J/Q/K while the text uses Вале/Дама/Поп.
- **Fix:** `make_partial_obs_figure.py`: all fs → 10; boxes h1–h3 width 1.7 → 1.85. Mapping: 'Observed: BET, then fold' → 'Наблюдавано: ЗАЛОГ, после пас'; 'credit ONE situation\n(bet with K)' → 'приписва се на ЕДНА ситуация\n(залог с K)'; 'spread evidence over every consistent deal' → 'наблюдението се разпределя между всички съвместими раздавания'; 'Fold: effect only' → 'Пас: само следствие'. Optional: J/Q/K → В/Д/П in the six card labels. Re-render.

### F07-G05 · S1 · Fig. 34 three models: gender-agreement errors, stale render, too small
- **Where:** `renders/ch07/p138_f1.png` — caption "Three models on one interface…"
- **Problem:**
  1. Grammar: "един валиден глобален стратегия (изпъкнал)" (стратегия is feminine).
  2. Printed "Наблюдавано раздавания" (agreement error) and "един и същи интерфейс: наблюдения -> стратегия" differ from the current mapping, so the render is stale. The current mapping entry is itself wrong: 'приемам наблюдения -> излъчвам стратегия' (first person; "излъчвам" = broadcast).
  3. "Базиран на типове" vs glossary "Типово базиран"; "бройки" is colloquial; "принципен/скъп" is a calque of *principled*.
  4. Legibility: boxes 8.6–9.0 → 7.3–7.6 pt; notes 7.8–8.0 → 6.6–6.8 pt (scale 0.847).
  5. Overflow: type-based box, consistent box.
- **Fix:** `make_three_models_figure.py`: all fs → 10; in the source string "consume observations -> emit a strategy" replace "->" by "→". Mapping: 'Consistent\none valid global strategy (convex)' → 'Съгласуван\nедна валидна глобална стратегия (изпъкнала задача)'; 'same interface: consume observations -> emit a strategy' → 'общ интерфейс: наблюдения → стратегия'; 'Type-based\nbelief over a few known types' → 'Типово базиран\nубеждение върху няколко известни типа'; 'Continuous\nper-situation counts, smoothed' → 'Непрекъснат\nизгладени честоти по ситуации'; 'fast/fragile  →  robust/data-hungry  →  principled/costly' → 'бърз, но крехък  →  устойчив, но иска много данни  →  строго обоснован, но скъп'. Re-render.

### F07-G06 · S1 · Fig. 35 convex hull: "статия" for paper, overlapping labels, prints at 5–7 pt
- **Where:** `renders/ch07/p140_f1.png` — caption "Why fitting the mean can miss the truth…"
- **Problem:**
  1. Meaning: the RPS vertex *paper* is labelled "статия" (a journal article) in both panels.
  2. Illegible: in the right panel "убеждението се срива до един връх" is printed on top of the true-σ* dot, the arrow and the "истинска σ* (1/3, 1/3, 1/3)" label (the EN figure has the same overlap). In the left panel "обвивка на извадките" sits on the hull edge and a sample dot.
  3. Size: saved from figsize (11.0, 5.1) at dpi 200 (2183 px) and printed at 17.6 cm, so the scale is 0.634. Vertex labels 9 → 5.7 pt, titles 10.5 → 6.7 pt, annotations 8.0–8.2 → 5.1–5.2 pt.
  4. (S3) Not faithful to the source it illustrates: the right-panel samples (0.6,0.25,0.15), (0.2,0.6,0.2), (0.25,0.2,0.55) average to (0.35, 0.35, 0.30), not to the centre the text describes. Ganzfried (2025, Prop. 2) uses s1 = (0.2,0.4,0.4), s2 = (0.6,0.3,0.1), s3 = (0.2,0.3,0.5), and the posterior collapses onto s1. The left-panel third sample in the paper is (0.2,0.3,0.5), not (0.45,0.2,0.35).
- **Fix:** mapping 'paper' → 'хартия'. `make_consistency_figure.py`: figsize (11.0, 5.1) → (8.0, 4.0), dpi 200 → 300; vertex labels 9 → 10.5; titles 10.5 → 11; σ*/hull/collapse labels 8.0/8.2 → 10. Right panel: truth label to `ax.text(truth[0] + 0.12, truth[1], …, ha="left", va="center")`; the collapse label below the triangle as a single line, `ax.text(1.0, -0.38, "belief collapses to one vertex", ha="center", …)`, with `ax.set_ylim(-0.55, 2.1)`. Left panel: hull label above the hull (y = max sample y + 0.12). Optional: the paper's sample values, with the arrow pointing to s1. Mapping titles (optional polish): 'Истината е извън обвивката на извадките:\nнедостижима за всяко осредняване', 'Истината е вътре в обвивката:\nапостериорното разпределение пак се свива към една извадка'.

### F07-G07 · S1 · Fig. 36 Leduc exploitation: entirely English, 5.6 pt legend, undefined types
- **Where:** `renders/ch07/p145_f1.png` — caption "Exploitation against each Ледюк opponent…"; `summaryBg.md` links `../figures/impl_exploitation_leduc.png` (the EN file).
- **Problem:**
  1. Everything is English in the BG bundle: the title "Exploitation vs opponent type (leduc, scale)", the legend "BR ceiling (exact)", "Nash EV (exact)", "type_based", "continuous", the y-label "hero mean profit / hand", CamelCase code names on the x-axis, and decimal points. Cause: `implementation/step07/implementation/plotting.py` is listed in `plotting_scripts()` but has no `__main__`, so `render_bg_figures.py` runs it and gets nothing. The figure is a byte-identical copy of `plots/exploitation_leduc.png` written by `tournament.py`.
  2. Legibility: 1188 px at 120 dpi (figsize 9.9×5) printed at 17.6 cm, scale 0.70. Legend 8 → 5.6 pt; tick and axis labels 10 → 7.0 pt; 172 effective ppi (soft).
  3. The figure shows 9 types; the text defines 4 and the table shows 5. LoosePassive, Random, Level2 and Level3 are never introduced (see F07-X04). The title leaks the run config "(leduc, scale)".
  4. The current mapping entry 'Nash EV (exact)' → 'Нашева очаквана стойност (exact)' would leave "exact" in English even after a BG render.
- **Fix:** `plotting.py`: add `if __name__ == "__main__":` that loads `results/leduc_scale.json` and calls `plot_exploitation(result, "../../../deliverables/reports/step07/figures/impl_exploitation_leduc.png")` (the renderer chdirs to the script folder and writes the `_bg` twin). In `plot_exploitation`: figsize → (8, 4.4); dpi 120 → 300; `ax.legend(fontsize=10)`; `ax.tick_params(labelsize=10)`; ylabel fontsize 11; drop `set_title` (the caption carries it). Optionally plot only the five types of the text table. Mapping, new keys (the legend and tick strings come from the results JSON and are not in the mapping yet): 'type_based' → 'типово базиран', 'continuous' → 'непрекъснат', and the type names below; existing keys: 'BR ceiling (exact)' → 'таван на най-добрия отговор (точен)', 'Nash EV (exact)' → 'очаквана стойност при Наш (точна)', 'hero mean profit / hand' → 'средна печалба на агента / раздаване', and the type names CallingStation → Пасивен играч, Maniac → Маниак, Rock → Камък, LoosePassive → Разпуснат-пасивен, Nash → Наш, Random → Случаен, Level1/2/3 → Ниво 1/2/3. In `summaryBg.md`: "(../figures/impl_exploitation_leduc.png)" → "(../figures/impl_exploitation_leduc_bg.png)".

### F07-G08 · S1 · Fig. 37 adaptive loop: overlapping notes, "изстрели", agreement error, first person
- **Where:** `renders/ch07/p147_f1.png` — caption "The adaptive exploitation loop…"
- **Problem:**
  1. The two bottom notes overlap and are unreadable: "изстрели при смяна на с[тил]реакцията е толкова важна…". Both sit at y = 0.5 (x = 5.0 and 8.5).
  2. Meaning: "изстрели" means gunshots (a noun); *fires* here means "is triggered".
  3. Agreement: "Най-добър отговор смесена към Наш".
  4. First person in the top note: "повтарям всяка ръка; периодично преизчислявам…".
  5. Mood mix: "Наблюдава раздаване" / "Обновяване на модела" / "Действие".
  6. Legibility: notes 7.4–7.8 → 6.3–6.6 pt; boxes 8.4–9.0 → 7.1–7.6 pt (scale 0.847).
  7. Overflow: observe, update and reset boxes.
- **Fix:** `make_exploiter_loop_figure.py`: `note(ax, 5.0, 0.5, …)` → `note(ax, 5.0, 0.62, …)` and `note(ax, 8.5, 0.5, …)` → `note(ax, 8.5, 0.18, …)` (two rows); all fs → 10. Mapping: 'fires on a style shift' → 'задейства се при смяна на стила'; 'Best response\nblended toward Nash' → 'Най-добър отговор,\nсмесен с Наш'; 'repeat every hand; periodically rebuild the best response' → 'повтаря се при всяко раздаване; най-добрият отговор периодично се преизчислява'; 'Observe hand' → 'Наблюдение\nна раздаването'; 'Reset model +\ndrop to safe play' → 'Нулиране на модела +\nбезопасна игра'.

### F07-G09 · S2 · Stale BG renders, and a legibility floor the central overflow fix must respect
- **Where:** `deliverables/reports/step07/summary/*_bg.png` (all six written 1 Aug 13:08) vs `scripts/figures/out/figure_labels.json` (1 Aug 19:50).
- **Problem:** The printed figures predate the mapping, which is why "Q-бетинг", "Наблюдавано раздавания" and the old interface note still print (figs. 33, 34). Separately, at `shrink=1.7` and 17.6 cm print width, one matplotlib point prints as 0.85–0.88 pt, so 8.2 pt on paper needs fs ≥ 9.6. Every step-07 diagram uses 7.4–9.5. An auto-fit that *shrinks* text to fit the boxes would make all six diagrams less legible still.
- **Fix:** After the mapping fixes, run `python scripts/figures/render_bg_figures.py --only step07` and rebuild. In the central overflow fix, wrap the text or enlarge the box rather than shrink the font below fs 9.6. Raise `note()`'s default fs 7.6 → 10 in `_diagram_utils.py`: notes sit outside boxes, so this cannot cause overflow.

## B — Bulgarian language

### F07-B01 · S1 · grammar — first-person verbs in impersonal/2nd-person text
- **Where:** summaryBg.md § "Защо е необходимо моделиране на противника"; § "Връзки и бъдещи насоки"; onePagerBg.md "**Подход.**"
- **EN:** "The safe strategy is to randomize evenly and break even forever." / "Two things make this the whole step in miniature: you must **infer** the bias … if you **over-commit** to paper you become predictable" / "bounding how far you deviate from equilibrium by how much your read has earned" / "observe -> model -> best-respond -> act loop"
- **Now → Proposed:**
  - "Най-ясният начин да се види стойността е чрез картина „камък-ножица-хартия“." → "Стойността се вижда най-ясно в примера с „камък-ножица-хартия“."
  - "Безопасната стратегия е да **рандомизирам** равномерно и да **изравнявам** резултата завинаги." → "Безопасната стратегия е да избирате трите хода с равни вероятности и така завинаги да излизате на нула."
  - "Две неща правят тази глава цяла в миниатюра: трябва да **изведа** пристрастието от шумен поток от хвърляния (няколко не са достатъчни) и ако се **ангажирам прекалено** с хартия, ставате предвидими и те ви смазват с ножица." → "Този пример съдържа цялата глава в умален вид по две причини: пристрастието трябва да се **изведе** от шумен поток от хвърляния (няколко хвърляния не стигат), а ако **заложите прекалено много** на хартията, ставате предвидими и противникът ви смазва с ножица."
  - "като ограничава доколко се отклонявам от равновесие според това колко е заслужено прочетеното" → "като ограничава отклонението от равновесието според това доколко е обоснована преценката за противника"
  - onePagerBg: "изпълнява цикъла наблюдавай → моделирай → оптимално отговарям → действай" → "изпълнява цикъла наблюдение → моделиране → най-добър отговор → действие"
- **Why:** "рандомизирам", "изведа", "ангажирам", "отклонявам", "отговарям" are first-person singular: glossary citation forms pasted verbatim (T03). "Две неща правят тази глава цяла в миниатюра" does not parse. "картина" is a calque of *picture*.

### F07-B02 · S1 · meaning — the Nash opponent rendered as "our" opponent; five names for one type
- **Where:** summaryBg.md §§ 7.1, 7.2, 7.6, 7.7, 7.8
- **EN:** "Against a Nash opponent the gap is essentially **zero**" / "Against the Nash opponent every model earns…" / type name "**Nash**"
- **Now → Proposed:**
  - "Срещу наш противник разликата е по същество **нула**" → "Срещу противник, който играе равновесие на Наш, разликата е по същество **нула**"
  - "Срещу нашов противник всеки модел" → "Срещу противника „Наш“ всеки модел"
  - "(Малките отрицателни Нашеви стойности са" → "(Малките отрицателни стойности при равновесие на Наш са"
  - "| Равновесие на Наш (равновесна игра) |" → "| „Наш“ (равновесна игра) |"
  - "| **Наш равновесие** |" → "| **„Наш“** |"
  - "твърдо се ангажира с **Нашево равновесие**" → "твърдо се ангажира с типа **„Наш“**"
  - "срещу истинско равновесие на Наш противник" → "срещу противник, който наистина играе равновесие на Наш"
  - "| **Нашево равновесие** |" (2×, Kuhn and Leduc tables) → "| **„Наш“** |"
  - "*губи* от Нашево равновесие" → "*губи* срещу „Наш“"
  - "ограничаване на отклонението от Нашево равновесие чрез собствената увереност на модела" → "ограничаване на отклонението от равновесието на Наш според увереността на самия модел"
  - "(по избор смесена към Наш равновесие за безопасност)" → "(по избор смесена с равновесието на Наш за безопасност)"
- **Why:** "наш противник" reads as "our opponent" and "нашов" is not a word. Rule: the opponent *type* is „Наш“, in quotes like „камък“ and „маниак“; the *concept* is "равновесие на Наш" (glossary). The remaining two occurrences are in F07-B31.

### F07-B03 · S1 · grammar/calque — § 7.2 "Второ…" paragraph and the non-word "сходява"
- **Where:** summaryBg.md § "Защо дирихле и защо ви е нужна само средната стойност"; § "Три модела с единен интерфейс"
- **EN:** "Second — and this is the single most reused result in the area — to choose an optimal response you never need the whole posterior … responding to the mean is payoff-optimal but, as it turns out, can fail to *converge* to the opponent's true strategy…"
- **Now → Proposed:**
  - "Второ - и това е единственият най-често използван резултат в областта - за да изберете **оптимален отговор**, никога не е необходимо цялото **апостериорно разпределение** върху стратегиите; достатъчна е само неговата **средна стойност**. Вашата **очаквана печалба** срещу *разпределение* на стратегиите на опонента е равна на вашата **печалба** срещу единствената осреднена стратегия. Това свежда **неразрешим** интеграл върху **пространството на стратегиите** до „**оптимално отговарям** на един осреднен опонент“ и именно това прави **байесовата експлоатация** практична. (Раздел 5 се връща към това: отговарянето на средната стойност е **оптимален по отношение на изплащането**, но, както се оказва, може да не *сходява* към **истинската стратегия** на опонента - тънкостта, която работата от 2025 г. разрешава.)" → "Второ - и това е най-често използваният резултат в областта - за да се избере оптималният отговор, не е нужно цялото апостериорно разпределение върху стратегиите; достатъчна е само неговата **средна стойност**. Очакваната печалба срещу *разпределение* от стратегии на опонента е равна на печалбата срещу единствената осреднена стратегия. Това свежда изчислително непосилен интеграл върху пространството на стратегиите до задачата „най-добър отговор на един осреднен опонент“ и именно това прави байесовата експлоатация приложима на практика. (Раздел 5 се връща към това: отговорът на средната стойност е оптимален по отношение на печалбата, но, както ще се окаже, оценката може да не *клони* към истинската стратегия на опонента - тънкост, която работата от 2025 г. разрешава.)"
  - "и да се сходява към съгласуваната оценка при натрупването на доказателства" → "и постепенно да се приближава към съгласуваната оценка с натрупването на наблюдения"
- **Why:** "сходява" is not a Bulgarian verb. "единственият най-често използван" is a calque. "отговарянето … е оптимален" breaks gender agreement. "оптимално отговарям" is first person. "неразрешим" means undecidable (T06). "изплащане" deviates from the glossary (payoff → печалба). The eight bold spans are not bold in the EN.

### F07-B04 · S1 · meaning — "задното" for posterior
- **Where:** summaryBg.md § "Недостатъкът: напасването към **средна стойност**…" and § "Решението: изпъкнала програмираща задача…"
- **EN:** "the posterior weight on the single best-fitting sample" / "maximizing the log-posterior"
- **Now → Proposed:**
  - "задното тегло върху единствената най-добре пасваща извадка" → "апостериорното тегло на единствената най-добре пасваща извадка"
  - "максимизирането на **логаритъма на задната вероятност**" → "максимизирането на **логаритъма на апостериорната вероятност**"
- **Why:** "задно тегло" / "задна вероятност" means *rear* weight or probability, a literal calque of *posterior*. The chapter uses "апостериорно" everywhere else.

### F07-B05 · S1 · meaning — "exploitation" rendered as "exploration"
- **Where:** summaryBg.md § "Връзки и бъдещи насоки" — "крайните точки на спектъра безопасност–изследване"
- **EN:** "the two are the endpoints of the safety-exploitation spectrum"
- **Now → Proposed:** "крайните точки на спектъра безопасност–изследване" → "крайните точки на спектъра безопасност–експлоатация"
- **Why:** "изследване" means exploration (or research). The error comes from the settled glossary (T01).

### F07-B06 · S1 · meaning — call rendered as raise
- **Where:** summaryBg.md § "Адаптиране към промяна - нестационарни опоненти"
- **EN:** "unleashed on a maniac who calls everything"
- **Now → Proposed:** "пусната срещу маниак, който вдига всичко" → "пусната срещу маниак, който плаща всеки залог"
- **Why:** "вдига" means *raises*, a different poker action. The point of the sentence is that a bluff-heavy strategy loses against someone who *calls*.

### F07-B07 · S1 · meaning — definition of opponent modeling says "exploit the model"
- **Where:** summaryBg.md § "Защо е необходимо моделиране на противника"
- **EN:** "**deviating from Nash to exploit the pattern** — bluffing more against someone who folds too much, value-betting thinner against someone who calls too much."
- **Now → Proposed:** "**отклонение от равновесие на Наш с цел експлоатиране на модела** - блъфиране повече срещу някой, който се отказва твърде често, залагане за стойност по-тънко срещу някой, който плаща твърде често" → "**отклонение от равновесието на Наш, за да се използва забелязаната закономерност** - повече блъфове срещу някой, който се отказва твърде често, и залози за стойност с по-слаби ръце срещу някой, който плаща твърде често"
- **Why:** In this chapter "модел" is the *opponent model*; "exploit the model" says something different from "exploit the pattern". "залагане за стойност по-тънко" is a poker-slang calque.

### F07-B08 · S1 · English left — formulas, a footnote, the one-pager
- **Where:** summaryBg.md §§ 7.2, 7.5, footnote `ganzfried2016`; onePagerBg.md "Ключови резултати (измерени)"
- **Now → Proposed:**
  - "$$\text{belief about their strategy} \;\to\; \text{see an action} \;\to\; \text{update belief} \;\to\; \text{best-respond} \;\to\; \text{repeat.}$$" → a plain centred line (no math): "убеждение за стратегията → наблюдавано действие → обновяване на убеждението → най-добър отговор → повторение."
  - "\text{posterior} \propto" → "\text{апостериорно} \propto"
  - "\xrightarrow{\text{normalize}}" → "\xrightarrow{\text{нормализиране}}"
  - "\qquad \text{s.t.}\quad Fy = f" → "\qquad \text{при}\quad Fy = f"
  - "(Theorem 2.1: respond to the posterior mean.)" → "(Теорема 2.1: печалбата срещу средната стойност на апостериорното разпределение е равна на печалбата срещу цялото разпределение.)"
  - onePagerBg: "срещу експлоатируеми Kuhn противници; разликата спрямо Nash противник е ~0" → "срещу експлоатируеми противници в Кун; срещу противника „Наш“ разликата е ~0"
  - onePagerBg: "**губи от Nash (-0.175 спрямо таван от -0.083)**" → "**губи срещу „Наш“ (-0.175 при таван -0.083)**"
  - onePagerBg: "възстановява Kuhn стратегиите точно (TV ~0.004–0.021)" → "възстановява точно стратегиите в Кун (разстояние по обща вариация ~0.004–0.021)"
  - onePagerBg "(Kuhn: -0.116 -> +0.226)" → see F07-C01.
- **Why:** English prose in the BG bundle; all of it prints (pp. 132, 134, 140). Cyrillic inside `\text{}` has no precedent in the corpus, so check the first rebuild. The pseudocode block can stay English as code.

### F07-B09 · S1 · meaning — one-pager "Саморазкриването"
- **Where:** onePagerBg.md "**Връзка с дисертацията.**" — "Саморазкриването на Нашево равновесие в непрекъснатия модел е емпиричното обосноваване за този предпазен механизъм"
- **EN:** "The continuous model's Nash self-leak is the empirical case for that safety mechanism"
- **Now → Proposed:** "Саморазкриването на Нашево равновесие в непрекъснатия модел е емпиричното обосноваване за този предпазен механизъм" → "Самонанесената уязвимост на непрекъснатия модел срещу противника „Наш“ е емпиричният аргумент за този предпазен механизъм"
- **Why:** "саморазкриване" means self-disclosure. The sentence says the Nash equilibrium reveals itself, which is not the finding.

### F07-B10 · S1 · meaning — one-pager "при над 300 семена … доведе"
- **Where:** onePagerBg.md — "при над 300 семена грешен тип доведе след ръка 100 в ~13% от изпълненията"
- **EN:** "over 300 seeds a wrong type led past hand 100 in ~13% of runs"
- **Now → Proposed:** "при над 300 семена грешен тип доведе след ръка 100 в ~13% от изпълненията" → "в 300 изпълнения с различни начални числа грешен тип все още водеше след раздаване 100 в ~13% от тях"
- **Why:** "при над 300" means "at more than 300" (*over* here means "across"). "доведе" means "brought", not "was leading". "семена" deviates from the glossary (F07-B19).

### F07-B11 · S2 · meaning — "препратки" for references; "познатост"
- **Where:** summaryBg.md, chapter intro; onePagerBg.md "**Подход.**"
- **EN:** "no prior familiarity with the project's code is assumed … bounded, wherever possible, by *exact* analytical references rather than simulated ones"
- **Now → Proposed:**
  - "без предварителна познатост с програмния код на проекта" → "без предварително познаване на програмния код на проекта"
  - "са ограничени чрез *точни* аналитични препратки вместо симулирани такива" → "са поставени в *точни* аналитични граници, а не в симулирани"
  - onePagerBg: "така че всеки резултат е ограничен от точни аналитични препратки" → "така че всеки резултат е поставен в точни аналитични граници"
- **Why:** "препратка" means a cross-reference. The meaning is the reference values between which each result is placed (Nash EV and ceiling). "познатост" is not standard Bulgarian.

### F07-B12 · S2 · meaning — why equilibrium never adapts
- **Where:** summaryBg.md § 7.1 — "тъй като именно липсата на адаптация е основната ѝ характеристика"
- **EN:** "It never adapts, because adaptation is exactly what it was designed not to need."
- **Now → Proposed:** "Тя никога не се адаптира, тъй като именно липсата на адаптация е основната ѝ характеристика." → "Тя никога не се адаптира, защото е създадена именно така, че да не се нуждае от адаптация."
- **Why:** The BG is circular ("it does not adapt because not adapting is its feature"). It loses the design point the EN makes.

### F07-B13 · S2 · meaning — "еднопосочна"
- **Where:** summaryBg.md § 7.1 — "Второ, **експлоатацията е еднопосочна**"
- **EN:** "Second, **exploitation is directional**"
- **Now → Proposed:** "**експлоатацията е еднопосочна**" → "**експлоатацията зависи от вида на слабостта**"
- **Why:** "еднопосочна" means one-way. The point is that the best response leans in the direction of the opponent's specific leak (it bluffs more against a rock).

### F07-B14 · S2 · terminology — "Байсовото" and "доказателство" for evidence
- **Where:** summaryBg.md §§ 7.2, 7.3
- **EN:** "The Bayesian Core — belief, evidence, response"; "two evidential categories"; "spreads the evidence across them"
- **Now → Proposed:**
  - "## Байсовото ядро - убеждение, доказателство и реакция" → "## Байесовото ядро - убеждение, наблюдения и реакция"
  - "всяка ръка попада в една от двете доказателствени категории" → "всяка ръка попада в една от двете категории според това какво разкрива"
  - "и разпределя доказателствата между тях" → "и разпределя наблюдението между тях"
- **Why:** "Байсов" is a misspelling (glossary and chapter: "байесов"). In statistics *evidence* is data or observations; "доказателство" means proof, which is the opposite of what an ambiguous observation gives. One more occurrence is rewritten in F07-C04.

### F07-B15 · S2 · terminology — Dirichlet lower-case, prior/multinomial
- **Where:** summaryBg.md §§ 7.2, 7.4, 7.5
- **EN:** "the natural prior is the **Dirichlet** distribution, because it is the *conjugate* prior of the multinomial…"
- **Now → Proposed:**
  - "### Защо дирихле и защо ви е нужна само средната стойност" → "### Защо Дирихле и защо е нужна само средната стойност"
  - "естественото предварително убеждение е **дирихле** разпределението, защото то е *спрегнатото* предварително убеждение на **мултиномиалната**: актуализирането на дирихле с наблюдавани броеве води до друго дирихле разпределение, при което броевете просто се **добавят** към **псевдоброевете** на предварителното убеждение." → "естественото априорно разпределение е **разпределението на Дирихле**, защото то е *спрегнатото* априорно разпределение за мултиномиалното разпределение: обновяването на разпределение на Дирихле с наблюдаваните броеве дава отново разпределение на Дирихле, в което броевете просто се **добавят** към псевдоброевете на априорното разпределение."
  - "изгладено с дирихле предварително разпределение" → "изгладено с априорно разпределение на Дирихле"
  - "Поставянето на **дирихле предварително разпределение** върху теглата" → "Поставянето на **априорно разпределение на Дирихле** върху теглата"
- **Why:** Dirichlet is a proper name. The glossary has "Дирихле", and the chapter itself uses the capital in § 7.4. "на мултиномиалната" is a dangling adjective with no noun. Conjugate prior → "спрегнато априорно разпределение" (T04).

### F07-B16 · S2 · terminology — § 7.5.2 optimization vocabulary
- **Where:** summaryBg.md § "Решението: изпъкнала програмираща задача в последователна форма" and § 7.5.3
- **EN:** "The fix: a convex program…"; "The remedy reformulates…"; "a single, well-behaved optimization"; "The legal strategies"; "a sum of realization weights"; "so it is a **convex** problem"; "A standard **projected gradient** scheme"; "warm-starting each solve from the last, caching the per-hand terms"; "is a per-update convex solve fast enough"
- **Now → Proposed:**
  - "### Решението: изпъкнала програмираща задача в последователна форма" → "### Решението: задача на изпъкналата оптимизация в последователна форма"
  - "Лекарството преформулира оценката" → "Подходът преформулира оценката"
  - "на една единствена, добре дефинирана оптимизация" → "на една-единствена оптимизационна задача с добри свойства"
  - "Законните стратегии тогава са именно тези" → "Допустимите стратегии тогава са точно тези"
  - "сума от реализации на тегла върху това съгласувано множество" → "сума от реализационните тегла върху това съгласувано множество"
  - "така че това е **изпъкнал** проблем без **локални оптимуми**" → "така че това е **изпъкнала** задача без **локални оптимуми**"
  - "Достатъчен е стандартен **проектиран градиентен метод**" → "Достатъчен е стандартен **градиентен метод с проекция**"
  - "*достатъчно ли бързо е конвексното решаване при всяка актуализация за игра в реално време?*" → "*достатъчно бързо ли е решаването на изпъкналата задача при всяка актуализация за игра в реално време?*"
  - "(топло стартиране на всяко решаване от последното и кеширане на термините за всяко раздаване)" → "(всяко решаване да започва от предишното решение, а членовете за отделните раздавания да се кешират)"
- **Why:** "Лекарство" (medicine) and "законни" (lawful) are calques. "добре дефинирана" changes the meaning (*well-behaved* is not *well-defined*). "реализации на тегла" says "realizations of weights". "проектиран" reads as "designed" (T10). "конвексно" clashes with "изпъкнал" used everywhere else. "термини" are terminology words; the per-hand *terms* of a sum are "членове".

### F07-B17 · S2 · terminology — total-variation distance
- **Where:** summaryBg.md § 7.5.3 — "разстоянието по вариация е приблизително **0.004 до 0.021**"
- **EN:** "total-variation distance roughly **0.004 to 0.021**"
- **Now → Proposed:** "разстоянието по вариация е приблизително" → "разстоянието по обща вариация е приблизително"
- **Why:** The glossary entry is "разстояние по обща вариация". Without "обща" the name refers to no metric.

### F07-B18 · S2 · terminology — "несъответствие" for inconsistency
- **Where:** summaryBg.md § 7.6 — "Това е различен провал от несъответствието"
- **EN:** "It is a different failure from inconsistency"
- **Now → Proposed:** "Това е различен провал от несъответствието" → "Това е различен провал от липсата на съгласуваност"
- **Why:** It must point back to § 7.5's defined property ("съгласуван"). "Несъответствие" reads as a generic mismatch. See T05 for the better term overall.

### F07-B19 · S2 · terminology — "семена" for seeds
- **Where:** summaryBg.md § 7.6.1 (text, table header, table caption)
- **EN:** "**300 random seeds of 500 hands each**"
- **Now → Proposed:**
  - "**300 случайни семена от по 500 раздавания**" → "**300 изпълнения (с различни начални числа) от по 500 раздавания**"
  - "| Измерване (300 семена x 500 раздавания) | Резултат |" → "| Измерване (300 начални числа × 500 раздавания) | Резултат |"
  - ": Надеждност на детектора при 300 семена по 500 раздавания." → ": Надеждност на детектора при 300 начални числа по 500 раздавания."
- **Why:** The glossary gives seed → "начално число", and § 7.7 of the same chapter uses "начални числа". "семена" is a calque. Also "x" → "×".

### F07-B20 · S2 · meaning — "hand" as the cards held rendered "раздавания"
- **Where:** summaryBg.md § 7.3 — "Като разсъждава върху **всички възможни раздавания, които противникът би могъл да държи**."
- **EN:** "By reasoning over **all the hands the opponent might have held**."
- **Now → Proposed:** "**всички възможни раздавания, които противникът би могъл да държи**" → "**всички карти, които противникът би могъл да държи**"
- **Why:** One holds cards, not deals. (Optional S3: "на ръка" for *per hand* — "(на ръка)", "0.28 на ръка", "два жетона на ръка", "печалбата на ръка" — reads as "by hand" next to the heading "изчислена на ръка". § 7.6–7.8 already use "на раздаване".)

### F07-B21 · S2 · meaning — "изчислителна мощност" for compute cost
- **Where:** summaryBg.md § 7.4 — "интерпретируемост и изчислителна мощност"
- **EN:** "trading off convergence speed, robustness to surprises, interpretability, and compute"
- **Now → Proposed:** "интерпретируемост и изчислителна мощност" → "интерпретируемост и изчислителни разходи"
- **Why:** "изчислителна мощност" is computing power (hardware). The trade-off is computational cost. For the table header see F07-X02.

### F07-B22 · S2 · calque — English idioms translated word for word
- **Where:** summaryBg.md §§ 7.4, 7.6, 7.8
- **Now → Proposed:**
  - "сравнението да е „ябълки с ябълки“" → "сравнението да е при равни условия"
  - "този глад има зъби в по-голямата игра" → "тази нужда от данни се оказва сериозен проблем в по-голямата игра"
  - "Измерването на *абсолютното* приближение на победителя издава играта" → "Измерването на *абсолютното* съответствие на победителя разкрива проблема"
  - "(статичният модел отива на отрицателна печалба). Откриването на смяната и преобучаването възстановява до здравословна печалба." → "(печалбата на статичния модел става отрицателна). Откриването на смяната и повторното обучение връщат стабилна печалба."
  - "Маниакът там изпуска по над два жетона на ръка, така че непрекъснато адаптиращ се модел го експлоатира щедро без никакво нулиране" → "Там маниакът губи над два жетона на раздаване, така че непрекъснато адаптиращ се модел го експлоатира успешно и без нулиране"
- **Why:** *apples-to-apples*, *has teeth*, *gives the game away*, *goes negative*, *healthy profit*, *leaks*, *handsomely*: each is meaningless or odd in Bulgarian when translated literally.

### F07-B23 · S2 · grammar/calque — the consistent-model bullet
- **Where:** summaryBg.md § 7.4 — "**Съгласуван.** Оценява една единствена *глобално съгласувана* стратегия"
- **EN:** "Estimate a single *globally consistent* strategy — one guaranteed to be a valid strategy over the whole game tree … This is the most principled model and the most recent; it is important enough, and central enough to the thesis…"
- **Now → Proposed:** "Оценява една единствена *глобално съгласувана* стратегия - такава, която е гарантирано да бъде валидна стратегия върху цялото дърво на играта - вместо всяка ситуация поотделно. Това е най-принципиалният модел и най-новият; той е достатъчно важен и централен за тезата, за да получи собствен раздел (Раздел 5)." → "Оценява една-единствена *глобално съгласувана* стратегия - такава, която със сигурност е валидна стратегия в цялото дърво на играта - вместо всяка ситуация поотделно. Това е най-строго обоснованият и най-новият модел; той е достатъчно важен и централен за дисертацията, за да получи собствен раздел (Раздел 5)."
- **Why:** "която е гарантирано да бъде" is ungrammatical. "принципиален" means "principled" in the moral sense or "fundamental". *Thesis* here is the dissertation: "теза" is the thesis statement (the same slip appears in "от което тезата се нуждае", § 7.5.3; change it to "дисертацията").

### F07-B24 · S2 · meaning — "пътна карта за по-нататъшната работа"
- **Where:** summaryBg.md § 7.4 — "Следващата таблица служи като **пътна карта** за по-нататъшната работа:"
- **EN:** "The following table is the mental map to carry forward:"
- **Now → Proposed:** "Следващата таблица служи като **пътна карта** за по-нататъшната работа:" → "Следващата таблица обобщава сравнението и служи за ориентир в останалата част от главата:"
- **Why:** A "roadmap for further work" is a plan of future work, which the table is not.

### F07-B25 · S2 · grammar — bold and "във" in headings
- **Where:** summaryBg.md §§ 7.5, 7.5.1
- **Now → Proposed:**
  - "## Проблемът на съгласуваността и решението във **последователна форма**" → "## Проблемът на съгласуваността и решението в последователна форма"
  - "### Недостатъкът: напасването към **средна стойност** не е равносилно на откриване на истината" → "### Недостатъкът: напасването към средната стойност не е равносилно на откриването на истината"
- **Why:** "във" is used only before в/ф. Markdown bold inside headings also leaks into `SOURCE_GAPS.md` and the TOC tooling as "…във *".

### F07-B26 · S2 · poker term — *check* rendered "проверява/проверка"
- **Where:** summaryBg.md § 7.2 type table; § 7.6
- **EN:** "Never bets, never folds — checks when it can, calls any bet." / "*both* betting and checking a middling hand"
- **Now → Proposed:**
  - "Никога не залага, никога не се отказва - проверява, когато има възможност, и плаща всеки залог." → "Никога не залага и никога не се отказва - пропуска хода без залог (чек), когато може, и плаща всеки залог."
  - "както на залагане, така и на проверка със средна ръка" → "както на залог, така и на чек със средна ръка"
- **Why:** "проверява" reads as "verifies". In poker, *check* is passing without betting.

### F07-B27 · S2 · grammar — clitic at clause start
- **Where:** summaryBg.md § 7.2 type table — "Вкарва жетони само с най-добрата ръка; се отказва от всичко останало."
- **Now → Proposed:** "Вкарва жетони само с най-добрата ръка; се отказва от всичко останало." → "Вкарва жетони само с най-добрата ръка; с всичко останало се отказва."
- **Why:** A clitic ("се") cannot open a clause in Bulgarian.

### F07-B28 · S2 · meaning — "в значителен малък брой случаи"
- **Where:** summaryBg.md § 7.6.1
- **EN:** "in a meaningful minority of runs"
- **Now → Proposed:** "в значителен малък брой случаи моделът поддържаше" → "в немалка част от случаите моделът поддържаше"
- **Why:** "значителен малък брой" is self-contradictory.

### F07-B29 · S2 · grammar — gender agreement
- **Where:** summaryBg.md § 7.6.1 — "Честният поправка не е по-голямо меню - тя е да спрем да питаме"
- **Now → Proposed:** "Честният поправка не е по-голямо меню - тя е да спрем да питаме" → "Честната поправка не е по-голямо меню, а да спрем да питаме"
- **Why:** "поправка" is feminine.

### F07-B30 · S2 · calque — "read" as "прочитане/прочетеното/прочит"
- **Where:** summaryBg.md §§ 7.6.1, 7.7, 7.9 (the fourth occurrence is in F07-B01)
- **EN:** "scale how hard you exploit to how well-earned the read is" / "if the read is useless" / "exploitation must be scaled to how well-earned the read is"
- **Now → Proposed:**
  - "**мащабираме степента на експлоатация според това колко добре е заслужено прочитането**" → "**мащабираме степента на експлоатация според това доколко е обоснована преценката за противника**"
  - "(не можете да се представите по-зле от тази стойност, ако прочитът е безполезен)" → "(дори при безполезна преценка за противника резултатът не може да е по-лош от тази стойност)"
  - "**експлоатацията трябва да бъде мащабирана според това колко добре е заслужено прочетеното.**" → "**степента на експлоатация трябва да съответства на това доколко е обоснована преценката за противника.**"
- **Why:** Poker *read* translated as "reading", in three different forms. This is the chapter's closing principle, so it should read cleanly.

### F07-B31 · S2 · calque — *leak* as "изтичане"
- **Where:** summaryBg.md §§ 7.7, 7.9
- **EN:** "a self-inflicted leak" / "opens a leak in its **own** play" / "its Nash self-leak" / "The continuous model's self-inflicted leak against Nash"
- **Now → Proposed:**
  - "## От модела до печалбата - най-добрият отговор, таванът и самонанесеното изтичане" → "## От модела до печалбата - най-добрият отговор, таванът и самонанесената уязвимост"
  - "по този начин създава **изтичане** в собствената си игра" → "по този начин създава **уязвимост** в собствената си игра"
  - "неговото изтичане при Нашево равновесие са многократно" → "неговата уязвимост срещу „Наш“ са многократно"
  - "Самопричиненото изтичане на **непрекъснатия** модел срещу **Наш равновесие**" → "Самонанесената уязвимост на **непрекъснатия** модел срещу „Наш“"
- **Why:** "изтичане" means leakage of a fluid or of data. The poker sense is a weakness in one's own play (T07). The last two items also fix the Nash naming (F07-B02).

### F07-B32 · S2 · meaning — *undersampling*
- **Where:** summaryBg.md § 7.7 — "Подбирането на ограничена извадка, което само му коства малко срещу експлоатируеми опоненти, се превръща в активно вредно срещу неексплоатируем такъв."
- **EN:** "The undersampling that merely costs it a little against exploitable opponents turns actively harmful against an unexploitable one."
- **Now → Proposed:** "Подбирането на ограничена извадка, което само му коства малко срещу експлоатируеми опоненти, се превръща в активно вредно срещу неексплоатируем такъв." → "Недостигът на наблюдения, който срещу експлоатируеми опоненти му струва малко, се оказва активно вреден срещу неексплоатируем опонент."
- **Why:** "Подбиране на ограничена извадка" means *choosing* a small sample. The EN means too few observations per situation (T08).

### F07-B33 · S2 · calque — "стратегията на героя"
- **Where:** summaryBg.md § 7.8 — "периодично преизгражда стратегията на героя като най-добър отговор"
- **Now → Proposed:** "периодично преизгражда стратегията на героя като най-добър отговор" → "периодично преизгражда собствената си стратегия като най-добър отговор"
- **Why:** *Hero* is poker-forum jargon for "our player". A Bulgarian academic reader takes "герой" literally (T14).

### F07-B34 · S2 · meaning — staleness sentence and "експлоатация с мащабирана увереност"
- **Where:** summaryBg.md § 7.8
- **EN:** "can cost more than staleness when the new opponent is exploitable enough that staleness is cheap … connect directly to Chapter 8's confidence-scaled exploitation"
- **Now → Proposed:**
  - "може да струва повече от остарялост, когато новият опонент е достатъчно експлоатируем, така че остарялостта е евтина" → "може да струва повече от остарелия модел, когато новият опонент е толкова експлоатируем, че остарелият модел губи малко"
  - "те се свързват директно с експлоатацията с мащабирана увереност от Глава 8" → "те се свързват пряко с експлоатацията, мащабирана според увереността, от Глава 8"
- **Why:** "така че" (so that) turns the condition into a purpose. "експлоатация с мащабирана увереност" means exploitation *with scaled confidence*, which inverts what is scaled by what.

### F07-B35 · S2 · meaning — "точния извличащ таван"
- **Where:** summaryBg.md § 7.9 — "най-добрият отговор достига точния извличащ таван"
- **EN:** "best response reaches the exact extractable ceiling"
- **Now → Proposed:** "най-добрият отговор достига точния извличащ таван" → "най-добрият отговор достига точния таван на извлечимата стойност"
- **Why:** "извличащ" means "extracting" (active participle), which makes the ceiling the agent.

### F07-B36 · S2 · terminology — within-chapter inconsistencies
- **Where:** summaryBg.md throughout; onePagerBg.md
- **Now → Proposed:**
  - "около една двадесета от фиш" → "около една двадесета от жетон" (elsewhere "жетони"; glossary chips → жетони)
  - "залог, кол, пас" → "залог, плащане, пас" (elsewhere "плаща")
  - "(Кун покер и Ледюк холдем)" → "(Кун покер и Ледюк Холдем)" (§ 7.7 and the one-pager capitalize)
  - "- **Базиран на типове.**" → "- **Типово базиран.**"; "| Базиран на типове |" → "| Типово базиран |"; "| базиран на типове |" (2×) → "| типово базиран |" (glossary; the text also says "типово базиран")
  - onePagerBg "**Адаптивен експлоатер**" → "**Адаптивен експлоататор**" (the summary says "експлоататор")
- **Why:** One concept, one word. Each pair above appears within the same chapter.

### F07-B37 · S2 · terminology — "Зоологическа градина" (and a mixed-script glossary entry)
- **Where:** summaryBg.md § 7.2.1 heading and table caption
- **Now → Proposed:**
  - "### Зоологическа градина от типове" → "### „Зоопарк“ от типове"
  - ": Зоологическата градина от типове опоненти: поведението на всеки постоянен стил." → ": „Зоопаркът“ от типове опоненти: поведението на всеки постоянен стил."
- **Why:** The long literal form is heavier than the figurative *zoo* (the curated glossary has "Bot zoo → Зоопарк от агенти"). The settled entry "type zoo → типoв зоопарк" contains a **Latin "o"** in "типoв" (bytes `…\320\277 o \320\262`); fix it in the picker so search and hyphenation work.

### F07-B38 · S2 · one-pager — calques and grammar
- **Where:** onePagerBg.md "Подход." and "Ключови резултати (измерени)"
- **Now → Proposed:**
  - "със смес за безопасност на Наш" → "със смесване с равновесието на Наш за безопасност"
  - "най-добре реагиращ на грешна оценка на неексплоатируем противник отваря пропуск в собствената си игра" → "най-добрият отговор на грешна оценка на неексплоатируем противник създава уязвимост в собствената му игра"
  - "най-добрият отговор достига абсолютния таван" → "най-добрият отговор достига точния таван"
  - "(безопасна експлоатация, регулирана с КЛ-дивергенция)" → "(безопасна експлоатация с KL-регуларизация)"
- **Why:** "смес за безопасност на Наш" means "a mixture for Nash's safety". A participle cannot serve as the subject. The EN says *exact*, not *absolute*. KL stays in Latin script (rule 2; T11).

### F07-B39 · S2 · calque/stale — § 7.8 opening
- **Where:** summaryBg.md § 7.8 — "Това е откритата граница, към която дисертацията е насочена да атакува, и стъпката включва първата контролирана сонда."
- **EN:** "This is the open frontier the thesis is positioned to attack, and the step includes a first controlled probe."
- **Now → Proposed:** "Това е откритата граница, към която дисертацията е насочена да атакува, и стъпката включва първата контролирана сонда." → "Това е отворен проблем, към който е насочена дисертацията, и главата включва първи контролиран експеримент по него."
- **Why:** "насочена да атакува" is ungrammatical. "сонда" (a probe instrument) is a calque. "стъпката" is stale naming (F07-C05).

### F07-B40 · S2 · meaning — "Когато класът на модел съвпада"
- **Where:** summaryBg.md § 7.7 — "Когато класът на модел съвпада, най-добрият отговор"
- **EN:** "When the model class fits, best response extracts the full theoretical value"
- **Now → Proposed:** "Когато класът на модел съвпада, най-добрият отговор" → "Когато класът на модела пасва на противника, най-добрият отговор"
- **Why:** "съвпада" (coincides) has no object. The same idea is rendered correctly in § 7.9 ("съответства на противника").

### F07-B41 · S2 · typography — hyphen used as dash (≈ 92 places; corpus-wide)
- **Where:** summaryBg.md and onePagerBg.md throughout, e.g. "стратегия, която не може да бъде победена в дългосрочен план" is preceded by "*равновесие на Наш* - стратегия"; the PDF also breaks a line *before* the hyphen (p. 131: "…колкото и да е умен / - не може да я свали…").
- **Now → Proposed:** " - " → " – " (en dash with spaces; better a non-breaking space before it) outside math, code and tables of negative numbers.
- **Why:** The Bulgarian dash is "–" or "—", not a hyphen. This is corpus-wide: every step's summaryBg uses " - " (step 06 has 408), and only step 04 has a few "–". Fix once centrally (a pandoc filter or a guarded replace in the build), not per chapter.

### F07-B42 · S2 · typography — decimal point, thousands comma, "x" (corpus-wide)
- **Where:** summaryBg.md: 78 decimal numbers (all tables, § 7.2 math, text), "мач от 20,000 раздавания", "(300 семена x 500 раздавания)"; onePagerBg.md likewise.
- **Now → Proposed:** decimal point → decimal comma (in math `0{,}571`); "20,000" → "20 000"; "x" → "×".
- **Why:** Bulgarian uses the decimal comma. The BG figures already get it (`render_bg_figures.py` formats ticks with a comma), so text and figures now disagree. This is corpus-wide (every summaryBg mostly uses points), so a central decision is needed. "20,000" reads as 20.000 in Bulgarian.

### F07-B43 · S2 · formatting — bold the EN does not have (≈ 18 spans)
- **Where:** summaryBg.md has 148 bold spans vs 106 in the EN. The excess is concentrated in § 7.2 (32 vs 12). Spans not covered by other findings:
  - § 7.1: "**Равновесна стратегия на Наш**", "**игра за двама с нулева сума**", "**ограничение**"
  - § 7.2: "Всяко негово **действие** е следа", "**Моделиране на противника** *представлява*", "чести **залози**", "след четири **раздавания**", "интеграл или **симулация**", "Тази **затворена форма** съответства на „**непрекъснатия**“ модел"
  - § 7.4: "Няма един-единствен **модел на противника**", "Естествената **цел** е **хибриден подход**"
  - § 7.6.1: "една **наивна метрика** обединява: *бавна **сходимост*** и *отпадане след **сходимостта***"
  - § 7.9: "на **непрекъснатия** модел" (see F07-B31)
- **Now → Proposed:** remove the `**…**` around each listed span; for "*бавна **сходимост*** и *отпадане след **сходимостта***" → "*бавна сходимост* и *отпадане след сходимостта*".
- **Why:** The translation pipeline bolded glossary terms. In print (pp. 131, 134, 136) whole sentences look shouted and the real emphasis is lost.

## T — Glossary-level terminology

### F07-T01 · S1 · "safety-exploitation spectrum → спектър безопасност–изследване"
- **Where:** `llmPipeline/glossary_settled.md`; printed in step 07 § 7.9 (F07-B05).
- **Now → Proposed:** "спектър безопасност–изследване" → "спектър безопасност–експлоатация"
- **Why:** "изследване" means exploration. The error is in the glossary, so any other chapter that uses the term inherits it.

### F07-T02 · S1 · "call → залог"
- **Where:** glossary_settled.md
- **Now → Proposed:** "залог" → "плащане (кол)"; verb "плаща"
- **Why:** *Bet* is also "залог", so bet and call become indistinguishable. The raise/call confusion in F07-B06 shows the cost.

### F07-T03 · S1 · verb entries in dictionary (1st-person) form leak verbatim
- **Where:** glossary_settled.md: "best-respond → оптимално отговарям" (freq 4), "randomize → рандомизирам", "break even → изравняване". Results: "да **рандомизирам**", "„**оптимално отговарям** на…“", "наблюдавай → моделирай → оптимално отговарям"; figure labels "отговарям на…", "повтарям…", "приемам наблюдения…", "извличам…" (F07-B01, G03, G05, G08).
- **Now → Proposed:** store verb terms as a noun or neutral phrase with a "conjugate" flag: best-respond → "(да) играе най-добрия отговор" / noun "най-добър отговор"; randomize → "избира на случаен принцип"; break even → "излиза на нула".
- **Why:** Bulgarian cites verbs in the 1st-person singular, so a pipeline that inserts the entry as is produces "I randomize" in impersonal prose.

### F07-T04 · S2 · prior / likelihood / conjugate prior
- **Where:** glossary_settled.md: "prior → предварително убеждение", "likelihood → вероятност", "conjugate prior → спрегнат априорен"
- **Now → Proposed:** prior → "априорно разпределение" (keep "предварително убеждение" only for the informal *prior belief*); likelihood → "правдоподобие"; conjugate prior → "спрегнато априорно разпределение"
- **Why:** Bulgarian statistics pairs "априорно/апостериорно". The chapter already mixes "предварително убеждение", "априорно разпределение" and "предварително разпределение" for one object. "вероятност" erases the probability/likelihood distinction the Bayes formula rests on, and the BG one-pager already writes "априорно × правдоподобие → апостериорно".

### F07-T05 · S2 · consistent / consistency — decide before chapters 08 and 12 diverge further
- **Where:** curated `terminology_EN_BG.md`: "Consistent opponent modeling → Консистентно моделиране на противника"; settled: "consistent → съгласуван", "consistency → съгласуваност", "inconsistency → несъответствие". The chapter uses "съгласуван" (it departs from the curated file).
- **Now → Proposed:** For the *statistical* property Ganzfried defines (the estimate converges to the true strategy), use the standard Bulgarian statistics term "състоятелен / състоятелност" (as in "състоятелна оценка"), with inconsistency → "липса на състоятелност". Keep "съгласуван" only for "consistent with the observations" (trajectories, deals) and "globally consistent (valid) strategy". Then the model is named "състоятелен модел".
- **Why:** The two glossaries disagree and the chapter follows neither consistently (F07-B18). "съгласуван" also collides with its other sense inside the same section (the "съгласувани траектории").

### F07-T06 · S2 · "intractable → неразрешим"
- **Where:** glossary_settled.md; step 07 §§ 7.2, 7.5; step 11 (`SOURCE_GAPS.md` quotes "**неразрешим** от гледна точка на изчислителна мощност")
- **Now → Proposed:** intractable → "изчислително непосилен" (or "трудноизчислим"); tractable → "ефективно изчислим"
- **Why:** "неразрешим" means unsolvable or undecidable, which is a stronger and different claim than "too expensive to compute".

### F07-T07 · S2 · "leak → изтичане"
- **Now → Proposed:** "изтичане" → "уязвимост" (in one's own play) / "слабост"
- **Why:** A calque of poker slang. In Bulgarian, "изтичане" is data or fluid leakage (F07-B31).

### F07-T08 · S2 · "undersampling → подбиране на ограничена извадка"
- **Now → Proposed:** → "недостатъчна извадка" / "недостиг на наблюдения"
- **Why:** The entry describes *selecting* a small sample, which is not the phenomenon (F07-B32).

### F07-T09 · S2 · "sweep → обхождане", "robustness sweep → обхождане за устойчивост"
- **Now → Proposed:** → "серия експерименти" / "проверка на устойчивостта"
- **Why:** "обхождане" is traversal and collides with "обхождане на дървото на играта" in the same chapter (§ 7.9). The § 7.6.1 heading and § 7.9 "увереното, но грешно обхождане" do not read as an experiment series. Proposed § 7.6.1 heading: "Колко дълго може да остане грешен? Проверка на устойчивостта"; § 7.9: "увереното, но грешно обхождане" → "проверката на увереното, но грешно убеждение".

### F07-T10 · S2 · "projected gradient → проектиран градиентен метод"; "convex program → изпъкнала програмираща задача"
- **Now → Proposed:** → "градиентен метод с проекция"; → "задача на изпъкналата оптимизация"
- **Why:** "проектиран" reads as "designed". "програмираща задача" is a calque of *program* (F07-B16).

### F07-T11 · S2 · KL entries
- **Where:** "kl divergence → разминаване на Кълбек-Лайблер", "kl-regularized → регулиран с КЛ-дивергенция"
- **Now → Proposed:** → "дивергенция на Кулбак–Лайблер (KL)"; → "с KL-регуларизация"
- **Why:** Rule 2 keeps abbreviations in Latin script, so not "КЛ". The standard Bulgarian transliteration of Kullback is "Кулбак". This affects chapter 8 heavily.

### F07-T12 · S2 · "compute → изчислителна мощност"
- **Now → Proposed:** → "изчислителни разходи / изчислителна цена" when the meaning is cost (always, in this corpus)
- **Why:** "мощност" means hardware power (F07-B21, F07-X02).

### F07-T13 · S3 · "Nash EV → Нашева очаквана стойност"; "exploitation gap → пропуснато от експлоатация"
- **Now → Proposed:** → "очаквана стойност при равновесие на Наш" (the chapter's own table caption already says so); → "неизползван потенциал за експлоатация" (table header: "Разлика")
- **Why:** "Нашева" is an unusual adjective. "Пропуснато от експлоатация" reads as "missed by exploitation".

### F07-T14 · S3 · "hero → герой"
- **Now → Proposed:** → "собственият агент"
- **Why:** Poker-forum jargon, read literally by a non-poker reader (F07-B33, fig. 36 y-label).

## C — Content

### F07-C01 · S1 · Non-stationarity numbers and "single seed" caveat are stale
- **Where:** summaryBg.md § 7.8 table and last paragraph; onePagerBg.md; the same in summaryEn.md l. 488–489, 506–507 and onePager.md.
- **Problem:** The summary shows seed-0 values and says "(Този експеримент беше проведен при едно начално число…)". `implementation/step07/implementation/results/{kuhn,leduc}_scale.json` has 5 seeds [0–4], and seed 0 is exactly −0.116/+0.226 and +1.940/+0.525. report_en/report_bg §10 give the 5-seed means ± SE, and every seed agrees on the sign.
- **Now → Proposed:**
  - "| Кун | камък → маниак | **-0.116** | **+0.226** |" → "| Кун | камък → маниак | **-0.106 ± 0.007** | **+0.211 ± 0.008** |"
  - "| Ледюк | камък → маниак | **+1.940** | **+0.525** |" → "| Ледюк | камък → маниак | **+1.834 ± 0.054** | **+0.552 ± 0.017** |"
  - "(Този експеримент беше проведен при едно начално число, така че възприемайте *посоката* като стабилна, а точните величини - като илюстративни.)" → "(Стойностите са средни от пет начални числа ± стандартната грешка; посоката на ефекта е една и съща при всяко от тях.)"
  - onePagerBg "(Kuhn: -0.116 -> +0.226)" → "(Кун: -0.106 → +0.211)"
- **Note:** "around sixty resets" is fine (JSON: 55–60 per seed in Kuhn, 54–63 in Leduc). report_en l. 264 "58–59 resets per seed" does not match the JSON (54–63); fix it in the report.

### F07-C02 · S2 · "0.11 to 0.28" does not match the table above it
- **Where:** summaryBg.md § 7.1 — "**от 0.11 до 0.28 на ръка**"; EN l. 80 "**0.11 to 0.28 per hand**"
- **Problem:** The table shows gaps 0.215 / 0.227 / 0.213. The 0.11 and 0.28 values come from the *second-seat* rows that the summary omits (report_en §3: AlwaysCall seat 1 = 0.113, TightPassive seat 1 = 0.278).
- **Now → Proposed:** "**от 0.11 до 0.28 на ръка**" → "**около 0.21-0.23 на раздаване** (от 0.11 до 0.28, ако се вземат предвид и двете позиции на масата)"; EN: "**about 0.21–0.23 per hand** (0.11–0.28 across both seats)". The one-pager range is fine as it stands.

### F07-C03 · S2 · Overclaim: "statistically indistinguishable from the ceiling on every type in both games"
- **Where:** summaryBg.md § 7.7 — "типово базираният модел е статистически неразличим от тавана за всеки тип и в двете игри"; onePagerBg.md "типово базираният модел е статистически неразличим от тавана на най-добрия отговор срещу всеки противник и в двете игри"; EN equivalents; report_en l. 281.
- **Problem:** From `mean_per_hand_by_seed` in the results JSON (SE = sd of the 5 seed means / √5): Leduc Rock 0.912 vs 0.937 (SE 0.008, −3.2 SE), a row of the chapter's own Leduc table; Leduc Level2 2.679 vs 2.714 (−2.2 SE); Kuhn AlwaysPass 0.966 vs 0.975 (SE 0.001, −17 SE). 16 of 19 types are within 2 SE, and all are within 3 % of the ceiling.
- **Now → Proposed:** "типово базираният модел е статистически неразличим от тавана за всеки тип и в двете игри" → "типово базираният модел остава в рамките на 3% от тавана за всеки тип и в двете игри (и в рамките на две стандартни грешки за почти всички типове)"; the same in the one-pager and EN ("stays within 3 % of the ceiling on every type in both games, and within two standard errors on nearly all").

### F07-C04 · S2 · Overclaim: "without private information you cannot learn beyond your prior"
- **Where:** summaryBg.md § 7.3; EN l. 192–195
- **Problem:** Even without showdowns the observed action frequencies update the posterior: they rule out strategies whose *marginal* action frequencies disagree. What is lost is the *identifiability* of the card-conditional strategy, which is exactly Ganzfried (2025)'s assumption (ii).
- **Now → Proposed:** "Следствието е истински теоретичен лимит, а не неудобство при имплементацията: **без никога да наблюдавате частната информация на противника, не можете да научите повече от своето предварително убеждение**. Ако единственото, което виждате, са пасове, повече **раздавания** не помага - доказателството е фундаментално двусмислено." → "Следствието е истинско теоретично ограничение, а не неудобство при имплементацията: **без да наблюдавате частната информация на противника, можете да научите колко често той избира всяко действие, но не и с кои карти го прави**. Много различни стратегии пораждат едни и същи честоти на действията и повече раздавания не могат да ги различат." EN: "…**without ever observing the opponent's private information, you can learn how often they take each action but not which hands produce it**: many strategies yield the same action frequencies, and more hands cannot tell them apart."

### F07-C05 · S2 · Stale "Step" naming
- **Where:** summaryBg.md l. 21 "в по-ранните стъпки" (the EN says "chapters"), l. 155 "разглежданата стъпка", l. 194 "стъпката поставя изрично", l. 274 (F07-B39); fig. 31 "Стъпка 7/8" (F07-G02); summaryEn.md l. 52 "the whole step in miniature", l. 321 "underneath the whole step", l. 336 "the step poses", l. 472 "the step includes"; onePager.md "the step's real-time-feasibility question".
- **Now → Proposed:**
  - "Игровотеоретичен агент, изчислен в по-ранните стъпки, определя *равновесие на Наш*" → "Игровотеоретичният агент от предходните глави изчислява *равновесие на Наш*"
  - "Този раздел представлява теоретичната граница на разглежданата стъпка" → "Този раздел е най-напредналата теоретична част на главата"
  - "въпрос, който стъпката поставя изрично" → "въпрос, който главата поставя изрично"
  - EN: "step" → "chapter" in the four places above.
- **Why:** The bundle says "Глава". "изчислен агент" also misreads the EN (the agent *computes* the equilibrium).

### F07-C06 · S3 · Nash EV −0.060 vs the rock is below the game value the text says cannot be undercut
- **Where:** summaryBg.md § 7.1 table row "Камък … | -0.060 |" and the parenthesis "(Малките отрицателни Нашеви стойности са известният недостатък на първия играч в Кун покер от $-1/18 \approx -0.056$…"
- **Problem:** −0.060 < −1/18 ≈ −0.0556, although the text says no opponent can push an equilibrium below the game value. The Part I "Nash" is a 20 000-iteration CFR approximation (`exploration/exploitation_opportunity.py`), so small dips are expected but unexplained.
- **Fix:** Add to the parenthesis: "; равновесието тук е приближение, получено с 20 000 итерации на CFR, затова срещу отделен противник стойността може да падне с няколко хилядни под $-1/18$".

## S — Sources

### F07-S01 · S2 · SOURCE_GAPS row 1: "не — дори при наличие на безкрайни данни" → cite Ganzfried (2025)
- **Where:** summaryBg.md § 7.5 intro — "Изненадващият отговор е **не - дори при наличие на безкрайни данни** - и съществува принципно решение."
- **Proposal (cite):** append `[^ganzfried2025]` after "принципно решение.". Verified on the arXiv abstract of 2508.17671: existing approaches "do not guarantee that the model approaches the opponent's true strategy even in the limit as the number of game iterations approaches infinity", and the new algorithm is guaranteed to converge.

### F07-S02 · S2 · SOURCE_GAPS row 2: inside-the-hull collapse → Ganzfried (2025), Proposition 2
- **Where:** summaryBg.md § 7.5.1 — "…асимптотично убеждението **колабира върху една извадка**, вместо да се установи на истинската смес."
- **Proposal (cite):** append `[^ganzfried2025]` after "истинската смес.", and optionally name the method: "…методът на най-добрия байесов отговор с извадки (Ganzfried, 2025, твърдение 2)…". Verified in the arXiv HTML v7: σ* = (1/3,1/3,1/3), samples s1 = (0.2,0.4,0.4), s2 = (0.6,0.3,0.1), s3 = (0.2,0.3,0.5), "BBR will select s1 with probability → 1". The outside-hull case uses σ* = (0.8,0.1,0.1) with samples (0.5,0.3,0.2), (0.3,0.5,0.2), (0.2,0.3,0.5). The figure should match these (F07-G06).

### F07-S03 · S2 · SOURCE_GAPS row 3: "оценката доказано се сближава към σ*" → Ganzfried (2025), Proposition 4, plus one missing condition
- **Where:** summaryBg.md § 7.5.2 — "при леки условия (истината има положителна предварителна плътност, различни стратегии водят до различими наблюдения и всяка ситуация на противника се посещава безкрайно често) оценката доказано се сближава към $\sigma^*$"
- **Proposal (cite and correct):** → "при стандартни условия (истинската стратегия лежи във вътрешността на множеството от допустими стратегии и има положителна априорна плътност, различни стратегии водят до различими наблюдения и всяка ситуация на противника се посещава безкрайно често) оценката доказано се сближава към $\sigma^*$[^ganzfried2025]". Verified in HTML v7, Proposition 4: "(i) the true opponent strategy lies in the interior of ℳ and the prior assigns it positive density; (ii) … identifiable…; (iii) (persistent excitation) every opponent information set is visited infinitely often with nonzero frequency". The abstract calls these "standard Bayesian identifiability and visitation assumptions". "леки" is also a calque of *mild*.

### F07-S04 · S2 · Claim attributed to "the literature" that the cited paper does not make
- **Where:** summaryBg.md § 7.5.3 — "Причината е същата, която и самата литература посочва:"; EN "The reason is the reason the literature itself flags:"
- **Problem:** Ganzfried (2025) says the opposite: "we expect the approach to be scalable to large problems…" (HTML v7). Per-refit cost growing with history is this project's own measurement.
- **Proposal (soften):** "Причината е същата, която и самата литература посочва:" → "Причината е практическа:"; EN → "The reason is practical:".

### F07-S05 · S2 · Shoham & Leyton-Brown footnote cites the wrong sections (shared by steps 01, 02, 07, 08)
- **Where:** summaryBg.md footnote `shoham2008` — "Гл. 3–4 (игри в нормална и разгърната форма); гл. 5 (игри в разгърната форма); §3.4 (изчисляване на равновесия) и §4.6 (изчисляване на най-добри отговори) - механизмът в последователна форма под всяка линейна програма в Глава 8;"
- **Problem:** Checked against masfoundations.org/toc.html. Ch. 4 is "Computing Solution Concepts of Normal-Form Games" (not extensive form); §3.4 is "Further solution concepts for normal-form games"; §4.6 is "Computing correlated equilibria". The sequence form is in §5.2 ("Imperfect-information extensive-form games"). Ch. 7 "Learning and Teaching" is correct.
- **Proposal (correct):** → "Гл. 3 (игри в нормална форма); гл. 4 (изчисляване на решения на игри в нормална форма, §4.1 - линейно програмиране за игри с нулева сума); гл. 5 (игри в разгърната форма; §5.2 - игри с непълна информация и последователната форма, механизмът под всяка линейна програма в Глава 8);". The same correction applies to the EN footnote and to the identical footnote in steps 01, 02 and 08.

### F07-S06 · S3 · "first made … a theorem" overclaims (footnote `ganzfried2015`)
- **Where:** summaryBg.md footnote — "статията, която за първи път формулира като теорема принципа „експлоатирай, но никога не губи спрямо базовата линия“"
- **Problem:** McCracken & Bowling (2004, AAAI Fall Symposium on Artificial Multi-agent Learning) already proposed ε-safe strategies; Ganzfried & Sandholm characterize *when* safe exploitation is possible. Verified by web search: the AAAI FS-04-02 listing and Bowling's publication list.
- **Proposal (soften and complete):** "статията, която за първи път формулира като теорема принципа" → "статията, която характеризира кога е възможен принципът"; add "3(2), DOI 10.1145/2716322" (verified in Crossref).

### F07-S07 · S2 · The change-point detector is unsourced
- **Where:** summaryBg.md § 7.8 — "лек статистически монитор върху агресията на опонента"
- **Problem:** The method is Bayesian Online Change-point Detection, named in `implementation/step07/implementation/changepoint.py`, but the chapter neither names nor cites it.
- **Proposal (cite):** "лек статистически монитор върху агресията на опонента" → "лек статистически монитор върху агресията на опонента (байесово онлайн откриване на точки на промяна[^adams2007])", plus the new footnote `[^adams2007]: Adams, R. P. & MacKay, D. J. C. (2007). "Bayesian Online Changepoint Detection." *arXiv:0710.3742*.` Verified on the arXiv abstract page.

### F07-S08 · S3 · Footnote metadata (spot-check of key citations)
- **Where:** footnotes `bard2013`, `ganzfried2016`
- **Findings:** `bard2013` lists one author; the paper has four: "Bard, N., Johanson, M., Burch, N. & Bowling, M. (2013) … AAMAS, 255–262" (Crossref). `ganzfried2016` says "(2016/2018) … IEEE CIG": the venue is 2018 IEEE CIG, DOI 10.1109/CIG.2018.8490452 (Crossref), with the arXiv preprint 1603.03491 from 2016. "Theorem 2.1: respond to the posterior mean" **checked correct** in arXiv v6: "the payoff against the mean of a strategy distribution equals the payoff against the full distribution". `southey2005` checked correct (UAI 2005, arXiv:1207.1411). `ganzfried2025` checked correct (arXiv:2508.17671, single author, 25 Aug 2025).

## X — Structure

### F07-X01 · S2 · Two footnote markers point into other chapters
- **Where:** bundle p. 133 marker 24 (`southey2005`) and p. 148 marker 9 (`shoham2008`)
- **Problem:** The bundle is compiled as one document and the footnote labels are shared across chapters, so pandoc keeps the first definition. The Southey note prints only on p. 33 (chapter 3) and the Shoham note only on p. 11 (chapter 1), checked with a PyMuPDF text search of `allSummaries_bg.pdf`. A chapter-7 reader sees markers with nothing at the page foot. The same affects `ganzfried2015` in chapter 8, which points back into chapter 7.
- **Fix:** In `scripts/build_reports.py` bundling, prefix each chapter's footnote labels (e.g. `[^southey2005]` → `[^c07-southey2005]`) before concatenation.

### F07-X02 · S2 · Table 17 headers collide
- **Where:** bundle p. 138, table "Трите модела на противника, сравнени…". "Интерпретируемост" runs into "Изчислителна мощност".
- **Now → Proposed:** "| Модел | Представлява | Сближаване | Устойчив на непознати противници? | Интерпретируемост | Изчислителна мощност |" → "| Модел | Представлява | Сближаване | Устойчив на непознати противници? | Интерпретируемост | Изчислителна цена |", and the separator "|---|---|---|---|---|---|" → "|---|----|----|----|-----|---|".
- **Why:** Pipe-table column widths follow dash counts. Equal thirds give column 5 about 80 pt, while "Интерпретируемост" needs about 90 pt; 5/23 gives about 105 pt. "мощност" is also wrong in meaning (F07-B21).

### F07-X03 · S3 · Cross-references "Раздел N" vs printed "7.N"
- **Where:** summaryBg.md: "Раздел 2", "Раздел 4", "Раздел 5", "раздел 6", "Раздел 7", "Раздели 4–5" (about 15 places)
- **Fix:** → "раздел 7.N" (lower case, as the glossary's "както е показано в раздел N"). In a 226-page bundle, a bare "Раздел 5" can be read as chapter 5.

### F07-X04 · S3 · Opponent types used but never defined
- **Where:** summaryBg.md § 7.7 Leduc table ("Ниво-1") and fig. 36 (also LoosePassive, Random, Level 2/3)
- **Fix:** After the Leduc table add: "(„Ниво 1“ е противник, който играе най-добър отговор срещу случаен играч; в Ледюк менюто на типово базирания модел съдържа девет типа, показани на фигура 36.)" Source: `implementation/step07/implementation/level_k.py` ("Level 0: uniform random; Level k: best-responds to Level (k-1)") and report_en l. 197.
