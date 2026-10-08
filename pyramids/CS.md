# CS — Computer science

Standard v2 cited, not copied. Diagnosis: audit_engineering_cs.md. v1 source: twelve.txt 2608–3008. Theorems are owned by MA; complexity theory is MA bridge C3 (MSC 68Q), and CS cites it.

## 1. SCQA
**Situation.** Computer science makes and studies computations: procedures, programs, machines and the systems built from them.
**Complication.** v1 divided by layer of the stack and by community. That gave complexity theorems two homes (MA and CS), wrongly called FLP open, and counted heuristics as a sixth method.
**Question.** By what single dimension can every claim about a computation be placed once, with the theorems left in MA?
**Answer.** By the property the claim asserts of a computation: that it is correct, what it costs, how it coordinates, what it learns, or what it protects.

## 2. Governing thought
Computer science is exhausted by four faces of one pyramid: objects, methods, warrants and bridges.
Its objects divide into five properties of a computation: correctness, cost, coordination, learning, and protection.

## 3. Key line
Dimension: **the property asserted of a computation.** Order: structural, from the single program outward to many agents and adversaries.
1. Correctness
2. Cost
3. Coordination
4. Learning
5. Protection

## 4. Face O — Objects

### CS.O.A1 Correctness
**SCQA.** A computation is first judged by whether it does what it is specified to do. Specifications, semantics and proof tools exist, but most software is never proved. What can be claimed about correctness, and how? Key line: semantics, specification and verification, types, testing.
- CS.O.A1.1 Semantics of languages — operational, denotational and axiomatic semantics. Lambda calculus and Turing machines are equivalent in power (the theorem is MA.O.A1).
- CS.O.A1.2 Specification and verification — Hoare logic proves partial correctness; total correctness also needs termination. Model checking decides temporal properties of finite-state models.
- CS.O.A1.3 Types — well-typed programs do not go wrong (progress and preservation), for languages whose type system is proved sound.
- CS.O.A1.4 Testing — testing can show the presence of bugs, never their absence (Dijkstra), for any input space too large to exhaust.
- CS.O.A1.5 Limits of correctness — Rice's theorem: every non-trivial semantic property of programs is undecidable, for Turing-complete languages. Uses MA.O.A1.

### CS.O.A2 Cost
**SCQA.** A correct computation may still be too slow, too large or too costly in energy. Which costs can be bounded, and by what? Key line: algorithms, data structures, complexity, machines.
- CS.O.A2.1 Algorithms — each algorithm has a stated cost on a stated model. Comparison sorting needs Ω(n log n) comparisons in the worst case (a decision-tree lower bound, uses MA.B.C3).
- CS.O.A2.2 Data structures — amortised costs, e.g. union–find with path compression and union by rank runs in O(α(n)) per operation.
- CS.O.A2.3 Complexity classes — P, NP, PSPACE. Whether P = NP is OPEN and owned by MA.B.C3; CS uses it.
- CS.O.A2.4 Machines and architecture — memory hierarchy, pipelines, parallel speed-up. Amdahl's law bounds speed-up by 1/((1−p) + p/s) for a fixed workload whose fraction p is parallelisable by a factor s.
- CS.O.A2.5 Physical limits of hardware — Moore's law is an empirical trend, now slowing; it is not a law. Transistor physics is PH.

### CS.O.A3 Coordination
**SCQA.** Many computations run at once, share state and communicate over unreliable links. What can and cannot be coordinated? Key line: concurrency, distributed agreement, networks, data systems.
- CS.O.A3.1 Concurrency — races, deadlock, linearisability.
- CS.O.A3.2 Distributed agreement — FLP (Fischer, Lynch and Paterson, 1985): no deterministic protocol guarantees consensus in an asynchronous system if even one process may crash. This is a proved theorem, not an open problem. Byzantine agreement needs n ≥ 3f + 1 processes to tolerate f faulty ones, with synchronous oral messages and no signatures.
- CS.O.A3.3 Consistency under partition — CAP (Gilbert and Lynch, 2002 proof): during a network partition, a system cannot provide both linearisable consistency and availability.
- CS.O.A3.4 Networks — protocols, routing, congestion control.
- CS.O.A3.5 Data systems — databases, transactions (ACID), query optimisation. Information retrieval as a claim about records is IS.

### CS.O.A4 Learning
**SCQA.** Some computations improve from data instead of from a programmer's rules. What can such systems learn, and how well? Key line: learning theory, models and training, reasoning and planning, perception and language.
- CS.O.A4.1 Learning theory — a binary concept class is PAC-learnable if and only if its VC dimension is finite (uses MA.O.A5). No-free-lunch: averaged uniformly over all objective functions, every optimiser performs equally.
- CS.O.A4.2 Models and training — neural networks; universal approximation holds for one-hidden-layer networks with a non-polynomial activation, approximating continuous functions on compact sets to any accuracy. It says nothing about learnability. Empirical scaling laws are W4 claims within stated ranges.
- CS.O.A4.3 Reasoning and planning — search, logic programming, planning. Many planning problems are PSPACE-complete (uses MA.B.C3).
- CS.O.A4.4 Perception and language processing — vision, speech, NLP. Claims about language itself are LN.
- CS.O.A4.5 Alignment and evaluation of AI systems — whether a trained system pursues its intended objective. Methods are immature; much is OPEN.

### CS.O.A5 Protection
**SCQA.** Computations run among adversaries. What can be protected, from whom, and on what assumptions? Key line: cryptography in use, security of systems, privacy.
- CS.O.A5.1 Cryptography in use — protocols are secure relative to stated hardness assumptions (e.g. factoring). Security proofs are MA; the deployed protocol is CS.
- CS.O.A5.2 Systems security — access control, memory safety, attack surfaces.
- CS.O.A5.3 Privacy — differential privacy bounds how much one record changes an output distribution, by a stated ε.
- CS.O.A5.4 Quantum threats — Shor's algorithm factors in polynomial time on a fault-tolerant quantum computer. Uses MA.B.C3 and PH.O.A2.

## 5. Face M — Methods

| ID | Role | Shared role | Example |
|---|---|---|---|
| CS.M.1 | Formalise | M1 Represent | specify, define a model of computation |
| CS.M.2 | Prove | M2 Derive | correctness or bound proof |
| CS.M.3 | Build | M4 Intervene | implement a system |
| CS.M.4 | Run and measure | M5 Compute | benchmark, simulation, training run |
| CS.M.5 | Verify | M7 Verify | model checking, test suite, audit |

Five roles. M3 Observe and M6 Compare appear only inside CS.M.4 (empirical evaluation) and are not separate roles.

### Heuristics register (outside the count)
Premature optimisation is the root of all evil; worse is better; end-to-end argument; design patterns; "make it work, make it right, make it fast"; ablation as a habit.

## 6. Face W — Warrants

| Cell | Warrant | Standard of acceptance | Typical defeaters |
|---|---|---|---|
| CS.O.A1 | W1 + W11 | machine-checked proof, or verification against a formal specification | specification wrong, unsound tool, unmodelled environment |
| CS.O.A2 | W1 + W2 | proof of bound on a stated model; benchmark with stated variance | model mismatch with hardware, unrepresentative input |
| CS.O.A3 | W1 + W4 | impossibility or protocol proof; measured behaviour in deployment | failure model differs from assumed one |
| CS.O.A4 | W4 + W2 | held-out evaluation, stated metric and variance, replication | data leakage, benchmark overfitting, distribution shift |
| CS.O.A5 | W1 + W11 | reduction to a stated assumption; penetration test | broken assumption, side channel, implementation flaw |

## 7. Face B — Bridges

| ID | Field | Cells | Methods | Substrate |
|---|---|---|---|---|
| CS.B.C1 | Theory of computation | A1.5, A2.3 | M.1, M.2 | models (cites MA.B.C3) |
| CS.B.C2 | Programming languages | A1 | M.1, M.2, M.5 | languages |
| CS.B.C3 | Computer architecture | A2.4, A2.5 | M.3, M.4 | hardware (uses PH) |
| CS.B.C4 | Operating and distributed systems | A3 | M.3, M.4 | machines |
| CS.B.C5 | Databases | A3.5 | M.3, M.4 | data |
| CS.B.C6 | Artificial intelligence and machine learning | A4 | M.3, M.4 | data and models |
| CS.B.C7 | Security and privacy | A5 | all | systems |
| CS.B.C8 | Human–computer interaction | A1, A4 | M.3, M.4 | interfaces (user claims MS) |
| CS.B.C9 | Computational science | A2 | M.4 | other pyramids' models |

## 8. Assignment rules
1. Place by the property claimed: correctness, cost, coordination, learning or protection.
2. A theorem is MA, even when computer scientists prove it. Complexity theorems sit in MA.B.C3; CS cites "uses MA.B.C3".
3. A program delivered to a customer's specification is EN (EN.B.C5); whether the program is correct is CS.
4. A claim about users' minds is MS; the interface's measured effect is CS.B.C8.
5. A claim about the record, the catalogue or retrieval as such is IS; the algorithm's cost is CS.
6. A claim about language is LN; a system that processes it is CS.O.A4.4.
7. The legal duty on data is LA; the technical privacy guarantee is CS.O.A5.3.
8. A claim mixing two properties goes to the one its warrant establishes.

## 9. Scope boundary

| Refused | Owner |
|---|---|
| computability and complexity theorems | MA.O.A1, MA.B.C3 |
| device physics | PH.O.A4 |
| software delivery to contract | EN |
| users' cognition | MS |
| the record and its retrieval as information | IS |
| data protection law | LA |
| ethics of AI as argument | PL |

## 10. External crosswalk
**ACM CCS 2012** has 13 top-level classes. They land as follows:
- General and reference → refused, not a claim class
- Hardware → A2.4, A2.5, B.C3
- Computer systems organisation → A2.4, A3
- Networks → A3.4
- Software and its engineering → A1, EN.B.C5
- Theory of computation → A1.5, A2.3 (cites MA.B.C3)
- Mathematics of computing → refused to MA
- Information systems → A3.5, IS
- Security and privacy → A5
- Human-centred computing → B.C8
- Computing methodologies → A4
- Applied computing → refused, a catalogue
- Social and professional topics → refused to PL, LA, BU

Coverage: 9 of 13 land.

**CS2023** has 17 knowledge areas (checked: csed.acm.org/knowledge-areas):
- AL → A2.1–A2.2
- AR → A2.4
- AI → A4
- DM → A3.5
- FPL → A1.1–A1.3
- GIT → A4.4 (graphics as CS.B.C9)
- HCI → B.C8
- MSF → refused to MA
- NC → A3.4
- OS → A3
- PDC → A3.1–A3.3
- SEC → A5
- SEP → refused to PL and LA
- SDF → A1
- SE → A1.4 and EN.B.C5
- SPD → refused, a catalogue of platforms
- SF → A2.4

Coverage: 14 of 17 land; 3 are refused.

**ANZSRC 46** (checked 9 Oct 2026 against the ABS file anzsrc2020_for.xlsx) has 14 groups. 4601 Applied computing → catalogue. 4602 AI, 4603 Computer vision, 4611 Machine learning → A4. 4604 Cybersecurity → A5. 4605 Data management → A3.5 (records side is IS). 4606 Distributed computing → A3. 4607 Graphics → B.C9. 4608 Human-centred → B.C8. 4609 Information systems → A3.5 and IS. 4610 Library and information studies → IS. 4612 Software engineering → A1 and EN. 4613 Theory of computation → A1.5, A2.3. 4699 Other → not a cell. Coverage: 11 of 13 substantive groups land in CS; 4610 goes to IS; 4601 is refused.

## 11. Validation
Sizes: key line 5. Face O 5 cells + 24 sub-cells = 29. M roles 5. Heuristics 6, outside the count. W rows 5. B bridges 9.
Key line, word for word: Correctness. Cost. Coordination. Learning. Protection.
OPEN: P vs NP (owned by MA.B.C3, cited); AI alignment methods (A4.5).
CONTESTED: software engineering in EN vs CS (alternative: CS.O.A1); HCI as a CS bridge vs an MS cell.
Fixed from the audit: FLP is now stated as proved (1985), with its hypotheses. Heuristics are moved out of the role count.

## 12. Registry rows

| ID | Label | Home | Uses |
|---|---|---|---|
| CS.O.A1 | Correctness | O/A1 | — |
| CS.O.A1.1 | Semantics | O/A1 | MA.O.A1 |
| CS.O.A1.2 | Specification and verification | O/A1 | MA.O.A1 |
| CS.O.A1.3 | Types | O/A1 | — |
| CS.O.A1.4 | Testing | O/A1 | — |
| CS.O.A1.5 | Limits of correctness (Rice) | O/A1 | MA.O.A1 |
| CS.O.A2 | Cost | O/A2 | — |
| CS.O.A2.1 | Algorithms | O/A2 | MA.B.C3 |
| CS.O.A2.2 | Data structures | O/A2 | — |
| CS.O.A2.3 | Complexity classes | O/A2 | MA.B.C3 |
| CS.O.A2.4 | Machines and architecture | O/A2 | — |
| CS.O.A2.5 | Physical limits of hardware | O/A2 | PH.O.A4 |
| CS.O.A3 | Coordination | O/A3 | — |
| CS.O.A3.1 | Concurrency | O/A3 | — |
| CS.O.A3.2 | Distributed agreement (FLP, Byzantine) | O/A3 | MA.B.C3 |
| CS.O.A3.3 | Consistency under partition (CAP) | O/A3 | — |
| CS.O.A3.4 | Networks | O/A3 | — |
| CS.O.A3.5 | Data systems | O/A3 | IS.O.A4 |
| CS.O.A4 | Learning | O/A4 | — |
| CS.O.A4.1 | Learning theory | O/A4 | MA.O.A5 |
| CS.O.A4.2 | Models and training | O/A4 | MA.O.A4 |
| CS.O.A4.3 | Reasoning and planning | O/A4 | MA.B.C3 |
| CS.O.A4.4 | Perception and language processing | O/A4 | LN.O.A1 |
| CS.O.A4.5 | Alignment and evaluation | O/A4 | — |
| CS.O.A5 | Protection | O/A5 | — |
| CS.O.A5.1 | Cryptography in use | O/A5 | MA.O.A2, MA.B.C3 |
| CS.O.A5.2 | Systems security | O/A5 | — |
| CS.O.A5.3 | Privacy | O/A5 | MA.O.A5 |
| CS.O.A5.4 | Quantum threats | O/A5 | PH.O.A2, MA.B.C3 |
| CS.M.1–5 | Method roles | M | — |
| CS.B.C1–C9 | Bridges | B | as tabled |

## 13. Self-check against R1–R12

| Rule | Result | If FAIL: sentence and repair |
|---|---|---|
| R1 | PASS | Complexity theorems cited to MA.B.C3. |
| R2 | PASS | Counts in section 11 match sections 3–7. |
| R3 | PASS | Heuristics are outside the five roles. |
| R4 | PASS | ACM CCS 9 of 13; CS2023 14 of 17 (checked); ANZSRC 46 checked. |
| R5 | PASS | FLP, Byzantine, CAP, Amdahl, PAC, universal approximation, Rice and Hoare are each stated with hypotheses. |
| R6 | PASS | Two OPEN, two CONTESTED. |
| R7 | PASS | Members are identical in sections 2, 3 and 11. |
| R8 | PASS | Section 9. |
| R9 | PASS | A1–A5 each have SCQA, key line and objects. |
| R10 | PASS | Plain register. |
| R11 | FAIL (partial) | Dates for FLP (1985) and the CAP proof (2002) are from memory. Repair: cite the original papers. |
| R12 | PASS | IDs are stable. |
