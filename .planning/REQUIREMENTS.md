# Requirements: Get Research Done (GRD)

**Defined:** 2026-01-27
**Core Value:** Structured ML experimentation with scientific rigor — from hypothesis to validated conclusion

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Branding & Installation

- [x] **BRAND-01**: Rename GSD → GRD in all files, commands, and references
- [x] **BRAND-02**: Create new ASCII art logo for GRD CLI branding
- [x] **BRAND-03**: Update npm package name to get-research-done
- [x] **BRAND-04**: Update README and installation documentation

### Data Reconnaissance (Explorer Phase)

- [x] **DATA-01**: Explorer agent analyzes raw data and surfaces anomalies
- [x] **DATA-02**: Explorer generates DATA_REPORT.md with structured output
- [x] **DATA-03**: Explorer detects potential data leakage (feature/target overlap, temporal issues)
- [x] **DATA-04**: Explorer profiles data distributions (class imbalance, outliers, statistics)

### Hypothesis Synthesis (Architect Phase)

- [x] **HYPO-01**: Architect role transforms data insights + goals into testable hypothesis
- [x] **HYPO-02**: OBJECTIVE.md template with context, hypothesis, metrics, constraints, baselines
- [x] **HYPO-03**: Hypothesis must include falsification criteria (what would disprove it)
- [x] **HYPO-04**: Baseline enforcement — cannot claim improvement without defined baseline

### Recursive Validation Loop

- [x] **LOOP-01**: Researcher agent implements experiments and produces code/notebooks
- [x] **LOOP-02**: Critic agent audits work with exit codes (PROCEED/REVISE_METHOD/REVISE_DATA)
- [x] **LOOP-03**: State router implements conditional branching based on Critic exit codes
- [x] **LOOP-04**: REVISE_METHOD routes back to Researcher with critique feedback
- [x] **LOOP-05**: REVISE_DATA routes back to Explorer for data re-verification
- [x] **LOOP-06**: Evaluator agent runs quantitative benchmarks and produces SCORECARD.json
- [x] **LOOP-07**: Experiment versioning creates isolated run_NNN/ directories per iteration

### Human Evaluation Gate

- [ ] **HUMAN-01**: Evidence Package bundles OBJECTIVE + DATA_REPORT + CRITIC_LOGS + SCORECARD
- [ ] **HUMAN-02**: Decision gate prompts human for Seal/Iterate/Archive decision
- [ ] **HUMAN-03**: Decision log tracks human decisions with rationale in decision_log.md

### Notebook Support

- [ ] **NOTE-01**: System can execute Jupyter notebooks as experiments
- [ ] **NOTE-02**: Explicit graduation path from exploratory notebooks to validated scripts
- [ ] **NOTE-03**: Clear separation between exploration/ and validated/ code

### State & Configuration

- [x] **STATE-01**: STATE.md tracks current phase, active run, loop history
- [x] **STATE-02**: Config system for workflow preferences (inherited from GSD)
- [x] **STATE-03**: Context restoration for resuming work across sessions

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### ML Tooling Integration

- **TOOL-01**: MLflow integration for experiment tracking and metrics logging
- **TOOL-02**: DVC integration for data versioning with Git
- **TOOL-03**: Jupytext support for notebook versioning (.py sync)
- **TOOL-04**: Great Expectations integration for data validation

### Advanced Features

- **ADV-01**: Multi-user support with shared experiment registry
- **ADV-02**: Web UI for experiment visualization
- **ADV-03**: Red-teaming mode for Critic (adversarial validation)
- **ADV-04**: Automatic data profiling with statistical tests

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Requirements traceability (REQ-ID mapping) | Replaced by hypothesis-driven structure |
| Milestone/release system (v1/v2) | Research doesn't ship versions, it validates hypotheses |
| Software-specific agents (code mappers, integration checkers) | Keep only research-relevant agents |
| Feature-based planning | Hypotheses aren't features |
| Auto-tuning hyperparameters | Removes researcher agency, hides understanding |
| Cloud-only storage | Excludes on-prem/air-gapped researchers |
| Built-in model training | Opinionated about frameworks, not extensible |
| GUI-first design | CLI researchers won't adopt, not scriptable |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BRAND-01 | Phase 1 | Complete |
| BRAND-02 | Phase 1 | Complete |
| BRAND-03 | Phase 1 | Complete |
| BRAND-04 | Phase 1 | Complete |
| STATE-01 | Phase 1 | Complete |
| STATE-02 | Phase 1 | Complete |
| STATE-03 | Phase 1 | Complete |
| DATA-01 | Phase 2 | Complete |
| DATA-02 | Phase 2 | Complete |
| DATA-03 | Phase 2 | Complete |
| DATA-04 | Phase 2 | Complete |
| HYPO-01 | Phase 3 | Complete |
| HYPO-02 | Phase 3 | Complete |
| HYPO-03 | Phase 3 | Complete |
| HYPO-04 | Phase 3 | Complete |
| LOOP-01 | Phase 4 | Complete |
| LOOP-02 | Phase 4 | Complete |
| LOOP-03 | Phase 4 | Complete |
| LOOP-04 | Phase 4 | Complete |
| LOOP-05 | Phase 4 | Complete |
| LOOP-06 | Phase 4 | Complete |
| LOOP-07 | Phase 4 | Complete |
| HUMAN-01 | Phase 5 | Pending |
| HUMAN-02 | Phase 5 | Pending |
| HUMAN-03 | Phase 5 | Pending |
| NOTE-01 | Phase 6 | Pending |
| NOTE-02 | Phase 6 | Pending |
| NOTE-03 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 25 total
- Mapped to phases: 25
- Unmapped: 0 ✓

---
*Requirements defined: 2026-01-27*
*Last updated: 2026-01-30 after Phase 4 completion*
