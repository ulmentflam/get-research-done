# Phase 3: Hypothesis Synthesis - Context

**Gathered:** 2026-01-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Transform data insights (DATA_REPORT.md) into testable scientific hypotheses. Output OBJECTIVE.md with context, hypothesis statement, success metrics, constraints, baselines, and falsification criteria. Users can also bring their own hypothesis and bypass the Architect entirely.

</domain>

<decisions>
## Implementation Decisions

### Hypothesis Structure
- Flexible prose format with required elements (what, why, expected outcome) — not a rigid scientific template
- Architect proposes one hypothesis at a time; user can iterate or request alternatives
- Both synthesis modes: Architect can auto-propose from DATA_REPORT.md findings OR user can guide with their own direction
- User can bypass Architect entirely and write OBJECTIVE.md directly
- References to DATA_REPORT.md findings are optional (nice for traceability, not enforced)

### Success Metrics
- Both absolute thresholds and relative improvements allowed — user picks per hypothesis
- Multiple weighted metrics supported — composite score determines success
- Architect proposes weights; user approves/adjusts
- Evaluation methodology (k-fold CV, holdout, etc.) must be specified upfront in OBJECTIVE.md
- Metrics that require human judgment trigger human evaluation gate
- Final success = weighted average of metrics (no individual pass/fail thresholds required)

### Baseline Requirements
- Either run your own baseline OR cite literature values — just need a comparison point
- Baseline definition is NOT required, but system warns if missing
- Cached baseline results allowed if config unchanged — no need to re-run each time

### Falsification Criteria
- Both quantitative and qualitative criteria allowed; prefer quantitative when possible
- When falsification criteria are met, Critic decides routing (REVISE_DATA, REVISE_METHOD, or hand off to human)

### Claude's Discretion
- Whether hypothesis scope warrants single or multiple experiment runs
- Whether to include constraints section based on hypothesis complexity
- Whether to include explicit non-goals section when ambiguity is likely
- Statistical significance requirements based on experiment type
- Whether to include tiered success targets (pass/good/excellent)
- Simple vs strong baseline recommendations based on hypothesis
- Symmetric vs asymmetric falsification thresholds
- Graded failure tracking vs binary

</decisions>

<specifics>
## Specific Ideas

- Architect should feel like a research advisor: proposes, explains reasoning, accepts user override
- OBJECTIVE.md should be readable by someone unfamiliar with the codebase — self-contained context
- Evaluation methodology upfront prevents p-hacking and post-hoc metric selection

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-hypothesis-synthesis*
*Context gathered: 2026-01-28*
