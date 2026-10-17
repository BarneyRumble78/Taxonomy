"""Bind a claim to an exact span in a source or a tool output (R20).

The service does not fetch. A pyramid search is not evidence. A match is an
exact span after whitespace, case and Unicode quotes are normalised. Token
overlap is not a match. A mismatch of number, unit, entity or direction, in a
span that otherwise aligns, is a contradiction and never support. The quote is
that span, with its offsets.

A caller may label a warrant. The label is advisory. The grade is read from
the text and the source type, and a caller cannot raise a source above it.
"""
import json, re
from pathlib import Path

from certainty import rank, warrant_ceiling

ROOT = Path(__file__).resolve().parents[2]
_REG = None
_NUM = re.compile(r"\d{1,2}:\d{2}|-?\d+(?:\.\d+)?")
_NEG = re.compile(r"\b(?:not|no|never|none|false|didn't|does not|do not|did not)\b", re.I)
_ID = re.compile(r"\b[A-Z]{2}\.[OMWB]\.[A-Z]?\d+(?:\.\d+)*\b")
_STOP = {
    "that", "this", "with", "from", "have", "were", "been", "into", "over", "under",
    "than", "then", "they", "them", "their", "which", "what", "when", "where", "while",
    "there", "these", "those", "also", "only", "such", "said", "says", "about", "after",
    "before", "between", "through", "would", "could", "should", "claim", "claims",
}
_FRAME_STOP = _STOP | {
    "the", "and", "for", "are", "was", "not", "but", "its", "his", "her", "you", "our",
    "has", "had", "who", "how", "any", "all", "can", "may", "per", "via", "out", "off",
    "does", "did", "doing", "done", "being",
}
_TOKEN = re.compile(r"\d{1,2}:\d{2}|-?\d+(?:\.\d+)?|[a-z]+(?:'[a-z]+)?")
_LEAD = re.compile(
    r"^(?:(?:the|a|an|this)\s+)?(?:[\w']+\s+){0,3}?(?:conclusively\s+|definitely\s+)?"
    r"(?:proves|shows|demonstrates|confirms|establishes)\s+",
    re.I,
)
_SPLIT = re.compile(r"\s+\bbut\b\s+|;\s*|(?<=[.?!])\s+", re.I)
_TRIAL = re.compile(
    r"\b(?:randomi[sz]ed|controlled trial|clinical trial|cohort stud(?:y|ies)|meta-analysis|trial)\b",
    re.I,
)
_MEASURE = re.compile(
    r"\b(?:measured|measurement|sensor reading)\b|\bppb\b|\bppm\b|parts per (?:billion|million)",
    re.I,
)
_PROOF = re.compile(r"\b(?:qed|quod erat demonstrandum|we prove that|proof:)\b", re.I)
_QUOTES = {
    "\u2018": "'", "\u2019": "'", "\u2032": "'",
    "\u201c": '"', "\u201d": '"', "\u00ab": '"', "\u00bb": '"', "\u2033": '"',
}
TOOL_WARRANT = {
    "calculator": "W2", "compute": "W2", "arithmetic": "W2",
    "test": "W11", "test_runner": "W11", "runner": "W11",
    "sensor": "W4", "reading": "W4", "api": "W4",
    "search": "W7", "snippet": "W7",
}
_WARRANT = {f"W{i}" for i in range(1, 14)}
_DOWN = {
    "lower", "decrease", "decreased", "decreases", "decreasing",
    "fell", "fall", "falling", "falls", "reduced", "reduce", "reduces", "reducing", "down",
}
_UP = {
    "higher", "increase", "increased", "increases", "increasing",
    "rose", "rise", "rising", "rises", "raised", "raise", "raises", "raising", "up",
}
_DIR = {w: "down" for w in _DOWN}
_DIR.update({w: "up" for w in _UP})
_DAYS = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
_POLAR = {
    "not", "no", "never", "none", "false",
    "dont", "doesnt", "didnt", "isnt", "arent", "wasnt", "werent",
}
_UNITS = {
    "ppb", "ppm", "percent", "degree", "degrees", "foot", "feet",
    "metre", "metres", "meter", "meters", "million", "billion",
    "kg", "km", "dollar", "dollars",
}
_UNIT_ALIAS = {"meter": "metre", "meters": "metres", "degree": "degrees", "foot": "feet", "dollar": "dollars"}


def _registry():
    global _REG
    if _REG is None:
        _REG = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
    return _REG


def _ceil(code):
    return rank(warrant_ceiling(code))


def numbers(text):
    return _NUM.findall(text or "")


def _num_key(token):
    if re.fullmatch(r"\d{1,2}:\d{2}", token or ""):
        return token
    try:
        return f"{float(token):.10g}"
    except (TypeError, ValueError):
        return token


def numbers_agree(claim, quote, rel_tol=0.0):
    """True when every number in the claim appears in the quote. None if the claim has none."""
    wanted = numbers(claim)
    if not wanted:
        return None
    have = numbers(quote)
    if rel_tol:
        def close(a):
            if ":" in a:
                return a in have
            fa = float(a)
            return any(":" not in b and abs(float(b) - fa) <= rel_tol * max(1.0, abs(fa)) for b in have)
        return all(close(n) for n in wanted)
    have_keys = {_num_key(n) for n in have}
    return all(_num_key(n) in have_keys for n in wanted)


def _raw_text(doc):
    if isinstance(doc.get("output"), (dict, list)):
        return _flatten(doc["output"])
    if isinstance(doc.get("text"), (dict, list)):
        return _flatten(doc["text"])
    return str(doc.get("text") or doc.get("output") or "")


def _flatten(obj):
    parts = []

    def walk(node, key=None):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, k)
        elif isinstance(node, list):
            for v in node:
                walk(v, key)
        else:
            if key is not None:
                parts.append(str(key).replace("_", " "))
            if node is not None and not isinstance(node, bool):
                parts.append(str(node))

    walk(obj)
    return " ".join(parts)


def _grade(doc, kind):
    if kind != "source":
        tool = str((doc or {}).get("tool") or "").lower().replace(" ", "_")
        return TOOL_WARRANT.get(tool) or "W7"
    text = _raw_text(doc)
    if _PROOF.search(text):
        return "W1"
    if _TRIAL.search(text):
        return "W3"
    if _MEASURE.search(text):
        return "W4"
    return "W7"


def warrant_fields(doc, kind):
    """Grade from the text and the type. A caller label cannot raise that grade."""
    graded = _grade(doc, kind)
    declared = str((doc or {}).get("warrant") or "").upper()
    caller = declared in _WARRANT
    held = graded
    if caller and graded and _ceil(declared) < _ceil(graded):
        held = declared
    return {
        "warrant_held": held,
        "warrant_graded": graded,
        "warrant_declared_by_caller": caller,
    }


def warrant_of(doc, kind):
    return warrant_fields(doc, kind)["warrant_held"]


def _body(doc):
    return _raw_text(doc)


def _words(text):
    return [w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(w) > 3 and w not in _STOP]


def _normalize(text):
    """Lower case, ASCII quotes, collapsed whitespace. Punctuation splits tokens."""
    raw = text or ""
    out = []
    origin = []
    pending = False
    started = False
    i = 0
    n = len(raw)
    while i < n:
        ch = _QUOTES.get(raw[i], raw[i])
        low = ch.lower()
        if low.isspace() or low in "?!;,":
            if started:
                pending = True
            i += 1
            continue
        if low == ".":
            prev_digit = i > 0 and raw[i - 1].isdigit()
            next_digit = i + 1 < n and raw[i + 1].isdigit()
            if not (prev_digit and next_digit):
                if started:
                    pending = True
                i += 1
                continue
        if low == ":":
            prev_digit = i > 0 and raw[i - 1].isdigit()
            next_digit = i + 1 < n and raw[i + 1].isdigit()
            if not (prev_digit and next_digit):
                if started:
                    pending = True
                i += 1
                continue
        if pending and out:
            out.append(" ")
            origin.append(i)
            pending = False
        out.append(low)
        origin.append(i)
        started = True
        i += 1
    return "".join(out), origin


def _slice(body, norm, origin, needle, claim=""):
    if not needle:
        return None
    idx = norm.find(needle)
    if idx < 0 or idx >= len(origin):
        return None
    last = idx + len(needle) - 1
    if last >= len(origin):
        return None
    start = origin[idx]
    end = origin[last] + 1
    if end < len(body) and body[end] in ".?!" and (claim or "").rstrip().endswith(body[end]):
        end += 1
    return body[start:end], [start, end]


def _atoms(norm):
    toks = _TOKEN.findall(norm or "")
    merged = []
    i = 0
    while i < len(toks):
        if toks[i] == "parts" and i + 2 < len(toks) and toks[i + 1] == "per" and toks[i + 2] in ("billion", "million"):
            merged.append("ppb" if toks[i + 2] == "billion" else "ppm")
            i += 3
            continue
        if toks[i] == "per" and i + 1 < len(toks) and toks[i + 1] == "cent":
            merged.append("percent")
            i += 2
            continue
        merged.append(toks[i].replace("'", ""))
        i += 1
    polar = False
    seq = []
    for token in merged:
        if token in _POLAR:
            polar = True
            continue
        if token in _DIR:
            seq.append(("dir", _DIR[token]))
            continue
        if token in _DAYS:
            seq.append(("day", token))
            continue
        if re.fullmatch(r"\d{1,2}:\d{2}|-?\d+(?:\.\d+)?", token):
            kind = "time" if ":" in token else "num"
            seq.append((kind, _num_key(token) if kind == "num" else token))
            continue
        if token in _UNITS:
            seq.append(("unit", _UNIT_ALIAS.get(token, token)))
            continue
        if token in _FRAME_STOP or len(token) <= 2:
            continue
        seq.append(("word", token))
    return seq, polar


def _conflict(claim_norm, window_norm):
    """A slot mismatch on an otherwise aligned frame. None when the frame does not align."""
    cseq, cpol = _atoms(claim_norm)
    wseq, wpol = _atoms(window_norm)
    cdays = {a[1] for a in cseq if a[0] == "day"}
    wdays = {a[1] for a in wseq if a[0] == "day"}
    if cdays and wdays and cdays != wdays:
        shared = {a[1] for a in cseq if a[0] == "word"} & {a[1] for a in wseq if a[0] == "word"}
        if shared:
            return "day"
    if len(cseq) < 3 or len(wseq) < 2:
        return None
    if cseq == wseq:
        return "polarity" if cpol != wpol else None
    if len(cseq) == len(wseq):
        diffs = [i for i, (a, b) in enumerate(zip(cseq, wseq)) if a != b]
        if len(diffs) == 1 and cseq[diffs[0]][0] == wseq[diffs[0]][0]:
            return cseq[diffs[0]][0]
    cwords = [a for a in cseq if a[0] == "word"]
    wwords = [a for a in wseq if a[0] == "word"]
    cdir = {a[1] for a in cseq if a[0] == "dir"}
    wdir = {a[1] for a in wseq if a[0] == "dir"}
    if cdir and wdir and cdir != wdir and cwords and wwords:
        i = 0
        while i < len(cwords) and i < len(wwords) and cwords[i] == wwords[i]:
            i += 1
        j = 0
        while j < len(cwords) - i and j < len(wwords) - i and cwords[-1 - j] == wwords[-1 - j]:
            j += 1
        if i >= 2 and j >= 2:
            return "dir"
    if cwords and cwords == wwords:
        cnums = [a[1] for a in cseq if a[0] in ("num", "time")]
        wnums = [a[1] for a in wseq if a[0] in ("num", "time")]
        if cnums and wnums and cnums != wnums:
            return "num"
        if cpol != wpol:
            return "polarity"
    return None


def _windows(text):
    out = []
    start = 0
    for match in _SPLIT.finditer(text or ""):
        chunk = text[start:match.start()]
        if chunk.strip():
            lead = len(chunk) - len(chunk.lstrip())
            trimmed = chunk.strip()
            out.append((trimmed, start + lead, start + lead + len(trimmed)))
        start = match.end()
    chunk = (text or "")[start:]
    if chunk.strip():
        lead = len(chunk) - len(chunk.lstrip())
        trimmed = chunk.strip()
        out.append((trimmed, start + lead, start + lead + len(trimmed)))
    return out


def _support_span(claim, body):
    norm, origin = _normalize(body)
    claim_norm, _ = _normalize(claim)
    found = _slice(body, norm, origin, claim_norm, claim)
    if found:
        return found
    remainder = _LEAD.sub("", claim or "").strip()
    rest_norm, _ = _normalize(remainder)
    if rest_norm and rest_norm != claim_norm and len(rest_norm) >= 24:
        return _slice(body, norm, origin, rest_norm, remainder)
    return None


def _json_values(obj):
    strings, nums = [], []

    def walk(node):
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, bool) or node is None:
            return
        elif isinstance(node, (int, float)):
            nums.append(_num_key(str(node)))
        else:
            text = str(node).strip()
            if text:
                strings.append(text)

    walk(obj)
    return strings, nums


def _json_relation(claim, obj):
    strings, nums = _json_values(obj)
    if not strings or not nums:
        return None
    claim_norm, _ = _normalize(claim)
    seq, _polar = _atoms(claim_norm)
    claim_nums = [a[1] for a in seq if a[0] == "num"]
    claim_days = {a[1] for a in seq if a[0] == "day"}
    if not claim_nums:
        return None
    present = []
    value_days = set()
    for item in strings:
        item_norm, _ = _normalize(item)
        if not item_norm:
            continue
        present.append(item_norm in claim_norm)
        for atom in _atoms(item_norm)[0]:
            if atom[0] == "day":
                value_days.add(atom[1])
    if claim_days and value_days and claim_days != value_days and any(present):
        return "contradicts"
    if not all(present):
        return None
    if set(claim_nums) != set(nums):
        if set(claim_nums) & set(nums):
            return "contradicts"
        return None
    return "entails"


def _item(kind, doc, quote, span, relation, fields):
    ref = str(doc.get("id") or doc.get("url") or kind)
    return {
        "kind": kind,
        "ref": ref,
        "quote": (quote or "")[:500],
        "span": span,
        "relation": relation,
        "by": "rule",
        **fields,
    }


def match_spans(claim, docs, kind):
    """Exact span, or a slot mismatch on an aligned window. Overlap is not used."""
    out = []
    for doc in docs or []:
        if not isinstance(doc, dict):
            continue
        structured = doc.get("output") if isinstance(doc.get("output"), (dict, list)) else None
        if structured is None and isinstance(doc.get("text"), (dict, list)):
            structured = doc.get("text")
        body = _body(doc)
        if not body.strip():
            continue
        fields = warrant_fields(doc, kind)
        support = _support_span(claim, body)
        if support:
            quote, span = support
            out.append(_item(kind, doc, quote, span, "entails", fields))
        elif structured is not None:
            relation = _json_relation(claim, structured)
            if relation:
                out.append(_item(kind, doc, body, [0, len(body)], relation, fields))
                continue
        covered = support[1] if support else None
        claim_norm, _ = _normalize(claim)
        for window, start, end in _windows(body):
            if covered and start >= covered[0] and end <= covered[1]:
                continue
            if covered and covered[0] >= start and covered[1] <= end:
                continue
            window_norm, _ = _normalize(window)
            if not _conflict(claim_norm, window_norm):
                continue
            out.append(_item(kind, doc, window, [start, end], "contradicts", fields))
            break
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
