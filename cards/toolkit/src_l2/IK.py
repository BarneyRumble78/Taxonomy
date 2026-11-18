# Indigenous knowledge, level 2. No card carries tools. Each card takes its statement from its level-1 parent card.
# The builder adds the review note to every IK card.
import json
from pathlib import Path
_root = Path(__file__).resolve().parents[3]
_l1 = {c["node"]: c for c in json.loads((_root / "cards" / "toolkit" / "IK_L1.json").read_text(encoding="utf-8"))}
_map = json.loads((_root / "maps" / "IK" / "anzsrc2020.json").read_text(encoding="utf-8"))
T = {}
for _n in _map["nodes"]:
    if _n["level"] == 2:
        _p = _l1[_n["parent"]]
        T[_n["code"]] = (list(_p["solves"]), {k: " ".join(v) for k, v in _p["signature"].items()}, [], [], [])
