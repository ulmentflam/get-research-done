# Roadmap: Get Research Done (GRD)

## Milestones

- v1.0 MVP - Phases 1-9 (shipped 2026-01-30)
- v1.1 Research UX Refinement - Phases 10-14 (shipped 2026-02-01)
- **v1.2 Command Unification** - Phases 15-19 (active)

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

### v1.2 Command Unification (Phases 15-19) - ACTIVE

**Milestone Goal:** Transform all lifecycle commands from software-dev terminology (phases, milestones, roadmaps) to research-native terminology (experiments, studies, protocols) with correct command chaining.

**Requirements:** 27 total across 5 categories

---

#### Phase 15: Command Renames

**Goal:** All phase-related commands use experiment terminology consistently

**Dependencies:** None (foundation phase)

**Requirements:** RENAME-01, RENAME-02, RENAME-03, RENAME-04, RENAME-05, RENAME-06, RENAME-07, RENAME-08, RENAME-09

**Plans:** 4 plans

Plans:
- [x] 15-01-PLAN.md — Rename core workflow commands (plan-phase, execute-phase, discuss-phase)
- [x] 15-02-PLAN.md — Rename verification and research commands (verify-work, research-phase, list-phase-assumptions)
- [x] 15-03-PLAN.md — Rename roadmap management commands (add-phase, insert-phase, remove-phase)
- [x] 15-04-PLAN.md — Update help.md and final verification

**Success Criteria:**
1. User can run `design-experiment` instead of `plan-phase` and it functions identically
2. User can run `run-experiment` instead of `execute-phase` and it functions identically
3. User can run all 9 renamed commands (`design-experiment`, `run-experiment`, `scope-experiment`, `validate-results`, `literature-review`, `list-experiment-assumptions`, `add-experiment`, `insert-experiment`, `remove-experiment`) and each produces expected output
4. The `help` command shows all new experiment-based command names with correct descriptions

---

#### Phase 16: Command Chaining Fixes

**Goal:** Commands route to each other correctly using new terminology throughout the workflow

**Dependencies:** Phase 15 (renames must exist before chaining can reference them)

**Requirements:** CHAIN-01, CHAIN-02, CHAIN-03, CHAIN-04, CHAIN-05, CHAIN-06

**Plans:** 2 plans

Plans:
- [ ] 16-01-PLAN.md — Replace milestone terminology with study equivalents in routing (audit-study, complete-study, new-study)
- [ ] 16-02-PLAN.md — Add evaluate->graduate route for Seal decision and standardize --gaps flag

**Success Criteria:**
1. Running `new-study` suggests `design-experiment` as next step (not `plan-phase`)
2. Running `evaluate` with Seal decision explicitly suggests `graduate` as next step
3. All references to `audit-milestone`, `complete-milestone`, and `new-milestone` have been replaced with study equivalents
4. The `--gaps` flag works consistently across all commands that support it (no `--gaps-only` variants)

---

#### Phase 17: Artifact Updates

**Goal:** All artifact templates and references use consistent research terminology

**Dependencies:** Phase 16 (chaining determines what artifacts suggest)

**Requirements:** ARTIFACT-01, ARTIFACT-02, ARTIFACT-03, ARTIFACT-04

**Success Criteria:**
1. STATE.md template tracks experiments (not phases) with appropriate fields
2. ROADMAP.md uses study/experiment terminology consistently (no phase/milestone mixed usage)
3. The `help.md` file contains complete and accurate command reference for all renamed commands
4. All 33 command files have "Next Up" sections that reference the correct new command names

---

#### Phase 18: Version History Reset

**Goal:** GRD presents as a clean v1.0 product, not a continuation of GSD history

**Dependencies:** Phase 17 (artifacts must be updated before resetting version references)

**Requirements:** VERSION-01, VERSION-02, VERSION-03, VERSION-04, VERSION-05

**Success Criteria:**
1. PROJECT.md presents GRD as a fresh v1.0 product with no v1.0/v1.1 GSD references
2. STATE.md has no GSD milestone history, only GRD baseline state
3. package.json version reflects GRD 1.0 (not a continuation version)
4. MILESTONES.md is archived or removed (GSD history separated from GRD documentation)
5. "Validated" requirements are reframed as GRD baseline capabilities, not GSD migration artifacts

---

#### Phase 19: Documentation & Testing

**Goal:** All documentation reflects final state and command flows work end-to-end

**Dependencies:** Phases 15-18 (all changes must be complete before final validation)

**Requirements:** DOC-01, DOC-02, DOC-03

**Success Criteria:**
1. PROJECT.md is a clean, accurate GRD project document with no legacy terminology
2. All agent system prompts reference correct command names (no stale `plan-phase` references)
3. The complete workflow (`new-study` -> `design-experiment` -> `run-experiment` -> `validate-results` -> `complete-study`) can be executed end-to-end without broken command suggestions

---

## Progress

**Execution Order:**
Phases execute in numeric order: 15 -> 16 -> 17 -> 18 -> 19

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1-9. v1.0 MVP | v1.0 | 39/39 | Complete | 2026-01-30 |
| 10-14. v1.1 Research UX | v1.1 | 13/13 | Complete | 2026-02-01 |
| 15. Command Renames | v1.2 | 4/4 | Complete | 2026-02-02 |
| 16. Command Chaining | v1.2 | 0/2 | Not started | - |
| 17. Artifact Updates | v1.2 | 0/? | Not started | - |
| 18. Version History Reset | v1.2 | 0/? | Not started | - |
| 19. Documentation & Testing | v1.2 | 0/? | Not started | - |
