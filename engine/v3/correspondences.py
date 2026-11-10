"""Correspondence edges: load, validate and index. No model calls.

An edge links two nodes and records the mapping, the conditions under which
it holds and the places where it breaks. Schema:
schemas/correspondence_edge.schema.json. Data: correspondences/*.json, each
file an object with an "edges" list.

Errors are raised or returned as problems. Nothing here returns an empty
result in place of a failure.
"""
import hashlib
import json
import re
from pathlib import Path

from crosslinks import FIELDS, defined_ids

SCHEMA_FILE = "schemas/correspondence_edge.schema.json"
DATA_DIR = "correspondences"
CELL_RE = re.compile(
    r"^(%s)\.([OMWB])\.([A-Z]?[0-9]+(?:\.[0-9]+)*)$" % "|".join(FIELDS)
)
TOOLKIT_RE = re.compile(r"^(%s)\.TK\.[0-9A-Za-z.]+$" % "|".join(FIELDS))
MAP_RE = re.compile(r"^[A-Za-z0-9]+:.+$")
MA_SHORT_RE = re.compile(r"^- ([AB][0-9]+(?:\.[0-9]+)?)\b", re.M)


class CorrespondenceError(Exception):
    """A correspondence file could not be read or is malformed."""


def edge_id(source, target, kind):
    """Deterministic stable ID from the edge's defining triple."""
    digest = hashlib.sha1(f"{source}|{target}|{kind}".encode("utf-8"))
    return "CE-" + digest.hexdigest()[:10]


def ma_short_cells(root):
    """MA writes its sub-cells in short form ('- A2.5 Number and counting').

    Returns the full IDs those lines imply, such as MA.O.A2.5 and MA.M.B3.
    """
    path = Path(root) / "pyramids" / "MA.md"
    if not path.exists():
        return set()
    found = set()
    for label in MA_SHORT_RE.findall(path.read_text(encoding="utf-8")):
        face = "O" if label.startswith("A") else "M"
        found.add(f"MA.{face}.{label}")
    return found


class NodeIndex:
    """Resolves node IDs. Map and toolkit files are read only when needed."""

    def __init__(self, root):
        self.root = Path(root)
        self.cells = defined_ids(self.root) | ma_short_cells(self.root)
        self._map_field = None
        self._toolkit = None

    def _load_maps(self):
        self._map_field = {}
        folder = self.root / "maps"
        for path in sorted(folder.glob("*/*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            nodes = data["nodes"] if isinstance(data, dict) else data
            for node in nodes:
                self._map_field.setdefault(node["id"], path.parent.name)

    def _load_toolkit(self):
        self._toolkit = set()
        for path in sorted((self.root / "cards" / "toolkit").glob("*.json")):
            for card in json.loads(path.read_text(encoding="utf-8")):
                self._toolkit.add(card["id"])

    def field_of(self, node):
        """Field code that owns the node, or None when it does not resolve."""
        if node in FIELDS:
            return node
        match = CELL_RE.match(node)
        if match:
            if node in self.cells:
                return match.group(1)
            prefix = node + "."
            if any(item.startswith(prefix) for item in self.cells):
                return match.group(1)
            return None
        match = TOOLKIT_RE.match(node)
        if match:
            if self._toolkit is None:
                self._load_toolkit()
            return match.group(1) if node in self._toolkit else None
        if MAP_RE.match(node):
            if self._map_field is None:
                self._load_maps()
            return self._map_field.get(node)
        return None


def load_schema(root):
    return json.loads((Path(root) / SCHEMA_FILE).read_text(encoding="utf-8"))


def load_file(path):
    """Edges from one file. Raises CorrespondenceError on a bad file."""
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise CorrespondenceError(f"{path.name}: cannot read: {error}") from error
    if not isinstance(data, dict) or not isinstance(data.get("edges"), list):
        raise CorrespondenceError(f"{path.name}: expected an object with an 'edges' list")
    return data["edges"]


def load_edges(root, include_retired=False):
    """All edges under correspondences/. Raises if the folder is missing."""
    folder = Path(root) / DATA_DIR
    if not folder.is_dir():
        raise CorrespondenceError(f"{DATA_DIR}/ not found under {root}")
    edges = []
    for path in sorted(folder.glob("*.json")):
        for edge in load_file(path):
            if include_retired or not edge.get("retired"):
                edges.append(edge)
    return edges


def edge_problems(edge, index, validator):
    """Problems with one edge: schema first, then the semantic rules."""
    label = edge.get("id", "<no id>") if isinstance(edge, dict) else "<not an object>"
    problems = [
        f"{label}: schema: {'/'.join(str(p) for p in err.path) or '(root)'}: {err.message}"
        for err in validator.iter_errors(edge)
    ]
    if problems:
        return problems
    source, target = edge["source"], edge["target"]
    if source == target:
        problems.append(f"{label}: source and target are the same node")
    for role, node in (("source", source), ("target", target)):
        if index.field_of(node) is None:
            problems.append(f"{label}: {role} {node} does not resolve to a known node")
    origin = edge["provenance"]["origin"]
    status = edge["status"]
    if origin in ("transfer-operator", "formal-core") and status != "generated-unverified":
        problems.append(f"{label}: a {origin} edge must be generated-unverified")
    if status == "generated-unverified" and origin not in ("transfer-operator", "formal-core", "manual"):
        problems.append(f"{label}: generated-unverified needs origin transfer-operator, formal-core or manual")
    if status in ("proved", "programme", "conjectured", "asserted") and not edge["provenance"]["locators"]:
        problems.append(f"{label}: status {status} needs at least one locator")
    for locator in edge["provenance"]["locators"]:
        if not (index.root / locator["file"]).is_file():
            problems.append(f"{label}: locator file {locator['file']} not found")
    return problems


def check(root):
    """Problems across all correspondence files. An empty list means clean."""
    from jsonschema import Draft202012Validator

    root = Path(root)
    folder = root / DATA_DIR
    if not folder.is_dir():
        return [f"{DATA_DIR}/ not found"]
    validator = Draft202012Validator(load_schema(root))
    index = NodeIndex(root)
    problems, seen = [], {}
    files = sorted(folder.glob("*.json"))
    if not files:
        problems.append(f"{DATA_DIR}/ holds no edge files")
    for path in files:
        try:
            edges = load_file(path)
        except CorrespondenceError as error:
            problems.append(str(error))
            continue
        for edge in edges:
            problems.extend(f"{path.name}: {p}" for p in edge_problems(edge, index, validator))
            if isinstance(edge, dict) and "id" in edge:
                if edge["id"] in seen:
                    problems.append(f"{path.name}: {edge['id']} also appears in {seen[edge['id']]}")
                seen[edge["id"]] = path.name
    return problems


def neighbours(edges):
    """node -> list of (other node, edge). Undirected edges go both ways."""
    table = {}
    for edge in edges:
        table.setdefault(edge["source"], []).append((edge["target"], edge))
        if not edge["directed"]:
            table.setdefault(edge["target"], []).append((edge["source"], edge))
    return table


def field_pairs(edges, index):
    """Count of edges per (source field, target field)."""
    counts = {}
    for edge in edges:
        pair = (index.field_of(edge["source"]), index.field_of(edge["target"]))
        counts[pair] = counts.get(pair, 0) + 1
    return counts
