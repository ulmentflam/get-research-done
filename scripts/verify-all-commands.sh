#!/bin/bash
# Comprehensive GRD command verification
# Checks: help.md coverage, file structure, agent/workflow references
# Usage: ./scripts/verify-all-commands.sh

COMMANDS_DIR=".claude/commands/grd"
AGENTS_DIR=".claude/agents"
WORKFLOWS_DIR=".claude/get-research-done/workflows"
HELP_FILE="$COMMANDS_DIR/help.md"

# Built-in Claude Code agent types (not custom agent files)
BUILTIN_AGENTS="general-purpose|Explore|Plan|Bash"

echo "═══════════════════════════════════════════════════════════════"
echo "  GRD Command Verification Suite"
echo "═══════════════════════════════════════════════════════════════"
echo ""

TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_WARN=0

# ─────────────────────────────────────────────────────────────────
# SECTION 1: Help.md Documentation Coverage
# ─────────────────────────────────────────────────────────────────
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│  Section 1: Help.md Documentation Coverage                  │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

if [ ! -f "$HELP_FILE" ]; then
    echo "ERROR: $HELP_FILE not found"
    exit 1
fi

HELP_PASS=0
HELP_FAIL=0

for file in "$COMMANDS_DIR"/*.md; do
    [ "$file" = "$COMMANDS_DIR/help.md" ] && continue
    cmd=$(basename "$file" .md)

    if grep -q "/grd:$cmd" "$HELP_FILE"; then
        echo "  [PASS] /grd:$cmd documented"
        ((HELP_PASS++))
    else
        echo "  [FAIL] /grd:$cmd NOT documented in help.md"
        ((HELP_FAIL++))
    fi
done

echo ""
echo "  Summary: $HELP_PASS documented, $HELP_FAIL missing"
TOTAL_PASS=$((TOTAL_PASS + HELP_PASS))
TOTAL_FAIL=$((TOTAL_FAIL + HELP_FAIL))

# ─────────────────────────────────────────────────────────────────
# SECTION 2: Command File Structure Validation
# ─────────────────────────────────────────────────────────────────
echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│  Section 2: Command File Structure Validation               │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

STRUCT_PASS=0
STRUCT_FAIL=0
STRUCT_WARN=0

for file in "$COMMANDS_DIR"/*.md; do
    [ "$file" = "$COMMANDS_DIR/help.md" ] && continue
    cmd=$(basename "$file" .md)
    issues=""
    warnings=""

    # Check file is not empty
    if [ ! -s "$file" ]; then
        issues="$issues empty-file"
    fi

    # Check for description (should have some content describing the command)
    line_count=$(wc -l < "$file" | tr -d ' ')
    if [ "$line_count" -lt 5 ]; then
        warnings="$warnings short-file($line_count lines)"
    fi

    # Check for XML-style tags (common structure elements)
    has_objective=$(grep -c '<objective>\|<purpose>' "$file" 2>/dev/null || echo "0")
    has_context=$(grep -c '<context>\|<execution_context>' "$file" 2>/dev/null || echo "0")
    has_process=$(grep -c '<process>\|<tasks>\|<steps>' "$file" 2>/dev/null || echo "0")

    # Commands should have at least objective/purpose
    if [ "$has_objective" -eq 0 ] && [ "$has_context" -eq 0 ]; then
        # Check for alternative structures (some commands use different formats)
        has_any_structure=$(grep -cE '^##|^<[a-z_]+>' "$file" 2>/dev/null || echo "0")
        if [ "$has_any_structure" -lt 2 ]; then
            warnings="$warnings minimal-structure"
        fi
    fi

    # Report results
    if [ -n "$issues" ]; then
        echo "  [FAIL] $cmd:$issues"
        ((STRUCT_FAIL++))
    elif [ -n "$warnings" ]; then
        echo "  [WARN] $cmd:$warnings"
        ((STRUCT_WARN++))
    else
        echo "  [PASS] $cmd: valid structure"
        ((STRUCT_PASS++))
    fi
done

echo ""
echo "  Summary: $STRUCT_PASS valid, $STRUCT_WARN warnings, $STRUCT_FAIL invalid"
TOTAL_PASS=$((TOTAL_PASS + STRUCT_PASS))
TOTAL_FAIL=$((TOTAL_FAIL + STRUCT_FAIL))
TOTAL_WARN=$((TOTAL_WARN + STRUCT_WARN))

# ─────────────────────────────────────────────────────────────────
# SECTION 3: Agent Reference Validation
# ─────────────────────────────────────────────────────────────────
echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│  Section 3: Agent Reference Validation                      │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

AGENT_PASS=0
AGENT_FAIL=0
AGENT_WARN=0

for file in "$COMMANDS_DIR"/*.md; do
    [ "$file" = "$COMMANDS_DIR/help.md" ] && continue
    cmd=$(basename "$file" .md)

    # Extract agent references from subagent_type="..." patterns only
    # More precise regex to avoid matching prose text
    agent_refs=$(grep -oE 'subagent_type\s*[=:]\s*"[a-zA-Z-]+"' "$file" 2>/dev/null | \
                 sed 's/subagent_type[[:space:]]*[=:][[:space:]]*"//' | \
                 sed 's/"$//' | \
                 sort -u)

    if [ -z "$agent_refs" ]; then
        # No agent references - might be a simple command
        echo "  [INFO] $cmd: no agent references (may be orchestrator-only)"
        continue
    fi

    for agent in $agent_refs; do
        # Check if it's a built-in agent type
        if echo "$agent" | grep -qE "^($BUILTIN_AGENTS)$"; then
            echo "  [PASS] $cmd → $agent (built-in agent type)"
            ((AGENT_PASS++))
            continue
        fi

        # Check if agent file exists
        if [ -f "$AGENTS_DIR/$agent.md" ]; then
            echo "  [PASS] $cmd → $agent (exists)"
            ((AGENT_PASS++))
        else
            echo "  [FAIL] $cmd → $agent (NOT FOUND in $AGENTS_DIR/)"
            ((AGENT_FAIL++))
        fi
    done
done

echo ""
echo "  Summary: $AGENT_PASS valid refs, $AGENT_FAIL invalid refs"
TOTAL_PASS=$((TOTAL_PASS + AGENT_PASS))
TOTAL_FAIL=$((TOTAL_FAIL + AGENT_FAIL))

# ─────────────────────────────────────────────────────────────────
# SECTION 4: Workflow Reference Validation
# ─────────────────────────────────────────────────────────────────
echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│  Section 4: Workflow Reference Validation                   │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""

WORKFLOW_PASS=0
WORKFLOW_FAIL=0

for file in "$COMMANDS_DIR"/*.md; do
    [ "$file" = "$COMMANDS_DIR/help.md" ] && continue
    cmd=$(basename "$file" .md)

    # Extract workflow references (@...workflows/... or workflows/...)
    workflow_refs=$(grep -oE 'workflows/[a-z-]+\.md|workflows/[a-z-]+' "$file" 2>/dev/null | \
                    sed 's/workflows\///' | \
                    sed 's/\.md$//' | \
                    sort -u)

    if [ -z "$workflow_refs" ]; then
        continue
    fi

    for workflow in $workflow_refs; do
        # Check multiple possible locations
        found=0
        for dir in ".claude/get-research-done/workflows" ".claude/get-shit-done/workflows" ".claude/workflows"; do
            if [ -f "$dir/$workflow.md" ]; then
                echo "  [PASS] $cmd → $workflow (exists in $dir)"
                ((WORKFLOW_PASS++))
                found=1
                break
            fi
        done

        if [ $found -eq 0 ]; then
            echo "  [FAIL] $cmd → $workflow (NOT FOUND)"
            ((WORKFLOW_FAIL++))
        fi
    done
done

echo ""
echo "  Summary: $WORKFLOW_PASS valid refs, $WORKFLOW_FAIL invalid refs"
TOTAL_PASS=$((TOTAL_PASS + WORKFLOW_PASS))
TOTAL_FAIL=$((TOTAL_FAIL + WORKFLOW_FAIL))

# ─────────────────────────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  FINAL SUMMARY"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  Total Checks:"
echo "    PASS: $TOTAL_PASS"
echo "    WARN: $TOTAL_WARN"
echo "    FAIL: $TOTAL_FAIL"
echo ""

if [ $TOTAL_FAIL -eq 0 ]; then
    echo "  ✓ VERIFICATION PASSED"
    echo ""
    exit 0
else
    echo "  ✗ VERIFICATION FAILED ($TOTAL_FAIL issues)"
    echo ""
    exit 1
fi
