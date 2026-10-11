# Taxonomy Standard v3: an instrument for applying knowledge

Status: draft, 11 October 2026. It supersedes the purpose statement of Standard v2. The v2 rules R1–R12 still govern the content of the pyramids, except where amended below.

## 1. Purpose
Taxonomy exists to let a person or an AI apply knowledge to a problem. It covers three scales: the whole of knowledge, a whole field, and the distant parts of a field. Classifying claims is one operation among several, not the purpose.

## 2. Modes
| Mode | Input | Output |
|---|---|---|
| **Survey** | a subject, design, decision or question | what each relevant field sees; blind spots; a Minto synthesis |
| **Consult** | a problem and one field | every subfield swept; routes ranked by promise, cost and certainty |
| **Connect** | a precisely defined problem | tools from distant subfields whose signature matches, with their conditions checked |
| **Check** | a text or AI answer | each claim with its owner field and the warrant it needs (the v2 classifier) |
| **Zoom** | anything | example of / examples / part of / parts (after Steve Andreas), over the maps |

## 3. Scales
Knowledge → field (25) → cell (key line, 2–5 per field) → subfield (from the field's map) → topic → tool. Each level is a pyramid; the same operations work at every level.

## 4. Amendments to v2
- **R1 (one home) is scoped to Check mode and to registry IDs.** In Survey, Consult and Connect, a subject is expected to have many lenses, and an answer may live in several subfields.
- **R13 Coverage.** In Consult mode, every subfield in the field's map is considered, and each is either applied or explicitly set aside with a reason. No silent skipping.
- **R14 Conditions before use.** A tool or theorem proposed in Connect or Consult lists its hypotheses, and states whether the problem meets each one (yes / no / unknown).
- **R15 Verification status.** Every route carries one of: proposed, conditions checked, source found, tested. Nothing is shown as established without a source.
- **R16 Provenance.** Every run is recorded: problem, signature, nodes consulted, findings, sources, status.
- **R17 Maps follow authorities where they exist.** A field's subfield map comes from its authority scheme where one exists and its licence allows it: MSC2020 for mathematics, PhySH for physics, MeSH for medicine, ACM CCS for computing, JEL for economics. Otherwise it comes from ANZSRC 2020 fields. Licences are recorded per map.

## 5. Objects
- **Lens card:** per field and per cell. Question; what to look for; how to find out; what settles it and what breaks it; rules of thumb; collisions.
- **Map node:** a subfield in a field's map.
- **Toolkit card:** per map node or tool. Problems it solves; signature; flagship methods with hypotheses; inputs; outputs; famous cross-uses.
- **Problem signature:** the abstract shape of a problem, in the controlled vocabulary of `signatures/vocabulary.json`.
- **Run record:** provenance for every answer.

JSON schemas are in `schemas/`.

## 6. Unchanged
R5 (hypotheses in the sentence), R6 (OPEN and CONTESTED labelled), R10 (plain register), R11 (facts checked), R12 (stable IDs), W13 non-transfer, and the Māori-led review gate for IK all stand.
