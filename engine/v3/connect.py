"""Connect mode, minimal (Roadmap E5): match a problem signature to toolkit cards.

score(card) = sum over facets of weight(facet) * |problem ∩ card| / |problem|
plus a small bonus for each matching task. Ranks every card in the field, so distant
subfields are considered, not only the obvious one.

    python3 engine/v3/connect.py --sig '{"task":["infer"],"direction":["inverse"],"data":["data_poor"]}'
"""
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEIGHTS = {"task": 3.0, "structure": 2.0, "direction": 1.5, "uncertainty": 1.5, "linearity": 1.5,
           "symmetry": 1.5, "dynamics": 1.5, "agents": 1.5, "constraints": 1.0, "domain_type": 1.0,
           "data": 1.0, "scale": 1.0, "scope": 0.5, "goal_quality": 0.5}


def load_cards(field="MA"):
    cards = []
    for p in sorted((ROOT / "cards" / "toolkit").glob(f"{field}*.json")):
        cards += json.loads(p.read_text(encoding="utf-8"))
    return cards


def score(problem, card):
    s, why = 0.0, []
    for facet, vals in problem.items():
        have = set(card["signature"].get(facet, []))
        hit = set(vals) & have
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
