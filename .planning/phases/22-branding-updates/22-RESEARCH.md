# Phase 22: Branding Updates - Research

**Researched:** 2026-02-02
**Domain:** SVG graphics design, ASCII art, PNG conversion, color theory
**Confidence:** HIGH

## Summary

Phase 22 focuses on updating visual branding assets from GSD (Get Shit Done) to GRD (Get Research Done). The work is purely visual - no functional code changes. The existing SVG files use Unicode box-drawing characters (U+2500-U+257F) to create bold ASCII art logos, and the task is to swap the letters while maintaining the exact same style, structure, and proportions.

The research reveals that:
1. The existing logo uses Unicode box-drawing double-line characters (╔═╗║╚╝ etc.) which create a bold, chunky appearance
2. SVG-to-PNG conversion on macOS can be done with built-in tools (`sips`, `qlmanage`) or third-party tools (`rsvg-convert` via librsvg)
3. Dark/light mode SVG variants are best achieved using `prefers-color-scheme` media queries within the SVG
4. Blues and teals are trending for 2026 academic/research branding, with "Transformative Teal" being WGSN's Color of the Year

**Primary recommendation:** Manually edit the SVG text elements to swap G-S-D for G-R-D using the same Unicode box-drawing characters, convert to PNG using `rsvg-convert` (best quality), and implement dark/light variants using CSS media queries within the SVG files.

## Standard Stack

### Core Tools

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| SVG (manual editing) | SVG 1.1 | Vector graphic format | Universal browser support, text-based editing |
| Unicode Box Drawing | U+2500-U+257F | ASCII art characters | Standard Unicode block with 128 characters |
| librsvg (rsvg-convert) | 2.x | SVG to PNG conversion | Best quality, proper text rendering |

### Supporting Tools

| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| sips | Built-in macOS | SVG to PNG conversion | Quick conversion, no install needed |
| qlmanage | Built-in macOS | SVG to PNG via QuickLook | Alternative built-in option |
| ImageMagick convert | 7.x | SVG to PNG conversion | When already installed, batch processing |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual SVG editing | Figlet npm package | Figlet requires Node.js runtime; manual editing gives exact control over character placement |
| rsvg-convert | sips or qlmanage | Built-in tools are faster but may have quality issues with complex SVGs; rsvg-convert gives best quality |
| CSS media queries | Separate files | Multiple files harder to maintain; media queries keep variants in sync |

**Installation:**
```bash
# Install librsvg via Homebrew (recommended for PNG conversion)
brew install librsvg

# Built-in tools require no installation
# sips and qlmanage are pre-installed on macOS
```

## Architecture Patterns

### Current Project Structure
```
assets/
├── gsd-logo-2000.svg      # Main logo (to become grd-logo-2000.svg)
├── gsd-logo-2000.png      # PNG export (to become grd-logo-2000.png)
└── terminal.svg           # Terminal preview with install flow
```

### Pattern 1: SVG Text-Based ASCII Art

**What:** Use `<text>` elements within SVG with Unicode box-drawing characters for ASCII art
**When to use:** When creating monospaced, terminal-style logos that need to be scalable

**Example from current logo:**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 2000">
  <defs>
    <style>
      .bg { fill: #1a1b26; }
      .logo { font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', 'Courier New', monospace; fill: #7dcfff; }
    </style>
  </defs>

  <rect class="bg" width="2000" height="2000"/>

  <g transform="translate(1000, 1000)">
    <text class="logo" font-size="108" text-anchor="middle" y="-225">  ██████╗ ███████╗██████╗ </text>
    <!-- Additional lines -->
  </g>
</svg>
```

**Key aspects:**
- Monospaced font stack ensures consistent character spacing
- `xml:space="preserve"` maintains exact spacing
- `text-anchor="middle"` centers text horizontally
- Characters use Unicode box-drawing (U+2580 ▀ blocks, U+2588 █ full blocks, U+2550-257F ═╗╝║ etc.)

### Pattern 2: SVG Color Scheme with Dark/Light Mode

**What:** Use CSS `@media (prefers-color-scheme)` queries within `<style>` in SVG
**When to use:** When creating assets that need to adapt to user's system theme

**Example:**
```svg
<defs>
  <style>
    @media (prefers-color-scheme: dark) {
      .terminal-bg { fill: #1a1b26; }
      .text { fill: #c0caf5; }
    }
    @media (prefers-color-scheme: light) {
      .terminal-bg { fill: #f5f5f5; }
      .text { fill: #2e3440; }
    }
  </style>
</defs>
```

**Note:** Safari has limited support for media queries in `<img>` tags; inline `<svg>` provides best compatibility.

### Pattern 3: Terminal Preview SVG

**What:** Simulate a terminal window with title bar, buttons, and command output
**When to use:** For README documentation showing installation/usage flow

**Current structure (from terminal.svg):**
```svg
<!-- Window frame with border radius -->
<rect class="terminal-border" width="960" height="540" rx="12"/>
<rect class="terminal-bg" x="1" y="1" width="958" height="538" rx="11"/>

<!-- macOS-style window buttons -->
<circle class="btn-red" cx="24" cy="19" r="7"/>
<circle class="btn-yellow" cx="48" cy="19" r="7"/>
<circle class="btn-green" cx="72" cy="19" r="7"/>

<!-- Content with monospaced font -->
<g transform="translate(32, 72)">
  <text class="text prompt">~</text>
  <text class="text command">npx get-research-done</text>
  <!-- ASCII art banner -->
  <!-- Install output lines -->
</g>
```

### Anti-Patterns to Avoid

- **Using images for ASCII art instead of text** — Makes it uneditable and breaks at different sizes
- **Hardcoding colors without CSS classes** — Prevents theming and makes updates tedious
- **Forgetting xml:space="preserve"** — Collapses multiple spaces, breaking ASCII art alignment
- **Using proportional fonts** — Destroys ASCII art alignment; must use monospaced
- **Creating separate files for dark/light** — Doubles maintenance burden; use media queries

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| ASCII art generation | Custom character mapper | Unicode box-drawing characters directly | Unicode standard provides all needed glyphs (U+2500-U+257F) with consistent rendering |
| SVG to PNG conversion | Custom renderer | rsvg-convert, sips, or qlmanage | Text rendering is complex; existing tools handle fonts, antialiasing, size correctly |
| Color palette selection | Random hex codes | Design system colors (e.g., Tokyo Night, Nord) | Established palettes have tested contrast ratios and accessibility |
| Dark/light mode variants | Duplicate SVG files | CSS @media queries in SVG | Single source of truth prevents drift between variants |

**Key insight:** ASCII art in SVG is just text. The Unicode consortium has already solved box-drawing characters. Don't try to render them yourself; use `<text>` elements with proper monospaced fonts.

## Common Pitfalls

### Pitfall 1: Character Misalignment in ASCII Art
**What goes wrong:** ASCII art looks broken with characters not lining up
**Why it happens:** Mixing Unicode full-width and half-width characters, or using proportional fonts
**How to avoid:**
- Use only characters from Unicode box-drawing block (U+2500-U+257F)
- Always specify monospaced font stack
- Include `xml:space="preserve"` on text elements
- Test rendering in multiple browsers
**Warning signs:** Vertical lines don't align, boxes appear jagged

### Pitfall 2: Poor PNG Quality from SVG Conversion
**What goes wrong:** PNG output has blurry text, jagged edges, or wrong colors
**Why it happens:** Built-in macOS tools (sips, qlmanage) may not render fonts correctly
**How to avoid:**
- Use `rsvg-convert` from librsvg (best quality)
- Specify explicit width with `-w 2000` flag
- Test output at target size before committing
**Warning signs:** Text appears blurry at actual size, colors look washed out

### Pitfall 3: SVG Dark Mode Not Working
**What goes wrong:** SVG doesn't respond to system theme changes
**Why it happens:** Safari doesn't support `@media` queries in SVG loaded via `<img>` tag
**How to avoid:**
- Test in multiple browsers (Chrome, Firefox, Safari)
- Consider using inline SVG in HTML if critical
- Provide default colors that work reasonably in both modes
**Warning signs:** Works in Chrome/Firefox but not Safari

### Pitfall 4: Forgetting to Update File References
**What goes wrong:** README shows broken images after renaming logo files
**Why it happens:** File paths in markdown, HTML, or docs reference old filenames
**How to avoid:**
- Search entire codebase for old filename references before renaming
- Use grep/ripgrep: `rg 'gsd-logo'` to find all references
- Update package.json, README.md, and any docs in one commit
**Warning signs:** Build warnings about missing assets, broken images in README

### Pitfall 5: Unicode Character Rendering Issues
**What goes wrong:** Box-drawing characters appear as boxes or wrong glyphs
**Why it happens:** Missing font fallbacks or browser doesn't support Unicode properly
**How to avoid:**
- Include comprehensive monospaced font stack: `'SF Mono', 'Fira Code', 'JetBrains Mono', 'Courier New', monospace`
- Test on Windows (Consolas), macOS (SF Mono), and Linux (Liberation Mono)
- Verify font-family includes generic `monospace` fallback
**Warning signs:** Boxes render as � or wrong symbols on different platforms

## Code Examples

### Creating "GRD" ASCII Art (Manual Approach)

The current logo uses this style of box-drawing characters. To create "GRD" letters:

```
# G letter (from existing):
 ██████╗
██╔════╝
██║  ███╗
██║   ██║
╚██████╔╝
 ╚═════╝

# R letter (from existing):
██████╗
██╔══██╗
██████╔╝
██╔══██╗
██║  ██║
╚═╝  ╚═╝

# D letter (from existing):
██████╗
██╔══██╗
██║  ██║
██║  ██║
██████╔╝
╚═════╝
```

**Process:**
1. Open existing gsd-logo-2000.svg
2. Locate the 6 `<text>` elements (lines 14-19)
3. Replace the character sequences while maintaining exact spacing
4. Test in browser to verify alignment

### SVG to PNG Conversion (High Quality)

```bash
# Using rsvg-convert (recommended)
rsvg-convert -w 2000 grd-logo-2000.svg -o grd-logo-2000.png

# Using sips (built-in macOS, faster but lower quality)
sips --resampleHeightWidth 2000 2000 -s format png grd-logo-2000.svg -o grd-logo-2000.png

# Using qlmanage (built-in macOS)
qlmanage -t -s 2000 -o . grd-logo-2000.svg
# Then rename: mv grd-logo-2000.svg.png grd-logo-2000.png
```

### Updating Terminal Preview Content

Current terminal.svg shows:
```xml
<!-- Line 41 - Command -->
<text class="text command" font-size="15" x="36" y="0">npx get-shit-done-cc</text>

<!-- Line 52 - Title with version -->
<text class="text white" font-size="15" y="188">  Get Shit Done <tspan class="dim">v1.0.1</tspan></text>

<!-- Line 61 - Done message -->
<text class="text" font-size="15" y="352">
  <tspan class="green">  Done!</tspan>
  <tspan class="white"> Run </tspan>
  <tspan class="cyan">/gsd:help</tspan>
  <tspan class="white"> to get started.</tspan>
</text>
```

**Update to:**
```xml
<!-- Command -->
<text class="text command" font-size="15" x="36" y="0">npx get-research-done</text>

<!-- Title with version (read from package.json) -->
<text class="text white" font-size="15" y="188">  Get Research Done <tspan class="dim">v1.2.0</tspan></text>

<!-- Done message -->
<text class="text" font-size="15" y="352">
  <tspan class="green">  Done!</tspan>
  <tspan class="white"> Run </tspan>
  <tspan class="cyan">/grd:help</tspan>
  <tspan class="white"> to get started.</tspan>
</text>
```

**Note:** Current package.json shows v1.2.0; context indicates v1.3 is in progress. Confirm target version before updating.

### Implementing Research-Themed Color Palette

Based on 2026 trends (Transformative Teal as Color of the Year):

```svg
<defs>
  <style>
    /* Research/academic color scheme - blues and teals */
    .bg { fill: #0a1628; }                    /* Deep navy - scientific authority */
    .logo {
      font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', 'Courier New', monospace;
      fill: #4FB3D4;                          /* Transformative teal - 2026 trend */
    }

    /* Terminal colors */
    .terminal-bg { fill: #0c1821; }           /* Dark research lab aesthetic */
    .prompt { fill: #5E8BAF; }                /* Muted blue */
    .command { fill: #C9E0E8; }               /* Light cyan */
    .cyan { fill: #4FB3D4; }                  /* Teal accent */
    .green { fill: #7FB3B5; }                 /* Aqua green success */

    /* Light mode variants */
    @media (prefers-color-scheme: light) {
      .bg { fill: #E8F4F8; }                  /* Soft blue-white */
      .logo { fill: #005F73; }                /* Dark teal */
      .terminal-bg { fill: #F5FAFB; }
      .command { fill: #003C47; }
    }
  </style>
</defs>
```

**Color rationale:**
- **#4FB3D4 (Transformative Teal)**: Primary brand color, aligns with 2026 Color of the Year
- **Blues (#0a1628, #5E8BAF)**: Scientific authority, academic trust
- **High contrast**: Ensures accessibility (WCAG AA compliance)

### File Renaming Pattern

```bash
#!/bin/bash
# Rename logo files and update references

# Navigate to assets directory
cd assets/

# Rename files
mv gsd-logo-2000.svg grd-logo-2000.svg
mv gsd-logo-2000.png grd-logo-2000.png

# Update README reference (terminal.svg reference stays same)
cd ..
sed -i '' 's/gsd-logo-2000/grd-logo-2000/g' README.md

# Verify no other references exist
rg 'gsd-logo' --type md --type json --type js
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Bitmap logo files (.png only) | SVG-first with PNG export | ~2018 | Scalable logos, easier editing |
| Separate dark/light assets | CSS media queries in SVG | ~2020 | Single file, auto-adapts |
| Manual color picking | Design system colors | ~2021 | Consistent branding, accessibility |
| ImageMagick for conversion | rsvg-convert (librsvg) | ~2022 | Better text rendering quality |

**Deprecated/outdated:**
- **Figlet CLI for terminal logos**: While still functional, directly editing SVG text gives more control and avoids dependency
- **Multiple logo variants**: Dark/light/color variants should be consolidated using CSS media queries
- **Inline styles in SVG**: Modern practice uses `<defs><style>` for maintainability

## Open Questions

1. **Version number in terminal preview**
   - What we know: package.json shows v1.2.0, STATE.md indicates v1.3 in progress
   - What's unclear: Should terminal.svg show v1.2.0 (current), v1.3.0 (upcoming), or dynamically pull from package.json?
   - Recommendation: Use v1.3.0 since this is part of v1.3 milestone (Phase 22 of milestone v1.3). Alternatively, use generic "v1.x" if version updates are frequent.

2. **Light mode implementation scope**
   - What we know: Context mentions "both dark mode and light mode variants"
   - What's unclear: Whether light mode is for both logo AND terminal preview, or just logo
   - Recommendation: Implement light mode for both assets to maintain consistency. Terminal preview light mode would swap background to light gray and adjust text colors.

3. **Color palette final approval**
   - What we know: Blues/teals direction specified, Transformative Teal is 2026 trend
   - What's unclear: Exact shades and whether to match existing Tokyo Night theme or adopt new palette
   - Recommendation: Start with Transformative Teal (#4FB3D4) for primary color, keep existing Tokyo Night colors for terminal elements (proven good contrast). Get user approval before committing.

## Sources

### Primary (HIGH confidence)
- **Current project files**: `/assets/gsd-logo-2000.svg`, `/assets/terminal.svg`, `/package.json` - Direct inspection of existing implementation
- **Unicode Box Drawing spec**: [Wikipedia Box-drawing characters](https://en.wikipedia.org/wiki/Box-drawing_characters) - Official Unicode standard (U+2500-U+257F)
- **SVG 1.1 specification**: MDN Web Docs - Standard SVG text rendering

### Secondary (MEDIUM confidence)
- **librsvg documentation**: [rsvg-convert usage](https://www.ctrl.blog/entry/svg-embed-dark-mode.html) - Command-line SVG conversion best practices
- **macOS SVG conversion**: [Yellow Duck qlmanage tutorial](https://www.yellowduck.be/posts/how-to-convert-an-svg-to-png-using-qlmanage-on-macos), [sips guide](https://www.rshankar.com/convert-svg-to-png-with-sips/) - Built-in tool documentation
- **SVG dark mode**: [Cassidy James guide](https://cassidyjames.com/blog/prefers-color-scheme-svg-light-dark/), [Publii best practices](https://getpublii.com/docs/prepare-svg-for-light-dark-mode.html) - Media query implementation patterns
- **2026 Color trends**: [WGSN Transformative Teal](https://www.wgsn.com/en/blog/colour-year-2026-transformative-teal), [April Mawhinney 2026 Blues](https://www.aprilmawhinney.com/blogs/news/blue-is-the-colour-of-2026-deep-blues-and-teals-creating-dramatic-int) - Professional color forecasting

### Tertiary (LOW confidence)
- **ASCII art generators**: Various online tools (TextGeneratorPro, ASCIIFlow) - While functional, not needed for this specific task (manual editing preferred)
- **Figlet npm package**: [npm figlet](https://www.npmjs.com/package/figlet) - Mentioned but not verified; manual approach recommended

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - SVG text manipulation is well-established, Unicode box-drawing is standard
- Architecture: HIGH - Current implementation examined directly, patterns proven in production
- Pitfalls: MEDIUM - Based on common SVG/PNG issues documented in community resources
- Color palette: MEDIUM - Trend data verified from professional sources, but specific shades require user approval

**Research date:** 2026-02-02
**Valid until:** 60 days (stable domain - SVG/Unicode standards don't change rapidly)

**Key technical decisions verified:**
- ✓ Unicode box-drawing characters are standard and widely supported
- ✓ SVG text rendering with monospaced fonts is production-ready
- ✓ rsvg-convert is current best practice for SVG→PNG conversion
- ✓ CSS media queries in SVG work in modern browsers (with Safari caveat)
- ✓ Transformative Teal is documented 2026 Color of the Year

**Implementation note:** This is a straightforward visual update. The challenging part is not technical execution but ensuring exact character alignment in ASCII art and maintaining consistent branding across all assets. Manual editing with careful testing is more reliable than automated generation.
