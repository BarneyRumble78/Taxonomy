#!/usr/bin/env python3
"""Place queued pyramid nodes with the local model.

    python3 scripts/run_pyramid_queue.py --field EV

Reads pyramids/queues/<FIELD>.json. Appends pyramids/queues/<FIELD>.placed.jsonl.
A run can be stopped and started again. Existing pyramids/queues/<FIELD>.placed.json
is read for resume and is not rewritten. Does not edit pyramids/<FIELD>.json.

Each call sends 20 items (15–25) and asks for a JSON array. Three workers run
at once. Before starting Ollama, set the server parallelism to the same number:

    OLLAMA_NUM_PARALLEL=3 ollama serve

The default backend is Ollama's native API: POST http://localhost:11434/api/chat
with think false, stream false, and format set to the JSON schema. The OpenAI-
compatible /v1/chat/completions path ignores think false under a strict schema,
so qwen3 keeps thinking until the timeout. Use it only with --api openai.
The system prefix is the same on every place call so the server can cache it.

Anthropic is optional. The default model is claude-sonnet-5-5, the current
Sonnet. claude-sonnet-4-5 is accepted. The call uses a tool for the batch
array, caches the system prefix, and stops before a call that would pass
--max-cost (default $10). It reads ANTHROPIC_API_KEY and does not run unless
that key is set.

    python3 scripts/run_pyramid_queue.py --field EV --limit 20 --dry-run
    python3 scripts/run_pyramid_queue.py --field EV --batch 20 --workers 3
    python3 scripts/run_pyramid_queue.py --field EV --api openai
    python3 scripts/run_pyramid_queue.py --field EV --backend anthropic --max-cost 10
    python3 scripts/run_pyramid_queue.py --field EV --backend anthropic --max-cost 10 \\
        --only-status out_of_scope,needs_review,unsure
"""
import argparse
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = "qwen3:30b-a3b"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-5-5"
BATCH_SIZE = 20
DEFAULT_WORKERS = 3
PROGRESS_EVERY = 20
DEFAULT_MAX_COST = 10.0
ANTHROPIC_MAX_TOKENS = 3000
# List prices, USD per million tokens, Claude API global tier.
# Input, output, 5-minute cache write, cache read.
# https://platform.claude.com/docs/en/about-claude/pricing checked 11 Oct 2026.
ANTHROPIC_RATES = (
    ("sonnet-4-5", 3.00, 15.00, 3.75, 0.30),
    ("sonnet-4.5", 3.00, 15.00, 3.75, 0.30),
    ("sonnet-4-6", 3.00, 15.00, 3.75, 0.30),
    ("sonnet-4.6", 3.00, 15.00, 3.75, 0.30),
    ("sonnet-5-5", 2.00, 10.00, 2.50, 0.10),
    ("sonnet-5.5", 2.00, 10.00, 2.50, 0.10),
    ("sonnet-5", 2.00, 10.00, 2.50, 0.20),
    ("sonnet", 3.00, 15.00, 3.75, 0.30),
)
# Fitted to the EV Sonnet run of 12 Oct 2026 (83f86ef): $4.50 for about 5,060 items,
# which is $0.90 per 1,000. A character count of the prompt had put the bill at $0.37.
# These counts reproduce $0.90 at claude-sonnet-5-5 list prices ($2 and $10 per million).
MEASURED_BATCH_ITEMS = 20
MEASURED_BATCH_INPUT_TOKENS = 3000
MEASURED_BATCH_OUTPUT_TOKENS = 1200

SYSTEM_PLACE = (
    "DPSIR. Driver: an industry or activity that creates a load; fold it into pressures. "
    "Pressure: a load from human activity. "
    "State: a measured condition. "
    "Impact: a harm, or the attribution of that harm. "
    "Natural hazards and processes belong under State, in the natural-hazards group. "
    "Earthquake, volcanic eruption, seismic activity, and landslide are geological hazards. "
    "Floods, storms, droughts, heat waves, and natural disasters are hydro-meteorological hazards. "
    "Biogeochemical and ecological processes are natural processes, not impacts. "
    "Environmental concepts, natural resources, and earth-system sciences are states. "
    "Response: an action that changes a pressure or a state. "
    "Measurement, monitoring, and assessment are environmental methods. "
    "Environmental engineering is a technical response. "
    "Limit: a threshold a state is not meant to cross. "
    "Place each item on one group_id from its choices. "
    "out_of_scope covers a concept that is clearly not environmental, including a GIS or data-model term such as raster. "
    "If none of the groups is the right home, choose unsure. Do not force a fit."
)
ESCAPE = ("unsure", "out_of_scope")
SYSTEM_SUMMARY = (
    "Write one sentence that states the insight these ideas share. "
    "Name the shared feature. Do not open with 'Both are' or 'All are'. "
    "Do not only list the members. "
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


def result_matches(item, row, catalog=None):
    """True when a saved row still answers this item.

    A place row from an older queue counts when its group_id is still offered:
    a candidate, any DPSIR cell, unsure, or out_of_scope. A driver row always
    counts for that node. An empty reply is not final, so it is asked again.
    A summary is a different task.
    """
    if item_task(row) != item_task(item):
        return False
    if item_task(item) == "summarise":
        if not item.get("point_id") or row.get("point_id") != item.get("point_id"):
            return False
        if row.get("status") in (None, "", "placed"):
            return True
        return False
    if row.get("node_id") != item.get("node_id"):
        return False
    if row.get("dpsir") == "driver":
        return True
    if row.get("reason") == "the model reply was not usable":
        return False
    home = named_home(item.get("name"))
    if home and row.get("group_id") != home["group_id"]:
        return False
    if (is_technical_term(item.get("name")) or is_scoped_name(item.get("name"))) and row.get("group_id") != "out_of_scope" and row.get("status") != "out_of_scope":
        return False
    chosen = row.get("group_id")
    if chosen in ESCAPE or row.get("status") in ESCAPE:
        return True
    offered = {cand.get("group_id") for cand in (item.get("candidates") or []) if cand.get("group_id")}
    offered.update(group.get("group_id") for group in (catalog or []) if group.get("group_id"))
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


_CATALOG_CACHE = {}


def _short_statement(statement):
    text = " ".join(str(statement or "").split())
    if len(text) > 80:
        text = text[:77] + "..."
    return text


def _point_cell(point, parent_cell=None):
    cell = point.get("cell") or parent_cell
    anchor = str(point.get("anchor") or "")
    if not cell and anchor.startswith("cell:"):
        cell = anchor.split(":", 1)[1]
    if not cell and anchor.startswith("facet:"):
        parts = anchor.split(":")
        if len(parts) >= 2:
            cell = parts[1]
    return cell


def cell_catalog(field="EV", root=None):
    """Each DPSIR cell, then the top group under it. Every item is offered this whole set."""
    root = Path(root) if root else ROOT
    key = (field, str(root))
    if key in _CATALOG_CACHE:
        return _CATALOG_CACHE[key]
    groups = []
    pyramid = root / "pyramids" / f"{field}.json"
    if not pyramid.exists():
        pyramid = ROOT / "pyramids" / f"{field}.json"
    if pyramid.exists():
        data = json.loads(pyramid.read_text(encoding="utf-8"))
        for point in (data.get("key_line") or {}).get("points") or []:
            cell = _point_cell(point)
            if point.get("id"):
                groups.append({
                    "group_id": point["id"],
                    "cell": cell,
                    "statement": point.get("statement") or "",
                })
            for child in (point.get("support") or {}).get("points") or []:
                child_cell = _point_cell(child, cell)
                if child.get("id"):
                    groups.append({
                        "group_id": child["id"],
                        "cell": child_cell,
                        "statement": child.get("statement") or "",
                    })
                for grandchild in (child.get("support") or {}).get("points") or []:
                    if str(grandchild.get("anchor") or "").startswith("facet:") and grandchild.get("id"):
                        groups.append({
                            "group_id": grandchild["id"],
                            "cell": _point_cell(grandchild, child_cell),
                            "statement": grandchild.get("statement") or "",
                        })
    if not groups:
        rules = load_rules(field, root)
        for index, cell in enumerate(rules.get("cells") or [], start=1):
            parent = f"{field}.P.{index}"
            groups.append({
                "group_id": parent,
                "cell": cell.get("cell"),
                "statement": cell.get("statement") or "",
            })
            for facet_index, facet in enumerate(cell.get("facets") or [], start=1):
                groups.append({
                    "group_id": f"{parent}.{facet_index}",
                    "cell": cell.get("cell"),
                    "statement": facet.get("statement") or "",
                })
    _CATALOG_CACHE[key] = groups
    return groups


def cell_for_group(group_id, catalog=None, item=None):
    """The cell that owns this group. A facet inherits the cell of its parent."""
    by_id = {}
    for row in catalog or []:
        if row.get("group_id"):
            by_id[row["group_id"]] = row.get("cell")
    if by_id.get(group_id):
        return by_id[group_id]
    best = None
    for gid, cell in by_id.items():
        if cell and group_id.startswith(gid + ".") and (best is None or len(gid) > len(best[0])):
            best = (gid, cell)
    if best:
        return best[1]
    for cand in (item or {}).get("candidates") or []:
        if cand.get("group_id") == group_id and cand.get("cell"):
            return cand["cell"]
    return None


def choice_groups(item, catalog=None):
    """Top groups from every DPSIR cell, then this item's own groups."""
    groups = []
    seen = set()

    def add(group_id, statement):
        if not group_id or group_id in seen or group_id in ESCAPE:
            return
        seen.add(group_id)
        groups.append({"group_id": group_id, "statement": _short_statement(statement)})

    for row in catalog or []:
        add(row.get("group_id"), row.get("statement"))
    for cand in item.get("candidates") or []:
        add(cand.get("group_id"), cand.get("statement") or cand.get("facet"))
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


def hazard_group(name, rules=None):
    """The State subgroup for a named natural hazard or process."""
    key = (name or "").strip().lower()
    if not key:
        return None
    if rules is None:
        rules = load_rules("EV")
    for group in (rules.get("natural_hazards") or {}).get("groups") or []:
        names = {str(item).strip().lower() for item in (group.get("names") or [])}
        if key in names:
            return group
    return None


def natural_row(item, rules):
    """Place a named hazard on its State subgroup. No model call."""
    if item_task(item) != "place":
        return None
    group = hazard_group(item.get("name"), rules)
    if not group:
        return None
    return {
        "task": "place",
        "status": "placed",
        "dpsir": "natural",
        "node_id": item.get("node_id"),
        "name": item.get("name"),
        "cell": group.get("cell") or "EV.O.A2",
        "group_id": group["group_id"],
        "reason": "a natural hazard or process belongs under State",
    }


def is_technical_term(name, rules=None):
    """A GIS or data-model word, such as raster. Not an environmental concept."""
    if rules is None:
        rules = load_rules("EV")
    terms = [str(term) for term in (rules.get("out_of_scope_terms") or [])]
    if not terms:
        terms = ["raster", "gis"]
    pattern = re.compile(r"\b(" + "|".join(re.escape(term) for term in terms) + r")\b", re.I)
    return bool(pattern.search(name or ""))


def technical_row(item, rules):
    """Mark a GIS or data-model term out of scope. No model call."""
    if item_task(item) != "place" or not is_technical_term(item.get("name"), rules):
        return None
    return {
        "task": "place",
        "status": "out_of_scope",
        "node_id": item.get("node_id"),
        "name": item.get("name"),
        "cell": item.get("cell"),
        "group_id": "out_of_scope",
        "reason": "a GIS or data-model term is not an environmental concept",
    }


def named_home(name, rules=None):
    """The group an exact name belongs to, hazards first."""
    return hazard_group(name, rules) or ruled_group(name, rules)


def ruled_group(name, rules=None):
    """A methods, engineering, concept, resource, or earth-science group."""
    key = (name or "").strip().lower()
    if not key:
        return None
    if rules is None:
        rules = load_rules("EV")
    for group in rules.get("ruled_groups") or []:
        names = {str(item).strip().lower() for item in (group.get("names") or [])}
        if key in names:
            return group
    return None


def grouped_row(item, rules):
    """Place a named method, concept, resource, or science. No model call."""
    if item_task(item) != "place":
        return None
    group = ruled_group(item.get("name"), rules)
    if not group:
        return None
    return {
        "task": "place",
        "status": "placed",
        "node_id": item.get("node_id"),
        "name": item.get("name"),
        "cell": group.get("cell") or "",
        "group_id": group["group_id"],
        "reason": group.get("reason") or "the name belongs to this group",
    }


def is_scoped_name(name, rules=None):
    """An exact name that is not an environmental concept."""
    key = (name or "").strip().lower()
    if not key:
        return False
    if rules is None:
        rules = load_rules("EV")
    names = {str(item).strip().lower() for item in (rules.get("out_of_scope_names") or [])}
    return key in names


def scoped_row(item, rules):
    """Mark a chemical, place, organism, or economic term out of scope. No model call."""
    if item_task(item) != "place" or not is_scoped_name(item.get("name"), rules):
        return None
    return {
        "task": "place",
        "status": "out_of_scope",
        "node_id": item.get("node_id"),
        "name": item.get("name"),
        "cell": item.get("cell"),
        "group_id": "out_of_scope",
        "reason": "a chemical, place, organism, or economic term is not an environmental concept",
    }


def ruled_row(item, rules):
    """A row the rules can finish without a model call."""
    return driver_row(item, rules) or natural_row(item, rules) or grouped_row(item, rules) or scoped_row(item, rules) or technical_row(item, rules)


def _schema_body(schema, name, system, payload, api="native"):
    """Native /api/chat by default. OpenAI /v1/chat/completions is optional.

    Ollama's OpenAI route ignores think:false when response_format is a strict
    schema, so the model thinks until the timeout and content comes back empty.
    """
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False, separators=(",", ":"))},
    ]
    if api == "openai":
        return {
            "model": MODEL,
            "think": False,
            "temperature": 0,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": name, "strict": True, "schema": schema},
            },
            "messages": messages,
        }
    return {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "think": False,
        "format": schema,
        "options": {"temperature": 0, "num_predict": 3000},
    }


def _field_of(items):
    cell = (items[0].get("cell") or "") if items else ""
    if cell and "." in cell:
        return cell.split(".")[0]
    return "EV"


def request_batch(items, api="native", catalog=None):
    """One batch, thinking off. Place and summary batches use a fixed system prefix."""
    if not items:
        raise ValueError("empty batch")
    if catalog is None and item_task(items[0]) != "summarise":
        catalog = cell_catalog(_field_of(items))
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
        return _schema_body(SUMMARY_SCHEMA, "summaries", SYSTEM_SUMMARY, payload, api)
    groups = {}
    packed = []
    for item in items:
        rows = choice_groups(item, catalog)
        choices = [row["group_id"] for row in rows] + list(ESCAPE)
        for row in rows:
            groups.setdefault(row["group_id"], row["statement"])
        packed.append({"id": item_ref(item), "name": item.get("name") or "", "choices": choices})
    return _schema_body(PLACE_SCHEMA, "placements", SYSTEM_PLACE, {"groups": groups, "items": packed}, api)


def request_body(item, api="native", catalog=None):
    """One item, as a batch of one. Kept for callers that still pass a single concept."""
    return request_batch([item], api=api, catalog=catalog)


def chat_url(host, api="native"):
    host = (host or "http://localhost:11434").rstrip("/")
    if api == "openai":
        return host + "/v1/chat/completions"
    return host + "/api/chat"


def message_content(reply):
    """Native /api/chat uses message.content. The OpenAI route uses choices."""
    if not isinstance(reply, dict):
        return ""
    message = reply.get("message")
    if isinstance(message, dict) and "content" in message:
        return message.get("content") or ""
    choices = reply.get("choices") or []
    if choices and isinstance(choices[0], dict):
        return ((choices[0].get("message") or {}).get("content")) or ""
    return ""


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


def offered_ids(item, catalog=None):
    return {row["group_id"] for row in choice_groups(item, catalog)} | set(ESCAPE)


def summary_is_weak(text):
    """A summary that only says the members are the same kind of thing."""
    low = (text or "").lstrip().lower()
    return low.startswith("both are") or low.startswith("all are")


def row_from_model(item, raw, catalog=None):
    row = _base_row(item, raw.get("reason"))
    if item_task(item) == "summarise":
        summary = str(raw.get("summary") or "").strip()
        row["summary"] = summary
        if not summary or summary_is_weak(summary):
            row["status"] = "needs_review"
        else:
            row["status"] = "placed"
        return row
    group_id = str(raw.get("group_id") or "").strip()
    offered = offered_ids(item, catalog)
    if group_id == "out_of_scope":
        row["group_id"] = "out_of_scope"
        row["status"] = "out_of_scope"
    elif not group_id or group_id == "unsure":
        row["group_id"] = "unsure"
        row["status"] = "unsure"
    elif group_id in offered:
        row["group_id"] = group_id
        row["status"] = "placed"
        cell = cell_for_group(group_id, catalog, item)
        if cell:
            row["cell"] = cell
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


def resolve_batch(items, post, allow_retry=True, api="native", catalog=None):
    """Call the model. On a bad reply, retry, then split, then mark the item unsure."""
    if not items:
        return []
    try:
        reply = post(request_batch(items, api=api, catalog=catalog))
        parsed = parse_model_json(message_content(reply))
        if not isinstance(parsed, list):
            raise ValueError("missing items")
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, urllib.error.URLError, TimeoutError, OSError):
        if allow_retry:
            return resolve_batch(items, post, allow_retry=False, api=api, catalog=catalog)
        if len(items) > 1:
            mid = len(items) // 2
            return (
                resolve_batch(items[:mid], post, True, api, catalog)
                + resolve_batch(items[mid:], post, True, api, catalog)
            )
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
            good.append(row_from_model(item, raw, catalog))
    if len(missing) == len(items):
        if allow_retry:
            return resolve_batch(items, post, allow_retry=False, api=api, catalog=catalog)
        if len(items) > 1:
            mid = len(items) // 2
            return (
                resolve_batch(items[:mid], post, True, api, catalog)
                + resolve_batch(items[mid:], post, True, api, catalog)
            )
        return [unsure_row(items[0])]
    if missing:
        good.extend(resolve_batch(missing, post, True, api, catalog))
    return good


def row_key(row):
    """One saved answer per placed node, and one per summary point."""
    if item_task(row) == "summarise":
        return ("summarise", str(row.get("point_id") or ""))
    return ("place", str(row.get("node_id") or ""))


def row_status(row):
    """The status written on the row. A placed summary stays placed."""
    return row.get("status") or ""


def dedupe_rows(rows):
    """Last row for each item wins. Earlier copies of the same node are dropped."""
    order = []
    latest = {}
    for row in rows:
        key = row_key(row)
        if key not in latest:
            order.append(key)
        latest[key] = row
    return [latest[key] for key in order]


def read_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def compact_jsonl(path):
    """Rewrite the JSONL so each item appears once. Returns how many copies were dropped."""
    rows = read_jsonl(path)
    kept = dedupe_rows(rows)
    if len(kept) == len(rows):
        return 0
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in kept),
        encoding="utf-8",
    )
    return len(rows) - len(kept)


def load_previous(json_path, jsonl_path):
    rows = []
    if json_path.exists():
        previous = json.loads(json_path.read_text(encoding="utf-8"))
        rows.extend(previous.get("items") or [])
    rows.extend(read_jsonl(jsonl_path))
    return dedupe_rows(rows)


def parse_only_status(value):
    if not value:
        return ()
    return tuple(part.strip() for part in str(value).split(",") if part.strip())


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
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def price_rates(model):
    """Input, output, 5-minute cache write, cache read. Unknown models use the $3/$15 Sonnet rate."""
    name = (model or "").lower()
    for key, inp, out, write, read in ANTHROPIC_RATES:
        if key in name:
            return (inp, out, write, read)
    return (3.00, 15.00, 3.75, 0.30)


def list_usd(model, input_tokens=0, output_tokens=0, cache_read=0, cache_write=0):
    """List-price dollars for one set of token counts. Cache tokens are not also counted as input."""
    inp, out, write, read = price_rates(model)
    return (
        int(input_tokens) * inp
        + int(output_tokens) * out
        + int(cache_write) * write
        + int(cache_read) * read
    ) / 1_000_000


def expected_usd_per_thousand(model=None):
    """List price for 1,000 items, fitted to the EV Sonnet run at $0.90 per 1,000."""
    model = model or DEFAULT_ANTHROPIC_MODEL
    calls = 1000 / MEASURED_BATCH_ITEMS
    return list_usd(
        model,
        input_tokens=round(calls * MEASURED_BATCH_INPUT_TOKENS),
        output_tokens=round(calls * MEASURED_BATCH_OUTPUT_TOKENS),
    )


def output_cap_usd_per_thousand(model=None, max_tokens=ANTHROPIC_MAX_TOKENS):
    """List price for 1,000 items if every call uses the full output cap."""
    model = model or DEFAULT_ANTHROPIC_MODEL
    calls = 1000 / MEASURED_BATCH_ITEMS
    return list_usd(
        model,
        input_tokens=round(calls * MEASURED_BATCH_INPUT_TOKENS),
        output_tokens=round(calls * max_tokens),
    )


def anthropic_controls(model):
    """Sonnet 5.5 rejects forced tools, temperature, and thinking disabled.

    between_tools is its lowest thinking setting, so the call does not open
    on a trace. Effort stays at high, the API default for this model.
    Sonnet 4.5 still accepts a named tool.
    """
    name = (model or "").lower()
    if "sonnet" in name and ("5-5" in name or "5.5" in name):
        return {
            "thinking": {"type": "between_tools"},
            "effort": "high",
            "tool_choice": {"type": "auto"},
            "strict": True,
        }
    if "sonnet-5" in name or name.endswith("sonnet-5"):
        return {
            "thinking": {"type": "disabled"},
            "tool_choice": {"type": "auto"},
            "strict": False,
        }
    return {
        "tool_choice": {"type": "tool", "name": "record_placements"},
        "strict": False,
    }


def stable_prefix(catalog, items):
    """The place instructions and every group this run can offer. Same text on every call."""
    found = {}
    for row in catalog or []:
        group_id = row.get("group_id")
        if group_id and group_id not in ESCAPE:
            found.setdefault(group_id, " ".join(str(row.get("statement") or "").split()))
    for item in items or []:
        for cand in item.get("candidates") or []:
            group_id = cand.get("group_id")
            if group_id and group_id not in ESCAPE:
                found.setdefault(group_id, " ".join(str(cand.get("statement") or cand.get("facet") or "").split()))
    lines = [SYSTEM_PLACE, "", "Groups."]
    for group_id in sorted(found):
        lines.append(f"{group_id}: {found[group_id]}")
    lines.extend(["", "Call the tool once. Put every item in its items array."])
    return "\n".join(lines)


def _schema_of(body):
    schema = body.get("format")
    if schema is None:
        schema = body["response_format"]["json_schema"]["schema"]
    return schema


def _is_summary_schema(schema):
    item = schema["properties"]["items"]["items"]
    return "summary" in item.get("properties", {})


def to_anthropic(body, model, system_prefix):
    """Messages API body. The system prefix and the tool carry a cache breakpoint."""
    schema = _schema_of(body)
    summary = _is_summary_schema(schema)
    tool = "record_summaries" if summary else "record_placements"
    controls = anthropic_controls(model)
    if summary:
        system_text = SYSTEM_SUMMARY + "\nCall the tool once. Put every item in its items array."
    else:
        system_text = system_prefix
    choice = dict(controls["tool_choice"])
    if choice.get("type") == "tool":
        choice["name"] = tool
    tool_def = {
        "name": tool,
        "description": "Record one result for every item in the user message.",
        "input_schema": schema,
        "cache_control": {"type": "ephemeral"},
    }
    if controls["strict"]:
        tool_def["strict"] = True
    payload = {
        "model": model,
        "max_tokens": ANTHROPIC_MAX_TOKENS,
        "system": [{"type": "text", "text": system_text, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": body["messages"][1]["content"]}],
        "tools": [tool_def],
        "tool_choice": choice,
    }
    if controls.get("thinking"):
        payload["thinking"] = controls["thinking"]
    if controls.get("effort"):
        payload["output_config"] = {"effort": controls["effort"]}
    return payload


def anthropic_content(data):
    """Prefer the tool input. A JSON object in the text is accepted too."""
    if not isinstance(data, dict):
        return ""
    text = ""
    for block in data.get("content") or []:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "tool_use" and block.get("name") in ("record_placements", "record_summaries"):
            return json.dumps(block.get("input") or {})
        if block.get("type") == "text" and not text:
            text = block.get("text") or ""
    return text


def _post_anthropic(body, key):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "content-type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


class CostCap(Exception):
    """The next call would pass --max-cost. Items not sent stay pending."""

    def __init__(self, usd, limit):
        self.usd = usd
        self.limit = limit
        super().__init__(f"stopped at ${usd:.4f}, max-cost ${limit:.2f}")


class CostTracker:
    """Token counts and list-price dollars. A call reserves its worst case before it starts."""

    def __init__(self, model, max_cost):
        self.model = model
        self.max_cost = max_cost if max_cost and max_cost > 0 else 0.0
        self.input_tokens = 0
        self.output_tokens = 0
        self.cache_read = 0
        self.cache_write = 0
        self.reserved = 0.0
        self.stopped = False
        self._lock = threading.Lock()

    def usd(self):
        with self._lock:
            return self._usd()

    def _usd(self):
        return list_usd(
            self.model,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            cache_read=self.cache_read,
            cache_write=self.cache_write,
        )

    def begin(self, reserve):
        with self._lock:
            if self.max_cost and self._usd() + self.reserved + reserve > self.max_cost:
                self.stopped = True
                return False
            self.reserved += reserve
            return True

    def finish(self, reserve, usage):
        usage = usage or {}
        with self._lock:
            self.reserved = max(0.0, self.reserved - reserve)
            self.input_tokens += int(usage.get("input_tokens") or 0)
            self.output_tokens += int(usage.get("output_tokens") or 0)
            self.cache_read += int(usage.get("cache_read_input_tokens") or 0)
            self.cache_write += int(usage.get("cache_creation_input_tokens") or 0)
            if self.max_cost and self._usd() >= self.max_cost:
                self.stopped = True

    def line(self):
        return (
            f"cost ${self.usd():.4f} in {self.input_tokens} out {self.output_tokens} "
            f"cache_read {self.cache_read} cache_write {self.cache_write}"
        )


def reserve_usd(model, body):
    """Worst-case list price of one call: the prompt at input rates, and max_tokens at output rates."""
    text = body["system"][0]["text"] + body["messages"][0]["content"]
    return list_usd(model, input_tokens=max(1, len(text) // 4), output_tokens=body["max_tokens"])


def anthropic_send(body, model, system_prefix, tracker, client, key):
    """One Messages API call. Returns the shape resolve_batch already reads."""
    payload = to_anthropic(body, model, system_prefix)
    reserve = reserve_usd(model, payload)
    if not tracker.begin(reserve):
        raise CostCap(tracker.usd(), tracker.max_cost)
    data = None
    try:
        if client:
            data = client(payload)
        else:
            data = _post_anthropic(payload, key)
        return {"message": {"content": anthropic_content(data)}}
    finally:
        usage = data.get("usage") if isinstance(data, dict) else None
        tracker.finish(reserve, usage)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Place a pyramid queue with the local model.")
    parser.add_argument("--field", required=True)
    parser.add_argument("--batch", type=int, default=BATCH_SIZE, help="Items per call (15–25, default 20).")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Concurrent calls (2–4, default 3).")
    parser.add_argument("--limit", type=int, default=0, help="Stop after this many pending items. 0 means all.")
    parser.add_argument("--dry-run", action="store_true", help="Print the first batch and do not call the model.")
    parser.add_argument("--progress", type=int, default=PROGRESS_EVERY, help="Print a progress line every N items.")
    parser.add_argument(
        "--api",
        choices=("native", "openai"),
        default=os.environ.get("TAXONOMY_QUEUE_API", "native"),
        help="Ollama only. native is /api/chat (default). openai is /v1/chat/completions.",
    )
    parser.add_argument(
        "--backend",
        choices=("ollama", "anthropic"),
        default="ollama",
        help="ollama is the default. anthropic calls the Messages API.",
    )
    parser.add_argument(
        "--model",
        default="",
        help="Ollama default is qwen3:30b-a3b. Anthropic default is claude-sonnet-5-5. claude-sonnet-4-5 is accepted.",
    )
    parser.add_argument(
        "--max-cost",
        type=float,
        default=DEFAULT_MAX_COST,
        help="Stop before a call that would pass this many USD. 0 means no cap. Default 10.",
    )
    parser.add_argument(
        "--only-status",
        default="",
        help="Ask again only for these statuses, comma-separated. Example: out_of_scope,needs_review,unsure.",
    )
    return parser.parse_args(argv)


def resolve_model(backend, model):
    if model:
        return model
    if backend == "anthropic":
        return DEFAULT_ANTHROPIC_MODEL
    return MODEL


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
    catalog = cell_catalog(field, root)
    api = getattr(args, "api", None) or "native"
    if api not in ("native", "openai"):
        api = "native"
    backend = getattr(args, "backend", None) or "ollama"
    if backend not in ("ollama", "anthropic"):
        backend = "ollama"
    model = resolve_model(backend, getattr(args, "model", "") or "")
    max_cost = getattr(args, "max_cost", DEFAULT_MAX_COST)
    try:
        max_cost = float(max_cost)
    except (TypeError, ValueError):
        max_cost = DEFAULT_MAX_COST
    if not args.dry_run:
        compact_jsonl(dest_jsonl)
    saved = load_previous(dest_json, dest_jsonl)
    only = parse_only_status(getattr(args, "only_status", ""))
    if only:
        latest = {row_key(row): row for row in saved}
        pending = [
            item for item in items
            if (latest.get(row_key(item)) is not None and row_status(latest[row_key(item)]) in only)
        ]
    else:
        pending = [item for item in items if not any(result_matches(item, row, catalog) for row in saved)]
    if args.limit and args.limit > 0:
        pending = pending[:args.limit]
    if args.dry_run:
        model_preview = []
        drivers = 0
        for item in pending:
            if ruled_row(item, rules):
                drivers += 1
            else:
                model_preview.append(item)
        only_bit = f" only-status={','.join(only)}" if only else ""
        if backend == "anthropic":
            per_thousand = expected_usd_per_thousand(model)
            print(
                f"dry-run field={field} pending={len(pending)} drivers={drivers} "
                f"model_items={len(model_preview)} batch={batch_size} workers={workers} "
                f"backend=anthropic model={model} max-cost={max_cost:.2f} "
                f"expected ${per_thousand:.2f} per 1000 items{only_bit}"
            )
        else:
            print(
                f"dry-run field={field} pending={len(pending)} drivers={drivers} "
                f"model={len(model_preview)} batch={batch_size} workers={workers} api={api} "
                f"endpoint={chat_url('http://localhost:11434', api)} "
                f"(set OLLAMA_NUM_PARALLEL={workers} before ollama serve){only_bit}"
            )
        if model_preview:
            sample = list(chunks(model_preview, batch_size))[0]
            body = request_batch(sample, api=api, catalog=catalog)
            if backend == "anthropic":
                body = to_anthropic(body, model, stable_prefix(catalog, model_preview))
                print(f"system prefix cached ({len(body['system'][0]['text'])} chars)")
            else:
                print(f"system prefix cached ({len(body['messages'][0]['content'])} chars)")
            print(json.dumps(body, ensure_ascii=False))
        return {
            "pending": len(pending),
            "batch": batch_size,
            "workers": workers,
            "drivers": drivers,
            "api": api,
            "backend": backend,
            "model": model,
            "wrote": 0,
            "stopped": False,
            "cost": 0.0,
        }

    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    url = chat_url(host, api)
    key = ""
    tracker = None
    prefix = ""
    if backend == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if post is None and not key:
            raise SystemExit("ANTHROPIC_API_KEY is not set")
        tracker = CostTracker(model, max_cost)

    def send(body):
        if backend == "anthropic":
            return anthropic_send(body, model, prefix, tracker, post, key)
        if post:
            return post(body)
        return _post(url, body)

    dest_jsonl.parent.mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()
    counts = {"done": 0, "placed": 0, "unsure": 0, "out_of_scope": 0, "needs_review": 0, "since": 0}
    started = time.monotonic()
    progress_every = max(1, int(args.progress or PROGRESS_EVERY))
    total = len(pending)

    def progress_line():
        elapsed = time.monotonic() - started
        rate = counts["done"] / elapsed if elapsed else 0
        remaining = total - counts["done"]
        eta = remaining / rate if rate else 0
        cost = f" {tracker.line()}" if tracker is not None else ""
        print(
            f"progress {counts['done']}/{total} placed {counts['placed']} "
            f"unsure {counts['unsure']} out_of_scope {counts['out_of_scope']} "
            f"needs_review {counts['needs_review']}{cost} "
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

    only_bit = f" only-status={','.join(only)}" if only else ""
    if backend == "anthropic":
        print(
            f"field={field} pending={total} batch={batch_size} workers={workers} "
            f"backend=anthropic model={model} max-cost={max_cost:.2f} "
            f"expected ${expected_usd_per_thousand(model):.2f} per 1000 items{only_bit}",
            flush=True,
        )
    else:
        print(
            f"field={field} pending={total} batch={batch_size} workers={workers} api={api} "
            f"endpoint={url} (set OLLAMA_NUM_PARALLEL={workers} before ollama serve){only_bit}",
            flush=True,
        )
    local = []
    model_items = []
    for item in pending:
        decided = ruled_row(item, rules)
        if decided:
            local.append(decided)
        else:
            model_items.append(item)
    if backend == "anthropic":
        prefix = stable_prefix(catalog, model_items)
    record(local)
    batches = list(chunks(model_items, batch_size))
    stopped = False
    if batches:
        with ThreadPoolExecutor(max_workers=min(workers, len(batches))) as pool:
            future_batch = {
                pool.submit(resolve_batch, batch, send, True, api, catalog): batch for batch in batches
            }
            for future in as_completed(future_batch):
                batch = future_batch[future]
                try:
                    record(future.result())
                except CostCap:
                    stopped = True
                except AssertionError:
                    raise
                except Exception:
                    record([unsure_row(item) for item in batch])
    if counts["done"] and counts["since"]:
        progress_line()
    compact_jsonl(dest_jsonl)
    print(f"wrote {counts['done']} items to {dest_jsonl}", flush=True)
    if tracker is not None:
        print(tracker.line(), flush=True)
        if stopped or tracker.stopped:
            stopped = True
            print(
                f"stopped at max-cost ${max_cost:.2f}; unsent items stay pending",
                flush=True,
            )
    return {
        "pending": total,
        "batch": batch_size,
        "workers": workers,
        "wrote": counts["done"],
        "backend": backend,
        "model": model,
        "stopped": stopped,
        "cost": tracker.usd() if tracker is not None else 0.0,
    }


def main(argv=None):
    args = parse_args(argv)
    run(args)


if __name__ == "__main__":
    main()
