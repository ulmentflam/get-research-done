# /grd:evaluate

**Human evaluation gate for validated experiments (Phase 5 command)**

---
name: grd:evaluate
description: Human evaluation gate for validated experiments
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
phase: 5
requires: [experiments/run_NNN/SCORECARD.json]
produces: [experiments/run_NNN/DECISION.md, human_eval/decision_log.md]
---

<objective>

Present complete evidence packages to humans for final validation decisions on ML experiments.

This command launches Phase 5 of the recursive validation loop—after the Critic approves (PROCEED) and the Evaluator generates quantitative benchmarks (SCORECARD.json), this command presents the full evidence package to the human researcher for a final decision: Seal (validate hypothesis), Iterate (continue experimentation), or Archive (abandon hypothesis).

**Creates:**
- `experiments/run_NNN/DECISION.md` — per-run decision record with timestamp, rationale, and context
- `human_eval/decision_log.md` — central append-only log of all decisions

**Use cases:**
- After Evaluator completes: Review SCORECARD.json and make final validation decision
- Multiple runs: Compare evidence across iterations before deciding
- Hypothesis validation: Seal successful experiments for production/publication
- Negative results: Archive failed hypotheses with documentation for future reference

**After this command:** Based on decision:
- Seal: Experiment validated, ready for downstream use
- Iterate: Continue with /grd:research (potentially with new direction)
- Archive: Hypothesis preserved in experiments/archive/ with reason

</objective>

<execution_context>

@~/.claude/get-research-done/templates/decision.md
@~/.claude/get-research-done/templates/archive-reason.md

</execution_context>

<process>

## Phase 1: Setup and Evidence Loading

**Check if project initialized:**

```bash
[ ! -f .planning/PROJECT.md ] && echo "ERROR: Project not initialized. Run /grd:new-project first." && exit 1
```

**Determine target run:**

If [run_name] argument provided:
- Use specified run directory
- Validate it exists in experiments/

If no argument:
- Scan experiments/ for runs with SCORECARD.json
- Find most recent by modification time
- Use latest as target

```bash
# Find runs with SCORECARD.json
if [ -n "$RUN_NAME" ]; then
  RUN_DIR="experiments/$RUN_NAME"
  [ ! -d "$RUN_DIR" ] && echo "ERROR: Run not found: $RUN_DIR" && exit 1
else
  # Find latest run with SCORECARD
  RUN_DIR=$(find experiments -name "SCORECARD.json" -type f | xargs -I {} dirname {} | xargs dirname | sort -r | head -1)
  [ -z "$RUN_DIR" ] && echo "ERROR: No runs with SCORECARD.json found in experiments/" && exit 1
fi
```

**Check SCORECARD.json exists (hard gate):**

```bash
[ ! -f "$RUN_DIR/metrics/SCORECARD.json" ] && echo "ERROR: SCORECARD.json not found. Run must complete Evaluator phase first." && exit 1
```

This is a HARD GATE - cannot proceed without quantitative benchmarks from Evaluator.

**Load evidence package:**

1. **SCORECARD.json** (required):
   ```bash
   cat "$RUN_DIR/metrics/SCORECARD.json"
   ```
   Extract:
   - Verdict (PROCEED/FAIL)
   - Composite score
   - Individual metrics (name, value, threshold, status)
   - Timestamp

2. **OBJECTIVE.md** (required for context):
   ```bash
   cat .planning/OBJECTIVE.md
   ```
   Extract:
   - Hypothesis statement (what/why/expected)
   - Success metrics with weights and thresholds
   - Falsification criteria

3. **CRITIC_LOG.md** (required):
   ```bash
   cat "$RUN_DIR/CRITIC_LOG.md"
   ```
   Extract:
   - Critic verdict (PROCEED)
   - Confidence level (HIGH/MEDIUM/LOW)
   - Strengths identified
   - Weaknesses/concerns
   - Recommendations

4. **DATA_REPORT.md** (optional context):
   ```bash
   cat .planning/DATA_REPORT.md 2>/dev/null
   ```
   If exists, extract data characteristics for context.

5. **Run metadata:**
   ```bash
   # Extract from directory structure and files
   RUN_NAME=$(basename "$RUN_DIR")
   ITERATION=$(grep "Iteration:" "$RUN_DIR/CRITIC_LOG.md" | head -1 | sed 's/.*: //')
   TIMESTAMP=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$RUN_DIR")
   DESCRIPTION=$(head -1 "$RUN_DIR/README.md" 2>/dev/null | sed 's/^# //')
   ```

**Load iteration history:**

```bash
# Count all runs in experiments/
TOTAL_RUNS=$(find experiments -maxdepth 1 -type d -name "run_*" | wc -l | tr -d ' ')

# Load verdict history from previous runs
for run_dir in experiments/run_*; do
  if [ -f "$run_dir/CRITIC_LOG.md" ]; then
    VERDICT=$(grep "^\*\*Verdict:\*\*" "$run_dir/CRITIC_LOG.md" | head -1 | sed 's/\*\*Verdict:\*\* //')
    echo "$(basename $run_dir): $VERDICT"
  fi
done > /tmp/verdict_history.txt
```

## Phase 2: Evidence Presentation

**Display evaluation banner:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► EVIDENCE PACKAGE: {run_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run: {run_name}
Iteration: {N} of {total_runs}
```

**Present executive summary first (always):**

Read and parse evidence files:
1. SCORECARD.json → composite_score, overall_result, individual metrics
2. CRITIC_LOG.md → verdict (PROCEED), confidence (HIGH/MEDIUM/LOW), strengths, weaknesses, recommendations
3. OBJECTIVE.md → hypothesis statement (what section), success metrics with thresholds
4. DATA_REPORT.md (optional) → sample size, class balance, leakage warnings

Determine verdict category:
- **VALIDATED**: Critic PROCEED + composite_score >= threshold + overall_result = PASS
- **FAILED**: composite_score < threshold OR overall_result = FAIL
- **INCONCLUSIVE**: Critic PROCEED with LOW confidence OR mixed metric results (some pass, some fail with borderline composite)

Display executive summary:

```
## Executive Summary

**Hypothesis:** {brief_what_statement_from_OBJECTIVE}

**Verdict:** {VALIDATED|FAILED|INCONCLUSIVE} ({confidence} confidence)
**Key Result:** {primary_metric}={value} (target: {comparison}{threshold}) {PASS|FAIL}
**Composite Score:** {score} (threshold: {threshold})

**Recommendation:** {one_sentence_from_critic_or_derived}
```

**Determine drill-down depth adaptively:**

After executive summary, Claude decides which sections to present based on:
- **Complexity**: Multiple metrics → show full metrics table
- **Confidence**: LOW confidence → show critic reasoning in detail
- **Verdict clarity**: FAILED or INCONCLUSIVE → show more analysis
- **Data concerns**: If DATA_REPORT.md has warnings → show data characteristics
- **Multiple iterations**: If total_runs > 1 → show iteration timeline

**Potential drill-down sections (Claude selects relevant):**

### Data Characteristics
Show if DATA_REPORT.md exists and has relevant warnings or context:
- **Sample size:** {N} samples, {M} features
- **Class balance:** {distribution if classification}
- **Leakage warnings:** {HIGH confidence warnings from DATA_REPORT.md}
- **Data quality:** {missing data percentage, outliers addressed}

### Iteration Timeline
Show if multiple runs exist (total_runs > 1):
```
Iteration history ({total_runs} runs):
- run_001_baseline: REVISE_METHOD (initial architecture)
- run_002_tuned: REVISE_METHOD (hyperparameter optimization)
- run_003_final: PROCEED (current) ✓
```

Brief by default. User can request full history expansion.

### Critic Reasoning
Show if verdict is borderline, confidence is LOW, or concerns exist:

**Strengths:**
- {strength_1 from CRITIC_LOG.md}
- {strength_2}

**Concerns:**
- {weakness_1 or "None identified"}

**Why PROCEED was given:**
{Extract reasoning from CRITIC_LOG.md}

**Residual concerns:**
{Any caveats or conditions mentioned}

### Full Metrics Detail
Show if user needs detailed breakdown or multiple metrics with mixed results:

| Metric | Value | Threshold | Weight | Status |
|--------|-------|-----------|--------|--------|
| {metric_1} | {value} | {comparison}{threshold} | {weight} | {PASS|FAIL} |
| {metric_2} | {value} | {comparison}{threshold} | {weight} | {PASS|FAIL} |
...

**Composite Score:** {weighted_average} = {calculation} (threshold: {overall_threshold})

---

**Implementation notes:**
- DO NOT dump raw file contents
- Parse JSON/Markdown and extract relevant fields
- Present digestible summary with context
- Offer drill-down based on complexity and clarity
- Primary metric = highest weighted or first in metrics list

## Phase 3: Decision Gate

**Present decision options:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 DECISION OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Seal — Hypothesis validated, ready for production/publication
2. Iterate — Continue experimentation with refinements
3. Archive — Abandon hypothesis, preserve as negative result
```

**Use AskUserQuestion for decision:**

```
header: "Human Evaluation Decision"
question: "Based on evidence above, how would you like to proceed?"
options:
  - "Seal" — Accept and validate experiment
  - "Iterate" — Continue with more runs
  - "Archive" — Abandon hypothesis
```

**If user selects "Iterate":**

Auto-suggest next direction based on Critic's last recommendation from CRITIC_LOG.md:
- If CRITIC_LOG has recommendations: "Critic suggests: {recommendation}"
- Offer: "Would you like to continue with Critic's recommendation or specify a new direction?"

No confirmation needed - proceed to Phase 4 logging.

**If user selects "Seal":**

No confirmation needed - proceed to Phase 4 logging.

**If user selects "Archive":**

**Confirmation required:**

Use AskUserQuestion:
```
header: "Confirm Archive"
question: "This will archive all runs and abandon the hypothesis. Are you sure?"
options:
  - "Yes, archive" — Proceed with archival
  - "Cancel" — Return to decision options
```

If confirmed, **require rationale:**

Use AskUserQuestion:
```
header: "Archive Rationale"
question: "Why is this hypothesis being abandoned? (Required for negative results documentation)"
options: null  # Free text input
```

Store rationale for ARCHIVE_REASON.md generation.

## Phase 4: Decision Logging

**Create per-run DECISION.md:**

```bash
# Use template from get-research-done/templates/decision.md
# Populate with:
# - Timestamp (ISO 8601)
# - Hypothesis (from OBJECTIVE.md)
# - Decision (Seal/Iterate/Archive)
# - Rationale (user-provided if Archive, optional otherwise)
# - Evidence summary (verdict, scores, metrics)

cat > "$RUN_DIR/DECISION.md" << EOF
[Generated content from decision.md template]
EOF
```

**Append to central decision log:**

```bash
# Create human_eval/ directory if doesn't exist
mkdir -p human_eval

# Initialize decision_log.md if doesn't exist
if [ ! -f human_eval/decision_log.md ]; then
  cat > human_eval/decision_log.md << EOF
# Human Evaluation Decision Log

Chronological record of all human evaluation decisions.

| Date | Run | Decision | Run Directory |
|------|-----|----------|---------------|
EOF
fi

# Append current decision
TIMESTAMP=$(date -u +"%Y-%m-%d")
echo "| $TIMESTAMP | $RUN_NAME | $DECISION | $RUN_DIR/ |" >> human_eval/decision_log.md
```

**Update STATE.md:**

```bash
# Add decision to appropriate section based on type
if [ "$DECISION" = "Seal" ]; then
  # Add to validated experiments list in STATE.md
  echo "- **$RUN_NAME:** Sealed on $TIMESTAMP" >> .planning/STATE.md
elif [ "$DECISION" = "Archive" ]; then
  # Add to archived hypotheses in STATE.md
  echo "- **Archived:** $TIMESTAMP - $HYPOTHESIS_NAME" >> .planning/STATE.md
fi

# Update loop status
sed -i '' 's/loop_status: .*/loop_status: human_decision_complete/' .planning/STATE.md
```

## Phase 5: Archive Handling (if Archive decision)

**If decision is Archive:**

1. **Determine hypothesis name:**
   ```bash
   # Extract from OBJECTIVE.md "what" section
   HYPOTHESIS_NAME=$(grep -A 5 "^### What" .planning/OBJECTIVE.md | head -6 | tail -5 | tr '\n' ' ' | sed 's/  */ /g' | cut -c 1-60)
   # Sanitize for filename (replace spaces with underscores, remove special chars)
   HYPOTHESIS_SLUG=$(echo "$HYPOTHESIS_NAME" | tr ' ' '_' | tr -cd '[:alnum:]_-' | tr '[:upper:]' '[:lower:]')
   ARCHIVE_NAME="$(date +%Y-%m-%d)_$HYPOTHESIS_SLUG"
   ```

2. **Create archive directory:**
   ```bash
   mkdir -p experiments/archive/"$ARCHIVE_NAME"
   ```

3. **Move final run to archive:**
   ```bash
   # Move current run (with DECISION.md) to archive
   mv "$RUN_DIR" experiments/archive/"$ARCHIVE_NAME"/final_run
   ```

4. **Create ITERATION_SUMMARY.md:**
   ```bash
   # Collapse other runs into summary
   cat > experiments/archive/"$ARCHIVE_NAME"/ITERATION_SUMMARY.md << EOF
# Iteration Summary

Total iterations: $TOTAL_RUNS

## Verdict History
[Table of all runs with verdicts, scores, key observations]

## Metric Trends
[Best/worst values achieved across iterations]

## Key Learnings
[Extracted from Critic feedback across runs]
EOF
   ```

5. **Create ARCHIVE_REASON.md:**
   ```bash
   # Use template from get-research-done/templates/archive-reason.md
   # Populate with:
   # - Hypothesis name and statement
   # - Final iteration count
   # - User rationale (required)
   # - What we learned (user fills)
   # - What would need to change (user fills)
   # - Final metrics (best achieved vs targets)

   cat > experiments/archive/"$ARCHIVE_NAME"/ARCHIVE_REASON.md << EOF
[Generated content from archive-reason.md template]
EOF
   ```

6. **Clean up intermediate runs (optional):**
   ```bash
   # Prompt user: delete or zip intermediate runs?
   # If zip: tar czf experiments/archive/$ARCHIVE_NAME/intermediate_runs.tar.gz experiments/run_*
   # If delete: rm -rf experiments/run_*
   ```

**Display archive confirmation:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► HYPOTHESIS ARCHIVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Archived to:** experiments/archive/{archive_name}/

**Contents:**
- final_run/ — Final experiment with DECISION.md
- ARCHIVE_REASON.md — Why this failed and what was learned
- ITERATION_SUMMARY.md — Collapsed history of all attempts

**Reason:** {user_rationale}

This negative result is preserved for future reference.
```

## Phase 6: Completion Summary

**Display final summary:**

**If Seal:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► HYPOTHESIS VALIDATED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Run:** {run_name}
**Decision:** Seal
**Recorded:** experiments/{run_name}/DECISION.md

This experiment is validated and ready for production/publication.

**Next steps:**
- Review final artifacts in run directory
- Consider downstream actions (deployment, paper submission, etc.)
```

**If Iterate:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► CONTINUING EXPERIMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Run:** {run_name}
**Decision:** Iterate
**Recorded:** experiments/{run_name}/DECISION.md

Continuing experimentation based on: {direction_or_recommendation}

**Next steps:**
- Run: /grd:research --continue
  {if_specific_direction: with focus on {direction}}
```

**If Archive:**
```
[Archive confirmation message already shown in Phase 5]
```

**Update decision log reference:**
```
**Decision log:** human_eval/decision_log.md
```

</process>

<arguments>

**[run_name]** (optional)
- Name of specific run to evaluate
- Examples: "run_003_tuned", "run_001_baseline"
- If omitted, evaluates latest run with SCORECARD.json

</arguments>

<examples>

**Evaluate latest run:**
```
/grd:evaluate
# Finds latest run with SCORECARD.json
```

**Evaluate specific run:**
```
/grd:evaluate run_003_tuned
# Evaluates specified run
```

**After Evaluator completes:**
```
# Researcher → Critic → Evaluator → /grd:evaluate
/grd:evaluate
# Human reviews evidence and makes decision
```

</examples>

<output>

- `experiments/run_NNN/DECISION.md` — per-run decision record with:
  - Timestamp (ISO 8601)
  - Hypothesis statement
  - Decision (Seal/Iterate/Archive)
  - Rationale (if provided)
  - Evidence summary (verdict, scores, metrics)
  - Decision context (strengths, concerns, next steps)

- `human_eval/decision_log.md` — central append-only log with:
  - Chronological table of all decisions
  - Date, run name, decision type, run directory path

- `experiments/archive/YYYY-MM-DD_hypothesis_name/` (if Archive) with:
  - `final_run/` — final experiment directory with DECISION.md
  - `ARCHIVE_REASON.md` — required rationale and learnings
  - `ITERATION_SUMMARY.md` — collapsed iteration history

</output>

<success_criteria>

- [ ] SCORECARD.json hard gate enforced (required)
- [ ] Evidence package assembled (SCORECARD, OBJECTIVE, CRITIC_LOG, metadata)
- [ ] Executive summary presented with adaptive drill-down
- [ ] Human decision captured (Seal/Iterate/Archive)
- [ ] Confirmation required for Archive with rationale
- [ ] DECISION.md created in run directory
- [ ] Central decision_log.md updated
- [ ] STATE.md updated with decision
- [ ] Archive process executed if Archive selected
- [ ] ARCHIVE_REASON.md and ITERATION_SUMMARY.md created for archives

</success_criteria>
