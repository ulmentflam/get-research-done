---
name: grd:audit-study
description: Audit study completion against original hypotheses before archiving
argument-hint: "[version]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
  - Write
---

<objective>
Verify study achieved its definition of done. Check hypothesis coverage, experiment validity, and statistical rigor.

**This command IS the orchestrator.** Reads existing VERIFICATION.md files (experiments already verified during execute-phase), aggregates findings and limitations, then spawns integration checker for cross-experiment consistency.
</objective>

<execution_context>
<!-- Spawns grd-integration-checker agent which has all audit expertise baked in -->
</execution_context>

<context>
Version: $ARGUMENTS (optional — defaults to current study)

**Original Intent:**
@.planning/PROJECT.md
@.planning/HYPOTHESES.md

**Planned Work:**
@.planning/STUDY_PROTOCOL.md
@.planning/config.json (if exists)

**Completed Work:**
Glob: .planning/phases/*/*-SUMMARY.md
Glob: .planning/phases/*/*-VERIFICATION.md
</context>

<process>

## 0. Resolve Model Profile

Read model profile for agent spawning:

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Default to "balanced" if not set.

**Model lookup table:**

| Agent | quality | balanced | budget |
|-------|---------|----------|--------|
| grd-integration-checker | sonnet | sonnet | haiku |

Store resolved model for use in Task call below.

## 1. Determine Study Scope

```bash
# Get experiments in study
ls -d .planning/phases/*/ | sort -V
```

- Parse version from arguments or detect current from STUDY_PROTOCOL.md
- Identify all experiment directories in scope
- Extract study definition of done from STUDY_PROTOCOL.md
- Extract hypotheses mapped to this study from HYPOTHESES.md

## 2. Read All Experiment Verifications

For each experiment directory, read the VERIFICATION.md:

```bash
cat .planning/phases/01-*/*-VERIFICATION.md
cat .planning/phases/02-*/*-VERIFICATION.md
# etc.
```

From each VERIFICATION.md, extract:
- **Status:** passed | gaps_found
- **Hypothesis outcome:** supported | rejected | inconclusive
- **Statistical validity:** significance, effect size, confidence intervals
- **Limitations:** confounds, sample size issues
- **Reproducibility:** seeds, configurations documented

If an experiment is missing VERIFICATION.md, flag it as "unverified experiment" — this is a blocker.

## 3. Spawn Integration Checker

With experiment context collected:

```
Task(
  prompt="Check cross-experiment consistency and methodology.

Experiments: {experiment_dirs}
Hypothesis outcomes: {from VERIFICATIONs}
Methods used: {from SUMMARYs}

Verify:
- Consistent methodology across experiments
- No contradictory findings
- Statistical rigor (appropriate tests, significance)
- Reproducibility requirements met",
  subagent_type="grd-integration-checker",
  model="{integration_checker_model}"
)
```

## 4. Collect Results

Combine:
- Experiment-level outcomes and limitations (from step 2)
- Integration checker's report (methodology consistency, statistical issues)

## 5. Check Hypothesis Coverage

For each hypothesis in HYPOTHESES.md mapped to this study:
- Find testing experiment
- Check experiment verification status
- Determine: supported | rejected | inconclusive | untested

## 6. Aggregate into v{version}-STUDY-AUDIT.md

Create `.planning/v{version}-STUDY-AUDIT.md` with:

```yaml
---
study: {version}
audited: {timestamp}
status: passed | gaps_found | limitations
scores:
  hypotheses: N/M tested
  experiments: N/M completed
  statistical_rigor: N/M valid
  reproducibility: N/M documented
findings:
  supported: [HYP-IDs]
  rejected: [HYP-IDs]
  inconclusive: [HYP-IDs]
gaps:  # Critical blockers
  untested_hypotheses: [...]
  invalid_experiments: [...]
  methodology_issues: [...]
limitations:  # Non-critical, documented
  - experiment: 01-baseline
    items:
      - "Small sample size (n=100)"
      - "Single dataset evaluation"
---
```

Plus full markdown report with tables for hypotheses, experiments, statistics, limitations.

**Status values:**
- `passed` — all primary hypotheses tested, methodology valid
- `gaps_found` — critical issues exist (untested hypotheses, invalid methodology)
- `limitations` — no blockers but accumulated limitations need documentation

## 7. Present Results

Route by status (see `<offer_next>`).

</process>

<offer_next>
Output this markdown directly (not as a code block). Route based on status:

---

**If passed:**

## ✓ Study {version} — Audit Passed

**Score:** {N}/{M} hypotheses tested
**Findings:** {X} supported, {Y} rejected, {Z} inconclusive
**Report:** .planning/v{version}-STUDY-AUDIT.md

All primary hypotheses tested. Methodology validated. Results reproducible.

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Complete study** — archive findings and tag

/grd:complete-study {version}

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

---

**If gaps_found:**

## ⚠ Study {version} — Gaps Found

**Score:** {N}/{M} hypotheses tested
**Report:** .planning/v{version}-STUDY-AUDIT.md

### Untested Hypotheses

{For each untested hypothesis:}
- **{HYP-ID}: {claim}** — No experiment conducted

### Methodology Issues

{For each issue:}
- **Experiment {X}:** {issue description}

### Statistical Concerns

{For each concern:}
- **{experiment}:** {statistical issue}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Plan additional experiments** — close gaps

/grd:plan-study-gaps

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- cat .planning/v{version}-STUDY-AUDIT.md — see full report
- /grd:complete-study {version} — proceed anyway (document limitations)

───────────────────────────────────────────────────────────────

---

**If limitations (no blockers but accumulated limitations):**

## ⚡ Study {version} — Limitations Review

**Score:** {N}/{M} hypotheses tested
**Report:** .planning/v{version}-STUDY-AUDIT.md

All hypotheses tested. No critical methodology issues. Accumulated limitations need documentation.

### Limitations by Experiment

{For each experiment with limitations:}
**Experiment {X}: {name}**
- {limitation 1}
- {limitation 2}

### Total: {N} limitations across {M} experiments

───────────────────────────────────────────────────────────────

## ▶ Options

**A. Complete study** — document limitations, archive findings

/grd:complete-study {version}

**B. Run additional experiments** — address limitations

/grd:plan-study-gaps

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────
</offer_next>

<success_criteria>
- [ ] Study scope identified
- [ ] All experiment VERIFICATION.md files read
- [ ] Limitations and gaps aggregated
- [ ] Integration checker spawned for methodology consistency
- [ ] v{version}-STUDY-AUDIT.md created
- [ ] Results presented with actionable next steps
</success_criteria>
