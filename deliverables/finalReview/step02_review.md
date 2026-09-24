# Step 02 — final review

**Summary:** The chapter is short and mostly readable, but four things matter. (1) **Math.** The equilibrium table gives the second player's Queen call as 1/3 + α; the correct value is 1/3, and the chapter's own fig. 5 and results JSON show 0.335. Regret matching's average regret is said to vanish at O(√T); the correct rate is O(1/√T). The CFR bound is printed as O(Δ√(|I|/T)), but Zinkevich's Theorem 4 is linear in |I|. (2) **Bulgarian terms that change the meaning.** "нормални / разширени игри" is used for normal-/extensive-form games. "двуигрови" (literally "two-game") is used for two-player games; it comes from the settled glossary and occurs in six chapters. The Kuhn equilibrium list renders *call* as "залог", so King's line reads "Винаги залог, винаги залог". The one-pager turns Player 0's first-mover *disadvantage* into an "предимство". (3) **English left in print.** All three figures are entirely English, because `plotting.py` has no `__main__` and the curve data are not saved. Fig. 5 prints at 4.8–6.5 pt. The heading "От single-agent RL…" and the formula's "if/otherwise" are also English. (4) **Numbers.** "Game value −0.0602" is a running mean of sampled payoffs, not the value of the output strategy, which is −0.0555. "Chapter 14" is stale, and the report claims "all targets achieved" to 4 decimals. Of the candidate's 14 August comments, 10 are fully applied, 4 only partly (F02-B02, B06, B09, X02).
**Counts:** S1 15 · S2 23 · S3 5   (by category: G 4 · B 13 · T 4 · C 14 · S 6 · X 2)

Conventions in this file (as in the pilot):
- **Quotes.** Quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md` (including `**`, `*`, `$`). "EN" quotes come from `summaryEn.md` / `onePager.md`.
- **Page numbers.** "p. N" is the PDF page of `allSummaries_bg.pdf`; the printed folio is N − 1.
- **Decided centrally, counted but not quoted.** Proposals keep the current " - " dashes and decimal points. Counts: hyphen used as dash 34 (summary) + 11 (one-pager); bold spans 83 in BG vs 49 in EN; decimal points 5 + 16, plus "100,000" once. One shared footnote label (F07-X01): `shoham2008` is defined in chapter 1, so its two markers "9" in this chapter (pp. 19, 20) print no note.
- **Printed size.** Printed pt = matplotlib size × (17.6 cm ÷ saved width). The floor is ≈ 8.2 pt.

**Candidate's comments (chapter 2, 14):**
- **Applied (10):** "от първият", "и стига до", "непълна", "пълна", the four "източник/източници", "Вале", "изпитателно".
- **Partly applied (4):**
  - "игри а двама": done at the marked place; four "двуигрови" remain (F02-B02).
  - "това" on "нашето равновесие": now "Нашевото равновесие" (F02-B06).
  - "приблизителна стойност": done in the summary; the one-pager still says "„предсказвач“ най-добър отговор" (F02-B09).
  - Figure descriptions under each image with "фигура N": the captions are still the English alt text and nothing refers to "фиг. N" (F02-X02, F02-G01).
- **Chapter-0 (TOC) comments:** none concern chapter 2's headings except "Стъпка → Глава", which is applied.

## G — Figures

### F02-G01 · S1 · Bulgarian captions for all three figures (merge the italic descriptions into them)
- **Where:** summaryBg.md § "Емпирични визуализации"; pp. 26–28. The printed captions read "Фигура 3: Game Value Convergence", "Фигура 4: Exploitability Convergence", "Фигура 5: Strategy Analysis" (known corpus-wide defect). The real description is a separate italic paragraph under each caption.
- **Now → Proposed:**
  - "![Game Value Convergence](game_value_convergence.png)" → "![Средната печалба на Играч 0 при изтеглените раздавания, усреднена от началото на обучението, се приближава към теоретичната стойност $-1/18$ с нарастване на броя на итерациите на CFR.](game_value_convergence.png)"
  - "![Exploitability Convergence](exploitability_convergence.png)" → "![Експлоатируемост на средната стратегия спрямо броя на итерациите в двулогаритмичен мащаб. Измерените точки следват приблизително еталонния наклон $O(1/\sqrt{T})$ (прекъснатата линия), което съответства на теоретичната граница.](exploitability_convergence.png)"
  - "![Strategy Analysis](strategy_analysis.png)" → "![Средната стратегия, получена с CFR за Кун покер след 100 000 итерации: вероятностите за действие във всяко информационно множество. Честотите на блъф с вале и на плащане с дама съответстват на семейството от равновесия на Наш (α ≈ 0.19).](strategy_analysis.png)"
- **Fix:**
  - Replace the alt text in `summaryBg.md`, then delete the three italic paragraphs that follow the figures (they would repeat the caption).
  - Mirror the change in `summaryEn.md`: EN captions from the EN italic paragraphs, softened as in F02-C06 / C09.
  - When the BG renders exist (F02-G02–G04), change the file names to `*_bg.png`.
  - For the pseudo-headings, see F02-X02.

### F02-G02 · S1 · Fig. 3 game value: entirely English, legend over the curve, wrong player, quantity mislabelled
- **Where:** `renders/ch02/p026_f1.png` — caption "Фигура 3: Game Value Convergence"
- **Problem:**
  1. **Entirely English.** The title "Convergence of Game Value to Nash Equilibrium", the legend "Computed game value" / "Theoretical value (-1/18 ≈ -0.0556)", the axis labels, and the decimal points are all English. Cause: `summaryBg.md` links the EN file, and no `_bg` twin exists. The only step-02 script in `plotting_scripts()` is `implementation/step02/utils/plotting.py`. It has no `__main__`, so `render_bg_figures.py` runs it and writes nothing. The curves are produced at run time by `cfr/train.py` and `evaluate/convergence.py`, and their data are never saved.
  2. **Wrong player.** The y-label says "(Player 1)", but the text calls the first mover Player 0.
  3. **Legend over the curve.** The legend box sits on the curve between 60 000 and 100 000 iterations.
  4. **Mislabelled quantity.** "Computed game value" is `cumulative_util / (i + 1)` in `cfr_trainer.py`: the running mean of the *sampled* payoffs of the *current* strategies since iteration 1. It is not the value of any strategy (F02-C06).
  5. **Size.** 1299 px at 150 dpi = 8.66 in, printed 17.6 cm, so scale 0.800. Axis, tick and legend text 10 → 8.0 pt, just under the floor; title 12 → 9.6 pt; 188 ppi.
- **Fix:**
  - **Save the data and fix the seed.** In `cfr/train.py`: `random.seed(0)` at the top of `main()`, and add `"iteration_history": trainer.iteration_history, "game_value_history": trainer.game_value_history` to the dict in `save_results`.
  - **Add a `__main__` to `utils/plotting.py`** that re-plots from JSON, so the renderer can produce the BG twin without re-training:
    ```python
    if __name__ == "__main__":
        import json, types
        here = os.path.dirname(os.path.abspath(__file__))
        res = json.load(open(os.path.join(here, "..", "models", "cfr_results.json")))
        out = os.path.join(here, "..", "..", "..", "deliverables", "reports", "step02", "summary")
        class _Avg:
            def __init__(self, row): self.row = row
            def get_average_strategy(self): return [self.row["p_pass"], self.row["p_bet"]]
        stub = types.SimpleNamespace(node_map={k: _Avg(v) for k, v in res["strategies"].items()},
                                     iteration_history=res.get("iteration_history", []),
                                     game_value_history=res.get("game_value_history", []))
        create_strategy_charts(stub, out)
        if stub.iteration_history:
            create_convergence_chart(stub, out)
        conv = os.path.join(here, "..", "models", "convergence.json")
        if os.path.exists(conv):
            c = json.load(open(conv))
            create_exploitability_chart(c["checkpoints"], c["exploitabilities"], out)
    ```
  - **Changes in `create_convergence_chart`:**
    - `figsize=(10, 5)` → `(8, 4)`; `dpi=150` → `300`.
    - Drop `set_title`; the caption carries it.
    - `ax.legend(loc='lower right', fontsize=10)`.
    - `label='Computed game value'` → `'Running mean of sampled payoffs'`.
    - `set_ylabel('Average Game Value (Player 1)')` → `'Payoff to Player 0 (running mean)'`.
  - **Mapping (`figure_labels.json`), new keys:**
    - 'Running mean of sampled payoffs' → 'Текуща средна на изтеглените печалби'
    - 'Payoff to Player 0 (running mean)' → 'Печалба на Играч 0 (текуща средна)'
    - 'Theoretical value (-1/18 ≈ -0.0556)' → 'Теоретична стойност (−1/18 ≈ −0,0556)'. This is the runtime value of the f-string, which the static extractor did not see.
  - **Then:**
    - Run `python cfr/train.py` once, and `python scripts/figures/render_bg_figures.py --only step02`.
    - In `summaryBg.md`, change `(game_value_convergence.png)` → `(game_value_convergence_bg.png)`.
    - The seeded re-run changes the one-pager's numbers: α, 0.58247/0.58221, 2.6e-4, the ≥ 0.9999 values, 0.002–0.011, 0.3403, 0.5387/0.5274 and −0.0602. Update them from the new `cfr_results.json`.
  - **If a re-run is not wanted,** only fig. 5 can be translated (F02-G04). Figs. 3–4 then stay English, with the BG captions from F02-G01.

### F02-G03 · S1 · Fig. 4 exploitability: entirely English, stops at 50 000, one unseeded run per point
- **Where:** `renders/ch02/p027_f1.png` — caption "Фигура 4: Exploitability Convergence"
- **Problem:**
  1. **Entirely English.** Title "CFR Convergence: Exploitability vs Iterations (log-log)", legend "Measured exploitability" / "O(1/√T) reference", axis labels. Same cause as F02-G02.
  2. **Stops at 50 000.** The x-axis ends at 5·10⁴ (`config.py` checkpoints `[100, 500, 1_000, 5_000, 10_000, 50_000]`), while the chapter's run and fig. 3 use 100 000.
  3. **One unseeded run per point.** `evaluate/convergence.py` trains a *fresh, unseeded* `KuhnTrainer` for each checkpoint, so each point is one independent run. That is why the curve has a plateau between 1 000 and 5 000. The reference line is anchored to the first point only.
  4. **Size.** 1284 px at 150 dpi = 8.56 in, scale 0.809, so labels 10 → 8.1 pt (borderline); 185 ppi.
- **Fix:**
  - **`config.py` checkpoints** → `[100, 300, 1_000, 3_000, 10_000, 30_000, 100_000]`.
  - **`convergence.py`:**
    - Per seed `s` in 0–4: `random.seed(s)`, one trainer trained incrementally (`trainer.train(cp - done)`; the regret tables persist between calls), and exploitability measured at each checkpoint.
    - Save `{"checkpoints", "exploitabilities" (mean over seeds), "min", "max"}` to `models/convergence.json`.
  - **`create_exploitability_chart`:**
    - `figsize=(10, 6)` → `(8, 4.6)`; `dpi` → 300.
    - Drop `set_title`; `ax.legend(fontsize=10)`.
    - Optional: `ax.fill_between` for the min–max band.
  - **Mapping:**
    - '$O(1/\sqrt{T})$ reference' → 'еталонен наклон $O(1/\sqrt{T})$'. The current 'референтна' is an adjective with no noun.
    - 'CFR Iterations' 'итерации на CFR' → 'Итерации на CFR'.
    - 'Exploitability' 'експлоатируемост' → 'Експлоатируемост' (axis labels; both keys are shared with step03).
  - Re-render as in F02-G02 and link `exploitability_convergence_bg.png`. Update the slope in the text (F02-C09).

### F02-G04 · S1 · Fig. 5 strategy analysis: illegible (4.8–6.5 pt), English, numbering contradicts the text
- **Where:** `renders/ch02/p028_f1.png` — caption "Фигура 5: Strategy Analysis"
- **Problem:**
  1. **Illegible.** Saved from `figsize=(14, 12)`: 1933 px at 150 dpi = 12.9 in, printed at 17.6 cm, so scale 0.538. The printed sizes:

     | Element | matplotlib size | Printed |
     |---|---:|---:|
     | Bar value labels | 9 | 4.8 pt |
     | Axis labels, ticks, legends | 10 | 5.4 pt |
     | Panel titles | 12 | 6.5 pt |
     | Suptitle | 16 | 8.6 pt |
  2. **Entirely English, and most strings cannot be translated yet.** 13 strings are missing from the mapping altogether. They are passed as function arguments, so the static extractor missed them:
     - panel titles: 'Player 1: Opening Action', 'Player 2: Response to Pass', 'Player 2: Response to Bet (fold vs call)', 'Player 1: Facing Bet After Passing'
     - axis labels: 'Player 1 Card', 'Player 2 Card'
     - legends: 'Pass', 'Bet', 'Fold (pass)', 'Call (bet)'
     - card labels: 'J (card 1)', 'Q (card 2)', 'K (card 3)'
  3. **Numbering contradicts the text.** The panels number the players 1/2; the text uses 0/1 (F02-C07). "(card 1)" leaks the code's encoding.
  4. **Layout.** The figure prints 15.9 cm tall. It no longer fits on p. 27, which is left half empty under the stranded pseudo-heading "Анализ на стратегията" (F02-X02).
  5. **Content.** The figure is *right* where the text is wrong: the bottom-left panel shows the second player calling with Q at 0.34, not 1/3 + α (F02-C01).
- **Fix:**
  - **Changes in `utils/plotting.py`, `create_strategy_charts`:**
    - `figsize=(14, 12)` → `(8, 6.6)`; `dpi` → 300.
    - Drop `suptitle`; `GridSpec(... hspace=0.4 ...)` → `hspace=0.55`.
    - Titles → 'Player 0: opening action', 'Player 1: response to a pass', 'Player 1: response to a bet', 'Player 0: facing a bet after passing'.
    - x-labels → 'Player 0 card' / 'Player 1 card'; `card_labels = ['J', 'Q', 'K']`.
  - **Changes in `_bar_chart`:**
    - Value labels `fontsize=9` → `9.6`.
    - `ax.set_title(title, fontsize=10.5)`; `ax.tick_params(labelsize=10)`; x and y labels at fontsize 10.
    - `ax.legend(fontsize=9.6, loc='upper center', ncol=2)`; `ax.set_ylim(0, 1.3)`.
    - At about 7.9 in saved width the scale becomes ≈ 0.88, so 9.6 → 8.4 pt and 10 → 8.8 pt.
  - **Plot from `cfr_results.json`** via the `__main__` in F02-G02. This figure then needs no re-training and its numbers do not change.
  - **Mapping, new keys:**

    | EN | BG |
    |---|---|
    | 'Player 0: opening action' | 'Играч 0: първо действие' |
    | 'Player 1: response to a pass' | 'Играч 1: отговор на пас' |
    | 'Player 1: response to a bet' | 'Играч 1: отговор на залог' |
    | 'Player 0: facing a bet after passing' | 'Играч 0: срещу залог след пас' |
    | 'Player 0 card' | 'Карта на Играч 0' |
    | 'Player 1 card' | 'Карта на Играч 1' |
    | 'Pass' | 'Пас' |
    | 'Bet' | 'Залог' |
    | 'Fold (pass)' | 'Отказ (пас)' |
    | 'Call (bet)' | 'Плащане (залог)' |
  - Re-render and link `strategy_analysis_bg.png`.

## B — Bulgarian language

### F02-B01 · S1 · English left in the text (heading, formula, one-pager formulas)
- **Where:** summaryBg.md § 2.1 heading (also in the TOC and bookmarks); § "Напасване на съжалението - Градивният елемент" formula; onePagerBg.md "Ключови резултати"
- **Now → Proposed:**
  - "## От single-agent RL към многоагентно стратегическо взаимодействие" → "## От обучение с подкрепление с един агент към многоагентно стратегическо взаимодействие"
  - "\text{if } \sum > 0" → "\text{ако } \sum > 0"
  - "\text{otherwise}" → "\text{в противен случай}"
  - onePagerBg: "`P(bet | K) = 3*alpha`" → "$P(\text{залог} \mid K) = 3\alpha$"
  - onePagerBg: "`alpha = 0.1941`" → "$\alpha = 0.1941$"; "`1/3 + alpha = 0.5274`" → "$1/3 + \alpha = 0.5274$"; "(параметризирано чрез `alpha` в `[0, 1/3]`)" → "(параметризирано с $\alpha \in [0, 1/3]$)"
- **Why:**
  - All of these print.
  - The heading comes from the settled entry "single-agent rl → single-agent RL" (F02-T02). The proposal uses the settled "single-agent reinforcement learning → обучение с подкрепление с един агент".
  - "TD error" and "PPAD-complete" are fixed in F02-C11 and F02-S03.
  - Cyrillic inside `\text{}` needs a check on the first rebuild (as F07-B08).

### F02-B02 · S1 · meaning — "двуигров" (two-*game*) for two-player; "n-играчни" (new T01; candidate comment p. 27 only partly applied)
- **Where:** summaryBg.md § "Теорема за минимакс", § "Равновесие на Наш", § "Напасване на съжалението…"; onePagerBg.md "Проблем.", "Отворени въпроси."
- **EN:** "for two-player zero-sum games" / "for every finite, two-player, zero-sum game" / "In a two-player zero-sum game" / "(N-player games)" / "in a 3-player game"
- **Now → Proposed:**
  - "представлява фундаментална концепция на решение за двуигрови игри с нулева сума" → "представлява основна концепция за решение на игрите за двама играчи с нулева сума"
  - "за всяка крайна двуигрова игра с нулева сума съществува стратегия и за двамата играчи" → "за всяка крайна игра за двама играчи с нулева сума съществува стратегия за всеки от двамата"
  - "в конкретния случай на двуигрови игри с нулева сума минимаксен стратегически профил" → "в частния случай на игрите за двама играчи с нулева сума минимаксният стратегически профил"
  - "В **двуигрови игра с нулева сума**" → "В игра за двама играчи с нулева сума"
  - "(n-играчни игри)" → "(игри с N играчи)"
  - "играенето на Нашева стратегия в 3-играчна игра не предпазва" → "играта по равновесна стратегия в игра с трима играчи не предпазва"
  - onePagerBg: "Двуигровите игри с нулева сума с непълна информация изискват" → "Игрите за двама играчи с нулева сума и непълна информация изискват"
  - onePagerBg: "при n-играчни или игри с обща сума" → "в игри с N играчи или с обща сума"
- **Why:**
  - "двуигров" reads as "two-game". "двуигрови игра" also breaks number agreement.
  - The candidate's comment on p. 27 ("игри а двама") was applied only at the marked place ("За игри за двама").
  - "3-играчна" and "n-играчни" are calques. The settled glossary itself has "игра с n играчи".

### F02-B03 · S1 · terminology/meaning — "нормални / разширени / екстензивна" for normal-/extensive-form games
- **Where:** summaryBg.md § 2.1, § 2.2 heading (TOC), § 2.6
- **EN:** "begins with **normal-form games** … extends to **extensive-form games**" / "## Extensive-Form Games and Information Sets" / "extends regret matching to extensive-form games"
- **Now → Proposed:**
  - "Формализацията започва с **нормални игри** (едновременни ходове, като камък-ножица-хартия) и стига до **разширени игри**" → "Формализацията започва с **игрите в нормална форма** (едновременни ходове, като камък-ножица-хартия) и стига до **игрите в разгърната форма**"
  - "## Разширени игри и информационни множества" → "## Игри в разгърната форма и информационни множества"
  - "към игри в екстензивна форма" → "към игрите в разгърната форма"
  - "И в двата случая концепцията на решение се измества" → "И в двата случая концепцията за решение се измества"
- **Why:**
  - "нормални игри" means ordinary games, and "разширени игри" means extended games. Both glossaries have "игра в нормална форма" / "игра в разгърната форма", and § 2.2's own first sentence uses "Игра в разгърната форма", so the chapter uses three names for one concept.
  - The candidate's "и стига до" comment was applied but kept the wrong term.
  - Solution concept: the one-pager already says "концепция за решение".

### F02-B04 · S1 · meaning — *call* and *fold* in the Kuhn equilibrium and elsewhere (F07-T02, new T03)
- **Where:** summaryBg.md § "Кун покер - Най-простото изпитателно поле" (p. 24), §§ 2.2, 2.7, 2.9, fig. 5 description; onePagerBg.md "Ключови резултати"
- **EN:** "If facing bet after passing, always fold." / "call with probability $1/3 + \alpha$" / "always call" / "After bet, always fold." / "Always bet, always call." / "(call probability)" / "indifferent between call and fold" / "can always call with Q" / "bluff/call ratios" / "King bets and calls at >= 0.9999, Jack folds to a bet at 0.99998, Queen passes at the root at 0.99993 — while the mixing sits 0.002-0.011 off the closed form"
- **Now → Proposed:**
  - "Ако се изправи срещу залог след пас, винаги пас." → "Ако след пас срещне залог, винаги се отказва."
  - "Ако се изправи срещу залог след пас, залог с вероятност $1/3 + \alpha$." → "Ако след пас срещне залог, плаща с вероятност $1/3 + \alpha$."
  - "Ако се изправи срещу залог след пас, винаги залог." → "Ако след пас срещне залог, винаги плаща."
  - "След залог - винаги пас." → "След залог - винаги се отказва."
  - "След залог - залог с вероятност $1/3 + \alpha$." → "След залог - плаща с вероятност 1/3." (value corrected, F02-C01)
  - "Винаги залог, винаги залог." → "Винаги залага и винаги плаща."
  - "(вероятност за залог) и в двата случая" → "(вероятност за плащане) и в двата случая"
  - "безразличие (Q е безразличен между залог и пас в определени информационни множества)" → "безразличие (с Q играчът е безразличен между плащане и отказ в определени информационни множества)"
  - "Играч 0 винаги може да колне с Дама и да реализира печалба." → "Играч 0 може винаги да плаща с Дама и да печели."
  - "точните съотношения между блъф и залог" → "точните съотношения между блъф и плащане"
  - "оптималните честоти на **блъфиране** и **колване**" → "оптималните честоти на блъфиране и плащане" (this paragraph is deleted if F02-G01 is applied)
  - onePagerBg: "Поп залага и плаща на **>= 0.9999**, Вале пасува при залог на **0.99998**, Дама предава в корена на **0.99993** - докато смесването е **0.002–0.011** извън затворената форма" → "С Поп играчът залага и плаща с вероятност **>= 0.9999**, с Вале се отказва при залог с вероятност **0.99998**, а с Дама пасува при първия ход с вероятност **0.99993** - докато смесените честоти се отклоняват с **0.002–0.011** от затворената форма"
- **Why:**
  - With call = "залог", *bet* and *call* become the same word. "Винаги залог, винаги залог" and "след залог - залог" are nonsense to a reader.
  - "пас" for *fold* collides with the Kuhn action *pass*.
  - "колне/колване" is slang.
  - "Дама предава" means "the Queen hands over/betrays". "на 0.99998" is not a way to state a probability.

### F02-B05 · S1 · meaning — one-pager turns the first-mover disadvantage into an advantage
- **Where:** onePagerBg.md "Ключови резултати" — "възпроизвежда структурното първоначално предимство на Играч 0"
- **EN:** "reproducing Player 0's structural first-mover disadvantage"
- **Now → Proposed:** "възпроизвежда структурното първоначално предимство на Играч 0" → "възпроизвежда структурно неблагоприятното положение на Играч 0, който действа пръв"
- **Why:** "предимство" means advantage. The value −1/18 is a loss for Player 0, and the summary itself says "структурно неблагоприятна позиция".

### F02-B06 · S2 · terminology — "Нашев/Неш" forms (F07-T13; candidate comment "това", p. 30, only partly applied)
- **Where:** summaryBg.md §§ 2.4, 2.7, 2.8, 2.9 heading (TOC), footnote `chen2006`
- **Now → Proposed:**
  - "При Нашевото равновесие очакваната печалба" → "При това равновесие очакваната печалба" (the candidate's own wording)
  - "Играенето на Нашева стратегия гарантира поне стойността на играта" → "Равновесната стратегия гарантира поне стойността на играта"
  - "честотите на блъфиране в Нашево равновесие могат" → "честотите на блъфиране в равновесие на Наш могат"
  - "## Експлоатируемост - Мярка за отклонение от Нашево равновесие" → "## Експлоатируемост - мярка за отклонението от равновесието на Наш"
  - "За приблизителни равновесия по Наш експлоатируемостта" → "За приблизителни равновесия на Наш експлоатируемостта"
  - "аналитични извеждания на **Нашево равновесие** за опростени **покер** игри" → "аналитично извеждане на равновесия на Наш за опростени варианти на покер"
- **Why:**
  - The chapter uses four forms: "равновесие на Наш", "Нашево", "по Наш", "Неш".
  - The glossary form is "равновесие на Наш". "Нашево/Нашева" is the unusual adjective noted in F07-T13.
  - The candidate's comment asked for "това" in place of "нашето"; the fix produced "Нашевото".
  - The "Неш" occurrence in § 2.10 is fixed in F02-C13.

### F02-B07 · S2 · terminology — CFR and game-tree vocabulary
- **Where:** summaryBg.md §§ 2.2, 2.5, 2.6; onePagerBg.md "Подход."
- **Now → Proposed:**
  - "Ръбовете обозначават действия, а крайните възли съдържат изплащанията за всеки играч." → "Ребрата обозначават действия, а крайните възли съдържат печалбите на всеки играч."
  - "в своите **решаващи точки**" → "в своите точки на вземане на решение"
  - "**Алгоритъм (обикновен вариант на CFR с вероятностна извадка):**" → see F02-C05
  - "а. Направете вероятностна извадка на случайно раздаване на карти (вероятностна извадка)." → "а) Изтеглете случайно раздаване на картите (извадка на случайните събития)." (list marker: F02-X01)
  - "г. За всяко действие рекурсивно влезте в поддървото (отрицавайки полезността за игра с нулева сума)." → "г) За всяко действие рекурсивно обходете поддървото (като смените знака на полезността, тъй като играта е с нулева сума)."
  - onePagerBg: "рекурсивно контрафактично обхождане с напасване на съжалението и вероятностна извадка" → "рекурсивно контрафактично обхождане с напасване на съжалението и извадка на случайните събития"
- **Why:**
  - A graph edge is "ребро"; "ръб" is the edge of an object.
  - Glossary: payoff → "печалба".
  - "решаващи точки" means *decisive* points; § 2.5 itself says "точка на вземане на решение".
  - "отрицавайки" means "denying"; *negating* here is a sign change.
  - "вероятностна извадка" is the statistical *probability sample* and loses *chance*. The curated glossary has chance node → "възел на случайността". Also fix the settled entry "chance sampling → вероятностна извадка", which is used only in this chapter.

### F02-B08 · S2 · meaning — "в средноаритметичен смисъл"
- **Where:** summaryBg.md § 2.2 — "което да работи добре *в средноаритметичен смисъл* за всички състояния"
- **EN:** "you must pick one action that works well *on average* across all states in the information set"
- **Now → Proposed:** "което да работи добре *в средноаритметичен смисъл* за всички състояния" → "което да работи добре *средно* за всички състояния"
- **Why:** The average here is weighted by the probability of each state, not an arithmetic mean. The BG adds a false precision.

### F02-B09 · S2 · one-pager — calques, non-words, "предсказвач" in the omniscient sense (candidate comment p. 31 applied only in the summary)
- **Where:** onePagerBg.md "Подход.", "Ключови резултати", "Връзка с дисертацията.", "Отворени въпроси."
- **Now → Proposed:**
  - "тъй като „предсказвач“ най-добър отговор за всяко състояние *не е* най-добрият отговор; най-добрият отговарящ трябва да се ангажира с едно действие на информационно множество." → "тъй като „най-добрият отговор“, избран поотделно за всяко състояние със знание за картата на противника, *не е* истински най-добър отговор: играчът трябва да избере едно действие за цялото информационно множество."
  - "достатъчно малък, за да има равновесие *семейство* в затворена форма" → "достатъчно малък, за да има *семейство* от равновесия в затворена форма"
  - "Обучен за 100,000 итерации, с OpenSpiel скрипт за кръстосана проверка." → "Обучен със 100,000 итерации; към него има и скрипт за кръстосана проверка с OpenSpiel."
  - "*Чистите решения сходяват бързо; смесените честоти носят O(1/sqrt(T)) опашката.*" → "*Чистите решения се установяват бързо; бавната опашка O(1/sqrt(T)) е в смесените честоти.*"
  - "*Скорост на сходимост е теоретичната.*" → "*Скоростта на сходимост съответства на теоретичната.*" (also F02-C09)
  - "все още може да се усредни близо до `-1/18`" → "може да дава средна стойност близо до `-1/18`"
  - "Равновесието на Наш е отправната точка, от която тази дисертация се стреми да надгради" → "Равновесието на Наш е отправната точка, от която дисертацията цели да се отдалечи"
  - "се използва като буквален предсказвач в Глави 7–10" → "се използва без промени като предсказвач за най-добър отговор в Глави 7–10"
  - "Защо *средната* стратегия сходи, когато текущата не го прави" → "Защо *средната* стратегия клони към равновесие, а текущата - не"
  - "така че този точен алгоритъм вече е извън възможностите само една игра по-нагоре" → "така че този точен алгоритъм става непосилен още за следващата по големина игра"
- **Why:**
  - The candidate's own rule (curated glossary): the *oracle value* in the omniscient sense is not "предсказвач". The summary was fixed on this point (comment p. 31); the one-pager was not.
  - "сходяват/сходи" are not Bulgarian verbs for *converge* (cf. F07-B03).
  - "равновесие *семейство*" and "OpenSpiel скрипт" keep English word order.
  - "Скорост на сходимост е" lacks the article.
  - "надгради от" is a wrong collocation (*to leave* ≠ *to build on*).
  - "буквален предсказвач" and "една игра по-нагоре" are literal calques.

### F02-B10 · S2 · meaning — "полуулични и пълни модели"
- **Where:** summaryBg.md § "Математиката на покера" — "Техните полуулични и пълни модели изграждат интуиция"
- **EN:** "Their half-street and full-street models build intuition"
- **Now → Proposed:** "Техните полуулични и пълни модели изграждат интуиция" → "Техните модели с половин и с пълен рунд на залагане (half-street и full-street) изграждат интуиция"
- **Why:**
  - "полуулични" reads as "half-street" in the urban sense, and "пълни модели" (complete models) loses *full-street*.
  - A *street* is a betting round. English in parentheses follows the first-mention rule of `terminology_EN_BG.md`.
  - Also fix the settled entry "half-street models → модели на наполовина улица".

### F02-B11 · S2 · grammar — "със" in a heading
- **Where:** summaryBg.md § 2.10 heading (TOC)
- **Now → Proposed:** "## Връзки със глава 1 и бъдещи насоки" → "## Връзки с Глава 1 и бъдещи насоки"
- **Why:** "със" is used only before с/з. The rest of the chapter capitalizes "Глава".

### F02-B12 · S2 · calques and unnatural constructions
- **Where:** summaryBg.md §§ 2.3, 2.6, 2.7, 2.8, 2.9, 2.10
- **Now → Proposed:**
  - "(J залага, въпреки че държи най-слабата карта)" → "(с J се залага, въпреки че е най-слабата карта)"
  - "Представете си Кун стратегия, при която Играч 1 винаги блъфира с Вале (вместо 1/3 от времето)." → "Представете си стратегия за Кун покер, при която Играч 1 винаги блъфира с Вале (вместо в 1/3 от случаите)."
  - "Претеглянето с $\pi_{-i}$ осигурява съжалението да бъде пропорционално на честотата" → "Претеглянето с $\pi_{-i}$ прави съжалението пропорционално на честотата"
  - "защита срещу всяка експлоатативна стратегия" → "защита срещу всяка експлоатираща стратегия"
  - "може да съответства на множество различни основни състояния на играта." → "може да съответства на много различни действителни състояния на играта."
  - "който взема проби от части на дървото" → "който обхожда само извадка от дървото"
- **Why:**
  - A card does not "hold" a card.
  - "Кун стратегия" and "1/3 от времето" copy English word order and idiom.
  - "осигурява … да бъде" is a calque of *ensures that*.
  - "експлоатативен" is a calque; "основни" (basic) is not *underlying*; "взема проби" suggests lab samples.

### F02-B13 · S3 · typography — "&" in running text; capitals after a dash in headings
- **Where:** summaryBg.md §§ 2.5, 2.8 (TOC)
- **Now → Proposed:**
  - "Харт & Мас-Колел (2000)" → "Харт и Мас-Колел (2000)"
  - "## Напасване на съжалението - Градивният елемент" → "## Напасване на съжалението - градивният елемент"
  - "## Кун покер - Най-простото изпитателно поле" → "## Кун покер - най-простото изпитателно поле"
- **Why:** The capitals are English title case. The § 2.9 heading is in F02-B06.

## T — Glossary-level terminology

### F02-T01 · S1 · "two-player → двуигрови"; n-player entries
- **Where:** `llmPipeline/glossary_settled.md`:
  - "two-player → двуигрови"
  - "n-player → n-играчeн": the "e" is **Latin** (bytes `…\321\207 e \320\275`)
  - "N-player settings → N-игрова среда"
  - "N-player bound → N-играторска граница"

  "двуигров" prints in: summaryBg 02 (4×), 05, 06 (19 lines), 08 (2), 09 (3), 11; onePagerBg 06 (2), 08, 09 (2), 11.
- **Now → Proposed:**
  - two-player → "за двама играчи" (postposed: "игра за двама играчи"; the settled entries "two-player zero-sum → игра за двама с нулева сума" already do this).
  - n-player / N-player → "с N играчи" ("игра с N играчи", "при N играчи").
  - Delete the three N-player variants.
- **Why:**
  - "двуигров" means "two-game", and "N-игрова среда" means "an N-game environment".
  - Step 06 alone prints the wrong form 19 times.
  - The Latin letter breaks search and hyphenation.

### F02-T02 · S1 · settled "translations" that are English
- **Where:** `glossary_settled.md`:

  | Entry | Where it prints |
  |---|---|
  | "single-agent rl → single-agent RL" | step 02 heading; step 09 (4 lines) |
  | "td error → TD error" | step 02 § 2.10 |
  | "ppad-complete → PPAD-complete" | step 02 § 2.4 |
  | "vanilla counterfactual regret minimization → Vanilla Counterfactual Regret Minimization" | report_bg.md, twice |
  | "n-player egta evaluation framework → n-player EGTA evaluation framework" | not checked |
- **Now → Proposed:**
  - single-agent RL → "обучение с подкрепление с един агент" (a settled entry for the long form already exists)
  - TD error → "TD грешка"
  - PPAD-complete → "PPAD-пълен" (as in "NP-пълна задача")
  - vanilla CFR (long form) → "обикновен вариант на CFR" (the short-form entry already says so)
  - n-player EGTA evaluation framework → "рамка за оценяване с EGTA при N играчи"
- **Why:** The picker accepted English as the Bulgarian, so the pipeline pastes it into print unchanged. Abbreviations stay Latin; the words around them do not.

### F02-T03 · S2 · "fold → пас"
- **Where:** `glossary_settled.md` "fold → пас" (freq 5); printed "винаги пас" for *always fold* in steps 02 (3), 07, 08. Also note F07-T02 (call → залог).
- **Now → Proposed:** fold → "отказ"; verb "се отказва" (step 07 already writes "се отказва от всичко останало")
- **Why:** In Kuhn poker *pass* (the action p) is "пас". With fold also "пас", "след залог - винаги пас" cannot be told apart from a check, and the equilibrium list becomes ambiguous (F02-B04).

### F02-T04 · S3 · counterfactual: the two glossaries disagree
- **Where:**
  - curated `terminology_EN_BG.md`: "Counterfactual value → Контрафактуална стойност", "CFR → Минимизиране на контрафактуалното съжаление"
  - settled: "counterfactual regret minimization → минимизиране на контрафактичното съжаление" (freq 27)
  - The corpus prints "контрафактичн-" in about 37 lines (steps 01–11) and "контрафактуалн-" once (step 06).
- **Now → Proposed:** keep "контрафактичен" (what readers see everywhere) and change the two curated rows, or else change 37 lines. Either way, one form.
- **Why:** One concept, one word, across the bundle.

## C — Content

### F02-C01 · S1 · The second player's Queen call probability is 1/3, not 1/3 + α
- **Where:** summaryEn.md § "Kuhn Poker — The Simplest Testbed" — "- **Player 1 with Q:** After pass, always pass. After bet, call with probability $1/3 + \alpha$."; summaryBg.md (fixed in F02-B04)
- **Problem:** In Kuhn's solution only the first player's strategy depends on α. The second player's strategy is unique: with Q it calls a bet with probability exactly 1/3. Checks:
  - **Indifference.** Player 0's Jack is indifferent between bluffing and checking only if Q calls 1/3.
  - **Chapter's own data.** Fig. 5 (bottom-left panel: 0.34) and `models/cfr_results.json` ("2b": p_bet = 0.3353).
  - **Exact computation.** A profile with 1/3 + α at "2b" has NashConv 0.032, so it is not an equilibrium (computed in this review with an exact traversal of `cfr_results.json`).
  - **Wikipedia's Kuhn poker page** states the same.
- **Now → Proposed:**
  - EN: "After bet, call with probability $1/3 + \alpha$." (second occurrence, Player 1 row) → "After bet, call with probability 1/3."
  - Add after the list, EN: "(Player 1's strategy is the same in every equilibrium; only Player 0's depends on α.)"
  - Add after the list, BG: "(Стратегията на Играч 1 е една и съща във всички равновесия; от $\alpha$ зависи само стратегията на Играч 0.)"

### F02-C02 · S1 · Regret matching: average regret vanishes at O(1/√T), not O(√T)
- **Where:** summaryBg.md § 2.5 — "средното **съжаление** се сближава към нула със скорост $O(\sqrt{T})$"; EN "ensures average regret converges to zero at rate $O(\sqrt{T})$"
- **Problem:** $O(\sqrt{T})$ grows. The *cumulative* regret grows as $O(\sqrt{T})$, and the *average* regret falls as $O(1/\sqrt{T})$. Zinkevich et al. (2007), Theorem 4, gives the regret-matching bound $\Delta\sqrt{|A|}/\sqrt{T}$ on the average; verified in the NeurIPS proceedings PDF.
- **Now → Proposed:**
  - "средното **съжаление** се сближава към нула със скорост $O(\sqrt{T})$" → "средното съжаление клони към нула със скорост $O(1/\sqrt{T})$ (натрупаното съжаление расте не по-бързо от $O(\sqrt{T})$)"
  - EN: "converges to zero at rate $O(\sqrt{T})$" → "converges to zero at rate $O(1/\sqrt{T})$ (cumulative regret grows no faster than $O(\sqrt{T})$)"

### F02-C03 · S1 · The printed CFR bound is not Zinkevich's Theorem 4
- **Where:** summaryBg.md / summaryEn.md § 2.6 — "$$\text{exploit}(\bar{\sigma}^T) \leq O\left(\Delta\sqrt{|I|/T}\right)$$"
- **Problem:**
  - Theorem 4 (checked in the proceedings PDF): "$R^T_i \le \Delta_{u,i}|\mathcal{I}_i|\sqrt{|A_i|}/\sqrt{T}$". The paper adds: "the bound on the average overall regret is linear in the number of information sets."
  - Theorem 2: the average profile is a 2ε-equilibrium.
  - With the chapter's definition exploit = BR₀ + BR₁, exploit(σ̄ᵀ) = R₀ᵀ + R₁ᵀ ≤ Δ|𝓘|√|A|/√T.
  - The printed √|I| form is not in the paper. Lanctot et al. (2009) later proved a tighter bound (NeurIPS abstract).
- **Now → Proposed:**
  - "$$\text{exploit}(\bar{\sigma}^T) \leq O\left(\Delta\sqrt{|I|/T}\right)$$" → "$$\text{exploit}(\bar{\sigma}^T) \leq \frac{\Delta\,|\mathcal{I}|\,\sqrt{|A|}}{\sqrt{T}}$$" (both files)
  - "където $\Delta$ е максималният диапазон на печалбите, а $|I|$ - броят на информационните множества.[^zinkevich2007]" → "където $\Delta$ е обхватът на печалбите, $|\mathcal{I}|$ - броят на информационните множества на двамата играчи, а $|A|$ - най-големият брой действия в едно информационно множество.[^zinkevich2007] Границата е линейна по $|\mathcal{I}|$; по-късно е доказана и по-тясна граница.[^lanctot2009]"
  - EN: "where $\Delta$ is the maximum payoff range and $|I|$ is the number of information sets.[^zinkevich2007]" → "where $\Delta$ is the range of payoffs, $|\mathcal{I}|$ the number of information sets of both players and $|A|$ the largest number of actions at an information set.[^zinkevich2007] The bound is linear in $|\mathcal{I}|$; a tighter bound was proved later.[^lanctot2009]"
  - New footnote (both files): `[^lanctot2009]: Lanctot, M., Waugh, K., Zinkevich, M. & Bowling, M. (2009). "Monte Carlo Sampling for Regret Minimization in Extensive Games." *Advances in Neural Information Processing Systems 22*, 1078–1086.`

### F02-C04 · S1 · Stale "Chapter 14"
- **Where:** summaryBg.md § 2.9 callout — "Глава 14 изгражда обща рамка за оценяване около нея."; onePagerBg.md — "е показателят, който се пренася в Глави 7–8 и 14."; EN equivalents
- **Now → Proposed:**
  - "Глава 14 изгражда обща рамка за оценяване около нея." → "Тя е и отправната точка на методологията за оценяване в дисертацията (Принос №3)."
  - EN: "Chapter 14 builds a general evaluation framework around it." → "It is also the starting point of the thesis's evaluation methodology (Contribution #3)."
  - onePagerBg: "е показателят, който се пренася в Глави 7–8 и 14." → "е показателят, който се пренася в Глави 7–8 и в методологията за оценяване (Принос №3)."
  - onePager EN: "carried forward into Chapters 7-8 and 14." → "carried forward into Chapters 7-8 and into the evaluation methodology (Contribution #3)."
- **Why:** Chapters 13–15 were never written.

### F02-C05 · S2 · The implementation is chance-sampled CFR, not "vanilla" full-tree CFR
- **Where:** summaryBg.md § 2.6 algorithm title, § 2.10 "Напред"; onePagerBg.md "Подход.", "Отворени въпроси."; EN equivalents
- **Problem:**
  - `cfr_trainer.py` shuffles the cards each iteration ("Uses chance sampling"), following Neller & Lanctot. The tutorial says "when we use CFR, we specifically refer to chance-sampled CFR" (PDF read). Each iteration therefore visits 4 of Kuhn's 12 information sets.
  - This contradicts "every information set is visited every iteration".
  - Lanctot et al. (2009) show that chance sampling is a special case of MCCFR, so "Chapter 3 introduces sampling" is only half true.
  - "vanilla CFR" normally means the unsampled algorithm.
- **Now → Proposed:**
  - "**Алгоритъм (обикновен вариант на CFR с вероятностна извадка):**" → "**Алгоритъм (CFR с извадка на случайните събития, по Neller и Lanctot, 2013[^neller2013]):**"
  - EN: "**Algorithm (vanilla CFR with chance sampling):**" → "**Algorithm (CFR with chance sampling, as in Neller & Lanctot, 2013[^neller2013]):**"
  - "Глава 2 разглежда CFR с *пълно обхождане на дърво* - всяко информационно множество се посещава при всяка итерация. При по-големи игри това е неразрешим проблем." → "Реализацията в тази глава изтегля по едно раздаване на картите на итерация (извадка на случайните събития), но обхожда всички последователности от действия за него, така че всяка итерация пак засяга голяма част от дървото. При по-големи игри дори това е изчислително непосилно."
  - EN: "Chapter 2 covers *full tree traversal* CFR — every information set is visited every iteration. For larger games, this is intractable." → "The implementation here samples one card deal per iteration (chance sampling) but traverses every action sequence of that deal, so each iteration still touches a large part of the tree. For larger games even this is too expensive."
  - onePagerBg: "Обикновен вариант на CFR, написан от нулата за **Кун покер**" → "CFR с извадка на случайните събития, написан от нулата за **Кун покер**"; EN "Vanilla CFR written from scratch" → "Chance-sampled CFR written from scratch"
  - onePagerBg: "А пълното обхождане на дърво засяга всяко информационно множество при всяка итерация" → "А дори с по едно изтеглено раздаване на итерация CFR обхожда всички последователности от действия"; EN "full-tree traversal touches every information set on every iteration" → "even with one sampled deal per iteration, CFR traverses every action sequence of that deal"
- **Note:** Also fixes "неразрешим" (F07-T06). report_en/bg "Vanilla Counterfactual Regret Minimization" likewise.

### F02-C06 · S2 · "Game value −0.0602" is a noisy running mean, not the value of the output strategy
- **Where:** onePagerBg.md / onePager.md "Ключови резултати" / "Key results"; report_en/bg § 2; fig. 3 and its description
- **Problem:**
  - `KuhnTrainer.train` returns `cumulative_util / iterations`: the mean root payoff of the *sampled deals* under the *current* strategies, averaged from iteration 1.
  - Its standard error at 100 000 iterations is ≈ 0.004 (payoff SD 1.29 under the final profile), so −0.0602 is 1.1 SE from −1/18.
  - The value of the *average* strategy saved in `cfr_results.json`, computed exactly in this review, is **−0.05549**: 6.8·10⁻⁵ from −1/18, with NashConv 0.0043.
  - The one-pager undersells the result and labels the wrong quantity.
- **Now → Proposed:**
  - onePagerBg: "*Стойност на играта* **-0.0602**, измерена спрямо точната **-1/18 = -0.0556** при 100k итерации," → "*Стойност на играта* на средната стратегия **-0.0555** при точна стойност **-1/18 = -0.0556** (текущата средна на изтеглените печалби за всичките 100k итерации е **-0.0602**),"
  - EN: "*Game value* **-0.0602** measured against the exact **-1/18 = -0.0556** at 100k iterations," → "*Game value* of the average strategy **-0.0555** against the exact **-1/18 = -0.0556** (the running mean of sampled payoffs over all 100k iterations is **-0.0602**),"
- **Before applying:** add a print of the exact value to `evaluate/exploitability.py`: `_evaluate` of the average profile over `ALL_DEALS`, as `best_response.py` already does for pure strategies. Confirm −0.0555 there; the number above is the reviewer's own computation.

### F02-C07 · S2 · Player numbering switches between 0/1 and 1/2
- **Where:** summaryBg.md § 2.4 "Смесени стратегии", § 2.8 "Защо Кун е важен"; figs. 3 and 5 (F02-G02, G04)
- **Problem:** The rules, the equilibrium list and § 2.9 use Player 0 / Player 1. Two sentences and both figures use 1/2, so "Player 2" and "Player 1" each point to two different people.
- **Now → Proposed:**
  - "изисква Играч 2 да блъфира с Вале точно 1/3 от времето" → "изисква Играч 1 (вторият по ред) да блъфира с Вале в точно 1/3 от случаите"
  - "(Играч 2 вижда действието на Играч 1, преди да вземе своето решение)" → "(Играч 1 вижда действието на Играч 0, но не и картата му)"
  - EN: "has Player 2 bluffing with Jack exactly 1/3 of the time" → "has Player 1 (the second to act) bluffing with Jack exactly 1/3 of the time"
  - EN: "(Player 2 sees Player 1's action before deciding)" → "(Player 1 sees Player 0's action but not their card)"

### F02-C08 · S2 · Minimax paragraph: the theorem says the two values are *always* equal; it is not an algorithm
- **Where:** summaryBg.md § 2.3; EN "When these two values equal, the game is in equilibrium. This algorithm directly relates to Nash Equilibrium:"
- **Problem:** "When these two values are equal…" implies they sometimes are not. The content of the theorem is that, in mixed strategies, maximin = minimax, always.
- **Now → Proposed:**
  - "Когато тези две стойности са равни, играта достига равновесие. Този алгоритъм е пряко свързан с равновесието на Наш:" → "Теоремата твърди, че при смесени стратегии тези две стойности винаги са равни; общата им стойност е стойността на играта. Теоремата е пряко свързана с равновесието на Наш:"
  - EN: "When these two values equal, the game is in equilibrium. This algorithm directly relates to Nash Equilibrium:" → "The theorem states that, with mixed strategies, these two values are always equal; their common value is the value of the game. The theorem relates directly to Nash equilibrium:"

### F02-C09 · S2 · Slope −0.489 "confirming theoretical predictions" overclaims
- **Where:** summaryBg.md § 2.9 "Скорост на сходимост"; onePagerBg.md "*Скорост на сходимост е теоретичната.*" (fixed in F02-B09); report_en/bg
- **Problem:**
  - The slope is a least-squares fit to six points. Each point comes from a separate unseeded run (`evaluate/convergence.py`), and the last point is at 50 000.
  - O(1/√T) is an upper bound, not a prediction of the rate.
  - Re-running the same code with seeds 0–4 in this review gave slopes −0.511, −0.497, −0.511, −0.601, −0.522 (mean −0.53, SD 0.04).
- **Now → Proposed:**
  - "Нашият измерен наклон беше $-0.489$, което потвърждава теоретичните предвиждания." → "Измереният наклон е $-0.489$ (по едно изпълнение за всяка от шестте контролни точки), което съответства на границата $O(1/\sqrt{T})$; тя е горна граница, а не точна прогноза за скоростта."
  - EN: "Our measured slope was $-0.489$, confirming theoretical predictions." → "Our measured slope was $-0.489$ (one run per checkpoint, six checkpoints), consistent with the $O(1/\sqrt{T})$ bound, which is an upper limit rather than a prediction of the exact rate."
  - After F02-G03's seeded re-run, replace −0.489 by the 5-seed mean ± SD.

### F02-C10 · S2 · Report: "Nash strategies to 4 decimal places … All targets achieved ✓" contradicts the measured numbers
- **Where:** report_en.md / report_bg.md header and § 2 ("converged precisely to the analytical Nash equilibrium family")
- **Problem:** `cfr_results.json` and the one-pager show the mixed frequencies 0.002–0.011 off the closed form (Q call after pass-bet 0.5387 vs 0.5274). Only the pure decisions meet 4 decimals.
- **Now → Proposed:**
  - report_bg: "**Статус:** Всички цели са постигнати ✓" → "**Статус:** Целите за стойността на играта и скоростта на сходимост са постигнати; смесените честоти са на 0.002–0.011 от затворената форма (точност до четири знака е постигната само при чистите решения)"
  - report_en: "**Status:** All targets achieved ✓" → "**Status:** Game-value and convergence-rate targets met; mixed frequencies within 0.002–0.011 of the closed form (4-decimal accuracy reached only for the pure decisions)"
  - report § 2 "converged precisely to" → "converged to within 0.011 of"

### F02-C11 · S2 · DQN "converges to optimal" overclaims (and English left in the same sentence)
- **Where:** summaryBg.md § 2.10 — "В Глава 1 DQN минимизира TD error за всяко състояние поотделно, но цялостната q-функция се сближава до оптималната."; EN "In Chapter 1, DQN minimizes TD error at each state independently, yet the overall Q-function converges to optimal."
- **Problem:**
  - DQN, with a neural network, has no convergence guarantee.
  - DQN's loss is a single network loss over a batch, not a per-state minimization.
  - The guarantee belongs to tabular Q-learning (Watkins & Dayan, 1992; Crossref: *Machine Learning* 8(3–4), 279–292).
- **Now → Proposed:**
  - "В Глава 1 DQN минимизира TD error за всяко състояние поотделно, но цялостната q-функция се сближава до оптималната." → "В Глава 1 Q-обучението намалява TD грешката за всяко състояние поотделно, но в табличния случай Q-функцията доказано се сближава до оптималната; DQN запазва правилото за обновяване, но с невронна мрежа губи тази гаранция."
  - EN: "In Chapter 1, DQN minimizes TD error at each state independently, yet the overall Q-function converges to optimal." → "In Chapter 1, Q-learning reduces the TD error one state at a time, yet in the tabular case the Q-function provably converges to the optimum; DQN keeps the update rule but, with a neural network, loses the guarantee."

### F02-C12 · S3 · Rock–paper–scissors example: Scissors' regret becomes negative, and the shift is not gradual
- **Where:** summaryBg.md § 2.5; EN "while regret for Scissors will stay at zero. Your strategy will gradually shift toward playing Paper with increasing probability"
- **Problem:**
  - Against pure Rock, the cumulative regret for Scissors becomes *negative*; only its positive part, which the strategy uses, stays zero.
  - With expected-value updates the strategy is pure Paper after the first round. With sampled updates (Neller & Lanctot § 2.3) it gets there within a few rounds.
- **Now → Proposed:**
  - "докато съжалението за **ножица** остава нула. Постепенно стратегията ви се измества към игра с **хартия** с увеличаваща се вероятност, което представлява правилният най-добър отговор." → "докато съжалението за ножица става отрицателно и не влияе на стратегията. Стратегията бързо преминава към хартия - правилният най-добър отговор."
  - EN analogously: "while regret for Scissors turns negative and has no effect on the strategy. The strategy quickly moves to Paper, the correct best response."

### F02-C13 · S2 · It is the *average* strategy that converges (§§ 2.6, 2.10); "Неш"
- **Where:** summaryBg.md § 2.6 first paragraph, § 2.10 first paragraph
- **Problem:** "the overall strategy converges" contradicts the chapter's own point (Algorithm step 3; one-pager open question) that the current strategy does not converge. § 2.10 also spells "Неш".
- **Now → Proposed:**
  - "Ако **съжалението** за всяко **информационно множество** се сближи до нула, цялостната стратегия се сближава до **равновесие на Наш**." → "Ако средното съжаление във всяко информационно множество клони към нула, цялостната *средна* стратегия клони към равновесие на Наш."
  - "но цялостната стратегия се сближава до равновесие на Неш." → "но цялостната *средна* стратегия се сближава до равновесие на Наш."
  - EN: "If each information set's regret converges to zero, the overall strategy converges to Nash equilibrium." → "If each information set's average regret converges to zero, the overall *average* strategy converges to a Nash equilibrium."
  - EN § Connections: "yet the overall strategy converges to Nash." → "yet the overall *average* strategy converges to Nash."

### F02-C14 · S2 · Exploitability: name the convention (NashConv vs OpenSpiel's half); enumeration is not "the" correct approach
- **Where:** summaryBg.md § 2.9
- **Problem:**
  - The chapter defines exploitability as BR₀ + BR₁. In two-player zero-sum games that sum equals NashConv.
  - OpenSpiel's `exploitability()` returns NashConv / num_players, i.e. half. Verified in `open_spiel/python/algorithms/exploitability.py`: "equivalent to NashConv / num_players".
  - Chapter 3 plots OpenSpiel's "Nash Conv", and the thesis compares numbers across chapters, so the factor of 2 needs to be stated once.
  - "The correct approach enumerates all 64 pure strategies" is too strong. The code's own docstring says larger games need a bottom-up traversal.
- **Now → Proposed:**
  - "…спрямо стратегията на противника." Add after this sentence: "В игра за двама играчи с нулева сума тази сума се нарича още NashConv; OpenSpiel отчита като „експлоатируемост“ половината от нея, така че стойностите по двете конвенции се различават два пъти."
  - "За Кун покер правилният подход е да се изброят всички 2⁶ = 64 чисти стратегии и да се оцени всяка една от тях." → "За Кун покер е достатъчно да се изброят всички 2⁶ = 64 чисти стратегии и да се оцени всяка от тях; при по-големи игри най-добрият отговор се изчислява с едно обхождане отдолу нагоре, което обединява стойностите по информационни множества."
  - EN: add "In a two-player zero-sum game this sum is also called NashConv; OpenSpiel reports half of it as "exploitability", so the two conventions differ by a factor of 2."; "the correct approach enumerates all 2⁶ = 64 pure strategies and evaluates each." → "a brute-force approach that enumerates all 2⁶ = 64 pure strategies suffices; larger games need a single bottom-up traversal that aggregates over information sets."

## S — Sources

### F02-S01 · S2 · SOURCE_GAPS row (the O(1/√T) caption) → cite Zinkevich 2007 in § 2.9, soften the caption
- **Where:** summaryBg.md § "Емпирични визуализации" — "Проследяването на експлоатируемостта във времето показва скорост на сходимост $O(1/\sqrt{T})$."
- **Proposal (cite + soften):**
  - § 2.9: "**Скорост на сходимост:** При обикновен вариант на CFR експлоатируемостта намалява като $O(1/\sqrt{T})$." → "**Скорост на сходимост:** Теоретично експлоатируемостта на средната стратегия на CFR намалява като $O(1/\sqrt{T})$[^zinkevich2007] (фиг. 4)."
  - Caption: "показва" → "съответства на" (done in F02-G01's caption).
  - EN analogously.
- **Verification:** Theorems 2 and 4 were read in the NeurIPS 2007 proceedings PDF (pp. 1729–1736). Theorem 4 plus Theorem 2 give the O(1/√T) rate for the average profile. For the chance-sampled variant used here, the bound holds with high probability (Lanctot et al., 2009, abstract), footnote as in F02-C03. The footnote goes in the body rather than the caption: a note inside a LaTeX `\caption` is fragile.

### F02-S02 · S2 · Shoham & Leyton-Brown footnote cites wrong sections (same text as F07-S05)
- **Where:** summaryBg.md footnote `shoham2008` — "Гл. 3–4 (игри в нормална и разгърната форма); гл. 5 (игри в разгърната форма); §3.4 (изчисляване на равновесия) и §4.6 (изчисляване на най-добри отговори) - механизмът в последователна форма под всяка линейна програма в Глава 8;"
- **Problem:** Checked against masfoundations.org/toc.html:
  - Ch. 4 is "Computing Solution Concepts of Normal-Form Games" (not extensive form).
  - §3.4 is "Further solution concepts for normal-form games".
  - §4.6 is "Computing correlated equilibria".
  - The sequence form is §5.2.3.
  - "Глава 8" is meaningless in chapter 2.
  - The relevant sections for this chapter are §3.3 (best response and Nash equilibrium; Nash's theorem), §3.4.1 "Maxmin and minmax strategies", §4.1 "Computing Nash equilibria of two-player, zero-sum games", §5.2 "Imperfect-information extensive-form games", and §7.5 "No-regret learning and universal consistency".
- **Proposal (correct, chapter-specific):**
  - BG: "Гл. 3–4 (игри в нормална и разгърната форма); гл. 5 (игри в разгърната форма); §3.4 (изчисляване на равновесия) и §4.6 (изчисляване на най-добри отговори) - механизмът в последователна форма под всяка линейна програма в Глава 8; гл. 7 "Learning and Teaching" - рамката за учене в повтарящи се игри, включително напрежението, че действията едновременно *експлоатират* и *обучават* опонента." → "Гл. 3 (игри в нормална форма; §3.3 - най-добър отговор и равновесие на Наш, §3.4.1 - максиминни и минимаксни стратегии); §4.1 (изчисляване на равновесия на Наш в игри за двама играчи с нулева сума); гл. 5 (игри в разгърната форма; §5.2 - непълна информация и информационни множества, §5.2.3 - последователната форма); §7.5 "No-regret learning and universal consistency"."
  - EN: the corresponding "Ch. 3 (games in normal form; §3.3 best response and Nash equilibrium, §3.4.1 maxmin and minmax strategies); §4.1 (computing Nash equilibria of two-player zero-sum games); Ch. 5 (extensive-form games; §5.2 imperfect information and information sets, §5.2.3 the sequence form); §7.5 "No-regret learning and universal consistency"."
- **Note:** In the bundle this footnote's markers print no note (F07-X01).

### F02-S03 · S2 · PPAD claim unsourced and imprecise
- **Where:** summaryBg.md § 2.4 — "В тези условия намирането на точно равновесие на Наш е известно като изчислително неразрешим проблем, често попадащ в класа на сложност PPAD-complete."
- **Problem:**
  - No source.
  - "known to be intractable" overstates it: PPAD-completeness is strong evidence of intractability, not proof.
  - "PPAD-complete" and "неразрешим" (F07-T06) print as they are.
- **Proposal (cite + correct):**
  - BG: "В тези условия намирането на точно равновесие на Наш е известно като изчислително неразрешим проблем, често попадащ в класа на сложност PPAD-complete." → "В тези условия изчисляването на равновесие на Наш е PPAD-пълна задача - дори при игри за двама играчи с обща сума - и затова се смята за изчислително непосилно.[^daskalakis2009][^chen2009]"
  - EN: "In these settings, finding an exact Nash equilibrium is known to be computationally intractable, often falling into the complexity class PPAD-complete." → "In these settings, computing a Nash equilibrium is PPAD-complete, even for two-player general-sum games, and is therefore believed to be intractable.[^daskalakis2009][^chen2009]"
  - `[^daskalakis2009]: Daskalakis, C., Goldberg, P. W. & Papadimitriou, C. H. (2009). "The Complexity of Computing a Nash Equilibrium." *SIAM Journal on Computing*, 39(1), 195–259.`
  - `[^chen2009]: Chen, X., Deng, X. & Teng, S.-H. (2009). "Settling the Complexity of Computing Two-Player Nash Equilibria." *Journal of the ACM*, 56(3), 1–57.`
- **Verification:** both via Crossref (DOIs 10.1137/070699652, 10.1145/1516512.1516516).

### F02-S04 · S2 · "Nash play in a 3-player game does not protect against coalitions" is unsourced
- **Where:** summaryBg.md § 2.4 — "потенциално формирайки временни коалиции, които експлоатират третия играч."
- **Proposal (cite):**
  - Append `[^szafron2013]` after "третия играч."
  - `[^szafron2013]: Szafron, D., Gibson, R. & Sturtevant, N. (2013). "A Parameterized Family of Equilibrium Profiles for Three-Player Kuhn Poker." *Proc. AAMAS 2013*, 247–254.` Add the BG gloss "В тройния Кун покер един играч може да прехвърля печалба от единия противник към другия, без да напуска семейството от равновесия."
- **Verification:** Crossref (pages) and the PDF abstract: "the ability of one player to transfer utility to a second player at the expense of the third player, while playing a strategy in the profile family". This is the chapter's claim in the paper's own setting, Kuhn poker.

### F02-S05 · S3 · `bowling2015`: marker on the wrong sentence; wording drops the paper's qualifier
- **Where:** summaryBg.md § 2.10 — "Глава 5 заменя табличните стратегии с невронни мрежи.[^bowling2015]"; footnote "първата нетривиална игра с непълна информация, която по същество е решена."
- **Problem:**
  - The note (CFR+ solving limit hold'em) is attached to the neural-network sentence.
  - The paper's claim is "no nontrivial imperfect information game played competitively by humans has previously been solved", and the game is "essentially weakly solved". Verified: Crossref (Science 347(6218), 145–149) and the abstract wording via a search snippet.
- **Proposal:**
  - Move `[^bowling2015]` to the end of the sentence "…дори това е изчислително непосилно." (F02-C05).
  - Footnote: "Използва CFR+ за решаването на хедс-ъп лимит тексаски холдем - първата нетривиална игра с непълна информация, която по същество е решена." → "С CFR+ хедс-ъп лимит тексаски холдем е решен по същество (в слаб смисъл) - първата нетривиална игра с непълна информация, играна състезателно от хора, която е решена."
  - EN likewise: "…the first non-trivial imperfect-information game played competitively by humans to be (essentially weakly) solved."

### F02-S06 · S3 · Footnote metadata; spot-check of the key citations
- **Where:** footnotes `neller2013`, `kuhn1950`
- **Findings:**
  - `neller2013` "Section 1–2": regret matching and the RPS example are §2 (§2.3–2.4), and chance-sampled CFR on Kuhn is §3 (§3.4). Proposed: "…," §2–3 (version of 9 July 2013)". Read in the PDF; venue (Model AI Assignments, EAAI) not verified.
  - `kuhn1950`: add "Annals of Mathematics Studies 24, Princeton University Press, 97–103" (De Gruyter chapter listing via search).
  - **Checked correct via Crossref:** `vonneumann1928` (Math. Ann. 100(1), 295–320), `nash1950` (PNAS 36(1), 48–49), `blackwell1956` (PJM 6(1), 1–8), `hartmascolell2000` (Econometrica 68(5), 1127–1150).
  - **Checked correct against the proceedings PDF:** `zinkevich2007` (NIPS 20, 1729–1736; Theorem 4 exists, but the printed formula is wrong, F02-C03).
  - `chen2006` not checked.

## X — Structure

### F02-X01 · S2 · Two lists print as run-on paragraphs
- **Where:**
  - summaryBg.md and summaryEn.md § 2.4 "**Ключови свойства:**" / "**Key properties:**": bundle p. 21 prints "Ключови свойства: - Съществуване: … - Единственост: … - Смесени стратегии: …".
  - summaryBg.md § 2.6 algorithm step 2: p. 23 prints "а. Направете … б. Рекурсивно … в. …" as one paragraph.
- **Problem:**
  - Pandoc needs a blank line before a list. The fix of 7 April (commit 1dac0c1) was lost in the July retranslation.
  - Cyrillic "а." / "б." are not list markers, so the sub-steps that render correctly in EN collapse in BG.
- **Fix:**
  - Insert an empty line after "**Ключови свойства:**" and after "**Key properties:**".
  - In summaryBg.md turn each sub-step into a bullet: "   а. " → "   - а) ", "   б. " → "   - б) ", …, "   е. " → "   - е) ".
  - Optional: `check_headings.py`-style guard: fail the build if a line starting with "- **" follows a non-blank, non-list line.

### F02-X02 · S2 · Figure descriptions, pseudo-headings and references (candidate comment p. 32 only partly applied)
- **Where:** summaryBg.md § "Емпирични визуализации" (pp. 26–28)
- **Problem:**
  - The candidate asked that each description sit under its image and that the figures be referred to as "фигура N". Now each figure has a bold pseudo-heading, the English caption, and a separate italic paragraph. No sentence refers to a figure by number.
  - The pseudo-heading "Анализ на стратегията" is stranded at the foot of p. 27, above half a blank page; fig. 5 is on p. 28.
- **Fix:**
  - Apply F02-G01, which puts the description into the caption, and delete the three bold lines "**Сходимост на стойността на играта**", "**Сходимост на експлоатируемостта**", "**Анализ на стратегията**", plus their EN twins.
  - Refer to the figures from the text: § 2.9 "Скорост на сходимост" "(фиг. 4)" (F02-S01); after the Kuhn equilibrium list "(фиг. 5)"; after "Стойност на играта" "(фиг. 3)".
  - The bundle numbers figures globally (3–5), while the standalone summary starts at 1. Stable "фиг. 2.1–2.3" needs one central build change: `\counterwithin{figure}{section}` (the chapter is a level-1 section) in the LaTeX header used by `build_reports.py`. Until then, "(фигурата по-долу)" is safe.
