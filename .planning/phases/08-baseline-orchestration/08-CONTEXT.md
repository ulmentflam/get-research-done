# Phase 8: Baseline Orchestration - Context

**Gathered:** 2026-01-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Ensure baseline experiments are run before comparison experiments. This phase implements validation gates that check baseline results exist before main experiments can proceed, and handles multi-baseline scenarios where OBJECTIVE.md defines multiple comparison targets.

</domain>

<decisions>
## Implementation Decisions

### Validation timing
- Primary gate at Researcher start — check baseline exists when /grd:research runs (fail fast)
- Secondary safety check at Evaluator — verify baseline still valid when generating SCORECARD
- If OBJECTIVE.md has no baselines defined: warn but proceed ("No baselines defined — comparison will be limited")

### Baseline completeness
- Minimum requirement: metrics.json exists in baseline run directory
- Baseline must contain all metrics defined in OBJECTIVE.md (same metrics as experiment)
- If baseline used different dataset: warn about data hash mismatch but proceed
- Baseline does not need Critic PROCEED verdict or full SCORECARD — just quantitative results

### Missing baseline handling
- Block and prompt with suggested command: "Run baseline first: /grd:research --baseline <name>"
- Include baseline definition from OBJECTIVE.md in error message for clarity
- Override available via --skip-baseline flag (power users, logged warning)

### Multi-baseline scenarios
- Primary baseline required, secondary baselines optional
- Secondary baselines missing: warn and proceed ("Secondary baselines (X, Y) missing — comparison will be limited")
- SCORECARD shows comparison table with experiment vs each available baseline side-by-side

### Claude's Discretion
- Baseline validation caching strategy (re-check vs cache per session)
- Handling of malformed/incomplete metrics.json files
- How to designate primary baseline in OBJECTIVE.md (first-in-list vs explicit flag)
- Skip-baseline logging approach (STATE.md vs run metadata vs both)

</decisions>

<specifics>
## Specific Ideas

- Error messages should be actionable — show exactly what command to run
- Validation should fail fast (Researcher start) rather than late (after experiment completes)
- Multi-baseline comparison should be a table, not multiple separate sections

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 08-baseline-orchestration*
*Context gathered: 2026-01-30*
