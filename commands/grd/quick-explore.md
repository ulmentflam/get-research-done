---
name: grd:quick-explore
description: Fast EDA producing console summary for quick data familiarization decisions
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - AskUserQuestion
---

<objective>

Fast exploratory data analysis that outputs a console-friendly summary for quick decisions and team sharing.

Unlike `/grd:explore` which produces a comprehensive DATA_REPORT.md, quick-explore prioritizes speed and readability:
- Completes in under 60 seconds
- Outputs formatted summary to console (copy-paste ready)
- Highlights critical issues with visual indicators
- Generates minimal DATA_REPORT.md marked as "Quick Explore Mode"

**Creates:**
- Console output with TL;DR, column summary, distribution highlights
- `.planning/DATA_REPORT.md` — marked as Quick Explore Mode (run full explore for rigor)

**Use cases:**
- First look at a new dataset
- Quick check before a meeting
- Sharing data overview with team (copy-paste console output)
- Deciding whether to invest time in full exploration

**After this command:**
- For quick decisions: Use the console summary
- For modeling: Run `/grd:explore` for comprehensive analysis

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
    find "$DATA_PATH" -type f \( -name "*.csv" -o -name "*.parquet" -o -name "*.json" \) | head -10
else
    echo "ERROR: Path not found: $DATA_PATH"
    exit 1
fi
```

## Phase 2: Spawn Explorer Agent (Quick Mode)

Display quick explore banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► QUICK EXPLORE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analyzing: [data_path]
Mode: Quick (< 60 seconds)
```

Spawn grd-explorer agent with quick mode context:

```
Task(prompt="
<data_source>
Path: [data_path]
Type: [file | directory]
</data_source>

<profiling_mode>quick</profiling_mode>

<quick_mode_instructions>
Quick explore mode priorities:
1. Speed: Complete analysis in < 60 seconds
2. Console output: Format results for terminal display
3. Visual indicators: Use emoji and formatting for quick scanning
4. Critical issues: Surface blocking problems prominently

Skip in quick mode:
- Detailed correlation analysis
- Comprehensive leakage detection (do basic checks only)
- Full distribution histograms
- Percentile calculations beyond quartiles

Include in quick mode:
- Row/column counts, memory usage
- Column types and missing value percentages
- Basic distribution indicators (skewness direction, outlier flags)
- Top 3 most concerning data quality issues
- Quick leakage red flags (obvious column name patterns)

Output format:
1. Print formatted TL;DR to console
2. Print column summary table to console
3. Print distribution highlights to console
4. Print quality warnings to console
5. Write DATA_REPORT.md with 'Quick Explore Mode' header
</quick_mode_instructions>

<project_context>
@.planning/PROJECT.md

Extract:
- What this project is about
- What the target variable might be (if ML project)
</project_context>

<console_output_format>
Use Rich-style formatting for console output:

## TL;DR
- Rows: X | Columns: Y | Memory: Z MB
- Missing: X% overall | Y columns have nulls
- Types: X numeric, Y categorical, Z datetime
- Issues: [emoji] [count] [severity] items need attention

## Column Summary (one line per column)
| Column | Type | Missing | Distribution |
|--------|------|---------|--------------|
| age    | int  | 0%      | ▁▂▃▅▇ normal |
| income | float| 5%      | ▁▁▁▁▇ right-skewed |

## Distribution Highlights
- [column]: [skewness indicator] [outlier flag]

## Quality Warnings
- [emoji] [severity]: [description]
</console_output_format>

<output>
1. Print formatted analysis to console
2. Write .planning/DATA_REPORT.md with Quick Explore header
3. Return summary of findings
</output>
", subagent_type="grd-explorer", model="sonnet", description="Quick explore data")
```

## Phase 3: Present Results

After agent completes, display footer:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► QUICK EXPLORE COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick report: .planning/DATA_REPORT.md (Quick Explore Mode)

───────────────────────────────────────────────────────────────

**For comprehensive analysis:** /grd:explore [path]
**To proceed with hypothesis:** /grd:architect

Note: Quick explore provides fast insights but skips thorough
leakage detection. Run full explore before modeling.

───────────────────────────────────────────────────────────────
```

</process>

<arguments>

**[path]** (required)
- Path to data file or directory
- Examples: `./data/train.csv`, `./datasets/`

</arguments>

<examples>

**Quick look at CSV:**
```
/grd:quick-explore ./data/train.csv
```

**Quick look at dataset directory:**
```
/grd:quick-explore ./datasets/
```

</examples>

<output>

**Console output:**
- TL;DR summary (row/column counts, types, issues)
- Column summary table with distribution sparklines
- Quality warnings with severity indicators

**File output:**
- `.planning/DATA_REPORT.md` — marked as Quick Explore Mode

</output>

<success_criteria>

- [ ] Data path resolved
- [ ] grd-explorer spawned with quick mode context
- [ ] Console summary printed with formatted output
- [ ] DATA_REPORT.md created with Quick Explore Mode header
- [ ] Analysis completed in < 60 seconds
- [ ] User informed about full explore option

</success_criteria>
