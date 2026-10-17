"""Ordered verdicts. The first match wins. The word true is never returned.

First-match order: out_of_scope, contradicted, contested, overstated, supported, unverified.
That order is not severity. summary.worst uses SEVERITY:
contradicted, overstated, contested, unverified, out_of_scope, supported.

A supporting span and a contradicting span of the same warrant strength are contested.
A contradicting span wins when it is stronger, or when it is the only bound evidence.
"""
import core
from certainty import ceiling_ok, rank, warrant_ceiling

ORDER = ("out_of_scope", "contradicted", "contested", "overstated", "supported", "unverified")
SEVERITY = ("contradicted", "overstated", "contested", "unverified", "out_of_scope", "supported")
_STRONG = {"supported", "contradicted"}


def _ceil(code):
    return rank(warrant_ceiling(code))


def _shown(evidence, checks):
    for item in evidence or []:
        if item.get("by") == "rule" and item.get("relation") in ("entails", "contradicts"):
            if str(item.get("quote") or item.get("ref") or "").strip():
                return True
    for item in checks or []:
        if item.get("id") and item.get("result") in ("consistent", "contradicted"):
            if item.get("kind") != "missing_hypotheses":
                return True
    return False


def combine(placement, wreq, cert, evidence, checks, contested=False, *, instruction=False, question=False, w13=False, ik=False):
    """Return verdict, qualifier, reason, status, and certainty_without_evidence."""
    reasons = []
    evidence = list(evidence or [])
    checks = list(checks or [])
    level = (cert or {}).get("level") or "hedged"
    code = (wreq or {}).get("code")
    rule = [e for e in evidence if e.get("by") == "rule"]
    entails = [e for e in rule if e.get("relation") == "entails"]
    contradicts = [e for e in rule if e.get("relation") == "contradicts"]
    model_contra = [e for e in evidence if e.get("by") == "model" and e.get("relation") == "contradicts"]
    held_codes = [e.get("warrant_held") for e in entails + contradicts if e.get("warrant_held")]
    passed = [c for c in checks if c.get("result") == "consistent" and c.get("kind") != "missing_hypotheses"]
    failed = [c for c in checks if c.get("result") == "contradicted" and c.get("kind") != "missing_hypotheses"]
    missing_hyp = [c for c in checks if c.get("kind") == "missing_hypotheses"]
    for c in passed + failed:
        if c.get("warrant_held"):
            held_codes.append(c["warrant_held"])
    wheld = max(held_codes, key=_ceil) if held_codes else None

    def pack(verdict, qualifier, status):
        sources = [str(e.get("quote") or e.get("ref"))[:200] for e in evidence if e.get("by") == "rule"]
        sources += [c["id"] for c in checks if c.get("id")]
        out = {
            "verdict": verdict,
            "qualifier": qualifier,
            "reason": reasons,
            "status": status,
            "warrant_held": wheld,
            "certainty_without_evidence": False,
            "evidence": evidence,
            "checks": checks,
            "sources": [s for s in sources if s],
        }
        core.guard_status(out)
        if ik and out["verdict"] not in ("unverified", "contested", "out_of_scope"):
            reasons.append("IK placements stay provisional until Māori-led review.")
            out["verdict"] = "unverified"
            out["qualifier"] = None
            out["status"] = "proposed"
        if out["verdict"] == "true":
            out["verdict"] = "unverified"
            reasons.append("R18: no verdict is true.")
        return out

    if failed:
        item = failed[0]
        reasons.append(f"R21: check {item['id']} failed. {item.get('note', '')}".strip())
        status = "contradicted (small cases)" if item.get("kind") == "equation_small_cases" else "tested"
        return pack("contradicted", None, status)

    if instruction or question or w13:
        if question:
            reasons.append("R18: the text is a question, not a claim.")
        elif instruction:
            reasons.append("R18: the text reads as an instruction, not a claim.")
        else:
            reasons.append("W13 does not license a measurement, a date, a legal duty, or a word meaning.")
        return pack("out_of_scope", None, "proposed")

    def strongest(items):
        codes = [e.get("warrant_held") for e in items if e.get("warrant_held")]
        return max(codes, key=_ceil) if codes else None

    bound = bool(entails or contradicts or passed)
    if entails and contradicts:
        entail_held = strongest(entails)
        contra_held = strongest(contradicts)
        if _ceil(contra_held) > _ceil(entail_held):
            item = contradicts[0]
            reasons.append(f"R20: span {item.get('ref')} contradicts the claim.")
            return pack("contradicted", None, "source_found")
        if _ceil(contra_held) == _ceil(entail_held):
            reasons.append("R20: support and contradiction hold the same warrant, so the claim is contested.")
            return pack("contested", None, "source_found")
        contradicts = []
    elif contradicts:
        item = contradicts[0]
        reasons.append(f"R20: span {item.get('ref')} contradicts the claim.")
        return pack("contradicted", None, "source_found")

    if contested and (placement or bound):
        cross = [e for e in evidence if e.get("relation") == "cross"]
        if cross:
            reasons.append(f"R21: {cross[0].get('ref')} states the opposing claim, so the pair is contested.")
        else:
            reasons.append("R6: the claim is marked open or contested, or the evidence disagrees with itself.")
        return pack("contested", None, "proposed")

    small = [c for c in passed if c.get("kind") == "equation_small_cases"]
    only_none = any(c.get("model_claim") in ("none", "only") for c in small)
    evidence_exists = bool(entails or passed or contradicts)
    above = wheld is not None and not ceiling_ok(level, wheld)
    weaker = wheld is not None and code is not None and _ceil(wheld) < _ceil(code)
    established_soft = any(
        e.get("relation") == "entails" and e.get("status") in ("proposed", "conditions_checked")
        for e in rule
    )

    if missing_hyp:
        reasons.append(missing_hyp[0]["note"])
        return pack("overstated", None, "proposed")
    if only_none and small and not failed:
        reasons.append("R19: an only or none claim rests on a small-case search alone.")
        return pack("overstated", "small cases", "proposed")
    small_only = bool(small) and not entails and all(c.get("kind") == "equation_small_cases" for c in passed)
    if small_only and above:
        reasons.append(f"R19: stated certainty {level} exceeds what a small-case search can hold.")
        return pack("overstated", "small cases", "proposed")
    if evidence_exists and not small_only and (above or weaker or established_soft):
        if above:
            reasons.append(f"R19: stated certainty {level} exceeds the {wheld} ceiling.")
        if weaker:
            reasons.append(f"R19: warrant held {wheld} is weaker than warrant required {code}.")
        if established_soft:
            reasons.append("R15: the claim is stated as established while the evidence is not.")
        return pack("overstated", None, "proposed")

    meets = False
    warrant_ok = code is None or (wheld is not None and _ceil(wheld) >= _ceil(code))
    if entails and wheld and warrant_ok and ceiling_ok(level, wheld):
        meets = True
        reasons.append(f"R20: span {entails[0].get('ref')} entails the claim at {wheld}.")
    check_meet = [
        c for c in passed
        if c.get("kind") == "arithmetic"
        and (code is None or _ceil(c.get("warrant_held")) >= _ceil(code))
    ]
    if check_meet and ceiling_ok(level, check_meet[0].get("warrant_held")):
        meets = True
        reasons.append(f"R18: check {check_meet[0]['id']} passed.")
    if meets and not contradicts and not failed:
        status = "tested" if check_meet else "source_found"
        return pack("supported", None, status)

    if small and not only_none and ceiling_ok(level, "W9"):
        reasons.append("R18: a small-case search found no counterexample in range. This is not a proof.")
        return pack("supported", "small cases", "tested")

    if not placement and not bound:
        reasons.append("R18: the engine abstained, so the text is out of scope.")
        return pack("out_of_scope", None, "proposed")

    if model_contra:
        reasons.append("R22: a model noted a possible contradiction. That alone is not a verdict.")
    if level != "hedged" and not evidence_exists:
        reasons.append("R19: certainty without evidence.")
        out = pack("unverified", None, "unverified (model reasoning)" if model_contra else "proposed")
        out["certainty_without_evidence"] = True
        return out
    if not reasons:
        reasons.append("R18: no evidence met the bar. The verdict is unverified.")
    return pack("unverified", None, "unverified (model reasoning)" if model_contra else "proposed")
