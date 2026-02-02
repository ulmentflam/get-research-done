# Phase 22: Branding Updates - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Update SVG/PNG visual assets to reflect GRD identity. This includes the ASCII art logo, terminal preview content, file naming, and color scheme. No functional code changes — purely visual branding assets.

</domain>

<decisions>
## Implementation Decisions

### ASCII Art Design
- Bold block letters style (heavy, chunky — high visual impact)
- Just "GRD" letters, no tagline or decorative borders
- Use exact same font/style as current GSD letters — swap G-S-D for G-R-D
- Same size/scale proportions as current logo

### Terminal Preview Content
- Show `npx get-research-done` command being run
- Display install progress followed by GRD welcome banner with version
- End with `/grd:help` hint (e.g., "Try /grd:help to get started")

### File Naming & Sizes
- Logo files named `grd-logo-2000.*` (SVG and PNG)
- PNG output at 2000px width
- Delete old `gsd-logo-*` files after creating GRD versions
- Keep files in same location as current logo files

### Color Scheme
- New color palette with research/academic feel (blues, teals — scientific, trustworthy)
- Dark terminal background in preview (black/dark gray)
- Create both dark mode and light mode variants

### Claude's Discretion
- Exact version number to display in terminal preview
- Specific blue/teal shades for the new palette
- Light mode variant implementation details

</decisions>

<specifics>
## Specific Ideas

- Research/academic color direction: blues and teals convey scientific trustworthiness
- Terminal preview should feel like a real installation experience
- Two logo variants needed (dark and light backgrounds)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 22-branding-updates*
*Context gathered: 2026-02-02*
