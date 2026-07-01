"""
Naive Bayesian type detector (Step 07 exploration, Phase 2 / Day 2).

THE CORE LOOP of opponent modeling, in its simplest form. We hold a belief (a posterior)
over a small set of candidate opponent types. After each observed action we multiply in
its likelihood under each type and renormalize:

    posterior(type) is proportional to  prior(type) * product over observations of
                                        P(action | type, info_set)

Two experiments:
  1) Hidden opponent really IS one of our types (TightPassive) -> the posterior should
     concentrate on it within a handful of hands.
  2) Hidden opponent is a MIXTURE of two types -> the posterior should split between the
     two nearest types and stay low on the others (type-based models degrade gracefully).

SIMPLIFICATION (important — see the README "watch out"): this detector is *omniscient*
about the opponent's private card (it uses the true card when scoring the likelihood).
In real play you only see the card at showdown; the realistic version must marginalize
over the opponent's possible hands. That marginalization is built in the implementation
phase (Phase 4). Here we keep it simple to expose the belief-update loop cleanly.

Run (NOT executed here):  python implementation/step07/exploration/bayesian_type_detector.py
Runtime: < 1 s.
"""

import os
import json
import math
import random

from kuhn_tools import play_hand, random_deal
from opponent_types import make_type_zoo, mixture, tight_passive, loose_aggressive

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

CONFIG = {
    "hands": 50,
    "seed": 3,
    "epsilon": 0.02,   # likelihood smoothing; set to 0.0 to allow hard elimination
}


def uniform_prober(card, history):
    """50/50 opponent we play against the hidden type, to elicit varied decisions."""
    return (0.5, 0.5)


def run_detection(true_policy, candidates, hands, seed, epsilon):
    """Return (names, trajectory, n_obs).

    trajectory[h] is the posterior dict {name: prob} after hand h.
    """
    rng = random.Random(seed)
    names = list(candidates)
    log_post = {n: math.log(1.0 / len(names)) for n in names}  # uniform prior
    trajectory = []
    n_obs = 0

    for h in range(hands):
        opp_seat = 0 if (h % 2 == 0) else 1
        if opp_seat == 0:
            policy0, policy1 = true_policy, uniform_prober
        else:
            policy0, policy1 = uniform_prober, true_policy

        cards = random_deal(rng)
        decisions, _, _ = play_hand(cards, policy0, policy1, rng)

        for d in decisions:
            if d["player"] != opp_seat:
                continue
            n_obs += 1
            for n in names:
                p_action = candidates[n](d["card"], d["history"])[d["action"]]
                smoothed = (1.0 - epsilon) * p_action + epsilon * 0.5
                log_post[n] += math.log(max(smoothed, 1e-300))

        # normalize (log-sum-exp) into a posterior
        m = max(log_post.values())
        weights = {n: math.exp(log_post[n] - m) for n in names}
        z = sum(weights.values())
        trajectory.append({n: weights[n] / z for n in names})

    return names, trajectory, n_obs


def _print_trajectory(label, names, trajectory):
    print(f"\n=== {label} ===")
    checkpoints = [c for c in (1, 2, 5, 10, 20, 30, len(trajectory)) if c <= len(trajectory)]
    header = "hand  " + "".join(f"{n:>16}" for n in names)
    print(header)
    for c in checkpoints:
        post = trajectory[c - 1]
        print(f"{c:>4}  " + "".join(f"{post[n]:>16.3f}" for n in names))


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    candidates = make_type_zoo(include_nash=True, seed=CONFIG["seed"])

    scenarios = {
        "hidden = TightPassive": candidates["TightPassive"],
        "hidden = Mixture(TightPassive, LooseAggressive)":
            mixture(tight_passive, loose_aggressive, 0.5),
    }

    out = {}
    for label, true_policy in scenarios.items():
        names, trajectory, n_obs = run_detection(
            true_policy, candidates,
            hands=CONFIG["hands"], seed=CONFIG["seed"], epsilon=CONFIG["epsilon"],
        )
        _print_trajectory(f"{label}  ({n_obs} observations)", names, trajectory)
        out[label] = {"names": names, "trajectory": trajectory, "n_obs": n_obs}

    path = os.path.join(FIG_DIR, "type_detector.json")
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

    for label, data in out.items():
        names = data["names"]
        traj = data["trajectory"]
        x = range(1, len(traj) + 1)
        fig, ax = plt.subplots(figsize=(9, 5))
        for n in names:
            ax.plot(list(x), [post[n] for post in traj], marker="o", ms=3, label=n)
        ax.set_xlabel("hand")
        ax.set_ylabel("posterior probability")
        ax.set_ylim(0, 1)
        ax.set_title(f"Type posterior over time\n{label}")
        ax.legend()
        fig.tight_layout()
        safe = label.split("=")[0].strip().replace(" ", "_") + "_" + str(abs(hash(label)) % 1000)
        path = os.path.join(FIG_DIR, f"posterior_{safe}.png")
        fig.savefig(path, dpi=120)
        plt.close(fig)
        print(f"  plot -> {path}")


if __name__ == "__main__":
    main()
