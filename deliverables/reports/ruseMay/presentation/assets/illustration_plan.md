# Illustration Plan for HTML Slide Deck

Use these briefs to generate the replacement images for the placeholders in the deck. Keep the output as PNG files in this directory:

`deliverables/reports/ruseMay/presentation/assets/`

Global visual rules for all illustrations:
- Style: premium scientific vector-like digital illustration, clean academic conference deck, crisp edges, subtle depth, no cartoon style, no stock photo look.
- Background: transparent or very light `#F5F7FB`; avoid dark backgrounds.
- Palette:
  - Ink: `#17212C`
  - Soft ink: `#526173`
  - Blue: `#155F9F`
  - Blue soft: `#DBEAF8`
  - Red: `#C74735`
  - Red soft: `#FAE3DE`
  - Teal: `#148D80`
  - Teal soft: `#D8EEE9`
  - Amber: `#BB7D1C`
  - Rule gray: `#D7DDE7`
- Avoid embedded readable text unless the prompt explicitly requests it. The slide HTML will provide labels.
- Avoid decorative blobs, generic gradients, people, robots with faces, stock business imagery, and photorealism.
- Use thin geometric lines, structured panels, game-tree motifs, information-set boundaries, card/grid/auction/network symbols, and subtle shadows.

## illustration1_title_hero.png

Placeholder: `illustration1`

Slide: 1, title slide.

Target slot in slide: 720 x 610 CSS px, rendered at 1440 x 1220 px.

Recommended generation size/aspect ratio: `1440x1220`, aspect ratio `72:61`.

Purpose: First impression. It should signal multi-agent imperfect-information games, hidden state, and adaptive strategy learning.

Prompt:

```text
Create a premium scientific vector-style illustration for an academic presentation. Canvas 1440x1220 px, transparent or very light #F5F7FB background. Show an abstract multi-agent network connected to a faint extensive-form game tree: blue agent nodes (#155F9F), red unknown/opponent nodes (#C74735), teal evaluation/safety accents (#148D80), thin gray connector lines (#D7DDE7), and subtle information-set arcs. Include faint card-shape and hidden-state motifs, but no readable text. Style should be clean, precise, high-end conference slide, with soft shadows and crisp geometry. Avoid photorealism, people, cartoon faces, decorative blobs, and dark backgrounds.
```

## illustration2_systems_map.png

Placeholder: `illustration2`

Slide: 3, use cases.

Target slot in slide: 1712 x 610 CSS px, rendered at 3424 x 1220 px.

Recommended generation size/aspect ratio: `3424x1220`, aspect ratio `856:305`.

Purpose: Replace the use-case tiles with one coherent strategic-systems map.

Prompt:

```text
Create a wide premium scientific systems-map illustration for an academic presentation. Canvas 3424x1220 px, transparent or very light #F5F7FB background. Show five connected strategic domains as abstract zones around one central imperfect-information decision graph: financial markets with a price-line motif, cybersecurity with shield/network motif, social platforms with coordinated graph motif, security patrol with grid/path motif, and gaming platforms with cards/collusion motif. Use the exact palette #17212C, #526173, #155F9F, #DBEAF8, #C74735, #FAE3DE, #148D80, #D8EEE9, #BB7D1C, #D7DDE7. Keep it vector-like, crisp, scientific, and cohesive. No readable text. Avoid stock icons that look unrelated; the five areas must feel connected by a common game-theoretic abstraction.
```

## illustration3_testbed_abstraction.png

Placeholder: `illustration3`

Slide: 4, why study games.

Target slot in slide: 1712 x 460 CSS px, rendered at 3424 x 920 px.

Recommended generation size/aspect ratio: `3424x920`, aspect ratio `428:115`.

Purpose: Show that poker, auctions, pursuit-evasion, and coalition games are controlled validation environments sharing one abstraction.

Prompt:

```text
Create a wide scientific vector-style illustration for an academic presentation. Canvas 3424x920 px, transparent or very light #F5F7FB background. A central extensive-form game tree runs horizontally through the image. Four controlled testbed motifs emerge from it: hidden-card poker or Belot-like cards, auction bidding with hidden valuation, pursuit-evasion grid world with two dots and partial-observation fog, and coalition graph with alliance and betrayal edges. Use blue #155F9F for adaptation/inference, red #C74735 for risk/adversarial behavior, teal #148D80 for evaluation/safety, amber #BB7D1C for multi-player incentives, gray #D7DDE7 for structure. No readable text. Clean, precise, high-end academic diagram, not playful or cartoonish.
```

## illustration4_behavioral_adaptation.png

Placeholder: `illustration4`

Slide: 8, contribution 1.

Target slot in slide: approximately 935 x 600 CSS px, rendered at 1870 x 1200 px.

Recommended generation size/aspect ratio: `1870x1200`, aspect ratio `187:120`.

Purpose: Explain behavioral adaptation better than three process cards.

Prompt:

```text
Create a precise scientific diagram illustration for an academic presentation. Canvas 1870x1200 px, transparent or very light #F5F7FB background. Show a stream of observed opponent actions entering a belief-update module that splits into two inferred beliefs: hidden state and behavioural type. Then show a confidence gate that either routes to adaptive decision-making or falls back to equilibrium play. Use blue #155F9F for inference/adaptation, teal #148D80 for confidence/evaluation, red #C74735 for anomaly or adversarial signal, gray #D7DDE7 for connectors. Use abstract boxes, Bayesian belief particles, small card/grid symbols, and flow arrows. No readable text. Clean academic vector style, crisp geometry, subtle shadows.
```

## illustration5_safe_exploitation.png

Placeholder: `illustration5`

Slide: 9, contribution 2.

Target slot in slide: approximately 935 x 600 CSS px, rendered at 1870 x 1200 px.

Recommended generation size/aspect ratio: `1870x1200`, aspect ratio `187:120`.

Purpose: Show safe exploitation as a constrained drift from a reference policy.

Prompt:

```text
Create a scientific vector-style diagram for an academic presentation. Canvas 1870x1200 px, transparent or very light #F5F7FB background. Show a stable reference policy path in blue #155F9F surrounded by a translucent safety band in #DBEAF8. Show an exploitative policy path in red #C74735 bending toward opponent weakness but remaining inside or near the band. Add a subtle distance/regularisation visual using teal #148D80, suggesting pi_KL constraint without relying on readable text. Include small opponent-type nodes and risk boundary marks. Use gray #D7DDE7 structural lines, crisp geometry, subtle shadows. No readable text. Avoid cartoon or photorealistic style.
```

## illustration6_transformation.png

Placeholder: `illustration6`

Slide: 12, closing slide.

Target slot in slide: 1712 x 540 CSS px, rendered at 3424 x 1080 px.

Recommended generation size/aspect ratio: `3424x1080`, aspect ratio `856:270`.

Purpose: Final memorable transformation from fixed-strategy systems to adaptive, safe, accountable agents.

Prompt:

```text
Create a wide premium scientific transformation illustration for an academic presentation. Canvas 3424x1080 px, transparent or very light #F5F7FB background. On the left, show a fixed-strategy solver architecture as a rigid gray/blue policy block sending identical outputs to several opponent nodes. On the right, show an adaptive agent architecture with three integrated modules: inference/adaptation in blue #155F9F, safety constraint in red #C74735, and evaluation/accountability in teal #148D80. Connect left to right with a clean transformation flow, not a dramatic explosion. Use exact palette #17212C, #526173, #155F9F, #DBEAF8, #C74735, #FAE3DE, #148D80, #D8EEE9, #BB7D1C, #D7DDE7. No readable text. High-end academic vector style, crisp, calm, and memorable.
```
