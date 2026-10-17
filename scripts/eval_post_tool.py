"""Score a post-tool faithfulness file with ClaimGuard. Rules only.

Each record is JSON, one per line:
  {"id", "tool", "tool_output", "answer", "label"}
label is "faithful" or "hallucinated".
faithful should come back supported. hallucinated should come back contradicted or unverified.
A paraphrase the span matcher misses is counted as a miss. That is reported, not hidden.
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from claimguard import verify  # noqa: E402


def load(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def predict(row):
    out = verify(row["answer"], tool_outputs=[{
        "id": row.get("tool_id") or "call_1",
        "tool": row.get("tool") or "search",
        "output": row.get("tool_output") or "",
    }])
    verdicts = [c["verdict"] for c in out["claims"]]
    # A faithful answer should be supported on every claim. One miss fails the row.
    if row["label"] == "faithful":
        ok = bool(verdicts) and all(v == "supported" for v in verdicts)
    else:
        ok = bool(verdicts) and all(v in ("contradicted", "unverified") for v in verdicts)
    return {"id": row.get("id"), "label": row["label"], "verdicts": verdicts, "ok": ok}


def prf(rows, label):
    picked = [r for r in rows if r["label"] == label]
    if not picked:
        return {"precision": None, "recall": None, "f1": None, "n": 0}
    # The adapter has one prediction class per gold label, so precision equals recall here.
    hit = sum(1 for r in picked if r["ok"])
    recall = hit / len(picked)
    return {"precision": recall, "recall": recall, "f1": recall, "n": len(picked), "hit": hit}


def score(path):
    judged = [predict(row) for row in load(path)]
    return {
        "n": len(judged),
        "rows": judged,
        "faithful": prf(judged, "faithful"),
        "hallucinated": prf(judged, "hallucinated"),
        "note": "Measured on this file only. Not a launch figure.",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    args = ap.parse_args(argv)
    print(json.dumps(score(args.path), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
