This report is not a human agreement study and is not Krippendorff's alpha.

The gold in `pilot/heldout.tsv` is a test label written for this pass, not a ruling. `pilot/PROTOCOL.md` is unfilled. No alpha was computed. `pilot/claims.tsv` was not scored. The file was frozen before lexicon growth. SHA256 `e6826cf6f46b69371f17c95c1aab9c771885bbbecc233e28f95b6f3577a4b856`. 203 claims, 25 fields, at least six per field, 53 notes marked border.

Scores are exact matches of the rule engine to that gold. Confidence is not scored. It remains a ratio of cue-word scores.

## Overall

| Face | Before growth | After growth |
|---|---|---|
| Owner | 125/203 (0.6158) | 126/203 (0.6207) |
| Cell | 95/203 (0.4680) | 97/203 (0.4778) |
| Warrant | 77/203 (0.3793) | 77/203 (0.3793) |
| Method | 86/203 (0.4236) | 86/203 (0.4236) |

Growth changed two rows. H040 (Ohm's law) moved from AR to EN, which matches the gold owner and cell. Its warrant and method stayed wrong (gold W11/M7, engine W6/M6). H101 (Grimm's law) stayed LN and moved from LN.O.A1 to the gold cell LN.O.A5. Warrant and method stayed wrong.

## Per field, after growth

Owner before growth is shown because that was the revert test. Cell, warrant and method are the final counts. Only EN's owner count moved (4/8 to 5/8). Cell moved for EN (3/8 to 4/8) and LN (4/8 to 5/8). Warrant and method did not move in any field.

| Field | n | Owner before | Owner | Cell | Warrant | Method |
|---|---|---|---|---|---|---|
| AG | 7 | 3/7 | 3/7 | 2/7 | 1/7 | 1/7 |
| AR | 8 | 4/8 | 4/8 | 2/8 | 1/8 | 2/8 |
| BI | 6 | 3/6 | 3/6 | 3/6 | 1/6 | 1/6 |
| BU | 8 | 4/8 | 4/8 | 4/8 | 3/8 | 4/8 |
| CH | 8 | 6/8 | 6/8 | 6/8 | 1/8 | 2/8 |
| CS | 8 | 4/8 | 4/8 | 2/8 | 4/8 | 4/8 |
| DE | 7 | 4/7 | 4/7 | 1/7 | 3/7 | 3/7 |
| EA | 7 | 3/7 | 3/7 | 2/7 | 2/7 | 2/7 |
| EC | 11 | 7/11 | 7/11 | 4/11 | 1/11 | 3/11 |
| ED | 9 | 6/9 | 6/9 | 2/9 | 3/9 | 3/9 |
| EN | 8 | 4/8 | 5/8 | 4/8 | 2/8 | 1/8 |
| EV | 9 | 3/9 | 3/9 | 3/9 | 3/9 | 5/9 |
| HI | 11 | 6/11 | 6/11 | 6/11 | 5/11 | 6/11 |
| IK | 6 | 4/6 | 4/6 | 4/6 | 4/6 | 4/6 |
| IS | 7 | 4/7 | 4/7 | 4/7 | 0/7 | 1/7 |
| LA | 11 | 11/11 | 11/11 | 6/11 | 10/11 | 11/11 |
| LN | 8 | 5/8 | 5/8 | 5/8 | 5/8 | 5/8 |
| MA | 11 | 7/11 | 7/11 | 7/11 | 6/11 | 6/11 |
| MD | 7 | 6/7 | 6/7 | 5/7 | 3/7 | 3/7 |
| MS | 8 | 3/8 | 3/8 | 3/8 | 4/8 | 3/8 |
| PH | 8 | 6/8 | 6/8 | 4/8 | 5/8 | 5/8 |
| PL | 7 | 3/7 | 3/7 | 3/7 | 4/7 | 3/7 |
| PO | 8 | 7/8 | 7/8 | 6/8 | 1/8 | 0/8 |
| RE | 8 | 6/8 | 6/8 | 4/8 | 1/8 | 3/8 |
| ST | 7 | 6/7 | 6/7 | 5/7 | 4/7 | 5/7 |

IK rows stay provisional. They are test labels, not a Māori-led review.

## Warrant confusion (gold row, engine column)

NONE means the engine returned no placement.

| Gold | n | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 | W11 | W12 | W13 | NONE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W1 | 29 | 12 | 0 | 3 | 3 | 3 | 0 | 1 | 0 | 2 | 1 | 2 | 1 | 0 | 1 |
| W2 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| W3 | 20 | 2 | 0 | 12 | 2 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| W4 | 43 | 1 | 0 | 9 | 17 | 2 | 2 | 1 | 2 | 1 | 0 | 0 | 4 | 0 | 4 |
| W5 | 5 | 0 | 0 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| W6 | 7 | 0 | 0 | 2 | 2 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| W7 | 12 | 0 | 0 | 2 | 1 | 0 | 0 | 4 | 2 | 0 | 1 | 1 | 0 | 1 | 0 |
| W8 | 4 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| W9 | 13 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 8 | 0 | 0 | 0 | 0 | 1 |
| W10 | 13 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 11 | 0 | 0 | 0 | 0 |
| W11 | 5 | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| W12 | 39 | 1 | 0 | 13 | 6 | 4 | 6 | 2 | 2 | 0 | 0 | 0 | 5 | 0 | 0 |
| W13 | 11 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 3 | 1 | 0 | 0 | 1 | 5 | 0 |

W12 is the largest off-diagonal. Thirty-nine gold W12 rows, five predicted W12. Thirteen of those went to W3.

## Twenty worst misses

Ranked by owner miss, then cell, warrant and method. The note is the frozen gold note. It is not scored.

1. H203 gold MA.O.A5 W4 M3, engine no placement. "Ignore the outliers and the mean of the sample is the measurement to report." The opening "Ignore" is not the injection heuristic.
2. H201 gold EC.O.A4 W5 M3, engine CH.O.A4 W3 M4. "The central bank raised the official cash rate to reduce inflation."
3. H197 gold AG.O.A5 W3 M4, engine HI.O.A2 W7 M3. "Dairy cows on the irrigated platform produced more milk solids per hectare than cows on the dryland platform."
4. H196 gold EN.O.A1 W11 M7, engine PO.O.A1 W8 M2. "The safety case argues that the residual risk of the dam meets the stated tolerability line."
5. H190 gold LN.O.A3 W4 M3, engine MA.O.A2 W1 M4. "The child was taught the word 'river' by hearing it used of the Waikato."
6. H169 gold BU.O.A5 W12 M1, engine EC.O.A1 W4 M3. "The firm's March return shows output tax of forty-two thousand dollars."
7. H167 gold MA.O.A1 W1 M2, engine CH.O.A1 W3 M4. "Whether P equals NP is an open question."
8. H160 gold CH.O.A1 W4 M3, engine no placement. "Prussian blue is ferric ferrocyanide."
9. H159 gold HI.O.A1 W7 M3, engine EN.O.A1 W11 M7. "The inspection book for 1892 records that the bridge's midspan had settled by half an inch."
10. H158 gold ED.O.A3 W3 M4, engine MA.O.A2 W1 M2. "Pupils who were shown a written proof of the infinitude of primes later solved more transfer items than pupils who were not shown that proof."
11. H149 gold IK.O.A5 W13 M1, engine PO.O.A1 W6 M6. "Maori data sovereignty holds that Maori decide how data about Maori are collected and used." Provisional.
12. H148 gold IK.O.A4 W13 M1, engine PL.O.A2 W9 M2. "Wananga is a setting in which knowledge is discussed and passed on." Provisional.
13. H144 gold IS.O.A1 W12 M1, engine CH.O.A1 W3 M4. "An ISBN identifies a monographic manifestation, not the work in the abstract."
14. H140 gold IS.O.A2 W12 M1, engine CH.O.A1 W3 M4. "Dublin Core defines a small set of metadata elements for describing a resource."
15. H139 gold IS.O.A1 W12 M1, engine CH.O.A1 W3 M4. "A bibliographic record identifies a manifestation by title, creator and date."
16. H138 gold EV.O.A3 W5 M3, engine EN.O.A1 W11 M7. "Eutrophication follows when nutrient loads raise algal growth enough to deplete oxygen."
17. H137 gold EV.O.A5 W5 M3, engine PO.O.A1 W6 M6. "A planetary boundary is a proposed limit beyond which an Earth-system process leaves a Holocene-like state."
18. H136 gold EV.O.A4 W12 M1, engine PO.O.A1 W6 M6. "A marine protected area restricts extractive use inside a stated boundary."
19. H133 gold EV.O.A1 W4 M3, engine BU.O.A1 W12 M1. "Burning coal releases carbon dioxide that was stored in the fuel."
20. H130 gold AG.O.A4 W11 M7, engine CH.O.A1 W3 M4. "Pasteurisation of milk heats it enough to kill target pathogens and then cools it."
