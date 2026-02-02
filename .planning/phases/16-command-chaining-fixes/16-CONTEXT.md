# Phase 16: Command Chaining Fixes - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Commands route to each other correctly using new experiment-based terminology throughout the workflow. This includes next-step suggestions after command completion, error messages when prerequisites are missing, consistent flag patterns, and replacing all milestone terminology with study terminology.

</domain>

<decisions>
## Implementation Decisions

### Next-step suggestions
- Format: Primary suggestion + 2-3 alternatives below
- Primary is outcome-aware (validation fails → re-run; passes → next step)
- Include utility commands (pause-work, add-todo) when contextually appropriate
- Evaluate with "Seal" decision → primary suggestion is `/grd:graduate`
- Always suggest `/clear first → fresh context window` before context-heavy commands
- Show `--skip-*` variants only when research/context already exists
- `new-study` auto-routes to `/grd:design-experiment 1`
- `run-experiment` outcome-dependent: all pass → validate-results; failures → re-run or debug

### Error/edge messages
- Missing experiment: "No such experiment. Available experiments: 15, 16, 17..."
- Missing prerequisites: Direct command suggestion format — "No plan found. Run /grd:design-experiment 16 first."
- Gap terminology: Use "missing" instead of "gaps" — "3 missing requirements"
- Legacy artifacts: Explain migration — "Found 'phase' in STATE.md. GRD now uses 'experiment'. Update recommended."

### Flag consistency
- Claude's discretion on --gaps vs --gaps-only standardization
- Claude's discretion on which commands benefit from skip flags
- Short flags for common operations (like -g/--gaps, -v/--verbose)
- Deprecated flags: Silent acceptance — old flags work without warning

### Milestone→Study mapping
- `audit-study` checks both completion status AND whether hypotheses have conclusions
- Claude's discretion on MILESTONES.md handling (archive, migrate, or delete)
- `new-study` prompts for hypotheses but allows skipping to define later
- Replace 'milestone' with 'study' universally — clean terminology throughout

### Claude's Discretion
- Exact --gaps vs --gaps-only standardization choice
- Which commands benefit from additional skip flags
- MILESTONES.md handling approach (archive vs migrate vs delete)

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 16-command-chaining-fixes*
*Context gathered: 2026-02-02*
