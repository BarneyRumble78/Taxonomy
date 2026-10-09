# Backlog

## Standard and pyramids
- [ ] EN: add a home for stated requirements and design lives (pilot claim 41 found no cell). Decide: a requirements partition, or file specifications under EN.M.B5 with W12.
- [ ] Cite the remaining UNVERIFIED dates (see the ledger in docs/COMBINED_v2.2.md, Part 4).
- [ ] CH: map ACS's 32 technical divisions one by one. PH: transcribe PhySH's 17 disciplines and map them.
- [ ] HI, LA: subclass-level LCC maps (D–F, K).
- [ ] Deepen thin pyramids (CH, MD, CS, EC, BU, PO, LA, HI, LN, ED, DE, AG, EV, IS, IK) toward the depth of BI/EN/ST (5,000+ words, second key lines, named objects with hypotheses).
- [ ] Review semantic meaning of script-remapped cross-references in BI, EA, EN, MS, PL, ST, AR.
- [ ] Sharpen DE A2/A3 and EV A2/A3 cell definitions (pilot disagreements).

## Validation
- [ ] Human placement study: 3 human coders, 50 claims sampled from published literature, Krippendorff's alpha per face (pilot/PROTOCOL.md).
- [ ] Convene the Māori-led review (docs/MAORI_REVIEW_PACK.md). Owner action, not Claude's.

## Engine and API
- [ ] Build a held-out test set; the current pilot set was in view when the lexicon was written, so its scores are a regression floor only.
- [ ] Grow the lexicon from the pyramid texts automatically (named objects, key-line terms).
- [ ] Add a model-assisted classifier behind the same interface.
- [x] /classify, /lookup/{id}, /audit, /map, /relate built as a Cloudflare Worker (`docs/DEPLOY.md`). Still open: deploy it and add a rate-limit rule.
- [x] SKOS (JSON-LD) and JSON export of the registry (`public/v1`). Still open: DOI, licence, version tag.

## Website
- [ ] Working registration (needs a backend or form service outside the artifact sandbox).
- [ ] Real endorsements; downloadable policy and academic sample briefs.
- [ ] Own domain.

## Truth-seeking and map uses (from the owner's brief)
- [ ] `map` finds few fields for design briefs (a test sunglasses brief matched 3 of 25). Grow the lexicon from pyramid text, then re-test on a held-out set of briefs.
- [ ] Tools and theories per field: add a register of named objects (theorems, laws, methods, standards) to each pyramid's registry rows so `map` can list them, not only cells.
- [ ] Rosetta view: a `translate` call that restates one concept in each adjacent field's terms, using the `uses` edges and bridges. Needs ID-level `uses` (most are field-level now).
- [ ] Status face (current, contested, retracted, superseded), and Toulmin qualifier and rebuttal on claims.
- [ ] Primary and secondary owner for claims with two legitimate warrants.
- [ ] Engine faults seen in use: a "proves" claim about a tax cut went to Mathematics (the `proof` tie-break); a proof of a field result got method M3, not M2; "every finite integral domain is a field" went to analysis, not algebra. Fix them and add them as tests.
- [ ] Reconcile the registry count. The uploaded Phase 2 file says 888 IDs; the repo builds 984.
