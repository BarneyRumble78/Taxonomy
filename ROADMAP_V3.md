# Taxonomy v3: from classification to a general-purpose knowledge instrument

Goal: let a user apply the whole of knowledge, a whole field, or a distant part of a field to any problem. Talking to physics should mean talking to all of physics. Defining a problem precisely should surface methods from parts of a field nobody thought to try.

Three modes on one design:
1. **Survey:** all 25 fields as lenses.
2. **Consult:** a whole field, every subfield swept.
3. **Connect:** match a problem's structure to tools in distant subfields.

Classification stays as one operation (Check), not the purpose.

## A. Decisions to settle first
- [x] A1. Rewrite the purpose in `STANDARD_V2.md` → `STANDARD_V3.md`. Apply mode is primary; R1 (one home) applies to Check mode only.
- [ ] A2. Fix the scales: knowledge → field → subfield → topic → tool, and the depth target per field.
- [ ] A3. Choose the subfield skeleton per field (authority scheme or our own). See C.
- [ ] A4. Choose the AI backend(s) and cost limits per run (Claude API; local model optional).
- [ ] A5. Licensing for the published maps and cards (CC BY 4.0) and code (MIT).

## B. Data model
- [x] B1. **Lens card** (per field and per key-line cell), with six parts:
  - question
  - what to look for
  - how to find out (methods)
  - what settles it and what breaks it (warrants, defeaters)
  - rules of thumb
  - collisions (borders, uses, OPEN)
- [ ] B2. **Subfield node:** id, name, parent, authority code, short scope, key results.
- [x] B3. **Toolkit card** (per subfield and per major tool), with six parts:
  - problems it solves
  - problem signature
  - flagship methods and theorems, each with its hypotheses
  - inputs needed
  - outputs given
  - typical surprises and famous cross-uses
- [x] B4. **Problem signature schema**, a controlled vocabulary covering:
  - discrete or continuous
  - task: optimise, count, decide existence, assess stability, predict, infer, design, explain
  - symmetry and invariants
  - local or global
  - forward or inverse
  - deterministic or stochastic
  - linear or nonlinear
  - static or dynamic
  - scale and dimension
  - network or field structure
  - adversarial or not
  - data-rich or data-poor
  - constraint types
- [ ] B5. **Run record:** the problem, its signature, the fields and subfields consulted, findings, sources, verification status. This gives provenance for every answer.
- [ ] B6. JSON schemas for B1–B5, with validators in `scripts/check.py`.

## C. Content: the maps (depth)
- [x] C1. Mathematics: import the MSC2020 hierarchy (63 two-digit, 529 three-digit, ~6,000 five-digit) from msc2020.org, under its own licence.
- [ ] C2. Physics: PhySH disciplines and facets; ANZSRC 51 fields.
- [ ] C3. Medicine and biology: MeSH trees C, D and G; ICD-11 chapters.
- [ ] C4. Computer science: ACM CCS 2012 full tree; CS2023 knowledge units.
- [ ] C5. Economics: the JEL full tree.
- [ ] C6. Other fields: the ANZSRC 2020 six-digit fields (1,967) as the default skeleton; LCC subclasses where better.
- [ ] C7. Attach each map to its pyramid cells, with every subfield under one cell (the old R1 work, reused).
- [ ] C8. Check licences for every imported scheme before redistributing.

## D. Content: cards
- [~] D1. Convert the existing pyramids into lens cards: 25 field cards and 124 cell cards, mostly drawn from existing text.
- [~] D2. Mathematics toolkit cards for all 529 three-digit MSC classes. Draft with AI, then review.
- [ ] D3. Physics toolkit cards for each PhySH discipline, then deeper.
- [ ] D4. Toolkit cards for the remaining fields, at their first two levels.
- [ ] D5. Famous cross-connection catalogue, a seed set of 100 or more. Each entry gives problem, source field, tool field and date. Examples:
  - compressed sensing
  - persistent homology
  - optimal transport in ML
  - sphere packing and codes
  - Fourier methods in number theory
  - game theory in biology
- [ ] D6. Expert review: one reviewer per field for its cards; Māori-led review for IK (unchanged).
- [ ] D7. Mark every card's verification status, and record sources and dates.

## E. Engine (apply, consult, connect)
- [ ] E1. **Framer:** turns a user's input into a precise problem statement, its SCQA and its signature. Asks clarifying questions when the input is vague.
- [ ] E2. **Router:** picks the relevant fields (Survey) or subfields (Consult). The keyword engine is a fast first pass; the AI makes the final choice; coverage rules prevent skipping.
- [ ] E3. **Sweeper:** sends the framed problem to every selected node in parallel, each with its card as context. It returns applicability, approach, known results and conditions.
- [ ] E4. **Deepener:** expands the top nodes to their children, recursively, to a set depth and budget.
- [~] E5. **Matcher:** scores signature against toolkit cards across the whole field; similarity on signature features plus embeddings; returns distant candidates with an explanation of the mapping.
- [ ] E6. **Hypothesis checker:** for each proposed tool, lists the conditions and whether the problem meets them (yes / no / unknown).
- [ ] E7. **Synthesiser:** builds the Minto output (governing answer, key line of routes, evidence for each) and ranks routes by promise, cost and certainty.
- [ ] E8. **Verifier:** literature search for each route, a suggested small test, and OPEN/CONTESTED flags.
- [ ] E9. **Zoom operations:** Steve Andreas's moves (example of, examples, part of, parts), over the maps.
- [ ] E10. Keep the Check operation (the current classifier) as a module.
- [ ] E11. Budgets and caching: cap cost per run; cache card prompts; stream partial results.
- [ ] E12. Safety: prompt-injection guards on retrieved text; no route marked "verified" without a source.

## F. Interfaces
- [ ] F1. Python library and CLI: `taxonomy survey|consult|connect|check "…" [--field PH] [--depth 2]`.
- [ ] F2. **API:** `/survey`, `/consult/{field}`, `/connect`, `/check`, `/cards/{id}`, `/maps/{field}`; with keys, rate limits and an OpenAPI page.
- [ ] F3. MCP server exposing the same tools, so it works inside Claude, Claude Code and other assistants.
- [ ] F4. Claude skill: "apply Taxonomy" with the procedures, for use without the API.
- [ ] F5. RAG pack: a compact lens and card bundle (15–25k words per scale) to upload alongside a user's material.
- [ ] F6. Website: the existing tool tabs become Survey, Consult a field, Connect, Check, plus a run viewer showing routes, sources and verification.
- [ ] F7. Export results to report formats: brief, research plan, design requirements.

## G. Testing and evaluation
- [ ] G1. Schema and consistency tests for all maps and cards (CI).
- [ ] G2. **Retrodiction benchmark:** 50 or more historical problems, stated as they were before their cross-field solution. Measure whether Connect ranks the real solution in its top 5, and keep the answers hidden from the prompts.
- [ ] G3. **Coverage test:** for known multi-route problems, measure how many of the known routes Consult finds.
- [ ] G4. **Blind usefulness study:** real tasks with and without the tool, judged by experts.
- [ ] G5. Error log: wrong connections and failed hypotheses, fed back into the cards.
- [ ] G6. Keep the claim-classification reliability study for the Check mode only.

## H. Pilots
- [ ] H1. **Ask Mathematics prototype:** MSC map, 529 toolkit cards, Consult and Connect, 10 retrodiction cases, and one live problem from the owner.
- [ ] H2. Ask Physics.
- [ ] H3. A Survey run on a real design (sunglasses), a policy question and a strategy question.
- [ ] H4. Write up results; update the website and marketing claims only with what the tests show.

## I. Infrastructure
- [ ] I1. Repo restructure: `maps/`, `cards/lens/`, `cards/toolkit/`, `signatures/`, `engine/v3/`, `api/`, `mcp/`, `bench/`.
- [ ] I2. CI on GitHub Actions: checks, tests, benchmark smoke run.
- [ ] I3. Hosting for the API (small server or serverless), plus secrets management for model keys.
- [ ] I4. Versioning: semantic versions for the standard, maps and cards; changelog; Zenodo DOI per release.

## J. Order of work (suggested)
1. A1–A4, B1–B6 (one session)
2. C1, D1, D2 (mathematics first)
3. E1–E8 minimal, F1, G2 small, H1 (Ask Mathematics working end to end)
4. F3 MCP and F2 API
5. C2, D3, H2 (physics)
6. The remaining fields, F6 website, G4 study, H3–H4

## Progress log
- 2026-10-11: Standard v3 draft; schemas for lens card, map node, toolkit card, run record; signature vocabulary (14 facets).
- MSC2020 map imported: 63 / 534 / 6,006 nodes, each attached to a Taxonomy cell. The licence is CC BY-NC-SA, so commercial use needs permission.
- 149 draft lens cards: 143 parsed from pyramids plus 6 written for MA.
- 63 draft toolkit cards (two-digit MSC, 109 tools with hypotheses).
- Minimal Connect matcher and 5 seed retrodiction cases. These cases are not independent (same author wrote cards and cases), so they are smoke tests only.
- Next: B6 validators for lens and toolkit cards; E1 framer (AI); D2 three-digit cards; E3/E7 sweep and synthesis.
