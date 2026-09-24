# Step 11 — fixes applied
Applied: 65 · Skipped: 1 · Central: 8

Counted per finding of `step11_review.md` (66 = G 10 · B 20 · T 16 · C 11 · S 7 · X 2).
Applied = G01–G10, B01–B20 (B14 and B19 in part, see below), the in-file occurrences of
T01–T15, C01–C11 (C02 as the R4 caveat; C06 without item 5), S01–S07, X01–X02. Summary EN/BG
edits were exact-match scripts (77 BG + 44 EN replacements, every quote matched once);
the EN report had 34 exact replacements; the one-pagers and `report_bg.md` were rewritten
whole because almost every sentence changed (the BG report carried "{0.1}", "засаден",
"развръзка", "задънена улица", "героя", "оскъдна", "критична стойност", "представка-артефакт",
"предварителна поправка" for *pre-fix*, "съгласуване", "Шейпли/кредит", "двуигрална", "sLS").

**R4 (F11-C01/C02, caveat).** Formula corrected everywhere to $r=\alpha\,r_{sparse}+(1-\alpha)\,\text{credit}$
(summary EN/BG, report EN/BG, fig. 68, with "α = 1 win reward only / α = 0 credit only").
Mechanism caveat added as its own paragraph in § 11.4 (EN/BG), in the report's Exp. 4
conclusion and as limitation #1, in the one-pagers, and in "What held up" / the takeaways:
rollout credit = additive game → own win probability (computed once per batch from the initial
state); proxy = own critic value minus table mean; the coalition score (mean |C_ij|) also counts
hostility → "the coalition score rises when the win reward is replaced by a dense signal, which is
not yet evidence of learned coalitions". § 11.4 heading → "…and when the coalition score actually
rises". Report "Research directions" gains the real fix (help/harm-matrix credit + coalition-free
dense-reward control) as C2 research. Credit code untouched, nothing rerun.

Glossary rows applied beyond the review: 1.1, 1.7, 1.13, 1.18 (предсказвач → оракул, also in the
one-pager, where the review kept "предсказвач"), 1.26, 1.27, 1.28, 2.12, 2.16, 2.19, 2.20 (per the
coordinator's correction: *critic* → **оценител**, not "критик"), 2.28, 2.35, 2.36, 2.38, 2.45–2.48,
3.7, 3.12. Not applied: 2.3 self-play ("самообучение" kept: § 11.4, report, fig. 68 label).

Where the intent was applied differently from the review's literal text:
- Tiers: glossary 2.35 → "бърза проверка" / "пълен мащаб" (review: "пробна" / "разширена").
- Hero: glossary 3.7 → "собственият агент" (review: "обученият агент").
- "по мрежата α × …" → "за всички комбинации α × …" (2.28: grid is "решетка", "мрежа" clashes).
- S02: reused the corpus keys `[^pluribus]` (body identical to steps 04/06) and `[^daskalakis2009]`
  (step 02) instead of a combined new note; `[^bernheim1987]` new.
- S03: `[^decarufel2024]` placed once (Read-more); not repeated in "Доверие" (pandoc duplicates a
  twice-referenced note).
- C05: the constant-sum empty-core claim cites `[^ferguson]` (Ferguson's lecture notes, verified in
  the review's extract) — replace with Owen's textbook once edition/theorem are checked.
- C06.3 and the "coalition-forming costs winning" takeaway reworded for R4 ("Weighting the credit
  costs winning"); the "engine fidelity" takeaway now names the credit definition as a third weakness.
- New figure labels (BG) use the decimal comma — figures are not reached by the central text pass.

## Skipped (id — reason)
- T16 — self-play: glossary row 2.3 is still open.
- (partial) B14 — "самообучение" left for row 2.3; the rest of B14 applied.
- (partial) C06 item 5 (S3) — "0.25–0.31" kept: 0.31 is pre-fix, but the post-fix dev log
  (EXECUTION_NOTES, Phase 4) gives ~0.32 for the skill-ladder pool, so the range stands; not trivial.
- (partial) C02 optional rename "coalition-aware MAPPO" → not done (headings keep the name; caveat added).

## Central (id — what is needed)
- T01–T15 — the settled/curated glossary entries themselves; GLOSSARY_DECISIONS 2.20 still says "критик"
  (coordinator: "оценител").
- Label validator — `translate_labels.py` KEEP_LATIN requires "Shapley" and "alpha", but glossary 1.28
  decided "Шапли"; 7 entries in `labels_step11.json` write "Шапли" and will be rejected on merge unless
  the list is aligned. (α labels were moved to `$\alpha$` in the sources, so "alpha" is not an issue.)
- B19 — official BG subtitle fixed in summaryBg/onePagerBg only; the other 22 BG files need the same.
- Footnote keys — `balduzzi2019` shared with step 10, whose body still has the old (Balduzzi-only +
  PBT) text; `pluribus`, `daskalakis2009` reused (identical bodies). § 5.3 per-chapter labels.
- S05 — `implementation/step11/targetedReading/summary.md` Paper 3 (piKL = Jacob et al. 2022; Bakhtin
  et al. 2023) is not plotting code — not editable here.
- S06 — curated `terminology_EN_BG.md` spinning-top note → "(Balduzzi et al., 2019; Czarnecki et al., 2020)".
- Typography 5.1/5.2 and extra bold (0.5) in the summary: left to the central pass (bold removed only in
  sentences rewritten here).
- Build — `build_reports.py` crashes printing "✓" on a cp1251 console; ran with `PYTHONIOENCODING=utf-8`.
  Also for the candidate: `validate.py` does not save the check-5 (coalition-pool) ratios; they exist only
  in EXECUTION_NOTES (needs a code change + rerun).

## Numbers changed (old → new, where)
- Reward formula $(1-\alpha)r_{sparse}+\alpha\,credit$ → $\alpha r_{sparse}+(1-\alpha)credit$ — summary EN/BG, report EN/BG, fig. 68.
- "~4.4x the sparse baseline" → "Shapley agents' score ~4.5x the sparse" (0.0484/0.0109; the gap ratio is 3.5x) — Table 41, one-pagers, report tables/text, figs. 68–69; dropped where it described the gap.
- "any tier, α ≥ 0.3: −0.001 … −0.004" → scale −0.0003 … −0.0035 (all negative); smoke −0.0031 … +0.0012 (none significant) — Table 41, report table (smoke row was "~0 … −0.003"), fig. 68.
- Takeaway "α = 0 → ~0.25 floor" → ~0.29 (near 0.25).
- One-pager "0.525 → 0.013" → "0.54 → 0.013".
- "~10x smoke" / "effect grows with game size" → "12x the smoke gap at synergy 0.1; game size and training length confounded".
- "`**` = > 2 SE" → "+ ≈ p < 0.12 with 5 seeds".
- "1950" → "published 1964" (summary, one-pagers, reports).

## Figures (file — what changed — printed size now)
- `sls_coalition{,_bg}.png` (fig. 64) — fs 8.0–8.6 → 10; boxes widened; note now "in this engine … negotiation is not modelled" (C03); "Step 07" → Chapter 7; result box re-worded (no "cross-pair edge"/"засаден"/"чифт"). 17.6 cm, scale 0.85 → 8.5 pt.
- `impl_coalition_graph{,_bg}.png` (fig. 65, G03) — was an all-zero baseline-pool matrix; now the planted-alliance matrix from `smoke_results.json` (10 / −1 / 0), RdBu ±10, no title, 300 dpi. 11.2 cm → 10–11 pt.
- `shapley_credit{,_bg}.png` (fig. 66) — fs → 10.2; core box full width at the bottom (no overlap); value box widened, math survives translation; "fair" → "satisfies Shapley's axioms"; SLS empty core stated as constant-sum. 17.6 cm, scale 0.86 → 8.7 pt.
- `impl_shapley_attribution{,_bg}.png` (fig. 67, G05) — was the asymmetric position only; now grouped bars symmetric vs asymmetric from `smoke_results.json`, equal-share line, no title, 300 dpi. 12.7 cm → 9.6–10 pt.
- `mappo_blend{,_bg}.png` (fig. 68, G06) — formula fixed; boxes no longer overlap; MEASURED/TRADE-OFF boxes translated ($\alpha$ in sources); fs → 10. 17.6 cm, scale 0.88 → 8.8 pt.
- `impl_sweep_coalition_gap{,_bg}.png` (fig. 69, G07) — (12.4×4.4 in, 120 dpi) → (7.0×3.8 in, 300 dpi); no suptitle; legend below the panels (it covered the α=0→0.1 lines); now has a BG twin. 17.6 cm → 9.5–9.9 pt (was 4.5–6.7).
- `egta_spinning_top{,_bg}.png` (fig. 70, G08) — fs → 10; result box widened; "(КОЛЕЛО)" → "strong cyclic part", "Step 10" → Chapter 10, EGTA note corrected (C09). 17.6 cm, scale 0.85 → 8.5 pt.
- Fig. 71 `impl_spinning_top.png` (G09) — removed from summary EN/BG and reports (coalition-pool values exist in no results file; Table 42 carries them). File left in place, unreferenced.
- `plotting.py`: no-argument run now draws figs. 65/67/69 from saved results only, straight into `summary/` (old simulating path behind `--config`). Results files hash-checked unchanged before/after every run. Copies of the three impl figures (+ `_bg`) placed in `figures/`; `report_bg.md` links the `_bg` twins.
- Report-only `impl_coalition_timeline.png`: caption was false (it shows only hostile scores); re-captioned honestly. Its in-figure title still reads "(PREDICTION)" — regenerating needs a simulated game, so left.

## Remaining overflow / legibility warnings
- Renderer (save-time fitting, floor fs 9.5): no overflow warnings. Printed crops (`renders_fix/step11/ch11/`) read clean; figure text ≈ 75–85 % of caption height.
- BG one-pager fits only at the tightest setting (8 pt / 1.1 cm) after trimming wording; EN at 9 pt / 1.3 cm.

## Verification (build ok? check_headings / check_captions output for this step)
- `build_reports.py --step step11 --type all`: all six PDFs built (summary BG 14 pp / EN 12 pp; report BG 19 pp). BG one-pager 1 page.
- `check_headings.py`: 44 PDFs, 0 missing headings. `check_captions.py`: 24 PDFs, 0 with unaccounted figures.
- Built PDFs scanned: no U+FFFD; no "Шейпли", "кредит", "засаден", "развръзка", "героя", "оскъд", "критик/критична", "1950", "Step"; Cyrillic inside `\text{}` renders.
