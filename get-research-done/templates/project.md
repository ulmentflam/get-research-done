# PROJECT.md Template

Template for `.planning/PROJECT.md` — the living research context document.

<template>

```markdown
# [Project Name]

## Research Question

[The core question this study investigates — clear, specific, answerable]

## Study Overview

[Current accurate description — 2-3 sentences. What does this research investigate and why?
Use the user's language and framing. Update whenever reality drifts from this description.]

## Expected Contribution

[The ONE insight, method, or finding that makes this research worthwhile.
One sentence that drives prioritization when tradeoffs arise.]

## Hypotheses

### Validated

<!-- Tested and confirmed through experiments. -->

(None yet — experiments validate)

### Active

<!-- Current hypotheses being tested. -->

- [ ] [Hypothesis 1]
- [ ] [Hypothesis 2]
- [ ] [Hypothesis 3]

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent scope creep. -->

- [Exclusion 1] — [why]
- [Exclusion 2] — [why]

## Research Environment

- **Data:** [what's available, what's needed]
- **Compute:** [resources available]
- **Timeline:** [any deadlines]
- **Prior work:** [relevant background]

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| [Choice] | [Why] | [✓ Good / ⚠️ Revisit / — Pending] |

---
*Last updated: [date] after [trigger]*
```

</template>

<guidelines>

**Research Question:**
- The core question this study investigates
- Clear, specific, and answerable
- Should be falsifiable through experiments
- Update if the research direction shifts fundamentally

**Study Overview:**
- Current accurate description of the research
- 2-3 sentences capturing what you're investigating and why
- Use the user's words and framing
- Update when the research evolves beyond this description

**Expected Contribution:**
- The single most important insight or finding
- Everything else can fail; this must be answered
- Drives prioritization when tradeoffs arise
- Rarely changes; if it does, it's a significant pivot

**Hypotheses — Validated:**
- Hypotheses tested and confirmed through experiments
- Format: `- ✓ [Hypothesis] — [experiment/study]`
- These are locked — changing them requires explicit discussion

**Hypotheses — Active:**
- Current hypotheses being tested
- These are predictions until validated through experiments
- Move to Validated when confirmed, Out of Scope if refuted

**Hypotheses — Out of Scope:**
- Explicit boundaries on what we're not investigating
- Always include reasoning (prevents scope creep)
- Includes: considered and rejected, deferred to future studies, explicitly excluded

**Research Environment:**
- Data available and data needed
- Compute resources and constraints
- Timeline and deadlines
- Prior work and relevant background

**Key Decisions:**
- Significant choices that affect future work
- Add decisions as they're made throughout the project
- Track outcome when known:
  - ✓ Good — decision proved correct
  - ⚠️ Revisit — decision may need reconsideration
  - — Pending — too early to evaluate

**Last Updated:**
- Always note when and why the document was updated
- Format: `after Phase 2` or `after v1.0 milestone`
- Triggers review of whether content is still accurate

</guidelines>

<evolution>

PROJECT.md evolves throughout the research lifecycle.

**After each experiment:**
1. Hypotheses refuted? → Move to Out of Scope with findings
2. Hypotheses confirmed? → Move to Validated with experiment reference
3. New hypotheses emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "Study Overview" still accurate? → Update if drifted

**After each study:**
1. Full review of all sections
2. Expected Contribution check — still the right focus?
3. Audit Out of Scope — reasons still valid?
4. Update Research Environment with current state

</evolution>

<brownfield>

For existing codebases or prior experiments:

1. **Map codebase first** via `/grd:map-codebase`

2. **Infer Validated hypotheses** from existing work:
   - What has the codebase already demonstrated?
   - What patterns are established?
   - What's clearly working and validated?

3. **Gather Active hypotheses** from user:
   - Present inferred current state
   - Ask what they want to investigate next

4. **Initialize:**
   - Validated = inferred from existing code/experiments
   - Active = user's hypotheses for this study
   - Out of Scope = boundaries user specifies
   - Research Environment = includes current codebase state

</brownfield>

<state_reference>

STATE.md references PROJECT.md:

```markdown
## Project Reference

See: .planning/PROJECT.md (updated [date])

**Expected contribution:** [One-liner from Expected Contribution section]
**Current focus:** [Current experiment name]
```

This ensures Claude reads current PROJECT.md context.

</state_reference>
