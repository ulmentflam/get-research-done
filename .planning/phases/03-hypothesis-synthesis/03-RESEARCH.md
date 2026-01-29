# Phase 3: Hypothesis Synthesis - Research

**Researched:** 2026-01-28
**Domain:** Scientific hypothesis formulation, ML experiment design, falsification criteria
**Confidence:** MEDIUM

## Summary

Hypothesis synthesis for ML experiments requires balancing scientific rigor with practical flexibility. Recent research (2025-2026) shows increasing formalization of hypothesis generation using LLMs, with emphasis on falsification criteria, structured evaluation methodologies, and transparent baseline comparisons. The key insight is that hypothesis testing is highly formalized, but hypothesis generation remains largely informal—creating opportunity for guided, conversational synthesis.

**Key findings:**
- **LLM-based hypothesis synthesis** is emerging as a formal process (Chicago Human+AI lab, January 2026) with data-driven + literature-based refinement
- **Iterative refinement frameworks** (POPPER, self-reflective prompting) enable conversational improvement with 5-15 iterations typical
- **Falsification criteria** are becoming machine-readable (Lakens & DeBruine 2020), with automated frameworks validating hypotheses
- **Evaluation methodology upfront** prevents p-hacking and establishes clear success criteria
- **Baseline requirements** are increasingly scrutinized—EMBRACE and REFORMS checklists emphasize comparable, well-optimized baselines
- **Markdown templates** for scientific documents exist but no standard OBJECTIVE.md format—opportunity to define domain-specific structure

**Primary recommendation:** Build conversational Architect agent using iterative refinement pattern (propose → user feedback → refine), generate OBJECTIVE.md with structured sections (context, hypothesis, metrics, baselines, falsification), validate using schema-based frontmatter checking, and provide flexible prose format with required elements rather than rigid scientific template.

## Standard Stack

The established libraries/tools for hypothesis synthesis and experiment design:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pydantic | 2.10+ | Data validation, schema definition | De facto standard for Python data validation, JSON schema generation |
| pyyaml | 6.0.1 | YAML parsing for frontmatter | Standard YAML library, required for markdown frontmatter |
| markdown-it-py | 3.0+ | Markdown parsing | Fast, CommonMark-compliant parser with plugin support |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| scikit-learn | 1.8.0 | Cross-validation utilities, baseline models | K-fold, stratified sampling, simple baselines |
| scipy | 1.14+ | Statistical tests (t-test, chi-square) | Statistical significance testing, falsification validation |
| anthropic | 0.48+ | Claude API for conversational refinement | Interactive hypothesis refinement, advisor-like dialogue |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pydantic | marshmallow | Marshmallow more verbose, pydantic has JSON schema generation |
| markdown-it-py | mistune | Mistune faster but less extensible, markdown-it has plugin ecosystem |
| scikit-learn baselines | custom implementations | Custom code misses edge cases, sklearn baselines well-tested |
| conversational refinement | one-shot generation | One-shot lacks user guidance, iterative allows correction |

**Installation:**
```bash
# Core validation and parsing
pip install pydantic>=2.10.0 pyyaml==6.0.1 markdown-it-py>=3.0.0

# ML evaluation and statistical testing
pip install scikit-learn>=1.8.0 scipy>=1.14.0

# Conversational refinement (if using Claude API)
pip install anthropic>=0.48.0
```

## Architecture Patterns

### Recommended Project Structure
```
grd_agents/
├── architect/                    # Hypothesis synthesis agent
│   ├── __init__.py
│   ├── synthesizer.py            # Core hypothesis generation logic
│   ├── refiner.py                # Iterative refinement loop
│   ├── schemas.py                # OBJECTIVE.md schema definitions
│   ├── validator.py              # Frontmatter and content validation
│   └── advisor.py                # Conversational advisor interface
└── shared/
    ├── templates/
    │   └── objective.md          # OBJECTIVE.md template
    └── validation/
        └── schemas.py            # Shared schema definitions
```

### Pattern 1: Iterative Conversational Refinement
**What:** LLM proposes hypothesis → user provides feedback → LLM refines → repeat until convergence
**When to use:** User wants guidance but has domain knowledge to steer direction
**Example:**
```python
# Source: Chicago Human+AI lab hypothesis generation research (2026)
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class HypothesisProposal:
    hypothesis: str
    rationale: str
    expected_outcome: str
    confidence: str  # HIGH/MEDIUM/LOW
    data_constraints: List[str]
    iteration: int

class IterativeArchitect:
    def __init__(self, data_report_path: Optional[str] = None):
        self.data_report = self._load_data_report(data_report_path) if data_report_path else None
        self.iteration = 0
        self.max_iterations = 15  # Typical convergence: 5-15 iterations

    def propose_hypothesis(self, user_direction: Optional[str] = None) -> HypothesisProposal:
        """Generate hypothesis proposal from data insights or user direction."""
        self.iteration += 1

        # If user provides direction, use it; otherwise synthesize from data
        if user_direction:
            hypothesis = self._synthesize_from_direction(user_direction)
        elif self.data_report:
            hypothesis = self._synthesize_from_data_report(self.data_report)
        else:
            raise ValueError("Need either data_report or user_direction")

        return HypothesisProposal(
            hypothesis=hypothesis,
            rationale=self._explain_reasoning(hypothesis),
            expected_outcome=self._predict_outcome(hypothesis),
            confidence=self._assess_confidence(hypothesis),
            data_constraints=self._extract_constraints(self.data_report),
            iteration=self.iteration
        )

    def refine_hypothesis(self, proposal: HypothesisProposal,
                         user_feedback: str) -> HypothesisProposal:
        """Refine hypothesis based on user feedback."""
        self.iteration += 1

        # Apply user feedback to refine
        refined = self._apply_feedback(proposal, user_feedback)

        return HypothesisProposal(
            hypothesis=refined.hypothesis,
            rationale=refined.rationale,
            expected_outcome=refined.expected_outcome,
            confidence=refined.confidence,
            data_constraints=refined.data_constraints,
            iteration=self.iteration
        )

    def has_converged(self, proposal: HypothesisProposal, user_feedback: str) -> bool:
        """Check if user accepts proposal or max iterations reached."""
        return (
            "accept" in user_feedback.lower() or
            "looks good" in user_feedback.lower() or
            self.iteration >= self.max_iterations
        )
```

### Pattern 2: OBJECTIVE.md Schema with Pydantic
**What:** Define structured schema for OBJECTIVE.md with validation rules
**When to use:** Need to enforce required fields and validate user-written or LLM-generated objectives
**Example:**
```python
# Source: Pydantic 2.10+ validation patterns
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional
from datetime import datetime

class SuccessMetric(BaseModel):
    name: str = Field(..., description="Metric name (e.g., F1-score, RMSE)")
    threshold: float = Field(..., description="Success threshold value")
    comparison: Literal["greater_than", "less_than"] = Field(..., description="How to compare")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Metric weight in composite score")

    @field_validator('name')
    @classmethod
    def validate_metric_name(cls, v: str) -> str:
        allowed = ['accuracy', 'f1', 'precision', 'recall', 'auc-roc', 'rmse', 'mae', 'r2']
        if v.lower() not in allowed:
            raise ValueError(f"Metric must be one of: {allowed}")
        return v.lower()

class FalsificationCriteria(BaseModel):
    metric: str = Field(..., description="Metric to monitor for falsification")
    threshold: float = Field(..., description="Threshold that falsifies hypothesis")
    comparison: Literal["greater_than", "less_than"] = Field(...)
    type: Literal["quantitative", "qualitative"] = Field(default="quantitative")
    explanation: str = Field(..., description="What falsification means scientifically")

class Baseline(BaseModel):
    type: Literal["own_implementation", "literature_citation"] = Field(...)
    description: str = Field(..., description="What baseline is")
    expected_performance: Optional[float] = Field(None, description="Expected metric value")
    citation: Optional[str] = Field(None, description="Literature citation if applicable")

    @field_validator('citation')
    @classmethod
    def require_citation_for_literature(cls, v: Optional[str], info) -> Optional[str]:
        if info.data.get('type') == 'literature_citation' and not v:
            raise ValueError("Literature baselines require citation")
        return v

class EvaluationMethodology(BaseModel):
    strategy: Literal["k-fold", "stratified-k-fold", "time-series-split", "holdout"] = Field(...)
    k_folds: Optional[int] = Field(None, ge=2, le=20, description="Number of folds for k-fold CV")
    test_size: Optional[float] = Field(None, ge=0.1, le=0.5, description="Test set proportion for holdout")
    random_state: int = Field(default=42, description="Random seed for reproducibility")

    @field_validator('k_folds')
    @classmethod
    def require_k_for_kfold(cls, v: Optional[int], info) -> Optional[int]:
        strategy = info.data.get('strategy', '')
        if 'k-fold' in strategy and not v:
            raise ValueError("k-fold strategies require k_folds parameter")
        return v

class ObjectiveDocument(BaseModel):
    """Schema for OBJECTIVE.md frontmatter validation."""

    # Metadata
    created: datetime = Field(default_factory=datetime.now)
    phase: int = Field(default=3, description="Phase number")

    # Context
    context: str = Field(..., min_length=50, description="Background and motivation")

    # Hypothesis
    hypothesis: str = Field(..., min_length=20, description="What, why, expected outcome")

    # Success Metrics
    metrics: List[SuccessMetric] = Field(..., min_items=1, description="Success metrics with weights")

    # Evaluation
    evaluation: EvaluationMethodology = Field(..., description="How hypothesis will be tested")

    # Baselines
    baselines: List[Baseline] = Field(default_factory=list, description="Comparison baselines")

    # Falsification
    falsification_criteria: List[FalsificationCriteria] = Field(
        ..., min_items=1, description="What would disprove hypothesis"
    )

    # Optional
    constraints: Optional[List[str]] = Field(None, description="Known limitations")
    non_goals: Optional[List[str]] = Field(None, description="Explicit exclusions")

    @field_validator('metrics')
    @classmethod
    def validate_metric_weights(cls, v: List[SuccessMetric]) -> List[SuccessMetric]:
        total_weight = sum(m.weight for m in v)
        if not (0.99 <= total_weight <= 1.01):  # Allow float precision tolerance
            raise ValueError(f"Metric weights must sum to 1.0, got {total_weight}")
        return v

    def to_markdown(self) -> str:
        """Generate OBJECTIVE.md content from schema."""
        # Implementation would generate markdown from validated data
        pass
```

### Pattern 3: Baseline Warning System
**What:** Warn but don't block if baseline is undefined; provide guidance on options
**When to use:** User may not have baseline yet, but system should encourage one
**Example:**
```python
# Source: EMBRACE/REFORMS checklist requirements
from typing import Optional
from dataclasses import dataclass

@dataclass
class BaselineCheck:
    has_baseline: bool
    baseline_type: Optional[str]  # "own", "literature", None
    severity: str  # "WARNING", "INFO"
    message: str
    recommendations: list[str]

def check_baseline_definition(objective: ObjectiveDocument) -> BaselineCheck:
    """Soft gate: warn if baseline missing but allow proceeding."""

    if not objective.baselines or len(objective.baselines) == 0:
        return BaselineCheck(
            has_baseline=False,
            baseline_type=None,
            severity="WARNING",
            message="No baseline defined. Cannot claim improvement without comparison point.",
            recommendations=[
                "Option 1: Run your own baseline (simple model like logistic regression, decision tree)",
                "Option 2: Cite literature baseline for this task/dataset",
                "Option 3: Establish random/majority-class baseline for lower bound",
                "If baseline definition requires more data exploration, run /grd:explore first"
            ]
        )

    # Check baseline quality
    own_baselines = [b for b in objective.baselines if b.type == "own_implementation"]
    lit_baselines = [b for b in objective.baselines if b.type == "literature_citation"]

    if own_baselines:
        return BaselineCheck(
            has_baseline=True,
            baseline_type="own",
            severity="INFO",
            message=f"✓ {len(own_baselines)} own baseline(s) defined",
            recommendations=[
                "Ensure baseline uses same data preprocessing as experiment",
                "Document baseline hyperparameters for reproducibility",
                "Consider adding literature baseline for comparison"
            ]
        )

    if lit_baselines:
        return BaselineCheck(
            has_baseline=True,
            baseline_type="literature",
            severity="INFO",
            message=f"✓ {len(lit_baselines)} literature baseline(s) cited",
            recommendations=[
                "Verify literature baseline uses comparable data/task",
                "Note any differences in evaluation methodology",
                "Consider running own baseline to validate literature claims"
            ]
        )

    return BaselineCheck(
        has_baseline=False,
        baseline_type=None,
        severity="WARNING",
        message="Baseline definition incomplete",
        recommendations=["Review baseline requirements in OBJECTIVE.md template"]
    )
```

### Pattern 4: Composite Weighted Scoring
**What:** Calculate weighted average of multiple metrics for hypothesis success
**When to use:** Multiple metrics with different importance levels
**Example:**
```python
# Source: scikit-learn scoring patterns + weighted metrics research
from typing import Dict, List
import numpy as np

class CompositeScorer:
    """Calculate weighted composite score from multiple metrics."""

    def __init__(self, metrics: List[SuccessMetric]):
        self.metrics = metrics
        self._validate_weights()

    def _validate_weights(self):
        """Ensure weights sum to 1.0."""
        total = sum(m.weight for m in self.metrics)
        if not np.isclose(total, 1.0, atol=1e-6):
            raise ValueError(f"Metric weights must sum to 1.0, got {total}")

    def calculate_score(self, results: Dict[str, float]) -> Dict:
        """
        Calculate composite score and per-metric success.

        Args:
            results: Dict mapping metric name to value

        Returns:
            Dict with composite_score, per_metric_success, overall_success
        """
        composite_score = 0.0
        per_metric_success = {}

        for metric in self.metrics:
            if metric.name not in results:
                raise ValueError(f"Missing result for metric: {metric.name}")

            value = results[metric.name]

            # Check if metric meets threshold
            if metric.comparison == "greater_than":
                success = value >= metric.threshold
            else:  # less_than
                success = value <= metric.threshold

            per_metric_success[metric.name] = success

            # Contribute to weighted score only if threshold met
            # (Alternative: contribute proportional amount regardless of threshold)
            if success:
                composite_score += metric.weight

        return {
            'composite_score': composite_score,
            'per_metric_success': per_metric_success,
            'overall_success': composite_score >= 0.5,  # Majority of weighted metrics
            'metrics_passed': sum(per_metric_success.values()),
            'metrics_total': len(self.metrics)
        }

    def explain_score(self, results: Dict[str, float]) -> str:
        """Generate human-readable explanation of scoring."""
        score_info = self.calculate_score(results)

        explanation = f"Composite Score: {score_info['composite_score']:.2f}\n"
        explanation += f"Overall Success: {'✓' if score_info['overall_success'] else '✗'}\n\n"
        explanation += "Per-Metric Breakdown:\n"

        for metric in self.metrics:
            value = results[metric.name]
            success = score_info['per_metric_success'][metric.name]
            symbol = '✓' if success else '✗'

            explanation += f"  {symbol} {metric.name}: {value:.4f} "
            explanation += f"({'≥' if metric.comparison == 'greater_than' else '≤'} {metric.threshold}) "
            explanation += f"[weight: {metric.weight:.2f}]\n"

        return explanation
```

### Pattern 5: Falsification Routing Decision
**What:** When falsification criteria met, Critic decides routing (REVISE_DATA, REVISE_METHOD, human)
**When to use:** Hypothesis fails; need to determine root cause
**Example:**
```python
# Source: Phase 4 routing logic (LOOP-05 requirement)
from enum import Enum
from typing import List, Optional

class FalsificationRouting(Enum):
    REVISE_DATA = "revise_data"      # Data quality issue
    REVISE_METHOD = "revise_method"  # Method selection issue
    HUMAN_REVIEW = "human_review"    # Requires expert judgment

class FalsificationAnalyzer:
    """Analyzes falsification and determines routing."""

    def analyze(self,
                falsification_criteria: List[FalsificationCriteria],
                results: Dict[str, float],
                data_report_path: Optional[str] = None) -> FalsificationRouting:
        """
        Determine routing when hypothesis is falsified.

        Logic:
        - If data quality issues flagged in DATA_REPORT.md → REVISE_DATA
        - If method likely inappropriate for task → REVISE_METHOD
        - If unclear cause → HUMAN_REVIEW
        """

        # Check which criteria are falsified
        falsified = []
        for criterion in falsification_criteria:
            value = results.get(criterion.metric)
            if value is None:
                continue

            if criterion.comparison == "greater_than" and value > criterion.threshold:
                falsified.append(criterion)
            elif criterion.comparison == "less_than" and value < criterion.threshold:
                falsified.append(criterion)

        if not falsified:
            return None  # Hypothesis not falsified

        # Analyze root cause
        if self._suggests_data_issue(falsified, data_report_path):
            return FalsificationRouting.REVISE_DATA

        if self._suggests_method_issue(falsified):
            return FalsificationRouting.REVISE_METHOD

        return FalsificationRouting.HUMAN_REVIEW

    def _suggests_data_issue(self,
                            falsified: List[FalsificationCriteria],
                            data_report_path: Optional[str]) -> bool:
        """Check if falsification likely due to data quality."""
        if not data_report_path:
            return False

        # Load DATA_REPORT.md and check for:
        # - High leakage risk features
        # - Missing data patterns
        # - Class imbalance
        # - Train-test overlap

        # Placeholder logic
        return False  # Implement based on DATA_REPORT.md content

    def _suggests_method_issue(self, falsified: List[FalsificationCriteria]) -> bool:
        """Check if falsification likely due to inappropriate method."""
        # Heuristics:
        # - All metrics far from threshold → wrong method family
        # - Some metrics good, others bad → hyperparameter issue

        # Placeholder logic
        return False  # Implement based on metric patterns
```

### Anti-Patterns to Avoid

- **Rigid hypothesis template:** Users need flexibility; enforce required elements but allow prose format
- **No baseline requirement:** Always warn if baseline missing; comparison is essential for claims
- **Single metric success:** Multiple weighted metrics prevent gaming/overfitting to single target
- **Post-hoc metric selection:** Evaluation methodology must be defined upfront in OBJECTIVE.md
- **No falsification criteria:** Without falsification, experiment is unfalsifiable (unscientific)
- **Ignoring data constraints:** DATA_REPORT.md findings must inform hypothesis constraints
- **Skipping user iteration:** One-shot generation misses domain knowledge; iterate with user
- **Blocking on incomplete info:** Soft gates allow proceeding with warnings, user decides

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML frontmatter parsing | Custom regex parser | pyyaml + markdown-it-py | Edge cases in YAML syntax, nested structures, encoding issues |
| Schema validation | Manual dict checking | pydantic with field validators | Type coercion, nested validation, clear error messages |
| Cross-validation strategies | Custom train/test splitting | scikit-learn model_selection | Stratification, time-aware splits, reproducibility built-in |
| Statistical significance tests | Custom t-test implementation | scipy.stats | Handles missing data, small samples, multiple test types |
| Composite scoring | Manual weighted average | Structured scorer with validation | Weight normalization, threshold logic, clear explanations |
| Markdown template rendering | String concatenation | Jinja2 or f-strings with dataclass | Maintainability, escaping, readability |
| Conversational refinement | One-shot prompt | Iterative loop with state | Convergence tracking, user feedback integration, iteration limits |

**Key insight:** Hypothesis synthesis requires careful balance between structure (validation, required fields) and flexibility (prose format, user discretion). Use well-tested libraries for validation and statistical testing; build custom conversational flow for domain-specific iteration.

## Common Pitfalls

### Pitfall 1: Over-Constraining Hypothesis Format
**What goes wrong:** Users frustrated by rigid template; can't express hypothesis naturally
**Why it happens:** Temptation to enforce scientific paper format (null/alternative, formal statement)
**How to avoid:**
- Allow prose format with required elements (what, why, expected outcome)
- Validate presence of elements, not exact structure
- Show examples with varied formats, not single template
- Let Architect propose format that matches hypothesis type
**Warning signs:** Users bypass Architect to write OBJECTIVE.md directly, complaints about inflexibility

### Pitfall 2: Missing Evaluation Methodology Upfront
**What goes wrong:** User defines metrics but not how they'll be evaluated; enables p-hacking
**Why it happens:** Evaluation methodology feels like implementation detail, not hypothesis concern
**How to avoid:**
- Require evaluation methodology (k-fold/holdout/time-series) in OBJECTIVE.md
- Explain why upfront definition prevents cherry-picking results
- Architect proposes appropriate methodology based on data characteristics
- Validate that methodology matches task type (no k-fold for time series)
**Warning signs:** Results change dramatically with different CV strategies, post-hoc methodology changes

### Pitfall 3: Weak or Missing Baselines
**What goes wrong:** Claim improvements without comparable baseline; results not credible
**Why it happens:** Running baselines feels tedious; literature baselines may not exist
**How to avoid:**
- Warn (don't block) if baseline undefined
- Provide templates for simple baselines (majority class, mean prediction, linear model)
- Explain that EMBRACE/REFORMS checklists require baseline reporting
- Architect suggests baseline appropriate for task
**Warning signs:** Claimed performance gains but no reference point, literature comparisons with different eval methods

### Pitfall 4: Quantitative Metrics Without Statistical Significance
**What goes wrong:** Report metric improvements that aren't statistically significant; overfitting to random variation
**Why it happens:** ML community often reports single scores without confidence intervals or significance tests
**How to avoid:**
- Require multiple runs or cross-validation (not single train/test split)
- Include statistical significance testing in evaluation methodology
- Report confidence intervals or standard deviations with metrics
- Architect warns if single-run evaluation planned
**Warning signs:** Metric improvements <1%, high variance across runs, no error bars

### Pitfall 5: Falsification Criteria Too Lenient
**What goes wrong:** Hypothesis never falsified; confirmation bias prevents learning
**Why it happens:** Setting falsification thresholds requires predicting when hypothesis is clearly wrong
**How to avoid:**
- Architect proposes symmetric or asymmetric thresholds based on risk
- Explain that lenient criteria make hypothesis unfalsifiable (unscientific)
- Suggest quantitative thresholds where possible, qualitative only when necessary
- Include "worse than baseline" as minimum falsification criterion
**Warning signs:** Hypothesis "succeeds" but results are unimpressive, no experiments falsified ever

### Pitfall 6: Ignoring Data Constraints
**What goes wrong:** Hypothesis doesn't account for data quality issues flagged in DATA_REPORT.md
**Why it happens:** DATA_REPORT.md is optional input; user may skip Phase 2
**How to avoid:**
- Load DATA_REPORT.md if exists, extract constraints
- Include data constraints in OBJECTIVE.md (e.g., "excludes Feature X due to leakage")
- Architect references specific findings when proposing hypothesis
- Warn if high-risk features would be used in hypothesis
**Warning signs:** Leakage features used in experiment, temporal ordering violated

### Pitfall 7: No Iteration with User
**What goes wrong:** Architect generates hypothesis in one shot; misses user's domain knowledge
**Why it happens:** One-shot generation is simpler to implement than conversational loop
**How to avoid:**
- Always propose hypothesis first, await user feedback
- Support iteration: user can request alternatives, provide direction, refine elements
- Track iteration count, converge within 5-15 iterations typically
- Explain Architect's reasoning so user can provide informed feedback
**Warning signs:** User rewrites Architect's output extensively, complaints about misunderstanding task

## Code Examples

Verified patterns from official sources:

### K-Fold Cross-Validation Setup
```python
# Source: scikit-learn 1.8.0 documentation
from sklearn.model_selection import (
    KFold, StratifiedKFold, TimeSeriesSplit, cross_validate
)

def setup_cross_validation(strategy: str, n_folds: int = 5, random_state: int = 42):
    """Configure cross-validation strategy for evaluation methodology."""

    if strategy == "k-fold":
        return KFold(n_splits=n_folds, shuffle=True, random_state=random_state)

    elif strategy == "stratified-k-fold":
        # For classification with class imbalance
        return StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)

    elif strategy == "time-series-split":
        # For temporal data - no shuffle, respects time ordering
        return TimeSeriesSplit(n_splits=n_folds)

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

# Usage in evaluation
def evaluate_with_cv(model, X, y, cv_strategy, scoring_metrics):
    """Evaluate model using specified CV strategy."""
    cv = setup_cross_validation(
        strategy=cv_strategy.strategy,
        n_folds=cv_strategy.k_folds,
        random_state=cv_strategy.random_state
    )

    # Cross-validate with multiple metrics
    scores = cross_validate(
        model, X, y, cv=cv,
        scoring=scoring_metrics,  # Dict of metric names to scorers
        return_train_score=True,
        n_jobs=-1  # Parallel execution
    )

    return scores
```

### Statistical Significance Testing
```python
# Source: scipy.stats documentation + ML best practices
from scipy import stats
import numpy as np

def compare_models_paired_ttest(model1_scores: np.ndarray,
                                model2_scores: np.ndarray,
                                alpha: float = 0.05) -> dict:
    """
    Compare two models using paired t-test on CV scores.

    Args:
        model1_scores: Array of CV scores for model 1
        model2_scores: Array of CV scores for model 2
        alpha: Significance level (default 0.05)

    Returns:
        Dict with test results
    """
    # Paired t-test (scores from same folds)
    t_stat, p_value = stats.ttest_rel(model1_scores, model2_scores)

    # Effect size (Cohen's d)
    mean_diff = np.mean(model1_scores - model2_scores)
    std_diff = np.std(model1_scores - model2_scores, ddof=1)
    cohens_d = mean_diff / std_diff if std_diff > 0 else 0.0

    # Confidence interval for mean difference
    se = std_diff / np.sqrt(len(model1_scores))
    ci_lower = mean_diff - 1.96 * se
    ci_upper = mean_diff + 1.96 * se

    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < alpha,
        'mean_difference': mean_diff,
        'cohens_d': cohens_d,
        'confidence_interval': (ci_lower, ci_upper),
        'interpretation': (
            f"Model 1 is {'significantly' if p_value < alpha else 'not significantly'} "
            f"better than Model 2 (p={p_value:.4f}, effect size={cohens_d:.3f})"
        )
    }

# Usage in falsification
def check_falsification_significance(results: dict,
                                     falsification_criterion: FalsificationCriteria,
                                     baseline_scores: np.ndarray,
                                     alpha: float = 0.05) -> bool:
    """Check if falsification is statistically significant."""

    experiment_scores = results['cv_scores'][falsification_criterion.metric]

    comparison = compare_models_paired_ttest(
        baseline_scores,
        experiment_scores,
        alpha=alpha
    )

    # Falsified if experiment significantly worse than baseline
    return comparison['significant'] and comparison['mean_difference'] < 0
```

### YAML Frontmatter Validation
```python
# Source: pyyaml + pydantic validation patterns
import yaml
from pathlib import Path
from typing import Tuple, Optional

def parse_and_validate_objective(file_path: Path) -> Tuple[ObjectiveDocument, str]:
    """
    Parse OBJECTIVE.md with YAML frontmatter and validate against schema.

    Returns:
        Tuple of (validated_data, markdown_content)
    """
    content = file_path.read_text(encoding='utf-8')

    # Split frontmatter and markdown content
    if not content.startswith('---\n'):
        raise ValueError("OBJECTIVE.md must start with YAML frontmatter (---)")

    parts = content.split('---\n', 2)
    if len(parts) < 3:
        raise ValueError("OBJECTIVE.md frontmatter not properly closed")

    frontmatter_text = parts[1]
    markdown_content = parts[2].strip()

    # Parse YAML frontmatter
    try:
        frontmatter_data = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter: {e}")

    # Validate against schema
    try:
        objective = ObjectiveDocument(**frontmatter_data)
    except Exception as e:
        raise ValueError(f"Validation failed: {e}")

    return objective, markdown_content

# Usage
def validate_objective_file(file_path: str) -> Optional[str]:
    """Validate OBJECTIVE.md, return error message if invalid."""
    try:
        objective, content = parse_and_validate_objective(Path(file_path))

        # Additional content checks
        if len(content) < 100:
            return "WARNING: Objective content is very short. Provide more context."

        # Check baseline warning
        baseline_check = check_baseline_definition(objective)
        if baseline_check.severity == "WARNING":
            return f"WARNING: {baseline_check.message}"

        return None  # Valid

    except ValueError as e:
        return f"ERROR: {str(e)}"
```

### Iterative Hypothesis Refinement Loop
```python
# Source: Chicago Human+AI lab hypothesis generation + iterative refinement research
from anthropic import Anthropic
from typing import Optional

class ConversationalArchitect:
    """LLM-based hypothesis synthesis with iterative refinement."""

    def __init__(self, data_report_path: Optional[str] = None):
        self.client = Anthropic()
        self.data_report = self._load_data_report(data_report_path) if data_report_path else None
        self.conversation_history = []
        self.iteration = 0
        self.max_iterations = 15

    def synthesize_hypothesis(self, user_direction: Optional[str] = None) -> str:
        """Initial hypothesis proposal."""

        system_prompt = self._build_system_prompt()
        user_message = self._build_initial_user_message(user_direction)

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        proposal = response.content[0].text
        self.conversation_history.append(("assistant", proposal))
        self.iteration += 1

        return proposal

    def refine_hypothesis(self, user_feedback: str) -> str:
        """Refine hypothesis based on user feedback."""

        if self.iteration >= self.max_iterations:
            return "Max iterations reached. Please finalize hypothesis or start over."

        self.conversation_history.append(("user", user_feedback))

        # Build refinement prompt
        refinement_prompt = f"""
        User feedback: {user_feedback}

        Please refine the hypothesis based on this feedback. Consider:
        1. What specific changes does the user want?
        2. Are there any concerns about feasibility or data constraints?
        3. Does the refined hypothesis maintain scientific rigor?

        Provide the refined hypothesis with explanation of changes.
        """

        messages = self._build_message_history() + [
            {"role": "user", "content": refinement_prompt}
        ]

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            system=self._build_system_prompt(),
            messages=messages
        )

        refined = response.content[0].text
        self.conversation_history.append(("assistant", refined))
        self.iteration += 1

        return refined

    def _build_system_prompt(self) -> str:
        """Build system prompt with role and constraints."""

        prompt = """You are a research advisor helping formulate testable ML hypotheses.

Your job:
1. Propose clear, testable hypotheses based on data insights
2. Explain reasoning and expected outcomes
3. Suggest appropriate metrics and evaluation methodology
4. Identify data constraints and limitations
5. Refine based on user feedback

Guidelines:
- Use flexible prose format (what, why, expected outcome)
- Ground in data characteristics from DATA_REPORT.md if available
- Propose falsification criteria
- Suggest baselines for comparison
- Be conversational but scientifically rigorous
"""

        if self.data_report:
            prompt += f"\n\nDATA CONTEXT:\n{self._summarize_data_report()}"

        return prompt

    def _build_initial_user_message(self, user_direction: Optional[str]) -> str:
        """Build initial user message for hypothesis synthesis."""

        if user_direction:
            return f"Help me formulate a hypothesis for: {user_direction}"
        elif self.data_report:
            return "Analyze the data insights and propose a testable hypothesis."
        else:
            return "I need help formulating a hypothesis. What information do you need?"

    def _build_message_history(self) -> list:
        """Convert conversation history to Claude message format."""
        messages = []
        for role, content in self.conversation_history:
            messages.append({"role": role, "content": content})
        return messages

    def _load_data_report(self, path: str) -> str:
        """Load DATA_REPORT.md content."""
        return Path(path).read_text(encoding='utf-8')

    def _summarize_data_report(self) -> str:
        """Extract key findings from DATA_REPORT.md."""
        # Parse markdown, extract:
        # - Data overview
        # - Leakage warnings (high confidence)
        # - Missing data patterns
        # - Class imbalance
        # - Constraints

        # Placeholder - implement markdown parsing
        return self.data_report[:1000] if self.data_report else ""
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual hypothesis formulation | LLM-assisted synthesis with data grounding | 2025-2026 | Systematic hypothesis generation, reduces bias, literature integration |
| Informal generation process | Iterative refinement frameworks (5-15 iterations) | January 2026 | Convergence tracking, user guidance, reproducible process |
| Post-hoc metric selection | Upfront evaluation methodology | 2024-2025 | Prevents p-hacking, pre-registered analysis plans |
| Single metric success | Weighted composite scoring | 2025-2026 | Reduces gaming, balances multiple objectives, clearer tradeoffs |
| Qualitative falsification | Machine-readable falsification criteria | 2020-2025 | Automated validation, transparent decision-making, POPPER framework |
| Weak baselines common | EMBRACE/REFORMS checklists enforce comparable baselines | 2024-2025 | Credible comparisons, reproducible research, reduced false claims |
| Rigid scientific templates | Flexible prose with required elements | Emerging 2025-2026 | User adoption, domain flexibility, maintains rigor |
| Statistical tests rare | Significance testing standard for model comparison | 2023-2025 | Confidence in results, effect size reporting, paired t-tests |

**Deprecated/outdated:**
- One-shot hypothesis generation: Replaced by iterative conversational refinement
- Null/alternative hypothesis formalism for ML: Too rigid, prose format with falsification criteria preferred
- Single train/test split: K-fold cross-validation or time-series splits now standard
- "Beats baseline" without statistical test: Must show significance, not just mean improvement

## Open Questions

Things that couldn't be fully resolved:

1. **Optimal number of success metrics**
   - What we know: Multiple metrics prevent gaming, but too many dilute focus
   - What's unclear: 2-3 metrics typical, but no research on optimal number
   - Recommendation: Support 1-5 metrics, warn if >5 (may indicate unclear hypothesis)

2. **Baseline caching strategy**
   - What we know: User decisions allow cached baseline results if config unchanged
   - What's unclear: How to validate "config unchanged" programmatically
   - Recommendation: Hash hyperparameters + data preprocessing + random seed, warn if hash differs

3. **OBJECTIVE.md as single file vs split**
   - What we know: No standard exists; some projects use single OBJECTIVE.md, others split into multiple docs
   - What's unclear: Single file easier to track, but multi-hypothesis projects may need split
   - Recommendation: Start with single OBJECTIVE.md, add multi-hypothesis support if needed

4. **Architect agent autonomy level**
   - What we know: User decisions specify "proposes, explains reasoning, accepts user override"
   - What's unclear: When should Architect push back on user vs defer to domain expertise?
   - Recommendation: Architect warns about data constraints/falsifiability issues but always allows override

5. **Falsification routing automation**
   - What we know: Critic decides REVISE_DATA vs REVISE_METHOD vs human review
   - What's unclear: Heuristics for automated routing decision
   - Recommendation: Start conservative (route to human), build heuristics from user feedback patterns

## Sources

### Primary (HIGH confidence)
- [Chicago Human+AI lab Hypothesis Generation](https://chicagohai.github.io/hypogenic-demo/) - LLM-based hypothesis synthesis with data grounding
- [Iterative Self-Reflective Prompt Engineering Framework (January 2026)](https://www.irjet.net/archives/V13/i1/IRJET-V13I0185.pdf) - Iterative refinement with 5-15 iteration convergence
- [Design Principles for Falsifiable ML Research](https://arxiv.org/html/2405.18077v1) - Falsification criteria in ML experiments
- [Machine-Readable Hypothesis Tests (Lakens & DeBruine 2020)](https://journals.sagepub.com/doi/10.1177/2515245920970949) - Structured falsification criteria
- [scikit-learn 1.8.0 Cross-Validation Documentation](https://scikit-learn.org/stable/modules/cross_validation.html) - K-fold, stratified, time-series CV
- [EMBRACE Checklist for ML Research](https://pubs.acs.org/doi/10.1021/acs.est.4c09611) - Baseline reporting requirements
- [REFORMS Recommendations for ML Science](https://www.science.org/doi/10.1126/sciadv.adk3452) - Best practices for experimental design
- [Pydantic 2.10+ Documentation](https://docs.pydantic.dev/) - Schema validation patterns

### Secondary (MEDIUM confidence)
- [POPPER: Automated Hypothesis Testing (GitHub)](https://github.com/snap-stanford/POPPER) - Sequential falsification framework
- [Statistical Hypothesis Testing Review (January 2026)](https://www.mdpi.com/2227-7390/14/2/300) - Contemporary statistical methods
- [K-Fold Selection Impact (2026 Nature)](https://www.nature.com/articles/s41598-026-37247-x) - Bias-variance tradeoffs
- [MLflow vs WandB Comparison](https://neptune.ai/vs/wandb-mlflow) - Experiment tracking tools
- [mdschema: Markdown Schema Validator](https://github.com/jackchuma/mdschema) - Frontmatter validation
- [remark-lint-frontmatter-schema](https://github.com/JulianCataldo/remark-lint-frontmatter-schema) - JSON Schema validation for YAML

### Tertiary (LOW confidence)
- WebSearch results on hypothesis structure 2026 - Multiple sources, cross-referenced
- WebSearch results on weighted metrics 2026 - Emerging practices, limited research
- WebSearch results on conversational AI agents 2026 - Fast-moving field, frameworks evolving

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - pydantic, scikit-learn, scipy verified from official docs
- Architecture patterns: MEDIUM - Iterative refinement well-researched, but OBJECTIVE.md format novel
- Pitfalls: MEDIUM - Based on ML best practices research and falsifiability principles
- Conversational refinement: MEDIUM - Chicago lab research recent (2026), pattern not yet widespread
- Baseline requirements: HIGH - EMBRACE/REFORMS checklists published, community adoption growing

**Research date:** 2026-01-28
**Valid until:** 2026-03-28 (60 days - LLM capabilities evolving rapidly, hypothesis synthesis patterns still emerging)

**Critical notes:**
- No standard OBJECTIVE.md format exists—opportunity to define domain-specific structure
- User decisions from CONTEXT.md constrain approach: flexible prose (not rigid template), weighted metrics, baseline optional but warned, both quantitative and qualitative falsification
- Iterative refinement pattern is very recent (January 2026)—monitor for emerging best practices
- Phase 3 feeds into Phase 4 validation loop—OBJECTIVE.md consumed by Researcher/Critic agents
- Statistical significance testing often skipped in ML—emphasize its importance for falsification
