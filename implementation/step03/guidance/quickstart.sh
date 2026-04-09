#!/usr/bin/env bash
# Quick-start runner for Step 03: MCCFR Variants
# Usage: bash step03_quickstart.sh [option]
# 
# Options:
#   tutorial   - Run interactive educational demo (recommended first)
#   compare    - Run full comparison (10k iterations each, ~5 min)
#   analyze    - Run variance analysis (5 runs per method, ~5 min)
#   all        - Run all scripts in sequence
#   help       - Show this help message

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $1"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
}

run_cmd() {
    echo -e "${GREEN}▶ Running:${NC} $1"
    python "$1"
    echo -e "${GREEN}✓ Complete${NC}\n"
}

case "${1:-tutorial}" in
    tutorial)
        header "MCCFR Educational Tutorial (5k iterations each)"
        run_cmd "implementation/step03/tutorial.py"
        echo -e "${YELLOW}Next step: Run 'bash step03_quickstart.sh compare' for full comparison${NC}"
        ;;
    
    compare)
        header "MCCFR Full Comparison (10k iterations each)"
        run_cmd "implementation/step03/playground.py"
        echo -e "${YELLOW}Output saved: mccfr_comparison_results.json${NC}"
        ;;
    
    analyze)
        header "Variance & Performance Analysis"
        run_cmd "implementation/step03/analyze_mccfr.py"
        echo -e "${YELLOW}Output saved: mccfr_detailed_analysis.json${NC}"
        ;;
    
    all)
        header "Running ALL Step 03 experiments (15 min total)"
        run_cmd "implementation/step03/tutorial.py"
        run_cmd "implementation/step03/playground.py"
        run_cmd "implementation/step03/analyze_mccfr.py"
        echo -e "${GREEN}✓ All experiments complete!${NC}"
        ;;
    
    help|--help|-h)
        cat <<EOF
Step 03: MCCFR Variants - Quick Start

USAGE:
    bash step03_quickstart.sh [option]

OPTIONS:
    tutorial  - Interactive demo with explanations (5k iterations, ~3 min)
                Best starting point to understand the algorithm
    
    compare   - Full comparison of both methods (10k iterations, ~5 min)
                See which sampling type wins on Kuhn Poker
    
    analyze   - Statistical variance analysis (5 runs, ~5 min)
                Measure stability and computational cost
    
    all       - Run tutorial + compare + analyze (15 min)
                Complete experiment suite
    
    help      - Show this message

OUTPUTS:
    tutorial.py       → Console output (explanations + metrics)
    playground.py     → mccfr_comparison_results.json
    analyze_mccfr.py  → mccfr_detailed_analysis.json

WHAT YOU'LL LEARN:
    ✓ Why MCCFR scales to large games
    ✓ Trade-offs between sampling strategies
    ✓ How Nash equilibrium serves as convergence measure
    ✓ Empirical algorithm comparison methodology

RECOMMENDED SEQUENCE:
    1. bash step03_quickstart.sh tutorial     # Understand the concepts
    2. bash step03_quickstart.sh compare      # See results on Kuhn Poker
    3. bash step03_quickstart.sh analyze      # Measure stability

ADVANCED:
    python implementation/step03/playground.py     # Custom runs
    python implementation/step03/config.py         # Tweak hyperparameters
    cat implementation/step03/mccfr_explanation.md # Deep technical details

EOF
        ;;
    
    *)
        echo "Unknown option: $1"
        echo "Use 'bash step03_quickstart.sh help' for usage"
        exit 1
        ;;
esac
