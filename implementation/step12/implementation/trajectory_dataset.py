"""
trajectory_dataset.py  [CORE / thesis-critical]  -- raw L236-293.

Turns poker self-play into Decision-Transformer training data: sequences of
`(return-to-go, state, action)` triples, one sub-sequence per player per hand.

TWO RECIPES (raw L261-262 vs L374-378)
--------------------------------------
  - "self_play_nash"  : hero AND opponent both play near-Nash CFR (Step 02 `KuhnTrainer`).
                        This is the clean testbed for DT return-conditioning + the Paster
                        luck-vs-skill check (raw Day 2).
  - "mixed_opponents" : opponents are 50% near-Nash + 50% EXPLOITABLE archetypes (Step 07
                        `make_type_zoo`); the hero plays a blend of Nash and the exact
                        BEST RESPONSE to that opponent (Step 07 `best_response_policy`). This
                        makes the return-to-go VARY with the opponent, which is exactly what
                        ARDT's minimax conditioning needs (raw Day 3).

WHY RETURN-TO-GO IS CONSTANT WITHIN A HAND
------------------------------------------
Poker pays out only at the showdown/fold, so the reward is a single terminal number. The
return-to-go at every decision in the hand therefore equals the hand's final payoff (raw
L284-289). We store it per step so the DT sees the standard `(R_hat_t, s_t, a_t)` layout.
WARNING (Paster et al., 2022): this final-payoff return conflates SKILL with the LUCK of the
card deal -- the central caveat of the whole step, and the reason ARDT exists.

Foundations are imported, never copied (see deps.py): Step 02 CFR + engine, Step 07 game
interface + policies + opponent zoo + best response.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import numpy as np

import deps  # noqa: F401  (bootstraps step02 + step07 onto sys.path)
from engines import make_game
from policies import sample_action, tabular_policy, blend_policies
from opponent_types import make_type_zoo
from best_response import best_response_policy

from state_encoding import PokerStateEncoder

_PASS, _BET = 0, 1
_NUM_ACTIONS = {"kuhn": 2, "leduc": 3}


# --- data containers -----------------------------------------------------------------
@dataclass
class Step:
    """One recorded decision (from the acting player's perspective)."""

    state_vec: np.ndarray
    action: int
    timestep: int
    card: int                 # acting player's private card (raw int; for luck-vs-skill)
    legal: tuple
    rtg: float = 0.0          # return-to-go, filled once the hand terminates


@dataclass
class Trajectory:
    steps: list = field(default_factory=list)
    hero: int = 0
    ret: float = 0.0          # hero's final utility (chips)
    opponent: str = "self"


# --- near-Nash policy from Step 02 CFR ----------------------------------------------
def make_cfr_policy(game, iters: int = 30000, seed: int = 0):
    """Train Step 02 `KuhnTrainer` and wrap its average strategy as a Game-interface policy.

    Returns (policy, node_map). `node_map` (info_set -> InfoSetNode) is reused directly by the
    exact Step 02 exploitability metric elsewhere. Kuhn only; for Leduc use step07's
    `nash.solve_nash(make_game("leduc"), iters)` (documented -- SCALE extension).
    """
    if game.name != "kuhn":
        raise NotImplementedError(
            "make_cfr_policy currently generates Kuhn data. For Leduc (SCALE), generate "
            "near-Nash play with step07's nash.solve_nash(make_game('leduc'), iters)."
        )
    from cfr.cfr_trainer import KuhnTrainer

    random.seed(seed)  # KuhnTrainer uses module-level random.shuffle; seed for reproducibility
    trainer = KuhnTrainer()
    trainer.train(iters)
    table = {}
    for iset, node in trainer.node_map.items():
        avg = node.get_average_strategy()  # [p_pass, p_bet]
        table[iset] = {_PASS: float(avg[_PASS]), _BET: float(avg[_BET])}
    return tabular_policy(table), trainer.node_map


# --- opponent mix --------------------------------------------------------------------
def build_opponent_mix(game, nash_policy, seed: int = 0):
    """Return [(policy, label), ...] = near-Nash + exploitable archetypes (raw L376-377).

    The exploitable types come from Step 07's zoo (TightPassive, LooseAggressive, ...); Nash is
    the near-Nash CFR policy passed in (so we do not re-solve).
    """
    zoo = make_type_zoo(game, include_nash=False, include_random=False)
    mix = [(nash_policy, "Nash")]
    for name, pol in zoo.items():
        mix.append((pol, name))
    return mix


# --- the dataset ---------------------------------------------------------------------
class PokerTrajectoryDataset:
    """Generate DT training trajectories for Kuhn (or Leduc, SCALE) poker.

    Args:
        game_name      : "kuhn" (validated) or "leduc" (SCALE extension).
        recipe         : "self_play_nash" or "mixed_opponents".
        n_trajectories : number of hero trajectories to collect.
        hero           : which seat's experience we keep as data (0 or 1). In "self_play_nash"
                         we keep BOTH seats (so `n_trajectories` hands yield ~2x trajectories,
                         truncated to n_trajectories).
        exploit_frac   : (mixed recipe) probability the hero plays the exact best response to
                         the sampled opponent rather than Nash. Higher -> more exploitative,
                         higher-variance return-to-go.
        cfr_iters      : CFR budget for the near-Nash policy.
        seed           : RNG seed (Python random + numpy) for reproducibility.
    """

    def __init__(self, game_name: str = "kuhn", recipe: str = "self_play_nash",
                 n_trajectories: int = 50000, hero: int = 0, exploit_frac: float = 0.5,
                 cfr_iters: int = 30000, seed: int = 0):
        self.game = make_game(game_name)
        self.game_name = game_name.lower()
        self.recipe = recipe
        self.hero = hero
        self.num_actions = _NUM_ACTIONS[self.game_name]
        self.encoder = PokerStateEncoder(self.game_name)
        self.state_dim = self.encoder.state_dim
        self.rng = random.Random(seed)

        self.nash_policy, self.nash_node_map = make_cfr_policy(self.game, cfr_iters, seed)
        self.trajectories: list = []
        self._generate(n_trajectories, recipe, exploit_frac)

    # ---- generation ----
    def _generate(self, n: int, recipe: str, exploit_frac: float) -> None:
        deals = self.game.deals()
        if recipe == "self_play_nash":
            policies = [self.nash_policy, self.nash_policy]
            while len(self.trajectories) < n:
                deal = self.rng.choice(deals)
                for traj in self._play_and_record(policies, deal, "Nash", keep_both=True):
                    self.trajectories.append(traj)
                    if len(self.trajectories) >= n:
                        break
        elif recipe == "mixed_opponents":
            mix = build_opponent_mix(self.game, self.nash_policy)
            # Precompute the exact best response for BOTH hero seats vs each opponent (raw L379).
            # We randomize the hero's seat per hand so the data covers ALL info sets (both P0 and
            # P1); otherwise ARDT would never see one player's decisions.
            br_by_seat_opp = {seat: {label: best_response_policy(self.game, seat, pol)
                                     for pol, label in mix} for seat in (0, 1)}
            while len(self.trajectories) < n:
                opp_pol, opp_label = self.rng.choice(mix)
                hero_seat = self.rng.randint(0, 1)
                use_br = self.rng.random() < exploit_frac
                hero_pol = br_by_seat_opp[hero_seat][opp_label] if use_br else self.nash_policy
                policies = [None, None]
                policies[hero_seat] = hero_pol
                policies[1 - hero_seat] = opp_pol
                deal = self.rng.choice(deals)
                for traj in self._play_and_record(policies, deal, opp_label, keep_both=False,
                                                  hero_seat=hero_seat):
                    self.trajectories.append(traj)
                    if len(self.trajectories) >= n:
                        break
        else:
            raise ValueError(f"Unknown recipe {recipe!r}; use 'self_play_nash' or "
                             "'mixed_opponents'.")

    def _play_and_record(self, policies, deal, opp_label: str, keep_both: bool,
                         hero_seat: int | None = None):
        """Play one hand; return the trajectory(ies) we keep (hero-only, or both seats)."""
        state = self.game.root(deal)
        per_player = {0: [], 1: []}
        while not self.game.is_terminal(state):
            p = self.game.current_player(state)
            dist = policies[p](self.game, state)
            a = sample_action(dist, self.rng)
            vec = self.encoder.encode(self.game, state, p)
            card = int(self._private_card(state, p))
            per_player[p].append(Step(vec, a, len(per_player[p]), card,
                                      tuple(self.game.legal_actions(state))))
            state = self.game.apply(state, a)
        rets = (self.game.utility(state, 0), self.game.utility(state, 1))

        seats = (0, 1) if keep_both else (self.hero if hero_seat is None else hero_seat,)
        out = []
        for p in seats:
            steps = per_player[p]
            if not steps:
                continue
            for st in steps:
                st.rtg = float(rets[p])  # reward only at terminal -> RTG constant per hand
            out.append(Trajectory(steps=steps, hero=p, ret=float(rets[p]), opponent=opp_label))
        return out

    def _private_card(self, state, player: int) -> int:
        return int(state.cards[player])

    # ---- tensors for training ----
    def to_tensors(self, max_len: int | None = None) -> dict:
        """Pad trajectories into arrays for the DT.

        Returns dict of numpy arrays:
            returns_to_go : (N, T, 1) float32
            states        : (N, T, state_dim) float32
            actions       : (N, T) int64   (padded with 0; use `mask`)
            timesteps     : (N, T) int64
            mask          : (N, T) float32  (1 = real step, 0 = pad)
        """
        if not self.trajectories:
            raise RuntimeError("No trajectories generated.")
        T = max_len or max(len(t.steps) for t in self.trajectories)
        N = len(self.trajectories)
        rtg = np.zeros((N, T, 1), dtype=np.float32)
        states = np.zeros((N, T, self.state_dim), dtype=np.float32)
        actions = np.zeros((N, T), dtype=np.int64)
        timesteps = np.zeros((N, T), dtype=np.int64)
        mask = np.zeros((N, T), dtype=np.float32)
        for i, traj in enumerate(self.trajectories):
            for j, st in enumerate(traj.steps[:T]):
                rtg[i, j, 0] = st.rtg
                states[i, j] = st.state_vec
                actions[i, j] = st.action
                timesteps[i, j] = st.timestep
                mask[i, j] = 1.0
        return {"returns_to_go": rtg, "states": states, "actions": actions,
                "timesteps": timesteps, "mask": mask}

    # ---- diagnostics ----
    def return_stats(self) -> dict:
        """Per-seat mean return -- data-quality check vs the known Kuhn game value (raw L293).

        Prediction: with near-Nash self-play, seat 0 (acts first) mean approx -1/18 ~ -0.0556,
        seat 1 approx +1/18. (Kuhn's first-mover disadvantage.) These are TARGETS to verify.
        """
        by_seat = {0: [], 1: []}
        for t in self.trajectories:
            by_seat[t.hero].append(t.ret)
        out = {}
        for s in (0, 1):
            arr = np.array(by_seat[s], dtype=np.float64) if by_seat[s] else np.array([0.0])
            out[s] = {"n": len(by_seat[s]), "mean": float(arr.mean()),
                      "std": float(arr.std())}
        out["nash_value_seat0"] = -1.0 / 18.0
        return out

    def action_counts_by_card(self) -> dict:
        """{card: {action: count}} over the FIRST decision of each trajectory.

        Feeds the Paster luck-vs-skill test: if a model's "good play" depends on the card dealt
        rather than the situation, its action distribution is card-driven (raw L321).
        """
        out: dict = {}
        for t in self.trajectories:
            if not t.steps:
                continue
            st = t.steps[0]
            d = out.setdefault(st.card, {})
            d[st.action] = d.get(st.action, 0) + 1
        return out


# --- self-test (you run this) --------------------------------------------------------
def _selftest():
    print("trajectory_dataset self-test")
    print("-" * 60)
    # Tiny budget so the self-test is quick; real runs use config.py sizes.
    ds = PokerTrajectoryDataset("kuhn", recipe="self_play_nash",
                                n_trajectories=2000, cfr_iters=2000, seed=0)
    print(f"generated {len(ds.trajectories)} trajectories; state_dim={ds.state_dim}")
    stats = ds.return_stats()
    print(f"seat0 mean return = {stats[0]['mean']:+.4f} (target approx {stats['nash_value_seat0']:+.4f})")
    print(f"seat1 mean return = {stats[1]['mean']:+.4f} (target approx {-stats['nash_value_seat0']:+.4f})")
    t = ds.to_tensors()
    print(f"tensors: states{t['states'].shape} actions{t['actions'].shape} "
          f"rtg{t['returns_to_go'].shape} mask sum={t['mask'].sum():.0f}")
    print("by-card first-action counts:", ds.action_counts_by_card())

    ds2 = PokerTrajectoryDataset("kuhn", recipe="mixed_opponents",
                                 n_trajectories=1500, cfr_iters=2000, exploit_frac=0.5, seed=1)
    opps = {}
    for tr in ds2.trajectories:
        opps[tr.opponent] = opps.get(tr.opponent, 0) + 1
    print("mixed-opponent trajectory counts by opponent:", opps)
    print("done.")


if __name__ == "__main__":
    _selftest()
