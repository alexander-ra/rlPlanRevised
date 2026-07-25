"""
textarena_agent.py  [INF / optional]  -- raw L383-398, L406-427.

A THIN, OPTIONAL bridge to TextArena (Guertler et al., 2025, arXiv:2504.11442) -- a benchmark
of 57+ competitive text games with online TrueSkill scoring. It lets the SAME `LLMClient` we
use for Kuhn also play TextArena games, so the LLM-agent findings are not Kuhn-only anecdotes.

WHY IT IS OPTIONAL / GUARDED
----------------------------
`textarena` is not a repo dependency and its API evolves. So this module IMPORTS IT LAZILY and
degrades gracefully: if the package is absent, `textarena_available()` returns False and the
comparison harness simply omits the TextArena column. Kuhn (with the exact Step 02 metric)
remains the primary, self-contained testbed.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Verify against the
installed `textarena` version in the run session (the wrapper below targets the documented
`ta.make(env_id)` / `env.reset` / `env.step` / `env.get_observation` shape and MUST be checked).
"""

from __future__ import annotations

import deps  # noqa: F401

from llm_agent import LLMClient, KuhnPokerLLMAgent, make_client


def textarena_available() -> bool:
    try:
        import textarena  # noqa: F401
        return True
    except Exception:
        return False


class TextArenaLLMAgent:
    """Drive a TextArena environment with an `LLMClient`.

    The prompt is the environment's own natural-language observation; we forward it to the model
    and return the raw text as the action (TextArena parses free-form text actions per game).
    """

    def __init__(self, client: LLMClient, system_prompt: str | None = None,
                 temperature: float = 0.7, max_tokens: int = 512):
        self.client = client
        self.system_prompt = system_prompt or (
            "You are a skilled, rule-abiding player of competitive text games. Read the game "
            "state, reason briefly, and output ONLY the single valid action the game asks for.")
        self.temperature = temperature
        self.max_tokens = max_tokens

    def __call__(self, observation: str) -> str:
        return self.client.chat(self.system_prompt, observation,
                                temperature=self.temperature, max_tokens=self.max_tokens)


def run_episode(env_id: str, client: LLMClient, opponent=None, seed: int = 0) -> dict:
    """Play ONE TextArena episode of `env_id` (two-player). Returns a small result dict.

    Targets the documented TextArena loop; VERIFY the exact call signatures against the
    installed version before trusting results.
    """
    if not textarena_available():
        raise RuntimeError("textarena is not installed; this is the optional TextArena path.")
    import textarena as ta

    agent = TextArenaLLMAgent(client)
    env = ta.make(env_id)
    env.reset(num_players=2, seed=seed)
    done = False
    steps = 0
    while not done:
        player_id, observation = env.get_observation()
        action = agent(observation) if (opponent is None or player_id == 0) else opponent(observation)
        done, _info = env.step(action=action)
        steps += 1
    rewards = env.close()
    return {"env_id": env_id, "steps": steps, "rewards": rewards, "model": client.name}


def _selftest():
    print("textarena_agent self-test")
    print("-" * 50)
    print(f"textarena installed: {textarena_available()}")
    # The wrapper is constructible without textarena; only run_episode needs the package.
    agent = TextArenaLLMAgent(make_client({"backend": "stub"}))
    reply = agent("You are playing a game. State: ... What is your move?")
    print(f"wrapper callable; stub reply first line: {reply.splitlines()[0][:60]!r}")
    if not textarena_available():
        print("(textarena absent -> the comparison harness omits the TextArena column.)")


if __name__ == "__main__":
    _selftest()
