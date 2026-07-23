"""
seq_form.py -- the sequence-form LP engine. THE one new primitive Step 08 adds.

WHY THIS IS THE HEART OF THE STEP
---------------------------------
Every safe-exploitation method in this step is the SAME optimization:

    maximize   EV(hero vs opponent model)          # linear in the hero's realization plan x
    subject to a SAFETY CONSTRAINT                  # a set of linear "cuts" c_j . x >= floor_j
    and        x is a valid strategy                # treeplex (sequence-form) flow constraints

The methods (RNR, Ganzfried, prime-safe, SES gadget, adaptation) differ ONLY in which safety
cuts they add and what the floor is. So we build the LP machinery once, here, and the solvers
are thin wrappers.

THE REALIZATION PLAN x
----------------------
For a perfect-recall player, a strategy is a "realization plan" x that assigns a weight to
each of that player's SEQUENCES (root-to-here chains of their own (info_set, action) choices),
with x_empty = 1, x >= 0, and at every info set the children summing to the parent
(sum_a x_{Ia} = x_{seq(I)}). We REUSE Step 07's `SequenceForm` (from consistent_model.py) to
enumerate those sequences and the parent/child links -- it was written for an arbitrary
player, exactly what we need for the hero here.

EV IS LINEAR IN x
-----------------
Against a FIXED opponent policy, the hero's expected value is
    EV = sum over terminals of  [chance_prob * opp_reach * hero_utility] * x_{hero terminal seq}
because the hero's own action-probability product along a path IS x at that path's sequence.
So EV = c . x with c the "payoff vector" built by one tree traversal (`payoff_vector`). Full
best response is then just max_x c . x over the treeplex -- which cross-checks Step 07's exact
`best_response_value` (see `_selftest`).

DEPENDENCY: needs numpy + scipy (guarded). SciPy's HiGHS LP solver does the work.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import deps  # noqa: F401  (puts Step 07 modules on sys.path)
from consistent_model import SequenceForm
from policies import tabular_policy


class HeroTreeplex:
    """Sequence-form model of ONE player (the hero), plus the LP machinery to optimize a
    linear objective over that player's realization plans subject to safety cuts.

    Built once per (game, hero); reused across many solves (RNR sweep, Ganzfried iterations)."""

    def __init__(self, game, hero: int):
        self.game = game
        self.hero = hero
        # SequenceForm enumerates the sequences/info sets/links of its `opp` argument; here
        # we want the HERO's own sequences, so pass opp=hero.
        self.sf = SequenceForm(game, opp=hero)
        self.num_seq = self.sf.num_seq
        self._A_eq = None  # cached flow-constraint matrix (numpy)

    # ---- payoff vector: EV(hero vs opp_policy) = c . x -----------------------------
    def payoff_vector(self, opp_policy) -> list:
        """Linear coefficients c such that hero EV vs `opp_policy` equals c . x.

        c[k] accumulates, over every terminal whose hero-sequence id is k,
        chance_prob * (opponent reach) * hero_utility.  Hero action probabilities are NOT
        folded in -- they live in x."""
        c = [0.0] * self.num_seq
        for deal in self.game.deals():
            self._accumulate(self.game.root(deal), self.game.deal_prob(deal), 0, opp_policy, c)
        return c

    def _accumulate(self, state, weight, hero_seq_id, opp_policy, c):
        if self.game.is_terminal(state):
            c[hero_seq_id] += weight * self.game.utility(state, self.hero)
            return
        player = self.game.current_player(state)
        legal = self.game.legal_actions(state)
        if player == self.hero:
            iset = self.game.info_set(state, self.hero)
            for a in legal:
                child_id = self.sf.child_seq[(iset, a)]
                self._accumulate(self.game.apply(state, a), weight, child_id, opp_policy, c)
        else:
            dist = opp_policy(self.game, state)
            for a in legal:
                pa = dist.get(a, 0.0)
                if pa > 0.0:
                    self._accumulate(self.game.apply(state, a), weight * pa,
                                     hero_seq_id, opp_policy, c)

    # ---- treeplex flow constraints (cached) ----------------------------------------
    def flow_matrix(self):
        """A_eq (numpy) for the equality constraints A_eq x = 0: one row per info set,
        sum_a x_{Ia} - x_{seq(I)} = 0. (x_empty = 1 is pinned via variable bounds, not here.)"""
        import numpy as np
        if self._A_eq is not None:
            return self._A_eq
        rows = []
        for iset, parent in self.sf.parent_seq.items():
            row = np.zeros(self.num_seq)
            for a in self.sf.actions[iset]:
                row[self.sf.child_seq[(iset, a)]] += 1.0
            row[parent] -= 1.0
            rows.append(row)
        self._A_eq = np.vstack(rows) if rows else np.zeros((0, self.num_seq))
        return self._A_eq

    # ---- the LP ---------------------------------------------------------------------
    def solve(self, objective_c, cuts=None, sense: str = "max", fixed=None):
        """Optimize `objective_c . x` over valid realization plans, subject to safety `cuts`.

        cuts: list of (coeff_vector, floor) meaning coeff . x >= floor. (Used to encode
              worst-case-value >= safety floor via a best-response payoff vector -- see the
              constraint-generation solvers.)
        sense: "max" (default) or "min".
        fixed: optional {seq_id: value} to PIN certain sequence weights (via bounds). Used by
              the subgame solver to hold the hero's play OUTSIDE the subgame equal to the
              blueprint (only the subgame's sequences are then free to be re-optimized).

        Returns a SciPy OptimizeResult; `res.x` is the realization plan. Raises on failure so
        callers surface bugs loudly (per workflow: fail as a clear error, don't fake a result).
        """
        try:
            import numpy as np
            from scipy.optimize import linprog
        except ImportError as exc:  # pragma: no cover - dependency guard
            raise ImportError("seq_form.solve needs numpy + scipy (`pip install numpy scipy`).") \
                from exc

        c = np.asarray(objective_c, dtype=float)
        obj = c if sense == "min" else -c  # linprog minimizes

        A_eq = self.flow_matrix()
        b_eq = np.zeros(A_eq.shape[0])

        A_ub = b_ub = None
        if cuts:
            ub_rows, ub_vals = [], []
            for coeff, floor in cuts:
                # coeff . x >= floor   <=>   -coeff . x <= -floor
                ub_rows.append(-np.asarray(coeff, dtype=float))
                ub_vals.append(-float(floor))
            A_ub = np.vstack(ub_rows)
            b_ub = np.asarray(ub_vals, dtype=float)

        # x >= 0 everywhere; the empty sequence is pinned to 1; `fixed` pins subgame boundary.
        lb = [0.0] * self.num_seq
        ub = [None] * self.num_seq
        lb[0] = ub[0] = 1.0
        if fixed:
            for k, v in fixed.items():
                lb[k] = ub[k] = float(v)
        bounds = list(zip(lb, ub))

        res = linprog(obj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds,
                      method="highs")
        if not res.success:
            raise RuntimeError(f"seq_form LP failed: {res.message} (status {res.status})")
        return res

    # ---- realization plan of a given behavioral policy ------------------------------
    def realization_plan(self, policy) -> list:
        """Compute the hero's realization weights x for a behavioral `policy` (forward pass:
        x_empty = 1, x_{Ia} = x_{seq(I)} * beta_policy(I, a)). Used to pin the blueprint's
        play outside a subgame."""
        from policies import materialize
        table = materialize(self.game, policy, self.hero)
        x = [0.0] * self.num_seq
        x[0] = 1.0
        known = {0}
        progress = True
        while progress:
            progress = False
            for iset, parent in self.sf.parent_seq.items():
                if parent in known:
                    acts = self.sf.actions[iset]
                    dist = table.get(iset, {a: 1.0 / len(acts) for a in acts})
                    total = sum(max(0.0, dist.get(a, 0.0)) for a in acts) or 1.0
                    for a in acts:
                        cid = self.sf.child_seq[(iset, a)]
                        if cid not in known:
                            beta = max(0.0, dist.get(a, 0.0)) / total
                            x[cid] = x[parent] * beta
                            known.add(cid)
                            progress = True
        return x

    def subgame_info_sets(self, predicate) -> set:
        """Hero info sets where `predicate(state)` holds at a hero decision node -- the info
        sets that a subgame solve is allowed to change (everything else stays blueprint)."""
        found = set()
        for deal in self.game.deals():
            self._collect_subgame(self.game.root(deal), predicate, found)
        return found

    def _collect_subgame(self, state, predicate, found):
        if self.game.is_terminal(state):
            return
        player = self.game.current_player(state)
        if player == self.hero and predicate(state):
            found.add(self.game.info_set(state, self.hero))
        for a in self.game.legal_actions(state):
            self._collect_subgame(self.game.apply(state, a), predicate, found)

    # ---- read a behavioral policy back out of a realization plan --------------------
    def behavioral_table(self, x) -> dict:
        """info_set -> {action: prob} from a realization plan x (beta(I,a) = x_{Ia}/x_{seq(I)}).
        Unreached info sets (parent weight ~0) fall back to uniform."""
        table = {}
        for iset, parent in self.sf.parent_seq.items():
            acts = self.sf.actions[iset]
            denom = x[parent]
            if denom <= 1e-12:
                table[iset] = {a: 1.0 / len(acts) for a in acts}
                continue
            raw = {a: max(0.0, x[self.sf.child_seq[(iset, a)]] / denom) for a in acts}
            total = sum(raw.values())
            if total <= 0.0:
                table[iset] = {a: 1.0 / len(acts) for a in acts}
            else:
                table[iset] = {a: v / total for a, v in raw.items()}
        return table

    def policy(self, x):
        """The realization plan x as a callable policy(game, state) -> {action: prob}."""
        return tabular_policy(self.behavioral_table(x))

    # ---- convenience ----------------------------------------------------------------
    def full_best_response(self, opp_policy):
        """max_x c(opp) . x -- the unconstrained exploit. Returns (value, policy). This must
        agree with Step 07's exact best_response_value (see _selftest)."""
        c = self.payoff_vector(opp_policy)
        res = self.solve(c, sense="max")
        value = float(sum(ci * xi for ci, xi in zip(c, res.x)))
        return value, self.policy(res.x)


def expected_value(c, x) -> float:
    """EV = c . x for a payoff vector c and realization plan x."""
    return float(sum(ci * xi for ci, xi in zip(c, x)))


def _selftest():
    from engines import make_game
    from opponent_types import make_type_zoo
    from best_response import best_response_value

    print("seq_form self-test")
    print("-" * 60)
    for name in ("kuhn", "leduc"):
        game = make_game(name)
        zoo = make_type_zoo(game, include_nash=False)
        opp_name = "TightPassive" if name == "kuhn" else "Rock"
        opp = zoo[opp_name]
        for hero in (0, 1):
            tp = HeroTreeplex(game, hero)
            try:
                lp_val, _ = tp.full_best_response(opp)
            except ImportError as exc:
                print(f"[{name}] hero{hero}: SKIP ({exc})")
                break
            exact = best_response_value(game, hero, opp)
            ok = abs(lp_val - exact) < 1e-6
            print(f"[{name}] hero{hero} vs {opp_name}: LP BR={lp_val:+.6f} "
                  f"exact BR={exact:+.6f} match={ok} (#seq={tp.num_seq})")


if __name__ == "__main__":
    _selftest()
