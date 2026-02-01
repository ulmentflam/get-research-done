"""Rich formatting utilities for GRD console output.

This module provides formatting functions for quick-explore and insights modes,
producing terminal-friendly output that's easy to read and copy-paste.
"""

from typing import List, Dict, Any, Optional
import sys

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


# Quality indicator thresholds
QUALITY_THRESHOLDS = {
    'missing': {'good': 0.01, 'warning': 0.1, 'critical': 0.3},
    'unique_ratio': {'good': 0.95, 'warning': 0.5, 'critical': 0.1},
    'skewness': {'good': 0.5, 'warning': 1.0, 'critical': 2.0},
}


def generate_sparkline(values: List[float], width: int = 8) -> str:
    """Generate a sparkline representation of a distribution.

    Args:
        values: List of numeric values (histogram counts or raw values)
        width: Number of characters in sparkline

    Returns:
        String sparkline like "▁▂▃▅▇▅▃▁"
    """
    if not values or len(values) == 0:
        return "?" * width

    # Sparkline characters from lowest to highest
    chars = "▁▂▃▄▅▆▇█"

    try:
        min_val = min(values)
        max_val = max(values)

        if max_val == min_val:
            return chars[4] * min(len(values), width)

        # Normalize and map to characters
        result = []
        step = max(1, len(values) // width)
        for i in range(0, min(len(values), width * step), step):
            chunk = values[i:i + step]
            avg = sum(chunk) / len(chunk)
            normalized = (avg - min_val) / (max_val - min_val)
            char_idx = int(normalized * (len(chars) - 1))
            result.append(chars[char_idx])

        return ''.join(result[:width])
    except (ValueError, ZeroDivisionError):
        return "?" * width


def get_quality_indicator(value: float, metric: str, reverse: bool = False) -> str:
    """Get emoji quality indicator based on threshold.

    Args:
        value: The metric value to evaluate
        metric: One of 'missing', 'unique_ratio', 'skewness'
        reverse: If True, lower is better (default: higher is worse)

    Returns:
        Emoji indicator: "✓" (good), "⚠" (warning), "✗" (critical)
    """
    thresholds = QUALITY_THRESHOLDS.get(metric, {'good': 0.1, 'warning': 0.3, 'critical': 0.5})

    if reverse:
        # Lower is better (e.g., unique_ratio where high unique is good)
        if value >= thresholds['good']:
            return "✓"
        elif value >= thresholds['warning']:
            return "⚠"
        else:
            return "✗"
    else:
        # Higher is worse (e.g., missing percentage)
        if value <= thresholds['good']:
            return "✓"
        elif value <= thresholds['warning']:
            return "⚠"
        else:
            return "✗"


def get_skewness_indicator(skewness: float) -> str:
    """Get human-readable skewness indicator.

    Args:
        skewness: Skewness value from scipy.stats.skew

    Returns:
        String like "◀ left-skewed" or "▶ right-skewed" or "● normal"
    """
    if abs(skewness) < 0.5:
        return "● normal"
    elif skewness > 0:
        intensity = "strongly " if abs(skewness) > 2 else ""
        return f"▶ {intensity}right-skewed"
    else:
        intensity = "strongly " if abs(skewness) > 2 else ""
        return f"◀ {intensity}left-skewed"


def print_header_banner(title: str, subtitle: Optional[str] = None) -> None:
    """Print a header banner for console output.

    Args:
        title: Main title text
        subtitle: Optional subtitle
    """
    if RICH_AVAILABLE:
        console = Console()
        banner_text = f"GRD ► {title}"
        if subtitle:
            banner_text += f"\n{subtitle}"
        console.print(Panel(banner_text, style="bold blue"))
    else:
        print("=" * 55)
        print(f" GRD ► {title}")
        if subtitle:
            print(f" {subtitle}")
        print("=" * 55)


def print_tldr(stats: Dict[str, Any]) -> None:
    """Print TL;DR summary section.

    Args:
        stats: Dictionary with keys:
            - rows: int
            - columns: int
            - memory_mb: float
            - missing_pct: float
            - null_columns: int
            - numeric_cols: int
            - categorical_cols: int
            - datetime_cols: int
            - issue_count: int
            - issue_severity: str ('critical', 'warning', 'info')
    """
    rows = stats.get('rows', 0)
    cols = stats.get('columns', 0)
    memory = stats.get('memory_mb', 0)
    missing = stats.get('missing_pct', 0)
    null_cols = stats.get('null_columns', 0)
    numeric = stats.get('numeric_cols', 0)
    categorical = stats.get('categorical_cols', 0)
    datetime = stats.get('datetime_cols', 0)
    issues = stats.get('issue_count', 0)
    severity = stats.get('issue_severity', 'info')

    severity_emoji = {'critical': '🔴', 'warning': '🟡', 'info': '🟢'}.get(severity, '⚪')

    if RICH_AVAILABLE:
        console = Console()
        console.print("\n[bold]## TL;DR[/bold]\n")
        console.print(f"• Rows: {rows:,} | Columns: {cols} | Memory: {memory:.1f} MB")
        console.print(f"• Missing: {missing:.1%} overall | {null_cols} columns have nulls")
        console.print(f"• Types: {numeric} numeric, {categorical} categorical, {datetime} datetime")
        if issues > 0:
            console.print(f"• Issues: {severity_emoji} {issues} {severity} items need attention")
        else:
            console.print("• Issues: ✓ No critical issues detected")
    else:
        print("\n## TL;DR\n")
        print(f"• Rows: {rows:,} | Columns: {cols} | Memory: {memory:.1f} MB")
        print(f"• Missing: {missing:.1%} overall | {null_cols} columns have nulls")
        print(f"• Types: {numeric} numeric, {categorical} categorical, {datetime} datetime")
        if issues > 0:
            print(f"• Issues: {severity_emoji} {issues} {severity} items need attention")
        else:
            print("• Issues: No critical issues detected")


def print_column_table(columns: List[Dict[str, Any]]) -> None:
    """Print column summary table with sparklines.

    Args:
        columns: List of dicts with keys:
            - name: str
            - dtype: str
            - missing_pct: float
            - distribution: List[float] (for sparkline)
            - skewness: Optional[float]
    """
    if RICH_AVAILABLE:
        console = Console()
        table = Table(title="Column Summary")
        table.add_column("Column", style="cyan")
        table.add_column("Type")
        table.add_column("Missing")
        table.add_column("Distribution")

        for col in columns:
            name = col.get('name', '?')
            dtype = col.get('dtype', '?')
            missing = col.get('missing_pct', 0)
            dist = col.get('distribution', [])
            skew = col.get('skewness')

            missing_str = f"{get_quality_indicator(missing, 'missing')} {missing:.0%}"

            sparkline = generate_sparkline(dist) if dist else "—"
            if skew is not None:
                sparkline += f" {get_skewness_indicator(skew)}"

            table.add_row(name, dtype, missing_str, sparkline)

        console.print(table)
    else:
        print("\n## Column Summary\n")
        print(f"{'Column':<20} {'Type':<10} {'Missing':<10} {'Distribution'}")
        print("-" * 60)
        for col in columns:
            name = col.get('name', '?')[:20]
            dtype = col.get('dtype', '?')[:10]
            missing = col.get('missing_pct', 0)
            dist = col.get('distribution', [])

            sparkline = generate_sparkline(dist) if dist else "—"
            print(f"{name:<20} {dtype:<10} {missing:>8.0%}  {sparkline}")


def print_distribution_highlights(highlights: List[Dict[str, Any]]) -> None:
    """Print distribution highlights section.

    Args:
        highlights: List of dicts with keys:
            - column: str
            - skewness: float
            - outliers: int (count)
            - note: Optional[str]
    """
    if not highlights:
        return

    if RICH_AVAILABLE:
        console = Console()
        console.print("\n[bold]## Distribution Highlights[/bold]\n")
        for h in highlights:
            col = h.get('column', '?')
            skew = h.get('skewness', 0)
            outliers = h.get('outliers', 0)
            note = h.get('note', '')

            skew_str = get_skewness_indicator(skew)
            outlier_str = f"🔺 {outliers} outliers" if outliers > 0 else ""

            line = f"• **{col}**: {skew_str}"
            if outlier_str:
                line += f" | {outlier_str}"
            if note:
                line += f" — {note}"

            console.print(Markdown(line))
    else:
        print("\n## Distribution Highlights\n")
        for h in highlights:
            col = h.get('column', '?')
            skew = h.get('skewness', 0)
            outliers = h.get('outliers', 0)

            skew_str = get_skewness_indicator(skew)
            outlier_str = f"| {outliers} outliers" if outliers > 0 else ""

            print(f"• {col}: {skew_str} {outlier_str}")


def print_quality_warnings(warnings: List[Dict[str, Any]]) -> None:
    """Print quality warnings section.

    Args:
        warnings: List of dicts with keys:
            - severity: 'critical' | 'warning' | 'info'
            - message: str
            - column: Optional[str]
    """
    if not warnings:
        return

    severity_emoji = {
        'critical': '🔴',
        'warning': '🟡',
        'info': '🟢'
    }

    if RICH_AVAILABLE:
        console = Console()
        console.print("\n[bold]## Quality Warnings[/bold]\n")
        for w in warnings:
            sev = w.get('severity', 'info')
            msg = w.get('message', '')
            col = w.get('column')

            emoji = severity_emoji.get(sev, '⚪')
            col_str = f"[{col}] " if col else ""

            style = {'critical': 'red', 'warning': 'yellow', 'info': 'green'}.get(sev, 'white')
            console.print(f"{emoji} [{style}]{sev.upper()}[/{style}]: {col_str}{msg}")
    else:
        print("\n## Quality Warnings\n")
        for w in warnings:
            sev = w.get('severity', 'info')
            msg = w.get('message', '')
            col = w.get('column')

            emoji = severity_emoji.get(sev, '')
            col_str = f"[{col}] " if col else ""

            print(f"{emoji} {sev.upper()}: {col_str}{msg}")


def print_footer(report_path: str, next_steps: Optional[List[str]] = None) -> None:
    """Print footer with report location and next steps.

    Args:
        report_path: Path to the generated report
        next_steps: Optional list of suggested next commands
    """
    if RICH_AVAILABLE:
        console = Console()
        console.print("\n" + "─" * 55)
        console.print(f"\n[bold]Report saved:[/bold] {report_path}")

        if next_steps:
            console.print("\n[bold]Next steps:[/bold]")
            for step in next_steps:
                console.print(f"  • {step}")

        console.print("\n" + "─" * 55)
    else:
        print("\n" + "-" * 55)
        print(f"\nReport saved: {report_path}")

        if next_steps:
            print("\nNext steps:")
            for step in next_steps:
                print(f"  • {step}")

        print("\n" + "-" * 55)


def format_number(value: float, precision: int = 2) -> str:
    """Format a number for display with appropriate precision.

    Args:
        value: Number to format
        precision: Decimal places

    Returns:
        Formatted string
    """
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{precision}f}M"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.{precision}f}K"
    elif abs(value) < 0.01 and value != 0:
        return f"{value:.2e}"
    else:
        return f"{value:.{precision}f}"
