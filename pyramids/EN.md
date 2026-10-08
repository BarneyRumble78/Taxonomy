# EN — Engineering

Standard: T/00_STANDARD_V2.md (R1–R12, faces O/M/W/B, M1–M7, W1–W13), cited not copied. Diagnosis: T/audit_engineering_cs.md (EN #1–#20, fact check, duplicates, coverage). v1 source: twelve.txt 2061–2607. Theorems are owned by MA (T/maths_reconciled.md) and cited as "uses MA.…". Physics, chemistry and earth owner IDs (PH.…, CH.…, EA.…) are the owner cells proposed in the audit; they must be reconciled against p2_PH, p2_CH and p2_EA when those files land.

## 1. SCQA

Situation. Engineering makes artefacts that perform a stated function under constraints of safety, cost, code, material and time. Complication. Department lists double-count: a pump is fluid mechanics, machine design, a control loop and a procurement specification at once. v1 also filed predictive formulas on its method side, kept two closing quantities in one cell, and gave no scope boundary. Question. Which single partition places every engineering claim, procedure and discipline exactly once, with each law cited to its owner?

## 2. Governing thought

Engineering is exhausted by four faces of one pyramid: objects, methods, warrants and bridges. Its object claims divide into five balances: force and deformation, mass and momentum, energy and entropy, electromagnetic state, and composition and microstructure.

## 3. Key line

This is the key line of Face O, the claim partition of the pyramid.

- Logic: inductive.
- Plural noun: balances.
- Dimension: the quantity whose balance or constitutive closure finishes the predictive model of an artefact.
- Order: structural, from load path to material.
- Members (5):
  1. force and deformation
  2. mass and momentum
  3. energy and entropy
  4. electromagnetic state
  5. composition and microstructure

Test for a new member (repairs audit EN #18). A sixth balance is warranted only if an artefact model needs a closing quantity none of the five carries. Information state passes that test and is therefore not an EN balance: it is owned by CS (uses CS.O.A2.4). Failure probability also passes it, and is owned by MA (uses MA.O.A5). Neither is held in EN by fiat.

## 4. Face O — Objects

Face O holds predictive claims used to size or exonerate an artefact. A formula that predicts behaviour lives here, never on Face M (audit EN #6). A law owned elsewhere appears as "uses <owner>"; EN owns the engineering reduction, correlation or closure.

### EN.O.A1 Force and deformation

Situation. Structures and machine elements are sized by equilibrium of force and moment, closed by a constitutive law. Complication. v1 divided this cell by "scale", yet listed inertia, which is not a scale (audit EN #5). Question. Which idealisations exhaust force-and-deformation models?

Key line. Plural noun: idealisations. Dimension: what the model idealises the body as. Order: from fewest to most degrees of freedom retained. Members (4): rigid bodies; slender members; deformable continua; contact interfaces.

- **EN.O.A1.1 Rigid bodies.** Statics: ΣF = 0 and ΣM = 0 when inertia is negligible. Dynamics: ΣF = m a and ΣM = dH/dt about the centre of mass or a fixed point. These laws are Newtonian mechanics (uses PH.O.A1.1). EN owns the free-body reduction and determinacy check.
  - EN.O.A1.1.1 Free-body diagram and static determinacy.
  - EN.O.A1.1.2 Rigid-body dynamics of mechanisms (linkages, gears, cams).
  - EN.O.A1.1.3 Lumped vibration models: single- and multi-degree-of-freedom systems with linear springs and viscous damping. Natural frequency ωn = √(k/m) for an undamped linear oscillator.
- **EN.O.A1.2 Slender members.** A member whose length greatly exceeds its section is reduced to section resultants plus a kinematic assumption.
  - EN.O.A1.2.1 Euler–Bernoulli beam. For a prismatic, linear-elastic member with small slopes and plane sections remaining plane and normal: EI d²v/dx² = M(x). With load q positive downward, dM/dx = V and dV/dx = −q (Gere and Goodno, §4.5; sign convention stated, audit fact check).
  - EN.O.A1.2.2 Timoshenko beam: adds shear deformation and rotary inertia for deep or short beams.
  - EN.O.A1.2.3 Torsion of a circular shaft. For a linear-elastic, circular or annular, prismatic bar under small twist: T = G J θ / L and τ = T r / J.
  - EN.O.A1.2.4 Euler column buckling. For an initially straight, slender, linear-elastic, centrally loaded column: Pcr = π² E I / (K L)². Stocky columns leave this formula for a tangent-modulus or code curve.
  - EN.O.A1.2.5 Kirchhoff–Love plate and Mindlin–Reissner plate. Kirchhoff–Love applies to thin plates with normals staying normal; Mindlin–Reissner admits transverse shear for moderately thick plates.
  - EN.O.A1.2.6 Thin-walled pressure vessel. For wall thickness much less than radius, under internal pressure p: hoop stress pr/t and longitudinal stress pr/2t.
- **EN.O.A1.3 Deformable continua.** The parent theory when section assumptions fail.
  - EN.O.A1.3.1 Cauchy stress and traction t = σᵀn (uses PH.O.A1.5 for the continuum balance laws).
  - EN.O.A1.3.2 Isotropic linear elasticity (Hooke). For small strain, a linear, isotropic material: σ = λ tr(ε) I + 2μ ε, with G = E / 2(1+ν). Uses PH.O.A1.5.
  - EN.O.A1.3.3 Yield criteria: Tresca (maximum shear) and von Mises (distortion energy), for isotropic ductile metals under quasi-static load.
  - EN.O.A1.3.4 Mohr's circle: principal stresses and maximum shear from the plane-stress transformation.
  - EN.O.A1.3.5 Linear-elastic fracture mechanics. Under small-scale yielding, K = Y σ √(π a). Mode I, plane-strain failure occurs when K reaches KIc (ASTM E399).
  - EN.O.A1.3.6 Fatigue life. Basquin (stress-life) and Coffin–Manson (strain-life) relations, fitted per material. Paris law da/dN = C (ΔK)^m holds in region II only; C and m depend on material and R-ratio (Paris and Erdogan 1963).
  - EN.O.A1.3.7 Geomechanics. Terzaghi effective stress σ′ = σ − u for saturated soil. Mohr–Coulomb strength τ = c′ + σ′ tan φ′ for drained soil and rock joints. CONTESTED: EA.O.A1 (rock and soil as earth materials) is the alternative owner; EN keeps the strength closure, EA owns genesis.
- **EN.O.A1.4 Contact interfaces.**
  - EN.O.A1.4.1 Hertz contact. For two smooth, elastic, non-conforming bodies with frictionless contact and small contact area: contact radius and peak pressure follow from load, curvatures and moduli. CONTESTED: PH.O.A1.5 is the alternative owner.
  - EN.O.A1.4.2 Coulomb friction: tangential force bounded by μ times normal force, an empirical closure.
  - EN.O.A1.4.3 Archard wear law: worn volume proportional to load times sliding distance over hardness, with a fitted wear coefficient (UNVERIFIED as to standard notation).
  - EN.O.A1.4.4 Concepts: stress concentration, Saint-Venant decay, shear centre, slenderness, ductility, redundancy, mechanism.

Miner's rule (linear damage sum) is not a Face O claim. It sits in the heuristics register EN.H.

### EN.O.A2 Mass and momentum

Situation. A flow is closed by conservation of mass and momentum plus a constitutive relation for fluid stress. Complication. v1 had no key line here (audit EN #12), and filed Navier–Stokes, Bernoulli and Reynolds number in both PH and EN. Question. Which flow domains exhaust mass-and-momentum models in engineering?

Key line. Plural noun: flow domains. Dimension: the boundary that confines the flow. Order: from fully confined to unconfined medium. Members (5): internal flows; external flows; free-surface flows; compressible and acoustic flows; porous-medium flows.

Shared basis. Integral mass and momentum balances on a control volume, and the Navier–Stokes equations for a Newtonian fluid, are owned by physics (uses PH.O.A1.5). Existence and regularity of Navier–Stokes solutions is MA (uses MA.O.A4). EN owns the reductions below.

- **EN.O.A2.1 Internal flows.**
  - EN.O.A2.1.1 Bernoulli equation along a streamline, for steady, inviscid, incompressible flow: p/ρ + V²/2 + g z = constant. Uses PH.O.A1.5. A loss term is added, not derived, when the hypotheses fail.
  - EN.O.A2.1.2 Darcy–Weisbach head loss h_f = f (L/D) V²/2g, where f is the Darcy (Moody) friction factor, four times the Fanning factor.
  - EN.O.A2.1.3 Colebrook equation and Moody chart for f in fully developed turbulent pipe flow (empirical closure). Minor losses K V²/2g.
  - EN.O.A2.1.4 Pump and fan matching: head-capacity curve against system curve. Affinity laws hold only between dynamically similar operating points.
  - EN.O.A2.1.5 Reynolds lubrication equation, for thin, viscous, laminar films with negligible inertia (tribology).
  - EN.O.A2.1.6 Euler turbomachine equation. For steady flow through a rotor, specific work done on the fluid is w = u₂c_θ2 − u₁c_θ1 (pump or compressor); for a turbine the extracted work is its negative.
  - EN.O.A2.1.7 Water hammer (Joukowsky surge Δp = ρ a ΔV for instantaneous valve closure in an elastic pipe).
- **EN.O.A2.2 External flows.** Drag and lift coefficients; boundary layer; separation as the stall and form-drag mechanism. Reynolds number Re = ρVL/μ = UL/ν (the two forms are equivalent, uses PH.O.A1.5). Flight mechanics and aeroelasticity draw on this cell plus EN.O.A1.
- **EN.O.A2.3 Free-surface flows.**
  - EN.O.A2.3.1 Open-channel specific energy and Froude number Fr = V/√(g h) for a rectangular channel.
  - EN.O.A2.3.2 Manning equation, an empirical resistance closure for steady, uniform, fully rough open-channel flow.
  - EN.O.A2.3.3 Ship hydrostatics and stability: buoyancy, metacentric height GM, righting arm, for small heel angles (initial stability).
  - EN.O.A2.3.4 Hull resistance and seakeeping, with Froude scaling of wave resistance.
- **EN.O.A2.4 Compressible and acoustic flows.**
  - EN.O.A2.4.1 Isentropic nozzle relations for a calorically perfect gas in adiabatic, reversible, quasi-one-dimensional flow. Choked flow when the throat is sonic (M = 1).
  - EN.O.A2.4.2 Normal-shock relations (Rankine–Hugoniot) for a perfect gas.
  - EN.O.A2.4.3 Linear acoustics: small-amplitude pressure waves in a quiescent fluid; sound pressure level and transmission loss (noise control).
- **EN.O.A2.5 Porous-medium flows.**
  - EN.O.A2.5.1 Darcy's law q = −(k/μ)∇p for slow, laminar flow through a rigid, saturated porous medium. CONTESTED: EA.O.A4 (groundwater) is the alternative owner.
  - EN.O.A2.5.2 Ergun equation for pressure drop through a packed bed of particles.
  - EN.O.A2.5.3 Consolidation (Terzaghi one-dimensional consolidation) for saturated, linear, laterally confined soil.

Concepts for A2: control volume versus particle, streamline, stagnation, cavitation (local pressure falls to vapour pressure), multiphase regime maps.

### EN.O.A3 Energy and entropy

Situation. Every efficiency claim and thermal sizing is the first law on a control volume, bounded by the second law and closed by a rate law. Complication. v1 lacked a key line and misstated the Stefan–Boltzmann exchange (audit fact check). Question. Which mechanisms exhaust energy-and-entropy models in engineering?

Key line. Plural noun: energy mechanisms. Dimension: what the model asks of the energy. Order: from bookkeeping to limit to rate to source. Members (4): first-law balances; second-law limits; heat-transfer rates; reacting energy.

- **EN.O.A3.1 First-law balances.**
  - EN.O.A3.1.1 Steady open-system first law: Q̇ − Ẇ = Σṁ(h + V²/2 + g z)out − Σṁ(h + V²/2 + g z)in, with heat in and work out positive. The law is owned by physics (uses PH.O.A4.1).
  - EN.O.A3.1.2 Property closures: ideal-gas model, steam and refrigerant tables (data, W12 and W4).
  - EN.O.A3.1.3 Cycles as applications: Rankine, Brayton, Otto, Diesel (air-standard idealisations), vapour-compression refrigeration with COP = Q_cold / W.
- **EN.O.A3.2 Second-law limits.**
  - EN.O.A3.2.1 Carnot efficiency 1 − T_c/T_h, the ceiling for a heat engine between two reservoirs at absolute temperatures. Uses PH.O.A4.1.
  - EN.O.A3.2.2 Exergy: work potential relative to a stated dead state. Irreversibility located per component, not only totalled.
  - EN.O.A3.2.3 Pinch analysis: minimum approach temperature in a heat-exchanger network.
- **EN.O.A3.3 Heat-transfer rates.**
  - EN.O.A3.3.1 Fourier's law q = −k∇T for an isotropic conductor; plane wall Q = k A ΔT / L at steady state. CONTESTED: PH.O.A4.1 (transport) is the alternative owner.
  - EN.O.A3.3.2 Newton's law of cooling q = h A (T_s − T_∞), with h from a Nusselt correlation used inside its stated Re and Pr range.
  - EN.O.A3.3.3 Radiation exchange. Emissive power of a grey surface is ε σ T⁴. Net exchange of a small grey surface with large surroundings is q = ε σ A (T_s⁴ − T_sur⁴), absolute temperatures (Incropera and DeWitt, ch. 1). Enclosures use view factors.
  - EN.O.A3.3.4 Heat exchangers: LMTD method, or effectiveness–NTU with NTU = U A / C_min.
  - EN.O.A3.3.5 Fins: added area against a convection boundary, with fin efficiency.
- **EN.O.A3.4 Reacting energy.** Heating value and stoichiometry enter the first law as an enthalpy of reaction (uses CH.O.A3.1). Adiabatic flame temperature is the no-heat-loss limit. Fire growth and smoke models for compartments draw on this cell (fire protection).

### EN.O.A4 Electromagnetic state

Situation. Power and signal artefacts are closed by circuit or field laws. Complication. v1 held electromagnetic and information state in one cell, which made six closing quantities (audit EN #4). Information state now belongs to CS. Question. Which reductions of electromagnetic theory exhaust EN models of power and signal?

Key line. Plural noun: electromagnetic reductions. Dimension: which reduction of Maxwell's equations closes the model. Order: from smallest to largest spatial extent relative to wavelength, then down to the device. Members (4): lumped circuits; electromechanical conversion; distributed fields; semiconductor devices.

Shared basis. Maxwell's equations, Faraday's law of induction and the Kirchhoff circuit laws (as the quasistatic reduction) are owned by physics (uses PH.O.A1.2b). EN owns the engineering reductions and device closures.

- **EN.O.A4.1 Lumped circuits.** Valid when the circuit is small compared with the shortest relevant wavelength.
  - EN.O.A4.1.1 Ohm's law V = I R for a linear resistor; Kirchhoff circuit laws (uses PH.O.A1.2b).
  - EN.O.A4.1.2 Impedance R, jωL and 1/(jωC), with phasors, for linear circuits in sinusoidal steady state.
  - EN.O.A4.1.3 Thévenin and Norton equivalents, for linear networks seen from two terminals.
  - EN.O.A4.1.4 Maximum power transfer. For a linear source with impedance Z_s, load power is maximised when Z_L = Z_s* (complex conjugate). A resistive match applies only to DC or purely resistive sources. A theorem, not a universal design rule.
  - EN.O.A4.1.5 Linear time-invariant system response: impulse response, transfer function, frequency response. Fourier and Laplace transforms are MA (uses MA.O.A4). State space ẋ = Ax + Bu, y = Cx + Du and G(s) = C(sI − A)⁻¹B + D, for LTI plants.
  - EN.O.A4.1.6 Sampling theorem. A band-limited signal with no content at or above B is recovered from samples taken faster than 2B per second. Uses MA.B.C4 (MSC 94A).
  - EN.O.A4.1.7 Concepts: ground and reference, power factor, harmonics, noise figure.
- **EN.O.A4.2 Electromechanical conversion.**
  - EN.O.A4.2.1 Magnetic circuit: Ampère's law with reluctance, for linear core material without saturation.
  - EN.O.A4.2.2 Ideal transformer V₁/V₂ = N₁/N₂, for zero leakage, zero winding resistance and infinite core permeability.
  - EN.O.A4.2.3 Machines: torque from current and flux. Synchronous speed n_s = 120 f / p (rpm, p poles). Induction-motor slip.
  - EN.O.A4.2.4 Power-flow equations for an AC network in balanced steady state (load flow).
- **EN.O.A4.3 Distributed fields.**
  - EN.O.A4.3.1 Transmission line: telegrapher's equations; characteristic impedance; reflection coefficient.
  - EN.O.A4.3.2 Waveguides and antennas: modes, gain, radiation pattern.
  - EN.O.A4.3.3 Friis transmission equation for far-field free-space links between matched, polarisation-aligned antennas.
  - EN.O.A4.3.4 Optical and photonic devices: fibre modes, attenuation, dispersion. Optics as physics (uses PH.O.A1.2c).
  - EN.O.A4.3.5 Electromagnetic compatibility: coupling paths and shielding; skin effect.
- **EN.O.A4.4 Semiconductor devices.**
  - EN.O.A4.4.1 Diode and MOSFET constitutive curves (e.g., Shockley diode equation for an ideal p–n junction with low injection).
  - EN.O.A4.4.2 Drift–diffusion device model (uses PH.O.A4.4a for band theory).
  - EN.O.A4.4.3 Digital abstraction: voltage bands treated as logic levels, with noise margins. Above this abstraction the claim is CS (uses CS.O.A2.4 for the Boolean function).
  - EN.O.A4.4.4 Power-electronic switching converters: averaged models of buck and boost stages in continuous conduction.

Information-theoretic bounds (Shannon–Hartley) are not EN claims. For a band-limited channel with additive white Gaussian noise and an average power constraint, C = B log₂(1 + S/N), with S/N a linear power ratio (Shannon 1949). Owner MA.B.C4 (MSC 94A); EN uses it in link budgets.

### EN.O.A5 Composition and microstructure

Situation. Process and materials models are closed by conservation of species plus a rate or equilibrium law, and by the microstructure that supplies material properties. Complication. v1 had no key line here, and refiled Arrhenius, Raoult and Faraday electrolysis, which chemistry owns. Question. Which closures exhaust composition-and-microstructure models?

Key line. Plural noun: composition closures. Dimension: what closes the species or structure balance. Order: from reaction to separation to solid to charge to nucleus. Members (5): reaction rates; equilibrium stages; microstructure–property relations; electrochemical cells; neutron balances.

- **EN.O.A5.1 Reaction rates.**
  - EN.O.A5.1.1 Species balance: accumulation = in − out + generation.
  - EN.O.A5.1.2 Ideal reactors: batch, continuous stirred tank (perfect mixing), plug flow (no axial mixing). Conversion against residence time; residence-time distribution diagnoses real reactors.
  - EN.O.A5.1.3 Arrhenius rate constant k = A exp(−E_a/RT), for an elementary or effective rate over a stated temperature range. Uses CH.O.A4.2.
  - EN.O.A5.1.4 Scale-up limits: mixing and heat removal.
- **EN.O.A5.2 Equilibrium stages.**
  - EN.O.A5.2.1 Raoult's law for ideal liquid mixtures, or a fugacity model when non-ideal (uses CH.O.A3.1).
  - EN.O.A5.2.2 McCabe–Thiele construction for binary distillation, assuming constant molar overflow.
  - EN.O.A5.2.3 Two-film theory: interphase flux = K Δc, with an overall coefficient. Rate-based models apply when stage equilibrium fails.
  - EN.O.A5.2.4 Flowsheet degrees of freedom, recycle and purge.
- **EN.O.A5.3 Microstructure–property relations.**
  - EN.O.A5.3.1 Phase diagram as the equilibrium map (uses CH.O.A3.1 for phase equilibrium).
  - EN.O.A5.3.2 TTT and CCT diagrams as kinetic maps for steels.
  - EN.O.A5.3.3 Hall–Petch relation σ_y = σ₀ + k d^(−1/2), for polycrystals over a stated grain-size range (fails at the nanoscale).
  - EN.O.A5.3.4 Rule of mixtures for composites, as upper (Voigt) and lower (Reuss) bounds, not a point prediction.
  - EN.O.A5.3.5 Dislocation slip as the mechanism of plastic flow (uses PH.O.A4.4 condensed matter).
- **EN.O.A5.4 Electrochemical cells.**
  - EN.O.A5.4.1 Faraday's laws of electrolysis: mass reacted proportional to charge passed (uses CH.O.A3.1). Applied to corrosion rate and plating.
  - EN.O.A5.4.2 Nernst equation for the reversible cell potential at stated activities (uses CH.O.A3.1).
  - EN.O.A5.4.3 Battery and fuel-cell device models: capacity, polarisation curves, state of charge.
  - EN.O.A5.4.4 Passivation as a kinetic state, not a permanent property.
- **EN.O.A5.5 Neutron balances.**
  - EN.O.A5.5.1 Effective multiplication factor k_eff; criticality at k_eff = 1.
  - EN.O.A5.5.2 One-group neutron diffusion equation, valid away from boundaries and strong absorbers; transport theory otherwise. Cross-section data uses PH.
  - EN.O.A5.5.3 Decay heat after shutdown, carried as a source by the energy balance EN.O.A3.1.
  - EN.O.A5.5.4 Shielding attenuation for a stated source and geometry.

## 5. Face M — Methods

Face M holds procedures. A procedure produces a decision, a form, a made thing or a check; it does not predict. Predictions used by a procedure are cited from Face O or from their owner.

Key line. Plural noun: stages. Dimension: what the procedure does to the artefact or its description. Order: chronological, by first use in a life cycle (ISO/IEC/IEEE 15288 as reference). Members (5): specification; analysis; synthesis; making; assurance.

Shared-standard note. M1–M7 have no "design" or "operate" role. Synthesis is mapped to M4 (construct a form) with M5; operation actions are mapped to M4 and in-service monitoring to M3/M7. This is flagged for the standard (audit §9).

| role ID | role | maps to M1–M7 | example |
|---|---|---|---|
| EN.M.B1 | Specification: states function, constraints and acceptance tests before a form is chosen | M1 Represent | Requirement with subject, measurable predicate and verification method; interface control document; traceability matrix |
| EN.M.B2 | Analysis: turns a Face O model into a number for a stated form | M2 Derive (closed form, dimensional analysis); M5 Compute (FE, FV, circuit solvers, Monte Carlo); M3 Observe (model or prototype test where the closure is unknown) | Buckingham Π: n − k groups, k the rank of the dimensional matrix; FE K u = F with mesh-convergence check; Newton–Raphson load flow |
| EN.M.B3 | Synthesis: chooses or generates the form, including optimisation and controller design | M4 Intervene (construct a form); M5 Compute (optimisation) | Morphological matrix; Ashby performance index; linear program; PID law; topology optimisation; design of experiments |
| EN.M.B4 | Making: physical acts on the artefact across its life, from manufacture to retirement | M4 Intervene | Casting, machining, welding, additive manufacturing, PCB assembly, construction sequencing, startup, maintenance actions, decommissioning |
| EN.M.B5 | Assurance: checks the artefact against specification (verification), need (validation) and in-service condition | M7 Verify; M3 Observe (metrology, NDT, condition monitoring) | Type test, acceptance test, commissioning, NDT, safety case, fault tree, FMEA, HAZOP, code check, certification, sign-off |

Sub-structure (first descent, R9):

- EN.M.B1 key line. Plural noun: requirement types. Dimension: what the requirement constrains. Members (3): functional requirements; constraints (cost, mass, code, environment); interface requirements. Warrant W12 (a stipulated, testable predicate).
- EN.M.B2 key line. Plural noun: analysis techniques. Dimension: how the balance becomes a number. Order: comparative. Members (4): closed-form reduction; discretisation; dimensional analysis and similitude; experiment on a model or prototype. Error and convergence theory of discretisation uses MA.B.C3 (MSC 65). Prototype testing to find a closure belongs here.
- EN.M.B3 key line. Plural noun: synthesis acts. Dimension: what is chosen. Members (4): concept generation; material and component selection; optimisation; control-law design. Linear-programming duality, for feasible primal and dual, certifies optimality (strong duality; uses MA.B.C4, MSC 90C). In simplex texts "standard form" means min c·x subject to A x = b, x ≥ 0 (Bertsimas and Tsitsiklis §1.1). Routh–Hurwitz, Nyquist and Lyapunov stability criteria for LTI or stated nonlinear plants use MA.B.C4 (MSC 93D). PID G_c(s) = K_p + K_i/s + K_d s, with a derivative filter in practice.
- EN.M.B4 key line. Plural noun: making acts. Dimension: the life phase acted on. Order: chronological. Members (4): manufacture and fabrication; construction and installation; startup; maintenance and decommissioning. Software build and deployment is CS (uses CS.M.3).
- EN.M.B5 key line. Plural noun: assurance checks. Dimension: what the artefact is checked against. Members (3): verification against specification; validation against need; in-service integrity. Commissioning is acceptance against specification and sits here; B4 keeps only startup (audit EN #7). Type test against a requirement sits here; prototype test to find a closure sits in B2. Reliability prediction (series system R = ΠR_i and parallel 1 − Π(1 − R_i), for independent elements; Weibull life model) uses MA.O.A5. SIL allocation per IEC 61508 is a stipulated requirement (W12) verified by the analysis it points to.

### Heuristics register (outside the count)

EN.H. A heuristic is what remains when the balance does not close in the time available. It stays here until a code calibration or test bounds it. The register is not a sixth stage (audit EN #14).

- EN.H.1 Factor of safety = capacity / demand, defined only on one failure mode.
- EN.H.2 Partial factors and allowable stresses, as calibrated heuristics inside a code's stated scope.
- EN.H.3 Derating below catalogue limits.
- EN.H.4 Miner's linear damage sum, pending sequence effects.
- EN.H.5 Rules of thumb: span-to-depth, pipe velocity, approach temperature, current density.
- EN.H.6 Order-of-magnitude (Fermi) estimates before software.
- EN.H.7 Risk index = likelihood × consequence, as a screening device.
- EN.H.8 TRIZ and quality function deployment, as idea and mapping catalogues.
- EN.H.9 Prefer the statically determinate load path you can check by hand.
- EN.H.10 Change one thing between prototypes.

## 6. Face W — Warrants

Named sub-sub-cells (EN.O.Ax.y.z) share the row of their parent sub-cell, stated explicitly here. A warrant does not travel: a code (W12) never substitutes for the balance (W1/W4).

| cell ID | warrant W# | standard of acceptance | typical defeaters |
|---|---|---|---|
| EN.O.A1 Force and deformation | W1, W4, W2 | Prediction matches test within stated uncertainty; code calibration meets the target reliability index | Hypothesis outside range (slenderness, small strain, linearity); imperfection sensitivity; residual stress; unmodelled failure mode |
| EN.O.A1.1 Rigid bodies | W1 | Equilibrium closes; determinacy checked | Neglected inertia or flexibility; wrong support idealisation |
| EN.O.A1.2 Slender members | W1 + W4 | Section assumption holds beyond Saint-Venant distance; test agrees | Stocky or short member; local buckling; stress concentration; large slope |
| EN.O.A1.3 Deformable continua | W1 + W2 + W4 | Mesh convergence plus validation test (ASME V&V 10); fracture and fatigue data to ASTM methods | Constitutive law out of range; singularities; LEFM used beyond small-scale yielding; Paris law outside region II |
| EN.O.A1.4 Contact interfaces | W1 + W4 | Measured contact stiffness, friction or wear within scatter band | Conforming geometry; lubrication regime change; surface roughness; fitted coefficient used off-population |
| EN.O.A2 Mass and momentum | W1, W2, W4 | Validation against experiment with stated uncertainty (ASME V&V 20) | Turbulence closure outside calibration; transition; multiphase; non-Newtonian fluid |
| EN.O.A2.1 Internal flows | W1 + W4 | Head-loss prediction within correlation scatter; pump test to standard | Developing flow; roughness change; cavitation; Fanning–Darcy confusion |
| EN.O.A2.2 External flows | W2 + W4 | Wind-tunnel or flight data at matched Re and Mach | Scale effect; transition location; separation not captured |
| EN.O.A2.3 Free-surface flows | W1 + W4 | Model basin or field gauging agreement; Froude similarity respected | Large heel angles; non-uniform flow; scale effect on viscous resistance |
| EN.O.A2.4 Compressible and acoustic flows | W1 + W4 | Nozzle and shock data agree; acoustic measurement to standard | Real-gas effects; viscous losses; nonlinear acoustics |
| EN.O.A2.5 Porous-medium flows | W1 + W4 | Permeability from test; pressure drop within scatter | Non-Darcy (inertial) regime; heterogeneity; unsaturated medium |
| EN.O.A3 Energy and entropy | W1, W4 | Energy balance closes within measurement uncertainty | Extrapolated correlation; non-equilibrium; wrong dead state |
| EN.O.A3.1 First-law balances | W1 + W4 (property data) | Balance closes; sign convention stated | Missing stream; stale property data |
| EN.O.A3.2 Second-law limits | W1 | Entropy generation non-negative in every component | Wrong reservoir temperatures; dead state undefined |
| EN.O.A3.3 Heat-transfer rates | W1 + W4 | Correlation used inside its Re/Pr range; test agrees | Fouling; radiation neglected; emissive power used as net exchange |
| EN.O.A3.4 Reacting energy | W1 + W4 | Calorimetry and flame data agree | Incomplete combustion; dissociation; heat loss |
| EN.O.A4 Electromagnetic state | W1, W4 | Prediction matches measurement; compliance test passes | Lumped assumption fails; parasitics; thermal drift |
| EN.O.A4.1 Lumped circuits | W1 + W4 | Measured response within component tolerance | Frequency too high; nonlinearity; resistive match used for complex source |
| EN.O.A4.2 Electromechanical conversion | W1 + W4 | Machine and transformer tests to IEC/IEEE standard | Saturation; leakage; unbalanced operation |
| EN.O.A4.3 Distributed fields | W1 + W2 + W4 | Field-solver convergence plus range or chamber test | Material dispersion; boundary model; near-field use of Friis |
| EN.O.A4.4 Semiconductor devices | W4 + W2 | Device curves within datasheet limits; TCAD calibrated | Temperature drift; high injection; process variation; metastability |
| EN.O.A5 Composition and microstructure | W4, W3, W2 | Mass balance closure; pilot-scale agreement; property certificates | Scale-up; impurities; kinetics confused with equilibrium |
| EN.O.A5.1 Reaction rates | W4 + W3 (pilot plant) | Rate data fitted over the operating range; RTD measured | Catalyst deactivation; mixing limits; extrapolated temperature |
| EN.O.A5.2 Equilibrium stages | W1 + W4 | Stage efficiency and VLE data agree | Non-ideal mixture treated as ideal; constant molar overflow fails |
| EN.O.A5.3 Microstructure–property | W4 | Property test certificates; metallography | Microstructure variability; grain size outside Hall–Petch range |
| EN.O.A5.4 Electrochemical cells | W1 + W4 | Polarisation and capacity tests | Side reactions; ageing; temperature |
| EN.O.A5.5 Neutron balances | W2 + W4 | Code validated against critical experiments; benchmark agreement | Cross-section uncertainty; diffusion used near boundaries |

## 7. Face B — Bridges

A bridge is a named discipline: (cell) × (method subset) × (substrate). Key line. Plural noun: bridges. Dimension: the primary function delivered to a client. Order: following the balances the function loads most heavily. Members (5): civil and environmental engineering; mechanical, aerospace and marine engineering; electrical and electronic engineering; chemical, materials and resources engineering; industrial and systems engineering.

Substrate rules (not bridges). Biomedical and agricultural engineering add a living substrate to a bridge (audit EN #9). Biomedical: tissue constitutive data enter EN.O.A1/A2/A3; device regulation uses LA; clinical outcome uses MD; physiology uses BI. Agricultural and biosystems: soil-plant-water flow is EN.O.A2 with a biological sink; organism claims use BI. Cyber-physical systems and digital twins: EN.B.C3 ∩ C1 or C2, with state claims using CS.O.A2.4.

| bridge ID | named field | cell(s) | method subset | substrate |
|---|---|---|---|---|
| EN.B.C1 | Civil and environmental engineering: shelter, passage, water and waste on the ground. Sub-bridges: structural, geotechnical, hydraulic, transport, construction, environmental, fire protection, geomatics/surveying, built environment | O.A1, O.A2, O.A3.4, O.A5.1 | M.B1, B2, B4 (construction), B5 (partial-factor codes) | ground, buildings, catchments, cities; site claims use EA; aesthetic verdict uses AR; price uses EC |
| EN.B.C2 | Mechanical, aerospace and marine engineering: controlled motion and work. Sub-bridges: machine design, thermal-fluid systems, automotive, aerospace (flight mechanics, aeroelasticity, propulsion, airworthiness), naval architecture and ocean, mechatronics and robotics, acoustics and tribology | O.A1, O.A2, O.A3 | M.B2, B3 (control), B4 (manufacture), B5 (type test, certification) | machines, vehicles, aircraft, vessels; orbital mechanics uses PH |
| EN.B.C3 | Electrical and electronic engineering: power and signal transfer. Sub-bridges: power systems, electronics, communications, signal processing, photonics, control implementation, computer engineering (hardware below the ISA), cybersecurity engineering of devices | O.A4 | M.B2 (circuit and load-flow), B3, B5 (EMC, IEC/IEEE type test) | grids, devices, links; above the ISA uses CS.O.A2.4; compilers use CS.M.3; protocols use CS.O.A3.4 |
| EN.B.C4 | Chemical, materials and resources engineering: change of composition or a specified microstructure, with containment. Sub-bridges: process, separations, reaction, materials and metallurgy, nuclear, petroleum, mining and extractive metallurgy, energy storage | O.A5, with O.A1 (vessel, rock mechanics), O.A3 (heat) | M.B2, B4 (plant), B5 (HAZOP, relief sizing, criticality) | plants, reactors, mines, wells; ore genesis uses EA |
| EN.B.C5 | Industrial and systems engineering: coordinated operation of a human–technical system. Sub-bridges: systems engineering (life-cycle processes, MBSE, interface management, V-model), operations research applied, reliability and safety engineering, human factors, engineering management, manufacturing systems | any O cell as a constraint | M.B1, B3 (optimisation), B5 | enterprises, supply chains, fleets; queueing uses MA.O.A5; optimisation uses MA.B.C4; human performance uses MS; cost uses EC/BU |

## 8. Assignment rules

1. A formula that predicts behaviour lives on Face O. A discretisation, optimiser or test protocol for it lives on Face M.
2. A law owned by another pyramid is cited, not re-filed: "uses PH.O.A1.5" for Navier–Stokes, Bernoulli, Reynolds number and Hooke.
3. Maxwell's equations, Faraday's law of induction and the Kirchhoff circuit laws: uses PH.O.A1.2b.
4. Second law and Carnot limit: uses PH.O.A4.1. First law in engineering form is cited from the same owner.
5. Arrhenius: uses CH.O.A4.2. Raoult, Nernst and Faraday's laws of electrolysis: uses CH.O.A3.1.
6. Semiconductor band theory: uses PH.O.A4.4a. EN owns the device curve and drift–diffusion device model.
7. Shannon–Hartley capacity and the sampling theorem: uses MA.B.C4 (MSC 94A).
8. Little's law, utilisation ρ = λ/(cμ), Weibull and system reliability: uses MA.O.A5.
9. LP duality, nonlinear optimisation theory and stability criteria: uses MA.B.C4 (MSC 90, 93).
10. Error and convergence of FE, FV and Monte Carlo: uses MA.B.C3. Running them is EN.M.B2.
11. Control theory is a synthesis method (EN.M.B3) on a plant model. It does not add a balance.
12. A code is a calibrated verification shortcut (EN.M.B5, W12). Using a code outside its scope fails verification.
13. Commissioning goes in EN.M.B5; startup goes in EN.M.B4. Prototype test for a closure goes in EN.M.B2; type test against a requirement goes in EN.M.B5.
14. Design choices (endianness, state encoding, degree of reaction) are EN.M.B3 acts, not Face O facts.
15. Software, compilers, protocols and algorithms are CS: EN.B.C3 lists them only as "uses CS.…".
16. Device below the ISA is EN.O.A4.4; the Boolean function is CS.O.A2.4.
17. Biomedical and agricultural engineering are substrate rules on C1–C4, not bridges.
18. Built environment: the artefact meeting its use specification is EN.B.C1; the aesthetic verdict is AR; the site is EA; the price is EC.
19. Contract, liability, product regulation and licensure duty are LA. The engineer's sign-off as a procedure is EN.M.B5.
20. Name collisions are resolved by full names: Euler–Bernoulli beam vs Euler column buckling; Kirchhoff–Love plate vs Kirchhoff circuit laws; Faraday's law of induction vs Faraday's laws of electrolysis.

## 9. Scope boundary

| refused claim type | owner pyramid id |
|---|---|
| Physical law and constant (Newton, Navier–Stokes, Maxwell, second law) | PH (PH.O.A1.1, A1.2, A1.3, A1.4b) |
| Band theory and device physics below the device curve | PH.O.A4.4a |
| Reaction mechanism, thermochemistry, electrochemical equilibrium | CH.O.A3.1, CH.O.A4.2 |
| Rock and soil genesis, site history, groundwater as earth state | EA.O.A1, EA.O.A4 |
| Theorem: probability, queueing, optimisation, control stability, information theory, numerical error | MA.O.A5, MA.B.C4, MA.B.C3 |
| Software, algorithm, protocol, information state | CS.O.A2.4, CS.M.3 |
| Tissue function, organism in production | BI |
| Clinical outcome of a device | MD |
| Human performance | MS |
| Engineering education research | ED.B.C1 |
| Cost, price, allocation | EC; firm accounts and procurement practice BU |
| Contract, liability, regulation, licensure | LA |
| Public policy on infrastructure | PO |
| Engineering ethics as normative argument | PL |
| Engineering history and heritage | HI |
| Architectural aesthetic judgement | AR |
| Teamwork, communication, lifelong learning (Washington Accord WA8, WA9, WA11) | not claims; refused as competences |

## 10. External crosswalk

Primary authority: ANZSRC 2020 Fields of Research, Division 40 Engineering (checked: https://sear.unisq.edu.au/view/for2020/for2020=5F40.html). Secondary: ABET Criteria for Accrediting Engineering Programs 2025–26, 31 program criteria (audit §5).

ANZSRC Division 40 groups. "4099 Other engineering" is a residual and is not a cell. All 19 named groups, 4001–4019, confirmed (checked 9 Oct 2026, ABS anzsrc2020_for.xlsx).

| ANZSRC group | EN home | status |
|---|---|---|
| 4001 Aerospace engineering | EN.B.C2 | lands |
| 4002 Automotive engineering | EN.B.C2 | lands |
| 4003 Biomedical engineering | substrate rule on C1–C4 | lands (substrate) |
| 4004 Chemical engineering | EN.B.C4 | lands |
| 4005 Civil engineering | EN.B.C1 | lands |
| 4006 Communications engineering | EN.B.C3; capacity uses MA.B.C4 | lands |
| 4007 Control engineering, mechatronics and robotics | EN.M.B3 + EN.B.C2 | lands |
| 4008 Electrical engineering | EN.B.C3 | lands |
| 4009 Electronics, sensors and digital hardware | EN.O.A4.4 + EN.B.C3 | lands |
| 4010 Engineering practice and education | practice → EN.M.B5; education research → ED | split, lands |
| 4011 Environmental engineering | EN.B.C1 | lands |
| 4012 Fluid mechanics and thermal engineering | EN.O.A2, EN.O.A3 | lands |
| 4013 Geomatic engineering | EN.B.C1 (surveying); geodesy uses EA | lands |
| 4014 Manufacturing engineering | EN.M.B4 + EN.B.C5 | lands |
| 4015 Maritime engineering | EN.B.C2 (marine), EN.O.A2.3 | lands |
| 4016 Materials engineering | EN.O.A5.3 + EN.B.C4 | lands |
| 4017 Mechanical engineering | EN.B.C2 | lands |
| 4018 Nanotechnology | EN.O.A5.3 at nanoscale; physics of the effect uses PH | partial: no nanoscale sub-cell yet |
| 4019 Resources engineering and extractive metallurgy | EN.B.C4 | lands |

Coverage: 18 of 19 named groups land fully; 1 partial (4018). 0 refused. 4099 is residual and excluded.

ABET program criteria (31). After the re-cut, the seven "missing" criteria in the audit now land: cybersecurity engineering (C3, uses CS), engineering physics (curriculum; its claims land on Face O cells; no bridge), fire protection (C1, EN.O.A3.4), geological (C4 with rock mechanics; genesis uses EA), naval architecture/marine/ocean (C2, EN.O.A2.3), optical/photonic (C3, EN.O.A4.3.4), surveying (C1). Mining now has rock mechanics (EN.O.A1.3.7). Coverage: 30 of 31 land on a cell, bridge or substrate rule; engineering physics is accounted for as a curriculum, not a bridge. Partial placements remaining: architectural (building services only via C1/A3), engineering management (C5; finance uses BU). These counts are from the audit list and are not re-checked against abet.org here.

## 11. Validation

Sizes:
- Key line (Face O): 5.
- Face O cells: 5 A-level + 22 sub-cells = 27 (A1: 4, A2: 5, A3: 4, A4: 4, A5: 5). Named objects (EN.O.Ax.y.z) are leaves, not counted as cells.
- M roles: 5. Sub-groups: B1 3, B2 4, B3 4, B4 4, B5 3.
- Heuristics: 10 (outside count).
- W rows: 27.
- B bridges: 5.

All groups lie within 2–5.

Key-line members, word for word: force and deformation; mass and momentum; energy and entropy; electromagnetic state; composition and microstructure.

Open problems (OPEN):
- OPEN: turbulence closure — no general predictive model of turbulent stress for engineering flows; RANS closures are calibrated models (EN.O.A2).
- OPEN: fatigue under variable-amplitude loading — sequence effects lack a general predictive law (EN.O.A1.3.6).
- OPEN: human reliability quantification — current numbers are heuristic (EN.B.C5; uses MS).

Contested placements (CONTESTED, with alternative):
- CONTESTED: Fourier conduction EN.O.A3.3.1; alternative PH.O.A4.1.
- CONTESTED: Darcy's law EN.O.A2.5.1; alternative EA.O.A4.
- CONTESTED: Hertz contact EN.O.A1.4.1; alternative PH.O.A1.5.
- CONTESTED: Mohr–Coulomb and effective stress EN.O.A1.3.7; alternative EA.O.A1.
- CONTESTED: information state refused to CS; alternative is a sixth EN balance (v1). Rejected because CS owns the state models and a sixth member is not needed.
- CONTESTED: operation folded into EN.M.B4 (actions) and EN.M.B5 (in-service integrity); alternative is a separate "operate and sustain" role, which would give six roles and need regrouping.
- CONTESTED: biomedical and agricultural as substrate rules; alternative is separate bridges (ABET and ANZSRC list biomedical separately).

## 12. Registry rows

| ID | label | home (face/cell) | uses |
|---|---|---|---|
| EN.O.A1 | Force and deformation | O | — |
| EN.O.A1.1 | Rigid bodies | O.A1 | PH.O.A1.1 |
| EN.O.A1.1.1 | Free-body diagram, determinacy | O.A1.1 | — |
| EN.O.A1.1.2 | Mechanism dynamics | O.A1.1 | PH.O.A1.1 |
| EN.O.A1.1.3 | Lumped vibration models | O.A1.1 | MA.O.A4 |
| EN.O.A1.2 | Slender members | O.A1 | — |
| EN.O.A1.2.1 | Euler–Bernoulli beam | O.A1.2 | — |
| EN.O.A1.2.2 | Timoshenko beam | O.A1.2 | — |
| EN.O.A1.2.3 | Torsion of circular shaft | O.A1.2 | — |
| EN.O.A1.2.4 | Euler column buckling | O.A1.2 | — |
| EN.O.A1.2.5 | Kirchhoff–Love and Mindlin–Reissner plates | O.A1.2 | — |
| EN.O.A1.2.6 | Thin-walled pressure vessel | O.A1.2 | — |
| EN.O.A1.3 | Deformable continua | O.A1 | PH.O.A1.5 |
| EN.O.A1.3.1 | Cauchy stress and traction | O.A1.3 | PH.O.A1.5 |
| EN.O.A1.3.2 | Isotropic linear elasticity (Hooke) | O.A1.3 | PH.O.A1.5 |
| EN.O.A1.3.3 | Tresca and von Mises yield | O.A1.3 | — |
| EN.O.A1.3.4 | Mohr's circle | O.A1.3 | MA.O.A2 |
| EN.O.A1.3.5 | LEFM, KIc | O.A1.3 | — |
| EN.O.A1.3.6 | Fatigue life, Paris law | O.A1.3 | — |
| EN.O.A1.3.7 | Effective stress, Mohr–Coulomb (CONTESTED) | O.A1.3 | EA.O.A1 |
| EN.O.A1.4 | Contact interfaces | O.A1 | — |
| EN.O.A1.4.1 | Hertz contact (CONTESTED) | O.A1.4 | — |
| EN.O.A1.4.2 | Coulomb friction | O.A1.4 | — |
| EN.O.A1.4.3 | Archard wear | O.A1.4 | — |
| EN.O.A1.4.4 | Contact and member concepts | O.A1.4 | — |
| EN.O.A2 | Mass and momentum | O | PH.O.A1.5 |
| EN.O.A2.1 | Internal flows | O.A2 | PH.O.A1.5 |
| EN.O.A2.1.1 | Bernoulli (applied) | O.A2.1 | PH.O.A1.5 |
| EN.O.A2.1.2 | Darcy–Weisbach | O.A2.1 | — |
| EN.O.A2.1.3 | Colebrook, Moody, minor losses | O.A2.1 | — |
| EN.O.A2.1.4 | Pump–system matching, affinity laws | O.A2.1 | — |
| EN.O.A2.1.5 | Reynolds lubrication equation | O.A2.1 | — |
| EN.O.A2.1.6 | Euler turbomachine equation | O.A2.1 | — |
| EN.O.A2.1.7 | Joukowsky surge | O.A2.1 | — |
| EN.O.A2.2 | External flows | O.A2 | PH.O.A1.5 |
| EN.O.A2.3 | Free-surface flows | O.A2 | — |
| EN.O.A2.3.1 | Specific energy, Froude number | O.A2.3 | — |
| EN.O.A2.3.2 | Manning equation | O.A2.3 | — |
| EN.O.A2.3.3 | Ship hydrostatics and stability | O.A2.3 | — |
| EN.O.A2.3.4 | Hull resistance, seakeeping | O.A2.3 | — |
| EN.O.A2.4 | Compressible and acoustic flows | O.A2 | PH.O.A4.1 |
| EN.O.A2.4.1 | Isentropic nozzle, choking | O.A2.4 | — |
| EN.O.A2.4.2 | Normal-shock relations | O.A2.4 | — |
| EN.O.A2.4.3 | Linear acoustics | O.A2.4 | PH.O.A1.5 |
| EN.O.A2.5 | Porous-medium flows | O.A2 | — |
| EN.O.A2.5.1 | Darcy's law (CONTESTED) | O.A2.5 | — |
| EN.O.A2.5.2 | Ergun equation | O.A2.5 | — |
| EN.O.A2.5.3 | Terzaghi consolidation | O.A2.5 | — |
| EN.O.A3 | Energy and entropy | O | PH.O.A4.1 |
| EN.O.A3.1 | First-law balances | O.A3 | PH.O.A4.1 |
| EN.O.A3.1.1 | Steady open first law | O.A3.1 | PH.O.A4.1 |
| EN.O.A3.1.2 | Property closures | O.A3.1 | — |
| EN.O.A3.1.3 | Power and refrigeration cycles | O.A3.1 | — |
| EN.O.A3.2 | Second-law limits | O.A3 | PH.O.A4.1 |
| EN.O.A3.2.1 | Carnot efficiency (applied) | O.A3.2 | PH.O.A4.1 |
| EN.O.A3.2.2 | Exergy | O.A3.2 | — |
| EN.O.A3.2.3 | Pinch analysis | O.A3.2 | — |
| EN.O.A3.3 | Heat-transfer rates | O.A3 | — |
| EN.O.A3.3.1 | Fourier conduction (CONTESTED) | O.A3.3 | — |
| EN.O.A3.3.2 | Newton cooling, Nusselt correlations | O.A3.3 | — |
| EN.O.A3.3.3 | Radiation exchange | O.A3.3 | PH.O.A4.1 |
| EN.O.A3.3.4 | LMTD, effectiveness–NTU | O.A3.3 | — |
| EN.O.A3.3.5 | Fins | O.A3.3 | — |
| EN.O.A3.4 | Reacting energy | O.A3 | CH.O.A3.1 |
| EN.O.A4 | Electromagnetic state | O | PH.O.A1.2b |
| EN.O.A4.1 | Lumped circuits | O.A4 | PH.O.A1.2b |
| EN.O.A4.1.1 | Ohm, Kirchhoff (applied) | O.A4.1 | PH.O.A1.2b |
| EN.O.A4.1.2 | Impedance and phasors | O.A4.1 | — |
| EN.O.A4.1.3 | Thévenin and Norton | O.A4.1 | — |
| EN.O.A4.1.4 | Maximum power transfer (conjugate) | O.A4.1 | — |
| EN.O.A4.1.5 | LTI response, state space | O.A4.1 | MA.O.A4 |
| EN.O.A4.1.6 | Sampling theorem (applied) | O.A4.1 | MA.B.C4 |
| EN.O.A4.1.7 | Circuit concepts | O.A4.1 | — |
| EN.O.A4.2 | Electromechanical conversion | O.A4 | PH.O.A1.2b |
| EN.O.A4.2.1 | Magnetic circuit | O.A4.2 | — |
| EN.O.A4.2.2 | Ideal transformer | O.A4.2 | — |
| EN.O.A4.2.3 | Machines, synchronous speed, slip | O.A4.2 | — |
| EN.O.A4.2.4 | AC power-flow equations | O.A4.2 | — |
| EN.O.A4.3 | Distributed fields | O.A4 | PH.O.A1.2b |
| EN.O.A4.3.1 | Transmission line | O.A4.3 | — |
| EN.O.A4.3.2 | Waveguides and antennas | O.A4.3 | — |
| EN.O.A4.3.3 | Friis transmission | O.A4.3 | — |
| EN.O.A4.3.4 | Optical and photonic devices | O.A4.3 | PH.O.A1.2c |
| EN.O.A4.3.5 | EMC, skin effect | O.A4.3 | — |
| EN.O.A4.4 | Semiconductor devices | O.A4 | PH.O.A4.4a |
| EN.O.A4.4.1 | Diode and MOSFET curves | O.A4.4 | PH.O.A4.4a |
| EN.O.A4.4.2 | Drift–diffusion device model | O.A4.4 | PH.O.A4.4a |
| EN.O.A4.4.3 | Digital abstraction | O.A4.4 | CS.O.A2.4 |
| EN.O.A4.4.4 | Switching converters | O.A4.4 | — |
| EN.O.A5 | Composition and microstructure | O | — |
| EN.O.A5.1 | Reaction rates | O.A5 | CH.O.A4.2 |
| EN.O.A5.1.1 | Species balance | O.A5.1 | — |
| EN.O.A5.1.2 | Ideal reactors, RTD | O.A5.1 | — |
| EN.O.A5.1.3 | Arrhenius (applied) | O.A5.1 | CH.O.A4.2 |
| EN.O.A5.1.4 | Scale-up limits | O.A5.1 | — |
| EN.O.A5.2 | Equilibrium stages | O.A5 | CH.O.A3.1 |
| EN.O.A5.2.1 | Raoult, fugacity (applied) | O.A5.2 | CH.O.A3.1 |
| EN.O.A5.2.2 | McCabe–Thiele | O.A5.2 | — |
| EN.O.A5.2.3 | Two-film theory | O.A5.2 | — |
| EN.O.A5.2.4 | Flowsheet degrees of freedom | O.A5.2 | — |
| EN.O.A5.3 | Microstructure–property relations | O.A5 | — |
| EN.O.A5.3.1 | Phase diagram (applied) | O.A5.3 | CH.O.A3.1 |
| EN.O.A5.3.2 | TTT and CCT diagrams | O.A5.3 | — |
| EN.O.A5.3.3 | Hall–Petch | O.A5.3 | — |
| EN.O.A5.3.4 | Rule of mixtures bounds | O.A5.3 | — |
| EN.O.A5.3.5 | Dislocation slip | O.A5.3 | PH.O.A4.4 |
| EN.O.A5.4 | Electrochemical cells | O.A5 | CH.O.A3.1 |
| EN.O.A5.4.1 | Faraday's laws of electrolysis (applied) | O.A5.4 | CH.O.A3.1 |
| EN.O.A5.4.2 | Nernst equation (applied) | O.A5.4 | CH.O.A3.1 |
| EN.O.A5.4.3 | Battery and fuel-cell models | O.A5.4 | — |
| EN.O.A5.4.4 | Passivation | O.A5.4 | — |
| EN.O.A5.5 | Neutron balances | O.A5 | PH |
| EN.O.A5.5.1 | k_eff, criticality | O.A5.5 | — |
| EN.O.A5.5.2 | Neutron diffusion equation | O.A5.5 | — |
| EN.O.A5.5.3 | Decay heat | O.A5.5 | — |
| EN.O.A5.5.4 | Shielding attenuation | O.A5.5 | — |
| EN.M.B1 | Specification | M | — |
| EN.M.B2 | Analysis | M | MA.B.C3 |
| EN.M.B3 | Synthesis | M | MA.B.C4 |
| EN.M.B4 | Making | M | — |
| EN.M.B5 | Assurance | M | MA.O.A5 |
| EN.H.1–EN.H.10 | Heuristics register entries | H | — |
| EN.B.C1 | Civil and environmental engineering | B | EA, AR, EC |
| EN.B.C2 | Mechanical, aerospace and marine engineering | B | PH |
| EN.B.C3 | Electrical and electronic engineering | B | CS.O.A2.4, CS.M.3 |
| EN.B.C4 | Chemical, materials and resources engineering | B | CH, EA |
| EN.B.C5 | Industrial and systems engineering | B | MA.O.A5, MA.B.C4, MS, EC, BU |
| (ext) Newtonian mechanics | cited | PH.O.A1.1 | PH.O.A1.1 |
| (ext) Navier–Stokes, Bernoulli, Reynolds number, Hooke | cited | PH.O.A1.5 | PH.O.A1.5 |
| (ext) Second law, Carnot | cited | PH.O.A4.1 | PH.O.A4.1 |
| (ext) Maxwell, Faraday induction, Kirchhoff laws | cited | PH.O.A1.2b | PH.O.A1.2b |
| (ext) Band theory | cited | PH.O.A4.4a | PH.O.A4.4a |
| (ext) Arrhenius | cited | CH.O.A4.2 | CH.O.A4.2 |
| (ext) Raoult, Nernst, Faraday electrolysis | cited | CH.O.A3.1 | CH.O.A3.1 |
| (ext) Shannon–Hartley, sampling theorem | cited | MA.B.C4 | MA.B.C4 |
| (ext) Little's law, Weibull, system reliability | cited | MA.O.A5 | MA.O.A5 |
| (ext) LP duality, Lyapunov, Nyquist, Routh–Hurwitz | cited | MA.B.C4 | MA.B.C4 |
| (ext) FE/FV/Monte Carlo error theory | cited | MA.B.C3 | MA.B.C3 |
| (ext) Navier–Stokes existence and regularity | cited | MA.O.A4 | MA.O.A4 |
| (ext) Boolean function, machine state | cited | CS.O.A2.4 | CS.O.A2.4 |

## 13. Self-check against R1–R12

| rule | PASS/FAIL | if FAIL: failing sentence and repair |
|---|---|---|
| R1 One home | FAIL (pilot) | "Claim 41 (design life) found no cell." Repair: add a requirements home (see Pilot finding). |
| R2 Counts exact | PASS | Section 11 sizes match sections 3–7. |
| R3 Heuristics outside count | PASS | EN.H is outside the five stages. |
| R4 Crosswalk with coverage | PASS (with caveat) | ANZSRC 40 confirmed (19 of 19 named groups); ABET figures are carried from the audit, not re-checked. |
| R5 Hypotheses stated | FAIL | "Basquin (stress-life) and Coffin–Manson (strain-life) relations, fitted per material." Repair: add hypotheses (constant-amplitude, fully reversed loading, specimen conditions). Also "Archard wear law" lacks the regime hypothesis (dry sliding, mild wear). |
| R6 Open and contested labelled | PASS | Three OPEN, seven CONTESTED in section 11. |
| R7 Word-for-word members | PASS | Section 2, 3 and 11 use identical member wording. |
| R8 Scope boundary | PASS | Section 9. |
| R9 First descent | PASS | Every A-cell has SCQA, key line and named objects. Face M roles have key lines but no SCQA (not required by R9 for Face M). |
| R10 Register, sentence length | FAIL (minor) | Some table cells and list items exceed 25 words, e.g. the EN.B.C1 "named field" cell. Repair: split sub-bridge lists into a separate column or list. |
| R11 Facts checked and cited | FAIL (partial) | Archard notation is UNVERIFIED; Joukowsky and Shockley statements are from general knowledge without a cited text. Repair: cite a standard text (e.g., Wylie and Streeter for surge; Sze for diodes). |
| R12 Stable IDs | PASS | All IDs follow EN.face.cell. |

### Pilot finding (Phase 2.2), open
Claim 41 ("design life is 100 years under the bridge manual") found no cell. The key line is a set of physical balances, so stated requirements and design lives have no Face O home. Two of three coders forced the claim into EN.O.A1. R1 fails for requirement claims until this is repaired. Candidate repairs: add a requirements partition alongside the balances, or file specifications under EN.M.B5 (verification) with warrant W12. Decision pending.
