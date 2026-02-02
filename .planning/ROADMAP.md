# Roadmap: Get Research Done (GRD)

## Milestones

- v1.0 MVP - Phases 1-9 (shipped 2026-01-30)
- v1.1 Research UX Refinement - Phases 10-14 (shipped 2026-02-01)
- v1.2 Command Unification - Phases 15-19 (shipped 2026-02-02)
- v1.3 Branding & Gemini Integration - Phases 20-23 (in progress)

## Phases

<details>
<summary>v1.0 MVP (Phases 1-9) - SHIPPED 2026-01-30</summary>

**Milestone Goal:** Recursive ML experimentation framework with data-first workflows, automated validation loops, and human decision gates

**Phases completed:** 1-9 (39 plans total)

**Key accomplishments:**
- GRD branding and CLI with 27 commands, new ASCII art, and npm package
- Data-first Explorer agent with statistical profiling and leakage detection
- Architect agent generating testable hypotheses with falsification criteria
- Recursive validation loop (Researcher/Critic/Evaluator) with routing
- Human evaluation gate with evidence packages and decision logging
- Jupyter notebook support with papermill execution and graduation path

**Stats:** 288 files created/modified, 48,494 lines of code, 47 days to ship

</details>

<details>
<summary>v1.1 Research UX Refinement (Phases 10-14) - SHIPPED 2026-02-01</summary>

**Milestone Goal:** Streamline GRD for research workflows by removing GSD legacy, adding accessible EDA for non-data-scientists, and creating fast exploration paths.

**Phases completed:** 10-14 (13 plans total)

- [x] Phase 10: Command Cleanup & Foundation (2/2 plans) - completed 2026-01-31
- [x] Phase 11: Terminology Rename (3/3 plans) - completed 2026-01-31
- [x] Phase 12: Quick Explore (3/3 plans) - completed 2026-02-01
- [x] Phase 13: Accessible Insights (2/2 plans) - completed 2026-02-01
- [x] Phase 14: Integration Testing & Validation (3/3 plans) - completed 2026-02-01

**Key accomplishments:**
- Study-centric terminology (6 lifecycle commands renamed)
- Quick Explore command with Rich console output
- Accessible Insights with plain English explanations
- Integration testing with 118/118 automated checks passed

**Stats:** 76 files created/modified, +16,503 lines of code, 3 days to ship

</details>

<details>
<summary>v1.2 Command Unification (Phases 15-19) - SHIPPED 2026-02-02</summary>

**Milestone Goal:** Transform all lifecycle commands from software-dev terminology (phases, milestones, roadmaps) to research-native terminology (experiments, studies, protocols) with correct command chaining.

**Phases completed:** 15-19 (12 plans total)

- [x] Phase 15: Command Renames (4/4 plans) - completed 2026-02-02
- [x] Phase 16: Command Chaining Fixes (2/2 plans) - completed 2026-02-02
- [x] Phase 17: Artifact Updates (3/3 plans) - completed 2026-02-02
- [x] Phase 18: Version History Reset (1/1 plan) - completed 2026-02-02
- [x] Phase 19: Documentation & Testing (2/2 plans) - completed 2026-02-02

**Key accomplishments:**
- Renamed 9 commands to research terminology (design-experiment, run-experiment, etc.)
- Fixed command chaining for complete research workflow
- Updated templates to use experiment/study terminology
- Reset external documentation for clean product positioning
- Added 23 integration tests validating command chains

**Stats:** 83 files created/modified, +3,452 lines of code, 2 days to ship

**Full archive:** .planning/milestones/v1.2-ROADMAP.md

</details>

### v1.3 Branding & Gemini Integration (In Progress)

**Milestone Goal:** Update visual branding to GRD identity, sync with upstream GSD for Gemini CLI and other features, and finalize documentation.

- [x] Phase 20: GSD Sync Setup & Exploration (SYNC-01, SYNC-02, SYNC-03) - completed 2026-02-02
- [ ] Phase 21: Gemini CLI Integration (SYNC-04, SYNC-05)
- [ ] Phase 22: Branding Updates (BRAND-01, BRAND-02, BRAND-03, BRAND-04, BRAND-05, BRAND-06)
- [ ] Phase 23: Documentation & Finalization (DOCS-01, DOCS-02, DOCS-03)

## Phase Details

### Phase 20: GSD Sync Setup & Exploration
**Goal**: Establish GSD upstream remote and identify features to cherry-pick
**Depends on**: Nothing (first phase of milestone)
**Requirements**: SYNC-01, SYNC-02, SYNC-03
**Success Criteria** (what must be TRUE):
  1. GSD upstream remote is configured and fetchable (`git fetch gsd-upstream` works)
  2. List of new GSD features since fork is documented with commit hashes
  3. Cherry-pick decisions are documented (what to take, what to skip, why)
  4. Gemini CLI location identified in GSD codebase
**Plans**: 1 plan
Plans:
- [x] 20-01-PLAN.md - Add upstream remote, document features, create cherry-pick decisions - completed 2026-02-02

### Phase 21: Gemini CLI Integration
**Goal**: Cherry-pick Gemini CLI and selected features from GSD, adapt to GRD branding
**Depends on**: Phase 20 (need cherry-pick list and commit hashes)
**Requirements**: SYNC-04, SYNC-05
**Success Criteria** (what must be TRUE):
  1. Gemini CLI command is available (`/grd:gemini` or equivalent)
  2. Gemini CLI uses GRD terminology and conventions
  3. Any additional cherry-picked features function correctly
  4. No GSD-specific references remain in cherry-picked code
**Plans**: 1 plan
Plans:
- [ ] 21-01-PLAN.md - Cherry-pick universal improvements and Gemini support, adapt branding

### Phase 22: Branding Updates
**Goal**: Update SVG/PNG assets to reflect GRD identity
**Depends on**: Nothing (can run parallel with Phase 21)
**Requirements**: BRAND-01, BRAND-02, BRAND-03, BRAND-04, BRAND-05, BRAND-06
**Success Criteria** (what must be TRUE):
  1. SVG logo displays "GRD" ASCII art (not "GSD")
  2. Terminal preview shows `npx get-research-done` command
  3. Terminal preview shows "Get Research Done v1.3.0" title
  4. Terminal preview shows GRD-specific install output and `/grd:help`
  5. PNG logo is regenerated from updated SVG at 2000px
  6. Logo files renamed to `grd-logo-2000.*`
**Plans**: TBD

### Phase 23: Documentation & Finalization
**Goal**: Update all documentation to reflect v1.3 changes and any new features
**Depends on**: Phase 21, Phase 22 (need to document what was added)
**Requirements**: DOCS-01, DOCS-02, DOCS-03
**Success Criteria** (what must be TRUE):
  1. README.md reflects current GRD branding and v1.3 features
  2. help.md includes any new commands from cherry-picks
  3. All cherry-picked features have usage documentation
**Plans**: TBD

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1-9. v1.0 MVP | v1.0 | 39/39 | Complete | 2026-01-30 |
| 10-14. v1.1 Research UX | v1.1 | 13/13 | Complete | 2026-02-01 |
| 15-19. v1.2 Command Unification | v1.2 | 12/12 | Complete | 2026-02-02 |
| 20. GSD Sync Setup & Exploration | v1.3 | 1/1 | Complete | 2026-02-02 |
| 21. Gemini CLI Integration | v1.3 | 0/1 | Not started | - |
| 22. Branding Updates | v1.3 | 0/TBD | Not started | - |
| 23. Documentation & Finalization | v1.3 | 0/TBD | Not started | - |
