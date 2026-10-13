# MA — top-down Minto pyramid

Built by scripts/minto_pass.py from the grouped classification. Three rules (Minto pp. 9-11): each summary states the idea of its group, members are the same kind of idea, and they are in a stated order.

## Introduction

**Situation.** Mathematics is catalogued by several overlapping schemes that mix subject matter with containers and applications.

**Complication.** The schemes duplicate topics and include generic headings, so no single list shows how the field actually divides.

**Question.** How is everything in mathematics divided?

**Answer.** Mathematics is divided by the kind of question it asks, into algebraic and discrete structure, space and shape, change and the continuum, foundations and the discipline as a human activity, and the modelling of claims from other fields, in that order.

## Governing thought

Mathematics is divided by the kind of question it asks, into algebraic and discrete structure, space and shape, change and the continuum, foundations and the discipline as a human activity, and the modelling of claims from other fields, in that order.

## Key line

Group of kinds of question. Basis: kinds. Dimension: kind of question a topic addresses. Order: structure. The pillars run from pure structure through space and change to foundations and finally to mathematics serving other fields.

1. Structure is the kind of question about operations, order, counting and number, and its topics study algebraic and discrete systems. `MA.K1`
2. Space is the kind of question about shape, position and symmetry, and its topics study topology, geometry and groups. `MA.K2`
3. Change and the continuum is the kind of question about limits, variation and functions, and its topics study analysis and the equations of change. `MA.K3`
4. Foundations and the discipline is the kind of question about what mathematics rests on and how it is practised as a human activity, covering logic, history and teaching. `MA.K4`
5. Modelling other fields is the kind of question about how mathematics expresses and computes claims from physics, decision science, biology, data and computing. `MA.K5`

## Groups

### 1. Structure is the kind of question about operations, order, counting and number, and its topics study algebraic and discrete systems.

- **Algebraic systems study sets with operations such as fields, rings and algebras.**
  _basis: kinds, order: structure. From the most general systems to specific ring types._
  - General algebraic systems
  - Field theory and polynomials
  - Commutative algebra
  - Associative rings and algebras
  - Nonassociative rings and algebras
- **Discrete structure studies counting, order and the properties of whole numbers.**
  _basis: kinds, order: structure. From counting to order to numbers._
  - Combinatorics
  - Order, lattices, ordered algebraic structures
  - Number theory
- **Linear and unifying structure studies matrices and the abstract languages of categories and K-theory that relate algebraic systems.**
  _basis: kinds, order: structure. From concrete matrices to abstract unifying theories._
  - Linear and multilinear algebra; matrix theory
  - \(K\)-theory
  - Category theory; homological algebra

### 2. Space is the kind of question about shape, position and symmetry, and its topics study topology, geometry and groups.

- **Topology and manifolds study qualitative properties of space that survive continuous deformation.**
  _basis: kinds, order: structure. From general to algebraic and manifold topology._
  - General topology
  - Algebraic topology
  - Manifolds and cell complexes
- **Geometry studies measured, convex and algebraic shape in its classical and modern forms.**
  _basis: kinds, order: structure. From classical geometry to algebraic geometry._
  - Geometry
  - Convex and discrete geometry
  - Differential geometry
  - Algebraic geometry
- **Symmetry studies the groups, including topological and Lie groups, that describe the symmetries of spaces.**
  _basis: kinds, order: structure. From abstract groups to continuous groups._
  - Group theory and generalizations
  - Topological groups, Lie groups

### 3. Change and the continuum is the kind of question about limits, variation and functions, and its topics study analysis and the equations of change.

- **Real and classical analysis studies functions, measure, series and approximation on the real line.**
  _basis: kinds, order: structure. From functions to measure and series._
  - Real functions
  - Measure and integration
  - Sequences, series, summability
  - Approximations and expansions
- **Complex analysis studies functions of complex variables together with potentials and special functions.**
  _basis: kinds, order: structure. From one complex variable to several and special functions._
  - Functions of a complex variable
  - Potential theory
  - Several complex variables and analytic spaces
  - Special functions
- **Harmonic analysis and transforms study the decomposition of functions into oscillating components and the transforms that achieve it.**
  _basis: kinds, order: structure. From Euclidean to abstract harmonic analysis to transforms._
  - Harmonic analysis on Euclidean spaces
  - Integral transforms, operational calculus
- **Equations and dynamics study how quantities evolve, through differential, difference and integral equations and dynamical systems.**
  _basis: kinds, order: structure. From ordinary to partial equations and dynamics._
  - Ordinary differential equations
  - Partial differential equations
  - Dynamical systems and ergodic theory
  - Difference and functional equations
  - Integral equations
- **Abstract analysis and optimisation study infinite-dimensional spaces, operators and extremal problems.**
  _basis: kinds, order: structure. From spaces to operators to optimisation._
  - Functional analysis
  - Operator theory
  - Calculus of variations and optimal control; optimization

### 4. Foundations and the discipline is the kind of question about what mathematics rests on and how it is practised as a human activity, covering logic, history and teaching.

- Mathematical logic and foundations
- History and biography
- Mathematics education

### 5. Modelling other fields is the kind of question about how mathematics expresses and computes claims from physics, decision science, biology, data and computing.

- **Physical modelling expresses claims about matter, fields and the cosmos in mathematical form.**
  _basis: kinds, order: structure. From mechanics through fields and quanta to cosmic scales._
  - Mathematical physics
  - Mechanics of particles and systems
  - Mechanics of deformable solids
  - Fluid mechanics
  - Optics, electromagnetic theory
- **Thermal, quantum and cosmic modelling expresses claims about heat, microscopic matter, gravity, stars and the earth.**
  _basis: kinds, order: structure. From heat to the earth and sky._
  - Classical thermodynamics, heat transfer
  - Quantum theory
  - Statistical mechanics, structure of matter
  - Relativity and gravitational theory
  - Astronomy and astrophysics
- **Decision and living-systems modelling uses mathematics for choices, economies, biology and the earth.**
  _basis: kinds, order: structure. From the earth to decisions to living systems._
  - Operations research, mathematical programming
  - Game theory, economics, finance, and other social and behavioral sciences
  - Biology and other natural sciences
- **Information and chance modelling uses mathematics for control, communication and random processes.**
  _basis: kinds, order: structure. From control to information to chance._
  - Systems theory; control
  - Information and communication theory, circuits
  - Probability theory and stochastic processes
- **Computation applies mathematics to calculating answers and to the theory of computing.**
  _basis: kinds, order: structure. From general applied methods to numerical and computing._
  - Applied mathematics
  - Numerical analysis
  - Computer science

## Routed to other fields

- Global analysis, analysis on manifolds
- Abstract harmonic analysis
- Geophysics

## Checks

- minto_check: clean
- field_check holds: True — Misplaced: P5.5.1 applied mathematics (generic), P5.5.2 numerical analysis (fits P3), P2.3.1 group theory (fits P1 structure).
