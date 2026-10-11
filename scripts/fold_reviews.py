"""Fold reviewed labels into a labelled set. Never into the frozen eval file.

A review line is JSON. A reviewed table is TSV with claim, owner, cell, warrant, method.
The output is a new labelled file. A path named heldout, or a file whose bytes match
the frozen set, is refused.
"""
import csv, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FROZEN = ROOT / "pilot" / "heldout.tsv"
FROZEN_SHA256 = "e6826cf6f46b69371f17c95c1aab9c771885bbbecc233e28f95b6f3577a4b856"


def refuse(path):
    path = Path(path)
    if "heldout" in path.name.lower():
        raise SystemExit(f"refusing {path}: the frozen eval is not a training file")
    if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == FROZEN_SHA256:
        raise SystemExit(f"refusing {path}: those bytes are the frozen set")
    try:
        if path.resolve() == FROZEN.resolve():
            raise SystemExit(f"refusing {path}: the frozen eval is not a training file")
    except OSError:
        pass


def load_queue(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def load_reviewed(path):
    with Path(path).open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def fold(queue_path, reviewed_path, out_path):
    refuse(out_path)
    refuse(queue_path)
    refuse(reviewed_path)
    queued = {row.get("claim"): row for row in load_queue(queue_path)}
    chosen = []
    for row in load_reviewed(reviewed_path):
        claim = row.get("claim")
        if claim not in queued:
            continue
        if not row.get("owner"):
            continue
        chosen.append({
            "claim": claim,
            "owner": row.get("owner"),
            "cell": row.get("cell") or "",
            "warrant": row.get("warrant") or "",
            "method": row.get("method") or "",
            "model": (queued[claim].get("model") or ""),
            "prompt_version": (queued[claim].get("prompt_version") or ""),
        })
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["claim", "owner", "cell", "warrant", "method", "model", "prompt_version"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(chosen)
    return chosen


def main(argv):
    if len(argv) != 4:
        raise SystemExit("usage: fold_reviews.py queue.jsonl reviewed.tsv out.tsv")
    rows = fold(argv[1], argv[2], argv[3])
    print(f"wrote {argv[3]} rows={len(rows)}")


if __name__ == "__main__":
    main(sys.argv[1:])
