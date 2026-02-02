---
name: grd:plan-study-gaps
description: Create experiments to close gaps identified by study audit
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

<objective>
Create all experiments necessary to close gaps identified by `/grd:audit-study`.

Reads STUDY-AUDIT.md, groups gaps into logical experiments, creates experiment entries in STUDY_PROTOCOL.md, and offers to plan each experiment.

One command creates all follow-up experiments — no manual `/grd:add-phase` per gap.
</objective>

<execution_context>
<!-- Spawns grd-planner agent which has all planning expertise baked in -->
</execution_context>

<context>
**Audit results:**
Glob: .planning/v*-STUDY-AUDIT.md (use most recent)

**Original intent (for prioritization):**
@.planning/PROJECT.md
@.planning/HYPOTHESES.md

**Current state:**
@.planning/STUDY_PROTOCOL.md
@.planning/STATE.md
</context>

<process>

## 1. Load Audit Results

```bash
# Find the most recent audit file
ls -t .planning/v*-STUDY-AUDIT.md 2>/dev/null | head -1
```

Parse YAML frontmatter to extract structured gaps:
- `gaps.untested_hypotheses` — hypotheses not yet tested
- `gaps.invalid_experiments` — methodology issues
- `gaps.methodology_issues` — statistical or design problems

If no audit file exists or has no gaps, error:
```
No audit gaps found. Run `/grd:audit-study` first.
```

## 2. Prioritize Gaps

Group gaps by priority from HYPOTHESES.md:

| Priority | Action |
|----------|--------|
| `primary` | Create experiment, blocks study completion |
| `secondary` | Create experiment, recommended |
| `exploratory` | Ask user: include or defer? |

For methodology gaps, prioritize by severity of the issue.

## 3. Group Gaps into Experiments

Cluster related gaps into logical experiments:

**Grouping rules:**
- Same untested hypothesis → single experiment
- Related methodology fixes → combined experiment
- Statistical replication needed → power analysis experiment
- Keep experiments focused: 1-2 hypotheses each

**Example grouping:**
```
Gap: HYP-03 untested (ablation not performed)
Gap: Methodology: need additional baseline
Gap: Statistical: insufficient power for HYP-02

→ Experiment 6: "Ablation Study"
  - Test HYP-03 with ablation analysis
  - Include additional baseline for comparison
  - Use larger sample for statistical power

→ Experiment 7: "Replication with Power"
  - Retest HYP-02 with adequate sample size
```

## 4. Determine Experiment Numbers

Find highest existing experiment:
```bash
ls -d .planning/phases/*/ | sort -V | tail -1
```

New experiments continue from there:
- If Experiment 5 is highest, gaps become Experiment 6, 7, 8...

## 5. Present Gap Closure Plan

```markdown
## Gap Closure Plan

**Study:** {version}
**Gaps to close:** {N} untested hypotheses, {M} methodology issues

### Proposed Experiments

**Experiment {N}: {Name}**
Closes:
- {HYP-ID}: {hypothesis not yet tested}
- Methodology: {issue to address}
Method: {proposed approach}

**Experiment {N+1}: {Name}**
Closes:
- Statistical: {power/significance issue}
Method: {proposed approach}

{If exploratory gaps exist:}

### Deferred (exploratory)

These gaps are optional. Include them?
- {gap description}
- {gap description}

---

Create these {X} experiments? (yes / adjust / defer optional)
```

Wait for user confirmation.

## 6. Update STUDY_PROTOCOL.md

Add new experiments to current study:

```markdown
### Experiment {N}: {Name}
**Hypothesis:** {HYP-ID}
**Method:** {approach}
**Gap Closure:** Addresses audit finding
**Success Criteria:** {metrics and thresholds}
**Controls:** {what to control for}

### Experiment {N+1}: {Name}
...
```

## 7. Create Experiment Directories

```bash
mkdir -p ".planning/phases/{NN}-{name}"
```

## 8. Commit Protocol Update

**Check planning config:**

```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

**If `COMMIT_PLANNING_DOCS=false`:** Skip git operations

**If `COMMIT_PLANNING_DOCS=true` (default):**

```bash
git add .planning/STUDY_PROTOCOL.md
git commit -m "docs(protocol): add gap closure experiments {N}-{M}"
```

## 9. Offer Next Steps

```markdown
## ✓ Gap Closure Experiments Created

**Experiments added:** {N} - {M}
**Gaps addressed:** {count} hypotheses, {count} methodology issues

---

## ▶ Next Up

**Plan first gap closure experiment**

`/grd:plan-phase {N}`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/grd:execute-phase {N}` — if plans already exist
- `cat .planning/STUDY_PROTOCOL.md` — see updated protocol

---

**After all gap experiments complete:**

`/grd:audit-study` — re-audit to verify gaps closed
`/grd:complete-study {version}` — archive when audit passes
```

</process>

<gap_to_experiment_mapping>

## How Gaps Become Experiments

**Untested hypothesis → Experiment:**
```yaml
gap:
  id: HYP-03
  claim: "Feature X improves performance by >10%"
  reason: "Ablation study not performed"

becomes:

experiment: "Feature X Ablation"
tasks:
  - name: "Implement ablation"
    files: [experiments/ablation.py]
    action: "Remove feature X and measure performance drop"

  - name: "Statistical analysis"
    files: [analysis/ablation_results.py]
    action: "Compute significance of performance difference"

  - name: "Document findings"
    files: [results/ablation.md]
    action: "Record whether hypothesis supported/rejected"
```

**Methodology gap → Experiment:**
```yaml
gap:
  experiment: 2
  issue: "Missing baseline comparison"
  reason: "Can't attribute improvement to proposed method"

becomes:

experiment: "Baseline Comparison"
tasks:
  - name: "Implement baseline"
    files: [baselines/standard.py]
    action: "Implement standard baseline method"

  - name: "Run comparison"
    files: [experiments/baseline_comparison.py]
    action: "Compare proposed vs baseline on same data"

  - name: "Update analysis"
    files: [analysis/comparative.py]
    action: "Add baseline to all performance tables"
```

**Statistical gap → Experiment:**
```yaml
gap:
  experiment: 1
  issue: "Insufficient statistical power"
  reason: "Sample size too small for claimed effect"
  missing:
    - "Power analysis"
    - "Larger sample evaluation"

becomes:

experiment: "Power Analysis and Replication"
tasks:
  - name: "Power analysis"
    files: [analysis/power.py]
    action: "Compute required sample size for effect"

  - name: "Data collection"
    action: "Gather additional samples to meet power requirement"

  - name: "Replication"
    files: [experiments/replication.py]
    action: "Re-run experiment with adequate sample"
```

</gap_to_experiment_mapping>

<success_criteria>
- [ ] STUDY-AUDIT.md loaded and gaps parsed
- [ ] Gaps prioritized (primary/secondary/exploratory)
- [ ] Gaps grouped into logical experiments
- [ ] User confirmed experiment plan
- [ ] STUDY_PROTOCOL.md updated with new experiments
- [ ] Experiment directories created
- [ ] Changes committed
- [ ] User knows to run `/grd:plan-phase` next
</success_criteria>
