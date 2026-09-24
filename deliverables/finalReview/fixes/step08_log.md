# Step 08 — fixes applied
Applied: 70 · Skipped: 2 · Central: 5

Applied = G01–G09, B01–B35 except B21, T01–T03 and T07–T10 (the occurrences in this chapter), C01–C10,
S01–S06, X01–X04. The edits cover summaryEn/Bg, onePager/Bg and report_en/bg. The BG summary and the BG
one-pager were rewritten as a whole, because nearly every paragraph carried a finding.

R-items (TRIAGE § B), text only. No solver code was touched.
- **R1 / C01.** The method is now named **best equilibrium** (BG „най-доброто равновесие“, "the
  Ganzfried–Sandholm baseline"). The code id `ganzfried` is kept wherever the text refers to code or results.
  - Tables use "best eq." / „най-добро равн.“ with a caption note.
  - Figure labels: fig. 38 floor note, fig. 39 row, fig. 41 legend, fig. 42 tick, fig. 43 title, fig. 44
    legend.
  - Captions and the § 8.6 heading are relabelled too.
  - § 8.3 (a) has C01's rewrite, plus two sentences on what RWYWE/BEFFE would add and that implementing them
    is future work. The same point is in § 8.9, the one-pager's open questions, report § 1 (a note) and
    report § 13 (a new first research direction).
  - Verified against the Ganzfried & Sandholm author PDF (cs.cmu.edu, EC'12 version). RWYWE plays
    argmax over SAFE(k_t), with k_{t+1} = k_t + u − v*. BEFFE = "Best Equilibrium Followed by Full
    Exploitation". Propositions 5.4 and 5.5 prove both safe. The "best equilibrium" strategy is § 5.3 in that
    version (§ 6.3 in TEAC, per the review). The text cites no section number.
- **R2 / C02.** The caveat is in § 8.7, § 8.8 (headline sentence and the SES paragraph), § 8.9, the fig. 43
  caption and labels (caps 40 / 400), the one-pager headline, report § 10 (heading and body) and report § 13.
  No rerun.
- **lit_gaps corrections.**
  - Jeary, L.; Liu, M. (full author list); Milec: AAMAS 2025 extended abstract, pp. 2675–2677.
  - Equal share is written as a fair-share *target* C/n that cannot be secured against opponents with
    different fixed strategies (C09 text, report § 13).
  - piKL does not occur in any step-08 file (summary, one-pager and report, EN and BG, were grepped).
    Nothing to change.
- **⟦MATHI5⟧.** Both placeholders are gone: B01 gives the p ≈ 0.7 formula, and C08 replaces the second
  one. The BG summary has no "MATH" string left.

### Deviations from the review's proposals (on purpose)
- **Glossary 1.18 (oracle → оракул).** Used instead of the review's "предсказвач": "оракул за най-лошия
  случай", "метод на двойния оракул", in the text, captions and figure labels.
- **Glossary 2.35.** smoke → „бърза проверка (*smoke*)“ and scale → „пълен мащаб (*scale*)“, not B04's
  „пробно изпълнение“.
- **Row 1.10 (blueprint) left open.** Every review proposal that says „базова стратегия“ for *blueprint*
  was written with the chapter's existing „план“. That covers B07, B33, C03, C04, C08, S05 and the figure
  label 'blueprint\n(pinned)' → 'план\n(фиксиран)'. At first use, (в) now reads „план (blueprint)“ to
  separate it from „план за реализация“. Where the review's „базова стратегия“ meant *baseline*, as in C09,
  I used „базова линия“.
- **B17.** Applied as the review's paraphrase („стойността, която … равновесие на Наш постига срещу самото
  себе си“). It avoids the self-play term, so row 2.3 is untouched.
- **C04's −0.1197.** This value is not in `leduc_bounded_scale.json`. It comes from `EXECUTION_NOTES.md`
  (Leduc bounded run) and is written as −0.120 "in the run notes". It was not re-derived by a rerun (that
  would mean running CFR, which agents may not do). It is consistent with the JSON: the four converged SES
  cells have wc −0.1293…−0.1297 with converged = True at tol 0.01, so the floor is ≤ −0.119.
- **X01.** The review's dash widths still let the "prime_safe" and "adaptation" headers collide in print.
  They were widened to |11|9|4|5|5|6|6|6| (Kuhn) and |11|9|5|5|7|6|7| (Leduc), in EN and BG. The BG Leduc
  cells were shortened: "✓ (194 ит.)" and "✗ лимит", with a caption note explaining them.
- **Adaptation-safety formula (B02).** The BG version with Cyrillic ran past the right margin. It is now a
  two-line `aligned` display.
- **G04.** Took the preferred option: fig. 40 is dropped from both summaries, and the pointer now reads
  "the grey line in the next figure". The report still uses the figure (report § 2), so `pareto_curve.py`
  got a plot-only mode (`PLOT_ONLY=1` or `--plot-only`, reads the saved JSON; the JSON md5 is unchanged).
  The labels are now 1−λ = weight on the best response, the title was dropped, fs 10 and 300 dpi. A BG twin
  now exists.
- **Other edits outside the review's list.**
  - Dial EN: "Nash / GTO" → "Nash equilibrium" (G02 item 4).
  - Dial box: "safety governor" is now "*ограничител*" in the BG text, to match the figure.
  - Kuhn table: an X04 note on `ses_subgame` and `Thresholdish`, in EN and BG.
  - § 8.6 item 2 gained the sentence "The gain is small because a per-hand floor at v* admits only
    equilibrium strategies (§ 8.3)", which ties R1 to C07.
- **report_bg.** Beyond the R/C items it got the glossary pass. Fixed forms: „Льодюк“ ×11, „Нэш“,
  „нашов/Нашево“, „героя“, „сходи/сходява/сближава“, „джаджа“, „изтичане/течове“, „политиката“,
  „контраексплойтър“, „семена“, „изненадващ обрат“, „Canonical“, „предсказвач“, „равнини на
  отсичане/сечение“, „безопасен спрямо прайм“, „шаблон“, „вятърна печалба“, „ръка/ръце“ (a deal),
  „крал-флоп/поп на флопа“, „✗ capped“, `*.JSON`. All seven BG report captions were translated, and five
  point at `_bg` twins; `rnr_playground_kuhn.png` has none (see Central).

## Skipped (id — reason)
- B21 / T04 — blueprint → „базова стратегия“: GLOSSARY row 1.10 is still open, and the brief says to leave
  it. „план“ is kept, with "(blueprint)" at first use.
- C01 optional part (implement RWYWE) and C03 optional part (rename `ses_subgame`): code changes, which
  the triage reserves for the candidate. The text says RWYWE is future work.

## Central (id — what is needed)
1. Merge `deliverables/finalReview/fixes/labels_step08.json` (58 keys) into
   `scripts/figures/out/figure_labels.json`. It adds the new source strings (best equilibrium, Chapter 7/8
   notes, oracle, ≥/→/ε forms) and replaces the regressed step-08 values. The last four value fixes
   (made after the first render) are: 'Full best response…', 'SES subgame (Liu)…', 'Payoff vector c…' and
   'exploitability (game value − worst case; ≥ 0)'. It also carries the generic number keys "0.0"…"1.0" →
   "0,0"…"1,0".
2. Glossary files (`glossary_settled.md`, curated `terminology_EN_BG.md`) need T01–T03 and T07–T10:
   bang-bang, two-/N-player, worst-case value, safe exploitation, cutting-plane / cut, gadget, exploiter.
   Only this chapter's occurrences were fixed.
3. T05 (curated SES expansion → "Safe Exploitation Search") and T06 (curated "Ограничен Наш отговор" → „ограничен
   отговор по Наш (RNR)“). Both are curated-file rows; the chapter text already uses the right forms.
4. `implementation/step08/exploration/rnr_playground.py` (report fig., report § 3) has no BG twin. Its
   `main()` recomputes and rewrites `rnr_playground_kuhn.json`, so it was not run. It needs a plot-only mode,
   as `pareto_curve.py` now has. The BG report shows the English PNG with a Bulgarian caption.
5. Build: at the end of § 8.7, three consecutive footnote markers print run together as "101112" (EN and
   BG, pre-existing). This needs a separator in the footnote filter. The shared-label and typography items
   (§ 5.1–5.3) are central as briefed.

## Numbers changed (old → new, where)
- No result value changed. All numbers were re-read from `kuhn_scale.json`, `pareto_kuhn.json` and
  `leduc_bounded_scale.json`.
- New numbers, all computed from those files:
  - best equilibrium's gain over Nash, 0.002–0.076 per hand = 1–9 % of full_br's gain (C07; summary,
    one-pager, report § 6 and § 13);
  - `Thresholdish` +0.019 vs +0.015 (X04);
  - switch at p ≈ 0.68, and the chord 0.002 better than the naive blend (C05);
  - global cells 2.3–3.0 s ("about 2.5 s") vs SES 29.6–78.5 s ("30–79 s") and 194–400 iterations (R2);
  - SES floor −0.120 (from EXECUTION_NOTES, see above).
- Fig. 44 x axis: downsampled index 0–400 → hand 0–20 000; the switch line is now at hand 10 000 (was drawn
  at index 200). The caption and the tables now say the curve is seed 0.
- Report fig. (pareto_curve): the point labels were λ = weight on Nash; they are now weight on BR (1 − λ),
  matching report § 2's table.
- C04: "residual 0.04 — top item to resolve" → measured against v*; SES sits at the 0.01 tolerance of its own
  floor (summary § 8.8, report § 10, § 12 item 2, § 13, one-pager).

## Figures (file — what changed — printed size now)
All six BG summary figures print at 17.6 cm (renders_fix/step08/ch08, manifest: 303–389 ppi). Every text
element is at fs ≥ 10, except the inset ticks of fig. 41 (fs 9, 8.9 pt).
- dial_safe_exploitation(_bg) — `make_dial_figure.py`:
  - fs 8.4–8.6 → 10 everywhere;
  - side boxes are 3.7/3.8 × 1.3 and the middle box 4.45 × 1.35;
  - the governor label was moved above the "EXPLOITATION" label, where it collided in BG;
  - the floor note has 3 lines, with the Chapter 7 / Chapter 8 notes stacked;
  - ylim (−0.3, 5.2). Prints at 8.5 pt, 389 ppi.
- one_lp_engine(_bg) — `make_lp_engine_figure.py`:
  - fs 7.4–8.4 → 10; the columns were widened within 14 units (3.8 / 4.05 / 5.4);
  - the check box is 4 lines and the rows are 0.9 high;
  - the loop note sits above the BR box; the bottom note has 2 lines at y 1.6, and ylim is (1.1, 8.4);
  - "Step 7" → "Chapter 7"; the R1 row label. Prints at 8.6 pt, 385 ppi.
- global_vs_local(_bg) — `make_global_local_figure.py`:
  - fs → 10; titles and notes on 2–3 lines, with the 40/400 caps in the notes;
  - taller triangles (apex 5.7) and a wider inner triangle (8.7–12.5, apex 3.6), so the BG labels sit
    inside;
  - R1 title. Prints at 8.9 pt, 369 ppi.
- impl_pareto_kuhn(_bg) — `plotting.py` `plot_pareto`:
  - RNR drawn as markers only, annotated p ≤ 0.6 / p ≥ 0.7;
  - "prime-safe = adaptation" is a single star;
  - an inset of the safe corner; the title was dropped;
  - figsize (7, 4.8), 300 dpi, fs 10 (inset 9). Prints at 9.9 pt, 303 ppi.
- impl_methods_kuhn(_bg) — `plot_tournament`: figsize (7, 4.2), 300 dpi, fs 10, title dropped, "best eq."
  tick, "Nash floor −0.056" with a true minus. Prints at 9.9 pt, 303 ppi.
- impl_teaching_kuhn(_bg): the x axis is hands, the switch is at switch_at, fs 10, 300 dpi, the title was
  dropped and the legend reads "best equilibrium". Prints at 9.9 pt, 303 ppi.
- `plotting.py` now has a plot-only `__main__` (reads `results/*.json`, writes `impl_*.png` to
  `deliverables/reports/step08/figures/`), so `render_bg_figures.py` produces the BG twins.
  `summaryBg.md` points at the `_bg` files.
- pareto_curve_kuhn(_bg) (report only) — see G04 above. Copied to `deliverables/reports/step08/figures/`.
- Result JSONs: git shows no change to any `results/*.json` or `exploration/figures/*.json`.

## Remaining overflow / legibility warnings
- `render_bg_figures.py` (the new save-time fitter) printed **no overflow warnings** in the final run.
  Earlier warnings were fixed by enlarging boxes and shortening five BG labels.
- The BG one-pager fits on one page at the 8.5pt/1.2cm rung, after trimming about 10 % of its wording (at
  first it overflowed even at 8 pt). The EN one-pager fits at 10pt/1.5cm.
- The BG Kuhn table still wraps the first column to 2–3 lines and "най-лош случай" to 2 lines. It is
  readable and no longer splits across pages.
- Teaching-attack legend and bar-chart ticks keep the code ids (full_br, adaptation, nash, prime_safe,
  ses_subgame) Latin, consistently with the tables.

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step08 --type all`: all 6 PDFs built. Summary is 17 pp (EN) / 21 pp (BG);
  report is 18 / 23; one-pagers are 1 / 1.
- `check_headings.py`: 44 PDFs, 0 missing for step 08. The only 3 missing are in step12_bg.pdf, another
  chapter.
- `check_captions.py`: 24 PDFs checked, 0 with unaccounted figures.
- Cyrillic inside `\text{}` (праг, модел, Наш, за всеки противник, експлоатируемост(…), най-лош случай(…))
  renders correctly (B02 check, pp. 3–7 of step08_bg.pdf).
- Printed crops: `deliverables/finalReview/renders_fix/step08/ch08/`. All six were checked: legible, no
  overlaps, no English left except Latin method and code names.
