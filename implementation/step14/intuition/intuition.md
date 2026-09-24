# Chapter 14 — Intuition: how do you grade a player who changes?

## The problem in one paragraph

"My poker bot won 60 % of its games" sounds good until you ask *against whom*. Beating weak bots
is easy; the question is what the bot would do against the opponents it will actually meet, and
what the worst opponent could do to it. For a fixed bot there are two classic answers: its
**exploitability** (how much a perfect counter-strategy would take from it) and its **rating in a
population** (Elo and its successors). For a bot that *adapts* — that watches you and changes its
play — both answers break. Exploitability can only punish it for leaving the equilibrium, however
much it gains; population ratings reward it for beating weak bots without asking whether it can
be lured into a trap. With three or more players there is not even a single "worst opponent":
two opponents can gang up. This chapter builds an evaluation that asks four questions at once —
*how much does it gain, how fast, how badly can it be hurt, and how sure are we?* — and checks
where each older answer goes wrong.

## A mental picture

Think of hiring a negotiator. One reference asks "what is the worst deal a ruthless counterpart
could force on this person?" (exploitability). Another asks "how did this person do in the last
twenty negotiations?" (population rating). A good hire needs both — plus: *how quickly do they
read a new counterpart, how quickly do they notice when the counterpart changes tactics, and can
they be played by a counterpart who acts naive and then turns?* And if three parties sit at the
table, *what if the other two coordinate?* Neither reference alone answers these.

## The menu of approaches

| Approach | What it measures | When you would use it | Main weakness |
|---|---|---|---|
| Exploitability / NashConv | worst case against a best responder (two players); distance from an equilibrium (N players) | small games, exact; large games via a learned best response | punishes any deviation; a learned best response only gives a lower bound; no guarantee with 3+ players |
| Head-to-head win rate | average result against specific opponents | matches against a known field | card luck needs thousands of hands; depends entirely on the field |
| Variance reduction (duplicate, DIVAT, AIVAT) | same win rate, less noise | poker evaluation, especially with humans | AIVAT needs one strategy to be known; the value function must be fixed in advance |
| Elo / TrueSkill | a single skill number from wins and losses | transitive games, arenas | meaningless in cycles; inflated by adding weak copies |
| Nash averaging | performance against the maximum-entropy Nash mixture of the meta-game | redundant populations | gives zero weight to agents outside the equilibrium support |
| α-Rank | long-run share in an evolutionary process | many-player, general-sum populations | the ranking depends on the selection pressure α |
| Voting (VasE, maximal lotteries) | the lottery no other candidate beats by a majority | many tasks as voters | treats each agent as a fixed candidate |
| Population return + within-population exploitability (repeated RPS benchmark) | gain against a weak field and robustness in one score | one two-player game | "within-population" misses exploiters outside the field |

## How the field got here (short timeline)

- **1978 — Elo**: a single skill number for chess, assuming a total order.
- **2006 — DIVAT / optimal unbiased estimators**: poker evaluation starts subtracting luck.
- **2007–2015 — safe exploitation** (restricted Nash response, Ganzfried–Sandholm): the two-axis
  trade-off between gain and worst case becomes explicit.
- **2013 — ACPC's two winner rules**: total bankroll (exploit the field) vs instant-runoff (do
  not lose) — the two families disagree in practice.
- **2017–2018 — AIVAT**: variance reduction that also uses the known strategy of one agent;
  used to evaluate DeepStack and later Pluribus.
- **2018–2020 — Nash averaging, α-Rank, spinning tops**: rankings that handle cycles and
  redundancy; games are "transitive at the top, cyclic in the middle".
- **2019 — OpenSpiel's NashConv**: a common worst-case yardstick for N players, explicitly not a
  guarantee.
- **2022 — learned best responses (ISMCTS-BR)**: exploitability estimates for large games, as
  lower bounds.
- **2023 — VasE; the repeated-RPS benchmark**: voting theory for evaluation; the first protocol
  that scores return and robustness together, for one game.
- **2025–2026 — N-player ratings, LLM arenas, anytime-valid AIVAT, AIVAT pathologies**: more
  populations, more players — still fixed agents.

## Easy to get wrong

- **Exploitability is not a score of how good an agent is.** An agent can be far from
  equilibrium and win a lot; Nash can be unexploitable and win little.
- **NashConv = 0 is not safety with three players.** It says no single player wants to deviate;
  it says nothing about two players deviating together.
- **A learned best response that finds nothing proves nothing.** It is a lower bound; report its
  budget.
- **AIVAT estimates an expected payoff, not exploitability**, and needs a strategy you know.
- **An adaptive agent has no fixed entry in a meta-game.** Its payoff depends on how long the
  match is and what it has seen, so every ranking of it depends on the chosen horizon.
- **Adding copies of a weak bot changes Elo but not Nash averaging** — which is a feature for
  redundancy and a bug for crediting real exploitation.

## You should be able to answer

1. Why can exploitability only punish an exploiting agent? What second number does it need?
2. Why is there no "exploitability" with three players, and what could replace it?
3. What does AIVAT subtract from a hand's result, and why is the estimate still unbiased?
4. Why does Nash averaging give an exploiter zero weight while Elo puts it first?
5. What does α change in α-Rank, and why should you always sweep it?
6. Which four numbers would you report for an adaptive poker agent, and how would you get
   confidence intervals on each?

## Key takeaways for the final summary

- Worst case and population performance are two different questions; adaptive agents need both,
  plus speed, recovery and confidence — reported together, not collapsed into one number.
- With three or more players the worst case must include coalitions; NashConv does not.
- Every ranking method has a known way to mislead on adaptive or exploiting agents; the chapter
  tests each on real zoos rather than asserting it.
