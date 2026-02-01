# Phase 12: Quick Explore - Research

**Researched:** 2026-02-01
**Domain:** Fast EDA with terminal/console output
**Confidence:** HIGH

## Summary

Phase 12 implements a "quick explore" mode as a variant of the existing Explorer agent. This produces fast, console-based EDA summaries optimized for team communication (copy-paste to Slack/docs) rather than comprehensive HTML reports.

**Key findings:**
- Python Rich library is the standard for beautiful terminal output with markdown, tables, emoji, and colors
- Quick EDA tools (ydata-profiling, Sweetviz) exist but generate HTML reports, not console output
- Custom implementation using pandas basic methods with Rich formatting is the right approach
- 60-second target is feasible by skipping expensive operations (detailed histograms, full leakage analysis)
- Sparklines and emoji indicators enhance scannability without requiring charts

**Primary recommendation:** Build mode variant using pandas describe() + Rich formatting. Skip expensive operations (correlation matrices >50 cols, detailed leakage heuristics). Focus on immediate value: data overview, missing values, basic distributions, simple quality flags.

## Standard Stack

The established libraries/tools for terminal-based EDA output:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Rich | 14.1.0+ | Terminal formatting with markdown, tables, colors, emoji | Industry standard for beautiful CLI output (23k+ GitHub stars) |
| pandas | 2.2+ | Data manipulation and basic statistics | Universal data analysis foundation |
| NumPy | 1.26+ | Numerical computations, statistical functions | Core dependency for pandas, scipy |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| sparklines | 3.0+ | Unicode sparkline generation (▁▂▃▅▇) | Distribution visualization in single line |
| scipy | 1.13+ | Statistical tests (skewness, outlier detection) | When basic stats need statistical rigor |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Rich | colorama + termcolor | Rich provides unified API (tables, panels, markdown) vs manual formatting |
| Custom output | ydata-profiling | ydata generates HTML reports, not console output; 10X slower |
| pandas describe() | Sweetviz | Sweetviz produces HTML, requires >10 seconds for small datasets |

**Installation:**
```bash
pip install rich>=14.1.0 pandas>=2.2.0 scipy>=1.13.0 sparklines>=3.0.0
```

## Architecture Patterns

### Recommended Project Structure
```
src/grd/
├── explorer/
│   ├── __init__.py
│   ├── quick.py          # Quick explore mode implementation
│   ├── full.py           # Existing full explorer
│   └── formatters.py     # Rich formatting utilities (tables, indicators)
```

### Pattern 1: Mode Detection with Shared Logic
**What:** Single Explorer agent with mode parameter determining analysis depth
**When to use:** Avoids code duplication, enables shared utilities
**Example:**
```python
# Source: Based on existing grd-explorer.md structure

class ExplorerMode:
    QUICK = "quick"
    FULL = "full"

def explore_data(df: pd.DataFrame, mode: ExplorerMode = ExplorerMode.FULL):
    """Execute exploration with mode-specific depth."""

    # Shared: Data loading and basic profiling
    overview = profile_structure(df)

    if mode == ExplorerMode.QUICK:
        # Quick: Basic stats only
        stats = df.describe()
        missing = df.isnull().sum()

        # Skip: Detailed leakage detection, correlation matrices
        return format_quick_summary(overview, stats, missing)
    else:
        # Full: Comprehensive analysis
        leakage = detect_leakage_comprehensive(df)
        correlations = compute_correlation_matrix(df)

        return generate_data_report(overview, leakage, correlations)
```

### Pattern 2: Rich Console Output with Structured Formatting
**What:** Use Rich's Console, Table, and Panel for beautiful terminal output
**When to use:** All console output for quick explore mode
**Example:**
```python
# Source: https://rich.readthedocs.io/en/stable/console.html

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def print_quick_summary(df, stats, missing):
    """Print formatted quick explore summary."""

    # Header with warning banner
    console.print(Panel(
        "[bold yellow]⚡ Quick Explore[/bold yellow]\n"
        "Run /grd:explore for rigorous analysis",
        style="yellow"
    ))

    # TL;DR prose summary
    tldr = f"Dataset has [bold]{len(df):,}[/bold] rows, [bold]{len(df.columns)}[/bold] columns. "
    tldr += format_notable_issues(df, missing)
    console.print(Markdown(f"## TL;DR\n{tldr}"))

    # One-line-per-column table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Column", style="white")
    table.add_column("Type", style="dim")
    table.add_column("Missing%", justify="right")
    table.add_column("Key Stat", justify="right")
    table.add_column("Indicator", justify="center")

    for col in df.columns:
        missing_pct = (df[col].isnull().sum() / len(df)) * 100
        indicator = get_quality_indicator(df[col], missing_pct)
        key_stat = get_key_stat(df[col])

        table.add_row(
            col,
            str(df[col].dtype),
            f"{missing_pct:.1f}%",
            key_stat,
            indicator
        )

    console.print(table)
```

### Pattern 3: Sparkline Distribution Hints
**What:** Use Unicode block characters to show distribution shape inline
**When to use:** Quick visual indication without generating full histograms
**Example:**
```python
# Source: https://github.com/deeplook/sparklines

from sparklines import sparklines

def generate_sparkline(series: pd.Series) -> str:
    """Generate Unicode sparkline for numerical column."""
    if not pd.api.types.is_numeric_dtype(series):
        return "—"

    # Sample to 20 bins for consistent width
    data = series.dropna()
    if len(data) == 0:
        return "—"

    hist, _ = np.histogram(data, bins=20)
    spark = sparklines(hist)[0]

    return spark

# Usage in table:
# | price | float64 | 2.3% | $45.2 | ▁▂▃▅▇▅▃▂▁ |
```

### Pattern 4: Emoji Quality Indicators
**What:** Use emoji to flag data quality issues prominently
**When to use:** All data quality assessments (missing, outliers, suspicious patterns)
**Example:**
```python
# Source: User CONTEXT decisions + https://github.com/carpedm20/emoji

def get_quality_indicator(series: pd.Series, missing_pct: float) -> str:
    """Return emoji indicator for column quality."""

    # Missing data thresholds
    if missing_pct > 50:
        return "⚠️ HIGH MISSING"
    elif missing_pct > 20:
        return "⚠️ MISSING"

    # Numerical outlier detection (quick Z-score check)
    if pd.api.types.is_numeric_dtype(series):
        z_scores = np.abs((series - series.mean()) / series.std())
        outlier_pct = (z_scores > 3).sum() / len(series) * 100
        if outlier_pct > 5:
            return "⚠️ OUTLIERS"

    # Categorical high cardinality
    if pd.api.types.is_object_dtype(series):
        cardinality = series.nunique() / len(series)
        if cardinality > 0.95:
            return "⚠️ HIGH CARD"

    return "✅"
```

### Pattern 5: Incremental Output for Large Datasets
**What:** Stream results as computed to avoid perception of hanging
**When to use:** Datasets with >50 columns or processing that takes >5 seconds
**Example:**
```python
# Source: Rich documentation on live displays

from rich.live import Live
from rich.progress import Progress

def analyze_columns_incremental(df: pd.DataFrame):
    """Analyze columns with live progress display."""

    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing columns...", total=len(df.columns))

        results = []
        for col in df.columns:
            result = analyze_single_column(df[col])
            results.append(result)
            progress.update(task, advance=1)

    return results
```

### Anti-Patterns to Avoid

- **Generating HTML reports:** Quick explore is console-only for immediate viewing
- **Full correlation matrices:** For >50 columns, correlation computation becomes expensive (>10s)
- **Comprehensive leakage detection:** Statistical tests per column pair is too slow for quick mode
- **Histograms/visualizations:** Terminal doesn't support graphics; use sparklines instead
- **Sampling without notification:** Always inform user if data is sampled (transparency)

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Terminal formatting | ANSI escape codes | Rich library | Rich handles terminal compatibility, width detection, color support detection |
| Sparklines | Unicode character selection | sparklines package | Tufte-style sparklines with proper scaling and binning |
| Statistical outlier detection | Custom Z-score logic | scipy.stats.zscore | Handles edge cases (constant values, NaN, inf) |
| Correlation calculation | Manual covariance/std | pandas.DataFrame.corr() | Optimized implementations, handles missing data |
| Progress indicators | Print statements | Rich.progress | Non-blocking updates, time estimation, clean output |

**Key insight:** Terminal output is harder than it looks. Rich abstracts away:
- Terminal width detection and text wrapping
- Color support detection (256-color vs 16-color vs no color)
- Unicode support detection and fallbacks
- Consistent styling across output types

## Common Pitfalls

### Pitfall 1: Over-optimizing for Speed
**What goes wrong:** Skipping too much analysis produces shallow, unhelpful output
**Why it happens:** Pressure to meet 60-second target leads to removing valuable checks
**How to avoid:** 60-second target is a soft guideline per CONTEXT decisions. Prioritize accuracy over speed.
**Warning signs:**
- Output lacks actionable insights
- Users still need to run full explore immediately after
- Data quality issues go undetected

**From CONTEXT:** "60-second target is soft guideline — accept longer time for accuracy"

### Pitfall 2: Correlation Matrix on Wide Datasets
**What goes wrong:** Computing full correlation matrix on 200+ column dataset takes minutes
**Why it happens:** pandas.DataFrame.corr() is O(n²) in columns
**How to avoid:**
- Set column threshold: skip correlation if >50 columns
- Alternative: compute only top-N correlations with target (if specified)
**Warning signs:**
- Command appears to hang with no output
- Memory usage spikes significantly

**Performance data:** Per pyNetCor benchmarks, pandas correlation on 70,000 features takes >60 minutes vs 21 seconds with optimized tools.

### Pitfall 3: Forgetting to Flag Quick Mode
**What goes wrong:** User trusts quick explore output as comprehensive, misses critical issues
**Why it happens:** Output looks professional and complete
**How to avoid:** Prominent warning banner at top and reminder at bottom
**Warning signs:** Users don't run full explore when they should

**Required per CONTEXT:**
- Header: "⚡ Quick Explore — Run full explore for rigorous analysis"
- Footer: "Run /grd:explore for complete analysis"
- Architect integration: Warning if only quick-explore was run

### Pitfall 4: Emoji Not Displaying
**What goes wrong:** Terminal doesn't support emoji, shows � or boxes
**Why it happens:** Not all terminals support Unicode emoji rendering
**How to avoid:** Rich detects emoji support; use fallback text when unsupported
**Warning signs:** User reports seeing boxes or question marks

```python
# Detection pattern
from rich.console import Console

console = Console()
if console.legacy_windows:
    # Windows legacy terminal - use ASCII
    indicator = "[!]"
else:
    # Modern terminal - use emoji
    indicator = "⚠️"
```

### Pitfall 5: Inconsistent Missing Value Handling
**What goes wrong:** Different columns report different "missing" semantics (NaN, None, "", 0)
**Why it happens:** pandas distinguishes between NaN and empty string
**How to avoid:** Define missing explicitly: `df.replace("", np.nan).replace(" ", np.nan)`
**Warning signs:**
- Missing% doesn't match user's manual count
- String columns show 0% missing but contain empty strings

## Code Examples

Verified patterns from official sources:

### Example 1: Quick Explore Main Flow
```python
# Source: Synthesized from grd-explorer.md + Rich documentation

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import pandas as pd
import numpy as np
from datetime import datetime

console = Console()

def quick_explore(df: pd.DataFrame, target_col: str = None) -> str:
    """
    Execute quick explore workflow.
    Returns: Markdown-formatted string for DATA_REPORT.md
    """

    # 1. Print header banner with warning
    console.print(Panel(
        "[bold yellow]⚡ Quick Explore Mode[/bold yellow]\n\n"
        "Fast analysis for quick familiarization.\n"
        "Run [bold cyan]/grd:explore[/bold cyan] for rigorous, complete analysis.",
        title="Quick Explore",
        border_style="yellow"
    ))

    # 2. Generate TL;DR
    tldr = generate_tldr(df, target_col)
    console.print(Markdown(f"## TL;DR\n{tldr}\n"))

    # 3. Dataset overview table
    print_overview_table(df)

    # 4. Per-column summary (one line per column)
    print_column_summary(df)

    # 5. Distribution patterns (if numerical columns exist)
    if df.select_dtypes(include=[np.number]).shape[1] > 0:
        print_distribution_highlights(df)

    # 6. Data quality warnings
    print_quality_warnings(df)

    # 7. Light suggestions
    print_suggestions(df, target_col)

    # 8. Footer reminder
    console.print("\n[dim]💡 Tip: Run [bold]/grd:explore[/bold] for complete analysis with leakage detection[/dim]\n")

    # 9. Generate markdown for DATA_REPORT.md
    return generate_markdown_output(df, target_col)
```

### Example 2: TL;DR Generation
```python
# Source: User CONTEXT requirement for prose summary

def generate_tldr(df: pd.DataFrame, target_col: str = None) -> str:
    """Generate 2-3 sentence prose summary."""

    # Basic counts
    n_rows = len(df)
    n_cols = len(df.columns)
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    summary = f"Dataset has **{n_rows:,} rows** and **{n_cols} columns** ({memory_mb:.1f} MB). "

    # Notable issues
    issues = []

    # High missing columns
    missing_pcts = (df.isnull().sum() / len(df)) * 100
    high_missing = missing_pcts[missing_pcts > 20]
    if len(high_missing) > 0:
        cols = ", ".join(high_missing.index[:3])
        issues.append(f"high missing in {cols}")

    # Duplicate rows
    n_dupes = df.duplicated().sum()
    if n_dupes > 0:
        pct = (n_dupes / len(df)) * 100
        issues.append(f"{n_dupes:,} duplicate rows ({pct:.1f}%)")

    # Potential outliers (quick check on numerical columns)
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        for col in num_cols[:3]:  # Check first 3 numerical columns
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            outlier_pct = (z_scores > 3).sum() / len(df) * 100
            if outlier_pct > 5:
                issues.append(f"possible outliers in {col}")
                break

    if issues:
        summary += f"**Notable:** {', '.join(issues)}."
    else:
        summary += "No major data quality issues detected."

    return summary
```

### Example 3: One-Line-Per-Column Table
```python
# Source: User CONTEXT decision + Rich Tables documentation

from rich.table import Table
from sparklines import sparklines

def print_column_summary(df: pd.DataFrame):
    """Print one-line-per-column summary table."""

    table = Table(
        title="Column Summary",
        show_header=True,
        header_style="bold cyan",
        border_style="dim"
    )

    table.add_column("Column", style="white", no_wrap=True)
    table.add_column("Type", style="dim", width=12)
    table.add_column("Missing%", justify="right", width=10)
    table.add_column("Key Stat", justify="right", width=15)
    table.add_column("Distribution", justify="center", width=12)
    table.add_column("Indicator", justify="center", width=15)

    for col in df.columns:
        # Basic info
        dtype_str = str(df[col].dtype)
        missing_pct = (df[col].isnull().sum() / len(df)) * 100

        # Key stat (mean for numerical, mode for categorical)
        if pd.api.types.is_numeric_dtype(df[col]):
            key_stat = f"{df[col].mean():.2f}"
        else:
            mode_val = df[col].mode()
            key_stat = str(mode_val[0])[:10] if len(mode_val) > 0 else "—"

        # Distribution sparkline
        dist = generate_sparkline(df[col])

        # Quality indicator with emoji
        indicator = get_quality_indicator(df[col], missing_pct)

        # Add row with conditional styling
        style = "red" if "⚠️" in indicator else None
        table.add_row(col, dtype_str, f"{missing_pct:.1f}%", key_stat, dist, indicator, style=style)

    console.print(table)
```

### Example 4: Skewness Flags
```python
# Source: User CONTEXT requirement for skewness indicators

from scipy.stats import skew

def print_distribution_highlights(df: pd.DataFrame):
    """Print distribution pattern highlights with skewness flags."""

    console.print("\n[bold]Distribution Patterns[/bold]\n")

    num_cols = df.select_dtypes(include=[np.number]).columns

    for col in num_cols:
        data = df[col].dropna()
        if len(data) == 0:
            continue

        # Calculate skewness
        skewness = skew(data)

        # Determine flag
        if abs(skewness) < 0.5:
            flag = "✅ Symmetric"
            color = "green"
        elif skewness > 1:
            flag = "⚠️ Right-skewed"
            color = "yellow"
        elif skewness < -1:
            flag = "⚠️ Left-skewed"
            color = "yellow"
        else:
            flag = "~ Moderate skew"
            color = "white"

        # Print with color
        console.print(f"  [{color}]{col}[/{color}]: {flag} (skew={skewness:.2f})")
```

### Example 5: Memory-Efficient Correlation Filtering
```python
# Source: Avoiding Pitfall 2 (wide datasets)

def compute_top_correlations(df: pd.DataFrame, target_col: str = None, max_cols: int = 50):
    """
    Compute correlations efficiently, skipping if too many columns.
    Returns top correlations with target if specified.
    """

    num_df = df.select_dtypes(include=[np.number])
    n_cols = num_df.shape[1]

    if n_cols > max_cols:
        console.print(f"[yellow]⚠️ Skipping correlation analysis ({n_cols} columns > {max_cols} threshold)[/yellow]")
        return None

    if target_col and target_col in num_df.columns:
        # Compute only target correlations
        corrs = num_df.corr()[target_col].drop(target_col).abs().sort_values(ascending=False)
        return corrs.head(5)
    else:
        # Quick mode: don't compute full matrix
        console.print("[dim]💡 Specify target column for correlation analysis[/dim]")
        return None
```

### Example 6: Leakage Heuristics (Quick Mode)
```python
# Source: User CONTEXT decision + leakage detection research

def detect_leakage_quick(df: pd.DataFrame, target_col: str) -> list:
    """
    Quick leakage detection using basic heuristics.
    Skips expensive statistical tests.
    """

    if not target_col or target_col not in df.columns:
        return []

    warnings = []

    # Heuristic 1: High feature-target correlation (threshold: 0.95)
    num_df = df.select_dtypes(include=[np.number])
    if target_col in num_df.columns:
        corrs = num_df.corr()[target_col].drop(target_col).abs()
        high_corr = corrs[corrs > 0.95]

        for feat, corr_val in high_corr.items():
            warnings.append({
                'type': 'high_correlation',
                'feature': feat,
                'correlation': f"{corr_val:.3f}",
                'note': f"Suspiciously high correlation with target. Verify {feat} is not derived from target."
            })

    # Heuristic 2: Column name patterns suggesting leakage
    leakage_patterns = ['_target', '_label', '_pred', '_score', 'future_', 'next_']
    for col in df.columns:
        if col == target_col:
            continue
        col_lower = col.lower()
        if any(pattern in col_lower for pattern in leakage_patterns):
            warnings.append({
                'type': 'suspicious_name',
                'feature': col,
                'note': f"Column name suggests possible leakage: '{col}'"
            })

    # Heuristic 3: Perfect prediction columns (unique per row with target)
    # Skip: Too expensive for quick mode

    return warnings
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| pandas-profiling HTML reports | Rich terminal output | 2024-2025 | CLI-native workflows; copy-paste friendly for team communication |
| ANSI color codes | Rich library | 2020-2021 | Cross-platform compatibility, automatic fallbacks |
| Manual correlation thresholds | H2O Driverless AI (0.95/0.999) | 2022-2023 | Industry standard thresholds for leakage detection |
| ydata-profiling for all EDA | Mode-specific tools | 2025-2026 | Quick mode for speed, full mode for rigor |

**Deprecated/outdated:**
- **pandas-profiling (old name):** Renamed to ydata-profiling in 2023; use new name
- **colorama for all terminal colors:** Rich supersedes for structured output (tables, panels)
- **Sweetviz with NumPy 2.0:** Compatibility issues; requires NumPy 1.x as of 2026

## Open Questions

Things that couldn't be fully resolved:

1. **Caching for Repeated Runs**
   - What we know: User CONTEXT defers caching decision to Claude's discretion
   - What's unclear: Whether quick-explore is run multiple times on same dataset (workflow pattern)
   - Recommendation: Skip caching in initial implementation. Add if users report repeated runs as pain point.

2. **Leakage Detection Trade-off**
   - What we know: User CONTEXT says "determine what's feasible within speed budget"
   - What's unclear: Exact speed budget after other computations
   - Recommendation: Implement basic heuristics (correlation threshold, name patterns). Skip expensive statistical tests (per-column model training).

3. **Correlation Highlights Feasibility**
   - What we know: User CONTEXT says "determine if top 3-5 correlations are feasible"
   - What's unclear: Performance on wide datasets (100+ columns)
   - Recommendation: Set column threshold (50 cols). If below threshold, compute top-5 correlations with target only. If above, skip with user notification.

4. **Sparkline Library Maturity**
   - What we know: sparklines package exists and generates Tufte-style sparklines
   - What's unclear: Maintenance status, edge case handling
   - Recommendation: Use sparklines package. Wrap in try-except with fallback to "—" if generation fails.

## Sources

### Primary (HIGH confidence)
- [Rich Documentation - Tables](https://rich.readthedocs.io/en/stable/tables.html) - Table API, styling, alignment
- [Rich Documentation - Console API](https://rich.readthedocs.io/en/stable/console.html) - Console methods, emoji support
- [Rich Documentation - Markdown](https://rich.readthedocs.io/en/latest/markdown.html) - Markdown rendering capabilities
- [Rich GitHub Repository](https://github.com/Textualize/rich) - Official source (23k+ stars)
- [sparklines PyPI](https://pypi.org/project/sparklines/) - Sparkline generation library
- [sparklines GitHub](https://github.com/deeplook/sparklines) - Implementation details

### Secondary (MEDIUM confidence)
- [10 Best Python EDA Tools](https://medium.com/top-python-libraries/10-best-python-eda-tools-transform-data-analysis-fast-aa4563174f4e) - EDA tool comparison, DataPrep.EDA performance claims
- [Comparing Five Most Popular EDA Tools](https://towardsdatascience.com/comparing-five-most-popular-eda-tools-dccdef05aa4c/) - ydata-profiling vs Sweetviz comparison
- [Four Common Pitfalls in EDA](https://towardsdatascience.com/four-common-pitfalls-to-avoid-in-exploratory-data-analysis-85d822dd5e34/) - Treating correlation as causation, insufficient cleaning
- [Data Leakage Detection](https://towardsdatascience.com/data-leakage-in-machine-learning-6161c167e8ba/) - High correlation as leakage indicator
- [H2O Driverless AI Leakage Detection](https://docs.h2o.ai/driverless-ai/1-10-lts/docs/userguide/leakage-shift-detection.html) - 0.95 AUC threshold standard
- [pyNetCor Performance Benchmarks](https://academic.oup.com/nargab/article/6/4/lqae177/7928179) - Correlation performance data (pandas 260X slower)
- [Beginner's Guide to EDA - Georgia Tech OMSCS](https://sites.gatech.edu/omscs7641/2026/01/26/eda-for-cs7641/) - 2026 best practices, reproducibility emphasis

### Tertiary (LOW confidence)
- WebSearch results on EDA mistakes - General guidance, no specific methodologies
- WebSearch on emoji terminal output - Library listings, limited technical depth

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Rich is industry standard for terminal output, well-documented
- Architecture: HIGH - Patterns based on existing grd-explorer structure + Rich official examples
- Pitfalls: HIGH - Correlation performance verified with benchmarks; other pitfalls from CONTEXT decisions
- Leakage detection: MEDIUM - Quick heuristics inferred from thresholds in H2O docs, not comprehensive method
- Sparklines: MEDIUM - Library exists and functional, but maturity/edge cases unclear

**Research date:** 2026-02-01
**Valid until:** 2026-04-01 (60 days - stable tools, unlikely to change significantly)
