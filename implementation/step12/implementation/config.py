"""
config.py  [INF]  -- run profiles, the LLM model roster, and runtime notes for Step 12.

TWO PROFILES
------------
  SMOKE : tiny, CPU-friendly, LLM = offline stub. For a fast end-to-end shakedown that the whole
          pipeline wires together (data -> DT/ARDT/BC -> exploitability -> table) with no GPU.
  SCALE : full sizes for the RTX 5090; LLM points at a real local model (default gpt-oss 20B).

Select with the env var STEP12_PROFILE=SMOKE|SCALE (default SMOKE), e.g. on PowerShell:
    $env:STEP12_PROFILE = "SCALE"; python comparison_table.py

LLM ROSTER (confirmed with the user)
------------------------------------
  default     : gpt-oss 20B          (strong open-weight reasoner; comfortable on 24-32GB VRAM)
  alternative : Qwen2.5-7B-Instruct  (dense, robust, fast; the "base" of the pair below)
  alternative : OpenThinker3-7B      (a reasoning-SFT of the SAME Qwen2.5-7B base -> a clean
                                      base-vs-reasoning-tuned comparison)
Nemotron 3 Nano is deferred unless results are compelling. The client is model-agnostic: every
preset below is just (base_url, model) for an OpenAI-compatible server, so swapping models is a
one-line change. All numbers these produce are PREDICTIONS until the run session.
"""

from __future__ import annotations

import os

# Target returns to sweep for the DT return-conditioning experiment. Kuhn hand payoffs are in
# {-2,-1,+1,+2}; +3 is IMPOSSIBLE (no hand ever returned it) -> the Paster OOD-extrapolation probe.
TARGET_RETURNS = [-2.0, -1.0, 1.0, 2.0]
IMPOSSIBLE_RETURN = 3.0

# "Within 50 mbb/h of Nash" (raw L462) with a 1-chip big blind == exploitability <= 0.05 chips.
ARDT_NASH_TOLERANCE_CHIPS = 0.05


# --- LLM presets (dicts consumed by llm_agent.make_client) ---------------------------
LLM_STUB = {"backend": "stub"}

# OpenAI-compatible local servers. base_url defaults assume LM Studio (port 1234); for Ollama use
# "http://localhost:11434/v1". api_key is unused by local servers (kept for OpenRouter/OpenAI).
# MODEL IDS VERIFIED AGAINST A RUNNING SERVER (2026-07-25, LM Studio 0.4.20).
# `GET /v1/models` reports the PUBLISHER-QUALIFIED id (e.g. "openai/gpt-oss-20b"), not the bare
# name these presets originally guessed ("gpt-oss-20b"). A wrong id fails at request time, so
# `llm_agent.make_client` now resolves ids against /v1/models and reports what IS served.
#
# max_tokens is a per-preset knob (added in the run session): the client default of 256 is fine
# for gpt-oss -- it returns its chain-of-thought in a SEPARATE `reasoning` field, so `content`
# holds just the answer (~99 completion tokens measured) -- but a model that emits <think> INLINE
# needs far more headroom or it gets truncated before the "Action:" line and is scored illegal.
LLM_GPT_OSS_20B = {
    "backend": "openai", "base_url": "http://localhost:1234/v1",
    "model": "openai/gpt-oss-20b", "api_key": None, "timeout": 180.0, "max_tokens": 512,
}
LLM_QWEN25_7B = {
    "backend": "openai", "base_url": "http://localhost:1234/v1",
    "model": "qwen2.5-7b-instruct", "api_key": None, "timeout": 180.0, "max_tokens": 512,
}
LLM_OPENTHINKER3_7B = {
    "backend": "openai", "base_url": "http://localhost:1234/v1",
    "model": "openthinker3-7b", "api_key": None, "timeout": 600.0,  # long CoT -> higher timeout
    # MEASURED 2026-07-25: this model needs ~6,500 completion tokens to close its <think> block on
    # a single Kuhn decision (gpt-oss needs 99). At max_tokens=4096 it NEVER closed </think> on any
    # probe -- 18k chars of unfinished monologue, no action committed. 16000 gives headroom.
    # NOTE: it must also be LOADED with a big context or the request cannot fit:
    #     lms load openthinker3-7b --context-length 32768
    # (the 8192 default leaves no room for a 16k completion).
    "max_tokens": 16000,
}

LLM_ROSTER = {
    "stub": LLM_STUB,
    "gpt_oss_20b": LLM_GPT_OSS_20B,
    "qwen2.5_7b": LLM_QWEN25_7B,
    "openthinker3_7b": LLM_OPENTHINKER3_7B,
}


# --- profiles ------------------------------------------------------------------------
SMOKE = {
    "name": "SMOKE",
    "game": "kuhn",
    "seed": 0,
    # data
    "n_trajectories": 5000,
    "cfr_iters": 5000,
    "exploit_frac": 0.5,
    # DT / ARDT / BC model
    "hidden_size": 32,
    "n_layer": 2,
    "n_head": 4,
    "max_ep_len": 8,
    "dt_epochs": 15,
    "estimator_epochs": 20,
    "bc_epochs": 15,
    "batch_size": 128,
    "lr": 1e-3,
    "expectile_tau": 0.1,
    "dt_target_return": 2.0,
    # LLM
    "llm_styles": ["plain", "cot", "gametheory"],
    "llm_temperature": 0.0,   # deterministic for the stub
    "llm_samples": 4,
    "llm_preset": LLM_STUB,
}

SCALE = {
    "name": "SCALE",
    "game": "kuhn",          # Leduc is an optional SCALE extension (see README)
    "seed": 0,
    "n_trajectories": 50000,
    "cfr_iters": 30000,
    "exploit_frac": 0.5,
    "hidden_size": 64,
    "n_layer": 3,
    "n_head": 4,
    "max_ep_len": 16,
    "dt_epochs": 60,
    "estimator_epochs": 80,
    "bc_epochs": 60,
    "batch_size": 256,
    "lr": 1e-3,
    "expectile_tau": 0.1,
    "dt_target_return": 2.0,
    "llm_styles": ["plain", "cot", "gametheory"],
    "llm_temperature": 0.7,
    "llm_samples": 16,
    "llm_preset": LLM_GPT_OSS_20B,
}

PROFILES = {"SMOKE": SMOKE, "SCALE": SCALE}


def active_config() -> dict:
    """Return the profile named by STEP12_PROFILE (default SMOKE). Also honors
    STEP12_LLM=<roster key> to override the LLM preset without editing this file."""
    name = os.environ.get("STEP12_PROFILE", "SMOKE").upper()
    if name not in PROFILES:
        raise ValueError(f"Unknown STEP12_PROFILE={name!r}; choose from {sorted(PROFILES)}")
    cfg = dict(PROFILES[name])  # shallow copy so overrides don't mutate the module constant
    llm_key = os.environ.get("STEP12_LLM")
    if llm_key:
        if llm_key not in LLM_ROSTER:
            raise ValueError(f"Unknown STEP12_LLM={llm_key!r}; choose from {sorted(LLM_ROSTER)}")
        cfg["llm_preset"] = LLM_ROSTER[llm_key]
    # RUN-SESSION ADDITION: STEP12_LLM_SAMPLES overrides how many times each info set is queried
    # to estimate the LLM's mixed strategy. This matters more than it looks: at the SMOKE default
    # of 4, every per-info-set probability is 4 Bernoulli draws (SE up to 0.25), and real models
    # are NOT bit-deterministic even at temperature 0 (MoE routing under batching). Two identical
    # gpt-oss runs measured bluff(J) = 0.75 and 0.25 for the same prompt style. Raise this before
    # quoting any LLM frequency as a result.
    samples = os.environ.get("STEP12_LLM_SAMPLES")
    if samples:
        cfg["llm_samples"] = int(samples)
    # STEP12_LLM_TEMP overrides sampling temperature. IMPORTANT for real models: SMOKE defaults to
    # 0.0 because that makes the offline STUB reproducible -- but at temperature 0 a real LLM plays
    # a PURE strategy, so all N samples at an info set return the same action and the measured
    # "frequency" degenerates to exactly 0.0 or 1.0. Measured on gpt-oss-20b: bluff(J) came out
    # 0.75, 0.25 and 1.00 on three runs of the same config, because exploitability then depends on
    # WHICH pure strategy the model happened to land on. To measure a mixed strategy you need
    # temperature > 0 (SCALE uses 0.7).
    temp = os.environ.get("STEP12_LLM_TEMP")
    if temp:
        cfg["llm_temperature"] = float(temp)
    # STEP12_LLM_STYLES restricts which prompt styles are measured, e.g. "cot" or "plain,cot".
    # Needed because cost per style is wildly model-dependent: a full 3-style x 24-sample pass is
    # ~16 min on gpt-oss but ~9 HOURS on OpenThinker3-7B (~6,500 completion tokens and ~38 s per
    # single decision). Restricting to the CoT row keeps the base-vs-reasoning-tuned comparison
    # against Qwen2.5-7B affordable; unmeasured styles are simply absent from the results file
    # rather than silently defaulted.
    styles = os.environ.get("STEP12_LLM_STYLES")
    if styles:
        cfg["llm_styles"] = [s.strip() for s in styles.split(",") if s.strip()]
    return cfg


RUNTIME_NOTES = """
RUNTIME NOTES (verify in the run session)
=========================================
GPU / torch (RTX 5090, Blackwell sm_120):
  - The DT/ARDT here are TINY; SMOKE runs fine on CPU. Only SCALE benefits from CUDA.
  - Blackwell needs a recent CUDA (12.8+) build of PyTorch. If `torch.cuda.is_available()` is
    False on the 5090, install a cu128 (or nightly cu128) wheel. The code auto-falls back to CPU.

Serving a local LLM (OpenAI-compatible; pick ONE):
  - LM Studio: load the model, start its local server; base_url = http://localhost:1234/v1,
    model = the id LM Studio shows. (Default in the presets above.)
  - Ollama:    `ollama pull <model>` then `ollama serve`; base_url = http://localhost:11434/v1,
    model = the pulled tag (e.g. "qwen2.5:7b-instruct").
  - vLLM / OpenRouter / OpenAI: same shape; set base_url, model, and api_key.

Switching models without editing code:
    $env:STEP12_PROFILE = "SCALE"; $env:STEP12_LLM = "qwen2.5_7b"; python comparison_table.py
    $env:STEP12_LLM = "openthinker3_7b"; python comparison_table.py

Roster fit on a 24-32GB card:
  - gpt-oss 20B        : default; run a quantized build if VRAM is tight.
  - Qwen2.5-7B-Instruct: comfortable at bf16/fp16; fast; good robustness baseline.
  - OpenThinker3-7B    : same footprint as Qwen2.5-7B but ALWAYS emits long CoT -> higher latency
                         and more text to parse; budget a larger timeout (already set) and expect
                         a lower throughput than Qwen2.5.
"""


def _selftest():
    print("config self-test")
    print("-" * 50)
    for name in ("SMOKE", "SCALE"):
        os.environ["STEP12_PROFILE"] = name
        cfg = active_config()
        print(f"{name}: game={cfg['game']} n_traj={cfg['n_trajectories']} "
              f"dt_epochs={cfg['dt_epochs']} llm={cfg['llm_preset']['backend']}")
    os.environ["STEP12_PROFILE"] = "SMOKE"
    os.environ["STEP12_LLM"] = "qwen2.5_7b"
    print("override STEP12_LLM=qwen2.5_7b ->", active_config()["llm_preset"]["model"])
    del os.environ["STEP12_LLM"]
    print(f"TARGET_RETURNS={TARGET_RETURNS} IMPOSSIBLE={IMPOSSIBLE_RETURN} "
          f"ARDT_tol={ARDT_NASH_TOLERANCE_CHIPS} chips")


if __name__ == "__main__":
    _selftest()
