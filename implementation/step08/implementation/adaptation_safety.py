"""
adaptation_safety.py -- Ge et al. (2024) "adaptation safety" (raw step Day 8, L493-508).

THE RELAXED SAFETY NOTION
-------------------------
Ganzfried demands "never earn less than PERFECT Nash." Ge relaxes this to "be NO MORE
EXPLOITABLE than the blueprint you were already going to play":

    is_adaptation_safe(exploit, blueprint)  <=>  exploitability(exploit) <= exploitability(blueprint)
                                            <=>  worst_case_value(exploit) >= worst_case_value(blueprint)

Since a real blueprint is already eps-exploitable, this is strictly WEAKER than Ganzfried
safety (weaker by exactly eps = exploitability(blueprint)) and therefore ACHIEVABLE where
strict safety is not -- and it usually allows MORE exploitation.

Two entry points:
  - `is_adaptation_safe(...)`     : the standalone checker (raw step L495-498).
  - `adaptation_safe_exploit(...)`: the solver, which is just the Ganzfried core with
                                    floor = worst_case_value(blueprint) (raw step L499-501).

PITFALL (raw step L610, logged as OPEN): if the blueprint is TERRIBLE (huge exploitability),
adaptation safety is trivially satisfied by almost anything. A meaningful use needs a
reasonable baseline. We surface the blueprint's exploitability in the result so this is
visible, not hidden.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import deps  # noqa: F401
from seq_form import HeroTreeplex
from safety_checker import worst_case_value, game_value
from ganzfried_solver import safe_exploit


def is_adaptation_safe(game, exploit_policy, blueprint_policy, hero: int,
                       tolerance: float = 1e-6) -> bool:
    """True iff the exploiting strategy is no more exploitable than the blueprint."""
    wc_exploit = worst_case_value(game, exploit_policy, hero)
    wc_blueprint = worst_case_value(game, blueprint_policy, hero)
    return wc_exploit >= wc_blueprint - tolerance


def adaptation_safe_exploit(game, hero: int, opp_model, blueprint_policy,
                            treeplex: "HeroTreeplex | None" = None, **kw) -> dict:
    """Solve with the adaptation-safety floor = blueprint's worst-case value."""
    tp = treeplex if treeplex is not None else HeroTreeplex(game, hero)
    floor = worst_case_value(game, blueprint_policy, hero)
    res = safe_exploit(game, hero, opp_model, floor=floor, treeplex=tp, **kw)
    res["method"] = "adaptation"
    res["blueprint_worst_case"] = floor
    return res


def compare_safety_notions(game, hero, opp_model, nash_policy, blueprint_policy,
                           nash_value: float | None = None) -> dict:
    """Head-to-head (raw step L502-508): Ganzfried (floor v*) vs adaptation (floor blueprint
    worst-case). Adaptation's weaker floor should permit >= exploitation. Returns both
    results plus the blueprint's own exploitability (to expose the 'bad blueprint' pitfall)."""
    from ganzfried_solver import ganzfried_safe_exploit
    tp = HeroTreeplex(game, hero)
    v = nash_value if nash_value is not None else game_value(game, nash_policy, hero)
    ganz = ganzfried_safe_exploit(game, hero, opp_model, v, treeplex=tp)
    adapt = adaptation_safe_exploit(game, hero, opp_model, blueprint_policy, treeplex=tp)
    return {
        "game": game.name, "hero": hero, "nash_value": v,
        "blueprint_exploitability": v - worst_case_value(game, blueprint_policy, hero),
        "ganzfried": {"exploitation_value": ganz["exploitation_value"],
                      "worst_case_value": ganz["worst_case_value"], "safe": ganz["safe"]},
        "adaptation": {"exploitation_value": adapt["exploitation_value"],
                       "worst_case_value": adapt["worst_case_value"], "safe": adapt["safe"]},
    }


def _selftest():
    from engines import make_game
    from nash import solve_nash_cached
    from opponent_types import make_type_zoo
    from best_response import best_response_policy
    from prime_safe import make_epsilon_equilibrium

    print("adaptation_safety self-test")
    print("-" * 60)
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    v = game_value(game, nash, hero)
    zoo = make_type_zoo(game, nash_iters=30000)
    opp = zoo["TightPassive"]
    blueprint = make_epsilon_equilibrium(game, iters=200)  # a realistic imperfect blueprint

    br = best_response_policy(game, hero, opp)
    print(f"[kuhn] is_adaptation_safe(Nash, blueprint) = "
          f"{is_adaptation_safe(game, nash, blueprint, hero)} (want True: Nash <= its own expl.)")
    print(f"[kuhn] is_adaptation_safe(full BR, blueprint) = "
          f"{is_adaptation_safe(game, br, blueprint, hero)} (want False: BR is exploitable)")
    try:
        cmp = compare_safety_notions(game, hero, opp, nash, blueprint, v)
    except ImportError as exc:
        print(f"SKIP solver ({exc})")
        return
    print(f"[kuhn] blueprint exploitability = {cmp['blueprint_exploitability']:+.4f}")
    print(f"[kuhn] Ganzfried  EV={cmp['ganzfried']['exploitation_value']:+.4f} "
          f"wc={cmp['ganzfried']['worst_case_value']:+.4f} safe={cmp['ganzfried']['safe']}")
    print(f"[kuhn] Adaptation EV={cmp['adaptation']['exploitation_value']:+.4f} "
          f"wc={cmp['adaptation']['worst_case_value']:+.4f} safe={cmp['adaptation']['safe']}")
    print("expect: adaptation EV >= Ganzfried EV (weaker floor -> more exploitation).")


if __name__ == "__main__":
    _selftest()
