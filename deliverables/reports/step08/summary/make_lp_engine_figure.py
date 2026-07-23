"""Section 2/4 figure: one LP engine, five safety floors.

The sequence-form treeplex yields a linear objective (EV vs the model); a constraint-
generation loop calls an exact best response as the worst-case oracle and adds a safety
cut until the floor is met. The five method families are the SAME solve with a different
floor. Output: one_lp_engine.png. Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, rc, lc, tc, bc, cc
from _diagram_utils import C_SAFE, C_MODEL, C_NET, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=8.4, xlim=(0, 14), ylim=(0, 8.4), shrink=1.7)

# --- the core solve (left column) ---
sf = box(ax, 0.4, 6.4, 3.1, 1.2, "SequenceForm\n(hero treeplex, reused)", fc=C_ANNOT, fs=8.2)
pv = box(ax, 0.4, 4.4, 3.1, 1.2, "Payoff vector c\nEV vs model = c . x", fc=C_MODEL, fs=8.2)
lp = box(ax, 0.4, 2.4, 3.1, 1.3, "seq-form LP\nmax c . x  s.t.\ntreeplex + safety cuts",
         fc=C_NET, fs=8.2, fontweight="bold")
arrow(ax, bc(sf), tc(pv))
arrow(ax, bc(pv), tc(lp))

# --- constraint generation loop (middle) ---
br = box(ax, 4.8, 4.4, 3.2, 1.2, "exact best response\n(worst-case oracle, Step 7)",
         fc=C_EXPLOIT, fs=8.2)
chk = box(ax, 4.8, 2.4, 3.2, 1.3, "worst-case >= floor ?\nno -> add cut c_adv . x >= floor\n"
          "yes -> done", fc=C_SAFE, fs=7.8)
arrow(ax, rc(lp), lc(chk))
arrow(ax, tc(chk), bc(br))
arrow(ax, lc(br), (3.5, 5.0), rad=-0.2)   # cut fed back into the LP
note(ax, 4.15, 5.9, "double-oracle\ncutting-plane loop", fs=7.4, color="#2c3e50")

# --- five floors (right column) ---
note(ax, 11.3, 7.9, "same solve, different FLOOR:", fs=8.4, color="#2c3e50")
rows = [
    ("RNR (Johanson)", "tunable via p (max-min)"),
    ("Ganzfried", "floor = Nash value v*"),
    ("prime-safe (Jeary)", "floor = v* - eps"),
    ("SES subgame (Liu)", "blueprint value, LOCAL gadget"),
    ("adaptation (Ge)", "<= blueprint exploitability"),
]
y = 6.9
for name, desc in rows:
    b = box(ax, 9.2, y, 4.4, 0.82, f"{name}\n{desc}", fc=C_ANNOT, fs=7.6)
    arrow(ax, rc(chk), lc(b), rad=0.12, lw=1.0)
    y -= 1.02

note(ax, 6.9, 0.6, "one validated primitive (Step 7's exact best response) powers BOTH the "
                   "objective and every safety check", fs=7.8)

save(fig, "deliverables/reports/step08/summary/one_lp_engine.png")
