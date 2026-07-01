"""
Mixture recovery via EM (Step 07 exploration, Phase 2).

WHY THIS EXISTS
---------------
The naive Bayesian type detector (`bayesian_type_detector.py`) keeps a SINGLE posterior
over types -- a product of per-observation likelihoods. Against an opponent that is a
genuine BLEND of two types it collapses to the single best *global* explanation (Nash),
reporting a misleading ~1.0 even though Nash fits the blend only mediocrely (geo-mean
per-action likelihood ~0.31 vs ~0.74 against a true Nash). The posterior is a RELATIVE,
normalized quantity ("best among these four"), not a statement of absolute fit.

This script asks a different question: not "which ONE type are you?" but "what MIX of
types are you?" We fit mixing weights pi over the K fixed types by Expectation-
Maximization:

    E-step:  responsibility r_ik = pi_k * P(action_i | type_k) / sum_j pi_j P(action_i|type_j)
    M-step:  pi_k = mean_i r_ik
    (iterate to convergence)

Each observation is softly credited to the types and the weights are the average credit.
A naive HARD per-hand tally (argmax each hand, then count) does NOT work: it is confounded
by overlapping types -- AlwaysCall and TightPassive both "check" a weak hand, so the argmax
cannot separate them. EM deconfounds them and recovers the true weights.

WHAT IT PLOTS
-------------
The mixing-weight estimate is re-fit after every hand (warm-started from the previous
hand's estimate), giving a per-hand TRAJECTORY: one line per type, so you can watch the
weights move up/down together and converge to the true blend as evidence accumulates --
the mixture analogue of the detector's "posterior over time" charts.

RESULT (verify by running): against a w/(1-w) blend of TightPassive and LooseAggressive,
the two active lines climb to ~w and ~(1-w) while AlwaysCall and Nash decay to ~0; the old
global posterior (printed for contrast) instead reports Nash ~ 1.0. The EM log-likelihood
in pi is concave (log of a linear mix), so EM reaches the global optimum -- no local minima.

NOTE (per implementation/WORKFLOW.md): written for you to run. Runtime < 1 s.
Run: python implementation/step07/exploration/mixture_recovery.py
"""

import os
import re
import json
import math
import random

from kuhn_tools import play_hand, random_deal
from opponent_types import make_type_zoo, mixture, tight_passive, loose_aggressive

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

CONFIG = {
    "ratios": [0.5, 0.7],   # weight_a on TightPassive in the hidden Tight/Loose blend
    "hands": 250,           # trajectory horizon (enough to converge; readable as a line chart)
    "seed": 3,
    "epsilon": 0.02,        # likelihood smoothing (matches the detector)
    "nash_iterations": 20000,
    "em_iters": 300,        # max EM iterations per re-fit (cold start / final)
    "em_warm_iters": 60,    # max EM iterations per per-hand re-fit (warm-started -> few needed)
}


def uniform_prober(card, history):
    """50/50 opponent we play the hidden type against, to elicit varied decisions."""
    return (0.5, 0.5)


def collect_by_hand(true_policy, hands, seed):
    """Play `hands` hands of the hidden opponent vs the prober; return a list with one
    entry per hand: the list of that hand's opponent (card, history, action) decisions."""
    rng = random.Random(seed)
    per_hand = []
    for h in range(hands):
        opp_seat = 0 if (h % 2 == 0) else 1
        if opp_seat == 0:
            policy0, policy1 = true_policy, uniform_prober
        else:
            policy0, policy1 = uniform_prober, true_policy
        cards = random_deal(rng)
        decisions, _, _ = play_hand(cards, policy0, policy1, rng)
        per_hand.append([(d["card"], d["history"], d["action"])
                         for d in decisions if d["player"] == opp_seat])
    return per_hand


def likelihood(policy, obs_item, epsilon):
    """eps-smoothed probability that `policy` assigns to the observed action."""
    card, history, action = obs_item
    p = policy(card, history)[action]
    return (1.0 - epsilon) * p + epsilon * 0.5


def global_posterior(candidates, obs, epsilon):
    """The OLD method: single posterior over types = product of per-obs likelihoods."""
    names = list(candidates)
    log_post = {n: 0.0 for n in names}
    for o in obs:
        for n in names:
            log_post[n] += math.log(likelihood(candidates[n], o, epsilon))
    m = max(log_post.values())
    w = {n: math.exp(log_post[n] - m) for n in names}
    z = sum(w.values())
    return {n: w[n] / z for n in names}


def em_step_to_convergence(candidates, obs, epsilon, pi0, iters):
    """Run EM for the mixing weights starting from pi0 until convergence (or `iters`)."""
    names = list(candidates)
    pi = dict(pi0)
    for _ in range(iters):
        acc = {n: 0.0 for n in names}
        for o in obs:
            r = {n: pi[n] * likelihood(candidates[n], o, epsilon) for n in names}
            z = sum(r.values())
            for n in names:
                acc[n] += r[n] / z
        new_pi = {n: acc[n] / len(obs) for n in names}
        if max(abs(new_pi[n] - pi[n]) for n in names) < 1e-9:
            return new_pi
        pi = new_pi
    return pi


def em_trajectory(candidates, per_hand, epsilon, warm_iters):
    """Per-hand EM trajectory: after each hand, re-fit the mixing weights on all
    observations so far, warm-started from the previous hand's estimate."""
    names = list(candidates)
    pi = {n: 1.0 / len(names) for n in names}
    seen = []
    traj = []
    for hand in per_hand:
        seen.extend(hand)
        if seen:
            pi = em_step_to_convergence(candidates, seen, epsilon, pi, warm_iters)
        traj.append(dict(pi))
    return traj


def true_weights(names, weight_a):
    """Ground-truth mixing weights of the Tight/Loose blend, keyed by candidate name."""
    tw = {n: 0.0 for n in names}
    tw["TightPassive"] = weight_a
    tw["LooseAggressive"] = 1.0 - weight_a
    return tw


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    candidates = make_type_zoo(include_nash=True,
                               nash_iterations=CONFIG["nash_iterations"],
                               seed=CONFIG["seed"])
    names = list(candidates)
    eps = CONFIG["epsilon"]

    out = {}
    for w in CONFIG["ratios"]:
        label = f"Mixture(TightPassive {int(w*100)}%, LooseAggressive {int((1-w)*100)}%)"
        true_policy = mixture(tight_passive, loose_aggressive, w)
        per_hand = collect_by_hand(true_policy, CONFIG["hands"], CONFIG["seed"])
        flat = [o for hand in per_hand for o in hand]

        post = global_posterior(candidates, flat, eps)
        traj = em_trajectory(candidates, per_hand, eps, CONFIG["em_warm_iters"])
        pi_final = traj[-1]
        tw = true_weights(names, w)

        print(f"\n=== {label}   ({len(flat)} observations over {CONFIG['hands']} hands) ===")
        checkpoints = [c for c in (1, 5, 10, 20, 50, 100, CONFIG["hands"]) if c <= len(traj)]
        col = "".join(f"{n:>16}" for n in names)
        print(f"{'hand':>6}{col}")
        for c in checkpoints:
            p = traj[c - 1]
            print(f"{c:>6}" + "".join(f"{p[n]:>16.2f}" for n in names))
        print(f"{'TRUE':>6}" + "".join(f"{tw[n]:>16.2f}" for n in names))
        print(f"{'(old global posterior:)':>24} " +
              "  ".join(f"{n}={post[n]:.2f}" for n in names))

        out[label] = {"names": names, "trajectory": traj, "global_posterior": post,
                      "em_final": pi_final, "true_weights": tw,
                      "weight_a": w, "n_obs": len(flat), "hands": CONFIG["hands"]}

    path = os.path.join(FIG_DIR, "mixture_recovery.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved -> {path}")

    _maybe_plot(out)


def _maybe_plot(out):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"(plotting skipped: {exc})")
        return

    colors = {"AlwaysCall": "#1f77b4", "TightPassive": "#ff7f0e",
              "LooseAggressive": "#2ca02c", "Nash": "#d62728"}
    for label, data in out.items():
        names = data["names"]
        traj = data["trajectory"]
        tw = data["true_weights"]
        x = range(1, len(traj) + 1)
        fig, ax = plt.subplots(figsize=(9, 5))
        for n in names:
            ax.plot(list(x), [p[n] for p in traj], lw=1.6,
                    color=colors.get(n), label=n)
            if tw[n] > 0:  # dashed reference line at the true weight for active types
                ax.axhline(tw[n], color=colors.get(n), ls=":", lw=1.0, alpha=0.7)
        ax.set_xlabel("hand")
        ax.set_ylabel("EM mixing weight")
        ax.set_ylim(-0.02, 1.02)
        ax.set_title(f"EM mixing weights over time (dotted = true blend)\n{label}")
        ax.legend(loc="center right")
        fig.tight_layout()
        safe = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
        path = os.path.join(FIG_DIR, f"mixture_recovery_{safe}.png")
        fig.savefig(path, dpi=120)
        plt.close(fig)
        print(f"  plot -> {path}")


if __name__ == "__main__":
    main()
