# Requirements: GRD v1.1 Research UX Refinement

**Defined:** 2026-01-30
**Core Value:** Structured ML experimentation with scientific rigor — from hypothesis to validated conclusion, with a Critic agent enforcing skepticism at every step.

## v1.1 Requirements

Requirements for Research UX Refinement milestone. Each maps to roadmap phases.

### Command Cleanup

- [ ] **CLEAN-01**: Delete 32 duplicate " 2.md" skill files from skills directory
- [ ] **CLEAN-02**: Remove `audit-milestone` command (GSD-specific, not research-relevant)
- [ ] **CLEAN-03**: Remove `plan-milestone-gaps` command (GSD-specific, not research-relevant)
- [ ] **CLEAN-04**: Update help.md documentation to reflect all command changes

### Terminology Rename

- [ ] **TERM-01**: Rename `new-milestone` to research-appropriate term (e.g., `new-objective` or `new-hypothesis`)
- [ ] **TERM-02**: Rename `plan-phase` to research-appropriate term (e.g., `hypothesize` or `plan-experiment`)
- [ ] **TERM-03**: Rename other lifecycle commands to match GRD research terminology (discuss-phase, execute-phase, verify-work, etc.)
- [ ] **TERM-04**: Update all internal references in skill files, agent prompts, and documentation

### Quick Explore

- [ ] **QUICK-01**: Create `/grd:quick-explore` command as mode variant of Explorer agent
- [ ] **QUICK-02**: Execute full analysis in <60 seconds (skip thorough leakage detection)
- [ ] **QUICK-03**: Output summary statistics (row count, column types, missing values percentage)
- [ ] **QUICK-04**: Highlight distribution patterns (skewness indicators, outlier flags)
- [ ] **QUICK-05**: Output formatted summary to console (markdown-compatible)

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
| CLEAN-01 | TBD | Pending |
| CLEAN-02 | TBD | Pending |
| CLEAN-03 | TBD | Pending |
| CLEAN-04 | TBD | Pending |
| TERM-01 | TBD | Pending |
| TERM-02 | TBD | Pending |
| TERM-03 | TBD | Pending |
| TERM-04 | TBD | Pending |
| QUICK-01 | TBD | Pending |
| QUICK-02 | TBD | Pending |
| QUICK-03 | TBD | Pending |
| QUICK-04 | TBD | Pending |
| QUICK-05 | TBD | Pending |
| INSIGHT-01 | TBD | Pending |
| INSIGHT-02 | TBD | Pending |
| INSIGHT-03 | TBD | Pending |
| INSIGHT-04 | TBD | Pending |
| INSIGHT-05 | TBD | Pending |

**Coverage:**
- v1.1 requirements: 18 total
- Mapped to phases: 0
- Unmapped: 18

---
*Requirements defined: 2026-01-30*
*Last updated: 2026-01-30 after initial definition*
