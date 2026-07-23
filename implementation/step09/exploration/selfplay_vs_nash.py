"""
selfplay_vs_nash.py -- does self-play converge to Nash on Kuhn? (Spoiler: the AVERAGE does.)

WHAT IT DOES
------------
Runs FICTITIOUS-PLAY self-play on Kuhn Poker (raw step L140-145): each iteration both players
best-respond to the OPPONENT'S running AVERAGE strategy, then fold their new best response
into their own average. We reuse Step 07's exact best response and NashConv, and track TWO
exploitability curves:

  - the AVERAGE strategy's NashConv  -> should DECREASE toward 0 (converges to Nash),
  - the LAST-ITERATE (pure BR) NashConv -> stays high / oscillates (pure best responses are
    themselves wildly exploitable).

This is the concrete answer to the raw step's question "does self-play converge to Nash?":
the *average iterate* does (Robinson 1951 / CFR-style averaging), the *last iterate* does not.
It is also the intuition PSRO builds on -- PSRO is iterated best response over a POPULATION,
with a meta-Nash mixture playing the role of the average.

HOW TO PLAY WITH IT (edit CONFIG)
---------------------------------
  iters      : more iterations -> the average's NashConv keeps shrinking (slowly, ~1/sqrt t).
  eval_every : how often to measure NashConv (each measurement is a couple of exact BRs).

WHAT TO WATCH OUT FOR
---------------------
- Fictitious play converges SLOWLY. Expect the average NashConv to fall from ~0.9 toward
  ~0.05-0.1 over a couple hundred iterations, not to hit machine zero.
- Kuhn's game value for player 0 is -1/18 = -0.0556; NashConv (br0 + br1) is what goes to 0,
  not the value.
- The last-iterate curve is SUPPOSED to look bad -- that is the lesson.

HOW TO READ THE RESULTS (PREDICTIONS -- verify by running)
----------------------------------------------------------
- average NashConv: monotone-ish DOWN toward ~0.
- last-iterate NashConv: stays large (order ~1), does not converge.

RUNTIME: ~seconds to a minute on Kuhn (a few hundred exact best responses).
"""

from __future__ import annotations

import _bootstrap  # noqa: F401  (side effect: puts step07/implementation on sys.path)

from engines import make_game
from best_response import best_response_policy, nash_gap
from policies import tabular_policy, uniform_policy, materialize

from _marl_tools import save_json, get_plt, figures_dir

CONFIG = {
    "iters": 200,
    "eval_every": 5,
    "save_plot": True,
}


def _normalize(counts: dict) -> dict:
    table = {}
    for iset, acts in counts.items():
        total = sum(acts.values())
        table[iset] = {a: (v / total if total > 0 else 0.0) for a, v in acts.items()}
    return table


def _accumulate(counts: dict, table: dict):
    for iset, dist in table.items():
        slot = counts.setdefault(iset, {})
        for a, p in dist.items():
            slot[a] = slot.get(a, 0.0) + p


def main():
    cfg = CONFIG
    game = make_game("kuhn")
    print("Fictitious-play self-play on Kuhn: average vs last-iterate exploitability")
    print("=" * 78)

    counts0, counts1 = {}, {}
    curve = {"iter": [], "avg_nashconv": [], "last_nashconv": []}

    for it in range(1, cfg["iters"] + 1):
        avg0 = tabular_policy(_normalize(counts0)) if counts0 else uniform_policy()
        avg1 = tabular_policy(_normalize(counts1)) if counts1 else uniform_policy()

        br0 = best_response_policy(game, 0, avg1)  # BR to opponent's average
        br1 = best_response_policy(game, 1, avg0)

        _accumulate(counts0, materialize(game, br0, 0))
        _accumulate(counts1, materialize(game, br1, 1))

        if it % cfg["eval_every"] == 0 or it == cfg["iters"]:
            new_avg0 = tabular_policy(_normalize(counts0))
            new_avg1 = tabular_policy(_normalize(counts1))
            avg_gap = nash_gap(game, new_avg0, new_avg1)["nash_conv"]
            last_gap = nash_gap(game, br0, br1)["nash_conv"]
            curve["iter"].append(it)
            curve["avg_nashconv"].append(avg_gap)
            curve["last_nashconv"].append(last_gap)
            print(f"  iter {it:4d}   avg NashConv = {avg_gap:.4f}   "
                  f"last-iterate NashConv = {last_gap:.4f}")

    print("\nPREDICT: avg NashConv trends toward ~0; last-iterate stays large (oscillates).")
    path = save_json("selfplay_vs_nash.json", {"config": cfg, "curve": curve})
    print(f"saved {path}")

    if cfg["save_plot"]:
        _plot(curve)


def _plot(curve):
    plt = get_plt()
    if plt is None:
        print("[plot] matplotlib not installed -> skipping PNG.")
        return
    import os
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(curve["iter"], curve["avg_nashconv"], "-o", ms=3, label="average iterate")
    ax.plot(curve["iter"], curve["last_nashconv"], "-s", ms=3, label="last iterate (pure BR)")
    ax.set_yscale("log")
    ax.set_xlabel("fictitious-play iteration")
    ax.set_ylabel("NashConv (exploitability)")
    ax.set_title("Kuhn self-play: the AVERAGE converges to Nash, the last iterate does not")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    out = os.path.join(figures_dir(), "selfplay_vs_nash.png")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    print(f"[plot] wrote {out}")


if __name__ == "__main__":
    main()
