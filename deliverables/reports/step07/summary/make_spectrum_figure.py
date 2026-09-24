"""Optional intro figure: the safety-exploitation dial (sensor vs actuator).

A one-axis schematic from pure safety (Nash) to pure exploitation (hard best
response), marking where opponent modeling operates and the sensor/actuator split
between Chapter 7 and Chapter 8. Output: spectrum_safety_exploitation.png.
Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, tc, bc
from _diagram_utils import C_SAFE, C_EXPLOIT, C_MODEL, C_ANNOT, EC
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(w=14, h=5.6, xlim=(0, 14), ylim=(0, 5.6), shrink=1.7)

# the dial as a thick horizontal gradient-ish bar (two flat halves)
ax.add_patch(FancyArrowPatch((1.0, 4.1), (13.0, 4.1), arrowstyle="-", lw=10,
                             color="#d7dee6", zorder=1))
note(ax, 1.0, 4.75, "SAFETY", fs=11, color="#2c5a8f", ha="left", style="normal")
note(ax, 13.0, 4.75, "EXPLOITATION", fs=11, color="#a5453a", ha="right", style="normal")

# boxes sized for the longer Bulgarian labels at fs 10 (prints at ~8.5 pt)
left = box(ax, 0.3, 2.35, 3.8, 1.3, "Nash / GTO\n(unexploitable, blind)", fc=C_SAFE, fs=10)
mid = box(ax, 5.0, 2.35, 4.0, 1.3, "Model + bounded\ndeviation", fc=C_MODEL, fs=10,
          fontweight="bold")
right = box(ax, 9.9, 2.35, 3.8, 1.3, "Hard best response\n(max value, max risk)",
            fc=C_EXPLOIT, fs=10)

for b in (left, mid, right):
    x = b[0] + b[2] / 2
    arrow(ax, (x, 3.65), (x, 3.95))

note(ax, 7.0, 1.7, "opponent modeling lives here: extract value from earned reads,\n"
                   "cap how exploitable you let yourself become", fs=10)
# the two chapter notes are stacked, not side by side: the Bulgarian strings are
# longer than the gap between two centred columns and ran into each other
note(ax, 7.0, 0.95, "Chapter 7 builds the SENSOR (the model)", fs=10, color="#2c3e50")
note(ax, 7.0, 0.45, "Chapter 8 builds the ACTUATOR (safe exploitation)", fs=10, color="#2c3e50")

save(fig, "deliverables/reports/step07/summary/spectrum_safety_exploitation.png")
