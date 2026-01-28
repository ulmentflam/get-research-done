# Coding Conventions

**Analysis Date:** 2026-01-27

## Naming Patterns

**Files:**
- kebab-case for all executable files (gsd-check-update.js, gsd-statusline.js)
- kebab-case for markdown documentation (gsd-style.md, execute-phase.md)
- index.js for entry points in bin/ directory
- .md extension for all documentation and command files

**Functions:**
- camelCase for all JavaScript functions (buildHookCommand, expandTilde, readSettings, getGlobalDir)
- PascalCase for constructor/factory functions (convertClaudeToOpencodeFrontmatter as transformation function)
- Descriptive verb-noun pattern (verifyInstalled, cleanupOrphanedFiles, configureOpencodePermissions)
- No special prefix for async functions

**Variables:**
- camelCase for all variables (selectedRuntimes, targetDir, settingsPath, claudeDir)
- CAPS_UNDERSCORES for configuration constants (HOOKS_DIR, DIST_DIR)
- Avoid underscore prefix (no private marker convention)
- Verbose naming over abbreviations (targetDirectory not tgtDir, claudeDirectory not cDir)

**Types/Objects:**
- camelCase for object properties (display_name, context_window, remaining_percentage - following JSON API convention)
- camelCase for function parameters and destructured properties (srcDir, destDir, dirName)
- No TypeScript interfaces (plain Node.js, no type annotations)

## Code Style

**Formatting:**
- No formal formatter configured
- Consistent 2-space indentation throughout
- 80-100 character line length (varies by context)
- Semicolons required at end of statements
- Template literals for multi-line strings (backticks)

**Linting:**
- No ESLint configuration detected
- No Prettier configuration
- Code follows implicit conventions:
  - Declarative variable naming (what, not how)
  - Function organization: declarations first, then implementation
  - Grouped related functionality together

**Code Organization:**
- Shebang header for executable scripts: `#!/usr/bin/env node`
- Version/comment header describing script purpose
- Constants defined at module top
- Helper functions before main execution logic
- Main execution at bottom of file

## Import Organization

**Order:**
1. Node.js built-ins (fs, path, os, require, child_process)
2. Package dependencies (none in core implementation - esbuild dev-only)
3. Local modules (relative imports with require)
4. No ES6 imports - pure CommonJS (require/module.exports)

**Patterns:**
- `const module = require('module')` at top
- `const { function } = require('./relative-path')` for destructuring
- No aliasing or path mapping
- Relative paths use ../ and ./ notation

## Error Handling

**Patterns:**
- Try-catch blocks for JSON parsing and file operations
- Process.exit(1) for fatal errors with descriptive messages
- Silent failures in non-critical paths (try/catch with empty catch blocks)
- Error messages logged to console.error with colored output

**Error Communication:**
- Use colored output (ANSI escape codes) for error clarity:
  - Yellow (\x1b[33m) for warnings
  - Red for critical errors (used in exit handlers)
- Wrap error context: show what was attempted, what failed
- User-facing messages vs. internal errors (different messaging)

**Exit Codes:**
- Process.exit(0) for success
- Process.exit(1) for errors/validation failures

## Logging

**Framework:**
- console.log for standard output
- console.error for error messages
- Inline ANSI color codes for styled output

**Patterns:**
- Colored output with status indicators:
  - `✓` (green checkmark) for success/completion
  - `⚠` (yellow warning) for cautions/skipped operations
  - `✗` (red x) for failures
- Indentation with spaces for nested status messages
- Progress indication: "Copying file..." then "  → /path/to/file"
- Banner text for major operations

**Where to Log:**
- Log at operation boundaries (installation start/end, file operations)
- Log progress for multi-step operations (copying files, generating directories)
- Log configuration decisions (where installing, what runtime)
- Avoid logging in helper functions (let caller log context)

## Comments

**When to Comment:**
- Explain non-obvious logic (env var precedence, XDG spec compliance)
- Document business rules (why specific check is needed)
- Explain workarounds or platform-specific behaviors (Windows path handling)
- Avoid obvious comments ("increment counter", "read file")

**Format:**
- Single-line comments: `// Comment here`
- Multi-line comments: `/* Multi\nline\ncomment */` for complex explanations
- No JSDoc (no formal API documentation)

**TODO Comments:**
- Format: `// TODO: description`
- Link to issue/context when relevant: `// TODO: Remove in v2.0 (breaking change)`
- Mark cleanup work in upgrade paths

## Function Design

**Size:**
- Keep functions under 100 lines for readability
- Extract helpers for distinct responsibilities
- Single responsibility: each function does one thing

**Parameters:**
- Max 3-4 parameters preferred
- Use object for 4+ related parameters: `function install(options: { isGlobal, runtime })`
- Destructure in parameter list when helpful
- Avoid boolean flags when semantic naming helps (isGlobal, isOpencode instead of flags)

**Return Values:**
- Explicit return statements required
- Return early for guard clauses and error conditions
- Return objects for multiple values: `{ settingsPath, settings, statuslineCommand }`
- Void functions for side-effect operations (file writes, console output)

## Module Design

**Exports:**
- Single responsibility per file
- module.exports for functions meant to be called externally
- No complex export patterns
- Main execution logic at bottom (after function definitions)

**File Structure Pattern:**
```javascript
#!/usr/bin/env node
// Single-line description

const fs = require('fs');
const path = require('path');
const { otherModule } = require('./other');

const CONSTANT = 'value';

/**
 * Helper function 1
 */
function helper1() {}

/**
 * Helper function 2
 */
function helper2() {}

/**
 * Main exported function
 */
function mainOperation() {}

// Main execution (if CLI script)
if (require.main === module) {
  mainOperation();
}
```

**No Barrel Files:**
- Each file is independent
- No index.js re-exports
- Direct requires from specific files

## Markdown File Conventions

**Command Files (commands/gsd/*.md):**
- YAML frontmatter with: name, description, argument-hint, allowed-tools
- XML semantic tags for structure: `<objective>`, `<execution_context>`, `<context>`, `<process>`, `<success_criteria>`
- Markdown headers (#, ##) for content organization within tags
- @-references to load related content: `@~/.claude/get-shit-done/workflows/execute-phase.md`

**Workflow Files (get-shit-done/workflows/*.md):**
- No YAML frontmatter
- XML semantic tags: `<purpose>`, `<required_reading>`, `<process>`, `<step>`
- Named steps with priority: `<step name="load_project_state" priority="first">`
- Code blocks in backticks with language identifier
- Conditional logic with `<if>` tags

**Agent Files (agents/gsd-*.md):**
- YAML frontmatter: name, description, tools, color
- `<role>` section explaining responsibilities
- Multiple structural sections (`<why_this_matters>`, `<philosophy>`, `<process>`)
- Named steps with descriptive step names
- Detailed execution instructions with bash examples

## Cross-Cutting Patterns

**Path Handling:**
- Use path.join() for cross-platform compatibility
- Expand ~ with expandTilde() function
- Forward slashes in Node.js (works on all platforms)
- Windows compatibility: explicit windowsHide flag for child_process

**JSON Operations:**
- readSettings() reads JSON with fallback to empty object
- writeSettings() writes with proper formatting (JSON.stringify with indent 2, newline)
- Always add trailing newline to JSON files

**File System Operations:**
- Create directories with fs.mkdirSync({ recursive: true })
- Clean installs: delete existing destination before copying
- Preserve user content: only delete GSD-specific files during uninstall

**Interactive Prompts:**
- readline.createInterface for user interaction
- Timeout handling for non-TTY environments
- Default values in brackets: `[1]`
- Clear instructions with numbered options

---

*Convention analysis: 2026-01-27*
*Update when patterns change*
