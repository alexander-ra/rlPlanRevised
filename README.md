# RL PhD Study Plan

**Official PhD Title:**
- **EN:** Research on the possibilities for applying Artificial Intelligence in computer games
- **BG:** Изследване на възможностите за приложение на изкуствения интелект в компютърни игри

**Research Focus:**
Adaptive Strategy Learning in Multi-Agent Imperfect-Information Environments

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
├── .venv/                               # Project-wide Python virtual environment (not committed)
├── .vscode/settings.json               # VS Code interpreter + analysis config
├── requirements.txt                     # Loose dependency constraints (pip install -r)
├── requirements-lock.txt               # Pinned lockfile for exact reproduction
├── planArchitecture.md                  # Strategic core: 15-step plan, career alignment, methodology
├── deliverables/
│   ├── studyPlan/
│   │   ├── en/                          # English study plan (YAML metadata + 9 markdown sections)
│   │   └── bg/                          # Bulgarian translation
│   ├── reports/
│   │   ├── step01/                      # Step 1 report package (EN/BG report + EN/BG summary + figures)
│   │   └── step02/                      # Step 2 report package (EN/BG report + EN/BG summary + figures)
│   ├── summaries/
│   │   ├── step01_en.pdf                # Built summary PDF (Step 1, English)
│   │   ├── step01_bg.pdf                # Built summary PDF (Step 1, Bulgarian)
│   │   ├── step02_en.pdf                # Built summary PDF (Step 2, English)
│   │   └── step02_bg.pdf                # Built summary PDF (Step 2, Bulgarian)
│   └── terminology_EN_BG.md             # Translation dictionary
├── exports/
│   ├── studyPlanEN.pdf                  # Pre-built PDF (English)
│   └── studyPlanBG.pdf                  # Pre-built PDF (Bulgarian)
├── implementation/
│   └── step01/                          # Step 1: DQN + PPO from scratch
│       ├── config.py                    # All hyperparameters in one place (edit here to experiment)
│       ├── benchmark.py                 # Trains SB3 baselines and compares against custom implementations
│       ├── compare_sb3.py               # Loads sb3_results_cache.json and generates comparison plots
│       ├── verify_setup.py              # Smoke-test: confirms gym, torch, tensorboard all work
│       ├── sb3_results_cache.json       # Cached SB3 training curves (avoid re-running SB3 for plots)
│       ├── dqn/
│       │   ├── replay_buffer.py         # Circular buffer — push() and sample() for experience replay
│       │   ├── q_network.py             # MLP: obs → hidden layers → Q-values per action
│       │   ├── agent.py                 # Full DQN algorithm: ε-greedy, TD update, target network sync
│       │   └── train.py                 # CartPole-v1 training loop; logs to logs/dqn/
│       ├── ppo/
│       │   ├── networks.py              # PolicyNetwork (actor, Categorical) + ValueNetwork (critic)
│       │   ├── gae.py                   # Generalized Advantage Estimation — reverse-sweep with done mask
│       │   ├── agent.py                 # Full PPO algorithm: rollout, clipped surrogate loss, update epochs
│       │   └── train.py                 # LunarLander-v3 training loop; logs to logs/ppo/
│       ├── utils/
│       │   ├── env_wrappers.py          # Gymnasium wrappers and reward normalisation helpers
│       │   ├── logger.py                # Thin TensorBoard SummaryWriter wrapper
│       │   └── plotting.py              # Learning curve and comparison chart generators
│       ├── models/                      # Saved checkpoints (.pt) and SB3 zips
│       │   ├── dqn_cartpole.pt          # Final DQN weights (CartPole-v1)
│       │   ├── dqn_cartpole_best.pt     # Best-performing DQN checkpoint during training
│       │   ├── dqn_cartpole.zip         # SB3-format DQN model (for SB3 evaluation)
│       │   ├── ppo_lunarlander.pt       # Final PPO weights (LunarLander-v3)
│       │   └── ppo_lunarlander_best.pt  # Best-performing PPO checkpoint during training
│       └── logs/                        # TensorBoard event files (gitignored; generated at runtime)
│           ├── dqn/
│           └── ppo/
│   └── step02/                          # Step 2: Vanilla CFR on Kuhn Poker
│       ├── config.py                    # CFR training configuration
│       ├── compare_openspiel.py         # Cross-check vs OpenSpiel and analytical Nash strategy
│       ├── verify_setup.py              # Dependency and environment verification
│       ├── cfr/
│       │   ├── kuhn_poker.py            # Kuhn Poker game logic and terminal utilities
│       │   ├── info_set_node.py         # Regret-matching node for one information set
│       │   ├── cfr_trainer.py           # Recursive CFR traversal + training loop
│       │   └── train.py                 # Training entrypoint
│       ├── evaluate/
│       │   ├── best_response.py         # Best-response computation against fixed strategy
│       │   ├── exploitability.py        # Exploitability metrics and evaluation helpers
│       │   └── convergence.py           # Convergence diagnostics and data export
│       ├── figures/                     # Generated convergence/strategy figures
│       ├── models/                      # Saved strategy snapshots
│       └── logs/                        # JSON logs from CFR training/evaluation
├── planning/
│   ├── rawSteps/                        # 15 executable learning steps (full 5-phase cycle each)
│   ├── cleanSteps/                      # Supervisor-facing versions (formal references only)
│   ├── discussions/                     # Change proposals, debate trail
│   └── email_instructions.md            # Email guidelines for supervisor communication
├── interactiveStudy/                    # Standalone HTML5 viewer for rawSteps
│   ├── src/                             # Source: shell.html, styles.css, app.js
│   ├── build.py                         # Build script → dist/index.html
│   └── dist/                            # Built output (~638 KB single file)
└── oldSources/                          # Prior drafts (reference only)
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

---

## Python Environment Setup

A single project-wide virtual environment (`.venv/` at the repo root) is used for all implementation steps.

### Prerequisites

- Python 3.10+
- `git`

### First-time setup

```bash
git clone <repo-url>
cd rlPlanRevised

# Create the virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# Install from the pinned lockfile (exact reproducible versions)
pip install -r requirements-lock.txt

# OR install from loose requirements (latest compatible versions)
# pip install -r requirements.txt

# Verify everything works
python implementation/step01/verify_setup.py
```

> **box2d (LunarLander):** `box2d-py` builds from source and requires SWIG.
> If it fails, install SWIG first: `pip install swig`, then retry.

> **PyTorch CPU vs CUDA:** The lockfile pins CPU-only PyTorch (`torch==2.11.0+cpu`).
> For GPU training, install the appropriate CUDA wheel from https://pytorch.org/get-started/locally/ instead.

### VS Code IDE configuration

The workspace ships a `.vscode/settings.json` that points the Python interpreter at `.venv/bin/python` and adds the implementation paths to Pylance's analysis. After opening the workspace, VS Code should pick it up automatically.

If you still see import-error squiggles:

1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Choose the entry that shows `.venv/bin/python` at the project root.
   If it is not listed, click **Enter interpreter path…** and paste: `./.venv/bin/python`
3. `Ctrl+Shift+P` → **Developer: Reload Window**

### Running scripts

```bash
# Activate the venv (if not already active)
source .venv/bin/activate

# Run any implementation step script
cd implementation/step01
python dqn/train.py
python ppo/train.py
python benchmark.py
```

Inside VS Code: open any `.py` file and press `F5` → choose **Python File**. The selected interpreter is used automatically.

**TensorBoard:** install the VS Code extension `ms-toolsai.tensorboard`, then `Ctrl+Shift+P` → **Python: Launch TensorBoard** → point to `implementation/step01/logs/`.
