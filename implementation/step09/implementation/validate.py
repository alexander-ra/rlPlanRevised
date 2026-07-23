"""
Validation harness for Step 09 -- the checks that decide whether the multi-agent
implementations are actually CORRECT (not merely running). Encodes the raw step's validation
targets (L450-456) plus the LOLA cooperation result (L250-256).

Run it yourself:  python validate.py
Each check prints PASS / FAIL / SKIP with the observed numbers. Sizes are kept modest so the
whole thing finishes in a few minutes (PSRO-on-Leduc dominates). The EXPECTED outcomes are
described (as predictions) in README.md; this script reports what actually happened.

Every check is wrapped so an exception becomes a FAIL with its message rather than aborting the
run. Neural checks (CTDE / communication) SKIP cleanly if torch is absent; the numpy-only
checks (matrix games, PSRO, LOLA) always run.

NOTE (per implementation/WORKFLOW.md): written by the agent but NOT executed by it.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401
from engines import make_game

from matrix_games import make_matrix_game, classify_outcome
from goofspiel import Goofspiel
import psro as psro_mod
import lola as lola_mod
from evaluation import independent_learn_matrix, _StatelessCoopEnv


# --- matrix games: outcomes match analytic Nash -------------------------------------
def check_matrix_nash():
    details = []
    ok = True

    # Prisoner's Dilemma: dominant-strategy -> defection (final profile at the NE).
    pd = make_matrix_game("prisoners_dilemma")
    x, y, _ = independent_learn_matrix(pd, steps=4000, lr=0.1, seed=0)
    pd_ok = pd.nashconv(x, y) < 0.05
    ok = ok and pd_ok
    details.append(f"PD final x={np.round(x,2).tolist()} (want Defect) NashConv={pd.nashconv(x,y):.3f}")

    # Matching Pennies: last iterate CYCLES; the TIME AVERAGE converges to (1/2,1/2).
    mp = make_matrix_game("matching_pennies")
    _, _, hist = independent_learn_matrix(mp, steps=8000, lr=0.1, seed=0)
    half = len(hist["x"]) // 2
    xbar = np.mean(np.array(hist["x"][half:]), axis=0)
    ybar = np.mean(np.array(hist["y"][half:]), axis=0)
    mp_ok = mp.nashconv(xbar, ybar) < 0.1
    ok = ok and mp_ok
    details.append(f"MP avg x={np.round(xbar,2).tolist()} y={np.round(ybar,2).tolist()} "
                   f"NashConv(avg)={mp.nashconv(xbar,ybar):.3f} (want ~0; last-iterate cycles)")

    # Stag Hunt & Battle of the Sexes: converge to *some* listed pure NE (init-dependent).
    for name in ("stag_hunt", "battle_of_the_sexes"):
        g = make_matrix_game(name)
        seed_ok = True
        for seed in (0, 1, 2):
            x, y, _ = independent_learn_matrix(g, steps=6000, lr=0.1, seed=seed)
            seed_ok = seed_ok and (g.nashconv(x, y) < 0.05)
        ok = ok and seed_ok
        details.append(f"{name}: all seeds reach a Nash (NashConv<0.05)? {seed_ok}")

    return ok, " | ".join(details)


# --- PSRO on Kuhn: exploitability -> ~0 ---------------------------------------------
def check_psro_kuhn():
    psro = psro_mod.PSRO(make_game("kuhn"), oracle="exact", seed=0)
    h = psro.iterate(rounds=15)
    final = h["exploitability"][-1]
    ok = final < 0.05
    return ok, (f"final exploitability={final:.5f} after {len(h['round'])} rounds "
                f"(want < 0.05; started at {h['exploitability'][0]:.4f})")


# --- PSRO on Leduc: exploitability < 0.5 within 20 iters ----------------------------
def check_psro_leduc():
    psro = psro_mod.PSRO(make_game("leduc"), oracle="exact", seed=0)
    h = psro.iterate(rounds=20)
    final = h["exploitability"][-1]
    ok = final < 0.5
    return ok, (f"final exploitability={final:.4f} within {len(h['round'])} iters "
                f"(raw-step target < 0.5; started at {h['exploitability'][0]:.4f})")


# --- PSRO on Goofspiel: exploitability decreases ------------------------------------
def check_psro_goofspiel():
    goof = Goofspiel(num_cards=3)
    h = psro_mod.psro_goofspiel(goof, rounds=5, seed=0)
    first, last = h["exploitability"][0], h["exploitability"][-1]
    ok = last < first + 1e-9
    return ok, f"exploitability {first:.4f} -> {last:.4f} (want non-increasing)"


# --- MADDPG centralized critic has lower variance than independent critics -----------
def check_critic_variance():
    from learners import torch_available
    if not torch_available():
        return None, "torch not installed -> SKIP"
    from coop_env import CoopSignalEnv
    from maddpg import MADDPG
    env = CoopSignalEnv(n_targets=4, comm=False, seed=0)
    algo = MADDPG(env, {"seed": 0})
    hist = algo.train(episodes=4000, batch_episodes=256, seed=0)
    cmp = algo.critic_variance_comparison(hist)
    ok = cmp["central_lower"]
    return ok, (f"central_final_loss={cmp['central_final_loss']:.4f} vs "
                f"indep_final_loss={cmp['indep_final_loss']:.4f} (want central < indep)")


# --- communication helps (CommNet ON vs OFF) ----------------------------------------
def check_communication_helps():
    from learners import torch_available
    if not torch_available():
        return None, "torch not installed -> SKIP"
    from coop_env import CoopSignalEnv
    import commnet as commnet_mod
    res = commnet_mod.compare(lambda: CoopSignalEnv(n_targets=4, comm=True, seed=0),
                              episodes=6000, batch_episodes=256, seed=0)
    ok = res["comm_helps"]
    return ok, (f"comm ON={res['comm_on_reward']:.3f} vs OFF={res['comm_off_reward']:.3f} "
                f"(want ON >> OFF ~= 1/K = 0.25)")


# --- CTDE beats independent learners on the climbing game ----------------------------
def check_ctde_beats_il():
    from learners import torch_available
    if not torch_available():
        return None, "torch not installed -> SKIP"
    from learners import IndependentLearners
    from maddpg import MADDPG
    from coop_env import ClimbingGame
    il = IndependentLearners(_StatelessCoopEnv(ClimbingGame()), {"seed": 0})
    il.train(episodes=4000, batch_episodes=256, seed=0)
    il_r = il.greedy_reward(episodes=1)
    md = MADDPG(_StatelessCoopEnv(ClimbingGame()), {"seed": 0})
    md.train(episodes=4000, batch_episodes=256, seed=0)
    md_r = md.greedy_reward(episodes=1)
    ok = md_r > il_r + 1e-6
    return ok, f"MADDPG reward={md_r:.2f} vs IL reward={il_r:.2f} (want CTDE higher; optimum=11)"


# --- LOLA induces cooperation on the IPD (and lr_opp=0 == naive) ---------------------
def check_lola_cooperation():
    # sanity: LOLA with lr_opp=0 must reproduce the naive gradient exactly
    g_naive = lola_mod.naive_grads(np.zeros(5), np.zeros(5), 0.96, 1e-4)[0]
    g_lola0 = lola_mod.lola_grad(1, np.zeros(5), np.zeros(5), 0.96, 0.0, 1e-4)
    sanity = float(np.max(np.abs(g_naive - g_lola0))) < 1e-6
    res = lola_mod.validate_cooperation({"steps": 200})
    ok = sanity and res["lola_cooperates_more"]
    return ok, (f"lr_opp=0==naive? {sanity}; naive return={res['naive_return']:.2f} (~1) vs "
                f"LOLA return={res['lola_return']:.2f} (~3)")


# --- OpenSpiel cross-check (the exact BR engine PSRO relies on) ----------------------
def check_openspiel_cross():
    from compare_openspiel import cross_check_nashconv_uniform
    ok = cross_check_nashconv_uniform()
    if ok is None:
        return None, "OpenSpiel not installed -> SKIP"
    return ok, "NashConv(uniform) matches OpenSpiel within tol (see lines above)"


CHECKS = [
    ("matrix-game outcomes match analytic Nash", check_matrix_nash),
    ("PSRO Kuhn exploitability -> ~0", check_psro_kuhn),
    ("PSRO Leduc exploitability < 0.5 in 20 iters", check_psro_leduc),
    ("PSRO Goofspiel exploitability decreases", check_psro_goofspiel),
    ("MADDPG central critic lower variance than indep", check_critic_variance),
    ("communication helps (CommNet ON vs OFF)", check_communication_helps),
    ("CTDE beats IL on the climbing game", check_ctde_beats_il),
    ("LOLA induces cooperation on the IPD", check_lola_cooperation),
    ("OpenSpiel exploitability cross-check", check_openspiel_cross),
]


def main():
    print("Step 09 validation")
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
        print(f"[{status}] {name:48s} {detail}")
    print("=" * 78)
    print(f"passed={passed} failed={failed} skipped={skipped}")
    return failed == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
