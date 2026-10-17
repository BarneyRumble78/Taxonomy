"""Deterministic checks. core.check_equations is wrapped, not replaced."""
import re

import core

_ARITH = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*(×|\*|x|times|\+|-|/|÷|divided by)\s*(-?\d+(?:\.\d+)?)\s*=\s*(-?\d+(?:\.\d+)?)",
    re.I,
)
_HYP = re.compile(r"\b(?:if|assume|assumed|hypothesis|hypotheses|given|let|where|provided that|suppose)\b", re.I)
_THEOREM = re.compile(r"\btheorem\b", re.I)
_OPEN = re.compile(r"\b(?:open problem|remains open|is open|still open|contested|unresolved)\b", re.I)
_ESTABLISHED = re.compile(r"\b(?:established|proves|proven|certainly)\b", re.I)


def _apply(op, a, b):
    if op in ("×", "*", "x", "times"):
        return a * b
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op in ("/", "÷", "divided by"):
        if b == 0:
            return None
        return a / b
    return None


def check_arithmetic(claim):
    reports = []
    for i, m in enumerate(_ARITH.finditer(claim or ""), start=1):
        # A power expression is the equation checker's job.
        if "^" in m.group(0) or "²" in m.group(0):
            continue
        a, b = float(m.group(1)), float(m.group(3))
        got = _apply(m.group(2).lower(), a, b)
        if got is None:
            continue
        stated = float(m.group(4))
        ok = abs(got - stated) <= 1e-9
        reports.append({
            "id": f"arith{i}",
            "kind": "arithmetic",
            "result": "consistent" if ok else "contradicted",
            "note": f"{m.group(0)} {'holds' if ok else 'does not hold'} as arithmetic.",
            "warrant_held": "W2",
        })
    return reports


def check_equations(claim):
    """Delegate to core.check_equations. A failed search is a shown contradiction."""
    report = core.check_equations(claim)
    if not report:
        return []
    failed = report.get("consistent") is False
    return [{
        "id": "eq1",
        "kind": "equation_small_cases",
        "result": "contradicted" if failed else "consistent",
        "note": report.get("note") or "",
        "model_claim": report.get("model_claim"),
        "warrant_held": "W2",
    }]


def check_hypotheses(claim):
    if not _THEOREM.search(claim or ""):
        return []
    if _HYP.search(claim or ""):
        return []
    return [{
        "id": "hyp1",
        "kind": "missing_hypotheses",
        "result": "contradicted",
        "note": "R5: a named theorem does not state its hypotheses.",
        "warrant_held": None,
    }]


def check_open(claim):
    return _OPEN.search(claim or "") is not None


def check_established_wording(claim):
    return _ESTABLISHED.search(claim or "") is not None


def run_checks(claim):
    return check_arithmetic(claim) + check_equations(claim) + check_hypotheses(claim)
