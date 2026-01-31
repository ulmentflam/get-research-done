# Architecture: Command Cleanup & EDA Integration

**Domain:** ML research workflow tool (GRD) — command structure and EDA integration
**Researched:** 2026-01-30
**Confidence:** HIGH (existing codebase analysis)

## Executive Summary

GRD v1.1 needs to clean up legacy GSD commands that don't fit ML research workflows and add two accessible EDA commands (`quick-explore` and `insights`) to lower the barrier to data exploration. The current architecture has 32 unique commands with 32 duplicate files (64 total), a mix of generic project management (GSD heritage) and research-specific workflows. The recommended cleanup removes 8 GSD-specific commands, renames 4 phase/milestone concepts to research terminology, and integrates 2 new EDA commands as streamlined variations of the existing Explorer agent.

**Key architectural decision:** The new EDA commands are **variants of existing agents**, not new agent types. `quick-explore` spawns a constrained Explorer agent (depth=summary, no-leakage-check), and `insights` spawns Explorer with output format changes (business-friendly language, executive summary focus). This preserves the proven agent architecture while adding accessibility layers.

**Integration points:**
- Commands live in `.claude/commands/grd/` (standard command layer)
- Both new commands spawn `grd-explorer` agent with mode flags
- Explorer agent gains `--mode=quick|insights` parameter support
- No new artifact types — both write to `.planning/DATA_REPORT.md` with section headers
- Fit into existing workflow: user can run quick-explore → insights → full explore as progressive depth

## Current Command Landscape

### Inventory (32 unique commands)

**Categorized by purpose:**

```
Research Loop (GRD Core) — 6 commands
├── explore.md                    # Full EDA with Explorer agent
├── architect.md                  # Hypothesis synthesis
├── research.md                   # Experiment implementation + Critic
├── evaluate.md                   # Human decision gate
├── graduate.md                   # Notebook → script conversion
└── map-codebase.md              # Brownfield analysis (4 parallel agents)

Project Lifecycle — 3 commands
├── new-project.md               # Greenfield init (questioning → research → roadmap)
├── new-milestone.md             # Subsequent milestone init
└── complete-milestone.md        # Archive milestone, tag release

Phase Management (GSD Heritage) — 8 commands
├── plan-phase.md                # Create PLAN.md for phase
├── execute-phase.md             # Execute all plans in phase
├── verify-work.md               # UAT for phase deliverables
├── discuss-phase.md             # Capture user vision before planning
├── research-phase.md            # Domain research before planning
├── list-phase-assumptions.md    # Show Claude's plan before executing
├── add-phase.md                 # Append phase to roadmap
├── insert-phase.md              # Insert decimal phase (7.1 between 7 and 8)
└── remove-phase.md              # Delete and renumber future phases

Roadmap Management (GSD Heritage) — 2 commands
├── audit-milestone.md           # Check requirements coverage
└── plan-milestone-gaps.md       # Create phases for audit gaps

Session Management — 2 commands
├── pause-work.md                # Create .continue-here file
└── resume-work.md               # Restore from STATE.md

Todo Management — 2 commands
├── add-todo.md                  # Capture idea with context
└── check-todos.md               # List and work on todos

Utilities — 9 commands
├── help.md                      # Command reference
├── progress.md                  # Status + intelligent routing
├── settings.md                  # Interactive config
├── set-profile.md               # Quick model profile switch
├── debug.md                     # Systematic debugging with state
├── quick.md                     # Ad-hoc task (planner + executor, no agents)
├── update.md                    # Update GRD with changelog
└── join-discord.md              # Community link
```

### Duplicate File Issue

**Problem:** 32 commands have " 2.md" duplicates (64 files total)

```bash
$ ls .claude/commands/grd/ | wc -l
      64

$ ls .claude/commands/grd/ | grep " 2.md" | wc -l
      32
```

**Likely cause:** Filesystem collision during installation or git merge artifact

**Resolution:** Delete all " 2.md" files — they're exact duplicates

```bash
find .claude/commands/grd/ -name "* 2.md" -delete
```

## Command Categorization: Keep vs Remove

### Keep As-Is (Research-Relevant) — 22 commands

These align with ML research workflows and should remain unchanged:

**Research Loop (6):**
- `explore`, `architect`, `research`, `evaluate`, `graduate`, `map-codebase`
- Core GRD workflow — no changes needed

**Project/Milestone Lifecycle (3):**
- `new-project`, `new-milestone`, `complete-milestone`
- Essential initialization and archival

**Research Planning (3):**
- `discuss-phase`, `research-phase`, `list-phase-assumptions`
- GRD uses phases to structure research roadmaps — valuable context gathering

**Execution (2):**
- `execute-phase`, `verify-work`
- Standard orchestration for roadmap execution

**Session/Todo (4):**
- `pause-work`, `resume-work`, `add-todo`, `check-todos`
- Universal workflow utilities

**Utilities (4):**
- `help`, `progress`, `settings`, `set-profile`
- Core UX and configuration

### Rename (Research Terminology) — 4 commands

Replace "phase/milestone" with research-appropriate terms:

| Current Name | New Name | Rationale |
|--------------|----------|-----------|
| `plan-phase` | `plan-phase` | Keep — "phase" is appropriate for research roadmap structure (Phase 1: Data Recon, Phase 2: Baseline, etc.) |
| `add-phase` | `add-phase` | Keep — adding phases to research roadmap is standard |
| `insert-phase` | `insert-phase` | Keep — urgent research work mid-roadmap is valid |
| `remove-phase` | `remove-phase` | Keep — removing future phases from roadmap is valid |

**Decision:** NO RENAMES NEEDED. "Phase" and "milestone" are appropriate for research workflows:
- **Phase** = stage in research roadmap (data recon, baseline, hypothesis testing)
- **Milestone** = version/cycle boundary (v1.0 = baseline model, v1.1 = feature engineering)

Research projects have phases and milestones just like software projects. The terminology is correct.

### Remove (GSD-Specific) — 2 commands

Pure project management commands that don't fit ML research:

| Command | Why Remove | Alternative |
|---------|------------|-------------|
| `audit-milestone.md` | Checks requirements coverage against ROADMAP.md — software-centric metric | Research uses `evaluate` to assess hypothesis validation, not requirement completion |
| `plan-milestone-gaps.md` | Creates phases to close audit gaps — assumes requirements-driven planning | Research is hypothesis-driven, not gap-driven |

**Removal strategy:**
- Delete command files
- No git history cleanup (preserved in pre-v1.1 tags)
- Update `help.md` to remove references

### Questionable — 4 commands

Commands where value for research workflows is unclear:

| Command | Research Relevance | Keep or Remove? |
|---------|-------------------|-----------------|
| `quick.md` | Ad-hoc task execution (planner + executor, skip agents) | **KEEP** — useful for quick fixes, utility scripts, non-research tasks during project |
| `debug.md` | Systematic debugging with persistent state | **KEEP** — debugging experiments is research work (why did model diverge?) |
| `update.md` | Update GRD with changelog preview | **KEEP** — standard utility |
| `join-discord.md` | Community link | **KEEP** — user support |

**Decision:** Keep all 4. They're general utilities that apply to any Claude Code project.

## New EDA Commands Architecture

### Command 1: `/grd:quick-explore`

**Purpose:** Lightweight EDA for rapid data familiarization

**Target user:** Researcher who wants quick stats before deciding whether full EDA is needed

**How it works:**
1. User runs `/grd:quick-explore ./data/train.csv`
2. Command spawns `grd-explorer` agent with flags:
   ```
   --mode=quick
   --depth=summary
   --no-leakage-check
   --no-anomaly-examples
   ```
3. Explorer runs constrained analysis:
   - Data shape, column types, memory usage
   - Summary statistics (mean, median, std, quantiles)
   - Missing data counts (no MCAR/MAR/MNAR classification)
   - Class balance (if target column specified)
   - Skip: outlier detection, leakage detection, correlation matrix
4. Writes `.planning/DATA_REPORT.md` with section header:
   ```markdown
   # Data Report (Quick Explore)

   **Generated:** [timestamp]
   **Mode:** Quick (summary statistics only)
   **Dataset:** ./data/train.csv

   For full analysis, run `/grd:explore ./data/train.csv`

   ## Data Overview
   [summary stats]
   ```

**Duration:** 30-60 seconds vs 5-15 minutes for full explore

**Output artifact:** `.planning/DATA_REPORT.md` (quick mode header)

**Integration points:**
- Gating: No soft gate on `architect` — quick mode is not sufficient for hypothesis formation
- Progression: User can run `quick-explore` → `explore` to upgrade to full analysis
- Critic: If Critic returns REVISE_DATA, it routes to full `explore`, not `quick-explore`

**Implementation notes:**
- Reuse existing Explorer agent code with mode parameter
- No new agent file needed — add mode detection to `grd-explorer.md`
- Command file is thin orchestration layer

### Command 2: `/grd:insights`

**Purpose:** Business-friendly EDA output for stakeholders

**Target user:** Non-technical stakeholder (PM, executive) who needs data understanding without statistical jargon

**How it works:**
1. User runs `/grd:insights ./data/train.csv`
2. Command spawns `grd-explorer` agent with flags:
   ```
   --mode=insights
   --depth=full
   --output-style=business
   ```
3. Explorer runs full analysis (same as `/grd:explore`) but transforms output:
   - Replace statistical terms with plain language
   - Add executive summary section (3-4 bullet points)
   - Focus on actionable insights, not raw numbers
   - Include "What This Means" explanations for each section
   - Visualizations as markdown tables (no code blocks)
4. Writes `.planning/DATA_REPORT.md` with section header:
   ```markdown
   # Data Insights Report

   **Generated:** [timestamp]
   **Mode:** Business Insights
   **Dataset:** ./data/train.csv

   ## Executive Summary

   - [Key finding 1 in plain language]
   - [Key finding 2]
   - [Key finding 3]
   - [Critical risk or recommendation]

   ## What We're Working With
   [data overview without jargon]

   ## What Stands Out
   [anomalies and patterns in stakeholder language]

   ## What Could Go Wrong
   [risks without statistical terminology]
   ```

**Duration:** Same as full explore (5-15 minutes) — same analysis, different output format

**Output artifact:** `.planning/DATA_REPORT.md` (insights mode header)

**Integration points:**
- Gating: Counts as full EDA for `architect` soft gate (mode=insights runs full analysis)
- Critic: If Critic returns REVISE_DATA, routes to full `explore` (not insights)
- Progression: Insights is parallel to explore, not a step before/after

**Language transformation examples:**

| Statistical Term | Business-Friendly |
|------------------|------------------|
| "Mean: 42.3, Std: 15.8" | "Typical value is 42, with most entries between 26 and 58" |
| "Skewness: 2.4" | "Most values cluster at the low end, with a few very high outliers" |
| "Class imbalance: 95/5 ratio" | "Only 5% of cases are positive — model might struggle to detect them" |
| "High correlation (r=0.87)" | "These two factors almost always move together" |
| "MCAR missing data" | "Missing values appear random, likely safe to ignore" |
| "Temporal leakage risk" | "Warning: Data from the future might be leaking into predictions" |

**Implementation notes:**
- Reuse existing Explorer agent code with output transformation layer
- Add business language templates to Explorer agent
- Executive summary generation requires LLM call (Sonnet sufficient)

## Recommended Command Structure (v1.1)

### Final Count: 32 commands (2 removed, 2 added)

**Research Loop (8 commands):**
- `explore` — Full EDA with Explorer agent
- `quick-explore` — **NEW** — Lightweight EDA (summary stats only)
- `insights` — **NEW** — Business-friendly EDA output
- `architect` — Hypothesis synthesis
- `research` — Experiment implementation + Critic
- `evaluate` — Human decision gate
- `graduate` — Notebook → script conversion
- `map-codebase` — Brownfield analysis

**Project Lifecycle (3 commands):**
- `new-project` — Greenfield init
- `new-milestone` — Subsequent milestone init
- `complete-milestone` — Archive milestone

**Phase Management (8 commands):**
- `plan-phase` — Create PLAN.md for phase
- `execute-phase` — Execute all plans in phase
- `verify-work` — UAT for phase deliverables
- `discuss-phase` — Capture user vision
- `research-phase` — Domain research before planning
- `list-phase-assumptions` — Show Claude's plan
- `add-phase` — Append phase to roadmap
- `insert-phase` — Insert decimal phase
- `remove-phase` — Delete and renumber future phases

**Session Management (2 commands):**
- `pause-work` — Create .continue-here file
- `resume-work` — Restore from STATE.md

**Todo Management (2 commands):**
- `add-todo` — Capture idea
- `check-todos` — List and work on todos

**Utilities (9 commands):**
- `help` — Command reference
- `progress` — Status + intelligent routing
- `settings` — Interactive config
- `set-profile` — Quick model profile switch
- `debug` — Systematic debugging
- `quick` — Ad-hoc task execution
- `update` — Update GRD
- `join-discord` — Community link

**Removed (2 commands):**
- ~~`audit-milestone`~~ — Software-centric requirements coverage
- ~~`plan-milestone-gaps`~~ — Gap-driven planning (research is hypothesis-driven)

## Integration with Existing Architecture

### Agent Spawn Patterns

**Existing pattern (from `/grd:explore`):**

```markdown
<process>
## Step 1: Validate Input

Check that data path exists and is readable.

## Step 2: Spawn Explorer Agent

Task(
  prompt="
  <data_path>$ARGUMENTS</data_path>
  <mode>full</mode>
  <depth>comprehensive</depth>
  <output>.planning/DATA_REPORT.md</output>

  Run full EDA. See grd-explorer.md for instructions.
  ",
  subagent_type="grd-explorer",
  model="sonnet",
  description="Explore dataset"
)
```

**New pattern for `/grd:quick-explore`):**

```markdown
<process>
## Step 1: Validate Input

Check that data path exists and is readable.

## Step 2: Spawn Explorer Agent (Quick Mode)

Task(
  prompt="
  <data_path>$ARGUMENTS</data_path>
  <mode>quick</mode>
  <depth>summary</depth>
  <leakage_check>false</leakage_check>
  <anomaly_examples>false</anomaly_examples>
  <output>.planning/DATA_REPORT.md</output>

  Run quick EDA (summary statistics only). See grd-explorer.md for instructions.
  ",
  subagent_type="grd-explorer",
  model="sonnet",
  description="Quick explore dataset"
)
```

**New pattern for `/grd:insights`):**

```markdown
<process>
## Step 1: Validate Input

Check that data path exists and is readable.

## Step 2: Spawn Explorer Agent (Insights Mode)

Task(
  prompt="
  <data_path>$ARGUMENTS</data_path>
  <mode>insights</mode>
  <depth>full</depth>
  <output_style>business</output_style>
  <executive_summary>true</executive_summary>
  <output>.planning/DATA_REPORT.md</output>

  Run full EDA with business-friendly output. See grd-explorer.md for instructions.
  ",
  subagent_type="grd-explorer",
  model="sonnet",
  description="Generate data insights"
)
```

### Explorer Agent Modifications

**Current `grd-explorer.md` structure:**

```markdown
---
name: grd-explorer
description: Analyzes raw data and generates DATA_REPORT.md
tools: Read, Write, Bash, Glob, Grep
color: blue
---

<role>
You are the GRD Explorer agent. Your job is data reconnaissance.
</role>

<execution_flow>
## Step 0: Detect Analysis Mode
[existing: initial vs revision]

## Step 1: Load and Validate Data
[existing: pandas loading, validation]

## Step 2: Data Overview
[existing: shape, types, memory]

## Step 3: Statistical Profiling
[existing: summary stats, distributions]

...
```

**Required modifications:**

```markdown
<execution_flow>
## Step 0: Detect Analysis Mode

**Mode detection from task prompt:**

Parse `<mode>` tag from spawn prompt:
- `full` — Full EDA (default)
- `quick` — Summary statistics only
- `insights` — Full EDA with business-friendly output
- `revision` — Targeted re-analysis (existing)

Parse additional flags:
- `<depth>`: summary | comprehensive
- `<leakage_check>`: true | false
- `<anomaly_examples>`: true | false
- `<output_style>`: technical | business
- `<executive_summary>`: true | false

**Mode-specific behavior:**

| Mode | Steps to Run | Output Format | Duration |
|------|-------------|---------------|----------|
| quick | 1-3 only | Technical, condensed | 30-60s |
| full | 1-9 | Technical, comprehensive | 5-15m |
| insights | 1-9 | Business-friendly | 5-15m |
| revision | Targeted subset | Technical, appended | 1-5m |

## Step 1: Load and Validate Data
[unchanged]

## Step 2: Data Overview
[unchanged]

## Step 3: Statistical Profiling
[unchanged]

## Step 4: Distribution Analysis
**If mode == 'quick': SKIP**
[existing code]

## Step 5: Missing Data Patterns
**If mode == 'quick': Only counts, skip MCAR/MAR/MNAR**
[existing code with conditional depth]

## Step 6: Outlier Detection
**If mode == 'quick': SKIP**
[existing code]

## Step 7: Class Balance Analysis
[unchanged — always run if target specified]

## Step 8: Data Leakage Detection
**If leakage_check == false: SKIP**
[existing code]

## Step 9: Write DATA_REPORT.md

**Output transformation based on mode:**

if output_style == 'business':
    - Generate executive summary (3-4 bullets)
    - Transform statistical terms to plain language
    - Add "What This Means" sections
    - Use stakeholder-friendly headers

if mode == 'quick':
    - Add "Quick Explore" header
    - Include note about running full explore
    - Omit skipped sections

[Write file logic]
```

### File System Changes

**New command files:**
```
.claude/commands/grd/
├── quick-explore.md    # NEW — Thin orchestration layer
└── insights.md         # NEW — Thin orchestration layer
```

**Modified agent files:**
```
agents/
└── grd-explorer.md     # MODIFIED — Add mode detection and output transformation
```

**Deleted command files:**
```
.claude/commands/grd/
├── audit-milestone.md          # REMOVE
├── plan-milestone-gaps.md      # REMOVE
└── * 2.md (32 duplicates)      # REMOVE ALL
```

**No new artifact types:**
- All three explore variants write to `.planning/DATA_REPORT.md`
- Section headers differentiate mode
- Existing Architect soft gate reads DATA_REPORT.md (any mode)

## Workflow Integration

### Progressive Exploration Path

**User journey:**

```
Initial familiarity → Quick decision → Full analysis → Stakeholder communication

/grd:quick-explore data.csv
  ↓ (30 seconds)
  "Dataset looks reasonable, proceed to full EDA"

/grd:explore data.csv
  ↓ (10 minutes)
  "Identified class imbalance and temporal leakage risks"

/grd:insights data.csv
  ↓ (10 minutes, different output)
  "Generated stakeholder-friendly report for PM review"
```

**Alternative paths:**

```
Path 1: Skip quick, go straight to full
/grd:explore → /grd:architect

Path 2: Insights only (stakeholder first)
/grd:insights → share with PM → /grd:explore → /grd:architect

Path 3: Quick check, abort if data is wrong
/grd:quick-explore → "Dataset is corrupt, fix data" → no further steps
```

### Gating Behavior

**Soft gate on `/grd:architect`:**

Current behavior:
```markdown
If DATA_REPORT.md missing:
  Warn: "No DATA_REPORT.md found. Run /grd:explore first (recommended)."
  Offer: "Continue anyway" | "Run explore first"
```

Proposed behavior:
```markdown
If DATA_REPORT.md missing:
  Warn: "No DATA_REPORT.md found. Run /grd:explore or /grd:quick-explore first."
  Offer: "Continue anyway" | "Run explore" | "Run quick-explore"

If DATA_REPORT.md exists but mode=quick:
  Warn: "Only quick explore completed. Full EDA recommended before hypothesis."
  Offer: "Continue anyway" | "Run full explore"

If DATA_REPORT.md exists and mode in [full, insights]:
  Proceed without warning (both modes run full analysis)
```

### Critic Routing

**REVISE_DATA exit code:**

Current behavior:
```markdown
If Critic returns REVISE_DATA:
  Route to: /grd:explore (targeted re-analysis)
```

Proposed behavior:
```markdown
If Critic returns REVISE_DATA:
  Route to: /grd:explore (full analysis, revision mode)

  Never route to quick-explore or insights —
  revision mode needs comprehensive re-analysis
```

**Reasoning:** Quick explore is insufficient for validating Critic concerns. Insights mode is for stakeholder communication, not validation.

## Build Order

### Phase 1: Cleanup (1-2 hours)

**Priority:** Clear technical debt before adding features

**Tasks:**
1. Delete all " 2.md" duplicate files
   ```bash
   find .claude/commands/grd/ -name "* 2.md" -delete
   git add .claude/commands/grd/
   git commit -m "chore: remove duplicate command files"
   ```

2. Delete GSD-specific commands
   ```bash
   rm .claude/commands/grd/audit-milestone.md
   rm .claude/commands/grd/plan-milestone-gaps.md
   git add .claude/commands/grd/
   git commit -m "chore: remove GSD-specific commands not relevant to research"
   ```

3. Update `help.md`
   - Remove references to deleted commands
   - Add placeholder entries for new commands (coming in Phase 2)
   ```bash
   git add .claude/commands/grd/help.md
   git commit -m "docs: update help after command cleanup"
   ```

**Verification:**
- `ls .claude/commands/grd/ | wc -l` should show 30 (32 unique - 2 removed, no duplicates)
- `/grd:help` should not reference deleted commands

### Phase 2: Add `/grd:quick-explore` (3-4 hours)

**Priority:** Simpler of the two new commands (no output transformation)

**Tasks:**
1. Modify `agents/grd-explorer.md`
   - Add mode detection (Step 0)
   - Add conditional skipping (Steps 4, 6, 8)
   - Add quick mode output header (Step 9)
   - Test: Manual spawn with `--mode=quick`

2. Create `.claude/commands/grd/quick-explore.md`
   - Thin orchestration layer
   - Parse data path argument
   - Spawn Explorer with quick mode flags
   - Test: `/grd:quick-explore ./data/sample.csv`

3. Update `help.md`
   - Add quick-explore entry in Research Loop section
   - Document when to use (rapid familiarization)

**Verification:**
- Quick explore completes in <60 seconds
- DATA_REPORT.md contains "Quick Explore" header
- Skipped sections are absent (outliers, leakage, anomaly examples)
- Architect soft gate warns about quick mode

### Phase 3: Add `/grd:insights` (4-6 hours)

**Priority:** More complex (output transformation required)

**Tasks:**
1. Modify `agents/grd-explorer.md`
   - Add insights mode detection
   - Add business language transformation templates
   - Add executive summary generation (LLM call)
   - Add "What This Means" sections
   - Test: Manual spawn with `--mode=insights`

2. Create `.claude/commands/grd/insights.md`
   - Thin orchestration layer
   - Parse data path argument
   - Spawn Explorer with insights mode flags
   - Test: `/grd:insights ./data/sample.csv`

3. Update `help.md`
   - Add insights entry in Research Loop section
   - Document when to use (stakeholder communication)

**Verification:**
- Insights output uses plain language (no "skewness", "MCAR", etc.)
- Executive summary is 3-4 actionable bullets
- Duration matches full explore (5-15 minutes)
- Architect soft gate accepts insights mode as full EDA

### Phase 4: Integration Testing (2-3 hours)

**Priority:** Validate workflow paths and gating

**Test scenarios:**
1. Progressive path: quick-explore → explore → architect
2. Insights path: insights → architect (should proceed without warning)
3. Quick-only path: quick-explore → architect (should warn)
4. Critic routing: research → REVISE_DATA → explore (not quick-explore)
5. Overwrite behavior: quick-explore → explore (should replace, not append)

**Regression tests:**
1. Existing explore still works without flags
2. Critic revision mode still routes correctly
3. Help command shows all 32 commands

**Documentation:**
- Update README.md with new command descriptions
- Add examples to CHANGELOG.md

## Component Boundaries

### Command Layer (Orchestration)

**Responsibilities:**
- Parse user arguments
- Validate prerequisites (data file exists, project initialized)
- Spawn agents with context
- No business logic (agent does the work)

**Example (quick-explore.md):**
```markdown
<process>
1. Parse $ARGUMENTS for data path
2. Validate file exists
3. Spawn grd-explorer with --mode=quick
4. Wait for completion
5. Display summary ("Quick explore complete, see .planning/DATA_REPORT.md")
</process>
```

### Agent Layer (Execution)

**Responsibilities:**
- Receive mode flags from orchestrator
- Execute analysis based on mode
- Write output artifacts
- Return structured result

**Example (grd-explorer.md Step 0):**
```python
mode = parse_mode_from_prompt()  # 'quick' | 'full' | 'insights' | 'revision'
depth = parse_depth_from_prompt()  # 'summary' | 'comprehensive'
leakage_check = parse_flag('leakage_check', default=True)

if mode == 'quick':
    skip_steps = [4, 6, 8]  # Distribution, outlier, leakage
    output_header = "# Data Report (Quick Explore)"
elif mode == 'insights':
    skip_steps = []
    output_style = 'business'
    generate_executive_summary = True
```

### Output Layer (Artifacts)

**Responsibilities:**
- Single source of truth for data understanding
- Mode-differentiated headers
- Consumed by downstream commands (Architect, Critic)

**Example (.planning/DATA_REPORT.md):**
```markdown
# Data Report (Quick Explore)

**Generated:** 2026-01-30 14:32:00
**Mode:** Quick (summary statistics only)
**Dataset:** ./data/train.csv

For full analysis, run `/grd:explore ./data/train.csv`

## Data Overview
- Rows: 10,000
- Columns: 15 (8 numeric, 7 categorical)
- Memory: 1.2 MB

## Summary Statistics
[table]

## Missing Data
- Total missing: 234 values (1.5% of dataset)
- Affected columns: age (120), income (114)

## Class Balance
- Target column: 'label'
- Distribution: 7,200 class_0 (72%), 2,800 class_1 (28%)
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: New Agent Types
**What NOT to do:** Create `grd-quick-explorer.md` and `grd-insights-explorer.md` as separate agents

**Why bad:**
- Code duplication (3 nearly identical agents)
- Maintenance burden (bug fixes require 3 changes)
- Architecture bloat (adds complexity without value)

**Instead:** Single Explorer agent with mode parameter

### Anti-Pattern 2: New Artifact Types
**What NOT to do:** Write to `.planning/QUICK_REPORT.md` and `.planning/INSIGHTS_REPORT.md`

**Why bad:**
- Architect needs to check 3 files instead of 1
- Inconsistent gating (which file counts as "explored"?)
- User confusion (which report is current?)

**Instead:** Single DATA_REPORT.md with section headers

### Anti-Pattern 3: Over-Parameterization
**What NOT to do:** Add 10+ flags for granular control (--skip-outliers, --skip-correlation, --skip-missing, etc.)

**Why bad:**
- Combinatorial explosion (100+ possible configurations)
- User decision fatigue ("Which flags do I need?")
- Maintenance nightmare (test all combinations)

**Instead:** Three modes with opinionated defaults

### Anti-Pattern 4: Mode Drift
**What NOT to do:** Let users override mode behavior (quick mode + full leakage check)

**Why bad:**
- Defeats purpose of modes (quick is no longer quick)
- Unexpected behavior (why did quick take 10 minutes?)
- Documentation burden (explain all overrides)

**Instead:** Modes are immutable profiles (quick = fast, full = comprehensive)

### Anti-Pattern 5: Renaming Existing Commands
**What NOT to do:** Rename `plan-phase` to `plan-research-phase`, `new-milestone` to `new-research-cycle`

**Why bad:**
- Breaks existing user muscle memory
- Git history confusion (command appears deleted)
- No benefit (phase/milestone are correct terms)

**Instead:** Keep existing names (phase and milestone apply to research)

## Success Criteria

**Command cleanup complete when:**
- [ ] Zero " 2.md" duplicate files remain
- [ ] `audit-milestone` and `plan-milestone-gaps` removed
- [ ] `help.md` updated to reflect removals
- [ ] Command count: 30 unique files in `.claude/commands/grd/`

**quick-explore complete when:**
- [ ] Command file created (`.claude/commands/grd/quick-explore.md`)
- [ ] Explorer agent modified (mode detection + conditional skipping)
- [ ] Quick explore completes in <60 seconds on 100K row dataset
- [ ] DATA_REPORT.md contains "Quick Explore" header
- [ ] Architect warns if only quick mode completed
- [ ] Help entry added

**insights complete when:**
- [ ] Command file created (`.claude/commands/grd/insights.md`)
- [ ] Explorer agent modified (business language transformation)
- [ ] Insights output uses plain language (no statistical jargon)
- [ ] Executive summary generated (3-4 actionable bullets)
- [ ] Duration matches full explore (full analysis, different output)
- [ ] Architect accepts insights mode as full EDA
- [ ] Help entry added

**Integration verified when:**
- [ ] Progressive path works (quick → explore → architect)
- [ ] Insights path works (insights → architect, no warning)
- [ ] Quick-only warns (quick → architect, soft gate triggered)
- [ ] Critic routes to full explore (REVISE_DATA never goes to quick)
- [ ] Overwrite behavior correct (quick → explore replaces)
- [ ] Existing explore unchanged (no regression)
- [ ] All tests pass

## Open Questions

**Q1: Should quick-explore check for leakage at all?**
- **Argument for:** Leakage is critical, shouldn't be skipped even in quick mode
- **Argument against:** Leakage checks are slow (correlation matrix), defeats "quick" purpose
- **Recommendation:** Skip in quick mode. User can run full explore if concerned. Document this clearly.

**Q2: Should insights mode generate visualizations?**
- **Argument for:** Charts are more accessible than tables for non-technical stakeholders
- **Argument against:** GRD is text-first (portability), visualizations require matplotlib/plotly
- **Recommendation:** Defer to v1.2. Use markdown tables with ASCII art for now (e.g., `█████░░░░░ 50%`).

**Q3: Can user run insights → quick-explore (reverse order)?**
- **Behavior:** Yes, but quick will overwrite insights report
- **Warning:** Command should detect existing report mode and warn before overwrite
- **Recommendation:** Add overwrite warning to both commands.

**Q4: Should removed commands redirect users?**
- **Example:** `/grd:audit-milestone` → "This command was removed. Use `/grd:evaluate` instead."
- **Implementation:** Keep stub command files with error messages
- **Recommendation:** No redirects. Clean removal. If users run deleted commands, error is clear ("command not found"). Update messaging in CHANGELOG.

**Q5: Should help.md group commands by workflow stage?**
- **Current:** Flat list by category (Research Loop, Lifecycle, etc.)
- **Alternative:** Workflow sequence (Project Init → Planning → Execution → Evaluation)
- **Recommendation:** Keep current structure. Users understand categorical grouping better than workflow sequences (not everyone follows linear paths).

---

*Architecture analysis: 2026-01-30*
*Ready for roadmap creation: Yes*
