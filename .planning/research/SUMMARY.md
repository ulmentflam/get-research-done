# GRD v1.2 Command Unification Research Summary

**Project:** Get Research Done (GRD) v1.2
**Domain:** CLI Command Structure / Workflow Orchestration
**Researched:** 2026-02-01
**Confidence:** HIGH

## Executive Summary

GRD's command structure needs alignment between its research-native terminology goal and its actual command chaining. Research reveals three core issues: (1) commands still use software-dev terminology (plan-phase, execute-phase) while the project philosophy is research-centric; (2) command chains are broken with three missing commands referenced in "Next Up" suggestions (audit-milestone, complete-milestone, new-milestone); and (3) some commands are orphaned with no inbound routes (graduate, debug).

Industry CLI tools (DVC, MLflow, wandb) favor noun-verb patterns for resource management with standard CRUD verbs. GRD's current verb-noun compound pattern (plan-phase, execute-phase) is acceptable but should be renamed to research vocabulary. The target flow should be: `new-study` -> `design-experiment` -> `run-experiment` -> `validate-results` -> `complete-study`, with Critic verdicts routing to appropriate next commands.

The highest-impact change is renaming the 6 core phase commands to experiment terminology and fixing the command chaining so `new-study` routes to `design-experiment`, not `plan-phase`. Secondary changes include removing or implementing the missing milestone commands and adding explicit routes to orphaned commands.

---

## Key Findings

### CLI Naming Conventions (from CLI_NAMING.md)

ML/research CLI tools overwhelmingly follow **noun-verb** patterns at the subcommand level. Standard CRUD verbs dominate (`create`, `delete`, `list`, `show`), with domain-specific verbs for lifecycle operations (`run`, `restore`, `apply`).

**Recommended verbs by category:**

| Category | Verbs | Usage |
|----------|-------|-------|
| Lifecycle | `new`, `plan`, `execute`, `verify`, `complete`, `graduate` | Studies/experiments |
| CRUD | `add`, `remove`, `insert`, `list`, `show` | Phases/todos |
| State | `pause`, `resume`, `reset` | Session management |
| Analysis | `check`, `audit`, `explore`, `research` | Investigation |

**Key insight:** GRD's current pattern works; only the nouns need changing (phase -> experiment, milestone -> study).

### Research Workflow Mental Models (from RESEARCH_WORKFLOW.md)

Researchers think in terms of **studies** (comprehensive investigations) and **experiments** (individual hypothesis tests). The standard research lifecycle is:

```
Problem Formulation -> Hypothesis Generation -> Study Design ->
Data Collection -> Analysis -> Iteration -> Dissemination
```

**Terminology mapping:**

| GRD Current | Research-Native | Alignment |
|-------------|-----------------|-----------|
| Project | Project | Good |
| Milestone | Study | Needs rename |
| Phase | Experiment | Needs rename |
| Plan | Protocol/Design | Needs rename |
| Verify | Validate/Evaluate | Needs rename |

**Key insight:** "Phase" and "Plan" feel engineering-coded. "Experiment" and "Design" better match researcher mental models.

### Current Command Structure (from CURRENT_COMMANDS.md)

GRD has **33 commands** across 7 categories. Analysis found:

**Broken chains (3 missing commands):**
| Referenced Command | Referenced By | Issue |
|-------------------|---------------|-------|
| `/grd:audit-milestone` | execute-phase, verify-work, progress | Does not exist |
| `/grd:complete-milestone` | progress, verify-work | Does not exist |
| `/grd:new-milestone` | progress | Does not exist |

**Orphaned commands (2):**
| Command | Issue |
|---------|-------|
| `graduate` | No inbound routes from other commands |
| `debug` | Standalone entry point (acceptable) |

**Naming inconsistencies:**
- `--gaps` vs `--gaps-only` used interchangeably
- "Study" vs "Milestone" terminology confused in workflows

### Command Chaining Patterns (from COMMAND_CHAINING.md)

Best practice: **linear default, branch on verdict**. The most successful CLI workflows follow:

```
[Preparation] --> [Execution] --> [Verification] --> [Finalization]
```

**Verdict-based routing matrix:**

| Verdict Type | Auto-Route? | User Confirmation? |
|--------------|-------------|-------------------|
| Success (clean) | Yes | No |
| Success with warnings | No | Yes |
| Partial success | No | Yes (with options) |
| Recoverable failure | Yes (to fix loop) | After N retries |
| Unrecoverable failure | No | Yes |

**Key insight:** GRD's Critic verdicts (PROCEED, REVISE_METHOD, REVISE_DATA) should map directly to command routes.

---

## Recommended Command Renames

| Current | Proposed | Rationale |
|---------|----------|-----------|
| `plan-phase` | `design-experiment` | Matches research terminology; "design" is what researchers call experiment planning |
| `execute-phase` | `run-experiment` | "Run" is standard for experiment execution (DVC, MLflow) |
| `discuss-phase` | `scope-experiment` | "Scope" captures context gathering before design |
| `verify-work` | `validate-results` | "Validate" is more statistical/research-native |
| `literature-review` | `literature-review` | Explicit about what the research step does |
| `list-experiment-assumptions` | `list-experiment-assumptions` | Keep pattern, change noun |
| `add-phase` | `add-experiment` | Keep pattern, change noun |
| `insert-phase` | `insert-experiment` | Keep pattern, change noun |
| `remove-phase` | `remove-experiment` | Keep pattern, change noun |
| `audit-milestone` | `audit-study` | Already exists; remove milestone references |
| `complete-milestone` | `complete-study` | Already exists; remove milestone references |
| `new-milestone` | (remove) | Milestone concept deprecated; studies are the unit |

**No changes needed:**
- `new-study`, `audit-study`, `complete-study`, `plan-study-gaps` (already research-native)
- `explore`, `quick-explore`, `insights`, `architect`, `research`, `evaluate`, `graduate` (ML workflow)
- `progress`, `pause-work`, `resume-work`, `help`, `settings`, `set-profile`, `update` (utility)
- `add-todo`, `check-todos`, `debug`, `quick`, `map-codebase` (peripheral, not in main flow)

---

## Flow Fixes

### Primary Development Workflow

**Current (broken):**
```
new-study --> plan-phase --> execute-phase --> verify-work --> complete-milestone (MISSING)
```

**Fixed:**
```
new-study --> design-experiment --> run-experiment --> validate-results --> complete-study
```

### Command Chaining Updates

| Trigger | Current Next Up | Fixed Next Up |
|---------|-----------------|---------------|
| `new-study` complete | `/grd:design-experiment {N}` | `/grd:design-experiment 1` |
| `design-experiment` complete | (new) | `/grd:run-experiment {N}` |
| `run-experiment` complete | `/grd:scope-experiment {Z+1}` | `/grd:validate-results {N}` OR `scope-experiment {N+1}` |
| `validate-results` passed | `/grd:complete-milestone` | `/grd:complete-study` OR `design-experiment {N+1}` |
| `evaluate` with Seal | (none) | `/grd:graduate` (add explicit route) |

### Critic Verdict Routing

| Critic Verdict | Route To | Command Offered |
|----------------|----------|-----------------|
| `PROCEED` | Human decision gate | `/grd:evaluate` |
| `REVISE_METHOD` | Back to experiment | `/grd:run-experiment {N}` (continue mode) |
| `REVISE_DATA` | Back to EDA | `/grd:explore` (auto-spawned) |

---

## Commands to Remove/Consolidate

### Remove (references only, not actual commands)

| Reference | Found In | Action |
|-----------|----------|--------|
| `/grd:audit-milestone` | execute-phase, verify-work, progress | Replace with `/grd:audit-study` |
| `/grd:complete-milestone` | progress, verify-work | Replace with `/grd:complete-study` |
| `/grd:new-milestone` | progress | Replace with `/grd:new-study` |

### Consolidate

| Candidate | Consolidate Into | Rationale |
|-----------|------------------|-----------|
| `literature-review` | `literature-review` | Same function, research-native name |
| `discuss-phase` | `scope-experiment` | Same function, research-native name |

### Flag Standardization

| Current Usage | Standardize To | Files to Update |
|---------------|----------------|-----------------|
| `--gaps` / `--gaps-only` | `--gaps` | verify-work, execute-phase |

---

## Implications for Roadmap

Based on research, suggested phase structure for v1.2:

### Phase 1: Command Rename Infrastructure

**Rationale:** Foundation work enables all other phases; breaking change requires careful migration
**Delivers:** Renamed commands with aliases for backward compatibility (optional)
**Scope:**
- Rename 9 phase-related commands to experiment terminology
- Update all command file names and content
- Update help.md command reference

**Avoids pitfall:** User confusion from sudden breaking changes (consider aliases)

### Phase 2: Fix Command Chaining

**Rationale:** Depends on Phase 1 renames being complete; broken chains undermine UX
**Delivers:** Correct "Next Up" suggestions throughout the workflow
**Scope:**
- Update all `offer_next` sections in command files
- Remove milestone references, replace with study references
- Add explicit route to `graduate` from `evaluate`
- Fix flag inconsistency (`--gaps` everywhere)

**Avoids pitfall:** Infinite loops or dead ends in command flow

### Phase 3: State and Artifact Updates

**Rationale:** Artifacts should match new terminology; STATE.md should track experiments not phases
**Delivers:** Consistent research terminology in all artifacts
**Scope:**
- Update STATE.md template (experiment tracking, not phase tracking)
- Update ROADMAP.md references to use study/experiment terminology (or deprecate)
- Add research-specific state tracking (iteration count, last Critic verdict)

**Avoids pitfall:** Terminology mismatch between commands and artifacts

### Phase 4: Documentation and Testing

**Rationale:** Must validate changes work correctly before shipping
**Delivers:** Validated command flows, updated documentation
**Scope:**
- Update PROJECT.md with new command names
- Update any inline documentation
- Manual testing of primary workflow paths
- Update README/installation docs if they reference old commands

**Avoids pitfall:** Shipping untested changes that break user workflows

### Phase Ordering Rationale

1. **Rename first:** All other changes depend on knowing the final command names
2. **Fix chains second:** Chains reference command names, so must follow renames
3. **State/artifacts third:** Templates and state use command names in suggestions
4. **Test last:** Validation can only happen after all changes are in place

### Research Flags

**Phases needing deeper research during planning:**
- **Phase 3:** May need research on STATE.md schema versioning for future migrations

**Phases with standard patterns (skip literature-review):**
- **Phase 1:** Straightforward file renames and content updates
- **Phase 2:** Pattern established in COMMAND_CHAINING.md research
- **Phase 4:** Standard documentation updates

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| CLI Naming | HIGH | Verified against DVC, MLflow, wandb, Sacred, Hydra official docs |
| Research Workflow | HIGH | Multiple academic sources (Harvard, NNLM, CRISP-DM) |
| Current Commands | HIGH | Direct analysis of existing codebase |
| Command Chaining | HIGH | Patterns verified against Git, Terraform, Docker, CI/CD |

**Overall confidence:** HIGH

### Gaps to Address

1. **Backward compatibility:** Research did not determine whether command aliases should be provided. Decision needed: hard cutover vs. deprecation period with aliases.

2. **ROADMAP.md fate:** Currently uses "phase" terminology heavily. Decision needed: (a) rename to STUDY_PROTOCOL.md and update structure, (b) keep ROADMAP.md but update terminology, or (c) deprecate for research workflows.

3. **Artifact file naming:** Commands will be renamed but artifacts (e.g., `{phase}-CONTEXT.md`) may need renaming too. Decision needed during Phase 3 planning.

---

## Sources

### Primary (HIGH confidence)
- [DVC Command Reference](https://dvc.org/doc/command-reference) - experiment lifecycle patterns
- [MLflow CLI Reference](https://mlflow.org/docs/latest/cli.html) - noun-verb structure
- [Command Line Interface Guidelines](https://clig.dev/) - general CLI best practices
- [Harvard Research Lifecycle](https://researchsupport.harvard.edu/research-lifecycle) - academic terminology
- [CRISP-DM for Data Science](https://www.datascience-pm.com/) - ML workflow phases

### Secondary (MEDIUM confidence)
- [W&B CLI Reference](https://docs.wandb.ai/ref/cli/) - state toggles, sync patterns
- [Sacred CLI Reference](https://sacred.readthedocs.io/en/stable/command_line.html) - configuration patterns
- [Terraform Core Workflow](https://developer.hashicorp.com/terraform/intro/core-workflow) - plan/apply pattern

### Internal (HIGH confidence)
- GRD command files (33 commands analyzed)
- PROJECT.md current state and requirements
- Existing workflow orchestration patterns

---

*Research completed: 2026-02-01*
*Ready for roadmap: yes*
