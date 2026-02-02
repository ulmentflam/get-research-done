# Phase 20: GSD Sync Setup & Exploration - Research

**Researched:** 2026-02-02
**Domain:** Git remote management and selective feature integration from forked repositories
**Confidence:** HIGH

## Summary

This phase establishes synchronization with the upstream GSD repository to identify and cherry-pick new features added after GRD forked. GRD forked from GSD at commit 1fe3fa4 (December 14, 2025) and has since diverged significantly with research-focused branding and workflows. The upstream GSD repository has continued development, most notably adding native Gemini CLI support in v1.10.0 (January 29, 2026).

The standard approach is: (1) add GSD as an "upstream" remote, (2) fetch all upstream branches and commits, (3) use git log and git diff to identify new features since the fork point, (4) document cherry-pick decisions based on GRD's research-focused identity, and (5) selectively apply commits using git cherry-pick with conflict resolution.

**Primary recommendation:** Add upstream remote immediately, document all new GSD features since fork (especially Gemini CLI integration commits), then create a decision matrix for what to cherry-pick vs. skip based on GRD's research workflow focus.

## Standard Stack

The established tools for fork synchronization and selective feature integration:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| git | 2.x+ | Version control with remote management | Industry standard for fork workflows |
| git remote | built-in | Multi-remote repository management | Native Git support for upstream/origin pattern |
| git fetch | built-in | Retrieve upstream changes without merging | Safe exploration of upstream changes |
| git cherry-pick | built-in | Selective commit application | Standard for applying specific commits across branches |
| git log | built-in | Commit history analysis | Core tool for identifying changes since divergence |
| git diff | built-in | Change comparison between branches | Essential for understanding scope of changes |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| git merge-base | built-in | Find common ancestor commits | Identify exact fork point for comparison |
| gh cli | 2.x+ | GitHub API interactions | Fetch commit details, PR history, release notes |
| git log --graph | built-in | Visualize branch topology | Understand parallel development paths |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Cherry-pick | Merge upstream/main | Brings all changes including breaking ones |
| Manual remote add | GitHub "Sync fork" UI | Works but misses selective feature adoption |
| Cherry-pick range | Rebase onto upstream | Rewrites history, loses GRD commit trail |

**Installation:**
```bash
# No installation needed - native Git commands
git --version  # Verify Git 2.x+
gh --version   # Optional: GitHub CLI for richer commit exploration
```

## Architecture Patterns

### Recommended Remote Structure
```
GRD Repository (local)
├── origin/          # Points to ulmentflam/get-research-done
│   ├── main         # GRD's main branch (current work)
│   └── ...
└── gsd-upstream/    # Points to glittercowboy/get-shit-done
    ├── main         # Upstream GSD development
    └── ...
```

### Pattern 1: Upstream Remote Configuration
**What:** Configure GSD as a tracked upstream remote for ongoing synchronization
**When to use:** Initial setup and any future sync operations
**Example:**
```bash
# Source: Git official documentation + GitHub fork workflows
# https://docs.github.com/articles/fork-a-repo

# Add GSD upstream remote
git remote add gsd-upstream https://github.com/glittercowboy/get-shit-done.git

# Verify remotes
git remote -v
# origin         git@github.com:ulmentflam/get-research-done.git (fetch)
# origin         git@github.com:ulmentflam/get-research-done.git (push)
# gsd-upstream   https://github.com/glittercowboy/get-shit-done.git (fetch)
# gsd-upstream   https://github.com/glittercowboy/get-shit-done.git (push)

# Fetch all upstream branches and commits
git fetch gsd-upstream
```

### Pattern 2: Feature Discovery with Three-Dot Notation
**What:** Use git log and git diff with three-dot notation to find changes since fork point
**When to use:** Identifying what's new in upstream since divergence
**Example:**
```bash
# Source: Git documentation + Atlassian Git tutorials
# https://www.atlassian.com/git/tutorials/git-log

# Find commits in upstream not in GRD
git log --oneline --no-merges main..gsd-upstream/main

# Find files changed since fork point (three-dot = since common ancestor)
git diff --name-status main...gsd-upstream/main

# Get detailed commit messages for feature identification
git log --pretty=format:"%h - %an, %ar : %s" main..gsd-upstream/main

# Find merge base (fork point) explicitly
git merge-base main gsd-upstream/main
```

### Pattern 3: Selective Cherry-Pick Strategy
**What:** Cherry-pick commits by feature category with conflict resolution workflow
**When to use:** Applying upstream features while preserving GRD identity
**Example:**
```bash
# Source: Atlassian Git Cherry-Pick Tutorial + GitHub workflows
# https://www.atlassian.com/git/tutorials/cherry-pick

# Cherry-pick single commit
git cherry-pick <commit-hash>

# Cherry-pick range of commits (include ^ to include start commit)
git cherry-pick <start-hash>^..<end-hash>

# If conflicts occur:
# 1. Resolve conflicts in affected files
# 2. Stage resolved files
git add <resolved-files>

# 3. Continue cherry-pick
git cherry-pick --continue

# Or skip problematic commit
git cherry-pick --skip

# Or abort entire operation
git cherry-pick --abort
```

### Pattern 4: Feature Decision Matrix
**What:** Structured decision framework for cherry-pick vs. skip choices
**When to use:** Evaluating each upstream feature against GRD's research focus
**Example:**
```markdown
| Feature | Commits | Decision | Rationale |
|---------|---------|----------|-----------|
| Gemini CLI support | abc123, def456 | CHERRY-PICK | Aligns with GRD multi-platform goal |
| New gsd-researcher agent | ghi789 | SKIP | GRD has grd-explorer (different approach) |
| Context compliance checker | jkl012 | CHERRY-PICK | Universal quality improvement |
| Branching strategies | mno345 | EVALUATE | May conflict with GRD study workflow |
```

### Anti-Patterns to Avoid
- **Blind merge of upstream/main:** Brings breaking changes and GSD-specific features that conflict with GRD branding
- **Cherry-picking without testing:** Each cherry-picked commit should be tested individually before proceeding
- **Ignoring conflict markers:** Incomplete conflict resolution leads to broken code
- **Cherry-picking merge commits:** Creates duplicate history and confusion (use --no-merges flag)

## Don't Hand-Roll

Problems that look simple but have existing Git solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Finding fork point | Manual commit date comparison | `git merge-base main gsd-upstream/main` | Handles complex branching, rebases, multiple ancestors |
| Comparing branches | Diff each file individually | `git diff --name-status main...gsd-upstream/main` | Three-dot notation finds common ancestor automatically |
| Tracking cherry-picked commits | Manual spreadsheet | Git commit messages with "(cherry picked from commit xyz)" | Git cherry-pick adds this automatically with -x flag |
| Conflict detection before apply | Try and see what breaks | `git cherry-pick -n <commit>` (no commit, preview only) | Dry-run mode shows conflicts without committing |
| Multiple commit selection | Script to loop through commits | `git cherry-pick <hash>^..<hash>` | Native range syntax handles sequence correctly |

**Key insight:** Git's fork workflow tooling is battle-tested across millions of open-source projects. The three-dot notation, merge-base, and cherry-pick sequencing handle edge cases (rebases, non-linear history, octopus merges) that custom scripts miss.

## Common Pitfalls

### Pitfall 1: Two-Dot vs Three-Dot Confusion
**What goes wrong:** Using `git diff main..gsd-upstream/main` (two dots) compares branch tips, not changes since fork
**Why it happens:** Two-dot and three-dot syntax look similar but have different semantics
**How to avoid:** Always use three dots (`...`) for fork comparisons: `git diff main...gsd-upstream/main` compares upstream's tip to the common ancestor
**Warning signs:** Diff shows changes from both repositories; unrelated commits appear in log

### Pitfall 2: Cherry-Picking Without Commit Context
**What goes wrong:** Cherry-picking commit B that depends on commit A fails with conflicts or broken functionality
**Why it happens:** Commits often have implicit dependencies (API changes, refactors, config updates)
**How to avoid:** Use `git log -p <commit-hash>` to read full diff; check preceding commits for dependencies; test after each cherry-pick
**Warning signs:** Tests break after cherry-pick; undefined variables/functions appear; imports fail

### Pitfall 3: Merge Commits in Cherry-Pick Range
**What goes wrong:** Cherry-picking a merge commit duplicates history and creates confusing parent relationships
**Why it happens:** `git log main..gsd-upstream/main` includes merge commits by default
**How to avoid:** Always use `--no-merges` flag: `git log --no-merges main..gsd-upstream/main`
**Warning signs:** Git complains about "mainline parent"; duplicate commits appear with different hashes

### Pitfall 4: Incomplete Conflict Resolution
**What goes wrong:** Leaving conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) in code causes syntax errors
**Why it happens:** Forgetting to remove markers after choosing changes; not testing after resolution
**How to avoid:** After resolving conflicts, search for marker strings: `grep -r "<<<<<<< HEAD" .`; run tests before `git cherry-pick --continue`
**Warning signs:** Build failures; syntax errors in previously working files; grep finds conflict markers

### Pitfall 5: Cherry-Picking into Dirty Working Directory
**What goes wrong:** Cherry-pick conflicts with uncommitted local changes, creating unrecoverable mixed state
**Why it happens:** Starting cherry-pick without clean working tree
**How to avoid:** Always check `git status` before cherry-picking; commit or stash local changes first
**Warning signs:** Git refuses to cherry-pick; "files would be overwritten" error

### Pitfall 6: Not Using -x Flag for Traceability
**What goes wrong:** Losing track of which upstream commits were cherry-picked, making future syncs harder
**Why it happens:** Default cherry-pick doesn't record source commit in message
**How to avoid:** Use `git cherry-pick -x <commit>` to append "(cherry picked from commit <hash>)" to message
**Warning signs:** Can't tell which features already synced; duplicate work on future sync

## Code Examples

Verified patterns from official Git documentation and fork workflow tutorials:

### Complete Upstream Setup and Feature Discovery
```bash
# Source: Git official documentation, GitHub fork workflow
# https://docs.github.com/articles/syncing-a-fork
# https://git-scm.com/docs/git-remote

# Step 1: Add GSD upstream remote
git remote add gsd-upstream https://github.com/glittercowboy/get-shit-done.git

# Step 2: Fetch all upstream branches and commits (doesn't modify local files)
git fetch gsd-upstream

# Step 3: Find fork point (common ancestor)
FORK_POINT=$(git merge-base main gsd-upstream/main)
echo "GRD forked from GSD at commit: $FORK_POINT"

# Step 4: List new upstream commits since fork
echo "New GSD commits since fork:"
git log --oneline --no-merges main..gsd-upstream/main

# Step 5: Show changed files since fork
echo "Files changed in upstream:"
git diff --name-status main...gsd-upstream/main

# Step 6: Detailed commit messages for feature identification
git log --pretty=format:"%h - %an, %ar : %s" --no-merges main..gsd-upstream/main > upstream-features.txt
```

### Gemini CLI Feature Identification
```bash
# Source: GSD repository analysis
# Based on research: v1.10.0 added Gemini CLI support (Jan 29, 2026)

# Search for Gemini-related commits
git log --grep="gemini\|Gemini" --no-merges --oneline gsd-upstream/main

# Expected relevant commits (based on WebFetch research):
# - "Gemini support to installer (#301)" - DryadeCore
# - "Gemini CLI agent loading errors (#347)" - Cristian Uibar
# - "respect attribution.commit setting (compatible opencode) (#286)"

# Show detailed changes in Gemini installer commit
git show <gemini-installer-commit-hash> --stat

# Show full diff for Gemini agent loading fixes
git show <gemini-agent-fix-commit-hash>
```

### Selective Cherry-Pick with Decision Log
```bash
# Source: Git cherry-pick documentation + fork best practices
# https://www.atlassian.com/git/tutorials/cherry-pick

# Create feature decision log
cat > .planning/phases/20-gsd-sync-setup---exploration/CHERRY_PICK_DECISIONS.md << 'EOF'
# Cherry-Pick Decisions

## To Cherry-Pick
| Feature | Commits | Reason |
|---------|---------|--------|
| Gemini CLI support | <hash1>, <hash2> | Aligns with multi-platform goal |
| Context compliance | <hash3> | Quality improvement |

## To Skip
| Feature | Reason |
|---------|--------|
| GSD-specific branding | Conflicts with GRD identity |
| Software dev workflows | GRD is research-focused |
EOF

# Cherry-pick with traceability
git cherry-pick -x <commit-hash>

# If conflicts occur, resolve and continue
git status                    # See conflicted files
# ... manually resolve conflicts ...
git add <resolved-files>
git cherry-pick --continue

# Test after each cherry-pick
npm test                      # Or appropriate test command
git commit --amend            # Add test results to commit message if needed
```

### Conflict Resolution Workflow
```bash
# Source: Git documentation + community best practices
# https://git-scm.com/docs/git-cherry-pick

# Start cherry-pick
git cherry-pick -x <commit-hash>

# If conflicts occur:
# 1. Check what's conflicted
git status

# 2. View conflict markers in files
cat <conflicted-file>

# 3. Resolve manually (edit files, remove markers)
# Choose between GRD changes (<<<<<<< HEAD) and upstream changes (>>>>>>> <commit>)

# 4. Verify no conflict markers remain
grep -r "<<<<<<< HEAD" .     # Should return nothing
grep -r "=======" .           # Should return nothing (or only legitimate content)
grep -r ">>>>>>>" .           # Should return nothing

# 5. Stage resolved files
git add <resolved-files>

# 6. Continue cherry-pick
git cherry-pick --continue

# 7. Test immediately
npm test

# Alternative: Skip if commit isn't critical
git cherry-pick --skip

# Alternative: Abort if conflicts too complex
git cherry-pick --abort
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual file copying | `git cherry-pick` with upstream remote | Always standard | Preserves commit history, author attribution |
| Two-dot syntax (`..`) | Three-dot syntax (`...`) for fork comparison | Git 1.7+ | Correctly identifies changes since common ancestor |
| Merge all upstream | Selective cherry-pick with decision matrix | Modern fork workflows | Prevents breaking changes, preserves identity |
| No commit traceability | `git cherry-pick -x` flag | Git 1.7+ | Tracks upstream source, eases future syncs |
| GitHub "Sync fork" button | Manual cherry-pick after analysis | 2024+ fork best practices | Selective adoption vs. blind sync |

**Deprecated/outdated:**
- **Downloading zip and copying files:** Loses commit history, author info, and ability to track changes
- **Git format-patch + git am:** More complex than cherry-pick for selective sync
- **Rebase onto upstream:** Rewrites GRD's commit history, breaking published branches

## Open Questions

Things that couldn't be fully resolved:

1. **GSD Gemini Implementation Details**
   - What we know: GSD v1.10.0 added Gemini CLI support via installer with TOML conversion, tool name mapping, and agent frontmatter changes
   - What's unclear: Exact commit hashes for Gemini feature (need `git fetch gsd-upstream` first); full extent of changes (may span 5-10 commits)
   - Recommendation: After adding remote, use `git log --grep="gemini" -i gsd-upstream/main` to find all commits; review each for applicability to GRD

2. **Installer Compatibility**
   - What we know: GSD installer converts .md commands to .toml for Gemini; GRD installer may have diverged
   - What's unclear: How much GRD's installer has changed since fork; whether cherry-picking GSD's Gemini code will conflict
   - Recommendation: Cherry-pick Gemini commits to feature branch first; test installer with all three runtimes (Claude/OpenCode/Gemini) before merging

3. **Agent Prompt Divergence**
   - What we know: GRD renamed agents (grd-explorer vs gsd equivalents); GSD may have updated agent prompts
   - What's unclear: Whether GSD agent improvements apply to GRD's research-focused agents
   - Recommendation: Document which GSD agents map to which GRD agents; evaluate agent prompt updates separately from Gemini feature

4. **Fork Point Precision**
   - What we know: GRD history shows "Initial commit: Get Shit Done" (1fe3fa4, Dec 14, 2025) then "feat: rebrand to GRD" (4bff035)
   - What's unclear: Whether GRD forked from GSD's initial commit or a later point
   - Recommendation: Use `git merge-base` after fetching to confirm exact fork point; may be earlier than rebrand commit

5. **Community Port vs. Upstream Feature**
   - What we know: README mentions "grd-gemini" community port by uberfuzzy; GSD added native Gemini support
   - What's unclear: Whether community port is obsoleted by GSD's native support; compatibility differences
   - Recommendation: Cherry-pick GSD's native Gemini support; evaluate community port's innovations separately

## Sources

### Primary (HIGH confidence)
- [Git Official Documentation - git-remote](https://git-scm.com/docs/git-remote) - Remote management commands
- [Git Official Documentation - git-cherry-pick](https://git-scm.com/docs/git-cherry-pick) - Cherry-pick syntax and options
- [Git Official Documentation - git-merge-base](https://git-scm.com/docs/git-merge-base) - Finding common ancestors
- [GitHub Docs - Fork a repository](https://docs.github.com/articles/fork-a-repo) - Official fork workflow
- [GitHub Docs - Syncing a fork](https://docs.github.com/articles/syncing-a-fork) - Upstream sync patterns
- [GSD Repository](https://github.com/glittercowboy/get-shit-done) - Upstream source (687 commits, 10.8k stars)
- [GSD CHANGELOG.md](https://github.com/glittercowboy/get-shit-done/blob/main/CHANGELOG.md) - Version history with Gemini CLI in v1.10.0

### Secondary (MEDIUM confidence)
- [Atlassian Git Cherry-Pick Tutorial](https://www.atlassian.com/git/tutorials/cherry-pick) - Comprehensive cherry-pick guide (WebSearch verified)
- [Atlassian Advanced Git Log](https://www.atlassian.com/git/tutorials/git-log) - Log filtering and formatting (WebSearch verified)
- [Medium - Mastering Git Cherry-Pick](https://medium.com/@314rate/mastering-git-cherry-pick-advanced-guide-with-real-world-examples-3df3d9f284f5) - Real-world examples (WebSearch verified)
- [Gemini CLI vs Claude Code - Composio Blog](https://composio.dev/blog/gemini-cli-vs-claude-code-the-better-coding-agent) - Gemini CLI capabilities and comparison (WebSearch verified with multiple sources)
- [Shipyard - Claude Code vs Gemini CLI (Jan 2026)](https://shipyard.build/blog/claude-code-vs-gemini-cli/) - Performance comparison, pricing, context windows (WebSearch verified)

### Tertiary (LOW confidence, marked for validation)
- Community blog posts about fork synchronization strategies - General best practices but not GSD-specific
- Stack Overflow discussions on cherry-pick conflicts - Useful patterns but need verification for this codebase
- GitHub Gist examples of cross-fork cherry-picking - Educational but may not match GSD/GRD structure

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Native Git commands with extensive documentation and battle-testing
- Architecture: HIGH - Fork workflow patterns are well-established in open-source community
- GSD feature identification: MEDIUM - Based on WebFetch of CHANGELOG and commits; needs `git fetch` for commit hashes
- Gemini CLI details: MEDIUM - WebFetch confirmed v1.10.0 added Gemini support; need upstream fetch for technical details
- Conflict resolution: HIGH - Standard Git cherry-pick conflict resolution is well-documented

**Research date:** 2026-02-02
**Valid until:** 30 days (2026-03-04) - GSD is actively developed; check for new features monthly
**Next sync recommendation:** After v1.3 milestone completes, review GSD changelog quarterly for new features

**Key takeaway for planner:** This is straightforward Git workflow with well-established patterns. Main complexity is decision-making (what to cherry-pick vs. skip) rather than technical execution. Focus planning on feature evaluation and testing, not Git mechanics.
