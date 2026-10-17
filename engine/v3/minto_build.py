"""Build a field pyramid from its rule and its maps, then count Minto failures.

No model is called. The key line takes its basis and order from the rule
file. Source nodes keep their parent links. Nothing else is invented: a
source group has no basis, no order, and no definition sentence.

Two further free rules are used only when pricing model work. An LCC
schedule line is filed under its class heading. A flat term index is
catalogued under its cell. The checker is also run without those rules,
so the raw rebuild is visible.
"""
import math
import re
from collections import defaultdict
from pathlib import Path

from cost_cap import USD_PER_THOUSAND
from field_rebuild import indigenous_route, load_indigenous, load_maps, load_rule
from minto_check import is_definition, minto_issues

LCC_LINE = re.compile(r"^[A-Z]{1,3}\d")
CELL_INDEX = re.compile(r"\.O\.A(\d+)")
FLAT_MIN_NODES = 1000
FLAT_LEVEL1 = 0.9


def is_lcc_schedule(node):
    """A schedule line under a class letter. The class heading itself stays."""
    if not str(node.get("_file") or "").startswith("lcc"):
        return False
    return bool(LCC_LINE.match(str(node.get("code") or "")))


def flat_index_files(maps, min_nodes=FLAT_MIN_NODES, level1_share=FLAT_LEVEL1):
    """Files that are term lists, not a hierarchy. The Gold Book is one."""
    found = []
    for filename, nodes in maps:
        if len(nodes) < min_nodes:
            continue
        level1 = sum(1 for node in nodes if int(node.get("level") or 1) == 1)
        if level1 / len(nodes) >= level1_share:
            found.append(filename)
    return found


def min_new_groups(members):
    """Groups to insert so this many siblings sit in groups of two to five."""
    if members <= 5:
        return 0
    groups = 0
    remaining = members
    while remaining > 5:
        remaining = math.ceil(remaining / 5)
        groups += remaining
    return groups


def _tagged(maps):
    tagged = []
    for filename, nodes in maps:
        for node in nodes:
            if not node.get("id"):
                continue
            row = dict(node)
            row["_file"] = filename
            tagged.append(row)
    return tagged


def _select(nodes, cap, table, field, catalogue):
    """Nodes that enter the pyramid. Catalogue rules apply only when asked."""
    flat = set(catalogue.get("flat") or [])
    use_catalogue = catalogue.get("enabled")
    admitted = []
    lcc_filed = flat_filed = 0
    for node in nodes:
        if int(node.get("level") or 1) > cap:
            continue
        route = indigenous_route(node, table)
        if route and route.get("owner") != field:
            continue
        if use_catalogue and is_lcc_schedule(node):
            lcc_filed += 1
            continue
        if use_catalogue and node.get("_file") in flat:
            flat_filed += 1
            continue
        admitted.append(node)
    return admitted, lcc_filed, flat_filed


def _forest(nodes):
    """Source parent links. A missing parent hangs on the cell."""
    ids = {node["id"] for node in nodes}
    children = defaultdict(list)
    roots = []
    for node in nodes:
        parent = node.get("parent")
        if parent in ids:
            children[parent].append(node)
        else:
            roots.append(node)

    def point(node):
        kids = sorted(children.get(node["id"], []), key=lambda item: (str(item.get("code") or ""), item.get("name") or ""))
        made = {
            "id": node["id"],
            "anchor": f"node:{node['id']}",
            "statement": node.get("name") or node["id"],
            "name": node.get("name") or "",
        }
        if kids:
            made["support"] = {
                "logic_type": "inductive",
                "plural_noun": "members",
                "points": [point(child) for child in kids],
            }
        return made

    roots.sort(key=lambda item: (str(item.get("code") or ""), item.get("name") or ""))
    return [point(node) for node in roots]


def _cell_point(ident, anchor, statement, nodes, basis=None, order=None, dimension=None, rank_note=None):
    support = {
        "logic_type": "inductive",
        "plural_noun": "members",
        "points": _forest(nodes),
    }
    if basis:
        support["basis"] = basis
        support["order"] = order
    if dimension:
        support["mece_dimension"] = dimension
    if rank_note:
        support["rank_note"] = rank_note
    return {
        "id": ident,
        "anchor": anchor,
        "statement": statement,
        "name": statement,
        "support": support,
    }


def _face(cell):
    parts = str(cell or "").split(".")
    if len(parts) < 2 or not parts[1]:
        return ""
    return parts[1][0]


def _object_index(cell):
    match = CELL_INDEX.search(str(cell or ""))
    if not match:
        return None
    return int(match.group(1))


def build_pyramid(field, root, catalogue=False, flat_min_nodes=FLAT_MIN_NODES):
    """A pyramid the free rebuild can emit. Statements on source nodes are names."""
    root = Path(root)
    rule = load_rule(field, root)
    cap = int(rule.get("depth_cap") or 2)
    table = load_indigenous(root)
    maps = load_maps(field, root)
    nodes = _tagged(maps)
    flat = flat_index_files(maps, min_nodes=flat_min_nodes) if catalogue else []
    admitted, lcc_filed, flat_filed = _select(
        nodes, cap, table, field, {"enabled": catalogue, "flat": flat}
    )
    key = rule["key_line"]
    members = list(key["members"])
    objects = rule.get("objects")
    by_cell = defaultdict(list)
    orphans = []
    for node in admitted:
        cell = node.get("taxonomy_cell") or ""
        if not cell:
            orphans.append(node)
            continue
        by_cell[cell].append(node)

    points = []
    if objects:
        object_members = list(objects["members"])
        object_nodes = {index: [] for index in range(1, len(object_members) + 1)}
        faces = {"M": [], "B": defaultdict(list)}
        for cell, group in by_cell.items():
            face = _face(cell)
            index = _object_index(cell)
            if face == "O" and index in object_nodes:
                object_nodes[index].extend(group)
            elif face == "M":
                faces["M"].extend(group)
            elif face == "B":
                faces["B"][cell].extend(group)
            else:
                orphans.extend(group)
        object_points = []
        for index, name in enumerate(object_members, start=1):
            cell = f"{field}.O.A{index}"
            object_points.append(_cell_point(
                f"{field}.P.1.{index}", f"cell:{cell}", name, object_nodes[index]
            ))
        objects_support = {
            "logic_type": "inductive",
            "plural_noun": "members",
            "mece_dimension": objects.get("dimension") or "",
            "basis": objects["basis"],
            "order": objects["order"],
            "points": object_points,
        }
        if objects.get("rank_note"):
            objects_support["rank_note"] = objects["rank_note"]
        points.append({
            "id": f"{field}.P.1",
            "anchor": f"cell:{field}.O",
            "statement": members[0],
            "name": members[0],
            "support": objects_support,
        })
        for offset, name in enumerate(members[1:], start=2):
            low = name.lower()
            if "pract" in low or "method" in low:
                anchor = f"cell:{field}.M"
                points.append(_cell_point(f"{field}.P.{offset}", anchor, name, faces["M"]))
            elif "bridg" in low:
                bridge_points = []
                for index, cell in enumerate(sorted(faces["B"]), start=1):
                    bridge_points.append(_cell_point(
                        f"{field}.P.{offset}.{index}", f"cell:{cell}", cell, faces["B"][cell]
                    ))
                support = {
                    "logic_type": "inductive",
                    "plural_noun": "members",
                    "points": bridge_points,
                }
                points.append({
                    "id": f"{field}.P.{offset}",
                    "anchor": f"cell:{field}.B",
                    "statement": name,
                    "name": name,
                    "support": support,
                })
            else:
                points.append(_cell_point(f"{field}.P.{offset}", f"cell:{field}.P.{offset}", name, []))
    else:
        used = set()
        for index, name in enumerate(members, start=1):
            cell = f"{field}.O.A{index}"
            used.add(cell)
            points.append(_cell_point(f"{field}.P.{index}", f"cell:{cell}", name, by_cell.get(cell, [])))
        for cell, group in by_cell.items():
            if cell not in used:
                orphans.extend(group)

    support = {
        "logic_type": "inductive",
        "plural_noun": "members",
        "mece_dimension": key.get("dimension") or "",
        "basis": key["basis"],
        "order": key["order"],
        "points": points,
    }
    if key.get("rank_note"):
        support["rank_note"] = key["rank_note"]
    pyramid = {
        "field": field,
        "governing_thought": rule.get("scope") or "",
        "key_line": support,
    }
    meta = {
        "depth_cap": cap,
        "admitted": len(admitted),
        "lcc_filed": lcc_filed,
        "flat_filed": flat_filed,
        "flat_files": flat,
        "orphans": len(orphans),
        "catalogue": bool(catalogue),
    }
    return pyramid, meta


def _split_sizes(issues):
    oversized = []
    undersized = []
    for label in issues["group_size"]:
        match = re.search(r"\((\d+)\)\s*$", label)
        count = int(match.group(1)) if match else 0
        if count > 5:
            oversized.append((count, label))
        else:
            undersized.append((count, label))
    oversized.sort(reverse=True)
    return oversized, undersized


def model_items(pyramid):
    """Formation placements and definition sentences. Leaves are not summarised.

    A group of two to five keeps its members and needs one sentence.
    A larger group needs each member placed, plus the new groups that
    hold them. A group of fewer than two is dissolved, not summarised.
    """
    formation = summaries = 0
    worst = {"children": 0, "id": "", "name": ""}

    def walk(points):
        nonlocal formation, summaries
        for point in points or []:
            kids = ((point.get("support") or {}).get("points"))
            if kids is None:
                continue
            count = len(kids)
            if count > worst["children"]:
                worst["children"] = count
                worst["id"] = point.get("id") or ""
                worst["name"] = point.get("name") or point.get("statement") or ""
            if count > 5:
                formation += count
                extra = min_new_groups(count)
                summaries += extra
                if not is_definition(point.get("statement") or ""):
                    summaries += 1
            elif count < 2:
                formation += count
            elif not is_definition(point.get("statement") or ""):
                summaries += 1
            walk(kids)

    walk((pyramid.get("key_line") or {}).get("points"))
    return {
        "formation": formation,
        "summaries": summaries,
        "items": formation + summaries,
        "worst": worst,
    }


def examine(pyramid, meta):
    """Checker counts plus the model items for this pyramid."""
    issues = minto_issues(pyramid)
    oversized, undersized = _split_sizes(issues)
    priced = model_items(pyramid)
    return {
        "admitted": meta["admitted"],
        "lcc_filed": meta["lcc_filed"],
        "flat_filed": meta["flat_filed"],
        "flat_files": meta["flat_files"],
        "orphans": meta["orphans"],
        "catalogue": meta["catalogue"],
        "loose_topics": len(issues["loose_topics"]),
        "oversized_groups": len(oversized),
        "undersized_groups": len(undersized),
        "missing_basis": len(issues["missing_basis"]),
        "missing_order": len(issues["missing_order"]),
        "template_summaries": len(issues["template_summaries"]),
        "missing_summaries": len(issues["missing_summaries"]),
        "single_child": len(issues["single_child"]),
        "group_size": len(issues["group_size"]),
        "basis_order_mismatch": len(issues["basis_order_mismatch"]),
        "degree_without_rank": len(issues["degree_without_rank"]),
        "mixed_kinds": len(issues["mixed_kinds"]),
        "formation": priced["formation"],
        "summaries": priced["summaries"],
        "items": priced["items"],
        "worst": priced["worst"],
        "worst_groups": [label for _, label in oversized[:8]],
        "checker": {key: len(value) for key, value in issues.items()},
    }


def audit_field(field, root, flat_min_nodes=FLAT_MIN_NODES):
    """The raw rebuild, then the same tree after catalogue filing."""
    root = Path(root)
    literal_pyramid, literal_meta = build_pyramid(field, root, catalogue=False, flat_min_nodes=flat_min_nodes)
    concept_pyramid, concept_meta = build_pyramid(field, root, catalogue=True, flat_min_nodes=flat_min_nodes)
    return {
        "field": field,
        "depth_cap": literal_meta["depth_cap"],
        "literal": examine(literal_pyramid, literal_meta),
        "concept": examine(concept_pyramid, concept_meta),
    }


def claude_usd(items):
    return round(int(items) * USD_PER_THOUSAND / 1000, 6)


def admitted_nodes(field, root):
    """Catalogue-filtered nodes that still need a Minto group. No model call."""
    root = Path(root)
    rule = load_rule(field, root)
    cap = int(rule.get("depth_cap") or 2)
    table = load_indigenous(root)
    maps = load_maps(field, root)
    nodes = _tagged(maps)
    flat = flat_index_files(maps)
    admitted, _lcc, _flat = _select(nodes, cap, table, field, {"enabled": True, "flat": flat})
    rows = []
    for node in admitted:
        cell = node.get("taxonomy_cell") or ""
        if not cell:
            continue
        rows.append({
            "id": node["id"],
            "name": node.get("name") or node["id"],
            "code": str(node.get("code") or ""),
            "cell": cell,
        })
    rows.sort(key=lambda item: (item["cell"], item["code"], item["id"]))
    return {
        "field": field,
        "principle": rule.get("organising_principle") or "",
        "nodes": rows,
    }
