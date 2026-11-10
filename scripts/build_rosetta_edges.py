"""Write the correspondence edges implied by rosetta/cores.json. No model calls.

Two cells that bind the same formal core get one undirected edge, with the
role mapping, the shared assumptions and the differences filled in.

Run: python3 scripts/build_rosetta_edges.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
import rosetta  # noqa: E402

problems = rosetta.check(ROOT)
if problems:
    print("\n".join(problems))
    sys.exit("rosetta/cores.json has problems; no edges were written.")
edges = rosetta.derived_edges(rosetta.load(ROOT))
out = ROOT / "correspondences" / "rosetta_edges.json"
body = {"source": "rosetta/cores.json", "generated_by": "scripts/build_rosetta_edges.py",
        "date": rosetta.SEED_DATE, "note": "Generated. Do not edit by hand; rerun the script.",
        "edges": edges}
out.write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"{out.relative_to(ROOT)}: {len(edges)} edges")
