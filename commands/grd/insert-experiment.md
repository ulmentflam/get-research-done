---
name: grd:insert-experiment
description: Insert urgent work as decimal experiment (e.g., 72.1) between existing experiments
argument-hint: <after> <description>
allowed-tools:
  - Read
  - Write
  - Bash
---

<objective>
Insert a decimal experiment for urgent work discovered mid-study that must be completed between existing integer experiments.

Uses decimal numbering (72.1, 72.2, etc.) to preserve the logical sequence of planned experiments while accommodating urgent insertions.

Purpose: Handle urgent work discovered during execution without renumbering entire roadmap.
</objective>

<execution_context>
@.planning/ROADMAP.md
@.planning/STATE.md
</execution_context>

<process>

<step name="parse_arguments">
Parse the command arguments:
- First argument: integer experiment number to insert after
- Remaining arguments: experiment description

Example: `/grd:insert-experiment 72 Fix critical auth bug`
→ after = 72
→ description = "Fix critical auth bug"

Validation:

```bash
if [ $# -lt 2 ]; then
  echo "ERROR: Both experiment number and description required"
  echo "Usage: /grd:insert-experiment <after> <description>"
  echo "Example: /grd:insert-experiment 72 Fix critical auth bug"
  exit 1
fi
```

Parse first argument as integer:

```bash
after_phase=$1
shift
description="$*"

# Validate after_phase is an integer
if ! [[ "$after_phase" =~ ^[0-9]+$ ]]; then
  echo "ERROR: Experiment number must be an integer"
  exit 1
fi
```

</step>

<step name="load_roadmap">
Load the roadmap file:

```bash
if [ -f .planning/ROADMAP.md ]; then
  ROADMAP=".planning/ROADMAP.md"
else
  echo "ERROR: No roadmap found (.planning/ROADMAP.md)"
  exit 1
fi
```

Read roadmap content for parsing.
</step>

<step name="verify_target_phase">
Verify that the target experiment exists in the roadmap:

1. Search for "### Experiment {after_phase}:" heading
2. If not found:

   ```
   ERROR: Experiment {after_phase} not found in roadmap
   Available experiments: [list experiment numbers]
   ```

   Exit.

3. Verify experiment is in current study (not completed/archived)
   </step>

<step name="find_existing_decimals">
Find existing decimal experiments after the target experiment:

1. Search for all "### Experiment {after_phase}.N:" headings
2. Extract decimal suffixes (e.g., for Experiment 72: find 72.1, 72.2, 72.3)
3. Find the highest decimal suffix
4. Calculate next decimal: max + 1

Examples:

- Experiment 72 with no decimals → next is 72.1
- Experiment 72 with 72.1 → next is 72.2
- Experiment 72 with 72.1, 72.2 → next is 72.3

Store as: `decimal_phase="$(printf "%02d" $after_phase).${next_decimal}"`
</step>

<step name="generate_slug">
Convert the experiment description to a kebab-case slug:

```bash
slug=$(echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
```

Experiment directory name: `{decimal-experiment}-{slug}`
Example: `06.1-fix-critical-auth-bug` (experiment 6 insertion)
</step>

<step name="create_phase_directory">
Create the experiment directory structure:

```bash
phase_dir=".planning/experiments/${decimal_phase}-${slug}"
mkdir -p "$phase_dir"
```

Confirm: "Created directory: $phase_dir"
</step>

<step name="update_roadmap">
Insert the new experiment entry into the roadmap:

1. Find insertion point: immediately after Experiment {after_phase}'s content (before next experiment heading or "---")
2. Insert new experiment heading with (INSERTED) marker:

   ```
   ### Experiment {decimal_phase}: {Description} (INSERTED)

   **Goal:** [Urgent work - to be planned]
   **Depends on:** Experiment {after_phase}
   **Plans:** 0 plans

   Plans:
   - [ ] TBD (run /grd:design-experiment {decimal_phase} to break down)

   **Details:**
   [To be added during planning]
   ```

3. Write updated roadmap back to file

The "(INSERTED)" marker helps identify decimal experiments as urgent insertions.

Preserve all other content exactly (formatting, spacing, other experiments).
</step>

<step name="update_project_state">
Update STATE.md to reflect the inserted experiment:

1. Read `.planning/STATE.md`
2. Under "## Accumulated Context" → "### Roadmap Evolution" add entry:
   ```
   - Experiment {decimal_phase} inserted after Experiment {after_phase}: {description} (URGENT)
   ```

If "Roadmap Evolution" section doesn't exist, create it.

Add note about insertion reason if appropriate.
</step>

<step name="completion">
Present completion summary:

```
Experiment {decimal_phase} inserted after Experiment {after_phase}:
- Description: {description}
- Directory: .planning/experiments/{decimal-experiment}-{slug}/
- Status: Not planned yet
- Marker: (INSERTED) - indicates urgent work

Roadmap updated: {roadmap-path}
Project state updated: .planning/STATE.md

---

## ▶ Next Up

**Experiment {decimal_phase}: {description}** — urgent insertion

`/grd:design-experiment {decimal_phase}`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- Review insertion impact: Check if Experiment {next_integer} dependencies still make sense
- Review roadmap

---
```
</step>

</process>

<anti_patterns>

- Don't use this for planned work at end of study (use /grd:add-experiment)
- Don't insert before Experiment 1 (decimal 0.1 makes no sense)
- Don't renumber existing experiments
- Don't modify the target experiment content
- Don't create plans yet (that's /grd:design-experiment)
- Don't commit changes (user decides when to commit)
  </anti_patterns>

<success_criteria>
Experiment insertion is complete when:

- [ ] Experiment directory created: `.planning/experiments/{N.M}-{slug}/`
- [ ] Roadmap updated with new experiment entry (includes "(INSERTED)" marker)
- [ ] Experiment inserted in correct position (after target experiment, before next integer experiment)
- [ ] STATE.md updated with roadmap evolution note
- [ ] Decimal number calculated correctly (based on existing decimals)
- [ ] User informed of next steps and dependency implications
      </success_criteria>
