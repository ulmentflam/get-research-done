# Phase 6: Notebook Support - Context

**Gathered:** 2026-01-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Users can execute Jupyter notebooks as experiments with explicit graduation to validated scripts. Notebooks in exploration can be run through the GRD validation loop (Researcher → Critic → Evaluator). When notebooks achieve Critic PROCEED verdict, they can graduate to production scripts in src/experiments/. This phase covers notebook execution, directory structure, graduation requirements, and Critic enforcement for notebooks.

</domain>

<decisions>
## Implementation Decisions

### Notebook execution
- Parameterization encouraged but not required for exploration notebooks
- Fresh kernel for every run (reproducibility over speed)
- Cell-level timeout to catch infinite loops early
- Auto-detect kernel from notebook metadata, fall back to current environment
- Save both executed notebook AND extract outputs to structured files in run_NNN/
- Inherit environment for GPU/resources (no explicit declaration required)
- Retry once on execution failure before marking run as failed
- Capture both stdout/stderr streams AND encourage structured GRD logging for key events

### Directory structure
- Exploration notebooks live in `notebooks/exploration/` (top-level, not under experiments/)
- No validated notebooks directory — graduation converts notebooks to scripts
- Original notebook stays in exploration alongside graduated script (not archived/deleted)
- User discretion for organization within exploration/ (no enforced structure)
- Graduated scripts land in `src/experiments/`
- Script header comment references source notebook (no separate metadata file)
- Notebook runs create standard experiments/run_NNN/ directories (same as scripts)

### Graduation checklist
- All graduation requirements equally important (no prioritization)
- Hardcoded paths: advisory warning (doesn't block graduation)
- Random seed: must be explicitly set (numpy, torch, random, etc.)
- Graduation requires successful run with Critic PROCEED verdict

### Critic enforcement
- Same evaluation standards for notebooks and scripts (no special treatment)
- Cell execution order not a Critic concern (execution handles via fresh kernel)
- REVISE_METHOD response: create new notebook version (don't edit in place)
- Tiered blocking: reproducibility checks block graduation, style checks warn only

### Claude's Discretion
- Notebook execution engine (papermill vs nbconvert vs other)
- Output/metric extraction approach (cell tags vs convention vs hybrid)
- Checkpointing support (complexity vs value tradeoff)
- Container/isolation support (if any)
- Cell-level timeout duration

</decisions>

<specifics>
## Specific Ideas

- Graduation means conversion to script — notebooks are for exploration, scripts are for production
- Versioning on revision: when Critic returns REVISE_METHOD, user creates new notebook version rather than editing in place
- Tiered validation: hard blocks for reproducibility (seeds), soft warnings for style (paths)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 06-notebook-support*
*Context gathered: 2026-01-30*
