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

1. `/grd:new-project` - Initialize project (includes research, requirements, roadmap)
2. `/grd:design-experiment 1` - Create detailed plan for first phase
3. `/grd:run-experiment 1` - Execute the phase

## Staying Updated

GRD evolves fast. Update periodically:

```bash
npx get-research-done@latest
```

## Core Workflow

```
/grd:new-project → /grd:design-experiment → /grd:run-experiment → repeat
```

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

### Phase Planning

**`/grd:scope-experiment <number>`**
Help articulate your vision for a phase before planning.

- Captures how you imagine this phase working
- Creates CONTEXT.md with your vision, essentials, and boundaries
- Use when you have ideas about how something should look/feel

Usage: `/grd:scope-experiment 2`

**`/grd:research-phase <number>`**
Comprehensive ecosystem research for niche/complex domains.

- Discovers standard stack, architecture patterns, pitfalls
- Creates RESEARCH.md with "how experts build this" knowledge
- Use for 3D, games, audio, shaders, ML, and other specialized domains
- Goes beyond "which library" to ecosystem knowledge

Usage: `/grd:research-phase 3`

**`/grd:list-phase-assumptions <number>`**
See what Claude is planning to do before it starts.

- Shows Claude's intended approach for a phase
- Lets you course-correct if Claude misunderstood your vision
- No files created - conversational output only

Usage: `/grd:list-phase-assumptions 3`

**`/grd:design-experiment <number>`**
Create detailed execution plan for a specific phase.

- Generates `.planning/phases/XX-phase-name/XX-YY-PLAN.md`
- Breaks phase into concrete, actionable tasks
- Includes verification criteria and success measures
- Multiple plans per phase supported (XX-01, XX-02, etc.)

Usage: `/grd:design-experiment 1`
Result: Creates `.planning/phases/01-foundation/01-01-PLAN.md`

### Execution

**`/grd:run-experiment <phase-number>`**
Execute all plans in a phase.

- Groups plans by wave (from frontmatter), executes waves sequentially
- Plans within each wave run in parallel via Task tool
- Verifies phase goal after all plans complete
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

### Roadmap Management

**`/grd:add-experiment <description>`**
Add new experiment to end of current study.

- Appends to ROADMAP.md
- Uses next sequential number
- Updates phase directory structure

Usage: `/grd:add-experiment "Add feature ablation experiment"`

**`/grd:insert-phase <after> <description>`**
Insert urgent work as decimal phase between existing phases.

- Creates intermediate phase (e.g., 7.1 between 7 and 8)
- Useful for discovered work that must happen mid-study
- Maintains phase ordering

Usage: `/grd:insert-phase 7 "Fix critical data leak bug"`
Result: Creates Phase 7.1

**`/grd:remove-phase <number>`**
Remove a future phase and renumber subsequent phases.

- Deletes phase directory and all references
- Renumbers all subsequent phases to close the gap
- Only works on future (unstarted) phases
- Git commit preserves historical record

Usage: `/grd:remove-phase 17`
Result: Phase 17 deleted, phases 18-20 become 17-19

### Study Management

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

**`/grd:validate-results [phase]`**
Validate built features through conversational UAT.

- Extracts testable deliverables from SUMMARY.md files
- Presents tests one at a time (yes/no responses)
- Automatically diagnoses failures and creates fix plans
- Ready for re-execution if issues found

Usage: `/grd:verify-work 3`

### Study Auditing

**`/grd:audit-study [version]`**
Audit study completion against original intent.

- Reads all phase VERIFICATION.md files
- Checks requirements coverage
- Spawns integration checker for cross-phase wiring
- Creates STUDY-AUDIT.md with gaps and tech debt

Usage: `/grd:audit-study`

**`/grd:plan-study-gaps`**
Create phases to close gaps identified by audit.

- Reads STUDY-AUDIT.md and groups gaps into phases
- Prioritizes by requirement priority (must/should/nice)
- Adds gap closure phases to ROADMAP.md
- Ready for `/grd:design-experiment` on new phases

Usage: `/grd:plan-study-gaps`

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

**Interactive Mode**

- Confirms each major decision
- Pauses at checkpoints for approval
- More guidance throughout

**YOLO Mode**

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
/grd:design-experiment 1       # Create plans for first phase
/clear
/grd:run-experiment 1    # Execute all plans in phase
```

**Resuming work after a break:**

```
/grd:progress  # See where you left off and continue
```

**Adding urgent mid-study work:**

```
/grd:insert-phase 5 "Critical data preprocessing fix"
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
