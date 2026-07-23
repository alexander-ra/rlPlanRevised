"""
psro.py -- Policy-Space Response Oracles: population + meta-Nash + best-response oracle.

WHAT THIS IS
------------
The raw step's thesis-critical 🔴 build (L353, L395-424, L481-485): PSRO (Lanctot et al. 2017),
the double-oracle loop lifted to policies and the bridge from game theory (Steps 2-8) to MARL.

    repeat:
      1. build the meta-game payoff matrix U between the two policy populations,
      2. solve its meta-Nash (meta_nash.solve_meta_nash -- LP for zero-sum),
      3. train a best RESPONSE (the oracle) to the opponent's meta-Nash MIXTURE,
      4. add each new best response to its population.

THREE DRIVERS
-------------
- `PSRO` (this class): EXTENSIVE-FORM games via Step 07 (Kuhn, Leduc). The oracle is Step 07's
  EXACT best response; the crucial subtlety is that the opponent's meta-Nash mixture over
  BEHAVIORAL policies is realization-equivalent (Kuhn's theorem, perfect recall) to a SINGLE
  behavioral policy -- `mixture_behavioral_policy` -- so the exact BR engine applies directly.
  This is the path validated against the raw step's targets (Kuhn exploitability -> ~0; Leduc
  < 0.5 within 20 iters, L454-455).
- `psro_matrix` : matrix games (population = pure actions); meta-Nash + pure best response.
- `psro_goofspiel` : native Goofspiel via its exact best-response-to-a-mixture recursion.

The default oracle is EXACT (double oracle -> converges to a Nash of the game). An optional
`oracle="noisy"` mixes the exact BR with uniform noise to STUDY the approximate-oracle
question (raw step OPEN, L487-489); a full PPO-over-EFG oracle is a heavier extension noted in
the README.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (puts step07/implementation on sys.path)
from best_response import best_response_policy, best_response_value, exact_value, nash_gap
from policies import uniform_policy, tabular_policy, blend_policies

from meta_nash import solve_meta_nash


# --- realization-weighted behavioral mixture over an EFG population ------------------
def mixture_behavioral_policy(game, opp_player: int, policies, weights):
    """Collapse a meta-Nash MIXTURE over the opponent's behavioral policies into ONE
    behavioral policy that is realization-equivalent to it (perfect recall / Kuhn's theorem).

    At each opponent info set I:  beta(a|I) = sum_j w_j r_j(I) pi_j(a|I) / sum_j w_j r_j(I),
    where r_j(I) is policy j's OWN reach probability to I (product of its action probs on the
    path; chance and hero excluded, exactly as CFR accumulates an average strategy).
    """
    num: dict = {}   # iset -> {action: weight}
    den: dict = {}   # iset -> weight

    def traverse(state, pol, w, reach):
        if game.is_terminal(state):
            return
        player = game.current_player(state)
        legal = game.legal_actions(state)
        if player == opp_player:
            iset = game.info_set(state, opp_player)
            dist = pol(game, state)
            slot = num.setdefault(iset, {})
            den[iset] = den.get(iset, 0.0) + w * reach
            for a in legal:
                pa = dist.get(a, 0.0)
                slot[a] = slot.get(a, 0.0) + w * reach * pa
                if pa > 0.0:
                    traverse(game.apply(state, a), pol, w, reach * pa)
        else:
            # hero / chance: opponent reach unchanged; enumerate all branches (sum over histories)
            for a in legal:
                traverse(game.apply(state, a), pol, w, reach)

    total_w = sum(weights)
    for pol, w in zip(policies, weights):
        if w <= 0.0:
            continue
        for deal in game.deals():
            traverse(game.root(deal), pol, w, 1.0)  # exclude chance from reach (uniform, cancels)

    table = {}
    for iset, slot in num.items():
        d = den.get(iset, 0.0)
        if d > 0.0:
            table[iset] = {a: v / d for a, v in slot.items()}
    return tabular_policy(table)


class PSRO:
    """PSRO on a Step 07 extensive-form game (Kuhn / Leduc)."""

    def __init__(self, game, oracle: str = "exact", noise: float = 0.1, seed: int = 0):
        self.game = game
        self.oracle = oracle
        self.noise = noise
        self.rng = np.random.default_rng(seed)
        # each population starts with a single uniform-random policy
        self.pop = {0: [uniform_policy()], 1: [uniform_policy()]}
        self.U = None  # meta payoff matrix (player 0's EV), shape (|pop0|, |pop1|)
        self._build_meta_from_scratch()

    # ---- meta-game bookkeeping ----
    def _build_meta_from_scratch(self):
        n0, n1 = len(self.pop[0]), len(self.pop[1])
        self.U = np.zeros((n0, n1))
        for i in range(n0):
            for j in range(n1):
                self.U[i, j] = exact_value(self.game, 0, self.pop[0][i], self.pop[1][j])

    def _extend_meta(self, added0: bool, added1: bool):
        """Recompute only the new row/column after adding best responses."""
        n0, n1 = len(self.pop[0]), len(self.pop[1])
        U = np.zeros((n0, n1))
        U[:self.U.shape[0], :self.U.shape[1]] = self.U
        if added0:
            i = n0 - 1
            for j in range(n1):
                U[i, j] = exact_value(self.game, 0, self.pop[0][i], self.pop[1][j])
        if added1:
            j = n1 - 1
            for i in range(n0):
                U[i, j] = exact_value(self.game, 0, self.pop[0][i], self.pop[1][j])
        self.U = U

    # ---- oracle ----
    def _best_response(self, hero: int, opp_mixture):
        br = best_response_policy(self.game, hero, opp_mixture)
        if self.oracle == "exact":
            return br
        # "noisy": blend the exact BR with uniform to emulate an approximate oracle
        return blend_policies([br, uniform_policy()], [1.0 - self.noise, self.noise])

    # ---- the loop ----
    def iterate(self, rounds: int = 20):
        history = {"round": [], "exploitability": [], "pop_sizes": []}
        for r in range(rounds):
            row_mix, col_mix = solve_meta_nash(self.U)  # zero-sum LP
            # meta-mixture exploitability in the FULL game
            beta0 = mixture_behavioral_policy(self.game, 0, self.pop[0], row_mix)
            beta1 = mixture_behavioral_policy(self.game, 1, self.pop[1], col_mix)
            expl = nash_gap(self.game, beta0, beta1)["nash_conv"]
            history["round"].append(r)
            history["exploitability"].append(expl)
            history["pop_sizes"].append((len(self.pop[0]), len(self.pop[1])))

            # train a best response for each player to the opponent's meta-mixture
            br0 = self._best_response(0, beta1)
            br1 = self._best_response(1, beta0)
            self.pop[0].append(br0)
            self.pop[1].append(br1)
            self._extend_meta(added0=True, added1=True)
        return history

    def meta_nash_policies(self):
        """Return the current meta-Nash behavioral policies (both seats)."""
        row_mix, col_mix = solve_meta_nash(self.U)
        return (mixture_behavioral_policy(self.game, 0, self.pop[0], row_mix),
                mixture_behavioral_policy(self.game, 1, self.pop[1], col_mix))


# --- PSRO on a matrix game (population = pure actions) -------------------------------
def psro_matrix(game, rounds: int = 8, seed: int = 0):
    """PSRO on a `matrix_games.MatrixGame`. Population members are pure actions; the meta-game
    is a submatrix of the full game. Returns a history of meta-mixture exploitability."""
    rng = np.random.default_rng(seed)
    n0, n1 = game.n_actions
    pop0 = [int(rng.integers(n0))]
    pop1 = [int(rng.integers(n1))]
    A_full = game.A
    B_full = None if game.zero_sum else game.B
    history = {"round": [], "exploitability": []}
    for r in range(rounds):
        subA = A_full[np.ix_(pop0, pop1)]
        subB = None if game.zero_sum else B_full[np.ix_(pop0, pop1)]
        row_mix, col_mix = solve_meta_nash(subA, subB)
        # lift to full-action mixtures
        x = np.zeros(n0)
        y = np.zeros(n1)
        for a, w in zip(pop0, row_mix):
            x[a] += w
        for a, w in zip(pop1, col_mix):
            y[a] += w
        expl = game.nashconv(x, y)
        history["round"].append(r)
        history["exploitability"].append(float(expl))
        # best responses to the opponent's meta-mixture (over full action set)
        _, br0 = game.best_response_value(0, y)
        _, br1 = game.best_response_value(1, x)
        if br0 not in pop0:
            pop0.append(br0)
        if br1 not in pop1:
            pop1.append(br1)
    return history


# --- PSRO on native Goofspiel -------------------------------------------------------
def psro_goofspiel(goof, rounds: int = 8, seed: int = 0):
    """PSRO on a `goofspiel.Goofspiel`. Population members are deterministic BR tables; the
    oracle is Goofspiel's exact best-response-to-a-mixture recursion. Returns exploitability
    history of the meta-mixture."""
    from goofspiel import uniform_policy as gs_uniform, table_policy

    pop0 = [gs_uniform()]
    pop1 = [gs_uniform()]

    def meta_matrix():
        U = np.zeros((len(pop0), len(pop1)))
        for i, p0 in enumerate(pop0):
            for j, p1 in enumerate(pop1):
                U[i, j] = goof.exact_value(p0, p1)
        return U

    history = {"round": [], "exploitability": []}
    for r in range(rounds):
        U = meta_matrix()
        row_mix, col_mix = solve_meta_nash(U)
        # meta-mixture exploitability: BR to each side's mixture minus the mixture value
        v0 = goof.best_response_value_vs_mixture(0, pop1, col_mix.tolist())  # best P0 can get
        v1 = goof.best_response_value_vs_mixture(1, pop0, row_mix.tolist())  # best P1 can get
        # game value of the meta-mixture profile for P0:
        mix_val = float(row_mix @ U @ col_mix)
        expl = (v0 - mix_val) + (v1 - (-mix_val))   # zero-sum: P1 mixture value = -mix_val
        history["round"].append(r)
        history["exploitability"].append(float(expl))
        # add exact BRs (as deterministic tables) to the opponent's mixtures
        _, tab0 = goof.best_response_value_vs_mixture(0, pop1, col_mix.tolist(), return_table=True)
        _, tab1 = goof.best_response_value_vs_mixture(1, pop0, row_mix.tolist(), return_table=True)
        pop0.append(table_policy(tab0))
        pop1.append(table_policy(tab1))
    return history


def _selftest():
    from engines import make_game
    print("psro self-test")
    print("-" * 60)
    game = make_game("kuhn")
    psro = PSRO(game, seed=0)
    hist = psro.iterate(rounds=6)
    for r, e, ps in zip(hist["round"], hist["exploitability"], hist["pop_sizes"]):
        print(f"  round {r}: pop={ps} meta-Nash exploitability={e:.4f}")
    print("  PREDICT: exploitability decreases toward ~0 as the population grows.")


if __name__ == "__main__":
    _selftest()
