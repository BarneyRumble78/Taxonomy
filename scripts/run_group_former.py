#!/usr/bin/env python3
"""Form Minto groups for one field. No call unless asked.

    python3 scripts/run_group_former.py --field MA --backend anthropic --max-cost 0.08 --global-max-cost 60
    python3 scripts/run_group_former.py --field AG --backend ollama --max-cost 0 --global-max-cost 60

Ollama uses native POST /api/chat with think false. Anthropic uses the
Messages API, a cached system prefix, and the shared cost ledger.
--max-cost 0 leaves the field cap off. A stopped cell is not written, so
the next run continues it.

Claude fields, on the machine that holds ANTHROPIC_API_KEY:

    python3 scripts/run_group_former.py --field MA --backend anthropic --max-cost 0.08 --global-max-cost 60
    python3 scripts/run_group_former.py --field PH --backend anthropic --max-cost 5.57 --global-max-cost 60
    python3 scripts/run_group_former.py --field CH --backend anthropic --max-cost 0.14 --global-max-cost 60
    python3 scripts/run_group_former.py --field CS --backend anthropic --max-cost 0.29 --global-max-cost 60
    python3 scripts/run_group_former.py --field MD --backend anthropic --max-cost 0.37 --global-max-cost 60

Or the five fields from the plan:

    python3 scripts/run_all_fields.py --execute --fields MA,PH,CH,CS,MD

Qwen fields, on the Mac, after Ollama is up:

    OLLAMA_NUM_PARALLEL=3 ollama serve
    python3 scripts/run_all_fields.py --execute --fields AG,AR,BI,BU,DE,EA,EC,ED,EN,HI,IK,IS,LA,LN,MS,PL,PO,RE,ST
"""
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine" / "v3"))
sys.path.insert(0, str(ROOT / "scripts"))

from cost_cap import load_ledger, record as record_spend, save_ledger  # noqa: E402
from group_former import (  # noqa: E402
    SCHEMA,
    SYSTEM,
    append_log,
    cell_jobs,
    finished_cells,
    form_cell,
    log_path,
    pending_work,
    read_log,
    write_result,
)
import run_pyramid_queue as queue  # noqa: E402


def parse_reply(content):
    text = (content or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    if not text:
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict) and (isinstance(data.get("groups"), list) or isinstance(data.get("statement"), str)):
        data.setdefault("groups", [])
        return data
    return None


def request_body(task, payload, model, api="native"):
    """Same native body as the queue runner. The system text does not change."""
    body = queue._schema_body(SCHEMA, "groups", SYSTEM, {"task": task, **payload}, api)
    body["model"] = model
    return body


def _post_ollama(url, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Form Minto groups for one field.")
    parser.add_argument("--field", required=True)
    parser.add_argument("--batch", type=int, default=20, help="Admitted nodes per call. Default 20.")
    parser.add_argument("--dry-run", action="store_true", help="Print the prefix and do not call a model.")
    parser.add_argument("--backend", choices=("ollama", "anthropic"), default="ollama")
    parser.add_argument("--api", choices=("native", "openai"), default=os.environ.get("TAXONOMY_QUEUE_API", "native"))
    parser.add_argument("--model", default="")
    parser.add_argument("--max-cost", type=float, default=0.0, help="Field cap in USD. 0 means no field cap.")
    parser.add_argument("--global-max-cost", type=float, default=queue.DEFAULT_GLOBAL_MAX_COST)
    parser.add_argument("--root", default="")
    return parser.parse_args(argv)


def run(args, post=None, anthropic_post=None, root=None):
    """One field. post and anthropic_post stand in for the network in tests."""
    field = args.field
    root = Path(root) if root else ROOT
    backend = args.backend if args.backend in ("ollama", "anthropic") else "ollama"
    model = queue.resolve_model(backend, args.model or "")
    api = args.api if args.api in ("native", "openai") else "native"
    jobs = cell_jobs(field, root)
    path = log_path(root, field)
    rows = read_log(path)
    done = finished_cells(rows)
    pending_jobs = [job for job in jobs if job["cell"] not in done]
    if args.dry_run:
        sample = None
        if pending_jobs and pending_jobs[0]["nodes"]:
            sample = request_body("form", {
                "cell": pending_jobs[0]["cell"],
                "principle": pending_jobs[0]["principle"],
                "nodes": [{"id": node["id"], "name": node["name"]} for node in pending_jobs[0]["nodes"][:2]],
                "min_groups": 1,
                "problems": [],
            }, model, api)
        print(
            f"dry-run field={field} cells={len(jobs)} pending={len(pending_jobs)} "
            f"backend={backend} model={model} max-cost={float(args.max_cost):.2f} "
            f"global-max-cost={float(args.global_max_cost):.2f}"
        )
        print(f"system prefix cached ({len(SYSTEM)} chars)")
        if sample and backend == "ollama":
            print(f"endpoint={queue.chat_url(os.environ.get('OLLAMA_HOST', 'http://localhost:11434'), api)}")
        return {
            "field": field,
            "pending": len(pending_jobs),
            "cells": len(jobs),
            "backend": backend,
            "model": model,
            "wrote": 0,
            "stopped": False,
            "cost": 0.0,
            "system": SYSTEM,
        }

    ledger = load_ledger(queue.ledger_file(root)) if backend == "anthropic" else None
    tracker = None
    key = ""
    if backend == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if anthropic_post is None and not key:
            raise SystemExit("ANTHROPIC_API_KEY is not set")
        tracker = queue.CostTracker(
            model,
            float(args.max_cost),
            float(args.global_max_cost),
            float((ledger.get("fields") or {}).get(field) or 0),
            float(ledger.get("spent") or 0),
        )
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    url = queue.chat_url(host, api)
    stopped = False
    wrote = 0

    saved = [0.0]

    def _save_spend():
        # Record spend after every call so a crash cannot lose it.
        if tracker is None or ledger is None:
            return
        delta = tracker.usd() - saved[0]
        if delta > 0:
            record_spend(ledger, field, delta)
            save_ledger(queue.ledger_file(root), ledger)
            saved[0] += delta

    def send(task, payload):
        body = request_body(task, payload, model, api)
        if backend == "anthropic":
            try:
                reply = queue.anthropic_send(body, model, SYSTEM, tracker, anthropic_post, key)
            finally:
                _save_spend()
        elif post is not None:
            reply = post(body)
        else:
            reply = _post_ollama(url, body)
        parsed = parse_reply(queue.message_content(reply))
        if not parsed:
            return {"statement": "", "basis": "", "order": "", "rank_note": "", "groups": []}
        return parsed

    for job in pending_jobs:
        fresh = read_log(path)
        pending, seed_groups, _exhausted = pending_work(fresh, job["cell"], job["nodes"])

        def on_batch(formed, job=job):
            append_log(path, {
                "field": field,
                "cell": job["cell"],
                "part": "batch",
                "status": formed.get("status"),
                "batch_key": ",".join(sorted(formed.get("member_ids") or [])),
                "member_ids": formed.get("member_ids") or [],
                "review_ids": formed.get("review_ids") or [],
                "groups": formed.get("groups") or [],
                "reason": formed.get("reason") or "",
            })

        def ask(task, payload, job=job):
            return send(task, {
                "cell": job["cell"],
                "principle": job["principle"],
                **payload,
            })

        try:
            outcome = form_cell(
                job["cell"],
                pending,
                ask,
                batch_size=args.batch,
                seed_groups=seed_groups,
                on_batch=on_batch,
                known=job["nodes"],
            )
        except queue.CostCap:
            stopped = True
            break
        line = {
            "field": field,
            "cell": job["cell"],
            "part": "cell",
            "status": outcome.get("status"),
            "reason": outcome.get("reason") or "",
            "member_ids": outcome.get("member_ids") or [],
        }
        if outcome.get("point"):
            line["point"] = outcome["point"]
        if outcome.get("review_ids"):
            line["review_ids"] = outcome["review_ids"]
        if outcome.get("statement_review"):
            line["statement_review"] = outcome["statement_review"]
        if outcome.get("groups") and not outcome.get("point"):
            line["groups"] = outcome["groups"]
        append_log(path, line)
        wrote += 1
        if tracker is not None and tracker.stopped:
            stopped = True
            break
    rows = read_log(path)
    write_result(root, field, rows)
    cost = 0.0
    if tracker is not None:
        cost = tracker.usd()
        print(tracker.line(), flush=True)
        _save_spend()
        if stopped or tracker.stopped:
            stopped = True
            limit = float(args.global_max_cost) if tracker.stop_scope == "global" else float(args.max_cost)
            scope = tracker.stop_scope or "field"
            print(f"stopped at {scope} max-cost ${limit:.2f}; unsent cells stay pending", flush=True)
    placed = sum(1 for row in rows if row.get("part") == "cell" and row.get("status") == "placed")
    print(f"field={field} cells={len(jobs)} placed={placed} wrote={wrote} stopped={stopped}", flush=True)
    return {
        "field": field,
        "pending": len(pending_jobs),
        "cells": len(jobs),
        "backend": backend,
        "model": model,
        "wrote": wrote,
        "placed": placed,
        "stopped": stopped,
        "cost": cost,
        "system": SYSTEM,
    }


def main(argv=None):
    args = parse_args(argv)
    result = run(args, root=Path(args.root) if args.root else None)
    if args.dry_run:
        print("dry-run only; no model was called")
    return 0 if not result.get("stopped") else 0


if __name__ == "__main__":
    sys.exit(main())
