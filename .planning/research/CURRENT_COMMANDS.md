# GRD Command Structure Analysis

**Analyzed:** 2026-02-01
**Total Commands:** 33

## Full Command Inventory

| # | Command | Purpose | Creates | Requires | Next Up Suggestions |
|---|---------|---------|---------|----------|---------------------|
| 1 | `add-phase` | Add phase to end of current milestone | Phase directory, ROADMAP.md update | ROADMAP.md, STATE.md | `/grd:design-experiment {N}` |
| 2 | `add-todo` | Capture idea/task as todo | `.planning/todos/pending/*.md` | STATE.md (optional) | Continue work, add another, `/grd:check-todos` |
| 3 | `architect` | Synthesize testable hypotheses (ML Phase 3) | `.planning/OBJECTIVE.md` | PROJECT.md, DATA_REPORT.md (optional) | `/grd:research` |
| 4 | `audit-study` | Audit study completion against hypotheses | `v{version}-STUDY-AUDIT.md` | STUDY_PROTOCOL.md, HYPOTHESES.md, VERIFICATION.md files | `/grd:complete-study` or `/grd:plan-study-gaps` |
| 5 | `check-todos` | List and work on pending todos | Moves todo to `done/` | `.planning/todos/pending/` | Work on it, add to phase, brainstorm |
| 6 | `complete-study` | Archive completed study | `studies/v{version}-*.md` | STUDY_PROTOCOL.md, HYPOTHESES.md, v{version}-STUDY-AUDIT.md | `/grd:new-study` |
| 7 | `debug` | Systematic debugging with persistent state | `.planning/debug/*.md` | None | Fix now, plan fix, manual fix |
| 8 | `discuss-phase` | Gather phase context through questioning | `{phase}-CONTEXT.md` | STATE.md, ROADMAP.md | `/grd:research-phase` or `/grd:design-experiment` |
| 9 | `evaluate` | Human evaluation gate (ML Phase 5) | `DECISION.md`, `decision_log.md` | `SCORECARD.json` | Seal, Iterate, Archive |
| 10 | `execute-phase` | Execute all plans in a phase | `*-SUMMARY.md`, `*-VERIFICATION.md` | PLAN.md files, ROADMAP.md | `/grd:discuss-phase {Z+1}` or `/grd:audit-milestone` |
| 11 | `explore` | Analyze data for ML projects | `.planning/DATA_REPORT.md` | PROJECT.md | `/grd:architect` |
| 12 | `graduate` | Graduate notebook to production script | `src/experiments/*.py` | Notebook with PROCEED verdict | Review script, add tests |
| 13 | `help` | Show command reference | None | None | None |
| 14 | `insert-phase` | Insert decimal phase (e.g., 7.1) | Phase directory, ROADMAP.md update | ROADMAP.md, STATE.md | `/grd:design-experiment {N.M}` |
| 15 | `insights` | Generate plain English data insights | `DATA_REPORT.md`, `INSIGHTS_SUMMARY.md` | PROJECT.md | `/grd:architect` |
| 16 | `list-phase-assumptions` | Surface Claude's assumptions | None (conversational) | STATE.md, ROADMAP.md | `/grd:discuss-phase`, `/grd:design-experiment` |
| 17 | `map-codebase` | Analyze existing codebase | `.planning/codebase/*.md` (7 files) | Existing code files | `/grd:new-project` |
| 18 | `new-project` | Initialize new project | PROJECT.md, config.json, research/, REQUIREMENTS.md, ROADMAP.md, STATE.md | None | `/grd:design-experiment 1` |
| 19 | `new-study` | Start new research study | HYPOTHESES.md, STUDY_PROTOCOL.md | PROJECT.md, STATE.md | `/grd:design-experiment {N}` |
| 20 | `pause-work` | Create context handoff | `.continue-here.md` | STATE.md | `/grd:resume-work` |
| 21 | `plan-phase` | Create detailed execution plan | `*-PLAN.md`, `*-RESEARCH.md` | ROADMAP.md, STATE.md | `/grd:run-experiment` |
| 22 | `plan-study-gaps` | Create experiments to close audit gaps | STUDY_PROTOCOL.md update | v{version}-STUDY-AUDIT.md | `/grd:design-experiment {N}` |
| 23 | `progress` | Check project status and route | None | STATE.md, ROADMAP.md | Context-dependent routing |
| 24 | `quick-explore` | Fast EDA console summary | `DATA_REPORT.md` (quick mode) | PROJECT.md | `/grd:explore` or `/grd:architect` |
| 25 | `quick` | Execute ad-hoc task with GRD guarantees | `.planning/quick/NNN-*/PLAN.md, SUMMARY.md` | ROADMAP.md | `/grd:quick` |
| 26 | `remove-phase` | Remove future phase and renumber | ROADMAP.md update, directory deletion | ROADMAP.md, STATE.md | `/grd:progress` |
| 27 | `research-phase` | Research how to implement a phase (standalone) | `{phase}-RESEARCH.md` | ROADMAP.md | `/grd:design-experiment` |
| 28 | `research` | Implement ML experiments (Phase 4) | `experiments/run_NNN/` | OBJECTIVE.md | Review verdict, `/grd:evaluate` |
| 29 | `resume-work` | Resume from previous session | None | STATE.md | Context-dependent routing |
| 30 | `set-profile` | Switch model profile | config.json update | config.json | None |
| 31 | `settings` | Configure workflow toggles | config.json update | config.json | None |
| 32 | `update` | Update GRD to latest version | None | None | Restart Claude Code |
| 33 | `verify-work` | Validate features through UAT | `{phase}-UAT.md`, fix plans | SUMMARY.md files | `/grd:run-experiment --gaps-only` |

---

## Command Flow Diagrams

### Primary Development Workflow

```
/grd:new-project
       |
       v
+------+------+
|             |
v             v
/grd:map-codebase   (brownfield)
       |
       v
/grd:discuss-phase 1  (optional)
       |
       v
/grd:design-experiment 1
       |
       v
/grd:run-experiment 1
       |
       +---> /grd:validate-results 1 (optional)
       |              |
       |              v (if issues)
       |     /grd:run-experiment 1 --gaps-only
       |
       v
/grd:discuss-phase 2  OR  /grd:design-experiment 2
       |
       v
   ... repeat ...
       |
       v
/grd:complete-milestone (referenced but NOT in commands)
```

### ML/Research Workflow

```
/grd:new-project
       |
       v
/grd:explore  OR  /grd:quick-explore  OR  /grd:insights
       |
       v
/grd:architect
       |
       v
/grd:research  <--+
       |          |
       v          | (REVISE_METHOD/REVISE_DATA)
   Critic         |
       |          |
       +----------+
       | (PROCEED)
       v
/grd:evaluate
       |
       +---> Seal --> done
       +---> Iterate --> /grd:research --continue
       +---> Archive --> experiments/archive/
```

### Study Management Flow

```
/grd:new-study
       |
       v
/grd:design-experiment N
       |
       v
/grd:run-experiment N
       |
       v
   ... experiments ...
       |
       v
/grd:audit-study
       |
       +---> passed --> /grd:complete-study
       +---> gaps_found --> /grd:plan-study-gaps
                                    |
                                    v
                           /grd:design-experiment N
                                    |
                                    v
                           /grd:run-experiment N
                                    |
                                    v
                           /grd:audit-study (re-audit)
```

### Session Management Flow

```
/grd:pause-work
       |
       v
.continue-here.md created
       |
       v
/grd:resume-work  OR  /grd:progress
       |
       v
Context-dependent routing
```

---

## "Next Up" Reference Chains

### Commands That Reference Other Commands

| Command | References in "Next Up" |
|---------|-------------------------|
| `add-phase` | `plan-phase` |
| `add-todo` | `check-todos` |
| `architect` | `research` |
| `audit-study` | `complete-study`, `plan-study-gaps` |
| `complete-study` | `new-study` |
| `discuss-phase` | `research-phase`, `plan-phase` |
| `execute-phase` | `discuss-phase`, `plan-phase`, `verify-work`, `audit-milestone` |
| `explore` | `architect` |
| `insert-phase` | `plan-phase` |
| `insights` | `architect` |
| `list-phase-assumptions` | `discuss-phase`, `plan-phase` |
| `map-codebase` | `new-project` |
| `new-project` | `discuss-phase 1`, `plan-phase 1` |
| `new-study` | `discuss-phase`, `plan-phase` |
| `pause-work` | `resume-work` |
| `plan-phase` | `execute-phase` |
| `plan-study-gaps` | `plan-phase`, `audit-study`, `complete-study` |
| `progress` | `execute-phase`, `plan-phase`, `discuss-phase`, `complete-milestone`, `new-milestone` |
| `quick-explore` | `explore`, `architect` |
| `research-phase` | `plan-phase` |
| `research` | `research --continue`, `evaluate`, `explore`, `architect` |
| `verify-work` | `execute-phase --gaps-only`, `plan-phase --gaps`, `discuss-phase`, `audit-milestone`, `complete-milestone` |

---

## Broken Chains Identified

### 1. Missing Commands (Referenced but Don't Exist)

| Referenced Command | Referenced By | Issue |
|-------------------|---------------|-------|
| `/grd:audit-milestone` | `execute-phase`, `verify-work`, `progress` | **Command does not exist** |
| `/grd:complete-milestone` | `progress`, `verify-work` | **Command does not exist** |
| `/grd:new-milestone` | `progress` | **Command does not exist** |

### 2. Inconsistent Naming

| Issue | Details |
|-------|---------|
| `complete-study` vs `complete-milestone` | Studies are completed, but milestones are "completed" with a non-existent command |
| `audit-study` vs `audit-milestone` | Studies can be audited, but milestone audit doesn't exist |

### 3. Orphaned Commands

| Command | Issue |
|---------|-------|
| `graduate` | Only referenced in its own docs, no other command routes to it |
| `debug` | No command routes to it; standalone entry point |

### 4. Circular/Unclear Routes

| Flow | Issue |
|------|-------|
| `verify-work` -> `execute-phase --gaps-only` | Good, but `--gaps-only` is mentioned; the flag is `--gaps` in some places |
| `research` -> `explore` | REVISE_DATA suggests explore, but then says to run `architect` after |

---

## Artifact Mapping

### What Creates What

| Artifact | Created By | Consumed By |
|----------|-----------|-------------|
| `PROJECT.md` | `new-project` | All commands |
| `config.json` | `new-project`, `settings`, `set-profile` | All orchestrators |
| `ROADMAP.md` | `new-project` | `plan-phase`, `execute-phase`, `progress`, `verify-work` |
| `STATE.md` | `new-project` | All commands |
| `REQUIREMENTS.md` | `new-project` | `plan-phase`, `execute-phase` |
| `research/*.md` | `new-project` (phase 6) | `plan-phase` |
| `{phase}-CONTEXT.md` | `discuss-phase` | `plan-phase` |
| `{phase}-RESEARCH.md` | `plan-phase`, `research-phase` | `plan-phase` |
| `*-PLAN.md` | `plan-phase` | `execute-phase` |
| `*-SUMMARY.md` | `execute-phase` | `progress`, `verify-work`, `audit-study` |
| `*-VERIFICATION.md` | `execute-phase` | `audit-study` |
| `{phase}-UAT.md` | `verify-work` | `execute-phase --gaps-only` |
| `DATA_REPORT.md` | `explore`, `quick-explore`, `insights` | `architect`, `research` |
| `INSIGHTS_SUMMARY.md` | `insights` | Stakeholder sharing |
| `OBJECTIVE.md` | `architect` | `research` |
| `experiments/run_NNN/` | `research` | `evaluate` |
| `SCORECARD.json` | `research` (via Evaluator) | `evaluate` |
| `CRITIC_LOG.md` | `research` (via Critic) | `evaluate` |
| `DECISION.md` | `evaluate` | Archive |
| `HYPOTHESES.md` | `new-study` | `audit-study`, `complete-study` |
| `STUDY_PROTOCOL.md` | `new-study`, `plan-study-gaps` | `plan-phase`, `audit-study` |
| `v{version}-STUDY-AUDIT.md` | `audit-study` | `complete-study`, `plan-study-gaps` |
| `studies/v{version}-*.md` | `complete-study` | Historical reference |
| `codebase/*.md` | `map-codebase` | `new-project` |
| `todos/pending/*.md` | `add-todo` | `check-todos` |
| `todos/done/*.md` | `check-todos` | Archive |
| `debug/*.md` | `debug` | `debug` (resume) |
| `.continue-here.md` | `pause-work` | `resume-work` |
| `quick/NNN-*/` | `quick` | `quick` |

---

## Command Categories

### Project Lifecycle
- `new-project` - Start
- `map-codebase` - Analyze existing code (brownfield)
- `progress` - Status check
- `pause-work` / `resume-work` - Session management

### Phase Workflow
- `discuss-phase` - Gather context
- `list-phase-assumptions` - Preview Claude's approach
- `research-phase` - Domain research (standalone)
- `plan-phase` - Create plans
- `execute-phase` - Run plans
- `verify-work` - UAT validation

### Roadmap Management
- `add-phase` - Append phase
- `insert-phase` - Insert decimal phase
- `remove-phase` - Delete and renumber

### ML/Research Workflow
- `explore` - Full data profiling
- `quick-explore` - Fast EDA
- `insights` - Business-friendly insights
- `architect` - Hypothesis synthesis
- `research` - Experiment implementation
- `evaluate` - Human evaluation gate
- `graduate` - Notebook to script

### Study Management
- `new-study` - Start study
- `audit-study` - Verify study completion
- `plan-study-gaps` - Close audit gaps
- `complete-study` - Archive study

### Configuration
- `settings` - Interactive config
- `set-profile` - Quick profile switch
- `update` - Update GRD

### Utility
- `help` - Command reference
- `add-todo` / `check-todos` - Todo management
- `debug` - Debugging with state
- `quick` - Ad-hoc tasks

---

## Critical Gaps Summary

### Missing Commands (3)
1. **`/grd:audit-milestone`** - Referenced by 3 commands but doesn't exist
2. **`/grd:complete-milestone`** - Referenced by 3 commands but doesn't exist
3. **`/grd:new-milestone`** - Referenced by 1 command but doesn't exist

### Naming Inconsistencies
- "Study" vs "Milestone" terminology is confused in the workflow
- Some places say `--gaps`, others say `--gaps-only`

### Orphaned Commands
- `graduate` has no inbound routes from other commands
- `debug` is standalone (acceptable - it's an entry point)

### Workflow Integrity
- The primary development workflow breaks at milestone completion
- The ML workflow is mostly self-contained and complete
- Study management flow is complete but separate from milestone concept

---

## Recommendations

1. **Create missing milestone commands** or **remove milestone references**:
   - If milestones are deprecated in favor of studies, update all references
   - If milestones are still needed, create `audit-milestone`, `complete-milestone`, `new-milestone`

2. **Standardize flag naming**:
   - Use `--gaps` consistently (or `--gaps-only` consistently)

3. **Add routes to orphaned commands**:
   - `graduate` should be suggested after successful `evaluate` with Seal decision

4. **Clarify study vs milestone relationship**:
   - Document when to use studies (ML research) vs milestones (software development)
   - Or unify the concepts
