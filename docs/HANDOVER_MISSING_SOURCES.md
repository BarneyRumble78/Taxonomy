# Handover: retrieve the missing taxonomy sources

Repo: github.com/BarneyRumble78/Taxonomy, branch `v3-content`. Read `CLAUDE.md` first.

## Task
Download the published taxonomies listed below, save each raw file in `sources/`, and add a parser to
`scripts/build_maps_more.py` that writes `maps/<FIELD>/<scheme>.json` in the existing node format:
`{"id", "code", "name", "level", "parent", "taxonomy_cell"}`. Every node goes under a cell of its owning field.
The cell list for each field is in `cards/lens/<FIELD>.json`.

Do only this. Do not buy anything, sign up for anything, or add features. Use free public downloads only.
If a source cannot be fetched, record it under "Still blocked" with the URL and the HTTP status, and move on.

## Missing sources

| # | Field | Source | Where to try | Blocked last time |
|---|---|---|---|---|
| 1 | PL | PhilPapers category tree (about 5,000 categories) | philpapers.org/categories.pl, philpapers.org/browse/all | 403 to curl; try a browser or the PhilPapers API |
| 2 | MS | APA PsycInfo classification codes (22 / 135) | apa.org/pubs/databases/training/class-codes | Returned a 212-byte page; copy the table from the HTML in a browser |
| 3 | HI | LCC classes E and F (history of the Americas) | loc.gov/aba/publications/FreeLCC/freelcc.html | lcco_e.pdf and lcco_f.pdf returned 404; find the current file names on that page |
| 4 | ST | Strategy and security studies: no ANZSRC home | LCC U and V are already in; add ANZSRC 440804 (Defence studies) and 440810 (Peace studies) fields, and the UNESCO Thesaurus "Politics and government" microthesaurus (vocabularies.unesco.org) | Not tried |
| 5 | EV | UNESCO Thesaurus environment terms, or GEMET | vocabularies.unesco.org (SKOS download); eionet.europa.eu/gemet (RDF download) | Not tried |
| 6 | DE | Getty AAT "Styles and periods", "Activities" and "Objects > Furnishings and equipment" facets (top levels only) | vocab.getty.edu (SPARQL or the full dump) | Not tried |
| 7 | AR | Getty AAT top facets, for the empty AR.O.A5 "Value" and AR.O.A2 "Form" | as above | Not tried |
| 8 | IS | ISKO Encyclopedia of Knowledge Organization category list | isko.org/cyclo | Not tried |
| 9 | LN | Glottolog language families (for LN.O.A5) and the Linguistics subfield list of the LSA or ANZSRC 4704 fields | glottolog.org (CLDF download on GitHub: glottolog/glottolog-cldf) | Not tried |
| 10 | ED | ERIC Thesaurus | eric.ed.gov/?ti=all (descriptor list; bulk download page) | Not tried |
| 11 | AG | AGROVOC top concepts | agrovoc.fao.org (core .nt.zip) | Not tried |
| 12 | CH | ChEBI role ontology (roles only, not the molecules) | ftp.ebi.ac.uk/pub/databases/chebi/ontology (chebi.obo, filter to the role branch CHEBI:50906) | Not tried |
| 13 | EN | No single engineering taxonomy; LCC T is in. Add IEEE Thesaurus top terms if a free PDF is published | ieee.org (IEEE Taxonomy PDF) | Not tried |

## Cells with nothing in them (look for sources that fill these)
CH.O.A4 Rates and mechanisms · HI.O.A3 Cause · LN.O.A1 Signal · LN.O.A3 Meaning · AR.O.A5 Value ·
ED.O.A4 Assessment · EV.O.A3 Impacts · EV.O.A5 Limits · ST.O.A5 Information.
Some can be filled by re-placing nodes that are already in the maps (e.g. MeSH "Chemical Phenomena" into CH.O.A4;
ERIC assessment terms into ED.O.A4). Note any re-placement in the placement table, not by editing map files by hand.

## Known limits of what is already there (do not try to fix in this task)
- Placement is coarse: nodes inherit the cell of their top-level heading. PH (3,747 of 4,291 in A1) and CH
  (12,200 of 12,759 in A1) are lopsided. Fine placement is the Minto conversion step, done separately.
- Mathematics has no section-12 registry; the coverage check allows its MA.B.C1–C5 cells by name.

## Done means
1. Each new source is in `sources/` and has a map in `maps/<FIELD>/`, with `scheme`, `source` URL, `retrieved` date and `licence` text as published.
2. `maps/index.json` lists it (rerun `python3 scripts/build_maps.py && python3 scripts/build_maps_more.py`).
3. These all pass: `python3 scripts/check_coverage.py`, `python3 scripts/check.py`, `python3 scripts/validate_cards.py`, `python3 -m pytest -q tests`.
4. A short list at the end of this file: what was added (node counts), what is still blocked and why.
5. Commit on `v3-content` and push. Do not merge to main.
