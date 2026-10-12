"""Form Minto groups for one cell and write a definition for each group.

No network calls live here. A caller supplies `ask(task, payload)`. The
system instructions stay fixed so a prompt cache can hit. A proposal that
fails the checker is asked again, then the batch is split.
"""
import json
from pathlib import Path

from minto_build import admitted_nodes
from minto_check import BASIS_ORDERS, ORDERS, is_definition, minto_counts

BATCH = 20
# A cell needs two groups, and each group needs two leaves.
MIN_CELL = 4
PASS_KEYS = (
    "template_summaries",
    "group_size",
    "single_child",
    "missing_basis",
    "missing_order",
    "basis_order_mismatch",
    "degree_without_rank",
    "loose_topics",
    "missing_summaries",
)

SYSTEM = "\n".join([
    "You group concepts into a Minto classification.",
    "A group has two to five members.",
    "Basis is cause_effect, parts, or kinds.",
    "cause_effect takes order time.",
    "parts takes order structure.",
    "kinds takes order structure, or degree when rank_note states the ranking.",
    "The statement of a group is one sentence of at least six words.",
    "It defines the group.",
    "It does not start with These, Both are, or All are.",
    "Every id in the user message appears in exactly one group.",
    "Return JSON matching the schema.",
])

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "statement": {"type": "string"},
        "basis": {"type": "string", "enum": ["cause_effect", "parts", "kinds"]},
        "order": {"type": "string", "enum": ["time", "structure", "degree"]},
        "rank_note": {"type": "string"},
        "groups": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "statement": {"type": "string"},
                    "basis": {"type": "string", "enum": ["cause_effect", "parts", "kinds"]},
                    "order": {"type": "string", "enum": ["time", "structure", "degree"]},
                    "rank_note": {"type": "string"},
                    "members": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["statement", "basis", "order", "rank_note", "members"],
            },
        },
    },
    "required": ["statement", "basis", "order", "rank_note", "groups"],
}


def batches(nodes, size=BATCH):
    """Chunks of at least two. A leftover of one stays with the previous chunk."""
    rows = list(nodes)
    size = max(2, int(size))
    out = []
    while rows:
        if len(rows) <= size + 1:
            out.append(rows)
            break
        out.append(rows[:size])
        rows = rows[size:]
    return out


def _pair_problem(basis, order, rank_note, label):
    if basis not in BASIS_ORDERS:
        return f"{label} basis"
    if order not in BASIS_ORDERS[basis]:
        return f"{label} order {basis}/{order}"
    if order == "degree" and not (rank_note or "").strip():
        return f"{label} rank"
    if order not in ORDERS:
        return f"{label} order"
    return ""


def _group_pyramid(group, names):
    points = []
    for member in group.get("members") or []:
        name = names.get(member) or member
        points.append({
            "id": member,
            "anchor": f"node:{member}",
            "statement": name,
            "name": name,
        })
    support = {
        "basis": group.get("basis"),
        "order": group.get("order"),
        "points": points,
    }
    if group.get("rank_note"):
        support["rank_note"] = group["rank_note"]
    return {"key_line": support}


def checker_problems(pyramid):
    counts = minto_counts(pyramid)
    return [f"{key} {counts[key]}" for key in PASS_KEYS if counts.get(key)]


def validate_groups(nodes, proposal, min_groups=1):
    """Structural checks, then minto_check on each group."""
    wanted = [node["id"] for node in nodes]
    names = {node["id"]: node.get("name") or node["id"] for node in nodes}
    groups = (proposal or {}).get("groups") if isinstance(proposal, dict) else None
    if not isinstance(groups, list) or not groups:
        return ["no groups"]
    if len(groups) < min_groups:
        return [f"need at least {min_groups} groups"]
    problems = []
    seen = []
    for index, group in enumerate(groups):
        members = list(group.get("members") or [])
        label = f"group {index}"
        if not 2 <= len(members) <= 5:
            problems.append(f"{label} has {len(members)} members")
        pair = _pair_problem(group.get("basis"), group.get("order"), group.get("rank_note"), label)
        if pair:
            problems.append(pair)
        if not is_definition(group.get("statement") or ""):
            problems.append(f"{label} statement")
        seen.extend(members)
        if not problems:
            found = checker_problems(_group_pyramid(group, names))
            problems.extend(f"{label} {item}" for item in found)
    if sorted(seen) != sorted(wanted) or len(seen) != len(wanted):
        problems.append("members do not match the batch")
    return problems


def validate_head(head, group_points):
    """The cell sentence, then minto_check on the groups under that basis and order."""
    if not isinstance(head, dict):
        return ["no head"]
    problems = []
    if not is_definition(head.get("statement") or ""):
        problems.append("cell statement")
    pair = _pair_problem(head.get("basis"), head.get("order"), head.get("rank_note"), "cell")
    if pair:
        problems.append(pair)
    if problems:
        return problems
    support = {
        "basis": head.get("basis"),
        "order": head.get("order"),
        "points": group_points,
    }
    if head.get("rank_note"):
        support["rank_note"] = head["rank_note"]
    return checker_problems({"key_line": support})


def _stamp(groups, ident):
    stamped = []
    for group in groups:
        stamped.append({
            "id": next(ident),
            "statement": group.get("statement") or "",
            "basis": group.get("basis"),
            "order": group.get("order"),
            "rank_note": group.get("rank_note") or "",
            "members": list(group.get("members") or []),
        })
    return stamped


def form_batch(nodes, ask, ident, min_groups=1, depth=0):
    """Ask twice. A batch of four or more is then split in half."""
    if len(nodes) < 2:
        return {"status": "blocked", "reason": "fewer than two members", "member_ids": [node["id"] for node in nodes]}
    problems = []
    proposal = None
    for _attempt in range(2):
        proposal = ask("form", {
            "nodes": [{"id": node["id"], "name": node.get("name") or node["id"]} for node in nodes],
            "min_groups": min_groups,
            "problems": problems,
        })
        problems = validate_groups(nodes, proposal, min_groups=min_groups)
        if not problems:
            return {"status": "placed", "groups": _stamp(proposal["groups"], ident)}
    if len(nodes) < 4 or depth > 8:
        return {
            "status": "needs_review",
            "reason": "; ".join(problems),
            "member_ids": [node["id"] for node in nodes],
        }
    mid = len(nodes) // 2
    if mid < 2 or len(nodes) - mid < 2:
        return {
            "status": "needs_review",
            "reason": "; ".join(problems),
            "member_ids": [node["id"] for node in nodes],
        }
    left = form_batch(nodes[:mid], ask, ident, min_groups=1, depth=depth + 1)
    right = form_batch(nodes[mid:], ask, ident, min_groups=1, depth=depth + 1)
    if left.get("status") != "placed" or right.get("status") != "placed":
        return {
            "status": "needs_review",
            "reason": "split failed",
            "member_ids": [node["id"] for node in nodes],
            "parts": [left, right],
        }
    return {"status": "placed", "groups": left["groups"] + right["groups"]}


def _as_nodes(groups):
    return [{"id": group["id"], "name": group["statement"]} for group in groups]


def _nest(parent_groups, children):
    """Parent members are child group ids. Keep the child group under that member."""
    by_id = {group["id"]: group for group in children}
    nested = []
    for parent in parent_groups:
        parent = dict(parent)
        parent["children"] = [by_id[member] for member in parent["members"] if member in by_id]
        nested.append(parent)
    return nested


def _to_point(group, leaves):
    points = []
    if group.get("children"):
        points = [_to_point(child, leaves) for child in group["children"]]
    else:
        for member in group.get("members") or []:
            name = leaves.get(member) or member
            points.append({
                "id": member,
                "anchor": f"node:{member}",
                "statement": name,
                "name": name,
            })
    support = {
        "logic_type": "inductive",
        "plural_noun": "members",
        "basis": group.get("basis"),
        "order": group.get("order"),
        "points": points,
    }
    if group.get("rank_note"):
        support["rank_note"] = group["rank_note"]
    return {
        "id": group["id"],
        "anchor": f"group:{group['id']}",
        "statement": group.get("statement") or "",
        "name": group.get("statement") or "",
        "support": support,
    }


def _min_groups(count):
    if count <= 5:
        return 2
    return 1


def _max_group_index(groups, cell):
    """Highest G index already used under this cell, including nested groups."""
    prefix = f"{cell}.G"
    highest = 0
    for group in groups or []:
        gid = str(group.get("id") or "")
        tail = gid[len(prefix):] if gid.startswith(prefix) else ""
        if tail.isdigit():
            highest = max(highest, int(tail))
        highest = max(highest, _max_group_index(group.get("children"), cell))
    return highest


def _ident(cell, groups):
    start = _max_group_index(groups, cell) + 1
    return iter(f"{cell}.G{index}" for index in range(start, 100000))


def form_cell(cell, nodes, ask, batch_size=BATCH, seed_groups=None, on_batch=None, known=None):
    """Groups for one cell, then one definition for the cell itself.

    seed_groups are batches already on the resume log. Their ids are not
    reused. on_batch is called after each new batch so a stop can resume
    without repeating it. known supplies names for members already grouped.
    """
    nodes = list(nodes)
    groups = list(seed_groups or [])
    ident = _ident(cell, groups)
    if len(nodes) < MIN_CELL and not groups:
        return {
            "cell": cell,
            "status": "blocked",
            "reason": "fewer than four admitted nodes",
            "member_ids": [node["id"] for node in nodes],
        }
    blocked = []
    for chunk in batches(nodes, batch_size):
        whole = not groups and len(chunk) == len(nodes)
        minimum = _min_groups(len(chunk)) if whole else 1
        formed = form_batch(chunk, ask, ident, min_groups=minimum)
        formed = dict(formed)
        formed["member_ids"] = [node["id"] for node in chunk]
        if on_batch:
            on_batch(formed)
        if formed.get("status") != "placed":
            blocked.append(formed)
            continue
        groups.extend(formed["groups"])
    guard = 0
    while len(groups) > 5 and guard < 8:
        guard += 1
        lifted = form_batch(_as_nodes(groups), ask, ident, min_groups=1)
        if lifted.get("status") != "placed":
            return {
                "cell": cell,
                "status": "needs_review",
                "reason": "could not group the groups",
                "member_ids": [node["id"] for node in nodes],
            }
        groups = _nest(lifted["groups"], groups)
    if blocked or not 2 <= len(groups) <= 5:
        return {
            "cell": cell,
            "status": "needs_review",
            "reason": f"{len(groups)} groups under the cell",
            "member_ids": [node["id"] for node in nodes],
            "blocked": blocked,
        }
    leaves = {}
    for node in list(known or []) + nodes:
        leaves[node["id"]] = node.get("name") or node["id"]
    points = [_to_point(group, leaves) for group in groups]
    problems = []
    head = None
    for _attempt in range(2):
        head = ask("head", {
            "groups": [{"id": group["id"], "statement": group["statement"]} for group in groups],
            "problems": problems,
        })
        problems = validate_head(head, points)
        if not problems:
            break
    else:
        return {
            "cell": cell,
            "status": "needs_review",
            "reason": "; ".join(problems),
            "member_ids": [node["id"] for node in nodes],
        }
    support = {
        "logic_type": "inductive",
        "plural_noun": "members",
        "basis": head.get("basis"),
        "order": head.get("order"),
        "points": points,
    }
    if head.get("rank_note"):
        support["rank_note"] = head["rank_note"]
    point = {
        "id": cell,
        "anchor": f"cell:{cell}",
        "statement": head.get("statement") or "",
        "name": head.get("statement") or "",
        "support": support,
    }
    return {
        "cell": cell,
        "status": "placed",
        "member_ids": [node["id"] for node in nodes],
        "point": point,
        "blocked": blocked,
    }


def cell_jobs(field, root):
    """One job per cell that has an admitted node. Catalogue rules already applied."""
    found = admitted_nodes(field, root)
    by_cell = {}
    for node in found["nodes"]:
        by_cell.setdefault(node["cell"], []).append(node)
    jobs = []
    for cell in sorted(by_cell):
        jobs.append({
            "field": field,
            "cell": cell,
            "principle": found["principle"],
            "nodes": by_cell[cell],
        })
    return jobs


def log_path(root, field):
    return Path(root) / "pyramids" / "queues" / f"{field}.groups.jsonl"


def result_path(root, field):
    return Path(root) / "pyramids" / "queues" / f"{field}.groups.json"


def read_log(path):
    rows = []
    path = Path(path)
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def pending_work(rows, cell, nodes):
    """Placed batches stay done. A batch is exhausted after two failed tries.

    A cell line closes the cell, so this only matters when that line is
    absent. Delete the cell line to ask again. Delete its batch lines too
    if a failed batch should be asked a further time.
    """
    done = set()
    groups = []
    attempts = {}
    for row in rows:
        if row.get("cell") != cell or row.get("part") != "batch":
            continue
        key = row.get("batch_key") or ""
        if row.get("status") == "needs_review":
            attempts[key] = attempts.get(key, 0) + 1
        if row.get("status") == "placed":
            done.update(row.get("member_ids") or [])
            groups.extend(row.get("groups") or [])
    exhausted = set()
    for row in rows:
        if row.get("cell") != cell or row.get("part") != "batch" or row.get("status") != "needs_review":
            continue
        if attempts.get(row.get("batch_key") or "", 0) >= 2:
            exhausted.update(row.get("member_ids") or [])
    pending = [node for node in nodes if node["id"] not in done and node["id"] not in exhausted]
    return pending, groups, sorted(exhausted)


def finished_cells(rows):
    """Cells with a terminal line. A cost stop writes no such line."""
    done = {}
    for row in rows:
        if row.get("part") == "cell" and row.get("cell"):
            done[row["cell"]] = row
    return done


def append_log(path, row):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_result(root, field, rows):
    cells = []
    for row in rows:
        if row.get("part") == "cell" and row.get("status") == "placed" and row.get("point"):
            cells.append(row["point"])
    payload = {"field": field, "cells": cells}
    path = result_path(root, field)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload
