# Get Research Done (GRD)

## What This Is

A recursive, agentic framework for machine learning research that brings structured rigor to hypothesis validation. GRD is a Claude Code workflow tool for ML researchers, evolving from the Get Shit Done (GSD) philosophy but optimized for the non-linear, data-dependent nature of AI research. The system provides a complete research loop: Data Reconnaissance → Hypothesis Synthesis → Recursive Validation → Human Evaluation, with automatic routing between phases based on Critic verdicts. Now includes fast EDA paths (quick-explore, insights) for rapid data familiarization.

## Core Value

Structured ML experimentation with scientific rigor — from hypothesis to validated conclusion, with a Critic agent enforcing skepticism at every step.

## Current State

**Version:** v1.2 (shipped 2026-02-02)
**Codebase:** ~68,000 LOC (Markdown, TypeScript, Python)
**Tech stack:** Claude Code hooks, MCP integration, papermill notebook execution, Rich console formatting

**Shipped capabilities:**
- `/grd:explore` — Data reconnaissance with hardware profiling and leakage detection
- `/grd:quick-explore` — Fast EDA with Rich console output for quick decisions (v1.1)
- `/grd:insights` — Plain English data insights for business analysts (v1.1)
- `/grd:architect` — Hypothesis synthesis with testable OBJECTIVE.md generation
- `/grd:research` — Recursive validation loop with Researcher/Critic/Evaluator agents
- `/grd:evaluate` — Human decision gate with evidence packages
- `/grd:graduate` — Notebook-to-script graduation path
- Experiment-based lifecycle commands: new-study, design-experiment, run-experiment, validate-results, complete-study (v1.2)
- Research-native command terminology: 9 commands renamed to experiment/study vocabulary (v1.2)
- Integration test suite: 23 automated tests validate command chains (v1.2)

## Philosophy

- **Hypothesis over Features**: We don't build features; we test hypotheses
- **Data-First**: No research objective is set without initial Exploratory Data Analysis (EDA)
- **The Recursive Loop**: Self-correcting system — if results contradict the data profile, the agentic loop forces return to the data layer
- **Critic-Led Rigor**: Automated Critic agent acts as scientific skeptic to prevent overfitting, data leakage, and logical fallacies
- **Progressive Exploration**: Start fast (quick-explore) → add depth (insights/explore) → formalize hypothesis (architect)

## Requirements

### Validated

- ✓ GRD branding with ASCII art and npm package — v1.0
- ✓ Explorer agent with data profiling and leakage detection — v1.0
- ✓ Architect agent with hypothesis synthesis — v1.0
- ✓ Recursive validation loop (Researcher/Critic/Evaluator) — v1.0
- ✓ Human evaluation gate with decision logging — v1.0
- ✓ Notebook execution and graduation path — v1.0
- ✓ REVISE_DATA auto-routing — v1.0
- ✓ Baseline experiment orchestration — v1.0
- ✓ Hardware profiling and long-running experiment support — v1.0
- ✓ GSD command cleanup — Remove/repurpose commands that don't fit research workflows — v1.1
- ✓ Research terminology — Rename phase/milestone concepts to match research style — v1.1
- ✓ Quick explore — Fast EDA producing summary for quick decisions — v1.1
- ✓ Accessible EDA — Plain English insights for business analysts (no code, no jargon) — v1.1
- ✓ Experiment terminology — Renamed 9 commands to research-native vocabulary (design-experiment, run-experiment, etc.) — v1.2
- ✓ Command chaining — new-study→design-experiment→run-experiment→validate-results→complete-study workflow — v1.2
- ✓ Template updates — STATE.md and ROADMAP.md use experiment/study terminology — v1.2
- ✓ Version history reset — CHANGELOG.md presents GRD as fresh product with GSD acknowledgment — v1.2
- ✓ Integration tests — 23 automated tests validate command renames and chains — v1.2

### Active

**v1.3 Branding & Gemini Integration**

- [ ] Update SVG assets with GRD branding (logo, terminal preview)
- [ ] Regenerate PNG from updated SVG
- [ ] Cherry-pick Gemini CLI from upstream GSD
- [ ] Adapt Gemini CLI for GRD terminology and workflows

### Future

- [ ] MLflow integration for experiment tracking
- [ ] DVC integration for data versioning
- [ ] Multi-user support with shared experiment registry
- [ ] Web UI for experiment visualization
- [ ] Red-teaming mode for Critic (adversarial validation)
- [ ] Automatic data profiling with statistical tests
- [ ] Visual previews (ASCII charts, embedded images)
- [ ] Confidence indicators in plain language

### Out of Scope

- Requirements traceability (REQ-ID mapping) — replaced by hypothesis-driven structure
- Milestone/release system (v1/v2) — research doesn't ship versions, it validates hypotheses
- Software-specific agents (code mappers, integration checkers) — keep only research-relevant agents
- Feature-based planning — hypotheses aren't features
- Auto-tuning hyperparameters — removes researcher agency, hides understanding
- Cloud-only storage — excludes on-prem/air-gapped researchers
- Built-in model training — opinionated about frameworks, not extensible
- GUI-first design — CLI researchers won't adopt, not scriptable
- Full automated EDA libraries (ydata-profiling, Sweetviz) — Installation friction, HTML output doesn't fit terminal workflow

## Context

**Existing codebase:** This is now a mature project with three shipped milestones. The v1.2 codebase has:
- Claude Code hooks for workflow automation
- Agent spawning system for specialized tasks (Explorer, Architect, Researcher, Critic, Evaluator, Graduator)
- Workflow orchestration via skill files (32 commands with study-centric terminology)
- State tracking and context restoration
- Template system for artifacts (DATA_REPORT.md, OBJECTIVE.md, SCORECARD.json, etc.)
- Notebook execution via papermill with graduation validation
- Hardware profiling for reproducibility
- Fast EDA paths with Rich console formatting (quick-explore, insights)
- Plain English insights generation with actionable recommendations

**Target audience:** ML researchers who need structure for experimentation without the overhead of product management tooling.

**Key insight:** Research is recursive, not linear. The Critic agent's ability to force loops back to earlier phases (REVISE_DATA sends back to Explorer) is the core innovation over GSD's linear phase progression.

## The GRD Lifecycle

### Phase 1: Data Reconnaissance (Explorer)
- **Input:** Raw Dataset + High-level Project Goal
- **Output:** `DATA_REPORT.md` (distributions, anomalies, leakage risks, baseline signals, hardware profile)
- **Fast paths:** `/grd:quick-explore` (summary output), `/grd:insights` (plain English)

### Phase 2: Hypothesis Synthesis (Architect)
- **Input:** DATA_REPORT.md + Project Goal
- **Output:** `OBJECTIVE.md` (testable hypothesis with falsification criteria)
- **Note:** Warns if only quick-explore data available; recommends full explore for production

### Phase 3: Recursive Agentic Loop
1. **Researcher** develops code, training pipelines, experimental setups
2. **Critic** audits work with three exit paths:
   - `PROCEED`: Logic sound, results align with data profile → Evaluator
   - `REVISE_METHOD`: Logical error, bad hyperparams → back to Researcher
   - `REVISE_DATA`: Anomalous results, potential leakage → back to Explorer (auto-spawned)
3. **Evaluator** runs standardized benchmark suite

### Phase 4: Human Evaluation (Decision Gate)
- **Evidence Package:** OBJECTIVE.md + DATA_REPORT.md + CRITIC_LOGS.md + SCORECARD.json
- **Decisions:** Seal (proven) / Iterate (refine) / Archive (disproven)

## Agent Roles

| Role | Responsibility | Primary Output |
|------|----------------|----------------|
| Explorer | Uncover the "truth" of the data before coding | `DATA_REPORT.md` |
| Architect | Turn goals into testable, scientific hypotheses | `OBJECTIVE.md` |
| Researcher | Implementation, experimentation, optimization | `experiment_scripts/` |
| Critic | Skepticism, finding data leaks, logical red-teaming | `CRITIC_LOG.md` |
| Evaluator | Quantitative benchmarking against objective | `SCORECARD.json` |
| Graduator | Notebook-to-script conversion with validation | `src/experiments/` |

## Folder Structure

```
.
├── PROJECT_GOAL.md       # North Star vision
├── OBJECTIVE.md          # Active hypothesis being tested
├── reports/
│   └── DATA_REPORT.md    # Living document of data insights
├── agents/               # System prompts for agent roles
│   ├── grd-explorer.md
│   ├── grd-architect.md
│   ├── grd-researcher.md
│   ├── grd-critic.md
│   ├── grd-evaluator.md
│   └── grd-graduator.md
├── experiments/          # Versioned history of every loop
│   └── run_001/
│       ├── code/         # Python scripts, configs, notebooks
│       ├── logs/         # Researcher vs. Critic argument logs
│       ├── data_check.md # Recorded if recursion to EDA occurred
│       └── scorecard.json
├── notebooks/
│   └── exploration/      # Exploratory notebooks (pre-graduation)
├── src/
│   ├── grd/              # Core GRD modules
│   │   ├── formatters.py # Rich console formatting
│   │   ├── quick.py      # Quick explore analysis
│   │   └── insights.py   # Plain English insights
│   └── experiments/      # Graduated validated scripts
└── human_eval/           # Narrative record of human decisions
    └── decision_log.md   # Why we pivoted or promoted a hypothesis
```

## Constraints

- **Tech stack**: Must remain Claude Code compatible (hooks, MCP integration)
- **Installation**: npm-based, same mechanism as GSD with new package name
- **Backward compatibility**: Not required — this is a clean break from GSD

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Recursive loop over linear phases | Research is non-linear; results often invalidate assumptions | ✓ Good |
| Critic agent with exit codes | Forces scientific rigor, prevents overfitting/leakage | ✓ Good |
| Data-first philosophy | Hypotheses must be grounded in data reality | ✓ Good |
| Human-in-the-loop gate | Prevents false positives, maintains research integrity | ✓ Good |
| LLM-powered Critic routing | More flexible than rule-based, handles edge cases | ✓ Good |
| Default 5 iteration limit with cycle detection | Prevents infinite loops, controls compute costs | ✓ Good |
| REVISE_DATA auto-spawn Explorer | Completes recursive automation, no manual intervention | ✓ Good |
| Session-level timeout approval | Prevents repeated prompts during long-running experiments | ✓ Good |
| Random seed as hard graduation requirement | Enforces reproducibility for notebook-to-script | ✓ Good |
| Study-centric terminology (v1.1) | Better matches research workflows than GSD naming | ✓ Good |
| Quick explore with warning (v1.1) | Enables fast iteration while preventing shallow analysis | ✓ Good |
| Inline Python for insights (v1.1) | Simpler than Jinja2 templates, easier to maintain | ✓ Good |
| Experiment-based command names (v1.2) | Eliminates software-dev vocabulary, research-native CLI | ✓ Good |
| External-only version reset (v1.2) | Clean product positioning while preserving internal context | ✓ Good |
| Intentional stale refs in agents (v1.2) | Deferred agent prompt updates to minimize scope | — Pending |

---
*Last updated: 2026-02-02 after v1.3 milestone started*
