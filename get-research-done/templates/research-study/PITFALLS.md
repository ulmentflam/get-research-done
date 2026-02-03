# Pitfalls Research Template

Template for `.planning/research/PITFALLS.md` — common mistakes and confounds in the research domain.

<template>

```markdown
# Pitfalls Research

**Research Question:** [the core question being investigated]
**Researched:** [date]
**Confidence:** [HIGH/MEDIUM/LOW]

## Data Leakage

### Common Leakage Sources

| Leakage Type | How It Happens | Detection | Prevention |
|--------------|----------------|-----------|------------|
| [type] | [mechanism] | [how to detect] | [how to prevent] |
| [type] | [mechanism] | [how to detect] | [how to prevent] |
| [type] | [mechanism] | [how to detect] | [how to prevent] |

### Domain-Specific Leakage

| Source | Risk Level | Experiment Affected |
|--------|------------|---------------------|
| [specific to this domain] | [HIGH/MEDIUM/LOW] | [which experiments] |

## Statistical Pitfalls

### Common Errors

| Error | Description | Correct Approach |
|-------|-------------|------------------|
| Multiple comparisons | [how it manifests] | [correction method] |
| P-hacking | [how it manifests] | [pre-registration] |
| Small sample size | [how it manifests] | [power analysis] |
| [domain-specific] | [how it manifests] | [solution] |

### Misleading Results

| Pitfall | Warning Signs | What to Do |
|---------|---------------|------------|
| [overfitting to test] | [indicators] | [prevention] |
| [dataset artifacts] | [indicators] | [prevention] |
| [confounding variables] | [indicators] | [prevention] |

## Experimental Design Pitfalls

### Setup Errors

| Error | Impact | Prevention |
|-------|--------|------------|
| [improper splits] | [what goes wrong] | [correct approach] |
| [data contamination] | [what goes wrong] | [correct approach] |
| [unfair comparison] | [what goes wrong] | [correct approach] |

### Baseline Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| [weak baselines] | [inflates results] | [include strong baselines] |
| [unfair hyperparameter tuning] | [biased comparison] | [equal tuning budget] |
| [cherry-picked runs] | [misleading variance] | [report all runs] |

## Implementation Pitfalls

### Common Bugs

| Bug | Symptom | Fix |
|-----|---------|-----|
| [implementation issue] | [how it manifests] | [solution] |
| [library misuse] | [how it manifests] | [solution] |
| [numerical issue] | [how it manifests] | [solution] |

### Reproducibility Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| [different results] | [random seeds] | [fix and document seeds] |
| [platform differences] | [hardware/software] | [specify environment] |
| [version drift] | [library updates] | [pin versions] |

## Domain-Specific Pitfalls

### [Research Area] Specific

| Pitfall | Why It's Specific | Prevention |
|---------|-------------------|------------|
| [domain pitfall] | [domain context] | [domain solution] |
| [domain pitfall] | [domain context] | [domain solution] |

## Interpretation Pitfalls

| Pitfall | Example | Correct Interpretation |
|---------|---------|------------------------|
| [over-claiming] | [specific case] | [appropriate claim] |
| [causation vs correlation] | [specific case] | [appropriate language] |
| [generalization] | [specific case] | [appropriate scope] |

## Prevention Checklist

### Before Running Experiments

- [ ] Data leakage audit completed
- [ ] Splits created BEFORE any exploration
- [ ] Baselines selected and justified
- [ ] Evaluation protocol pre-registered
- [ ] Statistical tests chosen upfront

### During Experiments

- [ ] Seeds documented for all runs
- [ ] Intermediate results logged
- [ ] Anomalies investigated immediately
- [ ] Ablations planned systematically

### Before Claiming Results

- [ ] Multiple runs completed
- [ ] Statistical significance verified
- [ ] Ablations support conclusions
- [ ] Alternative explanations considered
- [ ] Claims match evidence scope

## Sources

- [Paper on pitfalls] — [specific warnings]
- [Reproducibility study] — [common issues found]
- [Domain best practices] — [recommendations]

---
*Pitfalls research for: [research question]*
*Researched: [date]*
```

</template>

<guidelines>

**Data Leakage:**
- Be specific about leakage mechanisms
- Include detection strategies
- Note which experiments are affected

**Statistical Pitfalls:**
- Cover common errors
- Provide actionable prevention
- Include domain-specific issues

**Implementation Pitfalls:**
- Warn about common bugs
- Include reproducibility issues
- Note library-specific gotchas

**Prevention Checklist:**
- Actionable items at each stage
- Can be used as actual checklist
- Covers entire experiment lifecycle

</guidelines>
