# Metrics Research Template

Template for `.planning/research/METRICS.md` — evaluation standards and metrics for the research domain.

<template>

```markdown
# Metrics Research

**Research Question:** [the core question being investigated]
**Researched:** [date]
**Confidence:** [HIGH/MEDIUM/LOW]

## Primary Metrics

### Main Evaluation Metrics

| Metric | Formula/Definition | When to Use | Interpretation |
|--------|-------------------|-------------|----------------|
| [metric name] | [how computed] | [use case] | [what values mean] |
| [metric name] | [how computed] | [use case] | [what values mean] |
| [metric name] | [how computed] | [use case] | [what values mean] |

### Recommended Primary Metric

**For this study:** [metric name]

**Rationale:**
- [why this metric fits the research question]
- [how it handles edge cases]
- [community acceptance]

## Secondary Metrics

| Metric | Purpose | When to Report |
|--------|---------|----------------|
| [metric] | [what it measures] | [always/conditionally] |
| [metric] | [what it measures] | [always/conditionally] |

## Statistical Significance

### Recommended Tests

| Comparison Type | Test | Assumptions | Threshold |
|-----------------|------|-------------|-----------|
| [A vs B] | [test name] | [requirements] | p < [value] |
| [multiple comparisons] | [test name] | [requirements] | [correction method] |

### Sample Size Requirements

| Effect Size | Required N | Power |
|-------------|------------|-------|
| Small (d=0.2) | [N] | 0.80 |
| Medium (d=0.5) | [N] | 0.80 |
| Large (d=0.8) | [N] | 0.80 |

### Confidence Intervals

- **Report:** [what intervals to compute]
- **Method:** [bootstrap/analytical/etc]
- **Runs:** [number of seeds/folds]

## Evaluation Protocol

### Standard Protocol

1. **Data split:** [train/val/test strategy]
2. **Hyperparameter tuning:** [on which split]
3. **Final evaluation:** [how many runs, what to report]
4. **Reporting format:** [mean ± std, median, etc]

### Cross-Validation

| Strategy | When to Use | Folds |
|----------|-------------|-------|
| [k-fold] | [condition] | [k] |
| [stratified] | [condition] | [k] |
| [leave-one-out] | [condition] | [N] |

## Metric Pitfalls

| Pitfall | Example | How to Avoid |
|---------|---------|--------------|
| [metric gaming] | [specific case] | [prevention] |
| [misleading comparison] | [specific case] | [correct approach] |
| [statistical error] | [specific case] | [correct approach] |

## Domain-Specific Considerations

### [Domain] Metrics

| Metric | Domain Meaning | Standard Threshold |
|--------|----------------|-------------------|
| [domain metric] | [interpretation] | [acceptable range] |
| [domain metric] | [interpretation] | [acceptable range] |

### What NOT to Report

| Metric | Why Avoid | Better Alternative |
|--------|-----------|-------------------|
| [problematic metric] | [specific issue] | [use this instead] |

## Reproducibility Checklist

- [ ] Random seeds documented
- [ ] Number of runs specified
- [ ] Variance/CI reported
- [ ] Statistical tests applied
- [ ] Evaluation splits specified
- [ ] Metric implementations verified

## Sources

- [Paper/standard] — [metrics defined]
- [Benchmark docs] — [evaluation protocol]
- [Statistical reference] — [test recommendations]

---
*Metrics research for: [research question]*
*Researched: [date]*
```

</template>

<guidelines>

**Primary Metrics:**
- Choose metrics aligned with the research question
- Explain interpretation (higher=better, ranges, etc)
- Note community standards

**Statistical Significance:**
- Specify exact tests to use
- Include correction for multiple comparisons
- Define significance thresholds upfront

**Evaluation Protocol:**
- Be explicit about data splits
- Specify number of runs/seeds
- Define reporting format

**Metric Pitfalls:**
- Warn about metric gaming
- Note misleading comparisons
- Prevent common statistical errors

</guidelines>
