# Deliverables Translation Audit + EN→BG Machine-Translation Workflow

## Context

The PhD hub keeps every deliverable bilingual (EN + BG). Steps 01–04 and the study
plan are fully translated, but recent work (steps 05–08) and the data request exist
**only in English**. As the project scales to all 15 steps, hand-translating each
deliverable is a bottleneck. The goal: a **streamlined Azure + Claude hybrid pipeline**
that turns any English deliverable into a publish-quality Bulgarian one with **only a
final human review** — smoke-tested on one step first, then applied to the backlog and
to every future step.

Decisions locked with the user: **engine = Azure Translator (bulk MT) + Claude
(structure-preserving pre/post-edit)**; **scope = supervisor-facing deliverables only**;
**pilot = step 07**.

---

## 1. Current translation coverage (the audit)

**Fully bilingual already (EN+BG) — no action:**
- Study plan: all 9 sections (`studyPlan/en/*` ↔ `studyPlan/bg/*`)
- Reports steps 01–04: `report_en/bg.md` + `summary/summaryEn/Bg.md`
- `reports/ruseMay/report.md` ↔ `report_bg.md`
- `terminology_EN_BG.md` (the bilingual glossary itself — not a translation target)

**EN-only — needs BG (in scope, "Tier 1", ~332K chars):**

| Content unit | File | EN chars |
|---|---|---:|
| step05 summary | `reports/step05/summary/summaryEn.md` | 41,738 |
| step06 summary | `reports/step06/summary/summaryEn.md` | 135,668 |
| step07 report | `reports/step07/report_en.md` | 34,536 |
| step07 summary | `reports/step07/summary/summaryEn.md` | 35,069 |
| step07 onePager | `reports/step07/summary/onePager.md` | 4,017 |
| step08 report | `reports/step08/report_en.md` | 34,206 |
| step08 summary | `reports/step08/summary/summaryEn.md` | 35,244 |
| step08 onePager | `reports/step08/summary/onePager.md` | 4,563 |
| data request | `dataRequest/data_request_en.md` | 7,019 |
| **Total** | | **~332,060** |

**Out of scope (internal / non-deliverable EN-only, "Tier 2", ~291K):** step04
`full paperanalysys.md`, step06 `CHAPTER_PLAN.md` + `research/*.md` (5 files), all
`ruseMay/` planning docs, `reports/README.md`. Left untranslated.

**Flags (separate from this work):**
- `reports/step01/report_bg.md` is a **21-line stub** vs a 300-line EN original — an
  existing translation gap to backfill later (out of scope here, but noted).
- step05 and step06 have **no `report_en.md` at all** (only summaries) — a *content*
  gap, not a translation gap.
- `onePager.md` (step07/08) breaks the naming convention (no `_en`/`En` suffix); BG
  output will be written as `onePagerBg.md` to stay parallel.

---

## 2. Glossary assessment (is it sufficient?)

**Verdict: strong enough to steer MT, but consolidate + extend first.**

Strengths: `terminology_EN_BG.md` has ~196 term pairs across 7 domains **plus**
prose guidelines that cover the hard parts — false-friend warnings (несъвършена vs
непълна информация; промишлен vs продуктивен), the **first-mention rule** (BG term +
English in parentheses), "keep algorithm abbreviations & math notation in Latin", and
formal-register guidance. Poker jargon (VPIP, PFR, chip dumping, Kuhn/Leduc, HSD, EMD)
is covered. The already-human-translated steps 01–04 + study plan are gold-standard
**few-shot references**.

Gaps to fix before scaling (small, one-time):
1. **Three inventories drift.** `terminology_EN_BG.md` (196), `studyPlan/*/09_glossary.md`
   (55), and `add_glossary_markers.py`'s `TERM_MAP` (~55) are maintained separately.
   → Designate `terminology_EN_BG.md` as **single source of truth** and derive a
   machine-readable `glossary.tsv` (English⇥Bulgarian⇥keep-latin-flag) from it for the
   pipeline. Do **not** rewrite the other two now; just stop adding new terms to them.
2. **Sparse RL core.** Add ~15 missing general-RL terms (temporal-difference,
   bootstrapping, on/off-policy, actor-critic, entropy regularization, epsilon-greedy,
   softmax/Boltzmann, KL divergence, trust region, replay ratio, return normalization…).
3. **No morphology notes.** Add one short paragraph to the guidelines noting Bulgarian
   inflection so the human reviewer knows Azure will need agreement/declension fixes.

---

## 3. Engine choice & volume math (why Azure free tier fits)

| Service | Free tier | Fits backlog (332K)? | Fits a future step (~75K)? |
|---|---|---|---|
| **Azure Translator F0** (chosen) | **2,000,000 chars / month** | Yes, 6× headroom | Yes, easily |
| DeepL API Free | 500,000 chars / month | Yes, but tight | Yes |
| Google Cloud Translation | 500,000 chars / month | Tight | Yes |

Azure F0 (2M/mo) clears the entire backlog **and** all remaining steps 09–15 within a
single month if desired. One free Azure account: create an **Azure AI Translator**
resource, tier **F0**, note the **key** + **endpoint** + **region** (store in a local
`.env`, never commit). *(Confirm the 2M limit on the pricing page at signup — Azure
occasionally revises free quotas.)*

**Division of labor** (the "feed Azure plain text, agent rebuilds it" design):
- **Azure = bulk sentence MT.** Receives only translatable prose, returns Bulgarian.
- **Claude = everything structural + terminological.** Protects non-translatable spans,
  enforces the glossary + first-mention rule, and reassembles valid markdown.

---

## 4. The pipeline — `scripts/translate_deliverable.py`

A new script that takes an English `.md` and produces its BG twin. Mirror the conventions
of the existing `scripts/build_reports.py` (argparse, `REPO_ROOT` pathing, `--step`).

**Stage A — Protect & segment (Claude/rule-based, in-script):**
Walk the markdown and split into an ordered list of blocks, each tagged
`translate` or `keep`. **Keep verbatim** (never sent to Azure):
- Fenced code blocks ```` ``` ````, inline `` `code` ``, code paths in backticks
- LaTeX: `$...$`, `$$...$$`, `\(...\)`
- The HTML title comment header (`<!-- OFFICIAL PhD TITLE ... -->`)
- URLs / image paths inside `![alt](path)` and `[text](url)` — **path kept, alt/text
  translated**
- Table pipe structure `|---|` (cell *contents* translate individually)
- Algorithm abbreviations from the glossary's keep-latin list (CFR, DQN, PPO, RNR, …)

**Stage B — Azure translate (per translatable segment):**
- POST to `…/translate?api-version=3.0&from=en&to=bg&textType=html`.
- Wrap protected inline spans as `<span class="notranslate">…</span>` so Azure passes
  them through untouched (native Azure HTML behavior).
- Inject glossary terms as **dynamic dictionary** markup so Azure emits the mandated BG
  term: `<mstrans:dictionary translation="Безопасна експлоатация">Safe exploitation</mstrans:dictionary>`.
- Batch segments to respect Azure's per-request array/size limits.

**Stage C — Reassemble (in-script):**
Stitch translated segments back into the original block skeleton → valid BG markdown
with identical structure, figure paths, tables, and math.

**Stage D — Claude glossary/register post-edit pass (agent):**
A focused Claude pass over the reassembled `_bg.md` that:
- Applies the **first-mention convention** (first use of each term → `BG термин (English)`).
- Fixes Bulgarian inflection/agreement Azure gets wrong.
- Cross-checks terminology against `terminology_EN_BG.md` and the **existing human BG
  translations** (steps 01–04 / study plan) as style anchors.
- Confirms all math, code, figure paths, and the title comment survived intact.

**Stage E — Human final review** → then build the PDF with the existing toolchain:
`python3 scripts/build_reports.py --step 07 --lang bg`.

Output filenames (parallel to EN): `report_bg.md`, `summary/summaryBg.md`,
`summary/onePagerBg.md`, `dataRequest/data_request_bg.md`.

---

## 5. Smoke test — Step 07 (pilot)

Run the full pipeline on step07's three EN files (report + summary + onePager, ~73K —
exercises every file type: prose report, structured summary, terse one-pager):

1. Create Azure F0 resource; put key/endpoint/region in `.env`.
2. Derive `glossary.tsv` from `terminology_EN_BG.md`; add the ~15 RL terms + morphology note.
3. Implement `translate_deliverable.py`; run on `reports/step07/report_en.md`.
4. **Manually diff** the generated `report_bg.md` against the EN source AND against a
   known-good human BG report (e.g. `step04/report_bg.md`) for register/terminology.
5. Run Claude post-edit (Stage D); human review; build BG PDF.
6. **Acceptance criteria:** structure byte-parity (same headings/tables/figures/math),
   glossary terms correct with first-mention parentheses, no English left in prose,
   PDF builds clean with Cyrillic (DejaVu fonts). Record failure modes and tune Stages
   A/B/D before scaling.

---

## 6. Scale-out

**Backlog (after pilot passes):** run the pipeline over step05, step06, step08 summaries,
step08 report + onePager, and `data_request_en.md`. (~259K remaining; well within one
month of Azure F0.) step06 summary is large (135K) — batch it.

**Steady state (steps 09–15 and beyond):** the target workflow —
1. Author the step's report/summary/onePager **in English only**.
2. `python3 scripts/translate_deliverable.py --step NN` → BG drafts.
3. **Human does final review only** (the explicit goal), then build PDFs.

This makes English the single authoring surface and reduces the human's job to review.

---

## 7. Files to create / modify

- **New:** `scripts/translate_deliverable.py` (the pipeline, Stages A–C + Azure calls).
- **New:** `glossary.tsv` (derived, machine-readable; committed) + `.env` (key, **git-ignored**).
- **Edit:** `deliverables/terminology_EN_BG.md` — add ~15 RL terms + a morphology note;
  mark it the single source of truth.
- **Generated (reviewed by human):** `report_bg.md` / `summaryBg.md` / `onePagerBg.md` /
  `data_request_bg.md` for steps 05–08 + dataRequest.
- **No change** to `build_reports.py` (it already builds `_bg` PDFs), the interactive
  viewer, or Tier-2 internal files.

## 8. Verification

- **Pipeline unit check:** round-trip a small file; assert the block skeleton (headings,
  table rows, figure paths, `$math$`) is byte-identical between EN and BG except prose.
- **Terminology check:** grep BG output for glossary source terms that should have become
  BG (e.g. no stray "Safe exploitation"); confirm abbreviations stayed Latin.
- **Build check:** `scripts/build_reports.py --step 07 --lang bg` produces a clean PDF
  with correct Cyrillic rendering.
- **Human review gate:** side-by-side EN/BG read of the pilot before declaring the
  workflow production-ready for the backlog.
