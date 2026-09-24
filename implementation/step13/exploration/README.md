# Step 13 — Exploration

One script, to look at real hand histories before any modelling.

| Script | What it does | Runtime |
|---|---|---|
| `explore_hands.py` | Prints raw PHH hands from one iPoker file and one Pluribus hand, then the parser's replay of each (position, street, pot, price, action class, result). | < 5 s |

Run from the repository root with the venv active; the data must be in `D:/datasets/phh-dataset`
(clone command in `../EXECUTION_NOTES.md`).

## Knobs

| Parameter | Effect | Try |
|---|---|---|
| `--file` | which of the 2,081 IPN files (time order) | `--file 1000` (day 12) |
| `--n` | how many hands | `--n 10` |
| `--seed` | which hands | any integer |

## What to watch out for

- `????` means an unknown hole card. Most hands have none known; showdown cards appear on the
  `d dh` line even when the show line reads `sm ????`.
- Stacks are `inf` in the HandHQ data, so an all-in looks like a street dealt with no betting.
  The parser accepts exactly that pattern and marks the hand `implied_allin`.
- A negative entry in `blinds_or_straddles` is a *post* by a newly seated player, not a refund.
- Heads-up hands list the big blind first (pokerkit convention).

## How to read the output

Each decision line shows the price the player faced; `fold` when `to call` is 0 never happens in
a clean hand except as a rare free fold. The result line is exact for uncontested hands and for
showdowns with known cards; otherwise it is an equal split among the showdown players and is
labelled `showdown_unknown`.

## Key takeaways for the final summary

- The data is real but thin: no stacks, no recorded winnings, few known cards, no table names.
  Every downstream statistic has to be defined on what is recorded.
- Replaying each hand with an independent engine is what exposed the three conventions above.
