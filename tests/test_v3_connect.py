"""Smoke retrodiction cases for Connect (Roadmap G2, seed set).
Each states a problem's shape only; the known historical tool must rank in the top 5."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from connect import connect

CASES = [
    ("sparse signal from few measurements (compressed sensing)", {"task": ["infer"], "structure": ["time_series"], "direction": ["inverse"], "data": ["data_poor"]}, "MA.TK.42"),
    ("count arrangements up to symmetry (Pólya)", {"task": ["count"], "symmetry": ["permutation"], "domain_type": ["discrete"]}, "MA.TK.20"),
    ("shape of a point cloud (persistent homology)", {"task": ["infer", "classify"], "structure": ["geometric_space"], "data": ["data_rich"]}, "MA.TK.55"),
    ("stable outcome among competing agents (Nash)", {"task": ["predict"], "agents": ["multiple_competing"]}, "MA.TK.91"),
    ("reconstruct an interior from projections (Radon / CT)", {"task": ["infer"], "direction": ["inverse"]}, "MA.TK.44"),
]

def test_schema_counts():
    cards = json.loads((ROOT / "cards" / "toolkit" / "MA.json").read_text(encoding="utf-8"))
    assert len(cards) == 63

def test_retrodiction_top5():
    misses = []
    for name, sig, want in CASES:
        got = [r["card"] for r in connect(sig, top=5)]
        if want not in got:
            misses.append((name, got))
    assert not misses, misses
