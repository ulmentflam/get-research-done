"""Insights generation module for plain English data analysis.

This module provides accessible data insights for business analysts,
translating statistical findings into plain English with actionable recommendations.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

from .quick import _load_data, _compute_basic_stats, _analyze_columns, _detect_quality_issues
from .formatters import print_header_banner, print_footer


# Statistical term translations
STAT_TRANSLATIONS = {
    'null': 'missing value',
    'NaN': 'missing value',
    'dtype': 'data type',
    'int64': 'whole number',
    'float64': 'decimal number',
    'object': 'text',
    'bool': 'yes/no',
    'datetime64': 'date/time',
    'category': 'category',
    'skewness': 'distribution shape',
    'outlier': 'unusual value',
    'cardinality': 'number of unique values',
}


def generate_insights(
    data_path: str,
    output_dir: str = ".planning",
    target_column: Optional[str] = None,
    project_context: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate plain English data insights.

    Args:
        data_path: Path to data file
        output_dir: Directory for output files
        target_column: Optional target column for ML context
        project_context: Optional project description for context

    Returns:
        Dictionary with paths to generated files
    """
    if not PANDAS_AVAILABLE:
        raise ImportError("pandas is required for generate_insights")

    # Load and analyze data
    df = _load_data(data_path, sample_size=50000)
    stats = _compute_basic_stats(df)
    columns = _analyze_columns(df)
    warnings = _detect_quality_issues(df, target_column)

    # Generate insights
    critical_issues = identify_critical_issues(df, warnings)
    recommendations = generate_recommendations(df, stats, warnings)
    llm_prompts = generate_llm_prompts(df, stats, columns, project_context)

    # Print header
    print_header_banner("DATA INSIGHTS", f"Analyzing: {data_path}")

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Generate technical report
    report_path = Path(output_dir) / "DATA_REPORT.md"
    report_content = _generate_technical_report(data_path, df, stats, columns, warnings)
    with open(report_path, 'w') as f:
        f.write(report_content)

    # Generate insights summary
    summary_path = Path(output_dir) / "INSIGHTS_SUMMARY.md"
    summary_content = _generate_insights_summary(
        data_path=data_path,
        stats=stats,
        columns=columns,
        critical_issues=critical_issues,
        recommendations=recommendations,
        llm_prompts=llm_prompts,
    )
    with open(summary_path, 'w') as f:
        f.write(summary_content)

    # Print summary to console
    print(summary_content)

    print_footer(
        str(summary_path),
        next_steps=[
            "Share INSIGHTS_SUMMARY.md with stakeholders",
            "Use LLM prompts for deeper analysis",
            "/grd:architect — form hypothesis from insights"
        ]
    )

    return {
        'report_path': str(report_path),
        'summary_path': str(summary_path),
        'stats': stats,
        'critical_issues': critical_issues,
        'recommendations': recommendations,
    }


def identify_critical_issues(df: 'pd.DataFrame', warnings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identify critical issues requiring attention.

    Args:
        df: pandas DataFrame
        warnings: Quality warnings from analysis

    Returns:
        List of critical issues with plain English explanations
    """
    issues = []

    for w in warnings:
        if w['severity'] == 'critical':
            issues.append({
                'title': f"High missing data in {w.get('column', 'dataset')}",
                'what_it_means': _explain_issue(w),
                'recommended_action': _suggest_action(w),
            })

    # Check for other critical patterns
    # Duplicate rows
    dup_count = df.duplicated().sum()
    if dup_count > len(df) * 0.1:
        issues.append({
            'title': f"{dup_count:,} duplicate rows detected",
            'what_it_means': "Over 10% of your data are exact copies. This could mean data was accidentally duplicated during collection or processing.",
            'recommended_action': "Review data collection process. Consider removing duplicates before analysis.",
        })

    # Constant columns
    for col in df.columns:
        if df[col].nunique() == 1:
            issues.append({
                'title': f"Column '{col}' has only one value",
                'what_it_means': "This column provides no useful information for analysis since every row has the same value.",
                'recommended_action': "Remove this column from your analysis.",
            })

    return issues


def generate_recommendations(
    df: 'pd.DataFrame',
    stats: Dict[str, Any],
    warnings: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Generate prioritized recommendations.

    Args:
        df: pandas DataFrame
        stats: Basic statistics
        warnings: Quality warnings

    Returns:
        List of recommendations with priority and effort
    """
    recommendations = []

    # High priority: Critical warnings
    for w in warnings:
        if w['severity'] == 'critical':
            recommendations.append({
                'priority': 'High',
                'title': f"Fix {w.get('column', 'data')} issues",
                'description': _explain_issue(w),
                'effort': 'Medium',
                'code_example': _get_fix_code(w, df),
            })

    # Medium priority: Warnings
    for w in warnings:
        if w['severity'] == 'warning':
            recommendations.append({
                'priority': 'Medium',
                'title': f"Address {w.get('column', 'data')} concerns",
                'description': _explain_issue(w),
                'effort': 'Low',
                'code_example': _get_fix_code(w, df),
            })

    # Low priority: Improvements
    if stats['missing_pct'] > 0.05:
        recommendations.append({
            'priority': 'Low',
            'title': 'Consider imputation strategy',
            'description': f"About {stats['missing_pct']:.0%} of values are missing. You might improve model performance by filling these gaps intelligently.",
            'effort': 'Medium',
            'code_example': "# Simple imputation\ndf.fillna(df.median(), inplace=True)",
        })

    return recommendations


def generate_llm_prompts(
    df: 'pd.DataFrame',
    stats: Dict[str, Any],
    columns: List[Dict[str, Any]],
    project_context: Optional[str] = None,
) -> List[str]:
    """Generate LLM prompts for further exploration.

    Args:
        df: pandas DataFrame
        stats: Basic statistics
        columns: Column analysis
        project_context: Optional project description

    Returns:
        List of copy-paste ready prompts
    """
    prompts = []
    context_str = f" for {project_context}" if project_context else ""

    # Numeric columns relationships
    numeric_cols = [c['name'] for c in columns if 'int' in c['dtype'] or 'float' in c['dtype']]
    if len(numeric_cols) >= 2:
        prompts.append(
            f"Analyze the relationship between '{numeric_cols[0]}' and '{numeric_cols[1]}'{context_str}. "
            f"What patterns might explain their correlation? What business insights could this reveal?"
        )

    # Missing data strategy
    high_missing = [c for c in columns if c['missing_pct'] > 0.1]
    if high_missing:
        col = high_missing[0]['name']
        prompts.append(
            f"The column '{col}' has {high_missing[0]['missing_pct']:.0%} missing values. "
            f"What are the best strategies for handling this? Consider: "
            f"1) Why might this data be missing? "
            f"2) What imputation method would preserve the data's meaning? "
            f"3) Should we drop this column entirely?"
        )

    # Categorical analysis
    cat_cols = [c['name'] for c in columns if c['dtype'] == 'object']
    if cat_cols:
        prompts.append(
            f"Analyze the categorical column '{cat_cols[0]}'{context_str}. "
            f"What do the different categories represent? Are there any categories that should be combined or renamed?"
        )

    # General exploration
    prompts.append(
        f"This dataset has {stats['rows']:,} rows and {stats['columns']} columns{context_str}. "
        f"What are the 3 most important questions we should answer with this data? "
        f"What analyses would provide the most business value?"
    )

    return prompts[:5]  # Limit to 5 prompts


def _explain_issue(warning: Dict[str, Any]) -> str:
    """Generate plain English explanation for a warning.

    Args:
        warning: Warning dictionary

    Returns:
        Plain English explanation
    """
    msg = warning.get('message', '')
    col = warning.get('column', 'this data')

    if 'missing' in msg.lower():
        pct = msg.split('%')[0].replace('~', '').strip() if '%' in msg else '30'
        return (
            f"About {pct}% of rows have no value for '{col}'. "
            f"This is significant and could skew your analysis. "
            f"Models trained on this data might make poor predictions for records with missing values."
        )

    if 'constant' in msg.lower():
        return (
            f"Every row has the exact same value for '{col}'. "
            f"This column won't help distinguish between different outcomes and should be removed."
        )

    if 'cardinality' in msg.lower():
        return (
            f"'{col}' has almost as many unique values as there are rows. "
            f"This is often an ID column (like customer_id) that shouldn't be used for prediction."
        )

    if 'leakage' in msg.lower():
        return (
            f"The column name '{col}' suggests it might contain information that wouldn't be available "
            f"at prediction time. Using this could make your model look artificially good but fail in production."
        )

    return msg


def _suggest_action(warning: Dict[str, Any]) -> str:
    """Generate recommended action for a warning.

    Args:
        warning: Warning dictionary

    Returns:
        Recommended action string
    """
    msg = warning.get('message', '').lower()

    if 'missing' in msg:
        return "Either fill in the missing values (imputation) or remove this column if the data can't be recovered."

    if 'constant' in msg:
        return "Remove this column from your analysis."

    if 'cardinality' in msg:
        return "If this is an ID column, exclude it from modeling. If it's a text field, consider grouping similar values."

    if 'leakage' in msg:
        return "Verify this column would be available at prediction time. If not, remove it to prevent data leakage."

    return "Review and address before proceeding."


def _get_fix_code(warning: Dict[str, Any], df: 'pd.DataFrame') -> str:
    """Generate example code to fix an issue.

    Args:
        warning: Warning dictionary
        df: pandas DataFrame

    Returns:
        Python code example
    """
    col = warning.get('column')
    msg = warning.get('message', '').lower()

    if not col:
        return "# Review data and apply appropriate fix"

    if 'missing' in msg:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            return f"# Fill missing values with median\ndf['{col}'].fillna(df['{col}'].median(), inplace=True)"
        else:
            return f"# Fill missing values with mode (most common value)\ndf['{col}'].fillna(df['{col}'].mode()[0], inplace=True)"

    if 'constant' in msg:
        return f"# Remove constant column\ndf.drop('{col}', axis=1, inplace=True)"

    if 'cardinality' in msg:
        return f"# Remove high-cardinality column (likely ID)\ndf.drop('{col}', axis=1, inplace=True)"

    return f"# Review column '{col}' and apply appropriate fix"


def _generate_technical_report(
    data_path: str,
    df: 'pd.DataFrame',
    stats: Dict[str, Any],
    columns: List[Dict[str, Any]],
    warnings: List[Dict[str, Any]],
) -> str:
    """Generate technical DATA_REPORT.md content.

    Args:
        data_path: Original data path
        df: pandas DataFrame
        stats: Basic statistics
        columns: Column analysis
        warnings: Quality warnings

    Returns:
        Markdown string
    """
    lines = []

    lines.append("# Data Report")
    lines.append("")
    lines.append(f"**Source:** `{data_path}`")
    lines.append(f"**Generated by:** GRD Insights Mode")
    lines.append("")

    # Overview
    lines.append("## Data Overview")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Rows | {stats['rows']:,} |")
    lines.append(f"| Columns | {stats['columns']} |")
    lines.append(f"| Memory | {stats['memory_mb']:.1f} MB |")
    lines.append(f"| Missing Values | {stats['missing_pct']:.1%} |")
    lines.append(f"| Numeric Columns | {stats['numeric_cols']} |")
    lines.append(f"| Categorical Columns | {stats['categorical_cols']} |")
    lines.append("")

    # Column Summary
    lines.append("## Column Summary")
    lines.append("")
    lines.append("| Column | Type | Missing | Unique |")
    lines.append("|--------|------|---------|--------|")
    for col in columns:
        unique = df[col['name']].nunique() if col['name'] in df.columns else '?'
        lines.append(f"| {col['name']} | {col['dtype']} | {col['missing_pct']:.0%} | {unique} |")
    lines.append("")

    # Quality Issues
    if warnings:
        lines.append("## Data Quality Issues")
        lines.append("")
        for w in warnings:
            emoji = {'critical': '🔴', 'warning': '🟡', 'info': '🟢'}.get(w['severity'], '⚪')
            col_str = f"**{w['column']}**: " if w.get('column') else ""
            lines.append(f"- {emoji} {col_str}{w['message']}")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by GRD Insights*")

    return "\n".join(lines)


def _generate_insights_summary(
    data_path: str,
    stats: Dict[str, Any],
    columns: List[Dict[str, Any]],
    critical_issues: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]],
    llm_prompts: List[str],
) -> str:
    """Generate INSIGHTS_SUMMARY.md content.

    Args:
        data_path: Original data path
        stats: Basic statistics
        columns: Column analysis
        critical_issues: Critical issues list
        recommendations: Recommendations list
        llm_prompts: LLM prompts list

    Returns:
        Markdown string
    """
    lines = []

    lines.append("# Data Insights Summary")
    lines.append("")
    lines.append(f"**Dataset:** `{data_path}`")
    lines.append("")

    # TL;DR
    lines.append("## TL;DR")
    lines.append("")
    lines.append(f"- **Size:** {stats['rows']:,} records with {stats['columns']} data points each")
    lines.append(f"- **Completeness:** {100 - stats['missing_pct']*100:.0f}% of data is filled in")
    lines.append(f"- **Data types:** {stats['numeric_cols']} numbers, {stats['categorical_cols']} categories")

    issue_count = len(critical_issues)
    if issue_count > 0:
        lines.append(f"- **Issues:** {issue_count} item(s) need attention before analysis")
    else:
        lines.append("- **Quality:** Data looks ready for analysis")
    lines.append("")

    # 5 Things to Know
    lines.append("## 5 Things to Know About This Data")
    lines.append("")
    lines.append("| Finding | What This Means |")
    lines.append("|---------|-----------------|")
    lines.append(f"| {stats['rows']:,} rows of data | {'Enough for reliable statistical analysis' if stats['rows'] > 1000 else 'Limited sample - interpret results with caution'} |")
    lines.append(f"| {stats['columns']} columns | {'Complex dataset with many features' if stats['columns'] > 20 else 'Manageable number of features'} |")

    if stats['null_columns'] > 0:
        lines.append(f"| {stats['null_columns']} columns have gaps | Some data collection may be incomplete |")

    if stats['numeric_cols'] > 0:
        lines.append(f"| {stats['numeric_cols']} numeric columns | These can be used for calculations and predictions |")

    if stats['categorical_cols'] > 0:
        lines.append(f"| {stats['categorical_cols']} category columns | These represent groups or classifications |")
    lines.append("")

    # Critical Issues
    if critical_issues:
        lines.append("## Critical Issues")
        lines.append("")
        for issue in critical_issues:
            lines.append(f"### {issue['title']}")
            lines.append("")
            lines.append(f"**What this means:** {issue['what_it_means']}")
            lines.append("")
            lines.append(f"**Recommended action:** {issue['recommended_action']}")
            lines.append("")

    # Recommendations
    if recommendations:
        lines.append("## Recommendations")
        lines.append("")
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"### {i}. [{rec['priority']}] {rec['title']}")
            lines.append("")
            lines.append(rec['description'])
            if rec.get('code_example'):
                lines.append("")
                lines.append("```python")
                lines.append(rec['code_example'])
                lines.append("```")
            lines.append("")

    # LLM Prompts
    if llm_prompts:
        lines.append("## Dig Deeper")
        lines.append("")
        lines.append("Copy and paste these prompts to explore further:")
        lines.append("")
        for i, prompt in enumerate(llm_prompts, 1):
            lines.append(f"**Prompt {i}:**")
            lines.append("```")
            lines.append(prompt)
            lines.append("```")
            lines.append("")

    lines.append("---")
    lines.append("*Generated by GRD Insights*")

    return "\n".join(lines)
