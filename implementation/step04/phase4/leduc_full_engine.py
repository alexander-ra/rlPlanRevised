"""Phase 4 shim around step03's Leduc engine.

Re-exports `LeducState`, `ALL_DEALS`, `NUM_ACTIONS`, action constants, and
`InfoSetNode` so phase-4 trainers can target the original 6-card game
without scattering relative imports through every module. There is no
behavioural difference from step03 — this is a single place to tweak if
the upstream interface ever moves.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_STEP03 = os.path.abspath(os.path.join(_HERE, "..", "..", "step03"))
if _STEP03 not in sys.path:
    sys.path.insert(0, _STEP03)

from cfr.leduc_poker import (  # noqa: E402
    ALL_DEALS,
    LeducState,
    NUM_ACTIONS,
    NUM_CARDS,
    FOLD,
    CHECK_CALL,
    RAISE,
    ACTION_NAMES,
    card_rank,
)
from cfr.info_set_node import InfoSetNode  # noqa: E402
from evaluate.best_response import best_response_value  # noqa: E402

__all__ = [
    "ALL_DEALS",
    "LeducState",
    "NUM_ACTIONS",
    "NUM_CARDS",
    "FOLD",
    "CHECK_CALL",
    "RAISE",
    "ACTION_NAMES",
    "card_rank",
    "InfoSetNode",
    "best_response_value",
]
