"""Spend plan for a Qwen first pass and a small Claude escalation. No model calls.

The global cap is $60. Assigned caps sum to at most $55. Five dollars stay
in reserve. Claude is offered only to mathematics, physics, chemistry,
computing, medicine, and the one shared MeSH queue. Every other field is
Qwen only.

The unsure rate is a planning default of 25 percent, taken from the EV
first pass (unsure plus needs_review). A queue the rules already place
uses a rate of zero. MeSH disagreements take the cell of the primary tree
number before any of them are priced.
"""
import json
import math
from pathlib import Path

from cost_cap import ALLOCATION, GLOBAL_BUDGET, RESERVE, UNSURE_RATE, USD_PER_THOUSAND
from field_rebuild import FIELDS, mesh_fields, prepare, shared_queue

PRIORITY = ["MA", "PH", "CH", "CS", "MD"]
MESH = "MESH"
MESH_FOCUS = ["MD", "BI", "CH", "MS", "AG"]
CLAUDE_IDS = PRIORITY + [MESH]


def _cents(usd):
    return int(math.floor(float(usd) * 100 + 1e-6))


def _ceil_cents(usd):
    return int(math.ceil(float(usd) * 100 - 1e-9))


def estimate_escalation(model_items, rate):
    """Items a first pass is assumed to leave, and the Claude price of those items."""
    model_n = int(model_items)
    used = 0.0 if model_n == 0 else float(rate)
    escalate = int(round(model_n * used))
    usd = escalate * USD_PER_THOUSAND / 1000
    return used, escalate, usd


def _scale_caps(entries):
    """Keep Claude caps at or under the allocation. Priority receives leftover cents."""
    limit = _cents(ALLOCATION)
    raw = []
    for entry in entries:
        if entry["mode"] != "claude":
            entry["cap_cents"] = 0
            continue
        entry["cap_cents"] = _ceil_cents(entry["estimate_usd"])
        raw.append(entry)
    total = sum(entry["cap_cents"] for entry in raw)
    if total <= limit:
        return
    if total == 0:
        return
    exact = []
    for entry in raw:
        share = entry["cap_cents"] * limit / total
        entry["cap_cents"] = int(math.floor(share))
        exact.append(share - entry["cap_cents"])
    left = limit - sum(entry["cap_cents"] for entry in raw)
    order = sorted(range(len(raw)), key=lambda index: (-exact[index], CLAUDE_IDS.index(raw[index]["id"])))
    for index in order[:left]:
        raw[index]["cap_cents"] += 1


def build_plan(root):
    """One row per field, then the shared MeSH queue. Counts come from the maps."""
    root = Path(root)
    entries = []
    for field in FIELDS:
        report = prepare(field, root)
        free = report["ruled"] + report["filed"] + report["kept_override"] + report["routed"]
        rate, escalate, usd = estimate_escalation(report["model"], UNSURE_RATE)
        entries.append({
            "id": field,
            "kind": "field",
            "nodes": report["nodes"],
            "free": free,
            "ruled": report["ruled"],
            "filed": report["filed"],
            "kept_override": report["kept_override"],
            "routed": report["routed"],
            "unanchored": report["unanchored"],
            "model": report["model"],
            "unsure_rate": rate,
            "escalate_items": escalate,
            "estimate_usd": round(usd, 6),
            "depth_cap": report["depth_cap"],
        })
    owners = mesh_fields(root)
    mesh = shared_queue(owners, root, include_rows=False, focus=MESH_FOCUS)
    rate, escalate, usd = estimate_escalation(mesh["unresolved"], UNSURE_RATE)
    entries.append({
        "id": MESH,
        "kind": "mesh",
        "nodes": mesh["conflicts"],
        "free": mesh["resolved"],
        "ruled": mesh["resolved"],
        "filed": 0,
        "kept_override": 0,
        "routed": 0,
        "unanchored": 0,
        "model": mesh["unresolved"],
        "unsure_rate": rate,
        "escalate_items": escalate,
        "estimate_usd": round(usd, 6),
        "depth_cap": None,
        "descriptor_rows": mesh["descriptor_rows"],
        "tree_copies": mesh["tree_copies"],
        "conflicts": mesh["conflicts"],
        "cross_field_conflicts": mesh["cross_field_conflicts"],
        "focus_cross_conflicts": mesh["focus_cross_conflicts"],
        "focus_resolved": mesh["focus_resolved"],
        "resolved": mesh["resolved"],
        "fields": mesh["fields"],
    })
    for entry in entries:
        entry["mode"] = "claude" if entry["id"] in CLAUDE_IDS else "qwen"
    _scale_caps(entries)
    for entry in entries:
        entry["cap"] = round(entry.pop("cap_cents") / 100, 2)
    order_ids = [item for item in CLAUDE_IDS if any(entry["id"] == item for entry in entries)]
    order_ids.extend(field for field in FIELDS if field not in PRIORITY)
    by_id = {entry["id"]: entry for entry in entries}
    ordered = [by_id[item] for item in order_ids]
    assigned = round(sum(entry["cap"] for entry in ordered), 2)
    return {
        "global_cap": GLOBAL_BUDGET,
        "allocation": ALLOCATION,
        "reserve": RESERVE,
        "assigned": assigned,
        "headroom": round(ALLOCATION - assigned, 2),
        "unsure_rate": UNSURE_RATE,
        "usd_per_thousand": USD_PER_THOUSAND,
        "priority": PRIORITY,
        "claude": CLAUDE_IDS,
        "mesh_focus": MESH_FOCUS,
        "order": ordered,
        "totals": {
            "fields": len(FIELDS),
            "nodes": sum(entry["nodes"] for entry in ordered if entry["kind"] == "field"),
            "free": sum(entry["free"] for entry in ordered if entry["kind"] == "field"),
            "model": sum(entry["model"] for entry in ordered if entry["kind"] == "field"),
            "mesh_conflicts": by_id[MESH]["conflicts"],
            "mesh_resolved": by_id[MESH]["resolved"],
            "mesh_model": by_id[MESH]["model"],
            "focus_cross_conflicts": by_id[MESH]["focus_cross_conflicts"],
            "focus_resolved": by_id[MESH]["focus_resolved"],
            "estimate_usd": round(sum(entry["estimate_usd"] for entry in ordered if entry["mode"] == "claude"), 2),
            "assigned": assigned,
        },
    }


def render_markdown(plan):
    """The budget note. Figures are the dry-run counts, not a measured Qwen rate."""
    totals = plan["totals"]
    lines = [
        "# Budget plan",
        "",
        "No model was called. The global Claude cap is $60. Assigned caps sum to at most $55. Five dollars stay in reserve.",
        "",
        "Mathematics, physics, chemistry, computing and medicine may escalate to Claude. The shared MeSH queue may escalate as one queue. Every other field is Qwen only.",
        "",
        "The Qwen first-pass rate is 25 percent unsure or needs_review. That figure is the EV planning default, not a new measurement.",
        "",
        "The widened EV re-run left 1,268 of 5,059 rows unsure, about 25 percent. The first counted pass left 1,117 of 5,060 rows unsure or needs_review, about 22 percent. This plan uses 25 percent.",
        "",
        "Where the rules already place a node, the rate is zero. A MeSH disagreement takes the cell of its primary tree number. That number is the first in lexicographic order, which is the order NLM lists. Only a disagreement with no deciding tree number stays in the model queue.",
        "",
        f"Field maps hold {totals['nodes']:,} nodes. {totals['free']:,} are placed with no model. {totals['model']:,} remain in field model queues after the depth cap.",
        "",
        f"The one MeSH queue holds {totals['mesh_conflicts']:,} cell disagreements. {totals['mesh_resolved']:,} are ruled by the primary tree number. {totals['mesh_model']:,} stay for a model.",
        "",
        f"{totals['focus_cross_conflicts']:,} of those disagreements cross medicine, biology, chemistry, mind and society, and agriculture. {totals['focus_resolved']:,} of them are ruled.",
        "",
        f"Estimated Claude spend on the escalation queues is ${totals['estimate_usd']:.2f}.",
        "",
    ]
    if plan["assigned"] == 0:
        lines.extend([
            "The six escalation queues are authorised for Claude. Their caps are zero because the rules left no row to escalate. The $55 stays unallocated until a later plan has rows to buy.",
            "",
        ])
    kept = [
        entry for entry in plan["order"]
        if entry["kind"] == "field" and entry["kept_override"]
    ]
    if kept:
        kept.sort(key=lambda entry: (-entry["kept_override"], entry["id"]))
        bits = ", ".join(f"{entry['id']} {entry['kept_override']:,}" for entry in kept)
        lines.extend([
            f"Fine nodes that keep a cell different from the capped ancestor: {bits}.",
            "",
        ])
    lines.extend([
        "| Pot | $ |",
        "|---|---:|",
        f"| Assigned Claude caps | {plan['assigned']:.2f} |",
        f"| Unallocated headroom | {plan['headroom']:.2f} |",
        f"| Reserve | {plan['reserve']:.2f} |",
        f"| Global cap | {plan['global_cap']:.2f} |",
        "",
        "| Queue | Free | Model queue | Rate | Est. escalate | Est. $ | Mode | Cap $ |",
        "|---|---:|---:|---:|---:|---:|---|---:|",
    ])
    for entry in plan["order"]:
        rate = "0%" if entry["unsure_rate"] == 0 else "25%"
        mode = "Claude" if entry["mode"] == "claude" else "Qwen only"
        lines.append(
            f"| {entry['id']} | {entry['free']:,} | {entry['model']:,} | {rate} | "
            f"{entry['escalate_items']:,} | {entry['estimate_usd']:.2f} | {mode} | {entry['cap']:.2f} |"
        )
    lines.extend([
        "",
        "Free means ruled, filed under a parent, kept as an override, or routed by a rule. The MeSH row counts disagreements ruled by the primary tree number.",
        "",
        "Run order is mathematics, physics, chemistry, computing, medicine, the MeSH queue, then the Qwen-only fields. `scripts/run_all_fields.py` reads this plan, resumes from a state file, and stops on a cap. A dry run does not call a model.",
        "",
    ])
    return "\n".join(lines)


def write_plan(root, plan=None):
    root = Path(root)
    plan = plan or build_plan(root)
    folder = root / "pyramids" / "rebuild"
    folder.mkdir(parents=True, exist_ok=True)
    payload = json.loads(json.dumps(plan))
    (folder / "budget_plan.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (folder / "BUDGET_PLAN.md").write_text(render_markdown(plan), encoding="utf-8")
    return plan


def load_plan(root):
    path = Path(root) / "pyramids" / "rebuild" / "budget_plan.json"
    return json.loads(path.read_text(encoding="utf-8"))
