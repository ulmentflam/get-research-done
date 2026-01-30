# Phase 5: Human Evaluation Gate - Research

**Researched:** 2026-01-30
**Domain:** CLI decision gates, evidence presentation, experiment decision logging
**Confidence:** HIGH

## Summary

Phase 5 implements a human-in-the-loop validation gate where researchers make final decisions on experiment outcomes after reviewing complete evidence packages. This phase bridges automated validation (Phase 4's Critic/Evaluator) with human strategic judgment.

The research focused on three core technical domains: (1) CLI patterns for interactive decision prompts with safe defaults and confirmation flows, (2) evidence package presentation following the inverted pyramid principle (executive summary first, details on demand), and (3) decision logging structures using markdown-based decision records with metadata tracking.

Key findings: Modern CLI tools use interactive prompts with visual emphasis for critical decisions, requiring explicit opt-in for destructive actions (like Archive). Evidence packages should lead with outcome/verdict, then provide drill-down sections based on complexity. Decision logs use append-only markdown tables with timestamps and minimal metadata, cross-referencing detailed decision files per run.

**Primary recommendation:** Build evidence presentation as adaptive Claude conversation (not static markdown dump), use AskUserQuestion for decision prompting with Archive requiring confirmation and rationale, implement dual logging (per-run DECISION.md + central decision_log.md), and preserve negative results in date-prefixed archive directories with ARCHIVE_REASON.md.

## Standard Stack

The established tools and patterns for this domain:

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| AskUserQuestion | Built-in | Interactive CLI decision prompts | Native Claude Code tool for user confirmation gates |
| Markdown | - | Decision log format | Human-readable, version-controllable, no parsing needed |
| Bash | 5.x | File operations, directory management | Universal CLI scripting for archiving and logging |

**Note:** This phase is CLI-orchestrated by Claude, not a standalone npm package. It uses Claude's native conversation capabilities for adaptive evidence presentation rather than static templates.

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Inquirer.js | 9.x+ | TypeScript CLI prompts (if needed) | If extending beyond Claude Code's native prompts |
| MADR | 3.x | Markdown decision record templates | Reference for decision log structure |
| Tree | Standard | Directory visualization | Show evidence package structure to user |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Claude conversation | Static markdown report | Static loses adaptability - can't adjust detail based on user questions |
| AskUserQuestion | Inquirer.js prompts | Inquirer requires Node.js implementation, AskUserQuestion is native |
| Markdown logs | SQLite database | DB adds complexity, markdown is human-readable and git-friendly |
| Append-only log | Git history only | Log provides quick chronological view without git archaeology |

**Installation:**

No npm packages required - uses Claude Code native capabilities + bash.

## Architecture Patterns

### Evidence Package Structure

```
experiments/run_003_tuned/
├── OBJECTIVE.md          # Original hypothesis (symlink to .planning/OBJECTIVE.md)
├── DATA_REPORT.md        # Data characteristics (symlink if exists)
├── CRITIC_LOG.md         # Critic's evaluation with verdict
├── metrics/
│   └── SCORECARD.json    # Quantitative evaluation results
├── code/                 # Experiment implementation
├── outputs/              # Model artifacts, predictions
└── logs/                 # Training logs
```

**Evidence package content (presented by Claude):**
1. OBJECTIVE.md → hypothesis context
2. DATA_REPORT.md → data characteristics
3. CRITIC_LOG.md → qualitative evaluation
4. SCORECARD.json → quantitative metrics

### Decision Log Structure

**Dual logging pattern:**

```
experiments/run_003_tuned/DECISION.md    # Per-run decision with full context
human_eval/decision_log.md               # Central append-only log
```

**Per-run DECISION.md:**
```markdown
# Human Decision: run_003_tuned

**Timestamp:** 2026-01-30T14:23:45Z
**Hypothesis:** [brief statement]
**Decision:** Seal | Iterate | Archive
**Rationale:** [user's reasoning]

## Evidence Summary
- Composite score: 0.87 (threshold: 0.80)
- Verdict: PROCEED (HIGH confidence)
- Key metric: F1=0.85 (target: >=0.80)

## Next Actions
[Seal] Hypothesis validated, ready for publication
[Iterate] Continue with: [specific direction]
[Archive] Reason: [why hypothesis abandoned]
```

**Central decision_log.md:**
```markdown
# Human Evaluation Decision Log

| Timestamp | Run | Decision | Reference |
|-----------|-----|----------|-----------|
| 2026-01-30 14:23 | run_003_tuned | Seal | experiments/run_003_tuned/ |
| 2026-01-29 10:15 | run_002_baseline | Iterate | experiments/run_002_baseline/ |
```

### Archive Structure for Negative Results

```
experiments/archive/2026-01-30_hypothesis_name/
├── ARCHIVE_REASON.md         # Why hypothesis failed
├── ITERATION_SUMMARY.md      # Collapsed history of all attempts
├── run_003_final/            # Final run preserved
│   ├── CRITIC_LOG.md
│   ├── SCORECARD.json
│   └── [all run artifacts]
└── metadata.json             # Archival metadata
```

### Pattern 1: Adaptive Evidence Presentation

**What:** Claude presents evidence conversationally, adjusting detail level based on user engagement

**When to use:** Always - this is the core pattern for Phase 5

**Example:**
```typescript
// Conceptual flow (implemented as Claude conversation, not code)

1. Present Executive Summary
   - Hypothesis statement
   - Verdict: VALIDATED / FAILED / INCONCLUSIVE
   - Key metric(s) vs threshold
   - Composite score

2. Assess User Response
   - User asks "How did it perform?" → Expand metrics section
   - User says "Archive this" → Confirm and capture rationale
   - User asks "What did Critic say?" → Show CRITIC_LOG highlights

3. Offer Decision Prompt
   - Only after user has reviewed evidence
   - Use AskUserQuestion with clear options
```

**Source:** Inspired by [inverted pyramid approach](https://openstax.org/books/principles-data-science/pages/10-3-effective-executive-summaries) for executive summaries

### Pattern 2: Confirmation for Destructive Actions

**What:** Archive decision requires explicit confirmation and mandatory rationale

**When to use:** When user selects "Archive" option

**Example:**
```typescript
// Conceptual AskUserQuestion flow
if (decision === "Archive") {
  confirmArchive = AskUserQuestion({
    header: "⚠️  Archive Confirmation",
    question: "This will archive all runs and mark hypothesis as failed. Continue?",
    options: ["Yes, archive with rationale", "Cancel"]
  });

  if (confirmArchive === "Yes, archive with rationale") {
    rationale = AskUserQuestion({
      header: "Archive Rationale",
      question: "Why is this hypothesis being abandoned? (will be saved in ARCHIVE_REASON.md)",
      type: "text" // Multi-line input
    });
  }
}
```

**Source:** [CLI confirmation best practices](https://www.nngroup.com/articles/confirmation-dialog/) - use initial: false for dangerous actions

### Pattern 3: Iterate Routing with Auto-Suggestion

**What:** When user chooses Iterate, system suggests next direction based on Critic's last recommendation

**When to use:** When decision is "Iterate" and CRITIC_LOG contains REVISE_METHOD or REVISE_DATA

**Example:**
```bash
# Extract Critic's last recommendation
LAST_RECOMMENDATION=$(grep -A 5 "## Recommendations" experiments/run_003/CRITIC_LOG.md | head -6)

# Present suggestion to user
echo "Critic suggested: $LAST_RECOMMENDATION"
echo ""
echo "Continue with: [REVISE_METHOD] or [REVISE_DATA]?"
```

**Source:** [Human-in-the-loop decision gates](https://parseur.com/blog/human-in-the-loop-ai) - system should provide context at decision points

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| CLI interactive prompts | Custom stdin parsing | AskUserQuestion (native) or Inquirer.js | Edge cases: terminal encoding, signal handling, input validation |
| Decision record format | Custom JSON schema | MADR markdown format | Established ADR format with tooling support, human-readable |
| Evidence presentation | Static markdown template | Claude adaptive conversation | Static templates can't adjust to user questions or confusion |
| Archive compression | Custom tar/zip logic | Built-in tar with bash | Handles permissions, symlinks, metadata correctly |
| Timestamp generation | Custom date formatting | ISO 8601 (`date -u +"%Y-%m-%dT%H:%M:%SZ"`) | Standard, sortable, timezone-aware |

**Key insight:** CLI decision gates require human factors engineering, not just technical implementation. Use native tools (AskUserQuestion), established patterns (MADR), and adaptive presentation (Claude) rather than building custom infrastructure.

## Common Pitfalls

### Pitfall 1: Information Overload in Evidence Package

**What goes wrong:** Dumping OBJECTIVE.md + DATA_REPORT.md + CRITIC_LOG.md + SCORECARD.json as raw text overwhelms user

**Why it happens:** Temptation to "show everything" for completeness, treating evidence package as file dump

**How to avoid:**
- Lead with executive summary (3-4 sentences)
- Highlight: hypothesis, verdict, key metric vs threshold
- Offer drill-down on demand: "Want to see Critic's reasoning?" or "Review data characteristics?"
- Use Claude's conversational ability to gauge user interest

**Warning signs:** User says "too much to read", asks "what's the bottom line?", or stops reading mid-package

**Source:** [Effective executive summaries](https://openstax.org/books/principles-data-science/pages/10-3-effective-executive-summaries) - inverted pyramid structure

### Pitfall 2: Missing Rationale for Archive Decisions

**What goes wrong:** User archives hypothesis without documenting why, losing valuable negative result knowledge

**Why it happens:** Rationale feels optional when you're frustrated with failed experiment

**How to avoid:**
- Make rationale REQUIRED for Archive decision (block without it)
- Prompt with specific questions: "What didn't work?", "What would need to change?", "What did we learn?"
- Show rationale preview before confirming archive
- Explain value: "This prevents future researchers from repeating this approach"

**Warning signs:** ARCHIVE_REASON.md contains generic text like "didn't work" or "metrics too low"

**Source:** [Publishing negative results](https://pmc.ncbi.nlm.nih.gov/articles/PMC6945059/) - well-documented failures save time

### Pitfall 3: Cycle Detection False Positives

**What goes wrong:** System flags "cycle" when user is legitimately exploring parameter space iteratively

**Why it happens:** Simple count-based detection (e.g., "3 REVISE_METHOD in a row = cycle")

**How to avoid:**
- Check if metrics are improving across iterations (trend analysis)
- Look for identical recommendations appearing repeatedly
- Consider metric delta: improving by 0.01 each time = progress, not cycle
- Escalate only when: same verdict + metrics stagnant + recommendations identical

**Warning signs:** User overrides "cycle detected" frequently, or says "I'm making progress"

**Source:** Phase 4 verification report - cycle detection mentioned in agents/grd-researcher.md line 891-916

### Pitfall 4: Lost Context in Central Decision Log

**What goes wrong:** decision_log.md entries lack enough context to understand decisions months later

**Why it happens:** Minimal metadata policy taken too far - only timestamp and decision

**How to avoid:**
- Include key metric value in log entry: "F1=0.85"
- Reference run directory for full context
- Add brief rationale excerpt (first sentence only) for Archive decisions
- Keep composite score in log

**Warning signs:** You read decision_log.md and can't remember why you made that decision

**Example good entry:**
```markdown
| 2026-01-30 14:23 | run_003_tuned | Seal | F1=0.85 (>0.80) | experiments/run_003_tuned/ |
```

## Code Examples

Verified patterns from system design and best practices:

### Executive Summary Presentation

```markdown
# Evidence Package: run_003_tuned

## Executive Summary

**Hypothesis:** Gradient boosting with temporal features outperforms baseline

**Verdict:** ✅ VALIDATED

**Key Results:**
- F1 Score: 0.85 (target: ≥0.80) ✓
- Composite Score: 0.87 (threshold: 0.80) ✓
- Critic Verdict: PROCEED (HIGH confidence)

**Recommendation:** Hypothesis validated. Ready to seal.

---

*Want to review?*
- Data characteristics → DATA_REPORT.md
- Critic's full evaluation → CRITIC_LOG.md
- Detailed metrics → SCORECARD.json
- Training logs → logs/
```

**Source:** Internal design - 05-CONTEXT.md decisions

### AskUserQuestion Decision Gate

```javascript
// Conceptual pattern (implemented in command orchestrator)

// Step 1: Present evidence summary (above)

// Step 2: Decision gate
const decision = await AskUserQuestion({
  header: "🔬 Experiment Complete: run_003_tuned",
  question: "How would you like to proceed?",
  options: [
    "Seal — Hypothesis validated, ready for production/publication",
    "Iterate — Continue experimentation (Critic will suggest next direction)",
    "Archive — Abandon hypothesis, preserve as negative result"
  ]
});

// Step 3: Handle decision
if (decision.includes("Seal")) {
  // Create DECISION.md, update decision_log.md, update STATE.md
  // No confirmation needed - affirmative decision
}

if (decision.includes("Iterate")) {
  // Extract Critic's last recommendation
  // Auto-suggest: REVISE_METHOD or REVISE_DATA
  // Route back to /grd:research with --continue
}

if (decision.includes("Archive")) {
  // Confirmation gate (destructive action)
  const confirm = await AskUserQuestion({
    header: "⚠️  Confirm Archive",
    question: "This will archive all runs and mark hypothesis as failed. Continue?",
    options: ["Yes, I want to archive", "Cancel"]
  });

  if (confirm.includes("Yes")) {
    // Capture rationale (REQUIRED)
    const rationale = await AskUserQuestion({
      header: "Archive Rationale",
      question: "Why is this hypothesis being abandoned? (saved in ARCHIVE_REASON.md)",
      type: "text" // Free-form input
    });

    // Execute archival process
  }
}
```

**Source:** [CLI confirmation patterns](https://www.thoughtworks.com/en-us/insights/blog/engineering-effectiveness/elevate-developer-experiences-cli-design-guidelines)

### Archive Directory Creation

```bash
#!/bin/bash
# Archive failed hypothesis with metadata

RUN_DIR="experiments/run_003_tuned"
HYPOTHESIS_NAME=$(grep "^# Hypothesis:" .planning/OBJECTIVE.md | sed 's/# Hypothesis: //' | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
DATE_PREFIX=$(date +%Y-%m-%d)
ARCHIVE_DIR="experiments/archive/${DATE_PREFIX}_${HYPOTHESIS_NAME}"

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

# Move final run
mv "$RUN_DIR" "$ARCHIVE_DIR/run_final"

# Create ARCHIVE_REASON.md
cat > "$ARCHIVE_DIR/ARCHIVE_REASON.md" <<EOF
# Archive Reason: $HYPOTHESIS_NAME

**Archived:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Original Hypothesis:** $(grep "^# Hypothesis:" .planning/OBJECTIVE.md | sed 's/# Hypothesis: //')

## Why This Failed

$USER_RATIONALE

## What We Learned

[To be filled: key insights from failed attempts]

## What Would Need to Change

[To be filled: conditions under which this might work]

---
*This negative result is preserved to prevent future researchers from repeating this approach.*
EOF

# Create ITERATION_SUMMARY.md (collapse other runs)
cat > "$ARCHIVE_DIR/ITERATION_SUMMARY.md" <<EOF
# Iteration Summary

| Iteration | Run | Verdict | Key Metric | Date |
|-----------|-----|---------|------------|------|
| 1 | run_001_baseline | REVISE_METHOD | F1=0.72 | 2026-01-28 |
| 2 | run_002_tuned | REVISE_METHOD | F1=0.76 | 2026-01-29 |
| 3 | run_003_final | ESCALATE | F1=0.78 | 2026-01-30 |

**Trend:** Metrics improved slowly but never reached threshold (F1≥0.80)

**Final decision:** Archived after 3 iterations, insufficient progress toward validation.
EOF

echo "✓ Archived to: $ARCHIVE_DIR"
```

**Source:** 05-CONTEXT.md implementation notes + [archiving best practices](https://www.infrrd.ai/blog/document-archiving-solutions-in-2026)

### Decision Log Append

```bash
#!/bin/bash
# Append decision to central log

DECISION_LOG="human_eval/decision_log.md"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
RUN_NAME="run_003_tuned"
DECISION="Seal"
KEY_METRIC="F1=0.85"
RUN_PATH="experiments/$RUN_NAME/"

# Create log if doesn't exist
if [ ! -f "$DECISION_LOG" ]; then
  mkdir -p human_eval
  cat > "$DECISION_LOG" <<EOF
# Human Evaluation Decision Log

| Timestamp | Run | Decision | Key Metric | Reference |
|-----------|-----|----------|------------|-----------|
EOF
fi

# Append entry (chronological, newest at bottom)
echo "| $TIMESTAMP | $RUN_NAME | $DECISION | $KEY_METRIC | $RUN_PATH |" >> "$DECISION_LOG"

echo "✓ Decision logged to $DECISION_LOG"
```

**Source:** [MADR decision log patterns](https://adr.github.io/madr/) - append-only chronological

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual experiment evaluation | Automated Critic + human gate | 2024-2025 | Critic catches obvious issues, human focuses on strategic decisions |
| Static reports | Adaptive conversation | Claude Code (2025) | Evidence presentation adjusts to user questions |
| Text file confirmation | Interactive CLI prompts | Modern CLI tools (2023+) | Safer with explicit opt-in for destructive actions |
| Git history only | Structured decision logs | ADR movement (2019+) | Quick chronological view without git archaeology |

**Deprecated/outdated:**
- Manual decision tracking in spreadsheets → Replaced by markdown decision logs (version controllable, human-readable)
- Confirmation dialogs in GUI → CLI uses AskUserQuestion with explicit options
- Deleting failed experiments → Archive with rationale (preserve negative results)

## Open Questions

Things that couldn't be fully resolved:

1. **Should Seal trigger downstream actions?**
   - What we know: CONTEXT.md defers this question to research phase
   - What's unclear: Whether to automatically copy to `validated/`, create release notes, or trigger publication workflow
   - Recommendation: Phase 5 only logs Seal decision. Downstream actions (if any) should be Phase 6 or user-initiated. Keep decision gate focused on validation, not publication.

2. **How to handle partial validation?**
   - What we know: SCORECARD.json has per-metric PASS/FAIL, but overall_result is binary
   - What's unclear: If 80% of metrics pass but one critical metric fails, is this Seal or Iterate?
   - Recommendation: Show metric breakdown in evidence summary. Let human decide based on which metrics failed. Critic should flag critical vs nice-to-have metrics in CRITIC_LOG.md.

3. **Should Archive preserve all runs or just final?**
   - What we know: CONTEXT.md says "final + summary", but storage tradeoff unclear
   - What's unclear: How much storage is acceptable for archived experiments?
   - Recommendation: Keep final run fully, collapse others into ITERATION_SUMMARY.md with key stats. Optionally: add `--archive-all` flag for full preservation if storage permits.

## Sources

### Primary (HIGH confidence)

- [AskUserQuestion tool](https://docs.anthropic.com/en/docs/claude-code) - Native Claude Code interactive prompts
- [CLI Design Guidelines](https://www.thoughtworks.com/en-us/insights/blog/engineering-effectiveness/elevate-developer-experiences-cli-design-guidelines) - Thoughtworks on developer experience
- [MADR: Markdown Architectural Decision Records](https://adr.github.io/madr/) - Decision log format standard
- [Effective Executive Summaries - OpenStax](https://openstax.org/books/principles-data-science/pages/10-3-effective-executive-summaries) - Data science communication
- 05-CONTEXT.md - User decisions from /grd:discuss-phase (locked choices)

### Secondary (MEDIUM confidence)

- [Confirmation Dialog Best Practices - NN/G](https://www.nngroup.com/articles/confirmation-dialog/) - When to confirm user actions
- [Human-in-the-Loop AI Guide - Parseur](https://parseur.com/blog/human-in-the-loop-ai) - HITL decision gates (2026 trends)
- [Publishing Negative Results - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6945059/) - Why document failures
- [CLI Progress Indicators - npm](https://npm-compare.com/cli-progress,cli-spinners,ora,progress) - Spinner/progress libraries
- [ML Experiment Tracking - Neptune.ai](https://neptune.ai/blog/ml-experiment-tracking) - Metadata tracking patterns

### Tertiary (LOW confidence)

- [Inquirer.js TypeScript](https://www.npmjs.com/package/inquirer) - Alternative to AskUserQuestion (not needed but referenced)
- [Document Archiving 2026 - Infrrd](https://www.infrrd.ai/blog/document-archiving-solutions-in-2026) - General archiving practices

## Metadata

**Confidence breakdown:**
- Evidence presentation: HIGH - Based on established executive summary patterns (OpenStax, data science communication standards) and Claude's adaptive conversation capabilities
- Decision interface: HIGH - AskUserQuestion is native Claude Code tool, confirmation patterns verified in UI/UX literature (NN/G)
- Decision logging: HIGH - MADR is established standard with tooling, markdown logs are proven in architecture decision records community
- Archiving: MEDIUM - Best practices from negative results publishing and clinical trial archiving, but GRD-specific implementation details designed from scratch

**Research date:** 2026-01-30
**Valid until:** 2026-02-28 (30 days - stable patterns, CLI tools mature)

**Key assumptions validated:**
- Claude Code supports AskUserQuestion with multi-line text input (confirmed in commands/grd/*.md usage)
- Markdown decision logs are human-readable and git-friendly (MADR standard)
- Adaptive evidence presentation is superior to static templates (OpenStax data science communication)
- Archive decisions should preserve context for future researchers (negative results publishing literature)

**Implementation risks:**
- LOW: Evidence presentation complexity - Claude handles conversational adaptation naturally
- LOW: Decision logging - Markdown is simple and proven
- MEDIUM: Archive disk usage - May need compression strategy if experiments generate large artifacts
- LOW: User confusion - Clear decision options and confirmation gates prevent errors
