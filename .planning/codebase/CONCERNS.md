# Codebase Concerns

**Analysis Date:** 2026-01-27

## Tech Debt

**Parallel Execution State Tracking:**
- Issue: Executor agent (`gsd-executor.md`, `agents/gsd-executor.md`) must track which tasks completed in each wave when running plans in parallel. STATE.md coordination across simultaneous Claude instances relies on file I/O ordering and potential race conditions.
- Files: `agents/gsd-executor.md`, `get-shit-done/workflows/execute-plan.md`
- Impact: If multiple parallel executors write to STATE.md or shared tracking files simultaneously, task completion records could collide or become inconsistent, leading to duplicate execution or missed verifications
- Fix approach: Implement file-locking mechanism or use unique temp files per executor wave that get merged after all tasks complete

**Context Load in Orchestrator Pattern:**
- Issue: Commands like `/gsd:new-project` (`commands/gsd/new-project.md`) spawn multiple research agents in parallel, then orchestrator collects all results and inlines them for synthesis. Large research output (STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md) in parallel research can accumulate to high context usage before synthesis even begins.
- Files: `commands/gsd/new-project.md`, `agents/gsd-research-synthesizer.md`
- Impact: Early-phase context pressure when research output is large, forcing synthesis to compress findings or work in degraded mode
- Fix approach: Research agents write directly to `.planning/research/` and don't return output; orchestrator reads files instead of collecting inline

**Plan Verification Loop with Revisions:**
- Issue: Plan checker (`gsd-plan-checker.md`, 745 lines) can request revisions up to 3 times. If revisions keep failing, user escalation occurs but no automatic degradation path exists (can't skip checker and execute unverified plans).
- Files: `agents/gsd-plan-checker.md`, `agents/gsd-planner.md`
- Impact: If planner cannot satisfy checker on 3rd revision attempt, workflow blocks waiting for user input. No graceful fallback exists.
- Fix approach: Add 4th attempt with reduced strictness (focus on critical dimensions only), or auto-approve with warnings if max iterations reached

**Manual Dependency Management in Plans:**
- Issue: Planner must manually track task dependencies and assign wave numbers (`wave: 1`, `wave: 2`). Complex phases with many interdependencies require explicit reasoning about execution order that could be automated.
- Files: `agents/gsd-planner.md` lines ~515-570 (dependency graph section)
- Impact: Planner might create invalid dependency chains (circular, missing transitive deps) that only fail during execution
- Fix approach: Require planner to output a formalized dependency matrix that executor validates before running

## Known Bugs

**File Path Expansion in Windows:**
- Symptoms: Path references may not expand correctly in Windows environments, particularly with tilde expansion (`~/.claude/`)
- Files: `bin/install.js` lines 38-89 (global directory resolution)
- Trigger: Installation on Windows, especially in non-standard environments like Docker or WSL
- Workaround: Use explicit `CLAUDE_CONFIG_DIR` or `OPENCODE_CONFIG_DIR` environment variables instead of relying on tilde expansion

**Phase Directory Naming Inconsistency:**
- Symptoms: Phase folders can exist as both `01-phase-name` (zero-padded) and `1-phase-name` (unpadded), causing duplicate phase detection
- Files: Any command that globs for phase directories: `agents/gsd-executor.md`, workflows
- Trigger: Manual phase folder renaming, or migration from older GSD versions
- Workaround: Always use zero-padded phase numbering (`01-`, `02-`, etc.) manually; planner respects this convention

**OpenCode Global Config Path:**
- Symptoms: Previous versions used `~/.opencode/` but OpenCode follows XDG spec expecting `~/.config/opencode/`. Upgrades may have orphaned configs.
- Files: `bin/install.js` lines 47-64 (getOpencodeGlobalDir function)
- Trigger: Upgrade from v1.9.6 or earlier on systems using OpenCode
- Workaround: Manually move `~/.opencode/` to `~/.config/opencode/` if upgrading from old versions

## Security Considerations

**Context Window Dangerously Large Agent Prompts:**
- Risk: Some agents like `gsd-planner.md` (1,386 lines), `gsd-executor.md` (784 lines), and `gsd-debugger.md` (1,203 lines) contain extensive instructional context that could reduce available context for actual work if loaded together with large project files
- Files: `agents/gsd-planner.md`, `agents/gsd-executor.md`, `agents/gsd-debugger.md`
- Current mitigation: Each agent spawned individually in fresh context window; orchestrators don't load multiple agents together
- Recommendations: Monitor agent file sizes; break largest agents (>1000 lines) into role-specific sub-modules if they continue growing

**Dependency Version Pinning:**
- Risk: `package.json` has no lockfile vendoring and only one dev dependency (`esbuild`). npm install across environments may pull different versions, especially with major package updates.
- Files: `package.json` (no exact versions), `package-lock.json` exists but only documents esbuild
- Current mitigation: Minimal dependencies by design (philosophy documented in MAINTAINERS.md)
- Recommendations: Ensure npm ci (not npm install) is used in CI/Docker; document minimum Node.js version (currently >=16.7.0)

**Installation Script Permissions:**
- Risk: `bin/install.js` creates directories and copies files into user config directories. If run with elevated privileges, could modify system-wide configs unintentionally.
- Files: `bin/install.js`
- Current mitigation: Script clearly asks for location (global vs local) before proceeding
- Recommendations: Add warning if run with `sudo` or elevated privileges; default to local installation if elevation detected

**Unvalidated State File Operations:**
- Risk: STATE.md and CONTEXT.md files are read/written without strict validation. Malformed YAML/JSON in these files could cause parsing failures in dependent agents.
- Files: Any agent that reads `.planning/STATE.md` or `{phase}-CONTEXT.md`
- Current mitigation: Grep/cat operations use defensive patterns with `|| echo "default"`
- Recommendations: Add JSON schema validation when reading `.planning/config.json`; add try-catch around YAML parsing in state readers

## Performance Bottlenecks

**Large Markdown File Parsing:**
- Problem: Commands must read and parse large files like CHANGELOG.md (1,202 lines), execute-plan.md (1,844 lines), complete-milestone.md (756 lines) using grep/cat patterns that scale linearly with file size
- Files: `get-shit-done/workflows/execute-plan.md`, any workflow using heavy file reads
- Cause: Workflows use bash patterns (grep, sed, awk) on full file contents instead of streaming or indexing
- Improvement path: Pre-compute and cache frequently accessed sections (e.g., store "current phase number" in STATE.md instead of parsing ROADMAP.md each time)

**Research Agent Parallel Output Consolidation:**
- Problem: Four research agents run in parallel (stack, features, architecture, pitfalls), each writing files. Synthesizer then reads all files in sequence and consolidates findings. If any agent takes longer, synthesis is blocked.
- Files: `agents/gsd-research-synthesizer.md`, `commands/gsd/new-project.md`
- Cause: Synchronization point (all research must complete before synthesis starts) in orchestrator
- Improvement path: Implement streaming synthesis where each research file is processed immediately upon completion, not waited on

**Verification Loop Context Accumulation:**
- Problem: Verification workflow reads plan file, executes all tasks, reads verification results, and planner agent must reread entire plan to revise it. With 3 revision iterations, large plans get read 4 times total.
- Files: `agents/gsd-planner.md`, `agents/gsd-plan-checker.md`
- Cause: No file caching or incremental update strategy
- Improvement path: Planner stores parsed task structure in STATE.md to avoid full re-reads during revisions

## Fragile Areas

**Phase Numbering and File Matching:**
- Files: `agents/gsd-executor.md`, any orchestrator scanning for phase directories
- Why fragile: Globs for `{phase}*` pattern require exact naming convention. If user renames phase folder manually (e.g., drops zero-padding), executor can't find plans, create summaries, or commit to correct phase.
- Safe modification: Always rename phase folders using a command (not manual rename), add validation in executor to warn if naming is inconsistent
- Test coverage: No automated tests for phase folder discovery; all phase naming changes rely on manual verification

**Dependency Graph Validation:**
- Files: `agents/gsd-planner.md` task breakdown section, executor wave execution
- Why fragile: Planner creates dependency graphs and wave assignments. Executor trusts these are correct. Circular dependencies, missing transitive depends, or invalid wave numbers can cause deadlock or incorrect execution order.
- Safe modification: Add pre-execution dependency validation in executor before any task runs; print the dependency graph so user can verify
- Test coverage: No automated tests for dependency validation; all plans rely on planner's manual reasoning

**State File Consistency Across Parallel Execution:**
- Files: `agents/gsd-executor.md`, `get-shit-done/workflows/execute-plan.md`, any parallel wave execution
- Why fragile: Multiple executor instances may write STATE.md and phase SUMMARY files simultaneously. File system doesn't provide atomic multi-write, so concurrent updates can lose data.
- Safe modification: Implement write-then-rename pattern (write to temp file, atomic rename) for all state updates; add append-only log for completed tasks
- Test coverage: No concurrent execution tests; all testing assumes sequential task completion

**Orchestrator File Inlining Patterns:**
- Files: Any command file that uses `@file` references and inlines content with cat/read
- Why fragile: Orchestrators rely on @ references being correctly resolved and file contents being readable. Large files or missing files can cause orchestrator to fail without graceful fallback.
- Safe modification: Wrap file reads in try-catch, provide clear error messages if referenced files don't exist; validate file paths before passing to agents
- Test coverage: No tests for missing/unreadable file handling in orchestrator pattern

## Scaling Limits

**Context Window per Agent (200k tokens):**
- Current capacity: Each agent spawned with ~200k token budget per Claude instance
- Limit: With projects adding 50+ files and planning for 5+ phases, context can fill to 50-70% before task execution, causing quality degradation
- Scaling path: Implement file filtering in agents (only load relevant files, not entire codebase); add file size warnings in orchestrators; split large phases into smaller sub-phases

**Parallel Execution Waves:**
- Current capacity: Executor groups tasks into waves and runs each wave sequentially. Wave grouping is manual (planner assigns wave numbers).
- Limit: With 20+ tasks in a phase, optimal wave calculation becomes complex; planner may create sub-optimal waves (too many sequential tasks that could run in parallel)
- Scaling path: Implement automatic wave calculation from dependency graph; validate that executor is actually achieving parallel speedup

**Research Output Size:**
- Current capacity: 4 parallel research agents produce 4-5 markdown files (STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md, SUMMARY.md)
- Limit: Large domain research (e.g., full framework ecosystems) can produce 50-100kb per file, totaling 200-500kb input to synthesizer
- Scaling path: Compress research output (summaries within summaries); split FEATURES.md into smaller category files; implement streaming synthesis

## Dependencies at Risk

**esbuild (v0.24.0):**
- Risk: Only development dependency, used for building hooks. No pinned version constraints; could auto-upgrade to incompatible major version.
- Impact: Hook build failures if esbuild introduces breaking changes; installation would fail
- Migration plan: Pin to `^0.24.0` in package.json; add pre-publish build test to ensure hooks build successfully

**Node.js >=16.7.0:**
- Risk: Lower bound is 8 years old. Ecosystem has moved to Node 18+ LTS. Unclear if GSD still works on Node 16.
- Impact: Users on old Node versions may hit unexpected failures due to API differences or missing features
- Migration plan: Test against Node 18 LTS and 20 LTS; update minimum requirement to 18.0.0; document breaking Node version support if introduced

## Missing Critical Features

**Atomic File Writes in Parallel Execution:**
- Problem: Executor writes STATE.md and phase SUMMARY.md without atomic file operations. Concurrent writes from parallel waves can corrupt files or lose task completion data.
- Blocks: Scaling beyond sequential execution; reliable multi-wave execution; resumable execution after crashes

**Automated Dependency Validation:**
- Problem: Planner manually creates dependency graphs and wave assignments. No pre-execution validation that dependencies are valid (no circular deps, all transitive deps satisfied).
- Blocks: Complex phase planning; confidence in parallel execution correctness

**Codebase Index for Fast Reference:**
- Problem: Commands read entire ROADMAP.md, STATE.md, PROJECT.md files even when looking for single values. No index or fast lookup structure.
- Blocks: Performance scaling on large projects; reducing orchestrator execution time

**Rollback/Undo Capability:**
- Problem: If execution produces wrong output, user must manually delete files or revert commits. No built-in undo mechanism.
- Blocks: Safe experimentation; recovery from incorrect plans

## Test Coverage Gaps

**Parallel Execution State Consistency:**
- What's not tested: Multiple executor instances writing to same STATE.md and SUMMARY files concurrently
- Files: `agents/gsd-executor.md`, execution workflows
- Risk: Data corruption, lost task records, inconsistent completion tracking
- Priority: **High** — directly impacts reliability of multi-wave execution

**Phase Folder Discovery and Naming:**
- What's not tested: Executor correctly finds phase folders with zero-padded and non-zero-padded names; renames are detected
- Files: Any command globbing for `{phase}*` patterns
- Risk: Executor skips phases due to naming mismatches
- Priority: **High** — affects core workflow reliability

**Dependency Graph Validation:**
- What's not tested: Planner-created dependency graphs for circular dependencies, missing transitive edges, invalid wave assignments; executor detects these before execution
- Files: `agents/gsd-planner.md`, `agents/gsd-executor.md`
- Risk: Deadlock during execution, tasks running in wrong order
- Priority: **High** — directly impacts plan correctness

**File Reading Error Handling:**
- What's not tested: Graceful degradation when referenced files don't exist, are malformed, or unreadable; orchestrators provide clear errors instead of silent failures
- Files: Any orchestrator using @ references and file reads
- Risk: Silent failures, unclear error messages, workflow stops without user guidance
- Priority: **Medium** — affects debuggability but doesn't block functionality

**Installation on Windows and WSL:**
- What's not tested: Full installation flow on Windows, Windows Subsystem for Linux, Docker containers; path expansion works correctly
- Files: `bin/install.js`
- Risk: Installation fails on non-Unix systems; users follow incorrect workarounds
- Priority: **Medium** — affects platform support

---

*Concerns audit: 2026-01-27*
