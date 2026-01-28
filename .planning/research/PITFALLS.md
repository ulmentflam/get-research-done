# Domain Pitfalls: ML Research Workflow Tools

**Domain:** Machine Learning Research Workflow Automation
**Researched:** 2026-01-27
**Confidence:** MEDIUM (based on established ML engineering principles and research practices)

## Executive Summary

ML research workflow tools fail when they treat research like software development. The fundamental difference: software ships deterministic features, research tests probabilistic hypotheses. Tools that optimize for "getting to production faster" miss the point — research optimizes for understanding truth, not shipping code.

**Critical insight:** Most pitfalls stem from insufficient skepticism. Tools should make it harder to deceive yourself, not easier to ship models.

---

## Critical Pitfalls

These mistakes cause rewrites, invalid research, or catastrophic deployment failures.

### Pitfall 1: Data Leakage Through Tool Convenience

**What goes wrong:**
Workflow tools that auto-generate train/test splits without explicit temporal or stratification controls enable subtle leakage. The tool "just works" — which means researchers don't understand what it's doing under the hood.

**Examples:**
- Automatic feature engineering that uses future information
- Default sklearn `train_test_split()` on time-series data (shuffles temporally dependent rows)
- Normalization computed on full dataset before split
- Using test set metrics to select models during hyperparameter tuning

**Why it happens:**
Tools prioritize convenience over correctness. "Zero-config experiment tracking" sounds good but hides critical decisions about data boundaries.

**Consequences:**
- Inflated performance metrics (90% accuracy becomes 60% in production)
- Invalid research conclusions
- Wasted compute on experiments with contaminated results
- Loss of trust when models fail in deployment

**Prevention:**
- **Explicit data provenance tracking:** Tool must force user to declare "where does this data come from?" before any split
- **Temporal validation by default:** For time-series, tool should enforce chronological split unless user explicitly overrides
- **Critic agent validation:** Check for leakage patterns:
  - Are test indices referenced during training?
  - Is normalization fit on train+test?
  - Are features derived from target variable?
- **Mandatory data freeze:** Test set should be write-protected after creation

**Detection (warning signs):**
- Performance drops significantly between validation and holdout test
- Model performs suspiciously well on early experiments
- Features have perfect correlation with target
- Researcher can't explain why specific split strategy was chosen

**Phase mapping:**
- **Phase 1 (Data Reconnaissance):** Explorer must document temporal dependencies, leakage risks
- **Phase 3 (Recursive Loop):** Critic must validate splits before Researcher trains

---

### Pitfall 2: Experiment Versioning Without Hypothesis Versioning

**What goes wrong:**
Tools track `experiment_001`, `experiment_002`, etc. but don't track *why* experiments were run or what hypothesis they tested. Six months later, you have 200 experiment folders with no narrative.

**Examples:**
- Git-like versioning for experiments without commit messages
- Hyperparameter logs without "why we tried this"
- Results tables without interpretation
- Model checkpoints without decision context

**Why it happens:**
Tools copy software versioning patterns without adapting to research context. In software, code is self-documenting. In research, code + results ≠ understanding.

**Consequences:**
- Can't reproduce thought process, only execution
- Redundant experiments (forgot we already tried that)
- No learning accumulation between researchers
- Unable to write coherent papers (no storyline connecting results)

**Prevention:**
- **Hypothesis-first structure:** Every experiment folder must contain `HYPOTHESIS.md` stating:
  - What we believe
  - Why we believe it
  - What would disprove it
  - How this experiment tests it
- **Decision log:** `DECISION_LOG.md` tracks: "Based on experiment N, we decided X because Y"
- **Critic gate:** Experiments without stated hypothesis are rejected
- **Relationship mapping:** Track which experiments are refinements vs pivots vs validations

**Detection (warning signs):**
- Researcher can't explain why they ran experiment N
- Team members re-run experiments that already exist
- Paper writing requires "archaeology" through experiment folders
- Code changes between experiments but unclear what hypothesis changed

**Phase mapping:**
- **Phase 2 (Hypothesis Synthesis):** Architect must create testable hypothesis with falsification criteria
- **Phase 3 (Recursive Loop):** Each Researcher iteration must reference hypothesis being tested
- **Phase 4 (Human Evaluation):** Evidence package must show hypothesis → experiment → result chain

---

### Pitfall 3: Metric Fixation Without Distribution Validation

**What goes wrong:**
Tools optimize for single scalar metrics (accuracy, F1, loss) without validating that the underlying data distribution matches assumptions. Model achieves 95% accuracy but on a shifted or cherry-picked distribution.

**Examples:**
- Optimizing RMSE when distribution is long-tailed (mean is misleading)
- High accuracy from class imbalance (99% accuracy on 99:1 dataset)
- Aggregate metrics hiding subgroup failures
- Validation set that doesn't match deployment distribution

**Why it happens:**
Tools present dashboards with big numbers. Humans optimize what's measured. Nobody checks if the measurement is meaningful.

**Consequences:**
- Models fail catastrophically on rare-but-important cases
- Fairness issues (high average accuracy, terrible minority performance)
- Inability to detect distribution shift
- False confidence in model quality

**Prevention:**
- **Distribution-first evaluation:** Before any metric, Explorer documents:
  - Class balance
  - Outliers
  - Subgroup distributions
  - Temporal drift patterns
- **Stratified metrics by default:** Tool automatically breaks down performance by:
  - Quantiles
  - Known subgroups
  - Confidence bins
- **Critic validation:** Check that metric choice matches distribution characteristics
- **Red flag detection:** Automatic warnings when:
  - High variance across quantiles
  - Performance << random baseline on subgroups
  - Validation distribution diverges from training

**Detection (warning signs):**
- High aggregate metric but can't explain failure modes
- Model works on average cases, fails on edges
- Performance varies wildly by subgroup
- Data distribution not documented in research reports

**Phase mapping:**
- **Phase 1 (Data Reconnaissance):** Explorer must profile distributions before modeling
- **Phase 2 (Hypothesis Synthesis):** Architect must define success metrics appropriate to distribution
- **Phase 3 (Recursive Loop):** Evaluator must report stratified metrics, not just aggregates

---

### Pitfall 4: Notebook-to-Production Graduation Without Refactor

**What goes wrong:**
Research code stays in notebooks, then gets "productionized" by wrapping notebook cells in functions. The tool facilitates this transition without enforcing separation of exploration vs execution logic.

**Examples:**
- Production code with hardcoded paths from notebook
- Global state from notebook cells leaking into modules
- Non-deterministic execution order dependencies
- Model training that only works in notebook environment

**Why it happens:**
Tools treat notebooks as the final artifact rather than exploration medium. "Export to .py" features create illusion of production-readiness.

**Consequences:**
- Non-reproducible model training
- Fragile pipelines that break on environment changes
- Inability to scale or parallelize training
- Technical debt that compounds over time

**Prevention:**
- **Explicit graduation gate:** Tool distinguishes:
  - `experiments/exploration/` — Notebooks for EDA, prototyping
  - `experiments/validated/` — Refactored, reproducible training scripts
  - `production/` — Deployment-ready modules
- **Refactor checklist:** Before promotion, validate:
  - No hardcoded paths
  - Deterministic execution with seed control
  - Configurable via parameters (not cell edits)
  - Unit tests for data processing logic
- **Two-stage workflow:**
  1. Notebook for hypothesis exploration
  2. Script rewrite for validated experiments
- **Critic enforcement:** Notebooks can't be marked "complete" — only refactored scripts

**Detection (warning signs):**
- "Works on my machine" syndrome
- Can't reproduce results without notebook environment
- Training scripts with unexplained magic numbers
- Production code imports from `notebook_utils`

**Phase mapping:**
- **Phase 3 (Recursive Loop):** Researcher produces notebooks for exploration, but Evaluator requires scripts for benchmarking
- **Post-validation:** Graduation path clearly separates exploration from production artifacts

---

### Pitfall 5: Hyperparameter Search Without Compute Budget Discipline

**What goes wrong:**
Tools make it trivial to launch massive hyperparameter sweeps without forcing cost-benefit analysis. Researchers burn compute on grid searches that provide marginal gains.

**Examples:**
- Grid search over 1000 configurations for 0.5% metric improvement
- Random search without early stopping
- Hyperparameter tuning before establishing baseline
- Optimization without understanding parameter sensitivity

**Why it happens:**
Tools abstract away compute cost. "Just add more trials" is easier than thinking critically about search strategy.

**Consequences:**
- Wasted compute budget
- Overfitting to validation set through excessive tuning
- Inability to identify truly important hyperparameters
- False attribution of gains (was it architecture or just more tuning?)

**Prevention:**
- **Budget-first planning:** Before hyperparameter search, declare:
  - Compute budget (hours, cost)
  - Expected improvement threshold
  - Stopping criteria
- **Baseline requirement:** Can't start tuning until simple baseline exists
- **Sensitivity analysis:** Tool automatically reports parameter importance
- **Critic challenge:** "Would this compute be better spent on more data or different architecture?"
- **Bayesian by default:** Sequential optimization, not exhaustive grid search

**Detection (warning signs):**
- Hyperparameter search runs for days without clear improvement
- Can't explain which parameters matter most
- Tuning happens before architecture validation
- No documentation of compute cost vs metric gain

**Phase mapping:**
- **Phase 2 (Hypothesis Synthesis):** Architect must specify expected improvement and budget
- **Phase 3 (Recursive Loop):** Researcher must justify search strategy to Critic before execution

---

### Pitfall 6: Ignoring Negative Results

**What goes wrong:**
Tools optimize for tracking successful experiments. Negative results (hypothesis disproven, approach failed) get deleted or forgotten rather than documented.

**Examples:**
- Deleting experiment folders that "didn't work"
- Dashboard showing only best results
- No documentation of what was tried and failed
- Research reports presenting only positive findings

**Why it happens:**
Publication bias extends to tooling. Success feels like progress; failure feels like waste.

**Consequences:**
- Repeated mistakes (new researcher tries same failed approach)
- Publication bias (inflates field-wide success rates)
- Loss of scientific knowledge
- Inability to explain boundaries of approach

**Prevention:**
- **Negative results are first-class:** Tool treats "hypothesis disproven" as valid outcome
- **Mandatory failure documentation:** When Critic returns `REVISE_METHOD` or `REVISE_DATA`, the reason must be logged
- **Archive, don't delete:** Failed experiments move to `experiments/negative_results/` with explanation
- **Decision log tracks failures:** "We tried X, it failed because Y, we learned Z"
- **Evaluation includes negatives:** "What did we try that didn't work?" is required in final report

**Detection (warning signs):**
- Experiment numbers have gaps (001, 002, 005, 007...)
- Team members repeat failed approaches
- Can't explain what was tried before current approach
- Research narrative only shows successes

**Phase mapping:**
- **Phase 3 (Recursive Loop):** Critic exit codes explicitly capture failure modes
- **Phase 4 (Human Evaluation):** Evidence package includes negative results with lessons learned

---

## Moderate Pitfalls

These cause delays or technical debt but are recoverable.

### Pitfall 7: Random Seed Management Theater

**What goes wrong:**
Tools set random seeds for "reproducibility" but don't control all sources of randomness. Results appear reproducible but aren't.

**Examples:**
- Setting numpy seed but not torch seed
- Controlling seeds but not hardware (CUDA non-determinism)
- Seeds set in notebook but not in imported modules
- Different results on different hardware despite same seed

**Prevention:**
- **Comprehensive seed control:** Tool must set:
  - Python `random`
  - NumPy
  - PyTorch/TensorFlow
  - CUDA (deterministic algorithms)
  - DataLoader workers
- **Hardware fingerprint:** Log GPU model, driver version, compute capability
- **Reproducibility test:** Tool validates that running twice produces identical results
- **Honest disclosure:** If non-determinism unavoidable (distributed training), document it

**Detection:**
- Results vary between runs despite same seed
- Can't reproduce colleague's results despite same code

---

### Pitfall 8: Model Checkpointing Without Experiment Context

**What goes wrong:**
Tools save model weights but not the context needed to use them meaningfully.

**Examples:**
- `.pth` file without training config
- Checkpoint without preprocessing pipeline
- Saved model without metadata (what data, what task)
- No record of what experiment produced this checkpoint

**Prevention:**
- **Artifact bundling:** Save together:
  - Model weights
  - Training configuration
  - Data preprocessing pipeline
  - Performance metrics
  - Experiment ID and hypothesis
- **Self-contained checkpoints:** Loading model should restore full inference pipeline
- **Metadata sidecar:** JSON with training context, data stats, timestamp, git hash

**Detection:**
- Can't figure out what a checkpoint was for
- Model file orphaned from training code

---

### Pitfall 9: Evaluation Without Error Analysis

**What goes wrong:**
Tools report aggregate metrics but don't surface *where* the model fails.

**Examples:**
- High accuracy but no understanding of error patterns
- Confusion matrix presented but not analyzed
- No breakdown of errors by input characteristics
- Missing qualitative error inspection

**Prevention:**
- **Automatic error analysis:** Tool must generate:
  - Error distribution by feature values
  - Hardest examples (highest loss)
  - Prediction confidence vs correctness
  - Systematic failure patterns
- **Critic requirement:** Can't mark experiment complete without error analysis
- **Error-first presentation:** Show worst failures before best successes

**Detection:**
- Can describe accuracy but not failure modes
- Model fails on deployment and team is surprised

---

### Pitfall 10: Configuration Sprawl

**What goes wrong:**
Every experiment has slightly different config file format. No standard for specifying data paths, model architecture, training hyperparameters.

**Examples:**
- Mixing command-line args, YAML files, Python dicts
- Hardcoded paths scattered through code
- No validation of config completeness
- Config changes between experiments not tracked

**Prevention:**
- **Schema-validated configs:** Tool enforces config structure
- **Templating system:** Start from validated baseline config
- **Config diffing:** Tool shows "what changed from experiment N to N+1"
- **Version control:** Configs committed with code

**Detection:**
- Can't run old experiment because config format changed
- Different team members use different config styles

---

## Minor Pitfalls

Annoyances that create friction but are easily fixed.

### Pitfall 11: Verbose Logging Without Structure

**What goes wrong:**
Training logs dump every metric every step. Impossible to extract signal from noise.

**Prevention:**
- Structured logging (JSON lines, not print statements)
- Configurable verbosity levels
- Summary statistics over epochs, not raw values

---

### Pitfall 12: No Environment Reproducibility

**What goes wrong:**
Code works but environment not captured. Different package versions cause subtle differences.

**Prevention:**
- Lock files (requirements.txt with versions, poetry.lock)
- Container definitions (Dockerfile)
- Environment export with every experiment

---

### Pitfall 13: Forgetting to Track Data Versions

**What goes wrong:**
Data changes over time but not versioned. Can't reproduce experiment because underlying data shifted.

**Prevention:**
- Data version hashing or DVC integration
- Track data pipeline code with experiments
- Immutable data snapshots for experiments

---

## Phase-Specific Warnings

| Phase | Likely Pitfall | Mitigation |
|-------|---------------|------------|
| Data Reconnaissance | Ignoring temporal structure → leakage | Explorer must document time dependencies explicitly |
| Hypothesis Synthesis | Untestable hypothesis | Architect must specify falsification criteria |
| Researcher (implementation) | Notebook code without refactor path | Separate exploration notebooks from validated scripts |
| Critic (validation) | Checking metrics without checking distribution | Critic must validate data assumptions, not just results |
| Evaluator (benchmarking) | Single aggregate metric | Report stratified metrics automatically |
| Human Evaluation | Confirmation bias | Explicitly require evidence package with negative results |

---

## GRD-Specific Risks

Based on the project architecture, here are pitfalls specific to GRD's design:

### Risk 1: Infinite Recursive Loops

**Problem:** Critic sends back to Explorer, Explorer produces same report, loop never converges.

**Prevention:**
- Maximum recursion depth (e.g., 3 loops)
- Force new information requirement: "What's different this time?"
- Human escalation after N loops

---

### Risk 2: Critic Becomes Adversarial Theater

**Problem:** Critic always finds issues to justify its existence, slowing down valid research.

**Prevention:**
- Critic must provide *actionable* feedback (not just "be more careful")
- Exit code justification required
- False positive tracking (if Critic blocks valid work, adjust sensitivity)

---

### Risk 3: Hypothesis Drift

**Problem:** Original hypothesis morphs through recursive iterations until results are "good" but hypothesis no longer matches.

**Prevention:**
- Lock original hypothesis in OBJECTIVE.md
- Track hypothesis modifications explicitly
- Human gate requires: "Did we answer the original question or change the question?"

---

### Risk 4: Data Reconnaissance Becomes EDA Busywork

**Problem:** Explorer produces 50-page reports of every distribution and correlation without insight.

**Prevention:**
- Focus Explorer on *anomalies* and *risks*, not comprehensive statistics
- Maximum report length
- Critic validates: "Did Explorer surface leakage risks and baseline signals?"

---

### Risk 5: Scorecard Gaming

**Problem:** Evaluator produces SCORECARD.json that looks good but doesn't capture true performance.

**Prevention:**
- Architect pre-specifies metrics in OBJECTIVE.md (Evaluator can't choose post-hoc)
- Scorecard must include worst-case performance, not just average
- Confidence intervals required, not point estimates

---

## Sources

**Confidence Level:** MEDIUM

This analysis is based on:
- Established ML engineering best practices (data leakage patterns, evaluation pitfalls)
- Common failures documented in ML research (replication crisis, publication bias)
- Known anti-patterns in experiment tracking tools (MLflow, Weights & Biases usage patterns)

**Verification status:**
- WebSearch unavailable during research session
- Based on ML engineering principles from training knowledge (as of January 2025)
- Patterns validated against GRD's specific architecture (Critic agent, recursive loops)

**Recommendations for validation:**
- Cross-reference specific tools: MLflow, Weights & Biases, Neptune.ai documentation on best practices
- Review ML reproducibility papers for empirical evidence of these pitfalls
- Consult ML research teams for real-world failure modes

**Limitations:**
- Unable to verify against 2026 current tools or recent case studies
- Some pitfalls may be less relevant with modern tool improvements
- Phase mappings are specific to GRD architecture and may need adjustment

---

**Last Updated:** 2026-01-27
