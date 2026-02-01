#!/bin/bash
# Verify REVISE_DATA routing spawns Explorer in full mode (not quick)
# Usage: ./scripts/verify-revise-data-routing.sh

echo "=== REVISE_DATA Routing Verification ==="
echo ""

RESEARCHER_FILE=".claude/agents/grd-researcher.md"
EXPLORER_FILE=".claude/agents/grd-explorer.md"

PASS=0
FAIL=0

# Check researcher file exists
if [ ! -f "$RESEARCHER_FILE" ]; then
    echo "ERROR: $RESEARCHER_FILE not found"
    exit 1
fi

# Check Explorer file exists
if [ ! -f "$EXPLORER_FILE" ]; then
    echo "ERROR: $EXPLORER_FILE not found"
    exit 1
fi

echo "=== Task Prompt Analysis ==="
echo ""

# 1. Verify REVISE_DATA spawn prompt does NOT include quick mode indicators
echo "Checking REVISE_DATA spawn prompt..."

# Extract the Task prompt section for REVISE_DATA from researcher
# Look for "Route: REVISE_DATA" section and the Task prompt within it
REVISE_DATA_SECTION=$(sed -n '/Route: REVISE_DATA/,/Route: ESCALATE\|^##/p' "$RESEARCHER_FILE" 2>/dev/null)

# Check for quick mode indicators in the spawn prompt
if echo "$REVISE_DATA_SECTION" | grep -qi "profiling_mode.*quick\|<profiling_mode>\s*quick\|quick.?explore"; then
    echo "  [FAIL] REVISE_DATA spawn prompt contains quick mode indicator"
    ((FAIL++))
else
    echo "  [PASS] REVISE_DATA spawn prompt does NOT contain quick mode indicator"
    ((PASS++))
fi

# Check for targeted re-analysis indicator
if echo "$REVISE_DATA_SECTION" | grep -qi "targeted re-analysis\|revision.*not initial"; then
    echo "  [PASS] REVISE_DATA spawn prompt mentions targeted re-analysis"
    ((PASS++))
else
    echo "  [WARN] REVISE_DATA spawn prompt may not clearly indicate revision mode"
fi

# Check the spawn uses grd-explorer subagent
if echo "$REVISE_DATA_SECTION" | grep -qi 'subagent_type.*grd-explorer\|subagent_type="grd-explorer"'; then
    echo "  [PASS] REVISE_DATA spawns grd-explorer agent"
    ((PASS++))
else
    echo "  [FAIL] REVISE_DATA may not spawn grd-explorer agent"
    ((FAIL++))
fi

echo ""
echo "=== Mode Detection Regex Validation ==="
echo ""

# 2. Verify Explorer mode detection regex patterns
echo "Checking Explorer mode detection patterns..."

# Check that quick indicators exist in explorer
if grep -q "quick_indicators\|quick mode" "$EXPLORER_FILE"; then
    echo "  [PASS] Explorer has quick mode detection"
    ((PASS++))
else
    echo "  [FAIL] Explorer missing quick mode detection"
    ((FAIL++))
fi

# Check that insights indicators exist in explorer
if grep -q "insights_indicators\|insights mode" "$EXPLORER_FILE"; then
    echo "  [PASS] Explorer has insights mode detection"
    ((PASS++))
else
    echo "  [FAIL] Explorer missing insights mode detection"
    ((FAIL++))
fi

# Check default mode is full
if grep -qi "return 'full'\|default.*full" "$EXPLORER_FILE"; then
    echo "  [PASS] Explorer defaults to full mode"
    ((PASS++))
else
    echo "  [WARN] Explorer default mode unclear"
fi

echo ""
echo "=== Command Task Prompt Pattern Matching ==="
echo ""

# 3. Verify quick-explore command uses quick mode indicator
QUICK_CMD=".claude/commands/grd/quick-explore.md"
if [ -f "$QUICK_CMD" ]; then
    if grep -q '<profiling_mode>' "$QUICK_CMD" && grep -qi 'quick' "$QUICK_CMD"; then
        echo "  [PASS] quick-explore.md has <profiling_mode> quick"
        ((PASS++))
    else
        echo "  [FAIL] quick-explore.md missing proper mode indicator"
        ((FAIL++))
    fi
else
    echo "  [SKIP] quick-explore.md not found"
fi

# 4. Verify insights command uses insights mode indicator
INSIGHTS_CMD=".claude/commands/grd/insights.md"
if [ -f "$INSIGHTS_CMD" ]; then
    if grep -q '<profiling_mode>' "$INSIGHTS_CMD" && grep -qi 'insights' "$INSIGHTS_CMD"; then
        echo "  [PASS] insights.md has <profiling_mode> insights"
        ((PASS++))
    else
        echo "  [FAIL] insights.md missing proper mode indicator"
        ((FAIL++))
    fi
else
    echo "  [SKIP] insights.md not found"
fi

echo ""
echo "=== Summary ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "VERIFICATION PASSED: REVISE_DATA routes to full Explorer mode"
    exit 0
else
    echo "VERIFICATION FAILED: $FAIL issues found"
    exit 1
fi
