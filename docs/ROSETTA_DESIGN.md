# The Rosetta layer: design for a ten-year horizon

Prepared 10 November 2026 on branch `v4-generative`. Status: design proposal, with a working first slice.
Sections 2 and 7 are speculation and are labelled as such. Nothing here is an evaluated result.

## 1. Governing thought

A future reasoning system will already hold the facts. It will lack a checked map of which ideas are the same idea.
Taxonomy can be that map: one mathematical structure, many field dialects, and the exact conditions under which each translation holds.
New ideas come from two places on the map: the empty cells, and the points where a translation breaks.

## 2. The view from 2036 (speculation)

Suppose a capable system in 2036 could call this tool. What would it want from it?

It would not want stored knowledge. It would have read more than the pyramids contain.
It would not want a smaller model inside the tool, guessing on its behalf.

It would want five things it cannot produce reliably alone:
1. **Compression.** Thousands of tools across 25 fields reduce to a much smaller set of structures. Reasoning over the structures is cheaper.
2. **Addresses.** A stable ID for every structure, binding and edge, so a claim can cite exactly what it relies on.
3. **Conditions.** For each translation, which assumptions hold on both sides and which do not.
4. **Gaps.** A list of where a structure has never been applied, held as questions.
5. **An audit trail.** Who checked each entry, against what source, and to what standard.

That leads to one design decision. **The tool contains no model.** It is data plus deterministic operations.
The caller supplies the intelligence; the tool supplies memory, structure and honesty about status.
The local-model steps in the v3 engine remain useful today as drafting aids. They are not the durable part.

## 3. The unit of knowledge: the formal core

The original Rosetta stone carried one decree in three scripts. A formal core carries one structure in many fields.

| Part | Content | Example: diffusion |
|---|---|---|
| Structure | One sentence, free of any field's words | A conserved density spreads with flux proportional to its gradient |
| Mathematics node | The MA node that owns it | `MSC:35Kxx` |
| Roles | Named slots | density, diffusivity, flux law, boundary |
| Assumptions | Separate checkable statements (R5) | steps are independent and of finite variance |
| Guarantee | What follows when all assumptions hold | smoothing, a maximum principle, square-root spreading |
| Bindings | Per field: what fills each role, which assumptions are met, where it breaks | physics, engineering, finance, genetics, machine learning, psychology |

Mathematics stays the apex and owner of every structure. Each field owns only its binding.
A binding with no stated limit is rejected by the validator. The differences are the product.

## 4. Operations

| Operation | What it does | State |
|---|---|---|
| `find` | Locate cores and bindings by words | Built |
| `translate` | Map one field's tool onto another's, role by role, with assumption differences | Built |
| `holes` | List fields where a core has no binding, as questions | Built |
| `distance` | Lineage distance through tree, cores and edges; assumption distance between bindings | Built |
| Derived edges | Write a correspondence edge for every pair of cells sharing a core | Built: 102 edges |
| `transfer` | Carry a technique into a field that lacks it, and list what must be shown | Next |
| `relax` | Drop one assumption and find the structure that survives | Next |
| `collide` | Take two cores bound in one cell and ask what their combination implies | Later |
| `compose` | Record that one core specialises or combines others | Later |

`translate` withholds the guarantee unless every assumption holds on both sides.
The physics-to-finance diffusion translation, for example, reports that independent finite-variance steps fail in finance.

## 5. What is built today

- `rosetta/cores.json`: 12 formal cores with 56 bindings across 13 fields. All are `draft`.
- `engine/v3/rosetta.py`: the operations above, with no model calls.
- `correspondences/rosetta_edges.json`: 102 derived edges, each `generated-unverified`.
- `python3 taxonomy.py rosetta translate RC-diffusion PH EC`, and `find`, `holes`, `matrix`, `distance`.
- Lineage distance between an epidemic threshold and reactor criticality falls from 6 to 2 once the shared core is recorded.
- Validation in `scripts/check.py`, and 28 tests.

**Provenance of the seed.** I wrote the 12 cores from general knowledge in one session. No source was checked.
They are textbook-level, but every entry is unverified until a person reviews it against a cited source.
I did not read the benchmark answer files. Overlap with the existing 50-problem set is still likely, because good cores are famous.
That set therefore cannot count as evidence for this layer.

## 6. How it scales

1. **Candidates from the mathematics map.** Each three-digit MSC class is a source of candidate cores.
2. **Bindings proposed by models.** For each core, a model proposes bindings in each field. Each enters as `draft`.
3. **A verification ladder.** draft, then sourced, then reviewed by a field specialist, then formalised.
4. **Formalisation.** At the top rung the core is a statement in a proof assistant, and each binding an instance of it.
5. **Three scripts, not one.** The pyramids have faces for Objects, Methods and Warrants. This seed covers Objects only.
   Method cores (for example, triangulating independent records) and warrant cores would bring in fields that mathematics describes poorly.
6. **Versioning.** IDs never change (R12). Retired cores point to their successors.

## 7. Where discoveries might come from (speculation)

- **Holes.** A structure proven useful in six fields and absent from a seventh is a reasonable place to look.
- **Broken assumptions.** Where a field violates an assumption, either a known generalisation applies or new mathematics is needed.
- **Unexpected proximity.** Two cells that are far apart in the tree and close through a core share more than their fields acknowledge.
- **Collisions.** A cell that binds two cores invites the question of what holds when both apply.

None of these is a discovery. Each is a lead that a person, or a later system, must test.

## 8. Limits

- **Analogy is not truth.** A shared structure licenses a question, not a conclusion.
- **An empty cell is ambiguous.** The transfer may be untried, tried and failed, or simply unrecorded here.
- **The mathematical view favours formal fields.** History, law and the arts are thinly served until method and warrant cores exist.
- **W13 does not transfer.** Tradition-internal authority is never mapped onto another field.
- **Indigenous knowledge stays provisional.** The validator rejects any IK binding not marked speculative, pending Māori-led review.
- **One author.** The seed reflects one model's knowledge and its blind spots.
- **No evidence of usefulness yet.** That is the job of the evaluation in `docs/PLAN_V4.md`.

## 9. Next steps

1. Review of the 12 seed cores by Chris, with sources added.
2. The `transfer` and `relax` operations.
3. Cores for the FLASH slice, so that assumption distance can be tested as a heterogeneity metric.
4. A local MCP server exposing the operations, once evaluation exists.
