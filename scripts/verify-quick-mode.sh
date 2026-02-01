#!/bin/bash
# Verify DATA_REPORT.md contains Quick Explore Mode header
# Usage: ./scripts/verify-quick-mode.sh [path-to-data-report]

DATA_REPORT="${1:-.planning/DATA_REPORT.md}"

if [ ! -f "$DATA_REPORT" ]; then
    echo "ERROR: $DATA_REPORT not found"
    exit 1
fi

# Check for Quick Explore header in first 30 lines
if head -30 "$DATA_REPORT" | grep -qi "Quick Explore"; then
    echo "PASS: Quick Explore header found"
    exit 0
else
    echo "FAIL: Quick Explore header not found in first 30 lines"
    echo "Hint: This file may be from full explore mode"
    exit 1
fi
