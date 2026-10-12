#!/usr/bin/env python3
"""Render pyramids/queues/<FIELD>.groups.json to pyramids/<FIELD>_minto_groups.md. No model call."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def walk(p, depth, out):
    s = p.get("support") or {}
    pad = "  " * depth
    out.append(f"{pad}- **{p.get('statement') or p.get('name')}**" if s.get("points") else f"{pad}- {p.get('statement') or p.get('name')}")
    if s.get("points"):
        meta = f"basis: {s.get('basis')}, order: {s.get('order')}"
        if s.get("rank_note"):
            meta += f". {s['rank_note']}"
        out.append(f"{pad}  _{meta}_")
        for c in s["points"]:
            walk(c, depth + 1, out)

def main(field):
    d = json.loads((ROOT / "pyramids" / "queues" / f"{field}.groups.json").read_text())
    out = [f"# {field} Minto groups", ""]
    for cell in d["cells"]:
        out.append(f"## {cell['id']}")
        walk(cell, 0, out)
        out.append("")
    (ROOT / "pyramids" / f"{field}_minto_groups.md").write_text("\n".join(out) + "\n")

if __name__ == "__main__":
    for f in sys.argv[1:]:
        main(f)
