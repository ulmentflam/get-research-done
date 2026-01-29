---
phase: 03-hypothesis-synthesis
plan: 03
subsystem: hypothesis-validation
tags: [validation, data-constraints, error-handling, soft-gates]

# Dependency graph
requires:
  - phase: 03-01
    provides: Hypothesis domain model and OBJECTIVE.md specification
  - phase: 03-02
    provides: Architect command and agent implementation
provides:
  - Comprehensive validation logic for OBJECTIVE.md generation
  - Data-informed warnings from DATA_REPORT.md characteristics
  - Baseline soft gate (warns but allows proceeding)
  - Error vs warning distinction (blocks vs allows with confirmation)
  - Auto-populated constraints from data analysis
affects: [04-critic, phase-4, hypothesis-validation]

# Tech tracking
tech-stack:
  added: []
  patterns: [validation-orchestration, soft-gates, data-informed-warnings]

key-files:
  created: []
  modified: [agents/grd-architect.md]

key-decisions:
  - "Validation implemented as inline agent guidance, not executable code"
  - "Metric weights must sum to 1.0 - ERROR if invalid (blocks generation)"
  - "Baseline missing is WARNING only - soft gate allows proceeding"
  - "Data characteristics extracted in Step 1.3 for validation context"
  - "Class imbalance + accuracy metric triggers F1/AUC recommendation"
  - "HIGH confidence leakage warnings integrated into validation"

patterns-established:
  - "Validation orchestration: collect errors/warnings, present together, block on errors only"
  - "Soft gates: warn with options, user decides to proceed or fix"
  - "Data-informed warnings: use DATA_REPORT.md findings to contextualize validation"

# Metrics
duration: 2min
completed: 2026-01-29
---

# Phase 3 Plan 3: Validation & Constraints Summary

**Comprehensive validation guards OBJECTIVE.md generation with metric weight enforcement, baseline soft gate, and data-informed warnings from DATA_REPORT.md**

## Performance

- **Duration:** 2 min
- **Started:** 2026-01-29T06:17:01Z
- **Completed:** 2026-01-29T06:19:00Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Hypothesis completeness, metric weight, evaluation methodology, falsification criteria validation logic added
- Baseline soft gate warns but allows proceeding (not blocking)
- Data characteristics extraction (datetime columns, class imbalance, leakage, missing data, sample size)
- Data-informed validation warnings (class imbalance + accuracy, temporal leakage, HIGH confidence leakage features)
- Auto-populated constraints section from DATA_REPORT.md findings

## Task Commits

Each task was committed atomically:

1. **Task 1: Add validation logic to grd-architect agent** - `21ea03d` (feat)
2. **Task 2: Add data constraints integration** - `4df3566` (feat)

## Files Created/Modified
- `agents/grd-architect.md` - Enhanced Step 1.3 for data characteristics extraction, Step 6 with comprehensive validation subsections (6.1-6.6), Step 7 with auto-generated constraints

## Decisions Made

**Validation implemented as inline agent guidance:**
- Not executable code - agent applies rules using reasoning during Step 6 execution
- Pseudocode-style logic that agent follows to validate OBJECTIVE.md before generation

**Metric weights must sum to 1.0 (ERROR if invalid):**
- Tolerance: ±0.01
- Blocks OBJECTIVE.md generation until fixed
- User must adjust weights before proceeding

**Baseline missing is WARNING only (soft gate):**
- Warns user without comparison point, cannot claim improvement
- Presents options: own baseline, literature citation, random/majority baseline
- User can proceed with warning noted or return to refinement

**Data characteristics extraction in Step 1.3:**
- Extracts: datetime columns, class imbalance severity, HIGH confidence leakage warnings, missing data columns, sample size
- Used in validation (Step 6) and constraint generation (Step 7)

**Class imbalance + accuracy metric warning:**
- If HIGH class imbalance and user selects accuracy as primary metric
- Recommends F1, precision/recall, or AUC instead
- Suggests stratified k-fold over standard k-fold

**HIGH confidence leakage integration:**
- Warns if DATA_REPORT.md flagged leakage with HIGH confidence
- Lists features to exclude from hypothesis
- User decides if actionable based on domain knowledge

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## Next Phase Readiness

- Validation logic complete - OBJECTIVE.md generation is now guarded
- Baseline soft gate enables flexible but informed hypothesis acceptance
- Data-informed warnings provide contextual validation based on actual data characteristics
- Ready for Phase 4 (Critic) to consume validated OBJECTIVE.md documents

**No blockers.**

---
*Phase: 03-hypothesis-synthesis*
*Completed: 2026-01-29*
