# Research Summary Template

Template for `.planning/research/SUMMARY.md` — executive synthesis of all research findings.

<template>

```markdown
# Research Summary

**Study:** [study name/version]
**Research Question:** [the core question]
**Synthesized:** [date]

## Executive Summary

[2-3 sentence summary of key findings and recommendations]

## Key Findings

### Methods

**Recommended approach:** [primary method]
- Rationale: [why]
- Alternative: [backup method] if [condition]

**Key insight:** [most important methodological finding]

### Baselines

**Must compare against:**
1. [baseline 1] — [expected performance]
2. [baseline 2] — [expected performance]
3. [baseline 3] — [expected performance]

**Minimum bar:** Beat [baseline] by [margin] on [metric]

### Metrics

**Primary metric:** [metric] — [why chosen]
**Secondary metrics:** [list]
**Significance threshold:** p < [value] with [correction]

### Critical Pitfalls

1. **[Pitfall 1]:** [one-line summary]
   - Prevention: [how to avoid]
   - Affected experiment: [which one]

2. **[Pitfall 2]:** [one-line summary]
   - Prevention: [how to avoid]
   - Affected experiment: [which one]

3. **[Pitfall 3]:** [one-line summary]
   - Prevention: [how to avoid]
   - Affected experiment: [which one]

## Study Protocol Implications

### Suggested Experiments

Based on the research question and literature:

| # | Experiment | Tests | Method | Key Pitfall to Avoid |
|---|------------|-------|--------|---------------------|
| 1 | [name] | [hypothesis] | [from METHODS.md] | [from PITFALLS.md] |
| 2 | [name] | [hypothesis] | [from METHODS.md] | [from PITFALLS.md] |
| 3 | [name] | [hypothesis] | [from METHODS.md] | [from PITFALLS.md] |

### Experiment Dependencies

```
[Experiment 1] → [Experiment 2] (needs baseline results)
                → [Experiment 3] (needs hyperparameters)
[Experiment 4] (independent)
```

### Research Flags

| Experiment | Flag | Action Needed |
|------------|------|---------------|
| [N] | Needs additional research | [specific topic] |
| [N] | High pitfall risk | [specific concern] |
| [N] | Baseline unclear | [what to investigate] |

## Confidence Assessment

| Research Area | Confidence | Gaps |
|---------------|------------|------|
| Methods | [HIGH/MEDIUM/LOW] | [what's uncertain] |
| Baselines | [HIGH/MEDIUM/LOW] | [what's uncertain] |
| Metrics | [HIGH/MEDIUM/LOW] | [what's uncertain] |
| Pitfalls | [HIGH/MEDIUM/LOW] | [what's uncertain] |

## Quick Reference

### Before Each Experiment

1. Review pitfalls from PITFALLS.md
2. Verify baseline implementation
3. Confirm evaluation protocol

### Standard Evaluation Protocol

1. [Step 1 from METRICS.md]
2. [Step 2 from METRICS.md]
3. [Step 3 from METRICS.md]

### Go/No-Go Criteria

- **Proceed if:** [conditions met]
- **Stop and reassess if:** [warning signs]

## Source Files

| File | Key Content |
|------|-------------|
| METHODS.md | Prior approaches, experimental designs |
| BASELINES.md | SOTA, comparison methods |
| METRICS.md | Evaluation protocol, statistical tests |
| PITFALLS.md | What to avoid, prevention strategies |

---
*Research synthesis for: [study name]*
*Synthesized: [date]*
```

</template>

<guidelines>

**Executive Summary:**
- 2-3 sentences maximum
- Actionable recommendations
- Key insight that changes approach

**Key Findings:**
- One key takeaway per research area
- Concrete recommendations
- Quantitative where possible

**Study Protocol Implications:**
- Suggest experiment structure
- Note dependencies
- Flag areas needing attention

**Quick Reference:**
- Immediately useful for each experiment
- Standard protocols to follow
- Go/no-go decision criteria

</guidelines>
