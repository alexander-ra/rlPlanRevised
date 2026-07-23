"""Intro figure: the safety-exploitation dial, with the safety GOVERNOR.

A one-axis schematic from pure safety (Nash) to pure exploitation (hard best response),
marking where SAFE exploitation operates and the "governor" that caps how far the dial
can spin past the point a worst-case adversary could drag you below your baseline.
Output: dial_safe_exploitation.png. Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_SAFE, C_EXPLOIT, C_MODEL, EC
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(w=14, h=5.2, xlim=(0, 14), ylim=(0, 5.2), shrink=1.7)

# the dial as a thick horizontal bar
ax.add_patch(FancyArrowPatch((1.0, 3.6), (13.0, 3.6), arrowstyle="-", lw=10,
                             color="#d7dee6", zorder=1))
note(ax, 1.2, 4.25, "SAFETY", fs=11, color="#2c5a8f", ha="left", style="normal")
note(ax, 12.8, 4.25, "EXPLOITATION", fs=11, color="#a5453a", ha="right", style="normal")

left = box(ax, 0.6, 2.3, 3.0, 1.0, "Nash / GTO\n(unexploitable, blind)", fc=C_SAFE, fs=8.6)
mid = box(ax, 5.0, 2.3, 4.0, 1.0, "SAFE exploitation\nmax value s.t. worst-case >= floor",
          fc=C_MODEL, fs=8.4, fontweight="bold")
right = box(ax, 10.4, 2.3, 3.0, 1.0, "Full best response\n(max value, max risk)",
            fc=C_EXPLOIT, fs=8.6)

for b, x in ((left, 2.1), (mid, 7.0), (right, 11.9)):
    arrow(ax, (x, 3.3), (x, 3.55))

# the governor: a hard stop past which the dial cannot spin
ax.add_patch(FancyArrowPatch((9.15, 3.15), (9.15, 4.05), arrowstyle="-", lw=2.2,
                             color="#a5453a", zorder=5))
note(ax, 9.15, 4.35, "safety governor", fs=7.6, color="#a5453a", style="normal")

note(ax, 7.0, 1.65, "the floor is the only thing that differs between methods:\n"
                    "Ganzfried >= Nash value  |  prime-safe >= Nash-eps  |  "
                    "adaptation >= blueprint value", fs=7.8)
note(ax, 3.6, 0.7, "Step 7 built the SENSOR (the model)", fs=8.2, color="#2c3e50")
note(ax, 10.4, 0.7, "Step 8 builds the ACTUATOR (safe exploitation)", fs=8.2, color="#2c3e50")

save(fig, "deliverables/reports/step08/summary/dial_safe_exploitation.png")
