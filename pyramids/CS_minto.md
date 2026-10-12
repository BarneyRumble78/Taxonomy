# CS — top-down Minto pyramid

Built by scripts/minto_pass.py from the grouped classification. Three rules (Minto pp. 9-11): each summary states the idea of its group, members are the same kind of idea, and they are in a stated order.

## Introduction

**Situation.** Computer science studies computations, and every field in it asserts some property of them.

**Complication.** The fields are catalogued by several inconsistent schemes, with residual and container headings mixed in with real topics.

**Question.** How is everything in computer science divided by the property asserted of a computation?

**Answer.** Computer science divides by the property asserted of a computation into correctness, cost, coordination, learning and protection, moving from the single program outward to many agents and adversaries.

## Governing thought

Computer science divides by the property asserted of a computation into correctness, cost, coordination, learning and protection, moving from the single program outward to many agents and adversaries.

## Key line

Group of properties. Basis: kinds. Dimension: the property asserted of a computation. Order: structure. The pillars run from the single program outward to many agents and adversaries.

1. Correctness is the property that a computation does what it is specified, expressed and proved to do, covering program structure, verification, process quality and formal theory. `CS.K1`
2. Cost is the property of how much time, space, bandwidth or effort a computation consumes and how that is traded off against quality. `CS.K2`
3. Coordination is the property of how a computation interacts with other systems, agents and the world through networks, reasoning, language and perception. `CS.K3`
4. Learning is the property that a computation improves its behaviour from data or produces content and products for users, alongside cross-cutting reference tools. `CS.K4`
5. Protection is the property that a computation resists attack and safeguards data, spanning formal and human aspects and the concrete systems that are defended. `CS.K5`

## Groups

### 1. Correctness is the property that a computation does what it is specified, expressed and proved to do, covering program structure, verification, process quality and formal theory.

- **Structural and notational properties concern how a program is expressed, organized and architected, including its languages, notations, and overall organization.**
  _basis: kinds, order: structure. Ordered by structure, from broad software areas to specific notations and architecture._
  - Software and its engineering
  - Software organization and properties
  - Software notations and tools
  - Programming languages
  - Software architecture
- **Correctness and assurance properties concern whether a computation meets its specification, as shown by formal proof, testing, verification and validation.**
  _basis: kinds, order: structure. Ordered by structure, from formal proof to testing and validation._
  - Formal methods for software
  - Software testing, verification and validation
  - Automated software engineering
- **Quality and process properties concern how well software is built and managed, including its requirements, measured quality, empirical evidence and creation practices.**
  _basis: kinds, order: structure. Ordered by structure, from requirements through process and metrics to empirical study._
  - Software creation and management
  - Requirements engineering
  - Software quality, processes and metrics
  - Empirical software engineering
  - Software engineering
- **Foundational properties characterize a computation by its mathematics, randomness, defining formal model, or provable correctness and cost.**
  _basis: kinds, order: structure. Ordered from mathematical foundations through probabilistic and formal models to correctness and efficiency._
  - **Mathematics of computing covers the mathematical foundations asserted of computations, such as discreteness, continuity, probability and analysis.**
    _basis: kinds, order: structure. Ordered by structure, from the umbrella field to its branches._
    - Mathematics of computing
    - Discrete mathematics
    - Continuous mathematics
    - Mathematical analysis
  - **Probabilistic and information-theoretic properties characterize a computation by its randomness, uncertainty and information content.**
    _basis: kinds, order: structure. Ordered by structure, from probability to information and random structures._
    - Probability and statistics
    - Information theory
    - Randomness, geometry and discrete structures
  - **Computability and expressiveness properties characterize a computation by the formal model, language or automaton that defines what it can do.**
    _basis: kinds, order: structure. Ordered by structure, from the general field to specific formal models._
    - Theory of computation
    - Models of computation
    - Formal languages and automata theory
  - **Correctness, efficiency and difficulty properties characterize a computation by what can be proved, how costly it is, and how well an algorithm solves it.**
    _basis: kinds, order: structure. Ordered by structure, from logic and semantics to complexity and algorithm design._
    - Computational complexity and cryptography
    - Logic
    - Design and analysis of algorithms
    - Semantics and reasoning
    - Theory and algorithms for application domains
- **Theoretical computing fields assert that a computation has provable, approximable or reliably transmittable properties.**
  _basis: kinds, order: structure. Ordered from formal theory to numerical and quantum computation and then coding and information theory._
  - **Formal theory of computation asserts that a computation has provable properties such as complexity, decidability, logical correctness, concurrency behaviour and algorithmic efficiency.**
    _basis: kinds, order: structure. Kinds of formal theoretical properties, listed by structure with no ranking._
    - Theory of computation
    - Computational complexity and computability
    - Computational logic and formal languages
    - Concurrency theory
    - Data structures and algorithms
  - **Numerical and quantum computation asserts that a computation approximates mathematical quantities accurately or exploits quantum physical resources.**
    _basis: kinds, order: structure. Kinds of physical and numerical computation, listed by structure with no ranking._
    - Numerical computation and mathematical software
    - Quantum computation
    - Theory of computation not elsewhere classified
  - **Coding and information theory asserts that a computation represents, compresses and transmits information reliably across noisy channels.**
    _basis: kinds, order: structure. Kinds of coding and communication topics, listed by structure with no ranking._
    - Coding, information theory and compression
    - Audio coding
    - Biological information theory
    - Channel coding

### 2. Cost is the property of how much time, space, bandwidth or effort a computation consumes and how that is traded off against quality.

- **Coding theory topics are the measures, operations, trade-offs and context that make up the study of coding and information.**
  _basis: parts, order: structure. Ordered from information measures to coding operations, compression trade-offs and broader context._
  - **Information measures are quantities that numerically characterize information content or the difference between code words.**
    _basis: kinds, order: degree. Ranked from the most fundamental information measures to code-word metrics._
    - Information entropy
    - Mutual information
    - Hamming distances
    - Hamming weight
  - **Coding operations are the processes that transform messages into code words and recover them again.**
    _basis: kinds, order: degree. Ranked from the general transformation steps to the specialized coding schemes._
    - Encoding
    - Decoding
    - Source coding
    - Error compensation
  - **Compression and rate trade-off topics concern how much a signal can be compressed for a given level of allowed distortion.**
    _basis: kinds, order: degree. Ranked from the theoretical rate-distortion framework to its applied forms._
    - Rate distortion theory
    - Rate-distortion
    - Speech coding
  - **Broader context topics are the general field label and applications or models that extend beyond core coding theory.**
    _basis: kinds, order: degree. Ranked from the field itself to peripheral applications and unrelated models._
    - Information theory
    - Network coding
    - Genetic communication
    - Technology acceptance model
- **Behavioural and human-facing properties classify a computation by the property it asserts, such as its speed, correctness, usability, trustworthiness, or the content it processes.**
  _basis: kinds, order: structure. Kinds ordered by structure, from field-level framing to specific property types._
  - **Each of these fields is defined by the property it asserts of a computation, whether its speed, its correctness, its delivery infrastructure, or the structure and rules of the network it runs on.**
    _basis: kinds, order: structure_
    - **Performance-oriented fields assert that a computation runs fast, scales in parallel or uses little energy, and measure how well it does so.**
      _basis: kinds, order: degree. Ranked from the broadest speed-focused concern, high performance and parallelism, to the narrower concerns of energy use and measurement._
      - High performance computing
      - Concurrent/parallel systems and technologies
      - Energy-efficient computing
      - Performance evaluation
    - **Deployment and connectivity fields assert that a computation is delivered over a particular infrastructure, such as the cloud, mobile devices, networks, services or embedded things.**
      _basis: kinds, order: structure. Ordered structurally from centralised infrastructure to edge and device-level deployment._
      - Cloud computing
      - Networking and communications
      - Service oriented computing
      - Mobile computing
      - Cyberphysical systems and internet of things
    - **Correctness-oriented fields assert that a computation behaves reliably and coordinates correctly across components, from dependable systems to distributed algorithms and the operating system layer.**
      _basis: kinds, order: structure. Ordered structurally from system-wide guarantees down to the operating system layer._
      - Dependable systems
      - Distributed systems and algorithms
      - Operating systems
    - **Network architectures and components are the structural parts from which a network is built.**
      _basis: kinds, order: structure. Ordered by structure._
      - Network architectures
      - Network components
      - Network performance evaluation
      - Network properties
    - **Network protocols and algorithms are the rules and procedures that govern how a network behaves.**
      _basis: kinds, order: structure. Ordered by structure._
      - Network protocols
      - Network algorithms
      - Network services
      - Network types
  - **Each of these concepts classes computing by a property asserted of a computation, whether the broad application areas it serves, the timeliness and dependability of its systems, or how well people can use and interact with it.**
    _basis: kinds, order: structure_
    - **The umbrella categories for applied computing are general headings that gather application areas without naming one specific domain.**
      _basis: kinds, order: structure. Ordered by structure of the classification schemes._
      - Computers in other domains
      - Applied computing
    - **Computer systems organization covers kinds of systems classed by the property they assert of computation, such as timeliness, dependability or embedded operation.**
      _basis: kinds, order: structure. Ordered by structure of the classification schemes._
      - Computer systems organization
      - Architectures
      - Embedded and cyber-physical systems
      - Real-time systems
      - Dependable and fault-tolerant systems and networks
    - **Human-computer interaction concepts assert that a computation is shaped around how people use, design for, and gain access to it.**
      _basis: kinds, order: structure. Ordered from the broad field of HCI to the narrower concerns of interaction design and accessibility._
      - Human computer interaction (HCI)
      - Interaction design
      - Accessibility
    - **Application and presentation concepts assert that a computation serves a particular purpose, such as trading goods or making data visible.**
      _basis: kinds, order: structure. Ordered from commercial application to data presentation, with no ranking implied._
      - Electronic commerce
      - Visualization
  - **Human-centred and trust properties assert that a computation serves, supports, or can be trusted by the people who use it or are affected by it.**
    _basis: kinds, order: structure. Kinds of people-facing property, listed by structure with no ranking implied._
    - **Human-centred fields assert that a computation serves, understands or supports people, covering accessibility, emotion, collaboration and learning.**
      _basis: kinds, order: structure. Ordered structurally from individual users to groups and educational settings._
      - Accessible computing
      - Affective computing
      - Collaborative and social computing
      - Computing education
    - **Computer systems are judged by the trust properties asserted of them, such as fairness, ethics, security, and human oversight of automated decisions.**
      _basis: kinds, order: structure. Ordered by structure, from ethical trust properties to security and oversight._
      - Fairness, accountability, transparency, trust and ethics of computer systems
      - Computer security
      - Mixed initiative and human-in-the-loop
    - **Computation is characterised by how well it serves human users, through usable interaction, clear visual presentation, and interfaces that fit people.**
      _basis: kinds, order: structure. Ordered by structure, from general interaction to presentation and interface forms._
      - Human-computer interaction
      - Information visualisation
      - Computer interfaces
      - Human-centred computing not elsewhere classified
  - **Execution and performance properties assert how a computation runs, in terms of efficiency, concurrency, scale, timing, or computing paradigm.**
    _basis: kinds, order: structure. Kinds of execution property, listed by structure with no ranking implied._
    - **Computation is characterised by how efficiently and correctly it runs, in its performance, its tolerance of approximation, and its coordination of concurrent work.**
      _basis: kinds, order: structure. Ordered by structure, from performance to approximation and concurrency control._
      - Computer performance
      - Approximate computing
      - Concurrency control
      - Computer architecture
    - **Each of these concepts names a way of executing computation, either by running many operations or tasks at the same time or by operating at very large scale and speed.**
      _basis: kinds, order: structure. Ordered from general concurrency to extreme scale._
      - Parallel processing
      - Multitasking
      - High performance computing
      - Petascale computing
    - **Execution-model concepts characterize a computation by the computing paradigm or timing and scheduling regime under which it runs.**
      _basis: kinds, order: structure. Ordered by structure, from computing paradigms to timing and scheduling regimes._
      - Probability computing
      - Quantum computing
      - Real-time systems
      - Time sharing computer systems
  - **Content and software properties, together with residual categories, assert what a computation transforms or infers, which software artifact it is, or that it is general or unclassified.**
    _basis: kinds, order: structure. Kinds of content and software property plus residual categories, listed by structure with no ranking implied._
    - **Umbrella and residual categories collect computing work whose asserted property is either general to a whole division or not classified elsewhere.**
      _basis: kinds, order: structure. Ordered structurally from division-level headings to residual catch-all codes._
      - Distributed computing and systems software
      - Human-centred computing
      - Distributed computing and systems software not elsewhere classified
      - Applied computing not elsewhere classified
    - **A computation is characterized by the nature of the content it transforms or the inference it draws, whether visual data, recognized patterns, probabilistic reasoning, or structured data.**
      _basis: kinds, order: structure. Ordered from raw signal handling to uncertain reasoning._
      - Image processing
      - Pattern recognition
      - Probabilistic computing
      - Data systems
    - **Software-oriented concepts characterize a computation by the program artifact, its engineering discipline, its hosting layer, or its restoration after failure.**
      _basis: kinds, order: structure. Ordered by structure, from the software artifact to its engineering, hosting and recovery._
      - Software
      - Software engineering
      - Virtual machine monitors
      - System recovery
- **Organisational and representational methodologies are kinds of computation defined by how work is divided across processes or how systems and mathematical objects are modelled and transformed.**
  _basis: kinds, order: structure. Ordered from coordination of work to representation of systems._
  - **Parallel, concurrent and distributed methodologies are computation approaches defined by how work is split and coordinated across processes or machines.**
    _basis: kinds, order: structure. Ordered by structure of the coordination model._
    - Parallel computing methodologies
    - Distributed computing methodologies
    - Concurrent computing methodologies
    - Computing methodologies
  - **Modeling, simulation, graphics and symbolic manipulation are methodologies that represent or transform systems and mathematical objects computationally.**
    _basis: kinds, order: structure. Ordered by structure of what is represented._
    - Modeling and simulation
    - Modelling and simulation
    - Computer graphics
    - Symbolic and algebraic manipulation

### 3. Coordination is the property of how a computation interacts with other systems, agents and the world through networks, reasoning, language and perception.

- **Network and substrate properties classify a computation by the structure, rules, and infrastructure of the system on which it is built and delivered.**
  _basis: kinds, order: structure. Kinds ordered by structure, from network parts to rules to deployment infrastructure._
  - **Network architectures and components are the structural parts, protocols and algorithms are the governing rules, and deployment fields are the infrastructure over which a network delivers computation.**
    _basis: parts, order: structure. Ordered from structure to rules to delivery infrastructure._
    - **Computing applied to the life, health and physical sciences is one kind of application domain, defined by the natural-science subject matter.**
      _basis: kinds, order: structure. Ordered by structure of the classification schemes._
      - Life and medical sciences
      - Applications in health
      - Applications in life sciences
      - Applications in physical sciences
    - **Computing applied to law, social behaviour, education and the arts and humanities is a kind of application domain defined by human and cultural subject matter.**
      _basis: kinds, order: structure. Ordered by structure of the classification schemes._
      - Law, social and behavioral sciences
      - Arts and humanities
      - Education
      - Applications in arts and humanities
      - Applications in social sciences and education
    - **Computing applied to handling information, evidence, planning and location is a kind of application defined by the data and decisions processed.**
      _basis: kinds, order: structure. Ordered by structure of the classification schemes._
      - Computer forensics
      - Operations research
      - Document management and text processing
      - Spatial data and applications
  - **Network architectures and components are the structural parts, protocols and algorithms are the governing rules, and deployment fields are the infrastructure over which a network delivers computation.**
    _basis: kinds, order: structure_
    - **Human-centered and applied computing are the areas where computation is shaped by people and by domains of use.**
      _basis: kinds, order: structure. Ordered by structure._
      - Human-centered computing
      - Collaborative and social computing
      - Ubiquitous and mobile computing
      - Applied computing
      - Enterprise computing
    - **Physical sciences and engineering and Networks are broad computing areas, each defined by the kind of system or domain a computation is applied to.**
      _basis: kinds, order: structure. Members are peer application areas ordered by structure, with no ranking among them._
      - Physical sciences and engineering
      - Networks
  - **Substrate, structure, and embedding properties assert what a computation is built from, where it is deployed, or how the system providing it is organised.**
    _basis: kinds, order: structure. Kinds of substrate and deployment property, listed by structure with no ranking implied._
    - **Computation is characterised by where and how it is embedded in the world, in ambient devices, social robots, and applied settings.**
      _basis: kinds, order: structure. Ordered by structure, from embedded devices to social agents and applications._
      - Pervasive computing
      - Social robotics
      - Computer applications
      - Computer peripherals
    - **Computation is characterised by the general field and substrate it belongs to, from the broad discipline and machines to networks and molecular computing.**
      _basis: kinds, order: structure. Ordered by structure, from the broad field to specific substrates and networks._
      - Computers and information processing
      - Computer science
      - Computers
      - Computer networks
      - DNA computing
    - **Each concept names the physical or logical substrate on which a computation is carried out, so that the property asserted is what the computation is built from.**
      _basis: kinds, order: structure. Ordered from conventional electronic substrates to unconventional ones._
      - Hardware
      - Digital systems
      - Optical computing
      - Molecular computing
    - **A computation can be characterized by where it runs and the environment in which it is deployed, such as across networked machines, on portable devices, embedded in surroundings, or on virtualized platforms.**
      _basis: kinds, order: structure. Ordered from spread-out systems to ubiquitous and virtualized ones._
      - Distributed computing
      - Mobile computing
      - Pervasive computing
      - Platform virtualization
    - **Memory, file servers, database machines, and open systems each name a way a computing system is structured, around storage, service, or interoperability, so that it can provide a computation.**
      _basis: kinds, order: structure. Ordered from storage components to openly interoperable systems._
      - Memory
      - File servers
      - Database machines
      - Open systems
- **Intelligent reasoning and agency computations are kinds of computation that reason over knowledge, choose actions under constraints, or act and adapt autonomously.**
  _basis: kinds, order: structure. Ordered from knowledge and uncertainty reasoning to adaptive agents, constraint-driven choice, and the intelligence fields as a whole._
  - **Knowledge-based and uncertainty-handling methodologies are artificial intelligence approaches that reason over represented knowledge or imprecise information.**
    _basis: kinds, order: structure. Ordered by structure of the reasoning approach._
    - Artificial intelligence
    - Artificial Intelligence & Expert Systems
    - Artificial intelligence
    - Knowledge representation and reasoning
    - Fuzzy computation
  - **Adaptive, evolutionary and agent-based methodologies are approaches in which autonomous or evolving entities act and adapt, including robots.**
    _basis: kinds, order: structure. Ordered by structure of the adaptive entity._
    - Artificial life and complex adaptive systems
    - Autonomous agents and multiagent systems
    - Evolutionary computation
    - Intelligent robotics
    - Robotics
  - **Computations in this group are asserted to select a correct, feasible or best choice among alternatives.**
    _basis: kinds, order: structure. Ordered by structure, from choosing actions to solving constraints and optima._
    - Planning and decision making
    - Satisfiability and optimisation
  - **Computations in this group are asserted to handle general, residual or mixed-modality intelligent processing that is not defined by a single choice or solution task.**
    _basis: kinds, order: structure. Ordered by structure, from general AI to vision and multimedia and multimodal processing._
    - Artificial intelligence not elsewhere classified
    - Computer vision and multimedia computation not elsewhere classified
    - Multimodal analysis and synthesis
  - **Intelligence fields are kinds of computation judged by whether they exhibit intelligent, reasoned, or self-developing behavior.**
    _basis: kinds, order: structure. Ordered structurally from the umbrella field to its specific branches._
    - Computational and artificial intelligence
    - Artificial intelligence
    - Computational intelligence
    - Machine intelligence
- **Perception and language computations are kinds of computation that acquire, interpret, produce or transform human language and sensory signals such as speech, images, audio and video.**
  _basis: kinds, order: structure. Ordered from language and speech to sensing and media signal transformation._
  - **Language and speech computations are defined by the property of understanding, recognising or producing human language and speech.**
    _basis: kinds, order: structure. Kinds of language and speech computation, listed in no ranked order._
    - Natural language processing
    - Speech production
    - Speech recognition
  - **Visual and sensing computations are defined by the property of acquiring and interpreting visual scenes and sensed signals.**
    _basis: kinds, order: structure. Kinds of visual and sensing computation, listed in no ranked order._
    - Computer vision and multimedia computation
    - Active sensing
    - Computational imaging
    - Computer vision
    - Pattern recognition
  - **Media transformation computations are defined by the property of processing, compressing or synthesising audio, image and video signals.**
    _basis: kinds, order: structure. Kinds of media signal computation, listed in no ranked order._
    - Audio processing
    - Image and video coding
    - Image processing
    - Video processing

### 4. Learning is the property that a computation improves its behaviour from data or produces content and products for users, alongside cross-cutting reference tools.

- **Learning-based computations are kinds of computation that acquire or improve their behaviour from data or feedback rather than from explicit rules.**
  _basis: kinds, order: structure. Ordered from the general learning property to specific method families and network architectures._
  - **Machine learning and neural network methodologies are approaches in which computation acquires its behavior from data rather than explicit rules.**
    _basis: kinds, order: structure. Ordered by structure of the learning approach._
    - Machine learning
    - Neural Networks
  - **Learning computations are defined by the property of improving behaviour from data, including under adversarial conditions or from context.**
    _basis: kinds, order: structure. Kinds of learning computation, listed in no ranked order._
    - Machine learning
    - Adversarial machine learning
    - Context learning
  - **Machine learning paradigms are kinds of learning in which a computation is asserted to improve its behavior from data or experience.**
    _basis: kinds, order: structure. Ordered by structure, from specific named paradigms to the residual catch-all category._
    - Reinforcement learning
    - Semi- and unsupervised learning
    - Machine learning not elsewhere classified
  - **Foundational areas of computational intelligence are kinds of study that assert formal reasoning or developmental growth as the property of a computation.**
    _basis: kinds, order: structure. Ordered by structure, from formal reasoning to developmental processes._
    - Logic
    - Autonomous mental development
  - **Neural network approaches are kinds of computation built from layered networks of interconnected artificial units.**
    _basis: kinds, order: structure. Ordered structurally from general networks to deep architectures._
    - Deep learning
    - Neural networks
    - Neural networks
- **Applied and media computing characterizes a computation by the products, experiences and environments it delivers to users.**
  _basis: kinds, order: structure. Ordered from general applied products to interactive media and then immersive environments._
  - **Applied properties characterize a computation by the software, designs, images or games it produces for users.**
    _basis: kinds, order: structure. Ordered by structure, from mathematical software to graphics fields and their applications._
    - Mathematical software
    - Graphics, augmented reality and games
    - Computer aided design
    - Computer graphics
    - Entertainment and gaming
  - **Creative media computing covers computations whose asserted property is generating or shaping stories, game content, and sound for human experience.**
    _basis: kinds, order: structure. Ordered structurally from narrative to generated content to audio media._
    - Interactive narrative
    - Procedural content generation
    - Sound and music computing
  - **Information-theoretic constructs describe the properties of a computation in terms of how information is transmitted and represented between sender and receiver.**
    _basis: kinds, order: structure. Ordered structurally from the transmission medium to the representation applied to messages._
    - Communication channels
    - Codes
  - **Immersive and applied media computing asserts that a computation produces simulated or blended environments that serve a purpose beyond entertainment.**
    _basis: kinds, order: structure. Kinds of immersive and applied environments, listed by structure with no ranking._
    - Serious games
    - Virtual and mixed reality
    - Graphics, augmented reality and games not elsewhere classified
- **Reference documents and cross-cutting tools support the study and use of computations without asserting one specific property of them.**
  _basis: kinds, order: structure. Ordered by structure, from document types to cross-computing tools._
  - General and reference
  - Document types
  - Cross-computing tools and techniques

### 5. Protection is the property that a computation resists attack and safeguards data, spanning formal and human aspects and the concrete systems that are defended.

- **Conceptual and formal fields assert abstract guarantees about a computation, covering the overall domain, provable properties, data protection and human or policy constraints.**
  _basis: kinds, order: structure. Ordered from the broad umbrella domain to formal proofs, then data protections, then human and policy dimensions._
  - **Broad umbrella fields name the overall security and privacy domain within which specific computation properties are asserted.**
    _basis: kinds, order: structure. Ordered by structure from the general ACM and ANZSRC top-level headings to the narrower security heading._
    - Security and privacy
    - Cybersecurity and privacy
  - **Mathematical and formal foundations assert provable properties of a computation, such as secrecy, correctness and security guarantees.**
    _basis: kinds, order: structure. Ordered by structure from cryptographic primitives to formal theory and the services built on them._
    - Cryptography
    - Cryptography
    - Formal methods and theory of security
    - Security services
  - **Data-centred protections assert confidentiality, integrity and privacy of information handled or stored by a computation, including after-the-fact evidence.**
    _basis: kinds, order: structure. Ordered by structure from stored data security to data protection, privacy, and forensic examination._
    - Database and storage security
    - Data security and protection
    - Data and information privacy
    - Digital forensics
  - **Human, social and policy dimensions assert how people, professions and regulation shape and constrain secure computation.**
    _basis: kinds, order: structure. Ordered by structure from the individual user to the profession, society and policy._
    - User characteristics
    - Human and societal aspects of security and privacy
    - Social and professional topics
    - Professional topics
    - Computing / technology policy
- **System-oriented fields assert that the concrete machinery of a computation, from hardware and software layers to whole networks, resists attack and fails detectably.**
  _basis: kinds, order: structure. Ordered from system-level defenses to single-layer security to whole interconnected system security._
  - **System-level defenses assert that hardware, operating systems, software and networks resist attack and misbehave detectably.**
    _basis: kinds, order: structure. Ordered by structure from hardware at the bottom up through systems, software, and network layers, ending with detection._
    - Security in hardware
    - Systems security
    - Software and application security
    - Network security
    - Intrusion/anomaly detection and malware mitigation
  - **Layer-specific security fields assert security of a single component layer of a computation, either the physical hardware or the software running on it.**
    _basis: kinds, order: structure. Ordered by structure from the lowest layer, hardware, to the higher layer, software and applications._
    - Hardware security
    - Software and application security
  - **Broad system-level security fields assert security of whole interconnected systems and networks, together with the residual cybersecurity and privacy topics not classified elsewhere.**
    _basis: kinds, order: structure. Ordered by structure from the defined system and network field to the residual catch-all category._
    - System and network security
    - Cybersecurity and privacy not elsewhere classified

## Checks

- minto_check: {'mixed_kinds': ["CS.O.A1.G4: ['condition', 'response']"]}
- field_check holds: False — Pillars are not mutually exclusive values of one dimension: P2 mixes coding theory, human-facing and methodology groups under "cost" (P2.1-P2.3); P1.4/P1.5 overlap on theory; P4.2/P4.3 are not learning.
