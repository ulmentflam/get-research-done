# Phase 12: Quick Explore - Context

**Gathered:** 2026-02-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Fast EDA command producing console summary for quick data familiarization. Primary use case is team sharing — generating a summary that can be copy-pasted into Slack/docs for stakeholder communication. Full statistical rigor deferred to `/grd:explore`.

</domain>

<decisions>
## Implementation Decisions

### Output scope
- Include visual indicators: sparkline-style distribution hints, skewness flags alongside stats
- Prominently flag data quality issues: missing values, duplicates, suspicious patterns with warning symbols
- Include data types and memory usage — useful for engineering decisions
- Analyze full data (no sampling) — accuracy matters more than speed
- Light suggestions based on findings: "Consider investigating X" style hints

### Claude's Discretion (Output scope)
- Leakage detection: determine what's feasible within speed budget (basic heuristics vs skip)
- Correlation highlights: determine if top 3-5 correlations are feasible within speed budget

### Display format
- Single flowing markdown summary — easy to copy-paste into Slack/docs
- Use color AND emoji indicators (⚠️ for warnings, ✅ for clean, colored text)
- One line per column: name | type | missing% | key stat | indicator
- TL;DR at top: 2-3 sentence prose summary ("Dataset has X rows, Y columns. Notable: high missing in Z, possible outliers in W.")

### Speed tradeoffs
- 60-second target is soft guideline — accept longer time for accuracy
- On failure: show partial results + error note (something is better than nothing)

### Claude's Discretion (Speed tradeoffs)
- Expensive computation skipping: determine best value-to-time ratio
- Caching: determine if result caching adds value for repeated runs

### Warning behavior
- Header banner: "⚡ Quick Explore — Run full explore for rigorous analysis"
- Data quality concerns flagged inline with same indicator style as regular findings
- Always end with suggestion: "Run /grd:explore for complete analysis"
- Architect integration: prominent warning if only quick-explore was run ("Only quick-explore run — hypotheses based on shallow analysis")

</decisions>

<specifics>
## Specific Ideas

- Output should be copy-paste ready for Slack/team communication
- Balance between informative and scannable — team members need to grok it quickly
- Warnings about shallow analysis should be clear but not overwhelming

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 12-quick-explore*
*Context gathered: 2026-02-01*
