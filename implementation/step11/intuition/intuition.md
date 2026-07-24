# Step 11 — Intuition: Dynamic Coalition Formation in Free-For-All Games

> Phase 1 of Step 11. Mental model only — no proofs, no code. Built on the raw step's intuition
> phase ([`step_11_coalition_formation_ffa.md`](../../../planning/rawSteps/step_11_coalition_formation_ffa.md), L44-77).

---

## 1. The core idea, in one paragraph

In every previous step you played **2-player** games, where there is nothing to negotiate: you
either cooperate or you don't, and "the opponent" is a single thing to model or exploit. **The
moment a third player joins, something new appears: alliances.** Two players can gang up on a
third — sharing information, coordinating moves, one sacrificing to let the other win — and then
one of them can *betray* the other the instant it pays off. This cycle — **form a coalition,
exploit it, dissolve it, form a new one** — is the heart of every free-for-all (FFA) game (poker
with 6 players, Diplomacy with 7, a 4-player board game) and is *essentially unstudied* in the
RL/game-AI literature. Classical game theory splits into two halves that each answer only part of
it: **non-cooperative** theory (Nash) tells each *individual* what to do but treats players as
islands and cannot talk about "who allies with whom"; **cooperative** theory (Shapley value, the
core) is *about* coalitions — who should join, how to split the winnings, when a group is stable —
but it assumes the coalitions are **fixed in advance**. The real, open problem is the **dynamic**
case: coalitions that form, shift, and shatter *during* play. No classical solution concept
handles it, which is exactly why it is a PhD frontier.

---

## 2. A picture to hold in your head

**A dinner party where only one guest can stay.** Four people are at a table; by the end of the
night three must leave and one "wins" the house. Nobody can win alone, so people pair up —
"let's push out Dana first" — passing each other the good seats, covering for each other. But the
pact is inherently unstable: the moment it's down to you and your ally, your ally *is* the last
obstacle, so the smart move is to have betrayed them one turn earlier. Everyone knows this,
everyone is watching for it, and the whole game is a running estimate of *who is currently with
whom* and *when the knife comes out.*

**So Long Sucker (SLS)** is that dinner party turned into a board game — and it was **designed on
purpose** (1950, by John Nash, Lloyd Shapley, Martin Shubik & Melvin Hausner — two of them future
Nobel laureates) to study exactly this tension. Four players, colored chips, and the only way to
win is to be the **last one standing** while the other three are eliminated. Crucially, you can
place *another player's* chip — which literally helps them — so **the entire alliance is encoded
in who plays whose chips.** Placing your ally's chip is a handshake; refusing to, or capturing
their pile, is the betrayal. There is no separate "negotiation phase" — the coalition dynamics
*are* the moves.

**The poker version (your thesis domain).** In 6-player poker, two colluding players might soft-
play each other (never raise into one another) or chip-dump (deliberately lose a pot to a partner).
That is a coalition, expressed purely through betting actions — and detecting it is the same
inference problem as reading SLS chip placements.

---

## 3. Why the third player breaks everything (precisely)

Three concrete things change when you go from N=2 to N≥3:

1. **Nash stops being useful.** In 2-player zero-sum games Nash is *the* answer: unexploitable,
   unique in value, computable. In an N-player FFA game Nash is (a) **computationally intractable**
   (PPAD-hard in general) and (b) **strategically empty** — it tells each player to guard against
   the *worst case* over all others, which ignores that the others might *coordinate against you*.
   Bakhtin et al. note the Nash strategy in Diplomacy is essentially "do nothing" — a useless
   baseline. So the "safe strategy" you spent Steps 2–8 building on **has no good analog here.**
2. **"Best response" loses meaning, so exploitability dies.** Exploitability (Steps 3–10) measures
   how much a best-responding *opponent* could beat you. Against *three* players who might ally,
   there is no single best response to compute a gap against. This is why Step 11's evaluation is
   **empirical** (win-rates, coalition scores, an EGTA meta-game), not an exploitability number.
3. **The reward is sparse and shared-fate.** Only 1 of 4 players wins. If you only reward the
   winner (+1) and punish the rest, an agent gets almost no signal about *which of its mid-game
   moves helped which ally.* The fix is **credit assignment**: decompose the outcome into
   per-player contributions so each move carries a learning signal. The tool for that is the
   **Shapley value.**

---

## 4. The two toolkits, compared

Cooperative game theory gives a menu of **solution concepts** — different answers to "how should a
coalition's value be split, and which coalitions are stable?" You should know what each one is for.

| Concept | Question it answers | One-line definition | Main weakness |
|---|---|---|---|
| **Nash equilibrium** (non-coop) | What does each *individual* do? | No player can gain by unilaterally deviating. | Says nothing about coalitions; intractable / meaningless for large-N FFA. |
| **Shapley value** | What is each player's *fair* share? | Average marginal contribution over all join orders. | Assumes the *grand* coalition forms; is about fairness, not stability. |
| **The core** | Is an allocation *stable*? | No sub-coalition can profitably break away. | **Can be empty** — then *no* allocation is stable (true of purely competitive games like SLS). |
| **Nucleolus** | The "most stable" allocation when the core is awkward. | Lexicographically minimize the worst coalition's dissatisfaction. | Always exists but is harder to compute and to interpret. |
| **Coalition-structure generation** | Which *partition* of players into coalitions is best? | Search over all partitions (Bell-number many). | Super-exponential search space; assumes coalitions are *static*. |

Two deeper axes matter for this step:

- **Static vs dynamic coalitions.** All of the above are **static**: the coalition (or partition)
  is decided and then the value is divided. SLS is **dynamic** — the coalition structure changes
  *every turn*. Classical theory barely touches this; it is the thesis gap.
- **Shapley-credit MARL vs piKL behavioral prior** — the two ways this step turns cooperative
  theory into a *learning* signal and a *safety* baseline:
  - **Shapley-credit (Wang et al. 2020, "Shapley Q-value"):** decompose the team's value into each
    agent's average marginal contribution and use *that* as its reward. Turns sparse winner-take-
    all into a dense, per-move signal → the agent learns *who it is really helping.*
  - **piKL (Bakhtin et al. 2022):** since Nash can't be the safety anchor, regularize the policy
    toward a **behavioral prior** (how humans play) — deviate only when it provably pays. This is
    the N-player replacement for "stay near Nash," and the seed of the thesis's Contribution #2.

---

## 5. Development over time (a dated lineage)

| Year | Milestone | What it fixed / added |
|---|---|---|
| **1950** | **So Long Sucker** invented (Nash, Shapley, Shubik, Hausner) | A minimal game *engineered* to force coalition formation & betrayal — the perfect FFA testbed. |
| **1953** | **Shapley value** (Shapley) | A principled, axiomatic *fair* division of coalition gains — "average marginal contribution". |
| **1950s–60s** | **The core** (Gillies), **nucleolus** (Schmeidler 1969) | Shift focus from fairness to **stability**: which allocations can't be broken by a defecting subgroup? |
| **2011** | Chalkiadakis, Elkind & Wooldridge — *Computational* cooperative GT | Makes the classical concepts **algorithmic**; coalition-structure generation over 2^N / Bell-number spaces. |
| **2020** | **Shapley Q-value** (Wang et al., AAAI) | Brings Shapley into **MARL** as a *credit-assignment* mechanism (global reward → local rewards). |
| **2022** | **piKL / no-press Diplomacy** (Bakhtin et al.); **CICERO** (Meta, Science) | Human-level N-player play by **replacing the Nash baseline with a behavioral prior**; CICERO adds language-based negotiation. |
| **2024** | **First RL papers on SLS** (Sharan & Adak; De Carufel & Jerade endgame analysis) | The very first learning agents on SLS — basic DQN, **no coalition mechanism** — plus an exact 2-player endgame solution. The gap this step fills. |

The tell that this is frontier work: a game invented by Nobel laureates in **1950** did not get its
**first RL treatment until 2024** — and even that used vanilla DQN with no notion of coalitions.

---

## 6. Common misconceptions / easy to get wrong

- **"Shapley value tells you how to split the pot in SLS."** No. SLS is purely competitive — only
  one player wins, so there is no shared pot to divide and the *grand coalition makes no sense*. We
  borrow Shapley only as a **credit-assignment** signal ("how much did this move help each player?"),
  **not** as a payoff-division rule. (Raw Confusions L596.)
- **"A coalition means the players agreed to cooperate."** In SLS there is no communication channel
  — a coalition is *implicit*, inferred only from behavior (whose chips you play). And a player may
  play another's chip for a purely selfish, non-alliance reason, so detection is **noisy**
  (genuine alliance vs strategic manipulation is an open problem — raw Confusions L597).
- **"The core is the stable answer."** For a zero-sum, 1-winner game the core is almost certainly
  **empty** — meaning *every* arrangement can be broken by some subgroup. Coalitions in SLS are
  therefore *inherently unstable*; they *will* be betrayed. Emptiness of the core is not a failure
  of the analysis, it is the finding. (Math Flag L325-326.)
- **"Nash is the safe fallback, as in poker."** In 4-player FFA, Nash is both intractable and
  strategically weak; the safe baseline shifts to a **behavioral / population prior** (piKL). This
  is the single most important conceptual shift of Phase E. (Math Flag L328-329.)
- **"Exploitability just extends to 4 players."** There is no single best response to compute a gap
  against a *coalition*; standard exploitability does not generalize. Evaluation must be empirical /
  EGTA-based.
- **"Beating the last opponent means you improved."** FFA coalition dynamics are **non-transitive**
  (rock-paper-scissors between coalition *pairings*: {A,B} beats {C,D}, but {B,C} beats {A,D}, ...),
  so — as in Step 10 — self-play can cycle. The spinning-top ratio makes this precise (predict a
  large cyclic component for SLS).

---

## 7. "You should be able to answer …" (self-check)

Reuse of the raw step's exit-checklist "explain from memory" items (L608-611) plus a few extras:

1. State the **Shapley value formula** and say what "each player's fair share" means — then say why
   in SLS we use it for *credit*, not for *payoff division*.
2. Define the **core** of a cooperative game and explain **why SLS almost certainly has an empty
   core** (hint: zero-sum, one winner).
3. Explain **why Nash equilibrium fails as a safety baseline** in N-player FFA (two reasons:
   intractable *and* strategically empty).
4. Explain **piKL** in one sentence and why a **behavioral prior** replaces Nash in N-player
   settings.
5. Describe how a coalition is **encoded** in SLS moves, and how the coalition detector infers it
   (help vs harm) — and why that is the *same inference* as Step 07's opponent model, on a different
   observation space.
6. Predict what the **spinning-top** decomposition will say about the SLS meta-game, and why.
7. Explain why SLS evaluation cannot use **exploitability** and what replaces it (win-rate,
   coalition score, EGTA meta-game).

---

## Key takeaways for the final summary

- **The N=2 → N≥3 jump is qualitative, not quantitative:** alliances appear, Nash becomes
  intractable *and* meaningless, and exploitability loses its definition. This reframes all three
  thesis contributions (adaptation → *social-structure* adaptation; safety → *behavioral* baseline;
  evaluation → *EGTA/coalition* metrics).
- **SLS is the ideal testbed:** small enough (4 players, finite) to analyze, rich enough to force
  real coalition dynamics, with an **exact 2-player endgame** for correctness — and *invented by
  Nash & Shapley to study this very tension.*
- **Cooperative GT supplies the tools but not the answer:** Shapley (fairness/credit), core
  (stability — *empty* for SLS ⇒ coalitions are inherently unstable), nucleolus, coalition-structure
  generation — all **static**; the **dynamic** case is the open gap.
- **Two concrete mechanisms carry into the build:** Shapley-value **credit assignment** (dense
  learning signal for a sparse 1-winner reward) and the **piKL** insight (behavioral prior as the
  N-player safety baseline = the crux of Contribution #2).
- **Expect non-transitivity:** SLS coalition pairings should be strongly cyclic (rock-paper-scissors
  over alliances), so self-play cycles and population/diversity methods (Step 10) matter — a
  prediction the spinning-top ratio will settle on a real run.
