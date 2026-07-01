"""
[P8] Bayesian Online Change-point Detection (Adams & MacKay, 2007).

A stationary opponent model quietly rots when the opponent changes style. BOCPD gives us a
running posterior over the "run length" r_t = how many hands since the last change. When the
opponent switches, recent hands stop fitting the accumulated statistics, the run-length
posterior collapses toward 0, and we can react (here: forget the stale observations and
re-learn).

We track a single binary signal per hand -- did the opponent take the *aggressive* action
at their first decision (BET in Kuhn, RAISE in Leduc)? -- with a conjugate Beta-Bernoulli
predictive. That is enough to notice a passive->aggressive (or vice versa) shift, which is
exactly the non-stationarity test in tournament.py.

The recursion is the standard one:
    P(r_t=0)      proportional to  sum_r P(r_{t-1}=r) * pred(x_t | r) * H
    P(r_t=r+1)    proportional to  P(r_{t-1}=r) * pred(x_t | r) * (1 - H)
with a constant hazard H = 1/expected_run_length and Beta sufficient statistics per run.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from observation_buffer import candidate_deals
from policies import replay

# Which action counts as "aggressive" per game (BET / RAISE).
_AGGRESSIVE = {"kuhn": {1}, "leduc": {2}}


def aggression_signal(game, obs):
    """1 if the opponent's first action this hand was aggressive, else 0, else None if the
    opponent never acted (the hand carries no signal)."""
    cds = candidate_deals(game, obs)
    if not cds:
        return None
    decisions = replay(game, cds[0], obs.actions)  # turn order is card-independent
    aggressive = _AGGRESSIVE.get(game.name, set())
    for d in decisions:
        if d.player == obs.opp:
            return 1 if d.action in aggressive else 0
    return None


class BernoulliBOCPD:
    """Beta-Bernoulli online change-point detector."""

    def __init__(self, hazard: float = 1.0 / 150.0, alpha0: float = 1.0, beta0: float = 1.0,
                 max_run: int = 400):
        self.hazard = hazard
        self.alpha0 = alpha0
        self.beta0 = beta0
        self.max_run = max_run
        self.alpha = [alpha0]      # Beta a-params, indexed by run length
        self.beta = [beta0]        # Beta b-params
        self.R = [1.0]             # run-length posterior P(r_t = r)
        self.t = 0
        self.changepoints = []     # hand indices where a change was flagged

    def update(self, x: int):
        """Fold in one binary observation; returns the new run-length posterior."""
        a = self.alpha
        b = self.beta
        # Predictive prob of x under each current run length (Beta mean).
        pred = [(ai / (ai + bi)) if x == 1 else (bi / (ai + bi)) for ai, bi in zip(a, b)]
        growth = [self.R[r] * pred[r] * (1.0 - self.hazard) for r in range(len(self.R))]
        cp_mass = sum(self.R[r] * pred[r] * self.hazard for r in range(len(self.R)))
        new_R = [cp_mass] + growth
        z = sum(new_R)
        if z <= 0.0:
            new_R = [1.0] + [0.0] * (len(new_R) - 1)
            z = 1.0
        new_R = [v / z for v in new_R]

        new_alpha = [self.alpha0] + [a[r] + (1 if x == 1 else 0) for r in range(len(a))]
        new_beta = [self.beta0] + [b[r] + (0 if x == 1 else 1) for r in range(len(b))]

        # Truncate to bound memory/compute (drop the longest, least-relevant runs).
        if len(new_R) > self.max_run:
            new_R = new_R[: self.max_run]
            new_alpha = new_alpha[: self.max_run]
            new_beta = new_beta[: self.max_run]
            s = sum(new_R)
            new_R = [v / s for v in new_R] if s > 0 else new_R

        self.R, self.alpha, self.beta = new_R, new_alpha, new_beta
        self.t += 1
        return new_R

    def map_run_length(self) -> int:
        return max(range(len(self.R)), key=lambda r: self.R[r])

    def changepoint_prob(self, window: int = 3) -> float:
        """Posterior mass on a very recent change (short run length)."""
        return sum(self.R[: window])

    def reset_runs(self):
        """Collapse back to 'a change just happened' (used after we act on a detection)."""
        self.alpha = [self.alpha0]
        self.beta = [self.beta0]
        self.R = [1.0]


def _selftest():
    print("changepoint self-test")
    print("-" * 50)
    import random
    rng = random.Random(0)
    det = BernoulliBOCPD(hazard=1.0 / 100.0)
    # 150 hands at p(agg)=0.1, then 150 at p(agg)=0.9. Expect a detection near hand ~150.
    flagged = None
    for i in range(300):
        p = 0.1 if i < 150 else 0.9
        x = 1 if rng.random() < p else 0
        det.update(x)
        if i > 5 and det.changepoint_prob(window=3) > 0.5 and (i >= 150):
            flagged = flagged or i
    print(f"first post-switch detection near hand {flagged} (switch was at 150)")
    print(f"final MAP run length = {det.map_run_length()}")


if __name__ == "__main__":
    _selftest()
