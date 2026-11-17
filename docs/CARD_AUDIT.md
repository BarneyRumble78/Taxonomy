# Toolkit card audit

## Audit 1: mathematics, three-digit depth (`cards/toolkit/MA_L2.json`)

Date: 13 November 2026. Auditor: claude-fable-5-2, the same model that drafted the cards. This is not an independent review.

**Sample.** 30 cards drawn at random, seed `20261113`, from the 297 cards that carry tools.
Cards without tools were left out of the draw because they hold nothing to check. The 30 cards hold 61 tools.

**Method.** Each tool's hypotheses were compared with the statement on the English Wikipedia page for that result,
read on 13 November 2026 through a summarising page reader. Wikipedia is a reference that can be cited, but it is not a textbook,
and the reader can miss detail. A specialist check against textbooks would be stronger.

**Rule used.** A tool is a *miss* if a hypothesis needed for the result is absent or wrong.
Hypotheses that are stricter than necessary are not counted as misses. A tool is *not confirmed* if the page neither supports nor contradicts a stated hypothesis.

### Result

| | Count | Share | Wilson 95% interval |
|---|---:|---:|---:|
| Tools with a miss | 8 of 61 | 13% | 7% to 24% |
| Tools not confirmed by the source read | 6 of 61 | 10% | 5% to 20% |
| Tools confirmed | 47 of 61 | 77% | |
| Cards with at least one miss | 7 of 30 | 23% | 12% to 41% |

Read plainly: roughly one mathematics tool in eight had a hypothesis missing or imprecise as drafted. Under R5 each of those is an error.

### Misses

| Card | Tool | What was wrong | Page |
|---|---|---|---|
| 74Sxx | Céa's lemma | Boundedness (continuity) of the bilinear form was missing | Céa's lemma |
| 20Cxx | Schur's lemma | The scalar form needs finite-dimensional representations; this was missing | Schur's lemma |
| 83Cxx | Positive mass theorem | Completeness of the initial data was missing; the result is per asymptotic end | Positive energy theorem |
| 83Cxx | Penrose singularity theorem | "Trapped surface" should be "closed trapped surface"; Cauchy surface should be connected | Penrose–Hawking singularity theorems |
| 44Axx | Convolution theorem | "Functions for which the transform converges" is too loose | Convolution theorem |
| 68Txx | Optimality of A* search | "Consistent for graph search" is true only when expanded nodes are never reopened | A* search algorithm |
| 05Cxx | Euler's formula for planar graphs | "Finite" was missing | Planar graph |
| 74Cxx | Limit analysis theorems | Convexity of the yield surface was missing; "small displacements" should be "small strains" | Limit analysis |

### Not confirmed by the source read

These were neither supported nor contradicted. They need a better source.

| Card | Tool | Hypothesis not confirmed |
|---|---|---|
| 49Qxx | Isoperimetric inequality | That the class is sets of finite perimeter |
| 76Dxx | Leray's theorem on weak solutions | Square-integrable divergence-free initial data |
| 49Lxx | Hamilton–Jacobi–Bellman equation with viscosity solutions | That the value function is the viscosity solution |
| 19Lxx | Bott periodicity theorem | The restriction to compact Hausdorff spaces |
| 44Axx | Laplace inversion formula | The stated conditions for the Bromwich integral |
| 83Cxx | Choquet-Bruhat's theorem | Attribution, vacuum case and local nature |

### Confirmed

03Fxx (Gödel first and second; cut-elimination), 05Axx (inclusion-exclusion; Burnside; generating functions),
05Cxx (Hall; max-flow min-cut; four colour), 06Exx (Stone), 11Hxx (Minkowski), 11Kxx (Weyl), 11Uxx (Matiyasevich), 14Cxx (Bézout),
15Bxx (Perron–Frobenius; Gershgorin), 20Bxx (orbit-stabiliser; Cayley), 20Cxx (Maschke; character orthogonality),
30Axx (Cauchy; maximum modulus), 31Axx (maximum principle; Perron), 46Hxx (Gelfand–Mazur; spectral radius), 49Jxx (direct method),
53Exx (Hamilton), 58Axx (Stokes; de Rham; Frobenius), 60Kxx (renewal; Pollaczek–Khinchine; Little), 60Lxx (Lyons),
65Kxx (gradient descent; interior-point; simplex), 68Txx (universal approximation; perceptron), 76Dxx (Stokes drag), 76Nxx (isentropic relations),
83Cxx (Birkhoff).

### What was done afterwards

The eight misses were corrected in the source files, and the same A* wording was corrected where it also appears in the computing cards.
**The figures above describe the cards as drafted, before those corrections.** The other 267 mathematics cards with tools were not checked,
so the same error rate should be expected in them until they are.

## Audit 2: mathematics, all remaining cards with tools (in progress)

Started 13 November 2026. Same method and rule as audit 1. The 267 cards outside the first sample hold 489 distinct tool statements.

**Progress: 49 of 489 checked** (classes 03 to 13, part).

| | Count |
|---|---:|
| Confirmed | 44 |
| Miss | 1 |
| Not confirmed by the source read | 4 |

Miss: 03Bxx, Gödel's completeness theorem. The card did not say that uncountable languages need a choice principle. Corrected.

Not confirmed: 11Jxx Dirichlet's approximation theorem (page formula unreadable); 12Fxx Abel–Ruffini (characteristic zero is implied, not stated);
12Hxx Liouville's theorem (the equal-constants condition is not on the page); 12Lxx and 14Pxx Tarski–Seidenberg (page treats the real numbers only).

The page reader flagged two further items that were judged not to be misses on reading its reason:
quadratic reciprocity (the card's hypothesis, two distinct odd primes, is the page's) and Hensel's lemma (the simple-root form does not need a monic polynomial).

**440 tool statements remain unchecked** (classes 13 to 94).

## Audit 3: the 23 other fields with tools, ten cards each

Date: 14 to 18 November 2026. Indigenous knowledge has no tools to check.

**Sample.** For each field, ten cards drawn at random from the cards carrying tools at levels 1 and 2 together,
seed `20261113 + sum of the character codes of the field code`. Every distinct tool on those cards was checked: 315 tools.

**Method.** Same rule as audit 1. The lookups were done by helper agents running a smaller model (claude-sonnet), each reading
English Wikipedia or, where no page existed, another named source. Every reported miss was then reviewed by the drafting model
against the card's own description before being accepted. This is not an independent specialist review.

| Code | Field | Tools | Confirmed | Miss | Not confirmed | Miss rate, Wilson 95% |
|---|---|---:|---:|---:|---:|---:|
| BI | Biology | 17 | 11 | 0 | 6 | 0% to 18% |
| CH | Chemistry | 18 | 14 | 1 | 3 | 1% to 26% |
| MD | Medicine | 17 | 9 | 0 | 8 | 0% to 18% |
| AG | Agriculture | 10 | 6 | 0 | 4 | 0% to 28% |
| PH | Physics | 20 | 14 | 0 | 6 | 0% to 16% |
| EA | Earth science | 15 | 6 | 0 | 9 | 0% to 20% |
| EV | Environment | 11 | 6 | 0 | 5 | 0% to 26% |
| EN | Engineering | 11 | 7 | 0 | 4 | 0% to 26% |
| CS | Computing | 21 | 20 | 0 | 1 | 0% to 15% |
| IS | Information science | 18 | 16 | 0 | 2 | 0% to 18% |
| DE | Design | 14 | 8 | 0 | 6 | 0% to 22% |
| ST | Strategy | 15 | 13 | 0 | 2 | 0% to 20% |
| EC | Economics | 18 | 12 | 1 | 5 | 1% to 26% |
| BU | Business | 15 | 13 | 0 | 2 | 0% to 20% |
| MS | Mind and society | 14 | 8 | 0 | 6 | 0% to 22% |
| ED | Education | 10 | 5 | 0 | 5 | 0% to 28% |
| PO | Politics | 11 | 9 | 0 | 2 | 0% to 26% |
| LA | Law | 10 | 8 | 0 | 2 | 0% to 28% |
| PL | Philosophy | 13 | 11 | 0 | 2 | 0% to 23% |
| LN | Languages | 6 | 6 | 0 | 0 | 0% to 39% |
| HI | History | 13 | 11 | 0 | 2 | 0% to 23% |
| AR | Arts | 13 | 6 | 0 | 7 | 0% to 23% |
| RE | Religion | 5 | 4 | 0 | 1 | 0% to 43% |
| | **All** | **315** | **223** | **2** | **90** | **0% to 2%** |

### Misses (both accepted and corrected)

| Card | Tool | What was wrong |
|---|---|---|
| CH.TK.340306 (and level 1 CH.TK.3403) | Carothers equation | Equal amounts of the two functional groups, and linear bifunctional monomers, were not stated |
| EC.TK.E2 | Tobin's q theory of investment | Hayashi's condition also needs linearly homogeneous adjustment costs and price-taking, not only constant returns |

### What the "not confirmed" column means

90 of 315 tools (29%) could not be settled from the source read. In almost every case the page did not
mention the condition at all, rather than contradicting it. The share is highest in fields whose "hypotheses" are conditions of good
practice rather than theorem statements: Earth science, Arts, Medicine, Design, Mind and society, Education. A specialist or a textbook
would settle these better than an encyclopaedia.

The low miss rate here should be read with that in mind: an unsettled condition is not a confirmed one.

<details><summary>Tools not confirmed, by field</summary>

- **BI**: Peptide mass spectrometry with database search; Network centrality and module detection; Ordinary differential equation network model; Flux balance analysis; De Bruijn graph assembly; Mendelian segregation
- **CH**: Dose-response bioassay; Arrhenius equation; Retrosynthetic analysis
- **MD**: Hill dose-response model; Fick principle; Direct age standardisation; Pedigree analysis; Validated rating scales; Bayesian diagnostic reasoning with likelihood ratios; Cost-effectiveness analysis; Multivariable risk score (Framingham-type)
- **AG**: Standardised Precipitation Index; Reference evapotranspiration with crop coefficients (FAO-56); Difference-in-differences; Monin–Obukhov similarity theory
- **PH**: Equations of stellar structure; Reynolds-averaged Navier–Stokes with a closure model; Renormalisation group; Momentum from track curvature; Calorimetry; Percolation analysis of robustness
- **EA**: Oxygen-isotope proxies; Gaussian plume model; Degree-day melt model; Monin–Obukhov similarity theory; Eddy covariance; Universal Soil Loss Equation; Shields criterion; Lossless entropy coding; Stefan solution
- **EV**: Cohort-component projection; Travel cost method; Hedonic pricing; Surplus production model; Quantitative structure-activity relationship
- **EN**: Smith predictor; Time study; Bloch equations; Allan variance
- **CS**: Conformance testing against WCAG
- **IS**: Fixity checking with checksums; Collaborative filtering by matrix factorisation
- **DE**: Steady-state heat loss (U-value); Elemental cost planning; Anthropometric design for percentiles; Four-step travel demand model; Map overlay suitability analysis; Conservation by significance assessment (Burra Charter process)
- **ST**: Military decision-making process; Order-of-battle analysis
- **EC**: Spatial equilibrium (Rosen–Roback); Oates decentralisation theorem; Monocentric city model; Hedonic price model; Life-cycle and permanent income hypothesis
- **BU**: Van Westendorp price sensitivity meter; Event study
- **MS**: Intergenerational mobility table; Factor analysis; Intersectional analysis; Event history analysis (Cox model); Drift-diffusion model; General linear model for functional imaging
- **ED**: Classical test theory; Cluster randomised trial; Critical incident technique; Generalisability study; Logic model with outcome evaluation
- **PO**: Mill's methods of agreement and difference; Process tracing
- **LA**: Functional method of comparative law; Proportionality test
- **PL**: Charitable exegesis; Dutch book argument
- **HI**: Comparative history; Dating by letter forms
- **AR**: Close reading; Stylometric authorship attribution; Pigment analysis; Infrared reflectography and X-radiography; Attribution by comparison; Historic-geographic method; Watermark dating
- **RE**: Comparative method in the study of religion

</details>

## Not yet audited

- The 24 non-mathematics fields, levels 1 and 2 (the handover asks for 10 cards per field).
- `cards/toolkit/MA.json`, the 63 two-digit cards that predate this work.
