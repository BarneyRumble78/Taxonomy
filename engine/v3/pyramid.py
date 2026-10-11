"""Build a Minto pyramid for one field from its published maps.

Orders follow Minto Chapter 6 (time, structure, degree). The key line is
inductive, which Chapter 5 prefers at that level. Groups are MECE in the
sense of Chapter 7: mutually exclusive, collectively exhaustive, and between
two and five members. This module does not call a language model. Nodes it
cannot place with a rule or a confident embedding go to a queue.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORDERS = ("time", "structure", "degree")
QUESTIONS = ("why", "how", "so_what", "which_ones")
OTHER = re.compile(r"\bother\b|not elsewhere classified|n\.e\.c\b", re.I)
WORD = re.compile(r"[A-Za-z0-9]+(?:[-–][A-Za-z0-9]+)?")


def normalise_name(name):
    text = (name or "").lower().replace("–", " ").replace("—", " ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_field_nodes(field):
    """Every map node for the field, tagged with its file and scheme."""
    index = _load_json(ROOT / "maps" / "index.json")
    primary = index[field]["primary"]
    nodes = []
    for path in sorted((ROOT / "maps" / field).glob("*.json")):
        data = _load_json(path)
        scheme = data.get("scheme") or path.name
        for node in data["nodes"]:
            item = dict(node)
            item["_file"] = f"maps/{field}/{path.name}"
            item["_scheme"] = scheme
            item["_primary"] = path.name == primary
            nodes.append(item)
    return nodes, primary


def dedupe_nodes(nodes):
    """Merge nodes with the same normalised name. The primary scheme supplies the name and the cell."""
    groups = defaultdict(list)
    for node in nodes:
        groups[normalise_name(node["name"])].append(node)
    merged = []
    id_map = {}
    for key, group in groups.items():
        if not key:
            continue
        group = sorted(group, key=lambda n: (not n["_primary"], n["_file"], n["id"]))
        keep = next((n for n in group if n["_primary"]), group[0])
        sources = [_source(n) for n in group]
        concept = {
            "id": keep["id"],
            "name": keep["name"],
            "cell": keep.get("taxonomy_cell"),
            "parent": keep.get("parent"),
            "sources": sources,
            "member_ids": [n["id"] for n in group],
        }
        for node in group:
            id_map[node["id"]] = keep["id"]
        merged.append(concept)
    by_id = {c["id"]: c for c in merged}
    for concept in merged:
        parent = concept.get("parent")
        if parent in id_map:
            parent = id_map[parent]
        if parent == concept["id"] or parent not in by_id:
            parent = None
        elif by_id[parent]["cell"] != concept["cell"]:
            parent = None
        concept["parent"] = parent
    return merged


def _source(node):
    return {"scheme": node["_scheme"], "id": node["id"], "code": node.get("code") or "", "file": node["_file"]}


def _sentence(text):
    words = WORD.findall(text)
    return len(words) >= 3 and text.endswith(".") and text.count(".") == 1 and bool(
        re.search(r"\b(is|are|places|holds|covers|follows|aims)\b", text)
    )


def keyword_facet(name, facets):
    """Longest keyword wins. Two facets tied at that length is not a rule."""
    low = name.lower()
    hits = []
    for facet in facets:
        best = 0
        for word in facet["keywords"]:
            token = re.escape(word.lower())
            pattern = r"\b" + token + (r"\b" if len(word) <= 5 else "")
            if re.search(pattern, low):
                best = max(best, len(word))
        if best:
            hits.append((best, facet["key"]))
    if not hits:
        return None
    hits.sort(reverse=True)
    if len(hits) > 1 and hits[0][0] == hits[1][0] and hits[0][1] != hits[1][1]:
        return None
    return hits[0][1]


def _cosine(a, b):
    return sum(x * y for x, y in zip(a, b))


def _embed(texts):
    import sys
    engine = ROOT / "engine"
    if str(engine) not in sys.path:
        sys.path.insert(0, str(engine))
    from taxonomy_engine import embed_queries
    return embed_queries(list(texts))


def _article(noun):
    return "an" if (noun or "")[:1].lower() in "aeiou" else "a"


FILLER = re.compile(
    r"is the class that holds|\bis (?:a|an) (?:pressure|measured state|impact|response|limit)\b",
    re.I,
)
STOP = {
    "the", "a", "an", "of", "and", "or", "in", "on", "for", "to", "from", "with",
    "by", "at", "as", "into", "over", "under", "its", "their", "this", "that",
}
KIND_PATTERNS = (
    ("response", re.compile(r"\b(treatments?|controls?|management|polic(?:y|ies)|protections?|regulations?|remediations?|remediat\w*|legislations?|plannings?|directives?)\b", re.I), "responses"),
    ("population", re.compile(r"\b(populations?|peoples?|people|demographics?|workforces?|inhabitants?)\b", re.I), "populations"),
    ("flow", re.compile(r"\b(flows?|fluxes|flux|runoffs?)\b", re.I), "flows"),
    ("activity", re.compile(r"\b(industr(?:y|ies)|husbandry|farming|agricultures?|logging|harvests?|mining|fishings?|fisher(?:y|ies)|cultivations?|grazings?|extractions?|abstractions?)\b", re.I), "activities"),
    ("place", re.compile(r"\b(city|cities|oceans?|lakes?|basins?|rivers?|seas?|coasts?|coastal|regions?|geograph\w*|zones?|settlements?|areas?)\b", re.I), "places"),
    ("organism", re.compile(r"\b(species|pests?|animals?|plants?|biota|fauna|flora|organisms?|wildlife)\b", re.I), "organisms"),
    ("substance", re.compile(r"\b(wastes?|pollutants?|fertilisers?|fertilizers?|sewage|chemicals?|fuels?|sludges?|pesticides?|emissions?|effluents?)\b", re.I), "substances"),
    ("condition", re.compile(r"\b(levels?|concentrations?|quality|composition|temperatures?|climates?|ozone|status)\b", re.I), "conditions"),
    ("institution", re.compile(r"\b(agenc(?:y|ies)|laws?|programmes?|programs?|measures?|standards?|lev(?:y|ies))\b", re.I), "institutions"),
)
KIND_PLURAL = {key: plural for key, _pat, plural in KIND_PATTERNS}
ROLE_CELL = {"response": "EV.O.A4", "state": "EV.O.A2"}


def is_filler(statement):
    """A parent that only names its topic, or calls itself a class that holds its members."""
    return bool(FILLER.search(statement or ""))


def _term_pattern(term):
    if term.endswith("y"):
        return re.compile(r"\b" + re.escape(term[:-1]) + r"(?:y|ies)\b", re.I)
    return re.compile(r"\b" + re.escape(term) + r"s?\b", re.I)


def dpsir_role(name, rules):
    """Response words, resource stocks, and ambiguous phrases, in that order.

    The cell definitions in rules['dpsir'] are applied before any embedding.
    """
    text = name or ""
    for term in rules.get("response_terms") or []:
        if _term_pattern(term).search(text):
            return "response"
    low = text.lower()
    for phrase in rules.get("ambiguous_phrases") or []:
        if phrase.lower() in low:
            return "ambiguous"
    for term in rules.get("state_resources") or []:
        if _term_pattern(term).search(text):
            return "state"
    return None


def apply_dpsir(concepts, rules):
    """Move concepts whose wording contradicts the map cell. Ambiguous names are queued."""
    queued = []
    for concept in concepts:
        role = dpsir_role(concept["name"], rules)
        concept["dpsir_role"] = role
        concept["dpsir_skip"] = False
        if role == "ambiguous":
            concept["dpsir_skip"] = True
            queued.append({
                "task": "place",
                "node_id": concept["id"],
                "name": concept["name"],
                "cell": concept.get("cell"),
                "reason": "the DPSIR role is ambiguous",
                "margin": None,
                "candidates": [
                    {"cell": cell, "facet": None, "score": None}
                    for cell in ("EV.O.A1", "EV.O.A2", "EV.O.A3", "EV.O.A4", "EV.O.A5")
                ],
            })
        elif role in ROLE_CELL:
            concept["cell"] = ROLE_CELL[role]
    by_id = {concept["id"]: concept for concept in concepts}
    for concept in concepts:
        parent = concept.get("parent")
        if (
            not parent
            or parent not in by_id
            or by_id[parent].get("cell") != concept.get("cell")
            or by_id[parent].get("dpsir_skip")
            or concept.get("dpsir_skip")
        ):
            concept["parent"] = None
    return queued


def kind_of(name):
    """One kind of thing. Response words win, then population, flow, activity, and the rest."""
    for key, pattern, _plural in KIND_PATTERNS:
        if pattern.search(name or ""):
            return key
    return "unsorted"


def kind_plural(kind):
    if kind in KIND_PLURAL:
        return KIND_PLURAL[kind]
    if kind.startswith("word:"):
        return kind.split(":", 1)[1]
    return "ideas"


def _tokens(name):
    return [token.lower() for token in WORD.findall(name or "") if token.lower() not in STOP and len(token) > 2]


def common_word(names):
    lists = [_tokens(name) for name in names]
    if not lists or any(not tokens for tokens in lists):
        return None
    shared = set(lists[0])
    for tokens in lists[1:]:
        shared &= set(tokens)
    if not shared:
        return None
    return max(shared, key=len)


def _noun_plural(noun):
    parts = (noun or "idea").split()
    if not parts[-1].endswith("s"):
        parts[-1] += "s"
    return " ".join(parts)


def _leaf_names(points):
    """Concept names under a group, skipping labels this builder wrote onto class points."""
    names = []
    for point in points:
        anchor = str(point.get("anchor") or "")
        if anchor.startswith("node:"):
            names.append(point.get("name") or "")
            continue
        below = (point.get("support") or {}).get("points") or []
        found = _leaf_names(below)
        names.extend(found or [point.get("name") or ""])
    return names


def summarise_names(names, noun, kind):
    """A sentence about the children's common feature. Weak cases are flagged, not filled with a topic label."""
    plural = kind_plural(kind)
    feature = common_word(names)
    banned = {plural.lower(), kind.lower()}
    if kind.startswith("word:"):
        banned.add(kind.split(":", 1)[1].lower())
    banned_stems = {word.rstrip("s") for word in banned}
    if feature and (feature.lower() in banned or feature.lower().rstrip("s") in banned_stems):
        feature = None
    noun_p = _noun_plural(noun)
    if feature:
        statement = f"These {plural} are the {feature} {noun_p}."
        needs = False
    else:
        statement = f"These {plural} are alike as {noun_p}."
        needs = True
    if is_filler(statement) or not _sentence(statement) or len(WORD.findall(statement)) > 25:
        statement = f"These {plural} are alike as {noun_p}."
        needs = True
    return statement, needs, feature or plural


def assign_facets(concepts, cell_rule, margin, vectors, floor):
    """Place concepts into the cell's facets. Returns (placed, queued).

    placed: concept id -> {facet, method}
    A keyword, or a parent placed by a keyword, is a rule. An embedding is
    used only when the gap over the next facet is at least `margin` and the
    score against that facet is at least `floor`.
    """
    facets = cell_rule["facets"]
    by_key = {f["key"]: f for f in facets}
    in_cell = [c for c in concepts if c["cell"] == cell_rule["cell"]]
    by_id = {c["id"]: c for c in in_cell}
    children = defaultdict(list)
    for concept in in_cell:
        if concept.get("parent") in by_id:
            children[concept["parent"]].append(concept["id"])
    placed = {}
    ambiguous = []
    for concept in in_cell:
        if concept.get("dpsir_skip") or OTHER.search(concept["name"]):
            continue
        role = concept.get("dpsir_role")
        if role == "response" and cell_rule["cell"] != "EV.O.A4":
            continue
        if role == "state" and cell_rule["cell"] != "EV.O.A2":
            continue
        facet = keyword_facet(concept["name"], facets)
        if facet:
            placed[concept["id"]] = {"facet": facet, "method": "rule"}
        else:
            ambiguous.append(concept["id"])
    # Hierarchy: an unplaced child takes a parent that a keyword rule placed.
    changed = True
    while changed:
        changed = False
        for concept in in_cell:
            if concept["id"] in placed or concept.get("dpsir_skip") or OTHER.search(concept["name"]):
                continue
            role = concept.get("dpsir_role")
            if role == "ambiguous":
                continue
            if role == "response" and cell_rule["cell"] != "EV.O.A4":
                continue
            if role == "state" and cell_rule["cell"] != "EV.O.A2":
                continue
            parent = concept.get("parent")
            if parent in placed and placed[parent]["method"] == "rule":
                placed[concept["id"]] = {"facet": placed[parent]["facet"], "method": "rule"}
                changed = True
    queued = []
    facet_vecs = {f["key"]: vectors[f["statement"]] for f in facets}
    for cid in ambiguous:
        if cid in placed or OTHER.search(by_id[cid]["name"]):
            continue
        vec = vectors[by_id[cid]["name"]]
        scored = sorted(((_cosine(vec, facet_vecs[key]), key) for key in facet_vecs), reverse=True)
        best, second = scored[0], scored[1] if len(scored) > 1 else (0.0, None)
        gap = best[0] - second[0]
        if gap >= margin and best[0] >= floor:
            placed[cid] = {"facet": best[1], "method": "embedding", "margin": round(gap, 4)}
        else:
            if best[0] < floor:
                reason = f"embedding score {best[0]:.4f} is below {floor:.4f}"
            else:
                reason = f"embedding gap {gap:.4f} is below {margin:.4f}"
            queued.append({
                "node_id": cid,
                "name": by_id[cid]["name"],
                "cell": cell_rule["cell"],
                "reason": reason,
                "margin": round(gap, 4),
                "candidates": [{"facet": key, "score": round(score, 4)} for score, key in scored],
            })
    for concept in in_cell:
        if concept["id"] in placed or any(q["node_id"] == concept["id"] for q in queued):
            continue
        if OTHER.search(concept["name"]):
            queued.append({
                "node_id": concept["id"],
                "name": concept["name"],
                "cell": cell_rule["cell"],
                "reason": "the source name is an Other bucket",
                "margin": None,
                "candidates": [{"facet": f["key"], "score": None} for f in facets],
            })
    return placed, queued, by_id, children, by_key


class IdBook:
    """Stable ids. An anchor keeps its id. A missing anchor is retired, never reused."""

    def __init__(self, field, previous):
        self.field = field
        self.used = set()
        self.by_anchor = {}
        self.retired = []
        self._seen = set()
        if previous:
            self.retired = list(previous.get("retired") or [])
            for item in self.retired:
                self.used.add(item["id"])
            for point in _walk_points(previous.get("key_line", {}).get("points") or []):
                anchor = point.get("anchor")
                if anchor:
                    self.by_anchor[anchor] = point["id"]
                    self.used.add(point["id"])

    def get(self, parent_id, anchor):
        self._seen.add(anchor)
        if anchor in self.by_anchor:
            return self.by_anchor[anchor]
        n = 1
        while True:
            cand = f"{parent_id}.{n}"
            if cand not in self.used:
                break
            n += 1
        self.used.add(cand)
        self.by_anchor[anchor] = cand
        return cand

    def finish(self):
        for anchor, pid in list(self.by_anchor.items()):
            if anchor not in self._seen and not any(r["id"] == pid for r in self.retired):
                self.retired.append({"id": pid, "anchor": anchor, "replaced_by": None, "status": "RETIRED"})
        return self.retired


def _walk_points(points):
    for point in points:
        yield point
        support = point.get("support") or {}
        yield from _walk_points(support.get("points") or [])


def _point(pid, anchor, statement, sources, idea_type="situation"):
    return {
        "id": pid,
        "anchor": anchor,
        "statement": statement,
        "idea_type": idea_type,
        "sources": sources,
    }


def _group(points, plural, dimension, order, question):
    return {
        "logic_type": "inductive",
        "plural_noun": plural,
        "mece_dimension": dimension,
        "order": order,
        "question_raised": question,
        "points": points,
    }


def _cap(name):
    text = name.strip()
    return text[:1].upper() + text[1:] if text else text


def _dedupe_sources(sources):
    out, seen = [], set()
    for src in sources:
        key = (src.get("file"), src.get("id"))
        if key in seen:
            continue
        seen.add(key)
        out.append(src)
    return out


def _clean_name(name, max_words):
    text = (name or "").replace("–", " ").replace("—", " ")
    text = re.sub(r"[.()\[\]{}:;!?\"/\\]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" ,;/-")
    words = text.split()
    if len(words) > max_words:
        words = words[:max_words]
    return " ".join(words)


def _fit_statement(name, tail):
    """One sentence, at most 25 words, with a verb and a single period."""
    words = _clean_name(name, 40).split()
    while words:
        statement = f"{_cap(' '.join(words))} {tail}."
        if (
            _sentence(statement)
            and len(WORD.findall(statement)) <= 25
            and not re.search(r"(?i)\bthere are\b", statement)
        ):
            return statement
        words.pop()
    return f"This item {tail}."


def _short(name):
    return _clean_name(name, 8) or "this group"


def pack_concepts(placed, by_id, children, facet_key, ids, parent_id, noun, vectors):
    """Group one facet into MECE sets of two to five.

    Source hierarchy is kept when a parent has two or more children in the
    facet (Chapter 6, structural order). A single child is collapsed onto its
    parent as provenance. A wider set is split by embeddings and every member
    stays in some group (Chapter 6, degree). The medoid is a child point as
    well as the name of the class. Returns a dict with points, collapsed ids,
    and any ids that still had to be queued.
    """
    members = [cid for cid, info in placed.items() if info["facet"] == facet_key and cid in by_id]
    incoming = list(members)
    # Keyword groups lead. An embedding joins the nearest keyword idea only when it is
    # actually near that idea; otherwise it stays in the queue.
    children = defaultdict(list, {parent: list(kids) for parent, kids in children.items()})
    virtual_parent = {}
    rule_members = [cid for cid in members if placed[cid]["method"] == "rule"]
    if len(rule_members) >= 2 and vectors:
        kept = []
        for cid in members:
            if placed[cid]["method"] == "rule":
                kept.append(cid)
                continue
            vec = vectors.get(by_id[cid]["name"])
            if not vec:
                continue
            host = max(rule_members, key=lambda rid: _cosine(vec, vectors.get(by_id[rid]["name"], [])))
            host_vec = vectors.get(by_id[host]["name"])
            if host_vec and _cosine(vec, host_vec) >= 0.62:
                source_parent = by_id[cid].get("parent")
                if source_parent in children:
                    children[source_parent] = [kid for kid in children[source_parent] if kid != cid]
                if cid not in children[host]:
                    children[host].append(cid)
                virtual_parent[cid] = host
                kept.append(cid)
        members = kept
    member_set = set(members)
    queued = []
    for cid in incoming:
        if cid in member_set:
            continue
        concept = by_id[cid]
        queued.append({
            "node_id": cid,
            "name": concept["name"],
            "cell": concept["cell"],
            "reason": "not near a keyword idea in this facet",
            "margin": None,
            "candidates": [{"facet": facet_key, "score": None}],
        })
    if len(members) < 2:
        for cid in members:
            concept = by_id[cid]
            queued.append({
                "node_id": cid,
                "name": concept["name"],
                "cell": concept["cell"],
                "reason": "fewer than two ideas in the facet",
                "margin": None,
                "candidates": [],
            })
        return {"points": [], "queued": queued, "collapsed": [], "summaries": [], "order": "structure",
                "plural_noun": "kinds", "mece_dimension": f"parts of {facet_key}"}

    used = set()
    collapsed = []
    summary_items = []
    absorbed_by = {}
    queued_ids = set()

    def order_ids(cids):
        return sorted(cids, key=lambda i: (by_id[i]["name"].lower(), by_id[i]["id"]))

    def queue(cid, reason):
        if cid in queued_ids or cid in used or cid not in by_id:
            return
        queued_ids.add(cid)
        concept = by_id[cid]
        queued.append({
            "node_id": cid,
            "name": concept["name"],
            "cell": concept["cell"],
            "reason": reason,
            "margin": None,
            "candidates": [],
        })

    def reachable(starts):
        seen = set()
        stack = list(starts)
        while stack:
            cid = stack.pop()
            if cid in seen or cid not in member_set:
                continue
            seen.add(cid)
            for kid in children.get(cid, []):
                if kid in member_set and kid not in seen:
                    stack.append(kid)
        return seen

    def absorb(start):
        """Follow a unary chain to the first branch. The chain is collapsed."""
        node = start
        absorbed = []
        seen = set()
        while node not in seen:
            seen.add(node)
            kids = [k for k in children.get(node, []) if k in member_set and k not in seen]
            if len(kids) >= 2:
                absorbed.append(node)
                return kids, absorbed
            if len(kids) == 1:
                absorbed.append(node)
                node = kids[0]
                continue
            return None, []
        return None, []

    def partition(cids):
        """Two to five clusters, each of size at least two. Every id is kept."""
        if len(cids) <= 25:
            k = min(5, len(cids) // 2)
        else:
            k = min(5, len(cids) // 2, max(2, (len(cids) + 4) // 5))
        clusters = None
        if vectors and all(by_id[cid]["name"] in vectors for cid in cids):
            clusters = _cluster_all(cids, [vectors[by_id[cid]["name"]] for cid in cids], k)
        if not clusters:
            clusters = _chunk(cids, k, by_id)
        return clusters

    def _leaf_statements(points):
        lines = []
        for point in points:
            kids = (point.get("support") or {}).get("points") or []
            if kids:
                lines.extend(_leaf_statements(kids))
            else:
                lines.append(point["statement"])
        return lines

    def note_summary(point, below):
        if not point.get("needs_summary"):
            return
        cell = point.get("cell")
        if not cell:
            for child in below:
                if child.get("cell"):
                    cell = child["cell"]
                    break
        summary_items.append({
            "task": "summarise",
            "needs_summary": True,
            "node_id": point["id"],
            "point_id": point["id"],
            "name": point["statement"],
            "cell": cell,
            "reason": "needs a summary of the children",
            "children": _leaf_statements(below),
            "candidates": [],
        })

    def apply_summary(point, below, kind, order):
        names = _leaf_names(below)
        statement, needs, feature = summarise_names(names, noun, kind)
        point["statement"] = statement
        point["kind"] = kind
        point["name"] = feature
        point["needs_summary"] = needs
        point["question_raised"] = "which_ones"
        point["support"] = _group(below, kind_plural(kind), f"the {kind_plural(kind)}", order, "which_ones")
        note_summary(point, below)

    def one_kind(cids):
        """Keep the largest single kind. Other kinds are queued, not mixed in."""
        grouped = defaultdict(list)
        unsorted = []
        for cid in cids:
            kind = kind_of(by_id[cid]["name"])
            if kind == "unsorted":
                unsorted.append(cid)
            else:
                grouped[kind].append(cid)
        if unsorted:
            counts = defaultdict(int)
            token_sets = {}
            for cid in unsorted:
                token_sets[cid] = set(_tokens(by_id[cid]["name"]))
                for token in token_sets[cid]:
                    counts[token] += 1
            rest = list(unsorted)
            if counts:
                token = max(counts, key=lambda item: (counts[item], item))
                bucket = [cid for cid in unsorted if token in token_sets[cid]]
                if len(bucket) >= 2:
                    grouped["word:" + token] = bucket
                    rest = [cid for cid in unsorted if cid not in set(bucket)]
            for cid in rest:
                queue(cid, "no shared kind with another idea")
        for kind, group in list(grouped.items()):
            if len(group) < 2:
                for cid in group:
                    queue(cid, "fewer than two ideas of this kind")
                del grouped[kind]
        if not grouped:
            return [], None
        kind = max(grouped, key=lambda item: (len(grouped[item]), item))
        for other, group in grouped.items():
            if other == kind:
                continue
            for cid in group:
                queue(cid, "different kind from the group")
        return grouped[kind], kind

    def release(points):
        """Drop a subtree that is a different kind from its parent. Those ideas go back to the queue."""
        drop = {point["id"] for point in _walk_points(points)}
        cids = []
        for point in _walk_points(points):
            anchor = point.get("anchor") or ""
            if anchor.startswith("node:"):
                cids.append(anchor[5:])
        released = set()
        for cid in cids:
            for extra in absorbed_by.get(cid, []):
                used.discard(extra)
                released.add(extra)
                queue(extra, "different kind from the group")
            used.discard(cid)
            released.add(cid)
            queue(cid, "different kind from the group")
        collapsed[:] = [cid for cid in collapsed if cid not in released]
        summary_items[:] = [item for item in summary_items if item.get("point_id") not in drop]

    def make_point(cid, pid_parent, link):
        if cid in used:
            return None
        absorbed_local = []
        kids = []
        if link:
            node = cid
            seen = {cid}
            while True:
                nxt = []
                seen_kids = set()
                for kid in children.get(node, []):
                    if kid in member_set and kid not in seen and kid not in used and kid not in seen_kids:
                        seen_kids.add(kid)
                        nxt.append(kid)
                if len(nxt) == 1:
                    absorbed_local.append(nxt[0])
                    seen.add(nxt[0])
                    node = nxt[0]
                    continue
                if len(nxt) >= 2:
                    kids = nxt
                break
        used.add(cid)
        absorbed_by[cid] = list(absorbed_local)
        for extra in absorbed_local:
            used.add(extra)
            collapsed.append(extra)
        sources = _dedupe_sources(
            [src for extra_id in [cid] + absorbed_local for src in by_id[extra_id]["sources"]]
        )
        statement = _fit_statement(by_id[cid]["name"], f"is {_article(noun)} {noun}")
        pid = ids.get(pid_parent, f"node:{cid}")
        point = _point(pid, f"node:{cid}", statement, sources)
        point["placement"] = placed[cid]["method"]
        point["kind"] = kind_of(by_id[cid]["name"])
        point["name"] = by_id[cid]["name"]
        point["cell"] = by_id[cid]["cell"]
        point["needs_summary"] = False
        if len(kids) >= 2:
            kept, child_kind = one_kind(list(kids))
            if child_kind == point["kind"] and len(kept) >= 2:
                below = split_into_points(kept, pid, True)
                if 2 <= len(below) <= 5 and {child.get("kind") for child in below} == {point["kind"]}:
                    order = "structure" if all(child["anchor"].startswith("node:") for child in below) else "degree"
                    apply_summary(point, below, point["kind"], order)
                elif below:
                    release(below)
            else:
                for child_id in kept:
                    queue(child_id, "different kind from the group")
        return point

    def _summarise_class(sid, anchor, below, kind):
        if not 2 <= len(below) <= 5:
            if below:
                release(below)
            return None
        summary = _point(
            sid,
            anchor,
            f"These {kind_plural(kind)} are alike as {_noun_plural(noun)}.",
            _dedupe_sources([src for point in _walk_points(below) for src in point["sources"]]),
        )
        summary["placement"] = "embedding"
        summary["cell"] = below[0].get("cell")
        apply_summary(summary, below, kind, "degree")
        return summary

    def _bucket_point(bucket, pid_parent, link, kind):
        bucket = [cid for cid in bucket if cid not in used]
        if len(bucket) < 2:
            return None
        medoid = min(bucket, key=lambda cid: (by_id[cid]["name"].lower(), cid))
        anchor = f"class:{pid_parent}:{medoid}"
        sid = ids.get(pid_parent, anchor)
        if len(bucket) <= 5:
            below = []
            for cid in order_ids(bucket):
                point = make_point(cid, sid, link)
                if point is not None:
                    below.append(point)
            return _summarise_class(sid, anchor, below, kind)
        ordered = order_ids(bucket)
        k = min(5, max(2, len(ordered) // 2))
        size = len(ordered) // k
        extra = len(ordered) % k
        below = []
        start = 0
        for index in range(k):
            stop = start + size + (1 if index < extra else 0)
            chunk = ordered[start:stop]
            start = stop
            if len(chunk) < 2:
                continue
            child = _bucket_point(chunk, sid, link, kind)
            if child:
                below.append(child)
        return _summarise_class(sid, anchor, below, kind)

    def _feature_points(cids, pid_parent, link, kind):
        """Up to five groups that each share a content word, so the summary can name it."""
        token_sets = {cid: set(_tokens(by_id[cid]["name"])) for cid in cids}
        counts = defaultdict(int)
        for cid in cids:
            for token in token_sets[cid]:
                counts[token] += 1
        tokens = sorted(
            (token for token, count in counts.items() if count >= 2),
            key=lambda token: (-counts[token], -len(token), token),
        )
        groups = []
        taken = set()
        for token in tokens:
            bucket = [cid for cid in cids if cid not in taken and token in token_sets[cid]]
            if len(bucket) >= 2:
                groups.append(bucket)
                taken.update(bucket)
        if len(groups) < 2:
            return None
        groups.sort(key=lambda bucket: (-len(bucket), by_id[bucket[0]]["name"].lower(), bucket[0]))
        kept, extra_groups = groups[:5], groups[5:]
        points = []
        for bucket in kept:
            point = _bucket_point(bucket, pid_parent, link, kind)
            if point:
                points.append(point)
        if not 2 <= len(points) <= 5:
            for point in points:
                release([point])
            return None
        for bucket in extra_groups:
            for cid in bucket:
                queue(cid, "not in a group of two to five")
        for cid in cids:
            if cid not in taken:
                queue(cid, "no shared feature with another idea")
        return points

    def split_into_points(cids, pid_parent, link):
        cids = [cid for cid in cids if cid not in used]
        if len(cids) < 2:
            return []
        cids, kind = one_kind(cids)
        if len(cids) < 2 or not kind:
            return []
        if len(cids) <= 5:
            points = []
            for cid in order_ids(cids):
                point = make_point(cid, pid_parent, link)
                if point is not None:
                    points.append(point)
            return points
        featured = _feature_points(cids, pid_parent, link, kind)
        if featured:
            return featured
        clusters = partition(cids)
        clusters = sorted(clusters, key=lambda cl: (-len(cl), by_id[cl[0]]["name"].lower(), cl[0]))
        points = []
        for cluster in clusters:
            medoid = cluster[0]
            anchor = f"class:{pid_parent}:{medoid}"
            sid = ids.get(pid_parent, anchor)
            if len(cluster) <= 5:
                ordered = [medoid] + order_ids([c for c in cluster if c != medoid])
                below = []
                for cid in ordered:
                    point = make_point(cid, sid, link)
                    if point is not None:
                        below.append(point)
            else:
                below = split_into_points(cluster, sid, link)
            if not 2 <= len(below) <= 5:
                if below:
                    release(below)
                continue
            summary = _point(
                sid,
                anchor,
                f"These {kind_plural(kind)} are alike as {_noun_plural(noun)}.",
                _dedupe_sources([src for point in _walk_points(below) for src in point["sources"]]),
            )
            summary["placement"] = "embedding"
            summary["cell"] = below[0].get("cell")
            apply_summary(summary, below, kind, "degree")
            points.append(summary)
        return points

    roots = [cid for cid in members if virtual_parent.get(cid, by_id[cid].get("parent")) not in member_set]
    top_ids = None
    pre = []
    link = True
    if len(roots) >= 2 and reachable(roots) == member_set:
        top_ids = roots
    elif len(roots) == 1:
        kids, absorbed = absorb(roots[0])
        if kids and set(absorbed) | reachable(kids) == member_set:
            top_ids = kids
            pre = absorbed
    if top_ids is None:
        top_ids = list(members)
        link = False
        pre = []
    for cid in pre:
        used.add(cid)
        collapsed.append(cid)
    points = split_into_points(top_ids, parent_id, link)
    if not 2 <= len(points) <= 5:
        for cid in members:
            if cid not in used:
                queue(cid, "the facet did not form a group of two to five")
        return {"points": [], "queued": queued, "collapsed": [], "summaries": [], "order": "structure",
                "plural_noun": "kinds", "mece_dimension": f"parts of {facet_key}"}
    for cid in members:
        if cid not in used:
            queue(cid, "not in a group of two to five")
    if all(p["anchor"].startswith("node:") for p in points):
        order, plural, dimension = "structure", "kinds", f"parts of {facet_key}"
    else:
        order, plural, dimension = "degree", "classes", f"classes within {facet_key}"
    return {
        "points": points,
        "queued": queued,
        "collapsed": [cid for cid in collapsed if cid not in {p["anchor"][5:] for p in _walk_points(points) if p["anchor"].startswith("node:")}],
        "order": order,
        "plural_noun": plural,
        "mece_dimension": dimension,
        "summaries": summary_items,
    }


def _chunk(cids, k, by_id):
    ordered = sorted(cids, key=lambda i: (by_id[i]["name"].lower(), by_id[i]["id"]))
    k = max(2, min(k, len(ordered) // 2))
    buckets = [[] for _ in range(k)]
    for index, cid in enumerate(ordered):
        buckets[index % k].append(cid)
    return [bucket for bucket in buckets if bucket]


def _central_first(cluster, vecs):
    """Name a class by its most typical member, which is also a child of the class."""
    if len(cluster) < 2:
        return list(cluster)
    try:
        import numpy as np
        matrix = np.asarray(vecs, dtype=np.float32)
        choice = int((matrix @ matrix.T).sum(axis=1).argmax())
    except Exception:
        choice = max(range(len(cluster)), key=lambda i: sum(_cosine(vecs[i], vecs[j]) for j in range(len(vecs))))
    cid = cluster[choice]
    return [cid] + [other for other in cluster if other != cid]


def _cluster_all(cids, vecs, k):
    """Balanced degree split. Every id is kept. The central member of each class is first."""
    k = min(k, len(cids) // 2)
    if k < 2:
        return None
    try:
        import numpy as np
        matrix = np.asarray(vecs, dtype=np.float32)
        direction = matrix[0]
        for _ in range(8):
            direction = matrix.T @ (matrix @ direction)
            norm = float(np.linalg.norm(direction))
            if norm == 0:
                break
            direction = direction / norm
        projection = matrix @ direction
        order = [cids[i] for i in np.argsort(projection, kind="mergesort")]
        ordered_vecs = [vecs[cids.index(cid)] for cid in order]
    except Exception:
        order = sorted(cids)
        ordered_vecs = list(vecs)
    buckets = [[] for _ in range(k)]
    bucket_vecs = [[] for _ in range(k)]
    size = len(order) // k
    extra = len(order) % k
    start = 0
    for index in range(k):
        stop = start + size + (1 if index < extra else 0)
        buckets[index] = order[start:stop]
        bucket_vecs[index] = ordered_vecs[start:stop]
        start = stop
    clusters = [_central_first(bucket, vec) for bucket, vec in zip(buckets, bucket_vecs) if len(bucket) >= 2]
    if not 2 <= len(clusters) <= 5:
        return None
    return clusters


def build_pyramid(field, embed=True):
    rules = _load_json(ROOT / "pyramids" / "rules" / f"{field}.json")
    nodes, _primary = load_field_nodes(field)
    concepts = dedupe_nodes(nodes)
    # Cell definitions in rules["dpsir"] move or queue a concept before any embedding.
    dpsir_queue = apply_dpsir(concepts, rules)
    previous = None
    path = ROOT / "pyramids" / f"{field}.json"
    if path.exists():
        try:
            previous = _load_json(path)
        except json.JSONDecodeError:
            previous = None
    ids = IdBook(field, previous if previous and previous.get("field") == field else None)
    margin = float(rules["margin"])
    floor = float(rules.get("embed_floor", 0.62))
    texts = {c["name"] for c in concepts}
    for cell in rules["cells"]:
        texts.add(cell["statement"])
        for facet in cell["facets"]:
            texts.add(facet["statement"])
    vectors = {}
    if embed:
        ordered = sorted(texts)
        embedded = _embed(ordered)
        vectors = dict(zip(ordered, embedded))
    key_points = []
    queue = list(dpsir_queue)
    summary_items = []
    rule_ids = set()
    embed_ids = set()
    def _note(concept_id):
        bucket = rule_ids if placed[concept_id]["method"] == "rule" else embed_ids
        bucket.add(concept_id)

    for cell in rules["cells"]:
        placed, queued, by_id, children, _by_key = assign_facets(concepts, cell, margin, vectors, floor)
        claimed = set()
        for facet in cell["facets"]:
            members = [concept_id for concept_id, info in placed.items() if info["facet"] == facet["key"]]
            if members:
                continue
            best_item, best_score = None, None
            for item in queued:
                if item["node_id"] in claimed or item["reason"].startswith("the source name is an Other"):
                    continue
                for cand in item.get("candidates") or []:
                    score = cand.get("score")
                    if cand.get("facet") == facet["key"] and score is not None and (best_score is None or score > best_score):
                        best_item, best_score = item, score
            if best_item:
                claimed.add(best_item["node_id"])
                placed[best_item["node_id"]] = {"facet": facet["key"], "method": "embedding"}
        queue.extend(item for item in queued if item["node_id"] not in claimed)
        cid = ids.get(f"{field}.P", f"cell:{cell['cell']}")
        facet_points = []
        for facet in cell["facets"]:
            members = [concept_id for concept_id, info in placed.items() if info["facet"] == facet["key"]]
            anchor = f"facet:{cell['cell']}:{facet['key']}"
            fid = ids.get(cid, anchor)
            if len(members) < 2:
                if len(members) != 1:
                    ids._seen.discard(anchor)
                    continue
                concept_id = members[0]
                _note(concept_id)
                facet_point = _point(fid, anchor, facet["statement"], by_id[concept_id]["sources"])
                facet_point["facet"] = facet["key"]
                facet_points.append(facet_point)
                continue
            packed = pack_concepts(
                placed, by_id, children, facet["key"], ids, fid, cell["noun"], vectors,
            )
            if not 2 <= len(packed["points"]) <= 5:
                ids._seen.discard(anchor)
                for concept_id in members:
                    if any(item["node_id"] == concept_id for item in queue):
                        continue
                    concept = by_id[concept_id]
                    queue.append({
                        "node_id": concept_id,
                        "name": concept["name"],
                        "cell": cell["cell"],
                        "reason": "the facet did not form a group of two to five",
                        "margin": None,
                        "candidates": [{"facet": facet["key"], "score": None}],
                    })
                continue
            queue.extend(packed["queued"])
            summary_items.extend(packed.get("summaries") or [])
            noted = set()
            for point in _walk_points(packed["points"]):
                if point.get("anchor", "").startswith("node:"):
                    concept_id = point["anchor"][5:]
                    noted.add(concept_id)
                    _note(concept_id)
            for concept_id in packed["collapsed"]:
                if concept_id in noted or concept_id not in placed:
                    continue
                noted.add(concept_id)
                _note(concept_id)
            sources = _dedupe_sources(
                [src for point in _walk_points(packed["points"]) for src in point["sources"]]
                + [src for concept_id in packed["collapsed"] for src in by_id[concept_id]["sources"]]
            )
            facet_point = _point(fid, anchor, facet["statement"], sources)
            facet_point["facet"] = facet["key"]
            facet_point["question_raised"] = "which_ones"
            facet_point["support"] = _group(
                packed["points"],
                packed["plural_noun"],
                packed["mece_dimension"],
                packed["order"],
                "which_ones",
            )
            facet_points.append(facet_point)
        if not 2 <= len(facet_points) <= 5:
            raise SystemExit(f"{cell['cell']} has {len(facet_points)} facets; a group needs two to five")
        cell_sources = _dedupe_sources([src for facet_point in facet_points for src in facet_point["sources"]])
        cell_point = _point(cid, f"cell:{cell['cell']}", cell["statement"], cell_sources)
        cell_point["cell"] = cell["cell"]
        cell_point["question"] = cell.get("question")
        cell_point["question_raised"] = cell["question_raised"]
        cell_point["support"] = _group(
            facet_points, cell["plural_noun"], cell["mece_dimension"], cell["order"], cell["question_raised"],
        )
        key_points.append(cell_point)
        print(f"{cell['cell']}: {len(facet_points)} facets", file=sys.stderr)
    # Fill candidate group ids now that facet ids exist.
    facet_ids = {}
    cell_ids = {}
    for point in key_points:
        cell_ids[point["cell"]] = {"group_id": point["id"], "statement": point["statement"]}
        for facet in point["support"]["points"]:
            facet_ids[(point["cell"], facet.get("facet"))] = {
                "group_id": facet["id"],
                "statement": facet["statement"],
            }
    for item in queue:
        item.setdefault("task", "place")
        enriched = []
        for cand in item.get("candidates") or []:
            cell = cand.get("cell") or item.get("cell")
            facet = cand.get("facet")
            if facet:
                found = facet_ids.get((cell, facet))
            elif cell:
                found = cell_ids.get(cell)
            else:
                found = None
            enriched.append({**cand, **found} if found else cand)
        item["candidates"] = enriched
    retired = ids.finish()
    pyramid = {
        "field": field,
        "audience": rules["audience"],
        "introduction": rules["introduction"],
        "governing_thought": rules["governing_thought"],
        "key_line": {
            "logic_type": rules["key_line"]["logic_type"],
            "plural_noun": rules["key_line"]["plural_noun"],
            "mece_dimension": rules["key_line"]["mece_dimension"],
            "order": rules["key_line"]["order"],
            "question_raised": rules["key_line"]["question_raised"],
            "points": key_points,
        },
        "retired": retired,
        "review": {
            "situation_accepted": None,
            "complication_follows": None,
            "governing_thought_answers": None,
            "children_answer_the_question": None,
            "no_overlap": None,
            "summary_is_an_inference": None,
            "signed_by": None,
        },
        "build": {
            "nodes_in": len(nodes),
            "after_dedupe": len(concepts),
            "placed_by_rules": len(rule_ids),
            "placed_by_embeddings": len(embed_ids),
            "queued": 0,
            "margin": margin,
            "embed_floor": floor,
            "embedder": "BAAI/bge-small-en-v1.5",
            "orders": ["time", "structure", "degree"],
            "key_line_logic": "inductive",
        },
    }
    # Placed concepts include collapsed provenance. The queue is everyone else.
    placed_ids = rule_ids | embed_ids
    queue_ids = {item["node_id"] for item in queue}
    missing = [c for c in concepts if c["id"] not in placed_ids and c["id"] not in queue_ids]
    for concept in missing:
        queue.append({
            "node_id": concept["id"],
            "name": concept["name"],
            "cell": concept["cell"],
            "reason": "not placed in a group of two to five",
            "margin": None,
            "candidates": [],
        })
    deduped = []
    seen_q = set()
    for item in queue:
        item.setdefault("task", "place")
        if not item.get("candidates"):
            item["candidates"] = []
        if item["node_id"] in seen_q or item["node_id"] in placed_ids:
            continue
        seen_q.add(item["node_id"])
        deduped.append(item)
    reasons = {}
    for item in deduped:
        reason = item["reason"]
        if reason.startswith("embedding "):
            reason = "embedding below the recorded threshold"
        reasons[reason] = reasons.get(reason, 0) + 1
    pyramid["build"]["placed"] = len(placed_ids)
    pyramid["build"]["placed_by_rules"] = len(rule_ids)
    pyramid["build"]["placed_by_embeddings"] = len(embed_ids)
    pyramid["build"]["queued"] = len(deduped)
    pyramid["build"]["queue_reasons"] = reasons
    seen_summary = set()
    unique_summaries = []
    for item in summary_items:
        point_id = item.get("point_id")
        if not point_id or point_id in seen_summary:
            continue
        seen_summary.add(point_id)
        item["task"] = "summarise"
        item["needs_summary"] = True
        unique_summaries.append(item)
    pyramid["build"]["needs_summary"] = len(unique_summaries)
    return pyramid, deduped + unique_summaries


def render_markdown(pyramid, depth=3):
    """Governing thought, SCQA, key line, and the top levels. No deeper dump."""
    intro = pyramid["introduction"]
    lines = [
        f"# {pyramid['field']} — pyramid",
        "",
        "The introduction is Situation, Complication, Question, Answer (Chapter 4). "
        "The key line is inductive (Chapter 5). Order is time, structure, or degree (Chapter 6). "
        "Each summary is an inference over a group of two to five (Chapter 7).",
        "",
        "## Introduction",
        "",
        f"**Situation.** {intro['situation']}",
        "",
        f"**Complication.** {intro['complication']}",
        "",
        f"**Question.** {intro['question']}",
        "",
        f"**Answer.** {pyramid['governing_thought']}",
        "",
        "## Governing thought",
        "",
        pyramid["governing_thought"],
        "",
        "## Key line",
        "",
    ]
    key = pyramid["key_line"]
    lines.append(
        f"Inductive group of {key['plural_noun']}. "
        f"Dimension: {key['mece_dimension']}. Order: {key['order']}."
    )
    lines.append("")
    for index, point in enumerate(key["points"], start=1):
        lines.append(f"{index}. {point['statement']} `{point['id']}`")
    lines.append("")
    lines.append("## Groups")
    lines.append("")
    for index, point in enumerate(key["points"], start=1):
        lines.append(f"### {index}. {point['statement']}")
        lines.append("")
        support = point.get("support") or {}
        if point.get("question"):
            lines.append(f"Question. {point['question']}")
            lines.append("")
        if support:
            lines.append(
                f"Inductive group of {support['plural_noun']}. "
                f"Dimension: {support['mece_dimension']}. Order: {support['order']}."
            )
            lines.append("")
        _render_level(lines, support.get("points") or [], depth - 1, str(index))
        lines.append("")
    lines.append("This pyramid classifies the field. A problem-solving pyramid for one case would start from a defined problem (Chapter 8) and is a later document.")
    lines.append("")
    return "\n".join(lines)


def _render_level(lines, points, depth, prefix):
    for index, point in enumerate(points, start=1):
        label = f"{prefix}.{index}"
        lines.append(f"- **{label}.** {point['statement']} `{point['id']}`")
        if depth > 1 and point.get("support"):
            for child_i, child in enumerate(point["support"]["points"], start=1):
                lines.append(f"  - **{label}.{child_i}.** {child['statement']} `{child['id']}`")
