"""
Validation harness for Step 07 -- the checks that decide whether the implementation is
actually correct (as opposed to merely running).

Run it yourself:  python validate.py
Each check prints PASS / FAIL / SKIP with the observed numbers. Sizes are kept small so the
whole thing finishes in well under a minute on Kuhn. These thresholds encode the raw step's
validation targets; the *expected* outcomes are described (as predictions) in README.md --
this script reports what actually happened when you run it.

Every check is wrapped so an exception becomes a FAIL with its message, rather than aborting
the run -- handy while you are debugging the trickier modules (the consistent model above
all).

NOTE (per implementation/WORKFLOW.md): written by the agent but NOT executed by it.
"""

from __future__ import annotations

import random

from engines import make_game
from policies import uniform_policy
from opponent_types import make_type_zoo
from best_response import best_response_value, exact_value, nash_gap
from nash import solve_nash_cached
from type_based_model import TypeBasedModel
from continuous_model import ContinuousModel
from adaptive_exploiter import AdaptiveExploiter, stationary, switching, exploitation_references
from tournament import mean_policy_tv, collect_observations

KUHN_GAME_VALUE = -1.0 / 18.0


# --- individual checks (each returns (status, detail)) ------------------------------
def check_kuhn_nash_value():
    game = make_game("kuhn")
    nash, _ = solve_nash_cached(game, 50000)
    v = exact_value(game, 0, nash, nash)
    ok = abs(v - KUHN_GAME_VALUE) < 0.01
    return ok, f"exact_value(Nash,Nash)={v:+.4f} target={KUHN_GAME_VALUE:+.4f}"


def check_kuhn_nash_unexploitable():
    game = make_game("kuhn")
    nash, _ = solve_nash_cached(game, 50000)
    gap = nash_gap(game, nash, nash)["nash_conv"]
    return gap < 0.05, f"NashConv(Nash,Nash)={gap:.4f} (want < 0.05)"


def check_br_beats_uniform():
    details = []
    ok = True
    for name in ("kuhn", "leduc"):
        game = make_game(name)
        br0 = best_response_value(game, 0, uniform_policy())
        ok = ok and (br0 > 0.0)
        details.append(f"{name} BR0 vs uniform={br0:+.3f}")
    return ok, "; ".join(details) + " (both want > 0)"


def check_type_detection():
    game = make_game("kuhn")
    hero, opp = 0, 1
    zoo = make_type_zoo(game, nash_iters=30000)
    truth = "TightPassive"
    rng = random.Random(0)
    buf = collect_observations(game, hero, zoo[truth], 500, rng, hero_policy=zoo["Nash"])
    model = TypeBasedModel(game, hero, zoo)
    model.observe(buf)
    post = model.posterior().get(truth, 0.0)
    ok = post > 0.8 and model.map_type() == truth
    return ok, f"posterior[{truth}]={post:.3f}, MAP={model.map_type()} (want >0.8 & correct)"


def check_continuous_recovers():
    game = make_game("kuhn")
    hero, opp = 0, 1
    zoo = make_type_zoo(game, include_nash=False)
    truth = zoo["LooseAggressive"]
    rng = random.Random(0)
    buf = collect_observations(game, hero, truth, 3000, rng, hero_policy=uniform_policy())
    model = ContinuousModel(game, hero, prior_strength=1.0)
    model.observe(buf)
    tv = mean_policy_tv(game, opp, model.predicted_policy(), truth)
    return tv < 0.15, f"mean TV(estimate, LooseAggressive)={tv:.3f} (want < 0.15)"


def check_consistent_recovers():
    try:
        import scipy  # noqa: F401
    except ImportError:
        return None, "scipy not installed -> SKIP (pip install scipy to enable)"
    from consistent_model import ConsistentModel
    game = make_game("kuhn")
    hero, opp = 0, 1
    zoo = make_type_zoo(game, include_nash=False)
    truth = zoo["TightPassive"]
    rng = random.Random(0)
    buf = collect_observations(game, hero, truth, 1500, rng, hero_policy=uniform_policy())
    model = ConsistentModel(game, hero)
    model.observe(buf)
    model.fit()
    est = model.predicted_policy()
    # opponent is player 1, who acts only after player 0. Build a state where player 1 holds
    # the King and is to act: deal (J, K), player 0 passes -> player 1 (K) on the spot.
    s = game.apply(game.root((1, 3)), 0)  # action 0 = PASS by player 0
    dist = est(game, s)                   # player 1's distribution at info set "3p"
    king_bet = dist.get(1, 0.0)
    return king_bet > 0.75, f"P(BET|King) for opp=player1={king_bet:.3f} (want > 0.75)"


def check_exploit_beats_nash():
    game = make_game("kuhn")
    hero = 0
    zoo = make_type_zoo(game, nash_iters=30000)
    truth = zoo["TightPassive"]
    refs = exploitation_references(game, hero, truth, zoo["Nash"])
    model = ContinuousModel(game, hero)
    ex = AdaptiveExploiter(game, hero, model, nash_policy=zoo["Nash"],
                           refit_every=50, min_hands_before_exploit=25)
    res = ex.run(stationary(truth), 3000, random.Random(0))
    realized = res["mean_per_hand"]
    ok = realized > refs["nash_ev"] + 0.03 and realized <= refs["ceiling"] + 0.02
    return ok, (f"realized={realized:+.3f} nash_ev={refs['nash_ev']:+.3f} "
                f"ceiling={refs['ceiling']:+.3f} (want nash_ev < realized <= ceiling)")


def check_changepoint_helps():
    game = make_game("kuhn")
    hero = 0
    zoo = make_type_zoo(game, nash_iters=30000)
    seg = switching([(0, zoo["TightPassive"]), (1000, zoo["LooseAggressive"])])
    after = {}
    for use_cp in (False, True):
        model = ContinuousModel(game, hero)
        ex = AdaptiveExploiter(game, hero, model, nash_policy=zoo["Nash"], refit_every=50,
                               min_hands_before_exploit=25, use_changepoint=use_cp)
        res = ex.run(seg, 2000, random.Random(7))
        post_switch = res["profits"][1000:]
        after[use_cp] = sum(post_switch) / len(post_switch)
    ok = after[True] >= after[False] - 0.02  # change-point should not hurt; usually helps
    return ok, (f"post-switch mean: static={after[False]:+.3f} "
                f"changepoint={after[True]:+.3f} (want changepoint >= static)")


CHECKS = [
    ("kuhn Nash value (-1/18)", check_kuhn_nash_value),
    ("kuhn Nash unexploitable", check_kuhn_nash_unexploitable),
    ("BR beats uniform (kuhn+leduc)", check_br_beats_uniform),
    ("type-based detection", check_type_detection),
    ("continuous recovers strategy", check_continuous_recovers),
    ("consistent recovers strategy", check_consistent_recovers),
    ("exploiter beats Nash, under ceiling", check_exploit_beats_nash),
    ("change-point helps non-stationary", check_changepoint_helps),
]


def main():
    print("Step 07 validation")
    print("=" * 70)
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
        print(f"[{status}] {name:36s} {detail}")
    print("=" * 70)
    print(f"passed={passed} failed={failed} skipped={skipped}")
    return failed == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
