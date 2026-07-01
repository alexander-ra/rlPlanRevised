"""
Consistent (sequence-form) opponent model -- after Ganzfried (2025), "Bayesian Opponent
Modeling in Imperfect-Information Games".

WHY THIS EXISTS
---------------
The continuous model estimates each info set independently. Under partial observability
that is statistically awkward: a fold tells you the opponent did *something* with *some*
card, but per-info-set counting cannot use that evidence cleanly. The fix is to estimate a
single, globally consistent strategy in SEQUENCE FORM, where the marginalized likelihood
becomes concave and the whole MAP problem is a tractable convex program.

THE IDEA IN ONE PARAGRAPH
-------------------------
A player's sequence-form / realization plan assigns a weight y_sigma to each "sequence"
sigma (a root-to-here chain of that player's own (info_set, action) choices), with
y_empty = 1 and, at every info set I, the children summing to the parent: sum_a y_{Ia} =
y_{sigma_I}, y >= 0. The realization weight of the opponent's full action path equals the
PRODUCT of their behavioral probabilities along it -- i.e. exactly the likelihood of those
actions. So for one hand the (card-)marginalized likelihood is

    P(hand) = sum over consistent cards c of  pi(c) * y_{sigma(c)}

which is *linear* in y. The log of a sum of linear terms is concave, so

    maximize   sum over hands log( sum_c pi(c) y_{sigma(c)} )  +  prior(y)
    subject to the sequence-form (treeplex) constraints

is a convex program with a unique-up-to-degeneracy solution -- the maximum-a-posteriori
*consistent* opponent strategy. We solve it with SciPy and read the behavioral strategy
back out as beta(I,a) = y_{Ia} / y_{sigma_I}.

DEPENDENCY / SCOPE NOTE
-----------------------
This module needs numpy + scipy (only here). It is validated by the source paper on Kuhn,
which is the default; Leduc works too but the program is larger and slower (see README's
"likely to break" list -- this is the module most likely to need a debugging pass).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import math

from bayesian_model import OpponentModel
from observation_buffer import candidate_deals
from policies import replay, tabular_policy


# --- sequence form of one player, built from the game tree ---------------------------
class SequenceForm:
    """Enumerates player `opp`'s sequences, info sets, and the parent/child links that
    define the treeplex constraints. Perfect recall is assumed (true for Kuhn & Leduc)."""

    def __init__(self, game, opp: int):
        self.game = game
        self.opp = opp
        self.seq_index = {(): 0}        # sequence tuple -> id; empty sequence is id 0
        self.parent_seq = {}            # info_set -> parent sequence id
        self.actions = {}               # info_set -> ordered list of legal actions
        self.child_seq = {}             # (info_set, action) -> sequence id
        for deal in game.deals():
            self._walk(game.root(deal), ())
        self.num_seq = len(self.seq_index)

    def _walk(self, state, opp_seq):
        if self.game.is_terminal(state):
            return
        player = self.game.current_player(state)
        legal = self.game.legal_actions(state)
        if player == self.opp:
            iset = self.game.info_set(state, self.opp)
            if iset not in self.parent_seq:
                self.parent_seq[iset] = self.seq_index[opp_seq]
                self.actions[iset] = list(legal)
                for a in legal:
                    key = opp_seq + ((iset, a),)
                    if key not in self.seq_index:
                        self.seq_index[key] = len(self.seq_index)
                    self.child_seq[(iset, a)] = self.seq_index[key]
            for a in legal:
                self._walk(self.game.apply(state, a), opp_seq + ((iset, a),))
        else:
            for a in legal:
                self._walk(self.game.apply(state, a), opp_seq)

    def terminal_seq_for(self, deal, actions):
        """The opponent's terminal sequence id when `actions` is replayed under `deal`,
        or None if the opponent never acted this hand."""
        decisions = [(d.info_set, d.action)
                     for d in replay(self.game, deal, actions) if d.player == self.opp]
        if not decisions:
            return None
        return self.child_seq[decisions[-1]]  # the last child seq encodes the whole chain

    def uniform_realization(self):
        """A valid interior starting point: realization weights of the uniform strategy."""
        y = [0.0] * self.num_seq
        y[0] = 1.0
        known = {0}
        # Forward fixpoint: fill children once their parent sequence is known.
        progress = True
        while progress:
            progress = False
            for iset, parent in self.parent_seq.items():
                if parent in known:
                    n = len(self.actions[iset])
                    for a in self.actions[iset]:
                        cid = self.child_seq[(iset, a)]
                        if cid not in known:
                            y[cid] = y[parent] / n
                            known.add(cid)
                            progress = True
        return y


# --- the model -----------------------------------------------------------------------
class ConsistentModel(OpponentModel):
    name = "consistent"

    def __init__(self, game, hero: int, prior_pseudocount: float = 0.5):
        super().__init__(game, hero)
        self.sf = SequenceForm(game, self.opp)
        self.prior_pseudocount = float(prior_pseudocount)
        self.observations: list = []
        self._dirty = True
        self._table: dict = {}          # info_set -> {action: prob}
        self._y = None                  # last solved realization plan

    def update(self, obs):
        self.observations.append(obs)
        self._dirty = True

    # ---- the convex program ----
    def _hand_terms(self):
        """For each usable hand, the (sequence ids, weights) of the marginalized
        likelihood term log( sum_i w_i y_{seq_i} )."""
        terms = []
        for obs in self.observations:
            cds = candidate_deals(self.game, obs)
            seqs = []
            for d in cds:
                sid = self.sf.terminal_seq_for(d, obs.actions)
                if sid is not None:
                    seqs.append(sid)
            if not seqs:
                continue
            w = 1.0 / len(seqs)
            terms.append((seqs, w))
        return terms

    def _prior_coeffs(self):
        """Linear coefficients c0[sigma] for the regularizer term sum_sigma c0 * log y.

        We add a pseudo-count kappa to each *child* sequence and nothing to parents. Two
        reasons:
          - CONCAVITY. A faithful behavioral Dirichlet would also subtract kappa*|A(I)| at
            each parent; those -log(y_parent) terms make the sequence-form objective
            non-concave and invite local optima. Children-only keeps c0 >= 0, so
            sum c0*log y is concave and the whole program is convex -> a clean global solve.
          - IT IS STILL SMOOTHING. On the treeplex constraint surface, maximizing
            sum_a log y_{Ia} subject to sum_a y_{Ia} = y_{sigma_I} is maximized by an equal
            split (AM-GM) -- i.e. it pulls the behavioral strategy toward uniform, exactly
            like a symmetric Dirichlet. kappa>0 also keeps the optimum off the y=0 boundary.
        (Documented as a deliberate, mild approximation; see README "likely to break".)"""
        kappa = self.prior_pseudocount
        c0 = [0.0] * self.sf.num_seq
        if kappa <= 0.0:
            return c0
        for iset in self.sf.parent_seq:
            for a in self.sf.actions[iset]:
                c0[self.sf.child_seq[(iset, a)]] += kappa
        return c0

    def fit(self):
        try:
            import numpy as np
            from scipy.optimize import minimize, LinearConstraint, Bounds
        except ImportError as exc:  # pragma: no cover - dependency guard
            raise ImportError(
                "ConsistentModel.fit() needs numpy + scipy. Install with "
                "`pip install numpy scipy`."
            ) from exc

        n = self.sf.num_seq
        terms = self._hand_terms()
        c0 = np.asarray(self._prior_coeffs(), dtype=float)

        # Pre-pack each hand term as an index list for fast objective/gradient evaluation.
        packed = [(np.asarray(seqs, dtype=int), w) for seqs, w in terms]

        def neg_obj_and_grad(y):
            # Objective F(y) = sum_terms log(sum_i w*y[seq_i]) + sum_sigma c0[sigma] log y.
            # We minimize -F and supply -grad.
            ylog = np.log(np.clip(y, 1e-15, None))
            f = float(c0 @ ylog)
            grad = c0 / np.clip(y, 1e-15, None)
            for idx, w in packed:
                s = w * float(np.sum(y[idx]))
                if s <= 0.0:
                    s = 1e-15
                f += math.log(s)
                # d/dy[k] log(w*sum y[idx]) = w / s  for each k in idx
                np.add.at(grad, idx, w / s)
            return -f, -grad

        # Constraints: y_empty = 1 (bound), y >= eps, and sum_a y_{Ia} = y_{sigma_I}.
        lb = np.full(n, 1e-9)
        ub = np.full(n, 1.0)
        lb[0] = ub[0] = 1.0  # pin the empty sequence
        bounds = Bounds(lb, ub)

        rows = []
        for iset, parent in self.sf.parent_seq.items():
            row = np.zeros(n)
            for a in self.sf.actions[iset]:
                row[self.sf.child_seq[(iset, a)]] += 1.0
            row[parent] -= 1.0
            rows.append(row)
        constraints = []
        if rows:
            A = np.vstack(rows)
            constraints.append(LinearConstraint(A, 0.0, 0.0))

        y0 = np.asarray(self.sf.uniform_realization(), dtype=float)
        y0 = np.clip(y0, 1e-9, 1.0)

        res = minimize(neg_obj_and_grad, y0, jac=True, bounds=bounds,
                       constraints=constraints, method="trust-constr",
                       options={"maxiter": 500, "gtol": 1e-8, "xtol": 1e-10})
        y = np.clip(res.x, 1e-12, None)
        self._y = y
        self._table = self._behavioral_from_y(y)
        self._dirty = False
        return res

    def _behavioral_from_y(self, y) -> dict:
        table = {}
        for iset, parent in self.sf.parent_seq.items():
            acts = self.sf.actions[iset]
            denom = y[parent]
            if denom <= 0.0:
                p = 1.0 / len(acts)
                table[iset] = {a: p for a in acts}
                continue
            raw = {a: max(0.0, y[self.sf.child_seq[(iset, a)]] / denom) for a in acts}
            total = sum(raw.values())
            if total <= 0.0:
                p = 1.0 / len(acts)
                table[iset] = {a: p for a in acts}
            else:
                table[iset] = {a: v / total for a, v in raw.items()}
        return table

    # ---- readout ----
    def predicted_policy(self):
        if self._dirty:
            self.fit()
        return tabular_policy(self._table)

    def reset(self):
        self.observations = []
        self._dirty = True
        self._table = {}
        self._y = None


def _selftest():
    import random
    from engines import make_game
    from policies import play_hand, uniform_policy
    from observation_buffer import Observation
    from opponent_types import make_type_zoo

    print("consistent_model self-test")
    print("-" * 50)
    game = make_game("kuhn")
    sf = SequenceForm(game, opp=0)
    print(f"[kuhn] opponent sequences = {sf.num_seq} (expect 13: 1 + 6 info sets x 2)")
    print(f"[kuhn] opponent info sets = {len(sf.parent_seq)} (expect 6)")

    hero, opp = 1, 0
    truth = make_type_zoo(game, include_nash=False)["TightPassive"]
    model = ConsistentModel(game, hero)
    rng = random.Random(5)
    pols = [None, None]
    pols[opp] = truth
    pols[hero] = uniform_policy()
    for _ in range(1500):
        hand = play_hand(game, pols, rng.choice(game.deals()), rng)
        opp_priv = hand.deal[opp] if opp in hand.revealed else None
        model.update(Observation(hero, opp, hand.deal[hero], None, hand.actions,
                                 opp_priv, hand.utilities[hero]))
    res = model.fit()
    print(f"[kuhn] solver success={getattr(res, 'success', '?')} "
          f"final -logpost={getattr(res, 'fun', float('nan')):.3f}")
    est = model.predicted_policy()
    s = game.root((3, 1))  # opponent (player 0) holds the King at the open node
    dist = est(game, s)
    print(f"[kuhn] estimated P(BET | King, open) = {dist.get(1, 0.0):.3f} "
          f"(TightPassive bets the King ~ 1 - eps)")


if __name__ == "__main__":
    _selftest()
