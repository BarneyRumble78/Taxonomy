"""Build level-1 toolkit cards from hand-written sources in cards/toolkit/src_l1/<FIELD>.py.

  python3 scripts/build_l1_cards.py            # all fields with a source file
Each source defines T = {code: (solves, signature, tools, inputs, outputs)} or C("note") for a
catalogue node that carries no tools. A source may set D = C("note") as the stated default for unlisted nodes. Signature values are space-separated strings per facet.
Fails loudly if a node is missing, a key is unknown or a signature value is outside the vocabulary.
Writes cards/toolkit/<FIELD>_L1.json. Every card is status "draft".
"""
import json, sys, runpy
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
VOCAB = json.loads((ROOT / "signatures" / "vocabulary.json").read_text(encoding="utf-8"))["facets"]
INDEX = json.loads((ROOT / "maps" / "index.json").read_text(encoding="utf-8"))
BY, DATE = "claude-fable-5-2", "2026-11-11"
IK_NOTE = "Placement and content are provisional and await Māori-led and Indigenous-led review. Tools are left empty on purpose."

def C(note):
    return (["locate work on this subject within the field's catalogue"], {"task": "classify"}, [], [], [], note)

fails = 0
for src in sorted((ROOT / "cards" / "toolkit" / "src_l1").glob("*.py")):
    field = src.stem
    NS = runpy.run_path(str(src), {"C": C})
    T, D = NS["T"], NS.get("D")  # D: stated catalogue default for flat thesaurus terms that are not subfields
    nodes = [n for n in json.loads((ROOT / "maps" / field / INDEX[field]["primary"]).read_text(encoding="utf-8"))["nodes"] if n["level"] == 1]
    codes = {n["code"] for n in nodes}
    for k in T:
        if k not in codes: print(f"{field}: unknown code {k!r}"); fails += 1
    cards = []
    for n in nodes:
        if n["code"] not in T and D: T[n["code"]] = D
        if n["code"] not in T: print(f"{field}: no card for {n['code']!r}"); fails += 1; continue
        e = T[n["code"]]
        solves, sig, tools, inputs, outputs = e[:5]
        note = e[5] if len(e) > 5 else ""
        sig = {f: v.split() for f, v in sig.items()}
        for f, vs in sig.items():
            for v in vs:
                if f not in VOCAB or v not in VOCAB[f]: print(f"{field} {n['code']}: bad signature {f}={v}"); fails += 1
        for t in tools:
            if len(t) != 3 or not t[2]: print(f"{field} {n['code']}: tool {t[0]!r} lacks hypotheses (R5)"); fails += 1
        notes = "drafted in session by a model from general knowledge; no source checked; needs specialist review"
        if note: notes = note + " " + notes[0].upper() + notes[1:]
        if field == "IK": notes = IK_NOTE + " " + notes
        cards.append({"id": f"{field}.TK.{n['code']}", "field": field, "node": n["id"], "name": n["name"],
                      "taxonomy_cell": n.get("taxonomy_cell"), "solves": solves, "signature": sig,
                      "tools": [{"name": a, "does": b, "hypotheses": c} for a, b, c in tools],
                      "inputs": inputs, "outputs": outputs, "cross_uses": [], "status": "draft",
                      "generated_by": BY, "date": DATE, "notes": notes})
    (ROOT / "cards" / "toolkit" / f"{field}_L1.json").write_text(json.dumps(cards, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{field}: {len(cards)}/{len(nodes)} cards, {sum(1 for c in cards if c['tools'])} with tools, {sum(len(c['tools']) for c in cards)} tools")
sys.exit(1 if fails else 0)
