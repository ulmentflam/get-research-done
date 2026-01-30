# /grd:graduate

**Graduate validated notebooks to production Python scripts (Phase 6 command)**

---
name: graduate
description: Graduate a validated notebook to a production Python script in src/experiments/
argument-hint: "<notebook_path> [--run <run_number>] [--name <script_name>]"
allowed-tools: [Read, Write, Bash, Glob, Grep, Task]
---

<objective>

Graduate an exploratory notebook that has received Critic PROCEED verdict into a validated Python script.

This command:
1. Validates notebook meets graduation requirements (seeds, parameters cell)
2. Confirms Critic PROCEED verdict exists for a run of this notebook
3. Converts notebook to Python script via nbconvert
4. Adds graduation metadata header from template
5. Places script in src/experiments/
6. Logs graduation to decision_log.md

**Requirements:**
- Notebook must have passing Critic PROCEED verdict (any confidence level)
- Notebook must meet graduation checklist (random seed set, parameters cell tagged)
- Original notebook stays in notebooks/exploration/ (not moved/deleted)

**Use cases:**
- After successful validation: Convert approved notebook to script for production
- Multiple notebooks: Graduate each independently with separate scripts
- Script refactoring: Generated script includes refactoring checklist for manual completion

**After this command:** Review graduated script, complete refactoring checklist, add tests.

</objective>

<execution_context>

@~/.claude/get-research-done/templates/graduated-script.md

</execution_context>

<process>

## Phase 1: Validate Arguments

**Check if project initialized:**

```bash
[ ! -f .planning/PROJECT.md ] && echo "ERROR: Project not initialized. Run /grd:new-project first." && exit 1
```

**Validate notebook_path argument:**

1. Verify notebook_path is provided:
   ```bash
   [ -z "$NOTEBOOK_PATH" ] && echo "ERROR: notebook_path required. Usage: /grd:graduate <notebook_path>" && exit 1
   ```

2. Verify file exists and is a notebook:
   ```bash
   [ ! -f "$NOTEBOOK_PATH" ] && echo "ERROR: Notebook not found: $NOTEBOOK_PATH" && exit 1
   [[ "$NOTEBOOK_PATH" != *.ipynb ]] && echo "ERROR: File must be a Jupyter notebook (.ipynb)" && exit 1
   ```

3. Verify notebook is in notebooks/exploration/:
   ```bash
   if [[ "$NOTEBOOK_PATH" != notebooks/exploration/* ]]; then
     echo "WARNING: Notebook is not in notebooks/exploration/"
     echo "Graduation is intended for exploration notebooks."
     # Allow proceeding but warn
   fi
   ```

**Parse optional arguments:**

- `--run RUN_NUM`: Specific run number that passed (auto-detect if omitted)
- `--name SCRIPT_NAME`: Name for graduated script (default: notebook name)

## Phase 2: Find Passing Run

**If --run specified:**

```bash
RUN_DIR="experiments/run_${RUN_NUM}*"
RUN_DIR=$(ls -d $RUN_DIR 2>/dev/null | head -1)

if [ -z "$RUN_DIR" ] || [ ! -d "$RUN_DIR" ]; then
  echo "ERROR: Run directory not found: experiments/run_${RUN_NUM}*"
  exit 1
fi

# Verify CRITIC_LOG.md exists and has PROCEED verdict
if [ ! -f "$RUN_DIR/CRITIC_LOG.md" ]; then
  echo "ERROR: No CRITIC_LOG.md found in $RUN_DIR"
  exit 1
fi

VERDICT=$(grep "^\*\*Decision:\*\*" "$RUN_DIR/CRITIC_LOG.md" | head -1 | sed 's/.*: //')
if [ "$VERDICT" != "PROCEED" ]; then
  echo "ERROR: Run $RUN_DIR has verdict '$VERDICT', not PROCEED"
  echo "Only runs with PROCEED verdict can be graduated."
  exit 1
fi

# Verify run used this notebook (check config.yaml source_notebook)
if [ -f "$RUN_DIR/config.yaml" ]; then
  SOURCE_NB=$(grep "source_notebook:" "$RUN_DIR/config.yaml" | sed 's/.*: //')
  if [ -n "$SOURCE_NB" ] && [ "$SOURCE_NB" != "$NOTEBOOK_PATH" ]; then
    echo "WARNING: Run was executed with different notebook: $SOURCE_NB"
  fi
fi
```

**If --run not specified:**

```bash
# Scan experiments/run_*/CRITIC_LOG.md for PROCEED verdicts
PASSING_RUNS=""

for run_dir in experiments/run_*; do
  if [ -f "$run_dir/CRITIC_LOG.md" ]; then
    verdict=$(grep "^\*\*Decision:\*\*" "$run_dir/CRITIC_LOG.md" | head -1 | sed 's/.*: //')
    if [ "$verdict" = "PROCEED" ]; then
      # Check if this run used our notebook
      if [ -f "$run_dir/config.yaml" ]; then
        source_nb=$(grep "source_notebook:" "$run_dir/config.yaml" | sed 's/.*: //' | tr -d ' "')
        if [ "$source_nb" = "$NOTEBOOK_PATH" ]; then
          PASSING_RUNS="$PASSING_RUNS $run_dir"
        fi
      fi
    fi
  fi
done

if [ -z "$PASSING_RUNS" ]; then
  echo "ERROR: No PROCEED verdict found for $NOTEBOOK_PATH"
  echo "Run /grd:research with this notebook first."
  exit 1
fi

# Use most recent passing run
RUN_DIR=$(echo $PASSING_RUNS | tr ' ' '\n' | sort -r | head -1)
echo "Auto-detected passing run: $RUN_DIR"
```

**Extract verdict date:**

```bash
VERDICT_DATE=$(grep "^\*\*Timestamp:\*\*" "$RUN_DIR/CRITIC_LOG.md" | head -1 | sed 's/.*: //')
CRITIC_CONFIDENCE=$(grep "^\*\*Confidence:\*\*" "$RUN_DIR/CRITIC_LOG.md" | head -1 | sed 's/.*: //')
```

## Phase 3: Run Graduation Validation

Display graduation banner:
```
-------------------------------------------------------
 GRD > GRADUATION VALIDATION
-------------------------------------------------------

Notebook: {notebook_path}
Passing run: {run_dir}
Verdict: PROCEED ({confidence})
```

Spawn grd-graduator agent with:
- notebook_path
- run_dir (from Phase 2)
- script_name (from --name or derived from notebook)

```python
graduation_result = Task(prompt=f"""
<graduation_context>
Notebook: {notebook_path}
Run directory: {run_dir}
Script name: {script_name}
Verdict date: {verdict_date}
</graduation_context>

<instructions>
Execute notebook graduation workflow:

1. Validate graduation requirements using graduation_validator
2. Convert notebook to script via nbconvert
3. Apply graduated-script template for metadata header
4. Write to src/experiments/
5. Report completion with warnings if any

Template: @get-research-done/templates/graduated-script.md
</instructions>
""", subagent_type="grd-graduator", model="sonnet", description="Graduate notebook to script")
```

## Phase 4: Log Graduation

**Update human_eval/decision_log.md:**

```bash
# Ensure human_eval directory exists
mkdir -p human_eval

# Create log file if doesn't exist
if [ ! -f human_eval/decision_log.md ]; then
  cat > human_eval/decision_log.md << 'EOF'
# Human Evaluation Decision Log

This log tracks all human evaluation decisions for this research project.

| Date | Run | Decision | Rationale |
|------|-----|----------|-----------|
EOF
fi

# Append graduation entry
TIMESTAMP=$(date +"%Y-%m-%d")
echo "| $TIMESTAMP | $(basename $RUN_DIR) | GRADUATED | Notebook graduated to src/experiments/${SCRIPT_NAME}.py |" >> human_eval/decision_log.md
```

## Phase 5: Report Success

Display completion message:

```
-------------------------------------------------------
 GRD > GRADUATION COMPLETE
-------------------------------------------------------

Source notebook: {notebook_path}
Validated run: {run_dir}
Graduated script: src/experiments/{script_name}.py

Graduation details:
- Critic verdict: PROCEED ({confidence})
- Verdict date: {verdict_date}
- Graduation warnings: {warnings_list or "None"}

MANUAL REFACTORING REQUIRED:
The graduated script needs manual cleanup before production use:

- [ ] Remove/convert magic commands (grep "^%" in script)
- [ ] Extract code into functions
- [ ] Replace parameter cell with argparse
- [ ] Add docstrings and type hints
- [ ] Verify all random seeds are set
- [ ] Write tests for core functions

See the script header for full checklist.

Decision logged to: human_eval/decision_log.md
```

</process>

<arguments>

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `notebook_path` | Yes | Path to notebook in notebooks/exploration/ |
| `--run` | No | Specific run number that passed (auto-detect if omitted) |
| `--name` | No | Name for graduated script (default: notebook name) |

</arguments>

<examples>

**Graduate with auto-detected run:**
```
/grd:graduate notebooks/exploration/001_initial_experiment.ipynb
# Auto-detects latest PROCEED run for this notebook
# Creates: src/experiments/001_initial_experiment.py
```

**Graduate with specific run:**
```
/grd:graduate notebooks/exploration/baseline.ipynb --run 003
# Uses experiments/run_003_*/CRITIC_LOG.md for validation
# Creates: src/experiments/baseline.py
```

**Graduate with custom name:**
```
/grd:graduate notebooks/exploration/my_experiment.ipynb --name production_model
# Creates: src/experiments/production_model.py
```

**Full specification:**
```
/grd:graduate notebooks/exploration/feature_eng.ipynb --run 005 --name feature_pipeline
# Uses specific run, custom script name
# Creates: src/experiments/feature_pipeline.py
```

</examples>

<output>

- `src/experiments/{script_name}.py` — Graduated Python script containing:
  - Metadata header with source notebook, run, verdict
  - Refactoring checklist as TODO comments
  - Converted notebook code (via nbconvert)
  - Template functions for reproducibility

- `human_eval/decision_log.md` — Updated with graduation entry

</output>

<success_criteria>

- [ ] Notebook path validated (exists, is .ipynb, in exploration/)
- [ ] PROCEED verdict confirmed for run (specified or auto-detected)
- [ ] Graduation requirements validated (seeds, parameters cell)
- [ ] Notebook converted to script via nbconvert
- [ ] Metadata header applied from template
- [ ] Script written to src/experiments/
- [ ] Graduation logged to decision_log.md
- [ ] Original notebook unchanged in notebooks/exploration/
- [ ] Warnings reported (if any)

</success_criteria>
