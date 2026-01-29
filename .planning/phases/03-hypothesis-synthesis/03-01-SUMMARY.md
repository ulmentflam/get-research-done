---
phase: 03-hypothesis-synthesis
plan: 01
subsystem: templates
tags: [hypothesis, objective, documentation, yaml, scientific-method]

# Dependency graph
requires:
  - phase: 02-data-reconnaissance
    provides: DATA_REPORT.md template and structure patterns
provides:
  - OBJECTIVE.md template for hypothesis documentation
  - Structured format with context, hypothesis, metrics, evaluation, baselines, falsification
  - YAML frontmatter for machine-readable validation
affects: [04-experiment-design, grd-architect]

# Tech tracking
tech-stack:
  added: []
  patterns: [hypothesis-documentation, yaml-frontmatter, scientific-rigor]

key-files:
  created: [get-research-done/templates/objective.md]
  modified: []

key-decisions:
  - "Flexible prose hypothesis format (what/why/expected) instead of rigid null/alternative structure"
  - "Weighted metrics with composite scoring (weights must sum to 1.0)"
  - "Evaluation methodology defined upfront to prevent p-hacking"
  - "Falsification criteria required (quantitative preferred, qualitative allowed)"
  - "Baseline warnings but not blocking (system warns if empty)"

patterns-established:
  - "Template structure: YAML frontmatter + markdown sections with tables"
  - "Placeholder syntax: {{variable_name}} for agent population"
  - "Self-contained context: template readable without codebase familiarity"
  - "Severity levels and thresholds: following data-report.md patterns"

# Metrics
duration: 1min
completed: 2026-01-28
---

# Phase 3 Plan 01: Template Creation Summary

**OBJECTIVE.md template with flexible hypothesis structure, weighted success metrics, evaluation methodology, baselines, and falsification criteria — designed for grd-architect agent population while supporting direct user authoring**

## Performance

- **Duration:** 1 min 14 sec
- **Started:** 2026-01-28T22:11:49Z
- **Completed:** 2026-01-28T22:13:03Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- Created comprehensive 240-line OBJECTIVE.md template with 8 major sections
- Structured YAML frontmatter for machine validation (metrics, evaluation, baseline_defined, has_falsification_criteria)
- Flexible prose hypothesis format matching CONTEXT.md decisions (not rigid scientific format)
- Weighted metrics system with composite scoring and validation notes
- Evaluation methodology section enforcing upfront strategy definition
- Falsification criteria section with quantitative/qualitative types and Critic routing guidance

## Task Commits

Each task was committed atomically:

1. **Task 1: Create OBJECTIVE.md template** - `da73e79` (feat)

## Files Created/Modified
- `get-research-done/templates/objective.md` - Hypothesis documentation template with context, hypothesis (what/why/expected), success metrics (weighted), evaluation methodology, baselines, falsification criteria, optional constraints/non-goals

## Decisions Made

**Template Structure Decisions:**
1. **Flexible prose hypothesis format** - Uses what/why/expected outcome structure instead of rigid null/alternative hypothesis format (per CONTEXT.md decision for research advisor feel)
2. **Weighted metrics with validation note** - Metrics table includes weight column with explicit note that weights must sum to 1.0 for composite scoring
3. **Evaluation methodology upfront** - Dedicated section with strategy, parameters, and justification to prevent p-hacking and post-hoc metric selection
4. **Baseline warnings not blocking** - Template includes warning note if baselines section empty, but system allows proceeding (per CONTEXT.md: baseline not required but warned)
5. **Falsification criteria required** - At least one criterion required, with types (quantitative/qualitative) and Critic routing guidance documented

**Pattern Consistency:**
- Followed data-report.md patterns: YAML-like frontmatter metadata, table formats for structured data, severity indicators, timestamp/status at top
- Used {{placeholder}} syntax throughout for agent population
- Added helpful HTML comments with examples and guidance
- Self-contained context in each section (readable without codebase knowledge)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for:**
- Phase 3 Plan 02: Architect agent implementation (can use this template)
- Phase 4: Experiment design (will read OBJECTIVE.md files created from this template)

**Template completeness:**
- All required sections present and documented
- Frontmatter designed for validation logic
- Comments provide guidance for both agent and human authors
- Follows data-report.md consistency patterns

**No blockers.**

---
*Phase: 03-hypothesis-synthesis*
*Completed: 2026-01-28*
