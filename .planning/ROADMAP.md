# Roadmap: Get Research Done (GRD)

## Overview

GRD transforms the Get Shit Done (GSD) codebase into a recursive, agentic framework for ML research. This roadmap moves from foundational rebranding through data-first workflow implementation, culminating in the recursive validation loop that is GRD's core innovation. Each phase delivers a coherent capability, building from orchestration foundations through specialized agents to human-in-the-loop validation gates. The journey completes with notebook support, enabling researchers to graduate exploratory work into validated experiments.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3, 4, 5, 6): Planned milestone work
- Decimal phases (e.g., 2.1, 2.2): Urgent insertions (if needed, marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Core Orchestration & Branding** - Foundation layer with GRD identity and state management
- [x] **Phase 2: Data Reconnaissance** - Explorer agent for data-first EDA workflow
- [x] **Phase 3: Hypothesis Synthesis** - Architect agent transforms insights into testable objectives
- [x] **Phase 4: Recursive Validation Loop** - Researcher/Critic/Evaluator agents with state routing
- [x] **Phase 5: Human Evaluation Gate** - Evidence packages and decision logging
- [ ] **Phase 6: Notebook Support** - Jupyter integration and graduation path

## Phase Details

### Phase 1: Core Orchestration & Branding
**Goal**: Establish GRD identity and orchestration foundation for specialized agents

**Depends on**: Nothing (first phase)

**Requirements**: BRAND-01, BRAND-02, BRAND-03, BRAND-04, STATE-01, STATE-02, STATE-03

**Success Criteria** (what must be TRUE):
  1. User can run `grd` command and see GRD-branded CLI with ASCII art
  2. User can install via npm with `get-research-done` package name
  3. GRD agents can spawn with isolated contexts and file-based state persistence
  4. STATE.md tracks loop history and current research phase
  5. User can resume interrupted sessions with full context restoration

**Plans**: 6 plans

Plans:
- [x] 01-01-PLAN.md — Rename core directories and files (commands/, get-research-done/, agents/, hooks/)
- [x] 01-02-PLAN.md — Create GRD ASCII art branding for CLI installer
- [x] 01-03-PLAN.md — Update text references across commands, agents, and workflows
- [x] 01-04-PLAN.md — Update hooks and build scripts for GRD naming
- [x] 01-05-PLAN.md — Update package.json, README, and extend STATE.md template
- [x] 01-06-PLAN.md — Final verification and human approval checkpoint

### Phase 2: Data Reconnaissance
**Goal**: Users can analyze raw data and surface anomalies before hypothesis formation

**Depends on**: Phase 1

**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04

**Success Criteria** (what must be TRUE):
  1. User can run `/grd:explore` command to launch Explorer agent on raw dataset
  2. Explorer generates DATA_REPORT.md with distributions, outliers, and anomaly flags
  3. Explorer detects potential data leakage risks (feature/target overlap, temporal issues)
  4. User cannot proceed to hypothesis synthesis without completed DATA_REPORT.md (data-first gating enforced)

**Plans**: 4 plans

Plans:
- [x] 02-01-PLAN.md — Create /grd:explore command, grd-explorer agent skeleton, and DATA_REPORT.md template
- [x] 02-02-PLAN.md — Implement Explorer agent data loading, sampling, and statistical profiling
- [x] 02-03-PLAN.md — Implement Explorer agent leakage detection and report generation
- [x] 02-04-PLAN.md — Integrate soft gate into /grd:architect and verify complete workflow

### Phase 3: Hypothesis Synthesis
**Goal**: Users can transform data insights into testable scientific hypotheses

**Depends on**: Phase 2

**Requirements**: HYPO-01, HYPO-02, HYPO-03, HYPO-04

**Success Criteria** (what must be TRUE):
  1. User can run `/grd:architect` command to synthesize hypothesis from DATA_REPORT.md
  2. Architect generates OBJECTIVE.md with context, hypothesis, success metrics, constraints, and baselines
  3. OBJECTIVE.md includes falsification criteria (what would disprove the hypothesis)
  4. System enforces baseline definition before accepting hypothesis as complete

**Plans**: 4 plans

Plans:
- [x] 03-01-PLAN.md — Create OBJECTIVE.md template with all required sections
- [x] 03-02-PLAN.md — Update /grd:architect command and create grd-architect agent
- [x] 03-03-PLAN.md — Add validation logic and baseline warning system
- [x] 03-04-PLAN.md — Integration verification and human approval checkpoint

### Phase 4: Recursive Validation Loop
**Goal**: Experiments are validated through skeptical criticism with automatic routing back to earlier phases when anomalies detected

**Depends on**: Phase 3

**Requirements**: LOOP-01, LOOP-02, LOOP-03, LOOP-04, LOOP-05, LOOP-06, LOOP-07

**Success Criteria** (what must be TRUE):
  1. Researcher agent can implement experiments (code, notebooks, training pipelines) from OBJECTIVE.md
  2. Critic agent audits work and returns exit codes: PROCEED, REVISE_METHOD, or REVISE_DATA
  3. REVISE_METHOD routes back to Researcher with critique feedback
  4. REVISE_DATA routes back to Explorer for data re-verification
  5. PROCEED routes to Evaluator for quantitative benchmarking
  6. Each iteration creates isolated `experiments/run_NNN/` directory with code, logs, and outputs
  7. Evaluator generates SCORECARD.json with metrics against hypothesis success criteria
  8. Loop depth limits prevent infinite recursion (maximum iterations enforced)

**Plans**: 5 plans

Plans:
- [x] 04-01-PLAN.md — Create /grd:research command, grd-researcher agent, and experiment directory templates
- [x] 04-02-PLAN.md — Create grd-critic agent with LLM-based routing and CRITIC_LOG template
- [x] 04-03-PLAN.md — Create grd-evaluator agent and SCORECARD.json template
- [x] 04-04-PLAN.md — Wire loop orchestration with iteration limits and human gate
- [x] 04-05-PLAN.md — Verification and human approval checkpoint

### Phase 5: Human Evaluation Gate
**Goal**: Humans make final validation decisions based on complete evidence packages

**Depends on**: Phase 4

**Requirements**: HUMAN-01, HUMAN-02, HUMAN-03

**Success Criteria** (what must be TRUE):
  1. System bundles evidence package: OBJECTIVE.md + DATA_REPORT.md + CRITIC_LOGS.md + SCORECARD.json
  2. User receives interactive decision gate prompting for Seal/Iterate/Archive choice
  3. Human decisions are logged in `human_eval/decision_log.md` with rationale
  4. Failed hypotheses (Archive path) are preserved with explanation in `experiments/archive/`

**Plans**: 5 plans

Plans:
- [x] 05-01-PLAN.md — Create /grd:evaluate command and decision/archive templates
- [x] 05-02-PLAN.md — Implement evidence presentation and decision gate
- [x] 05-03-PLAN.md — Implement decision logging (per-run and central)
- [x] 05-04-PLAN.md — Implement archive flow for negative results
- [x] 05-05-PLAN.md — Verification and human approval checkpoint

### Phase 6: Notebook Support
**Goal**: Users can execute Jupyter notebooks as experiments with explicit graduation to validated scripts

**Depends on**: Phase 5

**Requirements**: NOTE-01, NOTE-02, NOTE-03

**Success Criteria** (what must be TRUE):
  1. System can execute Jupyter notebooks as experiments via papermill or similar engine
  2. Clear separation exists between `notebooks/exploration/` (notebooks) and `src/experiments/` (scripts)
  3. Graduation checklist validates notebooks are refactored (no hardcoded paths, deterministic seeds, parameterized)
  4. Critic enforces graduation requirements before marking notebooks as "validated"

**Plans**: 5 plans

Plans:
- [ ] 06-01-PLAN.md — Create notebook executor and graduation validator Python modules
- [ ] 06-02-PLAN.md — Create graduated script template and directory scaffolds
- [ ] 06-03-PLAN.md — Update grd-researcher agent for notebook execution support
- [ ] 06-04-PLAN.md — Create /grd:graduate command and grd-graduator agent
- [ ] 06-05-PLAN.md — Update Critic for notebook evaluation and verify phase end-to-end

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Orchestration & Branding | 6/6 | Complete | 2026-01-28 |
| 2. Data Reconnaissance | 4/4 | Complete | 2026-01-28 |
| 3. Hypothesis Synthesis | 4/4 | Complete | 2026-01-28 |
| 4. Recursive Validation Loop | 5/5 | Complete | 2026-01-30 |
| 5. Human Evaluation Gate | 5/5 | Complete | 2026-01-30 |
| 6. Notebook Support | 0/5 | Planned | - |

---
*Roadmap created: 2026-01-27*
*Depth: standard (6 phases)*
*Coverage: 25/25 requirements mapped*
