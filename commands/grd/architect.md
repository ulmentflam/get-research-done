# /grd:architect

**Synthesizes testable hypotheses from data insights with iterative refinement (Phase 3 command)**

---
name: grd:architect
description: Synthesize testable hypotheses from data insights with iterative refinement
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - AskUserQuestion
agent: grd-architect
phase: 3
requires: [DATA_REPORT.md (optional but recommended)]
produces: [OBJECTIVE.md]
---

<objective>

Transform data insights into testable ML hypotheses through an interactive, advisor-like process.

This command enables conversational hypothesis synthesis—the Architect agent proposes hypotheses, explains reasoning, and refines based on user feedback. The agent acts as a research advisor, not a dictator: it suggests directions but accepts user override.

**Creates:**
- `.planning/OBJECTIVE.md` — testable hypothesis with success metrics, evaluation strategy, baselines, and falsification criteria

**Use cases:**
- After data exploration: Ground hypothesis in DATA_REPORT.md findings
- New research direction: Define what to test and how success is measured
- Experiment planning: Establish clear falsification criteria before implementation
- Iterative refinement: Collaborate with agent to improve hypothesis quality

**After this command:** Review OBJECTIVE.md for accuracy, then proceed with /grd:research (Phase 4) to implement experiments.

</objective>

<execution_context>

@~/.claude/get-research-done/templates/objective.md

</execution_context>

<process>

## Phase 1: Setup and Context Loading

**Check if project initialized:**

```bash
[ ! -f .planning/PROJECT.md ] && echo "ERROR: Project not initialized. Run /grd:new-project first." && exit 1
```

**Check for completed data reconnaissance (soft gate):**

```bash
ls .planning/DATA_REPORT.md 2>/dev/null
```

**If DATA_REPORT.md exists:**
- Note: "Using data insights from DATA_REPORT.md"
- Read and extract key findings for hypothesis grounding:
  - Leakage warnings to avoid in hypothesis
  - Data quality issues that constrain approach
  - Class balance requiring special handling
  - Feature correlations suggesting relationships
- Pass findings to architect agent for context

**If DATA_REPORT.md does NOT exist:**
- Warn: "WARNING: No DATA_REPORT.md found. Data reconnaissance not completed."
- Suggest: "Run /grd:explore first to analyze your data before forming hypotheses."
- Ask: "Continue anyway? (yes/no)"
- If user says yes: Proceed without data context
- If user says no: Exit and suggest running /grd:explore

This is a SOFT GATE - warns but allows proceeding. User decides if data-first is needed for their workflow.

**Why this matters:**
- Hypotheses grounded in data characteristics are more likely to be testable
- Data quality issues may constrain what's scientifically valid to test
- Leakage patterns inform which features should be excluded from hypothesis tests

**Load project context:**

```bash
cat .planning/PROJECT.md
```

Extract:
- Project goals and domain context
- Any stated research questions
- Domain-specific constraints

## Phase 2: Hypothesis Mode Selection

**Check for optional [direction] argument:**

Parse command invocation for direction text after command name.

**If direction provided:**
- Use as starting point for hypothesis
- Mode: "user-directed"
- Pass direction to architect agent

**If no direction but DATA_REPORT.md exists:**
- Mode: "auto-propose"
- Architect will analyze DATA_REPORT.md findings and propose hypothesis

**If neither:**
- Use AskUserQuestion:
  ```
  header: "Hypothesis Direction"
  question: "What would you like to test? (Or press Enter to auto-propose from DATA_REPORT.md)"
  options: null  # Free text input
  ```
- If user provides text: Mode "user-directed"
- If empty and DATA_REPORT.md exists: Mode "auto-propose"
- If empty and no DATA_REPORT.md: Exit with error "No direction provided and no DATA_REPORT.md to auto-propose from"

**Check for flags:**

- `--skip-data-check`: Skip the DATA_REPORT.md soft gate warning

## Phase 3: Spawn Architect Agent

Display banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► SYNTHESIZING HYPOTHESIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mode: [auto-propose | user-directed]
Data context: [DATA_REPORT.md found | No data report]
```

Spawn grd-architect agent with context:

```
Task(prompt="
<mode>
[auto-propose | user-directed]
Direction: [user_direction_if_any]
</mode>

<data_context>
@.planning/DATA_REPORT.md (if exists)

Key findings to incorporate:
- Leakage warnings: [list]
- Data quality issues: [list]
- Class balance: [summary]
- Feature correlations: [relevant findings]
- Missing data patterns: [summary]
</data_context>

<project_context>
@.planning/PROJECT.md

Extract:
- Project goals
- Domain context
- Any stated research questions
</project_context>

<instructions>
Execute hypothesis synthesis workflow:

1. Propose hypothesis based on mode (auto from data OR user direction)
2. Explain reasoning and expected outcome
3. Suggest success metrics and evaluation methodology
4. Identify baseline options
5. Define falsification criteria
6. Await user feedback
7. Refine if requested, up to 15 iterations
8. When user approves, generate OBJECTIVE.md

Use template: @get-research-done/templates/objective.md
Write to: .planning/OBJECTIVE.md
</instructions>
", subagent_type="grd-architect", model="sonnet", description="Synthesize testable hypothesis")
```

## Phase 4: Present Results

After agent completes, read OBJECTIVE.md and present summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► HYPOTHESIS SYNTHESIZED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Hypothesis: [brief statement from OBJECTIVE.md "What" section]

**Metrics:** [list with weights]
**Evaluation:** [strategy]
**Baseline:** [defined | WARNING: not defined]
**Falsification:** [criteria count] criteria defined

---

**Full objective:** `.planning/OBJECTIVE.md`

**Next steps:**
- Review OBJECTIVE.md for accuracy
- Run /grd:research to implement experiment (Phase 4)
```

**If baseline not defined:**
Display warning: "⚠️  WARNING: No baseline defined. Cannot claim improvement without comparison. Consider adding baseline to OBJECTIVE.md before proceeding."

**If critical validation issues:**
Display any warnings from architect agent (e.g., metric weights don't sum to 1.0, no falsification criteria)

</process>

<arguments>

**[direction]** (optional)
- Text describing what you want to test
- Examples: "Does feature X improve prediction?", "Can we reduce RMSE below 0.5?"
- If omitted, Architect will auto-propose from DATA_REPORT.md findings

**Flags:**

`--skip-data-check`
- Skip the DATA_REPORT.md soft gate warning
- Use when intentionally working without data reconnaissance

</arguments>

<examples>

**Auto-propose from data:**
```
/grd:architect
# Architect analyzes DATA_REPORT.md and proposes hypothesis
```

**User-directed hypothesis:**
```
/grd:architect "Can ensemble methods improve F1 over single models?"
# Architect starts from user's direction
```

**Skip data gate:**
```
/grd:architect --skip-data-check
# Proceed without DATA_REPORT.md warning
```

**Complex hypothesis:**
```
/grd:architect "Test if temporal features reduce false positives by 20% while maintaining recall above 0.85"
# Architect refines multi-metric hypothesis with user
```

</examples>

<output>

- `.planning/OBJECTIVE.md` — testable hypothesis with:
  - Context (problem, motivation, data characteristics, constraints)
  - Hypothesis (what, why, expected outcome)
  - Success metrics (weighted, with thresholds)
  - Evaluation methodology (strategy, parameters, statistical significance)
  - Baselines (own implementation or literature citations)
  - Falsification criteria (quantitative preferred)
  - Constraints and non-goals

</output>

<success_criteria>

- [ ] DATA_REPORT.md soft gate executed (warn if missing)
- [ ] Mode determined (auto-propose or user-directed)
- [ ] Architect agent spawned with appropriate context
- [ ] User can provide direction or receive auto-proposal
- [ ] OBJECTIVE.md generated with all required sections
- [ ] Summary presented with next steps
- [ ] Baseline warning issued if applicable

</success_criteria>
