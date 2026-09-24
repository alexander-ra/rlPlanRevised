# Brief — Bulgarian version of a new chapter (steps 13, 14, 15)

Translate one finished English chapter into Bulgarian: `summary/summaryEn.md` →
`summaryBg.md`, `summary/onePager.md` → `onePagerBg.md`, `report_en.md` → `report_bg.md`,
plus Bulgarian twins of its figures. Readers see the Bulgarian; it must read as natural
academic Bulgarian written by the candidate, not as a translation. The September 2026 review
of chapters 1–12 found what goes wrong — avoid all of it.

## Read first

- The English sources you translate, completely.
- `deliverables/finalReview/GLOSSARY_DECISIONS.md` — apply every ✅ row. For the rows still
  open (1.10 blueprint, 2.3 self-play, 2.5 bootstrapping, 1.18 oracle) use the form the
  corrected corpus currently uses ("план", "самообучение", "оракул"; for bootstrapping grep
  the corpus) so the candidate's later decision can be applied in one pass everywhere.
- `deliverables/terminology_EN_BG.md` (curated) and `llmPipeline/glossary_settled.md` (settled;
  where it conflicts with GLOSSARY_DECISIONS, GLOSSARY_DECISIONS wins).
- Two corrected Bulgarian chapters as models of register and conventions:
  `deliverables/reports/step08/summary/summaryBg.md`, `…/step11/summary/summaryBg.md`, and
  their `onePagerBg.md` and `report_bg.md`.
- The glossary-level findings in any `deliverables/finalReview/stepNN_review.md` (§ T) — they
  list the calques to avoid.

## Rules

- Meaning first: the Bulgarian says exactly what the English says — no additions, no
  omissions, same numbers, same hedges.
- Terminology from the glossaries; one concept, one word throughout the chapter; first use of
  a term: Bulgarian followed by the English in parentheses.
- No calques: not "прави смисъл", "в очакване" (in expectation), "изтичане" (leak),
  "двуигров", "неразрешим" (intractable), "задно" (posterior), "сходява", "персонализиран"
  (custom), "реално време" for wall-clock, "извън линия" for offline, first-person verb
  forms ("рандомизирам"), "герой" for hero, "проверка" for check, "пас" for fold.
- Names: algorithms, systems and datasets in Latin script (CFR, PPO, Pluribus, OpenSpiel,
  player2vec, PHH, iPoker, HandHQ…); people transliterated (Наш, Кун, Шапли); Kuhn → Кун,
  Leduc → Ледюк; Nash as an opponent type in quotes „Наш“, the concept "равновесие на Наш".
- "Глава N" for chapters; "раздел N.M" for sections.
- Keep the Markdown structure identical (headings, tables, math, footnote labels, image
  paths, attributes). Footnote *bodies* (bibliography) stay as in English except linking
  words; titles of papers stay in the original.
- Figure captions (the image alt text) in Bulgarian, pointing at the `_bg.png` twins.
- Typography: write numbers and dashes as in English while translating, then run
  `python scripts/bg_typography.py --apply --only stepNN` once at the end (en dashes, decimal
  comma, thousands separator).

## Figures

Render the Bulgarian twins with a label overlay you create at
`deliverables/finalReview/fixes/labels_stepNN.json` (`{"English label": "Bulgarian"}`):
`python scripts/figures/render_bg_figures.py --only stepNN --labels-overlay deliverables/finalReview/fixes/labels_stepNN.json`.
Fix every overflow the renderer reports (enlarge the box or shorten the wording, never shrink
below its floor). Plot from saved results only; if a script would recompute or overwrite a
results file, stop and use a plot-only path. Check printed legibility after the build with
`python scripts/figures/render_printed.py --pdf deliverables/summaries/stepNN_bg.pdf --out deliverables/finalReview/renders_new/stepNN_bg` and Read the crops.

## Build and verify

`PYTHONIOENCODING=utf-8 python scripts/build_reports.py --step stepNN --lang bg --type all`;
the BG one-pager must fit on one page (trim wording, not content, if needed);
`python scripts/check_headings.py`, `python scripts/check_captions.py` clean for your step.

Edit only `deliverables/reports/stepNN/**` (Bulgarian files and `_bg` figures),
`deliverables/finalReview/fixes/labels_stepNN.json` and your scratch subfolder. Do not commit.

## Final message

≤ 8 lines: files produced, word counts EN vs BG, figures with BG twins, build/check results,
and any term you had to decide that the candidate should confirm.
