"""Form Minto groups for one cell and write a definition for each group.

No network calls live here. A caller supplies `ask(task, payload)`. The
system instructions stay fixed so a prompt cache can hit. A proposal is
repaired before it is rejected: missing ids join the nearest group by a
local word embedding, or a further group; singletons merge into a neighbour;
group sizes stay 2 to 5. A bare label gets one sentence call, then a
templated definition flagged for review. A batch that still fails is split,
and a passing half is kept.
"""
import json
import math
import re
from pathlib import Path

from minto_build import admitted_nodes
from minto_check import BASIS_ORDERS, ORDERS, is_definition, minto_counts

BATCH = 20
# Below this, the cell is one group. At or above it, the cell needs 2 to 5.
MIN_CELL = 4
FURTHER = "further"
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
    "The user message gives group_count. Return exactly that many groups.",
    "When the task is sentence, return only statement, one defining sentence for that group.",
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


def validate_head(head, group_points, allow_single=False):
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
    found = checker_problems({"key_line": support})
    if allow_single:
        found = [
            item for item in found
            if not item.startswith("group_size") and not item.startswith("single_child")
        ]
    return found


def target_groups(count):
    """ceil(n/4), clamped to 2–5. A cell under four nodes is one group."""
    count = int(count)
    if count < MIN_CELL:
        return 1
    number = math.ceil(count / 4)
    if number < 2:
        number = 2
    if number > 5:
        number = 5
    high = max(1, count // 2)
    low = max(1, math.ceil(count / 5))
    return max(low, min(high, number))


def embed_text(text):
    """Word counts as a vector. Local and deterministic. No model call."""
    counts = {}
    for token in re.findall(r"[a-z0-9]+", (text or "").lower()):
        counts[token] = counts.get(token, 0.0) + 1.0
    return counts


def _cosine(left, right):
    if not left or not right:
        return 0.0
    dot = 0.0
    for key, value in left.items():
        if key in right:
            dot += value * right[key]
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def _legalise(basis, order, rank_note):
    rank_note = rank_note or ""
    if basis not in BASIS_ORDERS:
        basis = "kinds"
    allowed = BASIS_ORDERS[basis]
    if order not in allowed or (order == "degree" and not rank_note.strip()):
        order = "structure" if "structure" in allowed else "time"
    return basis, order, rank_note


def _blank_group(members=None, statement=""):
    basis, order, rank_note = _legalise("kinds", "structure", "")
    group = {
        "statement": statement,
        "basis": basis,
        "order": order,
        "rank_note": rank_note,
        "members": list(members or []),
    }
    if (statement or "").strip().lower() == FURTHER:
        group["further"] = True
    return group


def _group_text(group, names):
    parts = [group.get("statement") or ""]
    for member in group.get("members") or []:
        parts.append(names.get(member) or member)
    return " ".join(parts)


def _nearest_index(name, groups, names):
    """Highest cosine above zero. Ties keep the earlier group."""
    text = embed_text(name)
    best = None
    for index, group in enumerate(groups):
        score = round(_cosine(text, embed_text(_group_text(group, names))), 6)
        if score <= 0:
            continue
        cand = (score, -index)
        if best is None or cand > best[0]:
            best = (cand, index)
    if best is None:
        return None
    return best[1]


def _further_index(groups):
    for index, group in enumerate(groups):
        if group.get("further") or (group.get("statement") or "").strip().lower() == FURTHER:
            return index
    return None


def assign_members(nodes, proposal):
    """Drop unknown ids. Missing ids join the nearest group, or one further group."""
    names = {node["id"]: node.get("name") or node["id"] for node in nodes}
    wanted = [node["id"] for node in nodes]
    wanted_set = set(wanted)
    raw_groups = (proposal or {}).get("groups") if isinstance(proposal, dict) else None
    groups = []
    seen = set()
    for raw in raw_groups or []:
        if not isinstance(raw, dict):
            continue
        basis, order, rank_note = _legalise(raw.get("basis"), raw.get("order"), raw.get("rank_note"))
        members = []
        for member in raw.get("members") or []:
            member = str(member)
            if member not in wanted_set or member in seen:
                continue
            members.append(member)
            seen.add(member)
        group = {
            "statement": raw.get("statement") or "",
            "basis": basis,
            "order": order,
            "rank_note": rank_note,
            "members": members,
        }
        if (group["statement"] or "").strip().lower() == FURTHER:
            group["further"] = True
        groups.append(group)
    for missing in wanted:
        if missing in seen:
            continue
        dest = _nearest_index(names[missing], groups, names)
        if dest is None:
            dest = _further_index(groups)
        if dest is None:
            groups.append(_blank_group(statement=FURTHER))
            dest = len(groups) - 1
        groups[dest]["members"].append(missing)
        seen.add(missing)
    return [group for group in groups if group["members"]]


def _absorb(groups, src, dest):
    """Move src into dest. dest is updated before src is removed."""
    if src == dest:
        return
    statement = groups[dest].get("statement") or ""
    other = groups[src].get("statement") or ""
    if not is_definition(statement) and (is_definition(other) or len(other) > len(statement)):
        groups[dest]["statement"] = other
        if (other or "").strip().lower() == FURTHER:
            groups[dest]["further"] = True
    groups[dest]["members"].extend(groups[src]["members"])
    if groups[src].get("further"):
        groups[dest]["further"] = True
    del groups[src]


def _pair_choice(groups, names, limit):
    best = None
    for left in range(len(groups)):
        for right in range(left + 1, len(groups)):
            total = len(groups[left]["members"]) + len(groups[right]["members"])
            if limit is not None and total > limit:
                continue
            score = round(_cosine(
                embed_text(_group_text(groups[left], names)),
                embed_text(_group_text(groups[right], names)),
            ), 6)
            cand = (score, -left, -right)
            if best is None or cand > best[0]:
                best = (cand, left, right)
    return None if best is None else (best[1], best[2])


def _merge_closest(groups, names, limit):
    pair = _pair_choice(groups, names, limit)
    if pair is None:
        return False
    _absorb(groups, pair[1], pair[0])
    return True


def _least_similar_member(group, names):
    members = group["members"]
    best = None
    for index, member in enumerate(members):
        others = [names.get(item) or item for item in members if item != member]
        score = round(_cosine(
            embed_text(names.get(member) or member),
            embed_text(" ".join(others)),
        ), 6)
        cand = (score, -index)
        if best is None or cand < best[0]:
            best = (cand, member)
    return best[1]


def _peel(group, names, count):
    moving = []
    while len(moving) < count and len(group["members"]) > 2:
        member = _least_similar_member(group, names)
        group["members"].remove(member)
        moving.append(member)
    return moving


def _shed_excess(groups, names):
    index = max(range(len(groups)), key=lambda item: (len(groups[item]["members"]), -item))
    size = len(groups[index]["members"])
    if size <= 5:
        return False
    extra = size - 5
    moving = _peel(groups[index], names, extra if extra >= 2 else 2)
    if not moving:
        return False
    groups.append(_blank_group(moving, FURTHER))
    return True


def _split_toward_target(groups, names):
    candidates = [index for index, group in enumerate(groups) if len(group["members"]) >= 4]
    if not candidates:
        return False
    index = max(candidates, key=lambda item: (len(groups[item]["members"]), -item))
    moving = _peel(groups[index], names, 2)
    if len(moving) < 2:
        groups[index]["members"].extend(moving)
        return False
    groups.append(_blank_group(moving, groups[index].get("statement") or ""))
    return True


def _merge_one_singleton(groups, names):
    singles = [index for index, group in enumerate(groups) if len(group["members"]) == 1]
    if not singles or len(groups) < 2:
        return False
    src = singles[0]
    text = embed_text(_group_text(groups[src], names))
    best = None
    for index, group in enumerate(groups):
        if index == src or len(group["members"]) >= 5:
            continue
        score = round(_cosine(text, embed_text(_group_text(group, names))), 6)
        cand = (score, -index)
        if best is None or cand > best[0]:
            best = (cand, index)
    if best is None:
        return _merge_closest(groups, names, limit=None)
    _absorb(groups, src, best[1])
    return True


def _legal_shape(groups, target):
    if target == 1:
        return len(groups) == 1 and bool(groups[0]["members"])
    if not 2 <= len(groups) <= 5:
        return False
    return all(2 <= len(group["members"]) <= 5 for group in groups)


def _pair_fits(groups):
    for left in range(len(groups)):
        for right in range(left + 1, len(groups)):
            if len(groups[left]["members"]) + len(groups[right]["members"]) <= 5:
                return True
    return False


def balance(groups, names, target):
    """Singleton merges, then closest-pair merges, until sizes are 2–5."""
    groups = [_blank_group(group.get("members"), group.get("statement") or "") | {
        "basis": group.get("basis") or "kinds",
        "order": group.get("order") or "structure",
        "rank_note": group.get("rank_note") or "",
        "further": bool(group.get("further")),
    } for group in groups if group.get("members")]
    for group in groups:
        basis, order, rank_note = _legalise(group.get("basis"), group.get("order"), group.get("rank_note"))
        group["basis"] = basis
        group["order"] = order
        group["rank_note"] = rank_note
    if not groups:
        return []
    if target == 1:
        while len(groups) > 1:
            if not _merge_closest(groups, names, limit=None):
                break
        return groups
    for _step in range(80):
        if _legal_shape(groups, target) and len(groups) == target:
            return groups
        if any(len(group["members"]) == 1 for group in groups) and len(groups) > 1:
            if _merge_one_singleton(groups, names):
                continue
            break
        if any(len(group["members"]) > 5 for group in groups):
            if _shed_excess(groups, names):
                continue
            break
        if len(groups) > 5 or (len(groups) > target and _pair_fits(groups)):
            if _merge_closest(groups, names, limit=5):
                continue
            if _merge_closest(groups, names, limit=None):
                continue
            break
        if len(groups) < target:
            if _split_toward_target(groups, names):
                continue
            break
        if _legal_shape(groups, target):
            return groups
        break
    return [group for group in groups if group["members"]]


def repair_groups(nodes, proposal):
    """A legal packing of these nodes, or None when the nodes cannot be packed."""
    if not nodes:
        return None
    names = {node["id"]: node.get("name") or node["id"] for node in nodes}
    groups = assign_members(nodes, proposal)
    if not groups:
        groups = [_blank_group([node["id"] for node in nodes], FURTHER)]
    target = target_groups(len(nodes))
    groups = balance(groups, names, target)
    got = [member for group in groups for member in group["members"]]
    if sorted(got) != sorted(node["id"] for node in nodes) or len(got) != len(nodes):
        return None
    if not _legal_shape(groups, target):
        return None
    return groups


def _fallback_statement(group, names):
    label = " ".join((group.get("statement") or "").split()).strip(" .")
    if not label or label.lower() == FURTHER:
        shown = [names.get(member) or member for member in (group.get("members") or [])[:2]]
        label = " and ".join(shown) if shown else "the named members"
    text = f"The group covers {label} as one kind of claim."
    if not is_definition(text):
        text = "The group covers the named members as one kind of claim."
    return text


def _fill_statements(groups, nodes, ask):
    """One sentence call for a bare label, then a templated definition flagged for review."""
    names = {node["id"]: node.get("name") or node["id"] for node in nodes}
    for group in groups:
        if is_definition(group.get("statement") or ""):
            continue
        reply = ask("sentence", {
            "label": group.get("statement") or "",
            "members": [
                {"id": member, "name": names.get(member) or member}
                for member in group.get("members") or []
            ],
        }) or {}
        text = reply.get("statement") if isinstance(reply, dict) else ""
        if is_definition(text or ""):
            group["statement"] = text.strip()
            continue
        group["statement"] = _fallback_statement(group, names)
        group["review"] = True


def _fallback_head(groups):
    return "The cell gathers the groups under one stated order."


def _fill_head(head, groups, ask):
    text = (head or {}).get("statement") or "" if isinstance(head, dict) else ""
    if is_definition(text):
        return text, False
    reply = ask("sentence", {
        "label": text,
        "members": [{"id": group["id"], "name": group.get("statement") or group["id"]} for group in groups],
    }) or {}
    got = reply.get("statement") if isinstance(reply, dict) else ""
    if is_definition(got or ""):
        return got.strip(), False
    fallback = _fallback_head(groups)
    if not is_definition(fallback):
        fallback = "The cell gathers the groups under one stated order."
    return fallback, True


def _stamp(groups, ident):
    stamped = []
    for group in groups:
        row = {
            "id": next(ident),
            "statement": group.get("statement") or "",
            "basis": group.get("basis"),
            "order": group.get("order"),
            "rank_note": group.get("rank_note") or "",
            "members": list(group.get("members") or []),
        }
        if group.get("review"):
            row["review"] = True
        if group.get("further"):
            row["further"] = True
        stamped.append(row)
    return stamped


def _review_only(nodes, reason):
    ids = [node["id"] for node in nodes]
    return {
        "status": "needs_review",
        "reason": reason,
        "member_ids": ids,
        "review_ids": ids,
        "groups": [],
    }


def _combine_halves(left, right):
    """Keep every passing group. Only the failed nodes go to review."""
    groups = []
    review = []
    for part in (left, right):
        groups.extend(part.get("groups") or [])
        if part.get("status") == "placed":
            review.extend(part.get("review_ids") or [])
        else:
            review.extend(part.get("review_ids") or part.get("member_ids") or [])
    placed = {member for group in groups for member in group.get("members") or []}
    review = [item for item in review if item not in placed]
    if groups:
        return {
            "status": "placed",
            "groups": groups,
            "review_ids": review,
            "reason": "split kept the passing half" if review else "",
        }
    return {
        "status": "needs_review",
        "reason": "split failed",
        "groups": [],
        "review_ids": review,
        "member_ids": review,
    }


def form_batch(nodes, ask, ident, min_groups=1, depth=0):
    """Ask twice. Repair the reply. A batch of four or more is then split."""
    del min_groups  # The target count is ceil(n/4), not the caller's minimum.
    nodes = list(nodes)
    count = target_groups(len(nodes))
    if not nodes:
        return _review_only(nodes, "no members")
    problems = []
    for _attempt in range(2):
        proposal = ask("form", {
            "nodes": [{"id": node["id"], "name": node.get("name") or node["id"]} for node in nodes],
            "group_count": count,
            "min_groups": count,
            "problems": problems,
        })
        groups = repair_groups(nodes, proposal)
        if not groups:
            problems = ["could not repair the groups"]
            continue
        _fill_statements(groups, nodes, ask)
        minimum = 1 if count == 1 else 2
        if len(nodes) == 1:
            problems = []
        else:
            problems = validate_groups(nodes, {"groups": groups}, min_groups=minimum)
        if not problems:
            return {
                "status": "placed",
                "groups": _stamp(groups, ident),
                "review_ids": [],
            }
    if len(nodes) < MIN_CELL or depth > 8:
        return _review_only(nodes, "; ".join(problems) or "could not repair the groups")
    mid = len(nodes) // 2
    if mid < 2 or len(nodes) - mid < 2:
        return _review_only(nodes, "; ".join(problems) or "could not repair the groups")
    left = form_batch(nodes[:mid], ask, ident, depth=depth + 1)
    right = form_batch(nodes[mid:], ask, ident, depth=depth + 1)
    return _combine_halves(left, right)


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
    point = {
        "id": group["id"],
        "anchor": f"group:{group['id']}",
        "statement": group.get("statement") or "",
        "name": group.get("statement") or "",
        "support": support,
    }
    if group.get("review"):
        point["review"] = True
    return point


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
    if not nodes and not groups:
        return {
            "cell": cell,
            "status": "needs_review",
            "reason": "no admitted nodes",
            "member_ids": [],
        }
    blocked = []
    review_ids = []
    for chunk in batches(nodes, batch_size):
        formed = form_batch(chunk, ask, ident)
        formed = dict(formed)
        chunk_ids = [node["id"] for node in chunk]
        placed_ids = []
        for group in formed.get("groups") or []:
            for member in group.get("members") or []:
                if member in chunk_ids and member not in placed_ids:
                    placed_ids.append(member)
        formed["member_ids"] = placed_ids if formed.get("status") == "placed" else list(formed.get("member_ids") or chunk_ids)
        if on_batch:
            on_batch(formed)
        review_ids.extend(item for item in formed.get("review_ids") or [] if item not in review_ids)
        if formed.get("groups"):
            groups.extend(formed["groups"])
        if formed.get("status") != "placed":
            blocked.append(formed)
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
    seed_leaves = sum(len(group.get("members") or []) for group in (seed_groups or []))
    allow_single = (len(nodes) + seed_leaves) < MIN_CELL and len(groups) == 1
    if blocked or not (allow_single or 2 <= len(groups) <= 5):
        return {
            "cell": cell,
            "status": "needs_review",
            "reason": f"{len(groups)} groups under the cell",
            "member_ids": [node["id"] for node in nodes],
            "review_ids": review_ids,
            "groups": groups,
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
        text, head_review = _fill_head(head, groups, ask)
        if isinstance(head, dict):
            head = dict(head)
        else:
            head = {"basis": "kinds", "order": "structure", "rank_note": ""}
        head["statement"] = text
        basis, order, rank_note = _legalise(head.get("basis"), head.get("order"), head.get("rank_note"))
        head["basis"] = basis
        head["order"] = order
        head["rank_note"] = rank_note
        problems = validate_head(head, points, allow_single=allow_single)
        if not problems:
            break
    else:
        return {
            "cell": cell,
            "status": "needs_review",
            "reason": "; ".join(problems),
            "member_ids": [node["id"] for node in nodes],
            "review_ids": review_ids,
            "groups": groups,
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
    if head_review:
        point["review"] = True

    def _flagged(rows):
        found = []
        for group in rows or []:
            if group.get("review"):
                found.append(group["id"])
            found.extend(_flagged(group.get("children")))
        return found

    return {
        "cell": cell,
        "status": "placed",
        "member_ids": [node["id"] for node in nodes],
        "point": point,
        "blocked": blocked,
        "review_ids": review_ids,
        "statement_review": _flagged(groups),
        "head_review": head_review,
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
