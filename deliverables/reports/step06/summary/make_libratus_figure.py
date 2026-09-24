"""Generate Figure 6.2 for the Step 6 summary: Libratus architecture.

Three stacked panels (offline blueprint / online nested safe subgame solving /
overnight self-improver) with a feedback arrow from the bottom panel back into
the blueprint, and a dashed arrow carrying the blueprint's value estimate into
the online gadget. All text is fs 10 (titles 11) on a 7.9 in canvas, i.e.
>= 8.2 pt in print; the boxes are sized for the longer Bulgarian labels, and
no note or arrow crosses a box.
Output: libratus_arch.png in this directory.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _diagram_utils import (
    box, rc, lc, tc, bc, cc, arrow, panel_bg, note, new_fig, save,
    C_OFFLINE, C_ONLINE, C_ANNOT, C_NET, C_WARN, EC,
)

FS = 10
VAL = "#8a6d1a"   # value-estimate link
FB = "#7a1f1f"    # overnight feedback

fig, ax = new_fig(w=15.8, h=18.97, xlim=(0, 16.2), ylim=(0.0, 19.45), shrink=2.0)

panel_bg(ax, 0.15, 13.15, 15.9, 6.1, C_OFFLINE, label="OFFLINE: build the blueprint (before play)",
         label_fs=11, label_ha="left")
panel_bg(ax, 0.15, 4.3, 15.9, 8.15, C_ONLINE,
         label="ONLINE: nested safe subgame solving (every late decision)", label_fs=11, label_ha="left")
panel_bg(ax, 0.15, 0.2, 15.9, 3.55, "#f7ecd8", label="OVERNIGHT: self-improver (between days)",
         label_fs=11, label_ha="left")

# ================= TOP: offline blueprint =================
t1 = box(ax, 0.35, 16.35, 15.25, 2.2,
         "Abstract the game: action abstraction (asymmetric bet-size menu)\n+ card abstraction ONLY on turn/river (55M→2.5M turn;\n2.4B→1.25M river); NONE on pre-flop/flop\n10¹⁶¹ → ~10¹² decision points",
         fc="white", fs=FS)
t2 = box(ax, 0.35, 13.45, 7.45, 2.6,
         "Solve with MCCFR +\nregret-based pruning (self-play;\nskips very-negative-regret\nbranches; ~3× speedup)",
         fc="white", fs=FS)
t3 = box(ax, 8.15, 13.45, 7.45, 2.6,
         "Blueprint strategy — crisp on\nrounds 1–2, blurry on rounds 3–4\n(late-round numbers only estimate\nthe value of reaching a subgame)",
         fc=C_NET, fs=FS, lw=1.7)
arrow(ax, (bc(t2)[0], t1[1]), tc(t2))
arrow(ax, rc(t2), lc(t3))

# ================= MIDDLE: online nested safe subgame solving =================
m1 = box(ax, 0.35, 9.2, 3.1, 2.6, "Play the\nblueprint on\nrounds 1–2", fc="white", fs=FS)
m2 = box(ax, 3.85, 9.2, 5.25, 2.6,
         "Reach round 3 (or a\nsmall-enough subtree):\nbuild a finer subgame,\nNO card abstraction",
         fc="white", fs=FS)
m3 = box(ax, 9.5, 9.2, 3.3, 2.6, "Solve an\nAUGMENTED\nsubgame\nwith CFR+", fc="white", fs=FS)
m4 = box(ax, 13.35, 9.2, 2.25, 2.6, "Act", fc="white", fs=FS)
arrow(ax, rc(m1), lc(m2))
arrow(ax, rc(m2), lc(m3))
arrow(ax, rc(m3), lc(m4))
note(ax, 1.9, 7.5, "off-tree bets\nhere are\nROUNDED —\nresidual\nweakness", fs=FS, color="#a33")

gadget = box(ax, 3.85, 6.2, 9.35, 2.6,
             "Gadget (at the augmented root): opponent\nchooses — \"alternative payoff\"\n(blueprint's value estimate)\nvs. \"enter the detailed subgame\"",
             fc=C_ANNOT, fs=FS)
arrow(ax, bc(m3), (bc(m3)[0], gadget[1] + gadget[3]), style="-")

# blueprint value estimate -> gadget: straight down the gap between m3 and m4
VX = 13.07
arrow(ax, (VX, t3[1]), (VX, gadget[1] + gadget[3]), dashed=True, color=VAL)
note(ax, VX - 0.2, 12.8, "blueprint supplies the value estimate", fs=FS, color=VAL, ha="right")

# nested: every later off-tree bet builds a new augmented subgame
arrow(ax, bc(m4), rc(gadget), rad=-0.35, lw=1.6)
note(ax, 8.1, 5.3,
     "opponent bets off-tree → re-solve a new AUGMENTED subgame\nincluding that bet (nested); Libratus also perturbs its own\nbet sizes by ±0–8% at the first solve",
     fs=FS, ha="center")

# ================= BOTTOM: overnight self-improver =================
o1 = box(ax, 0.35, 0.45, 4.65, 2.6, "Collect opponents'\nmost-used off-menu\nbet sizes from the day", fc="white", fs=FS)
o2 = box(ax, 5.45, 0.45, 4.9, 2.6, "Pick k≈3 holes\n(by frequency ×\ndistance from nearest\nabstract action)", fc="white", fs=FS)
o3 = box(ax, 10.8, 0.45, 4.8, 2.6, "Solve those branches\nto equilibrium overnight\nand graft into\nthe blueprint", fc="white", fs=FS)
arrow(ax, rc(o1), lc(o2))
arrow(ax, rc(o2), lc(o3))

# feedback loop: overnight -> blueprint (right margin)
MX = 15.9
arrow(ax, rc(o3), (MX, rc(o3)[1]), style="-", lw=2.0, color=FB)
arrow(ax, (MX, rc(o3)[1]), (MX, rc(t3)[1]), style="-", lw=2.0, color=FB)
arrow(ax, (MX, rc(t3)[1]), rc(t3), lw=2.0, color=FB, mutation_scale=14, shrinkA=0)
note(ax, MX - 0.2, 4.03, "feedback: graft into blueprint", fs=FS, color=FB, ha="right")

save(fig, str(Path(__file__).parent / "libratus_arch.png"))
