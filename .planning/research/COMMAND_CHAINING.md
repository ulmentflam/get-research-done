# Command Chaining and Workflow Orchestration Research

**Researched:** 2026-02-01
**Focus:** How should commands chain together in a CLI workflow tool?
**Confidence:** HIGH (verified with existing GRD patterns + external best practices)

## Executive Summary

Command chaining in CLI workflow tools follows predictable patterns that create intuitive user experiences. The key insight: **good workflow tools don't just execute commands, they guide users through a mental model of their work**.

This research synthesizes patterns from Git, Docker, Terraform, CI/CD pipelines, and GRD's existing implementation to define best practices for command flow, branching on verdicts (like Critic), state management, and "Next Up" UX.

---

## 1. What Makes Command Flows Intuitive

### Pattern: Linear Phases with Clear State Transitions

The most successful CLI workflows (Git, Terraform, Docker) share a common structure:

```
[Preparation] --> [Execution] --> [Verification] --> [Finalization]
```

**Git:** `status` --> `add` --> `commit` --> `push`
**Terraform:** `init` --> `plan` --> `apply`
**Docker:** `build` --> `run` --> `push`
**GRD:** `new-project` --> `plan-phase` --> `execute-phase` --> `verify-work`

### Key Principles

| Principle | Description | GRD Example |
|-----------|-------------|-------------|
| **Progressive disclosure** | Each command reveals the next logical step | After `execute-phase`, suggest `verify-work` or `discuss-phase {n+1}` |
| **State visibility** | Users can always see where they are | `/grd:progress` shows position in roadmap |
| **Reversibility awareness** | Dangerous operations require confirmation | Phase skipping in `transition.md` always prompts |
| **Build once, deploy many** | Create artifacts that can be reused | PLAN.md created once, executed potentially multiple times |

### What Kills Intuition

**Anti-patterns to avoid:**

1. **Command bloat** — Too many commands for similar tasks creates confusion
2. **Hidden state** — When users can't see what state they're in
3. **Inconsistent naming** — `plan-phase` vs `execute-phase` vs `literature-review` (GRD does this well)
4. **No escape hatch** — Users trapped in flows they can't exit

### GRD Alignment Assessment

GRD's current command structure follows the linear phases pattern well:

```
new-project --> plan-phase --> execute-phase --> verify-work --> complete-milestone
         \                          |
          \--> discuss-phase -------+
           \--> literature-review -----+
```

**Strength:** Clear phase-based progression
**Gap:** Command naming still mixed between GSD terminology (phase/milestone) and research terminology (study/experiment) per v1.2 goals

---

## 2. Branching Workflows (Success -> A, Failure -> B)

### Pattern: Verdict-Based Routing

Modern CI/CD and workflow tools route based on discrete outcomes, not just pass/fail.

**Terraform model:**
```
plan --> [user reviews] --> approve --> apply
                       |
                       +--> reject --> revise configuration
```

**CI/CD pipeline model:**
```
test --> [pass] --> deploy to staging --> [pass] --> deploy to prod
     |                              |
     +--> [fail] --> notify dev     +--> [fail] --> rollback
```

**GRD Critic model (current):**
```
Researcher --> Critic --> [PROCEED] --> Evaluator
                     |
                     +--> [REVISE_METHOD] --> back to Researcher
                     |
                     +--> [REVISE_DATA] --> back to Explorer
```

### Best Practices for Verdict-Based Routing

| Practice | Rationale | GRD Implementation |
|----------|-----------|-------------------|
| **Discrete exit codes** | Machines can route on them | Critic uses PROCEED/REVISE_METHOD/REVISE_DATA |
| **Human-readable verdict** | Users understand what happened | VERIFICATION.md status: passed/gaps_found/human_needed |
| **Automatic vs manual routing** | Some routes should auto-trigger | REVISE_DATA auto-spawns Explorer; gaps_found offers command |
| **Bounded retry loops** | Prevent infinite iteration | Critic has 5 iteration limit; planner-checker has 3 iterations |
| **Escalation path** | When automation fails, humans take over | `human_needed` verdict stops for approval |

### Branching Decision Matrix

When designing verdict routes, use this framework:

| Verdict Type | Auto-Route? | User Confirmation? | Rationale |
|--------------|-------------|-------------------|-----------|
| **Success (clean)** | Yes | No | Expected path, no friction needed |
| **Success with warnings** | No | Yes | User should acknowledge |
| **Partial success** | No | Yes (with options) | User chooses: accept, fix, or abort |
| **Recoverable failure** | Yes (to fix loop) | After N retries | Let automation try first |
| **Unrecoverable failure** | No | Yes | Human decision required |
| **Destructive change** | Never | Always | Safety rail |

### GRD Implementation Examples

**execute-phase routing (from execute-phase.md):**
```
Phase complete --> [passed] + more phases --> "Route A: Phase verified, more phases remain"
              |
              +--> [passed] + last phase --> "Route B: Milestone complete"
              |
              +--> [gaps_found] --> "Route C: Need additional planning"
              |
              +--> [human_needed] --> Present checklist, get approval
```

**verify-work routing (from verify-work.md):**
```
All tests pass + more phases --> Route A (next phase)
All tests pass + last phase --> Route B (milestone complete)
Issues found + fix plans ready --> Route C (execute fixes)
Issues found + planning blocked --> Route D (manual intervention)
```

### Recommendation for v1.2 Critic Verdicts

Map research-native verdicts to command routes:

| Critic Verdict | Route To | Command Offered |
|----------------|----------|-----------------|
| `VALIDATED` | Human decision gate | `/grd:evaluate` |
| `ITERATE` | Back to experiment | `/grd:run-experiment {n}` |
| `REVISE_HYPOTHESIS` | Back to hypothesis | `/grd:design-experiment --revise` |
| `REVISE_DATA` | Back to EDA | `/grd:explore` (auto-spawned) |

---

## 3. "Next Step" Suggestions Best Practices

### Pattern: Contextual Guidance

The [Command Line Interface Guidelines](https://clig.dev/) emphasizes:

> "Suggest commands the user should run. When several commands form a workflow, suggesting to the user commands they can run next helps them learn how to use your program and discover new functionality."

Git exemplifies this: `git status` shows both state AND suggests commands:
```
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes)
```

### Best Practices

| Practice | Example | Why It Works |
|----------|---------|--------------|
| **Primary action prominent** | `/grd:run-experiment 5` in a box | Reduces decision fatigue |
| **Alternatives available** | "Also available:" section | Power users need escape hatches |
| **Context-specific** | Show different options based on state | Relevance builds trust |
| **Clear next step** | "Next Up: Phase 6" with goal | Users know what's ahead |
| **Fresh context reminder** | `<sub>/clear first</sub>` | Prevents context bloat issues |

### GRD's Current Pattern (Excellent)

From `execute-phase.md`:

```markdown
## Next Up

**Phase {Z+1}: {Name}** -- {Goal from ROADMAP.md}

/grd:scope-experiment {Z+1} -- gather context and clarify approach

<sub>/clear first --> fresh context window</sub>

---

**Also available:**
- /grd:design-experiment {Z+1} -- skip discussion, plan directly
- /grd:validate-results {Z} -- manual acceptance testing before continuing
```

**What makes this work:**
1. Primary recommendation with rationale
2. Copy-pasteable command
3. Context management hint
4. Alternatives for different user preferences

### Enhancements for v1.2

Add **state awareness** to suggestions:

```markdown
## Next Up

**Based on current state:** CONTEXT.md exists, no PLAN.md

**Recommended:** /grd:design-experiment 3

<sub>Context gathered, ready to plan</sub>
```

Show **why** this is the recommendation, not just what.

---

## 4. State Management Between Commands

### Pattern: Explicit State Files

The most robust CLI workflows maintain explicit state that survives command boundaries.

**Terraform:** `.terraform/` directory + `terraform.tfstate`
**Git:** `.git/` directory with refs, objects, index
**GRD:** `.planning/` directory with STATE.md, ROADMAP.md, config.json

### State Management Strategies

| Strategy | Use Case | GRD Usage |
|----------|----------|-----------|
| **File-based state** | Persistent, versionable | STATE.md, ROADMAP.md |
| **Environment variables** | Session-scoped, ephemeral | Not currently used |
| **Command flags** | Per-invocation override | `--gaps-only`, `--skip-verify` |
| **Config files** | User preferences | config.json |

### State File Responsibilities in GRD

| File | What It Tracks | When Updated |
|------|----------------|--------------|
| `STATE.md` | Current position, decisions, blockers, session info | After every command |
| `ROADMAP.md` | Phase structure, completion status, requirements mapping | After phase/milestone changes |
| `config.json` | Workflow preferences, model profile | On `/grd:settings` |
| `PROJECT.md` | Requirements (validated/active/out-of-scope), key decisions | After phase completion |

### Best Practices

1. **Single source of truth** — Each piece of state lives in exactly one place
2. **Human-readable state** — Users can `cat STATE.md` to understand position
3. **Automatic state updates** — Commands update state as side effect, not manual
4. **Recovery from state** — `/grd:progress` and `/grd:resume-work` reconstruct context
5. **State validation** — Commands check state consistency before executing

### State Synchronization Pattern

From `transition.md`:

```bash
# Read state before action
cat .planning/STATE.md
cat .planning/PROJECT.md
cat .planning/ROADMAP.md

# Perform action...

# Update state atomically
# 1. Update ROADMAP.md
# 2. Update PROJECT.md (evolve requirements)
# 3. Update STATE.md (position, session)
# 4. Commit all together
```

### Recommendation: State Schema Version

Add version to state files for future migrations:

```markdown
<!-- STATE.md -->
---
schema_version: 1
---

## Current Position
...
```

---

## 5. Patterns from Reference Workflows

### Git Workflow Patterns

**Lesson: Make state visible**

`git status` is the most-used Git command because it answers "where am I?" without side effects.

GRD equivalent: `/grd:progress`

**Lesson: Suggest corrections**

When Git encounters typos, it suggests similar commands:
```
git: 'statis' is not a git command. Did you mean 'status'?
```

GRD opportunity: Command fuzzy matching in Claude Code hooks.

### Terraform Workflow Patterns

**Lesson: Plan before apply**

Terraform's `plan` --> `apply` split serves two purposes:
1. User can review changes before committing
2. Automation can create plans that are later applied

GRD has this: `plan-phase` --> `execute-phase`

**Lesson: State locking**

Only one plan can be outstanding at a time to prevent conflicts.

GRD implication: STATE.md should indicate if a command is in progress.

### Docker Workflow Patterns

**Lesson: Build once, deploy many**

Docker images are immutable artifacts created once and deployed repeatedly.

GRD equivalent: PLAN.md files are artifacts that can be re-executed (with `--gaps-only`).

**Lesson: Layer caching**

Docker reuses unchanged layers for speed.

GRD opportunity: Skip research if RESEARCH.md exists (already implemented).

### CI/CD Pipeline Patterns

**Lesson: Stage gates**

Pipelines pause at gates for human approval on critical transitions.

GRD has this: `human_needed` verdict in verification.

**Lesson: Parallel where possible, sequential where necessary**

Wave-based execution in GRD follows this pattern.

**Lesson: Artifact promotion**

Artifacts (builds) promote through environments (dev --> staging --> prod).

GRD equivalent: PLAN.md promotes to SUMMARY.md after execution.

---

## 6. GRD-Specific Recommendations

### Command Flow Fix for v1.2

Current flow has terminology mismatch:
```
new-study --> plan-phase --> execute-phase
```

Should be:
```
new-study --> design-experiment --> run-experiment
```

### Branching on Critic Verdicts

Current implementation in research loop (from PROJECT.md):
```
Researcher --> Critic --> PROCEED --> Evaluator
                     |
                     +--> REVISE_METHOD --> Researcher
                     |
                     +--> REVISE_DATA --> Explorer
```

**Recommendation:** Map to command routes:

```markdown
## Critic Verdict

**REVISE_DATA** -- Data anomaly detected

The Critic found results inconsistent with the data profile.
Returning to data reconnaissance.

/grd:explore --from-critic

<sub>This spawns automatically in YOLO mode</sub>
```

### State Between Research Commands

Add research-specific state tracking to STATE.md:

```markdown
## Research Position

Study: v1.2 Command Unification
Experiment: 3 of 5 (Hypothesis Validation)
Iteration: 2 of 5
Last Critic verdict: REVISE_METHOD
```

### "Next Up" Template for Research Commands

```markdown
---

## Next Up

**{Experiment N}: {Name}** -- {Hypothesis from STUDY_PROTOCOL.md}

/grd:run-experiment {N}

<sub>Iteration {M}/{max} | Last verdict: {verdict}</sub>

---

**Also available:**
- /grd:validate-results -- check results so far
- /grd:scope-experiment {N} -- clarify approach before running

---
```

---

## 7. Summary: Command Chaining Principles for GRD

### Core Principles

1. **Linear default, branch on verdict** — Happy path is linear; verdicts create branches
2. **State survives commands** — STATE.md is the single source of truth
3. **Suggest next, show alternatives** — Primary action prominent, escape hatches available
4. **Bounded automation** — Auto-retry with limits, escalate to human when stuck
5. **Terminology consistency** — Commands match user's mental model (research, not software dev)

### Implementation Checklist for v1.2

- [ ] Rename phase commands to experiment commands
- [ ] Map Critic verdicts to command routes in `offer_next` sections
- [ ] Add research-specific state tracking to STATE.md template
- [ ] Update help.md with research-native command flow
- [ ] Ensure command chaining: `new-study` --> `design-experiment` --> `run-experiment`
- [ ] Add iteration tracking visible in "Next Up" suggestions

### Command Flow Diagram (Target State)

```
/grd:new-study
    |
    v
/grd:design-experiment 1 <-------+
    |                            |
    v                            |
/grd:run-experiment 1            |
    |                            |
    v                            |
[Critic Verdict]                 |
    |                            |
    +--[VALIDATED]---> /grd:evaluate
    |                            |
    +--[ITERATE]-------> (back to run-experiment)
    |                            |
    +--[REVISE_HYPOTHESIS]-------+
    |
    +--[REVISE_DATA]---> /grd:explore (auto)
                              |
                              v
                         (back to design-experiment)
```

---

## Sources

### Official Documentation & Guides
- [Command Line Interface Guidelines](https://clig.dev/) - Comprehensive CLI design principles
- [Terraform Core Workflow](https://developer.hashicorp.com/terraform/intro/core-workflow) - init/plan/apply pattern
- [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows) - Branch-based workflow patterns

### CLI UX Patterns
- [UX patterns for CLI tools](https://lucasfcosta.com/2022/06/01/ux-patterns-cli-tools.html) - Interactive modes, suggestions
- [10 design principles for delightful CLIs](https://www.atlassian.com/blog/it-teams/10-design-principles-for-delightful-clis) - Atlassian's design principles
- [3 steps to create an awesome UX in a CLI application](https://opensource.com/article/22/7/awesome-ux-cli-application) - Progressive discovery

### Workflow & Orchestration
- [Workflows patterns and best practices](https://cloud.google.com/blog/topics/developers-practitioners/workflows-patterns-and-best-practices-part-1) - Task chaining patterns
- [CI/CD Process: Flow, Stages, and Critical Best Practices](https://codefresh.io/learn/ci-cd-pipelines/ci-cd-process-flow-stages-and-critical-best-practices/) - Stage-based workflow
- [7 Pipeline Design Patterns for Continuous Delivery](https://www.singlestoneconsulting.com/blog/7-pipeline-design-patterns-for-continuous-delivery) - Pipeline patterns

### State Management
- [Click Context Management](https://deepwiki.com/pallets/click/2.3-context-management) - State hierarchy patterns
- [Running Terraform in automation](https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform) - State persistence between runs

### Internal GRD Sources
- `.planning/PROJECT.md` - Current GRD lifecycle definition
- `commands/grd/execute-phase.md` - Routing and offer_next patterns
- `commands/grd/verify-work.md` - Verdict-based routing
- `commands/grd/progress.md` - State inspection patterns
- `get-research-done/workflows/transition.md` - State update patterns
