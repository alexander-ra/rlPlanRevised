"""Generate Figure 6.3 for the Step 6 summary: Pluribus architecture.

Two stacked panels (offline Linear-MCCFR blueprint / online depth-limited
search with continuation strategies), with the blueprint block reused
(highlighted, dashed arrow) as the source of the leaf continuation strategies.
The online decision is drawn as a cycle: current state -> finer subgame ->
real-time solve -> leaf evaluation -> act on the final iterate -> next
decision. All text is fs 10 (titles 11) on a 7.9 in canvas, i.e. >= 8.2 pt
in print; the boxes are sized for the longer Bulgarian labels, and the dashed
arrow runs down the gap between two boxes instead of across one.
Output: pluribus_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_ANNOT, C_NET, EC,
)

FS = 10
VAL = "#8a6d1a"

fig, ax = new_fig(w=15.8, h=18.73, xlim=(0, 16.2), ylim=(0.1, 19.3), shrink=2.0)

panel_bg(ax, 0.15, 11.85, 15.9, 7.25, C_OFFLINE,
         label="OFFLINE: blueprint by self-play (one 64-core server, ~$150)", label_fs=11, label_ha="left")
# the online title takes two lines so that it ends left of the dashed arrow
panel_bg(ax, 0.15, 0.3, 15.9, 10.35, C_ONLINE)
ax.text(0.4, 10.45, "ONLINE: depth-limited search\n(every decision on rounds 2–4)", ha="left", va="top",
        fontsize=11, fontweight="bold", color="#2c3e50", zorder=1)

# ================= TOP: offline blueprint =================
p1 = box(ax, 0.35, 14.25, 7.2, 4.1,
         "Abstract the 6-max game: action\nabstraction (1–14 pot-fraction bet\nsizes; fine round 1, coarse rounds\n3–4) + information abstraction\n(lossless round 1; ~200 buckets\nper round later)",
         fc="white", fs=FS)
p2 = box(ax, 8.05, 14.25, 7.55, 4.1,
         "Solve by Linear MCCFR:\nexternal-sampling MCCFR,\nlinear iteration-weighting +\nmodified negative-regret pruning\n(skip regret ≲ −3×10⁸ on 95% of\niterations, except the last round)",
         fc="white", fs=FS)
p3 = box(ax, 0.35, 12.15, 11.2, 1.7,
         "Blueprint strategy — crisp on round 1, increasingly\nblurry on rounds 2–4 (played directly only on\nround 1; a scaffold thereafter)",
         fc=C_NET, fs=FS, lw=1.7)
arrow(ax, rc(p1), lc(p2))
arrow(ax, (10.5, p2[1]), (10.5, p3[1] + p3[3]))
note(ax, 13.75, 13.0, "no neural network;\nno human data", fs=FS)

# ================= BOTTOM: online depth-limited search =================
q1 = box(ax, 0.35, 5.7, 5.5, 3.6,
         "Current public state →\nset the subgame root\nat the START of the\ncurrent betting round\n(chance node over\nhand-belief distribution)",
         fc="white", fs=FS)
q2 = box(ax, 6.2, 5.7, 4.8, 3.6,
         "Build a finer-grained\nsubgame (lossless on\ncurrent round; ~500\nbuckets/round later;\n1–6 bet sizes)", fc="white", fs=FS)
q3 = box(ax, 11.35, 5.7, 4.3, 3.6,
         "Solve in real\ntime with Linear\nCFR (depth limit:\na round or two\nahead)", fc="white", fs=FS)
q4 = box(ax, 6.2, 1.6, 9.45, 3.6,
         "At each LEAF: each remaining player picks\none of k=4 continuation strategies — the\nblueprint, or the blueprint biased toward\nfold / call / raise — and the rest of the\nhand is rolled out under the chosen\nstrategies to value the leaf",
         fc=C_ANNOT, fs=FS)
q5 = box(ax, 0.35, 1.6, 5.5, 3.6, "Act on the\nfinal iterate", fc="white", fs=FS)

arrow(ax, rc(q1), lc(q2))
arrow(ax, rc(q2), lc(q3))
arrow(ax, bc(q3), (bc(q3)[0], q4[1] + q4[3]))
arrow(ax, lc(q4), rc(q5))
arrow(ax, tc(q5), bc(q1), lw=1.6)

# blueprint -> source of the leaf continuation strategies (gap between q2 and q3)
VX = 11.17
arrow(ax, (VX, p3[1]), (VX, q4[1] + q4[3]), dashed=True, color=VAL)
note(ax, VX - 0.2, 11.25, "blueprint is the source of the\nk=4 continuation strategies", fs=FS, color=VAL, ha="right")

note(ax, 8.1, 0.95, "any off-tree opponent bet → add that exact bet\nand re-solve from the current round's root", fs=FS, ha="center")

save(fig, str(Path(__file__).parent / "pluribus_arch.png"))
