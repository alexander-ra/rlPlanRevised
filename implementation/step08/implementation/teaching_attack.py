"""
teaching_attack.py -- the deception stress test (raw step L527-530, L537).

A DECEPTIVE opponent plays a weak, exploitable type (the "bait", e.g. TightPassive) for the
first `switch_at` hands to lure the modeler into a big deviation, then switches to strong play
(the "reveal", e.g. Nash) to punish it. This is the "being taught and exploited" scenario that
adaptation safety (Ge 2024) is designed to neutralize.

We run the online pipeline for several methods and compare post-switch behavior:
  - UNSAFE (`full_br`): over-commits to the bait, then bleeds after the reveal.
  - SAFE (`ganzfried`, `adaptation`): the safety floor caps the post-switch loss -- worst-case
    stays >= the Nash floor by construction, so the reveal cannot drag them below baseline.
  - `nash`: the control -- never deviates, never gets taught.

Reported per method (averaged over seeds): mean/hand overall, mean/hand AFTER the switch, and
the count of safety violations (played strategies whose worst-case fell below the Nash floor).

Expected (PREDICTION -- verify): safe methods' post-switch mean stays near the Nash baseline
(bounded loss); `full_br`'s is clearly worse. Safety violations: 0 for safe methods, > 0 for
`full_br`.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import random

import deps  # noqa: F401
from opponent_types import make_type_zoo
from nash import solve_nash_cached

from safety_checker import game_value
from prime_safe import make_epsilon_equilibrium
from pipeline import SafeExploitPipeline, make_model, make_ctx, switching


def run_teaching_attack(game, hero, cfg, zoo=None, ctx=None) -> dict:
    """Run the teaching-attack test for the methods in cfg['teaching_attack']."""
    ta = cfg["teaching_attack"]
    bait = ta["bait"][game.name]
    reveal = ta["reveal"][game.name]
    switch_at, total = ta["switch_at"], ta["total"]
    seeds = ta["seeds"]

    if zoo is None:
        zoo = make_type_zoo(game, nash_iters=cfg["nash_iters"][game.name])
    if ctx is None:
        nash, _ = solve_nash_cached(game, cfg["nash_iters"][game.name])
        v = game_value(game, nash, hero)
        blueprint = make_epsilon_equilibrium(game, cfg["epsilon_baseline_iters"][game.name])
        ctx = make_ctx(game, hero, nash, blueprint, v)

    schedule = switching([(0, zoo[bait]), (switch_at, zoo[reveal])])
    model_name = cfg["pipeline"]["model"]
    refit_every = cfg["pipeline"]["refit_every"]
    min_hands = cfg["pipeline"]["min_hands_before_exploit"]

    out = {"game": game.name, "bait": bait, "reveal": reveal, "switch_at": switch_at,
           "total": total, "seeds": list(seeds), "methods": {}}

    for method in ta["methods"]:
        means, after_means, violations = [], [], []
        rep_curve = None
        for si, seed in enumerate(seeds):
            model = make_model(model_name, game, hero, zoo)
            pipe = SafeExploitPipeline(game, hero, method, model, ctx,
                                       refit_every=refit_every, min_hands_before_exploit=min_hands)
            res = pipe.run(schedule, total, random.Random(500 + seed))
            after = res["profits"][switch_at:]
            means.append(res["mean_per_hand"])
            after_means.append(sum(after) / len(after) if after else 0.0)
            violations.append(res["safety_violations"])
            if si == 0:
                rep_curve = _downsample(res["cumulative"], 400)
        out["methods"][method] = {
            "mean_per_hand": sum(means) / len(means),
            "mean_after_switch": sum(after_means) / len(after_means),
            "safety_violations_by_seed": violations,
            "cumulative_seed0": rep_curve,
        }
    return out


def _downsample(seq, k):
    n = len(seq)
    if n <= k:
        return list(seq)
    step = n / k
    return [seq[min(n - 1, int(i * step))] for i in range(k)]


def print_summary(result):
    print(f"\n  -- teaching attack ({result['game']}): {result['bait']} -> {result['reveal']} "
          f"at hand {result['switch_at']} (mean over {len(result['seeds'])} seeds) --")
    print(f"  {'method':12s} {'mean/hand':>10s} {'after switch':>13s} {'safety viol.':>13s}")
    for method, blk in result["methods"].items():
        viol = blk["safety_violations_by_seed"]
        print(f"  {method:12s} {blk['mean_per_hand']:>10.4f} {blk['mean_after_switch']:>13.4f} "
              f"{str(viol):>13s}")


def _selftest():
    from engines import make_game
    import config as cfgmod

    print("teaching_attack self-test")
    print("-" * 60)
    cfg = cfgmod.get_config("smoke")
    cfg["teaching_attack"]["seeds"] = [0]      # keep the self-test quick
    cfg["teaching_attack"]["total"] = 800
    cfg["teaching_attack"]["switch_at"] = 400
    game = make_game("kuhn")
    try:
        res = run_teaching_attack(game, cfg["hero"], cfg)
    except ImportError as exc:
        print(f"SKIP ({exc})")
        return
    print_summary(res)


if __name__ == "__main__":
    _selftest()
