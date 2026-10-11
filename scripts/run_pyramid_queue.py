#!/usr/bin/env python3
"""Place queued pyramid nodes with the local model.

    python3 scripts/run_pyramid_queue.py --field EV

One item per call. Reads pyramids/queues/<FIELD>.json and writes
pyramids/queues/<FIELD>.placed.json. A run can be stopped and started again.
Does not edit pyramids/<FIELD>.json.

The call is OpenAI-compatible: POST http://localhost:11434/v1/chat/completions,
model qwen3:30b-a3b, think false, JSON schema.
"""
import argparse
import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = "qwen3:30b-a3b"
DPSIR_ORDER = ("EV.O.A1", "EV.O.A2", "EV.O.A3", "EV.O.A4", "EV.O.A5")


def item_task(item):
    """place, unless the item asks for a summary. A row with no task is a place result."""
    if item.get("task"):
        return item["task"]
    if item.get("needs_summary"):
        return "summarise"
    return "place"


def result_matches(item, row):
    """True when a saved row still answers this item.

    A place row from an older queue counts only when its group_id is still
    one of the candidates, or is unsure. A summary is a different task.
    """
    if item_task(row) != item_task(item):
        return False
    if item_task(item) == "summarise":
        return bool(item.get("point_id")) and row.get("point_id") == item.get("point_id")
    if row.get("node_id") != item.get("node_id"):
        return False
    chosen = row.get("group_id")
    if chosen == "unsure":
        return True
    offered = [cand.get("group_id") for cand in (item.get("candidates") or []) if cand.get("group_id")]
    return chosen in offered


def _dpsir_text(cell):
    field = (cell or "").split(".")[0] or "EV"
    path = ROOT / "pyramids" / "rules" / f"{field}.json"
    if not path.exists():
        return ""
    rules = json.loads(path.read_text(encoding="utf-8"))
    lines = rules.get("dpsir") or {}
    return " ".join(lines[key] for key in DPSIR_ORDER if key in lines)


def request_body(item):
    """One queue item, thinking off. Place items choose a group. Summary items write one sentence."""
    if item_task(item) == "summarise":
        return _summary_body(item)
    return _place_body(item)


def _place_body(item):
    groups = []
    for cand in item.get("candidates") or []:
        group_id = cand.get("group_id")
        if not group_id or any(row["group_id"] == group_id for row in groups):
            continue
        groups.append({
            "group_id": group_id,
            "statement": cand.get("statement") or cand.get("facet") or "",
        })
    enum = [row["group_id"] for row in groups] + ["unsure"]
    payload = {
        "name": item.get("name"),
        "cell": item.get("cell"),
        "reason_queued": item.get("reason"),
        "groups": groups,
    }
    defs = _dpsir_text(item.get("cell"))
    system = (
        (defs + " " if defs else "")
        + "Choose the group_id this concept belongs to. "
        "Use unsure when none of the groups fits. Reply with the schema only."
    )
    return {
        "model": MODEL,
        "think": False,
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "placement",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "group_id": {"type": "string", "enum": enum},
                        "reason": {"type": "string"},
                    },
                    "required": ["group_id", "reason"],
                },
            },
        },
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    }


def _summary_body(item):
    payload = {
        "point_id": item.get("point_id"),
        "cell": item.get("cell"),
        "children": item.get("children") or [],
    }
    return {
        "model": MODEL,
        "think": False,
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "summary",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "summary": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["summary", "reason"],
                },
            },
        },
        "messages": [
            {
                "role": "system",
                "content": (
                    "Write one sentence on what these ideas have in common. "
                    "State the shared feature. Do not only name the topic. "
                    "Reply with the schema only."
                ),
            },
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    }


def _post(url, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Place a pyramid queue with the local model.")
    parser.add_argument("--field", required=True)
    args = parser.parse_args(argv)
    field = args.field
    src = ROOT / "pyramids" / "queues" / f"{field}.json"
    dest = ROOT / "pyramids" / "queues" / f"{field}.placed.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) else data
    rows = []
    if dest.exists():
        previous = json.loads(dest.read_text(encoding="utf-8"))
        rows = list(previous.get("items") or [])
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    url = host + "/v1/chat/completions"
    for item in items:
        if any(result_matches(item, row) for row in rows):
            continue
        reply = _post(url, request_body(item))
        content = reply["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        task = item_task(item)
        row = {
            "task": task,
            "node_id": item.get("node_id"),
            "name": item.get("name"),
            "cell": item.get("cell"),
            "reason": parsed.get("reason"),
        }
        if task == "summarise":
            row["needs_summary"] = True
            row["point_id"] = item.get("point_id")
            row["summary"] = parsed.get("summary")
        else:
            row["group_id"] = parsed.get("group_id")
        rows.append(row)
        dest.write_text(
            json.dumps({"field": field, "model": MODEL, "items": rows}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"placed {len(rows)} items in {dest}")


if __name__ == "__main__":
    main()
