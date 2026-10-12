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
5. A pillar with 2 to 5 items lists them in "members" and leaves "sections" empty. A pillar with more than 5 items puts them in 2 to 5 "sections", each with 2 to 5 member ids, and leaves "members" empty. A pillar may NOT have exactly one item: if only one group fits a pillar, rethink the pillars.
6. Every statement (governing thought, pillar, section) is one plain declarative sentence ending with a full stop, at least eight words, saying what the members have in common and why they belong together (the summary idea, not a heading). Never start with "These", "Both are" or "All are". Never mention MSC, LCC, ANZSRC, MeSH, catalogue, taxonomy or codes.
9. "rewrites": for any input group whose statement describes a library, catalogue or code scheme instead of subject matter, give {id, statement} with a new subject-matter summary sentence (same rules as 6). Leave it empty when nothing needs rewriting.
10. "retired": ids of items with is_leaf true that are only container headings for the whole field (e.g. "Mathematics", "Pure mathematics", "General"), not topics. At most five. Retired ids are not placed under any pillar.
11. "dissolve": ids of input groups that are catch-alls or mix values of your dimension (e.g. "neighbouring areas"). Their listed children (by child id) then become items you must place individually, exactly once each; the dissolved group id itself is not placed.
12. "merge": when two leaf items name the same topic from different published sources (e.g. "Numerical analysis" and "Numerical and computational mathematics", or "Statistics" twice), give {keep, drop}; the drop id is folded into the keep id and is not placed. Only leaf ids. Never leave the same topic in two places.
13. A field may legitimately have a pillar for the discipline studied as a human activity (its history, teaching and community) and a pillar for its use in other fields' systems, if the dimension is the role the knowledge plays. Put every applied, computational or modelling topic in ONE pillar only.
7. Pillar statements must restate the key-line dimension: each names its own value of the dimension (e.g. "Practice is ...").
8. basis is cause_effect (order must be time), parts (order must be structure) or kinds (order structure, or degree with a rank_note). rank_note is one sentence explaining the order.
Call the tool record_pyramid exactly once."""

SEC = {"type": "object", "additionalProperties": False,
       "properties": {"statement": {"type": "string"}, "basis": {"type": "string", "enum": ["cause_effect", "parts", "kinds"]},
                      "order": {"type": "string", "enum": ["time", "structure", "degree"]}, "rank_note": {"type": "string"},
                      "members": {"type": "array", "items": {"type": "string"}}},
       "required": ["statement", "basis", "order", "rank_note", "members"]}
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
                         "merge": {"type": "array", "items": {"type": "object", "additionalProperties": False, "properties": {"keep": {"type": "string"}, "drop": {"type": "string"}}, "required": ["keep", "drop"]}}},
          "required": ["merge", "dissolve", "rewrites", "retired", "governing_thought", "dimension", "plural_noun", "basis", "order", "rank_note", "situation", "complication", "question", "pillars"]}
CHECK_SYSTEM = """You check a classification pyramid from the top down, strictly.
holds is true only when ALL of these are true: the governing thought names one dimension intrinsic to the field (for example what the knowledge is about, the role a piece of knowledge plays such as object studied / practice / application to another field, scale, stage or theme); the 2-5 pillars are mutually exclusive values of that dimension and together exhaust the field; each pillar statement restates its value of the dimension; every group under a pillar belongs to that pillar's value better than to any other pillar; no pillar or section is organised by a library, catalogue or code scheme.
Ids like P1.2 are neutral positions, not codes. Leaf topic names come from published sources and cannot be renamed; judge where they are placed, not their wording. Overlap means one item fits two pillars equally well, not merely that two fields are related.
problems: the number of misplaced or overlapping items you found (0 when holds is true).
note: one sentence, at most twenty-five words; when holds is false, name the worst problem and the group ids involved.
Call the tool record_check exactly once."""
CHECK_SCHEMA = {"type": "object", "additionalProperties": False,
                "properties": {"holds": {"type": "boolean"}, "problems": {"type": "integer"}, "note": {"type": "string"}}, "required": ["holds", "problems", "note"]}

EXPAND = re.compile(BAN.pattern + r"|\bcontainer|classifications?\b|\bcategories\b", re.I)
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
        self.field, self.field_cap, self.stage_cap, self.used = field, field_cap, stage_cap, 0.0

    def call(self, system, user, tool, schema, max_tokens):
        worst = (len(system) + len(user)) / 3.2 / 1e6 * IN_RATE + max_tokens / 1e6 * OUT_RATE
        prior = float(json.loads(LEDGER.read_text())["fields"].get(f"MINTO:{self.field}", 0))
        if prior + worst > self.field_cap:
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
    md = (ROOT / "pyramids" / f"{field}.md")
    text = md.read_text() if md.exists() else ""
    rb = ROOT / "pyramids" / "rebuild" / f"{field}.json"
    rbj = json.loads(rb.read_text()) if rb.exists() else {}
    return g, items, text, rbj


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
    for i, p in enumerate(pills, 1):
        texts.append(p["statement"]); grp(f"pillar {i}", p)
        if p["sections"] and p["members"]:
            errs.append(f"pillar {i} has both members and sections")
        if p["sections"]:
            if not 2 <= len(p["sections"]) <= 5: errs.append(f"pillar {i} has {len(p['sections'])} sections; need 2-5")
            for j, s in enumerate(p["sections"], 1):
                texts.append(s["statement"]); grp(f"pillar {i} section {j}", s)
                if not 2 <= len(s["members"]) <= 5: errs.append(f"pillar {i} section {j} has {len(s['members'])} members; need 2-5")
                seen += s["members"]
        else:
            if not 2 <= len(p["members"]) <= 5: errs.append(f"pillar {i} has {len(p['members'])} members; need 2-5 (use sections if more than 5)")
            seen += p["members"]
    for t in texts:
        if not is_definition(t) or TEMPLATE.search(t) or BAN.search(t):
            errs.append(f"statement not allowed (blank, template or names a source scheme): {t[:90]}")
    ret = r.get("retired") or []
    if len(ret) > 5: errs.append("more than five retired ids")
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
    pts = []
    for i, p in enumerate(r["pillars"], 1):
        pid = f"{field}.K{i}"
        if p["sections"]:
            kids = []
            for j, s in enumerate(p["sections"], 1):
                kids.append({"id": f"{pid}.S{j}", "anchor": f"section:{pid}.S{j}", "statement": s["statement"], "name": s["statement"],
                             "support": {"logic_type": "inductive", "basis": s["basis"], "order": s["order"], "rank_note": s["rank_note"],
                                         "points": [copy.deepcopy(items[m]["point"]) for m in s["members"]]}})
        else:
            kids = [copy.deepcopy(items[m]["point"]) for m in p["members"]]
        pts.append({"id": pid, "anchor": f"pillar:{pid}", "title": p["title"], "statement": p["statement"], "name": p["statement"],
                    "support": {"logic_type": "inductive", "basis": p["basis"], "order": p["order"], "rank_note": p["rank_note"], "points": kids}})
    return {"field": field, "introduction": {"situation": r["situation"], "complication": r["complication"], "question": r["question"],
                                             "answer": r["governing_thought"]},
            "governing_thought": r["governing_thought"],
            "key_line": {"logic_type": "inductive", "plural_noun": r["plural_noun"], "mece_dimension": r["dimension"],
                         "basis": r["basis"], "order": r["order"], "rank_note": r["rank_note"], "points": pts},
            "retired": [{"id": x, "name": items[x]["point"].get("name"), "reason": "container heading for the whole field, not a topic"} for x in r.get("retired") or []],
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
    user = "Restructure this field. Input JSON:\n" + json.dumps(payload, ensure_ascii=False, indent=1)
    if dry:
        print(user); return None
    b = Budget(field, field_cap, stage_cap)
    feedback = ""
    pyr = None
    best = None
    for attempt in range(6):
        msg = user + (f"\n\nYour previous answer was rejected. Fix ALL of these and answer again:\n{feedback}" if feedback else "")
        try:
            r = b.call(SYSTEM, msg, "record_pyramid", SCHEMA, 6000)
        except RuntimeError as e:
            log(f"{field} stop: {e}"); break
        its = expand(r, items)
        bad_d = [d for d in r.get("dissolve") or [] if d not in items or not (items[d]["point"].get("support") or {}).get("points")]
        lids = {k for k, v in its.items() if not (v["point"].get("support") or {}).get("points")}
        errs = validate(r, list(its), lids, gids) + [f"dissolve id {d} is not an input group" for d in bad_d]
        if errs:
            feedback = "\n".join("- " + e for e in errs); log(f"{field} attempt {attempt+1} invalid: {feedback[:400]}")
            continue
        pyr = build(field, r, its)
        iss = minto_issues(pyr)
        bad = {k: v for k, v in iss.items() if v}
        pyr["minto_issues"] = bad
        view = {"governing_thought": pyr["governing_thought"], "key_line_dimension": r["dimension"],
                "pillars": [{"id": f"P{pi}", "statement": p["statement"],
                             "under": [{"id": f"P{pi}.{ci}", "statement": c.get("statement") or c.get("name"),
                                        "under": [(x.get("statement") or x.get("name") or "")[:140] for x in (c.get("support") or {}).get("points", [])][:5] if c.get("anchor", "").startswith("section:") else None}
                                       for ci, c in enumerate(p["support"]["points"], 1)]} for pi, p in enumerate(pyr["key_line"]["points"], 1)]}
        try:
            chk = b.call(CHECK_SYSTEM, "Check this pyramid:\n" + json.dumps(view, ensure_ascii=False, indent=1), "record_check", CHECK_SCHEMA, 2500)
        except RuntimeError as e:
            log(f"{field} stop: {e}"); break
        pyr["field_check"] = {"governing_thought": pyr["governing_thought"], "key_line": [p["statement"] for p in pyr["key_line"]["points"]],
                              "holds": bool(chk.get("holds")) and not bad, "note": chk.get("note", ""), "review": not chk.get("holds")}
        log(f"{field} attempt {attempt+1} minto_issues={sum(len(v) for v in bad.values())} holds={chk.get('holds')} note={chk.get('note')}")
        pyr["field_check"]["problems"] = int(chk.get("problems") or 0) + sum(len(v) for v in bad.values())
        if best is None or pyr["field_check"]["holds"] or pyr["field_check"]["problems"] < best["field_check"]["problems"]:
            best = pyr
        if pyr["field_check"]["holds"]:
            break
        pos = {f"P{pi}.{ci}": (c.get("id") or c.get("name")) for pi, p in enumerate(pyr["key_line"]["points"], 1) for ci, c in enumerate(p["support"]["points"], 1)}
        feedback = f"- minto_check problems: {bad}\n- top-down check said: {chk.get('note')}\n- position key for that note: {json.dumps(pos)}"
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
    ap.add_argument("--stage-cap", type=float, default=22.0); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    res = run(a.field, a.max_cost, a.stage_cap, a.dry_run)
    print(json.dumps(res))
