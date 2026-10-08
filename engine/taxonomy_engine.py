"""Taxonomy Engine v0.1: transparent rule-based classifier for Taxonomy Standard v2.

classify(sentence) -> owner field, Face O cell, warrant (W1-W13), method (M1-M7).
whole_view(subject) -> the question each of the 25 fields asks of a subject.

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
# Heuristic only. An instruction-like imperative is not a claim. Failure to
# classify is not a security guarantee: a later sentence can still look like one.
INSTRUCTION_HEURISTIC = re.compile(
    r"\b(?:ignore|disregard|forget)\b.{0,80}\b(?:previous|prior|above)\b"
    r"|\breveal\b.{0,40}\bsystem prompt\b",
    re.I,
)
CONFIDENCE_NOTE = "Confidence is a ratio of cue-word scores, not a probability."
# Epistemic verbs. They do not name a mathematical object.
_PROOF_VERBS = ("prove", "proof")


def _score(text, words):
    return sum(1 for w in words if w in text)


def _field_score(text, field, skip_kw=()):
    kw = [w for w in field["kw"] if w not in skip_kw]
    return _score(text, kw) + 0.5 * sum(_score(text, cl) for cl in field["cells"])


def instruction_heuristic(sentence):
    """True when the wording is an instruction-like imperative, not a claim."""
    return bool(INSTRUCTION_HEURISTIC.search(sentence or ""))


def classify(sentence):
    # No W1–W5 warrant: there is no claim to place. Heuristic, not a guarantee.
    if instruction_heuristic(sentence):
        return None
    t = " " + sentence.lower() + " "
    fields = LEXICON["fields"]
    scores = {c: _field_score(t, f) for c, f in fields.items()}
    # "proves the tax cut works" is not a theorem. Drop bare proof-verbs from
    # Mathematics when another field has already matched its own cues.
    other = max((s for c, s in scores.items() if c != "MA"), default=0)
    if other > 0:
        scores["MA"] = _field_score(t, fields["MA"], skip_kw=_PROOF_VERBS)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    owner, top = ranked[0]
    if top == 0:
        return None
    # A theorem, or an open mathematical question, may keep a near-tie in MA.
    # The word "proof" alone must not.
    if any(k in t for k in ("theorem", "question is open")) and scores["MA"] >= top - 1 and scores["MA"] > 0:
        owner = "MA"
    if LAW_CUE.search(t) and scores["LA"] >= top - 2:
        owner = "LA"
    cs = [_score(t, words) for words in fields[owner]["cells"]]
    idx = cs.index(max(cs))
    # "Integral domain" is a ring (structure), not the integral of analysis.
    if owner == "MA" and "integral domain" in t:
        idx = 1
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
    # A proof claim is derived (M2). A weak observe cue such as "has a" must not turn it into M3.
    proof_claim = warrant == "W1" and (w.get("W1", 0) > 0 or any(s in t for s in ("prove", "proof", "theorem", "lemma")))
    if proof_claim and method == "M3":
        method = "M2"
    alts = [c for c, s in ranked[1:4] if s > 0 and s >= top - 1 and c != owner]
    second = ranked[1][1] if len(ranked) > 1 else 0
    return {"owner": owner, "owner_name": NAMES.get(owner), "cell": cell, "cell_name": CELLS[owner][idx],
            "warrant": warrant, "warrant_name": WARRANT_NAMES[warrant],
            "method": method, "method_name": METHOD_NAMES[method],
            "confidence": round(top / (top + second + 1), 2),
            "confidence_note": CONFIDENCE_NOTE,
            "contested_with": alts}


def whole_view(subject):
    t = " " + subject.lower() + " "
    out = []
    for c, name in NAMES.items():
        f = LEXICON["fields"][c]
        rel = _score(t, f["kw"]) + 0.5 * sum(_score(t, cl) for cl in f["cells"])
        out.append({"field": c, "name": name, "relevance": rel,
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
