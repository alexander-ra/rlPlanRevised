# Step 12 — fixes applied
Applied: 65 · Skipped: 2 · Central: 6

Applied = G01–G08, B01–B29, the T01/T02/T04–T11 *occurrences* in the step-12 files, C01–C10,
S01–S06 (S05 only in part), X01–X02. R8 (TRIAGE § B) is covered by C01–C10. Every review quote
matched exactly once: a script checked the match count before replacing, so nothing needed
applying by hand. EN mirrors every C/S/X change. The one-pager EN was rewritten so it says the
same as the BG (B25/B28 bullets).

**R8, as decided (text fix, no reruns):**
- C01: the one-pager headline is now "BC 0.055 < ARDT 0.469 < DT 0.799". The real models score
  0.25–0.33, and the 0.833 row is marked as the scripted stub. Same in the report EN/BG (caption
  and lead sentence).
- C02: the Kuhn "collapse" is now a *spike* in exploitability, to ≈ 1.9 chips (the summary) and
  1.98 (the report, "its play collapses"). Fixed in summary EN/BG and report EN/BG.
- C08: the ARDT `Q̃(s,a)` fix is marked as a hypothesis that was never run (summary § 12.3,
  takeaways 1–2, one-pager, report § MATH FLAG B / R2 / research directions). ARDT's minimax
  target is exact only for deterministic transitions. This is cited to Tang, Cheng & Kumar 2025
  (arXiv:2510.11877, CART). I checked the authors, the workshop and the method name CART on the
  arXiv abstract page.
- C04: "no in-context adaptation" is now scoped to one model (Qwen2.5-7B-Instruct), a 20-hand
  window and one conclusive opponent (0.824 → 0.827). The text now says the models do respond
  when told the opponent type (adaptation delta up to 0.92).
- C06: gpt-oss-20b is described as a mixture-of-experts model with 21B total / 3.6B active
  parameters. "Scale is irrelevant" is gone.
- C10: models, serving and "own measurements" are now stated. The wording is "LM Studio 0.4.20
  on an RTX 5090, temperature 0.7; the quantisation of the weights was not recorded". This is in
  summary § 12.5 EN/BG, the one-pager "Подход"/Approach, and the report header EN/BG. The
  temperature (0.7) was checked in every real-model results JSON.
- C09: removed all four stale chapter-13/14 references in each summary (Step 13, Глава 13 ×2,
  Глава 14; EN: Chapter 13 ×3, Chapter 14). Also removed report EN/BG "Chapter 13's fixed logs",
  "Chapter 14 evaluation framework", "raw step" ×2 / "суровата стъпка", "Суровият код", "the
  step" ×2, and the one-pager's "The step's" / "стъпката".

Deviations from the review wording:
- **GLOSSARY 2.3 (self-play) is undecided, so "самообучение" stays.** B02 is applied, but with
  "…при които самообучението не е възможно" instead of "самоигра". B30 and T03 are skipped.
- **GLOSSARY 1.7:** the overlay's 'Nash' is 'равновесие на Наш'. 'Nash (CFR)' is 'равновесие на
  Наш (CFR)', not the review's 'равновесие (CFR)'.
- **GLOSSARY 2.7:** C04's "фиксирано предварително убеждение" became "фиксирано априорно
  убеждение".
- **B02 / C10 / S04:** C10's sentence also names the RTX 5090 and says the quantisation was not
  recorded (R8 instruction).
- **G01 captions:** where a figure lost numbers, its caption now carries them: fig. 73 has
  Pearson r; fig. 75 has the MAE values (the panel titles dropped them); fig. 77 has the totals
  0.234 / 220. The fig. 73 caption was shortened by one line so the figure fits on its page
  (X02). The EN captions were rewritten to match (they now name the model, per F12-C10).
- **G02:** no `parse_known_args` edit. The renderer now isolates argv, so `plotting.py` ran
  under it unchanged. Bar values use `locale.format_string`, so the BG prints 0,392 and the EN
  0.392.
- **S05 (S3, optional):** only "(измерено в собствена симулация)" / "(measured in own
  simulation)" was added to the formula. The ESPER sentence was not added.
- **S03:** the TextArena footnote was deleted, not re-attached.
- **BG one-pager:** fitting it on one page took wording cuts only (no content removed). I also
  removed its two forced line breaks in "Проблем." (the EN has none).
- **Extra, same intent** (glossary rows or the same error as a finding):
  - summaryBg: "Ако обусловим върху" → "по"; "обуславя не върху … а върху" → "по … по" (2.21);
    "два кръга на залагане" → "рунда" (3.4); "Лимит Холдем" → "лимитен холдем";
    one-pager "минимакс преетикетиране" → "минимаксно".
- **report_bg.md** (glossary and R8 pass; the review read it for consistency only):
  - Title and wording:
    - title "Последователни модели … ситуации" → "Модели на последователности … среди";
    - "Нашово/Нашево равновесие", "Наш равновесие", "Референтният Nash" → "равновесие(то) на
      Наш" / "равновесието";
    - "условно връщане", "кондициониране" → "обуславяне по възвръщаемостта";
    - "очаквана възвръщаемост до края" → "остатъчна";
    - "извън линия", "извънлинейният" → "офлайн";
    - "разликата е намалена" → "затворена част от разликата";
    - "обхождане" → "серия (експерименти)";
    - "преозначава", "целта за преозначаване" → "преетикетира", "целевата стойност при
      преетикетирането".
  - Poker terms:
    - "улица" / "кръг" → "рунд на залагане"; "проверката" → "чекът"; "пасна" / "пасувате"
      (fold / check) → "откажа" / "чек"; "залагащ" (call) → "плащащ";
    - "несдвоени раздавания срещу висока маса" → "ръце без чифт и висока обща карта";
      "текстурата на масата" → "състава на общите карти";
    - "изтичане" → "загуба"; "незаконен/незаконни" → "недопустим(и)".
  - Other terms:
    - "профил на дим" → "профил SMOKE (бърза проверка)"; "предварително убеждение" →
      "априорно";
    - "жетони/ръка" → "жетона на раздаване"; "60-ръчна" → "сесия от 60 раздавания";
    - "(Трансформър за вземане на решения)" → "Decision Transformer"; "АБДМ" → ARDT; "ДТ" →
      DT; "ГЕМ" → "големият езиков модел"; "Бекенд" → "Модел";
    - "опорни системи" → "варианти на агент"; "reasoning-SFT" → "дообучаване за разсъждения
      (SFT)"; "token logprobs" → "логаритмичните вероятности на токените".
  - Case errors: "coT" ×5 → "CoT", "openThinker3" ×3, "nash-CFR" ×2.
  - Bot names in the tables → „Винаги пас“ / „Винаги залог“ / „Стегнат-пасивен“ (as in fig. 76).
  - The heading "Съгласуване между прогноза и реалност" → "Съпоставка: прогноза и реалност"
    (1.27). The two cross-references now use the real headings.
  - Figures: all 8 report_bg captions were translated to Bulgarian, and all 8 images now point
    at the `_bg` twins.
  - "самообучение" is left as it is (row 2.3).

## Skipped (id — reason)
- F12-B30 — self-play → "самоигра"; GLOSSARY row 2.3 is still open (❓), and the brief says to
  leave it.
- F12-T03 — same row 2.3; its occurrences in summaryBg, onePagerBg and report_bg are unchanged.
- (partial) F12-S05 — the optional S3 ESPER sentence was not added.

## Central (id — what is needed)
- F12-T01…T11 — the glossary entries themselves (glossary_settled / terminology_EN_BG). Only
  their occurrences in the step-12 files were fixed.
- Shared figure_labels.json:
  - 'Nash' → 'Наш равновесие' is rejected by row 1.7. The overlay gives 'равновесие на Наш'.
    Step 12 is the only occurrence listed.
  - The overlay also redefines two runtime-observed shared keys: 'TightPassive' ('стегнат-пасивен'
    → 'Стегнат-пасивен') and 'LooseAggressive' ('свободно-агресивен' → 'Разпуснат-агресивен',
    per F12-G07). Check the other steps that plot these bots before merging.
- F12-S01 / GLOSSARY 5.3 — footnote label `kuhn1950` is shared with step 02. Step 02's copy drops
  "A" from the title ("Simplified Two-Person Poker"); that needs fixing there. `chen2021`,
  `paster2022` and `tang2024` may also collide in the bundle. New labels: `lin2026`, `guo2023`,
  `tang2025`.
- GLOSSARY 5.1–5.2 — " - " dashes, decimal points and "5,000/50,000/20,000" in summaryBg,
  onePagerBg and report_bg. The stray "1,576" in the BG one-pager is also central. New text
  follows the surrounding style.
- The pipeline-added bold spans in report_bg (e.g. "**раздавания**", "**агента**") are left for
  the central pass.
- F12-C10's "record the GGUF quantisation in the report" — it was not recorded anywhere
  (EXECUTION_NOTES, results JSON). The text now says so. Recording it needs the candidate's LM
  Studio model list.

## Numbers changed (old → new, where)
All come from the committed JSON in `implementation/step12/implementation/results/`. No
reruns.

| Quantity | Old | New | Where |
|---|---|---|---|
| One-pager headline | BC 0.055 << ARDT 0.469 < DT 0.799 < LLM 0.833 | BC < ARDT < DT; real LLMs 0.25–0.33; stub 0.833 | one-pager EN/BG, report EN/BG |
| Kuhn DT at R = −1 | "sharp collapse" / "рязък спад" | spike to ≈ 1.9 chips (1.85 in dt_experiments; 1.98 fine sweep) | summary EN/BG, report EN/BG + fig. caption |
| LLM vs Nash exploitability | "59× more exploitable" | 0.357 vs 0.006 chips | summary, one-pager, report EN/BG |
| Share of the gain from passive/random bots | "entire gain" | nearly 90 % (0.354 of 0.402; Random 0.267 vs 0.119 added) | same |
| In-context adaptation | mean gap closed +0.38, mean learning −0.22 | AlwaysPass 83 % (0.824 → 0.827); others ±0.53–0.80; told-type adaptation up to 0.92 | one-pager, summary, report |
| gpt-oss-20b size | "20B" | 21B total / 3.6B active | summary, one-pager, report |
| Leduc vs weak bots | "cannot beat at all" | −0.071 vs +0.582, wins only vs the 2 passive types | summary, one-pager, report |
| Leduc dips | not mentioned | 0: −0.80 ± 0.07 (17.4 % of steps); −5: −0.88 ± 0.06; modal −0.45 ± 0.02 | summary EN/BG, report EN/BG |
| BC in the summary | absent | 0.055 vs Nash 0.016 vs DT 0.799 (0.67–0.80 across retrains) | summary § 12.4 EN/BG (X01) |
| Fig. 72 legend | "vanilla DT (0.731)", "Nash (0.017)" | values moved to the caption | fig. + caption |

## Figures (file — what changed — printed size now)
Script: `implementation/step12/implementation/plotting.py` (plotting code only: DPI = 300,
display-name maps, `_num()` = locale-aware bar values). EN and `_bg` PNGs were copied to
`summary/` (6) and `figures/` (12). summaryBg and report_bg link the `_bg` twins.
All six print at 17.6 cm (render_printed manifest).
- impl_tau_sweep — f-string legend labels dropped; legend fs 8 → 10, moved below the axes (it
  covered the τ = 0.01 point); 7 × 4.6 in @300. **9.9 pt**, 303 ppi (was legend 7.9 pt, 131
  ppi).
- impl_leduc_return_conditioning — f-string title and legend removed; legend fs 10, below the
  axes; 8 × 3.85 in @300 (shortened so it fits under the text on p. 4). **8.7 pt**, 347 ppi (was
  6.9–8.7 pt, 150 ppi).
- impl_leak_decomposition — (11, 5) → (8, 4.4); suptitle removed; title "Where the loss is".
  **8.7 pt**, 347 ppi (was 6.3–7.6 pt).
- impl_stated_vs_executed — (11, 8) → (8, 6.2); ticks, legends and bar values fs 8 → 10; one
  shared legend above the panels (the per-panel legends covered lines); display names, no
  truncation; y headroom so "1,576" clears the title. **10.0 pt**, 300 ppi (was 6.0–7.4 pt).
- impl_exploitation_frontier — scatter panel dropped; (12, 4.6) → (8, 4.2); title "Winnings per
  opponent"; series "Nash (CFR)" / "Qwen2.5-7B-Instruct"; ticks fs 10. **8.7 pt**, 347 ppi (was
  4.6–6.9 pt).
- impl_leduc_illegal_taxonomy — (11.5, 4.4) → (8, 4.2); categories and situations go through
  set_*ticklabels with display names; titles 10.5; n= fs 10; x-room for n= labels. **8.7 pt**,
  347 ppi (was 4.8–6.0 pt).
- Report-only (dpi 130 → 300; BG labels via the overlay, layout unchanged): return_conditioning
  (the BG title is wrapped to 2 lines, since it was clipped), bet_prob_by_card, and
  exploitability_bars × 4.

## Remaining overflow / legibility warnings
- Renderer (`render_bg_figures.py --only step12 --labels-overlay …`): 1 script ok, 0 failed, 12
  BG figures, **no overflow warnings**. There are no box diagrams in step 12.
- Everything prints at ≥ 8.7 pt. The fig. 77 BG category ticks ("повишаване / над лимита" next
  to "отказ при / безплатен / чек") sit close together but do not touch (checked on the crop).
- X02: the BG summary now has one ~30 %-empty page (p. 6, before fig. 75). It had three gaps
  (30–50 %) and 11 pages; it now has 10. EN: no gap.
- Results JSON: all 19 files are byte-identical before and after every plotting and render run
  (sha256 checked). Only PNGs were written.

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step12 --type all` (PYTHONIOENCODING=utf-8): all 6 PDFs built.
  - The BG one-pager fits on 1 page at the tightest rung (8pt / 1.1cm), after trimming the
    wording.
  - The EN one-pager fits at 9pt / 1.3cm.
  - The BG summary is 10 pages, the EN summary 9.
- `check_headings.py`: 44 PDFs checked, 0 missing headings (step 12 clean).
- `check_captions.py`: 24 PDFs checked, 0 with unaccounted figures (step 12 clean).
- In the built step12_bg.pdf:
  - `\text{(измерено в собствена симулация)}` typesets;
  - the new footnotes print (Kuhn, Lin, Guo, Tang–Cheng–Kumar; Tang–Marques…);
  - none of "Step 13", "Глава 13/14", "условно връщане", "очаквана възвръщаемост до края",
    "Наш равновесие", "TextArena" remains.
  - The same stale and glossary strings are absent from step12_report_bg.pdf.
- Crops: `deliverables/finalReview/renders_fix/step12/ch12/p003…p009_f1.png`. I read all six:
  captions are in Bulgarian with decimal commas in the figures; labels are ≈ 80–90 % of the
  caption letter height; nothing overlaps or is clipped.
