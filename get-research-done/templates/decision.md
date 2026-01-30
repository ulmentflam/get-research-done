# Human Decision Template

Template for per-run decision records in `experiments/run_NNN/DECISION.md`.

---

## File Template

```markdown
# Human Decision: {{run_name}}

**Timestamp:** {{ISO_8601_timestamp}}
**Hypothesis:** {{brief_hypothesis_from_objective}}
**Decision:** {{Seal|Iterate|Archive}}
**Rationale:** {{user_reasoning_if_provided}}

## Evidence Summary

**Critic Verdict:** {{PROCEED}} (Confidence: {{HIGH|MEDIUM|LOW}})
**Composite Score:** {{score}} (threshold: {{threshold}})
**Key Metric:** {{metric_name}}={{value}} (target: {{comparison}}{{threshold}})

## Metrics Detail

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| {{metric_1}} | {{value}} | {{threshold}} | {{PASS|FAIL}} |
| {{metric_2}} | {{value}} | {{threshold}} | {{PASS|FAIL}} |

## Decision Context

### For Seal
- Hypothesis validated
- Ready for production/publication
- All success criteria met

### For Iterate
- Continuing experimentation
- Direction: {{REVISE_METHOD|REVISE_DATA}} (from Critic recommendation)
- Next focus: {{specific_area}}

### For Archive
- Hypothesis abandoned
- Reason: {{user_rationale_required}}
- Preserved as negative result

---

*Decision recorded: {{ISO_8601_timestamp}}*
*Run directory: experiments/{{run_name}}/*
```

---

## Usage Notes

**Field descriptions:**

- **run_name:** Directory name (e.g., run_003_tuned) extracted from experiments/ path
- **ISO_8601_timestamp:** Format YYYY-MM-DDTHH:MM:SSZ (UTC time)
- **brief_hypothesis_from_objective:** Extract "what" statement from OBJECTIVE.md (1-2 sentences max)
- **Decision:** One of: Seal, Iterate, Archive
- **Rationale:** REQUIRED for Archive, optional for Seal/Iterate

**Evidence Summary fields:**

- **Critic Verdict:** Always "PROCEED" (required to reach human eval)
- **Confidence:** Extract from CRITIC_LOG.md (HIGH/MEDIUM/LOW)
- **Composite Score:** Weighted average from SCORECARD.json
- **threshold:** Overall threshold from OBJECTIVE.md
- **Key Metric:** Primary metric (highest weight or first in list)
- **comparison:** Operator (>, <, >=, <=, ==)

**Metrics Detail table:**

- Pull all metrics from SCORECARD.json
- Include: name, achieved value, threshold, PASS/FAIL status
- Order by weight (descending) or as defined in OBJECTIVE.md

**Decision Context sections:**

- Only populate the section matching the decision type
- For Iterate: include Critic's recommendation if available
- For Archive: user_rationale is REQUIRED

**Example populated template:**

```markdown
# Human Decision: run_003_tuned

**Timestamp:** 2026-01-30T14:35:00Z
**Hypothesis:** Ensemble methods will improve F1 score over single models
**Decision:** Seal
**Rationale:** Results demonstrate clear improvement with robust validation

## Evidence Summary

**Critic Verdict:** PROCEED (Confidence: HIGH)
**Composite Score:** 0.89 (threshold: 0.80)
**Key Metric:** f1_score=0.91 (target: >=0.85)

## Metrics Detail

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| f1_score | 0.91 | 0.85 | PASS |
| precision | 0.88 | 0.80 | PASS |
| recall | 0.94 | 0.80 | PASS |

## Decision Context

### For Seal
- Hypothesis validated
- Ready for production/publication
- All success criteria met

---

*Decision recorded: 2026-01-30T14:35:00Z*
*Run directory: experiments/run_003_tuned/*
```

---

## Integration

This template is used by `/grd:evaluate` command in Phase 4 (Decision Logging).

**Inputs:**
- OBJECTIVE.md (hypothesis, metrics, thresholds)
- SCORECARD.json (metrics values, composite score)
- CRITIC_LOG.md (verdict, confidence)
- User decision (Seal/Iterate/Archive)
- User rationale (if Archive or provided)

**Output:**
- experiments/run_NNN/DECISION.md (this template populated)
- Appended to human_eval/decision_log.md (summary entry)
