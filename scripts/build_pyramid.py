#!/usr/bin/env python3
"""Build one field pyramid from its published maps.

Does not call a language model. Nodes the rules and embeddings cannot place
are written to pyramids/queues/<FIELD>.json.

    python3 scripts/build_pyramid.py --field EV
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from pyramid import build_pyramid, render_markdown


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build a Minto pyramid for one field.")
    parser.add_argument("--field", required=True)
    args = parser.parse_args(argv)
    field = args.field
    pyramid, queue = build_pyramid(field)
    (ROOT / "pyramids").mkdir(parents=True, exist_ok=True)
    queue_dir = ROOT / "pyramids" / "queues"
    queue_dir.mkdir(parents=True, exist_ok=True)
    (ROOT / "pyramids" / f"{field}.json").write_text(
        json.dumps(pyramid, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (ROOT / "pyramids" / f"{field}_minto.md").write_text(render_markdown(pyramid), encoding="utf-8")
    (queue_dir / f"{field}.json").write_text(
        json.dumps({
            "field": field,
            "model": "qwen3:30b-a3b",
            "endpoint": "http://localhost:11434/v1/chat/completions",
            "items": queue,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    run_dir = ROOT / "runs" / "pyramid"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / f"{field}.json").write_text(
        json.dumps(pyramid["build"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps(pyramid["build"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
