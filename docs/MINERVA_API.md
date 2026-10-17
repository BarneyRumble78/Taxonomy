# Minerva API

Worker `taxonomy-api`. Version string on `/v1/health`: `3.0.0-minerva.1`. This is the contract Skynet should call. Placement inside `/v1/verify` is rules-only. `options.adjudicate` is accepted and ignored.

## Routes

| Method | Path | What it does |
|---|---|---|
| GET | `/v1/health` | `ok`, version, and the verify line |
| POST | `/v1/classify` | Unchanged. Rule stage, then retrieval and a model only when `RETRIEVE=1` or `ADJUDICATE=1` |
| POST | `/v1/place` | Rules only. Same abstentions as the rule stage. No model |
| POST | `/v1/audit` | Wording flags. Status string: `experimental heuristic: flags are prompts for a person, not findings` |
| POST | `/v1/verify` | ClaimGuard. Rules only unless `VERIFY_MODEL=1` |
| GET | `/v1/fields` | 25 fields from the catalog |
| GET | `/v1/pyramids/{FIELD}` | Catalog sections, depth 0–1 |
| GET | `/v1/pyramids/{FIELD}/search?q=` | Those sections filtered by the query |
| GET | `/v1/pyramids/{FIELD}/full` | R2 or KV, else 404 plus `static_url` |

`/v1/classify` still limits `text` to 1000 characters. `/v1/verify` accepts `text` up to 4000 characters or `claim` up to 1000. The body cap is 100 KB (413). Each of `/v1/verify`, `/v1/classify` and `/v1/audit` allows 60 requests a minute per IP. The key is the IP plus the path, so the three routes have separate counters. A further request returns 429 with `Retry-After: 60`. The Worker binding is `VERIFY_LIMITER` (`namespace_id` `1001` in `wrangler.toml`). Without that binding, the same cap is kept in memory for the isolate, which is what tests and `wrangler dev` use.

## Verify

Request: `{text|claim, sources[], tool_outputs[], options}`. At most 10 sources and 10 tool outputs. The service does not fetch URLs.

Response: `version` `claimguard-0.1`, `engine` `3.0.0`, `claims[]`, `summary.worst`, `provenance`. Each claim has `placement`, `warrant_required`, `warrant_mismatch`, `certainty`, `evidence`, `checks`, `verdict`, `qualifier`, `reason`, `status`. A bound span also carries `warrant_graded` and `warrant_declared_by_caller`. The caller label is advisory. `warrant_held` is the graded warrant, unless the caller named a weaker one.

Verdict order, first match: `out_of_scope`, `contradicted`, `contested`, `overstated`, `supported`, `unverified`. The value `true` is not a verdict. `summary.worst` does not use that order. It ranks by severity: `contradicted`, `overstated`, `contested`, `unverified`, `out_of_scope`, `supported`. Support and contradiction at the same warrant strength are `contested`. A stronger contradicting span, or a contradicting span alone, is `contradicted`.

Smoke check, no sources: `Smoking causes cancer.` and `Vaccines cause autism, as proven by a 2024 Lancet study.` are `unverified (R19)`. They are not overstated. Overstated needs some evidence. `certainty.ceiling_ok` is the R19 check. It is false for an absolute claim with no evidence, or with evidence too weak for that wording.

`VERIFY_MODEL=1` plus an AI binding may propose a split and an entailment label. If `VERIFY_KEYS` is bound, the model runs only for a bearer token whose SHA-256 is stored. The label is `by: "model"` and cannot raise a verdict to supported or contradicted (R22). The Anthropic backend is not called from the Worker.

## Forecast warrant

A forecast requires **W9** (argument from a model), not W6 (comparative inference). The table lives in `engine/claim_types.json` and is the same map `engine/adjudicate.mjs` and `engine/adjudicator.py` already use. Skynet's earlier emulation used W6. Point Skynet at this table.

| Claim type | Warrant |
|---|---|
| observation | W4 |
| event | W7 |
| attribution | W7 |
| causal | W5 |
| forecast | W9 |
| intent | W8 |
| legal | W10 |

The claim type wins over the field default. A year in the sentence is an event cue, so a dated measurement can require W7. `warrant_mismatch` is true when the placed warrant and the required warrant differ. Audit does not add that flag.

## Known weaknesses

- Physics (`PH`) holds, with 33 misplaced items (geology, seismology and learning theory under gravity; network items in atomic; technology under nuclei). Count is from the catalog, commit lineage noted in the pyramid pass that moved the count from 12 to 33.
- Business (`BU`) holds, 6 misplaced. Language (`LN`) holds, 14 misplaced. Both had a Minto pass. They were not in the later rebuild of sections under a fixed key line (that series was PH, AG, IS, EA, AR).
- Environment (`EV`) is the older format: `holds` is null.
- Rules-only span matching misses paraphrases. A faithful paraphrase with no shared span comes back unverified. See `docs/CLAIMGUARD_EVAL.md`.
- Indigenous knowledge placements stay provisional. An IK claim is capped at unverified, contested, or out of scope.
- Certainty ceilings are a first draft.
- Without the `VERIFY_LIMITER` binding, the 60-per-minute cap is per isolate, not global. A deploy uses the binding in `wrangler.toml`.
- `/v1/audit` still has `border_claim`. It fires when confidence is under 0.4 or `contested_with` is non-empty. The vaccine sentence places in medicine above that floor, so the flag stays off. That is the current rule stage, not a dropped flag.
