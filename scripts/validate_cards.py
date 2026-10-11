"""Validate lens cards, toolkit cards and maps against schemas/ (Roadmap B6)."""
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT = Path(__file__).resolve().parent.parent
S = {n: Draft202012Validator(json.loads((ROOT / "schemas" / f"{n}.schema.json").read_text())) for n in ("lens_card", "toolkit_card", "map_node")}
errs = 0
def check(kind, items, where):
    global errs
    for it in items:
        for e in S[kind].iter_errors(it):
            errs += 1
            print(f"{where} {it.get('id')}: {e.message}")
for f in sorted((ROOT / "cards" / "lens").glob("*.json")): check("lens_card", json.loads(f.read_text(encoding="utf-8")), f.name)
for f in sorted((ROOT / "cards" / "toolkit").glob("*.json")): check("toolkit_card", json.loads(f.read_text(encoding="utf-8")), f.name)
for f in sorted((ROOT / "maps").glob("*/*.json")): check("map_node", json.loads(f.read_text(encoding="utf-8"))["nodes"], f.name)
print("valid" if not errs else f"{errs} errors"); sys.exit(1 if errs else 0)
