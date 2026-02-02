# CLI Naming Conventions: ML/Research Workflow Tools

**Researched:** 2026-02-01
**Confidence:** HIGH (official documentation verified via WebFetch)

## Executive Summary

ML/research CLI tools overwhelmingly follow a **noun-verb** pattern at the subcommand level (e.g., `dvc exp run`, `mlflow experiments create`). The primary noun groups resources logically, then verbs operate on those resources. Standard CRUD verbs dominate (`create`, `delete`, `list`, `show`), with domain-specific verbs for lifecycle operations (`run`, `restore`, `apply`).

GRD should adopt the noun-verb pattern for resource management and use domain-appropriate verbs for its research workflow lifecycle.

---

## Tool Analysis

### DVC (Data Version Control)

**Pattern:** Git-inspired commands + noun-verb for experiments

**Core Commands (Git-inspired verbs):**
| Command | Pattern | Notes |
|---------|---------|-------|
| `init` | verb | Initialize project |
| `add` | verb | Track files |
| `push` | verb | Upload to remote |
| `pull` | verb | Download from remote |
| `checkout` | verb | Update workspace |
| `fetch` | verb | Download to cache |
| `diff` | verb | Show changes |
| `status` | verb | Show state |

**Experiment Commands (`dvc exp <verb>`):**
| Subcommand | Pattern | Description |
|------------|---------|-------------|
| `run` | verb | Execute experiment |
| `show` | verb | Display experiments |
| `diff` | verb | Compare experiments |
| `apply` | verb | Apply experiment changes to workspace |
| `branch` | verb | Promote experiment to Git branch |
| `clean` | verb | Cleanup temporary files |
| `list` | verb | List experiments |
| `push` | verb | Push to remote |
| `pull` | verb | Pull from remote |
| `remove` | verb | Delete experiment |
| `save` | verb | Save current state as experiment |

**Key insight:** DVC uses `exp` as the noun, then standard verbs. `apply` and `branch` are lifecycle-specific verbs for "graduating" experiments.

**Sources:**
- [DVC Command Reference](https://dvc.org/doc/command-reference)
- [DVC Experiment Commands](https://doc.dvc.org/command-reference/exp/run)

---

### MLflow

**Pattern:** Noun-verb with CRUD operations

**Top-Level Command Groups (nouns):**
| Group | Purpose |
|-------|---------|
| `experiments` | Experiment lifecycle |
| `runs` | Individual run management |
| `models` | Model deployment |
| `artifacts` | Artifact operations |
| `deployments` | Deployment targets |
| `traces` | Trace management |

**Experiments Subcommands:**
| Subcommand | Pattern | Description |
|------------|---------|-------------|
| `create` | CRUD verb | Create experiment |
| `delete` | CRUD verb | Mark for deletion |
| `restore` | lifecycle verb | Restore deleted experiment |
| `rename` | verb | Change name |
| `search` | verb | Find experiments |
| `get` | CRUD verb | Retrieve single experiment |
| `csv` | noun (export format) | Export as CSV |

**Runs Subcommands:**
| Subcommand | Pattern | Description |
|------------|---------|-------------|
| `create` | CRUD verb | Create run |
| `delete` | CRUD verb | Mark for deletion |
| `restore` | lifecycle verb | Restore deleted run |
| `describe` | verb | Show details |
| `list` | CRUD verb | List runs |
| `link-traces` | compound verb | Associate traces |

**Lifecycle States:** MLflow uses `active_only`, `deleted_only`, `all` as view filters rather than explicit state commands. Deletion is soft (mark for deletion) with explicit `restore` and `gc` (garbage collect) for permanent deletion.

**Sources:**
- [MLflow CLI Reference](https://mlflow.org/docs/latest/cli.html)

---

### Weights & Biases (wandb)

**Pattern:** Mixed - some verb-first, some noun-verb

**Primary Commands:**
| Command | Pattern | Description |
|---------|---------|-------------|
| `init` | verb | Configure directory |
| `login` | verb | Authenticate |
| `agent` | noun | Run sweep agent |
| `launch` | verb | Launch or queue job |
| `sync` | verb | Synchronize data |
| `pull` | verb | Pull files |
| `restore` | verb | Restore run state |
| `sweep` | noun | Initialize hyperparameter sweep |
| `status` | verb | Show configuration |

**Noun-based Command Groups:**
| Group | Subcommands |
|-------|-------------|
| `artifact` | (commands for artifact interaction) |
| `job` | (commands for job management) |
| `server` | (commands for local server) |

**State Toggles:**
| Command | Description |
|---------|-------------|
| `online` | Enable sync |
| `offline` | Disable sync |
| `enabled` | Enable W&B |
| `disabled` | Disable W&B |

**Key insight:** W&B uses adjectives (`online`/`offline`, `enabled`/`disabled`) for state toggles rather than `set-state` patterns.

**Sources:**
- [W&B CLI Reference](https://docs.wandb.ai/ref/cli/)

---

### Hydra

**Pattern:** Flag-based configuration, not subcommand-based

Hydra operates through command-line flags and config overrides rather than subcommands:

| Flag | Purpose |
|------|---------|
| `--config-path, -cp` | Override config path |
| `--config-name, -cn` | Override config name |
| `--config-dir, -cd` | Add config directory |
| `--info, -i` | Print Hydra info |
| `--multirun` | Enable sweep mode |

**Override syntax:**
```bash
python my_app.py db=postgresql db.timeout=20
python my_app.py +experiment=fast_mode  # + for new fields
```

**Key insight:** Hydra doesn't use CLI commands for lifecycle - it's configuration-first with runtime composition.

**Sources:**
- [Hydra CLI Flags](https://hydra.cc/docs/advanced/hydra-command-line-flags/)
- [Hydra Experiment Configuration](https://hydra.cc/docs/patterns/configuring_experiments/)

---

### Sacred

**Pattern:** Built-in commands with custom extensions

**Built-in Commands:**
| Command | Description |
|---------|-------------|
| `print_config` | Display configuration |
| `print_dependencies` | Show dependencies |
| `save_config` | Export configuration |
| `print_named_configs` | List named configs |

**Configuration Override Pattern:**
```bash
./example.py with 'a=10' 'b="FooBar"'
./example.py with variant1  # Named config
./example.py with config.json  # File config
```

**Lifecycle Flags:**
| Flag | Purpose |
|------|---------|
| `-q, --queue` | Queue run (don't execute) |
| `-u, --unobserved` | Run without observers |
| `-n, --name` | Set run name |
| `-i, --id` | Set run ID |

**Key insight:** Sacred uses `with` as a configuration mechanism, and flags for lifecycle control rather than subcommands.

**Sources:**
- [Sacred CLI Reference](https://sacred.readthedocs.io/en/stable/command_line.html)

---

### Neptune.ai

**Pattern:** Python-first, minimal CLI

Neptune primarily uses Python API rather than CLI commands. The CLI focuses on:
- Authentication
- Environment configuration
- Framework integrations (callbacks)

**Key insight:** Neptune is API-first, CLI-minimal. Not a good model for CLI-heavy tools.

**Sources:**
- [Neptune Documentation](https://docs.neptune.ai/)

---

## Common Patterns Across Tools

### Standard Verbs

| Verb | Usage | Tools |
|------|-------|-------|
| `init` | Initialize project/directory | DVC, wandb, Sacred |
| `run` | Execute experiment/job | DVC, MLflow |
| `create` | Create new resource | MLflow |
| `delete` | Remove/mark for deletion | MLflow |
| `list` | List resources | DVC, MLflow, wandb |
| `show` | Display details | DVC |
| `diff` | Compare versions | DVC |
| `push` | Upload to remote | DVC, wandb |
| `pull` | Download from remote | DVC, wandb |
| `restore` | Recover deleted resource | MLflow |
| `apply` | Apply changes to workspace | DVC |
| `sync` | Synchronize state | wandb |

### Experiment Lifecycle Patterns

**Three-stage lifecycle observed:**

1. **Creation/Setup:** `init`, `create`, `add`
2. **Execution:** `run`, `start`
3. **Completion/Graduation:** `apply`, `branch`, `save`, `complete`

**Soft deletion pattern:**
- `delete` marks for deletion (reversible)
- `restore` recovers deleted items
- `gc` (garbage collect) permanently removes

### Noun-Verb vs Verb-Noun

| Pattern | Example | When Used |
|---------|---------|-----------|
| Noun-verb | `dvc exp run`, `mlflow experiments create` | Resource-centric, CRUD operations |
| Verb-first | `wandb sync`, `dvc push` | Global operations, common actions |
| Flag-based | `--multirun`, `with config` | Configuration, mode selection |

**Industry trend:** Noun-verb is more common for tools with multiple resource types. Docker popularized this pattern (`docker container create`).

---

## Recommendations for GRD

### Current GRD Commands (Audit)

GRD currently uses:
- `new-project`, `new-study` (verb-noun compound)
- `execute-phase`, `plan-phase`, `literature-review` (verb-noun compound)
- `complete-study`, `audit-study`, `graduate` (verb-noun or standalone verb)
- `add-phase`, `remove-phase`, `insert-phase` (verb-noun compound)
- `pause-work`, `resume-work` (verb-noun compound)

**Pattern:** Primarily verb-noun compounds with kebab-case.

### Naming Recommendations

**1. Keep verb-noun compounds for phase operations:**

The current pattern (`execute-phase`, `plan-phase`) is clear and consistent. The "phase" suffix groups related commands visually when listed alphabetically.

**2. Use industry-standard verbs:**

| Current | Recommendation | Rationale |
|---------|---------------|-----------|
| `new-study` | Keep | `new` is common (PowerShell, git) |
| `complete-study` | Keep | `complete` is clearer than `finish` |
| `graduate` | Keep | Domain-specific, intuitive metaphor |
| `audit-study` | Consider `verify-study` | Aligns with `verify-work` |

**3. Study lifecycle commands:**

| Lifecycle Stage | Command | Notes |
|-----------------|---------|-------|
| Create | `new-study` | Already exists |
| Plan gaps | `plan-study-gaps` | Already exists |
| Execute | (via `execute-phase`) | Study phases are phases |
| Verify | `audit-study` | Consider rename to `verify-study` |
| Complete | `complete-study` | Already exists |
| Graduate | `graduate` | Move from quick to roadmap |

**4. Avoid ambiguous verbs:**

Per CLI guidelines, avoid verbs that could be confused:
- Don't use both `update` and `upgrade`
- Don't use both `get` and `fetch` for similar operations
- GRD already avoids this well

**5. Consider noun-first grouping for future scale:**

If GRD grows to have many more resource types, consider restructuring to:
```
grd study new
grd study complete
grd study audit
grd phase execute
grd phase plan
grd phase add
```

For now, the current flat structure with verb-noun compounds works well given the manageable number of commands.

### Verb Recommendations by Category

**Lifecycle verbs (for studies/experiments):**
- `new` - create new resource
- `plan` - create plan for resource
- `execute` - run/perform the work
- `verify` - check correctness
- `complete` - mark as finished
- `graduate` - promote to higher status

**CRUD verbs (for phases/todos):**
- `add` - add new item
- `remove` - delete item
- `insert` - add at specific position
- `list` - show all items
- `show` - display single item details

**State verbs:**
- `pause` - temporarily stop
- `resume` - continue from pause
- `reset` - return to initial state

**Analysis verbs:**
- `check` - validate
- `audit` - comprehensive review
- `explore` - investigate/discover
- `research` - deep investigation

---

## Confidence Assessment

| Finding | Confidence | Source |
|---------|------------|--------|
| DVC commands | HIGH | Official docs via WebFetch |
| MLflow commands | HIGH | Official docs via WebFetch |
| W&B commands | HIGH | Official docs via WebFetch |
| Sacred commands | HIGH | Official docs via WebFetch |
| Hydra patterns | HIGH | Official docs via WebSearch |
| Noun-verb preference | HIGH | clig.dev, Azure CLI guidelines |
| GRD recommendations | MEDIUM | Based on analysis, not tested |

---

## Sources

- [DVC Command Reference](https://dvc.org/doc/command-reference)
- [MLflow CLI Reference](https://mlflow.org/docs/latest/cli.html)
- [W&B CLI Reference](https://docs.wandb.ai/ref/cli/)
- [Sacred CLI Reference](https://sacred.readthedocs.io/en/stable/command_line.html)
- [Hydra CLI Flags](https://hydra.cc/docs/advanced/hydra-command-line-flags/)
- [Neptune Documentation](https://docs.neptune.ai/)
- [Command Line Interface Guidelines](https://clig.dev/)
- [Azure CLI Command Guidelines](https://github.com/Azure/azure-cli/blob/dev/doc/command_guidelines.md)
