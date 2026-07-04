"""Optional intro figure: the safety-exploitation dial (sensor vs actuator).

A one-axis schematic from pure safety (Nash) to pure exploitation (hard best
response), marking where opponent modeling operates and the sensor/actuator split
between Step 7 and Step 8. Output: spectrum_safety_exploitation.png.
Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, tc, bc
from _diagram_utils import C_SAFE, C_EXPLOIT, C_MODEL, C_ANNOT, EC
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(w=14, h=5.0, xlim=(0, 14), ylim=(0, 5.0), shrink=1.7)

# the dial as a thick horizontal gradient-ish bar (two flat halves)
ax.add_patch(FancyArrowPatch((1.0, 3.4), (13.0, 3.4), arrowstyle="-", lw=10,
                             color="#d7dee6", zorder=1))
note(ax, 1.2, 4.05, "SAFETY", fs=11, color="#2c5a8f", ha="left", style="normal")
note(ax, 12.8, 4.05, "EXPLOITATION", fs=11, color="#a5453a", ha="right", style="normal")

left = box(ax, 0.6, 2.1, 3.0, 1.0, "Nash / GTO\n(unexploitable, blind)", fc=C_SAFE, fs=8.6)
mid = box(ax, 5.2, 2.1, 3.6, 1.0, "Model + bounded\ndeviation", fc=C_MODEL, fs=8.8,
          fontweight="bold")
right = box(ax, 10.4, 2.1, 3.0, 1.0, "Hard best response\n(max value, max risk)",
            fc=C_EXPLOIT, fs=8.6)

for b, x in ((left, 2.1), (mid, 7.0), (right, 11.9)):
    arrow(ax, (x, 3.1), (x, 3.35))

note(ax, 7.0, 1.5, "opponent modeling lives here: extract value from earned reads,\n"
                   "cap how exploitable you let yourself become", fs=8.0)
note(ax, 3.6, 0.6, "Step 7 builds the SENSOR (the model)", fs=8.2, color="#2c3e50")
note(ax, 10.4, 0.6, "Step 8 builds the ACTUATOR (safe exploitation)", fs=8.2, color="#2c3e50")

save(fig, "deliverables/reports/step07/summary/spectrum_safety_exploitation.png")
