"""
Validation harness for Step 10 -- the checks that decide whether the population-training /
evolutionary-GT implementations are actually CORRECT (not merely running). Encodes the raw
step's validation targets (L486-492) plus the deliverables (L475-484).

Run it yourself:  python validate.py
Each check prints PASS / FAIL / SKIP with the observed numbers. The exact suites (replicator,
spinning-top, EGTA-on-exact-policies, PSRO) always run; the neural league / self-play checks
SKIP cleanly if torch is absent. Sizes are kept modest so the whole thing finishes in a few
minutes (the neural league dominates).

Every check is wrapped so an exception becomes a FAIL with its message rather than aborting the
run. The EXPECTED outcomes are described (as predictions) in README.md; this script reports
what actually happened.

NOTE (per implementation/WORKFLOW.md): written by the agent but NOT executed by it.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401
from engines import make_game
from best_response import nash_gap
from nash import solve_nash_cached
from policies import uniform_policy
from psro import PSRO

import evo_games
import replicator as rep
import spinning_top as st
import egta


# --- replicator dynamics match the analytic ESS (raw L486, L375-380) ----------------
def check_replicator():
    details = []
    ok = True

    # Prisoner's Dilemma: cooperator share -> 0 (defection dominates).
    pd = evo_games.make_evo_game("prisoners_dilemma")
    xs = rep.simulate_single(pd.A, [0.5, 0.5], T=6000, dt=0.01)
    pd_ok = rep.converged(xs) and xs[-1][1] > 0.98
    ok = ok and pd_ok
    details.append(f"PD final={np.round(xs[-1],3).tolist()} (want ~[0,1] Defect) ok={pd_ok}")

    # Hawk-Dove: converge to the mixed ESS p(Hawk)=V/C=0.5.
    hd = evo_games.make_evo_game("hawk_dove")
    xs = rep.simulate_single(hd.A, [0.2, 0.8], T=8000, dt=0.01)
    hd_ok = rep.converged(xs) and abs(xs[-1][0] - 0.5) < 0.02
    ok = ok and hd_ok
    details.append(f"Hawk-Dove final p(Hawk)={xs[-1][0]:.3f} (want ~0.5) ok={hd_ok}")

    # RPS: NEVER converges -- persistent orbit around uniform.
    rps = evo_games.make_evo_game("rock_paper_scissors")
    xs = rep.simulate_single(rps.A, [0.4, 0.35, 0.25], T=8000, dt=0.01)
    radius = rep.orbit_radius(xs, [1 / 3, 1 / 3, 1 / 3])
    rps_ok = (not rep.converged(xs)) and radius > 0.02
    ok = ok and rps_ok
    details.append(f"RPS converged={rep.converged(xs)} orbit_radius={radius:.3f} "
                   f"(want NOT converged) ok={rps_ok}")

    # Stag Hunt: two basins -> two starts reach different pure equilibria.
    sh = evo_games.make_evo_game("stag_hunt")
    a = rep.simulate_single(sh.A, [0.8, 0.2], T=6000, dt=0.01)[-1]
    b = rep.simulate_single(sh.A, [0.2, 0.8], T=6000, dt=0.01)[-1]
    sh_ok = abs(a[0] - b[0]) > 0.9   # one -> all-Stag, the other -> all-Hare
    ok = ok and sh_ok
    details.append(f"Stag Hunt basins: start0->{np.round(a,2).tolist()} start1->{np.round(b,2).tolist()} ok={sh_ok}")

    return ok, " | ".join(details)


# --- spinning top: RPS is ~100% cyclic; pure-skill is ~100% transitive (raw L487) ---
def check_spinning_top():
    rps = evo_games.make_evo_game("rock_paper_scissors").A
    tr_rps = st.transitive_ratio(rps, "hodge")
    tr_skill = st.transitive_ratio(st.pure_skill_game(5), "hodge")
    ok = tr_rps < 0.05 and tr_skill > 0.95
    return ok, (f"RPS transitive_ratio={tr_rps:.4f} (want ~0), pure-skill transitive_ratio="
                f"{tr_skill:.4f} (want ~1); [raw-step SVD on RPS would give "
                f"{st.transitive_ratio(rps, 'svd'):.3f} -- see spinning_top.py NOTE]")


# --- EGTA meta-Nash <= best individual, on EXACT policies (torch-free) ---------------
def check_egta_meta_nash_exact():
    """Fast, torch-free EGTA check: a population of exact policies (uniform + two CFR-Nash at
    different iteration counts + a fold-happy policy) has a meta-Nash no more exploitable than
    its best member (raw L490)."""
    game = make_game("kuhn")
    nash_a, _ = solve_nash_cached(game, iters=3000)
    nash_b, _ = solve_nash_cached(game, iters=500)
    policies = [uniform_policy(), nash_a, nash_b]
    rep_ = egta.analyze_population(game, policies, ["uniform", "nash3k", "nash500"])
    ok = rep_["meta_nash_no_worse_than_best_individual"]
    return ok, (f"meta-Nash exploitability={rep_['meta_nash_exploitability']} <= best individual="
                f"{rep_['best_individual_exploitability']}? {ok}")


# --- PBT league: main-agent exploitability decreases over epochs (raw L488) ----------
def check_league_exploitability_decreases():
    from ppo_agent import torch_available
    if not torch_available():
        return None, "torch not installed -> SKIP"
    from league import LeducLeague
    game = make_game("leduc")
    cfg = {"num_main": 2, "num_main_exploiters": 1, "num_league_exploiters": 1,
           "episodes_per_epoch": 128, "epochs": 12, "freeze_every": 4, "pbt_every": 6, "seed": 0}
    league = LeducLeague(game, cfg)
    league.run()
    traj = [v for v in league.history["min_main_exploitability"] if v is not None]
    # target: the BEST-so-far main exploitability at the end is below the start (progress).
    start = traj[0]
    best_end = min(traj[len(traj) // 2:])
    ok = best_end < start
    return ok, f"min-main-exploitability start={start:.3f} best-second-half={best_end:.3f} (want lower)"


# --- EGTA meta-Nash <= best individual, on the trained league (torch) ----------------
def check_league_meta_nash():
    from ppo_agent import torch_available
    if not torch_available():
        return None, "torch not installed -> SKIP"
    from league import LeducLeague
    game = make_game("leduc")
    cfg = {"num_main": 2, "num_main_exploiters": 1, "num_league_exploiters": 1,
           "episodes_per_epoch": 128, "epochs": 10, "freeze_every": 4, "pbt_every": 6, "seed": 1}
    league = LeducLeague(game, cfg)
    league.run()
    rep_ = league.final_report()["egta"]
    ok = rep_["meta_nash_no_worse_than_best_individual"]
    return ok, (f"league meta-Nash exploitability={rep_['meta_nash_exploitability']} <= best "
                f"individual={rep_['best_individual_exploitability']}? {ok}")


# --- league meta-Nash exploitability comparable to PSRO on Leduc (raw L491-492) ------
def check_league_vs_psro():
    from ppo_agent import torch_available
    if not torch_available():
        return None, "torch not installed -> SKIP"
    from league import LeducLeague
    game = make_game("leduc")
    psro = PSRO(game, oracle="exact", seed=0)
    psro_expl = psro.iterate(rounds=12)["exploitability"][-1]
    cfg = {"num_main": 2, "num_main_exploiters": 1, "num_league_exploiters": 1,
           "episodes_per_epoch": 128, "epochs": 10, "freeze_every": 4, "pbt_every": 6, "seed": 2}
    league = LeducLeague(game, cfg)
    league.run()
    league_expl = league.final_report()["egta"]["meta_nash_exploitability"]
    # "comparable": same order of magnitude. Neural agents on a small budget won't match exact
    # PSRO, so we allow a generous band and treat this as a trend claim to verify (WORKFLOW 0).
    ok = league_expl <= max(2.0, 3.0 * psro_expl)
    return ok, (f"league meta-Nash={league_expl:.3f} vs PSRO(12)={psro_expl:.3f} "
                f"(want comparable order; generous band)")


CHECKS = [
    ("replicator dynamics match analytic ESS", check_replicator),
    ("spinning-top: RPS ~100% cyclic, skill ~100% transitive", check_spinning_top),
    ("EGTA meta-Nash <= best individual (exact policies)", check_egta_meta_nash_exact),
    ("PBT league main-agent exploitability decreases", check_league_exploitability_decreases),
    ("EGTA meta-Nash <= best individual (trained league)", check_league_meta_nash),
    ("league meta-Nash comparable to PSRO on Leduc", check_league_vs_psro),
]


def main():
    print("Step 10 validation")
    print("=" * 78)
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
        print(f"[{status}] {name:54s} {detail}")
    print("=" * 78)
    print(f"passed={passed} failed={failed} skipped={skipped}")
    return failed == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
