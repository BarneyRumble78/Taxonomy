# Taxonomy Standard v3: an instrument for applying knowledge

Status: draft, 11 October 2026. It supersedes the purpose statement of Standard v2. The v2 rules R1–R12 still govern the content of the pyramids, except where amended below. Section 4a, the ClaimGuard rules, is also draft, dated 17 October 2026.

## 1. Purpose
Taxonomy exists to let a person or an AI apply knowledge to a problem. It covers three scales: the whole of knowledge, a whole field, and the distant parts of a field. Classifying claims is one operation among several, not the purpose.

## 2. Modes
| Mode | Input | Output |
|---|---|---|
| **Survey** | a subject, design, decision or question | what each relevant field sees; blind spots; a Minto synthesis |
| **Consult** | a problem and one field | every subfield swept; routes ranked by promise, cost and certainty |
| **Connect** | a precisely defined problem | tools from distant subfields whose signature matches, with their conditions checked |
| **Check** | a text or AI answer | each atomic claim, its home, and one verdict (R18). The verdict rules are draft. |
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

## 4a. ClaimGuard (draft)

This section amends R1 and R15 for Check mode. It adds R18–R22. It is draft. A verdict is never the word true.

### Amendments

- **R1 (amended).** One sentence, one home. In Check mode, ClaimGuard first splits a sentence into atomic claims. Each atomic claim has one owning pyramid, face and cell. A compound sentence carries one verdict per atomic claim. A sentence verdict is the worst of its parts.
- **R15 (amended).** Every route carries one of: proposed, conditions checked, source found, tested. Every ClaimGuard claim also carries one verdict (R18). Nothing is shown as established without a source or a passed check. A model's conclusion is never established.

### Rules

- **R18 Verdicts.** Check mode gives each atomic claim exactly one verdict: supported, contradicted, overstated, contested, unverified or out of scope. Each verdict states its placement, the warrant required, the evidence held, the checks run and a reason. Where evidence is missing, the verdict is unverified. No verdict is true.
- **R19 Certainty matching.** A claim's stated certainty must not exceed the warrant its evidence holds. The certainty ceiling for each warrant is in the R19 table. A claim stated above its ceiling is overstated, even if it is otherwise correct.
- **R20 Evidence binding.** Support or contradiction from a source or a tool output is bound to an exact quoted span and its locator. The locator is a source id, a tool call id, or a URL. A claim about a tool's result is checked against that tool's output, not against the model's summary of it. A number in the claim must match the number in the span, within any stated tolerance.
- **R21 Contradiction.** A claim contradicts the standard when it conflicts with a registry entry's stated content or hypotheses. It contradicts a text when it conflicts with another claim in that text that holds a stronger warrant. A deterministic check that fails is a contradiction. A model's judgement alone is not.
- **R22 Advisory models.** A model may split claims, propose spans and propose verdicts. Every model output passes the status guard. A model output can only lower a verdict to unverified. It can never raise one to supported or contradicted. On the Worker, a paid model runs only when VERIFY_MODEL=1. That flag stays off. The Anthropic path still needs TAXONOMY_ADJUDICATE_PAID=1.

The verdicts are tested in this order. The first match wins.

| Order | Verdict | When it matches |
|---|---|---|
| 1 | out of scope | The engine abstains, the text is not a claim, or W13 is used outside its tradition. |
| 2 | contradicted | A shown check fails, or a quoted span entails the negation. A model-only contradiction stays unverified. |
| 3 | contested | The standard labels the result open or contested, or the evidence both supports and contradicts at one warrant. |
| 4 | overstated | Evidence is weaker than the certainty stated, a theorem omits its hypotheses, or an only or none claim rests on a small-case search alone. |
| 5 | supported | A cited span or a passed check meets the required warrant, and the certainty is within the ceiling. A small-case search alone is supported (small cases), not a proof. |
| 6 | unverified | Nothing above matched. This is the default. |

### R19 certainty ceilings (first draft)

| Warrant held | Ceiling | Wording it allows |
|---|---|---|
| W1, W11, W12 | absolute | is, always, proves, when a check or a stipulation is shown |
| W2, W3, W4, W5, W10 | assertive | shows, found, measured, with the uncertainty stated |
| W6, W7, W8, W9, W13 | qualified | suggests, indicates, argues, according to |
| none | hedged | hedged wording only |

An unhedged claim with no evidence is unverified. It is flagged certainty without evidence. It is not overstated, because overstated needs some evidence.

### Required warrant by claim type

The claim type wins over the field default when a type is detected. A forecast owes W9, argument, not W6, comparative inference. Skynet's earlier emulation used W6. This table is the contract.

| Claim type | Warrant |
|---|---|
| observation | W4 |
| event | W7 |
| attribution | W7 |
| causal | W5 |
| forecast | W9 |
| intent | W8 |
| legal | W10 |

### Tool outputs (first draft)

| Tool kind | Warrant held |
|---|---|
| calculator | W2 |
| test runner | W11 |
| sensor or API reading | W4 |
| search snippet | W7 |

A caller may declare a warrant on a source. Retrieval over the pyramids is context for placement. It is not evidence for supported.

Indigenous knowledge placements stay provisional until Māori-led review. For those claims the verdict is at most unverified or contested.

## 5. Objects
- **Lens card:** per field and per cell. Question; what to look for; how to find out; what settles it and what breaks it; rules of thumb; collisions.
- **Map node:** a subfield in a field's map.
- **Toolkit card:** per map node or tool. Problems it solves; signature; flagship methods with hypotheses; inputs; outputs; famous cross-uses.
- **Problem signature:** the abstract shape of a problem, in the controlled vocabulary of `signatures/vocabulary.json`.
- **Run record:** provenance for every answer.

JSON schemas are in `schemas/`.

## 6. Unchanged
R5 (hypotheses in the sentence), R6 (OPEN and CONTESTED labelled), R10 (plain register), R11 (facts checked), R12 (stable IDs), W13 non-transfer, and the Māori-led review gate for IK all stand.
