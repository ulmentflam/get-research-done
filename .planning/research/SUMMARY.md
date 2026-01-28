# Project Research Summary

**Project:** GRD (Get Research Done)
**Domain:** ML Research Workflow Automation
**Researched:** 2026-01-27
**Confidence:** MEDIUM

## Executive Summary

GRD is a Claude Code workflow tool that transforms ML research from ad-hoc experimentation into hypothesis-driven validation with automated skepticism. Unlike existing tools (MLflow, Weights & Biases, DVC) that track *what happened*, GRD enforces *why it happened* and *whether it's valid* through a recursive validation loop with a Critic agent. The system operates through five specialized agents (Explorer, Architect, Researcher, Critic, Evaluator) coordinated by an orchestrator that routes workflow based on validation exit codes (PROCEED, REVISE_METHOD, REVISE_DATA).

The recommended approach extends GSD's proven Node.js + Markdown architecture with Python-based ML tooling integrations. Node.js handles orchestration (Claude Code compatibility), while Python ecosystem tools (MLflow for experiment tracking, DVC for data versioning, JupyterLab + Jupytext for notebook management) handle domain-specific operations via subprocess calls. The data-first philosophy mandates exploratory data analysis before hypothesis formation, preventing the #1 ML research pitfall: spending weeks on experiments with fundamental flaws.

Key risk: recursive loops can become infinite or hypothesis drift can occur. Mitigation requires maximum loop depth limits, hypothesis locking, and explicit human decision gates (Seal/Iterate/Archive) with structured evidence packages. The tool must make it harder to deceive yourself, not easier to ship models—insufficient skepticism is the root cause of most ML research failures (data leakage, metric fixation, ignoring negative results).

## Key Findings

### Recommended Stack

GRD's stack balances orchestration simplicity (GSD's Node.js foundation) with ML ecosystem power (Python tooling). The hybrid approach keeps workflow logic in JavaScript while delegating domain operations to Python, maintaining Claude Code compatibility while accessing best-in-class ML libraries.

**Core technologies:**
- **Node.js (>= 18.0.0)**: Orchestration runtime, inherits GSD's proven agent spawning patterns
- **MLflow (>= 2.9.0)**: Self-hosted experiment tracking with Python API, local `.mlruns` storage for MVP
- **DVC (>= 3.0.0)**: Git-like data versioning, separates metadata (Git) from artifacts (configurable storage)
- **JupyterLab + Jupytext (4.0+ / 1.15+)**: Interactive notebooks with `.py:percent` sync for Git versioning
- **uv + pyproject.toml**: Fast Python package management (10-100x pip), modern dependency locking
- **Great Expectations (>= 0.18.0)**: Declarative data validation to catch quality issues before training
- **Ruff + mypy**: Fast Python linting/formatting (Rust-based) and type checking for code quality

**Storage strategy:**
- Local-first for MVP: `.mlruns/` (MLflow), `.grd/artifacts/` (large files), `data/raw|processed|features/` (DVC-tracked)
- Scalability path: S3/GCS for remote artifacts, SQLite for experiment metadata search

**Version confidence note:** Stack recommendations based on 2024 knowledge cutoff. MLflow 2.9.x, DVC 3.x, uv 0.1+ were current—verify latest stable versions before implementation.

### Expected Features

**Must have (table stakes):**
- **Experiment versioning**: Every run tracked with code, hyperparameters, environment—minimum viable feature for adoption
- **Metric logging**: Loss curves, custom metrics, immediate comparison—researchers abandon tools without this
- **Data versioning**: DVC-based tracking to prevent "can't reproduce because data changed" scenarios
- **Reproducibility**: Environment capture (Python version, packages, CUDA) for exact re-runs
- **Local-first operation**: Must work offline/air-gapped for academic/corporate researchers on compute clusters
- **Notebook integration**: Auto-logging from Jupyter cells, standard ML research interface
- **CLI interface**: `grd run experiment.py` style commands for script-based workflows
- **Git integration**: Track commit hash per experiment, atomic commits per validation loop iteration

**Should have (competitive differentiators):**
- **Critic Agent (automated skepticism)**: Catches data leakage, overfitting, logical errors before wasted compute—core GRD innovation
- **Recursive validation loop**: REVISE_DATA exit code forces return to data layer when results contradict expectations
- **Hypothesis-driven structure**: OBJECTIVE.md replaces "let's try X" with testable claims and falsification criteria
- **Data-first philosophy**: Mandatory EDA (Explorer agent → DATA_REPORT.md) before hypothesis formation
- **Human-in-the-loop gates**: Explicit decision points (Seal/Iterate/Archive) with evidence packages prevent false positives
- **Baseline enforcement**: Must define baseline before claiming improvement prevents "5% better than random" claims
- **Exit code taxonomy**: PROCEED/REVISE_METHOD/REVISE_DATA provides structured feedback, not binary pass/fail
- **Experiment narratives**: Structured logs of *why* decisions were made, not just metrics

**Defer to v2+:**
- **Multi-user support**: Complex; single-researcher workflow must work first
- **Web UI**: CLI-first for researchers; dashboard nice-to-have
- **Model registry**: Advanced feature; file system sufficient for MVP
- **W&B integration**: Optional cloud sync; start with self-hosted MLflow
- **Red-teaming mode**: Enhanced Critic adversarial validation; basic skepticism first
- **Auto-tuning hyperparameters**: Removes researcher agency; suggest ranges instead
- **Built-in compute**: Can't compete with existing clusters; integrate, don't replace

**Anti-features (explicitly avoid):**
- GUI-first design, cloud-only storage, proprietary artifact formats, auto-deployment, leaderboards, "AI co-pilot" marketing, one-click reproducibility promises—these create lock-in, remove control, or overstate capabilities.

### Architecture Approach

GRD follows a layered architecture with recursive validation loops and specialized agent roles. The orchestration layer spawns agents with isolated contexts, routes workflow based on Critic exit codes, and manages file-based state persistence. Five agents (Explorer, Architect, Researcher, Critic, Evaluator) each have narrow responsibilities: data reconnaissance, hypothesis synthesis, implementation, skeptical validation, and quantitative benchmarking. Each recursive loop iteration creates a new `experiments/run_NNN/` directory with complete context (code, logs, outputs) for reproducibility. Human decision gates receive evidence packages (OBJECTIVE.md + DATA_REPORT.md + critique logs + scorecard) before marking hypotheses as validated/disproven/needs-iteration.

**Major components:**
1. **Orchestration Layer** — Workflow commands (slash commands), agent spawner (subagent API), state router (Critic exit code branching), decision gate (human checkpoints)
2. **Agent Execution Layer** — Explorer (EDA, leakage detection), Architect (hypothesis synthesis), Researcher (implementation), Critic (validation with exit codes), Evaluator (metrics, scorecard generation)
3. **Artifact Layer** — DATA_REPORT.md (living EDA document), experiments/run_NNN/* (versioned snapshots), reports & logs (audit trail)
4. **Persistence Layer** — File-based state (OBJECTIVE.md, STATE.md), Git tracking (atomic commits per iteration), config store (.planning/config.json)

**Key patterns:**
- **Recursive validation loop**: Critic routes backward (REVISE_DATA → Explorer, REVISE_METHOD → Researcher) when anomalies detected
- **Data-first gating**: No hypothesis without DATA_REPORT.md—enforced by orchestrator
- **Versioned isolation**: Each iteration gets new run_NNN/ directory with full context
- **Evidence packages**: Bundle all context for human decisions
- **Role separation**: Agents receive only relevant context (Explorer gets raw data, Critic gets experimental results)

### Critical Pitfalls

**1. Data Leakage Through Tool Convenience**
- **Risk**: Auto-generated train/test splits hide temporal dependencies, future information in features, test set contamination during normalization
- **Prevention**: Explorer must document temporal dependencies; Critic validates splits, checks feature/target overlap, enforces data freeze on test sets; explicit data provenance tracking required before any split
- **Phase mapping**: Phase 1 (Explorer documents leakage risks), Phase 3 (Critic validates splits before training)

**2. Experiment Versioning Without Hypothesis Versioning**
- **Risk**: 200 experiment folders with no narrative, can't reproduce thought process, redundant experiments, paper writing requires "archaeology"
- **Prevention**: Every run_NNN/ must contain HYPOTHESIS.md stating belief, rationale, falsification criteria; DECISION_LOG.md tracks "based on experiment N, we decided X because Y"; Critic rejects experiments without stated hypothesis
- **Phase mapping**: Phase 2 (Architect creates testable hypothesis), Phase 3 (each iteration references hypothesis), Phase 4 (evidence package shows hypothesis→experiment→result chain)

**3. Metric Fixation Without Distribution Validation**
- **Risk**: Optimize single scalars (accuracy, F1) without checking data distribution—95% accuracy on shifted/cherry-picked distribution
- **Prevention**: Explorer documents class balance, outliers, subgroups, drift before any modeling; Evaluator reports stratified metrics (by quantile, subgroup, confidence bins), not aggregates; automatic warnings for high subgroup variance
- **Phase mapping**: Phase 1 (Explorer profiles distributions), Phase 2 (Architect defines metrics appropriate to distribution), Phase 3 (Evaluator reports stratified results)

**4. Notebook-to-Production Graduation Without Refactor**
- **Risk**: Production code is wrapped notebook cells with hardcoded paths, global state, non-deterministic execution order
- **Prevention**: Explicit graduation gate distinguishes exploration notebooks (`experiments/exploration/`) from validated scripts (`experiments/validated/`); refactor checklist (no hardcoded paths, deterministic with seed control, configurable via parameters, unit tests); Critic won't mark notebooks as "complete"
- **Phase mapping**: Phase 3 (Researcher produces notebooks for exploration, but Evaluator requires scripts for benchmarking)

**5. Ignoring Negative Results**
- **Risk**: Failed experiments deleted/forgotten, repeated mistakes, publication bias, loss of scientific knowledge
- **Prevention**: "Hypothesis disproven" is valid outcome; when Critic returns REVISE_METHOD/REVISE_DATA, reason logged; failed experiments archived to `experiments/negative_results/` with explanation; decision log tracks failures; evaluation includes "what we tried that didn't work"
- **Phase mapping**: Phase 3 (Critic exit codes capture failure modes), Phase 4 (evidence package includes negative results with lessons learned)

**GRD-specific risks:**
- **Infinite recursive loops**: Maximum 3 loops, force new information requirement, human escalation
- **Adversarial Critic theater**: Exit codes need actionable feedback, false positive tracking
- **Hypothesis drift**: Lock original in OBJECTIVE.md, track modifications, human gate checks "did we answer original question?"
- **EDA busywork**: Focus Explorer on *anomalies* and *risks*, not comprehensive statistics; maximum report length

## Implications for Roadmap

Based on research, suggested phase structure follows component dependency chains and isolates complexity:

### Phase 1: Core Orchestration & State Management
**Rationale:** Foundation layer must exist before specialized agents can function. GSD's orchestration patterns are proven—adapt for GRD lifecycle (recursive loops vs linear tasks).
**Delivers:**
- Agent spawner with isolated contexts
- STATE.md extensions (loop_history, Critic verdicts, current_phase)
- File-based state persistence
- Basic slash command structure (`/grd:explore`, `/grd:validate`)
**Addresses:** Table stakes features (CLI interface, Git integration)
**Avoids:** Configuration sprawl (pitfall #10)—establish config schema early
**Research flag:** Minimal—GSD patterns are well-documented, direct adaptation

### Phase 2: Data-First Workflow (Explorer → Architect)
**Rationale:** Data-first philosophy is core differentiator; must work before adding complexity of recursive loops. Linear flow (Explorer → Architect) validates agent communication patterns.
**Delivers:**
- Explorer agent (DATA_REPORT.md generation, EDA scripts, leakage detection)
- Architect agent (OBJECTIVE.md synthesis from data + goals)
- Data-first gating (no hypothesis without DATA_REPORT.md)
**Addresses:** Differentiators (data-first philosophy, hypothesis-driven structure)
**Avoids:** Pitfall #1 (data leakage)—Explorer documents temporal dependencies, distribution characteristics
**Uses:** Python subprocess calls for EDA (pandas, matplotlib, seaborn)
**Research flag:** Medium complexity—needs research on effective leakage detection patterns, statistical profiling depth

### Phase 3: Recursive Validation Loop (Researcher ↔ Critic)
**Rationale:** Core innovation requiring foundation + basic agents. Most complex component—state machine logic, exit code routing, versioned experiment isolation.
**Delivers:**
- Researcher agent (implementation, Python scripts/notebooks)
- Critic agent (skeptical validation with exit codes)
- State router (PROCEED → Evaluator, REVISE_METHOD → Researcher, REVISE_DATA → Explorer)
- Experiment versioning (run_NNN/ directories with code, logs, outputs snapshots)
- Loop depth limits and convergence checks
**Addresses:** Differentiators (Critic agent, recursive loops, exit code taxonomy)
**Avoids:** Pitfall #2 (hypothesis versioning)—each run_NNN/ contains HYPOTHESIS.md snapshot
**Implements:** Recursive validation loop pattern (Architecture)
**Research flag:** High complexity—needs research on Critic validation depth (rule-based vs LLM-powered), exit code decision trees, infinite loop detection strategies

### Phase 4: Quantitative Evaluation & Human Gate
**Rationale:** Depends on experiments producing artifacts. Evaluation without human oversight leads to false positives (pitfall #4—metrics-only validation).
**Delivers:**
- Evaluator agent (scorecard.json generation, benchmark execution)
- Evidence package generator (bundles OBJECTIVE + DATA_REPORT + critique logs + scorecard)
- Human decision gate (interactive prompt: Seal/Iterate/Archive)
- decision_log.md tracking with rationale capture
**Addresses:** Differentiators (evidence packages, human-in-the-loop gates)
**Avoids:** Pitfall #3 (metric fixation)—Evaluator reports stratified metrics; Pitfall #6 (ignoring negatives)—Archive path preserves failed hypotheses
**Research flag:** Low complexity—patterns clear from research, mainly integration work

### Phase 5: ML Tooling Integration
**Rationale:** Enhances workflow with ecosystem tools. Can start simple (local file tracking) and add sophistication incrementally.
**Delivers:**
- MLflow integration (experiment logging via Python subprocess)
- DVC setup (data versioning initialization)
- JupyterLab + Jupytext config (notebook versioning)
- Great Expectations integration (data validation checkpoints)
**Addresses:** Table stakes (experiment versioning, data versioning, notebook integration, reproducibility)
**Avoids:** Pitfall #7 (random seed management)—comprehensive seed control; Pitfall #13 (data versioning)—DVC tracks data pipeline
**Uses:** Stack technologies (MLflow, DVC, Jupytext, Great Expectations)
**Research flag:** Medium complexity—needs research on MLflow Python API subprocess patterns, DVC remote storage config, Jupytext automation

### Phase 6: Notebook Graduation Path
**Rationale:** Addresses transition from exploratory notebooks to validated scripts. Enhancement to Researcher workflow—optional for MVP, improves usability.
**Delivers:**
- Notebook execution engine (papermill integration)
- Graduation checklist (refactor validation)
- experiments/exploration/ vs experiments/validated/ separation
- Notebook → .py conversion with seed control and parameterization
**Addresses:** Differentiators (notebook → production path)
**Avoids:** Pitfall #4 (notebook-to-production without refactor)
**Research flag:** Low complexity—papermill is well-documented, mainly workflow design

### Phase Ordering Rationale

- **Foundation first (Phase 1):** Orchestration must exist before agents can run
- **Linear before recursive (Phase 2 → 3):** Validate basic agent patterns before adding loop complexity
- **Validation before evaluation (Phase 3 → 4):** Critic must route to Evaluator; experiments must exist to evaluate
- **Core workflow before tooling (Phases 1-4 → 5):** Workflow can function with manual tracking; MLflow/DVC enhance but aren't blocking
- **Graduation last (Phase 6):** Depends on Researcher working; notebook support is UX polish

**Grouping logic:**
- Phase 1 isolates infrastructure complexity
- Phases 2-3-4 are the core research loop (must work end-to-end for MVP)
- Phases 5-6 enhance with ecosystem integrations and UX improvements

**Pitfall avoidance:**
- Phases 1-2 address data leakage and hypothesis versioning early (foundational issues)
- Phase 3 enforces recursive validation to catch metric fixation
- Phase 4 human gate prevents false positives
- Phases 5-6 add reproducibility safeguards (environment capture, seed control)

### Research Flags

Phases likely needing `/grd:research-phase` during planning:

- **Phase 2 (Explorer agent):** Complex—needs research on statistical profiling depth, leakage detection patterns (temporal/spatial/feature overlap), when to flag distribution anomalies vs report them
- **Phase 3 (Critic logic):** Complex—needs research on validation decision trees (what triggers REVISE_DATA vs REVISE_METHOD?), rule-based checks vs LLM reasoning depth, false positive minimization strategies
- **Phase 5 (MLflow/DVC integration):** Medium—needs research on subprocess orchestration patterns (Node.js → Python → MLflow API), DVC remote storage setup for team scaling, Great Expectations checkpoint configuration

Phases with standard patterns (can skip research-phase):

- **Phase 1 (Orchestration):** GSD architecture is proven, direct adaptation
- **Phase 4 (Evaluator):** Metrics computation is well-documented, mainly implementation
- **Phase 6 (Notebook graduation):** papermill and Jupytext patterns are established

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | MEDIUM | Core technologies (Node.js, Python, MLflow, DVC) are standard, but specific versions may have updated in 2025; uv is new (2024 release) so stability needs verification |
| Features | HIGH | Table stakes features validated against established tools (W&B, MLflow, DVC); differentiators grounded in GRD's documented design philosophy |
| Architecture | MEDIUM | GSD orchestration patterns are proven (HIGH), but recursive validation loop is novel (MEDIUM)—no direct precedents in training knowledge |
| Pitfalls | HIGH | Data leakage, metric fixation, notebook-to-production issues are well-documented ML engineering failures; GRD-specific risks are logical extrapolations |

**Overall confidence:** MEDIUM

### Gaps to Address

**Technology versions (MEDIUM urgency):**
- MLflow current version: Research based on 2.9.x (late 2024)—check for 3.x releases or API changes
- DVC current version: Research based on 3.x—verify latest stable
- uv stability: Released mid-2024, rapid adoption—verify API stability for production use, check if breaking changes in 0.2+
- Great Expectations: Research based on 0.18.x—may have 1.0 release, check for API changes

**Implementation details (HIGH urgency):**
- Critic decision logic: Rules vs LLM-powered reasoning? Training knowledge insufficient for optimal depth—needs prototyping during Phase 3 planning
- Infinite loop detection: Maximum 3 iterations is heuristic—needs empirical validation, may require escape hatch strategies
- MLflow subprocess patterns: Node.js orchestrating Python MLflow calls—verify error handling, async execution, environment isolation

**Integration scope (MEDIUM urgency):**
- Should GRD integrate with W&B/Neptune.ai or compete? Research flagged as "defer to v2+", but roadmap should clarify integration hooks vs native implementation
- Framework coverage: PyTorch-first or framework-agnostic from day 1? Research assumed both supported—needs decision on MVP scope
- Storage backend: SQLite for metadata catalog at what scale threshold? Research suggested "small team, <100 experiments"—validate assumptions

**Validation during implementation:**
- Critic false positive rate: Unknown until real usage—needs user feedback loop, potentially Phase 3 requires pilot testing
- Evidence package presentation: Interactive prompts vs web UI? Research assumed CLI, but human gate UX needs validation
- Hypothesis drift detection: Locked OBJECTIVE.md prevents drift, but how to handle legitimate hypothesis refinement? Needs decision criteria

**How to handle:**
- **Technology versions:** Flag for verification at Phase 5 planning (ML tooling integration)—can prototype with documented versions initially
- **Critic logic:** Flag for Phase 3 research-phase—prototype rule-based first, evaluate if LLM enhancement needed
- **Integration scope:** Clarify in roadmap introduction—MVP is standalone, v2+ adds integrations
- **Validation needs:** Build telemetry into MVP (Phase 4)—track Critic exit code frequency, loop iteration counts, human gate decision patterns

## Sources

### Primary (HIGH confidence)
- GSD existing codebase: /Users/evanowen/Library/Mobile Documents/com~apple~CloudDocs/Workspace/playground/get-research-done/.planning/codebase/ARCHITECTURE.md
- GRD PROJECT.md: /Users/evanowen/Library/Mobile Documents/com~apple~CloudDocs/Workspace/playground/get-research-done/.planning/PROJECT.md
- Established ML engineering principles: Data leakage patterns, train/test contamination, reproducibility requirements (training knowledge through Jan 2025)

### Secondary (MEDIUM confidence)
- MLflow architecture patterns: Experiment tracking, artifact storage, model registry (training knowledge, versions may have updated)
- Weights & Biases patterns: Run versioning, collaborative features (training knowledge)
- DVC patterns: Git-like data versioning, pipeline DAGs (training knowledge)
- JupyterLab + Jupytext: Notebook versioning approaches (training knowledge, stable patterns)

### Tertiary (LOW confidence—needs verification)
- uv package manager: Released 2024, rapid adoption—version stability and API changes need verification
- Great Expectations 0.18.x: May have 1.0 release in 2025—API changes possible
- MLflow 2.9.x: Current version unknown—may have 3.x releases with breaking changes
- PyTorch/TensorFlow versions: Rapidly evolving—training knowledge reflects 2.x/2.15+ but specific versions need verification

**Verification status:**
- WebSearch and Context7 unavailable during research session
- All findings based on training knowledge (cutoff January 2025)
- No external source verification for 2026 current state

**Recommended verification before implementation:**
- MLflow: https://mlflow.org/releases
- DVC: https://dvc.org/doc/install
- uv: https://github.com/astral-sh/uv/releases
- Great Expectations: https://docs.greatexpectations.io/

---
*Research completed: 2026-01-27*
*Ready for roadmap: yes*
