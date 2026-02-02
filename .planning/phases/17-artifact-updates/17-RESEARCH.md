# Phase 17: Artifact Updates - Research

**Researched:** 2026-02-01
**Domain:** Technical documentation and template maintenance
**Confidence:** HIGH

## Summary

This phase updates artifact templates and command documentation to use consistent research-native terminology (experiments, studies, protocols) replacing software development terminology (phases, milestones, roadmaps). The work involves template file updates, comprehensive find-and-replace operations, and routing updates across 33 command files.

The domain is technical documentation maintenance rather than software implementation. Key challenges include maintaining internal consistency, avoiding breaking existing projects mid-flight, and ensuring command routing forms a complete graph where every command suggests appropriate next steps.

Standard approach: batch template updates first (minimize merge conflicts), then systematic terminology replacement (automated where possible), followed by manual routing updates (requires semantic understanding of workflow states).

**Primary recommendation:** Use structured find-and-replace with verification checkpoints. Templates updated atomically, terminology replaced with grep-verified patterns, routing updated command-by-command with cross-referencing.

## Standard Stack

### Core

No external libraries needed - this is pure documentation work.

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| sed | system | Batch text replacement | POSIX standard, reliable for template updates |
| grep | system | Pattern verification | Validate replacements completed |
| git | system | Version control | Track changes, enable rollback |

### Supporting

| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| diff | system | Compare before/after | Verify template changes |
| markdown linter | markdownlint | Validate syntax | Ensure documentation quality |

### Alternatives Considered

None - this is fundamental text file manipulation.

**Installation:**
```bash
# No installation needed - using system tools
```

## Architecture Patterns

### Recommended Update Structure

```
Phase 17 Workflow:
1. Template Updates (atomic)
   ├── STATE.md template (experiment tracking)
   ├── ROADMAP.md template (study/experiment terminology)
   └── Verify with diff

2. Help Documentation (comprehensive)
   ├── Command categorization (Lifecycle/Research/Data/Utility)
   ├── Full reference (name + desc + args + examples + flags)
   └── Quick-start workflow section

3. Routing Updates (semantic)
   ├── Identify 10 commands with "Next Up" sections
   ├── Update each with correct command names
   ├── Add context-aware routing (last experiment vs. more remaining)
   └── Cross-verify all routes form complete graph

4. Verification
   ├── Grep for old terminology
   ├── Verify STATE.md tracks experiments
   ├── Check help.md completeness
   └── Validate all routing destinations exist
```

### Pattern 1: Template Terminology Updates

**What:** Systematic replacement of terminology in template files

**When to use:** When templates define structure used by generator commands

**Example:**
```bash
# Source: Standard sed practice for template updates

# In state.md template - update section headers
sed -i 's/## Milestone History/## Research History/g' templates/state.md
sed -i 's/Phase: \[X\] of \[Y\]/Experiment: \[X\] of \[Y\]/g' templates/state.md

# In roadmap.md template - update throughout
sed -i 's/phase/experiment/g' templates/roadmap.md
sed -i 's/Phase/Experiment/g' templates/roadmap.md
sed -i 's/milestone/study/g' templates/roadmap.md
sed -i 's/Milestone/Study/g' templates/roadmap.md

# Verify changes
grep -n "phase\|milestone" templates/state.md  # Should find none
```

**Key insight:** Template changes affect NEW projects only. Existing project files (like .planning/ROADMAP.md) are intentionally NOT updated per STATE.md decision.

### Pattern 2: Command Routing Graph

**What:** Each command's "Next Up" section suggests appropriate next commands based on workflow state

**When to use:** When commands need to guide users through multi-step workflows

**Example structure:**
```markdown
## ▶ Next Up

**Experiment {N}: {Name}** — {Goal}

/grd:design-experiment {N}

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────

**Also available:**
- /grd:scope-experiment {N} — gather context first
- /grd:list-experiment-assumptions {N} — see planned approach
```

**Routing decision tree:**
- After validation, last experiment → `/grd:complete-study`
- After validation, more experiments → `/grd:design-experiment {N+1}`
- After planning → `/grd:run-experiment {N}`
- After execution → `/grd:validate-results {N}`
- After study completion → `/grd:new-study`

### Pattern 3: Help Documentation Structure

**What:** Categorized command reference with quick-start workflow

**When to use:** Users need to discover commands and understand workflow

**Example structure:**
```markdown
# GRD Command Reference

## Quick Start

1. /grd:new-study - Initialize with protocol
2. /grd:design-experiment 1 - Create plan
3. /grd:run-experiment 1 - Execute

## Core Workflow

new-study → design-experiment → run-experiment → validate-results → repeat

## Commands by Category

### Lifecycle Commands
- /grd:new-study - Start research study
- /grd:design-experiment - Plan experiment
- /grd:run-experiment - Execute plans
- /grd:validate-results - Test results
- /grd:complete-study - Archive study

### Research Commands
- /grd:scope-experiment - Capture vision
- /grd:literature-review - Research domain
- /grd:list-experiment-assumptions - See approach

[... etc ...]
```

### Anti-Patterns to Avoid

- **Incomplete routing graphs:** Command suggests next step that doesn't exist or uses wrong terminology
- **Mixed terminology:** Templates using both "phase" and "experiment" inconsistently
- **Breaking existing projects:** Updating .planning files in active projects (only update templates)
- **Undocumented commands:** help.md missing commands that exist

## Don't Hand-Roll

Problems that look simple but need systematic approaches:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Find all terminology to replace | Manual search | grep with pattern file | 33 files × multiple terms = error-prone |
| Verify routing completeness | Manual review | Routing graph verification script | Easy to miss circular or dead-end routes |
| Template consistency | Update each separately | Batch sed with verification | Ensures no templates missed |

**Key insight:** Documentation updates are tedious and error-prone. Automation catches what manual review misses.

## Common Pitfalls

### Pitfall 1: Template vs. Instance Confusion

**What goes wrong:** Updating both templates AND existing project files, breaking active work

**Why it happens:** Templates (.md files in get-research-done/templates/) look similar to project files (.planning/*.md)

**How to avoid:**
- Templates are in `get-research-done/templates/` - THESE get updated
- Project files are in `.planning/` - THESE do NOT get updated (per STATE.md decision)
- Commands are in `commands/grd/` - "Next Up" sections get updated

**Warning signs:** Git diff shows changes to `.planning/STATE.md` or `.planning/ROADMAP.md` in this repo

### Pitfall 2: Inconsistent "Experiment" References

**What goes wrong:** Some places use "experiment", some use "phase", causing user confusion

**Why it happens:** Find-and-replace misses context-specific uses (e.g., "argument-hint" fields, inline references)

**How to avoid:**
- Use grep to find ALL occurrences: `grep -r "phase" commands/grd/*.md`
- Check contextual appropriateness: some uses like "argument-hint" need semantic updates
- Verify help.md references match actual command names

**Warning signs:** help.md describes "phase number" but command is now "experiment number"

### Pitfall 3: Routing Dead Ends

**What goes wrong:** Command suggests next step that's impossible to reach or uses old command name

**Why it happens:** Routing is semantic (depends on workflow state), not mechanical

**How to avoid:**
- Map all 10 commands with "Next Up" sections
- Verify each suggested command exists
- Check conditional routing (e.g., "if last experiment" vs. "if more remain")
- Test workflow graph completeness: every end state has a next step

**Warning signs:** User reaches completion but no suggestion for what's next, or suggestion uses old command name like `/grd:plan-phase`

### Pitfall 4: STATE.md Tracking Mismatch

**What goes wrong:** STATE.md template still references "phases" when workflow now uses "experiments"

**Why it happens:** STATE.md is complex with multiple sections needing coordinated updates

**How to avoid:**
- Update all section headers atomically
- Check field names: "Phase: X of Y" → "Experiment: X of Y"
- Verify progress calculation still makes sense
- Update comments/documentation in template

**Warning signs:** New projects initialized with "Phase 1 of 5" instead of "Experiment 1 of 5"

## Code Examples

Verified patterns from codebase analysis:

### Current "Next Up" Pattern (validate-results.md)

```markdown
## ▶ Next Up

**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

/grd:scope-experiment {Z+1} — gather context and clarify approach

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────

**Also available:**
- /grd:design-experiment {Z+1} — skip discussion, plan directly
- /grd:run-experiment {Z+1} — skip to execution (if already planned)
```

**Update needed:** Replace "Phase" with "Experiment" in all instances

### Current STATE.md Template Section

```markdown
## Current Position

Phase: [X] of [Y] ([Phase name])
Plan: [A] of [B] in current phase
Status: [Ready to plan / Planning / Ready to execute / In progress / Phase complete]
Last activity: [YYYY-MM-DD] — [What happened]

Progress: [░░░░░░░░░░] 0%
```

**Update needed:**
```markdown
## Current Position

Experiment: [X] of [Y] ([Experiment name])
Plan: [A] of [B] in current experiment
Status: [Ready to plan / Planning / Ready to execute / In progress / Experiment complete]
Last activity: [YYYY-MM-DD] — [What happened]

Progress: [░░░░░░░░░░] 0%
```

### Current ROADMAP.md Template Structure

```markdown
## Phase Details

### Phase 1: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Nothing (first phase)
**Requirements**: [REQ-01, REQ-02, REQ-03]
**Success Criteria** (what must be TRUE):
  1. [Observable behavior]
```

**Update needed:**
```markdown
## Experiment Details

### Experiment 1: [Name]
**Goal**: [What this experiment delivers]
**Depends on**: Nothing (first experiment)
**Requirements**: [REQ-01, REQ-02, REQ-03]
**Success Criteria** (what must be TRUE):
  1. [Observable behavior]
```

### Command Categorization Pattern (help.md)

Based on the 33 commands, logical grouping:

**Lifecycle (9 commands):**
- new-project, new-study, design-experiment, run-experiment, validate-results, complete-study, audit-study, plan-study-gaps, progress

**Research (5 commands):**
- scope-experiment, literature-review, list-experiment-assumptions, research, architect

**Data (3 commands):**
- explore, evaluate, insights

**Roadmap Management (3 commands):**
- add-experiment, insert-experiment, remove-experiment

**Session Management (2 commands):**
- pause-work, resume-work

**Quick Mode (2 commands):**
- quick, quick-explore

**Todo Management (2 commands):**
- add-todo, check-todos

**Utility (7 commands):**
- help, update, settings, set-profile, debug, map-codebase, graduate

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Software dev terminology (phases, milestones) | Research-native terminology (experiments, studies) | Phase 15-16 (completed) | Phase 17 updates artifacts to reflect new terminology |
| Scattered routing hints | Structured "Next Up" sections | v1.0 | Phase 17 updates to use correct command names |
| Ad-hoc help text | Categorized command reference | v1.1 | Phase 17 expands with complete reference |

**Deprecated/outdated:**
- "phase" terminology: replaced with "experiment"
- "milestone" terminology: replaced with "study"
- GSD command prefix: removed entirely in v1.1

## Open Questions

Things needing clarification during planning:

1. **ROADMAP.md vs PROTOCOL.md naming**
   - What we know: CONTEXT.md says "rename to PROTOCOL.md", STATE.md says "keep ROADMAP.md"
   - What's unclear: Final decision on filename
   - Recommendation: Follow STATE.md (authoritative) - keep ROADMAP.md, update terminology only

2. **Existing project migration**
   - What we know: STATE.md says "Preserve CHANGELOG.md: Historical references intentionally not updated"
   - What's unclear: What about .planning/ROADMAP.md in THIS project?
   - Recommendation: Update template only, leave existing .planning/ files unchanged

3. **Directory structure migration**
   - What we know: CONTEXT.md mentions "Experiment folders use .planning/experiments/XX-name structure (rename from phases/)"
   - What's unclear: Is this in scope for Phase 17 or future phase?
   - Recommendation: Clarify with user - likely future phase (Phase 18 or 19)

## Sources

### Primary (HIGH confidence)
- Codebase analysis: 33 command files examined directly
- Template files: state.md, roadmap.md, help.md templates read
- Current ROADMAP.md: Phase 17 requirements and dependencies verified
- STATE.md: Authoritative decisions documented (keep ROADMAP.md, no backward compat)
- CONTEXT.md: User decisions from discuss-phase (conflicts resolved by STATE.md)

### Secondary (MEDIUM confidence)
- [Command Line Interface Guidelines](https://clig.dev/) - CLI help best practices
- [CLI Help pages | BetterCLI.org](https://bettercli.org/design/cli-help-page/) - Help page design patterns
- [Markdown Documentation Guide: Best Practices](https://developers-toolkit.com/blog/markdown-documentation-guide) - Documentation structure

### Tertiary (LOW confidence)
- None - all findings verified against codebase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Simple text manipulation, system tools
- Architecture: HIGH - Patterns observed in current codebase
- Pitfalls: HIGH - Based on direct codebase analysis and common documentation errors

**Research date:** 2026-02-01
**Valid until:** 60 days (stable domain - documentation patterns don't change rapidly)
