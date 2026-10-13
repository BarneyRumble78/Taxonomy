# Retrieval test 2: free fix (14 Oct 2026, $0 Claude)

The Mac was offline when I checked, so everything here ran deterministically on the box. Gold labels are unchanged. The 10 held-out questions (`heldout_gold.json`) were committed before the fix was built.

## What changed
- **Keywords:** every pillar (120) has curated plain-English keywords plus terms taken from its member topics, and every section with members has keywords from its member labels plus a small synonym map. See `pyramids/curated/pillar_keywords.json`.
- **19 added groups / 80 leaves**, marked `"added": true, "source": "minerva-curated"` (`pyramids/curated/added_topics.json`). They cover CS AI/agent security and generative AI; LA medicines regulation (Medsafe, drug approval) and everyday legal processes; EC labour markets/wages; EN civil structures (bridges, seismic); HI war and conflict; PL free will/determinism and normative ethics; RE world religions and worship; MA foundations and everyday discrete maths; ST contemporary security; DE product and inclusive design; AR genres and themes; PO elections and voting.
- **Checks:** the edits only add material. Minto issue counts are identical before and after, every group still has 2–5 members, and `check.py` passes.
- **Retrieval v2** (`scripts/retrieval_test_v2.py`): each field is scored by its best section, so big fields no longer win just by size, and the pillar top-3 can come from any field.

## Results (pillar top-1 / top-3, field top-1 / top-3)
| Set | Before (v1 retrieval, old pyramids) | Content only (v1, new) | Retrieval only (v2, old) | **After (v2, new)** |
|---|---|---|---|---|
| Original 20 | P 9/12 · F 13/17 | P 13/16 · F 17/19 | P 12/15 · F 15/20 | **P 14/19 · F 18/20** |
| Held-out 10 | P 3/4 · F 4/6 | P 3/5 · F 5/6 | P 5/6 · F 5/7 | **P 4/6 · F 5/7** |

## Overfitting
The gaps were found from the 20 tuning questions, and 7 of the additions directly target one of them (marked `in_sample`). So the jump from 9 to 14 on the original 20 overstates the real gain. On the held-out set the gain is small (pillar top-1 3→4, field top-1 4→5), and most of it comes from the retrieval change, not the added content. The added content even hurt one held-out question: H01 (LLM essay grading) now lands on CS AI security. The fair estimate is about 40–50% pillar top-1 on unseen questions.

## Remaining weak spots
- **Word collisions across fields:** "herd" sends vaccination (H09) to dairy herds, "earthquake" sends tsunami (H05) to EN civil structures, "defend" sends drones (H07) to law, and "prime numbers" (H08) goes to PH. "Emissions" still sends the catalytic converter question (T13) to EV, and "vehicle" still sends the autonomous-car liability question (T20) to EN.
- **Missing topics:** ST has no drones or unmanned systems, PL.K4 has nothing on lying or applied ethics, MA.K1 has no prime-number leaf (deliberately left out to keep the held-out set clean), and MD.K5 has no vaccination leaf.
- **Same-field confusion:** in ED, the assessment pillar still loses to the learners pillar.
- **Fix needed:** keyword search can't resolve meaning. It needs semantic reranking (Qwen on the Mac, or local embeddings).
