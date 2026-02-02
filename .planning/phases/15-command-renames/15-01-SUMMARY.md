---
phase: 15-command-renames
plan: 01
subsystem: cli
tags: [commands, naming, experiment-terminology]

# Dependency graph
requires:
  - phase: 11-terminology-rename
    provides: "Study-centric terminology foundation"
provides:
  - "Three core commands renamed to experiment terminology"
  - "All cross-references updated across codebase"
  - "design-experiment, run-experiment, scope-experiment commands"
affects: [16-command-chaining, 17-command-artifacts, documentation]

# Tech tracking
tech-stack:
  added: []
  patterns: ["Experiment-centric command naming"]

key-files:
  created:
    - commands/grd/design-experiment.md
    - commands/grd/run-experiment.md
    - commands/grd/scope-experiment.md
  modified:
    - agents/grd-planner.md
    - agents/grd-phase-researcher.md
    - agents/grd-plan-checker.md
    - agents/grd-roadmapper.md
    - agents/grd-verifier.md
    - agents/grd-codebase-mapper.md
    - get-research-done/workflows/*
    - get-research-done/templates/*
    - commands/grd/help.md

key-decisions:
  - "Use 'design-experiment' not 'plan-experiment' - emphasizes experimental design"
  - "Use 'run-experiment' not 'execute-experiment' - simpler, more direct"
  - "Use 'scope-experiment' not 'define-experiment' - scope implies boundaries"
  - "No backward compatibility aliases - clean break for v1.2"

patterns-established:
  - "Experiment terminology: design → run → validate (replacing plan → execute → verify)"

# Metrics
duration: 3min
completed: 2026-02-01
---

# Phase 15 Plan 01: Core Command Renames Summary

**Three core workflow commands renamed to experiment terminology: design-experiment, run-experiment, scope-experiment with full cross-reference updates**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-02T02:06:04Z
- **Completed:** 2026-02-02T02:09:18Z
- **Tasks:** 3
- **Files modified:** 73

## Accomplishments
- Renamed plan-phase → design-experiment across both command directories
- Renamed execute-phase → run-experiment with complete reference updates
- Renamed discuss-phase → scope-experiment with terminology shift
- Updated all agent, workflow, and template cross-references
- Preserved historical phase documentation (unchanged)

## Task Commits

Each task was committed atomically:

1. **Task 1: Rename plan-phase to design-experiment** - `13a52fd` (refactor)
2. **Task 2: Rename execute-phase to run-experiment** - `f13aed1` (refactor)
3. **Task 3: Rename discuss-phase to scope-experiment** - `680d39d` (refactor)

## Files Created/Modified

**Created:**
- `commands/grd/design-experiment.md` - Create experiment execution plans
- `commands/grd/run-experiment.md` - Execute experiment plans with wave parallelization
- `commands/grd/scope-experiment.md` - Capture experiment vision before planning

**Modified (selected):**
- `agents/grd-planner.md` - Updated command references
- `agents/grd-phase-researcher.md` - Updated workflow references
- `agents/grd-plan-checker.md` - Updated command references
- `get-research-done/workflows/execute-plan.md` - Updated orchestration docs
- `get-research-done/templates/phase-prompt.md` - Updated template references
- `commands/grd/help.md` - Updated command list

## Decisions Made

**Command naming rationale:**
- **design-experiment** over "plan-experiment" - emphasizes experimental design methodology
- **run-experiment** over "execute-experiment" - shorter, more direct (common in ML tooling)
- **scope-experiment** over "define-experiment" - "scope" better captures boundary-setting nature

**No backward compatibility:**
- Followed v1.2 decision to not provide aliases
- Clean break enables simpler codebase maintenance
- Users must update to new command names

## Deviations from Plan

None - plan executed exactly as written. All three commands renamed, frontmatter updated, cross-references replaced, historical docs preserved.

## Issues Encountered

**Issue:** .claude directory is gitignored
- **Resolution:** Mirrored commands/ directory tracks the same files
- **Impact:** None - both directories updated, only commands/ committed

## User Setup Required

None - command renames are internal refactoring. Users will see new command names in help and autocomplete.

## Next Phase Readiness

**Ready for:** Command chaining implementation (Phase 16)
- All core commands now use experiment terminology
- Cross-references updated for chain definitions
- Command structure stable for chaining patterns

**No blockers:** Clean rename with no breaking changes to command behavior, only names.

---
*Phase: 15-command-renames*
*Completed: 2026-02-01*
