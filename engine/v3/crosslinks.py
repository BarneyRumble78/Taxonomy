"""Cross-link check for pyramid citations and route files. No model calls.

Defined IDs follow scripts/check.py: an ID is defined in the pyramid file
whose stem is that field. A citation resolves when the ID is defined, or
when a longer defined ID extends it. Route destinations must be field codes.
"""
import json
import re
from pathlib import Path

FIELDS = (
    "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK"
).split()
ID_RE = re.compile(
    r"\b(%s)\.([OMWB])\.([A-Z]?[0-9]+(?:\.[0-9]+)*)" % "|".join(FIELDS)
)
USES_RE = re.compile(
    r"\buses\s+([A-Z]{2}\.[OMWB]\.[A-Z]?[0-9]+(?:\.[0-9]+)*)"
)
BRIDGES = {f"MA.B.C{number}" for number in range(1, 6)}


def defined_ids(root):
    """IDs written in the pyramid whose file stem is the field code."""
    root = Path(root)
    defined = set(BRIDGES)
    folder = root / "pyramids"
    if not folder.exists():
        return defined
    for path in sorted(folder.glob("*.md")):
        code = path.stem
        text = path.read_text(encoding="utf-8")
        for match in ID_RE.finditer(text):
            if match.group(1) == code:
                defined.add(match.group(0))
    return defined


def use_edges(root):
    """(source stem, cited id) for each 'uses XX.…' citation."""
    root = Path(root)
    edges = []
    folder = root / "pyramids"
    if not folder.exists():
        return edges
    for path in sorted(folder.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in USES_RE.finditer(text):
            edges.append((path.stem, match.group(1).rstrip(".")))
    return edges


def _resolves(cited, defined):
    if cited in defined:
        return True
    prefix = cited + "."
    return any(item.startswith(prefix) for item in defined)


def dangling_uses(root):
    """Citations that do not resolve. Unknown field codes dangle."""
    defined = defined_ids(root)
    problems = []
    for source, cited in use_edges(root):
        if not _resolves(cited, defined):
            problems.append(f"{source} cites undefined {cited}")
    return problems


def route_problems(root):
    """Route files and shared-queue homes whose field code is not a field."""
    root = Path(root)
    known = set(FIELDS)
    problems = []
    queue = root / "pyramids" / "queues"
    if not queue.exists():
        return problems
    for path in sorted(queue.glob("*.routes.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            field = json.loads(line).get("field")
            if field not in known:
                problems.append(f"{path.name} routes to unknown field {field}")
    for path in sorted(queue.glob("shared_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data.get("rows") or data.get("conflict_sample") or []:
            home = row.get("home")
            if home and home not in known:
                problems.append(f"{path.name} homes unknown field {home}")
    return problems


def check(root):
    """Dangling uses-citations and unknown route destinations."""
    dangling = dangling_uses(root)
    routes = route_problems(root)
    return {"dangling": dangling, "routes": routes}
