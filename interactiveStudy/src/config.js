/* ===== Step Metadata ===== */
const STEP_META = [
  { id: "step_01", num: 1,  title: "RL Basics",             phase: "A", phaseLabel: "A \u2014 Foundation",         days: 14 },
  { id: "step_02", num: 2,  title: "Game Theory + CFR",     phase: "A", phaseLabel: "A \u2014 Foundation",         days: 14 },
  { id: "step_03", num: 3,  title: "CFR Variants + MC",     phase: "B", phaseLabel: "B \u2014 Scaling",            days: 10 },
  { id: "step_04", num: 4,  title: "Game Abstraction",      phase: "B", phaseLabel: "B \u2014 Scaling",            days: 10 },
  { id: "step_05", num: 5,  title: "Neural Equilibrium",    phase: "C", phaseLabel: "C \u2014 Neural Methods",     days: 11 },
  { id: "step_06", num: 6,  title: "End-to-End Game AI",    phase: "C", phaseLabel: "C \u2014 Neural Methods",     days: 21 },
  { id: "step_07", num: 7,  title: "Opponent Modeling",     phase: "D", phaseLabel: "D \u2014 Opponent Modeling",  days: 21 },
  { id: "step_08", num: 8,  title: "Safe Exploitation",     phase: "D", phaseLabel: "D \u2014 Opponent Modeling",  days: 21 },
  { id: "step_09", num: 9,  title: "Multi-Agent RL",        phase: "E", phaseLabel: "E \u2014 Multi-Agent",        days: 14 },
  { id: "step_10", num: 10, title: "Population Training",   phase: "E", phaseLabel: "E \u2014 Multi-Agent",        days: 14 },
  { id: "step_11", num: 11, title: "Coalition Formation",   phase: "E", phaseLabel: "E \u2014 Multi-Agent",        days: 14 },
  { id: "step_12", num: 12, title: "Sequence Models + LLM", phase: "F", phaseLabel: "F \u2014 Data-Driven",        days: 10 },
  { id: "step_13", num: 13, title: "Behavioral Analysis",   phase: "F", phaseLabel: "F \u2014 Data-Driven",        days: 14 },
  { id: "step_14", num: 14, title: "Evaluation Frameworks", phase: "G", phaseLabel: "G \u2014 Integration",        days: 14 },
  { id: "step_15", num: 15, title: "Research Frontier",     phase: "G", phaseLabel: "G \u2014 Integration",        days: 10 },
];

const PLAN_START = new Date(2026, 2, 9); // March 9, 2026 (0-based month)
const BASE_TOTAL_DAYS = STEP_META.reduce((s, m) => s + m.days, 0); // 232

/* ===== Per-Phase Checkpoint count (texts come from t()) ===== */
const PHASE_CHECKPOINT_COUNTS = { 1: 2, 2: 2, 3: 2, 4: 2, 5: 2 };

/* ===== Report Availability (stepId → reports folder name) ===== */
const STEP_REPORTS = { step_01: 'step01', step_02: 'step02', step_03: 'step03' };
const REPORT_BASE_URL = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/reports';
const SUMMARY_BASE_URL = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/summaries';
const STUDY_PLAN_URL_EN = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/studyPlan/studyPlanEN.pdf';
const STUDY_PLAN_URL_BG = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/studyPlan/studyPlanBG.pdf';
const RESEARCH_GOALS_URL_EN = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/reports/ruseMay/adaptive-multiagents-initial-report-may-en.pdf';
const RESEARCH_GOALS_URL_BG = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/reports/ruseMay/adaptive-multiagents-initial-report-may-bg.pdf';

/* ===== Tertiary step colors for calendar (cycle within phase) ===== */
const STEP_BG_PALETTE = [
  ['#dbeafe','#bfdbfe','#93c5fd'],  // A — blue
  ['#fae8ff','#f5d0fe','#f0abfc'],  // B — fuchsia
  ['#fef3c7','#fde68a','#fcd34d'],  // C — amber
  ['#ffe4e6','#fecdd3','#fda4af'],  // D — rose
  ['#dcfce7','#bbf7d0','#86efac'],  // E — emerald
  ['#cffafe','#a5f3fc','#67e8f9'],  // F — cyan
  ['#ede9fe','#ddd6fe','#c4b5fd'],  // G — violet
];
const STEP_BG_PALETTE_DARK = [
  ['#1e3a5f','#1a3050','#162845'],  // A — blue
  ['#4a1248','#3d1040','#330e38'],  // B — fuchsia
  ['#44310a','#3a2808','#302006'],  // C — amber
  ['#4a1a2e','#401528','#361022'],  // D — rose
  ['#14432a','#103824','#0c2d1e'],  // E — emerald
  ['#0a3040','#08283a','#062033'],  // F — cyan
  ['#2a1555','#23114a','#1c0d3e'],  // G — violet
];
const PHASE_ORDER = ['A','B','C','D','E','F','G'];

function getStepBg(stepIndex) {
  const step = STEP_META[stepIndex];
  const phaseIdx = PHASE_ORDER.indexOf(step.phase);
  const palette = document.documentElement.getAttribute('data-theme') === 'dark' ? STEP_BG_PALETTE_DARK : STEP_BG_PALETTE;
  const colors = palette[phaseIdx] || palette[0];
  let posInPhase = 0;
  for (let i = 0; i < stepIndex; i++) {
    if (STEP_META[i].phase === step.phase) posInPhase++;
  }
  return colors[posInPhase % colors.length];
}

function getPhaseColors(phase) {
  const s = getComputedStyle(document.documentElement);
  const p = phase.toLowerCase();
  return {
    bg: s.getPropertyValue(`--phase-${p}-bg`).trim(),
    border: s.getPropertyValue(`--phase-${p}-border`).trim(),
    text: s.getPropertyValue(`--phase-${p}-text`).trim(),
  };
}

/* ===== State ===== */
let currentStepIndex = 0;
let scheduleAdjust = 0;
let isHomepage = false;
let isCalendarPage = false;
let isGlossaryPage = false;
let calendarMonth = new Date().getMonth();
let calendarYear = new Date().getFullYear();
let calendarFull = false;
