---
name: grd:insights
description: Generate plain English data insights for business analysts without code or jargon
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - AskUserQuestion
---

<objective>

Generate accessible, plain English data insights for business analysts and non-technical stakeholders.

Unlike `/grd:explore` (technical) or `/grd:quick-explore` (fast), insights mode produces:
- **Technical report** saved to file (same rigor as full explore)
- **Plain English summary** displayed in console with "What This Means" explanations
- **Actionable recommendations** based on data characteristics
- **LLM prompts** for further exploration (copy-paste ready)

**Creates:**
- `.planning/DATA_REPORT.md` — full technical analysis (saved, not displayed)
- `.planning/INSIGHTS_SUMMARY.md` — plain English summary with recommendations
- Console output with business-friendly insights

**Use cases:**
- Explaining data to business stakeholders
- Preparing for cross-functional meetings
- Documenting data characteristics for non-technical team members
- Getting LLM-powered exploration prompts for deeper analysis

**After this command:**
- Share INSIGHTS_SUMMARY.md with stakeholders
- Use LLM prompts for further exploration
- Proceed to `/grd:architect` for hypothesis formation

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

## Phase 2: Spawn Explorer Agent (Insights Mode)

Display insights banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► DATA INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analyzing: [data_path]
Mode: Insights (business-friendly output)
```

Spawn grd-explorer agent with insights mode context:

```
Task(prompt="
<data_source>
Path: [data_path]
Type: [file | directory]
</data_source>

<profiling_mode>insights</profiling_mode>

<insights_mode_instructions>
Insights mode generates TWO outputs:

1. **Technical Report** (DATA_REPORT.md)
   - Full statistical analysis (same as regular explore)
   - Save to .planning/DATA_REPORT.md
   - Do NOT display in console

2. **Plain English Summary** (INSIGHTS_SUMMARY.md + Console)
   - Business-friendly language
   - Every statistic includes 'What This Means' explanation
   - Actionable recommendations
   - LLM prompts for further exploration

Plain English writing rules:
- No jargon: 'missing values' not 'null frequency'
- Context for numbers: '15% missing' → '15% of rows have no value here, which could affect predictions'
- Severity language: 'critical' / 'concerning' / 'minor' / 'looks good'
- Action-oriented: 'Consider removing...' not 'High cardinality detected'
</insights_mode_instructions>

<summary_structure>
# Data Insights Summary

## TL;DR (5 bullet points max)
The most important things a business person needs to know.

## 5 Things to Know About This Data
| Finding | What This Means |
|---------|-----------------|
| X rows of data | Enough/not enough for reliable analysis |
| Y% missing in column Z | May need to collect more data or handle gaps |

## Critical Issues (if any)
Plain English explanation of blocking problems.

## Recommendations
Priority-sorted list with effort estimates:
1. [High] Fix X before modeling — prevents Y problem
2. [Medium] Consider Z — improves reliability

## Dig Deeper (LLM Prompts)
Copy-paste prompts for further exploration:

```
Analyze the relationship between [column A] and [column B] in this dataset.
What patterns do you see?
```

```
The [column] has [X]% missing values. What strategies would you recommend
for handling this, given that [context from data]?
```
</summary_structure>

<project_context>
@.planning/PROJECT.md

Extract:
- What this project is about
- Business context for recommendations
</project_context>

<output>
1. Write .planning/DATA_REPORT.md (full technical analysis)
2. Write .planning/INSIGHTS_SUMMARY.md (plain English summary)
3. Print INSIGHTS_SUMMARY.md content to console
4. Return paths to both files
</output>
", subagent_type="grd-explorer", model="sonnet", description="Generate data insights")
```

## Phase 3: Present Results

After agent completes, display footer:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► INSIGHTS COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**For stakeholders:** .planning/INSIGHTS_SUMMARY.md
**Technical details:** .planning/DATA_REPORT.md

───────────────────────────────────────────────────────────────

**Share with team:** Copy INSIGHTS_SUMMARY.md content
**Deep dive:** Use the LLM prompts in the summary
**Next step:** /grd:architect — form a hypothesis

───────────────────────────────────────────────────────────────
```

</process>

<arguments>

**[path]** (required)
- Path to data file or directory
- Examples: `./data/train.csv`, `./datasets/`

</arguments>

<examples>

**Generate insights for CSV:**
```
/grd:insights ./data/train.csv
```

**Generate insights for directory:**
```
/grd:insights ./datasets/
```

</examples>

<output>

**Files created:**
- `.planning/DATA_REPORT.md` — full technical analysis
- `.planning/INSIGHTS_SUMMARY.md` — plain English summary

**Console output:**
- Complete INSIGHTS_SUMMARY.md content displayed
- Business-friendly language throughout
- LLM prompts for further exploration

</output>

<success_criteria>

- [ ] Data path resolved
- [ ] grd-explorer spawned with insights mode context
- [ ] DATA_REPORT.md created with full technical analysis
- [ ] INSIGHTS_SUMMARY.md created with plain English summary
- [ ] Every statistic includes "What This Means" explanation
- [ ] Actionable recommendations provided
- [ ] LLM prompts generated for further exploration
- [ ] Summary displayed in console

</success_criteria>
