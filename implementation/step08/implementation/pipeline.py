"""
pipeline.py -- the full Step 7 -> Step 8 loop (raw step Day 9, L512-516).

    for each hand:
        play the current hero policy vs the (possibly shifting) opponent
        record the hand -> update the Step-7 opponent model
        every `refit_every` hands: rebuild the hero policy by running the chosen Step-8 SAFE
            EXPLOITATION solver against the model's current estimate

Step 07 is the SENSOR (an opponent model that consumes observations and emits a policy);
Step 08 is the ACTUATOR (a safe solver that turns that estimate into a bounded-risk strategy).
This module wires them together and measures, per method:
  - realized cumulative profit,
  - safety violations = refits whose PLAYED strategy has worst-case value below the Nash floor
    (safe methods should never violate; `full_br` will).

Methods (string ids, matching config): "nash", "full_br", "rnr_<p>", "ganzfried",
"prime_safe", "adaptation", "ses_subgame".

Reuses Step 07's play_hand / ObservationBuffer / models / schedules, and Step 08's solvers.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import time

import deps  # noqa: F401
from policies import play_hand
from observation_buffer import ObservationBuffer
from best_response import best_response_policy
from type_based_model import TypeBasedModel
from continuous_model import ContinuousModel

# Reuse Step 07's opponent schedules (stationary / switching) rather than re-implementing them.
from adaptive_exploiter import stationary, switching  # noqa: F401

from seq_form import HeroTreeplex
from safety_checker import worst_case_value, game_value
from rnr_solver import canonical_rnr
from ganzfried_solver import ganzfried_safe_exploit
from prime_safe import prime_safe_exploit
from adaptation_safety import adaptation_safe_exploit
from subgame_exploit_solver import subgame_exploit, whole_game, leduc_postflop


def make_model(name, game, hero, zoo):
    if name == "type_based":
        return TypeBasedModel(game, hero, zoo)
    if name == "continuous":
        return ContinuousModel(game, hero, prior_strength=1.0)
    raise ValueError(f"unknown Step-7 model {name!r}")


def build_hero_policy(method, game, hero, opp_model_policy, ctx):
    """Turn the model's current estimate `opp_model_policy` into a hero policy via `method`.
    `ctx` carries the shared pieces (nash, blueprint, nash_value, treeplex, predicate)."""
    tp = ctx["treeplex"]
    if method == "nash":
        return ctx["nash"]
    if method == "full_br":
        return best_response_policy(game, hero, opp_model_policy)
    if method.startswith("rnr_"):
        p = float(method.split("_", 1)[1])
        return canonical_rnr(game, hero, opp_model_policy, p, treeplex=tp)["policy"]
    if method == "ganzfried":
        return ganzfried_safe_exploit(game, hero, opp_model_policy, ctx["nash_value"],
                                      treeplex=tp)["policy"]
    if method == "prime_safe":
        return prime_safe_exploit(game, hero, opp_model_policy, ctx["blueprint"],
                                  ctx["nash_value"], treeplex=tp)["policy"]
    if method == "adaptation":
        return adaptation_safe_exploit(game, hero, opp_model_policy, ctx["blueprint"],
                                       treeplex=tp)["policy"]
    if method == "ses_subgame":
        return subgame_exploit(game, hero, opp_model_policy, ctx["blueprint"],
                               predicate=ctx["predicate"], treeplex=tp)["policy"]
    raise ValueError(f"unknown method {method!r}")


class SafeExploitPipeline:
    def __init__(self, game, hero, method, model, ctx, refit_every=200,
                 min_hands_before_exploit=100, safety_tol=1e-3):
        self.game = game
        self.hero = hero
        self.opp = 1 - hero
        self.method = method
        self.model = model
        self.ctx = ctx
        self.refit_every = refit_every
        self.min_hands_before_exploit = min_hands_before_exploit
        self.safety_tol = safety_tol

    def run(self, schedule, num_hands, rng, on_refit=None) -> dict:
        game = self.game
        deals = game.deals()
        buffer = ObservationBuffer(game, self.hero)
        hero_policy = self.ctx["nash"]  # start safe
        running = 0.0
        profits, cumulative, mode_log = [], [], []
        safety_violations = 0
        refit_worst_cases = []
        floor = self.ctx["nash_value"]

        for i in range(num_hands):
            opp_policy = schedule(i)
            pols = [None, None]
            pols[self.hero] = hero_policy
            pols[self.opp] = opp_policy
            hand = play_hand(game, pols, rng.choice(deals), rng)
            u = hand.utilities[self.hero]
            running += u
            profits.append(u)
            cumulative.append(running)
            mode_log.append(self.method if hero_policy is not self.ctx["nash"] else "safe")

            self.model.update(buffer.record(hand))

            if (i + 1) % self.refit_every == 0 and (i + 1) >= self.min_hands_before_exploit:
                t0 = time.time()
                est = self.model.predicted_policy()
                hero_policy = build_hero_policy(self.method, game, self.hero, est, self.ctx)
                wc = worst_case_value(game, hero_policy, self.hero)
                refit_worst_cases.append(wc)
                if wc < floor - self.safety_tol:
                    safety_violations += 1
                if on_refit is not None:
                    on_refit(i + 1, num_hands, time.time() - t0)

        n = max(1, num_hands)
        return {
            "game": game.name, "method": self.method, "num_hands": num_hands,
            "mean_per_hand": running / n, "profits": profits, "cumulative": cumulative,
            "mode_log": mode_log, "safety_violations": safety_violations,
            "refit_worst_cases": refit_worst_cases, "final_policy": hero_policy,
        }


def make_ctx(game, hero, nash, blueprint, nash_value, predicate=None):
    return {"nash": nash, "blueprint": blueprint, "nash_value": nash_value,
            "treeplex": HeroTreeplex(game, hero),
            "predicate": predicate or (leduc_postflop if game.name == "leduc" else whole_game)}


def _selftest():
    import random
    from engines import make_game
    from nash import solve_nash_cached
    from opponent_types import make_type_zoo
    from prime_safe import make_epsilon_equilibrium

    print("pipeline self-test")
    print("-" * 60)
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    zoo = make_type_zoo(game, nash_iters=30000)
    v = game_value(game, nash, hero)
    blueprint = make_epsilon_equilibrium(game, 200)
    ctx = make_ctx(game, hero, nash, blueprint, v)

    for method in ("full_br", "ganzfried"):
        try:
            model = make_model("continuous", game, hero, zoo)
            pipe = SafeExploitPipeline(game, hero, method, model, ctx, refit_every=200,
                                       min_hands_before_exploit=100)
            res = pipe.run(stationary(zoo["TightPassive"]), 1000, random.Random(0))
        except ImportError as exc:
            print(f"SKIP ({exc})")
            return
        print(f"[kuhn] {method:10s} mean/hand={res['mean_per_hand']:+.4f} "
              f"safety_violations={res['safety_violations']} "
              f"(PREDICT: full_br may violate; ganzfried should not)")


if __name__ == "__main__":
    _selftest()
