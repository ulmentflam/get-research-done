# Phase 7: REVISE_DATA Auto-Routing - Research

**Researched:** 2026-01-30
**Domain:** Agent orchestration, async task spawning, state management
**Confidence:** HIGH

## Summary

Phase 7 closes a high-priority tech debt item from Phase 4: automating the REVISE_DATA verdict path by having the Researcher agent auto-spawn the Explorer agent with targeted concerns from the Critic. Currently, REVISE_DATA requires manual user intervention to route back to /grd:explore - this phase eliminates that manual step to complete the fully autonomous recursive loop.

The research confirms that the GRD architecture already has all necessary primitives for this automation:
1. The Task tool for agent spawning (used extensively in Phase 4)
2. Structured Critic verdicts with extractable concerns (established in Phase 4)
3. The Explorer agent with --concerns flag support (created in Phase 2)
4. STATE.md tracking infrastructure (extended in Phases 1, 4, 5, 6)

The standard approach is to extend the Researcher agent's Step 7 routing logic to detect REVISE_DATA verdicts, extract targeted concerns from the Critic's recommendations, spawn Explorer via the Task tool with a formatted prompt, wait for Explorer completion, and then auto-continue the research loop without user intervention.

**Primary recommendation:** Use existing Task-based agent spawning pattern (proven in Phase 4 for Critic and Evaluator) to spawn Explorer on REVISE_DATA, extract concerns via regex from CRITIC_LOG.md, and leverage STATE.md to track data revision cycles.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Task tool | n/a | Agent spawning | Built-in Claude Code primitive for subagent spawning - used throughout GRD (Phases 4-6) |
| Markdown regex | Python stdlib | Critique parsing | No external dependencies, proven pattern in grd-researcher Step 7.3 |
| YAML frontmatter | PyYAML | Metadata parsing | Already in use for OBJECTIVE.md, config.yaml throughout GRD |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| STATE.md | n/a | Loop tracking | Update data revision history when Explorer spawns |
| CRITIC_LOG.md | n/a | Concern extraction | Parse recommendations section for data-specific issues |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Task tool spawning | Direct command routing | Task tool provides better context isolation and structured returns |
| Regex parsing | LLM extraction | Regex is deterministic and faster for structured markdown sections |
| Auto-spawn | Keep manual routing | Auto-spawn completes recursive loop, but manual preserves user control - Phase 4 decision was manual as interim |

**Installation:**
No new dependencies - uses existing GRD primitives and Task tool.

## Architecture Patterns

### Recommended Project Structure
```
agents/
├── grd-researcher.md       # UPDATE: Add Step 7.6 for REVISE_DATA auto-routing
└── grd-explorer.md         # EXISTING: Already supports --concerns flag (Phase 2)

get-research-done/templates/
├── state.md                # UPDATE: Add data_revisions tracking (minor extension)
└── critic-log.md           # EXISTING: Already has REVISE_DATA verdict section
```

### Pattern 1: Task-Based Agent Spawning (REVISE_DATA)
**What:** Spawn Explorer as subagent when Critic returns REVISE_DATA verdict
**When to use:** After parsing REVISE_DATA verdict in Researcher Step 7.3
**Example:**
```python
# Source: Phase 4 implementation (grd-researcher.md Step 7.2)
# Adapted for Explorer spawning on REVISE_DATA

if verdict == "REVISE_DATA":
    # Extract data concerns from Critic recommendations
    data_concerns = extract_data_concerns(
        weaknesses=weaknesses,
        recommendations=recommendations
    )

    # Format concerns for Explorer
    concerns_list = "\n".join([f"- {c}" for c in data_concerns])

    # Spawn Explorer via Task tool
    explorer_result = Task(prompt=f"""
<context>
@.planning/DATA_REPORT.md
@experiments/run_{run_num}_{description}/CRITIC_LOG.md

Critic identified potential data quality issues during experiment validation.
</context>

<concerns>
{concerns_list}
</concerns>

<instructions>
Re-analyze the dataset with focus on these specific concerns.
Append findings to DATA_REPORT.md under "## Revision: Iteration {iteration}" section.

Investigation scope:
{format_investigation_scope(data_concerns)}

After investigation, return:
- Updated findings for each concern
- Confidence level (HIGH/MEDIUM/LOW)
- Recommendation: proceed with revised understanding OR critical issue requires hypothesis reformulation
</instructions>

<output>
Append to DATA_REPORT.md and return structured result.
</output>
""", subagent_type="grd-explorer", model="sonnet", description="Re-analyze data with targeted concerns")

    # After Explorer completes, extract findings
    explorer_findings = parse_explorer_result(explorer_result)

    # Auto-continue research loop
    if explorer_findings['recommendation'] == 'proceed':
        # Increment iteration, return to Step 2 (Create Run Directory)
        return continue_research_loop(
            iteration=iteration + 1,
            context=explorer_findings
        )
    else:
        # Critical issue found - escalate to human
        return escalate_to_human(
            reason="Explorer found critical data issue",
            details=explorer_findings
        )
```

### Pattern 2: Concern Extraction from CRITIC_LOG.md
**What:** Parse structured recommendations to identify data-specific concerns
**When to use:** In REVISE_DATA routing logic (Step 7.6)
**Example:**
```python
# Source: grd-researcher.md Step 7.3 (verdict parsing pattern)
# Extended for concern extraction

def extract_data_concerns(weaknesses: List[str], recommendations: List[str]) -> List[str]:
    """Extract data-specific concerns from Critic feedback."""
    data_keywords = [
        'leakage', 'leak', 'data quality', 'distribution', 'drift',
        'feature', 'correlation', 'train-test', 'overlap', 'imbalance',
        'missing', 'outlier', 'anomaly', 'temporal', 'target'
    ]

    concerns = []

    # Check weaknesses for data-related issues
    for weakness in weaknesses:
        if any(keyword in weakness.lower() for keyword in data_keywords):
            concerns.append(weakness)

    # Check recommendations for data investigation requests
    for rec in recommendations:
        if any(keyword in rec.lower() for keyword in data_keywords):
            # Extract specific investigation request
            # e.g., "Investigate feature 'X' for leakage" -> "Feature 'X' potential leakage"
            concerns.append(rec)

    # Deduplicate and format
    return list(set(concerns))

def format_investigation_scope(concerns: List[str]) -> str:
    """Format concerns into Explorer investigation scope."""
    scope_items = []

    for concern in concerns:
        # Parse concern to determine investigation type
        if 'leakage' in concern.lower():
            scope_items.append(f"- Re-run leakage detection for: {extract_feature_names(concern)}")
        elif 'distribution' in concern.lower():
            scope_items.append(f"- Analyze distribution shift: {extract_feature_names(concern)}")
        elif 'train-test' in concern.lower():
            scope_items.append(f"- Verify train-test split integrity")
        else:
            scope_items.append(f"- Investigate: {concern}")

    return "\n".join(scope_items)
```

### Pattern 3: STATE.md Data Revision Tracking
**What:** Track REVISE_DATA cycles in STATE.md for iteration history
**When to use:** After spawning Explorer, before continuing loop
**Example:**
```markdown
## Research Loop State

### Data Revisions

| Iteration | Concerns | Explorer Result | Action Taken |
|-----------|----------|-----------------|--------------|
| 3 | Feature 'account_age' potential leakage | HIGH confidence leak confirmed, excluded from model | Researcher continues with revised features |
| 5 | Train-test overlap suspected | No overlap found, false positive | Researcher proceeds |
```

### Anti-Patterns to Avoid
- **Manual command instructions:** Don't return "Run /grd:explore with concerns..." - spawn Explorer automatically
- **Blocking on user input:** REVISE_DATA should auto-spawn and auto-continue, not wait for user
- **Lost concern context:** Don't just pass verdict - extract and format specific concerns from Critic recommendations
- **Infinite data loops:** Limit data revisions per hypothesis (e.g., max 2 REVISE_DATA cycles before ESCALATE)

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Agent spawning | Custom subprocess/exec | Task tool | Task tool provides context isolation, structured returns, error handling |
| Concern parsing | Custom NLP/embeddings | Regex + keyword matching | Structured markdown sections make regex deterministic and fast |
| State persistence | Custom JSON/DB | STATE.md markdown table | Already established pattern in Phases 4-5, human-readable audit trail |
| Iteration limits | Hardcoded checks | Configurable limit + cycle detection | Phase 4 established pattern: default 5, --limit flag override |

**Key insight:** The GRD architecture was designed for this - Task tool, structured verdicts, and STATE.md make REVISE_DATA auto-routing a natural extension of Phase 4's patterns, not a reimplementation.

## Common Pitfalls

### Pitfall 1: Context Loss in Explorer Spawn
**What goes wrong:** Explorer spawned without sufficient context from Critic findings, performs generic re-analysis instead of targeted investigation
**Why it happens:** Prompt doesn't reference CRITIC_LOG.md or format concerns clearly
**How to avoid:**
- Include @experiments/run_NNN/CRITIC_LOG.md in Explorer prompt
- Format concerns as bulleted list with investigation scope
- Pass iteration number so Explorer knows this is a revision, not initial EDA
**Warning signs:** Explorer generates generic DATA_REPORT.md updates that don't address Critic's specific concerns

### Pitfall 2: Infinite Data Revision Loops
**What goes wrong:** Critic repeatedly returns REVISE_DATA, Researcher keeps spawning Explorer, never converges
**Why it happens:** No limit on data revision cycles, unclear when data issue is fundamental vs. fixable
**How to avoid:**
- Track data_revision_count separate from iteration_count
- Limit data revisions (e.g., max 2 per hypothesis)
- After limit, force ESCALATE: "Data quality concerns persist after N revisions - hypothesis may not be viable"
**Warning signs:** STATE.md shows repeated REVISE_DATA verdicts with Explorer spawns

### Pitfall 3: Overwriting DATA_REPORT.md History
**What goes wrong:** Explorer overwrites original DATA_REPORT.md, losing baseline data profile
**Why it happens:** No versioning or append-only structure for data revisions
**How to avoid:**
- Append revisions as new sections: "## Revision: Iteration {N}"
- Keep original DATA_REPORT.md intact at top
- Include diff summary: "Changes from original analysis: ..."
**Warning signs:** Cannot compare current vs. original data profile, lost audit trail

### Pitfall 4: Not Checking Explorer Success Before Continuing
**What goes wrong:** Explorer fails or finds critical issue, but Researcher auto-continues anyway
**Why it happens:** No structured return parsing from Explorer Task spawn
**How to avoid:**
- Parse explorer_result for success/failure
- Check for "critical issue" flags in Explorer findings
- If critical: ESCALATE instead of continuing loop
- Log Explorer completion status in STATE.md
**Warning signs:** Research loop continues despite Explorer warnings of fundamental data problems

## Code Examples

Verified patterns from GRD codebase:

### Agent Spawning Pattern (Phase 4 Proven)
```python
# Source: grd-researcher.md Step 7.2 (Critic spawning)
# Pattern applies to Explorer spawning for REVISE_DATA

critic_verdict = Task(prompt=f"""
<experiment_artifacts>
Code: @experiments/run_{run_num}_{description}/code/train.py
Config: @experiments/run_{run_num}_{description}/config.yaml
Metrics: {json.dumps(metrics_summary, indent=2)}
</experiment_artifacts>

<objective_criteria>
@.planning/OBJECTIVE.md
...
</objective_criteria>

<instructions>
Evaluate this experiment implementation and results.
...
</instructions>

<output>
Return structured critique in format:
...
</output>
""", subagent_type="grd-critic", model="sonnet", description="Audit experiment and route verdict")
```

**Adaptation for Explorer:**
- Replace `subagent_type="grd-critic"` with `subagent_type="grd-explorer"`
- Include @CRITIC_LOG.md in artifacts section
- Format concerns in instructions section
- Request append-only update to DATA_REPORT.md

### Verdict Parsing Pattern (Phase 4 Established)
```python
# Source: grd-researcher.md Step 7.3
import re

verdict_match = re.search(r'\*\*Decision:\*\* (PROCEED|REVISE_METHOD|REVISE_DATA|ESCALATE)', critic_response)
verdict = verdict_match.group(1) if verdict_match else "ESCALATE"

confidence_match = re.search(r'\*\*Confidence:\*\* (HIGH|MEDIUM|LOW)', critic_response)
confidence = confidence_match.group(1) if confidence_match else "LOW"
```

**Extension for concern extraction:**
```python
# Extract recommendations section from CRITIC_LOG.md
recommendations_section = extract_section(critic_response, "## Recommendations", "## Reasoning")
recommendations = parse_list_items(recommendations_section)

# Filter for data-specific concerns
data_concerns = [r for r in recommendations if is_data_concern(r)]
```

### STATE.md Update Pattern (Phase 4-5 Proven)
```python
# Source: grd-researcher.md Step 7.7
def update_state_md(field: str, value: str):
    """Update STATE.md with loop tracking."""
    # Read current STATE.md
    with open('.planning/STATE.md', 'r') as f:
        state_content = f.read()

    # Update field (replace or append)
    updated_content = update_field_in_markdown(state_content, field, value)

    # Write back
    with open('.planning/STATE.md', 'w') as f:
        f.write(updated_content)
```

**Extension for data revision tracking:**
```python
def log_data_revision(iteration: int, concerns: List[str], result: str):
    """Append data revision entry to STATE.md."""
    state_md = read_file('.planning/STATE.md')

    # Format as markdown table row
    revision_entry = f"| {iteration} | {', '.join(concerns[:2])}... | {result} | {action} |"

    # Append to Data Revisions table
    state_md = append_to_table(state_md, "### Data Revisions", revision_entry)

    write_file('.planning/STATE.md', state_md)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual REVISE_DATA routing | Auto-spawn Explorer | Phase 7 (planned) | Completes fully autonomous recursive loop |
| Generic re-analysis | Targeted concern investigation | Phase 7 (planned) | Explorer re-analysis is scoped to Critic findings |
| Lost revision history | Append-only DATA_REPORT.md | Phase 7 (planned) | Audit trail of data understanding evolution |

**Deprecated/outdated:**
- Phase 4 manual routing decision: "REVISE_DATA requires manual routing" (04-04) - superseded by Phase 7 auto-routing

## Open Questions

Things that couldn't be fully resolved:

1. **How many data revision cycles before forced ESCALATE?**
   - What we know: Phase 4 has iteration_limit=5 for REVISE_METHOD
   - What's unclear: Should data revisions share same limit, or have separate limit?
   - Recommendation: Separate data_revision_limit=2 (data issues are more fundamental than method tuning)

2. **Should Explorer append or create versioned DATA_REPORT files?**
   - What we know: Single DATA_REPORT.md exists at .planning/DATA_REPORT.md
   - What's unclear: Append "## Revision" sections vs. create DATA_REPORT_v2.md
   - Recommendation: Append to single file with revision sections (simpler, maintains continuity)

3. **What if Explorer takes >10 minutes for large dataset re-analysis?**
   - What we know: Phase 9 (planned) addresses long-running experiments
   - What's unclear: Does this apply to Explorer spawns within REVISE_DATA?
   - Recommendation: Phase 7 assumes Explorer completes quickly (sampling), revisit in Phase 9 if needed

4. **Should REVISE_DATA auto-continue or gate to human?**
   - What we know: Phase 4 gates LOW confidence PROCEED to human
   - What's unclear: Should data revisions always auto-continue, or gate based on Explorer confidence?
   - Recommendation: Auto-continue unless Explorer flags "critical issue" (e.g., fundamental data quality problem)

## Sources

### Primary (HIGH confidence)
- agents/grd-researcher.md - Step 7 routing logic (Phase 4)
- agents/grd-critic.md - REVISE_DATA verdict structure (Phase 4)
- agents/grd-explorer.md - EDA workflow and --concerns flag (Phase 2)
- .planning/phases/04-recursive-validation-loop/04-04-PLAN.md - Loop orchestration implementation (Phase 4)
- .planning/STATE.md - Loop tracking infrastructure (Phases 1, 4, 5)

### Secondary (MEDIUM confidence)
- .planning/ROADMAP.md - Phase 7 success criteria and tech debt description
- .planning/PROJECT.md - Recursive loop philosophy and architecture decisions
- get-research-done/templates/critic-log.md - REVISE_DATA verdict template format

### Tertiary (LOW confidence)
- None - all research based on existing GRD codebase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Task tool, regex, STATE.md all proven in Phases 4-6
- Architecture: HIGH - Direct extension of Phase 4 patterns, no new primitives needed
- Pitfalls: MEDIUM - Pitfalls are anticipated (context loss, infinite loops) but not yet observed in production

**Research date:** 2026-01-30
**Valid until:** 2026-03-01 (30 days - GRD architecture is stable, internal codebase)
