# Requirements: GRD v1.2 Command Unification

**Defined:** 2026-02-01
**Core Value:** Establish GRD as a clean, research-native CLI with experiment-based terminology and fresh version history

## v1.2 Requirements

Requirements for Command Unification milestone. Each maps to roadmap phases.

### Command Renames

- [ ] **RENAME-01**: Rename `plan-phase` to `design-experiment` (file, content, help.md)
- [ ] **RENAME-02**: Rename `execute-phase` to `run-experiment` (file, content, help.md)
- [ ] **RENAME-03**: Rename `discuss-phase` to `scope-experiment` (file, content, help.md)
- [ ] **RENAME-04**: Rename `verify-work` to `validate-results` (file, content, help.md)
- [ ] **RENAME-05**: Rename `research-phase` to `literature-review` (file, content, help.md)
- [ ] **RENAME-06**: Rename `list-phase-assumptions` to `list-experiment-assumptions` (file, content, help.md)
- [ ] **RENAME-07**: Rename `add-phase` to `add-experiment` (file, content, help.md)
- [ ] **RENAME-08**: Rename `insert-phase` to `insert-experiment` (file, content, help.md)
- [ ] **RENAME-09**: Rename `remove-phase` to `remove-experiment` (file, content, help.md)

### Command Chaining Fixes

- [ ] **CHAIN-01**: Update `new-study` to route to `design-experiment` (not `plan-phase`)
- [ ] **CHAIN-02**: Replace all `audit-milestone` references with `audit-study`
- [ ] **CHAIN-03**: Replace all `complete-milestone` references with `complete-study`
- [ ] **CHAIN-04**: Replace all `new-milestone` references with `new-study`
- [ ] **CHAIN-05**: Add explicit route from `evaluate` Seal decision to `graduate`
- [ ] **CHAIN-06**: Standardize flag `--gaps-only` to `--gaps` everywhere

### Artifact Updates

- [ ] **ARTIFACT-01**: Update STATE.md template to track experiments instead of phases
- [ ] **ARTIFACT-02**: Update ROADMAP.md terminology (phase -> experiment, milestone -> study)
- [ ] **ARTIFACT-03**: Update help.md with complete new command reference
- [ ] **ARTIFACT-04**: Update all "Next Up" sections across all 33 command files

### Version History Reset

- [ ] **VERSION-01**: Reset PROJECT.md - remove v1.0/v1.1 references, start fresh as GRD 1.0
- [ ] **VERSION-02**: Reset STATE.md - clear milestone history table, reset to clean GRD state
- [ ] **VERSION-03**: Archive or remove MILESTONES.md - GSD-era history not relevant to GRD
- [ ] **VERSION-04**: Update package.json version to reflect GRD 1.0 (not continuation of GSD)
- [ ] **VERSION-05**: Clean up "Validated" requirements - reframe as GRD baseline, not GSD history

### Documentation

- [ ] **DOC-01**: Update PROJECT.md as clean GRD project document
- [ ] **DOC-02**: Update any inline command references in agent system prompts
- [ ] **DOC-03**: Verify all command flows work end-to-end

## Future Requirements

Deferred to future milestone. Not in v1.2 scope.

### Potential v2.0 Features

- **FUTURE-01**: MLflow integration for experiment tracking
- **FUTURE-02**: DVC integration for data versioning
- **FUTURE-03**: Multi-user support with shared experiment registry

## Out of Scope

Explicitly excluded from v1.2. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Backward compatibility aliases | User chose clean break; simpler implementation |
| ROADMAP.md deprecation | User chose keep and update terminology |
| New commands | v1.2 is rename/fix only, no new functionality |
| Agent system prompt renames | Keep grd-* prefixes, only change command names |
| Preserving GSD version history | Clean break - GRD starts fresh at 1.0 |
| Git history rewrite | Keep git commits, just update planning docs |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| RENAME-01 | Phase 15 | Pending |
| RENAME-02 | Phase 15 | Pending |
| RENAME-03 | Phase 15 | Pending |
| RENAME-04 | Phase 15 | Pending |
| RENAME-05 | Phase 15 | Pending |
| RENAME-06 | Phase 15 | Pending |
| RENAME-07 | Phase 15 | Pending |
| RENAME-08 | Phase 15 | Pending |
| RENAME-09 | Phase 15 | Pending |
| CHAIN-01 | Phase 16 | Pending |
| CHAIN-02 | Phase 16 | Pending |
| CHAIN-03 | Phase 16 | Pending |
| CHAIN-04 | Phase 16 | Pending |
| CHAIN-05 | Phase 16 | Pending |
| CHAIN-06 | Phase 16 | Pending |
| ARTIFACT-01 | Phase 17 | Pending |
| ARTIFACT-02 | Phase 17 | Pending |
| ARTIFACT-03 | Phase 17 | Pending |
| ARTIFACT-04 | Phase 17 | Pending |
| VERSION-01 | Phase 18 | Pending |
| VERSION-02 | Phase 18 | Pending |
| VERSION-03 | Phase 18 | Pending |
| VERSION-04 | Phase 18 | Pending |
| VERSION-05 | Phase 18 | Pending |
| DOC-01 | Phase 19 | Pending |
| DOC-02 | Phase 19 | Pending |
| DOC-03 | Phase 19 | Pending |

**Coverage:**
- v1.2 requirements: 27 total
- Mapped to phases: 27
- Unmapped: 0

---
*Requirements defined: 2026-02-01*
*Last updated: 2026-02-01 after roadmap creation*
