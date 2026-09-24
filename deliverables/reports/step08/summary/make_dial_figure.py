"""Intro figure: the safety-exploitation dial, with the safety GOVERNOR.

A one-axis schematic from pure safety (Nash) to pure exploitation (hard best response),
marking where SAFE exploitation operates and the "governor" that caps how far the dial
can spin past the point a worst-case adversary could drag you below your baseline.
Output: dial_safe_exploitation.png. Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_SAFE, C_EXPLOIT, C_MODEL, EC
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(w=14, h=5.5, xlim=(0, 14), ylim=(-0.3, 5.2), shrink=1.7)

# the dial as a thick horizontal bar
ax.add_patch(FancyArrowPatch((1.0, 3.6), (13.0, 3.6), arrowstyle="-", lw=10,
                             color="#d7dee6", zorder=1))
note(ax, 1.2, 4.25, "SAFETY", fs=11, color="#2c5a8f", ha="left", style="normal")
note(ax, 12.8, 4.25, "EXPLOITATION", fs=11, color="#a5453a", ha="right", style="normal")

left = box(ax, 0.3, 2.0, 3.7, 1.3, "Nash equilibrium\n(unexploitable, blind)", fc=C_SAFE, fs=10)
mid = box(ax, 4.75, 1.95, 4.45, 1.35, "SAFE exploitation\nmax value s.t.\nworst-case ≥ floor",
          fc=C_MODEL, fs=10, fontweight="bold")
right = box(ax, 9.9, 2.0, 3.8, 1.3, "Full best response\n(max value, max risk)",
            fc=C_EXPLOIT, fs=10)

# short arrows from each box top up to the dial
for b in (left, mid, right):
    x, y, w, h = b
    arrow(ax, (x + w / 2, y + h), (x + w / 2, 3.55))

# the governor: a hard stop past which the dial cannot spin
ax.add_patch(FancyArrowPatch((9.55, 3.15), (9.55, 4.2), arrowstyle="-", lw=2.2,
                             color="#a5453a", zorder=5))
note(ax, 9.55, 4.75, "safety governor", fs=10, color="#a5453a", style="normal")

note(ax, 7.0, 1.3, "the floor is the only thing that differs between methods:\n"
                    "best equilibrium ≥ v*  |  prime-safe ≥ v* − ε\n"
                    "adaptation ≥ blueprint worst case", fs=10)
note(ax, 7.0, 0.55, "Chapter 7 built the SENSOR (the model)", fs=10, color="#2c3e50")
note(ax, 7.0, 0.1, "Chapter 8 builds the ACTUATOR (safe exploitation)", fs=10, color="#2c3e50")

save(fig, "deliverables/reports/step08/summary/dial_safe_exploitation.png")
