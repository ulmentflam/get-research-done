# Quick Task 001: Sample CSV Data Exploration

**Dataset:** `.planning/test-data/sample.csv`
**Analysis Date:** 2026-02-01
**Purpose:** Understand customer purchase data structure and characteristics

---

## Data Overview

**Shape:**
- **Rows:** 100 customers
- **Columns:** 8 features

**Column Schema:**
| Column | Type | Description |
|--------|------|-------------|
| `id` | int64 | Unique customer identifier (1-100) |
| `age` | int64 | Customer age in years |
| `income` | int64 | Annual income in USD |
| `category` | object | Purchase category (electronics, clothing, home) |
| `purchase_amount` | float64 | Purchase value in USD |
| `is_premium` | int64 | Premium membership flag (0=no, 1=yes) |
| `signup_date` | datetime64[ns] | Customer signup date |
| `region` | object | Geographic region (north, south, east, west) |

---

## Numeric Statistics

### Age
- **Range:** 21 - 56 years
- **Mean:** 37.1 years
- **Median:** 36.0 years
- **Std Dev:** 9.9 years
- **Quartiles:** Q1=29, Q2=36, Q3=45

**Interpretation:** Broad age distribution suggests diverse customer base spanning young adults to middle-aged consumers.

### Income
- **Range:** $35,000 - $122,000
- **Mean:** $76,390
- **Median:** $76,000
- **Std Dev:** $24,209

**Interpretation:** Middle to upper-middle income bracket with balanced distribution around median.

### Purchase Amount
- **Range:** $42.00 - $899.00
- **Mean:** $290.90
- **Median:** $210.00
- **Std Dev:** $211.66

**Interpretation:** Wide range of purchase values with right-skewed distribution (mean > median), indicating some high-value outliers.

---

## Categorical Distributions

### Category (Purchase Type)
| Category | Count | Percentage | Avg Purchase |
|----------|-------|------------|--------------|
| Electronics | 34 | 34.0% | $341.24 |
| Clothing | 33 | 33.0% | $105.98 |
| Home | 33 | 33.0% | $423.95 |

**Interpretation:** Perfectly balanced category distribution. Home purchases have highest average value, clothing has lowest.

### Region (Geographic)
| Region | Count | Percentage |
|--------|-------|------------|
| North | 25 | 25.0% |
| South | 25 | 25.0% |
| East | 25 | 25.0% |
| West | 25 | 25.0% |

**Interpretation:** Perfectly balanced regional distribution - likely synthetic data for testing.

### Premium Status
| Status | Count | Percentage | Avg Purchase | Avg Income | Avg Age |
|--------|-------|------------|--------------|------------|---------|
| Non-Premium (0) | 56 | 56.0% | $180.76 | $59,929 | 30.3 years |
| Premium (1) | 44 | 44.0% | $431.08 | $97,341 | 45.7 years |

**Interpretation:** Premium customers are older, wealthier, and spend 2.4x more per purchase.

---

## Date Analysis

### Signup Date Range
- **Earliest:** 2023-09-20
- **Latest:** 2024-03-28
- **Date Range:** 190 days (approximately 6 months)

### Monthly Signup Distribution
| Month | Signups |
|-------|---------|
| 2023-09 | 2 |
| 2023-10 | 7 |
| 2023-11 | 9 |
| 2023-12 | 9 |
| 2024-01 | 26 |
| 2024-02 | 24 |
| 2024-03 | 23 |

**Interpretation:** Strong growth trend with signups accelerating from Q4 2023 into Q1 2024 (3x increase).

---

## Key Insights

### 1. Strong Income-Purchase Correlation (r = 0.747)
Higher income customers make significantly larger purchases. This strong positive correlation suggests purchase amount could be predicted from income level with reasonable accuracy.

### 2. Premium Customer Segmentation
Premium customers exhibit distinct characteristics:
- **15 years older** on average (45.7 vs 30.3)
- **62% higher income** ($97,341 vs $59,929)
- **138% larger purchases** ($431 vs $181)

This suggests premium status is driven by age and income, and premium members have substantially higher lifetime value.

### 3. Category-Specific Spending Patterns
Purchase amounts vary significantly by category:
- **Home goods:** Highest average ($424) - big-ticket items
- **Electronics:** Mid-range ($341) - gadgets, devices
- **Clothing:** Lowest average ($106) - frequent smaller purchases

This indicates different customer value propositions and marketing strategies may be needed per category.

### 4. Data Quality: Perfect Cleanliness
- **Zero missing values** across all columns
- **No duplicate IDs** detected
- **Valid date ranges** (all within 6-month window)
- **Perfectly balanced** categorical distributions

**Note:** This level of cleanliness and balance suggests this is synthetic test data, ideal for algorithm testing but may not reflect real-world messiness.

### 5. Growth Trajectory
Customer acquisition accelerated significantly in early 2024, with January-March averaging 24 signups/month vs. 6.75/month in September-December 2023. This 3.6x growth suggests successful marketing campaign or product-market fit.

### 6. Age Demographics Favor Premium Conversion
The 15-year age gap between premium and non-premium customers suggests a lifecycle opportunity: as the younger (30-year-old) cohort ages into their 40s with increasing income, they become prime targets for premium conversion campaigns.

---

## Data Quality Assessment

**Completeness:** ✓ Perfect (0% missing values)
**Consistency:** ✓ All data types appropriate
**Validity:** ✓ All values within expected ranges
**Uniqueness:** ✓ No duplicate customer IDs
**Accuracy:** ⚠️ Appears synthetic (perfect balance)

---

## Recommended Next Steps

1. **Predictive Modeling:** Build purchase amount predictor using income, age, premium status
2. **Segmentation Analysis:** K-means clustering to identify customer segments beyond premium/non-premium
3. **Premium Conversion:** Analyze non-premium customers aged 35+ with income >$75k as conversion targets
4. **Category Deep-Dive:** Investigate why home goods command 4x higher prices than clothing
5. **Seasonality Testing:** With more date range, examine monthly/seasonal purchase patterns

---

**Analysis completed:** 2026-02-01
**Tools used:** Python 3, pandas, numpy
**Dataset size:** 100 rows × 8 columns (100% clean)
