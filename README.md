# RL PhD Study Plan

**Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments**

| | |
|---|---|
| **Author** | Alexander Andreev |
| **Institution** | Ruse University "Angel Kanchev" |
| **Program** | PhD in Informatics (4.6) |
| **Supervisors** | Prof. Dr. Tsvetomir Vasilev, Assoc. Prof. Dr. Rumen Rusev |
| **Enrollment** | 18.02.2026 |
| **Phase 1 Deadline** | November 2026 |

## Overview

This repository contains the complete planning materials for the first phase of a PhD research program on adaptive strategy learning in multi-agent imperfect-information games. The research targets three contributions:

1. **Behavioral Adaptation Framework** — real-time opponent strategy inference
2. **Multi-Agent Safe Exploitation** — KL-regularized exploitation with safety guarantees for small N-player games
3. **Evaluation Methodology** — domain-agnostic framework for measuring adaptability and robustness

The study plan spans 15 learning steps organized into 7 thematic phases (A–G), covering ~28 weeks (April–October 2026) with a built-in buffer before the November deadline. Testbeds: Kuhn Poker (12 states) and Leduc Hold'em (~936 info sets) for exact algorithm verification.

## Repository Structure

```
.
├── planArchitecture.md              # Strategic core: 15-step plan, career alignment, methodology
├── deliverables/
│   ├── studyPlan/
│   │   ├── en/                      # English study plan (YAML metadata + 9 markdown sections)
│   │   └── bg/                      # Bulgarian translation
│   └── terminology_EN_BG.md         # Translation dictionary
├── exports/
│   ├── studyPlanEN.pdf              # Pre-built PDF (English)
│   └── studyPlanBG.pdf              # Pre-built PDF (Bulgarian)
├── planning/
│   ├── rawSteps/                    # 15 executable learning steps (full 5-phase cycle each)
│   ├── cleanSteps/                  # Supervisor-facing versions (formal references only)
│   ├── discussions/                 # Change proposals, debate trail
│   └── email_instructions.md        # Email guidelines for supervisor communication
├── interactiveStudy/                # Standalone HTML5 viewer for rawSteps
│   ├── src/                         # Source: shell.html, styles.css, app.js
│   ├── build.py                     # Build script → dist/index.html
│   └── dist/                        # Built output (~638 KB single file)
└── oldSources/                      # Prior drafts (reference only)
```

## Study Plan Phases

| Phase | Steps | Topic | Duration |
|-------|-------|-------|----------|
| **A** Foundations | 1–2 | RL basics, game theory, CFR | 4 weeks |
| **B** Scaling the Toolbox | 3–4 | CFR variants, MC methods, game abstraction | 3 weeks |
| **C** Neural Methods | 5–6 | Neural equilibrium, end-to-end game AI | 4.5 weeks |
| **D** Opponent Exploitation | 7–8 | Opponent modeling, safe exploitation | 6 weeks |
| **E** Multi-Agent Dynamics | 9–11 | MARL, population training, coalition formation | 6 weeks |
| **F** Data-Driven | 12–13 | Sequence models, LLM agents, behavioral analysis | 3.5 weeks |
| **G** Integration | 14–15 | Evaluation frameworks, research frontier mapping | 3.5 weeks |

Each step follows a 5-phase learning cycle: **Intuition → Exploration → Targeted Reading → Implementation → Consolidation**.

## Interactive Viewer

A mobile-friendly HTML viewer for browsing the 15 raw steps. Build and open:

```bash
cd interactiveStudy
python3 build.py
# open dist/index.html in browser (works via file://)
```

Features: sidebar navigation, day-level timeline bar, section jump, YouTube thumbnails, checkbox persistence, schedule delay control.

## PDF Export

Requires [Pandoc](https://pandoc.org/) and [Tectonic](https://tectonic-typesetting.github.io/):

```bash
# English
pandoc deliverables/studyPlan/en/00_metadata.yaml \
  deliverables/studyPlan/en/[0-9]*.md \
  --toc --toc-depth=2 --pdf-engine=tectonic \
  -V geometry:margin=2cm -V fontsize=11pt \
  -o exports/studyPlanEN.pdf

# Bulgarian
pandoc deliverables/studyPlan/bg/00_metadata.yaml \
  deliverables/studyPlan/bg/[0-9]*.md \
  --toc --toc-depth=2 --pdf-engine=tectonic \
  -V geometry:margin=2cm -V fontsize=11pt \
  -o exports/studyPlanBG.pdf
```
