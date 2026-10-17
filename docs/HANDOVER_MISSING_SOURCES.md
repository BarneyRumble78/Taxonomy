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

## Added (2026-10-11)

Licences are recorded as published. Nothing was blocked on a licence. Maps were not converted into Minto pyramids.

| Source | Nodes | Where |
|---|---:|---|
| PhilPapers categories | 5,938 | PL 5,937, ED 1 (Teaching Philosophy) |
| APA PsycInfo classification | 157 | MS 144, ED 9, CS 3, LN 1 |
| LCC classes E and F | 310 | HI, folded into `lcc.json` |
| UNESCO Thesaurus, Politics and government (mt6.15) | 92 | ST |
| GEMET 4.2.3 | 5,573 | EV |
| Getty AAT, top levels | 605 | DE 408, AR 197 |
| ISKO Encyclopedia of Knowledge Organization | 132 | IS |
| Glottolog families | 4,853 | LN, all on LN.O.A5 |
| ERIC Thesaurus (main terms) | 4,520 | ED |
| AGROVOC top concepts | 1,036 | AG |
| ChEBI role ontology | 1,649 | CH (1,205 on A4, 444 on A5) |
| IEEE Taxonomy, January 2026 | 8,037 | EN 6,849, CS 884, EA 233, ED 71 |

ANZSRC 440804 Defence studies and 440810 Peace studies were already in `maps/ST/anzsrc2020.json` (ST.O.A3 and ST.O.A4). They were not copied again.

Re-placements, in the placement tables:

- MeSH rate prefixes under G02 (kinetics, catalysis, hydrolysis, organic chemistry phenomena, oxidation-reduction, photochemical processes, polymerization, pyrolysis): 45 nodes moved from CH.O.A3 to CH.O.A4. The rest of G02 stays on CH.O.A3.
- ChEBI biological role and chemical role are CH.O.A4. Application is CH.O.A5.
- LCC CC 72–81 and the heading Historiography (E175–175.7) are HI.O.A3. The outline has no narrower lines under those spans, so the cell holds 3 nodes.
- LCC UB 250–277, UG 570–582 and UG 760–765 are ST.O.A5 (5 nodes).
- ANZSRC 470410 Phonetics is LN.O.A1. 470405 Discourse and pragmatics and 470408 Lexicography and semantics are LN.O.A3. 390402 Education assessment and evaluation is ED.O.A4.
- APA 2227 is ED.O.A4. APA 2720 is LN.O.A1. The 3500 block is ED. APA 4120, 4140 and 4160 are CS.O.A4.
- ERIC groups 820 and 830 are ED.O.A4.
- GEMET tops for impact, hazard, health and effect are EV.O.A3. Resource, risk and safety are EV.O.A5.
- AAT Physical Attributes is AR.O.A2. The critical-concepts branch is AR.O.A5.

Cells that were empty and now hold nodes: CH.O.A4, HI.O.A3, LN.O.A1, LN.O.A3, AR.O.A5, ED.O.A4, EV.O.A3, EV.O.A5, ST.O.A5. `check_coverage.py` reports no empty key-line cell. Total map nodes: 123,790.

Files kept out of git, with the extract that was committed:

- `agrovoc_core.nt.zip`, 74,107,876 bytes, from https://agrovoc.fao.org/latestAgrovoc/agrovoc_core.nt.zip. Committed file: `sources/agrovoc_top.nt`.
- `chebi.obo.gz` (ChEBI data-version 256) from https://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.obo.gz. Committed file: `sources/chebi_roles.obo`.
- Glottolog `values.csv` (about 21 MB). Committed file: `sources/glottolog_classification.tsv`, joined to `sources/glottolog_languages.csv`.

Checks on this tree: `check_coverage.py` passed, `check.py` passed, `validate_cards.py` printed `valid`, `pytest` 87 passed.

## Still blocked

None of the thirteen sources is still blocked. These alternates were used:

- https://philpapers.org/browse/all and https://philpapers.org/categories.pl return HTTP 403 to curl. The API wants a free key, which was not requested. The tree is the Internet Archive snapshot https://web.archive.org/web/20240924181241/https://philpapers.org/browse/all (24 September 2024): 5,938 categories after dropping repeated entries. A later live page has claimed 6,164.
- https://www.apa.org/pubs/databases/training/class-codes returns HTTP 200 as a 212-byte Incapsula page. The December 2022 printer-friendly PDF of the same chart was saved (157 codes).
- ieee.org taxonomy URLs return HTTP 202. The January 2026 Widen share https://ieee-org.widen.net/s/dr9nl9n8kw/ieee-taxonomy_jan_2026_pdf returns HTTP 404. The PDF is the file served by https://ieee-org.widen.net/content/umbnbirtxs/original/ieee-taxonomy.pdf (version 1.05, created 14 January 2026).
- The LSA subfield list was not fetched. ANZSRC 4704, with the three field overrides above, is the linguistics list the handover allowed instead.
