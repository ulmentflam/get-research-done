# State Template

<!-- STATE.md template v2.0 - GRD research loop tracking -->

Template for `.planning/STATE.md` — the project's living memory.

---

## File Template

```markdown
# Project State

## Project Reference

See: .planning/PROJECT.md (updated [date])

**Core value:** [One-liner from PROJECT.md Core Value section]
**Current focus:** [Current experiment name]

## Current Position

Experiment: [X] of [Y] ([Experiment name])
Plan: [A] of [B] in current experiment
Status: [Ready to plan / Planning / Ready to execute / In progress / Experiment complete]
Last activity: [YYYY-MM-DD] — [What happened]

Progress: [░░░░░░░░░░] 0%

## Research Loop State

**Active Hypothesis:** {{hypothesis_id_or_none}}
**Objective:** {{brief_hypothesis_statement}}
**Status:** {{not_started|in_progress|pending_review|archived}}

### Current Iteration

- **Iteration:** {{N}} of {{limit}} (default limit: 5)
- **Current Run:** experiments/{{run_NNN_description}}
- **Phase:** {{researcher|critic|evaluator|human_review}}
- **Data Revisions:** {{data_revision_count}} of {{data_revision_limit}} (default limit: 2)

### Loop History

| Iteration | Run | Verdict | Confidence | Metrics Summary |
|-----------|-----|---------|------------|-----------------|
| 1 | run_001_baseline | REVISE_METHOD | MEDIUM | acc=0.72 |
| 2 | run_002_tuned | PROCEED | HIGH | acc=0.85 |

### Verdict Trend

- **Pattern:** {{improving|stagnant|degrading|mixed}}
- **Consecutive same verdicts:** {{N}}
- **Last 3 verdicts:** {{verdict1, verdict2, verdict3}}

### Human Decisions

| Timestamp | Decision | Rationale |
|-----------|----------|-----------|
| {{timestamp}} | {{Continue|Archive|Reset|Escalate}} | {{user_rationale}} |

### Data Revisions

Track REVISE_DATA cycles within current hypothesis:

| Iteration | Concerns | Explorer Result | Action Taken |
|-----------|----------|-----------------|--------------|
| {{N}} | {{concern_list}} | {{result_summary}} | {{action}} |

**Data Revision Limits:**
- Current count: {{data_revision_count}} of {{data_revision_limit}}
- If limit reached: Escalate to human (data quality may be insufficient for hypothesis)

## Performance Metrics

**Velocity:**
- Total plans completed: [N]
- Average duration: [X] min
- Total execution time: [X.X] hours

**By Experiment:**

| Experiment | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| - | - | - | - |

**Recent Trend:**
- Last 5 plans: [durations]
- Trend: [Improving / Stable / Degrading]

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Experiment X]: [Decision summary]
- [Experiment Y]: [Decision summary]

### Research Decisions

| Decision | Iteration | Impact |
|----------|-----------|--------|
| {{decision_description}} | {{N}} | {{what_changed}} |

### Pending Todos

[From .planning/todos/pending/ — ideas captured during sessions]

None yet.

### Blockers/Concerns

[Issues that affect future work]

None yet.

### Research Blockers

- **Current:** {{blocker_or_none}}
- **Requires:** {{human_action|data_fix|method_change}}

### Research Blockers

- **Current:** {{blocker_or_none}}
- **Requires:** {{human_action|data_fix|method_change}}

## Session Continuity

Last session: [YYYY-MM-DD HH:MM]
Stopped at: [Description of last completed action]
Resume file: [Path to .continue-here*.md if exists, otherwise "None"]

## Research Loop History

**Active Loop:** [N/A - no active research loop]
**Loop Status:** [idle/exploring/synthesizing/validating/complete]

| Loop | Started | Focus Area | Status | Outcome |
|------|---------|------------|--------|---------|
| - | - | - | - | - |

**Current Loop Progress:**
- [ ] Data reconnaissance (Explorer)
- [ ] Hypothesis synthesis (Architect)
- [ ] Implementation (Researcher)
- [ ] Validation (Critic)
- [ ] Evaluation (Evaluator)

**Loop Notes:**
_Notes from current research iteration appear here_
```

<purpose>

STATE.md is the project's short-term memory spanning all experiments and sessions.

**Problem it solves:** Information is captured in summaries, issues, and decisions but not systematically consumed. Sessions start without context.

**Solution:** A single, small file that's:
- Read first in every workflow
- Updated after every significant action
- Contains digest of accumulated context
- Enables instant session restoration

</purpose>

<lifecycle>

**Creation:** After ROADMAP.md is created (during init)
- Reference PROJECT.md (read it for current context)
- Initialize empty accumulated context sections
- Set position to "Experiment 1 ready to plan"

**Reading:** First step of every workflow
- progress: Present status to user
- plan: Inform planning decisions
- execute: Know current position
- transition: Know what's complete

**Writing:** After every significant action
- execute: After SUMMARY.md created
  - Update position (experiment, plan, status)
  - Note new decisions (detail in PROJECT.md)
  - Add blockers/concerns
- transition: After experiment marked complete
  - Update progress bar
  - Clear resolved blockers
  - Refresh Project Reference date

</lifecycle>

<sections>

### Project Reference
Points to PROJECT.md for full context. Includes:
- Core value (the ONE thing that matters)
- Current focus (which experiment)
- Last update date (triggers re-read if stale)

Claude reads PROJECT.md directly for requirements, constraints, and decisions.

### Current Position
Where we are right now:
- Experiment X of Y — which experiment
- Plan A of B — which plan within experiment
- Status — current state
- Last activity — what happened most recently
- Progress bar — visual indicator of overall completion

Progress calculation: (completed plans) / (total plans across all experiments) × 100%

### Performance Metrics
Track velocity to understand execution patterns:
- Total plans completed
- Average duration per plan
- Per-experiment breakdown
- Recent trend (improving/stable/degrading)

Updated after each plan completion.

### Accumulated Context

**Decisions:** Reference to PROJECT.md Key Decisions table, plus recent decisions summary for quick access. Full decision log lives in PROJECT.md.

**Pending Todos:** Ideas captured via /grd:add-todo
- Count of pending todos
- Reference to .planning/todos/pending/
- Brief list if few, count if many (e.g., "5 pending todos — see /grd:check-todos")

**Blockers/Concerns:** From "Next Experiment Readiness" sections
- Issues that affect future work
- Prefix with originating experiment
- Cleared when addressed

### Session Continuity
Enables instant resumption:
- When was last session
- What was last completed
- Is there a .continue-here file to resume from

### Research Loop History
Tracks recursive validation cycles (STATE-01 requirement):
- **Active Loop**: Which research loop is currently running (or N/A)
- **Loop Status**: Current stage (idle/exploring/synthesizing/validating/complete)
- **Loop Table**: History of completed and ongoing loops with outcomes
- **Current Loop Progress**: Checklist tracking which agents have contributed
- **Loop Notes**: Insights, decisions, and findings from the current iteration

When a research loop starts (future experiments), this section tracks:
- Explorer's data reconnaissance
- Architect's hypothesis synthesis
- Researcher's implementation
- Critic's validation challenges
- Evaluator's metric assessments

This enables the recursive "hypothesis → experiment → validate → refine" cycle that distinguishes GRD from linear development workflows.

### Data Revisions Table

Tracks REVISE_DATA cycles within the current hypothesis:
- **Iteration**: Which experiment iteration triggered data revision
- **Concerns**: Summary of data concerns from Critic (truncated)
- **Explorer Result**: Outcome of re-analysis (addressed, critical issue, etc.)
- **Action Taken**: What happened next (loop continues, escalated, etc.)

Data revisions are tracked separately from method revisions because:
- Data issues are more fundamental than hyperparameter tuning
- Lower limit (default 2) prevents infinite data loops
- Multiple data revisions suggest hypothesis may not be viable with current data

</sections>

<size_constraint>

Keep STATE.md under 100 lines.

It's a DIGEST, not an archive. If accumulated context grows too large:
- Keep only 3-5 recent decisions in summary (full log in PROJECT.md)
- Keep only active blockers, remove resolved ones

The goal is "read once, know where we are" — if it's too long, that fails.

</size_constraint>
