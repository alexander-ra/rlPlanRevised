"""summary figure: the coalition-aware MAPPO reward blend and the alpha knob.

Each SLS seat is a masked episodic PPO agent trained by self-play with a BLENDED reward, exactly as
in coalition_mappo.py: r = alpha * sparse_winner_reward + (1 - alpha) * Shapley_coalition_credit,
so alpha = 1 is the win reward only and alpha = 0 the credit only. The measured headline (5-seed
paired sweep) is that alpha is the dominant knob: the coalition score rises SIGNIFICANTLY only at
low alpha, and in the scale tier every alpha >= 0.3 cell is negative; the cheap critic-value proxy
has a larger effect than the rollout credit; and the credit costs win rate. (As implemented, the
credit carries no coalition information - see the chapter text.) Output: mappo_blend.png. Run with
the project .venv active; the PNG lands next to this file.

Text sizes: the figure prints at 17.6 cm (scale ~0.87), so fs 10 prints at ~8.7 pt.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_NET, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.4, xlim=(0, 14), ylim=(0, 7.4), shrink=1.7)

sparse = box(ax, 0.3, 5.3, 3.6, 1.4, "Sparse reward\n$r_{\\text{sparse}}$\n(winner takes all)", fc=C_SAFE, fs=10)
credit = box(ax, 0.3, 3.55, 3.6, 1.4, "Shapley coalition\ncredit (proxy\nor rollouts)", fc=C_MODEL, fs=10, fontweight="bold")
blend = box(ax, 4.5, 4.4, 4.3, 1.4,
            "BLEND\n$r = \\alpha\\,r_{\\text{sparse}} + (1-\\alpha)\\,\\text{credit}$", fc=C_NET, fs=10, fontweight="bold")
ppo = box(ax, 9.4, 4.4, 4.3, 1.4, "Masked episodic PPO\nself-play (4 seats)", fc=C_SAFE, fs=10, fontweight="bold")

arrow(ax, (sparse[0] + sparse[2], sparse[1] + sparse[3] / 2), (blend[0], blend[1] + blend[3] / 2 + 0.35), rad=-0.12)
arrow(ax, (credit[0] + credit[2], credit[1] + credit[3] / 2), (blend[0], blend[1] + blend[3] / 2 - 0.35), rad=0.12)
arrow(ax, (blend[0] + blend[2], blend[1] + blend[3] / 2), (ppo[0], ppo[1] + ppo[3] / 2))

note(ax, 7.0, 7.1,
     "$\\alpha$ sets the balance: $\\alpha=1$ → win reward only (\"just win\"), $\\alpha=0$ → coalition credit only.",
     fs=10, color="#2c3e50", style="normal")

sweep = box(ax, 0.3, 0.3, 8.9, 3.0,
            "MEASURED (5 seeds, paired;\n"
            "gap = coalition score: Shapley − sparse):\n"
            "   $\\alpha=0$, proxy, synergy 0.3: +0.0376 ± 0.0103\n"
            "      (score 4.5x the sparse one)\n"
            "   $\\alpha=0$, rollout credit: +0.0128 ± 0.0026\n"
            "   $\\alpha \\geq 0.3$, scale tier: −0.0003 … −0.0035 (DEAD ZONE)",
            fc=C_ANNOT, fs=10)

tradeoff = box(ax, 9.5, 0.3, 4.2, 3.0,
               "TRADE-OFF (measured):\n"
               "$\\alpha=0$ → win rate ~0.29\n"
               "(random play: 0.25)\n"
               "$\\alpha \\geq 0.1$ → win rate ~0.52",
               fc=C_EXPLOIT, fs=10)

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "mappo_blend.png"))
