"""Timed CFR+ abstraction comparison across the three Step-04 game families.

Runs each selected configuration for a fixed wall-clock training budget,
repeats across seeds, evaluates exploitability in that configuration's
own full game, and renders a three-panel variance plot:

  1. fixed-limit Leduc abstractions,
  2. mini no-limit Leduc action abstractions,
  3. Extended Leduc combined abstractions.

The script is resumable. Each `(config, seed)` row is appended to
`.day07_cfrplus_results.json` as soon as it finishes; existing rows are
skipped on later runs unless `--force` is passed.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, stdev
from typing import Callable

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leduc_full_engine import ALL_DEALS as LEDUC_DEALS
from leduc_full_engine import InfoSetNode, LeducState
from leduc_rank_engine import CANONICAL_DEALS as LEDUC_RANK_DEALS
from leduc_rank_engine import LeducRankState
from day02_card_bucketing import build_card_buckets, make_key_translator
from day02_hand_strength import NUM_RANKS as LEDUC_RANKS
from exploitability import exploitability_full_game, exploitability_via_proxy
from mini_nl_leduc import (
    ALL_DEALS as MINI_DEALS,
    BET_LARGE,
    BET_SMALL,
    MiniNLLeducState,
)
from day03_train import best_response_full_game as mini_best_response
from extended_leduc import (
    ALL_DEALS as EXT_DEALS,
    CANONICAL_DEALS as EXT_RANK_DEALS,
    BET_LARGE as EXT_BET_LARGE,
    BET_SMALL as EXT_BET_SMALL,
    ExtendedLeducState,
)
from day04_combined import build_buckets as build_ext_buckets
from day04_combined import make_translator as make_ext_translator

RESULTS_PATH = Path(_HERE) / ".day07_cfrplus_results.json"
CSV_PATH = Path(_HERE) / ".day07_cfrplus_results.csv"
FIG_DIR = Path(_HERE) / "figures"
PLOT_PATH = FIG_DIR / "day07_cfrplus_three_panels.png"
PANEL_PLOT_PATHS = {
    "fixed": FIG_DIR / "day07_cfrplus_fixed_leduc.png",
    "mini": FIG_DIR / "day07_cfrplus_mini_nl_leduc.png",
    "extended": FIG_DIR / "day07_cfrplus_extended_leduc.png",
}


@dataclass
class Config:
    name: str
    panel: str
    label: str
    state_factory_builder: Callable[[int], Callable]
    deals_builder: Callable[[int], list]
    evaluator_builder: Callable[[int], Callable[[dict], float]]
    order: int


class TimedCFRPlus:
    """CFR+ over any Leduc-shaped state class."""

    def __init__(self):
        self.node_map: dict[str, tuple[InfoSetNode, list]] = {}

    def step(self, iter_num: int, state_factory: Callable, deals: list):
        strategy_weight = iter_num
        for traversing_player in (0, 1):
            regret_buffer: dict[str, list[float]] = {}
            for entry in deals:
                if _is_weighted_deal(entry):
                    deal, chance_weight = entry
                else:
                    deal, chance_weight = entry, 1.0
                state = state_factory((deal[0], deal[1]), deal[2])
                self._cfr(state, traversing_player, strategy_weight, 1.0,
                          chance_weight, regret_buffer)
            for info_set, deltas in regret_buffer.items():
                node, _ = self.node_map[info_set]
                for a, delta in enumerate(deltas):
                    node.regret_sum[a] = max(node.regret_sum[a] + delta, 0.0)

    def _cfr(self, state, traversing: int, strategy_weight: int,
             opp_reach: float, chance_weight: float,
             regret_buffer: dict[str, list[float]]) -> float:
        if state.is_terminal():
            return state.get_utility(traversing)

        player = state.current_player()
        info_set = state.get_info_set(player)
        legal = state.legal_actions()
        if info_set not in self.node_map:
            self.node_map[info_set] = (InfoSetNode(len(legal)), legal)
        node, _ = self.node_map[info_set]
        strategy = node.get_current_strategy()

        if player == traversing:
            utils = [0.0] * len(legal)
            node_util = 0.0
            for idx, action in enumerate(legal):
                utils[idx] = self._cfr(
                    state.apply_action(action), traversing, strategy_weight,
                    opp_reach, chance_weight, regret_buffer)
                node_util += strategy[idx] * utils[idx]
            regret_buffer.setdefault(info_set, [0.0] * len(legal))
            for idx in range(len(legal)):
                regret_buffer[info_set][idx] += (
                    chance_weight * opp_reach * (utils[idx] - node_util))
            return node_util

        node_util = 0.0
        for idx, action in enumerate(legal):
            child_val = self._cfr(
                state.apply_action(action), traversing, strategy_weight,
                opp_reach * strategy[idx], chance_weight, regret_buffer)
            node_util += strategy[idx] * child_val
        for idx in range(len(legal)):
            node.strategy_sum[idx] += (
                chance_weight * opp_reach * strategy[idx] * strategy_weight)
        return node_util


class _BucketedRankState(LeducRankState):
    def __init__(self, cards, community, translator):
        super().__init__(cards, community)
        self._translator = translator

    def get_info_set(self, player: int) -> str:
        rank = self.cards[player]
        if self.round >= 1:
            full_key = f"{2 * rank}:{2 * self.community}|{self.history}"
        else:
            full_key = f"{2 * rank}|{self.history}"
        return self._translator(full_key)

    def apply_action(self, action: int) -> "_BucketedRankState":
        s = _BucketedRankState(self.cards, self.community, self._translator)
        _copy_common_state(self, s)
        s._do_action(action)
        return s


class _BucketedExtendedState(ExtendedLeducState):
    def __init__(self, cards, community, abstracted, rank_canonical,
                 translator):
        super().__init__(cards, community, abstracted=abstracted,
                         rank_canonical=rank_canonical)
        self._translator = translator

    def get_info_set(self, player: int) -> str:
        return self._translator(super().get_info_set(player))

    def apply_action(self, action: int) -> "_BucketedExtendedState":
        s = _BucketedExtendedState(self.cards, self.community,
                                   self.abstracted, self.rank_canonical,
                                   self._translator)
        _copy_common_state(self, s)
        s.stacks = list(self.stacks)
        s._do_action(action)
        return s


def _copy_common_state(src, dst):
    dst.history = src.history
    dst.round = src.round
    dst.bets = list(src.bets)
    dst.num_raises = list(src.num_raises)
    dst.round_actions = list(src.round_actions)
    dst.folded = src.folded
    dst._is_terminal = src._is_terminal


def _is_weighted_deal(entry) -> bool:
    return (
        isinstance(entry, tuple) and len(entry) == 2
        and isinstance(entry[1], (int, float))
        and isinstance(entry[0], tuple) and len(entry[0]) == 3
    )


def _fixed_rank_key(full_key: str) -> str:
    head, sep, tail = full_key.partition("|")
    if ":" in head:
        private, _, public = head.partition(":")
        head = f"{int(private) // 2}:{int(public) // 2}"
    else:
        head = str(int(head) // 2)
    return head + sep + tail


def _make_fixed_configs() -> list[Config]:
    configs = [
        Config(
            "fixed_full", "fixed", "Full CFR+",
            lambda seed: (lambda cards, community: LeducState(cards, community)),
            lambda seed: list(LEDUC_DEALS),
            lambda seed: (lambda nm: exploitability_full_game(nm) / 2.0),
            0,
        ),
        Config(
            "fixed_rank", "fixed", "Suit iso",
            lambda seed: (lambda cards, community: LeducRankState(cards, community)),
            lambda seed: list(LEDUC_RANK_DEALS),
            lambda seed: (
                lambda nm: exploitability_via_proxy(nm, _fixed_rank_key) / 2.0),
            1,
        ),
    ]
    spec = [
        ("k2_perfect", "k2 perfect", 2, 2, True, 2),
        ("k2_imperfect", "k2 imperfect", 2, 2, False, 3),
        ("k3_perfect", "k3 perfect", 3, 3, True, 4),
        ("k3_imperfect", "k3 imperfect", 3, 3, False, 5),
        ("k5_perfect", "k5 perfect", min(3, LEDUC_RANKS),
         min(5, LEDUC_RANKS * LEDUC_RANKS), True, 6),
        ("k5_imperfect", "k5 imperfect", min(3, LEDUC_RANKS),
         min(5, LEDUC_RANKS * LEDUC_RANKS), False, 7),
        ("full_bucket_perfect", "full bucket p", LEDUC_RANKS,
         LEDUC_RANKS * LEDUC_RANKS, True, 8),
        ("full_bucket_imperfect", "full bucket i", LEDUC_RANKS,
         LEDUC_RANKS * LEDUC_RANKS, False, 9),
    ]
    for name, label, kp, kf, recall, order in spec:
        full_name = f"fixed_{name}"

        def state_builder(seed, kp=kp, kf=kf, recall=recall):
            buckets = build_card_buckets(kp, kf, seed=seed)
            translator = make_key_translator(buckets, recall)
            return lambda cards, community: _BucketedRankState(
                cards, community, translator)

        def eval_builder(seed, kp=kp, kf=kf, recall=recall):
            buckets = build_card_buckets(kp, kf, seed=seed)
            translator = make_key_translator(buckets, recall)
            return lambda nm: exploitability_via_proxy(nm, translator) / 2.0

        configs.append(Config(
            full_name, "fixed", label, state_builder,
            lambda seed: list(LEDUC_RANK_DEALS), eval_builder, order))
    return configs


def _make_mini_configs() -> list[Config]:
    return [
        Config(
            "mini_full", "mini", "Full mini-NL",
            lambda seed: (
                lambda cards, community: MiniNLLeducState(
                    cards, community, abstracted=False)),
            lambda seed: list(MINI_DEALS),
            lambda seed: (
                lambda nm: (
                    mini_best_response(nm, 0)
                    + mini_best_response(nm, 1)) / 2.0),
            0,
        ),
        Config(
            "mini_action_abs", "mini", "Action abs",
            lambda seed: (
                lambda cards, community: MiniNLLeducState(
                    cards, community, abstracted=True)),
            lambda seed: list(MINI_DEALS),
            lambda seed: _mini_translator_eval("nearest"),
            1,
        ),
    ]


def _mini_translator_eval(translator_name: str):
    return lambda nm: (
        mini_best_response(nm, 0, translator_name=translator_name,
                           node_map_abstract=nm)
        + mini_best_response(nm, 1, translator_name=translator_name,
                             node_map_abstract=nm)
    ) / 2.0


def _make_extended_configs() -> list[Config]:
    return [
        Config(
            "ext_full", "extended", "Full extended",
            lambda seed: (
                lambda cards, community: ExtendedLeducState(
                    cards, community, abstracted=False,
                    rank_canonical=False)),
            lambda seed: list(EXT_DEALS),
            lambda seed: _extended_full_eval(),
            0,
        ),
        Config(
            "ext_suit", "extended", "Suit iso",
            lambda seed: (
                lambda cards, community: ExtendedLeducState(
                    cards, community, abstracted=False,
                    rank_canonical=True)),
            lambda seed: list(EXT_RANK_DEALS),
            lambda seed: _extended_proxy_eval(_extended_rank_key),
            1,
        ),
        Config(
            "ext_suit_action", "extended", "Suit + action",
            lambda seed: (
                lambda cards, community: ExtendedLeducState(
                    cards, community, abstracted=True,
                    rank_canonical=True)),
            lambda seed: list(EXT_RANK_DEALS),
            lambda seed: _extended_proxy_eval(
                _extended_rank_key, translate_actions=True),
            2,
        ),
        Config(
            "ext_triple", "extended", "Suit + action + buckets",
            lambda seed: _ext_triple_state_factory(seed),
            lambda seed: list(EXT_RANK_DEALS),
            lambda seed: _extended_proxy_eval(
                _ext_triple_key(seed), translate_actions=True),
            3,
        ),
    ]


def _ext_triple_state_factory(seed: int):
    buckets = build_ext_buckets(3, 3, seed=seed)
    translator = make_ext_translator(buckets, perfect_recall=False)
    return lambda cards, community: _BucketedExtendedState(
        cards, community, abstracted=True, rank_canonical=True,
        translator=translator)


def _ext_triple_key(seed: int):
    buckets = build_ext_buckets(3, 3, seed=seed)
    translator = make_ext_translator(buckets, perfect_recall=False)

    def translate(full_key: str) -> str:
        return translator(_extended_rank_key(full_key))

    return translate


def _extended_rank_key(full_key: str) -> str:
    head, sep, tail = full_key.partition("|")
    if ":" in head:
        private, _, public = head.partition(":")
        head = f"{int(private) // 2}:{int(public) // 2}"
    else:
        head = str(int(head) // 2)
    return head + sep + tail


def _extended_full_eval():
    return lambda nm: _extended_exploitability(nm, lambda key: key) / 2.0


def _extended_proxy_eval(key_translator, translate_actions: bool = False):
    return lambda nm: _extended_exploitability(
        nm, key_translator, translate_actions=translate_actions) / 2.0


def _extended_exploitability(node_map: dict, key_translator,
                             translate_actions: bool = False) -> float:
    br0 = _extended_best_response_value(
        node_map, 0, key_translator, translate_actions)
    br1 = _extended_best_response_value(
        node_map, 1, key_translator, translate_actions)
    return br0 + br1


def _extended_best_response_value(node_map: dict, br_player: int,
                                  key_translator,
                                  translate_actions: bool) -> float:
    br_strategy = {}
    for _ in range(10):
        br_cv = {}
        for deal in EXT_DEALS:
            state = ExtendedLeducState((deal[0], deal[1]), deal[2],
                                       abstracted=False,
                                       rank_canonical=False)
            _extended_br_accumulate(state, br_player, node_map, br_strategy,
                                    1.0, br_cv, key_translator,
                                    translate_actions)
        changed = False
        for info_set, action_vals in br_cv.items():
            best_a = max(action_vals, key=action_vals.get)
            if br_strategy.get(info_set) != best_a:
                changed = True
            br_strategy[info_set] = best_a
        if not changed:
            break

    total = 0.0
    for deal in EXT_DEALS:
        state = ExtendedLeducState((deal[0], deal[1]), deal[2],
                                   abstracted=False, rank_canonical=False)
        total += _extended_br_eval(state, br_player, node_map, br_strategy,
                                   key_translator, translate_actions)
    return total / len(EXT_DEALS)


def _extended_strategy(state, node_map: dict, key_translator,
                       translate_actions: bool) -> list[float]:
    legal = state.legal_actions()
    abstract_key = key_translator(state.get_info_set(state.current_player()))
    if abstract_key not in node_map:
        return [1.0 / len(legal)] * len(legal)
    node, abstract_legal = node_map[abstract_key]
    avg = node.get_average_strategy()
    abstract_mix = dict(zip(abstract_legal, avg))
    out = []
    for action in legal:
        if action in abstract_mix:
            out.append(abstract_mix[action])
        elif translate_actions and action == EXT_BET_LARGE:
            out.append(abstract_mix.get(EXT_BET_SMALL, 0.0))
        elif translate_actions and action == EXT_BET_SMALL:
            out.append(0.0 if EXT_BET_LARGE in legal
                       else abstract_mix.get(EXT_BET_SMALL, 0.0))
        else:
            out.append(0.0)
    total = sum(out)
    if total <= 0.0:
        return [1.0 / len(legal)] * len(legal)
    return [x / total for x in out]


def _extended_br_accumulate(state, br_player: int, node_map: dict,
                            br_strategy: dict, opp_reach: float,
                            br_cv: dict, key_translator,
                            translate_actions: bool) -> float:
    if state.is_terminal():
        return state.get_utility(br_player)
    player = state.current_player()
    legal = state.legal_actions()
    if player == br_player:
        info = state.get_info_set(player)
        br_cv.setdefault(info, {i: 0.0 for i in range(len(legal))})
        action_values = {}
        for idx, action in enumerate(legal):
            child_val = _extended_br_accumulate(
                state.apply_action(action), br_player, node_map, br_strategy,
                opp_reach, br_cv, key_translator, translate_actions)
            br_cv[info][idx] += opp_reach * child_val
            action_values[idx] = child_val
        if info in br_strategy:
            return action_values[br_strategy[info]]
        return max(action_values.values())

    strategy = _extended_strategy(
        state, node_map, key_translator, translate_actions)
    value = 0.0
    for idx, action in enumerate(legal):
        value += strategy[idx] * _extended_br_accumulate(
            state.apply_action(action), br_player, node_map, br_strategy,
            opp_reach * strategy[idx], br_cv, key_translator,
            translate_actions)
    return value


def _extended_br_eval(state, br_player: int, node_map: dict,
                      br_strategy: dict, key_translator,
                      translate_actions: bool) -> float:
    if state.is_terminal():
        return state.get_utility(br_player)
    player = state.current_player()
    legal = state.legal_actions()
    if player == br_player:
        info = state.get_info_set(player)
        chosen = br_strategy.get(info, 0)
        return _extended_br_eval(
            state.apply_action(legal[chosen]), br_player, node_map,
            br_strategy, key_translator, translate_actions)
    strategy = _extended_strategy(
        state, node_map, key_translator, translate_actions)
    value = 0.0
    for idx, action in enumerate(legal):
        value += strategy[idx] * _extended_br_eval(
            state.apply_action(action), br_player, node_map, br_strategy,
            key_translator, translate_actions)
    return value


def _train_one(config: Config, seed: int, budget: float,
               progress_every: float) -> dict:
    random.seed(seed)
    state_factory = config.state_factory_builder(seed)
    deals = config.deals_builder(seed)
    evaluator = config.evaluator_builder(seed)
    trainer = TimedCFRPlus()
    start = time.perf_counter()
    training_time = 0.0
    iter_num = 0
    next_progress = progress_every
    while training_time < budget:
        iter_num += 1
        t0 = time.perf_counter()
        trainer.step(iter_num, state_factory, deals)
        training_time += time.perf_counter() - t0
        if progress_every > 0 and training_time >= next_progress:
            print(
                f"    {config.label:<24} seed={seed} "
                f"train={training_time:6.1f}/{budget:.0f}s "
                f"iter={iter_num:>5} infos={len(trainer.node_map):>5}",
                flush=True,
            )
            while next_progress <= training_time:
                next_progress += progress_every

    eval_start = time.perf_counter()
    exploit = evaluator(trainer.node_map)
    eval_time = time.perf_counter() - eval_start
    wall_time = time.perf_counter() - start
    return {
        "panel": config.panel,
        "config": config.name,
        "label": config.label,
        "order": config.order,
        "seed": seed,
        "budget_sec": budget,
        "iterations": iter_num,
        "training_time_sec": training_time,
        "eval_time_sec": eval_time,
        "wall_time_sec": wall_time,
        "exploitability": exploit,
        "info_sets": len(trainer.node_map),
    }


def _load_results() -> list[dict]:
    if not RESULTS_PATH.exists():
        return []
    with RESULTS_PATH.open() as f:
        return json.load(f)


def _save_results(rows: list[dict]):
    with RESULTS_PATH.open("w") as f:
        json.dump(rows, f, indent=2)
    with CSV_PATH.open("w") as f:
        cols = [
            "panel", "config", "label", "seed", "budget_sec",
            "iterations", "training_time_sec", "eval_time_sec",
            "wall_time_sec", "exploitability", "gap_vs_full",
            "info_sets",
        ]
        f.write(",".join(cols) + "\n")
        for row in rows:
            f.write(",".join(_csv(row.get(c)) for c in cols) + "\n")


def _csv(value) -> str:
    if value is None:
        return ""
    text = str(value)
    if "," in text:
        return '"' + text.replace('"', '""') + '"'
    return text


def _with_gaps(rows: list[dict]) -> list[dict]:
    full_by_panel_seed = {}
    for row in rows:
        if row["config"] in {"fixed_full", "mini_full", "ext_full"}:
            full_by_panel_seed[(row["panel"], row["seed"])] = row[
                "exploitability"]
    out = []
    for row in rows:
        row = dict(row)
        baseline = full_by_panel_seed.get((row["panel"], row["seed"]))
        row["gap_vs_full"] = (
            None if baseline is None else row["exploitability"] - baseline)
        out.append(row)
    return out


def _all_configs() -> list[Config]:
    return _make_fixed_configs() + _make_mini_configs() + _make_extended_configs()


def _plot(rows: list[dict]):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    FIG_DIR.mkdir(exist_ok=True)
    panels = [
        ("fixed", "Fixed-limit Leduc", "exploitability"),
        ("mini", "Mini no-limit Leduc", "exploitability"),
        ("extended", "Extended Leduc", "exploitability"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    for ax, (panel, title, metric) in zip(axes, panels):
        panel_rows = sorted(
            [r for r in rows if r["panel"] == panel],
            key=lambda r: (r["order"], r["label"], r["seed"]),
        )
        labels = []
        values_by_label = []
        info_by_label = []
        for label in dict.fromkeys(r["label"] for r in panel_rows):
            values = [r[metric] for r in panel_rows
                      if r["label"] == label and r[metric] is not None]
            infos = [r["info_sets"] for r in panel_rows
                     if r["label"] == label]
            if not values:
                continue
            labels.append(label)
            values_by_label.append(values)
            info_by_label.append(round(mean(infos)))

        xs = list(range(len(labels)))
        for x, values in zip(xs, values_by_label):
            jittered = [x + (i - (len(values) - 1) / 2) * 0.08
                        for i in range(len(values))]
            ax.scatter(jittered, values, color="#1f77b4", alpha=0.75,
                       s=42, zorder=3)
            m = mean(values)
            sd = stdev(values) if len(values) > 1 else 0.0
            ax.errorbar([x], [m], yerr=[[sd], [sd]], fmt="o",
                        color="#d62728", capsize=4, markersize=5,
                        zorder=4)
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_ylabel("Final exploitability after 180s (log scale)")
        ax.set_xticks(xs)
        tick_labels = [
            f"{label}\n({info:,} infos)" for label, info in zip(labels, info_by_label)
        ]
        ax.set_xticklabels(tick_labels, rotation=35, ha="right")
        ax.grid(True, axis="y", which="both", linestyle="--", alpha=0.3)
        flat = [v for values in values_by_label for v in values if v > 0]
        ymin = min(flat, default=1e-6)
        ymax = max(flat, default=1.0)
        ax.set_ylim(ymin * 0.45, ymax * 1.8)
    fig.suptitle("CFR+ abstraction comparison: 3 seeds x 3 minutes each")
    fig.tight_layout()
    fig.savefig(PLOT_PATH, dpi=150, bbox_inches="tight")
    print(f"Plot saved to {PLOT_PATH}")
    plt.close(fig)

    for panel, title, metric in panels:
        _plot_single_panel(plt, rows, panel, title, metric)


def _plot_single_panel(plt, rows: list[dict], panel: str, title: str,
                       metric: str):
    panel_rows = sorted(
        [r for r in rows if r["panel"] == panel],
        key=lambda r: (r["order"], r["label"], r["seed"]),
    )
    labels = []
    values_by_label = []
    info_by_label = []
    for label in dict.fromkeys(r["label"] for r in panel_rows):
        values = [r[metric] for r in panel_rows
                  if r["label"] == label and r[metric] is not None]
        infos = [r["info_sets"] for r in panel_rows if r["label"] == label]
        if not values:
            continue
        labels.append(label)
        values_by_label.append(values)
        info_by_label.append(round(mean(infos)))

    if not labels:
        return

    width = 12 if len(labels) <= 4 else 16
    fig, ax = plt.subplots(figsize=(width, 7))
    colors = plt.get_cmap("tab20").colors
    xs = list(range(len(labels)))
    handles = []
    legend_labels = []

    for idx, (x, label, values, infos) in enumerate(
            zip(xs, labels, values_by_label, info_by_label)):
        color = colors[idx % len(colors)]
        jittered = [x + (i - (len(values) - 1) / 2) * 0.09
                    for i in range(len(values))]
        handle = ax.scatter(jittered, values, color=color, alpha=0.75,
                            s=56, zorder=3)
        m = mean(values)
        sd = stdev(values) if len(values) > 1 else 0.0
        ax.errorbar([x], [m], yerr=[[sd], [sd]], fmt="o",
                    color="black", capsize=5, markersize=5,
                    zorder=4)
        handles.append(handle)
        legend_labels.append(
            f"{label} ({infos:,} infos): {m:.3g} +/- {sd:.2g}")

    ax.set_yscale("log")
    ax.set_title(f"{title} - CFR+ after 180s")
    ax.set_ylabel("Final exploitability (log scale)")
    ax.set_xticks(xs)
    ax.set_xticklabels(
        [f"{label}\n({info:,} infos)"
         for label, info in zip(labels, info_by_label)],
        rotation=25 if len(labels) <= 4 else 35,
        ha="right",
    )
    ax.grid(True, axis="y", which="both", linestyle="--", alpha=0.3)
    flat = [v for values in values_by_label for v in values if v > 0]
    ax.set_ylim(min(flat) * 0.45, max(flat) * 1.8)
    ax.legend(handles, legend_labels, loc="center left",
              bbox_to_anchor=(1.01, 0.5), framealpha=0.95,
              title="Mean +/- SD exploitability")

    fig.tight_layout()
    path = PANEL_PLOT_PATHS[panel]
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Panel plot saved to {path}")
    plt.close(fig)


def _summarize(rows: list[dict]):
    print("\nSummary by config")
    print("-" * 92)
    print(f"{'Panel':<10} {'Config':<26} {'n':>2} {'gap mean':>12} "
          f"{'gap sd':>12} {'exploit mean':>14} {'iters mean':>11}")
    for panel in ("fixed", "mini", "extended"):
        labels = sorted(
            {r["label"] for r in rows if r["panel"] == panel},
            key=lambda label: min(r["order"] for r in rows
                                  if r["panel"] == panel
                                  and r["label"] == label),
        )
        for label in labels:
            subset = [r for r in rows
                      if r["panel"] == panel and r["label"] == label]
            gaps = [r["gap_vs_full"] for r in subset
                    if r["gap_vs_full"] is not None]
            exploits = [r["exploitability"] for r in subset]
            iters = [r["iterations"] for r in subset]
            gap_mean = mean(gaps) if gaps else math.nan
            gap_sd = stdev(gaps) if len(gaps) > 1 else 0.0
            print(f"{panel:<10} {label:<26} {len(subset):>2} "
                  f"{gap_mean:>12.6f} {gap_sd:>12.6f} "
                  f"{mean(exploits):>14.6f} {mean(iters):>11.1f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=180.0)
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--panels", nargs="+",
                        default=["fixed", "mini", "extended"])
    parser.add_argument("--progress-every", type=float, default=30.0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    configs = [c for c in _all_configs() if c.panel in args.panels]
    rows = [] if args.force else _load_results()
    completed = {
        (r["config"], r["seed"], float(r["budget_sec"])) for r in rows
    }

    print(f"Running {len(configs)} configs x {len(args.seeds)} seeds "
          f"x {args.seconds:.0f}s")
    print(f"Results: {RESULTS_PATH}")
    for config in configs:
        for seed in args.seeds:
            key = (config.name, seed, float(args.seconds))
            if key in completed:
                print(f"  skip {config.label:<26} seed={seed}")
                continue
            print(f"\n  start {config.panel}/{config.label} seed={seed}",
                  flush=True)
            row = _train_one(config, seed, args.seconds,
                             args.progress_every)
            rows.append(row)
            rows = _with_gaps(rows)
            _save_results(rows)
            print(
                f"  done  {config.label:<26} seed={seed} "
                f"iters={row['iterations']} exploit={row['exploitability']:.6f} "
                f"eval={row['eval_time_sec']:.1f}s",
                flush=True,
            )

    rows = _with_gaps(rows)
    _save_results(rows)
    _plot(rows)
    _summarize(rows)


if __name__ == "__main__":
    raise SystemExit(main())
