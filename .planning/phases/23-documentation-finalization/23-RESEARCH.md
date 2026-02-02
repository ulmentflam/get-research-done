# Phase 23: Documentation & Finalization - Research

**Researched:** 2026-02-02
**Domain:** Technical documentation for CLI tools
**Confidence:** HIGH

## Summary

Technical documentation for CLI tools in 2026 follows well-established patterns: README as primary entry point with badges/quickstart/workflow, help.md as comprehensive command reference with examples, CHANGELOG.md following Keep a Changelog format with Semantic Versioning. GRD's v1.3 adds Gemini CLI support requiring documentation of multi-runtime setup, model selection guidance, and visual branding updates.

The standard approach is README-first (getting started, visual appeal), comprehensive help reference (every command with examples), and structured changelog (grouped by type, reverse chronological). Badge selection should be minimal and meaningful (npm version, license, build status) using shields.io for consistency.

**Primary recommendation:** Follow Keep a Changelog format strictly (Added/Changed/Fixed/etc. categories), use shields.io for badge consistency, structure help.md by workflow phases (setup → exploration → completion), and provide copy-paste examples for every command.

## Standard Stack

The established patterns for CLI tool documentation:

### Core
| Component | Standard | Purpose | Why Standard |
|-----------|----------|---------|--------------|
| README.md | Markdown with badges | Primary entry point, quickstart | Universal GitHub standard, rendered automatically |
| CHANGELOG.md | Keep a Changelog format | Version history tracking | Industry standard since 2015, Semantic Versioning integration |
| help.md | Markdown command reference | Comprehensive usage guide | Searchable text format, version-controllable |
| Badges | shields.io | Visual status indicators | Consistent styling, dynamic updates, 1.6B+ images/month |

### Supporting
| Component | Standard | Purpose | When to Use |
|-----------|----------|---------|-------------|
| LICENSE | MIT/Apache/etc. | Legal clarity | Always (npm requirement) |
| Examples | Inline code blocks | Copy-paste usage | Every command (developer-first) |
| Visual assets | SVG/PNG | Branding, terminal previews | Hero images, installation demos |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Keep a Changelog | Custom format | Lose tooling compatibility, automation support |
| shields.io | Custom badges | Inconsistent styling, manual updates required |
| Markdown docs | Wiki/external site | Context split, harder to version control |

**Installation:**
```bash
# No dependencies - Markdown is native to npm/GitHub
# Badges via shields.io (URL-based, no installation)
```

## Architecture Patterns

### Recommended Documentation Structure
```
project/
├── README.md              # Entry point: badges, quickstart, workflow overview
├── CHANGELOG.md           # Keep a Changelog format, Semantic Versioning
├── commands/grd/help.md   # Comprehensive reference (embedded in CLI)
├── LICENSE                # Legal (required for npm)
└── assets/
    ├── logo.svg           # Branding
    └── terminal.svg       # Installation demo
```

### Pattern 1: README Hero Section
**What:** Logo, badges, one-line description, quickstart command above the fold
**When to use:** Every CLI tool README - first 3 seconds determine engagement
**Example:**
```markdown
# PROJECT NAME

**One-line value proposition**

[![npm version](https://img.shields.io/npm/v/package-name?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/package-name)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

```bash
npx package-name
```

![Terminal Preview](assets/terminal.svg)
```
**Source:** [River Editor GitHub README Template](https://rivereditor.com/blogs/write-perfect-readme-github-repo)

### Pattern 2: Keep a Changelog Format
**What:** Structured changelog with [Added], [Changed], [Fixed], [Deprecated], [Removed], [Security] categories
**When to use:** Every release - enables automation, tooling integration
**Example:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2026-02-02

### Added
- Gemini CLI support with TOML agent conversion
- Multi-runtime installer (Claude Code, OpenCode, Gemini)

### Changed
- Visual branding updated to GRD identity (teal color palette)

### Fixed
- Context bar scaling to show 100% at 80% token limit

[Unreleased]: https://github.com/user/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/user/repo/releases/tag/v1.3.0
```
**Source:** [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), [Common Changelog](https://common-changelog.org/)

### Pattern 3: Command Reference with Examples
**What:** Every command gets: name, description, usage syntax, 1-2 practical examples, "See also" links
**When to use:** help.md comprehensive reference - developers need copy-paste examples
**Example:**
```markdown
### `/grd:explore [path]`

Data reconnaissance and profiling.

**Usage:**
```
/grd:explore ./data/train.csv
```

**What it does:**
- Profiles distributions, class balance, outliers
- Detects missing data patterns (MCAR/MAR/MNAR)
- Identifies potential data leakage risks

**Examples:**

1. Explore single dataset:
   ```
   /grd:explore ./data/train.csv
   ```

2. Explore directory:
   ```
   /grd:explore ./data/
   ```

**See also:** `/grd:architect` (next step), `/grd:insights` (plain English summaries)
```
**Source:** [CLI Guidelines](https://clig.dev/), [Google Dev Docs](https://developers.google.com/style/code-syntax), [BetterCLI Help Pages](https://bettercli.org/design/cli-help-page/)

### Pattern 4: Workflow-Grouped Commands
**What:** Group commands by user journey phase, not alphabetically
**When to use:** README command table - users think in workflows, not alphabet
**Example:**
```markdown
## Commands

### Research Loop (Core Workflow)
| Command | What it does |
|---------|--------------|
| `/grd:explore` | Data reconnaissance |
| `/grd:architect` | Hypothesis synthesis |
| `/grd:research` | Experiment implementation |

### Project Setup
| Command | What it does |
|---------|--------------|
| `/grd:new-project` | Initialize project |
```
**Source:** [CLI Structure & Syntax](https://dev.to/paulasantamaria/command-line-interfaces-structure-syntax-2533)

### Anti-Patterns to Avoid
- **Badge overload:** More than 5 badges dilutes impact - select meaningful metrics only ([InfiniteJS Shields.io Mistakes](https://infinitejs.com/posts/common-mistakes-shields-io-badges/))
- **Stale badges:** Static badges become misleading - use shields.io dynamic badges ([DEV Community Badges](https://dev.to/cicirello/badges-tldr-for-your-repositorys-readme-3oo3))
- **Commands without examples:** Syntax-only docs require mental translation - provide copy-paste examples ([Developer-First CLI Docs](https://www.infrasity.com/blog/cli-docs-checklist))
- **Custom changelog format:** Breaks automation, tooling integration - use Keep a Changelog ([Keep a Changelog](https://keepachangelog.com/en/1.1.0/))

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Badge generation | Custom badge SVGs | [shields.io](https://shields.io/) | 1.6B images/month, dynamic updates, 1000+ badge types |
| Changelog format | Custom versioning | [Keep a Changelog](https://keepachangelog.com/) | Tooling integration (semantic-release), automation support |
| Command syntax docs | Plain text format | Markdown with code blocks | Syntax highlighting, copy button, GitHub rendering |
| Version numbering | Custom scheme | [Semantic Versioning](https://semver.org/) | Industry standard, tooling support (npm, semver) |

**Key insight:** Documentation infrastructure is commoditized - competing on format wastes energy. Focus on content quality, not format innovation.

## Common Pitfalls

### Pitfall 1: Incomplete v1.3 Feature Coverage
**What goes wrong:** New features (Gemini CLI, visual branding) exist in code but not in docs, users don't know they exist
**Why it happens:** Documentation lags implementation - features ship, docs update forgotten
**How to avoid:**
- Cross-reference Phase 21 SUMMARY.md (Gemini features added)
- Cross-reference Phase 22 SUMMARY.md (branding changes)
- Check git log for "feat:" commits since v1.2.0
**Warning signs:** README shows old logo, help.md missing Gemini installation flags

### Pitfall 2: Vague Model Selection Guidance
**What goes wrong:** Users ask "When should I use Gemini vs Claude?" - no clear answer in docs
**Why it happens:** Multi-LLM support is new domain - guidance isn't obvious
**How to avoid:**
- Document model strengths clearly (Claude: reasoning depth, coding; Gemini: multimodal, cost, context)
- Link to official setup docs (Gemini API key from Google AI Studio)
- Provide concrete examples: "Use Claude for complex debugging, Gemini for visual data analysis"
**Warning signs:** Generic "supports both" without selection criteria

### Pitfall 3: Changelog Without Milestone Grouping
**What goes wrong:** v1.3 entries scattered or missing historical context (v1.0, v1.1, v1.2)
**Why it happens:** CHANGELOG.md was minimal (only v1.2.0 entry), lacks milestone summaries
**How to avoid:**
- Include full version history (v1.0, v1.1, v1.2, v1.3)
- Add milestone summary for each version (key accomplishments)
- Use Keep a Changelog categories (Added/Changed/Fixed) consistently
**Warning signs:** Only current version documented, no historical context

### Pitfall 4: Badge URL Hardcoding
**What goes wrong:** Badges break when repo URL changes or package name updates
**Why it happens:** Copy-paste from examples without parameterization
**How to avoid:**
- Use shields.io dynamic badges with correct package name (get-research-done)
- Verify badge URLs resolve before committing
- Test badge display on GitHub (not just locally)
**Warning signs:** 404 badge images, incorrect version numbers

### Pitfall 5: Help.md Out of Sync with Commands
**What goes wrong:** Commands exist in commands/grd/ but not documented in help.md
**Why it happens:** help.md is manually curated - new commands added without doc update
**How to avoid:**
- Cross-reference commands/grd/ directory listing with help.md sections
- Ensure all 30 commands have entries
- Check for deprecated commands still documented
**Warning signs:** Command count mismatch, "command not found" for documented commands

## Code Examples

Verified patterns from official sources:

### Shields.io Badge URLs
```markdown
<!-- npm version badge (dynamic) -->
[![npm version](https://img.shields.io/npm/v/get-research-done?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/get-research-done)

<!-- npm downloads badge (dynamic) -->
[![npm downloads](https://img.shields.io/npm/dm/get-research-done?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/get-research-done)

<!-- GitHub stars badge (dynamic) -->
[![GitHub stars](https://img.shields.io/github/stars/ulmentflam/get-research-done?style=for-the-badge&logo=github&color=181717)](https://github.com/ulmentflam/get-research-done)

<!-- License badge (static) -->
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

<!-- Build status badge (if CI exists) -->
[![Build Status](https://img.shields.io/github/actions/workflow/status/ulmentflam/get-research-done/test.yml?style=for-the-badge)](https://github.com/ulmentflam/get-research-done/actions)
```
**Source:** [Shields.io](https://shields.io/), [NPM Version Badge](https://shields.io/badges/npm-version)

### Keep a Changelog Header
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes

[Unreleased]: https://github.com/user/repo/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/user/repo/releases/tag/vX.Y.Z
```
**Source:** [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

### Command Documentation Template
```markdown
**`/command:name <required> [optional]`**
Brief one-line description.

Detailed explanation of what the command does (2-3 sentences).

Key features:
- Bullet point 1
- Bullet point 2

Usage: `/command:name arg`

**Examples:**

1. Basic usage:
   ```
   /command:name simple-arg
   ```

2. Advanced usage:
   ```
   /command:name complex-arg --flag
   ```

**See also:** Related commands
```
**Source:** [CLI Guidelines](https://clig.dev/), [Google Dev Docs](https://developers.google.com/style/code-syntax)

### Gemini API Key Setup Documentation
```markdown
### Gemini CLI Support

GRD v1.3 adds support for Google's Gemini CLI alongside Claude Code and OpenCode.

**Installation:**
```bash
# Install to Gemini CLI
npx get-research-done --gemini --global

# Install to all runtimes
npx get-research-done --all --global
```

**Setup:**
1. Get API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Set environment variable:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
3. Verify: `gemini --version`

**When to use Gemini vs Claude:**
- **Claude:** Best for complex reasoning, coding tasks, detailed analysis
- **Gemini:** Best for multimodal tasks (images), cost efficiency, large context windows

See [Gemini CLI Authentication](https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html) for advanced setup.
```
**Source:** [Gemini CLI Docs](https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html), [Using Gemini API Keys](https://ai.google.dev/gemini-api/docs/api-key)

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Static badges | Dynamic shields.io | ~2018 | Auto-updating metrics, no manual edits |
| Custom changelogs | Keep a Changelog | 2015 (formalized) | Tooling integration (semantic-release, automation) |
| Alphabetical commands | Workflow-grouped | ~2020 (CLI Guidelines) | User-centric organization, faster discovery |
| Text-only READMEs | Visual hero sections | ~2021 | 4x more stars (River Editor analysis) |
| Single LLM docs | Multi-LLM selection guide | 2026 (multi-model era) | Users need model choice criteria |

**Deprecated/outdated:**
- **Travis CI badges:** GitHub Actions now standard (Travis free tier sunset 2020)
- **Manual version updates in docs:** Shields.io auto-fetches from npm
- **Markdown only:** Terminal SVG previews now expected for CLI tools

## Open Questions

Things that couldn't be fully resolved:

1. **Build status badge inclusion**
   - What we know: GRD has `npm test` with 23 tests, no CI workflow detected
   - What's unclear: Whether to add GitHub Actions CI or omit build badge
   - Recommendation: Omit build badge unless CI workflow exists (avoid misleading users)

2. **Version history depth in CHANGELOG.md**
   - What we know: Current CHANGELOG.md has only v1.2.0 entry
   - What's unclear: How detailed should v1.0, v1.1 historical entries be
   - Recommendation: Brief milestone summaries for v1.0-v1.2 (3-5 bullets each), detailed for v1.3

3. **Gemini model recommendations**
   - What we know: General Claude vs Gemini tradeoffs (reasoning vs multimodal, cost)
   - What's unclear: GRD-specific use cases where one is clearly better
   - Recommendation: Generic guidance (Claude for analysis, Gemini for cost/multimodal), let users experiment

## Sources

### Primary (HIGH confidence)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) - Changelog format standard
- [Semantic Versioning](https://semver.org/) - Version numbering spec
- [Shields.io](https://shields.io/) - Badge generation service
- [CLI Guidelines (clig.dev)](https://clig.dev/) - CLI design patterns
- [Google Dev Docs: Command-Line Syntax](https://developers.google.com/style/code-syntax) - Documentation style
- [Gemini CLI Authentication](https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html) - Official setup docs
- [Using Gemini API Keys](https://ai.google.dev/gemini-api/docs/api-key) - API key setup

### Secondary (MEDIUM confidence)
- [River Editor: GitHub README Template (2026)](https://rivereditor.com/blogs/write-perfect-readme-github-repo) - README best practices (verified with multiple sources)
- [BetterCLI.org: Help Pages](https://bettercli.org/design/cli-help-page/) - Help documentation patterns
- [Common Changelog](https://common-changelog.org/) - Alternative changelog spec (Keep a Changelog superset)
- [Teneo.ai: Best LLM in 2026 Comparison](https://www.teneo.ai/blog/the-best-llm-in-2026-gemini-3-vs-claude-4-5-vs-gpt-5-1) - Model selection guidance (verified with DataCamp, Ideas2It)

### Tertiary (LOW confidence)
- [InfiniteJS: Common Shields.io Mistakes](https://infinitejs.com/posts/common-mistakes-shields-io-badges/) - Badge anti-patterns (single source, general advice)
- [DataCamp: Claude vs Gemini](https://www.datacamp.com/blog/claude-vs-gemini) - Model comparison (marketing-focused)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Keep a Changelog, shields.io, Markdown are industry standards with official docs
- Architecture: HIGH - CLI Guidelines, Google Dev Docs, BetterCLI provide authoritative patterns
- Pitfalls: MEDIUM - Derived from general best practices, not GRD-specific testing
- Gemini guidance: MEDIUM - Model comparisons from recent sources (2026), but evolving rapidly

**Research date:** 2026-02-02
**Valid until:** 2026-04-02 (60 days - stable domain, but LLM landscape evolving)

---

## GRD-Specific Context

### What's New in v1.3 (Per Phase 21/22 SUMMARY.md)

**Phase 21: Gemini CLI Integration**
- Gemini CLI detection in installer
- TOML agent conversion for Gemini format
- Multi-runtime flags: --claude, --opencode, --gemini, --all
- Universal improvements: context bar scaling, branching strategies, attribution settings

**Phase 22: Branding Updates**
- GRD logo with teal color palette (#4FB3D4)
- Terminal preview SVG updated to GRD branding
- Logo generated as PNG (social media, package listings)

### Commands to Document (30 total)
**Research Loop:** explore, architect, research, evaluate, graduate
**Project Setup:** new-project, map-codebase
**Study Management:** new-study, complete-study, audit-study, plan-study-gaps
**Experiment Planning:** scope-experiment, literature-review, list-experiment-assumptions, design-experiment
**Execution:** run-experiment, validate-results
**Roadmap Management:** add-experiment, insert-experiment, remove-experiment
**Session:** pause-work, resume-work
**Quick Mode:** quick
**Todo:** add-todo, check-todos
**Utility:** help, update, settings, set-profile, debug, insights

### Current State (from existing docs)
- README.md: Has hero section, badges, workflow overview, commands table - needs v1.3 features
- help.md: Comprehensive command reference (30 commands) - needs Gemini flags, no structural changes
- CHANGELOG.md: Has v1.2.0 entry only - needs v1.0, v1.1, v1.3 additions

### User Decisions from CONTEXT.md (Locked Choices)
- README: Getting started focused, logo as hero, v1.3 in "What's New" section
- help.md: Full examples, organized by research phase, cross-references
- Gemini: Highlight as v1.3 feature, link to Google docs, show both models
- CHANGELOG: Separate file, milestone summaries, full history (v1.0-v1.3), self-contained
