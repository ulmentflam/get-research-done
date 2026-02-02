# Phase 19: Documentation & Testing - Research

**Researched:** 2026-02-02
**Domain:** Validation & Integration Testing
**Confidence:** HIGH

## Summary

This phase validates that all code, agent prompts, and workflows reflect renamed commands and test that command chains work end-to-end. Based on the CONTEXT.md decisions, the scope is **validation only** — no `.planning` file updates (PROJECT.md cleanup explicitly skipped).

The research identifies Node.js native test runner (stable since v20.0.0) as the standard for integration testing, ripgrep patterns for stale reference detection, and command-v for CLI command existence validation. The codebase has 423 markdown files outside `.planning/`, 34 agent prompts, and 14 workflow files requiring validation.

**Primary recommendation:** Use Node.js native test runner with child_process.spawn() for end-to-end command chain testing, ripgrep with word boundary patterns for stale reference detection, and manual human review before applying fixes.

## Standard Stack

The established tools for CLI validation and integration testing:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| node:test | v18.0.0+ (stable v20+) | Native test runner | Built-in, no dependencies, stable API |
| node:assert | Built-in | Assertions | Core module, well-documented patterns |
| node:child_process | Built-in | Spawn CLI commands | Standard for subprocess testing |
| ripgrep (rg) | Latest | Pattern matching | Fast, word boundaries, multiline support |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| bash test | Built-in | Command existence | CLI validation scripts |
| git grep | Built-in | Scoped searches | Alternative to ripgrep |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| node:test | Jest | Jest adds 20MB+ deps, overkill for simple CLI tests |
| node:test | Mocha | Requires chai/sinon, more config |
| ripgrep | grep/awk | rg is faster, better Unicode support |

**Installation:**
```bash
# node:test is built-in to Node.js v18+
# ripgrep already available via system
which rg || brew install ripgrep  # macOS
```

## Architecture Patterns

### Recommended Project Structure
```
tests/
├── integration/           # End-to-end command chain tests
│   ├── command-chains.test.js
│   └── fixtures/         # Test data if needed
├── validation/           # Stale reference detection
│   └── stale-refs.test.js
└── reports/              # Test output, exceptions list
    └── validation-exceptions.md
```

### Pattern 1: CLI Command Chain Testing
**What:** Spawn actual CLI commands and verify they exit successfully
**When to use:** Testing command routing (e.g., new-study suggests design-experiment)
**Example:**
```javascript
// Source: Node.js v25.3.0 Test Runner docs
import { test } from 'node:test';
import { spawn } from 'node:child_process';
import assert from 'node:assert';

test('command exists and runs', async (t) => {
  const proc = spawn('node', ['.claude/hooks/grd-check-update.js']);

  let stdout = '';
  proc.stdout.on('data', (data) => { stdout += data; });

  const exitCode = await new Promise((resolve) => {
    proc.on('close', resolve);
  });

  assert.strictEqual(exitCode, 0, 'Command should exit successfully');
});
```

### Pattern 2: Stale Reference Detection with Ripgrep
**What:** Use word boundaries to find exact command name matches
**When to use:** Scanning codebase for old command names
**Example:**
```bash
# Source: ripgrep user guide
# Word boundary prevents partial matches (e.g., "plan-phase" won't match "explain-phase")
rg '\bplan-phase\b' --type md --glob '!.planning/**' --glob '!CHANGELOG.md'

# Case-insensitive for prose that might capitalize
rg -i '\bplan-phase\b' --type md
```

### Pattern 3: Command Existence Validation
**What:** Verify commands exist before testing chains
**When to use:** Pre-test validation that setup is correct
**Example:**
```bash
# Source: bash command existence best practices
if ! command -v node &> /dev/null; then
    echo "ERROR: node not found in PATH"
    exit 1
fi

# For file existence (command files)
if [ ! -f "commands/grd/design-experiment.md" ]; then
    echo "ERROR: design-experiment.md not found"
    exit 1
fi
```

### Pattern 4: Human Review Before Automated Fixes
**What:** Generate match list, human reviews, then apply fixes
**When to use:** When context matters (historical references vs active code)
**Example:**
```bash
# Step 1: Generate matches with context
rg '\bplan-phase\b' --type md -C 2 > /tmp/matches.txt

# Step 2: Human reviews /tmp/matches.txt, marks exceptions
# Step 3: Apply fixes with sed, excluding exceptions
sed -i 's/\bplan-phase\b/design-experiment/g' file1.md file2.md
```

### Anti-Patterns to Avoid
- **Blind find/replace:** Historical references in CHANGELOG.md should stay unchanged
- **Testing internals instead of interfaces:** Test command routing, not agent implementation
- **Hard-coded file paths:** Use glob patterns or file discovery
- **Skipping isolation:** Each test should be independent (no shared state)

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Test runner | Custom test harness | node:test | Process isolation, reporters, coverage, watch mode |
| CLI spawning | Shell exec strings | child_process.spawn() | Safe argument passing, stream handling, exit codes |
| Pattern matching | Custom regex loops | ripgrep with -w | Word boundaries, Unicode, performance, multiline |
| Assertions | Custom if/throw | node:assert | Standard API, descriptive errors, strictEqual vs loose |

**Key insight:** Node.js native testing reached production maturity in v20.0.0 (2023). Using built-in modules eliminates dependency management and version conflicts.

## Common Pitfalls

### Pitfall 1: False Positives in Pattern Matching
**What goes wrong:** Simple grep finds "plan-phase" in comments explaining old behavior
**Why it happens:** Context-free pattern matching doesn't understand intent
**How to avoid:** Generate match list with context (-C flag), require human review
**Warning signs:** Matches in CHANGELOG.md, git commit messages, historical documentation

### Pitfall 2: Testing Implementation Instead of Interface
**What goes wrong:** Tests break when internal refactoring doesn't change behavior
**Why it happens:** Testing agent internals instead of command outputs
**How to avoid:** Test command existence and exit codes, not agent prompt content
**Warning signs:** Tests reading .claude/agents/*.md and asserting on prompt text

### Pitfall 3: Partial Command Name Matches
**What goes wrong:** "plan-phase" regex matches "explain-phase-transitions"
**Why it happens:** Regex without word boundaries
**How to avoid:** Use \b word boundaries or rg -w flag
**Warning signs:** Unexpected files in grep output

### Pitfall 4: Test Interdependence
**What goes wrong:** Test 2 fails when test 1 is skipped
**Why it happens:** Shared state or execution order dependencies
**How to avoid:** Each test spawns fresh processes, no shared files
**Warning signs:** Tests pass individually but fail when run together

### Pitfall 5: Ignoring Exit Codes
**What goes wrong:** Command fails but test passes because output looked okay
**Why it happens:** Only checking stdout, not exit code
**How to avoid:** Always assert on process exit code
**Warning signs:** Tests pass but actual command usage fails

### Pitfall 6: Hard-Coding Current Working Directory
**What goes wrong:** Tests fail when run from different directories
**Why it happens:** Assuming cwd is project root
**How to avoid:** Use __dirname or process.cwd() to resolve paths
**Warning signs:** "File not found" errors in CI but not local

## Code Examples

Verified patterns from official sources:

### End-to-End Command Chain Test
```javascript
// Source: Node.js v25.3.0 Test Runner + Child Process docs
import { describe, test } from 'node:test';
import { spawn } from 'node:child_process';
import assert from 'node:assert';

describe('Command Chain: design-experiment routing', () => {
  test('design-experiment command exists', async () => {
    const proc = spawn('ls', ['commands/grd/design-experiment.md']);
    const exitCode = await new Promise((resolve) => {
      proc.on('close', resolve);
    });
    assert.strictEqual(exitCode, 0);
  });

  test('run-experiment command exists', async () => {
    const proc = spawn('ls', ['commands/grd/run-experiment.md']);
    const exitCode = await new Promise((resolve) => {
      proc.on('close', resolve);
    });
    assert.strictEqual(exitCode, 0);
  });

  test('validate-results command exists', async () => {
    const proc = spawn('ls', ['commands/grd/validate-results.md']);
    const exitCode = await new Promise((resolve) => {
      proc.on('close', resolve);
    });
    assert.strictEqual(exitCode, 0);
  });
});
```

### Stale Reference Detection Script
```bash
#!/bin/bash
# Source: ripgrep user guide + bash best practices

# Old command names from STATE.md rename mapping
OLD_COMMANDS=(
  "plan-phase"
  "execute-phase"
  "discuss-phase"
  "verify-work"
  "research-phase"
  "list-phase-assumptions"
  "add-phase"
  "insert-phase"
  "remove-phase"
)

# Scan all files except .planning/ and CHANGELOG.md
for cmd in "${OLD_COMMANDS[@]}"; do
  echo "Searching for: $cmd"
  rg "\b${cmd}\b" \
    --type md \
    --glob '!.planning/**' \
    --glob '!CHANGELOG.md' \
    -C 2 \
    || echo "  ✓ No matches"
  echo ""
done
```

### Assertion Patterns
```javascript
// Source: Node.js assert module documentation
import assert from 'node:assert';

// Strict equality (recommended)
assert.strictEqual(actual, expected, 'Values must match exactly');

// Deep object comparison
assert.deepStrictEqual(obj1, obj2, 'Objects must be identical');

// Truthy/falsy checks
assert.ok(value, 'Value must be truthy');

// Error testing
assert.throws(() => {
  throw new Error('Expected error');
}, /Expected error/, 'Should throw with message');
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| External test frameworks (Jest, Mocha) | Node.js native test runner | v18.0.0 (stable v20.0.0) | Zero dependencies, faster CI |
| which command | command -v | 2020s | More portable, shell built-in |
| grep | ripgrep | 2016+ | 10-100x faster, better Unicode |
| Manual file reading | Test isolation modes | v18.0.0 | Each test file in separate process |

**Deprecated/outdated:**
- `which` for command existence: Use `command -v` (shell built-in, more reliable)
- Jest for simple CLI tests: Overkill, 20MB+ dependencies
- Plain grep: ripgrep is standard for modern codebases (better performance)

## Open Questions

Things that couldn't be fully resolved:

1. **Integration Test Placement**
   - What we know: Could be tests/, test/, or root-level
   - What's unclear: Existing test conventions in this codebase
   - Recommendation: Use tests/ at root (common Node.js pattern), no existing test dir found

2. **Exceptions Documentation Format**
   - What we know: CHANGELOG.md should be excluded from fixes
   - What's unclear: Best format for documenting other intentional exceptions
   - Recommendation: Simple markdown file (tests/reports/validation-exceptions.md) listing files/patterns

3. **Test Coverage Scope**
   - What we know: 9 renamed commands need end-to-end validation
   - What's unclear: Should test all 33 commands or just the 9 renames?
   - Recommendation: Test the 9 renames + their routing targets (12-15 commands total)

4. **Agent Prompt Validation Strategy**
   - What we know: 34 agent files, 6 contain stale references
   - What's unclear: Manual review vs automated fixes for agent prompts
   - Recommendation: Automated ripgrep detection, manual review, then targeted sed fixes

## Sources

### Primary (HIGH confidence)
- [Node.js Test Runner Documentation v25.3.0](https://nodejs.org/api/test.html) - Native test runner API
- [Node.js Child Process Documentation v25.3.0](https://nodejs.org/api/child_process.html) - spawn() for CLI testing
- [Node.js Assert Documentation v25.3.0](https://nodejs.org/api/assert.html) - Assertion methods
- [ripgrep User Guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md) - Pattern matching best practices
- [Bash Command Existence Checks](https://sqlpey.com/bash/bash-command-existence-checks/) - command -v pattern

### Secondary (MEDIUM confidence)
- [Integration tests on Node.js CLI](https://medium.com/@zorrodg/integration-tests-on-node-js-cli-part-1-why-and-how-fa5b1ba552fe) - CLI testing patterns
- [Node.js Test Runner Guide (Better Stack)](https://betterstack.com/community/guides/testing/nodejs-test-runner/) - Practical examples
- [Sonar: Hands on with Node.js test runner](https://www.sonarsource.com/blog/node-js-test-runner/) - Real-world usage

### Tertiary (LOW confidence)
- [Top JavaScript Testing Frameworks](https://www.browserstack.com/guide/top-javascript-testing-frameworks) - Framework comparison (general overview)
- [Code Documentation Best Practices 2026](https://www.qodo.ai/blog/code-documentation-best-practices-2026/) - Documentation validation trends

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Node.js native test runner documented in v25.3.0 official docs
- Architecture: HIGH - Patterns verified against official Node.js and ripgrep documentation
- Pitfalls: HIGH - Based on documented common mistakes and bash best practices

**Research date:** 2026-02-02
**Valid until:** 60 days (stable tooling, Node.js LTS cycle is long)

**Scope constraints from CONTEXT.md:**
- PROJECT.md cleanup: **SKIP ENTIRELY** (explicitly decided)
- Agent prompt validation: GRD agents only (get-research-done/ directory)
- GSD source directory: Out of scope
- Integration test placement: Claude's discretion (no tests/ directory exists yet)
- Grep patterns: Claude's discretion (recommend ripgrep with -w)
- Exceptions documentation: Claude's discretion (recommend tests/reports/)

**Key findings:**
- Found 6 stale references in 5 agent files (.claude/agents/)
- Found stale references in 2 workflow files (get-research-done/workflows/)
- 423 markdown files outside .planning/ require scanning
- Node.js v18+ native test runner eliminates need for Jest/Mocha
- User decision: Human reviews each match before fixing (no blind replacement)
