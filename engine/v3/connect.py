"""Connect mode, minimal (Roadmap E5): match a problem signature to toolkit cards.

score(card) = sum over facets of weight(facet) * |problem ∩ card| / |problem|
plus a small bonus for each matching task. Ranks every card in the field, so distant
subfields are considered, not only the obvious one.

    python3 engine/v3/connect.py --sig '{"task":["infer"],"direction":["inverse"],"data":["data_poor"]}'
"""
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIELDS = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()
WEIGHTS = {"task": 3.0, "structure": 2.0, "direction": 1.5, "uncertainty": 1.5, "linearity": 1.5,
           "symmetry": 1.5, "dynamics": 1.5, "agents": 1.5, "constraints": 1.0, "domain_type": 1.0,
           "data": 1.0, "scale": 1.0, "scope": 0.5, "goal_quality": 0.5}


def _vals(raw):
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw] if raw else []
    return [v for v in raw if v]


def load_cards(field="MA"):
    if field not in FIELDS:
        raise ValueError("unknown field code")
    cards = []
    for p in sorted((ROOT / "cards" / "toolkit").glob(f"{field}*.json")):
        if p.name.startswith(field):
            cards += json.loads(p.read_text(encoding="utf-8"))
    return cards


def score(problem, card):
    s, why = 0.0, []
    signature = card.get("signature") or {}
    for facet, raw in (problem or {}).items():
        vals = _vals(raw)
        if not vals:
            continue
        hit = set(vals) & set(_vals(signature.get(facet)))
        if hit:
            s += WEIGHTS.get(facet, 1.0) * len(hit) / len(vals)
            why.append(f"{facet}: {', '.join(sorted(hit))}")
    return s, why


def connect(problem, field="MA", top=8):
    ranked = []
    for c in load_cards(field):
        s, why = score(problem, c)
        if s > 0:
            ranked.append({"card": c["id"], "node": c["node"], "name": c["name"], "score": round(s, 2),
                           "matched_on": why, "tools": [t["name"] for t in c["tools"]],
                           "check_conditions": {t["name"]: t["hypotheses"] for t in c["tools"]}})
    ranked.sort(key=lambda r: -r["score"])
    return ranked[:top]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sig", required=True, help="JSON signature, facets from signatures/vocabulary.json")
    ap.add_argument("--field", default="MA")
    ap.add_argument("--top", type=int, default=8)
    a = ap.parse_args()
    print(json.dumps(connect(json.loads(a.sig), a.field, a.top), indent=1, ensure_ascii=False))
