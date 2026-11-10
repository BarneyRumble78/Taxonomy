"""Seed correspondence edges from text already in the pyramids. No model calls.

Two sources:
1. 'uses XX.…' citations in pyramids/XX.md  -> correspondences/seed_uses.json
2. The 'Correspondences' table in pyramids/MA.md -> correspondences/seed_ma.json

The script copies what the pyramids state. It does not add mappings,
conditions or differences: those lists stay empty until someone records them.
Rows it cannot convert are listed under "skipped" with a reason.

Run: python3 scripts/build_correspondences.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from correspondences import NodeIndex, edge_id  # noqa: E402
from crosslinks import FIELDS  # noqa: E402

SEED_DATE = "2026-11-10"
GENERATED_BY = "scripts/build_correspondences.py"
ID = r"(?:%s)\.[OMWB]\.[A-Z]?[0-9]+(?:\.[0-9]+)*[a-z]?" % "|".join(FIELDS)
USES_RE = re.compile(r"\buses\s+(%s(?:(?:,\s*|\s+and\s+)%s)*)" % (ID, ID))
ID_RE = re.compile(ID)
EMPTY_MAPPING = {"objects": [], "methods": [], "warrants": []}


def quote(line, start, end, width=110):
    text = line[max(0, start - width):min(len(line), end + width)].strip()
    return re.sub(r"\s+", " ", text)


def heading_cell(line, field):
    """The field's own cell ID when the line opens with it, else None."""
    match = re.match(r"^[\s\-*#>0-9.]*\**\s*(%s\.[OMWB]\.[A-Z]?[0-9]+(?:\.[0-9]+)*)" % field, line)
    return match.group(1) if match else None


def resolve_cited(cited, index):
    """Resolved node for a cited ID. A trailing letter (A1.2b) is dropped
    when only the unlettered ID is defined, as scripts/check.py does."""
    if index.field_of(cited):
        return cited
    bare = re.sub(r"[a-z]$", "", cited)
    return bare if bare != cited and index.field_of(bare) else None


def build_uses(index):
    edges, skipped = {}, []
    for field in FIELDS:
        path = ROOT / "pyramids" / f"{field}.md"
        rel = f"pyramids/{field}.md"
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in USES_RE.finditer(line):
                for cited in ID_RE.findall(match.group(1)):
                    where = {"file": rel, "line": number, "cited": cited}
                    if cited[:2] == field:
                        skipped.append({**where, "reason": "cites its own field"})
                        continue
                    source = resolve_cited(cited, index)
                    if source is None:
                        skipped.append({**where, "reason": "cited ID does not resolve"})
                        continue
                    cell = heading_cell(line, field)
                    target = cell or field
                    key = edge_id(source, target, "transfer")
                    edge = edges.setdefault(key, {
                        "id": key, "source": source, "target": target,
                        "kind": "transfer", "directed": True,
                        "mapping": json.loads(json.dumps(EMPTY_MAPPING)),
                        "holds_under": [], "breaks_where": [],
                        "status": "asserted",
                        "status_note": "Stated as a 'uses' citation in the pyramid text. Not independently checked.",
                        "provenance": {
                            "origin": "pyramid-uses-citation", "date": SEED_DATE,
                            "generated_by": GENERATED_BY,
                            "target_resolution": "line-heading" if cell else "field-only",
                            "kind_assigned_by": "seed-rule", "locators": []}})
                    edge["provenance"]["locators"].append(
                        {"file": rel, "line": number, "quote": quote(line, match.start(), match.end())})
                    if cited != source:
                        edge["provenance"].setdefault("cited_as", [])
                        if cited not in edge["provenance"]["cited_as"]:
                            edge["provenance"]["cited_as"].append(cited)
    return list(edges.values()), skipped


def ma_node(token, index):
    """Node for one entry in the MA table's 'Cells linked' column."""
    token = re.sub(r"\s*\(.*?\)\s*", "", token).strip()
    if re.fullmatch(r"A[0-9](?:\.[0-9]+)?", token):
        node = f"MA.O.{token}"
    elif re.fullmatch(r"B[0-9]", token):
        node = f"MA.M.{token}"
    elif re.fullmatch(r"[0-9]{2}[A-Z]", token):
        node = f"MSC:{token}xx"
    else:
        return None
    return node if index.field_of(node) else None


def ma_status(text):
    low = text.lower()
    if low.startswith("proved"):
        return "proved"
    if "conjectural" in low:
        return "conjectured"
    if "programme" in low:
        return "programme"
    return "asserted"


def build_ma(index):
    rel = "pyramids/MA.md"
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.startswith("## Correspondences"))
    except StopIteration:
        raise SystemExit("MA.md has no '## Correspondences' section; nothing was written.")
    edges, skipped = [], []
    for offset, line in enumerate(lines[start + 1:], start + 2):
        if line.startswith("## "):
            break
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("Edge", "") or set(cells[0]) <= set("-: "):
            continue
        name, linked, status_text = cells
        tokens = [t.strip() for t in linked.split("↔")]
        nodes = [ma_node(t, index) for t in tokens]
        if None in nodes or len(nodes) < 2:
            bad = [t for t, n in zip(tokens, nodes) if n is None]
            skipped.append({"file": rel, "line": offset, "name": name,
                            "reason": f"not a node: {', '.join(bad) or linked}"})
            continue
        group = "MA-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        for left, right in zip(nodes, nodes[1:]):
            edges.append({
                "id": edge_id(left, right, "shared-formalism"),
                "source": left, "target": right,
                "kind": "shared-formalism", "directed": False,
                "mapping": json.loads(json.dumps(EMPTY_MAPPING)),
                "holds_under": [], "breaks_where": [],
                "status": ma_status(status_text), "status_note": status_text,
                "provenance": {
                    "origin": "ma-correspondence-table", "date": SEED_DATE,
                    "generated_by": GENERATED_BY, "name": name, "group": group,
                    "kind_assigned_by": "seed-rule",
                    "note": "A chain A ↔ B ↔ C is split into adjacent pairs, as written.",
                    "locators": [{"file": rel, "line": offset, "quote": line.strip()}]}})
    return edges, skipped


def write(name, source, edges, skipped):
    out = ROOT / "correspondences" / name
    out.parent.mkdir(exist_ok=True)
    edges = sorted(edges, key=lambda e: e["id"])
    body = {"source": source, "generated_by": GENERATED_BY, "date": SEED_DATE,
            "note": "Generated. Do not edit by hand; rerun the script.",
            "edges": edges, "skipped": skipped}
    out.write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(edges)} edges, {len(skipped)} skipped")


def main():
    index = NodeIndex(ROOT)
    uses, skipped_uses = build_uses(index)
    write("seed_uses.json", "'uses' citations in pyramids/*.md", uses, skipped_uses)
    ma, skipped_ma = build_ma(index)
    write("seed_ma.json", "Correspondences table in pyramids/MA.md", ma, skipped_ma)
    for item in skipped_uses + skipped_ma:
        print("  skipped:", json.dumps(item, ensure_ascii=False))


if __name__ == "__main__":
    main()
