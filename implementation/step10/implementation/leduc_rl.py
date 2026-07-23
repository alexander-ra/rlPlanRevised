"""
leduc_rl.py -- the RL adapter that lets a neural agent PLAY Leduc, and the bridge that turns a
trained net back into an EXACT tabular policy (raw step 10 L408-438; the "neural train, exact
evaluate" design confirmed for this step).

WHY THIS MODULE EXISTS
----------------------
Step 07/09 evaluate policies EXACTLY over the Leduc game tree (`exact_value`, `nash_gap`). But
a PBT league trains NEURAL agents by self-play rollouts. This module is the seam between the
two worlds:

  1. `encode_info_set(iset)` : turn a Leduc information-set string into a fixed-length feature
     vector a small MLP can consume (structured: private/board card ranks + round + betting
     history), so the net can GENERALISE across similar spots rather than memorise indices.
  2. `rollout(...)`          : play one Leduc hand with a hero acting via a net (`act_fn`) and
     an opponent acting via any `policy(game,state)` -> transitions + terminal reward, so the
     PPO agent can learn from Monte-Carlo returns.
  3. `extract_tabular_policy(game, probs_fn)` : walk the WHOLE tree and read the net's action
     distribution at every info set (via Step 07's `materialize`), producing a plain tabular
     behavioral policy. That policy is then fed to the EXACT engine -- so exploitability, the
     EGTA payoff matrix, Elo and the spinning-top decomposition are all computed on ground
     truth, with the net's stochastic training the only source of noise.

Validity of (3) rests on Leduc's PERFECT RECALL (same assumption as Step 09's
`mixture_behavioral_policy`): a behavioral policy read off per-info-set is realization-
equivalent to what the net actually plays.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (puts step09 + step07 on sys.path)
from policies import tabular_policy, materialize, sample_action

# Leduc actions (mirror step03/cfr/leduc_poker.py): FOLD=0, CHECK_CALL=1, RAISE=2.
FOLD, CHECK_CALL, RAISE = 0, 1, 2
N_ACTIONS = 3

# --- feature layout -----------------------------------------------------------------
_N_RANKS = 3            # J, Q, K  (Leduc card rank = card // 2)
_MAX_HIST = 8           # max betting-action chars we encode (Leduc rounds are short)
_ACTION_CHARS = ("f", "c", "r")   # fold / check-call / raise (matches ACTION_NAMES)
# [priv rank one-hot 3] [board rank one-hot 3] [board-known 1] [round one-hot 2] [history 8*3]
OBS_DIM = _N_RANKS + _N_RANKS + 1 + 2 + _MAX_HIST * len(_ACTION_CHARS)


def encode_info_set(iset: str) -> np.ndarray:
    """Leduc info-set string -> fixed-length float32 feature vector (length OBS_DIM).

    Info-set format (from LeducState.get_info_set):
        round 0:  "<card>|<history>"                 e.g. "4|cr"
        round 1:  "<card>:<community>|<history>"      e.g. "4:2|cr/c"
    card / community are ids 0-5; rank = id // 2. `history` uses chars c/r/f and '/' (round
    separator). We encode CARD RANK (not id) because rank drives strategy; the '/' is dropped
    (the round is captured explicitly).
    """
    vec = np.zeros(OBS_DIM, dtype=np.float32)
    left, _, hist = iset.partition("|")

    if ":" in left:
        card_s, comm_s = left.split(":")
        card = int(card_s)
        comm = int(comm_s)
        round_idx = 1
    else:
        card = int(left)
        comm = None
        round_idx = 0

    off = 0
    # private card rank one-hot
    vec[off + (card // 2)] = 1.0
    off += _N_RANKS
    # board card rank one-hot + known flag
    if comm is not None:
        vec[off + (comm // 2)] = 1.0
    off += _N_RANKS
    vec[off] = 1.0 if comm is not None else 0.0
    off += 1
    # round one-hot (0 or 1)
    vec[off + round_idx] = 1.0
    off += 2
    # betting history: ordered one-hot over {f,c,r}, drop the '/' separators, pad/truncate
    actions = [ch for ch in hist if ch in _ACTION_CHARS]
    for i, ch in enumerate(actions[:_MAX_HIST]):
        vec[off + i * len(_ACTION_CHARS) + _ACTION_CHARS.index(ch)] = 1.0
    return vec


def masked_distribution(raw_probs, legal_actions) -> dict:
    """Restrict a length-N_ACTIONS probability vector to the legal actions and renormalize.
    A defensive uniform fallback covers the (degenerate) all-zero-mass case."""
    raw = np.asarray(raw_probs, dtype=float)
    restricted = {a: max(0.0, float(raw[a])) for a in legal_actions}
    total = sum(restricted.values())
    if total <= 0.0:
        p = 1.0 / len(legal_actions)
        return {a: p for a in legal_actions}
    return {a: v / total for a, v in restricted.items()}


def make_net_policy(probs_fn):
    """Wrap a net's `probs_fn(obs) -> length-N_ACTIONS array` as a Step 07 policy
    `policy(game, state) -> {action: prob}` (masked to legal actions).

    `probs_fn` must be DETERMINISTIC given `obs` (it is read exhaustively by
    `extract_tabular_policy` / `materialize`)."""
    def policy(game, state):
        legal = game.legal_actions(state)
        obs = encode_info_set(game.info_set(state))
        return masked_distribution(probs_fn(obs), legal)
    return policy


def extract_tabular_policy(game, probs_fn):
    """Read the net's distribution at EVERY info set (both seats) -> one tabular behavioral
    policy usable by the exact engine. Info-set strings partition by acting player (the acting
    player is fixed by the betting-history parity), so merging the two seats' tables is safe.
    """
    net_pol = make_net_policy(probs_fn)
    table = materialize(game, net_pol, 0)
    table.update(materialize(game, net_pol, 1))
    return tabular_policy(table)


def rollout(game, hero_seat: int, act_fn, opp_policy, rng):
    """Play one Leduc hand; the hero (seat `hero_seat`) acts via `act_fn`, the opponent via
    `opp_policy`.

    act_fn(obs, legal_actions) -> (action:int, logp:float)   -- samples + returns log-prob.
    opp_policy(game, state) -> {action: prob}                -- any Step 07 policy.

    Returns (transitions, hero_utility) where transitions is a list of
    (obs, action, logp, mask) tuples at the hero's decision nodes -- `mask` is a length-
    N_ACTIONS 0/1 vector of the legal actions so PPO can recompute masked log-probs during the
    update. Leduc has no intermediate reward, so the Monte-Carlo return for EVERY hero decision
    this hand is the terminal `hero_utility`.
    """
    deal = game.deals()[rng.integers(len(game.deals()))]
    state = game.root(deal)
    transitions = []
    while not game.is_terminal(state):
        player = game.current_player(state)
        legal = game.legal_actions(state)
        if player == hero_seat:
            obs = encode_info_set(game.info_set(state, hero_seat))
            action, logp = act_fn(obs, legal)
            mask = np.zeros(N_ACTIONS, dtype=np.float32)
            mask[list(legal)] = 1.0
            transitions.append((obs, action, logp, mask))
            state = game.apply(state, action)
        else:
            dist = opp_policy(game, state)
            action = sample_action(dist, rng)
            state = game.apply(state, action)
    return transitions, float(game.utility(state, hero_seat))


def _selftest():
    print("leduc_rl self-test")
    print("-" * 60)
    from engines import make_game
    from policies import uniform_policy
    game = make_game("leduc")

    # encoding sanity: a few info sets encode to the right shape and are distinct.
    samples = ["4|", "4|cr", "4:2|cr/c", "0:5|r/"]
    vecs = [encode_info_set(s) for s in samples]
    print(f"OBS_DIM={OBS_DIM}; encoded {len(samples)} info sets, all shape "
          f"{vecs[0].shape} -> {all(v.shape == (OBS_DIM,) for v in vecs)}")
    distinct = len({v.tobytes() for v in vecs}) == len(samples)
    print(f"distinct encodings for distinct info sets: {distinct}")

    # a uniform 'net' (probs_fn returns uniform-over-3) extracts to a valid tabular policy.
    uniform_probs = lambda obs: np.ones(N_ACTIONS) / N_ACTIONS  # noqa: E731
    tab = extract_tabular_policy(game, uniform_probs)
    # the extracted uniform-over-legal policy must match Step 07's uniform_policy exactly on EV.
    from best_response import exact_value
    v_extracted = exact_value(game, 0, tab, tab)
    v_uniform = exact_value(game, 0, uniform_policy(), uniform_policy())
    print(f"extracted-uniform vs uniform_policy EV(P0): {v_extracted:+.4f} vs {v_uniform:+.4f} "
          f"(PREDICT ~equal: both uniform-over-legal)")

    # rollout smoke: greedy-random hero vs uniform opp returns a finite utility + transitions.
    rng = np.random.default_rng(0)
    def rand_act(obs, legal):
        a = int(rng.choice(legal))
        return a, float(np.log(1.0 / len(legal)))
    tr, u = rollout(game, 0, rand_act, uniform_policy(), rng)
    print(f"rollout: {len(tr)} hero decisions, terminal hero utility={u:+.1f}")


if __name__ == "__main__":
    _selftest()
