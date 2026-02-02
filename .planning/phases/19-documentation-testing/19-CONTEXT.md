# Phase 19: Documentation & Testing - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Validate that all code and agent prompts reflect renamed commands and test that command chains work end-to-end. This phase focuses on **validation only** — all `.planning` files remain untouched.

</domain>

<decisions>
## Implementation Decisions

### PROJECT.md Cleanup
- **Skip entirely** — No changes to any `.planning` files
- Success criteria in ROADMAP.md needs revision to reflect this scope change
- All `.planning` files (PROJECT.md, STATE.md, ROADMAP.md) stay as-is

### Agent Prompt Validation
- Check **all GRD agents** in `get-research-done/` directory
- Stale references = old command names + old terminology in routing text
- Use grep search to find matches, fix anything found
- GSD source directory is out of scope (GRD agents only)

### End-to-End Workflow Test
- Test **all command chains** (every command that routes to another)
- Create **automated integration test** that invokes commands
- Success = each command exists and runs without error
- Claude decides test file placement based on codebase structure

### Stale Reference Detection
- Scan **everything except `.planning/`** directory
- Use the 9 old command names from STATE.md rename mapping table:
  - `plan-phase` → `design-experiment`
  - `execute-phase` → `run-experiment`
  - `discuss-phase` → `scope-experiment`
  - `verify-work` → `validate-results`
  - `research-phase` → `literature-review`
  - `list-phase-assumptions` → `list-experiment-assumptions`
  - `add-phase` → `add-experiment`
  - `insert-phase` → `insert-experiment`
  - `remove-phase` → `remove-experiment`
- **Human reviews each match** before fixing (no blind replacement)
- Matches that shouldn't change: document as intentional exceptions

### Claude's Discretion
- Integration test file placement
- Exact grep patterns for stale detection
- How to structure the exceptions documentation
- Order of validation tasks

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches.

</specifics>

<deferred>
## Deferred Ideas

- **Cherry-picking from upstream GSD** — Sync fixes and Google CI integration from source repo. This is its own phase involving repo management and selective integration.
- **GSD source directory updates** — Checking/updating agents in the GSD directory (separate from GRD)

</deferred>

---

*Phase: 19-documentation-testing*
*Context gathered: 2026-02-02*
