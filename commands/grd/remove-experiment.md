---
name: grd:remove-experiment
description: Remove a future experiment from roadmap and renumber subsequent experiments
argument-hint: <experiment-number>
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

<objective>
Remove an unstarted future experiment from the roadmap and renumber all subsequent experiments to maintain a clean, linear sequence.

Purpose: Clean removal of work you've decided not to do, without polluting context with cancelled/deferred markers.
Output: Experiment deleted, all subsequent experiments renumbered, git commit as historical record.
</objective>

<execution_context>
@.planning/ROADMAP.md
@.planning/STATE.md
</execution_context>

<process>

<step name="parse_arguments">
Parse the command arguments:
- Argument is the experiment number to remove (integer or decimal)
- Example: `/grd:remove-experiment 17` → experiment = 17
- Example: `/grd:remove-experiment 16.1` → experiment = 16.1

If no argument provided:

```
ERROR: Experiment number required
Usage: /grd:remove-experiment <experiment-number>
Example: /grd:remove-experiment 17
```

Exit.
</step>

<step name="load_state">
Load project state:

```bash
cat .planning/STATE.md 2>/dev/null
cat .planning/ROADMAP.md 2>/dev/null
```

Parse current experiment number from STATE.md "Current Position" section.
</step>

<step name="validate_phase_exists">
Verify the target experiment exists in ROADMAP.md:

1. Search for `### Experiment {target}:` heading
2. If not found:

   ```
   ERROR: Experiment {target} not found in roadmap
   Available experiments: [list experiment numbers]
   ```

   Exit.
</step>

<step name="validate_future_phase">
Verify the experiment is a future experiment (not started):

1. Compare target experiment to current experiment from STATE.md
2. Target must be > current experiment number

If target <= current experiment:

```
ERROR: Cannot remove Experiment {target}

Only future experiments can be removed:
- Current experiment: {current}
- Experiment {target} is current or completed

To abandon current work, use /grd:pause-work instead.
```

Exit.

3. Check for SUMMARY.md files in experiment directory:

```bash
ls .planning/experiments/{target}-*/*-SUMMARY.md 2>/dev/null
```

If any SUMMARY.md files exist:

```
ERROR: Experiment {target} has completed work

Found executed plans:
- {list of SUMMARY.md files}

Cannot remove experiments with completed work.
```

Exit.
</step>

<step name="gather_phase_info">
Collect information about the experiment being removed:

1. Extract experiment name from STUDY_PROTOCOL.md heading: `### Experiment {target}: {Name}`
2. Find experiment directory: `.planning/experiments/{target}-{slug}/`
3. Find all subsequent experiments (integer and decimal) that need renumbering

**Subsequent experiment detection:**

For integer experiment removal (e.g., 17):
- Find all experiments > 17 (integers: 18, 19, 20...)
- Find all decimal experiments >= 17.0 and < 18.0 (17.1, 17.2...) → these become 16.x
- Find all decimal experiments for subsequent integers (18.1, 19.1...) → renumber with their parent

For decimal experiment removal (e.g., 17.1):
- Find all decimal experiments > 17.1 and < 18 (17.2, 17.3...) → renumber down
- Integer experiments unchanged

List all experiments that will be renumbered.
</step>

<step name="confirm_removal">
Present removal summary and confirm:

```
Removing Experiment {target}: {Name}

This will:
- Delete: .planning/experiments/{target}-{slug}/
- Renumber {N} subsequent experiments:
  - Experiment 18 → Experiment 17
  - Experiment 18.1 → Experiment 17.1
  - Experiment 19 → Experiment 18
  [etc.]

Proceed? (y/n)
```

Wait for confirmation.
</step>

<step name="delete_phase_directory">
Delete the target experiment directory if it exists:

```bash
if [ -d ".planning/experiments/{target}-{slug}" ]; then
  rm -rf ".planning/experiments/{target}-{slug}"
  echo "Deleted: .planning/experiments/{target}-{slug}/"
fi
```

If directory doesn't exist, note: "No directory to delete (experiment not yet created)"
</step>

<step name="renumber_directories">
Rename all subsequent experiment directories:

For each experiment directory that needs renumbering (in reverse order to avoid conflicts):

```bash
# Example: renaming 18-dashboard to 17-dashboard
mv ".planning/experiments/18-dashboard" ".planning/experiments/17-dashboard"
```

Process in descending order (20→19, then 19→18, then 18→17) to avoid overwriting.

Also rename decimal experiment directories:
- `17.1-fix-bug` → `16.1-fix-bug` (if removing integer 17)
- `17.2-hotfix` → `17.1-hotfix` (if removing decimal 17.1)
</step>

<step name="rename_files_in_directories">
Rename plan files inside renumbered directories:

For each renumbered directory, rename files that contain the experiment number:

```bash
# Inside 17-dashboard (was 18-dashboard):
mv "18-01-PLAN.md" "17-01-PLAN.md"
mv "18-02-PLAN.md" "17-02-PLAN.md"
mv "18-01-SUMMARY.md" "17-01-SUMMARY.md"  # if exists
# etc.
```

Also handle CONTEXT.md and DISCOVERY.md (these don't have experiment prefixes, so no rename needed).
</step>

<step name="update_roadmap">
Update ROADMAP.md:

1. **Remove the experiment section entirely:**
   - Delete from `### Experiment {target}:` to the next experiment heading (or section end)

2. **Remove from experiment list:**
   - Delete line `- [ ] **Experiment {target}: {Name}**` or similar

3. **Remove from Progress table:**
   - Delete the row for Experiment {target}

4. **Renumber all subsequent experiments:**
   - `### Experiment 18:` → `### Experiment 17:`
   - `- [ ] **Experiment 18:` → `- [ ] **Experiment 17:`
   - Table rows: `| 18. Dashboard |` → `| 17. Dashboard |`
   - Plan references: `18-01:` → `17-01:`

5. **Update dependency references:**
   - `**Depends on:** Experiment 18` → `**Depends on:** Experiment 17`
   - For the experiment that depended on the removed experiment:
     - `**Depends on:** Experiment 17` (removed) → `**Depends on:** Experiment 16`

6. **Renumber decimal experiments:**
   - `### Experiment 17.1:` → `### Experiment 16.1:` (if integer 17 removed)
   - Update all references consistently

Write updated ROADMAP.md.
</step>

<step name="update_state">
Update STATE.md:

1. **Update total experiment count:**
   - `Experiment: 16 of 20` → `Experiment: 16 of 19`

2. **Recalculate progress percentage:**
   - New percentage based on completed plans / new total plans

Do NOT add a "Roadmap Evolution" note - the git commit is the record.

Write updated STATE.md.
</step>

<step name="update_file_contents">
Search for and update experiment references inside plan files:

```bash
# Find files that reference the old experiment numbers
grep -r "Experiment 18" .planning/experiments/17-*/ 2>/dev/null
grep -r "Experiment 19" .planning/experiments/18-*/ 2>/dev/null
# etc.
```

Update any internal references to reflect new numbering.
</step>

<step name="commit">
Stage and commit the removal:

**Check planning config:**

```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

**If `COMMIT_PLANNING_DOCS=false`:** Skip git operations

**If `COMMIT_PLANNING_DOCS=true` (default):**

```bash
git add .planning/
git commit -m "chore: remove experiment {target} ({original-experiment-name})"
```

The commit message preserves the historical record of what was removed.
</step>

<step name="completion">
Present completion summary:

```
Experiment {target} ({original-name}) removed.

Changes:
- Deleted: .planning/experiments/{target}-{slug}/
- Renumbered: Experiments {first-renumbered}-{last-old} → {first-renumbered-1}-{last-new}
- Updated: ROADMAP.md, STATE.md
- Committed: chore: remove experiment {target} ({original-name})

Current roadmap: {total-remaining} experiments
Current position: Experiment {current} of {new-total}

---

## What's Next

Would you like to:
- `/grd:progress` — see updated roadmap status
- Continue with current experiment
- Review roadmap

---
```
</step>

</process>

<anti_patterns>

- Don't remove completed experiments (have SUMMARY.md files)
- Don't remove current or past experiments
- Don't leave gaps in numbering - always renumber
- Don't add "removed experiment" notes to STATE.md - git commit is the record
- Don't ask about each decimal experiment - just renumber them
- Don't modify completed experiment directories
</anti_patterns>

<edge_cases>

**Removing a decimal experiment (e.g., 17.1):**
- Only affects other decimals in same series (17.2 → 17.1, 17.3 → 17.2)
- Integer experiments unchanged
- Simpler operation

**No subsequent experiments to renumber:**
- Removing the last experiment (e.g., Experiment 20 when that's the end)
- Just delete and update ROADMAP.md, no renumbering needed

**Experiment directory doesn't exist:**
- Experiment may be in STUDY_PROTOCOL.md but directory not created yet
- Skip directory deletion, proceed with ROADMAP.md updates

**Decimal experiments under removed integer:**
- Removing Experiment 17 when 17.1, 17.2 exist
- 17.1 → 16.1, 17.2 → 16.2
- They maintain their position in execution order (after current last integer)

</edge_cases>

<success_criteria>
Experiment removal is complete when:

- [ ] Target experiment validated as future/unstarted
- [ ] Experiment directory deleted (if existed)
- [ ] All subsequent experiment directories renumbered
- [ ] Files inside directories renamed ({old}-01-PLAN.md → {new}-01-PLAN.md)
- [ ] ROADMAP.md updated (section removed, all references renumbered)
- [ ] STATE.md updated (experiment count, progress percentage)
- [ ] Dependency references updated in subsequent experiments
- [ ] Changes committed with descriptive message
- [ ] No gaps in experiment numbering
- [ ] User informed of changes
</success_criteria>
