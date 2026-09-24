"""Section 2/4 figure: one LP engine, five safety floors.

The sequence-form treeplex yields a linear objective (EV vs the model); a constraint-
generation loop calls an exact best response as the worst-case oracle and adds a safety
cut until the floor is met. The five method families are the SAME solve with a different
floor. Output: one_lp_engine.png. Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, rc, lc, tc, bc, cc
from _diagram_utils import C_SAFE, C_MODEL, C_NET, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=7.3, xlim=(0, 14), ylim=(1.1, 8.4), shrink=1.7)

# --- the core solve (left column) ---
sf = box(ax, 0.2, 6.4, 3.8, 1.2, "SequenceForm\n(hero treeplex, reused)", fc=C_ANNOT, fs=10)
pv = box(ax, 0.2, 4.4, 3.8, 1.2, "Payoff vector c\nEV vs model = c · x", fc=C_MODEL, fs=10)
lp = box(ax, 0.2, 2.2, 3.8, 1.7, "seq-form LP\nmax c · x  s.t.\ntreeplex + safety cuts",
         fc=C_NET, fs=10, fontweight="bold")
arrow(ax, bc(sf), tc(pv))
arrow(ax, bc(pv), tc(lp))

# --- constraint generation loop (middle) ---
br = box(ax, 4.35, 4.4, 4.05, 1.2, "exact best response\n(worst-case oracle, Chapter 7)",
         fc=C_EXPLOIT, fs=10)
chk = box(ax, 4.35, 2.2, 4.05, 1.8, "worst-case ≥ floor ?\nno → add cut\nc_adv · x ≥ floor\n"
          "yes → done", fc=C_SAFE, fs=10)
arrow(ax, rc(lp), lc(chk))
arrow(ax, tc(chk), bc(br))
arrow(ax, lc(br), (4.0, 5.0), rad=-0.2)   # cut fed back into the LP
note(ax, 6.4, 6.05, "double-oracle\ncutting-plane loop", fs=10, color="#2c3e50")

# --- five floors (right column) ---
note(ax, 11.2, 8.15, "same solve, different FLOOR:", fs=10, color="#2c3e50")
rows = [
    ("RNR (Johanson)", "tunable via p (max-min)"),
    ("best equilibrium (Ganzfried–Sandholm)", "floor = Nash value v*"),
    ("prime-safe (Jeary)", "floor = v* − ε"),
    ("SES subgame (Liu)", "blueprint value, LOCAL gadget"),
    ("adaptation (Ge)", "≤ blueprint exploitability"),
]
y = 6.9
for name, desc in rows:
    b = box(ax, 8.55, y, 5.4, 0.9, f"{name}\n{desc}", fc=C_ANNOT, fs=10)
    arrow(ax, rc(chk), lc(b), rad=0.12, lw=1.0)
    y -= 1.02

note(ax, 6.9, 1.6, "one validated primitive (Chapter 7's exact best response)\n"
                   "powers BOTH the objective and every safety check", fs=10)

save(fig, "deliverables/reports/step08/summary/one_lp_engine.png")
