# Architecture

**Analysis Date:** 2026-01-27

## Pattern Overview

**Overall:** Orchestrated Multi-Agent System for Spec-Driven Development

**Key Characteristics:**
- Context engineering layer abstracting complexity from users
- Master-subordinate agent architecture with specialized roles
- File-based state management across phases and iterations
- Markdown-first specification and workflow format
- Wave-based parallel task execution with dependency management

## Layers

**CLI/Orchestration Layer:**
- Purpose: User-facing command interface and workflow orchestration
- Contains: Slash command definitions, orchestration logic, agent spawning
- Location: `bin/install.js`, `commands/gsd/`
- Depends on: Subagents, templates, workflows, state management
- Used by: Claude Code/OpenCode runtime through slash commands

**Agent Layer:**
- Purpose: Specialized execution engines for distinct system phases
- Contains: Agent prompt systems defining role, tools, validation criteria
- Location: `agents/`
- Agents: gsd-codebase-mapper, gsd-planner, gsd-executor, gsd-verifier, gsd-debugger, gsd-integration-checker, gsd-phase-researcher, gsd-project-researcher, gsd-plan-checker, gsd-research-synthesizer, gsd-roadmapper
- Depends on: Tools (Read, Write, Edit, Bash, Glob, Grep, WebFetch), state files
- Used by: Orchestrators to execute specialized tasks

**Resource Layer:**
- Purpose: Reusable knowledge, procedures, and document templates
- Contains: References (principles), templates (document structures), workflows (step-by-step procedures)
- Location: `get-shit-done/references/`, `get-shit-done/templates/`, `get-shit-done/workflows/`
- Depends on: None (knowledge base)
- Used by: Agents and orchestrators during execution

**State Management Layer:**
- Purpose: Track project progress, decisions, and accumulated context
- Contains: Project state files, configuration, codebase analysis documents
- Location: `.planning/` (user's project directory)
- Files: STATE.md, config.json, RESEARCH.md, PLAN.md, SUMMARY.md, codebase/STACK.md|ARCHITECTURE.md|CONVENTIONS.md|TESTING.md|INTEGRATIONS.md|STRUCTURE.md|CONCERNS.md
- Depends on: File system only
- Used by: All orchestrators to track and resume work

**Installation/Bootstrap Layer:**
- Purpose: Deliver system to user's Claude Code/OpenCode config directory
- Contains: Installation script with platform detection and config management
- Location: `bin/install.js`
- Depends on: File system, environment variables
- Used by: Users during `npx get-shit-done-cc` setup

## Data Flow

**Project Initialization Flow:**

1. User runs `/gsd:new-project` command
2. Orchestrator loads or creates `.planning/` directory structure
3. Orchestrator spawns gsd-project-researcher agent to understand existing codebase
4. Agent reads codebase, writes RESEARCH.md
5. Orchestrator spawns gsd-planner to create roadmap
6. gsd-planner reads research and project requirements, writes ROADMAP.md
7. gsd-planner spawns gsd-plan-checker to verify roadmap quality
8. State locked in .planning/STATE.md, .planning/config.json

**Phase Planning Flow:**

1. User runs `/gsd:plan-phase [number]` for next phase
2. Orchestrator validates phase exists in roadmap
3. If no research: Orchestrator spawns gsd-phase-researcher
   - Agent reads codebase, external docs, writes RESEARCH.md
4. Orchestrator spawns gsd-planner
   - Agent reads RESEARCH.md and phase requirements
   - Agent generates PLAN.md files for each task
5. Orchestrator spawns gsd-plan-checker
   - Agent reads all PLAN.md files, verifies completeness
   - Returns VERIFICATION.md with gaps
6. If gaps found: Loop back to planner with gap feedback
7. Plans locked in .planning/phases/{PHASE}-{NAME}/

**Phase Execution Flow:**

1. User runs `/gsd:execute-phase [number]`
2. Orchestrator loads STATE.md, validates phase exists
3. Orchestrator discovers plans in phase directory
4. Orchestrator analyzes plan dependencies, groups into waves
5. For each wave:
   - Orchestrator spawns gsd-executor agents (parallel, one per plan)
   - Agents load plan, execute tasks sequentially
   - Agents create atomic commits per task
   - Agents write SUMMARY.md upon completion
   - Orchestrator waits for all agents in wave to complete
6. After all plans complete, orchestrator runs gsd-verifier
   - Verifier reads all SUMMARY.md files
   - Verifier runs verification criteria
   - Verifier produces VERIFICATION-REPORT.md
7. STATE.md updated with completion status

**Codebase Analysis Flow (Map-Codebase Command):**

1. User runs `/gsd:map-codebase [focus]` (optional focus: tech, arch, quality, concerns)
2. If no focus provided: Orchestrator spawns 4 parallel agents
   - Agent 1 (tech focus): reads package manifests, configs → writes STACK.md, INTEGRATIONS.md
   - Agent 2 (arch focus): reads directory structure, entry points → writes ARCHITECTURE.md, STRUCTURE.md
   - Agent 3 (quality focus): reads linting configs, tests → writes CONVENTIONS.md, TESTING.md
   - Agent 4 (concerns focus): reads code for TODOs, complexity → writes CONCERNS.md
3. Each agent writes documents directly to `.planning/codebase/`
4. Orchestrator collects confirmations and reports completion

**State Management:**

- Persistent state lives in `.planning/` (project root)
- Agents are stateless - they read state files at start, write outputs
- Each phase creates isolated state directory: `.planning/phases/{PHASE}-{NAME}/`
- Accumulation: Earlier phases' outputs inform later phases' inputs
- Resumption: Any interrupted phase can resume from PLAN.md + STATE.md

## Key Abstractions

**Command Orchestrator:**
- Purpose: Parse user input, spawn appropriate agent, coordinate workflow
- Examples: `commands/gsd/new-project.md`, `commands/gsd/execute-phase.md`
- Pattern: Markdown workflow definitions with embedded process steps
- Responsibilities: Validate environment, load state, spawn agents, wait for completion, commit changes

**Agent (Subagent):**
- Purpose: Execute focused task with specialized role and tools
- Examples: `agents/gsd-executor.md`, `agents/gsd-planner.md`
- Pattern: YAML frontmatter (role, tools, color) + detailed execution instructions
- Responsibilities: Load context, execute task, write output files, report completion

**Document Template:**
- Purpose: Define structure for user-facing and internal documents
- Examples: `get-shit-done/templates/project.md`, `get-shit-done/templates/codebase/architecture.md`
- Pattern: Markdown with placeholders and instructions
- Usage: Orchestrators and agents fill templates with discovered content

**Workflow Procedure:**
- Purpose: Multi-step process that orchestrators delegate to agents
- Examples: `get-shit-done/workflows/execute-plan.md`, `get-shit-done/workflows/verify-phase.md`
- Pattern: Markdown with numbered/nested steps, bash commands, conditionals
- Responsibilities: Define how to execute complex operations

**State File (Accumulated Context):**
- Purpose: Track project decisions and progress
- Examples: STATE.md (current status), RESEARCH.md (domain understanding), PLAN.md (executable specs)
- Pattern: Markdown with YAML frontmatter + sections
- Usage: Agents read as context, orchestrators update after phases complete

## Entry Points

**Installation Entry:**
- Location: `bin/install.js`
- Triggers: `npx get-shit-done-cc` command
- Responsibilities: Detect platform, prompt for runtime/location, copy resources to config directory

**CLI Command Entry:**
- Location: `commands/gsd/{command}.md`
- Triggers: `/gsd:{command}` invoked in Claude Code/OpenCode
- Responsibilities: Validate environment, parse arguments, spawn orchestrators/agents

**Agent Entry:**
- Location: `agents/{agent-name}.md`
- Triggers: Task passed to agent via Claude API
- Responsibilities: Parse frontmatter, load referenced files, execute role-based task

## Error Handling

**Strategy:** Fail loudly with context, offer recovery paths

**Patterns:**

- **Validation Errors:** Check state before spawning agents (fail fast if .planning/ missing)
- **Agent Failures:** Catch exception, report to user with context from STATE.md, suggest `/gsd:debug` or resume with `--gaps` flag
- **Partial Completion:** Agents checkpoint at task boundaries - can resume from PLAN.md without re-executing completed tasks
- **State Corruption:** Commands validate STATE.md syntax; if invalid, offer to reconstruct from artifacts
- **Tool Permission Errors:** Recommend `--dangerously-skip-permissions` flag for automated use

## Cross-Cutting Concerns

**Logging:**
- Agent approach: Console output summarizes progress and decisions
- Orchestrator approach: Report agent confirmations, collect and display verification results
- User visibility: All significant decisions logged to STATE.md for audit trail

**Context Management:**
- File-based state persists across agent invocations
- Agents load full context at start, minimize context transfer to orchestrator
- State files (PROJECT.md, RESEARCH.md, PLAN.md) serve as context bridges between agents

**Git Integration:**
- Orchestrators create commits after phase completion
- Agents create atomic commits per task during execution
- State files (PLAN.md, SUMMARY.md) are committed for audit trail
- Config: `.planning/config.json` controls whether planning docs are committed

**Platform Support:**
- Installation supports Claude Code (Windows/macOS/Linux) and OpenCode (open source alternative)
- Installer converts Claude Code frontmatter to OpenCode format
- Hook commands normalize paths for cross-platform execution

**Model Profile Selection:**
- Config: `.planning/config.json` stores user's model_profile (quality/balanced/budget)
- Agents spawn with profile-appropriate models
- Mapping: Each agent has model by profile (e.g., gsd-planner uses opus/opus/sonnet)
- Fallback: Defaults to balanced if not configured

---

*Architecture analysis: 2026-01-27*
*Update when major patterns change*
