---
name: grd:explore
description: Analyze raw data and generate DATA_REPORT.md with distributions, outliers, anomalies, and leakage detection
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - AskUserQuestion
---

<objective>

Explore and profile raw datasets to surface patterns, anomalies, and potential issues before hypothesis formation.

This command performs data reconnaissance—generating a comprehensive DATA_REPORT.md that reveals distributions, outliers, missing data patterns, class imbalance, and potential data leakage risks.

**Creates:**
- `.planning/DATA_REPORT.md` — comprehensive data profile and leakage analysis

**Use cases:**
- New dataset: Understand data characteristics before modeling
- Suspicious results: Check for leakage or data quality issues
- Feature engineering: Identify patterns and anomalies to inform feature creation
- Debugging: Profile data when model behavior is unexpected

**After this command:** Review DATA_REPORT.md for issues, then proceed with hypothesis formation and experimentation.

</objective>

<execution_context>

@~/.claude/get-research-done/templates/data-report.md

</execution_context>

<process>

## Phase 1: Setup and Data Path Resolution

**Check if project initialized:**

```bash
[ ! -f .planning/PROJECT.md ] && echo "ERROR: Project not initialized. Run /grd:new-project first." && exit 1
```

**Determine data path:**

If [path] argument provided:
- Use it directly
- Validate path exists

If no argument:
- Check for common data directories (./data/, ./datasets/, ./raw/)
- If found, list contents and ask user to select
- If not found, ask user to provide path interactively

**Validate data source:**

```bash
# Check if path exists
if [ -f "$DATA_PATH" ]; then
    echo "Single file: $DATA_PATH"
elif [ -d "$DATA_PATH" ]; then
    echo "Directory: $DATA_PATH"
    # List data files
    find "$DATA_PATH" -type f \( -name "*.csv" -o -name "*.parquet" -o -name "*.json" -o -name "*.jsonl" \) | head -20
else
    echo "ERROR: Path not found: $DATA_PATH"
    exit 1
fi
```

**Check for flags:**

- `--detailed`: Enable full profiling mode (histograms, percentiles, skewness, correlation heatmaps)
- Default: Quick profiling (basic stats, outliers, leakage checks)

## Phase 2: Spawn Explorer Agent

Display exploration banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► EXPLORING DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analyzing: [data_path]
Mode: [quick | detailed]
```

Spawn grd-explorer agent with context:

```
Task(prompt="
<data_source>
Path: [data_path]
Type: [file | directory]
</data_source>

<profiling_mode>
[quick | detailed]

Quick: Basic stats, distributions, outliers, leakage checks (fast)
Detailed: Full profiling with histograms, percentiles, skewness, correlation matrices (comprehensive)
</profiling_mode>

<project_context>
@.planning/PROJECT.md

Extract:
- What this project is about
- What the target variable might be (if ML project)
- Any known data characteristics
</project_context>

<instructions>
Execute data exploration workflow:

1. Load data (handle CSV, Parquet, JSON, JSONL)
2. Profile structure and distributions
3. Detect missing data patterns (MCAR/MAR/MNAR)
4. Find outliers and anomalies
5. Check class balance (if target identified)
6. Detect potential data leakage
7. Generate recommendations

Write: .planning/DATA_REPORT.md
Use template: ~/.claude/get-research-done/templates/data-report.md
</instructions>

<output>
Return DATA_REPORT.md path when complete.
</output>
", subagent_type="grd-explorer", model="sonnet", description="Explore and profile data")
```

## Phase 3: Present Results

After agent completes, read DATA_REPORT.md and present key findings:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► EXPLORATION COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Dataset Summary

**Rows:** [count] | **Columns:** [count] | **Memory:** [size]

## Key Findings

### Must Address (Blocking)
[List critical issues from recommendations]

### Should Address (Non-blocking)
[List recommended fixes]

### Leakage Risks
[High/medium confidence leakage indicators]

### Data Quality
[Missing data, outliers, imbalance summary]

---

**Full report:** `.planning/DATA_REPORT.md`

**Next steps:**
- Address blocking issues before modeling
- Consider should-fix items for better results
- Review leakage risks carefully—high confidence indicates problems
```

**If critical issues found:**

Offer to create tasks/reminders for fixing them:

Use AskUserQuestion:
- header: "Data Issues"
- question: "Critical data issues detected. Create follow-up tasks?"
- options:
  - "Yes" — Add to project backlog
  - "No" — I'll handle manually

If yes, create TODO entries or add to requirements tracking.

</process>

<arguments>

**[path]** (optional)
- Path to data file or directory
- Examples: `./data/train.csv`, `s3://bucket/data.parquet`, `./datasets/`
- If omitted, will prompt interactively

**Flags:**

`--detailed`
- Enable comprehensive profiling
- Includes: histograms, percentiles, skewness, kurtosis, correlation matrices
- Use when: Deep analysis needed or investigating specific issues
- Default: Quick mode (faster, covers essentials)

</arguments>

<examples>

**Explore single file:**
```
/grd:explore ./data/train.csv
```

**Explore directory:**
```
/grd:explore ./datasets/
```

**Detailed profiling:**
```
/grd:explore ./data/train.csv --detailed
```

**Interactive mode (no arguments):**
```
/grd:explore
# Will prompt for path
```

**Remote data:**
```
/grd:explore s3://my-bucket/data.parquet
```

</examples>

<output>

- `.planning/DATA_REPORT.md` — comprehensive data profile with:
  - Data overview (shape, types, memory)
  - Column summaries (types, nulls, unique values)
  - Distributions and statistics
  - Missing data analysis
  - Outlier detection
  - Class balance (if target specified)
  - Data leakage analysis
  - Recommendations

</output>

<success_criteria>

- [ ] Data path resolved (from argument or user input)
- [ ] grd-explorer agent spawned with context
- [ ] DATA_REPORT.md generated in .planning/
- [ ] Key findings presented to user
- [ ] Critical issues surfaced with next steps

</success_criteria>
