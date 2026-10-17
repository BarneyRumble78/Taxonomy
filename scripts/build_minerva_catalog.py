"""Section catalog for the Worker. Full pyramids stay out of the bundle.

Depth 0 and 1 only: the key line and its sections. Leaf nodes are in the
static JSON published with the site, and optionally in R2 or KV.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "engine" / "minerva_catalog.json"


def _sections(points, depth, out):
    for point in points or []:
        if depth <= 1:
            out.append({
                "id": point.get("id"),
                "statement": str(point.get("statement") or point.get("name") or "")[:400],
                "keywords": list(point.get("keywords") or [])[:12],
                "depth": depth,
            })
        support = point.get("support") or {}
        _sections(support.get("points"), depth + 1, out)


def build():
    site = json.loads((ROOT / "site" / "site_data.json").read_text(encoding="utf-8"))
    fields = []
    for path in sorted((ROOT / "pyramids").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        check = data.get("field_check") or {}
        sections = []
        _sections((data.get("key_line") or {}).get("points"), 0, sections)
        code = path.stem
        fields.append({
            "code": code,
            "name": (site.get("p") or {}).get(code, {}).get("name", code),
            "governing_thought": data.get("governing_thought") or "",
            "holds": check.get("holds"),
            "misplaced": check.get("misplaced"),
            "note": (check.get("note") or "")[:280],
            "format": "legacy" if check.get("holds") is None else "minto",
            "sections": sections,
        })
    return {"version": "3", "built": "2026-10-17", "fields": fields}


def main():
    catalog = build()
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} fields={len(catalog['fields'])} bytes={OUT.stat().st_size}")
    return catalog


if __name__ == "__main__":
    main()
