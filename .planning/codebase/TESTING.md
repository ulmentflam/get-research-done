# Testing Patterns

**Analysis Date:** 2026-01-27

## Test Framework

**Runner:**
- Not detected - no test framework configured
- package.json has zero test dependencies
- No jest.config.js, vitest.config.ts, or mocha.opts found
- No test scripts in package.json

**Assertion Library:**
- None configured
- Not applicable (no test infrastructure)

**Run Commands:**
- No test commands available
- To add testing: would need to install test framework first

## Test File Organization

**Location:**
- No test files found in codebase
- No *.test.js, *.spec.js, or __tests__/ directories detected
- No separate tests/ directory structure

**Naming Convention:**
- Not established (no tests to reference)
- Recommended pattern if adding tests: `*.test.js` alongside source files

**Structure:**
- No test file organization currently used
- If tests are added: recommend co-locating with source
  - `bin/install.js` → `bin/install.test.js`
  - `hooks/gsd-statusline.js` → `hooks/gsd-statusline.test.js`
  - `scripts/build-hooks.js` → `scripts/build-hooks.test.js`

## Test Structure

**Suite Organization:**
- No tests currently exist
- Recommended pattern based on similar Node.js projects:
```javascript
describe('Module Name', () => {
  describe('functionName', () => {
    it('should handle success case', () => {
      // arrange
      // act
      // assert
    });

    it('should handle error case', () => {
      // test code
    });
  });
});
```

**Patterns to Use if Tests Added:**
- Use describe blocks for module organization
- Use it() for individual test cases
- Follow arrange/act/assert pattern
- One focus per test (one primary assertion)
- Setup: use beforeEach for per-test state
- Teardown: use afterEach to clean up and restore mocks

## Mocking

**Framework:**
- No mocking framework configured
- If tests added: recommend Vitest (modern, ESM-compatible) or Jest

**Common Mocking Needs:**
- File system operations (fs, fs-extra)
- Child process execution (spawn, execSync)
- Network requests (API calls)
- Environment variables (process.env)
- Interactive input (readline)

**Patterns to Use:**
```javascript
// Mock file system
vi.mock('fs');
const mockFs = vi.mocked(fs);

// Mock child_process
vi.mock('child_process');
const mockSpawn = vi.mocked(spawn);

// Mock fs-extra operations
vi.mock('fs-extra', () => ({
  readFile: vi.fn(),
  writeFile: vi.fn(),
  mkdirSync: vi.fn()
}));
```

**What to Mock:**
- External file system operations (especially destructive operations)
- Child process spawning (prevent actual command execution)
- API calls (prevent external dependencies)
- Filesystem reads (to control test data)
- Time/dates if needed (vi.useFakeTimers)

**What NOT to Mock:**
- Pure utility functions
- Object/JSON manipulation helpers
- String formatting functions
- Configuration parsing (unless hitting real filesystem)

## Fixtures and Factories

**Test Data:**
- No fixtures currently exist
- Recommended pattern if tests added:
```javascript
// Factory function in test file
function createTestConfig(overrides = {}) {
  return {
    targetDir: '/tmp/test',
    isGlobal: false,
    runtime: 'claude',
    ...overrides
  };
}

// Reusable test file content
const sampleCommandFile = `---
name: gsd:test
description: Test command
allowed-tools:
  - Read
  - Write
---

Content here`;
```

**Location:**
- Factory functions: define in test file near usage (keep tests self-contained)
- Shared fixtures: create tests/fixtures/ directory if needed across multiple tests
- Mock markdown content: define as template strings in test file

## Coverage

**Requirements:**
- No coverage target enforced
- No .nycrc or coverage configuration in package.json
- Not measured or tracked currently

**If Adding Tests:**
- Recommend focusing on critical paths first:
  - Path expansion and resolution (expandTilde)
  - Configuration reading/writing (readSettings, writeSettings)
  - File operations (copyWithPathReplacement, verifyInstalled)
  - CLI argument parsing
  - Installation logic (core business)
- Test error paths and edge cases
- Aim for >70% coverage on critical modules

**View Coverage (if configured):**
```bash
npm run test:coverage
# or
npm test -- --coverage
```

## Test Types

**Unit Tests:**
- Test individual functions in isolation
- Mock file system and process calls
- Mock external dependencies
- Examples to test:
  - `expandTilde()` - path expansion
  - `parseConfigDirArg()` - CLI argument parsing
  - `readSettings()` / `writeSettings()` - configuration
  - `getDirName()` - mapping runtime to directory

**Integration Tests:**
- Test multiple modules working together
- Mock file system boundaries but use real logic
- Examples to test:
  - Installation flow: install() function calling multiple helpers
  - Command copying with path replacement
  - Cleanup and orphaned file removal

**E2E Tests:**
- Not currently used
- Could test via CLI: `node bin/install.js --help`
- Could verify file system changes in temp directories
- Not recommended given CLI nature - integration tests sufficient

## Common Patterns

**Async Testing:**
- Not heavily used (most code is synchronous)
- Child process uses spawn() which is async-but-unref'd
- If testing async:
```javascript
it('should handle async operation', async () => {
  const result = await asyncFunction();
  expect(result).toBe('expected');
});
```

**Error Testing:**
```javascript
it('should throw on invalid input', () => {
  expect(() => expandTilde(null)).toThrow();
});

it('should exit on validation error', () => {
  expect(() => parseConfigDirArg([]))
    .toThrow('--config-dir requires a path');
});
```

**File System Testing:**
```javascript
import { vi } from 'vitest';
import * as fs from 'fs';

vi.mock('fs');

it('reads and parses JSON configuration', () => {
  const mockFs = vi.mocked(fs);
  mockFs.readFileSync.mockReturnValue(
    JSON.stringify({ statusLine: { command: '...' } })
  );

  const settings = readSettings('/path/to/settings.json');
  expect(settings.statusLine).toBeDefined();
});
```

## Infrastructure Notes

**Current Limitations:**
- Only esbuild as dev dependency (for hook bundling, not used currently)
- No test framework installed
- No CI integration for tests

**Bootstrap Path (if adding tests):**
1. Install Vitest: `npm install -D vitest @vitest/ui`
2. Create vitest.config.ts
3. Add test script to package.json: `"test": "vitest"`
4. Create tests/ directory structure
5. Add pre-commit hook to run tests

**Build Impact:**
- Tests should NOT be bundled (exclude *.test.js from esbuild)
- Tests run against source, not bundled output
- Hooks bundled separately via build-hooks.js script

---

*Testing analysis: 2026-01-27*
*Currently no test framework configured - this documents expected patterns if tests are added*
