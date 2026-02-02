# Phase 17: Artifact Updates - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Update all artifact templates and references to use consistent research terminology (experiments, studies, protocols). This includes STATE.md, ROADMAP.md (to be renamed), help.md, and command routing across 33 command files.

</domain>

<decisions>
## Implementation Decisions

### Template terminology
- STATE.md tracks progress as "Experiment: N of M" format
- ROADMAP.md renamed to PROTOCOL.md
- "Milestone" replaced with "Study" throughout
- Plan files renamed from XX-YY-PLAN.md to EXP-XX-YY.md
- CONTEXT.md filename kept (not renamed to SCOPE.md)
- Experiment folders use .planning/experiments/XX-name structure (rename from phases/)
- "Milestone History" section becomes "Research History"
- RESEARCH.md filename kept (matches literature-review output)

### Help documentation
- Commands grouped by type: Lifecycle, Research, Data, Utility
- Full reference detail: name + description + args + examples + common flags
- Quick-start workflow section included with new-study → design-experiment → run-experiment → validate-results flow
- No deprecated command mappings — clean break, new commands only

### Next-step routing
- Verbose format: command + tips (include /clear suggestion and alternatives)
- Skip hints context-dependent: only suggest --skip-research when appropriate
- Post-validation routing conditional: last experiment → complete-study, else → next experiment
- Data-aware routing: data workflows suggest explore/architect/evaluate; code workflows suggest design/run

### Archive strategy
- Delete old phase-based templates completely (no archive)
- MILESTONES.md deleted entirely
- All GSD prefixed commands removed (no aliases, no deprecation warnings)

### Claude's Discretion
- Whether to migrate existing .planning/phases/ to experiments/ or keep for v1.2 completion
- Exact categorization of commands into Lifecycle/Research/Data/Utility groups
- Format details for quick-start examples

</decisions>

<specifics>
## Specific Ideas

- PROTOCOL.md feels more research-native than keeping ROADMAP.md
- "Research History" has broader framing than "Study History" — preferred
- EXP-XX-YY.md naming makes experiment files immediately identifiable
- Clean break on GSD removal — no backward compatibility complexity

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 17-artifact-updates*
*Context gathered: 2026-02-02*
