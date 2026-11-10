# Taxonomy v4: analysis and plan

Prepared 10 November 2026 on branch `v4-generative` (`911560d`). Status: proposal for Chris's review.
It responds to the handover of the same date. Figures are measured on this branch unless marked (UNVERIFIED).

## 1. Governing thought

Taxonomy can become a generative engine if it gains one thing it lacks: a shared formal layer.
Today the fields sit side by side. Nothing states that two tools in two fields are the same mathematics.
Build that layer through mathematics, prove it on one narrow slice for FLASH, then widen it to all 25 fields.

## 2. What the repo is today

| Asset | Measured | Reading |
|---|---|---|
| Pyramids | 25 fields, 990 registry IDs | Strong on ownership and warrants. Depth is uneven: 15 fields are under 2,700 words. |
| Mathematics | 2,030 words, no registry entries | The intended common language is among the thinnest fields. |
| Maps | 307,561 nodes | Wide, but they are other bodies' classifications, with mixed licences. |
| Toolkit cards | 63, mathematics only | Signatures average 2.3 of 14 facets. Tools carry one-line descriptions. |
| Connect | Facet overlap, one field | It cannot compare two fields, and the signatures are too coarse to separate tools. |
| Cross-field edges | 86 typed edges (WP1) | 38 of 82 citations come from EN. The edges hold no mappings yet. |
| Benchmark | 50 problems, never scored | The design is good. The evidence does not exist yet. |
| Tests | 234 pass, CI green | Sound base. |

## 3. Where I differ from the handover

The handover's rules and its insistence on honest evaluation are right. I would change five things.

### 3.1 The missing piece is an interlingua, not more cards
The handover scales the current card format to 25 fields. That format cannot support alignment.
A tool such as "Knot invariants: distinguish knots" has no typed parts to map onto another field.

I propose each tool carries a **formal core**:
- the mathematical structure it instantiates, as a pointer to an MA node;
- role bindings, which say what plays each role in this field;
- its assumptions, as separate checkable statements (R5 already requires them);
- its guarantee, which says what it delivers when the assumptions hold.

Two tools in different fields with the same formal core are a candidate correspondence.
This makes "mathematics as the common language" literal and machine-checkable.
It also needs about n links to mathematics, not n² pairwise edges.
The Kalman filter, Bayesian updating and data assimilation would meet at one MA node, each with its own bindings.

### 3.2 Tree distance is a weak heterogeneity metric on its own
Distance in a classification tree reflects how librarians grouped subjects. It does not reflect how systems fail.
Knight and Leveson's finding was that versions fail together on the same hard inputs.
A mechanism-based reading is that variants fail together when they share a violated assumption.

Taxonomy can compute that, because its tools list their assumptions. I propose testing three predictors, not one:
1. **Lineage distance:** shortest path through the pyramid tree and correspondence edges.
2. **Assumption distance:** one minus the overlap of the two variants' assumption sets.
3. **A null predictor:** a code-level difference measure with no knowledge content.

If assumption distance predicts failure correlation and tree distance does not, that is still a useful result for FLASH.

### 3.3 The planned FLASH test is under-powered
Four variants give six pairs. No test on six dependent pairs can support a claim.
I propose 8 to 10 variants (28 to 45 pairs), three plants for replication, and a Mantel permutation test.
Fault classes and thresholds would be fixed in the pre-registration, before any variant runs.

### 3.4 Retrodiction mostly measures recall
Time-slicing the cards does not help, because the local model already knows the famous answers.
A model trained after 2004 has read about compressed sensing. No pre-2004 model exists to test with.

I propose four responses:
- Report the gain over the no-Taxonomy baseline, with a paired test, never the raw score alone.
- Add a **signature-only arm**: the deterministic matcher sees facets only, so it cannot recall anything.
- Add a **prospective set**: cross-field results published after the model's training cut-off.
- State the limit plainly in the report.

At n = 30 a Wilson interval spans roughly ±17 points. Small effects will not be detectable, and the report should say so.

### 3.5 Slice first, then scale
The handover drafts cards for all 25 fields before the operator exists.
I would build one vertical slice end to end, then scale what works.
A timed local run gave 15.5 tokens a second on `qwen3.6:27b`, about 35 seconds a card.
One thousand cards is about ten hours of unattended running, so scale is not the constraint. Card quality is.

## 4. Risks to settle early

- **Licensing.** There is no licence file. MSC2020 is CC BY-NC-SA. The IEEE taxonomy is CC BY-NC-ND, which bars derivatives. ACM CCS and JEL are limited to non-commercial or scholarly use. ANZSRC is unconfirmed. This reading is mine and is not legal advice (UNVERIFIED). One option is a core that depends only on open schemes (PhySH, GCMD, LCC, MeSH) with the rest as optional add-ons.
- **Generated cards will contain errors.** I propose a random audit of 50 cards against sources, with the error rate reported.
- **Independence of the held-out set.** I have now read the cards. A set I draft in this session is not independent. A fresh session barred from `cards/`, or an outside author, would be cleaner.
- **Mathematics is not in the registry.** Registering MA sub-cells needs Chris's decision under R12.
- **Edge density is an authoring artefact.** EN looks close to everything because EN was written in most depth. Distance needs a stated correction.
- **"Provably equivalent" is beyond this work.** z3 can prove an invariant on a small linear model. It does not prove the Python code. The report must say that.

## 5. Plan

### Track A: FLASH slice, by 27 November
Scope: control and estimation tools across MA, EN, CS, PH, EC and BI. About 40 tools.

| Dates | Work | Done when |
|---|---|---|
| 10–12 Nov | Tool schema v2 with formal core, bindings, assumptions and guarantee. Cards for the slice, each sourced. Pre-registration for the FLASH experiment. | Cards validate. Pre-registration is committed before any run. |
| 12–15 Nov | Transfer operator v1: select, align, transfer, list mismatches, propose. Three distance measures, documented with their properties. | The operator runs on five pairs. Distances pass near-and-far tests. |
| 15–20 Nov | FLASH demonstrator: formal spec, 8–10 variants, three plants, property tests, z3 invariants where tractable, fault campaign, analysis. | The result is reported whichever way it falls. |
| 18–23 Nov | Development-set retrodiction with all baselines, run overnight. Signature-only arm. | Tables regenerate offline from logged runs. Cost ledger reads USD 0. |
| 23–27 Nov | Technical report and draft RFI notes for Chris. | Chris has both, with three days to review before 30 November. |

**Gate, 15 November.** If the operator's output on five pairs is not useful to read, the RFI notes present the concept and the metric design only.

### Track B: the Rosetta stone, December to February (dates indicative)
1. **Interlingua at scale.** Formal-core cards for all 25 fields at two levels, and MA at three-digit MSC level. Audit by sample.
2. **Correspondence discovery.** Propose edges wherever two fields share a formal core. Each stays `generated-unverified` until a person checks it.
3. **Evaluation at scale.** Independent held-out set, prospective set, coverage test, error log, blind usefulness study.
4. **Depth.** Bring the 15 thin pyramids and MA up to the depth of EN and ST.
5. **Professional packaging.** Pinned dependencies, `make reproduce`, versioned schemas, changelog, licence file, local MCP server.
6. **Review.** One reviewer per field for cards. Māori-led review for IK is unchanged and stays Chris's action.

## 6. What would count as success

- **Track A:** a pre-registered test of whether knowledge-based distance predicts failure diversity, with intervals and a null comparison.
- **Track B:** the engine proposes cross-field transfers that reviewers rate useful more often than a baseline model does.
- **Both:** every number traces to a logged run, and every miss is in the report.

## 7. Decisions for Chris

1. Would you like Track A to proceed as set out, or the handover's original order?
2. Is the formal-core design acceptable as an addition to the toolkit card schema?
3. Which local model should runs use? `qwen3.6:27b` is timed and fits in memory.
4. Controller or estimator for the demonstrator? An estimator has more distinct lineages; a controller has clearer safety bounds.
5. May MA sub-cells be registered as IDs?
6. Who could author or sign off the independent held-out set?
7. How would you like the licence question handled before anything is sent to DARPA?
