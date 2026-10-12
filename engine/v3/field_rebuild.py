"""Free classification rebuild for any field. No model calls.

A rule file states the scope, the organising principle, and the Minto basis
and order. Map nodes already carrying a cell keep it. Fine-grained nodes
(a level below the field cap, including shelf numbers) are filed under the
nearest ancestor at the cap. Only a top concept with no cell is a model item.

Indigenous topics follow pyramids/rebuild/ANZSRC45.json. A subject claim
leaves for its sector field. A knowledge-system claim stays with IK, and
stays provisional until Māori-led review.
"""
import json
import re
from collections import Counter
from pathlib import Path

from cost_cap import ESCALATE_STATUS, USD_PER_THOUSAND, hybrid_estimate
from minto_check import BASIS_ORDERS
from shortlist import ranked_shortlist

FIELDS = (
    "AG AR BI BU CH CS DE EA EC ED EN HI IK IS LA LN MA MD MS PH PL PO RE ST"
).split()
SHELF = re.compile(r"\d+\.\d+")
SHORTLIST_WIDTH = 12


def is_shelf(node):
    """A cutter or decimal shelf number. MSC codes such as 03B44 do not match."""
    return bool(SHELF.search(str((node or {}).get("code") or "")))


def is_fine(node, cap):
    """True when the node is below the cap, so it can be filed under a parent."""
    level = int((node or {}).get("level") or 1)
    deep = level > int(cap)
    return deep or (is_shelf(node) and deep)


def load_rule(field, root):
    path = Path(root) / "pyramids" / "rebuild" / f"{field}.json"
    rule = json.loads(path.read_text(encoding="utf-8"))
    problems = validate_rule(rule)
    if problems:
        raise ValueError(f"{field}: " + "; ".join(problems))
    return rule


def validate_rule(rule):
    """Basis and order must be a legal Minto pair. Degree needs a ranking."""
    problems = []
    key = rule.get("key_line") or {}
    basis = key.get("basis")
    order = key.get("order")
    if basis not in BASIS_ORDERS:
        problems.append(f"unknown basis {basis}")
    elif order not in BASIS_ORDERS[basis]:
        problems.append(f"order {order} does not match basis {basis}")
    if order == "degree" and not (key.get("rank_note") or "").strip():
        problems.append("degree order needs a rank note")
    members = key.get("members") or []
    if not 2 <= len(members) <= 5:
        problems.append(f"key line has {len(members)} members")
    scope = (rule.get("scope") or "").strip()
    if scope.count(".") != 1:
        problems.append("scope must be one sentence")
    objects = rule.get("objects")
    if objects:
        if objects.get("order") not in BASIS_ORDERS.get(objects.get("basis"), ()):
            problems.append("objects basis and order do not match")
        if objects.get("order") == "degree" and not (objects.get("rank_note") or "").strip():
            problems.append("objects degree order needs a rank note")
    return problems


def load_indigenous(root):
    path = Path(root) / "pyramids" / "rebuild" / "ANZSRC45.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    routes = []
    for route in data.get("routes") or []:
        routes.append({**route, "_re": re.compile(route["pattern"], re.I)})
    data = dict(data)
    data["routes"] = routes
    return data


def indigenous_route(node, table):
    """A claim-type route, or the IK default for an indigenous-studies code."""
    if not table:
        return None
    name = node.get("name") or ""
    for route in table.get("routes") or []:
        if route["_re"].search(name):
            return route
    # MSC class 45 is integral equations. Only an ANZSRC indigenous-studies code
    # takes the default. The code is numeric (4501, 450101), and the id is ANZSRC:45…
    ident = str(node.get("id") or "")
    code = str(node.get("code") or "")
    anzsrc = ident.startswith("ANZSRC:") or str(node.get("scheme") or "").startswith("ANZSRC")
    if anzsrc and (ident.startswith("ANZSRC:45") or (code.isdigit() and code.startswith("45"))):
        return {
            "id": "indigenous-studies",
            "owner": table.get("default_owner") or "IK",
            "cell": table.get("default_cell") or "IK.O.A5",
            "reason": table.get("default_reason") or "",
            "provisional": True,
        }
    return None


def load_maps(field, root):
    """(filename, nodes) for every map file of this field."""
    folder = Path(root) / "maps" / field
    found = []
    if not folder.exists():
        return found
    for path in sorted(folder.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        nodes = data.get("nodes") if isinstance(data, dict) else None
        if isinstance(nodes, list):
            found.append((path.name, nodes))
    return found


def nearest_capped_ancestor(node, by_id, cap):
    """The nearest ancestor whose level is at or above the cap."""
    seen = set()
    parent_id = node.get("parent")
    while parent_id and parent_id not in seen:
        seen.add(parent_id)
        parent = by_id.get(parent_id)
        if not parent:
            return None
        if int(parent.get("level") or 1) <= int(cap):
            return parent
        parent_id = parent.get("parent")
    return None


def rule_catalog(rule):
    """One group per key-line member. Used when the field has no built pyramid."""
    field = rule.get("field") or ""
    groups = []
    for index, member in enumerate((rule.get("key_line") or {}).get("members") or [], start=1):
        groups.append({
            "group_id": f"{field}.P.{index}",
            "cell": f"{field}.O.A{index}",
            "statement": member,
        })
    return groups


def classify_nodes(nodes, field, cap, table):
    """Status for each node. A pre-assigned cell is kept, including an override."""
    by_id = {node["id"]: node for node in nodes if node.get("id")}
    rows = []
    for node in nodes:
        if not node.get("id"):
            continue
        route = indigenous_route(node, table)
        if route and route.get("owner") != field:
            rows.append({
                "id": node["id"],
                "name": node.get("name") or "",
                "status": "routed",
                "owner": route.get("owner"),
                "cell": route.get("cell"),
                "reason": route.get("reason") or "",
                "provisional": True,
            })
            continue
        specific = route and route.get("id") not in (None, "indigenous-studies") and route.get("owner") == field
        if specific:
            rows.append({
                "id": node["id"],
                "name": node.get("name") or "",
                "status": "ruled",
                "cell": route.get("cell"),
                "reason": route.get("reason") or "",
                "provisional": True,
            })
            continue
        provisional = bool(route and route.get("owner") == field)
        cell = node.get("taxonomy_cell") or ""
        fine = is_fine(node, cap)
        ancestor = nearest_capped_ancestor(node, by_id, cap) if fine else None
        ancestor_cell = (ancestor or {}).get("taxonomy_cell") or ""
        if cell:
            if fine and ancestor_cell and cell != ancestor_cell:
                rows.append({
                    "id": node["id"],
                    "name": node.get("name") or "",
                    "status": "kept_override",
                    "cell": cell,
                    "ancestor_cell": ancestor_cell,
                    "provisional": provisional,
                })
            else:
                rows.append({
                    "id": node["id"],
                    "name": node.get("name") or "",
                    "status": "ruled",
                    "cell": cell,
                    "provisional": provisional,
                })
            continue
        if fine and ancestor_cell:
            rows.append({
                "id": node["id"],
                "name": node.get("name") or "",
                "status": "filed",
                "cell": ancestor_cell,
                "parent": ancestor.get("id"),
                "provisional": provisional,
            })
            continue
        if fine:
            rows.append({
                "id": node["id"],
                "name": node.get("name") or "",
                "status": "unanchored",
                "level": node.get("level"),
            })
            continue
        rows.append({
            "id": node["id"],
            "name": node.get("name") or "",
            "status": "model",
            "level": node.get("level"),
            "code": node.get("code"),
        })
    return rows


def escalate_count(field, root):
    """Rows a previous run left as unsure or needs_review. No rate is invented."""
    path = Path(root) / "pyramids" / "queues" / f"{field}.placed.jsonl"
    if not path.exists():
        return 0
    latest = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = row.get("node_id") or row.get("id")
        latest[key] = row
    return sum(1 for row in latest.values() if (row.get("status") or "") in ESCALATE_STATUS)


def prepare(field, root, keep_rows=False):
    """Counts after the free filing step. Model items are the tops with no cell."""
    root = Path(root)
    rule = load_rule(field, root)
    cap = int(rule.get("depth_cap") or 2)
    table = load_indigenous(root)
    catalog = rule_catalog(rule)
    counts = Counter()
    by_map = {}
    tops = 0
    model_sample = []
    kept_rows = []
    for filename, nodes in load_maps(field, root):
        rows = classify_nodes(nodes, field, cap, table)
        file_counts = Counter(row["status"] for row in rows)
        by_map[filename] = dict(file_counts)
        by_map[filename]["nodes"] = len(rows)
        counts.update(file_counts)
        counts["nodes"] += len(rows)
        for node, row in zip((node for node in nodes if node.get("id")), rows):
            if int(node.get("level") or 1) <= cap:
                tops += 1
            if row["status"] == "model" and len(model_sample) < 12:
                row = dict(row)
                row["candidates"] = [
                    {"group_id": item["group_id"], "statement": item["statement"]}
                    for item in ranked_shortlist(row.get("name"), catalog, SHORTLIST_WIDTH)
                ]
                model_sample.append(row)
        if keep_rows:
            kept_rows.extend(rows)
    model = counts["model"]
    escalate = escalate_count(field, root)
    report = {
        "field": field,
        "depth_cap": cap,
        "scope": rule.get("scope"),
        "organising_principle": rule.get("organising_principle"),
        "basis": (rule.get("key_line") or {}).get("basis"),
        "order": (rule.get("key_line") or {}).get("order"),
        "nodes": counts["nodes"],
        "ruled": counts["ruled"],
        "filed": counts["filed"],
        "kept_override": counts["kept_override"],
        "routed": counts["routed"],
        "unanchored": counts["unanchored"],
        "model": model,
        "tops": tops,
        "shortlist_width": SHORTLIST_WIDTH,
        "by_map": by_map,
        "model_sample": model_sample,
        "hybrid": hybrid_estimate(model, escalate, USD_PER_THOUSAND),
        "upper_if_all_tops_escalated": round(tops * USD_PER_THOUSAND / 1000, 6),
        "upper_if_cap_not_applied": round(counts["nodes"] * USD_PER_THOUSAND / 1000, 6),
        "note": (
            "Claude is priced only for unsure and needs_review rows already on file. "
            "No unsure rate is applied to the remaining tops."
        ),
    }
    if keep_rows:
        report["rows"] = kept_rows
    return report


def shared_queue(fields, root, include_rows=False, sample=20):
    """One queue row per MeSH descriptor UI. Tree copies stay on that row.

    The same descriptor is often filed under medicine, biology, chemistry,
    and the other life-science maps. The UI is the dedupe key, not the tree id.
    Agreeing cells have one home. Disagreeing cells stay for a model, with
    those cells as the candidates.
    """
    root = Path(root)
    buckets = {}
    for field in fields:
        path = root / "maps" / field / "mesh2026.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for node in data.get("nodes") or []:
            ui = node.get("ui")
            if not ui:
                continue
            row = buckets.setdefault(ui, {"ui": ui, "name": node.get("name") or "", "copies": []})
            if not row["name"]:
                row["name"] = node.get("name") or ""
            row["copies"].append({
                "field": field,
                "id": node.get("id"),
                "code": node.get("code"),
                "cell": node.get("taxonomy_cell") or "",
            })
    rows = []
    shared = agreed = conflicts = cross_field_conflicts = 0
    conflict_sample = []
    for ui in sorted(buckets):
        bucket = buckets[ui]
        copies = bucket["copies"]
        present = sorted({copy["field"] for copy in copies})
        cells = sorted({copy["cell"] for copy in copies if copy["cell"]})
        if len(present) > 1:
            shared += 1
        if len(cells) > 1:
            status = "model"
            home = ""
            conflicts += 1
            if len(present) > 1:
                cross_field_conflicts += 1
            if len(conflict_sample) < sample:
                conflict_sample.append({
                    "ui": ui,
                    "name": bucket["name"],
                    "fields": present,
                    "cells": cells,
                    "status": "model",
                })
        else:
            status = "home"
            home = cells[0].split(".")[0] if cells else (present[0] if present else "")
            if len(present) > 1:
                agreed += 1
        if include_rows:
            rows.append({
                "ui": ui,
                "name": bucket["name"],
                "status": status,
                "home": home,
                "cells": cells,
                "copies": copies,
            })
    return {
        "fields": list(fields),
        "key": "MeSH descriptor UI",
        "descriptor_rows": len(buckets),
        "tree_copies": sum(len(bucket["copies"]) for bucket in buckets.values()),
        "shared_descriptors": shared,
        "agreed": agreed,
        "conflicts": conflicts,
        "cross_field_conflicts": cross_field_conflicts,
        "conflict_sample": conflict_sample,
        "rows": rows,
    }
