---
name: grd:help
description: Show available GRD commands and usage guide
---

<objective>
Display the complete GRD command reference.

Output ONLY the reference content below. Do NOT add:

- Project-specific analysis
- Git status or file context
- Next-step suggestions
- Any commentary beyond the reference
  </objective>

<reference>
# GRD Command Reference

**GRD** (Get Research Done) creates hierarchical research plans optimized for hypothesis-driven ML experimentation with Claude Code.

## Quick Start

GRD supports multiple Claude-compatible runtimes: **Claude Code**, **OpenCode**, and **Gemini CLI**.

1. `/grd:new-project` - Initialize (questioning → research → requirements → roadmap)
2. `/grd:design-experiment 1` - Plan first experiment
3. `/grd:run-experiment 1` - Execute experiment
4. `/grd:validate-results 1` - Verify results
5. Repeat steps 2-4 for remaining experiments
6. `/grd:complete-study` - Archive study and prepare for next

## Staying Updated

GRD evolves fast. Update periodically:

```bash
npx get-research-done@latest
```

## Installation Options

GRD supports multiple Claude-compatible runtimes:

| Runtime | Flag | Config Directory |
|---------|------|------------------|
| Claude Code | `--claude` | `~/.claude/` |
| OpenCode | `--opencode` | `~/.opencode/` |
| Gemini CLI | `--gemini` | `~/.gemini/` |

**Examples:**

```bash
npx get-research-done --claude --global    # Claude Code only
npx get-research-done --gemini --global    # Gemini CLI only
npx get-research-done --both --global      # Claude Code + OpenCode
npx get-research-done --all --global       # All runtimes
```

**Gemini CLI Setup:**

For Gemini CLI, set the `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your-api-key"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Core Workflow

```
new-project → design-experiment → run-experiment → validate-results → repeat
                   |                                        |
                   v                                        v
            scope-experiment                         complete-study
            literature-review                           (when done)
```

## Commands by Category

### Lifecycle Commands

| Command | Description |
|---------|-------------|
| `/grd:new-project` | Initialize project with questioning → research → requirements → roadmap |
| `/grd:new-study` | Start new research study |
| `/grd:design-experiment` | Create detailed plan for experiment |
| `/grd:run-experiment` | Execute experiment plans |
| `/grd:validate-results` | Test experiment results through UAT |
| `/grd:complete-study` | Archive completed study |
| `/grd:audit-study` | Audit study against hypotheses |
| `/grd:plan-study-gaps` | Create experiments to close audit gaps |
| `/grd:progress` | Check status and route to next action |

### Research Commands

| Command | Description |
|---------|-------------|
| `/grd:scope-experiment` | Capture vision before planning |
| `/grd:literature-review` | Comprehensive ecosystem research |
| `/grd:list-experiment-assumptions` | See Claude's intended approach |
| `/grd:research` | General domain research |
| `/grd:architect` | Hypothesis synthesis from data |

### Data Commands

| Command | Description |
|---------|-------------|
| `/grd:explore` | Data reconnaissance and profiling |
| `/grd:evaluate` | Model evaluation with evidence packages |
| `/grd:insights` | Plain English data explanations |

### Roadmap Management

| Command | Description |
|---------|-------------|
| `/grd:add-experiment` | Add experiment to end of study |
| `/grd:insert-experiment` | Insert urgent experiment between existing |
| `/grd:remove-experiment` | Remove future experiment and renumber |

### Session Management

| Command | Description |
|---------|-------------|
| `/grd:pause-work` | Create context handoff |
| `/grd:resume-work` | Restore previous session |

### Quick Mode

| Command | Description |
|---------|-------------|
| `/grd:quick` | Execute small ad-hoc tasks |
| `/grd:quick-explore` | Fast data exploration |

### Todo Management

| Command | Description |
|---------|-------------|
| `/grd:add-todo` | Capture idea as todo |
| `/grd:check-todos` | List and select todos to work on |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/grd:help` | Show command reference |
| `/grd:update` | Update GRD to latest |
| `/grd:settings` | Configure workflow toggles |
| `/grd:set-profile` | Switch model profile |
| `/grd:debug` | Systematic debugging with persistence |
| `/grd:map-codebase` | Map existing codebase |
| `/grd:graduate` | Graduate notebook to production |

### Project Initialization

**`/grd:new-project`**
Initialize new project through unified flow.

One command takes you from idea to ready-for-planning:
- Deep questioning to understand what you're researching
- Optional domain research (spawns 4 parallel researcher agents)
- Requirements definition with v1/v2/out-of-scope scoping
- Roadmap creation with phase breakdown and success criteria

Creates all `.planning/` artifacts:
- `PROJECT.md` — vision and requirements
- `config.json` — workflow mode (interactive/yolo)
- `research/` — domain research (if selected)
- `REQUIREMENTS.md` — scoped requirements with REQ-IDs
- `ROADMAP.md` — phases mapped to requirements
- `STATE.md` — project memory

Usage: `/grd:new-project`

**`/grd:map-codebase`**
Map an existing codebase for brownfield projects.

- Analyzes codebase with parallel Explore agents
- Creates `.planning/codebase/` with 7 focused documents
- Covers stack, architecture, structure, conventions, testing, integrations, concerns
- Use before `/grd:new-project` on existing codebases

Usage: `/grd:map-codebase`

### Experiment Planning

**`/grd:scope-experiment <number>`**
Capture your vision for an experiment before planning.

- Captures how you imagine this experiment working
- Creates CONTEXT.md with your vision, essentials, and boundaries
- Use when you have ideas about how something should look/feel

Usage: `/grd:scope-experiment 2`

**`/grd:literature-review <number>`**
Comprehensive ecosystem research for niche/complex domains.

- Discovers standard stack, architecture patterns, pitfalls
- Creates RESEARCH.md with "how experts build this" knowledge
- Use for 3D, games, audio, shaders, ML, and other specialized domains
- Goes beyond "which library" to ecosystem knowledge

Usage: `/grd:literature-review 3`

**`/grd:list-experiment-assumptions <number>`**
See what Claude is planning to do for an experiment.

- Shows Claude's intended approach for an experiment
- Lets you course-correct if Claude misunderstood your vision
- No files created - conversational output only

Usage: `/grd:list-experiment-assumptions 3`

**`/grd:design-experiment <number>`**
Create detailed execution plan for an experiment.

- Generates `.planning/phases/XX-phase-name/XX-YY-PLAN.md`
- Breaks experiment into concrete, actionable tasks
- Includes verification criteria and success measures
- Multiple plans per experiment supported (XX-01, XX-02, etc.)

Usage: `/grd:design-experiment 1`
Result: Creates `.planning/phases/01-foundation/01-01-PLAN.md`

### Execution

**`/grd:run-experiment <experiment-number>`**
Execute all plans in an experiment.

- Groups plans by wave (from frontmatter), executes waves sequentially
- Plans within each wave run in parallel via Task tool
- Verifies experiment goal after all plans complete
- Updates REQUIREMENTS.md, ROADMAP.md, STATE.md

Usage: `/grd:run-experiment 5`

### Quick Mode

**`/grd:quick`**
Execute small, ad-hoc tasks with GRD guarantees but skip optional agents.

Quick mode uses the same system with a shorter path:
- Spawns planner + executor (skips researcher, checker, verifier)
- Quick tasks live in `.planning/quick/` separate from planned phases
- Updates STATE.md tracking (not ROADMAP.md)

Use when you know exactly what to do and the task is small enough to not need research or verification.

Usage: `/grd:quick`
Result: Creates `.planning/quick/NNN-slug/PLAN.md`, `.planning/quick/NNN-slug/SUMMARY.md`

### Study Management

**`/grd:add-experiment <description>`**
Add new experiment to end of current study.

- Appends to ROADMAP.md
- Uses next sequential number
- Updates experiment directory structure

Usage: `/grd:add-experiment "Add feature ablation experiment"`

**`/grd:insert-experiment <after> <description>`**
Insert urgent experiment between existing experiments.

- Creates intermediate experiment (e.g., 7.1 between 7 and 8)
- Useful for discovered work that must happen mid-study
- Maintains experiment ordering

Usage: `/grd:insert-experiment 7 "Fix critical data leak bug"`
Result: Creates Experiment 7.1

**`/grd:remove-experiment <number>`**
Remove a future experiment and renumber subsequent experiments.

- Deletes experiment directory and all references
- Renumbers all subsequent experiments to close the gap
- Only works on future (unstarted) experiments
- Git commit preserves historical record

Usage: `/grd:remove-experiment 17`
Result: Experiment 17 deleted, experiments 18-20 become 17-19

**`/grd:new-study <name>`**
Start a new research study through unified flow.

- Deep questioning to understand your research question
- Optional literature review (spawns 4 parallel researcher agents)
- Hypothesis definition with testable claims
- Study protocol creation with experiments and success criteria

Creates: HYPOTHESES.md, STUDY_PROTOCOL.md

Usage: `/grd:new-study "v2.0 Model Comparison"`

**`/grd:complete-study <version>`**
Archive completed study with findings.

- Creates STUDIES.md entry with hypothesis outcomes
- Archives protocol and findings to studies/ directory
- Documents which hypotheses were supported/rejected
- Creates git tag for the release

Usage: `/grd:complete-study 1.0.0`

**`/grd:audit-study [version]`**
Audit study against original hypotheses.

- Verifies all primary hypotheses were tested
- Checks methodology and statistical rigor
- Creates STUDY-AUDIT.md with gaps and limitations

Usage: `/grd:audit-study`

**`/grd:plan-study-gaps`**
Create experiments to close gaps from audit.

- Groups gaps into logical follow-up experiments
- Adds experiments to STUDY_PROTOCOL.md
- Ready for `/grd:design-experiment` on new experiments

Usage: `/grd:plan-study-gaps`

### Progress Tracking

**`/grd:progress`**
Check project status and intelligently route to next action.

- Shows visual progress bar and completion percentage
- Summarizes recent work from SUMMARY files
- Displays current position and what's next
- Lists key decisions and open issues
- Offers to execute next plan or create it if missing
- Detects 100% study completion

Usage: `/grd:progress`

### Session Management

**`/grd:resume-work`**
Resume work from previous session with full context restoration.

- Reads STATE.md for project context
- Shows current position and recent progress
- Offers next actions based on project state

Usage: `/grd:resume-work`

**`/grd:pause-work`**
Create context handoff when pausing work mid-phase.

- Creates .continue-here file with current state
- Updates STATE.md session continuity section
- Captures in-progress work context

Usage: `/grd:pause-work`

### Debugging

**`/grd:debug [issue description]`**
Systematic debugging with persistent state across context resets.

- Gathers symptoms through adaptive questioning
- Creates `.planning/debug/[slug].md` to track investigation
- Investigates using scientific method (evidence → hypothesis → test)
- Survives `/clear` — run `/grd:debug` with no args to resume
- Archives resolved issues to `.planning/debug/resolved/`

Usage: `/grd:debug "model training doesn't converge"`
Usage: `/grd:debug` (resume active session)

### Todo Management

**`/grd:add-todo [description]`**
Capture idea or task as todo from current conversation.

- Extracts context from conversation (or uses provided description)
- Creates structured todo file in `.planning/todos/pending/`
- Infers area from file paths for grouping
- Checks for duplicates before creating
- Updates STATE.md todo count

Usage: `/grd:add-todo` (infers from conversation)
Usage: `/grd:add-todo Add hyperparameter sweep experiment`

**`/grd:check-todos [area]`**
List pending todos and select one to work on.

- Lists all pending todos with title, area, age
- Optional area filter (e.g., `/grd:check-todos models`)
- Loads full context for selected todo
- Routes to appropriate action (work now, add to phase, brainstorm)
- Moves todo to done/ when work begins

Usage: `/grd:check-todos`
Usage: `/grd:check-todos models`

### User Acceptance Testing

**`/grd:validate-results [experiment]`**
Validate experiment results through conversational UAT.

- Extracts testable deliverables from SUMMARY.md files
- Presents tests one at a time (yes/no responses)
- Automatically diagnoses failures and creates fix plans
- Ready for re-execution if issues found

Usage: `/grd:validate-results 3`

### Configuration

**`/grd:settings`**
Configure workflow toggles and model profile interactively.

- Toggle researcher, plan checker, verifier agents
- Select model profile (quality/balanced/budget)
- Updates `.planning/config.json`

Usage: `/grd:settings`

**`/grd:set-profile <profile>`**
Quick switch model profile for GRD agents.

- `quality` — Opus everywhere except verification
- `balanced` — Opus for planning, Sonnet for execution (default)
- `budget` — Sonnet for writing, Haiku for research/verification

Usage: `/grd:set-profile budget`

### Utility Commands

**`/grd:help`**
Show this command reference.

**`/grd:update`**
Update GRD to latest version with changelog preview.

- Shows installed vs latest version comparison
- Displays changelog entries for versions you've missed
- Highlights breaking changes
- Confirms before running install
- Better than raw `npx get-research-done`

Usage: `/grd:update`

## Files & Structure

```
.planning/
├── PROJECT.md            # Project vision
├── ROADMAP.md            # Current phase breakdown
├── STATE.md              # Project memory & context
├── config.json           # Workflow mode & gates
├── todos/                # Captured ideas and tasks
│   ├── pending/          # Todos waiting to be worked on
│   └── done/             # Completed todos
├── debug/                # Active debug sessions
│   └── resolved/         # Archived resolved issues
├── codebase/             # Codebase map (brownfield projects)
│   ├── STACK.md          # Languages, frameworks, dependencies
│   ├── ARCHITECTURE.md   # Patterns, layers, data flow
│   ├── STRUCTURE.md      # Directory layout, key files
│   ├── CONVENTIONS.md    # Coding standards, naming
│   ├── TESTING.md        # Test setup, patterns
│   ├── INTEGRATIONS.md   # External services, APIs
│   └── CONCERNS.md       # Tech debt, known issues
└── phases/
    ├── 01-foundation/
    │   ├── 01-01-PLAN.md
    │   └── 01-01-SUMMARY.md
    └── 02-core-features/
        ├── 02-01-PLAN.md
        └── 02-01-SUMMARY.md
```

## Workflow Modes

Set during `/grd:new-project`:

**Guided Mode**

- Confirms each major decision
- Pauses at checkpoints for approval
- More guidance throughout

**Autonomous Mode**

- Auto-approves most decisions
- Executes plans without confirmation
- Only stops for critical checkpoints

Change anytime by editing `.planning/config.json`

## Planning Configuration

Configure how planning artifacts are managed in `.planning/config.json`:

**`planning.commit_docs`** (default: `true`)
- `true`: Planning artifacts committed to git (standard workflow)
- `false`: Planning artifacts kept local-only, not committed

When `commit_docs: false`:
- Add `.planning/` to your `.gitignore`
- Useful for OSS contributions, client projects, or keeping planning private
- All planning files still work normally, just not tracked in git

**`planning.search_gitignored`** (default: `false`)
- `true`: Add `--no-ignore` to broad ripgrep searches
- Only needed when `.planning/` is gitignored and you want project-wide searches to include it

Example config:
```json
{
  "planning": {
    "commit_docs": false,
    "search_gitignored": true
  }
}
```

## Common Workflows

**Starting a new project:**

```
/grd:new-project        # Unified flow: questioning → research → requirements → roadmap
/clear
/grd:design-experiment 1       # Create plans for first experiment
/clear
/grd:run-experiment 1    # Execute all plans in experiment
```

**Resuming work after a break:**

```
/grd:progress  # See where you left off and continue
```

**Adding urgent mid-study work:**

```
/grd:insert-experiment 5 "Critical data preprocessing fix"
/grd:design-experiment 5.1
/grd:run-experiment 5.1
```

**Completing a study:**

```
/grd:complete-study 1.0.0
/clear
/grd:new-study  # Start next study (questioning → research → requirements → roadmap)
```

**Capturing ideas during work:**

```
/grd:add-todo                    # Capture from conversation context
/grd:add-todo Try different loss function  # Capture with explicit description
/grd:check-todos                 # Review and work on todos
/grd:check-todos models          # Filter by area
```

**Debugging an issue:**

```
/grd:debug "model outputs NaN after epoch 3"  # Start debug session
# ... investigation happens, context fills up ...
/clear
/grd:debug                                    # Resume from where you left off
```

## Getting Help

- Read `.planning/PROJECT.md` for project vision
- Read `.planning/STATE.md` for current context
- Check `.planning/ROADMAP.md` for phase status
- Run `/grd:progress` to check where you're up to
  </reference>
