---
type: prompt
name: grd:complete-study
description: Archive completed study and prepare for next version
argument-hint: <version>
allowed-tools:
  - Read
  - Write
  - Bash
---

<objective>
Mark study {{version}} complete, archive to studies/, and update STUDY_PROTOCOL.md and HYPOTHESES.md.

Purpose: Create historical record of completed research, archive study artifacts (protocol + hypotheses + results), and prepare for next study.
Output: Study archived (protocol + hypotheses + findings), PROJECT.md evolved, git tagged.
</objective>

<execution_context>
**Load these files NOW (before proceeding):**

- @~/.claude/get-research-done/workflows/complete-study.md (main workflow)
- @~/.claude/get-research-done/templates/study-archive.md (archive template)
  </execution_context>

<context>
**Project files:**
- `.planning/STUDY_PROTOCOL.md`
- `.planning/HYPOTHESES.md`
- `.planning/STATE.md`
- `.planning/PROJECT.md`

**User input:**

- Version: {{version}} (e.g., "1.0", "1.1", "2.0")
  </context>

<process>

**Follow complete-study.md workflow:**

0. **Check for audit:**

   - Look for `.planning/v{{version}}-STUDY-AUDIT.md`
   - If missing or stale: recommend `/grd:audit-study` first
   - If audit status is `gaps_found`: recommend `/grd:plan-study-gaps` first
   - If audit status is `passed`: proceed to step 1

   ```markdown
   ## Pre-flight Check

   {If no v{{version}}-STUDY-AUDIT.md:}
   ⚠ No study audit found. Run `/grd:audit-study` first to verify
   hypothesis coverage, experiment validity, and statistical rigor.

   {If audit has gaps:}
   ⚠ Study audit found gaps. Run `/grd:plan-study-gaps` to create
   experiments that close the gaps, or proceed anyway to accept limitations.

   {If audit passed:}
   ✓ Study audit passed. Proceeding with completion.
   ```

1. **Verify readiness:**

   - Check all experiments in study have completed plans (SUMMARY.md exists)
   - Check all primary hypotheses have been tested
   - Present study scope and stats
   - Wait for confirmation

2. **Gather stats:**

   - Count experiments, analyses, findings
   - Calculate git range, file changes
   - Extract timeline from git log
   - Present summary, confirm

3. **Extract findings:**

   - Read all experiment SUMMARY.md files in study range
   - Extract 4-6 key findings
   - Note which hypotheses were supported/rejected
   - Present for approval

4. **Archive study:**

   - Create `.planning/studies/v{{version}}-PROTOCOL.md`
   - Extract full experiment details from STUDY_PROTOCOL.md
   - Fill study-archive.md template
   - Update STUDY_PROTOCOL.md to one-line summary with link

5. **Archive hypotheses:**

   - Create `.planning/studies/v{{version}}-HYPOTHESES.md`
   - Mark all hypotheses as tested (checkboxes checked)
   - Note hypothesis outcomes (supported, rejected, inconclusive)
   - Delete `.planning/HYPOTHESES.md` (fresh one created for next study)

6. **Update PROJECT.md:**

   - Add "Current State" section with completed findings
   - Add "Validated Findings" from this study
   - Add "Next Study Goals" section
   - Archive previous content in `<details>` (if v1.1+)

7. **Commit and tag:**

   - Stage: STUDIES.md, PROJECT.md, STUDY_PROTOCOL.md, STATE.md, archive files
   - Commit: `chore: archive v{{version}} study`
   - Tag: `git tag -a v{{version}} -m "[study summary - N hypotheses tested]"`
   - Ask about pushing tag

8. **Offer next steps:**
   - `/grd:new-study` — start next study (questioning → literature review → hypotheses → protocol)

</process>

<success_criteria>

- Study archived to `.planning/studies/v{{version}}-PROTOCOL.md`
- Hypotheses archived to `.planning/studies/v{{version}}-HYPOTHESES.md`
- `.planning/HYPOTHESES.md` deleted (fresh for next study)
- STUDY_PROTOCOL.md collapsed to one-line entry
- PROJECT.md updated with findings
- Git tag v{{version}} created
- Commit successful
- User knows next steps
  </success_criteria>

<critical_rules>

- **Load workflow first:** Read complete-study.md before executing
- **Verify completion:** All experiments must have SUMMARY.md files
- **User confirmation:** Wait for approval at verification gates
- **Archive before deleting:** Always create archive files before updating/deleting originals
- **One-line summary:** Collapsed study in STUDY_PROTOCOL.md should be single line with link
- **Fresh hypotheses:** Next study starts with `/grd:new-study` which includes hypothesis definition
  </critical_rules>
