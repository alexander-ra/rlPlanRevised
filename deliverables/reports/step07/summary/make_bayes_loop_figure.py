"""Section 2 figure: the opponent-modeling belief-update loop.

prior -> (x likelihood of observed action) -> posterior -> best response -> act,
with the observed outcome feeding the next iteration. Output: bayes_loop.png next
to this file. Run from repo root with the project .venv active.
"""
from _diagram_utils import new_fig, box, arrow, note, save, rc, lc, tc, bc, cc
from _diagram_utils import C_SAFE, C_MODEL, C_NET, C_EXPLOIT, C_ANNOT

fig, ax = new_fig(w=14, h=6.2, xlim=(0, 14), ylim=(0, 6.2), shrink=1.7)

prior = box(ax, 0.4, 3.6, 2.7, 1.2, "Prior belief\nover strategy", fc=C_SAFE, fs=9.5)
like = box(ax, 4.0, 3.6, 3.0, 1.2, "Likelihood of\nobserved action", fc=C_NET, fs=9.5)
post = box(ax, 7.9, 3.6, 2.7, 1.2, "Posterior belief", fc=C_MODEL, fs=9.5, fontweight="bold")
br = box(ax, 11.0, 3.6, 2.6, 1.2, "Best response", fc=C_EXPLOIT, fs=9.5)

act = box(ax, 11.0, 1.0, 2.6, 1.1, "Act in the hand", fc=C_ANNOT, fs=9.0)
obs = box(ax, 4.0, 1.0, 3.0, 1.1, "Observe opponent\naction (or showdown)", fc=C_ANNOT, fs=8.6)

arrow(ax, rc(prior), lc(like))
arrow(ax, rc(like), lc(post))
arrow(ax, rc(post), lc(br))
arrow(ax, bc(br), tc(act))
arrow(ax, lc(act), rc(obs))
arrow(ax, tc(obs), bc(like))

note(ax, 5.5, 5.15, "posterior  \u221d  prior  \u00d7  P(action | strategy)", fs=9.0,
     color="#2c3e50", style="italic")
note(ax, 9.25, 2.9, "respond to the\nposterior mean", fs=7.4)
note(ax, 7.0, 0.35, "each hand sharpens the belief; showdowns reveal the hidden card",
     fs=7.6)

save(fig, "deliverables/reports/step07/summary/bayes_loop.png")
