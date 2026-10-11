"""v3 engine: Frame, Survey, Consult, Connect (Roadmap E1–E8, minimal).

Every function takes an `llm` callable: prompt -> parsed JSON (see llm.py).
Each run is saved to runs/<timestamp>-<mode>.json as a run record (R16).
"""
import json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VOCAB = json.loads((ROOT / "signatures" / "vocabulary.json").read_text())["facets"]
FIELDS = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()

RULES = (
    "Rules: be specific and expert. State every theorem or method with its conditions and whether this problem meets "
    "each one (yes / no / unknown). Do not invent sources; if you name a paper or result you are not sure of, say "
    "'(unverified)'. Mark anything speculative as a hypothesis. Plain English, short sentences."
)


def lens_cards(field):
    p = ROOT / "cards" / "lens" / f"{field}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def map_nodes(field, level=1):
    p = ROOT / "maps" / field
    for f in sorted(p.glob("*.json")) if p.exists() else []:
        return [n for n in json.loads(f.read_text(encoding="utf-8"))["nodes"] if n["level"] == level]
    return []


def children(field, node_id):
    p = ROOT / "maps" / field
    for f in sorted(p.glob("*.json")) if p.exists() else []:
        return [n for n in json.loads(f.read_text(encoding="utf-8"))["nodes"] if n.get("parent") == node_id and n["level"] == 2]
    return []


def toolkit(field):
    out = {}
    for p in sorted((ROOT / "cards" / "toolkit").glob(f"{field}*.json")):
        out.update({c["node"]: c for c in json.loads(p.read_text(encoding="utf-8"))})
    return out


def clean_signature(sig):
    out = {}
    for facet, vals in (sig or {}).items():
        vals = [vals] if isinstance(vals, str) else vals
        ok = [v for v in vals if v in VOCAB.get(facet, [])]
        if ok:
            out[facet] = ok
    return out


def save(record):
    d = ROOT / "runs"
    d.mkdir(exist_ok=True)
    record.setdefault("created", time.strftime("%Y-%m-%dT%H:%M:%S"))
    record.setdefault("id", time.strftime("%Y%m%d-%H%M%S") + "-" + record["mode"])
    (d / f"{record['id']}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False), encoding="utf-8")
    return record


# ---------- E1 Frame ----------
def frame(text, llm):
    prompt = f"""You frame problems for a knowledge instrument. Turn the user's input into a precise problem.

Input: {text}

Return only JSON:
{{"problem": "one precise sentence: what is sought, given what, under which constraints",
  "scqa": {{"situation": "", "complication": "", "question": "", "answer_form": "what a good answer looks like"}},
  "signature": {{facet: [values]}}  using ONLY these facets and values: {json.dumps(VOCAB)},
  "fields": ["up to 8 two-letter field codes most likely to matter, from {FIELDS}"],
  "unknowns": ["facts that would change the answer"],
  "clarifying_questions": ["at most 3, only if the input is genuinely ambiguous"]}}"""
    r = llm(prompt)
    r["signature"] = clean_signature(r.get("signature"))
    r["fields"] = [f for f in r.get("fields", []) if f in FIELDS]
    return r


# ---------- Survey (all of knowledge) ----------
def survey(text, llm, fields=None, framed=None):
    framed = framed or frame(text, llm)
    chosen = fields or FIELDS
    cards = {f: lens_cards(f) for f in chosen}
    lens_txt = "\n".join(f"- {f} {c[0]['name']}: {c[0]['question']} Cells: " + "; ".join(x['name'] for x in c[1:])
                         for f, c in cards.items() if c)
    prompt = f"""Apply the whole of human knowledge to this problem, field by field.
Problem: {framed['problem']}
Context: {json.dumps(framed.get('scqa', {}))}

Lenses (field: question; cells):
{lens_txt}

For EVERY field listed, either apply it or set it aside with a reason (no silent skipping).
{RULES}
Return only JSON:
{{"views": [{{"field": "XX", "cell": "XX.O.An", "sees": "the specific point this field makes", "question": "the hardest question it asks",
             "evidence": "what would settle it (warrant)", "risk": "what could go wrong"}}],
  "set_aside": [{{"field": "XX", "reason": ""}}],
  "collisions": ["where two fields pull against each other"],
  "blind_spots": ["fields people usually ignore here that matter"],
  "synthesis": {{"governing_thought": "", "key_line": ["2-5 supporting points"], "next_steps": [""]}}}}"""
    r = llm(prompt, max_tokens=8000)
    covered = {v.get("field") for v in r.get("views", [])} | {s.get("field") for s in r.get("set_aside", [])}
    r["uncovered"] = [f for f in chosen if f not in covered]
    return save({"mode": "survey", "input": text, "framed": framed, "signature": framed.get("signature"),
                 "consulted": chosen, "result": r})


# ---------- Consult (a whole field) ----------
def _nodes_for(field):
    nodes = map_nodes(field)
    if nodes:
        return [{"id": n["id"], "name": n["name"]} for n in nodes]
    return [{"id": c["id"], "name": c["name"]} for c in lens_cards(field)[1:]]


def consult(text, field, llm, batch=16, deepen=3, framed=None):
    framed = framed or frame(text, llm)
    nodes, tk = _nodes_for(field), toolkit(field)
    findings = {}
    for i in range(0, len(nodes), batch):
        part = nodes[i:i + batch]
        listing = "\n".join(f"- {n['id']} {n['name']}" + (f" | tools: {', '.join(t['name'] for t in tk[n['id']]['tools'])}" if n["id"] in tk else "") for n in part)
        prompt = f"""You are the whole of the field {field}, every specialist at once. Problem: {framed['problem']}
Signature: {json.dumps(framed.get('signature', {}))}

Consider EACH subfield below. For each, say whether it applies, and if so how a specialist there would attack the problem.
{listing}
{RULES}
Return only JSON: {{"nodes": [{{"id": "", "applies": "yes|maybe|no", "approach": "", "known_results": [""], "conditions": [{{"condition": "", "met": "yes|no|unknown"}}], "promise": 0-5, "cost": 0-5}}]}}"""
        for n in llm(prompt, max_tokens=6000).get("nodes", []):
            findings[n.get("id")] = n
    missing = [n["id"] for n in nodes if n["id"] not in findings]
    ranked = sorted((f for f in findings.values() if f.get("applies") in ("yes", "maybe")),
                    key=lambda f: (-(f.get("promise") or 0), f.get("cost") or 0))
    deeper = []
    for f in ranked[:deepen]:
        kids = children(field, f["id"])
        if not kids:
            continue
        prompt = f"""Go deeper inside {f['id']} for this problem: {framed['problem']}
Earlier view: {f.get('approach')}
Sub-areas: {"; ".join(k['code'] + ' ' + k['name'] for k in kids)}
Pick the 1-3 most useful sub-areas and give specific methods or theorems with their conditions.
{RULES}
Return only JSON: {{"node": "{f['id']}", "picks": [{{"code": "", "method": "", "conditions": [{{"condition": "", "met": "yes|no|unknown"}}], "first_step": ""}}]}}"""
        deeper.append(llm(prompt, max_tokens=3000))
    prompt = f"""Synthesise a Minto answer for the problem: {framed['problem']}
Field consulted: {field}. Findings: {json.dumps(ranked[:12])[:20000]}
Deeper work: {json.dumps(deeper)[:12000]}
Return only JSON: {{"governing_thought": "", "routes": [{{"summary": "", "nodes": [""], "why": "", "conditions_open": [""], "status": "proposed|conditions_checked", "promise": 0-5, "cost": 0-5}}], "surprises": ["routes from unexpected subfields"], "verify_next": [""]}}"""
    synth = llm(prompt, max_tokens=5000)
    return save({"mode": "consult", "input": text, "field": field, "framed": framed, "signature": framed.get("signature"),
                 "consulted": [n["id"] for n in nodes], "not_returned": missing, "findings": findings,
                 "deeper": deeper, "result": synth})


# ---------- Connect (distant tools with the same shape) ----------
def connect_run(text, field, llm, top=8, framed=None):
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from connect import connect as match
    framed = framed or frame(text, llm)
    cands = match(framed.get("signature", {}), field, top)
    prompt = f"""Problem: {framed['problem']}
Signature: {json.dumps(framed.get('signature', {}))}
Candidate tools from across {field}, chosen by matching the problem's shape (some may be from distant subfields):
{json.dumps(cands)[:20000]}
For each candidate: explain the mapping (what in the problem corresponds to what in the tool), check each condition (yes/no/unknown), and rate promise 0-5. Flag the most surprising viable candidate.
{RULES}
Return only JSON: {{"candidates": [{{"card": "", "mapping": "", "conditions": [{{"condition": "", "met": "yes|no|unknown"}}], "promise": 0-5, "status": "proposed|conditions_checked"}}], "most_surprising": "", "verify_next": [""]}}"""
    r = llm(prompt, max_tokens=5000)
    return save({"mode": "connect", "input": text, "field": field, "framed": framed, "signature": framed.get("signature"),
                 "consulted": [c["card"] for c in cands], "matcher": cands, "result": r})
