# Upstream GSD Features Since Fork

## Fork Information

| Property | Value |
|----------|-------|
| Fork point commit | `339e9112990e024fea746d244765ada8a044a848` |
| Fork point message | `chore: remove GitHub Actions release workflow` |
| Total commits since fork | 16 |
| Date range | 2026-01-24 to 2026-02-02 |
| Upstream remote | `gsd-upstream` -> `https://github.com/glittercowboy/get-shit-done.git` |

## Commits Since Fork

| Hash | Author | Date | Subject |
|------|--------|------|---------|
| `2347fca` | Szymon Gwozdz | 2026-02-02 | fix: clarify ASCII box-drawing vs text content with diacritics (#289) |
| `d165496` | superresistant | 2026-02-02 | feat(install): respect attribution.commit setting (compatible opencode) (#286) |
| `b5ca9a2` | Lex Christopherson | 2026-01-31 | 1.11.1 |
| `d8840c4` | Lex Christopherson | 2026-01-31 | 1.11.0 |
| `f3db981` | Lex Christopherson | 2026-01-31 | docs: update changelog and README for v1.11.0 |
| `3257139` | Lex Christopherson | 2026-01-31 | fix(plan-phase): pass CONTEXT.md to all downstream agents |
| `5ee22e6` | Lex Christopherson | 2026-01-30 | feat(git): add squash merge option for branching strategies |
| `80d6799` | Lex Christopherson | 2026-01-30 | 1.10.1 |
| `3b70b10` | Lex Christopherson | 2026-01-30 | docs: update changelog for v1.10.1 |
| `5660b6f` | Cristian Uibar | 2026-01-30 | fix: Gemini CLI agent loading errors (#347) |
| `beca9fa` | Lex Christopherson | 2026-01-29 | 1.10.0 |
| `d58f2b5` | Lex Christopherson | 2026-01-29 | docs: update README and changelog for v1.9.14 |
| `91aaa35` | Lex Christopherson | 2026-01-29 | chore: remove dead code from Gemini PR |
| `5379832` | Dryade AI | 2026-01-29 | feat: add Gemini support to installer (#301) |
| `87b2cd0` | David Novak | 2026-01-29 | fix: scale context bar to show 100% at actual 80% limit |
| `197800e` | Dave | 2026-01-24 | feat(git): add unified branching strategy option |

## Feature Categories

### Gemini CLI Support (3 commits - HIGH PRIORITY)

Primary feature for GRD v1.3 integration.

| Hash | Description | Files Modified |
|------|-------------|----------------|
| `5379832` | **feat: add Gemini support to installer (#301)** - Core Gemini CLI integration | `bin/install.js`, `package.json` |
| `5660b6f` | **fix: Gemini CLI agent loading errors (#347)** - Agent frontmatter conversion, tool mapping, template syntax fixes | `bin/install.js`, `agents/gsd-phase-researcher.md`, `agents/gsd-plan-checker.md`, `agents/gsd-planner.md`, `agents/gsd-verifier.md` |
| `91aaa35` | **chore: remove dead code from Gemini PR** - Cleanup of unused code paths | `bin/install.js` |

**Dependency order:** `5379832` -> `91aaa35` -> `5660b6f`

**Key capabilities added:**
- Claude-to-Gemini tool mapping (Read -> read_file, Bash -> run_shell_command, etc.)
- Agent YAML frontmatter conversion for Gemini compatibility
- Template syntax conversion (${VAR} -> $VAR)
- HTML tag stripping for terminal output
- `experimental.enableAgents` configuration for Gemini CLI

### Git/Workflow Enhancements (2 commits)

| Hash | Description | Files Modified |
|------|-------------|----------------|
| `5ee22e6` | **feat(git): add squash merge option for branching strategies** | `commands/gsd/settings.md` |
| `197800e` | **feat(git): add unified branching strategy option** | `commands/gsd/settings.md` |

### Planning/Phase Improvements (1 commit)

| Hash | Description | Files Modified |
|------|-------------|----------------|
| `3257139` | **fix(plan-phase): pass CONTEXT.md to all downstream agents** | `commands/gsd/plan-phase.md` |

### Installer Improvements (1 commit)

| Hash | Description | Files Modified |
|------|-------------|----------------|
| `d165496` | **feat(install): respect attribution.commit setting (compatible opencode)** | `bin/install.js` |

### Bug Fixes (2 commits)

| Hash | Description | Files Modified |
|------|-------------|----------------|
| `2347fca` | **fix: clarify ASCII box-drawing vs text content with diacritics (#289)** | `GSD-STYLE.md` |
| `87b2cd0` | **fix: scale context bar to show 100% at actual 80% limit** | `hooks/gsd-statusline.js` |

### Documentation Updates (3 commits)

| Hash | Description | Files Modified |
|------|-------------|----------------|
| `f3db981` | docs: update changelog and README for v1.11.0 | `CHANGELOG.md`, `README.md` |
| `3b70b10` | docs: update changelog for v1.10.1 | `CHANGELOG.md` |
| `d58f2b5` | docs: update README and changelog for v1.9.14 | `CHANGELOG.md`, `README.md` |

### Version Bumps (3 commits)

| Hash | Version | Date |
|------|---------|------|
| `b5ca9a2` | 1.11.1 | 2026-01-31 |
| `d8840c4` | 1.11.0 | 2026-01-31 |
| `80d6799` | 1.10.1 | 2026-01-30 |
| `beca9fa` | 1.10.0 | 2026-01-29 |

## Files Changed Since Fork

| Status | File |
|--------|------|
| M | CHANGELOG.md |
| M | GSD-STYLE.md |
| M | README.md |
| M | agents/gsd-phase-researcher.md |
| M | agents/gsd-plan-checker.md |
| M | agents/gsd-planner.md |
| M | agents/gsd-verifier.md |
| M | bin/install.js |
| M | commands/gsd/add-todo.md |
| M | commands/gsd/plan-phase.md |
| M | commands/gsd/settings.md |
| M | get-shit-done/references/planning-config.md |
| M | get-shit-done/templates/codebase/structure.md |
| M | get-shit-done/templates/research-project/ARCHITECTURE.md |
| M | get-shit-done/workflows/complete-milestone.md |
| M | get-shit-done/workflows/execute-phase.md |
| M | hooks/gsd-statusline.js |
| M | package-lock.json |
| M | package.json |

**Total files modified:** 19

## Gemini-Related Commits (All History)

Broader search across entire upstream history (not just since fork):

| Hash | Subject |
|------|---------|
| `d165496` | feat(install): respect attribution.commit setting (compatible opencode) (#286) |
| `5660b6f` | fix: Gemini CLI agent loading errors (#347) |
| `d58f2b5` | docs: update README and changelog for v1.9.14 |
| `91aaa35` | chore: remove dead code from Gemini PR |
| `5379832` | feat: add Gemini support to installer (#301) |
| `7e9b8de` | docs: add community ports section to README |

## Summary Statistics

| Category | Count |
|----------|-------|
| Total commits | 16 |
| Feature commits | 4 |
| Fix commits | 4 |
| Documentation commits | 3 |
| Version bump commits | 4 |
| Chore commits | 1 |
| Gemini-specific commits | 3 |

---
*Generated: 2026-02-02*
*Fork point: `339e911` (2026-01-24)*
*Latest upstream: `2347fca` (2026-02-02)*
