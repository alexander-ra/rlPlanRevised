"""Generate Figure 6.2 for the Step 6 summary: Libratus architecture.

Three stacked panels (offline blueprint / online nested safe subgame solving /
overnight self-improver) with a feedback arrow from the bottom panel back into
the blueprint, and a dashed arrow carrying the blueprint's value estimate into
the online gadget. Output: libratus_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_ANNOT, C_NET, C_WARN, EC,
)

fig, ax = new_fig(w=15.8, h=11.6, xlim=(0, 16.2), ylim=(0.3, 13.3))

panel_bg(ax, 0.15, 9.3, 15.9, 3.7, C_OFFLINE, label="OFFLINE: build the blueprint (before play)")
panel_bg(ax, 0.15, 3.5, 15.9, 5.5, C_ONLINE, label="ONLINE: nested safe subgame solving (every late decision)")
panel_bg(ax, 0.15, 0.4, 15.9, 2.7, "#f7ecd8", label="OVERNIGHT: self-improver (between days)")

# ================= TOP: offline blueprint =================
t1 = box(ax, 0.4, 9.75, 5.0, 2.7,
          "Abstract the game: action\nabstraction (asymmetric bet-size\nmenu) + card abstraction ONLY on\nturn/river (55M→2.5M turn;\n2.4B→1.25M river); NONE on\npre-flop/flop\n10¹⁶¹ → ~10¹² decision points",
          fc="white", fs=7.6)
t2 = box(ax, 5.9, 10.2, 3.9, 2.0,
          "Solve with MCCFR +\nregret-based pruning\n(self-play; skips very-negative-\nregret branches; ~3× speedup)",
          fc="white", fs=8.0)
t3 = box(ax, 10.3, 10.2, 5.4, 2.0,
          "Blueprint strategy — crisp on\nrounds 1–2, blurry on rounds 3–4\n(late-round numbers only estimate\nthe value of reaching a subgame)",
          fc=C_NET, fs=8.0, lw=1.7)
arrow(ax, rc(t1), lc(t2))
arrow(ax, rc(t2), lc(t3))

# ================= MIDDLE: online nested safe subgame solving =================
m1 = box(ax, 0.4, 6.5, 3.5, 1.55, "Play the blueprint\non rounds 1–2", fc="white", fs=8.3)
note(ax, 2.15, 6.15, "off-tree opponent bets here are\nROUNDED — residual weakness", fs=7.2, color="#a33")
m2 = box(ax, 4.35, 6.5, 3.5, 1.55,
          "Reach round 3 (or a small-\nenough subtree): build a finer\nsubgame, NO card abstraction",
          fc="white", fs=7.6)
m3 = box(ax, 8.3, 6.5, 3.5, 1.55, "Solve an AUGMENTED\nsubgame with CFR+", fc="white", fs=8.3)
m4 = box(ax, 12.25, 6.5, 3.5, 1.55, "Act", fc="white", fs=9.5)
arrow(ax, rc(m1), lc(m2))
arrow(ax, rc(m2), lc(m3))
arrow(ax, rc(m3), lc(m4))

gadget = box(ax, 6.6, 4.4, 4.9, 1.9,
             "Gadget (at the augmented root): opponent\nchooses — \"alternative payoff\" (blueprint's\nvalue estimate) vs. \"enter the detailed subgame\"",
             fc=C_ANNOT, fs=7.6)
arrow(ax, bc(m3), tc(gadget))
arrow(ax, (t3[0] + 1.2, t3[1]), (gadget[0] + gadget[2] - 0.6, gadget[1] + gadget[3]),
      dashed=True, color="#8a6d1a", rad=0.15)
note(ax, 13.3, 5.55, "blueprint supplies\nthe value estimate", fs=7.0, color="#8a6d1a")

arrow(ax, bc(m4), (m2[0] + m2[2] * 0.5, m2[1]), rad=-0.55, lw=1.6)
note(ax, 8.1, 3.75, "opponent bets off-tree → re-solve a new AUGMENTED subgame\nincluding that bet (nested); Libratus also perturbs its own bet\nsizes ±0–8% at the first solve", fs=7.2, ha="center")

# ================= BOTTOM: overnight self-improver =================
o1 = box(ax, 0.6, 1.0, 4.4, 1.5, "Collect opponents' most-used\noff-menu bet sizes from the day", fc="white", fs=8.3)
o2 = box(ax, 5.6, 1.0, 3.9, 1.5, "Pick k≈3 holes (by frequency\n× distance from nearest\nabstract action)", fc="white", fs=8.0)
o3 = box(ax, 10.1, 1.0, 5.6, 1.5, "Solve those branches to equilibrium\novernight and graft into the blueprint", fc="white", fs=8.2)
arrow(ax, rc(o1), lc(o2))
arrow(ax, rc(o2), lc(o3))

# feedback loop: overnight -> blueprint (margin route, right side)
MX = 16.05
arrow(ax, rc(o3), (MX, o3[1] + o3[3] / 2), style="-", lw=2.0, color="#7a1f1f")
arrow(ax, (MX, o3[1] + o3[3] / 2), (MX, t3[1] + t3[3] / 2), style="-", lw=2.0, color="#7a1f1f")
arrow(ax, (MX, t3[1] + t3[3] / 2), rc(t3), lw=2.0, color="#7a1f1f", mutation_scale=14)
note(ax, 15.55, 7.5, "feedback:\ngraft into\nblueprint", fs=7.2, color="#7a1f1f", ha="right")

save(fig, str(Path(__file__).parent / "libratus_arch.png"))
