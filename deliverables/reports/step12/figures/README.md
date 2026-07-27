# Step 12 — figures/

The exact experiment PNGs the Step 12 deliverables cite. Every figure must trace to a real artifact
under `implementation/step12/implementation/results/`; **nothing here is fabricated**. Figures copied
from the implementation are prefixed `impl_`.

**Status: all 12 figures are present and were produced by real runs.** Unlike earlier steps there
are no conceptual box-and-arrow diagrams in this step — every figure is measured data.

> **Why that emphasis.** `implementation/plotting.py` originally shipped with **only** a `_selftest`
> that plotted *hard-coded* numbers into `results/`, and it was the sole PNG-producing path in the
> step — so following the runbook literally committed a fabricated figure. It was replaced with a
> `main()` that renders exclusively from `results/*.json`. Regenerating is therefore safe and
> idempotent.

---

## How to regenerate and assemble them

```bash
# 1. regenerate every figure from the committed results JSON (no model calls, no training)
cd implementation/step12/implementation
python plotting.py                      # -> results/*.png  (12 figures)
```

```powershell
# 2. copy into the deliverables folder with the impl_ prefix (from the repo root)
$src = "implementation/step12/implementation/results"
$dst = "deliverables/reports/step12/figures"
foreach ($f in "return_conditioning","bet_prob_by_card","tau_sweep","leak_decomposition",
                "stated_vs_executed","exploitation_frontier","leduc_illegal_taxonomy",
                "leduc_return_conditioning","exploitability_bars_stub",
                "exploitability_bars_qwen2.5-7b-instruct",
                "exploitability_bars_openai_gpt-oss-20b",
                "exploitability_bars_openthinker3-7b") {
  Copy-Item "$src/$f.png" "$dst/impl_$f.png"
}
# the summary cites its figures flat, so copy the ones it uses next to summaryEn.md as well
```

```bash
# 3. build the PDFs (toolchain: pandoc + xelatex; tectonic is not installed on this machine)
python scripts/build_reports.py --step step12 --lang en
# -> deliverables/reports/step12/step12_report_en.pdf
# -> deliverables/summaries/step12_en.pdf
```

---

## Figure manifest (what each shows + its source artifact)

### Core build — Kuhn

| File | Cited in | Source artifact | Status |
|---|---|---|---|
| `impl_return_conditioning.png` | report | `results/dt_experiments_SMOKE.json` | present |
| `impl_bet_prob_by_card.png` | report | `results/dt_experiments_SMOKE.json` | present |
| `impl_tau_sweep.png` | report, summary | `results/tau_sweep_SMOKE.json` | present |
| `impl_exploitability_bars_stub.png` | report | `results/comparison_SMOKE_stub.json` | present |
| `impl_exploitability_bars_qwen2.5-7b-instruct.png` | report | `results/comparison_SMOKE_qwen2.5-7b-instruct.json` | present |
| `impl_exploitability_bars_openai_gpt-oss-20b.png` | report | `results/comparison_SMOKE_openai_gpt-oss-20b.json` | present |
| `impl_exploitability_bars_openthinker3-7b.png` | report | `results/comparison_SMOKE_openthinker3-7b.json` | present |

### Follow-on experiments — Kuhn

| File | Cited in | Source artifact | Status |
|---|---|---|---|
| `impl_leak_decomposition.png` | report, summary | `results/decomposition_qwen2.5-7b-instruct_plain_logprob.json` | present |
| `impl_stated_vs_executed.png` | report, summary | `results/frequency_elicitation_{qwen2.5-7b-instruct, openai_gpt-oss-20b}.json` | present |
| `impl_exploitation_frontier.png` | report, summary | `results/exploitation_qwen2.5-7b-instruct.json` | present |

### Leduc

| File | Cited in | Source artifact | Status |
|---|---|---|---|
| `impl_leduc_return_conditioning.png` | report, summary | `results/leduc_stage0.json` | present |
| `impl_leduc_illegal_taxonomy.png` | report, summary | `results/leduc_illegal_taxonomy_qwen2.5-7b-instruct.json` | present |

---

## Not pictured (deliberately)

- **C10 head-to-head** (`results/head_to_head.json`) — a 4×4 matrix reads better as a table than a
  figure; it is tabulated in the report.
- **B5 opponent modelling** (`results/opponent_modeling_qwen2.5-7b-instruct.json`) — three cells,
  two of them underpowered (SE ±0.80 and ±0.53); plotting them would imply more precision than the
  data supports. Tabulated with error bars instead.
