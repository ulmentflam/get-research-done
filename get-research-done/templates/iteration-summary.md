# Iteration Summary Template

Template for `experiments/archive/YYYY-MM-DD_hypothesis_name/ITERATION_SUMMARY.md`.

Collapses all iteration attempts into a single summary document when archiving.

---

## File Template

```markdown
# Iteration Summary: {{hypothesis_name}}

**Total Iterations:** {{N}}
**Date Range:** {{first_run_date}} to {{last_run_date}}
**Outcome:** Archived (hypothesis abandoned)

## Iteration History

| # | Run | Date | Verdict | Confidence | Key Metric | Notes |
|---|-----|------|---------|------------|------------|-------|
| 1 | run_001_baseline | YYYY-MM-DD | REVISE_METHOD | MEDIUM | F1=0.72 | Initial attempt |
| 2 | run_002_tuned | YYYY-MM-DD | REVISE_METHOD | MEDIUM | F1=0.76 | Hyperparameter tuning |
| 3 | run_003_final | YYYY-MM-DD | ESCALATE | LOW | F1=0.78 | Limit reached |

## Metric Trend

**Best achieved:** {{metric}}={{best_value}}
**Target:** {{threshold}}
**Gap:** {{best_value - threshold}}
**Trend:** {{improving|stagnant|degrading}}

## Verdict Distribution

- PROCEED: {{count}}
- REVISE_METHOD: {{count}}
- REVISE_DATA: {{count}}
- ESCALATE: {{count}}

## Key Observations

{{Summary of what was tried and why it didn't work}}

## Preserved Artifacts

- Final run: {{run_NNN_description}}/
- All CRITIC_LOG.md files (merged or individual)
- Final SCORECARD.json

---

*Summary generated on archive. See ARCHIVE_REASON.md for human rationale.*
```

---

## Usage Notes

**Field descriptions:**

- **hypothesis_name:** Human-readable name from OBJECTIVE.md "what" section
- **N:** Total iteration count (number of runs attempted)
- **first_run_date:** Timestamp from earliest run directory
- **last_run_date:** Timestamp from final run directory
- **Outcome:** Always "Archived (hypothesis abandoned)" for this template

**Iteration History table:**

Populate from all run directories in experiments/:
- **#:** Sequential iteration number (1, 2, 3...)
- **Run:** Run directory name (run_001_baseline, run_002_tuned, etc.)
- **Date:** Extraction date from CRITIC_LOG.md or directory timestamp
- **Verdict:** Critic verdict (PROCEED, REVISE_METHOD, REVISE_DATA, ESCALATE)
- **Confidence:** Critic confidence level (HIGH, MEDIUM, LOW)
- **Key Metric:** Primary metric value from SCORECARD.json (e.g., "F1=0.72")
- **Notes:** Brief description of what was tried (from run README.md or CRITIC_LOG.md)

**Metric Trend section:**

- **Best achieved:** Highest value attained across all iterations for primary metric
- **Target:** Threshold from OBJECTIVE.md for that metric
- **Gap:** Difference (best_value - threshold), show with sign
- **Trend:** Classify based on metric progression:
  - "improving" if values consistently increase across iterations
  - "stagnant" if values plateau or fluctuate without progress
  - "degrading" if values decrease (rare but possible with overfitting)

**Verdict Distribution:**

Count occurrences of each verdict type across all runs:
```bash
# Example calculation
PROCEED=$(grep -h "^\*\*Verdict:\*\* PROCEED" experiments/run_*/CRITIC_LOG.md | wc -l)
REVISE_METHOD=$(grep -h "^\*\*Verdict:\*\* REVISE_METHOD" experiments/run_*/CRITIC_LOG.md | wc -l)
REVISE_DATA=$(grep -h "^\*\*Verdict:\*\* REVISE_DATA" experiments/run_*/CRITIC_LOG.md | wc -l)
ESCALATE=$(grep -h "^\*\*Verdict:\*\* ESCALATE" experiments/run_*/CRITIC_LOG.md | wc -l)
```

**Key Observations section:**

Synthesize learnings from all iterations. Extract from:
- CRITIC_LOG.md strengths/weaknesses across runs
- Patterns in metric progression
- What approaches were attempted (architectures, hyperparameters, data transformations)
- Why none succeeded (common failure mode)

Examples:
- "All iterations struggled with class imbalance (99.2% negative). Resampling techniques (SMOTE, undersampling) did not improve recall."
- "Metric progression stagnated after run 2. Runs 3-5 showed no improvement despite hyperparameter changes, suggesting architectural limitation."
- "Data leakage warnings in DATA_REPORT.md were confirmed. Removing leaked features in run 4-5 caused significant performance drop, revealing hypothesis depended on invalid signal."

**Preserved Artifacts section:**

List what's kept in the archive:
- Final run directory (moved from experiments/)
- CRITIC_LOG.md files (individual or merged)
- Final SCORECARD.json
- ARCHIVE_REASON.md (user rationale)
- This ITERATION_SUMMARY.md

**Example populated template:**

```markdown
# Iteration Summary: Ensemble Methods for Fraud Detection

**Total Iterations:** 5
**Date Range:** 2026-01-15 to 2026-01-30
**Outcome:** Archived (hypothesis abandoned)

## Iteration History

| # | Run | Date | Verdict | Confidence | Key Metric | Notes |
|---|-----|------|---------|------------|------------|-------|
| 1 | run_001_baseline | 2026-01-15 | REVISE_METHOD | MEDIUM | F1=0.52 | Initial ensemble (RF+GBM) |
| 2 | run_002_smote | 2026-01-18 | REVISE_METHOD | MEDIUM | F1=0.56 | Added SMOTE resampling |
| 3 | run_003_weighted | 2026-01-22 | REVISE_METHOD | MEDIUM | F1=0.58 | Class weight optimization |
| 4 | run_004_reduced | 2026-01-25 | REVISE_METHOD | LOW | F1=0.57 | Feature reduction (237→15) |
| 5 | run_005_final | 2026-01-30 | ESCALATE | LOW | F1=0.58 | Limit reached |

## Metric Trend

**Best achieved:** F1=0.58
**Target:** 0.85
**Gap:** -0.27
**Trend:** stagnant (plateaued at 0.56-0.58 after run 2)

## Verdict Distribution

- PROCEED: 0
- REVISE_METHOD: 4
- REVISE_DATA: 0
- ESCALATE: 1

## Key Observations

All five iterations struggled with severe class imbalance (99.2% negative class, N=120 positive examples). Despite trying multiple approaches (SMOTE resampling, class weighting, feature reduction), F1 score plateaued at 0.56-0.58, far below the target of 0.85.

**What was tried:**
- Run 1: Baseline ensemble (Random Forest + Gradient Boosting)
- Run 2: SMOTE oversampling to balance classes
- Run 3: Class weight optimization (weighted loss functions)
- Run 4: Feature reduction (237→15 features) to reduce overfitting
- Run 5: Combined approach with focal loss

**Common failure mode:**
All iterations achieved high precision (>0.90) but poor recall (<0.42), indicating the model learned to be conservative due to extreme class imbalance. Resampling techniques introduced artificial patterns that didn't generalize. The fundamental issue is insufficient positive examples (N=120) for the hypothesis to be testable with ensemble methods.

**Critic's repeated concerns:**
- "Limited positive examples prevent ensemble diversity"
- "High precision but poor recall suggests severe class imbalance"
- "Feature space too large relative to positive sample size"

## Preserved Artifacts

- Final run: run_005_final/ (complete snapshot with DECISION.md)
- All CRITIC_LOG.md files (archived individually in final_run/)
- Final SCORECARD.json (F1=0.58, composite=0.64)
- ARCHIVE_REASON.md (user rationale for abandonment)
- This ITERATION_SUMMARY.md

---

*Summary generated on archive. See ARCHIVE_REASON.md for human rationale.*
```

---

## Integration

This template is used by `/grd:evaluate` command in Phase 5 (Archive Handling) when user selects "Archive" decision.

**Inputs:**
- All run directories in experiments/ (run_001, run_002, ...)
- CRITIC_LOG.md from each run (verdict, confidence, recommendations)
- SCORECARD.json from each run (metrics, composite score)
- OBJECTIVE.md (hypothesis, target thresholds)

**Generation logic:**

```bash
# Collect all runs
RUNS=$(ls -1d experiments/run_* | sort)
TOTAL=$(echo "$RUNS" | wc -l | tr -d ' ')

# Extract date range
FIRST_DATE=$(stat -f "%Sm" -t "%Y-%m-%d" $(echo "$RUNS" | head -1))
LAST_DATE=$(stat -f "%Sm" -t "%Y-%m-%d" $(echo "$RUNS" | tail -1))

# Build iteration history table
for run in $RUNS; do
  VERDICT=$(grep "^\*\*Verdict:\*\*" "$run/CRITIC_LOG.md" | head -1 | awk '{print $2}')
  CONFIDENCE=$(grep "^\*\*Confidence:\*\*" "$run/CRITIC_LOG.md" | head -1 | awk '{print $2}')
  METRIC=$(jq -r '.metrics[0] | "\(.name)=\(.value)"' "$run/metrics/SCORECARD.json")
  NOTES=$(head -1 "$run/README.md" | sed 's/^# //')
  echo "| $i | $(basename $run) | $DATE | $VERDICT | $CONFIDENCE | $METRIC | $NOTES |"
done

# Calculate metric trend
BEST_METRIC=$(jq -s 'map(.metrics[0].value) | max' experiments/run_*/metrics/SCORECARD.json)
TARGET=$(jq -r '.metrics[0].threshold' .planning/OBJECTIVE.md)
GAP=$(echo "$BEST_METRIC - $TARGET" | bc)

# Determine trend (simplified)
if [ "$GAP" -lt -0.10 ]; then
  TREND="stagnant (far from target)"
else
  TREND="improving (but insufficient)"
fi
```

**Output:**
- experiments/archive/YYYY-MM-DD_hypothesis_slug/ITERATION_SUMMARY.md
- Referenced by ARCHIVE_REASON.md in same directory
- Provides historical context for negative result
