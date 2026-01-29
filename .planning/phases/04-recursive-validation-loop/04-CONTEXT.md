# Phase 4: Recursive Validation Loop - Context

**Gathered:** 2026-01-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Experiments are validated through skeptical criticism with automatic routing back to earlier phases when anomalies detected. Researcher implements experiments from OBJECTIVE.md, Critic audits and routes (PROCEED/REVISE_METHOD/REVISE_DATA), and Evaluator generates quantitative scorecards. Each iteration is isolated in its own directory. Loop depth limits prevent infinite recursion.

</domain>

<decisions>
## Implementation Decisions

### Critic Decision Logic
- LLM reasoning for routing decisions (not rules-based) — flexible interpretation of experiment quality
- Structured critique output format: Strengths, Weaknesses, Verdict, Recommendations sections
- Critic decides case-by-case whether issue is data vs method — no fixed mapping
- Full history access: Critic sees all previous CRITIC_LOGS to avoid cycles and track progress
- Both levels of feedback on REVISE: general issue description + specific actionable suggestions when possible
- Evaluation anchored to OBJECTIVE.md success criteria first, then broader scientific skepticism
- Flag suspicious success: unusually high metrics trigger skeptical investigation for overfitting/leakage
- Ambiguous failures route to user: if Critic can't determine root cause, surface to human for routing decision
- Track trends across runs: note if metrics improving/degrading across iterations
- Include confidence level (HIGH/MEDIUM/LOW) in verdicts

### Experiment Isolation
- Full snapshot in each run_NNN directory: code, data refs, configs, logs, outputs, metrics
- Data handling via symlink/reference: point to shared data location, record hash/version for reproducibility
- Archive failed runs immediately: move to archive/ to keep experiments/ clean
- Descriptive naming: run_001_baseline, run_002_lr_sweep — human readable with incrementing prefix

### Researcher Output Format
- Both Python scripts and Jupyter notebooks supported — user chooses or Researcher infers from context
- Config file recommended but not required — suggest config.yaml for hyperparameters
- Brief README.md in each run: one-paragraph summary explaining what, why, how to reproduce

### Loop Escape Behavior
- Configurable max iterations (default: 5)
- Force human decision at limit: present evidence package, user must choose
- Human options: Continue (more iterations), Archive (give up), Reset (restart with new approach), Escalate (reformulate hypothesis entirely)

### Claude's Discretion
- PROCEED threshold: whether to allow "proceed with minor concerns noted" vs strict "no significant issues"
- Low-confidence PROCEED handling: when to gate to human for confirmation
- Separate vs combined iteration limits for REVISE_METHOD vs REVISE_DATA
- Code structure balance between template and flexibility based on experiment needs

</decisions>

<specifics>
## Specific Ideas

No specific references — open to standard approaches for ML experiment validation loops.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 04-recursive-validation-loop*
*Context gathered: 2026-01-28*
