# ST — top-down Minto pyramid

Built by scripts/minto_pass.py from the grouped classification. Three rules (Minto pp. 9-11): each summary states the idea of its group, members are the same kind of idea, and they are in a stated order.

## Introduction

**Situation.** Strategy studies how opposing parties contend through organised force.

**Complication.** The knowledge is scattered across military, naval, weapons and detection headings that obscure which feature of the contest each one explains.

**Question.** How is everything in strategy divided?

**Answer.** Strategy is divided by the feature of the strategic situation that a claim explains, namely the actors who contend, the game they play, the coercion they apply, the conduct of their operations, and the information each side holds.

## Governing thought

Strategy is divided by the feature of the strategic situation that a claim explains, namely the actors who contend, the game they play, the coercion they apply, the conduct of their operations, and the information each side holds.

## Key line

Group of features of the strategic situation. Basis: kinds. Dimension: the feature of the strategic situation that the claim explains. Order: structure. The pillars run from who contends, to the setting of the contest, to the force applied, to how it is carried out, to what each side knows.

1. Actors are the forces, organisations and personnel that contend in a strategic situation, and their administration and organisation explain who contends. `ST.K1`
2. The game is the strategic setting of conflict, defence and operational planning that gives the contest its structure. `ST.K2`
3. Coercion is the destructive force that actors apply through weapons, munitions and their physical effects. `ST.K3`
4. Conduct is the way actors carry out operations through service branches, supply, maintenance and engineering. `ST.K4`
5. Information is what each side senses, locates, learns and denies, through detection, locating, intelligence and countermeasures. `ST.K5`

## Groups

### 1. Actors are the forces, organisations and personnel that contend in a strategic situation, and their administration and organisation explain who contends.

- **Military forces and their organisation and administration explain how armed actors are constituted and governed.**
  _basis: kinds, order: structure. From forces in general to their administration._
  - Military Forces and Organizations
  - Armies: Organization, distribution, military situation
  - Military administration
  - Navies: Organization, distribution, naval situation
  - Naval administration
- **Naval and marine personnel are the human actors who crew and serve in naval forces.**
  _basis: kinds, order: structure. From seamen to marines._
  - Naval seamen
  - NAVAL PERSONNEL
  - Marines

### 2. The game is the strategic setting of conflict, defence and operational planning that gives the contest its structure.

- **Conflict and defence research fields are scholarly disciplines that study war, civil conflict and defence as features of the strategic situation.**
  _basis: kinds, order: structure. Parallel academic fields; no ranking implied._
  - Defence studies
  - Civil war
  - Conflict research
- Conflict Processes
- Peace studies
- **Defense and operations frameworks are the strategic-level arrangements for protecting a population and for planning and conducting military action.**
  _basis: kinds, order: structure. Ordered from civil protection through defense systems to operational strategy and tactics._
  - Civil Defense
  - Defense Systems
  - Military Operations, Strategy and Tactics

### 3. Coercion is the destructive force that actors apply through weapons, munitions and their physical effects.

- **Weapon technologies and munitions are the kinds of armament that deliver destructive force against targets.**
  _basis: kinds, order: structure. From strategic weapon classes to airborne munitions and naval ordnance._
  - **Weapons technologies are classes of armament whose destructive capability shapes the strategic balance between states.**
    _basis: kinds, order: structure. Parallel weapon types; no ranking implied._
    - Nuclear Weapons
    - Directed Energy Weapons
    - Guided Munitions
  - **Guided missiles, rockets, and aerial bombs are distinct kinds of airborne munitions that deliver explosive force against targets.**
    _basis: kinds, order: structure. Ordered by structure of the delivery mechanism: guided propulsion, unguided propulsion, unpowered drop._
    - Guided Missiles
    - Rockets
    - Aerial Bombs
  - Naval ordnance
- **Combat vehicles, armor, guns and fire control are the land and bombing platforms that bring firepower to bear.**
  _basis: kinds, order: structure. From vehicles and armor to guns and fire control._
  - Combat Vehicles
  - Armor
  - Guns
  - Fire Control and Bombing Systems
- **Missile technology and explosive and ballistic science explain how coercive force is launched, travels and detonates.**
  _basis: kinds, order: structure. From launching to trajectories, warheads, reentry and the physics of explosions._
  - Guided Missile Launching and Basing Support
  - Guided Missile Trajectories, Accuracy and Ballistics
  - Guided Missile Warheads and Fuzes
  - Guided Missile Reentry Vehicles
  - **Explosive effects and ballistic science are the physical phenomena and materials that explain how munitions detonate and travel.**
    _basis: kinds, order: structure. Ordered by structure from the explosive materials to the underwater application, the explosion phenomenon, and ballistics._
    - Ammunition and Explosives
    - Underwater Ordnance
    - Explosions
    - Ballistics

### 4. Conduct is the way actors carry out operations through service branches, supply, maintenance and engineering.

- **Land combat branches and engineering are the arms through which armies conduct operations.**
  _basis: kinds, order: structure. From infantry and cavalry to artillery and engineering._
  - Infantry
  - Cavalry. Armor
  - Artillery
  - Military engineering. Air forces
  - MILITARY ENGINEERING
- **Logistics, maintenance and support services sustain forces so that operations can continue.**
  _basis: kinds, order: structure. From supply to maintenance and minor services._
  - Logistics, Military Facilities and Supplies
  - Maintenance and transportation
  - Naval maintenance
  - Minor services of navies

### 5. Information is what each side senses, locates, learns and denies, through detection, locating, intelligence and countermeasures.

- **Detection technologies sense targets through sound, light, radio, magnetic and seismic energy.**
  _basis: kinds, order: structure. From medium-specific to other detection kinds._
  - **Medium-specific detection kinds sense targets through sound, light, or radio-wave energy.**
    _basis: kinds, order: structure. Ordered by sensing medium: acoustic, optical, radar._
    - Acoustic Detection and Detectors
    - Optical Detection and Detectors
    - Active and Passive Radar Detection Equipment
  - Non-acoustic and Non-magnetic Submarine Detection
  - Magnetic and Electric Field Detection and Detectors
  - Seismic Detection and Detectors
  - Miscellaneous Detection and Detectors
- **Locating, intelligence and countermeasures determine where targets are and exploit or defeat an opponent's detection.**
  _basis: kinds, order: structure. From locating, to gathering intelligence, to defeating the opponent's sensing._
  - **Locating functions determine where a target or the own platform is, through bearing, range, position, and guidance.**
    _basis: kinds, order: structure. Ordered from bearing-only to full range and position fixing and guidance._
    - Direction Finding
    - Target Direction,Range and Position Finding
    - Navigation and Guidance
  - Military Intelligence
  - Navigation, Detection and Countermeasures
  - Countermeasures

## Checks

- minto_check: clean
- field_check holds: True — Misplaced: P3.1.1.3 Guided Munitions duplicates P3.1.2.1; P3.3.5.2 Underwater Ordnance belongs with P3.1.3; P4.1.4 air forces, P4.1.2 Armor, P5.2.3 mixed.
