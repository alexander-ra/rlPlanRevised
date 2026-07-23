"""
prime_safe.py -- Prime-Safe opponent exploitation for eps-equilibrium baselines
(Jeary & Turrini 2023). Raw step Day 6, L470-479.

THE FIX IT MAKES
----------------
Ganzfried (2015) pins the safety floor to the PERFECT Nash value v*. But every real baseline
is an eps-equilibrium (abstraction, finite compute -- Step 04), so anchoring to v* is
unjustified: the baseline itself can be exploited for eps. Prime-safe lowers the floor to the
baseline's own worst-case value:

    eps   = exploitability(baseline)        = v* - worst_case_value(baseline)     (>= 0)
    floor = v* - eps                        = worst_case_value(baseline)

i.e. "never earn less than the worst case of the strategy you were going to play anyway."
We then reuse the SAME constraint-generation core (`ganzfried_solver.safe_exploit`) with this
adjusted floor.

SELF-CONTAINED eps-BASELINE
---------------------------
To get a genuine eps-equilibrium without depending on Step 04's (engine-incompatible)
abstracted strategies, we EARLY-STOP CFR: a few hundred iterations gives a strategy that is
demonstrably not yet converged, so its measured exploitability eps > 0. (Step 04's abstracted
Leduc strategy is the "real" motivation, but it lives on a different engine; using early-stop
CFR here keeps the module runnable on the shared Kuhn/Leduc engines and makes eps something we
MEASURE, never fabricate.)

Validation (raw step L561, L478): the exploitation strategy's worst-case must be >= v* - eps,
and eps must equal the measured exploitability of the abstract/early-stopped baseline.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import deps  # noqa: F401
from nash import solve_nash
from seq_form import HeroTreeplex
from safety_checker import worst_case_value, game_value
from ganzfried_solver import safe_exploit


def make_epsilon_equilibrium(game, iters: int = 300):
    """An intentionally UNDER-trained CFR strategy -> a genuine eps-equilibrium (eps > 0).
    Returns a policy callable. Increase `iters` to shrink eps toward 0 (perfect Nash)."""
    policy, _ = solve_nash(game, iters=iters)
    return policy


def measure_epsilon(game, baseline_policy, hero: int, nash_value: float) -> float:
    """eps = how exploitable the baseline is = v* - worst_case_value(baseline)  (>= 0)."""
    return nash_value - worst_case_value(game, baseline_policy, hero)


def prime_safe_exploit(game, hero: int, opp_model, baseline_policy, nash_value: float,
                       treeplex: "HeroTreeplex | None" = None, **kw) -> dict:
    """Prime-safe exploitation: floor = v* - eps(baseline). Reuses the Ganzfried core."""
    eps = measure_epsilon(game, baseline_policy, hero, nash_value)
    floor = nash_value - eps
    tp = treeplex if treeplex is not None else HeroTreeplex(game, hero)
    res = safe_exploit(game, hero, opp_model, floor=floor, treeplex=tp, **kw)
    res["method"] = "prime_safe"
    res["epsilon"] = eps
    res["nash_value"] = nash_value
    res["baseline_worst_case"] = worst_case_value(game, baseline_policy, hero)
    # sanity: the prime-safe floor equals the baseline's own worst-case value.
    return res


def _selftest():
    from engines import make_game
    from nash import solve_nash_cached
    from opponent_types import make_type_zoo
    from exploitation_metrics import exploitation_value

    print("prime_safe self-test")
    print("-" * 60)
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    v = game_value(game, nash, hero)
    zoo = make_type_zoo(game, nash_iters=30000)
    opp = zoo["TightPassive"]

    baseline = make_epsilon_equilibrium(game, iters=200)  # under-trained on purpose
    try:
        eps = measure_epsilon(game, baseline, hero, v)
        res = prime_safe_exploit(game, hero, opp, baseline, v)
    except ImportError as exc:
        print(f"SKIP ({exc})")
        return
    print(f"[kuhn] v* = {v:+.4f}; measured eps(baseline) = {eps:+.4f} (want > 0)")
    print(f"[kuhn] prime-safe floor = v*-eps = {v - eps:+.4f} "
          f"(= baseline worst-case {res['baseline_worst_case']:+.4f})")
    print(f"[kuhn] prime-safe exploitation value = {res['exploitation_value']:+.4f} "
          f"(Nash EV vs opp = {exploitation_value(game, nash, opp, hero):+.4f})")
    print(f"[kuhn] prime-safe worst-case = {res['worst_case_value']:+.4f} "
          f"(want >= v*-eps = {v - eps:+.4f})")
    print(f"[kuhn] safe={res['safe']}")


if __name__ == "__main__":
    _selftest()
