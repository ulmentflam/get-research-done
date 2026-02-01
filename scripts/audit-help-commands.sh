#!/bin/bash
# Audit help.md for v1.1 command coverage and deprecated command removal
# Usage: ./scripts/audit-help-commands.sh

echo "=== Help Documentation Audit ==="
echo ""

HELP_FILE=".claude/commands/grd/help.md"

if [ ! -f "$HELP_FILE" ]; then
    echo "ERROR: $HELP_FILE not found"
    exit 1
fi

PASS=0
FAIL=0

# V1.1 commands that MUST be documented
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

# Deprecated commands that MUST NOT appear
DEPRECATED_COMMANDS=(
    "new-milestone"
    "complete-milestone"
    "discuss-phase"
    "execute-phase"
    "verify-work"
    "audit-milestone"
    "plan-milestone-gaps"
)

echo "=== V1.1 Command Documentation Check ==="
echo ""

for cmd in "${V11_COMMANDS[@]}"; do
    if grep -q "/grd:$cmd" "$HELP_FILE"; then
        echo "  [PASS] /grd:$cmd documented"
        ((PASS++))
    else
        echo "  [FAIL] /grd:$cmd NOT documented"
        ((FAIL++))
    fi
done

echo ""
echo "=== Deprecated Command Removal Check ==="
echo ""

for cmd in "${DEPRECATED_COMMANDS[@]}"; do
    if grep -q "/grd:$cmd" "$HELP_FILE"; then
        echo "  [FAIL] /grd:$cmd still present (should be removed)"
        ((FAIL++))
    else
        echo "  [PASS] /grd:$cmd not present (correctly removed)"
        ((PASS++))
    fi
done

echo ""
echo "=== Summary ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "AUDIT PASSED: All v1.1 commands documented, no deprecated commands found"
    exit 0
else
    echo "AUDIT FAILED: $FAIL issues found"
    exit 1
fi
