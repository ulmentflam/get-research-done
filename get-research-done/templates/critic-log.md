# Critic Evaluation: {{run_name}}

**Timestamp:** {{timestamp}}
**Iteration:** {{iteration_number}}
**Objective:** {{brief_hypothesis}}

---

## Verdict

**Decision:** {{PROCEED | REVISE_METHOD | REVISE_DATA | ESCALATE}}
**Confidence:** {{HIGH | MEDIUM | LOW}}

## Reasoning

{{explanation_of_routing_decision}}

{{context_for_why_this_verdict_makes_sense}}

{{evidence_supporting_decision}}

## Metrics Summary

| Metric | Value | Threshold | Comparison | Result |
|--------|-------|-----------|------------|--------|
| {{metric_name}} | {{value}} | {{threshold}} | {{>|<|=}} | {{PASS|FAIL}} |

**Composite Score:** {{weighted_average}} (threshold: {{composite_threshold}})

**Baseline Comparison:** {{if_baseline_defined}}

| Metric | Baseline | Actual | Improvement | % Change |
|--------|----------|--------|-------------|----------|
| {{metric_name}} | {{baseline_value}} | {{actual_value}} | {{delta}} | {{percentage}} |

## Strengths

{{list_of_what_experiment_does_well}}

Examples:
- Implementation correctly uses stratified k-fold as specified in OBJECTIVE.md
- Random seed set to 42 for reproducibility
- Clear documentation in README.md
- Hyperparameters well-documented in config.yaml
- Code quality is high with proper error handling
- Training/validation curves show healthy learning behavior

## Weaknesses

{{list_of_issues_or_concerns}}

Examples:
- F1 score (0.78) below threshold (0.80)
- Train-test gap of 0.08 suggests mild overfitting
- Learning rate may be too high (training loss plateaus early)
- Missing validation curves in output
- Evaluation methodology doesn't match OBJECTIVE.md (used holdout instead of k-fold)
- Random seed not set (non-reproducible results)

## Recommendations

{{list_of_specific_actionable_suggestions}}

**For REVISE_METHOD verdicts:**
- Reduce learning rate from 0.1 to 0.01
- Add dropout layer with rate 0.3 to reduce overfitting
- Increase training epochs from 50 to 100 (training curve not plateaued)
- Add early stopping with patience=10 to prevent overfitting
- Fix data split bug on line 45 in train.py
- Add missing metrics to output (currently missing F1 score)

**For REVISE_DATA verdicts:**
- Investigate feature 'transaction_id' for potential leakage (dominates feature importance)
- Re-analyze temporal features for leakage (results suggest future information used)
- Verify target column is correct (baseline outperforms model significantly)
- Check for train-test overlap (metrics suggest data contamination)
- Investigate data quality issues (high variance across folds)

**For PROCEED verdicts:**
- Document validation approach in final report
- Consider additional robustness checks before production
- Monitor for drift in production deployment

**For ESCALATE verdicts:**
- Human decision required (see evidence package below)
- Consider revising hypothesis or success criteria
- May need to collect additional data
- Strategic pivot may be necessary

## Investigation Notes

{{notes_from_scientific_skepticism_checks}}

### Suspicious Success Check

{{result_of_investigation_for_unusually_high_metrics}}

- Metrics: {{list_metrics_and_values}}
- Task complexity: {{assessment_of_difficulty}}
- Assessment: {{plausible | suspicious | highly_suspicious}}
- Reasoning: {{why}}

### Train-Test Gap

- Train metric: {{value}}
- Validation metric: {{value}}
- Gap: {{delta}}
- Assessment: {{acceptable | moderate_concern | high_concern}}
- Reasoning: {{why}}

### Reproducibility

- Random seed set: {{yes|no}}
- Dependencies documented: {{yes|no}}
- Data references recorded: {{yes|no}}
- Assessment: {{reproducible | partially_reproducible | non_reproducible}}

### Data Integrity

{{if_DATA_REPORT_referenced}}

- Leakage features excluded: {{yes|no|N/A}}
- Class imbalance handled: {{yes|no|N/A}}
- Temporal splits used if needed: {{yes|no|N/A}}
- Assessment: {{concerns_none | concerns_minor | concerns_major}}

### Code Quality

- Evaluation matches OBJECTIVE.md: {{yes|no}}
- Data split correct: {{yes|no}}
- Hyperparameters documented: {{yes|no}}
- Error handling present: {{yes|no}}
- Assessment: {{good | acceptable | needs_improvement}}

## Trend Analysis

**Iteration Trend:** {{improving | stagnant | degrading | first_run}}

{{comparison_with_previous_iterations_if_available}}

**Historical Performance:**

| Iteration | Composite Score | Key Changes | Verdict |
|-----------|----------------|-------------|---------|
| 1 | {{value}} | {{change_description}} | {{verdict}} |
| 2 | {{value}} | {{change_description}} | {{verdict}} |
| 3 (current) | {{value}} | {{change_description}} | {{verdict}} |

**Trend Assessment:**

{{detailed_analysis_of_progress_across_iterations}}

Examples:
- "Metrics improving steadily (+0.02 per iteration). Current trajectory suggests threshold will be reached in 1-2 more iterations."
- "Metrics stagnant across 3 iterations despite different hyperparameters. May indicate fundamental limitation."
- "Metrics degrading. Recent changes counterproductive—consider reverting to iteration 1 approach."

**Cycle Detection:**

{{if_same_verdict_repeated}}

- Same verdict: {{verdict}} repeated {{N}} times
- Assessment: {{no_cycle | potential_cycle | cycle_detected}}
- Action: {{continue | escalate | try_different_approach}}

## Next Steps

{{based_on_verdict}}

### If PROCEED (HIGH confidence)
Ready for quantitative evaluation by Evaluator agent.

**Action:** Run `/grd:evaluate` to generate SCORECARD.json

**What happens next:**
- Evaluator will run comprehensive benchmark suite
- Results will be compared against OBJECTIVE.md criteria
- SCORECARD.json will be generated for human evaluation gate

### If PROCEED (MEDIUM confidence)
Metrics meet criteria but minor concerns noted.

**Action:** Proceed to Evaluator with caveats

**Caveats:**
{{list_of_minor_concerns_to_monitor}}

### If PROCEED (LOW confidence)
**HUMAN GATE REQUIRED**

Metrics pass thresholds but concerns exist:
{{list_of_concerns}}

**Question for human:**
Should we proceed to Evaluator despite concerns, or investigate further?

**Options:**
1. Proceed to Evaluator (accept concerns)
2. REVISE_METHOD (address concerns first)
3. ESCALATE (need strategic decision)

### If REVISE_METHOD
Address implementation issues and re-run experiment.

**Action:** Implement recommendations above, then run experiment again

**Specific fixes needed:**
{{prioritized_list_of_fixes}}

**Expected impact:**
{{what_should_improve_if_fixes_applied}}

**Estimated effort:** {{low|medium|high}}

### If REVISE_DATA
Return to data exploration with specific concerns.

**Action:** Run `/grd:explore` with focus areas

**Concerns to investigate:**
{{list_of_specific_data_concerns}}

**What to look for:**
{{guidance_for_data_re_analysis}}

**Updates needed:**
- Append findings to DATA_REPORT.md
- Update OBJECTIVE.md if constraints change
- Re-run experiment with corrected data

### If ESCALATE
Human decision required—cannot determine clear path forward.

**Reason for escalation:** {{cycle_detected | ambiguous_root_cause | iteration_limit | strategic_decision_needed}}

**Evidence Package:**

#### Iteration History
{{summary_of_all_attempts}}

#### Conflicting Signals
{{description_of_ambiguity_or_contradiction}}

#### Attempted Resolutions
{{what_was_tried_and_why_it_didnt_work}}

#### Recommendation
{{suggested_strategic_direction_or_questions_for_human}}

**Human Options:**
1. Continue with more iterations (increase limit)
2. Revise hypothesis or success criteria (update OBJECTIVE.md)
3. Archive hypothesis as disproven (document learnings)
4. Return to data collection (need more/better data)
5. Strategic pivot (fundamentally different approach)

## Appendix

### Falsification Criteria Status

{{if_falsification_criteria_defined_in_OBJECTIVE}}

| Criterion | Status | Notes |
|-----------|--------|-------|
| {{criterion_name}} | {{not_met | approaching | met}} | {{details}} |

**Assessment:** {{hypothesis_still_viable | approaching_falsification | falsified}}

### Experiment Metadata

- **Run directory:** {{path_to_run_NNN}}
- **Code files:** {{list_of_key_files}}
- **Configuration:** {{path_to_config_yaml_or_none}}
- **Documentation:** {{path_to_README_or_none}}
- **Training time:** {{duration_in_seconds_or_minutes}}
- **Compute resources:** {{cpu|gpu|tpu}} - {{details}}

### References

- **OBJECTIVE.md:** `.planning/OBJECTIVE.md`
- **DATA_REPORT.md:** {{path_or_none}}
- **Previous iterations:** {{paths_to_previous_CRITIC_LOGs}}

---

*Critique by grd-critic*
*Agent version: GRD Critic v1.0*
*Referenced: .planning/OBJECTIVE.md*
