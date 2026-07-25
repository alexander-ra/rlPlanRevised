"""
strategy_extraction.py  [CORE]  -- raw L430-446.

Turns ANY agent (DT, ARDT, BC, LLM, or a plain Game-interface policy) into a Kuhn strategy
profile in EXACTLY the shape Step 02's exact exploitability metric consumes: a
`node_map` mapping each of the 12 Kuhn info sets to an object with `.get_average_strategy()`
returning `[p_pass, p_bet]`. This is the bridge that lets every method be scored on the same
exact ruler (raw L432-446).

The 12 Kuhn info sets (Step 02 convention: `str(card) + history`):
    P0: 1, 2, 3, 1pb, 2pb, 3pb        P1: 1p, 2p, 3p, 1b, 2b, 3b

Torch is imported lazily INSIDE the neural extractors, so this module (and `evaluation`,
`comparison_table`) stay importable and usable for the CFR/LLM paths with no torch installed.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import deps  # noqa: F401
from engines import KuhnState
from policies import materialize

_PASS, _BET = 0, 1

KUHN_P0_INFO_SETS = ["1", "2", "3", "1pb", "2pb", "3pb"]
KUHN_P1_INFO_SETS = ["1p", "2p", "3p", "1b", "2b", "3b"]
KUHN_INFO_SETS = KUHN_P0_INFO_SETS + KUHN_P1_INFO_SETS


class _StrategyNode:
    """Minimal stand-in for step02's InfoSetNode: only `.get_average_strategy()` is needed by
    `compute_exploitability` / `best_response_value`."""

    def __init__(self, avg):
        self._avg = [float(avg[_PASS]), float(avg[_BET])]

    def get_average_strategy(self):
        return list(self._avg)


def _parse_info_set(iset: str):
    card = int(iset[0])
    history = iset[1:]
    player = len(history) % 2  # seat 0 acts first
    return card, history, player


def _build_kuhn_state(card: int, history: str, player: int) -> KuhnState:
    other = 2 if card != 2 else 1  # any distinct valid card; encoding uses only the acting card
    cards = (card, other) if player == 0 else (other, card)
    return KuhnState(cards, history)


# --- neural extractors (torch, lazy) -------------------------------------------------
def extract_dt_strategy(model, encoder, game, target_return: float, device: str = "cpu") -> dict:
    """Query the DT at every info set, conditioned on `target_return`, into a node_map."""
    import torch

    model = model.to(device)
    model.eval()
    node_map = {}
    for iset in KUHN_INFO_SETS:
        card, history, player = _parse_info_set(iset)
        vec = encoder.encode(game, _build_kuhn_state(card, history, player), player)
        states = torch.as_tensor(vec, dtype=torch.float32, device=device).view(1, 1, -1)
        actions = torch.zeros((1, 1), dtype=torch.long, device=device)
        rtg = torch.full((1, 1, 1), float(target_return), dtype=torch.float32, device=device)
        timesteps = torch.zeros((1, 1), dtype=torch.long, device=device)
        mask = torch.ones((1, 1), dtype=torch.float32, device=device)
        probs = model.action_probs(states, actions, rtg, timesteps, mask)[0].tolist()
        node_map[iset] = _StrategyNode(probs)
    return node_map


def extract_ardt_strategy(ardt, encoder, game, device: str = "cpu") -> dict:
    """Like the DT extractor, but each info set is conditioned on ARDT's ESTIMATED MINIMAX
    (worst-case) return for that state -- the whole point of ARDT."""
    import torch  # noqa: F401

    ardt.dt.to(device)
    ardt.dt.eval()
    ardt.estimator.to(device)
    node_map = {}
    for iset in KUHN_INFO_SETS:
        card, history, player = _parse_info_set(iset)
        vec = encoder.encode(game, _build_kuhn_state(card, history, player), player)
        target = ardt.robust_target(vec, device=device)
        node_map[iset] = _dt_single(ardt.dt, encoder, game, vec, target, device)
    return node_map


def _dt_single(model, encoder, game, vec, target_return, device):
    import torch

    states = torch.as_tensor(vec, dtype=torch.float32, device=device).view(1, 1, -1)
    actions = torch.zeros((1, 1), dtype=torch.long, device=device)
    rtg = torch.full((1, 1, 1), float(target_return), dtype=torch.float32, device=device)
    timesteps = torch.zeros((1, 1), dtype=torch.long, device=device)
    mask = torch.ones((1, 1), dtype=torch.float32, device=device)
    probs = model.action_probs(states, actions, rtg, timesteps, mask)[0].tolist()
    return _StrategyNode(probs)


def extract_bc_strategy(model, encoder, game, device: str = "cpu") -> dict:
    """Behavioral-cloning strategy: state -> action probs, no return conditioning."""
    import torch

    model = model.to(device)
    model.eval()
    node_map = {}
    for iset in KUHN_INFO_SETS:
        card, history, player = _parse_info_set(iset)
        vec = encoder.encode(game, _build_kuhn_state(card, history, player), player)
        s = torch.as_tensor(vec, dtype=torch.float32, device=device).view(1, -1)
        probs = model.action_probs(s)[0].tolist()
        node_map[iset] = _StrategyNode(probs)
    return node_map


# --- policy extractor (torch-free: CFR, LLM, any Game policy) -------------------------
def extract_policy_strategy(policy_fn, game) -> dict:
    """Materialize a Game-interface policy (both seats) into a node_map. Works for the CFR
    near-Nash policy and for an `llm_policy(...)` wrapper."""
    node_map = {}
    for player in (0, 1):
        table = materialize(game, policy_fn, player)
        for iset, dist in table.items():
            node_map[iset] = _StrategyNode([dist.get(_PASS, 0.0), dist.get(_BET, 0.0)])
    return node_map


# --- luck-vs-skill probe -------------------------------------------------------------
def dt_root_bet_prob_by_card(model, encoder, game, target_return: float,
                             device: str = "cpu") -> dict:
    """Root-node P(bet) for each card under a fixed target return (Paster luck-vs-skill test)."""
    import torch  # noqa: F401

    out = {}
    for card in (1, 2, 3):
        vec = encoder.encode(game, _build_kuhn_state(card, "", 0), 0)
        node = _dt_single(model, encoder, game, vec, target_return, device)
        out[card] = node.get_average_strategy()[_BET]
    return out


def _selftest():
    from engines import make_game
    from trajectory_dataset import make_cfr_policy

    print("strategy_extraction self-test (CFR path; torch-free)")
    print("-" * 60)
    game = make_game("kuhn")
    nash_policy, _ = make_cfr_policy(game, iters=3000, seed=0)
    node_map = extract_policy_strategy(nash_policy, game)
    print(f"extracted {len(node_map)} info sets (expect 12): "
          f"{sorted(node_map.keys())}")
    print("root strategies (P(pass), P(bet)):")
    for iset in KUHN_P0_INFO_SETS[:3]:
        print(f"  {iset}: {['%.2f' % x for x in node_map[iset].get_average_strategy()]}")


if __name__ == "__main__":
    _selftest()
