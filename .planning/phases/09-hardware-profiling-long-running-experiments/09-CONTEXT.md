# Phase 9: Hardware Profiling & Long-Running Experiments - Context

**Gathered:** 2026-01-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Capture hardware context (GPU, CUDA, CPU, memory) during data exploration for reproducibility, and handle experiments that exceed standard task timeouts (training runs, hyperparameter sweeps). Explorer profiles hardware at EDA time; Researcher estimates duration and manages long-running execution with user confirmation.

</domain>

<decisions>
## Implementation Decisions

### Hardware profile scope
- Store in both locations: DATA_REPORT.md gets summary section, dedicated HARDWARE_PROFILE.md gets full details
- Hardware profiling runs during Explorer EDA (natural starting point, captured once)
- Profile reusable across experiments from same data exploration

### Duration estimation
- Estimate based on data size + hardware specs (rows, features, GPU memory, CPU cores)
- Long-running threshold is user-configurable (default can be 10 minutes to match task timeout)
- Estimates inform whether to trigger long-running mode confirmation

### Long-running mode UX
- Single confirmation at experiment start: "This may take ~X hours. Proceed?"
- After confirmation, hands-off execution — no further prompts during that research loop
- Session-level approval: once confirmed, all iterations in current research loop run uninterrupted
- No repeated confirmations per iteration

### Checkpoint & resume behavior
- Experiment code owns checkpoints — GRD documents best practices but doesn't manage saving/loading
- Interrupted experiments marked as INTERRUPTED, partial outputs preserved in run directory
- GRD provides resumability hints in run metadata: document how to resume (checkpoint path, epoch number)

### Claude's Discretion
- GPU details depth (basic vs extended) based on experiment type
- Cloud/container environment detection based on available signals
- Progress verbosity during long runs (minimal heartbeat vs rich metrics vs log streaming)
- Hardware upgrade suggestions when estimates are high
- Session boundary tracking for multi-day experiments

</decisions>

<specifics>
## Specific Ideas

- Hardware profile should capture enough for someone to reproduce on similar hardware
- Long-running confirmation should show estimated time clearly before user commits
- Interrupted runs should leave clear breadcrumbs for resumption

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 09-hardware-profiling-long-running-experiments*
*Context gathered: 2026-01-30*
