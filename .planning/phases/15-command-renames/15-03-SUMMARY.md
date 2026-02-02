---
phase: 15-command-renames
plan: 03
subsystem: commands
tags: [command-names, terminology, grd, experiments]

# Dependency graph
requires:
  - phase: 15-command-renames
    provides: renamed experiment lifecycle commands
provides:
  - Renamed add-phase to add-experiment
  - Renamed insert-phase to insert-experiment
  - Renamed remove-phase to remove-experiment
  - Updated all cross-references in active code
affects: [command-documentation, user-facing-commands]

# Tech tracking
tech-stack:
  added: []
  patterns: [experiment-centric-terminology]

key-files:
  created:
    - .claude/commands/grd/add-experiment.md
    - .claude/commands/grd/insert-experiment.md
    - .claude/commands/grd/remove-experiment.md
    - commands/grd/add-experiment.md
    - commands/grd/insert-experiment.md
    - commands/grd/remove-experiment.md
  modified:
    - .claude/commands/grd/help.md
    - commands/grd/help.md
    - .claude/agents/grd-planner.md
    - .claude/agents/grd-roadmapper.md
    - .claude/get-research-done/workflows/execute-plan.md

key-decisions:
  - "Complete rename of roadmap management commands to experiment terminology"
  - "Updated all cross-references in active code (excluding historical .planning/phases/ docs)"

patterns-established:
  - "All phase-related commands now use experiment terminology consistently"

# Metrics
duration: 6min
completed: 2026-02-02
---

# Phase 15 Plan 03: Roadmap Management Command Renames Summary

**Renamed add-phase, insert-phase, and remove-phase to add-experiment, insert-experiment, and remove-experiment with complete cross-reference updates**

## Performance

- **Duration:** 6 min
- **Started:** 2026-02-02T02:06:52Z
- **Completed:** 2026-02-02T02:12:57Z
- **Tasks:** 3
- **Files modified:** 12

## Accomplishments
- Renamed all three roadmap management commands to experiment terminology
- Updated frontmatter and descriptions in all command files (both .claude and commands directories)
- Updated all cross-references across active codebase
- Zero orphan references remain in active system files

## Task Commits

Each task was committed atomically:

1. **Task 1: Rename add-phase to add-experiment** - `daa2a5c` (refactor)
2. **Task 2: Rename insert-phase to insert-experiment** - `d2efe33` (refactor)
3. **Task 3: Rename remove-phase to remove-experiment** - `78a57f8` (refactor)

## Files Created/Modified
- `.claude/commands/grd/add-experiment.md` - Add experiment to end of current study
- `.claude/commands/grd/insert-experiment.md` - Insert urgent experiment between existing experiments
- `.claude/commands/grd/remove-experiment.md` - Remove future experiment and renumber
- `commands/grd/add-experiment.md` - Mirror of add-experiment command
- `commands/grd/insert-experiment.md` - Mirror of insert-experiment command
- `commands/grd/remove-experiment.md` - Mirror of remove-experiment command
- `.claude/commands/grd/help.md` - Updated command reference
- `commands/grd/help.md` - Updated command reference (mirror)
- `.claude/agents/grd-planner.md` - Updated reference to insert-experiment
- `.claude/agents/grd-roadmapper.md` - Updated reference to insert-experiment
- `.claude/get-research-done/workflows/execute-plan.md` - Updated reference to add-experiment
- `commands/grd/check-todos.md` - Updated references to add-experiment

## Decisions Made
- Maintained dual-directory structure (.claude and commands) for compatibility
- Excluded historical .planning/phases/ docs from cross-reference updates (they are historical records)
- Updated terminology to use "experiment" and "study" consistently throughout

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## Next Phase Readiness

All three roadmap management commands successfully renamed to experiment terminology. This completes the experiment-centric terminology migration for all 9 phase-related commands (3 lifecycle + 3 planning + 3 management).

Ready to proceed with remaining phases in the command rename milestone.

---
*Phase: 15-command-renames*
*Completed: 2026-02-02*
