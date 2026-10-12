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
from minto_build import audit_field, claude_usd

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
        found = audit_field(field, root)
        literal = found["literal"]
        concept = found["concept"]
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
            "minto_in_pyramid": literal["admitted"],
            "minto_loose": literal["loose_topics"],
            "minto_oversized": literal["oversized_groups"],
            "minto_undersized": literal["undersized_groups"],
            "minto_missing_basis": literal["missing_basis"],
            "minto_missing_order": literal["missing_order"],
            "minto_template": literal["template_summaries"],
            "minto_missing_summaries": literal["missing_summaries"],
            "catalogue_filed": concept["lcc_filed"] + concept["flat_filed"],
            "admitted": concept["admitted"],
            "formation": concept["formation"],
            "summaries": concept["summaries"],
            "minto_items": concept["items"],
            "flat_files": concept["flat_files"],
            "worst": literal["worst"],
            "worst_groups": literal["worst_groups"],
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
        "minto_in_pyramid": 0,
        "minto_loose": 0,
        "minto_oversized": 0,
        "minto_undersized": 0,
        "minto_missing_basis": 0,
        "minto_missing_order": 0,
        "minto_template": 0,
        "minto_missing_summaries": 0,
        "catalogue_filed": 0,
        "admitted": 0,
        "formation": 0,
        "summaries": 0,
        "minto_items": 0,
        "flat_files": [],
        "worst": {"children": 0, "id": "", "name": ""},
        "worst_groups": [],
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
        if entry["kind"] == "field" and entry["mode"] == "claude":
            entry["estimate_usd"] = claude_usd(entry["minto_items"])
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
            "minto_items": sum(entry["minto_items"] for entry in ordered),
            "claude_items": sum(entry["minto_items"] for entry in ordered if entry["mode"] == "claude" and entry["kind"] == "field"),
            "qwen_items": sum(entry["minto_items"] for entry in ordered if entry["mode"] == "qwen"),
            "formation": sum(entry["formation"] for entry in ordered),
            "summaries": sum(entry["summaries"] for entry in ordered),
        },
    }


def _row(plan, ident):
    return next(entry for entry in plan["order"] if entry["id"] == ident)


def _count(number, one, many):
    word = one if number == 1 else many
    return f"{number:,} {word}"


def render_markdown(plan):
    """The budget note. Cell filing is reported separately from the Minto checker."""
    totals = plan["totals"]
    ma = _row(plan, "MA")
    hi = _row(plan, "HI")
    flat = sorted({name for entry in plan["order"] for name in entry.get("flat_files") or []})
    flat_text = ", ".join(flat) if flat else "none"
    lines = [
        "# Budget plan",
        "",
        "No model was called. The global Claude cap is $60. Assigned caps sum to at most $55. Five dollars stay in reserve.",
        "",
        "A cell on a source node is a filing mark. It is not a Minto group. The count of nodes that already have a cell is not a classification.",
        "",
        f"Field maps hold {totals['nodes']:,} nodes. {totals['free']:,} already have a cell, a filed parent, or a route. {totals['model']:,} remain in the cell-assignment queue. That queue is not the work below.",
        "",
        "The rebuild hangs each capped node on its cell by the source parent link. It copies basis and order only from the rule file. Source groups get the source name as their statement. `engine/v3/minto_check.py` then reads that pyramid. Environmental science passes the same checker with every count at 0.",
        "",
        f"Mathematics puts {ma['minto_in_pyramid']:,} capped nodes in the pyramid. {ma['minto_loose']:,} are loose topics under a cell. {_count(ma['minto_oversized'], 'group has', 'groups have')} more than five members. {_count(ma['minto_undersized'], 'group has', 'groups have')} fewer than two. {ma['minto_missing_basis']:,} groups lack a basis. {ma['minto_missing_order']:,} lack an order. {ma['minto_template']:,} summaries match a template. {ma['minto_missing_summaries']:,} group nodes lack a plain-definition sentence.",
        "",
        f"The largest mathematics group is {ma['worst']['name']} ({ma['worst']['id']}), with {ma['worst']['children']:,} members.",
        "",
        f"History puts {hi['minto_in_pyramid']:,} capped nodes in the pyramid. {hi['minto_loose']:,} are loose topics under a cell. {_count(hi['minto_oversized'], 'group has', 'groups have')} more than five members. {_count(hi['minto_undersized'], 'group has', 'groups have')} fewer than two. {hi['minto_missing_basis']:,} groups lack a basis. {hi['minto_missing_order']:,} lack an order. {hi['minto_template']:,} summaries match a template. {hi['minto_missing_summaries']:,} group nodes lack a plain-definition sentence.",
        "",
        f"The largest history group is {hi['worst']['name']} ({hi['worst']['id']}), with {hi['worst']['children']:,} members. The depth cap is 2, and LCC schedule lines sit at level 2, so the cap does not file them.",
        "",
        "Physics is almost the whole Claude estimate because its cap admits the PACS second level. The Gold Book is the flat index, so those chemistry terms stay in the checker table and out of the Claude count.",
        "",
        "Before any model is priced, two free rules file catalogue lines. An LCC schedule line, letters then digits, is filed under its class heading. A flat index, at least 1,000 nodes of which 90 percent are level 1, is catalogued under its cell. Flat indexes in this run: " + flat_text + ".",
        "",
        "Model work is what remains. Formation places each member of an illegal group into a group of two to five. A summary is one plain-definition sentence on a group node, not on a leaf. A group already of size two to five needs the sentence and the basis, not a new placement.",
        "",
        "This estimate does not use the 25 percent EV placement rate. There is no measured Qwen rate for forming groups. Qwen items are priced at $0. Claude items use the measured $0.90 per 1,000.",
        "",
        "Claude forms the groups and writes the sentences for mathematics, physics, chemistry, computing and medicine. Qwen does both for the other fields. The MESH queue is not a group-forming queue. Its cell disagreements are already ruled by the primary tree number.",
        "",
        f"The one MeSH queue holds {totals['mesh_conflicts']:,} cell disagreements. {totals['mesh_resolved']:,} are ruled by the primary tree number. {totals['mesh_model']:,} stay for a model. {totals['focus_cross_conflicts']:,} of those disagreements cross medicine, biology, chemistry, mind and society, and agriculture. {totals['focus_resolved']:,} of them are ruled.",
        "",
        f"Claude items are {totals['claude_items']:,}. Qwen items are {totals['qwen_items']:,}. Formation items are {totals['formation']:,}. Summary items are {totals['summaries']:,}. Estimated Claude spend is ${totals['estimate_usd']:.2f}.",
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
        "Checker on the pyramid the rebuild emits now. Catalogue filing is not applied in this table.",
        "",
        "| Field | In pyramid | Loose under cells | Oversized groups | Undersized groups | Missing basis | Missing order | Template summaries | Missing summaries |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for entry in plan["order"]:
        if entry["kind"] != "field":
            continue
        lines.append(
            f"| {entry['id']} | {entry['minto_in_pyramid']:,} | {entry['minto_loose']:,} | "
            f"{entry['minto_oversized']:,} | {entry['minto_undersized']:,} | "
            f"{entry['minto_missing_basis']:,} | {entry['minto_missing_order']:,} | "
            f"{entry['minto_template']:,} | {entry['minto_missing_summaries']:,} |"
        )
    lines.extend([
        "",
        "Model work after the two catalogue rules. A cap is Claude money. Qwen rows are local.",
        "",
        "| Field | Catalogue filed | Admitted | Formation | Summaries | Mode | Est. $ | Cap $ |",
        "|---|---:|---:|---:|---:|---|---:|---:|",
    ])
    for entry in plan["order"]:
        if entry["kind"] != "field":
            continue
        mode = "Claude" if entry["mode"] == "claude" else "Qwen only"
        lines.append(
            f"| {entry['id']} | {entry['catalogue_filed']:,} | {entry['admitted']:,} | "
            f"{entry['formation']:,} | {entry['summaries']:,} | {mode} | "
            f"{entry['estimate_usd']:.2f} | {entry['cap']:.2f} |"
        )
    lines.extend([
        "",
        "Oversized means more than five members. Undersized means fewer than two. A loose topic is a leaf whose parent is a cell. A missing summary is a group node whose statement is not a sentence of at least six words.",
        "",
        "The unallocated headroom is not a finished field. It is money not yet assigned. Qwen drafts for the other nineteen fields have no measured pass rate against this checker.",
        "",
        "`scripts/run_all_fields.py` reads this plan. A dry run does not call a model. Rows with Minto items stay pending: the cell placer is not a group former, and this run does not start one.",
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
