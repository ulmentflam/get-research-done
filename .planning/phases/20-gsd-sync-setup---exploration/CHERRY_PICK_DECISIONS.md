# Cherry-Pick Decision Matrix

## Summary

| Metric | Count |
|--------|-------|
| Total features evaluated | 16 |
| CHERRY-PICK (as-is) | 7 |
| CHERRY-PICK (adapt for GRD) | 3 |
| SKIP | 4 |
| EVALUATE LATER | 2 |

## Decision Criteria

Features evaluated against GRD requirements:

1. **Research alignment** - Does it support ML experimentation workflows?
2. **Branding conflict** - Does it reference "GSD" in user-facing content?
3. **Universal improvement** - Is it a bug fix or enhancement benefiting all users?
4. **Adaptation required** - Does it need GRD-specific modifications?

---

## To CHERRY-PICK (As-Is)

Universal improvements that apply directly to GRD without modification.

| Feature | Commits | Files | Rationale |
|---------|---------|-------|-----------|
| Context bar scaling fix | `87b2cd0` | `hooks/gsd-statusline.js` | Bug fix - universal improvement to UI accuracy |
| ASCII box-drawing clarification | `2347fca` | `GSD-STYLE.md` | Style guide improvement - applies to all agents |
| Attribution commit setting | `d165496` | `bin/install.js` | Installer improvement - respects user preferences |
| CONTEXT.md downstream passing | `3257139` | `commands/gsd/plan-phase.md` | Planning improvement - better context propagation |
| Squash merge option | `5ee22e6` | `commands/gsd/settings.md` | Git workflow option - universal feature |
| Unified branching strategy | `197800e` | `commands/gsd/settings.md` | Git workflow option - universal feature |
| Gemini dead code removal | `91aaa35` | `bin/install.js` | Code cleanup - removes unused code paths |

**Total: 7 commits**

---

## To CHERRY-PICK (Adapt for GRD)

Features requiring GRD branding or research-specific modifications.

| Feature | Commits | Files | Adaptation Needed | Rationale |
|---------|---------|-------|-------------------|-----------|
| Gemini installer support | `5379832` | `bin/install.js`, `package.json` | Update branding references (GSD -> GRD), adjust tool names | Core feature for v1.3 - enables Gemini CLI support |
| Gemini agent loading fixes | `5660b6f` | `bin/install.js`, `agents/*.md` | Agent files already GRD-branded; only need install.js changes | Critical for Gemini CLI compatibility |
| Changelog/README updates | `f3db981`, `3b70b10`, `d58f2b5` | `CHANGELOG.md`, `README.md` | Skip content; extract only Gemini-related entries if applicable | GRD maintains its own changelog |

**Total: 3 commits (3 unique features)**

---

## To SKIP

Features that don't apply to GRD or conflict with project identity.

| Feature | Commits | Rationale for Skipping |
|---------|---------|------------------------|
| Version bump 1.11.1 | `b5ca9a2` | GRD has its own versioning scheme |
| Version bump 1.11.0 | `d8840c4` | GRD has its own versioning scheme |
| Version bump 1.10.1 | `80d6799` | GRD has its own versioning scheme |
| Version bump 1.10.0 | `beca9fa` | GRD has its own versioning scheme |

**Total: 4 commits**

---

## To Evaluate Later

Features that may be useful but need further investigation.

| Feature | Commits | Why Deferred |
|---------|---------|--------------|
| Package.json updates | Various | Need to diff specific dependency changes vs GRD's current dependencies |
| Package-lock.json | Various | Auto-generated; will sync after package.json decisions |

**Total: 2 areas**

---

## Gemini CLI Integration Details

### Commit Dependency Chain

Apply in this order to maintain code consistency:

```
1. 5379832 - feat: add Gemini support to installer (#301)
   └── Adds core Gemini detection and installation logic

2. 91aaa35 - chore: remove dead code from Gemini PR
   └── Cleans up unnecessary code paths

3. 5660b6f - fix: Gemini CLI agent loading errors (#347)
   └── Fixes agent compatibility issues
```

### Files Requiring GRD Branding Updates

| File | Branding Needed | Details |
|------|-----------------|---------|
| `bin/install.js` | Yes | Update "get-shit-done" -> "get-research-done" in paths and messages |
| `agents/grd-*.md` | No | Already GRD-branded in our fork |
| `package.json` | Partial | May need to update tool name references |

### Key Gemini Features to Adopt

1. **Tool mapping** - `claudeToGeminiTools` mapping:
   - Read -> read_file
   - Bash -> run_shell_command
   - Write -> write_file
   - Edit -> edit_file
   - Grep -> grep_search
   - Glob -> glob_tool
   - Task -> (excluded)
   - mcp__* -> (excluded)

2. **Agent conversion** - `convertClaudeToGeminiAgent()`:
   - Convert YAML frontmatter to Gemini format
   - Remove unsupported fields (color)
   - Convert tools array format

3. **Template syntax** - Replace `${VAR}` with `$VAR` for Gemini CLI parsing

4. **HTML stripping** - Remove `<sub>` tags for terminal output

5. **Config setting** - `experimental.enableAgents: true` for Gemini CLI

---

## Phase 21 Preparation

### Cherry-Pick Order for Phase 21

Execute cherry-picks in this sequence:

```bash
# Step 1: Universal improvements (low risk)
git cherry-pick 87b2cd0  # Context bar fix
git cherry-pick 2347fca  # ASCII box-drawing
git cherry-pick 3257139  # CONTEXT.md passing
git cherry-pick 5ee22e6  # Squash merge option
git cherry-pick 197800e  # Unified branching

# Step 2: Installer improvements
git cherry-pick d165496  # Attribution setting
git cherry-pick 91aaa35  # Dead code removal

# Step 3: Gemini core (requires adaptation)
git cherry-pick --no-commit 5379832  # Gemini installer
# Manual adaptation needed here

# Step 4: Gemini fixes (after core)
git cherry-pick --no-commit 5660b6f  # Agent loading
# Manual adaptation needed here
```

### Expected Conflicts

| File | Conflict Likelihood | Reason |
|------|---------------------|--------|
| `bin/install.js` | HIGH | Heavy GRD customization in installer |
| `package.json` | MEDIUM | Different dependencies may exist |
| `commands/gsd/settings.md` | LOW | Path renamed to grd/ in GRD |
| `agents/*.md` | NONE | Different file names (grd-*.md) |

### Testing Plan After Cherry-Pick

1. **Installer tests:**
   ```bash
   node bin/install.js --help
   # Verify Gemini option appears
   ```

2. **Tool detection:**
   ```bash
   # In a test directory with Gemini CLI installed:
   node bin/install.js
   # Verify Gemini is detected
   ```

3. **Agent compatibility:**
   - Verify agents install correctly
   - Check YAML frontmatter format
   - Confirm tool names map correctly

4. **Workflow tests:**
   - Run `/grd:settings` to verify branching options
   - Run `/grd:plan-phase` to verify CONTEXT.md passing

---

## Decision Summary

### Immediate Actions (Phase 21)

1. Cherry-pick 7 universal improvements as-is
2. Adapt and apply 3 Gemini-related commits with GRD branding
3. Skip 4 version bump commits
4. Test Gemini CLI integration end-to-end

### Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| install.js conflicts | High | Use `--no-commit`, manual merge |
| Gemini detection failure | Medium | Verify environment detection logic |
| Agent format issues | Low | Agents already converted to GRD format |
| Branding leaks | Medium | Search for "gsd" strings after merge |

---
*Generated: 2026-02-02*
*Based on: UPSTREAM_FEATURES.md*
*For: Phase 21 execution*
