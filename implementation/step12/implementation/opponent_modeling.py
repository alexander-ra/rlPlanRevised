"""
opponent_modeling.py  [CORE]  -- does the LLM actually LEARN an opponent? (experiment B5)

WHAT WAS WRONG WITH THE OLD "ADAPTATION" NUMBER
-----------------------------------------------
`evaluation.opponent_adaptation` hands the model a SENTENCE describing its opponent ("calls almost
every bet and never folds") and checks whether its bluff rate moves. That measures
instruction-following, not opponent modelling -- the model is told the answer. Everything else in
this step is likewise static: `strategy_extraction` queries each info set independently, so the
agent never sees a previous hand, an outcome, or a showdown.

WHAT THIS DOES INSTEAD
----------------------
Plays a real SESSION of N hands against a fixed zoo archetype with the observed history of previous
hands in context -- cards, actions, showdowns, results -- and nothing else. No description of the
opponent is given. Then asks whether play drifts toward the exploiting response.

This is the actual behavioural-adaptation experiment (thesis contribution #1). It routes the session
log through the agent's existing `opponent_profile` slot, so `llm_agent` needs no changes.

THE METRIC: exploitation gap closed
-----------------------------------
Against a fixed archetype there are two reference win rates, both exactly computable:

    nash_wr - Nash-CFR's chips/hand   (unexploitative floor: takes only what is given)
    br_wr   - the exact best response (step07 `best_response_policy`): the ceiling

    gap_closed = (hero_wr - nash_wr) / (br_wr - nash_wr)

    0.0  = plays like Nash, learns nothing about this opponent
    1.0  = plays like the exact best response, fully exploits it
    <0   = worse than Nash, i.e. actively mis-adapting

We report it for the first vs the second half of the session, so LEARNING (a rising gap) is
separable from a fixed exploitative prior (a flat but positive gap). That distinction is the whole
point: a model that starts exploitative is not adapting, it is just loose.

COST: every decision is a live call (the context changes each hand, so nothing can be cached) --
~1.5 calls/hand. Budget ~N*1.5 calls per opponent.

Usage:  python opponent_modeling.py [--hands 60] [--opponents AlwaysPass,AlwaysBet,TightPassive]
Writes results/opponent_modeling_<model>.json

NOTE: added during the RUN session. All numbers are MEASUREMENTS.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time

import deps  # noqa: F401
from engines import make_game
from policies import sample_action
from opponent_types import make_type_zoo
from best_response import best_response_policy

from config import active_config
from llm_agent import make_client, KuhnPokerLLMAgent, _PASS, _BET
from trajectory_dataset import make_cfr_policy

_CARD = {1: "Jack", 2: "Queen", 3: "King"}
HERO_SEAT = 0   # fixed so the session narrative ("you act first") stays coherent; all baselines
                # below are computed in the SAME seat, so the comparison is apples-to-apples.


def describe_hand(idx: int, hero_card: int, opp_card: int, actions: list,
                  hero_util: float, showdown: bool) -> str:
    """One line of session history, from the hero's point of view."""
    parts = []
    for i, a in enumerate(actions):
        who = "You" if i % 2 == HERO_SEAT else "Opponent"
        parts.append(f"{who} {'bet' if a == _BET else 'checked/passed'}")
    tail = (f" Showdown: opponent had the {_CARD[opp_card]}." if showdown
            else " Opponent's card was not revealed.")
    res = f" You {'won' if hero_util > 0 else 'lost'} {abs(hero_util):.0f} chip(s)."
    return f"Hand {idx}: You held the {_CARD[hero_card]}. " + "; ".join(parts) + "." + tail + res


def history_text(lines: list, max_hands: int = 20) -> str | None:
    if not lines:
        return None
    shown = lines[-max_hands:]
    return ("Here is what has happened so far against THIS SAME opponent "
            "(use it to infer their tendencies and exploit them):\n" + "\n".join(shown))


def play_session(game, agent, opp_policy, n_hands: int, seed: int = 0,
                 max_hands_in_context: int = 20) -> dict:
    rng = random.Random(seed)
    deals = game.deals()
    lines, per_hand = [], []
    for h in range(n_hands):
        deal = rng.choice(deals)
        state = game.root(deal)
        actions = []
        while not game.is_terminal(state):
            p = game.current_player(state)
            if p == HERO_SEAT:
                card = int(state.cards[p])
                a, _raw, _ok = agent.act(card, state.history,
                                         tuple(game.legal_actions(state)),
                                         opponent_profile=history_text(lines,
                                                                       max_hands_in_context))
            else:
                a = sample_action(opp_policy(game, state), rng)
            actions.append(a)
            state = game.apply(state, a)
        util = game.utility(state, HERO_SEAT)
        showdown = abs(util) == 2 or state.history == "pp"
        hero_card, opp_card = int(deal[HERO_SEAT]), int(deal[1 - HERO_SEAT])
        lines.append(describe_hand(h + 1, hero_card, opp_card, actions, util, showdown))
        per_hand.append({"hand": h + 1, "hero_card": hero_card, "opp_card": opp_card,
                         "actions": actions, "utility": util, "deal": deal})
    return {"per_hand": per_hand, "mean": sum(x["utility"] for x in per_hand) / max(1, len(per_hand)),
            "deals": [x["deal"] for x in per_hand]}


def exact_ev(game, deal, hero_policy, opp_policy) -> float:
    """EXACT expected chips for the hero on one deal -- full tree expectation, no sampling.

    RUN-SESSION FIX (2026-07-27). The first version sampled the baselines over their OWN random
    deals while the hero played a different 60-deal sequence. With Kuhn's per-hand std ~1.2 that
    left an SE of ~0.155 on a 60-hand session -- comparable to the entire Nash->BR span -- and the
    unpaired deal luck produced `gap_closed` values of +2.18 and +1.74, i.e. the hero apparently
    BEATING the exact best-response ceiling, which is impossible. (Checked by hand vs AlwaysBet:
    K->+2, Q->0, J->-1 gives a true ceiling of +0.333, matching the computed BR of +0.3387, so the
    ceiling was right and the hero's number was the artefact.)

    Baselines are now computed EXACTLY and on the HERO'S OWN realised deal sequence, which removes
    both sampling noise and deal luck from the comparison.
    """
    def rec(state, reach):
        if game.is_terminal(state):
            return game.utility(state, HERO_SEAT) * reach
        p = game.current_player(state)
        pol = hero_policy if p == HERO_SEAT else opp_policy
        total = 0.0
        for a, pr in pol(game, state).items():
            if pr > 0:
                total += rec(game.apply(state, a), reach * pr)
        return total
    return rec(game.root(deal), 1.0)


def baseline_on_deals(game, hero_policy, opp_policy, deals: list) -> float:
    """Exact mean EV over the hero's actual deal sequence (paired, zero variance)."""
    return sum(exact_ev(game, d, hero_policy, opp_policy) for d in deals) / max(1, len(deals))


def main():
    ap = argparse.ArgumentParser(description="B5: in-context opponent modelling.")
    ap.add_argument("--hands", type=int, default=60)
    ap.add_argument("--opponents", default="AlwaysPass,AlwaysBet,TightPassive")
    ap.add_argument("--style", default="cot")
    ap.add_argument("--temp", type=float, default=0.7)
    ap.add_argument("--context-hands", type=int, default=20)
    ap.add_argument("--baseline-hands", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    cfg = active_config()
    game = make_game(cfg["game"])
    preset = cfg.get("llm_preset") or {}
    model = preset.get("model", "stub")
    zoo = make_type_zoo(game, include_nash=False, include_random=True)
    wanted = [o.strip() for o in args.opponents.split(",") if o.strip()]
    missing = [o for o in wanted if o not in zoo]
    if missing:
        raise SystemExit(f"Unknown opponents {missing}; available: {sorted(zoo)}")

    nash_policy, _ = make_cfr_policy(game, max(cfg["cfr_iters"], 50000), cfg["seed"])

    print(f"B5 opponent modelling: model={model} hands={args.hands} "
          f"opponents={wanted} context={args.context_hands} hands")
    print("=" * 82)

    import statistics
    rows = {}
    for opp_name in wanted:
        opp_pol = zoo[opp_name]
        br_pol = best_response_policy(game, HERO_SEAT, opp_pol)

        agent = KuhnPokerLLMAgent(make_client(preset), prompt_style=args.style,
                                  temperature=args.temp)
        sess = play_session(game, agent, opp_pol, args.hands, args.seed, args.context_hands)
        utils = [x["utility"] for x in sess["per_hand"]]
        deals = sess["deals"]

        # PAIRED, EXACT baselines on the hero's OWN deal sequence (see exact_ev docstring).
        nash_wr = baseline_on_deals(game, nash_policy, opp_pol, deals)
        br_wr = baseline_on_deals(game, br_pol, opp_pol, deals)

        half = len(utils) // 2
        first_wr = sum(utils[:half]) / max(1, half)
        second_wr = sum(utils[half:]) / max(1, len(utils) - half)
        nash_1 = baseline_on_deals(game, nash_policy, opp_pol, deals[:half])
        nash_2 = baseline_on_deals(game, nash_policy, opp_pol, deals[half:])
        br_1 = baseline_on_deals(game, br_pol, opp_pol, deals[:half])
        br_2 = baseline_on_deals(game, br_pol, opp_pol, deals[half:])

        se = statistics.stdev(utils) / (len(utils) ** 0.5) if len(utils) > 1 else float("nan")
        span = br_wr - nash_wr

        def closed(wr, n_wr, b_wr):
            s = b_wr - n_wr
            return (wr - n_wr) / s if abs(s) > 1e-9 else float("nan")

        gc = closed(sess["mean"], nash_wr, br_wr)
        gc1 = closed(first_wr, nash_1, br_1)
        gc2 = closed(second_wr, nash_2, br_2)
        se_gc = se / abs(span) if abs(span) > 1e-9 else float("nan")

        rows[opp_name] = {
            "nash_winrate_exact": nash_wr, "br_winrate_exact": br_wr,
            "hero_winrate": sess["mean"], "hero_se": se,
            "first_half_winrate": first_wr, "second_half_winrate": second_wr,
            "gap_closed_overall": gc, "gap_closed_se": se_gc,
            "gap_closed_first_half": gc1, "gap_closed_second_half": gc2,
            "learning_delta": gc2 - gc1,
            "exceeds_ceiling": bool(sess["mean"] > br_wr + 2 * se),
            "illegal_rate": agent.stats.illegal_rate(), "calls": agent.stats.calls,
        }
        r = rows[opp_name]
        print(f"\n--- vs {opp_name} ---")
        print(f"  Nash {nash_wr:+.4f} | BR ceiling {br_wr:+.4f} | hero {sess['mean']:+.4f} "
              f"+/- {se:.4f} chips/hand  (exact paired baselines on the hero's own deals)")
        print(f"  gap closed: overall {gc:+.2f} +/- {se_gc:.2f}   "
              f"first half {gc1:+.2f} -> second half {gc2:+.2f}  (learning {gc2 - gc1:+.2f})")
        if r["exceeds_ceiling"]:
            print("  !! hero exceeds the BR ceiling by >2 SE -- IMPOSSIBLE, investigate before "
                  "reporting (do not treat as a finding)")
        print(f"  illegal {r['illegal_rate']:.1%} over {r['calls']} calls")

    print("\n" + "=" * 82)
    mean_closed = sum(r["gap_closed_overall"] for r in rows.values()) / len(rows)
    mean_learn = sum(r["learning_delta"] for r in rows.values()) / len(rows)
    print(f"mean gap closed = {mean_closed:+.2f}   mean learning (2nd half - 1st) = {mean_learn:+.2f}")
    if mean_learn > 0.15:
        print("-> Evidence of IN-CONTEXT LEARNING: exploitation improves within the session.")
    elif mean_closed > 0.15:
        print("-> Exploitative but NOT learning: a fixed loose prior, flat across the session.")
    else:
        print("-> No meaningful exploitation of these opponents from observed play alone.")

    payload = {"model": model, "style": args.style, "temperature": args.temp,
               "hands": args.hands, "context_hands": args.context_hands,
               "hero_seat": HERO_SEAT, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "mean_gap_closed": mean_closed, "mean_learning_delta": mean_learn,
               "opponents": rows}
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"opponent_modeling_{model.replace('/', '_')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nsaved -> {path}")


if __name__ == "__main__":
    main()
