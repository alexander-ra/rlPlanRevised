"""summary figure: the coalition-aware MAPPO reward blend and the alpha knob.

Each SLS seat is a masked episodic PPO agent trained by self-play with a BLENDED reward:
r = (1 - alpha) * sparse_winner_reward + alpha * Shapley_coalition_credit. The measured headline
(5-seed paired sweep) is that alpha is the dominant knob: coalitions emerge SIGNIFICANTLY only at low
alpha (heavy credit weight), and every alpha >= 0.3 suppresses the signal; the cheap critic-value
proxy beats the expensive counterfactual credit; and coalition behavior costs win-rate. Output:
mappo_blend.png. Run with the project .venv active; the PNG lands next to this file.
"""
import os

from _diagram_utils import new_fig, box, arrow, note, save
from _diagram_utils import C_MODEL, C_SAFE, C_EXPLOIT, C_NET, C_ANNOT, EC

fig, ax = new_fig(w=14, h=7.4, xlim=(0, 14), ylim=(0, 7.4), shrink=1.7)

sparse = box(ax, 0.4, 5.4, 3.4, 1.3, "Sparse reward\n$r_{\\text{sparse}}$ (winner takes all)", fc=C_SAFE, fs=8.4)
credit = box(ax, 0.4, 3.5, 3.4, 1.3, "Shapley coalition credit\n(proxy or counterfactual)", fc=C_MODEL, fs=8.2, fontweight="bold")
blend = box(ax, 4.6, 4.4, 4.2, 1.4,
            "BLEND\n$r = (1-\\alpha)\\,r_{\\text{sparse}} + \\alpha\\,\\text{credit}$", fc=C_NET, fs=8.6, fontweight="bold")
ppo = box(ax, 9.6, 4.4, 4.0, 1.4, "Masked episodic PPO\nself-play (4 seats)", fc=C_SAFE, fs=8.4, fontweight="bold")

arrow(ax, (sparse[0] + sparse[2], sparse[1] + sparse[3] / 2), (blend[0], blend[1] + blend[3] / 2 + 0.35), rad=-0.12)
arrow(ax, (credit[0] + credit[2], credit[1] + credit[3] / 2), (blend[0], blend[1] + blend[3] / 2 - 0.35), rad=0.12)
arrow(ax, (blend[0] + blend[2], blend[1] + blend[3] / 2), (ppo[0], ppo[1] + ppo[3] / 2))

note(ax, 7.0, 7.05,
     "alpha dials between 'just win' (alpha=0 -> pure coalition credit ... 1 -> pure sparse).",
     fs=8.4, color="#2c3e50", style="normal")

sweep = box(ax, 0.4, 0.9, 8.6, 2.9,
            "MEASURED (5-seed paired sweep; gap = coalition score shapley - sparse):\n"
            "  alpha = 0 (proxy, synergy 0.3):  +0.0376 +/- 0.0103   ** (~4.4x sparse)\n"
            "  alpha = 0 (counterfactual):      +0.0128 +/- 0.0026   **\n"
            "  alpha >= 0.3 (any cell):         -0.001 ... -0.004     (negative - the DEAD ZONE)\n"
            "Effect GROWS with game size; the cheap proxy beats the expensive counterfactual.",
            fc=C_ANNOT, fs=7.7)

tradeoff = box(ax, 9.4, 0.9, 4.2, 2.9,
               "TRADE-OFF (measured):\n"
               "alpha = 0    -> win-rate ~0.29\n"
               "               (near 0.25 floor)\n"
               "alpha >= 0.1 -> win-rate ~0.52\n\n"
               "Forming is primary,\n"
               "winning secondary.",
               fc=C_EXPLOIT, fs=7.8)

save(fig, os.path.join(os.path.dirname(os.path.abspath(__file__)), "mappo_blend.png"))
