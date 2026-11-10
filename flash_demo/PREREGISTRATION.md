# Pre-registration: does knowledge distance predict failure diversity?

Committed 11 November 2026, before any fault scenario was run on any variant.
The git history is the timestamp. Changes after this commit are listed under "Deviations" in `RESULTS.md`.

## Hypothesis
Among independently designed implementations of one specification, pairs that are further apart in
knowledge lineage fail together less often.

- **H1 (lineage):** failure correlation falls as lineage distance rises.
- **H2 (assumptions):** failure correlation falls as assumption distance rises.
- **Null comparison:** a code-text distance with no knowledge content.

Either hypothesis may be false. A null or opposite result will be reported as such.

## Units
- **Variants:** the 10 estimators in `variants.py`. Each has a mathematics map node (`msc`) and a set of assumptions.
- **Pairs:** 45.
- **Plants:** tracking, thermal, oscillator (`SPEC.md`).
- **Scenarios:** 9 fault classes x 4 levels x 10 repeats = 360 per plant, 1,080 in all (`faults.py`).
  Faults begin at step 150. Seeds start at 20261110 and are disjoint from the development seeds.
- Every variant sees identical data in each scenario.

## Outcome
A trial fails when requirement S1 or S2 is broken (`SPEC.md`).
For each pair, the outcome is the **phi coefficient** between the two variants' pass/fail records.
A pair is dropped from a test when either variant never fails or always fails there. Dropped pairs are counted.

## Predictors
| Name | Definition |
|---|---|
| `lineage_tree` (primary for H1) | Links on the shortest path between the two `msc` nodes, using map and pyramid tree links only. |
| `lineage_full` | The same, with formal cores and correspondence edges added. |
| `assumption` (primary for H2) | 1 minus the Jaccard overlap of the two assumption sets. |
| `code` (null) | Normalised compression distance (zlib) between the two classes' source text. |

## Test
- **Statistic:** Spearman correlation between predictor and phi, over pairs.
- **Significance:** Mantel test with 9,999 permutations of variant labels, one-sided (rho below zero), seed 7.
- **Primary analysis:** all three plants pooled (1,080 scenarios).
- **Threshold:** p below 0.025 for each of H1 and H2 (Bonferroni over two primary tests).
- **Interval:** 95% bootstrap interval for rho, resampling scenarios 2,000 times.
- **Replication:** the same test on each plant alone. Reported, not used for the decision.
- **Secondary:** the pooled test after removing scenarios where all variants agree.
- **Independence check:** observed joint-failure share against the product of the two failure rates.

## Decision rule
- H1 is **supported** if pooled rho for `lineage_tree` is negative with p below 0.025.
- H2 is **supported** if pooled rho for `assumption` is negative with p below 0.025.
- A supported hypothesis is **credited to knowledge content** only if the `code` predictor does not do as well.
- Otherwise the hypothesis is **not supported** by this experiment.

## What was done before this commit
- Variants were run on fault-free data only, with development seeds from 900000.
  All ten met S1 on all three plants at the first attempt. No parameter was changed afterwards.
- Predictor values were computed and inspected. No fault data existed at that point.
- No fault scenario had been run on any variant.

## Known weaknesses, stated in advance
1. **One author.** One model wrote the variants, their assumption sets, their map nodes and the fault list.
   The variants are not independently designed in Knight and Leveson's sense, and the assumption sets are judgements.
2. **Lineage nodes were assigned by the author.** The transfer operator did not propose the variants.
3. **Shared inputs.** Seven variants use the same plant model. All ten use the same sensor.
4. **Small n.** Ten variants give 45 dependent pairs. Only a strong effect can be detected.
5. **Toy scale.** Three small linear plants in simulation. Nothing here shows the result would hold for real systems.
6. **Coarse lineage scale.** `lineage_tree` takes only four distinct values across the 45 pairs.
7. **Fault choice.** The fault classes were chosen by the author and are not a sample of real-world faults.
