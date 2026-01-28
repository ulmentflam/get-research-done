# Phase 2: Data Reconnaissance - Context

**Gathered:** 2026-01-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Users can analyze raw data and surface anomalies before hypothesis formation. The Explorer agent launches on raw datasets, generates DATA_REPORT.md with distributions, outliers, anomaly flags, and data leakage detection. Creating hypotheses and experiments are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Data input handling
- Interactive prompt when no path provided — detect data files and let user select
- Auto-detect train/test/val splits — if train.csv exists, look for corresponding test.csv/val.csv
- Confirm key columns with user — auto-infer types but ask user to confirm target column, ID columns, with "No target (unsupervised)" as valid option
- Auto-sample large datasets to ~100k rows, note sampling in report
- Support cloud storage (s3://, gs://) using environment defaults (AWS_PROFILE, GOOGLE_APPLICATION_CREDENTIALS)
- Stream and sample for large remote files — don't require full download
- Auto-decompress .csv.gz, .parquet.gz, .zip files transparently
- No caching — fresh analysis every time

### Report content & structure
- Adaptive depth — summary stats by default, --detailed flag for full profiling (histograms, percentiles, skewness, kurtosis)
- Anomalies presented with both statistical summary AND top-N specific examples, ranked by severity
- No visualizations — text/markdown tables only for portability
- Multi-file reports include per-file sections plus explicit comparison/drift analysis section
- Tiered recommendations — must-address issues (blocking) vs nice-to-have suggestions
- Missing data analysis includes counts, pattern analysis (random vs systematic vs correlated), and estimated modeling impact
- Full correlation matrix with all pairwise correlations, highlighting high/problematic correlations

### Leakage detection scope
- Comprehensive leakage checks: feature-target, temporal, train-test overlap, proxy variables, derived features
- Confidence-based severity — risk severity plus confidence score for each detection
- Warn only on leakage — report risks but don't block proceeding (user decides if they matter)

### Gating behavior
- Soft gate — warn if DATA_REPORT.md missing when running /grd:architect, but allow proceeding
- REVISE_DATA routing — when Critic returns REVISE_DATA, route back to Explorer
- Targeted re-check on REVISE_DATA — only re-analyze aspects flagged by Critic, not full re-exploration
- DATA_REPORT.md stored in .planning/ folder alongside other GRD planning docs

### Claude's Discretion
- Data format support (CSV/Parquet as baseline, extend based on common ML patterns)
- Minimal preprocessing to make data readable (encoding, missing headers)
- ID/lookup column detection approach (naming patterns + cardinality)
- Temporal leakage detection aggressiveness
- Reproducibility approach (seeding for determinism)

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-data-reconnaissance*
*Context gathered: 2026-01-28*
