# Get Research Done (GRD)

## What This Is

A recursive, agentic framework for machine learning research that brings structured rigor to hypothesis validation. GRD is a Claude Code workflow tool for ML researchers, evolving from the Get Shit Done (GSD) philosophy but optimized for the non-linear, data-dependent nature of AI research. Instead of moving from PRD to Task, GRD moves from Data Reconnaissance to Hypothesis to Recursive Validation.

## Core Value

Structured ML experimentation with scientific rigor — from hypothesis to validated conclusion, with a Critic agent enforcing skepticism at every step.

## Philosophy

- **Hypothesis over Features**: We don't build features; we test hypotheses
- **Data-First**: No research objective is set without initial Exploratory Data Analysis (EDA)
- **The Recursive Loop**: Self-correcting system — if results contradict the data profile, the agentic loop forces return to the data layer
- **Critic-Led Rigor**: Automated Critic agent acts as scientific skeptic to prevent overfitting, data leakage, and logical fallacies

## Requirements

### Validated

- ✓ Claude Code hook integration — existing
- ✓ Agent spawning architecture — existing
- ✓ State tracking system (STATE.md) — existing
- ✓ Config system for workflow preferences — existing
- ✓ Phase/planning model — existing

### Active

- [ ] Rebrand GSD → GRD (name, ASCII art, package name)
- [ ] New lifecycle: Data Reconnaissance → Hypothesis Synthesis → Recursive Loop → Human Evaluation
- [ ] Explorer Agent: Analyzes raw data, produces DATA_REPORT.md
- [ ] Architect role: Turns goals into testable hypotheses, produces OBJECTIVE.md
- [ ] Researcher Agent: Implementation, experimentation, optimization
- [ ] Critic Agent: Skepticism, data leak detection, red-teaming with exit codes (PROCEED/REVISE_METHOD/REVISE_DATA)
- [ ] Evaluator Agent: Quantitative benchmarking, produces SCORECARD.json
- [ ] OBJECTIVE.md template replacing PRD (Context, Hypothesis, Success Metrics, Constraints, Baselines)
- [ ] Experiment versioning structure (experiments/run_001/, run_002/, etc.)
- [ ] Human-in-the-Loop decision gate (Seal/Iterate/Archive)
- [ ] Notebook → production code graduation path
- [ ] New folder structure (reports/, agents/, experiments/, human_eval/)
- [ ] Update installation script with new package name
- [ ] New ASCII art for GRD branding

### Out of Scope

- Requirements traceability (REQ-ID mapping) — replaced by hypothesis-driven structure
- Milestone/release system (v1/v2) — research doesn't ship versions, it validates hypotheses
- Software-specific agents (code mappers, integration checkers) — keep only research-relevant agents
- Feature-based planning — hypotheses aren't features

## Context

**Existing codebase:** This is a brownfield refactor of the GSD (Get Shit Done) project. The current codebase has:
- Claude Code hooks for workflow automation
- Agent spawning system for specialized tasks
- Workflow orchestration via skill files
- State tracking and context restoration
- Template system for artifacts

**Target audience:** ML researchers who need structure for experimentation without the overhead of product management tooling.

**Key insight:** Research is recursive, not linear. The Critic agent's ability to force loops back to earlier phases (REVISE_DATA sends back to Explorer) is the core innovation over GSD's linear phase progression.

## The GRD Lifecycle

### Phase 1: Data Reconnaissance (Explorer)
- **Input:** Raw Dataset + High-level Project Goal
- **Output:** `DATA_REPORT.md` (distributions, anomalies, leakage risks, baseline signals)

### Phase 2: Hypothesis Synthesis (Architect)
- **Input:** DATA_REPORT.md + Project Goal
- **Output:** `OBJECTIVE.md` (testable hypothesis replacing PRD)

### Phase 3: Recursive Agentic Loop
1. **Researcher** develops code, training pipelines, experimental setups
2. **Critic** audits work with three exit paths:
   - `PROCEED`: Logic sound, results align with data profile → Evaluator
   - `REVISE_METHOD`: Logical error, bad hyperparams → back to Researcher
   - `REVISE_DATA`: Anomalous results, potential leakage → back to Explorer
3. **Evaluator** runs standardized benchmark suite

### Phase 4: Human Evaluation (Decision Gate)
- **Evidence Package:** OBJECTIVE.md + DATA_REPORT.md + CRITIC_LOGS.md + SCORECARD.json
- **Decisions:** Seal (proven) / Iterate (refine) / Archive (disproven)

## Agent Roles

| Role | Responsibility | Primary Output |
|------|----------------|----------------|
| Explorer | Uncover the "truth" of the data before coding | `DATA_REPORT.md` |
| Architect | Turn goals into testable, scientific hypotheses | `OBJECTIVE.md` |
| Researcher | Implementation, experimentation, optimization | `experiment_scripts/` |
| Critic | Skepticism, finding data leaks, logical red-teaming | `critique_report.md` |
| Evaluator | Quantitative benchmarking against objective | `SCORECARD.json` |

## Folder Structure

```
.
├── PROJECT_GOAL.md       # North Star vision
├── OBJECTIVE.md          # Active hypothesis being tested
├── reports/
│   └── DATA_REPORT.md    # Living document of data insights
├── agents/               # System prompts for agent roles
│   ├── explorer.prompt
│   ├── researcher.prompt
│   ├── critic.prompt
│   └── evaluator.prompt
├── experiments/          # Versioned history of every loop
│   └── run_001/
│       ├── code/         # Python scripts, configs, notebooks
│       ├── logs/         # Researcher vs. Critic argument logs
│       ├── data_check.md # Recorded if recursion to EDA occurred
│       └── scorecard.json
└── human_eval/           # Narrative record of human decisions
    └── decision_log.md   # Why we pivoted or promoted a hypothesis
```

## Constraints

- **Tech stack**: Must remain Claude Code compatible (hooks, MCP integration)
- **Installation**: npm-based, same mechanism as GSD with new package name
- **Backward compatibility**: Not required — this is a clean break from GSD

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Recursive loop over linear phases | Research is non-linear; results often invalidate assumptions | — Pending |
| Critic agent with exit codes | Forces scientific rigor, prevents overfitting/leakage | — Pending |
| Data-first philosophy | Hypotheses must be grounded in data reality | — Pending |
| Human-in-the-loop gate | Prevents false positives, maintains research integrity | — Pending |

---
*Last updated: 2026-01-27 after initialization*
