# Phase 17: Artifact Updates - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Update all artifact templates and references to use consistent research terminology (experiments, studies, protocols). This includes STATE.md, ROADMAP.md (to be renamed), help.md, and command routing across 33 command files.

</domain>

<decisions>
## Implementation Decisions

### Critical Constraint: GRD/GSD Coexistence
- **GRD and GSD are separate tools** that must coexist on the same system
- **No backward compatibility needed** — GRD doesn't need to support GSD commands
- **No conflicts allowed** — each tool operates independently
- **This project uses GSD** — the `.planning/` directory here uses GSD conventions
- **GRD templates are for new GRD projects** — not for migrating existing GSD projects

### Template terminology (GRD templates only)
- GRD's STATE.md tracks progress as "Experiment: N of M" format
- GRD's ROADMAP.md uses study/experiment terminology (keep filename as ROADMAP.md for familiarity)
- GSD templates remain untouched — they're a separate tool
- No renaming of plan files or folder structure — GRD uses same conventions as GSD
- RESEARCH.md filename kept (matches literature-review output)

### Help documentation
- Commands grouped by type: Lifecycle, Research, Data, Utility
- Full reference detail: name + description + args + examples + common flags
- Quick-start workflow section included with new-study → design-experiment → run-experiment → validate-results flow
- GRD commands only — GSD has its own help.md

### Next-step routing
- Verbose format: command + tips (include /clear suggestion and alternatives)
- Skip hints context-dependent: only suggest --skip-research when appropriate
- Post-validation routing conditional: last experiment → complete-study, else → next experiment
- Data-aware routing: data workflows suggest explore/architect/evaluate; code workflows suggest design/run

### What NOT to change
- GSD templates, commands, or artifacts — separate tool
- This project's `.planning/` directory — uses GSD
- MILESTONES.md — belongs to GSD, leave it alone
- No migration of phases/ to experiments/ — unnecessary

### Claude's Discretion
- Exact categorization of commands into Lifecycle/Research/Data/Utility groups
- Format details for quick-start examples
- Whether ROADMAP.md should be renamed to PROTOCOL.md in GRD templates (leaning toward keeping ROADMAP.md)

</decisions>

<specifics>
## Specific Ideas

- Keep ROADMAP.md filename in GRD — familiar to users, just update terminology inside
- "Research History" has broader framing than "Study History" — preferred for GRD templates
- GRD and GSD install to different locations (~/.claude/get-research-done vs ~/.claude/get-shit-done)
- Commands are prefixed differently (/grd: vs /gsd:) so no collision

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 17-artifact-updates*
*Context gathered: 2026-02-02*
