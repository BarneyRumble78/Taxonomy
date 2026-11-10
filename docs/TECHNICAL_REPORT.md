# Generating Meaningful Cyber-Physical Heterogeneity: Formal Interlingua, Cross-Lineage Transfer, and Empirical Verification of the Assumption Distance Hypothesis

**Technical report:** TR-2026-TAX-01, revision 2
**Author:** Chris Townsend. Prepared with AI assistance (Claude; an earlier draft by Antigravity).
**Date:** 11 November 2026
**Repository:** `github.com/BarneyRumble78/Taxonomy`, branch `v4-generative`
**Status:** draft for the owner's review. Not submitted anywhere.

Revision 2 replaces revision 1 (commit `3aa133a`). Revision 1 described plants, fault classes, file names and
figures that do not match the experiment that was run. Every figure below is taken from
`flash_demo/results/` and can be regenerated with `make reproduce`.

---

## Abstract

Independently written versions of one specification tend to fail together (Knight and Leveson, 1986; citation not re-checked for this report, UNVERIFIED).
DARPA's FLASH request for information asks for metrics of heterogeneity between implementations.
We ask whether a map of knowledge can say in advance which pairs of implementations will fail differently.

We built ten estimators of one quantity, each from a different mathematical lineage, to one specification.
We ran them on three small simulated plants under 1,080 fault scenarios, and measured how strongly each pair's failures were correlated.
The hypotheses, predictors, test and decision rule were committed before any fault run.

Two results follow. First, distance between the methods' positions in a classification of mathematics did not predict failure correlation
(Spearman rho −0.20, one-sided p = 0.114). Second, distance between the methods' stated assumptions did
(rho −0.86, 95% interval −0.88 to −0.82, p = 0.0001), and did so on each plant separately.
A text-compression distance with no knowledge content also predicted it, more weakly (rho −0.45, p = 0.004).

The experiment is small, simulated and single-authored. It supports a design suggestion, not a general claim:
measure heterogeneity by the overlap of stated assumptions, including the assumptions every variant shares.

---

## 1. Problem

Redundancy protects a system only if its channels fail at different times.
Knight and Leveson's experiment found that separately written programs failed on the same inputs more often than independence predicts.
A common reading is that designers share training and therefore share mistaken beliefs.

FLASH (RFI DARPA-SN-27-17, as described in the project handover; not re-checked against the RFI text, UNVERIFIED) seeks many
implementations of one formal specification that are equivalent in function and different in a way that matters.
That needs a measure of difference that predicts failure behaviour before deployment.

Taxonomy holds structured summaries of 25 fields. Rule R5 of its standard requires every named tool to state its hypotheses.
This report tests whether that material yields a usable heterogeneity metric.

## 2. Design

### 2.1 Formal cores
A formal core is one mathematical structure with its field-specific readings (`rosetta/cores.json`, schema in `schemas/`).

| Part | Content |
|---|---|
| Structure | One sentence free of any field's vocabulary |
| Mathematics node | The node in the MSC2020 map that owns the structure |
| Roles | Named slots, such as state, dynamics, observation |
| Assumptions | Separate checkable statements |
| Guarantee | What follows when every assumption holds |
| Bindings | Per field: what fills each role, which assumptions are met, where the analogy breaks |

The validator rejects a binding that states no limit.
The current seed holds 12 cores with 56 bindings across 12 fields. All are drafts written by one model from general knowledge.
None has been checked against a source.

### 2.2 Correspondence edges
A typed edge links two nodes and records the mapping, the conditions and the differences (`correspondences/`).
There are 188 edges: 71 from `uses` citations in the pyramids, 15 from the mathematics correspondences table,
and 102 derived from pairs of cells that share a core. The 102 derived edges are marked `generated-unverified`.

### 2.3 Operations
All operations are deterministic and call no model (`engine/v3/rosetta.py`).

| Operation | Result |
|---|---|
| `find` | Cores and bindings matching a query |
| `translate` | Role-by-role mapping between two fields, with assumption differences |
| `holes` | Fields where a core has no binding, stated as questions |
| `distance` | Lineage distance and assumption distance |

`translate` withholds the guarantee unless every assumption holds in both fields.

## 3. The transfer operator

`engine/v3/transfer.py` carries a core into a field that does not bind it. It has two stages.

1. **Brief (no model).** It lists the existing bindings, most distant first, and asks one question per role and per assumption.
2. **Fill (optional model).** A model proposes answers. The answer is validated strictly and always marked `generated-unverified`.
   An answer with no stated mismatch is rejected.

Five sample runs used a local model (`qwen3.6:27b`). All five passed validation.
In all five the model judged the transfer already known in the target field, and in none did the guarantee carry.
These are five observations, not an evaluation. No claim in those records has been checked against a source.

The operator did not propose the estimator variants in section 5. They were chosen by the author of the experiment.

## 4. Distance measures

| Measure | Definition | Properties |
|---|---|---|
| Lineage (tree) | Links on the shortest path between two nodes, through map parents, cells, fields and a common root | A shortest-path metric on an undirected graph |
| Lineage (full) | The same, with core hubs and correspondence edges added | A metric; sensitive to how densely a field has been written up |
| Assumption | 1 minus the Jaccard overlap of two assumption sets | Jaccard distance is a metric; range 0 to 1 |
| Code (null) | Normalised compression distance between two classes' source text | No knowledge content; used as a comparison |

Across the 45 variant pairs, tree lineage and assumption distance were nearly uncorrelated (rho 0.03), so the experiment could separate them.
Tree lineage took only four distinct values.

## 5. The FLASH demonstrator

### 5.1 Specification
One component: a discrete-time estimator of a single measured quantity (`flash_demo/SPEC.md`).

| ID | Requirement | Check |
|---|---|---|
| S1 | Error exceeds 2 sigma in at most 5% of scored steps | Simulation |
| S2 | Every output is finite for any readings, including missing ones | Property-based tests |
| S3 | With disturbances inside 3 sigma, error stays within 5 sigma once inside | z3, one plant, three variants |
| S4 | Mean compute time per step under 5 ms | Timing test |

A trial fails when S1 or S2 is broken.

### 5.2 Plants
Three linear plants in simulation: a constant-velocity tracking target, a first-order thermal mass with a known heater input,
and a lightly damped oscillator. Each trial runs 400 steps; the first 50 are not scored; faults begin at step 150.

### 5.3 Variants

| Variant | Method | Mathematics node | Assumptions relied on |
|---|---|---|---|
| kalman | Kalman filter | `MSC:93E11` | 8 |
| huber_kalman | Kalman filter with clipped innovation | `MSC:62F35` | 6 |
| luenberger | Pole-placement observer | `MSC:93B53` | 4 |
| h_infinity | Minimax filter | `MSC:93B36` | 4 |
| particle | Bootstrap particle filter | `MSC:65C35` | 8 |
| moving_horizon | Windowed least squares | `MSC:93E24` | 5 |
| bounded_error | Windowed minimax fit | `MSC:65G40` | 5 |
| alpha_beta | Fixed-gain tracker, no model | `MSC:93C55` | 5 |
| low_pass | Exponential smoothing, no model | `MSC:94A12` | 4 |
| repeated_median | Robust line fit, no model | `MSC:62G35` | 3 |

Assumptions are drawn from a shared list of eleven (`flash_demo/variants.py`). All ten variants rely on an unbiased sensor.
Seven use the plant model.

### 5.4 Faults
Nine classes, four levels each, ten repeats: 360 scenarios per plant and 1,080 in all.
The classes are bias, slow drift, dropout, stuck sensor, saturation, outliers, heavy-tailed noise, raised noise and unmodelled forcing.
Every variant saw identical data in each scenario.

### 5.5 Verification before the campaign
- All ten variants met S1 on all three plants in fault-free runs, at the first attempt. No parameter was changed afterwards.
- Property-based tests found no reading sequence that produced a non-finite output.
- z3 proved an invariant error bound on the thermal plant for three variants at their settled gains:
  luenberger 1.816, kalman 2.174, h_infinity 2.080, each below the S3 limit of 2.5. z3 also refuted a bound 1% tighter in each case.

This is verification-lite. The proofs concern a model of the loop. They say nothing about the Python code, floating-point rounding,
the two-state plants or the period before gains settle. The variants are not proved equivalent to one another.

## 6. Evaluation

### 6.1 Pre-registration
`flash_demo/PREREGISTRATION.md` was committed at 18:59 NZDT on 10 November 2026 (commit `62844e6`), before any fault scenario was run.
It fixed two hypotheses, the predictors, the Mantel permutation test, a threshold of p below 0.025 for each hypothesis, and the decision rule.

- **H1:** failure correlation falls as tree lineage distance rises.
- **H2:** failure correlation falls as assumption distance rises.

### 6.2 Primary result (three plants pooled, 1,080 scenarios, 45 pairs)

| Predictor | Spearman rho | 95% bootstrap interval | One-sided p | Verdict |
|---|---|---|---|---|
| Lineage (tree) | −0.20 | −0.25 to −0.14 | 0.1142 | H1 not supported |
| Lineage (full) | −0.26 | −0.31 to −0.21 | 0.0638 | Not significant |
| Assumption | −0.86 | −0.88 to −0.82 | 0.0001 | H2 supported |
| Code (null) | −0.45 | −0.47 to −0.42 | 0.0042 | Predicts, less well than assumption |

The p-values come from 9,999 permutations of variant labels. The intervals resample scenarios, not variants,
so they understate uncertainty about which variants were chosen.

### 6.3 Replication by plant

| Plant | Lineage (tree) rho, p | Assumption rho, p | Code rho, p |
|---|---|---|---|
| tracking | −0.19, 0.096 | −0.42, 0.014 | −0.31, 0.026 |
| thermal | −0.09, 0.232 | −0.88, 0.0001 | −0.31, 0.041 |
| oscillator | −0.29, 0.054 | −0.70, 0.0001 | −0.46, 0.005 |

Assumption distance was significant on each plant. The effect was weakest on the tracking plant.
Removing the 440 scenarios in which all variants agreed left the pooled result unchanged (assumption rho −0.85, p = 0.0001; 640 scenarios).

### 6.4 The null predictor
Code distance was also significant. Variants that share a plant model share a base class, so their source text is similar.
An exploratory partial correlation suggests the assumption effect is not explained by code similarity:
assumption given code, −0.83; code given assumption, −0.21.
This check was added after the results were seen. It was not pre-registered and carries no significance test.

### 6.5 Were failures independent?
No. Both variants of a pair failed in 36.0% of scenarios, against 23.5% expected under independence, a ratio of 1.53.
Mean pairwise phi was 0.52. This reproduces Knight and Leveson's pattern at small scale.

### 6.6 Failure rates

| Variant | Failures | Rate | Wilson 95% interval |
|---|---|---|---|
| huber_kalman | 341/1080 | 31.6% | 28.9% to 34.4% |
| particle | 389/1080 | 36.0% | 33.2% to 38.9% |
| kalman | 442/1080 | 40.9% | 38.0% to 43.9% |
| h_infinity | 457/1080 | 42.3% | 39.4% to 45.3% |
| repeated_median | 526/1080 | 48.7% | 45.7% to 51.7% |
| moving_horizon | 541/1080 | 50.1% | 47.1% to 53.1% |
| luenberger | 557/1080 | 51.6% | 48.6% to 54.5% |
| alpha_beta | 641/1080 | 59.4% | 56.4% to 62.2% |
| low_pass | 648/1080 | 60.0% | 57.0% to 62.9% |
| bounded_error | 704/1080 | 65.2% | 62.3% to 68.0% |

Overall, 5,246 of 10,800 trials failed. The fault levels were set to be severe, so these rates describe the campaign, not field reliability.

### 6.7 Where diversity helped and where it could not
- **Sensor bias and slow drift defeated every variant.** Failure rates under bias ran from 43% to 84%, and under drift from 68% to 100%.
  All ten assume an unbiased sensor. Diversity of algorithm does not remove a shared assumption.
- **Unmodelled forcing split the variants by model use.** The Kalman and particle filters failed in 93% and 100% of those trials. The model-free tracker failed in none.
- **Outliers split them by robustness.** The bounded-error estimator failed in every outlier trial. The Huber filter failed in none and the repeated median in 2%.

## 7. Limitations

1. **One author.** One model wrote the variants, their assumption sets, their map nodes and the fault list.
   The assumption sets were fixed before any fault run, but their author knew the algorithms. Part of the effect may reflect that knowledge.
   This is the most serious limit on H2.
2. **The variants were not independently developed.** They share a code base, a plant model and a sensor. Knight and Leveson studied separate teams.
3. **Small n.** Ten variants give 45 dependent pairs. A different ten might behave differently.
4. **Toy scale.** Three small linear plants in simulation. Nothing here shows the result holds for real cyber-physical systems.
5. **Chosen faults.** The fault classes were chosen by the author and are not sampled from field data.
6. **Coarse lineage scale.** Tree lineage took four values. A finer or better-founded lineage measure might do better. H1 is not refuted in general.
7. **Verification-lite.** Section 5.5 states what was and was not proved.
8. **The knowledge layer is unverified.** The 12 cores are drafts. The experiment did not use them: it used assumption sets written for the ten variants.
9. **No evaluation of the generative claim.** Whether the engine proposes useful cross-field transfers has not been tested.
10. **Licensing is unresolved.** Several subfield maps carry non-commercial or no-derivatives terms, and the repository has no licence file.

## 8. What a full standard still requires

| Gap | What would close it |
|---|---|
| Single authorship | Assumption sets written by people who have not seen the code; variants written by separate teams or separate models |
| Scale | More variants, nonlinear plants, and at least one hardware-in-the-loop or published benchmark system |
| Fault realism | A fault list drawn from a published taxonomy or incident data, fixed by a third party |
| Confirmation | A second pre-registered run on new plants and new variants, with the partial-correlation test registered in advance |
| Equivalence | Machine-checked proofs that variants meet one formal specification, at least for a small case |
| Knowledge layer | Each core reviewed against cited sources by a field specialist; assumption sets derived from the cores, not written beside them |
| Generative evaluation | A held-out retrodiction set authored independently, with baselines and ablations, and a prospective set after the model's cut-off |
| Reproducibility | Pinned dependency versions; the campaign and analysis run in CI |
| Licensing | A licence audit of every imported scheme, and a licence file |

## 9. Reproduction

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
make check            # conformance checks
make test             # 300 tests
make flash-verify     # z3 bounds
make reproduce        # rebuilds flash_demo/RESULTS.md from the logged campaign
make flash-campaign   # reruns all 1,080 scenarios (about one minute on the development machine)
```

Dependency versions are not yet pinned. The campaign uses fixed seeds.
Cost: USD 0. The experiment used no model. The five transfer samples used a local model.

## 10. Conclusion

In one small pre-registered simulation, overlap of stated assumptions predicted which implementations failed together.
Position in a classification of mathematics did not. Faults that violated an assumption shared by every variant defeated all of them.

The suggestion for heterogeneity work is specific and testable: record each variant's assumptions, measure their overlap,
and treat any assumption common to all variants as a single point of failure.
Whether this holds beyond a toy setting is an open question that the steps in section 8 would address.
