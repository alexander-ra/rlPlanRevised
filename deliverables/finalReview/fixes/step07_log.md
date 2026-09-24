# Step 07 — fixes applied
Applied: 81 · Skipped: 0 · Central: 6

Applied = G01–G09, B01–B40, B43, the T01–T14 *occurrences* in the step-07 files, C01–C06,
S01–S08, X02–X04. No R-item. Every review quote matched exactly once (scripted, match
count checked), except where noted. EN mirrored for every C/S finding (and C05's four EN
"step" places); report_en/report_bg carry C01's reset count and C03.

Deviations from the review wording, all for a decided glossary row or a stated reason:
- **GLOSSARY 1.12 overrides "съгласуван"** for the statistical property: the model is now
  "състоятелен", the property "състоятелност" (summary §§ 7.4–7.9, table, one-pager,
  report_bg, fig. 34 box). B18 → "липсата на състоятелност" (not "съгласуваност"); B03's
  "съгласуваната оценка" → "състоятелната оценка". "съгласуван" kept only for "globally
  consistent strategy" and "consistent with the observations" (trajectories, deals).
- **GLOSSARY 3.1 fold → отказ** overrides the review's "пас": B36 "залог, кол, пас" →
  "залог, плащане, отказ"; § 7.3 "Пас - само следствие", "Как се справя моделът с пас?",
  "пасът го оставя…", "(пас скрива…)", "ако тя не е приключила с пас" → отказ; fig. 33
  'Fold: effect only' → 'Отказ: само следствие', 'Observed: BET, then fold' → '…, после
  отказ'; G01 fig. 33 caption "при отказ". "(Чист опонент „винаги пас на залог“" → "Чист
  опонент, който винаги се отказва при залог,". check → "чек" (B26).
- **GLOSSARY 1.7**: fig. 36 'Nash EV (exact)' → 'очаквана стойност при равновесие на Наш
  (точна)' (review: "при Наш"); fig. 37 'Best response\nblended toward Nash' → 'Най-добър
  отговор,\nсмесен с равновесието\nна Наш' (review: "смесен с Наш").
- **B08 formula**: the loop line is a raw `\begin{center}…\end{center}` block (plain text,
  no math, centred, wraps). Checked on p. 4 of step07_bg.pdf. Cyrillic `\text{апостериорно}`,
  `\text{нормализиране}`, `\text{при}` typeset (checked in the PDF text).
- **C06** new text writes "20,000" (surrounding style; typography is central).
- **C02** BG "0.21-0.23" with a hyphen (surrounding style); EN "0.21–0.23".
- **G06** used the optional Ganzfried (2025) sample values: left σ* = (0.8, 0.1, 0.1) with
  (0.5, 0.3, 0.2), (0.3, 0.5, 0.2), (0.2, 0.3, 0.5); right s1 = (0.2, 0.4, 0.4),
  s2 = (0.6, 0.3, 0.1), s3 = (0.2, 0.3, 0.5), which average to (1/3, 1/3, 1/3), so the
  text's "centre of three samples that average to it" is now true of the figure. With
  these values s1 is only 0.23 from the centre, so the collapse arrow was hidden under the
  σ* dot: s1 is marked with an orange ring instead. BG figure uses the decimal comma
  "(0,8; 0,1; 0,1)" and "(1/3; 1/3; 1/3)".
- **G04** optional S3 applied: J/Q/K → В/Д/П in the six card labels (text says Вале/Дама/Поп).
- **G07**: plotting.py now shows display names in EN too ("type-based", "Calling station",
  "Level-1", …); the overlay keys follow these new EN strings. The Nash tick is "Nash
  (equilibrium)" → „Наш“ (равновесие), to avoid the shared key 'Nash' (see Central). All
  nine Leduc types kept (the figure complements the five-row table); X04's note defines
  Level-k and says the menu has nine types "shown in the next figure" (not "фигура 36":
  numbering differs between the standalone summary and the bundle). Table row "Ниво-1" →
  "Ниво 1" to match figure and note. EN note added too.
- Extra, same intent (glossary rows or the same error as a finding):
  summaryBg "(на ръка)", "печалбата на ръка", "всяка ръка попада…", "в края на ръката",
  "Ръката завършва…", "за всяка наблюдавана ръка" → раздаване (3.6); "(**предварително
  убеждение**)", "предварителното убеждение", "средната стойност апостериори",
  "предварителни псевдоброеве", "Вероятността на едно наблюдение" → априорно/апостериорно/
  правдоподобие (2.7); "за преобучаване" → "за всяко повторно решаване" (2.25 makes
  преобучение = overfitting); "с цел съгласуваност" → "с цел еднообразие"; "емпиричният
  случай" → "емпиричният аргумент" (as B09); "Моделиране на противника *представлява*" →
  "Моделирането…" (article, with B43); one-pager "(мащабирано от доверие забравяне," →
  "(забравяне, мащабирано според увереността;" (B34), "*Когато класът на модела съвпада…
  абсолютния таван*" → "пасва на противника… точния таван" (B40/B38).
- **report_bg.md** (glossary pass; the review read it for consistency only): Нашево/наш
  равновесие/Неш → „Наш“ (type) or равновесие на Наш (concept); експлоатер → експлоататор;
  КЛ-дивергенция / "регуляризация на КЛ" → KL-регуларизация; "разминаване на Кълбек–
  Лайблер" → "дивергенция на Кулбак–Лайблер (KL)"; съгласуван → състоятелен (as above);
  семена/начални условия → начални числа; на ръка/ръце (per deal) → раздаване; герой →
  собственият агент; изтичане/саморазкриване → уязвимост; прочит/прочетеното → преценка за
  противника; оптимално отговаря(ме) → най-добър отговор; сходяват/сходява → клонят /
  достигне сходимост; предварително убеждение → априорно разпределение; вероятност
  (likelihood) → правдоподобие; проверява/проверка → чек; фолдва/фолдове → се отказва/отказ;
  "приема всичко" → "плаща всеки залог"; подбиране на ограничена извадка → недостиг на
  наблюдения; изпъкнала програмираща задача → задача на изпъкналата оптимизация;
  пренастройване → повторно напасване; зоологическа градина → зоопарк; базиран на типове →
  типово базиран; "ябълки с ябълки" → при равни условия; Cyrillic "МАР"/"ТВ" → Latin MAP/TV;
  typo "неехплоатируем"; English table headers "Opponent | ceiling" → "Опонент | таван".
  Meaning fixes in the same pass: § 6 "Повърхностите за **изследване**, с конкретно измерено
  лице, …" (a misparse of "The exploration surfaces … the tension") → "Изследването в Част I
  показва с конкретни измерени стойности напрежението…"; § 13 "сигнал за промяна на
  точката" / "потапя промяната на точката" → "сигнал за точка на промяна" / "проваля
  забравянето при точка на промяна"; "последователните модели" (EN: non-parametric and
  sequence-form models) → "непараметричните модели и моделите в последователна форма".
  report_bg fig. line 237 now points at impl_exploitation_leduc_bg.png. "данни от
  самообучение" (self-play, row 2.3 ❓) left untouched.

## Skipped (id — reason)
- none.

## Central (id — what is needed)
- F07-B41 / F07-B42 (GLOSSARY 5.1–5.2) — dashes, decimal comma, "20,000", in summaryBg,
  onePagerBg, report_bg. Only "x" → "×" in the B19 table header was applied (it was part of
  B19's quote).
- F07-X01 / GLOSSARY 5.3 — per-chapter footnote labels. New label `adams2007` added here;
  `shoham2008`, `southey2005`, `ganzfried2015` are shared with other chapters. The S05
  Shoham correction also applies to the identical footnote in steps 01, 02, 08.
- F07-T01…T14 — the glossary entries themselves (glossary_settled / terminology_EN_BG / the
  picker); only their occurrences in step-07 files were fixed. Includes F07-B37's
  Latin "o" in the settled entry "типoв зоопарк".
- Shared figure_labels.json key 'Nash' → 'Наш равновесие' (step 12's plotting.py legend)
  is itself the form GLOSSARY 1.7 rejects ("равновесие на Наш" for the concept). Not
  overlaid here (step 07 now uses "Nash (equilibrium)"). The step-07 overlay also redefines
  shared keys 'EXPLOITATION', 'Nash / GTO\n(unexploitable, blind)' (both also in step 08's
  make_dial_figure.py; review F07-G02 intends the change for both) and 'Act in the hand',
  'Update model', 'Best response' (step 07 only).
- F07-G09 renderer (scripts/figures/render_bg_figures.py): (1) `fit_label` measures a box
  while the script draws, i.e. before `tight_layout()` enlarges the axes, so it sees boxes
  ~25 % smaller than printed and re-wraps/shrinks labels that would fit — fixed for step 07
  only, in its `_diagram_utils.py` (axes fill the figure from the start; `save()` crops to
  the drawn content instead of `bbox_inches="tight"`, which kept the invisible axes and
  widened the image). Other steps whose diagrams call tight_layout() are affected the same
  way. (2) `MIN_FONT = 9.0` lets the fitter shrink to fs 9, which prints ~7.7 pt, below the
  8.2 pt floor (fs 9.6).
- report_bg.md figure captions (11) are still English, and 9 of its 11 images point at
  English PNGs; outside this review's scope (it covered the summary chapter).

## Numbers changed (old → new, where)
From `implementation/step07/implementation/results/{kuhn,leduc}_scale.json` (5 seeds, no
rerun). ± = SE as in report §10/§11 (population SD / √5; sample-SD SE would be
0.008 / 0.009 / 0.060 / 0.019).

| Quantity | Old | New | Where |
|---|---|---|---|
| Kuhn static, after switch | −0.116 (seed 0) | −0.106 ± 0.007 | summary EN/BG § 7.8 table; one-pager EN/BG |
| Kuhn change-point, after switch | +0.226 | +0.211 ± 0.008 | same |
| Leduc static, after switch | +1.940 | +1.834 ± 0.054 | summary EN/BG table |
| Leduc change-point, after switch | +0.525 | +0.552 ± 0.017 | summary EN/BG table |
| "single seed" caveat | "run at a single seed…" | "means over five seeds ± SE; every seed agrees on the direction" | summary EN/BG |
| Leduc resets per seed | 58–59 | 54–63 (Kuhn 55–60) | report_en/bg § 10 |
| Kuhn gap vs exploitable styles | 0.11 to 0.28 per hand | about 0.21–0.23 per hand (0.11–0.28 across both seats) | summary EN/BG § 7.1 |
| Type-based vs ceiling | "statistically indistinguishable on every type" | within 3 % on every type, within 2 SE on nearly all (16 of 19; out: Kuhn AlwaysPass −17 SE, Leduc Rock −3.2 SE, Level2 −2.2 SE) | summary EN/BG § 7.7; one-pager EN/BG; report_en/bg § 11 text + table |
| Fig. 35 samples | (0.6,0.25,0.15),(0.2,0.6,0.2),(0.25,0.2,0.55); left 3rd (0.45,0.2,0.35) | Ganzfried (2025) values above | fig. 35 EN/BG |

## Figures (file — what changed — printed size now)
All printed at 17.6 cm (render_printed manifest); EN and `_bg` twins regenerated.
- `_diagram_utils.py` — box/note default fs 7.6/9.0 → 10; axes fill the figure (fitter
  measures true box size); `save()` crops to content, no tight_layout.
- spectrum_safety_exploitation(_bg).png — boxes 3.8–4.0 × 1.3, fs 8.6–8.8 → 10, notes
  8.0–8.2 → 10, chapter notes stacked at y 0.95 / 0.45 (no collision), "Step 7/8" →
  "Chapter 7/8", BG "Чист най-добър отговор", "Равновесие на Наш" (no GTO), ЕКСПЛОАТАЦИЯ,
  impersonal note. Scale 0.859 → 8.6 pt (SAFETY/EXPLOITATION 9.4 pt); 384 ppi.
- bayes_loop(_bg).png — boxes enlarged (obs 4.2 × 1.3), fs 7.4–9.5 → 10; "\н" gone
  (overlay 'Априорно убеждение\nза стратегията'), "Апостериорно\nубеждение" fits, правдоподобие,
  impersonal notes. Scale 0.847 → 8.5 pt; 390 ppi.
- partial_observability(_bg).png — boxes 3.6/4.8 wide, h1–h3 1.85, fs 7.6–9 → 10; ЗАЛОГ,
  "приписва се на ЕДНА ситуация", 2-line fold note. Scale 0.849 → 8.5 pt (panel titles
  8.9 pt); 389 ppi.
- three_models(_bg).png — model boxes 5.3 × 1.5, fs 7.8–9 → 10, "->" → "→"; Типово
  базиран / Непрекъснат / Състоятелен, agreement fixed, "общ интерфейс: наблюдения →
  стратегия". Scale 0.841 → 8.4 pt; 393 ppi.
- consistency_convex_hull(_bg).png — (11, 5.1) @200 → (8, 4.4) @300; vertices 9 → 10.5,
  titles 10.5 → 11, labels 8–8.2 → 10; labels on white backing, clear of dots/edges;
  collapse label one line below the triangle; хартия. Scale 0.877 → labels 8.8 pt,
  vertices 9.2, titles 9.6; 342 ppi (was 5.1–6.7 pt, 315 ppi).
- figures/impl_exploitation_leduc(_bg).png — plotting.py `__main__` (plot-only, reads
  results/leduc_scale.json); (9.9, 5) @120 → (8, 4.4) @300; legend 8 → 10 above the axes
  (it covered the Maniac bar); ticks 10, ylabel 11; title dropped; display names; BG fully
  translated (legend, ticks, ylabel "средна печалба на агента / раздаване", decimal comma).
  summaryBg now links the `_bg` twin. Scale 0.866 → 8.7 pt (ylabel 9.5); 347 ppi (was
  5.6–7.0 pt, 172 ppi).
- adaptive_loop(_bg).png — fs 7.4–9 → 10, boxes 2.7–3.4 × 1.3, bottom notes on two rows
  (y 0.7 / 0.22, no overlap), "задейства се", agreement, impersonal top note. Scale 0.859
  → 8.6 pt; 384 ppi.

## Remaining overflow / legibility warnings
- Renderer (`render_bg_figures.py --only step07 --labels-overlay …`): 11 scripts ok, 0
  failed, 17 BG figures, **no overflow warnings**. Every box label kept fs 10; the fitter
  only re-wrapped four at fs 10 ('Априорно убеждение за стратегията', 'Правдоподобие на
  наблюдаваното действие', 'Действие в раздаването', 'Наблюдавано: ЗАЛОГ, после отказ'),
  and the line breaks read naturally (checked on the crops).
- All printed text 8.4–9.6 pt; smallest is fig. 34 at 8.4 pt.
- The render re-ran implementation/step07/exploration/*.py: robustness_sweep.json,
  fingerprints_cache.json and type_detector.json were re-saved **byte-identical** (no git
  diff), so nothing was restored. The exploration `_bg` PNGs it writes (report figures)
  are left in place (fingerprint_TightPassive_bg.png modified, 9 new, as the earlier test
  run had already produced).

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step07 --type all` (with PYTHONIOENCODING=utf-8; without it the
  script's ✓ print crashes on the cp1251 console): all 6 PDFs built. BG one-pager fits on
  one page at 10pt / 1.5cm; EN at 10pt / 1.8cm. BG summary 20 pages.
- `check_headings.py`: no missing heading in step 07 (44 PDFs, 4 missing — step08_en,
  step09_bg).
- `check_captions.py`: step 07 clean (24 PDFs, 1 with unaccounted figures — step08_en).
- Crops: `deliverables/finalReview/renders_fix/step07/ch07/p003…p018_f1.png`, all seven
  read; captions Bulgarian, labels ≈ 80–85 % of caption letter height, nothing overlaps.
