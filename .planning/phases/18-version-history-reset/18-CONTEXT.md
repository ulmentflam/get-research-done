# Phase 18: Version History Reset - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Reset GRD's external presentation to be a clean v1.0 product. This phase focuses ONLY on external-facing artifacts (README.md, CHANGELOG.md, package.json metadata). All .planning files remain unchanged — internal history is preserved.

</domain>

<decisions>
## Implementation Decisions

### Scope clarification
- .planning files stay completely unchanged (STATE.md, PROJECT.md, MILESTONES.md, ROADMAP.md, etc.)
- Reset applies only to: README.md, CHANGELOG.md, package.json metadata
- Internal GSD milestone history is preserved for development continuity

### GSD acknowledgment
- Brief acknowledgment of GSD origins in README.md footer
- Something like "Built on the GSD framework" — small, not prominent
- No mention of GSD versions or migration in main documentation

### CHANGELOG handling
- Reset completely — clear all GSD-era entries
- Start fresh with GRD 1.0 changelog
- No archive of old entries needed

### Version numbering
- Keep current version in package.json (don't reset to 1.0.0)
- Keep v1.2 milestone designation in ROADMAP.md
- Follow standard semver for future releases

### External documentation
- README presents GRD with feature highlights (Explorer, Architect, Critic, etc.)
- Capabilities listed as GRD features, not as "validated requirements"
- Clean product positioning without migration references

### Claude's Discretion
- Exact wording of GSD acknowledgment in README footer
- README structure and feature presentation
- Package.json description and keywords updates

</decisions>

<specifics>
## Specific Ideas

- GSD acknowledgment should be understated — footer placement, brief wording
- README should highlight key agents (Explorer, Architect, Critic) as GRD capabilities

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 18-version-history-reset*
*Context gathered: 2026-02-02*
