#!/usr/bin/env python3
"""Place queued pyramid nodes with the local model.

    python3 scripts/run_pyramid_queue.py --field EV

Reads pyramids/queues/<FIELD>.json. Appends pyramids/queues/<FIELD>.placed.jsonl.
A run can be stopped and started again. Existing pyramids/queues/<FIELD>.placed.json
is read for resume and is not rewritten. Does not edit pyramids/<FIELD>.json.

Each call sends 20 items (15–25) and asks for a JSON array. Three workers run
at once. Before starting Ollama, set the server parallelism to the same number:

    OLLAMA_NUM_PARALLEL=3 ollama serve

The call is OpenAI-compatible: POST http://localhost:11434/v1/chat/completions,
model qwen3:30b-a3b, think false, JSON schema. The system prefix is the same
on every place call so the server can cache it.

    python3 scripts/run_pyramid_queue.py --field EV --limit 20 --dry-run
    python3 scripts/run_pyramid_queue.py --field EV --batch 20 --workers 3
"""
import argparse
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = "qwen3:30b-a3b"
BATCH_SIZE = 20
DEFAULT_WORKERS = 3
PROGRESS_EVERY = 20

SYSTEM_PLACE = (
    "DPSIR. Driver: an industry or activity that creates a load; fold it into pressures. "
    "Pressure: a load from human activity. "
    "State: a measured condition. "
    "Impact: a harm, or the attribution of that harm. "
    "Response: an action that changes a pressure or a state. "
    "Limit: a threshold a state is not meant to cross. "
    "Place each item on one group_id from its choices, or unsure. Reply with the schema only."
)
SYSTEM_SUMMARY = (
    "Write one sentence on what these ideas have in common. "
    "State the shared feature. Do not only name the topic. "
    "Reply with the schema only."
)
PLACE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "group_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["id", "group_id", "reason"],
            },
        }
    },
    "required": ["items"],
}
SUMMARY_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "summary": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["id", "summary", "reason"],
            },
        }
    },
    "required": ["items"],
}


def item_task(item):
    """place, unless the item asks for a summary. A row with no task is a place result."""
    if item.get("task"):
        return item["task"]
    if item.get("needs_summary"):
        return "summarise"
    return "place"


def item_ref(item):
    if item_task(item) == "summarise":
        return str(item.get("point_id") or item.get("node_id") or "")
    return str(item.get("node_id") or "")


def result_matches(item, row):
    """True when a saved row still answers this item.

    A place row from an older queue counts only when its group_id is still
    one of the candidates, or is unsure. A driver row always counts for that
    node. A summary is a different task.
    """
    if item_task(row) != item_task(item):
        return False
    if item_task(item) == "summarise":
        return bool(item.get("point_id")) and row.get("point_id") == item.get("point_id")
    if row.get("node_id") != item.get("node_id"):
        return False
    if row.get("dpsir") == "driver":
        return True
    chosen = row.get("group_id")
    if chosen == "unsure" or row.get("status") == "unsure":
        return True
    offered = [cand.get("group_id") for cand in (item.get("candidates") or []) if cand.get("group_id")]
    return chosen in offered


def load_rules(field, root=None):
    root = Path(root) if root else ROOT
    path = root / "pyramids" / "rules" / f"{field}.json"
    if not path.exists():
        path = ROOT / "pyramids" / "rules" / f"{field}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def is_driver(name, rules):
    low = (name or "").lower()
    return any(phrase.lower() in low for phrase in (rules.get("driver_phrases") or []))


def likely_groups(item):
    """Candidate groups for this item's cell. Other cells are left out of the prompt."""
    cell = item.get("cell")
    groups = []
    for cand in item.get("candidates") or []:
        if cell and cand.get("cell") and cand.get("cell") != cell:
            continue
        group_id = cand.get("group_id")
        if not group_id or any(row["group_id"] == group_id for row in groups):
            continue
        statement = cand.get("statement") or cand.get("facet") or ""
        statement = " ".join(str(statement).split())
        if len(statement) > 80:
            statement = statement[:77] + "..."
        groups.append({"group_id": group_id, "statement": statement})
    return groups


def driver_group(item):
    """The pressure cell. Drivers are folded into that group, not split across facets."""
    for cand in item.get("candidates") or []:
        if cand.get("group_id") and cand.get("cell") == "EV.O.A1" and not cand.get("facet"):
            return cand["group_id"]
    for cand in item.get("candidates") or []:
        if cand.get("group_id") and cand.get("cell") == "EV.O.A1":
            return cand["group_id"]
    return "EV.P.1"


def driver_row(item, rules):
    """Same group and note for every driver industry or activity. No model call."""
    if item_task(item) != "place" or not is_driver(item.get("name"), rules):
        return None
    note = rules.get("driver_note") or "A driver is folded into pressures."
    return {
        "task": "place",
        "status": "placed",
        "dpsir": "driver",
        "node_id": item.get("node_id"),
        "name": item.get("name"),
        "cell": "EV.O.A1",
        "group_id": driver_group(item),
        "note": note,
        "reason": "a driver is folded into pressures",
    }


def _schema_body(schema, name, system, payload):
    return {
        "model": MODEL,
        "think": False,
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": name, "strict": True, "schema": schema},
        },
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False, separators=(",", ":"))},
        ],
    }


def request_batch(items):
    """One batch, thinking off. Place and summary batches use a fixed system prefix."""
    if not items:
        raise ValueError("empty batch")
    if item_task(items[0]) == "summarise":
        payload = {
            "items": [
                {
                    "id": item_ref(item),
                    "children": _short_lines(item.get("children") or []),
                }
                for item in items
            ]
        }
        return _schema_body(SUMMARY_SCHEMA, "summaries", SYSTEM_SUMMARY, payload)
    groups = {}
    packed = []
    for item in items:
        choices = [row["group_id"] for row in likely_groups(item)] or ["unsure"]
        for row in likely_groups(item):
            groups.setdefault(row["group_id"], row["statement"])
        packed.append({"id": item_ref(item), "name": item.get("name") or "", "choices": choices})
    return _schema_body(PLACE_SCHEMA, "placements", SYSTEM_PLACE, {"groups": groups, "items": packed})


def request_body(item):
    """One item, as a batch of one. Kept for callers that still pass a single concept."""
    return request_batch([item])


def _short_lines(lines, limit=8):
    out = []
    for line in lines[:limit]:
        text = " ".join(str(line).split())
        if len(text) > 80:
            text = text[:77] + "..."
        out.append(text)
    return out


def parse_model_json(content):
    text = (content or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    if not text:
        return None
    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        items = data.get("items")
        if isinstance(items, list):
            return items
    return None


def _base_row(item, reason):
    row = {
        "task": item_task(item),
        "node_id": item.get("node_id"),
        "name": item.get("name"),
        "cell": item.get("cell"),
        "reason": reason or "",
    }
    if row["task"] == "summarise":
        row["needs_summary"] = True
        row["point_id"] = item.get("point_id")
    return row


def row_from_model(item, raw):
    row = _base_row(item, raw.get("reason"))
    if item_task(item) == "summarise":
        summary = str(raw.get("summary") or "").strip()
        row["summary"] = summary
        row["status"] = "placed" if summary else "needs_review"
        return row
    group_id = str(raw.get("group_id") or "").strip()
    offered = {cand["group_id"] for cand in likely_groups(item)}
    if not group_id or group_id == "unsure":
        row["group_id"] = "unsure"
        row["status"] = "unsure"
    elif group_id in offered:
        row["group_id"] = group_id
        row["status"] = "placed"
    else:
        row["group_id"] = group_id
        row["status"] = "needs_review"
    return row


def unsure_row(item, reason="the model reply was not usable"):
    row = _base_row(item, reason)
    row["status"] = "unsure"
    if item_task(item) == "summarise":
        row["summary"] = ""
    else:
        row["group_id"] = "unsure"
    return row


def resolve_batch(items, post, allow_retry=True):
    """Call the model. On a bad reply, retry, then split, then mark the item unsure."""
    if not items:
        return []
    try:
        reply = post(request_batch(items))
        content = ((reply.get("choices") or [{}])[0].get("message") or {}).get("content")
        parsed = parse_model_json(content)
        if not isinstance(parsed, list):
            raise ValueError("missing items")
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, urllib.error.URLError, TimeoutError, OSError):
        if allow_retry:
            return resolve_batch(items, post, allow_retry=False)
        if len(items) > 1:
            mid = len(items) // 2
            return resolve_batch(items[:mid], post, True) + resolve_batch(items[mid:], post, True)
        return [unsure_row(items[0])]
    by_id = {}
    for raw in parsed:
        if isinstance(raw, dict) and raw.get("id"):
            by_id[str(raw["id"])] = raw
    good = []
    missing = []
    for item in items:
        raw = by_id.get(item_ref(item))
        if raw is None:
            missing.append(item)
        else:
            good.append(row_from_model(item, raw))
    if len(missing) == len(items):
        if allow_retry:
            return resolve_batch(items, post, allow_retry=False)
        if len(items) > 1:
            mid = len(items) // 2
            return resolve_batch(items[:mid], post, True) + resolve_batch(items[mid:], post, True)
        return [unsure_row(items[0])]
    if missing:
        good.extend(resolve_batch(missing, post, True))
    return good


def load_previous(json_path, jsonl_path):
    rows = []
    if json_path.exists():
        previous = json.loads(json_path.read_text(encoding="utf-8"))
        rows.extend(previous.get("items") or [])
    if jsonl_path.exists():
        for line in jsonl_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def chunks(items, size):
    size = max(1, size)
    for start in range(0, len(items), size):
        yield items[start:start + size]


def clamp_batch(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = BATCH_SIZE
    return min(25, max(15, number))


def clamp_workers(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = DEFAULT_WORKERS
    return min(4, max(1, number))


def _fmt_span(seconds):
    seconds = max(0, int(seconds))
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}h{minutes:02d}m"
    if minutes:
        return f"{minutes}m{secs:02d}s"
    return f"{secs}s"


def _post(url, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Place a pyramid queue with the local model.")
    parser.add_argument("--field", required=True)
    parser.add_argument("--batch", type=int, default=BATCH_SIZE, help="Items per call (15–25, default 20).")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Concurrent calls (2–4, default 3).")
    parser.add_argument("--limit", type=int, default=0, help="Stop after this many pending items. 0 means all.")
    parser.add_argument("--dry-run", action="store_true", help="Print the first batch and do not call the model.")
    parser.add_argument("--progress", type=int, default=PROGRESS_EVERY, help="Print a progress line every N items.")
    return parser.parse_args(argv)


def run(args, post=None, root=None):
    field = args.field
    root = Path(root) if root else ROOT
    batch_size = clamp_batch(args.batch)
    workers = clamp_workers(args.workers)
    src = root / "pyramids" / "queues" / f"{field}.json"
    dest_json = root / "pyramids" / "queues" / f"{field}.placed.json"
    dest_jsonl = root / "pyramids" / "queues" / f"{field}.placed.jsonl"
    data = json.loads(src.read_text(encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) else data
    rules = load_rules(field, root)
    saved = load_previous(dest_json, dest_jsonl)
    pending = [item for item in items if not any(result_matches(item, row) for row in saved)]
    if args.limit and args.limit > 0:
        pending = pending[:args.limit]
    if args.dry_run:
        model_preview = []
        drivers = 0
        for item in pending:
            if driver_row(item, rules):
                drivers += 1
            elif item_task(item) == "place" and not likely_groups(item):
                continue
            else:
                model_preview.append(item)
        print(
            f"dry-run field={field} pending={len(pending)} drivers={drivers} "
            f"model={len(model_preview)} batch={batch_size} workers={workers} "
            f"(set OLLAMA_NUM_PARALLEL={workers} before ollama serve)"
        )
        if model_preview:
            sample = list(chunks(model_preview, batch_size))[0]
            body = request_batch(sample)
            print(f"system prefix cached ({len(body['messages'][0]['content'])} chars)")
            print(json.dumps(body, ensure_ascii=False))
        return {
            "pending": len(pending),
            "batch": batch_size,
            "workers": workers,
            "drivers": drivers,
            "wrote": 0,
        }

    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    url = host + "/v1/chat/completions"

    def send(body):
        if post:
            return post(body)
        return _post(url, body)

    dest_jsonl.parent.mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()
    counts = {"done": 0, "placed": 0, "unsure": 0, "needs_review": 0, "since": 0}
    started = time.monotonic()
    progress_every = max(1, int(args.progress or PROGRESS_EVERY))
    total = len(pending)

    def progress_line():
        elapsed = time.monotonic() - started
        rate = counts["done"] / elapsed if elapsed else 0
        remaining = total - counts["done"]
        eta = remaining / rate if rate else 0
        print(
            f"progress {counts['done']}/{total} placed {counts['placed']} "
            f"unsure {counts['unsure']} needs_review {counts['needs_review']} "
            f"elapsed {_fmt_span(elapsed)} eta {_fmt_span(eta)}",
            flush=True,
        )

    def record(rows):
        if not rows:
            return
        line = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
        with lock:
            with dest_jsonl.open("a", encoding="utf-8") as handle:
                handle.write(line)
                handle.flush()
            for row in rows:
                counts["done"] += 1
                status = row.get("status") or "unsure"
                if status not in counts:
                    status = "unsure"
                counts[status] += 1
                counts["since"] += 1
            if counts["since"] >= progress_every:
                counts["since"] = 0
                progress_line()

    print(
        f"field={field} pending={total} batch={batch_size} workers={workers} "
        f"(set OLLAMA_NUM_PARALLEL={workers} before ollama serve)",
        flush=True,
    )
    local = []
    model_items = []
    for item in pending:
        decided = driver_row(item, rules)
        if decided:
            local.append(decided)
        elif not likely_groups(item) and item_task(item) == "place":
            local.append(unsure_row(item, "no candidate group"))
        else:
            model_items.append(item)
    record(local)
    batches = list(chunks(model_items, batch_size))
    if batches:
        with ThreadPoolExecutor(max_workers=min(workers, len(batches))) as pool:
            future_batch = {pool.submit(resolve_batch, batch, send): batch for batch in batches}
            for future in as_completed(future_batch):
                batch = future_batch[future]
                try:
                    record(future.result())
                except AssertionError:
                    raise
                except Exception:
                    record([unsure_row(item) for item in batch])
    if counts["done"] and counts["since"]:
        progress_line()
    print(f"wrote {counts['done']} items to {dest_jsonl}", flush=True)
    return {"pending": total, "batch": batch_size, "workers": workers, "wrote": counts["done"]}


def main(argv=None):
    args = parse_args(argv)
    run(args)


if __name__ == "__main__":
    main()
