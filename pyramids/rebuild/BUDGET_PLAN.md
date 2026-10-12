# Budget plan

No model was called. The global Claude cap is $60. Assigned caps sum to at most $55. Five dollars stay in reserve.

Mathematics, physics, chemistry, computing and medicine may escalate to Claude. The shared MeSH queue may escalate as one queue. Every other field is Qwen only.

The Qwen first-pass rate is 25 percent unsure or needs_review. That figure is the EV planning default, not a new measurement.

The widened EV re-run left 1,268 of 5,059 rows unsure, about 25 percent. The first counted pass left 1,117 of 5,060 rows unsure or needs_review, about 22 percent. This plan uses 25 percent.

Where the rules already place a node, the rate is zero. A MeSH disagreement takes the cell of its primary tree number. That number is the first in lexicographic order, which is the order NLM lists. Only a disagreement with no deciding tree number stays in the model queue.

Field maps hold 301,910 nodes. 301,910 are placed with no model. 0 remain in field model queues after the depth cap.

The one MeSH queue holds 6,071 cell disagreements. 6,071 are ruled by the primary tree number. 0 stay for a model.

3,404 of those disagreements cross medicine, biology, chemistry, mind and society, and agriculture. 3,404 of them are ruled.

Estimated Claude spend on the escalation queues is $0.00.

The six escalation queues are authorised for Claude. Their caps are zero because the rules left no row to escalate. The $55 stays unallocated until a later plan has rows to buy.

Fine nodes that keep a cell different from the capped ancestor: PH 3,141, ED 695, HI 226, BU 17, LA 13, IS 10, MA 10, LN 8, ST 5, CH 1.

| Pot | $ |
|---|---:|
| Assigned Claude caps | 0.00 |
| Unallocated headroom | 55.00 |
| Reserve | 5.00 |
| Global cap | 60.00 |

| Queue | Free | Model queue | Rate | Est. escalate | Est. $ | Mode | Cap $ |
|---|---:|---:|---:|---:|---:|---|---:|
| MA | 6,678 | 0 | 0% | 0 | 0.00 | Claude | 0.00 |
| PH | 8,586 | 0 | 0% | 0 | 0.00 | Claude | 0.00 |
| CH | 29,907 | 0 | 0% | 0 | 0.00 | Claude | 0.00 |
| CS | 2,558 | 0 | 0% | 0 | 0.00 | Claude | 0.00 |
| MD | 24,004 | 0 | 0% | 0 | 0.00 | Claude | 0.00 |
| MESH | 6,071 | 0 | 0% | 0 | 0.00 | Claude | 0.00 |
| AG | 42,524 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| AR | 1,944 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| BI | 22,294 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| BU | 3,593 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| DE | 2,758 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| EA | 4,788 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| EC | 1,231 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| ED | 5,052 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| EN | 11,297 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| HI | 78,475 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| IK | 343 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| IS | 25,427 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| LA | 4,811 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| LN | 5,515 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| MS | 3,089 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| PL | 6,126 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| PO | 353 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| RE | 1,015 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |
| ST | 9,542 | 0 | 0% | 0 | 0.00 | Qwen only | 0.00 |

Free means ruled, filed under a parent, kept as an override, or routed by a rule. The MeSH row counts disagreements ruled by the primary tree number.

Run order is mathematics, physics, chemistry, computing, medicine, the MeSH queue, then the Qwen-only fields. `scripts/run_all_fields.py` reads this plan, resumes from a state file, and stops on a cap. A dry run does not call a model.
