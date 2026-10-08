# The Mathematics Pyramid, reconciled (MA, v2)

Replaces both v1 versions: the four-layer MSC pyramid (K1–K4) and the five-object pyramid in the twelve volume. The object/method split of the twelve volume is kept as the primary partition, because every other pyramid uses it. The K-layers survive as the ORDER of Side A (dependency order) and as the grouping of Side C bridges. Every one of the 63 MSC2020 two-digit classes lands exactly once (checked by script).

## Governing thought
Mathematics is exhausted by two sides of one pyramid: claims about a mathematical object — the assumptions of proof, structure, space, change and the continuum, or chance — and practices that define, prove, compute, infer from data, or model a claim from another field. Every MSC class is a bridge: a community working one object cell with a characteristic subset of those practices. An application in physics or economics is that field's claim, written in this language.

## SCQA
- Situation. Mathematics states what follows from stated assumptions. MSC2020 files it as 63 classes, 529 three-digit and 6,022 five-digit classes (6,006 in the March 2020 announcement).
- Complication. Two v1 pyramids disagree. One sorts by role in a dependency chain and calls probability applied; the other sorts by object and calls chance core. MSC numbering hides dependency, and its cross-cutting classes (00, 97, 58, 19, 37) are where MathSciNet and zbMATH disagree most (EMS Newsletter, June 2018: F1 0.83 top level, 0.72 second, 0.58 third over 78,063 articles).
- Question. What single partition places every theorem, practice and MSC class exactly once, and agrees with the other pyramids' object/method split?

## Key line
Logic inductive · plural noun partitions · dimension role in the taxonomy (object / practice / community) · order structural.
1. Every theorem is about one object: the assumptions of proof, structure, space, change and the continuum, or chance.
2. Every practice is one role: define, prove, compute, infer from data, or model an outside claim.
3. Every MSC class is a bridge: an object cell worked by a subset of the roles, or mathematics as the object of another pyramid.

## Assignment rules
- An MSC class's home is the cell that owns its typical theorem. Applied classes 70–94 are modelling bridges: the equation as a law is physics, chemistry, economics; existence, uniqueness and regularity of its solutions are MA.O.A4 (e.g. 35Q30 Navier–Stokes).
- Probability (60) is an object, MA.O.A5 (measure of total mass one). Statistics (62): a theorem about an estimator is A5; a procedure applied to data is role B4. Causal identification designs belong to economics (EC.B2) and are cited.
- Category theory (18) sits in A1 as the language of structure-preserving maps. Contested: if foundations means logic plus ZFC only, 18 moves to A2. Moving it changes no other placement.
- Computability (03D) is owned here. Complexity theory's theorems are W1 claims; the class 68 home is bridge C3, and CS cites MA for computability and owns cost models of machines (CS.O.A2).
- Information and coding theorems (94A) are owned at bridge C4 "information"; engineering (EN.O.A4) and CS (CS.O.A1) cite.
- Game theory (91A): the solution concept and its existence theorem are MA (C4, W1); equilibrium as allocation is economics (EC.O.A2); choosing or changing the game against an adaptive opponent is strategy (ST).
- History of mathematics (01) and mathematics education (97) are bridge C5: mathematics as the OBJECT of another pyramid's claim. Dated claims about mathematicians are owned by history (HI); claims about learning under an educational arrangement are owned by education (ED.B.C1); the general mechanism of learning is MS.O.A1.5. (Owner pointer amended in Phase 2.1; no MA cell or number changed.) 00 is a catalogue class (collections, general), not a cell.
- "Bridges" in the K-document (Langlands, algebraic topology, index theory, topos theory, HoTT) are renamed CORRESPONDENCES: registry edges that state two cells are linked by a theorem or programme. They are not communities and not cells. Status (proved / programme) is recorded on the edge.

## Side A — Objects (Face O), in dependency order
Key line: inductive · plural noun mathematical objects · dimension the dominant structure the theorem is about · order dependency (each presupposes the earlier).

### MA.O.A1 Foundations — what a proof may assume (03, 18)
- A1.1 Logic: consequence, proof, model, computability (03B, 03C, 03D, 03F, 03G, 03H). Gödel's first incompleteness theorem: a consistent, effectively axiomatised theory interpreting elementary arithmetic has a sentence it neither proves nor refutes. Model theory: compactness, Löwenheim–Skolem. Computability: halting problem undecidable; Church–Turing thesis (a thesis, not a theorem).
- A1.2 Sets and types: ZFC as default ground; choice, large cardinals, forcing and independence (CH independent of ZFC, Gödel 1940, Cohen 1963); type theory (03B38); homotopy type theory as a programme (no dedicated MSC code).
- A1.3 Categories: category, functor, natural transformation (Eilenberg–Mac Lane 1945); adjunctions; homological algebra (18G); higher categories (18N). Topos as a correspondence to logic and geometry.
Warrant: W1 relative to a stated metatheory. Defeaters: an unstated axiom; an independence result.

### MA.O.A2 Structure — operations, order and number (05, 06, 08, 11, 12, 13, 15, 16, 17, 19, 20, 22)
- A2.1 Order and universal algebra (06, 08).
- A2.2 Groups and symmetry (20, 22). Classification of finite simple groups; Lie groups (22 flagged: algebra plus topology).
- A2.3 Rings, fields and algebras (12, 13, 16, 17). Galois theory; Noetherian rings; Lie algebras.
- A2.4 Linear algebra and K-theory (15, 19). Spectral theorem for normal matrices; Jordan form over algebraically closed fields.
- A2.5 Number and counting (11, 05). Fundamental theorem of arithmetic; prime number theorem; quadratic reciprocity; Fermat's Last Theorem (Wiles 1995, with Taylor–Wiles); enumerative, extremal and algebraic combinatorics; Ramsey's theorem.
Warrant: W1. Defeaters: counterexample; gap in a long proof (classification of finite simple groups is the standard case of a distributed proof).

### MA.O.A3 Space — shape, nearness and dimension (14, 51, 52, 53, 54, 55, 57, 58)
- A3.1 Algebraic geometry (14): varieties and schemes.
- A3.2 Classical, convex and discrete geometry (51, 52): Euclid's postulates; projective geometry; Helly's theorem.
- A3.3 Differential geometry and global analysis (53, 58): curvature; Gauss–Bonnet; Ricci flow (53E); Atiyah–Singer index theorem as a correspondence to A4 and A2.
- A3.4 Topology (54, 55, 57): continuity without distance; homotopy and homology; Poincaré conjecture (Perelman 2003).
Warrant: W1.

### MA.O.A4 Change and the continuum — limits, functions, equations (26–49 analysis classes, 19 in all)
- A4.1 Function theory and measure (26, 28, 30, 31, 32, 33, 40): real and complex functions, Lebesgue measure and integral, special functions.
- A4.2 Equations of change (34, 35, 37, 39, 45): ODE existence and uniqueness (Picard–Lindelöf, under a Lipschitz condition); PDE; dynamical systems and ergodic theory (37, a high-disagreement class).
- A4.3 Approximation and harmonic analysis (41, 42, 43, 44): Fourier series and transforms; wavelets.
- A4.4 Functional analysis and operators (46, 47): Banach and Hilbert spaces; spectral theory.
- A4.5 Extremal problems (49): calculus of variations, optimal control. Flag: optimisation overlaps 90 (bridge C4).
Warrant: W1. Defeaters: a hidden regularity assumption.

### MA.O.A5 Chance — measures of total mass one (60, 62)
- A5.1 Probability and stochastic processes (60): Kolmogorov axioms (1933); laws of large numbers; central limit theorem (finite variance); martingales; Brownian motion; rough analysis (60L).
- A5.2 Mathematical statistics (62, theorem side): consistency and efficiency of estimators under stated models; Neyman–Pearson lemma; Bayes' theorem as a probability identity.
Warrant: W1. The procedure applied to data is B4.

## Side B — Practices (Face M)
Key line: inductive · plural noun roles · dimension what the practice does to a claim · order structural. Heuristics register sits outside the count.
| Role | Shared role | What it does | Warrant it produces |
|---|---|---|---|
| B1 Define and axiomatise | M1 Represent | States terms and assumptions, nothing smuggled | W12 (a stipulation; fruitfulness is judged later) |
| B2 Prove | M2 Derive | Deduction, induction, contradiction, construction, computer-assisted proof | W1; formal verification (Lean, Coq, Isabelle) adds W11 |
| B3 Compute | M5 Compute | Algorithms returning a mathematical object; numerical analysis with error bounds; symbolic computation | W2 |
| B4 Infer from data | M3 Observe | Estimation, testing, Bayesian updating, model checking | W4 under the model's assumptions; causal claims owe W5 (economics) |
| B5 Model | M1 Represent | Writes another field's claim as one of these objects | Internal consequences W1; fit to the world owes the owner's warrant (W3/W4) |
Heuristics register (MA.M.H): try small cases; look for an invariant; draw a picture; work backwards; dimensional check; Pólya's "solve a simpler problem". Useful; never a proof.

## Side C — MSC classes as bridges (Face B)
Key line: inductive · plural noun bridges · dimension the object × role pairing the community takes as home · order dependency, matching Side A.
| Bridge | Pairing | MSC classes | Count |
|---|---|---|---|
| C1 Pure mathematics | A1–A4 × B1–B2 | 03, 05, 06, 08, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 26, 28, 30, 31, 32, 33, 34, 35, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 51, 52, 53, 54, 55, 57, 58 | 41 |
| C2 Probability and statistics | A5 × B2, B4 | 60, 62 | 2 |
| C3 Computational mathematics | any × B3 | 65, 68 | 2 |
| C4 Mathematical modelling | outside claim × B5 | physical: 70, 74, 76, 78, 80, 81, 82, 83 · cosmos and earth: 85, 86 · decision and control: 90, 91, 93 · life: 92 · information: 94 | 15 |
| C5 Mathematics as an object of another pyramid | HI, ED, catalogue | 00, 01, 97 | 3 |
Total 63. Cell homes for C1: A1 = 03, 18; A2 = 05, 06, 08, 11, 12, 13, 15, 16, 17, 19, 20, 22; A3 = 14, 51, 52, 53, 54, 55, 57, 58; A4 = the 19 analysis classes.

## Correspondences (registry edges, not cells)
| Edge | Cells linked | Status |
|---|---|---|
| Langlands programme | A2.5 ↔ A2.2 ↔ A4.3 (43) ↔ A3.1 | Mostly conjectural; geometric Langlands claimed proved (Gaitsgory, Raskin et al., 2024, five papers) |
| Modularity theorem | 11G ↔ 11F | Proved (Wiles 1995; Breuil–Conrad–Diamond–Taylor 2001 for all elliptic curves over Q) |
| Algebraic topology | A3.4 ↔ A2 | Established |
| Arithmetic geometry | 11G ↔ 14G | Established |
| Analytic number theory | A2.5 ↔ A4.1 ↔ A4.3 | Established; Riemann hypothesis open |
| Index theory | A3.3 ↔ A4.2 ↔ A2.4 | Proved (Atiyah–Singer 1963) |
| Topos theory | A1.1 ↔ A1.3 ↔ A3 | Active programme |
| Homotopy type theory | A1.2 ↔ A3.4 ↔ A1.3 | Programme |
| Measure-theoretic probability | A5 ↔ A4.1 | Established |
| Computation ↔ everything | B3 ↔ all | Practice, not a theorem |

## What changed from v1
| Issue | v1 (K-doc) | v1 (twelve) | v2 |
|---|---|---|---|
| Primary partition | Role in dependency chain | Object + method | Object + method; dependency kept as order |
| Probability | Applied (K3.1) | Core object A4 | Object A5 |
| Statistics | Applied | Split A4/B | Theorem A5; procedure B4; one MSC home C2 |
| Category theory | Foundations | Absent | A1.3, flagged |
| History, education | Reflective layer K4 | Absent | Bridge C5, owned by HI and ED |
| MSC mapping | All 63 | None | All 63 |
| "Bridges" | Cross-links | Ownership lines | Renamed correspondences |
| Gödel | Correct | Missing "effectively axiomatised" | Fixed |

## Validation
- Counts: Side A 5, Side B 5 (+ register), Side C 5. Sub-groups: A1 3, A2 5, A3 4, A4 5, A5 2. C4 split into 5. All within 2–5.
- MSC: 63/63, each once (script check). Contested: 18, 22, 58, 37, 60, 62, 49/90, 68.
- Open items: verify every named theorem's hypotheses against a standard text (R5); expert review by a logician, an algebraist, an analyst, a probabilist.
