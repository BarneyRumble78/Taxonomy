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

## Audit 3: the 24 other fields, ten cards each (in progress)

Samples are drawn with seed `20261113 + sum of the character codes of the field code`, from cards carrying tools at levels 1 and 2 together.
The sample lists are reproducible from that rule. Roughly 400 tools are in the samples.

**Progress: BI partly checked, 14 of 17 tools.** No misses. Nine confirmed. Five not confirmed by the page read
(alignment correctness and site independence for phylogenetics; De Bruijn coverage and repeat conditions; breeder's equation scope;
segregation distortion; decoy-based false discovery rate; ethogram reliability requirement counted with these).

Other fields: not started.

## Not yet audited

- The 24 non-mathematics fields, levels 1 and 2 (the handover asks for 10 cards per field).
- `cards/toolkit/MA.json`, the 63 two-digit cards that predate this work.
