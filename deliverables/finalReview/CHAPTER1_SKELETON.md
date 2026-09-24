# Chapter I — skeleton and budgets

**Official frame** (individual plan, stage 1, due 11.2026): *Analysis of the state of the
problem. Formulation of relevance, goal, tasks, and thesis.* 25–30 standard pages of 1800
characters → **45–54k Bulgarian characters**. BG runs ~1.12× EN in characters, so the
English draft targets **~6.5–7.5k words** (1 standard page ≈ 250 EN words). References,
figure captions and tables are outside the budget.

The individual plan fixes the problem statement Chapter I must answer or visibly refine:
state-of-the-art poker AIs (Libratus, DeepStack, Pluribus) play near-GTO strategies, rarely
adapt to a specific opponent and are not designed for fraud/collusion detection; scripted
bots, simplified CFR agents and basic RL cover separate aspects but are static or easy to
exploit. **Goal:** an adaptive agent that starts from a safe strategy and improves its
outcome against sub-optimal opponents. **Tasks** (verbatim order): research existing
adaptive-AI solutions; design an agent that adapts to different players and detects fraud
attempts; select methods/tools and build a simulation environment with an agent interface;
create a variety of opponents; develop the adaptive agent; train it against different
opponents; implement and test the system.

The three contributions: **C1** Behavioral Adaptation Framework (real-time opponent
inference) · **C2** Multi-Agent Safe Exploitation (small N-player games; no general N-player
safety theorem is claimed) · **C3** Evaluation Methodology (domain-agnostic adaptability
and robustness measurement; framed as "existing evaluation breaks here, ours catches it").

## Sections

| § | Title (EN / BG) | Pages | ≈ EN words | Fed by | Ends with |
|---|---|---:|---:|---|---|
| 1.1 | Introduction: relevance and problem statement / Въведение: актуалност и постановка на проблема | 2 | 500 | plan, 06, 07, 11 | why adaptation + fair play matter; scope (imperfect-information multi-agent games as testbed) |
| 1.2 | Theoretical foundations: RL, game theory, CFR / Теоретични основи | 4 | 1000 | 01, 02, 03, 04 | equilibrium is computable at scale via sampling + abstraction |
| 1.3 | Neural methods and landmark systems / Невронни методи и системи от най-високо ниво | 3.5 | 875 | 05, 06 | every landmark system plays a fixed approximate equilibrium — nobody adapts |
| 1.4 | Opponent modeling and behavioral adaptation / Моделиране на противника и поведенческа адаптация | 4.5 | 1125 | 07, 12, (09 LOLA) | gap for C1: no unified detect → adapt → evaluate loop |
| 1.5 | Safe exploitation and the multi-agent extension / Безопасна експлоатация и многоагентно разширение | 5.5 | 1375 | 08, 09, 10, 11 | gap for C2: safety theory stops at two players; coalitions/collusion break it |
| 1.6 | Evaluating agents in multi-agent games / Оценяване на агенти в многоагентни игри | 3.5 | 875 | 02, 03, 08, 10, 11 + literature (AIVAT, α-Rank, Nash averaging, VasE) | gap for C3: no cross-game framework for adaptability/robustness |
| 1.7 | Conclusions: goal, tasks and thesis / Изводи, цел, задачи и теза | 3 | 750 | all | RQ1–RQ3, goal, tasks (mapped to the plan's tasks), thesis statement, route through Chapters II–IV |
| | **Total** | **26** | **~6500** | | 1–3 figures, leaving headroom to 30 |

## Per-chapter digest caps (raw material for the extract files)

Caps are for the *digest* in each `stepNN_extract.md` — deliberately above each chapter's
share, since drafting will cut further.

| Step | Feeds | Digest cap (EN words) |
|---|---|---:|
| 01 | 1.2 | 300 |
| 02 | 1.2, 1.6 | 350 |
| 03 | 1.2, 1.6 | 300 |
| 04 | 1.2 | 350 |
| 05 | 1.3 | 500 |
| 06 | 1.3, 1.1 | 700 |
| 07 | 1.4, 1.1 | 600 |
| 08 | 1.5, 1.6 | 650 |
| 09 | 1.5, 1.4 | 400 |
| 10 | 1.5, 1.6 | 400 |
| 11 | 1.5, 1.6, 1.1 | 450 |
| 12 | 1.4 | 400 |

## Voice

Chapter I is a state-of-the-art analysis, not a learning diary. Literature is presented in
a neutral scholarly voice; the candidate's own experiments appear only as brief supporting
evidence for a gap ("a replication on Leduc shows …"), never as the narrative spine.

## Citation style

Numbered, in order of first citation, square brackets: `[12]`, `[3, 7]`. Bibliography
entries IEEE-like: authors, title, venue, year, DOI/arXiv id. Provisional — to be adjusted
to the department's rules after the supervisors see the draft.
