# Phase 11: Terminology Rename - Research

**Researched:** 2026-01-30
**Domain:** Large-scale codebase refactoring and CLI command renaming
**Confidence:** HIGH

## Summary

Phase 11 requires renaming 6 lifecycle commands and updating all internal references across 128+ markdown files. This is a standard **large-scale refactoring** task common in CLI tool evolution. The domain is well-established with clear patterns for safe execution.

The standard approach uses:
- **ripgrep** for finding all references (fast, respects gitignore)
- **git mv** for file renames (preserves history)
- **perl -i -pe** for content replacement (cross-platform, works on macOS)
- **Incremental commits** for safe rollback

Key insight: This is NOT a rewrite — it's a systematic rename. The functionality stays identical; only terminology changes. Success depends on comprehensive coverage (finding ALL references) and safe execution (test between steps).

**Primary recommendation:** Execute in 3 atomic waves: (1) rename command files, (2) update command content, (3) update references. Each wave commits separately for rollback safety.

## Standard Stack

The established tools for large-scale code renaming:

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| ripgrep | 14.1.1+ | Pattern finding | 10-100x faster than grep, respects gitignore, filters by file type |
| git | 2.40+ | File renaming | Preserves commit history, enables rollback |
| perl | 5.x | Content replacement | Cross-platform (unlike sed -i), handles regex well |

### Supporting
| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| fd | 10.2.0+ | File finding | Faster alternative to find, user-friendly syntax |
| VS Code | Latest | IDE refactoring | Symbol renaming in code (not needed for markdown) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| ripgrep | grep | grep 10-100x slower, doesn't respect gitignore by default |
| perl -i -pe | sed -i | sed syntax differs macOS vs Linux, perl is portable |
| git mv | mv + git add | git mv preserves history automatically |

**Installation:**
```bash
# macOS (via Homebrew) - already installed per CLAUDE.local.md
brew install ripgrep fd-find

# Verify availability
which rg perl git
```

## Architecture Patterns

### Recommended Execution Structure

This refactoring follows the **expand-contract pattern** adapted for terminology:
1. **Expand**: Create new command files alongside old
2. **Migrate**: Update all references from old → new
3. **Contract**: Remove old command files

**Critical**: Do NOT combine file rename with content changes in same commit. Separate operations for clear git history.

### Pattern 1: Atomic Wave Execution

**What:** Group related changes into atomic commits that can be rolled back independently

**When to use:** Any multi-file refactoring with >20 file changes

**Structure:**
```bash
# Wave 1: Rename command skill files (6 files)
git mv old-name.md new-name.md
git commit -m "rename: command files"

# Wave 2: Update command file content (names, references)
rg pattern | xargs perl -i -pe 's/old/new/g'
git commit -m "refactor: update command content"

# Wave 3: Update all references in other files
rg pattern | xargs perl -i -pe 's/old/new/g'
git commit -m "refactor: update references"
```

**Example from this phase:**
```
Wave 1: Rename 6 command files
  - new-milestone.md → new-study.md
  - complete-milestone.md → complete-study.md
  - discuss-phase.md → scope-study.md
  - plan-phase.md → plan-study.md
  - execute-phase.md → run-study.md
  - verify-work.md → validate-study.md

Wave 2: Update frontmatter names in renamed files
  - grd:new-milestone → grd:new-study
  - (etc for all 6)

Wave 3: Update all references
  - Agent prompts (60+ files)
  - Templates (10+ files)
  - Workflows (12 files)
  - Help documentation
  - Example commands in comments
```

### Pattern 2: Preview Before Modify

**What:** Always preview changes before writing to disk

**When to use:** Every content replacement operation

**Example:**
```bash
# Preview: See what will change
rg "new-milestone" --files-with-matches

# Preview: See exact replacements
rg "new-milestone" | head -20

# Execute: Apply changes
rg "new-milestone" --files-with-matches -0 | \
  xargs -0 perl -i -pe 's/new-milestone/new-study/g'

# Verify: Check git diff
git diff --stat
git diff | head -100
```

### Pattern 3: Scope-Limited Replacement

**What:** Limit replacements to specific file types or directories

**When to use:** Avoid false positives in unrelated files (logs, node_modules, etc.)

**Example:**
```bash
# Only markdown files in .claude directory
rg "grd:discuss-phase" .claude --type md --files-with-matches -0 | \
  xargs -0 perl -i -pe 's/grd:discuss-phase/grd:scope-study/g'

# Only specific directories
rg "Phase \d+:" --glob ".planning/**/*.md" --files-with-matches -0 | \
  xargs -0 perl -i -pe 's/Phase (\d+):/Study \1:/g'
```

### Anti-Patterns to Avoid

- **Big-bang commit**: Don't rename files and update content in one commit. Separate for clear history.
- **Blind sed on macOS**: `sed -i` breaks on macOS without empty string. Use `perl -i -pe` instead.
- **Manual find-replace**: Don't edit files individually. Scripted replacement ensures consistency.
- **Skipping preview**: Always preview before executing. Catch edge cases early.

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Cross-platform find-replace | Custom sed wrapper | `perl -i -pe` | sed -i syntax differs macOS vs Linux, perl is portable |
| File renaming with history | mv + git add | `git mv` | Preserves commit history automatically, one command |
| Finding all occurrences | Manual search | `ripgrep --files-with-matches` | 10-100x faster, respects .gitignore, type filtering |
| Bulk file operations | Shell loops | `xargs -0` with null separator | Handles spaces in filenames, parallel execution |
| Regex replacement in markdown | String replacement | Proper regex anchoring | "phase" in "multiphase" needs word boundaries |

**Key insight:** Large-scale refactoring requires **comprehensive coverage** (find ALL references) and **safe execution** (preview, commit, rollback). Manual approaches miss edge cases. Established tools handle corner cases (spaces in filenames, special characters, symlinks).

## Common Pitfalls

### Pitfall 1: Incomplete Reference Coverage

**What goes wrong:** Miss references in comments, examples, frontmatter, templates, or documentation. Users get "command not found" errors.

**Why it happens:** Focusing only on code, forgetting that CLI tools have references in:
- Command frontmatter (`name: grd:old-command`)
- Help documentation examples
- Agent prompts that spawn commands
- Workflow orchestrators
- Template files
- Comments explaining what commands do

**How to avoid:**
1. Search ALL markdown files, not just commands: `rg "old-command" --type md`
2. Search without file type filtering for edge cases: `rg "old-command"`
3. Check frontmatter specifically: `rg "^name: grd:old-command"`
4. Preview file list before replacing: `rg "pattern" --files-with-matches`

**Warning signs:**
- Rename completes but help shows old commands
- Agents try to spawn old command names
- Examples in documentation reference deleted commands

### Pitfall 2: Word Boundary Issues

**What goes wrong:** Replacing "phase" catches "multiphase" and "rephase". Replacing "milestone" catches "milestone-based" when you wanted "milestone v1.0".

**Why it happens:** Using literal string replacement without regex word boundaries.

**How to avoid:**
Use perl regex with word boundaries:
```bash
# BAD: Catches "rephase", "multiphase"
perl -i -pe 's/phase/study/g'

# GOOD: Only standalone "phase"
perl -i -pe 's/\bphase\b/study/g'

# GOOD: Only "Phase N:" pattern
perl -i -pe 's/Phase (\d+):/Study \1:/g'
```

**Context-specific replacements:**
```bash
# Only frontmatter names
perl -i -pe 's/^name: grd:discuss-phase$/name: grd:scope-study/' file.md

# Only command invocations
perl -i -pe 's/\/grd:discuss-phase/\/grd:scope-study/g'

# Only in specific line context
perl -i -pe 's/Phase (\d+): /Study \1: / if /^#### Phase/'
```

**Warning signs:**
- Git diff shows unexpected replacements
- Compound words broken ("multi-study" instead of "multiphase")
- File paths changed when only content should change

### Pitfall 3: macOS vs Linux Differences

**What goes wrong:** Script works on Linux, breaks on macOS (or vice versa).

**Why it happens:**
- `sed -i` requires empty string on macOS: `sed -i "" ...`
- `xargs` behavior differs (use `-0` for null separator on both)
- Case-sensitive filesystem differences

**How to avoid:**
**Use portable tools:**
```bash
# PORTABLE: Works macOS + Linux
perl -i -pe 's/old/new/g' file.md
rg pattern --files-with-matches -0 | xargs -0 perl -i -pe 's/old/new/g'

# FRAGILE: Breaks on macOS
sed -i 's/old/new/g' file.md
```

**Platform check pattern (if needed):**
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  SED_INPLACE="sed -i ''"
else
  SED_INPLACE="sed -i"
fi
```

**Better:** Just use perl and avoid the problem.

**Warning signs:**
- Command fails with "extra characters" error on macOS
- Script tested on one platform, untested on other

### Pitfall 4: Changing Too Much at Once

**What goes wrong:** Rename 50 things in one commit. Something breaks. Can't identify which change caused the issue. Rollback loses all work.

**Why it happens:** Eagerness to "get it done" without considering rollback scenarios.

**How to avoid:**
**Incremental commits following wave pattern:**
```bash
# Commit 1: Rename command files only
git mv new-milestone.md new-study.md
git mv complete-milestone.md complete-study.md
# ... (all 6 renames)
git add .
git commit -m "rename: lifecycle command files

- new-milestone → new-study
- complete-milestone → complete-study
- discuss-phase → scope-study
- plan-phase → plan-study
- execute-phase → run-study
- verify-work → validate-study"

# Commit 2: Update command frontmatter
# (single focused change)
git add .
git commit -m "refactor: update command names in frontmatter"

# Commit 3: Update agent references
# (another focused change)
git add .
git commit -m "refactor: update command names in agents"
```

**Rollback becomes surgical:**
```bash
# Broke at commit 3? Revert just that commit
git revert HEAD

# Need to redo commit 2? Reset to commit 1, redo
git reset --hard HEAD~2
```

**Warning signs:**
- Git diff shows 50+ files changed
- Multiple types of changes in one commit (renames + content + docs)
- Fear of committing because "not done yet"

## Code Examples

Verified patterns from official sources:

### Find All References (ripgrep)
```bash
# Source: https://learnbyexample.github.io/learn_gnugrep_ripgrep/ripgrep.html
# Find all files containing pattern
rg "new-milestone" --files-with-matches

# Filter by file type
rg "new-milestone" --type md --files-with-matches

# Search specific directory
rg "grd:discuss-phase" .claude/ --files-with-matches

# Show context (3 lines before/after)
rg "new-milestone" -C 3

# Count matches per file
rg "Phase \d+:" --count
```

### Safe Batch Replacement (ripgrep + perl)
```bash
# Source: https://dev.to/webduvet/efficiently-finding-and-replacing-text-in-multiple-files-using-ripgrep-and-sed-3anl
# Pattern: Find files with ripgrep, replace with perl
rg "pattern" --files-with-matches -0 | \
  xargs -0 perl -i -pe 's/old/new/g'

# With preview before execution
echo "Files that will be modified:"
rg "new-milestone" --files-with-matches
echo "Press enter to continue..."
read
rg "new-milestone" --files-with-matches -0 | \
  xargs -0 perl -i -pe 's/new-milestone/new-study/g'
```

### Preserve Git History (git mv)
```bash
# Source: https://thelinuxcode.com/git-move-files-practical-renames-refactors-and-history-preservation-in-2026/
# Single file rename
git mv old-name.md new-name.md

# Batch rename with loop
for file in discuss-phase plan-phase execute-phase; do
  git mv "commands/grd/${file}.md" "commands/grd/${file%%-phase}-study.md"
done

# Verify history preserved
git log --follow -- new-name.md
```

### Context-Aware Replacement (perl)
```bash
# Replace with word boundaries
perl -i -pe 's/\bphase\b/study/g' file.md

# Replace only in specific context (frontmatter)
perl -i -pe 's/^name: grd:(\S+)$/name: grd:\1/ if /^name:/' file.md

# Capture groups for transformation
perl -i -pe 's/Phase (\d+):/Study \1:/g' file.md
perl -i -pe 's/Milestone v(\S+)/Version v\1/g' file.md

# Multi-line replacement (use -0777)
perl -i -0777 -pe 's/old-pattern\nwith-newlines/new-pattern\nwith-newlines/g' file.md
```

### Verification Pattern
```bash
# After replacement, verify changes
git status  # Show modified files
git diff --stat  # Show change summary
git diff -- file.md  # Review specific file changes
git diff | grep "^[-+]" | head -50  # Preview additions/deletions

# Check for leftover old references
rg "new-milestone|complete-milestone|discuss-phase" --count
# Should return 0 matches after complete rename
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual find-replace in editor | ripgrep + automated replacement | ~2020 | 100x faster, comprehensive coverage |
| sed for content replacement | perl -i -pe for portability | ~2021 | Cross-platform compatibility (macOS + Linux) |
| Single big-bang commit | Incremental atomic commits | ~2022 | Safe rollback, clear history |
| File rename then content change (one commit) | Separate file rename + content commits | ~2023 | Git tracks renames better, easier to review |

**Deprecated/outdated:**
- **grep for finding**: ripgrep is 10-100x faster and respects .gitignore by default
- **sed -i without platform check**: Breaks on macOS, use perl -i -pe instead
- **Manual editor search/replace**: Error-prone for 100+ files, use scripted approach
- **Big-bang refactoring commits**: Modern practice is atomic commits per change type

## Open Questions

Things that couldn't be fully resolved:

1. **Backward compatibility**
   - What we know: Phase 11 renames commands with no deprecation period
   - What's unclear: Whether any external tools/scripts depend on old command names
   - Recommendation: Check for external references outside `.claude/` before renaming. Low risk since GRD is internal tooling.

2. **Version numbering terminology**
   - What we know: "milestone" → "version" for release groupings (v1.0, v1.1)
   - What's unclear: Whether existing git tags (if any) should be renamed
   - Recommendation: Leave git tags unchanged (they're historical). Only update future references.

3. **File path terminology**
   - What we know: Directory `.planning/phases/` stays as-is per context
   - What's unclear: Whether "phase" in directory name creates confusion with "study" terminology
   - Recommendation: Keep directory structure unchanged. Only update content terminology. Directory rename out of scope.

## Sources

### Primary (HIGH confidence)
- [ripgrep documentation](https://learnbyexample.github.io/learn_gnugrep_ripgrep/ripgrep.html) - Search and filtering patterns
- [Git Move Files: Practical Renames in 2026](https://thelinuxcode.com/git-move-files-practical-renames-refactors-and-history-preservation-in-2026/) - History preservation techniques
- [Efficiently Finding and Replacing Text with ripgrep and sed](https://dev.to/webduvet/efficiently-finding-and-replacing-text-in-multiple-files-using-ripgrep-and-sed-3anl) - Batch replacement patterns

### Secondary (MEDIUM confidence)
- [Code Refactoring: When to Refactor and How to Avoid Mistakes](https://www.tembo.io/blog/code-refactoring) - Incremental approach best practices
- [Good Refactoring vs Bad Refactoring](https://www.builder.io/blog/good-vs-bad-refactoring) - Anti-patterns (big-bang commits)
- [How to break up a large code refactor](https://viktorstanchev.com/posts/how-to-break-up-a-large-code-refactor/) - Atomic wave execution pattern

### Tertiary (LOW confidence)
- [WebStorm TypeScript Refactoring](https://www.jetbrains.com/help/webstorm/specific-typescript-refactorings.html) - IDE refactoring (not applicable to markdown)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - ripgrep, git, perl are mature, well-documented tools with 5+ years of stable usage
- Architecture: HIGH - Wave-based refactoring is established pattern, well-documented in multiple sources
- Pitfalls: HIGH - Common mistakes verified across multiple refactoring guides (word boundaries, platform differences, atomic commits)

**Research date:** 2026-01-30
**Valid until:** 90 days (stable domain — tools and patterns evolve slowly)
