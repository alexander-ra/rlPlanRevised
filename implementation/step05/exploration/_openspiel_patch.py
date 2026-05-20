"""Runtime patch for an OpenSpiel PyTorch Deep CFR bug.

The bundled `deep_cfr.DeepCFRSolver._learn_advantage_network` returns `None`
*before* doing the optimizer step on the advantage network — so the advantage
networks never train. The strategy network still trains (its sibling check at
line 603 is written correctly), which is why `policy_loss` looks healthy but
exploitability stays flat at random-strategy levels.

The buggy line, from `open_spiel/python/pytorch/deep_cfr.py:565`:

    if len(samples.info_state == 0):
        return None

`samples.info_state == 0` is an elementwise boolean array of length 128 (the
batch size); `len(...)` returns 128, which is truthy, so the `return None` is
taken every time. The intended check was `if len(samples.info_state) == 0:`.

We apply the fix as a monkey-patch so we don't have to fork OpenSpiel. Import
this module *before* constructing a `DeepCFRSolver`.

OpenSpiel version observed: 1.6.12 (open_spiel/python/pytorch/deep_cfr.py).
Revisit when bumping OpenSpiel — the patch is a no-op if the source already
reads `len(samples.info_state) == 0`.
"""

from __future__ import annotations

import inspect

import torch
from open_spiel.python.pytorch import deep_cfr


def _patched_learn_advantage_network(self, player):
    for _ in range(self._advantage_network_train_steps):
        if self._batch_size_advantage:
            if self._batch_size_advantage > len(self._advantage_memories[player]):
                return None
            samples = self._advantage_memories[player].sample(
                self._batch_size_advantage
            )
        else:
            self._advantage_memories[player].shuffle()
            samples = self._advantage_memories[player].experience

        if len(samples.info_state) == 0:
            return None

        self._optimizer_advantages[player].zero_grad()
        iters = torch.FloatTensor(samples.iteration, device=self._device).sqrt()
        outputs = self._advantage_networks[player](
            torch.FloatTensor(samples.info_state, device=self._device)
        )
        advantages = torch.FloatTensor(samples.advantage, device=self._device)
        loss_advantages = self._loss_advantages(
            iters * outputs, iters * advantages
        )
        loss_advantages.backward()
        self._optimizer_advantages[player].step()

    return loss_advantages.detach().cpu().item()


def apply():
    src = inspect.getsource(deep_cfr.DeepCFRSolver._learn_advantage_network)
    if "len(samples.info_state == 0)" in src:
        deep_cfr.DeepCFRSolver._learn_advantage_network = (
            _patched_learn_advantage_network
        )
        print("[openspiel_patch] applied Deep CFR _learn_advantage_network fix")
    else:
        print("[openspiel_patch] OpenSpiel already patched; skipping")


# Convenience: applying on import keeps call sites short.
apply()
