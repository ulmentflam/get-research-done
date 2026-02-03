# Baselines Research Template

Template for `.planning/research/BASELINES.md` — state-of-the-art and baseline methods for comparison.

<template>

```markdown
# Baselines Research

**Research Question:** [the core question being investigated]
**Researched:** [date]
**Confidence:** [HIGH/MEDIUM/LOW]

## State of the Art

### Current Best Methods

| Method | Performance | Dataset/Benchmark | Year | Notes |
|--------|-------------|-------------------|------|-------|
| [name] | [metric: value] | [benchmark] | [year] | [key insight] |
| [name] | [metric: value] | [benchmark] | [year] | [key insight] |
| [name] | [metric: value] | [benchmark] | [year] | [key insight] |

### Performance Trends

- **5 years ago:** [typical performance]
- **Current SOTA:** [best performance]
- **Expected ceiling:** [theoretical/practical limits]

## Baseline Methods

### Simple Baselines (Always Include)

| Baseline | Expected Performance | Why Include |
|----------|---------------------|-------------|
| Random | [expected] | Lower bound sanity check |
| Majority class | [expected] | Class imbalance baseline |
| [domain-specific simple] | [expected] | [rationale] |

### Standard Baselines (Compare Against)

| Baseline | Expected Performance | Implementation |
|----------|---------------------|----------------|
| [established method] | [expected] | [library/paper reference] |
| [established method] | [expected] | [library/paper reference] |

### Strong Baselines (Beat These)

| Baseline | Performance | Complexity | Notes |
|----------|-------------|------------|-------|
| [recent method] | [metric: value] | [high/medium/low] | [key characteristics] |
| [recent method] | [metric: value] | [high/medium/low] | [key characteristics] |

## Benchmark Datasets

| Dataset | Size | Task | Standard Splits | Notes |
|---------|------|------|-----------------|-------|
| [name] | [N samples] | [task type] | [train/val/test] | [considerations] |
| [name] | [N samples] | [task type] | [train/val/test] | [considerations] |

## Minimum Bar for Contribution

To make a meaningful contribution in this area:

- **Must beat:** [baseline] by [margin] on [metric]
- **Should compare against:** [methods list]
- **Standard evaluation:** [protocol description]

## Gap Analysis

| Gap | Current SOTA | Potential | Opportunity |
|-----|--------------|-----------|-------------|
| [limitation] | [current state] | [what's possible] | [how to exploit] |
| [limitation] | [current state] | [what's possible] | [how to exploit] |

## Reproduction Notes

### Verified Implementations

| Method | Implementation | Verified? | Notes |
|--------|----------------|-----------|-------|
| [method] | [library/repo] | [yes/no] | [gotchas] |
| [method] | [library/repo] | [yes/no] | [gotchas] |

### Common Reproduction Issues

- [Issue 1]: [how to avoid]
- [Issue 2]: [how to avoid]

## Sources

- [Paper/benchmark] — [what was learned]
- [Leaderboard/repo] — [current standings]
- [Context7/docs] — [what was verified]

---
*Baselines research for: [research question]*
*Researched: [date]*
```

</template>

<guidelines>

**State of the Art:**
- Include specific numbers with metrics
- Note which benchmark/dataset
- Track performance trends over time

**Baseline Methods:**
- Always include simple baselines (sanity checks)
- Include standard baselines (fair comparison)
- Include strong baselines (meaningful contribution)

**Minimum Bar:**
- Be explicit about what constitutes a contribution
- Include margin of improvement needed
- Specify evaluation protocol

**Gap Analysis:**
- Identify opportunities for improvement
- Focus on gaps relevant to the research question
- Consider practical constraints

</guidelines>
