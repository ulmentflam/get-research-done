---
phase: 09-hardware-profiling-long-running
plan: 02
subsystem: experiment-management
tags: [timeout-management, checkpoints, pytorch, resumability, signal-handlers]

# Dependency graph
requires:
  - phase: 09-hardware-profiling-long-running
    provides: Phase context for hardware-aware experiment management
provides:
  - ExperimentTimeoutManager with session-level approval for long-running experiments
  - CheckpointHandler for save/load/resume of training state
  - Signal handlers for graceful shutdown on interruption
  - Resumability hints for actionable checkpoint guidance
affects: [09-03, researcher-agent, experiment-orchestration]

# Tech tracking
tech-stack:
  added: []
  patterns: [session-level-approval, checkpoint-resume, graceful-shutdown, signal-handlers]

key-files:
  created:
    - src/grd/experiment/__init__.py
    - src/grd/experiment/timeout_manager.py
    - src/grd/experiment/checkpoint_handler.py
  modified: []

key-decisions:
  - "Session-level approval applies for entire session after first long-running request"
  - "Timeout manager does not use asyncio - provides configuration for external timeout handling"
  - "Checkpoints saved in two formats: versioned (checkpoint_epoch_N.pt) and latest (checkpoint_latest.pt)"
  - "Signal handlers (SIGINT/SIGTERM) set interrupted flag rather than forcing immediate save"
  - "Uses torch.save() with atomic writes when available, fallback to pickle"

patterns-established:
  - "Pattern: Session-level approval without repeated prompts for long-running experiments"
  - "Pattern: get_timeout() returns None after approval to bypass timeout constraints"
  - "Pattern: Checkpoint saves model_state, optimizer_state, epoch, loss, and metadata"
  - "Pattern: Graceful shutdown sets interrupted flag for training loops to handle cleanup"
  - "Pattern: get_resumability_hints() provides actionable guidance for resume decisions"

# Metrics
duration: 2.6min
completed: 2026-01-30
---

# Phase 9 Plan 02: Timeout & Checkpoint Management Summary

**Session-level timeout approval and checkpoint-resume for long-running ML training experiments**

## Performance

- **Duration:** 2.6 min
- **Started:** 2026-01-30T18:43:49Z
- **Completed:** 2026-01-30T18:46:27Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- ExperimentTimeoutManager provides session-level approval tracking without repeated prompts
- CheckpointHandler saves complete training state (model, optimizer, epoch, loss, metadata)
- Signal handlers enable graceful shutdown with checkpoint save before termination
- Resumability hints guide users on checkpoint availability and resume options
- Both modules verified with comprehensive unit tests

## Task Commits

Each task was committed atomically:

1. **Task 1: Create timeout manager module** - `0dd7297` (feat)
2. **Task 2: Create checkpoint handler module** - `7d57a11` (feat)

## Files Created/Modified
- `src/grd/experiment/__init__.py` - Package exports for ExperimentTimeoutManager and CheckpointHandler
- `src/grd/experiment/timeout_manager.py` - Session-level timeout approval and configuration
- `src/grd/experiment/checkpoint_handler.py` - Checkpoint save/load with graceful shutdown support

## Decisions Made

**1. Session-level approval applies for entire session**
- Once user approves long-running mode, all subsequent experiments in session bypass timeout
- Prevents repeated prompts during multi-experiment workflows
- Approval metadata logged for audit trail with timestamp and estimated duration

**2. Timeout manager is configuration-only (no asyncio)**
- Provides configuration for external timeout handling (subprocess.run, asyncio.timeout, etc.)
- get_timeout() returns timeout value (int) or None (no timeout)
- Caller applies timeout, manager just tracks approval state

**3. Dual checkpoint format (versioned + latest)**
- checkpoint_epoch_N.pt: Versioned checkpoints for specific epochs
- checkpoint_latest.pt: Latest checkpoint for easy resume without searching
- Enables both debugging (specific epoch) and production resume (latest)

**4. Signal handlers set flag rather than forcing save**
- SIGINT/SIGTERM set self.interrupted = True
- Training loop checks flag and handles cleanup
- Prevents race conditions from forced saves during signal handling

**5. torch.save() with pickle fallback**
- Prefers torch.save() for PyTorch models (atomic writes, proper tensor serialization)
- Falls back to pickle if torch not available (for non-PyTorch experiments)
- Both approaches save to same .pt extension for consistency

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

**Import verification complexity**
- Issue: Main grd package __init__.py imports notebook_executor which requires papermill dependency
- Resolution: Used importlib.util.spec_from_file_location to load modules directly without parent __init__.py
- Impact: Verification succeeded, no changes to production code needed

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Ready for integration:**
- Both modules are standalone and tested
- ExperimentTimeoutManager ready for integration in researcher agent
- CheckpointHandler ready for use in training scripts and notebooks
- Signal handlers registered automatically on CheckpointHandler instantiation

**Integration points:**
- Plan 09-03 will integrate hardware profiler during EDA
- Researcher agent will use ExperimentTimeoutManager for long-running experiment detection
- Training notebooks/scripts will use CheckpointHandler for resume support

**No blockers or concerns**

---
*Phase: 09-hardware-profiling-long-running*
*Completed: 2026-01-30*
