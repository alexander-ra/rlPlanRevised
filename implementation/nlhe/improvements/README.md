# improvements/ — staged proposals (NOT wired in)

Each `improvements/<Letter>/` folder holds a proposal from
`../improvementProposals.md`. **Nothing here is imported by the live trainer.**
You apply them yourself: either copy a provided module into `src/`, or apply the
before/after snippets shown in each folder's `README.md` to the real files.

Guiding goal (see improvementProposals.md): the tabular run is a **self-play
seed**, so "sensible everywhere + low variance" matters more than depth. Order:

1. **A** (defaults) — kill the random-postflop floor. Low risk. ★ do first
2. **E** (eval/measure) — make gains visible. Low risk.
3. **B** (flop-start) — convert 400h into real postflop skill. Med risk.
4. **C** (CFR+/DCFR) — cheap convergence speedup. Low risk.
5. **D** (abstraction / scale) — only if coverage stays the bottleneck.

| Folder | Proposals | Artifact type | Touches live code? |
|---|---|---|---|
| A | A1 heuristic default, A2 nearest-bucket, A3 warm-start | new module + wiring diffs | eval + distill (output side) |
| B | B1 flop-start, B3 soft-freeze mix (B2/B4/B5 sketched) | new module + config diff | mccfr + daemon loop |
| C | C3 CFR+/DCFR (C1/C2/C4 sketched) | diff | mccfr.traverse |
| D | D2 action abstraction, D3/D4 (design) | config example + design | abstraction (rebuild) |
| E | E1 measure_reach (exists), E3 readable eval | config diff | config only |

Risk labels are dev/correctness risk, not upside.
