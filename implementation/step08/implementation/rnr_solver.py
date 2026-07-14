"""
rnr_solver.py -- Restricted Nash Response (Johanson, Zinkevich & Bowling 2007).

>>> BIG FLAG: canonical RNR vs the raw step's naive p-blend <<<
The raw step's Day-2/Day-3 text (L128-142, L432-441) describes RNR as a p-BLEND of Nash and
best response -- "(1-p)*Nash + p*BR" -- or "at most p% of info sets use BR". That is a fine
INTUITION but it is NOT Johanson's algorithm. Canonical RNR computes the hero's EQUILIBRIUM
against a "p-restricted" opponent: an opponent forced to play the fixed model with probability
p and free to play adversarially with probability (1-p). Because the (1-p) part best-responds
to the hero, RNR(p) solves a MAX-MIN:

    RNR(p) = argmax_x [ p * EV(x vs model) + (1-p) * min_{sigma'} EV(x vs sigma') ]

We implement the REAL thing (a cutting-plane max-min LP with an auxiliary worst-case
variable t) AND the naive blend, side by side, so you can SEE that canonical RNR dominates
the blend (more profit at the same exploitability). Do not conflate the two. (workflow.md
§0/§2: flag ambiguity, implement faithfully, don't silently pick the easy reading.)

Endpoints (validation, raw step L559): p=0 -> pure max-min = Nash (exploitability ~ 0);
p=1 -> pure exploitation = full best response (EV = BR value).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import deps  # noqa: F401
from best_response import best_response_policy
from policies import blend_policies
from seq_form import HeroTreeplex, expected_value
from safety_checker import worst_case_value, game_value
from exploitation_metrics import exploitation_value


def canonical_rnr(game, hero: int, opp_model, p: float, treeplex: "HeroTreeplex | None" = None,
                  max_iters: int = 40, tol: float = 1e-7, verbose: bool = False) -> dict:
    """Solve RNR(p) as a max-min via cutting planes on an auxiliary worst-case variable t.

    Variables z = [x_0..x_{n-1}, t]. Maximize p * c_model . x + (1-p) * t, subject to
    treeplex(x), and t <= c_adv . x for every discovered adversary payoff vector c_adv (each
    is the opponent's BR to the current x). At optimality t = min_sigma' EV(x vs sigma')."""
    try:
        import numpy as np
        from scipy.optimize import linprog
    except ImportError as exc:  # pragma: no cover
        raise ImportError("rnr_solver needs numpy + scipy.") from exc

    opp = 1 - hero
    tp = treeplex if treeplex is not None else HeroTreeplex(game, hero)
    n = tp.num_seq
    c_model = np.asarray(tp.payoff_vector(opp_model), dtype=float)

    A_eq_x = tp.flow_matrix()                       # (m, n)
    A_eq = np.hstack([A_eq_x, np.zeros((A_eq_x.shape[0], 1))])  # t has no flow role
    b_eq = np.zeros(A_eq.shape[0])

    # bounds: x >= 0 with x[0] pinned to 1; t free.
    bounds = [(0.0, None)] * n + [(None, None)]
    bounds[0] = (1.0, 1.0)

    # objective (minimize): -(p * c_model . x + (1-p) * t)
    obj = np.concatenate([-p * c_model, [-(1.0 - p)]])

    adv_rows, adv_b = [], []  # t - c_adv . x <= 0
    x = None
    hero_pol = None
    for it in range(max_iters):
        A_ub = np.vstack(adv_rows) if adv_rows else None
        b_ub = np.asarray(adv_b, dtype=float) if adv_b else None
        res = linprog(obj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds,
                      method="highs")
        if not res.success:
            raise RuntimeError(f"RNR LP failed at p={p}: {res.message}")
        z = res.x
        x = z[:n]
        t = z[n]
        hero_pol = tp.policy(x)
        wc = worst_case_value(game, hero_pol, hero)  # true min over adversaries
        if verbose:
            print(f"    [rnr p={p:.2f}] iter {it}: t={t:+.4f} true_wc={wc:+.4f} "
                  f"cuts={len(adv_rows)}", flush=True)
        # t is the LP's optimistic worst-case (an upper bound on the true wc). Converged when
        # the LP's t no longer over-estimates the achievable worst-case.
        if t <= wc + tol:
            break
        opp_br = best_response_policy(game, opp, hero_pol)
        c_adv = np.asarray(tp.payoff_vector(opp_br), dtype=float)
        row = np.concatenate([-c_adv, [1.0]])       # t - c_adv . x <= 0
        adv_rows.append(row)
        adv_b.append(0.0)

    return {
        "method": "rnr", "variant": "canonical", "p": p, "game": game.name, "hero": hero,
        "exploitation_value": exploitation_value(game, hero_pol, opp_model, hero),
        "worst_case_value": worst_case_value(game, hero_pol, hero),
        "policy": hero_pol, "realization_plan": list(x) if x is not None else None,
        "iterations": it + 1,
    }


def naive_rnr(game, hero: int, opp_model, p: float, nash_policy) -> dict:
    """The raw step's blend: (1-p)*Nash + p*BR(model). Provided for the flagged comparison
    ONLY -- it is not the RNR algorithm."""
    br = best_response_policy(game, hero, opp_model)
    if p <= 0.0:
        pol = nash_policy
    elif p >= 1.0:
        pol = br
    else:
        pol = blend_policies([br, nash_policy], [p, 1.0 - p])
    return {
        "method": "rnr", "variant": "naive_blend", "p": p, "game": game.name, "hero": hero,
        "exploitation_value": exploitation_value(game, pol, opp_model, hero),
        "worst_case_value": worst_case_value(game, pol, hero),
        "policy": pol,
    }


def rnr_sweep(game, hero, opp_model, nash_policy, ps=None, include_naive: bool = True,
              verbose: bool = False) -> dict:
    """Sweep p and return canonical (and optionally naive) RNR curves. `nash_policy` is only
    needed for the naive blend and as a reference."""
    if ps is None:
        ps = [i / 10.0 for i in range(11)]
    tp = HeroTreeplex(game, hero)
    v = game_value(game, nash_policy, hero)
    canonical, naive = [], []
    for p in ps:
        canonical.append(_row(canonical_rnr(game, hero, opp_model, p, treeplex=tp,
                                             verbose=verbose), v))
        if include_naive:
            naive.append(_row(naive_rnr(game, hero, opp_model, p, nash_policy), v))
    return {"game": game.name, "hero": hero, "game_value": v,
            "canonical": canonical, "naive": naive}


def _row(res, v):
    return {"p": res["p"], "exploitation_value": res["exploitation_value"],
            "worst_case_value": res["worst_case_value"],
            "exploitability": v - res["worst_case_value"]}


def _selftest():
    from engines import make_game
    from nash import solve_nash_cached
    from opponent_types import make_type_zoo
    from best_response import best_response_value

    print("rnr_solver self-test")
    print("-" * 60)
    game = make_game("kuhn")
    hero = 0
    nash, _ = solve_nash_cached(game, 30000)
    zoo = make_type_zoo(game, nash_iters=30000)
    tp = zoo["TightPassive"]
    v = game_value(game, nash, hero)
    br_val = best_response_value(game, hero, tp)

    try:
        sweep = rnr_sweep(game, hero, tp, nash, ps=[0.0, 0.5, 1.0])
    except ImportError as exc:
        print(f"SKIP ({exc})")
        return
    print(f"[kuhn] game value v* = {v:+.4f}; full BR value = {br_val:+.4f}")
    print(f"{'p':>5s} {'canon EV':>10s} {'canon expl':>11s} {'naive EV':>10s} "
          f"{'naive expl':>11s}")
    for cr, nr in zip(sweep["canonical"], sweep["naive"]):
        print(f"{cr['p']:>5.1f} {cr['exploitation_value']:>10.4f} {cr['exploitability']:>11.4f} "
              f"{nr['exploitation_value']:>10.4f} {nr['exploitability']:>11.4f}")
    print("expect: p=0 canon exploitability ~ 0; p=1 canon EV ~ full BR; "
          "canon dominates naive (more EV at equal exploitability).")


if __name__ == "__main__":
    _selftest()
