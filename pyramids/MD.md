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
**SCQA.** Medicine first names what is wrong. Names come from classification rules (conventions), but the entities they name are meant to be real. What is a disorder, and which ones are there?
**Key line.** Disease entities, classification, mental disorder, syndromes and multimorbidity.
- **MD.O.A1.1 Disease entities.** A disorder is a departure from BI function that harms the person. The concept itself is debated in PL; MD uses a working definition.
  - MD.O.A1.1.1 Immune disorders: autoimmunity, immunodeficiency, allergy. Normal immune function is BI.
  - MD.O.A1.1.2 Neoplasms: the clinical entity is here; the cell biology is BI.
- **MD.O.A1.2 Classification.** ICD-11 (in effect from 1 January 2022) and DSM-5-TR (2022). Classification rules are W12.
  - MD.O.A1.2.1 Diagnostic thresholds, such as HbA1c for diabetes, are conventions set by expert bodies.
- **MD.O.A1.3 Mental disorder.** The diagnosis is MD; normal cognition is MS; the concept of mental disorder is PL (CONTESTED).
  - MD.O.A1.3.1 Categorical against dimensional models (RDoC, HiTOP) as competing classification programmes.
- **MD.O.A1.4 Syndromes and multimorbidity.** Co-occurring conditions; frailty.

### MD.O.A2 Causes and mechanisms
**SCQA.** Why does the disorder occur? Causes range from pathogens to genes to social conditions. Evidence for causation is often observational. What is claimed, and on what warrant?
**Key line.** Pathogens, genetic causes, pathophysiology, environmental and social determinants.
- **MD.O.A2.1 Pathogens.** Germ theory. Koch's postulates are a historical heuristic, not a test for all pathogens (asymptomatic carriers and unculturable agents fail them).
  - MD.O.A2.1.1 Antimicrobial resistance: selection under drug exposure (the evolutionary mechanism is BI).
- **MD.O.A2.2 Genetic causes.** Monogenic disorders with Mendelian inheritance; polygenic risk scores, whose predictive power varies by ancestry.
- **MD.O.A2.3 Pathophysiology.** The mechanism of a disordered process (e.g. atherosclerosis, insulin resistance).
- **MD.O.A2.4 Environmental and social determinants.** Exposures (tobacco, air pollution); deprivation. The social structure is MS; the exposure source is EV.

### MD.O.A3 Diagnosis and prognosis
**SCQA.** How is the disorder recognised, and how will it go? Tests are imperfect, and their value depends on who is tested. What is claimed?
**Key line.** Signs and tests, test accuracy, prognosis, screening tests.
- **MD.O.A3.1 Signs, symptoms and tests.** Clinical examination, imaging, laboratory tests.
- **MD.O.A3.2 Test accuracy.** Sensitivity and specificity. Predictive values depend on prevalence (Bayes' theorem, owned by MA.O.A5).
  - MD.O.A3.2.1 Likelihood ratios combine with pre-test odds to give post-test odds, assuming test independence.
- **MD.O.A3.3 Prognosis.** Survival, course, prognostic models. A model's calibration and discrimination are stated in a named population.
- **MD.O.A3.4 Screening tests.** Testing people without symptoms. The programme decision is A5.3.

### MD.O.A4 Treatment and drugs
**SCQA.** What changes the course of a disorder? Drugs, procedures and therapies are tested in trials, approved by regulators and monitored after approval. What is claimed about effect and safety?
**Key line.** Pharmacology, surgery and procedures, psychological and rehabilitative therapy, drug safety, drug development and regulation.
- **MD.O.A4.1 Pharmacology.** Pharmacokinetics: absorption, distribution, metabolism and excretion. Pharmacodynamics: dose–response. The molecule is CH.
  - MD.O.A4.1.1 First-order elimination: half-life t½ = ln 2 / k, for linear kinetics.
  - MD.O.A4.1.2 Therapeutic index as the ratio of toxic to effective dose.
  - MD.O.A4.1.3 Pharmacogenomics: genotype-dependent drug response.
- **MD.O.A4.2 Surgery and procedures.**
- **MD.O.A4.3 Psychological and rehabilitative therapy.** Cognitive behavioural therapy; physiotherapy. The mental mechanism is MS.
- **MD.O.A4.4 Drug safety.** Adverse effects; pharmacovigilance after approval.
  - MD.O.A4.4.1 Residues of veterinary drugs in human food: the safety limit is MD; the animal treatment is AG.
- **MD.O.A4.5 Drug development and regulation.** Trial phases I–IV; approval by bodies such as Medsafe (NZ), the FDA and EMA. The legal authority is LA.

### MD.O.A5 Populations and prevention
**SCQA.** Disorders occur in populations, and many are prevented rather than treated. Population claims rest on surveillance and study design. What is claimed?
**Key line.** Epidemiology, transmission, prevention and screening, health systems.
- **MD.O.A5.1 Epidemiology.** Incidence, prevalence, relative and absolute risk.
- **MD.O.A5.2 Transmission.** R0 holds for a fully susceptible population under a stated contact model. The herd-immunity threshold 1 − 1/R0 assumes homogeneous mixing.
- **MD.O.A5.3 Prevention and screening programmes.** Vaccines; screening. Lead-time and length bias are stated defeaters for screening benefit.
- **MD.O.A5.4 Health systems.** Delivery, access and quality. Price and finance are EC; law is LA; policy is PO.
- **MD.O.A5.5 Global and Māori health.** Health inequities by population. Under the two-mode rule, the tradition-internal side of rongoā and hauora is IK. Its clinical efficacy for a named condition is MD under W3.

## 5. Face M — Methods

| ID | Role | Shared role | Example |
|---|---|---|---|
| MD.M.1 | Classify | M1 Represent | ICD coding, case definitions |
| MD.M.2 | Examine | M3 Observe | history, examination, imaging |
| MD.M.3 | Trial | M4 Intervene | randomised controlled trial |
| MD.M.4 | Study populations | M3 Observe | cohort, case–control, surveillance |
| MD.M.5 | Synthesise evidence | M6 Compare and reconstruct | systematic review, meta-analysis (GRADE) |

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
Sizes: key line 5. Face O 5 cells + 22 sub-cells = 27. M roles 5. Heuristics 6, outside the count. W rows 5. B bridges 9.
Key line, word for word: Disorders. Causes and mechanisms. Diagnosis and prognosis. Treatment and drugs. Populations and prevention.
CONTESTED: the concept of mental disorder (MD vs PL vs MS); categorical vs dimensional classification; traditional medicine in ICD-11 chapter 26 and ANZSRC 4208.
OPEN: mechanisms of many chronic diseases (e.g. Alzheimer's disease); the transportability of polygenic scores across ancestries.

## 12. Registry rows

| ID | Label | Home | Uses |
|---|---|---|---|
| MD.O.A1 | Disorders | O/A1 | — |
| MD.O.A1.1 | Disease entities | O/A1 | BI, PL |
| MD.O.A1.1.1 | Immune disorders | O/A1 | BI |
| MD.O.A1.1.2 | Neoplasms | O/A1 | BI |
| MD.O.A1.2 | Classification | O/A1 | — |
| MD.O.A1.2.1 | Diagnostic thresholds, such as HbA1c for diabetes, are conventions set | O/A1 | — |
| MD.O.A1.3 | Mental disorder | O/A1 | MS, PL |
| MD.O.A1.3.1 | Categorical against dimensional models (RDoC, HiTOP) as competing clas | O/A1 | — |
| MD.O.A1.4 | Syndromes and multimorbidity | O/A1 | — |
| MD.O.A2 | Causes and mechanisms | O/A2 | — |
| MD.O.A2.1 | Pathogens | O/A2 | — |
| MD.O.A2.1.1 | Antimicrobial resistance | O/A2 | BI |
| MD.O.A2.2 | Genetic causes | O/A2 | — |
| MD.O.A2.3 | Pathophysiology | O/A2 | — |
| MD.O.A2.4 | Environmental and social determinants | O/A2 | EV, MS |
| MD.O.A3 | Diagnosis and prognosis | O/A3 | — |
| MD.O.A3.1 | Signs, symptoms and tests | O/A3 | — |
| MD.O.A3.2 | Test accuracy | O/A3 | MA.O.A5 |
| MD.O.A3.2.1 | Likelihood ratios combine with pre-test odds to give post-test odds, a | O/A3 | — |
| MD.O.A3.3 | Prognosis | O/A3 | — |
| MD.O.A3.4 | Screening tests | O/A3 | — |
| MD.O.A4 | Treatment and drugs | O/A4 | — |
| MD.O.A4.1 | Pharmacology | O/A4 | CH |
| MD.O.A4.1.1 | First-order elimination | O/A4 | — |
| MD.O.A4.1.2 | Therapeutic index as the ratio of toxic to effective dose. | O/A4 | — |
| MD.O.A4.1.3 | Pharmacogenomics | O/A4 | — |
| MD.O.A4.2 | Surgery and procedures. | O/A4 | — |
| MD.O.A4.3 | Psychological and rehabilitative therapy | O/A4 | MS |
| MD.O.A4.4 | Drug safety | O/A4 | — |
| MD.O.A4.4.1 | Residues of veterinary drugs in human food | O/A4 | AG |
| MD.O.A4.5 | Drug development and regulation | O/A4 | LA |
| MD.O.A5 | Populations and prevention | O/A5 | — |
| MD.O.A5.1 | Epidemiology | O/A5 | — |
| MD.O.A5.2 | Transmission | O/A5 | — |
| MD.O.A5.3 | Prevention and screening programmes | O/A5 | — |
| MD.O.A5.4 | Health systems | O/A5 | EC, LA, PO |
| MD.O.A5.5 | Global and Māori health | O/A5 | IK |

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
