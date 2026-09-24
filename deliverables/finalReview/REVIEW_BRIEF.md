# Final review brief — one chapter (step NN)

You are reviewing **one chapter** of a PhD candidate's 12-chapter study corpus (steps
01–12). The corpus is published as a ~226-page Bulgarian summaries bundle, read by the
supervisors and a handful of others. The same careful read also serves a second purpose:
extracting material for the official **Chapter I** of the dissertation (see
`deliverables/finalReview/CHAPTER1_SKELETON.md` — read it first).

The candidate writes English first; **Bulgarian is what readers see.** The BG text
already went through a Bulgarian-specific LLM fluency pass, so it is mostly fluent. What
survives that pass is what this review is for.

**You are read-only.** Write exactly two files and touch nothing else:

- `deliverables/finalReview/stepNN_review.md` — findings
- `deliverables/finalReview/stepNN_extract.md` — Chapter I material

Other agents are reviewing the other chapters in parallel; shared files (glossary, build
scripts, figure label mapping) are edited later by one person only — propose changes to
them in your findings instead.

## Inputs for step NN

| What | Where |
|---|---|
| Chapter text EN / BG (the bundle chapter) | `deliverables/reports/stepNN/summary/summaryEn.md`, `summaryBg.md` |
| One-pager EN / BG | `…/summary/onePager.md`, `onePagerBg.md` |
| Step report EN / BG (consistency only) | `deliverables/reports/stepNN/report_en.md`, `report_bg.md` (steps 05, 06 have none) |
| Figures as printed in the BG bundle, with caption | `deliverables/finalReview/renders/chNN/*.png` + `renders/manifest.json` (printed width, effective ppi, caption) |
| Full BG pages of the chapter | render with `python scripts/figures/render_printed.py --chapter N --pages` (110 dpi) |
| EN bundle, for comparison | `python scripts/figures/render_printed.py --pdf deliverables/bundles/allSummaries_en.pdf --out deliverables/finalReview/renders_en --chapter N` |
| Figure sources | `deliverables/reports/stepNN/summary/make_*.py`, `implementation/stepNN/**`; the list of all plotting scripts is `plotting_scripts()` in `scripts/figures/extract_labels.py`. BG variants are produced by `scripts/figures/render_bg_figures.py` from the label mapping `scripts/figures/out/figure_labels.json` |
| Terminology | `deliverables/terminology_EN_BG.md` (curated conventions) and `llmPipeline/glossary_settled.md` (3.3k settled terms — known to contain inconsistencies) |
| Claims already known to lack a source | `deliverables/reports/SOURCE_GAPS.md`, your step's section |
| Figure labels still in English | `deliverables/reports/FIGURE_LABELS_BG.md`, last section |

| **Calibration example** — the finished pilot | `deliverables/finalReview/step07_review.md`, `step07_extract.md`. Match its depth, format and tone. |
| **Gap validation** (literature, Sept 2026) | `deliverables/finalReview/lit_gaps.md`, `lit_evaluation.md` — your extract's *Gaps* section must be consistent with these: do not restate a gap they show as narrowed/closed as if it were open. Their "Citation corrections" list names errors in specific chapters — fix any in yours. |
| The candidate's own proofreading comments (Aug 2026, on an older build of the BG bundle) | `deliverables/finalReview/user_comments_2026-08-01.json` — field `chapter` (0 = table of contents; those concern headings, check the ones matching your chapter's headings). Most were applied since; check each one for your chapter and report any **not applied** as a finding (quote the comment). |

Python: activate `.venv` (`source .venv/Scripts/activate`); PyMuPDF (`fitz`) and PIL are
installed. View images with the Read tool. You may use WebSearch / WebFetch to verify a
citation — **never propose a reference you have not verified**; say how you verified it.

## Known corpus-wide defects (confirm for your chapter, don't rediscover)

- **Every figure caption in `summaryBg.md` is English** — the image alt text, which the
  translation pipeline skipped. Provide a full Bulgarian caption for each of your figures
  (as findings G-…).
- Chapters 13–15 were **never written**. Any reference to them, or to "Step 13/14/15", or
  to future work that presumes them, is stale.
- **Bulgarian labels overflow the boxes of the diagram figures** (boxes are sized for the
  shorter English; see `renders/ch07/p134_f1.png`). This is likely fixed centrally —
  auto-fitting text in the BG render or the shared `_diagram_utils.py` box helper — so for
  overflow just list each affected box/label (one finding per figure), and propose a
  shorter BG wording where one exists. Font-size hacks per figure are not needed for it.
- One mapping entry has a corrupted line break (`\н` — backslash + Cyrillic н — printed
  literally: "Предварително\нубеждение"). Already known; report any other literal
  escape you see.
- **Decided centrally — do not report per occurrence** (one line in your Summary with the
  count is enough): hyphen " - " used as a dash (→ en dash), decimal point / "20,000"
  thousands separator in BG text (→ decimal comma, "20 000"), bold spans the translation
  pipeline added that the EN does not have, and footnote labels shared between chapters in
  the single-document bundle (F07-X01).
- **Glossary-level errors already found** in the pilot (F07-T01 … T14 — e.g. "изследване"
  for exploitation, "залог" for call, 1st-person verb forms "рандомизирам / оптимално
  отговарям", "неразрешим" for intractable, "изтичане" for leak, "задно" for posterior,
  "наш противник" for the Nash opponent, "съгласуван" vs "състоятелен" for consistent):
  do not re-report them as T findings; **do** report their occurrences in your chapter as
  B findings that cite the T id, with the exact quote and proposed text. Report *new*
  glossary-level problems as T.
- **Figure legibility floor:** printed pt = matplotlib fontsize × (printed width ÷ saved
  width in inches). Body text is 10.9 pt; the floor is ≈ 8.2 pt printed, which at the usual
  17.6 cm print width means fs ≥ ~9.6. When BG text overflows a box, the fix is to wrap or
  enlarge the box — never to shrink the font below the floor.
- Algorithm and system names stay in Latin script (CFR, DQN, PPO, MCCFR, Libratus,
  Pluribus, OpenSpiel, Shapley …); Kuhn → Кун, Leduc → Ледюк.

## What to check

### G — Figures (highest priority after BG)
For every figure in the chapter, look at the printed crop and decide:
- **Legible at print size?** The caption in the crop is body-size type. A label clearly
  smaller than ~75 % of the caption's letter height, text overlapping lines/other text,
  clipped labels, or a legend you have to squint at → not legible.
- **Soft/blurry?** `effective_ppi` < 150 in the manifest will look soft in print.
- **English left in the BG figure** (beyond the Latin-script names above)? Decimal point
  instead of decimal comma?
- **Does the figure show what the text and caption claim?** Wrong/stale numbers, axis
  labels that contradict the text.
- **Does it earn its place?** (Rarely an issue; flag only clear cases.)

For each problem name **the generating script** and **the concrete change**
(e.g. "`make_bayes_loop_figure.py`: box text fontsize 7 → 10, figsize (10,4) → (8,4.2)
so it prints larger; dpi 110 → 200"), or the label-mapping entry to add/fix. Figures
without problems get one line saying so — the reader needs to know you looked.

### B — Bulgarian language (highest priority)
Compare `summaryBg.md` with `summaryEn.md` section by section (and `onePagerBg.md` with
`onePager.md`). Report:
1. **Meaning errors** — the BG says something different from, or less than, the EN.
2. **Terminology** — a term used inconsistently inside the chapter, deviating from
   `terminology_EN_BG.md`, or a settled term that is itself wrong/awkward for a Bulgarian
   academic reader (the last kind is a **T** finding — glossary level, affects all chapters).
3. **Calques and unnatural constructions** a Bulgarian academic reader would stumble on —
   literal English word order, noun piles, "прави смисъл"-type calques, wrong register.
4. **English left in the text** (untranslated fragments, headings, table cells).
5. **Typography** — „…“ quotes, en/em dashes, decimal comma, `ѝ`, spacing around units.

Do **not** rewrite sentences that are correct and natural just because you would phrase
them differently. Every proposed change must fix something you can name.

### C — Content
- Technical correctness of claims, definitions, formulas.
- Overclaims: "first", "proves", "state of the art", "always", "guarantees" — flag if the
  evidence (a toy game, one seed, a replication) does not carry it.
- **Numbers consistent** across summary / report / one-pager, EN and BG.
- Stale references (chapters 13–15, planned work that did not happen, "Step" naming where
  the bundle says "Chapter").

### S — Sources
- For each `SOURCE_GAPS.md` item of your step: propose a **verified** citation, or propose
  softening/removing the claim. Say which.
- Spot-check the existing citations that carry the chapter's key claims: real paper,
  correct authors/year, and does it actually say that?
- Other important claims that lack a source and are not in `SOURCE_GAPS.md`.

### X — Structure (light touch)
The bundle gets fixed, not endlessly polished. Flag only clear problems: a section that
repeats another, a paragraph that contradicts the chapter's own results, an ordering that
confuses. Do not propose restructuring for taste.

## Output 1 — `stepNN_review.md`

```
# Step NN — final review

**Summary:** 2–4 sentences: overall state, the few things that matter most.
**Counts:** S1 n · S2 n · S3 n   (by category: G n · B n · T n · C n · S n · X n)

## G — Figures
### FNN-G01 · S1 · <short label>
- **Where:** <figure file / page> — caption "…"
- **Problem:** …
- **Fix:** <script + concrete change, or mapping entry>

## B — Bulgarian language
### FNN-B01 · S2 · meaning
- **Where:** summaryBg.md § "<BG heading>" — "<exact BG quote, ≥ 6 words, greppable>"
- **EN:** "<the corresponding EN>"
- **Now → Proposed:** "<current BG>" → "<proposed BG>"
- **Why:** …

## T — Glossary-level terminology
## C — Content
## S — Sources
## X — Structure
```

Quotes must be copied **exactly** from the source file so the fix can be applied by
search-and-replace. One finding per problem; group only true repeats (the same wrong term
in 9 places is one finding listing the 9 locations).

**Severity** — **S1**: wrong, misleading, illegible, or English in the Bulgarian text;
**S2**: clearly worth fixing; **S3**: optional polish (will usually be skipped — keep
these few).

## Output 2 — `stepNN_extract.md` (for Chapter I)

```
# Step NN — Chapter I extract
**Feeds:** § 1.x (primary), § 1.y
## Digest            (≤ the step's cap in CHAPTER1_SKELETON.md; EN; neutral
                      state-of-the-art voice, no "we learned"/"in this step")
## Key sources       (one line each, IEEE-like: authors, title, venue, year, DOI/arXiv;
                      mark [verified] or [unverified])
## Gaps              (what the literature does not do — each tied to C1/C2/C3 and to
                      the sources that show it)
## Own evidence      (results from this step worth ≤ 1 sentence in Chapter I: the exact
                      numbers, the file they come from, and the caveat — toy game, seeds…)
## Figure candidate  (0–1 figure for Chapter I, and why)
## To verify         (anything Chapter I must not cite before it is checked)
```

## Final message

Reply with ≤ 10 lines: the counts, the three most important findings, and anything you
could not check.
