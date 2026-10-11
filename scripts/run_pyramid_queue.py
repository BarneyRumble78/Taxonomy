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


def request_body(item):
    """One queue item, thinking off, group_id constrained to the candidates or unsure."""
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
            {
                "role": "system",
                "content": (
                    "Choose the group_id this concept belongs to. "
                    "Use unsure when none of the groups fits. Reply with the schema only."
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
    done = {}
    if dest.exists():
        previous = json.loads(dest.read_text(encoding="utf-8"))
        for row in previous.get("items") or []:
            done[row["node_id"]] = row
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    url = host + "/v1/chat/completions"
    for item in items:
        if item["node_id"] in done:
            continue
        reply = _post(url, request_body(item))
        content = reply["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        done[item["node_id"]] = {
            "node_id": item["node_id"],
            "name": item.get("name"),
            "cell": item.get("cell"),
            "group_id": parsed.get("group_id"),
            "reason": parsed.get("reason"),
        }
        dest.write_text(
            json.dumps({"field": field, "model": MODEL, "items": list(done.values())}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"placed {len(done)} items in {dest}")


if __name__ == "__main__":
    main()
