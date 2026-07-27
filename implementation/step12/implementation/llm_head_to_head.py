"""
llm_head_to_head.py  [SUP]  -- model vs model on the exact Kuhn ruler (experiment C10).

Exploitability says how a PERFECT adversary punishes each model; the zoo (B6) says how each model
punishes SCRIPTED weakness. Neither says what happens when two language models play each other --
which is the setting people actually care about when they talk about "LLMs playing games".

Because each model's policy here is STATIC (no cross-hand memory), we extract it once with 12
logprob calls (A1, validated on the `plain` style) and then simulate the whole round robin with
zero further model calls. Strategies are cached to results/strategy_<model>_<style>.json so
re-running the tournament is free.

Reported per pair: mean chips/hand for the row player, seats alternated so Kuhn's first-mover
disadvantage (-1/18) cannot bias any cell. Nash-CFR is included as a calibration row: it should be
near 0 against everyone (it neither exploits nor is exploited), which doubles as a sanity check on
the whole tournament.

Usage:
    python llm_head_to_head.py --extract qwen2.5_7b        # 12 calls, caches the strategy
    python llm_head_to_head.py --extract gpt_oss_20b       # (load each model first via lms)
    python llm_head_to_head.py --tournament --hands 20000  # call-free

NOTE: added during the RUN session. All numbers are MEASUREMENTS.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import random
import time

import deps  # noqa: F401
from engines import make_game
from policies import sample_action, tabular_policy

from config import active_config, LLM_ROSTER
from llm_agent import make_client, KuhnPokerLLMAgent, _PASS, _BET
from logprob_policy import logprob_policy, LogprobStats
from strategy_extraction import extract_policy_strategy, KUHN_INFO_SETS
from evaluation import exploitability_chips
from trajectory_dataset import make_cfr_policy

_RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def _path(tag: str) -> str:
    return os.path.join(_RES, f"strategy_{tag}.json")


def extract_and_cache(roster_key: str, style: str, temp: float) -> str:
    cfg = active_config()
    game = make_game(cfg["game"])
    preset = LLM_ROSTER[roster_key]
    model = preset["model"]
    agent = KuhnPokerLLMAgent(make_client(preset), prompt_style=style, temperature=temp)
    stats = LogprobStats()
    nm = extract_policy_strategy(logprob_policy(agent, stats=stats), game)
    table = {i: nm[i].get_average_strategy() for i in KUHN_INFO_SETS}
    tag = f"{model.replace('/', '_')}_{style}"
    os.makedirs(_RES, exist_ok=True)
    payload = {"model": model, "roster_key": roster_key, "style": style, "temperature": temp,
               "calls": stats.calls, "unmapped_mass": stats.mean_unmapped,
               "exploitability_chips": exploitability_chips(nm),
               "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"), "strategy": table}
    with open(_path(tag), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"extracted {model} ({style}) in {stats.calls} calls -> {_path(tag)}")
    print(f"  exploitability = {payload['exploitability_chips']:.4f} chips, "
          f"unmapped mass = {stats.mean_unmapped:.4f}")
    return tag


def _policy_from_table(table: dict):
    """info_set -> [p_pass, p_bet]  ==>  a Game-interface policy."""
    as_dist = {i: {_PASS: v[0], _BET: v[1]} for i, v in table.items()}
    return tabular_policy(as_dist)


def play(game, pol_a, pol_b, hands: int, seed: int) -> float:
    """Mean chips/hand for A, seats alternated."""
    rng = random.Random(seed)
    deals = game.deals()
    tot = 0.0
    for h in range(hands):
        a_seat = h % 2
        pols = [None, None]
        pols[a_seat] = pol_a
        pols[1 - a_seat] = pol_b
        state = game.root(rng.choice(deals))
        while not game.is_terminal(state):
            p = game.current_player(state)
            state = game.apply(state, sample_action(pols[p](game, state), rng))
        tot += game.utility(state, a_seat)
    return tot / max(1, hands)


def main():
    ap = argparse.ArgumentParser(description="C10: LLM vs LLM head-to-head.")
    ap.add_argument("--extract", help="roster key to extract and cache")
    ap.add_argument("--tournament", action="store_true")
    ap.add_argument("--style", default="plain", help="A1 is validated for 'plain'")
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--hands", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    if args.extract:
        extract_and_cache(args.extract, args.style, args.temp)
        return
    if not args.tournament:
        ap.error("pass --extract <key> or --tournament")

    cfg = active_config()
    game = make_game(cfg["game"])
    nash_policy, _ = make_cfr_policy(game, max(cfg["cfr_iters"], 50000), cfg["seed"])

    entries = {"Nash-CFR": (nash_policy, exploitability_chips(
        extract_policy_strategy(nash_policy, game)))}
    for p in sorted(glob.glob(os.path.join(_RES, "strategy_*.json"))):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        if d.get("style") != args.style:
            continue
        entries[d["model"]] = (_policy_from_table(d["strategy"]), d["exploitability_chips"])

    if len(entries) < 3:
        raise SystemExit(f"Only {len(entries)} entrants found. Extract at least two models first:\n"
                         "  python llm_head_to_head.py --extract qwen2.5_7b\n"
                         "  python llm_head_to_head.py --extract gpt_oss_20b")

    names = list(entries)
    print(f"C10 head-to-head: {len(names)} entrants, {args.hands} hands/pair, style={args.style}")
    print("=" * 78)
    matrix = {a: {} for a in names}
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if i == j:
                matrix[a][b] = 0.0
            elif j < i:
                matrix[a][b] = -matrix[b][a]          # zero-sum: reuse the mirrored result
            else:
                matrix[a][b] = play(game, entries[a][0], entries[b][0], args.hands, args.seed)

    w = max(len(n) for n in names) + 2
    hdr = " " * w + "".join(f"{n[:13]:>15}" for n in names) + f"{'MEAN':>10}{'expl':>10}"
    print(hdr)
    print("-" * len(hdr))
    for a in names:
        opp = [matrix[a][b] for b in names if b != a]
        line = f"{a:<{w}}" + "".join(f"{matrix[a][b]:>15.4f}" for b in names)
        line += f"{sum(opp) / len(opp):>10.4f}{entries[a][1]:>10.4f}"
        print(line)
    print("-" * len(hdr))
    print("(row player's chips/hand; seats alternated. Nash row ~0 everywhere = sanity check.)")

    payload = {"style": args.style, "hands": args.hands, "seed": args.seed,
               "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "exploitability": {a: entries[a][1] for a in names},
               "matrix": matrix}
    out = os.path.join(_RES, "head_to_head.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nsaved -> {out}")


if __name__ == "__main__":
    main()
