"""Bind a claim to quoted spans in caller-supplied sources and tool outputs (R20).

The service does not fetch. A pyramid search is not evidence. Number mismatch
is a contradiction. A model's label is never written here; the caller may add
by=model items, and those cannot by themselves support or contradict (R22).
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_REG = None
_NUM = re.compile(r"-?\d+(?:\.\d+)?")
_NEG = re.compile(r"\b(?:not|no|never|none|false|didn't|does not|do not|did not)\b", re.I)
_ID = re.compile(r"\b[A-Z]{2}\.[OMWB]\.[A-Z]?\d+(?:\.\d+)*\b")
_STOP = {
    "that", "this", "with", "from", "have", "were", "been", "into", "over", "under",
    "than", "then", "they", "them", "their", "which", "what", "when", "where", "while",
    "there", "these", "those", "also", "only", "such", "said", "says", "about", "after",
    "before", "between", "through", "would", "could", "should", "claim", "claims",
}
TOOL_WARRANT = {
    "calculator": "W2", "compute": "W2", "arithmetic": "W2",
    "test": "W11", "test_runner": "W11", "runner": "W11",
    "sensor": "W4", "reading": "W4", "api": "W4",
    "search": "W7", "snippet": "W7",
}
_WARRANT = {f"W{i}" for i in range(1, 14)}


def _registry():
    global _REG
    if _REG is None:
        _REG = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
    return _REG


def numbers(text):
    return _NUM.findall(text or "")


def numbers_agree(claim, quote, rel_tol=0.0):
    """True when every number in the claim appears in the quote. None if the claim has none."""
    wanted = numbers(claim)
    if not wanted:
        return None
    have = numbers(quote)
    if rel_tol:
        def close(a):
            fa = float(a)
            return any(abs(float(b) - fa) <= rel_tol * max(1.0, abs(fa)) for b in have)
        return all(close(n) for n in wanted)
    return all(n in have for n in wanted)


def warrant_of(doc, kind):
    declared = str((doc or {}).get("warrant") or "").upper()
    if declared in _WARRANT:
        return declared
    if kind == "source":
        return "W7"
    tool = str((doc or {}).get("tool") or "").lower().replace(" ", "_")
    return TOOL_WARRANT.get(tool)


def _body(doc):
    if isinstance(doc.get("output"), (dict, list)):
        return json.dumps(doc["output"], ensure_ascii=False)
    return str(doc.get("text") or doc.get("output") or "")


def _words(text):
    return [w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(w) > 3 and w not in _STOP]


def _span_of(hay, quote):
    if not quote:
        return [0, 0]
    idx = hay.lower().find(quote.lower()[:80])
    if idx < 0:
        return [0, min(len(hay), len(quote))]
    return [idx, min(len(hay), idx + len(quote))]


def match_spans(claim, docs, kind):
    """Lexical overlap plus number check. relation is entails, contradicts, or neutral."""
    out = []
    words = _words(claim)
    claim_neg = _NEG.search(claim or "") is not None
    for doc in docs or []:
        if not isinstance(doc, dict):
            continue
        body = _body(doc)
        if not body.strip():
            continue
        low = body.lower()
        hits = sum(1 for w in words if w in low)
        overlap = (hits / len(words)) if words else 0
        quote = ""
        relation = "neutral"
        folded = " ".join((claim or "").lower().split())
        if folded and folded in " ".join(body.lower().split()):
            quote = claim.strip()
            relation = "entails"
        elif overlap >= 0.6:
            quote = body.strip()[:240]
            relation = "entails"
        agreed = numbers_agree(claim, body) if relation == "entails" or numbers(claim) else None
        if relation == "entails" and agreed is False:
            relation = "contradicts"
            quote = quote or body.strip()[:240]
        elif relation == "entails":
            doc_neg = _NEG.search(body) is not None
            if doc_neg != claim_neg and overlap >= 0.6:
                relation = "contradicts"
        if relation == "neutral":
            continue
        ref = str(doc.get("id") or doc.get("url") or kind)
        out.append({
            "kind": kind,
            "ref": ref,
            "quote": quote[:500],
            "span": _span_of(body, quote),
            "relation": relation,
            "warrant_held": warrant_of(doc, kind),
            "by": "rule",
        })
    return out


def registry_hits(claim, placement=None):
    """A registry id in the claim, set against that row's label. Not a web lookup."""
    text = claim or ""
    ids = set(_ID.findall(text))
    if not ids:
        return []
    rows = {row.get("id"): row for row in _registry() if isinstance(row, dict)}
    neg = _NEG.search(text) is not None
    out = []
    for ident in sorted(ids):
        row = rows.get(ident)
        if not row:
            continue
        label = str(row.get("label") or "")
        if label and label.lower() not in text.lower() and not neg:
            continue
        relation = "contradicts" if neg else "entails"
        out.append({
            "kind": "registry",
            "ref": ident,
            "quote": f"{ident} {label}".strip(),
            "span": [0, 0],
            "relation": relation,
            "warrant_held": "W12",
            "by": "rule",
        })
    return out
