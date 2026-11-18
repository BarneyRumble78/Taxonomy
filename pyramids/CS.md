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

**SCQA.** Situation. A computation is first judged by whether it does what it is specified to do. Complication. Specifications, semantics and proof tools exist, but most software is never proved, and the specification itself may be wrong. Question. What can be claimed about correctness, by what means, and where do such claims stop? Answer. CS owns the meaning of programs, the specification and its verification, type discipline, testing, and the limits on all four. The undecidability theorems behind those limits are owned by MA (uses MA.O.A1).

Key line (inductive; plural noun: correctness claims; dimension: the means by which agreement with intent is asserted; order: from meaning, through proof and types, to sampling, then to limits). Members (5): Semantics · Specification and verification · Types · Testing · Limits of correctness.

- CS.O.A1.1 Semantics of languages. **A program has a meaning that can be stated independently of any one implementation.** Operational, denotational and axiomatic semantics are three styles of stating it. Lambda calculus and Turing machines are equivalent in power (the theorem is MA.O.A1).
  - CS.O.A1.1.1 Operational semantics. A program's meaning can be given as a transition relation on configurations. Two implementations agree when they realise the same relation on observable steps.
  - CS.O.A1.1.2 Denotational semantics. A program's meaning can be given as a mathematical object, such as a continuous function on a domain. Recursion is then a least fixed point (the fixed-point theorem is MA.O.A2).
  - CS.O.A1.1.3 Adequacy. Operational and denotational accounts of one language agree on observable outcomes only when an adequacy result is proved for that language. Adequacy is a per-language claim, not a general one.
  - CS.O.A1.1.4 Church–Turing thesis. Every effectively calculable function is Turing-computable. It is a thesis about the informal notion, not a theorem. Its standing is CONTESTED between CS and PL (uses PL.O.A5).
- CS.O.A1.2 Specification and verification. **A program can be proved to meet a formal specification, given a sound logic and a correct specification.** Hoare logic proves partial correctness; total correctness also needs termination. Model checking decides temporal properties of finite-state models.
  - CS.O.A1.2.1 Hoare triples. A triple {P} C {Q} states that if P holds before C and C terminates, Q holds after. Loops need an invariant supplied by a person or a tool.
  - CS.O.A1.2.2 Termination. Total correctness needs a variant: a quantity in a well-founded order that each loop iteration decreases. No algorithm finds a variant for every terminating program (uses MA.O.A1).
  - CS.O.A1.2.3 Model checking. Temporal-logic properties of a finite-state model are decidable. Practical limits come from state-space explosion, which grows exponentially with the number of concurrent components.
  - CS.O.A1.2.4 Separation logic. Programs that share heap memory can be reasoned about locally when assertions describe disjoint heap regions. The frame rule carries a proof past code that touches other regions.
- CS.O.A1.3 Types. **Well-typed programs do not go wrong, for languages whose type system is proved sound.** Soundness is shown as progress and preservation.
  - CS.O.A1.3.1 Progress and preservation. A well-typed term is either a value or can take a step, and stepping keeps its type. Together these rule out stuck states under the stated semantics.
  - CS.O.A1.3.2 Type inference. For the Hindley–Milner fragment, every typable term has a principal type that an algorithm finds. Extensions such as higher-rank polymorphism lose decidable full inference.
  - CS.O.A1.3.3 Curry–Howard correspondence. Types correspond to propositions and terms to proofs, for stated pairs of type systems and logics. The correspondence itself is owned by MA (uses MA.O.A1); its use in proof assistants is CS.
- CS.O.A1.4 Testing. **Testing can show the presence of bugs, never their absence (Dijkstra), for any input space too large to exhaust.** It samples behaviour; it does not prove.
  - CS.O.A1.4.1 Coverage criteria. Statement, branch and path coverage measure how much of a program a test suite exercises. High coverage does not imply a low residual defect rate. The size of the gap is an empirical claim (W4).
  - CS.O.A1.4.2 Property-based testing. Random inputs drawn against a stated property find counterexamples a fixed suite misses. A pass is evidence of absence only within the input distribution used.
  - CS.O.A1.4.3 Mutation testing. A suite's strength can be estimated by the fraction of seeded faults it detects. The estimate assumes that seeded faults resemble real ones; that assumption is (UNVERIFIED) in general.
- CS.O.A1.5 Limits of correctness. **No general procedure decides any non-trivial semantic property of programs.** Rice's theorem holds for Turing-complete languages. Uses MA.O.A1.
  - CS.O.A1.5.1 Halting problem. No program decides, for every program and input, whether that program halts. The theorem is MA.O.A1; CS uses it as the root of verification limits.
  - CS.O.A1.5.2 Sound but incomplete analysis. Static analysers escape Rice's theorem by over-approximating: they may report false alarms but miss no error in the analysed class. Abstract interpretation is the general method.
  - CS.O.A1.5.3 Specification gap. A proof shows agreement with the specification, not with intent. Defects in the specification are outside what verification can catch.

Named objects: operational semantics, denotational semantics, lambda calculus, Church–Turing thesis, Hoare logic (hypotheses: sound rules, stated pre- and postconditions, partial correctness unless a variant is given), separation logic, model checking (hypothesis: a finite-state model), type soundness, Hindley–Milner inference, Curry–Howard correspondence, coverage, property-based testing, mutation testing (hypothesis: seeded faults represent real ones), Rice's theorem, halting problem, abstract interpretation (hypotheses: a lattice of abstract values and sound transfer functions).

### CS.O.A2 Cost

**SCQA.** Situation. A correct computation may still be too slow, too large or too costly in energy. Complication. Costs are stated on abstract models, but they are paid on real hardware with caches, pipelines and physical limits. Question. Which costs can be bounded, on which model, and how far do the bounds carry to machines? Answer. CS owns algorithms and data structures with their stated costs, the use of complexity classes, machine organisation, and the engineering limits of hardware. Complexity theorems are MA (uses MA.B.C3); device physics is PH.

Key line (inductive; plural noun: cost claims; dimension: what bears the cost; order: from the procedure, to its data, to the problem class, to the machine, to physics). Members (5): Algorithms · Data structures · Complexity classes · Machines and architecture · Physical limits of hardware.

- CS.O.A2.1 Algorithms. **Each algorithm has a stated cost on a stated model.** Comparison sorting needs Ω(n log n) comparisons in the worst case (a decision-tree lower bound, uses MA.B.C3).
  - CS.O.A2.1.1 Asymptotic cost. Big-O statements bound growth up to a constant factor and beyond some input size. They do not rank two algorithms at a given practical size.
  - CS.O.A2.1.2 Design paradigms. Divide and conquer, dynamic programming and greedy choice each apply when a stated structural property holds. Greedy choice is optimal only under a matroid-like exchange property.
  - CS.O.A2.1.3 Randomised algorithms. An algorithm with access to random bits may have lower expected cost or simpler structure. Its guarantee is a probability over its own coins, not over inputs (uses MA.O.A5).
  - CS.O.A2.1.4 Approximation. For some NP-hard optimisation problems, polynomial algorithms reach a stated ratio of the optimum. For others, no such ratio is reachable unless P = NP (uses MA.B.C3).
- CS.O.A2.2 Data structures. **A data structure trades the cost of one operation against another, and amortised analysis bounds the total over a sequence.** Union–find with path compression and union by rank runs in O(α(n)) amortised time per operation.
  - CS.O.A2.2.1 Amortised analysis. A sequence of m operations can cost less than m times the worst single operation. The potential method makes the bound exact for a stated sequence model.
  - CS.O.A2.2.2 Hashing. Hash tables give expected constant-time lookup under a uniform-hashing or universal-family assumption. Adversarial keys defeat a fixed hash function.
  - CS.O.A2.2.3 Balanced search trees. Red–black and AVL trees keep height O(log n), so search, insert and delete run in O(log n) worst-case time.
  - CS.O.A2.2.4 External memory. When data exceed fast memory, cost is better counted in block transfers than in operations. B-trees are designed for that model.
- CS.O.A2.3 Complexity classes. **Problems fall into classes by the resources a solving machine needs.** P, NP and PSPACE are the standard examples. Whether P = NP is OPEN and owned by MA.B.C3; CS uses it.
  - CS.O.A2.3.1 Reductions in practice. Showing a new problem NP-hard by reduction is evidence that no efficient exact algorithm is likely. CS uses this to redirect effort to heuristics or approximation.
  - CS.O.A2.3.2 Hardness assumptions as engineering inputs. Cryptography and fine-grained complexity rest on stated conjectures, such as the exponential-time hypothesis. Results built on them are conditional (uses MA.B.C3).
  - CS.O.A2.3.3 Parameterised complexity. Some NP-hard problems are fast when a stated parameter is small. Fixed-parameter tractability is a claim about that parameter, not about the problem in general.
- CS.O.A2.4 Machines and architecture. **Real cost depends on the memory hierarchy, pipelines and parallelism of the machine.** Amdahl's law bounds speed-up by 1/((1−p) + p/s) for a fixed workload whose fraction p is parallelisable by a factor s.
  - CS.O.A2.4.1 Locality. Programs that reuse nearby data run faster on cached machines. The gap between cache and main-memory latency is large enough to reverse asymptotic rankings at practical sizes.
  - CS.O.A2.4.2 Gustafson's law. When the problem grows with the processor count, scaled speed-up is (1−p) + p·N. It does not contradict Amdahl's law; it changes the fixed quantity.
  - CS.O.A2.4.3 Instruction-level parallelism. Pipelines and out-of-order execution overlap instructions. Data dependencies and branch mispredictions bound the achievable overlap.
  - CS.O.A2.4.4 Accelerators. Specialised hardware such as GPUs gives large speed-ups for regular, data-parallel work. Irregular control flow loses most of that gain.
- CS.O.A2.5 Physical limits of hardware. **Hardware cost is bounded by engineering trends that are not laws.** Moore's law is an empirical trend, now slowing. Transistor physics is PH.
  - CS.O.A2.5.1 End of Dennard scaling. Power density no longer stays constant as transistors shrink. Clock rates have therefore plateaued, and designers turned to many cores. Device causes are PH (uses PH.O.A4).
  - CS.O.A2.5.2 Landauer's bound. Erasing one bit dissipates at least kT ln 2 of energy. The principle is owned by PH (uses PH.O.A4); CS cites it as a floor far below current practice.
  - CS.O.A2.5.3 Energy as a cost measure. Energy per operation is now a first-class cost alongside time and space. Its measured values depend on the device and are W4 claims.

Named objects: asymptotic notation, decision-tree lower bound, dynamic programming, greedy algorithm (hypothesis: exchange property), randomised algorithm, approximation ratio, amortised analysis, universal hashing (hypothesis: keys independent of the chosen function), balanced search tree, B-tree, external-memory model, P, NP, PSPACE, exponential-time hypothesis, fixed-parameter tractability, Amdahl's law (hypotheses: fixed workload, fixed parallel fraction, no overhead), Gustafson's law (hypothesis: workload scales with processors), Moore's law (an empirical trend), Dennard scaling, Landauer's bound (uses PH.O.A4).

### CS.O.A3 Coordination

**SCQA.** Situation. Many computations run at once, share state and communicate over unreliable links. Complication. Failures, delays and partitions make many intuitive goals impossible, and v1 misreported FLP as open. Question. What can and cannot be coordinated, under which failure and timing models? Answer. CS owns concurrency, distributed agreement, consistency under partition, networks and data systems. Each claim must state its timing model and its failure model.

Key line (inductive; plural noun: coordination claims; dimension: the scope of the shared state; order: from one machine, to a group agreeing, to a partitioned system, to a network, to a database). Members (5): Concurrency · Distributed agreement · Consistency under partition · Networks · Data systems.

- CS.O.A3.1 Concurrency. **Concurrent programs are correct only relative to a stated correctness condition, such as linearisability or freedom from deadlock.** Races, deadlock and linearisability are the standard objects.
  - CS.O.A3.1.1 Coffman conditions. Deadlock requires mutual exclusion, hold and wait, no pre-emption and circular wait together. Breaking any one prevents it.
  - CS.O.A3.1.2 Linearisability. A concurrent object is linearisable when each operation appears to take effect at one instant between its call and return. Linearisability is composable across objects.
  - CS.O.A3.1.3 Memory models. Hardware and language memory models allow reorderings that sequential reasoning does not expect. Data-race-free programs observe sequential consistency under the models that promise it.
  - CS.O.A3.1.4 Wait-free hierarchy. Shared objects can be ranked by consensus number. Read–write registers alone cannot solve wait-free consensus for two processes (uses MA.B.C3).
- CS.O.A3.2 Distributed agreement. **Consensus is impossible or possible depending on the timing and failure model, and the boundary is proved.** FLP (Fischer, Lynch and Paterson, 1985): no deterministic protocol guarantees consensus in an asynchronous system if even one process may crash. This is a proved theorem, not an open problem. Byzantine agreement needs n ≥ 3f + 1 processes to tolerate f faulty ones, with synchronous oral messages and no signatures.
  - CS.O.A3.2.1 Partial synchrony. Consensus becomes solvable when message delays are eventually bounded, even if the bound is unknown. Practical protocols rely on this model.
  - CS.O.A3.2.2 Crash-fault consensus protocols. Paxos and Raft keep safety under asynchrony and give liveness under partial synchrony, with a majority of processes correct. Safety never depends on timing.
  - CS.O.A3.2.3 Randomised consensus. Allowing random choices sidesteps FLP: termination holds with probability one rather than deterministically.
  - CS.O.A3.2.4 Signed messages. With unforgeable signatures, synchronous Byzantine agreement tolerates any number of faulty processes for some problem variants. The bound n ≥ 3f + 1 applies to the unsigned case.
- CS.O.A3.3 Consistency under partition. **A replicated system must give up either linearisable consistency or availability while a partition lasts.** CAP (Gilbert and Lynch, 2002 proof) states this.
  - CS.O.A3.3.1 Scope of CAP. CAP constrains behaviour only during a partition. Its popular "pick two of three" reading misstates it.
  - CS.O.A3.3.2 Latency trade-off. Even without partitions, stronger consistency costs latency. This trade-off is an engineering claim with measured magnitudes (W4).
  - CS.O.A3.3.3 Convergent replicated data types. CRDTs reach the same state on all replicas once all updates are delivered, without coordination. They require operations that commute or merges that form a semilattice.
- CS.O.A3.4 Networks. **Network protocols deliver stated guarantees over links that lose, reorder and delay packets.** Protocols, routing and congestion control are the standard objects.
  - CS.O.A3.4.1 Layering. Protocol stacks separate concerns so that each layer offers a service to the one above. Cross-layer effects, such as loss read as congestion, are common defeaters.
  - CS.O.A3.4.2 End-to-end argument. A function that needs knowledge at the endpoints can be completely provided only there. Lower-layer versions are performance aids. Its reach is CONTESTED where networks carry security functions.
  - CS.O.A3.4.3 Congestion control. Additive-increase, multiplicative-decrease converges towards a fair, efficient share of a bottleneck under a stated feedback model.
  - CS.O.A3.4.4 Two Generals problem. Over a lossy link, no finite protocol guarantees that two parties both know they agree. Reliable delivery protocols therefore give probabilistic or eventual guarantees.
- CS.O.A3.5 Data systems. **A data system gives stated guarantees on stored records under concurrent access and failure.** Databases, transactions (ACID) and query optimisation are the standard objects. Information retrieval as a claim about records is IS.
  - CS.O.A3.5.1 Relational model. Data held as relations can be queried by relational algebra. Relational algebra and safe relational calculus have equal expressive power (uses MA.O.A1).
  - CS.O.A3.5.2 Serialisability. Concurrent transactions are correct when their effect equals some serial order. Two-phase locking guarantees conflict-serialisability.
  - CS.O.A3.5.3 Weaker isolation. Snapshot isolation allows write-skew anomalies that serialisability forbids. Many deployed systems default to weaker levels.
  - CS.O.A3.5.4 Query optimisation. A declarative query has many equivalent plans, and cost-based optimisers choose among them by estimates. Estimate errors grow with the number of joins.

Named objects: deadlock, Coffman conditions, linearisability, memory model, consensus number, FLP impossibility (hypotheses: asynchrony, determinism, one crash fault), Byzantine agreement bound (hypotheses: synchrony, oral messages), partial synchrony, Paxos, Raft (hypothesis: a correct majority), CAP theorem (hypotheses: partition, linearisability, availability as defined by Gilbert and Lynch), CRDT (hypothesis: commuting operations or semilattice merge), end-to-end argument, AIMD, Two Generals problem, relational model, ACID, serialisability, two-phase locking, snapshot isolation.

### CS.O.A4 Learning

**SCQA.** Situation. Some computations improve from data instead of from a programmer's rules. Complication. Learning theory gives guarantees for idealised settings, while practice runs on scaling and benchmarks that theory does not yet explain. Question. What can such systems learn, how well, and how can that be checked? Answer. CS owns learning theory as applied, models and training, reasoning and planning, perception and language processing, and alignment and evaluation. Probability and approximation theorems are MA.

Key line (inductive; plural noun: learning claims; dimension: what the claim is about; order: from guarantees, to trained models, to their use in search, to their use on signals, to whether they serve their purpose). Members (5): Learning theory · Models and training · Reasoning and planning · Perception and language processing · Alignment and evaluation.

- CS.O.A4.1 Learning theory. **What can be learned from samples is bounded by the capacity of the hypothesis class.** A binary concept class is PAC-learnable if and only if its VC dimension is finite (uses MA.O.A5). No-free-lunch: averaged uniformly over all objective functions, every optimiser performs equally.
  - CS.O.A4.1.1 Sample complexity. For a class of VC dimension d, the samples needed scale with d/ε, with a log(1/δ) term, up to logarithmic factors in the realisable case. The bound assumes i.i.d. samples.
  - CS.O.A4.1.2 Bias–variance trade-off. Expected squared error splits into bias, variance and noise. The classical U-shaped risk curve is not universal; double descent is reported in over-parameterised models (W4).
  - CS.O.A4.1.3 Online learning. Without distributional assumptions, regret against the best fixed expert can grow sublinearly in time. Multiplicative-weights methods achieve this.
  - CS.O.A4.1.4 Generalisation of deep networks. Why heavily over-parameterised networks generalise is not explained by VC bounds. This is OPEN.
- CS.O.A4.2 Models and training. **Trained models fit functions from data by optimisation, and expressive power does not imply learnability.** Universal approximation holds for one-hidden-layer networks with a non-polynomial activation, approximating continuous functions on compact sets to any accuracy. Empirical scaling laws are W4 claims within stated ranges.
  - CS.O.A4.2.1 Gradient-based training. Backpropagation computes exact gradients of a differentiable loss at cost proportional to one forward pass. Convergence to a global optimum is not guaranteed for non-convex losses (uses MA.O.A4).
  - CS.O.A4.2.2 Scaling laws. Loss falls as a power law in parameters, data and compute over measured ranges. Extrapolation beyond those ranges is (UNVERIFIED).
  - CS.O.A4.2.3 Architectures. Convolution encodes translation equivariance; attention computes data-dependent weighting over a sequence. Standard self-attention costs time quadratic in sequence length.
  - CS.O.A4.2.4 Regularisation. Weight penalties, dropout and early stopping reduce overfitting on held-out data. Their effect is measured per task, not guaranteed.
- CS.O.A4.3 Reasoning and planning. **Search and inference find solutions in spaces too large to enumerate, at stated worst-case cost.** Many planning problems are PSPACE-complete (uses MA.B.C3).
  - CS.O.A4.3.1 Heuristic search. A* returns an optimal path when its heuristic is admissible. With a consistent heuristic it expands each node at most once.
  - CS.O.A4.3.2 SAT solving. Conflict-driven clause learning solves many large industrial instances quickly, though SAT is NP-complete. Why practical instances are easy is OPEN.
  - CS.O.A4.3.3 Markov decision processes. With known transitions and rewards, value iteration converges to an optimal policy for discounted problems. Reinforcement learning drops the known-model assumption.
  - CS.O.A4.3.4 Probabilistic inference. Exact inference in general Bayesian networks is NP-hard (uses MA.B.C3). Practice uses approximation, such as sampling or variational methods.
- CS.O.A4.4 Perception and language processing. **Systems map signals such as images, speech and text to structured outputs, and are judged by measured performance.** Vision, speech and NLP are the standard areas. Claims about language itself are LN.
  - CS.O.A4.4.1 Benchmark performance. A reported accuracy holds for the test distribution used. Performance often drops under distribution shift.
  - CS.O.A4.4.2 Language models. Next-token prediction trained at scale yields models usable for many tasks without task-specific training. The extent of their reasoning ability is CONTESTED.
  - CS.O.A4.4.3 Adversarial examples. Small input perturbations can change a classifier's output while leaving human judgement unchanged. Robustness certificates hold only within a stated perturbation set.
- CS.O.A4.5 Alignment and evaluation of AI systems. **Whether a trained system pursues its intended objective cannot yet be reliably checked.** Methods are immature; much is OPEN.
  - CS.O.A4.5.1 Specification gaming. Systems optimised on a proxy objective can satisfy the proxy while failing the intent. Documented cases exist; their frequency in deployed systems is (UNVERIFIED).
  - CS.O.A4.5.2 Learning from human feedback. Training on human preference judgements shifts model behaviour towards rated preferences. It inherits the raters' errors and the reward model's limits.
  - CS.O.A4.5.3 Interpretability. Methods that locate features or circuits inside trained networks give partial accounts of computation. Whether they scale to full explanations is OPEN.
  - CS.O.A4.5.4 Evaluation validity. A benchmark score supports a capability claim only if the test data were not in training. Contamination checks are a W4 defeater test.

Named objects: PAC learning (hypotheses: i.i.d. samples from a fixed distribution, binary labels), VC dimension, no-free-lunch theorem (hypothesis: uniform average over all objectives), bias–variance decomposition (hypothesis: squared loss), double descent, regret, multiplicative weights, universal approximation (hypotheses: one hidden layer, non-polynomial activation, compact domain), backpropagation, scaling laws (W4, within ranges), attention, A* (hypothesis: admissible heuristic), CDCL SAT solving, Markov decision process (hypotheses: Markov property, known model for planning), Bayesian network, adversarial example, language model, reinforcement learning from human feedback, interpretability, benchmark contamination.

### CS.O.A5 Protection

**SCQA.** Situation. Computations run among adversaries. Complication. Security proofs hold relative to assumptions and models, while attacks exploit implementations, side channels and people. Question. What can be protected, from whom, and on what assumptions? Answer. CS owns deployed cryptography, systems security, privacy guarantees and the response to quantum threats. Proofs of security reductions are MA; data-protection law is LA.

Key line (inductive; plural noun: protection claims; dimension: what is protected and against which adversary; order: from the message, to the system, to the individual record, to future adversaries). Members (4): Cryptography in use · Systems security · Privacy · Quantum threats.

- CS.O.A5.1 Cryptography in use. **A protocol is secure only relative to a stated adversary model and hardness assumption.** Factoring is one such assumption. Security proofs are MA; the deployed protocol is CS.
  - CS.O.A5.1.1 Reduction-based security. A scheme is proved secure by showing that breaking it would solve an assumed-hard problem. The proof says nothing if the assumption fails (uses MA.B.C3).
  - CS.O.A5.1.2 Composition. A protocol secure in isolation can fail when composed with others. Universally composable security is one framework that preserves security under composition.
  - CS.O.A5.1.3 Implementation gap. Deployed cryptography is broken more often through implementation and key management than through its mathematics. This is an empirical claim (W4, UNVERIFIED as a proportion).
- CS.O.A5.2 Systems security. **A system is secure only against a stated threat model, and attack surface grows with complexity.** Access control, memory safety and attack surfaces are the standard objects.
  - CS.O.A5.2.1 Memory safety. Languages with enforced memory safety remove whole classes of vulnerability, such as buffer overflows. Unsafe escape hatches reintroduce them.
  - CS.O.A5.2.2 Least privilege. Granting each component only the rights it needs limits the damage of a compromise. Its effect is measured as reduced blast radius, not as prevention.
  - CS.O.A5.2.3 Side channels. Timing, power and cache behaviour can leak secrets that a functional model of the system does not represent. Speculative-execution attacks are a hardware instance.
  - CS.O.A5.2.4 Information-flow control. Non-interference states that secret inputs do not affect public outputs. Type systems can enforce it for stated languages, excluding timing channels unless modelled.
- CS.O.A5.3 Privacy. **Some privacy guarantees can be stated as bounds on what an output reveals about one record.** Differential privacy bounds how much one record changes an output distribution, by a stated ε.
  - CS.O.A5.3.1 Composition of privacy loss. Running several differentially private analyses adds their ε values in the basic theorem. Advanced composition gives tighter bounds at a small δ cost (uses MA.O.A5).
  - CS.O.A5.3.2 Failure of de-identification. Removing names does not prevent re-identification when other attributes can be linked. k-anonymity does not give the guarantee differential privacy gives.
  - CS.O.A5.3.3 Privacy–utility trade-off. Smaller ε means more noise and lower accuracy for a fixed sample size. No mechanism escapes this for all queries.
- CS.O.A5.4 Quantum threats. **A fault-tolerant quantum computer would break widely deployed public-key schemes.** Shor's algorithm factors in polynomial time on such a machine. Uses MA.B.C3 and PH.O.A2.
  - CS.O.A5.4.1 Grover's speed-up. Unstructured search gains only a quadratic speed-up on a quantum computer. Doubling symmetric key lengths is the standard response.
  - CS.O.A5.4.2 Post-quantum cryptography. Schemes based on lattices, codes and hashes are designed to resist known quantum attacks. Their hardness assumptions are less studied than factoring.
  - CS.O.A5.4.3 Harvest now, decrypt later. Ciphertext recorded today could be decrypted when large quantum computers exist. When such machines will exist is OPEN.

Named objects: hardness assumption, reduction-based security proof, universal composability, threat model, memory safety, least privilege, side channel, non-interference (hypothesis: no unmodelled channels), differential privacy (hypotheses: neighbouring datasets differ in one record, stated ε and δ), composition theorem, k-anonymity, Shor's algorithm (hypothesis: a fault-tolerant quantum computer), Grover's algorithm, post-quantum cryptography.

## 5. Face M — Methods

| ID | Role | Shared role | Example |
|---|---|---|---|
| CS.M.1 | Formalise | M1 Represent | specify, define a model of computation; e.g. a TLA+ model of a replication protocol |
| CS.M.2 | Prove | M2 Derive | correctness or bound proof; e.g. a loop invariant, a lower bound by adversary argument |
| CS.M.3 | Build | M4 Intervene | implement a system; e.g. a compiler, a database engine, a trained model |
| CS.M.4 | Run and measure | M5 Compute | benchmark, simulation, training run; e.g. throughput with stated variance, held-out loss |
| CS.M.5 | Verify | M7 Verify | model checking, test suite, audit; e.g. a fuzzing campaign, a proof checked in Coq or Isabelle |

Five roles. Example: a consensus protocol is formalised (CS.M.1), proved safe (CS.M.2), built (CS.M.3), measured under load (CS.M.4) and model-checked (CS.M.5). M3 Observe and M6 Compare appear only inside CS.M.4 (empirical evaluation) and are not separate roles.

### Heuristics register (outside the count)
Premature optimisation is the root of all evil; worse is better; end-to-end argument; design patterns; "make it work, make it right, make it fast"; ablation as a habit.

## 6. Face W — Warrants

| Cell | Warrant | Standard of acceptance | Typical defeaters |
|---|---|---|---|
| CS.O.A1 | W1 + W11 | machine-checked proof, or verification against a formal specification | specification wrong, unsound tool, unmodelled environment |
| CS.O.A2 | W1 + W2 | proof of bound on a stated model; benchmark with stated variance | model mismatch with hardware, unrepresentative input; e.g. cache effects reversing an asymptotic ranking |
| CS.O.A3 | W1 + W4 | impossibility or protocol proof; measured behaviour in deployment | failure model differs from assumed one |
| CS.O.A4 | W4 + W2 | held-out evaluation, stated metric and variance, replication | data leakage, benchmark overfitting, distribution shift; e.g. test items found in the training corpus |
| CS.O.A5 | W1 + W11 | reduction to a stated assumption; penetration test | broken assumption, side channel, implementation flaw; e.g. a timing leak in a proved scheme |

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

Example of a warrant chain: Raft's safety is W1 (proof); its throughput is W4 (measurement). A claim mixing them is split.

Bridge examples: C1 holds Rice's theorem in use; C2 holds type soundness; C3 holds Amdahl's law; C4 holds FLP and Raft; C5 holds serialisability; C6 holds PAC learning and scaling laws; C7 holds differential privacy; C8 holds measured interface effects; C9 holds numerical simulation cost.

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
Sizes: key line 5. Face O 5 cells + 24 sub-cells = 29, plus 86 second-level child cells (CS.O.An.m.k). M roles 5. Heuristics 6, outside the count. W rows 5. B bridges 9.
Key line, word for word: Correctness. Cost. Coordination. Learning. Protection.
OPEN: P vs NP (owned by MA.B.C3, cited); AI alignment methods (A4.5); generalisation of deep networks (A4.1.4); easiness of practical SAT (A4.3.2); interpretability at scale (A4.5.3); timing of fault-tolerant quantum computers (A5.4.3).
CONTESTED: software engineering in EN vs CS (alternative: CS.O.A1); HCI as a CS bridge vs an MS cell; Church–Turing thesis in CS vs PL (A1.1.4); reach of the end-to-end argument (A3.4.2); reasoning ability of language models (A4.4.2).
Second-level key lines: A1 semantics, verification, types, testing, limits; A2 algorithms, data structures, classes, machines, physical limits; A3 concurrency, agreement, partition, networks, data systems; A4 theory, training, planning, perception, alignment; A5 cryptography, systems, privacy, quantum.
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
| CS.O.A1.1.1 | Operational semantics | O/A1 | — |
| CS.O.A1.1.2 | Denotational semantics | O/A1 | MA.O.A2 |
| CS.O.A1.1.3 | Adequacy | O/A1 | — |
| CS.O.A1.1.4 | Church–Turing thesis | O/A1 | PL.O.A5 |
| CS.O.A1.2.1 | Hoare triples | O/A1 | — |
| CS.O.A1.2.2 | Termination | O/A1 | MA.O.A1 |
| CS.O.A1.2.3 | Model checking | O/A1 | — |
| CS.O.A1.2.4 | Separation logic | O/A1 | — |
| CS.O.A1.3.1 | Progress and preservation | O/A1 | — |
| CS.O.A1.3.2 | Type inference | O/A1 | — |
| CS.O.A1.3.3 | Curry–Howard correspondence | O/A1 | MA.O.A1 |
| CS.O.A1.4.1 | Coverage criteria | O/A1 | — |
| CS.O.A1.4.2 | Property-based testing | O/A1 | — |
| CS.O.A1.4.3 | Mutation testing | O/A1 | — |
| CS.O.A1.5.1 | Halting problem | O/A1 | MA.O.A1 |
| CS.O.A1.5.2 | Sound but incomplete analysis | O/A1 | — |
| CS.O.A1.5.3 | Specification gap | O/A1 | — |
| CS.O.A2.1.1 | Asymptotic cost | O/A2 | — |
| CS.O.A2.1.2 | Design paradigms | O/A2 | — |
| CS.O.A2.1.3 | Randomised algorithms | O/A2 | MA.O.A5 |
| CS.O.A2.1.4 | Approximation | O/A2 | MA.B.C3 |
| CS.O.A2.2.1 | Amortised analysis | O/A2 | — |
| CS.O.A2.2.2 | Hashing | O/A2 | — |
| CS.O.A2.2.3 | Balanced search trees | O/A2 | — |
| CS.O.A2.2.4 | External memory | O/A2 | — |
| CS.O.A2.3.1 | Reductions in practice | O/A2 | — |
| CS.O.A2.3.2 | Hardness assumptions as engineering inputs | O/A2 | MA.B.C3 |
| CS.O.A2.3.3 | Parameterised complexity | O/A2 | — |
| CS.O.A2.4.1 | Locality | O/A2 | — |
| CS.O.A2.4.2 | Gustafson's law | O/A2 | — |
| CS.O.A2.4.3 | Instruction-level parallelism | O/A2 | — |
| CS.O.A2.4.4 | Accelerators | O/A2 | — |
| CS.O.A2.5.1 | End of Dennard scaling | O/A2 | PH.O.A4 |
| CS.O.A2.5.2 | Landauer's bound | O/A2 | PH.O.A4 |
| CS.O.A2.5.3 | Energy as a cost measure | O/A2 | — |
| CS.O.A3.1.1 | Coffman conditions | O/A3 | — |
| CS.O.A3.1.2 | Linearisability | O/A3 | — |
| CS.O.A3.1.3 | Memory models | O/A3 | — |
| CS.O.A3.1.4 | Wait-free hierarchy | O/A3 | MA.B.C3 |
| CS.O.A3.2.1 | Partial synchrony | O/A3 | — |
| CS.O.A3.2.2 | Crash-fault consensus protocols | O/A3 | — |
| CS.O.A3.2.3 | Randomised consensus | O/A3 | — |
| CS.O.A3.2.4 | Signed messages | O/A3 | — |
| CS.O.A3.3.1 | Scope of CAP | O/A3 | — |
| CS.O.A3.3.2 | Latency trade-off | O/A3 | — |
| CS.O.A3.3.3 | Convergent replicated data types | O/A3 | — |
| CS.O.A3.4.1 | Layering | O/A3 | — |
| CS.O.A3.4.2 | End-to-end argument | O/A3 | — |
| CS.O.A3.4.3 | Congestion control | O/A3 | — |
| CS.O.A3.4.4 | Two Generals problem | O/A3 | — |
| CS.O.A3.5.1 | Relational model | O/A3 | MA.O.A1 |
| CS.O.A3.5.2 | Serialisability | O/A3 | — |
| CS.O.A3.5.3 | Weaker isolation | O/A3 | — |
| CS.O.A3.5.4 | Query optimisation | O/A3 | — |
| CS.O.A4.1.1 | Sample complexity | O/A4 | — |
| CS.O.A4.1.2 | Bias–variance trade-off | O/A4 | — |
| CS.O.A4.1.3 | Online learning | O/A4 | — |
| CS.O.A4.1.4 | Generalisation of deep networks | O/A4 | — |
| CS.O.A4.2.1 | Gradient-based training | O/A4 | MA.O.A4 |
| CS.O.A4.2.2 | Scaling laws | O/A4 | — |
| CS.O.A4.2.3 | Architectures | O/A4 | — |
| CS.O.A4.2.4 | Regularisation | O/A4 | — |
| CS.O.A4.3.1 | Heuristic search | O/A4 | — |
| CS.O.A4.3.2 | SAT solving | O/A4 | — |
| CS.O.A4.3.3 | Markov decision processes | O/A4 | — |
| CS.O.A4.3.4 | Probabilistic inference | O/A4 | MA.B.C3 |
| CS.O.A4.4.1 | Benchmark performance | O/A4 | — |
| CS.O.A4.4.2 | Language models | O/A4 | — |
| CS.O.A4.4.3 | Adversarial examples | O/A4 | — |
| CS.O.A4.5.1 | Specification gaming | O/A4 | — |
| CS.O.A4.5.2 | Learning from human feedback | O/A4 | — |
| CS.O.A4.5.3 | Interpretability | O/A4 | — |
| CS.O.A4.5.4 | Evaluation validity | O/A4 | — |
| CS.O.A5.1.1 | Reduction-based security | O/A5 | MA.B.C3 |
| CS.O.A5.1.2 | Composition | O/A5 | — |
| CS.O.A5.1.3 | Implementation gap | O/A5 | — |
| CS.O.A5.2.1 | Memory safety | O/A5 | — |
| CS.O.A5.2.2 | Least privilege | O/A5 | — |
| CS.O.A5.2.3 | Side channels | O/A5 | — |
| CS.O.A5.2.4 | Information-flow control | O/A5 | — |
| CS.O.A5.3.1 | Composition of privacy loss | O/A5 | MA.O.A5 |
| CS.O.A5.3.2 | Failure of de-identification | O/A5 | — |
| CS.O.A5.3.3 | Privacy–utility trade-off | O/A5 | — |
| CS.O.A5.4.1 | Grover's speed-up | O/A5 | — |
| CS.O.A5.4.2 | Post-quantum cryptography | O/A5 | — |
| CS.O.A5.4.3 | Harvest now, decrypt later | O/A5 | — |
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
| R6 | PASS | Six OPEN, five CONTESTED; UNVERIFIED claims flagged in A1.4.3, A4.2.2, A4.5.1, A5.1.3. |
| R7 | PASS | Members are identical in sections 2, 3 and 11. |
| R8 | PASS | Section 9. |
| R9 | PASS | A1–A5 each have SCQA, key line and objects. |
| R10 | PASS | Plain register. |
| R11 | FAIL (partial) | Dates for FLP (1985) and the CAP proof (2002) are from memory. Repair: cite the original papers. |
| R12 | PASS | IDs are stable. |
