# Phase 21: Gemini CLI Integration - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Cherry-pick Gemini CLI support and universal improvements from upstream GSD (10 commits total), adapt branding to GRD, and verify integration works. Phase 20 identified specific commits and their dependencies.

</domain>

<decisions>
## Implementation Decisions

### Cherry-pick approach
- Best-effort auto-resolve conflicts - only stop if completely stuck
- Claude decides: individual vs squashed commits for universal improvements
- Cherry-pick normally then amend for Gemini commits (faster approach)
- Fix forward if issues arise (keep commit, add fix on top)
- Claude decides: attribution approach and commit ordering
- Include package.json/lock updates only if Gemini commits require them
- Work directly on main branch (no feature branch)

### Branding adaptation
- Comprehensive updates: paths, messages, help text, comments, internal references, AND variable names
- Update all command references from /gsd: to /grd: prefix
- Claude decides: commit message handling for -x flag references
- Final branding sweep required: grep for 'gsd', 'GSD', 'get-shit-done' after all cherry-picks

### Testing strategy
- Smoke test level: verify Gemini detected + agents install
- Gemini CLI is available locally for testing
- Run full test suite after cherry-picks to verify no regressions
- Success criteria: installer detects Gemini AND agents install correctly for Gemini CLI format

### Claude's Discretion
- Individual vs squashed commits for universal improvements
- Commit attribution (preserve original author or attribute to GRD)
- Optimal cherry-pick order based on dependencies
- Commit message handling for upstream references

</decisions>

<specifics>
## Specific Ideas

- Cherry-pick order from Phase 20 research: universal improvements first, then installer changes, then Gemini core
- Gemini dependency chain: `5379832` -> `91aaa35` -> `5660b6f`
- Expected HIGH conflict likelihood on bin/install.js
- Tool mapping documented in CHERRY_PICK_DECISIONS.md (Read->read_file, Bash->run_shell_command, etc.)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 21-gemini-cli-integration*
*Context gathered: 2026-02-02*
