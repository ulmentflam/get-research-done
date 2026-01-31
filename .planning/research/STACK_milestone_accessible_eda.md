# Technology Stack: Accessible EDA for Business Analysts

**Project:** GRD v1.1 - Accessible EDA Feature
**Researched:** 2026-01-30
**Focus:** Plain English data insights for non-technical users
**Confidence:** HIGH (verified with official documentation and recent 2026 sources)

## Executive Summary

The accessible EDA feature requires a **two-layer architecture**: (1) LLM-powered natural language generation to transform statistical findings into business insights, and (2) optional automated EDA libraries for rapid visual exploration. The Explorer agent already performs comprehensive statistical analysis (pandas, scipy) - the new feature layer sits on top, translating technical findings into accessible narratives.

**Core recommendation:** Use direct LLM prompting with structured templates (Claude via existing MCP integration) for insight generation. Avoid heavy automated EDA libraries in the critical path - they create installation friction and generate HTML reports unsuitable for terminal-based workflows.

---

## Recommended Stack

### 1. Natural Language Insight Generation (REQUIRED)

| Component | Version | Purpose | Integration Point |
|-----------|---------|---------|-------------------|
| **Claude API** | Latest (via MCP) | Transform statistical analysis into plain English insights | Existing GRD MCP integration |
| **Structured prompts** | Custom templates | Convert DATA_REPORT.md sections to business-friendly summaries | New prompt engineering module |

**Why this approach:**
- Zero new dependencies (uses existing Claude Code MCP)
- Terminal-native output (no HTML reports)
- Full control over narrative tone and depth
- Iterative refinement based on user feedback
- Maintains GRD's lightweight philosophy

**How it works:**
```python
# Pseudocode flow
statistical_analysis = explorer_agent.analyze(df)  # Existing
business_insights = insight_generator.translate(
    statistical_analysis,
    audience="business_analyst",
    tone="conversational",
    depth="executive_summary"
)
```

**Prompt engineering pattern (verified via 2026 research):**
- **Role-based prompting**: "You are a data analyst explaining findings to a business stakeholder"
- **Structured output**: Request specific sections (Key Findings, Business Impact, Recommendations)
- **Step-by-step reasoning**: Chain-of-thought for complex statistical interpretations
- **Context injection**: Include domain context from PROJECT.md

---

### 2. Data Summary Utilities (OPTIONAL, for quick-explore command)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **skimpy** | 0.0.20 (Jan 2026) | Console-based data summaries | Terminal output for `/grd:quick-explore` |
| **great-tables** | 0.20.0 (Oct 2025) | Publication-quality tables | Professional reports if needed |

**Why skimpy:**
- Python >=3.10 (compatible with GRD's existing environment)
- Terminal-native output (no browser pop-ups)
- Lightweight alternative to `df.describe()` with better formatting
- MIT license, production-stable
- Recent release (Jan 2026) shows active maintenance

**Why great-tables:**
- Python >=3.9 (broad compatibility)
- Styled output for formal reports
- Integrates with pandas DataFrames
- Active development (Oct 2025 release)

**Installation:**
```bash
pip install skimpy>=0.0.20 great-tables>=0.20.0
```

---

### 3. Automated EDA Libraries (NOT RECOMMENDED for v1.1)

**Evaluated but excluded:**

| Library | Latest Version | Python Support | Why Excluded |
|---------|---------------|----------------|--------------|
| **ydata-profiling** | 4.18.1 (Jan 2026) | >=3.10, <3.14 | Heavy dependencies, slow on large datasets, HTML-only output |
| **Sweetviz** | 2.3.1 (Nov 2023) | >=3.7 | NumPy 2.0 compatibility issues, stale (2023) |
| **D-Tale** | 3.19.1 (Jan 2026) | 2.7-3.11 | Flask/React dependency, browser-based UI, overkill for terminal workflow |
| **DataPrep** | 0.4.5 (Aug 2022) | >=3.8, <3.11 | Stale (2022), Dask dependency for "10x performance" not needed |
| **PandasAI** | 3.0.0 (Jan 2026) | >=3.8, <=3.11 | External LLM API calls, not integrated with GRD's MCP, query-based not report-based |
| **LIDA** | Latest | >=3.10 | Visualization-focused, grammar-agnostic code generation inappropriate for data insights |

**Why not automated EDA libraries:**
1. **Installation friction**: Heavy dependencies (Flask, React, Dask) conflict with GRD's lightweight philosophy
2. **Output mismatch**: HTML reports don't fit terminal-based research workflows
3. **Slow performance**: Tools like ydata-profiling are 10x slower than DataPrep, which itself is overkill
4. **Workflow disruption**: Browser pop-ups (D-Tale, Sweetviz) break terminal focus
5. **Maintenance risk**: Several libraries stale (Sweetviz 2023, DataPrep 2022) or have compatibility issues
6. **Wrong abstraction**: These tools are designed for initial exploration, not layering insights on existing analysis

**Key insight from research:**
> "Automated reports are powerful, but they're not a silver bullet, and sometimes you still need to perform your own EDA to make sure everything is going as planned." ([The Lazy Data Scientist's Guide](https://www.kdnuggets.com/the-lazy-data-scientists-guide-to-exploratory-data-analysis))

GRD already performs thorough manual EDA via the Explorer agent. The v1.1 goal is **insight translation**, not **EDA automation**.

---

## Architecture: Insight Generation Module

### Module Structure

```
src/grd/insights/
├── __init__.py
├── templates.py          # Prompt templates for different audiences
├── generator.py          # LLM interaction via MCP
├── formatters.py         # Terminal-friendly output formatting
└── summarizers.py        # Statistical summary aggregation
```

### Integration with Existing Stack

**Existing Explorer agent stack (DO NOT change):**
- pandas (data manipulation)
- scipy (statistical tests)
- numpy (numerical operations)
- pyarrow (Parquet support)
- smart_open (cloud storage)

**New insight layer (minimal addition):**
- skimpy (optional, for quick summaries)
- great-tables (optional, for styled reports)
- Custom prompt templates (core requirement)

**Data flow:**
```
1. Explorer agent generates DATA_REPORT.md (existing)
   ├─ Statistical analysis (pandas, scipy)
   ├─ Leakage detection (correlation matrices)
   └─ Recommendations (severity-tiered)

2. Insight generator reads DATA_REPORT.md (new)
   ├─ Parse structured sections
   ├─ Extract key metrics
   └─ Send to Claude via MCP with prompt template

3. Claude returns plain English insights (new)
   ├─ Executive summary
   ├─ Key findings in business terms
   ├─ Action items with rationale
   └─ Risk assessment in accessible language

4. Formatter outputs to terminal (new)
   ├─ Markdown formatting
   ├─ Color-coded severity indicators
   └─ Collapsible technical details
```

---

## Prompt Engineering Strategy

### Template Categories

**1. Executive Summary Template**
```
Role: You are a senior data analyst presenting findings to C-suite executives.

Context:
- Dataset: {dataset_name}
- Rows: {row_count:,}
- Purpose: {project_goal}

Statistical Findings:
{data_report_excerpt}

Task:
Generate a 3-5 sentence executive summary explaining:
1. What the data shows
2. Most critical insight (in business terms)
3. Recommended next action

Tone: Professional, confident, jargon-free
Audience: Business stakeholders with no technical background
```

**2. Accessible Insights Template**
```
Role: You are a data storyteller explaining technical findings to business analysts.

Context:
- Dataset: {dataset_name}
- Analysis: {analysis_type}

Technical Findings:
{statistical_details}

Task:
Translate each finding into plain English:
- What it means for the business
- Why it matters
- What actions to consider

Rules:
- No jargon (no "z-score", "IQR", "correlation coefficient")
- Use analogies when helpful
- Include confidence level in everyday language ("highly confident", "worth investigating")
- Explain severity in business impact terms
```

**3. Risk Communication Template**
```
Role: You are a data quality specialist explaining risks to project managers.

Context:
- Dataset: {dataset_name}
- Issues detected: {issue_count}

Technical Analysis:
{leakage_detection_results}
{missing_data_patterns}
{outlier_analysis}

Task:
For each issue, explain:
1. What the problem is (in simple terms)
2. Why it could cause problems (business consequences)
3. How urgent it is (action required vs. monitor)
4. How to fix it (step-by-step for non-coders)

Tone: Helpful, non-alarmist, action-oriented
Focus: Business risk, not statistical theory
```

### Best Practices from 2026 Research

Based on verified 2026 prompt engineering research:

1. **Zero-shot over few-shot**: Modern LLMs (Claude Opus 4.5) understand tasks from description alone; examples can bias toward irrelevant patterns

2. **Role clarity**: State role at prompt start; "You are a..." establishes perspective and tone

3. **Step-by-step reasoning**: For complex statistical interpretations (e.g., "correlation 0.92 suggests leakage"), request chain-of-thought analysis

4. **Structured output**: Specify sections explicitly (Key Findings, Business Impact, Recommendations) for consistent formatting

5. **Context injection**: Include PROJECT.md excerpts so insights align with project goals

6. **Iterative refinement**: Test templates on sample datasets, refine based on readability feedback

**Sources:**
- [Prompt Engineering Techniques: Top 6 for 2026](https://www.k2view.com/blog/prompt-engineering-techniques/)
- [The only Prompt Engineering guide you'll need for 2026](https://medium.com/@karl.foster/the-only-prompt-engineering-guide-youll-need-for-2026-7ebfb8857fc8)
- [Mastering Prompts for Data Analysis with LLMs](https://promptwritersai.com/mastering-prompts-for-data-analysis-with-llms/)

---

## Alternatives Considered

### Why Not LIDA?

**What it is:** Microsoft's automatic visualization generation tool using LLMs
**Current version:** Latest release requires Python >=3.10
**Features:**
- Data summarization to natural language
- Automated visualization goal generation
- Grammar-agnostic viz code generation (matplotlib, seaborn, altair)
- Self-evaluation and repair

**Why not for GRD:**
1. **Visualization-first**: LIDA generates charts, not business insights. GRD needs narrative explanations.
2. **Code generation**: LIDA outputs Python code for visualizations. GRD needs plain English summaries.
3. **Wrong abstraction**: LIDA is for creating new visualizations interactively. GRD analyzes existing statistics.
4. **Heavy installation**: Requires `llmx` and `openai` packages; duplicates GRD's MCP integration.
5. **Infographic focus**: Beta feature generates stylized graphics, not terminal-friendly reports.

**When to reconsider:** If GRD adds interactive visualization mode in v2.0+, LIDA could power chart generation.

**Sources:**
- [LIDA: Automatic Visualizations with LLMs](https://microsoft.github.io/lida/)
- [GitHub: microsoft/lida](https://github.com/microsoft/lida)

---

### Why Not PandasAI?

**What it is:** Natural language query interface for pandas DataFrames
**Current version:** 3.0.0 (Jan 2026), Python >=3.8, <=3.11
**Features:**
- Conversational data analysis (ask questions in plain English)
- LLM-powered code generation for pandas operations
- Data visualization and feature generation

**Why not for GRD:**
1. **Query-based paradigm**: PandasAI answers specific questions ("What's the average?"). GRD needs comprehensive summaries.
2. **External API calls**: Uses OpenAI API separately from GRD's MCP integration; adds API key management complexity.
3. **Code generation focus**: Generates pandas code, not business insights. Wrong layer of abstraction.
4. **Interactive workflow**: Designed for iterative questioning, not report generation.
5. **Version constraint**: Python <=3.11 blocks future Python upgrades.

**When to reconsider:** If GRD adds conversational mode for interactive data exploration, PandasAI could enable "ask me anything" about datasets.

**Sources:**
- [PandasAI Technology Analysis](https://www.oreateai.com/blog/pandasai-technology-analysis-a-natural-language-data-analysis-framework/2340a374b1aecba9216790e2df0af6eb)
- [PandasAI PyPI](https://pypi.org/project/pandasai/)

---

### Why Not Automated EDA Libraries?

**Evaluated libraries:**
- ydata-profiling: Comprehensive but slow (10x slower than DataPrep)
- Sweetviz: Dataset comparison focus, NumPy 2.0 issues, stale (2023)
- D-Tale: Interactive GUI, Flask/React overhead, browser-based
- DataPrep: Fast (Dask-based) but stale (2022), Python <3.11 constraint

**Fundamental mismatch:**
All automated EDA libraries solve **initial exploration** (unknown dataset → comprehensive profile). GRD already does this via the Explorer agent.

v1.1 goal: **Insight translation** (technical profile → business-friendly narrative). This is a presentation/communication problem, not an analysis problem.

**Key research finding:**
> "Automated reports are powerful, but they're not a silver bullet... Manual EDA is essential for feature engineering, domain context, and hypothesis testing. Human judgment is still needed to evaluate the outcomes of the exploration and to adopt any strategies that arise from it." ([The Lazy Data Scientist's Guide](https://www.kdnuggets.com/the-lazy-data-scientists-guide-to-exploratory-data-analysis))

**Why this matters:** GRD provides the "human judgment" layer via the Architect and Researcher agents. Automated EDA would create redundancy, not value.

**Sources:**
- [4 Ways to Automate EDA in Python](https://builtin.com/data-science/EDA-python)
- [Top Automated EDA Python Packages](https://www.nb-data.com/p/python-packages-for-automated-eda)
- [Comparing Five Most Popular EDA Tools](https://towardsdatascience.com/comparing-five-most-popular-eda-tools-dccdef05aa4c/)

---

## Installation

### Minimal (Recommended for v1.1)

```bash
# No new dependencies required
# Uses existing Claude Code MCP integration
```

### With Quick-Explore Utilities (Optional)

```bash
pip install skimpy>=0.0.20 great-tables>=0.20.0
```

### Python Version Requirements

| Component | Min Python | Max Python | Notes |
|-----------|-----------|-----------|-------|
| GRD existing stack | 3.9+ | 3.13 | Verified with ydata-profiling, pandas |
| Claude MCP | 3.9+ | 3.13 | Existing integration |
| skimpy (optional) | 3.10+ | 3.13 | Recent release (Jan 2026) |
| great-tables (optional) | 3.9+ | 3.13 | Broad compatibility |

**Recommendation:** Target Python 3.10+ for v1.1 (enables skimpy without breaking existing compatibility).

---

## What NOT to Add

### 1. Browser-Based UIs (D-Tale, Sweetviz)

**Why not:**
- Breaks terminal-based research flow
- Flask/React dependencies add installation friction
- HTML reports don't fit CLI-native tools
- Requires port management for local servers

**When appropriate:** Never for GRD's core workflow. Consider for separate web dashboard if v2.0+ adds web UI.

---

### 2. Heavy Profiling Libraries (ydata-profiling)

**Why not:**
- 10x slower than alternatives on large datasets
- Generates comprehensive HTML reports (Explorer agent already provides this in DATA_REPORT.md)
- Heavy dependencies conflict with lightweight philosophy
- Memory-intensive on datasets >100k rows

**When appropriate:** If users specifically request HTML reports, offer as optional export format, not core workflow.

---

### 3. Duplicate LLM Integrations (PandasAI, LIDA)

**Why not:**
- GRD already integrates Claude via MCP
- Multiple LLM API keys create configuration complexity
- Different LLM providers (OpenAI vs. Anthropic) fragment user experience
- Code generation paradigm conflicts with GRD's agentic workflow

**When appropriate:** If users need specific features (LIDA's visualization, PandasAI's queries), offer as plugins, not core dependencies.

---

### 4. Visualization Code Generation (LIDA, matplotlib automation)

**Why not:**
- GRD focuses on insights, not charts
- Generated code requires review/debugging (adds cognitive load)
- Terminal-based tools render poorly in CLI
- Business analysts want findings, not code

**When appropriate:** If v2.0+ adds notebook integration, LIDA could generate visualizations for Jupyter cells.

---

### 5. Dask/Spark for "Performance" (DataPrep)

**Why not:**
- GRD already uses pandas sampling (100k rows) for efficiency
- Dask adds dependency complexity for marginal benefit
- Explorer agent profiling is fast enough (<10s on 100k rows)
- Distributed computing overkill for single-machine research workflows

**When appropriate:** If GRD targets big data use cases (>10M rows), revisit distributed computing. Not needed for v1.1.

---

## Success Criteria

### Lightweight Integration
- [ ] Zero new required dependencies (uses existing MCP)
- [ ] Optional dependencies <2 packages (skimpy, great-tables)
- [ ] No browser-based tools in core workflow
- [ ] Installation time <10 seconds

### Accessible Output
- [ ] Plain English insights (no jargon)
- [ ] Terminal-native formatting (no HTML pop-ups)
- [ ] Severity indicators in business terms ("Critical: affects model accuracy" not "Z-score >3")
- [ ] Action items with rationale ("Remove feature X because it correlates 0.95 with target, suggesting data leakage")

### Integration Quality
- [ ] Reads existing DATA_REPORT.md structure
- [ ] Preserves technical details for ML researchers (collapsible sections)
- [ ] Generates summaries in <5 seconds (LLM API call)
- [ ] Handles missing sections gracefully (partial reports)

### Maintainability
- [ ] Prompt templates version-controlled
- [ ] No external LLM API key management
- [ ] Clear separation from Explorer agent (insight layer, not analysis layer)
- [ ] Testable with sample DATA_REPORT.md files

---

## Confidence Assessment

| Area | Confidence | Rationale |
|------|-----------|-----------|
| LLM prompting approach | HIGH | Verified via 2026 prompt engineering research; GRD already uses MCP |
| Excluding automated EDA | HIGH | Research confirms "not a silver bullet"; GRD already does manual EDA |
| skimpy/great-tables | MEDIUM | Recent releases, active maintenance, but limited production use data |
| Python version targets | HIGH | Verified via PyPI official pages dated 2025-2026 |
| Template effectiveness | MEDIUM | Requires empirical testing with real datasets; best practices established |

---

## Sources

### LLM & Prompt Engineering (2026)
- [Prompt Engineering Techniques: Top 6 for 2026](https://www.k2view.com/blog/prompt-engineering-techniques/)
- [The only Prompt Engineering guide you'll need for 2026](https://medium.com/@karl.foster/the-only-prompt-engineering-guide-youll-need-for-2026-7ebfb8857fc8)
- [Mastering Prompts for Data Analysis with LLMs](https://promptwritersai.com/mastering-prompts-for-data-analysis-with-llms/)
- [Best practices for LLM prompt engineering - Palantir](https://www.palantir.com/docs/foundry/aip/best-practices-prompt-engineering)

### Automated EDA Landscape (2025-2026)
- [10 Lesser-Known Python Libraries Every Data Scientist Should Be Using in 2026](https://www.kdnuggets.com/10-lesser-known-python-libraries-every-data-scientist-should-be-using-in-2026)
- [Top 50 Python Libraries to Know in 2026](https://www.analyticsvidhya.com/blog/2024/12/python-libraries/)
- [Top 10 Python Libraries for Automated Data Analysis – Kanaries](https://docs.kanaries.net/articles/python-auto-eda)
- [4 Ways to Automate EDA in Python](https://builtin.com/data-science/EDA-python)

### Specific Libraries (Verified 2025-2026)
- [LIDA: Automatic Visualizations with LLMs](https://microsoft.github.io/lida/)
- [PandasAI Technology Analysis](https://www.oreateai.com/blog/pandasai-technology-analysis-a-natural-language-data-analysis-framework/2340a374b1aecba9216790e2df0af6eb)
- [Comparing Five Most Popular EDA Tools](https://towardsdatascience.com/comparing-five-most-popular-eda-tools-dccdef05aa4c/)
- [ydata-profiling v4.18.1 (Jan 13, 2026)](https://pypi.org/project/ydata-profiling/)
- [Sweetviz v2.3.1 (Nov 29, 2023)](https://pypi.org/project/sweetviz/)
- [D-Tale v3.19.1 (Jan 28, 2026)](https://pypi.org/project/dtale/)
- [DataPrep v0.4.5 (Aug 4, 2022)](https://pypi.org/project/dataprep/)
- [skimpy v0.0.20 (Jan 3, 2026)](https://pypi.org/project/skimpy/)
- [great-tables v0.20.0 (Oct 31, 2025)](https://pypi.org/project/great-tables/)

### Critical Perspectives
- [The Lazy Data Scientist's Guide to Exploratory Data Analysis](https://www.kdnuggets.com/the-lazy-data-scientists-guide-to-exploratory-data-analysis)
- [Top Automated EDA Python Packages for Efficient Data Analysis](https://www.nb-data.com/p/python-packages-for-automated-eda)

---

**Last updated:** 2026-01-30
**Next review:** After v1.1 implementation, validate template effectiveness with real datasets
