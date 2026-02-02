# Roadmap Template

Template for `.planning/ROADMAP.md`.

## Initial Roadmap (v1.0 Greenfield)

```markdown
# Roadmap: [Project Name]

## Overview

[One paragraph describing the journey from start to finish]

## Experiments

**Experiment Numbering:**
- Integer experiments (1, 2, 3): Planned study work
- Decimal experiments (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal experiments appear between their surrounding integers in numeric order.

- [ ] **Experiment 1: [Name]** - [One-line description]
- [ ] **Experiment 2: [Name]** - [One-line description]
- [ ] **Experiment 3: [Name]** - [One-line description]
- [ ] **Experiment 4: [Name]** - [One-line description]

## Experiment Details

### Experiment 1: [Name]
**Goal**: [What this experiment delivers]
**Depends on**: Nothing (first experiment)
**Requirements**: [REQ-01, REQ-02, REQ-03]
**Success Criteria** (what must be TRUE):
  1. [Observable behavior from user perspective]
  2. [Observable behavior from user perspective]
  3. [Observable behavior from user perspective]
**Plans**: [Number of plans, e.g., "3 plans" or "TBD"]

Plans:
- [ ] 01-01: [Brief description of first plan]
- [ ] 01-02: [Brief description of second plan]
- [ ] 01-03: [Brief description of third plan]

### Experiment 2: [Name]
**Goal**: [What this experiment delivers]
**Depends on**: Experiment 1
**Requirements**: [REQ-04, REQ-05]
**Success Criteria** (what must be TRUE):
  1. [Observable behavior from user perspective]
  2. [Observable behavior from user perspective]
**Plans**: [Number of plans]

Plans:
- [ ] 02-01: [Brief description]
- [ ] 02-02: [Brief description]

### Experiment 2.1: Critical Fix (INSERTED)
**Goal**: [Urgent work inserted between experiments]
**Depends on**: Experiment 2
**Success Criteria** (what must be TRUE):
  1. [What the fix achieves]
**Plans**: 1 plan

Plans:
- [ ] 02.1-01: [Description]

### Experiment 3: [Name]
**Goal**: [What this experiment delivers]
**Depends on**: Experiment 2
**Requirements**: [REQ-06, REQ-07, REQ-08]
**Success Criteria** (what must be TRUE):
  1. [Observable behavior from user perspective]
  2. [Observable behavior from user perspective]
  3. [Observable behavior from user perspective]
**Plans**: [Number of plans]

Plans:
- [ ] 03-01: [Brief description]
- [ ] 03-02: [Brief description]

### Experiment 4: [Name]
**Goal**: [What this experiment delivers]
**Depends on**: Experiment 3
**Requirements**: [REQ-09, REQ-10]
**Success Criteria** (what must be TRUE):
  1. [Observable behavior from user perspective]
  2. [Observable behavior from user perspective]
**Plans**: [Number of plans]

Plans:
- [ ] 04-01: [Brief description]

## Progress

**Execution Order:**
Experiments execute in numeric order: 2 → 2.1 → 2.2 → 3 → 3.1 → 4

| Experiment | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. [Name] | 0/3 | Not started | - |
| 2. [Name] | 0/2 | Not started | - |
| 3. [Name] | 0/2 | Not started | - |
| 4. [Name] | 0/1 | Not started | - |
```

<guidelines>
**Initial planning (v1.0):**
- Experiment count depends on depth setting (quick: 3-5, standard: 5-8, comprehensive: 8-12)
- Each experiment delivers something coherent
- Experiments can have 1+ plans (split if >3 tasks or multiple subsystems)
- Plans use naming: {phase}-{plan}-PLAN.md (e.g., 01-02-PLAN.md)
- No time estimates (this isn't enterprise PM)
- Progress table updated by execute workflow
- Plan count can be "TBD" initially, refined during planning

**Success criteria:**
- 2-5 observable behaviors per experiment (from user's perspective)
- Cross-checked against requirements during roadmap creation
- Flow downstream to `must_haves` in design-experiment
- Verified by validate-results after execution
- Format: "User can [action]" or "[Thing] works/exists"

**After studies ship:**
- Collapse completed studies in `<details>` tags
- Add new study sections for upcoming work
- Keep continuous experiment numbering (never restart at 01)
</guidelines>

<status_values>
- `Not started` - Haven't begun
- `In progress` - Currently working
- `Complete` - Done (add completion date)
- `Deferred` - Pushed to later (with reason)
</status_values>

## Study-Grouped Roadmap (After v1.0 Ships)

After completing first study, reorganize with study groupings:

```markdown
# Roadmap: [Project Name]

## Studies

- ✅ **v1.0 MVP** - Experiments 1-4 (shipped YYYY-MM-DD)
- 🚧 **v1.1 [Name]** - Experiments 5-6 (in progress)
- 📋 **v2.0 [Name]** - Experiments 7-10 (planned)

## Experiments

<details>
<summary>✅ v1.0 MVP (Experiments 1-4) - SHIPPED YYYY-MM-DD</summary>

### Experiment 1: [Name]
**Goal**: [What this experiment delivers]
**Plans**: 3 plans

Plans:
- [x] 01-01: [Brief description]
- [x] 01-02: [Brief description]
- [x] 01-03: [Brief description]

[... remaining v1.0 experiments ...]

</details>

### 🚧 v1.1 [Name] (In Progress)

**Study Goal:** [What v1.1 delivers]

#### Experiment 5: [Name]
**Goal**: [What this experiment delivers]
**Depends on**: Experiment 4
**Plans**: 2 plans

Plans:
- [ ] 05-01: [Brief description]
- [ ] 05-02: [Brief description]

[... remaining v1.1 experiments ...]

### 📋 v2.0 [Name] (Planned)

**Study Goal:** [What v2.0 delivers]

[... v2.0 experiments ...]

## Progress

| Experiment | Study | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Foundation | v1.0 | 3/3 | Complete | YYYY-MM-DD |
| 2. Features | v1.0 | 2/2 | Complete | YYYY-MM-DD |
| 5. Security | v1.1 | 0/2 | Not started | - |
```

**Notes:**
- Study emoji: ✅ shipped, 🚧 in progress, 📋 planned
- Completed studies collapsed in `<details>` for readability
- Current/future studies expanded
- Continuous experiment numbering (01-99)
- Progress table includes study column
