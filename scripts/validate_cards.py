#!/usr/bin/env python3
"""Validate lens cards, toolkit cards and maps against schemas/ (Roadmap B6).

The standard library is enough. A fresh checkout does not need jsonschema.
Signature values must also belong to signatures/vocabulary.json.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = json.loads((ROOT / "signatures" / "vocabulary.json").read_text(encoding="utf-8"))["facets"]
LENS_ID = re.compile(r"^[A-Z]{2}(\.O\.A[0-9]+)?$")
FIELD_ID = re.compile(r"^[A-Z]{2}$")
errs = 0


def err(where, msg):
    global errs
    errs += 1
    print(f"{where}: {msg}")


def strings(where, obj, key):
    val = obj.get(key)
    if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
        err(where, f"{key} must be an array of strings")


def check_lens(card, where):
    where = f"{where} {card.get('id')}"
    for key in ("id", "field", "name", "question", "look_for", "find_out", "settles", "breaks", "rules_of_thumb", "collisions", "status"):
        if key not in card:
            err(where, f"missing {key}")
    if not isinstance(card.get("name"), str) or not isinstance(card.get("question"), str):
        err(where, "name and question must be strings")
    if not LENS_ID.match(str(card.get("id", ""))):
        err(where, f"bad id {card.get('id')}")
    if not FIELD_ID.match(str(card.get("field", ""))):
        err(where, "bad field")
    for key in ("look_for", "find_out", "settles", "breaks", "rules_of_thumb", "collisions"):
        if key in card:
            strings(where, card, key)
    if card.get("status") not in ("draft", "reviewed"):
        err(where, "bad status")
    if "open" in card:
        strings(where, card, "open")


def check_tool(card, where):
    where = f"{where} {card.get('id')}"
    for key in ("id", "field", "node", "name", "solves", "signature", "tools", "status"):
        if key not in card:
            err(where, f"missing {key}")
    if not isinstance(card.get("signature"), dict):
        err(where, "signature must be an object")
    else:
        for facet, vals in card["signature"].items():
            if facet not in VOCAB:
                err(where, f"unknown facet {facet}")
                continue
            if not isinstance(vals, list):
                err(where, f"{facet} must be a list")
                continue
            for value in vals:
                if value not in VOCAB[facet]:
                    err(where, f"bad signature {facet}={value}")
    if not isinstance(card.get("tools"), list):
        err(where, "tools must be a list")
    else:
        for tool in card["tools"]:
            if not isinstance(tool, dict):
                err(where, "tool must be an object")
                continue
            for key in ("name", "does", "hypotheses"):
                if key not in tool:
                    err(where, f"tool missing {key}")
            hyps = tool.get("hypotheses")
            if not isinstance(hyps, list) or not all(isinstance(x, str) for x in hyps):
                err(where, "hypotheses must be an array of strings")
    if "solves" in card:
        strings(where, card, "solves")
    if card.get("status") not in ("draft", "reviewed"):
        err(where, "bad status")


def check_node(node, where):
    where = f"{where} {node.get('id')}"
    for key in ("id", "code", "name", "level"):
        if key not in node:
            err(where, f"missing {key}")
    level = node.get("level")
    if isinstance(level, bool) or not isinstance(level, int) or level < 1:
        err(where, "level must be an integer >= 1")
    if "parent" in node and node["parent"] is not None and not isinstance(node["parent"], str):
        err(where, "parent must be a string or null")
    for key in ("id", "code", "name"):
        if key in node and not isinstance(node[key], str):
            err(where, f"{key} must be a string")


def main():
    for path in sorted((ROOT / "cards" / "lens").glob("*.json")):
        for card in json.loads(path.read_text(encoding="utf-8")):
            check_lens(card, path.name)
    for path in sorted((ROOT / "cards" / "toolkit").glob("*.json")):
        for card in json.loads(path.read_text(encoding="utf-8")):
            check_tool(card, path.name)
    for path in sorted((ROOT / "maps").glob("*/*.json")):
        for node in json.loads(path.read_text(encoding="utf-8")).get("nodes") or []:
            check_node(node, path.name)
    print("valid" if not errs else f"{errs} errors")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
