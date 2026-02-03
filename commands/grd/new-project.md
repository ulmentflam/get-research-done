---
name: grd:new-project
description: Initialize a new research project with deep context gathering and PROJECT.md
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - AskUserQuestion
---

<objective>

Initialize a new research project through unified flow: questioning → literature review (optional) → hypotheses → study protocol.

This is the most leveraged moment in any project. Deep questioning here means better hypotheses, better experiments, better outcomes. One command takes you from idea to ready-for-experimentation.

**Creates:**
- `.planning/PROJECT.md` — project context and research question
- `.planning/config.json` — workflow preferences
- `.planning/research/` — literature review (optional)
- `.planning/HYPOTHESES.md` — testable hypotheses with success criteria
- `.planning/STUDY_PROTOCOL.md` — experiment structure
- `.planning/STUDIES.md` — study tracking and archive
- `.planning/STATE.md` — project memory

**After this command:** Run `/grd:scope-experiment 1` to start execution.

</objective>

<execution_context>

@~/.claude/get-research-done/references/questioning.md
@~/.claude/get-research-done/references/ui-brand.md
@~/.claude/get-research-done/templates/project.md
@~/.claude/get-research-done/templates/hypotheses.md

</execution_context>

<process>

## Phase 1: Setup

**MANDATORY FIRST STEP — Execute these checks before ANY user interaction:**

1. **Abort if project exists:**
   ```bash
   [ -f .planning/PROJECT.md ] && echo "ERROR: Project already initialized. Use /grd:progress" && exit 1
   ```

2. **Initialize git repo in THIS directory** (required even if inside a parent repo):
   ```bash
   if [ -d .git ] || [ -f .git ]; then
       echo "Git repo exists in current directory"
   else
       git init
       echo "Initialized new git repo"
   fi
   ```

3. **Detect existing code/data (brownfield detection):**
   ```bash
   CODE_FILES=$(find . -name "*.py" -o -name "*.ipynb" -o -name "*.R" -o -name "*.jl" 2>/dev/null | grep -v node_modules | grep -v .git | head -20)
   DATA_FILES=$(find . -name "*.csv" -o -name "*.parquet" -o -name "*.json" -o -name "*.pkl" 2>/dev/null | grep -v node_modules | grep -v .git | head -20)
   HAS_PACKAGE=$([ -f requirements.txt ] || [ -f pyproject.toml ] || [ -f environment.yml ] || [ -f setup.py ] && echo "yes")
   HAS_CODEBASE_MAP=$([ -d .planning/codebase ] && echo "yes")
   ```

4. **Detect existing documentation:**
   ```bash
   DOC_FILES=$(find . -name "*.md" -o -name "*.txt" -o -name "*.pdf" -o -name "*.docx" -o -name "*.tex" 2>/dev/null | grep -v node_modules | grep -v .git | grep -v .planning | head -20)
   README_EXISTS=$([ -f README.md ] || [ -f readme.md ] && echo "yes")
   DOCS_DIR=$([ -d docs ] || [ -d documentation ] || [ -d notes ] && echo "yes")
   ```

   **You MUST run all bash commands above using the Bash tool before proceeding.**

## Phase 2: Brownfield Offer

**If existing code/data detected and .planning/codebase/ doesn't exist:**

Check the results from setup step:
- If `CODE_FILES` is non-empty OR `DATA_FILES` is non-empty OR `HAS_PACKAGE` is "yes"
- AND `HAS_CODEBASE_MAP` is NOT "yes"

Use AskUserQuestion:
- header: "Existing Code"
- question: "I detected existing code/data in this directory. Would you like to map the codebase first?"
- options:
  - "Map codebase first" — Run /grd:map-codebase to understand existing architecture (Recommended)
  - "Skip mapping" — Proceed with project initialization

**If "Map codebase first":**
```
Run `/grd:map-codebase` first, then return to `/grd:new-project`
```
Exit command.

**If "Skip mapping":** Continue to Phase 2.5.

**If no existing code detected OR codebase already mapped:** Continue to Phase 2.5.

## Phase 2.5: Documentation Intake

**Check for existing documentation:**

Check the results from setup step:
- If `DOC_FILES` is non-empty OR `README_EXISTS` is "yes" OR `DOCS_DIR` is "yes"

Use AskUserQuestion:
- header: "Documentation"
- question: "I found existing documentation. Would you like me to use it as context for the project?"
- options:
  - "Yes, read documentation (Recommended)" — I'll extract research context, hypotheses, and constraints
  - "Let me specify files" — I'll tell you which files to read
  - "Skip documentation" — Start fresh, I'll explain everything

**If "Yes, read documentation":**

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► READING DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Read detected documentation files (prioritize README, then docs/, then .pdf files, then other .md/.txt files).

**Supported formats:** Markdown (.md), PDF (.pdf), plain text (.txt), LaTeX (.tex), Word (.docx)

For each document, extract:
- Research questions or objectives
- Hypotheses (stated or implied)
- Methods mentioned
- Data descriptions
- Constraints or requirements
- Prior results or findings

Store extracted context for use in Phase 3 and 4.

Display summary:
```
## Documentation Summary

**Files read:** [count]
**Research context found:**
- [key point 1]
- [key point 2]
- [key point 3]

**Potential hypotheses identified:**
- [hypothesis 1]
- [hypothesis 2]

I'll use this context during questioning.
```

**If "Let me specify files":**

Ask inline: "Which files should I read? (paths or patterns)"

Read specified files and extract context as above.

**If "Skip documentation":** Continue to Phase 3.

**If no documentation detected:** Continue to Phase 3.

## Phase 3: Deep Questioning

**Display stage banner:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► QUESTIONING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Open the conversation:**

**If documentation was loaded in Phase 2.5:**

Present what you learned and ask for confirmation/expansion:

"Based on the documentation, here's what I understand:

**Research focus:** [extracted from docs]
**Key hypotheses:** [extracted from docs]
**Constraints:** [extracted from docs]

Is this accurate? What would you like to add or clarify?"

**If no documentation was loaded:**

Ask inline (freeform, NOT AskUserQuestion):

"What do you want to investigate?"

Wait for their response. This gives you the context needed to ask intelligent follow-up questions.

**Follow the thread:**

Based on what they said, ask follow-up questions that dig into their response. Use AskUserQuestion with options that probe what they mentioned — interpretations, clarifications, concrete examples.

Keep following threads. Each answer opens new threads to explore. Ask about:
- What sparked this research question
- What they hope to learn or prove
- What they mean by vague terms
- What success looks like
- What data/resources are available
- What constraints exist (time, compute, data access)

Consult `questioning.md` for techniques:
- Challenge vagueness
- Make abstract concrete
- Surface assumptions
- Find edges
- Reveal motivation

**Check context (background, not out loud):**

As you go, mentally check the context checklist from `questioning.md`. If gaps remain, weave questions naturally. Don't suddenly switch to checklist mode.

**Gather initial hypotheses:**

When the research question is clear, ask about initial hypotheses:

Use AskUserQuestion:
- header: "Hypotheses"
- question: "Do you have any initial hypotheses you want to test?"
- options:
  - "Yes, I have hypotheses" — Let me share what I expect to find
  - "Not yet" — I want to explore the data / do literature review first
  - "Just a research question" — I'm starting with a question, not predictions

**If "Yes, I have hypotheses":**

Ask inline: "What are your initial hypotheses? (Share as many as you have)"

Collect all hypotheses they provide. For each one:
- Clarify if vague
- Ask about expected evidence
- Note any stated success criteria

**If "Not yet" or "Just a research question":**

That's fine — hypotheses will be defined after literature review in Phase 7. Note this for PROJECT.md.

**Decision gate:**

When you could write a clear PROJECT.md with research question (and any initial hypotheses), use AskUserQuestion:

- header: "Ready?"
- question: "I think I understand what you're investigating. Ready to create PROJECT.md?"
- options:
  - "Create PROJECT.md" — Let's move forward
  - "Keep exploring" — I want to share more / ask me more

If "Keep exploring" — ask what they want to add, or identify gaps and probe naturally.

Loop until "Create PROJECT.md" selected.

## Phase 4: Write PROJECT.md

Synthesize all context into `.planning/PROJECT.md` using the template from `templates/project.md`.

**Research-focused structure:**

```markdown
# [Project Name]

## Research Question

[The core question this project investigates — clear, specific, answerable]

## What This Is

[One paragraph describing the research project]

## Core Value

[The ONE insight or capability that makes this research worthwhile]

## Hypotheses

### Validated

(None yet — experiments validate)

### Active

[If user provided initial hypotheses during questioning:]
- [ ] [Initial hypothesis 1]
- [ ] [Initial hypothesis 2]
- [ ] [... as many as provided]

[If user has no initial hypotheses:]
(To be defined after literature review)

### Out of Scope

- [Exclusion 1] — [why]
- [Exclusion 2] — [why]

## Context & Constraints

- **Data:** [what's available, what's needed]
- **Compute:** [resources available]
- **Timeline:** [any deadlines]
- **Prior work:** [relevant background]

## Current Study: v1.0 [Study Name]

**Research Question:** [One sentence core question]

**Target Hypotheses:**
- [Primary hypothesis 1]
- [Primary hypothesis 2]
- [... from Active hypotheses above]

**Expected Impact:** [What insights or capabilities this study enables]

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| [Choice from questioning] | [Why] | — Pending |
```

**For brownfield projects (codebase map exists):**

Infer Validated hypotheses from existing work:

1. Read `.planning/codebase/ARCHITECTURE.md` if exists
2. Identify what the codebase already demonstrates
3. These become the initial Validated set

**Last updated footer:**

```markdown
---
*Last updated: [date] after initialization*
```

Do not compress. Capture everything gathered.

**Commit PROJECT.md:**

```bash
mkdir -p .planning
git add .planning/PROJECT.md
git commit -m "$(cat <<'EOF'
docs: initialize research project

[One-liner research question from PROJECT.md]
EOF
)"
```

## Phase 5: Workflow Preferences

**Round 1 — Core workflow settings (4 questions):**

```
questions: [
  {
    header: "Mode",
    question: "How do you want to work?",
    multiSelect: false,
    options: [
      { label: "YOLO (Recommended)", description: "Auto-approve, just execute" },
      { label: "Interactive", description: "Confirm at each step" }
    ]
  },
  {
    header: "Depth",
    question: "How thorough should the study be?",
    multiSelect: false,
    options: [
      { label: "Quick", description: "Ship fast (3-5 experiments, 1-3 plans each)" },
      { label: "Standard", description: "Balanced scope and rigor (5-8 experiments, 3-5 plans each)" },
      { label: "Comprehensive", description: "Thorough coverage (8-12 experiments, 5-10 plans each)" }
    ]
  },
  {
    header: "Execution",
    question: "Run plans in parallel?",
    multiSelect: false,
    options: [
      { label: "Parallel (Recommended)", description: "Independent plans run simultaneously" },
      { label: "Sequential", description: "One plan at a time" }
    ]
  },
  {
    header: "Git Tracking",
    question: "Commit planning docs to git?",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Planning docs tracked in version control" },
      { label: "No", description: "Keep .planning/ local-only (add to .gitignore)" }
    ]
  }
]
```

**Round 2 — Workflow agents:**

These spawn additional agents during planning/execution. They add tokens and time but improve quality.

| Agent | When it runs | What it does |
|-------|--------------|--------------|
| **Researcher** | Before planning each experiment | Investigates methods, finds baselines, surfaces pitfalls |
| **Plan Checker** | After plan is created | Verifies plan actually tests the hypothesis |
| **Verifier** | After experiment execution | Confirms success criteria were met |

All recommended for important research. Skip for quick experiments.

```
questions: [
  {
    header: "Research",
    question: "Research before planning each experiment? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Investigate methods, find baselines, surface pitfalls" },
      { label: "No", description: "Plan directly from hypotheses" }
    ]
  },
  {
    header: "Plan Check",
    question: "Verify plans will test their hypotheses? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Catch gaps before execution starts" },
      { label: "No", description: "Execute plans without verification" }
    ]
  },
  {
    header: "Verifier",
    question: "Verify results satisfy success criteria after each experiment? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Confirm hypotheses actually tested" },
      { label: "No", description: "Trust execution, skip verification" }
    ]
  },
  {
    header: "Model Profile",
    question: "Which AI models for planning agents?",
    multiSelect: false,
    options: [
      { label: "Balanced (Recommended)", description: "Sonnet for most agents — good quality/cost ratio" },
      { label: "Quality", description: "Opus for research/protocol — higher cost, deeper analysis" },
      { label: "Budget", description: "Haiku where possible — fastest, lowest cost" }
    ]
  }
]
```

Create `.planning/config.json` with all settings:

```json
{
  "mode": "yolo|interactive",
  "depth": "quick|standard|comprehensive",
  "parallelization": true|false,
  "commit_docs": true|false,
  "model_profile": "quality|balanced|budget",
  "workflow": {
    "research": true|false,
    "plan_check": true|false,
    "verifier": true|false
  }
}
```

**If commit_docs = No:**
- Set `commit_docs: false` in config.json
- Add `.planning/` to `.gitignore` (create if needed)

**If commit_docs = Yes:**
- No additional gitignore entries needed

**Commit config.json:**

```bash
git add .planning/config.json
git commit -m "$(cat <<'EOF'
chore: add project config

Mode: [chosen mode]
Depth: [chosen depth]
Parallelization: [enabled/disabled]
Workflow agents: research=[on/off], plan_check=[on/off], verifier=[on/off]
EOF
)"
```

**Note:** Run `/grd:settings` anytime to update these preferences.

## Phase 5.5: Resolve Model Profile

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

## Phase 6: Literature Review Decision

Use AskUserQuestion:
- header: "Literature Review"
- question: "Research the domain before defining hypotheses?"
- options:
  - "Research first (Recommended)" — Discover prior methods, baselines, evaluation standards
  - "Skip research" — I know this domain well, go straight to hypotheses

**If "Research first":**

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► LITERATURE REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Researching [research question] domain...
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

Spawn 4 parallel grd-project-researcher agents with research-focused context:

```
Task(prompt="First, read ~/.claude/agents/grd-project-researcher.md for your role and instructions.

<research_type>
Study Research — Methods dimension for [research question].
</research_type>

<question>
What methods have been used to investigate similar questions? What are standard experimental designs?
</question>

<project_context>
[PROJECT.md summary - research question, constraints, what they're investigating]
</project_context>

<downstream_consumer>
Your METHODS.md feeds into hypothesis formulation and experiment design. Be prescriptive:
- Prior approaches with their limitations
- Standard experimental designs for this domain
- What NOT to do and why
</downstream_consumer>

<quality_gate>
- [ ] Methods are relevant to the research question
- [ ] Limitations of each approach documented
- [ ] Suggested baselines identified
</quality_gate>

<output>
Write to: .planning/research/METHODS.md
Use template: ~/.claude/get-research-done/templates/research-study/METHODS.md
</output>
", subagent_type="general-purpose", model="{researcher_model}", description="Methods research")

Task(prompt="First, read ~/.claude/agents/grd-project-researcher.md for your role and instructions.

<research_type>
Study Research — Baselines dimension for [research question].
</research_type>

<question>
What are the current baselines and state-of-the-art for this problem? What performance should we expect?
</question>

<project_context>
[PROJECT.md summary]
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
Use template: ~/.claude/get-research-done/templates/research-study/BASELINES.md
</output>
", subagent_type="general-purpose", model="{researcher_model}", description="Baselines research")

Task(prompt="First, read ~/.claude/agents/grd-project-researcher.md for your role and instructions.

<research_type>
Study Research — Metrics dimension for [research question].
</research_type>

<question>
What metrics and evaluation protocols are standard for this domain? What statistical tests are appropriate?
</question>

<project_context>
[PROJECT.md summary]
</project_context>

<downstream_consumer>
Your METRICS.md informs success criteria in the study protocol. Include:
- Primary and secondary metrics
- Statistical significance thresholds
- Evaluation datasets/benchmarks
- Standard evaluation protocols
</downstream_consumer>

<quality_gate>
- [ ] Metrics aligned with research question
- [ ] Significance thresholds defined
- [ ] Evaluation protocol reproducible
</quality_gate>

<output>
Write to: .planning/research/METRICS.md
Use template: ~/.claude/get-research-done/templates/research-study/METRICS.md
</output>
", subagent_type="general-purpose", model="{researcher_model}", description="Metrics research")

Task(prompt="First, read ~/.claude/agents/grd-project-researcher.md for your role and instructions.

<research_type>
Study Research — Pitfalls dimension for [research question].
</research_type>

<question>
What do researchers commonly get wrong in this area? What are the critical mistakes and confounds?
</question>

<project_context>
[PROJECT.md summary]
</project_context>

<downstream_consumer>
Your PITFALLS.md prevents invalid conclusions. For each pitfall:
- Warning signs (how to detect early)
- Prevention strategy (how to avoid)
- Which experiment should address it
</downstream_consumer>

<quality_gate>
- [ ] Pitfalls are specific to this research area (not generic advice)
- [ ] Data leakage and confounds covered
- [ ] Statistical pitfalls documented
- [ ] Prevention strategies are actionable
</quality_gate>

<output>
Write to: .planning/research/PITFALLS.md
Use template: ~/.claude/get-research-done/templates/research-study/PITFALLS.md
</output>
", subagent_type="general-purpose", model="{researcher_model}", description="Pitfalls research")
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
Use template: ~/.claude/get-research-done/templates/research-study/SUMMARY.md
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

**Methods:** [from SUMMARY.md]
**Baselines:** [from SUMMARY.md]
**Key Pitfalls:** [from SUMMARY.md]

Files: `.planning/research/`
```

**If "Skip research":** Continue to Phase 7.

## Phase 7: Define Hypotheses

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► DEFINING HYPOTHESES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Load context:**

Read PROJECT.md and extract:
- Research question
- Initial hypotheses from questioning (if any were provided)
- Any explicit scope boundaries

**If research exists:** Read research/SUMMARY.md and extract insights.

**Handle based on initial hypotheses state:**

**Case A: User provided initial hypotheses in Phase 3:**

Present and refine them:

```
You mentioned these initial hypotheses:

- **H1:** [User's hypothesis 1]
- **H2:** [User's hypothesis 2]
- [... all provided hypotheses]

Based on the literature review, I'd suggest:
- Refining H1 to: [more specific version with metrics]
- Adding baseline: [suggested from research]
- Watch out for: [pitfall from research]

Let's refine these and add any new ones.
```

**Case B: User had no initial hypotheses:**

Generate hypotheses from research and research question:

```
Based on the research question and literature review, here are suggested hypotheses:

## Suggested Primary Hypotheses

- **H1:** [Derived from research question + methods research]
  - Success: [metric from METRICS.md]
  - Method: [from METHODS.md]

- **H2:** [Another testable claim]
  - Success: [metric threshold]
  - Method: [suggested approach]

## Suggested Secondary Hypotheses

- **H3:** [Lower priority investigation]
  - Success: [metric threshold]

## Recommended Baselines

- **B1:** [From BASELINES.md] — Expected: [performance]
- **B2:** [From BASELINES.md] — Expected: [performance]

**Key insights from literature:** [from SUMMARY.md]

---

Do these capture what you want to investigate? You can accept, modify, add, or remove any.
```

**Case C: No initial hypotheses AND no research:**

Gather hypotheses through conversation:

Ask: "Based on your research question, what specific claims do you want to test? What do you expect to find?"

For each hypothesis mentioned:
- Ensure it's specific and falsifiable
- Define success criteria
- Identify potential confounds

If user struggles, help them derive hypotheses:
- "If [research question], what would prove it true?"
- "What would you need to see in the data to be convinced?"
- "What's the simplest claim we could test first?"

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

**Hypothesis quality criteria:**

Good hypotheses are:
- **Specific and falsifiable:** "Model X outperforms baseline Y by >5% on metric Z" (not "Model X is better")
- **Testable:** Can be validated with available data/resources
- **Independent:** Minimal dependencies on other hypotheses
- **Measurable:** Clear success/failure criteria

Reject vague hypotheses. Push for specificity:
- "Deep learning works better" → "LSTM outperforms logistic regression by >10% F1 on dataset X"
- "The model is robust" → "Model maintains >90% accuracy when input noise σ < 0.1"

**Generate HYPOTHESES.md:**

Create `.planning/HYPOTHESES.md` with:
- Primary Hypotheses with HYP-IDs (checkboxes)
- Secondary Hypotheses
- Deferred Hypotheses (explicit exclusions)
- Baselines with expected performance
- Success Criteria for each hypothesis
- Traceability section (empty, filled by protocol)

**HYP-ID format:** `HYP-[NUMBER]` (HYP-01, HYP-02)

**Present full hypotheses list:**

Show every hypothesis for user confirmation:

```
## Study v1.0 Hypotheses

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

```bash
git add .planning/HYPOTHESES.md
git commit -m "$(cat <<'EOF'
docs: define study v1.0 hypotheses

[X] hypotheses defined ([N] primary, [M] secondary)
EOF
)"
```

## Phase 8: Create Study Protocol

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► CREATING STUDY PROTOCOL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Spawning protocol designer...
```

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

</planning_context>

<instructions>
Create study protocol for v1.0:

**IMPORTANT: Create STUDY_PROTOCOL.md NOT ROADMAP.md**

1. Start experiment numbering from 1
2. Derive experiments from hypotheses (one experiment per primary hypothesis, generally)
3. Map every primary hypothesis to at least one experiment
4. Define for each experiment:
   - Hypothesis being tested (HYP-ID)
   - Method/approach
   - Expected outcome
   - Success criteria (metrics, thresholds)
   - Controls and baselines
5. Validate 100% coverage of primary hypotheses
6. Write files immediately (STUDY_PROTOCOL.md, STUDIES.md, STATE.md, update HYPOTHESES.md traceability)
7. Return PROTOCOL CREATED with summary

Write files first, then return. This ensures artifacts persist even if context is lost.

**STUDY_PROTOCOL.md structure:**
```markdown
# Study Protocol: v1.0 [Name]

## Research Question
[From PROJECT.md]

## Experiments

### Experiment 1: [Name]
**Hypothesis:** HYP-01
**Method:** [Approach description]
**Baselines:** [What to compare against]
**Metrics:** [How success is measured]
**Success Criteria:** [Specific thresholds]
**Expected Outcome:** [What we expect to find]
**Controls:** [Confounds being controlled]

### Experiment 2: [Name]
...
```

**STUDIES.md structure:**
```markdown
# Studies Archive

**Project:** [Name]
**Current Study:** v1.0 [Name]
**Total Experiments:** [count]

## Active Study

**v1.0: [Name]**
- Status: In Progress
- Experiments: 1 to [N]
- Hypotheses: [count] primary, [count] secondary
- Started: [date]

See: `STUDY_PROTOCOL.md`, `HYPOTHESES.md`

---

## Completed Studies

(None yet)

---

## Experiment Index

| # | Name | Study | Hypothesis | Result |
|---|------|-------|------------|--------|
| 1 | [name] | v1.0 | HYP-01 | Pending |
| 2 | [name] | v1.0 | HYP-02 | Pending |
```

**STATE.md structure:**
```markdown
# Project State

## Project Reference

See: .planning/PROJECT.md (updated [date])

**Core value:** [One-liner from PROJECT.md]
**Current focus:** Experiment 1

## Current Position

Experiment: 1 of [N] ([Experiment 1 name])
Plan: Not started
Status: Ready to plan
Last activity: [date] — Study v1.0 initialized

Progress: [░░░░░░░░░░] 0%

## Accumulated Context

### Decisions

None yet.

### Pending Todos

None yet.

### Blockers/Concerns

None yet.

## Session Continuity

Last session: [date]
Stopped at: Project initialized
Resume file: None
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
| 1 | [Name] | HYP-01 | [Method] | [criteria] |
| 2 | [Name] | HYP-02 | [Method] | [criteria] |
...

### Experiment Details

**Experiment 1: [Name]**
Hypothesis: HYP-01
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
- Re-spawn with revision context:
  ```
  Task(prompt="
  <revision>
  User feedback on protocol:
  [user's notes]

  Current STUDY_PROTOCOL.md: @.planning/STUDY_PROTOCOL.md

  Update the protocol based on feedback. Edit files in place.
  Return PROTOCOL REVISED with changes made.
  </revision>
  ", subagent_type="grd-roadmapper", model="{roadmapper_model}", description="Revise protocol")
  ```
- Present revised protocol
- Loop until user approves

**If "Review full file":** Display raw `cat .planning/STUDY_PROTOCOL.md`, then re-ask.

**Commit protocol (after approval):**

```bash
git add .planning/STUDY_PROTOCOL.md .planning/STUDIES.md .planning/STATE.md .planning/HYPOTHESES.md
git commit -m "$(cat <<'EOF'
docs: create study v1.0 protocol ([N] experiments)

Experiments:
1. [experiment-name]: tests HYP-01
2. [experiment-name]: tests HYP-02
...

All primary hypotheses covered.
EOF
)"
```

## Phase 10: Done

Present completion with next steps:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GRD ► PROJECT INITIALIZED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**[Project Name]**

| Artifact         | Location                       |
|------------------|--------------------------------|
| Project          | `.planning/PROJECT.md`         |
| Config           | `.planning/config.json`        |
| Literature Review| `.planning/research/`          |
| Hypotheses       | `.planning/HYPOTHESES.md`      |
| Study Protocol   | `.planning/STUDY_PROTOCOL.md`  |
| Studies Archive  | `.planning/STUDIES.md`         |

**[N] experiments** | **[X] hypotheses** | Ready to run ✓

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Experiment 1: [Experiment Name]** — [Method from STUDY_PROTOCOL.md]

`/grd:scope-experiment 1` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/grd:design-experiment 1` — skip discussion, plan directly

───────────────────────────────────────────────────────────────
```

</process>

<output>

- `.planning/PROJECT.md`
- `.planning/config.json`
- `.planning/research/` (if research selected)
  - `METHODS.md`
  - `BASELINES.md`
  - `METRICS.md`
  - `PITFALLS.md`
  - `SUMMARY.md`
- `.planning/HYPOTHESES.md`
- `.planning/STUDY_PROTOCOL.md`
- `.planning/STUDIES.md`
- `.planning/STATE.md`

</output>

<success_criteria>

- [ ] .planning/ directory created
- [ ] Git repo initialized
- [ ] Brownfield detection completed
- [ ] Deep questioning completed (threads followed, not rushed)
- [ ] PROJECT.md captures research question and context → **committed**
- [ ] config.json has workflow mode, depth, parallelization → **committed**
- [ ] Literature review completed (if selected) — 4 parallel agents spawned → **committed**
- [ ] Hypotheses gathered (from research or conversation)
- [ ] User scoped each hypothesis (primary/secondary/defer)
- [ ] HYPOTHESES.md created with HYP-IDs → **committed**
- [ ] grd-roadmapper spawned with context
- [ ] Protocol files written immediately (not draft)
- [ ] User feedback incorporated (if any)
- [ ] STUDY_PROTOCOL.md created with experiments and hypothesis mappings
- [ ] STUDIES.md initialized for study tracking
- [ ] STATE.md initialized
- [ ] HYPOTHESES.md traceability updated
- [ ] User knows next step is `/grd:scope-experiment 1`

**Atomic commits:** Each phase commits its artifacts immediately. If context is lost, artifacts persist.

</success_criteria>
