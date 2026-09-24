"""Figure for § "Pipeline 2 — HSD + EMD + k-means + imperfect recall".

Replaces the earlier k-means scatter (day01_infoset_clustering.py), which
clustered seven mixed card/betting features and so did not show the HSD +
EMD bucketing the section describes (final review F04-G02).

Everything is computed by the chapter's own code — no training:
  - left:  the pre-flop hand-strength distributions (HSD) of the three
           private cards, from phase4/day02_hand_strength.hsd_pre_flop;
  - right: the post-flop hand strength of the nine (private, public) card
           combinations, coloured by the k-means-with-EMD bucket that
           phase4/day02_card_bucketing.build_card_buckets assigns with
           k = 3; k = 5 gives the identical partition (checked below),
           which is why the k3 and k5 abstractions coincide.

Output: leduc_hsd.png beside this script (Bulgarian twin via
scripts/figures/render_bg_figures.py).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PHASE4 = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                      "implementation", "step04", "phase4"))
if PHASE4 not in sys.path:
    sys.path.insert(0, PHASE4)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402

from day02_hand_strength import (  # noqa: E402
    NUM_RANKS, _bin_index, hand_strength_at_showdown, hsd_pre_flop)
from day02_card_bucketing import build_card_buckets  # noqa: E402

OUT = os.path.join(HERE, "leduc_hsd.png")
CARDS = ["Jack", "Queen", "King"]
CARD_COLOURS = ["#1f77b4", "#d95f02", "#1b9e77"]
# decimal strings are passed as whole labels so the Bulgarian twin can
# swap in the decimal comma through the label mapping
FMT = {1 / 6: "0.17", 1 / 2: "0.50", 5 / 6: "0.83"}


def _fmt(v: float) -> str:
    return min(FMT.items(), key=lambda kv: abs(kv[0] - v))[1]


def main() -> None:
    fig, (ax_l, ax_r) = plt.subplots(
        1, 2, figsize=(8, 3.6), gridspec_kw={"width_ratios": [1.35, 1]})

    # -- left: pre-flop HSDs ------------------------------------------------
    width = 0.045
    for p in range(NUM_RANKS):
        hist = hsd_pre_flop(p)
        # each non-empty HSD bin holds one exact showdown strength; draw the
        # bar at that value rather than at the bin centre
        exact = {_bin_index(hand_strength_at_showdown(p, c)):
                 hand_strength_at_showdown(p, c) for c in range(NUM_RANKS)}
        xs = [exact[i] for i, v in enumerate(hist) if v > 0]
        ys = [v for v in hist if v > 0]
        mean_hs = sum(x * y for x, y in zip(xs, ys))
        ax_l.bar([x + (p - 1) * width for x in xs], ys, width=width,
                 color=CARD_COLOURS[p],
                 label=f"{CARDS[p]} (mean {mean_hs:.2f})")
    ax_l.set_xlim(0, 1)
    ax_l.set_ylim(0, 1.42)
    ax_l.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax_l.set_xticks([0, 1 / 6, 1 / 2, 5 / 6, 1])
    ax_l.set_xticklabels(["0", "0.17", "0.50", "0.83", "1"])
    ax_l.set_xlabel("Hand strength at showdown", fontsize=11)
    ax_l.set_ylabel("Probability", fontsize=11)
    ax_l.set_title("Before the public card", fontsize=11)
    ax_l.tick_params(labelsize=10)
    ax_l.legend(fontsize=10, frameon=False, loc="upper center")
    ax_l.grid(True, axis="y", linestyle="--", alpha=0.3)

    # -- right: post-flop strengths and their buckets -----------------------
    b3 = build_card_buckets(NUM_RANKS, 3)["postflop"]
    b5 = build_card_buckets(NUM_RANKS, 5)["postflop"]
    assert b3 == b5, "k = 3 and k = 5 no longer coincide; update the caption"
    strength = [[hand_strength_at_showdown(p, c) for c in range(NUM_RANKS)]
                for p in range(NUM_RANKS)]
    # colour each cell by its bucket, ordered by the bucket's strength
    order = sorted(set(b3.values()),
                   key=lambda b: min(strength[p][c]
                                     for (p, c), bb in b3.items() if bb == b))
    rank_of = {b: i for i, b in enumerate(order)}
    grid = [[rank_of[b3[(p, c)]] for c in range(NUM_RANKS)]
            for p in range(NUM_RANKS)]
    cmap = ListedColormap(["#deebf7", "#9ecae1", "#3182bd"])
    ax_r.imshow(grid, cmap=cmap, vmin=-0.5, vmax=2.5)
    for p in range(NUM_RANKS):
        for c in range(NUM_RANKS):
            ax_r.text(c, p, _fmt(strength[p][c]), ha="center", va="center",
                      fontsize=10,
                      color="white" if grid[p][c] == 2 else "black")
    ax_r.set_xticks(range(NUM_RANKS))
    ax_r.set_yticks(range(NUM_RANKS))
    ax_r.set_xticklabels(CARDS)
    ax_r.set_yticklabels(CARDS)
    ax_r.set_xlabel("Public card", fontsize=11)
    ax_r.set_ylabel("Private card", fontsize=11)
    ax_r.set_title("After the public card", fontsize=11)
    ax_r.tick_params(labelsize=10, length=0)

    fig.tight_layout()
    fig.savefig(OUT, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {OUT}")


if __name__ == "__main__":
    main()
