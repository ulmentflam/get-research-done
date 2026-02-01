# Phase 14: Integration Testing & Validation - Research

**Researched:** 2026-02-01
**Domain:** End-to-end workflow testing for Claude Code command orchestration
**Confidence:** HIGH

## Summary

This phase focuses on validating that all v1.1 GRD workflow paths function correctly end-to-end. Unlike typical software integration testing, GRD commands are Claude Code skill files (markdown) that orchestrate agent spawning, file creation, and state transitions. The "testing" approach must validate workflow behavior through scenario execution and state verification rather than traditional unit/integration test frameworks.

The research identified that GRD's testing domain is unique: commands are declarative prompts processed by Claude Code, not executable Python functions. Traditional pytest-based testing cannot directly invoke slash commands. Instead, integration validation requires:
1. Manual scenario execution with checklist verification
2. State file assertions (DATA_REPORT.md mode headers, warning presence, file existence)
3. Help documentation audits for command coverage

**Primary recommendation:** Create a validation checklist with specific test scenarios, expected outputs, and verification commands. Execute manually, document results, and add regression detection through pre-commit hooks that verify critical state patterns.

## Standard Stack

The established tools for this domain:

### Core

| Tool | Purpose | Why Standard |
|------|---------|--------------|
| Manual scenario execution | Primary test method | Claude Code commands cannot be programmatically invoked from pytest |
| Bash scripts | Verification automation | Check file existence, content patterns, state consistency |
| grep/ripgrep | Content assertions | Verify mode headers, warning text, command references |
| Pre-commit hooks | Regression prevention | Block commits if help.md diverges from available commands |

### Supporting

| Tool | Purpose | When to Use |
|------|---------|-------------|
| diff | Before/after state comparison | Comparing DATA_REPORT.md between modes |
| tree | Directory structure verification | Confirming expected files created |
| jq | JSON state parsing | config.json and SCORECARD.json validation |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual execution | pytest-subprocess simulation | Could mock CLI responses but misses agent behavior validation |
| Checklists | Automated UI testing | Claude Code has no stable UI automation interface |
| Pre-commit hooks | CI pipeline | Pre-commit catches issues locally before push |

**Installation:**
```bash
# Already available in project
pip install rich  # For formatted test output
```

## Architecture Patterns

### Recommended Test Structure

```
.planning/phases/14-integration-testing-validation/
├── 14-RESEARCH.md           # This file
├── 14-01-PLAN.md            # Workflow path validation plan
├── 14-02-PLAN.md            # Help documentation audit plan
├── VALIDATION_CHECKLIST.md  # Test scenarios with pass/fail
└── VALIDATION_RESULTS.md    # Execution results log
```

### Pattern 1: Scenario-Based Validation

**What:** Define explicit user journeys with expected outcomes
**When to use:** Every workflow path from success criteria
**Example:**

```markdown
## Scenario: Progressive Exploration Path

### Setup
- Fresh project with .planning/PROJECT.md
- Data file at ./data/sample.csv

### Steps
1. Run: /grd:quick-explore ./data/sample.csv
2. Verify: DATA_REPORT.md contains "Quick Explore Mode" header
3. Run: /grd:explore ./data/sample.csv
4. Verify: DATA_REPORT.md contains full profiling (no Quick header)
5. Run: /grd:architect
6. Verify: No "insufficient data" warning in output
7. Verify: OBJECTIVE.md created

### Expected Result
All steps complete without error. Architect proceeds with full data context.
```

### Pattern 2: State Assertion Scripts

**What:** Bash scripts that verify file state after command execution
**When to use:** Automate verification of expected patterns
**Example:**

```bash
#!/bin/bash
# verify-quick-mode.sh

DATA_REPORT=".planning/DATA_REPORT.md"

# Check file exists
if [ ! -f "$DATA_REPORT" ]; then
    echo "FAIL: DATA_REPORT.md not found"
    exit 1
fi

# Check for Quick Explore header
if grep -q "Quick Explore Mode" "$DATA_REPORT"; then
    echo "PASS: Quick Explore header present"
else
    echo "FAIL: Quick Explore header missing"
    exit 1
fi

# Check for full explore reminder
if grep -q "Run.*explore.*for complete analysis" "$DATA_REPORT"; then
    echo "PASS: Full explore reminder present"
else
    echo "WARN: Full explore reminder missing (non-blocking)"
fi
```

### Pattern 3: Help Documentation Audit

**What:** Verify help.md covers all actual commands
**When to use:** Prevent documentation drift after renames
**Example:**

```bash
#!/bin/bash
# audit-help-commands.sh

HELP_FILE=".claude/commands/grd/help.md"
COMMANDS_DIR=".claude/commands/grd"

# Get documented commands from help.md
DOCUMENTED=$(grep -oE '/grd:[a-z-]+' "$HELP_FILE" | sort -u)

# Get actual command files
ACTUAL=$(ls "$COMMANDS_DIR"/*.md 2>/dev/null | xargs -I{} basename {} .md | grep -v help | sort -u)

# Compare
echo "=== Commands in help.md but no file ==="
comm -23 <(echo "$DOCUMENTED" | sed 's|/grd:||') <(echo "$ACTUAL")

echo "=== Command files not in help.md ==="
comm -13 <(echo "$DOCUMENTED" | sed 's|/grd:||') <(echo "$ACTUAL")
```

### Anti-Patterns to Avoid

- **Anti-pattern: Testing agent internals:** Agent behavior is prompt-driven and non-deterministic. Test outcomes (files created, content patterns) not intermediate agent decisions.
- **Anti-pattern: Expecting exact output match:** Agent responses vary. Use pattern matching (contains, regex) not exact string comparison.
- **Anti-pattern: Skipping manual verification:** Automated scripts can verify state but human review catches UX issues that scripts miss.

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Command documentation sync | Custom documentation generator | Pre-commit hook checking help.md | Simple diff-based detection is sufficient |
| Test data generation | Synthetic data factories | Sample CSV with known characteristics | Tests need reproducible data, not complex generation |
| Workflow state machine | FSM implementation | Checklist verification | GRD workflows are linear paths, not complex state machines |
| Output capture | Complex logging framework | Manual observation + screenshots | Claude Code sessions are ephemeral, capture during execution |

**Key insight:** GRD integration testing is validation, not automation. The value is confirming workflows work before release, not building a permanent test suite that runs continuously.

## Common Pitfalls

### Pitfall 1: Trying to Automate Claude Code Command Invocation

**What goes wrong:** Attempting to call `/grd:quick-explore` from pytest or bash scripts
**Why it happens:** Natural instinct to automate testing like traditional software
**How to avoid:** Accept that Claude Code commands are invoked interactively. Use manual execution with automated verification of results.
**Warning signs:** Building complex subprocess wrappers that don't actually test agent behavior

### Pitfall 2: Testing Against Exact Output Text

**What goes wrong:** Tests break when agent wording changes slightly
**Why it happens:** Treating LLM output like deterministic code output
**How to avoid:** Test for presence of key patterns, not exact strings. Example: Check for "Quick Explore" header, not the full header text.
**Warning signs:** Frequent test failures after prompt tuning

### Pitfall 3: Ignoring Mode Detection Regex Accuracy

**What goes wrong:** Explorer agent misdetects mode, runs wrong analysis type
**Why it happens:** Regex patterns in grd-explorer.md may not match actual task prompts
**How to avoid:** Explicitly test that mode detection regex matches the task prompt format from each command (quick-explore, insights, explore)
**Warning signs:** Quick explore running full analysis, or insights mode producing only DATA_REPORT.md

### Pitfall 4: Missing Warning Text Verification

**What goes wrong:** Architect proceeds without warning when it should warn
**Why it happens:** Warning logic is in agent prompt, easy to miss verification
**How to avoid:** Test scenario: quick-explore only, then architect. Verify warning text appears.
**Warning signs:** Users get no feedback about insufficient data depth

### Pitfall 5: REVISE_DATA Routing to Wrong Command

**What goes wrong:** Critic routes REVISE_DATA but Explorer spawns quick mode instead of full
**Why it happens:** Task prompt from Researcher may not have explicit mode indicator
**How to avoid:** Verify Researcher's spawn prompt for REVISE_DATA explicitly says "full" or "detailed" mode
**Warning signs:** Data quality issues not caught on re-analysis after REVISE_DATA

## Code Examples

Verified patterns from the existing codebase:

### Mode Detection Regex (from grd-explorer.md)

```python
# Source: .claude/agents/grd-explorer.md lines 98-124
def detect_profiling_mode(task_prompt: str) -> str:
    """Determine if Explorer is in quick, insights, or full profiling mode."""
    import re

    # Check for quick mode indicator in task prompt
    quick_indicators = [
        r'mode.*quick',
        r'<profiling_mode>\s*quick',
        r'quick.?explore',
        r'quick mode'
    ]

    for pattern in quick_indicators:
        if re.search(pattern, task_prompt.lower()):
            return 'quick'

    # Check for insights mode indicator in task prompt
    insights_indicators = [
        r'mode.*insights',
        r'<profiling_mode>\s*insights',
        r'insights.?mode',
        r'business analyst audience',
        r'plain english'
    ]

    for pattern in insights_indicators:
        if re.search(pattern, task_prompt.lower()):
            return 'insights'

    return 'full'  # Default to full mode
```

### Verification Script: Quick Mode Header

```bash
#!/bin/bash
# verify-quick-header.sh
# Checks DATA_REPORT.md for Quick Explore mode header

DATA_REPORT="${1:-.planning/DATA_REPORT.md}"

if [ ! -f "$DATA_REPORT" ]; then
    echo "ERROR: $DATA_REPORT not found"
    exit 1
fi

# Pattern from quick.py generate_markdown_report()
if head -20 "$DATA_REPORT" | grep -q "Quick Explore Mode"; then
    echo "PASS: Quick Explore header found"
    exit 0
else
    echo "FAIL: Quick Explore header not found in first 20 lines"
    exit 1
fi
```

### Verification Script: Architect Warning Detection

```bash
#!/bin/bash
# verify-architect-warning.sh
# Run after /grd:architect when only quick-explore was done

# This must be run manually and output observed
# Pattern to look for in architect output:
#   "WARNING: No DATA_REPORT.md found"  (if no report)
#   or warning about insufficient data depth (if quick only)

echo "Manual verification required:"
echo "1. Run /grd:quick-explore on test data"
echo "2. Run /grd:architect"
echo "3. Verify warning appears about insufficient data depth"
echo ""
echo "Expected warning should mention one of:"
echo "  - 'Quick Explore' data may be insufficient"
echo "  - Run full /grd:explore for comprehensive analysis"
echo "  - Data reconnaissance not completed"
```

### Help Command Audit Script

```bash
#!/bin/bash
# audit-help-commands.sh
# Verify help.md documents all available commands

COMMANDS_DIR=".claude/commands/grd"
HELP_FILE="$COMMANDS_DIR/help.md"

echo "=== GRD Command Coverage Audit ==="
echo ""

# Count actual command files (excluding help itself)
ACTUAL_COUNT=$(ls "$COMMANDS_DIR"/*.md 2>/dev/null | grep -v help.md | wc -l | tr -d ' ')
echo "Command files found: $ACTUAL_COUNT"

# Count documented commands in help.md
DOCUMENTED_COUNT=$(grep -cE '^\*\*`/grd:' "$HELP_FILE" 2>/dev/null || echo 0)
echo "Commands in help.md: $DOCUMENTED_COUNT"

# Check specific v1.1 commands
echo ""
echo "=== V1.1 Command Verification ==="

V11_COMMANDS=(
    "quick-explore"
    "insights"
    "new-study"
    "complete-study"
    "scope-study"
    "plan-study"
    "run-study"
    "validate-study"
    "audit-study"
    "plan-study-gaps"
)

for cmd in "${V11_COMMANDS[@]}"; do
    if grep -q "/grd:$cmd" "$HELP_FILE"; then
        echo "  [PASS] /grd:$cmd documented"
    else
        echo "  [FAIL] /grd:$cmd NOT in help.md"
    fi
done

# Check for deprecated commands that should NOT be in help
echo ""
echo "=== Deprecated Commands (should NOT appear) ==="

DEPRECATED=(
    "new-milestone"
    "complete-milestone"
    "discuss-phase"
    "execute-phase"
    "verify-work"
    "audit-milestone"
    "plan-milestone-gaps"
)

for cmd in "${DEPRECATED[@]}"; do
    if grep -q "/grd:$cmd" "$HELP_FILE"; then
        echo "  [FAIL] /grd:$cmd still in help.md (should be removed)"
    else
        echo "  [PASS] /grd:$cmd not in help.md"
    fi
done
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Mocking Claude responses | Testing outcomes not responses | 2025 | More reliable validation |
| pytest for CLI testing | Manual + verification scripts | 2026 | Matches agentic workflow reality |
| CI-based integration tests | Pre-release validation checklist | 2026 | Faster feedback, less infrastructure |

**Deprecated/outdated:**
- Attempting to invoke Claude Code commands programmatically (not supported)
- Using pytest-subprocess for agent behavior testing (misses actual agent decisions)

## Open Questions

Things that couldn't be fully resolved:

1. **REVISE_DATA spawn prompt verification**
   - What we know: Critic issues REVISE_DATA verdict, Researcher spawns Explorer
   - What's unclear: Exact task prompt format Researcher uses for REVISE_DATA spawn
   - Recommendation: During validation, inspect actual spawn prompt to confirm "full" mode specified

2. **Warning text location in Architect output**
   - What we know: Architect should warn when DATA_REPORT.md is from quick-explore only
   - What's unclear: Where exactly this warning appears (console, file, or both)
   - Recommendation: Manual verification during test scenario execution

3. **Insights mode DATA_REPORT.md header**
   - What we know: Insights generates DATA_REPORT.md (technical) + INSIGHTS_SUMMARY.md
   - What's unclear: Whether DATA_REPORT.md from insights has distinct header
   - Recommendation: Check insights.py templates during validation

## Sources

### Primary (HIGH confidence)
- `.claude/agents/grd-explorer.md` - Mode detection patterns, profiling behavior
- `.claude/agents/grd-critic.md` - REVISE_DATA routing logic
- `.claude/commands/grd/architect.md` - DATA_REPORT.md soft gate logic
- `.claude/commands/grd/quick-explore.md` - Task prompt format for quick mode
- `.claude/commands/grd/insights.md` - Task prompt format for insights mode
- `.claude/commands/grd/help.md` - Current command documentation
- `.claude/get-research-done/lib/quick.py` - Quick mode output format
- `.claude/get-research-done/lib/insights.py` - Insights mode output format

### Secondary (MEDIUM confidence)
- [pytest documentation on fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) - Verified fixture patterns
- [pytest-subprocess](https://pypi.org/project/pytest-subprocess/) - Subprocess simulation patterns
- [Claude Code hooks guide](https://code.claude.com/docs/en/hooks-guide) - Hook-based validation patterns
- [Anthropic Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) - TDD with agentic coding

### Tertiary (LOW confidence)
- General integration testing patterns from web searches - Applied to unique domain

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Based on direct codebase analysis and Claude Code constraints
- Architecture: HIGH - Patterns derived from actual GRD implementation
- Pitfalls: MEDIUM - Based on codebase analysis, some scenarios need validation

**Research date:** 2026-02-01
**Valid until:** 2026-03-01 (stable domain, workflow commands unlikely to change structure)
