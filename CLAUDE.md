# CLAUDE.md — Project Instructions for Claude

## Project Overview

PhD research hub for Alexander Andreev's doctoral program at Ruse University "Angel Kanchev".  
**Topic:** "Research on the possibilities for applying AI in computer games"  
**Focus:** Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments  
**Phase 1 deadline:** November 2026 | **Defense:** April 2029

The repo started as a step-by-step learning booklet and evolved into a full PhD workspace covering planning, implementation, reports, summaries, an interactive viewer, and build tooling.

## Current Progress

- **Steps 1–2 completed** (RL basics + Game Theory/CFR)
- **Steps 3–15 planned** (April–October 2026)
- Step 1: DQN + PPO from scratch (CartPole, LunarLander)
- Step 2: Vanilla CFR on Kuhn Poker + OpenSpiel comparison
- Bilingual reports and summaries exist for steps 1–2 (EN + BG)

## Repository Layout

```
PLAN.md                          # Master roadmap: 15-step plan, career alignment, methodology
planning/
  rawSteps/                      # Full learning versions (videos, blogs, AI tags)
  cleanSteps/                    # Formal supervisor-facing versions
  discussions/                   # Change proposals, debate trail
  email_instructions.md          # Supervisor communication guidelines
implementation/
  step01/                        # DQN + PPO (Python/PyTorch)
  step02/                        # Vanilla CFR on Kuhn Poker
deliverables/
  studyPlan/{en,bg}/             # Study plan markdown sources + built PDFs
  reports/step{01,02}/           # Step reports (EN/BG markdown + built PDFs + figures)
  summaries/                     # Built summary PDFs
  terminology_EN_BG.md           # Translation dictionary
interactiveStudy/                # HTML5 viewer for rawSteps (build.py → dist/)
scripts/                         # Build scripts (build_pdf.py, build_reports.py, etc.)
docs/                            # GitHub Pages deployment output
oldSources/                      # Prior drafts (reference only)
```

## Build Commands

```bash
# Activate venv first
source .venv/bin/activate

# Study plan PDFs
python3 scripts/build_pdf.py               # both languages
python3 scripts/build_pdf.py --lang en     # English only

# Step report + summary PDFs
python3 scripts/build_reports.py                        # all steps
python3 scripts/build_reports.py --step step01          # one step
python3 scripts/build_reports.py --type summary         # summaries only

# Interactive study viewer
cd interactiveStudy && python3 build.py    # → dist/index.html

# Run implementation code
cd implementation/step01 && python dqn/train.py
cd implementation/step02 && python cfr/train.py
```

## Key Conventions

- **Bilingual:** All deliverables exist in English and Bulgarian
- **PDF toolchain:** Pandoc + Tectonic (XeTeX). BG builds use DejaVu fonts for Cyrillic
- **Python:** 3.10+, single `.venv/` at repo root, PyTorch CPU-only by default
- **Step naming:** `step01`, `step02`, etc. (zero-padded two digits)
- **Learning cycle:** Each step follows 5 phases: Intuition → Exploration → Targeted Reading → Implementation → Consolidation
- **Code ownership tags:** 🔴 HAND-CODE / 🟡 AI-ASSISTED / 🟢 AI-GENERATED (see PLAN.md §4.4)
- **Reports:** Each step produces 4 PDFs: report EN, report BG, summary EN, summary BG
- **Figures:** Stored in `deliverables/reports/stepXX/figures/` and copied into `summary/` subdirs

## When Editing Steps

- rawSteps are the source of truth; cleanSteps are derived from them
- Never add YouTube links, blog posts, or AI tags to cleanSteps (supervisor-facing)
- Always include the surgical reading protocol (READ/SKIM/SKIP/MATH) in rawSteps
- Implementation components must be tagged 🔴/🟡/🟢 with justification

## When Building Reports

- Image paths in markdown are relative to the `.md` file's directory
- BG PDFs require: `--pdf-engine=tectonic -V mainfont="DejaVu Serif" -V sansfont="DejaVu Sans"`
- Summary PDFs go to `deliverables/summaries/stepXX_{en,bg}.pdf`
- Report PDFs go to `deliverables/reports/stepXX/stepXX_report_{en,bg}.pdf`

## Thesis Contributions (Target)

1. **Behavioral Adaptation Framework** — real-time opponent strategy inference
2. **Multi-Agent Safe Exploitation** — KL-regularized exploitation with safety guarantees (small N-player games)
3. **Evaluation Methodology** — domain-agnostic framework for measuring adaptability and robustness
