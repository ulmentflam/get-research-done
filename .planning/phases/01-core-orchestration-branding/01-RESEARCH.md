# Phase 1: Core Orchestration & Branding - Research

**Researched:** 2026-01-27
**Domain:** Package refactoring, CLI branding, state management extension
**Confidence:** HIGH

## Summary

This phase refactors the existing GSD (Get Shit Done) codebase to establish the GRD (Get Research Done) identity and extend state tracking for research loop management. The work involves systematic renaming across 91 files, creating new ASCII art branding, updating npm package metadata, and extending STATE.md to track research iterations.

The existing codebase has a mature structure with 27 slash commands, 11 agents, 51 workflow/template files, and a robust state management system. The refactor is straightforward—rename references, update branding, extend state tracking—with no architectural changes required.

**Primary recommendation:** Execute as a systematic find-and-replace refactor with branding updates and incremental STATE.md extension. Use the existing state.md template as foundation and add research loop tracking section.

## Standard Stack

### Core (Already in Place)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Node.js | >=16.7.0 | Runtime for installer and hooks | Existing requirement, stable API |
| CommonJS | Native | Module system | Current codebase pattern, no ES6 modules |
| fs (built-in) | Native | File operations | Standard Node.js file handling |
| path (built-in) | Native | Cross-platform paths | Required for Windows/Mac/Linux support |
| readline (built-in) | Native | CLI prompts | Current pattern for interactive installs |

### Supporting (Already in Place)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| esbuild | ^0.24.0 | Hook bundling | Dev dependency for hooks/dist/ compilation |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| CommonJS | ES6 modules | Current codebase uses require(), no benefit to migrate |
| Built-in fs | fs-extra | No need for additional abstraction, built-in sufficient |
| Manual find-replace | codemod/jscodeshift | Overkill for straightforward string replacement |

**Installation:**
No new dependencies required. Existing package.json dependencies are sufficient.

## Architecture Patterns

### Recommended Project Structure
```
get-research-done/
├── bin/install.js           # Update banner, package name references
├── package.json             # Update name: "get-research-done"
├── README.md                # Update title, installation instructions
├── GRD-STYLE.md             # Rename from GSD-STYLE.md
├── commands/grd/            # Rename from commands/gsd/
│   └── *.md                # Update name: "grd:command" in frontmatter
├── get-research-done/       # Rename from get-shit-done/
│   ├── references/
│   ├── templates/
│   │   └── state.md        # Extend with research loop section
│   └── workflows/
├── agents/                  # Rename gsd-*.md → grd-*.md
│   └── grd-*.md
└── hooks/                   # Update gsd-*.js → grd-*.js
    ├── grd-statusline.js
    └── grd-check-update.js
```

### Pattern 1: ASCII Art CLI Branding
**What:** Display ASCII art banner on installation and CLI invocation
**When to use:** Package installer welcome message, command help output
**Example:**
```javascript
// Source: Existing pattern in bin/install.js lines 91-102
const banner = `
${cyan}   ██████╗ ███████╗██████╗
  ██╔════╝ ██╔════╝██╔══██╗
  ██║  ███╗███████╗██║  ██║
  ██║   ██║╚════██║██║  ██║
  ╚██████╔╝███████║██████╔╝
   ╚═════╝ ╚══════╝╚═════╝${reset}

  Get Shit Done ${dim}v${pkg.version}${reset}
  A meta-prompting, context engineering and spec-driven
  development system for Claude Code (and opencode) by TÂCHES.
`;
```

**For GRD branding:**
- Create similar block-letter ASCII art for "GRD" (3 letters instead of 3)
- Update tagline to reflect research focus
- Keep ANSI color scheme (cyan/dim for consistency)
- Use online generators like [ASCII Art Generator](http://www.network-science.de/ascii/) or [ASCII Art Generator](https://www.asciiart.eu/text-to-ascii-art)
- Verify monospace rendering (80-character terminal width)

**Design considerations:**
- CLI tool banners improve GitHub star conversion by 40% and provide instant brand recognition (Source: [Orbit2x Creative ASCII Art Ideas 2026](https://orbit2x.com/blog/50-creative-ascii-art-ideas-examples-use-cases))
- Stick to basic ASCII (32-126) for maximum terminal compatibility
- Filled-in ASCII art style is trending in 2026, influenced by Claude Code branding (Source: [CLI Renaissance Alert: Meet oh-my-logo](https://dev.to/shinshin86/cli-renaissance-alert-meet-oh-my-logo-your-gemini-cli-and-claude-code-style-logo-generator-2gp1))

### Pattern 2: NPM Package Migration
**What:** Publish new package name while deprecating old package
**When to use:** Major rebrand that changes npm package name
**Example:**
```bash
# 1. Update package.json
npm version major --no-git-tag-version
# Update name to "get-research-done"

# 2. Publish new package
npm publish

# 3. Deprecate old package (manual step after publishing)
npm deprecate get-shit-done-cc "WARNING: This project has been renamed to get-research-done. Install using get-research-done instead."
```

**Key steps for npm migration:**
1. Update package.json name field: `"get-research-done"`
2. Update bin entry: `"get-research-done": "bin/install.js"`
3. Update repository URLs to new GitHub repo (if renamed)
4. Publish to npm with new name
5. Deprecate old package with migration message
6. Update documentation to reference new package name

**Sources:**
- [Lerna: A Tale of Renaming NPM Packages](https://medium.com/@dlacustodio/lerna-a-tale-of-renaming-npm-packages-4d3c534bc31)
- [How to rename an NPM package in your package.json](https://gist.github.com/nandorojo/1b969a0d88cf81ca8a2a334a5bd2ee4a)

### Pattern 3: File-Based State Persistence for Loop Tracking
**What:** Extend STATE.md to track research loop iterations with file-based persistence
**When to use:** Research workflows with multiple exploration/refinement cycles
**Example:**
```markdown
## Research Loop History

**Current Loop:** 2
**Status:** In refinement

| Loop | Started | Completed | Focus Area | Outcome |
|------|---------|-----------|------------|---------|
| 1 | 2026-01-20 | 2026-01-20 | Initial domain exploration | 12 sources analyzed, 3 patterns identified |
| 2 | 2026-01-21 | In progress | Pattern validation | Refining hypotheses |

**Loop 2 Progress:**
- [x] Hypothesis formulation
- [x] Source gathering
- [ ] Cross-validation
- [ ] Synthesis
```

**Why file-based over in-memory:**
- Survives Claude Code session restarts (Source: [Store State on Filesystem in Node.js CLIs with Conf](https://egghead.io/lessons/javascript-store-state-on-filesystem-in-node-js-clis-with-conf))
- Enables context restoration across agent invocations
- Human-readable format (markdown) for debugging
- Git-trackable for version history

**Libraries considered (but not needed):**
- `conf`: Simple persistent storage (665+ projects use it) - Overkill for markdown-based state
- `node-persist`: localStorage-like API - Not needed, STATE.md already uses markdown
- Current approach: Use existing STATE.md pattern, extend with research section

**2026 trends:**
- Reactive Proxies for state change detection (not applicable to file-based markdown)
- Persistent storage via browser localStorage (not applicable to CLI)
- File-based storage remains best for CLI state across restarts (Source: [Strategies for State Management in Node.js](https://nelkodev.com/en/blog/mastering-state-management-in-large-node-js-applications/))

### Anti-Patterns to Avoid
- **Multi-pass refactoring:** Don't rename in stages. Do all renames atomically in one phase to avoid broken state.
- **Manual find-replace in IDE:** Use systematic bash/grep for consistency, verify with git diff before commit.
- **Breaking existing installs:** Maintain backward compatibility in hooks that read from filesystem (check both old and new paths during transition).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| ASCII art generation | Custom text-to-art renderer | Online generators ([ASCII Art Generator](http://www.network-science.de/ascii/), [oh-my-logo](https://dev.to/shinshin86/cli-renaissance-alert-meet-oh-my-logo-your-gemini-cli-and-claude-code-style-logo-generator-2gp1)) | Character spacing and alignment is complex, generators handle edge cases |
| Package name validation | Custom regex checks | npm publish pre-flight checks | npm validates package names, duplicate effort |
| File-based state management library | Custom JSON serialization | Existing STATE.md markdown pattern | Already works, human-readable, git-trackable |
| Loop counter persistence | Custom database | Markdown table in STATE.md | Simpler, debuggable, matches existing state tracking pattern |

**Key insight:** The existing GSD architecture already solves state persistence elegantly via markdown files. Don't introduce complexity by adding databases or specialized state libraries.

## Common Pitfalls

### Pitfall 1: Incomplete Reference Updates
**What goes wrong:** Renaming file/directory names but missing string references in code leads to broken imports and missing files at runtime.
**Why it happens:** Text references (in comments, strings, template paths) aren't caught by automated refactoring tools.
**How to avoid:**
1. Use grep to find ALL references: `grep -r "gsd\|GSD\|get-shit-done" . --include="*.md" --include="*.js" --include="*.json"`
2. Create checklist of rename categories: filenames, directory names, package.json fields, npm package name, documentation titles, command names (gsd: → grd:), agent names (gsd-* → grd-*), path references in code
3. Verify each category with targeted grep after rename
4. Test installation in clean environment before publishing

**Warning signs:**
- Module not found errors during npm install
- 404s when loading @-referenced files
- Commands not appearing in slash command list
- Hooks failing silently

### Pitfall 2: NPM Package Name Conflicts
**What goes wrong:** Publishing new package without checking availability leads to publish failure or namespace squatting issues.
**Why it happens:** Not checking npm registry before committing to new name.
**How to avoid:**
1. Check availability: `npm search get-research-done` (should return no results)
2. Verify on npmjs.com before starting refactor
3. Consider scoped packages (@your-org/grd) if name taken
4. Reserve name ASAP: publish v0.0.1 placeholder if needed

**Warning signs:**
- npm publish fails with "package name taken"
- Similar package exists with different purpose (namespace confusion)

### Pitfall 3: ASCII Art Rendering Issues
**What goes wrong:** ASCII art looks perfect in development but breaks in user terminals due to encoding or monospace font issues.
**Why it happens:** Different terminals handle ANSI escape codes differently; some fonts aren't truly monospace.
**How to avoid:**
1. Use only basic ASCII characters (32-126 range)
2. Test in multiple terminals: iTerm2, Terminal.app, Windows Terminal, Alacritty
3. Avoid extended Unicode (box drawing chars) unless absolutely required
4. Verify at 80-character width (common default)
5. Add fallback: if banner rendering fails, show simple text logo

**Warning signs:**
- Banner alignment breaks in certain terminals
- Colors don't render (check ANSI escape code support)
- Extra/missing characters in output

### Pitfall 4: State Migration Without Backwards Compatibility
**What goes wrong:** Extending STATE.md structure breaks existing workflows that parse specific sections.
**Why it happens:** Adding new sections changes file structure, scripts expect old format.
**How to avoid:**
1. Add new sections at end (preserve existing section order)
2. Make new sections optional (check for existence before parsing)
3. Version STATE.md format in frontmatter if needed: `<!-- STATE.md v2 -->`
4. Update all workflows that read STATE.md to handle both formats

**Warning signs:**
- Workflows fail with parse errors after STATE.md update
- Old sections missing expected data
- Scripts that use grep/awk on STATE.md break

## Code Examples

Verified patterns from existing codebase:

### Systematic Renaming with Git
```bash
# Source: GSD refactoring best practices
# Find all files that need renaming
find . -type f \( -name "*gsd*" -o -name "*get-shit-done*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*"

# Rename files atomically (do not use git mv in loop - creates partial state)
# Instead: rename all, then stage all at once

# Rename directories
mv commands/gsd commands/grd
mv get-shit-done get-research-done

# Rename agent files
for file in agents/gsd-*.md; do
  git mv "$file" "${file/gsd-/grd-}"
done

# Rename hooks
for file in hooks/gsd-*.js; do
  git mv "$file" "${file/gsd-/grd-}"
done

# Update text references in all files
find . -type f \( -name "*.md" -o -name "*.js" -o -name "*.json" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" \
  -exec sed -i '' 's/gsd:/grd:/g' {} +

find . -type f \( -name "*.md" -o -name "*.js" -o -name "*.json" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" \
  -exec sed -i '' 's/get-shit-done/get-research-done/g' {} +

# Verify no references remain
grep -r "gsd:" . --include="*.md" --include="*.js" | grep -v "grd:"
grep -r "get-shit-done" . --include="*.md" --include="*.js"

# Stage all changes atomically
git add -A
git status  # Review changes
git commit -m "refactor: rename GSD → GRD across entire codebase"
```

### Extended STATE.md Template
```markdown
# Source: Extending get-research-done/templates/state.md

## Research Loop History

**Active Loop:** [N] (started [YYYY-MM-DD])
**Loop Focus:** [Current research focus area]

| Loop | Started | Duration | Focus | Status | Key Findings |
|------|---------|----------|-------|--------|--------------|
| 1 | [date] | [hours] | [area] | Complete | [summary] |
| 2 | [date] | [hours] | [area] | In progress | [current state] |

**Loop [N] Progress:**
- [x] Phase 1: Initial exploration
- [x] Phase 2: Source gathering
- [ ] Phase 3: Cross-validation
- [ ] Phase 4: Synthesis

**Iteration Notes:**
- [Observation from current loop]
- [Pattern identified]
- [Question to explore next]
```

### Package.json Updates
```json
// Source: Current package.json with required updates
{
  "name": "get-research-done",
  "version": "2.0.0",  // Major version bump for rebrand
  "description": "A research-oriented meta-prompting, context engineering and spec-driven development system for Claude Code by TÂCHES.",
  "bin": {
    "get-research-done": "bin/install.js"
  },
  "files": [
    "bin",
    "commands",
    "get-research-done",  // Renamed from get-shit-done
    "agents",
    "hooks/dist",
    "scripts"
  ],
  "keywords": [
    "claude",
    "claude-code",
    "ai",
    "research",  // New keyword
    "meta-prompting",
    "context-engineering",
    "spec-driven-development"
  ],
  "repository": {
    "type": "git",
    "url": "git+https://github.com/glittercowboy/get-research-done.git"  // Updated
  },
  "homepage": "https://github.com/glittercowboy/get-research-done",  // Updated
  "bugs": {
    "url": "https://github.com/glittercowboy/get-research-done/issues"  // Updated
  }
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Generic ASCII text | Filled-in block letter ASCII art | 2026 | CLI tools using Claude Code style logos see 40% higher GitHub star conversion |
| npm package rename by abandoning old | Deprecate old package with migration message | Established pattern | Users get automatic notification to migrate |
| In-memory state | File-based persistent state | Standard for Node.js CLIs | State survives restarts, enables session restoration |
| Custom state management libs | Built-in markdown + fs module | Current GSD pattern | Simpler, debuggable, human-readable |

**Deprecated/outdated:**
- Plain text logos without styling - CLI users expect branded experience in 2026
- Breaking package changes without deprecation warnings - npm best practice is to deprecate old package
- JSON for human-readable state - Markdown tables are more accessible and git-friendly

## Open Questions

Things that couldn't be fully resolved:

1. **GitHub repository rename timing**
   - What we know: Package name change can happen before or after GitHub repo rename
   - What's unclear: Whether to rename GitHub repo simultaneously or keep get-shit-done repo with new package
   - Recommendation: Coordinate GitHub rename with package publish, update all URLs atomically

2. **Loop tracking granularity**
   - What we know: STATE.md should track research loop iterations with start/end times and outcomes
   - What's unclear: What fields are essential vs. optional (duration? number of sources? confidence level?)
   - Recommendation: Start minimal (loop number, focus, status), extend based on actual research workflow needs

3. **Backwards compatibility for existing GSD users**
   - What we know: Existing GSD installations will need migration path
   - What's unclear: Should installer detect old GSD install and auto-migrate, or require manual uninstall?
   - Recommendation: Installer should detect ~/.claude/get-shit-done/, offer to migrate automatically, preserve user's .planning/ data

## Sources

### Primary (HIGH confidence)
- Existing codebase analysis:
  - `/bin/install.js` - Installation patterns, banner display, rename logic
  - `/package.json` - Current package structure and dependencies
  - `/get-shit-done/templates/state.md` - Current STATE.md template
  - `/GSD-STYLE.md` - Architecture principles and conventions
  - `/.planning/codebase/STRUCTURE.md` - Directory layout and file organization
  - `/.planning/codebase/CONVENTIONS.md` - Naming patterns and code style
- File count analysis:
  - 120 total files (.md, .js, .json)
  - 91 files containing GSD/gsd references
  - 27 command files in commands/gsd/
  - 11 agent files (gsd-*.md)
  - 51 workflow/template files in get-shit-done/

### Secondary (MEDIUM confidence)
- [Orbit2x Creative ASCII Art Ideas 2026](https://orbit2x.com/blog/50-creative-ascii-art-ideas-examples-use-cases) - CLI branding ROI and best practices
- [CLI Renaissance Alert: Meet oh-my-logo](https://dev.to/shinshin86/cli-renaissance-alert-meet-oh-my-logo-your-gemini-cli-and-claude-code-style-logo-generator-2gp1) - 2026 ASCII art trends
- [Lerna: A Tale of Renaming NPM Packages](https://medium.com/@dlacustodio/lerna-a-tale-of-renaming-npm-packages-4d3c534bc31) - npm rename patterns
- [Store State on Filesystem in Node.js CLIs with Conf](https://egghead.io/lessons/javascript-store-state-on-filesystem-in-node-js-clis-with-conf) - CLI state persistence patterns

### Tertiary (LOW confidence)
- [npm Docs: Renaming an organization](https://docs.npmjs.com/renaming-an-organization/) - Organization-level rename (not applicable to single package)
- [Strategies for State Management in Node.js](https://nelkodev.com/en/blog/mastering-state-management-in-large-node-js-applications/) - General state management (GRD already has simpler markdown-based approach)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Existing codebase verified, no new dependencies required
- Architecture: HIGH - Patterns extracted directly from working codebase
- Pitfalls: MEDIUM - Based on npm best practices and CLI development experience, not GRD-specific evidence

**Research date:** 2026-01-27
**Valid until:** 2026-02-27 (30 days - stable refactoring patterns, npm conventions unlikely to change)
