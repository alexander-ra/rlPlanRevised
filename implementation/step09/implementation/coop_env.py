"""
coop_env.py -- a small COOPERATIVE environment with partial observability + a global state.

WHY THIS EXISTS
---------------
The raw step's CTDE / communication experiments target PettingZoo MPE `simple_spread`
(L133-138, L426-431). Per WORKFLOW.md the core must run on the repo's own code, so this is a
self-contained stand-in that isolates the two things we actually need to validate:

  1. COMMUNICATION helps (raw step Validation L456): the listener cannot solve the task from
     its own observation; a learned message channel lets it succeed.
  2. A CENTRALIZED critic has LOWER VARIANCE than independent critics (Validation L453):
     because the centralized value sees the global state + joint actions, its value targets
     are (near-)deterministic, whereas an independent critic sees a non-stationary,
     partially-observed world and its targets are noisy.

THE TASK (CoopSignal): a one-step cooperative "referential game".
  - A target g in {0..K-1} is drawn uniformly. It is the GLOBAL STATE.
  - Agent 0 (the SPEAKER) observes a one-hot of g. Agent 1 (the LISTENER) observes zeros.
  - If communication is enabled, the speaker emits a message vector delivered to the listener.
  - Each agent outputs an action in {0..K-1}. Shared reward = 1.0 iff BOTH actions equal g,
    else 0.0.
  - Without communication the listener can do no better than 1/K (guessing); with a learned
    message it can reach ~1.0. The speaker's own action is trivially learnable (it sees g).

One-step (contextual-bandit style) on purpose: it makes the communication benefit and the
critic-variance comparison exact and cheap, with no confound from long-horizon credit
assignment.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy-only.
"""

from __future__ import annotations

import numpy as np


class CoopSignalEnv:
    """One-step cooperative referential game (speaker/listener). See module docstring."""

    n_agents = 2
    SPEAKER = 0
    LISTENER = 1

    def __init__(self, n_targets: int = 4, comm: bool = False, msg_dim: int | None = None,
                 seed: int = 0):
        self.n_targets = int(n_targets)
        self.comm = bool(comm)
        self.msg_dim = int(msg_dim) if msg_dim is not None else self.n_targets
        self.rng = np.random.default_rng(seed)
        self._g = 0  # current target

    # ---- shapes (so learners can size their networks) ----
    @property
    def n_actions(self) -> int:
        return self.n_targets

    @property
    def obs_dim(self) -> int:
        """Per-agent observation size. With comm, the listener's obs is concatenated with a
        message; we expose the base obs size here and deliver messages separately via step()."""
        return self.n_targets

    @property
    def global_state_dim(self) -> int:
        return self.n_targets

    # ---- dynamics ----
    def reset(self):
        """Draw a target; return (observations, global_state)."""
        self._g = int(self.rng.integers(self.n_targets))
        return self.observations(), self.global_state()

    def observations(self):
        """One-hot of g for the speaker; zeros for the listener (partial observability)."""
        speaker_obs = np.zeros(self.n_targets, dtype=np.float32)
        speaker_obs[self._g] = 1.0
        listener_obs = np.zeros(self.n_targets, dtype=np.float32)
        return [speaker_obs, listener_obs]

    def global_state(self):
        s = np.zeros(self.n_targets, dtype=np.float32)
        s[self._g] = 1.0
        return s

    def step(self, actions):
        """actions = [a_speaker, a_listener]. Returns (reward_shared, done, info)."""
        a0, a1 = int(actions[0]), int(actions[1])
        reward = 1.0 if (a0 == self._g and a1 == self._g) else 0.0
        info = {"target": self._g, "speaker_correct": a0 == self._g,
                "listener_correct": a1 == self._g}
        return reward, True, info

    @property
    def target(self) -> int:
        return self._g

    def optimal_reward_no_comm(self) -> float:
        """Best achievable expected reward WITHOUT communication: speaker always right,
        listener guesses -> 1/K."""
        return 1.0 / self.n_targets

    def optimal_reward_with_comm(self) -> float:
        """With a sufficient message channel the listener can always match -> 1.0."""
        return 1.0


class ClimbingGame:
    """The Claus & Boutilier (1998) 'climbing game' -- a stateless cooperative matrix game
    where INDEPENDENT learners get trapped by miscoordination penalties while a joint-action
    (centralized) learner finds the optimum. A clean IL-vs-CTDE contrast.

    Shared payoff matrix (both agents receive it):
                 b0    b1    b2
        a0 |    11   -30     0
        a1 |   -30     7     6
        a2 |     0     0     5
    The optimum (a0,b0)=11 is flanked by -30 penalties; the "safe" (a2,b2)=5 attracts
    independent learners (relative overgeneralization).
    """

    n_agents = 2

    PAYOFF = np.array([[11.0, -30.0, 0.0],
                       [-30.0, 7.0, 6.0],
                       [0.0, 0.0, 5.0]])

    def __init__(self):
        self.n_actions = self.PAYOFF.shape[0]

    def step(self, actions):
        r = float(self.PAYOFF[int(actions[0]), int(actions[1])])
        return r, True, {}

    def optimal(self):
        return 11.0, (0, 0)

    def safe(self):
        return 5.0, (2, 2)


def _selftest():
    print("coop_env self-test")
    print("-" * 60)
    env = CoopSignalEnv(n_targets=4, comm=False, seed=0)
    obs, gs = env.reset()
    print(f"[CoopSignal] target={env.target} speaker_obs={obs[0].tolist()} "
          f"listener_obs={obs[1].tolist()} global={gs.tolist()}")
    r_match, done, info = env.step([env.target, env.target])
    r_miss, _, _ = env.step([env.target, (env.target + 1) % 4])
    print(f"   reward(both match)={r_match} reward(listener wrong)={r_miss} done={done}")
    print(f"   no-comm ceiling={env.optimal_reward_no_comm():.3f}  "
          f"comm ceiling={env.optimal_reward_with_comm():.3f}")
    cg = ClimbingGame()
    print(f"[Climbing] optimal={cg.optimal()} safe={cg.safe()} "
          f"r(a0,b0)={cg.step([0,0])[0]} r(a0,b1)={cg.step([0,1])[0]}")


if __name__ == "__main__":
    _selftest()
