# Phase 5 Context: Human Evaluation Gate

**Created:** 2026-01-30
**Phase goal:** Humans make final validation decisions based on complete evidence packages

## Decisions

### Evidence Package Presentation

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Presentation style | Executive summary first | Lead with outcome, details on demand |
| Summary highlight | Hypothesis outcome | User wants to know pass/fail immediately |
| Drill-down approach | Claude decides | Adaptive based on context and complexity |
| Iteration history | Collapsed by default | Mention count, expand on request to avoid clutter |

**Implementation notes:**
- Executive summary should state: hypothesis, verdict (validated/failed/inconclusive), key metric
- Drill-down sections: Data characteristics, Iteration timeline, Critic reasoning, Full metrics
- Claude determines drill-down depth based on complexity and verdict confidence

### Decision Interface

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Decision options | Seal / Iterate / Archive | Three clear paths: accept, continue, abandon |
| Iterate routing | Auto-suggest based on Critic | Use Critic's last recommendation to guide next step |
| Confirmation flow | Confirm destructive only | Archive requires confirmation, Seal/Iterate don't |
| Rationale requirement | Required for Archive only | Document why hypothesis was abandoned |

**Implementation notes:**
- Seal = hypothesis validated, ready for production/publication
- Iterate = continue experimentation (Critic auto-suggests: REVISE_METHOD or REVISE_DATA path)
- Archive = abandon hypothesis, preserve as negative result
- Archive confirmation: "This will archive all runs. Are you sure? (requires rationale)"

### Decision Logging

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Storage location | Both | Per-run DECISION.md + central decision_log.md |
| Metadata captured | Minimal | Timestamp, decision, rationale (if provided) |
| Log organization | Chronological | Append-only, newest at bottom |
| Cross-references | Log references run only | Central log points to run directory |

**Implementation notes:**
- Per-run `DECISION.md` in `experiments/run_NNN/` with full context
- Central `human_eval/decision_log.md` as append-only summary
- Log entry format: `| 2026-01-30 | run_003_tuned | Seal | experiments/run_003_tuned/ |`
- No bidirectional links needed — log is source of truth for history

### Negative Results Preservation

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Archive location | experiments/archive/ | Flat archive directory |
| Archive metadata | ARCHIVE_REASON.md | Dedicated file explaining why it failed |
| Preservation scope | Final + summary | Keep final run, collapse others into summary |
| Directory structure | By date prefix | archive/2026-01-30_hypothesis_name/ |

**Implementation notes:**
- On Archive decision:
  1. Move final run to `experiments/archive/YYYY-MM-DD_hypothesis_name/`
  2. Create `ARCHIVE_REASON.md` with user's rationale
  3. Create `ITERATION_SUMMARY.md` collapsing other runs (count, verdict history, metric trend)
  4. Delete intermediate run directories (or optionally zip)
- Archive browsable for future reference: "what didn't work and why"

## Deferred Ideas

None captured during discussion.

## Open Questions for Research

1. How should evidence package be rendered? (Markdown sections vs interactive prompt)
2. Should Seal trigger any downstream actions? (e.g., copy to `validated/`, create release notes)
3. How to handle partial validation? (some metrics pass, others fail)

## Dependencies

- Requires Phase 4 complete (Researcher/Critic/Evaluator loop)
- Builds on: OBJECTIVE.md, DATA_REPORT.md, CRITIC_LOG.md, SCORECARD.json

---
*Context captured: 2026-01-30*
*Ready for: /grd:research-phase or /grd:plan-phase*
