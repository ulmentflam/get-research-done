---
phase: "04"
plan: "02"
title: "Critic Agent & Structured Evaluation"
subsystem: "recursive-validation"
tags: ["critic-agent", "experiment-evaluation", "routing-logic", "scientific-skepticism"]
status: "complete"
completed: "2026-01-29"

dependencies:
  requires:
    - "03-01-SUMMARY.md: OBJECTIVE.md template with success criteria structure"
    - "02-01-SUMMARY.md: DATA_REPORT.md structure with leakage warnings"
  provides:
    - "grd-critic agent with LLM-based routing (PROCEED/REVISE_METHOD/REVISE_DATA/ESCALATE)"
    - "CRITIC_LOG.md template for structured critique output"
    - "Suspicious success detection for overfitting/leakage"
    - "Iteration history tracking to prevent cycles"
  affects:
    - "04-01: Researcher agent uses Critic verdict to determine next action"
    - "04-04: Workflow integration depends on Critic routing logic"

tech_stack:
  added: []
  patterns:
    - "LLM reasoning for routing decisions (not rule-based)"
    - "Confidence levels (HIGH/MEDIUM/LOW) with LOW gating to human"
    - "Structured critique format with strengths, weaknesses, reasoning"
    - "Scientific skepticism checks integrated into agent workflow"

file_tracking:
  created:
    - "agents/grd-critic.md: Critic agent with 7-step evaluation workflow"
    - "get-research-done/templates/critic-log.md: Template for CRITIC_LOG.md output"
  modified: []

decisions:
  - id: "04-02-01"
    title: "LLM reasoning for routing (not rules)"
    rationale: "Flexible interpretation of experiment quality requires context-aware reasoning, not rigid rule thresholds"
    impact: "Critic can handle edge cases and ambiguous failures that rules would miss"
  - id: "04-02-02"
    title: "Confidence levels gate LOW to human"
    rationale: "Never auto-proceed when Critic lacks confidence—prevent false positives in validation"
    impact: "Human confirmation required for PROCEED (LOW confidence) verdicts"
  - id: "04-02-03"
    title: "Suspicious success triggers investigation"
    rationale: "Unusually high metrics (>95%) often indicate overfitting or leakage, not legitimate performance"
    impact: "Critic flags and investigates perfect/near-perfect results before accepting them"
  - id: "04-02-04"
    title: "Iteration history tracking"
    rationale: "Detect cycles (same verdict repeated 3x) and trends (improving/stagnant/degrading) to guide routing"
    impact: "Escalate when stuck in loops, provide context on progress trajectory"

metrics:
  duration: "5min"
  tasks_completed: 2
  files_created: 2
  lines_added: 1254

context:
  blockers_resolved: []
  next_phase_readiness: "Ready for Phase 04-03 (Evaluator Agent) - Critic provides verdict that gates to Evaluator"
---

# Phase 04 Plan 02: Critic Agent & Structured Evaluation Summary

**One-liner:** LLM-powered Critic agent with four routing verdicts (PROCEED/REVISE_METHOD/REVISE_DATA/ESCALATE), confidence levels, and suspicious success detection

## What Was Built

Created the grd-critic agent—the scientific skeptic of the recursive validation loop. The Critic evaluates experiments against OBJECTIVE.md success criteria and uses LLM reasoning to route decisions, providing actionable feedback for revision paths.

**Key Outputs:**
1. **agents/grd-critic.md** (966 lines)
   - 7-step workflow: load context → evaluate metrics → apply skepticism → determine verdict → generate critique → write log → return verdict
   - All four verdicts with clear criteria:
     - PROCEED (HIGH/MEDIUM/LOW confidence)
     - REVISE_METHOD (implementation/hyperparameter issues)
     - REVISE_DATA (leakage/quality concerns → back to Explorer)
     - ESCALATE (ambiguous failures/cycles/strategic decisions)
   - Scientific skepticism checks:
     - Suspicious success detection (>95% metrics)
     - Train-test gap analysis (overfitting)
     - Reproducibility assessment (random seed, determinism)
     - Data integrity validation (leakage features excluded)
     - Code quality review (matches OBJECTIVE.md)
   - Iteration history tracking (detect cycles, trends)

2. **get-research-done/templates/critic-log.md** (288 lines)
   - Structured critique format: verdict, confidence, reasoning, metrics summary
   - Investigation notes: suspicious success, train-test gap, reproducibility, data integrity, code quality
   - Trend analysis with iteration history table
   - Next steps guidance for each verdict type (PROCEED → Evaluator, REVISE_METHOD → Researcher, REVISE_DATA → Explorer, ESCALATE → Human)
   - Falsification criteria tracking
   - Evidence package for escalations

**Architecture:**
- Critic reads OBJECTIVE.md for success criteria (metrics, thresholds, weights)
- Compares experiment metrics against thresholds, calculates weighted composite score
- Applies LLM reasoning to detect patterns (overfitting, leakage, quality issues)
- Routes to correct resolution path with specific actionable recommendations
- Tracks iteration history to detect cycles (same verdict 3x triggers escalation)
- LOW confidence PROCEED verdicts gate to human for confirmation

**Key Innovation:**
LLM reasoning instead of rigid rules. Critic interprets context (task complexity, data profile, implementation quality) to make nuanced routing decisions. This handles edge cases like "metrics pass but suspicious" or "metrics fail but unclear if data or method issue."

## Decisions Made

1. **LLM reasoning for routing (not rule-based)** - Flexible interpretation allows context-aware decisions. A rule-based system would struggle with ambiguous cases like "metrics pass but train-test gap suggests overfitting—is this acceptable or should we block?"

2. **Confidence levels (HIGH/MEDIUM/LOW) with LOW gating to human** - Prevents false positives. If Critic lacks confidence, don't auto-proceed—surface to human for judgment call.

3. **Suspicious success detection** - Metrics >95% on complex tasks often indicate problems, not success. Critic flags and investigates before accepting extraordinary claims.

4. **Iteration history tracking** - Detect cycles (REVISE_METHOD 3x without progress) and trends (improving/stagnant/degrading). Escalate when stuck in loops.

## Implementation Notes

**What went well:**
- 7-step workflow maps cleanly to scientific evaluation process
- All four verdicts have clear criteria and example scenarios
- Structured output format enables programmatic parsing if needed
- Edge cases documented (no previous logs, missing metrics, falsification criteria met)

**Deviations from plan:**
None—plan executed exactly as specified.

## Testing & Verification

All verification checks passed:
- ✓ Agent file exists with 7-step workflow (966 lines > 250 min)
- ✓ All four verdicts documented (PROCEED, REVISE_METHOD, REVISE_DATA, ESCALATE)
- ✓ Confidence levels (HIGH/MEDIUM/LOW) required in every verdict
- ✓ OBJECTIVE.md referenced (25 occurrences) for success criteria
- ✓ CRITIC_LOG references throughout agent
- ✓ Template file exists with all sections (288 lines > 40 min)
- ✓ Template has: verdict, confidence, reasoning, metrics, strengths, weaknesses, recommendations, trend analysis, next steps

**Key links verified:**
- agents/grd-critic.md → .planning/OBJECTIVE.md (reads success criteria)
- agents/grd-critic.md → experiments/run_NNN/CRITIC_LOG.md (writes structured critique)
- Pattern matches specification: file read for OBJECTIVE.md, file write for CRITIC_LOG

## Integration Points

**Upstream dependencies:**
- OBJECTIVE.md (from 03-01) provides success metrics, thresholds, weights, evaluation methodology
- DATA_REPORT.md (from 02-01) provides leakage warnings to check during evaluation

**Downstream impacts:**
- Researcher agent (04-01) receives verdict and acts: PROCEED → call Evaluator, REVISE_METHOD → tune and re-run, REVISE_DATA → call Explorer, ESCALATE → surface to human
- Evaluator agent (04-03) only runs if Critic returns PROCEED (any confidence level)
- Workflow integration (04-04) orchestrates the loop: Researcher → Critic → [verdict-based routing]

**Data flow:**
```
OBJECTIVE.md → Critic (load success criteria)
experiments/run_NNN/metrics.json → Critic (load experiment results)
experiments/run_NNN/train.py → Critic (review implementation)
experiments/run_*/CRITIC_LOG.md → Critic (load iteration history)
Critic → experiments/run_NNN/CRITIC_LOG.md (write structured critique)
Critic → Researcher (return verdict for routing)
```

## Lessons Learned

1. **LLM reasoning scales better than rules** - The flexibility to say "metrics pass but I'm suspicious" or "metrics fail but it's unclear why" is critical. Rigid thresholds would either miss issues or block legitimate results.

2. **Confidence levels prevent false positives** - LOW confidence PROCEED with human gate catches cases where "the numbers look okay but something feels wrong." This is exactly the skepticism we need.

3. **Structured output enables automation** - CRITIC_LOG.md format is human-readable but also parseable. Future tooling could extract verdicts, track trends, generate reports programmatically.

4. **Iteration tracking is essential** - Without cycle detection, the loop could run indefinitely with REVISE_METHOD → REVISE_METHOD → REVISE_METHOD. Tracking history lets us detect stagnation and escalate.

## Next Phase Readiness

✅ **Ready for Phase 04-03** (Evaluator Agent & Quantitative Benchmarking)

**What's ready:**
- Critic provides PROCEED verdict that gates entry to Evaluator
- Confidence level indicates whether human confirmation needed
- CRITIC_LOG.md captures full rationale for why experiment passed critique

**What Evaluator needs:**
- Read OBJECTIVE.md for benchmark configuration
- Run comprehensive evaluation suite (k-fold, bootstrap, statistical tests)
- Generate SCORECARD.json with detailed metrics
- No routing decisions—Evaluator just produces data for human evaluation gate

**Risks:**
None—Critic design is complete and ready for integration.

---

**Commits:**
- 44c3a74: feat(04-02): create grd-critic agent
- 2dbf7d3: feat(04-02): create CRITIC_LOG.md template

**Duration:** 5 minutes
**Files:** 2 created, 1254 lines total
**Status:** ✅ Complete
