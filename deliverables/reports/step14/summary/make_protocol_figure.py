"""summary figure: the joint evaluation protocol of Chapter 14.

The bot zoo (stationary, LLM-derived, equilibrium and adaptive agents, plus switching and
teaching opponents) plays fixed-seat duplicate matches over several seeds. Every hand is scored
by three estimators (raw chips, AIVAT, policy-exact). Four readouts are reported together:
gain, speed and recovery, exposure (two-player: worst case below the game value; N-player:
coalition value), and confidence. Population rankings (Layer 2) are reported as context.
Output: protocol.png next to this file. Run from the repo root with the project .venv active.

Text sizes: the figure is saved at ~7 in and prints at 17.6 cm, so fs 10 prints at ~9.5 pt.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save, rc, lc
from _diagram_utils import C_MODEL, C_SAFE, C_NET, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=8.6, xlim=(0, 14), ylim=(0, 8.6), shrink=2.0)
FS = 10

zoo = box(ax, 0.2, 4.0, 3.5, 3.6,
          "BOT ZOO\nequilibria, rule types,\nLLM-derived,\nadaptive (Ch. 7-8);\n"
          "switching and\nteaching opponents", fc=C_MODEL, fs=FS)
match = box(ax, 0.2, 1.3, 3.5, 2.2,
            "MATCHES\nfixed seats, duplicate\ncards, ≥ 3 seeds,\nK hands", fc=C_ANNOT, fs=FS)
est = box(ax, 4.5, 2.6, 3.4, 3.8,
          "PER-HAND\nESTIMATORS\nraw chips\nAIVAT (chance +\nagent known)\npolicy-exact\n(bots only)",
          fc=C_SAFE, fs=FS)

y0, h, gap = 6.4, 1.55, 0.25
gain = box(ax, 8.7, y0, 5.1, h, "GAIN\nabove the blueprint vs a\nsub-optimal population", fc=C_NET, fs=FS)
speed = box(ax, 8.7, y0 - (h + gap), 5.1, h, "SPEED + RECOVERY\nhands to hold half the gain;\nafter an opponent switch",
            fc=C_NET, fs=FS)
expo = box(ax, 8.7, y0 - 2 * (h + gap), 5.1, h,
           "EXPOSURE\n2P: worst case below v*;\nN-player: coalition value", fc=C_EXPLOIT, fs=FS)
conf = box(ax, 8.7, y0 - 3 * (h + gap), 5.1, h,
           "CONFIDENCE\n95 % intervals; estimator and\nexploiter budget named", fc=C_ANNOT, fs=FS)

arrow(ax, (1.95, 4.0), (1.95, 3.5))
arrow(ax, rc(match), lc(est))
for b in (gain, speed, expo, conf):
    arrow(ax, rc(est), lc(b), rad=0.0)

note(ax, 6.2, 0.55,
     "Context, not a verdict: Elo, Nash averaging, α-Rank (α swept), VasE, spinning top",
     fs=FS, color="#2c3e50", style="normal")

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "protocol.png"))
