# Methods Research Template

Template for `.planning/research/METHODS.md` — prior approaches and methodologies for the research domain.

<template>

```markdown
# Methods Research

**Research Question:** [the core question being investigated]
**Researched:** [date]
**Confidence:** [HIGH/MEDIUM/LOW]

## Prior Approaches

### Established Methods

| Method | Description | Strengths | Limitations |
|--------|-------------|-----------|-------------|
| [name] | [how it works] | [when it works well] | [known weaknesses] |
| [name] | [how it works] | [when it works well] | [known weaknesses] |
| [name] | [how it works] | [when it works well] | [known weaknesses] |

### Recent Advances

| Method | Year | Key Innovation | Applicability |
|--------|------|----------------|---------------|
| [name] | [year] | [what's new] | [when to use] |
| [name] | [year] | [what's new] | [when to use] |

## Experimental Designs

### Standard Protocols

| Design | Use Case | Key Requirements |
|--------|----------|------------------|
| [design type] | [when appropriate] | [what's needed] |
| [design type] | [when appropriate] | [what's needed] |

### Controls and Comparisons

- **Positive controls:** [what should always work]
- **Negative controls:** [what should never work]
- **Ablation strategy:** [how to isolate effects]

## Implementation Considerations

### Data Requirements

| Method | Data Type | Minimum Sample Size | Notes |
|--------|-----------|---------------------|-------|
| [method] | [type] | [N] | [considerations] |

### Computational Requirements

| Method | Resources Needed | Runtime Estimate |
|--------|------------------|------------------|
| [method] | [GPU/CPU/memory] | [time estimate] |

## What NOT to Do

| Anti-Pattern | Why It Fails | Better Approach |
|--------------|--------------|-----------------|
| [bad practice] | [specific problem] | [recommended alternative] |
| [bad practice] | [specific problem] | [recommended alternative] |

## Suggested Approach for This Study

Based on the research question and constraints:

1. **Primary method:** [recommendation]
   - Why: [rationale]

2. **Comparison baseline:** [recommendation]
   - Why: [rationale]

3. **Ablation studies:** [what to vary]
   - Why: [what we learn]

## Sources

- [Paper/resource] — [what was learned]
- [Paper/resource] — [what was learned]
- [Context7/docs] — [what was verified]

---
*Methods research for: [research question]*
*Researched: [date]*
```

</template>

<guidelines>

**Prior Approaches:**
- Document what's been tried before
- Include both successes and failures
- Explain WHY methods work or don't work

**Experimental Designs:**
- Focus on designs appropriate for the research question
- Include control strategies
- Note minimum requirements

**What NOT to Do:**
- Actively warn against common mistakes
- Explain the specific failure mode
- Provide actionable alternatives

**Suggested Approach:**
- Make concrete recommendations
- Justify based on project constraints
- Consider resource limitations

</guidelines>
