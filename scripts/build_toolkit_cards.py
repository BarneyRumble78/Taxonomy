"""Build cards/toolkit/MA.json from cards/toolkit/MA_two_digit_src.py, validating
signatures against signatures/vocabulary.json and nodes against maps/MA/msc2020.json."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "cards" / "toolkit"))
from MA_two_digit_src import T
vocab = json.loads((ROOT / "signatures" / "vocabulary.json").read_text())["facets"]
nodes = {n["code"]: n for n in json.loads((ROOT / "maps" / "MA" / "msc2020.json").read_text(encoding="utf-8"))["nodes"]}
cards, errs = [], []
for code, (solves, sig, tools, cross) in T.items():
    node = nodes.get(f"{code}-XX")
    if not node:
        errs.append(f"{code}: no MSC node"); continue
    for f, vals in sig.items():
        for v in vals:
            if v not in vocab.get(f, []): errs.append(f"{code}: bad signature {f}={v}")
    cards.append({"id": f"MA.TK.{code}", "field": "MA", "node": node["id"], "name": node["name"],
                  "taxonomy_cell": node.get("taxonomy_cell"), "solves": solves, "signature": sig,
                  "tools": [{"name": n, "does": d, "hypotheses": h} for n, d, h in tools],
                  "cross_uses": cross, "status": "draft"})
missing = [c[:2] for c in nodes if c.endswith("-XX") and c[:2] not in T]
if missing: errs.append(f"two-digit classes without a card: {missing}")
(ROOT / "cards" / "toolkit" / "MA.json").write_text(json.dumps(cards, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(cards)} toolkit cards; {sum(len(c['tools']) for c in cards)} tools")
print("\n".join(errs) or "valid")
sys.exit(1 if errs else 0)
