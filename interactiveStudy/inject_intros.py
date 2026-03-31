#!/usr/bin/env python3
"""One-shot script: inject phase overview + contribution alignment from the
EN study plan into each rawSteps file, right after the first '---' separator.

Idempotent: if the marker '> **Phase Overview' already exists, the file is skipped.
"""

from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "planning" / "rawSteps"

# Phase overviews (keyed by phase letter)
PHASE_OVERVIEW = {
    "A": "This phase covers the foundational material required for all subsequent work: reinforcement learning basics (value estimation, policy optimization, experience replay) and game-theoretic fundamentals (extensive-form games, Nash equilibrium computation, and exploitability measurement). A solid command of both domains is essential before proceeding to the more specialized topics of later phases.",
    "B": "Phase A established a working CFR solver on the minimal Kuhn Poker benchmark, but vanilla CFR requires a full traversal of the game tree on every iteration — an approach that becomes infeasible as games grow. This phase will introduce two complementary scaling mechanisms: Monte Carlo sampling methods that reduce per-iteration cost, and game abstraction techniques that reduce the game tree itself. These tools are needed to bridge the gap between toy benchmarks and the medium-scale games on which later thesis work will be developed.",
    "C": "Phases A and B established tabular equilibrium solvers and abstraction techniques for medium-scale games. However, tabular methods store explicit strategy and regret values at every information set — an approach whose memory requirements grow linearly with game size and become prohibitive for large-scale domains. This phase replaces tabular storage with neural network function approximation, enabling equilibrium computation without explicit game tree enumeration.",
    "D": "This phase addresses the central research question: how should an agent adapt its play to a specific opponent? The preceding phases built the algorithmic toolbox — equilibrium solvers, abstraction, and neural approximation — but did not yet tackle opponent-aware play. Step 7 will introduce inference mechanisms that convert observed action sequences into beliefs about opponent behavior. Step 8 will cover algorithms that translate those beliefs into profitable yet safe strategy adjustments.",
    "E": "The preceding phases focused on two-player imperfect-information games. Phase E will transition the study to multi-agent settings, where new challenges arise: non-stationarity from simultaneously learning agents, credit assignment in joint-reward environments, and the emergence of coalitions. Step 9 introduces multi-agent RL paradigms (CTDE, PSRO), Step 10 scales to population-based training and evolutionary game theory, and Step 11 applies these tools to coalition formation in free-for-all games.",
    "F": "The preceding phases developed methods entirely within synthetic, self-play environments. Phase F will bridge the gap between theoretical methods and real-world behavioral data. Step 12 introduces sequence models (Decision Transformers) and assesses large language model agents in strategic settings. Step 13 applies the resulting pipeline to anonymized real-world poker hand histories, constructing player embeddings, behavioral classification systems, and a collusion detection module.",
    "G": "Phase G will synthesize the preceding work into two integrative deliverables. Step 14 constructs a unified evaluation framework validated across all game types encountered in the study plan — constituting the core of Contribution 3 (Evaluation Methodology). Step 15 maps the research frontier, designs the experimental program, produces a Chapter I outline for the dissertation, and establishes the publication pipeline.",
}

# Contribution alignment per step
STEP_ALIGNMENT = {
    "step_01": "The reinforcement learning methods studied in this step — value estimation, policy gradients, and experience replay — will recur throughout the thesis, particularly in the opponent modeling and adaptive exploitation components of the planned contributions.",
    "step_02": "The extensive-form game representation and CFR algorithm introduced here will provide the formal framework and baseline equilibrium computation used throughout the thesis. Exploitability, defined and implemented in this step, will serve as the primary quantitative metric across all three contributions.",
    "step_03": "Monte Carlo CFR variants will provide the computationally tractable equilibrium computation needed for medium-scale games, which will underpin the empirical work in later contributions. CFR+ accelerates convergence, enabling equilibrium computation for games beyond the reach of vanilla CFR.",
    "step_04": "This step will study how game abstraction — both lossless and lossy — affects the quality of computed equilibria, and how subgame solving can refine strategies during play. These techniques are directly relevant to later work on safe exploitation and opponent modeling.",
    "step_05": "Deep CFR and NFSP will be studied as methods for computing equilibrium strategies in games too large for tabular solvers — a capability needed for the planned behavioral adaptation work. NFSP's anticipatory parameter, which interpolates between equilibrium and exploitative play, foreshadows the exploitation–safety tradeoff central to the thesis.",
    "step_06": "This step will survey five landmark game-solving systems that define the current state of the art. ReBeL's public belief state framework is of particular relevance to the planned belief-based opponent modeling (Contribution 1). Pluribus demonstrates empirical success in multiplayer poker without formal safety guarantees — highlighting the theoretical gap that Contribution 2 will seek to address.",
    "step_07": "Bayesian opponent modeling will serve as the inference component of the planned Behavioral Adaptation Framework (Contribution 1). Three modeling paradigms will be studied — type-based models, continuous parametric models, and consistent convergent estimators — each offering different tradeoffs between assumptions, convergence speed, and robustness.",
    "step_08": "This step covers the exploitation–safety tradeoff, which is the theoretical core of the thesis. Key topics include the Restricted Nash Response (RNR), the Safety Theorem of Ganzfried and Sandholm (2015) — which provides formal guarantees in two-player zero-sum settings but fails in N-player games — and subgame exploitation methods for real-time safe play.",
    "step_09": "This step will provide the algorithmic vocabulary for extending the thesis from two-player to multi-agent settings. The CTDE paradigm introduces the architectural pattern — centralized training, decentralized execution — used throughout the remainder of the thesis. PSRO provides a population-based framework relevant to defining safety in multi-agent populations.",
    "step_10": "Population-based training and the AlphaStar league architecture will be studied as examples of implicit opponent modeling at population scale, complementing the explicit Bayesian modeling of Step 7. The spinning top decomposition — distinguishing genuine skill improvement from non-transitive cycling — will be adopted into the evaluation methodology (Contribution 3).",
    "step_11": "This step crystallizes the central theoretical gap of the thesis. In two-player games, safe exploitation uses Nash equilibrium as the safety baseline (Step 8). In N-player free-for-all games, Nash equilibrium is both computationally intractable and strategically insufficient — it ignores coalition structures.",
    "step_12": "This step will study the Decision Transformer architecture and its adversarially robust variant (ARDT), which recovers near-Nash strategies from offline data — a potential alternative path for Contribution 2 that bypasses intractable equilibrium computation in N-player settings.",
    "step_13": "This step will apply the behavioral adaptation methodology from Steps 7, 8, and 12 to anonymized industry data, providing practical validation for Contribution 1. The behavioral deviation from equilibrium play measured on real player data will quantify exploitation opportunities relevant to Contribution 2.",
    "step_14": "This step will constitute the core of Contribution 3 directly. The planned three-layer evaluation framework will integrate exploitability computation, population-level ranking (Elo, α-Rank, VasE), and statistical confidence quantification (AIVAT variance reduction).",
    "step_15": "This step will complete the learning phase and design the research phase. The deliverables will include a research frontier map for each contribution, formal contribution design documents, experimental specifications, a Chapter I outline (25–30 pages), and a publication pipeline through to defense.",
}

# Which phase each step belongs to
STEP_PHASE = {
    "step_01": "A", "step_02": "A",
    "step_03": "B", "step_04": "B",
    "step_05": "C", "step_06": "C",
    "step_07": "D", "step_08": "D",
    "step_09": "E", "step_10": "E", "step_11": "E",
    "step_12": "F", "step_13": "F",
    "step_14": "G", "step_15": "G",
}

# Which steps are the first in their phase (show phase overview)
PHASE_FIRST_STEP = {"step_01", "step_03", "step_05", "step_07", "step_09", "step_12", "step_14"}

STEP_FILENAMES = {
    "step_01": "step_01_rl_basics.md",
    "step_02": "step_02_game_theory_cfr.md",
    "step_03": "step_03_cfr_variants_mc.md",
    "step_04": "step_04_game_abstraction_scaling.md",
    "step_05": "step_05_neural_equilibrium.md",
    "step_06": "step_06_end_to_end_game_ai.md",
    "step_07": "step_07_opponent_modeling.md",
    "step_08": "step_08_safe_exploitation.md",
    "step_09": "step_09_multi_agent_rl.md",
    "step_10": "step_10_population_training_evo_gt.md",
    "step_11": "step_11_coalition_formation_ffa.md",
    "step_12": "step_12_sequence_models_llm_agents.md",
    "step_13": "step_13_behavioral_analysis.md",
    "step_14": "step_14_evaluation_frameworks.md",
    "step_15": "step_15_research_frontier_mapping.md",
}


def inject():
    for step_id, filename in STEP_FILENAMES.items():
        filepath = RAW_DIR / filename
        text = filepath.read_text(encoding="utf-8")

        # Idempotency check
        if "> **Phase Overview" in text or "> **Contribution Alignment" in text:
            print(f"SKIP {filename} (already injected)")
            continue

        # Find the first '---' line
        lines = text.split("\n")
        sep_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "---":
                sep_idx = i
                break

        if sep_idx is None:
            print(f"WARN {filename}: no --- separator found, skipping")
            continue

        # Build the intro block
        phase = STEP_PHASE[step_id]
        parts = []
        if step_id in PHASE_FIRST_STEP:
            parts.append(f"> **Phase Overview:** {PHASE_OVERVIEW[phase]}")
            parts.append(">")
        parts.append(f"> **Contribution Alignment:** {STEP_ALIGNMENT[step_id]}")

        intro_block = "\n".join(parts)

        # Insert after the --- line: blank line, intro block, blank line
        lines.insert(sep_idx + 1, "")
        lines.insert(sep_idx + 2, intro_block)
        lines.insert(sep_idx + 3, "")

        filepath.write_text("\n".join(lines), encoding="utf-8")
        print(f"DONE {filename}")


if __name__ == "__main__":
    inject()
