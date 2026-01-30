# Archive Reason Template

Template for documenting failed/abandoned hypotheses in `experiments/archive/YYYY-MM-DD_hypothesis_name/ARCHIVE_REASON.md`.

---

## File Template

```markdown
# Archive Reason: {{hypothesis_name}}

**Archived:** {{ISO_8601_timestamp}}
**Original Hypothesis:** {{hypothesis_statement_from_objective}}
**Final Iteration:** {{N}} of {{limit}}
**Final Verdict:** {{ESCALATE|REVISE_METHOD_limit|REVISE_DATA_unresolved}}

## Why This Failed

{{user_rationale_required}}

## What We Learned

{{Insights from failed attempts - to be filled by user}}

- Key finding 1
- Key finding 2
- Key finding 3

## What Would Need to Change

{{Conditions under which this might work - to be filled by user}}

- Required change 1
- Required change 2
- Required change 3

## Final Metrics

| Metric | Best Value | Target | Gap |
|--------|------------|--------|-----|
| {{metric}} | {{best_achieved}} | {{threshold}} | {{difference}} |

## Iteration Timeline

See: `ITERATION_SUMMARY.md` for detailed history of all attempts.

**Summary:**
- Total runs: {{N}}
- Verdict distribution: {{PROCEED: X, REVISE_METHOD: Y, REVISE_DATA: Z, ESCALATE: W}}
- Best composite score: {{best_score}} (needed: {{threshold}})

---

*This negative result is preserved to prevent future researchers from repeating this approach without the necessary conditions.*

---

**Archive location:** experiments/archive/{{YYYY-MM-DD}}_{{hypothesis_slug}}/
**Decision recorded:** human_eval/decision_log.md
```

---

## Usage Notes

**Field descriptions:**

- **hypothesis_name:** Human-readable name extracted from OBJECTIVE.md "what" section
- **hypothesis_slug:** Filename-safe version (spaces→underscores, lowercase, alphanumeric only)
- **ISO_8601_timestamp:** Format YYYY-MM-DDTHH:MM:SSZ (UTC time)
- **hypothesis_statement_from_objective:** Full "what/why/expected" from OBJECTIVE.md
- **N:** Final iteration count from run directory
- **limit:** Iteration limit (default 5, or custom from --limit flag)
- **Final Verdict:** Reason for archival (ESCALATE, REVISE_METHOD limit reached, REVISE_DATA unresolved)

**Why This Failed (REQUIRED):**

This is the most critical section. User must provide substantive explanation:
- What was attempted
- Why it didn't work
- What blocked success
- Any insights about the approach

Examples:
- "Data quality issues prevented reliable model training. Missing values in key features caused high variance."
- "Hypothesis was too ambitious given available data. Sample size (N=500) insufficient for complex ensemble methods."
- "Leakage detection revealed fundamental data collection flaw that cannot be corrected without re-collection."

**What We Learned (user fills):**

Insights that emerged from failed attempts. Examples:
- "Feature X has stronger predictive power than initially assumed"
- "Class imbalance >90% requires specialized techniques beyond standard methods"
- "Temporal drift in data makes cross-validation unreliable"

**What Would Need to Change (user fills):**

Conditions for future success. Examples:
- "Collect 10x more data (N=5000+) to support ensemble complexity"
- "Fix data pipeline to prevent leakage at source"
- "Reformulate as binary classification instead of multi-class"

**Final Metrics table:**

- Show best values achieved across ALL iterations (not just final)
- Include gap calculation (target - best_achieved)
- Order by importance (primary metric first)

**Example populated template:**

```markdown
# Archive Reason: Ensemble Methods for Fraud Detection

**Archived:** 2026-01-30T15:45:00Z
**Original Hypothesis:** Ensemble methods will improve F1 score over single models by combining predictions from random forest, gradient boosting, and neural networks.
**Final Iteration:** 5 of 5
**Final Verdict:** REVISE_METHOD_limit

## Why This Failed

After 5 iterations with different ensemble configurations, we could not achieve the target F1 score of 0.85. The fundamental issue is severe class imbalance (99.2% negative class) combined with limited positive examples (N=120). Ensemble methods require sufficient positive examples to learn diverse patterns, but our dataset is too imbalanced for this approach to work effectively.

All iterations showed high precision (>0.90) but poor recall (<0.40), resulting in F1 scores between 0.52-0.58. Attempts to address this through resampling (SMOTE, undersampling) introduced artificial patterns that didn't generalize to the test set.

## What We Learned

- Class imbalance of 99%+ requires specialized loss functions (focal loss) rather than ensemble complexity
- Resampling techniques (SMOTE) work poorly with high-dimensional data (237 features)
- Single model (gradient boosting) with class weights performed nearly as well as ensembles (F1: 0.56 vs 0.58)
- Feature importance analysis revealed only 15 features have meaningful signal

## What Would Need to Change

- Collect 10x more positive examples (N=1200+) to support ensemble diversity
- Reduce feature space to top 15-20 features to prevent overfitting on noise
- Use focal loss or cost-sensitive learning instead of standard ensemble methods
- Consider anomaly detection approaches instead of classification
- Re-evaluate hypothesis: perhaps single model is sufficient given data constraints

## Final Metrics

| Metric | Best Value | Target | Gap |
|--------|------------|--------|-----|
| f1_score | 0.58 | 0.85 | -0.27 |
| precision | 0.92 | 0.80 | +0.12 |
| recall | 0.42 | 0.80 | -0.38 |

## Iteration Timeline

See: `ITERATION_SUMMARY.md` for detailed history of all attempts.

**Summary:**
- Total runs: 5
- Verdict distribution: PROCEED: 0, REVISE_METHOD: 5, REVISE_DATA: 0, ESCALATE: 0
- Best composite score: 0.64 (needed: 0.80)

---

*This negative result is preserved to prevent future researchers from repeating this approach without the necessary conditions.*

---

**Archive location:** experiments/archive/2026-01-30_ensemble_methods_fraud_detection/
**Decision recorded:** human_eval/decision_log.md
```

---

## Integration

This template is used by `/grd:evaluate` command in Phase 5 (Archive Handling) when user selects "Archive" decision.

**Inputs:**
- OBJECTIVE.md (hypothesis statement, metrics, thresholds)
- All SCORECARD.json files across runs (for best metrics)
- All CRITIC_LOG.md files (for verdict history)
- User rationale (REQUIRED from confirmation prompt)
- Iteration metadata (count, limit, final verdict)

**Outputs:**
- experiments/archive/YYYY-MM-DD_hypothesis_slug/ARCHIVE_REASON.md (this template)
- Referenced by ITERATION_SUMMARY.md in same directory
- Logged in human_eval/decision_log.md

**Archive directory structure:**
```
experiments/archive/YYYY-MM-DD_hypothesis_name/
├── ARCHIVE_REASON.md          # This template (why it failed)
├── ITERATION_SUMMARY.md        # Collapsed run history
└── final_run/                  # Final run directory moved from experiments/
    ├── DECISION.md
    ├── SCORECARD.json
    ├── CRITIC_LOG.md
    └── ...
```
