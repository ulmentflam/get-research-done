# Hypotheses Template

Template for `.planning/HYPOTHESES.md` — testable hypotheses for a research study.

<template>

```markdown
# Study Hypotheses

**Study:** v[X.Y] [Study Name]
**Research Question:** [the core question being investigated]
**Created:** [date]

## Primary Hypotheses

Must test in this study:

- [ ] **HYP-01**: [Specific, falsifiable claim]
  - **Success criteria:** [metric] [comparison] [threshold]
  - **Method:** [how to test]
  - **Controls:** [what to control for]

- [ ] **HYP-02**: [Specific, falsifiable claim]
  - **Success criteria:** [metric] [comparison] [threshold]
  - **Method:** [how to test]
  - **Controls:** [what to control for]

- [ ] **HYP-03**: [Specific, falsifiable claim]
  - **Success criteria:** [metric] [comparison] [threshold]
  - **Method:** [how to test]
  - **Controls:** [what to control for]

## Secondary Hypotheses

Test if time/resources permit:

- [ ] **HYP-04**: [Specific, falsifiable claim]
  - **Success criteria:** [metric] [comparison] [threshold]
  - **Depends on:** [which primary hypothesis]

- [ ] **HYP-05**: [Specific, falsifiable claim]
  - **Success criteria:** [metric] [comparison] [threshold]
  - **Depends on:** [which primary hypothesis]

## Baselines

Reference points for comparison:

- **BASELINE-01**: [Method name]
  - **Expected performance:** [metric: value]
  - **Source:** [paper/implementation]

- **BASELINE-02**: [Method name]
  - **Expected performance:** [metric: value]
  - **Source:** [paper/implementation]

## Deferred Hypotheses

Explicitly out of scope for this study:

- **DEFER-01**: [Hypothesis]
  - **Why deferred:** [reasoning]
  - **Future study:** [when to revisit]

## Hypothesis Quality Checklist

For each hypothesis, verify:

- [ ] **Specific:** States exactly what will be measured
- [ ] **Falsifiable:** Can be proven wrong with data
- [ ] **Testable:** We have the data/resources to test it
- [ ] **Independent:** Minimal coupling to other hypotheses
- [ ] **Measurable:** Clear success/failure criteria

## Traceability

| HYP-ID | Experiment | Status | Result |
|--------|------------|--------|--------|
| HYP-01 | — | Pending | — |
| HYP-02 | — | Pending | — |
| HYP-03 | — | Pending | — |

---
*Hypotheses for study v[X.Y]*
*Last updated: [date]*
```

</template>

<guidelines>

**Primary vs Secondary:**
- Primary hypotheses MUST be tested
- Secondary are optional if time permits
- Deferred are explicitly out of scope

**Good Hypotheses:**
- Specific: "Model X outperforms Y by >5% on metric Z"
- NOT vague: "Model X is better"

**Success Criteria:**
- Include metric name
- Include comparison (>, <, =, within range)
- Include specific threshold

**Traceability:**
- Maps hypotheses to experiments
- Updated as study progresses
- Shows status and results

</guidelines>
