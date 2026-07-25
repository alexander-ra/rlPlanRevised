"""
validate.py  [CORE + INF]  -- the PASS/FAIL harness for Step 12's five validation targets
(raw L458-463). Run it in the verification session; here it is written but NOT executed.

The five targets (verbatim intent from the raw step):
  1. DT: conditioning on HIGH return-to-go yields LOWER exploitability than LOW.
  2. Stochasticity/luck: the DT's action distribution VARIES BY CARD (it keys partly on the deal,
     not only the situation) -- the Paster luck-vs-skill signature.
  3. ARDT < DT: on MIXED-opponent data, ARDT is LESS exploitable vs Nash than a standard DT
     trained on the same data.
  4. ARDT near Nash: ARDT is within ~50 mbb/h of Nash (== <= 0.05 chips; see the units note).
  5. LLM honesty: the LLM is HONESTLY MORE exploitable than Nash, and we capture WHERE it fails
     (bluff frequency off, illegal moves).

Torch-dependent checks (1-4) report SKIP if PyTorch is unavailable; check 5 (CFR + LLM stub)
always runs. Target #4 is aspirational -- it may FAIL at SMOKE sizes; that is expected and is
itself information (record it, scale up, re-check).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here; all thresholds are TARGETS.
"""

from __future__ import annotations

from dataclasses import dataclass

import deps  # noqa: F401
from deps import torch_available
from engines import make_game

from trajectory_dataset import PokerTrajectoryDataset, make_cfr_policy
from strategy_extraction import (extract_policy_strategy, extract_dt_strategy,
                                 extract_ardt_strategy, dt_root_bet_prob_by_card)
from evaluation import exploitability_chips, chips_to_mbb_per_hand, bluff_freq, illegal_move_rate
from llm_agent import make_client, KuhnPokerLLMAgent, llm_policy
from config import (active_config, TARGET_RETURNS, ARDT_NASH_TOLERANCE_CHIPS)

# Card-dependence threshold for target #2: max-min root P(bet) across the three cards.
_CARD_SPREAD_THRESHOLD = 0.10


@dataclass
class CheckResult:
    idx: int
    name: str
    status: str          # PASS / FAIL / SKIP
    detail: str


def _fmt(chips: float) -> str:
    return f"{chips:.4f} chips ({chips_to_mbb_per_hand(chips):.1f} mbb/h)"


def run_checks(cfg: dict, device: str = "cpu") -> list:
    results = []
    game = make_game(cfg["game"])

    # Near-Nash reference (always available; torch-free).
    nash_policy, _ = make_cfr_policy(game, cfg["cfr_iters"], cfg["seed"])
    nash_expl = exploitability_chips(extract_policy_strategy(nash_policy, game))

    high_R, low_R = max(TARGET_RETURNS), min(TARGET_RETURNS)

    if torch_available():
        from decision_transformer import DecisionTransformer, DecisionTransformerConfig
        from train_dt import build_and_train, train_decision_transformer
        from ardt import build_and_train_ardt

        # DT on self-play data (targets 1 & 2).
        dt_model, dt_ds = build_and_train(cfg, device=device)
        expl_high = exploitability_chips(
            extract_dt_strategy(dt_model, dt_ds.encoder, game, high_R, device))
        expl_low = exploitability_chips(
            extract_dt_strategy(dt_model, dt_ds.encoder, game, low_R, device))
        results.append(CheckResult(
            1, "DT high-RTG < low-RTG exploitability",
            "PASS" if expl_high < expl_low else "FAIL",
            f"high({high_R:+.0f})={_fmt(expl_high)} vs low({low_R:+.0f})={_fmt(expl_low)}"))

        bet_by_card = dt_root_bet_prob_by_card(dt_model, dt_ds.encoder, game, high_R, device)
        spread = max(bet_by_card.values()) - min(bet_by_card.values())
        results.append(CheckResult(
            2, "DT action varies by card (luck)",
            "PASS" if spread >= _CARD_SPREAD_THRESHOLD else "FAIL",
            f"root P(bet) by card J/Q/K = "
            f"{bet_by_card[1]:.2f}/{bet_by_card[2]:.2f}/{bet_by_card[3]:.2f}; spread={spread:.2f}"))

        # ARDT + a standard DT on the SAME mixed-opponent data (targets 3 & 4).
        ardt, ds_mixed = build_and_train_ardt(cfg, device=device)
        ardt_expl = exploitability_chips(
            extract_ardt_strategy(ardt, ds_mixed.encoder, game, device))

        dt_mixed = DecisionTransformer(DecisionTransformerConfig(
            state_dim=ds_mixed.state_dim, act_dim=ds_mixed.num_actions,
            hidden_size=cfg["hidden_size"], n_layer=cfg["n_layer"], n_head=cfg["n_head"],
            max_ep_len=cfg["max_ep_len"]))
        train_decision_transformer(dt_mixed, ds_mixed.to_tensors(), epochs=cfg["dt_epochs"],
                                   batch_size=cfg["batch_size"], lr=cfg["lr"], device=device)
        dt_mixed_expl = exploitability_chips(
            extract_dt_strategy(dt_mixed, ds_mixed.encoder, game, high_R, device))
        results.append(CheckResult(
            3, "ARDT < standard DT (mixed data, vs Nash)",
            "PASS" if ardt_expl < dt_mixed_expl else "FAIL",
            f"ARDT={_fmt(ardt_expl)} vs DT={_fmt(dt_mixed_expl)}"))

        gap_to_nash = abs(ardt_expl - nash_expl)
        results.append(CheckResult(
            4, "ARDT within ~50 mbb/h of Nash",
            "PASS" if ardt_expl <= ARDT_NASH_TOLERANCE_CHIPS else "FAIL",
            f"ARDT={_fmt(ardt_expl)}, Nash={_fmt(nash_expl)}, tol={ARDT_NASH_TOLERANCE_CHIPS} "
            f"chips (aspirational; may need SCALE). gap={gap_to_nash:.4f} chips"))
    else:
        for i, name in ((1, "DT high-RTG < low-RTG exploitability"),
                        (2, "DT action varies by card (luck)"),
                        (3, "ARDT < standard DT (mixed data, vs Nash)"),
                        (4, "ARDT within ~50 mbb/h of Nash")):
            results.append(CheckResult(i, name, "SKIP", "PyTorch unavailable"))

    # Target 5: LLM honestly more exploitable than Nash (always runs, offline stub by default).
    client = make_client(cfg.get("llm_preset"))
    agent = KuhnPokerLLMAgent(client, prompt_style="cot", temperature=cfg["llm_temperature"])
    llm_nm = extract_policy_strategy(llm_policy(agent, samples=cfg["llm_samples"]), game)
    llm_expl = exploitability_chips(llm_nm)
    results.append(CheckResult(
        5, "LLM honestly more exploitable than Nash",
        "PASS" if llm_expl > nash_expl else "FAIL",
        f"LLM({client.name})={_fmt(llm_expl)} > Nash={_fmt(nash_expl)}; "
        f"bluff(J)={bluff_freq(llm_nm):.2f}, illegal={illegal_move_rate(agent):.0%}"))
    return results


def main():
    cfg = active_config()
    device = "cpu"
    if torch_available():
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"validate: profile={cfg['name']} device={device} "
          f"(targets are raw L458-463; numbers are predictions)")
    print("=" * 78)
    results = run_checks(cfg, device=device)
    for r in results:
        print(f"[{r.status:4}] {r.idx}. {r.name}")
        print(f"        {r.detail}")
    n_pass = sum(1 for r in results if r.status == "PASS")
    n_fail = sum(1 for r in results if r.status == "FAIL")
    n_skip = sum(1 for r in results if r.status == "SKIP")
    print("=" * 78)
    print(f"summary: {n_pass} PASS / {n_fail} FAIL / {n_skip} SKIP  (of {len(results)})")


if __name__ == "__main__":
    main()
