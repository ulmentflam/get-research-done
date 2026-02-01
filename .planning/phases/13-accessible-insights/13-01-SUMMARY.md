---
phase: 13-accessible-insights
plan: 01
subsystem: insights
tags: [jinja2, nlg, narrative-generation, plain-english, business-intelligence]

# Dependency graph
requires:
  - phase: 12-quick-explore
    provides: "quick.py analysis functions, formatters.py"
provides:
  - insights.py module with generate_insights() function
  - insights_summary.md.j2 template for plain English output
  - data_report.md.j2 template for technical reports
  - Statistical explanation helpers (explain_row_count, explain_missing, etc.)
  - LLM prompt generation for further exploration
affects: [13-02, 14-integration-testing]

# Tech tracking
tech-stack:
  added: [Jinja2 3.1+]
  patterns: [template-based-narrative-generation, severity-aware-language, inverted-pyramid-structure]

key-files:
  created:
    - .claude/get-research-done/lib/templates/insights_summary.md.j2
    - .claude/get-research-done/lib/templates/data_report.md.j2
    - .claude/get-research-done/lib/insights.py
  modified: []

key-decisions:
  - "Template-based approach for narrative generation (not LLM) for consistency and speed"
  - "Two-output strategy: DATA_REPORT.md (technical) + INSIGHTS_SUMMARY.md (plain English)"
  - "Severity thresholds: >50% missing = critical, 20-50% = moderate, <20% = healthy"
  - "Reuse quick.py functions (detect_leakage_quick, generate_suggestions) to avoid duplication"
  - "LLM prompts include specific dataset context (row counts, column names, percentages)"

patterns-established:
  - "Inverted pyramid: TL;DR at top, 5 Things to Know, then detailed sections"
  - "What This Means pattern: every statistic gets plain English explanation"
  - "Action-oriented recommendations: specific code examples, not generic advice"
  - "Severity-aware language: emoji indicators + appropriate tone (critical/moderate/healthy)"

# Metrics
duration: 4min
completed: 2026-02-01
---

# Phase 13 Plan 01: Core Insights Module Summary

**Jinja2-templated insights generation with plain English explanations, severity-aware language, and LLM prompts for business analyst audience**

## Performance

- **Duration:** 4 min
- **Started:** 2026-02-01T13:10:00Z
- **Completed:** 2026-02-01T13:16:00Z
- **Tasks:** 3
- **Files created:** 3

## Accomplishments

- Created insights.py module (759 lines) with generate_insights() as main entry point
- Built insights_summary.md.j2 template with TL;DR, "5 Things to Know", severity-aware conditionals, recommendations, and LLM prompts
- Built data_report.md.j2 template for comprehensive technical reports
- Implemented explanation helpers for plain English statistical interpretations
- End-to-end test passed with sample data containing known issues

## Task Commits

Note: .claude/ directory is gitignored (local-only command files). Tasks were completed but no git commits were generated for code changes.

1. **Task 1: Create Jinja2 templates** - (no commit - gitignored)
2. **Task 2: Create insights.py module** - (no commit - gitignored)
3. **Task 3: Test insights generation** - (no commit - verification only)

## Files Created

- `.claude/get-research-done/lib/templates/insights_summary.md.j2` - Plain English summary template with inverted pyramid structure
- `.claude/get-research-done/lib/templates/data_report.md.j2` - Technical report template with comprehensive statistics
- `.claude/get-research-done/lib/insights.py` - 759-line insights generation orchestrator

## Decisions Made

1. **Template-based over LLM-based narrative:** Chose Jinja2 templates for consistency, speed, and predictability (avoids latency and cost of LLM calls)
2. **Dual output strategy:** DATA_REPORT.md for technical audience, INSIGHTS_SUMMARY.md for business analysts
3. **Reuse quick.py functions:** Imported detect_leakage_quick and generate_suggestions to avoid code duplication
4. **Installed Jinja2 dependency:** Added Jinja2 3.1.6 to support template rendering

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Installed missing Jinja2 dependency**
- **Found during:** Task 2 (insights.py import)
- **Issue:** Jinja2 package not installed, import failing
- **Fix:** Ran `pip install Jinja2`
- **Verification:** Module imports successfully

---

**Total deviations:** 1 auto-fixed (blocking dependency)
**Impact on plan:** Essential for Jinja2 template functionality. No scope creep.

## Issues Encountered

None - all tasks completed as planned.

## User Setup Required

None - Jinja2 installed automatically during execution.

## Next Phase Readiness

- insights.py module ready for integration with /grd:insights command (Phase 13-02)
- Templates tested and generating expected output
- All must_haves verified:
  - insights.py generates plain English explanations
  - INSIGHTS_SUMMARY.md has TL;DR at top
  - Severity-aware language adapts to findings
  - Recommendations include code examples
  - LLM prompts based on actual dataset findings

---
*Phase: 13-accessible-insights*
*Completed: 2026-02-01*
