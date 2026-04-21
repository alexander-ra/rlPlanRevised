# Paper Formatting Guidelines for Academic PDFs

Reference document for session reports, research proposals, and thesis-track
deliverables in this repo. Compiled from IEEE/ACM author guidelines, IMRaD
conventions, major university dissertation manuals (Indiana, Stanford, UNC,
UCSF, Harvard GSAS, UC Irvine, WSU) and established scientific writing
style guides.

These are **conventions**, not laws. Individual venues override them —
always check a specific conference/journal's call for papers before
submission. For internal Ruse University session reports the target is
"recognizable as academic-quality formatting to any reviewer."

---

## 1. Document Structure

### Research proposals / session reports (what we write here)

Standard section order:

1. **Abstract** — 150–300 words, self-contained, written last
2. **Introduction** — motivation, problem, research gap, contributions preview
3. **Review of Existing Solutions** (a.k.a. Literature Review / Background)
4. **Proposed Solution** — methodology, contributions, scope
5. **Expected Outcomes / Timeline** (optional; can live inside §4)
6. **Conclusion**
7. **References**

PhD proposals commonly run 15–30 pages. Session reports 5–15.

### Empirical papers (IMRaD — once we have results)

Introduction → Methods → Results → Discussion. An extended variant
(Introduction, Literature Review, Methods, Results, Discussion, Conclusion)
dominates high-impact journals. Methods/Results use past tense; Discussion
connects findings to prior work and limitations.

### Abstract rules

- **Length:** 150–300 words. Engineering/applied sciences lean 150–200;
  life sciences 200–250; medicine up to 400 with structured headings.
- **Self-contained** — not part of the introduction; must make sense in
  isolation because indexers (Google Scholar, arXiv) display it alone.
- **Covers four things:** problem/motivation, approach, result (or
  expected contributions for a proposal), implication.
- **No citations, no undefined acronyms, no figure references.**
- **Write it last.**

---

## 2. Page Layout and Typography

### Margins

- **1 inch (2.54 cm) on all sides.** Standard across IEEE, ACM, and every
  major dissertation manual.
- If bound physically, some manuals require 1.5" left margin for the
  gutter. Electronic-only: 1" everywhere.

### Font

- **Serif font for body** (Times New Roman, Liberation Serif, DejaVu
  Serif for Cyrillic). Sans-serif acceptable for headings.
- **Body size:** 10–12 pt.
  - 10 pt for two-column conference format (IEEE, ACM)
  - 11 pt for single-column research reports (our default)
  - 12 pt for dissertations / formal theses
- **Do not substitute fonts** if targeting a template. Install the font
  the template requires.
- **Embed all fonts in the PDF.** Pandoc + Tectonic handles this by
  default; verify before submission.

### Line spacing

- **1.0 (single)** — conference proceedings, two-column
- **1.15–1.25** — research proposals, session reports (our default: 1.25)
- **1.5–2.0 (double)** — dissertations, drafts under review

### Paragraph style

- **Justified text** is standard for PDF output.
- **Indent first line** of each paragraph *or* use blank line between
  paragraphs — pick one and stay consistent.
- **Widows and orphans** (single lines stranded at top/bottom of page):
  avoid. LaTeX/Tectonic handles this automatically.

### Page numbers

- **Yes, always.** Bottom center or bottom right.
- Roman numerals (i, ii, iii) for front matter; Arabic (1, 2, 3) from
  Introduction onward.

### Headings

- **Numbered sections** are standard (IEEE, most university manuals).
- Use a clear hierarchy: §1, §1.1, §1.1.1. Don't nest deeper than three
  levels in short documents.

---

## 3. Writing Style

### Tone

- Formal, objective, third-person.
- "We" is acceptable in research proposals, methods sections, and
  collaborative work. "I" is discouraged in science/engineering;
  accepted in humanities and reflective sections.
- Avoid contractions (don't, it's, we've) in formal prose.
- Avoid colloquialisms, hyperbole, and promotional language ("novel
  revolutionary breakthrough" ← don't).

### Voice

- Mix active and passive according to what the sentence is doing:
  - **Active** for arguments, claims, and contributions ("The framework
    extends…", "We propose…").
  - **Passive** for methods and results when the actor is irrelevant
    ("Samples were collected…", "The model was evaluated on…").

### Clarity and concision

- Prefer short sentences. Split anything running over ~30 words.
- One idea per paragraph.
- Define every acronym on first use, in both abstract and body (they are
  read independently). Example: "Counterfactual Regret Minimization
  (CFR)".
- Avoid jargon your committee may not have in active memory — or define
  it briefly on first use. "Wider audience" means more definitions, not
  fewer.

### Tense

- **Introduction / background:** present tense for established facts
  ("CFR converges at O(1/√T)"), past tense for specific studies
  ("Brown and Sandholm [2] demonstrated…").
- **Methods / Results:** past tense ("We trained…", "Accuracy reached…").
- **Discussion / Conclusion:** present tense for claims, future tense
  for follow-up work.

---

## 4. Punctuation Specifics (common error sources)

- **Em dash (—)**: for parenthetical breaks. No spaces around it in US
  style; spaces around it in UK style. Pick one and be consistent.
  Pandoc renders `---` as em dash.
- **En dash (–)**: for numeric ranges (pp. 418–424, 2020–2025). Pandoc
  renders `--` as en dash.
- **Hyphen (-)**: for compound adjectives ("multi-agent", "real-time")
  and hyphenated names. Never for ranges, never for parenthetical
  breaks.
- **Oxford (serial) comma**: use it consistently throughout. "A, B, and
  C" is preferred in formal academic writing.
- **Quotation marks**: straight ASCII in source; let Pandoc convert to
  curly quotes. Don't mix curly and straight.
- **One space after a period**, not two.

---

## 5. Citations and References

### In-text

- Numbered `[1]` (IEEE) or author-year `(Brown, 2018)` (APA/Harvard).
  Pick one per document. Numbered is standard in engineering/CS; author-
  year in social sciences and humanities.
- Cite on first use of a claim, and again only when ambiguity would
  arise.

### Reference list

- **Consistent style** end-to-end: same author-name format, same
  journal-title treatment (italic vs. upright), same page-range dash.
- **Resolve every citation**: a number that appears in the body must
  exist in the bibliography; an entry in the bibliography that is never
  cited should be removed.
- **Count:** typical ranges
  - Conference paper: 20–40
  - Journal article: 40–80
  - PhD thesis: hundreds
  - Research proposal / session report: 8–20 (quality over coverage)
- **Prefer peer-reviewed sources** over arXiv preprints when both exist.
  Preprints are acceptable for very recent work not yet indexed.

---

## 6. Figures, Tables, and Equations

- **Numbered and referenced** from the text ("See Figure 1", "Table 2
  reports…"). No floating figures without a mention.
- **Captions:** below figures, above tables (academic convention).
- **Captions describe, not just label.** "Figure 1: Training loss" is
  weak. "Figure 1: DQN training loss on CartPole-v1 over 500 episodes;
  shaded band is ±1σ over 5 seeds." is useful.
- **Equations numbered** if referenced later. Don't number throwaway
  inline math.
- **Units and symbols** consistent (one notation for the same concept
  across the whole document).

---

## 7. Bilingual Documents (our EN/BG setup)

- **Cyrillic-capable fonts required** for BG: DejaVu Serif/Sans, Liberation
  Serif/Sans, or Noto Serif. Times New Roman on some systems lacks full
  Cyrillic coverage.
- **Keep reference numbering identical** across EN and BG versions so a
  reader can cross-check.
- **Translated technical terms**: consult `deliverables/terminology_EN_BG.md`
  and be consistent. A term coined in one language should be glossed
  parenthetically in the other on first use (e.g., "регрет (regret)").
- **Formatting parity**: if you change the EN layout (margins, spacing,
  heading levels), mirror it in BG to preserve visual consistency.

---

## 8. Pre-submission Checklist

Before building the final PDF:

- [ ] Abstract is 150–300 words, self-contained, no citations
- [ ] All acronyms defined on first use in body (and separately in abstract)
- [ ] All figures/tables numbered and referenced from the text
- [ ] All in-text citations resolve to a reference list entry
- [ ] Reference list sorted consistently (by appearance or alphabetic)
- [ ] No typos in high-visibility locations (title, abstract, headings)
- [ ] Section numbering enabled; heading hierarchy makes sense
- [ ] Page numbers present
- [ ] Font is serif, 10–12 pt, embedded in PDF
- [ ] Margins 1 inch / 2.54 cm on all sides
- [ ] Line spacing consistent throughout
- [ ] One voice, one tense per section — no mid-paragraph switching
- [ ] No first-person "I" unless explicitly a reflective section
- [ ] No contractions in formal prose
- [ ] Em/en/hyphen dashes used correctly
- [ ] Oxford comma applied consistently (or consistently omitted)

---

## Sources

- [IEEE Paper Format — Scribbr](https://www.scribbr.com/ieee/ieee-paper-format/)
- [Manuscript Templates for IEEE Conference Proceedings](https://www.ieee.org/conferences/publishing/templates)
- [ACM Primary Article Template](https://www.acm.org/publications/proceedings-template)
- [ACM FAccT 2026 Author Guide](https://facctconference.org/2026/authorguide.html)
- [IMRaD Report Guide — George Mason University Writing Center](https://writingcenter.gmu.edu/writing-resources/imrad/writing-an-imrad-report)
- [Structure of a Research Paper: IMRaD Format — University of Minnesota](https://libguides.umn.edu/StructureResearchPaper)
- [Doctoral Dissertation Formatting — Indiana University Bloomington](https://graduate.indiana.edu/academic-requirements/thesis-dissertation/doctoral-guide/formatting.html)
- [Dissertation Format Requirements — UNC Chapel Hill Graduate School](https://gradschool.unc.edu/academics/thesis-diss/guide/format.html)
- [Dissertation Formatting — Stanford Student Services](https://studentservices.stanford.edu/my-academics/earn-my-degree/graduate-degree-progress/dissertations-and-theses/prepare-your-work-0)
- [Dissertation Formatting Guidance — Harvard GSAS](https://gsas.harvard.edu/resource/dissertation-formatting-guidance)
- [Thesis/Dissertation Formatting Manual — UC Irvine](https://guides.lib.uci.edu/gradmanual/pagination)
- [Academic Writing Style — USC Libraries](https://libguides.usc.edu/writingguide/academicwriting)
- [Writing a Research Proposal — USC Libraries](https://libguides.usc.edu/writingguide/assignments/researchproposal)
- [Research Proposal Structure — Massey OWLL](https://owll.massey.ac.nz/assignment-types/research-proposal-structure.php)
- [Language and Style — University of Leeds Library](https://library.leeds.ac.uk/info/14011/writing/221/language-and-style)
- [How to Write a Good Abstract — PMC (Ranganathan, Andrade)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3136027/)
- [Abstract and Keywords Guide — APA Style 7th Ed.](https://apastyle.apa.org/instructional-aids/abstract-keywords-guide.pdf)
- [Common Punctuation Issues in Scientific Writing — BioScience Writers](https://www.biosciencewriters.com/Common-Punctuation-Issues-in-Scientific-Writing.aspx)
- [Em/En/Hyphen — Merriam-Webster](https://www.merriam-webster.com/grammar/em-dash-en-dash-how-to-use)
- [The Oxford Scientist Style Guide](https://oxsci.org/wp-content/uploads/2021/01/The-Oxford-Scientist-Style-Guide.pdf)
