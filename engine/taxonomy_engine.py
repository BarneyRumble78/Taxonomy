"""Taxonomy classifier.

rule_placement matches a cue at a left boundary. A light inflection may follow
(theorem/theorems). A truncated stem may continue a word (topolog/topology).
An exact cue may not: "force" does not match "forces".
classify abstains when the cue-score ratio is under 0.40 or retrieval disagrees,
then may ask a pluggable model to adjudicate that queue. Samples must agree.
A warrant cue is recorded as such. If none fired, the field default is reported
and default_applied is true. The method is the one that warrant uses.

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
# Truncated on purpose. They match a word that continues past the cue.
STEMS = frozenset({
    "topolog", "diagnos", "electromagnet", "bacteri", "mitochondri", "descend", "phylogen", "geolog",
    "manufactur", "simulat", "randomi", "catalogu", "morpholog", "theolog", "religio", "pedagog",
    "classif", "certif", "turbulen", "concurren", "serialis", "hippocamp", "ontolog", "epistem",
    "commemorat", "revitalis", "accessib", "purif", "chromatograph", "spectroscop", "electr", "cosmolog",
    "vaccin", "escalat", "kaitiaki", "depress", "axiom", "reconstruct", "interpret", "convention",
})
# Plural "forces" is armed forces, not the physics lemma "force".
EXACT = frozenset({"force"})
_SUFFIX = "(?:led|ies|ing|ers|ally|es|ed|er|s)"
_CUE_RE = {}
_MILITARY = re.compile(
    r"\b(?:armed forces|air force|ground forces|military|troops?|soldiers?|armies|army|navies|navy|"
    r"brigades?|battalions?|artillery|missiles?|airstrikes?|air strikes?|warships?|naval mines?|sea mines?|"
    r"minefields?|minelaying|battlefield|invasions?|invaded|bombard(?:ment|ed|ing)?|casualt(?:y|ies)|"
    r"enem(?:y|ies)|offensives?|garrisons?|warplanes?|drone strikes?|shelling|blockades?|weapons?|flanks?|"
    r"munitions?)\b"
)
_NAVAL_MINE = re.compile(
    r"\b(?:naval mines?|sea mines?|minefields?|minelaying)\b|"
    r"\b(?:naval|sea|harbour|harbor|strait|shipping|waterway|channel)\b(?:\W+\w+){0,6}?\W+\bmines?\b|"
    r"\bmines?\b(?:\W+\w+){0,6}?\W+\b(?:strait|shipping|harbour|harbor|naval|waterway|laid)\b"
)
_PHYSICS_FORCE = re.compile(
    r"\b(?:newtons?|particles?|mass|gravity|gravitational|momentum|acceleration|electromagnetic|"
    r"intermolecular|net force|inertial|torque|vectors?)\b"
)
_NOT_ARMED_FORCES = re.compile(
    r"\b(?:labour|labor|work)\s+forces?\b|\bworkforce\b|\bmarket forces\b|\bcompetitive forces\b|"
    r"\beconomic forces\b|\bsocial forces\b|\bdriving forces\b"
)
_CYBER_ATTACK = re.compile(r"\b(?:malware|ransomware|phishing|phish|zero-day|passwords?|encrypt(?:ion|ed)?)\b")
_YEAR = re.compile(r"\b(?:1[0-9]{3}|20[0-9]{2})\b")
_MINE_CUES = ("naval mine", "sea mine", "minefield", "minelaying")
_INDEX = None
_EMBEDDER = None
_VEC_CACHE = {}


def _cue_re(cue):
    compiled = _CUE_RE.get(cue)
    if compiled is not None:
        return compiled
    raw = cue.lower()
    if raw.endswith(" "):
        compiled = re.compile(r"(?<![a-z0-9])" + re.escape(raw))
    elif re.fullmatch(r"[a-z0-9]+", raw):
        if raw in STEMS:
            compiled = re.compile(r"(?<![a-z0-9])" + re.escape(raw))
        elif raw in EXACT:
            compiled = re.compile(r"(?<![a-z0-9])" + re.escape(raw) + r"(?![a-z0-9])")
        else:
            compiled = re.compile(r"(?<![a-z0-9])" + re.escape(raw) + _SUFFIX + r"?(?![a-z0-9])")
    else:
        parts = raw.split(" ")
        head, last = parts[:-1], parts[-1]
        body = r"\s+".join(re.escape(p) for p in head)
        if body:
            body += r"\s+"
        if re.fullmatch(r"\d+", last):
            last_re = re.escape(last) + r"(?![a-z])"
        elif last in STEMS:
            last_re = re.escape(last)
        else:
            last_re = re.escape(last) + _SUFFIX + r"?(?![a-z0-9])"
        compiled = re.compile(r"(?<![a-z0-9])" + body + last_re)
    _CUE_RE[cue] = compiled
    return compiled


def cue_hit(text, cue):
    """Left boundary, then a word boundary or a light inflection. Stems may continue."""
    return _cue_re(cue).search(text) is not None


def _score(text, words, skip=()):
    return sum(1 for w in words if w not in skip and cue_hit(text, w))


def _score_field(text, field, skip=()):
    cells = [_score(text, cl, skip) for cl in field["cells"]]
    return _score(text, field["kw"], skip) + 0.5 * sum(cells), cells


def _sense(text, scores, cells):
    """Politics and Strategy senses from the geopolitical cue pass. Kept in step with rules.mjs."""
    fields = LEXICON["fields"]
    if re.search(r"\bprime ministers?\b", text):
        skip = {"prime"} | (set(_PROOF_VERBS) if max((s for c, s in scores.items() if c != "MA"), default=0) > 0 else set())
        scores["MA"], cells["MA"] = _score_field(text, fields["MA"], skip=skip)
    physics = _PHYSICS_FORCE.search(text)
    labour = _NOT_ARMED_FORCES.search(text)
    military = _MILITARY.search(text) or _NAVAL_MINE.search(text)
    plural_forces = re.search(r"\bforces\b", text)
    if not physics and not labour and (plural_forces or (military and re.search(r"\bforce\b", text))):
        scores["PH"], cells["PH"] = _score_field(text, fields["PH"], skip={"force"})
    foreign_act = re.search(r"\bforeign (?:state|power|government|military|attack|forces)\b", text) or (
        re.search(r"\b(?:prime ministers?|foreign ministers?|government)\b", text) and re.search(r"\b(?:foreign|attacked|attack)\b", text)
    )
    claimed_attack = re.search(r"\bclaimed responsibility\b", text) and re.search(r"\battacks?\b", text)
    computerish = _CYBER_ATTACK.search(text) or re.search(r"\b(?:software|computer|server|cyber|database|network)\b", text)
    if (military or foreign_act or claimed_attack) and not _CYBER_ATTACK.search(text):
        scores["CS"], cells["CS"] = _score_field(text, fields["CS"], skip={"attack"})
    if claimed_attack and scores["ST"] == 0 and not computerish:
        cells["ST"][3] += 1
        scores["ST"] += 1.5
    if _NAVAL_MINE.search(text) and not any(cue_hit(text, cue) for cue in _MINE_CUES):
        cells["ST"][3] += 1
        scores["ST"] += 1.5
    if military and scores["ST"] == 0:
        cells["ST"][3] += 1
        scores["ST"] += 1.5
    if re.search(r"\b(?:prime ministers?|foreign ministers?|the government)\b", text) and re.search(r"\bforeign\b", text):
        scores["PO"] += 0.5
    if re.search(r"\bland court\b", text):
        scores["IK"], cells["IK"] = _score_field(text, fields["IK"], skip={"land"})
    if _YEAR.search(text) and scores["HI"] > 0 and not military and not plural_forces:
        scores["ST"], cells["ST"] = _score_field(text, fields["ST"], skip={"war"})


def _score_all(text):
    fields = LEXICON["fields"]
    scores, cells = {}, {}
    for code, field in fields.items():
        scores[code], cells[code] = _score_field(text, field)
    other = max((s for c, s in scores.items() if c != "MA"), default=0)
    if other > 0:
        scores["MA"], cells["MA"] = _score_field(text, fields["MA"], skip=_PROOF_VERBS)
    _sense(text, scores, cells)
    return scores, cells


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
    scores, cells = _score_all(t)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    owner, top = ranked[0]
    if top == 0:
        return None
    if any(cue_hit(t, k) for k in ("theorem", "question is open")) and scores["MA"] >= top - 1 and scores["MA"] > 0:
        owner = "MA"
    if LAW_CUE.search(t) and scores["LA"] >= top - 2:
        owner = "LA"
    cell_scores = cells.get(owner) or []
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
    default = DEFAULT_WARRANT.get(owner)
    if wmax > 0:
        warrant = keys[wvals.index(wmax)]
        if default in keys and wvals[keys.index(default)] >= wmax:
            warrant = default
        default_applied = False
        if warrant == "W13" and owner not in ("RE", "IK"):
            warrant = default
            default_applied = True
    else:
        warrant = default
        default_applied = True
    method = WARRANT_TO_METHOD.get(warrant) if warrant else None
    second = ranked[1][1] if len(ranked) > 1 else 0
    alts = [c for c, s in ranked[1:4] if s > 0 and s >= top - 1 and c != owner]
    return {
        "owner": owner,
        "cell": cell,
        "cell_index": idx if cell else None,
        "warrant": warrant,
        "default_applied": default_applied,
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
        "default_applied": bool(p.get("default_applied")),
        "method": method,
        "method_name": METHOD_NAMES.get(method) if method else None,
        "confidence": p["confidence"],
        "confidence_note": p.get("confidence_note") or CONFIDENCE_NOTE,
        "contested_with": p.get("contested_with") or [],
        "adjudicated": bool(p.get("adjudicated")),
    }


QUEUE_REASONS = ("low_confidence", "stages_disagree", "no_cue")
_CHUNKS = None
_OFF = {"0", "false", "off", "no"}


def aligned_chunks():
    global _CHUNKS
    if _CHUNKS is None:
        digest, chunks = chunks_sha256()
        index = load_index()
        if digest != index.get("chunks_sha256") or [c["field"] for c in chunks] != index.get("fields"):
            raise RuntimeError("pyramid chunks do not match engine/retrieval_index.json")
        _CHUNKS = chunks
    return _CHUNKS


def retrieve_definitions(vector, k=5, limit=600):
    """Best pyramid chunk for each of the nearest fields. Text is context, not an answer."""
    if not vector:
        return []
    index = load_index()
    chunks = aligned_chunks()
    qn = math.sqrt(sum(x * x for x in vector)) or 1.0
    best = {}
    for code, vec, chunk in zip(index["fields"], index["vectors"], chunks):
        dot = cn = 0.0
        for a, b in zip(vector, vec):
            dot += a * b
            cn += b * b
        score = dot / (qn * (math.sqrt(cn) or 1.0))
        prev = best.get(code)
        if prev is None or score > prev[0]:
            best[code] = (score, chunk["text"][:limit].rstrip())
    ranked = sorted(best.items(), key=lambda kv: (-kv[1][0], FIELD_CODES.index(kv[0])))
    return [{"field": code, "text": text} for code, (_score, text) in ranked[:k]]


def _caller(adjudicator):
    """False forces the stage off. A callable is used as given. Otherwise the environment."""
    if adjudicator is False:
        return None
    if callable(adjudicator):
        return adjudicator
    if os.environ.get("TAXONOMY_ADJUDICATE", "").strip().lower() in _OFF:
        return None
    from adjudicator import provider_from_env
    return provider_from_env()


def _prepare(sentences, embed_queue):
    """Rule stage, then retrieval for sentences the rules would place.

    Queue sentences are embedded only when a model will see them. An embedding
    failure keeps a rule placement and marks retrieval unavailable.
    """
    staged = [stage_rule(s) for s in sentences]
    need = [
        i for i, s in enumerate(staged)
        if s["reason"] is None or (embed_queue and s["reason"] in QUEUE_REASONS)
    ]
    vectors = {}
    unavailable = False
    if need:
        try:
            for i, vec in zip(need, embed_queries([sentences[i] for i in need])):
                vectors[i] = vec
        except Exception as exc:
            if isinstance(exc, AssertionError):
                raise
            unavailable = True
    index = None if unavailable else load_index()
    prepared = []
    for i, stage in enumerate(staged):
        item = {
            "reason": stage["reason"],
            "placement": None,
            "retrieval": None,
            "vector": None if unavailable else vectors.get(i),
        }
        if stage["reason"] is None:
            if unavailable or i not in vectors:
                decided = adjudicate(stage, None)
            else:
                decided = adjudicate(stage, retrieve_field(vectors[i], index))
            item["reason"] = decided["reason"]
            item["placement"] = decided.get("placement")
            item["retrieval"] = decided.get("retrieval")
        prepared.append(item)
    return prepared


def _complete(call, messages):
    raw = call(messages)
    if isinstance(raw, tuple):
        return raw[0], raw[1] or {}
    return raw, {}


def place_many(sentences, adjudicator=None):
    """Full cascade. The model runs only on the abstention queue, and only if configured.

    low_confidence, stages_disagree and no_cue are the queue. An instruction
    heuristic hit and a multi-sentence split are not. Three samples must agree
    on the owner. If the embedding model cannot be loaded, a sentence that
    passed the rule stage is kept and retrieval is marked unavailable.
    """
    call = _caller(adjudicator)
    prepared = _prepare(sentences, embed_queue=call is not None)
    from adjudicator import N_SAMPLES, adjudication_messages, agree_samples
    out = []
    for sentence, item in zip(sentences, prepared):
        if item["placement"]:
            out.append({
                "placement": _decorate(item["placement"]),
                "reason": None,
                "retrieval": item["retrieval"],
            })
            continue
        reason = item["reason"]
        if call is None or reason not in QUEUE_REASONS:
            out.append({"placement": None, "reason": reason})
            continue
        definitions = retrieve_definitions(item["vector"]) if item.get("vector") is not None else []
        messages = adjudication_messages(sentence, definitions)
        samples, usage = [], []
        try:
            for _ in range(N_SAMPLES):
                text, meta = _complete(call, messages)
                samples.append(text)
                if meta:
                    usage.append(meta)
        except Exception as exc:
            if isinstance(exc, AssertionError):
                raise
            out.append({"placement": None, "reason": reason, "adjudication": {"status": "error"}})
            continue
        agreed = agree_samples(samples)
        if not agreed:
            out.append({"placement": None, "reason": reason, "adjudication": {"status": "disagree"}})
            continue
        out.append({
            "placement": _decorate(agreed),
            "reason": None,
            "retrieval": {"status": "adjudicated"},
            "adjudication": {"status": "agree", "usage": usage},
        })
    return out


def adjudication_jobs(sentences):
    """Prompts for the queue. Does not call a model."""
    from adjudicator import adjudication_messages, message_id
    prepared = _prepare(sentences, embed_queue=True)
    jobs = []
    for i, (sentence, item) in enumerate(zip(sentences, prepared)):
        if item["placement"] or item["reason"] not in QUEUE_REASONS:
            continue
        definitions = retrieve_definitions(item["vector"]) if item.get("vector") is not None else []
        messages = adjudication_messages(sentence, definitions)
        jobs.append({
            "index": i,
            "claim": sentence,
            "reason": item["reason"],
            "messages": messages,
            "id": message_id(messages),
        })
    return jobs


def place_detail(sentence, query_vector=None, adjudicator=None):
    """One sentence. Pass query_vector to skip the model and force the cosine stage."""
    if query_vector is not None:
        stage = stage_rule(sentence)
        if stage["reason"] is not None:
            return {"placement": None, "reason": stage["reason"]}
        decided = adjudicate(stage, retrieve_field(query_vector))
        if decided.get("placement"):
            decided["placement"] = _decorate(decided["placement"])
        return decided
    return place_many([sentence], adjudicator=adjudicator)[0]


def classify(sentence):
    """Public placement, or None when the cascade abstains."""
    return place_detail(sentence)["placement"]


def whole_view(subject):
    t = " " + subject.lower() + " "
    scores, _cells = _score_all(t)
    out = []
    for c, name in NAMES.items():
        out.append({"field": c, "name": name, "relevance": scores.get(c, 0),
                    "questions": [f"{name} / {cell}: what does this field establish about {subject}, and on what warrant?"
                                  for cell in CELLS[c]]})
    return sorted(out, key=lambda r: -r["relevance"])


def evaluate(path, adjudicator=None):
    """Headline counts an abstention as a miss. Warrant is scored with the default filled in.

    default_applied is reported beside that score. A match on a default is not
    hidden inside the warrant accuracy.
    """
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))
    placed = place_many([r["claim"] for r in rows], adjudicator=adjudicator)
    hit = {"owner": 0, "cell": 0, "warrant": 0, "method": 0}
    answered = 0
    answered_hit = {"owner": 0, "cell": 0, "warrant": 0, "method": 0}
    reasons = {}
    n_default = n_cue = w_default = w_cue = 0
    for r, d in zip(rows, placed):
        key = "placed" if d.get("placement") else (d.get("reason") or "abstain")
        reasons[key] = reasons.get(key, 0) + 1
        p = d.get("placement")
        if not p:
            continue
        answered += 1
        if p.get("default_applied"):
            n_default += 1
            w_default += int(p.get("warrant") == r["warrant"])
        else:
            n_cue += 1
            w_cue += int(p.get("warrant") == r["warrant"])
        for k in hit:
            ok = int(p.get(k) == r[k])
            hit[k] += ok
            answered_hit[k] += ok
    n = len(rows)
    return {
        "n": n,
        "abstain": n - answered,
        "reasons": reasons,
        "headline_counts": hit,
        "headline": {k: v / n for k, v in hit.items()},
        "answered_n": answered,
        "answered_counts": answered_hit,
        "answered": {k: (v / answered if answered else 0) for k, v in answered_hit.items()},
        "default_applied": n_default,
        "cue_warrant_n": n_cue,
        "warrant_including_default": hit["warrant"] / n if n else 0,
        "warrant_when_default_applied": (w_default / n_default) if n_default else None,
        "warrant_when_cue": (w_cue / n_cue) if n_cue else None,
        "default_applied_matches": w_default,
        "cue_warrant_matches": w_cue,
    }


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "--view":
        print(json.dumps(whole_view(" ".join(a[1:])), indent=2, ensure_ascii=False))
    elif a[0] == "--eval":
        report = evaluate(a[1])
        n, answered = report["n"], report["answered_n"]
        print(f"n {n} answered {answered} abstain {report['abstain']} ({report['abstain'] / n:.1%})")
        print("reasons " + " ".join(f"{k}={v}" for k, v in sorted(report["reasons"].items())))
        for k in report["headline"]:
            h, ans = report["headline_counts"][k], report["answered_counts"][k]
            print(f"headline {k:8s} {h}/{n} ({report['headline'][k]:.1%})  answered {ans}/{answered}")
        print(
            f"warrant including default {report['default_applied_matches'] + report['cue_warrant_matches']}/{n}"
            f"  default_applied {report['default_applied']}/{answered}"
            f" of which {report['default_applied_matches']} match gold"
            f"  cue warrant {report['cue_warrant_matches']}/{report['cue_warrant_n']}"
        )
    elif a[0] == "--detail":
        print(json.dumps(place_detail(" ".join(a[1:])), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(classify(" ".join(a)), indent=2, ensure_ascii=False))
