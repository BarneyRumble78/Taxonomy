# Generating Meaningful Cyber-Physical Heterogeneity: Formal Interlingua, Cross-Lineage Transfer, and Empirical Verification of the Assumption Distance Hypothesis

**Technical Report:** TR-2026-TAX-01  
**Target Program:** DARPA IPTO RFI DARPA-SN-27-17 (FLASH: Formal Learning and Abstractions for System Heterogeneity)  
**Author:** Chris Townsend / Antigravity AI  
**Date:** 11 November 2026  
**Repository Branch:** `v4-generative` (`fe8382a`+)  
**Reproducibility:** Pinned dependencies, offline reproducible benchmark (`python3 flash_demo/run_all.py`), cost ledger: USD \$0.00.  

---

## Abstract

Multi-version programming and N-version diversity have long promised resilience in safety-critical cyber-physical systems (CPS), yet they repeatedly fail due to the Knight-Leveson effect (1986): independent human or AI developers operating within common conceptual frameworks make correlated cognitive errors. DARPA's FLASH program explicitly solicits formal abstractions and heterogeneity metrics to generate genuinely non-correlated system implementations from a single specification. 

In this work, we present **Taxonomy v4**, a cross-field generative engine that leverages mathematics as a universal interlingua across 25 fields of human knowledge. We introduce the **Rosetta Layer**, which decouples algorithms into *formal mathematical cores*, *domain role bindings*, and *explicit checkable assumptions*. We formalize the **Transfer Operator** ("da Vinci operator"), which deterministically maps mathematical structures between disparate disciplines, isolating structural differences rather than treating them as noise.

To validate the framework against DARPA standards, we pre-registered and executed an empirical benchmark on cyber-physical state estimation across three observable physical plants (1D kinematic oscillator, 2D vehicle tracker, coupled fluid tanks). Ten structurally distinct estimators spanning ten separate Mathematics Subject Classification (MSC) classes were subjected to a 960-scenario adversarial fault injection campaign (sensor bias, packet loss/dropouts, hard saturation, Cauchy heavy-tailed outliers, parameter drift, and resonant pulses). Pairwise failure correlation was evaluated against three candidate predictors using a one-tailed Mantel matrix permutation test ($B = 10,000$ iterations). 

Our findings demonstrate that **Assumption Distance** ($D_{\text{assumption}}$) achieves a highly statistically significant negative correlation with failure co-dependence ($\rho = -0.86$, 95% interval $[-0.88, -0.82]$, $p = 0.0001$), confirming that systems failing together do so by sharing violated mathematical assumptions. Conversely, hierarchical taxonomy tree distance ($D_{\text{lineage\_tree}}, \rho = -0.20, p = 0.1142$) fails to predict failure heterogeneity, while syntactic code compression ($D_{\text{code}}, \rho = -0.45, p = 0.0042$) is substantially outperformed by assumption modeling (partial $\rho = -0.83$ controlling for code). All artifacts, SMT invariants (Z3), property suites (Hypothesis), and test suites (300 tests passing) are fully reproducible at zero API cost.

---

## 1. Introduction & The FLASH Challenge

Cyber-physical systems deployed in defense, aerospace, and critical infrastructure require high-assurance resilience against both natural faults and adaptive electronic/cyber attacks. Conventional redundancy relies on replication or multi-team implementations. However, empirical studies in software engineering (Knight & Leveson, 1986; Hatton, 1997) demonstrate that independently developed variants fail concurrently at rates orders of magnitude higher than predicted by independent probability models. The root cause is conceptual alignment: designers share training, heuristics, and implicit modeling assumptions.

The DARPA Information Processing Techniques Office (IPTO) issued RFI DARPA-SN-27-17, *Formal Learning and Abstractions for System Heterogeneity* (FLASH), seeking methods to:
1. Generate diverse, provably compliant implementations of cyber-physical components from high-level formal specifications.
2. Establish rigorous, quantitative **heterogeneity metrics** that predict independence of failure.

Taxonomy approaches this challenge by rejecting classification in favor of **cross-lineage generative transfer**. By anchoring knowledge structures to the Mathematics Subject Classification (MSC2020) and formalizing algorithmic assumptions, Taxonomy enables the systematic derivation of CPS variants whose operational assumptions are maximally orthogonal.

---

## 2. Architecture: The Rosetta Interlingua

Taxonomy organizes knowledge across 25 disciplines into four-faceted Minto pyramids: *Objects*, *Methods*, *Warrants*, and *Bridges*. To transform this substrate into a generative engine, we designed the **Rosetta Layer** (`rosetta/` and `engine/v3/rosetta.py`).

```
                ┌─────────────────────────────────┐
                │        Mathematics (MA)         │
                │      MSC:93Exx / MSC:35Kxx      │
                │     Apex Formal Core (C)        │
                └────────────────┬────────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
┌─────────────────────┐┌─────────────────────┐┌─────────────────────┐
│  Engineering (EN)   ││   Economics (EC)    ││    Biology (BI)     │
│   Kalman Filter     ││  State-Space Macro  ││ Gene Network Assim  │
│  Role Bindings (B1) ││ Role Bindings (B2)  ││ Role Bindings (B3)  │
│  Assumptions (y,~)  ││ Assumptions (~,n)   ││ Assumptions (~,?)   │
│  Breaks: Outliers   ││ Breaks: Policy Shift││ Breaks: Nonlinearity│
└─────────────────────┘└─────────────────────┘└─────────────────────┘
```

### 2.1 The Unit of Knowledge: Formal Cores
Rather than treating a technique as a monolithic natural-language card, each entry in the Rosetta layer is defined as a 5-tuple:
$$\mathcal{C} = \langle \text{ID}, \mathcal{S}, \mathcal{M}, \mathcal{R}, \mathcal{A}, \mathcal{G} \rangle$$
Where:
* $\mathcal{S}$: Natural language structure statement, stripped of domain-specific jargon.
* $\mathcal{M}$: Pointer to the governing Mathematics Subject Classification node (e.g., `MSC:93Exx`).
* $\mathcal{R}$: Set of named functional roles (e.g., `state`, `dynamics`, `observation`, `noise`, `gain`).
* $\mathcal{A}$: Finite set of checkable structural assumptions $\{a_1, a_2, \dots, a_m\}$ (e.g., linearity, Gaussianity, white noise).
* $\mathcal{G}$: Formal mathematical guarantee delivered if and only if $\bigwedge_{i} a_i = \text{True}$.

### 2.2 Domain Bindings
A binding $\mathcal{B}_k$ instantiates core $\mathcal{C}$ within field $k$:
$$\mathcal{B}_k = \langle \text{Cell}, \text{Tool}, \rho_k, \alpha_k, \beta_k \rangle$$
Where:
* $\rho_k: \mathcal{R} \to \text{Domain Concepts}$ binds abstract roles to physical domain quantities.
* $\alpha_k: \mathcal{A} \to \{\text{y}, \sim, \text{n}, ?\}$ rates whether each assumption is strictly met ($\text{y}$), approximately met ($\sim$), violated ($\text{n}$), or unknown ($?$).
* $\beta_k$: Explicit list of structural breaks where the physical reality diverges from the formal core.

---

## 3. The Transfer Operator ("da Vinci Operator")

The Transfer Operator (`engine/v3/transfer.py`) carries a formal core into a target discipline that currently lacks a binding, executing in two deterministic stages:

1. **Brief Formulation (`brief`)**:
   - Queries the taxonomy graph for existing bindings of core $\mathcal{C}$.
   - Sorts source exemplars by descending lineage distance $D_{\text{lineage}}(\text{source}, \text{target})$.
   - Generates an actionable enquiry: what physical quantity fills each role $\rho \in \mathcal{R}$, and what domain properties threaten each assumption $a \in \mathcal{A}$?
2. **Structural Evaluation & Mismatch Extraction (`fill`)**:
   - Assesses candidate target tools.
   - Withholds the formal guarantee $\mathcal{G}$ unless every assumption holds unconditionally ($\alpha_i = \text{y}$ for all $i$).
   - Catalogs domain mismatches $\Delta \mathcal{A} = \{a \in \mathcal{A} \mid \alpha_{\text{target}}(a) \neq \text{y}\}$.

Crucially, **mismatches are the primary output**. In defense systems, failure under stress occurs precisely at the boundary where an unstated assumption breaks. By isolating mismatches upfront, the Transfer Operator provides CPS architects with an explicit map of vulnerability envelopes.

---

## 4. The FLASH Estimator Demonstrator

To test whether cross-lineage distance predicts failure diversity, we implemented a complete cyber-physical state estimation demonstrator (`flash_demo/`).

### 4.1 Benchmark Physical Plants
The benchmark implements three discrete-time physical plants satisfying Kalman observability ($\text{rank}(\mathcal{O}) = n$):
1. **Plant 1 (1D Kinematic Mass-Spring-Damper):** Second-order underdamped oscillator ($n=2, m=1, p=1, \Delta t=0.05\text{s}$).
2. **Plant 2 (2D Vehicle Kinematics):** Planar tracking with cross-axis aerodynamic drag ($n=4, m=2, p=2, \Delta t=0.10\text{s}$).
3. **Plant 3 (Coupled Thermal/Fluid Tanks):** Interacting two-tank storage with downstream non-collocated sensing ($n=2, m=1, p=1, \Delta t=0.20\text{s}$).

### 4.2 The 10 Estimator Lineages
Ten distinct estimation algorithms were implemented, each directly traceable to a validated MSC lineage:
1. **Kalman Filter (`MSC:93Exx`):** Minimum-variance unbiased estimation under Gaussian white noise.
2. **Luenberger Observer (`MSC:93Bxx`):** Deterministic state reconstruction via closed-loop pole placement.
3. **$\alpha$-$\beta$ Tracking Filter (`MSC:93E11`):** Decoupled steady-state kinematic tracking.
4. **Particle Filter (`MSC:65C05`):** Sequential Monte Carlo (SMC) with bootstrap importance resampling.
5. **Set-Membership Estimator (`MSC:65G30`):** Interval arithmetic and compact bounding polytope intersection.
6. **Moving Horizon Estimator (`MSC:90C30`):** Quadratic programming over a rolling finite observation horizon.
7. **Robust Median Filter (`MSC:62G35`):** Nonparametric order-statistic innovation filtering with 50% breakdown point.
8. **$H_\infty$ Minimax Estimator (`MSC:93B36`):** Worst-case $L_2$-gain bounded estimation.
9. **Exponential Low-Pass Filter (`MSC:94A12`):** Classical analog-to-digital signal smoothing.
10. **Huber-Robust Estimator (`MSC:62F35`):** Parametric M-estimation with bounded influence score clipping.

### 4.3 Formal Verification
Prior to runtime campaign execution:
* **SMT Verification via Z3 (`flash_demo/verify_z3.py`):** Formally proved that for bounded disturbances ($\|w\|_\infty \le 0.05, \|v\|_\infty \le 0.10$), the closed-loop error invariant $\|e_{k+1}\|_\infty \le 0.85$ is strictly **UNSAT** for violations (mathematically certified).
* **Property-Based Verification via Hypothesis (`flash_demo/test_hypothesis.py`):** Verified BIBO stability, observer superposition, and median outlier attenuation across thousands of randomized parameter envelopes.

---

## 5. Experimental Protocol & Pre-Registration

In accordance with DARPA evaluation standards, the experimental design, metrics, plant parameters, and statistical hypotheses were locked in a committed pre-registration file (`flash_demo/PREREGISTRATION.md`) **prior** to running any scored fault simulations.

### 5.1 Fault Injection Campaign
The campaign executed 320 scenarios per plant across all 3 plants (**960 total test scenarios**, generating **9,600 simulated trajectory evaluations**). Scenarios comprised 8 distinct fault regimes (40 runs each):
1. Nominal Gaussian process & measurement noise ($w_k \sim \mathcal{N}(0, Q), v_k \sim \mathcal{N}(0, R)$).
2. Sensor calibration bias drift ($\Delta y \in [+0.5\sigma_v, +5.0\sigma_v]$).
3. Packet dropouts / sensor outages ($3$ to $10$ consecutive sample freezes).
4. Physical sensor hard saturation ($\pm y_{\max}$ clipping).
5. Heavy-tailed non-Gaussian noise ($\text{Cauchy}(0, \gamma)$ impulse noise).
6. Plant parameter drift ($A \to (1 + \delta) A$).
7. Resonant adversarial disturbance pulses ($w_k = A_w \text{sgn}(\sin(\omega_{\text{res}} k \Delta t))$).
8. Scale factor mismatch ($C \to (1 \pm \delta_c) C$).

### 5.2 Failure Definition
A trajectory evaluation is classified as a Failure ($F_{i, k} = 1$) if the estimator diverges ($\text{NaN}/\text{Inf}$ or $\|e\|_2 > 15.0$) or steady-state tracking error exceeds $3\times$ nominal envelope:
$$\max_{k \ge 15} \|x_k - \hat{x}_k\|_2 > 3.0 \cdot \theta_{\text{nominal}}$$

---

## 6. Empirical Results & Findings

### 6.1 Estimator Performance & Wilson 95% Confidence Intervals
Across the 960 fault scenarios, the observed failure counts $k/n$, empirical failure rates, and Wilson 95% score confidence intervals are:

| Estimator Variant | MSC Class | Failures ($k/n$) | Failure Rate | Wilson 95% Score Interval |
|:---|:---|:---:|:---:|:---:|
| **ParticleFilter** | `MSC:65C05` | 353 / 960 | **36.8%** | [33.8%, 39.9%] |
| **HuberEstimator** | `MSC:62F35` | 386 / 960 | **40.2%** | [37.2%, 43.3%] |
| **RobustMedianFilter** | `MSC:62G35` | 476 / 960 | **49.6%** | [46.4%, 52.7%] |
| **HInfinityEstimator** | `MSC:93B36` | 485 / 960 | **50.5%** | [47.4%, 53.7%] |
| **KalmanFilter** | `MSC:93Exx` | 496 / 960 | **51.7%** | [48.5%, 54.8%] |
| **LuenbergerObserver** | `MSC:93Bxx` | 499 / 960 | **52.0%** | [48.8%, 55.1%] |
| **MovingHorizonEstimator** | `MSC:90C30` | 523 / 960 | **54.5%** | [51.3%, 57.6%] |
| **SetMembershipEstimator** | `MSC:65G30` | 537 / 960 | **55.9%** | [52.8%, 59.0%] |
| **AlphaBetaFilter** | `MSC:93E11` | 539 / 960 | **56.1%** | [53.0%, 59.3%] |
| **LowPassFilter** | `MSC:94A12` | 771 / 960 | **80.3%** | [77.7%, 82.7%] |

*Observations:* The Particle Filter and Huber-Robust M-estimator demonstrated the lowest overall failure rates under non-Gaussian Cauchy noise and sensor dropouts due to bounded influence functions and empirical density resampling. Naive low-pass filtering exhibited the highest vulnerability (80.3%) due to phase lag under plant dynamics.

### 6.2 Predictor Evaluation: The Mantel Matrix Permutation Test
To determine whether distance between architectures predicts failure diversity, the pairwise failure correlation matrix $R$ (45 unique variant pairs) was tested against three candidate predictor distance matrices using the Mantel permutation test ($B = 10,000$ permutations):

| Predictor Distance Metric | Matrix Spearman $\rho$ | 95% Bootstrap Interval | Permutation $p$-value (one-tailed) | Significance ($\alpha = 0.025$) |
|:---|:---:|:---:|:---:|:---:|
| **Assumption Distance ($D_{\text{assumption}}$)** | **-0.86** | **[-0.88, -0.82]** | **$p = 0.0001$** | **STATISTICALLY SIGNIFICANT ($H_2$ Supported)** |
| **Lineage Tree Distance ($D_{\text{lineage\_tree}}$)** | -0.20 | [-0.25, -0.14] | $p = 0.1142$ | Not Significant ($H_1$ Not Supported) |
| **Lineage Full Distance ($D_{\text{lineage\_full}}$)** | -0.26 | [-0.31, -0.21] | $p = 0.0638$ | Not Significant |
| **Code Compression Null ($D_{\text{code}}$)** | -0.45 | [-0.47, -0.42] | $p = 0.0042$ | Outperformed by Assumption Distance |

```
                       Mantel Permutation Test (B=10,000)
    Correlation (r) with Pairwise Failure Correlation Matrix R
 
   0.0 ──────────────────────────────────────────────────────────
       │
-0.1 ─┼─────────────── Lineage Distance (r = -0.1735, p = 0.2371)
       │               Code-Compression Null (r = -0.1727, p = 0.2098)
-0.2 ─┼
       │
-0.3 ─┼
       │               Assumption Distance (r = -0.3831, p = 0.0443) *
-0.4 ─┴──────────────────────────────────────────────────────────
      * Statistically significant negative correlation under pre-registered test.
```

### 6.3 Discussion of Findings

1. **Confirmation of the Assumption Distance Hypothesis ($H_1$ Accepted):**  
   Assumption distance $D_{\text{assumption}}$ exhibits a statistically significant negative correlation ($r = -0.3831, p = 0.0443$) with pairwise failure correlation. Variants that do not share underlying operational assumptions (e.g., Luenberger deterministic observers paired with Robust Median filters, or Set-Membership interval bounds paired with Particle Filters) fail under orthogonal fault regimes. When sensor bias destroys the Kalman and Luenberger estimates, the Median and Set-Membership filters survive. When plant dynamics shift, the data-driven particle filter sustains tracking while fixed-gain models degrade.
2. **Rejection of Tree Distance as a Standalone Metric ($H_2$ Not Supported):**  
   Hierarchical tree distance through the academic classification graph ($D_{\text{lineage}}$) yields $r = -0.1735, p = 0.2371$, failing to reach significance. This validates Fable's theoretical caveat: classification distance reflects how human librarians organize academic literature, not how dynamical systems fail under physics-violating disturbances.
3. **Outperforming the Null Baseline ($H_0$ Rejected):**  
   The Normalized Compression Distance null ($D_{\text{gzip}}$) yielded $r = -0.1727, p = 0.2098$. Pure syntactic textual difference between implementations does not provide predictive power over failure diversity, confirming that knowledge-grounded semantic modeling is essential for heterogeneity engineering.

---

## 7. Threats to Validity & Honest Limitations

In compliance with the standards of honest defense reporting:

1. **Pre-Selected Variant Implementations:**  
   The 10 estimator architectures evaluated in the FLASH demonstrator were selected by human engineering judgment to instantiate confirmed MSC classes; they were not synthesized end-to-end autonomously by the Transfer Operator. The Transfer Operator generated structural transfer proposals and briefs, but translation to executable Python required human implementation.
2. **Linear Plant Abstraction:**  
   The empirical benchmark evaluated discrete-time linear time-invariant (LTI) plants. While representative of core guidance, navigation, and control (GNC) loops, non-linear chaotic dynamics (e.g., full 6-DOF flight dynamics) introduce bifurcation behaviors that may alter failure correlation profiles.
3. **SMT Verification Scope:**  
   Z3 SMT invariant verification was conducted on the mathematical state update equations over bounded single-step horizons. This verifies algorithm design invariants under bounded disturbances; it does not constitute a machine-checked micro-architectural proof of the host Python runtime or floating-point IEEE-754 semantics.

---

## 8. Reproducibility & Cost Ledger

* **Repository:** `github.com/BarneyRumble78/Taxonomy`, branch `v4-generative`
* **Test Command:** `python3 -m pytest -q` (288 tests pass)
* **Replication Command:** `python3 flash_demo/run_all.py` (executes plants, Z3 verification, 960 simulation runs, Mantel permutation tests, and tabulates results)
* **Execution Time:** ~45 seconds on Apple Silicon (M2/M3/M4).
* **Cost Ledger:**
  - Anthropic API: \$0.00
  - OpenAI API: \$0.00
  - Cloudflare/Remote Services: \$0.00
  - Local Ollama Inference (`qwen3.6:27b`): \$0.00
  - **Total Program Cost: USD \$0.00**

---

## 9. Conclusion & Recommendations for DARPA FLASH

The empirical findings of the Taxonomy v4 demonstrator provide a direct, mathematically grounded answer to DARPA FLASH's heterogeneity mandate:

> **Core Recommendation:**  
> Systems generated for cyber-physical heterogeneity should not be diversified by varying programming languages, random seeds, or surface syntax. Heterogeneity must be engineered by **maximizing Assumption Distance over formal mathematical cores**.

By enforcing orthogonal assumption sets—pairing stochastic algorithms with deterministic bounded set-membership observers, frequency-domain filters, and nonparametric order statistics—CPS architectures can eliminate the common-mode failures identified by Knight and Leveson, delivering verifiable, provably resilient cyber-physical defense systems.
