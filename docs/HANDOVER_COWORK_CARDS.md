# Handover: complete the knowledge content of Taxonomy v4

**For:** Claude Cowork
**From:** Chris Townsend (owner), prepared with Claude Code on 11 November 2026
**Repo:** `github.com/BarneyRumble78/Taxonomy`, branch `v4-generative` (start from its tip; `307cab9` or later)

Read this whole document first. Then read `CLAUDE.md`, `docs/ROSETTA_DESIGN.md`, `docs/PLAN_V4.md`,
`standard/STANDARD_V2.md` and `standard/STANDARD_V3.md`.

---

## 1. The job in one paragraph

Taxonomy has the structure for 25 fields but little of the content that makes it generative.
Four pieces of content are missing. Your job is to produce them as validated drafts, in this order:
register mathematics, toolkit cards for all 25 fields, mathematics cards at three-digit depth, and formal cores at scale.
Everything you produce is a **draft for review**. Nothing you write becomes "reviewed" or "verified" by your own say-so.

## 2. Ground rules (hard; ask Chris before departing from any)

1. **Never merge to `main`, never deploy.** `main` auto-deploys to taxonomy.co.nz. Work on a branch cut from `v4-generative`
   (suggested `v4-content`) and open a pull request into `v4-generative`. Chris merges.
2. **Spend nothing.** No paid API keys, no `TAXONOMY_LLM=anthropic`, no `TAXONOMY_ADJUDICATE_PAID=1`. See section 4 for the two free routes.
3. **No secrets** in files, commits, chat or logs.
4. **Failures must look like failures.** Never write an empty card or a placeholder in place of an error. Log what failed.
5. **No invented anything.** No invented citations, theorems, dates or results. If you are not confident a tool or its hypotheses are right, leave it out.
   Mark unchecked facts `(UNVERIFIED)`.
6. **Benchmark hygiene.** Never open `bench/retrodiction_answers.json` or `bench/cross_connections.json`. Never use them, or the
   problem list, as a source of card or core ideas.
7. **Do not touch the pre-registered experiment.** Leave `flash_demo/variants.py`, `faults.py`, `plants.py`, `campaign.py`,
   `SPEC.md`, `PREREGISTRATION.md` and `results/campaign.csv` exactly as they are. See task 0.
8. **Standard rules hold.** R12 stable IDs: never renumber or reuse; retire instead. MA is the apex and owns every theorem.
   R5: every tool states its hypotheses. Do not restructure MA's five cells or its 63/63 MSC placement.
9. **Indigenous knowledge stays provisional.** IK cards carry a note that placement awaits Māori-led review. IK bindings in cores
   must have `maturity: speculative`. W13 (tradition-internal authority) is never mapped onto another field.
10. **Do not edit generated files by hand:** `registry/`, `correspondences/seed_*.json`, `correspondences/rosetta_edges.json`.
11. **Register.** Plain academic prose, sentences under 25 words, NZ spelling. No promotional language.
12. **Working with Chris.** Polite and non-directive. Offer options. Flag uncertainty. Report at the end of each task.

## 3. Starting state (measured 11 November 2026)

| Layer | State |
|---|---|
| Pyramids | 25 fields. 15 are under 2,700 words. |
| Registry | 990 IDs. **Mathematics has none**: `pyramids/MA.md` has no section 12. |
| Lens cards | 149, all `draft`. One card per field has an empty `breaks` list. |
| Toolkit cards | 63, in `cards/toolkit/MA.json` only (two-digit MSC). 109 tools. All `draft`. |
| Formal cores | 12 cores, 56 bindings, 12 fields bound. All `draft`, unreviewed. |
| Correspondence edges | 188 (71 `uses`, 15 MA table, 102 derived from cores). |
| Tests | 300 pass. `scripts/check.py` passes. CI green. |

Set up: `python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt`. Then `make check` and `make test`.

## 4. How to draft: two free routes

Ask Chris which he prefers before starting. Both are free.

**Route A: local Ollama on Chris's Mac.** Works only if your session can reach `127.0.0.1:11434` on his machine.
- Models installed on 10 November: `qwen3.6:27b` (about 15 tokens a second), `qwen3.6:35b`, `qwen2.5:14b-instruct`.
- Set `TAXONOMY_MODEL=qwen3.6:27b` and `TAXONOMY_OLLAMA_TIMEOUT=900`.
- The `qwen3.6` models refuse JSON-format requests. `engine/v3/llm.py` now retries without the constraint.
- Chris keeps local AI services off unless in use. Do not install autostart services. Tell him when long runs start and end.

**Route B: you draft the cards yourself, in session.** This uses no API key. Quality should be higher than the local model.
- Set `generated_by` to your model name. Do not present these cards as model-free or reviewed.

If neither route is available, stop and tell Chris. Do not route around it.

Whichever route you use, every card and core records `generated_by`, the date, and `status: draft`.

---

## 5. Tasks

### Task 0. Protect the experiment's reproducibility (small, do first)

`make reproduce` recomputes the `lineage_full` predictor from the current cores and edges.
Adding cores would silently change a pre-registered result.

- Before adding any core or edge, run `python3 -m flash_demo.analysis` and confirm `flash_demo/RESULTS.md` is unchanged (`git diff`).
- Then freeze the four predictor matrices to `flash_demo/results/distances.json`, and make `analysis.py` read that file,
  failing loudly if it is missing. Add a test that the frozen file reproduces the committed `RESULTS.md`.
- **Done when** `make reproduce` gives an identical `RESULTS.md` after you add a dummy core in a scratch copy.

### Task 1. Register mathematics

Mathematics writes its sub-cells in short form (`- A2.5 Number and counting`) and has no registry rows.
`scripts/build_registry.py` reads a `## 12. Registry rows` table from each pyramid.

- Add a `## 12. Registry rows` section to `pyramids/MA.md`, in the same four-column format as `pyramids/PH.md`.
- Register only what MA.md already defines. Do not create new cells. Expected rows:
  - `MA.O.A1` to `MA.O.A5` and their existing sub-cells (`MA.O.A1.1` … `MA.O.A5.2`), labels copied from the headings.
  - `MA.M.B1` to `MA.M.B5`, from the table under "Side B" (Define and axiomatise, Prove, Compute, Infer from data, Model).
  - `MA.B.C1` to `MA.B.C5`.
  - Ask Chris whether the heuristics register `MA.M.H` gets a row. Other fields register one `H` row.
  - Note: `ma_short_cells()` currently recognises the A sub-cells only, not B1 to B5. One table row ("Computation ↔ everything")
    was skipped from the edge seed for that reason. After registration, rerun `python3 scripts/build_correspondences.py` and report what changed.
- **Show Chris the full row list before committing.** These IDs are permanent under R12.
- Run `python3 scripts/build_registry.py`, `make check`, `make test`. Some tests may assert the old row count of 990; update the
  expected number only where the test is plainly a count check, and say so in your report.
- `engine/v3/correspondences.py` has a helper `ma_short_cells()` that infers these IDs. Keep it working; note in the report that it is now redundant.
- `CLAUDE.md` asks for a site rebuild after any pyramid change. Run `python3 scripts/build_site.py` and report the size of the
  `site/dist` diff. If it is large, ask Chris whether to commit it on this branch.
- **Done when** MA rows appear in `registry/registry.json`, checks and tests pass, and Chris has approved the row list.

### Task 2. Toolkit cards for all 25 fields

Tool: `scripts/draft_toolkit_cards.py --field XX --level N`. It is resumable and writes `cards/toolkit/<FIELD>_L<level>.json`.

Fix these in the script first, with tests:
1. **It reads every map in `maps/<FIELD>/`.** Biology alone has 22,133 MeSH nodes. Add a `--map` option and default to the
   field's primary map from `maps/index.json`.
2. **Card IDs can collide** across schemes (`<FIELD>.TK.<code>`). Include the scheme in the ID for non-primary maps.
3. **A failed batch is skipped silently** when the model omits a node. Log every node that was requested and not returned,
   and exit non-zero if any remain after retries.
4. **Batch size.** Twelve cards at 8,000 tokens is about nine minutes a call on the local model. Use a batch of 3 or 4.
5. **Record provenance.** Add `generated_by` and `date` to each card. Extend `schemas/toolkit_card.schema.json` to allow them.

Scope:
- Level 1 of the primary map for all 24 non-mathematics fields, then level 2.
- Report node counts per field before drafting. If level 2 of any field exceeds about 300 nodes, ask Chris before running it.
- Each card: what kinds of problem the subfield solves, stated without subject matter; a signature from
  `signatures/vocabulary.json`; one to four tools, each with its hypotheses; inputs; outputs.
- Leave `cross_uses` empty unless confident. This field is the most likely place for invention.

Quality gate, per field:
- `python3 scripts/validate_cards.py` passes.
- Draw a random sample of 10 cards (fixed seed). Check each tool and its hypotheses against a named textbook or reference
  you can cite. Record the outcome in `docs/CARD_AUDIT.md` as k of n with a Wilson 95% interval. Do not fix only the sampled cards
  and then report the sample as clean.

Watch for: `engine/v3/connect.py` loads every `cards/toolkit/<FIELD>*.json`. New MA files will change Connect's rankings and may
break `tests/test_v3_connect.py`. If so, tell Chris; do not loosen the test to make it pass.

- **Done when** all 25 fields have validated level-1 cards, `docs/CARD_COVERAGE.md` shows counts per field with the share that
  have tools and hypotheses, and the audit is recorded.

### Task 3. Mathematics to three-digit depth

- `python3 scripts/draft_toolkit_cards.py --field MA --level 2` covers the 534 three-digit MSC classes in `maps/MA/msc2020.json`.
  It writes `cards/toolkit/MA_L2.json`. Leave `cards/toolkit/MA.json` (63 cards) unchanged; a test counts it.
- Mathematics owns every theorem, so R5 matters most here. A theorem without its hypotheses is an error, not a draft.
- Some classes are administrative (history, education, general reference). Give these a card with no tools and a note saying why.
- Audit a random sample of 30 cards as in task 2.
- The MSC2020 map is CC BY-NC-SA. Cards derived from it inherit that question. Note this in the coverage report; do not resolve it yourself.
- **Done when** 534 cards validate, the coverage report lists how many carry tools and hypotheses, and the audit is recorded.

### Task 4. Formal cores at scale

Read `docs/ROSETTA_DESIGN.md` and the 12 existing cores in `rosetta/cores.json` before writing any.
Schema: `schemas/formal_core.schema.json`. Validator: `rosetta.check()` in `engine/v3/rosetta.py`, run by `make check`.

What a good core is:
- **One mathematical structure**, stated in one sentence free of any field's vocabulary.
- **An MA node that exists** in the map (`ma_node`, such as `MSC:35Kxx`).
- **Named roles**, at least two.
- **Assumptions as separate checkable statements**, with ids `a1`, `a2`, …
- **A guarantee**: what follows when every assumption holds.
- **Bindings in at least three fields.** Each binding gives the field's own name for the tool, what fills every role,
  a code for every assumption (`y`, `~`, `n`, `?`), and **at least one stated break**. The validator rejects a binding with none.
- Each binding's `cell` must be a real ID owned by that field. Use the field code when no cell fits.
- `maturity`: `standard` for textbook use, `specialist` for a subfield's use, `speculative` for a proposal.

Method:
1. Use the three-digit MSC classes from task 3 as the list of candidate structures. Work through them in order.
2. Keep a candidate only if you can name real, established uses in three or more fields. Most classes will not qualify. That is expected.
3. Prefer `?` to a guess for any assumption code.
4. Record a source for each core and binding in the `sources` list where you can cite one. Leave it empty rather than invent.
5. After each batch: `python3 scripts/build_rosetta_edges.py`, `make check`, `make test`.

Target: aim for about 150 cores. Quality matters more than the count. Report the number of candidates considered and rejected.

Coverage goal: every field has at least five bindings. Thirteen fields have none today: BU, PO, PL, HI, LN, AR, RE, ED, DE, AG, EV, IK,
and MA as a target (MA is never a binding target; that is by design).

**A design question to raise with Chris, not to settle alone.** Mathematical cores serve the formal fields well and the humanities poorly.
The design proposes *method cores* (for example, triangulating independent records) and *warrant cores*. The schema requires `ma_node`
to be a mathematics node, so these do not fit yet. Draft a short proposal for a `face` field (`object`, `method`, `warrant`) and wait for his decision.
Do not force history, law or the arts into mathematical cores to raise the coverage number.

Audit: draw 20 cores at random. For each, check the structure, the guarantee and two bindings against a cited source.
Record the result in `docs/CORE_AUDIT.md` with a Wilson interval.

- **Done when** the cores validate, derived edges are regenerated, the coverage matrix (`python3 taxonomy.py rosetta matrix`)
  is in the report, and the audit is recorded.

---

## 6. Order, and what to do if time is short

Task 0, then 1, then 2 at level 1, then 3, then 4, then 2 at level 2.
If time is short, a smaller set of audited cards and cores is worth more than a complete unaudited one. Tell Chris early.

## 7. Reporting

At the end of each task, report to Chris:
- what changed, with counts;
- what failed or was skipped, and why;
- the audit result, including misses;
- anything that needs his decision.

Commit per task with a clear message. Push only your own branch. Open one pull request into `v4-generative` per task or pair of tasks.

## 8. Do not

- Do not mark any card or core `reviewed`.
- Do not claim the content is complete, verified or DARPA-grade. It will be a set of drafts with a measured error rate.
- Do not change `docs/TECHNICAL_REPORT.md`, `docs/FLASH_RFI_NOTES.md` or any title of Chris's work.
- Do not update website or marketing text.
- Do not send email or contact anyone on Chris's behalf.
- Do not deepen the pyramids themselves. That is separate work and needs Chris's direction.

## 9. Questions to ask Chris at the start (one short message)

1. Route A (local Ollama) or route B (you draft in session)?
2. Is branch name `v4-content` acceptable?
3. May the MA registry rows be exactly the cells already written in `MA.md`, with no additions?
4. Is there a ceiling on cards per field at level 2?
5. Who will review the drafts, field by field, once they exist?

## 10. Commands

```
make check                                        # conformance, edges, cores
make test                                         # 300 tests at handover
python3 scripts/build_registry.py                 # after editing section 12 of a pyramid
python3 scripts/draft_toolkit_cards.py --field PH --level 1
python3 scripts/validate_cards.py
python3 scripts/build_rosetta_edges.py            # after editing rosetta/cores.json
python3 taxonomy.py rosetta matrix                # cores by field
python3 taxonomy.py rosetta translate RC-diffusion PH EC
make reproduce                                    # must leave flash_demo/RESULTS.md unchanged
```
