# GRD v1.1 Validation Checklist

**Purpose:** Systematic manual testing of GRD workflow integrations with automated state verification.

**Created:** 2026-02-01
**Version:** v1.1
**Status:** Not executed

---

## Scenario 1: Progressive Exploration Path

**Success Criteria Reference:** SC-1 (Quick → Full → Architect flow)

### Setup

1. Fresh .planning/ directory with PROJECT.md initialized
2. Test data file at ./data/sample.csv with known characteristics
3. No existing DATA_REPORT.md or OBJECTIVE.md

### Steps

1. Run: `/grd:quick-explore ./data/sample.csv`
2. Verify: Quick mode execution completes without errors
3. Run: `./scripts/verify-quick-mode.sh` to confirm Quick Explore header
4. Run: `/grd:explore ./data/sample.csv`
5. Verify: Full profiling execution completes
6. Check: DATA_REPORT.md no longer has "Quick Explore Mode" header
7. Run: `/grd:architect`
8. Verify: Architect proceeds without warnings about insufficient data
9. Verify: OBJECTIVE.md created with testable hypothesis

### Verification

**Manual checks:**
- [ ] Quick-explore output displays Rich console formatting
- [ ] Full explore output contains comprehensive profiling
- [ ] Architect does NOT warn about data depth
- [ ] OBJECTIVE.md contains falsification criteria

**Automated checks:**
```bash
# After step 3
./scripts/verify-quick-mode.sh  # Should PASS

# After step 6
./scripts/verify-quick-mode.sh  # Should FAIL (no longer quick mode)

# After step 9
test -f .planning/OBJECTIVE.md && echo "PASS: OBJECTIVE.md exists"
```

### Expected Result

All steps complete without error. DATA_REPORT.md transitions from Quick mode header to full profiling. Architect proceeds normally without insufficient-data warnings.

### Status

[ ] Not run / [x] Pass / [!] Fail

---

## Scenario 2: Insights Path

**Success Criteria Reference:** SC-2 (Insights → Architect flow)

### Setup

1. Fresh .planning/ directory with PROJECT.md initialized
2. Test data file at ./data/sample.csv
3. No existing DATA_REPORT.md or INSIGHTS_SUMMARY.md

### Steps

1. Run: `/grd:insights ./data/sample.csv`
2. Verify: Insights mode execution completes
3. Run: `./scripts/verify-insights-mode.sh` to confirm both output files
4. Check: INSIGHTS_SUMMARY.md contains plain English narrative
5. Check: DATA_REPORT.md contains technical profiling
6. Run: `/grd:architect`
7. Verify: Architect proceeds without insufficient-data warnings
8. Verify: OBJECTIVE.md created

### Verification

**Manual checks:**
- [ ] INSIGHTS_SUMMARY.md uses plain English (no code, no jargon)
- [ ] INSIGHTS_SUMMARY.md has TL;DR, 5 Things to Know, What This Means sections
- [ ] DATA_REPORT.md has technical profiling suitable for Architect
- [ ] Architect does NOT warn about data depth

**Automated checks:**
```bash
# After step 3
./scripts/verify-insights-mode.sh  # Should PASS (both files exist)

# After step 8
test -f .planning/OBJECTIVE.md && echo "PASS: OBJECTIVE.md exists"

# Check INSIGHTS_SUMMARY.md has expected sections
grep -qi "TL;DR" .planning/INSIGHTS_SUMMARY.md && echo "PASS: TL;DR found"
grep -qi "5 Things to Know" .planning/INSIGHTS_SUMMARY.md && echo "PASS: 5 Things found"
grep -qi "What This Means" .planning/INSIGHTS_SUMMARY.md && echo "PASS: What This Means found"
```

### Expected Result

Insights mode produces both DATA_REPORT.md (technical) and INSIGHTS_SUMMARY.md (plain English). Architect proceeds without warnings because DATA_REPORT.md provides sufficient technical depth.

### Status

[ ] Not run / [x] Pass / [!] Fail

---

## Scenario 3: Quick-Only Warning Path

**Success Criteria Reference:** SC-3 (Architect warns on quick-explore-only data)

### Setup

1. Fresh .planning/ directory with PROJECT.md initialized
2. Test data file at ./data/sample.csv
3. No existing DATA_REPORT.md

### Steps

1. Run: `/grd:quick-explore ./data/sample.csv`
2. Verify: Quick mode execution completes
3. Run: `./scripts/verify-quick-mode.sh` to confirm Quick header
4. Run: `/grd:architect` WITHOUT running full explore
5. Observe output for warning about data depth
6. Run: `./scripts/verify-architect-warning.sh` for guidance on what to look for

### Verification

**Manual checks:**
- [ ] Architect output contains warning text about quick-explore data
- [ ] Warning suggests running full `/grd:explore` for comprehensive analysis
- [ ] Architect still proceeds but user is informed of limitation

**Expected warning patterns:**
- "'Quick Explore' data may be insufficient"
- "quick-explore only provides basic reconnaissance"
- "run full /grd:explore for comprehensive profiling"
- "data reconnaissance not completed"

**Automated checks:**
```bash
# After step 3
./scripts/verify-quick-mode.sh  # Should PASS

# After step 5
./scripts/verify-architect-warning.sh  # Provides verification guidance
```

### Expected Result

Architect detects Quick Explore mode header in DATA_REPORT.md and outputs warning text informing user that full explore is recommended. Architect proceeds with hypothesis synthesis but user is aware of data depth limitation.

### Status

[ ] Not run / [x] Pass / [!] Fail

---

## Scenario 4: REVISE_DATA Routing

**Success Criteria Reference:** SC-4 (Critic REVISE_DATA routes to full Explorer, not quick mode)

### Setup

1. Existing project with DATA_REPORT.md and OBJECTIVE.md
2. Running experiment in progress (via `/grd:research`)
3. Critic agent evaluating results

### Steps

1. Trigger REVISE_DATA verdict from Critic (simulate by observing actual research loop)
2. Observe Researcher spawning Explorer agent
3. Inspect task prompt sent to Explorer
4. Verify task prompt contains "full" or "detailed" mode indicators
5. Verify task prompt does NOT contain "quick" mode indicators
6. Confirm Explorer runs full profiling (not quick mode)

### Verification

**Manual checks:**
- [ ] Critic verdict is REVISE_DATA (not REVISE_METHOD or PROCEED)
- [ ] Researcher spawns Explorer with explicit mode specification
- [ ] Task prompt includes phrases like "targeted re-analysis" or "full profiling"
- [ ] Task prompt does NOT say "quick" or "summary only"
- [ ] Explorer output produces full DATA_REPORT.md (comprehensive)

**Mode detection verification:**
```bash
# Check Explorer mode detection patterns (from grd-explorer.md)
# Quick mode patterns to AVOID in REVISE_DATA:
#   - mode.*quick
#   - <profiling_mode>\s*quick
#   - quick.?explore
#   - quick mode
```

### Expected Result

When Critic issues REVISE_DATA, Researcher spawns Explorer in full profiling mode (not quick mode). Task prompt explicitly specifies full/detailed analysis. Explorer produces comprehensive DATA_REPORT.md suitable for addressing Critic's concerns.

### Status

[ ] Not run / [x] Pass / [!] Fail

---

## Scenario 5: Help Documentation Coverage

**Success Criteria Reference:** SC-5 (All v1.1 commands documented, no deprecated commands)

### Setup

1. Current .claude/commands/grd/ directory with help.md and command files
2. Audit script ready at scripts/audit-help-commands.sh

### Steps

1. Run: `./scripts/audit-help-commands.sh`
2. Verify: All v1.1 commands show [PASS]
3. Verify: All deprecated commands show [PASS] (not in help.md)
4. Verify: No undocumented command files
5. Check final audit result

### Verification

**V1.1 commands that MUST be documented:**
- [ ] /grd:quick-explore
- [ ] /grd:insights
- [ ] /grd:new-study
- [ ] /grd:complete-study
- [ ] /grd:scope-study
- [ ] /grd:plan-study
- [ ] /grd:run-study
- [ ] /grd:validate-study
- [ ] /grd:audit-study
- [ ] /grd:plan-study-gaps

**Deprecated commands that MUST NOT appear:**
- [ ] /grd:new-milestone
- [ ] /grd:complete-milestone
- [ ] /grd:discuss-phase
- [ ] /grd:execute-phase
- [ ] /grd:verify-work
- [ ] /grd:audit-milestone
- [ ] /grd:plan-milestone-gaps

**Automated checks:**
```bash
./scripts/audit-help-commands.sh
# Expected output:
#   V1.1 commands: 10 passed, 0 failed
#   Deprecated check: 7 passed, 0 failed
#   AUDIT PASSED: All v1.1 commands documented, no deprecated commands found
# Expected exit code: 0
```

### Expected Result

Audit script shows all 10 v1.1 commands documented in help.md. All 7 deprecated commands are NOT present in help.md. All command files have corresponding documentation. Exit code 0 (PASS).

### Status

[ ] Not run / [x] Pass / [!] Fail

---

## Summary

| Scenario | SC Ref | Status | Notes |
|----------|--------|--------|-------|
| Progressive Exploration Path | SC-1 | [ ] | Quick → Full → Architect |
| Insights Path | SC-2 | [ ] | Insights → Architect |
| Quick-Only Warning Path | SC-3 | [ ] | Quick → Architect warning |
| REVISE_DATA Routing | SC-4 | [ ] | Critic routing to full mode |
| Help Documentation Coverage | SC-5 | [ ] | Command audit |

**Execution date:** _____________
**Tester:** _____________
**Overall result:** [ ] All Pass / [ ] Partial / [ ] Fail

---

## Notes

Use this section to document any unexpected behavior, edge cases, or observations during validation testing.
