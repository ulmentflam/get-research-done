# Phase 13: Accessible Insights - Research

**Researched:** 2026-02-01
**Domain:** Natural Language Generation for business intelligence reporting
**Confidence:** HIGH

## Summary

Phase 13 implements a `/grd:insights` command that transforms technical EDA output into plain English insights for business analyst audiences. This phase builds on Phase 12's Quick Explore by adding narrative generation, actionable recommendations, and LLM-ready prompts.

**Key findings:**
- Natural Language Generation (NLG) in business intelligence is standard in 2026, with PyNarrative emerging as the leading Python library
- Plain English explanations follow proven patterns: analogies, inline translations, and "What This Means" sections
- Action-oriented writing focuses on specific next steps rather than observations ("23% missing — decide: drop rows, fill values, or investigate")
- Jinja2 templates are ideal for structured narrative generation with conditional logic for severity-based language
- Executive summaries follow inverted pyramid format with TL;DR at top, scannable sections, and bold key findings
- LLM prompt engineering in 2026 favors zero-shot clear instructions over few-shot examples for modern models

**Primary recommendation:** Build narrative generation layer using Jinja2 templates with severity-aware conditional logic. Generate two outputs: comprehensive DATA_REPORT.md (saved to file) and INSIGHTS_SUMMARY.md (displayed in chat with Rich formatting). Use template-based approach for consistency, not LLM generation which adds latency and unpredictability.

## Standard Stack

The established libraries/tools for narrative generation from data:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Jinja2 | 3.1+ | Template engine for generating formatted text | Industry standard for Python text templating, used by Flask, Ansible, Sphinx |
| Rich | 14.1.0+ | Terminal formatting (from Phase 12) | Beautiful console output with markdown support |
| pandas | 2.2+ | Data manipulation (from Phase 12) | Foundation for all data operations |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| PyNarrative | 0.1+ | Automated narrative generation from DataFrames | If automated NLG from raw data is needed (optional) |
| inflect | 7.0+ | Natural language formatting (pluralization, numbers to words) | Converting "1 column" vs "2 columns" naturally |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Jinja2 | Python f-strings | f-strings lack conditional logic, require verbose if/else in Python code |
| Jinja2 | LLM generation (OpenAI/Anthropic) | LLM adds latency, cost, unpredictability; overkill for structured narratives |
| Template-based | PyNarrative auto-generation | PyNarrative good for charts, less control over tone/style for our use case |

**Installation:**
```bash
pip install Jinja2>=3.1.0 inflect>=7.0.0
# Rich and pandas already installed from Phase 12
```

## Architecture Patterns

### Recommended Project Structure
```
.claude/get-research-done/lib/
├── formatters.py        # Rich formatting (from Phase 12)
├── quick.py             # Quick explore (from Phase 12)
├── insights.py          # NEW: Insight generation orchestrator
└── templates/
    ├── data_report.md.j2       # Technical DATA_REPORT.md template
    └── insights_summary.md.j2  # Plain English INSIGHTS_SUMMARY.md template
```

### Pattern 1: Severity-Aware Narrative Generation
**What:** Use Jinja2 conditional logic to generate severity-appropriate language
**When to use:** All data quality findings, recommendations, warnings
**Example:**
```jinja2
{# Source: User CONTEXT + Jinja2 best practices #}
{% if missing_pct > 50 %}
🚨 **Critical:** {{ column }} has {{ missing_pct|round(1) }}% missing values —
this is severe. You'll need to decide: drop this column entirely, or investigate
why over half the data is missing.
{% elif missing_pct > 20 %}
⚠️ **Note:** {{ column }} has {{ missing_pct|round(1) }}% missing values.
Consider: (1) check if missingness correlates with other columns,
(2) median/mode imputation, or (3) drop rows with missing values.
{% else %}
✅ {{ column }} looks healthy with only {{ missing_pct|round(1) }}% missing.
{% endif %}
```

### Pattern 2: Inline Translation of Technical Terms
**What:** Technical term followed by plain English explanation in parentheses
**When to use:** Every statistical concept in insights output
**Example:**
```python
# Source: User CONTEXT decisions + statistical communication best practices

STAT_TRANSLATIONS = {
    'standard_deviation': 'Standard deviation (how spread out values are)',
    'skewness': 'Skewness (symmetry of distribution)',
    'correlation': 'Correlation (how strongly two things move together)',
    'cardinality': 'Cardinality (number of unique values)',
    'outliers': 'Outliers (extreme values far from typical)'
}

def explain_stat(stat_name: str, value: float, context: str) -> str:
    """Generate explanation with inline translation."""
    translated = STAT_TRANSLATIONS.get(stat_name, stat_name)

    if stat_name == 'standard_deviation':
        return f"{translated}: {value:.2f} — values typically range ±{value:.0f} from average"
    elif stat_name == 'skewness':
        if abs(value) < 0.5:
            return f"{translated}: {value:.2f} — roughly symmetric, like a bell curve"
        else:
            direction = "right (long tail of high values)" if value > 0 else "left (long tail of low values)"
            return f"{translated}: {value:.2f} — leans {direction}"
    # ... additional cases
```

### Pattern 3: Two-Output Strategy
**What:** Generate detailed technical report (saved) + plain English summary (displayed)
**When to use:** All insights generation commands
**Example:**
```python
# Source: User CONTEXT requirement for dual output

def generate_insights(df: pd.DataFrame, target_col: Optional[str] = None):
    """Generate both technical and accessible reports."""
    console = Console()

    # 1. Analyze data (same logic for both outputs)
    analysis = analyze_dataframe(df, target_col)

    # 2. Generate technical DATA_REPORT.md (comprehensive)
    technical_report = render_template(
        'data_report.md.j2',
        analysis=analysis,
        include_technical_details=True,
        include_statistics=True
    )
    Path('DATA_REPORT.md').write_text(technical_report)

    # 3. Generate plain English INSIGHTS_SUMMARY.md
    insights_summary = render_template(
        'insights_summary.md.j2',
        analysis=analysis,
        include_technical_details=False,
        include_what_this_means=True,
        include_recommendations=True
    )
    Path('INSIGHTS_SUMMARY.md').write_text(insights_summary)

    # 4. Display insights summary to console with Rich
    console.print(Markdown(insights_summary))

    console.print(f"\n[dim]📄 Full technical report saved to: DATA_REPORT.md[/dim]")
    console.print(f"[dim]📝 Plain English summary saved to: INSIGHTS_SUMMARY.md[/dim]")
```

### Pattern 4: Inverted Pyramid Structure
**What:** Most important information first, progressively more detailed
**When to use:** INSIGHTS_SUMMARY.md structure
**Example:**
```markdown
# Data Insights Summary

## TL;DR (3-second read)
[One sentence: most critical finding + immediate action]

## 5 Things to Know (30-second scan)
**Bold headlines that tell the story**
1. **[Finding]:** [What this means] [Action if needed]
2. ...

## Data Overview
[Brief stats: rows, columns, memory]

## Key Findings
[Detailed sections with "What This Means" for each]

## Recommendations
[Specific, actionable next steps with severity flags]

## Dig Deeper (LLM Prompts)
[3-5 copy-paste ready prompts]
```

### Pattern 5: Action-Oriented Recommendations
**What:** Specific next steps with examples, not generic advice
**When to use:** All recommendation sections
**Example:**
```jinja2
{# Source: User CONTEXT + data storytelling best practices #}
{% if high_missing_cols %}
## Missing Data Strategy

{% for col, pct in high_missing_cols %}
**{{ col }} ({{ pct|round(1) }}% missing)**

You'll need to decide:
1. **Drop rows:** If missing data is random, lose {{ (n_rows * pct / 100)|int|format_number }} rows
2. **Impute:** Fill with {{ recommend_imputation(col) }} (median for numerical, mode for categorical)
3. **Investigate:** Check if missingness correlates with {{ suggest_related_cols(col) }}

Example code:
```python
# Option 1: Drop rows
df_clean = df.dropna(subset=['{{ col }}'])

# Option 2: Impute
df['{{ col }}'].fillna(df['{{ col }}'].median(), inplace=True)
```
{% endfor %}
{% endif %}
```

### Pattern 6: LLM Prompt Generation
**What:** Create 3-5 copy-paste ready prompts focused on highest-value questions
**When to use:** End of insights summary
**Example:**
```python
# Source: User CONTEXT + 2026 prompt engineering best practices

def generate_llm_prompts(analysis: Dict[str, Any]) -> List[str]:
    """Generate contextual prompts based on findings."""
    prompts = []

    # Critical issues → investigation prompts
    if analysis['critical_issues']:
        issue = analysis['critical_issues'][0]
        prompts.append(
            f"I have a dataset with {analysis['n_rows']:,} rows where "
            f"the '{issue['column']}' column has {issue['pct']:.1f}% missing values. "
            f"What are the possible causes of this much missing data, and how should I decide "
            f"whether to drop the column, drop rows, or impute values?"
        )

    # Target variable → prediction prompts
    if analysis['target_col']:
        prompts.append(
            f"I'm trying to predict '{analysis['target_col']}' from this data. "
            f"Based on the features available, what modeling approaches would work best? "
            f"What feature engineering should I consider?"
        )

    # Outliers → analysis prompts
    if analysis['outlier_cols']:
        col = analysis['outlier_cols'][0]
        prompts.append(
            f"My '{col}' column has {analysis['outlier_pcts'][col]:.1f}% outliers "
            f"(values beyond 3 standard deviations). Should I remove these, cap them, "
            f"or leave them? How do I decide?"
        )

    # Always include: general exploration prompt
    prompts.append(
        f"I have a dataset with {analysis['n_rows']:,} rows and {analysis['n_cols']} columns. "
        f"What exploratory visualizations should I create to understand relationships between variables?"
    )

    return prompts[:5]  # Max 5 prompts per CONTEXT
```

### Anti-Patterns to Avoid

- **Using technical jargon without translation:** Every term must have plain English explanation
- **Generic recommendations:** "Consider handling missing values" → specify HOW with examples
- **Burying the lede:** Most important finding must be in TL;DR, not buried in middle
- **Over-explaining trivial findings:** "Dataset has 1000 rows" doesn't need "What This Means"
- **LLM generation for structured output:** Adds latency and unpredictability; use templates

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Text templating with conditionals | String concatenation with if/else | Jinja2 | Template engine handles escaping, whitespace, complex logic cleanly |
| Number formatting | Manual formatting logic | inflect library | Handles edge cases: "1 column" vs "2 columns", "21st" vs "22nd" |
| Markdown rendering in terminal | ANSI codes manually | Rich.Markdown | Handles heading styles, code blocks, lists automatically |
| Statistical explanations | Custom descriptions | Template library + analogies | Consistency across all outputs, easier to improve |
| Prompt engineering | Ad-hoc string building | Template-based with context injection | Ensures prompts are well-structured, self-contained |

**Key insight:** Narrative generation is fundamentally a templating problem, not an NLP/LLM problem. Use templates for structure and consistency, reserve LLMs for when user needs to generate novel analysis.

## Common Pitfalls

### Pitfall 1: Over-Explaining Simple Concepts
**What goes wrong:** Every statistic gets verbose explanation, output becomes tedious
**Why it happens:** Following "explain everything" requirement too literally
**How to avoid:** Scale explanation depth to complexity. Row count needs one line, leakage needs paragraphs
**Warning signs:** Insights summary exceeds 3 pages for small dataset

**From research:** Audiences scan, don't read. Bold key findings, keep paragraphs 2-3 sentences max.

### Pitfall 2: Technical Jargon Slipping Through
**What goes wrong:** Terms like "cardinality," "skewness," "z-score" appear without translation
**Why it happens:** Developer writes template, doesn't think from business analyst perspective
**How to avoid:** Every statistical term gets inline translation pattern: "Term (plain English)"
**Warning signs:** Need to explain what something means when sharing output

**From research:** Use common words and phrases that convey meaning and intuition, avoid acronyms and symbols.

### Pitfall 3: Vague Recommendations
**What goes wrong:** "Consider handling missing values" without specific guidance
**Why it happens:** Trying to be general-purpose, avoiding prescriptive advice
**How to avoid:** Provide 2-3 specific options with tradeoffs and example code
**Warning signs:** Recommendations don't answer "what should I do next?"

**From CONTEXT decisions:** Action-oriented tone with specific next steps. User wants prescriptive guidance.

### Pitfall 4: Wrong Severity Indicators
**What goes wrong:** Using 🚨 Critical for minor issues, or ⚠️ Note for serious problems
**Why it happens:** Arbitrary thresholds not aligned with actual impact
**How to avoid:** Critical = breaks modeling or causes wrong conclusions. Note = should investigate but not blocking
**Warning signs:** User ignores critical warnings because too many false alarms

**From research:** Critical alerts demand immediate attention, note-level alerts addressed during regular workflow.

### Pitfall 5: LLM Prompts Too Generic
**What goes wrong:** Prompts like "Analyze my data" that don't include dataset context
**Why it happens:** Copying generic templates without injecting actual findings
**How to avoid:** Every prompt includes specific numbers from this dataset (row count, column names, percentages)
**Warning signs:** Prompts could apply to any dataset

**From research:** 2026 prompt engineering emphasizes specificity and context. Modern LLMs work best with clear, detailed instructions.

### Pitfall 6: Not Distinguishing Between Observation and Action
**What goes wrong:** Presenting findings without translating to "what should I do?"
**Why it happens:** Researcher mindset (describe what's there) vs business analyst mindset (recommend action)
**How to avoid:** Every finding section ends with "What to do:" or "Next steps:"
**Warning signs:** Reader responds "OK, so what?"

**From research:** Big difference between observations ("found X") and actionable insights ("found X, therefore do Y").

### Pitfall 7: One-Size-Fits-All Output
**What goes wrong:** Same level of detail regardless of dataset complexity
**Why it happens:** Fixed template without conditional sections
**How to avoid:** Template logic scales with findings (e.g., skip "Outliers" section if no outliers detected)
**Warning signs:** 5-row dataset gets 10-page report

**From CONTEXT decisions:** Length scales with data complexity (Claude decides based on findings).

## Code Examples

Verified patterns from official sources:

### Example 1: Insight Generation Main Flow
```python
# Source: Synthesized from CONTEXT + research findings

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
import pandas as pd
from typing import Optional, Dict, Any

def generate_insights(
    df: pd.DataFrame,
    target_col: Optional[str] = None,
    output_dir: str = "."
) -> None:
    """
    Generate accessible insights for business analyst audience.

    Creates two outputs:
    1. DATA_REPORT.md - Technical, comprehensive report (saved to file)
    2. INSIGHTS_SUMMARY.md - Plain English summary (displayed + saved)

    Args:
        df: pandas DataFrame to analyze
        target_col: Optional target column for modeling-focused insights
        output_dir: Directory to save output files
    """
    console = Console()

    # 1. Analyze data (reuse Quick Explore analysis)
    from quick import (
        generate_tldr,
        print_overview_table,
        detect_leakage_quick,
        generate_suggestions
    )

    analysis = {
        'n_rows': len(df),
        'n_cols': len(df.columns),
        'memory_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
        'target_col': target_col,
        'critical_issues': identify_critical_issues(df),
        'moderate_issues': identify_moderate_issues(df),
        'positive_findings': identify_positive_findings(df),
        'recommendations': generate_recommendations(df, target_col),
        'llm_prompts': generate_llm_prompts(df, target_col),
        'column_details': analyze_columns(df)
    }

    # 2. Set up Jinja2 environment
    template_dir = Path(__file__).parent / 'templates'
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Add custom filters
    env.filters['format_number'] = lambda x: f"{x:,}"
    env.filters['format_pct'] = lambda x: f"{x:.1f}%"

    # 3. Generate technical DATA_REPORT.md
    technical_template = env.get_template('data_report.md.j2')
    technical_report = technical_template.render(
        df=df,
        analysis=analysis,
        include_technical=True
    )

    output_path = Path(output_dir) / 'DATA_REPORT.md'
    output_path.write_text(technical_report)

    # 4. Generate plain English INSIGHTS_SUMMARY.md
    insights_template = env.get_template('insights_summary.md.j2')
    insights_summary = insights_template.render(
        df=df,
        analysis=analysis,
        include_technical=False
    )

    summary_path = Path(output_dir) / 'INSIGHTS_SUMMARY.md'
    summary_path.write_text(insights_summary)

    # 5. Display insights summary to console with Rich
    console.print(Markdown(insights_summary))

    # 6. Print file locations
    console.print(f"\n[dim]📄 Full technical report: {output_path}[/dim]")
    console.print(f"[dim]📝 Plain English summary: {summary_path}[/dim]")
```

### Example 2: Critical Issue Identification
```python
# Source: User CONTEXT + data quality best practices

def identify_critical_issues(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Identify critical data quality issues requiring immediate attention.

    Critical = breaks modeling or causes wrong conclusions

    Returns list of dicts with: type, column, severity, pct, message
    """
    issues = []

    # Critical threshold: >50% missing
    missing_pcts = (df.isnull().sum() / len(df)) * 100
    critical_missing = missing_pcts[missing_pcts > 50]

    for col, pct in critical_missing.items():
        issues.append({
            'type': 'high_missing',
            'column': col,
            'severity': 'critical',
            'pct': pct,
            'message': f"Over half the data missing ({pct:.1f}%)"
        })

    # Critical: Constant columns (no variance)
    for col in df.columns:
        if df[col].nunique() <= 1:
            issues.append({
                'type': 'constant',
                'column': col,
                'severity': 'critical',
                'message': 'Column has no variance — cannot be useful for modeling'
            })

    # Critical: Target leakage (correlation > 0.98)
    # [Leakage detection logic from Phase 12]

    return issues


def identify_moderate_issues(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Identify moderate issues worth investigating.

    Moderate = should address but not immediately blocking
    """
    issues = []

    # Moderate: 20-50% missing
    missing_pcts = (df.isnull().sum() / len(df)) * 100
    moderate_missing = missing_pcts[(missing_pcts > 20) & (missing_pcts <= 50)]

    for col, pct in moderate_missing.items():
        issues.append({
            'type': 'missing',
            'column': col,
            'severity': 'moderate',
            'pct': pct,
            'message': f"Notable amount of missing data ({pct:.1f}%)"
        })

    # Moderate: Outliers (>5% beyond 3 std)
    # [Outlier detection from Phase 12]

    return issues


def identify_positive_findings(df: pd.DataFrame) -> List[str]:
    """
    Identify positive findings (things that look healthy).

    Returns list of positive statements to balance the report.
    """
    findings = []

    # Check for low missing rates
    missing_pcts = (df.isnull().sum() / len(df)) * 100
    low_missing = missing_pcts[missing_pcts < 5]

    if len(low_missing) > 0:
        findings.append(
            f"{len(low_missing)} columns have minimal missing data (<5%)"
        )

    # Check for no duplicates
    if df.duplicated().sum() == 0:
        findings.append("No duplicate rows detected")

    # Check for balanced distributions
    # [Distribution checks from Phase 12]

    return findings
```

### Example 3: Recommendation Generation with Specificity
```python
# Source: User CONTEXT + action-oriented writing research

def generate_recommendations(
    df: pd.DataFrame,
    target_col: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Generate specific, actionable recommendations with example code.

    Each recommendation includes:
    - What: The action to take
    - Why: The reason (tied to a specific finding)
    - How: Example code snippet
    - Priority: critical/moderate/optional
    """
    recommendations = []

    # Recommendation for high missing data
    missing_pcts = (df.isnull().sum() / len(df)) * 100
    high_missing = missing_pcts[missing_pcts > 20]

    for col, pct in high_missing.items():
        dtype = df[col].dtype

        if pct > 50:
            # Critical: likely need to drop column
            recommendations.append({
                'priority': 'critical',
                'what': f"Decide on strategy for {col}",
                'why': f"Column has {pct:.1f}% missing — over half the data",
                'how': f"""Option 1: Drop the column entirely
```python
df = df.drop(columns=['{col}'])
```

Option 2: Investigate why it's missing
```python
# Check if missingness correlates with other columns
missing_mask = df['{col}'].isnull()
df.groupby(missing_mask).mean()
```""",
                'reference': col
            })
        else:
            # Moderate: imputation might work
            if pd.api.types.is_numeric_dtype(dtype):
                strategy = "median"
                example_value = df[col].median()
            else:
                strategy = "mode"
                example_value = df[col].mode()[0] if len(df[col].mode()) > 0 else "N/A"

            recommendations.append({
                'priority': 'moderate',
                'what': f"Handle missing values in {col}",
                'why': f"Column has {pct:.1f}% missing",
                'how': f"""Option 1: Impute with {strategy}
```python
df['{col}'].fillna({example_value}, inplace=True)
```

Option 2: Drop rows with missing values
```python
df = df.dropna(subset=['{col}'])  # Loses {int(len(df) * pct / 100):,} rows
```""",
                'reference': col
            })

    # Recommendation for class imbalance (if target specified)
    if target_col and target_col in df.columns:
        value_counts = df[target_col].value_counts()
        if len(value_counts) >= 2:
            ratio = value_counts.iloc[0] / value_counts.iloc[-1]
            if ratio > 5:
                recommendations.append({
                    'priority': 'moderate',
                    'what': f"Address class imbalance in {target_col}",
                    'why': f"Ratio is {ratio:.1f}:1 — model will be biased toward majority class",
                    'how': f"""Option 1: Oversample minority class
```python
from imblearn.over_sampling import SMOTE
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X, y)
```

Option 2: Use class weights
```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(class_weight='balanced')
```""",
                    'reference': target_col
                })

    return sorted(recommendations, key=lambda x: {'critical': 0, 'moderate': 1, 'optional': 2}[x['priority']])
```

### Example 4: Jinja2 Template for INSIGHTS_SUMMARY.md
```jinja2
{# Source: User CONTEXT + inverted pyramid structure #}
# Data Insights Summary

**Generated:** {{ timestamp }}
**Dataset:** {{ analysis.n_rows|format_number }} rows × {{ analysis.n_cols }} columns

---

## TL;DR

{% if analysis.critical_issues %}
**Critical finding:** {{ analysis.critical_issues[0].message }} in column `{{ analysis.critical_issues[0].column }}`. Address this before modeling.
{% elif analysis.moderate_issues %}
**Key finding:** {{ analysis.moderate_issues[0].message }} in column `{{ analysis.moderate_issues[0].column }}`. Plan to handle this during preprocessing.
{% else %}
**Overall:** Data looks healthy with no major quality issues detected. Ready for exploratory analysis.
{% endif %}

---

## 5 Things to Know

{% for item in analysis.key_takeaways[:5] %}
**{{ loop.index }}. {{ item.headline }}**
{{ item.explanation }}
{% if item.action %}→ Action: {{ item.action }}{% endif %}

{% endfor %}

---

## Data Overview

| Metric | Value | What This Means |
|--------|-------|-----------------|
| Rows | {{ analysis.n_rows|format_number }} | {{ explain_row_count(analysis.n_rows) }} |
| Columns | {{ analysis.n_cols }} | {{ explain_column_count(analysis.n_cols) }} |
| Memory | {{ analysis.memory_mb|round(1) }} MB | {{ explain_memory(analysis.memory_mb) }} |
| Missing Data | {{ analysis.total_missing_pct|format_pct }} | {{ explain_missing(analysis.total_missing_pct) }} |

---

## Critical Issues

{% if analysis.critical_issues %}
{% for issue in analysis.critical_issues %}
### 🚨 {{ issue.column }}

**Problem:** {{ issue.message }}

**What this means:** {% if issue.type == 'high_missing' %}
Over half your data is missing for this column. Using it as-is will severely limit your analysis — most rows will be excluded or you'll need aggressive imputation that adds uncertainty.
{% elif issue.type == 'constant' %}
This column has the same value for every row. It provides zero information for modeling and should be dropped immediately.
{% endif %}

**What to do:** [Specific recommendation with example code]

{% endfor %}
{% else %}
✅ No critical issues detected.
{% endif %}

---

## Recommendations

{% for rec in analysis.recommendations %}
### {% if rec.priority == 'critical' %}🚨 Critical{% elif rec.priority == 'moderate' %}⚠️ Important{% else %}💡 Optional{% endif %}: {{ rec.what }}

**Why:** {{ rec.why }}

**How to address:**
{{ rec.how }}

{% endfor %}

---

## Dig Deeper (LLM Prompts)

Copy and paste these prompts into ChatGPT, Claude, or any LLM to explore further:

{% for prompt in analysis.llm_prompts %}
**{{ loop.index }}. {{ prompt.title }}**
```
{{ prompt.text }}
```

{% endfor %}

---

*📄 For full technical details, see DATA_REPORT.md*
*🤖 Generated by GRD Accessible Insights*
```

### Example 5: LLM Prompt Generation with Context
```python
# Source: User CONTEXT + 2026 prompt engineering best practices

def generate_llm_prompts(
    df: pd.DataFrame,
    target_col: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Generate 3-5 contextual LLM prompts for further exploration.

    Prompts are:
    - Specific to this dataset (include row/column counts, actual column names)
    - Self-contained (no need to upload data)
    - Generic (work with any LLM)
    - Focused on highest-value questions based on findings

    Returns list of dicts with 'title' and 'text' keys.
    """
    prompts = []

    # Analyze for key characteristics
    missing_pcts = (df.isnull().sum() / len(df)) * 100
    high_missing_cols = missing_pcts[missing_pcts > 20].index.tolist()

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # Prompt 1: Missing data strategy (if applicable)
    if high_missing_cols:
        col = high_missing_cols[0]
        pct = missing_pcts[col]
        prompts.append({
            'title': 'Missing Data Strategy',
            'text': f"""I have a dataset with {len(df):,} rows and a column called '{col}' that has {pct:.1f}% missing values.

The column type is {df[col].dtype}. The data is for [describe your use case].

Question: What are the possible reasons this data might be missing? Should I:
1. Drop the column entirely
2. Drop rows with missing values (losing {int(len(df) * pct / 100):,} rows)
3. Impute values (and if so, what method?)

What factors should guide my decision?"""
        })

    # Prompt 2: Feature engineering (if target specified)
    if target_col and target_col in df.columns:
        feature_cols = [c for c in df.columns if c != target_col][:5]
        prompts.append({
            'title': 'Feature Engineering Ideas',
            'text': f"""I'm building a model to predict '{target_col}' from a dataset with {len(df):,} rows.

Available features include: {', '.join(feature_cols)}, and {len(df.columns) - 1 - len(feature_cols)} others.

I have {len(num_cols)} numerical columns and {len(cat_cols)} categorical columns.

Question: What feature engineering techniques should I consider?
- Interactions between which features might be valuable?
- Should I create polynomial features?
- How should I handle the categorical variables?
- Are there domain-specific transformations I should try?"""
        })

    # Prompt 3: Outlier handling (if outliers detected)
    outlier_cols = []
    for col in num_cols[:10]:  # Check first 10 numerical columns
        data = df[col].dropna()
        if len(data) > 0 and data.std() > 0:
            z_scores = np.abs((data - data.mean()) / data.std())
            outlier_pct = (z_scores > 3).sum() / len(data) * 100
            if outlier_pct > 5:
                outlier_cols.append((col, outlier_pct))

    if outlier_cols:
        col, pct = outlier_cols[0]
        prompts.append({
            'title': 'Outlier Treatment',
            'text': f"""My column '{col}' has {pct:.1f}% of values that are outliers (beyond 3 standard deviations from the mean).

The column contains [describe what this measures, e.g., "customer purchase amounts in dollars"].

Question: Should I remove these outliers, cap them (winsorize), transform the data (log/sqrt), or leave them as-is? What are the implications of each choice for my analysis?"""
        })

    # Prompt 4: Model selection (if target specified)
    if target_col and target_col in df.columns:
        target_type = "numerical" if pd.api.types.is_numeric_dtype(df[target_col]) else "categorical"
        task = "regression" if target_type == "numerical" else "classification"

        prompts.append({
            'title': f'Model Selection for {task.title()}',
            'text': f"""I need to build a {task} model to predict '{target_col}'.

Dataset characteristics:
- {len(df):,} rows
- {len(num_cols)} numerical features
- {len(cat_cols)} categorical features
- Target variable is {target_type}

Question: What modeling approaches would work well for this scenario?
- Should I start with linear models or tree-based models?
- How should I handle the mix of numerical and categorical features?
- What validation strategy should I use?
- Are there any preprocessing steps critical for the models you recommend?"""
        })

    # Prompt 5: Exploratory visualization (always include)
    prompts.append({
        'title': 'Visualization Strategy',
        'text': f"""I have a dataset with {len(df):,} rows, {len(num_cols)} numerical columns, and {len(cat_cols)} categorical columns.

{'My goal is to predict ' + target_col + '.' if target_col else 'I want to explore relationships in the data.'}

Question: What visualizations should I create to understand this data?
- What plots will reveal important relationships?
- Should I focus on distributions, correlations, or patterns over time?
- Are there specific visualizations that work best for this type of analysis?"""
    })

    # Return max 5 prompts (prioritize based on findings)
    return prompts[:5]
```

### Example 6: Statistical Explanation Helpers
```python
# Source: Research on explaining statistics in plain English

def explain_row_count(n_rows: int) -> str:
    """Explain what row count means for analysis."""
    if n_rows < 100:
        return "Very small dataset — statistical patterns may not be reliable"
    elif n_rows < 1000:
        return "Small dataset — good for quick experiments, may need more data for production"
    elif n_rows < 100000:
        return "Moderate size — sufficient for most modeling techniques"
    elif n_rows < 1000000:
        return "Large dataset — plenty of data for complex models"
    else:
        return f"Very large dataset — consider sampling for exploratory work"


def explain_column_count(n_cols: int) -> str:
    """Explain what column count means for analysis."""
    if n_cols < 5:
        return "Few features — may limit model performance"
    elif n_cols < 20:
        return "Typical feature count for focused analysis"
    elif n_cols < 100:
        return "Many features — feature selection may improve model performance"
    else:
        return "High-dimensional dataset — consider dimensionality reduction"


def explain_missing(missing_pct: float) -> str:
    """Explain what missing data percentage means."""
    if missing_pct < 1:
        return "Minimal missing data — unlikely to impact analysis"
    elif missing_pct < 5:
        return "Low missing data — simple handling (drop rows) likely sufficient"
    elif missing_pct < 20:
        return "Moderate missing data — need thoughtful imputation strategy"
    else:
        return "High missing data — significant preprocessing required"


def explain_memory(memory_mb: float) -> str:
    """Explain what memory usage means practically."""
    if memory_mb < 10:
        return "Tiny — loads instantly, no memory concerns"
    elif memory_mb < 100:
        return "Small — fits comfortably in memory"
    elif memory_mb < 1000:
        return "Moderate — most operations will be fast"
    else:
        memory_gb = memory_mb / 1024
        return f"Large ({memory_gb:.1f} GB) — consider chunking or sampling for some operations"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual narrative writing | Template-based generation with Jinja2 | 2020-2023 | Consistent tone, faster iteration, easier maintenance |
| Few-shot prompting for LLMs | Zero-shot with clear instructions | 2024-2026 | Modern models understand tasks without examples, fewer tokens |
| Generic recommendations | Context-specific with example code | 2025-2026 | Business analysts can immediately act on insights |
| Technical reports only | Dual output (technical + accessible) | 2025-2026 | Wider audience, faster communication to non-technical stakeholders |
| Observations without action | Action-oriented insights | 2025-2026 | Insights drive behavior change, not just awareness |

**Deprecated/outdated:**
- **LLM-based narrative generation for structured reports:** Adds latency, cost, unpredictability; templates are faster and more consistent (2026)
- **Few-shot prompting as default:** Modern models (2026) perform better with clear zero-shot instructions than biased few-shot examples
- **One executive summary for all audiences:** 2026 best practice is tailored reports for different stakeholder needs

## Open Questions

Things that couldn't be fully resolved:

1. **PyNarrative Maturity**
   - What we know: PyNarrative exists and can generate narratives from DataFrames
   - What's unclear: Production readiness, edge case handling, whether it matches our specific tone requirements
   - Recommendation: Start with Jinja2 templates (full control). Evaluate PyNarrative if automated generation becomes valuable.

2. **Optimal Prompt Length**
   - What we know: Prompts should be specific and include dataset context
   - What's unclear: Whether 2026 LLMs prefer shorter, focused prompts or longer, comprehensive ones
   - Recommendation: Start with medium-length prompts (150-250 words) that are self-contained. User can edit.

3. **Analogy Library Completeness**
   - What we know: Real-world analogies help non-technical understanding
   - What's unclear: Which analogies resonate best for each statistical concept
   - Recommendation: Start with proven analogies from research (bell curve for normal distribution, etc.). Iterate based on user feedback.

4. **Integration with Phase 12**
   - What we know: Phase 12 Quick Explore generates technical output
   - What's unclear: Whether insights generation reuses Quick Explore analysis or runs independently
   - Recommendation: Reuse Quick Explore analysis logic to avoid duplication. Insights generation adds narrative layer.

## Sources

### Primary (HIGH confidence)
- [Jinja2 Official Documentation](https://jinja.palletsprojects.com/en/stable/templates/) - Template syntax, filters, best practices
- [KDnuggets: 10 Basic Statistical Concepts in Plain English](https://www.kdnuggets.com/10-basic-statistical-concepts-in-plain-english) - Non-technical explanations
- [Jinja2 Tutorial - Part 4: Template Filters](https://ttl255.com/jinja2-tutorial-part-4-template-filters/) - Filter usage and best practices
- [Jinja2 Conditional Logic Best Practices](https://30dayscoding.com/blog/jinja-else-if-statements) - Control flow patterns

### Secondary (MEDIUM confidence)
- [Coherent Solutions: NLP in Business Intelligence 2026](https://www.coherentsolutions.com/insights/nlp-in-business-intelligence-7-success-stories-benefits-and-future-trends) - NLG in BI trends
- [JMP: 10 Rules for Communicating Statistical Concepts](https://www.jmp.com/en/blog/inspiration/10-rules-for-communicating-statistical-concepts-to-a-non-technical-audience) - Statistical communication
- [Indiana Wesleyan University: Data Storytelling for Managers (2026)](https://www.indwes.edu/articles/2026/01/data-storytelling-managers-dashboards-into-decisions) - Inverted pyramid approach
- [Juice Analytics: Making Actionable Insights Drive Action (2026)](https://www.juiceanalytics.com/writing/from-insight-to-impact-2026) - Action-oriented recommendations
- [Medium: The Only Prompt Engineering Guide for 2026](https://medium.com/@karl.foster/the-only-prompt-engineering-guide-youll-need-for-2026-7ebfb8857fc8) - Zero-shot vs few-shot
- [KDnuggets: PyNarrative for Data Storytelling](https://www.kdnuggets.com/pynarrative-an-excellent-python-library-for-data-storytelling) - PyNarrative library overview
- [Bricklayer AI: Alert Severity Levels Guide](https://www.bricklayer.ai/insights/a-guide-to-alert-severity-levels/) - Severity classification standards
- [ClickUp: Executive Summary Examples 2026](https://clickup.com/blog/executive-summary-examples/) - TL;DR formatting
- [AgencyAnalytics: Data Analysis Report Writing](https://agencyanalytics.com/blog/data-analysis-report) - Report structure best practices
- [NetSuite: 11 Common Data Analysis Mistakes](https://www.netsuite.com/portal/resource/articles/data-warehouse/data-mistakes.shtml) - Pitfalls to avoid
- [DashThis: Data Analysis Mistakes](https://dashthis.com/blog/mistakes-in-data-analysis/) - Non-technical audience mistakes

### Tertiary (LOW confidence)
- WebSearch results on narrative generation - General trends, not specific methods
- Medium articles on prompt engineering - Community perspectives, not official guidance

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Jinja2 is proven, widely used, well-documented
- Architecture patterns: HIGH - Template-based approach is established pattern for structured text generation
- Pitfalls: HIGH - Based on research + user CONTEXT decisions about tone and structure
- Statistical explanations: MEDIUM - Analogies from research, but effectiveness depends on audience
- LLM prompt engineering: MEDIUM - 2026 best practices emerging, zero-shot guidance is solid but prompt examples need validation

**Research date:** 2026-02-01
**Valid until:** 2026-03-15 (45 days - NLG and prompt engineering are fast-moving but templates remain stable)
