# Phase 11: Terminology Rename - Context

**Gathered:** 2026-01-31
**Status:** Ready for planning

<domain>
## Phase Boundary

Rename 6 lifecycle commands from GSD-style terminology to research-centric GRD terminology. Update all internal references (agent prompts, templates, documentation) to use new names consistently. The rename mapping is fixed per ROADMAP.md.

</domain>

<decisions>
## Implementation Decisions

### Command naming
- `new-milestone` → `new-study` — confirmed
- `complete-milestone` → `complete-study` — confirmed
- `discuss-phase` → `scope-study` — confirmed (scope emphasizes defining boundaries)
- `plan-phase` → `plan-study` — confirmed
- `execute-phase` → `run-study` — confirmed (short, active, familiar from "run experiments")
- `verify-work` → `validate-study` — confirmed (emphasizes validating results met goals)

### Internal consistency
- Update ALL references — agent prompts, templates, and docs use new terminology
- Replace "phase" with "study" everywhere (ROADMAP, STATE, plan files)
- Replace "milestone" with "version" for version groupings (v1.0, v1.1)
- Example: "Phase 11" becomes "Study 11", "Milestone History" becomes "Version History"

### Terminology boundaries
- "study" = individual research unit (what was "phase")
- "version" = release grouping (what was "milestone")
- Core research commands unchanged: `explore`, `architect`, `research`, `evaluate`, `graduate`

### Claude's Discretion
- Order of file updates during implementation
- How to handle any edge cases in terminology (compound terms, etc.)

</decisions>

<specifics>
## Specific Ideas

No specific requirements — standard find-and-replace approach with comprehensive coverage.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 11-terminology-rename*
*Context gathered: 2026-01-31*
