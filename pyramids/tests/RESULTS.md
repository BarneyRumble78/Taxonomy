# Minerva retrieval test 1 (14 Oct 2026)

**Method.** The Mac's Qwen was offline (the machine was disconnected on both checks), so retrieval is a deterministic top-down BM25 on the box: pick the field, then rank the pillars inside the top field only, then the section, then the group. Script: `scripts/retrieval_test.py`. Gold labels were committed before the run (`retrieval_gold.json`). Alternate fields/pillars were accepted for cross-field questions.

| Level | Top-1 | Top-3 |
|---|---|---|
| Field | 13/20 (65%) | 17/20 (85%) |
| Pillar | 9/20 (45%) | 12/20 (60%) |

## Misses (pillar top-1)
| Q | Gold | Got | Cause |
|---|---|---|---|
| T01 AI-agent prompt injection | CS.K5 | IS.K4 | Retrieval (no synonym for "protected"→security) + pyramid gap: no AI/LLM/agent security topic in CS.K5 |
| T02 Medsafe approval | LA.K4 / MD.K4 | MD.K5 | Pyramid: no medicines or drug regulation anywhere in LA; MD routes it to prevention |
| T05 free will | PL.K1 | BU (field) | Pyramid: PL.K1 is 46 tokens with no free will/determinism; "will" and "compatible" pulled it to business |
| T08 minimum wage | EC.K3 | PO | Pyramid: EC has no labour market, wage or employment topics |
| T13 catalytic converter | CH.K4 | EV | Retrieval: "emissions/nitrogen" pull to EV; CH.K4 has catalysis |
| T14 earthquake bridge | EN.K2 | DE | Pyramid: EN (727 topics) has no bridges or seismic/earthquake engineering |
| T15 causes of WWI | HI.K3 | HI.K4 | Pyramid: HI has no "war" topic at all; the cause pillar is thin |
| T16 formative assessment | ED.K4 | ED.K2 | Retrieval: ED.K4 has the terms; the larger learner pillar wins |
| T17 MMP / PR | PO.K2 | CS | Retrieval: "representation/systems" pull to CS; PO has parties and elections |
| T19 revenue accounting | BU.K1 | EC | Retrieval (mostly): BU.K1 has accounting but not revenue or recognition |
| T20 autonomous-vehicle liability | LA.K3 | EN.K2 | Retrieval: "vehicle" pulls to EN; LA.K3 has liability and tort |

Split: 6 pyramid (T01 partly, T02, T05, T08, T14, T15), 5 retrieval (T13, T16, T17, T19, T20).

## Coverage imbalance (leaf topics per field)
PH 3390, ED 2283, AG 1142, LN 853, EN 727 … PO 132, LA 128, CH 125, AR 89, DE 62, MA 60, ST 55, **RE 19**. The thin fields have short labels and few everyday words, and big fields soak up lexical matches.

## Question pyramids (T03, T04, T09)
I drafted these on the box from general knowledge, because Qwen was offline and no sources were fetched. Sonnet's strict review **failed all three**: there were no sources, the key lines weren't cleanly MECE (T04 and T09), some linked nodes were weak, and some claims were imprecise (the explicit-formula wording; "permanently" in T09). Details: `question_pyramid_judgements.json`. Claude spend: **$0.049**.
