"""
evaluation.py  [CORE]  -- raw L430-463.

The metrics every agent is graded on, all computed from a Kuhn `node_map` (see
strategy_extraction.py) or from an LLM agent's call stats:

  - exploitability_chips(node_map) : the EXACT Step 02 metric (BR0 + BR1). This is the headline
    number; 0 = Nash. Reported in CHIPS (see the units note below).
  - bluff_freq(node_map)           : P(bet | Jack, first to act) -- the classic Kuhn bluff.
  - value_bet_freq(node_map)       : P(bet | King, first to act) -- value betting the nuts.
  - illegal_move_rate(agent)       : fraction of LLM replies that were unmappable to a legal
                                     action (a headline LLM-agent failure mode).
  - opponent_adaptation(agent)     : does the LLM change its bluffing when TOLD the opponent is
                                     a calling-station vs a folder? (Memoryless single-hand LLMs
                                     only adapt if given opponent info in the prompt.)

UNITS NOTE (raw L462 says "within 50 mbb/h"; we report CHIPS)
------------------------------------------------------------
Step 02's `compute_exploitability` returns NashConv in CHIPS (the sum of both players'
best-response gains). The raw target is phrased in milli-big-blinds per hand (mbb/h). Treating
the 1-chip ante as the big blind, 1 chip = 1000 mbb, so `chips_to_mbb_per_hand(chips)` = chips *
1000. The "within 50 mbb/h of Nash" target therefore means exploitability <= 0.05 chips. We
expose both so the threshold is read correctly (raw L462 vs Step 02's chip units).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import deps  # noqa: F401
from evaluate.exploitability import compute_exploitability  # step02 exact metric

_PASS, _BET = 0, 1
BIG_BLIND_CHIPS = 1.0  # the ante in Kuhn, used as the bb unit for the mbb/h conversion


# --- headline exploitability ---------------------------------------------------------
def exploitability_chips(node_map: dict) -> float:
    """Exact Kuhn exploitability (NashConv), in CHIPS, via Step 02. 0 == Nash."""
    return float(compute_exploitability(node_map))


def chips_to_mbb_per_hand(chips: float, big_blind: float = BIG_BLIND_CHIPS) -> float:
    """Convert chip exploitability to milli-big-blinds per hand (raw L462's unit)."""
    return chips * 1000.0 / big_blind


def exploitability_mbb_per_hand(node_map: dict) -> float:
    return chips_to_mbb_per_hand(exploitability_chips(node_map))


# --- strategy-shape metrics ----------------------------------------------------------
def _bet_prob(node_map: dict, info_set: str) -> float:
    node = node_map.get(info_set)
    if node is None:
        return float("nan")
    return float(node.get_average_strategy()[_BET])


def bluff_freq(node_map: dict) -> float:
    """P(bet | Jack, first to act). Nash bluffs the Jack at a specific low frequency."""
    return _bet_prob(node_map, "1")


def value_bet_freq(node_map: dict) -> float:
    """P(bet | King, first to act)."""
    return _bet_prob(node_map, "3")


def strategy_metrics(node_map: dict) -> dict:
    """All node_map-derived metrics in one dict."""
    chips = exploitability_chips(node_map)
    return {
        "exploitability_chips": chips,
        "exploitability_mbb_per_hand": chips_to_mbb_per_hand(chips),
        "bluff_freq_J": bluff_freq(node_map),
        "value_bet_freq_K": value_bet_freq(node_map),
    }


# --- LLM-specific metrics ------------------------------------------------------------
def illegal_move_rate(agent) -> float:
    """Fraction of the agent's replies that could not be mapped to a legal action."""
    return agent.stats.illegal_rate()


def opponent_adaptation(agent, samples: int = 12) -> dict:
    """Does the LLM bluff LESS vs a calling-station and MORE vs a folder when TOLD so?

    Returns bluff frequency (P(bet | Jack, first to act)) under two opponent notes plus the
    delta. A strategically adaptive agent should bluff less against a station (it never folds)
    and more against a folder. Prediction to verify; the offline stub ignores the note, so its
    delta should be ~0 (a useful negative control).
    """
    station = "Your opponent calls almost every bet and never folds."
    folder = "Your opponent folds far too often to any bet."

    def bluff_rate(note):
        bets = 0
        for _ in range(samples):
            a, _raw, _ok = agent.act(1, "", (_PASS, _BET), opponent_profile=note)
            bets += 1 if a == _BET else 0
        return bets / samples

    vs_station = bluff_rate(station)
    vs_folder = bluff_rate(folder)
    return {"bluff_vs_station": vs_station, "bluff_vs_folder": vs_folder,
            "adaptation_delta": vs_folder - vs_station}


def _selftest():
    from engines import make_game
    from trajectory_dataset import make_cfr_policy
    from strategy_extraction import extract_policy_strategy
    from llm_agent import KuhnPokerLLMAgent, ScriptedReasonerClient

    print("evaluation self-test")
    print("-" * 60)
    game = make_game("kuhn")
    nash_policy, _ = make_cfr_policy(game, iters=4000, seed=0)
    nm = extract_policy_strategy(nash_policy, game)
    m = strategy_metrics(nm)
    print(f"[Nash-CFR] exploitability = {m['exploitability_chips']:.4f} chips "
          f"({m['exploitability_mbb_per_hand']:.1f} mbb/h) -- expect ~0")
    print(f"[Nash-CFR] bluff(J)={m['bluff_freq_J']:.3f}  value_bet(K)={m['value_bet_freq_K']:.3f}")

    agent = KuhnPokerLLMAgent(ScriptedReasonerClient(), prompt_style="cot")
    print(f"[LLM-stub] illegal rate = {illegal_move_rate(agent):.2%} (before any calls: 0)")
    adapt = opponent_adaptation(agent, samples=10)
    print(f"[LLM-stub] adaptation delta = {adapt['adaptation_delta']:+.2f} "
          "(stub ignores the note -> ~0 expected)")


if __name__ == "__main__":
    _selftest()
