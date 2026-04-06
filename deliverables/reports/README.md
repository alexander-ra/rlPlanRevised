# Reports & Summaries Guidelines

This directory contains the deliverables for each learning step.

## Reports (`stepXX/report_{lang}.md`)

Minimal text only — just what was developed, key targets/results, and relevant images.
Think of it as an executive summary of the implementation work.

## Summaries (`stepXX/summary/summary{Lang}.md`)

Detailed theoretical narrative and explanations for each step.

### Section Numbering Convention

**Do NOT put manual section numbers (e.g. `## 2.1 Title`) in the markdown headings.**

The PDF build script (`scripts/build_reports.py`) automatically generates section numbers
using pandoc's `--number-sections` with `--number-offset`. The offset is derived from
the step number so that:

| Step    | Sections in PDF |
|---------|-----------------|
| step01  | 1.1, 1.2, 1.3… |
| step02  | 2.1, 2.2, 2.3… |
| step03  | 3.1, 3.2, 3.3… |
| stepNN  | N.1, N.2, N.3… |

So in the markdown source, just write plain headings:

```markdown
## From Single-Agent RL to Multi-Agent Strategic Interaction
## Extensive-Form Games and Information Sets
```

The build script handles the rest. This keeps the markdown clean and avoids double-numbering.

### Images

Images should be placed in `stepXX/figures/` and referenced from summaries with
relative paths like `../figures/image_name.png`. The build script constrains images
to fit within page width automatically (via `scripts/pandoc_img_fix.tex`).
