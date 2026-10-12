"""Minto checks for a classification pyramid.

A group has two to five members (Chapter 6, p. 78; Chapter 10, p. 174).
Each group states a basis (cause and effect, parts of a whole, or kinds)
and an order that matches that basis. Degree is allowed only with an
explicit ranking. Summaries define the group. They do not use a blank pattern.
"""
import re

TEMPLATE = re.compile(
    r"^(These|Both are|All are)\b|alike as|is the class that holds|^\s*$",
    re.I,
)
WORD = re.compile(r"[A-Za-z0-9]+(?:[-–][A-Za-z0-9]+)?")
ORDERS = {"time", "structure", "degree"}
BASES = {"cause_effect", "parts", "kinds"}
# cause/effect is a sequence. Parts follow the structure of the whole.
# Kinds are a classification, unless a ranking is stated.
BASIS_ORDERS = {
    "cause_effect": {"time"},
    "parts": {"structure"},
    "kinds": {"structure", "degree"},
}


def _walk_points(points):
    for point in points or []:
        yield point
        yield from _walk_points((point.get("support") or {}).get("points") or [])


def iter_groups(pyramid):
    """Every inductive group, including the key line and the method register."""
    key = pyramid.get("key_line") or {}
    if key.get("points") is not None:
        yield "key line", key
    stack = list(key.get("points") or [])
    while stack:
        point = stack.pop()
        support = point.get("support")
        if support and support.get("points") is not None:
            yield point.get("id") or point.get("statement"), support
            stack.extend(support.get("points") or [])
    methods = pyramid.get("method_line")
    if methods and methods.get("points") is not None:
        yield "methods", methods
        stack = list(methods.get("points") or [])
        while stack:
            point = stack.pop()
            support = point.get("support")
            if support and support.get("points") is not None:
                yield point.get("id") or point.get("statement"), support
                stack.extend(support.get("points") or [])


def _kind_of_name(name):
    """A coarse kind, used only to spot a mixed group of leaves."""
    text = name or ""
    patterns = (
        ("response", r"\b(treatments?|controls?|management|polic(?:y|ies)|protections?|regulations?|remediations?|adaptations?|mitigations?)\b"),
        ("limit", r"\b(standards?|criteri(?:on|a)|objectives?)\b"),
        ("activity", r"\b(industr(?:y|ies)|mining|fishings?|fisher(?:y|ies)|extractions?)\b"),
        ("substance", r"\b(wastes?|pollutants?|emissions?|effluents?|fuels?)\b"),
        ("place", r"\b(oceans?|lakes?|rivers?|seas?|basins?)\b"),
        ("condition", r"\b(climates?|ozone|temperatures?|quality)\b"),
    )
    for kind, pattern in patterns:
        if re.search(pattern, text, re.I):
            return kind
    return "unsorted"


def is_definition(statement):
    """A plain-definition summary: one sentence of at least six words, not a template."""
    text = (statement or "").strip()
    if not text.endswith("."):
        return False
    if TEMPLATE.search(text):
        return False
    return len(WORD.findall(text)) >= 6


def _loose_and_summaries(pyramid):
    """Leaves hung directly on a cell, and group nodes with no definition sentence."""
    loose = []
    missing = []

    def walk(points, parent_anchor):
        for point in points or []:
            support = point.get("support")
            kids = (support or {}).get("points") if support else None
            anchor = str(point.get("anchor") or "")
            if support is not None and not is_definition(point.get("statement") or ""):
                missing.append(point.get("id") or point.get("statement"))
            if parent_anchor.startswith("cell:") and not support:
                loose.append(point.get("id") or point.get("name") or point.get("statement"))
            if kids is not None:
                walk(kids, anchor)

    walk((pyramid.get("key_line") or {}).get("points"), "")
    walk((pyramid.get("method_line") or {}).get("points"), "")
    return loose, missing


def minto_issues(pyramid):
    """Lists of failures. An empty list is a pass for that check."""
    issues = {
        "template_summaries": [],
        "group_size": [],
        "single_child": [],
        "missing_basis": [],
        "missing_order": [],
        "basis_order_mismatch": [],
        "degree_without_rank": [],
        "mixed_kinds": [],
        "loose_topics": [],
        "missing_summaries": [],
    }
    for label, group in iter_groups(pyramid):
        points = group.get("points") or []
        if len(points) == 1:
            issues["single_child"].append(label)
        if not (2 <= len(points) <= 5):
            issues["group_size"].append(f"{label} ({len(points)})")
        basis = group.get("basis")
        order = group.get("order")
        if basis not in BASES:
            issues["missing_basis"].append(label)
        if order not in ORDERS:
            issues["missing_order"].append(label)
        elif basis in BASIS_ORDERS and order not in BASIS_ORDERS[basis]:
            issues["basis_order_mismatch"].append(f"{label}: {basis}/{order}")
        if order == "degree" and not (group.get("rank_note") or "").strip():
            issues["degree_without_rank"].append(label)
        leaves = [point for point in points if str(point.get("anchor") or "").startswith("node:")]
        if len(leaves) >= 2:
            kinds = {_kind_of_name(point.get("name") or point.get("statement")) for point in leaves}
            kinds.discard("unsorted")
            if len(kinds) > 1:
                issues["mixed_kinds"].append(f"{label}: {sorted(kinds)}")
    for point in _walk_points((pyramid.get("key_line") or {}).get("points")):
        if point.get("support") and TEMPLATE.search(point.get("statement") or ""):
            issues["template_summaries"].append(point.get("id") or point.get("statement"))
    methods = pyramid.get("method_line") or {}
    for point in _walk_points(methods.get("points")):
        if point.get("support") and TEMPLATE.search(point.get("statement") or ""):
            issues["template_summaries"].append(point.get("id") or point.get("statement"))
    loose, missing = _loose_and_summaries(pyramid)
    issues["loose_topics"] = loose
    issues["missing_summaries"] = missing
    return issues


def minto_counts(pyramid):
    issues = minto_issues(pyramid)
    return {key: len(value) for key, value in issues.items()}
