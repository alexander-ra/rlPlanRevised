"""
leduc_llm.py  [SUP]  -- scouting: can an LLM play Leduc? (Leduc Stage 1-lite)

SCOPE / WHY THIS IS DELIBERATELY CHEAP
--------------------------------------
LLM play is scouting for this thesis, not a core contribution, so this deliberately avoids the
expensive Leduc machinery:

  - NO exact exploitability. That lives in step03, whose package is literally named `cfr` and
    collides with step02's (see deps.py); resolving it is Stage 1 work and buys little here.
    Instead we score by ACTUAL PERFORMANCE -- chips/hand vs a near-Nash opponent and vs the step07
    zoo -- which is honest, needs no new metric, and is the same yardstick `leduc_stage0.py` used
    for the DT, so LLM and DT numbers are directly comparable.
  - NO full 936-info-set enumeration. We query the model LAZILY, only at info sets that actually
    come up in play, and cache by canonical info-set string. Reach probability does the subsetting
    for free: common decisions get queried, rare ones never do. The run reports how many distinct
    info sets were actually needed -- which answers "do you have to cover all 936?" empirically.

LEDUC vs KUHN -- what had to change
-----------------------------------
  - THREE actions (0=FOLD, 1=CALL/CHECK, 2=RAISE) instead of two, with a DIFFERENT verb mapping:
    in Kuhn "check"->PASS and "bet"->BET; here "check"->CALL(1) and "bet"->RAISE(2). Reusing the
    Kuhn map would silently mis-map every check.
  - Legal actions VARY (fold is illegal unless facing a raise; raise is illegal at the cap), so the
    action distribution must be masked -- the same bug class fixed for the DT in Stage 0.
  - TWO betting rounds with a revealed board card, and a pair-beats-high-card showdown rule.
  - Bet sizing: ante 1, raise 2 in round 1, raise 4 in round 2, max 2 raises per round
    (=> payoffs {+-1,+-3,...,+-13}, matching the measured ladder).

Usage:  python leduc_llm.py [--hands 600] [--style plain]
Writes results/leduc_llm_<model>.json

NOTE: added during the RUN session. All numbers are MEASUREMENTS.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import time

import numpy as np

import deps  # noqa: F401
from engines import make_game
from policies import sample_action
from opponent_types import make_type_zoo

from config import active_config
from llm_agent import make_client
from logprob_policy import _NEUTRAL, map_token
from trajectory_dataset import make_cfr_policy

FOLD, CALL, RAISE = 0, 1, 2

# RUN-SESSION FIX (2026-07-27): Leduc's 6-card deck uses card ids 0..5, NOT ranks 0..2 --
# `rank = card // 2`, so 0,1=Jack, 2,3=Queen, 4,5=King (matches state_encoding.py:167). The first
# deal happens to be (0,1,2), so an id->name map looked fine until a King (id 4 or 5) came up and
# raised KeyError. It also means "does my card pair the board" must compare RANKS, not ids --
# comparing ids would have said a Jack never pairs the other Jack.
_RANK = {0: "Jack", 1: "Queen", 2: "King"}


def rank_of(card: int) -> int:
    return int(card) // 2

# Leduc verb map -- NOT the Kuhn one. "check" is a CALL here, "bet" is a RAISE.
_LEDUC_VERB = {
    "fold": FOLD,
    "call": CALL, "check": CALL,
    "raise": RAISE, "bet": RAISE, "allin": RAISE, "all-in": RAISE,
}

LEDUC_RULES = (
    "You are playing Leduc Hold'em, a simplified poker game.\n"
    "Deck: 6 cards -- two Jacks, two Queens, two Kings (Jack lowest, King highest).\n"
    "Each player antes 1 chip and is dealt ONE private card. There are two betting rounds.\n"
    "After the first round, ONE community card is revealed, then the second round is played.\n"
    "Actions: FOLD (give up the pot), CALL (match the current bet; if nothing is due this is a "
    "CHECK), RAISE (increase the bet).\n"
    "A raise costs 2 chips in the first round and 4 chips in the second. At most 2 raises per "
    "round.\n"
    "Showdown: if your private card PAIRS the community card you win (a pair beats any unpaired "
    "hand). Otherwise the higher private card wins. Equal cards split.\n"
    "Your goal is to maximise chips won over many hands."
)

_STYLE = {
    "plain": ("Reply with ONLY your action on a single line: 'Action: FOLD', 'Action: CALL' or "
              "'Action: RAISE'."),
    "cot": ("Think step by step about your hand strength, the community card, the pot and what "
            "your opponent's actions imply, THEN end your reply with a final line exactly: "
            "'Action: FOLD', 'Action: CALL' or 'Action: RAISE'."),
}


def describe(state, player: int) -> str:
    """Natural-language situation description from `player`'s point of view."""
    card = _RANK[rank_of(state.cards[player])]
    lines = [f"Your private card: {card}."]
    rnd = int(state.round)
    if rnd == 0:
        lines.append("This is the FIRST betting round; no community card is showing yet.")
    else:
        lines.append(f"The community card is the {_RANK[rank_of(state.community)]}. "
                     "This is the SECOND (final) betting round.")
        if rank_of(state.cards[player]) == rank_of(state.community):
            lines.append("Your card PAIRS the community card -- this is the strongest possible "
                         "holding.")
    hist = state.history
    if not hist:
        lines.append("You act first, before any bets.")
    else:
        parts, actor = [], 0
        for ch in hist:
            if ch == "/":
                parts.append("-- community card revealed --")
                actor = 0
                continue
            who = "You" if actor % 2 == (len(_round_actions(hist)) % 2) else "Opponent"
            parts.append(f"{who} {'raised' if ch == 'r' else 'called/checked'}")
            actor += 1
        lines.append("Betting so far: " + "; ".join(parts) + ".")
    pot = int(state.bets[0]) + int(state.bets[1])
    due = abs(int(state.bets[0]) - int(state.bets[1]))
    lines.append(f"Pot: {pot} chips." + (f" You must put in {due} more to call."
                                         if due else " Nothing is due -- you may check."))
    return "\n".join(lines)


def _round_actions(hist: str) -> str:
    return hist.split("/")[-1]


def build_prompt(state, player: int, style: str, legal) -> tuple:
    names = {FOLD: "FOLD", CALL: "CALL", RAISE: "RAISE"}
    allowed = ", ".join(names[a] for a in legal)
    user = describe(state, player) + f"\nLegal actions right now: {allowed}.\n" + _STYLE[style]
    return LEDUC_RULES, user


def parse_leduc_action(text: str, legal):
    low = text.lower()
    if "<think>" in low:
        if "</think>" not in low:
            return None
        low = low.split("</think>")[-1]
    m = re.findall(r"action\s*[:\-/=]\s*([a-z\-]+)", low)
    cands = m or re.findall(r"\b(fold|call|check|raise|bet|all-?in)\b", low)[-1:]
    for tok in reversed(cands):
        tok = tok.replace("all-in", "allin")
        if tok in _LEDUC_VERB and _LEDUC_VERB[tok] in legal:
            return _LEDUC_VERB[tok]
    return None


def leduc_action_distribution(tokens, legal):
    """Sum logprob mass per legal action over surface forms; mask + renormalise."""
    per = {a: 0.0 for a in legal}
    unmapped = 0.0
    for tok, prob in tokens:
        norm = re.sub(r"[^a-z\-]", "", tok.strip().lower()).replace("all-in", "allin")
        a = map_token(norm, _LEDUC_VERB)   # prefix-aware: ' RA'->RAISE, ' F'->FOLD
        if a is not None:
            if a in per:
                per[a] += prob
            else:
                unmapped += prob      # a real poker verb, illegal in THIS state
        elif not _NEUTRAL.match(tok):
            unmapped += prob
    tot = sum(per.values())
    if tot <= 0:
        return {a: 1.0 / len(legal) for a in legal}, unmapped
    return {a: p / tot for a, p in per.items()}, unmapped


class LeducLLMPolicy:
    """Lazy, cached, logprob-based Leduc policy. One model call per NEW info set."""

    def __init__(self, client, style: str = "plain", temperature: float = 0.7):
        self.client = client
        self.style = style
        self.temperature = temperature
        self.cache: dict = {}
        self.calls = 0
        self.unmapped = 0.0

    def __call__(self, game, state):
        player = game.current_player(state)
        legal = tuple(game.legal_actions(state))
        key = (game.info_set(state, player), legal)
        if key not in self.cache:
            system, user = build_prompt(state, player, self.style, legal)
            toks = self.client.chat_logprobs(system, user, prefill="Action:", top_logprobs=20,
                                             temperature=self.temperature)
            dist, um = leduc_action_distribution(toks, legal)
            self.cache[key] = dist
            self.calls += 1
            self.unmapped += um
        return dict(self.cache[key])

    @property
    def mean_unmapped(self) -> float:
        return self.unmapped / self.calls if self.calls else 0.0


def play(game, hero, opp, hands: int, seed: int):
    rng = random.Random(seed)
    deals = game.deals()
    utils = []
    for h in range(hands):
        hs = h % 2
        pols = [None, None]
        pols[hs] = hero
        pols[1 - hs] = opp
        state = game.root(rng.choice(deals))
        while not game.is_terminal(state):
            p = game.current_player(state)
            state = game.apply(state, sample_action(pols[p](game, state), rng))
        utils.append(game.utility(state, hs))
    a = np.array(utils, dtype=np.float64)
    return float(a.mean()), float(a.std() / max(1, len(a)) ** 0.5)


def main():
    ap = argparse.ArgumentParser(description="Leduc LLM scouting run.")
    ap.add_argument("--hands", type=int, default=600)
    ap.add_argument("--style", default="plain")
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--cfr-iters", type=int, default=20000)
    ap.add_argument("--zoo-hands", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    cfg = active_config()
    preset = cfg.get("llm_preset") or {}
    model = preset.get("model", "stub")
    game = make_game("leduc")
    nash_policy, _ = make_cfr_policy(game, args.cfr_iters, args.seed)

    print(f"Leduc LLM scouting: model={model} style={args.style} hands={args.hands}")
    print("=" * 78)
    hero = LeducLLMPolicy(make_client(preset), args.style, args.temp)

    t0 = time.time()
    mean, se = play(game, hero, nash_policy, args.hands, args.seed)
    dt_ref = -0.4542   # leduc_stage0.py, DT at its modal target, vs the same near-Nash opponent
    print(f"vs near-Nash : {mean:+.4f} +/- {se:.4f} chips/hand  ({args.hands} hands, "
          f"seats alternated)")
    print(f"   reference : DT (return-conditioned, modal target) {dt_ref:+.4f}; "
          f"Nash vs Nash = 0 by construction")
    print(f"   info sets queried: {hero.calls} distinct (of 936 total = "
          f"{hero.calls / 936:.1%}) in {time.time() - t0:.0f}s")
    print(f"   unmapped logprob mass: {hero.mean_unmapped:.4f}")

    zoo = make_type_zoo(game, include_nash=False, include_random=True)
    print(f"\nvs the exploitable zoo ({args.zoo_hands} hands each):")
    print(f"{'opponent':<16}{'LLM':>12}{'+/- se':>9}{'Nash':>12}")
    print("-" * 49)
    rows = {}
    for name, pol in zoo.items():
        lm, lse = play(game, hero, pol, args.zoo_hands, args.seed)
        nm, _ = play(game, nash_policy, pol, 20000, args.seed)
        rows[name] = {"llm": lm, "llm_se": lse, "nash": nm}
        print(f"{name:<16}{lm:>12.4f}{lse:>9.4f}{nm:>12.4f}")
    print("-" * 49)
    llm_mean = float(np.mean([r["llm"] for r in rows.values()]))
    nash_mean = float(np.mean([r["nash"] for r in rows.values()]))
    print(f"{'MEAN':<16}{llm_mean:>12.4f}{'':>9}{nash_mean:>12.4f}")
    print(f"\ntotal distinct info sets queried: {hero.calls} of 936 "
          f"({hero.calls / 936:.1%}) -- lazy caching means reach probability does the subsetting.")

    payload = {"game": "leduc", "model": model, "style": args.style, "temperature": args.temp,
               "hands_vs_nash": args.hands, "vs_nash_chips_per_hand": mean, "vs_nash_se": se,
               "dt_reference": dt_ref, "info_sets_queried": hero.calls, "info_sets_total": 936,
               "mean_unmapped_mass": hero.mean_unmapped, "zoo": rows,
               "zoo_mean_llm": llm_mean, "zoo_mean_nash": nash_mean,
               "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"leduc_llm_{model.replace('/', '_')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"saved -> {path}")


if __name__ == "__main__":
    main()
