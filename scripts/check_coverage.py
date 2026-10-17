"""Coverage check for the subfield maps (R13).

For every field: each map node must carry a registered cell of that field (any face; key-line counts shown),
and must sit in the folder of the field that owns the cell. Prints nodes per cell so thin cells show up.
Exit code 1 on any failure.
"""
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()


def main():
    cells, known = {}, {r["id"] for r in json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))}
    for f in FIELDS:
        cards = json.loads((ROOT / "cards" / "lens" / f"{f}.json").read_text(encoding="utf-8"))
        cells[f] = [c["id"] for c in cards[1:]]
        known |= set(cells[f])
    # MA has no section-12 registry yet; its Face B MSC bridge cells are named in pyramids/MA.md (Side C).
    known |= {f"MA.B.C{i}" for i in range(1, 6)}
    bad, total = [], 0
    print(f"{'field':5} {'maps':>4} {'nodes':>7}  nodes per key-line cell")
    for f in FIELDS:
        count, n_maps, n = Counter(), 0, 0
        for p in sorted((ROOT / "maps" / f).glob("*.json")):
            n_maps += 1
            for node in json.loads(p.read_text(encoding="utf-8"))["nodes"]:
                n += 1
                c = node.get("taxonomy_cell", "")
                if c not in known or not c.startswith(f + "."):
                    bad.append(f"{p.relative_to(ROOT)} {node['id']} cell {c!r} is not a registered cell of {f}")
                count[c] += 1
        total += n
        other = sum(v for c, v in count.items() if c not in cells[f])
        line = "  ".join(f"{c.split('.')[-1]}={count[c]}" for c in cells[f]) + (f"  other faces={other}" if other else "")
        empty = [c for c in cells[f] if not count[c]]
        print(f"{f:5} {n_maps:>4} {n:>7}  {line}" + (f"  EMPTY: {', '.join(empty)}" if empty else ""))
    print(f"total nodes {total}")
    for b in bad[:20]:
        print("FAIL", b)
    if bad:
        print(f"{len(bad)} failures")
        sys.exit(1)
    print("All map nodes sit under a registered cell of their own field.")


if __name__ == "__main__":
    main()
