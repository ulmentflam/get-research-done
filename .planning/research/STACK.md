# Technology Stack: ML Research Workflow Automation

**Project:** GRD (Get Research Done)
**Domain:** ML research workflow automation and experiment tracking
**Researched:** 2026-01-27
**Overall Confidence:** MEDIUM (based on training data through January 2025, no external verification available)

## Executive Summary

GRD is a Claude Code workflow tool optimized for ML researchers. The stack must support:
- Experiment tracking and versioning
- Data versioning and lineage
- Notebook management and reproducibility
- Hypothesis-driven workflow orchestration
- Integration with existing ML research tooling

**Recommended approach:** Extend GSD's Node.js + Markdown architecture with Python-based ML tooling integrations. Keep orchestration in Node.js (Claude Code compatibility), delegate ML operations to Python ecosystem tools.

---

## Core Architecture

### Orchestration Layer (Inherited from GSD)

| Technology | Version | Purpose | Rationale | Confidence |
|------------|---------|---------|-----------|------------|
| Node.js | >= 18.0.0 | Runtime for orchestration | GSD requires 16.7.0+; ML tools need newer features for async ops | HIGH |
| Markdown + YAML | - | Agent/command definitions | GSD pattern, maintains compatibility | HIGH |
| JSON | - | State/config management | Native Node.js support, simple | HIGH |

**Why Node.js orchestration with Python ML tools:**
- GSD's existing architecture is Node.js-based
- Claude Code runs Node.js naturally
- Python ecosystem dominates ML tooling
- Node can shell out to Python scripts for ML operations
- Keeps orchestration logic separate from domain logic

---

## Experiment Tracking

### Primary Recommendation: MLflow

| Technology | Version | Purpose | Rationale | Confidence |
|------------|---------|---------|-----------|------------|
| MLflow | >= 2.9.0 | Experiment tracking, model registry | Open source, self-hosted, comprehensive API | MEDIUM |
| Python | >= 3.9 | ML tooling runtime | Modern Python features, type hints | HIGH |

**Why MLflow:**
- **Self-hosted**: No vendor lock-in, runs locally or on-prem
- **Comprehensive**: Tracks experiments, models, parameters, metrics, artifacts
- **Programmatic API**: Python API for logging, Node.js can call via subprocess
- **UI included**: Built-in web UI for visualization (mlflow ui)
- **Model registry**: Versioning and staging for models
- **Standard**: De facto standard in ML research (especially academia)

**Integration approach:**
```javascript
// Node.js orchestration calls Python MLflow scripts
const { execSync } = require('child_process');
execSync(`python .grd/scripts/log-experiment.py --run-id ${runId} --metric ${metric}`, {
  cwd: projectRoot,
  env: { ...process.env, MLFLOW_TRACKING_URI: trackingUri }
});
```

**Configuration:**
- Tracking URI: `file://.mlruns` (local) or `http://mlflow-server:5000` (shared)
- Stored in `.planning/config.json` alongside GSD config

**Version note:** MLflow 2.9.0 was current in late 2024. CONFIDENCE: MEDIUM (cannot verify 2025 versions without web access)

### Alternative Considered: Weights & Biases (W&B)

| Technology | Why Not Primary | When to Use |
|------------|----------------|-------------|
| Weights & Biases | Cloud-hosted (requires account), vendor lock-in, API dependency | Collaborative teams, already using W&B, need social features |

**Trade-offs:**
- **W&B Pros**: Superior visualization, collaboration features, hosted (no setup)
- **W&B Cons**: Requires account/login, data leaves researcher's control, pricing for large-scale use
- **MLflow Pros**: Self-hosted, no external dependencies, free, full control
- **MLflow Cons**: More setup, less polished UI, fewer social features

**Recommendation:** Start with MLflow for GRD v1. Add W&B as optional integration in v2 if users request it.

---

## Data Versioning

### Primary Recommendation: DVC (Data Version Control)

| Technology | Version | Purpose | Rationale | Confidence |
|------------|---------|---------|-----------|------------|
| DVC | >= 3.0.0 | Data versioning, pipeline tracking | Git-like for data, integrates with MLflow | MEDIUM |

**Why DVC:**
- **Git-like interface**: `dvc add`, `dvc push`, `dvc pull` - familiar to developers
- **Storage agnostic**: Local, S3, GCS, Azure, SSH - configurable
- **Lightweight**: Stores metadata in Git, data separately
- **Pipeline tracking**: `.dvc` files track data dependencies
- **MLflow integration**: Can track DVC data versions in MLflow runs

**Integration approach:**
```bash
# GRD orchestrates DVC commands via Node.js
dvc add data/raw/dataset.csv
git add data/raw/dataset.csv.dvc .gitignore
dvc push  # Upload to remote storage

# Track DVC version in MLflow
python .grd/scripts/log-dvc-metadata.py --path data/raw/dataset.csv
```

**Configuration:**
- Remote storage: `.dvc/config` (DVC's standard)
- GRD tracks DVC remotes in `.planning/config.json` for validation

**Version note:** DVC 3.0+ introduced improved pipeline tracking. CONFIDENCE: MEDIUM (version based on 2024 knowledge)

### Alternative Considered: git-lfs

| Technology | Why Not Primary | When to Use |
|------------|----------------|-------------|
| git-lfs | Limited to Git hosting size limits, no pipeline tracking | Small datasets (<1GB), simple needs, already on GitHub/GitLab |

**Trade-offs:**
- **git-lfs Pros**: Simpler, native Git integration
- **git-lfs Cons**: GitHub/GitLab file size limits (2GB/5GB), no computation tracking
- **DVC Pros**: Unlimited size (storage-dependent), tracks pipelines, reproducibility features
- **DVC Cons**: Extra tool to learn, separate storage setup

---

## Notebook Management

### Primary Recommendation: JupyterLab + Jupytext

| Technology | Version | Purpose | Rationale | Confidence |
|------------|---------|---------|-----------|------------|
| JupyterLab | >= 4.0.0 | Interactive notebook environment | Standard ML research tool | HIGH |
| Jupytext | >= 1.15.0 | Notebook versioning (py/ipynb sync) | Git-friendly notebook management | MEDIUM |

**Why JupyterLab + Jupytext:**
- **JupyterLab**: Standard interface for ML research, everyone knows it
- **Jupytext**: Converts `.ipynb` ↔ `.py` for Git versioning
  - Notebooks are binary, terrible for Git diffs
  - Jupytext stores as `.py` with special comments
  - Git diffs work, merge conflicts are manageable

**Integration approach:**
```bash
# GRD configures Jupytext automatically
jupytext --set-formats ipynb,py:percent notebook.ipynb
# Creates notebook.py alongside notebook.ipynb
# Git tracks .py, .ipynb is gitignored
```

**Configuration:**
- `jupytext.toml` or `pyproject.toml` for project-wide settings
- GRD generates during project init
- Formats: `.py:percent` (recommended), `.py:light`, `.md`

**Reproducibility:**
- Track notebook execution order via outputs
- Use `papermill` for parameterized execution (phase-specific research)
- Log notebook runs to MLflow with parameters + outputs

### Alternative Considered: Plain Python scripts

| Approach | Why Not Primary | When to Use |
|----------|----------------|-------------|
| Pure .py scripts | No interactive exploration | Production pipelines, non-exploratory work |

**Trade-offs:**
- **Scripts Pros**: Git-native, no versioning issues, easier to test
- **Scripts Cons**: No visualization, poor for EDA (exploratory data analysis)
- **Notebooks Pros**: Interactive, visualization, standard for research
- **Notebooks Cons**: Hard to version, execution order issues

**GRD approach:** Support both. Exploratory phases use notebooks (with Jupytext), production phases use scripts.

---

## Python Environment Management

### Primary Recommendation: uv + pyproject.toml

| Technology | Version | Purpose | Rationale | Confidence |
|------------|---------|---------|-----------|------------|
| uv | >= 0.1.0 | Python package manager | Fast, modern, pip-compatible, virtual env management | MEDIUM |
| pyproject.toml | - | Dependency declaration | PEP 621 standard, replaces requirements.txt | HIGH |

**Why uv:**
- **Speed**: 10-100x faster than pip (Rust-based)
- **Modern**: Unified tool (pip + virtualenv + poetry features)
- **Compatibility**: Drop-in pip replacement
- **Lock files**: `uv.lock` for reproducibility
- **Released 2024**: Astral (Ruff creators) project, gaining rapid adoption

**Integration approach:**
```bash
# GRD initializes Python environment
uv venv .venv
uv pip install -e .  # Installs from pyproject.toml

# Lock dependencies
uv pip compile pyproject.toml -o requirements.lock
```

**pyproject.toml structure:**
```toml
[project]
name = "my-research-project"
version = "0.1.0"
dependencies = [
    "mlflow>=2.9.0",
    "dvc>=3.0.0",
    "jupyterlab>=4.0.0",
    "jupytext>=1.15.0",
]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]
```

**Confidence note:** uv was released in 2024 and rapidly adopted. CONFIDENCE: MEDIUM (may have version updates in 2025)

### Alternatives Considered

| Technology | Why Not Primary | When to Use |
|------------|----------------|-------------|
| Poetry | Slower, more opinionated, lock file conflicts | Complex dependency resolution needs |
| Conda | Heavy, slow, non-standard lock files | Need non-Python dependencies (CUDA, etc.) |
| pip + venv | No lock file standard, slower | Legacy compatibility |

**GRD decision:** Use `uv` for speed and modern tooling. Fall back to `pip` if user environment doesn't support uv.

---

## Workflow Orchestration

### Primary Recommendation: Custom Node.js (GSD Pattern)

| Technology | Version | Purpose | Rationale | Confidence |
|------------|---------|---------|-----------|------------|
| Node.js + child_process | Built-in | Orchestrate Python tools | Maintains GSD architecture, flexible | HIGH |

**Why custom orchestration:**
- GSD already has proven orchestration patterns
- ML workflow needs are domain-specific (hypothesis loops, validation)
- Existing tools (Airflow, Prefect, Dagster) are overkill for single-researcher workflows
- Node.js can shell out to Python for ML operations

**Pattern:**
```javascript
// Node.js orchestrates, Python executes
async function runExperiment(hypothesis, config) {
  const runId = generateRunId();

  // 1. Log hypothesis to MLflow
  await exec(`python .grd/scripts/start-run.py --run-id ${runId} --hypothesis "${hypothesis}"`);

  // 2. Execute experiment (Python script or notebook via papermill)
  await exec(`papermill experiments/experiment.ipynb output.ipynb -p run_id ${runId}`);

  // 3. Validate results (Python validation script)
  const result = await exec(`python .grd/scripts/validate.py --run-id ${runId}`);

  // 4. Update state
  updateState({ phase: 'validation', runId, result });
}
```

### Alternatives Considered

| Technology | Why Not Primary | When to Use |
|------------|----------------|-------------|
| Airflow | Too heavy, server required, overkill for solo researcher | Multi-researcher teams, complex DAGs |
| Prefect | Better than Airflow but still server-oriented | Need distributed execution |
| DVC Pipelines | Good for reproducibility, poor for interactive research | Pure pipeline automation, no human-in-loop |

**GRD approach:** Keep orchestration simple. Let researchers focus on research, not configuring workflow engines.

---

## Validation & Testing

### Primary Recommendation: Pytest + Great Expectations

| Technology | Version | Purpose | Rationale | Confidence |
|------------|---------|---------|---------|------------|
| pytest | >= 7.0.0 | Unit/integration testing | Standard Python testing | HIGH |
| Great Expectations | >= 0.18.0 | Data validation | Declarative data quality checks | MEDIUM |

**Why Great Expectations:**
- **Data validation**: ML research depends on data quality
- **Declarative**: Define expectations as checkpoints
- **MLflow integration**: Log validation results to MLflow
- **Catches issues early**: Bad data detected before hours of training

**Integration approach:**
```python
# .grd/validations/data_quality.py
import great_expectations as gex

context = gex.get_context()
suite = context.get_expectation_suite("raw_data_validation")

# Define expectations
suite.add_expectation(
    gex.core.ExpectColumnValuesToNotBeNull(column="target")
)

# Run validation
results = context.run_checkpoint("data_checkpoint")

# Log to MLflow
mlflow.log_metrics({"data_quality_score": results.statistics["success_percent"]})
```

**Alternative:** Pandera (lighter, dataframe-focused). Use if Great Expectations feels too heavy.

---

## Supporting Libraries

### Python ML Ecosystem

| Library | Version | Purpose | When to Use | Confidence |
|---------|---------|---------|-------------|------------|
| pandas | >= 2.0.0 | Data manipulation | Always (data analysis) | HIGH |
| numpy | >= 1.24.0 | Numerical computing | Always (ML operations) | HIGH |
| scikit-learn | >= 1.3.0 | ML algorithms | Classical ML experiments | HIGH |
| torch / tensorflow | >= 2.0 / >= 2.15 | Deep learning | Neural network research | MEDIUM |
| matplotlib / seaborn | >= 3.7 / >= 0.12 | Visualization | Always (EDA, results viz) | HIGH |
| polars | >= 0.19.0 | Fast dataframes | Large datasets (>1GB) | MEDIUM |

**Notes:**
- **PyTorch vs TensorFlow**: Both supported, let researcher choose in project init
- **Polars**: Alternative to pandas for large data, much faster
- **Version confidence**: MEDIUM for specific versions (may have 2025 updates)

### Node.js Utilities

| Library | Version | Purpose | When to Use | Confidence |
|---------|---------|---------|-------------|------------|
| chalk | >= 5.0.0 | Terminal coloring | Status output (GSD pattern) | HIGH |
| yaml | >= 2.3.0 | YAML parsing | Read .dvc, config files | HIGH |

---

## Storage & Artifacts

### Experiment Artifacts

| Storage Type | Recommended | Purpose | Configuration |
|--------------|-------------|---------|--------------|
| Local | `.mlruns/`, `.grd/artifacts/` | Development, single machine | Default |
| S3-compatible | MinIO (local), AWS S3 (cloud) | Shared storage, team collaboration | MLFLOW_TRACKING_URI, DVC remote |
| NFS/Shared disk | Mounted filesystem | On-prem shared storage | File path in config |

**GRD storage structure:**
```
.mlruns/               # MLflow tracking (experiments, runs, metrics)
.grd/
  artifacts/           # Large artifacts not in MLflow
  notebooks/           # Versioned notebooks (.py via Jupytext)
  scripts/             # Reusable Python scripts
  validations/         # Great Expectations checkpoints
data/
  raw/                 # Raw data (DVC-tracked)
  processed/           # Processed data (DVC-tracked)
  features/            # Feature engineering outputs (DVC-tracked)
```

---

## Development Tools

### Code Quality

| Tool | Version | Purpose | Rationale | Confidence |
|------|---------|---------|-----------|------------|
| Ruff | >= 0.1.0 | Python linting + formatting | Fast (Rust), replaces flake8+black | MEDIUM |
| mypy | >= 1.7.0 | Type checking | Catch errors before runtime | HIGH |

**Why Ruff:**
- 10-100x faster than flake8/black
- Single tool (linting + formatting)
- Compatible with existing configs
- Created by Astral (same team as uv)

### Git Integration

| Aspect | Approach | Rationale |
|--------|----------|-----------|
| Commits | GSD atomic commit pattern | Each experiment/phase gets own commit |
| Branches | Feature branches per hypothesis | Isolate experimental work |
| Tags | MLflow run IDs as tags | Link Git history to experiments |

**GRD git commit format:**
```
experiment(hyp-001): test hypothesis about feature correlation

- Run ID: mlflow-run-123abc
- Hypothesis: Feature X correlates with target Y
- Result: VALIDATED (p < 0.05)
- Next: Proceed to model training phase
```

---

## Installation & Setup

### GRD Initialization Script

```bash
# Install GRD (extends GSD)
npx get-research-done-cc --claude --global

# Initialize new ML research project
/grd:new-project

# GRD sets up:
# 1. Python environment (uv venv + pyproject.toml)
# 2. MLflow tracking (local .mlruns)
# 3. DVC init (data versioning)
# 4. Jupytext config (notebook versioning)
# 5. Great Expectations (data validation)
# 6. Git hooks (pre-commit: lint, data validation)
```

### pyproject.toml template

```toml
[project]
name = "my-ml-research"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = [
    "mlflow>=2.9.0",
    "dvc>=3.0.0",
    "dvc-s3>=3.0.0",  # If using S3
    "jupyterlab>=4.0.0",
    "jupytext>=1.15.0",
    "great-expectations>=0.18.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]
torch = [
    "torch>=2.0.0",
    "torchvision>=0.15.0",
]
tensorflow = [
    "tensorflow>=2.15.0",
]

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]

[tool.jupytext]
formats = "ipynb,py:percent"
```

---

## Anti-Patterns to Avoid

### What NOT to Use

| Technology | Why Avoid | What to Use Instead |
|------------|-----------|---------------------|
| requirements.txt only | No version locking, ambiguous dependencies | pyproject.toml + uv.lock |
| .ipynb in Git | Binary format, merge conflicts | Jupytext (.py:percent) |
| Conda for everything | Slow, heavy, reproducibility issues | uv for Python packages, Conda only for non-Python deps |
| Manual experiment tracking (spreadsheets) | Error-prone, not programmatic | MLflow |
| Global Python packages | Dependency conflicts, not reproducible | Virtual environments (uv venv) |
| Git LFS for large datasets (>5GB) | GitHub/GitLab size limits | DVC with S3/GCS remote |

---

## System Requirements

### Minimum

- Node.js 18.0.0+ (GRD orchestration)
- Python 3.9+ (ML tooling)
- Git 2.30+ (versioning, DVC)
- 8GB RAM (small datasets)
- 10GB disk space (MLflow artifacts, DVC cache)

### Recommended

- Node.js 20.x LTS
- Python 3.11+ (performance improvements)
- 16GB+ RAM (medium datasets)
- 100GB+ disk space (larger experiments)
- SSD (MLflow database, DVC cache performance)

### For Large-Scale Research

- Python 3.11+
- 32GB+ RAM
- 500GB+ SSD
- GPU (CUDA 12.0+ for PyTorch/TensorFlow)
- S3/GCS for remote artifact storage

---

## Confidence Assessment

| Category | Confidence | Notes |
|----------|------------|-------|
| Node.js orchestration | HIGH | Inherited from GSD, well-understood |
| MLflow | MEDIUM | Standard in 2024, version may have updated in 2025 |
| DVC | MEDIUM | Standard in 2024, version may have updated in 2025 |
| JupyterLab + Jupytext | HIGH | Mature, stable patterns |
| uv | MEDIUM | New in 2024, rapid adoption but may have breaking changes |
| Python versions | HIGH | Version ranges stable |
| Great Expectations | MEDIUM | API may have evolved in 2025 |
| PyTorch/TensorFlow versions | LOW | Versions change frequently, need verification |

---

## Sources & Verification Needed

**CRITICAL:** This research is based on training data through January 2025. The following need verification before roadmap creation:

1. **MLflow current version** - Was 2.9.x in late 2024, check for 2.x or 3.x releases
2. **DVC current version** - Was 3.x in 2024, verify latest stable
3. **uv stability** - Released mid-2024, check if API is stable for production use
4. **Great Expectations** - Was 0.18.x in 2024, may have 1.0 release
5. **Python library versions** - pandas 2.x, numpy 1.24+, scikit-learn 1.3+ (verify current stable)

**Verification sources to consult:**
- MLflow: https://mlflow.org/releases
- DVC: https://dvc.org/doc/install
- uv: https://github.com/astral-sh/uv/releases
- Great Expectations: https://docs.greatexpectations.io/

**If web access unavailable:** Flag these as "to be verified during implementation" and proceed with documented versions as baseline.

---

## Recommendation Summary

**For GRD v1.0, use:**

1. **Orchestration**: Node.js (GSD architecture) + Python subprocess calls
2. **Experiment Tracking**: MLflow (self-hosted, local `.mlruns`)
3. **Data Versioning**: DVC (git-like, flexible storage)
4. **Notebooks**: JupyterLab + Jupytext (reproducibility)
5. **Environment**: uv + pyproject.toml (speed, modern standards)
6. **Validation**: pytest + Great Expectations (code + data quality)
7. **Code Quality**: Ruff (fast) + mypy (type safety)

**Phase 1 (MVP)**: Focus on local, single-researcher workflow
**Phase 2+**: Add collaborative features (shared MLflow server, S3/GCS storage, W&B integration)

---

*Stack research completed: 2026-01-27*
*CONFIDENCE: MEDIUM overall (training data only, no external verification)*
*REQUIRES: Version verification before implementation*
