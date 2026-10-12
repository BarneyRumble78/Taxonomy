# MA — top-down Minto pyramid

Built by scripts/minto_pass.py from the grouped classification. Three rules (Minto pp. 9-11): each summary states the idea of its group, members are the same kind of idea, and they are in a stated order.

## Introduction

**Situation.** Mathematics spans abstract objects, the continuum, chance and uses in other sciences.

**Complication.** Published schemes mix subject areas, applications and container headings, so the topics overlap and repeat.

**Question.** How is everything in mathematics divided?

**Answer.** Mathematics is divided by the role a claim plays, into foundations and the discipline itself, algebraic and combinatorial structure, space and shape, change and chance, and the modelling and computing of claims from other fields, in that order.

## Governing thought

Mathematics is divided by the role a claim plays, into foundations and the discipline itself, algebraic and combinatorial structure, space and shape, change and chance, and the modelling and computing of claims from other fields, in that order.

## Key line

Group of roles. Basis: parts. Dimension: role the claim plays in mathematics (foundation, structure, space, change and chance, or modelling). Order: structure. The pillars run from what underlies all mathematics, through its internal objects, to its use outside itself.

1. Foundations and the discipline is the role of mathematics as the ground of proof and as a human activity with a history and a teaching practice. `MA.K1`
2. Structure is the role of mathematics as the study of algebraic, ordered and discrete objects defined by operations and relations. `MA.K2`
3. Space is the role of mathematics as the study of shape, position and continuity of spaces and the groups that act on them. `MA.K3`
4. Change and chance is the role of mathematics as the study of the continuum, of change through equations, and of random variation. `MA.K4`
5. Modelling and computing is the role of mathematics as a language for claims from other fields and as a means of computing answers. `MA.K5`

## Groups

### 1. Foundations and the discipline is the role of mathematics as the ground of proof and as a human activity with a history and a teaching practice.

- **Logic and category theory supply the formal ground on which every proof and structure rests.**
  _basis: parts, order: structure. Logic precedes the general language of categories._
  - Mathematical logic and foundations
  - Category theory; homological algebra
- **History and education treat mathematics as a human activity that is recorded and taught.**
  _basis: parts, order: structure. The past of the subject precedes its teaching._
  - History and biography
  - Mathematics education

### 2. Structure is the role of mathematics as the study of algebraic, ordered and discrete objects defined by operations and relations.

- **Algebraic systems study sets with operations such as groups, rings, fields and algebras.**
  _basis: parts, order: structure. General systems precede specific kinds of algebra._
  - General algebraic systems
  - Group theory and generalizations
  - Field theory and polynomials
  - Commutative algebra
- **Rings and linear structures study algebras, matrices and the algebraic invariants built from them.**
  _basis: parts, order: structure. Rings come before linear algebra and its invariants._
  - Associative rings and algebras
  - Nonassociative rings and algebras
  - Linear and multilinear algebra; matrix theory
  - \(K\)-theory
- **Discrete structure studies counting, order and the integers.**
  _basis: parts, order: structure. Counting precedes order and number._
  - Combinatorics
  - Order, lattices, ordered algebraic structures
  - Number theory

### 3. Space is the role of mathematics as the study of shape, position and continuity of spaces and the groups that act on them.

- **Topology studies the continuity and global form of spaces and manifolds.**
  _basis: parts, order: structure. General topology precedes algebraic and manifold topology._
  - General topology
  - Algebraic topology
  - Manifolds and cell complexes
  - Global analysis, analysis on manifolds
- **Geometry studies metric, convex, differential and algebraic shape together with continuous symmetry.**
  _basis: parts, order: structure. Elementary geometry precedes differential and algebraic geometry._
  - Geometry
  - Convex and discrete geometry
  - Differential geometry
  - Algebraic geometry
  - Topological groups, Lie groups

### 4. Change and chance is the role of mathematics as the study of the continuum, of change through equations, and of random variation.

- **Real, complex and functional analysis study functions, limits and the continuum.**
  _basis: parts, order: structure. Real analysis precedes complex and functional analysis._
  - **Real analysis studies real functions, measure, series and approximation.**
    _basis: parts, order: structure. Functions precede measure and series._
    - Real functions
    - Measure and integration
    - Sequences, series, summability
    - Approximations and expansions
  - **Complex analysis studies functions of complex variables, potentials and special functions.**
    _basis: parts, order: structure. One variable precedes several variables._
    - Functions of a complex variable
    - Potential theory
    - Several complex variables and analytic spaces
    - Special functions
  - **Harmonic and functional analysis study transforms, function spaces and operators.**
    _basis: parts, order: structure. Transforms precede abstract operators._
    - Harmonic analysis on Euclidean spaces
    - Abstract harmonic analysis
    - Integral transforms, operational calculus
    - Functional analysis
    - Operator theory
- **Equations and dynamics describe how quantities change through differential, integral and difference laws.**
  _basis: parts, order: structure. Equations precede the long-run behaviour they generate._
  - Ordinary differential equations
  - Partial differential equations
  - Difference and functional equations
  - Integral equations
  - Dynamical systems and ergodic theory
- **Probability and statistics study random variation and inference from data.**
  _basis: parts, order: structure. Theory of chance precedes inference from data._
  - Probability theory and stochastic processes
  - Statistics

### 5. Modelling and computing is the role of mathematics as a language for claims from other fields and as a means of computing answers.

- **Physical modelling expresses the laws of matter, fields and the cosmos in mathematical form.**
  _basis: parts, order: structure. Mechanics precedes fields, quantum theory and the cosmos._
  - **Mechanics and thermal physics model bodies, fluids, heat and matter.**
    _basis: parts, order: structure. Bodies precede fluids and heat._
    - Mechanics of particles and systems
    - Mechanics of deformable solids
    - Fluid mechanics
    - Classical thermodynamics, heat transfer
    - Statistical mechanics, structure of matter
  - **Fields, quanta and the cosmos are modelled through electromagnetism, quantum theory, relativity and the earth and sky.**
    _basis: parts, order: structure. Fields precede quantum, relativistic and cosmic scales._
    - Optics, electromagnetic theory
    - Quantum theory
    - Relativity and gravitational theory
    - Astronomy and astrophysics
    - Mathematical physics
  - **Geophysics models the structure and processes of the earth.**
    _basis: parts, order: structure. Earth models follow the physics they apply._
    - Geophysics
    - Calculus of variations and optimal control; optimization
- **Decision, social and life-science modelling expresses choices, systems and living processes in mathematics.**
  _basis: parts, order: structure. Decision problems precede social, life and engineered systems._
  - Operations research, mathematical programming
  - Game theory, economics, finance, and other social and behavioral sciences
  - Biology and other natural sciences
  - Systems theory; control
  - Information and communication theory, circuits
- **Computation turns mathematical claims into algorithms that produce numerical answers.**
  _basis: parts, order: structure. Numerical methods precede general computer science._
  - Numerical analysis
  - Computer science

## Checks

- minto_check: clean
- field_check holds: False — Mixed dimension (role vs subject matter); optimization P5.1.3.2 sits under geophysics, homological algebra P1.1.2 under foundations, and rings P2.1/P2.2 overlap.
