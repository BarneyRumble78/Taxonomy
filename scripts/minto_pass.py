#!/usr/bin/env python3
"""Top-down Minto pass for one grouped field. Anthropic, strict tool schema.

    python3 scripts/minto_pass.py --field MA --max-cost 1 --stage-cap 22

Reads pyramids/queues/<F>.groups.json (cells and their groups), the field's
governing thought and key line (pyramids/<F>.md, pyramids/rebuild/<F>.json).
One call writes a governing thought, a key line of 2-5 pillars on the field's
own dimension, and re-parents every existing group under exactly one pillar
(sections of 2-5 when a pillar would hold more than five). Deterministic
validation, then minto_check, then a top-down field check. One repair try.
Writes pyramids/<F>.json and pyramids/<F>_minto.md, and field_check into the
groups file. Spend goes to cost_ledger.json under MINTO:<F>.
"""
import argparse, copy, fcntl, json, os, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine" / "v3"))
sys.path.insert(0, str(ROOT / "scripts"))
from minto_check import minto_issues, is_definition, TEMPLATE  # noqa
import run_pyramid_queue as q  # noqa

MODEL = "claude-sonnet-5-5"
IN_RATE, OUT_RATE = 2.0, 10.0
LEDGER = ROOT / "pyramids" / "queues" / "cost_ledger.json"
QP = Path("/workspace/qp_spend.json")
BASELINE = 30.90
BAN = re.compile(r"\b(MSC|LCC|ANZSRC|MeSH|catalogue|catalog|classification scheme|taxonomy|source scheme|class(es)? [0-9])", re.I)

SYSTEM = """You restructure one field of a knowledge system into a top-down Minto pyramid (Minto, The Pyramid Principle).
Rules you must follow exactly:
1. governing_thought: one sentence that answers "how is everything in this field divided?" It names the field's OWN organising dimension and lists the pillars in order.
2. Key line: 2 to 5 pillars, MECE on ONE dimension that belongs to the field's own subject matter (e.g. for religion: the ultimate, sacred texts, practice, community). Never a library, catalogue, code or source-scheme dimension. Never a pillar for "other", "miscellaneous", "general" or "containers".
3. The field's existing key line in the input is a hint only. Use it if every group truly fits one of its values; otherwise choose a better subject-matter dimension (what the knowledge is about, e.g. its objects, scales, regimes, stages or themes) so that every group fits exactly one pillar. A strict reviewer will reject any group that sits under a pillar whose value it does not share.
4. Every group id in the input appears exactly once, under exactly one pillar. Do not invent, drop, merge or split group ids.
5. Every node (pillar, section, subsection) has EITHER 2 to 5 ids in "members" OR 2 to 5 children (a pillar's children are "sections", a section's children are "subsections"), never both, never exactly one. Build the tree top-down: decide the pillars first, then split each pillar on one dimension of its own, then split again if needed. A pillar may NOT have exactly one item: if only one group fits a pillar, rethink the pillars.
6. Every statement (governing thought, pillar, section) is one plain declarative sentence ending with a full stop, at least eight words, saying what the members have in common and why they belong together (the summary idea, not a heading). Never start with "These", "Both are" or "All are". Never mention MSC, LCC, ANZSRC, MeSH, catalogue, taxonomy or codes.
9. "rewrites": for any input group whose statement describes a library, catalogue or code scheme instead of subject matter, give {id, statement} with a new subject-matter summary sentence (same rules as 6). Leave it empty when nothing needs rewriting.
10. "retired": ids of items with is_leaf true that are only container headings for the whole field (e.g. "Mathematics", "Pure mathematics", "General"), not topics. At most twelve. Retired ids are not placed under any pillar.
11. "dissolve": ids of input groups that are catch-alls or mix values of your dimension (e.g. "neighbouring areas"). Their listed children (by child id) then become items you must place individually, exactly once each; the dissolved group id itself is not placed.
12. "merge": when two leaf items name the same topic from different published sources (e.g. "Numerical analysis" and "Numerical and computational mathematics", or "Statistics" twice), give {keep, drop}; the drop id is folded into the keep id and is not placed. Only leaf ids. Never leave the same topic in two places.
13. A field may legitimately have a pillar for the discipline studied as a human activity (its history, teaching and community) and a pillar for its use in other fields' systems, if the dimension is the role the knowledge plays. Put every applied, computational or modelling topic in ONE pillar only.
14. Forbidden at every level (pillar, section, subsection): catch-all or residual nodes ("other", "general", "miscellaneous", "related topics", "reference", "methods and general works", "frameworks"), and nodes that copy a library or industry catalogue class (LCC, NAICS, ISIC, IEEE topic lists, "not elsewhere classified"). Every pillar must be a distinct value of ONE dimension; do not mix dimensions (e.g. stages with themes, functions with industry sectors, scale with kinds of thing). If an item fits nowhere, rethink the dimension rather than adding a bucket. Generic leaf items (e.g. "General", "Other ... not elsewhere classified") should be put in "retired".
7. Pillar statements must restate the key-line dimension: each names its own value of the dimension (e.g. "Practice is ...").
8. basis is cause_effect (order must be time), parts (order must be structure) or kinds (order structure, or degree with a rank_note). rank_note is one sentence explaining the order.
15. "method_line" is a node outside the key line (same shape as a pillar). When the input gives no fixed key line, leave its members and sections empty unless items are about how the discipline is studied, taught or recorded. "routed": ids of items that belong to another field (usually empty).
Call the tool record_pyramid exactly once."""

SEC = {"type": "object", "additionalProperties": False,
       "properties": {"statement": {"type": "string"}, "basis": {"type": "string", "enum": ["cause_effect", "parts", "kinds"]},
                      "order": {"type": "string", "enum": ["time", "structure", "degree"]}, "rank_note": {"type": "string"},
                      "members": {"type": "array", "items": {"type": "string"}}},
       "required": ["statement", "basis", "order", "rank_note", "members"]}
SUB = copy.deepcopy(SEC)
SEC = copy.deepcopy(SEC)
SEC["properties"]["subsections"] = {"type": "array", "items": SUB}
SEC["required"] = SEC["required"] + ["subsections"]
PIL = {"type": "object", "additionalProperties": False,
       "properties": {"title": {"type": "string"}, "statement": {"type": "string"},
                      "basis": SEC["properties"]["basis"], "order": SEC["properties"]["order"], "rank_note": {"type": "string"},
                      "members": {"type": "array", "items": {"type": "string"}}, "sections": {"type": "array", "items": SEC}},
       "required": ["title", "statement", "basis", "order", "rank_note", "members", "sections"]}
SCHEMA = {"type": "object", "additionalProperties": False,
          "properties": {"governing_thought": {"type": "string"}, "dimension": {"type": "string"}, "plural_noun": {"type": "string"},
                         "basis": SEC["properties"]["basis"], "order": SEC["properties"]["order"], "rank_note": {"type": "string"},
                         "situation": {"type": "string"}, "complication": {"type": "string"}, "question": {"type": "string"},
                         "pillars": {"type": "array", "items": PIL},
                         "rewrites": {"type": "array", "items": {"type": "object", "additionalProperties": False, "properties": {"id": {"type": "string"}, "statement": {"type": "string"}}, "required": ["id", "statement"]}},
                         "retired": {"type": "array", "items": {"type": "string"}},
                         "dissolve": {"type": "array", "items": {"type": "string"}},
                         "method_line": PIL,
                         "routed": {"type": "array", "items": {"type": "string"}},
                         "merge": {"type": "array", "items": {"type": "object", "additionalProperties": False, "properties": {"keep": {"type": "string"}, "drop": {"type": "string"}}, "required": ["keep", "drop"]}}},
          "required": ["method_line", "routed", "merge", "dissolve", "rewrites", "retired", "governing_thought", "dimension", "plural_noun", "basis", "order", "rank_note", "situation", "complication", "question", "pillars"]}
CHECK_SYSTEM = """You check a classification pyramid from the top down (Minto key-line test).
key_line_holds is true when ALL of these are true: (a) the governing thought names one dimension intrinsic to the field (for example what the knowledge is about, the role a piece of knowledge plays, a causal link, scale, stage or theme) and answers the question how the field divides; (b) there are 2-5 pillars and each is a distinct value of that one dimension; (c) together the pillars cover the field, and no pillar is a catch-all; (d) each pillar statement restates its own value of the dimension; (e) no pillar or section is organised by a library, catalogue or code scheme.
Judge (a)-(e) on the governing thought, the pillars and their direct sections only. Do NOT set key_line_holds false because of individual misplaced items deeper down; count those in misplaced instead.
misplaced: the number of second- or third-level items that clearly belong under a different pillar.
Field-specific facts: in information science (IS) and library science, classification schemes, thesauri and catalogues are the subject matter itself, so a section about named schemes is legitimate there. In any field, a pillar for the discipline studied as a human activity (its history, teaching, methodology and profession) is a legitimate value when the dimension is the role the knowledge plays; judge it by whether its members fit that value.
The method line sits outside the key line and holds how the discipline is studied, taught and recorded; it is not a pillar and not a catch-all if its items fit that description. Routed items belong to another field and are not judged here.
Ids like P1.2 are neutral positions, not codes. Leaf topic names come from published sources and cannot be renamed.
note: one sentence, at most twenty-five words: the worst key-line problem if key_line_holds is false, otherwise the worst misplaced items by position.
Call the tool record_check exactly once."""
CHECK_SCHEMA = {"type": "object", "additionalProperties": False,
                "properties": {"key_line_holds": {"type": "boolean"}, "misplaced": {"type": "integer"}, "note": {"type": "string"}}, "required": ["key_line_holds", "misplaced", "note"]}

EXPAND = re.compile(BAN.pattern + r"|\bcontainer|classifications?\b|\bcategories\b", re.I)
PRE_RETIRED = []
FIXED = {}
FIXED_MODE = [False]
ATTEMPTS = [6]
LOG = Path("/workspace/minto_pass.log")


def log(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    with LOG.open("a") as h:
        h.write(line + "\n")


def total_spent():
    led = json.loads(LEDGER.read_text())
    qp = json.loads(QP.read_text()) if QP.exists() else {"spent": 0}
    return float(led.get("spent", 0)) + float(qp.get("spent", 0))


def add_spend(field, usd):
    with LEDGER.open("r+") as h:
        fcntl.flock(h.fileno(), fcntl.LOCK_EX)
        led = json.loads(h.read() or "{}")
        led["spent"] = round(float(led.get("spent", 0)) + usd, 6)
        k = f"MINTO:{field}"
        led.setdefault("fields", {})[k] = round(float(led["fields"].get(k, 0)) + usd, 6)
        h.seek(0); h.truncate(); h.write(json.dumps(led, indent=2) + "\n")
        fcntl.flock(h.fileno(), fcntl.LOCK_UN)


class Budget:
    def __init__(self, field, field_cap, stage_cap):
        cap_file = Path("/workspace/minto_stage_cap")
        if cap_file.exists():
            stage_cap = min(50.0, float(cap_file.read_text().strip()))  # Chris approved $50 hard stage cap (13 Oct, 1:23 PM)
        self.field, self.field_cap, self.stage_cap, self.used = field, field_cap, stage_cap, 0.0

    def call(self, system, user, tool, schema, max_tokens):
        worst = (len(system) + len(user)) / 3.2 / 1e6 * IN_RATE + max_tokens / 1e6 * OUT_RATE
        if self.used + worst > self.field_cap:
            raise RuntimeError(f"field cap ${self.field_cap} would be passed")
        if total_spent() - BASELINE + worst > self.stage_cap:
            raise RuntimeError(f"stage cap ${self.stage_cap} would be passed")
        ctl = q.anthropic_controls(MODEL)
        tdef = {"name": tool, "description": "Record the result.", "input_schema": schema}
        if ctl.get("strict"):
            tdef["strict"] = True
        body = {"model": MODEL, "max_tokens": max_tokens, "system": system,
                "messages": [{"role": "user", "content": user}], "tools": [tdef], "tool_choice": ctl["tool_choice"]}
        if ctl.get("thinking"):
            body["thinking"] = ctl["thinking"]
        if ctl.get("effort"):
            body["output_config"] = {"effort": ctl["effort"]}
        data = q._post_anthropic(body, os.environ["ANTHROPIC_API_KEY"])
        u = data.get("usage") or {}
        usd = (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) * 1.25 + u.get("cache_read_input_tokens", 0) * 0.05) / 1e6 * IN_RATE \
            + u.get("output_tokens", 0) / 1e6 * OUT_RATE
        self.used += usd
        add_spend(self.field, usd)
        log(f"{self.field} call {tool} in={u.get('input_tokens')} out={u.get('output_tokens')} usd={usd:.4f}")
        for b in data.get("content") or []:
            if b.get("type") == "tool_use" and b.get("name") == tool:
                return b.get("input") or {}
        raise RuntimeError("no tool_use in reply")


def section(text, head):
    m = re.search(rf"^## {re.escape(head)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def leaves(p, out, cap=6):
    sup = (p.get("support") or {}).get("points")
    if not sup:
        out.append(p.get("name") or p.get("statement") or p.get("id"))
    else:
        for c in sup:
            if len(out) >= cap:
                return out
            leaves(c, out, cap)
    return out


def load(field):
    g = json.loads((ROOT / "pyramids" / "queues" / f"{field}.groups.json").read_text())
    items = {}
    for c in g["cells"]:
        for p in (c.get("support") or {}).get("points") or []:
            kids = (p.get("support") or {}).get("points") or []
            if kids and EXPAND.search(p.get("statement") or ""):
                for k in kids:
                    items[k.get("id") or k.get("anchor")] = {"point": k, "cell": c.get("id")}
                continue
            pid = p.get("id") or p.get("anchor")
            items[pid] = {"point": p, "cell": c.get("id"), "cell_statement": c.get("statement")}
    TARGET = 75
    def nkids(p): return len((p.get("support") or {}).get("points") or [])
    while True:
        cands = [k for k, v in items.items() if nkids(v["point"]) and len(items) - 1 + nkids(v["point"]) <= TARGET]
        if not cands:
            break
        cands.sort(key=lambda k: (not EXPAND.search(items[k]["point"].get("statement") or ""), -nkids(items[k]["point"])))
        k = cands[0]
        v = items.pop(k)
        for c in v["point"]["support"]["points"]:
            items[c.get("id") or c.get("anchor")] = {"point": c, "cell": v.get("cell")}
    byname, drop = {}, []
    for k, v in items.items():
        pt = v["point"]
        if (pt.get("support") or {}).get("points"):
            continue
        nm = re.sub(r"\W+", " ", (pt.get("name") or pt.get("statement") or "")).strip().lower()
        if nm in byname:
            items[byname[nm]]["point"].setdefault("aliases", []).append(k); drop.append(k)
        else:
            byname[nm] = k
    for k in drop:
        items.pop(k)
    # Catalogue residual leaves are not topics: retire them before the model sees them.
    RESID = re.compile(r"not elsewhere classified|\bn\.?e\.?c\.?\b|^\s*(general|miscellaneous|other)\b|\bmiscellan|, general$|\(general\)", re.I)
    pre = [k for k, v in items.items() if not (v["point"].get("support") or {}).get("points") and RESID.search(v["point"].get("name") or v["point"].get("statement") or "")]
    PRE_RETIRED[:] = [{"id": k, "name": items[k]["point"].get("name"), "reason": "catalogue residual heading, not a topic"} for k in pre]
    for k in pre:
        items.pop(k)
    md = (ROOT / "pyramids" / f"{field}.md")
    text = md.read_text() if md.exists() else ""
    rb = ROOT / "pyramids" / "rebuild" / f"{field}.json"
    rbj = json.loads(rb.read_text()) if rb.exists() else {}
    return g, items, text, rbj


def repair(r, items):
    """Mechanical fixes only: no idea is moved across pillars."""
    groups = {k for k, v in items.items() if (v["point"].get("support") or {}).get("points")}
    ret = []
    for x in r.get("retired") or []:
        if x in groups:
            r.setdefault("dissolve", []).append(x)
        else:
            ret.append(x)
    r["retired"] = ret
    def fix(n, key):
        if not key:
            return
        nxt = {"sections": "subsections", "subsections": None}[key]
        kids = [c for c in n.get(key) or [] if c.get("members") or c.get(nxt or "_")]
        for c in kids:
            fix(c, nxt)
        changed = True
        while changed:
            changed = False
            for c in kids:
                if not c.get(nxt or "_") and len(c.get("members") or []) == 1 and len(kids) > 1:
                    others = sorted([o for o in kids if o is not c and not o.get(nxt or "_") and len(o["members"]) < 5], key=lambda o: len(o["members"]))
                    if others:
                        others[0]["members"] += c["members"]; kids.remove(c); changed = True; break
        if len(kids) == 1 and not kids[0].get(nxt or "_") and not n.get("members"):
            n["members"] = kids[0]["members"]; kids = []
        n[key] = kids
    for p in r.get("pillars") or []:
        fix(p, "sections")


def expand(r, items):
    """Dissolved groups put their children into items."""
    items = dict(items)
    for d in r.get("dissolve") or []:
        if d in items and (items[d]["point"].get("support") or {}).get("points"):
            for c in items.pop(d)["point"]["support"]["points"]:
                items[c.get("id") or c.get("anchor")] = {"point": c}
    for m in r.get("merge") or []:
        k, d = m.get("keep"), m.get("drop")
        if k in items and d in items and k != d and not (items[k]["point"].get("support") or {}).get("points") and not (items[d]["point"].get("support") or {}).get("points"):
            items[k] = {"point": dict(items[k]["point"], aliases=(items[k]["point"].get("aliases") or []) + [d] + (items[d]["point"].get("aliases") or []))}
            items.pop(d)
    return items


def validate(r, ids, leaf_ids=(), all_group_ids=()):
    errs = []
    gt = r.get("governing_thought", "")
    pills = r.get("pillars") or []
    if not 2 <= len(pills) <= 5:
        errs.append(f"key line has {len(pills)} pillars; need 2-5")
    seen = []
    texts = [gt]

    def grp(name, g):
        if g["basis"] == "cause_effect" and g["order"] != "time": errs.append(f"{name}: cause_effect needs order time")
        if g["basis"] == "parts" and g["order"] != "structure": errs.append(f"{name}: parts needs order structure")
        if g["basis"] == "kinds" and g["order"] == "time": errs.append(f"{name}: kinds cannot be order time")
    grp("key line", r)
    def node(name, n, kids_key):
        texts.append(n["statement"]); grp(name, n)
        kids = [c for c in (n.get(kids_key) or [])] if kids_key else []
        mem = n.get("members") or []
        if kids and mem:
            errs.append(f"{name} has both members and children")
        elif kids:
            if not 2 <= len(kids) <= 5: errs.append(f"{name} has {len(kids)} children; need 2-5")
            nxt = {"sections": "subsections", "subsections": None}[kids_key]
            for j, c in enumerate(kids, 1):
                node(f"{name} > {kids_key[:-1]} {j}", c, nxt)
        else:
            if not 2 <= len(mem) <= 5: errs.append(f"{name} has {len(mem)} members; need 2-5 (split into children if more than 5)")
            seen.extend(mem)
    for i, p in enumerate(pills, 1):
        node(f"pillar {i}", p, "sections")
    if FIXED and len(pills) != len(FIXED["pillars"]):
        errs.append(f"use exactly the {len(FIXED['pillars'])} fixed pillars in the given order")
    ml = r.get("method_line") or {}
    if ml.get("members") or ml.get("sections"):
        node("method line", ml, "sections")
    seen.extend(r.get("routed") or [])
    for t in texts:
        if not is_definition(t) or TEMPLATE.search(t) or BAN.search(t):
            errs.append(f"statement not allowed (blank, template or names a source scheme): {t[:90]}")
    ret = r.get("retired") or []
    if len(ret) > 12: errs.append("more than twelve retired ids")
    for x in ret:
        if x not in leaf_ids: errs.append(f"retired id {x} is not a leaf item")
    seen += ret
    for w in r.get("rewrites") or []:
        if w["id"] in all_group_ids:
            texts.append(w["statement"])
    r["rewrites"] = [w for w in r.get("rewrites") or [] if w["id"] in all_group_ids]
    dup = sorted({x for x in seen if seen.count(x) > 1})
    if dup: errs.append(f"group ids used more than once: {dup}")
    missing = sorted(set(ids) - set(seen))
    if missing: errs.append(f"group ids missing: {missing}")
    extra = sorted(set(seen) - set(ids))
    if extra: errs.append(f"unknown group ids: {extra}")
    return errs


def _rw(p, m):
    if p.get("id") in m:
        p["statement"] = p["name"] = m[p["id"]]
    for c in (p.get("support") or {}).get("points") or []:
        _rw(c, m)


def build(field, r, items):
    items = copy.deepcopy(items)
    m = {w["id"]: w["statement"] for w in r.get("rewrites") or []}
    for v in items.values():
        _rw(v["point"], m)
    def mk(n, nid, anchor, kids_key, extra=None):
        kids = n.get(kids_key) or [] if kids_key else []
        if kids:
            nxt = {"sections": ("subsections", "S"), "subsections": (None, "U")}[kids_key]
            pts_ = [mk(c, f"{nid}.{nxt[1]}{j}", "section", nxt[0]) for j, c in enumerate(kids, 1)]
        else:
            pts_ = [copy.deepcopy(items[x]["point"]) for x in n["members"]]
        out = {"id": nid, "anchor": f"{anchor}:{nid}", "statement": n["statement"], "name": n["statement"],
               "support": {"logic_type": "inductive", "basis": n["basis"], "order": n["order"], "rank_note": n["rank_note"], "points": pts_}}
        if extra: out.update(extra)
        return out
    pts = [mk(p, f"{field}.K{i}", "pillar", "sections", {"title": p["title"]}) for i, p in enumerate(r["pillars"], 1)]
    ml = r.get("method_line") or {}
    method = None
    if ml.get("members") or ml.get("sections"):
        m_ = mk(ml, f"{field}.M", "method", "sections")
        method = {"logic_type": "inductive", "statement": ml["statement"], "basis": ml["basis"], "order": ml["order"],
                  "rank_note": ml["rank_note"], "points": m_["support"]["points"]}
    return {"field": field, "introduction": {"situation": r["situation"], "complication": r["complication"], "question": r["question"],
                                             "answer": r["governing_thought"]},
            "governing_thought": r["governing_thought"],
            "key_line": {"logic_type": "inductive", "plural_noun": r["plural_noun"], "mece_dimension": r["dimension"],
                         "basis": r["basis"], "order": r["order"], "rank_note": r["rank_note"], "points": pts},
            "method_line": method,
            "routed": [{"id": x, "name": items[x]["point"].get("name")} for x in r.get("routed") or [] if x in items],
            "retired": [{"id": x, "name": items[x]["point"].get("name"), "reason": "container heading for the whole field, not a topic"} for x in r.get("retired") or []] + PRE_RETIRED,
            "build": {"script": "scripts/minto_pass.py", "model": MODEL, "source": f"pyramids/queues/{field}.groups.json"}}


def render(pyr):
    f = pyr["field"]; k = pyr["key_line"]; i = pyr["introduction"]
    L = [f"# {f} — top-down Minto pyramid", "", "Built by scripts/minto_pass.py from the grouped classification. Three rules (Minto pp. 9-11): each summary states the idea of its group, members are the same kind of idea, and they are in a stated order.", "",
         "## Introduction", "", f"**Situation.** {i['situation']}", "", f"**Complication.** {i['complication']}", "", f"**Question.** {i['question']}", "", f"**Answer.** {i['answer']}", "",
         "## Governing thought", "", pyr["governing_thought"], "", "## Key line", "",
         f"Group of {k['plural_noun']}. Basis: {k['basis']}. Dimension: {k['mece_dimension']}. Order: {k['order']}. {k['rank_note']}", ""]
    for n, p in enumerate(k["points"], 1):
        L.append(f"{n}. {p['statement']} `{p['id']}`")
    L += ["", "## Groups", ""]

    def walk(p, d):
        s = p.get("support")
        if s and s.get("points"):
            L.append("  " * d + f"- **{p['statement']}**")
            L.append("  " * d + f"  _basis: {s.get('basis')}, order: {s.get('order')}" + (f". {s['rank_note']}" if s.get("rank_note") else "") + "_")
            for c in s["points"]: walk(c, d + 1)
        else:
            L.append("  " * d + f"- {p.get('name') or p.get('statement')}")
    for n, p in enumerate(k["points"], 1):
        L += [f"### {n}. {p['statement']}", ""]
        for c in p["support"]["points"]: walk(c, 0)
        L.append("")
    ml = pyr.get("method_line")
    if ml:
        L += ["## Method line (outside the key line)", "", f"**{ml['statement']}**", f"_basis: {ml.get('basis')}, order: {ml.get('order')}_", ""]
        for c in ml["points"]: walk(c, 0)
        L.append("")
    if pyr.get("routed"):
        L += ["## Routed to other fields", ""] + [f"- {x['name']}" for x in pyr["routed"]] + [""]
    fc = pyr.get("field_check") or {}
    L += ["## Checks", "", f"- minto_check: {'clean' if not any(pyr.get('minto_issues', {}).values()) else pyr.get('minto_issues')}",
          f"- field_check holds: {fc.get('holds')} — {fc.get('note', '')}", ""]
    return "\n".join(L)


def run(field, field_cap, stage_cap, dry=False):
    g, items, text, rbj = load(field)
    ids = list(items)
    leaf_ids = {k for k, v in items.items() if not (v["point"].get("support") or {}).get("points")}
    gids = set()
    def _g(p):
        if (p.get("support") or {}).get("points"):
            gids.add(p.get("id")); [_g(c) for c in p["support"]["points"]]
    [_g(v["point"]) for v in items.values()]
    gt_old = section(text, "Governing thought")
    kl_old = section(text, "Key line")
    payload = {"field": field, "existing_governing_thought": gt_old[:1500], "existing_key_line": kl_old[:1500],
               "rebuild_key_line": rbj.get("key_line"), "scope": rbj.get("scope"),
               "groups": [{"id": k, "statement": v["point"].get("statement") or v["point"].get("name"),
                           "is_leaf": not (v["point"].get("support") or {}).get("points"),
                           "children": [{"id": c.get("id") or c.get("anchor"), "name": (c.get("statement") or c.get("name") or "")[:120]} for c in (v["point"].get("support") or {}).get("points") or []]} for k, v in items.items()]}
    kf = ROOT / "pyramids" / "keylines" / f"{field}.json"
    FIXED.clear()
    if FIXED_MODE[0] and kf.exists():
        FIXED.update(json.loads(kf.read_text()))
        payload["fixed_key_line"] = FIXED
        payload["instruction"] = ("The key line is FIXED and approved: use exactly these pillars, in this order, with these titles and statements. "
                                  "Your job is to place every item under the pillar whose value it shares, build 2-5 sections inside each pillar, "
                                  "write section statements that restate that pillar's value, and put items about " + FIXED["method_line"]["covers"] +
                                  " into method_line. " + FIXED.get("route_note", ""))
        payload.pop("existing_governing_thought", None); payload.pop("existing_key_line", None); payload.pop("rebuild_key_line", None)
    user = "Restructure this field. Input JSON:\n" + json.dumps(payload, ensure_ascii=False, indent=1)
    if dry:
        print(user); return None
    b = Budget(field, field_cap, stage_cap)
    feedback = ""
    pyr = None
    best = None
    last = None
    for attempt in range(ATTEMPTS[0]):
        msg = user + (f"\n\nYour previous answer (JSON below) was rejected. Return it corrected: keep everything that is fine, change only what is needed to fix ALL of these:\n{feedback}\n\nPrevious answer:\n{json.dumps(last, ensure_ascii=False)}" if feedback else "")
        try:
            r = b.call(SYSTEM, msg, "record_pyramid", SCHEMA, 10000)
        except RuntimeError as e:
            log(f"{field} stop: {e}"); break
        if not r.get("pillars"):
            feedback = feedback or "- key line had 0 pillars"; log(f"{field} attempt {attempt+1} empty reply"); continue
        if FIXED:
            r["governing_thought"] = FIXED["governing_thought"]
            for key in ("dimension", "plural_noun", "basis", "order", "rank_note"):
                r[key] = FIXED[key]
            for p_, fp in zip(r["pillars"], FIXED["pillars"]):
                p_["title"], p_["statement"] = fp["title"], fp["statement"]
            ml = r.get("method_line") or {}
            if ml:
                ml["title"] = "Method line"
        last = copy.deepcopy(r)
        repair(r, items)
        its = expand(r, items)
        bad_d = [d for d in r.get("dissolve") or [] if d not in items or not (items[d]["point"].get("support") or {}).get("points")]
        lids = {k for k, v in its.items() if not (v["point"].get("support") or {}).get("points")}
        errs = validate(r, list(its), lids, gids) + [f"dissolve id {d} is not an input group" for d in bad_d]
        if errs:
            feedback = "\n".join("- " + e for e in errs) + "\n- Remember: 2-5 pillars, each with 2-5 members or 2-5 sections of 2-5 members; every listed id exactly once."; log(f"{field} attempt {attempt+1} invalid: {feedback[:400]}")
            continue
        pyr = build(field, r, its)
        iss = minto_issues(pyr)
        # mixed_kinds is a DPSIR word heuristic (response, limit, place...) built for EV; it misfires elsewhere.
        bad = {k: v for k, v in iss.items() if v and (field == "EV" or k != "mixed_kinds")}
        pyr["minto_issues"] = bad
        def vw(n, pos, depth):
            sup = (n.get("support") or {}).get("points")
            d = {"id": pos, "statement": (n.get("statement") or n.get("name") or "")[:160]}
            if sup and depth < 3:
                d["under"] = [vw(c, f"{pos}.{i}", depth + 1) for i, c in enumerate(sup, 1)]
            return d
        view = {"governing_thought": pyr["governing_thought"], "key_line_dimension": r["dimension"],
                "pillars": [vw(p, f"P{pi}", 0) for pi, p in enumerate(pyr["key_line"]["points"], 1)],
                "method_line_outside_key_line": [vw(c, f"M.{i}", 1) for i, c in enumerate((pyr.get("method_line") or {}).get("points") or [], 1)],
                "routed_to_other_fields": [x["name"] for x in pyr.get("routed") or []]}
        try:
            chk = b.call(CHECK_SYSTEM, "Check this pyramid:\n" + json.dumps(view, ensure_ascii=False, indent=1), "record_check", CHECK_SCHEMA, 2500)
        except RuntimeError as e:
            log(f"{field} stop: {e}"); break
        pyr["field_check"] = {"governing_thought": pyr["governing_thought"], "key_line": [p["statement"] for p in pyr["key_line"]["points"]],
                              "holds": bool(chk.get("key_line_holds")) and not bad, "note": chk.get("note", ""), "review": not chk.get("key_line_holds")}
        log(f"{field} attempt {attempt+1} minto_issues={sum(len(v) for v in bad.values())} holds={chk.get('key_line_holds')} misplaced={chk.get('misplaced')} note={chk.get('note')}")
        pyr["field_check"]["misplaced"] = int(chk.get("misplaced") or 0)
        pyr["field_check"]["problems"] = (0 if chk.get("key_line_holds") else 100) + pyr["field_check"]["misplaced"] + sum(len(v) for v in bad.values())
        if best is None or pyr["field_check"]["holds"] or pyr["field_check"]["problems"] < best["field_check"]["problems"]:
            best = pyr
        if pyr["field_check"]["holds"] and (pyr["field_check"]["misplaced"] <= 5 or attempt >= 2):
            break
        pos = {f"P{pi}.{ci}": (c.get("id") or c.get("name")) for pi, p in enumerate(pyr["key_line"]["points"], 1) for ci, c in enumerate(p["support"]["points"], 1)}
        feedback = ("- The key line passed; now fix the misplaced items.\n" if pyr["field_check"]["holds"] else "") + f"- minto_check problems: {bad}\n- top-down check said: {chk.get('note')}\n- position key for that note: {json.dumps(pos)}"
        if b.used > field_cap * 0.8:
            break
    pyr = best
    if pyr is None:
        log(f"{field} FAILED no valid structure; cost ${b.used:.4f}"); return {"field": field, "holds": False, "cost": b.used}
    pyr["cost_usd"] = round(b.used, 4)
    (ROOT / "pyramids" / f"{field}.json").write_text(json.dumps(pyr, indent=2, ensure_ascii=False) + "\n")
    (ROOT / "pyramids" / f"{field}_minto.md").write_text(render(pyr))
    g["field_check"] = pyr["field_check"]
    (ROOT / "pyramids" / "queues" / f"{field}.groups.json").write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n")
    log(f"{field} DONE holds={pyr['field_check']['holds']} cost=${b.used:.4f}")
    return {"field": field, "holds": pyr["field_check"]["holds"], "cost": b.used}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--field", required=True); ap.add_argument("--max-cost", type=float, default=1.0)
    ap.add_argument("--stage-cap", type=float, default=22.0); ap.add_argument("--fixed", action="store_true")
    ap.add_argument("--attempts", type=int, default=6); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    FIXED_MODE[0] = a.fixed
    ATTEMPTS[0] = a.attempts
    res = run(a.field, a.max_cost, a.stage_cap, a.dry_run)
    print(json.dumps(res))
