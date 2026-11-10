# FLASH demonstrator: one-page summary

10 November 2026. Full tables: `RESULTS.md`. Method fixed in advance: `PREREGISTRATION.md` (commit `62844e6`).

## Question
DARPA's FLASH RFI asks for heterogeneity metrics. Knight and Leveson (1986) showed that independently
written versions still fail together. Can a knowledge map say in advance which pairs of implementations
will fail differently?

## What was done
- One specification: a single-output state estimator (`SPEC.md`).
- Ten implementations from ten mathematical lineages, on three small simulated plants.
- 1,080 fault scenarios in nine classes. Every variant saw identical data.
- For each of the 45 pairs, the correlation (phi) between their pass/fail records.
- Four distance measures, tested against that correlation by a permutation test.

## Result

| Predictor | Spearman rho | 95% interval | One-sided p | Verdict under the pre-registered rule |
|---|---|---|---|---|
| Lineage distance (tree) | -0.20 | -0.25 to -0.14 | 0.114 | **H1 not supported** |
| Lineage distance (with cores and edges) | -0.26 | -0.31 to -0.21 | 0.064 | Not significant |
| Assumption distance | -0.86 | -0.88 to -0.82 | 0.0001 | **H2 supported** |
| Code-text distance (null) | -0.45 | -0.47 to -0.42 | 0.004 | Predicts, but less well |

- **Position in the classification tree did not predict failure diversity.** The handover's stated hypothesis is not supported here.
- **Shared assumptions did.** Pairs relying on the same assumptions failed together; pairs relying on different ones did not.
  The effect held on each plant alone (p = 0.014, 0.0001, 0.0001).
- **The null predictor also carried signal.** Variants that share a model also share code.
  In an exploratory check, assumption distance kept its effect after allowing for code distance (partial rho -0.83).
  Code distance mostly lost its effect after allowing for assumption distance (partial rho -0.21). This check was not pre-registered.
- **Failures were far from independent.** Both variants of a pair failed in 36.0% of scenarios, against 23.5% expected
  under independence. Mean phi was 0.52. This is Knight and Leveson's pattern in miniature.
- **Some faults defeat every variant.** Sensor bias and slow drift caused failure in all ten, because all ten assume an
  unbiased sensor. No amount of algorithmic diversity removes a shared assumption.
- **Diversity helped where assumptions differed.** Under model mismatch the Kalman and particle filters failed in 93% and 100% of trials;
  the model-free tracker failed in none. Under outliers the bounded-error estimator failed in every trial; the Huber filter in none.

## Verification
- S1 accuracy: all ten variants passed on all three plants in fault-free runs, with no tuning.
- S2 totality: property-based tests found no input sequence giving a non-finite output.
- S3 safety bound: z3 proved a worst-case error bound for three fixed-gain variants on the thermal plant (`verify.py`).
- This is verification-lite. Nothing is proved about the Python code, and the variants are not proved equivalent.

## What this does and does not show
It shows, in one small pre-registered simulation, that a metric built from stated assumptions predicted failure
diversity and a metric built from classification position did not.

It does not show that this holds for real cyber-physical systems. The main reasons:
1. **One author.** One model wrote the variants, the assumption sets and the fault list. The assumption sets were fixed
   before any fault run, but their author knew the algorithms. Part of the effect may be that knowledge.
2. **Ten variants, 45 dependent pairs, three toy linear plants.**
3. **The fault list was chosen, not sampled from field data.**
4. **The lineage scale is coarse**: four distinct values. A finer lineage measure might behave differently.

## Why it matters for Taxonomy
Rule R5 already requires every tool to state its hypotheses. Those statements are what made the working metric computable.
The suggestion for FLASH is therefore specific: measure heterogeneity by overlap of stated assumptions, and design
variant sets to minimise it, including the assumptions every variant shares.

## Deviations from the pre-registration
- The date in `SPEC.md` and `PREREGISTRATION.md` read 11 November; the commit was made on 10 November (NZDT). Corrected.
- The partial-correlation check above was added after seeing the results and is labelled exploratory.
- No other change. No scenario, threshold, variant or assumption set was altered after the campaign ran.

## Reproduce
```
make reproduce        # regenerates RESULTS.md from the logged campaign, offline
make flash-campaign   # reruns all 1,080 scenarios (about one minute)
```
Cost: USD 0. No model was used in this experiment.
