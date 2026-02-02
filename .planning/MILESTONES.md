# Project Milestones: Get Research Done (GRD)

## v1.3 Branding & Gemini Integration (Shipped: 2026-02-02)

**Delivered:** Gemini CLI support with multi-runtime installer, visual branding transformation to GRD identity with research teal colors, and complete documentation refresh

**Phases completed:** 20-23 (4 plans total)

**Key accomplishments:**
- Cherry-picked 10 upstream GSD commits including full Gemini CLI support (--gemini flag, TOML conversion, agent loading)
- Transformed visual identity with GRD logo ASCII art and research teal color palette (#4FB3D4)
- Multi-runtime installer supporting Claude Code, OpenCode, and Gemini CLI
- Universal improvements: context bar scaling, ASCII box-drawing fix, squash merge strategy, unified branching
- Complete documentation: What's New section, Gemini CLI setup guide, CHANGELOG.md full version history

**Stats:**
- 49 files created/modified
- +5,874 net lines of code (Markdown, JavaScript, SVG)
- 4 phases, 4 plans, ~12 tasks
- 1 day from v1.2 to v1.3

**Git range:** `docs(20): capture phase context` → `docs(23): complete Documentation & Finalization phase`

**What's next:** v2.0 Advanced Features (MLflow integration, DVC integration, multi-user support, web UI)

---

## v1.2 Command Unification (Shipped: 2026-02-02)

**Delivered:** Research-native CLI with experiment-based terminology, correct command chaining, and clean product positioning

**Phases completed:** 15-19 (12 plans total)

**Key accomplishments:**
- Renamed 9 commands to research terminology — design-experiment, run-experiment, scope-experiment, validate-results, literature-review, list-experiment-assumptions, add-experiment, insert-experiment, remove-experiment
- Fixed command chaining — new-study→design-experiment→run-experiment→validate-results→complete-study workflow
- Updated templates (STATE.md, ROADMAP.md) to use experiment/study terminology
- Reset external documentation — CHANGELOG.md presents GRD as fresh v1.2.0 product with GSD acknowledgment
- Added integration tests — 23 automated tests validate all command renames and chains
- Documented validation exceptions for intentional stale references

**Stats:**
- 83 files created/modified
- +3,452 net lines of code (Markdown, JavaScript)
- 5 phases, 12 plans, ~25 tasks
- 2 days from v1.1 to v1.2

**Git range:** `feat(15-01)` → `revert(19-01)`

**What's next:** v2.0 Advanced Features (MLflow integration, DVC integration, multi-user support, web UI)

---

## v1.1 Research UX Refinement (Shipped: 2026-02-01)

**Delivered:** Streamlined research workflows with study-centric terminology, fast EDA via quick-explore, and plain English insights for business analysts

**Phases completed:** 10-14 (13 plans total)

**Key accomplishments:**
- Command cleanup and study-centric terminology — renamed 6 lifecycle commands (new-study, scope-study, plan-study, run-study, validate-study, complete-study)
- Quick Explore command (`/grd:quick-explore`) — fast EDA with Rich console output, sparklines, and quality indicators
- Accessible Insights command (`/grd:insights`) — plain English data insights with "What This Means" explanations and LLM prompts
- Architect warning system — detects Quick Explore Mode and warns about insufficient data depth
- Integration testing validation — 118/118 automated checks passed, all behavioral workflows verified

**Stats:**
- 76 files created/modified
- +16,503 lines of code (Markdown, Python, TypeScript)
- 5 phases, 13 plans, ~40 tasks
- 3 days from v1.0 to v1.1

**Git range:** `feat(10-01)` → `docs(14)`

**What's next:** v2.0 Advanced Features (MLflow integration, DVC integration, multi-user support, web UI)

---

## v1.0 MVP (Shipped: 2026-01-30)

**Delivered:** Recursive ML experimentation framework with data-first workflows, automated validation loops, and human decision gates

**Phases completed:** 1-9 (39 plans total)

**Key accomplishments:**
- GRD branding and CLI with 27 commands, new ASCII art, and npm package (get-research-done 2.0.0)
- Data-first Explorer agent with statistical profiling, leakage detection, and reproducible DATA_REPORT.md
- Architect agent generating testable hypotheses in OBJECTIVE.md with falsification criteria and baseline requirements
- Recursive validation loop (Researcher/Critic/Evaluator) with PROCEED/REVISE_METHOD/REVISE_DATA routing
- Human evaluation gate with evidence packages, decision logging (Seal/Iterate/Archive), and negative result archival
- Jupyter notebook support with papermill execution, graduation path to validated scripts, and evaluation parity

**Stats:**
- 288 files created/modified
- 48,494 lines of code (Markdown, TypeScript, Python)
- 9 phases, 39 plans, ~115 tasks
- 47 days from project start to ship

**Git range:** `Initial commit` → `feat(09-04)`

**What's next:** v2.0 Advanced Features (multi-user support, web UI, red-teaming mode, automatic data profiling)

---
