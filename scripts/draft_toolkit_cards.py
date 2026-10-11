"""Draft toolkit cards for a field's map nodes with a model (Roadmap D2-D4).

  python3 scripts/draft_toolkit_cards.py --field MA --level 2 --batch 12
  TAXONOMY_LLM=anthropic TAXONOMY_ADJUDICATE_PAID=1 python3 scripts/draft_toolkit_cards.py --field MA --level 2
Resumable: writes cards/toolkit/<FIELD>_L<level>.json and skips nodes already drafted.
Every card is validated against the signature vocabulary; status is "draft" until reviewed.
"""
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from llm import get_llm
from core import VOCAB, clean_signature

ap = argparse.ArgumentParser()
ap.add_argument("--field", default="MA"); ap.add_argument("--level", type=int, default=2)
ap.add_argument("--batch", type=int, default=12); ap.add_argument("--limit", type=int, default=0)
a = ap.parse_args()
nodes = [n for f in sorted((ROOT / "maps" / a.field).glob("*.json")) for n in json.loads(f.read_text(encoding="utf-8"))["nodes"] if n["level"] == a.level]
out = ROOT / "cards" / "toolkit" / f"{a.field}_L{a.level}.json"
done = {c["node"]: c for c in json.loads(out.read_text(encoding="utf-8"))} if out.exists() else {}
todo = [n for n in nodes if n["id"] not in done]
if a.limit: todo = todo[:a.limit]
llm = get_llm()
for i in range(0, len(todo), a.batch):
    part = todo[i:i + a.batch]
    prompt = f"""Write toolkit cards for these subfields of {a.field}. A toolkit card says what kinds of problem the subfield solves, stated WITHOUT subject matter, so that people from other fields can recognise their problem in it.
Subfields: {json.dumps([{"id": n["id"], "code": n["code"], "name": n["name"]} for n in part])}
Signature facets and allowed values: {json.dumps(VOCAB)}
For each, give 1-4 flagship tools (theorems, methods, algorithms) with their hypotheses stated precisely. Name famous uses outside the subfield only if you are confident; otherwise leave empty.
Return only JSON: {{"cards": [{{"node": "id", "solves": [""], "signature": {{facet: [values]}}, "tools": [{{"name": "", "does": "", "hypotheses": [""]}}], "inputs": [""], "outputs": [""], "cross_uses": [""]}}]}}"""
    for c in llm(prompt, max_tokens=8000).get("cards", []):
        n = next((x for x in part if x["id"] == c.get("node")), None)
        if not n: continue
        done[n["id"]] = {"id": f"{a.field}.TK.{n['code']}", "field": a.field, "node": n["id"], "name": n["name"],
                         "taxonomy_cell": n.get("taxonomy_cell"), "solves": c.get("solves", []),
                         "signature": clean_signature(c.get("signature")), "tools": c.get("tools", []),
                         "inputs": c.get("inputs", []), "outputs": c.get("outputs", []), "cross_uses": c.get("cross_uses", []),
                         "status": "draft", "notes": "model-drafted; needs specialist review"}
    out.write_text(json.dumps(list(done.values()), indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(done)}/{len(nodes)} drafted")
