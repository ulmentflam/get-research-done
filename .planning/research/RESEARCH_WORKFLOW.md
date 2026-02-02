# ML Research Workflow Mental Models

**Researched:** 2026-02-01
**Domain:** ML/academic research workflow terminology and mental models
**Confidence:** HIGH (multi-source verification)

## Executive Summary

ML researchers think about their work differently than software engineers. They follow a scientific lifecycle rooted in hypothesis generation, experimentation, and analysis rather than a product-centric build/deploy cycle. Understanding this mental model is essential for GRD to resonate with researchers rather than feel like a foreign software engineering imposition.

The research lifecycle moves through distinct phases: **problem formulation** -> **hypothesis generation** -> **experimental design** -> **data collection** -> **analysis** -> **iteration** -> **dissemination**. Researchers think in terms of "studies" (comprehensive investigations) and "experiments" (individual hypothesis tests), with experiments being building blocks within studies.

GRD's current terminology maps reasonably well to research mental models but could be optimized. "Phases" feel natural (research has phases), but "plans" and "tasks" feel more engineering-focused. The key insight: researchers think about **questions to answer** and **evidence to gather**, not "features to build."

---

## Standard Research Lifecycle Terminology

### Academic Research Lifecycle (General)

The standard academic research lifecycle includes these phases:

| Phase | Description | Activities |
|-------|-------------|------------|
| **Problem Formulation** | Identify research gap, define scope | Literature review, gap analysis, research question development |
| **Hypothesis Generation** | Form testable predictions | Theory development, variable identification, prediction formulation |
| **Study Design** | Plan how to test hypotheses | Method selection, data requirements, success criteria |
| **Data Collection** | Gather evidence | Run experiments, collect observations, build datasets |
| **Analysis** | Extract meaning from data | Statistical analysis, pattern identification, result interpretation |
| **Iteration** | Refine based on findings | Hypothesis refinement, additional experiments, methodology adjustment |
| **Dissemination** | Share findings | Publication, presentation, reproducibility artifacts |

**Sources:**
- [Harvard Research Lifecycle](https://researchsupport.harvard.edu/research-lifecycle)
- [NNLM Research Lifecycle](https://www.nnlm.gov/guides/data-glossary/research-lifecycle)
- [APH Quality Handbook](https://aph-qualityhandbook.org/research-lifecycle/)

### ML-Specific Research Lifecycle (CRISP-DM/CRISP-ML)

ML research follows an adaptation of the scientific method:

| Phase | CRISP-DM Term | ML Activities |
|-------|---------------|---------------|
| **1. Business/Problem Understanding** | Business Understanding | Define what problem we're solving, success criteria |
| **2. Data Understanding** | Data Understanding | EDA, data profiling, quality assessment |
| **3. Data Preparation** | Data Preparation | Cleaning, feature engineering, splitting |
| **4. Modeling** | Modeling | Architecture selection, training, hyperparameter tuning |
| **5. Evaluation** | Evaluation | Metrics, ablation studies, baseline comparisons |
| **6. Deployment** | Deployment | Production, monitoring, maintenance |

**Key insight:** CRISP-DM is iterative and cyclic. Researchers move back and forth between phases. This matches GRD's philosophy of "plans can lead to re-planning."

**Sources:**
- [CRISP-DM for Data Science 2025](https://www.datascience-pm.com/wp-content/uploads/2024/12/CRISP-DM-for-Data-Science-2025.pdf)
- [Udacity CRISP-DM Explained](https://www.udacity.com/blog/2025/03/crisp-dm-explained-a-proven-data-mining-methodology.html)

---

## Key Terminology: Researcher vs. Software Engineer

### Core Concepts

| Researcher Term | Software Engineer Term | GRD Current | Notes |
|-----------------|----------------------|-------------|-------|
| **Study** | Project | Project | Good alignment |
| **Experiment** | Feature / Sprint | Phase / Plan | Experiment = smaller unit of work testing one hypothesis |
| **Hypothesis** | Requirement | Requirement | Hypothesis is testable; requirement may not be |
| **Research Question** | User Story | (none) | Open-ended inquiry guiding the study |
| **Variables** | Features (ML inputs) / Parameters | (none) | Statistical terminology vs. ML terminology |
| **Ablation Study** | (no equivalent) | (none) | Systematic removal of components to measure contribution |
| **Baseline** | MVP / Current State | (none) | Reference point for comparison |
| **Pilot Study** | Proof of Concept / Spike | Discovery? | Feasibility test before full study |
| **Replication** | (testing?) | Verification | Reproducibility is central to research |

### What Researchers Say vs. What Engineers Say

| Researcher Says | Engineer Says | Meaning |
|-----------------|---------------|---------|
| "Run an experiment" | "Implement a feature" | Make a change and measure the outcome |
| "Test a hypothesis" | "Validate requirements" | Check if our assumption is correct |
| "Establish a baseline" | "Build MVP" | Create reference point for comparison |
| "Conduct ablation" | "Remove feature and test" | Systematically measure component value |
| "Analyze results" | "Review metrics" | Interpret outcome data |
| "Iterate on findings" | "Refactor based on feedback" | Improve based on new information |
| "Replicate the study" | "Ensure reproducibility" | Someone else can get same results |
| "Disseminate findings" | "Ship / Deploy" | Share work with others |

**Sources:**
- [Machine Learning Mastery - Controlled Experiments](https://machinelearningmastery.com/controlled-experiments-in-machine-learning/)
- [Google ML - Experiments](https://developers.google.com/machine-learning/managing-ml-projects/experiments)

---

## Experiment vs. Study: The Key Distinction

### Study (Higher Level)

A **study** is a comprehensive investigation designed to answer one or more research questions. Studies:
- Have a defined scope and methodology
- May include multiple experiments
- Produce findings that contribute to knowledge
- Are documented for reproducibility
- Have clear success criteria

**Example:** "A study on transformer architectures for low-resource language translation"

### Experiment (Lower Level)

An **experiment** is a controlled test of a specific hypothesis within a study. Experiments:
- Test a single hypothesis or small set of related hypotheses
- Have controlled variables (independent, dependent, controlled)
- Produce measurable results
- Are building blocks of studies
- Are reproducible with documented methodology

**Example:** "Experiment 3: Testing whether layer normalization placement affects BLEU scores"

### GRD Mapping

| Research Concept | GRD Concept | Alignment Quality |
|------------------|-------------|-------------------|
| Study | Milestone | Good - both represent significant body of work |
| Experiment | Phase | Moderate - phases are larger than typical experiments |
| Experimental Trial | Plan | Good - individual execution unit |
| Hypothesis | Success Criteria | Partial - hypotheses are predictions, not just criteria |
| Research Question | Phase Goal | Partial - questions are open-ended, goals are specific |

**Sources:**
- [Oregon State - Research Methods in ML](https://web.engr.oregonstate.edu/~tgd/talks/new-in-ml-2019.pdf)
- [ICML 2002 - Crafting Papers on ML](https://icml.cc/Conferences/2002/craft.html)

---

## The Hypothesis-Driven Development Model

ML researchers use hypothesis-driven development more than feature-driven development.

### The Cycle

```
1. Form Hypothesis
   "If we use attention, translation quality will improve"
        |
        v
2. Design Experiment
   Define variables, metrics, baseline, methodology
        |
        v
3. Execute Experiment
   Run training, collect results
        |
        v
4. Analyze Results
   Compare to baseline, statistical significance
        |
        v
5. Draw Conclusions
   Accept/reject hypothesis, identify next hypothesis
        |
        v
6. Iterate or Publish
   New hypothesis or write up findings
```

### Experiment Tracking Mental Model

Researchers think about:

| Element | What It Means | GRD Equivalent |
|---------|---------------|----------------|
| **Hypothesis** | Prediction to test | (implicit in task action?) |
| **Independent Variable** | What we change | (code changes in task) |
| **Dependent Variable** | What we measure | Verification criteria |
| **Controls** | What we hold constant | Constraints |
| **Baseline** | Reference for comparison | "Before" state |
| **Metrics** | How we measure success | Success criteria |
| **Artifacts** | What we save | Git commits, SUMMARY.md |

**Key insight:** Researchers are explicit about hypotheses. GRD implicitly embeds hypotheses in task descriptions. Making hypotheses explicit might resonate with researcher workflow.

**Sources:**
- [Neptune AI - ML Experiment Tracking](https://neptune.ai/blog/ml-experiment-tracking)
- [Trail ML - Experiment Tracking](https://www.trail-ml.com/blog/first-steps-experiment-tracking)
- [Weights & Biases - Intro to Experiment Tracking](https://wandb.ai/site/articles/intro-to-mlops-machine-learning-experiment-tracking/)

---

## How Researchers Talk About "Phases" of Work

Researchers do think in phases, but they use different names:

### Phase Terminology in Research

| Phase Type | Description | GRD Equivalent |
|------------|-------------|----------------|
| **Exploratory Phase** | Understand the problem, survey landscape | Research Phase |
| **Pilot Phase** | Test feasibility on small scale | Discovery |
| **Main Study** | Full execution of methodology | Execution Phase |
| **Analysis Phase** | Interpret results | Verification |
| **Iteration Phase** | Refine based on findings | Next Phase |

### Paper Structure as Phase Model

ML research papers implicitly reveal the phase structure researchers follow:

1. **Introduction** (Problem understanding)
2. **Related Work** (Ecosystem research)
3. **Methodology** (Design/planning)
4. **Experiments** (Execution)
5. **Results** (Analysis)
6. **Discussion** (Interpretation and future work)
7. **Conclusion** (Summary)

This maps loosely to:
- Introduction/Related Work = GRD Research
- Methodology = GRD Planning
- Experiments = GRD Execution
- Results/Discussion = GRD Verification

**Sources:**
- [Writing ML Research Papers](https://grigorisg9gr.github.io/machine%20learning/research%20paper/how-to-write-a-research-paper-in-machine-learning/)
- [UT Austin ML Paper Template](https://www.cs.utexas.edu/~mooney/cs391L/paper-template.html)

---

## Reproducibility: Central to Research Culture

Reproducibility is foundational to research culture in a way that "testing" is to engineering.

### Reproducibility Checklist (from ML Research)

Researchers expect to track:
- Code (exact version)
- Environment (dependencies, versions)
- Data (datasets, splits, preprocessing)
- Hyperparameters (all configuration)
- Random seeds (for stochastic processes)
- Hardware (GPU, memory, etc.)
- Results (metrics, artifacts)

### GRD Alignment

GRD's emphasis on:
- Git commits for each task (code tracking)
- SUMMARY.md with outcomes (result tracking)
- PLAN.md with specifications (methodology tracking)

**Gap:** GRD doesn't explicitly track environment, random seeds, or hyperparameters. This is more relevant for ML-specific research.

**Sources:**
- [Reproducibility in ML-based Research](https://arxiv.org/html/2406.14325v1)
- [Neptune AI - How to Solve Reproducibility in ML](https://neptune.ai/blog/how-to-solve-reproducibility-in-ml)

---

## GRD Terminology Mapping Recommendations

### Terms That Feel Natural to Researchers

| GRD Term | Researcher Comfort | Why |
|----------|-------------------|-----|
| **Project** | High | Universal term |
| **Milestone** | High | Clear, familiar concept |
| **Phase** | High | Researchers think in phases |
| **Research** | High | Core activity |
| **Discovery** | Medium | "Pilot study" or "exploratory analysis" might be more natural |
| **Verification** | Medium | "Evaluation" or "validation" more common |

### Terms That May Feel Forced

| GRD Term | Researcher Comfort | Alternative |
|----------|-------------------|-------------|
| **Plan** | Low | "Protocol" or "Methodology" |
| **Task** | Low | "Step" or "Procedure" |
| **Roadmap** | Low | "Research Agenda" or "Study Plan" |
| **Execute** | Low | "Conduct" or "Run" |

### Suggested Alternative Vocabulary (Optional)

If GRD wants to optimize for researcher mental models:

| Current GRD | Research-Aligned Alternative | Notes |
|-------------|------------------------------|-------|
| Phase | Study Component / Module | "Phase" is fine, widely understood |
| Plan | Protocol | More formal, research-feeling |
| Task | Procedure / Step | Less engineering-coded |
| Roadmap | Research Agenda | Common academic term |
| Execute | Conduct | "Conduct an experiment" |
| Verify | Evaluate / Validate | More statistical |
| Discovery | Pilot Investigation | Emphasizes feasibility |

**Recommendation:** Keep current terminology for broad appeal, but document the mapping so researchers understand the parallel.

---

## Researcher Workflow Pain Points (Opportunities for GRD)

### Common Researcher Complaints

1. **"Where did I put that experiment?"** - Tracking is ad-hoc
2. **"I can't reproduce my own results"** - Environment/config drift
3. **"What did I try already?"** - Experiment history gets lost
4. **"I don't know if this is good enough"** - Unclear success criteria
5. **"I have to start over"** - No checkpointing

### How GRD Addresses These

| Pain Point | GRD Feature |
|------------|-------------|
| Lost experiments | Phase/Plan structure with SUMMARY.md |
| Reproducibility | Git commits, explicit plans |
| Forgotten trials | STATE.md tracking, phase history |
| Unclear criteria | Success criteria in roadmap |
| Starting over | Checkpoint system, pause/resume |

---

## Metadata

**Research scope:**
- Academic research lifecycle models
- ML-specific workflow terminology
- CRISP-DM/CRISP-ML methodology
- Experiment vs. study distinction
- Reproducibility culture

**Confidence breakdown:**
- Research lifecycle: HIGH - multiple authoritative academic sources
- ML-specific terms: HIGH - verified with official docs and papers
- GRD mapping: MEDIUM - requires validation with actual researchers
- Alternative vocabulary: LOW - speculative, needs user testing

**Sources used:**
- [Harvard Research Lifecycle](https://researchsupport.harvard.edu/research-lifecycle)
- [NNLM Data Glossary - Research Lifecycle](https://www.nnlm.gov/guides/data-glossary/research-lifecycle)
- [CRISP-DM for Data Science 2025](https://www.datascience-pm.com/wp-content/uploads/2024/12/CRISP-DM-for-Data-Science-2025.pdf)
- [Udacity CRISP-DM Explained](https://www.udacity.com/blog/2025/03/crisp-dm-explained-a-proven-data-mining-methodology.html)
- [Machine Learning Mastery - Controlled Experiments](https://machinelearningmastery.com/controlled-experiments-in-machine-learning/)
- [Google ML - Experiments](https://developers.google.com/machine-learning/managing-ml-projects/experiments)
- [Oregon State - Research Methods in ML (PDF)](https://web.engr.oregonstate.edu/~tgd/talks/new-in-ml-2019.pdf)
- [ICML 2002 - Crafting Papers on ML](https://icml.cc/Conferences/2002/craft.html)
- [Neptune AI - ML Experiment Tracking](https://neptune.ai/blog/ml-experiment-tracking)
- [Weights & Biases - Intro to MLOps Experiment Tracking](https://wandb.ai/site/articles/intro-to-mlops-machine-learning-experiment-tracking/)
- [Reproducibility in ML Research](https://arxiv.org/html/2406.14325v1)
- [Writing ML Research Papers](https://grigorisg9gr.github.io/machine%20learning/research%20paper/how-to-write-a-research-paper-in-machine-learning/)

---

## Key Takeaways for GRD

1. **Study > Experiment > Trial** maps to **Milestone > Phase > Plan** - the hierarchy is aligned
2. **Hypothesis-driven** thinking is central to research - GRD could make hypotheses more explicit
3. **"Phase"** is a comfortable term for researchers - no need to change it
4. **"Plan"** and **"Task"** feel engineering-coded - consider "Protocol" and "Step" for researcher-facing docs
5. **Reproducibility** is culturally central - GRD's git-centric approach aligns well
6. **Iteration is expected** - GRD's "plans can lead to re-planning" matches research reality
7. **Baseline comparison** is fundamental - GRD could emphasize before/after tracking
8. **Success criteria** map to **hypotheses** - both are predictions about outcomes

---

*Research completed: 2026-02-01*
*Ready for terminology decisions: yes*
