"""
logprob_policy.py  [CORE]  -- exact mixed-strategy extraction from token logprobs (experiment A1).

WHY THIS EXISTS
---------------
The sampling-based `llm_policy` estimates P(action | info set) by calling the model N times and
counting. That is expensive and noisy, and the run session showed it is worse than "noisy":

  - At temperature 0 the model is (near-)deterministic, so all N samples collapse to ONE action and
    every measured frequency degenerates to exactly 0.0 or 1.0. bluff(J) read 0.75, 0.25 and 1.00
    on three runs of the SAME config; raising N from 4 to 24 did not help.
  - At temperature 0.7 the estimate is a Binomial with SE = sqrt(p(1-p)/N) ~ 0.10 at N=24 -- and it
    costs 24 requests per info set.

The model's action distribution is right there in the logits. Seed the assistant turn with
"Action:" so the next token IS the decision, ask for `top_logprobs`, and read the distribution
directly: ONE request, ZERO sampling variance, and the true mixed strategy rather than a sample
of it. On Kuhn that is 12 calls instead of 288 per prompt style (24x cheaper); on Leduc it is what
makes the 936-info-set measurement feasible at all (~45 min instead of ~52 h).

SURFACE-FORM AGGREGATION (the one subtlety)
-------------------------------------------
Probability mass is split across tokenisations of the same word -- measured on qwen2.5-7b:
    ' BET' 0.7628, ' PASS' 0.2366, 'PASS' 0.0004, ' PAS' 0.0001, '_bet' 0.0, ' Bet' 0.0 ...
Taking the top token alone would throw away the mass on the variants and, worse, would report a
PURE strategy. We normalise each token (strip, lowercase, drop non-letters) and SUM the mass per
action using the same `_VERB_TO_ACTION` map the text parser uses, so the two paths agree by
construction.

UNMAPPED MASS = the logprob analogue of the illegal-move rate. Probability the model puts on
tokens that are not any legal action ('**', '_bet', prose). Reported, not silently renormalised
away, because it is a real measure of instruction-following.

VALIDATED SCOPE -- READ THIS BEFORE USING IT (measured 2026-07-26, qwen2.5-7b, N=24, temp 0.7)
----------------------------------------------------------------------------------------------
`validate_logprob.py` compared this estimator against sampling on the SAME prompts:

    prompt style   mean |P(bet) gap|   binomial SE     verdict
    plain          0.027               0.102           CONSISTENT   (3.8x inside the noise floor)
    cot            0.237               0.102           DISCREPANT   (2.3x outside)

So this is a valid drop-in replacement for sampling ONLY when the prompt asks for an immediate
action. With a chain-of-thought prompt the naive prefill CONTRADICTS the instruction -- the prompt
says "think step by step, THEN answer", and we force the answer at token 1 -- which yields an
out-of-distribution policy, not the model's CoT policy (measured exploitability 0.832 vs 0.350
chips for the same prompt sampled properly). Use `reasoned_logprob_policy` for CoT prompts.

NOTE: added during the RUN session (not authored blind). Numbers it produces are MEASUREMENTS.
"""

from __future__ import annotations

import re

import deps  # noqa: F401

from llm_agent import _VERB_TO_ACTION, _PASS, _BET, KuhnPokerLLMAgent

# Tokens that carry no action information; ignored when computing unmapped mass so that markdown
# and whitespace artefacts are not counted as instruction-following failures.
_NEUTRAL = re.compile(r"^[\s\*_#`>\-\.:\"']*$")


def action_distribution(tokens: list, legal_actions=(_PASS, _BET)) -> tuple:
    """[(token, prob), ...] -> ({action: prob}, unmapped_mass, neutral_mass).

    Mass is summed per action over all surface forms, then renormalised over the LEGAL actions.
    `unmapped_mass` is probability on real words that are not a legal action; `neutral_mass` is
    probability on punctuation/markdown noise.
    """
    per_action = {a: 0.0 for a in legal_actions}
    unmapped = 0.0
    neutral = 0.0
    for tok, prob in tokens:
        norm = re.sub(r"[^a-z\-]", "", tok.strip().lower())
        norm = norm.replace("all-in", "allin")
        if norm in _VERB_TO_ACTION:
            a = _VERB_TO_ACTION[norm]
            if a in per_action:
                per_action[a] += prob
            else:
                unmapped += prob            # a legal poker verb, but not legal in THIS state
        elif _NEUTRAL.match(tok):
            neutral += prob
        else:
            unmapped += prob
    total = sum(per_action.values())
    if total <= 0.0:
        # Model put no mass on any legal action: fall back to uniform and let the caller see
        # unmapped_mass ~ 1.0 rather than silently inventing a confident strategy.
        n = len(legal_actions)
        return {a: 1.0 / n for a in legal_actions}, unmapped, neutral
    return {a: p / total for a, p in per_action.items()}, unmapped, neutral


class LogprobStats:
    """Diagnostics accumulated across an extraction pass."""

    def __init__(self):
        self.calls = 0
        self.unmapped_mass = 0.0
        self.neutral_mass = 0.0

    @property
    def mean_unmapped(self) -> float:
        return self.unmapped_mass / self.calls if self.calls else 0.0

    @property
    def mean_neutral(self) -> float:
        return self.neutral_mass / self.calls if self.calls else 0.0


def logprob_policy(agent: KuhnPokerLLMAgent, opponent_profile: str | None = None,
                   prefill: str = "Action:", top_logprobs: int = 20,
                   stats: LogprobStats | None = None, cache: dict | None = None):
    """Game-interface policy (game, state) -> {action: prob} using ONE logprob call per info set.

    Drop-in replacement for `llm_agent.llm_policy`, so it composes with
    `strategy_extraction.extract_policy_strategy` and the exact Step 02 metric unchanged.
    """
    stats = stats if stats is not None else LogprobStats()
    cache = cache if cache is not None else {}

    def policy(game, state):
        legal = tuple(game.legal_actions(state))
        player = game.current_player(state)
        card = int(state.cards[player])
        history = state.history
        key = (card, history, legal)
        if key not in cache:
            system, user = agent.build_prompt(card, history, opponent_profile)
            toks = agent.client.chat_logprobs(system, user, prefill=prefill,
                                              top_logprobs=top_logprobs)
            dist, unmapped, neutral = action_distribution(toks, legal)
            stats.calls += 1
            stats.unmapped_mass += unmapped
            stats.neutral_mass += neutral
            cache[key] = dist
        return dict(cache[key])

    policy.stats = stats          # type: ignore[attr-defined]
    policy.cache = cache          # type: ignore[attr-defined]
    return policy


_ACTION_TAIL = re.compile(r"\n?\s*(?:\*\*)?\s*action\s*[:\-/=]", re.IGNORECASE)


def strip_trailing_action(text: str) -> str:
    """Drop the model's final 'Action: X' line, keeping the reasoning that led to it."""
    matches = list(_ACTION_TAIL.finditer(text))
    return text[:matches[-1].start()].rstrip() if matches else text.rstrip()


def reasoned_action_distribution(agent, card: int, history: str, legal=(_PASS, _BET),
                                 k: int = 4, opponent_profile: str | None = None,
                                 top_logprobs: int = 20) -> tuple:
    """CoT-safe extraction: let the model reason, THEN read the action distribution.

    Why this exists: with a chain-of-thought prompt the naive prefill is invalid (see the module
    docstring). Here we sample `k` reasonings and, for each, re-prompt with that reasoning as the
    assistant prefill plus "Action:" -- reading the FULL distribution at the decision token instead
    of a single 0/1 draw, then averaging.

    This is Rao-Blackwellisation, not a free lunch: a CoT policy mixes through TWO channels --
    variation in the reasoning, and variation in the action given that reasoning. Logprobs
    integrate out the second exactly; the first still needs sampling. So the cost is 2k calls
    rather than 1, but the variance at fixed budget is far lower than k binary draws (each sample
    contributes a probability, not a coin flip).
    """
    system, user = agent.build_prompt(card, history, opponent_profile)
    acc = {a: 0.0 for a in legal}
    unmapped = neutral = 0.0
    for _ in range(k):
        raw = agent.client.chat(system, user, temperature=agent.temperature)
        prefill = strip_trailing_action(raw) + "\nAction:"
        toks = agent.client.chat_logprobs(system, user, prefill=prefill,
                                          top_logprobs=top_logprobs)
        dist, um, ne = action_distribution(toks, legal)
        for a in legal:
            acc[a] += dist[a] / k
        unmapped += um / k
        neutral += ne / k
    return acc, unmapped, neutral


def reasoned_logprob_policy(agent: KuhnPokerLLMAgent, k: int = 4,
                            opponent_profile: str | None = None,
                            stats: LogprobStats | None = None, cache: dict | None = None):
    """Game-interface policy using `reasoned_action_distribution` (CoT-safe, 2k calls/info set)."""
    stats = stats if stats is not None else LogprobStats()
    cache = cache if cache is not None else {}

    def policy(game, state):
        legal = tuple(game.legal_actions(state))
        player = game.current_player(state)
        card = int(state.cards[player])
        history = state.history
        key = (card, history, legal)
        if key not in cache:
            dist, um, ne = reasoned_action_distribution(agent, card, history, legal, k,
                                                        opponent_profile)
            stats.calls += 2 * k
            stats.unmapped_mass += um
            stats.neutral_mass += ne
            cache[key] = dist
        return dict(cache[key])

    policy.stats = stats          # type: ignore[attr-defined]
    policy.cache = cache          # type: ignore[attr-defined]
    return policy


def _selftest():
    """Offline check of the aggregation maths (no server needed)."""
    print("logprob_policy self-test (aggregation only; no model calls)")
    print("-" * 66)
    # Real measured distribution from qwen2.5-7b on the Jack-first-to-act node.
    toks = [(" BET", 0.7628), (" PASS", 0.2366), ("PASS", 0.0004), (" PAS", 0.0001),
            ("_bet", 0.0), ("_PASS", 0.0), (" **", 0.0), ("_pass", 0.0)]
    dist, unmapped, neutral = action_distribution(toks)
    print(f"  dist        = P(pass)={dist[_PASS]:.4f}  P(bet)={dist[_BET]:.4f}")
    print(f"  unmapped    = {unmapped:.4f}   neutral = {neutral:.4f}")
    assert abs(dist[_PASS] + dist[_BET] - 1.0) < 1e-9, "distribution must sum to 1"
    assert abs(dist[_BET] - 0.7628 / (0.7628 + 0.2371)) < 1e-3, "surface forms must be summed"
    print("  -> PASS mass correctly aggregated across ' PASS'/'PASS'/' PAS'")

    # Degenerate case: all mass on non-actions.
    dist2, unmapped2, _ = action_distribution([("**", 0.6), ("Sure", 0.4)])
    print(f"  no-legal-mass case -> dist={dist2}, unmapped={unmapped2:.2f} (expect uniform + ~0.4)")
    assert abs(dist2[_PASS] - 0.5) < 1e-9
    print("done.")


if __name__ == "__main__":
    _selftest()
