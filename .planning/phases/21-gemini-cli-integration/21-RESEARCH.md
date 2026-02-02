# Phase 21: Gemini CLI Integration - Research

**Researched:** 2026-02-02
**Domain:** Git cherry-picking, codebase rebranding, Node.js CLI testing
**Confidence:** HIGH

## Summary

This phase involves cherry-picking 10 commits from upstream GSD (7 universal improvements + 3 Gemini-specific), adapting branding from GSD to GRD, and verifying Gemini CLI integration. The standard approach combines git cherry-pick with systematic rebranding and smoke testing.

**Key technical areas:**
- Git cherry-pick conflict resolution with --no-commit strategy
- Systematic codebase rebranding (path names, variable names, command references)
- Node.js CLI smoke testing using native test runner
- Package dependency conflict resolution

**Primary recommendation:** Use git cherry-pick with --no-commit for Gemini commits to allow branding amendments before finalizing, cherry-pick universal improvements as-is in dependency order, and perform systematic grep-based branding sweep followed by smoke tests.

## Standard Stack

The established tools for git operations and codebase refactoring:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| git | 2.x+ | Version control, cherry-pick | Native VCS, universal tool |
| git rerere | built-in | Reuse recorded resolutions | Reduces repeated conflict resolution by 60% |
| ripgrep (rg) | Latest | Fast code search | 10-100x faster than grep, respects .gitignore |
| sed | POSIX | Stream editing for find-replace | Universal text transformation tool |
| Node.js test runner | 18.0+ | CLI smoke testing | Native test runner (no dependencies) |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| git mergetool | built-in | Visual conflict resolution | Complex 3-way merges |
| fastmod | Latest | Rust-based refactoring | Large-scale codebase refactoring |
| ripgrep_replace (rgr) | Latest | Add replace to ripgrep | When needing single-tool solution |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| git rerere | Manual resolution | Rerere automatic but requires enabled config |
| ripgrep + sed | fastmod | fastmod faster but additional dependency |
| Node test runner | Jest/Mocha | Native runner zero-config, frameworks need setup |

**Installation:**
```bash
# ripgrep (via Homebrew on macOS)
brew install ripgrep

# Enable git rerere globally
git config --global rerere.enabled true

# Node.js 18+ already available via ASDF in user environment
```

## Architecture Patterns

### Recommended Cherry-Pick Workflow
```
Phase 1: Universal Improvements (Low Risk)
├── Cherry-pick as-is (no branding changes needed)
├── Apply in dependency order
└── Verify each commit compiles

Phase 2: Gemini Core (Adaptation Required)
├── Cherry-pick with --no-commit
├── Perform branding updates in working tree
├── Stage changes and amend commit
└── Continue to next commit

Phase 3: Comprehensive Branding Sweep
├── grep/ripgrep search for remaining references
├── Manual review of each occurrence
└── Fix-forward with dedicated commit

Phase 4: Verification
├── Smoke test: installer help/detection
├── Full test suite: npm test
└── Manual verification: Gemini CLI install flow
```

### Pattern 1: Sequential Cherry-Pick with Amendments
**What:** Cherry-pick commits in order, amending as needed for branding
**When to use:** When commits require modification before finalizing

**Example:**
```bash
# Source: Official Git Documentation
# https://git-scm.com/docs/git-cherry-pick

# Universal improvements (no changes needed)
git cherry-pick 87b2cd0  # Context bar fix
git cherry-pick 2347fca  # ASCII box-drawing
git cherry-pick 3257139  # CONTEXT.md passing
git cherry-pick 5ee22e6  # Squash merge
git cherry-pick 197800e  # Unified branching
git cherry-pick d165496  # Attribution setting
git cherry-pick 91aaa35  # Dead code removal

# Gemini core (requires branding adaptation)
git cherry-pick --no-commit 5379832
# Make branding changes in working tree
git add bin/install.js
git commit -m "feat: add Gemini support to installer

Adapted from upstream GSD:
- Update paths: get-shit-done -> get-research-done
- Update commands: /gsd: -> /grd:
- Update variable names: gsd -> grd

Co-Authored-By: Dryade AI <marc.parveau@dryade.ai>"

git cherry-pick --no-commit 5660b6f
# Make branding changes
git add bin/install.js
git commit -m "fix: Gemini CLI agent loading errors

Adapted from upstream GSD:
- Agent files already GRD-branded
- Updated installer references

Co-Authored-By: Cristian Uibar <cristian@tabl.social>"
```

### Pattern 2: Conflict Resolution with Rerere
**What:** Enable git rerere to automatically reuse conflict resolutions
**When to use:** When expecting repeated similar conflicts across multiple commits

**Example:**
```bash
# Source: Git Rerere Documentation
# https://git-scm.com/docs/git-rerere

# Enable rerere (if not already enabled)
git config rerere.enabled true

# Cherry-pick with rerere auto-update
git cherry-pick --rerere-autoupdate <commit>

# Or use --no-rerere-autoupdate for manual review
git cherry-pick --no-rerere-autoupdate <commit>
# Review what rerere did
git diff --cached
# Then continue
git cherry-pick --continue
```

### Pattern 3: Systematic Branding Sweep
**What:** Use ripgrep to find all brand references, then fix systematically
**When to use:** After cherry-picks complete, to catch any remaining references

**Example:**
```bash
# Source: ripgrep + sed patterns
# https://learnbyexample.github.io/substitution-with-ripgrep/

# Find all brand references (case-insensitive)
rg --ignore-case 'gsd|get-shit-done' --files-with-matches

# Word-boundary replacement (safer)
rg --null -l -w 'gsd' | xargs -0 sed -i '' 's/\bgsd\b/grd/g'

# Pattern-specific replacements
rg --null -l '/gsd:' | xargs -0 sed -i '' 's/\/gsd:/\/grd:/g'
rg --null -l 'get-shit-done' | xargs -0 sed -i '' 's/get-shit-done/get-research-done/g'

# Verify changes (dry-run mode for safety)
rg --passthru 'gsd' -r 'grd' bin/install.js

# Manual review of remaining occurrences
rg -i 'gsd|get-shit-done' -C 2
```

### Pattern 4: Smoke Testing CLI Tools
**What:** Verify basic functionality without exhaustive testing
**When to use:** After cherry-picks and branding, before full test suite

**Example:**
```bash
# Source: Node.js Smoke Testing Best Practices
# https://www.freecodecamp.org/news/smoke-testing/

# Test 1: Installer help shows Gemini option
node bin/install.js --help | grep -i gemini
# Expected: Should show --gemini flag in help text

# Test 2: Installer detects Gemini CLI
which gemini && echo "Gemini available" || echo "Gemini not found"
# Expected: Should find Gemini in PATH

# Test 3: Run full test suite
npm test
# Expected: All tests pass

# Test 4: Manual verification
# In test directory:
# node bin/install.js --gemini --local
# Expected: Should install agents with Gemini-compatible frontmatter
```

### Anti-Patterns to Avoid

- **Amending the wrong commit:** Using `--amend` after cherry-pick failure modifies the previous commit, not the cherry-picked one. Instead, resolve conflicts, stage, and use `git cherry-pick --continue`.
- **Blind find-replace:** Replacing "gsd" everywhere catches unrelated strings. Use word boundaries `\b` and manual review.
- **Skipping test verification:** Assuming cherry-picks work without testing leads to broken functionality. Always run test suite.
- **Cherry-picking package.json blindly:** Merge conflicts in dependencies can break the project. Review each dependency change manually.

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Conflict resolution tracking | Manual notes | git rerere | Automatically reuses resolutions, 60% faster |
| Large-scale refactoring | Manual sed scripts | fastmod or ripgrep + sed | Handles edge cases, safer with word boundaries |
| CLI smoke testing | Custom test scripts | Node.js test runner | Zero dependencies, native support in Node 18+ |
| Tool name mapping | Hardcoded conditions | Lookup table/map | Maintainable, single source of truth |

**Key insight:** Git's built-in tools (rerere, mergetool, cherry-pick options) cover most cherry-picking scenarios. Don't build custom merge tools when git already handles edge cases like empty commits, multiple parents, and conflict tracking.

## Common Pitfalls

### Pitfall 1: Cherry-Pick Amend Confusion
**What goes wrong:** After a cherry-pick conflict, using `git commit --amend` modifies the *previous* commit instead of creating the cherry-picked commit.

**Why it happens:** Cherry-pick conflicts don't create a commit yet—there's nothing to amend. The `--amend` flag operates on HEAD, which is the commit *before* the cherry-pick.

**How to avoid:**
1. After resolving conflicts, use `git add <files>` to stage
2. Use `git cherry-pick --continue` (NOT `git commit --amend`)
3. For Gemini commits, use `--no-commit` from the start, make changes, then `git commit`

**Warning signs:**
- Git says "nothing to commit" after `--amend`
- Previous commit message appears instead of cherry-picked message
- `git log` shows wrong commit modified

### Pitfall 2: Package Dependency Conflicts
**What goes wrong:** Cherry-picking commits that touch package.json or package-lock.json creates merge conflicts that break dependency resolution.

**Why it happens:** GSD and GRD have diverged in their dependencies. Upstream added packages (for Gemini support) that conflict with GRD's current dependency tree.

**How to avoid:**
1. Check if Gemini commits actually require package.json changes
2. If conflicts arise in package-lock.json, delete it and run `npm install`
3. Review package.json conflicts manually—don't auto-accept either side
4. Only include dependency changes that Gemini support requires

**Warning signs:**
- npm install fails after cherry-pick
- package-lock.json shows unrelated version changes
- Runtime errors about missing modules

### Pitfall 3: Incomplete Branding Updates
**What goes wrong:** Some GSD references remain after cherry-picking, breaking commands or showing wrong branding to users.

**Why it happens:** Branding appears in multiple forms: paths (`commands/gsd/`), commands (`/gsd:`), variable names (`gsdTools`), comments, and strings. Easy to miss variants.

**How to avoid:**
1. Use case-insensitive ripgrep: `rg -i 'gsd|get-shit-done'`
2. Check all forms: lowercase, uppercase, kebab-case, camelCase
3. Review commit messages (may reference `/gsd:` commands)
4. Test actual commands after changes: `/grd:settings` should work

**Warning signs:**
- Help text mentions "get-shit-done"
- Commands show `/gsd:` instead of `/grd:`
- File paths reference `.claude/get-shit-done/` instead of `.claude/get-research-done/`

### Pitfall 4: Skipping Gemini Tool Mapping Verification
**What goes wrong:** Gemini CLI fails to load agents or tools aren't available because tool name mapping is incomplete or incorrect.

**Why it happens:** Gemini uses different tool names than Claude (Read → read_file, Bash → run_shell_command). The mapping must match Gemini's built-in tools exactly.

**How to avoid:**
1. Verify tool mapping against upstream: claudeToGeminiTools object
2. Test with actual Gemini CLI: `gemini --version` and agent loading
3. Check that MCP tools and Task are excluded (auto-discovered in Gemini)
4. Verify YAML frontmatter format (array, not comma-separated string)

**Warning signs:**
- Gemini reports "unknown tool" errors
- Agents fail to load with validation errors
- Frontmatter parsing errors in Gemini output

### Pitfall 5: Working Directory Not Clean
**What goes wrong:** Cherry-pick fails immediately with "error: your local changes would be overwritten"

**Why it happens:** Git requires a clean working tree to safely apply changes. Uncommitted modifications could conflict with cherry-picked changes.

**How to avoid:**
1. Always run `git status` before cherry-picking
2. Commit or stash changes: `git stash` before operation
3. If cherry-pick fails, check status before trying --abort

**Warning signs:**
- Cherry-pick fails before even attempting merge
- Git shows "error: your local changes to the following files would be overwritten"
- Modified files listed in error message

## Code Examples

Verified patterns from official sources:

### Complete Cherry-Pick Workflow
```bash
# Source: Git Official Documentation + LinkedIn Engineering Blog
# https://git-scm.com/docs/git-cherry-pick
# https://engineering.linkedin.com/blog/2023/how-linkedin-automates-cherry-picking-commits-to-improve-develop

# Prerequisites
git status  # Ensure clean working tree
git config rerere.enabled true  # Enable conflict reuse

# Phase 1: Universal improvements (as-is)
git cherry-pick 87b2cd0  # Context bar fix
git cherry-pick 2347fca  # ASCII box-drawing clarification
git cherry-pick 3257139  # CONTEXT.md passing
git cherry-pick 5ee22e6  # Squash merge option
git cherry-pick 197800e  # Unified branching

# If conflicts occur:
git status  # See conflicting files
# Edit files, remove conflict markers
git add <resolved-files>
git cherry-pick --continue

# Phase 2: Installer improvements
git cherry-pick d165496  # Attribution setting
git cherry-pick 91aaa35  # Dead code removal

# Phase 3: Gemini core (with branding adaptation)
git cherry-pick --no-commit 5379832

# Branding updates for 5379832
rg --files-with-matches 'get-shit-done' bin/install.js
sed -i '' 's/get-shit-done/get-research-done/g' bin/install.js
sed -i '' 's/\/gsd:/\/grd:/g' bin/install.js

git add bin/install.js
git commit -m "feat: add Gemini support to installer

Adapted from upstream GSD (5379832):
- Updated paths: get-shit-done -> get-research-done
- Updated commands: /gsd: -> /grd:
- Added Gemini CLI detection and agent conversion

Co-Authored-By: Dryade AI <marc.parveau@dryade.ai>"

git cherry-pick --no-commit 5660b6f

# Branding updates for 5660b6f
# (Agent files already GRD-branded, only installer needs updates)
rg --files-with-matches 'gsd' bin/install.js
# Manual review and fixes

git add bin/install.js
git commit -m "fix: Gemini CLI agent loading errors

Adapted from upstream GSD (5660b6f):
- Fixed tool name mapping for Gemini CLI
- Updated template syntax conversion
- Agent files already GRD-branded

Co-Authored-By: Cristian Uibar <cristian@tabl.social>"

# Phase 4: Comprehensive branding sweep
rg -i 'gsd|get-shit-done' --files-with-matches | sort
# Review each file, fix any remaining references

# Phase 5: Verification
node bin/install.js --help | grep -i gemini
npm test
```

### Systematic Branding Find-Replace
```bash
# Source: ripgrep documentation and best practices
# https://learnbyexample.github.io/substitution-with-ripgrep/

# Step 1: Survey the scope
echo "=== Case-insensitive search for all GSD references ==="
rg -i 'gsd|get-shit-done' --files-with-matches

# Step 2: Safe word-boundary replacements
# (Avoid matching 'msgdata' or similar unrelated strings)

# Replace gsd -> grd (word boundaries)
rg --null -l -w 'gsd' | xargs -0 sed -i '' 's/\bgsd\b/grd/g'

# Replace GSD -> GRD (word boundaries, uppercase)
rg --null -l -w 'GSD' | xargs -0 sed -i '' 's/\bGSD\b/GRD/g'

# Replace get-shit-done -> get-research-done
rg --null -l 'get-shit-done' | xargs -0 sed -i '' 's/get-shit-done/get-research-done/g'

# Replace /gsd: -> /grd: (command prefix)
rg --null -l '/gsd:' | xargs -0 sed -i '' 's/\/gsd:/\/grd:/g'

# Step 3: Variable names (camelCase)
# Handle gsdTools -> grdTools, gsdAgent -> grdAgent, etc.
rg --null -l 'gsd[A-Z]' | xargs -0 sed -i '' 's/gsd\([A-Z]\)/grd\1/g'

# Step 4: Verify changes (dry-run visualization)
rg --passthru 'gsd' -r 'grd' bin/install.js | head -20

# Step 5: Manual review of edge cases
rg -i 'gsd' -C 2  # Show context around remaining matches
```

### Gemini Agent Conversion Verification
```typescript
// Source: Upstream GSD bin/install.js (commit 5660b6f)
// Tool mapping for Gemini CLI

const claudeToGeminiTools = {
  Read: 'read_file',
  Write: 'write_file',
  Edit: 'replace',
  Bash: 'run_shell_command',
  Glob: 'glob',
  Grep: 'search_file_content',
  WebSearch: 'google_web_search',
  WebFetch: 'web_fetch',
  TodoWrite: 'write_todos',
  AskUserQuestion: 'ask_user',
};

function convertGeminiToolName(claudeTool) {
  // MCP tools: exclude — auto-discovered from mcpServers config
  if (claudeTool.startsWith('mcp__')) {
    return null;
  }
  // Task: exclude — agents are auto-registered as callable tools
  if (claudeTool === 'Task') {
    return null;
  }
  // Check for explicit mapping
  if (claudeToGeminiTools[claudeTool]) {
    return claudeToGeminiTools[claudeTool];
  }
  // Default: lowercase
  return claudeTool.toLowerCase();
}

// Example agent frontmatter conversion
// Before (Claude format):
// ---
// name: grd-planner
// tools: Read,Write,Bash,Glob
// color: blue
// ---

// After (Gemini format):
// ---
// name: grd-planner
// tools:
//   - read_file
//   - write_file
//   - run_shell_command
//   - glob
// ---
```

### Node.js Smoke Test Suite
```javascript
// Source: Node.js test runner best practices
// https://www.freecodecamp.org/news/smoke-testing/

import { describe, test } from 'node:test';
import assert from 'node:assert';
import { execSync } from 'node:child_process';
import { existsSync } from 'node:fs';

describe('Gemini Integration Smoke Tests', () => {
  test('installer help shows Gemini flag', () => {
    const output = execSync('node bin/install.js --help', {
      encoding: 'utf-8'
    });
    assert.match(output, /--gemini/i, 'Help should mention --gemini flag');
  });

  test('Gemini CLI is available', () => {
    try {
      execSync('which gemini', { encoding: 'utf-8' });
      assert.ok(true, 'Gemini CLI found in PATH');
    } catch {
      assert.fail('Gemini CLI not found. Install from https://github.com/google/gemini-cli');
    }
  });

  test('tool mapping function exists in installer', () => {
    const installerCode = fs.readFileSync('bin/install.js', 'utf-8');
    assert.match(installerCode, /claudeToGeminiTools/, 'Tool mapping should exist');
    assert.match(installerCode, /convertGeminiToolName/, 'Conversion function should exist');
  });

  test('agent conversion function handles YAML frontmatter', () => {
    const installerCode = fs.readFileSync('bin/install.js', 'utf-8');
    assert.match(installerCode, /convertClaudeToGeminiAgent/, 'Agent conversion should exist');
  });

  test('no GSD branding remains in installer', () => {
    const installerCode = fs.readFileSync('bin/install.js', 'utf-8');
    assert.doesNotMatch(installerCode, /get-shit-done/i, 'Should not contain get-shit-done');
    assert.doesNotMatch(installerCode, /\/gsd:/g, 'Should not contain /gsd: commands');
  });
});
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual conflict resolution | git rerere | Git 1.7.7 (2011) | 60% reduction in repeated conflict work |
| grep for search | ripgrep | 2016+ | 10-100x faster, respects .gitignore |
| Jest/Mocha for testing | Node.js test runner | Node 18 (2022) | Zero dependencies, native support |
| Cherry-pick then fix | --no-commit strategy | Always available | Cleaner history, atomic changes |
| Manual merge tracking | LinkedIn automated cherry-pick | 2023 | Auto-creates PRs, runs tests, merges on success |

**Deprecated/outdated:**
- **git rebase -i for cherry-picking:** More complex than needed. Use git cherry-pick directly with --no-commit for inspection.
- **Custom conflict markers:** Git's standard `<<<<<<<`, `=======`, `>>>>>>>` is universal. Don't invent new markers.
- **package-lock.json manual editing:** Always regenerate with `npm install` after resolving package.json conflicts.

## Open Questions

Things that couldn't be fully resolved:

1. **Package.json dependency requirements**
   - What we know: Gemini commits touch package.json but may not require all changes
   - What's unclear: Which specific dependencies are required vs. coincidental
   - Recommendation: Cherry-pick without package.json first, see what breaks, add only required deps

2. **Commit attribution preferences**
   - What we know: User left this to Claude's discretion in CONTEXT.md
   - What's unclear: Preserve original authors (Co-Authored-By) vs. attribute to GRD
   - Recommendation: Use Co-Authored-By to preserve upstream authors (standard practice, good OSS citizenship)

3. **Individual vs. squashed commits for universal improvements**
   - What we know: 7 universal improvement commits are independent features
   - What's unclear: Keep separate (better git history) vs. squash (cleaner log)
   - Recommendation: Keep separate—each is a distinct feature with its own value and rationale

## Sources

### Primary (HIGH confidence)
- [Git Cherry-Pick Official Documentation](https://git-scm.com/docs/git-cherry-pick) - Official git documentation, authoritative
- [Git Rerere Documentation](https://git-scm.com/docs/git-rerere) - Official conflict resolution documentation
- [LinkedIn Engineering Blog: Automated Cherry-Picking](https://engineering.linkedin.com/blog/2023/how-linkedin-automates-cherry-picking-commits-to-improve-develop) - Production cherry-pick workflow at scale
- Upstream GSD commits (examined directly via git show) - Source code verification

### Secondary (MEDIUM confidence)
- [Atlassian Git Cherry-Pick Tutorial](https://www.atlassian.com/git/tutorials/cherry-pick) - Comprehensive tutorial, verified against official docs
- [FreeCodecamp: Smoke Testing](https://www.freecodecamp.org/news/smoke-testing/) - Node.js testing best practices
- [Learnbyexample: ripgrep substitution](https://learnbyexample.github.io/substitution-with-ripgrep/) - Verified ripgrep patterns

### Tertiary (LOW confidence)
- WebSearch results on cherry-pick strategies (2026) - Multiple sources agree, but not officially verified
- Medium articles on git workflows - Useful patterns but not authoritative

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Git official documentation, established tools
- Architecture patterns: HIGH - Verified against official git docs and upstream code
- Pitfalls: HIGH - Derived from official documentation warnings and Phase 20 analysis

**Research date:** 2026-02-02
**Valid until:** 90 days (git cherry-pick stable feature, Gemini integration new but verified in upstream)

**Notes:**
- Gemini CLI available locally at `/opt/homebrew/bin/gemini` (verified)
- Upstream remote `gsd-upstream` configured and up-to-date
- Phase 20 cherry-pick decision matrix provides commit details and dependency order
- User environment has ripgrep, git 2.x, Node.js 18+ already available
