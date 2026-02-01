# Requirements: GRD v1.1 Research UX Refinement

**Defined:** 2026-01-30
**Core Value:** Structured ML experimentation with scientific rigor — from hypothesis to validated conclusion, with a Critic agent enforcing skepticism at every step.

## v1.1 Requirements

Requirements for Research UX Refinement milestone. Each maps to roadmap phases.

### Command Cleanup

- [x] **CLEAN-01**: Delete 32 duplicate " 2.md" skill files from skills directory
- [x] **CLEAN-02**: Remove `audit-milestone` command (GSD-specific, not research-relevant)
- [x] **CLEAN-03**: Remove `plan-milestone-gaps` command (GSD-specific, not research-relevant)
- [x] **CLEAN-04**: Update help.md documentation to reflect all command changes

### Terminology Rename

- [x] **TERM-01**: Rename `new-milestone` → `new-study`
- [x] **TERM-02**: Rename `complete-milestone` → `complete-study`
- [x] **TERM-03**: Rename `discuss-phase` → `scope-study`
- [x] **TERM-04**: Rename `plan-phase` → `plan-study`
- [x] **TERM-05**: Rename `execute-phase` → `run-study`
- [x] **TERM-06**: Rename `verify-work` → `validate-study`
- [x] **TERM-07**: Update all internal references in skill files, agent prompts, and documentation

### Quick Explore

- [x] **QUICK-01**: Create `/grd:quick-explore` command as mode variant of Explorer agent
- [x] **QUICK-02**: Execute full analysis in <60 seconds (skip thorough leakage detection)
- [x] **QUICK-03**: Output summary statistics (row count, column types, missing values percentage)
- [x] **QUICK-04**: Highlight distribution patterns (skewness indicators, outlier flags)
- [x] **QUICK-05**: Output formatted summary to console (markdown-compatible)

### Accessible EDA (Insights)

- [ ] **INSIGHT-01**: Create `/grd:insights` command for business analyst audience
- [ ] **INSIGHT-02**: Generate full technical DATA_REPORT.md (saved to file, not displayed in chat)
- [ ] **INSIGHT-03**: Generate plain English summary where every statistic is explained in context
- [ ] **INSIGHT-04**: Provide actionable recommendations based on data characteristics
- [ ] **INSIGHT-05**: Generate LLM prompts for further exploration (copy-paste ready for non-technical users)

## Future Requirements

Deferred to v1.2+ milestones. Tracked but not in current roadmap.

### MLflow Integration

- **MLFLOW-01**: Experiment tracking integration
- **MLFLOW-02**: Artifact logging from research loop

### DVC Integration

- **DVC-01**: Data versioning setup
- **DVC-02**: Pipeline tracking

### Advanced Features

- **ADV-01**: Multi-user support with shared experiment registry
- **ADV-02**: Web UI for experiment visualization
- **ADV-03**: Red-teaming mode for Critic (adversarial validation)
- **ADV-04**: Automatic data profiling with statistical tests
- **ADV-05**: Visual previews (ASCII charts, embedded images)
- **ADV-06**: Confidence indicators in plain language
- **ADV-07**: Causal language guardrails

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Full automated EDA libraries (ydata-profiling, Sweetviz) | Installation friction, HTML output doesn't fit terminal workflow |
| Dashboard/GUI | CLI-first philosophy, defer to v2.0+ |
| Natural language queries | Focus on output first, input later |
| Auto-tuning hyperparameters | Removes researcher agency |
| Cloud-only storage | Excludes on-prem/air-gapped researchers |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLEAN-01 | Phase 10 | Complete |
| CLEAN-02 | Phase 10 | Complete |
| CLEAN-03 | Phase 10 | Complete |
| CLEAN-04 | Phase 10 | Complete |
| TERM-01 | Phase 11 | Complete |
| TERM-02 | Phase 11 | Complete |
| TERM-03 | Phase 11 | Complete |
| TERM-04 | Phase 11 | Complete |
| TERM-05 | Phase 11 | Complete |
| TERM-06 | Phase 11 | Complete |
| TERM-07 | Phase 11 | Complete |
| QUICK-01 | Phase 12 | Complete |
| QUICK-02 | Phase 12 | Complete |
| QUICK-03 | Phase 12 | Complete |
| QUICK-04 | Phase 12 | Complete |
| QUICK-05 | Phase 12 | Complete |
| INSIGHT-01 | Phase 13 | Pending |
| INSIGHT-02 | Phase 13 | Pending |
| INSIGHT-03 | Phase 13 | Pending |
| INSIGHT-04 | Phase 13 | Pending |
| INSIGHT-05 | Phase 13 | Pending |

**Coverage:**
- v1.1 requirements: 21 total
- Mapped to phases: 21
- Complete: 16 (CLEAN-01-04, TERM-01-07, QUICK-01-05)
- Pending: 5 (INSIGHT-01-05)

**Note (2026-02-01):** Phase 12 complete. Quick explore verified with 5/5 success criteria passed.

---
*Requirements defined: 2026-01-30*
*Last updated: 2026-02-01 after phase reset*
