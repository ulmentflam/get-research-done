# Architecture Research: ML Research Workflow Systems

**Domain:** ML Research Workflow Tools
**Researched:** 2026-01-27
**Confidence:** MEDIUM

## Standard Architecture

### System Overview

ML research workflow systems follow a layered architecture with recursive validation loops. Based on analysis of MLflow, Weights & Biases, DVC, Metaflow, and existing GSD patterns:

```
┌─────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Workflow │  │  Agent   │  │  State   │  │ Decision │   │
│  │ Commands │  │ Spawner  │  │  Router  │  │   Gate   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │          │
├───────┴─────────────┴─────────────┴─────────────┴──────────┤
│                   AGENT EXECUTION LAYER                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Explorer │  │Architect │  │Researcher│  │  Critic  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │          │
│       └─────────────┴─────────────┴─────────────┘          │
│                          ↓                                  │
│              ┌─────────────────────┐                        │
│              │     Evaluator       │                        │
│              └─────────────────────┘                        │
├─────────────────────────────────────────────────────────────┤
│                   ARTIFACT LAYER                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │    Data    │  │Experiments │  │  Reports   │            │
│  │  Reports   │  │ (Versioned)│  │  & Logs    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
├─────────────────────────────────────────────────────────────┤
│                  PERSISTENCE LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ File-based │  │    Git     │  │   Config   │            │
│  │   State    │  │  Tracking  │  │   Store    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| **Workflow Commands** | User-facing entry points for lifecycle phases | Slash commands (`/grd:explore`, `/grd:validate`) |
| **Agent Spawner** | Creates isolated execution contexts for specialized agents | Subagent API with fresh context windows |
| **State Router** | Routes workflow based on Critic exit codes (PROCEED/REVISE_METHOD/REVISE_DATA) | State machine with conditional branching |
| **Decision Gate** | Human-in-the-loop validation checkpoint | Interactive prompts with Evidence Package presentation |
| **Explorer** | Data reconnaissance and profiling | EDA scripts, distribution analysis, leakage detection |
| **Architect** | Hypothesis synthesis from data + goals | Template-driven OBJECTIVE.md generation |
| **Researcher** | Experiment implementation and execution | Python scripts, notebook support, training pipelines |
| **Critic** | Skeptical validation with exit codes | Automated audit with three-path routing logic |
| **Evaluator** | Quantitative benchmarking | Metrics computation, scorecard generation |
| **Data Reports** | Living document of data insights | Markdown with statistics, visualizations, warnings |
| **Experiments** | Versioned experiment runs | Isolated directories (run_001/, run_002/) with code, logs, outputs |
| **Reports & Logs** | Audit trail of agent decisions | Markdown logs, Critic arguments, decision history |
| **File-based State** | Project memory across sessions | OBJECTIVE.md, DATA_REPORT.md, STATE.md |
| **Git Tracking** | Version control integration | Atomic commits per validation loop iteration |

## Recommended Project Structure

```
.
├── PROJECT_GOAL.md           # North Star vision (immutable)
├── OBJECTIVE.md              # Active hypothesis being tested
├── STATE.md                  # Current position in lifecycle
├── .planning/
│   ├── config.json           # Workflow preferences
│   └── research/             # Domain research for GRD itself
├── reports/
│   └── DATA_REPORT.md        # Living EDA document
├── agents/                   # System prompts (GRD-specific)
│   ├── explorer.prompt       # Data reconnaissance role
│   ├── architect.prompt      # Hypothesis synthesis role
│   ├── researcher.prompt     # Implementation role
│   ├── critic.prompt         # Validation role
│   └── evaluator.prompt      # Benchmarking role
├── experiments/              # Versioned experiment history
│   ├── run_001/
│   │   ├── code/            # Python scripts, notebooks, configs
│   │   │   ├── train.py
│   │   │   ├── config.yaml
│   │   │   └── notebook.ipynb
│   │   ├── logs/            # Researcher/Critic dialogue
│   │   │   ├── training.log
│   │   │   └── critique.md
│   │   ├── outputs/         # Model artifacts, predictions
│   │   │   ├── model.pkl
│   │   │   └── predictions.csv
│   │   ├── data_check.md    # Present if REVISE_DATA occurred
│   │   └── scorecard.json   # Evaluator benchmarks
│   └── run_002/             # Next iteration
└── human_eval/
    └── decision_log.md       # Human decisions (Seal/Iterate/Archive)
```

### Structure Rationale

- **reports/:** Living documents updated continuously as data understanding deepens (not versioned per run)
- **experiments/:** Immutable history — each run is a sealed snapshot for reproducibility
- **agents/:** Role definitions separate from implementation (system prompts, not code)
- **human_eval/:** Explicit human decision tracking (prevents false positives, maintains research integrity)

## Architectural Patterns

### Pattern 1: Recursive Validation Loop (Core Innovation)

**What:** Critic agent can route workflow backward to earlier phases based on anomalous results.

**When to use:** Always — this is GRD's defining pattern. Research is non-linear; results often invalidate assumptions.

**Trade-offs:**
- **Pro:** Prevents overfitting, data leakage, logical errors from propagating
- **Pro:** Self-correcting system aligns with scientific method
- **Con:** Can create long iteration cycles (feature, not bug)
- **Con:** Requires sophisticated state management to avoid loops

**Example:**
```typescript
// Critic exit path logic
enum CriticVerdict {
  PROCEED = "PROCEED",           // → Evaluator
  REVISE_METHOD = "REVISE_METHOD", // → Researcher
  REVISE_DATA = "REVISE_DATA"     // → Explorer
}

function handleCriticOutput(verdict: CriticVerdict, context: ExperimentContext) {
  switch (verdict) {
    case CriticVerdict.PROCEED:
      return spawnAgent('evaluator', context);
    case CriticVerdict.REVISE_METHOD:
      context.critiqueFeedback = loadCritiqueReport();
      return spawnAgent('researcher', context);
    case CriticVerdict.REVISE_DATA:
      context.anomaliesFound = extractAnomalies();
      return spawnAgent('explorer', context);
  }
}
```

### Pattern 2: Data-First Gating (Mandatory EDA Before Hypothesis)

**What:** No research objective can be set without initial Exploratory Data Analysis. Explorer must run before Architect.

**When to use:** Every new hypothesis or when REVISE_DATA verdict issued.

**Trade-offs:**
- **Pro:** Grounds hypotheses in data reality
- **Pro:** Surfaces data quality issues early
- **Con:** Adds upfront time cost
- **Con:** Requires discipline to not skip

**Example:**
```typescript
// Workflow orchestrator enforcing data-first
async function startNewHypothesis(goal: string, dataset: string) {
  // Block hypothesis synthesis until data profiled
  const dataReport = await spawnAgent('explorer', { dataset, goal });

  if (!dataReport.completed) {
    throw new Error("Cannot proceed to hypothesis without DATA_REPORT.md");
  }

  // Only now can Architect synthesize hypothesis
  const objective = await spawnAgent('architect', { dataReport, goal });
  return objective;
}
```

### Pattern 3: Versioned Experiment Isolation

**What:** Each iteration of the recursive loop creates a new `run_NNN/` directory with complete context (code, logs, outputs).

**When to use:** Every time Researcher produces a new implementation or Critic triggers re-work.

**Trade-offs:**
- **Pro:** Perfect reproducibility — each run is self-contained
- **Pro:** Easy comparison across iterations
- **Con:** Disk space grows with iteration count
- **Con:** Need garbage collection strategy for failed runs

**Example:**
```typescript
// Experiment versioning
function createExperimentRun(hypothesisId: string): ExperimentRun {
  const runNumber = getNextRunNumber();
  const runDir = `experiments/run_${runNumber.toString().padStart(3, '0')}`;

  fs.mkdirSync(`${runDir}/code`);
  fs.mkdirSync(`${runDir}/logs`);
  fs.mkdirSync(`${runDir}/outputs`);

  // Snapshot current OBJECTIVE.md and DATA_REPORT.md
  fs.copyFileSync('OBJECTIVE.md', `${runDir}/OBJECTIVE_snapshot.md`);
  fs.copyFileSync('reports/DATA_REPORT.md', `${runDir}/DATA_REPORT_snapshot.md`);

  return { runNumber, runDir };
}
```

### Pattern 4: Evidence Package for Human Gate

**What:** Bundle all context needed for human decision-making: OBJECTIVE.md, DATA_REPORT.md, CRITIC_LOGS.md, SCORECARD.json.

**When to use:** After Evaluator completes and before hypothesis is marked validated/disproven.

**Trade-offs:**
- **Pro:** Prevents false positives from automated metrics
- **Pro:** Human retains scientific judgment
- **Con:** Requires human availability (can't fully automate)

**Example:**
```typescript
interface EvidencePackage {
  objective: string;        // What hypothesis was tested
  dataReport: string;       // Ground truth about the data
  critiqueLogs: string[];   // Critic's arguments during loop
  scorecard: Scorecard;     // Quantitative results
  experimentPath: string;   // Path to run artifacts
}

async function presentToHuman(pkg: EvidencePackage): Promise<'SEAL' | 'ITERATE' | 'ARCHIVE'> {
  // Display structured evidence
  console.log(`\n=== Evidence Package ===`);
  console.log(`Hypothesis: ${pkg.objective}`);
  console.log(`Iterations: ${pkg.critiqueLogs.length}`);
  console.log(`Final Score: ${pkg.scorecard.primaryMetric}`);

  // Prompt for decision
  const decision = await prompt("Decision? (Seal/Iterate/Archive)");
  return decision.toUpperCase() as 'SEAL' | 'ITERATE' | 'ARCHIVE';
}
```

### Pattern 5: Agent Role Separation with Specialized Context

**What:** Each agent has narrow responsibility and receives only relevant context (Explorer gets raw data, Critic gets experimental results).

**When to use:** Always — prevents agents from overstepping boundaries.

**Trade-offs:**
- **Pro:** Clear accountability for each phase
- **Pro:** Optimized context windows (no irrelevant data)
- **Con:** Requires orchestrator to manage context routing

## Data Flow

### Primary Research Loop

```
[User: Project Goal + Dataset]
           ↓
    ┌─────────────┐
    │  Explorer   │ → DATA_REPORT.md
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │  Architect  │ → OBJECTIVE.md (hypothesis)
    └──────┬──────┘
           ↓
    ┌─────────────────────────────────────────────┐
    │         RECURSIVE VALIDATION LOOP           │
    │  ┌──────────┐        ┌─────────┐           │
    │  │Researcher│ ────→  │ Critic  │           │
    │  └────▲─────┘        └────┬────┘           │
    │       │ REVISE_METHOD     │                │
    │       └───────────────────┘                │
    │                            │ REVISE_DATA   │
    │       ┌────────────────────┘               │
    │       ↓                                    │
    │  ┌──────────┐  (PROCEED)  ┌──────────┐   │
    │  │ Explorer │ ─────────→  │Evaluator │   │
    │  └──────────┘              └────┬─────┘   │
    └────────────────────────────────┬───────────┘
                                     ↓
                            ┌────────────────┐
                            │  Human Gate    │
                            │ (Evidence Pkg) │
                            └────────┬───────┘
                                     ↓
                     ┌───────────────┴───────────────┐
                     ↓               ↓               ↓
                  [SEAL]         [ITERATE]       [ARCHIVE]
              (validated)    (refine & retry)   (disproven)
```

### Artifact Generation Flow

```
Explorer
  ↓ writes
DATA_REPORT.md (living document, continuously updated)
  ↓ read by
Architect
  ↓ writes
OBJECTIVE.md (testable hypothesis)
  ↓ read by
Researcher
  ↓ writes
experiments/run_NNN/code/* (implementation artifacts)
  ↓ read by
Critic
  ↓ writes
experiments/run_NNN/logs/critique.md (validation report)
  ↓ routes to
Evaluator
  ↓ writes
experiments/run_NNN/scorecard.json (quantitative metrics)
  ↓ packages into
Evidence Package (all of the above)
  ↓ presented to
Human
  ↓ writes
human_eval/decision_log.md (seal/iterate/archive decision + rationale)
```

### State Management Flow

```
STATE.md (persisted to disk)
  ├── current_phase: "recursive_loop"
  ├── active_run: "run_003"
  ├── loop_history: [
  │     { run: 1, verdict: "REVISE_METHOD" },
  │     { run: 2, verdict: "REVISE_DATA" },
  │     { run: 3, verdict: "PROCEED" }
  │   ]
  └── human_decision: null (pending)

Orchestrator reads STATE.md → determines next action
Agent writes updates → Orchestrator merges into STATE.md
Git commits STATE.md → audit trail across sessions
```

### Key Data Flows

1. **Hypothesis Synthesis Flow:** Raw data → DATA_REPORT.md → OBJECTIVE.md (ensures hypotheses grounded in data reality)
2. **Recursive Validation Flow:** Researcher output → Critic audit → conditional routing (PROCEED/REVISE_METHOD/REVISE_DATA)
3. **Experiment Versioning Flow:** Each loop iteration → new run_NNN/ directory with complete snapshot
4. **Human Decision Flow:** Evidence Package → Human gate → decision_log.md → next action (seal/iterate/archive)

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| **Single researcher, <10 experiments** | File-based state is sufficient. Git provides all versioning needed. |
| **Small team, <100 experiments** | Add metadata catalog (SQLite) for experiment search. File-based artifacts still work. |
| **Lab/org, 1000+ experiments** | Centralized artifact store (S3/GCS). Metadata DB (Postgres). API layer for multi-user coordination. |

### Scaling Priorities

1. **First bottleneck:** Experiment search/discovery. When you can't remember "which run had the good results," add metadata indexing.
2. **Second bottleneck:** Disk space from versioned artifacts. Implement garbage collection for ARCHIVE'd runs or failed iterations.
3. **Third bottleneck:** Multi-user coordination. Add locking mechanism or branch-per-hypothesis Git workflow.

**For GRD MVP:** File-based state is perfect. Target single researcher, <50 experiments. Defer scaling concerns until adoption validated.

## Anti-Patterns

### Anti-Pattern 1: Skipping Data Reconnaissance

**What people do:** Jump straight to hypothesis definition because "I know my data."

**Why it's wrong:**
- Missed leakage (e.g., target variable in features)
- Unnoticed distribution shifts
- False confidence in data quality

**Do this instead:** Enforce Explorer phase as mandatory gate. No OBJECTIVE.md without DATA_REPORT.md.

### Anti-Pattern 2: Weak Critic (Rubber-Stamp Validation)

**What people do:** Critic only checks "did the code run?" without logical scrutiny.

**Why it's wrong:**
- Overfitting passes through
- Data leakage undetected
- Results don't generalize

**Do this instead:** Critic must have domain knowledge prompts (data leakage patterns, common ML mistakes). Exit codes must be earned, not automatic.

### Anti-Pattern 3: Experiment Mutation (Overwriting Artifacts)

**What people do:** Reuse same directory for multiple iterations, overwriting previous results.

**Why it's wrong:**
- Loses reproducibility
- Can't compare iterations
- Debugging becomes impossible

**Do this instead:** Strict versioning — every Researcher invocation creates new run_NNN/. Old runs are immutable.

### Anti-Pattern 4: Metrics-Only Validation (No Human Gate)

**What people do:** Trust SCORECARD.json blindly, mark hypothesis validated if metric threshold met.

**Why it's wrong:**
- Metrics can be gamed (intentionally or not)
- False positives from overfitting
- Loses scientific rigor

**Do this instead:** Evidence Package + Human Gate is mandatory. Metrics inform, humans decide.

### Anti-Pattern 5: Linear Phase Progression (No Recursion)

**What people do:** Treat research like software development: plan → code → test → done.

**Why it's wrong:**
- Research is non-linear by nature
- Results often invalidate assumptions
- Forces forward-only progress even when wrong

**Do this instead:** Embrace recursive loop. REVISE_DATA is a feature, not a failure.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| **Claude Code** | Hook system for slash commands | Existing GSD integration is proven, reuse architecture |
| **MCP (Model Context Protocol)** | Agent spawning API | Claude Code's subagent mechanism provides isolation |
| **Git** | Atomic commits per validation loop iteration | Each run_NNN completion triggers commit |
| **Python runtime** | Execute Researcher-generated scripts | subprocess or notebook execution engine |
| **Jupyter** | Notebook support for EDA and experiments | nbconvert for notebook → production code graduation |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| **Orchestrator ↔ Agents** | File-based context passing (reads STATE.md, writes artifacts) | Stateless agents, all context from disk |
| **Agent ↔ Agent** | No direct communication — orchestrator routes | Prevents tight coupling |
| **Critic ↔ Orchestrator** | Exit codes (enum: PROCEED/REVISE_METHOD/REVISE_DATA) | Clean state machine logic |
| **Human ↔ System** | Interactive prompts for decisions | Evidence Package presentation, decision capture |

## GRD-Specific Architectural Decisions

### Reuse from GSD Architecture

GRD inherits GSD's proven patterns:

| GSD Pattern | GRD Adaptation |
|-------------|----------------|
| **Multi-agent orchestration** | Reuse spawner, adapt to Explorer/Architect/Researcher/Critic/Evaluator roles |
| **File-based state management** | STATE.md pattern proven, extend with loop_history and Critic verdicts |
| **Template-driven artifacts** | OBJECTIVE.md replaces PRD.md, DATA_REPORT.md is new |
| **Git integration** | Atomic commits per iteration instead of per task |
| **Config system** | `.planning/config.json` controls workflow preferences |

### New Architectural Components

| Component | Why Needed | Implementation Strategy |
|-----------|------------|------------------------|
| **Critic exit code router** | Enable recursive loops | State machine with conditional branching |
| **Evidence Package generator** | Support Human Gate | Bundle OBJECTIVE + DATA_REPORT + logs + scorecard |
| **Experiment versioning** | Reproducibility & comparison | Auto-increment run_NNN directories |
| **Notebook execution engine** | Support Jupyter workflows | nbconvert or papermill integration |
| **Data leakage detector** | Critic's core capability | Pattern matching + feature/target overlap analysis |

## Build Order Implications

Based on component dependencies, suggested phase structure for GRD roadmap:

### Phase 1: Core Orchestration (Foundation)
- Adapt GSD orchestrator for GRD lifecycle
- Implement STATE.md extensions (loop_history, Critic verdicts)
- Create basic agent spawning for Explorer → Architect → Researcher flow

**Rationale:** Foundation layer must exist before specialized agents can function.

### Phase 2: Agent Role Definitions (Specialization)
- Create Explorer agent (DATA_REPORT.md generation)
- Create Architect agent (OBJECTIVE.md synthesis)
- Create Researcher agent (experiment implementation)

**Rationale:** Linear flow before recursive loop — validate basic agent functionality.

### Phase 3: Recursive Validation Loop (Core Innovation)
- Implement Critic agent with exit code logic
- Add state router for PROCEED/REVISE_METHOD/REVISE_DATA
- Create experiment versioning (run_NNN directories)

**Rationale:** Most complex component — needs foundation + basic agents working first.

### Phase 4: Quantitative Evaluation (Metrics)
- Implement Evaluator agent
- Create scorecard.json generation
- Add benchmark suite execution

**Rationale:** Depends on experiments producing artifacts to evaluate.

### Phase 5: Human Decision Gate (Quality Control)
- Build Evidence Package generator
- Implement interactive decision prompt
- Create decision_log.md tracking

**Rationale:** Final validation layer — needs all upstream artifacts to exist.

### Phase 6: Notebook Support (Researcher UX)
- Add Jupyter notebook execution
- Implement notebook → production code graduation
- Support inline EDA in notebooks

**Rationale:** Enhancement to Researcher workflow — optional for MVP, improves usability.

## Sources

**Confidence Note:** This research is based on my training knowledge (pre-January 2025) of ML workflow systems. Web tools were unavailable for verification. Key claims about MLflow, Weights & Biases, DVC, and Metaflow architectures reflect common patterns as of my training cutoff but should be verified against current official documentation.

**Training knowledge sources:**
- MLflow architecture (experiment tracking, artifact storage, model registry patterns)
- Weights & Biases patterns (run versioning, interactive dashboards, sweep orchestration)
- DVC architecture (data versioning, pipeline DAGs, remote storage)
- Metaflow patterns (workflow DSL, step isolation, failure recovery)
- GSD existing architecture (proven multi-agent orchestration, file-based state)

**Primary sources (not web-verified):**
- Existing GSD codebase analysis (file://Users/evanowen/Library/Mobile Documents/com~apple~CloudDocs/Workspace/playground/get-research-done/.planning/codebase/ARCHITECTURE.md)
- GRD PROJECT.md requirements (file://Users/evanowen/Library/Mobile Documents/com~apple~CloudDocs/Workspace/playground/get-research-done/.planning/PROJECT.md)

**Recommended verification:**
- MLflow official docs: https://mlflow.org/docs/latest/tracking.html
- W&B architecture: https://docs.wandb.ai/guides/track
- DVC internals: https://dvc.org/doc/user-guide/project-structure/internal-files
- Metaflow design: https://docs.metaflow.org/introduction/what-is-metaflow

---
*Architecture research for: ML Research Workflow Systems (GRD)*
*Researched: 2026-01-27*
*Confidence: MEDIUM — based on training knowledge without current web verification*
