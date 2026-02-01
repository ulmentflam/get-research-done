#!/bin/bash
# Verify Insights mode produced both output files
# Usage: ./scripts/verify-insights-mode.sh [planning-dir]

PLANNING_DIR="${1:-.planning}"

PASS=0
FAIL=0

# Check DATA_REPORT.md exists
if [ -f "$PLANNING_DIR/DATA_REPORT.md" ]; then
    echo "PASS: DATA_REPORT.md exists"
    ((PASS++))
else
    echo "FAIL: DATA_REPORT.md not found"
    ((FAIL++))
fi

# Check INSIGHTS_SUMMARY.md exists
if [ -f "$PLANNING_DIR/INSIGHTS_SUMMARY.md" ]; then
    echo "PASS: INSIGHTS_SUMMARY.md exists"
    ((PASS++))
else
    echo "FAIL: INSIGHTS_SUMMARY.md not found"
    ((FAIL++))
fi

# Check INSIGHTS_SUMMARY.md has expected sections
if [ -f "$PLANNING_DIR/INSIGHTS_SUMMARY.md" ]; then
    if grep -qi "TL;DR\|5 Things to Know\|What This Means" "$PLANNING_DIR/INSIGHTS_SUMMARY.md"; then
        echo "PASS: INSIGHTS_SUMMARY.md has expected sections"
        ((PASS++))
    else
        echo "WARN: INSIGHTS_SUMMARY.md may be missing expected sections"
    fi
fi

echo ""
echo "Summary: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && exit 0 || exit 1
