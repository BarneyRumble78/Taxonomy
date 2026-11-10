"""Rosetta layer: formal cores and their bindings in each field. No model calls.

A formal core is one mathematical structure with named roles, assumptions and
a guarantee. A binding says what plays each role in one field, which
assumptions that field meets, and where the analogy breaks.

Operations:
  find(text)                 cores and bindings whose words match
  translate(core, a, b)      role-by-role mapping between two fields, with differences
  holes(core, field)         fields where a core has no binding: open questions
  lineage_distance(x, y)     shortest path through pyramid tree, cores and edges
  assumption_distance(p, q)  1 - Jaccard overlap of the assumptions two bindings meet
  derived_edges()            correspondence edges implied by shared cores

Every output is a lead to check, not a finding. Data: rosetta/cores.json.

    python3 engine/v3/rosetta.py translate RC-diffusion PH EC
    python3 engine/v3/rosetta.py holes --core RC-diffusion
    python3 engine/v3/rosetta.py find "random walk"
    python3 engine/v3/rosetta.py distance PH.O.A5.1 EC.O.A1.2
"""
import argparse
import json
import re
import sys
from collections import deque
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from correspondences import NodeIndex, edge_id, load_edges  # noqa: E402
from crosslinks import FIELDS  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = "rosetta/cores.json"
MET = ("y", "~", "n", "?")
MATURITY = ("standard", "specialist", "speculative")
CORE_ID_RE = re.compile(r"^RC-[a-z0-9-]+$")
SEED_DATE = "2026-11-10"


class RosettaError(Exception):
    """The Rosetta data is missing or malformed, or a query names nothing."""


def load(root=ROOT):
    """All formal cores. Raises RosettaError if the file is missing or bad."""
    path = Path(root) / DATA_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise RosettaError(f"{DATA_FILE}: cannot read: {error}") from error
    if not isinstance(data, dict) or not isinstance(data.get("cores"), list):
        raise RosettaError(f"{DATA_FILE}: expected an object with a 'cores' list")
    return data["cores"]


def core_by_id(cores, core_id):
    for core in cores:
        if core["id"] == core_id:
            return core
    raise RosettaError(f"unknown core {core_id}")


def bindings_in(core, field):
    return [b for b in core["bindings"] if b["field"] == field]


def one_binding(core, field, tool=None):
    """The binding of a core in a field. A tool substring picks among several."""
    found = bindings_in(core, field)
    if tool:
        found = [b for b in found if tool.lower() in b["tool"].lower()]
    if not found:
        raise RosettaError(f"{core['id']} has no binding in {field}" + (f" matching '{tool}'" if tool else ""))
    if len(found) > 1:
        names = "; ".join(b["tool"] for b in found)
        raise RosettaError(f"{core['id']} has {len(found)} bindings in {field}; name one: {names}")
    return found[0]


# ---------------------------------------------------------------- validation

def check(root=ROOT):
    """Problems in rosetta/cores.json. An empty list means clean."""
    root = Path(root)
    if not (root / DATA_FILE).is_file():
        return [f"{DATA_FILE} not found"]
    try:
        cores = load(root)
    except RosettaError as error:
        return [str(error)]
    from jsonschema import Draft202012Validator
    schema = json.loads((root / "schemas" / "formal_core.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    index = NodeIndex(root)
    problems, seen = [], set()
    if not cores:
        problems.append("no cores")
    for core in cores:
        label = core.get("id", "<no id>") if isinstance(core, dict) else "<not an object>"
        errors = [f"{label}: schema: {'/'.join(str(p) for p in e.path) or '(root)'}: {e.message}"
                  for e in validator.iter_errors(core)]
        if errors:
            problems.extend(errors)
            continue
        if label in seen:
            problems.append(f"{label}: duplicate core id")
        seen.add(label)
        if index.field_of(core["ma_node"]) != "MA":
            problems.append(f"{label}: ma_node {core['ma_node']} is not a mathematics node")
        roles = set(core["roles"])
        assumption_ids = [a["id"] for a in core["assumptions"]]
        if len(assumption_ids) != len(set(assumption_ids)):
            problems.append(f"{label}: duplicate assumption id")
        tools = set()
        for binding in core["bindings"]:
            where = f"{label} / {binding['field']} / {binding['tool']}"
            owner = index.field_of(binding["cell"])
            if owner is None:
                problems.append(f"{where}: cell {binding['cell']} does not resolve")
            elif owner != binding["field"]:
                problems.append(f"{where}: cell {binding['cell']} belongs to {owner}")
            if set(binding["roles"]) != roles:
                odd = sorted(set(binding["roles"]) ^ roles)
                problems.append(f"{where}: roles differ from the core: {', '.join(odd)}")
            if set(binding["assumptions_met"]) != set(assumption_ids):
                odd = sorted(set(binding["assumptions_met"]) ^ set(assumption_ids))
                problems.append(f"{where}: assumptions_met differs from the core: {', '.join(odd)}")
            key = (binding["field"], binding["cell"], binding["tool"])
            if key in tools:
                problems.append(f"{where}: duplicate binding")
            tools.add(key)
            if binding["field"] == "IK" and binding["maturity"] != "speculative":
                problems.append(f"{where}: IK bindings stay provisional (maturity speculative)")
    return problems


# ------------------------------------------------------------------- queries

def find(text, cores=None):
    """Cores and bindings whose text contains every word of the query."""
    cores = load() if cores is None else cores
    words = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 1]
    if not words:
        raise RosettaError("empty query")
    hits = []
    for core in cores:
        core_text = " ".join([core["id"], core["name"], core["structure"], core["guarantee"],
                              " ".join(core["roles"].values())]).lower()
        if all(w in core_text for w in words):
            hits.append({"core": core["id"], "name": core["name"], "matched": "core",
                         "fields": sorted({b["field"] for b in core["bindings"]})})
        for binding in core["bindings"]:
            text_b = " ".join([binding["tool"], " ".join(binding["roles"].values())]).lower()
            if all(w in text_b for w in words):
                hits.append({"core": core["id"], "name": core["name"], "matched": "binding",
                             "field": binding["field"], "cell": binding["cell"], "tool": binding["tool"]})
    return hits


def translate(core, source, target):
    """Role-by-role mapping between two bindings of one core, with differences.

    source and target are binding objects. The differences are the product:
    each one is a place where a technique may not carry over.
    """
    assumptions = []
    for item in core["assumptions"]:
        s, t = source["assumptions_met"][item["id"]], target["assumptions_met"][item["id"]]
        if s == t == "y":
            verdict = "holds in both"
        elif "?" in (s, t):
            verdict = "not known"
        elif s == t:
            verdict = "same limitation in both"
        else:
            verdict = "differs"
        assumptions.append({"id": item["id"], "text": item["text"], "source": s, "target": t, "verdict": verdict})
    return {
        "core": core["id"], "name": core["name"], "structure": core["structure"],
        "ma_node": core["ma_node"], "guarantee": core["guarantee"],
        "source": {"field": source["field"], "cell": source["cell"], "tool": source["tool"], "maturity": source["maturity"]},
        "target": {"field": target["field"], "cell": target["cell"], "tool": target["tool"], "maturity": target["maturity"]},
        "roles": [{"role": role, "meaning": meaning, "source": source["roles"][role], "target": target["roles"][role]}
                  for role, meaning in core["roles"].items()],
        "assumptions": assumptions,
        "breaks_in_source": source["breaks"], "breaks_in_target": target["breaks"],
        "guarantee_carries": all(a["verdict"] == "holds in both" for a in assumptions),
        "status": "generated-unverified",
    }


def holes(cores=None, core_id=None, field=None):
    """Fields where a core has no binding. Each is a question, not a claim.

    An empty cell may mean the transfer was never tried, or that it was tried
    and failed, or that this seed simply has not recorded it.
    """
    cores = load() if cores is None else cores
    if core_id:
        cores = [core_by_id(cores, core_id)]
    if field and field not in FIELDS:
        raise RosettaError(f"unknown field {field}")
    out = []
    for core in cores:
        bound = {b["field"] for b in core["bindings"]}
        for code in FIELDS:
            if code in bound or code == "MA" or (field and code != field):
                continue
            out.append({
                "core": core["id"], "name": core["name"], "field": code,
                "known_in": sorted(bound),
                "ask_roles": [f"In {code}, what would play the role of '{role}' ({meaning})?"
                              for role, meaning in core["roles"].items()],
                "ask_assumptions": [f"In {code}, does this hold? {a['text']}" for a in core["assumptions"]],
                "if_all_hold": core["guarantee"],
                "status": "open question",
            })
    return out


def matrix(cores=None):
    """core id -> {field: number of bindings}. The stone at a glance."""
    cores = load() if cores is None else cores
    table = {}
    for core in cores:
        row = {}
        for binding in core["bindings"]:
            row[binding["field"]] = row.get(binding["field"], 0) + 1
        table[core["id"]] = row
    return table


# ----------------------------------------------------------------- distances

def met_set(binding):
    """Assumptions a binding normally meets (code y)."""
    return {key for key, value in binding["assumptions_met"].items() if value == "y"}


def assumption_distance(core_a, binding_a, core_b, binding_b):
    """1 - Jaccard overlap of assumptions met. Range 0 to 1.

    Bindings of different cores share no assumptions, so their distance is 1.
    Two bindings that meet no assumptions at all are at distance 0 of each
    other only when they belong to the same core. Jaccard distance is a metric.
    """
    if core_a["id"] != core_b["id"]:
        return 1.0
    a, b = met_set(binding_a), met_set(binding_b)
    if not a and not b:
        return 0.0
    return 1.0 - len(a & b) / len(a | b)


def _parents(node):
    """Tree parent of a node: sub-cell -> cell -> field -> root."""
    if node == "K":
        return None
    if node in FIELDS:
        return "K"
    if node.startswith("RC-") or ":" in node:
        return None
    parts = node.split(".")
    if parts[0] not in FIELDS or len(parts) < 3:
        return None  # not a cell ID: no tree parent
    if len(parts) == 3:
        return parts[0]
    return ".".join(parts[:-1])


class Graph:
    """Undirected graph of tree links, core hubs and correspondence edges."""

    def __init__(self, root=ROOT, cores=None, use_edges=True, use_cores=True, exclude_field_edges=False):
        self.links = {}
        self.kinds = {}
        self.index = NodeIndex(root)
        cores = load(root) if cores is None else cores
        if use_cores:
            for core in cores:
                self._link(core["id"], core["ma_node"], "core-to-mathematics")
                for binding in core["bindings"]:
                    self._link(core["id"], binding["cell"], "binding")
        if use_edges:
            for edge in load_edges(root):
                if edge["provenance"]["origin"] == "formal-core":
                    continue  # already represented by the core hub
                if exclude_field_edges and (edge["source"] in FIELDS or edge["target"] in FIELDS):
                    continue
                self._link(edge["source"], edge["target"], "correspondence")
        for node in list(self.links):
            self._climb(node)

    def _link(self, a, b, kind):
        self.links.setdefault(a, set()).add(b)
        self.links.setdefault(b, set()).add(a)
        self.kinds[frozenset((a, b))] = kind

    def _parent(self, node):
        return self.index.map_parent(node) if ":" in node else _parents(node)

    def _climb(self, node):
        """Link a node to its ancestors: map parents, then cell, field and root."""
        parent = self._parent(node)
        while parent:
            self._link(node, parent, "map" if ":" in node else "tree")
            node, parent = parent, self._parent(parent)

    def path(self, a, b):
        """Shortest path as a list of nodes. Raises if either is unknown."""
        for node in (a, b):
            if node not in self.links and self.index.field_of(node) is not None:
                self._climb(node)
            if node not in self.links:
                raise RosettaError(f"{node} is not a known node")
        previous, queue = {a: None}, deque([a])
        while queue:
            here = queue.popleft()
            if here == b:
                out = []
                while here is not None:
                    out.append(here)
                    here = previous[here]
                return out[::-1]
            for there in sorted(self.links[here]):
                if there not in previous:
                    previous[there] = here
                    queue.append(there)
        raise RosettaError(f"no path between {a} and {b}")

    def distance(self, a, b):
        return len(self.path(a, b)) - 1

    def explain(self, a, b):
        nodes = self.path(a, b)
        return [{"from": x, "to": y, "via": self.kinds[frozenset((x, y))]} for x, y in zip(nodes, nodes[1:])]


def lineage_distance(a, b, root=ROOT, **options):
    """Number of links on the shortest path between two nodes.

    Links: tree (sub-cell, cell, field, root), map (a map node to its parent,
    and a top map node to its cell), core hubs and correspondence edges, all
    undirected with weight 1. Shortest-path length on an undirected
    graph is a metric: zero only for identical nodes, symmetric, and it obeys
    the triangle inequality. Without cores or edges every pair of cells in
    different fields is joined only through the root.
    """
    return Graph(root, **options).distance(a, b)


# ------------------------------------------------------------- derived edges

def derived_edges(cores=None):
    """Correspondence edges implied by two bindings sharing one core.

    Bindings in the same cell are skipped. Edges are undirected,
    kind shared-formalism, status generated-unverified.
    """
    cores = load() if cores is None else cores
    edges = {}
    for core in cores:
        for left, right in combinations(core["bindings"], 2):
            if left["cell"] == right["cell"]:
                continue
            left, right = sorted((left, right), key=lambda b: (b["cell"], b["tool"]))
            view = translate(core, left, right)
            key = edge_id(left["cell"], right["cell"], "shared-formalism")
            if key in edges:
                edges[key]["provenance"]["note"] += f" Also linked through {core['id']}."
                continue
            edges[key] = {
                "id": key, "source": left["cell"], "target": right["cell"],
                "kind": "shared-formalism", "directed": False,
                "mapping": {
                    "objects": [{"source": r["source"], "target": r["target"], "note": r["role"]} for r in view["roles"]],
                    "methods": [{"source": left["tool"], "target": right["tool"]}],
                    "warrants": []},
                "holds_under": [a["text"] for a in view["assumptions"] if a["verdict"] == "holds in both"],
                "breaks_where": (
                    [f"{a['text']} ({left['field']}: {a['source']}; {right['field']}: {a['target']})"
                     for a in view["assumptions"] if a["verdict"] != "holds in both"]
                    + [f"{left['field']}: {text}" for text in left["breaks"]]
                    + [f"{right['field']}: {text}" for text in right["breaks"]]),
                "status": "generated-unverified",
                "provenance": {
                    "origin": "formal-core", "date": SEED_DATE,
                    "generated_by": "engine/v3/rosetta.py from rosetta/cores.json",
                    "name": core["name"], "group": core["id"],
                    "note": f"Both cells bind {core['id']} (mathematics node {core['ma_node']}).",
                    "locators": []}}
    return sorted(edges.values(), key=lambda e: e["id"])


# ----------------------------------------------------------------------- CLI

def main(argv=None):
    parser = argparse.ArgumentParser(prog="rosetta", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("find", help="search cores and bindings")
    p.add_argument("text")
    p = sub.add_parser("translate", help="map one field's tool onto another's")
    p.add_argument("core"), p.add_argument("source"), p.add_argument("target")
    p.add_argument("--source-tool"), p.add_argument("--target-tool")
    p = sub.add_parser("holes", help="fields where a core is not yet bound")
    p.add_argument("--core"), p.add_argument("--field")
    sub.add_parser("matrix", help="bindings per core and field")
    p = sub.add_parser("distance", help="lineage distance between two nodes")
    p.add_argument("a"), p.add_argument("b")
    args = parser.parse_args(argv)
    try:
        cores = load()
        if args.command == "find":
            out = find(args.text, cores)
        elif args.command == "translate":
            core = core_by_id(cores, args.core)
            out = translate(core, one_binding(core, args.source, args.source_tool),
                            one_binding(core, args.target, args.target_tool))
        elif args.command == "holes":
            out = holes(cores, args.core, args.field)
        elif args.command == "matrix":
            out = matrix(cores)
        else:
            graph = Graph(cores=cores)
            out = {"a": args.a, "b": args.b, "distance": graph.distance(args.a, args.b),
                   "path": graph.explain(args.a, args.b)}
    except RosettaError as error:
        print(f"rosetta: {error}", file=sys.stderr)
        return 2
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
