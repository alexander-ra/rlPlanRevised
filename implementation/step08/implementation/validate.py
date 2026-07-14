"""
Validation harness for Step 08 -- the checks that decide whether the implementation is
actually CORRECT (not merely running). Encodes the raw step's validation targets (L558-564).

Run it yourself:  python validate.py
Each check prints PASS / FAIL / SKIP with the observed numbers. Sizes are kept small (Kuhn)
so the whole thing finishes quickly. The EXPECTED outcomes are described (as predictions) in
README.md; this script reports what actually happened when you run it.

Every check is wrapped so an exception becomes a FAIL with its message rather than aborting
the run -- handy while debugging the LP/solver modules. Checks needing numpy/scipy SKIP
cleanly if those are absent.

NOTE (per implementation/WORKFLOW.md): written by the agent but NOT executed by it.
"""

from __future__ import annotations

import deps  # noqa: F401
from engines import make_game
from nash import solve_nash_cached
from opponent_types import make_type_zoo
from best_response import best_response_value

from seq_form import HeroTreeplex
from safety_checker import game_value, worst_case_value
from exploitation_metrics import exploitation_value

_HAS_SCIPY = None


def _scipy_ok():
    global _HAS_SCIPY
    if _HAS_SCIPY is None:
        try:
            import scipy  # noqa: F401
            import numpy  # noqa: F401
            _HAS_SCIPY = True
        except ImportError:
            _HAS_SCIPY = False
    return _HAS_SCIPY


# --- checks (each returns (status_bool_or_None, detail)) -----------------------------
def check_seq_form_br_matches_exact():
    if not _scipy_ok():
        return None, "numpy/scipy not installed -> SKIP"
    game = make_game("kuhn")
    zoo = make_type_zoo(game, include_nash=False)
    opp = zoo["TightPassive"]
    ok = True
    details = []
    for hero in (0, 1):
        tp = HeroTreeplex(game, hero)
        lp_val, _ = tp.full_best_response(opp)
        exact = best_response_value(game, hero, opp)
        ok = ok and abs(lp_val - exact) < 1e-6
        details.append(f"hero{hero} LP={lp_val:+.5f} exact={exact:+.5f}")
    return ok, "; ".join(details) + " (want match < 1e-6)"


def check_rnr_endpoints():
    if not _scipy_ok():
        return None, "numpy/scipy not installed -> SKIP"
    from rnr_solver import canonical_rnr
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    zoo = make_type_zoo(game, nash_iters=30000)
    opp = zoo["TightPassive"]
    v = game_value(game, nash, hero)
    br_val = best_response_value(game, hero, opp)

    r0 = canonical_rnr(game, hero, opp, 0.0)
    r1 = canonical_rnr(game, hero, opp, 1.0)
    expl0 = v - r0["worst_case_value"]          # p=0 -> should be ~0 (Nash-safe)
    ev1 = r1["exploitation_value"]              # p=1 -> should be ~ full BR
    ok = abs(expl0) < 0.02 and abs(ev1 - br_val) < 0.02
    return ok, (f"p=0 exploitability={expl0:+.4f} (want ~0); "
                f"p=1 EV={ev1:+.4f} vs full BR={br_val:+.4f} (want ~equal)")


def check_ganzfried_safe_and_profitable():
    if not _scipy_ok():
        return None, "numpy/scipy not installed -> SKIP"
    from ganzfried_solver import ganzfried_safe_exploit
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    zoo = make_type_zoo(game, nash_iters=30000)
    opp = zoo["TightPassive"]
    v = game_value(game, nash, hero)
    res = ganzfried_safe_exploit(game, hero, opp, v)
    nash_ev = exploitation_value(game, nash, opp, hero)
    safe = res["worst_case_value"] >= v - 0.001
    profitable = res["exploitation_value"] >= nash_ev - 1e-6
    return safe and profitable, (f"worst-case={res['worst_case_value']:+.4f} vs v*={v:+.4f} "
                                 f"(want >= within 0.001); EV={res['exploitation_value']:+.4f} "
                                 f">= Nash EV {nash_ev:+.4f}")


def check_prime_safe_floor():
    if not _scipy_ok():
        return None, "numpy/scipy not installed -> SKIP"
    from prime_safe import prime_safe_exploit, make_epsilon_equilibrium
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    zoo = make_type_zoo(game, nash_iters=30000)
    opp = zoo["TightPassive"]
    v = game_value(game, nash, hero)
    baseline = make_epsilon_equilibrium(game, 200)
    res = prime_safe_exploit(game, hero, opp, baseline, v)
    eps = res["epsilon"]
    floor = v - eps
    ok = eps > 1e-4 and res["worst_case_value"] >= floor - 0.001
    return ok, (f"eps={eps:+.4f} (want > 0); floor=v*-eps={floor:+.4f}; "
                f"worst-case={res['worst_case_value']:+.4f} (want >= floor)")


def check_adaptation_safety_inequality():
    if not _scipy_ok():
        return None, "numpy/scipy not installed -> SKIP"
    from adaptation_safety import adaptation_safe_exploit, is_adaptation_safe
    from prime_safe import make_epsilon_equilibrium
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    zoo = make_type_zoo(game, nash_iters=30000)
    opp = zoo["TightPassive"]
    v = game_value(game, nash, hero)
    blueprint = make_epsilon_equilibrium(game, 200)
    res = adaptation_safe_exploit(game, hero, opp, blueprint)
    ok = is_adaptation_safe(game, res["policy"], blueprint, hero, tolerance=1e-3)
    expl_exploit = v - res["worst_case_value"]
    expl_bp = v - worst_case_value(game, blueprint, hero)
    return ok, (f"exploitability(exploit)={expl_exploit:+.4f} <= "
                f"exploitability(blueprint)={expl_bp:+.4f}? {ok}")


def check_subgame_differs_and_safe():
    if not _scipy_ok():
        return None, "numpy/scipy not installed -> SKIP"
    from subgame_exploit_solver import subgame_exploit, leduc_postflop
    game = make_game("leduc")
    hero = 0
    nash, _ = solve_nash_cached(game, 4000)
    zoo = make_type_zoo(game, nash_iters=4000)
    opp = zoo["Rock"]
    res = subgame_exploit(game, hero, opp, nash, predicate=leduc_postflop)
    ok = res["differs_from_blueprint"] and res["improves_ev"] and res["gadget_satisfied"]
    return ok, (f"differs={res['differs_from_blueprint']} (maxTV {res['max_subgame_tv']:.2f}), "
                f"improves_ev={res['improves_ev']} "
                f"(EV {res['exploitation_value']:+.3f} vs blueprint "
                f"{res['blueprint_ev_vs_model']:+.3f}), gadget={res['gadget_satisfied']}")


def check_openspiel_cross():
    from compare_openspiel import cross_check_nashconv_uniform
    ok = cross_check_nashconv_uniform()
    if ok is None:
        return None, "OpenSpiel not installed -> SKIP"
    return ok, "NashConv(uniform) matches OpenSpiel within tol (see lines above)"


CHECKS = [
    ("seq-form LP BR == exact BR (kuhn)", check_seq_form_br_matches_exact),
    ("RNR endpoints (p=0 safe, p=1 = full BR)", check_rnr_endpoints),
    ("Ganzfried safe (>= v*) & profitable", check_ganzfried_safe_and_profitable),
    ("prime-safe floor = v* - eps", check_prime_safe_floor),
    ("adaptation-safety inequality", check_adaptation_safety_inequality),
    ("subgame differs + improves + safe (leduc)", check_subgame_differs_and_safe),
    ("OpenSpiel exploitability cross-check", check_openspiel_cross),
]


def main():
    print("Step 08 validation")
    print("=" * 74)
    passed = failed = skipped = 0
    for name, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as exc:  # noqa: BLE001 - surface bugs as a clear FAIL
            ok, detail = False, f"EXCEPTION: {type(exc).__name__}: {exc}"
        if ok is None:
            status, skipped = "SKIP", skipped + 1
        elif ok:
            status, passed = "PASS", passed + 1
        else:
            status, failed = "FAIL", failed + 1
        print(f"[{status}] {name:44s} {detail}")
    print("=" * 74)
    print(f"passed={passed} failed={failed} skipped={skipped}")
    return failed == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
