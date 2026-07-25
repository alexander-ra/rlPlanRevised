"""
comparison_table.py  [SUP]  -- raw L436-446.

The headline deliverable: ONE table putting every method on the same exact Kuhn ruler --

    Nash-CFR | Decision Transformer | ARDT | Behavioral Cloning | LLM x {plain, CoT, game-theory}

with columns: exploitability (chips + mbb/h), bluff freq (Jack), value-bet freq (King), and --
for the LLM rows -- illegal-move rate and opponent-adaptation delta.

The CFR and LLM (offline-stub) rows run with NO torch and NO GPU. The DT/BC/ARDT rows require
torch and are skipped with a clear message if it is absent. Results are written to
`results/comparison_<profile>.json` when executed.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here; every number produced by
a real run is a measurement to record in EXECUTION_NOTES.md (next session).
"""

from __future__ import annotations

import json
import os
import time

import deps  # noqa: F401
from deps import torch_available
from engines import make_game

from trajectory_dataset import make_cfr_policy
from strategy_extraction import (extract_policy_strategy, extract_dt_strategy,
                                 extract_bc_strategy, extract_ardt_strategy)
from evaluation import strategy_metrics, illegal_move_rate, opponent_adaptation
from llm_agent import make_client, KuhnPokerLLMAgent, llm_policy


def _row(name: str, node_map: dict) -> dict:
    row = {"agent": name}
    row.update(strategy_metrics(node_map))
    row["illegal_rate"] = None
    row["adaptation_delta"] = None
    return row


def build_comparison(cfg: dict, device: str = "cpu", llm_spec: dict | None = None) -> list:
    rows = []
    game = make_game(cfg["game"])

    # --- Nash (near-optimal CFR) -----------------------------------------------------
    nash_policy, _ = make_cfr_policy(game, cfg["cfr_iters"], cfg["seed"])
    rows.append(_row("Nash-CFR", extract_policy_strategy(nash_policy, game)))

    # --- LLM x prompt styles ---------------------------------------------------------
    for style in cfg["llm_styles"]:
        client = make_client(llm_spec)
        agent = KuhnPokerLLMAgent(client, prompt_style=style,
                                  temperature=cfg["llm_temperature"])
        pol = llm_policy(agent, samples=cfg["llm_samples"])
        node_map = extract_policy_strategy(pol, game)
        row = _row(f"LLM-{style}", node_map)
        row["backend"] = client.name
        row["illegal_rate"] = illegal_move_rate(agent)
        row["adaptation_delta"] = opponent_adaptation(agent, cfg["llm_samples"])["adaptation_delta"]
        rows.append(row)

    # --- DT / BC / ARDT (torch) ------------------------------------------------------
    if torch_available():
        from train_dt import build_and_train
        from ardt import build_and_train_ardt
        from behavioral_cloning import BehavioralCloning, BCConfig, train_bc

        dt_model, dt_ds = build_and_train(cfg, device=device)
        dt_nm = extract_dt_strategy(dt_model, dt_ds.encoder, dt_ds.game,
                                    target_return=cfg["dt_target_return"], device=device)
        rows.append(_row("DT", dt_nm))

        bc = BehavioralCloning(BCConfig(dt_ds.state_dim, dt_ds.num_actions, cfg["hidden_size"]))
        train_bc(bc, dt_ds.to_tensors(), epochs=cfg["bc_epochs"], batch_size=cfg["batch_size"],
                 lr=cfg["lr"], device=device)
        rows.append(_row("BC", extract_bc_strategy(bc, dt_ds.encoder, dt_ds.game, device=device)))

        ardt, ardt_ds = build_and_train_ardt(cfg, device=device)
        rows.append(_row("ARDT", extract_ardt_strategy(ardt, ardt_ds.encoder, ardt_ds.game,
                                                        device=device)))
    else:
        print("(PyTorch unavailable -> DT, BC and ARDT rows are skipped. CFR + LLM rows stand.)")

    return rows


def print_table(rows: list) -> None:
    header = f"{'agent':<14}{'expl(chips)':>12}{'expl(mbb/h)':>12}{'bluffJ':>8}{'valueK':>8}" \
             f"{'illegal':>9}{'adapt':>8}"
    print(header)
    print("-" * len(header))
    for r in rows:
        illegal = "" if r["illegal_rate"] is None else f"{r['illegal_rate']:.0%}"
        adapt = "" if r["adaptation_delta"] is None else f"{r['adaptation_delta']:+.2f}"
        print(f"{r['agent']:<14}{r['exploitability_chips']:>12.4f}"
              f"{r['exploitability_mbb_per_hand']:>12.1f}{r['bluff_freq_J']:>8.2f}"
              f"{r['value_bet_freq_K']:>8.2f}{illegal:>9}{adapt:>8}")


def save_results(rows: list, cfg: dict, path: str | None = None) -> str:
    if path is None:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"comparison_{cfg['name']}.json")
    payload = {"profile": cfg["name"], "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "config": {k: cfg[k] for k in cfg if k != "llm_preset"}, "rows": rows}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path


def main():
    from config import active_config

    cfg = active_config()
    device = "cpu"
    if torch_available():
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"comparison_table: profile={cfg['name']} device={device} "
          f"llm_backend={(cfg.get('llm_preset') or {}).get('backend', 'stub')}")
    rows = build_comparison(cfg, device=device, llm_spec=cfg.get("llm_preset"))
    print()
    print_table(rows)
    path = save_results(rows, cfg)
    print(f"\nsaved -> {path}")
    print("(All numbers are from THIS run; record them in EXECUTION_NOTES.md next session.)")


if __name__ == "__main__":
    main()
