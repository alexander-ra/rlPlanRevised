"""
Robustness sweep for the type detector on an out-of-set opponent (Step 07 exploration).

Backs the "500-hand / 300-seed" analysis in the exploration README and the step-07 report
(section 4.3). It asks, for the hidden Mixture(TightPassive, LooseAggressive) opponent that
matches NO single candidate type:

  - Does the single-type posterior ever end on the WRONG type after 500 hands?   (No.)
  - Once Nash permanently takes the lead, does it ever fall back?                 (No.)
  - How LONG can a wrong type confidently hold the lead before Nash overtakes?    (Long.)

The finding: Nash never *falls* -- once it locks in it stays -- but convergence can be very
slow, with the maniac (LooseAggressive) confidently owning the belief for 100-200+ hands
first, purely because an early run of bet-heavy hands looks exactly like "always bets".
This is the concrete cautionary tale for safe exploitation (Step 08): a model can be
confident AND wrong for a long time.

Also regenerates the illustrative 500-hand posterior chart for the most volatile seed.

NOTE (per implementation/WORKFLOW.md): written for you to run. Runtime a few seconds.
Run: python implementation/step07/exploration/robustness_sweep.py
"""

import os
import json
import statistics

from opponent_types import make_type_zoo, mixture, tight_passive, loose_aggressive
from bayesian_type_detector import run_detection

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

CONFIG = {
    "hands": 500,
    "seeds": 300,
    "epsilon": 0.02,
    "nash_iterations": 20000,
    "zoo_seed": 3,
}


def permanent_takeover_hand(trajectory, winner="Nash"):
    """1-based hand from which `winner` is the argmax for the rest of the match
    (i.e. it takes the lead and never loses it again). len+1 if it never does."""
    winners = [max(p, key=p.get) for p in trajectory]
    t = len(trajectory)
    for i in range(len(trajectory) - 1, -1, -1):
        if winners[i] != winner:
            t = i + 1
            break
    else:
        t = 0
    return t + 1


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    candidates = make_type_zoo(include_nash=True,
                               nash_iterations=CONFIG["nash_iterations"],
                               seed=CONFIG["zoo_seed"])
    true_policy = mixture(tight_passive, loose_aggressive, 0.5)
    eps = CONFIG["epsilon"]
    H, S = CONFIG["hands"], CONFIG["seeds"]

    final_winner = {}
    takeover_hands = []
    wobble_after = 0                 # after permanent Nash takeover, Nash still dips < 0.5
    most_volatile = (None, 2.0, None)  # (seed, post-100 min Nash, trajectory)

    for s in range(S):
        _, traj, _ = run_detection(true_policy, candidates, hands=H, seed=s, epsilon=eps)
        fin = max(traj[-1], key=traj[-1].get)
        final_winner[fin] = final_winner.get(fin, 0) + 1

        t = permanent_takeover_hand(traj, "Nash")
        takeover_hands.append(t)
        if any(traj[i]["Nash"] < 0.5 for i in range(t - 1, len(traj))):
            wobble_after += 1

        post100_min = min(p["Nash"] for p in traj[100:])
        if post100_min < most_volatile[1]:
            most_volatile = (s, post100_min, traj)

    takeover_hands.sort()
    p90 = takeover_hands[int(0.9 * S)]
    results = {
        "hands": H, "seeds": S,
        "final_winner_distribution": final_winner,
        "nash_final_winner": f"{final_winner.get('Nash', 0)}/{S}",
        "takeover_hand": {"min": takeover_hands[0],
                          "median": statistics.median(takeover_hands),
                          "p90": p90, "max": takeover_hands[-1]},
        "wrong_type_led_past_100": f"{sum(1 for h in takeover_hands if h > 100)}/{S}",
        "wrong_type_led_past_200": f"{sum(1 for h in takeover_hands if h > 200)}/{S}",
        "nash_dip_after_permanent_takeover": f"{wobble_after}/{S}",
        "most_volatile_seed": most_volatile[0],
    }

    print(f"=== detector robustness: hidden = Mixture(Tight, Loose), {H} hands x {S} seeds ===")
    print(f"  final winner distribution        : {final_winner}")
    print(f"  Nash is final winner             : {results['nash_final_winner']}")
    th = results["takeover_hand"]
    print(f"  permanent-Nash-takeover hand     : min={th['min']}, median={th['median']:.0f}, "
          f"90th pct={th['p90']}, max={th['max']}")
    print(f"  wrong type led past hand 100     : {results['wrong_type_led_past_100']}")
    print(f"  wrong type led past hand 200     : {results['wrong_type_led_past_200']}")
    print(f"  Nash dipped <0.5 AFTER lock-in   : {results['nash_dip_after_permanent_takeover']}")

    path = os.path.join(FIG_DIR, "robustness_sweep.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved -> {path}")

    _plot_most_volatile(most_volatile[0], most_volatile[2], H)


def _plot_most_volatile(seed, trajectory, hands):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"(plotting skipped: {exc})")
        return
    names = list(trajectory[0])
    x = range(1, len(trajectory) + 1)
    fig, ax = plt.subplots(figsize=(11, 5))
    for n in names:
        ax.plot(list(x), [p[n] for p in trajectory], lw=1.3, label=n)
    ax.set_xlabel("hand")
    ax.set_ylabel("posterior probability")
    ax.set_ylim(-0.02, 1.02)
    ax.set_title(f"Type posterior over {hands} hands (most volatile seed={seed})\n"
                 f"hidden = Mixture(TightPassive, LooseAggressive)")
    ax.legend(loc="center right")
    fig.tight_layout()
    path = os.path.join(
        FIG_DIR, "posterior_hidden_mixture_tightpassive_looseaggressive_500hands.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"  plot -> {path}")


if __name__ == "__main__":
    main()
