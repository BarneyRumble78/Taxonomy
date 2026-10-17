# Integration plan: one Minto pyramid per field

Status: draft, 11 October 2026. Branch `v3-content`. This is the ordered plan for turning the published maps into pyramids that Survey, Consult, Connect, Check and Zoom can run across all 25 fields at once. It follows `standard/STANDARD_V3.md` and the Minto method's Section 12 checklist. Counts below are from `python3 scripts/check_coverage.py` after the rebuild on this date. The maps hold 307,561 nodes. No key-line cell is empty.

Licences are recorded on each map. They do not block a placement.

## 0. What this round added

| Source | Where it landed | Nodes |
|---|---|---|
| ACM CCS 2012, labels repaired | CS 1,564, IS 324, EN 225 | 2,113, with English names |
| PhilPapers archive 30 June 2025 | PL 6,028, ED 1 | 6,029 unique categories, 91 more than the September 2024 snapshot |
| Getty AAT, one further level | DE 2,629, AR 885 | 3,514, up from 605 |
| AGROVOC full English hierarchy | AG | 42,008, up from the top concepts only |
| PACS 2010 regular edition | PH | 4,295. Cells: A4 2,049, A3 798, A1 691, A2 618, A5 139 |
| IUPAC Gold Book term index | CH | 15,307. The index has no broader links |
| ChEBI chemical entity, depth 2 | CH | 192 class nodes under CHEBI:24431 |
| NAICS 2022 | BU | 2,122 |
| ISIC Rev. 4 | BU | 766 |
| LCC 2024 full schedules, C, D, E-F, K, U-V, Z | HI 76,794, IS 22,867, ST 9,305, LA 3,984, EN 2,773 | numbered captions and headings |
| LCC subclass outlines KB, KD, KE, KF, KZ | folded into the LCC outline | religious law stays on RE; the others on LA |
| DTIC subject categories 15, 16, 17, 19 | ST | 39 |
| APSA organized sections | PO 42, PL 4, ST 1 | 47 |
| UNESCO History, Linguistics, Languages, Legal systems, Information | HI 51, LN 67 and 151, LA 75, IS 312 | from the thesaurus already on disk |
| UNESCO Politics and government, re-split | PO 90, ST 2 | defence, peace and intelligence stay on ST |
| UNESCO labels for Indigenous terms | IK | 3. Provisional |

ANZSRC six-digit moves in the same rebuild: 470406 to LN.O.A5, 470411 to LN.O.A4, 480401 and 480605 to LA.O.A3.

Still blocked, or downloaded and not mapped:

- NATOTerm, `https://nso.nato.int/natoterm/content/nato/pages/home.html`, HTTP 403.
- ECPR standing groups, `https://ecpr.eu/StandingGroups`, HTTP 403.
- EuroVoc. The dataset page returns HTTP 200. The HTML has no direct SKOS or RDF file. The download is a portal popup.
- LSA subfields. `https://www.linguisticsociety.org/what-linguistics` redirects to the LSA homepage. The subfield list is not in the response.
- ACLED. A guessed 2024 codebook URL returned HTTP 404. No stable public category file was found.
- SIPRI. No public category-list file was located.
- US SIC. OSHA publishes an HTML manual, not one file. NAICS and ISIC were taken instead.
- DTIC full term list. `sources/dtic_thesaurus.xlsx` (1.1 MB, August 2025) was saved. It is a general technical thesaurus, so only the military subject categories were mapped.
- IUPAC Gold Book live site, HTTP 403. The term index was taken from the Internet Archive snapshot of 15 March 2024.
- PhilPapers live site, HTTP 403. The tree was taken from the Internet Archive.

The cells that are still thin, and that the conversion below has to rebalance, are: CH.O.A1 holds 26,608 of 29,907 chemistry nodes; HI.O.A4 holds 71,967 of 78,475 history nodes; LA.O.A1 holds 4,732 of 4,811 law nodes; IS.O.A1 holds 20,962 of 25,427 information nodes; LN.O.A5 holds 5,422 of 5,515 language nodes, while Signal and Meaning hold 4 each; ST.O.A5 holds 43; PO.O.A3 holds 6; DE.O.A3 holds 2; BU.O.A1 holds 10; BI.O.A5 holds 10.

## 1. Target data model

One file, `pyramids/<FIELD>.json`, per field. The map files stay as the source record. A pyramid does not replace them.

The object has six parts.

1. **Introduction.** Situation, complication, question, and question type, as in the method's output schema. The question for a field is the question already on its lens card.
2. **Governing thought.** One declarative sentence that answers that question. It is a summary of the key line, not a topic label.
3. **Key line.** The two to five cells already registered for the field (`cards/lens/<FIELD>.json`). Each point is a full sentence. The group records `logic_type` (inductive or deductive; induction is preferred at the key line, Minto Chapter 5) and one order from Minto Chapter 6: time, structure, or degree. An inductive group also records the plural noun and the single MECE dimension (Chapter 7).
4. **Groups below the key line.** Each source node that survives deduplication becomes a point under the cell it was placed in, then under a group of like kind. A group is inductive or deductive, never both. It has two to five members. It has no member named Other.
5. **Provenance.** Every pyramid point lists the source nodes it came from: scheme, id, code, and the map file. A point with no source is not written.
6. **Stable ids.** A pyramid point id has the form `<FIELD>.P.<path>`, for example `EV.P.2.3`. R12 applies. An id is never renumbered and never reused. A retired point keeps its id, is marked RETIRED, and points at the new home.

Vertical relation: each parent stores the question it raises (`why`, `how`, `so_what`, or `which_ones`). The children are the answer to that question and to no other.

Horizontal relation: a group stores one logic type. An inductive group stores one plural noun that fits every member. A deductive group is three steps, and the third follows from the first two.

Mathematics is the reference and is not rebuilt by this pipeline. Its five cells and its MSC placement stay as they are.

IK points stay marked provisional until the Māori-led review in `docs/MAORI_REVIEW_PACK.md`.

## 2. Conversion pipeline

Run the steps in this order. Each step writes a report under `runs/pyramid/` (git-ignored) before the next step starts.

### 2.1 Dedupe and merge

Within one field, two nodes merge when their normalised names match, or when a recorded crosswalk says they are the same concept. The survivor keeps every source id. The display name is the name from the field's primary scheme in `maps/index.json`. Children are re-parented onto the survivor. A node is not merged across fields. A concept that genuinely belongs in two fields stays as two points, each with its own provenance, until a bridge (section 3) is written.

### 2.2 Crosswalks

Crosswalks are explicit tables, not guesses. The first tables are the ones already encoded in the builders: ANZSRC six-digit overrides, MeSH tree prefixes, PACS sections, and the LCC span overrides. Further tables are added only from a published concordance (NAICS to ISIC is one candidate) and are stored at `crosswalks/<left>__<right>.json` with the source URL and the date.

### 2.3 Rebalance

A cell that holds more than half the field's nodes, or fewer than five, is split or fed before the pyramid is accepted. The split uses one dimension already named on the lens card. It does not invent a sixth key-line cell. The known cases are the thin and heavy cells in section 0. History's geographic captions (HI.O.A4) are grouped by the LCC subclass (CB, D, E, F, and so on) so the cell is a pyramid of regions and periods, not a flat list of 72,000 captions. Law's K schedule (LA.O.A1) is grouped the same way, by subclass. Chemistry's Gold Book titles stay on CH.O.A1 until a later pass can group them, because the downloaded index has no hierarchy.

### 2.4 Placement cascade

A node whose cell is already set by an authority rule is not moved by a model. The cascade applies only to nodes that the rules did not place, and to nodes flagged for rebalance.

1. **Rules.** Keyword and prefix tables of the kind already in `scripts/build_maps_more.py` and `scripts/build_maps_deep.py`. A rule names the cell and the pattern.
2. **Embeddings.** The same local embedding path the engine can already call. Each cell has a short exemplar text taken from its lens card. A node goes to the nearest cell only when the margin over the second nearest is above a threshold recorded in the run. Otherwise it is left for the next step.
3. **Local model.** Qwen3 30B (`qwen3:30b-a3b`) through Ollama, as `engine/v3/llm.py` already defaults. The prompt includes the cell questions and forbids a new cell. If that model fails, the fallback is `gemma3:12b`, which the same module already uses. The paid Anthropic path is not part of this pipeline.
4. **Human review.** A queue of the nodes the model marked uncertain, plus a sample of the ones it placed. Nothing in the queue is treated as settled until a person accepts it.

### 2.5 Validation tests

Add `tests/test_pyramid.py`. It reads each `pyramids/<FIELD>.json` and applies the checks from Section 12 of the method that a program can decide.

Automated, and failing the test:

- The governing thought is one sentence and is present.
- The key line has two to five points.
- No point is named Other.
- Each group has one logic type, not a mixture.
- An inductive group has a plural noun. A deductive group has three steps.
- Each group names one order from Minto Chapter 6: time, structure, or degree.
- Each parent names the question the children answer.
- Every point id matches `<FIELD>.P.` and no id repeats.
- A RETIRED id is not reused.
- Every point has at least one source node, and that node exists in a map file.
- Key-line point ids match the registered lens cells.

Left to a person, and stored as a signed line in the pyramid file rather than asserted by the test:

- The situation is something the reader would accept without proof.
- The governing thought answers the question and could be disagreed with.
- The children answer the question the parent raises, and not another one.
- The members of a group do not overlap, and nothing the question requires is missing.
- An action group is summarised by its effect, and a situation group by the inference.

`scripts/check.py` stays the check for the v2 pyramids. The new test does not weaken it.

## 3. Bridges

A bridge is a record in `bridges/<FIELD>.json`: source point, target point, relation, and a source node or a sentence that warrants the link. The relations to start with are the ones Zoom needs: `example_of`, `examples`, `part_of`, `parts`, plus `uses` for the cross-field citation the v2 rules already allow ("uses XX.O.An").

A bridge is not a second home. Check mode still has one owner. Survey, Consult and Connect may follow a bridge and must say they did.

The first bridges are mechanical. A map node that was re-rooted with `moved_from` becomes a `uses` bridge back to the field it left. Later bridges come from the toolkit cards' famous cross-uses, then from human review. A query that applies all 25 fields reads the 25 pyramids and then the bridges, and does not depend on a node having been copied into every field.

## 4. How each mode uses the pyramids

The modes are specified in `standard/STANDARD_V3.md`. The CLI is `taxonomy.py`. Zoom is specified and is not a CLI mode yet.

- **Survey** (`engine/v3/core.py` `survey`). Read the governing thought and the key line of every field, or of the fields named with `--fields`. Return what each field sees, which cells had no relevant child, and one Minto synthesis across those key lines. A blind spot is a key-line point whose children were all set aside.
- **Consult** (`consult`). Stay inside one field. Walk every group under the key line. R13: each group is applied or set aside with a reason. Rank the routes by the promise, cost and certainty the toolkit card already stores. R14: a proposed tool lists its hypotheses and whether the problem meets them.
- **Connect** (`connect_run`, and `engine/v3/connect.py`). Build the problem signature as now. Search toolkit cards in every field, not only the field named, once those cards point at pyramid points. Keep the conditions check.
- **Check** (`check`). Unchanged. One claim, one owner field, the warrant that cell requires. The pyramid is not a second classifier.
- **Zoom.** From any point, follow `example_of` / `examples` and `part_of` / `parts`. The answer is the neighbouring points, with their sources. This is the mode to add after the first bridges exist.

Every run keeps the R16 record already written to `runs/`.

## 5. Order of the fields

MA is not in this queue. It is the reference. EV is the pilot, because GEMET is one scheme, 5,573 nodes, and all five cells already hold nodes.

Effort here means how much of the pipeline in section 2 the field needs. It is not a calendar estimate.

| Order | Field | Nodes now | Why this place |
|---|---|---|---|
| 1 | EV | 5,651 | Pilot. One main scheme. Practise dedupe, grouping and the Section 12 tests on a field that is not lopsided. |
| 2 | EC | 1,231 | JEL is the authority and is already hierarchical. |
| 3 | CS | 2,558 | ACM labels are now real names. IEEE is the second scheme. |
| 4 | PO | 353 | Small. APSA and UNESCO are in. Political behaviour (6 nodes) needs a group, not more downloads, unless ECPR becomes available. |
| 5 | RE | 1,015 | LCC outline only. Confirm the KB outline belongs here and stop. |
| 6 | DE | 2,758 | AAT is the mass. Activities and conditions (2 and 15 nodes) need groups inside the key line, not new cells. |
| 7 | ED | 5,052 | ERIC is the mass and is already one thesaurus. |
| 8 | PH | 8,586 | PhySH stays primary. PACS is the balancing scheme and already spreads across the five cells. |
| 9 | MS | 3,089 | PsycInfo plus MeSH. One small cell (25 nodes) to group. |
| 10 | BU | 3,593 | NAICS and ISIC are in. Accounts holds 10 nodes and needs a group under the key line. |
| 11 | AR | 1,944 | AAT physical and critical concepts plus LCC. |
| 12 | PL | 6,126 | PhilPapers is the mass. The June 2025 snapshot is the one to dedupe. |
| 13 | EA | 4,788 | GCMD is the authority. |
| 14 | ST | 9,542 | LCC U-V full schedule is the mass. Information holds 43 nodes. DTIC is the extra source. NATO, SIPRI and ACLED remain blocked. |
| 15 | EN | 11,297 | IEEE is primary. The LCC T schedule is the second mass. |
| 16 | AG | 42,524 | AGROVOC is now the full hierarchy. Group under the 25 top concepts before any model sees a leaf. |
| 17 | MD | 24,004 | MeSH is the authority. Do not re-cut the tree numbers by hand. |
| 18 | BI | 22,294 | MeSH again. The thin cell (10 nodes) is a grouping task. |
| 19 | CH | 29,907 | Heaviest rebalance. MeSH chemicals and the Gold Book both sit on composition. Group the Gold Book only after a hierarchy exists, or accept a flat list under named facets and say so. |
| 20 | LA | 4,811 | The full K schedule sits on Sources. Group by subclass first. EuroVoc is still blocked. |
| 21 | IS | 25,427 | The full Z schedule sits on Items. Group by subclass. UNESCO information is the second scheme. |
| 22 | HI | 78,475 | Largest file. Group the full C, D and E-F schedules by subclass before any other step. UNESCO history is the small causation set. |
| 23 | LN | 5,515 | Glottolog fills Diversity. Signal and Meaning still have 4 nodes each. Do not pretend the UNESCO linguistics microthesaurus fixes that. Wait for a real phonetics and semantics vocabulary, or group what is there and mark the gap. |
| 24 | IK | 343 | Last. ANZSRC 45 is the mass. The three UNESCO terms stay provisional. No further IK source is added without the Māori-led review. |

A field is finished when `tests/test_pyramid.py` passes for it and the human lines in section 2.5 are signed. EV is finished before the second field starts, so the test suite is real before the large fields are touched.

## 6. Storage, indexes, and surfaces

Store of record, in git:

- `maps/<FIELD>/<scheme>.json`, as now. One node carries `id`, `code`, `name`, `level`, `parent`, `taxonomy_cell`.
- `pyramids/<FIELD>.json`, the model in section 1.
- `bridges/<FIELD>.json`, the links in section 3.
- `crosswalks/*.json`, the concordances in section 2.2.
- `maps/index.json`, the scheme counts and the primary scheme.

Built locally, git-ignored, regenerated by a script:

- A SQLite file with FTS5 over node names, pyramid statements, and bridge endpoints. This is the search index. It is not a second source of truth.
- An embedding table in the same SQLite file, one vector per pyramid point and per toolkit card, using the local embedder. Vectors are rebuilt, not edited.

CLI, added beside the modes that already exist:

- `python3 taxonomy.py survey|consult|connect|check`, unchanged in contract.
- `python3 taxonomy.py zoom "<point or phrase>"`, once bridges exist.
- `python3 scripts/build_pyramids.py --field EV`, the pipeline in section 2 for one field.
- `python3 scripts/build_index.py`, the SQLite file.

No new HTTP service in this plan. The site already describes an API. It should read the same JSON the CLI reads, when that work is done. Until then the CLI is the surface.

## 7. Quality gates

A field's pyramid is not merged until all of these are true.

1. `scripts/check.py`, `scripts/check_coverage.py`, `scripts/validate_cards.py` and `python3 -m pytest -q tests` pass.
2. `tests/test_pyramid.py` passes for that field.
3. The human lines in section 2.5 are present and named.
4. Every point traces to a source node. A point with no source is a defect.
5. No id from a previous revision of that pyramid has been reused.
6. IK, if touched, is still marked provisional.
7. The run record names the rules, the embedding threshold, the model, and the person who signed the review.

The pilot report for EV is the template for the other 23 fields.
