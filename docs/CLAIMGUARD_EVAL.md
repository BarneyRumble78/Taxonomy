# ClaimGuard evaluation

Checked 17 October 2026. Figures below are measurements on files in this repo, or quotations from arXiv pages fetched that day. They are not launch results.

## What was not done

`pilot/heldout_verdicts.tsv` copies the 203 frozen claims and adds `evidence_text`, `verdict_gold`, `certainty_gold`, `labeller`, `date`. Gold cells are blank. `labeller` is `UNLABELLED`. The plan's 600-row set (an overstated variant and a contradicted variant, two blinded labellers, Krippendorff's alpha) is not in the repo. `pilot/heldout.tsv` is unchanged.

## Developer sample (n = 8)

`pilot/claimguard_developer_sample.tsv`. One developer, 17 October 2026, not a second coder. Rules-only `verify`.

7 of 8 rows matched the developer label. The miss is S8: a faithful paraphrase ("is not the Dirac value") was marked `contradicted` because the span matcher treats a negation at high token overlap as a contradiction. S7, a lighter paraphrase, did match and came back `supported`.

That is 7/8 on this file. It is not a precision for `supported`, and it is not the launch bar.

## Post-tool fixture

`scripts/eval_post_tool.py` reads JSON lines of tool output, answer, and label (`faithful` or `hallucinated`). It calls `verify`. Faithful should be `supported` on every claim. Hallucinated should be `contradicted` or `unverified`.

`pilot/post_tool_fixture.jsonl` has four rows. On 17 October 2026: the identical span was supported, the wrong year was contradicted, the unrelated answer was unverified, and the "is not" paraphrase (faithful) was contradicted. Faithful hit 1 of 2. Hallucinated hit 2 of 2. The ToolHACE dataset is not vendored and was not run.

## Placement floors

On the 203 frozen claims, `rule_placement`, with an abstention counted as a miss:

| | Measured 17 Oct 2026 | Floor |
|---|---|---|
| owner | 139/203 = 68.47% | 62.1% |
| cell | 102/203 = 50.25% | 48% |
| warrant | 81/203 = 39.90% | 37.9% |
| method | 95/203 = 46.80% | 42% |

`tests/test_eval_gate.py` fails if a floor is crossed. The early public baseline on the site is still 62.1% owner and 37.9% warrant. The table above is a later rule-stage measurement, not a replacement for that sentence.

## Launch targets (not results)

| Metric | Target |
|---|---|
| Precision of supported, rules-only | ≥ 0.95 |
| Precision of contradicted | ≥ 0.90 |
| Recall of overstated on overstated variants | ≥ 0.70 |
| Model-only verdicts reaching supported or contradicted | 0 |
| Post-tool recall of hallucinated claims | ≥ 0.70 at the precision above |
| Placement | no fall through the floors above |

A high unverified rate is the intended behaviour when no span is shown.

## Papers

Fetched from arXiv on 17 October 2026. Abstracts and the HTML full text only. Numbers that were not on those pages are omitted.

- ToolHACE, arXiv:2610.17125 (12 October 2026), Nikolay Ivanov and others. A span-level benchmark for hallucinations after a tool returns, with five categories: Correct, Answer Mismatch, Overgeneration, Undergeneration, Missing Tool. The adapter in `scripts/eval_post_tool.py` is the same shape of check (tool output against the answer). The dataset itself is not in this repo.
- NabaOS tool receipts, arXiv:2603.10060, Abhinaba Basu. HMAC-signed tool receipts. NyayaVerifyBench: 1,800 scenarios, four languages. The paper reports detection of 94.2% of fabricated tool references, 87.6% of count misstatements, and 91.3% of false absence claims, with under 15 ms overhead.
- TRACE, arXiv:2510.19186, Tanya Shourya, Yingfan Wang, Zhaoyi Joey Hou, Shamik Roy, Vinayshekhar Bannihatti Kumar, Rashmi Gangadharaiah. The HTML text says 566 conversations, 2,181 turns, and 26 error cases. SCOPE's overall F1 is given as 76%. On the hard case (user satisfied, agent wrong) it gives reward modelling 70% accuracy and SCOPE 32%.
- MIRAGE-Bench, arXiv:2507.21017, Weichen Zhang, Yiyou Sun, and others. Three ways an agent action can be unfaithful: to the task instructions, to the execution history, or to environment observations.
