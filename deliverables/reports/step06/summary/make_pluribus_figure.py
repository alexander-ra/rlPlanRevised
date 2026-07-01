"""Generate Figure 6.3 for the Step 6 summary: Pluribus architecture.

Two stacked panels (offline Linear-MCCFR blueprint / online depth-limited
search with continuation strategies), with the blueprint block reused
(highlighted, dashed arrow) inside the bottom panel's leaf gadget.
Output: pluribus_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_ANNOT, C_NET, EC,
)

fig, ax = new_fig(w=15.8, h=9.3, xlim=(0, 16.2), ylim=(-0.3, 10.7))

panel_bg(ax, 0.15, 7.1, 15.9, 3.5, C_OFFLINE,
         label="OFFLINE: blueprint by self-play (one 64-core server, ~$150)")
panel_bg(ax, 0.15, 0.4, 15.9, 6.5, C_ONLINE,
         label="ONLINE: depth-limited search (every decision on rounds 2–4)")

# ================= TOP: offline blueprint =================
p1 = box(ax, 0.4, 7.55, 5.0, 2.15,
          "Abstract the 6-max game:\naction abstraction (1–14 pot-\nfraction bet sizes; fine round 1,\ncoarse rounds 3–4) + information\nabstraction (lossless round 1;\n~200 buckets/round later)",
          fc="white", fs=7.7)
p2 = box(ax, 5.7, 7.85, 4.0, 1.55,
          "Solve by Linear MCCFR:\nexternal-sampling MCCFR,\nlinear iteration-weighting +\nmodified negative-regret pruning\n(skip regret ≲ −3×10⁸ on 95% of\niterations, except the last round)",
          fc="white", fs=7.0)
p3 = box(ax, 10.0, 7.85, 5.7, 1.55,
          "Blueprint strategy — crisp on\nround 1, increasingly blurry on\nrounds 2–4 (played directly only\non round 1; a scaffold thereafter)",
          fc=C_NET, fs=7.6, lw=1.7)
arrow(ax, rc(p1), lc(p2))
arrow(ax, rc(p2), lc(p3))
note(ax, 2.9, 7.35, "no neural network; no human data", fs=7.4)

# ================= BOTTOM: online depth-limited search =================
q1 = box(ax, 0.4, 4.55, 3.7, 1.7,
          "Current public state → set\nsubgame root at the START of\nthe current betting round\n(chance node over hand-belief\ndistribution)", fc="white", fs=7.3)
q2 = box(ax, 4.5, 4.55, 3.5, 1.7,
          "Build a finer-grained subgame\n(lossless on current round;\n~500 buckets/round later;\n1–6 bet sizes)", fc="white", fs=7.4)
q3 = box(ax, 8.4, 4.55, 3.3, 1.7,
          "Solve in real time with\nLinear CFR (depth limit a\nround or two ahead)", fc="white", fs=7.6)
q5 = box(ax, 12.1, 4.55, 3.6, 1.7, "Act on the\nfinal iterate", fc="white", fs=9.0)

arrow(ax, rc(q1), lc(q2))
arrow(ax, rc(q2), lc(q3))
arrow(ax, rc(q3), lc(q5))

q4 = box(ax, 3.6, 2.15, 8.6, 2.05,
          "At each LEAF: each remaining player picks one of k=4\ncontinuation strategies — the blueprint, or the blueprint\nbiased toward fold / call / raise — and the rest of the hand\nis rolled out under the chosen strategies to value the leaf",
          fc=C_ANNOT, fs=7.6)
arrow(ax, bc(q3), tc(q4))
arrow(ax, (p3[0] + 1.0, p3[1]), (q4[0] + q4[2] - 1.2, q4[1] + q4[3]),
      dashed=True, color="#8a6d1a", rad=0.12)
note(ax, 12.8, 7.35, "blueprint is the source of\nthe k=4 continuation strategies", fs=7.0, color="#8a6d1a")

arrow(ax, bc(q5), (q1[0] + q1[2] * 0.5, q1[1]), rad=-0.32, lw=1.6)
note(ax, 8.1, 0.15, "any off-tree opponent bet → add that exact bet\nand re-solve from the current round's root", fs=7.3, ha="center")

save(fig, str(Path(__file__).parent / "pluribus_arch.png"))
