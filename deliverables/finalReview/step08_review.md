# Step 08 — final review

**Summary:** Every number in the chapter matches the result JSONs, but the chapter's safe-exploitation theory needs correcting. (1) Content at the core of C2. The method called "Ganzfried" puts the floor $v^*$ on each hand's strategy. That is Ganzfried & Sandholm's weakest safe baseline ("best equilibrium", their §6.3), not their gift-risking algorithm, and it explains why the "core result" gains only 0.002–0.076 per hand. The SES paragraph credits Liu et al. with Ge et al.'s stronger guarantee. The Leduc headline ("global does not scale; local does") compares a 40-iteration cap with a 400-iteration one. The "bang-bang frontier" holds only for how $p$ maps to a strategy, sampled on an 11-point grid; the frontier itself is not bang-bang. (2) The Bulgarian text prints two corrupted formulas ("⟦MATHI5⟧", pp. 157 and 161) and English in formulas, footnotes and tables. It also has meaning errors: "нашия план" (our plan) for the Nash blueprint, "последователност от герои" (a sequence of heroes), "безопасен спрямо прайм", and "unsafe" rendered "експлоатируем". Several of these come from settled glossary entries (T01–T04). (3) All seven figures fail at print size. Two diagrams have colliding labels. Five result plots are entirely English at 130–141 ppi. Fig. 40's λ labels run opposite to the text's $p$. The current label mapping has also reverted four step-08 entries to English. Corpus-wide items, counted once and not reported per occurrence: " - " as a dash 63× in the summary (+14 in the one-pager); decimal points ≈ 170 (+14); "30,000"-style separators 5×; 161 bold spans against 122 in the EN; 3 footnote markers whose note prints in another chapter (`ganzfried2015` ×2 → ch. 7, `shoham2008` → ch. 1; F07-X01). The pilot's T11 (KL) does not occur anywhere in this chapter (summary, one-pager, reports EN/BG checked). T05 occurs once (F08-B28).
**Counts:** S1 22 · S2 46 · S3 6   (by category: G 9 · B 35 · T 10 · C 10 · S 6 · X 4)

Conventions in this file: quotes are **raw markdown** from `summaryBg.md` / `onePagerBg.md` (including `**`, `*`, `$`, and the U+2011 non-breaking hyphens the source contains in § 8.9). Proposals keep the chapter's " - " dashes and decimal points; both are fixed centrally. "EN" quotes come from `summaryEn.md` / `onePager.md`. The EN files are hard-wrapped, so EN quotes cite line numbers and may need joining across a line break. Printed sizes: matplotlib size × (printed width ÷ saved image width). Body text is 10.9 pt and the floor is ≈ 8.2 pt. "p. N" is the PDF page of `allSummaries_bg.pdf`, as in `renders/manifest.json`. Terms follow the pilot where it decided them: "агент/собствен агент" for *hero* (T14), „Наш“ for the Nash opponent type (F07-B02), "жетон", "начално число", "раздаване".

## G — Figures

### F08-G01 · S1 · Bulgarian captions for all seven figures
- **Where:** summaryBg.md, image alt text of figs. 38–44 (pp. 150–165). All seven print in English (known corpus-wide defect). The BG alt texts of figs. 38 and 39 are also stale copies: they say "Step 7 / Step 8" and "(Step 7's best response)" where the EN now says "Chapter".
- **Now → Proposed:**
  - "![The safety-exploitation dial with a governor. Pure Nash is unexploitable but blind; a full best response extracts the most value but is maximally risky. Safe exploitation operates in between, capped by a floor on the worst-case value. Step 7 built the sensor (the model); Step 8 builds the actuator (safe exploitation). The only thing that differs between methods is where the floor sits.]" → "![Скалата безопасност–експлоатация с ограничител. Чистото равновесие на Наш е неексплоатируемо, но „сляпо“; пълният най-добър отговор извлича най-голяма стойност, но носи най-голям риск. Безопасната експлоатация действа между двете крайности, като стойността в най-лошия случай не може да падне под определен праг. Глава 7 изгради сензора (модела), а Глава 8 изгражда изпълнителния механизъм (безопасната експлоатация). Методите се различават единствено по това къде е поставен прагът.]"
  - "![One LP engine, five safety floors. The sequence-form treeplex gives a linear objective (EV vs the model); a constraint-generation loop calls an exact best response as the worst-case oracle and adds a safety cut until the floor is met. RNR, Ganzfried, prime-safe, SES and adaptation are the SAME solve with a different floor - and one validated primitive (Step 7's best response) powers both the objective and every safety check.]" → "![Една LP-задача, пет прага за безопасност. Дървовидният политоп в последователна форма дава линейна целева функция (очакваната стойност срещу модела); цикълът за генериране на ограничения използва точния най-добър отговор като предсказвач за най-лошия случай и добавя отсичащо ограничение, докато прагът не бъде спазен. RNR, Ганцфрид, prime-safe, SES и адаптацията са ЕДНА И СЪЩА задача с различен праг, а една вече проверена операция (най-добрият отговор от Глава 7) захранва както целевата функция, така и всяка проверка за безопасност.]"
  - "![The naive Nash/best-response blend on Kuhn: a smooth exploitation-safety frontier where each increment of profit costs a near-proportional increment of your own worst-case loss.]" → "![Наивното смесване на равновесието на Наш с най-добрия отговор в Кун: плавна граница между експлоатация и безопасност, при която всяко увеличение на печалбата струва почти пропорционално увеличение на собствената загуба в най-лошия случай.]" (only if the figure is kept; see F08-G04)
  - "![The exploitation-safety frontier on Kuhn with the LP operating points. The canonical RNR "curve" is only an interpolation between two achieved clusters (the safe corner and the full-BR corner); the smooth line is the dominated naive blend; the stars (Ganzfried, prime-safe, adaptation) sit at the efficient safe corner.]" → "![Границата между експлоатация и безопасност в Кун с работните точки на LP-методите. „Кривата“ на каноничния RNR е само отсечка между двете постигнати групи точки (безопасния ъгъл и ъгъла на пълния най-добър отговор); плавната линия е доминираното наивно смесване; звездите (Ганцфрид, prime-safe, адаптация) са в ефективния безопасен ъгъл.]"
  - "![Methods versus the Rock on Kuhn: green is EV against the opponent, red is worst-case value, the dashed line is the Nash floor. Only the full best response's worst-case (red) plunges to −0.5, far below the floor; every principled method hugs the floor while still exploiting.]" → "![Методите срещу „камък“ в Кун: в зелено е очакваната стойност срещу противника, в червено - стойността в най-лошия случай, а пунктирът е прагът на Наш. Само при пълния най-добър отговор стойността в най-лошия случай (червено) пада до −0.5, далеч под прага; всички строго обосновани методи остават близо до прага и печелят колкото равновесието или малко повече.]" (the last clause also fixes an overclaim, F08-C07: against the Rock they gain 0.002–0.006 over Nash)
  - "![Global versus local safety. Global methods re-solve the whole tree; on Ледюк their constraint-generation loop did not converge within the iteration budget and left grossly unsafe strategies. The subgame method pins play outside a chosen subgame to the blueprint and re-solves only that subgame with a gadget - a far smaller problem that did converge and stayed near-safe.]" → "![Глобална срещу локална безопасност. Глобалните методи решават наново цялото дърво; в Ледюк техният цикъл за генериране на ограничения не достигна сходимост в рамките на лимита от 40 итерации и остави силно небезопасни стратегии. Методът с под-игра фиксира играта извън избраната под-игра според базовата стратегия и решава наново само нея с приспособление - много по-малка задача, която при лимит 400 итерации достигна сходимост и остана почти безопасна.]" (the iteration caps: F08-C02)
  - "![Teaching attack on Kuhn, cumulative profit. The full best response (blue) climbs on the bait to about +1700, then only drifts down after the switch - it ends far ahead, because a Nash "revealer" claws back only about the game value per hand. The safe methods refuse the bait and pay the first-player tax throughout.]" → "![Обучаваща атака в Кун, натрупана печалба (изпълнение с начално число 0). Пълният най-добър отговор (синьо) се изкачва до около +1700 по време на примамката и след смяната само бавно слиза - завършва далеч напред, защото „разкриващият“ противник, който играе равновесие на Наш, си връща само около стойността на играта на раздаване. Безопасните методи не се хващат на примамката и през цялото време плащат „данъка“ на първия играч.]" (seed 0: F08-G08)
- **Fix:** replace the alt text in `summaryBg.md` (the `](file.png)` part stays). In `summaryEn.md` add "(seed 0)" to the fig. 44 caption, and for fig. 43 add the iteration caps (F08-C02).

### F08-G02 · S1 · Fig. 38 dial: English "(max value, max risk)", "под" for floor, colliding "Стъпка" notes, too small
- **Where:** `renders/ch08/p150_f1.png` — caption "The safety-exploitation dial with a governor…"
- **Problem:**
  1. English in the BG figure: "(max value, max risk)" in the right box. The mapping entry keeps it: 'Full best response\n(max value, max risk)' → 'пълен най-добър отговор\n(max value, max risk)'.
  2. Middle box "макс. стойност при най-лош случай >= под": *floor* is rendered "под", which reads as the preposition "under". "при" loses *s.t.*, and ">=" is ASCII. The box text runs outside both edges.
  3. The two bottom notes run into each other as one line: "Стъпка 7 изгради СЕНЗОРА (модела) Стъпка 8 изгражда…". Both use the stale "Стъпка" (same defect as F07-G02).
  4. "Наш / GTO": GTO is an undefined abbreviation that the text never uses. The box text touches both edges.
  5. "БЕЗОПАСНОСТ" is upper case but "експлоатация" lower case (the shared key 'EXPLOITATION', F07-G02).
  6. Floor note "подът е единственото… безопасен спрямо прайм >= Наш-епс": "подът" = the floor of a room, "Наш-епс" is not a term, "безопасен спрямо прайм" is F08-B08. "безопасен регулатор" is not a governor; it reads as "a safe regulator".
  7. Legibility (scale 0.865 = 17.6 cm ÷ 2643 px @ 330 dpi): boxes 8.4–8.6 → 7.3–7.4 pt; notes 7.6–8.2 → 6.6–7.1 pt. Only the two axis titles (fs 11 → 9.5 pt) pass.
- **Fix:** `make_dial_figure.py`:
  - Font sizes: all `box` fs → 10, all `note` fs → 10.
  - Boxes: left box `box(ax, 0.6, 2.3, 3.0, 1.0, …)` → `box(ax, 0.4, 2.3, 3.3, 1.0, …)`; right box `box(ax, 10.4, 2.3, 3.0, 1.0, …)` → `box(ax, 10.0, 2.3, 3.6, 1.0, …)`; middle box h 1.0 → 1.4 (y 2.3 → 2.0), three lines. Start the three short arrows at the new box tops.
  - Notes: move the floor note to y 1.35 and split it into three lines. Replace the Step notes with "Chapter 7 built the SENSOR (the model)" / "Chapter 8 builds the ACTUATOR (safe exploitation)", stacked at `note(ax, 7.0, 0.55, …)` and `note(ax, 7.0, 0.1, …)`, with `ylim (0, 5.2)` → `(-0.3, 5.2)`.
  - Mapping, existing keys:
    - 'Full best response\n(max value, max risk)' → 'Пълен най-добър отговор\n(макс. стойност, макс. риск)'
    - 'Nash / GTO\n(unexploitable, blind)' → 'Равновесие на Наш\n(неексплоатируемо, сляпо)' (shared with step 07)
    - 'EXPLOITATION' → 'ЕКСПЛОАТАЦИЯ'
    - 'safety governor' → 'предпазен ограничител'
  - Mapping, new keys for the edited source strings:
    - 'SAFE exploitation\nmax value s.t.\nworst-case >= floor' → 'БЕЗОПАСНА експлоатация\nмакс. стойност при\nнай-лош случай ≥ праг'
    - 'the floor is the only thing that differs between methods:\nGanzfried >= v*  |  prime-safe >= v* - eps\nadaptation >= blueprint worst case' → 'методите се различават само по прага:\nГанцфрид ≥ v*  |  prime-safe ≥ v* − ε\nадаптация ≥ най-лош случай на базовата стратегия'
    - 'Глава 7 изгради СЕНЗОРА (модела)' and 'Глава 8 изгражда ИЗПЪЛНИТЕЛНИЯ МЕХАНИЗЪМ (безопасната експлоатация)'

### F08-G03 · S1 · Fig. 39 LP engine: labels overlap across boxes, English "floor/cut/s.t./LOCAL/eps", Latin "da", stale "Стъпка 7", prints at 6.1–6.9 pt
- **Where:** `renders/ch08/p152_f1.png` — caption "One LP engine, five safety floors…"
- **Problem:**
  1. Illegible collisions:
     - The green box's second line runs into the red box's second line: "EV спрямо модел = c(предсказвач за най-лош случай, Стъпка 7)".
     - The check box's lines sit on top of the incoming and outgoing arrows: "не", ">= floor".
     - "LP в последователна форма" and "treeplex + разрези за безопасност" overflow the yellow box, and "SequenceForm (герой treeplex, повторно използван)" overflows its box.
     - "стойност на плана, LOCAL приспособление" overflows its row box.
  2. English in the BG figure: "SequenceForm", "treeplex" (×2), "s.t.", "floor" (×3), "cut", "eps", "LOCAL". "da -> готово" is written in Latin letters (should be "да").
  3. Stale "Стъпка 7" twice. The bottom note "една валидирана примитивна (…)" is an adjective with no noun. "под = стойност на Наш v*" repeats the "под" error, and "<= план експлоатируемост" is a noun pile.
  4. A large empty band separates the diagram from the bottom note: the boxes end at y 2.4 and the note sits at y 0.6.
  5. Legibility (scale 0.824 = 17.6 cm ÷ 2775 px @ 330 dpi): boxes 8.2 → 6.8 pt; check box 7.8 → 6.4 pt; rows 7.6 → 6.3 pt; notes 7.4–8.4 → 6.1–6.9 pt.
  6. The current mapping is worse than the print: 'exact best response\n(worst-case oracle, Step 7)' → 'точен най-добър отговор\n(worst-case oracle, Step 7)' (English), and 'seq-form LP…' → 'LP във последователна форма…' ("във", F07-B25). A re-render with today's mapping would print these.
- **Fix:** `make_lp_engine_figure.py`:
  - Font sizes: all `box` and `note` fs → 10. Keep `new_fig(w=14, …, xlim=(0, 14))`: widening the canvas would shrink the print scale.
  - Geometry, within the same 14 units:
    - left column w 3.1 → 3.6 (x 0.4 → 0.2)
    - middle column x 4.8 → 4.3, w 3.2 → 3.8, check box h 1.3 → 1.8 (four lines)
    - right column x 9.2 → 8.6, w 4.4 → 5.2
    - feedback arrow end (3.5, 5.0) → (3.8, 5.0)
    - bottom note y 0.6 → 1.6 on two lines; `ylim (0, 8.4)` → `(1.1, 8.4)`
  - Source strings: "Step 7" → "Chapter 7" (both).
  - Mapping (the keys change with the source edits):
    - 'SequenceForm\n(hero treeplex, reused)' → 'Последователна форма\n(политоп на агента)'
    - 'Payoff vector c\nEV vs model = c . x' → 'Вектор на печалбата c\nEV спрямо модела = c · x'
    - 'seq-form LP\nmax c . x  s.t.\ntreeplex + safety cuts' → 'LP в последователна форма\nmax c · x  при\nполитоп + отсичания за безопасност'
    - 'exact best response\n(worst-case oracle, Chapter 7)' → 'точен най-добър отговор\n(предсказвач за най-лошия\nслучай, гл. 7)'
    - 'worst-case >= floor ?\nno -> add cut c_adv . x >= floor\nyes -> done' → 'най-лош случай ≥ праг?\nне → добави отсичане\nc_adv · x ≥ праг\nда → край'
    - 'double-oracle\ncutting-plane loop' → 'двоен предсказвач:\nметод на отсичащите равнини'
    - 'same solve, different FLOOR:' → 'една и съща задача, различен ПРАГ:'
    - 'RNR (Johanson)\ntunable via p (max-min)' → 'RNR (Johanson)\nнастройва се чрез p (максимин)'
    - 'Ganzfried\nfloor = Nash value v*' → 'Ганцфрид\nпраг = стойността на играта v*'
    - 'prime-safe (Jeary)\nfloor = v* - eps' → 'prime-safe (Jeary)\nпраг = v* − ε'
    - 'SES subgame (Liu)\nblueprint value, LOCAL gadget' → 'SES, под-игра (Liu)\nбазова стратегия, ЛОКАЛНО приспособление'
    - 'adaptation (Ge)\n<= blueprint exploitability' → 'адаптация (Ge)\n≤ експлоатируемост на базовата стратегия'
    - "one validated primitive (Chapter 7's exact best response) powers BOTH the objective and every safety check" → 'една проверена операция (точният най-добър отговор от Глава 7)\nзахранва ЕДНОВРЕМЕННО целевата функция и всяка проверка за безопасност'

### F08-G04 · S1 · Fig. 40 naive blend: English, λ labels opposite to the text's p, a wrong "ABOVE", 130 ppi, and it duplicates fig. 41
- **Where:** `renders/ch08/p157_f1.png` — caption "The naive Nash/best-response blend on Kuhn…"; `summaryBg.md` links `../figures/pareto_curve_kuhn.png` (the EN file; no BG twin exists).
- **Problem:**
  1. The figure is entirely English: title, axes, "labels = lambda".
  2. The point labels contradict the text. `exploration/pareto_curve.py` defines λ as the weight on *Nash* ("0.0 .. 1.0 (weight on Nash)"), so "0.0" sits on the full best response (+0.167, 0.444) and "1.0" on Nash (−0.047, 0.001). The text and Table 23 define the blend as $(1-p)\cdot$Nash$ + p\cdot$BR, so $p=0$ is Nash. A reader matching the labels to Table 23 finds them reversed; report_en §2 relabels the same data "λ (weight on BR)".
  3. The title claims "efficient solvers push ABOVE this". With y = worst-case loss, better means lower and to the right; fig. 41 itself says "down-and-right = better". The chapter's own result is also that the solvers barely leave this line (F08-C05).
  4. At 780 px printed at 15.2 cm it is 130 effective ppi (soft); point labels fs 7 → 7.0 pt.
  5. It adds nothing that fig. 41 does not show: the grey line in fig. 41 is the same blend with identical values (`pareto_kuhn.json` rnr_naive vs `pareto_curve_kuhn.json`).
- **Fix (preferred):** drop fig. 40 from both summaries and change the pointer:
  - "(фигура по-долу, вляво)" → "(сивата линия на следващата фигура)"
  - EN l. 242 "(Figure below, left)" → "(the grey line in the next figure)"

  If it is kept instead:
  - `pareto_curve.py`: annotate `f"{1 - r['lambda']:.1f}"` and relabel it $p$ = weight on the best response; replace the title by "Naive Nash/BR blend (labels: p = weight on the best response)" or drop it; annotation fs 7 → 10; `dpi=130` → 300; write to `deliverables/reports/step08/figures/`.
  - Mapping: 'Naive Nash/BR blend frontier -- kuhn\n(labels = lambda; efficient solvers push ABOVE this)' → delete; 'worst-case loss (exploitability, >= 0)' → 'загуба в най-лошия случай (експлоатируемост, ≥ 0)' (current value keeps "exploitability" in English).

### F08-G05 · S1 · Fig. 41 frontier: English, 130 ppi, a hidden star, and it cannot show the dominance it claims
- **Where:** `renders/ch08/p158_f1.png` — caption "The exploitation-safety frontier on Kuhn with the LP operating points…"; source `implementation/step08/implementation/plotting.py` `plot_pareto`.
- **Problem:**
  1. English throughout: the title "Exploitation-safety frontier -- kuhn (down-and-right = better; solvers should dominate the naive blend)", the axes and the legend (code names).
  2. 845 px printed at 16.5 cm is 130 effective ppi (soft); legend fs 8 → 8.0 pt.
  3. The orange `prime_safe` star lies exactly under the red `adaptation` star (identical point), so the reader sees two stars where the caption names three.
  4. The canonical RNR is drawn `"-o"`, so its two clusters are joined by a straight line lying on top of the grey blend. The 0.002 dominance the text claims at the safe corner is invisible at this scale.
- **Fix:** `plotting.py` `plot_pareto`:
  - Draw RNR with markers only (`"o"`, no line), annotated "p ≤ 0.6" / "p ≥ 0.7".
  - Label the coinciding point "prime_safe = adaptation".
  - Add an inset of the safe corner (x −0.050…−0.035, y 0…0.010) so that ganzfried (−0.044, 0.0005), prime-safe/adaptation (−0.040, 0.0079) and the blend's end (−0.047, 0.0003) separate.
  - figsize (6.5, 5) → (7, 4.8); dpi 130 → 300; legend fs 8 → 10; drop `set_title` (the caption carries it).
  - Add the `__main__` from F08-G09.

  Mapping:
  - 'exploitability (game value - worst-case; >= 0)' → 'експлоатируемост (стойност на играта − най-лош случай; ≥ 0)'
  - 'naive Nash/BR blend' → 'наивно смесване Наш/BR' (current 'наивен Nash/BR микс': English plus slang)
  - 'RNR canonical' → 'каноничен RNR'
  - 'exploitation profit (EV vs TightPassive)' → 'печалба от експлоатацията (EV срещу „камък“)'
  - new keys: 'ganzfried' → 'Ганцфрид', 'prime_safe' → 'prime-safe', 'adaptation' → 'адаптация'

### F08-G06 · S1 · Fig. 42 methods bar chart: English, 7.4 pt ticks and legend, 141 ppi, "TightPassive" where the text says „камък“
- **Where:** `renders/ch08/p160_f1.png` — caption "Methods versus the Rock on Kuhn…"; source `plotting.py` `plot_tournament`.
- **Problem:**
  1. English throughout. The title "Methods vs TightPassive -- kuhn (worst-case below the floor = unsafe)" names the opponent differently from the caption and text ("Rock", „камък“). The legend "Nash floor -0.056" uses a hyphen-minus and a decimal point.
  2. 975 px printed at 17.6 cm is 141 ppi (scale 0.924); x tick labels and legend fs 8 → 7.4 pt.
  3. The figure shows a `ses_subgame` bar that the summary's Kuhn table omits, and neither text explains it (F08-X04).
- **Fix:** `plot_tournament`: figsize (7.5, 4.5) → (7, 4.2); dpi 130 → 300; `set_xticklabels(…, fontsize=8)` → 10; `legend(fontsize=8)` → 10; drop `set_title`. Mapping, new keys: 'EV vs TightPassive' → 'EV срещу „камък“'; 'Nash floor -0.056' → 'праг на Наш −0,056' (a runtime f-string, so the key is the rendered text).

### F08-G07 · S1 · Fig. 43 global vs local: both title lines and both notes collide, "подпомагащ" for gadget, first person, mapping regressed to English
- **Where:** `renders/ch08/p162_f1.png` — caption "Global versus local safety…"
- **Problem:**
  1. Unreadable collisions: the two panel titles touch ("…адаптация)ЛОКАЛНА безопасност…"), and so do the two bottom notes ("…(грубо небезопасен)най-лош случай ~-0.13…"). Each is one long line centred at x = 3.3 and 10.6.
  2. Meaning: "подпомагащ под-игра SES" reads as "helping subgame SES". The gadget is "приспособление" (the chapter's own word).
  3. First person: "преизчислявам ЦЯЛОТО дърво" (T03).
  4. Overlaps: "план (фиксиран)" sits on the triangle's apex edges; "под-игра (преизчислявана + приспособление)" overflows the small triangle.
  5. Numbers: "-0.64 .. -1.33", "~-0.13", "+0.25..+0.68" use hyphen-minus, ".." and decimal points. The notes also hide the unequal iteration caps (40 vs 400; F08-C02).
  6. Stale render with a regressed mapping. The print shows "план (фиксиран)" and "(преизчислявана + приспособление)". The current mapping has 'blueprint\n(pinned)' → 'план\n(pinned)', 'subgame\n(re-solved\n+ gadget)' → 'под-игра\n(re-solved\n+ gadget)', and 'GLOBAL safety (Ganzfried / prime-safe / adaptation)' → '…(Ganzfried / prime-safe / adaptation)', so re-rendering today would put English back.
  7. Legibility (scale 0.889 = 17.6 cm ÷ 2572 px @ 330 dpi): titles 9.0 → 8.0 pt; triangle labels 7.4–8.6 → 6.6–7.6 pt; notes 7.6 → 6.8 pt.
- **Fix:** `make_global_local_figure.py`:
  - Font sizes: all `note` fs → 10.
  - Titles on two lines each ("GLOBAL safety\n(Ganzfried / prime-safe / adaptation)", "LOCAL safety\n(SES: subgame + gadget)") at y 6.2 → 6.1, with `ylim (0, 6.6)` → `(-0.6, 6.9)`.
  - Bottom notes on three lines each, at y 0.85 → 0.5.
  - Blueprint label y 4.4 → 4.0.
  - Enlarge the small triangle: apex (10.6, 3.3) → (10.6, 3.6), base 9.7–11.5 → 9.3–11.9, label y 2.05 → 2.1.
  - Add the caps to the EN source strings: "capped at 40 iters" and "converged in 194-350 iters (cap 400)".
  - Mapping:
    - 'GLOBAL safety\n(Ganzfried / prime-safe / adaptation)' → 'ГЛОБАЛНА безопасност\n(Ганцфрид / prime-safe / адаптация)'
    - 'LOCAL safety\n(SES: subgame + gadget)' → 'ЛОКАЛНА безопасност\n(SES: под-игра + приспособление)'
    - 're-solve the\nWHOLE tree' → 'преизчисляване на\nЦЯЛОТО дърво'
    - 'blueprint\n(pinned)' → 'базова стратегия\n(фиксирана)'
    - 'subgame\n(re-solved\n+ gadget)' → 'под-игра\n(преизчислена\n+ приспособление)'
    - the two notes → 'Ледюк: спрени при лимит 40 итерации,\nБЕЗ сходимост; най-лош случай\nот −0,64 до −1,33 (силно небезопасни)' and 'Ледюк: сходимост за 194–350 итерации (лимит 400);\nнай-лош случай ≈ −0,13 (почти безопасен);\nот +0,25 до +0,68 срещу слабите типове'
  - The decimal commas may trip the pipeline's "numbers changed" check; accept them by hand.

### F08-G08 · S1 · Fig. 44 teaching attack: English, the x axis is a sample index, and the curves are one seed
- **Where:** `renders/ch08/p165_f1.png` — caption "Teaching attack on Kuhn, cumulative profit…"
- **Problem:**
  1. English throughout; the title "Teaching attack -- kuhn: TightPassive -> Nash" uses code names.
  2. The x axis "hand (downsampled)" runs 0–400. That is the index of the downsampled curve, not the hand: the dotted "opponent switch" at 200 is hand 10 000.
  3. The curves are `cumulative_seed0` (`kuhn_scale.json`), a single seed. The table beside it reports 5-seed means. Seed 0's full_br ends at +1196 (+0.060/hand) against the table's +0.051, and neither caption says so.
  4. 141 ppi; legend fs 8 → 7.4 pt.
- **Fix:** `plotting.py` teaching curve:
  - Plot against `np.arange(len(curve)) * ta["total"] / len(curve)`; xlabel "hand"; the switch line at `ta["switch_at"]`.
  - `legend(fontsize=10)`; dpi 300; drop the title; caption "(seed 0)" (F08-G01).
  - Mapping: 'hand' → 'раздаване'; 'opponent switch' → 'смяна на противника'.

### F08-G09 · S2 · The five result plots never get a BG version; the three diagram renders are stale
- **Where:** `plotting.py`, `exploration/pareto_curve.py`, `summary/*_bg.png` (written 1 Aug 13:08) vs `scripts/figures/out/figure_labels.json` (1 Aug 19:50).
- **Problem:**
  - `plotting.py` is in `plotting_scripts()` but has no `__main__`, so `render_bg_figures.py` runs it and gets nothing (same cause as F07-G07). `pareto.py` and `tournament.py`, which call it, contain no `savefig` and are not listed.
  - `summaryBg.md` links the EN files `../figures/impl_*.png` and `../figures/pareto_curve_kuhn.png`.
  - The three diagram renders predate the mapping. For four entries (F08-G03 item 6, F08-G07 item 6) the *print* is better than the current mapping: those "dictionary"-sourced values kept English words, so the next render will regress unless they are fixed first.
- **Fix:**
  - `plotting.py`: add `if __name__ == "__main__":` that loads `results/kuhn_scale.json` and `results/pareto_kuhn.json` and calls `plot_tournament({"kuhn": r}, FIG)` and `plot_pareto({"kuhn": p}, FIG)`. Use `FIG = "../../../deliverables/reports/step08/figures"` and add a `prefix="impl_"` argument so that the outputs keep their current names.
  - Fix the mapping entries above, then run `python scripts/figures/render_bg_figures.py --only step08`.
  - Point `summaryBg.md` at the `_bg` twins.
  - The central overflow fix must wrap text or enlarge boxes, never shrink it below fs ≈ 9.6 (F07-G09).

## B — Bulgarian language

### F08-B01 · S1 · corrupted formulas — a math placeholder printed literally (pp. 157, 161)
- **Where:** summaryBg.md § "Ограничен отговор по Наш…" and § "Ганцфрид върху Кун…"
- **EN:** "jumps straight to the full best response at $p \approx 0.7$ (EV $+0.167$, exploitability $0.444$)" / "(Prime-safe and adaptation coincide here because, for this baseline, $v^* - \varepsilon = \text{worst-case(blueprint)}$ …)"
- **Now → Proposed:**
  - "при $ (EV $ (EV $, exploitability $, експлоатируемост ⟦MATHI5⟧). Няма междинни точки." → "при $p \approx 0.7$ (EV $+0.167$, експлоатируемост $0.444$). Между изпробваните стойности на $p$ (през 0.1) няма междинни точки." (the second sentence also carries F08-C05)
  - The second occurrence, "…за тази базова линия ⟦MATHI5⟧ - двете долни граници са буквално равни…", is replaced as a whole by F08-C08, which also corrects the claim.
- **Why:** The translation pipeline's inline-math placeholder was never restored, and the first formula was scrambled around it. Both print (p. 157: "при $ (EV $ (EV $, exploitability $, експлоатируемост ⟦MATHI5⟧)"). The same defect exists in step 06 (`⟦MATHI10⟧`, l. 454), and a "$ (EV $" pattern appears in step 09. Grep the whole corpus for "⟦MATH".

### F08-B02 · S1 · English left in formulas
- **Where:** summaryBg.md §§ 8.2, 8.3, 8.5 (all print, pp. 151–156)
- **Now → Proposed:**
  - "\sum_{\text{terminals } z} \big[\text{chance}(z)\cdot \text{opp-reach}(z)\cdot u_{\text{hero}}(z)\big]" → "\sum_{z \in Z} \big[\pi_c(z)\cdot \pi_{-h}(z)\cdot u_h(z)\big]", and "защото собственото произведение на вероятностите" → "където $Z$ са крайните състояния, $\pi_c(z)$ е вероятността на случайните ходове, $\pi_{-h}(z)$ - вероятността на ходовете на противника, а $u_h(z)$ - печалбата на агента. Това е така, защото собственото произведение на вероятностите" (apply the same to the EN, l. 90 and l. 93)
  - "\qquad \text{for all opponents } \sigma'." → "\qquad \text{за всеки противник } \sigma'."
  - "$\text{EV}(x,\sigma') \ge \text{floor}$" → "$\text{EV}(x,\sigma') \ge \text{праг}$"
  - "\text{floor} \;=\; v^* - \varepsilon, \qquad \varepsilon = \text{exploitability(baseline)} \ge 0," → "\text{праг} \;=\; v^* - \varepsilon, \qquad \varepsilon = \text{експлоатируемост(базова линия)} \ge 0,"
  - "\text{exploitability}(x) \;\le\; \text{exploitability(blueprint)} \quad\Longleftrightarrow\quad \text{worst-case}(x) \ge \text{worst-case(blueprint)}." → "\text{експлоатируемост}(x) \;\le\; \text{експлоатируемост(базова стратегия)} \quad\Longleftrightarrow\quad \text{най-лош случай}(x) \ge \text{най-лош случай(базова стратегия)}."
  - "\text{EV}(x,\text{model})" → "\text{EV}(x,\text{модел})"
  - "$(1-p)\cdot\text{Nash} + p\cdot\text{BR}$" → "$(1-p)\cdot\text{Наш} + p\cdot\text{BR}$"
- **Why:** English words print in the displayed formulas. The symbolic sum removes the language problem altogether. Cyrillic inside `\text{}` has no precedent in the corpus, so check the first rebuild (as F07-B08). The pseudocode block and the `floor = v*` code spans may stay English as code.

### F08-B03 · S1 · English prose in four footnotes, plus English quotation marks
- **Where:** summaryBg.md footnotes (print on pp. 154, 155, 159, 162)
- **Now → Proposed:**
  - "[^johanson2007]: Johanson, M., Zinkevich, M. & Bowling, M. (2007). "Computing Robust Counter-Strategies." *NeurIPS* — Restricted Nash Response, the tunable ancestor of all of the above." → "[^johanson2007]: Johanson, M., Zinkevich, M. & Bowling, M. (2007). "Computing Robust Counter-Strategies." *NIPS 2007*, 721–728 - ограниченият отговор по Наш (RNR), настройваемият предшественик на методите по-горе."
  - "[^gordon2003]: the constraint-generation / double-oracle idea traces to McMahan, Gordon & Blum (2003), "Planning in the Presence of Cost Functions Controlled by an Adversary," *ICML* - общата рецепта за "оптимизиране срещу най-лош случай, който откривате докато вървите."" → "[^gordon2003]: Идеята за генериране на ограничения / двоен предсказвач идва от McMahan, H. B., Gordon, G. J. & Blum, A. (2003). "Planning in the Presence of Cost Functions Controlled by an Adversary." *ICML* - общата рецепта за „оптимизиране срещу най-лош случай, който се открива в хода на решаването“."
  - "[^liu2022]: Liu, W. et al. (2022). "Safe Opponent-Exploitation Subgame Refinement." *NeurIPS* (the gadget)." → "[^liu2022]: Liu, M., Wu, C., Liu, Q., Jing, Y., Yang, J., Tang, P. & Zhang, C. (2022). "Safe Opponent-Exploitation Subgame Refinement." *NeurIPS* - търсене на безопасна експлоатация (SES) с приспособление; добавената експлоатируемост е ограничена отгоре (теорема 4.1)."
  - "[^search2024]: Ge, Z. et al. (2024), *op. cit.* — OX-Search bounds exploitation loss *per information set*, hardening the same idea against "teaching" attacks." → "[^search2024]: Ge, Z. et al. (2024), *op. cit.* - OX-Search: повторно решаване на под-игри с приспособление, което гарантира, че експлоатируемостта не надвишава тази на базовата стратегия (теорема 4.3); може да се прилага вложено при всяко ново информационно множество и е насочено срещу противник, който първо „обучава“ модела, а после го експлоатира."
  - "прави лоста $p$ да зависи от това колко данни подкрепят всяка част от стратегията, което е това, което изглажда границата на практика." → "прави параметъра $p$ зависим от това колко данни подкрепят всяка част от стратегията - и именно това изглажда границата на практика."
- **Why:** English sentences print in the BG bundle, and "…" quotes should be „…“. The metadata corrections (Liu's initial, the full author list, NIPS pages) are verified in F08-S04. The OX-Search content is corrected in F08-S05.

### F08-B04 · S1 · English left in text and tables
- **Where:** summaryBg.md §§ 8.2, 8.5, 8.6, 8.8
- **Now → Proposed:**
  - "| $p$ | Canonical RNR - EV | Canonical - експлоатируемост | наивна смеска - EV | наивна - експлоатируемост |" → "| $p$ | каноничен RNR - EV | каноничен RNR - експлоатируемост | наивно смесване - EV | наивно смесване - експлоатируемост |"
  - "| **Маниак** (LooseAggr.) |" → "| **Маниак** (разпуснат-агресивен) |"
  - "| **AlwaysBet** |" → "| **Винаги залага** (`AlwaysBet`) |"
  - "| **AlwaysPass** (най-експлоатируем) |" → "| **Винаги пасува** (`AlwaysPass`; най-експлоатируем) |"
  - "| **CallingStation** |" → "| **Пасивен играч** (`CallingStation`) |"
  - "| **LoosePassive** |" → "| **Разпуснат-пасивен** (`LoosePassive`) |"
  - "В *smoke* изпълнението (30,000 CFR итерации)" → "В пробното изпълнение (*smoke*, 30,000 итерации на CFR)"
  - "подчинени на линейните ограничения на **treeplex**" → "подчинени на линейните ограничения на **дървовидния политоп** (treeplex)"
  - "treeplex е множество от **линейни ограничения**" → "дървовидният политоп се задава с **линейни ограничения**"
  - "$\max_x c\cdot x$ върху treeplex" → "$\max_x c\cdot x$ върху дървовидния политоп" (the fourth "treeplex" is rewritten in F08-C03)
- **Why:** English prints in the BG text (pp. 151, 157, 159, 161, 163). The type names follow chapter 7's BG table ("Пасивен играч", "разпуснат-агресивен"); the code id stays in backticks because the prose refers to `AlwaysPass`. "Canonical" in § 8.5's lead sentence is fixed in F08-B27, and "ε-safety" in F08-B08.

### F08-B05 · S1 · meaning — the Nash opponent and the Nash blueprint as "our" (F07-B02)
- **Where:** summaryBg.md intro, §§ 8.5, 8.6, 8.7, 8.8.1
- **EN:** "lost to an unexploitable Nash opponent" / "play the Nash blueprint everywhere" / "**Nash** (control)" / "the 'reveal' is only a *Nash* opponent"
- **Now → Proposed:**
  - "(в Ледюк той всъщност *загуби* срещу неексплоатируем Нашов противник)" → "(в Ледюк той всъщност *загуби* срещу неексплоатируемия противник „Наш“)"
  - "играйте нашия план навсякъде" → "играйте навсякъде базовата стратегия (равновесието на Наш)"
  - "| **Наш равновесие** (контрол) |" → "| **„Наш“** (контролен) |"
  - "тъй като „разкриването“ е само *Нашов* опонент" → "тъй като „разкриващият“ противник е само „Наш“"
  - "- от **Нашево равновесие** до пълен най-добър отговор" → "- от равновесието на Наш до пълния най-добър отговор"
  - "една Нашева стратегия гарантира" → "равновесната стратегия на Наш гарантира"
- **Why:** "нашия план" says "our plan", a different statement from "the Nash blueprint". "Нашов" is not a word, and "Наш равновесие" breaks agreement. The rest of the adjectival "Нашево/Нашева" (F07-T13) are in the rewrites of F08-B09, F08-B12, F08-B26, F08-B33, F08-C01 and F08-C04.

### F08-B06 · S1 · meaning — *unsafe* rendered "експлоатируем"
- **Where:** summaryBg.md § 8.6 (the fourth occurrence is in F08-C06)
- **EN:** "worst-case −0.33 / −0.17, unsafe" / "They appear "unsafe" in the table only because the flag compares to $v^*$" / "even the Nash policy is flagged "unsafe""
- **Now → Proposed:**
  - "(идентична стойност с `full_br`, най-лошият случай −0.33 / −0.17, експлоатируем)" → "(същата стойност като `full_br`, стойност в най-лошия случай −0.33 / −0.17 - небезопасен)"
  - "Те изглеждат „експлоатируеми“ в таблицата само защото флагът се сравнява с $v^*$;" → "Те изглеждат „небезопасни“ в таблицата само защото флагът ги сравнява с $v^*$;"
  - "дори стратегията на Наш е маркирана като „експлоатируема“" → "дори стратегията на Наш е маркирана като „небезопасна“"
- **Why:** In this chapter *unsafe* means "worst case below the floor". Every strategy except an exact equilibrium is exploitable, so the BG sentence "they look exploitable only because of the flag" is false: prime-safe *is* exploitable by 0.008, by design. § 8.8 already uses "небезопасен" correctly.

### F08-B07 · S1 · meaning/terminology — *hero* as "герой", including "последователност от герои" (T14)
- **Where:** summaryBg.md §§ 8.2, 8.4, 8.5, 8.7 (≈ 20 occurrences)
- **EN:** "pin every hero sequence *outside* the subgame to its blueprint realization weight (so the hero plays the blueprint everywhere except the subgame), and set the safety floor to the blueprint's own worst-case value"
- **Now → Proposed:**
  - "**фиксирайте** всяка последователност от герои *извън* под-играта към теглото на реализацията на плана (така че героят играе плана навсякъде, освен в под-играта) и задайте прага на безопасност на най-лошата стойност на самия план." → "**фиксирайте** всяка последователност на агента *извън* под-играта на реализационното ѝ тегло в базовата стратегия (така че агентът играе базовата стратегия навсякъде освен в под-играта) и задайте прага на безопасност равен на стойността в най-лошия случай на самата базова стратегия."
  - Elsewhere: "героя" → "агента", "героят" → "агентът". The first occurrence (l. 43) becomes "собствения агент"; see F08-B11.
- **Why:** "последователност от герои" says "a sequence of heroes", and the sentence also loses *worst-case value* and *blueprint*. "Герой" is poker-forum jargon read literally (F07-T14). The chapter only ever has one agent and one "противник", so "агент" is unambiguous.

### F08-B08 · S1 · meaning — *prime-safe* rendered "безопасен спрямо прайм"
- **Where:** summaryBg.md §§ 8.3, 8.4, 8.6, 8.9
- **Now → Proposed:**
  - "**(б) Безопасен спрямо прайм / ε-safety (Jeary & Turrini 2023): корекция за несъвършена базова линия.**" → "**(б) Безопасност prime-safe (Jeary & Turrini 2023): корекция за несъвършена базова линия.**"
  - "безопасен спрямо прайм понижава пода с точно експлоатируемостта на самата базова линия," → "методът prime-safe понижава прага точно с експлоатируемостта на самата базова линия,"
  - "| Безопасен спрямо прайм (2023) |" → "| Prime-safe (2023) |"
  - "безопасен спрямо прайм използва `floor = v* − ε`" → "prime-safe използва `floor = v* − ε`"
  - "**Безопасен спрямо прайм и адаптацията изразходват предвидения ε-бюджет.**" → "**Prime-safe и адаптацията изразходват измерен ε-бюджет.**" (also F08-B13: *measured*, not "предвидения")
  - "„Прайм‑безопасен“ и „адаптация“ разширяват гаранцията" → "Prime-safe и адаптацията разширяват гаранцията"
- **Why:** "безопасен спрямо прайм" means "safe relative to a prime", which is meaningless. "Prime-safe" is Jeary & Turrini's coined name and should stay a Latin method name, as the one-pager already does. "ε-safety" is English, and it is McCracken & Bowling's more general notion, not this one.

### F08-B09 · S1 · meaning — *leak* as "изтичане/изтича" (T07)
- **Where:** summaryBg.md § 8.9 "Обратни връзки" (the third occurrence is in F08-C04)
- **EN:** "The continuous model's self-inflicted leak against Nash on Leduc (Chapter 7, §7) … and, indeed, Ganzfried never leaks to Nash here."
- **Now → Proposed:** "произтича от самопричиненото изтичане на непрекъснатия модел спрямо **Нашево равновесие** в играта **Ледюк** (Глава 7, §7) - и действително **ганцфрид** тук никога не изтича към **Нашево равновесие**." → "произтича от самонанесената уязвимост на непрекъснатия модел срещу „Наш“ в Ледюк (Глава 7, § 7.7) - и наистина тук Ганцфрид никога не губи срещу „Наш“ повече от стойността на играта."
- **Why:** "изтича към Нашево равновесие" says "flows out towards the Nash equilibrium". The poker sense is a weakness in one's own play (F07-B31, T07). The sentence also has lower-case "ганцфрид" and five bold spans that the EN does not have.

### F08-B10 · S1 · grammar — first-person "оптимално отговарям" (T03), and a third name for *best response*
- **Where:** summaryBg.md § 8.1
- **EN:** "you best-respond hard to your current read: maximum profit **if** the read is right" / "the full best response to the tight "Rock" style on Kuhn earns **+0.167 per hand**, but its **worst-case value is −0.5** — an adversary who best-responds back can take half a chip a hand off it."
- **Now → Proposed:**
  - "Ако пък я завъртите докрай към *експлоатация*, ще **оптимално отговарям** твърдо на текущото си впечатление: максимална **печалба**, **ако** впечатлението е вярно" → "Ако пък я завъртите докрай към *експлоатация*, ще играете чист най-добър отговор на текущата си преценка за противника: максимална печалба, **ако** преценката е вярна"
  - "пълният **оптимален отговор** на стегнатия стил „**камък**“ в **Кун** носи **+0.167 на раздаване**, но неговият **най-лош стойностен случай е −0.5** - противник, който **оптимално отговаря** обратно, може да вземе половин чип на раздаване от него." → "пълният най-добър отговор на стегнатия стил „камък“ в Кун носи **+0.167 на раздаване**, но стойността му в най-лошия случай е **−0.5** - противник, който на свой ред играе най-добър отговор срещу него, може да му взема по половин жетон на раздаване."
- **Why:** "ще оптимално отговарям" means "you will I-best-respond" (F07-T03). The chapter otherwise says "най-добър отговор", and "оптимален отговор" is a third name for the same object. The fix also covers *read* ("преценка", F07-B30), *worst-case value* (T03 below) and chip ("жетон", F07-B36).

### F08-B11 · S2 · meaning — "every exploitation method" (the BG drops *safe*); § 8.2 heading and objective
- **Where:** summaryBg.md § 8.2
- **EN:** "## Exploitation as Constrained Optimization" / "The single most useful idea in this chapter is that **every safe-exploitation method is the same optimization problem** with one part swapped out." / "> maximize the hero's expected value against the opponent model, **subject to** a safety floor on the hero's worst-case value."
- **Now → Proposed:**
  - "## Експлоатацията като **ограничена оптимизация**" → "## Експлоатацията като оптимизация с ограничения"
  - "Единствената най-полезна идея в тази глава е, че **всеки метод за експлоатация представлява един и същ проблем на оптимизация**, при който се заменя само една негова част." → "Най-полезната идея в тази глава е, че **всеки метод за безопасна експлоатация е една и съща оптимизационна задача**, в която се сменя само една част."
  - "> максимизиране на очакваната стойност на героя спрямо модела на противника, **при условие** за праг на безопасност за най-лошия стойностен случай на героя." → "> максимизиране на очакваната стойност на собствения агент спрямо модела на противника **при ограничение**: стойността му в най-лошия случай да не пада под прага на безопасност."
- **Why:** Without "безопасна" the claim is false: a plain best response is not a floor-constrained problem. "ограничена оптимизация" means "limited optimization"; *constrained* is "с ограничения". "Единствената най-полезна" is the calque of F07-B03. Bold does not belong in a heading (F07-B25).

### F08-B12 · S2 · meaning — "Nash's own EV" rendered as "the equilibrium value of Nash"
- **Where:** summaryBg.md §§ 8.6, 8.8
- **EN:** "**and** it beats Nash's own EV on every exploitable type — most vividly **+0.222 versus Nash's +0.146** against `AlwaysPass`, and +0.131 versus +0.118 against the Maniac." / "(**+0.25 to +0.68** versus the weak types, beating Nash)"
- **Now → Proposed:**
  - "**и** той превъзхожда равновесната стойност на Наш при всеки експлоатируем тип - най-ярко **+0.222 срещу +0.146 на Наш** срещу `alwaysPass` и +0.131 срещу +0.118 срещу маниак." → "**и** печели повече от стратегията на Наш срещу всеки експлоатируем тип - най-ярко **+0.222 срещу +0.146 за Наш** срещу `AlwaysPass` и +0.131 срещу +0.118 при маниака."
  - "(**+0.25 до +0.68** спрямо слабите типове, надминавайки **Нашево равновесие**)" → "(**+0.25 до +0.68** срещу слабите типове - повече от стратегията на Наш)"
- **Why:** "равновесната стойност" is the game value $v^*$, which nothing can beat in the worst case. The EN compares against the Nash *strategy's EV* against that opponent. The fix also covers the case-mangled code id `alwaysPass` and "срещу … срещу".

### F08-B13 · S2 · meaning — the ε-budget is *measured*, not "предвидения"
- **Where:** summaryBg.md § 8.6
- **EN:** "**Prime-safe and adaptation spend a measured ε-budget.** … and the run *measured* the early-stopped-CFR baseline's exploitability at $\varepsilon = 0.0074$"
- **Now → Proposed:** "а изпълнението *измерва* експлоатируемостта на базовата линия с ранно прекратен CFR при $\varepsilon = 0.0074$;" → "а при изпълнението експлоатируемостта на базовата линия (CFR, спрян преждевременно) е *измерена*: $\varepsilon = 0.0074$;" (heading: F08-B08)
- **Why:** "предвидения" means "foreseen/planned", the opposite of the point. "измерва … с ранно прекратен CFR" says the measuring is done *with* CFR.

### F08-B14 · S2 · meaning — "first-player value" as "първоначална стойност"
- **Where:** summaryBg.md § 8.6 — "(известната първоначална **стойност** в **Кун**, $\approx -1/18$)"
- **EN:** "(Kuhn's known first-player value, $\approx -1/18$)"
- **Now → Proposed:** "(известната първоначална **стойност** в **Кун**, $\approx -1/18$)" → "(известната стойност на Кун за първия играч, $\approx -1/18$)"
- **Why:** "първоначална" means "initial". −1/18 is the game value for the player who acts first.

### F08-B15 · S2 · meaning — *dual* LP as "двойно", *local/subgame* as a noun pile, OX-Search transliterated
- **Where:** summaryBg.md § 8.9 "Напред към дисертацията"
- **EN:** "an **exact one-shot dual LP** for the worst-case constraint, or a commitment to **local / subgame** safety (SES, OX-Search)"
- **Now → Proposed:** "**точно еднократно двойно линейно програмиране** за ограничението при най-лошия случай или ангажимент към **локална / под‑игра** безопасност (SES, OX‑търсене)" → "**точна двойнствена LP-задача, решавана еднократно**, за ограничението за най-лошия случай, или избор на **локална безопасност на ниво под-игра** (SES, OX-Search)"
- **Why:** "двойно линейно програмиране" means "double linear programming". The LP dual is "двойнствена задача". OX-Search is an algorithm name and stays Latin (curated table). The source uses U+2011 in "под‑игра" and "OX‑търсене".

### F08-B16 · S2 · meaning — "at the adversarial long-run average"
- **Where:** summaryBg.md § 8.1 — "гаранцията се отнася до дългосрочната средна стойност при противников подход"
- **EN:** "the guarantee is on the long-run adversarial average"
- **Now → Proposed:** "гаранцията се отнася до дългосрочната средна стойност при противников подход" → "гаранцията се отнася до дългосрочната средна печалба срещу най-неблагоприятния противник"
- **Why:** "при противников подход" ("with an opposing approach") has no meaning here.

### F08-B17 · S2 · meaning — *self-play value* as "самообучение"
- **Where:** summaryBg.md § 8.4
- **EN:** "an *approximate* Nash's self-play value can sit a hair **above** the game's true achievable max-min, so requiring the exact `wc ≥ floor` can make the LP eventually infeasible"
- **Now → Proposed:** "*приблизителната* стойност от самообучението в равновесието на Наш може да бъде съвсем малко **над** истинската постижима максимин стойност на играта, така че изискването за точно `wc ≥ floor` може да направи линейното програмиране в крайна сметка недопустимо" → "стойността, която *приблизителното* равновесие на Наш постига срещу самото себе си, може да бъде съвсем малко **над** истинската постижима максиминна стойност на играта, така че изискването за точно `wc ≥ floor` може в даден момент да направи LP-задачата недопустима (без допустимо решение)"
- **Why:** "самообучение" means self-learning (training). The EN means the value of the strategy played against itself. "линейното програмиране … недопустимо" makes the discipline infeasible; it is the LP instance that is (F08-B23).

### F08-B18 · S2 · meaning — teaching-attack setup: "the model passes each solver", double quotes, "семена"
- **Where:** summaryBg.md § 8.8.1
- **EN:** "A deceptive opponent plays the weak Rock bait for 10 000 hands, then switches to a strong Nash "reveal" for 10 000 more; a Step-7 model feeds each solver every 500 hands (5 seeds)."
- **Now → Proposed:**
  - "Последният експеримент е стрес тест за измама, който цялата система за безопасност трябва да издържи." → "Последният експеримент е проверка при измама - изпитанието, което цялата система за безопасност трябва да издържи."
  - "Измамлив опонент играе слабата примамка „камък“ в продължение на 10,000 раздавания, след което преминава към силно „Нашево равновесие“ „разкриване“ за още 10,000; моделът от Глава 7 подава всеки решавач на всеки 500 раздавания (5 семена)." → "Измамлив противник играе слабия стил „камък“ като примамка в продължение на 10,000 раздавания, след което „разкрива“ силната си игра и още 10,000 раздавания играе равновесие на Наш; на всеки 500 раздавания моделът от Глава 7 подава обновената си оценка на всеки решавач (5 начални числа)."
- **Why:** "подава всеки решавач" says "passes each solver" (hands it over). The EN means the model feeds the solvers. "силно „Нашево равновесие“ „разкриване“" is two quoted nouns side by side. "семена" is F07-B19; the table header of the same section already says "начално число".

### F08-B19 · S2 · meaning/grammar — teaching-attack conclusion
- **Where:** summaryBg.md § 8.8.1, paragraph after the figure
- **EN:** "so the windfall is never repaid within 10 000 hands" / "The corrected takeaway, which I now believe is the right design lesson:" / "measure safety by the worst case, not by realized profit against a benign opponent" / "so it trips the $v^*$-referenced counter by design"
- **Now → Proposed:**
  - "така че неочакваната печалба никога не се възстановява в рамките на 10,000 ръце" → "така че тази неочаквана печалба не бива върната в рамките на 10,000 раздавания"
  - "Коригираният извод, в който сега вярвам, че е правилният урок за проектиране:" → "Коригираният извод, който сега смятам за правилния урок при проектирането, е:"
  - "срещу добронамерен опонент" → "срещу безобиден противник"
  - "така че по дизайн задейства брояча, посочен в $v^*$." → "така че по замисъл задейства брояча, който се отчита спрямо $v^*$."
  - "„обучаващата атака наказва алчния експлойтър“" → "„обучаващата атака наказва алчния експлоататор“"; "за да накажете алчния експлойтър" → "за да накажете алчния експлоататор"; "адаптивен контраексплойтър" → "адаптивен контраексплоататор" (T10)
- **Why:** "не се възстановява" says the windfall is not restored. The EN means the opponent never wins it back. "в който сега вярвам, че е" does not parse. "посочен в $v^*$" means "indicated in v*". "добронамерен" means well-intentioned.

### F08-B20 · S2 · terminology — *floor* as "под / пода / подът"
- **Where:** summaryBg.md §§ 8.3, 8.6 (the figures: F08-G02, F08-G03)
- **Now → Proposed:**
  - "като подът на **Нашево равновесие** е $v^* = -0.056$" → "като прагът на Наш е $v^* = -0.056$"
  - "понижава пода" → F08-B08
  - table header "Неформална долна граница" → F08-B33
- **Why:** "под" is the floor of a room and, in figures, reads as the preposition "under". The chapter's term is "праг". Optional S3: the chapter also uses "долна граница" for the same floor (≈ 9×, e.g. "остава на долната граница на Наш", "наруши долната граница на Наш"). It also uses "долна граница" for a cut's *lower bound* (§ 8.4), a different object, so "праг" throughout would separate the two.

### F08-B21 · S2 · terminology — *blueprint* as "план", next to "план за реализация"
- **Where:** summaryBg.md §§ 8.3, 8.4, 8.7 (proposed term: T04)
- **Now → Proposed:**
  - "да бъдеш не по-експлоатируем от своя план.**" → "да не бъдеш по-експлоатируем от своята базова стратегия.**"
  - "Тъй като планът вече е $\varepsilon$-експлоатируем" → "Тъй като базовата стратегия вече е $\varepsilon$-експлоатируема"
  - "ако планът е *ужасен*, „не по-лошо от плана“ се удовлетворява тривиално" → "ако базовата стратегия е *ужасна*, „не по-лошо от базовата стратегия“ се удовлетворява тривиално"
  - "Тъй като „играйте плана също вътре в под-играта“ винаги е възможно" → "Тъй като „играйте базовата стратегия и вътре в под-играта“ винаги е допустимо"
  - The remaining occurrences are in F08-B07, F08-B30, F08-B33, F08-C03 and F08-C04.
- **Why:** § 8.2 and § 8.7 use "план за реализация" (realization plan, the LP variable) a few lines from "план" (blueprint). In § 8.7 both occur in one sentence ("теглото на реализацията на плана"). A reader cannot tell them apart. *Feasible* is "допустимо", not "възможно".

### F08-B22 · S2 · terminology — *cut / cutting plane*: five renderings
- **Where:** summaryBg.md §§ 8.2, 8.5, 8.8
- **Now → Proposed:**
  - "(двоен предсказвач / цикъл с равнини на сечение)" → "(двоен предсказвач / метод на отсичащите равнини)"
  - "добавяме единственото линейно сечение, което той предполага" → "добавяме единственото линейно отсичащо ограничение, което той поражда"
  - "която решаваме със същия механизъм с равнини на отсичане" → "който решаваме със същия метод на отсичащите равнини" (also "която" → "който": the antecedent is "максимин")
  - "цикълът с равнини на сечение добавя по един съперников срез на итерация" → "методът на отсичащите равнини добавя по едно отсичащо ограничение на итерация"
  - "така че 40 среза изобщо не фиксират" → "така че 40 отсичащи ограничения изобщо не фиксират"
- **Why:** The chapter uses "сечение", "срез", "равнини на сечение", "равнини на отсичане", plus "разрез" and "cut" (one-pager, figure) for one object. The Bulgarian OR term is "метод на отсичащите равнини" (T08).

### F08-B23 · S2 · terminology — the LP instance called four different things
- **Where:** summaryBg.md §§ 8.2, 8.4, 8.5, 8.7, 8.8, 8.9
- **Now → Proposed:**
  - "За да се превърне това в *изчислима* програма" → "За да се превърне това в *изчислима* задача"
  - "а целият метод е **линейна програма**" → "а целият метод е **задача на линейното програмиране (LP)**"
  - "да проверим линейната програма спрямо кода" → "да проверим LP-задачата спрямо кода"
  - "решаваме линейната програма, прочитаме стратегията на героя" → "решаваме LP-задачата, прочитаме стратегията на агента"
  - "(iii) решава линейното програмиране с ограничение за безопасност със решавача HiGHS на SciPy" → "(iii) решава LP-задачата с ограничение за безопасност с решавача HiGHS на SciPy"
  - "методите на ЛП достигат" → "LP-методите достигат"
  - "линейното програмиране може само да се справи поне толкова добре" → "решението на LP-задачата може да бъде само поне толкова добро"
  - "главната линейна програма продължава да връща" → "главната LP-задача продължава да връща"
  - "значително по-малка линейна програма" → "значително по-малка LP-задача"
  - "която линейното програмиране оптимизира" → "която LP-задачата оптимизира"
- **Why:** The same object appears as "линейна програма" (a calque), "линейното програмиране" (the discipline), "ЛП" and "LP" (one-pager, figures). "със решавача" should be "с решавача" ("със" only before с/з).

### F08-B24 · S2 · lexis — *converge* rendered with non-verbs (cf. F07-B03)
- **Where:** summaryBg.md §§ 8.8, 8.9 (one-pager: F08-B34)
- **Now → Proposed:**
  - "като записваше за всяка клетка дали решаването е **сходимо** или е достигнало лимита" → "като за всяка клетка е записано дали решаването е **достигнало сходимост**, или лимита"
  - "**достигнаха лимита от 40 итерации без да сходят**" → "**достигнаха лимита от 40 итерации, без да достигнат сходимост**"
  - "SES **сходи** при трима от четиримата експлоатируеми опоненти" → "SES **достигна сходимост** при трима от четиримата експлоатируеми противници"
  - "не сходява в рамките на практически бюджет" → "не достига сходимост в рамките на практически бюджет"
  - "несходимостта в Ледюк представлява" → "липсата на сходимост в Ледюк представлява"
- **Why:** "сходи/сходят" is the verb "to pop over (somewhere)", and "сходява" is not a word (F07-B03). The noun "сходимост" is right, so the verb phrase is "достига сходимост".

### F08-B25 · S2 · grammar/terminology — *worst-case value* and the doubled article "неговият най-лошият случай"
- **Where:** summaryBg.md §§ 8.2, 8.6
- **Now → Proposed:**
  - "Прагът на безопасност представлява ограничение върху **най-лошия случай** стойност" → "Прагът на безопасност е ограничение върху **стойността в най-лошия случай**"
  - "но неговият най-лошият случай се срива до **−0.5**" → "но стойността му в най-лошия случай се срива до **−0.5**"
  - "Срещу *всеки* противник неговият най-лошият случай остава на долната граница на Наш" → "Срещу *всеки* противник стойността му в най-лошия случай остава на прага на Наш"
  - "нейният най-лошият случай е $-0.0568$" → "стойността ѝ в най-лошия случай е $-0.0568$"
- **Why:** "на най-лошия случай стойност" does not parse. "неговият най-лошият" carries two articles. Settled "worst-case value → най-лошият стойностен случай" (T03) is the source. The chapter's own table caption already has the right form: "стойност в най-лошия случай".

### F08-B26 · S2 · terminology — "двуигрова" and "$N$-игрова" for two-/N-*player* (T02)
- **Where:** summaryBg.md §§ 8.1, 8.3.1
- **Now → Proposed:**
  - "В **двуигрова игра с нулева сума** тази гаранция е точна" → "В игра с нулева сума за двама играчи тази гаранция е точна"
  - "В **$N>2$-игрова** игра това се срива: Нашевата стратегия *не* гарантира фиксирана стойност срещу произволни противници" → "В игра с $N>2$ играчи това се срива: равновесната стратегия на Наш *не* гарантира фиксирана стойност срещу произволни противници"
  - The third form, "$N$-игрова игра", is in F08-C09; "в двуигрови игра" is in F08-C01.
- **Why:** "двуигрова игра" means "a two-game game", and "двуигрови игра" also breaks agreement. The same paragraph already says "игра за двама с нулева сума".

### F08-B27 · S2 · terminology — *bang-bang* as "изненадващ обрат", "Canonical", "обхождане" (T01, F07-T09)
- **Where:** summaryBg.md § 8.5 heading and lead, § 8.6 item 3
- **EN:** "## Restricted Nash Response and the Bang-Bang Frontier" / "**The measured surprise — canonical RNR is bang-bang.** I predicted the canonical sweep would be a smooth, monotone frontier…" / "This is the §5 bang-bang threshold moving with opponent exploitability"
- **Now → Proposed:**
  - "## Ограничен отговор по Наш и граница „включено–изключено“" → "## Ограничен отговор по Наш и скокообразното превключване"
  - "**Измерената изненада - Canonical RNR е изненадващ обрат.** Предвидих, че каноничното обхождане ще бъде гладка, монотонна граница, която доминира смеската навсякъде. Не е така. В играта Кун срещу камък, Canonical RNR връща" → "**Измерената изненада - каноничният RNR превключва скокообразно.** Предвидих, че при изменение на $p$ каноничният RNR ще очертае гладка, монотонна граница, която доминира смесването навсякъде. Не е така. В Кун срещу „камък“ каноничният RNR връща"
  - "Това е §5 праг „включено–изключено“, който се движи с експлоатируемостта на противника - и конкретната причина Ганцфрид, който ограничава *стойността*, а не *копче*, да бъде по-добрият примитив." → "Това е прагът на превключване от § 8.5, който се измества според експлоатируемостта на противника - и конкретната причина Ганцфрид, който ограничава *стойността*, а не параметър, да е по-добрата основа."
- **Why:** "изненадващ обрат" means "a surprising twist", so "RNR is a surprising twist" says nothing. The heading also claims the *frontier* is bang-bang, which F08-C05 disputes. "обхождане" is traversal (F07-T09), and "копче" (a button) is a third word for *knob*.

### F08-B28 · S2 · terminology — "съгласуваността" for the consistency work (T05)
- **Where:** summaryBg.md § 8.9 — "от работата върху CFR и съгласуваността е *променливата*"
- **EN:** "the sequence-form representation from the CFR and consistency work becomes the *variable* the LP optimizes"
- **Now → Proposed:** "от работата върху CFR и съгласуваността е *променливата*" → "от работата върху CFR и върху състоятелността (Глава 7) е *променливата*"
- **Why:** This is the pilot's T05: Ganzfried's statistical consistency is "състоятелност". This is the only occurrence in chapter 8.

### F08-B29 · S2 · terminology — within-chapter inconsistencies
- **Where:** summaryBg.md throughout
- **Now → Proposed:**
  - Ganzfried in lower case:
    - "печелят малко повече от ганцфрид" → "печелят малко повече от Ганцфрид"
    - "Гаранцията на ганцфрид е *глобална*" → "Гаранцията на Ганцфрид е *глобална*"
    - "Предвидих, че ганцфрид ще бъде безопасен на Ледюк, както е на Кун." → "Предвидих, че Ганцфрид ще бъде безопасен в Ледюк, както в Кун."
    - "„Ганцфрид“ е безопасен" → "Ганцфрид е безопасен"
  - "не представлява** алгоритъма на Johanson" → "не представлява** алгоритъма на Йохансон" (§ 8.5 prose also has "Гладката крива на Йохансон"; citations stay Latin)
  - "който прави $p$ за всеки информационен набор" → "който задава отделно $p$ за всяко информационно множество"; "*данни-ориентирания* вариант" → "варианта *със смещение към данните* (data-biased)"
  - "Вместо това **глобалните** решаващи" → "Вместо това **глобалните** решавачи" (the table caption says "решавачи")
  - "| Опонент | метрика |" → "| Противник | метрика |". Elsewhere "опонент/опонента/опонентът/опоненти/опонентите" → "противник/противника/противникът/противници/противниците" (≈ 12×; § 8.6 table header already says "Противник")
  - "(Кун покер и Ледюк холдем)" → "(Кун покер и Ледюк Холдем)" (§ 8.8 capitalizes)
  - King:
    - "под-играта зададена на крал-флоп" → "под-играта, зададена като „поп на масата“"
    - "малката под-игра „крал-флоп“" → "малката под-игра „поп на масата“"
    - "„Ледюк кръг 2“" → "„втори рунд в Ледюк“"
  - "до **+0.975** срещу `alwaysPass`" → "до **+0.975** срещу `AlwaysPass`"; "експлоатируемите `alwaysPass` / `AlwaysBet`" → "експлоатируемите `AlwaysPass` / `AlwaysBet`" (the third is in F08-B12)
- **Why:** One concept, one spelling. § 8.7 says "поп" for the King and chapter 7 uses "Поп", while "крал-флоп" mixes a chess King with hold'em slang (Leduc has no flop). The case-mangled `alwaysPass` is not the code id.

### F08-B30 · S2 · calques and slang
- **Where:** summaryBg.md intro, §§ 8.1, 8.2, 8.3.1, 8.4, 8.5, 8.6, 8.8
- **Now → Proposed:**
  - "Това е глава, изградена из основи, за *безопасна* експлоатация на противника:" → "Тази глава въвежда от самото начало *безопасната* експлоатация на противника:"
  - "не се предполага предварителна познатост с кода на проекта" → "не се изисква предварително познаване на програмния код на проекта" (F07-B11)
  - "и са ограничени, където е възможно, от *точни* аналитични препратки, а не симулирани такива" → "и където е възможно, са поставени в *точни* аналитични граници, а не в симулирани" (F07-B11)
  - "Когато дадено изпълнение противоречи на това, което теорията ме е накарала да очаквам, аз го заявявам и го съгласувам - тези пропуски са най-показателните части от главата." → "Когато резултатът противоречи на онова, което теорията ме е карала да очаквам, казвам го изрично и обяснявам разминаването - тъкмо тези разминавания са най-поучителните части на главата."
  - "или сте били *сандбегвани* (умишлено подхранвани със слаб стил, за да се предизвика голямо **отклонение**)" → "или противникът нарочно ви е подвел (показвал ви е слаб стил, за да ви примами към голямо отклонение)"
  - "на една вече доверена примитивна операция" → "на една вече проверена елементарна операция"
  - "- атакуващата точка на дисертацията" → "- точката, от която тръгва дисертацията"
  - "набор от *щифтове*, които фиксират играта на героя извън избрана под-игра да бъде равна на плана" → "набор от *фиксирани тегла*, които задържат играта на агента извън избраната под-игра такава, каквато е в базовата стратегия"
  - "**Знаме, което си струва да се запази.**" → "**Уговорка, която си струва да се запомни.**"
  - "> **Бележка за резолюцията на измерването, защото това ме ухапа.**" → "> **Бележка за точността на измерването (сблъсках се с този проблем на практика).**"
  - "в противен случай базовата линия ще „спъне“ собствения си тест." → "в противен случай базовата линия няма да издържи собствената си проверка."
  - "Това беше маркирано като номер едно „вероятно ще се счупи“ елемент *преди* изпълнението и точно там се счупи." → "Още *преди* изпълнението това беше отбелязано като най-вероятното слабо място - и методът се провали точно там."
  - "*Оставам честен към себе си относно SES:*" → "*За SES обаче трябва да се отбележи:*"
- **Why:** Each is literal English. "съгласувам" means "coordinate/agree", and "пропуски" means omissions (the EN means discrepancies). "сандбегвани" is untranslated slang, and "щифтове" are hardware pins. "Знаме", "ме ухапа" and "атакуващата точка" are word-for-word. "доверена" means "entrusted".

### F08-B31 · S2 · grammar
- **Where:** summaryBg.md §§ 8.2, 8.5
- **Now → Proposed:**
  - "Причината да се плати тази „данък“ за смяна на променливите" → "Причината да се плати този „данък“ за смяната на променливите"
  - "(вериги от корен до тук от собствените им избори)" → "(поредици от собствените му избори от корена до текущата точка)"
  - "Променяйки $p$ от 0 до 1 се проследява път" → "При изменение на $p$ от 0 до 1 се проследява път"
- **Why:** "данък" is masculine, and the choices belong to one agent ("му", not "им"). The adverbial participle "Променяйки" dangles: the path does not change $p$.

### F08-B32 · S2 · poker terms — *hand* as "раздавания/ръка"
- **Where:** summaryBg.md §§ 8.1, 8.8.1
- **Now → Proposed:**
  - "той напълно спира да блъфира определени **раздавания**" → "той напълно спира да блъфира с определени карти"
  - "(+0.051/ръка общо)" → "(+0.051 на раздаване общо)"
  - "стойността на играта на ръка" → "стойността на играта на раздаване"
- **Why:** One bluffs *with* cards, not "bluffs deals" (F07-B20). Elsewhere the chapter measures per "раздаване". "на ръка" also reads as "by hand".

### F08-B33 · S2 · tables — safety-notion table and teaching-attack table
- **Where:** summaryBg.md table after § 8.3 (c); table in § 8.8.1
- **Now → Proposed:**
  - "| Понятие за безопасност | Неформална долна граница | Нужди | Слабост |" → "| Понятие за безопасност | Неформален праг | Изисква | Слабост |"
  - "| Ганцфрид (2015) | $\ge v^*$ | едно *перфектно* Нашево референтно ниво | перфектното Нашево равновесие е неизчислимо в мащаб |" → "| Ганцфрид (2015) | $\ge v^*$ | *точно* равновесие на Наш като базова линия | точното равновесие на Наш е практически неизчислимо в големи игри |"
  - "| Адаптация (2024) | $\le$ експлоатируемост на плана | всеки план | безсмислено, ако планът е лош |" → "| Адаптация (2024) | $\le$ експлоатируемостта на базовата стратегия | произволна базова стратегия | безсъдържателно, ако базовата стратегия е лоша |" (the prime-safe row is in F08-B08)
  - "| метод | средна стойност/ръка (всички) | средна стойност/ръка (след преминаване) | нарушения на безопасността / начално число |" → "| метод | средно на раздаване (общо) | средно на раздаване (след смяната) | нарушения на безопасността / начално число |"
  - "| адаптация | −0.046 |" → "| adaptation | −0.046 |"; "| Нашево равновесие | −0.051 |" → "| nash | −0.051 |"
- **Why:** "Нужди" means wants or necessities; the column says what each notion requires. *Vacuous* is "безсъдържателно", not "безсмислено". The teaching-attack table translated two of its four code ids, while `full_br` and `ganzfried` stay code (as in the Kuhn and Leduc tables); the text refers to all four as code. "след преминаване" is "after passing".

### F08-B34 · S2 · one-pager — English, calques and meaning errors
- **Where:** onePagerBg.md
- **EN:** onePager.md
- **Now → Proposed:**
  - "най-добре реагиращият към несъвършен модел може да отвори пропуск в собствената си игра (непрекъснатият модел *загуби* от Нашево равновесие в Ледюк)" → "най-добрият отговор на несъвършен модел може да създаде уязвимост в собствената игра (непрекъснатият модел *загуби* срещу „Наш“ в Ледюк)"
  - "при условие за праг на безопасност върху най-лошия стойностен случай*" → "при ограничение стойността в най-лошия случай да не пада под прага на безопасност*"
  - "която е линейна по отношение на последователната форма за реализация на героя" → "която е линейна по плана за реализация на агента в последователна форма"
  - "извикване на точен най-добър отговор като най-лошия случай предсказвач → добавяне на разрез, ако е небезопасен" → "извикване на точния най-добър отговор като предсказвач за най-лошия случай → добавяне на отсичащо ограничение, ако стратегията е небезопасна"
  - "Нашево равновесие и „зоологията“ на противниците" → "равновесието на Наш и „зоопарка“ от типове противници"
  - "**SES** (стойност на плана, наложена локално върху под-игра чрез джаджа), **adaptation** (не по-експлоатируем от плана)" → "**SES** (стойността на базовата стратегия, наложена локално в под-игра чрез приспособление), **адаптация** (не по-експлоатируема от базовата стратегия)"
  - "Тестови среди: Kuhn и Ледюк" → "Тестови среди: Кун и Ледюк"
  - "така че всеки резултат е ограничен от точни аналитични препратки" → "така че всеки резултат е поставен в точни аналитични граници"
  - "*Безопасното използване работи в Kuhn.*" → "*Безопасната експлоатация работи в Кун.*"
  - "*ε се измерва, а не се конструира.* Prime-safe/adaptation понижават" → "*ε се измерва, а не се приема наготово.* Prime-safe и адаптацията понижават"
  - "*Каноничният RNR е превключващ, а не с гладка граница* (противоречащо предсказание). В игра толкова малка, LP max-min скача" → "*Каноничният RNR превключва скокообразно, а не по плавна граница* (предсказанието не се потвърди). В толкова малка игра максиминната LP-задача скача"
  - "*Заглавие - глобалната безопасна експлоатация не се мащабира; локалната да.* В **Ледюк**, глобалните решаващи (Ganzfried/prime-safe/adaptation) **не успяват да се сближат в рамките на 40 итерации**" → "*Основен резултат - при лимит от 40 итерации глобалните решавачи не достигат сходимост, а локалният метод (с лимит 400) достига.* В **Ледюк** глобалните решавачи (Ganzfried/prime-safe/адаптация) **не достигат сходимост в рамките на 40 итерации**" (content: F08-C02)
  - "**методът на под-играта (SES) се сближава**" → "**методът на под-играта (SES) достига сходимост**"
  - "нежен разкривател на равновесие на Наш никога не си връща вятърничавата печалба от фазата на примамка. За наказателен тест е необходим адаптивен контраексплойтър." → "„разкриващият“ противник, който просто играе равновесие на Наш, е твърде мек и не си връща неочакваната печалба на full_br от фазата на примамката. За наказващ тест е необходим адаптивен контраексплоататор."
  - "несъходимостта на Ледюк" → "липсата на сходимост в Ледюк"; "точна двойствена линейнопрограмна задача, като същевременно" → "точна двойнствена LP-задача, като същевременно"
  - "(точна двойствена линейнопрограмна задача срещу подлокална игра - стената на Ледюк)" → "(точна двойнствена LP-задача срещу локална безопасност в под-игра - „стената“ на Ледюк)"
  - "(0.04 > tol - доказуемо или само приблизително безопасен?)" → "(0.04 > допустимото отклонение - доказуемо или само приблизително безопасно?)"
  - "факта за двуигрови игри с нулева сума, че равновесието на Наш осигурява" → "факта, валиден за игри с нулева сума за двама играчи, че равновесието на Наш осигурява"
- **Why:**
  - Meaning errors: "вятърничавата печалба" (*flighty* profit) for *windfall*; "подлокална игра" (a "sub-local game") for *local/subgame*; "Заглавие" (a title) for *headline*; "зоологията" (the science) for *zoo*; "се сближават" (grow closer, befriend) for *converge*.
  - English: "Kuhn", "adaptation", "tol".
  - "Безопасното използване" (safe *use*) is T07; "джаджа" is a gadget in the gizmo sense, which the candidate already rejected for the heading (Aug 2026 comment, TOC p. 7).
  - "линейна по … последователната форма за реализация" drops *plan*.
  - The other items repeat F08-B05–B25.

### F08-B35 · S3 · polish
- **Where:** summaryBg.md §§ 8.6, 8.7
- **Now → Proposed:**
  - "бъде **надолу-затворена** (веднъж щом сте в нея, оставате в нея)" → "бъде **затворена надолу** (веднъж влезли в нея, оставате в нея)"
  - "решава всеки метод срещу *перфектен* модел" → "решава всеки метод срещу *точен* модел"
- **Why:** "затворено надолу" is the usual word order for the order-theoretic term. "веднъж щом" doubles the conjunction. *Perfect* model = an exact one.

## T — Glossary-level terminology

### F08-T01 · S1 · "bang-bang → изненадващ обрат"
- **Where:** `llmPipeline/glossary_settled.md`: "bang-bang → изненадващ обрат", "bang-bang frontier → граница „включено–изключено“", "bang-bang threshold → праг „включено–изключено“". Printed on pp. 156–157 and 161 (F08-B27).
- **Now → Proposed:** bang-bang → "скокообразен (превключване тип „всичко или нищо“)"; bang-bang frontier → "скокообразно превключване" (after F08-C05 the frontier itself is not bang-bang); bang-bang threshold → "праг на превключване"
- **Why:** "изненадващ обрат" means "a surprising twist". It is a paraphrase of the chapter's "measured surprise", not a translation of the control-theory term.

### F08-T02 · S1 · "two-player → двуигрови" and the N-player family (one entry in mixed script)
- **Where:** glossary_settled.md: "two-player → двуигрови", "N-player settings → N-игрова среда", "N-player bound → N-играторска граница", "n-player → n-играчeн". The last contains a **Latin "e"**: bytes `d187 65 d0bd` between "ч" and "н". Printed in F08-B26 and the one-pager.
- **Now → Proposed:** two-player → "за двама играчи" ("игра с нулева сума за двама играчи"); N-player → "с N играчи" ("игра с N играчи", "граница при N играчи", "среда с N играчи")
- **Why:** "двуигрови" means "two-game" and "N-игрова" means "N-game". The correct phrase "игра за двама" is already a settled entry ("two-player zero-sum → игра за двама с нулева сума"), so the same corpus now has both forms. Fix the Latin letter in the picker, as for F07-B37's "типoв".

### F08-T03 · S2 · "worst-case value → най-лошият стойностен случай"
- **Where:** glossary_settled.md (freq 8); ch. 8 §§ 8.1, 8.2 and the one-pager (F08-B10, F08-B11, F08-B25, F08-B34)
- **Now → Proposed:** → "стойност в най-лошия случай"
- **Why:** "the worst value-case" is a word-by-word calque. Chapter 8's own table caption already uses the right form.

### F08-T04 · S2 · *blueprint*: "Схема", "план", "план-стратегия", "план за долна граница"
- **Where:** curated `terminology_EN_BG.md` "Blueprint (strategy) → Схема (на стратегията)". Settled: "blueprint strategy → план-стратегия", "blueprint floor → план за долна граница", "blueprint architecture → архитектурен план". Chapters 06 and 08 print "план".
- **Now → Proposed:** blueprint → "базова стратегия (blueprint)"; blueprint floor → "праг на базовата стратегия"
- **Why:** The curated file and the settled glossary disagree, and the bundle follows neither consistently. "план" collides with "план за реализация" (realization plan) inside chapter 8's §§ 8.2 and 8.7. "план за долна граница" says "a plan for a lower bound", and "схема" suggests a diagram.

### F08-T05 · S2 · curated SES expansion is wrong
- **Where:** `terminology_EN_BG.md`, abbreviations table: "SES | Safe Exploitation Subgame | Безопасна експлоатация на под-игри"
- **Now → Proposed:** → "SES | Safe Exploitation Search | Търсене на безопасна експлоатация"
- **Why:** Liu et al. (NeurIPS 2022) name it "a novel real-time search framework, called Safe Exploitation Search (SES)" (verified on the NeurIPS abstract page). Chapter 8 already uses the right name.

### F08-T06 · S2 · curated "Restricted Nash Response → Ограничен Наш отговор"
- **Where:** `terminology_EN_BG.md` (method table and abbreviations table); settled has "restricted nash response → ограничен отговор по Наш" (freq 9), which chapter 8 uses.
- **Now → Proposed:** curated → "ограничен отговор по Наш (RNR)"
- **Why:** "Наш отговор" reads as "our response" (the F07-B02 problem). The settled form avoids it, so the two files should agree on it.

### F08-T07 · S2 · *safe exploitation* as "безопасно използване"
- **Where:** glossary_settled.md: "safe-exploitation solver → решавач за безопасно използване", "safe-exploitation analysis → анализ на безопасното експлоатиране". Printed as "Безопасното използване" in § 8.9 and the one-pager (F08-B34).
- **Now → Proposed:** → "решавач за безопасна експлоатация", "анализ на безопасната експлоатация"
- **Why:** The curated term is "безопасна експлоатация". "използване" (use) loses the strategic sense and puts two terms into one chapter.

### F08-T08 · S2 · "cutting-plane → равнина на отсичане"; no entry for *cut*
- **Where:** glossary_settled.md; ch. 8 uses "сечение", "срез", "разрез", "cut" (F08-B22)
- **Now → Proposed:** cutting-plane → "отсичаща равнина"; cutting-plane method/loop → "метод на отсичащите равнини"; new entry *cut* → "отсичащо ограничение"
- **Why:** These are the standard Bulgarian OR forms. The missing *cut* entry is why five renderings appear.

### F08-T09 · S3 · "gadget game → игра с джаджа"
- **Where:** glossary_settled.md; the one-pager's "чрез джаджа"
- **Now → Proposed:** → "игра с приспособление (gadget)"
- **Why:** "джаджа" is colloquial ("gizmo"). The candidate replaced "джаджи" in the heading (Aug 2026 comment "решаване на под игри"), and settled "gadget → приспособление" already exists.

### F08-T10 · S3 · "exploiters → експлоатьори", "counter-exploiter → контраексплойтър"
- **Where:** glossary_settled.md; ch. 8 § 8.8.1 and the one-pager
- **Now → Proposed:** → "експлоататори", "контраексплоататор"
- **Why:** Chapter 7 settled on "експлоататор" (F07-B36). Two transliterations of one English word now print in adjacent chapters.

## C — Content

### F08-C01 · S1 · "Ganzfried" is Ganzfried & Sandholm's *best-equilibrium* baseline, not their safe exploitation algorithm
- **Where:** summaryBg.md / summaryEn.md § 8.3 (a) (EN l. 122–133); § 8.6 ("the core result"); table after § 8.3; fig. 39 row "Ganzfried".
- **Problem:**
  - The constraint EV$(x,\sigma') \ge v^*$ for all $\sigma'$ is imposed on each hand's strategy. In a two-player zero-sum game it admits only maximin (equilibrium) strategies, so the LP returns the equilibrium strategy that does best against the model. In Kuhn this is the best member of P1's one-parameter family of equilibria.
  - Ganzfried & Sandholm define safety over the *repeated* game (Def. 4.1: "a worst-case payoff of at least $v_i$ per period in expectation"). Their safe exploitation algorithms (RWYW, RWYWE, BEFFE) deviate *beyond* equilibrium by risking only the gifts already won.
  - The per-hand version is their § 6.3 "Best Equilibrium Strategy" baseline: "This would clearly be safe, but can only exploit the opponent as much as the best equilibrium can, and potentially leaves a lot of exploitation on the table." Their abstract reports that "aggressive safe exploitation strategies significantly outperform adjusting the exploitation within stage-game equilibrium strategies only".
  - The chapter's explanation ("deviate … within the 'slack' the opponent's mistakes create (their gifts)") describes the RWYWE mechanism, which is not implemented. This is why the "core result" gains so little: +0.002 per hand against the Rock and AlwaysBet (F08-C07).
  - Verified in the full text (the author PDF at cs.cmu.edu, ACM TEAC 3(2), Art. 8) and in Crossref.
- **Now → Proposed:**
  - BG: "**(а) Сигурност при ганцфрид (2015): никога да не се печели по-малко от стойността на играта.** При *перфектно* Нашево равновесие $\sigma^*$ като базова линия, изискването е" → "**(а) Безопасност по Ганцфрид и Сандхолм (2015): никога да не се печели по-малко от стойността на играта.** Определението им се отнася до повтарящата се игра: средно поне $v^*$ на раздаване, каквото и да прави противникът. Тук то се налага на стратегията за всяко отделно раздаване, с точно равновесие на Наш $\sigma^*$ като базова линия:"
  - BG: "Това е най-силната и най-чистата концепция. Нейното доказателство се основава на **теоремата за минимакс**: в двуигрови игра с нулева сума Нашевата стратегия *гарантира* стойността $v^*$ срещу всеки противник, така че човек може да се отклони към експлоатация на модела в рамките на „хлабината“, създадена от грешките на противника (техните *подаръци*) и никога да не падне под $v^*$. Уловката е предпоставката: *перфектно* Нашево равновесие, което е неизчислимо във всяка голяма игра." → "Това е най-силното и най-чистото понятие. То се опира на **теоремата за минимакса**: в игра с нулева сума за двама играчи равновесната стратегия на Наш *гарантира* стойността $v^*$ срещу всеки противник. На прага за всяко отделно раздаване обаче отговарят само равновесните стратегии, затова методът избира онази равновесна стратегия, която печели най-много срещу модела (вариантът „най-добро равновесие“ при Ганцфрид и Сандхолм). Пълните им алгоритми отиват по-далеч: отклоняват се от равновесието, като рискуват само „подаръците“ (грешките на противника), вече спечелени в предходните раздавания. Уловката е в предпоставката: нужно е точно равновесие на Наш, а то е практически неизчислимо във всяка голяма игра."
  - EN l. 122–123: "**(a) Ganzfried safety (2015): never earn less than the game value.** With a *perfect* Nash equilibrium $\sigma^*$ as baseline, require" → "**(a) Ganzfried–Sandholm safety (2015): never earn less than the game value.** Their definition is over the repeated game: at least $v^*$ per hand in expectation, whatever the opponent does. Here it is imposed on each hand's strategy, with an exact Nash equilibrium $\sigma^*$ as baseline:"
  - EN l. 129–133: replace "so one can deviate toward exploiting the model within the "slack" the opponent's mistakes create (their *gifts*) and never fall below $v^*$. The catch is the premise: a *perfect* Nash equilibrium, which is uncomputable in any large game." with "Only equilibrium strategies meet this per-hand floor, so the method picks the equilibrium strategy that does best against the model (Ganzfried and Sandholm's "best equilibrium" baseline). Their full algorithms go further: they deviate beyond equilibrium by risking only the *gifts* (the opponent's mistakes) already banked in earlier hands. The catch is the premise: an exact Nash equilibrium, which is not computable in practice in any large game."
  - Optional, recommended for the thesis: add Ganzfried & Sandholm's RWYWE as a method. It is the stronger two-player baseline for C2, and it needs only the existing LP with floor $v^* - k_t$.

### F08-C02 · S1 · The Leduc headline compares a 40-iteration cap with a 400-iteration one
- **Where:** summaryBg/En § 8.8 (headline, SES paragraph), § 8.7 last sentence, § 8.9, one-pager "Headline"; fig. 43.
- **Problem:**
  - `leduc_bounded_scale.json`: every global cell has `iterations: 40, capped: true` and a `solve_seconds` of 2.3–3.0. SES ran 194, 211, 350 and 400 iterations (`capped: false`) in 29.6–78.5 s.
  - The summary itself says the run used "a 40-iteration budget on the constraint-generation loop" (l. 369–370), then reports SES converging in 194–350 iterations.
  - "global safe-exploitation does not scale, even to Leduc" and "the difference between a solve that converges and one that does not" therefore rest on unequal budgets. report_en § 11, caveat (2), says so ("not that it can never reach safety given far more"); the summary and one-pager do not.
- **Now → Proposed:**
  - BG: "**Основната констатация е отрицателна и емпирична: глобалната безопасна експлоатация не се мащабира, дори до Ледюк.**" → "**Основната констатация е отрицателна и емпирична: при лимит от 40 итерации глобалното решаване не достига сходимост дори в Ледюк.**"
  - BG: "- конкретният аргумент за методите за под-игри в реално време и против наивно глобално решаване." → "- конкретният аргумент за методите за под-игри в реално време и против наивно глобално решаване. Сравнението обаче не е при равни условия: глобалните решавачи са спрени след 40 итерации (около 2.5 s на клетка), а SES е имал лимит 400 и е използвал 194–400 итерации (30–79 s на клетка). Резултатът показва, че глобалният цикъл е бавен и небезопасен *в рамките на този бюджет*, а не че не може да достигне безопасност при по-голям."
  - BG: "§8 показва, че именно то определя дали решаването ще **успее** или няма да успее." → "§ 8.8 показва, че в Ледюк решаването на под-игра достига сходимост в рамките на своя бюджет, а глобалното - не."
  - EN l. 390–391: "global safe-exploitation does not scale, even to Leduc." → "within a 40-iteration cap, the global solve did not converge even on Leduc."; after l. 406 add the same caveat sentence; l. 360–361 → "§8 shows that, on Leduc, the subgame solve converged within its budget and the global solves did not converge within theirs."
  - EN one-pager l. 45: "*Headline — global safe-exploitation does not scale; local does.*" → "*Headline — within a 40-iteration cap the global solvers did not converge on Leduc; the subgame method (cap 400) did.*" (BG: F08-B34)

### F08-C03 · S2 · The SES text credits Liu et al. with Ge et al.'s guarantee
- **Where:** § 8.7, EN l. 345–351; footnotes `liu2022`, `search2024`.
- **Problem:**
  - Liu et al. do not guarantee that SES is never worse than the blueprint. Their Theorem 4.1 is an *additive* bound: exp$(\sigma'_2) \le$ exp$(\sigma^*_2) + \frac{2}{1-(2\tau+1)\alpha}\Delta$. It grows with the exploitation level α and the reach-estimation error τ, and is relative to the constrained NE σ*₂, not to the blueprint.
  - The guarantee the chapter states, exp$(\sigma') \le$ exp$(\sigma)$, is Ge et al.'s adaptation safety (their Def. 4.1), achieved by OX-Search (their Theorem 4.3). Ge et al. write of Liu et al. that "their strategies may not always guarantee safety".
  - The chapter's `ses_subgame` (pins + floor = blueprint worst case, solved exactly) is an adaptation-safe subgame re-solve, closer to OX-Search than to SES.
  - Verified in both full texts (NeurIPS 2022 PDF; PMLR v235 PDF).
- **Now → Proposed:**
  - BG: "с **приспособление**, което гарантира, че локалното отклонение никога не може да направи героя по-зле *глобално* от плана." → "с **приспособление**, което ограничава отгоре колко локалното отклонение може да увеличи експлоатируемостта (границата расте с нивото на експлоатация и с грешката на модела на противника). По-строгата гаранция, използвана тук - никога да не си по-експлоатируем от базовата стратегия, - е безопасността на адаптацията на Ge и др., която техният метод OX-Search постига при повторното решаване на под-игри."
  - BG: "В последователна форма приспособлението се реализира директно върху treeplex:" → "Реализацията в тази глава налага тази по-строга гаранция директно върху дървовидния политоп:"
  - EN l. 347–348: "with a **gadget** that guarantees the local deviation can never make the hero worse off *globally* than the blueprint." → "with a **gadget** that bounds how much the local deviation can add to exploitability (the bound grows with the exploitation level and the error of the opponent model). The stricter guarantee used here — never more exploitable than the blueprint — is Ge et al.'s adaptation safety, which their OX-Search achieves for subgame re-solving."; l. 350 "In sequence form the gadget is realized directly on the treeplex" → "The implementation here enforces that stricter guarantee directly on the treeplex"
  - Optional: rename the method column `ses_subgame` → "subgame (adaptation-safe)" in the text, keeping the code id.

### F08-C04 · S2 · The "top open item" on SES names the wrong blueprint; the chapter's own run largely answers it
- **Where:** § 8.8, EN l. 408–413.
- **Problem:**
  - The SES floor is the worst case of the *blueprint*, and in `tournament.py` l. 86 the blueprint is `make_epsilon_equilibrium(game, cfg["epsilon_baseline_iters"])` — an early-stopped CFR (800 iterations on Leduc), not the 40 000-iteration Nash (worst case −0.089) the text names.
  - `EXECUTION_NOTES.md` (Leduc bounded run) records that blueprint's worst case as −0.1197 and reads SES as "at the blueprint's own guarantee (−0.1197) within the 1e-2 tolerance".
  - The three converged cells sit at −0.1297/−0.1296/−0.1296, i.e. 0.010 below their own floor, exactly at the tolerance. The "residual 0.043" is measured against $v^*$ and is mostly the blueprint's own exploitability (≈ 0.034).
  - The −0.1197 value is not in the JSON; re-derive it before stating it.
- **Now → Proposed:**
  - BG: "Дали този остатък от 0.04 представлява приспособлението, което легитимно се ограничава до вече под-$v^*$ план (най-лошият случай на самото **Нашево равновесие** е −0.089, което е с 0.003 под $v^*$), артефакт от толерантността при **сходимост** или малко изтичане във външното поддеревно фиксиране е основният въпрос за разрешаване, преди SES да бъде обявен за *доказуемо* **безопасен**." → "Това нарушение обаче се мери спрямо $v^*$. Собственият праг на SES е стойността в най-лошия случай на базовата стратегия - тук това е спряното преждевременно CFR (−0.120), а не равновесието на Наш (−0.089) - и трите клетки със сходимост са с 0.010 под този праг, т.е. точно на границата на допустимото отклонение 0.01. Следователно SES е спазил своя праг в рамките на допустимото отклонение, а остатъкът се дължи главно на експлоатируемостта на самата базова стратегия; дали методът е *доказуемо* безопасен, ще покаже повторно изпълнение с по-малко допустимо отклонение."
  - EN l. 410–413: replace "Whether that residual 0.04 is the gadget legitimately bounding … before calling SES *provably* safe." with "That violation is measured against $v^*$, though. SES's own floor is the blueprint's worst case — here the early-stopped CFR baseline (−0.120), not the Nash strategy (−0.089) — and the three converged cells sit 0.010 below it, exactly at the 0.01 tolerance. So SES held its gadget floor to within the tolerance, and the residual is mostly the blueprint's own exploitability; a rerun with a tighter tolerance would show whether it is *provably* safe."
  - Report § 10 and § 12 item 2 carry the same misreading.

### F08-C05 · S2 · "Bang-bang frontier": what is bang-bang is the map from p to a strategy, shown on an 11-point grid
- **Where:** § 8.5 heading, lead and "Why" paragraph (EN l. 224, 247–276); one-pager bullet 3.
- **Problem:**
  1. `pareto_kuhn.json` samples $p \in \{0, 0.1, …, 1\}$. With the two vertices found (EV −0.0444 / exploitability 0 and +0.1667 / 0.4444), the RNR objective switches where $p\cdot\Delta$EV $= (1-p)\cdot\Delta$expl, i.e. at $p \approx 0.678$. Any further vertex would be optimal only for $p$ inside (0.6, 0.7), which was not sampled. "There are no intermediate points" is true of the grid only.
  2. The *frontier* is not bang-bang. Johanson et al. (2007) define the mixture of two strategies (their Eq. 3) and prove each $p$-RNR is an ε-safe best response (Theorem 1). Mixing the two RNR strategies reaches every point of the chord between the corners, because EV is linear in the mixture and the worst case is concave. The discrete jumps are how a linear objective traces a concave frontier, in any game.
  3. In Kuhn against TightPassive the chord lies only ≈ 0.002 above the naive blend (the blend is exactly linear: 0.02133 EV and 0.0445 exploitability per step of 0.1). So "choose *where* to deviate, not *how much* uniformly" gains about nothing here. The text says "the headline lesson survives", but this game does not show it.
  4. Johanson et al. report "highly concave" curves "meaning that dramatic reductions in exploitability can be achieved with only a small sacrifice", measured in an abstracted Texas hold'em game. Verified in the NIPS 2007 full text (poker.cs.ualberta.ca PDF).
- **Now → Proposed:**
  - Heading and lead: F08-B27; "no intermediate points": F08-B01.
  - BG: "Основният извод остава - „избери *къде* да се отклониш, а не *колко* равномерно“ - но механизмът („гладък RNR циферблат“) е артефакт от големи игри и в малка игра честната картина е дискретен преход от безопасен връх към BR-връх, чийто праг *се измества според това колко експлоатируем е противникът*." → "Скокообразно обаче е само съответствието между $p$ и стратегията, а не самата граница: смесването на двете RNR стратегии (Йохансон и др. дефинират такова смесване) достига всяка точка от отсечката между двата ъгъла, защото очакваната стойност е линейна по смесването, а стойността в най-лошия случай е вдлъбната. При двата намерени върха превключването става при $p \approx 0.68$, а евентуален междинен връх би бил оптимален само за $p$ между 0.6 и 0.7, където обхождането не е проверявало. В Кун срещу „камък“ тази отсечка е само с около 0.002 над наивното смесване, така че тук изборът *къде* да се отклониш почти не носи предимство пред равномерното смесване; силно вдлъбнати граници Йохансон и др. отчитат в голяма абстрахирана игра на холдем. Малката игра показва друго: $p$ не е плавна скала - стратегията превключва от безопасния връх към BR-върха при праг, който *се измества според това колко експлоатируем е противникът*."
  - EN l. 272–276: the same content — "What is bang-bang is the map from $p$ to a strategy, not the frontier: mixing the two RNR strategies (Johanson et al. define this mixture) reaches every point on the chord, because EV is linear in the mixture and the worst case is concave. With the two vertices found, the switch happens at $p \approx 0.68$; any further vertex would be optimal only for $p$ between 0.6 and 0.7, which the sweep did not sample. Against the Rock the chord lies only ≈ 0.002 above the naive blend, so here choosing *where* to deviate buys almost nothing over uniform scaling; Johanson et al. report strongly concave frontiers in a large abstracted hold'em game. What the small game does show is that $p$ is not a dial: the strategy switches from the safe vertex to the BR vertex at a threshold that *moves with how exploitable the opponent is*."
  - EN l. 224: "## Restricted Nash Response and the Bang-Bang Frontier" → "## Restricted Nash Response and the Bang-Bang Switch"

### F08-C06 · S2 · "The single unsafe method in the table" is false
- **Where:** § 8.6 item 1 (EN l. 308–309)
- **Problem:** In the same table `rnr_0.5` is unsafe against three of the five opponents (worst case −0.111, −0.167, −0.333), which item 3 itself states. prime-safe and adaptation are flagged unsafe against $v^*$ in every row.
- **Now → Proposed:**
  - BG: "Това е единственият експлоатируем метод в таблицата и той е експлоатируем срещу *всеки* противник, защото противникът винаги може оптимално да отговаря обратно на дупката, която той отваря." → "Това е единственият метод, който е небезопасен срещу *всеки* противник (`rnr_0.5` е небезопасен срещу три от петте), защото противникът винаги може да отговори с най-добър отговор на уязвимостта, която той създава."
  - EN l. 308–309: "It is the single unsafe method in the table, and it is unsafe against *every* opponent" → "It is the only method that is unsafe against *every* opponent (`rnr_0.5` is unsafe against three)"

### F08-C07 · S2 · "Keep most of the upside" and "exploit meaningfully" overstate the core result
- **Where:** § 8.1 (EN l. 62–63), § 8.6 item 2 (EN l. 313–314)
- **Problem:** From `kuhn_scale.json`, Ganzfried's gain over the Nash strategy is:
  - +0.0024 against TightPassive (1 % of the best response's headroom of 0.213)
  - +0.0023 against AlwaysBet (1 %)
  - +0.013 against LooseAggressive (6 %)
  - +0.076 against AlwaysPass (9 %)
  - +0.004 against Thresholdish, a sixth type in the JSON that the table omits (9 %)

  § 8.1's example — "keeping most of that +0.167 upside" against the Rock — is the case where it keeps ≈ 1 %. This follows from F08-C01: a per-hand floor at $v^*$ only chooses among equilibria.
- **Now → Proposed:**
  - BG: "**Безопасна експлоатация** е дисциплината да се запази по-голямата част от този +0.167 потенциал за печалба, като същевременно се избягва −0.5 потенциала за загуба." → "Безопасната експлоатация е дисциплината да се вземе от този потенциал толкова, колкото позволяват грешките на противника, без да се поема рискът от −0.5."
  - BG: "Това е резултатът, който стъпката съществува, за да произведе: *можете да експлоатирате смислено, като доказуемо никога не падате под равновесната стойност.*" → "Именно този резултат е целта на главата: *може да се експлоатира, като доказуемо никога не се пада под равновесната стойност* - но печалбата е малка: срещу четирите експлоатируеми типа Ганцфрид печели с 0.002–0.076 на раздаване повече от Наш, т.е. 1–9% от онова, което печели пълният най-добър отговор."
  - EN l. 62–63: "Safe exploitation is the discipline of keeping most of that +0.167 upside while refusing the −0.5 downside." → "Safe exploitation is the discipline of taking as much of that upside as the opponent's mistakes allow while refusing the −0.5 downside."
  - EN l. 313–314: "This is the result the step exists to produce: *you can exploit meaningfully while provably never dropping below equilibrium value.*" → "This is the result the chapter set out to produce: *you can exploit while provably never dropping below equilibrium value* — but only a little: against the four exploitable types Ganzfried gains 0.002–0.076 per hand over Nash, 1–9 % of what the full best response gains."

### F08-C08 · S2 · Prime-safe and adaptation coincide by definition, not as a finding of the run
- **Where:** § 8.6 parenthesis (EN l. 326–329); report § 8
- **Problem:**
  - `prime_safe.py` l. 50–52 defines ε := $v^*$ − worst_case(baseline), so $v^* - \varepsilon$ *is* the baseline's worst case, for every baseline.
  - `tournament.py` passes the same early-stopped CFR strategy as the prime-safe baseline and the adaptation blueprint.
  - Jeary & Turrini's abstract ("we redefine the value of the game of a player to be the worst-case payoff their strategy could be susceptible to") and Ge et al.'s Def. 4.1 (exp$(\sigma') \le$ exp$(\sigma)$) state the same floor whenever the baseline and the blueprint are one strategy.
  - "for this baseline" and "which the run confirms rather than a bug" present an identity as an empirical result. § 8.3 and its table present them as two different floors.
- **Now → Proposed:**
  - BG (also replaces the corrupted "⟦MATHI5⟧", F08-B01): "(Безопасен спрямо прайм и адаптацията съвпадат тук, защото за тази базова линия ⟦MATHI5⟧ - двете долни граници са буквално равни, което изпълнението потвърждава, а не е грешка.)" → "(Prime-safe и адаптацията съвпадат по конструкция: $\varepsilon$ се определя като $v^*$ минус стойността на базовата линия в най-лошия случай, така че $v^* - \varepsilon$ е точно тази стойност, а реализацията използва една и съща стратегия (CFR, спрян преждевременно) и като базова линия за prime-safe, и като базова стратегия за адаптацията. Праговете на Jeary и Turrini и на Ge и др. съвпадат винаги, когато двете са една и съща стратегия; разликата е в приложението - алгоритми за цялата игра срещу повторно решаване на под-игри.)"
  - EN l. 326–329: the same parenthesis in English — "(Prime-safe and adaptation coincide by construction: ε is defined as $v^*$ minus the baseline's worst case, so $v^* - \varepsilon$ is that worst case, and the implementation uses the same early-stopped CFR strategy as the prime-safe baseline and the adaptation blueprint. Jeary & Turrini's floor and Ge et al.'s coincide whenever the two are the same strategy; they differ in setting — whole-game exploitation algorithms versus subgame re-solving — not in the floor.)"

### F08-C09 · S2 · N-player paragraph: "their payoffs no longer sum to the negative of yours" is false for zero-sum games, and the open problem is stated as unexplored (lit_gaps C2)
- **Where:** § 8.3.1 (EN l. 173–178); one-pager "Open questions"
- **Problem:**
  1. In an N-player *zero-sum* game — including the three-player Kuhn/Leduc the thesis plans — the other players' payoffs *do* sum to the negative of yours. What fails is that no *single* opponent's payoff is the negative of yours, so there is no two-player minimax value. Equilibria are also not unique and give different payoffs.
  2. "whether an N-player analogue of the value guarantee exists" is posed as unexplored. `lit_gaps.md` (C2, "Narrowed") shows N-player safety notions exist: team-maxmin values against a coordinated coalition, and equal share, which is provably not securable against opponents playing different fixed strategies. The open part is exploitation *combined with* a baseline-relative loss bound, tested against colluding opponents.
- **Now → Proposed:**
  - BG: "(другите могат да координират действията си и техните печалби вече не се сумират до отрицанието на твоята), така че няма единна $v^*$, към която да се закотви. **Това е отвореният проблем за Принос №2** - дали съществува аналог на гаранцията за стойност в $N$-игрова игра или структурно предположение (например коалиционна структура) трябва да възстанови опорната точка." → "(печалбата на отделния противник вече не е равна на вашата със знак минус - в игра с нулева сума това важи само за сумата от печалбите на всички противници, - затова противниците могат да действат координирано срещу вас, а различните равновесия ви носят различни печалби), така че няма единна $v^*$, към която да се закотви. Равновесията в игри с повече от двама играчи не са „нито единствени, нито неексплоатируеми“[^ge2025]. Понятия за безопасност при $N$ играчи съществуват, но са или много консервативни (максиминната стойност срещу координирана коалиция[^celli2018]), или доказано непостижими срещу противници с различни фиксирани стратегии (равният дял[^ge2025]). **Това е отвореният проблем за Принос №2** - експлоатация на слаби противници в малки игри с $N$ играчи при ограничена загуба спрямо базова стратегия, включително срещу противници, действащи в сговор."
  - New footnotes, in both files:
    - `[^ge2025]: Ge, J., Wang, Y., Li, W. & Jin, C. (2025). "Securing Equal Share: A Principled Approach for Learning Multiplayer Symmetric Games." *ICML*; arXiv:2406.04201.`
    - `[^celli2018]: Celli, A. & Gatti, N. (2018). "Computational Results for Extensive-Form Adversarial Team Games." *AAAI* 32(1). DOI 10.1609/aaai.v32i1.11462.`
    - Verification: Ge — the arXiv abstract ("equilibria in multiplayer games are neither unique nor non-exploitable") and HTML v2 (Prop. 4.1: "There exist symmetric zero-sum games with opponents using fixed but differing strategies, such that no learner's strategy secures an equal share"); the ICML 2025 venue is per `lit_gaps.md`. Celli & Gatti — Crossref.
    - Neither label occurs in other chapters (checked), so they add no F07-X01 collision.
  - EN l. 175–178: the same content in English.

### F08-C10 · S2 · Stale "Step" naming
- **Where:**
  - EN: l. 185 "The one primitive the whole step adds", l. 313 "the step exists to produce" (F08-C07), l. 419 "a Step-7 model feeds each solver", l. 456 "But the step's most valuable result".
  - BG: "Единствената примитивна операция, която цялата стъпка добавя" (§ 8.4).
  - Alt texts and figure labels: F08-G01–G03.
  - report_en § 5 and § 9 also say "a Step-7 model".
- **Now → Proposed:**
  - "Единствената примитивна операция, която цялата стъпка добавя, е `HeroTreeplex`" → "Единствената нова елементарна операция, която главата добавя, е `HeroTreeplex`"
  - EN "step" → "chapter", "Step-7 model" → "Chapter 7 model"
- **Why:** The bundle says "Глава"; the candidate asked for this change in his Aug 2026 comment on TOC p. 2 ("maybe its time to change all emntion of steps into chapters").

## S — Sources

### F08-S01 · S2 · SOURCE_GAPS row: "Резултатите на Кун потвърждават коректността на изпълнителния механизъм" → soften (own result)
- **Where:** summaryBg.md § 8.9 — "Резултатите на Кун потвърждават коректността на изпълнителния механизъм;"; EN l. 468 "The Kuhn results confirm the actuator is sound;"
- **Proposal (soften):** This is the chapter's own measurement, so no citation applies. "confirm … sound" overclaims from perfect models in one exactly solvable game with a per-hand floor (F08-C01).
  - "Резултатите на Кун потвърждават коректността на изпълнителния механизъм;" → "Резултатите в Кун показват, че изпълнителният механизъм работи според теорията (при точен модел на противника и в игра, която може да се реши точно);"
  - EN → "The Kuhn results show the actuator behaves as the theory predicts (with a perfect opponent model, in an exactly solvable game);"

### F08-S02 · S2 · Shoham & Leyton-Brown footnote cites the wrong sections (this chapter's copy of F07-S05)
- **Where:** summaryBg.md footnote `shoham2008` — "Гл. 3–4 (игри в нормална и разгърната форма); гл. 5 (игри в разгърната форма); §3.4 (изчисляване на равновесия) и §4.6 (изчисляване на най-добри отговори) - механизмът в последователна форма под всяка линейна програма в Глава 8;"; EN l. 479 identical in English.
- **Problem:** Same text as the step-07 footnote, checked in F07-S05 against masfoundations.org/toc.html. Ch. 4 is "Computing Solution Concepts of Normal-Form Games"; § 3.4 is "Further solution concepts for normal-form games"; § 4.6 is "Computing correlated equilibria". The sequence form is § 5.2. In the bundle this footnote prints only in chapter 1 (shared label, F07-X01), but both source files need the fix.
- **Proposal (correct):** "Гл. 3–4 (игри в нормална и разгърната форма); гл. 5 (игри в разгърната форма); §3.4 (изчисляване на равновесия) и §4.6 (изчисляване на най-добри отговори) - механизмът в последователна форма под всяка линейна програма в Глава 8;" → "Гл. 3 (игри в нормална форма); гл. 4 (изчисляване на решения на игри в нормална форма, §4.1 - линейно програмиране за игри с нулева сума); гл. 5 (игри в разгърната форма; §5.2 - игри с непълна информация и последователната форма, механизмът под всяка LP-задача в Глава 8);" The same in the EN footnote.

### F08-S03 · S2 · `ganzfried2015`: "first made … a theorem" overclaims; the venue is incomplete; the description misses what the paper proves
- **Where:** summaryBg.md — "статията, която за първи път формулира като теорема принципа „експлоатирай, но никога не губи спрямо базовата линия“"; EN l. 477 "the paper that first made "exploit but never lose to the baseline" a theorem".
- **Problem:**
  - McCracken & Bowling (2004) proposed ε-safe strategies earlier (F07-S06). Ganzfried & Sandholm themselves cite them and say prior work had (incorrectly) held safe deviation impossible.
  - Their contribution is to show that safe deviation is possible exactly when "gift" strategies exist, and to give algorithms for the repeated game. Verified in the full text (TEAC 3(2), Art. 8) and in Crossref (DOI 10.1145/2716322).
- **Proposal (soften and complete):**
  - "статията, която за първи път формулира като теорема принципа „експлоатирай, но никога не губи спрямо базовата линия“" → "статията, която показва, че в повтаряща се игра за двама с нулева сума отклонението от равновесието може да е безопасно точно когато противникът прави „подаръци“, и дава алгоритми, които рискуват само вече спечеленото"
  - Add "3(2), статия 8. DOI 10.1145/2716322" after the journal name.
  - EN correspondingly.

### F08-S04 · S2 · Citation metadata (lit_gaps "Citation corrections" and spot-check)
- **Where:** footnotes `jeary2023`, `liu2022`, `milec2025`, `safe2024`, `johanson2007`, `johanson2009`, `gordon2003` (EN and BG)
- **Findings and fixes:**
  - `jeary2023`: "Jeary, J. & Turrini, P. (2023). "Safe Opponent Exploitation for ε-Equilibrium Strategies," *arXiv:2307.12338*." → "Jeary, L. & Turrini, P. (2023). "Safe Opponent Exploitation For Epsilon Equilibrium Strategies." *arXiv:2307.12338*." The first author is **Linus** Jeary, and the arXiv title spells "Epsilon". Verified on arXiv. No peer-reviewed venue found (web search).
  - `liu2022`: "Liu, W. et al." → "Liu, M., Wu, C., Liu, Q., Jing, Y., Yang, J., Tang, P. & Zhang, C." (**Mingyang** Liu). Verified on the NeurIPS proceedings page. BG full text: F08-B03.
  - `milec2025`: "Milec, D., Kovařík, V. & Lisý, V. (2025). "Adapting Beyond the Depth Limit," *arXiv:2501.10464*" → "Milec, D., Kovařík, V. & Lisý, V. (2025). "Adapting Beyond the Depth Limit: Counter Strategies in Large Imperfect Information Games." *AAMAS 2025* (extended abstract), 2675–2677; arXiv:2501.10464". The venue is per `lit_gaps.md` (Crossref + IFAAMAS listing), not rechecked by me. The full title matches the arXiv PDF listing found by search.
  - `safe2024`: "Ge, Z. et al. (2024). "Safe and Robust Subgame Exploitation…," *ICML*." → "Ge, Z., Xu, Z., Ding, T., Meng, L., An, B., Li, W. & Gao, Y. (2024). "Safe and Robust Subgame Exploitation in Imperfect Information Games." *ICML*, PMLR 235, 15255–15270." Verified on the PMLR page.
  - `johanson2007`: venue "*NeurIPS*" → "*NIPS 2007*, 721–728". Pages from the ACM DL listing (via search); the full text was read.
  - `johanson2009`: add "PMLR 5, 264–271". Verified on the PMLR listing (via search).
  - `gordon2003`: the label names the second author; the authors and title are correct (McMahan, Gordon & Blum, ICML 2003, verified via search listings). BG prose: F08-B03.

### F08-S05 · S2 · `search2024` describes OX-Search wrongly
- **Where:** footnote `search2024` — "OX-Search bounds exploitation loss *per information set*, hardening the same idea against "teaching" attacks."
- **Problem:** Ge et al.'s guarantee is whole-strategy adaptation safety: exp$(\sigma'_2) \le$ exp$(\sigma_2)$ for the refined strategy (Theorem 4.3). Per-information-set is how it is *applied* ("employ OX-Search repeatedly at each newly encountered information set in a nested fashion"), not what is bounded. The "being taught and exploited" motivation is correct. Verified in the PMLR v235 PDF.
- **Proposal (correct):** BG in F08-B03. EN: "— OX-Search: subgame re-solving with a gadget that keeps the refined strategy no more exploitable than the blueprint (adaptation safety, Theorem 4.3), applicable in nested fashion at each newly reached information set; motivated by the "being taught and exploited" problem; tested on Leduc and Flop Hold'em, two-player."

### F08-S06 · S3 · "The oldest principled method" (RNR, 2007)
- **Where:** summaryBg.md § 8.5 — "Най-старият принципен метод, **ограничен отговор по Наш** (Johanson 2007)"; EN l. 226.
- **Problem:** McCracken & Bowling's ε-safe strategies (2004) are older, and Johanson et al. (2007) say RNR "is closely related to ϵ-safe best responses [MB04]" (verified in the NIPS 2007 full text). "принципен" is the moral sense (F07-B23).
- **Proposal (soften):** "Най-старият принципен метод, **ограничен отговор по Наш** (Johanson 2007)" → "Един от най-ранните строго обосновани методи, **ограниченият отговор по Наш** (Johanson 2007; близък до ε-безопасните стратегии на McCracken и Bowling от 2004 г.)"; EN "The oldest principled method" → "One of the earliest principled methods".

## X — Structure

### F08-X01 · S2 · Tables 24 and 25: first two columns collide and every metric row wraps into three lines
- **Where:** bundle pp. 159–160 (Table 24, Kuhn) and p. 163 (Table 25, Leduc). The printed headers read "Противникметрика", and the row labels "AlwaysBetEV", "AlwaysPassEV" and "LoosePassiveEV". "най-лошият случай" breaks over three lines, so Table 24 splits across two pages.
- **Now → Proposed:**
  - "| Противник | метрика | nash | full_br | rnr_0.5 | **ganzfried** | prime_safe | adaptation |" keeps its header; its separator "|---|---|---:|---:|---:|---:|---:|---:|" → "|------------|-------|----:|----:|----:|----:|----:|----:|"
  - The Leduc separator "|---|---|---:|---:|---:|---:|---:|" (under "| Опонент | метрика |…") → "|------------|-------|----:|----:|-----:|-----:|-----:|"
  - In both tables the metric cell "най-лошият случай" → "най-лош случай"
- **Why:** Pipe-table widths follow dash counts. Equal widths give the first column ≈ 1/8 of the line, too narrow for "AlwaysPass (най-експлоатируем)". The labels from F08-B04 are longer still.

### F08-X02 · S2 · The pseudocode block runs off the right margin (p. 155)
- **Where:** summaryBg.md / summaryEn.md code block in § 8.4. The printed lines end "…: the oracl" and "…# a valid lower bound on the worst", with "case" missing.
- **Now → Proposed:**
  - "    wc  <- worst_case_value(pol)          # = -(opponent's exact best response) : the oracle" → "    wc  <- worst_case_value(pol)    # = -(opp. exact BR value): the oracle"
  - "    add the cut  c(adv) . x >= floor - slack   to cuts     # a valid lower bound on the worst case" → "    add cut c(adv) . x >= floor - slack   # valid lower bound on worst case"
- **Why:** At the bundle's code size, ≈ 88 characters fit on a line; these two lines are 95 and 100 characters. Apply the same edit in both languages.

### F08-X03 · S3 · Cross-references "§5/§6/§7/§8" and "Figure below, left"
- **Where:** summaryBg.md: "(§7)", "(§5)", "Тази последна точка се повтаря в §6", "§8 показва", "Това е §5 праг" (F08-B27), "(Глава 7, §7)" (F08-B09), "(фигура по-долу, вляво)" (F08-G04)
- **Fix:** → "§ 8.7", "§ 8.5", "§ 8.6", "§ 8.8", "§ 7.7". There is no "left" panel: "(фигура по-долу, вляво)" → "(сивата линия на следващата фигура)" if fig. 40 is dropped, otherwise "(фигурата по-долу)". EN likewise.
- **Why:** In a 226-page bundle a bare "§5" is ambiguous (F07-X03).

### F08-X04 · S3 · The Kuhn table drops two things the figure and the JSON contain
- **Where:** § 8.6 Table 24 vs fig. 42 and `kuhn_scale.json`
- **Problem:** Fig. 42 shows a `ses_subgame` bar that the table omits, and nothing says why. On Kuhn the subgame is the whole game, so SES coincides with adaptation (report § 5). The JSON also has a sixth opponent, `Thresholdish`, that the claim "on every exploitable type" silently includes.
- **Fix:** After the table add: "(`ses_subgame` не е показан: в Кун под-играта е цялата игра и методът съвпада с адаптацията. Шестият тип в данните, `Thresholdish`, дава същата картина: Ганцфрид +0.019 срещу +0.015 за Наш.)" Also add it to the EN.
