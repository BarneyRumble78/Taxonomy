# PH — Physics

Standard v2 cited, not copied. Diagnosis: audit_physics_chemistry.md (29 of 74 checks flagged). v1 source: twelve.txt 229–1181. Theorems are owned by MA and cited as "uses MA.…". Phase 2.2 deepening: every A-cell now has its own SCQA, a second key line, and named objects with hypotheses.

## 1. SCQA
**Situation.** Physics states laws of matter, energy, space and time. Each law holds within a regime set by which constants matter: the speed of light c, Planck's constant ħ, Newton's constant G, and the number of interacting bodies N.
**Complication.** v1 called its grid "the Bronstein cube". It named eight vertices but used four families. It had no home for transport, plasma, fluids or radiation in matter. It counted heuristics as a sixth method. The audit flagged 29 of 74 fact checks, including the Clapeyron and Clausius–Clapeyron confusion, quasiparticle lifetime against rate, and a missing k_B in the black-hole entropy.
**Question.** Into which regimes does every physical claim fall, so that each law has one home and each empty vertex is filled or refused?
**Answer.** Five regimes, read off an adaptation of the c–G–ħ cube of theories plus an N axis that is the author's own addition. The standard cube does not contain N.

## 2. Governing thought
Physics is exhausted by four faces of one pyramid: objects, methods, warrants and bridges.
Its objects divide into five regimes: classical motion and fields, quantum systems, gravitation and the cosmos, matter in equilibrium, and matter out of equilibrium.

## 3. Key line
Dimension: **the governing constants of the claim** (which of c, ħ, G and N set its scale). Logic inductive. Order: structural, from fewest constants to most, then the N axis.
1. Classical motion and fields
2. Quantum systems
3. Gravitation and the cosmos
4. Matter in equilibrium
5. Matter out of equilibrium

**Cube map.** This is an adaptation of the c–G–ħ cube of physical theories. It is not Bronstein's 1933 scheme, and the attribution of the cube's modern form is left open (UNVERIFIED). N is the author's axis.

| Vertex | Theory | Home |
|---|---|---|
| none | Newtonian mechanics | PH.O.A1.1 |
| c | special relativity; Maxwell electrodynamics | PH.O.A1.2–A1.3 |
| ħ | non-relativistic quantum mechanics | PH.O.A2.1 |
| c, ħ | quantum field theory | PH.O.A2.3 |
| G | Newtonian gravity | PH.O.A3.1 |
| c, G | general relativity | PH.O.A3.2 |
| G, ħ | no established theory | REFUSED as a cell. Such claims go to PH.O.A3.5, OPEN |
| c, G, ħ | quantum gravity | PH.O.A3.5, OPEN |
| N, equilibrium | thermodynamics, statistical mechanics, condensed matter | PH.O.A4 |
| N, driven or relaxing | transport, fluids, plasma, radiation in matter, nonlinear dynamics | PH.O.A5 |

**MECE test.** Exclusive: each claim is placed by the largest set of constants its derivation needs. Exhaustive: every vertex of the cube, and both states of the N axis, has a home or a stated refusal.
**CONTESTED.** Newtonian gravity is placed in A3, not A1, so all gravitation shares one home. The alternative files it in A1 by the "no c, no ħ" rule.

## 4. Face O — Objects

### PH.O.A1 Classical motion and fields
**SCQA.** Situation. Bodies and fields move by deterministic laws when ħ and G are negligible. Classical physics remains the working physics of engineering and much of astronomy. Complication. Each law holds only inside stated limits: speeds below c for mechanics, and actions much larger than ħ throughout. Special relativity and Noether's theorem also cross into other cells, and engineering claims often cite them without their limits. Question. Which classical laws does physics own, and within what limits does each hold? Answer. Physics owns the laws of bodies, fields, spacetime symmetry and continua in the classical regime. Mathematics owns the theorems about their equations, and engineering owns the artefacts that use them.

**Key line** (inductive; plural noun: classical laws; dimension: the entity or structure the law governs; order: structural, from one body to extended media). Members (5): Particle mechanics · Classical fields · Special relativity · Symmetry and conservation · Continuum mechanics.

- **PH.O.A1.1 Particle mechanics. Newton's laws hold in inertial frames for speeds much below c.** They fail near c (A1.3) and for actions near ħ (A2). In a non-inertial frame, fictitious forces must be added. Trajectories are unique given initial data only where the forces satisfy a Lipschitz condition (uses MA.O.A4).
  - PH.O.A1.1.1 Lagrangian and Hamiltonian mechanics are equivalent where the Legendre transform is regular.
  - PH.O.A1.1.2 Liouville's theorem: Hamiltonian flow preserves phase-space volume. The theorem is MA.O.A4; its physical use is here.
  - PH.O.A1.1.3 Rigid-body motion, oscillators and small vibrations.
- **PH.O.A1.2 Classical fields. Maxwell's equations govern electromagnetic fields in vacuum, and in linear media given constitutive relations.** The Lorentz force law couples the fields to charges and is a separate postulate. The classical description fails where single-photon effects matter.
  - PH.O.A1.2.1 Electrostatics and magnetostatics, including the quasistatic circuit laws (Kirchhoff) as the limit of slow change.
  - PH.O.A1.2.2 Electromagnetic waves; c is the propagation speed in vacuum.
  - PH.O.A1.2.3 Classical optics: geometric optics in the short-wavelength limit; diffraction and interference.
- **PH.O.A1.3 Special relativity. The laws take the same form in all inertial frames, and c is frame-invariant.** The theory holds where gravity is negligible, that is, in flat spacetime. Where G matters, the claim moves to A3.2. Time dilation is measured with the lifetimes of fast muons and with atomic clocks (W4).
  - PH.O.A1.3.1 Lorentz transformations; time dilation; length contraction.
  - PH.O.A1.3.2 Mass–energy equivalence, E = mc² for a body at rest.
- **PH.O.A1.4 Symmetry and conservation. Noether: each continuous symmetry of a local action yields a conserved current.** The theorem is MA (uses MA.O.A4); the physical conservation law is PH. A conservation law holds for the closed system. A driven subsystem, with explicit time dependence in its action, does not conserve energy.
  - PH.O.A1.4.1 Energy, momentum and angular momentum from time, space and rotation symmetry.
  - PH.O.A1.4.2 Charge conservation from the gauge symmetry of electrodynamics.
- **PH.O.A1.5 Continuum mechanics. Solids and fluids are treated as continua where the medium is smooth on the scale of interest.** Cauchy stress gives traction t = σᵀn. The continuum hypothesis fails when grain size or the molecular mean free path approaches the length of interest.
  - PH.O.A1.5.1 Linear elasticity: Hooke's law for small strain in a linear elastic solid.
  - PH.O.A1.5.2 Constitutive laws close the balance equations. The artefact meeting a specification is EN.

Named objects: Newton's laws (inertial frame; v ≪ c; action ≫ ħ). Hamilton's equations (regular Legendre transform). Liouville's theorem (Hamiltonian flow; no dissipation or scattering). Maxwell's equations (classical fields; constitutive relations in media). Kirchhoff's circuit laws (lumped elements; slow change). Lorentz transformation (inertial frames; constant c). Noether's theorem (local action; continuous symmetry; equations of motion hold). Cauchy stress (continuum hypothesis). Hooke's law (small strain; linear elastic solid).

### PH.O.A2 Quantum systems
**SCQA.** Situation. When action is comparable to ħ, states superpose and measurement yields statistics, not trajectories. Quantum theory is the most precisely tested theory in physics. Complication. Its interpretation is disputed. Some quantum claims are shared with other fields: entanglement protocols with CS, the chemical bond with CH, and meaning with PL. Question. What is claimed, and what is left to philosophy? Answer. Physics owns the formalism, its measured predictions, the particle and field content, and atomic and optical systems. PL owns the arguments about what the formalism means.

**Key line** (inductive; plural noun: quantum claims; dimension: the aspect of a quantum system that the claim concerns; order: formal structure, correlation, relativistic content, applications, then meaning). Members (5): States and dynamics · Non-locality · Quantum fields and particles · Atomic, molecular and optical physics · Interpretation of quantum mechanics.

- **PH.O.A2.1 States and dynamics. A closed system's state evolves unitarily by the Schrödinger equation.** The Born rule gives outcome probabilities. Both are stated here for non-relativistic systems, and the Born rule needs a stated measurement basis. An open system evolves non-unitarily, which is the setting of decoherence.
  - PH.O.A2.1.1 The uncertainty relation σ_x σ_p ≥ ħ/2 holds for any state (the theorem is MA.O.A2, as operator algebra).
  - PH.O.A2.1.2 Decoherence: interaction with an environment suppresses interference in a preferred basis. It does not by itself select a single outcome.
  - PH.O.A2.1.3 Tunnelling and bound states.
- **PH.O.A2.2 Non-locality. Bell: any local hidden-variable theory with measurement independence obeys the CHSH bound S ≤ 2.** Quantum mechanics reaches 2√2 (the Tsirelson bound). Loophole-free violations were reported in 2015 (Delft, Vienna, NIST). The result excludes local hidden-variable models, not quantum mechanics. Superdeterminism denies measurement independence and is CONTESTED (the argument is PL).
  - PH.O.A2.2.1 Entanglement as a resource: teleportation, quantum key distribution. Deployed protocols are CS.O.A5.
  - PH.O.A2.2.2 No-signalling: entanglement cannot transmit information faster than light.
- **PH.O.A2.3 Quantum fields and particles. The Standard Model describes three of the four known interactions, with gauge group SU(3)×SU(2)×U(1).** It omits gravity, and in its minimal form it omits neutrino masses and dark matter. The Standard Model prediction for the muon anomalous magnetic moment depends on how the hadronic contribution is computed. The agreement with measurement is CONTESTED (UNVERIFIED as to the latest result).
  - PH.O.A2.3.1 Spin–statistics and CPT hold for local, Lorentz-invariant quantum field theories with energy bounded below.
  - PH.O.A2.3.2 The Higgs boson was observed in 2012 (ATLAS and CMS).
  - PH.O.A2.3.3 Neutrino oscillation implies non-zero neutrino masses. The mass ordering is OPEN.
  - PH.O.A2.3.5 Nuclear structure and decay: half-lives are measured constants (W4), e.g. the ¹⁴C half-life of 5,730 ± 40 years. Radiometric ages built on them are EA.
  - PH.O.A2.3.4 Renormalisation: physics at low energy is insensitive to most details at high energy, for renormalisable theories and effective field theories.
- **PH.O.A2.4 Atomic, molecular and optical physics. Atomic level structure and spectra are measured and computed here, and light–atom interaction follows from them.** The chemical bond is CH; PH owns the level structure. Spectral lines are the main evidence, and their widths set the precision of the clocks below.
  - PH.O.A2.4.1 Lasers: stimulated emission in a medium with population inversion.
  - PH.O.A2.4.2 Laser cooling and Bose–Einstein condensation of dilute gases (first achieved 1995).
  - PH.O.A2.4.3 Atomic clocks and precision measurement. The SI second has been defined by the caesium-133 hyperfine transition since 1967.
- **PH.O.A2.5 Interpretation of quantum mechanics. The empirical content of quantum mechanics is placed here, and the interpretive arguments are placed in PL.** CONTESTED placement. The empirical content stays here. Copenhagen, many-worlds, pilot-wave and collapse theories, as arguments, are PL.
  - PH.O.A2.5.1 Interpretations that add no new dynamics (Copenhagen, many-worlds, pilot-wave) predict the same outcome statistics as unitary quantum mechanics. This holds for non-relativistic systems. No experiment to date separates them, so the choice among them is argument (PL).
  - PH.O.A2.5.2 Collapse models (GRW, continuous spontaneous localisation) add a stochastic term with a free strength parameter. Experiments have bounded that parameter from above (W4). The current excluded range is UNVERIFIED.
  - PH.O.A2.5.3 Matter-wave interference has been shown for molecules of order 10⁴ atomic mass units. This tests unitary evolution at that size, not any one interpretation. The largest mass reached to date is UNVERIFIED.

Named objects: Schrödinger equation (non-relativistic; closed system). Born rule (state in a Hilbert space; stated measurement basis). Heisenberg–Robertson uncertainty relation (any state; observables with finite variance). Decoherence (system–environment interaction; preferred basis). Bell–CHSH inequality (local hidden variables; measurement independence; two settings per party). Tsirelson bound (quantum correlations in the CHSH scenario). Spin–statistics and CPT theorems (local, Lorentz-invariant quantum field theory; energy bounded below). Standard Model (renormalisable gauge theory with the stated group). Renormalisation group (separation of scales). Two-level model with the rotating-wave approximation (near-resonant drive; weak coupling; other levels far detuned). Doppler cooling (closed cycling transition; light tuned below resonance). Radioactive decay law (constant decay probability per nucleus; independent decays).

### PH.O.A3 Gravitation and the cosmos
**SCQA.** Situation. Where G matters, gravity shapes motion, and at high mass or speed it shapes spacetime itself. The cosmos is the only laboratory at the largest scales. Complication. Newtonian gravity is placed here by choice (CONTESTED). Cosmological claims rest on model-dependent inference, and the corner where c, G and ħ all matter has no tested theory. Question. What is claimed, and what is still open? Answer. Physics owns gravitation from the weak-field law to general relativity. It also owns the astrophysical and cosmological claims drawn from it, and one OPEN cell for quantum gravity.

**Key line** (inductive; plural noun: gravitational claims; dimension: the field strength and scale at which gravity is claimed to act; order: weak field, strong field, bodies, the whole universe, the quantum limit). Members (5): Newtonian gravity · General relativity · Astrophysics · Cosmology · Quantum gravity.

- **PH.O.A3.1 Newtonian gravity. The inverse-square attraction is valid for weak fields and speeds much below c.** Its first failure in the solar system is the anomalous precession of Mercury's perihelion (A3.2.1). The cell is placed here, not in A1 (CONTESTED, section 3).
  - PH.O.A3.1.1 Kepler's laws follow for two point masses.
  - PH.O.A3.1.2 Celestial mechanics: perturbation theory for many bodies. The n-body problem's mathematics is MA.O.A4.
- **PH.O.A3.2 General relativity. Einstein's field equations relate spacetime curvature to stress-energy, and the equivalence principle holds locally.** Exact solutions need symmetry assumptions. The theory is tested by solar-system measurements, binary-pulsar timing and gravitational-wave signals. Strong-field tests are fewer. Whether it holds on cosmological scales without dark components is OPEN (A3.4.3).
  - PH.O.A3.2.1 Classical tests: Mercury's perihelion, light deflection, gravitational redshift.
  - PH.O.A3.2.2 Black holes: the Schwarzschild and Kerr solutions. Singularity theorems (Penrose, Hawking) assume energy conditions and trapped surfaces (uses MA.O.A3).
  - PH.O.A3.2.3 Gravitational waves: first detected 14 September 2015, announced February 2016 (LIGO).
- **PH.O.A3.3 Astrophysics. Stars, compact objects and galaxies are described by gravity with equations of state, nuclear reactions and radiative transfer.** Stellar structure is a model solved under spherical symmetry and equilibrium. The interior is observed only indirectly, through oscillations and neutrinos.
  - PH.O.A3.3.1 Stellar structure and nucleosynthesis.
  - PH.O.A3.3.2 The Chandrasekhar limit: about 1.4 solar masses for a non-rotating white dwarf supported by electron degeneracy pressure.
  - PH.O.A3.3.3 Neutron stars, pulsars, accretion.
- **PH.O.A3.4 Cosmology. ΛCDM fits the expansion history, the cosmic microwave background and large-scale structure.** The model assumes general relativity, large-scale homogeneity and isotropy, cold dark matter and a cosmological constant. Fit quality is judged by agreement of parameters across probes. The Hubble tension currently strains that agreement.
  - PH.O.A3.4.1 Hubble–Lemaître expansion. The "Hubble tension" between early- and late-universe measurements is OPEN.
  - PH.O.A3.4.2 The CMB, discovered 1965.
  - PH.O.A3.4.3 Dark matter and dark energy: inferred from gravity; their identities are OPEN.
  - PH.O.A3.4.4 Inflation: a CONTESTED programme with supporting but not decisive evidence.
- **PH.O.A3.5 Quantum gravity. No tested theory combines c, G and ħ, and the cell is OPEN.** Claims here carry W1 only (section 6). The semiclassical results below have wide agreement. They rest on quantum fields on a fixed curved background, not on a quantum theory of gravity.
  - PH.O.A3.5.1 Bekenstein–Hawking entropy S = k_B c³ A / (4Għ) for a black hole of horizon area A. (The v1 omission of k_B is fixed.)
  - PH.O.A3.5.2 Hawking radiation: a semiclassical prediction (quantum fields on a curved background), not yet observed for astrophysical black holes.
  - PH.O.A3.5.3 Programmes: string theory, loop quantum gravity, asymptotic safety. All lack decisive empirical tests.

Named objects: Newton's law of gravitation (weak field; v ≪ c). Kepler's laws (two point masses; bound orbit). Equivalence principle (local; free fall independent of composition). Einstein field equations (general relativity; specified stress-energy). Schwarzschild solution (spherical symmetry; vacuum; no rotation or charge). Kerr solution (stationary and axisymmetric; vacuum; no charge). Birkhoff's theorem (spherical symmetry; vacuum exterior). Singularity theorems (energy conditions; trapped surfaces). Chandrasekhar limit (non-rotating white dwarf; electron degeneracy pressure). Virial theorem (bound system in equilibrium). Jeans criterion (uniform static medium). Friedmann equations (general relativity; homogeneity and isotropy). ΛCDM (the assumptions in A3.4). Standard candles (calibrated luminosity; absorption corrected). Bekenstein–Hawking entropy (black hole horizon area A). Hawking radiation (quantum fields on a fixed curved background).

### PH.O.A4 Matter in equilibrium
**SCQA.** Situation. Many bodies at equilibrium show laws that no single body shows: temperature, phases, rigidity. Equilibrium is an idealisation, but a very good one for most matter at rest. Complication. The idealisation fails for glasses, driven systems and small systems, and the ergodic justification of statistical mechanics is CONTESTED. Free energy and the ground state are also claimed by chemistry. Question. What is claimed? Answer. Physics owns the laws of thermodynamics, their statistical derivation, the classification of phase change, and the physics of ordered and quantum condensed states. CH owns reaction thermochemistry (uses CH.O.A3).

**Key line** (inductive; plural noun: equilibrium laws and models; dimension: the level of description of a many-body equilibrium; order: macroscopic law, microscopic derivation, collective change, material states). Members (4): Thermodynamics · Statistical mechanics · Phase transitions · Condensed states.

- **PH.O.A4.1 Thermodynamics. Macroscopic equilibrium states obey the zeroth, first, second and third laws without reference to microscopic structure.** The zeroth law defines temperature. The laws are stated for closed or isolated systems at equilibrium. Engine and cycle design is EN.O.A3, which cites this cell.
  - PH.O.A4.1.1 First law: the change in internal energy of a closed system equals heat in minus work out (sign convention stated).
  - PH.O.A4.1.2 Second law: the entropy of an isolated system does not decrease. Carnot efficiency 1 − T_c/T_h bounds any engine between two reservoirs.
  - PH.O.A4.1.3 Third law: entropy approaches a constant as T → 0, for systems with a non-degenerate ground state.
- **PH.O.A4.2 Statistical mechanics. Ensembles derive thermodynamics from microstates.** The microcanonical ensemble assumes equilibrium and equal a priori probability. The canonical ensemble assumes weak coupling to a heat bath at fixed temperature. Ensembles can disagree for systems with long-range interactions.
  - PH.O.A4.2.1 Boltzmann entropy S = k_B ln W.
  - PH.O.A4.2.2 Quantum statistics: Fermi–Dirac and Bose–Einstein distributions for indistinguishable particles.
  - PH.O.A4.2.3 Ergodic hypothesis: CONTESTED as a justification. The ergodic theorems are MA.O.A4.
- **PH.O.A4.3 Phase transitions. Coexistence lines and critical points follow from equilibrium conditions on the free energy.** Transitions are first order, with latent heat, or continuous, with a diverging correlation length. A sharp transition requires the thermodynamic limit, so finite systems show rounded transitions.
  - PH.O.A4.3.1 Clapeyron equation: dP/dT = L/(T Δv) on a coexistence line.
  - PH.O.A4.3.2 Clausius–Clapeyron: d ln P/dT = L/(RT²). It adds an ideal vapour, negligible condensed-phase volume and constant L. (The v1 mislabel is fixed.)
  - PH.O.A4.3.3 Critical phenomena and universality: systems with the same dimension, symmetry and interaction range share critical exponents. Renormalisation-group explanation (Wilson).
  - PH.O.A4.3.4 Mermin–Wagner: no spontaneous breaking of a continuous symmetry at T > 0 in d ≤ 2 with short-range interactions.
- **PH.O.A4.4 Condensed states. Band structure, superconductivity, magnetism, topological phases and defects are measured properties of ordered matter.** Independent-electron band theory explains many properties. Strongly correlated materials are the main exception. Device design on semiconductors is EN.O.A4.
  - PH.O.A4.4.1 Quasiparticles: an excitation with decay rate Γ = 1/τ is well defined when ħΓ is much less than its energy. (The v1 lifetime–rate confusion is fixed.)
  - PH.O.A4.4.2 BCS theory of conventional superconductivity: electron pairing mediated by phonons, for weak coupling. High-temperature superconductivity mechanisms are OPEN.
  - PH.O.A4.4.3 Semiconductors and device physics: drift–diffusion transport in the low-injection regime.
  - PH.O.A4.4.4 Dislocations as the mechanism of plastic flow in crystals.
  - PH.O.A4.4.5 Topological phases: quantum Hall effects (integer 1980, fractional 1982).

Named objects: First law (closed system; sign convention stated). Second law (isolated system). Carnot efficiency (cycle between two reservoirs). Third law (non-degenerate ground state). Boltzmann entropy S = k_B ln W (equal a priori probability). Partition function and Boltzmann distribution (equilibrium with a heat bath at fixed temperature). Fermi–Dirac and Bose–Einstein distributions (indistinguishable particles; equilibrium). Clapeyron equation (on a coexistence line). Clausius–Clapeyron equation (ideal vapour; negligible condensed-phase volume; constant L). Landau theory (mean field; small order parameter; fluctuations neglected). Universality (dimension, symmetry and interaction range shared). Mermin–Wagner theorem (continuous symmetry; d ≤ 2; short-range interactions; T > 0). Bloch's theorem (periodic potential; independent electrons). BCS theory (weak phonon-mediated attraction near the Fermi surface). Density functional theory (ground state only; approximate exchange–correlation functional). Metropolis Monte Carlo (detailed balance; ergodic chain; run long against the correlation time).

### PH.O.A5 Matter out of equilibrium
**SCQA.** Situation. Most of nature is out of equilibrium, from fluids and plasmas to stars and living cells. Complication. v1 had no home for driven or relaxing matter. Many results far from equilibrium are numerical or phenomenological, and the theorems about their equations belong to MA. Question. Which laws hold away from equilibrium, and how far away? Answer. Physics owns linear-response transport, fluid and plasma models, radiative laws and nonlinear systems, each with a stated distance from equilibrium.

**Key line** (inductive; plural noun: non-equilibrium claims; dimension: the medium and how far it is driven from equilibrium; order: near equilibrium first, strongly driven last). Members (5): Transport near equilibrium · Fluids · Plasmas · Radiation and matter · Nonlinear dynamics and complex systems.

- **PH.O.A5.1 Transport near equilibrium. Small gradients produce fluxes proportional to them, with coefficients fixed by equilibrium fluctuations.** The linear regime requires gradients small enough that local equilibrium holds. Beyond that range the flux–gradient relation is nonlinear.
  - PH.O.A5.1.1 Linear response; the fluctuation–dissipation theorem for systems near equilibrium.
  - PH.O.A5.1.2 Onsager reciprocity: assumes microscopic reversibility, with the magnetic field reversed when one is present.
  - PH.O.A5.1.3 Diffusion, conduction, viscosity as transport coefficients; Boltzmann transport equation for dilute gases.
- **PH.O.A5.2 Fluids. Navier–Stokes governs Newtonian fluids.** Global smoothness in three dimensions is OPEN and owned by MA.O.A4. The continuum hypothesis and a linear stress–strain-rate relation are assumed. Rarefied and non-Newtonian flows need other closures. Engineering use of flow is EN.O.A2, which cites this cell.
  - PH.O.A5.2.1 Turbulence: Kolmogorov's 1941 scaling for homogeneous isotropic turbulence at high Reynolds number. A full theory is OPEN.
  - PH.O.A5.2.2 Dimensionless groups (Reynolds, Mach) set the regime.
- **PH.O.A5.3 Plasmas. Quasi-neutral ionised matter shows collective behaviour on scales larger than the Debye length.** Descriptions range from kinetic to fluid, and the choice depends on collisionality and scale. A model is valid only inside its stated range.
  - PH.O.A5.3.1 Magnetohydrodynamics, valid where collisions keep a fluid description.
  - PH.O.A5.3.2 Fusion plasmas: Lawson criterion for net energy gain, given confinement time and density at a stated temperature.
- **PH.O.A5.4 Radiation and matter. Radiation in thermal equilibrium follows Planck's law, and its transport through matter follows a transfer equation.** Radiative transfer needs stated absorption and emission coefficients. Local thermodynamic equilibrium is often assumed and must be checked. Climate use of the laws is EA.O.A4.3, which cites this cell.
  - PH.O.A5.4.1 Planck's law for blackbody radiation in thermal equilibrium; Stefan–Boltzmann law as its integral.
  - PH.O.A5.4.2 Radiative transfer through absorbing and emitting media.
  - PH.O.A5.4.3 Interaction of ionising radiation with matter (stopping, attenuation). Nuclear decay itself, with its half-lives, moved to PH.O.A2.3.5 after the pilot (claim 38).
- **PH.O.A5.5 Nonlinear dynamics and complex systems. Nonlinear systems show sensitive dependence on initial conditions, pattern formation and collective motion.** Theorems are MA.O.A4; the physical system is here.
  - PH.O.A5.5.1 Non-equilibrium fluctuation theorems (Jarzynski, Crooks) for systems driven from an initial equilibrium.
  - PH.O.A5.5.2 The largest Lyapunov exponent estimated from a time series measures the mean exponential rate of separation of nearby trajectories. It needs an ergodic invariant measure and a record long enough for the average to converge. Noise also produces apparent separation (uses MA.O.A4).
  - PH.O.A5.5.3 A uniform state that is stable without diffusion can become unstable to periodic pattern (Turing). This needs at least two interacting species with sufficiently different diffusion rates. Chemical realisations have been reported. Whether it explains a given biological pattern is CONTESTED, and that placement is BI (uses BI.O.A3.2).
  - PH.O.A5.5.4 Self-propelled particles with alignment can show long-range orientational order in two dimensions (Vicsek model, Toner–Tu theory). Equilibrium forbids this by PH.O.A4.3.4, whose hypotheses fail in a driven system. Experimental confirmation is UNVERIFIED.

Named objects: Linear response (small perturbation from equilibrium). Fluctuation–dissipation theorem (linear response; initial thermal equilibrium). Onsager reciprocity (microscopic reversibility; magnetic field reversed). Boltzmann transport equation (dilute gas; binary collisions; molecular chaos). Navier–Stokes equations (continuum; Newtonian fluid). Reynolds number (ratio of inertial to viscous forces). Kolmogorov 1941 scaling (homogeneous isotropic turbulence; high Reynolds number; inertial range). Magnetohydrodynamics (scales large against gyroradius and Debye length; quasi-neutral; frequencies below the cyclotron frequency). Vlasov equation (collisions negligible; many particles in a Debye sphere). Lawson criterion (thermal plasma; steady power balance). Planck's law (radiation in thermal equilibrium). Stefan–Boltzmann law (integral of Planck's law). Radiative transfer equation (stated coefficients). Jarzynski equality and Crooks relation (initial equilibrium; stated driving protocol). Lyapunov exponent (ergodic invariant measure; long record). Turing instability (two species; stable uniform state; unequal diffusion). Vicsek model (self-propelled particles with alignment).

## 5. Face M — Methods

| ID | Role | Shared role | Example |
|---|---|---|---|
| PH.M.1 | Formulate | M1 Represent | write the Lagrangian; choose units and variables |
| PH.M.2 | Solve | M2 Derive | perturbation theory, exact solution, symmetry argument |
| PH.M.3 | Measure | M3 Observe | spectroscopy, interferometry, telescope survey |
| PH.M.4 | Experiment | M4 Intervene | collider, cold-atom trap, condensed-matter probe |
| PH.M.5 | Simulate | M5 Compute | lattice QCD, molecular dynamics, N-body, plasma codes |

Five roles. M6 Compare appears inside PH.M.3 as the combination of measurements. M7 Verify of instruments is EN.

Field examples by role:
- PH.M.1 Formulate. Fixing the Lagrangian of the Standard Model sets its symmetry content (A2.3). Writing the Hamiltonian of a spin lattice precedes any calculation of a condensed state (A4.4). Scaling the Navier–Stokes equations by the Reynolds number gives the regime (A5.2.2).
- PH.M.2 Solve. The Kepler problem has an exact solution for two point masses (A3.1.1). Perturbation theory gives energy shifts of atomic levels (A2.4). The Schwarzschild solution is exact under spherical symmetry and vacuum (A3.2.2).
- PH.M.3 Measure. Laser interferometry detected gravitational waves (A3.2.3). Spectroscopy of a hyperfine transition realises the SI second (A2.4.3). Combining independent probes, such as the microwave background and supernova distances, is how the Hubble tension is posed (A3.4.1).
- PH.M.4 Experiment. Bell tests use entangled photons or spins with fast, random setting choices (A2.2). Collider runs searched for the Higgs boson (A2.3.2). Laser-cooled atoms in traps reach Bose–Einstein condensation (A2.4.2).
- PH.M.5 Simulate. N-body codes follow structure formation (A3.4). Molecular dynamics samples an ensemble (A4.2). Lattice calculations treat strongly coupled fields (A2.3). Plasma codes follow instabilities (A5.3).

### Heuristics register (outside the count)
- Dimensional analysis
- Order-of-magnitude estimation
- Symmetry first
- Limiting cases
- The correspondence principle
- Naturalness (CONTESTED as a guide since no new physics appeared at the LHC)
- "Shut up and calculate"

## 6. Face W — Warrants

| Cell | Warrant | Standard of acceptance | Typical defeaters |
|---|---|---|---|
| PH.O.A1 | W4 + W1 | prediction matches measurement within stated uncertainty; derivation valid | regime exceeded (speed near c, action near ħ) |
| PH.O.A2 | W3 + W4 | controlled experiment with quoted uncertainty; replication; 5σ for discovery claims in particle physics | loopholes, systematic error, look-elsewhere effect |
| PH.O.A3 | W4 | observation with stated uncertainty; independent probes agree | model dependence, selection effects, cosmic variance |
| PH.O.A3.5 | W1 only, OPEN | internal consistency; no empirical warrant yet | no testable prediction |
| PH.O.A4 | W3 + W4 + W1 | measured property matches a derived value | finite-size effects, impurities, non-equilibrium |
| PH.O.A5 | W4 + W2 | measurement, or simulation with an error bound | closure assumption, numerical artefact |

Sub-cells share their parent's row, except A3.5, which is stated separately.

Field examples of warrants and defeaters:
- PH.O.A1 (W4 + W1). A spacecraft trajectory predicted from Newtonian mechanics is compared with tracking data within the quoted uncertainty. A defeater is a regime error, such as using Newton's laws for a particle near c.
- PH.O.A2 (W3 + W4). The Higgs claim required 5σ in each of two experiments (A2.3.2). A Bell test must close detection, locality and setting-choice loopholes before its violation counts as decisive (A2.2).
- PH.O.A3 (W4). A gravitational-wave detection claims a false-alarm rate and coincidence in separate detectors (A3.2.3). The Hubble tension is a conflict between probes whose defeaters are calibration and selection effects (A3.4.1).
- PH.O.A3.5 (W1 only, OPEN). The Bekenstein–Hawking entropy is derived semiclassically and has no measurement (A3.5.1). A claim in this cell may not be stated above its W1 ceiling.
- PH.O.A4 (W3 + W4 + W1). A measured critical exponent is compared with the renormalisation-group value (A4.3.3). Finite-size rounding and impurities defeat a sharp-transition claim.
- PH.O.A5 (W4 + W2). A direct numerical solution of the Navier–Stokes equations carries a grid-convergence test (A5.2). A turbulence closure that fits one flow and fails another is defeated by that second flow (A5.2.1).

## 7. Face B — Bridges

| ID | Field | Cells | Methods | Substrate |
|---|---|---|---|---|
| PH.B.C1 | Particle and nuclear physics | A2.3, A5.4.3 | M.2, M.4, M.5 | accelerators, detectors |
| PH.B.C2 | AMO physics and quantum optics | A2.1, A2.2, A2.4 | M.3, M.4 | atoms, light |
| PH.B.C3 | Astrophysics and cosmology | A3 | M.2, M.3, M.5 | the sky |
| PH.B.C4 | Condensed matter physics | A4, A5.1 | all | solids, liquids |
| PH.B.C5 | Plasma and fluid physics | A5.2, A5.3 | M.2, M.3, M.5 | plasmas, flows |
| PH.B.C6 | Geophysics | A1, A5 | M.3, M.5 | the Earth (uses EA) |
| PH.B.C7 | Biophysics and medical physics | A4, A5 | M.3, M.4 | cells, patients (uses BI, MD) |
| PH.B.C8 | Quantum information | A2.2 | M.2, M.4 | qubits (protocols CS) |

Field examples of bridges:
- PH.B.C1. A detector collaboration combines a beam (M.4), a simulation of detector response (M.5) and derived cross-sections (M.2).
- PH.B.C2. An atomic-clock group measures a transition frequency (M.3) in laser-cooled atoms held in a trap (M.4).
- PH.B.C3. A survey team measures brightness and redshift (M.3), runs N-body simulations (M.5) and derives stellar structure (M.2).
- PH.B.C4. Angle-resolved photoemission measures band structure (M.3). Density functional codes compute it (M.5). Crystal growth supplies the sample (M.4).
- PH.B.C5. A tokamak programme runs confinement experiments (M.4) and compares them with magnetohydrodynamic codes (M.5).
- PH.B.C6. Seismology measures wave speeds in the Earth (M.3), and mantle-convection codes simulate flow (M.5). The state of the Earth is EA.
- PH.B.C7. Optical tweezers measure the force on a single molecule (M.3, M.4). Radiotherapy dose calculation is computed (M.5) and used in MD.
- PH.B.C8. A key-distribution link is built and tested against the Bell bound (M.4). The protocol itself is CS.

## 8. Assignment rules
1. Place a claim by the largest set of constants its derivation needs. Place N-body claims in A4 or A5 by equilibrium.
2. A theorem about the equations is MA. The claim that nature obeys them is PH.
3. A bond, reaction rate or molecular structure is CH. Atomic levels are PH.
4. A device meeting a specification is EN. The law it relies on is PH.
5. Quantum interpretation: empirical content in PH.O.A2, argument in PL.
6. Physics education research is ED (uses PH).
7. Climate and Earth-system claims are EA. The radiative law they use is PH.O.A5.4.
8. A claim that crosses regimes goes to the regime with more constants.

## 9. Scope boundary

| Refused | Owner |
|---|---|
| theorems about differential equations and operators | MA.O.A2, MA.O.A4 |
| chemical bonding and reaction | CH |
| Earth state, climate record | EA |
| instrument and device design | EN |
| meaning of quantum mechanics | PL |
| physics teaching | ED |

## 10. External crosswalk
**ANZSRC 51** Physical sciences (checked 9 Oct 2026, ABS anzsrc2020_for.xlsx) has 11 groups:

| Group | Home |
|---|---|
| 5101 Astronomical sciences | A3, B.C3 |
| 5102 Atomic, molecular and optical physics | A2.4, B.C2 |
| 5103 Classical physics | A1 |
| 5104 Condensed matter physics | A4, B.C4 |
| 5105 Medical and biological physics | B.C7 |
| 5106 Nuclear and plasma physics | A2.3, A5.3, B.C1, B.C5 |
| 5107 Particle and high energy physics | A2.3, B.C1 |
| 5108 Quantum physics | A2.1, A2.2, B.C8 |
| 5109 Space sciences | A3, with EA for the near-Earth environment |
| 5110 Synchrotrons and accelerators | Face M (PH.M.4), instruments EN |
| 5199 Other physical sciences | not a cell |

Coverage: 9 of 10 substantive groups land as cells or bridges; 5110 lands as method.
**PhySH** (APS) has five facets: research areas, physical systems, properties, techniques and professional topics. It lists 17 disciplines (checked: Wikipedia summary of physh.aps.org). The 17 names are not yet transcribed, so a discipline-by-discipline map is pending (R4 partial). Professional topics such as education and careers are refused to ED and BU.

## 11. Validation
Sizes: key line 5. Face O 5 cells + 24 sub-cells = 29, with 72 named objects below them. A-cell key lines state their member counts: A1 5, A2 5, A3 5, A4 4, A5 5. M roles 5. Heuristics 7, outside the count. W rows 6. B bridges 8.
Key line, word for word: Classical motion and fields. Quantum systems. Gravitation and the cosmos. Matter in equilibrium. Matter out of equilibrium.
OPEN: quantum gravity (A3.5); dark matter and dark energy; the Hubble tension; neutrino mass ordering; high-temperature superconductivity; turbulence; 3D Navier–Stokes smoothness (MA, cited).
CONTESTED: interpretation of QM (PH vs PL); Newtonian gravity in A3 rather than A1; inflation; naturalness as a guide; the ergodic justification; superdeterminism (A2.2); the muon anomalous magnetic moment comparison (A2.3); Turing patterns as an explanation of biological form (A5.5.3, home BI).
UNVERIFIED: the attribution of the modern c–G–ħ cube; the current excluded range of collapse-model parameters (A2.5.2); the largest molecule shown to interfere (A2.5.3); the latest muon anomalous magnetic moment result (A2.3); experimental confirmation of two-dimensional flocking order (A5.5.4).
Phase 2.3 added second key lines with member counts, a bold claim for every sub-cell, named objects with hypotheses for A1 to A5, and six third-level cells under sub-cells that had fewer than two (A2.5.1 to A2.5.3, A5.5.2 to A5.5.4).
Fixed from the audit: the cube is now named as an adaptation; N is marked as the author's axis; G–ħ is refused and c–G–ħ is OPEN; transport, plasma and radiation have homes; Clapeyron is distinguished from Clausius–Clapeyron; the quasiparticle condition uses rate; k_B is restored; heuristics are outside the count.

## 12. Registry rows

| ID | Label | Home | Uses |
|---|---|---|---|
| PH.O.A1 | Classical motion and fields | O/A1 | — |
| PH.O.A1.1 | Particle mechanics | O/A1 | — |
| PH.O.A1.1.1 | Lagrangian and Hamiltonian mechanics are equivalent where the Legendre | O/A1 | — |
| PH.O.A1.1.2 | Liouville's theorem | O/A1 | MA.O.A4 |
| PH.O.A1.1.3 | Rigid-body motion, oscillators and small vibrations. | O/A1 | — |
| PH.O.A1.2 | Classical fields | O/A1 | — |
| PH.O.A1.2.1 | Electrostatics and magnetostatics, including the quasistatic circuit l | O/A1 | — |
| PH.O.A1.2.2 | Electromagnetic waves; c is the propagation speed in vacuum. | O/A1 | — |
| PH.O.A1.2.3 | Classical optics | O/A1 | — |
| PH.O.A1.3 | Special relativity | O/A1 | — |
| PH.O.A1.3.1 | Lorentz transformations; time dilation; length contraction. | O/A1 | — |
| PH.O.A1.3.2 | Mass–energy equivalence, E = mc² for a body at rest. | O/A1 | — |
| PH.O.A1.4 | Symmetry and conservation | O/A1 | MA, MA.O.A4 |
| PH.O.A1.4.1 | Energy, momentum and angular momentum from time, space and rotation sy | O/A1 | — |
| PH.O.A1.4.2 | Charge conservation from the gauge symmetry of electrodynamics. | O/A1 | — |
| PH.O.A1.5 | Continuum mechanics | O/A1 | — |
| PH.O.A1.5.1 | Linear elasticity | O/A1 | — |
| PH.O.A1.5.2 | Constitutive laws close the balance equations | O/A1 | EN |
| PH.O.A2 | Quantum systems | O/A2 | — |
| PH.O.A2.1 | States and dynamics | O/A2 | — |
| PH.O.A2.1.1 | The uncertainty relation σ_x σ_p ≥ ħ/2 holds for any state (the theore | O/A2 | MA.O.A2 |
| PH.O.A2.1.2 | Decoherence | O/A2 | — |
| PH.O.A2.1.3 | Tunnelling and bound states. | O/A2 | — |
| PH.O.A2.2 | Non-locality | O/A2 | — |
| PH.O.A2.2.1 | Entanglement as a resource | O/A2 | CS.O.A5 |
| PH.O.A2.2.2 | No-signalling | O/A2 | — |
| PH.O.A2.3 | Quantum fields and particles | O/A2 | — |
| PH.O.A2.3.1 | Spin–statistics and CPT hold for local, Lorentz-invariant quantum fiel | O/A2 | — |
| PH.O.A2.3.2 | The Higgs boson was observed in 2012 (ATLAS and CMS). | O/A2 | — |
| PH.O.A2.3.3 | Neutrino oscillation implies non-zero neutrino masses | O/A2 | — |
| PH.O.A2.3.4 | Renormalisation | O/A2 | — |
| PH.O.A2.3.5 | Nuclear structure and decay | O/A2 | EA |
| PH.O.A2.4 | Atomic, molecular and optical physics | O/A2 | CH |
| PH.O.A2.4.1 | Lasers | O/A2 | — |
| PH.O.A2.4.2 | Laser cooling and Bose–Einstein condensation of dilute gases (first ac | O/A2 | — |
| PH.O.A2.4.3 | Atomic clocks and precision measurement | O/A2 | — |
| PH.O.A2.5 | Interpretation of quantum mechanics | O/A2 | PL |
| PH.O.A2.5.1 | Interpretations without new dynamics agree on statistics | O/A2 | PL |
| PH.O.A2.5.2 | Collapse models and experimental bounds | O/A2 | PL |
| PH.O.A2.5.3 | Matter-wave interference of large molecules | O/A2 | — |
| PH.O.A3 | Gravitation and the cosmos | O/A3 | — |
| PH.O.A3.1 | Newtonian gravity | O/A3 | — |
| PH.O.A3.1.1 | Kepler's laws follow for two point masses. | O/A3 | — |
| PH.O.A3.1.2 | Celestial mechanics | O/A3 | MA.O.A4 |
| PH.O.A3.2 | General relativity | O/A3 | — |
| PH.O.A3.2.1 | Classical tests | O/A3 | — |
| PH.O.A3.2.2 | Black holes | O/A3 | MA.O.A3 |
| PH.O.A3.2.3 | Gravitational waves | O/A3 | — |
| PH.O.A3.3 | Astrophysics | O/A3 | — |
| PH.O.A3.3.1 | Stellar structure and nucleosynthesis. | O/A3 | — |
| PH.O.A3.3.2 | The Chandrasekhar limit | O/A3 | — |
| PH.O.A3.3.3 | Neutron stars, pulsars, accretion. | O/A3 | — |
| PH.O.A3.4 | Cosmology | O/A3 | — |
| PH.O.A3.4.1 | Hubble–Lemaître expansion | O/A3 | — |
| PH.O.A3.4.2 | The CMB, discovered 1965. | O/A3 | — |
| PH.O.A3.4.3 | Dark matter and dark energy | O/A3 | — |
| PH.O.A3.4.4 | Inflation | O/A3 | — |
| PH.O.A3.5 | Quantum gravity | O/A3 | — |
| PH.O.A3.5.1 | Bekenstein–Hawking entropy S = k_B c³ A / (4Għ) for a black hole of ho | O/A3 | — |
| PH.O.A3.5.2 | Hawking radiation | O/A3 | — |
| PH.O.A3.5.3 | Programmes | O/A3 | — |
| PH.O.A4 | Matter in equilibrium | O/A4 | — |
| PH.O.A4.1 | Thermodynamics. | O/A4 | — |
| PH.O.A4.1.1 | First law | O/A4 | — |
| PH.O.A4.1.2 | Second law | O/A4 | — |
| PH.O.A4.1.3 | Third law | O/A4 | — |
| PH.O.A4.2 | Statistical mechanics | O/A4 | — |
| PH.O.A4.2.1 | Boltzmann entropy S = k_B ln W. | O/A4 | — |
| PH.O.A4.2.2 | Quantum statistics | O/A4 | — |
| PH.O.A4.2.3 | Ergodic hypothesis | O/A4 | MA.O.A4 |
| PH.O.A4.3 | Phase transitions. | O/A4 | — |
| PH.O.A4.3.1 | Clapeyron equation | O/A4 | — |
| PH.O.A4.3.2 | Clausius–Clapeyron | O/A4 | — |
| PH.O.A4.3.3 | Critical phenomena and universality | O/A4 | — |
| PH.O.A4.3.4 | Mermin–Wagner | O/A4 | — |
| PH.O.A4.4 | Condensed states | O/A4 | — |
| PH.O.A4.4.1 | Quasiparticles | O/A4 | — |
| PH.O.A4.4.2 | BCS theory of conventional superconductivity | O/A4 | — |
| PH.O.A4.4.3 | Semiconductors and device physics | O/A4 | — |
| PH.O.A4.4.4 | Dislocations as the mechanism of plastic flow in crystals. | O/A4 | — |
| PH.O.A4.4.5 | Topological phases | O/A4 | — |
| PH.O.A5 | Matter out of equilibrium | O/A5 | — |
| PH.O.A5.1 | Transport near equilibrium. | O/A5 | — |
| PH.O.A5.1.1 | Linear response; the fluctuation–dissipation theorem for systems near  | O/A5 | — |
| PH.O.A5.1.2 | Onsager reciprocity | O/A5 | — |
| PH.O.A5.1.3 | Diffusion, conduction, viscosity as transport coefficients; Boltzmann  | O/A5 | — |
| PH.O.A5.2 | Fluids | O/A5 | MA.O.A4 |
| PH.O.A5.2.1 | Turbulence | O/A5 | — |
| PH.O.A5.2.2 | Dimensionless groups (Reynolds, Mach) set the regime. | O/A5 | — |
| PH.O.A5.3 | Plasmas | O/A5 | — |
| PH.O.A5.3.1 | Magnetohydrodynamics, valid where collisions keep a fluid description. | O/A5 | — |
| PH.O.A5.3.2 | Fusion plasmas | O/A5 | — |
| PH.O.A5.4 | Radiation and matter. | O/A5 | — |
| PH.O.A5.4.1 | Planck's law for blackbody radiation in thermal equilibrium; Stefan–Bo | O/A5 | — |
| PH.O.A5.4.2 | Radiative transfer through absorbing and emitting media. | O/A5 | — |
| PH.O.A5.4.3 | Nuclear decay and radiation interaction with matter | O/A5 | — |
| PH.O.A5.5 | Nonlinear dynamics and complex systems | O/A5 | MA.O.A4 |
| PH.O.A5.5.1 | Non-equilibrium fluctuation theorems (Jarzynski, Crooks) for systems d | O/A5 | — |
| PH.O.A5.5.2 | Lyapunov exponent from a time series | O/A5 | MA.O.A4 |
| PH.O.A5.5.3 | Turing instability and pattern formation | O/A5 | BI.O.A3.2 |
| PH.O.A5.5.4 | Long-range order in two-dimensional active matter | O/A5 | PH.O.A4.3.4 |

## 13. Self-check against R1–R12

| Rule | Result | If FAIL: sentence and repair |
|---|---|---|
| R1 | PASS | — |
| R2 | PASS | Counts checked by script. |
| R3 | PASS | — |
| R4 | PASS (partial) | ANZSRC 51 9 of 10 checked. "The 17 names are not yet transcribed." Repair: transcribe PhySH disciplines and map each. |
| R5 | PASS | Noether, Bell, CPT, spin–statistics, Mermin–Wagner, Clapeyron, Onsager, Chandrasekhar, Bekenstein–Hawking, Lawson stated with conditions. |
| R6 | PASS | Seven OPEN, eight CONTESTED. |
| R7 | PASS | — |
| R8 | PASS | — |
| R9 | PASS | Deepened in Phases 2.2 and 2.3. |
| R10 | PASS | — |
| R11 | FAIL (partial) | Dates (2012 Higgs, 1995 BEC, 1965 CMB, 1980/1982 quantum Hall, 1967 SI second) are standard but not cited to sources here. Repair: add citations. |
| R12 | PASS | IDs used by EN (A1.1, A1.2, A1.5, A4.1, A4.4) kept stable. |
