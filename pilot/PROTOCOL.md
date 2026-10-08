# Part 5 — Placement protocol

This is a protocol, not a study. No coding has been done and no α is reported. Every number below is a design parameter or a comparator, not a result.

## 5.1 What is tested
Whether three independent coders, given only this file, place the same claim in the same home. A home has four parts: the owning pyramid, the Face O cell, the Face W warrant type, and the Face M role of the method behind the claim. Each part is scored separately.

## 5.2 Sample: fifty claims
- **Unit.** One declarative sentence, as published, with its citation. Not a paper, not a topic.
- **Frame.** Sentences drawn from abstracts and textbooks across all 25 pyramids.
- **Allocation.** Stratified: 25 claims, one per pyramid (MA and the 24 others), drawn at random from that field's literature. Then 25 border claims, drawn from the registry's "uses" edges, where one pyramid cites another. The border half is where the system is most likely to fail, so it is over-sampled on purpose.
- **Exclusions.** Claims under IK and RE·T are coded only with Māori-led and tradition-competent review. They are reported separately and never pooled.
- **Freeze.** The 50 sentences are fixed, hashed and published before coding begins.

## 5.3 Coders
- Three coders: one subject specialist per draw (rotating), one information scientist, and one generalist. Optionally a fourth, AI coder, reported separately and never pooled with the humans.
- Coders work blind to each other and to the author's intended home.
- Training: one hour on the standard and on ten practice claims that are not in the sample.
- Each coder records a home for each of the four faces and a one-line reason.

## 5.4 Agreement measure
- **Statistic.** Krippendorff's α, nominal level, computed separately for each face: owner, O-cell, W-type and M-role. Three coders, fifty units; missing values allowed.
- **Uncertainty.** Bootstrap 95% interval (10,000 resamples of units).
- **Thresholds (Krippendorff's conventional bands).** α ≥ .800 means the face is reliable. .667 ≤ α < .800 is tentative. α < .667 means the face is not yet a usable code.
- **Comparator.** Agreement between MathSciNet and zbMATH on MSC codes for the same articles: F1 0.83 at the top level, 0.72 at the second and 0.58 at the third, on 78,063 articles (source as given in related_work.md). α and F1 are different statistics. The comparison is a reading guide: the owner face should do no worse than the top-level F1, and O-cells no worse than the second.

## 5.5 Decision rules (fixed before coding)
1. If owner α < .667, the ownership rule and the border rules are revised before any other face is examined.
2. If O-cell α is tentative or worse in a pyramid, that pyramid's key line is re-cut. Re-cutting goes back to Phase 3.
3. If W-type α < .667, the controlled list W1–W13 is not yet a code. Merge or redefine the types the confusion matrix shows are confused.
4. Every disagreement is logged with the three reasons. The log is published with the ledger.
5. The protocol's results are reported whatever they show.

## 5.6 What would count against the system
- Coders agree on an owner but disagree on the cell. That means the key lines are not mutually exclusive.
- Coders place border claims by surface vocabulary rather than by warrant. That means the ownership rule is not being applied.
- Agreement is high only for the specialist coder. That means the file depends on expertise it does not write down.
