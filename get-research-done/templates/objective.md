# Hypothesis: {{hypothesis_title}}

**Created:** {{timestamp}}
**Phase:** 3 (Hypothesis Synthesis)
**Status:** {{draft|review|finalized}}
**Data Report:** {{path_to_data_report_or_none}}

---
metadata:
  hypothesis_id: {{unique_id}}
  version: 1
  created: {{timestamp}}
  phase: 3
  status: {{draft|review|finalized}}
  data_report: {{path_or_null}}

# Success metrics (for validation)
metrics:
  - name: {{metric_name}}
    threshold: {{value}}
    comparison: {{greater_than|less_than|equal_to}}
    weight: {{0.0-1.0}}
  # Note: Weights must sum to 1.0

# Evaluation methodology
evaluation:
  strategy: {{k-fold|stratified-k-fold|time-series-split|holdout}}
  k_folds: {{number_or_null}}
  test_size: {{proportion_or_null}}
  random_state: 42
  justification: {{why_this_strategy}}

# Baseline status
baseline_defined: {{true|false}}

# Falsification criteria
has_falsification_criteria: {{true|false}}
---

## Context

<!-- Background and motivation for this hypothesis (min 50 chars) -->

### Problem Statement

{{what_problem_or_question_is_being_addressed}}

### Motivation

{{why_this_hypothesis_matters}}

### Data Characteristics

{{data_insights_that_inform_this_hypothesis}}

<!-- If DATA_REPORT.md exists, reference specific findings:
- Missing data patterns that need handling
- Class imbalance requiring special attention
- Outliers or anomalies discovered
- Feature correlations that suggest relationships
- Leakage concerns that constrain approach
-->

### Known Constraints

{{limitations_or_constraints_that_apply}}

<!-- Examples:
- Computational resource limits
- Data quality issues from DATA_REPORT.md
- Domain-specific restrictions
- Time constraints
- Regulatory/ethical considerations
-->

## Hypothesis

<!-- Flexible prose format with required elements -->

### What

{{clear_statement_of_what_is_being_tested}}

<!-- Example: "A gradient boosting model trained on engineered temporal features will outperform a baseline logistic regression in predicting customer churn." -->

### Why

{{rationale_based_on_data_insights_or_domain_knowledge}}

<!-- Example: "DATA_REPORT.md shows strong temporal patterns in customer activity leading up to churn events. Non-linear methods like gradient boosting can capture these complex time-dependent relationships better than linear models." -->

### Expected Outcome

{{predicted_result_if_hypothesis_is_true}}

<!-- Example: "We expect to see:
- AUC-ROC improvement of at least 0.05 over baseline
- Precision at top 10% recall exceeding 0.70
- Temporally engineered features appearing in top 10 feature importances
" -->

## Success Metrics

<!-- How success is measured. Weights must sum to 1.0. -->

| Metric | Threshold | Comparison | Weight | Notes |
|--------|-----------|------------|--------|-------|
| {{metric_name_1}} | {{value}} | {{greater_than|less_than}} | {{0.0-1.0}} | {{context}} |
| {{metric_name_2}} | {{value}} | {{greater_than|less_than}} | {{0.0-1.0}} | {{context}} |

**Success Definition:** Weighted average of metrics must meet or exceed composite threshold of {{value}}.

**Metric Types Supported:**
- **Absolute thresholds**: "Accuracy >= 0.85"
- **Relative improvements**: "AUC improvement >= 0.05 over baseline"

**Note:** If any metric requires human judgment (e.g., "qualitative assessment of interpretability"), this will trigger a human evaluation gate during experimentation.

## Evaluation Methodology

<!-- Must be defined upfront to prevent p-hacking and post-hoc metric selection -->

**Strategy:** {{k-fold-cv|stratified-k-fold|time-series-split|holdout}}

**Parameters:**
- K-folds: {{number_or_null}}
- Test size: {{proportion_or_null}}
- Random state: 42 (for reproducibility)
- {{additional_parameters}}

**Justification:**

{{why_this_evaluation_strategy_is_appropriate}}

<!-- Examples:
- "Stratified k-fold (k=5) preserves class distribution in each fold, critical given 8:1 imbalance in target variable (per DATA_REPORT.md)"
- "Time-series split with 80/20 train/test prevents temporal leakage identified in DATA_REPORT.md"
- "Holdout validation (70/30 split) sufficient given large dataset size (>100k samples)"
-->

**Statistical Significance:**

{{how_statistical_significance_will_be_assessed}}

<!-- Examples:
- "95% confidence intervals via bootstrapping (1000 iterations)"
- "Paired t-test between model and baseline (p<0.05 threshold)"
- "Not applicable - deterministic evaluation"
-->

## Baselines

<!-- Comparison points. Either run your own baseline OR cite literature values. -->

| Baseline | Type | Expected Performance | Citation | Status |
|----------|------|---------------------|----------|--------|
| {{baseline_name}} | {{own_implementation|literature_citation}} | {{metric_value}} | {{paper_or_url}} | {{pending|complete}} |

**Baseline Types:**
- **own_implementation**: You will run this baseline yourself during experimentation
- **literature_citation**: Published result from paper/benchmark

**Warning:** If this section is empty, the system will flag it. Baselines provide essential context for evaluating hypothesis success.

**Caching:** Baseline results can be cached if configuration hasn't changed. No need to re-run baseline for every experiment iteration.

## Falsification Criteria

<!-- What would disprove this hypothesis? At least one criterion required. -->

| Criterion | Metric | Threshold | Type | Explanation |
|-----------|--------|-----------|------|-------------|
| {{criterion_name}} | {{metric_name}} | {{value}} | {{quantitative|qualitative}} | {{what_falsification_means}} |

**Types:**
- **quantitative** (preferred): Numeric threshold that objectively disproves hypothesis
- **qualitative**: Subjective assessment (use sparingly, document clearly)

**Falsification Meaning:**

{{what_it_means_scientifically_if_criteria_are_met}}

<!-- Example: "If the model's AUC-ROC is within 0.02 of the baseline, the hypothesis that temporal features provide meaningful signal is falsified. This would suggest that churn is not driven by time-dependent patterns, and we should explore other feature engineering approaches or problem formulations." -->

**Critic Routing:**

When falsification criteria are met, the Critic agent will decide:
- **REVISE_DATA**: Return to data exploration with specific concerns
- **REVISE_METHOD**: Adjust methodology while keeping hypothesis
- **HUMAN**: Hand off to human for strategic decision

## Constraints

<!-- Optional section: Known limitations that bound the experiment -->

{{constraints_from_data_report}}

<!-- Examples from DATA_REPORT.md:
- "30% missing values in feature X require imputation strategy"
- "Class imbalance (15:1) requires stratified sampling"
- "High correlation (0.92) between features A and B suggests redundancy"
- "Temporal leakage risk in rolling features - must compute train-only"
-->

{{resource_constraints}}

<!-- Examples:
- "Training time limited to 2 hours per experiment"
- "Memory constraint: 16GB RAM available"
- "GPU not available - CPU training only"
-->

{{scope_boundaries}}

<!-- Examples:
- "Experiment limited to tabular features only (no text/images)"
- "Single-label classification only (no multi-label)"
- "Batch inference only (no real-time serving requirements)"
-->

## Non-Goals

<!-- Optional section: Explicit exclusions to prevent scope creep -->

This hypothesis does NOT attempt to prove:

- {{explicit_exclusion_1}}
- {{explicit_exclusion_2}}

<!-- Examples:
- "This does not prove production readiness (only predictive performance)"
- "This does not address model interpretability (explainability is out of scope)"
- "This does not claim generalization beyond the current dataset"
- "This does not optimize for inference latency (accuracy-focused only)"
-->

---

*Template: get-research-done/templates/objective.md*
*To be populated by: grd-architect agent or user directly*
