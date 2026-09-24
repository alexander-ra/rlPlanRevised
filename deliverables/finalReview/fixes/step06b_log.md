# Step 06b — fixes applied (ReBeL, Student of Games, Synthesis; figs. 27–30)

Applied: 95 · Skipped: 1 · Central: 18
(G 6 · B 53 · C 14 · S 20 · X 2 applied; B28 skipped; T01–T14 central — their occurrences in this half are applied through the B items)

Files: `summaryEn.md` / `summaryBg.md` from "## ReBeL (2020)" to the end (incl. the shared footnote block), `make_{rebel,sog,evolution,reuse}_figure.py`, `_diagram_utils.py` (one new option), the eight PNGs of figs. 27–30, `fixes/labels_step06.json` (06a's 42 entries kept, 58 added). Scripts (scratchpad `s06b/`): `apply_bg.py` (267 exact replacements, every one matched once, then case-sensitive replace-alls B05/B07/1.22 on this half only), `apply_bg2.py` (16 hand fixes after reading the result), `apply_en.py` (61 whitespace-tolerant replacements, all matched), `labels.py` (overlay entries).

## Deviations from the review's exact proposals (intent kept)
- **Row 2.3 (self-play) untouched**, so B28 is skipped: "самообучение" stays; only its word-order fixes were applied where "самоигра" was already the word ("обучение с подкрепление чрез самоигра"). Proposals that introduced "самоигра"/"игра срещу себе си" (B20, B32, B44, B53, S14, G02/G03 labels) were written with the current "самообучение", avoiding the "обучение чрез самообучение" tautology where possible. **Row 1.10 (blueprint)** kept "план" (C09's "безопасна базова стратегия" → "безопасния план").
- **Glossary rows win over the review:** 1.22 continual re-solving → "непрекъснато пререшаване" everywhere, incl. fig. 30 (G05 proposed "Продължително пререшаване"); 2.17 test-time → "по време на игра" / "етап на игра" (B38 had "етапа на тестване"); 2.23 → "модели на последователности" in the C07 hand-off; 2.6, 3.5 (board → общи карти), 3.6 (played hands → раздавания; 1326 hands → ръце), 3.9, 3.11, 3.14, 2.15, 2.40, 1.13 applied beyond the listed quotes.
- **06a's X02/X03 carried into this half:** headings "Пропускът, който запълни" (B03 proposed "Празнината, която запълва"), "Уговорки, задънени улици и какво статията не описва", "Изчислителни разходи и достъпност"; rows "Тип игра", "Също и с пълна информация?", "Изчислителни разходи"; `|--|------|` in both scorecards (EN too).
- X01: "(Фигура 6.4/6.5)" → "(вж. фигурата по-долу)" / "(see the figure below)", as 06a did; "(Фигура 2)" → "(фиг. 2 в статията)".
- S13: the proposed clarification "DeepStack – only vs LBR" would contradict DeepStack's human match, so written as "DeepStack played no head-to-head matches against other bots, and no LBR result was reported for Libratus" (EN/BG).
- S07 attribution ("by its authors' account") also in the ReBeL opening and scorecard; S04's "decentralized multi-agent POMDPs" also in EN; C13/B50 "heads-up professional who had done best of the four humans against Libratus" also in the EN opening.
- S16: `[^kilcher2022]` on the first Schmid quotation only (as proposed); "prohibitively expensive in some games" cited to `[^sog]`. The other interview quotations were not checked against the audio.
- C10: the list is kept; only the draft editorial note is removed — the candidate may still trim it.
- B01/B02: the EN math spans that crossed a line break are now on one line, so the pipeline cannot split them again.
- Adjacent fixes: "беше *недостъпна*" (парадигма), "когато бъде насочен" (LBR), "би премахнала" (стъпка), "PBS е въведено", "Обобщено в едно изречение: … , а нито една система…", "~25 милиона ядро-часа" (06a's unit), "уникална стратегия" → "отделна", EN "stated in the main text 'only informally'" (checked in the SoG text).
- Footnotes: used 06a's `brown2018dls`, `brown2020rebel`, `cicero2022`; added `bakhtin2020`, `kilcher2022`; `sog` metadata completed (S20); `brown2017` already had *NeurIPS 30*.

## Skipped (id — reason)
- F06b-B28 — self-play → "самоигра" is glossary row 2.3, an open choice; word-order parts applied (see above).

## Central (id — what is needed)
- F06b-T01…T14 — glossary entries (`llmPipeline/glossary_settled.md`, `terminology_EN_BG.md`): multiplayer, two-player, sound, opponent-blind, in expectation, self-play (row 2.3, open), PBS, prior policy, leaf, anytime, test-time compute, offline, names kept in Latin (Player of Games, Liar's Dice, Reconnaissance Blind Chess, Student of Games), mbb/g + hands. Also the settled entries "multi-pro field → многопроцесорно поле", "river abstraction → речна абстракция", "frontier → граница", "nash-and-search" (B11, B14, B26, S14).
- `figure_labels.json` — merge `fixes/labels_step06.json`. All keys of figs. 27–30 that changed are new keys; the old ones for these four scripts are now unused. Shared keys changed: 'Student of\nGames' → identity (was "Студент по\nИгри"), 'Action abstraction' → "Абстракция на действията" (capitalised; step 04 uses the same key), 'Depth-limited solving', 'Continual re-solving', 'Public belief state' etc. (only fig. 30 uses them, checked by grep).
- § 5.1–5.2 typography (dashes, "7,500", "99.5%", "800,000") and GLOSSARY 0.5 extra bold — left for the central pass; new BG text written with " - " and "20,000"-style numbers like the surrounding text.
- § 5.3 shared footnote labels: `sog`, `pluribus`, `lbr`, `libratus`, `deepstack`, `brown2017` also exist in other chapters.

## Numbers changed (old → new, where)
- SoG exploitability bound: $|\mathcal{N}|UA/\sqrt{T}$ → $|\mathcal{N}|U\sqrt{A}/\sqrt{T}$ (SoG key-innovation formula EN/BG, Synthesis bullet EN/BG); $|\mathcal{N}|$ now "number of information states in the interior" — C01.
- "2 of 400 games against a mid-training AlphaZero" → "against a fully trained AlphaZero searching 8,000 simulations per move" — C02.
- "costs range over six orders of magnitude" → "differ by several orders of magnitude" — C08.
- "For seventy years" → "Since Samuel's checkers program of the 1950s" — C12.
- Hand-off "Chapters 7–15", "Phase D–G", "ReBeL-Lite-on-Leduc task" → "Chapters 7–12", chapters 9–11/12, task removed — C07.
- ReBeL net (BG): "6×1536 скрити слоя" → "6 скрити слоя по 1536 неврона" — B43.
- Fig. 30 cells (G05): continual re-solving now DeepStack + SoG only; depth-limited solving no longer Libratus; AIVAT now DeepStack, Pluribus, ReBeL, SoG (not Libratus); safe (nested) subgame solving no longer Pluribus.

## Figures (file — what changed — printed size now)
All four: every text fs 10, panel titles fs 11 (two lines, left-aligned), boxes sized from measured Bulgarian extents so the renderer neither re-wraps nor shrinks anything; Bulgarian captions (G01); no text outside the axes, so the BG image is never wider than the EN one.
- `rebel_arch[_bg].png` (fig. 27) — kept side by side on an 8-in canvas; net feeds both loops by dashed arrows in the white gutter (no arrow crosses a box); loop-backs in the outer lanes; "retrain nets" note folded into box ⑤ (now also says the sampled leaf is the next β) and the leaf-value note into test box ②; the two grey PBS→loop arrows dropped; definition box, net label, imperatives/1st person, "листо" fixed (G02). Prints at 16.9 cm: BG 7.6 in → **8.7 pt** (titles 9.6), EN 8.0 in → 8.3 pt; 14.9 cm tall.
- `sog_arch[_bg].png` (fig. 28) — same geometry; pink scatter dots deleted; "push new net" routed up the outer right lane into the CVPN; mini-tree clear of the footer; footer on two lines with the two regime notes below it; "априорна стратегия", "процесите (actors)", no "Huber loss"/1st person (G03). Prints at 16.9 cm: BG 8.02 in → **8.3 pt**, EN 8.04 in → 8.3 pt; 15.8 cm tall.
- `evolution_arc[_bg].png` (fig. 29) — rebuilt in inch coordinates (8.2-in canvas): lane labels in their own column, tags on two rows with the last right-aligned (no collisions), footer on 3–4 lines inside its box, "Student of Games" in Latin, all lane labels translated (G04). **Deviation:** the dashed DeepStack–Libratus "unified by depth-limited solving" link is removed rather than relabelled — the corrected "later unified … (2018)" note has no room at fs 10, Libratus never used depth-limited solving, and the 2018 paper is now cited in the text (`[^brown2018dls]`). Width 98 %; prints at 17.2 cm: BG 8.0 in → **8.5 pt**, EN 8.05 in → 8.4 pt.
- `component_reuse[_bg].png` (fig. 30) — four rows corrected (above), "Chapters 3–5", row labels capitalised and per glossary, long BG labels on two lines, note on three lines (G05). Width 90 % → 98 % in both md files; prints at 17.2 cm: BG 7.73 in → **8.8 pt**, EN 7.86 in → 8.6 pt.
- `_diagram_utils.py` — `panel_bg(..., label_dy=0.32)` added for two-line titles (default unchanged, figs. 24–26 identical).

## Remaining overflow / legibility warnings
- `render_bg_figures.py --only step06 --labels-overlay …`: no overflow warnings, 7/7 scripts ok.
- Crops `renders_fix/step06/ch06/p033, p043, p052, p053` checked: nothing overlaps, clipped or re-wrapped. `p042_f1.png` and `p051_f1.png` there are stale 06a crops from before the page numbers shifted.

## Verification
- `python scripts/build_reports.py --step step06 --type all`: all built — summaries EN 47 pp / BG 57 pp; one-pagers EN 1 page (10pt/1.8cm), **BG 1 page (9pt/1.3cm)**. No report_*.md exists for step 06.
- `check_headings.py`: 44 PDFs, 0 missing headings. `check_captions.py`: 24 PDFs, 0 with unaccounted figures.
- BG PDF: the SoG bound with Cyrillic `\text{…}` typesets (p. 45); no `⟦MATH`, no literal `[^…]`, no "$ pairs the public …"; "Recursive Belief-based Learning" only as the one English gloss (p. 30); new notes print (bakhtin2020 p. 32, kilcher2022 p. 40); CICERO reuses note 9 from the DeepStack section.
