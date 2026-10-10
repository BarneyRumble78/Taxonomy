"""Build engine/retrieval_index.json from pyramid sections 2, 3 and 4.

Uses BAAI/bge-small-en-v1.5 through fastembed. The same embed call, with no
query prefix, is used for chunks and for later queries. Vectors are L2-normalised
and rounded to 6 decimal places so the Worker cosine uses the stored numbers.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import taxonomy_engine as te


def main():
    digest, chunks = te.chunks_sha256(ROOT)
    texts = [c["text"] for c in chunks]
    vectors = te.embed_queries(texts)
    index = {
        "model": "BAAI/bge-small-en-v1.5",
        "dim": 384,
        "words": 90,
        "sections": [2, 3, 4],
        "chunks_sha256": digest,
        "fields": [c["field"] for c in chunks],
        "vectors": vectors,
    }
    if any(len(v) != 384 for v in vectors):
        raise SystemExit("embedding dimension is not 384")
    out = ROOT / "engine" / "retrieval_index.json"
    out.write_text(json.dumps(index, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {out} chunks={len(chunks)} sha256={digest}")


if __name__ == "__main__":
    main()
