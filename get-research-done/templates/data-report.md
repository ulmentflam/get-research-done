# Data Report: {dataset_name}

**Generated:** {timestamp}
**Source:** {file_path_or_paths}
**Sampling:** {sampling_note_if_applicable}

## Data Overview

| Metric | Value |
|--------|-------|
| Total Rows | {count} |
| Total Columns | {count} |
| Memory Usage | {size} |
| File Format | {format} |

### Column Summary

| Column | Type | Non-Null | Unique | Sample Values |
|--------|------|----------|--------|---------------|
| {col} | {dtype} | {count} | {count} | {values} |

## Distributions & Statistics

### Numerical Columns

| Column | Mean | Std | Min | 25% | 50% | 75% | Max |
|--------|------|-----|-----|-----|-----|-----|-----|
| {col} | {val} | {val} | {val} | {val} | {val} | {val} | {val} |

### Categorical Columns

| Column | Unique | Top Value | Frequency |
|--------|--------|-----------|-----------|
| {col} | {count} | {value} | {count} |

## Missing Data Analysis

| Column | Missing Count | Missing % | Pattern | Confidence |
|--------|---------------|-----------|---------|------------|
| {col} | {count} | {pct} | {MCAR/MAR/MNAR} | {HIGH/MEDIUM/LOW} |

**Pattern definitions:**
- **MCAR** (Missing Completely At Random): Missing values are randomly distributed, no correlation with other features
- **MAR** (Missing At Random): Missingness depends on observed data (other features)
- **MNAR** (Missing Not At Random): Missingness depends on the unobserved value itself

## Outlier Detection

### Statistical Outliers

| Column | Method | Outlier Count | % of Total | Severity |
|--------|--------|---------------|------------|----------|
| {col} | Z-score (>3) | {count} | {pct} | {severity} |
| {col} | IQR (1.5x) | {count} | {pct} | {severity} |

**Severity levels:**
- **LOW**: <1% outliers
- **MEDIUM**: 1-5% outliers
- **HIGH**: >5% outliers

### Top Anomalous Values

| Column | Value | Z-score | Reason |
|--------|-------|---------|--------|
| {col} | {val} | {z} | {explanation} |

## Class Balance (if target specified)

**Target Variable:** {target_column}

| Class | Count | Percentage |
|-------|-------|------------|
| {class} | {count} | {pct} |

**Imbalance Ratio:** {ratio}
**Severity:** {LOW/MEDIUM/HIGH}
**Recommendation:** {recommendation}

**Severity thresholds:**
- **LOW**: Ratio <2:1 (acceptable imbalance)
- **MEDIUM**: Ratio 2-10:1 (consider resampling or class weighting)
- **HIGH**: Ratio >10:1 (resampling or specialized techniques required)

## Data Leakage Analysis

### Feature-Target Correlation

| Feature | Correlation | Risk Level | Confidence | Notes |
|---------|-------------|------------|------------|-------|
| {feature} | {corr} | {HIGH/MEDIUM/LOW} | {confidence} | {explanation} |

**Risk thresholds:**
- **HIGH**: Correlation >0.9 (likely leakage)
- **MEDIUM**: Correlation 0.7-0.9 (investigate further)
- **LOW**: Correlation <0.7 (normal relationship)

### High Feature-Feature Correlations

| Feature 1 | Feature 2 | Correlation | Risk |
|-----------|-----------|-------------|------|
| {f1} | {f2} | {corr} | {risk_note} |

**Note:** Correlations >0.95 may indicate redundancy, derived features, or leakage.

### Train-Test Overlap (if multiple files)

| Metric | Value |
|--------|-------|
| Overlapping Rows | {count} |
| Overlap % (Train) | {pct} |
| Overlap % (Test) | {pct} |
| Severity | {severity} |

**Severity thresholds:**
- **LOW**: <1% overlap (minor contamination)
- **MEDIUM**: 1-5% overlap (significant issue)
- **HIGH**: >5% overlap (critical—invalidates evaluation)

### Temporal Leakage Indicators

| Issue | Detected | Confidence | Details |
|-------|----------|------------|---------|
| Future timestamps in features | {yes/no} | {confidence} | {details} |
| Train dates after test dates | {yes/no} | {confidence} | {details} |
| Rolling features computed globally | {unknown} | {confidence} | {details} |

**Common temporal leakage sources:**
- Features computed using future data (e.g., global mean instead of train-only mean)
- Target leakage through time-lagged features
- Features derived from test set statistics

## Recommendations

### Must Address (Blocking)

These issues will cause model failure or produce invalid results:

- [ ] {critical_issue_1}
- [ ] {critical_issue_2}

**Examples of blocking issues:**
- High-confidence data leakage (feature correlates >0.95 with target)
- Train-test overlap >5%
- Target variable has missing values
- Features with 100% missing values

### Should Address (Non-blocking)

These issues will reduce model quality but won't break training:

- [ ] {recommended_issue_1}
- [ ] {recommended_issue_2}

**Examples of non-blocking issues:**
- Missing data <30% (imputation recommended)
- High number of outliers (investigate or clip)
- Class imbalance >5:1 (resampling recommended)
- Low-variance features (consider removal)

### Notes

{additional_observations}

**Common observations:**
- High-cardinality categorical features (may need encoding strategy)
- Skewed distributions (may benefit from transformation)
- Correlated feature groups (consider dimensionality reduction)
- Data quality issues (duplicate rows, inconsistent formatting)

---

*Report generated by GRD Explorer Agent*
*Template: get-research-done/templates/data-report.md*
