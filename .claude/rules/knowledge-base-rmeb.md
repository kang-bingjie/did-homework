---
paths:
  - "2026Spring/LectureNotes/**/*.qmd"
  - "2026Spring/Labs/**/*.ipynb"
  - "2026Spring/LectureNotes/**/*.tex"
---

# Knowledge Base: Empirical Methods in Economics and Management (RMEB)

**Domain-specific knowledge for the five-pillar RMEB graduate course.**

---

## Course Identity

- **Course**: 经济与商务实证研究方法 (Empirical Methods in Economics and Management Studies)
- **Audience**: Master's and PhD students, Business School, Renmin University of China
- **Instructor**: Chen, Zhiyuan (陈志远)
- **Format**: 8 weeks, Friday 8:00–11:30
- **Language**: Chinese instruction, English academic sources
- **Paradigm**: AI-native empirical research training

---

## The Five Pillars

| Pillar | Week | Core Concept | Key Tool |
|--------|------|-------------|---------|
| Reduced-form causal inference | 3 | Identification via design | Stata, R (fixest, did) |
| Causal ML | 4 | Orthogonalization + honest trees | Python (doubleml, econml) |
| Structural estimation | 5–6 | Primitives + counterfactuals | Matlab, Python (scipy) |
| LLM text analysis | 7 | Annotation + validation | Python (openai, anthropic) |
| AI research automation | 8 | Audit trails + governance | Copilot, Claude Code |

---

## Notation Registry

| Symbol | Meaning | Convention | Anti-Pattern |
|--------|---------|-----------|-------------|
| $Y_i(1), Y_i(0)$ | Potential outcomes | Parentheses notation | $Y_{i1}, Y_{i0}$ |
| $Y_i$ | Observed outcome | No parentheses | $Y_i^*$ |
| $D_i$ | Treatment indicator | D or W | T (reserved for time) |
| $\tau$ | ATE | $E[Y(1)-Y(0)]$ | $\beta$ without context |
| $\tau(x)$ | CATE | Conditional on X=x | $\tau$ without argument |
| $e(X)$ | Propensity score | $P(D=1\|X)$ | $\pi$ (reserved for profit) |
| $X_i$ | Covariates | Pre-treatment | Z (reserved for instruments) |
| $Z_i$ | Instruments | IV setting | X (confusion with covariates) |
| $g(X)$ | Nuisance outcome model | DML setting | — |
| $m(X)$ | Nuisance treatment model | DML setting | — |

---

## Methods Registry

### Pillar 1: Reduced-Form Causal Inference

| Method | Key Assumption | Stata Command | R Package |
|--------|----------------|---------------|-----------|
| Panel FE | Strict exogeneity | `xtreg, fe` | `fixest::feols` |
| Two-Way FE (TWFE) | Parallel trends | `reghdfe` | `fixest::feols` |
| Callaway-Sant'Anna DID | Parallel trends, no anticipation | `csdid` | `did::att_gt` |
| Sun-Abraham | Heterogeneous treatment timing | `eventstudyinteract` | `fixest` with interactions |
| Synthetic Control | RMSPE-based donor matching | `synth` | `Synth::synth` |
| Sharp RD | Continuity of potential outcomes | `rdrobust` | `rdrobust::rdrobust` |
| Fuzzy RD / IV | Exclusion + relevance | `ivregress 2sls` | `fixest::feiv` |

### Pillar 2: Causal ML

| Method | Key Assumption | Python Package | R Package |
|--------|----------------|----------------|-----------|
| LASSO | Sparsity | `sklearn.linear_model.Lasso` | `glmnet` |
| DML (Partially Linear) | Neyman orthogonality | `doubleml` | `DoubleML` |
| DML (Interactive) | Neyman orthogonality | `doubleml` | `DoubleML` |
| Causal Forest | Honesty, overlap | `econml.grf` | `grf::causal_forest` |
| X-Learner | Overlap | `econml` | — |
| AIPW / DR-Learner | Doubly robust | `econml` | `drgee` |

### Pillar 3: Structural Estimation

| Model | Identification | Tool |
|-------|---------------|------|
| Logit / Nested Logit demand | Price variation, product characteristics | Stata, Python |
| BLP (Berry-Levinsohn-Pakes) | IV for endogenous prices | Matlab, Python (`pyblp`) |
| Gravity model | Trade flows, Anderson-van Wincoop | Stata (`ppmlhdfe`), R |
| Entry model (Bresnahan-Reiss) | Market size variation | Matlab, Python |

### Pillar 4: LLM Text Analysis

| Task | Method | Validation Standard |
|------|--------|-------------------|
| Binary classification | Single-prompt | Human benchmark ≥ 80% agreement |
| Multi-class coding | Batch + stacked | Krippendorff's α ≥ 0.6 |
| Scoring / continuous measure | Calibrated prompts | Correlation with human scores |
| Named entity extraction | Few-shot | F1 on validation sample |

### Pillar 5: AI Research Automation

- "Trust but verify" = AI drafts → human reads → human tests → audit note
- Required AI appendix fields: tool used, task, accepted example, rejected example, verification method
- Failure modes to teach: hallucinated citations, unverified code, over-automated robustness farming

---

## Anti-Patterns

| Anti-Pattern | Correction |
|-------------|-----------|
| Confusing prediction R² with causal identification | Show: high R² ≠ no omitted variable bias |
| Using TWFE with heterogeneous treatment timing without correction | Use Callaway-Sant'Anna or Sun-Abraham |
| Treating LLM annotation output as ground truth | Always compare to human-coded sample |
| Running DML without cross-fitting | Use `n_folds ≥ 2` in `DoubleML` |
| Structural parameters estimated without stating identification source | Every parameter needs its identifying variation |
| AI-generated code submitted without reproduction check | Reproduce tables independently from script |

---

## Key Equations

### Parallel Trends (DID)

$$E[Y_{it}(0) | D_i=1, t=1] - E[Y_{it}(0) | D_i=1, t=0] = E[Y_{it}(0) | D_i=0, t=1] - E[Y_{it}(0) | D_i=0, t=0]$$

### Double ML (Partially Linear Model)

$$Y = D\theta_0 + g_0(X) + \varepsilon, \quad E[\varepsilon|X,D]=0$$
$$D = m_0(X) + V, \quad E[V|X]=0$$

Residual-on-residual regression: $\hat{V} = D - \hat{m}(X)$, then regress $(Y - \hat{g}(X))$ on $\hat{V}$.

### Causal Forest CATE

$$\hat{\tau}(x) = \arg\min_{\tau} \sum_{i=1}^n \alpha_i(x) \left(Y_i - \bar{Y}_i - \tau(D_i - \bar{D}_i)\right)^2$$

where $\alpha_i(x)$ are random forest kernel weights.

### BLP Demand (Berry 1994 Contraction)

$$\delta_j = \ln(s_j) - \ln(s_0)$$
$$s_j(\delta) = \frac{e^{\delta_j}}{1 + \sum_k e^{\delta_k}}$$

---

## Stata Code Conventions

- Always `set more off` at top of do-files
- Use `reghdfe` for HDFE regressions, not `xtreg`
- Cluster standard errors: `vce(cluster id)` where `id` is the treatment unit
- Use `estout` / `esttab` for formatted regression tables
- Preserve/restore pattern for exploratory commands
- All do-files must end with `log close` if a log is opened
- Random seeds: `set seed 12345` at top of simulation do-files

---

## Python Code Conventions

- Use `pathlib.Path` for all file paths
- Set `random_state=42` (sklearn) or `np.random.seed(42)` at top
- `matplotlib` Chinese font setup required for any figure with Chinese labels
- Use `DoubleML` (not hand-coded) for DML estimation
- Use `econml` (not hand-coded) for causal forests
- Always use `cross_val_score` with stratified folds for classification tasks

---

## Course Literature Spine

### Reduced-Form
- Angrist & Pischke (2009) *Mostly Harmless Econometrics*
- Callaway & Sant'Anna (2021) JoE — Staggered DID
- Goodman-Bacon (2021) JoE — DID decomposition
- Sun & Abraham (2021) JoE — Staggered heterogeneous effects

### Causal ML
- Chernozhukov et al. (2018) *The Econometrics Journal* — Double ML
- Wager & Athey (2018) JASA — Causal forests
- Athey & Imbens (2019) JEP — Machine learning methods in economics

### Structural
- Berry (1994) RAND — BLP logit inversion
- Anderson & van Wincoop (2003) AER — Gravity equation
- Bresnahan & Reiss (1991) JPE — Entry and competition

### LLM Text Analysis
- Ludwig, Mullainathan & Rambachan (2025) NBER — LLMs as econometric tools
- Dell (2024) NBER — Deep learning for economists
- Fang, Li & Lu (2025) NBER — Decoding China's industrial policies

### AI Workflow
- Korinek (2023) — *Generative AI for economic research*
- Course policy: "vibe coding with audit trails"
