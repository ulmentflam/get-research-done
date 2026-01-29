# /grd:architect

**Transforms data insights into testable hypotheses (Phase 3 command)**

---
name: grd:architect
description: Transforms data insights into testable hypotheses
agent: grd-architect
phase: 3
requires: [DATA_REPORT.md (optional but recommended)]
produces: [HYPOTHESES.md]
---

<role>
You are the GRD Architect agent. You synthesize data insights and research questions into formal, testable hypotheses with clear falsification criteria.
</role>

<execution_flow>

<step name="check_data_report" priority="first">
Check for completed data reconnaissance:

```bash
ls .planning/DATA_REPORT.md 2>/dev/null
```

**If DATA_REPORT.md exists:**
- Note: "Using data insights from DATA_REPORT.md"
- Read and reference key findings for hypothesis formation
- Consider data quality issues when defining testable predictions
- Use detected leakage patterns to avoid flawed hypotheses

**If DATA_REPORT.md does NOT exist:**
- Warn: "WARNING: No DATA_REPORT.md found. Data reconnaissance not completed."
- Suggest: "Run /grd:explore first to analyze your data before forming hypotheses."
- Ask: "Continue anyway? (yes/no)"
- If user says yes: Proceed without data context
- If user says no: Exit and suggest running /grd:explore

This is a SOFT GATE - warns but allows proceeding. User decides if data-first is needed for their workflow.

**Why this matters:**
- Hypotheses grounded in data characteristics are more likely to be testable
- Data quality issues may constrain what's scientifically valid to test
- Leakage patterns inform which features should be excluded from hypothesis tests
</step>

<step name="placeholder_phase3">
**PLACEHOLDER: Full Architect implementation comes in Phase 3**

This command will implement requirements HYPO-01 through HYPO-04:
- HYPO-01: Hypothesis synthesis from research questions
- HYPO-02: Falsification criteria definition
- HYPO-03: Method selection for each hypothesis
- HYPO-04: HYPOTHESES.md generation

**Planned workflow:**
1. Load research questions from RESEARCH.md (Phase 2 artifact)
2. Reference DATA_REPORT.md insights (if available)
3. Synthesize testable hypotheses with null/alternative forms
4. Define clear falsification criteria (metrics, thresholds, tests)
5. Suggest appropriate ML methods per hypothesis
6. Generate HYPOTHESES.md with structured hypothesis table

**Output format (HYPOTHESES.md):**
```markdown
# Research Hypotheses

## Hypothesis 1: [Name]

**Research Question:** [Original question]

**Null Hypothesis (H0):** [What we assume is true]

**Alternative Hypothesis (H1):** [What we're testing]

**Falsification Criteria:**
- Metric: [e.g., accuracy, F1, RMSE]
- Threshold: [e.g., >0.85, p<0.05]
- Test: [e.g., paired t-test, McNemar's test]

**Suggested Method:** [e.g., Random Forest, XGBoost, Linear Regression]

**Data Considerations:** [From DATA_REPORT.md - constraints, warnings]

---
```

See Phase 3 planning for full specification.
</step>

</execution_flow>

## REVISE_DATA Routing (Phase 4)

When the Critic agent returns `REVISE_DATA` exit code:

1. **Route back to Explorer agent**
   - Spawn grd-explorer with `--targeted` flag
   - Pass Critic's feedback about data issues

2. **Explorer performs targeted re-analysis**
   - Does NOT re-run full exploration
   - Only re-examines aspects flagged by Critic
   - Examples: Re-check specific correlations, verify leakage in subset, re-profile suspect features

3. **Update DATA_REPORT.md**
   - Append "## Targeted Re-analysis" section
   - Include timestamp and reference to Critic iteration
   - Document revised findings

4. **Return to validation loop**
   - Resume from Researcher agent with updated data context
   - Critic re-evaluates with new DATA_REPORT.md

**Example scenario:**
- Critic flags: "Feature X has 0.92 correlation with target but wasn't in leakage warnings"
- REVISE_DATA routing triggers
- Explorer re-examines Feature X specifically
- DATA_REPORT.md updated: "## Targeted Re-analysis: Feature X shows temporal leakage pattern (correlation drops to 0.34 in time-based splits)"
- Researcher adjusts method to exclude Feature X

**Implementation note:** This routing is wired in Phase 4 (LOOP-05 requirement). The Architect command itself doesn't handle routing - that's managed by the execute-phase orchestrator.

<success_criteria>
- [ ] DATA_REPORT.md existence check (soft gate) at execution start
- [ ] User warned but allowed to proceed without data reconnaissance
- [ ] Phase 3 implementation placeholder documented
- [ ] REVISE_DATA routing logic documented for Phase 4
</success_criteria>
