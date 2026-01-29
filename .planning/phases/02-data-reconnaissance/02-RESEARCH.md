# Phase 2: Data Reconnaissance - Research

**Researched:** 2026-01-28
**Domain:** Data profiling, statistical analysis, and ML data quality assessment
**Confidence:** HIGH

## Summary

Data reconnaissance in ML requires automated statistical profiling, anomaly detection, and data leakage identification before model development. The established approach uses pandas/polars for data handling, statistical methods (Z-score, IQR) for outlier detection, and pattern-based heuristics for leakage detection.

**Key findings:**
- **Pandas 3.0.0** (January 2026) introduces breaking changes including dedicated string dtype and CoW semantics
- **Polars 1.37.1** offers 5-30x performance improvements for large datasets but requires Python 3.10+
- **ydata-profiling 4.18.1** provides one-line EDA but generates HTML reports (user wants markdown-only)
- Cloud streaming via **smart_open 7.5.0** (S3/GCS), **s3fs 2026.1.0**, and **gcsfs 2026.1.0** enables analysis without full downloads
- Reservoir sampling enables unbiased sampling from streams in O(k) memory
- Data leakage detection requires multi-faceted approach: mutual information, duplicate detection, temporal validation

**Primary recommendation:** Use pandas 3.0.0 with pyarrow 23.0.0 backend for data loading, implement custom statistical profiling (don't use ydata-profiling's HTML output), use smart_open for cloud storage streaming, and build pattern-based leakage detection using correlation analysis, duplicate detection, and temporal ordering checks.

## Standard Stack

The established libraries/tools for ML data profiling and reconnaissance:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pandas | 3.0.0 | Data manipulation and analysis | Universal ML data handling library, mature ecosystem |
| pyarrow | 23.0.0 | Parquet I/O, columnar data | Fastest Parquet reader, zero-copy interop, required by pandas 3.0+ |
| numpy | 1.26.0+ | Numerical computation | Dependency for pandas, statistical computations |
| scipy | latest | Statistical functions | zscore, correlation, statistical tests for outlier detection |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| polars | 1.37.1 | Fast dataframe operations | Datasets >1GB, performance-critical profiling, streaming large files |
| smart_open | 7.5.0 | Cloud storage streaming | S3/GCS file access without full download |
| s3fs | 2026.1.0 | S3 filesystem interface | Direct S3:// URL support in pandas |
| gcsfs | 2026.1.0 | GCS filesystem interface | Direct gs:// URL support in pandas |
| scikit-learn | 1.8.0 | Outlier detection algorithms | LOF, Isolation Forest, advanced anomaly detection |
| imbalanced-learn | 0.14.1 | Class imbalance detection | SMOTE variants, imbalance ratio analysis |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pandas | polars | Polars is 5-30x faster but less mature ecosystem, breaking API changes |
| Custom profiling | ydata-profiling | ydata-profiling generates HTML reports (user needs markdown), less control |
| scipy.stats | PyOD | PyOD has 45+ algorithms but overkill for basic profiling, adds complexity |
| smart_open | boto3 directly | boto3 is faster for large uploads but S3-only, no unified API |

**Installation:**
```bash
# Core stack
pip install pandas==3.0.0 pyarrow==23.0.0 numpy>=1.26.0 scipy

# Cloud storage streaming
pip install smart-open[s3,gcs]==7.5.0 s3fs==2026.1.0 gcsfs==2026.1.0

# Optional: performance and advanced detection
pip install polars==1.37.1 scikit-learn==1.8.0 imbalanced-learn==0.14.1
```

## Architecture Patterns

### Recommended Project Structure
```
grd_agents/
├── explorer/                     # Data reconnaissance agent
│   ├── __init__.py
│   ├── loader.py                 # Data loading with cloud support
│   ├── profiler.py               # Statistical profiling
│   ├── anomaly_detector.py       # Outlier and anomaly detection
│   ├── leakage_detector.py       # Data leakage checks
│   └── reporter.py               # Markdown report generation
└── shared/
    ├── sampling.py               # Reservoir sampling utilities
    └── cloud_io.py               # Cloud storage helpers
```

### Pattern 1: Streaming Cloud Data with Sampling
**What:** Stream large files from S3/GCS, apply reservoir sampling, avoid full downloads
**When to use:** Files >100MB on cloud storage, user specifies cloud paths (s3://, gs://)
**Example:**
```python
# Source: smart_open documentation + reservoir sampling pattern
import smart_open
import random

def stream_and_sample(uri: str, sample_size: int = 100000, seed: int = 42) -> list:
    """Reservoir sampling from cloud file without full download."""
    random.seed(seed)
    reservoir = []

    with smart_open.open(uri, 'r', encoding='utf-8') as f:
        # Read header
        header = next(f)

        # Reservoir sampling (Algorithm R)
        for i, line in enumerate(f):
            if i < sample_size:
                reservoir.append(line)
            else:
                # Random index between 0 and i
                j = random.randint(0, i)
                if j < sample_size:
                    reservoir[j] = line

    return [header] + reservoir
```

### Pattern 2: Pandas with PyArrow Backend for Parquet
**What:** Load Parquet files with column selection and filtering to reduce memory
**When to use:** Parquet files, need column subset, want best performance
**Example:**
```python
# Source: Apache Arrow documentation
import pyarrow.parquet as pq
import pandas as pd

def load_parquet_efficient(path: str, columns: list = None, filters: list = None):
    """Load Parquet with filtering and column selection."""
    # Use PyArrow for columnar efficiency
    table = pq.read_table(
        path,
        columns=columns,  # Only load needed columns
        filters=filters,  # Push down predicates
        memory_map=True   # Use memory mapping when possible
    )

    # Convert to pandas with zero-copy when possible
    df = table.to_pandas(
        self_destruct=True,     # Free Arrow memory
        types_mapper=pd.ArrowDtype  # Use Arrow-backed dtypes
    )
    return df
```

### Pattern 3: Memory-Efficient Data Type Optimization
**What:** Downcast numeric types, use categorical for low-cardinality strings
**When to use:** Large datasets, memory constraints, string columns with <50% unique values
**Example:**
```python
# Source: Pandas memory optimization best practices
import pandas as pd
import numpy as np

def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce memory by optimizing data types."""
    for col in df.select_dtypes(include=['int']).columns:
        # Downcast integers
        df[col] = pd.to_numeric(df[col], downcast='integer')

    for col in df.select_dtypes(include=['float']).columns:
        # Downcast floats
        df[col] = pd.to_numeric(df[col], downcast='float')

    for col in df.select_dtypes(include=['object']).columns:
        # Convert to category if cardinality < 50%
        num_unique = df[col].nunique()
        num_total = len(df[col])
        if num_unique / num_total < 0.5:
            df[col] = df[col].astype('category')

    return df
```

### Pattern 4: Statistical Outlier Detection (Z-score + IQR)
**What:** Detect outliers using both Z-score (for normal distributions) and IQR (for skewed)
**When to use:** Numerical columns, need robust outlier detection
**Example:**
```python
# Source: scipy.stats documentation + IQR method
from scipy import stats
import numpy as np

def detect_outliers(series: pd.Series, methods=['zscore', 'iqr']):
    """Detect outliers using multiple methods."""
    outliers = {}

    if 'zscore' in methods:
        # Z-score method (threshold: |z| > 3)
        z_scores = np.abs(stats.zscore(series.dropna()))
        outliers['zscore'] = series[z_scores > 3]

    if 'iqr' in methods:
        # IQR method (more robust for skewed data)
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers['iqr'] = series[(series < lower_bound) | (series > upper_bound)]

    return outliers
```

### Pattern 5: Correlation Matrix with Leakage Detection
**What:** Compute full correlation matrix, flag high correlations as potential leakage
**When to use:** Feature-target correlation analysis, proxy variable detection
**Example:**
```python
# Source: pandas documentation + ML leakage detection patterns
import pandas as pd

def detect_correlation_leakage(df: pd.DataFrame, target_col: str,
                                threshold: float = 0.95):
    """Detect potential data leakage via correlation."""
    # Compute correlation matrix (Pearson for linear relationships)
    corr_matrix = df.select_dtypes(include=[np.number]).corr()

    # Feature-target correlations
    target_corrs = corr_matrix[target_col].drop(target_col).abs()
    high_target_corr = target_corrs[target_corrs > 0.9]

    # Feature-feature correlations (potential proxies)
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                corr_pairs.append({
                    'feature1': corr_matrix.columns[i],
                    'feature2': corr_matrix.columns[j],
                    'correlation': corr_matrix.iloc[i, j],
                    'risk': 'High if one is derived from the other'
                })

    return {
        'high_target_correlation': high_target_corr.to_dict(),
        'high_feature_correlation': corr_pairs
    }
```

### Pattern 6: Train-Test Overlap Detection
**What:** Detect duplicate rows between train/test sets using hashing
**When to use:** Multi-file analysis (train.csv, test.csv), data leakage prevention
**Example:**
```python
# Source: Train-test split best practices
import pandas as pd
import hashlib

def detect_train_test_overlap(train_df: pd.DataFrame, test_df: pd.DataFrame,
                               subset_cols: list = None):
    """Detect overlapping rows between train and test sets."""
    # Hash rows for efficient comparison
    def hash_row(row):
        return hashlib.md5(str(row.values).encode()).hexdigest()

    # Use subset of columns if specified (exclude IDs, timestamps)
    cols = subset_cols or train_df.columns

    train_hashes = set(train_df[cols].apply(hash_row, axis=1))
    test_hashes = set(test_df[cols].apply(hash_row, axis=1))

    overlap = train_hashes & test_hashes

    return {
        'num_overlapping': len(overlap),
        'overlap_pct_train': len(overlap) / len(train_df) * 100,
        'overlap_pct_test': len(overlap) / len(test_df) * 100,
        'severity': 'HIGH' if len(overlap) / len(test_df) > 0.01 else 'LOW'
    }
```

### Pattern 7: Missing Data Pattern Analysis
**What:** Classify missing data as MCAR, MAR, or MNAR using statistical tests
**When to use:** Significant missing data (>5%), need to understand missingness mechanism
**Example:**
```python
# Source: Missing data analysis patterns (MCAR/MAR/MNAR)
import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind

def analyze_missing_patterns(df: pd.DataFrame):
    """Analyze missing data patterns to infer mechanism."""
    missing_analysis = {}

    for col in df.columns:
        if df[col].isnull().sum() > 0:
            # Create missingness indicator
            is_missing = df[col].isnull()

            # Test relationship with other variables (chi-square/t-test)
            relationships = []
            for other_col in df.columns:
                if other_col == col or df[other_col].isnull().all():
                    continue

                if df[other_col].dtype in ['object', 'category']:
                    # Chi-square test for categorical
                    contingency = pd.crosstab(is_missing, df[other_col])
                    chi2, p_value, _, _ = chi2_contingency(contingency)
                    if p_value < 0.05:
                        relationships.append((other_col, 'categorical', p_value))
                else:
                    # T-test for numerical
                    group1 = df[df[col].notnull()][other_col].dropna()
                    group2 = df[df[col].isnull()][other_col].dropna()
                    if len(group1) > 0 and len(group2) > 0:
                        t_stat, p_value = ttest_ind(group1, group2)
                        if p_value < 0.05:
                            relationships.append((other_col, 'numerical', p_value))

            # Infer mechanism
            if len(relationships) == 0:
                mechanism = 'MCAR (Missing Completely At Random)'
                confidence = 'MEDIUM'
            elif len(relationships) < len(df.columns) * 0.2:
                mechanism = 'MAR (Missing At Random)'
                confidence = 'MEDIUM'
            else:
                mechanism = 'MNAR (Missing Not At Random) - investigate further'
                confidence = 'LOW'

            missing_analysis[col] = {
                'missing_count': df[col].isnull().sum(),
                'missing_pct': df[col].isnull().sum() / len(df) * 100,
                'mechanism': mechanism,
                'confidence': confidence,
                'related_variables': [r[0] for r in relationships[:5]]
            }

    return missing_analysis
```

### Anti-Patterns to Avoid

- **Loading entire cloud files locally:** Stream and sample instead to avoid bandwidth/storage costs
- **Using ydata-profiling for markdown reports:** It generates HTML; build custom profiling for markdown output
- **Pandas concat with large files before analysis:** Sample each file first, then compare
- **Z-score on non-normal distributions:** Use IQR method for skewed data
- **Ignoring pandas 3.0 breaking changes:** Copy-on-Write eliminates chained assignment (df[col][row] = value)
- **Missing Column-major operations:** Parquet is columnar; read only needed columns, not full file
- **Not seeding random operations:** Use random seeds for reproducible sampling and shuffling

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Cloud file streaming | Custom boto3/GCS client wrappers | smart_open | Unified API for S3/GCS/Azure, handles retries, compression, buffering |
| Parquet reading | Custom chunked reader | pyarrow.parquet + pandas | Columnar layout optimizations, predicate pushdown, 10-100x faster |
| Reservoir sampling | Custom sampling logic | Standard Algorithm R pattern | Proven unbiased sampling, handles unknown stream lengths, O(k) memory |
| Outlier detection | Custom percentile thresholds | scipy.stats.zscore + IQR | Handles different distributions, established thresholds (3σ, 1.5 IQR) |
| Data type optimization | Manual dtype conversion | pandas downcast + category | Automatic optimization, handles edge cases, 40-60% memory reduction |
| Correlation computation | Manual covariance calculation | pandas.DataFrame.corr() | Optimized implementations, handles missing data, supports Pearson/Spearman/Kendall |
| Train-test overlap | Nested loop comparison | Hash-based set intersection | O(n) vs O(n²), handles large datasets, memory efficient |
| Missing data tests | Manual statistical tests | scipy.stats chi2/t-test | Proper statistical testing, handles edge cases, validated implementations |

**Key insight:** Data profiling has well-established statistical methods and optimized implementations. Custom solutions miss edge cases (missing data, mixed types, memory limits) and are 10-100x slower than optimized libraries.

## Common Pitfalls

### Pitfall 1: Pandas 3.0 Breaking Changes
**What goes wrong:** Code that worked on pandas 2.x fails with pandas 3.0 due to Copy-on-Write and string dtype changes
**Why it happens:** Pandas 3.0 (January 2026) introduces major breaking changes: dedicated string dtype by default, Copy-on-Write semantics enabled, chained assignment no longer works
**How to avoid:**
- Test with pandas 3.0 during development
- Replace `df[col][row] = value` with `df.loc[row, col] = value`
- Handle string dtype explicitly if expecting object dtype
- Use `inplace=True` methods carefully (now return self, not None)
**Warning signs:** SettingWithCopyWarning removed in 3.0, so silent failures possible; type errors with string operations

### Pitfall 2: Memory Exhaustion with Large DataFrames
**What goes wrong:** Loading large CSV/Parquet files crashes with OOM error
**Why it happens:** Default pandas dtypes are inefficient (int64/float64 even for small ranges), loading all columns when only subset needed, holding multiple copies in memory
**How to avoid:**
- Use `usecols` parameter to load only needed columns
- Apply dtype optimization immediately after loading (downcast, categorical)
- Use chunking for operations that don't need full dataset in memory
- Consider polars for datasets >1GB (5-30x less memory)
**Warning signs:** Memory usage >80% system RAM, long load times (>30s for <1GB files)

### Pitfall 3: Sampling Bias in Large Datasets
**What goes wrong:** Naive sampling (e.g., `df.head(100000)`) misses patterns in later data, introduces temporal bias
**Why it happens:** Taking first N rows assumes uniform distribution; data often has temporal ordering, class imbalance that varies over time
**How to avoid:**
- Use reservoir sampling for streams (Algorithm R guarantees uniform probability)
- Use stratified sampling if target variable known: `df.groupby('target').sample(frac=0.1)`
- Document sampling method in report with clear warnings about representativeness
- For temporal data, sample across time periods proportionally
**Warning signs:** Class distributions in sample differ significantly from metadata/documentation

### Pitfall 4: Cloud Storage Streaming Misconfiguration
**What goes wrong:** Cloud file access fails with auth errors, times out, downloads full file despite streaming intent
**Why it happens:** Missing AWS_PROFILE/GOOGLE_APPLICATION_CREDENTIALS env vars, wrong IAM permissions, not using streaming APIs correctly
**How to avoid:**
- Check environment credentials before attempting cloud access
- Use smart_open with explicit credentials parameter if env vars unavailable
- Test with small file first to validate access
- Use `buffering` parameter to control chunk sizes for large files
**Warning signs:** High bandwidth usage, temporary files appearing, 403 Forbidden errors

### Pitfall 5: False Positive Leakage Detection
**What goes wrong:** Leakage detection flags legitimate features as leakage, user loses trust in warnings
**Why it happens:** High correlation ≠ leakage (e.g., temperature in Celsius vs Fahrenheit), timestamp proximity in sequential data is expected, ID columns trigger overlap detection
**How to avoid:**
- Include confidence scores with each leakage detection
- Exclude known ID columns from overlap checks
- Flag but don't block on correlation >0.95 (let user decide)
- For temporal leakage, check if timestamp is actually used for prediction or just indexing
- Provide context: "High correlation detected, check if X is derived from Y"
**Warning signs:** User ignores warnings, disables checks, high false positive rate

### Pitfall 6: Incorrect Missing Data Classification
**What goes wrong:** Treating MAR data as MCAR leads to biased imputation, treating MNAR as MAR hides systematic issues
**Why it happens:** Statistical tests for missingness patterns require sufficient sample size, correlated missingness hard to detect with univariate tests
**How to avoid:**
- Test missingness relationship with ALL other variables, not just obvious ones
- Use multiple tests (chi-square for categorical, t-test for numerical)
- Report confidence levels honestly (LOW when unclear)
- Visualize missing data patterns (heatmap of missingness across rows)
- When in doubt, recommend domain expert consultation
**Warning signs:** Imputation results in unrealistic values, model performance drops on real data

### Pitfall 7: Temporal Leakage in Time-Series Data
**What goes wrong:** Features computed using future information leak into training, causing overoptimistic validation scores but poor production performance
**Why it happens:** Computing rolling statistics before train/test split, using global normalization, sorting data non-chronologically
**How to avoid:**
- Detect datetime columns early in profiling
- Flag any features that could be computed from future data (rolling means, cumulative stats)
- Check if train/test split respects temporal ordering
- Warn if test data has timestamps before train data timestamps
- For multi-file analysis, compare timestamp ranges across files
**Warning signs:** Perfect or near-perfect correlations with target in validation, timestamp columns present

## Code Examples

Verified patterns from official sources:

### Loading Cloud Data with Smart Open
```python
# Source: smart_open PyPI documentation
import smart_open

# Works for s3://, gs://, http://, local paths
# Transparent compression handling (.gz, .bz2, .zst)
with smart_open.open('s3://bucket/data.csv.gz', 'r', encoding='utf-8') as f:
    for line in f:
        process(line)  # Stream processing without full download

# Integration with pandas
import pandas as pd
df = pd.read_csv('s3://bucket/data.csv', storage_options={'key': 'xxx', 'secret': 'yyy'})
```

### Reading Parquet with Column Selection
```python
# Source: Apache Arrow v23.0.0 documentation
import pyarrow.parquet as pq

# Only read needed columns (columnar efficiency)
table = pq.read_table('data.parquet', columns=['feature1', 'feature2', 'target'])

# Apply filters before reading (predicate pushdown)
table = pq.read_table('data.parquet',
                      filters=[('feature1', '>', 0), ('feature1', '<', 100)])

# Memory-map for better performance
table = pq.read_table('data.parquet', memory_map=True)
```

### Pandas Correlation Matrix
```python
# Source: pandas 3.0.0 documentation
import pandas as pd

# Pearson correlation (linear relationships)
corr_pearson = df.corr(method='pearson')

# Spearman correlation (rank-based, handles non-linear monotonic)
corr_spearman = df.corr(method='spearman')

# Kendall tau (rank-based, more robust to outliers but slower)
corr_kendall = df.corr(method='kendall', min_periods=100)

# For large datasets, sample before computing Kendall (O(n²) complexity)
if len(df) > 10000 and method == 'kendall':
    sample_df = df.sample(n=10000, random_state=42)
    corr_kendall = sample_df.corr(method='kendall')
```

### Class Imbalance Detection
```python
# Source: imbalanced-learn documentation + ML best practices
import pandas as pd

def detect_class_imbalance(df: pd.DataFrame, target_col: str):
    """Detect and report class imbalance."""
    value_counts = df[target_col].value_counts()
    value_props = df[target_col].value_counts(normalize=True)

    # Calculate imbalance ratio (minority/majority)
    minority_count = value_counts.min()
    majority_count = value_counts.max()
    imbalance_ratio = minority_count / majority_count

    # Severity classification
    if imbalance_ratio > 0.5:
        severity = 'LOW'
        recommendation = 'No action needed'
    elif imbalance_ratio > 0.1:
        severity = 'MEDIUM'
        recommendation = 'Consider stratified sampling or class weights'
    else:
        severity = 'HIGH'
        recommendation = 'Strong imbalance detected. Consider SMOTE, undersampling, or specialized algorithms'

    return {
        'distribution': value_props.to_dict(),
        'imbalance_ratio': imbalance_ratio,
        'severity': severity,
        'recommendation': recommendation,
        'num_classes': len(value_counts)
    }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| pandas 2.x with object dtype strings | pandas 3.0 with dedicated str dtype | January 2026 | Faster string ops, type safety, breaking change for mixed-type columns |
| pandas-profiling | ydata-profiling | 2023 (renamed) | Adds Spark support, but still HTML-only output |
| Manual boto3 for cloud | smart_open unified API | Active 2025-2026 | Single API for S3/GCS/Azure, less boilerplate |
| PyArrow optional dependency | PyArrow required for pandas 3.0 | January 2026 | Faster I/O, better memory efficiency, Arrow ecosystem interop |
| View vs copy uncertainty | Copy-on-Write (CoW) default | pandas 3.0 | Eliminates SettingWithCopyWarning, breaks chained assignment |
| pytz for timezones | zoneinfo (stdlib) default | pandas 3.0 | pytz now optional, faster and stdlib-based |
| Isolation Forest (sklearn) | ECOD (PyOD) for outliers | 2025+ research | ECOD faster, parameter-free, but sklearn Isolation Forest still widely used |
| 10-fold CV for time series | Time-based 2-way/3-way splits | 2024-2025 research | Prevents future leakage, more robust validation |

**Deprecated/outdated:**
- pandas-profiling: Renamed to ydata-profiling in 2023
- pandas 2.x copy/view behavior: Eliminated by CoW in 3.0
- pytz as required dependency: Now optional, use zoneinfo
- s3fs for performance: Still slower than boto3 for large uploads (3x), use boto3.upload_file() for >1GB files

## Open Questions

Things that couldn't be fully resolved:

1. **Optimal sampling threshold for "large" datasets**
   - What we know: 100k rows commonly used, fits in memory for most analyses
   - What's unclear: Depends on column count, data types, operation complexity
   - Recommendation: Use 100k as default, make configurable, document in report

2. **Leakage detection aggressiveness (false positive rate)**
   - What we know: High correlation (>0.95) indicates potential leakage, but can be legitimate
   - What's unclear: Optimal threshold varies by domain (e.g., finance vs NLP)
   - Recommendation: Use 0.95 for feature-feature, 0.90 for feature-target, include confidence scores

3. **MissMecha library maturity**
   - What we know: Released August 2025, offers MCAR/MAR/MNAR testing
   - What's unclear: Production readiness, community adoption, maintenance status
   - Recommendation: Implement manual statistical tests (chi-square/t-test) initially, monitor MissMecha for future adoption

4. **Polars vs pandas trade-offs for this use case**
   - What we know: Polars 5-30x faster, but less mature, breaking changes likely
   - What's unclear: Worth the migration risk for data profiling (not model training)?
   - Recommendation: Start with pandas 3.0 + PyArrow backend, add polars as optional for large files (>1GB)

5. **Temporal leakage detection specificity**
   - What we know: Need to check timestamp ordering, rolling features, future information
   - What's unclear: How to detect implicit temporal leakage (e.g., feature X computed from future data but no timestamp column)
   - Recommendation: Focus on explicit checks (timestamp ordering, train/test date ranges), flag derived features for manual review

## Sources

### Primary (HIGH confidence)
- [Pandas 3.0.0 Release Notes](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html) - Breaking changes, new features
- [Apache Arrow Parquet Documentation v23.0.0](https://arrow.apache.org/docs/python/parquet.html) - Parquet reading best practices
- [smart_open 7.5.0 PyPI](https://pypi.org/project/smart-open/) - Cloud storage streaming
- [ydata-profiling Documentation](https://docs.profiling.ydata.ai/) - Automated profiling features
- [pandas.DataFrame.corr() Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html) - Correlation methods
- [scikit-learn 1.8.0 Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html) - LOF, Isolation Forest
- [imbalanced-learn 0.14.1 SMOTE](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html) - SMOTE documentation

### Secondary (MEDIUM confidence)
- [Polars Changelog](https://docs.pola.rs/releases/changelog/) - Version 1.37.1 features
- [Pandas Memory Optimization Guide](https://towardsdatascience.com/seven-killer-memory-optimization-techniques-every-pandas-user-should-know-64707348ab20) - Optimization techniques
- [Avoiding Data Leakage in Timeseries](https://towardsdatascience.com/avoiding-data-leakage-in-timeseries-101-25ea13fcb15f) - Temporal leakage patterns
- [Reservoir Sampling Explained](https://medium.com/pythoneers/dipping-into-data-streams-the-magic-of-reservoir-sampling-762f41b78781) - Algorithm R implementation
- [Statistical Outlier Detection Methods](https://towardsdatascience.com/3-simple-statistical-methods-for-outlier-detection-db762e86cd9d) - Z-score, IQR, Modified Z-score
- [MissMecha Package](https://arxiv.org/html/2508.04740v1) - MCAR/MAR/MNAR testing (August 2025)

### Tertiary (LOW confidence)
- [Hidden Leaks in Time Series Forecasting](https://arxiv.org/html/2512.06932v1) - LSTM leakage research (December 2025)
- [Pandas vs Polars Benchmarks](https://learn-big-data-on-aws.readthedocs.io/02-Best-Practices/Polars-vs-Pandas-Benchmark-in-AWS-Lambda/) - Performance comparisons
- WebSearch results on data profiling best practices 2026 - Multiple sources, cross-referenced

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - pandas 3.0, pyarrow 23.0, smart_open verified from official docs and PyPI
- Architecture patterns: HIGH - Based on official documentation and established ML practices
- Pitfalls: HIGH - pandas 3.0 breaking changes documented, memory/leakage issues from multiple sources
- Leakage detection: MEDIUM - Patterns established but optimal thresholds domain-dependent
- Missing data analysis: MEDIUM - MissMecha library new (Aug 2025), statistical tests well-established

**Research date:** 2026-01-28
**Valid until:** 2026-04-28 (90 days - pandas ecosystem relatively stable, but pandas 3.0 is new major version)

**Critical notes:**
- Pandas 3.0.0 released January 21, 2026 - very recent, expect ecosystem catching up
- User decisions from CONTEXT.md constrain approach: markdown-only reports (no ydata-profiling HTML), cloud streaming required, no caching
- Polars ecosystem less mature but significantly faster - recommend as optional dependency for large files
- Data leakage detection requires pattern-based heuristics, not a single library solution
