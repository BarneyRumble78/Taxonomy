#!/usr/bin/env python3
"""Check a question pyramid, and optionally render its markdown. No model calls.

    python3 scripts/build_question_pyramid.py pyramids/questions/EV_Q1_nz_nitrogen_eutrophication.json
    python3 scripts/build_question_pyramid.py path/to/question.json --write

The governing thought is one sentence of at most 25 words. The key line is
two to five yes/no issues. Each issue names its evidence. --write renders
markdown beside the JSON. It does not call a model.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from question_pyramid import load, render, validate


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Check or render a question pyramid.")
    parser.add_argument("path", help="JSON file for one question pyramid.")
    parser.add_argument("--write", action="store_true", help="Write the markdown beside the JSON.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    path = Path(args.path)
    data = load(path)
    problems = validate(data)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"valid {path}")
    if args.write:
        dest = path.with_suffix(".md")
        dest.write_text(render(data), encoding="utf-8")
        print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
