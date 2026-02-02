---
phase: 17-artifact-updates
plan: 01
subsystem: templates
tags: [templates, terminology, experiments, studies]

# Dependency graph
requires:
  - phase: 15-command-renames
    provides: Renamed commands using research terminology
provides:
  - Updated STATE.md template with experiment terminology
  - Updated ROADMAP.md template with experiment/study terminology
  - Consistent research vocabulary across all project templates
affects: [new-project, all future GRD projects initialized from templates]

# Tech tracking
tech-stack:
  added: []
  patterns: []

key-files:
  created: []
  modified:
    - get-research-done/templates/state.md
    - get-research-done/templates/roadmap.md

key-decisions:
  - "Preserve {phase}-{plan} file naming convention in templates (existing project structure)"
  - "Preserve research loop phase terminology (researcher|critic|evaluator) - different concept"
  - "Changed milestone to study terminology consistently"

patterns-established: []

# Metrics
duration: 4min
completed: 2026-02-02
---

# Phase 17 Plan 01: Template Terminology Update Summary

**STATE.md and ROADMAP.md templates now use consistent experiment/study terminology, replacing all phase/milestone references for new projects**

## Performance

- **Duration:** 4 min
- **Started:** 2026-02-02T17:06:16Z
- **Completed:** 2026-02-02T17:10:19Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Updated STATE.md template from "Phase: [X] of [Y]" to "Experiment: [X] of [Y]"
- Updated ROADMAP.md template from "Phase N:" to "Experiment N:" throughout
- Changed milestone terminology to study terminology in groupings
- Verified no mixed phase/experiment terminology remains in templates

## Task Commits

Each task was committed atomically:

1. **Task 1: Update STATE.md template terminology** - `26e594d` (feat) [pre-existing]
2. **Task 2: Update ROADMAP.md template terminology** - `61903a0` (feat)

## Files Created/Modified
- `get-research-done/templates/state.md` - Current Position section now tracks experiments, "By Experiment" section header, Next Experiment Readiness references
- `get-research-done/templates/roadmap.md` - All phase references changed to experiment, milestone groupings changed to study groupings, progress table uses Experiment column

## Decisions Made

**Preserve {phase}-{plan} file naming:** The file naming convention (e.g., 01-02-PLAN.md) was preserved in templates even though terminology changed to experiments. This maintains consistency with existing project structure and file organization patterns.

**Preserve research loop phase terminology:** The "Phase: {{researcher|critic|evaluator|human_review}}" reference in STATE.md was intentionally preserved because it refers to research loop phases (which agents are active), not project-level phases/experiments.

**Milestone to study mapping:** Consistently changed "milestone" to "study" in roadmap groupings (v1.0 MVP - Experiments 1-4) to align with research workflow terminology.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

**Task 1 pre-existing:** STATE.md template changes were already completed in commit 26e594d (from a previous session). Verified changes were correct and moved to Task 2.

## Next Phase Readiness

- Templates ready for new project initialization with consistent terminology
- All template terminology aligned with renamed commands from Phase 15
- No blockers for Phase 17-02 (version bump)

---
*Phase: 17-artifact-updates*
*Completed: 2026-02-02*
