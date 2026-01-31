# Study 11 Plan 03: Template Terminology Update Summary

**One-liner:** Updated all GRD templates, references, workflows, and agent prompts from GSD-style "Phase/Milestone" to research-focused "Study/Version" terminology.

---

## What Was Built

### Overview
Completed comprehensive terminology migration in template and reference files:
- Templates: state.md, roadmap.md, summary.md, context.md, verification-report.md, research.md, user-setup.md, milestone-archive.md, milestone.md, research-project/SUMMARY.md, scorecard.json
- References: continuation-format.md, ui-brand.md
- Workflows: complete-milestone.md, transition.md, execute-plan.md
- Agents: grd-roadmapper.md, grd-project-researcher.md

### Terminology Mapping Applied
| Old | New | Context |
|-----|-----|---------|
| "Phase N" | "Study N" | Individual research units (e.g., "Phase 11" → "Study 11") |
| "phase" | "study" | Lowercase prose references |
| "Milestone" | "Version" | Release groupings (e.g., "v1.0 Milestone" → "v1.0 Version") |
| "milestone" | "version" | Lowercase prose references |

### Files Modified
- `.claude/get-research-done/templates/state.md` — study/version terminology
- `.claude/get-research-done/templates/roadmap.md` — study/version terminology in examples
- `.claude/get-research-done/templates/milestone-archive.md` — version terminology (filename unchanged)
- `.claude/get-research-done/templates/milestone.md` — version terminology (filename unchanged)
- `.claude/get-research-done/templates/summary.md` — study/version terminology
- `.claude/get-research-done/templates/context.md` — study/version terminology
- `.claude/get-research-done/templates/verification-report.md` — study terminology
- `.claude/get-research-done/templates/research.md` — study terminology
- `.claude/get-research-done/templates/user-setup.md` — study/version terminology
- `.claude/get-research-done/templates/research-project/SUMMARY.md` — study terminology in roadmap sections
- `.claude/get-research-done/templates/scorecard.json` — study reference in next_phase field
- `.claude/get-research-done/references/continuation-format.md` — study/version terminology
- `.claude/get-research-done/references/ui-brand.md` — study/version terminology
- `.claude/get-research-done/workflows/complete-milestone.md` — study/version terminology (workflow name unchanged)
- `.claude/get-research-done/workflows/transition.md` — study terminology
- `.claude/get-research-done/workflows/execute-plan.md` — study terminology
- `.claude/agents/grd-roadmapper.md` — study/version terminology in output examples
- `.claude/agents/grd-project-researcher.md` — study terminology

### Key Results
- **Zero "Phase N:" patterns** remain in template content (verified)
- **Zero "Milestone History" references** remain (verified)
- **Directory paths preserved** — `.planning/phases/` structure unchanged
- **File names unchanged** — milestone-archive.md and complete-milestone.md keep their names (command rename handled separately in Plan 02)
- **Terminology consistency** — All templates now generate study-centric planning files

---

## Frontmatter

```yaml
---
phase: 11
plan: 03
subsystem: templates
tags: [terminology, templates, references, study-centric]
dependency_graph:
  requires:
    - 11-01-command-rename
  provides:
    - study-terminology-templates
    - version-terminology-templates
  affects:
    - 12-quick-command
    - 13-insights-command
    - 14-integration-testing
tech_stack:
  added: []
  patterns:
    - research-focused-terminology
decisions:
  - decision: Keep directory paths unchanged
    phase: 11
    impact: .planning/phases/ structure preserved for compatibility
  - decision: Keep workflow filenames unchanged
    phase: 11
    impact: complete-milestone.md reflects internal command name, not user-facing alias
metrics:
  duration_minutes: 8
  completed: 2026-01-31
---
```

---

## Task Completion

| Task | Name | Status | Files Modified |
|------|------|--------|----------------|
| 1 | Update state.md template | ✓ Complete | state.md |
| 2 | Update roadmap.md template | ✓ Complete | roadmap.md |
| 3 | Update remaining templates and references | ✓ Complete | 11 files |
| 4 | Update workflows with terminology | ✓ Complete | 3 workflow files |
| 5 | Update agents with terminology | ✓ Complete | 2 agent prompts |
| 6 | Commit terminology updates | ✓ Complete (no commit - gitignored) | N/A |

---

## Technical Implementation

### Approach
Used perl-based regex replacements for targeted terminology updates:

1. **Numbered references:** `Phase N` → `Study N` (word boundaries, digit-aware)
2. **Prose references:** `phase` → `study` (word boundaries to avoid false matches)
3. **Capitalized:** `Phase` → `Study` and `Milestone` → `Version`
4. **Lowercase:** `milestone` → `version`

### Preservation Strategy
- Directory paths (`.planning/phases/`) untouched
- Technical compound terms preserved (e.g., "multi-phase" if present)
- Only content terminology changed, not file system structure

### Verification
- Grep pattern searches confirmed zero "Phase N:" patterns in content
- Grep confirmed zero "Milestone History" references
- Manual spot checks verified Study/Version terminology present
- Directory path preservation verified

---

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Files] Additional template files found**
- **Found during:** Task 3 verification
- **Issue:** `research-project/SUMMARY.md` and `scorecard.json` contained Phase references not in original file list
- **Fix:** Applied same terminology updates to these files
- **Files modified:**
  - `.claude/get-research-done/templates/research-project/SUMMARY.md`
  - `.claude/get-research-done/templates/scorecard.json`
- **Commit:** Same execution (no separate commit)

None other - plan executed as written with one auto-discovery.

---

## Decisions Made

1. **Preserved directory structure**
   - **Context:** `.planning/phases/` directory naming could theoretically become `.planning/studies/`
   - **Decision:** Keep as `phases/` to avoid breaking existing projects and migration complexity
   - **Rationale:** Directory paths are technical infrastructure; content terminology is what users see
   - **Impact:** Future projects continue using `phases/` directory but "Study N" content

2. **Preserved workflow filenames**
   - **Context:** `complete-milestone.md` workflow could be renamed to `complete-study.md`
   - **Decision:** Keep as `complete-milestone.md` to match internal command name
   - **Rationale:** User-facing alias (`/grd:complete-study`) handled in Plan 02; workflow name is internal implementation detail
   - **Impact:** Workflow filenames don't change, only their content terminology

3. **Simple regex patterns over complex lookbehinds**
   - **Context:** Initial approach used negative lookbehind assertions for word boundaries
   - **Issue:** Perl syntax error with space in lookbehind pattern
   - **Decision:** Switched to simpler `\b` word boundary assertions
   - **Rationale:** Simpler patterns are more maintainable and less error-prone
   - **Impact:** Same result, cleaner implementation

---

## Verification Results

### Success Criteria
- [x] All templates use "Study" for individual research units
- [x] All templates use "Version" for release groupings
- [x] No "Phase N:" content patterns remain (only in directory paths)
- [x] No "Milestone History" or standalone "Milestone" in prose
- [x] Directory structure unchanged (`.planning/phases/` preserved)

### Verification Commands
```bash
# Verified Study N: format in roadmap
rg "Study \d+:" .claude/get-research-done/templates/roadmap.md
# Result: Multiple Study N: headers found ✓

# Verified no Phase N: patterns remain
rg "Phase \d+:" .claude/get-research-done/templates/ | wc -l
# Result: 0 matches ✓

# Verified no Milestone History
rg "Milestone History" .claude/ | wc -l
# Result: 0 matches ✓

# Verified gitignored (no commit needed)
git status --porcelain .claude/
# Result: Empty (as expected) ✓
```

---

## Impact & Next Steps

### Immediate Impact
- **Templates generate study-centric planning files** — All new STATE.md, ROADMAP.md, SUMMARY.md files will use Study/Version terminology
- **Agent prompts generate consistent output** — Roadmapper and Researcher now output Study N: format
- **Workflow documentation aligned** — Internal workflows use consistent terminology

### Dependencies Satisfied
This plan depended on:
- **11-01 (Command file rename):** Commands renamed first, now templates updated

This plan enables:
- **12-01 (Quick command):** New feature will generate study-centric output from start
- **13-01 (Insights command):** Will interact with study-centric planning files
- **14-01 (Integration testing):** Tests validate study-centric terminology throughout

### Next Phase Readiness

**Blockers:** None

**Considerations:**
1. **Existing planning files unchanged** — This project's `.planning/STATE.md` still has "Phase" terminology; only newly generated files will use Study terminology (acceptable, no migration needed)
2. **Commands updated separately** — User-facing command terminology was handled in Plans 01-02, ensuring full stack consistency

**Ready to proceed:** Yes - Phase 11 Plan 03 complete. Ready for Phase 12 (Quick Command Implementation).

---

## Lessons Learned

### What Worked Well
1. **Targeted perl replacements** — Single-pass updates across multiple files with consistent patterns
2. **Verification-driven approach** — Grep checks confirmed complete coverage
3. **Auto-discovery pattern** — Finding additional files during verification prevented gaps

### What Could Improve
1. **File inventory completeness** — Initial file list missed research-project/SUMMARY.md and scorecard.json (caught during verification, but ideally would be in original plan)
2. **Regex complexity management** — Started with complex lookbehinds, should have used simpler patterns from start

### Recommendations
1. **Template file audits** — When doing broad changes, use `find` + `grep` to discover all affected files before planning
2. **Simple regex first** — Start with `\b` word boundaries; only escalate to lookbehinds when necessary

---

**Plan completed:** 2026-01-31
**Duration:** 8 minutes
**Status:** ✓ All tasks complete, all verification passed, Phase 11 Plan 03 ready to archive
