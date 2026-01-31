# Project Research Summary

**Project:** GRD v1.1 - Research UX Refinement
**Domain:** ML research workflow tooling with accessible EDA
**Researched:** 2026-01-30
**Confidence:** HIGH

## Executive Summary

GRD v1.1 refines the research experience by cleaning up legacy GSD commands and adding accessible EDA capabilities for business stakeholders. The research reveals a clear architectural path: keep the existing Explorer agent and add mode variants (quick-explore for speed, insights for plain English) rather than creating new agents or dependencies. The technical foundation is solid—leverage existing Claude MCP integration with structured prompt templates for insight translation—avoiding heavy automated EDA libraries that add friction without value.

The critical insight is that accessible EDA is fundamentally a **presentation layer problem**, not an analysis problem. GRD already performs rigorous EDA via the Explorer agent; v1.1 translates those findings into business-friendly language. This approach maintains GRD's lightweight philosophy (zero new required dependencies) while expanding the audience from ML researchers to business analysts and product managers.

The primary risk is statistical misinterpretation—research documents that 60%+ of professionals misunderstand p-values and correlation vs. causation. Prevention requires explicit language guardrails: never use causal language for correlations, always report effect sizes alongside significance, and implement multiple comparison correction to filter spurious patterns. A second risk is integration breaking existing research workflows; the solution is mode-based isolation where quick/insights commands serve different personas without disrupting the core research loop.

## Key Findings

### Recommended Stack

**Zero new required dependencies.** The v1.1 feature set uses existing Claude Code MCP integration with custom prompt templates for insight generation. This aligns with GRD's lightweight philosophy and avoids the pitfalls of automated EDA libraries (heavy dependencies, HTML output, slow performance, workflow mismatch).

**Core technologies:**
- **Claude API (via MCP)**: Transform statistical analysis into plain English insights using structured prompts (role-based, step-by-step reasoning, business context injection)
- **Structured prompt templates**: Convert DATA_REPORT.md sections to accessible summaries with three audiences (executive, business analyst, risk communication)
- **Existing Explorer agent**: Reuse proven analysis pipeline (pandas, scipy, numpy) with mode parameter support for quick/insights variants

**Optional utilities (not critical path):**
- **skimpy** (0.0.20, Jan 2026): Console-based data summaries for quick-explore terminal output
- **great-tables** (0.20.0, Oct 2025): Publication-quality tables if formal reports needed

**Explicitly excluded:**
- Automated EDA libraries (ydata-profiling, Sweetviz, D-Tale, DataPrep): Installation friction, HTML output doesn't fit terminal workflows, redundant with existing Explorer
- Duplicate LLM integrations (PandasAI, LIDA): Wrong abstraction (query/visualization vs. narrative insights), API key complexity
- Visualization code generation: GRD focuses on insights, not charts; business analysts want findings, not code to debug

### Expected Features

**Must have (table stakes for business analysts):**
- Plain English summaries (no jargon: "average" not "mean", "typical spread" not "standard deviation")
- Automatic data quality checks (missing values, duplicates, outliers flagged proactively)
- Key insights highlighted (top 3-5 findings prioritized, prevent data paralysis)
- Fast results (quick-explore <60 seconds, insights 5-15 minutes same as full EDA)
- No code required (natural language or command-based, not SQL/Python barriers)
- Clean output format (Markdown for copy-paste to slides/emails)

**Should have (differentiators vs. generic BI tools):**
- Technical foundation underneath (insights grounded in rigorous Explorer EDA, not surface-level BI)
- Graduated detail levels (quick summary + option to drill into full technical analysis)
- Data leakage warnings (prevent "99% accuracy using customer_canceled feature" mistakes)
- Narrative structure (insights flow as story: data quality → patterns → recommendations)
- Confidence indicators (signal uncertainty: "high confidence: revenue trend" vs. "low confidence: seasonality")
- CLI integration (fits ML researcher workflow; business analysts can ask, researchers get technical depth)

**Defer (v2+):**
- Natural language queries (v1.1 focuses on output accessibility, not input; NLQ has accuracy/complexity issues)
- Business impact estimation (requires domain context like revenue data, user counts)
- Comparison baselines (needs historical data tracking infrastructure)
- Interactive visualizations (text-first portability; defer charts to Matplotlib integration)

### Architecture Approach

The v1.1 architecture adds accessible EDA as **mode variants of the existing Explorer agent**, not new agent types. This preserves proven patterns while layering accessibility. Commands (`/grd:quick-explore`, `/grd:insights`) are thin orchestration that spawn `grd-explorer` with mode flags (`--mode=quick|insights`, `--depth=summary|full`, `--output-style=technical|business`). The Explorer detects mode and adjusts behavior: quick mode skips outlier/leakage detection for speed, insights mode runs full analysis but transforms output with business language templates.

**Major components:**
1. **Command cleanup layer** — Remove 2 GSD-specific commands (audit-milestone, plan-milestone-gaps) that don't fit research workflows; delete 32 duplicate " 2.md" files
2. **Command orchestration** — Add quick-explore.md and insights.md as thin spawners that validate input and pass mode context to Explorer
3. **Explorer mode detection** — Modify grd-explorer.md Step 0 to parse mode flags and conditionally execute analysis steps
4. **Insight generation module** — LLM-powered translation using structured prompt templates (executive summary, accessible insights, risk communication)
5. **Output formatting layer** — Transform technical DATA_REPORT.md sections into plain English with "What This Means" explanations

**Critical architecture decisions:**
- **Single artifact type**: All three explore variants write to `.planning/DATA_REPORT.md` with mode headers; no QUICK_REPORT.md or INSIGHTS_REPORT.md to fragment state
- **Immutable modes**: Quick is fast (no leakage checks), insights is business-friendly (full analysis, plain language); no mode drift via user overrides
- **Gating preserved**: Architect soft gate checks DATA_REPORT.md presence and warns if only quick mode completed; full/insights both count as complete EDA
- **Critic routing unchanged**: REVISE_DATA always routes to full explore (revision mode), never quick-explore or insights

### Critical Pitfalls

1. **Correlation-Causation Trap** — Automated insights present correlations as actionable without causal verification; 60%+ professionals misinterpret. Prevention: Explicit language gates ("X and Y moved together" never "X causes Y"), three-element causation check (temporal, mechanism, confounding), confidence levels with warnings, require human approval for causal claims.

2. **Statistical Significance Theater** — P-values misunderstood even by professionals (70%+ error rate); "p<0.05" treated as "important" when reality is only measures null hypothesis likelihood. Prevention: Always report effect size + confidence intervals, plain English tiers (tiny/small/medium/large change), context-dependent thresholds ("Change detected (5%) vs. Your threshold (10%): BELOW"), flag contradictory signals.

3. **Integration Breaking Existing Workflows** — Adding business-analyst features conflicts with ML researcher workflows; command confusion, state corruption, Critic doesn't validate plain English. Prevention: Explicit persona modes (research vs. analyst), namespace isolation, state segregation (.grd/research/ vs. .grd/insights/), modular architecture with feature flags, clear command deprecation strategy.

4. **Jargon Creep in Plain English** — "Accessible" outputs gradually accumulate statistical terms as developers (data scientists) don't recognize jargon. Prevention: Mandatory jargon audit checklist (mean→average, outlier→unusual value), non-technical user testing (3+ business analysts review templates), LLM prompts enforce 8th grade reading level, automated jargon detection in CI.

5. **False Patterns at Scale** — Large datasets mathematically guarantee random correlations; automated systems surface spurious findings. Prevention: Multiple comparison correction (Bonferroni/FDR), domain knowledge filtering (blacklist known spurious pairs), bootstrapping/permutation tests for robustness, insight budget (limit to top 5-10 findings ranked by robustness).

## Implications for Roadmap

Based on research, suggested 4-phase structure prioritizing cleanup before features, simple before complex, integration testing throughout.

### Phase 1: Command Cleanup & Foundation (1-2 hours)

**Rationale:** Clear technical debt before adding features; prevents confusion and establishes clean baseline for v1.1 additions.

**Delivers:**
- Remove 32 duplicate " 2.md" files from `.claude/commands/grd/`
- Delete 2 GSD-specific commands (audit-milestone, plan-milestone-gaps)
- Update help.md to remove references and add placeholders for new commands
- Verification: 30 unique command files remain (32 - 2 removed, before adding 2 new)

**Addresses:** Reduces command count from 64 files (32 + duplicates) to 30 clean files, removing software-centric "requirements coverage" commands that don't fit hypothesis-driven research workflows.

**Avoids:** Pitfall 3 (Integration breaking workflows) by establishing clear command landscape before new additions; prevents confusion between legacy and new features.

**Research flags:** No additional research needed; file deletion is straightforward.

### Phase 2: Quick Explore (3-4 hours)

**Rationale:** Simpler of two new commands (no output transformation); provides fast feedback loop for data familiarization decisions.

**Delivers:**
- Modify `agents/grd-explorer.md` to add mode detection (Step 0) and conditional skipping (Steps 4, 6, 8 for distributions, outliers, leakage)
- Create `.claude/commands/grd/quick-explore.md` as thin orchestration layer
- Quick mode completes in <60 seconds vs. 5-15 minutes for full explore
- DATA_REPORT.md with "Quick Explore" header and note about running full explore

**Uses:** Existing Explorer agent (pandas, scipy) with constrained execution; skimpy (optional) for terminal-friendly summaries.

**Addresses:** Feature table stake "Fast results" and differentiator "Graduated detail levels" (quick overview before deciding on full analysis).

**Avoids:** Pitfall 2 (Statistical significance theater) by skipping complex tests in quick mode; prevents premature conclusions from insufficient analysis. Pitfall 3 (Integration breaking) via clear mode headers that gate downstream commands.

**Research flags:** Standard patterns; no additional research needed. Integration point with Architect soft gate requires testing.

### Phase 3: Accessible Insights (4-6 hours)

**Rationale:** More complex than quick-explore (output transformation required); enables stakeholder communication without separate manual translation.

**Delivers:**
- Modify `agents/grd-explorer.md` to add insights mode with business language transformation templates
- Executive summary generation (3-4 actionable bullets via LLM call)
- "What This Means" sections for each finding
- Create `.claude/commands/grd/insights.md` as thin orchestration layer
- Plain English output (no "skewness", "MCAR", "heteroscedasticity")

**Uses:** Claude MCP with structured prompts (role-based: data analyst → stakeholder, step-by-step reasoning, context injection from PROJECT.md).

**Addresses:** Feature table stakes "Plain English summaries", "Key insights highlighted", "Actionable recommendations". Differentiator "Narrative structure" (story flow vs. bullet points).

**Avoids:** Pitfall 1 (Correlation-causation) via explicit language guardrails in prompt templates. Pitfall 4 (Jargon creep) via non-technical user testing requirement. Pitfall 6 (Oversimplification) via layered disclosure (summary + expandable technical details).

**Research flags:** Prompt template effectiveness requires empirical testing with sample datasets; may need refinement based on business analyst feedback in Phase 4.

### Phase 4: Integration Testing & Validation (2-3 hours)

**Rationale:** Validate workflow paths, gating behavior, and prevent regressions before release.

**Delivers:**
- Progressive path testing: quick-explore → explore → architect
- Insights path testing: insights → architect (should proceed without warning)
- Quick-only path testing: quick-explore → architect (should warn about insufficient depth)
- Critic routing validation: research → REVISE_DATA → explore (not quick-explore)
- Overwrite behavior: quick-explore → explore (should replace, not append)
- Regression tests: existing explore works unchanged, Critic revision routes correctly, help shows all 32 commands

**Implements:** Confidence assessment verification—does the system correctly identify when quick mode is insufficient? Do warnings appear at correct gates?

**Avoids:** Pitfall 3 (Integration breaking) by testing both personas (ML researcher vs. business analyst) and ensuring isolation. Pitfall 5 (Data literacy resistance) by validating that business analysts can interpret outputs without training.

**Research flags:** User acceptance testing with 3+ business analysts needed to validate jargon-free language and actionable recommendations. May reveal prompt template refinements needed.

### Phase Ordering Rationale

- **Cleanup first (Phase 1):** Technical debt removal establishes clean baseline; prevents confusion between legacy and new commands; low-risk prerequisite for feature work.
- **Quick before Insights (Phases 2-3):** Quick-explore is simpler (conditional execution, no output transformation); validates mode architecture before adding complex language templates; provides fast-feedback feature for immediate user value.
- **Integration last (Phase 4):** Cannot test workflow paths until both new commands exist; regression testing validates nothing broke; user testing with business analysts validates accessibility claims.
- **Avoids pitfall accumulation:** Language guardrails (Pitfall 1, 4) built into Phase 3 prompts before user testing; mode isolation (Pitfall 3) verified in Phase 4 before release; prevents compounding issues.

### Research Flags

**Needs phase-specific research:**
- **Phase 3:** Prompt engineering effectiveness—test templates on sample datasets (Titanic, Boston Housing) to validate plain English translations; may need iteration based on readability scores and business analyst comprehension.
- **Phase 4:** User acceptance testing protocol—design test scenarios for business analysts (3+ participants); measure task completion rate, jargon comprehension, confidence in acting on insights.

**Standard patterns (skip research-phase):**
- **Phase 1:** File deletion and command cleanup—straightforward housekeeping
- **Phase 2:** Mode parameter addition to existing agent—architectural pattern established in research

**Open questions requiring validation:**
- Should quick-explore check for data leakage at all? (Research recommends skip for speed; document trade-off clearly)
- Should insights mode generate visualizations? (Research recommends defer to v1.2; use markdown tables with ASCII art for now)
- What depth control for insights? (Research suggests opinionated defaults over user-configured verbosity)
- Domain-aware templates? (Generic insights vs. specialized for e-commerce/finance/healthcare; defer specialization to v2.0)

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | **HIGH** | Verified via 2026 prompt engineering research and GRD's existing MCP integration; zero new required dependencies aligns with lightweight philosophy |
| Features | **MEDIUM-HIGH** | Business analyst expectations well-documented via 2026 BI tool research; GRD-specific differentiators (CLI integration, technical foundation) are novel but logical |
| Architecture | **HIGH** | Existing codebase analysis confirms Explorer agent reuse is clean; mode parameter pattern is standard; single artifact avoids state fragmentation |
| Pitfalls | **HIGH** | Statistical misinterpretation documented with 60-70% error rates; integration risks backed by software modularity research; jargon creep confirmed via UX studies |

**Overall confidence: HIGH**

The technical approach (mode variants + prompt templates) is sound and validated by existing GRD architecture. The primary uncertainties are **execution details**:
- Exact prompt wording for jargon-free insights (requires empirical testing in Phase 3)
- Business analyst comprehension rates (validated in Phase 4 user testing)
- Integration edge cases with Critic/Architect gates (tested in Phase 4)

These are normal implementation risks, not fundamental approach risks.

### Gaps to Address

**Gap 1: Statistical rigor vs. accessibility tradeoff**
- **Issue:** Research identifies tension between simplification (enables access) and precision (prevents misinterpretation)
- **Mitigation:** Phase 3 implements layered disclosure (simple summary + expandable technical details); Phase 4 user testing validates minimum statistical detail required
- **Validation:** A/B test with business analysts—does simplified version lead to incorrect decisions?

**Gap 2: Critic agent validation of plain English insights**
- **Issue:** Critic is designed to validate code/experiments, not narrative reports; unclear how it evaluates insights mode outputs
- **Mitigation:** Insights mode is presentation-only (same analysis as full explore, different format); Critic validates underlying technical DATA_REPORT.md, not plain English translation
- **Decision:** Critic never routes to insights mode (always full explore for revision); insights is stakeholder communication, not validation target

**Gap 3: Persona mode enforcement**
- **Issue:** Research recommends explicit persona modes (research vs. analyst) but implementation path unclear
- **Mitigation:** v1.1 uses command namespacing (explore/architect/research vs. quick-explore/insights) without formal mode system; defer persona modes to v1.2 if cross-contamination issues arise
- **Validation:** Phase 4 tests both personas independently; monitor for command confusion in first 30 days post-launch

**Gap 4: Prompt template effectiveness**
- **Issue:** Structured prompts are well-researched but context-specific; no guarantee GRD's templates produce jargon-free, actionable insights
- **Mitigation:** Phase 3 includes iterative refinement with sample datasets; Phase 4 requires 3+ business analyst review
- **Success criteria:** Pass rate >80% on "can you explain this finding in your own words without help" test

**Gap 5: Long-term jargon creep prevention**
- **Issue:** Research confirms jargon accumulates over time as developers add features; how to prevent drift?
- **Mitigation:** Establish jargon audit checklist in Phase 2; automated detection in CI (grep for banned terms: "p-value", "standard deviation", "heteroscedasticity"); quarterly business analyst review panel
- **Monitoring:** Track support tickets asking for term definitions as leading indicator

## Sources

### Primary (HIGH confidence)

**Stack research:**
- [Prompt Engineering Techniques: Top 6 for 2026](https://www.k2view.com/blog/prompt-engineering-techniques/) — Role-based prompting, structured output, step-by-step reasoning
- [ydata-profiling v4.18.1 PyPI](https://pypi.org/project/ydata-profiling/) — Version verification, Python compatibility
- [skimpy v0.0.20 PyPI](https://pypi.org/project/skimpy/) — Recent Jan 2026 release, terminal-native output
- [The Lazy Data Scientist's Guide to EDA](https://www.kdnuggets.com/the-lazy-data-scientists-guide-to-exploratory-data-analysis) — "Automated reports not a silver bullet"

**Features research:**
- [Top 11 AI Data Analysis Tools - 2026 Update](https://powerdrill.ai/blog/top-ai-data-analysis-tools-update) — Business analyst tool expectations
- [Self-Service Analytics Evaluation Guide](https://promethium.ai/guides/self-service-analytics-tools-platforms/) — Table stakes features
- [Data Democratization: Empowering Non-Technical Users](https://www.getorchestra.io/guides/data-democratization-empowering-non-technical-users) — Accessibility principles

**Architecture research:**
- Existing GRD codebase analysis — 32 unique commands, 32 duplicates, Explorer agent structure verified

**Pitfalls research:**
- [PMC: 70%+ P-value Misinterpretation Rate](https://pmc.ncbi.nlm.nih.gov/articles/PMC9383044/) — Statistical significance misunderstanding
- [Management Consulted: Correlation vs Causation](https://managementconsulted.com/correlation-vs-causation/) — "Identical mistake made thousands of times daily"
- [Airbyte: Spurious Correlations](https://airbyte.com/data-engineering-resources/spurious-correlations) — Large datasets guarantee random correlations
- [Informatica CDO Report 2026](https://www.informatica.com/about-us/news/news-releases/2026/01/20260127-new-global-cdo-report-reveals-data-governance-and-ai-literacy-as-key-accelerators-in-ai-adoption.html) — 75% employees need data literacy upskilling

### Secondary (MEDIUM confidence)

- [Comparing Five Popular EDA Tools](https://towardsdatascience.com/comparing-five-most-popular-eda-tools-dccdef05aa4c/) — Automated EDA library evaluation
- [Towards Data Science: Simplicity in Data Storytelling](https://towardsdatascience.com/the-real-challenge-in-data-storytelling-getting-buy-in-for-simplicity/) — Accuracy vs. accessibility tradeoff
- [Cleanlab: Spurious Correlations Detection](https://cleanlab.ai/blog/spurious-correlations/) — Automated detection tools
- [Number Analytics: Unmasking Spurious Correlations](https://www.numberanalytics.com/blog/unmasking-spurious-correlations-statistical-illusions) — Bootstrapping/permutation tests

### Tertiary (requires validation)

- Prompt template effectiveness for GRD's specific use case — needs empirical testing in Phase 3
- Business analyst comprehension rates for simplified outputs — validated in Phase 4 user testing
- Long-term jargon creep rates — monitor post-launch with support ticket analysis

---

**Research completed:** 2026-01-30
**Ready for roadmap:** Yes
**Next step:** Create detailed ROADMAP.md using these phase suggestions and research flags
