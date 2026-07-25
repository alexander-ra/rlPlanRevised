"""
exploration/llm_kuhn_repl.py

PROBE: watch an LLM actually PLAY Kuhn Poker on the real Step 02 engine and read its reasoning.

Plays a handful of hands of (LLM vs a fixed opponent) on the step07 `Game` wrapper over the
step02 Kuhn engine, printing the LLM's private card, the betting so far, its raw reasoning, and
the parsed action -- so you can SEE where the reasoning is sound and where it goes wrong.

By default it uses the OFFLINE scripted-reasoner stub (no GPU / no keys), so it runs anywhere.
Point it at a real local model by editing `SPEC` (see implementation/config.py presets), e.g.:
    SPEC = {"backend": "openai", "base_url": "http://localhost:1234/v1", "model": "gpt-oss-20b"}

PREDICTIONS (verify in the run session):
  - The stub folds the Jack to a bet, value-bets the King, and mostly checks the Queen.
  - A real LLM will usually play the King/Jack sensibly but mis-set its BLUFF frequency and
    occasionally emit an unmappable action (illegal-move rate > 0) -- captured by the harness.
"""

from __future__ import annotations

import random

import _bootstrap  # noqa: F401
from engines import make_game
from policies import sample_action
from trajectory_dataset import make_cfr_policy
from llm_agent import make_client, KuhnPokerLLMAgent

# Swap this for a config.py preset to use a real local model.
SPEC = {"backend": "stub"}
N_HANDS = 6
PROMPT_STYLE = "cot"


def main():
    print(f"llm_kuhn_repl -- {PROMPT_STYLE} prompt, backend={SPEC.get('backend')} "
          "(predictions only)")
    print("-" * 66)
    game = make_game("kuhn")
    rng = random.Random(0)
    agent = KuhnPokerLLMAgent(make_client(SPEC), prompt_style=PROMPT_STYLE, temperature=0.0)
    # Opponent: near-Nash CFR (cheap budget for the probe).
    opp_policy, _ = make_cfr_policy(game, iters=3000, seed=0)
    llm_seat = 0

    for h in range(N_HANDS):
        deal = rng.choice(game.deals())
        state = game.root(deal)
        print(f"\n=== hand {h + 1}: LLM holds "
              f"{ {1:'J',2:'Q',3:'K'}[deal[llm_seat]] } ===")
        while not game.is_terminal(state):
            p = game.current_player(state)
            if p == llm_seat:
                card = int(state.cards[p])
                a, raw, ok = agent.act(card, state.history)
                print(f"  [LLM] hist={state.history!r:5} -> "
                      f"{'BET' if a == 1 else 'PASS'} (parsed_ok={ok})")
                print(f"        {raw.splitlines()[-1]}")
            else:
                a = sample_action(opp_policy(game, state), rng)
                print(f"  [opp] hist={state.history!r:5} -> {'BET' if a == 1 else 'PASS'}")
            state = game.apply(state, a)
        print(f"  result: LLM utility = {game.utility(state, llm_seat):+.0f} chips")

    print(f"\nLLM illegal-move rate over the session: {agent.stats.illegal_rate():.0%} "
          f"({agent.stats.calls} calls). (Stub -> expect 0%.)")


if __name__ == "__main__":
    main()
