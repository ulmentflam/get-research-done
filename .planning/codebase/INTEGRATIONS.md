# External Integrations

**Analysis Date:** 2026-01-27

## APIs & External Services

**Package Registry:**
- npm Registry (registry.npmjs.org)
  - What it's used for: Version checking and package publication
  - Query: `npm view get-shit-done-cc version` (10s timeout)
  - Implementation: `hooks/gsd-check-update.js` line 45
  - Purpose: Checks for available updates and notifies via statusline

**Claude Code Integration:**
- Claude Code IDE hooks system
  - SessionStart hooks: Configured via `~/.claude/settings.json`
  - Update check hook runs on session start
  - Statusline hook provides real-time display

**OpenCode Integration:**
- OpenCode IDE hook system
  - Permission system: `~/.config/opencode/opencode.json`
  - Read permissions: Configured for GSD directories
  - External directory permissions: Configured for cross-project access

## External Tools & CLIs

**npm CLI:**
- Used for package version lookups
- Binary: `npm view get-shit-done-cc version`
- Called from: `hooks/gsd-check-update.js`
- Context: Background process for non-blocking update checks

**Node.js child_process:**
- Used to spawn background update check process
- Method: `spawn()` with `stdio: 'ignore'`
- Implementation: `hooks/gsd-check-update.js` line 25-59
- Purpose: Non-blocking async version checking

## Data Storage

**Local File System Only:**
- No databases or cloud storage services
- Configuration: `~/.claude/settings.json` or `~/.config/opencode/opencode.json`
- Caching: `~/.claude/cache/gsd-update-check.json`
- Todos: `~/.claude/todos/` directory (reads for statusline display)
- Versions: `VERSION` file stored in GSD install directory

**State Management:**
- Project state: `.planning/STATE.md` (created by agents)
- Config: `.planning/config.json` (workflow mode: interactive/yolo)

## Authentication & Identity

**Auth Provider:**
- None - GSD is a CLI tool without authentication
- No user accounts or logins required
- Installation is local to user's machine

**Access Control:**
- File system permissions: Uses Node.js fs API
- IDE runtime permissions: Configured via IDE settings.json files
- OpenCode special handling: Explicit permission grants in opencode.json

## Configuration Management

**Settings Files:**
- `~/.claude/settings.json` (Claude Code)
  - Hook registration for SessionStart events
  - Statusline command configuration
  - GSD registers hooks for update checking and statusline display

- `~/.config/opencode/opencode.json` (OpenCode)
  - Permission grants for read access to GSD directories
  - External directory permission grants
  - Tool permission configuration

**Environment Configuration:**
- Required env vars: None (all optional)
- Optional env vars:
  - `CLAUDE_CONFIG_DIR` - Override Claude config location
  - `OPENCODE_CONFIG_DIR` - Override OpenCode config location
  - `OPENCODE_CONFIG` - Override opencode.json path
  - `XDG_CONFIG_HOME` - XDG Base Directory support

## Hooks & IDE Integration

**Incoming Hooks (from IDE to GSD):**
- `SessionStart` hook - Update check trigger
  - Runs: `gsd-check-update.js` on each Claude session start
  - Context: Returns version info to cache file

- Statusline input - JSON from IDE
  - Reads: Model name, workspace directory, context window, session ID
  - Processes: `gsd-statusline.js` via stdin
  - Returns: Formatted terminal output to stdout

**Configuration Callbacks:**
- Hook registration: Via `~/.claude/settings.json`
- Statusline setup: Via `~/.claude/settings.json`
- Permission grants: Via `~/.config/opencode/opencode.json`

## CLI Tool Usage

**npm (version checking):**
- Command: `npm view get-shit-done-cc version`
- Timeout: 10 seconds
- Error handling: Silent on failure (doesn't break statusline)
- Cache file: `~/.claude/cache/gsd-update-check.json`

**Git Integration (via agents):**
- Agents use git commands via bash
- Not a direct integration, used by Claude when executing plans
- Git reference: `get-shit-done/references/git-integration.md`

## Webhook & Callback Paths

**Incoming:**
- SessionStart hook from Claude Code IDE
  - Triggers: `gsd-check-update.js` background process
  - Path: Registered in `settings.json` hooks.SessionStart array

- Statusline hook from Claude Code IDE
  - Receives: JSON stdin with session/model/context data
  - Path: Registered in `settings.json` statusLine field

**Outgoing:**
- None - GSD is a tool, not a service

## Environment & Installation

**Default Installation Locations:**

**Claude Code:**
- Global: `~/.claude/` (or CLAUDE_CONFIG_DIR)
- Local: `./.claude/` (project-specific)

**OpenCode:**
- Global: `~/.config/opencode/` (or OPENCODE_CONFIG_DIR)
- Local: `./.opencode/` (project-specific)

**Installed Components:**
- `commands/gsd/*.md` - Command definitions
- `agents/gsd-*.md` - Agent definitions
- `get-shit-done/` - Core skill and workflows
- `hooks/gsd-*.js` - Compiled hooks
- `settings.json` - Hook and statusline configuration

## Cross-Platform Considerations

**Windows Support:**
- Path handling with forward slashes for Node.js compatibility
- `windowsHide: true` in child_process spawn to prevent console flash
- Environment variable expansion (`~` to home directory)

**macOS/Linux Support:**
- XDG Base Directory spec for OpenCode
- Standard Unix home directory (`~`) handling
- Standard shell path resolution

## No External Dependencies

This project explicitly **avoids external package dependencies** in production:

- **Zero npm packages** in `dependencies` object
- **Only Node.js built-ins** for all functionality
- **Bundled hooks** with esbuild (dev-only, not in production)
- **No APIs beyond npm registry** (for version checking only)

This design choice ensures:
- Minimal dependency surface area
- Faster installation
- Reduced supply chain risk
- Compatibility across node versions 16.7.0+

---

*Integration audit: 2026-01-27*
