# Part 5A — Placement pilot (AI coders), run 9 October 2026

**This is a pilot, not the study.** It tests whether the protocol works and where the code breaks. It cannot be reported as the reliability of the taxonomy, for four reasons.
1. **The coders are AI models from the same family as the author.** Coder A was Claude Haiku, B was Claude Sonnet and C was Claude Opus, each working blind and alone. Shared training makes agreement easier than it would be for people.
2. **The author wrote the 50 claims.** They were not sampled from the literature as the protocol requires.
3. **The coders used a condensed codebook** (pilot/codebook.md), not the full file.
4. **The protocol says AI coders are reported separately and never pooled with humans.** That rule holds here. The human study (5.3) has not been run.

## Design as run
- **Claims.** 50 in all. 24 were core claims, one per pyramid excluding IK. 24 were border claims. 2 were Indigenous-knowledge claims, coded but held out of every α, as the protocol requires.
- **Coding.** Each coder recorded an owner, a cell (A-level), a warrant and a method for each claim.
- **Statistic.** Krippendorff's α (nominal), with a bootstrap 95% interval from 2,000 resamples.

## Results (48 pooled claims, 3 coders)

| Face | α | 95% interval | Band | Mean agreement with author's key |
|---|---|---|---|---|
| Owner | 0.928 | 0.864–0.985 | reliable (≥ .800) | 0.90 |
| Cell (A-level) | 0.717 | 0.611–0.813 | tentative | 0.74 |
| Warrant | 0.821 | 0.726–0.906 | reliable | 0.81 |
| Method | 0.832 | 0.733–0.916 | reliable | 0.76 |

| Stratum | Owner α | Cell α |
|---|---|---|
| Core (24) | 0.971 | 0.829 |
| Border (24) | 0.883 | 0.603 (below .667: not yet a usable code) |

**Comparator, read with care.** MathSciNet and zbMATH agree at F1 0.83 at the top MSC level and 0.72 at the second. α and F1 are different statistics. This pilot is also easier than that comparison: the claims were written by the author and coded by models of one family.

## What the pilot found (decision rules 5.5 applied)
Owner α clears .800, so rule 1 does not trigger. Cell α is tentative overall and fails on border claims, so rule 2 triggers: the key lines and border rules named below are re-examined. In five owner disagreements, all three coders, or two of them, disagreed with the author's key. Those are read as faults in the key or the code, not in the coders.

| # | Claim | Key | Coders | Finding | Repair |
|---|---|---|---|---|---|
| 19 | Mishnah redacted c. 200 CE | RE.O.A2 | HI, HI, HI | The dated-fact rule (HI) and RE.O.A2.2 "transmission" both claim it | A dated event in a text's history is HI. RE.O.A2.2 keeps claims about the transmitted text as text (variants, recension). Add to RE rules. |
| 43 | Great Wave uses Prussian blue | CH | AR, AR, AR | AR's own rule says pigment identity is CH, but the codebook lacked that rule | Add the material-identity border rule to the codebook |
| 46 | Aquinas argues from motion | RE | RE, PL, PL | The prime-mover argument starts from premises any reasoner may grant, so by RE's own rule 3 it is PL. The key was wrong. | Key corrected to PL; the report of what Aquinas held stays RE·S |
| 39 | P vs NP is open | MA | MA, CS, CS | "Computation → CS" in the codebook overrides MA.B.C3 | State "open problems and theorems in complexity → MA" in the ownership rule |
| 44 | Great Wave sold in Edo shops | HI | AR, HI, AR | Reception (AR.O.A4) against dated fact (HI) | Market facts are HI; their reading as reception is AR.O.A4. Add to AR rules. |
| 24 | TREC recall fell | IS | CS, IS, IS | Split decision; the rule holds | none |
| 49 | 1080 and kererū nesting | EV | EV, BI, EV | Split decision; the rule holds | none |

Cell-level faults in the author's own pyramids, found by the pilot:
- **PH:** nuclear decay sat in A5.4.3 while nuclear structure sat in A2.3 (claim 38). Decay moves to A2.3.
- **EN:** the key line is a set of physical balances, so a design-life requirement (claim 41) has no cell. Two coders forced it into EN.O.A1. This is a real gap. Repair: add a requirements home (W12) to EN, or file specifications under EN.M (verification).
- **DE A2 vs A3** (claim 42) and **EV A2 vs A3** (claim 23): coders split between state and impact, and between form and performance in use. Repair: sharpen the definitions of these neighbouring cells.

## Indigenous-knowledge claims (held out, not pooled)
- **Claim 25 (kaitiakitanga):** all three coders gave IK, W13. Cells split between IK.O.A2 and IK.O.A3.
- **Claim 48 (whakapapa in a Native Land Court minute book):** two coders gave HI, W7; one gave IK.O.A4, W7. The split is exactly the contested line between a dated record and transmission. Only the Māori-led review can settle it.

## Status
The pilot shows that the protocol runs and that the owner face is promising. Cells on border claims are not yet a code. The human study (three human coders, claims sampled from the literature) remains the gate for any reported reliability.
