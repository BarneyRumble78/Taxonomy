# CS — top-down Minto pyramid

Built by scripts/minto_pass.py from the grouped classification. Three rules (Minto pp. 9-11): each summary states the idea of its group, members are the same kind of idea, and they are in a stated order.

## Introduction

**Situation.** Computer science studies computations that are specified, run, connected, trained and attacked.

**Complication.** Existing classifications mix library schemes, residual classes and overlapping sources, so the same property appears in many places.

**Question.** How is everything in computer science divided?

**Answer.** Computer science is divided by the property asserted of a computation, running from the single program outward to many agents and adversaries: correctness, cost, coordination, learning and protection.

## Governing thought

Computer science is divided by the property asserted of a computation, running from the single program outward to many agents and adversaries: correctness, cost, coordination, learning and protection.

## Key line

Group of properties. Basis: kinds. Dimension: the property asserted of a computation. Order: structure. The pillars run from the single program outward to many agents and adversaries.

1. Correctness is the property that a computation meets its specification, shown through formal theory, mathematical foundations, verification and sound software construction. `CS.K1`
2. Cost is the property of how much time, energy, space or information a computation consumes, and how that consumption is measured and traded off. `CS.K2`
3. Coordination is the property of how a computation works with other components, machines, agents and people through shared structure and interaction. `CS.K3`
4. Learning is the property that a computation improves or exhibits intelligent behaviour from data, experience and reasoning rather than fixed rules. `CS.K4`
5. Protection is the property that a computation resists attack, keeps information confidential and can be trusted by the people it affects. `CS.K5`

## Groups

### 1. Correctness is the property that a computation meets its specification, shown through formal theory, mathematical foundations, verification and sound software construction.

- **Theoretical foundations assert that a computation has provable, mathematically describable properties and defined expressive power.**
  _basis: kinds, order: structure. Ordered from mathematical bases to models and reasoning._
  - **Mathematics of computing covers the mathematical foundations asserted of computations, such as discreteness, continuity, probability and analysis.**
    _basis: kinds, order: structure. Ordered by structure, from the umbrella field to its branches._
    - Mathematics of computing
    - Discrete mathematics
    - Continuous mathematics
    - Mathematical analysis
  - **Computability and expressiveness properties characterize a computation by the formal model, language or automaton that defines what it can do.**
    _basis: kinds, order: structure. Ordered by structure, from the general field to specific formal models._
    - Theory of computation
    - Models of computation
    - Formal languages and automata theory
  - **Formal theory of computation asserts that a computation has provable properties such as complexity, decidability, logical correctness, concurrency behaviour and algorithmic efficiency.**
    _basis: kinds, order: structure. Kinds of formal theoretical properties, listed by structure with no ranking._
    - Theory of computation
    - Computational complexity and computability
    - Computational logic and formal languages
    - Concurrency theory
    - Data structures and algorithms
  - Logic
  - Semantics and reasoning
- **Numerical and mathematical software and coding operations assert that a computation represents and approximates quantities accurately and recovers messages without error.**
  _basis: kinds, order: structure. Ordered from numerical accuracy to coding operations._
  - **Numerical and quantum computation asserts that a computation approximates mathematical quantities accurately or exploits quantum physical resources.**
    _basis: kinds, order: structure. Kinds of physical and numerical computation, listed by structure with no ranking._
    - Numerical computation and mathematical software
    - Quantum computation
    - Theory of computation not elsewhere classified
  - Mathematical software
  - **Coding operations are the processes that transform messages into code words and recover them again.**
    _basis: kinds, order: degree. Ranked from the general transformation steps to the specialized coding schemes._
    - Encoding
    - Decoding
    - Source coding
    - Error compensation
  - **Information-theoretic constructs describe the properties of a computation in terms of how information is transmitted and represented between sender and receiver.**
    _basis: kinds, order: structure. Ordered structurally from the transmission medium to the representation applied to messages._
    - Communication channels
    - Codes
- **Software engineering asserts that programs are specified, built, tested and maintained so that they behave as intended.**
  _basis: kinds, order: structure. Ordered from construction to assurance and recovery._
  - **Software construction asserts that programs are specified and organised through languages, requirements, architecture and notations.**
    _basis: kinds, order: structure. Ordered from requirements to notations and tools._
    - Requirements engineering
    - Software architecture
    - Programming languages
    - Software organization and properties
    - Software notations and tools
  - **Software assurance asserts that programs are checked, measured and managed so that their quality is demonstrated.**
    _basis: kinds, order: structure. Ordered from verification to empirical measurement and management._
    - **Correctness and assurance properties concern whether a computation meets its specification, as shown by formal proof, testing, verification and validation.**
      _basis: kinds, order: structure. Ordered by structure, from formal proof to testing and validation._
      - Formal methods for software
      - Software testing, verification and validation
      - Automated software engineering
    - Software quality, processes and metrics
    - Empirical software engineering
    - Software creation and management
  - **Software artefacts and recovery assert that programs as artefacts and the systems hosting them can be engineered and restored after failure.**
    _basis: kinds, order: structure. Ordered from artefact to discipline to restoration._
    - Software
    - Software engineering
    - System recovery

### 2. Cost is the property of how much time, energy, space or information a computation consumes, and how that consumption is measured and traded off.

- **Algorithmic and computational cost asserts how hard a computation is in principle and how it is designed to be efficient.**
  _basis: kinds, order: structure. Ordered from design to hardness._
  - Design and analysis of algorithms
  - Computational complexity and cryptography
  - Theory and algorithms for application domains
  - **Probabilistic and information-theoretic properties characterize a computation by its randomness, uncertainty and information content.**
    _basis: kinds, order: structure. Ordered by structure, from probability to information and random structures._
    - Probability and statistics
    - Information theory
    - Randomness, geometry and discrete structures
- **System performance asserts how fast, how parallel and how energy-frugal a running computation is, and how well it chooses among alternatives.**
  _basis: kinds, order: structure. Ordered from raw speed to hosting and choice._
  - **Performance-oriented fields assert that a computation runs fast, scales in parallel or uses little energy, and measure how well it does so.**
    _basis: kinds, order: degree. Ranked from the broadest speed-focused concern, high performance and parallelism, to the narrower concerns of energy use and measurement._
    - High performance computing
    - Concurrent/parallel systems and technologies
    - Energy-efficient computing
    - Performance evaluation
  - Virtual machine monitors
  - **Computations in this group are asserted to select a correct, feasible or best choice among alternatives.**
    _basis: kinds, order: structure. Ordered by structure, from choosing actions to solving constraints and optima._
    - Planning and decision making
    - Satisfiability and optimisation
  - **Computation is characterised by how efficiently and correctly it runs, in its performance, its tolerance of approximation, and its coordination of concurrent work.**
    _basis: kinds, order: structure. Ordered by structure, from performance to approximation and concurrency control._
    - Computer performance
    - Approximate computing
    - Concurrency control
    - Computer architecture
- **Information cost asserts how many symbols a message needs, measured by entropy, distance and rate-distortion limits and extended to coding in networks.**
  _basis: kinds, order: structure. Ordered from core measures to wider coding settings._
  - **Information measures and compression assert how much information a message carries and how far it can be compressed.**
    _basis: kinds, order: structure. Ordered from coding theory to measures to compression trade-offs._
    - **Coding and information theory asserts that a computation represents, compresses and transmits information reliably across noisy channels.**
      _basis: kinds, order: structure. Kinds of coding and communication topics, listed by structure with no ranking._
      - Coding, information theory and compression
      - Audio coding
      - Biological information theory
      - Channel coding
    - **Information measures are quantities that numerically characterize information content or the difference between code words.**
      _basis: kinds, order: degree. Ranked from the most fundamental information measures to code-word metrics._
      - Information entropy
      - Mutual information
      - Hamming distances
      - Hamming weight
    - **Compression and rate trade-off topics concern how much a signal can be compressed for a given level of allowed distortion.**
      _basis: kinds, order: degree. Ranked from the theoretical rate-distortion framework to its applied forms._
      - Rate distortion theory
      - Rate-distortion
      - Speech coding
  - **Information coding in networks and beyond asserts how information is carried across networks, living systems and user populations at some cost.**
    _basis: kinds, order: structure. Ordered from the general field to network coding to wider applications._
    - Information theory
    - Network coding
    - Technology acceptance model

### 3. Coordination is the property of how a computation works with other components, machines, agents and people through shared structure and interaction.

- **Networks and distributed execution assert that many machines cooperate through shared structures, rules and concurrent execution.**
  _basis: kinds, order: structure. Ordered from network structure to distributed execution._
  - **Network structure and rules assert how machines are connected and governed through architectures, protocols and substrates.**
    _basis: kinds, order: structure. Ordered from structure to rules to substrate._
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
  - **Distributed and concurrent execution asserts that many processes run together and coordinate reliably.**
    _basis: kinds, order: structure. Ordered from dependability to concurrency to execution regimes._
    - **Correctness-oriented fields assert that a computation behaves reliably and coordinates correctly across components, from dependable systems to distributed algorithms and the operating system layer.**
      _basis: kinds, order: structure. Ordered structurally from system-wide guarantees down to the operating system layer._
      - Dependable systems
      - Distributed systems and algorithms
      - Operating systems
    - **Parallel, concurrent and distributed methodologies are computation approaches defined by how work is split and coordinated across processes or machines.**
      _basis: kinds, order: structure. Ordered by structure of the coordination model._
      - Parallel computing methodologies
      - Distributed computing methodologies
      - Concurrent computing methodologies
      - Computing methodologies
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
- **Deployed platforms assert that computation is delivered across clouds, mobile devices, services and physical systems.**
  _basis: kinds, order: structure. Ordered from remote infrastructure to embedded devices._
  - **Service and cloud platforms assert that computation is delivered remotely as shared distributed services.**
    _basis: kinds, order: structure. Ordered from systems software to cloud to services._
    - Distributed computing and systems software
    - Cloud computing
    - Service oriented computing
  - **Mobile and cyber-physical platforms assert that computation is delivered over networks to portable and embedded devices.**
    _basis: kinds, order: structure. Ordered from communications to mobile to embedded devices._
    - Networking and communications
    - Mobile computing
    - Cyberphysical systems and internet of things
- **Agents and people assert that a computation interacts with other agents and users through robotics, interfaces and applications.**
  _basis: kinds, order: structure. Ordered from autonomous agents to human users._
  - **Autonomous agents assert that computations act and adapt on their own among other agents and the physical world.**
    _basis: kinds, order: structure. Ordered from agents to robots to adaptive systems._
    - Autonomous agents and multiagent systems
    - Intelligent robotics
    - Robotics
    - Artificial life and complex adaptive systems
    - Evolutionary computation
  - **Human-centred interaction asserts that a computation serves, supports and presents itself to the people who use it.**
    _basis: kinds, order: structure. Ordered from people to interaction to applications._
    - Human-centred computing
    - **Human-centred fields assert that a computation serves, understands or supports people, covering accessibility, emotion, collaboration and learning.**
      _basis: kinds, order: structure. Ordered structurally from individual users to groups and educational settings._
      - Accessible computing
      - Affective computing
      - Collaborative and social computing
      - Computing education
    - **Computation is characterised by how well it serves human users, through usable interaction, clear visual presentation, and interfaces that fit people.**
      _basis: kinds, order: structure. Ordered by structure, from general interaction to presentation and interface forms._
      - Human-computer interaction
      - Information visualisation
      - Computer interfaces
      - Human-centred computing not elsewhere classified
    - **Human-computer interaction concepts assert that a computation is shaped around how people use, design for, and gain access to it.**
      _basis: kinds, order: structure. Ordered from the broad field of HCI to the narrower concerns of interaction design and accessibility._
      - Human computer interaction (HCI)
      - Interaction design
      - Accessibility
    - **Application and presentation concepts assert that a computation serves a particular purpose, such as trading goods or making data visible.**
      _basis: kinds, order: structure. Ordered from commercial application to data presentation, with no ranking implied._
      - Electronic commerce
      - Visualization
  - **Applied computing and system organisation assert that computations are shaped around application areas and the organisation of systems.**
    _basis: kinds, order: structure. Ordered from application areas to system organisation to genetic communication._
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
    - Genetic communication
- **Media and creative computing asserts that a computation generates, transforms and presents content for human audiences.**
  _basis: kinds, order: structure. Ordered from creation to transformation._
  - **Creative and interactive media assert that a computation generates stories, games, sound and graphics for human experience.**
    _basis: kinds, order: structure. Ordered from creation to graphics and games._
    - **Creative media computing covers computations whose asserted property is generating or shaping stories, game content, and sound for human experience.**
      _basis: kinds, order: structure. Ordered structurally from narrative to generated content to audio media._
      - Interactive narrative
      - Procedural content generation
      - Sound and music computing
    - **Immersive and applied media computing asserts that a computation produces simulated or blended environments that serve a purpose beyond entertainment.**
      _basis: kinds, order: structure. Kinds of immersive and applied environments, listed by structure with no ranking._
      - Serious games
      - Virtual and mixed reality
      - Graphics, augmented reality and games not elsewhere classified
    - Graphics, augmented reality and games
    - Computer aided design
    - Computer graphics
  - **Media transformation asserts that a computation models, simulates and converts content across modalities.**
    _basis: kinds, order: structure. Ordered from modelling to modality conversion._
    - **Modeling, simulation, graphics and symbolic manipulation are methodologies that represent or transform systems and mathematical objects computationally.**
      _basis: kinds, order: structure. Ordered by structure of what is represented._
      - Modeling and simulation
      - Modelling and simulation
      - Computer graphics
      - Symbolic and algebraic manipulation
    - **Media transformation computations are defined by the property of processing, compressing or synthesising audio, image and video signals.**
      _basis: kinds, order: structure. Kinds of media signal computation, listed in no ranked order._
      - Audio processing
      - Image and video coding
      - Image processing
      - Video processing
    - Multimodal analysis and synthesis
    - Entertainment and gaming

### 4. Learning is the property that a computation improves or exhibits intelligent behaviour from data, experience and reasoning rather than fixed rules.

- **Machine learning asserts that behaviour is acquired from data under supervised, unsupervised, reinforcement and adversarial regimes.**
  _basis: kinds, order: structure. Ordered from general learning to specific regimes._
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
  - **Neural network approaches are kinds of computation built from layered networks of interconnected artificial units.**
    _basis: kinds, order: structure. Ordered structurally from general networks to deep architectures._
    - Deep learning
    - Neural networks
    - Neural networks
- **Perception and pattern learning asserts that a computation interprets language, images and signals by recognising patterns in them.**
  _basis: kinds, order: structure. Ordered from language and vision to patterns and data._
  - **Language and visual perception assert that a computation interprets human language, scenes and images.**
    _basis: kinds, order: structure. Ordered from language to vision._
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
    - Image processing
    - Pattern recognition
  - **Probabilistic and data inference asserts that a computation draws conclusions from uncertain and structured data.**
    _basis: kinds, order: structure. Ordered from probability to data._
    - Probabilistic computing
    - Data systems
- **Artificial and computational intelligence asserts that a computation reasons, evolves and develops intelligently.**
  _basis: kinds, order: structure. Ordered from general intelligence to specific techniques._
  - **Intelligence fields are kinds of computation judged by whether they exhibit intelligent, reasoned, or self-developing behavior.**
    _basis: kinds, order: structure. Ordered structurally from the umbrella field to its specific branches._
    - Computational and artificial intelligence
    - Artificial intelligence
    - Computational intelligence
    - Machine intelligence
  - **Foundational areas of computational intelligence are kinds of study that assert formal reasoning or developmental growth as the property of a computation.**
    _basis: kinds, order: structure. Ordered by structure, from formal reasoning to developmental processes._
    - Logic
    - Autonomous mental development
  - Artificial intelligence
  - Knowledge representation and reasoning
  - Fuzzy computation

### 5. Protection is the property that a computation resists attack, keeps information confidential and can be trusted by the people it affects.

- **Formal and data-centred protection asserts provable secrecy, integrity and privacy of information handled by a computation.**
  _basis: kinds, order: structure. Ordered from the overall domain to proofs to data._
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
- **System protection asserts that hardware, software and networks resist attack and fail detectably.**
  _basis: kinds, order: structure. Ordered from single layers to whole systems._
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
- **Human and policy protection asserts that people, regulation and trust properties such as fairness and oversight constrain a computation.**
  _basis: kinds, order: structure. Ordered from social to trust constraints._
  - **Human, social and policy dimensions assert how people, professions and regulation shape and constrain secure computation.**
    _basis: kinds, order: structure. Ordered by structure from the individual user to the profession, society and policy._
    - User characteristics
    - Human and societal aspects of security and privacy
    - Social and professional topics
    - Professional topics
    - Computing / technology policy
  - **Computer systems are judged by the trust properties asserted of them, such as fairness, ethics, security, and human oversight of automated decisions.**
    _basis: kinds, order: structure. Ordered by structure, from ethical trust properties to security and oversight._
    - Fairness, accountability, transparency, trust and ethics of computer systems
    - Computer security
    - Mixed initiative and human-in-the-loop

## Checks

- minto_check: clean
- field_check holds: True — Worst misplacements: P2.2.2 Virtual machine monitors, P2.1.2 cryptography, P2.3.2.3 Technology acceptance model, P3.2.2.1 Networking, P3.3.1.5 Evolutionary computation, P5.3.2.3 Mixed initiative, P4.2.2.2 Data systems.
