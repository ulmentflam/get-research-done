# Technology Stack

**Analysis Date:** 2026-01-27

## Languages

**Primary:**
- JavaScript - All executable code
- Node.js - Runtime for all binaries and hooks

**Secondary:**
- Markdown - Agent and command definitions (stored as .md files with YAML frontmatter)
- JSON - Configuration, package metadata, state management

## Runtime

**Environment:**
- Node.js 16.7.0 or higher (specified in `package.json` engines field)

**Package Manager:**
- npm
- Lockfile: `package-lock.json` (present)

## Frameworks & Build Tools

**Build/Development:**
- esbuild 0.24.0 - JavaScript bundler (dev dependency)
  - Used to bundle hooks from source into dist for distribution
  - Config: `scripts/build-hooks.js`

**CLI/Installation:**
- Custom Node.js installer script (`bin/install.js`)
  - No external CLI framework dependencies
  - Uses Node.js built-ins: fs, path, os, readline, child_process

## Key Dependencies

**Production Dependencies:**
- None (empty dependencies object in package.json)
- All functionality uses Node.js built-in modules only

**Development Dependencies:**
- esbuild ^0.24.0 - JavaScript bundler for hooks compilation

**Built-in Node.js Modules Used:**
- `fs` - File system operations (reading, writing, copying, deleting directories)
- `path` - Path manipulation and resolution
- `os` - OS-level operations (home directory, platform info)
- `readline` - Interactive terminal prompts for installer
- `child_process` - Spawning background processes for update checks

## Hooks & Runtime Scripts

**Hooks (located in `hooks/`):**
- `gsd-statusline.js` - Displays model name, current task, directory, context usage
  - Reads stdin JSON from Claude Code
  - Reads todo status from `~/.claude/todos/` directory
  - Reads update cache from `~/.claude/cache/gsd-update-check.json`
  - Outputs colored terminal output with progress bars and emoji

- `gsd-check-update.js` - Checks for GSD updates from npm registry
  - Spawns background process
  - Reads installed version from `VERSION` file
  - Calls `npm view get-shit-done-cc version` to check latest
  - Caches result to `~/.claude/cache/gsd-update-check.json`
  - 10-second timeout on npm registry check

## Configuration

**Environment Variables:**
- `CLAUDE_CONFIG_DIR` - Custom Claude Code config directory (overrides ~/.claude)
- `OPENCODE_CONFIG_DIR` - Custom OpenCode config directory (overrides ~/.config/opencode)
- `OPENCODE_CONFIG` - Alternate path to opencode.json
- `XDG_CONFIG_HOME` - XDG Base Directory spec support for OpenCode

**Installation Directories:**
- Claude Code: `~/.claude/` (or custom via CLAUDE_CONFIG_DIR)
- OpenCode: `~/.config/opencode/` (or custom via OPENCODE_CONFIG_DIR)
- Local (project): `./.claude/` or `./.opencode/`

**Build Configuration:**
- esbuild configured in `scripts/build-hooks.js` (simple file copy, no complex bundling)

## Platform Requirements

**Development:**
- Node.js 16.7.0+
- npm or equivalent package manager
- Cross-platform: Mac, Windows, Linux supported

**Production/Installation:**
- Node.js 16.7.0+ (verified at runtime)
- npm registry access (for update checks)
- Write permissions to home directory (for config installation)
- Home directory access via `~` expansion

## Published Package

**Registry:**
- npm package: `get-shit-done-cc`
- Version: 1.9.13
- Published as: `npx get-shit-done-cc`

**Installation Methods:**
- Global install: `npx get-shit-done-cc --claude --global`
- Local install: `npx get-shit-done-cc --claude --local`
- Both runtimes: `npx get-shit-done-cc --both --global`

## File Distribution

**Published Files (in `files` array):**
- `bin/` - CLI entry point
- `commands/` - GSD command definitions
- `get-shit-done/` - Core skill and workflow definitions
- `agents/` - Agent prompt definitions
- `hooks/dist/` - Compiled hook scripts
- `scripts/` - Build scripts

**Not Published:**
- `hooks/` source (only dist/ published)
- Node modules
- Git history

---

*Stack analysis: 2026-01-27*
