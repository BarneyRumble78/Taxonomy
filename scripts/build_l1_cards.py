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

def K(solves, sig, tools=(), inp="", out="", note=""):
    """Compact form: sig 'task=predict estimate|structure=graph_network'; hypotheses, inputs, outputs split on '; '."""
    sp = lambda x: [y.strip() for y in x.split("; ") if y.strip()]
    e = (sp(solves), dict(kv.split("=") for kv in sig.split("|")), [(a, d, sp(h)) for a, d, h in tools], sp(inp), sp(out))
    return e + (note,) if note else e

def N(solves, sig):
    return K(solves, sig, note="No tool is listed. None could be stated with confidence in this draft.")

fails = 0
LEVEL = int(sys.argv[1]) if len(sys.argv) > 1 else 1   # python3 scripts/build_l1_cards.py 2  builds level 2 from src_l2/
NEC = C("Residual class of the scheme (not elsewhere classified). It holds no tools of its own.")
seen = {c["id"] for q in (ROOT / "cards" / "toolkit").glob("*_L*.json") if not q.name.endswith(f"_L{LEVEL}.json") for c in json.loads(q.read_text(encoding="utf-8"))}
SRC = ROOT / "cards" / "toolkit" / f"src_l{LEVEL}"
for src in sorted(q for q in SRC.glob("*.py") if "__" not in q.stem):
    field = src.stem
    NS = runpy.run_path(str(src), {"C": C, "K": K, "N": N})
    T, D = dict(NS["T"]), NS.get("D")
    for part in sorted(SRC.glob(f"{field}__*.py")):      # large fields are split across FIELD__n.py parts
        PT = runpy.run_path(str(part), {"C": C, "K": K, "N": N})["T"]
        for k in PT:
            if k in T: print(f"{field}: {k!r} defined twice"); fails += 1
        T.update(PT)  # D: stated catalogue default for flat thesaurus terms that are not subfields
    nodes = [n for n in json.loads((ROOT / "maps" / field / INDEX[field]["primary"]).read_text(encoding="utf-8"))["nodes"] if n["level"] == LEVEL]
    uniq, dupmap = {}, 0
    for n in nodes:                      # a map may list the same node id twice; one card per node id
        if n["id"] in uniq: dupmap += 1
        else: uniq[n["id"]] = n
    nodes = list(uniq.values())
    if dupmap: print(f"{field}: {dupmap} repeated node ids in the map were skipped")
    cnt = {}
    for n in nodes: cnt[n["code"]] = cnt.get(n["code"], 0) + 1
    for n in nodes:                      # same code under two parents: key and card id use the node id tail
        if cnt[n["code"]] > 1: n["code"] = n["id"].split(":", 1)[1]
    codes = {n["code"] for n in nodes}
    for k in T:
        if k not in codes: print(f"{field}: unknown code {k!r}"); fails += 1
    cards = []
    for n in nodes:
        if n["code"] not in T and "not elsewhere classified" in n["name"].lower(): T[n["code"]] = NEC
        if f"{field}.TK.{n['code']}" in seen: print(f"{field}: id collision {n['code']!r}"); fails += 1
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
    (ROOT / "cards" / "toolkit" / f"{field}_L{LEVEL}.json").write_text(json.dumps(cards, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{field}: {len(cards)}/{len(nodes)} cards, {sum(1 for c in cards if c['tools'])} with tools, {sum(len(c['tools']) for c in cards)} tools")
sys.exit(1 if fails else 0)
