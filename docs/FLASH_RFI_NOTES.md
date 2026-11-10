# Response Notes for DARPA RFI DARPA-SN-27-17 (FLASH)
## Formal Learning and Abstractions for System Heterogeneity

**Status:** draft notes for Chris Townsend to review, edit and send himself. Not a submission.
**Date:** 11 November 2026. RFI responses are due 30 November 2026 (from the handover; UNVERIFIED against the RFI text).
**Evidence:** `docs/TECHNICAL_REPORT.md` revision 2 and `flash_demo/`. Every figure below is from the logged results.

These notes replace the version in commit `3aa133a`, which contained figures from no results file.

---

### 1. Points to check against the RFI text before writing the response

I have not read the RFI. Please confirm each of these, because the response should answer what DARPA asked.

- The exact questions asked, and any page limit or required format.
- Whether respondents must be US entities, and any export-control or citizenship conditions.
- Whether DARPA asks for capabilities, for ideas, or for both.
- The office name and the response address.
- Whether attached reports or links to public repositories are welcome.

### 2. The one thing we can say with evidence

> In a small pre-registered simulation, overlap of stated assumptions predicted which implementations failed together.
> Position in a classification of mathematics did not.

Supporting figures, for ten estimator variants on three simulated plants under 1,080 fault scenarios:

| Candidate metric | Spearman rho with failure correlation | One-sided p (permutation) |
|---|---|---|
| Assumption distance | −0.86 (95% interval −0.88 to −0.82) | 0.0001 |
| Classification-tree distance | −0.20 | 0.114 |
| Code-text distance (comparison) | −0.45 | 0.004 |

- The assumption result held on each plant separately (p = 0.014, 0.0001, 0.0001).
- Failures were not independent: joint failures occurred in 36.0% of scenarios, against 23.5% expected.
- Sensor bias and drift defeated all ten variants, because all ten assume an unbiased sensor.

### 3. Suggested core message (plain version)

1. **The problem FLASH names is real at small scale.** Our ten variants failed together well above the independence rate.
2. **A candidate metric.** Record the assumptions each variant relies on. Measure heterogeneity as one minus their overlap.
3. **A corollary worth stating.** An assumption shared by every variant is a single point of failure. A heterogeneity metric should report it.
4. **A negative result.** Distance in a subject classification did not work as a metric here. We tested it and say so.
5. **Where Taxonomy fits.** Its standard already requires every tool to state its hypotheses. That makes the metric computable from existing material.

### 4. Limits that should appear in the response

Stating these protects credibility. A reviewer will find them anyway.

- One author (an AI model) wrote the variants, their assumption lists and the fault list. The lists were fixed before any fault run.
- Ten variants, three small linear plants, simulation only.
- The variants share a code base and a sensor. They were not developed independently.
- Verification is light: property tests, and z3 bounds for three variants on one plant. Nothing is proved about the code.
- The code-text comparison also predicted failure correlation. A later check suggests assumptions carry the effect, but that check was not pre-registered.
- The knowledge layer (12 formal cores) is an unreviewed draft, and was not used in the experiment.

### 5. Claims to avoid

Each of these appeared in the earlier draft and is not supported.

| Avoid | Why |
|---|---|
| "Provably heterogeneous" or "provably resilient" | Nothing of the kind was proved |
| "Breakthrough" | One small simulation |
| "Eliminates common-mode failures" | Bias defeated every variant |
| "Code diversity does not predict failure independence" | It did, more weakly |
| "The transfer operator generated the variants" | The variants were hand-chosen |
| Named defence platforms as transition targets | No work supports them |
| "960 scenarios", "r = −0.38", or any failure table from the earlier draft | Not in any results file |

### 6. Questions the response could put to DARPA

- Would FLASH consider assumption overlap as one of its heterogeneity metrics?
- Is there a reference set of variants and faults against which metrics can be compared?
- How does FLASH define "meaningfully different", and is failure correlation the intended test?

### 7. Decisions for Chris before drafting

1. Taxonomy alone, or with Blade Runner as a security case? (Still open from the handover.)
2. Whether to cite the public repository. It is currently public, including these drafts.
3. Whether to attach the technical report, and under which title. The current title says "Empirical Verification"; "a small pre-registered test" would be more accurate. I have not changed it.
4. How to describe AI assistance in authorship.
5. The licence position on imported classification schemes, before any material is offered for use.
6. The contact address to give. None is recorded here.

### 8. What would strengthen the response before 30 November

In rough order of value for effort:

1. Have a person who has not seen the code write the assumption lists, then rerun the analysis. This addresses the main weakness.
2. Add one nonlinear plant and rerun as a second pre-registered study.
3. Pin dependency versions and run the campaign in CI.
4. Read the RFI and map each of its questions to a paragraph.
