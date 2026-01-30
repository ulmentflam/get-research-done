---
phase: 09-hardware-profiling-long-running
plan: 01
subsystem: infra
tags: [hardware-profiling, gpu-detection, duration-estimation, psutil, torch, gputil]

# Dependency graph
requires:
  - phase: 06-notebook-execution
    provides: "Notebook execution infrastructure requiring hardware context"
provides:
  - "Hardware profiling module capturing CPU, memory, disk, and GPU specs"
  - "Duration estimation for training and EDA experiments"
  - "Long-running experiment detection (>10 minutes)"
  - "Confidence levels for estimation quality"
affects: [07-recursive-validation, 02-exploration, 04-research]

# Tech tracking
tech-stack:
  added:
    - psutil (optional, for CPU/memory/disk profiling)
    - py-cpuinfo (optional, for detailed CPU specs)
    - GPUtil (optional, for GPU detection fallback)
    - torch.cuda (optional, preferred for GPU detection)
  patterns:
    - "Graceful degradation with missing dependencies"
    - "GPU detection hierarchy: torch.cuda > GPUtil > None"
    - "TFLOPs lookup table for duration estimation"
    - "50% efficiency factor for realistic training estimates"

key-files:
  created:
    - src/grd/hardware/__init__.py
    - src/grd/hardware/profiler.py
    - src/grd/hardware/estimator.py
  modified:
    - src/grd/__init__.py

key-decisions:
  - "PyTorch cuda preferred over GPUtil for ML workload GPU detection"
  - "Conservative 5.0 TFLOPs default for unknown GPU models"
  - "Long-running threshold set at 600 seconds (10 minutes)"
  - "Confidence levels based on GPU detection quality: HIGH (known GPU), MEDIUM (partial match), LOW (unknown/no GPU)"
  - "Lazy imports in grd package to avoid dependency conflicts"

patterns-established:
  - "HardwareProfile TypedDict: structured hardware context for reproducibility"
  - "DurationEstimate TypedDict: standardized experiment time estimates"
  - "Separate EDA and training duration estimation functions"
  - "Warning logs for missing dependencies, not errors"

# Metrics
duration: 2.5min
completed: 2026-01-30
---

# Phase 9 Plan 01: Hardware Profiling & Duration Estimation Summary

**Hardware profiling with GPU detection (torch.cuda/GPUtil) and ML-aware duration estimation using TFLOPs lookup table for reproducible experiments**

## Performance

- **Duration:** 2.5 min
- **Started:** 2026-01-30T18:43:48Z
- **Completed:** 2026-01-30T18:46:17Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Hardware profiler captures CPU (cores, frequency, architecture), memory (total/available), disk (total/free), and GPU (model, memory, CUDA version) context
- GPU detection with intelligent fallback: torch.cuda (preferred for ML) → GPUtil → None (graceful degradation)
- Training duration estimation using GPU TFLOPs lookup table with 50% efficiency factor
- EDA duration estimation based on data size and memory constraints
- Long-running experiment detection (>600 seconds) for timeout bypass workflow
- Confidence scoring (HIGH/MEDIUM/LOW) reflects GPU detection and estimation quality

## Task Commits

Each task was committed atomically:

1. **Task 1: Create hardware profiler module** - `674aabc` (feat)
2. **Task 2: Create duration estimator module** - `674aabc` (feat)

**Combined commit:** Both tasks committed together as cohesive feature

## Files Created/Modified

### Created
- `src/grd/hardware/__init__.py` - Package exports (capture_hardware_profile, estimate_training_duration, estimate_eda_duration, TypedDicts)
- `src/grd/hardware/profiler.py` - HardwareProfile capture with psutil/cpuinfo/torch/GPUtil
- `src/grd/hardware/estimator.py` - Duration estimation for training and EDA

### Modified
- `src/grd/__init__.py` - Lazy imports to prevent dependency conflicts

## Decisions Made

**1. PyTorch cuda preferred over GPUtil for GPU detection**
- Rationale: More reliable for ML workloads, provides compute capability and CUDA version
- Impact: Better GPU context for reproducibility, aligns with target domain (ML experiments)

**2. Conservative 5.0 TFLOPs default for unknown GPUs**
- Rationale: Better to overestimate duration than underestimate, prevents unexpected timeouts
- Impact: More generous time estimates for custom/new GPU models

**3. Long-running threshold at 600 seconds (10 minutes)**
- Rationale: Aligns with standard task timeout, clear boundary for user confirmation
- Impact: Experiments >10 minutes will require explicit approval in Phase 9 follow-up plans

**4. Lazy imports in grd package**
- Rationale: notebook_executor imports papermill at package load time, blocking hardware module usage
- Impact: Hardware module can be imported independently, no unnecessary dependencies loaded

**5. Separate EDA and training estimation functions**
- Rationale: EDA and training have fundamentally different performance characteristics
- Impact: More accurate estimates, simpler per-function logic

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Implemented lazy imports in grd/__init__.py**
- **Found during:** Task 1 verification (testing hardware module import)
- **Issue:** Direct imports of notebook_executor and graduation_validator at grd package load caused ModuleNotFoundError (papermill not installed). Blocked ability to import hardware module independently.
- **Fix:** Replaced direct imports with `__getattr__` lazy loading pattern. Functions only imported when accessed, not at package initialization.
- **Files modified:** src/grd/__init__.py
- **Verification:** Successfully imported `from grd.hardware import capture_hardware_profile` without papermill dependency
- **Committed in:** 674aabc (combined with task commit)

---

**Total deviations:** 1 auto-fixed (1 blocking issue)
**Impact on plan:** Essential fix to enable hardware module usage. No scope creep - maintains same API, just defers imports. Improves package modularity.

## Issues Encountered

**Missing optional dependencies (expected)**
- psutil, py-cpuinfo, GPUtil, torch not installed in test environment
- Gracefully handled per design - functions return partial profiles with warnings
- Not blocking - dependencies are optional and marked as such in research

**Shell customization warnings**
- zsh errors (`__zoxide_z`, `pay-respects`) are harmless shell plugin warnings
- Do not affect Python execution or module functionality

## User Setup Required

None - no external service configuration required.

**Optional dependencies:**
Users can install hardware profiling dependencies for full functionality:
```bash
pip install psutil py-cpuinfo gputil torch
```

If dependencies are missing, hardware module returns partial profiles with "Unknown" values and warning logs. System remains functional.

## Next Phase Readiness

**Ready for Phase 9 follow-up plans:**
- Hardware profiling infrastructure complete
- Duration estimation ready for integration with Explorer and Researcher agents
- Long-running detection flag enables timeout bypass workflow
- Confidence scoring enables quality-aware decision making

**Integration points prepared:**
- Explorer agent can call `capture_hardware_profile()` during EDA and include in DATA_REPORT.md
- Researcher agent can call `estimate_training_duration()` to detect long-running experiments
- Evaluator can reference hardware context for reproducibility verification

**No blockers.** Hardware profiling is a self-contained module with no external service dependencies.

---
*Phase: 09-hardware-profiling-long-running*
*Completed: 2026-01-30*
