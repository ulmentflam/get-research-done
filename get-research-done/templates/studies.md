# Studies Template

Template for `.planning/STUDIES.md` — archive of completed studies and version history.

<template>

```markdown
# Studies Archive

**Project:** [Project Name]
**Current Study:** v[X.Y] [Study Name]
**Total Experiments:** [running count]

## Active Study

**v[X.Y]: [Study Name]**
- Status: In Progress
- Experiments: [N] to [M]
- Hypotheses: [count] primary, [count] secondary
- Started: [date]

See: `STUDY_PROTOCOL.md`, `HYPOTHESES.md`

---

## Completed Studies

<details>
<summary><strong>v[X.Y-1]: [Previous Study Name]</strong> — [outcome summary]</summary>

**Research Question:** [what was investigated]

**Hypotheses Tested:**
- [x] HYP-01: [hypothesis] — **CONFIRMED** ([result])
- [ ] HYP-02: [hypothesis] — **REJECTED** ([result])
- [~] HYP-03: [hypothesis] — **INCONCLUSIVE** ([result])

**Key Findings:**
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

**Experiments:** [N] to [M]
- Exp [N]: [name] — [outcome]
- Exp [N+1]: [name] — [outcome]

**Impact:**
- [What this enabled]
- [How it changed direction]

**Artifacts:**
- `archive/v[X.Y-1]/STUDY_PROTOCOL.md`
- `archive/v[X.Y-1]/HYPOTHESES.md`
- `archive/v[X.Y-1]/notebooks/`

**Completed:** [date]

</details>

<details>
<summary><strong>v[X.Y-2]: [Earlier Study Name]</strong> — [outcome summary]</summary>

[Same structure...]

</details>

---

## Validated Findings

Findings confirmed across studies:

| Finding | Study | Confidence | Notes |
|---------|-------|------------|-------|
| [finding] | v[X.Y] | HIGH | [context] |
| [finding] | v[X.Y] | MEDIUM | [context] |

## Open Questions

Questions raised but not yet answered:

| Question | Raised In | Priority | Notes |
|----------|-----------|----------|-------|
| [question] | v[X.Y] | HIGH | [context] |
| [question] | v[X.Y] | LOW | [context] |

## Study Timeline

| Version | Name | Experiments | Duration | Outcome |
|---------|------|-------------|----------|---------|
| v1.0 | [name] | 1-5 | [dates] | [summary] |
| v1.1 | [name] | 6-8 | [dates] | [summary] |
| v2.0 | [name] | 9-15 | [dates] | In Progress |

## Experiment Index

Quick lookup for all experiments across studies:

| # | Name | Study | Hypothesis | Result |
|---|------|-------|------------|--------|
| 1 | [name] | v1.0 | HYP-01 | Confirmed |
| 2 | [name] | v1.0 | HYP-02 | Rejected |
| ... | ... | ... | ... | ... |

---
*Studies archive for [project name]*
*Last updated: [date]*
```

</template>

<guidelines>

**Active Study:**
- Always shows current study at top
- Links to detailed protocol files
- Quick status overview

**Completed Studies:**
- Collapsed by default (keeps file scannable)
- Full hypothesis outcomes with results
- Key findings extracted
- Links to archived artifacts

**Validated Findings:**
- Cross-study confirmed findings
- Building knowledge base
- Confidence levels

**Open Questions:**
- Track questions for future studies
- Prioritize research agenda
- Don't lose insights

**Experiment Index:**
- Global experiment numbering
- Quick lookup across studies
- Track cumulative progress

</guidelines>
