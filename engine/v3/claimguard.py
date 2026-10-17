"""ClaimGuard: one verdict per atomic claim. Rules only unless an llm is passed.

A model may propose spans. It cannot raise a verdict to supported or contradicted (R22).
The word true is never returned.
"""
import json, re
from pathlib import Path

from certainty import certainty
from checks import check_open, run_checks
from evidence import match_spans, registry_hits
from verdict import ORDER, combine

ROOT = Path(__file__).resolve().parents[2]
_TYPES = json.loads((ROOT / "engine" / "claim_types.json").read_text(encoding="utf-8"))
_CUES = [(name, [re.compile(p, re.I) for p in pats]) for name, pats in (
    (name, _TYPES["cues"][name]) for name in _TYPES["priority"]
)]

import sys
sys.path.insert(0, str(ROOT / "engine"))
from adjudicator import REQUIRED_WARRANT, DEFAULT_WARRANT  # noqa: E402
from taxonomy_engine import instruction_heuristic, rule_placement, split_sentences  # noqa: E402

_TRAD = re.compile(r"\b(?:scripture|sacred|revealed|tradition holds|the church teaches|doctrine|canon)\b", re.I)
_DATED = re.compile(r"\b(?:1[0-9]{3}|20[0-9]{2})\b|\b\d+(?:\.\d+)?\s?(?:%|kg|km)\b", re.I)
_DUTY = re.compile(r"\bmust\b|\blegal duty\b|\bact (?:19|20)\d\d\b", re.I)
_SENSE = re.compile(r"\bmeans\b|\bdefinition of the word\b", re.I)
_Q = re.compile(r"\?\s*$")
_WORD = re.compile(r"[A-Za-z0-9]+")


def classify_claim_type(text):
    """Rule cues. The first matching type in the shared priority list wins."""
    raw = text or ""
    for name, pats in _CUES:
        if any(p.search(raw) for p in pats):
            return name
    return None


def required_warrant(placement, text):
    kind = classify_claim_type(text)
    if kind and kind in REQUIRED_WARRANT:
        return {"code": REQUIRED_WARRANT[kind], "from": "claim_type", "claim_type": kind}
    owner = (placement or {}).get("owner")
    code = DEFAULT_WARRANT.get(owner) if owner else None
    return {"code": code, "from": "owner", "claim_type": None}


def _and_split(sentence):
    parts = [sentence]
    out = []
    for part in parts:
        bits = part.split(" and ")
        if len(bits) == 2 and all(len(_WORD.findall(b)) >= 6 for b in bits):
            out.extend(b.strip() for b in bits if b.strip())
        else:
            out.append(part.strip())
    return [p for p in out if p]


def split_claims(text, llm=None, max_claims=20):
    """Sentence split, then a conjunction split when both sides are long enough."""
    raw = text or ""
    pieces = []
    for sentence in split_sentences(raw):
        pieces.extend(_and_split(sentence))
    if llm is not None:
        try:
            proposed = llm("Split into atomic claims. Reply JSON {\"claims\": [...]} of substrings.\n" + raw[:4000])
            extra = proposed.get("claims") if isinstance(proposed, dict) else None
            if isinstance(extra, list):
                kept = []
                low = raw.lower()
                for item in extra:
                    bit = str(item).strip()
                    if bit and bit.lower() in low:
                        kept.append(bit)
                if kept:
                    pieces = kept
        except Exception:
            pass
    cursor = 0
    out = []
    for bit in pieces[:max_claims]:
        idx = raw.find(bit, cursor)
        if idx < 0:
            idx = raw.lower().find(bit.lower(), cursor)
        span = [idx, idx + len(bit)] if idx >= 0 else [0, 0]
        if idx >= 0:
            cursor = span[1]
        out.append({"id": f"c{len(out) + 1}", "text": bit, "span": span})
    return out or [{"id": "c1", "text": raw.strip(), "span": [0, len(raw)]}]


def _w13(text, placement):
    owner = (placement or {}).get("owner")
    if owner in ("RE", "IK"):
        return False
    if not _TRAD.search(text or ""):
        return False
    return bool(_DATED.search(text or "") or _DUTY.search(text or "") or _SENSE.search(text or ""))


def _public_placement(p):
    if not p:
        return None
    return {
        "owner": p.get("owner"),
        "cell": p.get("cell"),
        "warrant": p.get("warrant"),
        "method": p.get("method"),
        "confidence": p.get("confidence"),
    }


def _siblings(claims):
    """R21: a later claim that negates an earlier one, at a stronger warrant, contradicts it."""
    from evidence import _NEG, _words, numbers_agree
    from certainty import warrant_ceiling
    from certainty import rank
    flags = {}
    for i, a in enumerate(claims):
        for b in claims:
            if a is b:
                continue
            if not _NEG.search(b["text"]) or _NEG.search(a["text"]):
                continue
            wa, wb = _words(a["text"]), set(_words(b["text"]))
            if not wa or sum(1 for w in wa if w in wb) / len(wa) < 0.6:
                continue
            if numbers_agree(a["text"], b["text"]) is False:
                continue
            sa = rank(warrant_ceiling((a.get("warrant_required") or {}).get("code")))
            sb = rank(warrant_ceiling((b.get("warrant_required") or {}).get("code")))
            if sb > sa:
                flags.setdefault(a["id"], "stronger")
            else:
                flags.setdefault(a["id"], "same")
    return flags


def verify(text, sources=None, tool_outputs=None, *, llm=None, split="rule", max_claims=20):
    """R18 verdicts. llm is advisory. Retrieval is not evidence."""
    claims = split_claims(text, llm=llm if split == "model" else None, max_claims=max_claims)
    built = []
    for claim in claims:
        sentence = claim["text"]
        instr = instruction_heuristic(sentence) or bool(_Q.search(sentence or ""))
        placement = None if instr else rule_placement(sentence)
        if placement and placement.get("confidence") is not None and placement["confidence"] < 0.4 and not instr:
            # The rule stage abstains under 0.40. Mirror that gate per atomic claim.
            placement = None
        wreq = required_warrant(placement, sentence)
        evidence = []
        evidence += match_spans(sentence, sources or [], "source")
        evidence += match_spans(sentence, tool_outputs or [], "tool_output")
        evidence += registry_hits(sentence, placement)
        if llm is not None and (sources or tool_outputs):
            try:
                blob = json.dumps({"claim": sentence, "sources": sources or [], "tools": tool_outputs or []})[:8000]
                reply = llm("Label entailment. Reply JSON {\"relation\":\"entails|contradicts|neutral\",\"quote\":\"\"}.\n" + blob)
                rel = str((reply or {}).get("relation") or "neutral")
                if rel in ("entails", "contradicts", "neutral") and rel != "neutral":
                    evidence.append({
                        "kind": "source", "ref": "model", "quote": str(reply.get("quote") or "")[:240],
                        "span": [0, 0], "relation": rel, "warrant_held": None, "by": "model",
                    })
            except Exception:
                pass
        checks = [] if instr else run_checks(sentence)
        built.append({
            "claim": claim, "text": sentence, "placement": placement, "wreq": wreq,
            "evidence": evidence, "checks": checks, "instruction": instr,
            "open": check_open(sentence), "w13": _w13(sentence, placement),
            "cert": certainty(sentence),
        })
    prepared = []
    for row in built:
        prepared.append({
            "id": row["claim"]["id"], "text": row["text"],
            "warrant_required": row["wreq"],
        })
    sibling = _siblings(prepared)
    results = []
    for row in built:
        contested = row["open"] or sibling.get(row["claim"]["id"]) == "same"
        if sibling.get(row["claim"]["id"]) == "stronger":
            row["evidence"].append({
                "kind": "source", "ref": "sibling", "quote": "another claim in this text",
                "span": [0, 0], "relation": "contradicts", "warrant_held": row["wreq"].get("code"),
                "by": "rule",
            })
        decided = combine(
            row["placement"], row["wreq"], row["cert"], row["evidence"], row["checks"],
            contested=contested, instruction=row["instruction"], w13=row["w13"],
            ik=(row["placement"] or {}).get("owner") == "IK",
        )
        mismatch = bool(
            row["placement"] and row["wreq"].get("code") and row["placement"].get("warrant")
            and row["wreq"]["code"] != row["placement"].get("warrant")
        )
        results.append({
            "id": row["claim"]["id"],
            "text": row["text"],
            "span": row["claim"]["span"],
            "placement": _public_placement(row["placement"]),
            "warrant_required": row["wreq"],
            "warrant_mismatch": mismatch,
            "certainty": {
                "level": row["cert"]["level"],
                "cues": row["cert"]["cues"],
                "ceiling_ok": decided["verdict"] != "overstated",
            },
            "evidence": decided.get("evidence") or [],
            "checks": decided.get("checks") or [],
            "verdict": decided["verdict"],
            "qualifier": decided.get("qualifier"),
            "reason": decided.get("reason") or [],
            "status": decided.get("status"),
            "certainty_without_evidence": bool(decided.get("certainty_without_evidence")),
        })
    counts = {name: 0 for name in ORDER}
    for row in results:
        counts[row["verdict"]] = counts.get(row["verdict"], 0) + 1
    worst = next((name for name in ORDER if counts.get(name)), "unverified")
    return {
        "version": "claimguard-0.1",
        "engine": "3.0.0",
        "claims": results,
        "summary": {"worst": worst, "counts": counts},
    }
