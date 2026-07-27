"""
validate_logprob.py  [CORE]  -- does exact logprob extraction agree with sampling? (experiment A1)

A cheaper estimator is only worth having if it measures the SAME thing. This runs both estimators
on the same model, same prompt style, same info sets, and reports:

  - per-info-set P(bet) from each method, and the max/mean absolute gap
  - exploitability under each induced strategy (the exact Step 02 metric)
  - cost: number of HTTP calls each needed
  - the logprob path's unmapped mass (its analogue of the illegal-move rate)

Expected (a prediction, to be checked): the two agree within sampling error -- roughly
SE = sqrt(p(1-p)/N) ~ 0.10 at N=24 -- while the logprob path uses 1/N of the calls. A LARGE,
systematic gap would mean the prefill ("Action:") changes the model's behaviour relative to free
generation, which would be a finding in its own right and a reason to keep sampling.

Usage:  python validate_logprob.py [--style cot] [--samples 24] [--temp 0.7]
Writes results/logprob_validation_<model>.json
"""

from __future__ import annotations

import argparse
import json
import os
import time

import deps  # noqa: F401
from engines import make_game

from config import active_config
from llm_agent import make_client, KuhnPokerLLMAgent, llm_policy, _BET
from logprob_policy import logprob_policy, LogprobStats
from strategy_extraction import extract_policy_strategy, KUHN_INFO_SETS
from evaluation import exploitability_chips, chips_to_mbb_per_hand, bluff_freq, value_bet_freq


def _pbet(node_map: dict) -> dict:
    return {i: node_map[i].get_average_strategy()[_BET] for i in KUHN_INFO_SETS}


def main():
    ap = argparse.ArgumentParser(description="A1: logprob vs sampled strategy extraction.")
    ap.add_argument("--style", default="cot")
    ap.add_argument("--samples", type=int, default=None, help="override llm_samples")
    ap.add_argument("--temp", type=float, default=None, help="override temperature")
    args = ap.parse_args()

    cfg = active_config()
    n = args.samples or cfg["llm_samples"]
    temp = args.temp if args.temp is not None else cfg["llm_temperature"]
    game = make_game(cfg["game"])
    preset = cfg.get("llm_preset") or {}
    model = preset.get("model", "stub")

    print(f"A1 validation: model={model} style={args.style} samples={n} temp={temp}")
    print("=" * 78)

    # --- exact: one logprob call per info set -------------------------------------------
    agent_lp = KuhnPokerLLMAgent(make_client(preset), prompt_style=args.style, temperature=temp)
    stats = LogprobStats()
    t0 = time.time()
    nm_lp = extract_policy_strategy(logprob_policy(agent_lp, stats=stats), game)
    t_lp = time.time() - t0
    expl_lp = exploitability_chips(nm_lp)

    # --- sampled: n calls per info set ---------------------------------------------------
    agent_s = KuhnPokerLLMAgent(make_client(preset), prompt_style=args.style, temperature=temp)
    t0 = time.time()
    nm_s = extract_policy_strategy(llm_policy(agent_s, samples=n), game)
    t_s = time.time() - t0
    expl_s = exploitability_chips(nm_s)

    p_lp, p_s = _pbet(nm_lp), _pbet(nm_s)
    gaps = {i: abs(p_lp[i] - p_s[i]) for i in KUHN_INFO_SETS}
    max_i = max(gaps, key=gaps.get)

    print(f"{'info set':<10}{'P(bet) logprob':>16}{'P(bet) sampled':>16}{'|gap|':>9}")
    print("-" * 51)
    for i in KUHN_INFO_SETS:
        print(f"{i:<10}{p_lp[i]:>16.3f}{p_s[i]:>16.3f}{gaps[i]:>9.3f}")
    print("-" * 51)
    mean_gap = sum(gaps.values()) / len(gaps)
    se = (0.25 / n) ** 0.5
    print(f"mean |gap| = {mean_gap:.3f}   max |gap| = {gaps[max_i]:.3f} at {max_i!r}")
    print(f"binomial SE at N={n} (worst case p=0.5) = {se:.3f}  -> "
          f"{'CONSISTENT' if mean_gap <= 2 * se else 'DISCREPANT (investigate before trusting A1)'}")
    print()
    print(f"exploitability : logprob {expl_lp:.4f} chips ({chips_to_mbb_per_hand(expl_lp):.1f} mbb/h)"
          f" | sampled {expl_s:.4f} chips ({chips_to_mbb_per_hand(expl_s):.1f} mbb/h)")
    print(f"bluff(J)       : logprob {bluff_freq(nm_lp):.3f} | sampled {bluff_freq(nm_s):.3f}")
    print(f"value-bet(K)   : logprob {value_bet_freq(nm_lp):.3f} | sampled {value_bet_freq(nm_s):.3f}")
    print(f"cost           : logprob {stats.calls} calls in {t_lp:.0f}s | "
          f"sampled {agent_s.stats.calls} calls in {t_s:.0f}s "
          f"({agent_s.stats.calls / max(1, stats.calls):.0f}x more)")
    print(f"unmapped mass  : mean {stats.mean_unmapped:.4f} (logprob analogue of illegal rate); "
          f"sampled illegal rate {agent_s.stats.illegal_rate():.2%}")

    payload = {
        "model": model, "style": args.style, "samples": n, "temperature": temp,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "p_bet_logprob": p_lp, "p_bet_sampled": p_s, "abs_gap": gaps,
        "mean_abs_gap": mean_gap, "max_abs_gap": gaps[max_i], "max_gap_info_set": max_i,
        "binomial_se": se,
        "exploitability_chips": {"logprob": expl_lp, "sampled": expl_s},
        "bluff_freq_J": {"logprob": bluff_freq(nm_lp), "sampled": bluff_freq(nm_s)},
        "value_bet_freq_K": {"logprob": value_bet_freq(nm_lp), "sampled": value_bet_freq(nm_s)},
        "calls": {"logprob": stats.calls, "sampled": agent_s.stats.calls},
        "seconds": {"logprob": round(t_lp, 1), "sampled": round(t_s, 1)},
        "unmapped_mass_mean": stats.mean_unmapped,
        "sampled_illegal_rate": agent_s.stats.illegal_rate(),
    }
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    safe = model.replace("/", "_")
    path = os.path.join(out_dir, f"logprob_validation_{safe}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nsaved -> {path}")


if __name__ == "__main__":
    main()
