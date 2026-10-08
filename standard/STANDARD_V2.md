# Pyramids of Knowledge — Conformance Standard v2 (working brief)

Source material (plain text extracted from Chris Townsend's PDFs):
- Method spec: /tmp/claude-0/-home-claude/91cbbc6c-1841-5867-af1c-b60b9f7449b5/scratchpad/method.txt (the Minto method: vertical rule, horizontal rule, MECE, 2–5 members, four orders, SCQA, no "Other", summaries state a message)
- Twelve-field volume: /tmp/claude-0/-home-claude/91cbbc6c-1841-5867-af1c-b60b9f7449b5/scratchpad/twelve.txt
  Line ranges: navigator + staffing map 1–150 · Mathematics 151–228 · Physics 229–1181 · Chemistry 1182–1516 · Biology 1517–1808 · Earth (geography and geology) 1809–2060 · Engineering 2061–2607 · Computer science 2608–3008 · Medicine and the drug 3009–3235 · Mind, brain and society 3236–3463 · Economics 3464–3729 · Business, trade, tax, accounting 3730–3917 · Politics 3918–4172 · Law 4173–4363 · Philosophy 4364–4796
- Four-layer mathematics pyramid reconciled with MSC2020: /tmp/claude-0/-home-claude/91cbbc6c-1841-5867-af1c-b60b9f7449b5/scratchpad/math.txt

## What v1 already does (keep it)
Each field pyramid has: an SCQA; a governing thought "X is exhausted by two sides of one pyramid"; Side A = claims/objects divided by one named dimension (regime, question, scale, balance, layer, function, unit, range, relation, claim-type); Side B = method roles; Side C = named fields/disciplines as "bridges" (a community pairing a claim-cell with a subset of methods, sometimes on a substrate); assignment rules; a crosswalk table ("one home each"); validation; "how to place a new object". The unit of classification is the CLAIM (a sentence), not the document or topic. Cross-field boundary rules ("incidence is economics, the duty is law") are the core asset.

## v2 architecture: four faces per pyramid
1. **Face O — Objects (claims).** Every claim-cell answers "what is this claim about?", divided by ONE named dimension, 2–5 members at each level, no "Other".
2. **Face M — Methods.** Every method role is mapped to one of SEVEN shared method roles, so the twelve method sides translate into each other:
   - M1 Represent (define, name, formalize, specify, notate, map, nomenclature)
   - M2 Derive (prove, analytical solution, argument, interpretation of a text, strategic/formal model solved)
   - M3 Observe (observe, measure, survey, field record, examine, date)
   - M4 Intervene (experiment, perturb, synthesize, construct, make, treat)
   - M5 Compute (algorithm, simulation, numerical model, fitted model)
   - M6 Compare and reconstruct (comparative method, phylogeny, case comparison, historical reconstruction, hermeneutic interpretation)
   - M7 Verify (test against specification, audit, assurance, peer review, adjudication)
   Heuristics are ALWAYS a labelled register outside the role count (the engineering rule), never a sixth role, never inside the 2–5 count.
3. **Face W — Warrant.** For every claim-cell: the warrant type it owes (from the controlled list below), its standard of acceptance, and its typical defeaters.
   Controlled warrant types: W1 Proof from stated assumptions · W2 Computation with stated error bound · W3 Controlled intervention (experiment, trial) · W4 Measurement/observation with stated uncertainty · W5 Causal identification from observational data · W6 Comparative inference (cases, lineages, cross-cultural) · W7 Source criticism of a dated record (documents, artefacts, strata) · W8 Interpretation traced to a record · W9 Argument (premises, inference, replies to objections) · W10 Valid source plus proof of facts to a standard before a forum (law) · W11 Verification against a specification · W12 Stipulation or convention (definitions, nomenclature, standards bodies) · W13 Tradition-internal authority (scripture, creed, canon, school) — legitimate inside theology and confessional practice, never transferable to another face.
4. **Face B — Bridges.** Named fields, departments, specialties = (claim-cell or boundary) × (method subset) × (substrate). Sectors and catalogues (a country, a species, a hospital) are not cells.

## Global rules (the conformance checklist)
- R1 One sentence, one home: every named result has ONE owning pyramid + face + cell. Other pyramids cite it as "uses [owner id]". The registry holds owners.
- R2 Counts are exact: the stated count in the key line, the listed members, and the validation "sizes" must agree.
- R3 Heuristics register sits outside the method count, in every pyramid.
- R4 Each pyramid has a crosswalk to its field's authoritative external scheme (e.g. MSC2020, PhySH, ACS/IUPAC, NSF BIO, ACM CCS 2012 + CS2023, MeSH/ICD, APA/ASA, JEL, APSA, PhilPapers, LCSH/LCC) with a coverage statement (how many of the authority's top-level classes land, which are refused and why).
- R5 Every named theorem, law or formula is stated with its hypotheses (a missing hypothesis is an error, e.g. Gödel without "effectively axiomatised").
- R6 Open problems and programmes are labelled as such; contested placements are flagged with the alternative.
- R7 Governing thought, key line and validation must agree word for word on the members.
- R8 Every pyramid states its scope boundary: what it refuses and which pyramid owns it.
- R9 Depth target per pyramid: master + first descent (each key-line child has SCQA + key line + named objects) is the minimum for v2; full leaf descent is v3.
- R10 Plain academic register. The Minto discipline governs structure; no self-sealing rhetoric (no "objection pre-diagnosed as one-sided"). Every placement must be something a specialist could disagree with and test.
- R11 Facts checked against primary or authoritative sources; citations recorded.
- R12 Stable IDs: field code (MA, PH, CH, BI, EA, EN, CS, MD, MS, EC, BU, PO, LA, PL, plus new fields) + face + cell, e.g. PH.O.A2.3.

## Output format for audits and prototypes
Markdown. Concise, specific, plain words, sentences under 25 words. Tables where items × attributes. No filler.
