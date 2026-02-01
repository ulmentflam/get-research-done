"""Quick explore analysis module for fast EDA.

This module provides fast data exploration capabilities for the /grd:quick-explore command,
prioritizing speed over comprehensiveness.
"""

from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json

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

from .formatters import (
    print_header_banner,
    print_tldr,
    print_column_table,
    print_distribution_highlights,
    print_quality_warnings,
    print_footer,
    generate_sparkline,
    get_quality_indicator,
)


def quick_explore(
    data_path: str,
    output_dir: str = ".planning",
    target_column: Optional[str] = None,
    sample_size: int = 10000,
) -> Dict[str, Any]:
    """Perform quick exploratory data analysis.

    Args:
        data_path: Path to data file (CSV, Parquet, JSON)
        output_dir: Directory for output files
        target_column: Optional target column for ML context
        sample_size: Max rows to analyze for speed (default 10k)

    Returns:
        Dictionary with analysis results
    """
    if not PANDAS_AVAILABLE:
        raise ImportError("pandas is required for quick_explore")

    # Load data
    df = _load_data(data_path, sample_size)

    # Compute statistics
    stats = _compute_basic_stats(df)
    columns = _analyze_columns(df)
    highlights = _get_distribution_highlights(df)
    warnings = _detect_quality_issues(df, target_column)

    # Print to console
    print_header_banner("QUICK EXPLORE", f"Analyzing: {data_path}")
    print_tldr(stats)
    print_column_table(columns)
    print_distribution_highlights(highlights)
    print_quality_warnings(warnings)

    # Generate report
    report_path = Path(output_dir) / "DATA_REPORT.md"
    report_content = generate_markdown_report(
        data_path=data_path,
        stats=stats,
        columns=columns,
        highlights=highlights,
        warnings=warnings,
        mode="quick"
    )

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Write report
    with open(report_path, 'w') as f:
        f.write(report_content)

    print_footer(
        str(report_path),
        next_steps=[
            "/grd:explore — full analysis with leakage detection",
            "/grd:architect — form hypothesis from data insights"
        ]
    )

    return {
        'stats': stats,
        'columns': columns,
        'highlights': highlights,
        'warnings': warnings,
        'report_path': str(report_path)
    }


def _load_data(path: str, sample_size: int) -> 'pd.DataFrame':
    """Load data from file with optional sampling.

    Args:
        path: Path to data file
        sample_size: Maximum rows to load

    Returns:
        pandas DataFrame
    """
    path = Path(path)

    if path.suffix == '.csv':
        # Check file size for sampling decision
        df = pd.read_csv(path, nrows=sample_size)
    elif path.suffix == '.parquet':
        df = pd.read_parquet(path)
        if len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=42)
    elif path.suffix in ('.json', '.jsonl'):
        df = pd.read_json(path, lines=path.suffix == '.jsonl', nrows=sample_size)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    return df


def _compute_basic_stats(df: 'pd.DataFrame') -> Dict[str, Any]:
    """Compute basic dataset statistics.

    Args:
        df: pandas DataFrame

    Returns:
        Dictionary with basic stats
    """
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    # Count column types
    numeric_cols = len(df.select_dtypes(include=['number']).columns)
    categorical_cols = len(df.select_dtypes(include=['object', 'category']).columns)
    datetime_cols = len(df.select_dtypes(include=['datetime64']).columns)

    # Missing data
    missing_total = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    missing_pct = missing_total / total_cells if total_cells > 0 else 0
    null_columns = (df.isnull().sum() > 0).sum()

    # Issue severity
    issue_count, issue_severity = _assess_overall_quality(df)

    return {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_mb': memory_mb,
        'missing_pct': missing_pct,
        'null_columns': null_columns,
        'numeric_cols': numeric_cols,
        'categorical_cols': categorical_cols,
        'datetime_cols': datetime_cols,
        'issue_count': issue_count,
        'issue_severity': issue_severity,
    }


def _analyze_columns(df: 'pd.DataFrame') -> List[Dict[str, Any]]:
    """Analyze each column for the summary table.

    Args:
        df: pandas DataFrame

    Returns:
        List of column analysis dictionaries
    """
    columns = []

    for col in df.columns:
        col_data = df[col]
        dtype = str(col_data.dtype)
        missing_pct = col_data.isnull().sum() / len(col_data)

        # Distribution for numeric columns
        distribution = []
        skewness = None

        if pd.api.types.is_numeric_dtype(col_data):
            # Remove nulls for histogram
            valid_data = col_data.dropna()
            if len(valid_data) > 0:
                try:
                    hist, _ = np.histogram(valid_data, bins=8)
                    distribution = hist.tolist()

                    if SCIPY_AVAILABLE and len(valid_data) > 3:
                        skewness = stats.skew(valid_data)
                except (ValueError, TypeError):
                    pass

        columns.append({
            'name': col,
            'dtype': dtype,
            'missing_pct': missing_pct,
            'distribution': distribution,
            'skewness': skewness,
        })

    return columns


def _get_distribution_highlights(df: 'pd.DataFrame') -> List[Dict[str, Any]]:
    """Get notable distribution characteristics.

    Args:
        df: pandas DataFrame

    Returns:
        List of distribution highlights
    """
    highlights = []

    for col in df.select_dtypes(include=['number']).columns:
        col_data = df[col].dropna()
        if len(col_data) < 10:
            continue

        skewness = 0
        outliers = 0
        note = None

        if SCIPY_AVAILABLE:
            skewness = stats.skew(col_data)

        # Simple outlier detection using IQR
        if NUMPY_AVAILABLE:
            q1, q3 = np.percentile(col_data, [25, 75])
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = ((col_data < lower) | (col_data > upper)).sum()

        # Only include if notable
        if abs(skewness) > 1.0 or outliers > len(col_data) * 0.05:
            if outliers > len(col_data) * 0.1:
                note = "High outlier count may affect models"
            elif abs(skewness) > 2:
                note = "Consider log transform"

            highlights.append({
                'column': col,
                'skewness': skewness,
                'outliers': outliers,
                'note': note,
            })

    return highlights[:5]  # Limit to top 5


def _detect_quality_issues(
    df: 'pd.DataFrame',
    target_column: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Detect data quality issues quickly.

    Args:
        df: pandas DataFrame
        target_column: Optional target column

    Returns:
        List of quality warnings
    """
    warnings = []

    # High missing columns
    for col in df.columns:
        missing_pct = df[col].isnull().sum() / len(df)
        if missing_pct > 0.3:
            warnings.append({
                'severity': 'critical',
                'column': col,
                'message': f"{missing_pct:.0%} missing values"
            })
        elif missing_pct > 0.1:
            warnings.append({
                'severity': 'warning',
                'column': col,
                'message': f"{missing_pct:.0%} missing values"
            })

    # Constant columns
    for col in df.columns:
        if df[col].nunique() == 1:
            warnings.append({
                'severity': 'warning',
                'column': col,
                'message': "Constant column (only one unique value)"
            })

    # High cardinality categorical
    for col in df.select_dtypes(include=['object']).columns:
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio > 0.9:
            warnings.append({
                'severity': 'info',
                'column': col,
                'message': f"High cardinality ({df[col].nunique()} unique values) - may be ID column"
            })

    # Quick leakage check - column name patterns
    leakage_patterns = ['target', 'label', 'outcome', 'result', 'future', 'leak']
    for col in df.columns:
        col_lower = col.lower()
        if any(p in col_lower for p in leakage_patterns):
            if target_column and col != target_column:
                warnings.append({
                    'severity': 'warning',
                    'column': col,
                    'message': f"Column name suggests potential leakage"
                })

    # Sort by severity
    severity_order = {'critical': 0, 'warning': 1, 'info': 2}
    warnings.sort(key=lambda x: severity_order.get(x['severity'], 3))

    return warnings[:10]  # Limit to top 10


def _assess_overall_quality(df: 'pd.DataFrame') -> Tuple[int, str]:
    """Assess overall data quality for TL;DR.

    Args:
        df: pandas DataFrame

    Returns:
        Tuple of (issue_count, severity)
    """
    issues = 0
    max_severity = 'info'

    # Check missing data
    missing_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
    if missing_pct > 0.3:
        issues += 1
        max_severity = 'critical'
    elif missing_pct > 0.1:
        issues += 1
        if max_severity != 'critical':
            max_severity = 'warning'

    # Check constant columns
    constant_cols = sum(1 for col in df.columns if df[col].nunique() == 1)
    if constant_cols > 0:
        issues += constant_cols
        if max_severity == 'info':
            max_severity = 'warning'

    # Check duplicate rows
    dup_pct = df.duplicated().sum() / len(df)
    if dup_pct > 0.1:
        issues += 1
        if max_severity != 'critical':
            max_severity = 'warning'

    return issues, max_severity


def generate_markdown_report(
    data_path: str,
    stats: Dict[str, Any],
    columns: List[Dict[str, Any]],
    highlights: List[Dict[str, Any]],
    warnings: List[Dict[str, Any]],
    mode: str = "quick"
) -> str:
    """Generate markdown report content.

    Args:
        data_path: Original data path
        stats: Basic statistics
        columns: Column analysis
        highlights: Distribution highlights
        warnings: Quality warnings
        mode: 'quick' or 'full'

    Returns:
        Markdown string
    """
    lines = []

    # Header with mode indicator
    if mode == "quick":
        lines.append("# Data Report (Quick Explore Mode)")
        lines.append("")
        lines.append("> **Note:** This is a quick exploration. Run `/grd:explore` for comprehensive analysis with leakage detection.")
        lines.append("")
    else:
        lines.append("# Data Report")
        lines.append("")

    lines.append(f"**Source:** `{data_path}`")
    lines.append(f"**Generated:** Quick Explore Mode")
    lines.append("")

    # Overview
    lines.append("## Overview")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Rows | {stats['rows']:,} |")
    lines.append(f"| Columns | {stats['columns']} |")
    lines.append(f"| Memory | {stats['memory_mb']:.1f} MB |")
    lines.append(f"| Missing | {stats['missing_pct']:.1%} |")
    lines.append(f"| Columns with nulls | {stats['null_columns']} |")
    lines.append("")

    # Column summary
    lines.append("## Column Summary")
    lines.append("")
    lines.append("| Column | Type | Missing | Notes |")
    lines.append("|--------|------|---------|-------|")
    for col in columns:
        notes = []
        if col['skewness'] is not None and abs(col['skewness']) > 1:
            notes.append(f"skew: {col['skewness']:.1f}")
        notes_str = ", ".join(notes) if notes else "—"
        lines.append(f"| {col['name']} | {col['dtype']} | {col['missing_pct']:.0%} | {notes_str} |")
    lines.append("")

    # Quality warnings
    if warnings:
        lines.append("## Quality Issues")
        lines.append("")
        for w in warnings:
            emoji = {'critical': '🔴', 'warning': '🟡', 'info': '🟢'}.get(w['severity'], '⚪')
            col_str = f"**{w['column']}**: " if w.get('column') else ""
            lines.append(f"- {emoji} {col_str}{w['message']}")
        lines.append("")

    # Distribution highlights
    if highlights:
        lines.append("## Distribution Notes")
        lines.append("")
        for h in highlights:
            note = f" — {h['note']}" if h.get('note') else ""
            lines.append(f"- **{h['column']}**: skewness {h['skewness']:.2f}, {h['outliers']} outliers{note}")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Generated by GRD Quick Explore*")

    return "\n".join(lines)


def detect_leakage_quick(df: 'pd.DataFrame', target_col: Optional[str] = None) -> List[str]:
    """Quick leakage detection based on column names only.

    Args:
        df: pandas DataFrame
        target_col: Target column name if known

    Returns:
        List of suspicious column names
    """
    suspicious = []
    patterns = ['target', 'label', 'outcome', 'result', 'future', 'leak', 'answer', 'y_']

    for col in df.columns:
        if target_col and col == target_col:
            continue

        col_lower = col.lower()
        if any(p in col_lower for p in patterns):
            suspicious.append(col)

    return suspicious


def generate_suggestions(stats: Dict[str, Any], warnings: List[Dict[str, Any]]) -> List[str]:
    """Generate next-step suggestions based on analysis.

    Args:
        stats: Basic statistics
        warnings: Quality warnings

    Returns:
        List of suggestion strings
    """
    suggestions = []

    # Based on warnings
    critical_count = sum(1 for w in warnings if w['severity'] == 'critical')
    if critical_count > 0:
        suggestions.append(f"Address {critical_count} critical issues before modeling")

    # Based on missing data
    if stats['missing_pct'] > 0.1:
        suggestions.append("Consider imputation strategy for missing values")

    # Default suggestions
    if not suggestions:
        suggestions.append("Data looks ready for exploration")
        suggestions.append("Run /grd:explore for comprehensive analysis")

    return suggestions
