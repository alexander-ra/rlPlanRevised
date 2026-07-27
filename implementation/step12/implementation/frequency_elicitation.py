"""
frequency_elicitation.py  [CORE]  -- does the model KNOW the frequency it fails to PLAY? (exp. B4)

THE QUESTION
------------
Every measured model gets hand RANKING right (King > Queen > Jack) and FREQUENCIES wrong: all of
them value-bet the King at 1.00 where Nash mixes at 0.68, and none bluffs the Jack under a plain
prompt. "The LLM is exploitable" does not distinguish three very different explanations:

  (a) IGNORANCE  - it does not know the right frequency.
  (b) EXECUTION  - it knows the frequency but cannot sample from it (a single forward pass emits
                   the argmax token; mixing requires a randomiser it does not have).
  (c) BOTH.

This separates them by asking the model, at the SAME 12 info sets and with byte-identical situation
text, "what percentage of the time should you BET here?" -- and comparing three quantities:

    stated(I)   - the frequency it says is correct        (knowledge)
    executed(I) - its actual P(bet) from logprobs (A1)    (behaviour)
    nash(I)     - ground truth                            (target)

DIAGNOSIS
    |stated - nash| small AND |executed - nash| large  -> (b) EXECUTION gap: it knows, cannot mix.
    |stated - nash| large                              -> (a) IGNORANCE (at least partly).

We also build a full strategy out of the STATED frequencies and score it with the exact Step 02
metric. That converts the knowing-vs-doing gap into chips: "if this model played at the frequencies
it itself says are correct, it would be X times less exploitable."

Usage:  python frequency_elicitation.py [--style frequency] [--repeats 3]
Writes results/frequency_elicitation_<model>.json

NOTE: added during the RUN session. All numbers are MEASUREMENTS.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import time

import deps  # noqa: F401
from engines import make_game

from config import active_config
from llm_agent import make_client, KuhnPokerLLMAgent, _BET
from logprob_policy import logprob_policy, LogprobStats
from strategy_extraction import (KUHN_INFO_SETS, _parse_info_set, _StrategyNode,
                                 extract_policy_strategy)
from evaluation import exploitability_chips, chips_to_mbb_per_hand
from trajectory_dataset import make_cfr_policy

_NUM = re.compile(r"(\d{1,3}(?:\.\d+)?)\s*%?")


def parse_percentage(text: str):
    """First number in [0,100] -> fraction in [0,1]; None if unparseable."""
    if not text:
        return None
    # Strip an inline reasoning block first (same hazard as parse_action).
    low = text.strip()
    if "</think>" in low.lower():
        low = low[low.lower().rindex("</think>") + len("</think>"):]
    for m in _NUM.finditer(low):
        try:
            v = float(m.group(1))
        except ValueError:
            continue
        if 0.0 <= v <= 100.0:
            return v / 100.0
    return None


def elicit(agent: KuhnPokerLLMAgent, card: int, history: str, repeats: int = 1):
    """Ask for the BET percentage at one info set; returns (mean, [raw values], n_unparsed)."""
    vals, bad = [], 0
    system, user = agent.build_prompt(card, history)
    for _ in range(repeats):
        raw = agent.client.chat(system, user, temperature=agent.temperature, max_tokens=64)
        v = parse_percentage(raw)
        if v is None:
            bad += 1
        else:
            vals.append(v)
    return (statistics.fmean(vals) if vals else None), vals, bad


def main():
    ap = argparse.ArgumentParser(description="B4: stated vs executed mixing frequency.")
    ap.add_argument("--repeats", type=int, default=3,
                    help="elicitations per info set (averaged; the ASK is cheap)")
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--exec-style", default="cot",
                    help="prompt style used for the EXECUTED (logprob) strategy")
    args = ap.parse_args()

    cfg = active_config()
    game = make_game(cfg["game"])
    preset = cfg.get("llm_preset") or {}
    model = preset.get("model", "stub")

    nash_policy, _ = make_cfr_policy(game, max(cfg["cfr_iters"], 50000), cfg["seed"])
    nash_nm = extract_policy_strategy(nash_policy, game)
    nash = {i: nash_nm[i].get_average_strategy()[_BET] for i in KUHN_INFO_SETS}

    print(f"B4 frequency elicitation: model={model} repeats={args.repeats} temp={args.temp}")
    print("=" * 78)

    # --- executed behaviour (A1 logprobs, one call per info set) -------------------------
    exec_agent = KuhnPokerLLMAgent(make_client(preset), prompt_style=args.exec_style,
                                   temperature=args.temp)
    stats = LogprobStats()
    exec_nm = extract_policy_strategy(logprob_policy(exec_agent, stats=stats), game)
    executed = {i: exec_nm[i].get_average_strategy()[_BET] for i in KUHN_INFO_SETS}

    # --- stated knowledge ---------------------------------------------------------------
    ask_agent = KuhnPokerLLMAgent(make_client(preset), prompt_style="frequency",
                                  temperature=args.temp)
    stated, raw_all, unparsed = {}, {}, 0
    for iset in KUHN_INFO_SETS:
        card, history, _player = _parse_info_set(iset)
        mean, vals, bad = elicit(ask_agent, card, history, args.repeats)
        stated[iset] = mean
        raw_all[iset] = vals
        unparsed += bad

    # --- report --------------------------------------------------------------------------
    hdr = f"{'info set':<9}{'stated':>9}{'executed':>10}{'nash':>8}{'|st-nash|':>11}{'|ex-nash|':>11}"
    print(hdr)
    print("-" * len(hdr))
    st_err, ex_err = [], []
    for i in KUHN_INFO_SETS:
        s = stated[i]
        e, n = executed[i], nash[i]
        se = abs(s - n) if s is not None else float("nan")
        ee = abs(e - n)
        if s is not None:
            st_err.append(se)
        ex_err.append(ee)
        s_txt = f"{s:>9.3f}" if s is not None else f"{'n/a':>9}"
        print(f"{i:<9}{s_txt}{e:>10.3f}{n:>8.3f}{se:>11.3f}{ee:>11.3f}")
    print("-" * len(hdr))
    mae_stated = statistics.fmean(st_err) if st_err else float("nan")
    mae_exec = statistics.fmean(ex_err)
    print(f"MAE vs Nash: stated={mae_stated:.3f}   executed={mae_exec:.3f}")

    # --- what if it PLAYED what it SAYS? -------------------------------------------------
    stated_nm = {}
    for i in KUHN_INFO_SETS:
        p = stated[i] if stated[i] is not None else executed[i]
        stated_nm[i] = _StrategyNode([1.0 - p, p])
    expl_stated = exploitability_chips(stated_nm)
    expl_exec = exploitability_chips(exec_nm)
    expl_nash = exploitability_chips(nash_nm)

    print()
    print(f"exploitability  executed(played)  = {expl_exec:.4f} chips "
          f"({chips_to_mbb_per_hand(expl_exec):.1f} mbb/h)")
    print(f"exploitability  stated(if played) = {expl_stated:.4f} chips "
          f"({chips_to_mbb_per_hand(expl_stated):.1f} mbb/h)")
    print(f"exploitability  Nash              = {expl_nash:.4f} chips")
    if expl_stated < expl_exec:
        print(f"-> KNOWING-vs-DOING GAP: playing its own stated frequencies would be "
              f"{expl_exec / max(expl_stated, 1e-9):.1f}x LESS exploitable.")
    else:
        print("-> No knowing-vs-doing gap: its stated frequencies are no better than its play.")
    print(f"unparsed elicitations: {unparsed}/{len(KUHN_INFO_SETS) * args.repeats}")

    payload = {
        "model": model, "repeats": args.repeats, "temperature": args.temp,
        "exec_style": args.exec_style, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stated": stated, "executed": executed, "nash": nash, "raw_elicitations": raw_all,
        "mae_stated_vs_nash": mae_stated, "mae_executed_vs_nash": mae_exec,
        "exploitability_chips": {"executed": expl_exec, "stated_if_played": expl_stated,
                                 "nash": expl_nash},
        "unparsed": unparsed, "logprob_unmapped_mass": stats.mean_unmapped,
    }
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"frequency_elicitation_{model.replace('/', '_')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nsaved -> {path}")


if __name__ == "__main__":
    main()
