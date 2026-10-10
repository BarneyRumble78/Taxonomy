"""Taxonomy classifier.

rule_placement matches cue words with a left boundary and does not abstain.
classify runs that stage, abstains when the cue-score ratio is under 0.40,
then asks bge-small which pyramid field the wording is nearest to. The two
stages must name the same field. A warrant is stated only when a warrant cue
fired, and the method is the one that warrant uses.

The browser page runs stage_rule only. It has no retrieval model.
engine/rules.mjs is the JavaScript copy of the rule stage. Keep them in step.
"""
import csv, hashlib, json, math, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXICON = json.loads((ROOT / "engine" / "lexicon.json").read_text(encoding="utf-8"))
_SITE = json.loads((ROOT / "site" / "site_data.json").read_text(encoding="utf-8"))
NAMES = {c: v["name"] for c, v in _SITE["p"].items()}
CELLS = {c: v["cells"] for c, v in _SITE["p"].items()}

WARRANT_NAMES = {"W1": "Proof", "W2": "Computation with error bound", "W3": "Controlled intervention",
    "W4": "Measurement with uncertainty", "W5": "Causal identification", "W6": "Comparative inference",
    "W7": "Source criticism of a dated record", "W8": "Interpretation traced to a record", "W9": "Argument",
    "W10": "Source and proof before a forum", "W11": "Verification against a specification",
    "W12": "Stipulation or convention", "W13": "Tradition-internal authority"}
METHOD_NAMES = {"M1": "Represent", "M2": "Derive", "M3": "Observe", "M4": "Intervene", "M5": "Compute",
    "M6": "Compare and reconstruct", "M7": "Verify"}
DEFAULT_WARRANT = {"MA": "W1", "PH": "W4", "CH": "W3", "BI": "W3", "EA": "W4", "MD": "W3", "EN": "W11",
    "CS": "W1", "MS": "W3", "EC": "W5", "BU": "W12", "ST": "W9", "PO": "W6", "LA": "W10", "PL": "W9",
    "HI": "W7", "LN": "W4", "AR": "W8", "RE": "W8", "ED": "W3", "DE": "W4", "AG": "W3", "EV": "W5",
    "IS": "W4", "IK": "W13"}
WARRANT_TO_METHOD = {"W1": "M2", "W2": "M5", "W3": "M4", "W4": "M3", "W5": "M3", "W6": "M6", "W7": "M3",
    "W8": "M6", "W9": "M2", "W10": "M2", "W11": "M7", "W12": "M1", "W13": "M1"}
WARRANT_ORDER = ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10", "W11", "W12", "W13"]
LAW_CUE = re.compile(r"\bact (19|20)\d\d\b|\bunder the [a-z ]+act\b")
INSTRUCTION_HEURISTIC = re.compile(
    r"\b(?:ignore|disregard|forget)\b.{0,80}\b(?:previous|prior|above)\b"
    r"|\breveal\b.{0,40}\bsystem prompt\b",
    re.I,
)
CONFIDENCE_FLOOR = 0.40
CONFIDENCE_NOTE = "Confidence is a ratio of cue-word scores, not a probability."
_PROOF_VERBS = ("prove", "proof")
_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
# A trailing citation is its own segment, so a statute glued on another claim cannot keep the sentence.
_TRAIL_ACT = re.compile(r"\s+under the [a-z ]+act (?:19|20)\d\d\.?$", re.I)
FIELD_CODES = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()
_CUE_RE = {}
_INDEX = None
_EMBEDDER = None
_VEC_CACHE = {}


def cue_hit(text, cue):
    """Left-boundary match. A cue ending in a space keeps a substring match."""
    if cue.endswith(" "):
        return cue in text
    pat = _CUE_RE.get(cue)
    if pat is None:
        pat = re.compile(r"(?<![a-z0-9])" + re.escape(cue))
        _CUE_RE[cue] = pat
    return pat.search(text) is not None


def _score(text, words):
    return sum(1 for w in words if cue_hit(text, w))


def _field_score(text, field, skip=()):
    kw = [w for w in field["kw"] if w not in skip]
    return _score(text, kw) + 0.5 * sum(_score(text, cl) for cl in field["cells"])


def instruction_heuristic(sentence):
    """True when the wording is an instruction-like imperative, not a claim."""
    return bool(INSTRUCTION_HEURISTIC.search(sentence or ""))


def split_sentences(sentence):
    text = sentence or ""
    pieces = []
    while True:
        m = _TRAIL_ACT.search(text)
        if not m or m.start() == 0:
            pieces.append(text)
            break
        pieces.append(text[m.start():])
        text = text[:m.start()]
    pieces.reverse()
    parts = []
    for chunk in pieces:
        parts.extend(p.strip() for p in _SPLIT.split(chunk) if p.strip())
    return parts or [sentence or ""]


def _warrant_keys():
    extra = [k for k in LEXICON["warrants"] if k not in WARRANT_ORDER]
    return WARRANT_ORDER + extra


def rule_placement(sentence):
    """Cue-word placement for one sentence. No confidence gate and no retrieval."""
    if instruction_heuristic(sentence):
        return None
    t = " " + (sentence or "").lower() + " "
    fields = LEXICON["fields"]
    scores = {c: _field_score(t, f) for c, f in fields.items()}
    other = max((s for c, s in scores.items() if c != "MA"), default=0)
    if other > 0:
        scores["MA"] = _field_score(t, fields["MA"], skip=_PROOF_VERBS)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    owner, top = ranked[0]
    if top == 0:
        return None
    if any(k in t for k in ("theorem", "question is open")) and scores["MA"] >= top - 1 and scores["MA"] > 0:
        owner = "MA"
    if LAW_CUE.search(t) and scores["LA"] >= top - 2:
        owner = "LA"
    cell_scores = [_score(t, words) for words in fields[owner]["cells"]]
    cell_max = max(cell_scores) if cell_scores else 0
    idx = cell_scores.index(cell_max) if cell_scores else None
    cell = None
    if owner == "MA" and "integral domain" in t:
        idx = 1
        cell = "MA.O.A2"
    elif cell_max > 0:
        cell = f"{owner}.O.A{idx + 1}"
    else:
        idx = None
    keys = _warrant_keys()
    wvals = [_score(t, LEXICON["warrants"].get(k, [])) for k in keys]
    wmax = max(wvals) if wvals else 0
    warrant = keys[wvals.index(wmax)] if wmax > 0 else None
    if warrant == "W13" and owner not in ("RE", "IK"):
        warrant = None
    method = WARRANT_TO_METHOD.get(warrant) if warrant else None
    second = ranked[1][1] if len(ranked) > 1 else 0
    alts = [c for c, s in ranked[1:4] if s > 0 and s >= top - 1 and c != owner]
    return {
        "owner": owner,
        "cell": cell,
        "cell_index": idx if cell else None,
        "warrant": warrant,
        "method": method,
        "confidence": round(top / (top + second + 1), 2),
        "contested_with": alts,
    }


def stage_rule(sentence):
    """Rules, the 0.40 gate, and the multi-sentence gate. No retrieval."""
    if instruction_heuristic(sentence):
        return {"placement": None, "reason": "instruction"}
    parts = split_sentences(sentence)
    if len(parts) > 1:
        placed = [rule_placement(p) for p in parts]
        owners = [p["owner"] if p else None for p in placed]
        if any(o is None for o in owners) or len(set(owners)) != 1:
            return {"placement": None, "reason": "multi_sentence"}
        if any(p["confidence"] < CONFIDENCE_FLOOR for p in placed):
            return {"placement": None, "reason": "low_confidence"}
        full = rule_placement(sentence)
        if not full or full["owner"] != owners[0]:
            return {"placement": None, "reason": "multi_sentence"}
        if full["confidence"] < CONFIDENCE_FLOOR:
            return {"placement": None, "reason": "low_confidence"}
        return {"placement": full, "reason": None}
    full = rule_placement(sentence)
    if not full:
        return {"placement": None, "reason": "no_cue"}
    if full["confidence"] < CONFIDENCE_FLOOR:
        return {"placement": None, "reason": "low_confidence"}
    return {"placement": full, "reason": None}


def adjudicate(staged, retrieved_field):
    """retrieved_field None means retrieval did not run. Disagreement abstains."""
    if staged["reason"]:
        return {"placement": None, "reason": staged["reason"]}
    if retrieved_field is None:
        return {"placement": staged["placement"], "reason": None, "retrieval": {"status": "unavailable"}}
    if retrieved_field != staged["placement"]["owner"]:
        return {"placement": None, "reason": "stages_disagree"}
    return {"placement": staged["placement"], "reason": None, "retrieval": {"status": "agree", "field": retrieved_field}}


def pyramid_chunks(root=None, words=90):
    """Sections 2, 3 and 4 of each field pyramid, in 90-word windows."""
    root = Path(root) if root else ROOT
    chunks = []
    for code in FIELD_CODES:
        text = (root / "pyramids" / f"{code}.md").read_text(encoding="utf-8")
        parts = []
        for n in (2, 3, 4):
            m = re.search(rf"## {n}\..*?(?=\n## |\Z)", text, re.S)
            if m:
                parts.append(m.group(0))
        body = "\n".join(parts)
        toks = body.split() or text.split()[:words]
        for i in range(0, len(toks), words):
            piece = " ".join(toks[i:i + words]).strip()
            if piece:
                chunks.append({"field": code, "text": piece})
    return chunks


def chunks_sha256(root=None):
    chunks = pyramid_chunks(root)
    blob = "\n\n".join(f"{c['field']}\n{c['text']}" for c in chunks)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest(), chunks


def load_index():
    global _INDEX
    if _INDEX is None:
        _INDEX = json.loads((ROOT / "engine" / "retrieval_index.json").read_text(encoding="utf-8"))
    return _INDEX


def _unit_round(values, places=6):
    vals = [float(x) for x in values]
    norm = math.sqrt(sum(x * x for x in vals)) or 1.0
    return [round(x / norm, places) for x in vals]


def _embedder():
    global _EMBEDDER
    if _EMBEDDER is None:
        from fastembed import TextEmbedding
        cache = os.environ.get("FASTEMBED_CACHE_PATH") or os.environ.get("FASTEMBED_CACHE") or "/tmp/fastembed-cache"
        _EMBEDDER = TextEmbedding("BAAI/bge-small-en-v1.5", cache_dir=cache)
    return _EMBEDDER


def embed_queries(texts):
    """Unit vectors rounded to 6 decimals, in the same space as the chunk index."""
    missing = [t for t in texts if t not in _VEC_CACHE]
    if missing:
        vectors = _embedder().embed(missing)
        for text, vec in zip(missing, vectors):
            raw = vec.tolist() if hasattr(vec, "tolist") else list(vec)
            _VEC_CACHE[text] = _unit_round(raw)
    return [_VEC_CACHE[t] for t in texts]


def retrieve_field(vector, index=None):
    """Field whose nearest chunk has the highest cosine. Ties keep index order."""
    index = index or load_index()
    if not vector:
        return None
    qn = math.sqrt(sum(x * x for x in vector))
    if qn == 0:
        return None
    best = -1e300
    field = None
    for code, vec in zip(index["fields"], index["vectors"]):
        dot = 0.0
        cn = 0.0
        for a, b in zip(vector, vec):
            dot += a * b
            cn += b * b
        score = dot / (qn * math.sqrt(cn))
        if score > best:
            best = score
            field = code
    return field


def _decorate(p):
    if not p:
        return None
    owner = p["owner"]
    idx = p.get("cell_index")
    warrant, method = p.get("warrant"), p.get("method")
    return {
        "owner": owner,
        "owner_name": NAMES.get(owner),
        "cell": p.get("cell"),
        "cell_name": CELLS[owner][idx] if p.get("cell") and idx is not None else None,
        "warrant": warrant,
        "warrant_name": WARRANT_NAMES.get(warrant) if warrant else None,
        "method": method,
        "method_name": METHOD_NAMES.get(method) if method else None,
        "confidence": p["confidence"],
        "confidence_note": CONFIDENCE_NOTE,
        "contested_with": p["contested_with"],
    }


def place_many(sentences):
    """Full cascade. Retrieval is skipped when the rule stage already abstained.

    If the embedding model cannot be loaded, a sentence that passed the rule
    stage is returned with retrieval status unavailable. The weak band does
    not call a model.
    """
    staged = [stage_rule(s) for s in sentences]
    need = [i for i, s in enumerate(staged) if s["reason"] is None]
    vectors = {}
    unavailable = False
    if need:
        try:
            for i, vec in zip(need, embed_queries([sentences[i] for i in need])):
                vectors[i] = vec
        except Exception:
            unavailable = True
    index = None if unavailable else load_index()
    out = []
    for i, stage in enumerate(staged):
        if stage["reason"] is not None:
            out.append({"placement": None, "reason": stage["reason"]})
            continue
        if unavailable:
            out.append(adjudicate(stage, None))
            continue
        field = retrieve_field(vectors[i], index)
        decided = adjudicate(stage, field)
        if decided.get("placement"):
            decided["placement"] = _decorate(decided["placement"])
        out.append(decided)
    return out


def place_detail(sentence, query_vector=None):
    """One sentence. Pass query_vector to skip the model and force the cosine stage."""
    stage = stage_rule(sentence)
    if stage["reason"] is not None:
        return {"placement": None, "reason": stage["reason"]}
    if query_vector is not None:
        decided = adjudicate(stage, retrieve_field(query_vector))
    else:
        decided = place_many([sentence])[0]
        return decided
    if decided.get("placement"):
        decided["placement"] = _decorate(decided["placement"])
    return decided


def classify(sentence):
    """Public placement, or None when the cascade abstains."""
    return place_detail(sentence)["placement"]


def whole_view(subject):
    t = " " + subject.lower() + " "
    out = []
    for c, name in NAMES.items():
        f = LEXICON["fields"][c]
        rel = _field_score(t, f)
        out.append({"field": c, "name": name, "relevance": rel,
                    "questions": [f"{name} / {cell}: what does this field establish about {subject}, and on what warrant?"
                                  for cell in CELLS[c]]})
    return sorted(out, key=lambda r: -r["relevance"])


def evaluate(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))
    placed = place_many([r["claim"] for r in rows])
    hit = {"owner": 0, "cell": 0, "warrant": 0, "method": 0}
    answered = 0
    answered_hit = {"owner": 0, "cell": 0, "warrant": 0, "method": 0}
    for r, d in zip(rows, placed):
        p = d.get("placement") or {}
        if d.get("placement"):
            answered += 1
        for k in hit:
            ok = int(p.get(k) == r[k]) if d.get("placement") else 0
            hit[k] += ok
            if d.get("placement"):
                answered_hit[k] += ok
    n = len(rows)
    return {
        "n": n,
        "abstain": n - answered,
        "headline": {k: v / n for k, v in hit.items()},
        "answered": {k: (v / answered if answered else 0) for k, v in answered_hit.items()},
    }


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "--view":
        print(json.dumps(whole_view(" ".join(a[1:])), indent=2, ensure_ascii=False))
    elif a[0] == "--eval":
        report = evaluate(a[1])
        print(f"n {report['n']} abstain {report['abstain']}")
        for k, v in report["headline"].items():
            print(f"headline {k:8s} {v:.4f}")
        for k, v in report["answered"].items():
            print(f"answered {k:8s} {v:.4f}")
    elif a[0] == "--detail":
        print(json.dumps(place_detail(" ".join(a[1:])), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(classify(" ".join(a)), indent=2, ensure_ascii=False))
