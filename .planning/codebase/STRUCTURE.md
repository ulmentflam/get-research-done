# Codebase Structure

**Analysis Date:** 2026-01-27

## Directory Layout

```
get-shit-done/
├── bin/                    # Executable entry points
│   └── install.js         # Installation script (npx entry)
├── commands/              # Slash command definitions
│   └── gsd/              # GSD-specific commands (one *.md per command)
├── get-shit-done/        # Resources installed to ~/.claude/ or ~/.config/opencode/
│   ├── references/       # Principle documents and guidance
│   ├── templates/        # Document templates for .planning/ artifacts
│   │   └── codebase/    # Codebase analysis templates
│   └── workflows/        # Multi-step procedures
├── agents/               # Agent prompt definitions
├── hooks/                # Git hooks (compiled to hooks/dist/)
├── scripts/              # Build scripts
├── .planning/            # Planning artifacts (created during /gsd:new-project)
├── .github/              # GitHub Actions config
├── assets/               # Documentation assets (SVG, images)
├── package.json          # Node.js project manifest
├── CHANGELOG.md          # Release history
├── README.md             # User-facing documentation
├── CONTRIBUTING.md       # Contribution guidelines
├── GSD-STYLE.md          # System design philosophy
├── MAINTAINERS.md        # Maintainer information
└── LICENSE               # MIT license
```

## Directory Purposes

**bin/**
- Purpose: Installation and bootstrap scripts
- Contains: JavaScript files executed by `npx`
- Key files: `install.js` - main installation orchestrator
- Subdirectories: None

**commands/gsd/**
- Purpose: Slash command definitions for Claude Code/OpenCode
- Contains: *.md files, one per `/gsd:` command
- Key files:
  - `new-project.md` - Initialize project with roadmap
  - `plan-phase.md` - Create plans for a phase
  - `execute-phase.md` - Run phase plans
  - `map-codebase.md` - Analyze codebase structure
  - `verify-work.md` - Verify phase completion
  - `research-phase.md` - Deep research for a phase
  - `audit-milestone.md` - Audit milestone progress
- Subdirectories: None (flat structure)
- Pattern: Each file = one command, YAML frontmatter defines behavior

**get-shit-done/references/**
- Purpose: Core principles and guidance documents
- Contains: Markdown files with system principles and patterns
- Key files: `model-profiles.md`, `git-integration.md`, `verification-patterns.md`, `tdd.md`, `planning-config.md`, `checkpoints.md`, `continuation-format.md`, `ui-brand.md`, `questioning.md`
- Subdirectories: None

**get-shit-done/templates/**
- Purpose: Document templates for creating .planning/ artifacts
- Contains: *.md template files with placeholders and instructions
- Key files:
  - `context.md` - Template for CONTEXT.md (user vision)
  - `project.md` - Template for PROJECT.md (project scope)
  - `requirements.md` - Template for REQUIREMENTS.md (feature list)
  - `discovery.md` - Template for DISCOVERY.md (domain research)
  - `research.md` - Template for RESEARCH.md (codebase analysis)
  - `phase-prompt.md` - Template for PLAN.md (executable specifications)
  - `summary.md` - Template for SUMMARY.md (execution results)
  - `UAT.md` - Template for user acceptance testing
  - `DEBUG.md` - Template for debugging sessions
  - `roadmap.md` - Template for ROADMAP.md (phase sequence)
  - `milestone.md` - Template for MILESTONE.md (tracked checkpoints)
  - `state.md` - Template for STATE.md (project state tracking)
  - `config.json` - Template for config.json (settings)
- Subdirectories:
  - `codebase/` - Templates for codebase analysis documents
    - `architecture.md` - ARCHITECTURE.md template
    - `structure.md` - STRUCTURE.md template
    - `stack.md` - STACK.md template
    - `integrations.md` - INTEGRATIONS.md template
    - `conventions.md` - CONVENTIONS.md template
    - `testing.md` - TESTING.md template
    - `concerns.md` - CONCERNS.md template

**get-shit-done/workflows/**
- Purpose: Reusable multi-step procedures called by orchestrators
- Contains: *.md workflow definitions
- Key files:
  - `execute-plan.md` - Execute all tasks in a plan
  - `execute-phase.md` - Execute all plans in a phase (wave-based)
  - `verify-phase.md` - Run verification criteria for phase
  - `verify-work.md` - Full verification workflow
  - `research-phase.md` - Research domain for a phase
  - `discovery-phase.md` - Discover requirements
  - `discuss-phase.md` - Discuss and refine phase details
  - `complete-milestone.md` - Mark milestone complete
  - `diagnose-issues.md` - Debug execution issues
  - `list-phase-assumptions.md` - Extract and list assumptions
  - `map-codebase.md` - Orchestrate parallel codebase mapping agents
  - `transition.md` - Transition workflow between phases
  - `resume-project.md` - Resume interrupted project
- Subdirectories: None

**agents/**
- Purpose: Agent prompt definitions (specialized execution engines)
- Contains: *.md files defining agent role, tools, and instructions
- Key files:
  - `gsd-codebase-mapper.md` - Maps codebase (4 focus areas: tech, arch, quality, concerns)
  - `gsd-planner.md` - Creates detailed execution plans
  - `gsd-executor.md` - Executes plans atomically with commits
  - `gsd-verifier.md` - Verifies phase completion
  - `gsd-plan-checker.md` - Validates plan quality
  - `gsd-debugger.md` - Handles execution failures
  - `gsd-phase-researcher.md` - Researches phase requirements
  - `gsd-project-researcher.md` - Analyzes existing projects
  - `gsd-integration-checker.md` - Validates external integrations
  - `gsd-roadmapper.md` - Creates project roadmaps
  - `gsd-research-synthesizer.md` - Synthesizes research findings
- Subdirectories: None
- Pattern: YAML frontmatter (name, description, tools, color) + execution instructions

**hooks/**
- Purpose: Git hooks for workflow automation
- Contains: Hook definitions (pre-commit, post-commit, etc.)
- Subdirectories: `dist/` - Compiled hooks (generated by build)
- Usage: Installed to `.git/hooks/` by install.js

**scripts/**
- Purpose: Build and development scripts
- Contains: Node.js and shell scripts
- Key files: `build-hooks.js` - Compiles hooks to dist/
- Subdirectories: None

**.planning/**
- Purpose: Project planning artifacts (created per-project)
- Contains: Project state, roadmap, phases, codebase analysis
- Key files:
  - `STATE.md` - Current project status and decisions
  - `config.json` - GSD settings (model_profile, commit_docs, etc.)
  - `PROJECT.md` - Project scope and overview
  - `ROADMAP.md` - Phase sequence and milestones
  - `RESEARCH.md` - Project domain analysis
  - `codebase/` - Codebase analysis documents (created by map-codebase)
    - `STACK.md` - Technology stack
    - `INTEGRATIONS.md` - External services
    - `ARCHITECTURE.md` - Code organization
    - `STRUCTURE.md` - Directory layout
    - `CONVENTIONS.md` - Coding patterns
    - `TESTING.md` - Test patterns
    - `CONCERNS.md` - Technical debt
  - `phases/` - Per-phase execution
    - `{PHASE}-{NAME}/` - Phase directory
      - `PLAN.md` - Executable plan
      - `RESEARCH.md` - Phase research
      - `SUMMARY.md` - Execution results
      - `VERIFICATION.md` - Verification report
- Subdirectories: `codebase/`, `phases/`
- Notes: Typically in .gitignore; use config.json to change

## Key File Locations

**Entry Points:**
- `bin/install.js` - Installation entry (runs `npx get-shit-done-cc`)
- `commands/gsd/*.md` - Slash command entries (run `/gsd:command` in Claude Code/OpenCode)

**Configuration:**
- `package.json` - Project metadata, bin entry, dependencies
- `.gitignore` - Excluded files from git
- `.github/workflows/` - GitHub Actions (publish workflow)
- `hooks/` - Git hooks for automation

**Resources:**
- `get-shit-done/references/` - Guidance and principles
- `get-shit-done/templates/` - Document structure templates
- `get-shit-done/workflows/` - Reusable procedures
- `agents/` - Agent prompt definitions

**Documentation:**
- `README.md` - Installation, usage, features
- `GSD-STYLE.md` - System philosophy and design principles
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines

## Naming Conventions

**Files:**
- kebab-case.md - Markdown documents (commands, workflows, agents, references)
- kebab-case.js - JavaScript source files
- UPPERCASE.md - Important project documents (README, CHANGELOG, GSD-STYLE)
- *.json - Configuration and package files

**Directories:**
- kebab-case - All directories (bin, commands, get-shit-done)
- Plural for collections - commands/, references/, templates/, workflows/, agents/
- Single hyphen separators (not underscores)

**Special Patterns:**
- `{command-name}.md` - Slash command definition (e.g., `new-project.md`)
- `gsd-{agent-name}.md` - Agent definition (prefix "gsd-")
- `{workflow-name}.md` - Workflow definition (no special prefix)
- `.planning/{filename}.md` - Artifact templates match this convention (STATE.md, PROJECT.md)

## Where to Add New Code

**New Slash Command:**
- Primary code: `commands/gsd/{command-name}.md`
- Documentation: Include in `README.md` commands section
- Testing: Add test case if test framework added
- Pattern: YAML frontmatter (name, description, arguments, allowed-tools, agent) + execution steps

**New Agent (Specialized Executor):**
- Primary code: `agents/gsd-{agent-name}.md`
- Documentation: Include in `README.md` or agent overview doc
- Pattern: YAML frontmatter (name, description, tools, color) + detailed role and execution instructions
- Reference: Likely called from a command or workflow

**New Template (Document Structure):**
- Implementation: `get-shit-done/templates/{name}.md`
- Subdirectory: Use `codebase/` subdir for codebase analysis templates
- Documentation: Template includes usage guidelines
- Pattern: Markdown with placeholders like `[YYYY-MM-DD]`, `[Placeholder text]`, guidelines in comments

**New Workflow (Reusable Procedure):**
- Implementation: `get-shit-done/workflows/{name}.md`
- Usage: Reference from command with `@~/.claude/get-shit-done/workflows/{name}.md` or `@~/.config/opencode/get-shit-done/workflows/{name}.md`
- Pattern: Markdown with numbered steps, conditionals, bash commands where needed

**New Reference (Principle Document):**
- Implementation: `get-shit-done/references/{name}.md`
- Usage: Reference from agents/commands as context (`@~/.claude/get-shit-done/references/{name}.md`)
- Pattern: Markdown explaining a concept, pattern, or principle

**Installation Hook:**
- Implementation: `hooks/{hook-name}` (source)
- Compilation: `scripts/build-hooks.js` compiles to `hooks/dist/{hook-name}`
- Usage: Installed to `.git/hooks/` by install.js

## Special Directories

**get-shit-done/**
- Purpose: Resources to install to user's Claude Code/OpenCode config directory
- Source: This directory is the source of truth
- Installation: Copied by `bin/install.js` to `~/.claude/get-shit-done/` or `~/.config/opencode/get-shit-done/`
- Committed: Yes (source code)
- Update: Changes here propagate on next `npx get-shit-done-cc@latest`

**commands/gsd/**
- Purpose: Slash commands to install
- Source: Copied by bin/install.js
- Installation destination: `~/.claude/commands/gsd/` or `~/.config/opencode/commands/gsd/`
- Committed: Yes (source code)
- Update: Changes propagate on next npm update

**hooks/dist/**
- Purpose: Compiled git hooks (built output)
- Source: Generated by `scripts/build-hooks.js`
- Committed: Yes (built artifacts)
- Regenerate: Run `npm run build:hooks` after modifying hooks/ files

**.planning/** (in user's project)
- Purpose: Project-specific planning artifacts
- Created: During `/gsd:new-project` initialization
- Committed: Configurable via `config.json` (default: true, unless in .gitignore)
- Structure: Mirrors GSD's template structure
- Updates: Modified by agent executions (plans, summaries, verification)

---

*Structure analysis: 2026-01-27*
*Update when directory structure changes*
