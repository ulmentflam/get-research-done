<div align="center">

# GET RESEARCH DONE (GRD)

**A recursive, agentic framework for ML research with hypothesis-driven experimentation for Claude Code.**

**Structured ML experimentation with scientific rigor — from hypothesis to validated conclusion, with a Critic agent enforcing skepticism at every step.**

[![npm version](https://img.shields.io/npm/v/get-research-done?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/get-research-done)
[![npm downloads](https://img.shields.io/npm/dm/get-research-done?style=for-the-badge&logo=npm&logoColor=white&color=CB3837)](https://www.npmjs.com/package/get-research-done)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/5JJgD5svVS)
[![GitHub stars](https://img.shields.io/github/stars/glittercowboy/get-research-done?style=for-the-badge&logo=github&color=181717)](https://github.com/glittercowboy/get-research-done)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

<br>

```bash
npx get-research-done
```

**Works on Mac, Windows, and Linux.**

<br>

![GSD Install](assets/terminal.svg)

<br>

*"If you know clearly what you want, this WILL build it for you. No bs."*

*"I've done SpecKit, OpenSpec and Taskmaster — this has produced the best results for me."*

*"By far the most powerful addition to my Claude Code. Nothing over-engineered. Literally just gets shit done."*

<br>

**Trusted by engineers at Amazon, Google, Shopify, and Webflow.**

[Why I Built This](#why-i-built-this) · [How It Works](#how-it-works) · [Commands](#commands) · [Why It Works](#why-it-works)

</div>

---

## Why I Built This

I'm a solo developer. I don't write code — Claude Code does.

Other spec-driven development tools exist; BMAD, Speckit... But they all seem to make things way more complicated than they need to be (sprint ceremonies, story points, stakeholder syncs, retrospectives, Jira workflows) or lack real big picture understanding of what you're building. I'm not a 50-person software company. I don't want to play enterprise theater. I'm just a creative person trying to build great things that work.

So I built GRD. The complexity is in the system, not in your workflow. Behind the scenes: context engineering, XML prompt formatting, subagent orchestration, state management, recursive validation loops. What you see: a few commands that just work.

The system gives Claude everything it needs to do ML research with scientific rigor — hypothesis generation, experimentation, validation, and skeptical review at every step.

That's what this is. No enterprise roleplay bullshit. Just an incredibly effective system for hypothesis-driven ML research using Claude Code.

— **TÂCHES**

---

ML research has a reproducibility crisis. Experiments are ad-hoc, hypotheses are vague, validation is subjective, and insights get lost.

GRD fixes that. It's the framework that makes ML research systematic. State your hypothesis, let the system design experiments, execute with rigor, and validate with skepticism.

---

## Who This Is For

ML researchers and practitioners who want structured experimentation with hypothesis-driven workflows — without building custom research infrastructure from scratch.

---

## Getting Started

```bash
npx get-research-done
```

The installer prompts you to choose:
1. **Runtime** — Claude Code, OpenCode, or both
2. **Location** — Global (all projects) or local (current project only)

Verify with `/grd:help` inside your Claude Code or OpenCode interface.

### Staying Updated

GRD evolves fast. Update periodically:

```bash
npx get-research-done@latest
```

<details>
<summary><strong>Non-interactive Install (Docker, CI, Scripts)</strong></summary>

```bash
# Claude Code
npx get-research-done --claude --global   # Install to ~/.claude/
npx get-research-done --claude --local    # Install to ./.claude/

# OpenCode (open source, free models)
npx get-research-done --opencode --global # Install to ~/.opencode/

# Both runtimes
npx get-research-done --both --global     # Install to both directories
```

Use `--global` (`-g`) or `--local` (`-l`) to skip the location prompt.
Use `--claude`, `--opencode`, or `--both` to skip the runtime prompt.

</details>

<details>
<summary><strong>Development Installation</strong></summary>

Clone the repository and run the installer locally:

```bash
git clone https://github.com/glittercowboy/get-research-done.git
cd get-research-done
node bin/install.js --claude --local
```

Installs to `./.claude/` for testing modifications before contributing.

</details>

### Recommended: Skip Permissions Mode

GRD is designed for frictionless automation. Run Claude Code with:

```bash
claude --dangerously-skip-permissions
```

> [!TIP]
> This is how GRD is intended to be used — stopping to approve `date` and `git commit` 50 times defeats the purpose.

<details>
<summary><strong>Alternative: Granular Permissions</strong></summary>

If you prefer not to use that flag, add this to your project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(date:*)",
      "Bash(echo:*)",
      "Bash(cat:*)",
      "Bash(ls:*)",
      "Bash(mkdir:*)",
      "Bash(wc:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(sort:*)",
      "Bash(grep:*)",
      "Bash(tr:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git tag:*)"
    ]
  }
}
```

</details>

---

## How It Works

> **Already have ML code?** Run `/grd:map-codebase` first. It spawns parallel agents to analyze your models, datasets, metrics, and experiment patterns. Then `/grd:new-project` knows your research context — questions focus on your hypothesis, and planning automatically loads your experimental setup.

### 1. Initialize Project

```
/grd:new-project
```

One command, one flow. The system:

1. **Questions** — Asks until it understands your research goal (hypothesis, metrics, baselines, constraints)
2. **Research** — Spawns parallel agents to investigate the domain (optional but recommended)
3. **Requirements** — Extracts what's essential for validation, what's future work
4. **Roadmap** — Creates phases mapped to the research loop (explore → synthesize → implement → validate)

You approve the roadmap. Now you're ready to experiment.

**Creates:** `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`, `.planning/research/`

---

### 2. Discuss Phase

```
/grd:discuss-phase 1
```

**This is where you shape the experiment design.**

Your roadmap has a sentence or two per phase. That's not enough context to design experiments the way *you* imagine them. This step captures your preferences before anything gets researched or planned.

The system analyzes the phase and identifies gray areas based on what's being researched:

- **Data exploration** → Feature selection, preprocessing, validation splits
- **Model architecture** → Layer design, activation functions, regularization
- **Training loops** → Optimization strategy, learning rate schedules, early stopping
- **Evaluation metrics** → Which metrics matter, baseline comparisons, statistical significance

For each area you select, it asks until you're satisfied. The output — `CONTEXT.md` — feeds directly into the next two steps:

1. **Researcher reads it** — Knows what patterns to investigate ("user wants transformer architecture" → research attention mechanisms)
2. **Planner reads it** — Knows what decisions are locked ("Adam optimizer decided" → plan includes optimizer configuration)

The deeper you go here, the more the system experiments the way you actually want. Skip it and you get reasonable defaults. Use it and you get *your* experimental design.

**Creates:** `{phase}-CONTEXT.md`

---

### 3. Plan Phase

```
/grd:plan-phase 1
```

The system:

1. **Researches** — Investigates how to design experiments for this phase, guided by your CONTEXT.md decisions
2. **Plans** — Creates 2-3 atomic experiment plans with XML structure
3. **Verifies** — Checks plans against research goals, loops until they pass

Each plan is small enough to execute in a fresh context window. No degradation, no context rot.

**Creates:** `{phase}-RESEARCH.md`, `{phase}-{N}-PLAN.md`

---

### 4. Execute Phase

```
/grd:execute-phase 1
```

The system:

1. **Runs experiments in waves** — Parallel where possible, sequential when dependent
2. **Fresh context per plan** — 200k tokens purely for experimentation, zero accumulated garbage
3. **Commits per task** — Every experiment gets its own atomic commit
4. **Verifies against hypotheses** — Checks the results validate what the phase proposed

Walk away, come back to completed experiments with clean git history and tracked results.

**Creates:** `{phase}-{N}-SUMMARY.md`, `{phase}-VERIFICATION.md`

---

### 5. Verify Work

```
/grd:verify-work 1
```

**This is where you confirm the results are valid.**

Automated verification checks that experiments ran and metrics were logged. But are the results *meaningful*? This is your chance to evaluate them.

The system:

1. **Extracts testable hypotheses** — What should be validated now
2. **Walks you through one at a time** — "Did accuracy improve over baseline?" Yes/no, or describe what's wrong
3. **Diagnoses failures automatically** — Spawns debug agents to find root causes
4. **Creates verified fix plans** — Ready for immediate re-execution

If everything validates, you move on. If something's invalid, you don't manually debug — you just run `/grd:execute-phase` again with the fix plans it created.

**Creates:** `{phase}-UAT.md`, fix plans if issues found

---

### 6. Repeat → Complete → Next Milestone

```
/grd:discuss-phase 2
/grd:plan-phase 2
/grd:execute-phase 2
/grd:verify-work 2
...
/grd:complete-milestone
/grd:new-milestone
```

Loop **discuss → plan → execute → verify** until milestone complete.

Each phase gets your input (discuss), proper research (plan), clean execution (execute), and human verification (verify). Context stays fresh. Quality stays high.

When all phases are done, `/grd:complete-milestone` archives the milestone and tags the release.

Then `/grd:new-milestone` starts the next version — same flow as `new-project` but for your existing codebase. You describe what you want to build next, the system researches the domain, you scope requirements, and it creates a fresh roadmap. Each milestone is a clean cycle: define → build → ship.

---

### Quick Mode

```
/grd:quick
```

**For ad-hoc experiments that don't need full planning.**

Quick mode gives you GRD guarantees (atomic commits, state tracking, metric logging) with a faster path:

- **Same agents** — Planner + executor, same quality
- **Skips optional steps** — No research, no plan checker, no Critic review
- **Separate tracking** — Lives in `.planning/quick/`, not phases

Use for: hyperparameter sweeps, ablation studies, metric checks, one-off experiments.

```
/grd:quick
> What do you want to do? "Run learning rate sweep from 1e-5 to 1e-2"
```

**Creates:** `.planning/quick/001-learning-rate-sweep/PLAN.md`, `SUMMARY.md`

---

## Why It Works

### Context Engineering

Claude Code is incredibly powerful *if* you give it the context it needs. Most ML researchers don't have time to structure it properly.

GRD handles it for you:

| File | What it does |
|------|--------------|
| `PROJECT.md` | Research vision, hypothesis, baseline expectations |
| `research/` | Domain knowledge (datasets, models, metrics, pitfalls) |
| `REQUIREMENTS.md` | Scoped validation requirements with phase traceability |
| `ROADMAP.md` | Research loop stages, what's validated |
| `STATE.md` | Decisions, blockers, loop history — memory across sessions |
| `PLAN.md` | Atomic experiment with XML structure, verification steps |
| `SUMMARY.md` | Results, insights, what changed, committed to history |
| `todos/` | Captured hypotheses and experiments for later work |

Size limits based on where Claude's quality degrades. Stay under, get consistent excellence.

### XML Prompt Formatting

Every plan is structured XML optimized for Claude:

```xml
<task type="auto">
  <name>Train baseline CNN model</name>
  <files>experiments/baseline_cnn.py</files>
  <action>
    Use PyTorch for model definition.
    3 conv layers with ReLU, max pooling, dropout.
    Train for 50 epochs with early stopping.
    Log metrics to MLflow.
  </action>
  <verify>MLflow shows run with test accuracy logged</verify>
  <done>Baseline model trained, metrics logged, checkpoint saved</done>
</task>
```

Precise instructions. No guessing. Verification built in.

### Multi-Agent Orchestration

Every stage uses the same pattern: a thin orchestrator spawns specialized agents, collects results, and routes to the next step.

| Stage | Orchestrator does | Agents do |
|-------|------------------|-----------|
| Research | Coordinates, presents findings | 5 parallel agents: Explorer (data), Architect (models), Researcher (domain), Critic (validity), Evaluator (metrics) |
| Planning | Validates, manages iteration | Planner creates experiments, checker verifies, Critic reviews, loop until pass |
| Execution | Groups into waves, tracks progress | Executors run experiments in parallel, each with fresh 200k context |
| Verification | Presents results, routes next | Verifier checks results against hypotheses, Critic challenges conclusions, debuggers diagnose failures |

The orchestrator never does heavy lifting. It spawns agents, waits, integrates results.

**The result:** You can run an entire research loop — deep domain investigation, multiple experiments designed and validated, models trained across parallel executors, automated verification against hypotheses — and your main context window stays at 30-40%. The work happens in fresh subagent contexts. Your session stays fast and responsive.

### Atomic Git Commits

Each task gets its own commit immediately after completion:

```bash
abc123f docs(02-01): complete baseline experiment plan
def456g feat(02-01): train CNN baseline model
hij789k feat(02-01): log metrics to MLflow
lmn012o feat(02-01): save model checkpoint
```

> [!NOTE]
> **Benefits:** Git bisect finds exact failing task. Each task independently revertable. Clear history for Claude in future sessions. Better observability in AI-automated workflow.

Every commit is surgical, traceable, and meaningful.

### Modular by Design

- Add phases to current milestone
- Insert urgent work between phases
- Complete milestones and start fresh
- Adjust plans without rebuilding everything

You're never locked in. The system adapts.

---

## Commands

### Core Workflow

| Command | What it does |
|---------|--------------|
| `/grd:new-project` | Full initialization: questions → research → requirements → roadmap |
| `/grd:discuss-phase [N]` | Capture implementation decisions before planning |
| `/grd:plan-phase [N]` | Research + plan + verify for a phase |
| `/grd:execute-phase <N>` | Execute all plans in parallel waves, verify when complete |
| `/grd:verify-work [N]` | Manual user acceptance testing ¹ |
| `/grd:audit-milestone` | Verify milestone achieved its definition of done |
| `/grd:complete-milestone` | Archive milestone, tag release |
| `/grd:new-milestone [name]` | Start next version: questions → research → requirements → roadmap |

### Navigation

| Command | What it does |
|---------|--------------|
| `/grd:progress` | Where am I? What's next? |
| `/grd:help` | Show all commands and usage guide |
| `/grd:update` | Update GSD with changelog preview |
| `/grd:join-discord` | Join the GSD Discord community |

### Brownfield

| Command | What it does |
|---------|--------------|
| `/grd:map-codebase` | Analyze existing codebase before new-project |

### Phase Management

| Command | What it does |
|---------|--------------|
| `/grd:add-phase` | Append phase to roadmap |
| `/grd:insert-phase [N]` | Insert urgent work between phases |
| `/grd:remove-phase [N]` | Remove future phase, renumber |
| `/grd:list-phase-assumptions [N]` | See Claude's intended approach before planning |
| `/grd:plan-milestone-gaps` | Create phases to close gaps from audit |

### Session

| Command | What it does |
|---------|--------------|
| `/grd:pause-work` | Create handoff when stopping mid-phase |
| `/grd:resume-work` | Restore from last session |

### Utilities

| Command | What it does |
|---------|--------------|
| `/grd:settings` | Configure model profile and workflow agents |
| `/grd:set-profile <profile>` | Switch model profile (quality/balanced/budget) |
| `/grd:add-todo [desc]` | Capture idea for later |
| `/grd:check-todos` | List pending todos |
| `/grd:debug [desc]` | Systematic debugging with persistent state |
| `/grd:quick` | Execute ad-hoc task with GSD guarantees |

<sup>¹ Contributed by reddit user OracleGreyBeard</sup>

---

## Configuration

GSD stores project settings in `.planning/config.json`. Configure during `/grd:new-project` or update later with `/grd:settings`.

### Core Settings

| Setting | Options | Default | What it controls |
|---------|---------|---------|------------------|
| `mode` | `yolo`, `interactive` | `interactive` | Auto-approve vs confirm at each step |
| `depth` | `quick`, `standard`, `comprehensive` | `standard` | Planning thoroughness (phases × plans) |

### Model Profiles

Control which Claude model each agent uses. Balance quality vs token spend.

| Profile | Planning | Execution | Verification |
|---------|----------|-----------|--------------|
| `quality` | Opus | Opus | Sonnet |
| `balanced` (default) | Opus | Sonnet | Sonnet |
| `budget` | Sonnet | Sonnet | Haiku |

Switch profiles:
```
/grd:set-profile budget
```

Or configure via `/grd:settings`.

### Workflow Agents

These spawn additional agents during planning/execution. They improve quality but add tokens and time.

| Setting | Default | What it does |
|---------|---------|--------------|
| `workflow.research` | `true` | Researches domain before planning each phase |
| `workflow.plan_check` | `true` | Verifies plans achieve phase goals before execution |
| `workflow.verifier` | `true` | Confirms must-haves were delivered after execution |

Use `/grd:settings` to toggle these, or override per-invocation:
- `/grd:plan-phase --skip-research`
- `/grd:plan-phase --skip-verify`

### Execution

| Setting | Default | What it controls |
|---------|---------|------------------|
| `parallelization.enabled` | `true` | Run independent plans simultaneously |
| `planning.commit_docs` | `true` | Track `.planning/` in git |

---

## Troubleshooting

**Commands not found after install?**
- Restart Claude Code to reload slash commands
- Verify files exist in `~/.claude/commands/grd/` (global) or `./.claude/commands/grd/` (local)

**Commands not working as expected?**
- Run `/grd:help` to verify installation
- Re-run `npx get-research-done` to reinstall

**Updating to the latest version?**
```bash
npx get-research-done@latest
```

**Using Docker or containerized environments?**

If file reads fail with tilde paths (`~/.claude/...`), set `CLAUDE_CONFIG_DIR` before installing:
```bash
CLAUDE_CONFIG_DIR=/home/youruser/.claude npx get-research-done --global
```
This ensures absolute paths are used instead of `~` which may not expand correctly in containers.

### Uninstalling

To remove GSD completely:

```bash
# Global installs
npx get-research-done --claude --global --uninstall
npx get-research-done --opencode --global --uninstall

# Local installs (current project)
npx get-research-done --claude --local --uninstall
npx get-research-done --opencode --local --uninstall
```

This removes all GRD commands, agents, hooks, and settings while preserving your other configurations.

---

## Community Ports

| Project | Platform | Description |
|---------|----------|-------------|
| [grd-opencode](https://github.com/rokicool/grd-opencode) | OpenCode | GRD adapted for OpenCode CLI |
| [grd-gemini](https://github.com/uberfuzzy/grd-gemini) | Gemini CLI | GRD adapted for Google's Gemini CLI |

---

## Star History

<a href="https://star-history.com/#glittercowboy/get-research-done&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=glittercowboy/get-research-done&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=glittercowboy/get-research-done&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=glittercowboy/get-research-done&type=Date" />
 </picture>
</a>

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

**Claude Code is powerful. GRD makes ML research systematic.**

</div>
