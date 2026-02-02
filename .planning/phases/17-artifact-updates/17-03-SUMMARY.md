---
phase: 17-artifact-updates
plan: 03
subsystem: docs
tags: [command-routing, user-experience, workflow-terminology]

# Dependency graph
requires:
  - phase: 15-command-rename-batch
    provides: New command names (design-experiment, run-experiment, etc.)
  - phase: 16-command-chaining
    provides: Command routing patterns and Next Up sections
provides:
  - Consistent experiment terminology in all command routing
  - Updated Next Up sections across 7 command files
  - Research-native workflow language throughout navigation
affects: [user-experience, command-discoverability, workflow-consistency]

# Tech tracking
tech-stack:
  added: []
  patterns: [experiment-routing-terminology]

key-files:
  created: []
  modified:
    - commands/grd/add-experiment.md
    - commands/grd/insert-experiment.md
    - commands/grd/new-project.md
    - commands/grd/design-experiment.md
    - commands/grd/validate-results.md
    - commands/grd/run-experiment.md
    - commands/grd/progress.md

key-decisions:
  - "Experiment terminology in routing but not process steps: User-facing navigation uses 'Experiment', internal process documentation retains 'Phase' for technical clarity"
  - "Section headers remain as-is: Status banners like 'PHASE {Z} VERIFIED' unchanged - only Next Up routing updated"

patterns-established:
  - "Next Up routing pattern: **Experiment {N}: {Name}** for all forward navigation"
  - "Completion section headers: **Experiment {Z} Complete** for progress milestones"

# Metrics
duration: 2min
completed: 2026-02-02
---

# Phase 17 Plan 03: Artifact Updates - Next Up Sections Summary

**All command routing now uses "Experiment" terminology - 7 command files updated with consistent experiment-based navigation**

## Performance

- **Duration:** 2 min
- **Started:** 2026-02-02T17:07:27Z
- **Completed:** 2026-02-02T17:09:00Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- Updated 4 simple routing commands (add-experiment, insert-experiment, new-project, design-experiment)
- Updated 3 complex routing commands with multiple Next Up sections (validate-results, run-experiment, progress)
- Consistent "Experiment {N}" pattern across all forward navigation
- Section headers updated where appropriate ("Experiment {Z} Complete")

## Task Commits

Each task was committed atomically:

1. **Task 1: Update simple routing commands** - `26e594d` (docs)
2. **Task 2: Update complex routing commands** - `b166239` (docs)

**Plan metadata:** (pending - to be committed)

## Files Created/Modified
- `commands/grd/add-experiment.md` - "Experiment {N}: {description}" in Next Up
- `commands/grd/insert-experiment.md` - "Experiment {decimal_phase}: {description}" in Next Up
- `commands/grd/new-project.md` - "Experiment 1: [Experiment Name]" in Next Up
- `commands/grd/design-experiment.md` - "Execute Experiment {X}" in Next Up
- `commands/grd/validate-results.md` - "Experiment {Z+1}: {Name}" in Route A Next Up
- `commands/grd/run-experiment.md` - "Experiment {Z+1}: {Name}" in Route A, "complete the experiment" text
- `commands/grd/progress.md` - All Next Up sections and completion headers use Experiment terminology

## Decisions Made

**Scope of updates:**
- Updated Next Up sections (user-facing routing suggestions)
- Updated section headers in progress.md ("Experiment {Z} Complete")
- Updated description text ("complete the experiment")
- Did NOT update process steps, examples, or status banners (e.g., "PHASE {Z} VERIFIED ✓")

Rationale: User sees "Experiment" in navigation flow. Internal process documentation and status banners can retain "Phase" for technical clarity without confusing the workflow experience.

**Section header approach:**
- Updated progress.md section headers ("## ✓ Experiment {Z} Complete")
- Left validate-results.md and run-experiment.md status banners unchanged ("PHASE {Z} VERIFIED ✓")

Rationale: Progress command is navigational, status banners are informational state indicators. Both valid, context-dependent.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - all grep patterns matched expected locations, all edits applied cleanly.

## Next Phase Readiness

- All command routing uses consistent experiment terminology
- User experience now fully research-native across navigation flow
- Ready for phase completion and version bump
- No blockers for subsequent artifact updates

---
*Phase: 17-artifact-updates*
*Completed: 2026-02-02*
