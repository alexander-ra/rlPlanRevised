# Wave 3 fix brief — one chapter (step NN)

You apply the September 2026 final-review findings to **one chapter**. The review is
done; your job is to apply it faithfully, verify the result as a reader will see it, and
log what you did. Other agents fix other chapters in parallel.

Read first: `deliverables/finalReview/TRIAGE.md` (the decisions), your
`stepNN_review.md` (the findings), `GLOSSARY_DECISIONS.md` (terminology), and
`REVIEW_BRIEF.md` (conventions the findings follow).

## What you may edit — and nothing else

- `deliverables/reports/stepNN/**` — summaryEn.md, summaryBg.md, onePager.md,
  onePagerBg.md, report_en.md, report_bg.md, the `make_*.py` figure scripts, this step's
  `_diagram_utils.py`, and the figure PNGs these produce.
- `implementation/stepNN/**` — **plotting code only** (font sizes, figure sizes, dpi,
  label strings, a `__main__` that plots from saved results). No algorithm changes.
- `deliverables/finalReview/fixes/labels_stepNN.json` — your figure-label overlay:
  a JSON object `{"English label exactly as in the script": "Bulgarian"}`.
- `deliverables/finalReview/fixes/stepNN_log.md` — your log (format below).

Do **not** edit: `scripts/figures/out/figure_labels.json` (shared; your overlay is merged
into it afterwards), the glossaries, `scripts/**`, `SOURCE_GAPS.md`, other steps' files.
Do not commit, do not build bundles. If a finding needs a shared file, log it as
"central" and move on.

## Running things

Project rule (`implementation/WORKFLOW.md`): agents do not run training or experiments.
You **may** run plotting scripts (they read saved results) and the PDF build. Exceptions,
decided by the candidate, are listed per step in TRIAGE § B — only those.
Never let a plotting run silently overwrite a results file; if a script recomputes and
re-saves results, stop and log it instead.

## Order of work

1. **Text (EN and BG).** Apply B, T-occurrence, C, S and X findings by exact search and
   replace — the quotes in the review are exact copies of the sources. If a quote no
   longer matches (another finding already rewrote the sentence), apply the intent by
   hand and note it in the log. C/S fixes usually touch both languages; keep EN and BG
   saying the same thing.
   - **Glossary:** apply every ✅ row of `GLOSSARY_DECISIONS.md` that occurs in your files
     (not just the ones your review listed — grep for the "Now" forms). **Leave rows 1.10
     (blueprint), 2.3 (self-play) and 2.5 (bootstrapping) untouched** — the candidate has
     not chosen yet; a later pass does them.
   - **Do not** apply the typography of `GLOSSARY_DECISIONS.md` § 5.1–5.2 (dashes, decimal
     comma, thousands separator). That runs centrally *after* all chapters, so your
     exact-quote replacements keep matching. Write numbers in new text the way the
     surrounding text does.
   - Footnotes: fix their content (S findings). The shared-label problem (§ 5.3) is
     central — ignore it.
   - Stale references to chapters 13–15 / "Step N": rewrite as the findings propose.
2. **Figures.** For every figure in the chapter:
   - Captions: replace the English alt text in `summaryBg.md` with the Bulgarian from your
     G findings.
   - Legibility: in the script, raise every text size so it prints at ≥ 8.2 pt
     (printed pt = fontsize × printed width ÷ saved width in inches; at the usual
     17.6 cm print width that means fs ≥ ~9.6 — use 10). Fix overlapping notes, clipped
     labels, soft images (dpi ≥ 200). Enlarge boxes rather than shrinking text.
   - Regenerate the English figure (run the script) and the Bulgarian twin:
     `python scripts/figures/render_bg_figures.py --only stepNN --labels-overlay deliverables/finalReview/fixes/labels_stepNN.json`
     The renderer now re-wraps Bulgarian text to fit its box and prints any label that
     still overflows — fix every one it lists (bigger box, shorter wording).
   - If `summaryBg.md` points at the English PNG, point it at the `_bg` twin.
   - Look at the result: `python scripts/figures/render_printed.py --pdf deliverables/summaries/stepNN_bg.pdf --out deliverables/finalReview/renders_fix/stepNN`
     after building (step 4), and Read the crops. Judge them as the review did.
3. **R-items** (TRIAGE § B) for your step, exactly as decided there.
4. **Build and verify:**
   `python scripts/build_reports.py --step stepNN --type all` (EN + BG summary, report,
   one-pager). Then `python scripts/check_headings.py` and `python scripts/check_captions.py`
   (they check all steps; look at yours). Render the crops (step 2) and check every figure.
   The BG one-pager must still fit on one page (the builder retries; check its message).
5. **Log** — `deliverables/finalReview/fixes/stepNN_log.md`:
   ```
   # Step NN — fixes applied
   Applied: <count> · Skipped: <count> · Central: <count>
   ## Skipped (id — reason)            e.g. S3 not trivial; quote gone; needs a rerun
   ## Central (id — what is needed)    shared files, glossary rows, build issues
   ## Numbers changed (old → new, where)
   ## Figures (file — what changed — printed size now)
   ## Remaining overflow / legibility warnings
   ## Verification (build ok? check_headings / check_captions output for this step)
   ```

## Final message

≤ 10 lines: counts applied/skipped/central, anything that did not build or still looks
wrong, and anything the candidate should look at first.
