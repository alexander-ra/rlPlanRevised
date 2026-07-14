"""
safety_checker.py -- the safety diagnostics (raw step Day 1, L407-411).

Safety in this step is a property of the HERO's strategy: how much can a worst-case adversary
punish it? We reuse Step 07's EXACT best response as the worst-case oracle -- everything here
is a thin, exact wrapper, no sampling.

Definitions (hero is a seat, 0 or 1; zero-sum):
  - worst_case_value(sigma)  = hero's guaranteed EV = -BR_opp(sigma)   (opponent best-responds)
  - exploitability(sigma)    = baseline_value - worst_case_value(sigma)  (>= 0; 0 = as safe as
                               the baseline; the "how far below my anchor can I be dragged")
  - is_safe(sigma, floor)    = worst_case_value(sigma) >= floor - tolerance
  - safety_margin(sigma, floor) = worst_case_value(sigma) - floor    (remaining safety budget)

The `floor` is the safety notion, injected by the caller:
  - Ganzfried: floor = Nash game value v*.
  - prime-safe: floor = v* - eps.
  - adaptation: floor = worst_case_value(blueprint)  (equivalently exploitability<=blueprint's).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import deps  # noqa: F401
from best_response import best_response_value, exact_value


def seat_order(hero: int, hero_policy, opp_policy):
    """Return (policy0, policy1) for exact_value given the hero's seat."""
    return (hero_policy, opp_policy) if hero == 0 else (opp_policy, hero_policy)


def game_value(game, nash_policy, hero: int = 0) -> float:
    """Equilibrium value from the hero's seat (Kuhn P0 = -1/18)."""
    return exact_value(game, hero, *seat_order(hero, nash_policy, nash_policy))


def worst_case_value(game, strategy, hero: int = 0) -> float:
    """Hero's worst-case EV: the opponent best-responds to the fixed hero strategy.
    In zero-sum this is -(opponent's best-response value against `strategy`)."""
    opp = 1 - hero
    return -best_response_value(game, opp, strategy)


def exploitability(game, strategy, hero: int, baseline_value: float) -> float:
    """How far the hero's worst-case sits below `baseline_value` (>= 0 means at/at-risk of the
    baseline; negative means strictly safer than the baseline)."""
    return baseline_value - worst_case_value(game, strategy, hero)


def is_safe(game, strategy, hero: int, floor: float, tolerance: float = 1e-3) -> bool:
    """True iff the hero's worst-case EV meets the safety `floor` (within tolerance)."""
    return worst_case_value(game, strategy, hero) >= floor - tolerance


def safety_margin(game, strategy, hero: int, floor: float) -> float:
    """Remaining safety budget: worst_case_value - floor (>= 0 safe; < 0 violates)."""
    return worst_case_value(game, strategy, hero) - floor


def _selftest():
    from engines import make_game
    from nash import solve_nash_cached
    from opponent_types import make_type_zoo
    from best_response import best_response_policy

    print("safety_checker self-test")
    print("-" * 60)
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    v = game_value(game, nash, hero)
    zoo = make_type_zoo(game, nash_iters=30000)
    br = best_response_policy(game, hero, zoo["TightPassive"])

    print(f"[kuhn] game value (P0) = {v:+.4f} (want ~ -0.0556)")
    print(f"[kuhn] Nash worst-case = {worst_case_value(game, nash, hero):+.4f} "
          f"(want ~ game value; Nash is unexploitable)")
    print(f"[kuhn] Nash is_safe(floor=v) = {is_safe(game, nash, hero, v)} (want True)")
    print(f"[kuhn] BR-to-TightPassive worst-case = {worst_case_value(game, br, hero):+.4f} "
          f"(want < game value: BR is exploitable)")
    print(f"[kuhn] BR is_safe(floor=v) = {is_safe(game, br, hero, v)} "
          f"(want False -- naive BR is NOT safe)")
    print(f"[kuhn] BR safety_margin(floor=v) = {safety_margin(game, br, hero, v):+.4f} "
          f"(want < 0)")


if __name__ == "__main__":
    _selftest()
