"""Taxonomy Engine v0.1: transparent rule-based classifier for Taxonomy Standard v2.

classify(sentence) -> owner field, Face O cell, warrant (W1-W13), method (M1-M7).
whole_view(subject) -> the question each of the 25 fields asks of a subject.

Cues match at word boundaries. A cue may take a light inflection, and a truncated
stem (topolog, diagnos, and the rest of STEMS) may continue a word. A cue does not
fire inside an unrelated word: "ion" does not match "national", "force" does not
match "forces", "ring" does not match "neighbouring".

Armed "forces", naval mines, and foreign-policy speech are read as Politics (PO)
or Strategy (ST), the fields the standard already gives those claims. Physics keeps
"force" when the sentence is about mass, motion or fields. Official statements,
testimony and claimed responsibility map to W7. Satellite imagery and event counts
map to W4.

Data: engine/lexicon.json (cue words) and site/site_data.json (field names, cells).
CLI:
    python engine/taxonomy_engine.py "The importer must pay GST at the border."
    python engine/taxonomy_engine.py --view "AI-enabled sunglasses"
    python engine/taxonomy_engine.py --eval pilot/key.tsv
"""
import csv, json, re, sys
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
LAW_CUE = re.compile(r"\bact (19|20)\d\d\b|\bunder the [a-z ]+act\b")

# Truncated on purpose in the lexicon. They match a word that continues past the cue.
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

# Conduct and coercion, not a physics force and not a computer-security attack.
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


def _cue_in(text, cue):
    return _cue_re(cue).search(text) is not None


def _score(text, words, skip=()):
    return sum(1 for w in words if w not in skip and _cue_in(text, w))


def _score_field(text, field, skip=()):
    cells = [_score(text, cl, skip) for cl in field["cells"]]
    return _score(text, field["kw"], skip) + 0.5 * sum(cells), cells


def _placement(sentence):
    """Field scores after boundary matching and sense rules. Returns padded text, scores, cell hits."""
    t = " " + sentence.lower() + " "
    fields = LEXICON["fields"]
    scores, cells = {}, {}
    for code, field in fields.items():
        scores[code], cells[code] = _score_field(t, field)
    if re.search(r"\bprime ministers?\b", t):
        scores["MA"], cells["MA"] = _score_field(t, fields["MA"], skip={"prime"})
    physics = _PHYSICS_FORCE.search(t)
    labour = _NOT_ARMED_FORCES.search(t)
    military = _MILITARY.search(t) or _NAVAL_MINE.search(t)
    plural_forces = re.search(r"\bforces\b", t)
    if not physics and not labour and (plural_forces or (military and re.search(r"\bforce\b", t))):
        scores["PH"], cells["PH"] = _score_field(t, fields["PH"], skip={"force"})
    foreign_act = re.search(r"\bforeign (?:state|power|government|military|attack|forces)\b", t) or (
        re.search(r"\b(?:prime ministers?|foreign ministers?|government)\b", t) and re.search(r"\b(?:foreign|attacked|attack)\b", t)
    )
    # A claimed attack, with no computer-security vocabulary, is conduct (ST), not a software attack (CS).
    claimed_attack = re.search(r"\bclaimed responsibility\b", t) and re.search(r"\battacks?\b", t)
    computerish = _CYBER_ATTACK.search(t) or re.search(r"\b(?:software|computer|server|cyber|database|network)\b", t)
    if (military or foreign_act or claimed_attack) and not _CYBER_ATTACK.search(t):
        scores["CS"], cells["CS"] = _score_field(t, fields["CS"], skip={"attack"})
    if claimed_attack and scores["ST"] == 0 and not computerish:
        cells["ST"][3] += 1
        scores["ST"] += 1.5
    if _NAVAL_MINE.search(t) and not any(_cue_in(t, cue) for cue in _MINE_CUES):
        cells["ST"][3] += 1
        scores["ST"] += 1.5
    if military and scores["ST"] == 0:
        cells["ST"][3] += 1
        scores["ST"] += 1.5
    if re.search(r"\b(?:prime ministers?|foreign ministers?|the government)\b", t) and re.search(r"\bforeign\b", t):
        scores["PO"] += 0.5
    # "Land" in "Land Court" names a historical tribunal, not a relation to land.
    if re.search(r"\bland court\b", t):
        scores["IK"], cells["IK"] = _score_field(t, fields["IK"], skip={"land"})
    # A dated narrative that only says "war" is history (HI), not strategy. Standard: a dated political event is HI.
    if _YEAR.search(t) and scores["HI"] > 0 and not military and not plural_forces:
        scores["ST"], cells["ST"] = _score_field(t, fields["ST"], skip={"war"})
    return t, scores, cells


def classify(sentence):
    t, scores, cells = _placement(sentence)
    fields = LEXICON["fields"]
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    owner, top = ranked[0]
    if top == 0:
        return None
    # Ownership tie-breaks (Standard v2 ownership rule)
    if any(_cue_in(t, k) for k in ("theorem", "proof", "question is open")) and scores["MA"] >= top - 1:
        owner = "MA"
    if LAW_CUE.search(t) and scores["LA"] >= top - 2:
        owner = "LA"
    cs = cells[owner]
    idx = cs.index(max(cs))
    cell = f"{owner}.O.A{idx + 1}"
    w = {k: _score(t, v) for k, v in LEXICON["warrants"].items()}
    wmax = max(w.values())
    warrant = max(w, key=w.get) if wmax > 0 else DEFAULT_WARRANT[owner]
    if w.get(DEFAULT_WARRANT[owner], 0) >= wmax:
        warrant = DEFAULT_WARRANT[owner]
    if warrant == "W13" and owner not in ("RE", "IK"):  # W13 never travels
        warrant = DEFAULT_WARRANT[owner]
    m = {k: _score(t, v) for k, v in LEXICON["methods"].items()}
    method = max(m, key=m.get) if max(m.values()) > 0 else WARRANT_TO_METHOD[warrant]
    alts = [c for c, s in ranked[1:4] if s > 0 and s >= top - 1 and c != owner]
    second = ranked[1][1] if len(ranked) > 1 else 0
    return {"owner": owner, "owner_name": NAMES.get(owner), "cell": cell, "cell_name": CELLS[owner][idx],
            "warrant": warrant, "warrant_name": WARRANT_NAMES[warrant],
            "method": method, "method_name": METHOD_NAMES[method],
            "confidence": round(top / (top + second + 1), 2), "contested_with": alts}


def whole_view(subject):
    _t, scores, _cells = _placement(subject)
    out = []
    for c, name in NAMES.items():
        out.append({"field": c, "name": name, "relevance": scores[c],
                    "questions": [f"{name} / {cell}: what does this field establish about {subject}, and on what warrant?"
                                  for cell in CELLS[c]]})
    return sorted(out, key=lambda r: -r["relevance"])


def evaluate(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))
    hit = {"owner": 0, "cell": 0, "warrant": 0, "method": 0}
    for r in rows:
        p = classify(r["claim"]) or {}
        for k in hit:
            hit[k] += int(p.get(k) == r[k])
    return {k: v / len(rows) for k, v in hit.items()}


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "--view":
        print(json.dumps(whole_view(" ".join(a[1:])), indent=2, ensure_ascii=False))
    elif a[0] == "--eval":
        for k, v in evaluate(a[1]).items():
            print(f"{k:8s} {v:.2f}")
    else:
        print(json.dumps(classify(" ".join(a)), indent=2, ensure_ascii=False))
