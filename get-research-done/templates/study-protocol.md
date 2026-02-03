# Study Protocol Template

Template for `.planning/STUDY_PROTOCOL.md` — experiment structure for a research study.

<template>

```markdown
# Study Protocol: v[X.Y] [Study Name]

**Research Question:** [the core question]
**Hypotheses:** [count] primary, [count] secondary
**Created:** [date]

## Overview

[2-3 sentence summary of what this study investigates and expected impact]

## Experiments

### Experiment [N]: [Descriptive Name]

**Hypothesis:** HYP-[XX] — [hypothesis statement]

**Method:**
[Detailed description of the approach]

**Baselines:**
- [Baseline 1]: [expected performance]
- [Baseline 2]: [expected performance]

**Data:**
- Dataset: [name/source]
- Split: [train/val/test sizes]
- Preprocessing: [key steps]

**Metrics:**
- Primary: [metric name]
- Secondary: [metric names]

**Success Criteria:**
- [ ] [metric] [comparison] [threshold]
- [ ] [additional criterion]

**Expected Outcome:**
[What we expect to find and why]

**Controls:**
- [Confound 1]: [how controlled]
- [Confound 2]: [how controlled]

**Pitfalls to Avoid:**
- [Pitfall from research]: [prevention strategy]

---

### Experiment [N+1]: [Descriptive Name]

**Hypothesis:** HYP-[XX] — [hypothesis statement]

**Method:**
[Detailed description of the approach]

**Baselines:**
- [Baseline 1]: [expected performance]

**Data:**
- Dataset: [name/source]
- Split: [train/val/test sizes]

**Metrics:**
- Primary: [metric name]

**Success Criteria:**
- [ ] [metric] [comparison] [threshold]

**Expected Outcome:**
[What we expect to find and why]

**Controls:**
- [Confound]: [how controlled]

**Depends On:**
- Experiment [N]: [what's needed from it]

---

## Experiment Dependencies

```
Exp [N] ──→ Exp [N+1] (needs baseline)
       └──→ Exp [N+2] (needs hyperparameters)

Exp [N+3] (independent)
```

## Execution Order

| Wave | Experiments | Rationale |
|------|-------------|-----------|
| 1 | [N], [N+3] | Independent, can run parallel |
| 2 | [N+1], [N+2] | Depend on Wave 1 results |

## Resource Estimates

| Experiment | Compute | Data | Time |
|------------|---------|------|------|
| [N] | [GPU hours] | [GB] | [estimate] |
| [N+1] | [GPU hours] | [GB] | [estimate] |

## Evaluation Protocol

### Standard Protocol (All Experiments)

1. **Seeds:** Run with seeds [0, 1, 2, 3, 4]
2. **Tuning:** Hyperparameters tuned on validation set only
3. **Reporting:** Mean ± std across seeds
4. **Significance:** p < 0.05 with Bonferroni correction

### Checkpoints

- [ ] After each experiment: Update HYPOTHESES.md status
- [ ] After each experiment: Log results in experiment notebook
- [ ] After wave completion: Review before proceeding

## Progress

| # | Experiment | Status | Result | Notes |
|---|------------|--------|--------|-------|
| [N] | [Name] | Pending | — | — |
| [N+1] | [Name] | Pending | — | — |

---
*Study protocol for v[X.Y]*
*Last updated: [date]*
```

</template>

<guidelines>

**Experiments:**
- One experiment per hypothesis (generally)
- Include all details needed to execute
- Reference pitfalls from research

**Dependencies:**
- Make dependencies explicit
- Plan execution waves
- Enable parallelization where possible

**Success Criteria:**
- Specific and measurable
- Aligned with hypothesis
- Multiple criteria for robust validation

**Progress Tracking:**
- Update as experiments complete
- Track status and results
- Note any deviations or issues

</guidelines>
