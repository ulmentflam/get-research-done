# Phase 8: Baseline Orchestration - Research

**Researched:** 2026-01-30
**Domain:** Validation gates, dependency orchestration, experiment baseline enforcement
**Confidence:** HIGH

## Summary

Phase 8 implements validation gates that enforce baseline experiment completion before main experiments can proceed. This research identifies standard patterns for pre-condition validation, fail-fast error messaging, and multi-baseline comparison scenarios.

The GRD system already has precedent for validation patterns (graduation_validator.py with tiered error/warning system) and orchestration patterns (Researcher agent spawning Critic, then routing based on verdicts). Baseline orchestration extends these patterns with early validation gates at Researcher start and safety checks at Evaluator.

Key findings support the context decisions: fail-fast validation at Researcher start, actionable error messages with suggested commands, tiered validation (hard gate for primary baseline, soft warnings for secondary baselines), and validation caching to avoid re-checking within a session.

**Primary recommendation:** Implement baseline validation as a pure agent-level check using bash file existence tests, OBJECTIVE.md parsing, and clear error messages—no new Python modules needed. Follow existing GRD patterns of soft gates with actionable warnings.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pathlib | Python 3.10+ stdlib | File existence checking | Modern, object-oriented filesystem paths recommended for 2026 |
| json | Python stdlib | metrics.json validation | Built-in, no dependencies, sufficient for schema validation |
| bash test | shell builtin | Fast file existence checks | Zero overhead, agent-level validation pattern in GRD |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| jsonschema | 4.26+ | Optional: strict schema validation | If metrics.json structure validation needed beyond existence check |
| pyyaml | 6.0+ | OBJECTIVE.md frontmatter parsing | If switching from markdown to pure YAML config |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| bash test -f | pathlib.Path.exists() | Python module adds overhead for simple checks, bash faster for agent validation |
| Manual JSON parsing | pydantic models | Adds complexity, overkill for baseline validation use case |
| Custom validation framework | Reuse graduation_validator.py pattern | Graduation validator is notebook-specific, baseline validation is experiment-generic |

**Installation:**
```bash
# No installation needed - uses Python stdlib and bash builtins
# Optional: jsonschema if strict validation desired
pip install jsonschema>=4.26
```

## Architecture Patterns

### Recommended Validation Flow
```
Researcher agent start (Step 1.1)
├── Parse OBJECTIVE.md baselines section
├── For each baseline defined:
│   ├── Check experiments/{baseline_run}/ exists
│   ├── Check metrics.json exists in baseline run
│   └── Validate metrics.json contains required metrics
├── If primary baseline missing: BLOCK with actionable error
├── If secondary baselines missing: WARN but proceed
└── Continue to experiment implementation

Evaluator agent start (Step 1)
├── Re-validate baseline still exists (safety check)
├── Load baseline metrics for comparison
└── Generate SCORECARD with baseline comparison table
```

### Pattern 1: Fail-Fast Validation Gate

**What:** Check baseline existence at Researcher agent start (Step 1.1, immediately after loading OBJECTIVE.md)

**When to use:** Primary baseline defined in OBJECTIVE.md

**Example:**
```bash
# Source: Fail-fast pattern research + GRD agent patterns
# In grd-researcher.md Step 1.1 (after OBJECTIVE.md parsing)

# Extract baselines from OBJECTIVE.md frontmatter
BASELINES=$(grep -A 10 "^## Baselines" .planning/OBJECTIVE.md | grep -E "^\|" | tail -n +2 | head -n -1)
PRIMARY_BASELINE=$(echo "$BASELINES" | head -n 1 | awk -F'|' '{print $2}' | xargs)

if [ -n "$PRIMARY_BASELINE" ]; then
  # Check if baseline run exists
  BASELINE_RUN=$(find experiments/ -maxdepth 1 -type d -name "*_${PRIMARY_BASELINE}" | head -n 1)

  if [ -z "$BASELINE_RUN" ]; then
    echo "ERROR: Baseline experiment required but not found"
    echo ""
    echo "OBJECTIVE.md defines baseline: ${PRIMARY_BASELINE}"
    echo "But no run directory exists for this baseline."
    echo ""
    echo "Action required:"
    echo "  /grd:research --baseline ${PRIMARY_BASELINE}"
    echo ""
    echo "Or to proceed without baseline (not recommended):"
    echo "  /grd:research --skip-baseline"
    exit 1
  fi

  # Check metrics.json exists
  if [ ! -f "${BASELINE_RUN}/metrics.json" ]; then
    echo "ERROR: Baseline run found but missing metrics.json"
    echo ""
    echo "Baseline run: ${BASELINE_RUN}"
    echo "Expected: ${BASELINE_RUN}/metrics.json"
    echo ""
    echo "This baseline may not have completed successfully."
    echo "Re-run baseline or use --skip-baseline to proceed anyway."
    exit 1
  fi

  echo "✓ Baseline validation passed: ${PRIMARY_BASELINE}"
fi
```

### Pattern 2: Metrics Completeness Check

**What:** Verify baseline metrics.json contains all metrics defined in OBJECTIVE.md

**When to use:** After confirming metrics.json exists

**Example:**
```bash
# Source: JSON validation research + GRD metrics patterns
# Uses jq for JSON parsing (available via nix/homebrew)

# Extract required metric names from OBJECTIVE.md
REQUIRED_METRICS=$(grep -A 20 "^## Success Metrics" .planning/OBJECTIVE.md | \
  grep -E "^\|" | tail -n +2 | head -n -1 | \
  awk -F'|' '{print $2}' | xargs | tr ' ' '\n')

# Check baseline metrics.json has all required metrics
BASELINE_METRICS=$(jq -r '.metrics | keys[]' "${BASELINE_RUN}/metrics.json" 2>/dev/null || echo "")

MISSING_METRICS=""
for metric in $REQUIRED_METRICS; do
  if ! echo "$BASELINE_METRICS" | grep -q "^${metric}$"; then
    MISSING_METRICS="${MISSING_METRICS}\n  - ${metric}"
  fi
done

if [ -n "$MISSING_METRICS" ]; then
  echo "WARNING: Baseline metrics incomplete"
  echo ""
  echo "Baseline: ${BASELINE_RUN}"
  echo "Missing metrics:${MISSING_METRICS}"
  echo ""
  echo "Comparison will be limited to available metrics."
  echo "Consider re-running baseline with current OBJECTIVE.md metrics."
fi
```

### Pattern 3: Multi-Baseline Validation

**What:** Handle primary (required) vs secondary (optional) baselines

**When to use:** OBJECTIVE.md defines multiple baselines for comparison

**Example:**
```bash
# Source: Context decisions + orchestration pattern research
# Primary baseline blocks, secondary baselines warn

# Parse all baselines from OBJECTIVE.md
BASELINE_COUNT=$(echo "$BASELINES" | wc -l)
PRIMARY_BASELINE=$(echo "$BASELINES" | head -n 1 | awk -F'|' '{print $2}' | xargs)
SECONDARY_BASELINES=$(echo "$BASELINES" | tail -n +2 | awk -F'|' '{print $2}' | xargs)

# Validate primary (blocking)
validate_primary_baseline "$PRIMARY_BASELINE"  # exits if missing

# Validate secondary (warning only)
MISSING_SECONDARY=""
for baseline in $SECONDARY_BASELINES; do
  BASELINE_RUN=$(find experiments/ -maxdepth 1 -type d -name "*_${baseline}" | head -n 1)
  if [ -z "$BASELINE_RUN" ]; then
    MISSING_SECONDARY="${MISSING_SECONDARY}\n  - ${baseline}"
  fi
done

if [ -n "$MISSING_SECONDARY" ]; then
  echo "WARNING: Secondary baselines missing"
  echo ""
  echo "Missing:${MISSING_SECONDARY}"
  echo ""
  echo "SCORECARD comparison will only include primary baseline."
  echo "Run additional baselines for more comprehensive comparison."
fi
```

### Anti-Patterns to Avoid

- **Late validation (after experiment runs):** Wastes compute time and researcher attention. Validate at Researcher start (fail fast).
- **Vague error messages:** "Baseline not found" without suggesting action. Always include the exact command to run.
- **Blocking on data hash mismatches:** Different data = different experiment, but shouldn't block. Warn instead.
- **Re-validating on every Evaluator call:** Cache validation results per session to avoid repeated filesystem checks.

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON schema validation | Custom dict traversal | jsonschema library or jq | Handles edge cases (missing keys, type mismatches, nested structures) |
| File existence with race conditions | Plain os.path.exists() | pathlib with try/except on operations | Avoids TOCTOU bugs between check and use |
| Baseline designation (primary vs secondary) | Custom YAML section | First-in-list convention | Simple, no extra syntax, follows common pattern |
| Validation caching | Custom timestamp tracking | Agent internal state variables | Persists across steps within agent execution |

**Key insight:** Baseline validation is simpler than it appears. Don't build validation infrastructure—use bash test commands, parse markdown with grep/awk, and rely on agent-level orchestration. The complexity is in clear error messages and multi-baseline logic, not validation mechanics.

## Common Pitfalls

### Pitfall 1: TOCTOU Race Conditions

**What goes wrong:** Check baseline exists, then later read metrics.json, but file deleted between checks.

**Why it happens:** Time-of-check-time-of-use race condition in filesystem operations.

**How to avoid:**
- Use try/except pattern when reading metrics.json instead of separate existence check
- Or accept the risk—baseline deletion during experiment is rare edge case
- Document: "Validation checks baseline at Researcher start; changes after this point not detected"

**Warning signs:** Intermittent "file not found" errors during Evaluator phase despite passing Researcher validation.

### Pitfall 2: Overly Strict Validation

**What goes wrong:** Block experiment when baseline used different dataset (data hash mismatch).

**Why it happens:** Interpreting "baseline" as "identical conditions" rather than "comparison point."

**How to avoid:**
- Warn on data hash mismatch but don't block
- Baseline with different data is still valid comparison (e.g., literature baseline on different dataset)
- Document in SCORECARD: "Baseline used different dataset (hash mismatch)"

**Warning signs:** Users frustrated by blocked experiments when baseline is conceptually valid.

### Pitfall 3: Silent Baseline Skipping

**What goes wrong:** --skip-baseline flag bypasses validation with no record in logs.

**Why it happens:** Override flag without logging creates audit trail gap.

**How to avoid:**
- Log skip-baseline usage to STATE.md: "Baseline validation skipped by user (--skip-baseline)"
- Include in SCORECARD metadata: "baseline_validation_skipped: true"
- Warn in /grd:evaluate: "No baseline comparison available (validation skipped)"

**Warning signs:** User confused why SCORECARD lacks baseline comparison, no record of decision.

### Pitfall 4: Incomplete Metrics Blocking

**What goes wrong:** Block when baseline has fewer metrics than current OBJECTIVE.md.

**Why it happens:** OBJECTIVE.md evolved since baseline was run, added new metrics.

**How to avoid:**
- Warn about missing metrics but proceed
- SCORECARD shows "N/A" for metrics without baseline values
- Document: "Baseline predates metric addition, comparison limited"

**Warning signs:** Cannot proceed with valid experiment because baseline is "outdated."

## Code Examples

Verified patterns from research and GRD codebase:

### Parsing OBJECTIVE.md Baselines
```bash
# Source: grep/awk patterns + GRD markdown conventions
# Extract baseline table from OBJECTIVE.md

parse_baselines() {
  local objective_file=".planning/OBJECTIVE.md"

  # Find ## Baselines section, extract table rows
  grep -A 20 "^## Baselines" "$objective_file" | \
    grep -E "^\|" | \
    tail -n +2 | \
    head -n -1 | \
    while IFS='|' read -r _ name type expected citation status _; do
      # Trim whitespace
      name=$(echo "$name" | xargs)
      type=$(echo "$type" | xargs)
      status=$(echo "$status" | xargs)

      # Output: name|type|status
      echo "${name}|${type}|${status}"
    done
}

# Usage:
# BASELINES=$(parse_baselines)
# PRIMARY=$(echo "$BASELINES" | head -n 1 | cut -d'|' -f1)
```

### Checking Metrics Completeness with jq
```bash
# Source: JSON validation research + jq documentation
# Verify baseline metrics.json has required keys

check_metrics_complete() {
  local baseline_run="$1"
  local required_metrics="$2"  # space-separated list

  local metrics_file="${baseline_run}/metrics.json"

  if [ ! -f "$metrics_file" ]; then
    echo "ERROR: metrics.json not found"
    return 1
  fi

  # Extract metric keys from JSON
  local available_metrics=$(jq -r '.metrics | keys[]' "$metrics_file" 2>/dev/null)

  # Check each required metric
  local missing=""
  for metric in $required_metrics; do
    if ! echo "$available_metrics" | grep -q "^${metric}$"; then
      missing="${missing} ${metric}"
    fi
  done

  if [ -n "$missing" ]; then
    echo "WARNING: Missing metrics:${missing}"
    echo "Comparison will be limited to available metrics."
    return 2  # Non-fatal warning
  fi

  return 0  # All metrics present
}
```

### Validation Caching in Agent State
```markdown
<!-- Source: GRD agent patterns (grd-researcher.md internal state) -->
<!-- Add to researcher agent internal state variables -->

### Baseline Validation State

Track validation results to avoid re-checking:
- baseline_validated: boolean (false until validated)
- baseline_run_path: string (cached path to baseline run directory)
- baseline_metrics_valid: boolean (true if completeness check passed)
- validation_warnings: list of warning messages

Cache remains valid for agent execution session. Reset on new /grd:research invocation.
```

### Multi-Baseline SCORECARD Comparison Table
```json
{
  "baseline_comparison": {
    "experiment_score": 0.857,
    "baselines": [
      {
        "name": "random_classifier",
        "type": "own_implementation",
        "score": 0.501,
        "improvement": 0.356,
        "improvement_pct": "71.1%",
        "significant": true
      },
      {
        "name": "prior_best_model",
        "type": "own_implementation",
        "score": 0.823,
        "improvement": 0.034,
        "improvement_pct": "4.1%",
        "significant": false
      },
      {
        "name": "literature_benchmark",
        "type": "literature_citation",
        "score": 0.840,
        "improvement": 0.017,
        "improvement_pct": "2.0%",
        "significant": "not_tested",
        "note": "Literature baseline from different dataset (hash mismatch)"
      }
    ],
    "primary_baseline": "random_classifier",
    "secondary_baselines": ["prior_best_model", "literature_benchmark"]
  }
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Validate at evaluation time | Fail-fast at experiment start | 2024-2025 industry shift | Saves compute time, clearer error messages |
| Binary pass/fail validation | Tiered errors/warnings | Modern CLI design (2026) | Distinguishes blocking vs advisory issues |
| Single baseline comparison | Multi-baseline tables | ML research best practices | Richer context for hypothesis validation |
| Manual baseline tracking | Automated dependency gates | Orchestration patterns (2026) | Reduces human error, enforces rigor |

**Deprecated/outdated:**
- Manual baseline run tracking: Modern systems auto-detect from run directories
- Blocking on all validation failures: Tiered validation (hard/soft gates) is current best practice
- Separate validation scripts: Agent-level validation integrated into workflow (no separate tools)

## Open Questions

Things that couldn't be fully resolved:

1. **Question: Should baseline validation cache persist across /grd:research invocations?**
   - What we know: GRD agents are stateless across command invocations, state persists only in files (STATE.md, run directories)
   - What's unclear: Whether to log "validated_baselines" to STATE.md for inter-command caching or re-validate each time
   - Recommendation: Re-validate each /grd:research start (simple, safe, minimal overhead). If performance issue emerges, add STATE.md caching in future phase.

2. **Question: How to designate primary baseline in multi-baseline scenarios?**
   - What we know: Context decisions say "primary baseline required, secondary optional" but no syntax specified
   - What's unclear: Use first-in-list convention, or add explicit "primary: true" flag in OBJECTIVE.md table?
   - Recommendation: **First-in-list convention** (simpler, no extra syntax, follows common pattern). Document in objective.md template: "First baseline listed is primary (required), subsequent baselines are secondary (optional)."

3. **Question: Should malformed metrics.json block or warn?**
   - What we know: Baseline must have metrics.json with required metrics; context says "minimum requirement: metrics.json exists"
   - What's unclear: If metrics.json exists but is invalid JSON, or has wrong structure—block or warn?
   - Recommendation: **Block if unparseable, warn if missing metrics**. Rationale: Unparseable JSON indicates failed experiment (shouldn't proceed), missing metrics is evolution issue (proceed with warning).

4. **Question: Skip-baseline logging strategy—STATE.md, run metadata, or both?**
   - What we know: Context says "logged warning" but doesn't specify location
   - What's unclear: Where to log the fact that --skip-baseline was used
   - Recommendation: **Both locations**. Log to STATE.md for session history, include in run README.md and SCORECARD.json metadata for per-run audit trail.

## Sources

### Primary (HIGH confidence)
- Python Validation Patterns: [Fail Fast Principle](https://www.codereliant.io/p/fail-fast-pattern), [Error Handling in CLI Tools](https://medium.com/@czhoudev/error-handling-in-cli-tools-a-practical-pattern-thats-worked-for-me-6c658a9141a9)
- File Validation: [Python File Existence Patterns 2026](https://thelinuxcode.com/python-checking-whether-files-and-directories-exist-practical-patterns-for-2026/), [Python argparse docs](https://docs.python.org/3/library/argparse.html)
- JSON Schema: [jsonschema 4.26.0 docs](https://python-jsonschema.readthedocs.io/), [jsonschema PyPI](https://pypi.org/project/jsonschema/)
- GRD codebase: graduation_validator.py (tiered validation pattern), grd-researcher.md (agent state and orchestration patterns)

### Secondary (MEDIUM confidence)
- Orchestration: [Data Pipeline Orchestration Tools 2026](https://dagster.io/learn/data-pipeline-orchestration-tools), [Multi-Agent Orchestration 2026](https://research.aimultiple.com/agentic-orchestration/)
- Multiple baseline design: [Multiple Baseline Design Wikipedia](https://en.wikipedia.org/wiki/Multiple_baseline_design), [Comparison Visualization Patterns](https://arxiv.org/html/2401.09289v1)

### Tertiary (LOW confidence)
- None—all key findings verified against primary sources

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Python stdlib, bash builtins, well-documented libraries
- Architecture: HIGH - Patterns verified in GRD codebase (graduation_validator.py) and research sources
- Pitfalls: MEDIUM - Based on general validation patterns and orchestration research, not GRD-specific validation experience

**Research date:** 2026-01-30
**Valid until:** 60 days (stable domain—validation patterns change slowly)
