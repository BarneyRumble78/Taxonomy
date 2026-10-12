# CS — top-down Minto pyramid

Built by scripts/minto_pass.py from the grouped classification. Three rules (Minto pp. 9-11): each summary states the idea of its group, members are the same kind of idea, and they are in a stated order.

## Introduction

**Situation.** Computing produces computations that people build, run, connect and rely on in many settings.

**Complication.** Computing knowledge is catalogued by many overlapping schemes, so topics are scattered, duplicated and mixed with residual headings.

**Question.** How is everything in computer science divided by what is asserted of a computation?

**Answer.** Computer science divides by the property asserted of a computation, ordered from the single program outward to many agents and adversaries: correctness, cost, coordination, learning, and protection.

## Governing thought

Computer science divides by the property asserted of a computation, ordered from the single program outward to many agents and adversaries: correctness, cost, coordination, learning, and protection.

## Key line

Group of properties. Basis: kinds. Dimension: the property asserted of a computation. Order: structure. The pillars run from the single program outward to many agents and adversaries.

1. Correctness is the property that a computation does what its specification, formal model or mathematical foundation says it should. `CS.K1`
2. Cost is the property of how much time, energy, information capacity or algorithmic effort a computation requires. `CS.K2`
3. Coordination is the property of how a computation cooperates with other components, machines, networks and people. `CS.K3`
4. Learning is the property that a computation improves its behaviour, reasons or acts intelligently from data and experience. `CS.K4`
5. Protection is the property that a computation and its data resist attack, misuse and failure. `CS.K5`

## Groups

### 1. Correctness is the property that a computation does what its specification, formal model or mathematical foundation says it should.

- **Software construction asserts that a program is well built, from its notations and structure to the processes and quality measures that govern it.**
  _basis: kinds, order: structure. From the artefact itself to the process that produces it._
  - **Notations and structure assert that a program is written in suitable languages, tools and architectures.**
    _basis: kinds, order: structure. From organisation of software to the notations used to write it._
    - Software organization and properties
    - Software notations and tools
    - Programming languages
    - Software architecture
  - **Process and quality assert that software is created, managed and measured so that it meets its requirements.**
    _basis: kinds, order: structure. From requirements through management to quality and empirical study._
    - Software creation and management
    - Requirements engineering
    - Software quality, processes and metrics
    - Empirical software engineering
  - **General and residual software topics assert correctness of programs as artefacts, their hosting layers and recovery after failure.**
    _basis: kinds, order: structure. From the program artefact to the residual engineering topics._
    - **Software-oriented concepts characterize a computation by the program artifact, its engineering discipline, its hosting layer, or its restoration after failure.**
      _basis: kinds, order: structure. Ordered by structure, from the software artifact to its engineering, hosting and recovery._
      - Software
      - Software engineering
      - Virtual machine monitors
      - System recovery
    - Software engineering not elsewhere classified
- **Formal and mathematical foundations assert that a computation has provable properties defined by models, logic and mathematics.**
  _basis: kinds, order: structure. From general mathematics to specific formal models and reasoning._
  - **Mathematical and model foundations assert that a computation rests on discrete, continuous and formal models of what it can do.**
    _basis: kinds, order: structure. From general mathematics to formal models._
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
    - Mathematical software
  - **Logic and theoretical guarantees assert that a computation has provable, reasoned or approximable properties.**
    _basis: kinds, order: structure. From logic and semantics to broader theoretical fields._
    - Logic
    - Semantics and reasoning
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
- **Dependability, assurance and reference topics assert that a computation behaves reliably, is verified, and is documented with common tools.**
  _basis: kinds, order: structure. From general reference material to verification and dependable operation._
  - **Correctness-oriented fields assert that a computation behaves reliably and coordinates correctly across components, from dependable systems to distributed algorithms and the operating system layer.**
    _basis: kinds, order: structure. Ordered structurally from system-wide guarantees down to the operating system layer._
    - Dependable systems
    - Distributed systems and algorithms
    - Operating systems
  - **Correctness and assurance properties concern whether a computation meets its specification, as shown by formal proof, testing, verification and validation.**
    _basis: kinds, order: structure. Ordered by structure, from formal proof to testing and validation._
    - Formal methods for software
    - Software testing, verification and validation
    - Automated software engineering
  - General and reference
  - Document types
  - Cross-computing tools and techniques

### 2. Cost is the property of how much time, energy, information capacity or algorithmic effort a computation requires.

- **Algorithmic and execution cost asserts how efficiently a computation runs, scales and uses energy.**
  _basis: kinds, order: structure. From algorithm design to measured system performance._
  - **Algorithmic cost asserts the effort an algorithm needs, as studied in design, complexity and domain-specific theory.**
    _basis: kinds, order: structure. From general design to complexity and applied theory._
    - Design and analysis of algorithms
    - Computational complexity and cryptography
    - Theory and algorithms for application domains
  - **Execution cost asserts how fast, how parallel and how energy-hungry a running computation is.**
    _basis: kinds, order: structure. From performance fields to execution regimes and residual topics._
    - **Performance-oriented fields assert that a computation runs fast, scales in parallel or uses little energy, and measure how well it does so.**
      _basis: kinds, order: degree. Ranked from the broadest speed-focused concern, high performance and parallelism, to the narrower concerns of energy use and measurement._
      - High performance computing
      - Concurrent/parallel systems and technologies
      - Energy-efficient computing
      - Performance evaluation
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
    - Other information and computing sciences
- **Information cost asserts how much information a computation carries, compresses and transmits across a channel.**
  _basis: kinds, order: structure. From general measures to operations and compression trade-offs._
  - **Information properties and measures characterise a computation by its randomness, uncertainty and information content.**
    _basis: kinds, order: structure. From general properties to numerical measures._
    - **Probabilistic and information-theoretic properties characterize a computation by its randomness, uncertainty and information content.**
      _basis: kinds, order: structure. Ordered by structure, from probability to information and random structures._
      - Probability and statistics
      - Information theory
      - Randomness, geometry and discrete structures
    - **Information-theoretic constructs describe the properties of a computation in terms of how information is transmitted and represented between sender and receiver.**
      _basis: kinds, order: structure. Ordered structurally from the transmission medium to the representation applied to messages._
      - Communication channels
      - Codes
    - **Information measures are quantities that numerically characterize information content or the difference between code words.**
      _basis: kinds, order: degree. Ranked from the most fundamental information measures to code-word metrics._
      - Information entropy
      - Mutual information
      - Hamming distances
      - Hamming weight
  - **Coding operations and trade-offs assert how messages are encoded, compressed and recovered within rate limits.**
    _basis: kinds, order: structure. From coding operations to compression trade-offs and wider context._
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
- **Media and graphics computation asserts that a computation transforms or generates images, sound, games and virtual environments at some processing cost.**
  _basis: kinds, order: structure. From processing signals to creating immersive experiences._
  - **Media creation and graphics assert that a computation generates stories, sound, games and designed images.**
    _basis: kinds, order: structure. From creative media to graphics and design._
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
    - Computer aided design
    - Computer graphics
    - Entertainment and gaming
  - **Perception and transformation assert that a computation interprets and transforms visual, linguistic and sensed content.**
    _basis: kinds, order: structure. From content kinds to methodologies and perception._
    - **A computation is characterized by the nature of the content it transforms or the inference it draws, whether visual data, recognized patterns, probabilistic reasoning, or structured data.**
      _basis: kinds, order: structure. Ordered from raw signal handling to uncertain reasoning._
      - Image processing
      - Pattern recognition
      - Probabilistic computing
      - Data systems
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
    - Computer vision and multimedia computation not elsewhere classified
    - Multimodal analysis and synthesis

### 3. Coordination is the property of how a computation cooperates with other components, machines, networks and people.

- **Network and distributed coordination asserts that computations communicate and cooperate across networks and systems.**
  _basis: kinds, order: structure. From network structure and rules to distributed services._
  - **Network structure and rules assert how networks are built and governed so computations can communicate.**
    _basis: kinds, order: structure. From overall substrate to structural parts and governing rules._
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
    - Networking and communications
  - **Distributed and service platforms assert that computations cooperate across machines, clouds, mobile devices and physical systems.**
    _basis: kinds, order: structure. From distributed systems to cloud, services and embedded devices._
    - Distributed computing and systems software
    - Cloud computing
    - Service oriented computing
    - Mobile computing
    - Cyberphysical systems and internet of things
- **Human and application coordination asserts that a computation is shaped around the people who use it and the purposes it serves.**
  _basis: kinds, order: structure. From general application areas to the people who use them._
  - **Application and systems areas assert that a computation serves particular purposes within organised systems.**
    _basis: kinds, order: structure. From general headings to specific purposes._
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
    - **Application and presentation concepts assert that a computation serves a particular purpose, such as trading goods or making data visible.**
      _basis: kinds, order: structure. Ordered from commercial application to data presentation, with no ranking implied._
      - Electronic commerce
      - Visualization
    - Applied computing not elsewhere classified
  - **Human-centred and trust concerns assert that a computation supports, is usable by and is trusted by people.**
    _basis: kinds, order: structure. From interaction to trust._
    - **Human-computer interaction concepts assert that a computation is shaped around how people use, design for, and gain access to it.**
      _basis: kinds, order: structure. Ordered from the broad field of HCI to the narrower concerns of interaction design and accessibility._
      - Human computer interaction (HCI)
      - Interaction design
      - Accessibility
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
    - Human-centred computing

### 4. Learning is the property that a computation improves its behaviour, reasons or acts intelligently from data and experience.

- **Machine learning asserts that a computation acquires behaviour from data through learning and neural methods.**
  _basis: kinds, order: structure. From general learning to specific neural and paradigm approaches._
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
- **Intelligence and decision making assert that a computation reasons, plans and acts intelligently.**
  _basis: kinds, order: structure. From general intelligence to specific reasoning and action methods._
  - **General intelligence fields assert that a computation exhibits reasoned or self-developing intelligent behaviour.**
    _basis: kinds, order: structure. From broad fields to foundational areas._
    - **Foundational areas of computational intelligence are kinds of study that assert formal reasoning or developmental growth as the property of a computation.**
      _basis: kinds, order: structure. Ordered by structure, from formal reasoning to developmental processes._
      - Logic
      - Autonomous mental development
    - **Intelligence fields are kinds of computation judged by whether they exhibit intelligent, reasoned, or self-developing behavior.**
      _basis: kinds, order: structure. Ordered structurally from the umbrella field to its specific branches._
      - Computational and artificial intelligence
      - Artificial intelligence
      - Computational intelligence
      - Machine intelligence
    - Artificial intelligence
    - Artificial intelligence not elsewhere classified
  - **Reasoning and choice assert that a computation represents knowledge and selects the best option among alternatives.**
    _basis: kinds, order: structure. From choice to representation and fuzziness._
    - **Computations in this group are asserted to select a correct, feasible or best choice among alternatives.**
      _basis: kinds, order: structure. Ordered by structure, from choosing actions to solving constraints and optima._
      - Planning and decision making
      - Satisfiability and optimisation
    - Knowledge representation and reasoning
    - Fuzzy computation
  - **Adaptive and embodied intelligence assert that a computation evolves, acts as an agent or controls robots.**
    _basis: kinds, order: structure. From adaptive populations to agents and robots._
    - Artificial life and complex adaptive systems
    - Autonomous agents and multiagent systems
    - Evolutionary computation
    - Intelligent robotics
    - Robotics

### 5. Protection is the property that a computation and its data resist attack, misuse and failure.

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

- minto_check: clean
- field_check holds: False — P1.3 is a catch-all mixing dependability with General/reference/Document types; P2.3 media/graphics and P3.2 application/human areas are topics, not cost or coordination properties.
