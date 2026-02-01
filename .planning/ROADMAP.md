# Roadmap: Get Research Done (GRD)

## Milestones

- ✅ **v1.0 MVP** - Phases 1-9 (shipped 2026-01-30)
- 🚧 **v1.1 Research UX Refinement** - Phases 10-14 (in progress)
- 📋 **v2.0 Advanced Features** - Phases 14+ (planned)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-9) - SHIPPED 2026-01-30</summary>

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

### 🚧 v1.1 Research UX Refinement (In Progress)

**Milestone Goal:** Streamline GRD for research workflows by removing GSD legacy, adding accessible EDA for non-data-scientists, and creating fast exploration paths.

#### Phase 10: Command Cleanup & Foundation

**Goal**: Remove GSD legacy commands and establish clean baseline for v1.1 features

**Depends on**: Phase 9 (v1.0 complete)

**Requirements**: CLEAN-01, CLEAN-02, CLEAN-03, CLEAN-04

**Success Criteria** (what must be TRUE):
1. All 32 duplicate " 2.md" skill files are deleted from `.claude/commands/grd/`
2. GSD-specific commands (audit-milestone, plan-milestone-gaps) are removed and no longer appear in help
3. Command count reduced from 64 files to 30 unique files (verified via ls count)
4. Help documentation reflects only research-relevant commands

**Plans:** 2 plans

Plans:
- [x] 10-01-PLAN.md — Delete duplicates, remove deprecated commands, update help.md
- [x] 10-02-PLAN.md — Restore audit/gap commands with study-centric naming (gap closure)

#### Phase 11: Terminology Rename

**Goal**: Rename lifecycle commands to match GRD research terminology

**Depends on**: Phase 10

**Requirements**: TERM-01, TERM-02, TERM-03, TERM-04, TERM-05, TERM-06, TERM-07

**Rename Mapping:**
| Current | New | Purpose |
|---------|-----|---------|
| `new-milestone` | `new-study` | Start a new research study |
| `complete-milestone` | `complete-study` | Archive and conclude a study |
| `discuss-phase` | `scope-study` | Scope the research approach |
| `plan-phase` | `plan-study` | Plan the research execution |
| `execute-phase` | `run-study` | Execute the research plan |
| `verify-work` | `validate-study` | Validate research results |

**Success Criteria** (what must be TRUE):
1. All 6 commands renamed with new skill files created
2. Old command names removed (no duplicates)
3. All internal references updated (agent prompts, orchestrators, templates)
4. Help documentation reflects new command names
5. STATE.md and ROADMAP.md templates use new terminology

**Plans:** 3 plans

Plans:
- [x] 11-01-PLAN.md — Rename 6 command files with git mv, update frontmatter
- [x] 11-02-PLAN.md — Update all internal references to new command names
- [x] 11-03-PLAN.md — Update broader terminology (Phase->Study, Milestone->Version)

#### Phase 12: Quick Explore

**Goal**: Enable fast EDA producing summary output for quick data familiarization decisions

**Depends on**: Phase 11

**Requirements**: QUICK-01, QUICK-02, QUICK-03, QUICK-04, QUICK-05

**Success Criteria** (what must be TRUE):
1. User can run `/grd:quick-explore <dataset>` and receive analysis results in under 60 seconds
2. Quick explore outputs summary statistics (row count, column types, missing values percentage) to console
3. Distribution patterns are highlighted with simple indicators (skewness flags, outlier alerts)
4. Output is markdown-formatted and copy-paste ready for team communication
5. DATA_REPORT.md contains "Quick Explore" mode header and note about running full explore for rigor

**Plans:** 3 plans

Plans:
- [x] 12-01-PLAN.md — Create quick-explore command and formatters module
- [x] 12-02-PLAN.md — Create quick.py analysis module and update data-report template
- [x] 12-03-PLAN.md — Integrate quick mode into Explorer/Architect agents and help.md

#### Phase 13: Accessible Insights

**Goal**: Generate plain English data insights for business analyst audience without code or jargon

**Depends on**: Phase 12

**Requirements**: INSIGHT-01, INSIGHT-02, INSIGHT-03, INSIGHT-04, INSIGHT-05

**Success Criteria** (what must be TRUE):
1. User can run `/grd:insights <dataset>` to generate business-friendly EDA report
2. Full technical DATA_REPORT.md is saved to file (same rigor as regular explore)
3. Plain English summary is displayed where every statistic includes "What This Means" explanation
4. Actionable recommendations based on data characteristics appear in summary
5. LLM prompts for further exploration are provided as copy-paste ready suggestions

**Plans**: TBD

Plans:
- [ ] 13-01: TBD during planning

#### Phase 14: Integration Testing & Validation

**Goal**: Validate workflow paths, gating behavior, and prevent regressions before release

**Depends on**: Phase 13

**Requirements**: (Integration testing spans all v1.1 requirements)

**Success Criteria** (what must be TRUE):
1. Progressive path works: quick-explore → full explore → architect proceeds without error
2. Insights path works: insights → architect proceeds without insufficient-data warning
3. Quick-only path triggers warning: quick-explore → architect warns about insufficient depth
4. Critic routing validated: research → REVISE_DATA → spawns full explore (not quick-explore)
5. Help documentation reflects all renamed commands and new commands

**Plans**: TBD

Plans:
- [ ] 14-01: TBD during planning

### 📋 v2.0 Advanced Features (Planned)

**Milestone Goal:** MLflow integration, DVC integration, multi-user support, web UI, red-teaming mode, automatic data profiling

**Phases:** 15+ (to be defined)

## Progress

**Execution Order:**
Phases execute in numeric order: 10 → 11 → 12 → 13 → 14 → 15...

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1-9. v1.0 MVP | v1.0 | 39/39 | Complete | 2026-01-30 |
| 10. Command Cleanup | v1.1 | 2/2 | Complete | 2026-01-31 |
| 11. Terminology Rename | v1.1 | 3/3 | Complete | 2026-01-31 |
| 12. Quick Explore | v1.1 | 3/3 | Complete | 2026-02-01 |
| 13. Accessible Insights | v1.1 | 0/? | Not started | - |
| 14. Integration Testing | v1.1 | 0/? | Not started | - |
