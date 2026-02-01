#!/bin/bash
# Audit help.md documentation coverage
# Usage: ./scripts/audit-help-commands.sh

COMMANDS_DIR=".claude/commands/grd"
HELP_FILE="$COMMANDS_DIR/help.md"

echo "=== GRD Command Coverage Audit ==="
echo ""

# Check help.md exists
if [ ! -f "$HELP_FILE" ]; then
    echo "ERROR: $HELP_FILE not found"
    exit 1
fi

# Count actual command files (excluding help itself)
ACTUAL_COUNT=$(ls "$COMMANDS_DIR"/*.md 2>/dev/null | grep -v help.md | wc -l | tr -d ' ')
echo "Command files found: $ACTUAL_COUNT"

# Count documented commands in help.md (looking for /grd: pattern)
DOCUMENTED_COUNT=$(grep -oE '/grd:[a-z-]+' "$HELP_FILE" | sort -u | wc -l | tr -d ' ')
echo "Unique commands in help.md: $DOCUMENTED_COUNT"
echo ""

# V1.1 commands that MUST be documented
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

V11_PASS=0
V11_FAIL=0

for cmd in "${V11_COMMANDS[@]}"; do
    if grep -q "/grd:$cmd" "$HELP_FILE"; then
        echo "  [PASS] /grd:$cmd documented"
        ((V11_PASS++))
    else
        echo "  [FAIL] /grd:$cmd NOT in help.md"
        ((V11_FAIL++))
    fi
done

echo ""
echo "V1.1 commands: $V11_PASS passed, $V11_FAIL failed"
echo ""

# Deprecated commands that should NOT appear
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

DEP_PASS=0
DEP_FAIL=0

for cmd in "${DEPRECATED[@]}"; do
    if grep -q "/grd:$cmd" "$HELP_FILE"; then
        echo "  [FAIL] /grd:$cmd still in help.md (should be removed)"
        ((DEP_FAIL++))
    else
        echo "  [PASS] /grd:$cmd not in help.md"
        ((DEP_PASS++))
    fi
done

echo ""
echo "Deprecated check: $DEP_PASS passed, $DEP_FAIL failed"
echo ""

# Command file coverage (optional - commands with files but not documented)
echo "=== Command File Coverage ==="

UNDOCUMENTED=0
for file in "$COMMANDS_DIR"/*.md; do
    [ "$file" = "$COMMANDS_DIR/help.md" ] && continue
    cmd=$(basename "$file" .md)
    if ! grep -q "/grd:$cmd" "$HELP_FILE"; then
        echo "  [WARN] $cmd has file but not documented in help.md"
        ((UNDOCUMENTED++))
    fi
done

if [ $UNDOCUMENTED -eq 0 ]; then
    echo "  All command files are documented"
fi

echo ""
echo "=== Summary ==="
TOTAL_FAIL=$((V11_FAIL + DEP_FAIL))
if [ $TOTAL_FAIL -eq 0 ]; then
    echo "AUDIT PASSED: All v1.1 commands documented, no deprecated commands found"
    exit 0
else
    echo "AUDIT FAILED: $TOTAL_FAIL issues found"
    exit 1
fi
