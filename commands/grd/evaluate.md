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

After evidence presentation, prompt user with three decision paths:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► DECISION GATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

How would you like to proceed?

1. **Seal** — Hypothesis validated, ready for production/publication
2. **Iterate** — Continue experimentation (Critic suggests: {direction})
3. **Archive** — Abandon hypothesis, preserve as negative result
```

**Extract Critic recommendation before prompting:**

```bash
# Parse CRITIC_LOG.md for last recommendation
CRITIC_RECOMMENDATION=$(grep -A 10 "## Recommendations" "$RUN_DIR/CRITIC_LOG.md" | tail -10)

# Determine suggested direction
if echo "$CRITIC_RECOMMENDATION" | grep -q "method\|algorithm\|architecture\|hyperparameter"; then
  DIRECTION="REVISE_METHOD"
  SUGGESTION="method refinement"
elif echo "$CRITIC_RECOMMENDATION" | grep -q "data\|feature\|sample\|leakage"; then
  DIRECTION="REVISE_DATA"
  SUGGESTION="data concerns"
else
  DIRECTION="continue experimentation"
  SUGGESTION="further iteration"
fi
```

**Use AskUserQuestion for decision:**

```javascript
AskUserQuestion({
  header: "Experiment Decision: {run_name}",
  question: "How would you like to proceed?",
  options: [
    "Seal — Hypothesis validated, ready for production/publication",
    "Iterate — Continue experimentation (Critic suggests: {SUGGESTION})",
    "Archive — Abandon hypothesis, preserve as negative result"
  ]
})
```

**Handle decision based on user selection:**

### If user selects "Seal":
- No confirmation needed (affirmative action)
- Store decision: `DECISION="Seal"`
- Proceed directly to Phase 4 (Decision Logging)
- Display: "Hypothesis sealed. Decision logged to {run_dir}/DECISION.md"

### If user selects "Iterate":
- No confirmation needed
- Store decision: `DECISION="Iterate"`
- Extract Critic's last recommendation from CRITIC_LOG.md
- Auto-suggest next steps based on direction:
  - If REVISE_METHOD: "Continue with method refinement. Next: /grd:research --continue"
  - If REVISE_DATA: "Data concerns identified. Next: /grd:explore with specific concerns, then /grd:research --continue"
  - If generic: "Continue experimentation. Next: /grd:research --continue"
- Display recommendation with next command
- Proceed to Phase 4 (Decision Logging)

### If user selects "Archive":
- **Confirmation gate required** (destructive action)

**Confirmation step:**

```javascript
AskUserQuestion({
  header: "Confirm Archive",
  question: "This will archive all runs and mark the hypothesis as failed. Continue?",
  options: [
    "Yes, archive with rationale",
    "Cancel"
  ]
})
```

If user selects "Cancel":
- Return to decision gate (re-prompt with Seal/Iterate/Archive options)
- Do not proceed to archival

If user selects "Yes, archive with rationale":
- **Require rationale** (mandatory for archive)

**Rationale capture:**

```javascript
AskUserQuestion({
  header: "Archive Rationale",
  question: "Why is this hypothesis being abandoned? (Required - saved in ARCHIVE_REASON.md)",
  // Free-form text input expected from user response
})
```

**Validate rationale:**
- Check rationale is not empty or whitespace-only
- If empty, prompt again: "Rationale is required to preserve context for future researchers. Please provide reason for abandonment."
- Loop until valid rationale provided
- Store rationale in variable: `ARCHIVE_RATIONALE="{user_input}"`

Store decision and rationale:
```bash
DECISION="Archive"
ARCHIVE_RATIONALE="{user_provided_text}"
```

Proceed to Phase 4 (Decision Logging) and Phase 5 (Archive Handling)

---

**Implementation notes:**
- Seal: Direct path to logging (no gates)
- Iterate: Direct path with auto-suggestion (no gates)
- Archive: Two-step confirmation (confirm → rationale) before proceeding
- All three paths eventually reach Phase 4 for DECISION.md creation

## Phase 4: Decision Logging

After user decision captured, generate decision records and update project state.

**Step 1: Extract evidence data for logging**

```bash
# Extract key data from evidence package for DECISION.md
TIMESTAMP_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TIMESTAMP_LOCAL=$(date +"%Y-%m-%d %H:%M")
TIMESTAMP_DATE=$(date +"%Y-%m-%d")

# Extract hypothesis brief from OBJECTIVE.md (what section)
HYPOTHESIS_BRIEF=$(grep -A 5 "^### What" .planning/OBJECTIVE.md | tail -n +2 | head -5 | tr '\n' ' ' | sed 's/  */ /g' | cut -c 1-100)

# Extract Critic data from CRITIC_LOG.md
CRITIC_CONFIDENCE=$(grep "^\*\*Confidence:\*\*" "$RUN_DIR/CRITIC_LOG.md" | head -1 | sed 's/.*: //')

# Extract Evaluator data from SCORECARD.json
COMPOSITE_SCORE=$(jq -r '.composite_score' "$RUN_DIR/metrics/SCORECARD.json")
THRESHOLD=$(jq -r '.threshold' "$RUN_DIR/metrics/SCORECARD.json")

# Get primary metric (highest weight or first)
KEY_METRIC_NAME=$(jq -r '.metrics | to_entries | max_by(.value.weight) | .key' "$RUN_DIR/metrics/SCORECARD.json")
KEY_METRIC_VALUE=$(jq -r --arg name "$KEY_METRIC_NAME" '.metrics[$name].value' "$RUN_DIR/metrics/SCORECARD.json")
KEY_METRIC_THRESHOLD=$(jq -r --arg name "$KEY_METRIC_NAME" '.metrics[$name].threshold' "$RUN_DIR/metrics/SCORECARD.json")
KEY_METRIC_COMPARISON=$(jq -r --arg name "$KEY_METRIC_NAME" '.metrics[$name].comparison' "$RUN_DIR/metrics/SCORECARD.json")
```

**Step 2: Build metrics table for DECISION.md**

```bash
# Extract all metrics from SCORECARD.json, sorted by weight descending
METRICS_TABLE=$(jq -r '.metrics | to_entries | sort_by(-.value.weight) | .[] |
  "| \(.key) | \(.value.value) | \(.value.comparison)\(.value.threshold) | \(.value.status) |"' \
  "$RUN_DIR/metrics/SCORECARD.json")
```

**Step 3: Generate decision-specific context**

```bash
# Populate decision context section based on type
if [ "$DECISION" = "Seal" ]; then
  DECISION_CONTEXT="### For Seal
- Hypothesis validated
- Ready for production/publication
- All success criteria met"

elif [ "$DECISION" = "Iterate" ]; then
  # Extract Critic's recommendation if available
  CRITIC_RECOMMENDATION=$(grep -A 10 "^\*\*Recommendation:\*\*" "$RUN_DIR/CRITIC_LOG.md" | tail -n +2 | head -5 | tr '\n' ' ' | sed 's/  */ /g')
  DECISION_CONTEXT="### For Iterate
- Continuing experimentation
- Direction: Based on Critic recommendation
- Next focus: ${CRITIC_RECOMMENDATION:-Further refinement needed}"

elif [ "$DECISION" = "Archive" ]; then
  DECISION_CONTEXT="### For Archive
- Hypothesis abandoned
- Reason: ${RATIONALE:-Not provided}
- Preserved as negative result"
fi
```

**Step 4: Create per-run DECISION.md**

Use Write tool to create DECISION.md in run directory:

```bash
# Generate DECISION.md from template
cat > "$RUN_DIR/DECISION.md" << EOF
# Human Decision: $RUN_NAME

**Timestamp:** $TIMESTAMP_ISO
**Hypothesis:** $HYPOTHESIS_BRIEF
**Decision:** $DECISION
**Rationale:** ${RATIONALE:-Not provided}

## Evidence Summary

**Critic Verdict:** PROCEED (Confidence: $CRITIC_CONFIDENCE)
**Composite Score:** $COMPOSITE_SCORE (threshold: $THRESHOLD)
**Key Metric:** $KEY_METRIC_NAME=$KEY_METRIC_VALUE (target: $KEY_METRIC_COMPARISON$KEY_METRIC_THRESHOLD)

## Metrics Detail

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
$METRICS_TABLE

## Decision Context

$DECISION_CONTEXT

---

*Decision recorded: $TIMESTAMP_ISO*
*Run directory: $RUN_DIR/*
EOF
```

**Step 5: Create/append to central decision_log.md**

Use Write tool with append logic:

```bash
# Ensure human_eval directory exists
mkdir -p human_eval

# Create log file if doesn't exist (use decision-log.md template header)
if [ ! -f human_eval/decision_log.md ]; then
  cat > human_eval/decision_log.md << EOF
# Human Evaluation Decision Log

This log tracks all human evaluation decisions for this research project.

| Timestamp | Run | Decision | Key Metric | Reference |
|-----------|-----|----------|------------|-----------|
EOF
fi

# Append new entry (chronological, newest at bottom)
echo "| $TIMESTAMP_LOCAL | $RUN_NAME | $DECISION | $KEY_METRIC_NAME=$KEY_METRIC_VALUE | $RUN_DIR/ |" >> human_eval/decision_log.md
```

**Step 6: Update STATE.md Research Loop State**

Update appropriate sections based on decision:

```bash
# Update Research Loop State > Status based on decision
if [ "$DECISION" = "Seal" ]; then
  # Mark hypothesis as validated
  sed -i '' 's/^\*\*Status:\*\* .*/\*\*Status:\*\* validated/' .planning/STATE.md

elif [ "$DECISION" = "Iterate" ]; then
  # Keep loop active, mark phase as researcher for next iteration
  sed -i '' 's/^\*\*Phase:\*\* .*/\*\*Phase:\*\* researcher/' .planning/STATE.md

elif [ "$DECISION" = "Archive" ]; then
  # Mark hypothesis as archived
  sed -i '' 's/^\*\*Status:\*\* .*/\*\*Status:\*\* archived/' .planning/STATE.md
fi

# Add entry to Human Decisions table
RATIONALE_EXCERPT=$(echo "${RATIONALE:-Not provided}" | head -c 50)

# Find Human Decisions table and append entry
# Using awk to find table and insert after header row
awk -v date="$TIMESTAMP_DATE" -v dec="$DECISION" -v rat="$RATIONALE_EXCERPT" '
  /^### Human Decisions/ { in_section=1 }
  in_section && /^\| Timestamp \| Decision \| Rationale \|$/ {
    print
    print "| " date " | " dec " | " rat " |"
    in_section=0
    next
  }
  { print }
' .planning/STATE.md > .planning/STATE.md.tmp && mv .planning/STATE.md.tmp .planning/STATE.md

# Update Loop History table with final decision annotation
# Mark current run with decision in parentheses
sed -i '' "s|\(^.*| $RUN_NAME |.*\)|\1 (Human: $DECISION)|" .planning/STATE.md
```

**Step 7: Display confirmation**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► DECISION LOGGED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Decision: {Seal|Iterate|Archive}

Logged to:
- experiments/{run_name}/DECISION.md
- human_eval/decision_log.md
- .planning/STATE.md (Research Loop State updated)

{Next steps based on decision:
  - Seal: "Experiment validated. Review run directory for artifacts."
  - Iterate: "Ready for next iteration. Run /grd:research --continue"
  - Archive: "Proceeding with archive workflow..." (triggers Phase 5)}
```

## Phase 5: Archive Handling (if Archive decision)

**If decision is Archive:**

**Step 1: Determine archive path**

```bash
# Extract hypothesis name from OBJECTIVE.md (sanitize for filesystem)
HYPOTHESIS_RAW=$(grep -A 1 "## Hypothesis" .planning/OBJECTIVE.md | tail -1 | head -c 50)
HYPOTHESIS_NAME=$(echo "$HYPOTHESIS_RAW" | tr ' ' '_' | tr -cd '[:alnum:]_-' | tr '[:upper:]' '[:lower:]')

# Date prefix
DATE_PREFIX=$(date +%Y-%m-%d)

# Archive directory path
ARCHIVE_DIR="experiments/archive/${DATE_PREFIX}_${HYPOTHESIS_NAME}"

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

echo "Creating archive directory: $ARCHIVE_DIR"
```

**Step 2: Identify final and intermediate runs**

```bash
# Find all run directories
ALL_RUNS=$(ls -d experiments/run_* 2>/dev/null | sort)

# Final run is the current one being evaluated (with DECISION.md)
FINAL_RUN="$RUN_DIR"

# Intermediate runs are all others
INTERMEDIATE_RUNS=$(echo "$ALL_RUNS" | grep -v "$(basename $FINAL_RUN)")

# Count intermediate runs
INTERMEDIATE_COUNT=$(echo "$INTERMEDIATE_RUNS" | grep -c "run_" || echo 0)
TOTAL_ITERATIONS=$(echo "$ALL_RUNS" | grep -c "run_")

echo "Identified:"
echo "  Final run: $FINAL_RUN"
echo "  Intermediate runs: $INTERMEDIATE_COUNT"
echo "  Total iterations: $TOTAL_ITERATIONS"
```

**Step 3: Move final run to archive**

Display progress:
```
Moving final run to archive...
  From: $FINAL_RUN
  To: $ARCHIVE_DIR/run_final/
```

```bash
# Move final run directory to archive (preserves full structure)
mv "$FINAL_RUN" "$ARCHIVE_DIR/run_final"

# Verify move succeeded
if [ ! -d "$ARCHIVE_DIR/run_final" ]; then
  echo "ERROR: Failed to move final run to archive"
  exit 1
fi

echo "✓ Final run moved to archive"
```

**Step 4: Generate ARCHIVE_REASON.md**

Extract data for ARCHIVE_REASON.md template:

```bash
# Extract hypothesis statement from OBJECTIVE.md
HYPOTHESIS_STATEMENT=$(grep -A 20 "^## Hypothesis" .planning/OBJECTIVE.md | grep -A 15 "^### What" | tail -n +2 | sed '/^###/,$d' | tr '\n' ' ' | sed 's/  */ /g')

# Extract final iteration and verdict
ITERATION_COUNT=$TOTAL_ITERATIONS
ITERATION_LIMIT=${ITERATION_LIMIT:-5}  # Default 5 if not set
FINAL_VERDICT=$(grep "^\*\*Verdict:\*\*" "$ARCHIVE_DIR/run_final/CRITIC_LOG.md" | head -1 | sed 's/\*\*Verdict:\*\* //')

# Extract best metrics across all runs
BEST_METRICS_TABLE=""
# Get metric names from OBJECTIVE.md
METRIC_NAMES=$(grep -A 50 "^## Success Metrics" .planning/OBJECTIVE.md | grep "^- \*\*" | sed 's/^- \*\*\(.*\)\*\*:.*/\1/')

# For each metric, find best value across all iterations
for metric in $METRIC_NAMES; do
  # Find best value from all SCORECARD.json files
  BEST_VALUE=$(jq -r --arg m "$metric" '.metrics[$m].value // empty' experiments/archive/*/run_final/metrics/SCORECARD.json "$ARCHIVE_DIR"/run_final/metrics/SCORECARD.json 2>/dev/null | sort -rn | head -1)
  TARGET=$(jq -r --arg m "$metric" '.metrics[$m].threshold // empty' "$ARCHIVE_DIR/run_final/metrics/SCORECARD.json" 2>/dev/null | head -1)
  COMPARISON=$(jq -r --arg m "$metric" '.metrics[$m].comparison // empty' "$ARCHIVE_DIR/run_final/metrics/SCORECARD.json" 2>/dev/null | head -1)

  if [ -n "$BEST_VALUE" ] && [ -n "$TARGET" ]; then
    GAP=$(echo "$BEST_VALUE - $TARGET" | bc 2>/dev/null || echo "N/A")
    BEST_METRICS_TABLE="$BEST_METRICS_TABLE
| $metric | $BEST_VALUE | $COMPARISON$TARGET | $GAP |"
  fi
done

# Get user rationale (already captured in Phase 3)
# USER_RATIONALE variable should be set from Archive confirmation step

# Create ARCHIVE_REASON.md from template
cat > "$ARCHIVE_DIR/ARCHIVE_REASON.md" << EOF
# Archive Reason: $HYPOTHESIS_NAME

**Archived:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Original Hypothesis:** $HYPOTHESIS_STATEMENT
**Final Iteration:** $ITERATION_COUNT of $ITERATION_LIMIT
**Final Verdict:** $FINAL_VERDICT

## Why This Failed

$ARCHIVE_RATIONALE

## What We Learned

*To be filled: Insights from failed attempts*

- Key finding 1
- Key finding 2
- Key finding 3

## What Would Need to Change

*To be filled: Conditions under which this might work*

- Required change 1
- Required change 2
- Required change 3

## Final Metrics

| Metric | Best Value | Target | Gap |
|--------|------------|--------|-----|
$BEST_METRICS_TABLE

## Iteration Timeline

See: ITERATION_SUMMARY.md for detailed history of all attempts.

---

*This negative result is preserved to prevent future researchers from repeating this approach without the necessary conditions.*

---

**Archive location:** experiments/archive/${DATE_PREFIX}_${HYPOTHESIS_NAME}/
**Decision recorded:** human_eval/decision_log.md
EOF

echo "✓ ARCHIVE_REASON.md created"
```

**Step 5: Generate ITERATION_SUMMARY.md**

Scan all run directories and compile iteration history:

```bash
# Build iteration history table from all runs
HISTORY_TABLE=""
ITERATION_NUM=1

# Collect verdict distribution counters
PROCEED_COUNT=0
REVISE_METHOD_COUNT=0
REVISE_DATA_COUNT=0
ESCALATE_COUNT=0

# Collect date range
FIRST_DATE=""
LAST_DATE=""

for run_dir in $ALL_RUNS; do
  run_name=$(basename "$run_dir")

  # Check if run has been archived (is now in archive/*/run_final/)
  if [ "$run_dir" = "$ARCHIVE_DIR/run_final" ] || [ ! -d "$run_dir" ]; then
    # This is the archived final run
    run_dir="$ARCHIVE_DIR/run_final"
  fi

  # Extract verdict and confidence from CRITIC_LOG.md
  if [ -f "$run_dir/CRITIC_LOG.md" ]; then
    verdict=$(grep "^\*\*Verdict:\*\*" "$run_dir/CRITIC_LOG.md" | head -1 | sed 's/\*\*Verdict:\*\* //')
    confidence=$(grep "^\*\*Confidence:\*\*" "$run_dir/CRITIC_LOG.md" | head -1 | sed 's/\*\*Confidence:\*\* //')

    # Count verdicts
    case "$verdict" in
      PROCEED) PROCEED_COUNT=$((PROCEED_COUNT + 1)) ;;
      REVISE_METHOD) REVISE_METHOD_COUNT=$((REVISE_METHOD_COUNT + 1)) ;;
      REVISE_DATA) REVISE_DATA_COUNT=$((REVISE_DATA_COUNT + 1)) ;;
      ESCALATE) ESCALATE_COUNT=$((ESCALATE_COUNT + 1)) ;;
    esac
  else
    verdict="N/A"
    confidence="N/A"
  fi

  # Extract key metric from SCORECARD.json (primary metric = highest weight)
  if [ -f "$run_dir/metrics/SCORECARD.json" ]; then
    key_metric_name=$(jq -r '.metrics | to_entries | max_by(.value.weight // 0) | .key // "N/A"' "$run_dir/metrics/SCORECARD.json" 2>/dev/null)
    key_metric_value=$(jq -r --arg m "$key_metric_name" '.metrics[$m].value // "N/A"' "$run_dir/metrics/SCORECARD.json" 2>/dev/null)
    key_metric="$key_metric_name=$key_metric_value"
  else
    key_metric="N/A"
  fi

  # Get run date
  run_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$run_dir" 2>/dev/null || date +%Y-%m-%d)

  # Track date range
  if [ -z "$FIRST_DATE" ]; then
    FIRST_DATE=$run_date
  fi
  LAST_DATE=$run_date

  # Extract notes from README.md
  notes=""
  if [ -f "$run_dir/README.md" ]; then
    notes=$(head -1 "$run_dir/README.md" | sed 's/^# //' | cut -c 1-30)
  fi

  # Append to history table
  HISTORY_TABLE="$HISTORY_TABLE
| $ITERATION_NUM | $run_name | $run_date | $verdict | $confidence | $key_metric | $notes |"

  ITERATION_NUM=$((ITERATION_NUM + 1))
done

# Calculate metric trend
# Extract primary metric values across all iterations
METRIC_VALUES=$(for run in $ALL_RUNS; do
  if [ -f "$run/metrics/SCORECARD.json" ]; then
    jq -r '.metrics | to_entries | max_by(.value.weight // 0) | .value.value // empty' "$run/metrics/SCORECARD.json" 2>/dev/null
  fi
done)

# Determine best metric
BEST_METRIC=$(echo "$METRIC_VALUES" | sort -rn | head -1)

# Get target from OBJECTIVE.md or final SCORECARD
TARGET_THRESHOLD=$(jq -r '.metrics | to_entries | max_by(.value.weight // 0) | .value.threshold // "N/A"' "$ARCHIVE_DIR/run_final/metrics/SCORECARD.json" 2>/dev/null)

# Calculate gap
if [ -n "$BEST_METRIC" ] && [ -n "$TARGET_THRESHOLD" ] && [ "$TARGET_THRESHOLD" != "N/A" ]; then
  GAP=$(echo "$BEST_METRIC - $TARGET_THRESHOLD" | bc 2>/dev/null || echo "N/A")
else
  GAP="N/A"
fi

# Determine trend (simple heuristic: compare first and last values)
FIRST_VALUE=$(echo "$METRIC_VALUES" | head -1)
LAST_VALUE=$(echo "$METRIC_VALUES" | tail -1)

if [ -n "$FIRST_VALUE" ] && [ -n "$LAST_VALUE" ]; then
  TREND_DIFF=$(echo "$LAST_VALUE - $FIRST_VALUE" | bc 2>/dev/null || echo 0)
  if (( $(echo "$TREND_DIFF > 0.05" | bc -l 2>/dev/null) )); then
    TREND="improving"
  elif (( $(echo "$TREND_DIFF < -0.05" | bc -l 2>/dev/null) )); then
    TREND="degrading"
  else
    TREND="stagnant"
  fi
else
  TREND="N/A"
fi

# Write ITERATION_SUMMARY.md
cat > "$ARCHIVE_DIR/ITERATION_SUMMARY.md" << EOF
# Iteration Summary: $HYPOTHESIS_NAME

**Total Iterations:** $TOTAL_ITERATIONS
**Date Range:** $FIRST_DATE to $LAST_DATE
**Outcome:** Archived (hypothesis abandoned)

## Iteration History

| # | Run | Date | Verdict | Confidence | Key Metric | Notes |
|---|-----|------|---------|------------|------------|-------|
$HISTORY_TABLE

## Metric Trend

**Best achieved:** $BEST_METRIC
**Target:** $TARGET_THRESHOLD
**Gap:** $GAP
**Trend:** $TREND

## Verdict Distribution

- PROCEED: $PROCEED_COUNT
- REVISE_METHOD: $REVISE_METHOD_COUNT
- REVISE_DATA: $REVISE_DATA_COUNT
- ESCALATE: $ESCALATE_COUNT

## Key Observations

*Summary of what was tried and why it didn't work*

## Preserved Artifacts

- Final run: run_final/
- All CRITIC_LOG.md files preserved in final run
- Final SCORECARD.json preserved in final run

---

*Summary generated on archive. See ARCHIVE_REASON.md for human rationale.*
EOF

echo "✓ ITERATION_SUMMARY.md created"
```

**Step 6: Create metadata.json**

Create archival metadata for programmatic access:

```bash
# Extract first line of rationale for summary
RATIONALE_FIRST_LINE=$(echo "$ARCHIVE_RATIONALE" | head -1 | cut -c 1-100)

# Create archival metadata JSON
cat > "$ARCHIVE_DIR/metadata.json" << EOF
{
  "archived_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "hypothesis": "$HYPOTHESIS_STATEMENT",
  "total_iterations": $TOTAL_ITERATIONS,
  "final_verdict": "$FINAL_VERDICT",
  "best_metric": "$BEST_METRIC",
  "target_threshold": "$TARGET_THRESHOLD",
  "archive_reason": "$RATIONALE_FIRST_LINE",
  "intermediate_runs_removed": $INTERMEDIATE_COUNT,
  "final_run_preserved": "run_final"
}
EOF

echo "✓ metadata.json created"
```

**Step 7: Clean up intermediate runs**

Display progress:
```
Cleaning up intermediate runs...
```

```bash
# Remove intermediate run directories (final run already moved to archive)
REMOVED_COUNT=0
for run_dir in $INTERMEDIATE_RUNS; do
  if [ -d "$run_dir" ] && [ -n "$run_dir" ]; then
    echo "  Removed: $run_dir"
    rm -rf "$run_dir"
    REMOVED_COUNT=$((REMOVED_COUNT + 1))
  fi
done

if [ $REMOVED_COUNT -eq 0 ]; then
  echo "  No intermediate runs to remove"
else
  echo "  Removed $REMOVED_COUNT intermediate run(s)"
fi

echo "  Kept: Final run preserved in archive"
```

**Step 8: Update decision_log.md reference**

Update the decision log entry to point to archive location:

```bash
# The decision log entry was created in Phase 4 pointing to experiments/run_NNN/
# Update it to point to archive location instead
RUN_NAME=$(basename "$FINAL_RUN")

# Update last entry in decision_log.md
# Change: experiments/run_NNN/ -> experiments/archive/YYYY-MM-DD_hypothesis/
if [ -f "human_eval/decision_log.md" ]; then
  # Use sed to replace the run path in the last occurrence
  sed -i.bak "s|experiments/$RUN_NAME/|$ARCHIVE_DIR/|g" human_eval/decision_log.md
  rm -f human_eval/decision_log.md.bak

  echo "✓ decision_log.md updated to reference archive location"
fi
```

**Step 9: Display archive completion**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► HYPOTHESIS ARCHIVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Archive Location:** $ARCHIVE_DIR

**Contents:**
- ARCHIVE_REASON.md — Your rationale preserved
- ITERATION_SUMMARY.md — All $TOTAL_ITERATIONS attempts summarized
- run_final/ — Final run with all artifacts
- metadata.json — Archival metadata

**Cleanup:**
- $INTERMEDIATE_COUNT intermediate run(s) removed
- Final run preserved with full artifacts

**Next steps:**
- Review ARCHIVE_REASON.md to add learnings
- Optionally fill "What We Learned" and "What Would Need to Change" sections
- Start new hypothesis with /grd:architect if ready

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
