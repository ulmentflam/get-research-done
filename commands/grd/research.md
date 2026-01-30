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

## Phase 1: Setup and State Loading

**Check if project initialized:**

```bash
[ ! -f .planning/PROJECT.md ] && echo "ERROR: Project not initialized. Run /grd:new-project first." && exit 1
```

**Check OBJECTIVE.md exists (hard gate):**

```bash
[ ! -f .planning/OBJECTIVE.md ] && echo "ERROR: No OBJECTIVE.md found. Run /grd:architect first." && exit 1
```

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

**Determine iteration state:**

If `--continue` flag:
- Find latest run directory in experiments/
- Read CRITIC_LOG.md for verdict and recommendations
- If verdict != REVISE_METHOD and verdict != REVISE_DATA: warn "No revision verdict to continue from"
- Load verdict history from previous runs
- Set iteration_count from previous run + 1

If `--iteration N`:
- Use provided N as iteration_count
- Warn if N conflicts with existing runs
- Load verdict history from runs 1 through N-1

If `--from-archive RUN_NAME`:
- Restore archived run from experiments/archive/
- Move back to experiments/
- Extract iteration count from run
- Load critique history

Otherwise (fresh start):
- Set iteration_count = 1
- Initialize empty verdict_history
- Scan experiments/ for existing runs to determine next run number

**Load iteration limit:**
- Default: 5
- Override with `--limit N` if provided
- Log: "Iteration limit: {N}"
- Store for Researcher agent

**Load verdict history:**
```bash
# Load all CRITIC_LOG.md files to build verdict history
for run_dir in experiments/run_*; do
  if [ -f "$run_dir/CRITIC_LOG.md" ]; then
    # Extract verdict, confidence, iteration from CRITIC_LOG
    VERDICT=$(grep "^\*\*Verdict:\*\*" "$run_dir/CRITIC_LOG.md" | head -1)
    CONFIDENCE=$(grep "^\*\*Confidence:\*\*" "$run_dir/CRITIC_LOG.md" | head -1)
    # Add to verdict_history array
  fi
done
```

**Update STATE.md:**
- Set current_phase: "research"
- Set current_iteration: {iteration_count}
- Set iteration_limit: {limit}
- Set active_hypothesis: (from OBJECTIVE.md)
- Update loop_history table with current iteration
- Set loop_status: "researcher" (in progress)

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

**If continuing from REVISE_METHOD:**

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

## Phase 3: Handle Loop Completion

After Researcher returns, parse verdict and update STATE.md accordingly.

**Extract verdict from Researcher response:**
```bash
# Parse Researcher return message for verdict
VERDICT=$(echo "$RESEARCHER_OUTPUT" | grep "^\*\*Verdict:\*\*" | sed 's/\*\*Verdict:\*\* //' | cut -d' ' -f1)
CONFIDENCE=$(echo "$RESEARCHER_OUTPUT" | grep "^\*\*Confidence:\*\*" | sed 's/\*\*Confidence:\*\* //')
ITERATION=$(echo "$RESEARCHER_OUTPUT" | grep "^\*\*Iteration:\*\*" | sed 's/\*\*Iteration:\*\* //')
```

**Route based on verdict:**

### If PROCEED (HIGH/MEDIUM confidence)

Researcher has spawned Evaluator automatically.

```bash
# Update STATE.md
echo "Updating STATE.md: verdict=PROCEED, status=evaluator_running"

# Add to loop history
echo "| $ITERATION | $RUN_NAME | PROCEED | $CONFIDENCE | {metrics} |" >> .planning/STATE.md

# Update loop status
sed -i 's/loop_status: .*/loop_status: evaluator/' .planning/STATE.md
```

**Display:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► EXPERIMENT APPROVED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Verdict:** PROCEED (Confidence: {confidence})
**Run:** experiments/{run_NNN_description}/

Evaluator running quantitative benchmarks...
SCORECARD.json will be generated in metrics/ directory.

Next: Ready for Phase 5 human review after Evaluator completes.
```

### If PROCEED (LOW confidence) - Human gate

Researcher has paused for human confirmation.

```bash
# Prompt human for decision
echo "Low confidence PROCEED - human confirmation required"
```

**Display concerns and options:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► HUMAN CONFIRMATION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Verdict:** PROCEED (LOW confidence)
**Run:** experiments/{run_NNN_description}/

Metrics pass but concerns exist:
{list_concerns_from_critic}

Options:
1. Approve - Proceed to Evaluator despite concerns
2. Revise - Treat as REVISE_METHOD, address concerns first
3. Investigate - Manual review before deciding
```

### If REVISE_METHOD (under limit)

Researcher has archived run and is ready for retry.

```bash
# Update STATE.md
echo "| $ITERATION | $RUN_NAME | REVISE_METHOD | $CONFIDENCE | {metrics} |" >> .planning/STATE.md

# Update iteration count
NEW_ITERATION=$((ITERATION + 1))
sed -i "s/current_iteration: .*/current_iteration: $NEW_ITERATION/" .planning/STATE.md

# Update loop status
sed -i 's/loop_status: .*/loop_status: researcher/' .planning/STATE.md
```

**Display:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► REVISION NEEDED (Method)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Iteration:** {iteration} of {limit}
**Run archived:** experiments/archive/{run_NNN_description}/

Issues identified:
{list_weaknesses}

Recommendations:
{list_recommendations}

Next: /grd:research --continue
```

### If REVISE_METHOD (limit reached)

Researcher has triggered human decision gate.

```bash
# Update STATE.md
echo "| $ITERATION | $RUN_NAME | REVISE_METHOD | $CONFIDENCE | limit_reached |" >> .planning/STATE.md
sed -i 's/loop_status: .*/loop_status: human_review/' .planning/STATE.md
```

**Display human decision prompt** (already handled by Researcher Step 8)

### If REVISE_DATA

Researcher has identified data quality issues.

```bash
# Update STATE.md
echo "| $ITERATION | $RUN_NAME | REVISE_DATA | $CONFIDENCE | data_concerns |" >> .planning/STATE.md
sed -i 's/loop_status: .*/loop_status: data_verification_required/' .planning/STATE.md

# Add to data_revisions table
echo "| $ITERATION | {concern_list} | pending |" >> .planning/STATE.md
```

**Display:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► REVISION NEEDED (Data)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Data concerns identified:**
{list_data_concerns}

**Recommended analysis:**
{specific_concerns_for_explorer}

Next steps:
1. Run: /grd:explore [path] --concerns "{concern_list}"
2. After Explorer updates DATA_REPORT.md:
   - Run /grd:research --continue to retry with updated data context
   - Or run /grd:architect to reformulate hypothesis
```

### If ESCALATE

Researcher has escalated to human for strategic decision.

```bash
# Update STATE.md
echo "| $ITERATION | $RUN_NAME | ESCALATE | N/A | ambiguous_failure |" >> .planning/STATE.md
sed -i 's/loop_status: .*/loop_status: human_review/' .planning/STATE.md

# Add blocker
echo "- **Current:** Ambiguous failure - cannot determine root cause" >> .planning/STATE.md
echo "- **Requires:** Human strategic decision" >> .planning/STATE.md
```

**Display:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► HUMAN DECISION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Reason:** Ambiguous failure - Critic could not determine root cause

Evidence:
{evidence_package_from_researcher}

Options:
1. Continue - Allow more iterations
2. Archive - Abandon hypothesis
3. Reset - Start fresh approach
4. Escalate - Reformulate hypothesis via /grd:architect
```

### If Archived/Reset (Human decision outcome)

```bash
# Update STATE.md based on decision
if [ "$DECISION" = "Archive" ]; then
  sed -i 's/loop_status: .*/loop_status: archived/' .planning/STATE.md
  echo "- **Status:** Hypothesis archived - {reason}" >> .planning/STATE.md
elif [ "$DECISION" = "Reset" ]; then
  sed -i 's/loop_status: .*/loop_status: idle/' .planning/STATE.md
  sed -i 's/current_iteration: .*/current_iteration: 0/' .planning/STATE.md
fi
```

**Researcher → Critic handoff:**
- Researcher completes experiment implementation
- Passes experiment artifacts to Critic
- Critic audits and returns verdict
- Researcher handles routing (including Evaluator spawn on PROCEED)

**Command does NOT spawn Critic or Evaluator directly.** Researcher orchestrates the full loop.

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
- One-line description for run naming
- Examples: "baseline", "lr_sweep", "feature_engineering"
- If omitted, uses "experiment"

**Flags:**

`--continue`
- Continue from previous run after REVISE_METHOD verdict
- Loads latest CRITIC_LOG.md recommendations
- Increments iteration count

`--iteration N`
- Manually specify iteration number
- Useful for resuming after interruption

`--limit N`
- Override default iteration limit (default: 5)
- Use with caution - higher limits increase cost

`--from-archive RUN_NAME`
- Restore archived run and continue from there
- Moves run back to experiments/

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
