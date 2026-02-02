# Phase 15: Command Renames - Context

**Gathered:** 2026-02-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Rename 9 phase-related CLI commands from software-dev terminology to research-native terminology. All references to these commands (in outputs, help text, error messages) must update atomically. This phase does not add new commands or change command behavior — only names.

</domain>

<decisions>
## Implementation Decisions

### Migration approach
- Hard break — old command names stop working immediately, no aliases or deprecation warnings
- Remove old names completely from codebase — no mapping tables, no backward compatibility
- Researcher/planner may surface additional renames beyond the 9 in ROADMAP.md during planning
- All cross-references must update atomically — no mixed terminology during implementation

### Command naming style
- Use verb-object format: `design-experiment`, `run-experiment`, `validate-results`
- Keep `literature-review` as-is (research convention, noun phrase acceptable here)
- Shorten compound names where unambiguous: prefer `list-assumptions` over `list-experiment-assumptions` if context is clear

### Help text updates
- No mention of old command names — clean break, no "formerly known as"
- One-liner descriptions per command
- Update `/grd:help` output as part of this phase

### Error messaging
- Standard "skill not found" for old command names — no special handling
- User-facing error messages use "experiment" terminology (e.g., "Experiment 99 not found")
- Include next-step suggestions in error output using new command names

### Terminology scope
- Rename "Phase" to "Experiment" throughout roadmap and user-facing text
- This applies to ROADMAP.md structure as well as command outputs

### Claude's Discretion
- Final choice between `scope-experiment` vs `define-experiment` for discuss-phase rename
- Help command grouping structure (keep current or reorganize by workflow stage)
- Specific wording of one-liner descriptions

</decisions>

<specifics>
## Specific Ideas

- "I want a clean break — no traces of the old terminology"
- Verb-object pattern for consistency, but `literature-review` is a research convention worth preserving
- Shorter command names are better when unambiguous

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 15-command-renames*
*Context gathered: 2026-02-01*
