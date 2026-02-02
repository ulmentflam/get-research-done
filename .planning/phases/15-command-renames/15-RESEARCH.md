# Phase 15: Command Renames - Research

**Researched:** 2026-02-01
**Domain:** CLI command renaming, file system operations, cross-reference updates
**Confidence:** HIGH

## Summary

This phase involves renaming 9 CLI commands from software-dev terminology (phase, milestone) to research-native terminology (experiment, study). The primary technical challenge is not the rename itself but ensuring all cross-references are updated atomically.

The codebase has a specific structure: commands are markdown files in `.claude/commands/grd/` (and mirrored in `commands/grd/`), with cross-references appearing in 37 files across the `.claude/` directory. Each command file has a frontmatter `name` field that must match the filename, and references to commands appear in help text, "Next Up" sections, and agent system prompts.

The user has decided on a hard break with no backward compatibility. This simplifies implementation: no alias tables, no deprecation warnings, no migration period. Old command names will simply not work.

**Primary recommendation:** Rename each command file AND its frontmatter AND all cross-references in a single atomic pass per command, using systematic grep-and-replace patterns.

## Standard Stack

No external libraries needed. This is a file system operation using standard shell tools.

### Core Tools
| Tool | Purpose | Why Standard |
|------|---------|--------------|
| `mv` | Rename command files | Native shell, reliable |
| `sed` | Update file contents | POSIX standard, in-place editing |
| `grep` | Find cross-references | Verification before/after changes |
| `git` | Atomic commits per rename | Maintains traceability |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| sed | ripgrep-replace (rg --replace) | ripgrep is read-only, no in-place edit |
| sed | node script | Heavier, but more control for complex patterns |
| per-file commits | single large commit | Per-rename commits better for rollback |

**No installation needed** - all tools already available in shell environment.

## Architecture Patterns

### Recommended Rename Sequence

```
For each of the 9 commands:
1. Rename file: mv plan-phase.md design-experiment.md
2. Update frontmatter name field in renamed file
3. Update all cross-references in all files
4. Verify no orphan references remain
5. Git commit the rename
```

### Pattern 1: Atomic Single-Command Rename

**What:** Rename one command completely before moving to the next
**When to use:** Always - prevents partial states

**Example:**
```bash
# 1. Rename file
mv .claude/commands/grd/plan-phase.md .claude/commands/grd/design-experiment.md
mv commands/grd/plan-phase.md commands/grd/design-experiment.md

# 2. Update frontmatter (in both locations)
sed -i '' 's/name: grd:design-experiment/name: grd:design-experiment/' .claude/commands/grd/design-experiment.md
sed -i '' 's/name: grd:design-experiment/name: grd:design-experiment/' commands/grd/design-experiment.md

# 3. Update all cross-references
find .claude/ -name "*.md" -exec sed -i '' 's|/grd:design-experiment|/grd:design-experiment|g' {} +
find commands/ -name "*.md" -exec sed -i '' 's|/grd:design-experiment|/grd:design-experiment|g' {} +

# 4. Verify no orphans
grep -r "plan-phase" .claude/ commands/

# 5. Commit
git add -A
git commit -m "feat(grd): rename plan-phase to design-experiment"
```

### Pattern 2: Cross-Reference Patterns to Find

The codebase uses several patterns for command references:

| Pattern | Example | Files Found In |
|---------|---------|----------------|
| `/grd:command` | `/grd:design-experiment 1` | help.md, all command files |
| `grd:command` (in frontmatter) | `name: grd:design-experiment` | command file frontmatter |
| Spawned by references | `Spawned by /grd:design-experiment` | agent files |
| Suggestion text | `Run /grd:design-experiment` | workflow files |

### Anti-Patterns to Avoid

- **Partial rename:** Renaming file but not frontmatter - breaks command lookup
- **Missing cross-references:** Leaving old names in help.md - confuses users
- **Mixed state:** Renaming some but not all before committing - untestable intermediate state
- **Hardcoded strings:** Watch for command names in error messages and examples

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Finding all references | Manual file-by-file search | `grep -r` with patterns | Easy to miss occurrences |
| In-place file editing | Python/Node script | `sed -i ''` | Native, no dependencies |
| Verifying completeness | Manual inspection | Post-rename grep verification | Catches orphans reliably |

**Key insight:** This is a text transformation problem. Use text tools, not programming tools.

## Common Pitfalls

### Pitfall 1: Forgetting Duplicate Command Directories

**What goes wrong:** Commands exist in BOTH `.claude/commands/grd/` AND `commands/grd/` - renaming only one breaks the other
**Why it happens:** Developers expect single source of truth
**How to avoid:** Always rename in both directories as atomic step
**Warning signs:** `diff` between directories shows differences

### Pitfall 2: Frontmatter Desync

**What goes wrong:** File renamed but `name:` field in frontmatter still has old name
**Why it happens:** Only thinking about filename, forgetting frontmatter
**How to avoid:** Rename file + update frontmatter in same step
**Warning signs:** Command not found after rename

### Pitfall 3: Missing Context in Agent Prompts

**What goes wrong:** Agent files like `grd-planner.md` reference old command names in their instructions
**Why it happens:** Agents aren't commands, easy to overlook
**How to avoid:** Include `.claude/agents/` in cross-reference scan
**Warning signs:** Agent spawns with wrong next-step suggestions

### Pitfall 4: Help.md Not Matching Reality

**What goes wrong:** help.md shows old command names or descriptions
**Why it happens:** help.md has both command references AND prose descriptions
**How to avoid:** Manually review help.md after automated updates
**Warning signs:** `/grd:help` output doesn't match available commands

### Pitfall 5: Workflow Files with Hardcoded Commands

**What goes wrong:** Workflow templates in `.claude/get-research-done/workflows/` have old names
**Why it happens:** These aren't commands themselves, easy to miss
**How to avoid:** Include workflows directory in cross-reference scan
**Warning signs:** Workflow outputs suggest old command names

## Code Examples

### Finding All References to a Command

```bash
# Find all occurrences of a command name (count by file)
grep -r "plan-phase" .claude/ commands/ --include="*.md" | wc -l

# Find files containing the command name
grep -rl "plan-phase" .claude/ commands/ --include="*.md"

# Show context around each occurrence
grep -rn "plan-phase" .claude/ commands/ --include="*.md" -C 1
```

### Safe In-Place Replacement (macOS)

```bash
# macOS sed requires empty string for in-place with no backup
sed -i '' 's/old-pattern/new-pattern/g' file.md

# Linux sed (no empty string needed)
sed -i 's/old-pattern/new-pattern/g' file.md
```

### Verifying Rename Completeness

```bash
# After rename, this should return 0 results
grep -r "plan-phase" .claude/ commands/ --include="*.md"

# Check new name exists in expected locations
grep -r "design-experiment" .claude/ commands/ --include="*.md" | head -20
```

### Full Rename Script Pattern

```bash
#!/bin/bash
# Pattern for one command rename

OLD="plan-phase"
NEW="design-experiment"

# Step 1: Rename files
mv ".claude/commands/grd/${OLD}.md" ".claude/commands/grd/${NEW}.md"
mv "commands/grd/${OLD}.md" "commands/grd/${NEW}.md"

# Step 2: Update frontmatter
sed -i '' "s/name: grd:${OLD}/name: grd:${NEW}/" ".claude/commands/grd/${NEW}.md"
sed -i '' "s/name: grd:${OLD}/name: grd:${NEW}/" "commands/grd/${NEW}.md"

# Step 3: Update all cross-references
find .claude/ -name "*.md" -exec sed -i '' "s|/grd:${OLD}|/grd:${NEW}|g" {} +
find commands/ -name "*.md" -exec sed -i '' "s|/grd:${OLD}|/grd:${NEW}|g" {} +

# Step 4: Verify
ORPHANS=$(grep -r "${OLD}" .claude/ commands/ --include="*.md" | wc -l)
if [ "$ORPHANS" -gt 0 ]; then
    echo "WARNING: Found $ORPHANS orphan references"
    grep -r "${OLD}" .claude/ commands/ --include="*.md"
fi

# Step 5: Commit
git add -A
git commit -m "feat(grd): rename ${OLD} to ${NEW}"
```

## Rename Mapping

The 9 commands to rename, based on requirements:

| Old Name | New Name | CONTEXT.md Guidance |
|----------|----------|---------------------|
| `plan-phase` | `design-experiment` | verb-object format |
| `execute-phase` | `run-experiment` | verb-object format |
| `discuss-phase` | `scope-experiment` | Claude's discretion (could be `define-experiment`) |
| `verify-work` | `validate-results` | verb-object format |
| `research-phase` | `literature-review` | noun phrase, research convention |
| `list-phase-assumptions` | `list-experiment-assumptions` | per CONTEXT.md, could shorten to `list-assumptions` |
| `add-phase` | `add-experiment` | verb-object format |
| `insert-phase` | `insert-experiment` | verb-object format |
| `remove-phase` | `remove-experiment` | verb-object format |

### Claude's Discretion Items

Per CONTEXT.md, I recommend:

1. **`scope-experiment` over `define-experiment`** for discuss-phase rename
   - Rationale: "scope" implies boundaries and clarification, which matches the purpose
   - "define" implies creation from scratch, but the phase already exists in roadmap

2. **Keep `list-experiment-assumptions`** (not shortened to `list-assumptions`)
   - Rationale: Consistency with other experiment-prefixed commands
   - "assumptions" alone is ambiguous without "experiment" context

## Cross-Reference Counts

Pre-research analysis found 205 occurrences across 37 files:

| Command | Approx References |
|---------|------------------|
| /grd:design-experiment | ~28 |
| /grd:run-experiment | ~25 |
| /grd:scope-experiment | ~15 |
| /grd:verify-work | ~20 |
| /grd:research-phase | ~12 |
| /grd:list-phase-assumptions | ~8 |
| /grd:add-phase | ~15 |
| /grd:insert-phase | ~12 |
| /grd:remove-phase | ~8 |

High-count files to pay attention to:
- `help.md` (28 references)
- `grd-planner.md` (11 references)
- `execute-phase.md` (9 references)
- `verify-work.md` (10 references)

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Software terminology | Research terminology | v1.2 (now) | User-facing language |
| Phase/Milestone | Experiment/Study | v1.2 (now) | All commands |

**Note:** This is an internal GRD evolution, not an industry-wide shift.

## Open Questions

1. **Mirror directory sync**
   - What we know: Commands exist in both `.claude/commands/grd/` and `commands/grd/`
   - What's unclear: Are these meant to be identical? Is there a sync mechanism?
   - Recommendation: Rename in both, verify they stay in sync

2. **Description updates in frontmatter**
   - What we know: Each command has a `description:` field
   - What's unclear: Should "phase" in descriptions become "experiment"?
   - Recommendation: Update descriptions to use experiment terminology per CONTEXT.md

3. **Internal documentation vs user-facing**
   - What we know: CONTEXT.md says "Phase" -> "Experiment" in user-facing text
   - What's unclear: Do internal comments in command files count?
   - Recommendation: Update all visible text; internal comments are lower priority

## Sources

### Primary (HIGH confidence)
- Direct codebase analysis via Read/Grep tools
- `.claude/commands/grd/*.md` - command file structure
- `.claude/agents/*.md` - agent cross-references
- `.planning/REQUIREMENTS.md` - requirement definitions
- `.planning/phases/15-command-renames/15-CONTEXT.md` - user decisions

### Secondary (MEDIUM confidence)
- Cross-reference counts from grep analysis
- Pattern matching based on observed file structure

### Tertiary (LOW confidence)
- None - all findings verified against actual codebase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - shell tools are well understood
- Architecture: HIGH - patterns derived from actual codebase structure
- Pitfalls: HIGH - identified through file structure analysis

**Research date:** 2026-02-01
**Valid until:** N/A - this is a one-time transformation, not ongoing domain knowledge
