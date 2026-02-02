---
name: grd:new-study
description: Start a new research study — define hypotheses and create study protocol
argument-hint: "[study name, e.g., 'v1.1 Feature Ablation']"
allowed-tools:
  - Read
  - Write
  - Bash
  - Task
  - AskUserQuestion
---

<objective>
Start a new research study through unified flow: questioning → literature review (optional) → hypotheses → study protocol.

This is the brownfield equivalent of new-project. The project exists, PROJECT.md has history. This command gathers "what's next", updates PROJECT.md, then continues through the full hypotheses → protocol cycle.

**Creates/Updates:**
- `.planning/PROJECT.md` — updated with new study goals
- `.planning/research/` — literature review (optional, focuses on NEW hypotheses)
- `.planning/HYPOTHESES.md` — testable hypotheses with success criteria
- `.planning/STUDY_PROTOCOL.md` — experiment structure with methods and expected outcomes
- `.planning/STATE.md` — reset for new study

**After this command:** Run `/grd:design-experiment [N]` to start experiment execution.
</objective>

<execution_context>
@~/.claude/get-research-done/references/questioning.md
@~/.claude/get-research-done/references/ui-brand.md
@~/.claude/get-research-done/templates/project.md
@~/.claude/get-research-done/templates/hypotheses.md
</execution_context>

<context>
Study name: $ARGUMENTS (optional - will prompt if not provided)

**Load project context:**
@.planning/PROJECT.md
@.planning/STATE.md
@.planning/STUDIES.md
@.planning/config.json

**Load study context (if exists, from /grd:discuss-study):**
@.planning/STUDY-CONTEXT.md
</context>

<process>

## Phase 1: Load Context

- Read PROJECT.md (existing project, validated hypotheses, decisions)
- Read STUDIES.md (what was completed previously)
- Read STATE.md (pending todos, blockers)
- Check for STUDY-CONTEXT.md (from /grd:discuss-study)

## Phase 2: Gather Study Goals

**If STUDY-CONTEXT.md exists:**
- Use hypotheses and scope from discuss-study
- Present summary for confirmation

**If no context file:**
- Present what was completed in last study
- Ask: "What do you want to investigate next?"
- Use AskUserQuestion to explore hypotheses
- Probe for priorities, constraints, scope

## Phase 3: Determine Study Version

- Parse last version from STUDIES.md
- Suggest next version (v1.0 → v1.1, or v2.0 for major)
- Confirm with user

## Phase 4: Update PROJECT.md

Add/update these sections:

```markdown
## Current Study: v[X.Y] [Name]

**Research Question:** [One sentence describing the core question]

**Target Hypotheses:**
- [Hypothesis 1]
- [Hypothesis 2]
- [Hypothesis 3]

**Expected Impact:** [What insights or capabilities this study enables]
```

Update Active Hypotheses section with new goals.

Update "Last updated" footer.

## Phase 5: Update STATE.md

```markdown
## Current Position

Experiment: Not started (defining hypotheses)
Plan: —
Status: Defining hypotheses
Last activity: [today] — Study v[X.Y] started
```

Keep Accumulated Context section (decisions, blockers) from previous study.

## Phase 6: Cleanup and Commit

Delete STUDY-CONTEXT.md if exists (consumed).

Check planning config:
```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

If `COMMIT_PLANNING_DOCS=false`: Skip git operations

If `COMMIT_PLANNING_DOCS=true` (default):
```bash
git add .planning/PROJECT.md .planning/STATE.md
git commit -m "docs: start study v[X.Y] [Name]"
```

## Phase 6.5: Resolve Model Profile

Read model profile for agent spawning:

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Default to "balanced" if not set.

**Model lookup table:**

| Agent | quality | balanced | budget |
|-------|---------|----------|--------|
| grd-project-researcher | opus | sonnet | haiku |
| grd-research-synthesizer | sonnet | sonnet | haiku |
| grd-roadmapper | opus | sonnet | sonnet |

Store resolved models for use in Task calls below.

## Phase 7: Literature Review Decision

Use AskUserQuestion:
- header: "Literature Review"
- question: "Research the domain before defining hypotheses?"
- options:
  - "Research first (Recommended)" — Discover prior work, baseline methods, common pitfalls
  - "Skip research" — I know the literature, go straight to hypotheses

**If "Research first":**

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► LITERATURE REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Researching prior work and baselines...
```

Create research directory:
```bash
mkdir -p .planning/research
```

Display spawning indicator:
```
◆ Spawning 4 researchers in parallel...
  → Methods research (prior approaches)
  → Baselines research (state-of-the-art)
  → Metrics research (evaluation standards)
  → Pitfalls research (common mistakes)
```

Spawn 4 parallel grd-project-researcher agents with study-aware context:

```
Task(prompt="
<research_type>
Study Research — Methods dimension for [research question].
</research_type>

<study_context>
SUBSEQUENT STUDY — Investigating [target hypotheses].

Existing validated findings (DO NOT re-research):
[List from PROJECT.md Validated hypotheses]

Focus ONLY on methods relevant to NEW hypotheses.
</study_context>

<question>
What methods have been used to investigate similar questions?
</question>

<project_context>
[PROJECT.md summary - current state, new study goals]
</project_context>

<downstream_consumer>
Your METHODS.md feeds into hypothesis formulation. Include:
- Prior approaches and their limitations
- Standard experimental designs
- What NOT to do and why
</downstream_consumer>

<quality_gate>
- [ ] Methods are relevant to the research question
- [ ] Limitations of each approach documented
- [ ] Suggested baselines identified
</quality_gate>

<output>
Write to: .planning/research/METHODS.md
</output>
", subagent_type="grd-project-researcher", model="{researcher_model}", description="Methods research")

Task(prompt="
<research_type>
Study Research — Baselines dimension for [research question].
</research_type>

<study_context>
SUBSEQUENT STUDY — Investigating [target hypotheses].

Focus on current state-of-the-art and baseline methods to compare against.
</study_context>

<question>
What are the current baselines and state-of-the-art for this problem?
</question>

<project_context>
[PROJECT.md summary - new study goals]
</project_context>

<downstream_consumer>
Your BASELINES.md feeds into experiment design. Include:
- Baseline methods with expected performance
- State-of-the-art benchmarks
- Minimum bar for meaningful contribution
</downstream_consumer>

<quality_gate>
- [ ] Quantitative benchmarks included where available
- [ ] Baseline implementations referenced
- [ ] Gap between baseline and SOTA characterized
</quality_gate>

<output>
Write to: .planning/research/BASELINES.md
</output>
", subagent_type="grd-project-researcher", model="{researcher_model}", description="Baselines research")

Task(prompt="
<research_type>
Study Research — Metrics dimension for [research question].
</research_type>

<study_context>
SUBSEQUENT STUDY — Investigating [target hypotheses].

Focus on how to measure success and validate findings.
</study_context>

<question>
What metrics and evaluation protocols are standard for this domain?
</question>

<project_context>
[PROJECT.md summary - research question, new hypotheses]
</project_context>

<downstream_consumer>
Your METRICS.md informs success criteria in the study protocol. Include:
- Primary and secondary metrics
- Statistical significance thresholds
- Evaluation datasets/benchmarks
</downstream_consumer>

<quality_gate>
- [ ] Metrics aligned with research question
- [ ] Significance thresholds defined
- [ ] Evaluation protocol reproducible
</quality_gate>

<output>
Write to: .planning/research/METRICS.md
</output>
", subagent_type="grd-project-researcher", model="{researcher_model}", description="Metrics research")

Task(prompt="
<research_type>
Study Research — Pitfalls dimension for [research question].
</research_type>

<study_context>
SUBSEQUENT STUDY — Investigating [target hypotheses].

Focus on common mistakes and confounds in this research area.
</study_context>

<question>
What are common mistakes, confounds, and pitfalls in this research area?
</question>

<project_context>
[PROJECT.md summary - current state, new hypotheses]
</project_context>

<downstream_consumer>
Your PITFALLS.md prevents invalid conclusions. For each pitfall:
- Warning signs (how to detect)
- Prevention strategy (experimental controls)
- Which experiment should address it
</downstream_consumer>

<quality_gate>
- [ ] Pitfalls specific to this research area
- [ ] Data leakage and confounds covered
- [ ] Statistical pitfalls documented
</quality_gate>

<output>
Write to: .planning/research/PITFALLS.md
</output>
", subagent_type="grd-project-researcher", model="{researcher_model}", description="Pitfalls research")
```

After all 4 agents complete, spawn synthesizer to create SUMMARY.md:

```
Task(prompt="
<task>
Synthesize research outputs into SUMMARY.md.
</task>

<research_files>
Read these files:
- .planning/research/METHODS.md
- .planning/research/BASELINES.md
- .planning/research/METRICS.md
- .planning/research/PITFALLS.md
</research_files>

<output>
Write to: .planning/research/SUMMARY.md
Commit after writing.
</output>
", subagent_type="grd-research-synthesizer", model="{synthesizer_model}", description="Synthesize research")
```

Display research complete banner and key findings:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► LITERATURE REVIEW COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Key Findings

**Prior Methods:** [from SUMMARY.md]
**Baseline Performance:** [from SUMMARY.md]
**Key Pitfalls:** [from SUMMARY.md]

Files: `.planning/research/`
```

**If "Skip research":** Continue to Phase 8.

## Phase 8: Define Hypotheses

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► DEFINING HYPOTHESES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Load context:**

Read PROJECT.md and extract:
- Core research question
- Current study goals
- Validated hypotheses (what's already proven)

**If research exists:** Read research/SUMMARY.md and extract insights.

**Present hypotheses by category:**

```
Based on the research question and literature review:

## Primary Hypotheses (must test)
- H1: [Specific, falsifiable claim]
- H2: [Specific, falsifiable claim]

## Secondary Hypotheses (if time permits)
- H3: [Specific, falsifiable claim]

## Baselines to include
- B1: [Baseline method for comparison]

**From literature review:** [relevant insights]

---
```

**If no research:** Gather hypotheses through conversation instead.

Ask: "What specific claims do you want to test?"

For each hypothesis mentioned:
- Ensure it's specific and falsifiable
- Define success criteria
- Identify potential confounds

**Scope hypotheses:**

For each hypothesis, use AskUserQuestion:

- header: "[Hypothesis]"
- question: "Include this hypothesis in the study?"
- options:
  - "Primary" — Must test in this study
  - "Secondary" — Test if time permits
  - "Defer" — Move to future study

Track responses:
- Primary → this study's core experiments
- Secondary → optional experiments
- Deferred → future study

**Generate HYPOTHESES.md:**

Create `.planning/HYPOTHESES.md` with:
- Primary Hypotheses with HYP-IDs (checkboxes)
- Secondary Hypotheses
- Deferred Hypotheses (explicit exclusions)
- Success Criteria for each hypothesis
- Traceability section (empty, filled by protocol)

**HYP-ID format:** `HYP-[NUMBER]` (HYP-01, HYP-02)

**Hypothesis quality criteria:**

Good hypotheses are:
- **Specific and falsifiable:** "Model X outperforms baseline Y by >5% on metric Z" (not "Model X is better")
- **Testable:** Can be validated with available data/resources
- **Independent:** Minimal dependencies on other hypotheses
- **Measurable:** Clear success/failure criteria

**Present full hypotheses list:**

Show every hypothesis for user confirmation:

```
## Study v[X.Y] Hypotheses

### Primary
- [ ] **HYP-01**: [Claim] — Success: [metric threshold]
- [ ] **HYP-02**: [Claim] — Success: [metric threshold]

### Secondary
- [ ] **HYP-03**: [Claim] — Success: [metric threshold]

### Baselines
- **BASELINE-01**: [Method] — Expected: [performance]

---

Does this capture what you're investigating? (yes / adjust)
```

If "adjust": Return to scoping.

**Commit hypotheses:**

Check planning config (same pattern as Phase 6).

If committing:
```bash
git add .planning/HYPOTHESES.md
git commit -m "$(cat <<'EOF'
docs: define study v[X.Y] hypotheses

[X] hypotheses defined ([N] primary, [M] secondary)
EOF
)"
```

## Phase 9: Create Study Protocol

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► CREATING STUDY PROTOCOL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Spawning protocol designer...
```

**Determine starting experiment number:**

Read STUDIES.md to find the last experiment number from previous study.
New experiments continue from there (e.g., if v1.0 ended at experiment 5, v1.1 starts at experiment 6).

Spawn grd-roadmapper agent with context (will create STUDY_PROTOCOL.md):

```
Task(prompt="
<planning_context>

**Project:**
@.planning/PROJECT.md

**Hypotheses:**
@.planning/HYPOTHESES.md

**Research (if exists):**
@.planning/research/SUMMARY.md

**Config:**
@.planning/config.json

**Previous study (for experiment numbering):**
@.planning/STUDIES.md

</planning_context>

<instructions>
Create study protocol for study v[X.Y]:

**IMPORTANT: Create STUDY_PROTOCOL.md NOT ROADMAP.md**

1. Start experiment numbering from [N] (continues from previous study)
2. Derive experiments from THIS STUDY's hypotheses (don't include validated/existing)
3. Map every hypothesis to at least one experiment
4. Define for each experiment:
   - Hypothesis being tested (HYP-ID)
   - Method/approach
   - Expected outcome
   - Success criteria (metrics, thresholds)
   - Controls and baselines
5. Validate 100% coverage of primary hypotheses
6. Write files immediately (STUDY_PROTOCOL.md, STATE.md, update HYPOTHESES.md traceability)
7. Return PROTOCOL CREATED with summary

Write files first, then return. This ensures artifacts persist even if context is lost.

**STUDY_PROTOCOL.md structure:**
```markdown
# Study Protocol: v[X.Y] [Name]

## Research Question
[From PROJECT.md]

## Experiments

### Experiment [N]: [Name]
**Hypothesis:** HYP-[XX]
**Method:** [Approach description]
**Baselines:** [What to compare against]
**Metrics:** [How success is measured]
**Success Criteria:** [Specific thresholds]
**Expected Outcome:** [What we expect to find]
**Controls:** [Confounds being controlled]

### Experiment [N+1]: [Name]
...
```
</instructions>
", subagent_type="grd-roadmapper", model="{roadmapper_model}", description="Create study protocol")
```

**Handle protocol designer return:**

**If `## PROTOCOL BLOCKED`:**
- Present blocker information
- Work with user to resolve
- Re-spawn when resolved

**If `## PROTOCOL CREATED`:**

Read the created STUDY_PROTOCOL.md and present it nicely inline:

```
---

## Proposed Study Protocol

**[N] experiments** | **[X] hypotheses covered** | All primary hypotheses covered ✓

| # | Experiment | Hypothesis | Method | Success Criteria |
|---|------------|------------|--------|------------------|
| [N] | [Name] | HYP-[XX] | [Method] | [criteria] |
| [N+1] | [Name] | HYP-[XX] | [Method] | [criteria] |
...

### Experiment Details

**Experiment [N]: [Name]**
Hypothesis: HYP-[XX]
Method: [approach]
Success criteria: [metrics and thresholds]
Expected outcome: [prediction]

[... continue for all experiments ...]

---
```

**CRITICAL: Ask for approval before committing:**

Use AskUserQuestion:
- header: "Protocol"
- question: "Does this study protocol work for you?"
- options:
  - "Approve" — Commit and continue
  - "Adjust experiments" — Tell me what to change
  - "Review full file" — Show raw STUDY_PROTOCOL.md

**If "Approve":** Continue to commit.

**If "Adjust experiments":**
- Get user's adjustment notes
- Re-spawn with revision context
- Present revised protocol
- Loop until user approves

**If "Review full file":** Display raw `cat .planning/STUDY_PROTOCOL.md`, then re-ask.

**Commit protocol (after approval):**

Check planning config (same pattern as Phase 6).

If committing:
```bash
git add .planning/STUDY_PROTOCOL.md .planning/STATE.md .planning/HYPOTHESES.md
git commit -m "$(cat <<'EOF'
docs: create study v[X.Y] protocol ([N] experiments)

Experiments:
[N]. [experiment-name]: tests HYP-[XX]
[N+1]. [experiment-name]: tests HYP-[XX]
...

All primary hypotheses covered.
EOF
)"
```

## Phase 10: Done

Present completion with next steps:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► STUDY INITIALIZED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Study v[X.Y]: [Name]**

| Artifact         | Location                       |
|------------------|--------------------------------|
| Project          | `.planning/PROJECT.md`         |
| Literature Review| `.planning/research/`          |
| Hypotheses       | `.planning/HYPOTHESES.md`      |
| Study Protocol   | `.planning/STUDY_PROTOCOL.md`  |

**[N] experiments** | **[X] hypotheses** | Ready to run ✓

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Experiment [N]: [Experiment Name]** — [Method from STUDY_PROTOCOL.md]

`/grd:discuss-phase [N]` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/grd:design-experiment [N]` — skip discussion, plan directly

───────────────────────────────────────────────────────────────
```

</process>

<success_criteria>
- [ ] PROJECT.md updated with Current Study section
- [ ] STATE.md reset for new study
- [ ] STUDY-CONTEXT.md consumed and deleted (if existed)
- [ ] Literature review completed (if selected) — 4 parallel agents spawned
- [ ] Hypotheses gathered (from research or conversation)
- [ ] User scoped each hypothesis (primary/secondary/defer)
- [ ] HYPOTHESES.md created with HYP-IDs
- [ ] Protocol designer spawned with experiment numbering context
- [ ] Protocol files written immediately (not draft)
- [ ] User feedback incorporated (if any)
- [ ] STUDY_PROTOCOL.md created with experiments continuing from previous study
- [ ] All commits made (if planning docs committed)
- [ ] User knows next step is `/grd:discuss-phase [N]`

**Atomic commits:** Each phase commits its artifacts immediately. If context is lost, artifacts persist.
</success_criteria>
