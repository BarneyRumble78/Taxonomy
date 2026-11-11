# Toolkit card coverage, level 1

Measured 12 November 2026 on branch `v4-content`. Built by `scripts/build_l1_cards.py` from `cards/toolkit/src_l1/`.

| Field | Primary map | Cards | With tools | Share | Tools | Every tool has hypotheses |
|---|---|---:|---:|---:|---:|---|
| AG | agrovoc.json | 36 | 4 | 11% | 4 | yes |
| AR | lcc.json | 18 | 9 | 50% | 13 | yes |
| BI | anzsrc2020.json | 10 | 9 | 90% | 23 | yes |
| BU | anzsrc2020.json | 10 | 7 | 70% | 13 | yes |
| CH | anzsrc2020.json | 8 | 7 | 88% | 19 | yes |
| CS | acm_ccs2012.json | 11 | 8 | 73% | 21 | yes |
| DE | anzsrc2020.json | 5 | 4 | 80% | 9 | yes |
| EA | gcmd.json | 24 | 14 | 58% | 31 | yes |
| EC | jel.json | 20 | 16 | 80% | 40 | yes |
| ED | eric.json | 686 | 24 | 3% | 25 | yes |
| EN | ieee.json | 46 | 39 | 85% | 88 | yes |
| EV | gemet.json | 112 | 22 | 20% | 24 | yes |
| HI | lcc.json | 34 | 11 | 32% | 19 | yes |
| IK | anzsrc2020.json | 20 | 0 | 0% | 0 | yes |
| IS | anzsrc2020.json | 3 | 3 | 100% | 7 | yes |
| LA | lcc.json | 7 | 2 | 29% | 5 | yes |
| LN | lcc.json | 13 | 2 | 15% | 4 | yes |
| MA | msc2020 (two-digit), existing | 63 | 60 | 95% | 109 | yes |
| MD | mesh2026.json | 9 | 9 | 100% | 18 | yes |
| MS | anzsrc2020.json | 13 | 11 | 85% | 20 | yes |
| PH | physh.json | 18 | 17 | 94% | 46 | yes |
| PL | philpapers.json | 7 | 4 | 57% | 8 | yes |
| PO | lcc.json | 13 | 6 | 46% | 10 | yes |
| RE | lcc.json | 14 | 2 | 14% | 3 | yes |
| ST | lcc.json | 17 | 9 | 53% | 13 | yes |
| **All** | | **1217** | **299** | **25%** | **572** | |

## What these cards are

- Every card is `status: draft`, `generated_by: claude-fable-5-2`. None is reviewed.
- They were drafted in session from general knowledge. **No source was checked and no audit sample has been drawn.**
  The quality gate in the handover (10 cards per field against a cited reference, Wilson interval) is still to do.
- `cross_uses` is empty on every card.

## Why many cards carry no tools

A card has no tools when its node is not a subfield with methods of its own. The card's note says which case applies.

- **ED (ERIC)** and **EV (GEMET)**: level 1 is a flat list of thesaurus terms such as "Animals" or "border". Only terms that name a method area carry tools.
- **AG (AGROVOC)**: level 1 is the thesaurus's top facets plus a few stray concepts.
- **HI, LN, AR, PO, LA, RE (LCC)**: most level-1 classes are regional, language-family or jurisdiction headings. Methods sit at the general class.
- **RE**: tradition headings carry no tools. Authority inside a tradition is W13 and is not mapped to other fields.
- **IK**: no card carries tools. Each carries the note that placement and content await Māori-led and Indigenous-led review.
- **ST**: branch-of-service headings carry no tools.

## Open points

- Level 2 has not been drafted.
- Licence of the source maps carries over to the cards. This is noted, not resolved.
- `scripts/draft_toolkit_cards.py` was not used and its five listed faults are not yet fixed.
