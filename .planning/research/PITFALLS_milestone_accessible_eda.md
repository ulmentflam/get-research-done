# Domain Pitfalls: Accessible EDA for Non-Data-Scientists

**Domain:** Adding business-analyst-friendly data insights to ML research framework
**Researched:** 2026-01-30
**Confidence:** HIGH (backed by multiple authoritative sources on BI tools, data literacy research, and statistical communication)

## Executive Summary

Building "plain English" data insights for non-technical users is fraught with unique challenges that go beyond typical software integration. The core tension: **simplification enables access but risks misinterpretation**. This research identifies 3 critical pitfalls (system-breaking), 4 moderate pitfalls (workflow disruption), and 3 minor pitfalls (UX friction) specific to adding `/grd:insights` and accessible EDA to the existing GRD framework.

**Most dangerous finding:** Statistical significance misinterpretation has documented failure rates above 60% even among professionals working with statistics. Automated insights that don't explicitly prevent correlation/causation confusion will cause business decisions based on false patterns.

## Critical Pitfalls

Mistakes that cause rewrites, major failures, or dangerous misuse.

---

### Pitfall 1: The Correlation-Causation Trap in Automated Insights

**What goes wrong:** Automated insight generation presents correlations as actionable findings without causal verification, leading business analysts to make decisions based on spurious patterns.

**Why it happens:**
- Machine learning models naturally identify patterns without distinguishing correlation from causation
- "Plain English" summaries hide statistical nuance by design
- Business analysts lack training to recognize spurious correlations
- Large datasets mathematically guarantee random high correlations ([Airbyte: Spurious Correlations](https://airbyte.com/data-engineering-resources/spurious-correlations))
- One study found "the identical mistake is made thousands of times a day in businesses where statistical analysis is performed" ([Management Consulted](https://managementconsulted.com/correlation-vs-causation/))

**Consequences:**
- Business decisions based on false patterns (e.g., "Sales increased when we hired more engineers" when both correlate with company growth)
- Loss of trust in the tool after recommendations fail
- Legal/compliance risk if insights drive regulated decisions
- Reputational damage if insights contradict domain expertise

**Prevention strategies:**

1. **Explicit causal language gates:**
   - NEVER: "X causes Y to increase"
   - ALWAYS: "X and Y moved together (correlation detected)"
   - Add boilerplate: "Correlation does not prove causation. Verify with domain experts before taking action."

2. **Three-element causation check** (from [DataCamp](https://www.datacamp.com/blog/data-demystified-correlation-vs-causation)):
   - Temporal relationship: Does cause precede effect?
   - Plausible mechanism: Is there a logical explanation?
   - Confounding variables: What else changed simultaneously?
   - Surface these as questions, not assertions

3. **Confidence levels with explicit warnings:**
   ```
   Insight confidence: LOW
   Why: Only 2 months of data, confounding variable detected (marketing campaign),
   no domain expert validation
   Risk: Acting on this insight may lead to incorrect decisions
   ```

4. **Integration with domain knowledge:**
   - Prompt for domain context: "What else was happening during this period?"
   - Flag insights that contradict provided context
   - Require human approval for any causal claim

**Detection warning signs:**
- Insights use language like "because," "caused by," "leads to"
- Business users take action without asking follow-up questions
- Insights suggest interventions without experimental validation
- Tool reports "surprising" correlations frequently

**Phase implications:**
- Phase 1 (Planning): Define causal language policy before any code
- Phase 2 (Core Implementation): Build language filtering and confidence scoring
- Phase 3 (Testing): Red-team with known spurious correlations
- Phase 4 (Documentation): Create "Common Mistakes" guide for users

**Source confidence:** HIGH (multiple academic sources, BI practitioner reports, statistical methodology research)

---

### Pitfall 2: Statistical Significance Theater

**What goes wrong:** Automated insights report "statistically significant" findings without context, causing business analysts to misinterpret p-values, effect sizes, and practical significance.

**Why it happens:**
- P-values are widely misunderstood even by professionals ([PMC: 70%+ misinterpretation rate](https://pmc.ncbi.nlm.nih.gov/articles/PMC9383044/))
- Common misconception: p < 0.05 means "important" or "the finding is true"
- Reality: p-value only measures likelihood under null hypothesis
- "Statistical significance can tell you there's a relationship but not the nature of that relationship" ([Statsig](https://www.statsig.com/perspectives/a-comprehensive-guide-to-statistical-significance))
- Automated systems focus on p < 0.05 threshold rather than effect size or practical impact

**Consequences:**
- Business analysts act on statistically significant but practically meaningless findings
- Small effect sizes (e.g., "2% increase") treated as major discoveries
- False sense of certainty leads to overconfident decisions
- Ignoring effect size means missing actually important changes that don't reach p < 0.05

**Prevention strategies:**

1. **Always report effect size + confidence intervals** ([FigPii recommendations](https://www.figpii.com/blog/misconceptions-about-statistical-significance/)):
   ```
   Finding: Customer satisfaction increased
   Statistical significance: p = 0.03 (yes, statistically significant)
   Effect size: +0.2 points on 10-point scale (2% improvement)
   Confidence interval: 0.1 to 0.3 points
   Practical significance: SMALL - Unlikely to impact business KPIs
   ```

2. **Plain English significance tiers:**
   - **Tiny change:** Detectable but probably not important
   - **Small change:** Noticeable to analysts, may not affect user behavior
   - **Medium change:** Likely to impact business metrics
   - **Large change:** Clear business impact expected

3. **Context-dependent thresholds:**
   - Prompt for "What change would matter for your decision?"
   - Compare effect size to business-meaningful threshold
   - Report: "Change detected (5%) vs. Your threshold (10%): BELOW"

4. **Flag contradictory signals:**
   - "Statistically significant (p=0.04) but effect size is tiny (0.1%)"
   - "Not statistically significant (p=0.08) but effect size is large (15%) - may need more data"

**Detection warning signs:**
- Insights emphasize p-values without effect sizes
- No mention of confidence intervals
- Business users use phrases like "proven" or "definitively shows"
- Reports don't distinguish statistical vs. practical significance

**Phase implications:**
- Phase 1: Define effect size calculation methods per metric type
- Phase 2: Build effect size + CI reporting as mandatory output
- Phase 3: User testing with business analysts - do they understand the difference?
- Phase 4: Create interpretation guide with worked examples

**Source confidence:** HIGH (medical research standards, BI best practices, statistical methodology papers)

---

### Pitfall 3: Integration Breaking Existing Workflows

**What goes wrong:** New accessible EDA features conflict with existing ML research workflows, causing command confusion, state corruption, or breaking the Critic-led recursive loop.

**Why it happens:**
- GRD v1.0 is designed for data scientists (technical, code-first)
- Accessible EDA targets business analysts (non-technical, insight-first)
- Two user personas with conflicting mental models using same system
- Command naming collisions (e.g., `/grd:explore` vs. `/grd:insights` vs. `/grd:quick-explore`)
- State management assumes single-user-type workflows
- Documentation/examples optimized for one persona confuse the other

**Consequences:**
- ML researchers accidentally trigger business-analyst features mid-research loop
- Business analysts invoke technical commands and get cryptic errors
- Critic agent doesn't know how to validate "plain English insights" (designed for code/experiments)
- Session state corruption when switching between personas
- User frustration leads to tool abandonment

**Prevention strategies:**

1. **Explicit persona modes** (from [ADP: HR and IT Alignment](https://www.adp.com/spark/articles/2026/01/hr-and-it-alignment-the-secret-to-seamless-data-integration.aspx)):
   ```bash
   grd init --mode=research    # ML researcher workflows
   grd init --mode=analyst     # Business analyst workflows
   ```
   - Mode determines available commands, templates, language level
   - Prevent cross-persona command invocation
   - Clear visual indicator in all outputs

2. **Namespace isolation:**
   - Research: `/grd:explore`, `/grd:architect`, `/grd:research`, etc.
   - Analyst: `/grd:insights`, `/grd:quick-explore`, `/grd:explain`
   - Shared: `/grd:help`, `/grd:status`

3. **State segregation:**
   - Separate directories: `.grd/research/` vs. `.grd/insights/`
   - Prevent Critic from validating analyst outputs (different criteria)
   - Clear error if wrong persona tries to continue workflow

4. **Modular architecture** ([Zapier: AI Integration](https://zapier.com/blog/ai-integration/)):
   - "Going all-in on one platform can create limited flexibility and higher switching costs"
   - Keep analyst features as optional plugin/module
   - Can be disabled without affecting core research loop
   - Version compatibility between core and modules

5. **Command deprecation strategy:**
   - Audit existing commands: which don't fit research workflows?
   - Explicit deprecation warnings before removal
   - Migration guide for affected users
   - Feature flag system for testing breaking changes

**Detection warning signs:**
- GitHub issues about "command doesn't work as expected"
- Users asking "which command should I use for X?"
- Error logs showing persona-mismatch attempts
- Documentation PRs adding persona clarifications

**Phase implications:**
- Phase 1: Audit existing commands, define persona split
- Phase 2: Implement mode system BEFORE adding analyst features
- Phase 3: Integration testing with both personas
- Phase 4: Clear documentation with persona-specific quick starts

**Source confidence:** MEDIUM (general software integration patterns, BI tool case studies, not specific to this exact scenario)

---

## Moderate Pitfalls

Mistakes that cause delays, technical debt, or user frustration.

---

### Pitfall 4: Jargon Creep in Plain English

**What goes wrong:** "Plain English" insights gradually accumulate statistical jargon as features are added, eventually becoming incomprehensible to business analysts.

**Why it happens:**
- Developers are data scientists who don't realize what's jargon
- Precision pressure: "mean" is clearer than "average" to developers
- Feature complexity increases, tempting technical shortcuts
- No non-technical user on review team to catch it
- Examples: "p-value," "confidence interval," "standard deviation," "normality," "heteroscedasticity"

**Consequences:**
- Business analysts stop using the tool
- Support burden increases (explaining terms)
- Users misinterpret jargon terms
- Defeats the purpose of "accessible" EDA

**Prevention:**

1. **Jargon audit checklist** (mandatory review):
   - Replace "mean" → "average"
   - Replace "standard deviation" → "typical spread" or "how much values vary"
   - Replace "outlier" → "unusual value"
   - Replace "correlation coefficient" → "strength of relationship (0-100%)"
   - Replace "statistically significant" → "unlikely to be random chance"

2. **Non-technical user testing:**
   - Minimum 3 business analysts review every insight template
   - Pass criteria: Can explain finding in their own words without help
   - Fail criteria: Ask "what does X mean?"

3. **Glossary with plain language:**
   - When technical term is unavoidable, provide tooltip/link
   - Example: "confidence interval (how precise this number is)"

4. **LLM prompt engineering for language level:**
   ```python
   system_prompt = """
   You are explaining data insights to a business analyst with no statistics training.
   NEVER use: p-value, standard deviation, variance, regression, coefficient
   ALWAYS use: average, typical, spread, relationship, pattern
   Write at 8th grade reading level. Use analogies.
   """
   ```

**Detection warning signs:**
- User support tickets asking for term definitions
- Business analysts forwarding insights to data scientists for translation
- Low adoption metrics
- User feedback: "too technical"

**Phase implications:**
- Phase 2: Define approved vocabulary list
- Phase 3: Automated jargon detection in CI
- Phase 4: User acceptance testing with business analysts

**Source confidence:** MEDIUM (UX best practices, BI tool reviews, but not specific research studies)

---

### Pitfall 5: Data Literacy Resistance

**What goes wrong:** Business analysts resist adopting the tool despite accessibility features, citing lack of training, executive support, or trust in data quality.

**Why it happens:**
- 75% of employees need data literacy upskilling ([Informatica CDO Report 2026](https://www.informatica.com/about-us/news/news-releases/2026/01/20260127-new-global-cdo-report-reveals-data-governance-and-ai-literacy-as-key-accelerators-in-ai-adoption.html))
- 28% of leaders cite employee resistance as biggest data literacy challenge ([DataCamp](https://www.datacamp.com/blog/what-is-data-literacy-a-comprehensive-guide-for-organizations))
- 65% of data science initiatives meet employee resistance
- Root causes: inadequate training, lack of executive buy-in, fear of looking incompetent

**Consequences:**
- Low adoption despite development investment
- Tool sits unused
- Business analysts continue manual/ad-hoc methods
- No ROI on accessible EDA features

**Prevention:**

1. **Microlearning integration** ([Coursera: Data Literacy 2026](https://www.coursera.org/enterprise/articles/data-literacy)):
   - "Long training sections lead to low memory retention"
   - Embed learning in the tool itself
   - First-use walkthrough with real data
   - Contextual tips during analysis

2. **Executive sponsorship program:**
   - Require executive champion before deployment
   - Success metrics aligned with business KPIs
   - Executive sends "why this matters" message

3. **Trust-building features:**
   - Show data source and freshness: "Based on Q4 2025 sales data (last updated 2026-01-15)"
   - Explain methodology in dropdown: "How we calculated this"
   - Comparison to known benchmarks: "Your average customer value ($50) vs. industry benchmark ($45)"

4. **Gradual complexity ramping:**
   - Level 1: Simple summaries (averages, totals, trends)
   - Level 2: Comparisons and segments
   - Level 3: Statistical tests and confidence
   - User controls progression

**Detection warning signs:**
- Low weekly active users
- High churn after first session
- Support tickets: "Is this data accurate?"
- Users don't trust insights enough to act

**Phase implications:**
- Phase 1: Design onboarding experience
- Phase 3: User testing with business analysts (observed sessions)
- Phase 4: Launch with executive sponsor, not bottom-up

**Source confidence:** HIGH (2026 industry reports, data literacy research)

---

### Pitfall 6: Oversimplification Loses Critical Nuance

**What goes wrong:** Simplifying insights to plain English removes nuance that's essential for correct interpretation, leading to misleading conclusions.

**Why it happens:**
- Accuracy vs. accessibility tradeoff ([Towards Data Science](https://towardsdatascience.com/the-real-challenge-in-data-storytelling-getting-buy-in-for-simplicity/))
- "When you simplify, you make judgment calls about what matters - but stakeholders who don't know you yet won't trust those judgments"
- Pressure to keep insights short (< 2 sentences)
- Missing context about data quality, time periods, segments

**Consequences:**
- Business analysts act on incomplete information
- Decisions ignore important caveats
- Trust erodes when simplified insights prove wrong
- Data scientists disavow the tool

**Prevention:**

1. **Layered disclosure** ([DASCA: Data Storytelling](https://www.dasca.org/world-of-data-science/article/effective-data-storytelling-tips-and-techniques-for-success)):
   - Level 1 (default): Simple summary
   - Level 2 (expandable): Methodology and caveats
   - Level 3 (optional): Full statistical details

   Example:
   ```
   Sales increased 15% in Q4 ▼

   [Expand]
   Caveat: 80% of increase from Black Friday weekend spike
   Excluding that weekend: +3% increase
   Data quality: 2% of transactions missing timestamps
   Time period: Oct 1 - Dec 31, 2025
   Comparison: vs. Q4 2024
   ```

2. **Mandatory context fields:**
   - Time period
   - Comparison baseline
   - Sample size
   - Data quality score
   - Segments included/excluded

3. **Red flag annotations:**
   - "Small sample size - interpret cautiously"
   - "Data quality issue detected in this period"
   - "Trend interrupted by [known event]"

4. **Peer review requirement:**
   - Data scientist spot-checks 10% of automated insights
   - Feedback loop to improve simplification algorithm

**Detection warning signs:**
- Data scientists say insights are "technically wrong"
- Business users surprised by full context
- Insights contradict detailed analysis
- Users forward to data scientists for validation

**Phase implications:**
- Phase 2: Design layered disclosure UI
- Phase 3: A/B test detail levels (too much vs. too little)
- Phase 4: Spot-check review process

**Source confidence:** MEDIUM (data storytelling best practices, expert opinions)

---

### Pitfall 7: The "False Patterns at Scale" Problem

**What goes wrong:** Automated insight generation surfaces spurious correlations as important findings because large datasets mathematically guarantee random correlations.

**Why it happens:**
- "Any sufficiently large dataset will yield strong correlations completely at random" ([Number Analytics](https://www.numberanalytics.com/blog/unmasking-spurious-correlations-statistical-illusions))
- "As datasets grow larger they have to contain arbitrary correlations" ([Cleanlab](https://cleanlab.ai/blog/spurious-correlations/))
- Multiple comparison problem: testing 1000 variables guarantees 50 "significant" findings by chance (p < 0.05)
- Automated systems surface whatever passes threshold, no domain sanity check

**Consequences:**
- Flood of meaningless "insights" drowns real signals
- Business analysts waste time investigating spurious patterns
- Tool loses credibility ("it said X and Y are related but that makes no sense")
- Computational waste generating useless findings

**Prevention:**

1. **Multiple comparison correction:**
   - Bonferroni correction: Adjust p-value threshold by number of tests
   - False Discovery Rate (FDR) control
   - Only surface top N most robust findings

2. **Domain knowledge filtering:**
   - Prompt for "Known relationships to exclude" (e.g., "Time of day and temperature both correlate with many things")
   - Blacklist obviously spurious pairs
   - Require plausible mechanism before reporting

3. **Bootstrapping and permutation tests** ([Number Analytics](https://www.numberanalytics.com/blog/decoding-hidden-spurious-correlations-data-trends)):
   - Shuffle data randomly, recompute correlations
   - If shuffled data shows similar correlation, it's spurious
   - Report: "Correlation strength: 0.7, Robustness: FAIL (found in random shuffles)"

4. **Automated detection with cleanlab:**
   - Use existing tools for spurious correlation detection
   - Pre-filter findings before presenting to users
   - [Cleanlab open-source package](https://cleanlab.ai/blog/spurious-correlations/)

5. **Insight budget:**
   - Limit to top 5-10 findings per analysis
   - Rank by robustness, effect size, and novelty
   - "We tested 500 relationships and found 23 correlations. Here are the 5 most robust."

**Detection warning signs:**
- Users report "weird" or "nonsensical" insights frequently
- Number of insights scales linearly with number of variables
- Insights contradict domain expertise
- Reproducibility issues (insights appear/disappear)

**Phase implications:**
- Phase 2: Implement multiple comparison correction
- Phase 3: Add bootstrapping validation
- Phase 4: User feedback loop to refine filters

**Source confidence:** HIGH (statistical methodology, ML research, automated detection tools)

---

## Minor Pitfalls

Mistakes that cause annoyance or UX friction but are easily fixable.

---

### Pitfall 8: Natural Language Query Frustration

**What goes wrong:** Business analysts struggle to phrase questions in ways the NLQ system understands, leading to irrelevant results or errors.

**Why it happens:**
- "Traditional NLQ has accuracy problems and difficulties answering complex queries" ([Polaris Market Research](https://www.polarismarketresearch.com/blog/ai-powered-bi-market-augmented-analytics-and-natural-language-queries))
- "Users have to learn how to ask the question the right way" ([TechTarget](https://www.techtarget.com/searchbusinessanalytics/feature/What-does-NLP-mean-for-augmented-analytics))
- Query parsing failures on complex or ambiguous questions
- Users don't know what data is available to query

**Prevention:**

1. **Guided NLQ** ([AnswerRocket](https://answerrocket.com/insights/natural-language-guide/)):
   - Suggest example questions
   - Auto-complete based on available data
   - Show query interpretation before executing
   - "Did you mean: [corrected query]?"

2. **Progressive disclosure:**
   - Start: "What data would you like to explore?" [Dropdown: Sales, Customers, Products]
   - Then: "What would you like to know about Sales?" [Suggestions: Trends, Comparisons, Breakdowns]
   - Build query step-by-step rather than free-form

3. **Query feedback loop:**
   - "We interpreted your question as: [SQL/logic]. Is this correct?"
   - Allow refinement before execution
   - Learn from corrections

**Detection warning signs:**
- High query retry rates
- Users give up after 2-3 failed queries
- Support tickets: "How do I ask about X?"

**Phase implications:**
- Phase 2: Guided query builder, not pure NLQ
- Phase 3: User testing with query task scenarios
- Phase 4: Query gallery with common examples

**Source confidence:** MEDIUM (BI vendor case studies, UX patterns)

---

### Pitfall 9: Data Quality Blindness

**What goes wrong:** Automated insights don't surface data quality issues, causing business analysts to act on insights from bad data.

**Why it happens:**
- "Data quality issues degrade accuracy of analysis and BI" ([IBM](https://www.ibm.com/think/insights/data-quality-issues))
- Automated systems assume clean data
- Business analysts lack visibility into data pipeline
- Missing values, duplicates, outliers hidden in aggregations

**Prevention:**

1. **Automatic data quality checks:**
   - Missing value %
   - Duplicate detection
   - Outlier flagging
   - Freshness alerts

2. **Quality score in every insight:**
   ```
   Data quality score: 85/100
   Issues detected:
   - 5% of records missing timestamps
   - 2 duplicate customer IDs found
   - Last updated 3 days ago
   ```

3. **Quality threshold gates:**
   - Refuse to generate insights if quality < threshold
   - "Data quality too low for reliable insights. Fix [issues] first."

**Detection warning signs:**
- Insights change dramatically when data is cleaned
- Users discover data issues after acting on insights
- Reproducibility problems

**Phase implications:**
- Phase 2: Integrate data quality checks
- Phase 3: Define quality thresholds per insight type

**Source confidence:** HIGH (industry reports on data quality)

---

### Pitfall 10: Visualization Overload

**What goes wrong:** Automated insights generate too many charts or use inappropriate chart types, causing confusion rather than clarity.

**Why it happens:**
- "Adding visual complexity to appear sophisticated rather than removing complexity to achieve clarity" ([University at Buffalo](https://research.lib.buffalo.edu/dataviz/best-practices))
- "Too many segments in pie charts - try 3, certainly no more than 6" ([University of Maryland](https://lib.guides.umd.edu/datavisualization/tips))
- Systems generate every possible visualization
- No consideration of user's question or decision context

**Prevention:**

1. **Chart type decision tree:**
   - Comparison: Bar chart
   - Trend over time: Line chart
   - Distribution: Histogram
   - Relationship: Scatter plot
   - Maximum 3 charts per insight

2. **Simplicity rules:**
   - Default to table for < 5 data points
   - Aggregate to top 5-10 categories for large dimensions
   - Progressive disclosure: Summary chart, detail on click

3. **Purpose-driven visualization:**
   - Ask: "What decision does this support?"
   - Only visualize if it aids that decision

**Detection warning signs:**
- Users complain about "too much information"
- Charts with dozens of categories
- Users screenshot and simplify externally

**Phase implications:**
- Phase 2: Define visualization selection logic
- Phase 3: User testing with eye tracking (what do they look at?)

**Source confidence:** HIGH (data visualization research, UX studies)

---

## Phase-Specific Warnings

Mapping pitfalls to development phases where they're most dangerous.

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|----------------|------------|
| **Phase 1: Planning & Design** | Pitfall 3: Integration breaking workflows | Define persona modes and namespaces upfront |
| **Phase 1: Language Policy** | Pitfall 1: Correlation-causation trap | Establish causal language rules BEFORE any code |
| **Phase 2: Core Implementation** | Pitfall 2: Statistical significance theater | Build effect size + CI as mandatory, not optional |
| **Phase 2: NLQ System** | Pitfall 8: Query frustration | Guided query builder, not pure free-form NLQ |
| **Phase 2: Insight Generation** | Pitfall 7: False patterns at scale | Multiple comparison correction from day 1 |
| **Phase 3: User Testing** | Pitfall 4: Jargon creep | Non-technical user reviews catch jargon early |
| **Phase 3: Integration Testing** | Pitfall 3: Breaking existing workflows | Test both personas, ensure isolation |
| **Phase 3: Quality Validation** | Pitfall 6: Oversimplification | A/B test detail levels with business analysts |
| **Phase 4: Launch Strategy** | Pitfall 5: Data literacy resistance | Require executive sponsor + onboarding program |
| **Phase 4: Monitoring** | Pitfall 9: Data quality blindness | Track quality scores, alert on degradation |
| **All Phases** | Pitfall 1, 2, 7: Statistical misuse | Red team every release with known edge cases |

---

## Research Gaps and Future Investigation

Areas where current research was insufficient or requires phase-specific deep dives:

1. **GRD Critic Agent Adaptation:** How should the Critic agent validate "plain English insights" when it's designed for code validation? Needs architectural research in Phase 1.

2. **Mode Switching UX:** If a business analyst discovers they need code-level control mid-analysis, how do they transition to research mode? Needs UX research in Phase 2.

3. **Statistical Rigor vs. Accessibility Tradeoff:** What's the minimum statistical detail required to prevent dangerous misinterpretation? Needs empirical testing in Phase 3.

4. **ML Researcher Adoption of Analyst Features:** Will ML researchers use `/grd:quick-explore` for initial EDA? Or does it threaten their workflow? Needs user research.

5. **Context7 Integration:** Can Context7 provide authoritative answers to business analyst queries about data meaning? Needs technical feasibility assessment.

---

## Sources

### Critical Pitfall Sources (HIGH confidence)

- [Airbyte: What is Spurious Correlation in Statistics](https://airbyte.com/data-engineering-resources/spurious-correlations)
- [Management Consulted: Correlation vs Causation](https://managementconsulted.com/correlation-vs-causation/)
- [DataCamp: Correlation vs. Causation](https://www.datacamp.com/blog/data-demystified-correlation-vs-causation)
- [PMC: Misinterpretations of P-values](https://pmc.ncbi.nlm.nih.gov/articles/PMC9383044/)
- [Statsig: Statistical Significance Guide](https://www.statsig.com/perspectives/a-comprehensive-guide-to-statistical-significance)
- [FigPii: Misconceptions About Statistical Significance](https://www.figpii.com/blog/misconceptions-about-statistical-significance/)
- [Informatica: CDO Report 2026 - AI Literacy](https://www.informatica.com/about-us/news/news-releases/2026/01/20260127-new-global-cdo-report-reveals-data-governance-and-ai-literacy-as-key-accelerators-in-ai-adoption.html)
- [DataCamp: What is Data Literacy? 2026 Guide](https://www.datacamp.com/blog/what-is-data-literacy-a-comprehensive-guide-for-organizations)

### Moderate Pitfall Sources (MEDIUM-HIGH confidence)

- [Polaris: AI-driven BI Market - NLQ Challenges](https://www.polarismarketresearch.com/blog/ai-powered-bi-market-augmented-analytics-and-natural-language-queries)
- [TechTarget: NLP and Augmented Analytics](https://www.techtarget.com/searchbusinessanalytics/feature/What-does-NLP-mean-for-augmented-analytics)
- [Towards Data Science: Simplicity in Data Storytelling](https://towardsdatascience.com/the-real-challenge-in-data-storytelling-getting-buy-in-for-simplicity/)
- [DASCA: Effective Data Storytelling](https://www.dasca.org/world-of-data-science/article/effective-data-storytelling-tips-and-techniques-for-success)
- [Number Analytics: Spurious Correlations](https://www.numberanalytics.com/blog/unmasking-spurious-correlations-statistical-illusions)
- [Cleanlab: Spurious Correlations Detection](https://cleanlab.ai/blog/spurious-correlations/)
- [Coursera: Data Literacy for Business 2026](https://www.coursera.org/enterprise/articles/data-literacy)
- [Zapier: AI Integration Best Practices](https://zapier.com/blog/ai-integration/)
- [ADP: HR and IT Alignment for Data Integration](https://www.adp.com/spark/articles/2026/01/hr-and-it-alignment-the-secret-to-seamless-data-integration.aspx)

### Supporting Sources (MEDIUM confidence)

- [University at Buffalo: Data Visualization Best Practices](https://research.lib.buffalo.edu/dataviz/best-practices)
- [University of Maryland: Data Visualization Tips](https://lib.guides.umd.edu/datavisualization/tips)
- [IBM: Data Quality Issues and Challenges](https://www.ibm.com/think/insights/data-quality-issues)
- [AnswerRocket: Natural Language & NLP Analytics Guide](https://answerrocket.com/insights/natural-language-guide/)
- [SR Analytics: Business Intelligence Trends 2026](https://sranalytics.io/blog/business-intelligence-trends/)

---

**Confidence Summary:**

| Pitfall Category | Overall Confidence | Reasoning |
|------------------|-------------------|-----------|
| Correlation/Causation (1) | HIGH | Multiple academic sources, documented failure rates |
| Statistical Significance (2) | HIGH | Medical research standards, practitioner consensus |
| Integration Breaking (3) | MEDIUM | Software patterns, not domain-specific research |
| Jargon Creep (4) | MEDIUM | UX best practices, lacking empirical studies |
| Data Literacy Resistance (5) | HIGH | 2026 industry reports with specific statistics |
| Oversimplification (6) | MEDIUM | Expert opinion, data storytelling research |
| False Patterns (7) | HIGH | Statistical methodology, automated detection research |
| NLQ Frustration (8) | MEDIUM | BI vendor reports, UX patterns |
| Data Quality (9) | HIGH | Industry reports, technical documentation |
| Visualization (10) | HIGH | Academic research, established guidelines |

**Overall research confidence: HIGH** with caveats for implementation-specific challenges (integration patterns, UX design) that will require validation during development.

---

**Last Updated:** 2026-01-30
