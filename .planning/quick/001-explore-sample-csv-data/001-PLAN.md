---
phase: quick
plan: 001
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/quick/001-explore-sample-csv-data/001-SUMMARY.md
autonomous: true

must_haves:
  truths:
    - "Data shape and types are documented"
    - "Descriptive statistics for numeric columns exist"
    - "Category distributions are summarized"
    - "Key insights and anomalies are identified"
  artifacts:
    - path: ".planning/quick/001-explore-sample-csv-data/001-SUMMARY.md"
      provides: "Complete data exploration summary"
      contains: "## Data Overview"
  key_links: []
---

<objective>
Explore the sample CSV dataset and generate a comprehensive data summary.

Purpose: Understand the structure, distributions, and characteristics of the customer purchase data.
Output: A summary document with statistics, distributions, and initial insights.
</objective>

<execution_context>
This is a quick exploration task - no research phase, single focused execution.
</execution_context>

<context>
@.planning/test-data/sample.csv
</context>

<tasks>

<task type="auto">
  <name>Task 1: Analyze CSV structure and generate exploration summary</name>
  <files>.planning/quick/001-explore-sample-csv-data/001-SUMMARY.md</files>
  <action>
Read and analyze .planning/test-data/sample.csv to produce a data exploration summary:

1. **Data Shape**: Document row count (100), column count (8), column names and inferred types

2. **Numeric Columns** (age, income, purchase_amount):
   - Min, max, mean, median, standard deviation
   - Note any outliers or unusual distributions

3. **Categorical Columns** (category, region, is_premium):
   - Value counts and percentages
   - category: electronics, clothing, home
   - region: north, south, east, west
   - is_premium: 0/1 binary flag

4. **Date Column** (signup_date):
   - Date range (earliest to latest)
   - Distribution across months

5. **Key Insights**:
   - Correlation observations (e.g., income vs purchase_amount, age vs is_premium)
   - Any notable patterns or segments
   - Data quality notes (missing values, anomalies)

Use Python with pandas for the analysis. Write results to the summary file.
  </action>
  <verify>
File exists: .planning/quick/001-explore-sample-csv-data/001-SUMMARY.md
Contains sections: Data Overview, Numeric Statistics, Categorical Distributions, Insights
  </verify>
  <done>
Summary document contains complete data profile with statistics for all 8 columns, distribution summaries, and at least 3 key insights about the data.
  </done>
</task>

</tasks>

<verification>
- Summary file exists and is readable
- All 8 columns are documented
- Numeric statistics are accurate
- Category counts match source data
</verification>

<success_criteria>
- Complete data exploration summary in 001-SUMMARY.md
- Numeric columns have min/max/mean/median/std
- Categorical columns have value counts
- At least 3 insights or observations documented
</success_criteria>

<output>
After completion, the summary will be at:
`.planning/quick/001-explore-sample-csv-data/001-SUMMARY.md`
</output>
