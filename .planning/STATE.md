# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-27)

**Core value:** Structured ML experimentation with scientific rigor — from hypothesis to validated conclusion, with a Critic agent enforcing skepticism at every step

**Current focus:** Phase 6 in progress — notebook support

## Current Position

Phase: 6 of 6 (Notebook Support)
Plan: 3 of 5 complete (Researcher agent notebook support)
Status: In progress
Last activity: 2026-01-30 — Completed 06-03-PLAN.md

Progress: [████████████████████████████████████████████████░░] 93% (28/30 plans complete)

## Performance Metrics

**Velocity:**
- Total plans completed: 25
- Average duration: 3.1 min
- Total execution time: 1.33 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01 | 6 | 17.2min | 2.9min |
| 02 | 4 | 21.0min | 5.3min |
| 03 | 4 | 11.2min | 2.8min |
| 04 | 5 | 22.0min | 4.4min |
| 05 | 5 | 16.0min | 3.2min |
| 06 | 3 | 7.0min | 2.3min |

**Recent Trend:**
- Last 5 plans: 06-03 (3min), 06-02 (2min), 06-01 (2min), 05-05 (3min), 05-04 (3min)
- Trend: Phase 6 continuing with consistent velocity

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

| Decision | Made In | Impact |
|----------|---------|--------|
| Phase 5 verified and approved | 05-05 | All Human Evaluation Gate requirements (HUMAN-01/02/03) satisfied and human-approved |
| Use git mv for all renames to preserve file history | 01-01 | All directory and file renames tracked in git history |
| Rename directories and files before updating content | 01-01 | Structural changes complete before textual content updates |
| Preserve directory/package names during rebranding | 01-02 | Technical identifiers (get-shit-done paths, get-shit-done-cc package) stay unchanged until later plans update them |
| Use Unicode box-drawing for GRD ASCII art | 01-02 | Terminal branding pattern: filled-in block letters with cyan color |
| Fixed set-profile.md missing grd: prefix | 01-03 | Ensures consistent command invocation pattern across all 27 commands |
| Used word boundary matching for GSD→GRD replacements | 01-03 | Prevents accidental replacements in historical/legacy contexts |
| Bumped version to 2.0.0 for major rebrand | 01-05 | Signifies breaking change from get-shit-done-cc to get-research-done package |
| Extended STATE.md with research loop tracking | 01-05 | STATE.md v2.0 supports recursive validation cycles (STATE-01 requirement) |
| Reframed documentation for ML research focus | 01-05 | README examples now use ML workflows (train models, learning rate sweeps) instead of web app features |
| Human approved GRD branding | 01-06 | Final verification confirms rebrand complete with correct ASCII art and package identity |
| Created explore command with optional path argument | 02-01 | Supports both scripted (/grd:explore path) and interactive (prompts for path) usage |
| Structured Explorer with 10-step workflow | 02-01 | Clear separation: load → profile → distributions → missing → outliers → balance → leakage → recommendations → report → completion |
| Designed DATA_REPORT.md with severity thresholds | 02-01 | Blocking vs non-blocking classification with confidence levels for actionable prioritization |
| Use reservoir sampling for datasets >100k rows | 02-02 | Seed=42 for reproducibility, documents sampling in report |
| Dual outlier detection (Z-score + IQR) | 02-02 | Z-score for normal distributions, IQR for skewed data |
| MCAR/MAR/MNAR classification via statistical tests | 02-02 | Chi-square for categorical, t-test for numerical relationships |
| Cloud streaming with smart_open | 02-02 | Stream from S3/GCS without full download, uses environment auth |
| PyArrow backend for Parquet | 02-02 | Memory-mapped, columnar selection, zero-copy conversion |
| Leakage warnings are advisory only | 02-03 | User decides if warnings are actionable based on domain knowledge |
| Correlation thresholds: >0.90 feature-target, >0.95 feature-feature | 02-03 | Balances sensitivity with false positive minimization |
| Train-test overlap severity: HIGH if >1% of test | 02-03 | Pragmatic threshold that catches meaningful overlap |
| Confidence scoring for leakage (HIGH/MEDIUM/LOW) | 02-03 | Based on sample size and statistical significance, guides prioritization |
| Soft gate warns but doesn't block | 02-04 | /grd:architect warns if DATA_REPORT.md missing but allows proceeding - user decides if data-first needed |
| REVISE_DATA routes to targeted re-analysis | 02-04 | Critic can return to Explorer with specific concerns, appends to DATA_REPORT.md |
| Flexible prose hypothesis format | 03-01 | What/why/expected structure instead of rigid null/alternative hypothesis (research advisor feel) |
| Weighted metrics with composite scoring | 03-01 | Metrics have weights that must sum to 1.0, final success = weighted average |
| Evaluation methodology upfront | 03-01 | Strategy defined in OBJECTIVE.md before experiments to prevent p-hacking |
| Falsification criteria required | 03-01 | At least one criterion (quantitative preferred), guides Critic routing |
| Baseline warnings not blocking | 03-01 | System warns if baselines empty but allows proceeding |
| Use ## Phase markdown format in commands | 03-02 | Consistent with explore.md pattern, not XML &lt;step&gt; tags |
| Agent uses ## Step markdown format | 03-02 | 8-step execution flow for grd-architect |
| Max 15 iterations for refinement | 03-02 | Escape hatches: finalize/reset/continue after limit |
| Metric weight normalization automatic | 03-02 | If sum != 1.0, normalize automatically and log in completion message |
| Explicit Write tool call for artifacts | 03-02 | Agent must use Write tool explicitly, not implicit file generation |
| Validation implemented as inline agent guidance | 03-03 | Not executable code - agent applies rules using reasoning during Step 6 execution |
| Metric weights must sum to 1.0 | 03-03 | ERROR if invalid (±0.01 tolerance), blocks OBJECTIVE.md generation until fixed |
| Baseline missing is WARNING only | 03-03 | Soft gate warns but allows proceeding - user decides if baseline needed before experiments |
| Data characteristics extracted in Step 1.3 | 03-03 | Datetime columns, class imbalance, leakage warnings, missing data, sample size used for validation |
| Class imbalance + accuracy metric warning | 03-03 | If HIGH imbalance and accuracy selected, recommend F1/precision/recall/AUC instead |
| HIGH confidence leakage integrated | 03-03 | Warns if DATA_REPORT.md flagged leakage with HIGH confidence, lists features to exclude |
| Phase 3 workflow verified end-to-end | 03-04 | Complete hypothesis synthesis workflow integration confirmed - command, agent, template all properly wired |
| Hard gate on OBJECTIVE.md | 04-01 | /grd:research requires OBJECTIVE.md (cannot proceed without hypothesis) |
| Soft reference to DATA_REPORT.md | 04-01 | Optional context for experiment design, not required |
| Data referenced with SHA-256 hashes | 04-01 | Provenance tracking via hashing, symlinks not copies |
| Researcher spawns Critic internally | 04-01 | Command spawns Researcher, Researcher spawns Critic via Task tool |
| Four verdict types defined | 04-01 | PROCEED/REVISE_METHOD/REVISE_DATA/ESCALATE for Critic routing |
| Complete snapshot per run | 04-01 | Each experiments/run_NNN/ contains code, config, data refs, logs, outputs, metrics, critique |
| Default iteration limit set to 5 | 04-04 | Configurable via --limit flag, balances exploration with cost control |
| Cycle detection after 3 identical verdicts | 04-04 | Forces ESCALATE when same verdict repeats 3+ times with similar recommendations |
| LOW confidence PROCEED requires human gate | 04-04 | Prevents proceeding with uncertain experiments - human can approve, reject, or investigate |
| REVISE_DATA requires manual routing | 04-04 | Data analysis is complex - user must manually route to /grd:explore with specific concerns |
| Human decision gate offers 4 options | 04-04 | Continue (extend limit), Archive (abandon), Reset (fresh start), Escalate (reformulate) |
| Phase 4 verified and approved | 04-05 | All files, references, routing paths, and LOOP requirements validated - recursive loop ready for production |
| SCORECARD.json hard gate for /grd:evaluate | 05-01 | Cannot proceed to human evaluation without Evaluator quantitative benchmarks |
| Executive summary first with adaptive drill-down | 05-01 | Evidence presentation leads with outcome, Claude determines detail depth based on complexity and confidence |
| Archive requires confirmation and rationale | 05-01 | Prevents accidental archival - user must confirm and explain why hypothesis failed |
| Dual decision logging system | 05-01 | Per-run DECISION.md (detailed) + central decision_log.md (chronological table) for audit trail |
| Negative results preserved with learnings | 05-01 | Archive structure captures why failed, what was learned, and what would need to change for future researchers |
| Executive summary leads with outcome | 05-02 | Hypothesis, verdict (VALIDATED/FAILED/INCONCLUSIVE), key result, composite score presented first |
| Verdict categorization logic | 05-02 | VALIDATED = Critic PROCEED + composite >= threshold + overall PASS; FAILED = score < threshold OR overall FAIL; INCONCLUSIVE = LOW confidence or mixed results |
| Seal and Iterate no confirmation | 05-02 | Affirmative actions proceed directly to logging; only Archive (destructive) requires confirmation |
| Archive two-step confirmation | 05-02 | Confirm action → capture mandatory rationale (validates not empty, loops until provided) |
| Iterate auto-suggests direction | 05-02 | Extract Critic recommendation, parse for method vs data keywords, display suggested path in decision prompt |
| ITERATION_SUMMARY.md collapses runs | 05-02 | Archive template with iteration history table, metric trends, verdict distribution, key observations from all attempts |
| Central log references run only | 05-03 | decision_log.md points to run directory, no bidirectional links (simplifies structure) |
| STATE.md decision tracking | 05-03 | Human Decisions table + Research Loop State status updates maintain consistency across evaluations |
| Archive to experiments/archive/YYYY-MM-DD_hypothesis/ | 05-04 | Date-prefixed directories with sanitized hypothesis names for negative results preservation |
| Final run preserved as run_final/ | 05-04 | Move final run to archive with full structure, remove intermediate runs |
| ARCHIVE_REASON.md mandatory rationale | 05-04 | Template-based documentation with user rationale, best metrics, learnings, and conditions for future success |
| ITERATION_SUMMARY.md generation | 05-04 | Collapsed history table with metric trends, verdict distribution, and key observations from all attempts |
| metadata.json for archives | 05-04 | Programmatic access to archival context (timestamps, metrics, iteration counts) |
| decision_log.md updated to archive location | 05-04 | References point to experiments/archive/ not original experiments/run_NNN/ path |
| Mandatory random_seed parameter in execute_notebook_experiment | 06-01 | Enforces reproducibility at API level - ValueError if random_seed missing from parameters |
| Tiered graduation validation | 06-01 | Seeds block graduation (errors), paths/magics warn only (advisory warnings) |
| Retry-on-failure enabled by default | 06-01 | Transient errors handled with automatic retry before marking run as failed |
| Dual metrics storage (notebook + JSON) | 06-01 | Metrics in scrapbook AND metrics.json for programmatic access |
| Graduated script uses docstring header for metadata | 06-02 | Source notebook reference, run directory, and critic verdict embedded in module docstring rather than separate metadata file |
| Refactoring checklist as TODO comments | 06-02 | Embedded in graduated script template for manual completion post-graduation |
| Directory .gitkeep files as documentation | 06-02 | Dual-purpose files serve as git markers and directory documentation |
| Step 1.5 detects experiment type before run directory | 06-03 | Researcher agent determines notebook vs script experiment type early in workflow |
| README template uses conditional sections | 06-03 | Single template with notebook-specific sections rather than separate notebook/script templates |

### Pending Todos

None yet.

### Blockers/Concerns

**From Research:**
- Phase 5 integration: Technology versions (MLflow 2.9.x, DVC 3.x, uv stability) need verification at planning time

**Resolved:**
- ✓ Phase 4 complexity: Critic decision logic implemented with LLM-powered reasoning (04-02)
- ✓ Phase 4 risk: Iteration limit (default 5) and cycle detection prevent infinite loops (04-04)
- ✓ Phase 4 validation: Complete integration verified with human approval (04-05)

## Session Continuity

Last session: 2026-01-30 (execution)
Stopped at: Completed 06-03-PLAN.md (Researcher agent notebook support)
Resume file: None

---
*State initialized: 2026-01-27*
