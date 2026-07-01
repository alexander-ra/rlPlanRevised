"""
Behavioral fingerprints (Step 07 exploration, Phase 2 / Day 1).

IDEA: every opponent type leaves a distinct "fingerprint" — its action frequencies at
each information set. An opponent model's whole job is to recover this fingerprint from
observed play. Here we just *look* at the fingerprints so we can see how different they
are (and how much sampling noise hides them at rarely-visited info sets).

We play each type against a uniform-random "prober" (which bets/checks 50/50) so that all
of the type's info sets — including the "facing a bet" ones — actually get visited. We
record the type's empirical action frequencies and compare them to its true policy.

Run (NOT executed here):  python implementation/step07/exploration/behavioral_fingerprints.py
Runtime: < 1 s (Kuhn is tiny).
"""

import os
import json
import random
from collections import defaultdict

from kuhn_tools import (
    BET, materialize_policy, info_set_label, play_hand, random_deal,
)
from opponent_types import make_type_zoo

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

# --- Config (smoke default; Kuhn never needs a larger run) --------------------------
CONFIG = {
    "hands_per_type": 2000,   # more hands -> less sampling noise in the fingerprint
    "seed": 7,
}


def uniform_prober(card, history):
    """A 50/50 opponent — used only to force coverage of every info set."""
    return (0.5, 0.5)


def measure_fingerprint(type_policy, hands, seed):
    """Return {info_set: {"n": visits, "p_bet": empirical bet freq}} for one type.

    The type is seated as player 0 for half the hands and player 1 for the other half so
    that all of its info sets are exercised.
    """
    rng = random.Random(seed)
    counts = defaultdict(lambda: [0, 0])  # info_set -> [n_pass, n_bet]

    for h in range(hands):
        type_seat = 0 if (h % 2 == 0) else 1
        if type_seat == 0:
            policy0, policy1 = type_policy, uniform_prober
        else:
            policy0, policy1 = uniform_prober, type_policy

        cards = random_deal(rng)
        decisions, _, _ = play_hand(cards, policy0, policy1, rng)
        for d in decisions:
            if d["player"] == type_seat:
                counts[d["info_set"]][d["action"]] += 1

    fingerprint = {}
    for info_set, (n_pass, n_bet) in counts.items():
        n = n_pass + n_bet
        fingerprint[info_set] = {"n": n, "p_bet": (n_bet / n) if n else float("nan")}
    return fingerprint


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    zoo = make_type_zoo(include_nash=True, seed=CONFIG["seed"])

    cache = {}
    for name, policy in zoo.items():
        emp = measure_fingerprint(policy, CONFIG["hands_per_type"], CONFIG["seed"])
        true = materialize_policy(policy, players=(0, 1))  # info_set -> [p_pass, p_bet]

        print(f"\n=== {name} ===")
        print(f"  {'info set':<14}{'visits':>8}{'emp p_bet':>12}{'true p_bet':>12}")
        for info_set in sorted(emp.keys()):
            true_pbet = true.get(info_set, [None, None])[BET]
            true_str = f"{true_pbet:.3f}" if true_pbet is not None else "  -  "
            print(f"  {info_set_label(info_set):<14}{emp[info_set]['n']:>8}"
                  f"{emp[info_set]['p_bet']:>12.3f}{true_str:>12}")

        cache[name] = {"empirical": emp,
                       "true": {k: v[BET] for k, v in true.items()}}

    out = os.path.join(FIG_DIR, "fingerprints_cache.json")
    with open(out, "w") as f:
        json.dump(cache, f, indent=2)
    print(f"\nSaved fingerprints -> {out}")

    _maybe_plot(cache)


def _maybe_plot(cache):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # matplotlib is optional
        print(f"(plotting skipped: {exc})")
        return

    for name, data in cache.items():
        info_sets = sorted(data["empirical"].keys())
        emp = [data["empirical"][i]["p_bet"] for i in info_sets]
        true = [data["true"].get(i, float("nan")) for i in info_sets]
        x = range(len(info_sets))

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar([i - 0.2 for i in x], true, width=0.4, label="true p(bet)")
        ax.bar([i + 0.2 for i in x], emp, width=0.4, label="empirical p(bet)")
        ax.set_xticks(list(x))
        ax.set_xticklabels([info_set_label(i) for i in info_sets], rotation=60, ha="right")
        ax.set_ylim(0, 1)
        ax.set_ylabel("P(bet)")
        ax.set_title(f"Behavioral fingerprint — {name}")
        ax.legend()
        fig.tight_layout()
        path = os.path.join(FIG_DIR, f"fingerprint_{name}.png")
        fig.savefig(path, dpi=120)
        plt.close(fig)
        print(f"  plot -> {path}")


if __name__ == "__main__":
    main()
