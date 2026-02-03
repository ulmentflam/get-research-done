---
name: grd:add-experiment
description: Add experiment to end of current study in roadmap
argument-hint: <description>
allowed-tools:
  - Read
  - Write
  - Bash
---

<objective>
Add a new integer experiment to the end of the current study in the roadmap.

This command appends sequential experiments to the current study's experiment list, automatically calculating the next experiment number based on existing experiments.

Purpose: Add planned work discovered during execution that belongs at the end of current study.
</objective>

<execution_context>
@.planning/ROADMAP.md
@.planning/STATE.md
</execution_context>

<process>

<step name="parse_arguments">
Parse the command arguments:
- All arguments become the experiment description
- Example: `/grd:add-experiment Add authentication` → description = "Add authentication"
- Example: `/grd:add-experiment Fix critical performance issues` → description = "Fix critical performance issues"

If no arguments provided:

```
ERROR: Experiment description required
Usage: /grd:add-experiment <description>
Example: /grd:add-experiment Add authentication system
```

Exit.
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

<step name="find_current_milestone">
Parse the roadmap to find the current study section:

1. Locate the "## Current Study:" heading
2. Extract study name and version
3. Identify all experiments under this study (before next "---" separator or next study heading)
4. Parse existing experiment numbers (including decimals if present)

Example structure:

```
## Current Study: v1.0 Foundation

### Experiment 4: Focused Command System
### Experiment 5: Path Routing & Validation
### Experiment 6: Documentation & Distribution
```

</step>

<step name="calculate_next_phase">
Find the highest integer experiment number in the current study:

1. Extract all experiment numbers from experiment headings (### Experiment N:)
2. Filter to integer phases only (ignore decimals like 4.1, 4.2)
3. Find the maximum integer value
4. Add 1 to get the next experiment number

Example: If phases are 4, 5, 5.1, 6 → next is 7

Format as two-digit: `printf "%02d" $next_phase`
</step>

<step name="generate_slug">
Convert the experiment description to a kebab-case slug:

```bash
# Example transformation:
# "Add authentication" → "add-authentication"
# "Fix critical performance issues" → "fix-critical-performance-issues"

slug=$(echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
```

Experiment directory name: `{two-digit-exp}-{slug}`
Example: `07-add-authentication`
</step>

<step name="create_exp_directory">
Create the experiment directory structure:

```bash
exp_dir=".planning/experiments/${exp_num}-${slug}"
mkdir -p "$exp_dir"
```

Confirm: "Created directory: $exp_dir"
</step>

<step name="update_roadmap">
Add the new experiment entry to the roadmap:

1. Find the insertion point (after last experiment in current study, before "---" separator)
2. Insert new experiment heading:

   ```
   ### Experiment {N}: {Description}

   **Goal:** [To be planned]
   **Depends on:** Experiment {N-1}
   **Plans:** 0 plans

   Plans:
   - [ ] TBD (run /grd:design-experiment {N} to break down)

   **Details:**
   [To be added during planning]
   ```

3. Write updated roadmap back to file

Preserve all other content exactly (formatting, spacing, other phases).
</step>

<step name="update_project_state">
Update STATE.md to reflect the new experiment:

1. Read `.planning/STATE.md`
2. Under "## Current Position" → "**Next Experiment:**" add reference to new experiment
3. Under "## Accumulated Context" → "### Roadmap Evolution" add entry:
   ```
   - Experiment {N} added: {description}
   ```

If "Roadmap Evolution" section doesn't exist, create it.
</step>

<step name="completion">
Present completion summary:

```
Experiment {N} added to current study:
- Description: {description}
- Directory: .planning/experiments/{exp-num}-{slug}/
- Status: Not planned yet

Roadmap updated: {roadmap-path}
Project state updated: .planning/STATE.md

---

## ▶ Next Up

**Experiment {N}: {description}**

`/grd:design-experiment {N}`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/grd:add-experiment <description>` — add another experiment
- Review roadmap

---
```
</step>

</process>

<anti_patterns>

- Don't modify phases outside current study
- Don't renumber existing phases
- Don't use decimal numbering (that's /grd:insert-experiment)
- Don't create plans yet (that's /grd:design-experiment)
- Don't commit changes (user decides when to commit)
  </anti_patterns>

<success_criteria>
Experiment addition is complete when:

- [ ] Experiment directory created: `.planning/experiments/{NN}-{slug}/`
- [ ] Roadmap updated with new experiment entry
- [ ] STATE.md updated with roadmap evolution note
- [ ] New experiment appears at end of current study
- [ ] Next experiment number calculated correctly (ignoring decimals)
- [ ] User informed of next steps
      </success_criteria>
