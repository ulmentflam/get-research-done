---
phase: 04-recursive-validation-loop
plan: 01
subsystem: recursive-validation
tags: [experiment-implementation, grd-researcher, grd-critic, isolated-runs, data-provenance, sha256, recursive-routing]

# Dependency graph
requires:
  - phase: 03-hypothesis-synthesis
    provides: OBJECTIVE.md with testable hypotheses and success criteria
provides:
  - /grd:research command for experiment implementation
  - grd-researcher agent with 8-step workflow
  - Experiment README template for run documentation
  - Isolated run directory pattern (experiments/run_NNN/)
  - Data provenance tracking (SHA-256 hashes)
  - Critic-driven routing infrastructure (PROCEED/REVISE_METHOD/REVISE_DATA/ESCALATE)
affects: [04-02-critic-agent, 04-03-evaluator-agent, 05-human-evaluation]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Isolated run directories (experiments/run_NNN_description/)"
    - "Data provenance via SHA-256 hashing, symlinks not copies"
    - "Recursive validation loop with Critic routing"
    - "OBJECTIVE.md hard gate (required for experiment implementation)"
    - "DATA_REPORT.md soft reference (optional context)"

key-files:
  created:
    - commands/grd/research.md
    - agents/grd-researcher.md
    - get-research-done/templates/experiment-readme.md
  modified: []

key-decisions:
  - "Hard gate on OBJECTIVE.md (required, cannot proceed without hypothesis)"
  - "Soft reference to DATA_REPORT.md (optional but recommended for data context)"
  - "Data referenced with SHA-256 hashes for provenance, not copied"
  - "Researcher spawns Critic via Task tool, not command-level spawn"
  - "Four verdict types: PROCEED/REVISE_METHOD/REVISE_DATA/ESCALATE"
  - "Complete snapshots in each run directory (code, config, data refs, logs, outputs, metrics, critique)"
  - "Auto-increment run numbering with optional description"
  - "README.md generated from template for each run"

patterns-established:
  - "Researcher agent 8-step pattern: Load context → Create directory → Reference data → Generate code → Execute → Collect metrics → Spawn Critic → Handle verdict"
  - "Run directory structure: code/, data/, logs/, outputs/, metrics/, plus README.md, config.yaml, CRITIC_LOG.md"
  - "CRITIC_LOG.md captures verdict and recommendations in each run"
  - "Continuation mode (--continue) loads previous critique history"

# Metrics
duration: 5min
completed: 2026-01-29
---

# Phase 04 Plan 01: Research Command & Agent Summary

**/grd:research command and grd-researcher agent with 8-step workflow implementing experiments from OBJECTIVE.md with Critic-driven recursive routing**

## Performance

- **Duration:** 5 min
- **Started:** 2026-01-29T04:13:58Z
- **Completed:** 2026-01-29T04:19:00Z
- **Tasks:** 3
- **Files created:** 3

## Accomplishments

- Created `/grd:research` command with OBJECTIVE.md hard gate and auto-increment run numbering
- Implemented grd-researcher agent with complete 8-step workflow (context loading through verdict handling)
- Established isolated run directory pattern with data provenance tracking (SHA-256 hashes)
- Integrated Critic-driven routing with four verdict types (PROCEED/REVISE_METHOD/REVISE_DATA/ESCALATE)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create /grd:research command** - `34b1d91` (feat)
2. **Task 2: Create grd-researcher agent** - `b4515b6` (feat)
3. **Task 3: Create experiment README template** - `0bc68bf` (feat)

## Files Created/Modified

**Created:**
- `commands/grd/research.md` - Phase 4 entry point for experiment implementation with OBJECTIVE.md hard gate
- `agents/grd-researcher.md` - 8-step workflow agent: loads context, creates runs, generates code, spawns Critic, routes verdicts
- `get-research-done/templates/experiment-readme.md` - Template for run directory README.md with placeholders for metadata, metrics, and verdict

## Decisions Made

**Command design:**
- Hard gate on OBJECTIVE.md (required) vs. soft reference to DATA_REPORT.md (optional context)
- Auto-increment run numbering by scanning experiments/ directory
- Continuation mode (--continue) for REVISE_METHOD iterations
- Command does NOT spawn Critic directly - Researcher manages Critic interaction internally

**Agent workflow:**
- 8-step pattern: Load context → Create directory → Reference data → Generate code → Execute → Collect metrics → Spawn Critic → Handle verdict
- Data provenance via SHA-256 hashes and .ref files (not copying large data files)
- Researcher spawns Critic via Task tool after metrics collection
- Four routing outcomes: PROCEED (approved), REVISE_METHOD (method issues), REVISE_DATA (data quality), ESCALATE (ambiguous failure)

**Run isolation:**
- Complete snapshot in each run directory: code/, data/, logs/, outputs/, metrics/, plus README.md, config.yaml, CRITIC_LOG.md
- Symlinks to data location with hash verification for provenance
- README.md generated from template with experiment summary and reproduction instructions

**Context integration:**
- OBJECTIVE.md: Extract hypothesis, metrics, evaluation methodology, baselines, falsification criteria
- DATA_REPORT.md: Extract data characteristics, leakage warnings, quality issues (if available)
- Previous CRITIC_LOG: Load critique history if continuing from REVISE_METHOD

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for Plan 04-02 (Critic Agent):**
- Researcher spawns Critic via Task tool (Step 7 in workflow)
- Critic needs implementation to receive experiment artifacts and return structured verdict
- Verdict format defined: Strengths, Weaknesses, Decision (PROCEED/REVISE_METHOD/REVISE_DATA/ESCALATE), Recommendations, Confidence, Reasoning

**Artifacts passed to Critic:**
- Experiment code (code/train.py or experiment.ipynb)
- Configuration (config.yaml)
- Metrics (SCORECARD.json with success criteria comparison)
- OBJECTIVE.md context
- DATA_REPORT.md findings
- Previous critique history (if continuing)

**Verdict routing:**
- PROCEED → Researcher may spawn Evaluator (or Phase 5 orchestrates)
- REVISE_METHOD → Logs critique, exits for /grd:research --continue
- REVISE_DATA → Routes back to /grd:explore with specific concerns
- ESCALATE → Surfaces to human for manual routing decision

**No blockers.** All interfaces defined for Critic agent implementation.

---
*Phase: 04-recursive-validation-loop*
*Completed: 2026-01-29*
