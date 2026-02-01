#!/bin/bash
# Document architect warning verification (manual observation required)
# Usage: ./scripts/verify-architect-warning.sh

echo "=== Architect Warning Verification ==="
echo ""
echo "This test requires manual observation of architect output."
echo ""
echo "Test Procedure:"
echo "1. Ensure only quick-explore was run (DATA_REPORT.md has Quick header)"
echo "2. Run: /grd:architect"
echo "3. Observe output for warning about data depth"
echo ""
echo "Expected Warning Patterns (look for any of these):"
echo "  - 'Quick Explore' data may be insufficient"
echo "  - quick-explore only provides basic"
echo "  - run full /grd:explore for"
echo "  - data reconnaissance not completed"
echo "  - WARNING: No DATA_REPORT.md"
echo ""
echo "Verification:"
echo "  If warning appears: TEST PASSED"
echo "  If no warning and architect proceeds: TEST FAILED"
echo ""

# Check current DATA_REPORT.md status as helper
if [ -f ".planning/DATA_REPORT.md" ]; then
    if head -30 ".planning/DATA_REPORT.md" | grep -qi "Quick Explore"; then
        echo "Current state: DATA_REPORT.md has Quick Explore header (correct setup)"
    else
        echo "Current state: DATA_REPORT.md is NOT Quick mode (wrong setup for this test)"
    fi
else
    echo "Current state: No DATA_REPORT.md (architect will warn about missing file)"
fi
