"""
leduc_illegal_taxonomy.py  [SUP]  -- WHAT kind of illegal action does the model want to take?

The Leduc scouting run measured ~25% of probability mass landing on actions that are not legal in
the current state (vs 0-1% illegal moves in Kuhn). That single number is ambiguous: it could be one
systematic misconception or diffuse confusion about the rules, and those are very different claims.

This breaks it down. Leduc has exactly two ways to want an illegal action, plus a format failure:

  FOLD_WHEN_FREE  - wanting to FOLD when nothing is due, so checking is free. Strictly dominated:
                    folding a free check throws away equity for nothing. Legal actions are (CALL,
                    RAISE); fold is not offered.
  RAISE_AT_CAP    - wanting to RAISE when the round's 2-raise cap is already reached. A rules/limit
                    misunderstanding rather than a strategic error. Legal actions are (FOLD, CALL).
  NON_ACTION      - probability on tokens that are not a poker action at all (prose, markdown).
                    A pure instruction-following failure.

Cross-tabbed by round (first/second) and by whether a bet is facing the player, so a systematic
pattern is separable from noise.

Method: sample info sets by REACH (random playouts) rather than enumerating all 936, then read the
raw 3-action logprob distribution at each WITHOUT masking, so illegal mass is measured rather than
renormalised away.

Usage:  python leduc_illegal_taxonomy.py [--max-infosets 250]
Writes results/leduc_illegal_taxonomy_<model>.json

NOTE: added during the RUN session. All numbers are MEASUREMENTS.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import time

import numpy as np

import deps  # noqa: F401
from engines import make_game

from config import active_config, LLM_ROSTER
from llm_agent import make_client
from logprob_policy import _NEUTRAL, map_token
from leduc_llm import build_prompt, _LEDUC_VERB, FOLD, CALL, RAISE

_NAME = {FOLD: "FOLD", CALL: "CALL", RAISE: "RAISE"}


def raw_action_mass(tokens) -> tuple:
    """Mass per action id REGARDLESS of legality, plus non-action and neutral mass."""
    per = {FOLD: 0.0, CALL: 0.0, RAISE: 0.0}
    non_action = 0.0
    neutral = 0.0
    for tok, prob in tokens:
        norm = re.sub(r"[^a-z\-]", "", tok.strip().lower()).replace("all-in", "allin")
        a = map_token(norm, _LEDUC_VERB)
        if a is not None:
            per[a] += prob
        elif _NEUTRAL.match(tok):
            neutral += prob
        else:
            non_action += prob
    return per, non_action, neutral


def sample_infosets(game, n_playouts: int, cap: int, seed: int) -> dict:
    """Reach-weighted sample: {(info_set, legal): (state, player, visits)}."""
    rng = random.Random(seed)
    out: dict = {}
    for _ in range(n_playouts):
        s = game.root(rng.choice(game.deals()))
        while not game.is_terminal(s):
            p = game.current_player(s)
            legal = tuple(game.legal_actions(s))
            key = (game.info_set(s, p), legal)
            if key in out:
                out[key][2] += 1
            elif len(out) < cap:
                out[key] = [s, p, 1]
            s = game.apply(s, rng.choice(legal))
    return out


def main():
    ap = argparse.ArgumentParser(description="Leduc illegal-action taxonomy.")
    ap.add_argument("--max-infosets", type=int, default=250)
    ap.add_argument("--playouts", type=int, default=1500)
    ap.add_argument("--style", default="plain")
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    cfg = active_config()
    preset = cfg.get("llm_preset") or {}
    model = preset.get("model", "stub")
    game = make_game("leduc")
    client = make_client(preset)

    sets = sample_infosets(game, args.playouts, args.max_infosets, args.seed)
    print(f"Leduc illegal-action taxonomy: model={model} style={args.style} "
          f"info_sets={len(sets)} (reach-sampled from {args.playouts} playouts)")
    print("=" * 82)

    cat = collections.Counter()          # category -> summed mass
    cat_n = collections.Counter()        # category -> number of info sets where it applies
    by_situation: dict = collections.defaultdict(lambda: {"illegal": 0.0, "n": 0})
    rows = []
    t0 = time.time()
    for (iset, legal), (state, player, visits) in sets.items():
        system, user = build_prompt(state, player, args.style, legal)
        toks = client.chat_logprobs(system, user, prefill="Action:", top_logprobs=20,
                                    temperature=args.temp)
        per, non_action, _neutral = raw_action_mass(toks)
        illegal_actions = [a for a in (FOLD, CALL, RAISE) if a not in legal]
        illegal_mass = sum(per[a] for a in illegal_actions) + non_action

        rnd = int(state.round)
        due = abs(int(state.bets[0]) - int(state.bets[1]))
        facing = due > 0
        sit = f"round{rnd + 1}/{'facing bet' if facing else 'nothing due'}"
        by_situation[sit]["illegal"] += illegal_mass
        by_situation[sit]["n"] += 1

        if FOLD in illegal_actions:
            cat["FOLD_WHEN_FREE"] += per[FOLD]
            cat_n["FOLD_WHEN_FREE"] += 1
        if RAISE in illegal_actions:
            cat["RAISE_AT_CAP"] += per[RAISE]
            cat_n["RAISE_AT_CAP"] += 1
        cat["NON_ACTION"] += non_action
        cat_n["NON_ACTION"] += 1

        rows.append({"info_set": iset, "legal": list(legal), "visits": visits,
                     "round": rnd + 1, "facing_bet": facing,
                     "mass": {_NAME[a]: per[a] for a in per},
                     "non_action": non_action, "illegal_mass": illegal_mass})

    n = len(rows)
    total_illegal = sum(r["illegal_mass"] for r in rows) / n
    print(f"mean illegal mass over {n} info sets = {total_illegal:.4f} "
          f"({time.time() - t0:.0f}s)\n")

    print(f"{'category':<18}{'mean mass':>12}{'applies to':>12}{'mean where it applies':>24}")
    print("-" * 66)
    for c in ("FOLD_WHEN_FREE", "RAISE_AT_CAP", "NON_ACTION"):
        share_all = cat[c] / n
        where = cat[c] / cat_n[c] if cat_n[c] else 0.0
        print(f"{c:<18}{share_all:>12.4f}{cat_n[c]:>9} sets{where:>24.4f}")
    print("-" * 66)
    print(f"{'TOTAL':<18}{total_illegal:>12.4f}")
    dom = max(("FOLD_WHEN_FREE", "RAISE_AT_CAP", "NON_ACTION"), key=lambda c: cat[c])
    print(f"-> dominant failure: {dom} ({cat[dom] / max(1e-9, sum(cat.values())):.0%} of all "
          "illegal mass)")

    print(f"\n{'situation':<28}{'mean illegal mass':>20}{'info sets':>12}")
    print("-" * 60)
    for sit in sorted(by_situation):
        d = by_situation[sit]
        print(f"{sit:<28}{d['illegal'] / max(1, d['n']):>20.4f}{d['n']:>12}")

    rows.sort(key=lambda r: -r["illegal_mass"])
    print("\nworst individual info sets:")
    for r in rows[:6]:
        print(f"  {r['info_set']:<18} legal={r['legal']} illegal={r['illegal_mass']:.3f} "
              f"mass={{F:{r['mass']['FOLD']:.2f} C:{r['mass']['CALL']:.2f} "
              f"R:{r['mass']['RAISE']:.2f}}}")

    payload = {"game": "leduc", "model": model, "style": args.style, "temperature": args.temp,
               "info_sets": n, "mean_illegal_mass": total_illegal,
               "categories": {c: {"mean_mass_all": cat[c] / n, "applies_to": cat_n[c],
                                  "mean_where_applies": (cat[c] / cat_n[c]) if cat_n[c] else 0.0}
                              for c in ("FOLD_WHEN_FREE", "RAISE_AT_CAP", "NON_ACTION")},
               "dominant": dom,
               "by_situation": {k: {"mean_illegal_mass": v["illegal"] / max(1, v["n"]),
                                    "n": v["n"]} for k, v in by_situation.items()},
               "rows": rows, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"leduc_illegal_taxonomy_{model.replace('/', '_')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nsaved -> {path}")


if __name__ == "__main__":
    main()
