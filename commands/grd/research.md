# /grd:research

**Implements experiments from OBJECTIVE.md with iterative validation (Phase 4 command)**

---
name: grd:research
description: Implement experiments from hypothesis with iterative validation loop
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - AskUserQuestion
agent: grd-researcher
phase: 4
requires: [OBJECTIVE.md]
produces: [experiments/run_NNN/]
---

<objective>

Execute hypothesis-driven experiment implementation with recursive validation through Critic agent.

This command launches Phase 4 of the recursive validation loop—the Researcher agent reads OBJECTIVE.md to understand what hypothesis to test, implements experiments in isolated run directories, and spawns the Critic agent for validation. The Critic routes verdicts (PROCEED/REVISE_METHOD/REVISE_DATA) that determine next steps.

**Creates:**
- `experiments/run_NNN_description/` — isolated run directory with complete snapshot
  - `code/` — experiment scripts (train.py or experiment.ipynb)
  - `config.yaml` — hyperparameters and settings
  - `data/` — symlinks/references to data with hashes
  - `logs/` — training output (stdout/stderr)
  - `outputs/` — model artifacts, predictions
  - `metrics/` — SCORECARD.json from Evaluator
  - `README.md` — brief experiment summary
  - `CRITIC_LOG.md` — Critic's evaluation and verdict

**Use cases:**
- After hypothesis formation: Implement experiments from OBJECTIVE.md
- Iterative refinement: Continue from REVISE_METHOD with Critic feedback
- Data validation: Trigger REVISE_DATA to return to /grd:explore
- Experiment versioning: Each iteration creates isolated, reproducible run

**After this command:** Review Critic verdict, proceed to Evaluator if PROCEED, or iterate based on routing.

</objective>

<execution_context>

@~/.claude/get-research-done/templates/experiment-readme.md

</execution_context>

<process>

## Phase 1: Setup - Validate Context

**Check if project initialized:**

```bash
[ ! -f .planning/PROJECT.md ] && echo "ERROR: Project not initialized. Run /grd:new-project first." && exit 1
```

**Check for OBJECTIVE.md (hard gate):**

```bash
ls .planning/OBJECTIVE.md 2>/dev/null
```

**If OBJECTIVE.md does NOT exist:**
- ERROR: "OBJECTIVE.md not found. Run /grd:architect first to define hypothesis."
- Exit immediately
- This is a HARD GATE - cannot proceed without hypothesis

**If OBJECTIVE.md exists:**
- Read and extract:
  - Hypothesis statement (what's being tested)
  - Success metrics (what defines success)
  - Evaluation methodology (how to evaluate)
  - Baselines (comparison points)
  - Falsification criteria (what would disprove hypothesis)
- Display brief summary:
  ```
  Hypothesis: [brief what statement]
  Metrics: [list with weights]
  Evaluation: [strategy]
  ```

**Determine run number:**

Parse optional [description] argument for run naming.

```bash
# Scan experiments/ directory for existing runs
if [ -d experiments ]; then
  # Get highest run number
  LAST_RUN=$(ls experiments/ | grep -E '^run_[0-9]+' | sed 's/run_\([0-9]*\).*/\1/' | sort -n | tail -1)
  NEXT_RUN=$((LAST_RUN + 1))
else
  mkdir -p experiments
  NEXT_RUN=1
fi

# Format with zero-padding
RUN_NUM=$(printf "%03d" $NEXT_RUN)
```

**Check for continuation mode:**

Parse flags:
- `--continue` - Continue from previous run with Critic feedback
- `--iteration N` - Specify iteration number manually (overrides auto-increment)

**If continuing:**

```bash
# Load previous CRITIC_LOG.md
LAST_RUN_DIR=$(ls -d experiments/run_* | sort | tail -1)
if [ -f "$LAST_RUN_DIR/CRITIC_LOG.md" ]; then
  CRITIQUE_HISTORY=$(cat "$LAST_RUN_DIR/CRITIC_LOG.md")
  echo "Continuing from previous run: $LAST_RUN_DIR"
  echo "Previous verdict: $(grep 'Verdict:' $LAST_RUN_DIR/CRITIC_LOG.md)"
fi
```

**Load DATA_REPORT.md context (soft reference):**

```bash
cat .planning/DATA_REPORT.md 2>/dev/null
```

If exists, extract data characteristics for experiment design:
- Sample size
- Feature types
- Class balance
- Leakage warnings
- Missing data patterns

If not exists, note: "No DATA_REPORT.md found - proceeding without data context"

## Phase 2: Spawn Researcher Agent

Display research banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► IMPLEMENTING EXPERIMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run: {run_NNN_description}
Hypothesis: [brief statement from OBJECTIVE.md]
Mode: [new | continue from REVISE_METHOD]
```

Spawn grd-researcher agent with context:

```
Task(prompt="
<objective_context>
@.planning/OBJECTIVE.md

Extract and internalize:
- Hypothesis (what, why, expected)
- Success metrics (names, thresholds, weights)
- Evaluation methodology (strategy, parameters)
- Baselines (comparison points)
- Falsification criteria (routing conditions)
- Constraints (data, resources, scope)
</objective_context>

<data_context>
@.planning/DATA_REPORT.md (if exists)

Extract for experiment design:
- Data characteristics (shape, types, distributions)
- Quality issues (missing data, outliers)
- Class balance (imbalance severity)
- Leakage warnings (features to exclude)
- Sample size (affects methodology)
</data_context>

<run_context>
Run number: {run_NNN}
Description: {description_or_auto}
Iteration: {iteration_count}
Previous critiques: {critique_history_if_continuing}
</run_context>

<instructions>
Execute experiment implementation workflow:

1. Create run directory: experiments/{run_NNN_description}/
2. Generate experiment code based on OBJECTIVE.md hypothesis
3. Create config.yaml with hyperparameters
4. Reference data (symlinks + hashes for provenance)
5. Execute experiment or prepare for user execution
6. Collect metrics and compare to OBJECTIVE.md success criteria
7. Spawn Critic agent for validation
8. Handle Critic verdict (PROCEED/REVISE_METHOD/REVISE_DATA/ESCALATE)

Use template: @get-research-done/templates/experiment-readme.md
Write README.md to run directory with experiment summary.
</instructions>

<output>
Return:
- Run directory path
- Experiment status (complete/pending/failed)
- Critic verdict
- Next steps based on routing
</output>
", subagent_type="grd-researcher", model="sonnet", description="Implement and validate experiment")
```

## Phase 3: Wait for Critic Routing

Researcher spawns Critic internally via Task tool. The command waits for final verdict.

**Researcher → Critic handoff:**
- Researcher completes experiment implementation
- Passes experiment artifacts to Critic
- Critic audits and returns verdict
- Researcher handles routing

**Command does NOT spawn Critic directly.** Researcher manages Critic interaction.

**Possible outcomes:**

1. **PROCEED** - Critic approved, Researcher spawns Evaluator
2. **REVISE_METHOD** - Methodological issues, Researcher logs and exits for retry
3. **REVISE_DATA** - Data quality issues, route back to /grd:explore
4. **ESCALATE** - Ambiguous failure, surface to human decision

## Phase 4: Present Results

After Researcher completes (with Critic verdict), present summary:

**If verdict is PROCEED:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► EXPERIMENT APPROVED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Run:** experiments/{run_NNN_description}/
**Verdict:** PROCEED (Confidence: {HIGH|MEDIUM|LOW})

## Experiment Summary

{one_paragraph_from_README.md}

## Metrics

{metrics_table_from_SCORECARD.json}

## Critic Assessment

**Strengths:**
{strengths_list}

**Concerns:**
{weaknesses_if_any}

**Recommendation:**
{recommendation_text}

---

**Next steps:**
- Review SCORECARD.json in run directory
- Evaluator will run quantitative benchmarks
- Proceed to human evaluation gate (Phase 5)
```

**If verdict is REVISE_METHOD:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► REVISION NEEDED (Method)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Run:** experiments/{run_NNN_description}/
**Verdict:** REVISE_METHOD (Confidence: {HIGH|MEDIUM|LOW})

## Issues Identified

{weaknesses_list_from_CRITIC_LOG}

## Recommendations

{specific_actionable_suggestions}

---

**Next steps:**
- Review CRITIC_LOG.md in run directory
- Address methodological issues
- Run: /grd:research --continue
```

**If verdict is REVISE_DATA:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► REVISION NEEDED (Data)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Run:** experiments/{run_NNN_description}/
**Verdict:** REVISE_DATA (Confidence: {HIGH|MEDIUM|LOW})

## Data Concerns

{data_issues_from_CRITIC_LOG}

## Recommendations

{specific_data_analysis_needed}

---

**Next steps:**
- Review CRITIC_LOG.md for specific concerns
- Run: /grd:explore [path] with targeted analysis
- Critic will append findings to DATA_REPORT.md
- Return to /grd:research after data issues resolved
```

**If verdict is ESCALATE:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► HUMAN DECISION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Run:** experiments/{run_NNN_description}/
**Verdict:** ESCALATE (Confidence: LOW)

## Ambiguous Failure

{reasoning_from_CRITIC_LOG}

Critic could not determine root cause (method vs data).

---

**Next steps:**
- Review CRITIC_LOG.md and experiment artifacts
- Manual investigation needed
- Decide: REVISE_METHOD, REVISE_DATA, or reformulate hypothesis
```

**Show run directory contents:**
```bash
tree -L 2 experiments/{run_NNN_description}
```

**Prompt for next action:**

Use AskUserQuestion if verdict requires human decision:
- header: "Experiment Status: {verdict}"
- question: "Review findings above. How would you like to proceed?"
- options:
  - "Continue" — Accept verdict and proceed
  - "Override" — Manual routing decision
  - "Archive" — Move run to archive/ and stop

</process>

<arguments>

**[description]** (optional)
- Brief description for run naming
- Examples: "baseline", "lr_sweep", "feature_eng"
- Used to create: experiments/run_001_baseline/
- If omitted, uses auto-generated description from hypothesis

**Flags:**

`--continue`
- Continue from previous run with Critic feedback
- Loads CRITIC_LOG.md from last run
- Increments iteration counter
- Use after REVISE_METHOD verdict

`--iteration N`
- Specify iteration number manually (overrides auto-increment)
- Use for: Resuming after interruption, manual organization
- Example: `--iteration 5` creates run_005_*

</arguments>

<examples>

**New experiment:**
```
/grd:research baseline
# Creates: experiments/run_001_baseline/
# Implements hypothesis from OBJECTIVE.md
```

**Continue after revision:**
```
/grd:research --continue
# Creates: experiments/run_002_revised/
# Includes previous Critic feedback
```

**Specific iteration:**
```
/grd:research --iteration 3 feature_engineering
# Creates: experiments/run_003_feature_engineering/
```

**Auto-named run:**
```
/grd:research
# Creates: experiments/run_001_hypothesis_test/
# Description inferred from OBJECTIVE.md
```

**After data revision:**
```
# After REVISE_DATA, fix data issues, then:
/grd:research --continue
# New run with updated data context
```

</examples>

<output>

- `experiments/run_NNN_description/` — isolated run directory containing:
  - `README.md` — experiment summary (what, why, how to reproduce)
  - `config.yaml` — hyperparameters and settings
  - `code/` — experiment scripts (train.py or experiment.ipynb)
  - `data/` — symlinks/references with hashes for provenance
  - `logs/` — training output (stdout/stderr)
  - `outputs/` — model artifacts, predictions
  - `metrics/` — SCORECARD.json from Evaluator
  - `CRITIC_LOG.md` — Critic's evaluation and verdict

**Run directory provides complete snapshot for reproducibility.**

</output>

<success_criteria>

- [ ] OBJECTIVE.md hard gate enforced (required, cannot proceed without it)
- [ ] Run number determined (auto-increment or specified)
- [ ] Researcher agent spawned with OBJECTIVE.md context
- [ ] DATA_REPORT.md context loaded if available
- [ ] Critique history passed if continuing
- [ ] Experiment implemented and validated
- [ ] Critic verdict obtained and routed appropriately
- [ ] Results presented with next steps
- [ ] Run directory created with complete artifacts

</success_criteria>
