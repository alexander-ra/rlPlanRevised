"""Section 2 figure: the opponent-modeling belief-update loop.

prior -> (x likelihood of observed action) -> posterior -> best response -> act,
with the observed outcome feeding the next iteration. Output: bayes_loop.png next
to this file. Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, rc, lc, tc, bc, cc
from _diagram_utils import C_SAFE, C_MODEL, C_NET, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=6.6, xlim=(0, 14), ylim=(0, 6.6), shrink=1.7)

# boxes sized for the longer Bulgarian labels at fs 10 (prints at ~8.5 pt)
prior = box(ax, 0.2, 3.7, 3.0, 1.4, "Prior belief\nover strategy", fc=C_SAFE, fs=10)
like = box(ax, 3.8, 3.7, 3.4, 1.4, "Likelihood of\nobserved action", fc=C_NET, fs=10)
post = box(ax, 7.8, 3.7, 2.8, 1.4, "Posterior belief", fc=C_MODEL, fs=10, fontweight="bold")
br = box(ax, 11.2, 3.7, 2.6, 1.4, "Best response", fc=C_EXPLOIT, fs=10)

act = box(ax, 11.2, 1.0, 2.6, 1.3, "Act in the hand", fc=C_ANNOT, fs=10)
obs = box(ax, 3.4, 1.0, 4.2, 1.3, "Observe opponent\naction (or showdown)", fc=C_ANNOT, fs=10)

arrow(ax, rc(prior), lc(like))
arrow(ax, rc(like), lc(post))
arrow(ax, rc(post), lc(br))
arrow(ax, bc(br), tc(act))
arrow(ax, lc(act), rc(obs))
arrow(ax, tc(obs), bc(like))

note(ax, 5.5, 5.55, "posterior  ∝  prior  ×  P(action | strategy)", fs=10,
     color="#2c3e50", style="italic")
note(ax, 9.2, 3.05, "respond to the\nposterior mean", fs=10)
note(ax, 7.0, 0.4, "each hand sharpens the belief; showdowns reveal the hidden card",
     fs=10)

save(fig, "deliverables/reports/step07/summary/bayes_loop.png")
