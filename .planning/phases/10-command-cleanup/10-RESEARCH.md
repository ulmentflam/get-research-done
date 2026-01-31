# Phase 10: Command Cleanup & Foundation - Research

**Researched:** 2026-01-30
**Domain:** File system cleanup, command deprecation, CLI documentation maintenance
**Confidence:** HIGH

## Summary

Phase 10 involves cleaning up duplicate command files and removing deprecated commands from a Node.js-based CLI tool. This is straightforward file system work with three main components: (1) deleting 32 duplicate " 2.md" files that are exact copies created by macOS file system, (2) removing two GSD-specific commands that don't apply to the research workflow, and (3) updating help documentation to reflect the changes.

The standard approach is: verify duplicates are identical, use explicit file deletion patterns with verification, update documentation atomically with file changes, and commit in a single atomic operation to maintain consistency.

**Primary recommendation:** Use bash `rm` with explicit file lists (not wildcards) to prevent accidental deletion, verify file counts before and after, and commit all changes (deletions + documentation update) together to maintain system consistency.

## Standard Stack

This is a file cleanup operation, not a development task requiring libraries. The only tools needed are standard POSIX utilities.

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| bash | 5.x+ | Script execution and file operations | Universal shell, safe patterns for deletion |
| git | 2.x+ | Version control for tracking deletions | Preserves history, enables rollback |
| ls/wc | POSIX | File verification and counting | Simple, reliable verification |

### Supporting
| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| find | GNU/BSD | Safe file discovery | When wildcards needed, testing patterns |
| diff | GNU/BSD | Verify files are identical | Confirm duplicates before deletion |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| rm (direct) | mv to trash | Safer but adds complexity, unnecessary for git-tracked files |
| Shell script | Node.js fs module | More portable but overkill for simple deletion |
| Manual deletion | Automated script | Manual safer for one-time, automation better documented |

**Installation:**
No installation needed - standard POSIX utilities available on all systems.

## Architecture Patterns

### Recommended Cleanup Structure
```
Phase 10 Execution:
├── 1. Verify current state (count files, check git status)
├── 2. Delete duplicate files (explicit list, verify each)
├── 3. Remove deprecated commands (explicit list)
├── 4. Update help.md documentation
├── 5. Verify final state (count files again)
└── 6. Commit atomically (all changes together)
```

### Pattern 1: Safe File Deletion
**What:** Delete files with explicit verification before and after
**When to use:** Any destructive file operation in production systems
**Example:**
```bash
# Source: Command Line Interface Guidelines (https://clig.dev/)
# Best practice from linux rm experts (2026)

# 1. Verify files exist and are duplicates
DUPLICATE_FILES=(
  ".claude/commands/grd/add-phase 2.md"
  ".claude/commands/grd/add-todo 2.md"
  # ... explicit list
)

# 2. Verify count matches expectation
EXPECTED_COUNT=32
ACTUAL_COUNT=${#DUPLICATE_FILES[@]}
if [ "$ACTUAL_COUNT" -ne "$EXPECTED_COUNT" ]; then
  echo "ERROR: Expected $EXPECTED_COUNT files, found $ACTUAL_COUNT"
  exit 1
fi

# 3. Optional: Verify duplicates are identical
for file in "${DUPLICATE_FILES[@]}"; do
  original="${file% 2.md}.md"
  if ! diff -q "$original" "$file" > /dev/null; then
    echo "WARNING: $file differs from original"
  fi
done

# 4. Delete with explicit list (not wildcards)
for file in "${DUPLICATE_FILES[@]}"; do
  if [ -f "$file" ]; then
    rm "$file"
    echo "Deleted: $file"
  else
    echo "WARNING: File not found: $file"
  fi
done

# 5. Verify final state
REMAINING=$(ls -1 .claude/commands/grd/*.md | wc -l)
echo "Remaining files: $REMAINING (expected: 30)"
```

### Pattern 2: Atomic Documentation Update
**What:** Update documentation in same commit as code/file changes
**When to use:** Any time user-facing interfaces change
**Example:**
```bash
# Source: CLI Guidelines (https://clig.dev/)
# Deprecation best practices from Microsoft WMIC removal (2026)

# 1. Remove commands first
rm .claude/commands/grd/audit-milestone.md
rm .claude/commands/grd/plan-milestone-gaps.md

# 2. Update help.md to remove references
# (Edit help.md to remove command documentation sections)

# 3. Stage and commit together (atomic change)
git add .claude/commands/grd/
git add .claude/commands/grd/help.md
git commit -m "feat(commands): remove GSD-specific commands

Remove audit-milestone and plan-milestone-gaps commands.
These are GSD-specific and not relevant to research workflow.

Updated help.md documentation to reflect removal.

Files removed: 2
Help sections removed: 2"
```

### Pattern 3: Pre-Change Verification
**What:** Validate assumptions about file state before making changes
**When to use:** Any destructive operation with specific expectations
**Example:**
```bash
# Source: Linux Expert Better 2026 (safe deletion practices)

# Verify current state matches expectations
CURRENT_COUNT=$(ls -1 .claude/commands/grd/*.md | wc -l)
EXPECTED_BEFORE=64

if [ "$CURRENT_COUNT" -ne "$EXPECTED_BEFORE" ]; then
  echo "ERROR: Expected $EXPECTED_BEFORE files, found $CURRENT_COUNT"
  echo "Current state does not match assumptions. Manual review needed."
  exit 1
fi

# Verify duplicates exist
DUPLICATE_COUNT=$(ls -1 .claude/commands/grd/*" 2.md" | wc -l)
if [ "$DUPLICATE_COUNT" -ne 32 ]; then
  echo "ERROR: Expected 32 duplicate files, found $DUPLICATE_COUNT"
  exit 1
fi

# Verify deprecated commands exist
if [ ! -f ".claude/commands/grd/audit-milestone.md" ]; then
  echo "WARNING: audit-milestone.md not found (may already be deleted)"
fi

echo "✓ Pre-change verification passed"
```

### Anti-Patterns to Avoid
- **Wildcard deletion without verification:** `rm *" 2.md"` can accidentally match unintended files
- **Separate documentation commits:** Creates inconsistent state where code and docs diverge
- **Assuming file counts:** Always verify actual state before making assumptions
- **No rollback plan:** Git provides automatic rollback; always commit to preserve history

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| File deduplication | Custom hash comparison tool | `diff -q` or `cmp` | POSIX standard, handles edge cases |
| Safe file deletion | Custom trash/backup system | `rm` + git (for tracked files) | Git history is the backup |
| Bulk file operations | Custom Node.js script | Bash with explicit lists | Simpler, more transparent, easier to verify |
| Documentation updates | Manual editing | Scripted sed/awk or manual with verification | Human review ensures accuracy |

**Key insight:** For one-time cleanup operations, simple bash scripts with explicit file lists are more transparent and verifiable than complex automation. Git history provides the safety net.

## Common Pitfalls

### Pitfall 1: Unquoted File Paths with Spaces
**What goes wrong:** Files with spaces in names (like "add-phase 2.md") break unquoted bash commands
**Why it happens:** Bash word splitting treats spaces as delimiters
**How to avoid:** Always quote file paths in bash: `rm "$file"` not `rm $file`
**Warning signs:** Commands work in tests but fail on production files with spaces

### Pitfall 2: Wildcard Matching Unintended Files
**What goes wrong:** Patterns like `*" 2.md"` might match files you don't intend
**Why it happens:** Wildcards expand based on actual filesystem contents, not expectations
**How to avoid:** Use explicit file lists or test patterns with `ls` first, verify count matches expectations
**Warning signs:** File count after deletion doesn't match expected reduction

### Pitfall 3: Documentation Out of Sync
**What goes wrong:** Help documentation still lists removed commands, confusing users
**Why it happens:** Updating code/files separately from documentation
**How to avoid:** Always update documentation in the same commit as command removal
**Warning signs:** Users report commands that "should exist" per docs but don't

### Pitfall 4: No Verification Before Deletion
**What goes wrong:** Delete wrong files or wrong number of files
**Why it happens:** Assuming file state without checking actual filesystem
**How to avoid:** Always verify file counts and existence before deletion, check results after
**Warning signs:** Surprised by number of files deleted, unexpected errors

### Pitfall 5: Forgetting to Update Installer
**What goes wrong:** Cleanup removes files locally but installer still copies duplicates on fresh install
**Why it happens:** Multiple sources of truth (local `.claude/` vs source `commands/` directory)
**How to avoid:** Clean both installed location AND source directory
**Warning signs:** Clean install recreates the duplicate files

## Code Examples

Verified patterns from research:

### Complete Safe Cleanup Script
```bash
# Source: Synthesized from CLI Guidelines and Linux safe deletion practices

#!/bin/bash
set -euo pipefail  # Exit on error, undefined variables

PHASE_DIR=".claude/commands/grd"

echo "=== Phase 10: Command Cleanup ==="
echo ""

# Step 1: Verify current state
echo "1. Verifying current state..."
CURRENT_COUNT=$(ls -1 "$PHASE_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "   Current files: $CURRENT_COUNT (expected: 64)"

if [ "$CURRENT_COUNT" -ne 64 ]; then
  echo "   WARNING: Expected 64 files, found $CURRENT_COUNT"
  echo "   Review filesystem state before proceeding."
  exit 1
fi

# Step 2: Delete duplicate " 2.md" files
echo ""
echo "2. Deleting duplicate ' 2.md' files..."
DELETED=0
while IFS= read -r file; do
  if [ -f "$file" ]; then
    rm "$file"
    DELETED=$((DELETED + 1))
    echo "   Deleted: $(basename "$file")"
  fi
done < <(find "$PHASE_DIR" -name "*2.md" -type f)

echo "   Deleted $DELETED files (expected: 32)"

# Step 3: Remove deprecated commands
echo ""
echo "3. Removing deprecated commands..."
DEPRECATED=(
  "$PHASE_DIR/audit-milestone.md"
  "$PHASE_DIR/plan-milestone-gaps.md"
)

for cmd in "${DEPRECATED[@]}"; do
  if [ -f "$cmd" ]; then
    rm "$cmd"
    echo "   Removed: $(basename "$cmd")"
  else
    echo "   WARNING: Not found: $(basename "$cmd")"
  fi
done

# Step 4: Verify final state
echo ""
echo "4. Verifying final state..."
FINAL_COUNT=$(ls -1 "$PHASE_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "   Final count: $FINAL_COUNT (expected: 30)"

if [ "$FINAL_COUNT" -ne 30 ]; then
  echo "   ERROR: Expected 30 files, found $FINAL_COUNT"
  echo "   Manual review required."
  exit 1
fi

echo ""
echo "✓ Cleanup complete: 64 → 30 files"
echo ""
echo "Next: Update help.md documentation and commit changes"
```

### Verification Command
```bash
# Verify cleanup was successful
ls -1 .claude/commands/grd/*.md | wc -l
# Expected output: 30

# Verify no duplicate files remain
ls -1 .claude/commands/grd/*" 2.md" 2>/dev/null | wc -l
# Expected output: 0 (or "No such file or directory")

# Verify deprecated commands removed
ls .claude/commands/grd/audit-milestone.md 2>/dev/null
ls .claude/commands/grd/plan-milestone-gaps.md 2>/dev/null
# Expected output: "No such file or directory" for both
```

### Help Documentation Update Pattern
```markdown
<!-- Source: CLI documentation best practices from Zapier Engineering -->

Remove these sections from help.md:

1. Under "### Milestone Auditing" section:
   - Remove **`/grd:audit-milestone [version]`** subsection
   - Remove **`/grd:plan-milestone-gaps`** subsection

2. Remove any cross-references in workflow examples:
   - Remove audit/gap closure examples from "## Common Workflows"

Verification:
- Search help.md for "audit-milestone" → should find 0 matches
- Search help.md for "plan-milestone-gaps" → should find 0 matches
- Command count in documentation should reflect 30 commands (not 34)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual file cleanup | Git-tracked atomic cleanup | Ongoing (2026) | Documentation stays in sync with code |
| Wildcard-based deletion | Explicit file lists | 2020s | Safer, more verifiable operations |
| Separate doc updates | Atomic commits | 2015+ (Git best practices) | Consistency guaranteed |
| Command deprecation warnings | Direct removal for internal tools | Varies | Internal tools can move faster |

**Deprecated/outdated:**
- **Wildcard deletion without verification:** Modern practice emphasizes explicit file lists and pre/post verification
- **rm without set -e:** Best practice now includes `set -euo pipefail` to catch errors early
- **Manual file operations:** For tracked files, scripted operations with verification are more reliable

## Open Questions

None - this phase is well-defined with clear success criteria:

1. **File identification:** All duplicate " 2.md" files are identical to their originals (verifiable with `diff`)
2. **Cleanup scope:** Exactly 34 files to remove (32 duplicates + 2 deprecated commands)
3. **Success verification:** Final count should be 30 files (64 - 34 = 30)
4. **Documentation scope:** Two sections to remove from help.md

## Sources

### Primary (HIGH confidence)
- [Command Line Interface Guidelines](https://clig.dev/) - CLI best practices, deprecation patterns
- [Linux Expert Better 2026: Safe File Deletion Guide](https://www.linuxoperatingsystem.net/rm-command-line-in-linux-an-experts-guide-to-safe-and-powerful-file-deletion/) - Safe deletion patterns
- [Fuchsia CLI Tool Help Requirements](https://fuchsia.dev/fuchsia-src/development/api/cli_help) - Documentation standards

### Secondary (MEDIUM confidence)
- [Microsoft WMIC Removal Documentation](https://support.microsoft.com/en-us/topic/windows-management-instrumentation-command-line-wmic-removal-from-windows-e9e83c7f-4992-477f-ba1d-96f694b8665d) - Command deprecation best practices
- [Zapier Engineering: Best Practices Building a CLI Tool](https://zapier.com/engineering/how-to-cli/) - Help documentation patterns
- [npm dedupe documentation](https://docs.npmjs.com/cli/v7/commands/npm-dedupe/) - Duplicate handling patterns (Node.js context)

### Tertiary (LOW confidence)
- [GitHub: git-filter-repo duplicate commits discussion](https://github.com/newren/git-filter-repo/issues/535) - Historical cleanup context
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) - Not needed for this phase (overkill)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - POSIX utilities, well-established patterns
- Architecture: HIGH - Simple file operations, clear verification steps
- Pitfalls: HIGH - Well-documented common mistakes, standard mitigation strategies

**Research date:** 2026-01-30
**Valid until:** 90 days (file operations are stable, unlikely to change)

**Special notes:**
- This phase involves macOS-created duplicate files (the " 2.md" suffix is a macOS file system pattern when files conflict during sync/copy operations)
- The duplicates exist in `.claude/commands/grd/` (the installed location) but verification needed for source `commands/grd/` directory as well
- No libraries needed - this is pure file system operations with standard tools
