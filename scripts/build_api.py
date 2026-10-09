"""Build the static API (public/v1/*) and the Worker data bundle (worker/data.json).

Inputs: pyramids/*.md, registry/registry.json, engine/lexicon.json, site/site_data.json.
Outputs: public/v1/{index,warrants,methods,graph,skos}.json(ld), public/v1/field/XX.json,
         public/v1/id/<ID>.json, public/openapi.json, worker/data.json.
Run after scripts/build_registry.py. Everything here is generated; never edit by hand.
"""
import json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import taxonomy_engine as te  # constants only

VERSION = "2.2.0-api.1"
CODES = list(te.NAMES)
PUB = ROOT / "public" / "v1"
SECTION = re.compile(r"^## (\d+)\.\s*(.*)$", re.M)
ID_LINE = re.compile(r"^[\s|#>*-]*\**([A-Z]{2}\.[OMWB]\.[A-Z]?\d+(?:\.\d+)*)\b")
ID_ANY = re.compile(r"\b([A-Z]{2})(?:\.[OMWB]\.[A-Z]?\d+(?:\.\d+)*)?")


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")


def sections(text):
    marks = list(SECTION.finditer(text))
    out = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[int(m.group(1))] = {"title": m.group(2).strip(), "text": text[m.end():end].strip()}
    return out


def table_rows(md):
    rows = []
    for line in md.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:] if rows else []  # drop header


def clean(s):
    return re.sub(r"\*\*|`", "", s).strip()


registry = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
site = json.loads((ROOT / "site" / "site_data.json").read_text(encoding="utf-8"))
reg_by_id = {r["id"]: r for r in registry}

# ---- per-ID text from the pyramids ---------------------------------------------------------
id_text, field_sections = {}, {}
for code in CODES:
    src = (ROOT / "pyramids" / f"{code}.md").read_text(encoding="utf-8")
    field_sections[code] = sections(src)
    for line in src.splitlines():
        m = ID_LINE.match(line)
        if m and m.group(1) not in id_text and m.group(1).startswith(code + "."):
            id_text[m.group(1)] = clean(re.sub(r"^[\s|#>*-]+", "", line))[:1200]

# ---- field-level graph from "uses" ---------------------------------------------------------
edges = {a: {} for a in CODES}
used_by = {}
for r in registry:
    for u in r["uses"]:
        m = ID_ANY.match(u)
        tgt = m.group(1) if m else None
        if tgt in CODES and tgt != r["owner"]:
            edges[r["owner"]][tgt] = edges[r["owner"]].get(tgt, 0) + 1
        if u in reg_by_id:
            used_by.setdefault(u, []).append(r["id"])


def pagerank(edges, d=0.85, iters=100):
    """Rank fields by how much other fields depend on them (edge A->B means A uses B)."""
    n = len(CODES)
    rank = {c: 1 / n for c in CODES}
    for _ in range(iters):
        new = {c: (1 - d) / n for c in CODES}
        for a in CODES:
            out = edges[a]
            tot = sum(out.values())
            if tot == 0:
                for c in CODES:
                    new[c] += d * rank[a] / n
            else:
                for b, w in out.items():
                    new[b] += d * rank[a] * w / tot
        rank = new
    return {c: round(v, 5) for c, v in sorted(rank.items(), key=lambda kv: -kv[1])}


graph = {"edges": edges, "foundational_rank": pagerank(edges),
         "note": "Edge A->B counts registry rows owned by A that cite B. Field-level; ID-level citations are folded to their field."}
write(PUB / "graph.json", graph)

# ---- warrants and methods ------------------------------------------------------------------
write(PUB / "warrants.json", [{"code": k, "name": v, "default_method": te.WARRANT_TO_METHOD[k]}
                              for k, v in te.WARRANT_NAMES.items()])
write(PUB / "methods.json", [{"code": k, "name": v} for k, v in te.METHOD_NAMES.items()])

# ---- per-field files -----------------------------------------------------------------------
cellinfo = {}
index_fields = []
ma_text = (ROOT / "pyramids" / "MA.md").read_text(encoding="utf-8")
for code in CODES:
    sd = site["p"][code]
    secs = field_sections[code]
    warrants = []
    for row in table_rows(secs.get(6, {}).get("text", "")):
        if len(row) >= 4 and re.match(rf"^{code}\.", row[0]):
            cid = clean(row[0]).split()[0]  # some fields write "ID Label" in the first column
            warrants.append({"cell": cid, "warrant": clean(row[1]), "standard": clean(row[2]), "defeaters": clean(row[3])})
            cellinfo[cid] = {"warrant": warrants[-1]["warrant"], "standard": warrants[-1]["standard"], "defeaters": warrants[-1]["defeaters"]}
    if code == "MA":  # MA states "Warrant: ... Defeaters: ..." under each cell heading instead of a table
        for blk in re.split(r"(?m)^###+ ", ma_text)[1:]:
            cid = re.match(r"(MA\.O\.A\d)", blk)
            w = re.search(r"^Warrant:\s*(.+?)$", blk, re.M)
            if cid and w:
                std, _, dfs = w.group(1).partition("Defeaters:")
                warrants.append({"cell": cid.group(1), "warrant": "W1", "standard": std.strip().rstrip("."), "defeaters": dfs.strip().rstrip(".")})
                cellinfo[cid.group(1)] = warrants[-1] and {k: warrants[-1][k] for k in ("warrant", "standard", "defeaters")}
    objs = [r for r in registry if r["owner"] == code and ".O." in r["id"]]
    meths = [{"id": r["id"], "label": r["label"], "home": r["home"]} for r in registry if r["owner"] == code and ".M." in r["id"]]
    brid = [{"id": r["id"], "label": r["label"]} for r in registry if r["owner"] == code and ".B." in r["id"]]
    for row in table_rows(secs.get(5, {}).get("text", "")):
        if len(row) >= 3 and re.match(rf"^{code}\.M\.", row[0]) and not any(m["id"] == row[0] for m in meths):
            meths.append({"id": row[0], "label": row[1], "role": row[2], "example": row[3] if len(row) > 3 else None})
    cells = [{"id": f"{code}.O.A{i + 1}", "name": n} for i, n in enumerate(sd["cells"])]
    bridges_raw = table_rows(secs.get(7, {}).get("text", ""))
    out = {
        "code": code, "name": sd["name"], "dimension": sd.get("dim"), "cells": cells,
        "objects": [{"id": r["id"], "label": r["label"], "uses": r["uses"], "text": id_text.get(r["id"])} for r in objs],
        "methods": meths, "warrants": warrants, "bridges": brid, "bridges_table": bridges_raw,
        "sections": {"governing_thought": secs.get(2, {}).get("text"), "key_line": secs.get(3, {}).get("text"),
                     "assignment_rules": secs.get(8, {}).get("text"), "scope_boundary": secs.get(9, {}).get("text"),
                     "crosswalk": secs.get(10, {}).get("text"), "validation": secs.get(11, {}).get("text")},
        "borders": sorted(({"field": b, "uses": w} for b, w in edges[code].items()), key=lambda x: -x["uses"]),
        "cited_by": sorted(({"field": a, "uses": edges[a][code]} for a in CODES if code in edges[a]), key=lambda x: -x["uses"]),
        "status": "provisional until Maori-led review" if code == "IK" else "working draft for expert review",
    }
    write(PUB / "field" / f"{code}.json", out)
    index_fields.append({"code": code, "name": sd["name"], "dimension": sd.get("dim"), "cells": len(cells),
                         "ids": sum(1 for r in registry if r["owner"] == code), "url": f"/v1/field/{code}.json"})

# ---- per-ID files --------------------------------------------------------------------------
for r in registry:
    write(PUB / "id" / f"{r['id']}.json", {
        **r, "text": id_text.get(r["id"]),
        "used_by": sorted(used_by.get(r["id"], [])),
        "warrant": cellinfo.get(r["id"]) or cellinfo.get(".".join(r["id"].split(".")[:3])),
        "field_url": f"/v1/field/{r['owner']}.json"})

# ---- index ---------------------------------------------------------------------------------
write(PUB / "index.json", {
    "name": "Taxonomy", "version": VERSION, "ids": len(registry), "fields": index_fields,
    "warrants": len(te.WARRANT_NAMES), "methods": len(te.METHOD_NAMES),
    "licence": {
        "spdx": "CC-BY-4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
        "copyright": "Chris Townsend, 2026",
        "code": "Apache-2.0",
        "code_url": "https://www.apache.org/licenses/LICENSE-2.0",
    },
    "status": "Working draft. Placement reliability has not been measured by people. Indigenous placements are provisional."})

# ---- SKOS (JSON-LD, URN identifiers so no host is assumed) ---------------------------------
def urn(i):
    return {"@id": f"urn:taxonomy:{i}"}

concepts = [{"@id": "urn:taxonomy:scheme", "@type": "skos:ConceptScheme", "skos:prefLabel": "Taxonomy",
             "skos:hasTopConcept": [urn(c) for c in CODES],
             "dct:license": "https://creativecommons.org/licenses/by/4.0/",
             "dct:rightsHolder": "Chris Townsend"}]
for c in CODES:
    concepts.append({"@id": f"urn:taxonomy:{c}", "@type": "skos:Concept", "skos:prefLabel": te.NAMES[c],
                     "skos:topConceptOf": urn("scheme"), "skos:inScheme": urn("scheme")})
for r in registry:
    parts = r["id"].split(".")
    parent = ".".join(parts[:-1])
    broader = parent if parent in reg_by_id else r["owner"]
    node = {"@id": f"urn:taxonomy:{r['id']}", "@type": "skos:Concept", "skos:prefLabel": r["label"],
            "skos:inScheme": urn("scheme"), "skos:broader": urn(broader)}
    rel = []
    for u in r["uses"]:
        m = ID_ANY.match(u)
        if u in reg_by_id:
            rel.append(urn(u))
        elif m and m.group(1) in CODES and m.group(1) != r["owner"]:
            rel.append(urn(m.group(1)))
    if rel:
        node["skos:related"] = rel
    concepts.append(node)
write(PUB / "skos.jsonld", {"@context": {"skos": "http://www.w3.org/2004/02/skos/core#",
                                          "dct": "http://purl.org/dc/terms/"}, "@graph": concepts})

# ---- OpenAPI -------------------------------------------------------------------------------
def op(summary, params=None, body=None):
    o = {"summary": summary, "responses": {"200": {"description": "OK"}, "400": {"description": "Bad request"}}}
    if params:
        o["parameters"] = [{"name": n, "in": "query", "required": req, "schema": {"type": "string"}, "description": d}
                           for n, req, d in params]
    if body:
        o["requestBody"] = {"required": True, "content": {"application/json": {"schema": {
            "type": "object", "required": [body], "properties": {body: {"type": "string"}, "assist": {"type": "boolean"}}}}}}
    return o

write(ROOT / "public" / "openapi.json", {
    "openapi": "3.0.3",
    "info": {"title": "Taxonomy API", "version": VERSION,
             "description": "Place claims, look up identifiers, map a subject across 25 fields and audit wording against evidence. Rule-based; model assist is optional and never overrides the rules. The worker code is Apache-2.0. The taxonomy data is CC BY 4.0.",
             "license": {"name": "Apache-2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0"}},
    "paths": {
        "/v1/classify": {"get": op("Place one sentence", [("text", True, "The claim")]), "post": op("Place one sentence", body="text")},
        "/v1/audit": {"post": op("Check a passage: placement per sentence, evidence-type footer, wording flags", body="text")},
        "/v1/map": {"get": op("Whole view of a subject: fields, their cells, borders, evidence standards",
                              [("subject", True, "Subject or design brief"), ("top", False, "Fields to expand (default 8)"), ("assist", False, "1 = ask the model for extra fields")])},
        "/v1/view": {"get": op("Lens questions for all 25 fields", [("subject", True, "Subject")])},
        "/v1/relate": {"get": op("Border strength between two fields or IDs", [("a", True, "Field code or ID"), ("b", True, "Field code or ID")])},
        "/v1/lookup/{id}": {"get": {"summary": "One identifier", "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}, "404": {"description": "Unknown ID"}}}},
        "/v1/field/{code}.json": {"get": {"summary": "A whole field: cells, objects, methods, warrants, bridges", "parameters": [{"name": "code", "in": "path", "required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
        "/v1/index.json": {"get": {"summary": "Fields and counts", "responses": {"200": {"description": "OK"}}}},
        "/v1/graph.json": {"get": {"summary": "Field-to-field citation graph with foundational rank", "responses": {"200": {"description": "OK"}}}},
        "/v1/skos.jsonld": {"get": {"summary": "SKOS concept scheme (JSON-LD)", "responses": {"200": {"description": "OK"}}}},
    }})

# ---- named register (generated from pyramid text; never hand-edit) ---------
# Names are exact substrings of a pyramid line. A name that cannot be tied to a
# line is not invented. Rows are traced. Nothing outside the pyramids is added.
NAMED_RE = re.compile(
    r"(?<![\w–—-])([A-Z][\w'’\-]+(?:\s+[A-Z][\w'’\-]+){0,3}(?:'s|’s)?\s+(?:law|theorem|lemma|principle|equation|conjecture))\b")
STD_RE = re.compile(r"\b((?:IFRS|IAS|ISO/IEC|ISO)\s*\d+[A-Z0-9]*)\b")
named_rows, seen_names = [], set()
for code in CODES:
    src_path = ROOT / "pyramids" / f"{code}.md"
    for n, line in enumerate(src_path.read_text(encoding="utf-8").splitlines(), 1):
        hits = [(m.group(1), m.start(), "named") for m in NAMED_RE.finditer(line)]
        hits += [(m.group(1), m.start(), "standard") for m in STD_RE.finditer(line)]
        cols = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if len(cols) >= 2 and re.match(rf"^{code}\.M\.", cols[0]) and cols[1] and len(cols[1]) <= 48:
            hits.append((cols[1], 0, "method"))
        for name, start, kind in hits:
            name = name.strip()
            if kind != "method":
                first = name.split()[0]
                if first.lower() in {"the", "every", "each", "this", "first", "second", "third", "physical", "a", "an"}:
                    continue
                prefix = line[max(0, start - 16):start]
                if re.search(r"(?i)(van|von|de)\s+'?t?\s*$", prefix):
                    continue
            key = (code, name.lower(), kind)
            if key in seen_names:
                continue
            seen_names.add(key)
            quote = line.strip()
            traced = name in line
            named_rows.append({
                "name": name, "kind": kind, "field": code,
                "source": f"pyramids/{code}.md", "line": n, "quote": quote[:300],
                "trace": "traced" if traced else "(UNVERIFIED)",
            })
named_doc = {
    "note": "Generated by scripts/build_api.py from pyramid text. Every traced name is a substring of the cited line. This file adds no name the pyramids do not already contain. A row the extractor cannot tie to its line is marked (UNVERIFIED) and is not a finding that the name is false.",
    "names": named_rows,
}
write(PUB / "named.json", named_doc)
write(ROOT / "registry" / "named.json", named_doc)

# ---- Worker data bundle --------------------------------------------------------------------
write(ROOT / "worker" / "data.json", {
    "version": VERSION,
    "lexicon": te.LEXICON, "names": te.NAMES, "cells": te.CELLS,
    "warrantNames": te.WARRANT_NAMES, "methodNames": te.METHOD_NAMES,
    "defaultWarrant": te.DEFAULT_WARRANT, "warrantToMethod": te.WARRANT_TO_METHOD,
    "cellinfo": cellinfo, "graph": edges,
    "ids": {r["id"]: r["label"] for r in registry}})

# the bundle is minified: it ships inside the Worker
p = ROOT / "worker" / "data.json"
p.write_text(json.dumps(json.loads(p.read_text(encoding="utf-8")), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
top = list(graph["foundational_rank"])[:5]
print(f"{len(registry)} ids, {len(CODES)} fields, {len(cellinfo)} cell warrant rows; most-cited fields: {', '.join(top)}")
