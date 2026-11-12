# Toolkit card coverage

Measured 13 November 2026 on branch `v4-content`. Built by `scripts/build_l1_cards.py` (argument `2` for level 2)
from the hand-written sources in `cards/toolkit/src_l1/` and `cards/toolkit/src_l2/`.

| Field | Primary map | L1 cards | L1 with tools | L1 tools | L2 cards | L2 with tools | L2 tools |
|---|---|---:|---:|---:|---:|---:|---:|
| AG | agrovoc.json | 36 | 4 | 4 | 1020 | 76 | 76 |
| AR | lcc.json | 18 | 9 | 13 | 37 | 11 | 17 |
| BI | anzsrc2020.json | 10 | 9 | 23 | 98 | 34 | 48 |
| BU | anzsrc2020.json | 10 | 7 | 13 | 91 | 24 | 43 |
| CH | anzsrc2020.json | 8 | 7 | 19 | 63 | 29 | 51 |
| CS | acm_ccs2012.json | 11 | 8 | 21 | 69 | 41 | 97 |
| DE | anzsrc2020.json | 5 | 4 | 9 | 51 | 16 | 23 |
| EA | gcmd.json | 24 | 14 | 31 | 226 | 78 | 102 |
| EC | jel.json | 20 | 16 | 40 | 139 | 57 | 121 |
| ED | eric.json | 686 | 24 | 25 | 1569 | 86 | 97 |
| EN | ieee.json | 46 | 39 | 88 | 682 | 201 | 276 |
| EV | gemet.json | 112 | 22 | 24 | 1092 | 79 | 81 |
| HI | lcc.json | 34 | 11 | 19 | 77 | 11 | 20 |
| IK | anzsrc2020.json | 20 | 0 | 0 | 320 | 0 | 0 |
| IS | anzsrc2020.json | 3 | 3 | 7 | 36 | 16 | 28 |
| LA | lcc.json | 7 | 2 | 5 | 39 | 9 | 14 |
| LN | lcc.json | 13 | 2 | 4 | 45 | 3 | 6 |
| MA | msc2020.json | 63 | 60 | 109 | 534 | 297 | 551 |
| MD | mesh2026.json | 9 | 9 | 18 | 113 | 14 | 23 |
| MS | anzsrc2020.json | 13 | 11 | 20 | 91 | 27 | 38 |
| PH | physh.json | 18 | 17 | 46 | 465 | 202 | 315 |
| PL | philpapers.json | 7 | 4 | 8 | 137 | 15 | 25 |
| PO | lcc.json | 13 | 6 | 10 | 14 | 6 | 12 |
| RE | lcc.json | 14 | 2 | 3 | 46 | 2 | 5 |
| ST | lcc.json | 17 | 9 | 13 | 24 | 9 | 14 |
| **All** | | **1217** | **299** | **572** | **7078** | **1343** | **2083** |

Mathematics level 1 is the existing `cards/toolkit/MA.json` (63 two-digit cards), unchanged.
Mathematics level 2 is the 534 three-digit MSC classes in `cards/toolkit/MA_L2.json`.
Every tool on every card lists at least one hypothesis: yes.

## What these cards are

- Every card is `status: draft`, `generated_by: claude-fable-5-2`. None is reviewed.
- They were drafted in session from general knowledge. **No source was checked and no audit sample has been drawn.**
  The handover's quality gate (random samples checked against a cited reference, with a Wilson interval) is still to do.
  Until it is done there is no measured error rate.
- `cross_uses` is empty on every card.

## Why most cards carry no tools

A card has no tools in one of two cases. Its note says which.

1. **The node is not a subfield with methods of its own.** This is most of the count.
   - ED (ERIC), EV (GEMET) and AG (AGROVOC) are flat thesaurus term lists at both levels. Terms such as "Animals", "Denmark" or
     "Grade 7" index documents. Only terms that name a method area carry tools.
   - HI, LN, AR, PO, LA and RE (Library of Congress classes) are mostly regional, language-family, jurisdiction or tradition headings.
   - EN (IEEE) level 2 mixes method areas with devices, materials and organisational topics.
   - In mathematics, history, education and collection classes carry no tools.
2. **No tool could be stated with confidence.** The handover says to leave these out and not to guess.
   This applies to many specialist classes in mathematics (237 of 534 carry no tools, 55 of them administrative, education or application classes),
   physics, biology and medicine. These are the places where a specialist would add most.

Indigenous knowledge (IK) carries no tools on any card at either level. Each card carries the note that placement and content
await Māori-led and Indigenous-led review. Religious-tradition headings (RE) carry no tools; authority there is W13.

## Map faults found, not fixed

- `maps/LA/lcc_k.json` and `maps/RE/lcc_b.json` list some level-2 node ids twice (LA 4, RE 3). One card was made per node id.
- `maps/EN/ieee.json` has 14 level-2 names that occur under two parents. Their card ids use the node id tail (`Parent|Name`).

## Open points

- The audit, as above.
- Licences of the source maps carry over to the cards (MSC2020 is CC BY-NC-SA). This is noted, not resolved.
- `scripts/draft_toolkit_cards.py` was not used and its five listed faults are not fixed.
- Handover tasks 0 (freeze experiment distances), 1 (register mathematics) and 4 (formal cores) are not started.
- `engine/v3/connect.py` loads every `cards/toolkit/<FIELD>*.json`, so the new files are now read by Connect.
  `tests/test_v3_connect.py` still passes. Rankings on real queries may have changed and were not compared.
