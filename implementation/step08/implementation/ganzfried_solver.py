"""
ganzfried_solver.py -- Ganzfried & Sandholm (2015) safe opponent exploitation, and the
generic constraint-generation CORE that prime-safe and adaptation-safety reuse.

THE PROBLEM (raw step Day 4, L444-456)
--------------------------------------
    maximize   EV(hero vs opponent model)                     # linear: c_model . x
    subject to worst_case_value(hero) >= floor                # a minimax / safety constraint
where floor = the Nash game value v* for pure Ganzfried safety (Theorem 1). The constraint's
worst-case is itself an inner best-response (the "min over opponents"), so we solve it by
CONSTRAINT GENERATION (a cutting-plane / double-oracle loop):

    repeat:
        x*   = argmax c_model . x  s.t. treeplex(x) and all discovered safety cuts
        pol  = behavioral(x*)
        wc   = worst_case_value(pol)          # exact BR by the adversary
        if wc >= floor - tol: DONE (safe)
        else: add the cut  c(adversary_BR) . x >= floor  and re-solve

Each cut is the payoff vector against the adversary's best response to the current strategy;
it is a valid linear lower bound on the true worst-case, so adding cuts tightens the relaxed
constraint toward the real one. The loop is finite (finitely many pure best responses).

WHY IT DOMINATES RNR ON KUHN (raw step L455): same safety floor, but Ganzfried maximizes
exploitation *directly* against the model, so it never gives up profit it does not have to.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import deps  # noqa: F401
from best_response import best_response_policy
from seq_form import HeroTreeplex, expected_value
from safety_checker import worst_case_value


def safe_exploit(game, hero: int, opp_model, floor: float, treeplex: "HeroTreeplex | None" = None,
                 fixed=None, max_iters: int = 30, tol: float = 1e-6, verbose: bool = False) -> dict:
    """Generic safe-exploitation solve: max EV vs `opp_model` s.t. worst-case >= `floor`.

    This is the shared engine. Ganzfried passes floor=v*; prime-safe passes floor=v*-eps;
    adaptation passes floor=worst_case_value(blueprint); the subgame solver passes `fixed`
    (blueprint pins outside the subgame). Returns a result dict (below).
    """
    opp = 1 - hero
    tp = treeplex if treeplex is not None else HeroTreeplex(game, hero)
    c_model = tp.payoff_vector(opp_model)  # the exploitation objective (fixed)

    cuts = []          # list of (payoff_vector_vs_adversary, floor)
    history = []       # per-iteration (exploitation_value, worst_case) for debugging
    x = None
    hero_pol = None
    for it in range(max_iters):
        res = tp.solve(c_model, cuts=cuts, sense="max", fixed=fixed)
        x = res.x
        hero_pol = tp.policy(x)
        exploit_ev = expected_value(c_model, x)
        wc = worst_case_value(game, hero_pol, hero)
        history.append({"iter": it, "exploit_ev": exploit_ev, "worst_case": wc,
                        "n_cuts": len(cuts)})
        if verbose:
            print(f"    [ganzfried] iter {it}: exploit_ev={exploit_ev:+.4f} "
                  f"worst_case={wc:+.4f} floor={floor:+.4f} cuts={len(cuts)}", flush=True)
        if wc >= floor - tol:
            return _result(game, hero, tp, x, hero_pol, c_model, floor, wc, exploit_ev,
                           it + 1, True, history)
        # discovered adversary: the opponent's exact BR to the current hero strategy.
        opp_br = best_response_policy(game, opp, hero_pol)
        c_adv = tp.payoff_vector(opp_br)
        cuts.append((c_adv, floor))

    # Exhausted iterations without meeting the floor: report the last strategy, unsafe flag.
    return _result(game, hero, tp, x, hero_pol, c_model, floor,
                   worst_case_value(game, hero_pol, hero),
                   expected_value(c_model, x), max_iters, False, history)


def _result(game, hero, tp, x, hero_pol, c_model, floor, wc, exploit_ev, iters, safe, history):
    return {
        "method": "ganzfried",
        "game": game.name,
        "hero": hero,
        "floor": floor,
        "exploitation_value": exploit_ev,     # EV vs the model (profit)
        "worst_case_value": wc,               # hero's guaranteed EV (safety)
        "safety_margin": wc - floor,          # >= ~0 means the floor is met
        "safe": bool(safe),
        "iterations": iters,
        "policy": hero_pol,                   # callable policy(game, state)
        "realization_plan": list(x) if x is not None else None,
        "history": history,
    }


def ganzfried_safe_exploit(game, hero, opp_model, nash_value, **kw) -> dict:
    """Ganzfried (2015): safe exploitation with the floor pinned to the Nash game value."""
    res = safe_exploit(game, hero, opp_model, floor=nash_value, **kw)
    res["method"] = "ganzfried"
    return res


def _selftest():
    from engines import make_game
    from nash import solve_nash_cached
    from opponent_types import make_type_zoo
    from safety_checker import game_value
    from exploitation_metrics import exploitation_value

    print("ganzfried_solver self-test")
    print("-" * 60)
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    v = game_value(game, nash, hero)
    zoo = make_type_zoo(game, nash_iters=30000)
    tp = zoo["TightPassive"]

    try:
        res = safe_exploit(game, hero, tp, floor=v, verbose=True)
    except ImportError as exc:
        print(f"SKIP ({exc})")
        return
    nash_ev = exploitation_value(game, nash, tp, hero)
    print(f"[kuhn] game value v* = {v:+.4f}")
    print(f"[kuhn] Nash EV vs TightPassive        = {nash_ev:+.4f}")
    print(f"[kuhn] Ganzfried exploitation value   = {res['exploitation_value']:+.4f} "
          f"(want >= Nash EV)")
    print(f"[kuhn] Ganzfried worst-case value     = {res['worst_case_value']:+.4f} "
          f"(want >= v* within tol -> safe)")
    print(f"[kuhn] safe={res['safe']} iterations={res['iterations']}")


if __name__ == "__main__":
    _selftest()
