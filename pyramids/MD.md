# MD — Medicine and the drug

Standard v2 cited, not copied. Diagnosis: audit_biology_earth_medicine.md. v1 source: twelve.txt 3009–3235. Phase 2.2 deepening: each A-cell has its own SCQA, key line and named objects with conditions.

## 1. SCQA
**Situation.** Medicine states what goes wrong in a human body or mind, how it is recognised, how it is treated, how a drug acts, and how disorders spread and are prevented in populations.
**Complication.** v1 duplicated normal function with BI and mixed the drug molecule (CH) with the drug's effect. The audit found that only half of MeSH's top-level categories had a home.
**Question.** By what single dimension can each medical claim be placed once, with normal function left to BI and the molecule left to CH?
**Answer.** By the clinical question the claim answers about a disorder: what it is, why it arises, how it is recognised, what changes its course, and how it behaves in populations.

## 2. Governing thought
Medicine is exhausted by four faces of one pyramid: objects, methods, warrants and bridges.
Its objects divide into five clinical questions: disorders, causes and mechanisms, diagnosis and prognosis, treatment and drugs, and populations and prevention.

## 3. Key line
Dimension: **the clinical question asked of a disorder.** Logic inductive. Order: the clinical sequence.
1. Disorders
2. Causes and mechanisms
3. Diagnosis and prognosis
4. Treatment and drugs
5. Populations and prevention

**MECE test.** "Type 2 diabetes is defined by HbA1c ≥ 48 mmol/mol" is A1 (a classification rule, W12). "Insulin resistance drives it" is A2. "HbA1c has sensitivity s" is A3. "Metformin lowers HbA1c" is A4. "Prevalence is rising" is A5.

## 4. Face O — Objects

### MD.O.A1 Disorders
**SCQA.** Situation. Medicine first names what is wrong. Names come from classification rules, which are conventions, but the entities they name are meant to be real. Complication. The same suffering can be cut into entities in more than one way, and thresholds move with evidence and committee decisions. Some names pick out a cause, some a mechanism, and some only a cluster of signs. Question. What is a disorder, and which kinds of claim about disorders does medicine own? Answer. Medicine owns the working definition of a disorder, the classification systems that name disorders, the diagnosis of mental disorder, and the clinical handling of clustered and co-occurring conditions. The concept of disease in general is argued in PL (uses PL.O.A4).
**Key line.** Inductive. Plural noun: kinds of disorder claim. Dimension: how the disorder is individuated. Order: from the single entity, to the system that names it, to the hardest case, to combinations. Members (4): Disease entities · Classification · Mental disorder · Syndromes and multimorbidity.

- **MD.O.A1.1 Disease entities.** A disorder is a departure from normal function that harms the person. Normal function is owned by BI (uses BI.O.A3.1). The concept itself is debated in PL; MD uses a working definition.
  - MD.O.A1.1.1 Immune disorders: autoimmunity, immunodeficiency, allergy. Normal immune function is BI (uses BI.O.A3.3).
  - MD.O.A1.1.2 Neoplasms: the clinical entity is here; the cell biology is BI.
  - MD.O.A1.1.3 A disease entity is individuated by at least one of aetiology, mechanism or clinical picture. A specialist can test which of the three a given name rests on.
  - MD.O.A1.1.4 Harm is part of the working definition. A biological variant without harm, such as a benign anatomical variant, is not a disorder here.
- **MD.O.A1.2 Classification.** Disorders are named by published systems, ICD-11 (in effect from 1 January 2022) and DSM-5-TR (2022). Classification rules are W12.
  - MD.O.A1.2.1 Diagnostic thresholds, such as HbA1c for diabetes, are conventions set by expert bodies.
  - MD.O.A1.2.2 A change in a threshold changes measured prevalence without any change in the population. Prevalence trends across a threshold change are therefore not comparable without adjustment.
  - MD.O.A1.2.3 Inter-rater reliability, usually reported as Cohen's kappa, is a property of a diagnostic category in a stated setting. It is measured in field trials, not assumed from the text of the criteria.
- **MD.O.A1.3 Mental disorder.** The diagnosis is MD; normal cognition is MS (uses MS.O.A1); the concept of mental disorder is PL (CONTESTED).
  - MD.O.A1.3.1 Categorical against dimensional models (RDoC, HiTOP) as competing classification programmes.
  - MD.O.A1.3.2 Most DSM categories are defined by symptom criteria, not by a known biological marker. A claim that a biomarker defines a psychiatric category is OPEN for most categories.
  - MD.O.A1.3.3 Comorbidity between psychiatric categories is common. Under the dimensional programme it is read as shared underlying dimensions (CONTESTED).
- **MD.O.A1.4 Syndromes and multimorbidity.** Co-occurring conditions and frailty are handled as clinical objects in their own right.
  - MD.O.A1.4.1 A syndrome is a recurring cluster of signs and symptoms whose single cause is unknown or not required. When a cause is found, the syndrome may be renamed as a disease entity (A1.1).
  - MD.O.A1.4.2 Multimorbidity, two or more chronic conditions in one person, rises with age. Trials often exclude such patients, so single-disease evidence transfers to them with stated uncertainty.

Named objects: disease entity, syndrome, ICD-11, DSM-5-TR, diagnostic threshold, inter-rater reliability (kappa; hypothesis: raters classify independently), RDoC, HiTOP, multimorbidity, frailty.

### MD.O.A2 Causes and mechanisms
**SCQA.** Situation. Every disorder invites the question why it occurs. Causes range from pathogens to genes to social conditions. Complication. Evidence for causation is often observational, causes interact, and a mechanism shown in cells may not operate in patients. Question. Which causal claims does medicine own, and what warrant does each need? Answer. Medicine owns pathogen causation, genetic causation of disease, the pathophysiology of disordered processes, and the effect of environmental and social exposures on disease. The underlying evolutionary, cellular and social processes are owned elsewhere and cited.
**Key line.** Inductive. Plural noun: kinds of cause. Dimension: where the cause originates. Order: from outside agent, to inherited make-up, to internal process, to surroundings. Members (4): Pathogens · Genetic causes · Pathophysiology · Environmental and social determinants.

- **MD.O.A2.1 Pathogens.** Germ theory holds that specific microorganisms cause specific infectious diseases. Koch's postulates are a historical heuristic, not a test for all pathogens (asymptomatic carriers and unculturable agents fail them).
  - MD.O.A2.1.1 Antimicrobial resistance: selection under drug exposure (the evolutionary mechanism is BI, uses BI.O.A4.1).
  - MD.O.A2.1.2 Molecular criteria, based on finding pathogen nucleic acid in diseased tissue, extend causal attribution to unculturable agents. Detection of nucleic acid alone does not show a viable or causal agent.
  - MD.O.A2.1.3 Host factors change the outcome of exposure to the same agent. The pathogen is necessary for an infectious disease but often not sufficient.
- **MD.O.A2.2 Genetic causes.** Monogenic disorders follow Mendelian inheritance; polygenic risk scores sum many small effects, and their predictive power varies by ancestry.
  - MD.O.A2.2.1 Penetrance, the fraction of carriers who develop the disorder, is often below one. Recurrence risks from pedigrees state the penetrance assumed.
  - MD.O.A2.2.2 A polygenic score built in one ancestry group usually predicts less well in others. Transportability across ancestries is OPEN.
  - MD.O.A2.2.3 Mendelian randomisation uses genetic variants as instruments for an exposure. Hypotheses: the variant affects the exposure, has no path to the outcome except through it, and shares no confounder with the outcome.
- **MD.O.A2.3 Pathophysiology.** Medicine owns the mechanism of a disordered process, such as atherosclerosis or insulin resistance. The normal process it departs from is BI.
  - MD.O.A2.3.1 A mechanism shown in cells or animals is a hypothesis about patients until shown in human data. Failure to transfer is a known defeater.
  - MD.O.A2.3.2 Many chronic disorders arise from several interacting mechanisms. A single-mechanism account of Alzheimer's disease, such as the amyloid hypothesis, is CONTESTED.
- **MD.O.A2.4 Environmental and social determinants.** Exposures such as tobacco and air pollution, and deprivation, change disease risk. The social structure is MS (uses MS.O.A5); the exposure source is EV.
  - MD.O.A2.4.1 The link between smoking and lung cancer is a model case of causal inference from observational data. It rests on consistency, strength, dose–response and temporality across many studies.
  - MD.O.A2.4.2 Socioeconomic gradients in health hold across many conditions. The size of the gradient is stated for a named population and measure of deprivation.
  - MD.O.A2.4.3 Exposure–response functions for air pollutants are estimated in named cohorts. Extrapolation below the lowest observed level is a stated assumption.

Named objects: germ theory, Koch's postulates (hypotheses: agent isolable and culturable; one agent per disease; a susceptible host can be tested), antimicrobial resistance, penetrance, polygenic risk score, Mendelian randomisation (hypotheses in A2.2.3), atherosclerosis, insulin resistance, amyloid hypothesis, social gradient, exposure–response function, Bradford Hill viewpoints (guides, not tests).

### MD.O.A3 Diagnosis and prognosis
**SCQA.** Situation. Before treating, a clinician must recognise the disorder and estimate its course. Complication. Tests are imperfect, and their value depends on who is tested. Prognostic models built in one place often fail elsewhere. Question. Which claims about recognising a disorder and forecasting its course does medicine own? Answer. Medicine owns the use of signs and tests, the accuracy of tests in populations, prognosis and its models, and tests applied to people without symptoms. The mathematics of probability is owned by MA.O.A5.
**Key line.** Inductive. Plural noun: kinds of recognition and forecast. Dimension: what the clinician learns from the information. Order: gather, weigh, forecast, then extend to the well. Members (4): Signs, symptoms and tests · Test accuracy · Prognosis · Screening tests.

- **MD.O.A3.1 Signs, symptoms and tests.** Clinical examination, imaging and laboratory tests are the sources of diagnostic information.
  - MD.O.A3.1.1 History taking supplies much of the information used in many primary-care diagnoses. The proportion varies by setting and is stated per study (UNVERIFIED as a general figure).
  - MD.O.A3.1.2 Laboratory reference intervals are usually the central 95 per cent of a healthy reference population. By construction about one healthy person in twenty falls outside a single interval.
- **MD.O.A3.2 Test accuracy.** Sensitivity and specificity describe a test against a reference standard. Predictive values depend on prevalence (Bayes' theorem, owned by MA.O.A5).
  - MD.O.A3.2.1 Likelihood ratios combine with pre-test odds to give post-test odds, assuming test independence.
  - MD.O.A3.2.2 A receiver operating characteristic curve shows sensitivity against one minus specificity across cut-offs. Choosing a cut-off is a decision about the cost of each error, not a property of the test.
  - MD.O.A3.2.3 Spectrum bias arises when accuracy is measured in very sick cases and healthy controls. Such studies overstate accuracy in practice populations.
- **MD.O.A3.3 Prognosis.** Survival, course and prognostic models are stated for a named population. A model's calibration and discrimination are stated in that population.
  - MD.O.A3.3.1 The Kaplan–Meier estimator gives survival over time. Hypothesis: censoring is unrelated to outcome.
  - MD.O.A3.3.2 A model with good discrimination can be poorly calibrated in a new setting. External validation and recalibration are needed before local use.
  - MD.O.A3.3.3 Cancer staging, such as TNM, is a prognostic classification. Its rules are W12; its prognostic value is an empirical claim here.
- **MD.O.A3.4 Screening tests.** Testing people without symptoms is a diagnostic act. The programme decision is A5.3.
  - MD.O.A3.4.1 At low prevalence, even a highly specific test yields many false positives relative to true positives. This follows from Bayes' theorem (uses MA.O.A5).
  - MD.O.A3.4.2 Overdiagnosis is the detection of disease that would never have caused harm. It is estimated from excess incidence in screened groups, under stated assumptions about lead time.

Named objects: sensitivity, specificity, predictive value, likelihood ratio (hypothesis: conditional independence of tests), ROC curve (hypothesis: reference standard classifies all participants), reference interval, Kaplan–Meier estimator (hypothesis: non-informative censoring), TNM staging, calibration, discrimination, overdiagnosis, STARD.

### MD.O.A4 Treatment and drugs
**SCQA.** Situation. Medicine aims to change the course of a disorder. Drugs, procedures and therapies are tested in trials, approved by regulators and monitored after approval. Complication. Effects measured in trials may not hold for the patient in front of the clinician. Surrogate endpoints can mislead, and harms appear late. Question. Which claims about treatment effect and safety does medicine own? Answer. Medicine owns drug action in patients, procedural and psychological treatments, drug safety, and the evidential stages of drug development. The molecule is CH and the legal authority is LA.
**Key line.** Inductive. Plural noun: kinds of intervention claim. Dimension: the means of intervention and its evidential stage. Order: drug action, physical procedure, talking and rehabilitative therapy, then harms and the pathway to approval. Members (5): Pharmacology · Surgery and procedures · Psychological and rehabilitative therapy · Drug safety · Drug development and regulation.

- **MD.O.A4.1 Pharmacology.** Pharmacokinetics covers absorption, distribution, metabolism and excretion. Pharmacodynamics covers dose–response. The molecule is CH (uses CH.O.A3).
  - MD.O.A4.1.1 First-order elimination: half-life t½ = ln 2 / k, for linear kinetics.
  - MD.O.A4.1.2 Therapeutic index as the ratio of toxic to effective dose.
  - MD.O.A4.1.3 Pharmacogenomics: genotype-dependent drug response.
  - MD.O.A4.1.4 The Hill dose–response model fits effect as a saturating function of concentration. Hypotheses: reversible binding at equilibrium and one receptor population.
- **MD.O.A4.2 Surgery and procedures.** Operations and procedures change anatomy or physiology by physical means. Their effects are claims of the same kind as drug effects.
  - MD.O.A4.2.1 Surgical outcomes depend on operator and centre volume for many procedures. The volume–outcome relation is stated per procedure.
  - MD.O.A4.2.2 Sham-controlled trials are possible for some procedures. Where they exist, they can show smaller effects than unblinded comparisons.
- **MD.O.A4.3 Psychological and rehabilitative therapy.** Cognitive behavioural therapy and physiotherapy are treatments tested like others. The mental mechanism is MS.
  - MD.O.A4.3.1 Blinding of patients is rarely possible in psychological therapy. Expectancy effects are a stated defeater for effect sizes.
  - MD.O.A4.3.2 Rehabilitation outcomes are measured as function and participation, not only as disease markers. The measure is named with the claim.
- **MD.O.A4.4 Drug safety.** Adverse effects are identified before and after approval. Pharmacovigilance continues after approval.
  - MD.O.A4.4.1 Residues of veterinary drugs in human food: the safety limit is MD; the animal treatment is AG.
  - MD.O.A4.4.2 Rare adverse effects are often undetectable in pre-approval trials. By the rule of three, zero events in n patients gives an approximate 95 per cent upper bound of 3/n (uses MA.O.A5).
  - MD.O.A4.4.3 Spontaneous reporting systems detect signals, not rates. A signal needs a comparative study before a causal claim.
- **MD.O.A4.5 Drug development and regulation.** Trials run in phases I–IV; approval comes from bodies such as Medsafe (NZ), the FDA and EMA. The legal authority is LA.
  - MD.O.A4.5.1 Phase I establishes safety and dose, phase II early efficacy, phase III confirmatory efficacy, and phase IV post-approval effects.
  - MD.O.A4.5.2 Effects on a surrogate endpoint do not guarantee effects on patient outcomes. Antiarrhythmic drugs that suppressed arrhythmia yet raised mortality are a known case (CAST).
  - MD.O.A4.5.3 The randomised controlled trial estimates the average effect of a treatment. Hypotheses: random concealed allocation, adequate power and intention-to-treat analysis.

Named objects: pharmacokinetics, pharmacodynamics, half-life (hypothesis: first-order kinetics), therapeutic index, Hill model (hypotheses in A4.1.4), pharmacogenomics, sham control, pharmacovigilance, rule of three (hypothesis: independent patients, zero events), surrogate endpoint, trial phases, randomised controlled trial (hypotheses in A4.5.3), number needed to treat (hypothesis: baseline risk matches the patient group), CONSORT.

### MD.O.A5 Populations and prevention
**SCQA.** Situation. Disorders occur in populations, and many are prevented rather than treated. Complication. Population claims rest on surveillance and study design, and an average effect may not hold for subgroups. Transmission models depend on contact assumptions that rarely hold exactly. Question. Which claims about disorders in populations and their prevention does medicine own? Answer. Medicine owns the measurement of disease frequency, the dynamics of transmission, the effect of prevention and screening programmes, the performance of health systems, and the health of named populations. Price, law and policy are owned elsewhere.
**Key line.** Inductive. Plural noun: kinds of population claim. Dimension: what is measured or changed at population level. Order: measure, spread, prevent, deliver, then distribute. Members (5): Epidemiology · Transmission · Prevention and screening programmes · Health systems · Global and Māori health.

- **MD.O.A5.1 Epidemiology.** Disease frequency is measured as incidence and prevalence; association as relative and absolute risk.
  - MD.O.A5.1.1 Prevalence approximates incidence times mean duration in a steady state with low prevalence. The approximation fails when either assumption fails.
  - MD.O.A5.1.2 Relative risk alone does not convey benefit. The same relative risk reduction gives a smaller absolute reduction at lower baseline risk.
  - MD.O.A5.1.3 Direct age standardisation compares rates across populations of different age structure. Hypothesis: a chosen standard population and stable age-specific rates.
- **MD.O.A5.2 Transmission.** R0 holds for a fully susceptible population under a stated contact model. The herd-immunity threshold 1 − 1/R0 assumes homogeneous mixing.
  - MD.O.A5.2.1 The SIR compartmental model describes susceptible, infected and recovered fractions. Hypotheses: homogeneous mixing, fixed rates and lasting immunity (uses MA.O.A4).
  - MD.O.A5.2.2 The effective reproduction number Rt falls as immunity rises and contacts change. An epidemic declines while Rt stays below one.
  - MD.O.A5.2.3 Heterogeneous contact can lower the herd-immunity threshold below 1 − 1/R0. The size of the reduction depends on the contact structure assumed.
- **MD.O.A5.3 Prevention and screening programmes.** Vaccines and screening prevent disease or its harm at population level. Lead-time and length bias are stated defeaters for screening benefit.
  - MD.O.A5.3.1 Vaccine efficacy is measured in trials; vaccine effectiveness is measured in routine use. The two can differ through population, strain and waning.
  - MD.O.A5.3.2 Screening benefit is shown by reduced disease-specific or all-cause mortality in a randomised comparison. Longer survival from diagnosis alone does not show benefit.
  - MD.O.A5.3.3 Programme criteria, such as those of Wilson and Jungner, are guides to whether screening is worthwhile. They are judgements, not tests.
- **MD.O.A5.4 Health systems.** Medicine owns claims about delivery, access and quality of care. Price and finance are EC; law is LA; policy is PO.
  - MD.O.A5.4.1 The Donabedian framework assesses quality by structure, process and outcome. Hypothesis: the process measured is linked to the outcome.
  - MD.O.A5.4.2 Comparisons of providers need risk adjustment for patient mix. Small case numbers make rankings unstable.
- **MD.O.A5.5 Global and Māori health.** Health inequities by population. Under the two-mode rule, the tradition-internal side of rongoā and hauora is IK. Its clinical efficacy for a named condition is MD under W3.
  - MD.O.A5.5.1 Inequity is stated as an absolute and a relative gap in a named measure, such as life expectancy or a disease rate. The two can move in opposite directions.
  - MD.O.A5.5.2 Differences in access, quality and outcome of care between population groups are measured with risk adjustment. Unadjusted gaps mix need with quality of care.

Named objects: incidence, prevalence, relative risk, absolute risk, age standardisation, R0, Rt, herd-immunity threshold (hypothesis: homogeneous mixing), SIR model (hypotheses in A5.2.1), vaccine efficacy, vaccine effectiveness, lead-time bias, length bias, Wilson–Jungner criteria, Donabedian framework, risk adjustment.

## 5. Face M — Methods

| ID | Role | Shared role | Example |
|---|---|---|---|
| MD.M.1 | Classify | M1 Represent | ICD coding, case definitions |
| MD.M.2 | Examine | M3 Observe | history, examination, imaging |
| MD.M.3 | Trial | M4 Intervene | randomised controlled trial |
| MD.M.4 | Study populations | M3 Observe | cohort, case–control, surveillance |
| MD.M.5 | Synthesise evidence | M6 Compare and reconstruct | systematic review, meta-analysis (GRADE) |

Examples. MD.M.1: coding a death certificate to an ICD-11 cause. MD.M.2: auscultation finding a heart murmur, followed by echocardiography. MD.M.3: a placebo-controlled trial of a statin with cardiovascular events as the endpoint. MD.M.4: a case–control study of an exposure in a rare cancer. MD.M.5: a Cochrane-style review pooling trials with a random-effects model, graded by GRADE.

### Heuristics register (outside the count)
- Common things are common
- Occam's razor in diagnosis, with Hickam's dictum against it
- Red-flag checklists
- Clinical judgement
- First, do no harm
- Bradford Hill viewpoints (guides to causal judgement, not tests)

## 6. Face W — Warrants

| Cell | Warrant | Standard | Defeaters |
|---|---|---|---|
| MD.O.A1 | W12 + W4 | criteria met; inter-rater reliability shown | low reliability; shifting thresholds |
| MD.O.A2 | W5 + W3 | causal identification (Mendelian randomisation, natural experiments); mechanism shown | confounding, reverse causation |
| MD.O.A3 | W4 | accuracy study against a reference standard (STARD) | spectrum bias, verification bias |
| MD.O.A4 | W3 | pre-registered, adequately powered RCT (CONSORT); post-marketing surveillance | surrogate endpoints, publication bias, short follow-up |
| MD.O.A5 | W5 + W4 | population data with causal design | ecological fallacy, surveillance artefact |

Examples. A1: a new psychiatric category is defeated if field-trial kappa is low. A2: an observational link between an exposure and disease is weakened if Mendelian randomisation finds no effect. A3: a biomarker validated only in hospital cases may fail in primary care (spectrum bias). A4: a drug that improves a laboratory marker may not reduce deaths (surrogate endpoint). A5: a rise in recorded cases after a new test is introduced may be a surveillance artefact.

## 7. Face B — Bridges

| ID | Field | Cells | Methods | Substrate |
|---|---|---|---|---|
| MD.B.C1 | Internal medicine and specialties | A1–A4 | M.2, M.3 | adult patients |
| MD.B.C2 | Surgery | A4.2 | M.2, M.3 | operable disorders |
| MD.B.C3 | Psychiatry | A1.3, A4.3 | M.2, M.3 | mental disorders |
| MD.B.C4 | Pathology and laboratory medicine | A2, A3 | M.2 | tissue, samples |
| MD.B.C5 | Clinical pharmacology | A4.1, A4.4, A4.5 | M.3 | drugs |
| MD.B.C6 | Epidemiology and public health | A5 | M.4, M.5 | populations |
| MD.B.C7 | Nursing, midwifery and allied health | A4.3, A5.4 | M.2 | care |
| MD.B.C8 | Paediatrics and obstetrics | A1–A4 | all | children, pregnancy |
| MD.B.C9 | Dentistry and ophthalmology | A1–A4 | M.2, M.3 | teeth, eyes |

Examples. C1: cardiology applies A3 risk scores and A4 trials to adult heart disease. C3: psychiatry uses DSM-5-TR criteria (A1.3) and trials of psychological therapy (A4.3). C4: histopathology supplies the reference standard for many A3 accuracy studies. C5: clinical pharmacology sets dosing from A4.1 kinetics. C6: public health runs A5.3 screening and vaccination programmes.

## 8. Assignment rules
1. Normal function is BI; the disorder is MD.
2. The molecule is CH; its action in a patient is MD.
3. A cost-effectiveness claim is EC; the effect size it uses is MD.
4. Consent, liability and regulatory authority are LA. The ethics argument is PL.
5. An animal disorder is AG; a zoonosis's human side is MD.
6. A diagnostic test's mathematics is MA; its accuracy in a population is MD.
7. Rongoā and hauora: tradition-internal claims are IK; efficacy for a named condition is MD under W3.

## 9. Scope boundary

| Refused | Owner |
|---|---|
| normal physiology and immunology | BI |
| drug synthesis and structure | CH |
| health economics | EC |
| medical law and regulation | LA |
| bioethics argument | PL |
| veterinary medicine | AG |
| normal cognition | MS |

## 10. External crosswalk
**MeSH** has 16 top-level categories (A–N, V, Z).
- **Land (5):** C Diseases → A1; D Chemicals and drugs → A4.1; E Techniques → Face M and A3–A4; F Psychiatry and psychology → A1.3, A4.3; N Health care → A5.4.
- **Refused (11):**
  - A Anatomy → BI
  - B Organisms → BI
  - G Phenomena and processes → BI, CH
  - H Disciplines → bridges
  - I Anthropology, education, sociology → MS, ED
  - J Technology, industry, agriculture → EN, AG
  - K Humanities → AR, HI
  - L Information science → IS
  - M Named groups → substrate
  - V Publication characteristics → not a claim
  - Z Geographicals → substrate

Coverage: 5 of 16 land.

**ICD-11** (in effect from 1 January 2022) has chapters 1–26; chapter 26 is the supplementary chapter on traditional medicine conditions. Section V (functioning) and section X (extension codes) are not chapters.
- All disorder chapters land in A1.2.
- Chapter 26 lands in A1.2 with a CONTESTED flag.
- V and X are refused as cells. Functioning goes to A5.4 and A3; extension codes are W12 conventions.

**ANZSRC 32** (16 groups) and **42** (9 groups) (checked 9 Oct 2026, ABS anzsrc2020_for.xlsx):
- 32: 3201–3215 clinical and biomedical groups land in A1–A4. 3204 Immunology, 3208 Medical physiology and 3209 Neurosciences split with BI and MS. 3210 Nutrition and dietetics splits with AG. 3299 Other is not a cell.
- 42: 4202 Epidemiology and 4206 Public health → A5. 4203 Health services and systems → A5.4. 4201 Allied health, 4204 Midwifery and 4205 Nursing → B.C7. 4207 Sports science → BI and MS. 4208 Traditional, complementary and integrative medicine → A4 under W3, CONTESTED. 4299 Other is not a cell.
- Coverage: 23 of 23 substantive groups land, wholly or in part.

## 11. Validation
Sizes: key line 5. Face O 5 cells + 22 sub-cells = 27. Third-level cells: 10 from Phase 2.2 + 50 added in this deepening = 60. M roles 5. Heuristics 6, outside the count. W rows 5. B bridges 9.
Key line, word for word: Disorders. Causes and mechanisms. Diagnosis and prognosis. Treatment and drugs. Populations and prevention.
CONTESTED: the concept of mental disorder (MD vs PL vs MS); categorical vs dimensional classification; comorbidity as shared dimensions (A1.3.3); the amyloid hypothesis (A2.3.2); traditional medicine in ICD-11 chapter 26 and ANZSRC 4208.
OPEN: mechanisms of many chronic diseases (e.g. Alzheimer's disease); the transportability of polygenic scores across ancestries (A2.2.2); biomarker definition of psychiatric categories (A1.3.2).
UNVERIFIED: the share of primary-care diagnoses made from history alone (A3.1.1).

## 12. Registry rows

| ID | Label | Home | Uses |
|---|---|---|---|
| MD.O.A1 | Disorders | O/A1 | — |
| MD.O.A1.1 | Disease entities | O/A1 | BI, PL |
| MD.O.A1.1.1 | Immune disorders | O/A1 | BI |
| MD.O.A1.1.2 | Neoplasms | O/A1 | BI |
| MD.O.A1.1.3 | A disease entity is individuated by at least one of aetiology | O/A1 | — |
| MD.O.A1.1.4 | Harm is part of the working definition | O/A1 | — |
| MD.O.A1.2 | Classification | O/A1 | — |
| MD.O.A1.2.1 | Diagnostic thresholds, such as HbA1c for diabetes, are conventions set | O/A1 | — |
| MD.O.A1.2.2 | A change in a threshold changes measured prevalence without any | O/A1 | — |
| MD.O.A1.2.3 | Inter-rater reliability, usually reported as Cohen's kappa, is a | O/A1 | — |
| MD.O.A1.3 | Mental disorder | O/A1 | MS, PL |
| MD.O.A1.3.1 | Categorical against dimensional models (RDoC, HiTOP) as competing clas | O/A1 | — |
| MD.O.A1.3.2 | Most DSM categories are defined by symptom criteria, not by a known | O/A1 | — |
| MD.O.A1.3.3 | Comorbidity between psychiatric categories is common | O/A1 | — |
| MD.O.A1.4 | Syndromes and multimorbidity | O/A1 | — |
| MD.O.A1.4.1 | A syndrome is a recurring cluster of signs and symptoms whose | O/A1 | — |
| MD.O.A1.4.2 | Multimorbidity, two or more chronic conditions in one person, rises | O/A1 | — |
| MD.O.A2 | Causes and mechanisms | O/A2 | — |
| MD.O.A2.1 | Pathogens | O/A2 | — |
| MD.O.A2.1.1 | Antimicrobial resistance | O/A2 | BI |
| MD.O.A2.1.2 | Molecular criteria, based on finding pathogen nucleic acid in | O/A2 | — |
| MD.O.A2.1.3 | Host factors change the outcome of exposure to the same agent | O/A2 | — |
| MD.O.A2.2 | Genetic causes | O/A2 | — |
| MD.O.A2.2.1 | Penetrance, the fraction of carriers who develop the disorder, is | O/A2 | — |
| MD.O.A2.2.2 | A polygenic score built in one ancestry group usually predicts less | O/A2 | — |
| MD.O.A2.2.3 | Mendelian randomisation uses genetic variants as instruments for an | O/A2 | — |
| MD.O.A2.3 | Pathophysiology | O/A2 | — |
| MD.O.A2.3.1 | A mechanism shown in cells or animals is a hypothesis about | O/A2 | — |
| MD.O.A2.3.2 | Many chronic disorders arise from several interacting mechanisms | O/A2 | — |
| MD.O.A2.4 | Environmental and social determinants | O/A2 | EV, MS |
| MD.O.A2.4.1 | The link between smoking and lung cancer is a model case of causal | O/A2 | — |
| MD.O.A2.4.2 | Socioeconomic gradients in health hold across many conditions | O/A2 | — |
| MD.O.A2.4.3 | Exposure–response functions for air pollutants are estimated in | O/A2 | — |
| MD.O.A3 | Diagnosis and prognosis | O/A3 | — |
| MD.O.A3.1 | Signs, symptoms and tests | O/A3 | — |
| MD.O.A3.1.1 | History taking supplies much of the information used in many | O/A3 | — |
| MD.O.A3.1.2 | Laboratory reference intervals are usually the central 95 per cent | O/A3 | — |
| MD.O.A3.2 | Test accuracy | O/A3 | MA.O.A5 |
| MD.O.A3.2.1 | Likelihood ratios combine with pre-test odds to give post-test odds, a | O/A3 | — |
| MD.O.A3.2.2 | A receiver operating characteristic curve shows sensitivity against | O/A3 | — |
| MD.O.A3.2.3 | Spectrum bias arises when accuracy is measured in very sick cases | O/A3 | — |
| MD.O.A3.3 | Prognosis | O/A3 | — |
| MD.O.A3.3.1 | The Kaplan–Meier estimator gives survival over time | O/A3 | — |
| MD.O.A3.3.2 | A model with good discrimination can be poorly calibrated in a new | O/A3 | — |
| MD.O.A3.3.3 | Cancer staging, such as TNM, is a prognostic classification | O/A3 | — |
| MD.O.A3.4 | Screening tests | O/A3 | — |
| MD.O.A3.4.1 | At low prevalence, even a highly specific test yields many false | O/A3 | MA.O.A5 |
| MD.O.A3.4.2 | Overdiagnosis is the detection of disease that would never have | O/A3 | — |
| MD.O.A4 | Treatment and drugs | O/A4 | — |
| MD.O.A4.1 | Pharmacology | O/A4 | CH |
| MD.O.A4.1.1 | First-order elimination | O/A4 | — |
| MD.O.A4.1.2 | Therapeutic index as the ratio of toxic to effective dose. | O/A4 | — |
| MD.O.A4.1.3 | Pharmacogenomics | O/A4 | — |
| MD.O.A4.1.4 | The Hill dose–response model fits effect as a saturating function | O/A4 | — |
| MD.O.A4.2 | Surgery and procedures. | O/A4 | — |
| MD.O.A4.2.1 | Surgical outcomes depend on operator and centre volume for many | O/A4 | — |
| MD.O.A4.2.2 | Sham-controlled trials are possible for some procedures | O/A4 | — |
| MD.O.A4.3 | Psychological and rehabilitative therapy | O/A4 | MS |
| MD.O.A4.3.1 | Blinding of patients is rarely possible in psychological therapy | O/A4 | — |
| MD.O.A4.3.2 | Rehabilitation outcomes are measured as function and participation | O/A4 | — |
| MD.O.A4.4 | Drug safety | O/A4 | — |
| MD.O.A4.4.1 | Residues of veterinary drugs in human food | O/A4 | AG |
| MD.O.A4.4.2 | Rare adverse effects are often undetectable in pre-approval trials | O/A4 | MA.O.A5 |
| MD.O.A4.4.3 | Spontaneous reporting systems detect signals, not rates | O/A4 | — |
| MD.O.A4.5 | Drug development and regulation | O/A4 | LA |
| MD.O.A4.5.1 | Phase I establishes safety and dose, phase II early efficacy, phase | O/A4 | — |
| MD.O.A4.5.2 | Effects on a surrogate endpoint do not guarantee effects on patient | O/A4 | — |
| MD.O.A4.5.3 | The randomised controlled trial estimates the average effect of a | O/A4 | — |
| MD.O.A5 | Populations and prevention | O/A5 | — |
| MD.O.A5.1 | Epidemiology | O/A5 | — |
| MD.O.A5.1.1 | Prevalence approximates incidence times mean duration in a steady | O/A5 | — |
| MD.O.A5.1.2 | Relative risk alone does not convey benefit | O/A5 | — |
| MD.O.A5.1.3 | Direct age standardisation compares rates across populations of | O/A5 | — |
| MD.O.A5.2 | Transmission | O/A5 | — |
| MD.O.A5.2.1 | The SIR compartmental model describes susceptible, infected and | O/A5 | MA.O.A4 |
| MD.O.A5.2.2 | The effective reproduction number Rt falls as immunity rises and | O/A5 | — |
| MD.O.A5.2.3 | Heterogeneous contact can lower the herd-immunity threshold below 1 | O/A5 | — |
| MD.O.A5.3 | Prevention and screening programmes | O/A5 | — |
| MD.O.A5.3.1 | Vaccine efficacy is measured in trials; vaccine effectiveness is | O/A5 | — |
| MD.O.A5.3.2 | Screening benefit is shown by reduced disease-specific or all-cause | O/A5 | — |
| MD.O.A5.3.3 | Programme criteria, such as those of Wilson and Jungner, are guides | O/A5 | — |
| MD.O.A5.4 | Health systems | O/A5 | EC, LA, PO |
| MD.O.A5.4.1 | The Donabedian framework assesses quality by structure, process and | O/A5 | — |
| MD.O.A5.4.2 | Comparisons of providers need risk adjustment for patient mix | O/A5 | — |
| MD.O.A5.5 | Global and Māori health | O/A5 | IK |
| MD.O.A5.5.1 | Inequity is stated as an absolute and a relative gap in a named | O/A5 | — |
| MD.O.A5.5.2 | Differences in access, quality and outcome of care between | O/A5 | — |

## 13. Self-check against R1–R12

| Rule | Result | If FAIL: sentence and repair |
|---|---|---|
| R1 | PASS | — |
| R2 | PASS | — |
| R3 | PASS | — |
| R4 | PASS | MeSH 5 of 16; ICD-11 chapters 1–26; ANZSRC 32 and 42 23 of 23 (checked). |
| R5 | PASS | Bayes, R0, herd-immunity threshold, half-life, likelihood ratios stated with conditions. |
| R6 | PASS | — |
| R7 | PASS | — |
| R8 | PASS | — |
| R9 | PASS | Deepened in Phase 2.2. |
| R10 | PASS | — |
| R11 | FAIL (partial) | The DSM-5-TR date (2022) and ICD-11 effective date are standard but not cited here. Repair: cite WHO and APA. |
| R12 | PASS | IDs cited by BI, EA and MS kept. |
