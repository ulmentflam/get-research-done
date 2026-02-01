# Phase 13: Accessible Insights - Context

**Gathered:** 2026-02-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Generate plain English data insights for business analyst audience without code or jargon. Full technical DATA_REPORT.md saved to file, plain English summary displayed with "What This Means" for every statistic. Actionable recommendations and LLM prompts for further exploration included.

</domain>

<decisions>
## Implementation Decisions

### Explanation style
- Action-oriented tone: "23% missing — you'll need to decide: drop rows, fill values, or investigate why"
- Use real-world analogies to help non-technical readers understand stats
- Include technical terms with inline translation: "Standard deviation (how spread out): 15.2 — values typically range ±15 from average"
- Every statistic gets a "What This Means" explanation, even basic ones like row count

### Recommendation depth
- Specific next steps, not generic guidance: "For the 23% missing in 'income', try: (1) check if missingness correlates with other columns, (2) consider median imputation"
- Severity indicators with flags: "🚨 Critical: Data leakage detected" vs "⚠️ Note: Minor skewness in age"
- Positive framing when no action needed: "Distribution looks healthy — no concerns"
- Reference specific columns with examples: "The 'transaction_date' column has future dates (e.g., row 234: 2027-03-15)"

### Output structure
- Executive summary first: TL;DR at top, then detailed sections ("5 things to know about this data")
- Length scales with data complexity (Claude decides based on findings)
- Heavily optimized for skimming: bold key findings, bullet points, headlines that tell the story
- Both console output (Rich formatting) AND saved to INSIGHTS_SUMMARY.md for sharing

### LLM prompts
- Mix of "dig deeper" investigation prompts and "what if" analysis prompts based on findings
- 3-5 total prompts, focused on highest-value questions
- Generic prompts that work with any LLM (ChatGPT, Claude, etc.)

### Claude's Discretion
- Whether prompts are fully self-contained or assume context (pick based on complexity)
- Exact analogies to use for each statistical concept
- How much detail in explanations based on finding complexity

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

*Phase: 13-accessible-insights*
*Context gathered: 2026-02-01*
