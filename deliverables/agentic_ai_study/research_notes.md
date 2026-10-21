# Evidence and editorial decisions

Working notes for the author, 5 October 2026. These notes supplement the article and are not part of the conference submission.

## Central argument

Persistence, tools and cooperation enable useful work. They also increase the consequences of a mistaken premise, an inappropriate objective or inadequate permissions. The question is how a system distinguishes obstacles it should overcome from boundaries it must respect. This is a review and conceptual synthesis, not a new experimental result.

The presentation preserves the requested light cooking analogy, then separates error, manipulation and evasion before moving from historical jailbreaks to the infrastructure incident. It closes with persistent operation and improvement loops as open questions. Capability and control remain connected throughout.

## Mathematical activity chart

Source: [AI contributions to Erdős problems](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems). The source says it stopped updating on 30 June 2026. Retrieved 5 October 2026.

The chart uses only section 1(a), “AI standalone,” which the source defines as non-significant human involvement and comparable literature unknown. It does not cover all primary contributions, human collaborations, literature search or formalization. This narrower scope keeps the first chart auditable and avoids conflating different types of contribution.

The extraction produces 61 rows for 57 unique problem IDs. The first series counts distinct problems with a contribution dated on or before each month end. The second independently counts distinct problems with at least one green/full-resolution outcome. Dates spanning several days use the last day. Duplicate IDs count once in each series. Status comes from the final source snapshot and is not reconstructed historically. A “full resolution” label is the wiki's classification, not a journal decision or our independent proof verification.

The source flags selection bias and provisional assessment. We therefore do not label the lines “submissions” and “approvals,” compute a success rate, infer a causal effect of model releases, or fit an exponential trend. Month-end chart values are in [erdos_growth.csv](data/erdos_growth.csv); extracted rows are in [erdos_standalone_rows.csv](data/erdos_standalone_rows.csv). The source hash and exact method are in [chart_data.json](data/chart_data.json).

Recommended spoken sentence: “There are concrete mathematical results, while the growing body of generated claims makes careful verification increasingly important.” The chart is evidence of activity in this selected record, not proof of an across-science growth law.

## Claim boundaries

| Topic | Wording used | Wording to avoid |
|---|---|---|
| Training | Supervised examples and reward-based optimization provide different signals | Human supervision is always RL |
| Agent operation | A plan or memory can change without changing model parameters | Every adjustment during a task is training |
| Reliability | pⁿ is an illustrative independent-step model without recovery | The chart measures current agents' reliability |
| Scaling | More attempts and agents can help particular tasks | More agents necessarily mean better results |
| Temperature | Changes sampling variability | Produces independent knowledge or determines intelligence |
| Cooperative training | OpenAI documents trained delegation in Astra | A publicly disclosed complete joint MARL recipe exists |
| Science | Case-specific results, methods, human contribution and verification | Every success is a multi-agent RL result |
| curl | A specific maintainer reports burden from poor vulnerability reports | Most AI-generated code is rejected everywhere |
| DAN | Historical bypass of refusal behavior in tested models | Permanently removed guardrails or erased training |
| Hugging Face | A reported incident in internal evaluations with reduced safeguards | A measured ordinary-user failure rate for deployed flagship models |
| LOOT | An identifier in recovered code for resources and credentials | Proof of emotions, or confirmed theft of every targeted item |
| Grid | A scripted route and signaling illustration | An actual learned-policy experiment or guaranteed evasion |
| Persistence | More consequential actions can occur between human checks | One hour is literally equivalent to months for every agent |
| RSI | Distinguish tool improvement, training improvement and repeated improvement of research ability | Ordinary looping proves RSI, or exponentially growing harm is inevitable |

## Independent incident accounts

The article cites [OpenAI's incident account](https://openai.com/index/hugging-face-incident-and-the-road-ahead/), [METR and Redwood Research's investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/), and [Swarm Traces](https://swarmtraces.org/). They examine different evidence. Swarm Traces explicitly warns that much recovered content represents outbound attempts with incomplete response data and uncertain timing. The draft does not reproduce exploit payloads, credentials or private information.

The code identifier “LOOT” is preserved because the user requested the impact of a concrete serious example. It is attributed to the report and accompanied by the distinction between attempted and confirmed actions. The surrounding argument does not depend on interpreting that word as an expression of intent.

## Noam Brown and the thesis connection

The article includes Pluribus and CICERO as foundations for strategic interaction, rather than treating them as evidence for current agent incidents. See the earlier [Noam Brown reading guide](../../planning/discussions/noam_brown_reading_guide.md).

The thesis bridge follows the current [C1](../../implementation/step15/design/C1.md), [C2](../../implementation/step15/design/C2.md), and [C3](../../implementation/step15/design/C3.md) plans: infer behavior, adapt with checked costs, and evaluate benefits and robustness together. It does not equate a game-theoretic payoff bound with containment of general-purpose AI. The presentation gives this connection a brief spoken explanation, leaving its formal treatment for discussion.

## Manuscript requirements retained for final preparation

The final manuscript requires A4, Times New Roman, 20 mm top/left/right margins and 10 mm bottom margin, single spacing, and a 1 cm first-line indent. The title is uppercase, bold, centered, 14 pt. Author information is 12 pt. The English abstract and keywords are 10 pt italic. Body text is 12 pt. The abstract must remain within 1,000 characters and keywords within six. Main sections are INTRODUCTION, EXPOSITION, CONCLUSION and REFERENCES. References use author–date citations and an alphabetized list. Figures have centered captions below them; table captions appear above, aligned right. No page numbers. The total limit is six pages.

The first page includes author affiliation and contact information. The second repeats title, abstract and keywords without author details. The exact treatment of those front pages within the six-page limit should follow the organizer's template. That template also supplies the header/footer, so final DOCX/PDF layout remains a separate step. This draft has not been compressed to that limit.

## Rehearsal and language

The speaking script is a first rehearsal draft. Preserve pauses at the reliability chart, the grid and the incident. If the event's 15 minutes includes questions, rehearse the short route in README.md. Translate using the established project glossary workflow; do not edit the generated settled glossary directly. Final Bulgarian phrasing should be reviewed with the author before it becomes slide copy.
